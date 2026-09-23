# Hoja de ruta de UPVITOR

Esta es la correspondencia oficial entre las fases del proyecto y su versión lógica.

Estado actual: **Fase 1 — Construcción / migración (`v1.3`)**.

## Fases oficiales

| Fase | Versiones | Objetivo | Termina cuando… |
| --- | --- | --- | --- |
| **0 — Diseño** | `v0.x` | Auditoría, arquitectura, Git/GitHub, reglas, especialidades, fuentes, duplicados, grupo 236, guía docente y compatibilidad Windows/macOS. | El diseño está aprobado y se sabe exactamente qué construir. |
| **1 — Construcción / migración** | `v1.x` | Crear físicamente la estructura necesaria; mover e indexar archivos; corregir nombres o extensiones; y conservar la trazabilidad. | La estructura existe, no se ha perdido información y los cambios han quedado comprobados y registrados en Git. |
| **2 — Uso académico real** | `v2.x` | Estudiar con UPVITOR: resúmenes, modo tutor, ejercicios, examinador, memoria, dudas, errores y entregables. | Órdenes como `Resumen tema 1`, `Tutor UD1` y `Examíname UD2` funcionan correctamente. |
| **3 — Validación y estabilización** | `v3.x` | Usar el sistema durante varias semanas y probar sesiones nuevas, Windows/macOS, Git, memoria, fuentes y OCR bajo demanda; corregir fallos reales. | UPVITOR funciona normalmente sin modificar continuamente su arquitectura. |
| **4 — Aplicación web** | `v4.x` | Llevar el sistema a una interfaz web con asignaturas, tutor, ejercicios, progreso, fuentes y panel de control. | UPVITOR puede utilizarse cómodamente desde la web sin depender de VS Code para el uso diario. |

## Reglas de transición

- Una modificación relevante dentro de la fase actual incrementa la segunda cifra.
- Al comenzar realmente una fase nueva, la segunda cifra se reinicia a cero: por ejemplo, `v1.x` pasa a `v2.0`.
- El cambio de fase requiere aprobación explícita del usuario y el inicio real del trabajo de esa fase.
- Completar técnicamente una parte de una fase no adelanta por sí solo la versión a la fase siguiente.
- `VERSION.md` registra la versión lógica; Git registra estados concretos del repositorio.
- No se crean commits, tags ni publicaciones automáticamente.

## Situación de la Fase 1

La migración y sus comprobaciones existen localmente. Antes de cerrar la Fase 1 queda revisar el conjunto final y, con autorización expresa, registrarlo mediante un commit de Git. La Fase 2 empezará como `v2.0` cuando se autorice e inicie el uso académico real.

Las áreas mencionadas en esta hoja de ruta describen funciones del sistema, no obligan a crear carpetas vacías ni falsos agentes. La estructura física seguirá siendo proporcional al contenido real.
