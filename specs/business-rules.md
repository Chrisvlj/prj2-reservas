# Reglas de negocio

Cada regla es comprobable. La prueba que la cubre está en `specs/acceptance-criteria.md` y en `docs/testing.md`.

## 1. Calendario

| ID | Regla |
|---|---|
| RN-01 | Cada bloque dura 50 minutos (45 de uso + 5 de transición). Hay 16 bloques, numerados del 1 al 16. El bloque 1 empieza a las 07:00 y el bloque 16 termina a las 20:20. |
| RN-02 | Una reserva cubre de 1 a 3 bloques consecutivos del mismo laboratorio y de la misma fecha. No cruza de un día a otro. |
| RN-03 | El uso efectivo de un bloque son sus primeros 45 minutos. Los 5 minutos finales son transición y no se reservan aparte. |

## 2. Quién puede reservar

| ID | Regla |
|---|---|
| RN-04 | Solo un usuario autenticado con rol estudiante, docente o administrador puede actuar. |
| RN-05 | Estudiante y docente crean reservas en línea solo si el inicio del primer bloque es al menos 60 minutos después del momento de la operación. |
| RN-06 | El administrador puede registrar una reserva presencial con cualquier antelación, incluida menos de 60 minutos, y también sobre un bloque que empieza el mismo día. No puede reservar un bloque ya terminado. |
| RN-07 | Una cuenta no tiene dos reservas en estado `confirmada` cuyos intervalos de tiempo se solapen, en el mismo laboratorio o en otro. |

## 3. Conflicto de cupo

| ID | Regla |
|---|---|
| RN-08 | Como máximo una reserva en estado `confirmada` cubre un par (laboratorio, fecha, bloque). |
| RN-09 | Si dos solicitudes válidas compiten por el mismo cupo, se confirma la que la base de datos persiste primero. La otra se rechaza. No se crea un cruce. |
| RN-10 | No se puede reservar un bloque en estado `deshabilitada` o `mantenimiento`. |
| RN-11 | Reservar bloques libres los pasa a `reservada` y crea la reserva en estado `confirmada`. |

## 4. Prioridad del docente

| ID | Regla |
|---|---|
| RN-12 | Un docente puede desplazar una reserva `confirmada` de un estudiante sobre los bloques que necesita. No aplica la antelación de 60 minutos. |
| RN-13 | El desplazamiento no aplica si el titular es docente o administrador, ni si algún bloque pedido ya terminó. |
| RN-14 | Al desplazar: la reserva del estudiante pasa a `desplazada`; los bloques que el docente toma quedan en una reserva `confirmada` del docente; los bloques del estudiante que el docente no toma vuelven a `libre`. |
| RN-15 | El sistema registra una notificación al estudiante con los otros laboratorios que estén `libre` en esos mismos bloques. Si no hay, la notificación indica que no hay alternativa. No se reserva otro laboratorio sin acción del estudiante. |
| RN-16 | Un docente no puede desplazarse a sí mismo ni usar el desplazamiento para evadir RN-07. Si el docente ya tiene otra reserva solapada, el desplazamiento se rechaza. |

## 5. Cancelación, inasistencia y mantenimiento

| ID | Regla |
|---|---|
| RN-17 | El titular o el administrador pueden cancelar una reserva `confirmada` que aún no ha terminado. |
| RN-18 | Si la cancelación ocurre 24 horas o más antes del inicio, los bloques de esa reserva pasan a `libre`. |
| RN-19 | Si la cancelación ocurre a menos de 24 horas del inicio, los bloques pasan a `deshabilitada`. |
| RN-20 | Un bloque ya iniciado se trata con la regla de menos de 24 horas: cancelarlo lo deja `deshabilitada`. |
| RN-21 | El administrador puede marcar no-show una reserva `confirmada` cuyo inicio ya pasó y que no fue cancelada. Los bloques pasan a `deshabilitada` y la reserva a `no_show`. |
| RN-22 | Solo el administrador pasa un bloque `deshabilitada` a `libre`. |
| RN-23 | El administrador pasa bloques `libre` a `mantenimiento` y, al cerrar el mantenimiento, de `mantenimiento` a `libre`. No pone en mantenimiento un bloque `reservada` sin cancelar o desplazar antes la reserva. |
| RN-24 | Una franja `deshabilitada` o en `mantenimiento` no se ofrece como alternativa en RN-15. |
| RN-25 | Un estudiante puede tener como máximo 2 reservas en estado `confirmada` cuya fecha caiga en la misma semana calendario, de lunes a domingo. La tercera se rechaza. El docente no tiene este tope. Una reserva `cancelada`, `desplazada` o `no_show` no cuenta. La reserva presencial cuenta para el estudiante titular. |

## 6. Estados

Reserva: `confirmada`, `cancelada`, `desplazada`, `no_show`.

Bloque por laboratorio y fecha: `libre`, `reservada`, `deshabilitada`, `mantenimiento`.

No hay otros estados. Una transición que no esté en las reglas anteriores se rechaza.
