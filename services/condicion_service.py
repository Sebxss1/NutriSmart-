from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.condicion_medica_model import CondicionMedica
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.condicion_repository import CondicionRepository
from schemas.condicion_schema import CondicionMedicaCrear, PacienteCondicionCrear


class CondicionService:
    def __init__(self, db: Session):
        self.repository = CondicionRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def listar_condiciones(self, incluir_inactivas: bool = False):
        return self.repository.listar(incluir_inactivas=incluir_inactivas)

    def crear_condicion(
        self,
        datos: CondicionMedicaCrear,
        usuario_actual: Usuario,
    ) -> CondicionMedica:
        rol = self._obtener_rol(usuario_actual)

        if rol not in {"administrador", "nutricionista"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador o nutricionista puede crear condiciones médicas.",
            )

        condicion_existente = self.repository.obtener_por_codigo_o_nombre(
            codigo=datos.codigo,
            nombre=datos.nombre,
        )

        if condicion_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una condición médica con ese código o nombre.",
            )

        condicion = CondicionMedica(
            codigo=datos.codigo,
            nombre=datos.nombre,
            descripcion=datos.descripcion,
        )
        return self.repository.crear(condicion)

    def listar_condiciones_paciente(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente_asignado(paciente_id, usuario_actual)

        return self.repository.listar_por_paciente(paciente.id)

    def agregar_condicion_a_paciente(
        self,
        paciente_id: int,
        datos: PacienteCondicionCrear,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente_asignado(paciente_id, usuario_actual)

        condicion = self.repository.obtener_condicion(datos.condicion_id)
        if not condicion or not condicion.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="La condición médica no existe o está inactiva.",
            )

        asociacion_existente = self.repository.obtener_asociacion(
            paciente_id=paciente.id,
            condicion_id=condicion.id,
        )
        if asociacion_existente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Esta condición ya está registrada para el paciente.",
            )

        return self.repository.agregar_a_paciente(
            paciente_id=paciente.id,
            condicion_id=condicion.id,
            observaciones=datos.observaciones,
        )

    def _obtener_paciente_asignado(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ) -> Paciente:
        rol = self._obtener_rol(usuario_actual)

        if rol != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede gestionar las condiciones de un paciente.",
            )

        paciente = (
            self.repository.db.query(Paciente)
            .filter(
                Paciente.id == paciente_id,
                Paciente.nutricionista_id == usuario_actual.id,
            )
            .first()
        )

        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o no está asignado a este nutricionista.",
            )

        return paciente