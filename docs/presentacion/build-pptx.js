const pptxgen = require("pptxgenjs");

const F = "Calibri";
const INK = "14181F";
const PAPER = "F4F2ED";
const MUTED = "3A424C";
const LINE = "D9D4CB";
const NIGHT = "12161C";
const SIGNAL = "E23D2B";

const L = 0.55;
const R = 12.83;
const W = R - L;

const OUT = "/home/macris209/prj2-reservas/docs/presentacion/reservas-laboratorios.pptx";

async function main() {
  const pres = new pptxgen();
  pres.defineLayout({ name: "WIDE", width: 13.333, height: 7.5 });
  pres.layout = "WIDE";
  pres.title = "Reservas de laboratorios";
  pres.subject = "Proyecto 2. Topicos Especiales II";
  pres.author = "Jorge de Leon, Christian Valdespino, Eriel Tensu";
  pres.company = "Topicos Especiales II";

  let n = 0;

  function hoja(fondo) {
    n += 1;
    const s = pres.addSlide();
    s.background = { color: fondo || PAPER };
    return s;
  }

  function notas(s, texto) {
    s.addNotes(texto);
  }

  function pie(s, oscuro) {
    const color = oscuro ? "C9D0D6" : MUTED;
    s.addText("Reservas de laboratorios", {
      x: L, y: 6.82, w: 7, h: 0.22,
      fontFace: F, fontSize: 13, color, margin: 0,
    });
    s.addText(String(n).padStart(2, "0"), {
      x: R - 1.1, y: 6.82, w: 1.1, h: 0.22,
      fontFace: F, fontSize: 13, color, align: "right", margin: 0,
    });
  }

  function marco(s) {
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.1, h: 7.5, fill: { color: NIGHT },
    });
  }

  function titulo(s, kicker, texto) {
    marco(s);
    s.addText(kicker, {
      x: L, y: 0.5, w: W, h: 0.24,
      fontFace: F, fontSize: 12, bold: true, color: SIGNAL, margin: 0, charSpacing: 1.1,
    });
    s.addText(texto, {
      x: L - 0.02, y: 0.78, w: W, h: 0.95,
      fontFace: F, fontSize: 36, bold: true, color: INK, margin: 0, valign: "top",
    });
  }

  function linea(s, x, y, w) {
    s.addShape(pres.shapes.RECTANGLE, {
      x, y, w, h: 0.015, fill: { color: LINE },
    });
  }

  // 1. Portada
  {
    const s = hoja(NIGHT);
    s.addShape(pres.shapes.RECTANGLE, {
      x: 0, y: 0, w: 0.18, h: 7.5, fill: { color: SIGNAL },
    });
    s.addText("PROYECTO 2  ·  TÓPICOS ESPECIALES II", {
      x: 0.7, y: 1.45, w: 11, h: 0.3,
      fontFace: F, fontSize: 13, bold: true, color: SIGNAL, margin: 0, charSpacing: 1.4,
    });
    s.addText("Reservas de\nlaboratorios", {
      x: 0.68, y: 1.9, w: 11, h: 2.15,
      fontFace: F, fontSize: 54, bold: true, color: "FFFFFF", margin: 0,
    });
    s.addText("Quien ya tiene sesión ve el horario y confirma.\nEl sistema escribe una sola reserva por cupo.", {
      x: 0.7, y: 4.3, w: 10.5, h: 0.85,
      fontFace: F, fontSize: 20, color: "E6EAED", margin: 0,
    });
    s.addText("Jorge de Leon    Christian Valdespino    Eriel Tensu", {
      x: 0.7, y: 5.55, w: 10.5, h: 0.4,
      fontFace: F, fontSize: 16, color: "C9D0D6", margin: 0,
    });
    pie(s, true);
    notas(s, "Leer el subtítulo y los nombres del grupo.");
  }

  // 2. Mapa — fila abierta, sin tarjetas altas
  {
    const s = hoja();
    titulo(s, "CÓMO SE CUENTA", "Cinco partes, en este orden");
    const partes = [
      ["01", "Problema", "Hoy hay que ir al laboratorio para saber si está libre, y aun así se cruzan los horarios."],
      ["02", "Resultado", "Reservar desde la sesión, en menos de tres minutos, sin dos personas en el mismo cupo."],
      ["03", "Reglas", "Lo escrito antes del código: calendario, cupo, cancelación y prioridad del docente."],
      ["04", "Sistema", "Una aplicación, una base y el mismo criterio en la pantalla y en la prueba."],
      ["05", "Prueba", "31 pruebas en verde y el tope de dos reservas confirmadas por semana."],
    ];
    const gap = 0.32;
    const cw = (W - gap * 4) / 5;
    partes.forEach((p, i) => {
      const x = L + i * (cw + gap);
      s.addText(p[0], {
        x, y: 2.15, w: cw, h: 0.4,
        fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
      });
      s.addText(p[1], {
        x, y: 2.58, w: cw, h: 0.42,
        fontFace: F, fontSize: 20, bold: true, color: INK, margin: 0,
      });
      s.addText(p[2], {
        x, y: 3.08, w: cw, h: 2.2,
        fontFace: F, fontSize: 15, color: INK, margin: 0, valign: "top",
      });
    });
    pie(s);
    notas(s, "Si el tiempo aprieta, ir a resultado, cupo y el cambio de mitad.");
  }

  // 3. Problema — dos columnas abiertas
  {
    const s = hoja();
    titulo(s, "EL PROBLEMA", "Hoy hay que ir para saber si hay cupo");
    const col = (W - 0.45) / 2;
    s.addText("Lo que ocurre", {
      x: L, y: 2.05, w: col, h: 0.4,
      fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
    });
    s.addText("Lo que cuesta", {
      x: L + col + 0.45, y: 2.05, w: col, h: 0.4,
      fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
    });
    linea(s, L, 2.52, col);
    linea(s, L + col + 0.45, 2.52, col);
    const izquierda = [
      "Docentes y estudiantes reservan el laboratorio en físico.",
      "No hay una consulta previa del horario.",
      "Para saber si está libre tienen que ir, y muchas veces ya está ocupado.",
      "Por eso reservan con mucha antelación, por si acaso.",
    ];
    izquierda.forEach((t, i) => {
      const y = 2.75 + i * 0.85;
      s.addText(String(i + 1).padStart(2, "0"), {
        x: L, y, w: 0.55, h: 0.7,
        fontFace: F, fontSize: 15, bold: true, color: INK, margin: 0,
      });
      s.addText(t, {
        x: L + 0.6, y, w: col - 0.7, h: 0.75,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    const derecha = [
      ["Desplazamiento inútil.", 22],
      ["Cruces de horario entre quienes creían tener el laboratorio.", 16],
      ["Laboratorios mal aprovechados: ocupados de más en unos horarios y vacíos en otros.", 16],
    ];
    derecha.forEach((t, i) => {
      const y = 2.75 + i * 1.1;
      s.addText(t[0], {
        x: L + col + 0.45, y, w: col, h: 0.95,
        fontFace: F, fontSize: t[1], bold: i === 0, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Primero el resultado para quien reserva. La tecnología viene después.");
  }

  // 4. Métricas — cifras arriba, texto pegado, sin caja alta
  {
    const s = hoja();
    titulo(s, "EL RESULTADO", "Reservar sin desplazarse");
    const metas = [
      ["< 4", "Cruces por semana", "El sistema se diseña para que no haya dos reservas\ndel mismo laboratorio a la misma hora.\nEl 4 no es la meta: es el margen si el sistema fallara."],
      ["< 3 min", "Desde la sesión", "Quien ya tiene sesión elige la fecha, ve los bloques y confirma.\nEn ese camino no hay un paso presencial."],
      ["40 → 70 %", "Ocupación", "Es una meta realista de uso.\nEl sistema no inventa reservas para hacer subir el porcentaje."],
    ];
    const gap = 0.36;
    const cw = (W - gap * 2) / 3;
    metas.forEach((m, i) => {
      const x = L + i * (cw + gap);
      s.addText(m[0], {
        x, y: 2.1, w: cw, h: 0.7,
        fontFace: F, fontSize: 32, bold: true, color: INK, margin: 0,
      });
      s.addText(m[1], {
        x, y: 2.82, w: cw, h: 0.36,
        fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
      });
      s.addText(m[2], {
        x, y: 3.22, w: cw, h: 2.2,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Insistir en que cero cruces es el diseño y cuatro es tolerancia.");
  }

  // 5. Personas — filas abiertas
  {
    const s = hoja();
    titulo(s, "QUIÉN LO USA", "Tres personas, tres necesidades");
    const gente = [
      ["Estudiante", "Ana", "Consulta la disponibilidad y reserva para una clase o un uso personal. No tiene prioridad sobre nadie.\nEn una semana, de lunes a domingo, puede tener como máximo dos reservas confirmadas."],
      ["Docente", "Luis", "Reserva igual que el estudiante y no tiene tope semanal.\nSi necesita un horario ya tomado por un estudiante, puede desplazarlo. No puede desplazar a otro docente."],
      ["Administrador", "Rosa", "Anota la reserva presencial, bloquea por mantenimiento\ny es la única persona que vuelve a liberar un horario deshabilitado."],
    ];
    gente.forEach((g, i) => {
      const y = 2.05 + i * 1.45;
      if (i > 0) linea(s, L, y - 0.16, W);
      s.addText(g[0], {
        x: L, y, w: 3.1, h: 0.42,
        fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0,
      });
      s.addText(g[1], {
        x: L, y: y + 0.46, w: 3.1, h: 0.4,
        fontFace: F, fontSize: 16, color: MUTED, margin: 0,
      });
      s.addText(g[2], {
        x: L + 3.4, y, w: W - 3.4, h: 1.15,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Una cuenta tiene un solo rol. Entre dos docentes gana quien reservó primero.");
  }

  // 6. Spec — lista, un archivo más grande
  {
    const s = hoja();
    titulo(s, "ANTES DEL CÓDIGO", "Nada se programó hasta dejarlo escrito");
    s.addText("specs/business-rules.md", {
      x: L, y: 2.05, w: W, h: 0.4,
      fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0,
    });
    s.addText("Las reglas RN-01 a RN-25. Cada una se puede aprobar o rechazar. El resto de los archivos sostiene esa lista.", {
      x: L, y: 2.5, w: W, h: 0.45,
      fontFace: F, fontSize: 16, color: INK, margin: 0,
    });
    const docs = [
      ["specs/outcomes.md", "El problema, los tres usuarios, el resultado y las tres métricas."],
      ["specs/acceptance-criteria.md", "CA-01 a CA-28, con un reloj fijo\npara no depender de la hora real."],
      ["specs/architecture.md", "Python, FastAPI, SQLite y pytest."],
      ["specs/api.md", "Las mismas operaciones de la pantalla, también en JSON."],
    ];
    docs.forEach((d, i) => {
      const col = i < 2 ? 0 : 1;
      const fila = i % 2;
      const x = L + col * ((W + 0.4) / 2);
      const y = 3.2 + fila * 1.15;
      const ww = (W - 0.4) / 2;
      s.addText(d[0], {
        x, y, w: ww, h: 0.32,
        fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
      });
      s.addText(d[1], {
        x, y: y + 0.34, w: ww, h: 0.6,
        fontFace: F, fontSize: 15, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Si piden un archivo, abrirlo. El que más se cita es business-rules.md.");
  }

  // 7. Calendario — la franja manda, los datos van sueltos
  {
    const s = hoja();
    titulo(s, "EL CALENDARIO", "16 bloques de 50 minutos");
    const hueco = 0.06;
    const ancho = (W - hueco * 15) / 16;
    for (let i = 0; i < 16; i++) {
      const reserva = i >= 3 && i <= 5;
      const x = L + i * (ancho + hueco);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, {
        x, y: 2.05, w: ancho, h: 0.62,
        fill: { color: reserva ? "FFFFFF" : NIGHT },
        line: reserva ? { color: SIGNAL, width: 1.5 } : undefined,
        rectRadius: 0.04,
      });
      s.addText(String(i + 1), {
        x, y: 2.05, w: ancho, h: 0.62,
        fontFace: F, fontSize: 13, bold: true, color: reserva ? SIGNAL : "FFFFFF",
        align: "center", valign: "middle", margin: 0,
      });
    }
    s.addText("07:00", {
      x: L, y: 2.76, w: 1.4, h: 0.28,
      fontFace: F, fontSize: 14, color: INK, margin: 0,
    });
    s.addText("20:20", {
      x: R - 1.4, y: 2.76, w: 1.4, h: 0.28,
      fontFace: F, fontSize: 14, color: INK, align: "right", margin: 0,
    });
    s.addText("Los bloques 4, 5 y 6, marcados, son un ejemplo de una sola reserva.", {
      x: L, y: 3.1, w: W, h: 0.32,
      fontFace: F, fontSize: 16, color: INK, margin: 0,
    });
    const datos = [
      ["50 min", "Cada bloque son 45 minutos de uso y 5 de transición.\nLa transición no se reserva aparte."],
      ["1 a 3", "Bloques seguidos, el mismo día y el mismo laboratorio.\nCuatro bloques se rechazan con RN-02."],
      ["20:20", "El bloque 1 empieza a las 07:00.\nDieciséis bloques terminan a las 20:20, no a las 21:00."],
      ["60 min", "En línea hace falta al menos una hora de antelación.\nCon menos, solo el administrador registra la presencial."],
    ];
    datos.forEach((d, i) => {
      const col = i % 2;
      const fila = Math.floor(i / 2);
      const x = L + col * (W / 2 + 0.1);
      const y = 3.6 + fila * 1.35;
      s.addText(d[0], {
        x, y, w: W / 2 - 0.3, h: 0.36,
        fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
      });
      s.addText(d[1], {
        x, y: y + 0.38, w: W / 2 - 0.3, h: 0.8,
        fontFace: F, fontSize: 15, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Si preguntan por las 21:00: 16 por 50 minutos no llegan. La decisión está en ADR-002.");
  }

  // 8. Cupo — separadores, el nombre de la regla manda
  {
    const s = hoja();
    titulo(s, "EL CUPO", "Una sola reserva queda escrita");
    const reglas = [
      ["RN-08", "El laboratorio", "No puede haber dos reservas confirmadas del mismo laboratorio, la misma fecha y el mismo bloque. Quien queda escrito primero se queda el cupo.\nLa otra petición se rechaza."],
      ["RN-07", "La persona", "La misma persona no puede tener dos reservas confirmadas que se solapen, aunque sean laboratorios distintos."],
      ["RN-09", "A la vez", "Si dos personas confirman el mismo cupo al mismo tiempo, la transacción deja una sola reserva.\nLa prueba lanza las dos juntas."],
    ];
    reglas.forEach((r, i) => {
      const y = 2.05 + i * 1.45;
      if (i > 0) linea(s, L, y - 0.14, W);
      s.addText(r[0], {
        x: L, y, w: 1.6, h: 0.36,
        fontFace: F, fontSize: 14, color: MUTED, margin: 0,
      });
      s.addText(r[1], {
        x: L + 1.7, y, w: W - 1.7, h: 0.4,
        fontFace: F, fontSize: 20, bold: true, color: INK, margin: 0,
      });
      s.addText(r[2], {
        x: L + 1.7, y: y + 0.42, w: W - 1.7, h: 0.8,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "El test se llama test_ca08. El orden es rol, rango, antelación, bloque deshabilitado, solape de la persona, tope semanal y al final el cupo del laboratorio.");
  }

  // 9. Cancelar — dos grupos, no cuatro cajas
  {
    const s = hoja();
    titulo(s, "CANCELAR", "Llegar tarde no devuelve el horario");
    const col = (W - 0.5) / 2;
    s.addText("Vuelve a quedar libre", {
      x: L, y: 2.1, w: col, h: 0.5,
      fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0,
    });
    s.addText("24 horas o más", {
      x: L, y: 2.7, w: col, h: 0.35,
      fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
    });
    s.addText("La reserva pasa a cancelada y los bloques vuelven a quedar libres. El estudiante puede usar ese cupo en otra reserva de la semana.", {
      x: L, y: 3.15, w: col, h: 1.3,
      fontFace: F, fontSize: 16, color: INK, margin: 0,
    });
    s.addText("Queda deshabilitado", {
      x: L + col + 0.5, y: 2.1, w: col, h: 0.5,
      fontFace: F, fontSize: 22, bold: true, color: SIGNAL, margin: 0,
    });
    const off = [
      ["Menos de 24 horas", "Los bloques quedan deshabilitados. Nadie más los reserva en línea."],
      ["No asistir", "El administrador marca no-show. El efecto es el mismo."],
      ["Liberar", "Solo el administrador, tras una solicitud presencial, lo pasa otra vez a libre."],
    ];
    off.forEach((f, i) => {
      const y = 2.75 + i * 1.1;
      s.addText(f[0], {
        x: L + col + 0.5, y, w: col, h: 0.32,
        fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
      });
      s.addText(f[1], {
        x: L + col + 0.5, y: y + 0.34, w: col, h: 0.65,
        fontFace: F, fontSize: 15, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "El mantenimiento es aparte: el administrador bloquea bloques libres y, al cerrarlo, vuelven a libres. No puede tapar una reserva sin cancelarla antes.");
  }

  // 10. Docente
  {
    const s = hoja();
    titulo(s, "PRIORIDAD", "El docente toma el horario del estudiante");
    const pasos = [
      ["1", "Sin la hora previa", "No se le exige la hora de antelación.\nNo puede tomar un bloque que ya terminó, ni desplazar a otro docente."],
      ["2", "La reserva cambia", "La del estudiante pasa a desplazada.\nLos bloques que el docente no usa vuelven a quedar libres."],
      ["3", "El aviso", "Se guardan los otros laboratorios libres en ese horario. Si no hay ninguno, el aviso lo dice.\nNo se crea otra reserva para el estudiante."],
      ["4", "Si el correo falla", "El cambio de reserva igual queda. El aviso queda pendiente o en error.\nEl correo no deshace la reserva."],
    ];
    pasos.forEach((p, i) => {
      const y = 2.0 + i * 1.1;
      s.addText(p[0], {
        x: L, y, w: 0.45, h: 0.95,
        fontFace: F, fontSize: 20, bold: true, color: INK, margin: 0,
      });
      s.addText(p[1], {
        x: L + 0.6, y, w: 3.15, h: 0.95,
        fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
      });
      s.addText(p[2], {
        x: L + 3.9, y, w: W - 3.9, h: 0.95,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Si el docente ya tiene ese horario en otro laboratorio, el desplazamiento se rechaza y el estudiante conserva su reserva.");
  }

  // 11. Sistema
  {
    const s = hoja();
    titulo(s, "EL SISTEMA", "Una aplicación y una sola base");
    const partes = [
      ["Python y FastAPI", "Sirven la página y el JSON. No hay una segunda copia de las reglas en el navegador."],
      ["SQLite", "Un archivo. Crear, cancelar o desplazar ocurre en una transacción,\nasí dos escrituras no confirman el mismo cupo."],
      ["pytest", "Cada prueba arma su base temporal y fija el reloj. Así se puede afirmar «faltan 30 minutos» sin depender de la hora de la máquina."],
    ];
    partes.forEach((p, i) => {
      const y = 2.05 + i * 1.15;
      s.addText(p[0], {
        x: L, y, w: 3.3, h: 0.95,
        fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
      });
      s.addText(p[1], {
        x: L + 3.5, y, w: W - 3.5, h: 0.95,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    linea(s, L, 5.5, W);
    s.addText("Para mostrarlo", {
      x: L, y: 5.65, w: 3.3, h: 0.4,
      fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
    });
    s.addText("uvicorn reservas.main:app --app-dir src\nCuentas ana, luis y rosa. La clave es el nombre en minúsculas.", {
      x: L + 3.5, y: 5.65, w: W - 3.5, h: 0.7,
      fontFace: F, fontSize: 16, color: INK, margin: 0,
    });
    pie(s);
    notas(s, "No defender el framework. Defender que la disponibilidad de la pantalla es la que usa la reserva.");
  }

  // 12. Demo — lista vertical, distinta del mapa
  {
    const s = hoja();
    titulo(s, "LA DEMOSTRACIÓN", "Se dice en cuatro pasos");
    const demo = [
      ["Entrar", "ana@lab.test, clave ana."],
      ["Mirar", "Una fecha con al menos una hora de margen. Comparar Lab 1 y Lab 2."],
      ["Confirmar", "Uno, dos o tres bloques seguidos. La reserva queda confirmada."],
      ["Repetir", "El mismo horario con Luis. El sistema responde RN-08 y no crea otra reserva."],
    ];
    const gap = 0.32;
    const cw = (W - gap * 3) / 4;
    demo.forEach((d, i) => {
      const x = L + i * (cw + gap);
      s.addText(String(i + 1).padStart(2, "0"), {
        x, y: 2.15, w: cw, h: 0.36,
        fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
      });
      s.addText(d[0], {
        x, y: 2.55, w: cw, h: 0.5,
        fontFace: F, fontSize: 22, bold: true, color: INK, margin: 0,
      });
      s.addText(d[1], {
        x, y: 3.15, w: cw, h: 1.8,
        fontFace: F, fontSize: 16, color: INK, margin: 0, valign: "top",
      });
    });
    pie(s);
    notas(s, "Hacerlo en vivo si hay red. Luis es luis@lab.test, clave luis. Rosa es rosa@lab.test, clave rosa. Si no hay red, leer estos pasos y abrir la captura de disponibilidad.");
  }

  // 13. Pruebas
  {
    const s = hoja();
    titulo(s, "LAS PRUEBAS", "Lo que queda demostrado");
    s.addText("31", {
      x: L, y: 2.05, w: 3.6, h: 1.15,
      fontFace: F, fontSize: 72, bold: true, color: INK, margin: 0,
    });
    s.addText("pruebas en verde", {
      x: L, y: 3.25, w: 3.6, h: 0.4,
      fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
    });
    s.addText("Reglas, aceptación, cancelación, desplazamiento y el tope semanal. Cada una usa su base y un reloj fijo.", {
      x: L, y: 3.72, w: 3.7, h: 1.3,
      fontFace: F, fontSize: 16, color: INK, margin: 0,
    });
    const hechos = [
      ["La obligatoria", "Ana y Luis piden el mismo bloque a la vez. Queda una sola reserva confirmada.\nLa otra recibe RN-08. Está en tests/test_no_doble_reserva.py."],
      ["El reloj", "No se mide con la hora de la máquina. El reloj de prueba dice, por ejemplo, que faltan 30 minutos, y la regla responde RN-05."],
      ["Los tres minutos", "No se miden con un temporizador. Se recorren en la pantalla: ver, elegir,\nconfirmar. Es el criterio CA-02."],
    ];
    hechos.forEach((h, i) => {
      const y = 2.05 + i * 1.4;
      if (i > 0) linea(s, L + 4.15, y - 0.12, W - 4.15);
      s.addText(h[0], {
        x: L + 4.15, y, w: W - 4.15, h: 0.34,
        fontFace: F, fontSize: 16, bold: true, color: INK, margin: 0,
      });
      s.addText(h[1], {
        x: L + 4.15, y: y + 0.36, w: W - 4.15, h: 0.85,
        fontFace: F, fontSize: 15, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "Si piden verla, correr pytest. La de concurrencia usa dos sesiones distintas.");
  }

  // 14. RN-25 — el 2 es la cifra
  {
    const s = hoja();
    titulo(s, "EL CAMBIO DE MITAD", "Tope de dos por semana");
    s.addText("2", {
      x: L, y: 2.05, w: 3.3, h: 1.2,
      fontFace: F, fontSize: 80, bold: true, color: INK, margin: 0,
    });
    s.addText("reservas confirmadas\nde lunes a domingo", {
      x: L, y: 3.3, w: 3.5, h: 0.8,
      fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
    });
    s.addText("La tercera se rechaza con RN-25 y el laboratorio sigue libre. El docente no tiene ese tope.\nSi el estudiante cancela una, puede crear otra.\nLa presencial también cuenta.", {
      x: L, y: 4.25, w: 3.6, h: 1.8,
      fontFace: F, fontSize: 15, color: INK, margin: 0,
    });
    const ciclo = [
      ["Pedido", "Issue 11, cuando el núcleo ya estaba en main."],
      ["Spec", "RF-14, RN-25\ny la decisión ADR-005."],
      ["Criterio", "CA-24 a CA-28. Misma semana y semana siguiente."],
      ["Código", "El conteo ocurre antes de ocupar el cupo. Pull request 12."],
    ];
    ciclo.forEach((c, i) => {
      const y = 2.05 + i * 1.05;
      s.addText(c[0], {
        x: L + 4.15, y, w: 2.2, h: 0.9,
        fontFace: F, fontSize: 18, bold: true, color: INK, margin: 0,
      });
      s.addText(c[1], {
        x: L + 6.4, y, w: W - 6.4, h: 0.9,
        fontFace: F, fontSize: 16, color: INK, margin: 0,
      });
    });
    pie(s);
    notas(s, "La semana empieza el lunes. Una reserva desplazada, cancelada o marcada como no-show no cuenta para el tope.");
  }

  await pres.writeFile({ fileName: OUT });
  console.log(OUT);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
