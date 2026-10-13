from sqlalchemy.orm import Session

from models.alimento_model import Alimento
from models.ingrediente_receta_model import IngredienteReceta
from models.receta_model import Receta


class RecetaRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, busqueda: str | None = None):
        consulta = self.db.query(Receta).filter(Receta.estado.is_(True))

        if busqueda:
            termino = f"%{busqueda.strip()}%"
            consulta = consulta.filter(Receta.nombre.ilike(termino))

        return consulta.order_by(Receta.nombre).all()

    def obtener(self, receta_id: int):
        return (
            self.db.query(Receta)
            .filter(Receta.id == receta_id)
            .first()
        )

    def obtener_por_codigo(self, codigo: str):
        return (
            self.db.query(Receta)
            .filter(Receta.codigo == codigo)
            .first()
        )

    def crear(self, receta: Receta) -> Receta:
        try:
            self.db.add(receta)
            self.db.commit()
            self.db.refresh(receta)
            return receta
        except Exception:
            self.db.rollback()
            raise

    def obtener_alimento(self, alimento_id: int):
        return (
            self.db.query(Alimento)
            .filter(
                Alimento.id == alimento_id,
                Alimento.estado.is_(True),
            )
            .first()
        )

    def listar_ingredientes(self, receta_id: int):
        return (
            self.db.query(IngredienteReceta)
            .filter(
                IngredienteReceta.receta_id == receta_id,
                IngredienteReceta.estado.is_(True),
            )
            .order_by(IngredienteReceta.id)
            .all()
        )

    def obtener_ingrediente(self, receta_id: int, alimento_id: int):
        return (
            self.db.query(IngredienteReceta)
            .filter(
                IngredienteReceta.receta_id == receta_id,
                IngredienteReceta.alimento_id == alimento_id,
            )
            .first()
        )

    def crear_ingrediente(
        self,
        ingrediente: IngredienteReceta,
    ) -> IngredienteReceta:
        try:
            self.db.add(ingrediente)
            self.db.commit()
            self.db.refresh(ingrediente)
            return ingrediente
        except Exception:
            self.db.rollback()
            raise
        
    def obtener_ingrediente_por_id(self, receta_id: int, ingrediente_id: int):
        return (
        self.db.query(IngredienteReceta)
        .filter(
            IngredienteReceta.id == ingrediente_id,
            IngredienteReceta.receta_id == receta_id,
        )
        .first()
    )

    def guardar_receta(self, receta: Receta):
        try:
            self.db.commit()
            self.db.refresh(receta)
            return receta
        except Exception:
            self.db.rollback()
            raise

    def desactivar_receta(self, receta: Receta):
        try:
            receta.estado = False
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise

    def guardar_ingrediente(self, ingrediente: IngredienteReceta):
        try:
            self.db.commit()
            self.db.refresh(ingrediente)
            return ingrediente
        except Exception:
            self.db.rollback()
            raise

    def desactivar_ingrediente(self, ingrediente: IngredienteReceta):
        try:
            ingrediente.estado = False
            self.db.commit()
        except Exception:
            self.db.rollback()
            raise