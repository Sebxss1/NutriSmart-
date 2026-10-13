from sqlalchemy import select
from sqlalchemy.orm import Session

from models.alimento_model import Alimento
from models.detalle_plan_model import DetallePlan
from models.paciente_model import Paciente
from models.plan_nutricional_model import PlanNutricional
from models.receta_model import Receta
from models.version_plan_model import VersionPlan


class DetallePlanRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_contexto_version(self, version_id: int):
        consulta = (
            select(VersionPlan, PlanNutricional, Paciente)
            .join(
                PlanNutricional,
                PlanNutricional.id == VersionPlan.plan_id,
            )
            .join(
                Paciente,
                Paciente.id == PlanNutricional.paciente_id,
            )
            .where(
                VersionPlan.id == version_id,
                VersionPlan.estado.is_(True),
                PlanNutricional.estado.is_(True),
                Paciente.estado.is_(True),
            )
        )
        fila = self.db.execute(consulta).first()
        return fila

    def listar_por_version(self, version_id: int) -> list[DetallePlan]:
        consulta = (
            select(DetallePlan)
            .where(
                DetallePlan.version_plan_id == version_id,
                DetallePlan.estado.is_(True),
            )
            .order_by(
                DetallePlan.dia,
                DetallePlan.tipo_comida,
                DetallePlan.id,
            )
        )
        return list(self.db.scalars(consulta).all())

    def obtener_detalle(
        self,
        version_id: int,
        detalle_id: int,
    ) -> DetallePlan | None:
        consulta = select(DetallePlan).where(
            DetallePlan.id == detalle_id,
            DetallePlan.version_plan_id == version_id,
            DetallePlan.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def obtener_alimento_activo(self, alimento_id: int) -> Alimento | None:
        consulta = select(Alimento).where(
            Alimento.id == alimento_id,
            Alimento.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def obtener_receta_activa(self, receta_id: int) -> Receta | None:
        consulta = select(Receta).where(
            Receta.id == receta_id,
            Receta.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def crear(self, detalle: DetallePlan) -> DetallePlan:
        try:
            self.db.add(detalle)
            self.db.commit()
            self.db.refresh(detalle)
            return detalle
        except Exception:
            self.db.rollback()
            raise

    def guardar(self, detalle: DetallePlan) -> DetallePlan:
        try:
            self.db.commit()
            self.db.refresh(detalle)
            return detalle
        except Exception:
            self.db.rollback()
            raise

    def desactivar(self, detalle: DetallePlan) -> None:
        try:
            detalle.estado = False
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise