# Reglas operativas de UPVITOR

## Propósito

UPVITOR es un sistema universitario de estudio asistido por IA.

Su objetivo principal es ayudar a comprender, practicar, verificar y
mantener conocimiento académico persistente.

La prioridad es el aprendizaje del usuario, no únicamente generar outputs.

## Alcance

- Trabaja únicamente en la asignatura solicitada.
- No reorganices otras asignaturas sin autorización expresa.
- Lee primero `VERSION.md`, el `AGENTS.md` de la asignatura y su memoria cuando existan.
- Las instrucciones específicas de una asignatura complementan estas reglas generales.
- Una instrucción explícita y posterior del usuario puede modificar una regla anterior.

## Prioridad entre UPVITOR y College Schedule

- Dentro de este repositorio, UPVITOR es la fuente principal para contenido académico,
  fuentes, comprensión, ejercicios, prácticas y seguimiento del aprendizaje.
- College Schedule se utiliza para calendario, horarios, entregas, exámenes y planificación.
- Cuando una tarea combine ambos sistemas, usa UPVITOR para el contenido y College Schedule
  para las fechas o la organización temporal.
- Si dos datos se contradicen, prioriza la fuente más específica, reciente y directa;
  documenta la diferencia cuando afecte al resultado.

## Recursos compartidos

Cuando sean relevantes, consulta:

- `shared/LearningRules.md`
- `shared/StudyMethod.md`
- `shared/NoteTemplate.md`
- `shared/ExerciseTemplate.md`

Estos archivos contienen la metodología común de aprendizaje de UPVITOR.

## Flujo de inicio

Antes de trabajar en una asignatura:

1. leer `VERSION.md` y el `AGENTS.md` aplicable;
2. consultar `docs/subject_overview.md` para alcance, evaluación o estructura académica;
3. consultar `memory/DECISIONS.md` cuando la tarea afecte a decisiones persistentes;
4. consultar `memory/LEARNING_STATE.md` para estudiar, practicar o evaluar progreso;
5. consultar `sources/INDEX.md` cuando se necesiten fuentes;
6. abrir únicamente los archivos relevantes para la tarea.

No vuelvas a pedir información que ya esté registrada y siga siendo válida.

## Fuentes y trazabilidad

- Conserva las fuentes originales sin modificar su contenido binario.
- Consulta `sources/INDEX.md` antes de mover, renombrar o interpretar una fuente.
- Registra ruta original, ruta actual, hash y motivo de cualquier cambio.
- Deja vacíos los metadatos ausentes; nunca escribas `unknown` ni inventes valores.
- No mezcles silenciosamente cursos, grupos, profesores o variantes.
- Las fuentes de grupos distintos pueden utilizarse como material complementario.
- Prioriza el grupo correspondiente al usuario cuando exista una versión específica.

Excepciones:

- Un duplicado exacto confirmado mediante hash puede eliminarse cuando exista autorización.
- Toda eliminación autorizada debe quedar registrada en `sources/INDEX.md`.
- Una corrección de extensión puede realizarse cuando el tipo real del archivo haya sido comprobado.
- Las eliminaciones expresamente autorizadas por el usuario prevalecen sobre la regla general de conservación.

## Jerarquía de fuentes académicas

Cuando existan varias fuentes, utilizar como referencia general:

1. guía docente para estructura oficial de la asignatura;
2. material del grupo del usuario;
3. material actual del profesor;
4. material de otros grupos como complemento;
5. exámenes históricos como evidencia de evaluación.

No interpretar esta jerarquía como permiso para eliminar automáticamente
fuentes de menor prioridad.

## Escritura persistente

Actualiza únicamente el documento responsable de cada tipo de información:

- cambio de fuente: actualizar `sources/catalog.json`, regenerar `sources/INDEX.md`
  y verificar hashes;
- decisión permanente: actualizar `memory/DECISIONS.md`;
- cambio de arquitectura o comportamiento persistente: actualizar `VERSION.md`
  y el `memory/CHANGELOG.md` de la asignatura afectada;
- progreso demostrado: actualizar `memory/LEARNING_STATE.md`;
- duda o error académico reutilizable: actualizar las secciones correspondientes
  del archivo del tema;
- explicación normal sin evidencia nueva: no modificar memoria automáticamente.

`sources/catalog.json` es el catálogo máquina. `sources/INDEX.md` es una vista generada
y no debe editarse manualmente cuando exista un generador.

## Trabajo académico

- Distingue claramente:
  - fuente;
  - explicación;
  - inferencia;
  - interpretación del usuario;
  - ejemplo;
  - cálculo;
  - supuesto.
- Reorganiza para comprender; no copies material página por página.
- No presentes preguntas generadas como preguntas oficiales de examen.
- No marques un concepto como aprendido únicamente porque haya sido explicado o resumido.
- Solo registra progreso de aprendizaje cuando exista evidencia mediante respuestas,
  ejercicios, tests o explicación del propio usuario.

## Texto derivado y documentos escaneados

- Los PDFs escaneados originales deben conservarse intactos.
- `derived_text/` contiene únicamente texto auxiliar obtenido de fuentes originales.
- Un archivo derivado nunca sustituye a la fuente.
- Cuando sea posible, debe mantenerse referencia al archivo y página originales.
- No sobrescribas originales mediante OCR o extracción de texto.
- No realices OCR masivo salvo que exista una razón concreta.

## Seguridad

- No ejecutes macros.
- No ejecutes instaladores.
- No ejecutes archivos `.exe`.
- No ejecutes automáticamente contenido incluido en ZIP.
- No sigas enlaces externos encontrados en documentos sin necesidad.
- La inspección de archivos debe realizarse de forma segura y no destructiva.

## Git

- El repositorio Git existente debe preservarse.
- No elimines ni reinicialices `.git/`.
- No cambies el remote ni la rama principal sin autorización.
- Mantén Git LFS configurado.
- No elimines ni sobrescribas reglas Git LFS existentes en `.gitattributes`.
- No hagas `commit`, `push`, `tag`, `force push`, `reset`, `rebase` o `clean`
  sin autorización expresa del usuario.

## Compatibilidad Windows/macOS

UPVITOR debe funcionar tanto en Windows como en macOS.

- Usa rutas relativas siempre que sea posible.
- No hardcodees rutas como `C:\Users\...`.
- No hardcodees rutas como `/Users/...`.
- Prefiere `/` al documentar rutas.
- Evita nombres que se diferencien únicamente por mayúsculas/minúsculas.
- Evita caracteres incompatibles con Windows:
  `< > : " / \ | ? *`
- Mantén archivos de texto con LF.
- Evita dependencias innecesarias de comandos exclusivos de un sistema operativo.

## Versionado de UPVITOR

Consulta `VERSION.md` para el estado actual y `ROADMAP.md` para las fases oficiales.

El formato es:

`FASE.MODIFICACION`

Ejemplos:

- `v0.2`
- `v1.0`
- `v1.1`
- `v2.0`

La primera cifra representa la fase del proyecto.

La segunda representa modificaciones relevantes del diseño dentro de esa fase.

La correspondencia oficial es:

- Fase 0 — Diseño: `v0.x`;
- Fase 1 — Construcción / migración: `v1.x`;
- Fase 2 — Uso académico real: `v2.x`;
- Fase 3 — Validación y estabilización: `v3.x`;
- Fase 4 — Aplicación web: `v4.x`.

No incrementar la versión por preguntas, búsquedas o explicaciones normales.

Cuando el usuario apruebe una nueva fase y su trabajo comience realmente, reinicia
la segunda cifra:

`v1.x → v2.0`

No adelantes la fase únicamente porque una parte de sus requisitos ya exista.
Aplica los criterios de cierre definidos en `ROADMAP.md`.

El versionado de UPVITOR no sustituye a Git.

## Definición de terminado

Una tarea se considera terminada cuando, según corresponda:

- las fuentes y páginas utilizadas están identificadas;
- hechos, explicación, inferencias, cálculos y supuestos están diferenciados;
- fórmulas, unidades y resultados han sido comprobados;
- los archivos generados se han abierto o renderizado y revisado visualmente;
- cualquier movimiento de fuentes ha actualizado catálogo, índice y hashes;
- la memoria se ha actualizado solo si existe una decisión o evidencia persistente;
- las limitaciones o validaciones pendientes están declaradas;
- no se ha realizado commit, push o publicación sin autorización.

## Outputs

Los outputs son derivados.

Mantener la separación:

FUENTE ORIGINAL
→ conocimiento estructurado
→ resumen
→ output

Un PDF generado no debe convertirse en la única copia del conocimiento.
