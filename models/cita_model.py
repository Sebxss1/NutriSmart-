from datetime import datetime

from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey,
    Integer, String, Text, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Cita(Base):
    __tablename__ = "cita"

    __table_args__ = (
        CheckConstraint(
            "estado_cita IN ('PROGRAMADA', 'REALIZADA', 'CANCELADA', 'REPROGRAMADA')",
            name="ck_cita_estado",
        ),
        CheckConstraint("fin > inicio", name="ck_cita_rango"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"), nullable=False
    )
    nutricionista_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"), nullable=False
    )
    inicio: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    fin: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    estado_cita: Mapped[str] = mapped_column(String(20), nullable=False)
    motivo: Mapped[str | None] = mapped_column(Text)

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