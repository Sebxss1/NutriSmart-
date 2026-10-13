from sqlalchemy import and_, func
from sqlalchemy.orm import Session

from models.alimento_model import Alimento
from models.alimento_region_model import AlimentoRegion


class AlimentoRegionRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_alimento(self, alimento_id: int):
        return (
            self.db.query(Alimento)
            .filter(
                Alimento.id == alimento_id,
                Alimento.estado.is_(True),
            )
            .first()
        )

    def obtener_registro(
        self,
        alimento_id: int,
        municipio_divipola: str,
        fecha_referencia,
    ):
        return (
            self.db.query(AlimentoRegion)
            .filter(
                AlimentoRegion.alimento_id == alimento_id,
                AlimentoRegion.municipio_divipola == municipio_divipola,
                AlimentoRegion.fecha_referencia == fecha_referencia,
            )
            .first()
        )

    def listar_disponibles_por_municipio(self, municipio_divipola: str):
        ultimos_registros = (
            self.db.query(
                AlimentoRegion.alimento_id.label("alimento_id"),
                func.max(
                    AlimentoRegion.fecha_referencia
                ).label("fecha_referencia"),
            )
            .filter(
                AlimentoRegion.municipio_divipola == municipio_divipola,
                AlimentoRegion.estado.is_(True),
            )
            .group_by(AlimentoRegion.alimento_id)
            .subquery()
        )

        return (
            self.db.query(AlimentoRegion)
            .join(
                ultimos_registros,
                and_(
                    AlimentoRegion.alimento_id
                    == ultimos_registros.c.alimento_id,
                    AlimentoRegion.fecha_referencia
                    == ultimos_registros.c.fecha_referencia,
                ),
            )
            .filter(
                AlimentoRegion.municipio_divipola == municipio_divipola,
                AlimentoRegion.estado.is_(True),
                AlimentoRegion.disponible.is_(True),
            )
            .order_by(AlimentoRegion.alimento_id)
            .all()
        )

    def crear(self, registro: AlimentoRegion) -> AlimentoRegion:
        try:
            self.db.add(registro)
            self.db.commit()
            self.db.refresh(registro)
            return registro
        except Exception:
            self.db.rollback()
            raise