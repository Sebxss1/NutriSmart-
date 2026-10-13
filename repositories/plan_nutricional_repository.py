from sqlalchemy.orm import Session

from models.objetivo_nutricional_model import ObjetivoNutricional
from models.paciente_model import Paciente
from models.plan_nutricional_model import PlanNutricional
from models.version_plan_model import VersionPlan


class PlanNutricionalRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_paciente(self, paciente_id: int):
        return (
            self.db.query(Paciente)
            .filter(Paciente.id == paciente_id)
            .first()
        )

    def listar_planes_por_paciente(self, paciente_id: int):
        return (
            self.db.query(PlanNutricional)
            .filter(
                PlanNutricional.paciente_id == paciente_id,
                PlanNutricional.estado.is_(True),
            )
            .order_by(PlanNutricional.creado.desc())
            .all()
        )

    def obtener_plan(self, plan_id: int):
        return (
            self.db.query(PlanNutricional)
            .filter(
                PlanNutricional.id == plan_id,
                PlanNutricional.estado.is_(True),
            )
            .first()
        )

    def obtener_objetivo(self, objetivo_id: int, paciente_id: int):
        return (
            self.db.query(ObjetivoNutricional)
            .filter(
                ObjetivoNutricional.id == objetivo_id,
                ObjetivoNutricional.paciente_id == paciente_id,
                ObjetivoNutricional.estado.is_(True),
            )
            .first()
        )

    def crear_plan_con_version_inicial(
        self,
        plan: PlanNutricional,
        version: VersionPlan,
    ):
        try:
            self.db.add(plan)
            self.db.flush()

            version.plan_id = plan.id
            self.db.add(version)

            self.db.commit()
            self.db.refresh(plan)
            self.db.refresh(version)

            return plan
        except Exception:
            self.db.rollback()
            raise

    def listar_versiones(self, plan_id: int, solo_entregadas: bool = False):
        consulta = self.db.query(VersionPlan).filter(
            VersionPlan.plan_id == plan_id,
            VersionPlan.estado.is_(True),
        )

        if solo_entregadas:
            consulta = consulta.filter(
                VersionPlan.estado_plan == "ENTREGADO"
            )

        return consulta.order_by(VersionPlan.numero_version.desc()).all()

    def obtener_version(self, plan_id: int, version_id: int):
        return (
            self.db.query(VersionPlan)
            .filter(
                VersionPlan.plan_id == plan_id,
                VersionPlan.id == version_id,
                VersionPlan.estado.is_(True),
            )
            .first()
        )

    def obtener_ultima_version(self, plan_id: int):
        return (
            self.db.query(VersionPlan)
            .filter(VersionPlan.plan_id == plan_id)
            .order_by(VersionPlan.numero_version.desc())
            .first()
        )

    def crear_version(self, version: VersionPlan):
        try:
            self.db.add(version)
            self.db.commit()
            self.db.refresh(version)
            return version
        except Exception:
            self.db.rollback()
            raise

    def guardar_version(self, version: VersionPlan):
        try:
            self.db.commit()
            self.db.refresh(version)
            return version
        except Exception:
            self.db.rollback()
            raise