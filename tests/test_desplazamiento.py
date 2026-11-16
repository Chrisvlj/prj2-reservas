from datetime import datetime

from reservas.models import Usuario
from tests.conftest import entrar


def _ana_reserva_lab1(client):
    entrar(client)
    respuesta = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 6},
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def test_ca11_y_ca12_docente_desplaza_y_ofrece_lab(client, reloj):
    reserva = _ana_reserva_lab1(client)
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    reloj.momento = datetime(2026, 11, 20, 9, 0)
    respuesta = client.post(f"/api/reservas/{reserva['id']}/desplazar", json={})
    assert respuesta.status_code == 200, respuesta.text
    cuerpo = respuesta.json()
    assert cuerpo["reserva_estudiante"]["estado"] == "desplazada"
    assert cuerpo["reserva_docente"]["estado"] == "confirmada"
    assert cuerpo["reserva_docente"]["usuario_id"] != reserva["usuario_id"]
    assert "Lab 2" in cuerpo["notificacion"]["cuerpo"]
    assert cuerpo["notificacion"]["laboratorios"] == ["Lab 2"]
    client.delete("/api/sesion")
    entrar(client)
    mias = client.get("/api/reservas").json()
    assert len(mias) == 1
    assert mias[0]["estado"] == "desplazada"


def test_ca13_notificacion_sin_alternativa(client, app):
    reserva = _ana_reserva_lab1(client)
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    bloqueo = client.post(
        "/api/franjas/mantenimiento",
        json={"laboratorio_id": 2, "fecha": "2026-11-20", "bloques": [4, 5, 6], "activo": True},
    )
    assert bloqueo.status_code == 200
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    respuesta = client.post(f"/api/reservas/{reserva['id']}/desplazar", json={})
    assert "No hay otro laboratorio" in respuesta.json()["notificacion"]["cuerpo"]
    assert respuesta.json()["notificacion"]["laboratorios"] == []
    del app


def test_ca14_no_desplaza_a_docente(client, app):
    entrar(client, "luis@lab.test", "luis")
    suya = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    ).json()
    with app.state.fabrica() as session:
        session.add(
            Usuario(
                nombre="Marta",
                correo="marta@lab.test",
                rol="docente",
                clave_hash=session.query(Usuario).filter_by(correo="luis@lab.test").one().clave_hash,
            )
        )
        session.commit()
    client.delete("/api/sesion")
    entrar(client, "marta@lab.test", "luis")
    respuesta = client.post(f"/api/reservas/{suya['id']}/desplazar", json={})
    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "RN-13"
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    assert client.get("/api/reservas").json()[0]["estado"] == "confirmada"


def test_ca15_docente_no_queda_en_dos_sitios(client):
    ana = _ana_reserva_lab1(client)
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    propia = client.post(
        "/api/reservas",
        json={"laboratorio_id": 2, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    assert propia.status_code == 201
    respuesta = client.post(
        f"/api/reservas/{ana['id']}/desplazar",
        json={"bloque_inicio": 4, "bloque_fin": 4},
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "RN-07"
    client.delete("/api/sesion")
    entrar(client)
    assert client.get("/api/reservas").json()[0]["estado"] == "confirmada"


def test_correo_fallido_no_deshace_el_desplazamiento(client):
    reserva = _ana_reserva_lab1(client)
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")

    def transporte(*_args):
        raise RuntimeError("smtp caído")

    from reservas.services import desplazar
    from reservas.models import Usuario

    with client.app.state.fabrica() as session:
        luis = session.query(Usuario).filter_by(correo="luis@lab.test").one()
        resultado = desplazar(
            session,
            luis,
            reserva["id"],
            None,
            None,
            client.app.state.reloj,
            transporte=transporte,
        )
        session.commit()
    assert resultado["reserva_estudiante"]["estado"] == "desplazada"
    assert resultado["notificacion"]["estado"] == "error"
