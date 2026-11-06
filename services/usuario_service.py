import secrets

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from config.settings import settings
from models.usuario_model import Usuario
from repositories.usuario_repository import UsuarioRepository
from schemas.usuario_schema import UsuarioCrear
from utils.seguridad import hash_password
from utils.roles import es_rol_administrador


class UsuarioService:
    def __init__(self, db: Session):
        self.repository = UsuarioRepository(db)

    def crear_administrador_inicial(
        self,
        datos: UsuarioCrear,
        clave_bootstrap: str,
    ) -> Usuario:
        clave_configurada = settings.bootstrap_token

        if not clave_configurada:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="El alta inicial no está habilitada. Configura BOOTSTRAP_TOKEN.",
            )

        if not secrets.compare_digest(
    clave_bootstrap.encode("utf-8"),
    clave_configurada.encode("utf-8"),
):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Clave de bootstrap incorrecta.",
            )

        if self.repository.contar_usuarios() > 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El administrador inicial ya fue creado.",
            )

        correo = datos.correo.strip().lower()

        usuario = Usuario(
            rol_id=0,  # Se asigna el id real del rol en el repositorio.
            nombre=datos.nombre.strip(),
            correo=correo,
            password_hash=hash_password(datos.password),
            estado=True,
        )

        return self.repository.crear_administrador_inicial(usuario)

    def crear_nutricionista(
        self,
        datos: UsuarioCrear,
        usuario_actual: Usuario,
    ) -> Usuario:
        if not usuario_actual.rol or not es_rol_administrador(usuario_actual.rol.nombre):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Solo un administrador puede crear nutricionistas.",
            )

        correo = datos.correo.strip().lower()

        if self.repository.buscar_por_correo(correo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Ya existe un usuario con ese correo.",
            )

        rol = self.repository.buscar_rol("nutricionista")

        if not rol:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="No existe un rol activo llamado 'nutricionista'.",
            )

        usuario = Usuario(
            rol_id=rol.id,
            nombre=datos.nombre.strip(),
            correo=correo,
            password_hash=hash_password(datos.password),
            estado=True,
        )

        return self.repository.crear_usuario(usuario)

    def listar_usuarios(self, usuario_actual: Usuario) -> list[dict]:
        self._exigir_administrador(usuario_actual)
        return [
            {
                "id": usuario.id,
                "nombre": usuario.nombre,
                "correo": usuario.correo,
                "rol_id": usuario.rol_id,
                "rol": usuario.rol.nombre if usuario.rol else "sin_rol",
                "estado": usuario.estado,
                "creado": usuario.creado,
            }
            for usuario in self.repository.listar_usuarios()
        ]

    def actualizar_estado(
        self, usuario_id: int, estado: bool, usuario_actual: Usuario
    ) -> Usuario:
        self._exigir_administrador(usuario_actual)
        usuario = self.repository.obtener_por_id(usuario_id)
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado.")
        if usuario.id == usuario_actual.id and not estado:
            raise HTTPException(status_code=400, detail="No puedes desactivar tu propia cuenta.")
        es_admin = usuario.rol is not None and es_rol_administrador(usuario.rol.nombre)
        if es_admin and usuario.estado and not estado and self.repository.contar_administradores_activos() <= 1:
            raise HTTPException(status_code=409, detail="Debe permanecer al menos un administrador activo.")
        usuario.estado = estado
        return self.repository.guardar(usuario)

    @staticmethod
    def _exigir_administrador(usuario: Usuario) -> None:
        if not usuario.rol or not es_rol_administrador(usuario.rol.nombre):
            raise HTTPException(status_code=403, detail="Solo un administrador puede gestionar usuarios.")
