from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.alimento_model import Alimento
from models.usuario_model import Usuario
from repositories.alimento_repository import AlimentoRepository
from schemas.alimento_schema import AlimentoCrear


class AlimentoService:
    def __init__(self, db: Session):
        self.repository = AlimentoRepository(db)

    def listar_alimentos(self, busqueda: str | None = None):
        return self.repository.listar(busqueda)

    def crear_alimento(
        self,
        datos: AlimentoCrear,
        usuario_actual: Usuario,
    ) -> Alimento:
        rol = usuario_actual.rol.nombre.lower() if usuario_actual.rol else ""

        if rol not in {"administrador", "nutricionista"}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador o nutricionista puede agregar alimentos.",
            )

        if self.repository.obtener_por_codigo(datos.codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un alimento con ese código.",
            )

        alimento = Alimento(
            **datos.model_dump(exclude={"codigo", "nombre", "categoria"}),
            codigo=datos.codigo.strip().upper(),
            nombre=datos.nombre.strip(),
            categoria=datos.categoria.strip(),
        )

        return self.repository.crear(alimento)