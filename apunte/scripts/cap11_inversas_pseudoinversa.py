"""Números y figuras del capítulo «Inversas y pseudoinversa: los cuatro subespacios».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Inversa de una 3x3 por cuña de filas»: A = [[2,1,0],[1,1,1],[0,1,3]];
      det = f1 . (f2 x f3); columnas de la inversa f2 x f3, f3 x f1, f1 x f2 sobre det;
      control A A^{-1} = I.
  E2  Ejemplo «Los cuatro subespacios de una 3x2 de rango 2»: A = [[1,0],[1,1],[1,2]];
      Im A (normal = cuña de las columnas), ker A^T, Im A^T, ker A; dimensiones.
  E3  Ejemplo «Recta por cuatro puntos»: (0,1), (1,2), (2,2), (3,4); ecuaciones normales,
      (a, b), residuo, A^T r = 0, |r|^2, P = A A^+ y (I-P) y = r.
  E4  Ejemplo «Solución de norma mínima de un sistema 2x3»: A = [[1,1,1],[1,-1,0]],
      b = (3,1); A^+ = A^T (A A^T)^{-1}; x+ ; núcleo; otra solución con más norma;
      las cuatro condiciones de Moore-Penrose; A^+ por SVD = np.linalg.pinv.
  P3  Figura de proyección: A = [[0,1],[1,1],[2,1]], y = (0,1,3) (recta por tres puntos del texto).
  S   Figura del sistema subdeterminado x + 2y = 5: solución de norma mínima (1,2).
  A   Aplicación topográfica: red de nivelación A (fija, 100,000 m), B, C, D; seis
      desniveles medidos; matriz de diseño 6x3; A^T A; cotas ajustadas; residuos; cierres
      de los circuitos; sigma0; precisión de cada cota. Red libre 6x4: rango, núcleo,
      solución de norma mínima por pseudoinversa, traslado al datum H_A = 100, desniveles
      ajustados iguales, Moore-Penrose.
  X1  Ejercicio 1: inversa de M = [[3,1],[5,2]]; R(30°)^{-1} = R(30°)^T.
  X2  Ejercicio 2: cuatro subespacios de B = [[1,2,3],[2,4,6]].
  X3  Ejercicio 3: tres medidas de una distancia 125,432; 125,438; 125,429 (ajuste de una
      constante): A^+ = (1/3)(1,1,1), media, residuos, sigma0.
  X4  Ejercicio 4: norma mínima de x + 2y + 2z = 9.
  X5  Ejercicio 5: P = A A^+ e I - P para la A de E2.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/inversas/:
  inv_cuatro_subespacios.png  esquema de los cuatro subespacios y las flechas de A y A^+.
  inv_proyeccion.png          y, su proyección A x sobre el plano Im A y el residuo perpendicular.
  inv_norma_minima.png        recta de soluciones de x + 2y = 5 y la solución de norma mínima.
  inv_red_nivelacion.png      la red de nivelación de la aplicación.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap11_inversas_pseudoinversa.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, FancyArrowPatch

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "inversas"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})


def moore_penrose(A, Ap, nombre):
    c = [np.allclose(A @ Ap @ A, A), np.allclose(Ap @ A @ Ap, Ap),
         np.allclose((A @ Ap).T, A @ Ap), np.allclose((Ap @ A).T, Ap @ A)]
    err = [np.abs(A @ Ap @ A - A).max(), np.abs(Ap @ A @ Ap - Ap).max(),
           np.abs((A @ Ap).T - A @ Ap).max(), np.abs((Ap @ A).T - Ap @ A).max()]
    print(f"Moore-Penrose {nombre}: AA+A=A {c[0]}, A+AA+=A+ {c[1]}, AA+ sim {c[2]}, A+A sim {c[3]};"
          f" error máx {max(err):.1e}")


# ---------------------------------------------------------------- E1
print("=== E1  inversa 3x3 por cuña de filas ===")
A1 = np.array([[2.0, 1, 0], [1, 1, 1], [0, 1, 3]])
f1, f2, f3 = A1
c1, c2, c3 = np.cross(f2, f3), np.cross(f3, f1), np.cross(f1, f2)
det1 = f1 @ c1
print("f2 x f3 =", c1, " f3 x f1 =", c2, " f1 x f2 =", c3)
print("det = f1.(f2 x f3) =", det1, " np.linalg.det =", round(np.linalg.det(A1), 10))
Ainv1 = np.column_stack([c1, c2, c3]) / det1
print("A^{-1} =\n", Ainv1)
print("A A^{-1} =\n", A1 @ Ainv1, " coincide con inv:", np.allclose(Ainv1, np.linalg.inv(A1)))

# ---------------------------------------------------------------- E2
print("\n=== E2  cuatro subespacios 3x2 ===")
A2 = np.array([[1.0, 0], [1, 1], [1, 2]])
n2 = np.cross(A2[:, 0], A2[:, 1])
print("cuña de columnas (normal de Im A) =", n2, " A^T n =", A2.T @ n2)
print("rango =", np.linalg.matrix_rank(A2), " A^T A =", (A2.T @ A2).tolist(), " det =", round(np.linalg.det(A2.T @ A2), 10))
print("dims: Im A = 2, ker A^T = 1, Im A^T = 2, ker A = 0")

# ---------------------------------------------------------------- E3
print("\n=== E3  recta por cuatro puntos ===")
xs = np.array([0.0, 1, 2, 3]); ys = np.array([1.0, 2, 2, 4])
A3 = np.column_stack([xs, np.ones(4)])
N3 = A3.T @ A3; t3 = A3.T @ ys
sol3 = np.linalg.solve(N3, t3)
r3 = ys - A3 @ sol3
print("A^T A =", N3.tolist(), " A^T y =", t3.tolist(), " det =", round(np.linalg.det(N3), 10))
print("(a, b) =", sol3, " ajustados =", A3 @ sol3, " residuo r = y - Ax =", r3)
print("A^T r =", A3.T @ r3, " |r|^2 =", round(r3 @ r3, 6))
Ap3 = np.linalg.inv(N3) @ A3.T
print("A^+ = (A^T A)^{-1} A^T =\n", Ap3, "\n20 A^+ =\n", 20 * Ap3)
P3m = A3 @ Ap3
print("P = A A^+ =\n", P3m, "\n10 P =\n", 10 * P3m)
print("P^2 = P:", np.allclose(P3m @ P3m, P3m), " traza P =", round(np.trace(P3m), 10), " (I-P) y =", (np.eye(4) - P3m) @ ys)
print("lstsq =", np.linalg.lstsq(A3, ys, rcond=None)[0], " pinv y =", np.linalg.pinv(A3) @ ys)

# ---------------------------------------------------------------- E4
print("\n=== E4  norma mínima 2x3 ===")
A4 = np.array([[1.0, 1, 1], [1, -1, 0]]); b4 = np.array([3.0, 1])
AAt = A4 @ A4.T
w4 = np.linalg.solve(AAt, b4)
Ap4 = A4.T @ np.linalg.inv(AAt)
x4 = Ap4 @ b4
k4 = np.cross(A4[0], A4[1])
print("A A^T =", AAt.tolist(), " w = (AA^T)^{-1} b =", w4)
print("A^+ = A^T (AA^T)^{-1} =\n", Ap4, "\n6 A^+ =\n", 6 * Ap4)
print("x+ = A^+ b =", x4, " A x+ =", A4 @ x4, " |x+|^2 =", x4 @ x4, " |x+| =", round(np.linalg.norm(x4), 4))
print("núcleo (cuña de filas) =", k4, " x+ . núcleo =", x4 @ k4)
x4b = x4 + 0.5 * k4
print("otra solución x+ + 0,5 k =", x4b, " A x =", A4 @ x4b, " |x|^2 =", x4b @ x4b)
print("A A^+ =\n", A4 @ Ap4, "\nA^+ A =\n", Ap4 @ A4, "\n6 A^+ A =\n", 6 * Ap4 @ A4)
moore_penrose(A4, Ap4, "E4")
U4, s4, Vt4 = np.linalg.svd(A4)
print("sigma =", s4, " sigma^2 =", s4 ** 2, " V Sigma^+ U^T = pinv:", np.allclose(Vt4.T[:, :2] @ np.diag(1 / s4) @ U4.T, Ap4),
      np.allclose(np.linalg.pinv(A4), Ap4))

# ---------------------------------------------------------------- P3 (figura de proyección)
print("\n=== P3  figura de proyección (tres puntos) ===")
Ap = np.array([[0.0, 1], [1, 1], [2, 1]]); yp = np.array([0.0, 1, 3])
xp = np.linalg.lstsq(Ap, yp, rcond=None)[0]; pp = Ap @ xp; rp = yp - pp
print("x =", xp, " Ax =", pp, " r =", rp, " A^T r =", Ap.T @ rp)

# ---------------------------------------------------------------- S
print("\n=== S  x + 2y = 5 ===")
As = np.array([[1.0, 2]]); xs_min = np.linalg.pinv(As) @ np.array([5.0])
print("x+ =", xs_min, " |x+| =", round(np.linalg.norm(xs_min), 4), " = sqrt(5)")

# ---------------------------------------------------------------- A
print("\n=== A  red de nivelación ===")
HA = 100.000
obs = [("A", "B", 1.238), ("B", "C", 0.835), ("C", "D", -1.457),
       ("D", "A", -0.612), ("A", "C", 2.070), ("B", "D", -0.621)]
idx = {"B": 0, "C": 1, "D": 2}
n, u = len(obs), 3
Ad = np.zeros((n, u)); bd = np.zeros(n); l = np.array([o[2] for o in obs])
for k, (i, j, h) in enumerate(obs):
    bd[k] = h
    if i == "A": bd[k] += HA
    else: Ad[k, idx[i]] = -1
    if j == "A": bd[k] -= HA
    else: Ad[k, idx[j]] = 1
print("A (6x3) =\n", Ad, "\nb =", bd)
N = Ad.T @ Ad; t = Ad.T @ bd
print("N = A^T A =\n", N, "\nA^T b =", np.round(t, 3), " det N =", round(np.linalg.det(N), 6))
Ninv = np.linalg.inv(N)
print("N^{-1} =\n", Ninv, "\n8 N^{-1} =\n", 8 * Ninv)
xh = Ninv @ t
print("cotas ajustadas H_B, H_C, H_D =", np.round(xh, 4))
v = Ad @ xh - bd
print("residuos v = A x - b (mm) =", np.round(1000 * v, 2))
print("suma v^2 (mm^2) =", round(1e6 * v @ v, 3), " A^T v =", np.round(Ad.T @ v, 12))
ladj = l + v
print("desniveles ajustados =", np.round(ladj, 5))
circ = {"ABC (AB+BC-AC)": [1, 1, 0, 0, -1, 0], "ACD (AC+CD+DA)": [0, 0, 1, 1, 1, 0],
        "BCD (BC+CD-BD)": [0, 1, 1, 0, 0, -1], "ABD (AB+BD+DA)": [1, 0, 0, 1, 0, 1]}
for nom, c in circ.items():
    c = np.array(c)
    print(f"circuito {nom}: cierre medido = {1000 * c @ l:+.1f} mm, suma residuos = {1000 * c @ v:+.2f} mm,"
          f" cierre ajustado = {c @ ladj:.1e}")
s0 = np.sqrt(v @ v / (n - u))
print("sigma0 = sqrt(v^T v / 3) =", round(1000 * s0, 3), "mm")
sig = s0 * np.sqrt(np.diag(Ninv))
print("sqrt(N^{-1}_ii) =", np.round(np.sqrt(np.diag(Ninv)), 4), " sigma H (mm) =", np.round(1000 * sig, 3))
# red libre
Al = np.zeros((n, 4)); idl = {"A": 0, "B": 1, "C": 2, "D": 3}
for k, (i, j, h) in enumerate(obs):
    Al[k, idl[i]] = -1; Al[k, idl[j]] = 1
print("\nred libre A (6x4) =\n", Al)
print("rango =", np.linalg.matrix_rank(Al), " A (1,1,1,1) =", Al @ np.ones(4),
      " det(A^T A) =", round(np.linalg.det(Al.T @ Al), 10))
print("A^T A =\n", Al.T @ Al)
Alp = np.linalg.pinv(Al)
xl = Alp @ l
print("x+ = A^+ l =", np.round(xl, 4), " suma =", round(xl.sum(), 12), " (perpendicular al núcleo)")
tras = HA - xl[0]
xl2 = xl + tras
print("trasladar t =", round(tras, 4), " -> cotas =", np.round(xl2, 4), " iguales al ajuste con A fijo:",
      np.allclose(xl2[1:], xh))
vl = Al @ xl - l
print("residuos red libre (mm) =", np.round(1000 * vl, 2), " iguales:", np.allclose(vl, v))
print("desniveles ajustados iguales:", np.allclose(Al @ xl, ladj))
moore_penrose(Al, Alp, "red libre")
print("A^+ A = I - (1/4) 11^T:", np.allclose(Alp @ Al, np.eye(4) - np.ones((4, 4)) / 4))
print("A A^+ (red libre) = A A^+ (A fijo):", np.allclose(Al @ Alp, Ad @ np.linalg.pinv(Ad)))
print("sigma singulares red libre =", np.round(np.linalg.svd(Al)[1], 4))

# ---------------------------------------------------------------- X1
print("\n=== X1 ===")
M = np.array([[3.0, 1], [5, 2]])
print("det M =", round(np.linalg.det(M), 10), " M^{-1} =", np.linalg.inv(M).tolist())
th = np.deg2rad(30); R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
print("R(30) R(30)^T = I:", np.allclose(R @ R.T, np.eye(2)), " R^T =", R.T)

# ---------------------------------------------------------------- X2
print("\n=== X2 ===")
B = np.array([[1.0, 2, 3], [2, 4, 6]])
print("rango =", np.linalg.matrix_rank(B))
for vv in ([2.0, -1, 0], [3.0, 0, -1]):
    print("B", vv, "=", B @ np.array(vv))
print("B^T (2,-1) =", B.T @ np.array([2.0, -1]))
print("(2,-1,0).(1,2,3) =", np.dot([2, -1, 0], [1, 2, 3]), " (3,0,-1).(1,2,3) =", np.dot([3, 0, -1], [1, 2, 3]))
print("B^+ = B^T/70:", np.allclose(np.linalg.pinv(B), B.T / 70), " (|1,2|^2 |1,2,3|^2 = 5*14 = 70)")

# ---------------------------------------------------------------- X3
print("\n=== X3 ===")
d = np.array([125.432, 125.438, 125.429]); Ac = np.ones((3, 1))
dh = (np.linalg.pinv(Ac) @ d)[0]
vd = dh - d
print("A^+ =", np.linalg.pinv(Ac).ravel(), " d =", round(dh, 4), " residuos (mm) =", np.round(1000 * vd, 1),
      " suma =", round(vd.sum(), 12))
s0d = np.sqrt(vd @ vd / 2)
print("v^T v (mm^2) =", round(1e6 * vd @ vd, 3), " sigma0 =", round(1000 * s0d, 3), "mm  sigma media =",
      round(1000 * s0d / np.sqrt(3), 3), "mm")

# ---------------------------------------------------------------- X4
print("\n=== X4 ===")
a = np.array([[1.0, 2, 2]]); x = np.linalg.pinv(a) @ np.array([9.0])
print("x+ =", x, " |x+| =", np.linalg.norm(x), " otra: (9,0,0) norma 9")

# ---------------------------------------------------------------- X5
print("\n=== X5 ===")
P5 = A2 @ np.linalg.pinv(A2)
print("6 P =\n", 6 * P5, "\n6 (I-P) =\n", 6 * (np.eye(3) - P5))
print("I - P = n n^T/6:", np.allclose(np.eye(3) - P5, np.outer(n2, n2) / 6), " traza P =", round(np.trace(P5), 10))
yv = np.array([1.0, 0, 2])
print("y = (1,0,2): P y =", P5 @ yv, " (I-P) y =", (np.eye(3) - P5) @ yv)

# ================================================================ figuras
# 1) cuatro subespacios
fig, ax = plt.subplots(figsize=(8.6, 4.0))
ax.set_xlim(0.2, 9.8); ax.set_ylim(-0.3, 4.6); ax.axis("off"); ax.set_aspect("equal")


def caja(o, ang, w, h, col, txt, sub):
    d1 = np.array([np.cos(ang), np.sin(ang)]); d2 = np.array([-np.sin(ang), np.cos(ang)])
    o = np.array(o)
    pts = [o, o + w * d1, o + w * d1 + h * d2, o + h * d2]
    ax.add_patch(Polygon(pts, closed=True, fc=col, ec=GRIS, alpha=0.28, lw=1))
    c = o + 0.5 * w * d1 + 0.5 * h * d2
    ax.text(*c, txt, ha="center", va="center", fontsize=10, weight="bold")
    ax.text(c[0], c[1] - 0.32, sub, ha="center", va="center", fontsize=8.5, color="#333")


o1 = np.array([3.2, 2.0]); o2 = np.array([6.8, 2.0])
g = np.deg2rad
caja(o1, g(135), 1.9, 1.9, TEAL, r"$\mathrm{Im}\,A^T$", "co-imagen, dim $r$")
caja(o1, g(225), 1.4, 1.4, GOLD, r"$\ker A$", "núcleo, dim $n-r$")
caja(o2, g(-45), 1.9, 1.9, TEAL, r"$\mathrm{Im}\,A$", "imagen, dim $r$")
caja(o2, g(-135), 1.4, 1.4, RUST, r"$\ker A^T$", "dim $m-r$")
for o in (o1, o2):
    ax.plot(*o, "o", color="k", ms=4)
ax.text(o1[0] + 0.12, o1[1] + 0.12, "$0$", fontsize=9); ax.text(o2[0] - 0.3, o2[1] + 0.12, "$0$", fontsize=9)
ax.text(1.85, 4.35, r"entrada $\mathbb{R}^n$", ha="center", fontsize=11)
ax.text(8.15, 4.35, r"salida $\mathbb{R}^m$", ha="center", fontsize=11)
ax.add_patch(FancyArrowPatch((2.0, 2.75), (8.0, 2.75), arrowstyle="-|>", mutation_scale=14, color=TEAL, lw=1.6,
                             connectionstyle="arc3,rad=-0.12"))
ax.text(5.0, 3.75, r"$A$: lleva $\mathrm{Im}\,A^T$ sobre $\mathrm{Im}\,A$ sin perder nada", ha="center", fontsize=9, color=TEAL)
ax.add_patch(FancyArrowPatch((8.0, 2.3), (2.0, 2.3), arrowstyle="-|>", mutation_scale=14, color=TEAL, lw=1.2,
                             ls="--", connectionstyle="arc3,rad=0.08"))
ax.text(5.0, 2.3, r"$A^{+}$ la deshace", ha="center", fontsize=9, color=TEAL)
ax.add_patch(FancyArrowPatch((3.7, 0.9), (6.72, 1.92), arrowstyle="-|>", mutation_scale=12, color=GOLD, lw=1.3,
                             connectionstyle="arc3,rad=0.25"))
ax.add_patch(FancyArrowPatch((6.3, 0.9), (3.28, 1.92), arrowstyle="-|>", mutation_scale=12, color=RUST, lw=1.1,
                             ls=":", connectionstyle="arc3,rad=-0.25"))
ax.text(5.0, 0.35, r"$A(\ker A)=0$", ha="center", fontsize=9, color="#7a5c00")
ax.text(5.0, -0.05, r"$A^{+}(\ker A^T)=0$", ha="center", fontsize=9, color=RUST)
fig.tight_layout(); fig.savefig(SALIDA / "inv_cuatro_subespacios.png", dpi=150); plt.close(fig)

# 2) proyección sobre la imagen (esquema en perspectiva del ejemplo de tres puntos)
fig, ax = plt.subplots(figsize=(6.4, 4.2))
plano = np.array([[-0.5, -0.6], [4.6, -0.6], [6.0, 1.6], [0.9, 1.6]])
ax.add_patch(Polygon(plano, closed=True, fc=TEAL, ec=TEAL, alpha=0.15, lw=1))
O2 = np.array([1.2, 0.0]); Pp2 = np.array([4.2, 0.9]); Y2 = Pp2 + np.array([0.0, 2.3])
c1 = np.array([2.2, -0.35]); c2 = np.array([0.0, 1.25])
for c, nm in ((c1, r"$a_1$"), (c2, r"$a_2$")):
    ax.annotate("", xy=O2 + c, xytext=O2, arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.1))
    ax.text(*(O2 + c * 1.06 + ([0.05, -0.15] if nm == r"$a_1$" else [-0.3, -0.05])), nm, color="#555", fontsize=10)
ax.annotate("", xy=Y2, xytext=O2, arrowprops=dict(arrowstyle="-|>", color=RUST, lw=2))
ax.annotate("", xy=Pp2, xytext=O2, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=2))
ax.plot(*zip(Pp2, Y2), color=GOLD, lw=2.4)
q = 0.18; e = (O2 - Pp2) / np.linalg.norm(O2 - Pp2)
ax.plot([Pp2[0] + q * e[0], Pp2[0] + q * e[0], Pp2[0]], [Pp2[1] + q * e[1], Pp2[1] + q * e[1] + q, Pp2[1] + q], color="k", lw=0.8)
ax.plot(*O2, "o", color="k", ms=3.5); ax.text(O2[0] - 0.25, O2[1] - 0.05, "$0$", fontsize=10)
ax.text(Y2[0] + 0.1, Y2[1], r"$y=(0,1,3)$", color=RUST, fontsize=11, va="center")
ax.text(Pp2[0] + 0.12, Pp2[1] - 0.32, r"$A\hat x=(-\frac{1}{6},\frac{4}{3},\frac{17}{6})$", color=TEAL, fontsize=10)
ax.text(Pp2[0] + 0.12, Pp2[1] + 1.15, r"$r=y-A\hat x=(\frac{1}{6},-\frac{1}{3},\frac{1}{6})$", color="#7a5c00", fontsize=10)
ax.text(2.3, -0.9, r"$\mathrm{Im}\,A$ (plano de las columnas)", color=TEAL, fontsize=10, ha="center")
ax.text(Pp2[0] + 0.12, Pp2[1] + 0.7, r"$A^T r=0$: $r\in\ker A^T$", color="#7a5c00", fontsize=10)
ax.set_xlim(-0.8, 7.6); ax.set_ylim(-1.15, 3.6); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout(); fig.savefig(SALIDA / "inv_proyeccion.png", dpi=150); plt.close(fig)

# 3) norma mínima
fig, ax = plt.subplots(figsize=(5.6, 4.6))
tt = np.linspace(-2.2, 2.2, 2)
L = xs_min[None, :] + tt[:, None] * np.array([2.0, -1]) / np.sqrt(5) * 2.6
ax.plot(L[:, 0], L[:, 1], color=TEAL, lw=2, label=r"soluciones de $x+2y=5$")
ax.annotate("", xy=xs_min, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=2))
otra = np.array([5.0, 0.0]); otra2 = np.array([3.0, 1.0])
for q in (otra, otra2):
    ax.annotate("", xy=q, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.2, ls="--"))
ax.plot(*zip(*[otra, otra2, xs_min]), "o", color=GRIS, ms=4)
ax.plot(*xs_min, "o", color=RUST, ms=6)
ax.text(xs_min[0] - 0.95, xs_min[1] + 0.15, r"$x^{+}=(1,2)$, $|x^{+}|=\sqrt{5}$", color=RUST)
ax.text(5.0, 0.2, r"$(5,0)$, norma $5$", color="#555", fontsize=9, ha="center")
ax.text(3.15, 1.12, r"$(3,1)$", color="#555", fontsize=9)
ax.annotate("", xy=(0.5, 1.0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.5))
ax.text(-0.15, 0.85, r"fila $(1,2)$", color="#7a5c00", fontsize=9, ha="right")
ax.annotate("", xy=xs_min + np.array([2.0, -1]) * 0.6, xytext=xs_min, arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.3))
ax.text(2.3, 1.55, r"núcleo $(2,-1)$", color=TEAL, fontsize=9)
ax.axhline(0, color=GRIS, lw=0.6); ax.axvline(0, color=GRIS, lw=0.6)
ax.set_xlim(-1.2, 6.2); ax.set_ylim(-1.2, 4.2); ax.set_aspect("equal"); ax.grid(alpha=0.25)
ax.legend(loc="upper right", fontsize=9)
fig.tight_layout(); fig.savefig(SALIDA / "inv_norma_minima.png", dpi=150); plt.close(fig)

# 4) red de nivelación
fig, ax = plt.subplots(figsize=(5.4, 4.0))
pos = {"A": (0, 0), "B": (4, 0.4), "C": (4.4, 3.4), "D": (0.4, 3.0)}
cotas = {"A": HA, "B": xh[0], "C": xh[1], "D": xh[2]}
for k, (i, j, h) in enumerate(obs):
    p, q = np.array(pos[i]), np.array(pos[j])
    ax.annotate("", xy=p + 0.88 * (q - p), xytext=p + 0.12 * (q - p),
                arrowprops=dict(arrowstyle="-|>", color=TEAL, lw=1.4))
    m = p + (0.72 if k in (4, 5) else 0.5) * (q - p); nrm = np.array([-(q - p)[1], (q - p)[0]]); nrm /= np.linalg.norm(nrm)
    off = 0.0 if k in (4, 5) else 0.28
    ax.text(*(m + off * nrm), f"{k + 1}: {h:+.3f}".replace(".", ","),
            fontsize=8.5, ha="center", va="center", color="#333",
            bbox=dict(fc="white", ec="none", alpha=0.85, pad=0.5))
for nme, p in pos.items():
    ax.plot(*p, "s" if nme == "A" else "o", color=RUST if nme == "A" else TEAL, ms=9)
    dx = -0.15 if nme in "AD" else 0.15
    ax.text(p[0] + dx, p[1] + (0.3 if nme in "CD" else -0.35), nme, ha="right" if nme in "AD" else "left",
            fontsize=11, weight="bold")
ax.text(-0.15, -0.75, "fijo: 100,000 m", color=RUST, fontsize=8.5)
ax.set_xlim(-1.3, 5.6); ax.set_ylim(-1.0, 4.0); ax.set_aspect("equal"); ax.axis("off")
fig.tight_layout(); fig.savefig(SALIDA / "inv_red_nivelacion.png", dpi=150); plt.close(fig)
print("\nfiguras en", SALIDA)
