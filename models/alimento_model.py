from datetime import datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Integer,
    Numeric,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class Alimento(Base):
    __tablename__ = "alimento"

    __table_args__ = (
        CheckConstraint("energia_kcal >= 0", name="ck_alimento_energia"),
        CheckConstraint("proteina_g >= 0", name="ck_alimento_proteina"),
        CheckConstraint("carbohidratos_g >= 0", name="ck_alimento_carbohidratos"),
        CheckConstraint("grasa_g >= 0", name="ck_alimento_grasa"),
        CheckConstraint("fibra_g >= 0", name="ck_alimento_fibra"),
        CheckConstraint("sodio_mg >= 0", name="ck_alimento_sodio"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    codigo: Mapped[str] = mapped_column(String(60), unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(160), nullable=False)
    categoria: Mapped[str] = mapped_column(String(80), nullable=False)

    unidad_base: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="100 g",
        server_default="100 g",
    )

    energia_kcal: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    proteina_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    carbohidratos_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    grasa_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    fibra_g: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    sodio_mg: Mapped[Decimal | None] = mapped_column(Numeric(10, 2))
    fuente_dato: Mapped[str | None] = mapped_column(String(200))

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