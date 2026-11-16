# Requisitos — Sistema de Reservas de Laboratorios

Traducción del outcome (`specs/outcomes.md`) a capacidades del sistema. Las reglas numeradas viven en `specs/business-rules.md`. Los criterios de aceptación que las verifican están en `specs/acceptance-criteria.md`.

## 1. Actores

| Actor | Descripción |
|---|---|
| Estudiante | Consulta disponibilidad y reserva para clase o uso personal. |
| Docente | Consulta y reserva con prioridad: puede desplazar una reserva de estudiante. |
| Administrador | Registra lo que ocurre en físico (reservas presenciales, mantenimiento) y libera franjas deshabilitadas. |

Una cuenta tiene un solo rol.

## 2. Requisitos funcionales

| ID | Requisito | Origen en el outcome |
|---|---|---|
| RF-01 | El usuario autenticado ve, para una fecha, qué laboratorios y bloques están libres, reservados, deshabilitados o en mantenimiento. | Ver disponibilidad en tiempo real, sin ir al laboratorio. |
| RF-02 | Estudiante y docente crean una reserva de 1 a 3 bloques consecutivos en un laboratorio libre. | Reservar sin desplazarse. |
| RF-03 | El sistema rechaza una reserva que se solape con otra reserva confirmada del mismo laboratorio. | Se elimina el cruce de horario. Quien reserva primero conserva el cupo. |
| RF-04 | El sistema rechaza que la misma persona tenga dos reservas confirmadas solapadas, aunque sean en laboratorios distintos. | No hay reservas simultáneas en laboratorios distintos. |
| RF-05 | Una reserva en línea exige al menos 60 minutos de antelación respecto del inicio. Con menos tiempo, solo el administrador puede registrarla como reserva presencial. | Mínimo 1 hora; si no, solo presencial. |
| RF-06 | El docente puede tomar un horario ya reservado por un estudiante. La reserva del estudiante pasa a desplazada, se le notifica y se le proponen otros laboratorios libres en ese mismo horario. | Prioridad del docente, sin límite de tiempo, con correo y otro horario. |
| RF-07 | Cancelar con 24 horas o más de antelación deja los bloques libres. | Cancelación con 1 día o más. |
| RF-08 | Cancelar con menos de 24 horas deja los bloques deshabilitados. | Cancelación tardía. |
| RF-09 | Marcar no-show deja los bloques deshabilitados. | El horario no se libera. |
| RF-10 | Solo el administrador libera una franja deshabilitada, tras la solicitud presencial. | Liberación solo presencial, vía administrador. |
| RF-11 | El administrador bloquea bloques por mantenimiento y los vuelve a abrir al cerrar el mantenimiento. | Mantenimiento. |
| RF-12 | El administrador registra una reserva presencial a nombre de un usuario, también cuando falta menos de 1 hora. | Las reservas físicas deben verse en el sistema. |
| RF-13 | Cada reserva guarda quién la creó y cuándo, para poder explicar un cruce si el sistema fallara. | Margen de menos de 4 cruces por semana, con trazabilidad. |

## 3. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | Completar una reserva (consultar, elegir, confirmar) cabe en menos de 3 minutos para quien ya tiene cuenta. |
| RNF-02 | Dos intentos simultáneos sobre el mismo laboratorio y bloques no pueden dejar dos reservas confirmadas. La comprobación y la escritura ocurren en la misma transacción. |
| RNF-03 | La disponibilidad que muestra la consulta es la que usa la creación de la reserva. No hay un estado paralelo en papel. |
| RNF-04 | El stack, la base de datos y el despliegue quedan descritos en `specs/architecture.md`. |
| RNF-05 | El uso de IA durante el desarrollo queda en `docs/ai-log.md`. |

## 4. Fuera de alcance en esta versión

- Pagos, listas de espera automáticas y reserva recurrente semanal.
- Aplicación móvil nativa.
- Más de un rol por cuenta.
- Un docente desplazando a otro docente. Entre docentes gana quien reservó primero.
- Envío real garantizado del correo: el sistema registra la notificación y el texto. El transporte SMTP es configurable y puede quedar en registro local durante el desarrollo.

## 5. Supuestos que la especificación fija

Estos puntos estaban abiertos en el outcome. Quedan decididos aquí para poder implementar. El registro de la decisión está en `docs/decisions.md`.

- Un bloque dura 50 minutos: 45 de uso y 5 de transición. Tres bloques son 150 minutos.
- La jornada reservable son 16 bloques de 50 minutos, de 07:00 a 20:20. Dieciséis por cincuenta minutos no llegan a las 21:00; el cierre real del último bloque es las 20:20.
- "Un día" de antelación para cancelar significa 24 horas antes del inicio del primer bloque.
- "Sin límite de tiempo" en el desplazamiento docente significa que no aplica la antelación de 60 minutos. No puede desplazar un bloque que ya terminó.
- La oferta de otro horario al estudiante desplazado son los otros laboratorios libres en los mismos bloques. Si no hay ninguno, la notificación lo dice y no se crea otra reserva sola.
