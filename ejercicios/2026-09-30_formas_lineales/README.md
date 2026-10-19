# Ejercicio del 30/9/2026 — formas lineales y cambio de base

Resolución propia (Gustavo, 2026-09-30) del ejercicio del 30/9: formas lineales (1,1) y (−1,2), matriz `A = [1.2 0.5; −0.1 1.3]`, u = (1,1), v = (−1,2).

Versión viva: los `.py` de esta carpeta (numpy + matplotlib). Los `.jl` originales (Julia 1.12 con Plots, antes en `~/julia/`) quedan en `julia/` como referencia; los `.py` son ports fieles, con la misma salida de texto y la misma figura.

- `matriz2x2.py`: cofactores, adjugada, determinante e inversa de una 2×2 a mano (`cofactores2x2`, `adjugada2x2`, `determinante2x2`, `inversa2x2`, `mostrar`), verificadas contra `numpy.linalg.inv`; después dibuja la grilla oblicua de la base {u, v} (paralelas a u por k·v y paralelas a v por k·u) y la misma grilla transformada por inv(A). Salida `matriz2x2_rectas.png`.
- `rectas_paralelas.py`: sólo la parte gráfica, con inv(A) calculada inline. Salida `rectas_paralelas.png`.
- `julia/matriz2x2.jl`, `julia/rectas_paralelas.jl`: los originales. Escriben sus PNG en `julia/`.

Hecho geométrico que muestran: una transformación lineal manda rectas en rectas y paralelas en paralelas; la grilla de {u, v} pasa a ser la grilla de {inv(A)·u, inv(A)·v}, cambian ángulo y espaciado, no la estructura; el área de cada paralelogramo se multiplica por 1/det(A). Las familias de paralelas son las curvas de nivel de las formas lineales.

Números de referencia (iguales en Julia y Python): det(A) = 1.61; inv(A) = [0.807453 −0.310559; 0.0621118 0.745342]; inv(A)·u = [0.497, 0.807]; inv(A)·v = [−1.429, 1.429]. La única diferencia de salida es el producto A·inv(A): Julia imprime la identidad exacta y numpy deja un 2·10⁻¹⁸ fuera de la diagonal (roundoff del BLAS).

Correr desde esta carpeta: `uv run python matriz2x2.py` y `uv run python rectas_paralelas.py` (referencia Julia: `cd julia && julia matriz2x2.jl`, la primera corrida de Plots tarda ~1 min). Es el insumo de la unidad `08_cambio_de_base` (pendiente, molde v2).
