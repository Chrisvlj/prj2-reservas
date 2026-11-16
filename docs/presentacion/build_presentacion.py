"""Presentación del proyecto 2.

El color y el ritmo salen de la plantilla de CitaFácil.
El relato sigue el PDF: ODD, SDD, código, pruebas, valor,
y estar listos para un cambio durante la sustentación.
"""

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
    texto(portada, Inches(0.7), Inches(1.45), Inches(11), Inches(0.35), [("TÓPICOS ESPECIALES II  ·  PROYECTO #2", 14, ORANGE, True, 0)])
    texto(portada, Inches(0.7), Inches(2.0), Inches(12), Inches(1.2), [("Reservas de laboratorios", 52, WHITE, True, 0)])
    texto(
        portada,
        Inches(0.7),
        Inches(3.35),
        Inches(11),
        Inches(1.2),
        [("ODD  →  SDD  →  código  →  pruebas  →  valor para quien reserva", 22, RGBColor(0xD7, 0xDE, 0xE8), False, 0)],
    )
    texto(
        portada,
        Inches(0.7),
        Inches(5.15),
        Inches(11),
        Inches(1.2),
        [
            ("Jorge de Leon    ·    Christian Valdespino    ·    Eriel Tensu", 18, WHITE, False, 8),
            ("Los roles rotan. Presenta quien salga al azar.", 15, RGBColor(0x9A, 0xA6, 0xB8), False, 0),
        ],
    )
    notas(portada, "El enunciado pide el recorrido completo y que cualquiera del grupo pueda presentarlo. No abrir por la herramienta.")

    problema = nueva(prs)
    kicker(problema, "ODD  ·  el problema")
    titulo(problema, "Hoy se enteran de que no hay cupo\ncuando ya llegaron")
    puntos = [
        "La reserva del laboratorio es física.",
        "Para saber si está libre hay que ir.",
        "Como a veces está ocupado, reservan con mucha antelación.",
        "Eso produce viajes inútiles, cruces de horario y laboratorios mal usados.",
    ]
    for i, punto in enumerate(puntos):
        y = Inches(2.55 + i * 1.05)
        ronda(problema, Inches(0.62), y, Inches(12.1), Inches(0.9), WHITE)
        texto(problema, Inches(0.95), y, Inches(11.4), Inches(0.9), [(punto, 20, INK, False, 0)], ancla="ctr")
    notas(problema, "Esta es la fase 1. La pregunta del PDF no es qué aplicación programar, sino qué resultado queremos para el usuario.")

    resultado = nueva(prs)
    kicker(resultado, "ODD  ·  el resultado")
    titulo(resultado, "Ver el horario libre y reservar\nsin desplazarse")
    metricas = [
        ("Cruces", "Menos de 4 por semana", "El sistema se diseña para cero. El margen es por si falla."),
        ("Tiempo", "Menos de 3 minutos", "Con la sesión ya iniciada: ver, elegir, confirmar."),
        ("Ocupación", "De 40 % a 70 %", "Meta realista. No se inventan reservas para subirla."),
    ]
    for i, (nombre, valor, detalle) in enumerate(metricas):
        x = Inches(0.55 + i * 4.2)
        ronda(resultado, x, Inches(3.15), Inches(3.95), Inches(3.15), WHITE)
        texto(resultado, x + Inches(0.28), Inches(3.4), Inches(3.4), Inches(0.35), [(nombre.upper(), 13, ORANGE, True, 0)])
        texto(resultado, x + Inches(0.28), Inches(3.9), Inches(3.4), Inches(0.9), [(valor, 24, NAVY, True, 0)])
        texto(resultado, x + Inches(0.28), Inches(5.05), Inches(3.4), Inches(0.95), [(detalle, 15, MUTED, False, 0)])
    notas(resultado, "Docente y estudiante consultan la misma disponibilidad con la que se confirma la reserva.")

    usuarios = nueva(prs)
    kicker(usuarios, "ODD  ·  quién lo usa")
    titulo(usuarios, "Tres necesidades distintas")
    personas = [
        ("Estudiante", "Consulta y reserva para clase o uso personal."),
        ("Docente", "Reserva, y puede desplazar la reserva de un estudiante."),
        ("Administrador", "Registra lo presencial, el mantenimiento y libera lo deshabilitado."),
    ]
    for i, (rol, detalle) in enumerate(personas):
        y = Inches(2.4 + i * 1.5)
        ronda(usuarios, Inches(0.62), y, Inches(12.1), Inches(1.32), WHITE)
        barra_rol = usuarios.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.62), y, Inches(0.1), Inches(1.32))
        barra_rol.fill.solid()
        barra_rol.fill.fore_color.rgb = ORANGE if i == 1 else NAVY
        barra_rol.line.fill.background()
        texto(usuarios, Inches(1.05), y + Inches(0.18), Inches(11), Inches(0.4), [(rol, 22, NAVY, True, 0)])
        texto(usuarios, Inches(1.05), y + Inches(0.68), Inches(11), Inches(0.4), [(detalle, 18, INK, False, 0)])
    notas(usuarios, "Entre docentes gana quien reservó primero. El docente solo desplaza a un estudiante.")

    specs = nueva(prs)
    kicker(specs, "SDD  ·  la especificación")
    titulo(specs, "El resultado se volvió reglas\nantes de escribir código")
    docs = [
        ("specs/outcomes.md", "Problema, usuarios y métricas."),
        ("specs/business-rules.md", "RN-01 a RN-25, cada una comprobable."),
        ("specs/acceptance-criteria.md", "CA-01 a CA-28, con reloj fijo."),
        ("specs/implementation-plan.md", "El orden de construcción y el cambio de mitad."),
    ]
    for i, (archivo, detalle) in enumerate(docs):
        col, fila = i % 2, i // 2
        x = Inches(0.55 + col * 6.4)
        y = Inches(3.2 + fila * 1.8)
        ronda(specs, x, y, Inches(6.15), Inches(1.6), WHITE)
        texto(specs, x + Inches(0.3), y + Inches(0.25), Inches(5.6), Inches(0.4), [(archivo, 18, NAVY, True, 0)])
        texto(specs, x + Inches(0.3), y + Inches(0.8), Inches(5.6), Inches(0.5), [(detalle, 16, MUTED, False, 0)])
    notas(specs, "También están architecture.md, data-model.md y api.md. El stack está declarado en la arquitectura, como pide el enunciado.")

    arquitectura = nueva(prs)
    kicker(arquitectura, "Código")
    titulo(arquitectura, "Una sola verdad del horario")
    hechos = [
        ("Python, FastAPI y SQLite", "Una aplicación. Sin una segunda copia de las reglas en el navegador."),
        ("Página y API juntas", "Reservar en pantalla usa el mismo caso de uso que el JSON."),
        ("Una transacción", "Si dos personas piden el mismo cupo, solo una queda confirmada."),
        ("pytest", "Cada prueba tiene su base y un reloj fijo."),
    ]
    for i, (nombre, detalle) in enumerate(hechos):
        y = Inches(2.45 + i * 1.15)
        texto(arquitectura, Inches(0.7), y, Inches(4.4), Inches(0.9), [(nombre, 20, NAVY, True, 0)], ancla="ctr")
        texto(arquitectura, Inches(5.3), y, Inches(7.3), Inches(0.9), [(detalle, 18, INK, False, 0)], ancla="ctr")
    notas(arquitectura, "Para la demo: uvicorn reservas.main:app --app-dir src. Cuentas ana, luis y rosa, clave igual al nombre.")

    pruebas = nueva(prs, oscura=True)
    texto(pruebas, Inches(0.7), Inches(0.5), Inches(8), Inches(0.3), [("PRUEBAS", 13, ORANGE, True, 0)])
    texto(pruebas, Inches(0.7), Inches(1.0), Inches(11), Inches(0.8), [("Lo que el enunciado obliga a demostrar", 32, WHITE, True, 0)])
    cifras = [
        ("31", "pruebas en verde,\nde reglas y de aceptación"),
        ("1", "cupo confirmado\nsi dos reservan a la vez"),
        ("CA-02", "los 3 minutos se ven\nen la pantalla, no en un timer"),
    ]
    for i, (numero, detalle) in enumerate(cifras):
        x = Inches(0.7 + i * 4.15)
        texto(pruebas, x, Inches(2.6), Inches(3.8), Inches(1.2), [(numero, 48, ORANGE if i == 1 else WHITE, True, 0)])
        texto(pruebas, x, Inches(4.15), Inches(3.8), Inches(1.3), [(detalle, 18, RGBColor(0xD7, 0xDE, 0xE8), False, 0)])
    texto(
        pruebas,
        Inches(0.7),
        Inches(6.0),
        Inches(12),
        Inches(0.8),
        [("También: antelación, cancelación, no-show, mantenimiento, desplazamiento y el tope semanal.", 16, RGBColor(0x9A, 0xA6, 0xB8), False, 0)],
    )
    notas(pruebas, "La prueba obligatoria es tests/test_no_doble_reserva.py. De dos hilos, uno recibe 201 y el otro RN-08.")

    cambio = nueva(prs)
    kicker(cambio, "Cambio a mitad del desarrollo")
    titulo(cambio, "Un estudiante, máximo dos reservas\nconfirmadas en la semana")
    cadena = [
        ("1", "Pedido", "Issue #11"),
        ("2", "Spec", "RF-14 y RN-25"),
        ("3", "Criterio", "CA-24 a CA-28"),
        ("4", "Código", "Antes de ocupar el cupo"),
        ("5", "Prueba", "En verde, PR #12"),
    ]
    for i, (numero, nombre, detalle) in enumerate(cadena):
        x = Inches(0.45 + i * 2.56)
        ronda(cambio, x, Inches(3.25), Inches(2.4), Inches(2.35), NAVY if i == 4 else WHITE)
        texto(cambio, x + Inches(0.18), Inches(3.4), Inches(2.05), Inches(0.4), [(numero, 20, ORANGE, True, 0)])
        texto(cambio, x + Inches(0.18), Inches(3.9), Inches(2.05), Inches(0.4), [(nombre, 18, WHITE if i == 4 else NAVY, True, 0)])
        texto(cambio, x + Inches(0.18), Inches(4.45), Inches(2.05), Inches(0.8), [(detalle, 14, RGBColor(0xD7, 0xDE, 0xE8) if i == 4 else MUTED, False, 0)])
    texto(
        cambio,
        Inches(0.62),
        Inches(6.0),
        Inches(12),
        Inches(0.8),
        [("La semana es de lunes a domingo. El docente no tiene ese tope. Cancelar libera el conteo.", 18, INK, False, 0)],
    )
    notas(cambio, "El PDF pide mostrar el ciclo completo: cambio, especificación, criterios, plan, código, pruebas y resultado. Este es ese ejemplo.")

    vivo = nueva(prs)
    kicker(vivo, "Durante la presentación")
    titulo(vivo, "Si piden un cambio, se recorre\nel mismo ciclo")
    pasos = [
        ("Anotar el cambio", "No se implementa de memoria."),
        ("Actualizar la regla y el criterio", "Primero specs/, después el código."),
        ("Cambiar código y prueba", "La pantalla no guarda una regla distinta."),
        ("Mostrar el resultado", "La prueba nueva, en verde."),
    ]
    for i, (nombre, detalle) in enumerate(pasos):
        col, fila = i % 2, i // 2
        x = Inches(0.55 + col * 6.4)
        y = Inches(3.15 + fila * 1.85)
        ronda(vivo, x, y, Inches(6.15), Inches(1.65), WHITE)
        texto(vivo, x + Inches(0.3), y + Inches(0.22), Inches(0.6), Inches(0.45), [(str(i + 1), 22, ORANGE, True, 0)])
        texto(vivo, x + Inches(1.0), y + Inches(0.22), Inches(4.8), Inches(0.45), [(nombre, 20, NAVY, True, 0)])
        texto(vivo, x + Inches(1.0), y + Inches(0.8), Inches(4.8), Inches(0.55), [(detalle, 16, MUTED, False, 0)])
    notas(vivo, "El enunciado dice que hay que estar listos para una petición en la sustentación. Ejemplo concreto: cambiar el 2 del tope semanal toca RN-25, CA-24 y tests/test_tope_semanal.py.")

    cierre = nueva(prs, oscura=True)
    barra(cierre)
    texto(cierre, Inches(0.7), Inches(0.65), Inches(12), Inches(1.6), [("Demo, evidencia y preguntas", 36, WHITE, True, 0)])
    bloques = [
        ("Demo", "Ana entra, elige el día y confirma de 1 a 3 bloques."),
        ("Evidencia", "specs/, tests/, docs/ai-log.md, issues y pull requests."),
        ("Roles", "Producto, arquitectura y QA rotan. Cualquiera puede presentar."),
    ]
    for i, (etiqueta, detalle) in enumerate(bloques):
        x = Inches(0.7 + i * 4.1)
        linea = cierre.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, Inches(2.9), Inches(1.15), Inches(0.045))
        linea.fill.solid()
        linea.fill.fore_color.rgb = ORANGE
        linea.line.fill.background()
        texto(cierre, x, Inches(3.15), Inches(3.7), Inches(0.4), [(etiqueta, 18, ORANGE, True, 0)])
        texto(cierre, x, Inches(3.7), Inches(3.7), Inches(1.3), [(detalle, 16, RGBColor(0xD7, 0xDE, 0xE8), False, 0)])
    texto(cierre, Inches(0.7), Inches(5.6), Inches(11), Inches(0.8), [("ana@lab.test / ana     luis@lab.test / luis     rosa@lab.test / rosa", 16, WHITE, False, 6)])
    texto(cierre, Inches(0.7), Inches(6.45), Inches(4), Inches(0.4), [("¿Preguntas?", 18, RGBColor(0x9A, 0xA6, 0xB8), False, 0)])
    notas(cierre, "Si preguntan por la IA, abrir docs/ai-log.md: solicitud, resultado y decisión. No recitar la herramienta.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SALIDA)
    print(SALIDA)


if __name__ == "__main__":
    construir()


