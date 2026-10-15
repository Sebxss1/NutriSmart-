from sqlalchemy.orm import Session

from models.consentimiento_model import Consentimiento


class ConsentimientoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_paciente(self, paciente_id: int):
        return (
            self.db.query(Consentimiento)
            .filter(
                Consentimiento.paciente_id == paciente_id,
                Consentimiento.estado.is_(True),
            )
            .order_by(Consentimiento.fecha_aceptacion.desc())
            .all()
        )

    def buscar_activo(
        self,
        paciente_id: int,
        consentimiento_id: int,
    ) -> Consentimiento | None:
        return (
            self.db.query(Consentimiento)
            .filter(
                Consentimiento.id == consentimiento_id,
                Consentimiento.paciente_id == paciente_id,
                Consentimiento.estado.is_(True),
            )
            .first()
        )

    def crear(self, consentimiento: Consentimiento) -> Consentimiento:
        try:
            self.db.add(consentimiento)
            self.db.commit()
            self.db.refresh(consentimiento)
            return consentimiento
        except Exception:
            self.db.rollback()
            raise

    def desactivar(self, consentimiento: Consentimiento) -> Consentimiento:
        try:
            consentimiento.estado = False
            self.db.commit()
            self.db.refresh(consentimiento)
            return consentimiento
        except Exception:
            self.db.rollback()
            raise