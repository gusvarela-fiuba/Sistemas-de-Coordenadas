"""Números y figura de la subsección «El conjugado armónico» (complemento «Transformaciones
proyectivas»).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  H1  Conjugado armónico en la recta: A = 0, B = 6, C = 4; D despejado de (A,B;C,D) = -1;
      comprobación de la razón doble.
  H2  Construcción con el cuadrilátero completo en el plano: A = (0,0), B = (6,0), C = (4,0),
      L = (2, 4) fuera de la recta, K = (3, 2) punto medio de LC; M = BK ∩ LA, N = AK ∩ LB,
      D = MN ∩ AB, todo con productos cruz en coordenadas homogéneas.
  H3  Invariancia: imágenes de 0, 6, 4, 12 por la homografía f(x) = (2x+1)/(x+3) del ejemplo
      de la razón doble y razón doble de las imágenes.
  H4  Punto medio y punto impropio: (0, 6; 3, d) para d grande tiende a -1.

Figura (PNG, fondo blanco, dpi 150) en apunte/figuras/proyectivas/:
  c1_conjugado_armonico.png   cuadrilátero completo L, M, N, K con A, B, C, D sobre la recta.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/capc1_conjugado_armonico.py
"""
from fractions import Fraction as F
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "proyectivas"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, INK = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#222222"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})


def razon_doble(a, b, c, d):
    return (c - a) * (d - b) / ((c - b) * (d - a))


# ---------------------------------------------------------------- H1
a, b, c = F(0), F(6), F(4)
# (c-a)(d-b) = -(c-b)(d-a)  =>  d [(c-a)+(c-b)] = b(c-a) + a(c-b)
d = (b * (c - a) + a * (c - b)) / ((c - a) + (c - b))
print(f"H1  A = {a}, B = {b}, C = {c}  ->  D = {d}   (A,B;C,D) = {razon_doble(a, b, c, d)}")

# ---------------------------------------------------------------- H2
h = lambda p: np.array([p[0], p[1], 1.0])
af = lambda q: q[:2] / q[2]
A, B, C = np.array([0.0, 0]), np.array([6.0, 0]), np.array([4.0, 0])
L = np.array([2.0, 4.0])
K = (L + C) / 2
M = af(np.cross(np.cross(h(B), h(K)), np.cross(h(L), h(A))))
N = af(np.cross(np.cross(h(A), h(K)), np.cross(h(L), h(B))))
D = af(np.cross(np.cross(h(M), h(N)), np.cross(h(A), h(B))))
for nom, P in (("L", L), ("M", M), ("N", N), ("K", K), ("D", D)):
    print(f"H2  {nom} = ({P[0]:.4f}, {P[1]:.4f})")
print(f"H2  (A,B;C,D) con la abscisa = {razon_doble(A[0], B[0], C[0], D[0]):.6f}")
assert abs(D[0] - float(d)) < 1e-9 and abs(D[1]) < 1e-12

# ---------------------------------------------------------------- H3
f = lambda x: (2 * x + 1) / (x + 3)
im = [f(F(x)) for x in (a, b, c, d)]
print("H3  f(0), f(6), f(4), f(12) =", ", ".join(str(x) for x in im),
      "  razón doble =", razon_doble(*im))

# ---------------------------------------------------------------- H4
for dd in (F(10**3), F(10**6)):
    print(f"H4  (0, 6; 3, {dd}) = {float(razon_doble(F(0), F(6), F(3), dd)):.6f}")

# ---------------------------------------------------------------- figura
fig, ax = plt.subplots(figsize=(7.6, 3.6))


def recta(P, Q, t0=-0.15, t1=1.15, **kw):
    T = np.array([t0, t1])
    ax.plot(P[0] + T * (Q[0] - P[0]), P[1] + T * (Q[1] - P[1]), **kw)


ax.axhline(0, color=TEAL, linewidth=1.2)
recta(L, A, -0.08, 1.12, color=GRIS, linewidth=1)
recta(L, B, -0.08, 1.08, color=GRIS, linewidth=1)
recta(L, C, -0.08, 1.12, color=GRIS, linewidth=1)
recta(A, N, -0.08, 1.15, color=GRIS, linewidth=1)
recta(B, M, -0.08, 1.15, color=GRIS, linewidth=1)
recta(M, D, -0.08, 1.04, color=RUST, linewidth=1.2, linestyle="--")
for nom, P, col, off in (("A", A, TEAL, (-0.1, -0.45)), ("B", B, TEAL, (-0.1, -0.45)),
                         ("C", C, TEAL, (-0.1, -0.45)), ("D", D, RUST, (-0.1, -0.45)),
                         ("L", L, INK, (0.12, 0.08)), ("M", M, INK, (-0.45, 0.05)),
                         ("N", N, INK, (0.12, 0.1)), ("K", K, INK, (-0.15, -0.5))):
    ax.plot(*P, "o", color=col, markersize=4.5)
    ax.text(P[0] + off[0], P[1] + off[1], f"${nom}$", color=col, fontsize=11)
ax.text(6.8, 3.4, r"$(A,B;C,D)=\frac{(4-0)(12-6)}{(4-6)(12-0)}=-1$", fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-1, 13); ax.set_ylim(-0.8, 4.6)
ax.set_xticks(range(0, 13, 2)); ax.set_yticks([0, 2, 4])
ax.spines[["top", "right"]].set_visible(False)
fig.tight_layout()
fig.savefig(SALIDA / "c1_conjugado_armonico.png", dpi=150, metadata={"Software": None})
plt.close(fig)
print("figura:", SALIDA / "c1_conjugado_armonico.png")
