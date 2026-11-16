"""Genera la presentación del proyecto para LibreOffice Impress."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

ROOT = Path(__file__).resolve().parents[2]
SALIDA = Path(__file__).resolve().parent / "reservas-laboratorios.pptx"
CAPTURA = ROOT / "docs" / "evidencias" / "08-disponibilidad.png"

NAVY = RGBColor(0x16, 0x32, 0x4F)
INK = RGBColor(0x1C, 0x24, 0x30)
MUTED = RGBColor(0x5C, 0x6B, 0x7A)
GREEN = RGBColor(0x1F, 0x7A, 0x4D)
CREAM = RGBColor(0xF4, 0xF6, 0xF8)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
LINE = RGBColor(0xD5, 0xDD, 0xE6)

ANCHO = Inches(13.333)
ALTO = Inches(7.5)


def _run(parrafo, texto, tamano, color, negrita=False):
    run = parrafo.add_run()
    run.text = texto
    run.font.size = Pt(tamano)
    run.font.color.rgb = color
    run.font.bold = negrita
    run.font.name = "Calibri"
    return run


def _caja(slide, izquierda, arriba, ancho, alto, relleno):
    forma = slide.shapes.add_shape(1, izquierda, arriba, ancho, alto)
    forma.shadow.inherit = False
    forma.fill.solid()
    forma.fill.fore_color.rgb = relleno
    forma.line.fill.background()
    forma.text_frame.word_wrap = True
    return forma


def _texto(slide, izquierda, arriba, ancho, alto, lineas, alineacion=PP_ALIGN.LEFT, ancla=MSO_ANCHOR.TOP):
    caja = slide.shapes.add_textbox(izquierda, arriba, ancho, alto)
    marco = caja.text_frame
    marco.word_wrap = True
    marco.auto_size = None
    marco.margin_left = Emu(0)
    marco.margin_right = Emu(0)
    marco.margin_top = Emu(0)
    marco.margin_bottom = Emu(0)
    try:
        marco._txBody.bodyPr.set("anchor", {MSO_ANCHOR.TOP: "t", MSO_ANCHOR.MIDDLE: "ctr", MSO_ANCHOR.BOTTOM: "b"}[ancla])
    except Exception:
        pass
    for indice, (texto, tamano, color, negrita) in enumerate(lineas):
        parrafo = marco.paragraphs[0] if indice == 0 else marco.add_paragraph()
        parrafo.alignment = alineacion
        parrafo.space_after = Pt(6)
        _run(parrafo, texto, tamano, color, negrita)
    return caja


def _notas(slide, texto):
    slide.notes_slide.notes_text_frame.text = texto


def _base(prs, titulo):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    _caja(slide, 0, 0, ANCHO, ALTO, CREAM)
    _caja(slide, 0, 0, ANCHO, Inches(0.12), NAVY)
    _texto(slide, Inches(0.55), Inches(0.32), Inches(12.2), Inches(0.7), [(titulo, 32, NAVY, True)])
    return slide


def _vinetas(slide, items, arriba=Inches(1.35)):
    _texto(
        slide,
        Inches(0.7),
        arriba,
        Inches(11.8),
        Inches(5.6),
        [(f"•  {item}", 22, INK, False) for item in items],
    )


def construir():
    prs = Presentation()
    prs.slide_width = ANCHO
    prs.slide_height = ALTO
    prs.core_properties.title = "Reservas de laboratorios"
    prs.core_properties.subject = "Proyecto 2 · Tópicos Especiales II"

    portada = prs.slides.add_slide(prs.slide_layouts[6])
    _caja(portada, 0, 0, ANCHO, ALTO, NAVY)
    _caja(portada, 0, Inches(5.55), ANCHO, Inches(1.95), RGBColor(0x10, 0x26, 0x3D))
    _texto(
        portada,
        Inches(0.7),
        Inches(1.7),
        Inches(11.5),
        Inches(2.4),
        [
            ("Reservas de laboratorios", 48, WHITE, True),
            ("Ver el horario y reservar sin ir al laboratorio", 24, RGBColor(0xD5, 0xE4, 0xF2), False),
        ],
    )
    _texto(
        portada,
        Inches(0.7),
        Inches(5.9),
        Inches(11.5),
        Inches(1.2),
        [
            ("Proyecto 2  ·  Tópicos Especiales II  ·  Prof. Regis Rivera", 18, WHITE, False),
            ("ODD  →  SDD  →  código  →  pruebas  →  valor para el usuario", 16, RGBColor(0xB7, 0xC9, 0xD9), False),
        ],
    )
    _notas(
        portada,
        "Abrir con el resultado, no con la tecnología. "
        "El sistema existe para que docente y estudiante sepan si hay laboratorio libre y lo reserven sin desplazarse.",
    )

    problema = _base(prs, "Hoy hay que ir a ver si está libre")
    _vinetas(
        problema,
        [
            "La reserva se hace en físico.",
            "Para saber si hay cupo hay que ir al laboratorio.",
            "Muchas veces ya está ocupado, así que se reserva con mucha antelación.",
            "Eso deja viajes inútiles, cruces de horario y laboratorios mal usados.",
        ],
    )
    _notas(problema, "Contar el problema en una frase: se enteran de que no hay cupo cuando ya llegaron.")

    resultado = _base(prs, "El resultado que tiene que ocurrir")
    _texto(
        resultado,
        Inches(0.7),
        Inches(1.3),
        Inches(12),
        Inches(1.1),
        [("Docente y estudiante ven la disponibilidad real y reservan en el sistema.", 22, INK, False)],
    )
    tarjetas = [
        ("Cruces", "Menos de 4 por semana", "El sistema apunta a cero"),
        ("Reservar", "Menos de 3 minutos", "Con la sesión ya iniciada"),
        ("Ocupación", "De 40 % a 70 %", "Meta realista, no un relleno"),
    ]
    for indice, (titulo, valor, detalle) in enumerate(tarjetas):
        izquierda = Inches(0.55 + indice * 4.2)
        tarjeta = _caja(resultado, izquierda, Inches(2.8), Inches(3.9), Inches(3.3), WHITE)
        tarjeta.line.color.rgb = LINE
        _texto(resultado, izquierda + Inches(0.3), Inches(3.05), Inches(3.3), Inches(0.5), [(titulo, 16, MUTED, True)])
        _texto(resultado, izquierda + Inches(0.3), Inches(3.6), Inches(3.3), Inches(1.3), [(valor, 26, NAVY, True)])
        _texto(resultado, izquierda + Inches(0.3), Inches(5.1), Inches(3.3), Inches(0.7), [(detalle, 16, INK, False)])
    _notas(
        resultado,
        "El margen de 4 cruces no es un objetivo. Es tolerancia si el sistema fallara. "
        "La ocupación no se sube inventando reservas.",
    )

    usuarios = _base(prs, "Tres personas, tres necesidades")
    filas = [
        ("Estudiante", "Consulta y reserva para clase o uso personal."),
        ("Docente", "Reserva y, si lo necesita, desplaza la reserva de un estudiante."),
        ("Administrador", "Registra lo presencial, el mantenimiento y libera lo deshabilitado."),
    ]
    for indice, (rol, detalle) in enumerate(filas):
        arriba = Inches(1.45 + indice * 1.7)
        _caja(usuarios, Inches(0.55), arriba, Inches(12.2), Inches(1.5), WHITE).line.color.rgb = LINE
        _caja(usuarios, Inches(0.55), arriba, Inches(0.16), Inches(1.5), GREEN if indice else NAVY)
        _texto(usuarios, Inches(1.0), arriba + Inches(0.22), Inches(11), Inches(0.45), [(rol, 24, NAVY, True)])
        _texto(usuarios, Inches(1.0), arriba + Inches(0.75), Inches(11), Inches(0.5), [(detalle, 18, INK, False)])
    _notas(usuarios, "Una cuenta, un rol. El docente no desplaza a otro docente: entre docentes gana quien reservó primero.")

    pantalla = _base(prs, "Reservar cabe en tres pasos")
    _texto(
        pantalla,
        Inches(0.55),
        Inches(1.2),
        Inches(5.4),
        Inches(5.5),
        [
            ("1.  Elegir la fecha", 22, INK, True),
            ("2.  Ver qué bloques están libres", 22, INK, True),
            ("3.  Confirmar de 1 a 3 bloques", 22, INK, True),
            ("", 12, INK, False),
            ("Cuentas de la demostración", 16, MUTED, True),
            ("ana@lab.test   /   ana", 18, INK, False),
            ("luis@lab.test   /   luis", 18, INK, False),
            ("rosa@lab.test   /   rosa", 18, INK, False),
        ],
    )
    if CAPTURA.exists():
        pantalla.shapes.add_picture(str(CAPTURA), Inches(6.15), Inches(1.35), Inches(6.7), Inches(4.7))
    _notas(pantalla, "Hacer el recorrido en vivo con Ana. No explicar la pantalla antes de mostrarla.")

    reglas = _base(prs, "Lo que el sistema no deja pasar")
    _vinetas(
        reglas,
        [
            "Un bloque dura 50 minutos: 45 de uso y 5 de transición. Máximo 3 bloques.",
            "La jornada va de 07:00 a 20:20.",
            "En línea hace falta al menos una hora de antelación. Con menos, solo presencial.",
            "No hay dos reservas confirmadas del mismo laboratorio a la misma hora.",
            "La misma persona no queda en dos laboratorios a la vez.",
        ],
    )
    _notas(reglas, "Si preguntan por las 21:00: 16 bloques de 50 minutos terminan a las 20:20. Eso está en la decisión ADR-002.")

    despues = _base(prs, "Qué pasa después de reservar")
    _vinetas(
        despues,
        [
            "Cancelar con 24 horas o más deja el bloque libre.",
            "Cancelar con menos de 24 horas, o un no-show, lo deja deshabilitado.",
            "Solo el administrador vuelve a dejar libre un bloque deshabilitado.",
            "El docente puede tomar el horario de un estudiante. Se le avisa y se le nombran otros laboratorios libres.",
            "Si el correo no sale, la reserva igual cambia y el aviso queda guardado.",
        ],
    )
    _notas(despues, "El desplazamiento no exige la hora de antelación. No puede tomar un bloque que ya terminó, ni dejar al docente en dos sitios.")

    cambio = _base(prs, "Cambio a mitad del desarrollo")
    _texto(
        cambio,
        Inches(0.7),
        Inches(1.3),
        Inches(12),
        Inches(1.3),
        [("Un estudiante no puede tener más de 2 reservas confirmadas en la misma semana, de lunes a domingo.", 24, INK, True)],
    )
    _vinetas(
        cambio,
        [
            "La tercera responde RN-25 y el laboratorio sigue libre.",
            "Cancelar una libera el conteo. El docente no tiene ese tope.",
            "La reserva presencial también cuenta para el estudiante.",
            "Quedó en el issue 11, el pull request 12 y cinco pruebas nuevas.",
        ],
        arriba=Inches(2.7),
    )
    _notas(cambio, "Este es el ejemplo del ciclo que pide el curso: primero la especificación, después el código y la prueba.")

    arquitectura = _base(prs, "Una sola verdad del horario")
    _vinetas(
        arquitectura,
        [
            "Python, FastAPI, SQLite y pytest. Una aplicación, sin servicios aparte.",
            "La página y la API pasan por las mismas reglas.",
            "Crear, cancelar o desplazar ocurre en una transacción.",
            "Si dos personas piden el mismo cupo a la vez, solo una queda confirmada.",
            "Para levantarlo: uvicorn reservas.main:app --app-dir src, y abrir el puerto 8000.",
        ],
    )
    _notas(arquitectura, "No defender el framework. Defender que la disponibilidad de la pantalla es la misma que usa la reserva.")

    pruebas = _base(prs, "31 pruebas, una de ellas obligatoria")
    _vinetas(
        pruebas,
        [
            "La prueba obligatoria impide la doble reserva, también cuando dos solicitudes llegan juntas.",
            "El resto cubre antelación, cancelación, no-show, mantenimiento, desplazamiento y el tope semanal.",
            "Los tres minutos de la reserva se demuestran en la pantalla, no con un temporizador.",
            "Cada prueba usa su propia base y un reloj fijo.",
        ],
    )
    _notas(pruebas, "Si piden ver la prueba, abrir tests/test_no_doble_reserva.py y decir que de dos solicitudes simultáneas solo una responde 201.")

    proceso = _base(prs, "El proceso que se evalúa")
    _vinetas(
        proceso,
        [
            "Repositorio Chrisvlj/prj2-reservas, con specs/ y docs/ai-log.md.",
            "Issues, ramas y pull requests. El núcleo entró en el PR 10 y el tope semanal en el PR 12.",
            "El tablero está en el proyecto de GitHub, con las tareas en Done.",
            "El uso de IA está anotado: qué se pidió, qué salió y qué se decidió.",
        ],
    )
    _notas(proceso, "Si preguntan por la IA, abrir docs/ai-log.md. No hace falta recitar la herramienta: hace falta mostrar la decisión.")

    vivo = _base(prs, "Si piden un cambio durante la presentación")
    pasos = [
        ("1", "Anotar el cambio"),
        ("2", "Actualizar la regla y el criterio"),
        ("3", "Cambiar el código"),
        ("4", "Cambiar la prueba y mostrarla en verde"),
    ]
    for indice, (numero, texto) in enumerate(pasos):
        izquierda = Inches(0.5 + indice * 3.2)
        _caja(vivo, izquierda, Inches(1.6), Inches(3.0), Inches(2.5), WHITE).line.color.rgb = LINE
        _texto(vivo, izquierda + Inches(0.2), Inches(1.8), Inches(2.6), Inches(0.7), [(numero, 28, GREEN, True)])
        _texto(vivo, izquierda + Inches(0.2), Inches(2.6), Inches(2.6), Inches(1.2), [(texto, 18, INK, True)])
    _texto(
        vivo,
        Inches(0.55),
        Inches(4.5),
        Inches(12.2),
        Inches(2.2),
        [
            ("Ejemplo ya recorrido: pasar el tope de 2 a otro número toca RN-25,", 20, INK, False),
            ("el criterio CA-24, la constante del código y tests/test_tope_semanal.py.", 20, INK, False),
            ("No se cambia la pantalla por un lado y la regla por otro.", 20, NAVY, True),
        ],
    )
    _notas(vivo, "Ofrecer hacer el cambio en ese orden. Si no da el tiempo, mostrar el diff del tope semanal como evidencia de que el ciclo ya se hizo.")

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    prs.save(SALIDA)
    print(SALIDA)


if __name__ == "__main__":
    construir()
