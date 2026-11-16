from datetime import datetime

from tests.conftest import entrar


def _reservar(client, bloque=4):
    respuesta = client.post(
        "/api/reservas",
        json={
            "laboratorio_id": 1,
            "fecha": "2026-11-20",
            "bloque_inicio": bloque,
            "bloque_fin": bloque,
        },
    )
    assert respuesta.status_code == 201, respuesta.text
    return respuesta.json()


def test_ca16_cancelar_con_un_dia_libera(client):
    entrar(client)
    reserva = _reservar(client)
    respuesta = client.post(f"/api/reservas/{reserva['id']}/cancelar")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado_franjas"] == "libre"
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[0]["bloques"][3]["estado"] == "libre"


def test_ca17_y_ca18_cancelar_tarde_deshabilita(client, reloj):
    entrar(client)
    reloj.momento = datetime(2026, 11, 20, 7, 30)
    reserva = _reservar(client)
    respuesta = client.post(f"/api/reservas/{reserva['id']}/cancelar")
    assert respuesta.json()["estado_franjas"] == "deshabilitada"
    client.delete("/api/sesion")
    entrar(client, "luis@lab.test", "luis")
    intento = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    assert intento.status_code == 409
    assert intento.json()["codigo"] == "RN-10"


def test_ca20_no_show_deshabilita(client, reloj):
    entrar(client)
    reserva = _reservar(client)
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    reloj.momento = datetime(2026, 11, 20, 10, 0)
    respuesta = client.post(f"/api/reservas/{reserva['id']}/no-show")
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "no_show"
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[0]["bloques"][3]["estado"] == "deshabilitada"
