from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from models.restriccion_alimentaria_model import RestriccionAlimentaria
from models.usuario_model import Usuario
from repositories.restriccion_repository import RestriccionRepository
from schemas.restriccion_schema import (
    RestriccionActualizar,
    RestriccionCrear,
)


class RestriccionService:
    def __init__(self, db: Session):
        self.db = db
        self.repository = RestriccionRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _obtener_paciente_asignado(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ) -> Paciente:
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede gestionar restricciones alimentarias.",
            )

        paciente = (
            self.db.query(Paciente)
            .filter(
                Paciente.id == paciente_id,
                Paciente.nutricionista_id == usuario_actual.id,
                Paciente.estado.is_(True),
            )
            .first()
        )

        if not paciente:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o no está asignado a este nutricionista.",
            )

        return paciente

    def listar_restricciones(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente_asignado(
            paciente_id,
            usuario_actual,
        )
        return self.repository.listar_por_paciente(paciente.id)

    def crear_restriccion(
        self,
        paciente_id: int,
        datos: RestriccionCrear,
        usuario_actual: Usuario,
    ) -> RestriccionAlimentaria:
        paciente = self._obtener_paciente_asignado(
            paciente_id,
            usuario_actual,
        )

        restriccion = RestriccionAlimentaria(
            paciente_id=paciente.id,
            nombre=datos.nombre.strip(),
            tipo=datos.tipo,
            motivo=datos.motivo,
        )
        return self.repository.crear(restriccion)

    def actualizar_restriccion(
        self,
        paciente_id: int,
        restriccion_id: int,
        datos: RestriccionActualizar,
        usuario_actual: Usuario,
    ) -> RestriccionAlimentaria:
        paciente = self._obtener_paciente_asignado(
            paciente_id,
            usuario_actual,
        )

        restriccion = self.repository.obtener_de_paciente(
            restriccion_id,
            paciente.id,
        )

        if not restriccion:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Restricción no encontrada para este paciente.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        if "nombre" in cambios and cambios["nombre"] is not None:
            cambios["nombre"] = cambios["nombre"].strip()

        for campo, valor in cambios.items():
            setattr(restriccion, campo, valor)

        return self.repository.guardar(restriccion)