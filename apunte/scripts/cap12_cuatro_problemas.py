"""Números y figuras del capítulo «Cuatro problemas de ajuste».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Recta simple y regresión total por seis puntos»: x = 1..6,
      y = (1, 3, 2, 5, 4, 6); ecuaciones normales, pendiente y|x y x|y, rho^2,
      matriz de dispersión, autovalores, dirección de la regresión total, sumas de
      cuadrados vertical y perpendicular de cada recta.
  E2  Ejemplo «Círculo por siete puntos de un arco»: puntos sintéticos (semilla fija)
      alrededor del círculo de centro (3, 2) y radio 5; ajuste algebraico (D, E, F),
      residuo algebraico perpendicular a las columnas, una iteración de Gauss-Newton y
      convergencia del ajuste geométrico; suma de residuos radiales.
  E3  Ejemplo «Procrustes con cuatro puntos»: nube A y nube B = giro de 30°, traslación
      y redondeo; M = B0^T A0, SVD, R = U V^T, det R, escala, residuos.
  H   En profundidad: Procrustes con escala sobre los tres puntos de control del
      capítulo de similaridades (C1, C2, C3) frente a Helmert lineal por mínimos cuadrados.
  A1  Aplicación: eje de una medianera, diez puntos en Gauss-Krüger faja 5 con error en E
      y en N; recta N|E, recta E|N y regresión total; acimutes y diferencias en segundos.
  A2  Aplicación: rotonda, nueve puntos del cordón; círculo algebraico y geométrico,
      iteraciones de Gauss-Newton, residuos radiales en cm.
  A3  Aplicación: dos levantamientos del mismo predio (seis vértices), Procrustes con
      escala; rotación, traslación, escala, residuos y RMS en cm.
  X1  Ejercicio 1: puntos (0,0), (1,1), (2,1), (3,4): rectas y|x y x|y, rho^2.
  X2  Ejercicio 2: regresión total de los mismos puntos.
  X3  Ejercicio 3: círculo por (0,0), (4,0), (0,2); punto (4, 2,2): residuo algebraico
      y distancia radial.
  X4  Ejercicio 4: Procrustes con un triángulo reflejado (det M < 0).

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/cuatro-problemas/:
  cp_rectas.png      E1: recta simple con residuos verticales y regresión total con
                     residuos perpendiculares, en la misma nube.
  cp_circulo.png     E2: círculo algebraico y geométrico con los residuos radiales.
  cp_procrustes.png  E3: las dos nubes antes y después de llevar A sobre B.
  cp_rotonda.png     A2: residuos radiales de la rotonda, exagerados.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap12_cuatro_problemas.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "cuatro-problemas"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
META = {"Software": None}


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(SALIDA / nombre, dpi=150, facecolor="white", metadata=META)
    plt.close(fig)


def recta_simple(x, y):
    """y = m x + c por ecuaciones normales."""
    A = np.column_stack([x, np.ones_like(x)])
    m, c = np.linalg.solve(A.T @ A, A.T @ y)
    return m, c, A


def regresion_total(P):
    """Centroide, dirección d (mayor valor singular), normal n (menor), sigma^2 menor."""
    cen = P.mean(0)
    X = P - cen
    U, S, Vt = np.linalg.svd(X, full_matrices=False)
    d, n = Vt[0], Vt[1]
    if d[0] < 0:
        d = -d
    return cen, d, n, S


def circulo_algebraico(P):
    A = np.column_stack([P[:, 0], P[:, 1], np.ones(len(P))])
    b = -(P[:, 0] ** 2 + P[:, 1] ** 2)
    D, E, F = np.linalg.solve(A.T @ A, A.T @ b)
    a, bb = -D / 2, -E / 2
    return np.array([D, E, F]), np.array([a, bb, np.sqrt(a * a + bb * bb - F)]), A, b


def gn_paso(P, th):
    a, b, r = th
    d = np.hypot(P[:, 0] - a, P[:, 1] - b)
    f = d - r
    J = np.column_stack([-(P[:, 0] - a) / d, -(P[:, 1] - b) / d, -np.ones(len(P))])
    delta = -np.linalg.solve(J.T @ J, J.T @ f)
    return th + delta, f, J


def circulo_geometrico(P, th0, tol=1e-12, maxit=50):
    th = th0.copy()
    for k in range(1, maxit + 1):
        nuevo, f, J = gn_paso(P, th)
        paso = np.abs(nuevo - th).max()
        th = nuevo
        if paso < tol:
            break
    d = np.hypot(P[:, 0] - th[0], P[:, 1] - th[1])
    f = d - th[2]
    J = np.column_stack([-(P[:, 0] - th[0]) / d, -(P[:, 1] - th[1]) / d, -np.ones(len(P))])
    return th, f, J, k


def procrustes(A, B, escala=True):
    """B ≈ s R A + t, con R rotación (det +1). Filas = puntos."""
    a0, b0 = A.mean(0), B.mean(0)
    A0, B0 = A - a0, B - b0
    M = B0.T @ A0
    U, S, Vt = np.linalg.svd(M)
    dd = np.sign(np.linalg.det(U @ Vt))
    D = np.diag([1.0, dd])
    R = U @ D @ Vt
    s = np.trace(np.diag(S) @ D) / np.sum(A0 ** 2) if escala else 1.0
    t = b0 - s * R @ a0
    res = B - (s * (R @ A.T).T + t)
    return dict(R=R, s=s, t=t, res=res, M=M, U=U, S=S, Vt=Vt, detUVt=np.linalg.det(U @ Vt),
                theta=np.degrees(np.arctan2(R[1, 0], R[0, 0])), A0=A0, B0=B0, a0=a0, b0=b0)


def acimut(dE, dN):
    """Acimut desde el norte, horario, en [0, 180) grados (orientación de una recta)."""
    return np.degrees(np.arctan2(dE, dN)) % 180.0


def gms(g):
    s = round(g * 3600.0, 1)
    G = int(s // 3600); s -= G * 3600
    M = int(s // 60); s -= M * 60
    return f"{G}°{M:02d}'{s:04.1f}\""


# ================================================================ E1
print("=== E1  recta simple y regresión total, seis puntos ===")
x1 = np.arange(1.0, 7.0)
y1 = np.array([1.0, 3, 2, 5, 4, 6])
m1, c1, A1 = recta_simple(x1, y1)
r1 = y1 - A1 @ np.array([m1, c1])
xb, yb = x1.mean(), y1.mean()
Sxx = np.sum((x1 - xb) ** 2); Syy = np.sum((y1 - yb) ** 2); Sxy = np.sum((x1 - xb) * (y1 - yb))
print("A^T A =", (A1.T @ A1).tolist(), " A^T y =", (A1.T @ y1).tolist())
print("medias =", xb, yb, " Sxx, Syy, Sxy =", Sxx, Syy, Sxy)
print(f"recta y|x: m = {m1:.6f} (= 31/35 = {31/35:.6f}), c = {c1:.6f}")
print("residuos verticales =", r1, " suma =", round(r1.sum(), 12), " A^T r =", np.round(A1.T @ r1, 12))
print(f"sum r^2 (vertical, recta y|x) = {r1 @ r1:.6f}  (= Syy - Sxy^2/Sxx = {Syy - Sxy**2/Sxx:.6f})")
mx = Sxy / Syy
print(f"recta x|y: dx/dy = {mx:.6f}; escrita y = ...: pendiente {1/mx:.6f} (= 35/31)")
print(f"producto m_yx * (dx/dy) = {m1*mx:.6f} = rho^2; rho = {Sxy/np.sqrt(Sxx*Syy):.6f}")
P1 = np.column_stack([x1, y1])
cen1, d1, n1, S1 = regresion_total(P1)
C1 = (P1 - cen1).T @ (P1 - cen1)
lam1 = np.linalg.eigvalsh(C1)
print("matriz de dispersión C = X0^T X0 =", C1.tolist(), " autovalores =", lam1, " sigma^2 =", S1 ** 2)
print("dirección d =", d1, " normal n =", n1, " pendiente total =", d1[1] / d1[0])
dperp_tot = (P1 - cen1) @ n1
print("distancias perpendiculares a la total =", np.round(dperp_tot, 6), " suma cuadrados =", round(dperp_tot @ dperp_tot, 6))
nsimple = np.array([-m1, 1.0]) / np.hypot(1, m1)
dperp_simple = (P1 - np.array([0, c1])) @ nsimple
print(f"suma de cuadrados perpendiculares a la recta y|x = {dperp_simple @ dperp_simple:.6f}")
vert_tot = y1 - (yb + (x1 - xb) * d1[1] / d1[0])
print(f"suma de cuadrados verticales a la total = {vert_tot @ vert_tot:.6f}")
print("C n =", C1 @ n1, " = lambda_min n:", np.allclose(C1 @ n1, lam1[0] * n1), " d.n =", round(d1 @ n1, 12))

fig, axs = plt.subplots(1, 2, figsize=(9.4, 4.2), sharey=True)
xx = np.array([0.3, 6.7])
for ax, modo in zip(axs, ("simple", "total")):
    ax.plot(xx, m1 * xx + c1, color=RUST if modo == "simple" else "#e3b8ac", lw=2.2 if modo == "simple" else 1.2,
            ls="-" if modo == "simple" else "--", label=fr"simple $y|x$: $y={m1:.3f}x{c1:+.3f}$".replace(".", "{,}"))
    ax.plot(xx, yb + (xx - xb) * d1[1] / d1[0], color=TEAL if modo == "total" else "#9cc6cf",
            lw=2.2 if modo == "total" else 1.2, ls="-" if modo == "total" else "--", label="total: $y=x$")
    if modo == "simple":
        for xi, yi in zip(x1, y1):
            ax.plot([xi, xi], [yi, m1 * xi + c1], color=RUST, lw=1, ls=":")
        ax.set_title("residuos verticales (recta simple)", fontsize=10)
    else:
        for p, dd in zip(P1, dperp_tot):
            q = p - dd * n1
            ax.plot([p[0], q[0]], [p[1], q[1]], color=TEAL, lw=1, ls=":")
        ax.set_title("residuos perpendiculares (regresión total)", fontsize=10)
    ax.plot(x1, y1, "o", color="#333333", ms=5, zorder=5)
    ax.plot(*cen1, "+", color=GOLD, ms=12, mew=2, zorder=6)
    ax.set_aspect("equal"); ax.set_xlim(0, 7); ax.set_ylim(0, 7)
    ax.grid(color="#e6e3dc", lw=.6); ax.legend(loc="upper left", fontsize=8, frameon=False)
    ax.set_xlabel("$x$")
axs[0].set_ylabel("$y$")
guardar(fig, "cp_rectas.png")

# ================================================================ E2
print("\n=== E2  círculo por siete puntos de un arco ===")
rng = np.random.default_rng(1212)
ang = np.radians(np.array([-20.0, 15, 50, 85, 120, 155, 190]))
P2 = np.column_stack([3 + 5 * np.cos(ang), 2 + 5 * np.sin(ang)]) + 0.15 * rng.normal(size=(7, 2))
P2 = np.round(P2, 2)
print("puntos =\n", P2)
DEF2, th2a, A2, b2 = circulo_algebraico(P2)
ra2 = b2 - A2 @ DEF2
print("(D, E, F) =", DEF2, " centro algebraico =", th2a[:2], " radio =", th2a[2])
print("A^T (residuo algebraico) =", np.round(A2.T @ ra2, 10))
d2a = np.hypot(P2[:, 0] - th2a[0], P2[:, 1] - th2a[1])
print("residuo algebraico x^2+y^2+Dx+Ey+F =", np.round(-ra2, 4), " d^2 - r^2 =", np.round(d2a**2 - th2a[2]**2, 4))
f2a = d2a - th2a[2]
print("residuos radiales con el algebraico =", np.round(f2a, 4), " suma =", round(f2a.sum(), 4), " suma cuad =", round(f2a @ f2a, 6))
th2_1, f0, J0 = gn_paso(P2, th2a)
print("Gauss-Newton: J^T J =\n", J0.T @ J0, "\n J^T f =", J0.T @ f0, "\n delta =", th2_1 - th2a)
print("tras una iteración: centro =", th2_1[:2], " radio =", th2_1[2])
th2g, f2g, J2g, it2 = circulo_geometrico(P2, th2a)
print(f"convergido en {it2} iteraciones: centro =", th2g[:2], " radio =", th2g[2])
print("diferencia una iteración - convergido =", th2_1 - th2g)
print("residuos radiales geométricos =", np.round(f2g, 4), " suma =", round(f2g.sum(), 12),
      " suma cuad =", round(f2g @ f2g, 6), " J^T f =", np.round(J2g.T @ f2g, 12))

fig, ax = plt.subplots(figsize=(5.6, 5.0))
tt = np.linspace(0, 2 * np.pi, 400)
ax.plot(th2a[0] + th2a[2] * np.cos(tt), th2a[1] + th2a[2] * np.sin(tt), color=GOLD, lw=1.2, ls="--", label="ajuste algebraico")
ax.plot(th2g[0] + th2g[2] * np.cos(tt), th2g[1] + th2g[2] * np.sin(tt), color=TEAL, lw=2, label="ajuste geométrico")
for p, f in zip(P2, f2g):
    u = (p - th2g[:2]) / np.hypot(*(p - th2g[:2]))
    q = th2g[:2] + th2g[2] * u
    ax.annotate("", q + 5 * f * u, q, arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.6), zorder=6)
    ax.plot([th2g[0], q[0]], [th2g[1], q[1]], color="#d8d5ce", lw=.7, zorder=0)
ax.plot(P2[:, 0], P2[:, 1], "o", color="#333333", ms=3.5, zorder=4, label="puntos")
ax.plot(*th2g[:2], "+", color=TEAL, ms=12, mew=2)
ax.plot(*th2a[:2], "x", color=GOLD, ms=8, mew=1.5)
ax.set_aspect("equal"); ax.grid(color="#e6e3dc", lw=.6)
ax.legend(loc="lower left", fontsize=8, frameon=False)
ax.set_title("residuos radiales al círculo geométrico (flechas ×5)", fontsize=10)
guardar(fig, "cp_circulo.png")

# ================================================================ E3
print("\n=== E3  Procrustes con cuatro puntos ===")
A3 = np.array([[0.0, 0], [4, 0], [4, 2], [0, 3]])
th = np.radians(30.0)
R30 = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
B3 = (R30 @ A3.T).T + np.array([6.0, 1.0])
B3 = np.round(B3 + np.array([[0.05, -0.04], [-0.03, 0.06], [0.04, 0.02], [-0.06, -0.04]]), 2)
print("A =\n", A3, "\nB =\n", B3)
pr3 = procrustes(A3, B3, escala=False)
print("centroides a0 =", pr3["a0"], " b0 =", pr3["b0"])
print("M = B0^T A0 =\n", pr3["M"])
print("U =\n", pr3["U"], "\nSigma =", pr3["S"], "\nV^T =\n", pr3["Vt"], "\ndet(U V^T) =", round(pr3["detUVt"], 10))
print("R =\n", pr3["R"], " theta =", pr3["theta"], " det R =", round(np.linalg.det(pr3["R"]), 12))
print("t =", pr3["t"])
print("residuos =\n", pr3["res"], "\n suma =", np.round(pr3["res"].sum(0), 12),
      " sum |r|^2 =", round(np.sum(pr3["res"] ** 2), 6))
M3 = pr3["M"]
print("2D: atan2(M21-M12, M11+M22) =", np.degrees(np.arctan2(M3[1, 0] - M3[0, 1], M3[0, 0] + M3[1, 1])))
pr3s = procrustes(A3, B3, escala=True)
print("con escala: s =", pr3s["s"], " theta =", pr3s["theta"], " sum |r|^2 =", round(np.sum(pr3s["res"] ** 2), 6))
Rp = (pr3["R"] @ pr3["A0"].T).T
print("sum r_i x (R a0_i) =", round(np.sum(pr3["res"][:, 0] * Rp[:, 1] - pr3["res"][:, 1] * Rp[:, 0]) * -1, 12))

fig, axs = plt.subplots(1, 2, figsize=(9.4, 4.0), sharex=True, sharey=True)
lleva = (pr3["R"] @ A3.T).T + pr3["t"]
for ax, tit in zip(axs, ("antes: dos nubes homólogas", "después: $R\\,a_i+t$ sobre $b_i$")):
    ax.fill(*B3.T, fc="#e8d3cc", ec=RUST, lw=1.5, label="nube $B$")
    if tit.startswith("antes"):
        ax.fill(*A3.T, fc="#d4e6e9", ec=TEAL, lw=1.5, label="nube $A$")
        for a, b in zip(A3, B3):
            ax.plot([a[0], b[0]], [a[1], b[1]], color=GRIS, lw=.7, ls=":")
    else:
        ax.fill(*lleva.T, fc="none", ec=TEAL, lw=1.8, label="$A$ llevada")
        for a, b in zip(lleva, B3):
            ax.plot([a[0], b[0]], [a[1], b[1]], color=RUST, lw=1.5)
    for k, b in enumerate(B3):
        ax.text(b[0] + .12, b[1] + .12, f"$b_{k+1}$", color=RUST, fontsize=9)
    ax.set_aspect("equal"); ax.grid(color="#e6e3dc", lw=.6); ax.set_title(tit, fontsize=10)
    ax.legend(loc="upper left", fontsize=8, frameon=False)
guardar(fig, "cp_procrustes.png")

# ================================================================ H
print("\n=== H  Procrustes con escala sobre C1, C2, C3 (capítulo de similaridades) ===")
loc = np.array([[50.0, 20.0], [310.0, 145.0], [120.0, 260.0]])
ofi = np.array([[5432134.871, 6154341.048], [5432306.387, 6154573.065], [5432084.658, 6154585.953]])
ob = ofi.mean(0)
print("baricentro oficial =", np.round(ob, 4), " baricentro local =", loc.mean(0))
prH = procrustes(loc, ofi - ob, escala=True)
print(f"Procrustes: s = {prH['s']:.7f}  theta = {prH['theta']:.5f}°  t (reducida) = {prH['t']}")
print("t completa =", np.round(prH["t"] + ob, 3))
print("residuos (m) =\n", np.round(prH["res"], 4), "\n suma =", np.round(prH["res"].sum(0), 12),
      " RMS punto =", round(np.sqrt(np.sum(prH["res"] ** 2) / 3), 4))
# Helmert lineal: E = a x - b y + tE, N = b x + a y + tN
rows, rhs = [], []
for (x, y), (E, N) in zip(loc, ofi - ob):
    rows += [[x, -y, 1, 0], [y, x, 0, 1]]; rhs += [E, N]
AH = np.array(rows); bH = np.array(rhs)
solH = np.linalg.solve(AH.T @ AH, AH.T @ bH)
print("Helmert MC: a, b, tE, tN =", solH, " lambda =", np.hypot(solH[0], solH[1]),
      " theta =", np.degrees(np.arctan2(solH[1], solH[0])))
print("diferencia s cos, s sin - (a, b) =", prH["s"] * prH["R"][1, 0] - solH[1], prH["s"] * prH["R"][0, 0] - solH[0])
rH = bH - AH @ solH
print("A^T r Helmert =", np.round(AH.T @ rH, 8), " sum r^2 =", round(rH @ rH, 8), " Procrustes sum r^2 =", round(np.sum(prH["res"]**2), 8))
L0 = loc - loc.mean(0); O0 = ofi - ob - (ofi - ob).mean(0)
print("a = sum p.q/sum|p|^2 =", np.sum(L0 * O0) / np.sum(L0**2), " b = sum p x q/sum|p|^2 =",
      np.sum(L0[:, 0] * O0[:, 1] - L0[:, 1] * O0[:, 0]) / np.sum(L0**2))

# ================================================================ A1
print("\n=== A1  eje de una medianera ===")
rng = np.random.default_rng(5412)
az_g = 41.5
E0, N0 = 5434512.0, 6152846.0
u_az = np.array([np.sin(np.radians(az_g)), np.cos(np.radians(az_g))])
s_ = np.linspace(0, 18, 10)
Pm = np.array([E0, N0]) + s_[:, None] * u_az + 0.03 * rng.normal(size=(10, 2))
Pm = np.round(Pm, 3)
print("puntos (E, N) =")
for k, p in enumerate(Pm, 1):
    print(f"  {k:2d}  {p[0]:.3f}  {p[1]:.3f}")
bm = Pm.mean(0)
Xm = Pm - bm
print("baricentro =", np.round(bm, 4))
print("reducidas =\n", np.round(Xm, 3))
SEE = np.sum(Xm[:, 0] ** 2); SNN = np.sum(Xm[:, 1] ** 2); SEN = np.sum(Xm[:, 0] * Xm[:, 1])
print("S_EE, S_NN, S_EN =", round(SEE, 4), round(SNN, 4), round(SEN, 4))
mNE = SEN / SEE; mEN = SEN / SNN
azNE = acimut(1.0, mNE); azEN = acimut(mEN, 1.0)
cenm, dm, nm, Sm = regresion_total(Pm)
azT = acimut(dm[0], dm[1])
print(f"N|E: dN/dE = {mNE:.6f}  acimut = {azNE:.6f}° = {gms(azNE)}")
print(f"E|N: dE/dN = {mEN:.6f}  acimut = {azEN:.6f}° = {gms(azEN)}")
print(f"total: d = {dm}  acimut = {azT:.6f}° = {gms(azT)}  sigma = {Sm}")
print(f"diferencias: N|E - total = {(azNE-azT)*3600:.1f}\"  E|N - total = {(azEN-azT)*3600:.1f}\"  N|E - E|N = {(azNE-azEN)*3600:.1f}\"")
rNE = Xm[:, 1] - mNE * Xm[:, 0]
print("residuos N|E (cm) =", np.round(100 * rNE, 2), " suma =", round(rNE.sum(), 12), " sum r*E =", round(np.sum(rNE * Xm[:, 0]), 10))
dT = Xm @ nm
print("dist. perpendiculares a la total (cm) =", np.round(100 * dT, 2), " suma =", round(dT.sum(), 12),
      " RMS =", round(100 * np.sqrt(dT @ dT / 10), 2), " cm; sum (d.X)(n.X) =", round(np.sum((Xm @ dm) * dT), 10))
print("eje generado con acimut", az_g, "° (dato sintético); total - generado =", round((azT - az_g) * 3600, 1), "\"")
sig0m = Sm[1] / np.sqrt(10 - 2)
print(f"sigma0 = sigma_min/sqrt(n-2) = {100*sig0m:.2f} cm; desvío del acimut ~ sigma0/sigma_max = {sig0m/Sm[0]:.3e} rad = {np.degrees(sig0m/Sm[0])*3600:.0f}\"")
# rotación del sistema: rotar 30°, recalcular
phi = np.radians(30.0)
Rot = np.array([[np.cos(phi), -np.sin(phi)], [np.sin(phi), np.cos(phi)]])
Xr = (Rot @ Xm.T).T
mr = np.sum(Xr[:, 0] * Xr[:, 1]) / np.sum(Xr[:, 0] ** 2)
_, dr, _, _ = regresion_total(Xr)
ang_simple_rot = np.degrees(np.arctan2(mr, 1)) - 30.0
ang_simple = np.degrees(np.arctan2(mNE, 1))
ang_tot_rot = np.degrees(np.arctan2(dr[1], dr[0])) - 30.0
ang_tot = np.degrees(np.arctan2(dm[1], dm[0]))
print(f"girando los ejes 30°: la simple cambia la dirección en {(ang_simple_rot-ang_simple)*3600:.1f}\"; la total en {(ang_tot_rot-ang_tot)*3600:.2e}\"")

# ================================================================ A2
print("\n=== A2  rotonda ===")
rng = np.random.default_rng(1405)
Ec, Nc, Rr = 5434655.0, 6152931.0, 14.0
angr = np.radians(np.array([100.0, 122, 145, 168, 190, 213, 236, 258, 280]))
Pr = np.column_stack([Ec + Rr * np.sin(angr), Nc + Rr * np.cos(angr)])
Pr = Pr + 0.02 * rng.normal(size=Pr.shape)
Pr = np.round(Pr, 3)
br = Pr.mean(0)
Xr2 = Pr - br
print("puntos (E, N) =")
for k, p in enumerate(Pr, 1):
    print(f"  {k}  {p[0]:.3f}  {p[1]:.3f}   reducidas {p[0]-br[0]:.3f} {p[1]-br[1]:.3f}")
print("baricentro =", np.round(br, 4))
DEFr, thra, Ara, bra = circulo_algebraico(Xr2)
print("(D, E, F) =", DEFr, " centro alg (red) =", thra[:2], " radio =", thra[2])
print("A^T r alg =", np.round(Ara.T @ (bra - Ara @ DEFr), 8))
th1r, _, _ = gn_paso(Xr2, thra)
thrg, frg, Jrg, itr = circulo_geometrico(Xr2, thra)
print("una iteración GN: ", th1r, " convergido (", itr, "it):", thrg)
print("centro geométrico completo =", np.round(thrg[:2] + br, 4), " radio =", round(thrg[2], 4))
print("diferencia alg - geom (mm): centro", np.round(1000 * (thra[:2] - thrg[:2]), 2), " radio", round(1000 * (thra[2] - thrg[2]), 2))
print("diferencia 1 it - convergido (mm):", np.round(1000 * (th1r - thrg), 4))
fra = np.hypot(Xr2[:, 0] - thra[0], Xr2[:, 1] - thra[1]) - thra[2]
print("residuos radiales alg (cm) =", np.round(100 * fra, 2))
print("residuos radiales geom (cm) =", np.round(100 * frg, 2), " suma =", round(frg.sum(), 12),
      " RMS =", round(100 * np.sqrt(frg @ frg / 9), 2), " cm, max |r| =", round(100 * np.abs(frg).max(), 2), " J^T f =", np.round(Jrg.T @ frg, 12))
sig0 = np.sqrt(frg @ frg / (9 - 3))
cov = sig0 ** 2 * np.linalg.inv(Jrg.T @ Jrg)
print("sigma0 (cm) =", round(100 * sig0, 2), " desvíos centro E, N, radio (cm) =", np.round(100 * np.sqrt(np.diag(cov)), 2))
print("rotonda generada con radio", Rr, "m (dato sintético)")

fig, ax = plt.subplots(figsize=(5.4, 5.0))
ex = 100.0
ax.plot(thrg[0] + thrg[2] * np.cos(tt), thrg[1] + thrg[2] * np.sin(tt), color=TEAL, lw=2, label="círculo geométrico")
for k, (p, f) in enumerate(zip(Xr2, frg), 1):
    u = (p - thrg[:2]) / np.hypot(*(p - thrg[:2]))
    q = thrg[:2] + thrg[2] * u
    tip = q + ex * f * u
    ax.annotate("", tip, q, arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.6))
    ax.plot(*q, "o", color="#333333", ms=4, zorder=5)
    ax.text(*(thrg[:2] + (thrg[2] + 3.2) * u), f"{k}\n{100*f:+.1f}".replace(".", ","), ha="center", va="center", fontsize=8)
ax.plot(*thrg[:2], "+", color=TEAL, ms=12, mew=2)
ax.set_aspect("equal"); ax.grid(color="#e6e3dc", lw=.6)
ax.set_xlim(thrg[0] - 21, thrg[0] + 21); ax.set_ylim(thrg[1] - 21, thrg[1] + 21)
ax.set_xlabel("$E-\\bar E$ (m)"); ax.set_ylabel("$N-\\bar N$ (m)")
ax.set_title("residuos radiales en cm (flechas ×100)", fontsize=10)
guardar(fig, "cp_rotonda.png")

# ================================================================ A3
print("\n=== A3  dos levantamientos del mismo predio ===")
rng = np.random.default_rng(3141)
V1 = np.array([[5434720.412, 6153018.237], [5434748.905, 6153041.118], [5434771.364, 6153013.552],
               [5434766.020, 6152982.774], [5434739.181, 6152969.405], [5434718.733, 6152990.861]])
b1 = V1.mean(0)
V10 = V1 - b1
thl = np.radians(-63.25)
Rl = np.array([[np.cos(thl), -np.sin(thl)], [np.sin(thl), np.cos(thl)]])
sl = 1.0 - 120e-6
V2 = sl * (Rl @ V10.T).T + np.array([1000.0 + 31.2, 1000.0 - 4.7]) + 0.02 * rng.normal(size=V10.shape)
V2 = np.round(V2, 3)
print("levantamiento 1 (E, N) y 2 (x, y):")
for k, (p, q) in enumerate(zip(V1, V2), 1):
    print(f"  V{k}  {p[0]:.3f} {p[1]:.3f}   red {p[0]-b1[0]:.3f} {p[1]-b1[1]:.3f}   lev2 {q[0]:.3f} {q[1]:.3f}")
print("baricentro lev 1 =", np.round(b1, 4), " baricentro lev 2 =", np.round(V2.mean(0), 4))
prA = procrustes(V2, V10, escala=True)   # lev 1 (reducido) ≈ s R lev2 + t
print("M =\n", prA["M"], "\n Sigma =", prA["S"], " det(UV^T) =", round(prA["detUVt"], 10))
print(f"R: theta = {prA['theta']:.6f}° = {gms(prA['theta'] % 360)}  det R = {np.linalg.det(prA['R']):.12f}")
print(f"s = {prA['s']:.8f}  ({(prA['s']-1)*1e6:.1f} ppm)")
print("t (reducida) =", np.round(prA["t"], 4), " t completa =", np.round(prA["t"] + b1, 3))
print("residuos (cm) =\n", np.round(100 * prA["res"], 2))
print("suma residuos =", np.round(prA["res"].sum(0), 12))
nr = np.hypot(prA["res"][:, 0], prA["res"][:, 1])
print("módulos (cm) =", np.round(100 * nr, 2), " RMS por punto =", round(100 * np.sqrt(np.sum(nr ** 2) / 6), 2),
      " cm; RMS por coordenada =", round(100 * np.sqrt(np.sum(nr ** 2) / 12), 2), " cm")
prA1 = procrustes(V2, V10, escala=False)
print("sin escala: theta =", round(prA1["theta"], 6), " RMS punto (cm) =", round(100 * np.sqrt(np.sum(prA1["res"] ** 2) / 6), 2))
Rp = (prA["R"] @ prA["A0"].T).T
print("sum r x (s R a0) =", round(np.sum(Rp[:, 0] * prA["res"][:, 1] - Rp[:, 1] * prA["res"][:, 0]), 10),
      " sum r.(R a0) =", round(np.sum(Rp * prA["res"]), 10))
print("datos sintéticos: giro", np.degrees(thl), "°, escala", sl)

# ================================================================ X1, X2
print("\n=== X1/X2  puntos (0,0), (1,1), (2,1), (3,4) ===")
xx1 = np.array([0.0, 1, 2, 3]); yy1 = np.array([0.0, 1, 1, 4])
mX, cX, AX = recta_simple(xx1, yy1)
xbX, ybX = xx1.mean(), yy1.mean()
sxx = np.sum((xx1 - xbX) ** 2); syy = np.sum((yy1 - ybX) ** 2); sxy = np.sum((xx1 - xbX) * (yy1 - ybX))
print("medias", xbX, ybX, " Sxx Syy Sxy", sxx, syy, sxy, " y|x: m, c =", mX, cX)
rX = yy1 - AX @ np.array([mX, cX])
print("residuos =", rX, " suma =", round(rX.sum(), 12), " sum r^2 =", round(rX @ rX, 6))
print("x|y: dx/dy =", sxy / syy, " pendiente como y(x) =", syy / sxy, " rho^2 =", sxy ** 2 / (sxx * syy))
PX = np.column_stack([xx1, yy1])
cX2, dX, nX, SX = regresion_total(PX)
CX = (PX - cX2).T @ (PX - cX2)
lX = np.linalg.eigvalsh(CX)
print("C =", CX.tolist(), " autovalores =", lX, " (7 ± sqrt 40 =", 7 + np.sqrt(40), 7 - np.sqrt(40), ")")
print("pendiente total =", dX[1] / dX[0], " = (lambda1 - Sxx)/Sxy =", (lX[1] - sxx) / sxy, " sum d^2 =", lX[0])

# ================================================================ X3
print("\n=== X3  círculo por tres puntos ===")
P3x = np.array([[0.0, 0], [4, 0], [0, 2]])
A3x = np.column_stack([P3x, np.ones(3)])
DEF3 = np.linalg.solve(A3x, -(P3x ** 2).sum(1))
print("(D, E, F) =", DEF3, " centro =", -DEF3[:2] / 2, " r =", np.sqrt((DEF3[:2] ** 2).sum() / 4 - DEF3[2]))
q = np.array([4.0, 2.2])
alg = q @ q + DEF3[:2] @ q + DEF3[2]
dq = np.hypot(*(q - (-DEF3[:2] / 2)))
rr = np.sqrt(5.0)
print("residuo algebraico =", alg, " d =", dq, " d - r =", dq - rr, " (d-r)(d+r) =", (dq - rr) * (dq + rr), " 2r(d-r) =", 2 * rr * (dq - rr))

# ================================================================ X4
print("\n=== X4  Procrustes con triángulo reflejado ===")
A4 = np.array([[0.0, 0], [2, 0], [0, 1]]); B4 = np.array([[0.0, 0], [-2, 0], [0, 1]])
p4 = procrustes(A4, B4, escala=False)
M4 = p4["M"]
print("A0 =\n", p4["A0"], "\nB0 =\n", p4["B0"], "\nM = B0^T A0 =\n", M4, " (x9:", 9 * M4, ") det M =", np.linalg.det(M4))
U4, S4, Vt4 = np.linalg.svd(M4)
print("Sigma =", S4, " det(UV^T) =", round(np.linalg.det(U4 @ Vt4), 10), " U V^T =\n", np.round(U4 @ Vt4, 10))
print("R corregida =\n", p4["R"], " theta =", p4["theta"], " atan2 =", np.degrees(np.arctan2(M4[1, 0] - M4[0, 1], M4[0, 0] + M4[1, 1])))
nA = np.sum(p4["A0"] ** 2); nB = np.sum(p4["B0"] ** 2)
trmax = np.hypot(M4[0, 0] + M4[1, 1], M4[1, 0] - M4[0, 1])
print("|A0|^2 =", nA, " |B0|^2 =", nB, " max tr =", trmax, " = sigma1 - sigma2 =", S4[0] - S4[1],
      " sum|r|^2 =", nA + nB - 2 * trmax, " (script:", np.sum(p4["res"] ** 2), ")")
print("con la reflexión UV^T: sum|r|^2 =", np.sum((p4["B0"] - (U4 @ Vt4 @ p4["A0"].T).T) ** 2))
print("\nFiguras en", SALIDA.relative_to(Path.cwd()) if SALIDA.is_relative_to(Path.cwd()) else SALIDA)
