# API

Base: `/api`. Las pantallas HTML cubren las mismas operaciones para el flujo de reserva. Los errores de regla usan HTTP 409 con `{"codigo": "RN-08", "mensaje": "..."}`. Un dato mal formado usa 422. Falta de rol usa 403. Falta de sesión usa 401.

La hora de la operación viaja en las pruebas por el reloj inyectado. Los clientes no envían "la hora oficial".

## 1. Sesión

| Método | Ruta | Rol | Efecto |
|---|---|---|---|
| POST | `/api/sesion` | público | Cuerpo: `correo`, `clave`. Abre sesión. |
| DELETE | `/api/sesion` | autenticado | Cierra sesión. |
| GET | `/api/sesion` | autenticado | Devuelve id, nombre y rol. |

## 2. Catálogo

| Método | Ruta | Rol | Efecto |
|---|---|---|---|
| GET | `/api/laboratorios` | autenticado | Laboratorios activos. |
| GET | `/api/disponibilidad?fecha=YYYY-MM-DD` | autenticado | Por laboratorio, los 16 bloques y su estado. |

Ejemplo de un bloque en la respuesta:

```json
{"bloque": 3, "inicio": "08:40", "fin": "09:30", "estado": "libre"}
```

`inicio`/`fin` son los 50 minutos del bloque. El uso de clase son los primeros 45.

## 3. Reservas

### Crear

`POST /api/reservas`

```json
{
  "laboratorio_id": 1,
  "fecha": "2026-11-20",
  "bloque_inicio": 2,
  "bloque_fin": 4
}
```

Rol estudiante o docente. Aplica RN-02, RN-05, RN-07, RN-08, RN-10, RN-11.

Respuesta 201: la reserva `confirmada` y el origen `en_linea`.

### Reserva presencial

`POST /api/reservas/presenciales`

```json
{
  "usuario_id": 12,
  "laboratorio_id": 1,
  "fecha": "2026-11-20",
  "bloque_inicio": 2,
  "bloque_fin": 2
}
```

Solo administrador. Misma comprobación de cupo y de solape del titular, sin RN-05. Origen `presencial`.

### Listar las propias

`GET /api/reservas?mias=1`

### Cancelar

`POST /api/reservas/{id}/cancelar`

Titular o administrador. Aplica RN-17 a RN-20. Respuesta: estado `cancelada` y el estado en que quedaron los bloques (`libre` o `deshabilitada`).

### Desplazar

`POST /api/reservas/{id}/desplazar`

Solo docente. `{id}` es la reserva del estudiante. Cuerpo opcional:

```json
{"bloque_inicio": 2, "bloque_fin": 3}
```

Si no se envían bloques, se toman todos los de la reserva del estudiante. Esos bloques deben ser un subconjunto consecutivo de la reserva desplazada, de 1 a 3 bloques.

Aplica RN-12 a RN-16. Respuesta: reserva nueva del docente, reserva del estudiante en `desplazada`, y la notificación creada (id, estado, laboratorios alternativos).

### No-show

`POST /api/reservas/{id}/no-show`

Solo administrador. Aplica RN-21.

## 4. Franjas de administración

`POST /api/franjas/liberar`

```json
{"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [2, 3]}
```

Solo administrador. Cada bloque debe estar `deshabilitada`. Pasan a `libre` (RN-22).

`POST /api/franjas/mantenimiento`

```json
{"laboratorio_id": 1, "fecha": "2026-11-20", "bloques": [5], "activo": true}
```

`activo: true` pasa de `libre` a `mantenimiento`. `activo: false` pasa de `mantenimiento` a `libre`. Aplica RN-23.

## 5. Páginas

| Ruta | Uso |
|---|---|
| `/` | Disponibilidad del día elegido y acceso a reservar. |
| `/reservas/nueva` | Confirmar de 1 a 3 bloques ya elegidos. |
| `/reservas` | Reservas del usuario y cancelar. |
| `/admin` | Presencial, mantenimiento, liberar, no-show. Solo administrador. |

## 6. Códigos de regla en los rechazos

El campo `codigo` usa el identificador RN cuando el rechazo es una regla de negocio. Varios pueden aplicar; se devuelve el primero que falle en este orden: rol y sesión, RN-02, RN-06 o RN-05, RN-10, RN-07, RN-25, RN-08, y el resto de la operación (desplazamiento, cancelación, mantenimiento).
