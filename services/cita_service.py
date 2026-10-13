from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.cita_model import Cita
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.cita_repository import CitaRepository
from schemas.cita_schema import CitaActualizar, CitaCrear


class CitaService:
    def __init__(self, db: Session):
        self.repository = CitaRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _obtener_paciente(self, paciente_id: int) -> Paciente:
        paciente = self.repository.obtener_paciente(paciente_id)

        if not paciente or not paciente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o inactivo.",
            )

        return paciente

    def _validar_lectura(self, paciente: Paciente, usuario: Usuario):
        rol = self._obtener_rol(usuario)

        es_nutricionista_asignado = (
            rol == "nutricionista"
            and paciente.nutricionista_id == usuario.id
        )
        es_paciente_propio = (
            rol == "paciente"
            and paciente.usuario_id == usuario.id
        )

        if not es_nutricionista_asignado and not es_paciente_propio:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para consultar estas citas.",
            )

    def _validar_nutricionista(self, paciente: Paciente, usuario: Usuario):
        if self._obtener_rol(usuario) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede gestionar esta cita.",
            )

        if paciente.nutricionista_id != usuario.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente no está asignado a este nutricionista.",
            )

    def listar(self, paciente_id: int, usuario: Usuario):
        paciente = self._obtener_paciente(paciente_id)
        self._validar_lectura(paciente, usuario)
        return self.repository.listar_por_paciente(paciente.id)

    def crear(
        self,
        paciente_id: int,
        datos: CitaCrear,
        usuario: Usuario,
    ) -> Cita:
        paciente = self._obtener_paciente(paciente_id)
        self._validar_nutricionista(paciente, usuario)

        if self.repository.existe_conflicto(
            paciente.id,
            usuario.id,
            datos.inicio,
            datos.fin,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El paciente o el nutricionista ya tiene una cita en ese horario.",
            )

        cita = Cita(
            paciente_id=paciente.id,
            nutricionista_id=usuario.id,
            inicio=datos.inicio,
            fin=datos.fin,
            estado_cita="PROGRAMADA",
            motivo=datos.motivo,
        )

        return self.repository.crear(cita)

    def reprogramar(
        self,
        paciente_id: int,
        cita_id: int,
        datos: CitaActualizar,
        usuario: Usuario,
    ) -> Cita:
        paciente = self._obtener_paciente(paciente_id)
        self._validar_nutricionista(paciente, usuario)

        cita = self.repository.obtener_cita(paciente.id, cita_id)

        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada para este paciente.",
            )

        if cita.estado_cita not in {"PROGRAMADA", "REPROGRAMADA"}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se pueden reprogramar citas pendientes.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        if not cambios:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Envía al menos un campo para actualizar.",
            )

        inicio_nuevo = cambios.get("inicio", cita.inicio)
        fin_nuevo = cambios.get("fin", cita.fin)

        if inicio_nuevo is None or fin_nuevo is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La cita debe tener fecha de inicio y fin.",
            )

        if fin_nuevo <= inicio_nuevo:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="La hora de fin debe ser posterior a la hora de inicio.",
            )

        cambio_horario = "inicio" in cambios or "fin" in cambios

        if cambio_horario and self.repository.existe_conflicto(
            paciente.id,
            cita.nutricionista_id,
            inicio_nuevo,
            fin_nuevo,
            excluir_cita_id=cita.id,
        ):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El paciente o el nutricionista ya tiene una cita en ese horario.",
            )

        for campo, valor in cambios.items():
            setattr(cita, campo, valor)

        if cambio_horario:
            cita.estado_cita = "REPROGRAMADA"

        return self.repository.guardar(cita)

    def cambiar_estado(
        self,
        paciente_id: int,
        cita_id: int,
        nuevo_estado: str,
        usuario: Usuario,
    ) -> Cita:
        paciente = self._obtener_paciente(paciente_id)
        self._validar_lectura(paciente, usuario)

        cita = self.repository.obtener_cita(paciente.id, cita_id)

        if not cita:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cita no encontrada para este paciente.",
            )

        rol = self._obtener_rol(usuario)
        es_nutricionista = rol == "nutricionista"
        es_paciente = rol == "paciente"

        if es_nutricionista:
            self._validar_nutricionista(paciente, usuario)
        elif nuevo_estado != "CANCELADA":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente solo puede cancelar su cita.",
            )

        if cita.estado_cita not in {"PROGRAMADA", "REPROGRAMADA"}:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="La cita ya no está pendiente.",
            )

        if es_paciente and nuevo_estado != "CANCELADA":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente solo puede cancelar su cita.",
            )

        cita.estado_cita = nuevo_estado
        return self.repository.guardar(cita)