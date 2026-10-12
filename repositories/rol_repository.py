from sqlalchemy import select
from sqlalchemy.orm import Session

from models.rol_model import Rol


class RolRepository:
    
    def __init__(self, db:Session):
        self.db = db
        
        
    def listar_activos(self) -> list[Rol]:
        consulta = (
            select(Rol)
            .where(Rol.estado.is_(True))
            .order_by(Rol.nombre)
        )
        return list(self.db.scalars(consulta).all())
        