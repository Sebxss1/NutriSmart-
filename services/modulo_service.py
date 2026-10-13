from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from models.modulo_model import Modulo
from models.usuario_model import Usuario
from repositories.modulo_repository import ModuloRepository
from schemas.modulo_schema import ModuloCrear


class ModuloService:
    def __init__(self, db: Session):
        self.repository = ModuloRepository(db)

    @staticmethod
    def _es_administrador(usuario: Usuario) -> bool:
        return (
            usuario.rol is not None
            and usuario.rol.nombre.lower() == "administrador"
        )

    def _exigir_administrador(self, usuario: Usuario):
        if not self._es_administrador(usuario):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador puede gestionar módulos y accesos.",
            )

    def listar_modulos(self):
        return self.repository.listar_activos()

    def crear_modulo(
        self,
        datos: ModuloCrear,
        usuario_actual: Usuario,
    ):
        self._exigir_administrador(usuario_actual)

        codigo = datos.codigo.strip().lower()

        if self.repository.obtener_por_codigo(codigo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un módulo con ese código.",
            )

        modulo = Modulo(
            codigo=codigo,
            nombre=datos.nombre.strip(),
            descripcion=(
                datos.descripcion.strip()
                if datos.descripcion
                else None
            ),
        )

        try:
            return self.repository.crear(modulo)
        except IntegrityError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No se pudo crear el módulo; verifica que el código no esté repetido.",
            ) from error

    def listar_modulos_por_rol(
        self,
        rol_id: int,
        usuario_actual: Usuario,
    ):
        self._exigir_administrador(usuario_actual)

        rol = self.repository.obtener_rol(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado o inactivo.",
            )

        return self.repository.listar_modulos_por_rol(rol_id)

    def actualizar_modulos_del_rol(
        self,
        rol_id: int,
        modulo_ids: list[int],
        usuario_actual: Usuario,
    ):
        self._exigir_administrador(usuario_actual)

        rol = self.repository.obtener_rol(rol_id)
        if not rol:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Rol no encontrado o inactivo.",
            )

        ids_solicitados = set(modulo_ids)
        modulos_activos = self.repository.obtener_modulos_por_ids(
            ids_solicitados
        )
        ids_validos = {modulo.id for modulo in modulos_activos}

        if ids_validos != ids_solicitados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Uno o más módulos no existen o están inactivos.",
            )

        return self.repository.reemplazar_modulos_del_rol(
            rol_id,
            ids_solicitados,
        )