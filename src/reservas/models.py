from sqlalchemy import CheckConstraint, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuario"
    __table_args__ = (
        CheckConstraint("rol in ('estudiante', 'docente', 'administrador')"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(120))
    correo: Mapped[str] = mapped_column(String(180), unique=True)
    rol: Mapped[str] = mapped_column(String(20))
    clave_hash: Mapped[str] = mapped_column(String(200))


class Laboratorio(Base):
    __tablename__ = "laboratorio"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), unique=True)
    ubicacion: Mapped[str] = mapped_column(String(120), default="")
    activo: Mapped[int] = mapped_column(default=1)


class Reserva(Base):
    __tablename__ = "reserva"
    __table_args__ = (
        CheckConstraint(
            "estado in ('confirmada', 'cancelada', 'desplazada', 'no_show')"
        ),
        CheckConstraint("origen in ('en_linea', 'presencial')"),
        CheckConstraint("bloque_fin - bloque_inicio + 1 between 1 and 3"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    laboratorio_id: Mapped[int] = mapped_column(ForeignKey("laboratorio.id"))
    fecha: Mapped[str] = mapped_column(String(10))
    bloque_inicio: Mapped[int]
    bloque_fin: Mapped[int]
    estado: Mapped[str] = mapped_column(String(20))
    origen: Mapped[str] = mapped_column(String(20))
    creada_en: Mapped[str] = mapped_column(String(32))
    creada_por: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    actualizada_en: Mapped[str] = mapped_column(String(32))
    desplaza_a: Mapped[int | None] = mapped_column(ForeignKey("reserva.id"), nullable=True)


class Franja(Base):
    __tablename__ = "franja"
    __table_args__ = (
        UniqueConstraint("laboratorio_id", "fecha", "bloque"),
        CheckConstraint("bloque between 1 and 16"),
        CheckConstraint(
            "estado in ('libre', 'reservada', 'deshabilitada', 'mantenimiento')"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    laboratorio_id: Mapped[int] = mapped_column(ForeignKey("laboratorio.id"))
    fecha: Mapped[str] = mapped_column(String(10))
    bloque: Mapped[int]
    estado: Mapped[str] = mapped_column(String(20))
    reserva_id: Mapped[int | None] = mapped_column(ForeignKey("reserva.id"), nullable=True)


class Notificacion(Base):
    __tablename__ = "notificacion"
    __table_args__ = (
        CheckConstraint("estado in ('pendiente', 'enviada', 'error')"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    reserva_id: Mapped[int] = mapped_column(ForeignKey("reserva.id"))
    destinatario_id: Mapped[int] = mapped_column(ForeignKey("usuario.id"))
    tipo: Mapped[str] = mapped_column(String(40))
    cuerpo: Mapped[str] = mapped_column(String(1000))
    estado: Mapped[str] = mapped_column(String(20))
    creada_en: Mapped[str] = mapped_column(String(32))
