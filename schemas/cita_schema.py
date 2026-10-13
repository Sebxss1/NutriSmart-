from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


EstadoCita = Literal["CANCELADA", "REALIZADA"]


class CitaCrear(BaseModel):
    inicio: datetime
    fin: datetime
    motivo: str | None = None

    @model_validator(mode="after")
    def validar_horario(self):
        if self.fin <= self.inicio:
            raise ValueError("La hora de fin debe ser posterior a la hora de inicio.")
        return self


class CitaActualizar(BaseModel):
    inicio: datetime | None = None
    fin: datetime | None = None
    motivo: str | None = None


class CitaEstadoActualizar(BaseModel):
    estado_cita: EstadoCita


class CitaRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    nutricionista_id: int
    inicio: datetime
    fin: datetime
    estado_cita: str
    motivo: str | None
    estado: bool
    creado: datetime
    actualizado: datetime