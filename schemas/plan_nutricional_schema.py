from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class PlanNutricionalCrear(BaseModel):
    nombre: str = Field(min_length=1, max_length=160)
    objetivo_id: int | None = Field(default=None, gt=0)


class PlanNutricionalRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    paciente_id: int
    objetivo_id: int | None
    creado_por_id: int
    nombre: str
    estado: bool
    creado: datetime
    actualizado: datetime


class VersionPlanCrear(BaseModel):
    notas: str | None = None


class VersionPlanEstadoActualizar(BaseModel):
    estado_plan: str = Field(pattern="^(APROBADO|ENTREGADO)$")


class VersionPlanRespuesta(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    plan_id: int
    numero_version: int
    estado_plan: str
    aprobado_por_id: int | None
    fecha_aprobacion: datetime | None
    notas: str | None
    estado: bool
    creado: datetime
    actualizado: datetime