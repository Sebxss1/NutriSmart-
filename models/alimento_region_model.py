from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    Boolean,
    CHAR,
    CheckConstraint,
    Date,
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


class AlimentoRegion(Base):
    __tablename__ = "alimento_region"

    __table_args__ = (
        UniqueConstraint(
            "alimento_id",
            "municipio_divipola",
            "fecha_referencia",
            name="uq_alimento_municipio_fecha",
        ),
        CheckConstraint(
            "precio_cop >= 0",
            name="ck_alimento_region_precio",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    alimento_id: Mapped[int] = mapped_column(
        ForeignKey("alimento.id"),
        nullable=False,
    )

    municipio_divipola: Mapped[str] = mapped_column(CHAR(5), nullable=False)
    precio_cop: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))

    disponible: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
        server_default="true",
    )

    fecha_referencia: Mapped[date] = mapped_column(Date, nullable=False)
    fuente: Mapped[str | None] = mapped_column(String(200))

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