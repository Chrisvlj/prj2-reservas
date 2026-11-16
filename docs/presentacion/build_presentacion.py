"""Presentación del proyecto 2 con el diseño de CitaFácil."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

SALIDA = Path(__file__).resolve().parent / "reservas-laboratorios.pptx"

NAVY = RGBColor(0x13, 0x20, 0x3C)
ORANGE = RGBColor(0xE7, 0x82, 0x39)
CREAM = RGBColor(0xF3, 0xF0, 0xE9)
WHITE = RGBColor(0xFE, 0xFC, 0xF7)
INK = RGBColor(0x13, 0x20, 0x3C)
MUTED = RGBColor(0x53, 0x5C, 0x6E)
ROW = RGBColor(0xEB, 0xE5, 0xD9)

W = Inches(13.333)
H = Inches(7.5)


def _run(parrafo, texto, tamano, color, negrita=False):
    run = parrafo.add_run()
    run.text = texto
    run.font.name = "Calibri"
    run.font.size = Pt(tamano)
    run.font.color.rgb = color
    run.font.bold = negrita
    return run


def _tf(shape, ancla="t"):
    marco = shape.text_frame
    marco.word_wrap = True
    marco.auto_size = None
    marco.margin_left = Emu(0)
    marco.margin_right = Emu(0)
    marco.margin_top = Emu(0)
    marco.margin_bottom = Emu(0)
    marco._txBody.bodyPr.set("anchor", ancla)
    return marco


def texto(slide, x, y, w, h, lineas, alineacion=PP_ALIGN.LEFT, ancla="t"):
    caja = slide.shapes.add_textbox(x, y, w, h)
    marco = _tf(caja, ancla)
    for i, (contenido, tamano, color, negrita, espacio) in enumerate(lineas):
        parrafo = marco.paragraphs[0] if i == 0 else marco.add_paragraph()
        parrafo.alignment = alineacion
        parrafo.space_after = Pt(espacio)
        _run(parrafo, contenido, tamano, color, negrita)
    return caja


def fondo(slide, color):
    forma = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, W, H)
    forma.fill.solid()
    forma.fill.fore_color.rgb = color
    forma.line.fill.background()
    return forma


def ronda(slide, x, y, w, h, color):
    forma = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, w, h)
    forma.adjustments[0] = 0.08
    forma.fill.solid()
    forma.fill.fore_color.rgb = color
    forma.line.fill.background()
    return forma


def barra(slide):
    forma = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(0.12), H)
    forma.fill.solid()
    forma.fill.fore_color.rgb = ORANGE
    forma.line.fill.background()


def notas(slide, cuerpo):
    slide.notes_slide.notes_text_frame.text = cuerpo


def kicker(slide, etiqueta, y=Inches(0.42)):
    texto(slide, Inches(0.62), y, Inches(8), Inches(0.32), [(etiqueta.upper(), 13, ORANGE, True, 0)])


def titulo(slide, frase, y=Inches(0.78)):
    texto(slide, Inches(0.62), y, Inches(12), Inches(1.15), [(frase, 32, NAVY, True, 0)])


def nueva(prs, oscura=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    fondo(slide, NAVY if oscura else CREAM)
    return slide


def construir():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H
    prs.core_properties.title = "Reservas de laboratorios"
    prs.core_properties.subject = "Proyecto 2 · Tópicos Especiales II"

    portada = nueva(prs, oscura=True)
    barra(portada)
    texto(portada, Inches(0.7), Inches(1.55), Inches(11), Inches(0.35), [("TÓPICOS ESPECIALES II  ·  PROYECTO #2", 14, ORANGE, True, 0)])
    texto(portada, Inches(0.7), Inches(2.15), Inches(12), Inches(1.1), [("Reservas de laboratorios", 54, WHITE, True, 0)])
    texto(
        portada,
        Inches(0.7),
        Inches(3.4),
        Inches(10.5),
        Inches(1.1),
        [("Ver la disponibilidad y reservar un laboratorio sin ir a consultarlo,\ncon las reglas, las pruebas y un cambio de especificación a mitad.", 20, RGBColor(0xD7, 0xDE, 0xE8), False, 0)],
    )
    roles = [("DEVELOPER", "Jorge de Leon"), ("QA", "Christian Valdespino"), ("REVIEWER", "Eriel Tensu")]
    for i, (rol, nombre) in enumerate(roles):
        x = Inches(0.7 + i * 3.3)
        texto(portada, x, Inches(5.55), Inches(3), Inches(0.28), [(rol, 11, RGBColor(0x9A, 0xA6, 0xB8), True, 0)])
        texto(portada, x, Inches(5.88), Inches(3), Inches(0.4), [(nombre, 16, WHITE, False, 0)])
    notas(portada, "Abrir con el resultado: reservar sin ir al laboratorio. Los nombres son el mismo grupo del proyecto 1.")

    contexto = nueva(prs)
    kicker(contexto, "Contexto")
    titulo(contexto, "Elegimos laboratorios: saber el cupo\nsin desplazarse")
    tarjetas = [
        ("PANTALLA", "HTML con Jinja2,\nsin framework aparte"),
        ("BACK-END", "Python 3, FastAPI\ny SQLAlchemy"),
        ("BASE DE DATOS", "SQLite en un archivo.\nLa misma verdad en pantalla y en la reserva"),
        ("HERRAMIENTA IA", "Cursor, agente CLI.\nEl uso queda en docs/ai-log.md"),
    ]
    for i, (etiqueta, cuerpo) in enumerate(tarjetas):
        x = Inches(0.62 + i * 3.15)
        ronda(contexto, x, Inches(3.35), Inches(2.95), Inches(2.15), WHITE)
        texto(contexto, x + Inches(0.22), Inches(3.55), Inches(2.55), Inches(0.3), [(etiqueta, 11, MUTED, True, 0)])
        texto(contexto, x + Inches(0.22), Inches(4.0), Inches(2.55), Inches(1.2), [(cuerpo, 15, INK, False, 0)])
    texto(
        contexto,
        Inches(0.62),
        Inches(5.75),
        Inches(12),
        Inches(0.7),
        [("Antes del código: el resultado en specs/outcomes.md y las reglas en specs/.", 16, INK, False, 0)],
    )
    texto(contexto, Inches(0.62), Inches(6.7), Inches(12), Inches(0.35), [("Repositorio: github.com/Chrisvlj/prj2-reservas", 13, MUTED, False, 0)])
    notas(contexto, "ODD primero, SDD después. No empezar por el framework.")

    proceso = nueva(prs)
    kicker(proceso, "Proceso")
    titulo(proceso, "Cada cambio pasó por el mismo ciclo")
    pasos = [
        ("1", "ODD", "Problema, usuarios\ny el resultado", False),
        ("2", "SDD", "Reglas, criterios\ny el plan", False),
        ("3", "Código + tests", "La regla y la prueba\nvan juntas", False),
        ("4", "Cambio", "RN-25: tope\nsemanal", False),
        ("5", "PR", "El núcleo en #10\ny el tope en #12", True),
    ]
    for i, (numero, nombre, detalle, oscuro) in enumerate(pasos):
        x = Inches(0.5 + i * 2.55)
        ronda(proceso, x, Inches(3.15), Inches(2.4), Inches(2.55), NAVY if oscuro else WHITE)
        color_num = ORANGE
        color_txt = WHITE if oscuro else INK
        color_det = RGBColor(0xD7, 0xDE, 0xE8) if oscuro else MUTED
        texto(proceso, x + Inches(0.2), Inches(3.32), Inches(2), Inches(0.4), [(numero, 20, color_num, True, 0)])
        texto(proceso, x + Inches(0.2), Inches(3.8), Inches(2), Inches(0.55), [(nombre, 16, color_txt, True, 0)])
        texto(proceso, x + Inches(0.2), Inches(4.45), Inches(2), Inches(0.9), [(detalle, 13, color_det, False, 0)])
    texto(
        proceso,
        Inches(0.62),
        Inches(6.15),
        Inches(12),
        Inches(0.6),
        [("main solo recibe lo que ya tiene prueba. El tablero del proyecto tiene las tareas en Done.", 16, INK, False, 0)],
    )
    notas(proceso, "Si preguntan el orden: resultado, especificación, código, prueba, pull request.")

    piezas = nueva(prs)
    titulo(piezas, "Seis reglas que sostienen el resultado", y=Inches(0.42))
    texto(piezas, Inches(8.6), Inches(0.55), Inches(4.2), Inches(0.4), [("Del outcome a la prueba", 13, MUTED, False, 0)], PP_ALIGN.RIGHT)
    bloques = [
        ("RF-01", "Ver el día", "16 bloques por laboratorio:\nlibre, reservado, deshabilitado\no mantenimiento."),
        ("RN-02", "De 1 a 3 bloques", "Cada bloque son 45 minutos\nde uso y 5 de transición.\nLa jornada cierra a las 20:20."),
        ("RN-08", "Un solo cupo", "No hay dos reservas\nconfirmadas del mismo\nlaboratorio a la misma hora."),
        ("RN-07", "Una persona, un lugar", "No puede tener dos reservas\nconfirmadas que se solapen,\naunque sean laboratorios distintos."),
        ("RN-12", "Prioridad del docente", "Desplaza al estudiante,\nse guarda el aviso y se nombran\notros laboratorios libres."),
        ("RN-25", "Tope de la semana", "El estudiante tiene máximo\n2 confirmadas de lunes\na domingo. El docente no."),
    ]
    for i, (codigo, nombre, detalle) in enumerate(bloques):
        col, fila = i % 3, i // 3
        x = Inches(0.55 + col * 4.2)
        y = Inches(1.85 + fila * 2.55)
        ronda(piezas, x, y, Inches(4.0), Inches(2.35), WHITE)
        texto(piezas, x + Inches(0.25), y + Inches(0.18), Inches(3.5), Inches(0.28), [(codigo, 12, ORANGE, True, 0)])
        texto(piezas, x + Inches(0.25), y + Inches(0.5), Inches(3.5), Inches(0.4), [(nombre, 18, NAVY, True, 0)])
        texto(piezas, x + Inches(0.25), y + Inches(1.05), Inches(3.5), Inches(1.05), [(detalle, 13, MUTED, False, 0)])
    notas(piezas, "RN-25 entró a mitad, cuando el núcleo ya estaba en main.")

    validacion = nueva(prs, oscura=True)
    texto(validacion, Inches(0.7), Inches(0.55), Inches(6), Inches(0.3), [("VALIDACIÓN", 13, ORANGE, True, 0)])
    texto(validacion, Inches(0.7), Inches(1.05), Inches(10), Inches(0.7), [("Lo que quedó en verde", 36, WHITE, True, 0)])
    cifras = [
        ("31", "pruebas pytest,\nincluida la obligatoria", False),
        ("1", "de dos solicitudes\nsimultáneas se confirma", True),
        ("16", "bloques en la jornada,\nde 07:00 a 20:20", False),
        ("10", "issues cerrados,\ndel plan y del cambio", False),
    ]
    for i, (numero, detalle, destacado) in enumerate(cifras):
        x = Inches(0.7 + i * 3.15)
        texto(validacion, x, Inches(2.7), Inches(2.9), Inches(1.3), [(numero, 60, ORANGE if destacado else WHITE, True, 0)])
        linea = validacion.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(4.15), Inches(2.4), Inches(0.015))
        linea.fill.solid()
        linea.fill.fore_color.rgb = RGBColor(0x3A, 0x4A, 0x66)
        linea.line.fill.background()
        texto(validacion, x, Inches(4.35), Inches(2.8), Inches(1.2), [(detalle, 15, RGBColor(0xD7, 0xDE, 0xE8), False, 0)])
    texto(validacion, Inches(0.7), Inches(6.55), Inches(11), Inches(0.4), [("Evidencia: pytest y docs/evidencias/12-rn25-pruebas.png", 13, RGBColor(0x9A, 0xA6, 0xB8), False, 0)])
    notas(validacion, "La cifra naranja es la prueba de no doble reserva. De dos hilos, uno recibe 201 y el otro RN-08.")

    tabla = nueva(prs)
    kicker(tabla, "Reglas")
    titulo(tabla, "Cinco rechazos que el usuario puede ver", y=Inches(0.78))
    filas = [
        ("RN-05", "Antelación", "En línea hacen falta 60 minutos. Con menos, solo el administrador.", "Presencial"),
        ("RN-08", "Cupo", "Dos personas no confirman el mismo laboratorio a la misma hora.", "Quien persiste primero"),
        ("RN-07", "Solape propio", "La misma persona no queda en dos laboratorios a la vez.", "Aunque el otro esté libre"),
        ("RN-19", "Cancelar tarde", "Con menos de 24 horas el bloque queda deshabilitado.", "Solo el administrador lo libera"),
        ("RN-25", "Semana", "La tercera reserva confirmada del estudiante se rechaza.", "El docente no tiene tope"),
    ]
    encabezados = ["ID", "Regla", "Qué pasa", "Detalle"]
    anchos = [Inches(1.3), Inches(2.1), Inches(6.3), Inches(2.6)]
    x0, y0 = Inches(0.55), Inches(2.25)
    alto = Inches(0.62)
    x = x0
    for encabezado, ancho in zip(encabezados, anchos):
        celda = tabla.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y0, ancho, alto)
        celda.fill.solid()
        celda.fill.fore_color.rgb = NAVY
        celda.line.fill.background()
        texto(tabla, x + Inches(0.12), y0, ancho - Inches(0.15), alto, [(encabezado, 13, WHITE, True, 0)], ancla="ctr")
        x += ancho
    for n, fila in enumerate(filas):
        y = y0 + alto * (n + 1)
        x = x0
        for valor, ancho in zip(fila, anchos):
            celda = tabla.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, ancho, alto)
            celda.fill.solid()
            celda.fill.fore_color.rgb = WHITE if n % 2 == 0 else ROW
            celda.line.fill.background()
            texto(tabla, x + Inches(0.12), y, ancho - Inches(0.18), alto, [(valor, 12, INK, False, 0)], ancla="ctr")
            x += ancho
    notas(tabla, "El orden de rechazo en la API es antelación, estado de la franja, solape de la persona, tope semanal y cupo.")

    caso = nueva(prs)
    kicker(caso, "El caso de la doble reserva")
    titulo(caso, "Dos personas, un solo laboratorio", y=Inches(0.85))
    texto(caso, Inches(0.62), Inches(2.5), Inches(3.2), Inches(1.5), [("1", 92, ORANGE, True, 0)])
    texto(caso, Inches(0.62), Inches(4.3), Inches(4.2), Inches(1.5), [("de las dos solicitudes\nqueda confirmada", 20, INK, False, 0)])
    texto(
        caso,
        Inches(5.3),
        Inches(2.55),
        Inches(7.3),
        Inches(3.3),
        [
            ("La lectura del cupo y la escritura van en la misma transacción.", 20, INK, False, 10),
            ("La prueba lanza las dos a la vez. Una responde 201 y la otra RN-08.", 20, INK, False, 10),
            ("Sin esa transacción, las dos podían leer «libre» y las dos confirmaban.", 20, INK, True, 0),
        ],
    )
    notas(caso, "El test está en tests/test_no_doble_reserva.py, test_ca08. No hace falta una sola ejecución para darlo por bueno: la prueba ya corre las dos juntas.")

    decisiones = nueva(prs)
    kicker(decisiones, "Decisiones")
    titulo(decisiones, "Lo que quedó fijo para poder probarlo")
    columnas = [
        (
            "Qué se decidió",
            [
                "16 bloques de 50 minutos terminan a las 20:20, no a las 21:00.",
                "«Un día» para cancelar son 24 horas antes del inicio.",
                "La semana del tope va de lunes a domingo.",
                "Si el correo falla, el desplazamiento igual queda guardado.",
            ],
        ),
        (
            "Dónde se ve",
            [
                "ADR-002 en docs/decisions.md.",
                "RN-18 y RN-19, con reloj fijo en las pruebas.",
                "ADR-005, issue #11 y el pull request #12.",
                "La notificación queda en pendiente o en error.",
            ],
        ),
    ]
    for i, (cabeza, items) in enumerate(columnas):
        x = Inches(0.55 + i * 6.4)
        ronda(decisiones, x, Inches(2.35), Inches(6.1), Inches(4.5), WHITE)
        texto(decisiones, x + Inches(0.35), Inches(2.55), Inches(5.4), Inches(0.45), [(cabeza, 18, NAVY, True, 0)])
        texto(
            decisiones,
            x + Inches(0.35),
            Inches(3.2),
            Inches(5.4),
            Inches(3.3),
            [(f"•  {item}", 15, INK, False, 8) for item in items],
        )
    notas(decisiones, "Estas decisiones cierran huecos del outcome. Si el horario institucional es otro, se cambia RN-01 en un solo lugar.")

    restricciones = nueva(prs)
    titulo(restricciones, "Lo que pide el enunciado", y=Inches(0.28))
    encabezado = ("#", "Restricción", "Dónde se demuestra")
    requisitos = [
        ("1", "Repositorio Git", "github.com/Chrisvlj/prj2-reservas"),
        ("2", "Especificaciones", "specs/: outcome, reglas, API, criterios y plan"),
        ("3", "Issues", "#1 a #9 del plan, y #11 del cambio de requisito"),
        ("4", "Commits", "El mensaje dice por qué, no solo qué archivo cambió"),
        ("5", "Ramas", "tarea/sistema-reservas, tarea/11-tope-semanal, tarea/presentacion"),
        ("6", "Pull request", "#10 el núcleo, #12 el tope, #13 esta presentación"),
        ("7", "Pruebas", "31 pytest. La de no doble reserva es obligatoria"),
        ("8", "Uso de IA", "docs/ai-log.md: solicitud, resultado y decisión"),
        ("9", "Cambio de spec", "RN-25, desde la regla hasta la prueba en verde"),
        ("10", "Arquitectura", "Python, FastAPI y SQLite, en specs/architecture.md"),
    ]
    y0 = Inches(1.35)
    alto = Inches(0.5)
    anchos = [Inches(0.7), Inches(2.6), Inches(9.2)]
    x0 = Inches(0.5)

    def fila_tabla(destino, y, valores, relleno, color, negrita):
        x = x0
        for valor, ancho in zip(valores, anchos):
            celda = destino.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, ancho, alto)
            celda.fill.solid()
            celda.fill.fore_color.rgb = relleno
            celda.line.fill.background()
            texto(destino, x + Inches(0.1), y, ancho - Inches(0.14), alto, [(valor, 12, color, negrita, 0)], ancla="ctr")
            x += ancho

    fila_tabla(restricciones, y0, encabezado, NAVY, WHITE, True)
    for n, fila in enumerate(requisitos):
        fila_tabla(restricciones, y0 + alto * (n + 1), fila, WHITE if n % 2 == 0 else ROW, INK, False)
    notas(restricciones, "Si piden una restricción, abrir el archivo de esa fila. No recitar las diez.")

    vivo = nueva(prs)
    kicker(vivo, "En la sustentación")
    titulo(vivo, "Si piden un cambio, el ciclo no se salta")
    vivos = [
        ("1", "Anotar\nel cambio"),
        ("2", "Actualizar\nla regla y el criterio"),
        ("3", "Cambiar\nel código"),
        ("4", "Dejar la prueba\nen verde"),
    ]
    for i, (numero, frase) in enumerate(vivos):
        x = Inches(0.55 + i * 3.2)
        ronda(vivo, x, Inches(2.45), Inches(3.0), Inches(2.15), WHITE)
        texto(vivo, x + Inches(0.25), Inches(2.65), Inches(2.5), Inches(0.5), [(numero, 26, ORANGE, True, 0)])
        texto(vivo, x + Inches(0.25), Inches(3.25), Inches(2.5), Inches(1.0), [(frase, 18, INK, True, 0)])
    texto(
        vivo,
        Inches(0.62),
        Inches(5.05),
        Inches(12),
        Inches(1.5),
        [
            ("Ejemplo ya hecho: el tope de 2 reservas por semana.", 20, INK, False, 6),
            ("Toca RN-25, CA-24, la constante del código y tests/test_tope_semanal.py.", 20, INK, False, 6),
            ("La pantalla no tiene una copia aparte de la regla.", 20, NAVY, True, 0),
        ],
    )
    notas(vivo, "Ofrecer recorrer ese orden. Si no hay tiempo, mostrar el diff del pull request #12.")

    cierre = nueva(prs, oscura=True)
    barra(cierre)
    texto(
        cierre,
        Inches(0.7),
        Inches(0.7),
        Inches(12),
        Inches(2.2),
        [("La disponibilidad que se ve\nes la misma que se reserva.", 36, WHITE, True, 0)],
    )
    cierres = [
        ("Demo en vivo", "Entrar como Ana, elegir el día\ny confirmar de 1 a 3 bloques."),
        ("Listos para un cambio", "Regla, criterio, código\ny prueba. En ese orden."),
        ("Todo en el repo", "specs/, tests/, ai-log.md\ny los pull requests #10 y #12."),
    ]
    for i, (etiqueta, detalle) in enumerate(cierres):
        x = Inches(0.7 + i * 4.1)
        linea = cierre.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(3.7), Inches(1.3), Inches(0.045))
        linea.fill.solid()
        linea.fill.fore_color.rgb = ORANGE
        linea.line.fill.background()
        texto(cierre, x, Inches(3.9), Inches(3.7), Inches(0.45), [(etiqueta, 16, ORANGE, True, 0)])
        texto(cierre, x, Inches(4.5), Inches(3.7), Inches(1.1), [(detalle, 15, RGBColor(0xD7, 0xDE, 0xE8), False, 0)])
    texto(cierre, Inches(0.7), Inches(6.45), Inches(4), Inches(0.4), [("¿Preguntas?", 18, RGBColor(0x9A, 0xA6, 0xB8), False, 0)])
    notas(cierre, "Cuentas: ana@lab.test / ana, luis@lab.test / luis, rosa@lab.test / rosa.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SALIDA)
    print(SALIDA)


if __name__ == "__main__":
    construir()
