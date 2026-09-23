# Convenciones técnicas

Estas convenciones mantienen consistencia en explicaciones y cálculos. Son reglas de trabajo de UPVITOR, no sustituyen la notación de una fuente oficial. Si una fuente usa otra convención, debe indicarse explícitamente.

## Variables y dominios

- `s`: variable compleja del dominio continuo.
- `z`: variable compleja del dominio discreto.
- `k`: índice de muestra.
- `T_s`: periodo de muestreo, expresado en segundos salvo indicación contraria.
- `ω`: frecuencia angular en rad/s.
- `f`: frecuencia en Hz; usar `ω = 2πf` al convertir.

No mezclar modelos continuos y discretos sin declarar el método de transformación y `T_s`.

## Diagramas y realimentación

- Identificar referencia, error, acción de control, salida, perturbación y ruido.
- Indicar si la realimentación es negativa o positiva.
- No asumir realimentación unitaria cuando el diagrama muestre un sensor o bloque distinto.
- Definir la función de lazo utilizada antes de calcular márgenes.

## Frecuencia y Bode

- Magnitud en decibelios: `20*log10(|G(jω)|)` para funciones de transferencia de amplitud.
- Fase en grados salvo que la fuente utilice radianes.
- Frecuencias de cruce y márgenes se calculan sobre la función de lazo declarada.
- Señalar aproximaciones gráficas y diferenciar lectura de Bode de cálculo analítico.

## Respuesta temporal y estabilidad

- Declarar el criterio de tiempo de establecimiento, por ejemplo 2 % o 5 %; no asumirlo.
- Indicar condiciones iniciales cuando afecten al resultado.
- Comprobar polos de la representación relevante: plano `s` o plano `z`.
- No equiparar estabilidad, rapidez y robustez.

## Reguladores y estructuras

- Distinguir regulador, planta, sensor, prefiltro y compensadores auxiliares.
- Separar seguimiento de referencia de rechazo de perturbaciones.
- Indicar qué señal es medible y dónde entra cada perturbación.
- En estructuras 2DoF, cascada, prealimentación o predictor de Smith, definir cada lazo antes de simplificar bloques.

## Presentación de resultados

- Mantener unidades en datos, pasos intermedios y resultado.
- Indicar redondeos y conservar precisión suficiente durante el cálculo.
- Comprobar signo, orden de magnitud, estabilidad e interpretación física.
- Diferenciar resultado exacto, aproximación, lectura gráfica y simulación.
