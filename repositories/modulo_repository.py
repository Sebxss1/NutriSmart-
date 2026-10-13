from sqlalchemy import select
from sqlalchemy.orm import Session

from models.modulo_model import Modulo
from models.moduloxrol_model import ModuloPorRol
from models.rol_model import Rol


class ModuloRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar_activos(self) -> list[Modulo]:
        consulta = (
            select(Modulo)
            .where(Modulo.estado.is_(True))
            .order_by(Modulo.nombre)
        )
        return list(self.db.scalars(consulta).all())

    def obtener_por_codigo(self, codigo: str) -> Modulo | None:
        consulta = select(Modulo).where(Modulo.codigo == codigo)
        return self.db.scalar(consulta)

    def crear(self, modulo: Modulo) -> Modulo:
        try:
            self.db.add(modulo)
            self.db.commit()
            self.db.refresh(modulo)
            return modulo
        except Exception:
            self.db.rollback()
            raise

    def obtener_rol(self, rol_id: int) -> Rol | None:
        consulta = select(Rol).where(
            Rol.id == rol_id,
            Rol.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def obtener_modulos_por_ids(self, modulo_ids: set[int]) -> list[Modulo]:
        if not modulo_ids:
            return []

        consulta = select(Modulo).where(
            Modulo.id.in_(modulo_ids),
            Modulo.estado.is_(True),
        )
        return list(self.db.scalars(consulta).all())

    def listar_modulos_por_rol(self, rol_id: int) -> list[Modulo]:
        consulta = (
            select(Modulo)
            .join(
                ModuloPorRol,
                ModuloPorRol.modulo_id == Modulo.id,
            )
            .where(
                ModuloPorRol.rol_id == rol_id,
                ModuloPorRol.estado.is_(True),
                Modulo.estado.is_(True),
            )
            .order_by(Modulo.nombre)
        )
        return list(self.db.scalars(consulta).all())

    def reemplazar_modulos_del_rol(
        self,
        rol_id: int,
        modulo_ids: set[int],
    ) -> list[Modulo]:
        try:
            consulta = select(ModuloPorRol).where(
                ModuloPorRol.rol_id == rol_id
            )
            asignaciones = list(self.db.scalars(consulta).all())
            asignaciones_por_modulo = {
                asignacion.modulo_id: asignacion
                for asignacion in asignaciones
            }

            # Activa los módulos incluidos y desactiva los omitidos.
            for modulo_id, asignacion in asignaciones_por_modulo.items():
                asignacion.estado = modulo_id in modulo_ids

            # Crea las relaciones que aún no existían.
            for modulo_id in modulo_ids:
                if modulo_id not in asignaciones_por_modulo:
                    self.db.add(
                        ModuloPorRol(
                            rol_id=rol_id,
                            modulo_id=modulo_id,
                            estado=True,
                        )
                    )

            self.db.commit()
            return self.listar_modulos_por_rol(rol_id)

        except Exception:
            self.db.rollback()
            raise