from datetime import date, datetime

from tests.conftest import entrar


def test_humo_semilla(client):
    ana = entrar(client)
    assert ana["rol"] == "estudiante"
    luis = entrar(client, "luis@lab.test", "luis")
    assert luis["rol"] == "docente"
    rosa = entrar(client, "rosa@lab.test", "rosa")
    assert rosa["rol"] == "administrador"
    labs = client.get("/api/laboratorios")
    assert [lab["nombre"] for lab in labs.json()] == ["Lab 1", "Lab 2"]


def test_ca01_disponibilidad_muestra_estado(client):
    entrar(client)
    creada = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 3, "bloque_fin": 3},
    )
    assert creada.status_code == 201
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    lab1 = dia[0]
    estados = {bloque["bloque"]: bloque["estado"] for bloque in lab1["bloques"]}
    assert estados[2] == "libre"
    assert estados[3] == "reservada"
    conflicto = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 3, "bloque_fin": 3},
    )
    assert conflicto.status_code == 409
    assert conflicto.json()["codigo"] == "RN-07"


def test_ca03_reserva_de_tres_bloques(client):
    ana = entrar(client)
    respuesta = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 6},
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["estado"] == "confirmada"
    assert cuerpo["origen"] == "en_linea"
    assert cuerpo["usuario_id"] == ana["id"]
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    estados = {b["bloque"]: b["estado"] for b in dia[0]["bloques"]}
    assert estados[4] == estados[5] == estados[6] == "reservada"


def test_ca04_rechaza_mas_de_tres_bloques(client):
    entrar(client)
    respuesta = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 1, "bloque_fin": 4},
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "RN-02"
    assert client.get("/api/reservas").json() == []


def test_ca05_rechaza_menos_de_una_hora(client, reloj):
    entrar(client)
    reloj.momento = datetime(2026, 11, 20, 9, 0)
    respuesta = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    assert respuesta.status_code == 409
    assert respuesta.json()["codigo"] == "RN-05"
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[0]["bloques"][3]["estado"] == "libre"


def test_ca06_y_ca23_presencial_bajo_la_hora(client, reloj):
    ana = entrar(client, "ana@lab.test", "ana")
    client.delete("/api/sesion")
    rosa = entrar(client, "rosa@lab.test", "rosa")
    reloj.momento = datetime(2026, 11, 20, 9, 0)
    respuesta = client.post(
        "/api/reservas/presenciales",
        json={
            "usuario_id": ana["id"],
            "laboratorio_id": 1,
            "fecha": "2026-11-20",
            "bloque_inicio": 4,
            "bloque_fin": 4,
        },
    )
    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["origen"] == "presencial"
    assert cuerpo["usuario_id"] == ana["id"]
    assert cuerpo["creada_por"] == rosa["id"]


def test_ca10_mismo_laboratorio_otro_bloque(client):
    entrar(client)
    primera = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    segunda = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 8, "bloque_fin": 8},
    )
    assert primera.status_code == 201
    assert segunda.status_code == 201


def test_ca19_solo_admin_libera(client, reloj):
    entrar(client)
    reloj.momento = datetime(2026, 11, 20, 7, 30)
    reserva = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    ).json()
    client.post(f"/api/reservas/{reserva['id']}/cancelar")
    ana = client.post("/api/franjas/liberar", json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [4]})
    assert ana.status_code == 403
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    rosa = client.post("/api/franjas/liberar", json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [4]})
    assert rosa.status_code == 200
    entrar(client)
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[0]["bloques"][3]["estado"] == "libre"


def test_ca21_y_ca22_mantenimiento(client):
    entrar(client)
    reserva = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 10, "bloque_fin": 10},
    )
    assert reserva.status_code == 201
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    tapada = client.post(
        "/api/franjas/mantenimiento",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [10], "activo": True},
    )
    assert tapada.status_code == 409
    assert tapada.json()["codigo"] == "RN-23"
    bloqueo = client.post(
        "/api/franjas/mantenimiento",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [11], "activo": True},
    )
    assert bloqueo.status_code == 200
    client.delete("/api/sesion")
    entrar(client)
    intento = client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 11, "bloque_fin": 11},
    )
    assert intento.status_code == 409
    assert intento.json()["codigo"] == "RN-10"
    client.delete("/api/sesion")
    entrar(client, "rosa@lab.test", "rosa")
    reabrir = client.post(
        "/api/franjas/mantenimiento",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [11], "activo": False},
    )
    assert reabrir.status_code == 200
    dia = client.get("/api/disponibilidad", params={"fecha": "2026-11-20"}).json()
    assert dia[0]["bloques"][10]["estado"] == "libre"


def test_ocupacion_no_inventa_reservas(client):
    entrar(client)
    client.post(
        "/api/reservas",
        json={"laboratorio_id": 1, "fecha": "2026-11-20", "bloque_inicio": 4, "bloque_fin": 4},
    )
    cuerpo = client.get("/api/ocupacion", params={"desde": "2026-11-20", "hasta": "2026-11-20"}).json()
    assert cuerpo["reservadas"] == 1
    assert cuerpo["denominador"] == 32
    assert cuerpo["porcentaje"] == 1 / 32


def test_recorrido_de_pantalla(client):
    pagina = client.post("/entrar", data={"correo": "ana@lab.test", "clave": "ana"}, follow_redirects=False)
    assert pagina.status_code == 303
    inicio = client.get("/")
    assert inicio.status_code == 200
    assert "Disponibilidad" in inicio.text
    reserva = client.post(
        "/reservas",
        data={"laboratorio_id": "1", "fecha": "2026-11-20", "bloque_inicio": "4", "bloque_fin": "4"},
        follow_redirects=False,
    )
    assert reserva.status_code == 303
    assert reserva.headers["location"] == "/reservas"
    lista = client.get("/reservas")
    assert "confirmada" in lista.text
