from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean, CheckConstraint, DateTime, ForeignKey, Integer,
    Numeric, SmallInteger, String, func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class DetallePlan(Base):
    __tablename__ = "detalle_plan"

    __table_args__ = (
        CheckConstraint("dia BETWEEN 1 AND 31", name="ck_detalle_plan_dia"),
        CheckConstraint(
            "tipo_comida IN "
            "('DESAYUNO', 'MEDIA_MANANA', 'ALMUERZO', 'MERIENDA', 'CENA')",
            name="ck_detalle_plan_tipo_comida",
        ),
        CheckConstraint("cantidad > 0", name="ck_detalle_plan_cantidad"),
        CheckConstraint(
            "(alimento_id IS NOT NULL AND receta_id IS NULL) OR "
            "(alimento_id IS NULL AND receta_id IS NOT NULL)",
            name="ck_detalle_plan_un_solo_origen",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    version_plan_id: Mapped[int] = mapped_column(
        ForeignKey("version_plan.id"), nullable=False
    )
    dia: Mapped[int] = mapped_column(SmallInteger, nullable=False)
    tipo_comida: Mapped[str] = mapped_column(String(30), nullable=False)
    alimento_id: Mapped[int | None] = mapped_column(ForeignKey("alimento.id"))
    receta_id: Mapped[int | None] = mapped_column(ForeignKey("receta.id"))
    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    unidad: Mapped[str] = mapped_column(String(30), nullable=False)

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