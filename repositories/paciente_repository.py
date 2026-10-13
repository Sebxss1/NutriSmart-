from sqlalchemy import func, select
from sqlalchemy.orm import Session

from models.paciente_model import Paciente
from models.rol_model import Rol
from models.usuario_model import Usuario


class PacienteRepository:
    def __init__(self, db: Session):
        self.db = db

    def buscar_rol_por_nombre(self, nombre: str) -> Rol | None:
        consulta = select(Rol).where(
            func.lower(Rol.nombre) == nombre.strip().lower(),
            Rol.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def crear(self, usuario: Usuario, paciente: Paciente) -> Paciente:
        try:
            self.db.add(usuario)
            self.db.flush()

            paciente.usuario_id = usuario.id
            self.db.add(paciente)
            self.db.commit()
            self.db.refresh(paciente)

            return paciente
        except Exception:
            self.db.rollback()
            raise

    def listar_de_nutricionista(
        self,
        nutricionista_id: int,
    ) -> list[Paciente]:
        consulta = (
            select(Paciente)
            .where(Paciente.nutricionista_id == nutricionista_id)
            .order_by(Paciente.apellidos, Paciente.nombres)
        )
        return list(self.db.scalars(consulta).all())

    def buscar_asignado(
        self,
        paciente_id: int,
        nutricionista_id: int,
    ) -> Paciente | None:
        consulta = select(Paciente).where(
            Paciente.id == paciente_id,
            Paciente.nutricionista_id == nutricionista_id,
        )
        return self.db.scalar(consulta)

    def guardar_cambios(self, paciente: Paciente) -> Paciente:
        try:
            self.db.commit()
            self.db.refresh(paciente)
            return paciente
        except Exception:
            self.db.rollback()
            raise