from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Consentimiento(Base):
    __tablename__ = "consentimiento"

    __table_args__ = (
        CheckConstraint(
            "tipo_otorgante IN ('PACIENTE', 'REPRESENTANTE')",
            name="ck_consentimiento_tipo_otorgante",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    paciente_id: Mapped[int] = mapped_column(
        ForeignKey("paciente.id"),
        nullable=False,
    )

    version_texto: Mapped[str] = mapped_column(String(40), nullable=False)

    fecha_aceptacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    otorgado_por: Mapped[str] = mapped_column(String(160), nullable=False)
    tipo_otorgante: Mapped[str] = mapped_column(String(20), nullable=False)

    registrado_por_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
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