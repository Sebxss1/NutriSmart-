from sqlalchemy.orm import Session

from models.alimento_model import Alimento


class AlimentoRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, busqueda: str | None = None, incluir_inactivos: bool = False):
        consulta = self.db.query(Alimento)
        if not incluir_inactivos:
            consulta = consulta.filter(Alimento.estado.is_(True))

        if busqueda:
            termino = f"%{busqueda.strip()}%"
            consulta = consulta.filter(Alimento.nombre.ilike(termino))

        return consulta.order_by(Alimento.nombre).all()

    def obtener_por_id(self, alimento_id: int) -> Alimento | None:
        return self.db.get(Alimento, alimento_id)

    def guardar(self, alimento: Alimento) -> Alimento:
        try:
            self.db.commit()
            self.db.refresh(alimento)
            return alimento
        except Exception:
            self.db.rollback()
            raise

    def obtener_por_codigo(self, codigo: str):
        return (
            self.db.query(Alimento)
            .filter(Alimento.codigo == codigo)
            .first()
        )

    def crear(self, alimento: Alimento) -> Alimento:
        try:
            self.db.add(alimento)
            self.db.commit()
            self.db.refresh(alimento)
            return alimento
        except Exception:
            self.db.rollback()
            raise
