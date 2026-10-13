from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import (
    CHAR,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    SmallInteger,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from config.database import Base


class Paciente(Base):
    __tablename__ = "paciente"

    __table_args__ = (
        CheckConstraint(
            "zona IN ('URBANA', 'RURAL')",
            name="ck_paciente_zona",
        ),
        CheckConstraint(
            "estrato BETWEEN 1 AND 6",
            name="ck_paciente_estrato",
        ),
        CheckConstraint(
            "presupuesto_semanal_cop >= 0",
            name="ck_paciente_presupuesto",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    nutricionista_id: Mapped[int] = mapped_column(
        ForeignKey("usuario.id"),
        nullable=False,
    )

    usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuario.id"),
        unique=True,
        nullable=True,
    )

    nombres: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)
    sexo: Mapped[str | None] = mapped_column(String(20))
    municipio_divipola: Mapped[str] = mapped_column(CHAR(5), nullable=False)
    zona: Mapped[str | None] = mapped_column(String(10))
    estrato: Mapped[int | None] = mapped_column(SmallInteger)
    presupuesto_semanal_cop: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2)
    )
    motivo_anulacion: Mapped[str | None] = mapped_column(Text)

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

    usuario = relationship("Usuario", foreign_keys=[usuario_id])
    nutricionista = relationship("Usuario", foreign_keys=[nutricionista_id])

    @property
    def correo(self) -> str | None:
        return self.usuario.correo if self.usuario else None