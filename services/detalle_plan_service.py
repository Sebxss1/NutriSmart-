from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.detalle_plan_model import DetallePlan
from models.paciente_model import Paciente
from models.plan_nutricional_model import PlanNutricional
from models.usuario_model import Usuario
from models.version_plan_model import VersionPlan
from repositories.detalle_plan_repository import DetallePlanRepository
from schemas.detalle_plan_schema import (
    DetallePlanActualizar,
    DetallePlanCrear,
)


class DetallePlanService:
    def __init__(self, db: Session):
        self.repository = DetallePlanRepository(db)

    @staticmethod
    def _obtener_rol(usuario: Usuario) -> str:
        if not usuario.rol:
            return ""
        return usuario.rol.nombre.lower()

    def _obtener_contexto(
        self,
        version_id: int,
    ) -> tuple[VersionPlan, PlanNutricional, Paciente]:
        fila = self.repository.obtener_contexto_version(version_id)

        if not fila:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Versión del plan no encontrada.",
            )

        return fila

    def _validar_acceso_lectura(
        self,
        version: VersionPlan,
        paciente: Paciente,
        usuario: Usuario,
    ):
        rol = self._obtener_rol(usuario)

        es_nutricionista_asignado = (
            rol == "nutricionista"
            and paciente.nutricionista_id == usuario.id
        )
        es_paciente_propietario = (
            rol == "paciente"
            and paciente.usuario_id == usuario.id
        )

        if not es_nutricionista_asignado and not es_paciente_propietario:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para consultar estos detalles.",
            )

        if es_paciente_propietario and version.estado_plan != "ENTREGADO":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo puedes consultar versiones entregadas.",
            )

    def _validar_edicion(
        self,
        version: VersionPlan,
        paciente: Paciente,
        usuario: Usuario,
    ):
        if self._obtener_rol(usuario) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede modificar el plan.",
            )

        if paciente.nutricionista_id != usuario.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente no está asignado a este nutricionista.",
            )

        if version.estado_plan != "BORRADOR":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Solo se puede editar una versión en estado BORRADOR.",
            )

    def listar_detalles(
        self,
        version_id: int,
        usuario: Usuario,
    ):
        version, _, paciente = self._obtener_contexto(version_id)
        self._validar_acceso_lectura(version, paciente, usuario)

        return self.repository.listar_por_version(version_id)

    def crear_detalle(
        self,
        version_id: int,
        datos: DetallePlanCrear,
        usuario: Usuario,
    ):
        version, _, paciente = self._obtener_contexto(version_id)
        self._validar_edicion(version, paciente, usuario)

        if datos.alimento_id is not None:
            alimento = self.repository.obtener_alimento_activo(
                datos.alimento_id
            )
            if not alimento:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alimento no encontrado o inactivo.",
                )

        if datos.receta_id is not None:
            receta = self.repository.obtener_receta_activa(datos.receta_id)
            if not receta:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Receta no encontrada o inactiva.",
                )

        detalle = DetallePlan(
            version_plan_id=version_id,
            dia=datos.dia,
            tipo_comida=datos.tipo_comida,
            alimento_id=datos.alimento_id,
            receta_id=datos.receta_id,
            cantidad=datos.cantidad,
            unidad=datos.unidad.strip(),
        )

        return self.repository.crear(detalle)

    def actualizar_detalle(
        self,
        version_id: int,
        detalle_id: int,
        datos: DetallePlanActualizar,
        usuario: Usuario,
    ):
        version, _, paciente = self._obtener_contexto(version_id)
        self._validar_edicion(version, paciente, usuario)

        detalle = self.repository.obtener_detalle(version_id, detalle_id)
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado para esta versión.",
            )

        cambios = datos.model_dump(exclude_unset=True)

        alimento_id = cambios.get("alimento_id", detalle.alimento_id)
        receta_id = cambios.get("receta_id", detalle.receta_id)

        if (alimento_id is None) == (receta_id is None):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="El detalle debe tener un alimento o una receta, pero no ambos.",
            )

        if alimento_id is not None:
            if not self.repository.obtener_alimento_activo(alimento_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Alimento no encontrado o inactivo.",
                )

        if receta_id is not None:
            if not self.repository.obtener_receta_activa(receta_id):
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Receta no encontrada o inactiva.",
                )

        for campo, valor in cambios.items():
            if campo == "unidad" and valor is not None:
                valor = valor.strip()
            setattr(detalle, campo, valor)

        return self.repository.guardar(detalle)

    def eliminar_detalle(
        self,
        version_id: int,
        detalle_id: int,
        usuario: Usuario,
    ):
        version, _, paciente = self._obtener_contexto(version_id)
        self._validar_edicion(version, paciente, usuario)

        detalle = self.repository.obtener_detalle(version_id, detalle_id)
        if not detalle:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Detalle no encontrado para esta versión.",
            )

        self.repository.desactivar(detalle)