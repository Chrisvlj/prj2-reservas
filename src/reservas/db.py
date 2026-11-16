import hashlib
import os
from collections.abc import Callable

from sqlalchemy import create_engine, event, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from reservas.models import Base, Laboratorio, Usuario

SEMILLA_USUARIOS = (
    ("Ana", "ana@lab.test", "estudiante", "ana"),
    ("Luis", "luis@lab.test", "docente", "luis"),
    ("Rosa", "rosa@lab.test", "administrador", "rosa"),
)


def hash_clave(clave: str, sal: str | None = None) -> str:
    sal = sal or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", clave.encode(), bytes.fromhex(sal), 100_000)
    return f"{sal}${digest.hex()}"


def verifica_clave(clave: str, almacenada: str) -> bool:
    sal, _digest = almacenada.split("$", 1)
    return hash_clave(clave, sal) == almacenada


def make_engine(database_url: str) -> Engine:
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False, "timeout": 5},
    )

    @event.listens_for(engine, "connect")
    def _conectar(dbapi_connection, _record):
        dbapi_connection.isolation_level = None
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA busy_timeout=5000")
        cursor.close()

    @event.listens_for(engine, "begin")
    def _comenzar(conn):
        conn.exec_driver_sql("BEGIN IMMEDIATE")

    return engine


def init_db(engine: Engine) -> None:
    Base.metadata.create_all(engine)
    fabrica = sessionmaker(bind=engine, expire_on_commit=False)
    with fabrica() as session:
        if session.scalar(select(Usuario.id).limit(1)) is None:
            for nombre, correo, rol, clave in SEMILLA_USUARIOS:
                session.add(
                    Usuario(
                        nombre=nombre,
                        correo=correo,
                        rol=rol,
                        clave_hash=hash_clave(clave, sal=hashlib.sha256(correo.encode()).hexdigest()[:32]),
                    )
                )
            session.add(Laboratorio(nombre="Lab 1", ubicacion="Edificio A", activo=1))
            session.add(Laboratorio(nombre="Lab 2", ubicacion="Edificio A", activo=1))
            session.commit()


def sesion_de(engine: Engine) -> Callable[[], Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
