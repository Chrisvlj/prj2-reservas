import threading
from datetime import date, datetime

from reservas.db import init_db, make_engine, sesion_de
from reservas.errors import ReglaError
from reservas.models import Reserva, Usuario
from reservas.reloj import RelojFijo
from reservas.services import crear_reserva, usuario_por_correo
from sqlalchemy import func, select

from tests.conftest import entrar


def test_ca07_no_doble_reserva_mismo_laboratorio(client):
    entrar(client)
    mia = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 5},
    )
    assert mia.status_code == 201
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    suya = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 5, "bloque_fin": 5},
    )
    assert suya.status_code == 409
    assert suya.json()["codigo"] == "RN-08"


def test_ca08_una_sola_gana_si_compiten(tmp_path):
    engine = make_engine(f"sqlite:///{tmp_path / 'carrera.db'}")
    init_db(engine)
    fabrica = sesion_de(engine)
    reloj = RelojFijo(datetime(2026, 11, 16, 8, 0))
    with fabrica() as session:
        ana = usuario_por_correo(session, "ana@lab.test")
        luis = usuario_por_correo(session, "luis@lab.test")
        ids = (ana.id, luis.id)
    barrera = threading.Barrier(2)
    resultados = []

    def intentar(usuario_id):
        barrera.wait()
        with fabrica() as session:
            try:
                actor = session.get(Usuario, usuario_id)
                crear_reserva(
                    session,
                    actor=actor,
                    usuario_id=usuario_id,
                    laboratorio_id=2,
                    fecha=date(2026, 11, 20),
                    bloque_inicio=8,
                    bloque_fin=8,
                    origen="en_linea",
                    reloj=reloj,
                )
                session.commit()
                resultados.append(201)
            except ReglaError as exc:
                session.rollback()
                resultados.append(exc.codigo)

    hilos = [threading.Thread(target=intentar, args=(usuario_id,)) for usuario_id in ids]
    for hilo in hilos:
        hilo.start()
    for hilo in hilos:
        hilo.join()
    assert resultados.count(201) == 1, resultados
    assert resultados.count("RN-08") == 1, resultados
    with fabrica() as session:
        confirmadas = session.scalar(
            select(func.count()).select_from(Reserva).where(
                Reserva.laboratorio_id == 2,
                Reserva.fecha == "2026-11-20",
                Reserva.bloque_inicio == 8,
                Reserva.estado == "confirmada",
            )
        )
    assert confirmadas == 1


def test_ca09_no_solape_entre_laboratorios(client):
    entrar(client)
    primera = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    segunda = client.post(
        "/api/reservas",
        json={"laboratorio_id": 2, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    assert primera.status_code == 201
    assert segunda.status_code == 409
    assert segunda.json()["codigo"] == "RN-07"
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[1]["bloques"][3]["estado"] == "libre"
