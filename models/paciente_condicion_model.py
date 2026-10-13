from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class PacienteCondicion(Base):
    __tablename__ = "paciente_condicion"

    __table_args__ = (
        UniqueConstraint(
            "paciente_id",
            "condicion_id",
            name="uq_paciente_condicion",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False,
    )

    condicion_id: Mapped[int] = mapped_column(
        ForeignKey("condicion_medica.id"),
        nullable=False,
    )

    observaciones: Mapped[str | None] = mapped_column(Text)

    fecha_registro: Mapped[date] = mapped_column(
        Date,
        nullable=False,
        server_default=func.current_date(),
    )

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