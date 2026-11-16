import os
from datetime import date
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from starlette.middleware.sessions import SessionMiddleware

from reservas.db import init_db, make_engine, sesion_de, verifica_clave
from reservas.errors import PermisoError, ReglaError
from reservas.reloj import RelojSistema
from reservas.services import (
    cancelar,
    crear_reserva,
    desplazar,
    disponibilidad,
    liberar,
    mantenimiento,
    marcar_no_show,
    ocupacion,
    reservas_de,
    usuario_por_correo,
)

TEMPLATES = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))


class SesionIn(BaseModel):
    correo: str
    clave: str


class ReservaIn(BaseModel):
    laboratorio_id: int
    fecha: date
    bloque_inicio: int
    bloque_fin: int


class PresencialIn(ReservaIn):
    usuario_id: int


class DesplazarIn(BaseModel):
    bloque_inicio: int | None = None
    bloque_fin: int | None = None


class FranjasIn(BaseModel):
    laboratorio_id: int
    fecha: date
    bloques: list[int] = Field(min_length=1)


class MantenimientoIn(FranjasIn):
    activo: bool


def create_app(database_url: str, reloj=None) -> FastAPI:
    engine = make_engine(database_url)
    init_db(engine)
    fabrica = sesion_de(engine)
    app = FastAPI(title="Reservas de laboratorios")
    app.state.engine = engine
    app.state.reloj = reloj or RelojSistema()
    app.state.fabrica = fabrica
    app.add_middleware(SessionMiddleware, secret_key=os.environ.get("RESERVAS_SECRET", "reservas-dev"))

    @app.exception_handler(ReglaError)
    async def regla(_request, exc: ReglaError):
        return JSONResponse(status_code=409, content={"codigo": exc.codigo, "mensaje": exc.mensaje})

    @app.exception_handler(PermisoError)
    async def permiso(_request, exc: PermisoError):
        return JSONResponse(status_code=403, content={"mensaje": exc.mensaje})

    def db():
        return fabrica()

    def actor_actual(request: Request):
        usuario_id = request.session.get("usuario_id")
        if not usuario_id:
            raise HTTPException(status_code=401, detail="Se requiere sesión")
        with db() as session:
            from reservas.models import Usuario

            usuario = session.get(Usuario, usuario_id)
            if usuario is None:
                raise HTTPException(status_code=401, detail="Se requiere sesión")
            session.expunge(usuario)
            return usuario

    def ejecutar(fn):
        with db() as session:
            resultado = fn(session)
            session.commit()
            return resultado

    @app.post("/api/sesion")
    def abrir_sesion(body: SesionIn, request: Request):
        with db() as session:
            usuario = usuario_por_correo(session, body.correo)
            if usuario is None or not verifica_clave(body.clave, usuario.clave_hash):
                raise HTTPException(status_code=401, detail="Correo o clave incorrectos")
            request.session["usuario_id"] = usuario.id
            return {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol}

    @app.delete("/api/sesion")
    def cerrar_sesion(request: Request):
        request.session.clear()
        return {"ok": True}

    @app.get("/api/sesion")
    def ver_sesion(request: Request):
        usuario = actor_actual(request)
        return {"id": usuario.id, "nombre": usuario.nombre, "rol": usuario.rol}

    @app.get("/api/laboratorios")
    def laboratorios(request: Request):
        actor_actual(request)
        with db() as session:
            from reservas.models import Laboratorio
            from sqlalchemy import select

            labs = session.scalars(select(Laboratorio).where(Laboratorio.activo == 1)).all()
            return [{"id": lab.id, "nombre": lab.nombre, "ubicacion": lab.ubicacion} for lab in labs]

    @app.get("/api/disponibilidad")
    def ver_disponibilidad(fecha: date, request: Request):
        actor_actual(request)
        return ejecutar(lambda session: disponibilidad(session, fecha))

    @app.post("/api/reservas", status_code=201)
    def reservar(body: ReservaIn, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: crear_reserva(
                session,
                actor=session.merge(actor),
                usuario_id=actor.id,
                laboratorio_id=body.laboratorio_id,
                fecha=body.fecha,
                bloque_inicio=body.bloque_inicio,
                bloque_fin=body.bloque_fin,
                origen="en_linea",
                reloj=app.state.reloj,
            )
        )

    @app.post("/api/reservas/presenciales", status_code=201)
    def reservar_presencial(body: PresencialIn, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: crear_reserva(
                session,
                actor=session.merge(actor),
                usuario_id=body.usuario_id,
                laboratorio_id=body.laboratorio_id,
                fecha=body.fecha,
                bloque_inicio=body.bloque_inicio,
                bloque_fin=body.bloque_fin,
                origen="presencial",
                reloj=app.state.reloj,
            )
        )

    @app.get("/api/reservas")
    def listar_reservas(request: Request, mias: int = 1):
        actor = actor_actual(request)
        if mias != 1:
            raise HTTPException(status_code=422, detail="Use mias=1")
        with db() as session:
            return reservas_de(session, actor.id)

    @app.post("/api/reservas/{reserva_id}/cancelar")
    def cancelar_reserva(reserva_id: int, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: cancelar(session, session.merge(actor), reserva_id, app.state.reloj)
        )

    @app.post("/api/reservas/{reserva_id}/desplazar")
    def desplazar_reserva(reserva_id: int, body: DesplazarIn, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: desplazar(
                session,
                session.merge(actor),
                reserva_id,
                body.bloque_inicio,
                body.bloque_fin,
                app.state.reloj,
            )
        )

    @app.post("/api/reservas/{reserva_id}/no-show")
    def no_show(reserva_id: int, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: marcar_no_show(session, session.merge(actor), reserva_id, app.state.reloj)
        )

    @app.post("/api/franjas/liberar")
    def liberar_franjas(body: FranjasIn, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: liberar(session, session.merge(actor), body.laboratorio_id, body.fecha, body.bloques)
        )

    @app.post("/api/franjas/mantenimiento")
    def mantener(body: MantenimientoIn, request: Request):
        actor = actor_actual(request)
        return ejecutar(
            lambda session: mantenimiento(
                session, session.merge(actor), body.laboratorio_id, body.fecha, body.bloques, body.activo
            )
        )

    @app.get("/api/ocupacion")
    def ver_ocupacion(desde: date, hasta: date, request: Request):
        actor_actual(request)
        with db() as session:
            return ocupacion(session, desde, hasta)

    def pagina(request: Request, nombre: str, **extra):
        usuario = None
        if request.session.get("usuario_id"):
            usuario = actor_actual(request)
        return TEMPLATES.TemplateResponse(
            request,
            nombre,
            {"usuario": usuario, "error": request.query_params.get("error"), **extra},
        )

    @app.get("/", response_class=HTMLResponse)
    def inicio(request: Request, fecha: date | None = None):
        if not request.session.get("usuario_id"):
            return RedirectResponse("/entrar", status_code=303)
        dia = fecha or app.state.reloj.ahora().date()
        datos = ejecutar(lambda session: disponibilidad(session, dia))
        return pagina(request, "disponibilidad.html", fecha=dia.isoformat(), laboratorios=datos)

    @app.get("/entrar", response_class=HTMLResponse)
    def entrar(request: Request):
        return pagina(request, "entrar.html")

    @app.post("/entrar")
    async def entrar_form(request: Request):
        form = await request.form()
        with db() as session:
            usuario = usuario_por_correo(session, str(form.get("correo", "")))
            if usuario is None or not verifica_clave(str(form.get("clave", "")), usuario.clave_hash):
                return RedirectResponse("/entrar?error=Correo+o+clave+incorrectos", status_code=303)
            request.session["usuario_id"] = usuario.id
        return RedirectResponse("/", status_code=303)

    @app.post("/salir")
    def salir(request: Request):
        request.session.clear()
        return RedirectResponse("/entrar", status_code=303)

    @app.post("/reservas")
    async def reservar_form(request: Request):
        actor = actor_actual(request)
        form = await request.form()
        try:
            body = ReservaIn(
                laboratorio_id=int(form["laboratorio_id"]),
                fecha=date.fromisoformat(str(form["fecha"])),
                bloque_inicio=int(form["bloque_inicio"]),
                bloque_fin=int(form["bloque_fin"]),
            )
            ejecutar(
                lambda session: crear_reserva(
                    session,
                    actor=session.merge(actor),
                    usuario_id=actor.id,
                    laboratorio_id=body.laboratorio_id,
                    fecha=body.fecha,
                    bloque_inicio=body.bloque_inicio,
                    bloque_fin=body.bloque_fin,
                    origen="en_linea",
                    reloj=app.state.reloj,
                )
            )
        except (ReglaError, ValueError, KeyError) as exc:
            mensaje = exc.mensaje if isinstance(exc, ReglaError) else "Datos de reserva incompletos"
            return RedirectResponse(f"/?error={mensaje.replace(' ', '+')}", status_code=303)
        return RedirectResponse("/reservas", status_code=303)

    @app.get("/reservas", response_class=HTMLResponse)
    def mis_reservas(request: Request):
        actor = actor_actual(request)
        with db() as session:
            lista = reservas_de(session, actor.id)
        return pagina(request, "reservas.html", reservas=lista)

    @app.post("/reservas/{reserva_id}/cancelar")
    def cancelar_form(reserva_id: int, request: Request):
        actor = actor_actual(request)
        try:
            ejecutar(lambda session: cancelar(session, session.merge(actor), reserva_id, app.state.reloj))
        except ReglaError as exc:
            return RedirectResponse(f"/reservas?error={exc.mensaje.replace(' ', '+')}", status_code=303)
        return RedirectResponse("/reservas", status_code=303)

    @app.get("/admin", response_class=HTMLResponse)
    def admin(request: Request):
        actor = actor_actual(request)
        if actor.rol != "administrador":
            raise HTTPException(status_code=403, detail="Solo el administrador")
        hoy = app.state.reloj.ahora().date()
        with db() as session:
            from reservas.models import Usuario
            from sqlalchemy import select

            usuarios = session.scalars(select(Usuario).order_by(Usuario.nombre)).all()
            datos_ocupacion = ocupacion(session, hoy, hoy)
            personas = [{"id": u.id, "nombre": u.nombre, "rol": u.rol} for u in usuarios]
        return pagina(request, "admin.html", personas=personas, ocupacion=datos_ocupacion, hoy=hoy.isoformat())

    def redirigir_admin(exc: Exception):
        mensaje = exc.mensaje if isinstance(exc, ReglaError) else "No se pudo completar la acción"
        return RedirectResponse(f"/admin?error={mensaje.replace(' ', '+')}", status_code=303)

    @app.post("/admin/presencial")
    async def admin_presencial(request: Request):
        actor = actor_actual(request)
        form = await request.form()
        try:
            ejecutar(
                lambda session: crear_reserva(
                    session,
                    actor=session.merge(actor),
                    usuario_id=int(form["usuario_id"]),
                    laboratorio_id=int(form["laboratorio_id"]),
                    fecha=date.fromisoformat(str(form["fecha"])),
                    bloque_inicio=int(form["bloque_inicio"]),
                    bloque_fin=int(form["bloque_fin"]),
                    origen="presencial",
                    reloj=app.state.reloj,
                )
            )
        except (ReglaError, ValueError, KeyError) as exc:
            return redirigir_admin(exc)
        return RedirectResponse("/admin", status_code=303)

    @app.post("/admin/mantenimiento")
    async def admin_mantenimiento(request: Request):
        actor = actor_actual(request)
        form = await request.form()
        try:
            ejecutar(
                lambda session: mantenimiento(
                    session,
                    session.merge(actor),
                    int(form["laboratorio_id"]),
                    date.fromisoformat(str(form["fecha"])),
                    [int(form["bloque"])],
                    str(form["activo"]) == "true",
                    )
            )
        except (ReglaError, ValueError, KeyError) as exc:
            return redirigir_admin(exc)
        return RedirectResponse("/admin", status_code=303)

    @app.post("/admin/liberar")
    async def admin_liberar(request: Request):
        actor = actor_actual(request)
        form = await request.form()
        try:
            ejecutar(
                lambda session: liberar(
                    session,
                    session.merge(actor),
                    int(form["laboratorio_id"]),
                    date.fromisoformat(str(form["fecha"])),
                    [int(form["bloque"])],
                )
            )
        except (ReglaError, ValueError, KeyError) as exc:
            return redirigir_admin(exc)
        return RedirectResponse("/admin", status_code=303)

    return app


def _url_por_defecto() -> str:
    ruta = os.environ.get("RESERVAS_DB", "data/reservas.db")
    path = Path(ruta)
    path.parent.mkdir(parents=True, exist_ok=True)
    return f"sqlite:///{path}"


app = create_app(_url_por_defecto())
