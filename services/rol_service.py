from sqlalchemy.orm import Session

from repositories.rol_repository import RolRepository


class RolService:
    def __init__(self, db: Session):
        self.rol_repository = RolRepository(db)
        
        
    def listar_roles(self):
        return self.rol_repository.listar_activos()
        