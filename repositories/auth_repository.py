from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.usuario_model import Usuario


class AuthRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_por_correo(self, correo: str) -> Usuario | None:
        correo_normalizado = correo.strip().lower()

        consulta = select(Usuario).where(
            func.lower(Usuario.correo) == correo_normalizado
        )

        return self.db.scalar(consulta)

    def buscar_por_id(self, usuario_id: int) -> Usuario | None:
        consulta = select(Usuario).where(Usuario.id == usuario_id)
        return self.db.scalar(consulta)