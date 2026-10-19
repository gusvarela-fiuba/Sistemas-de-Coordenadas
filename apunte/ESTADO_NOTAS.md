## Capítulos cerrados que ganarían con más espacio

Criterio vigente desde la fase G: no hay límite de páginas. Un capítulo ya cerrado que ganaría con más explicación, figuras o ejemplos se anota acá y no se reabre sin aprobación.

- Capítulo 12 (cerrado en 607073e con el criterio anterior de ~265 págs.): quedan 10,5 términos de campo cada 100 líneas, casi todos «residuo» y «Helmert» en enunciados y títulos; las dos demostraciones movidas a «En profundidad» están completas. Candidato a reabrir si el editor quiere más ejemplos resueltos.
- Capítulo 15 (cerrado en 2be3810 con el criterio anterior): dos demostraciones movidas a «En profundidad» completas; tres figuras en el capítulo. Candidato a reabrir si el editor quiere figuras del triángulo polar o de la loxodromia.
- Capítulo 11 (cerrado en fb92d8c con el criterio anterior): demostración de la adjugada en «En profundidad» completa; 4,1 términos de campo cada 100 líneas, lo que queda está en enunciados, ejemplos y consignas de unidades.

## Complementos C1 a C4 (E2, cerrados el 2026-10-19 con voz para el aula)

Los cuatro cumplen el mínimo del molde. Cada uno tiene su script `apunte/scripts/cN_*.py`, que calcula y verifica con `assert` todos los números que el texto cita; los datos son sintéticos y declarados como tales, salvo lo que se pide a `pyproj` 3.8.0 (PROJ 9.8.1), que el texto declara explícitamente (C2: factor de escala en EPSG:5347 con `get_factors`; C4: parámetros de las fajas EPSG:5343 a 5349 y la transformación EPSG:4694 → EPSG:5340).

Para decidir por el editor:

- C4: el primer dígito de la coordenada Este de Gauss-Krüger es el número de la faja (pedido del editor, resuelto acá con un ejemplo calculado por `pyproj`). La transformación POSGAR 94 → POSGAR 2007 que aplica `pyproj` es una traslación geocéntrica de unos 0,6 m con incertidumbre declarada de 1,5 m; el texto lo cuenta tal cual y una caja aclara que no es una corrección oficial. La caja heredada «La composición como operación central» (hace falta conmutatividad para construir un sistema de coordenadas) es dudosa y conviene revisarla.
- C2: el script viejo `capc2_conformes.py` se retiró por decisión del editor (reemplazado por `c2_conformes.py`). El enlace heredado a la unidad `15_transformaciones_conformes` dice «Unidad 19»: revisar la numeración.
- C1: los escalares de las columnas del patrón del pentágono siguen escritos con \(\lambda\) (no son autovalores); pasar a \(\mu_i\) si se quiere la convención estricta.
- C3: «Copernicus DEM GLO-30» cuenta como término de campo por la sigla, pero el crédito de la figura lo exige.
