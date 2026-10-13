from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class RestriccionCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=120)
    tipo: Literal["DURA", "PREFERENCIA"]
    motivo: str | None = None


class RestriccionActualizar(BaseModel):
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    tipo: Literal["DURA", "PREFERENCIA"] | None = None
    motivo: str | None = None
    estado: bool | None = None


class RestriccionRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    nombre: str
    tipo: str
    motivo: str | None
    estado: bool