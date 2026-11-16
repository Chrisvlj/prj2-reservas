from datetime import date, datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session

from reservas.errors import PermisoError, ReglaError
from reservas.models import Franja, Laboratorio, Notificacion, Reserva, Usuario
from reservas.notifications import despachar
from reservas.rules import (
    ANTELACION_CANCELACION,
    ANTELACION_EN_LINEA,
    fin_bloque,
    inicio_bloque,
    solapan,
    validar_rango,
)


def usuario_por_correo(session: Session, correo: str) -> Usuario | None:
    return session.scalar(select(Usuario).where(Usuario.correo == correo))


def reserva_dict(reserva: Reserva) -> dict:
    return {
        "id": reserva.id,
        "usuario_id": reserva.usuario_id,
        "laboratorio_id": reserva.laboratorio_id,
        "fecha": reserva.fecha,
        "bloque_inicio": reserva.bloque_inicio,
        "bloque_fin": reserva.bloque_fin,
        "estado": reserva.estado,
        "origen": reserva.origen,
        "creada_en": reserva.creada_en,
        "creada_por": reserva.creada_por,
        "actualizada_en": reserva.actualizada_en,
        "desplaza_a": reserva.desplaza_a,
    }


def asegurar_franjas(session: Session, laboratorio_id: int, fecha: date) -> list[Franja]:
    iso = fecha.isoformat()
    existentes = list(
        session.scalars(
            select(Franja).where(
                Franja.laboratorio_id == laboratorio_id,
                Franja.fecha == iso,
            )
        )
    )
    presentes = {franja.bloque for franja in existentes}
    for bloque in range(1, 17):
        if bloque not in presentes:
            session.add(
                Franja(
                    laboratorio_id=laboratorio_id,
                    fecha=iso,
                    bloque=bloque,
                    estado="libre",
                    reserva_id=None,
                )
            )
    session.flush()
    return list(
        session.scalars(
            select(Franja)
            .where(Franja.laboratorio_id == laboratorio_id, Franja.fecha == iso)
            .order_by(Franja.bloque)
        )
    )


def disponibilidad(session: Session, fecha: date) -> list[dict]:
    laboratorios = session.scalars(
        select(Laboratorio).where(Laboratorio.activo == 1).order_by(Laboratorio.id)
    ).all()
    resultado = []
    for laboratorio in laboratorios:
        franjas = asegurar_franjas(session, laboratorio.id, fecha)
        resultado.append(
            {
                "laboratorio_id": laboratorio.id,
                "nombre": laboratorio.nombre,
                "bloques": [
                    {
                        "bloque": franja.bloque,
                        "inicio": inicio_bloque(fecha, franja.bloque).strftime("%H:%M"),
                        "fin": fin_bloque(fecha, franja.bloque).strftime("%H:%M"),
                        "estado": franja.estado,
                    }
                    for franja in franjas
                ],
            }
        )
    return resultado


def _solape_de_usuario(
    session: Session,
    usuario_id: int,
    fecha: date,
    bloque_inicio: int,
    bloque_fin: int,
) -> bool:
    reservas = session.scalars(
        select(Reserva).where(
            Reserva.usuario_id == usuario_id,
            Reserva.estado == "confirmada",
            Reserva.fecha == fecha.isoformat(),
        )
    )
    return any(
        solapan(reserva.bloque_inicio, reserva.bloque_fin, bloque_inicio, bloque_fin)
        for reserva in reservas
    )


def crear_reserva(
    session: Session,
    *,
    actor: Usuario,
    usuario_id: int,
    laboratorio_id: int,
    fecha: date,
    bloque_inicio: int,
    bloque_fin: int,
    origen: str,
    reloj,
) -> dict:
    if origen == "en_linea":
        if actor.rol not in ("estudiante", "docente") or actor.id != usuario_id:
            raise PermisoError()
    elif origen == "presencial":
        if actor.rol != "administrador":
            raise PermisoError()
    else:
        raise ReglaError("RN-04", "Origen de reserva desconocido")

    validar_rango(bloque_inicio, bloque_fin)
    ahora = reloj.ahora()
    inicio = inicio_bloque(fecha, bloque_inicio)
    fin = fin_bloque(fecha, bloque_fin)
    if fin <= ahora:
        codigo = "RN-06" if origen == "presencial" else "RN-05"
        raise ReglaError(codigo, "El bloque ya terminó")
    if origen == "en_linea" and inicio - ahora < ANTELACION_EN_LINEA:
        raise ReglaError("RN-05", "La reserva en línea exige al menos 60 minutos de antelación")

    laboratorio = session.get(Laboratorio, laboratorio_id)
    if laboratorio is None or not laboratorio.activo:
        raise ReglaError("RN-10", "El laboratorio no está disponible")
    if session.get(Usuario, usuario_id) is None:
        raise ReglaError("RN-04", "El titular no existe")

    franjas = asegurar_franjas(session, laboratorio_id, fecha)
    pedidas = [franja for franja in franjas if bloque_inicio <= franja.bloque <= bloque_fin]
    for franja in pedidas:
        if franja.estado in ("deshabilitada", "mantenimiento"):
            raise ReglaError("RN-10", "La franja no se puede reservar")
    if _solape_de_usuario(session, usuario_id, fecha, bloque_inicio, bloque_fin):
        raise ReglaError("RN-07", "Ya tiene una reserva confirmada en ese horario")
    for franja in pedidas:
        if franja.estado == "reservada":
            raise ReglaError("RN-08", "Ese laboratorio ya está reservado en ese horario")

    ahora_iso = ahora.isoformat(timespec="seconds")
    reserva = Reserva(
        usuario_id=usuario_id,
        laboratorio_id=laboratorio_id,
        fecha=fecha.isoformat(),
        bloque_inicio=bloque_inicio,
        bloque_fin=bloque_fin,
        estado="confirmada",
        origen=origen,
        creada_en=ahora_iso,
        creada_por=actor.id,
        actualizada_en=ahora_iso,
        desplaza_a=None,
    )
    session.add(reserva)
    session.flush()
    cambiadas = session.execute(
        update(Franja)
        .where(
            Franja.laboratorio_id == laboratorio_id,
            Franja.fecha == fecha.isoformat(),
            Franja.bloque >= bloque_inicio,
            Franja.bloque <= bloque_fin,
            Franja.estado == "libre",
        )
        .values(estado="reservada", reserva_id=reserva.id)
    )
    if cambiadas.rowcount != bloque_fin - bloque_inicio + 1:
        raise ReglaError("RN-08", "Ese laboratorio ya está reservado en ese horario")
    return reserva_dict(reserva)


def reservas_de(session: Session, usuario_id: int) -> list[dict]:
    reservas = session.scalars(
        select(Reserva).where(Reserva.usuario_id == usuario_id).order_by(Reserva.id)
    )
    return [reserva_dict(reserva) for reserva in reservas]


def _franjas_de_reserva(session: Session, reserva_id: int) -> list[Franja]:
    return list(session.scalars(select(Franja).where(Franja.reserva_id == reserva_id)))


def cancelar(session: Session, actor: Usuario, reserva_id: int, reloj) -> dict:
    reserva = session.get(Reserva, reserva_id)
    if reserva is None or reserva.estado != "confirmada":
        raise ReglaError("RN-17", "No hay una reserva confirmada para cancelar")
    if actor.rol != "administrador" and actor.id != reserva.usuario_id:
        raise PermisoError()
    fecha = date.fromisoformat(reserva.fecha)
    ahora = reloj.ahora()
    if fin_bloque(fecha, reserva.bloque_fin) <= ahora:
        raise ReglaError("RN-17", "La reserva ya terminó")
    if inicio_bloque(fecha, reserva.bloque_inicio) - ahora >= ANTELACION_CANCELACION:
        estado_franja = "libre"
    else:
        estado_franja = "deshabilitada"
    reserva.estado = "cancelada"
    reserva.actualizada_en = ahora.isoformat(timespec="seconds")
    session.execute(
        update(Franja)
        .where(Franja.reserva_id == reserva.id)
        .values(estado=estado_franja, reserva_id=None)
    )
    return {"reserva": reserva_dict(reserva), "estado_franjas": estado_franja}


def marcar_no_show(session: Session, actor: Usuario, reserva_id: int, reloj) -> dict:
    if actor.rol != "administrador":
        raise PermisoError()
    reserva = session.get(Reserva, reserva_id)
    if reserva is None or reserva.estado != "confirmada":
        raise ReglaError("RN-21", "No hay una reserva confirmada")
    fecha = date.fromisoformat(reserva.fecha)
    if inicio_bloque(fecha, reserva.bloque_inicio) > reloj.ahora():
        raise ReglaError("RN-21", "La reserva aún no ha empezado")
    reserva.estado = "no_show"
    reserva.actualizada_en = reloj.ahora().isoformat(timespec="seconds")
    session.execute(
        update(Franja)
        .where(Franja.reserva_id == reserva.id)
        .values(estado="deshabilitada", reserva_id=None)
    )
    return reserva_dict(reserva)


def liberar(session: Session, actor: Usuario, laboratorio_id: int, fecha: date, bloques: list[int]) -> dict:
    if actor.rol != "administrador":
        raise PermisoError()
    if not bloques:
        raise ReglaError("RN-22", "Indique al menos un bloque")
    franjas = asegurar_franjas(session, laboratorio_id, fecha)
    por_bloque = {franja.bloque: franja for franja in franjas}
    for bloque in bloques:
        franja = por_bloque.get(bloque)
        if franja is None or franja.estado != "deshabilitada":
            raise ReglaError("RN-22", "Solo se libera una franja deshabilitada")
    session.execute(
        update(Franja)
        .where(
            Franja.laboratorio_id == laboratorio_id,
            Franja.fecha == fecha.isoformat(),
            Franja.bloque.in_(bloques),
            Franja.estado == "deshabilitada",
        )
        .values(estado="libre", reserva_id=None)
    )
    return {"laboratorio_id": laboratorio_id, "fecha": fecha.isoformat(), "bloques": bloques, "estado": "libre"}


def mantenimiento(
    session: Session,
    actor: Usuario,
    laboratorio_id: int,
    fecha: date,
    bloques: list[int],
    activo: bool,
) -> dict:
    if actor.rol != "administrador":
        raise PermisoError()
    franjas = asegurar_franjas(session, laboratorio_id, fecha)
    por_bloque = {franja.bloque: franja for franja in franjas}
    origen = "libre" if activo else "mantenimiento"
    destino = "mantenimiento" if activo else "libre"
    for bloque in bloques:
        franja = por_bloque.get(bloque)
        if franja is None or franja.estado != origen:
            raise ReglaError("RN-23", "El mantenimiento solo cubre franjas libres, y al cerrarlo vuelven a libres")
    session.execute(
        update(Franja)
        .where(
            Franja.laboratorio_id == laboratorio_id,
            Franja.fecha == fecha.isoformat(),
            Franja.bloque.in_(bloques),
            Franja.estado == origen,
        )
        .values(estado=destino, reserva_id=None)
    )
    return {"laboratorio_id": laboratorio_id, "bloques": bloques, "estado": destino}


def _alternativas(session: Session, fecha: date, bloque_inicio: int, bloque_fin: int, excluir: int) -> list[str]:
    nombres = []
    laboratorios = session.scalars(
        select(Laboratorio).where(Laboratorio.activo == 1, Laboratorio.id != excluir).order_by(Laboratorio.nombre)
    )
    for laboratorio in laboratorios:
        franjas = asegurar_franjas(session, laboratorio.id, fecha)
        pedidas = [franja for franja in franjas if bloque_inicio <= franja.bloque <= bloque_fin]
        if pedidas and all(franja.estado == "libre" for franja in pedidas):
            nombres.append(laboratorio.nombre)
    return nombres


def desplazar(
    session: Session,
    actor: Usuario,
    reserva_id: int,
    bloque_inicio: int | None,
    bloque_fin: int | None,
    reloj,
    transporte=None,
) -> dict:
    if actor.rol != "docente":
        raise PermisoError()
    reserva = session.get(Reserva, reserva_id)
    if reserva is None or reserva.estado != "confirmada":
        raise ReglaError("RN-13", "No hay una reserva confirmada para desplazar")
    titular = session.get(Usuario, reserva.usuario_id)
    if titular is None or titular.rol != "estudiante":
        raise ReglaError("RN-13", "Solo se puede desplazar la reserva de un estudiante")
    if bloque_inicio is None and bloque_fin is None:
        bloque_inicio, bloque_fin = reserva.bloque_inicio, reserva.bloque_fin
    if bloque_inicio is None or bloque_fin is None:
        raise ReglaError("RN-02", "Indique el inicio y el fin del desplazamiento")
    if not (reserva.bloque_inicio <= bloque_inicio <= bloque_fin <= reserva.bloque_fin):
        raise ReglaError("RN-02", "Los bloques deben ser parte de la reserva del estudiante")
    validar_rango(bloque_inicio, bloque_fin)
    fecha = date.fromisoformat(reserva.fecha)
    ahora = reloj.ahora()
    for bloque in range(bloque_inicio, bloque_fin + 1):
        if fin_bloque(fecha, bloque) <= ahora:
            raise ReglaError("RN-13", "No se puede desplazar un bloque que ya terminó")
    if _solape_de_usuario(session, actor.id, fecha, bloque_inicio, bloque_fin):
        raise ReglaError("RN-07", "El docente ya tiene una reserva en ese horario")

    alternativas = _alternativas(session, fecha, bloque_inicio, bloque_fin, reserva.laboratorio_id)
    if alternativas:
        cuerpo = (
            "Tu reserva fue desplazada por un docente. "
            "Laboratorios libres en el mismo horario: " + ", ".join(alternativas) + "."
        )
    else:
        cuerpo = "Tu reserva fue desplazada por un docente. No hay otro laboratorio libre en ese horario."

    reserva.estado = "desplazada"
    reserva.actualizada_en = ahora.isoformat(timespec="seconds")
    session.execute(
        update(Franja)
        .where(Franja.reserva_id == reserva.id)
        .values(estado="libre", reserva_id=None)
    )
    session.flush()
    nueva = Reserva(
        usuario_id=actor.id,
        laboratorio_id=reserva.laboratorio_id,
        fecha=reserva.fecha,
        bloque_inicio=bloque_inicio,
        bloque_fin=bloque_fin,
        estado="confirmada",
        origen="en_linea",
        creada_en=ahora.isoformat(timespec="seconds"),
        creada_por=actor.id,
        actualizada_en=ahora.isoformat(timespec="seconds"),
        desplaza_a=reserva.id,
    )
    session.add(nueva)
    session.flush()
    cambiadas = session.execute(
        update(Franja)
        .where(
            Franja.laboratorio_id == reserva.laboratorio_id,
            Franja.fecha == reserva.fecha,
            Franja.bloque >= bloque_inicio,
            Franja.bloque <= bloque_fin,
            Franja.estado == "libre",
        )
        .values(estado="reservada", reserva_id=nueva.id)
    )
    if cambiadas.rowcount != bloque_fin - bloque_inicio + 1:
        raise ReglaError("RN-08", "El horario ya no está disponible")
    estado_envio = despachar(titular.correo, "Reserva desplazada", cuerpo, transporte)
    notificacion = Notificacion(
        reserva_id=reserva.id,
        destinatario_id=titular.id,
        tipo="desplazamiento",
        cuerpo=cuerpo,
        estado=estado_envio,
        creada_en=ahora.isoformat(timespec="seconds"),
    )
    session.add(notificacion)
    session.flush()
    return {
        "reserva_docente": reserva_dict(nueva),
        "reserva_estudiante": reserva_dict(reserva),
        "notificacion": {
            "id": notificacion.id,
            "estado": notificacion.estado,
            "cuerpo": notificacion.cuerpo,
            "laboratorios": alternativas,
        },
    }


def ocupacion(session: Session, desde: date, hasta: date) -> dict:
    if hasta < desde:
        raise ReglaError("RN-01", "El periodo es inválido")
    dias = (hasta - desde).days + 1
    laboratorios = session.scalar(select(Laboratorio.id).where(Laboratorio.activo == 1).limit(1))
    cantidad = len(session.scalars(select(Laboratorio).where(Laboratorio.activo == 1)).all())
    del laboratorios
    denominador = cantidad * 16 * dias
    reservadas = len(
        session.scalars(
            select(Franja).where(
                Franja.fecha >= desde.isoformat(),
                Franja.fecha <= hasta.isoformat(),
                Franja.estado == "reservada",
            )
        ).all()
    )
    porcentaje = (reservadas / denominador) if denominador else 0.0
    return {
        "desde": desde.isoformat(),
        "hasta": hasta.isoformat(),
        "reservadas": reservadas,
        "denominador": denominador,
        "porcentaje": porcentaje,
    }


def iso(momento: datetime) -> str:
    return momento.isoformat(timespec="seconds")
