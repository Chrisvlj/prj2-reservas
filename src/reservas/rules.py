from datetime import date, datetime, time, timedelta

from reservas.errors import ReglaError

BLOQUES = range(1, 17)
DURACION_BLOQUE = timedelta(minutes=50)
ANTELACION_EN_LINEA = timedelta(minutes=60)
ANTELACION_CANCELACION = timedelta(hours=24)


def inicio_bloque(fecha: date, bloque: int) -> datetime:
    return datetime.combine(fecha, time(7, 0)) + DURACION_BLOQUE * (bloque - 1)


def fin_bloque(fecha: date, bloque: int) -> datetime:
    return inicio_bloque(fecha, bloque) + DURACION_BLOQUE


def validar_rango(bloque_inicio: int, bloque_fin: int) -> None:
    if not (1 <= bloque_inicio <= bloque_fin <= 16):
        raise ReglaError("RN-02", "Los bloques deben estar entre 1 y 16 y ser consecutivos")
    if bloque_fin - bloque_inicio + 1 > 3:
        raise ReglaError("RN-02", "Una reserva cubre como máximo 3 bloques")


def solapan(inicio_a: int, fin_a: int, inicio_b: int, fin_b: int) -> bool:
    return inicio_a <= fin_b and inicio_b <= fin_a
