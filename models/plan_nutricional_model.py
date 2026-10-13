from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class PlanNutricional(Base):
    __tablename__ = "plan_nutricional"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False,
    )

    objetivo_id: Mapped[int | None] = mapped_column(
        ForeignKey("objetivo_nutricional.id"),
        nullable=True,
    )

    creado_por_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(String(160), nullable=False)

    estado: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    creado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    actualizado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )