from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from models.plan_nutricional_model import PlanNutricional
from models.usuario_model import Usuario
from models.version_plan_model import VersionPlan
from repositories.plan_nutricional_repository import (
    PlanNutricionalRepository,
)
from schemas.plan_nutricional_schema import (
    PlanNutricionalCrear,
    VersionPlanCrear,
)


class PlanNutricionalService:
    def __init__(self, db: Session):
        self.repository = PlanNutricionalRepository(db)

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
                detail="No tienes permiso para consultar estos planes.",
            )

        return paciente

    def _obtener_plan_para_lectura(
        self,
        plan_id: int,
        usuario_actual: Usuario,
    ) -> PlanNutricional:
        plan = self.repository.obtener_plan(plan_id)

        if not plan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Plan nutricional no encontrado.",
            )

        self._obtener_paciente_para_lectura(
            plan.paciente_id,
            usuario_actual,
        )
        return plan

    def _validar_nutricionista_del_plan(
        self,
        plan: PlanNutricional,
        usuario_actual: Usuario,
    ):
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede modificar el plan.",
            )

        paciente = self.repository.obtener_paciente(plan.paciente_id)

        if not paciente or paciente.nutricionista_id != usuario_actual.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El paciente no está asignado a este nutricionista.",
            )

    def listar_planes(
        self,
        paciente_id: int,
        usuario_actual: Usuario,
    ):
        paciente = self._obtener_paciente_para_lectura(
            paciente_id,
            usuario_actual,
        )
        return self.repository.listar_planes_por_paciente(paciente.id)

    def crear_plan(
        self,
        paciente_id: int,
        datos: PlanNutricionalCrear,
        usuario_actual: Usuario,
    ):
        if self._obtener_rol(usuario_actual) != "nutricionista":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un nutricionista puede crear planes.",
            )

        paciente = self.repository.obtener_paciente(paciente_id)

        if (
            not paciente
            or not paciente.estado
            or paciente.nutricionista_id != usuario_actual.id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Paciente no encontrado o no asignado a este nutricionista.",
            )

        if datos.objetivo_id is not None:
            objetivo = self.repository.obtener_objetivo(
                datos.objetivo_id,
                paciente.id,
            )
            if not objetivo:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="El objetivo no existe o no pertenece a este paciente.",
                )

        plan = PlanNutricional(
            paciente_id=paciente.id,
            objetivo_id=datos.objetivo_id,
            creado_por_id=usuario_actual.id,
            nombre=datos.nombre.strip(),
        )

        version_inicial = VersionPlan(
            numero_version=1,
            estado_plan="BORRADOR",
        )

        return self.repository.crear_plan_con_version_inicial(
            plan,
            version_inicial,
        )

    def listar_versiones(
        self,
        plan_id: int,
        usuario_actual: Usuario,
    ):
        plan = self._obtener_plan_para_lectura(plan_id, usuario_actual)

        es_paciente = self._obtener_rol(usuario_actual) == "paciente"

        return self.repository.listar_versiones(
            plan.id,
            solo_entregadas=es_paciente,
        )

    def crear_version(
        self,
        plan_id: int,
        datos: VersionPlanCrear,
        usuario_actual: Usuario,
    ):
        plan = self._obtener_plan_para_lectura(plan_id, usuario_actual)
        self._validar_nutricionista_del_plan(plan, usuario_actual)

        ultima_version = self.repository.obtener_ultima_version(plan.id)

        if ultima_version and ultima_version.estado_plan == "BORRADOR":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe una versión en borrador para este plan.",
            )

        numero = ultima_version.numero_version + 1 if ultima_version else 1

        version = VersionPlan(
            plan_id=plan.id,
            numero_version=numero,
            estado_plan="BORRADOR",
            notas=datos.notas,
        )

        return self.repository.crear_version(version)

    def actualizar_estado_version(
        self,
        plan_id: int,
        version_id: int,
        nuevo_estado: str,
        usuario_actual: Usuario,
    ):
        plan = self._obtener_plan_para_lectura(plan_id, usuario_actual)
        self._validar_nutricionista_del_plan(plan, usuario_actual)

        version = self.repository.obtener_version(plan.id, version_id)

        if not version:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Versión no encontrada para este plan.",
            )

        transiciones_validas = {
            "BORRADOR": "APROBADO",
            "APROBADO": "ENTREGADO",
        }

        estado_siguiente = transiciones_validas.get(version.estado_plan)

        if nuevo_estado != estado_siguiente:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"No se puede cambiar de {version.estado_plan} "
                    f"a {nuevo_estado}."
                ),
            )

        version.estado_plan = nuevo_estado

        if nuevo_estado == "APROBADO":
            version.aprobado_por_id = usuario_actual.id
            version.fecha_aprobacion = datetime.now(timezone.utc)

        return self.repository.guardar_version(version)