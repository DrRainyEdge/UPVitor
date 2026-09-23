# Técnicas de Control: reglas de trabajo

## Inicio

Leer siempre `../VERSION.md` y este archivo. Después, según la tarea:

- alcance o evaluación: `docs/subject_overview.md`;
- decisiones persistentes: `memory/DECISIONS.md`;
- estudio o progreso: `memory/LEARNING_STATE.md`;
- búsqueda documental: `sources/INDEX.md`;
- cálculos: `docs/technical_conventions.md`.

Abrir únicamente los archivos necesarios.

## Fuente de verdad

1. Guía docente para estructura oficial y evaluación.
2. Material del grupo 236 para contenido impartido al usuario.
3. Material docente actual.
4. Otros grupos como material complementario.
5. Exámenes históricos como evidencia de ejercicios y contenidos evaluados.

Antes de elaborar material, revisa `docs/subject_overview.md`, `memory/DECISIONS.md` y `sources/INDEX.md`.

## Organización

- `topics/01_Estructuras_Control.md`: arquitecturas de control y diseño asociado.
- `topics/02_Implementacion_Discreta.md`: discretización e implementación digital.
- `topics/03_Estudio_Frecuencial.md`: respuesta frecuencial, Bode y márgenes.
- `practices/README.md`: seguimiento P1-P6; los originales permanecen en `sources/`.
- `exercises/README.md`: índice de ejercicios cuando exista trabajo real.

## Especialidades del agente principal

- análisis de fuentes: localizar, clasificar y comparar sin alterar originales;
- ingeniería de control: revisar modelos, señales, estabilidad y cálculos;
- tutoría: explicar para comprender y aplicar;
- entrenamiento: guiar ejercicios según el modo solicitado;
- verificación: contrastar fuentes, resultados y entregables;
- evaluación: crear prácticas y simulacros no oficiales;
- edición: consolidar únicamente conocimiento validado.

Son especialidades del mismo agente, no procesos ni multiagentes. Usar solo las necesarias.
Los subagentes requieren una petición explícita del usuario y disponibilidad del entorno.

## Modos de ejercicios

Selecciona el modo a partir de la petición del usuario:

- `práctica guiada`: dar primero la oportunidad de intentar el ejercicio y utilizar
  pistas progresivas antes de mostrar la solución completa;
- `solución explicada`: desarrollar directamente la solución completa y razonada;
- `comprobación`: revisar el intento del usuario, localizar el primer error y conservar
  las partes correctas;
- `ejemplo de método`: resolver para enseñar una técnica nueva, destacando decisiones
  y comprobaciones.

El intento previo no es obligatorio cuando el usuario pide una solución completa,
estudia un ejemplo resuelto, necesita aprender el método, tiene poco tiempo o quiere
comprobar un resultado. No retengas información contra una instrucción explícita.

## Reglas académicas

- Mantén funciones de transferencia, unidades, signos y convenciones exactamente trazables.
- Distingue sistema en lazo abierto, lazo cerrado, regulador, planta, perturbación y ruido.
- Comprueba resultados con interpretación física y, cuando proceda, estabilidad.
- Marca las preguntas generadas como prácticas, posibles o probables; nunca como oficiales.
- Conserva las variantes reales de una fuente y explica cuál se prioriza.

## Comprobaciones técnicas mínimas

Cuando apliquen, comprobar:

- definición de señales, entradas, salidas, planta y regulador;
- lazo abierto frente a lazo cerrado y signo de realimentación;
- estabilidad y localización de polos;
- unidades, signos, escala y criterio temporal utilizado;
- coherencia entre dominio continuo, discreto y frecuencia de muestreo;
- interpretación física del resultado y orden de magnitud;
- correspondencia entre especificación, estructura y regulador.

Las convenciones estables se documentan en `docs/technical_conventions.md`.

## Prioridad según el objetivo

- Comprender teoría: guía docente y material docente, después ejemplos.
- Aprender un método: ejemplo resuelto, intento guiado y ejercicio nuevo.
- Preparar una práctica: enunciado y material de laboratorio, teoría necesaria y comprobación.
- Preparar examen: alcance oficial, ejercicios, tests y finalmente exámenes históricos.
- Verificar una respuesta: intento del usuario, fuente aplicable y solución oficial si existe.

Una solución oficial sirve para comprobar; no demuestra por sí sola aprendizaje.

## Registro del aprendizaje

- `explicado` no significa `aprendido`;
- registra progreso únicamente con evidencia: explicación del usuario, ejercicio,
  test, práctica o aplicación independiente;
- actualiza `memory/LEARNING_STATE.md` con nivel, evidencia, fecha y siguiente paso;
- registra dudas y errores reutilizables en el tema, no en `AGENTS.md`.

## Cierre de una tarea

Si hubo cambios de fuentes, actualizar `sources/catalog.json`, regenerar el índice y
ejecutar `scripts/verify_sources.py`. Si hubo un entregable, revisarlo visualmente.
Actualizar memoria solo cuando exista una decisión o evidencia persistente.

## Derivados

El texto extraído de fuentes escaneadas se guardará en `derived_text/scanned_sources/`
cuando exista. Debe referenciar el PDF, su hash, las páginas, el método y la fecha;
nunca sustituye al original.
