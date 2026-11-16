from tests.conftest import entrar


def _reservar(client, fecha, bloque=4):
    return client.post(
        "/api/reservas",
        json={
            "laboratorio_id": 1,
            "fecha": fecha,
            "bloque_inicio": bloque,
            "bloque_fin": bloque,
        },
    )


def test_ca24_tercera_reserva_de_la_semana(client):
    entrar(client)
    assert _reservar(client, "2026-11-17").status_code == 201
    assert _reservar(client, "2026-11-18").status_code == 201
    tercera = _reservar(client, "2026-11-19")
    assert tercera.status_code == 409
    assert tercera.json()["codigo"] == "RN-25"
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-19"}).json()
    assert dia[0]["bloques"][3]["estado"] == "libre"


def test_ca25_cancelar_libera_el_tope(client):
    entrar(client)
    primera = _reservar(client, "2026-11-17").json()
    assert _reservar(client, "2026-11-18").status_code == 201
    client.post(f"/api/reservas/{primera['id']}/cancelar")
    tercera = _reservar(client, "2026-11-19")
    assert tercera.status_code == 201
    assert tercera.json()["estado"] == "confirmada"


def test_ca26_docente_sin_tope_semanal(client):
    entrar(client, "luis@lab.test", "luis")
    for fecha in ("2026-11-17", "2026-11-18", "2026-11-19"):
        respuesta = _reservar(client, fecha)
        assert respuesta.status_code == 201, respuesta.text
        assert respuesta.json()["estado"] == "confirmada"


def test_ca27_otra_semana_no_suma(client):
    entrar(client)
    assert _reservar(client, "2026-11-17").status_code == 201
    assert _reservar(client, "2026-11-18").status_code == 201
    siguiente = _reservar(client, "2026-11-24")
    assert siguiente.status_code == 201


def test_ca28_presencial_cuenta_para_el_estudiante(client):
    ana = entrar(client)
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    for fecha in ("2026-11-17", "2026-11-18"):
        respuesta = client.post(
            "/api/reservas/presenciales",
            json={
                "usuario_id": ana["id"],
                "laboratorio_id": 1,
                "fecha": fecha,
                "bloque_inicio": 4,
                "bloque_fin": 4,
            },
        )
        assert respuesta.status_code == 201, respuesta.text
    client.delete("/api/sesion")
    entrar(client)
    tercera = _reservar(client, "2026-11-19")
    assert tercera.status_code == 409
    assert tercera.json()["codigo"] == "RN-25"
