# Revisión semántica — capítulo 10 (Derivada y aproximación lineal): divergencia

Resumen: sin errores graves; la subsección nueva es correcta y coherente con el capítulo 7; dos menores (falta de etiqueta y precisión de «sin cambiar de área»).

Alcance: `apunte/contenido/10-derivada-aproximacion-lineal.tex` líneas 507-528 (`\subsection{La traza del jacobiano: divergencia de un campo de desplazamientos}` y su recuadro «La divergencia mide cuánto se expande el terreno…»).

## Verificado sin hallazgos
- Procedencia/voz: sin menciones personales ni de curso. («ya lo vimos en el capítulo~\ref{cap:formas-lineales}», línea 30, es una remisión interna al apunte, en una zona no modificada.)
- Matemática: el jacobiano de `x↦x+εu(x)` es `I+εJ`; el factor local de área es `det(I+εJ)=1+ε trJ+O(ε²)` por `prop:traza-derivada-det`; `tr J=∂u_E/∂E+∂u_N/∂N`; si `u` es afín, `J` es constante y coincide con `F-I` de `sec:aplicacion-deformacion`, de modo que la divergencia es la dilatación, la parte simétrica el tensor de deformación y la antisimétrica el giro sin efecto en el área. Todas las afirmaciones son correctas. Remisiones verificadas: `sec:metrica`, `ap:infinitesimales`, `cap:autovectores`, `sec:aplicacion-deformacion`, `prop:traza-derivada-det` (existen).
- No hay demostraciones propias, números ni script asociado en esta subsección; no hay recuadro `\unidadInteractiva` en la parte nueva (los de las líneas 62 y 348 son anteriores; verificados contra `unidades/10_jacobiano_primera_forma.py`: casos «la loma…» con punto inicial `(2,1)`, «plano inclinado z = 1 + 0.4u + 0.3v», deslizadores `du,dv`, y `E=1,16`, `F=0,12`, `G=1,09`).
- Notación: coherente con el capítulo 0 (`μ` para autovalores en este capítulo; `J` para jacobiano).

## Hallazgos

1. **menor** — `10-derivada-aproximacion-lineal.tex:507`: la `\subsection` de la divergencia no lleva `\label`, a diferencia de las vecinas (`sec:plano-superficie`, `sec:aplicacion-radiacion`). El cuadro «Qué mide cada operación» del capítulo 0 remite a secciones para la traza y no podrá citar esta. Propuesta: `\label{sec:divergencia}` y agregarla a la celda «Traza» del cuadro (`tab:operaciones`, columna «Sec.»).

2. **menor** — `10-derivada-aproximacion-lineal.tex:523-527`: «nula, sólo se deforma o gira sin cambiar de área». Divergencia nula implica área conservada sólo a primer orden (el término `ε²det J` puede ser no nulo, como muestra el capítulo 7 con traza 0 y `det E=-1`: área 0,99). Propuesta: «nula, el área no cambia a primer orden: el terreno sólo se deforma (a volumen constante) o gira». Conviene que la subsección enlace el ejemplo de traza cero del capítulo 7 (`fig:traza-area`, segunda matriz).
