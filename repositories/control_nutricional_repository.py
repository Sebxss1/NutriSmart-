from sqlalchemy import select
from sqlalchemy.orm import Session

from models.control_nutricional_model import ControlNutricional
from models.paciente_model import Paciente


class ControlNutricionalRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_paciente(self, paciente_id: int) -> Paciente | None:
        consulta = select(Paciente).where(Paciente.id == paciente_id)
        return self.db.scalar(consulta)

    def listar_por_paciente(
        self,
        paciente_id: int,
    ) -> list[ControlNutricional]:
        consulta = (
            select(ControlNutricional)
            .where(
                ControlNutricional.paciente_id == paciente_id,
                ControlNutricional.estado.is_(True),
            )
            .order_by(ControlNutricional.fecha_control.desc())
        )
        return list(self.db.scalars(consulta).all())

    def obtener_control(
        self,
        paciente_id: int,
        control_id: int,
    ) -> ControlNutricional | None:
        consulta = select(ControlNutricional).where(
            ControlNutricional.id == control_id,
            ControlNutricional.paciente_id == paciente_id,
            ControlNutricional.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def crear(self, control: ControlNutricional) -> ControlNutricional:
        try:
            self.db.add(control)
            self.db.commit()
            self.db.refresh(control)
            return control
        except Exception:
            self.db.rollback()
            raise

    def guardar(self, control: ControlNutricional) -> ControlNutricional:
        try:
            self.db.commit()
            self.db.refresh(control)
            return control
        except Exception:
            self.db.rollback()
            raise

    def desactivar(self, control: ControlNutricional):
        try:
            control.estado = False
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise