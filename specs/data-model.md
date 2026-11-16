# Modelo de datos

SQLite. Los nombres de columna están en español para alinearlos con las reglas de `specs/business-rules.md`.

## 1. Usuario

| Columna | Tipo | Notas |
|---|---|---|
| id | entero | clave |
| nombre | texto | obligatorio |
| correo | texto | único, obligatorio |
| rol | texto | `estudiante`, `docente`, `administrador` |
| clave_hash | texto | solo para la sesión de la entrega |

## 2. Laboratorio

| Columna | Tipo | Notas |
|---|---|---|
| id | entero | clave |
| nombre | texto | único, por ejemplo "Lab 1" |
| ubicacion | texto | opcional |
| activo | entero | 1 activo, 0 fuera de servicio permanente |

Un laboratorio inactivo no aparece como reservable. No sustituye al mantenimiento por bloques.

## 3. Franja

Una fila por laboratorio, fecha y número de bloque. Se crean al consultar o al reservar si aún no existen, en estado `libre`.

| Columna | Tipo | Notas |
|---|---|---|
| id | entero | clave |
| laboratorio_id | entero | |
| fecha | texto | `YYYY-MM-DD` |
| bloque | entero | 1 a 16 |
| estado | texto | `libre`, `reservada`, `deshabilitada`, `mantenimiento` |
| reserva_id | entero | nulo si no está `reservada` |

Único: (`laboratorio_id`, `fecha`, `bloque`).

Ese único es la garantía de RN-08 junto con la transacción: no hay dos franjas para el mismo cupo.

## 4. Reserva

| Columna | Tipo | Notas |
|---|---|---|
| id | entero | clave |
| usuario_id | entero | titular |
| laboratorio_id | entero | |
| fecha | texto | |
| bloque_inicio | entero | |
| bloque_fin | entero | inclusivo; fin - inicio + 1 entre 1 y 3 |
| estado | texto | `confirmada`, `cancelada`, `desplazada`, `no_show` |
| origen | texto | `en_linea`, `presencial` |
| creada_en | texto | ISO-8601 |
| creada_por | entero | usuario que ejecutó la acción; puede ser el administrador |
| actualizada_en | texto | |
| desplaza_a | entero | nulo, o id de la reserva de estudiante que fue desplazada |

## 5. Notificación

| Columna | Tipo | Notas |
|---|---|---|
| id | entero | clave |
| reserva_id | entero | |
| destinatario_id | entero | |
| tipo | texto | `desplazamiento` en esta versión |
| cuerpo | texto | incluye laboratorios alternativos, o dice que no hay |
| estado | texto | `pendiente`, `enviada`, `error` |
| creada_en | texto | |

## 6. Relaciones

```text
usuario 1---* reserva
laboratorio 1---* franja
laboratorio 1---* reserva
reserva 1---* franja        (mientras estado reservada)
reserva 1---* notificacion
reserva 0---1 reserva       (desplaza_a)
```

## 7. Consultas que el modelo debe poder responder

- Franjas de una fecha, todos los laboratorios activos, con su estado.
- Reservas `confirmada` de un usuario que solapan un intervalo.
- Laboratorios con todos los bloques pedidos en estado `libre`, para la oferta al estudiante desplazado.
- Reservas de una semana y franjas no `libre`, para calcular ocupación frente a la meta del 70 %.

## 8. Ocupación

La ocupación de un periodo es:

`franjas en estado reservada / (laboratorios activos × bloques de la jornada × días del periodo)`

La meta del outcome (de 40 % a 70 %) se informa con esa fórmula. El sistema no rellena reservas falsas para subir el porcentaje.
