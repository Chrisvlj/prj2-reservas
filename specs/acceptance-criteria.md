# Criterios de aceptación

Forma: dado un estado, cuando ocurre una acción, entonces el resultado observable. Cada criterio cita la regla. La prueba automática correspondiente se nombra en `docs/testing.md`.

El reloj de los escenarios es fijo: 2026-11-16 08:00, salvo que el criterio diga otra hora. Lab 1 y Lab 2 existen y están activos. Ana es estudiante, Luis es docente, Rosa es administradora.

## Disponibilidad

### CA-01 — Ver el día

Dado que el bloque 2 de Lab 1 está `libre` y el bloque 3 está `reservada`, cuando Ana consulta la disponibilidad del 2026-11-20, entonces ve esos estados y no puede confirmar el bloque 3.

Cubre RF-01.

### CA-02 — Reserva dentro de 3 minutos

Dado que Ana ya tiene sesión y hay un bloque libre, cuando recorre consulta, elección y confirmación, entonces el camino son esas tres acciones, sin un paso presencial.

Cubre RNF-01. Se comprueba con el recorrido de la interfaz, no con un temporizador de prueba.

## Reserva en línea

### CA-03 — Reserva válida

Dado un cupo libre dentro de la antelación, cuando Ana reserva los bloques 4 a 6 de Lab 1 el 2026-11-20, entonces existe una reserva `confirmada`, origen `en_linea`, y esos bloques quedan `reservada`.

Cubre RF-02, RN-02, RN-11. Inicio del bloque 4: 09:30. Antelación mayor a 60 minutos.

### CA-04 — Más de tres bloques

Cuando Ana pide los bloques 1 a 4, entonces la API responde 409 con `RN-02` y no se escribe reserva.

### CA-05 — Menos de una hora

Dado el reloj en 2026-11-20 09:00 y el bloque 3 empezando a las 08:40 ya pasado, o un bloque que empieza en 30 minutos, cuando Ana intenta reservarlo en línea, entonces recibe `RN-05` y el cupo sigue `libre`.

### CA-06 — Presencial bajo la hora

Dado el mismo reloj y un bloque que empieza en 30 minutos, cuando Rosa registra la reserva presencial a nombre de Ana, entonces la reserva queda `confirmada` con origen `presencial`.

Cubre RF-12, RN-06.

## Doble reserva

### CA-07 — Mismo laboratorio

Dado que Ana tiene confirmados los bloques 4 a 5 de Lab 1, cuando Luis reserva el bloque 5 de Lab 1, entonces Luis recibe `RN-08` y sigue existiendo una sola reserva confirmada sobre ese bloque.

Cubre RF-03, RN-08, RN-09. Esta prueba es obligatoria en `tests/test_no_doble_reserva.py`.

### CA-08 — Dos solicitudes a la vez

Cuando Ana y Luis confirman al mismo tiempo el bloque 8 de Lab 2, entonces exactamente una respuesta es 201 y la otra es 409 `RN-08`. Hay una sola fila `confirmada` para ese cupo.

Cubre RNF-02.

### CA-09 — Dos laboratorios a la vez

Dado que Ana tiene el bloque 4 de Lab 1, cuando Ana reserva el bloque 4 de Lab 2, entonces recibe `RN-07` y Lab 2 sigue `libre` en ese bloque.

Cubre RF-04.

### CA-10 — El mismo laboratorio, otro momento

Dado que Ana tiene el bloque 4 de Lab 1, cuando Ana reserva el bloque 8 de Lab 1, entonces la segunda reserva se confirma. RN-07 solo corta el solape.

## Prioridad docente

### CA-11 — Desplaza al estudiante

Dado que Ana tiene confirmados los bloques 4 a 6 de Lab 1 y falta menos de 60 minutos para el inicio, cuando Luis desplaza esa reserva, entonces la reserva de Ana pasa a `desplazada`, Luis tiene una `confirmada` sobre esos bloques y existe una notificación a Ana.

Cubre RF-06, RN-12, RN-15.

### CA-12 — Oferta de otro laboratorio

Dado CA-11 y que Lab 2 está `libre` en los bloques 4 a 6, cuando se crea la notificación, entonces el cuerpo nombra Lab 2 y no crea una reserva nueva para Ana.

### CA-13 — Sin alternativa

Dado que ningún otro laboratorio está libre en esos bloques, cuando Luis desplaza, entonces la notificación dice que no hay alternativa.

### CA-14 — No desplaza a otro docente

Dado que Luis ya tiene el bloque 4 de Lab 1, cuando otro docente intenta desplazarlo, entonces recibe rechazo y la reserva de Luis sigue `confirmada`.

Cubre RN-13.

### CA-15 — El docente no queda en dos sitios

Dado que Luis ya tiene el bloque 4 de Lab 2, cuando intenta desplazar el bloque 4 de Ana en Lab 1, entonces recibe `RN-07` y Ana conserva su reserva.

Cubre RN-16.

## Cancelación e inasistencia

### CA-16 — Con un día o más

Dado una reserva que empieza en 25 horas o más, cuando el titular cancela, entonces la reserva queda `cancelada` y los bloques `libre`.

Cubre RF-07, RN-18.

### CA-17 — Con menos de un día

Dado una reserva que empieza en 2 horas, cuando el titular cancela, entonces los bloques quedan `deshabilitada`.

Cubre RF-08, RN-19.

### CA-18 — Nadie más toma una franja deshabilitada

Dado CA-17, cuando Luis intenta reservar ese bloque, entonces recibe `RN-10`.

### CA-19 — Liberar es solo del administrador

Dado un bloque `deshabilitada`, cuando Ana intenta liberarlo, entonces recibe 403. Cuando Rosa lo libera, el bloque queda `libre`.

Cubre RF-10, RN-22.

### CA-20 — No-show

Dado una reserva cuyo inicio ya pasó, cuando Rosa marca no-show, entonces la reserva queda `no_show` y los bloques `deshabilitada`.

Cubre RF-09, RN-21.

## Mantenimiento

### CA-21 — Bloquear y reabrir

Cuando Rosa pone el bloque 10 de Lab 1 en mantenimiento, entonces nadie lo reserva. Cuando Rosa cierra el mantenimiento, el bloque vuelve a `libre`.

Cubre RF-11, RN-23.

### CA-22 — No tapar una reserva

Dado el bloque 10 `reservada`, cuando Rosa intenta pasarlo a mantenimiento, entonces la operación se rechaza y la reserva sigue `confirmada`.

## Trazabilidad

### CA-23 — Queda quién reservó

Dado CA-06, cuando se lee la reserva, entonces `creada_por` es Rosa y `usuario_id` es Ana.

Cubre RF-13.
