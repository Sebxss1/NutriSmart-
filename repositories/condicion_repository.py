from sqlalchemy import or_
from sqlalchemy.orm import Session

from models.condicion_medica_model import CondicionMedica
from models.paciente_condicion_model import PacienteCondicion


class CondicionRepository:
    def __init__(self, db: Session):
        self.db = db

    def listar(self, incluir_inactivas: bool = False):
        consulta = self.db.query(CondicionMedica)

        if not incluir_inactivas:
            consulta = consulta.filter(CondicionMedica.estado.is_(True))

        return consulta.order_by(CondicionMedica.nombre).all()

    def obtener_por_codigo_o_nombre(
        self,
        codigo: str,
        nombre: str,
    ):
        return (
            self.db.query(CondicionMedica)
            .filter(
                or_(
                    CondicionMedica.codigo == codigo,
                    CondicionMedica.nombre.ilike(nombre),
                )
            )
            .first()
        )

    def crear(self, condicion: CondicionMedica) -> CondicionMedica:
        try:
            self.db.add(condicion)
            self.db.commit()
            self.db.refresh(condicion)
            return condicion
        except Exception:
            self.db.rollback()
            raise

    def obtener_condicion(self, condicion_id: int):
        return (
            self.db.query(CondicionMedica)
            .filter(CondicionMedica.id == condicion_id)
            .first()
        )

    def listar_por_paciente(self, paciente_id: int):
        return (
            self.db.query(PacienteCondicion)
            .filter(PacienteCondicion.paciente_id == paciente_id)
            .all()
        )

    def obtener_asociacion(self, paciente_id: int, condicion_id: int):
        return (
            self.db.query(PacienteCondicion)
            .filter(
                PacienteCondicion.paciente_id == paciente_id,
                PacienteCondicion.condicion_id == condicion_id,
            )
            .first()
        )

    def agregar_a_paciente(
        self,
        paciente_id: int,
        condicion_id: int,
        observaciones: str | None = None,
    ):
        asociacion = PacienteCondicion(
            paciente_id=paciente_id,
            condicion_id=condicion_id,
            observaciones=observaciones,
        )

        try:
            self.db.add(asociacion)
            self.db.commit()
            self.db.refresh(asociacion)
            return asociacion
        except Exception:
            self.db.rollback()
            raise