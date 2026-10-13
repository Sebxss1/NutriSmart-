from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ModuloCrear(BaseModel):
    codigo: str = Field(
        min_length=2,
        max_length=60,
        pattern=r"^[a-z0-9_]+$",
    )
    nombre: str = Field(min_length=1, max_length=100)
    descripcion: str | None = None


class ModuloRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    codigo: str
    nombre: str
    descripcion: str | None
    estado: bool
    creado: datetime
    actualizado: datetime


class ModulosRolActualizar(BaseModel):
    modulo_ids: list[int] = Field(
        description="IDs de los módulos que tendrá asignados el rol."
    )