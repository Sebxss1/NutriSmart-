from sqlalchemy.orm import Session

from models.objetivo_nutricional_model import ObjetivoNutricional
from models.paciente_model import Paciente


class ObjetivoRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_paciente(self, paciente_id: int):
        return (
            self.db.query(Paciente)
            .filter(Paciente.id == paciente_id)
            .first()
        )

    def listar_por_paciente(self, paciente_id: int):
        return (
            self.db.query(ObjetivoNutricional)
            .filter(
                ObjetivoNutricional.paciente_id == paciente_id,
                ObjetivoNutricional.estado.is_(True),
            )
            .order_by(ObjetivoNutricional.fecha_inicio.desc())
            .all()
        )

    def obtener_objetivo(self, objetivo_id: int, paciente_id: int):
        return (
            self.db.query(ObjetivoNutricional)
            .filter(
                ObjetivoNutricional.id == objetivo_id,
                ObjetivoNutricional.paciente_id == paciente_id,
            )
            .first()
        )

    def crear(self, objetivo: ObjetivoNutricional):
        try:
            self.db.add(objetivo)
            self.db.commit()
            self.db.refresh(objetivo)
            return objetivo
        except Exception:
            self.db.rollback()
            raise

    def guardar(self, objetivo: ObjetivoNutricional):
        try:
            self.db.commit()
            self.db.refresh(objetivo)
            return objetivo
        except Exception:
            self.db.rollback()
            raise