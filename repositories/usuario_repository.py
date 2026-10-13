from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.rol_model import Rol
from models.usuario_model import Usuario


class UsuarioRepository:
    def __init__(self, db: Session):
        self.db = db

    def contar_usuarios(self) -> int:
        return len(self.db.scalars(select(Usuario.id)).all())

    def buscar_por_correo(self, correo: str) -> Usuario | None:
        consulta = select(Usuario).where(
            func.lower(Usuario.correo) == correo.strip().lower()
        )
        return self.db.scalar(consulta)

    def buscar_rol(self, nombre: str) -> Rol | None:
        consulta = select(Rol).where(
            func.lower(Rol.nombre) == nombre.lower(),
            Rol.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def crear_administrador_inicial(self, usuario: Usuario) -> Usuario:
        try:
            roles = {
                "administrador": "Administra usuarios y configuración.",
                "nutricionista": "Gestiona pacientes y planes nutricionales.",
                "paciente": "Consulta su información y planes nutricionales.",
            }

            roles_encontrados = {
                rol.nombre.lower(): rol
                for rol in self.db.scalars(select(Rol)).all()
            }

            for nombre, descripcion in roles.items():
                if nombre not in roles_encontrados:
                    rol = Rol(nombre=nombre, descripcion=descripcion, estado=True)
                    self.db.add(rol)
                    roles_encontrados[nombre] = rol

            self.db.flush()

            usuario.rol_id = roles_encontrados["administrador"].id
            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)

            return usuario
        except Exception:
            self.db.rollback()
            raise

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        try:
            self.db.add(usuario)
            self.db.commit()
            self.db.refresh(usuario)
            return usuario
        except Exception:
            self.db.rollback()
            raise