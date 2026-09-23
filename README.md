# UPVITOR

UPVITOR es un sistema universitario local para conservar fuentes, organizar conocimiento y convertir material académico en aprendizaje verificable.

## Alcance actual

La primera asignatura migrada es `Tecnicas_de_Control`. Las demás carpetas de asignaturas permanecen intactas hasta que exista una instrucción expresa para migrarlas.

## Estructura

- `shared/`: reglas y plantillas reutilizables.
- `Tecnicas_de_Control/sources/`: fuentes originales y catálogo de procedencia.
- `Tecnicas_de_Control/topics/`: un archivo vivo por unidad didáctica.
- `Tecnicas_de_Control/practices/`: seguimiento compacto de P1-P6.
- `Tecnicas_de_Control/exercises/`: ejercicios creados cuando exista trabajo real.
- `Tecnicas_de_Control/outputs/`: entregables generados.
- `Tecnicas_de_Control/memory/`: decisiones y evolución persistente.
- `Tecnicas_de_Control/scripts/`: mantenimiento del catálogo de fuentes.

## Fuentes

La jerarquía es: guía docente, material del grupo 236, material docente actual, otros grupos como complemento y exámenes históricos como evidencia. Ninguna explicación generada sustituye a una fuente original.

Las fuentes se organizan por función académica:

- `official/`: documentación oficial;
- `exams/`: exámenes, tests y formularios;
- `teaching_material/`: materiales de grupos docentes;
- `practices/`: materiales de laboratorio y práctica.

Consulta `Tecnicas_de_Control/sources/INDEX.md` antes de usar o reclasificar materiales.

`sources/catalog.json` es el catálogo máquina. `sources/INDEX.md` se genera a partir de él y no debe editarse manualmente.

## Inicio rápido

1. Lee `VERSION.md` y los `AGENTS.md` aplicables.
2. Abre `Tecnicas_de_Control/docs/subject_overview.md`.
3. Comprueba `Tecnicas_de_Control/memory/LEARNING_STATE.md`.
4. Localiza las fuentes en `Tecnicas_de_Control/sources/INDEX.md`.
5. Trabaja en el tema, práctica o ejercicio correspondiente.

## Verificación de fuentes

Desde la raíz del repositorio:

```text
python Tecnicas_de_Control/scripts/build_source_index.py
python Tecnicas_de_Control/scripts/verify_sources.py
```

El primer comando regenera el índice humano. El segundo comprueba cobertura y hashes. Ejecuta ambos después de añadir, mover, renombrar o eliminar una fuente.

## Versionado

`VERSION.md` registra la versión lógica de la arquitectura y `ROADMAP.md` define las fases oficiales y sus criterios de cierre. Git registra estados concretos de archivos. No se crean tags, commits ni publicaciones automáticamente.
