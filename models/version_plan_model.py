from datetime import datetime
from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, Integer,
    String, Text, UniqueConstraint, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class VersionPlan(Base):
    __tablename__ = "version_plan"

    __table_args__ = (
        CheckConstraint("numero_version > 0", name="ck_version_plan_numero"),
        CheckConstraint(
            "estado_plan IN ('BORRADOR', 'APROBADO', 'ENTREGADO', 'REEMPLAZADO')",
            name="ck_version_plan_estado_plan",
        ),
        UniqueConstraint("plan_id", "numero_version", name="uq_version_plan_numero"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plan_nutricional.id"), nullable=False
    )
    numero_version: Mapped[int] = mapped_column(Integer, nullable=False)
    estado_plan: Mapped[str] = mapped_column(String(20), nullable=False)
    aprobado_por_id: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"))
    fecha_aprobacion: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    notas: Mapped[str | None] = mapped_column(Text)

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