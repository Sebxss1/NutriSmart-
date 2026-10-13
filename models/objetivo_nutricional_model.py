from datetime import date, datetime

from sqlalchemy import (
    Boolean,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class ObjetivoNutricional(Base):
    __tablename__ = "objetivo_nutricional"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(String(60), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    meta_cuantificable: Mapped[str | None] = mapped_column(String(200))

    fecha_inicio: Mapped[date] = mapped_column(
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