# rectas_paralelas.py — familias de rectas paralelas a u = [1, 1] y v = [-1, 2],
# y las mismas familias después de multiplicar por inv(A), con A la de matriz2x2.py.
# (port fiel de julia/rectas_paralelas.jl: sólo la figura, inv(A) calculada inline)
#
# Idea geométrica: la recta paralela a u que pasa por P es  r(t) = P + t·u.
# Tomando P_k = k·v (múltiplos del OTRO vector) las paralelas a u quedan igualmente
# espaciadas y, junto con las paralelas a v que pasan por k·u, forman la grilla
# oblicua de la base {u, v}. Cada nodo es un punto a·u + b·v con a, b enteros.
#
# Como inv(A) es lineal, manda rectas en rectas y paralelas en paralelas: la grilla
# de {u, v} se transforma en la grilla de {inv(A)·u, inv(A)·v}. Cambia el ángulo
# entre las familias y el espaciado, pero no la estructura de grilla.
#
# Correr desde esta carpeta:  uv run python rectas_paralelas.py
#
# ==============================================================================
# GUÍA DIDÁCTICA DE PYTHON, NUMPY Y MATPLOTLIB
# ==============================================================================
# 1. Indexación base 0: en Python los índices arrancan en 0 (`A[0, 0]` es la
#    primera fila y primera columna; `u[0]` y `u[1]` son las componentes x e y).
# 2. Producto matricial `@` vs. producto elemento a elemento `*`:
#    `Ainv @ u` multiplica la matriz 2×2 por el vector `u`, mientras que
#    `t * u[0]` multiplica cada valor del arreglo `t` por el escalar `u[0]`.
# 3. Comprensión de listas (*list comprehension*):
#    `[a * u + b * v for a in range(...) for b in range(...)]` construye de
#    forma compacta todos los nodos de la red entera `a·u + b·v`. Nota:
#    `range(-k_max, k_max + 1)` incluye `k_max` porque en Python el límite
#    superior de `range(inicio, fin)` es abierto (no se incluye).
# 4. Slicing de columnas en NumPy:
#    `nodos[:, 0]` extrae toda la columna 0 (coordenadas x) y `nodos[:, 1]`
#    la columna 1 (coordenadas y) para graficarlas de una sola vez con `scatter`.
# ==============================================================================

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

A = np.array([[ 1.2, 0.5],
              [-0.1, 1.3]])
Ainv = np.array([[ A[1, 1], -A[0, 1]],
                 [-A[1, 0],  A[0, 0]]]) / (A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0])   # adj(A)/det(A)

u = np.array([ 1.0, 1.0])
v = np.array([-1.0, 2.0])
u2 = Ainv @ u          # ≈ [0.497, 0.807]
v2 = Ainv @ v          # ≈ [-1.429, 1.429]

k_max = 4                          # rectas a cada lado del origen
t     = np.linspace(-20, 20, 2)    # parámetro: bastan 2 puntos por recta (rango amplio para que crucen todo el cuadro)


def fmt(w):
    return "[" + ", ".join(str(round(float(x), 3)) for x in w) + "]"


def grilla(ax, u, v, nombre_u="u", nombre_v="v"):
    """Dibuja en `ax` la grilla oblicua de la base {u, v}: paralelas a u por k·v, paralelas a v por k·u."""
    # Rectas paralelas a u:  r_k(t) = k·v + t·u
    for k in range(-k_max, k_max + 1):
        ax.plot(k * v[0] + t * u[0], k * v[1] + t * u[1],
                color="steelblue", lw=2.5 if k == 0 else 1, alpha=1 if k == 0 else 0.6,
                label=f"paralelas a {nombre_u}" if k == 0 else None)
    # Rectas paralelas a v:  s_k(t) = k·u + t·v
    for k in range(-k_max, k_max + 1):
        ax.plot(k * u[0] + t * v[0], k * u[1] + t * v[1],
                color="firebrick", lw=2.5 if k == 0 else 1, alpha=1 if k == 0 else 0.6,
                label=f"paralelas a {nombre_v}" if k == 0 else None)
    # Vectores desde el origen (línea con etiqueta + punta de flecha)
    for w, color, nombre in ((u, "navy", nombre_u), (v, "darkred", nombre_v)):
        ax.plot([0, w[0]], [0, w[1]], color=color, lw=3, label=f"{nombre} = {fmt(w)}")
        ax.annotate("", xy=(w[0], w[1]), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=color, lw=3, mutation_scale=18))
    # Nodos a·u + b·v
    nodos = np.array([a * u + b * v for a in range(-k_max, k_max + 1) for b in range(-k_max, k_max + 1)])
    ax.scatter(nodos[:, 0], nodos[:, 1], s=12, color="black", zorder=3)
    return ax


def ejes(ax, tit):
    ax.set_aspect("equal")
    ax.set_xlim(-8, 8)
    ax.set_ylim(-8, 8)
    # framestyle = :origin
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    ax.spines["right"].set_visible(False)
    ax.spines["top"].set_visible(False)
    ax.set_title(tit)
    return ax


fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
grilla(ejes(ax1, "Base {u, v}"), u, v)
grilla(ejes(ax2, "Base {inv(A)·u, inv(A)·v}"), u2, v2, nombre_u="inv(A)·u", nombre_v="inv(A)·v")
for ax in (ax1, ax2):
    ax.legend(loc="upper left", fontsize=8)
fig.subplots_adjust(left=0.03, right=0.99, top=0.93, bottom=0.04, wspace=0.08)

salida = Path(__file__).resolve().parent / "rectas_paralelas.png"
fig.savefig(salida, dpi=100)
print("Guardado en ", salida, sep="")
