from datetime import datetime

import pytest
from fastapi.testclient import TestClient

from reservas.main import create_app
from reservas.reloj import RelojFijo


@pytest.fixture
def reloj():
    return RelojFijo(datetime(2026, 11, 16, 8, 0))


@pytest.fixture
def app(tmp_path, reloj):
    return create_app(f"sqlite:///{tmp_path / 'test.db'}", reloj)


@pytest.fixture
def client(app):
    with TestClient(app) as cliente:
        yield cliente


def entrar(client, correo="ana@lab.test", clave="ana"):
    respuesta = client.post("/api/sesion", json={"correo": correo, "clave": clave})
    assert respuesta.status_code == 200, respuesta.text
    return respuesta.json()
