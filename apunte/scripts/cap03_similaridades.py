"""Números y figuras del capítulo «Reflexiones, isometrías y similaridades».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Reflexión respecto de la recta que pasa por dos puntos»: recta por
      P = (1,2) y Q = (7,5), normal, proyección y reflejo de X = (5,8), matriz H y
      traslación de la reflexión, distancias a P conservadas.
  E2  Ejemplo «Dos reflexiones: rotación o traslación»: B: y = 1, A: x - y = 1 (secantes,
      giro de 90° alrededor de (2,1)), orden inverso, y B': x - y = -3 (paralela a A,
      traslación (4,-4)); punto de prueba p = (4,0).
  E3  Ejemplo «La similaridad que lleva un segmento a otro»: P = (1,1), Q = (3,2) van a
      P' = (-3,-1), Q' = (-3,4): parte lineal a + ib, razón, ángulo, traslación y centro.
  A   Aplicación topográfica (Helmert 2D, 4 parámetros): sistema local arbitrario ->
      Gauss-Krüger faja 5. Dos puntos de control C1, C2 -> a, b, t_E, t_N, lambda, theta;
      transformación de 3 puntos nuevos (D, F, G), distancias (cociente = lambda) y
      ángulo en F conservado; tercer punto de control C3: predicción, residuo y solución
      alternativa con C1, C3.
  X1..X8  Ejercicios de consolidación (reflexiones puntuales, paralelogramo, reflexión en
      recta, ejes paralelos, ejes a 30°, traslación y rotación, homotecia, similaridad 40°).
  X9  Ejercicio: inversa de la transformación de Helmert de la aplicación.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/similaridades/:
  helmert.png  levantamiento en el sistema local y en el oficial (dos paneles), con los
               puntos de control y los puntos transformados.
(Las demás figuras del capítulo están en TikZ.)

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap03_similaridades.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "similaridades"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
deg = np.pi / 180


def R(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def H(a):
    """Matriz de reflexión respecto de una recta por el origen de ángulo a."""
    return np.array([[np.cos(2 * a), np.sin(2 * a)], [np.sin(2 * a), -np.cos(2 * a)]])


def refl_recta(n, c, x):
    """Reflejo de x respecto de la recta n·x = c."""
    n, x = np.asarray(n, float), np.asarray(x, float)
    return x - 2 * (n @ x - c) / (n @ n) * n


# ---------------------------------------------------------------- E1
print("=== E1  reflexión respecto de la recta por P y Q ===")
P, Q, X = np.array([1.0, 2.0]), np.array([7.0, 5.0]), np.array([5.0, 8.0])
d = Q - P
n = np.array([d[1], -d[0]]) / 3          # normal (1,-2) (d = (6,3) = 3·(2,1))
c = n @ P
print("d =", d, " n =", n, " c = n·P =", c, " recta: x - 2y =", c)
print("n·X - c =", n @ X - c, " |n|^2 =", n @ n)
t = (X - P) @ d / (d @ d)
p = P + t * d
print("(X-P)·d =", (X - P) @ d, " |d|^2 =", d @ d, " t =", t, " proyección p =", p)
print("p por la normal =", X - (n @ X - c) / (n @ n) * n)
Xr = refl_recta(n, c, X)
print("reflejo X' =", Xr, " = 2p - X =", 2 * p - X)
Hm = np.eye(2) - 2 * np.outer(n, n) / (n @ n)
print("H = I - 2nn^T/|n|^2 =\n", Hm, "  ·5 =\n", 5 * Hm, " det =", np.linalg.det(Hm))
tr = 2 * c / (n @ n) * n
print("traslación 2c n/|n|^2 =", tr, " H X + t =", Hm @ X + tr)
print("|X-P|^2 =", (X - P) @ (X - P), " |X'-P|^2 =", (Xr - P) @ (Xr - P), " X'-P =", Xr - P)
print("|X-Q|^2 =", (X - Q) @ (X - Q), " |X'-Q|^2 =", (Xr - Q) @ (Xr - Q))

# ---------------------------------------------------------------- E2
print("\n=== E2  dos reflexiones ===")
phiB = lambda v: refl_recta([0, 1], 1, v)        # B: y = 1
phiA = lambda v: refl_recta([1, -1], 1, v)       # A: x - y = 1
phiBp = lambda v: refl_recta([1, -1], -3, v)     # B': x - y = -3
o = np.linalg.solve(np.array([[0, 1.0], [1, -1]]), [1, 1])
print("intersección de A y B: o =", o)
pp = np.array([4.0, 0.0])
print("p =", pp, " phiB(p) =", phiB(pp), " phiA(phiB(p)) =", phiA(phiB(pp)),
      " rotación 90° de p alrededor de o =", o + R(90 * deg) @ (pp - o))
for v in ([0, 0], [1, 0], [0, 1]):
    v = np.array(v, float)
    print("  phiA phiB", v, "->", phiA(phiB(v)), "  (3-y, x-1) =", (3 - v[1], v[0] - 1))
print("orden inverso phiB phiA(p) =", phiB(phiA(pp)), " rotación -90° =", o + R(-90 * deg) @ (pp - o))
print("paralelas: phiB'(p) =", phiBp(pp), " phiA(phiB'(p)) =", phiA(phiBp(pp)), " desplazamiento =", phiA(phiBp(pp)) - pp)
for v in ([0, 0], [2, 5]):
    v = np.array(v, float)
    print("  phiA phiB'", v, "->", phiA(phiBp(v)), " desplazamiento", phiA(phiBp(v)) - v)
print("distancia entre A y B' = 4/sqrt2 =", 4 / np.sqrt(2), " |traslación| = 4 sqrt2 =", 4 * np.sqrt(2))

# ---------------------------------------------------------------- E3
print("\n=== E3  similaridad que lleva PQ a P'Q' ===")
z1, z2, w1, w2 = 1 + 1j, 3 + 2j, -3 - 1j, -3 + 4j
a = (w2 - w1) / (z2 - z1)
b = w1 - a * z1
print("Q-P =", z2 - z1, " Q'-P' =", w2 - w1, " a + ib =", a, " t =", b)
lam = abs(a)
print("razón =", lam, " (sqrt5 =", np.sqrt(5), ")  |PQ| =", abs(z2 - z1), " |P'Q'| =", abs(w2 - w1))
print("ángulo (°) =", np.degrees(np.angle(a)), " mitad (ángulo entre los ejes de reflexión) =", np.degrees(np.angle(a)) / 2)
cen = b / (1 - a)
print("centro c = t/(1-a) =", cen)
Am = np.array([[a.real, -a.imag], [a.imag, a.real]])
print("A =\n", Am, " I - A =\n", np.eye(2) - Am, " solve:", np.linalg.solve(np.eye(2) - Am, [b.real, b.imag]))
print("|c-P| =", abs(cen - z1), " |c-P'| =", abs(cen - w1), " cociente =", abs(cen - w1) / abs(cen - z1))
print("|c-Q| =", abs(cen - z2), " |c-Q'| =", abs(cen - w2), " cociente =", abs(cen - w2) / abs(cen - z2))
print("verificación S(P), S(Q) =", a * z1 + b, a * z2 + b)
print("ángulo de P-c a P'-c (°) =", np.degrees(np.angle((w1 - cen) / (z1 - cen))))

# ---------------------------------------------------------------- A: Helmert 2D
print("\n=== A  Helmert 2D: local -> Gauss-Krüger faja 5 ===")
lam_v, th_v = 1.000150, 27.85 * deg              # parámetros "verdaderos" (sólo para fabricar datos)
t_v = np.array([5432100.000, 6154300.000])
loc = {"C1": (50.000, 20.000), "C2": (310.000, 145.000), "C3": (120.000, 260.000),
       "D": (180.000, 60.000), "F": (240.000, 210.000), "G": (70.000, 150.000)}
loc = {k: np.array(v) for k, v in loc.items()}
ofi = {k: np.round(t_v + lam_v * R(th_v) @ loc[k], 3) for k in ("C1", "C2", "C3")}
ofi["C3"] = ofi["C3"] + np.array([0.021, -0.034])  # error de medición en el tercer control
for k in ofi:
    print(f"{k}: local {loc[k]}  oficial E = {ofi[k][0]:.3f}  N = {ofi[k][1]:.3f}")


def helmert(k1, k2):
    z1, z2 = complex(*loc[k1]), complex(*loc[k2])
    w1, w2 = complex(*ofi[k1]), complex(*ofi[k2])
    ab = (w2 - w1) / (z2 - z1)
    t = w1 - ab * z1
    return ab.real, ab.imag, t.real, t.imag


aa, bb, tE, tN = helmert("C1", "C2")
dl = loc["C2"] - loc["C1"]
do = ofi["C2"] - ofi["C1"]
print("Δlocal C1->C2 =", dl, " Δoficial =", do)
print(f"|Δlocal|^2 = {dl @ dl:.3f}  Δx ΔE + Δy ΔN = {dl @ do:.3f}  Δx ΔN - Δy ΔE = {dl[0] * do[1] - dl[1] * do[0]:.3f}")
print(f"a = {aa:.9f}  b = {bb:.9f}  t_E = {tE:.3f}  t_N = {tN:.3f}")
# misma solución por el sistema lineal 4x4
M = np.array([[loc["C1"][0], -loc["C1"][1], 1, 0], [loc["C1"][1], loc["C1"][0], 0, 1],
              [loc["C2"][0], -loc["C2"][1], 1, 0], [loc["C2"][1], loc["C2"][0], 0, 1]])
sol = np.linalg.solve(M, [ofi["C1"][0], ofi["C1"][1], ofi["C2"][0], ofi["C2"][1]])
print("sistema 4x4 ->", [f"{s:.9f}" for s in sol])
lamA = np.hypot(aa, bb)
thA = np.degrees(np.arctan2(bb, aa))
print(f"lambda = {lamA:.7f}  (ppm = {(lamA - 1) * 1e6:.1f})  theta = {thA:.5f}°")
T = lambda x: np.array([aa * x[0] - bb * x[1] + tE, bb * x[0] + aa * x[1] + tN])
for k in ("C1", "C2"):
    print(f"control {k}: T = {T(loc[k])}  dato {ofi[k]}  dif = {T(loc[k]) - ofi[k]}")
nuevos = {k: T(loc[k]) for k in ("D", "F", "G")}
for k, v in nuevos.items():
    print(f"{k}: local {loc[k]} -> E = {v[0]:.3f}  N = {v[1]:.3f}")
for u, v in (("D", "F"), ("F", "G"), ("G", "D")):
    dloc = np.linalg.norm(loc[v] - loc[u]); dofi = np.linalg.norm(nuevos[v] - nuevos[u])
    print(f"lado {u}{v}: local {dloc:.3f}  oficial {dofi:.3f}  cociente {dofi / dloc:.7f}  dif {dofi - dloc:.3f}")


def ang(Pc, A1, A2):
    u, v = A1 - Pc, A2 - Pc
    return np.degrees(np.arccos(u @ v / np.linalg.norm(u) / np.linalg.norm(v)))


print(f"ángulo DFG local = {ang(loc['F'], loc['D'], loc['G']):.5f}°  oficial = {ang(nuevos['F'], nuevos['D'], nuevos['G']):.5f}°")
pred = T(loc["C3"])
res = ofi["C3"] - pred
print(f"C3 predicho E = {pred[0]:.3f}  N = {pred[1]:.3f}; dato {ofi['C3']}; residuo dE = {res[0]:.3f} dN = {res[1]:.3f}  |r| = {np.linalg.norm(res):.3f}")
a2, b2, tE2, tN2 = helmert("C1", "C3")
print(f"con C1, C3: a = {a2:.9f}  b = {b2:.9f}  t_E = {tE2:.3f}  t_N = {tN2:.3f}  lambda = {np.hypot(a2, b2):.7f}  theta = {np.degrees(np.arctan2(b2, a2)):.5f}°")
T2 = lambda x: np.array([a2 * x[0] - b2 * x[1] + tE2, b2 * x[0] + a2 * x[1] + tN2])
print(f"con C1, C3, C2 predicho = {T2(loc['C2'])}  dif con el dato = {ofi['C2'] - T2(loc['C2'])}  |.| = {np.linalg.norm(ofi['C2'] - T2(loc['C2'])):.3f}")
print(f"D con (C1,C2) {T(loc['D'])}  con (C1,C3) {T2(loc['D'])}  dif {T2(loc['D']) - T(loc['D'])}  |.| = {np.linalg.norm(T2(loc['D']) - T(loc['D'])):.3f}")
dC = [np.linalg.norm(loc[v] - loc[u]) for u, v in (("C1", "C2"), ("C1", "C3"), ("C2", "C3"))]
dO = [np.linalg.norm(ofi[v] - ofi[u]) for u, v in (("C1", "C2"), ("C1", "C3"), ("C2", "C3"))]
print("cocientes de distancias entre controles C1C2, C1C3, C2C3 =", [f"{o / l:.7f}" for o, l in zip(dO, dC)])

# Figura
fig, axs = plt.subplots(1, 2, figsize=(9.0, 4.2))
ordenL = ["C1", "D", "C2", "F", "C3", "G"]
for ax, base, tit, xl, yl in ((axs[0], loc, "sistema local (m)", "x", "y"),
                              (axs[1], {**{k: T(loc[k]) for k in loc}}, "sistema oficial, faja 5 (m)", "E", "N")):
    pts = np.array([base[k] for k in ordenL] + [base[ordenL[0]]])
    off = np.floor(pts[:-1].min(axis=0) / 100) * 100 if ax is axs[1] else np.zeros(2)
    ax.plot(pts[:, 0] - off[0], pts[:, 1] - off[1], color=GRIS, lw=.8, ls=":")
    for k in ordenL:
        v = base[k] - off
        ctrl = k.startswith("C")
        ax.plot(*v, marker="^" if ctrl else "o", ms=8 if ctrl else 6, color=RUST if ctrl else TEAL, zorder=3)
        ax.annotate(k, v, textcoords="offset points", xytext=(6, 5), fontsize=9)
    if ax is axs[1]:
        r3 = ofi["C3"] - off
        ax.plot(*r3, marker="x", ms=8, color=GOLD, mew=2)
        ax.annotate("dato de C3", r3, textcoords="offset points", xytext=(-14, -18), fontsize=8, color="#8a6d10")
        ax.set_xlabel(f"E − {off[0]:.0f}"); ax.set_ylabel(f"N − {off[1]:.0f}")
    else:
        ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.set_title(tit, fontsize=10)
    ax.set_aspect("equal"); ax.grid(color="#e4e2dc", lw=.6)
fig.tight_layout(); fig.savefig(SALIDA / "helmert.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- Ejercicios
print("\n=== X1  dos reflexiones puntuales ===")
a1, b1, x1 = np.array([2, -1.0]), np.array([-1, 2.0]), np.array([4, 3.0])
y1 = 2 * b1 - x1
print("rho_b(x) =", y1, " rho_a(...) =", 2 * a1 - y1, " x + 2(a-b) =", x1 + 2 * (a1 - b1))

print("\n=== X2  paralelogramo ===")
a1, b1, c1 = np.array([1, 0.0]), np.array([3, 1.0]), np.array([5, 4.0])
d1 = a1 - b1 + c1
print("d =", d1, " b-a =", b1 - a1, " c-d =", c1 - d1, " c-b =", c1 - b1, " d-a =", d1 - a1)

print("\n=== X3  reflejo de (3,4) en 2x - y = 1 ===")
n3, x3 = np.array([2, -1.0]), np.array([3, 4.0])
print("n·x - c =", n3 @ x3 - 1, " p =", x3 - (n3 @ x3 - 1) / 5 * n3, " (13/5, 21/5) =", (13 / 5, 21 / 5),
      " reflejo =", refl_recta(n3, 1, x3), " (11/5, 22/5) =", (11 / 5, 22 / 5))

print("\n=== X4  ejes y = 0 y y = 3 ===")
fB = lambda v: refl_recta([0, 1], 0, v); fA = lambda v: refl_recta([0, 1], 3, v)
v0 = np.array([0.7, 1.2])
print("phiA phiB - id =", fA(fB(v0)) - v0, " phiB phiA - id =", fB(fA(v0)) - v0)

print("\n=== X5  ejes a 0° y 30° ===")
print("H(30) H(0) =\n", H(30 * deg) @ H(0), "\nR(60) =\n", R(60 * deg))

print("\n=== X6  T_v R y R T_v, R = R(90°), v = (1,2) ===")
R90, v6 = R(90 * deg), np.array([1, 2.0])
print("R v =", R90 @ v6, " c1 =", np.linalg.solve(np.eye(2) - R90, v6), " c2 =", np.linalg.solve(np.eye(2) - R90, R90 @ v6))

print("\n=== X7  homotecia de centro (4,4), k = 3/2 ===")
o7 = np.array([4, 4.0])
for k, v in (("A", (0, 0)), ("B", (2, 0)), ("C", (0, 2))):
    print(k, "->", o7 + 1.5 * (np.array(v, float) - o7))

print("\n=== X8  similaridad 40°, razón 2, centro (1,1) ===")
o8 = np.array([1, 1.0])
print("H(20) H(0) = R(40)?", np.allclose(H(20 * deg) @ H(0), R(40 * deg)))
print("S(2,1) =", o8 + 2 * R(40 * deg) @ (np.array([2, 1.0]) - o8), " S(1,1) =", o8)

print("\n=== X9  inversa de la transformación de Helmert de A ===")
den = aa ** 2 + bb ** 2
ai, bi = aa / den, -bb / den
print(f"a^2 + b^2 = {den:.9f}  a' = a/(a^2+b^2) = {ai:.9f}  b' = -b/(a^2+b^2) = {bi:.9f}")
print(f"1/lambda = {1 / lamA:.7f}  ángulo inverso = {np.degrees(np.arctan2(bi, ai)):.5f}°")
inv = lambda w: np.array([ai * (w[0] - tE) - bi * (w[1] - tN), bi * (w[0] - tE) + ai * (w[1] - tN)])
for k in ("F",):
    w = np.round(nuevos[k], 3)
    print(f"{k} oficial (redondeado al mm) {w} -> local x = {inv(w)[0]:.3f}  y = {inv(w)[1]:.3f}")
w = ofi["C3"]
print(f"C3 dato oficial {w} -> local x = {inv(w)[0]:.3f}  y = {inv(w)[1]:.3f}  (local medido {loc['C3']})")
