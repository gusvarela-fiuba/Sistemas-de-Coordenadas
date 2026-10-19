"""Números y figura de la subsección «Cómo se transforman las mediciones» (capítulo 5).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  T1  Definición: comprobación numérica de <Au, v> = <u, A^T v> con A = [[2,1],[0,1]],
      u = (1,2), v = (3,-1).
  T2  Rotación: R(30°)^T R(30°) = I, es decir R^T = R^-1.
  T3  Contraejemplo de las normales: recta por q = (1,1) con dirección d = (2,1) y normal
      n = (-1,2); afinidad x' = A x + c con A = [[2,1],[0,1]], c = (0,5; 1).  Ángulo entre
      la recta transformada y A n (no es 90°) y entre la recta transformada y A^-T n (90°).
  T4  Aplicación: plano del terreno de cap05_formas_lineales.py (dh = (a,b)); cambio de
      coordenadas afín x' = A x + c con A = D R(30°), D = diag(2, 1), c = (100, 200).
      Forma nueva dh' = dh A^-1 (columna A^-T dh^T); cota predicha para 50 m hacia el
      acimut 120° en las dos coordenadas; dirección de máxima pendiente transformada como
      dirección (A u) frente a la columna A^-T dh^T; lo que da tomar esa columna como
      dirección, de vuelta en el terreno (acimut y pendiente).
  X   Ejercicio: A = [[1,2],[0,1]], recta x + y = 1 (normal (1,1)); recta imagen,
      normal A^-T n, ángulo de A n con la recta imagen.

Figura (PNG, fondo blanco, dpi 150) en apunte/figuras/formas-lineales/:
  fl_normales.png  recta y normal de T3 (izquierda) y sus imágenes por la afinidad
                   (derecha): A n deja de ser perpendicular, A^-T n no.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap05_transpuesta_normales.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "formas-lineales"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, TEALD, RUST, GOLD, GRIS = "#01696F", "#0C4E54", "#A84B2F", "#D19900", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "figure.facecolor": "white", "svg.hashsalt": "cap05"})


def angulo(u, v):
    """Ángulo (grados, entre 0 y 180) entre dos vectores con el producto escalar usual."""
    return np.rad2deg(np.arccos(u @ v / (np.linalg.norm(u) * np.linalg.norm(v))))


def az(v):
    """Acimut (grados, desde el norte, horario) de un vector (E, N)."""
    return np.rad2deg(np.arctan2(v[0], v[1])) % 360


def rot(t):
    t = np.deg2rad(t)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


# ---------------------------------------------------------------- T1
print("=== T1  <Au, v> = <u, A^T v> ===")
A = np.array([[2.0, 1.0], [0.0, 1.0]])
u = np.array([1.0, 2.0]); v = np.array([3.0, -1.0])
print("A u =", A @ u, " <Au,v> =", (A @ u) @ v, " A^T v =", A.T @ v, " <u,A^T v> =", u @ (A.T @ v))

# ---------------------------------------------------------------- T2
print("\n=== T2  rotación ===")
R30 = rot(30)
print("R(30)^T R(30) =\n", R30.T @ R30)

# ---------------------------------------------------------------- T3
print("\n=== T3  normales con A^-T ===")
q = np.array([1.0, 1.0]); d = np.array([2.0, 1.0]); n = np.array([-1.0, 2.0])
c = np.array([0.5, 1.0])
AiT = np.linalg.inv(A).T
print("n·d =", n @ d, "  recta: n·(x - q) = 0  ->  ", n, "· x =", n @ q)
print("A^-1 =\n", np.linalg.inv(A), "\nA^-T =\n", AiT)
qp, dp = A @ q + c, A @ d
nA, nT = A @ n, AiT @ n
print("q' = A q + c =", qp, " d' = A d =", dp)
print("A n =", nA, " (A n)·d' =", nA @ dp, " ángulo(A n, d') =", f"{angulo(nA, dp):.4f}°")
print("A^-T n =", nT, " (A^-T n)·d' =", nT @ dp, " ángulo(A^-T n, d') =", f"{angulo(nT, dp):.4f}°")
print("recta imagen: (A^-T n)·x' =", nT @ qp, " = n·q + (A^-T n)·c =", n @ q + nT @ c)
p2 = q + d; p2p = A @ p2 + c
print("segundo punto p = q + d =", p2, " -> ", p2p, " (A^-T n)·p' =", nT @ p2p)

# ---------------------------------------------------------------- T4
print("\n=== T4  aplicación: plano del terreno en coordenadas afines ===")
pts = np.array([[5512340.00, 6172480.00, 32.45],
                [5512420.00, 6172510.00, 34.27],
                [5512360.00, 6172580.00, 33.98]])
dd = pts[1:, :2] - pts[0, :2]
a, b = np.linalg.solve(dd, pts[1:, 2] - pts[0, 2])
dh = np.array([a, b])
print(f"dh = ({a:.6f}; {b:.6f})")
D = np.diag([2.0, 1.0])
AT = D @ R30
cT = np.array([100.0, 200.0])
ATinv = np.linalg.inv(AT)
print("A = D R(30) =\n", AT, "\ndet A =", np.linalg.det(AT))
print("A^-1 =\n", ATinv)
dhp = dh @ ATinv
print(f"dh' = dh A^-1 = ({dhp[0]:.6f}; {dhp[1]:.6f})   [= (A^-T dh^T)^T: {ATinv.T @ dh}]")
u120 = np.array([np.sin(np.deg2rad(120)), np.cos(np.deg2rad(120))])
W = 50 * u120
Wp = AT @ W
print(f"desplazamiento 50 m az 120: W = ({W[0]:.3f}; {W[1]:.3f})  W' = A W = ({Wp[0]:.3f}; {Wp[1]:.3f})")
print(f"dh(W) = {dh @ W:.6f}   dh'(W') = {dhp @ Wp:.6f}   cota = {pts[0, 2] + dh @ W:.4f} / {pts[0, 2] + dhp @ Wp:.4f}")
P1p = cT                                   # P1 está en el origen de las diferencias
print("P1' =", P1p, "  punto de llegada en coordenadas nuevas =", P1p + Wp)
# lo que daría transformar dh como un punto (con A)
dhA = AT @ dh
print(f"si se transformara dh con A: ({dhA[0]:.6f}; {dhA[1]:.6f})  aplicado a W' = {dhA @ Wp:.6f}")
gm = np.linalg.norm(dh); umax = dh / gm
print(f"pendiente máxima {100 * gm:.3f} %  acimut {az(dh):.2f}°")
dir_ok = AT @ umax
col = ATinv.T @ dh
print(f"dirección de máxima pendiente transformada como dirección: A u = ({dir_ok[0]:.6f}; {dir_ok[1]:.6f})")
print(f"columna A^-T dh^T = ({col[0]:.6f}; {col[1]:.6f})   ángulo entre ambas (en el papel nuevo) = {angulo(dir_ok, col):.3f}°")
Gp = ATinv.T @ ATinv
print("métrica nueva G' = A^-T A^-1 =\n", Gp)
gp = np.linalg.solve(Gp, dhp)
print("vector asociado G'^-1 dh'^T =", gp, " = A dh^T =", AT @ dh)
back = ATinv @ col                          # la columna tomada como dirección, de vuelta al terreno
ub = back / np.linalg.norm(back)
print(f"columna A^-T dh^T llevada al terreno con A^-1: ({back[0]:.6f}; {back[1]:.6f})  acimut {az(back):.2f}°"
      f"  pendiente en esa dirección {100 * dh @ ub:.3f} %")
print(f"A u de vuelta al terreno: acimut {az(ATinv @ dir_ok):.2f}°")

# ---------------------------------------------------------------- X
print("\n=== X  ejercicio ===")
AX = np.array([[1.0, 2.0], [0.0, 1.0]])
nX = np.array([1.0, 1.0]); dX = np.array([-1.0, 1.0])
AXiT = np.linalg.inv(AX).T
print("A^-1 =\n", np.linalg.inv(AX), "\nA^-T =\n", AXiT)
print("A^-T n =", AXiT @ nX, "  A d =", AX @ dX, " (A^-T n)·(A d) =", (AXiT @ nX) @ (AX @ dX))
print("A n =", AX @ nX, " (A n)·(A d) =", (AX @ nX) @ (AX @ dX), f" ángulo = {angulo(AX @ nX, AX @ dX):.4f}°")
for p in ([1.0, 0.0], [0.0, 1.0]):
    pp = AX @ np.array(p)
    print("  punto", p, "->", pp, " x'-y' =", pp[0] - pp[1])

# ================================================================ figura
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.6))
ts = np.array([-3.0, 3.0])
ax = axs[0]
seg = np.array([q + t * d for t in ts])
ax.plot(seg[:, 0], seg[:, 1], color=TEAL, lw=2)
ax.annotate("", xy=q + n / np.linalg.norm(n), xytext=q, arrowprops=dict(arrowstyle="-|>", color=TEALD, lw=2))
ax.text(*(q + n / np.linalg.norm(n) + [0.08, 0.0]), "$n=(-1,2)$", color=TEALD)
ax.plot(*q, "o", color="k", ms=4); ax.text(q[0] + 0.1, q[1] - 0.3, "$q$")
ax.set_xlim(-1.5, 3.5); ax.set_ylim(-0.5, 3.0)
ax.set_title("recta por $q=(1,1)$ con dirección $d=(2,1)$\ny su normal $n$ ($90^\\circ$)", fontsize=10)
ax = axs[1]
segp = np.array([qp + t * dp for t in np.array([-1.2, 1.0])])
ax.plot(segp[:, 0], segp[:, 1], color=TEAL, lw=2)
for vec, col_, lab, off in ((nA, RUST, f"$An$: {angulo(nA, dp):.1f}°".replace(".", ","), (0.15, -0.35)),
                            (nT, TEALD, f"$A^{{-T}}n$: {angulo(nT, dp):.0f}°", (-2.3, 0.15))):
    e = vec / np.linalg.norm(vec) * 1.4
    ax.annotate("", xy=qp + e, xytext=qp, arrowprops=dict(arrowstyle="-|>", color=col_, lw=2))
    ax.text(*(qp + e + off), lab, color=col_)
ax.plot(*qp, "o", color="k", ms=4); ax.text(qp[0] + 0.12, qp[1] - 0.35, "$q'=Aq+c$")
ax.set_xlim(-2.5, 7.0); ax.set_ylim(-0.5, 4.0)
ax.set_title("imagen por $x'=Ax+c$ con $A$ no ortogonal\n$An$ ya no es normal; $A^{-T}n$ sí", fontsize=10)
for ax in axs:
    ax.set_aspect("equal"); ax.axhline(0, color=GRIS, lw=.6); ax.axvline(0, color=GRIS, lw=.6)
fig.tight_layout(); fig.savefig(SALIDA / "fl_normales.png", dpi=150, metadata={"Software": None})
plt.close(fig)
print("\nfigura en", SALIDA / "fl_normales.png")
