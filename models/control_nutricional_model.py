from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, Integer,
    Numeric, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class ControlNutricional(Base):
    __tablename__ = "control_nutricional"

    __table_args__ = (
        CheckConstraint("peso_kg > 0", name="ck_control_peso"),
        CheckConstraint("estatura_cm > 0", name="ck_control_estatura"),
        CheckConstraint("cintura_cm > 0", name="ck_control_cintura"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"), nullable=False
    )
    registrado_por_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"), nullable=False
    )
    fecha_control: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False
    )
    peso_kg: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    estatura_cm: Mapped[Decimal] = mapped_column(Numeric(6, 2), nullable=False)
    cintura_cm: Mapped[Decimal | None] = mapped_column(Numeric(6, 2))
    observaciones: Mapped[str | None] = mapped_column(Text)

    estado: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=True, server_default="true"
    )
    creado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    actualizado: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )