from datetime import date, datetime

import pytest

from reservas.errors import ReglaError
from reservas.rules import fin_bloque, inicio_bloque, validar_rango


def test_bloque_4_empieza_a_las_0930():
    assert inicio_bloque(date(2026, 11, 20), 4) == datetime(2026, 11, 20, 9, 30)


def test_bloque_3_empieza_a_las_0840():
    assert inicio_bloque(date(2026, 11, 20), 3) == datetime(2026, 11, 20, 8, 40)


def test_bloque_16_termina_a_las_2020():
    assert fin_bloque(date(2026, 11, 20), 16) == datetime(2026, 11, 20, 20, 20)


def test_rn02_rechaza_mas_de_tres_bloques():
    with pytest.raises(ReglaError) as error:
        validar_rango(1, 4)
    assert error.value.codigo == "RN-02"
