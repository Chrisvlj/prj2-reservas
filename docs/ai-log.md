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
