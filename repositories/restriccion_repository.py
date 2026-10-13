from sqlalchemy.orm import Session

from models.restriccion_alimentaria_model import RestriccionAlimentaria


class RestriccionRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_por_paciente(
        self,
        paciente_id: int,
        incluir_inactivas: bool = False,
    ):
        consulta = self.db.query(RestriccionAlimentaria).filter(
            RestriccionAlimentaria.paciente_id == paciente_id
        )

        if not incluir_inactivas:
            consulta = consulta.filter(
                RestriccionAlimentaria.estado.is_(True)
            )

        return consulta.order_by(RestriccionAlimentaria.nombre).all()

    def obtener_de_paciente(
        self,
        restriccion_id: int,
        paciente_id: int,
    ):
        return (
            self.db.query(RestriccionAlimentaria)
            .filter(
                RestriccionAlimentaria.id == restriccion_id,
                RestriccionAlimentaria.paciente_id == paciente_id,
            )
            .first()
        )

    def crear(
        self,
        restriccion: RestriccionAlimentaria,
    ) -> RestriccionAlimentaria:
        try:
            self.db.add(restriccion)
            self.db.commit()
            self.db.refresh(restriccion)
            return restriccion
        except Exception:
            self.db.rollback()
            raise

    def guardar(
        self,
        restriccion: RestriccionAlimentaria,
    ) -> RestriccionAlimentaria:
        try:
            self.db.commit()
            self.db.refresh(restriccion)
            return restriccion
        except Exception:
            self.db.rollback()
            raise