from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.alimento_model import Alimento
from models.usuario_model import Usuario
from repositories.alimento_repository import AlimentoRepository
from schemas.alimento_schema import AlimentoActualizar, AlimentoCrear
from utils.roles import es_rol_administrador


class AlimentoService:
    def __init__(self, db: Session):
        self.repository = AlimentoRepository(db)

    def listar_alimentos(self, busqueda: str | None = None, incluir_inactivos: bool = False, usuario_actual: Usuario | None = None):
        es_admin = bool(usuario_actual and usuario_actual.rol and es_rol_administrador(usuario_actual.rol.nombre))
        return self.repository.listar(busqueda, incluir_inactivos and es_admin)

    def crear_alimento(
        self,
        datos: AlimentoCrear,
        usuario_actual: Usuario,
    ) -> Alimento:
        rol = usuario_actual.rol.nombre.lower() if usuario_actual.rol else ""

        if not (es_rol_administrador(rol) or rol == "nutricionista"):
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

    def actualizar_alimento(self, alimento_id: int, datos: AlimentoActualizar, usuario_actual: Usuario, estado: bool | None = None) -> Alimento:
        rol = usuario_actual.rol.nombre.lower() if usuario_actual.rol else ""
        if not es_rol_administrador(rol):
            raise HTTPException(status_code=403, detail="Solo un administrador puede modificar el catálogo.")
        alimento = self.repository.obtener_por_id(alimento_id)
        if not alimento:
            raise HTTPException(status_code=404, detail="Alimento no encontrado.")
        cambios = datos.model_dump(exclude_unset=True)
        for campo, valor in cambios.items():
            if isinstance(valor, str):
                valor = valor.strip()
            setattr(alimento, campo, valor)
        if estado is not None:
            alimento.estado = estado
        return self.repository.guardar(alimento)

    def actualizar_estado(self, alimento_id: int, estado: bool, usuario_actual: Usuario) -> Alimento:
        return self.actualizar_alimento(alimento_id, AlimentoActualizar(), usuario_actual, estado)
