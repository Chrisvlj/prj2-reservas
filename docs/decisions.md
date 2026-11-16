# Decisiones

## ADR-001 — Una aplicación Python, FastAPI y SQLite

Fecha: 2026-11-16. Estado: aceptada.

El sistema debe impedir dos reservas confirmadas del mismo cupo y mostrar esa misma disponibilidad. Una aplicación, una base SQLite y una transacción por escritura alcanzan para la entrega. FastAPI sirve las páginas y el JSON con los mismos casos de uso. pytest cubre las reglas sin levantar un segundo servicio.

Se descartó partir de una cola, un motor cliente-servidor o un framework de interfaz separado: agregan despliegue sin cambiar el resultado para el usuario.

## ADR-002 — Bloque de 50 minutos, jornada 07:00–20:20, día de 24 horas

Fecha: 2026-11-16. Estado: aceptada.

El outcome dice que 3 bloques son 45+5+45+5+45+5 minutos, es decir 150. La especificación fija el bloque en 50 minutos (45 de uso y 5 de transición) y 16 bloques. El bloque 1 empieza a las 07:00 y el bloque 16 termina a las 20:20. Una jornada hasta las 21:00 no cabe en 16 bloques de 50 minutos, así que el límite que se implementa es las 20:20.

"Un día" de antelación para cancelar se implementa como 24 horas antes del inicio, para poder probarlo con un reloj fijo. "Sin límite de tiempo" del docente se implementa como excepción a los 60 minutos de antelación, sin permitir desplazar un bloque ya terminado.

Si el horario institucional real fuera otro, se cambia la tabla de bloques en un solo lugar (`RN-01`) y se actualizan los criterios que citan horas concretas.

## ADR-003 — La notificación no bloquea el desplazamiento

Fecha: 2026-11-16. Estado: aceptada.

El outcome pide avisar por correo y ofrecer otro horario. La reserva del docente y el estado `desplazada` se confirman aunque el SMTP falle. Siempre queda una fila de notificación con el cuerpo (laboratorios alternativos, o la frase de que no hay). Así la evidencia del curso no depende de un buzón externo.

## ADR-004 — El uso de IA se documenta, no se presenta como otra persona

Fecha: 2026-11-16. Estado: aceptada.

El proyecto pide agentes de IA y un registro en `docs/ai-log.md` (actividad, herramienta, solicitud, resultado, decisión). Las capturas de esta fase muestran los artefactos producidos y los issues creados en GitHub. No se atribuyen a estudiantes distintos del grupo.
