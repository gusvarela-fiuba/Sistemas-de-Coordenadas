"""Números y figura de la subsección «El producto mixto» (capítulo «Subespacios, producto
cuña y determinante»).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  M1  Producto mixto u·(v×w) con las columnas del ejemplo del determinante 3x3:
      u = (1,2,0), v = (0,1,1), w = (1,0,2); v×w, det[u v w], área de la base |v×w|,
      altura u·(v×w)/|v×w|, permutaciones cíclicas y un intercambio.
  M2  Aplicación «cuatro puntos relevados, ¿están en el mismo plano?»: losa relevada con
      estación total, coordenadas locales (x, y, z) en metros; producto mixto de
      P2-P1, P3-P1, P4-P1 en m³, área del paralelogramo de la base, apartamiento
      d = |mixto| / |(P2-P1)×(P3-P1)| en mm y decisión con tolerancia de 5 mm; cota del
      plano en la planimetría de P4.
  X1  Ejercicio: el mismo relevamiento con la cota de P4 leída 12,436 m.

Figura (PNG, fondo blanco, dpi 150) en apunte/figuras/cuna-determinante/:
  cuna_mixto.png   paralelepípedo de u, v, w (M1) con la base de v, w, la normal v×w y la
                   altura de u sobre la base.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap06_producto_mixto.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "cuna-determinante"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "svg.hashsalt": "cap06", "path.simplify": False})


def mixto(u, v, w):
    return float(np.dot(u, np.cross(v, w)))


# ---------------------------------------------------------------- M1
u, v, w = np.array([1.0, 2, 0]), np.array([0.0, 1, 1]), np.array([1.0, 0, 2])
vw = np.cross(v, w)
m = mixto(u, v, w)
det = np.linalg.det(np.column_stack([u, v, w]))
area = np.linalg.norm(vw)
altura = m / area
print("M1  v x w =", vw)
print(f"M1  u·(v x w) = {m:.6f}   det[u v w] = {det:.6f}")
print(f"M1  |v x w| = sqrt({vw @ vw:.0f}) = {area:.6f}   altura = {altura:.6f}   area*altura = {area*altura:.6f}")
print(f"M1  ciclicas: v·(w x u) = {mixto(v, w, u):.6f}   w·(u x v) = {mixto(w, u, v):.6f}")
print(f"M1  intercambio: v·(u x w) = {mixto(v, u, w):.6f}")
assert abs(m - det) < 1e-12 and abs(m - 4) < 1e-12

# ---------------------------------------------------------------- M2
P1 = np.array([102.315, 205.480, 12.347])
P2 = np.array([110.842, 205.912, 12.391])
P3 = np.array([110.407, 214.276, 12.472])
P4 = np.array([101.874, 213.829, 12.431])
TOL_MM = 5.0


def coplanaridad(P1, P2, P3, P4, etiqueta):
    a, b, c = P2 - P1, P3 - P1, P4 - P1
    n = np.cross(a, b)
    mx = mixto(a, b, c)
    mx_det = np.linalg.det(np.vstack([a, b, c]))
    base = np.linalg.norm(n)
    d_mm = abs(mx) / base * 1000
    z_plano = P1[2] - (n[0] * (P4[0] - P1[0]) + n[1] * (P4[1] - P1[1])) / n[2]
    print(f"{etiqueta}  P2-P1 = {a}   P3-P1 = {b}   P4-P1 = {c}")
    print(f"{etiqueta}  (P2-P1) x (P3-P1) = ({n[0]:.6f}, {n[1]:.6f}, {n[2]:.6f})")
    t = n * c
    print(f"{etiqueta}  ((P2-P1) x (P3-P1))·(P4-P1) termino a termino: {t[0]:.6f} {t[1]:.6f} {t[2]:.6f} -> {t.sum():.6f}")
    print(f"{etiqueta}  mixto = (P2-P1)·((P3-P1) x (P4-P1)) = {mx:.6f} m3   det filas = {mx_det:.6f}")
    print(f"{etiqueta}  |(P2-P1) x (P3-P1)| = {base:.4f} m2   d = {d_mm:.3f} mm   "
          f"tolerancia {TOL_MM} mm -> {'coplanares' if d_mm <= TOL_MM else 'NO coplanares'}")
    print(f"{etiqueta}  cota del plano en (x4, y4) = {z_plano:.5f} m   z4 - z_plano = {(P4[2]-z_plano)*1000:.3f} mm")
    return mx, base, d_mm


coplanaridad(P1, P2, P3, P4, "M2")
coplanaridad(P1, P2, P3, np.array([P4[0], P4[1], 12.436]), "X1")

# ---------------------------------------------------------------- figura
fig = plt.figure(figsize=(6.4, 5.2))
ax = fig.add_subplot(111, projection="3d")
O = np.zeros(3)
caras = [[O, v, v + w, w], [u, u + v, u + v + w, u + w],
         [O, v, u + v, u], [w, v + w, u + v + w, u + w],
         [O, w, u + w, u], [v, v + w, u + v + w, u + v]]
ax.add_collection3d(Poly3DCollection([caras[0]], facecolor=TEAL, alpha=0.35, edgecolor=TEAL, linewidth=1.2))
ax.add_collection3d(Poly3DCollection(caras[1:], facecolor=GOLD, alpha=0.10, edgecolor=GRIS, linewidth=0.8))
for a, b in ((u, u + v), (u, u + w), (u + v, u + v + w), (u + w, u + v + w), (v, u + v),
             (w, u + w), (v + w, u + v + w)):
    ax.plot(*zip(a, b), color=GRIS, linewidth=1.0)
for vec, col, nom in ((u, RUST, "$u$"), (v, TEAL, "$v$"), (w, TEAL, "$w$")):
    ax.quiver(0, 0, 0, *vec, color=col, linewidth=2, arrow_length_ratio=0.08)
    ax.text(*(vec * 1.08), nom, color=col, fontsize=12)
nn = vw / area
ax.quiver(0, 0, 0, *(vw / area * 1.9), color=GRIS, linewidth=1.4, arrow_length_ratio=0.1, linestyle="-")
ax.text(*(nn * 2.0 + np.array([0.15, 0.0, 0.0])), r"$v\times w$", color=GRIS, fontsize=11)
pie = u - altura * nn
ax.plot(*zip(u, pie), color=RUST, linestyle="--", linewidth=1.2)
ax.text(*((u + pie) / 2 + np.array([0.08, 0.0, 0.0])), r"$h$", color=RUST, fontsize=11)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.set_xlim(-0.5, 2.5); ax.set_ylim(-0.5, 3.5); ax.set_zlim(-1.2, 3.2)
ax.view_init(elev=22, azim=35)
ax.set_box_aspect((3, 4, 4.4))
ax.set_title(r"$u\cdot(v\times w)=\det[u\;v\;w]=4$:  base $|v\times w|=\sqrt{6}$, altura $h=4/\sqrt{6}$",
             fontsize=10)
fig.tight_layout()
fig.savefig(SALIDA / "cuna_mixto.png", dpi=150, metadata={"Software": None})
plt.close(fig)
print("figura:", SALIDA / "cuna_mixto.png")
