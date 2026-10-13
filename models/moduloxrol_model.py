from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column

from config.database import Base


class ModuloPorRol(Base):
    __tablename__ = "moduloxrol"

    __table_args__ = (
        UniqueConstraint(
            "rol_id",
            "modulo_id",
            name="uq_moduloxrol_rol_modulo",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    rol_id: Mapped[int] = mapped_column(
        ForeignKey("rol.id"),
        nullable=False,
    )

    modulo_id: Mapped[int] = mapped_column(
        ForeignKey("modulo.id"),
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