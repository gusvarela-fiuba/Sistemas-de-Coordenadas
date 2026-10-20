# matriz2x2.py — adjugada, determinante e inversa de una matriz 2x2
# (port fiel de julia/matriz2x2.jl; misma salida de texto, misma figura)
#
# Para A = [a b; c d]:
#   det(A)  = a*d - b*c
#   cof(A)  = [ d -c; -b a ]        (matriz de cofactores)
#   adj(A)  = cof(A)'  = [ d -b; -c a ]   (adjugada = traspuesta de los cofactores)
#   inv(A)  = adj(A) / det(A)       (solo si det(A) != 0)
#
# Correr desde esta carpeta:  uv run python matriz2x2.py
#
# ==============================================================================
# GUÍA DIDÁCTICA DE PYTHON, NUMPY Y MATPLOTLIB
# ==============================================================================
# 1. Indexación base 0 vs. base 1 (Julia / MATLAB):
#    En Julia se escribe `A[1, 1]`, `A[1, 2]`, `A[2, 1]`, `A[2, 2]`. En Python
#    los índices empiezan en 0: `A[0, 0]`, `A[0, 1]`, `A[1, 0]`, `A[1, 1]`.
# 2. Transpuesta y producto matricial en NumPy:
#    - `.T` transpone un arreglo 2D (`cofactores2x2(A).T`, equivalente a `'` en
#      Julia/MATLAB para matrices reales).
#    - `@` es el producto de matrices (`A @ Ainv`). El operador `*` en NumPy
#      multiplica coordenada a coordenada (producto de Hadamard, como `.*`).
# 3. Valor especial `None`:
#    Cuando `det(A) == 0`, `inversa2x2(A)` devuelve `None` (el equivalente a
#    `nothing` en Julia) y lo chequeamos con `if Ainv is None:`.
# 4. Comparación en punto flotante (`np.allclose`):
#    En vez de comparar matrices con `==` (que fallaría por redondeos de 10⁻¹⁶),
#    `np.allclose(Ainv, np.linalg.inv(A))` verifica que coincidan dentro de la
#    tolerancia numérica estándar.
# ==============================================================================

from pathlib import Path

import numpy as np                  # numpy.linalg solo para verificar contra inv() de la librería
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt     # para la grilla de rectas paralelas (sección final)


def cofactores2x2(A):
    """Matriz de cofactores de una 2x2."""
    a, b = A[0, 0], A[0, 1]
    c, d = A[1, 0], A[1, 1]
    return np.array([[ d, -c],
                     [-b,  a]])


def adjugada2x2(A):
    """Adjugada de una 2x2: traspuesta de la matriz de cofactores."""
    return cofactores2x2(A).T


def determinante2x2(A):
    """Determinante de una 2x2 por la regla a*d - b*c."""
    return A[0, 0] * A[1, 1] - A[0, 1] * A[1, 0]


def inversa2x2(A):
    """Inversa de una 2x2 vía adj(A)/det(A). Devuelve `None` si es singular."""
    Δ = determinante2x2(A)
    if Δ == 0:
        return None
    return adjugada2x2(A) / Δ


# --- Impresión al estilo `display` de Julia (6 cifras significativas, columnas
#     alineadas por el punto decimal), para que la salida sea comparable 1:1. ---

def _num(x):
    s = f"{x:.6g}"
    if "e" not in s and "." not in s:
        s += ".0"
    return s


def mostrar_matriz(M, tipo="Matrix{Float64}"):
    n, m = M.shape
    print(f"{n}×{m} {tipo}:")
    celdas = [[_num(x) for x in fila] for fila in M]
    partes = [[c.split(".") for c in fila] for fila in celdas]
    wl = [max(len(partes[i][j][0]) for i in range(n)) for j in range(m)]
    wr = [max(len(partes[i][j][1]) for i in range(n)) for j in range(m)]
    for i in range(n):
        cols = [partes[i][j][0].rjust(wl[j]) + "." + partes[i][j][1].ljust(wr[j]) for j in range(m)]
        print((" " + "  ".join(cols)).rstrip())


def mostrar(A):
    print("A =")
    mostrar_matriz(A)
    Δ = determinante2x2(A)
    print(f"\ndet(A) = {A[0, 0]}·{A[1, 1]} − {A[0, 1]}·{A[1, 0]} = {Δ}")
    print("\nCofactores de A =")
    mostrar_matriz(cofactores2x2(A))
    print("\nadj(A) = cofactores' =")
    mostrar_matriz(adjugada2x2(A), tipo="transpose(::Matrix{Float64}) with eltype Float64")
    Ainv = inversa2x2(A)
    if Ainv is None:
        print("\nA es singular (det = 0): no tiene inversa.")
    else:
        print("\ninv(A) = adj(A) / det(A) =")
        mostrar_matriz(Ainv)
        print("\nVerificación A · inv(A) =")
        mostrar_matriz(A @ Ainv)
        print("\n¿Coincide con numpy.linalg.inv? ", np.allclose(Ainv, np.linalg.inv(A)), sep="")
    print()


# --- Programa principal ---
A = np.array([[ 1.2, 0.5],
              [-0.1, 1.3]])

mostrar(A)

# --- Gráfico: rectas paralelas a u y v, antes y después de multiplicar por inv(A) ---
#
# Idea geométrica: la recta paralela a u que pasa por P es  r(t) = P + t·u.
# Tomando P_k = k·v (múltiplos del OTRO vector) las paralelas a u quedan igualmente
# espaciadas y, junto con las paralelas a v que pasan por k·u, forman la grilla
# oblicua de la base {u, v}. Cada nodo es un punto a·u + b·v con a, b enteros.
#
# Como inv(A) es lineal, manda rectas en rectas y paralelas en paralelas: la grilla
# de {u, v} se transforma en la grilla de {inv(A)·u, inv(A)·v}. Cambia el ángulo
# entre las familias y el espaciado, pero no la estructura de grilla. El área de
# cada paralelogramo se multiplica por det(inv(A)) = 1/det(A).

u = np.array([ 1.0, 1.0])
v = np.array([-1.0, 2.0])

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


Ainv = inversa2x2(A)
if Ainv is None:
    print("A es singular: no se puede graficar la grilla transformada por inv(A).")
else:
    u2 = Ainv @ u
    v2 = Ainv @ v
    print("inv(A)·u = ", fmt(u2), sep="")
    print("inv(A)·v = ", fmt(v2), sep="")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7))
    grilla(ejes(ax1, "Base {u, v}"), u, v)
    grilla(ejes(ax2, "Base {inv(A)·u, inv(A)·v}"), u2, v2, nombre_u="inv(A)·u", nombre_v="inv(A)·v")
    for ax in (ax1, ax2):
        ax.legend(loc="upper left", fontsize=8)
    fig.subplots_adjust(left=0.03, right=0.99, top=0.93, bottom=0.04, wspace=0.08)

    salida = Path(__file__).resolve().parent / "matriz2x2_rectas.png"
    fig.savefig(salida, dpi=100)
    print("Gráfico guardado en ", salida, sep="")
