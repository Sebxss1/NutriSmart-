from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.control_nutricional_model import ControlNutricional
from models.paciente_model import Paciente
from models.usuario_model import Usuario
from repositories.control_nutricional_repository import (
    ControlNutricionalRepository,
)
from schemas.control_nutricional_schema import (
    ControlNutricionalActualizar,
    ControlNutricionalCrear,
)


class ControlNutricionalService:
    def __init__(self, db: Session):
        self.repository = ControlNutricionalRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _obtener_paciente(
        self,
        paciente_id: int,
    ) -> Paciente:
        paciente = self.repository.obtener_paciente(paciente_id)

        if not paciente or not paciente.estado:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o inactivo.",
            )

        return paciente

    def _validar_lectura(
        self,
        paciente: Paciente,
        usuario: Usuario,
    ):
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
                detail="No tienes permiso para consultar estos controles.",
            )

    def _validar_edicion(
        self,
        paciente: Paciente,
        usuario: Usuario,
    ):
        if self._obtener_rol(usuario) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede gestionar controles.",
            )

        if paciente.nutricionista_id != usuario.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente no está asignado a este nutricionista.",
            )

    def listar(
        self,
        paciente_id: int,
        usuario: Usuario,
    ):
        paciente = self._obtener_paciente(paciente_id)
        self._validar_lectura(paciente, usuario)

        return self.repository.listar_por_paciente(paciente.id)

    def crear(
        self,
        paciente_id: int,
        datos: ControlNutricionalCrear,
        usuario: Usuario,
    ) -> ControlNutricional:
        paciente = self._obtener_paciente(paciente_id)
        self._validar_edicion(paciente, usuario)

        control = ControlNutricional(
            paciente_id=paciente.id,
            registrado_por_id=usuario.id,
            fecha_control=datos.fecha_control,
            peso_kg=datos.peso_kg,
            estatura_cm=datos.estatura_cm,
            cintura_cm=datos.cintura_cm,
            observaciones=datos.observaciones,
        )

        return self.repository.crear(control)

    def actualizar(
        self,
        paciente_id: int,
        control_id: int,
        datos: ControlNutricionalActualizar,
        usuario: Usuario,
    ) -> ControlNutricional:
        paciente = self._obtener_paciente(paciente_id)
        self._validar_edicion(paciente, usuario)

        control = self.repository.obtener_control(
            paciente.id,
            control_id,
        )

        if not control:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control no encontrado para este paciente.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        if not cambios:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Envía al menos un campo para actualizar.",
            )

        campos_obligatorios = {
            "fecha_control",
            "peso_kg",
            "estatura_cm",
        }

        for campo in campos_obligatorios:
            if campo in cambios and cambios[campo] is None:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"El campo '{campo}' no puede quedar vacío.",
                )

        for campo, valor in cambios.items():
            setattr(control, campo, valor)

        return self.repository.guardar(control)

    def desactivar(
        self,
        paciente_id: int,
        control_id: int,
        usuario: Usuario,
    ):
        paciente = self._obtener_paciente(paciente_id)
        self._validar_edicion(paciente, usuario)

        control = self.repository.obtener_control(
            paciente.id,
            control_id,
        )

        if not control:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Control no encontrado para este paciente.",
            )

        self.repository.desactivar(control)