# Plan de implementación

Orden de construcción. Cada ítem sale de las especificaciones y termina en prueba antes de seguir al siguiente comportamiento. Los issues de GitHub usan el mismo título.

## 1. Secuencia

| Orden | Issue | Tarea | Spec | Prueba que la cierra |
|---|---|---|---|---|
| 1 | [#1](https://github.com/Chrisvlj/prj2-reservas/issues/1) | Esquema SQLite: usuario, laboratorio, franja, reserva, notificación. Semilla de Ana, Luis, Rosa, Lab 1 y Lab 2. | data-model | La semilla se lee en un test de humo. |
| 2 | [#2](https://github.com/Chrisvlj/prj2-reservas/issues/2) | Consultar disponibilidad de una fecha, creando franjas `libre` que falten. | RF-01, API disponibilidad | CA-01 |
| 3 | [#3](https://github.com/Chrisvlj/prj2-reservas/issues/3) | Crear reserva en línea de 1 a 3 bloques, con antelación y transacción. | RN-02, RN-05, RN-11 | CA-03, CA-04, CA-05 |
| 4 | [#4](https://github.com/Chrisvlj/prj2-reservas/issues/4) | Rechazar solape del mismo usuario y solape del mismo laboratorio, incluidos dos intentos concurrentes. | RN-07, RN-08, RN-09 | CA-07, CA-08, CA-09, CA-10 |
| 5 | [#5](https://github.com/Chrisvlj/prj2-reservas/issues/5) | Cancelar con las dos consecuencias (libre o deshabilitada) y no-show. | RN-17 a RN-21 | CA-16, CA-17, CA-18, CA-20 |
| 6 | [#6](https://github.com/Chrisvlj/prj2-reservas/issues/6) | Liberar, mantenimiento y reserva presencial del administrador. | RN-06, RN-22, RN-23 | CA-06, CA-19, CA-21, CA-22 |
| 7 | [#7](https://github.com/Chrisvlj/prj2-reservas/issues/7) | Desplazamiento docente y notificación con o sin alternativa. | RN-12 a RN-16 | CA-11 a CA-15 |
| 8 | [#8](https://github.com/Chrisvlj/prj2-reservas/issues/8) | Páginas de consulta, reserva y administración sobre los mismos casos de uso. | RNF-01, sección Páginas | CA-02, recorrido manual |
| 9 | [#9](https://github.com/Chrisvlj/prj2-reservas/issues/9) | Lectura de ocupación del periodo con la fórmula del modelo de datos. | outcomes, métrica 70 % | Consulta reproducible sobre datos de prueba. |

La tarea 4 no se salta. El proyecto exige una prueba automatizada de no permitir la doble reserva.

## 2. Definición de hecho de cada tarea

- La regla que toca sigue escrita igual en `specs/`, o la spec se actualizó antes que el código.
- Hay prueba automática del criterio citado, y pasa.
- No queda una segunda copia de la regla en la plantilla HTML.

## 3. Cambio de requisito a mitad del desarrollo

Cambio solicitado el 2026-11-16, con el núcleo de las tareas 1 a 9 ya en `main`: un estudiante no puede tener más de dos reservas confirmadas en la misma semana (lunes a domingo). El docente no tiene ese tope.

| Paso | Dónde quedó |
|---|---|
| Cambio solicitado | [#11](https://github.com/Chrisvlj/prj2-reservas/issues/11) |
| Especificación | RF-14, RN-25, ADR-005 |
| Criterios | CA-24 a CA-28 |
| Plan | Esta sección |
| Código | `src/reservas/services.py`, conteo antes de ocupar el cupo |
| Pruebas | `tests/test_tope_semanal.py` |
| Resultado | La tercera reserva de la semana responde `RN-25` y el cupo sigue libre |

## 4. Issues

El tablero de trabajo son issues en `Chrisvlj/prj2-reservas`, un issue por cada fila de la tabla de secuencia, con etiqueta de la fase de construcción (`datos`, `reglas`, `qa`, `ui`). Cerrar el issue requiere la prueba de esa fila en verde.

## 5. Rama e integración

- `main` se mantiene ejecutable.
- Cada fila de la tabla se trabaja en una rama `tarea/<numero>-<nombre-corto>`.
- La integración a `main` es un pull request que enlaza el issue y muestra la prueba.

## 6. Qué queda fuera de este plan

Presentación (LibreOffice Impress). El núcleo de las tareas 1 a 9 está en `main` y el cambio de la sección 3 está en el issue #11.
