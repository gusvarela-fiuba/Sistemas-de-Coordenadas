# Ejercicio del 30/9/2026 en Julia — formas lineales y cambio de base

Resolución propia (Gustavo, 2026-09-30, antes en `~/julia/`) del ejercicio de la clase del 30/9: formas lineales (1,1) y (−1,2), matriz `A = [1.2 0.5; −0.1 1.3]`.

- `matriz2x2.jl`: cofactores, adjunta, determinante e inversa de una 2×2 a mano, verificadas contra `LinearAlgebra`; después dibuja la grilla oblicua de la base {u, v} (paralelas a u por k·v y paralelas a v por k·u) y la misma grilla transformada por inv(A). Salida `matriz2x2_rectas.png`.
- `rectas_paralelas.jl`: sólo la parte gráfica, con inv(A) calculada inline. Salida `rectas_paralelas.png`.

Hecho geométrico que muestran: una transformación lineal manda rectas en rectas y paralelas en paralelas; la grilla de {u, v} pasa a ser la grilla de {inv(A)·u, inv(A)·v}, cambian ángulo y espaciado, no la estructura; el área de cada paralelogramo se multiplica por 1/det(A). Las familias de paralelas son las curvas de nivel de las formas lineales.

Correr (Julia 1.12 con Plots): `julia matriz2x2.jl`. Es el insumo de la unidad `08_cambio_de_base` (pendiente, molde v2).
