# Arquitectura

## 1. Stack

| Capa | Elección |
|---|---|
| Lenguaje | Python 3.12 |
| API y páginas | FastAPI, plantillas Jinja2 |
| Persistencia | SQLite, un archivo en el entorno local |
| Acceso a datos | SQLAlchemy 2 |
| Pruebas | pytest, contra la misma base en memoria o un archivo temporal |
| Procesos | Una aplicación. No hay cola ni servicios aparte en esta versión. |

La libertad tecnológica del proyecto queda cubierta con esta elección. El motivo está en `docs/decisions.md` (ADR-001).

## 2. Por qué esta forma

El resultado que hay que proteger es que dos personas no confirmen el mismo laboratorio a la misma hora, y que la pantalla de disponibilidad sea esa misma verdad. Una sola base y una transacción por operación de escritura bastan. SQLite serializa escrituras, y la restricción de no solapar reservas vive en la transacción de la aplicación más una restricción en el modelo de franjas.

La interfaz es servidor con formularios. Reservar es: elegir fecha, ver laboratorios, marcar de 1 a 3 bloques, confirmar. Ese camino es el que debe caber en 3 minutos (RNF-01).

## 3. Vista lógica

```text
Navegador
    |
    |  HTML (consulta y reserva) y JSON (mismas operaciones)
    v
FastAPI
    |-- sesiones y rol
    |-- casos de uso (disponibilidad, reservar, cancelar, desplazar, mantenimiento)
    |-- reglas RN-*  (único lugar donde se decide si una franja cambia de estado)
    v
SQLite
    usuarios, laboratorios, franjas, reservas, notificaciones
```

Las páginas HTML llaman a los mismos casos de uso que la API JSON. No hay una segunda implementación de las reglas en el navegador: el navegador solo impide enviar un formulario incompleto.

## 4. Módulos previstos

```text
src/reservas/
    main.py              aplicación, rutas JSON y páginas
    db.py                motor SQLite, semilla y sesión
    models.py            tablas
    rules.py             calendario y RN-02
    services.py          transacciones: reservar, cancelar, desplazar, bloquear
    notifications.py     registra la notificación (SMTP opcional)
    reloj.py             hora del sistema o reloj fijo para las pruebas
    errors.py            rechazo de regla y rechazo de permiso
    templates/           pantallas de consulta, reserva y administración
tests/
    test_rules.py
    test_no_doble_reserva.py
    test_cancelacion.py
    test_desplazamiento.py
    test_aceptacion.py
```

## 5. Concurrencia

Crear reserva, desplazar y registrar reserva presencial abren una transacción, leen las franjas involucradas, aplican las reglas y escriben reserva más franjas. Si otra transacción ya tomó el cupo, la operación responde conflicto y no deja filas a medias.

SQLite usa modo WAL en el archivo de desarrollo. Las pruebas de conflicto lanzan dos operaciones sobre el mismo cupo.

## 6. Tiempo

Todas las comparaciones de antelación usan una hora inyectada en el caso de uso. En producción es la hora local del servidor. En pruebas es un reloj fijo, para poder afirmar "faltan 59 minutos" sin depender del reloj de la máquina.

## 7. Correo

`notifications.py` escribe la fila de notificación con destinatario, asunto y cuerpo. Si existe la variable `SMTP_URL`, intenta el envío y guarda el resultado. Si no existe, la notificación queda en estado `pendiente` y el cuerpo queda disponible para la evidencia del curso. El desplazamiento no depende de que el correo salga: si el envío falla, la reserva igual cambia y la notificación queda registrada con error.

## 8. Entornos

| Entorno | Base | Correo |
|---|---|---|
| Desarrollo | `data/reservas.db` | registro local |
| Pruebas | SQLite temporal por test | no se envía |
| Demostración | el mismo esquema, con laboratorios de ejemplo | registro local |

No hay cuentas ni secretos en el repositorio. Un archivo `.env.example` listará `SMTP_URL` vacío.

## 9. Qué no entra en la arquitectura

- Réplicas, caché y balanceo.
- Inicio de sesión con un proveedor externo. La versión de entrega usa usuarios sembrados (estudiante, docente, administrador) y una sesión de servidor.
