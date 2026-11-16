# Pruebas

Plan de pruebas derivado de `specs/acceptance-criteria.md`. La suite está en `tests/` y se ejecuta con `pytest`.

## 1. Obligatorio según el enunciado

| Tipo | Dónde | Qué demuestra |
|---|---|---|
| Unitarias de reglas | `tests/test_rules.py` | RN-01 y RN-02: límites de bloque, duración 1 a 3, cálculo de inicio. |
| Reglas críticas | `tests/test_cancelacion.py`, `tests/test_desplazamiento.py` | CA-11 a CA-22. |
| Conflicto de reserva | `tests/test_no_doble_reserva.py` | CA-07, CA-08 y CA-09. CA-07 es la prueba obligatoria de no doble reserva. |
| Validación de usuario | `tests/test_aceptacion.py` | Rol, sesión, antelación de estudiante frente a reserva presencial del administrador (CA-05, CA-06, CA-19). |
| Criterios de aceptación | los archivos anteriores, un criterio por test con el id en el nombre | CA-01 a CA-23, salvo CA-02. |

CA-02 (reservar en menos de 3 minutos) se recorre en la interfaz y se anota en la evidencia manual. No se automatiza con un temporizador.

## 2. Nombres previstos

| Test | Criterio |
|---|---|
| `test_ca01_disponibilidad_muestra_estado` | CA-01 |
| `test_ca03_reserva_de_tres_bloques` | CA-03 |
| `test_ca04_rechaza_mas_de_tres_bloques` | CA-04 |
| `test_ca05_rechaza_menos_de_una_hora` | CA-05 |
| `test_ca06_presencial_bajo_la_hora` | CA-06 |
| `test_ca07_no_doble_reserva_mismo_laboratorio` | CA-07 |
| `test_ca08_una_sola_gana_si_compiten` | CA-08 |
| `test_ca09_no_solape_entre_laboratorios` | CA-09 |
| `test_ca10_mismo_laboratorio_otro_bloque` | CA-10 |
| `test_ca11_docente_desplaza_sin_antelacion` | CA-11 |
| `test_ca12_notificacion_ofrece_otro_lab` | CA-12 |
| `test_ca13_notificacion_sin_alternativa` | CA-13 |
| `test_ca14_no_desplaza_a_docente` | CA-14 |
| `test_ca15_docente_no_queda_en_dos_sitios` | CA-15 |
| `test_ca16_cancelar_con_un_dia_libera` | CA-16 |
| `test_ca17_cancelar_tarde_deshabilita` | CA-17 |
| `test_ca18_no_se_reserva_franja_deshabilitada` | CA-18 |
| `test_ca19_solo_admin_libera` | CA-19 |
| `test_ca20_no_show_deshabilita` | CA-20 |
| `test_ca21_mantenimiento` | CA-21 |
| `test_ca22_no_mantenimiento_sobre_reserva` | CA-22 |
| `test_ca23_presencial_guarda_quien_la_creo` | CA-23 |
| `test_ca24_tercera_reserva_de_la_semana` | CA-24 |
| `test_ca25_cancelar_libera_el_tope` | CA-25 |
| `test_ca26_docente_sin_tope_semanal` | CA-26 |
| `test_ca27_otra_semana_no_suma` | CA-27 |
| `test_ca28_presencial_cuenta_para_el_estudiante` | CA-28 |

## 3. Cómo se aísla el tiempo y la base

Cada test construye su SQLite temporal y fija el reloj que describe el criterio. No se comparte estado entre tests. El correo no sale de la máquina: se afirma sobre la fila de notificación.

## 4. Evidencia

La evidencia automática es la salida de `pytest` en verde. CA-02 se recorre en las pantallas: entrar, ver la disponibilidad, reservar y ver la reserva en la lista.
