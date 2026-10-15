from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
    func,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class RestriccionAlimentaria(Base):
    __tablename__ = "restriccion_alimentaria"

    __table_args__ = (
        CheckConstraint(
            "tipo IN ('DURA', 'PREFERENCIA')",
            name="ck_restriccion_alimentaria_tipo",
        ),
        Index(
            "uq_restriccion_paciente_nombre_tipo_activa",
            "paciente_id",
            "nombre",
            "tipo",
            unique=True,
            postgresql_where=text("estado IS TRUE"),
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False,
    )

    nombre: Mapped[str] = mapped_column(String(120), nullable=False)
    tipo: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str | None] = mapped_column(Text)

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