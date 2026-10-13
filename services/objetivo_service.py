from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.objetivo_nutricional_model import ObjetivoNutricional
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.objetivo_repository import ObjetivoRepository
from schemas.objetivo_schema import ObjetivoActualizar, ObjetivoCrear


class ObjetivoService:
    def __init__(self, db: Session):
        self.repository = ObjetivoRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _obtener_paciente_para_lectura(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ) -> Paciente:
        paciente = self.repository.obtener_paciente(paciente_id)

        if not paciente or not paciente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o inactivo.",
            )

        rol = self._obtener_rol(usuario_actual)

        es_nutricionista_asignado = (
            rol == "nutricionista"
            and paciente.nutricionista_id == usuario_actual.id
        )
        es_paciente_propio = (
            rol == "paciente"
            and paciente.usuario_id == usuario_actual.id
        )

        if not es_nutricionista_asignado and not es_paciente_propio:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para consultar los objetivos de este paciente.",
            )

        return paciente

    def _obtener_paciente_para_edicion(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ) -> Paciente:
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede gestionar objetivos nutricionales.",
            )

        paciente = self.repository.obtener_paciente(paciente_id)

        if (
            not paciente
            or not paciente.estado
            or paciente.nutricionista_id != usuario_actual.id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o no está asignado a este nutricionista.",
            )

        return paciente

    def listar_objetivos(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente_para_lectura(
            paciente_id,
            usuario_actual,
        )
        return self.repository.listar_por_paciente(paciente.id)

    def crear_objetivo(
        self,
        paciente_id: int,
        datos: ObjetivoCrear,
        usuario_actual: Usuario,
    ) -> ObjetivoNutricional:
        paciente = self._obtener_paciente_para_edicion(
            paciente_id,
            usuario_actual,
        )

        objetivo = ObjetivoNutricional(
            paciente_id=paciente.id,
            tipo=datos.tipo.strip(),
            descripcion=datos.descripcion,
            meta_cuantificable=datos.meta_cuantificable,
        )

        if datos.fecha_inicio is not None:
            objetivo.fecha_inicio = datos.fecha_inicio

        return self.repository.crear(objetivo)

    def actualizar_objetivo(
        self,
        paciente_id: int,
        objetivo_id: int,
        datos: ObjetivoActualizar,
        usuario_actual: Usuario,
    ) -> ObjetivoNutricional:
        paciente = self._obtener_paciente_para_edicion(
            paciente_id,
            usuario_actual,
        )

        objetivo = self.repository.obtener_objetivo(
            objetivo_id,
            paciente.id,
        )

        if not objetivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Objetivo no encontrado para este paciente.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        for campo, valor in cambios.items():
            if campo == "fecha_inicio" and valor is None:
                continue

            if campo == "tipo" and valor is not None:
                valor = valor.strip()

            setattr(objetivo, campo, valor)

        return self.repository.guardar(objetivo)