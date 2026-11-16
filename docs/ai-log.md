# AI Development Log

Registro pedido por el proyecto: actividad, IA utilizada, solicitud, resultado y decisión.

## 2026-11-16 — Fase 1, revisión del outcome

| Campo | Contenido |
|---|---|
| Actividad | Contrastar `outcomes.md` con el PDF del Proyecto 2. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | Revisar las instrucciones del PDF y decir si el outcome servía o había que descartarlo. |
| Resultado | El outcome cubre problema, usuarios, resultado, preguntas, reglas, métricas y supuestos de la Fase 1. No se descartó. |
| Decisión | Conservarlo y usarlo como entrada de la Fase 2. Pasarlo a `specs/outcomes.md`. |

## 2026-11-16 — Fase 2, especificaciones SDD

| Campo | Contenido |
|---|---|
| Actividad | Escribir requisitos, reglas, arquitectura, modelo, API, criterios de aceptación y plan. Abrir los issues de implementación. Capturar los documentos. |
| IA utilizada | Cursor, agente CLI Grok 4.7. Capturas con Firefox en modo headless sobre HTML generado desde los Markdown. |
| Solicitud | Proseguir con la Fase 2 y tomar capturas. |
| Resultado | Quedaron `specs/requirements.md`, `specs/business-rules.md`, `specs/architecture.md`, `specs/data-model.md`, `specs/api.md`, `specs/acceptance-criteria.md`, `specs/implementation-plan.md`, `docs/decisions.md`, `docs/testing.md` y `docs/ai-log.md`. En GitHub se abrieron los issues 1 a 9, uno por fila del plan. El tablero Projects no se creó: el token de `gh` no tiene el alcance `project`. |
| Decisión | Stack Python, FastAPI y SQLite (ADR-001). Bloque de 50 minutos y jornada 07:00–21:00 (ADR-002). El correo no bloquea el desplazamiento (ADR-003). Las capturas documentan artefactos e issues, y el uso de IA queda en este archivo (ADR-004). |

Supuestos que la Fase 1 dejaba abiertos y esta sesión cerró en la especificación: duración exacta del bloque, horario de la jornada, significado de "un día" y de "sin límite de tiempo", y qué hacer si no hay otro laboratorio para el estudiante desplazado.

## 2026-11-16 — Implementación del plan

| Campo | Contenido |
|---|---|
| Actividad | Implementar el esquema, las reglas, la API, las pantallas y las pruebas CA-01 a CA-23. Intentar crear el tablero de Projects. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | Proseguir, con el acceso a Projects ya renovado. |
| Resultado | Aplicación en `src/reservas` y 26 pruebas en verde, incluida la de no doble reserva concurrente. La jornada quedó en 07:00–20:20 porque 16 bloques de 50 minutos no llegan a las 21:00. `gh auth status` sigue mostrando un token sin el alcance `project` (`repo`, `gist`, `read:org`, `admin:public_key`), así que el tablero no se creó. |
| Decisión | Seguir con los issues como tablero de trabajo hasta que el token de `gh` incluya `project`. El fallo de correo no revierte un desplazamiento. |

## 2026-11-16 — Cambio de requisito: tope semanal del estudiante

| Campo | Contenido |
|---|---|
| Actividad | Recorrer un cambio de especificación: regla, criterios, plan, código y pruebas. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | Proseguir con la siguiente fase. |
| Resultado | RN-25 y RF-14: un estudiante tiene como máximo 2 reservas confirmadas de lunes a domingo. CA-24 a CA-28 cubren el rechazo, la liberación al cancelar, la excepción del docente, la semana siguiente y la reserva presencial. |
| Decisión | El tope no se aplica al docente (ADR-005). La semana se cuenta de lunes a domingo porque el calendario institucional no definió otro corte. |

## 2026-11-16 — Presentación

| Campo | Contenido |
|---|---|
| Actividad | Armar el material para presentar el proyecto en LibreOffice Impress. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | Seguir con la siguiente fase. |
| Resultado | `docs/presentacion/reservas-laboratorios.pptx` y el mismo archivo en `.odp`. Doce diapositivas: problema, resultado, usuarios, recorrido, reglas, el tope semanal, pruebas, proceso y qué hacer si piden un cambio en vivo. Cada diapositiva tiene notas para quien presente. |
| Decisión | La presentación abre con el resultado para el usuario. La tecnología aparece después, como el medio que impide el cruce de horario. |

## 2026-11-16 — Presentación con la plantilla de CitaFácil

| Campo | Contenido |
|---|---|
| Actividad | Rehacer la presentación usando el diseño de `CitaFácil — Sprint HU-1 a HU-6.pdf`. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | Usar ese archivo como plantilla e incluir el contenido de reservas de laboratorios. |
| Resultado | `docs/presentacion/reservas-laboratorios.pptx` y `.odp` quedan con el azul, el crema y el naranja de esa plantilla. El contenido es el de este proyecto: reglas, pruebas, tope semanal y el ciclo si piden un cambio. |
| Decisión | No se reutilizó el diseño anterior. Los nombres de la portada son los del mismo grupo, tal como están en la plantilla. |

## 2026-11-16 — La presentación sigue el PDF, no la historia de CitaFácil

| Campo | Contenido |
|---|---|
| Actividad | Reescribir el relato de las diapositivas. |
| IA utilizada | Cursor, agente CLI Grok 4.7. |
| Solicitud | No copiar la plantilla. Tomarla como ejemplo visual y seguir lo que el PDF pide en la presentación. |
| Resultado | Diez diapositivas: problema y resultado (ODD), especificación (SDD), código, pruebas, el cambio de mitad y el ciclo si piden otro cambio en la sustentación. El color sigue siendo el de la plantilla. |
| Decisión | No se trasladan historias de usuario, bugs de QA ni las diez restricciones del proyecto 1. Esos puntos no están en el enunciado de este proyecto. |

## 2026-11-16 — Presentación para leer en voz alta

| Campo | Contenido |
|---|---|
| Actividad | Rehacer la presentación para que se pueda explicar el proyecto leyendo las diapositivas. |
| IA utilizada | Cursor, agente CLI Grok 4.7, y la skill pptx de Anthropic con pptxgenjs. |
| Solicitud | Olvidar el diseño de CitaFácil, detallar el contenido y usar esa skill. |
| Resultado | Veinte diapositivas en `docs/presentacion/reservas-laboratorios.pptx` y el mismo archivo en `.odp`. Recorren el problema, las métricas, los tres usuarios, la especificación, el calendario, el cupo, la cancelación, el desplazamiento, la arquitectura, la demostración, las 31 pruebas, el tope semanal, el cambio en sala y dónde está la evidencia. Cada diapositiva tiene notas. |
| Decisión | El tema visual es propio del laboratorio (verde). No se reutiliza el naranja ni el azul de CitaFácil. El generador queda en `docs/presentacion/build-pptx.js`. |

## 2026-11-16 — Presentación con diseño propio

| Campo | Contenido |
|---|---|
| Actividad | Rehacer la presentación sin la skill de diapositivas, con un diseño propio y el mismo relato del proyecto. |
| IA utilizada | Cursor, agente CLI Grok 4.7, con pptxgenjs. |
| Solicitud | No usar la skill. Hacerla según criterio propio, con un diseño actual y bastante informativo. |
| Resultado | Diecisiete diapositivas en `docs/presentacion/reservas-laboratorios.pptx` y el mismo archivo en `.odp`. Recorren problema, métricas, usuarios, especificación, calendario, cupo, cancelación, desplazamiento, sistema, demostración, pruebas, tope semanal, cambio en sala y evidencias. Cada diapositiva tiene notas. |
| Decisión | Fondo claro, barra oscura y un solo acento. El texto se puede leer en voz alta. No se sigue la plantilla de CitaFácil ni el tema verde de la versión anterior. |

## 2026-11-16 — Dos pasadas de revisión del diseño

| Campo | Contenido |
|---|---|
| Actividad | Revisar la presentación con tres agentes y aplicar lo que coincidía. |
| IA utilizada | Cursor, agente CLI Grok 4.7, y tres revisores en paralelo (jerarquía, geometría del lienzo, tipo y contraste), cada uno en dos pasadas. |
| Solicitud | Varias pasadas con varios agentes, contra patrones de diseño de un lienzo de diapositivas. |
| Resultado | Se quitó el muro de tarjetas iguales, el cuerpo pasó a tinta oscura, los títulos de contenido a 36 pt y el margen de texto a 0.5 in. El rojo queda en el rótulo de sección, en «Queda deshabilitado» y en el ejemplo de los bloques 4 a 6. La segunda pasada no dejó defectos altos. |
| Decisión | Se puede presentar esta versión. Los archivos siguen en `docs/presentacion/reservas-laboratorios.pptx` y `.odp`. |
