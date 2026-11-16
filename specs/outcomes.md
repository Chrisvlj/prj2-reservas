# Outcomes — Sistema de Reservas de Laboratorios

Proyecto 2 · Tópicos Especiales II · Fase 1 (ODD)

Este documento es la entrada de la Fase 2. Las especificaciones en `specs/` traducen este resultado a requisitos, reglas, modelo, API, criterios de aceptación y plan.

## 1. Problema

Los docentes y estudiantes reservan los laboratorios de forma física. Para saber si hay disponibilidad deben ir presencialmente y, muchas veces, descubren que el laboratorio está ocupado. Por eso reservan con mucha antelación para intentar asegurarlo. Esto genera desplazamientos inútiles, cruces de horario y laboratorios mal aprovechados.

## 2. Usuarios y necesidades

| Usuario | Necesidad |
|---|---|
| Docente | Conocer la disponibilidad y reservar un laboratorio para dar clases, sin ir a consultarlo físicamente. Tiene prioridad sobre los estudiantes. |
| Estudiante | Conocer la disponibilidad y reservar un laboratorio (clases o motivos personales), sin ir a consultarlo físicamente. |
| Administrador | Bloquear laboratorios (mantenimiento, reservas presenciales) y liberar horarios deshabilitados. |

## 3. Outcome (resultado esperado)

Que docentes y estudiantes puedan ver en tiempo real qué laboratorios están disponibles en un horario y reservar uno sin desplazarse, eliminando los cruces de horario y aumentando el uso de los laboratorios.

## 4. Preguntas exploradas

1. **¿Quiénes son los usuarios?** Docentes y estudiantes. Requieren lo mismo: conocer la disponibilidad sin ir físicamente.
2. **¿Cómo se reserva hoy?** De forma física. Problema: hay que ir presencialmente para enterarse de que no hay disponibilidad, o reservar con mucha antelación.
3. **¿Qué pasa si dos personas quieren el mismo laboratorio a la misma hora?** Se le asigna a quien llegó primero. En el sistema, gana quien reserva primero.
4. **¿Qué reglas existen?**
   - Duración máxima de 3 bloques: 45 + 5 + 45 + 5 + 45 + 5 minutos (150 min).
   - Reserva con mínimo 1 hora de antelación (el mismo día); con menos tiempo, solo presencial.
   - Una persona no puede reservar el mismo laboratorio dos veces en un mismo momento.
   - No se permiten reservas simultáneas en laboratorios distintos.
   - Prioridad del docente sobre el estudiante.
5. **¿Qué pasa con cancelaciones, no-shows y mantenimiento?**
   - Cancelación con 1 día o más de antelación: el horario queda libre.
   - Cancelación con menos de 1 día: el horario queda deshabilitado; solo se libera si se solicita presencialmente al administrador.
   - No-show: el horario no se libera, queda deshabilitado salvo solicitud presencial.
   - Mantenimiento: lo bloquea el administrador.
6. **¿Qué pasa si un docente necesita un horario ya reservado por un estudiante?** El docente desplaza al estudiante, sin límite de tiempo. Se notifica por correo y se le ofrece otro horario.

## 5. Métricas de éxito

| Métrica | Meta |
|---|---|
| Cruces de horario | Menos de 4 por semana (ideal: 0; el margen contempla posibles fallos del sistema) |
| Tiempo para completar una reserva | Menos de 3 minutos |
| Porcentaje de ocupación de los laboratorios | Pasar de 40 % (actual) a 70 % (meta realista) |

## 6. Supuestos y puntos por confirmar

- El sistema está diseñado para impedir la doble reserva del mismo laboratorio (objetivo: 0 cruces). La meta de "menos de 4 cruces por semana" es un margen de tolerancia ante posibles fallos del sistema, no un objetivo deseado.
- La ocupación actual es de 40 %; la meta es llegar a 70 %, considerada realista.
- Se asume que las reservas presenciales las registra el administrador en el sistema para mantener la disponibilidad actualizada.
