# Reservas de laboratorios

Sistema para que docentes y estudiantes vean qué laboratorios están libres y reserven sin ir al laboratorio. El administrador registra lo presencial, el mantenimiento y la liberación de franjas deshabilitadas.

Proyecto 2 · Tópicos Especiales II · Desarrollo orientado por resultados y por especificaciones.

## Resultado

Docentes y estudiantes consultan la disponibilidad real y reservan en el sistema. El sistema no confirma dos reservas del mismo laboratorio a la misma hora. El docente puede desplazar la reserva de un estudiante; el estudiante recibe el aviso y la oferta de otro laboratorio.

El detalle del problema, las métricas y los supuestos está en [specs/outcomes.md](specs/outcomes.md).

## Especificaciones

| Documento | Contenido |
|---|---|
| [specs/outcomes.md](specs/outcomes.md) | Problema y resultado (Fase 1, ODD). |
| [specs/requirements.md](specs/requirements.md) | Requisitos funcionales y no funcionales. |
| [specs/business-rules.md](specs/business-rules.md) | Reglas RN-01 a RN-24. |
| [specs/architecture.md](specs/architecture.md) | Python 3.12, FastAPI, SQLite, pytest. |
| [specs/data-model.md](specs/data-model.md) | Tablas y ocupación. |
| [specs/api.md](specs/api.md) | Rutas JSON y páginas. |
| [specs/acceptance-criteria.md](specs/acceptance-criteria.md) | Criterios CA-01 a CA-23. |
| [specs/implementation-plan.md](specs/implementation-plan.md) | Orden de construcción y ramas. |

## Proceso

| Documento | Contenido |
|---|---|
| [docs/ai-log.md](docs/ai-log.md) | Uso de IA: solicitud, resultado y decisión. |
| [docs/decisions.md](docs/decisions.md) | Decisiones de stack, horario y notificaciones. |
| [docs/testing.md](docs/testing.md) | Pruebas previstas, incluida la de no doble reserva. |

## Ejecutar

```bash
python -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest
.venv/bin/uvicorn reservas.main:app --app-dir src
```

Cuentas de demostración: `ana@lab.test`, `luis@lab.test` y `rosa@lab.test`. La clave es `ana`, `luis` o `rosa`.

## Issues

El trabajo de implementación está en los issues del repositorio [Chrisvlj/prj2-reservas](https://github.com/Chrisvlj/prj2-reservas). Cada issue corresponde a una fila del plan.
