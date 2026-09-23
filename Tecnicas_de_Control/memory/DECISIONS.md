# Decisiones persistentes

## D-001 — Grupo prioritario

El grupo del usuario es 236. Se prioriza su material sin eliminar variantes reales de otros grupos.

## D-002 — Jerarquía de fuentes

Guía docente, grupo 236, material docente actual, otros grupos y exámenes históricos, en ese orden y según la función de cada fuente.

## D-003 — Duplicados exactos

Se conserva una sola copia después de confirmar igualdad binaria. La ruta eliminada, la canónica y el hash quedan en el índice.

## D-004 — Variantes

Los casi duplicados con diferencias reales se conservan como `_v1.1`, `_v1.2`, etc., manteniendo su procedencia en el índice.

## D-005 — Grupo de tardes

`Grupo_Tardes__aula_S44_` fue autorizado para eliminación y no se utilizó para construir la base de conocimiento.

## D-006 — Metadatos

Los campos no demostrados permanecen vacíos. No se usa `unknown`.

## D-007 — Fuentes escaneadas

No se realiza OCR masivo. Los derivados futuros son archivos independientes con referencia al original y sus páginas.

## D-008 — Versionado

`VERSION.md` usa `FASE.MODIFICACION`. Al comenzar una fase, la modificación se reinicia a cero. No implica tags de Git.

## D-009 — Git

Se conserva Git LFS para ZIP, compatibilidad Windows/macOS y LF para texto. Commit, push y tags requieren autorización expresa.

## D-010 — UPVITOR y College Schedule

UPVITOR es la fuente principal del contenido académico. College Schedule se utiliza para calendario, entregas y planificación temporal.

## D-011 — Modos de ejercicios

El intento inicial con pistas se aplica en modo práctica guiada. El usuario puede solicitar solución completa, ejemplo de método o comprobación sin quedar bloqueado por esa regla.

## D-012 — Evidencia de aprendizaje

Una explicación o resumen no demuestra dominio. El progreso se registra en `LEARNING_STATE.md` mediante respuestas, ejercicios, tests, prácticas o aplicaciones verificables.

## D-013 — Catálogo de fuentes

`sources/catalog.json` es la fuente máquina y `sources/INDEX.md` es una vista generada. Tras modificar fuentes deben regenerarse el índice y la verificación de hashes.

## D-014 — Arquitectura proporcional

No se crean carpetas o archivos solo para anticipar contenido futuro. Cada área comienza como un único índice o archivo y se divide únicamente cuando exista volumen real.

## D-015 — Especialidades y multiagentes

Las especialidades de fuentes, tutoría, ingeniería y verificación pertenecen al agente principal. Un archivo Markdown no constituye un agente. Los subagentes solo se crean cuando el usuario lo solicita expresamente y el entorno lo permite.

## D-016 — Organización de fuentes

Las fuentes se organizan por función académica: oficial, exámenes, material docente y prácticas. El formato se registra en el catálogo y no determina por sí solo la carpeta.

## D-017 — Fases oficiales

Las versiones `v0.x` a `v4.x` corresponden respectivamente a diseño, construcción/migración, uso académico real, validación/estabilización y aplicación web. Cada fase tiene un criterio de cierre explícito en `ROADMAP.md`; el cambio de fase requiere autorización del usuario e inicio real del trabajo, y reinicia la segunda cifra a cero.
