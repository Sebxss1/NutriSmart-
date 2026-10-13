from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class IngredienteReceta(Base):
    __tablename__ = "ingrediente_receta"

    __table_args__ = (
        UniqueConstraint(
            "receta_id",
            "alimento_id",
            name="uq_ingrediente_receta",
        ),
        CheckConstraint(
            "cantidad > 0",
            name="ck_ingrediente_receta_cantidad",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    receta_id: Mapped[int] = mapped_column(
        ForeignKey("receta.id"),
        nullable=False,
    )

    alimento_id: Mapped[int] = mapped_column(
        ForeignKey("alimento.id"),
        nullable=False,
    )

    cantidad: Mapped[Decimal] = mapped_column(Numeric(10, 3), nullable=False)
    unidad: Mapped[str] = mapped_column(String(30), nullable=False)

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