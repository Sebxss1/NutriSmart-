from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from models.cita_model import Cita
from models.paciente_model import Paciente


class CitaRepository:
    def __init__(self, db: Session):
        self.db = db

    def obtener_paciente(self, paciente_id: int) -> Paciente | None:
        consulta = select(Paciente).where(Paciente.id == paciente_id)
        return self.db.scalar(consulta)

    def listar_por_paciente(self, paciente_id: int) -> list[Cita]:
        consulta = (
            select(Cita)
            .where(
                Cita.paciente_id == paciente_id,
                Cita.estado.is_(True),
            )
            .order_by(Cita.inicio.desc())
        )
        return list(self.db.scalars(consulta).all())

    def obtener_cita(
        self,
        paciente_id: int,
        cita_id: int,
    ) -> Cita | None:
        consulta = select(Cita).where(
            Cita.id == cita_id,
            Cita.paciente_id == paciente_id,
            Cita.estado.is_(True),
        )
        return self.db.scalar(consulta)

    def existe_conflicto(
        self,
        paciente_id: int,
        nutricionista_id: int,
        inicio,
        fin,
        excluir_cita_id: int | None = None,
    ) -> bool:
        consulta = select(Cita.id).where(
            Cita.estado.is_(True),
            Cita.estado_cita.in_(["PROGRAMADA", "REPROGRAMADA"]),
            Cita.inicio < fin,
            Cita.fin > inicio,
            or_(
                Cita.paciente_id == paciente_id,
                Cita.nutricionista_id == nutricionista_id,
            ),
        )

        if excluir_cita_id is not None:
            consulta = consulta.where(Cita.id != excluir_cita_id)

        return self.db.scalar(consulta.limit(1)) is not None

    def crear(self, cita: Cita) -> Cita:
        try:
            self.db.add(cita)
            self.db.commit()
            self.db.refresh(cita)
            return cita
        except Exception:
            self.db.rollback()
            raise

    def guardar(self, cita: Cita) -> Cita:
        try:
            self.db.commit()
            self.db.refresh(cita)
            return cita
        except Exception:
            self.db.rollback()
            raise