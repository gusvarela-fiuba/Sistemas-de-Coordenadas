"""Números y figuras del capítulo «La derivada como aproximación lineal: jacobiano, gradiente y hessiana».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  I   La idea: escalera R -> R^2 -> R^n. sqrt(x) cerca de x = 100 con h = 0,5;
      f(x,y) = x^2 y cerca de (1,2) con el pasito (0,1; -0,1) (gradiente como fila).
  E1  Ejemplo «Jacobiano de polares a cartesianas»: P(r,t) = (r cos t, r sin t) en
      r = 2, t = 30°; J, det J = r; rectangulito dr = 0,1, dt = 0,05 rad: vértices exactos
      contra J (dr, dt), área exacta del trapecio polar contra r dr dt.
  E2  Ejemplo «Distancia y acimut desde una estación»: G(E,N) = (d, Az) con
      (dE, dN) = (300, 400) m; J_G, su inversa J_F de F(d,Az) = (E0 + d sin Az, N0 + d cos Az),
      producto J_G J_F = I; pasito (0,10; -0,05) m: lineal contra exacto (Δd, ΔAz en ″).
  E3  Ejemplo «Hessiana de h(x,y) = x^3 - 3xy + y^3»: puntos críticos (0,0) y (1,1),
      hessianas, autovalores y autovectores, clasificación; comprobación de segundo orden
      con el pasito (0,1; 0,1) desde (1,1) y (0,1; -0,1) desde (0,0).
  E4  Ejemplo «Newton para intersecar dos circunferencias»: A = (0,0), B = (100,0),
      dA = 80, dB = 60, arranque (60,40); primera iteración a mano y tabla de iteraciones.
  A   Aplicación topográfica: propagación de errores de una radiación. Estación en
      Gauss-Krüger faja 5, d = 1500 m, Az = 52°30'00", sigma_d = 3 mm + 2 ppm,
      sigma_Az = 5"; J, Sigma_EN, autovalores/autovectores (semiejes y orientación);
      simulación Monte Carlo con 10 000 pares (semilla 2026); tabla d = 500..2000 m;
      distancia a partir de la cual domina el error transversal.
  X1  Ejercicio 1: F(x,y) = (x^2 - y, xy) en (2,1); aproximación de F(2,1; 0,9).
  X2  Ejercicio 2: regla de la cadena para h = xy en polares, r = 2, t = 30°.
  X3  Ejercicio 3: h(x,y) = 100 - x^2 + xy - 2y^2: punto crítico y clasificación.
  X4  Ejercicio 4: Newton para A = (0,0), B = (50,0), dA = 30, dB = 40 desde (20,20).
  X5  Ejercicio 5: radiación d = 800 m, Az = 300°, sigma_d = 3 mm + 2 ppm, sigma_Az = 10".

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/derivada/:
  der_polar.png        rectángulo (dr, dt) en el plano (r, t) y su imagen curva con el
                       paralelogramo tangente J (dr, dt).
  der_hessiana.png     curvas de nivel de h cerca de la cuenca (1,1) y de la silla (0,0),
                       con las de la aproximación de segundo orden y los autovectores.
  der_newton.png       iteraciones de Newton hacia la intersección de dos circunferencias.
  der_radiacion.png    nube simulada del punto radiado y elipse de un desvío J Sigma J^T.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap10_derivada_jacobiano.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Ellipse

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "derivada"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
SEG = np.pi / (180 * 3600)  # un segundo sexagesimal en radianes


def titulo(t):
    print("\n" + "=" * 8 + " " + t)


# ---------------------------------------------------------------- I
titulo("I  la idea: escalera")
x0, h = 100.0, 0.5
print(f"sqrt(100,5) exacto = {np.sqrt(x0 + h):.6f}; lineal 10 + h/20 = {10 + h / 20:.6f}; "
      f"error = {np.sqrt(x0 + h) - 10 - h / 20:.2e}")
f2 = lambda x, y: x**2 * y
p, v = np.array([1.0, 2.0]), np.array([0.1, -0.1])
grad = np.array([2 * p[0] * p[1], p[0] ** 2])
print(f"f(x,y) = x^2 y en (1,2): f = {f2(*p)}, fila = {grad}, df(v) = {grad @ v:.4f}, "
      f"cambio real = {f2(*(p + v)) - f2(*p):.4f}")

# ---------------------------------------------------------------- E1
titulo("E1 polares -> cartesianas")
P = lambda r, t: np.array([r * np.cos(t), r * np.sin(t)])
JP = lambda r, t: np.array([[np.cos(t), -r * np.sin(t)], [np.sin(t), r * np.cos(t)]])
r0, t0 = 2.0, np.radians(30)
dr, dt = 0.1, 0.05
J1 = JP(r0, t0)
print("P(r0,t0) =", P(r0, t0))
print("J =\n", J1, "\ndet J =", np.linalg.det(J1))
for nombre, paso in (("(dr,0)", (dr, 0)), ("(0,dt)", (0, dt)), ("(dr,dt)", (dr, dt))):
    exacto = P(r0 + paso[0], t0 + paso[1]) - P(r0, t0)
    lineal = J1 @ np.array(paso)
    print(f"  paso {nombre}: exacto {exacto.round(4)}  lineal {lineal.round(4)}  "
          f"diferencia {np.linalg.norm(exacto - lineal):.4f}")
area_exacta = dt * ((r0 + dr) ** 2 - r0**2) / 2
print(f"área exacta del trapecio polar = {area_exacta:.5f}; r dr dt = {r0 * dr * dt:.5f}; "
      f"área (r+dr/2) dr dt = {(r0 + dr / 2) * dr * dt:.5f}")

# ---------------------------------------------------------------- E2
titulo("E2 distancia y acimut")
dE, dN = 300.0, 400.0
d = np.hypot(dE, dN)
Az = np.arctan2(dE, dN)
JG = np.array([[dE / d, dN / d], [dN / d**2, -dE / d**2]])
JF = np.array([[np.sin(Az), d * np.cos(Az)], [np.cos(Az), -d * np.sin(Az)]])
print(f"d = {d}, Az = {np.degrees(Az):.4f}° , det J_G = {np.linalg.det(JG):.6f} (= -1/d = {-1 / d})")
print("J_G =\n", JG, "\nJ_F =\n", JF, "\nJ_G J_F =\n", JG @ JF, "\ninv(J_F) =\n", np.linalg.inv(JF))
paso = np.array([0.10, -0.05])
lin = JG @ paso
dE2, dN2 = dE + paso[0], dN + paso[1]
ex = np.array([np.hypot(dE2, dN2) - d, np.arctan2(dE2, dN2) - Az])
print(f"pasito {paso}: lineal Δd = {lin[0]:.5f} m, ΔAz = {lin[1]:.6e} rad = {lin[1] / SEG:.2f}″")
print(f"            exacto Δd = {ex[0]:.5f} m, ΔAz = {ex[1]:.6e} rad = {ex[1] / SEG:.2f}″")

# ---------------------------------------------------------------- E3
titulo("E3 hessiana")
hfun = lambda x, y: x**3 - 3 * x * y + y**3
gradh = lambda x, y: np.array([3 * x**2 - 3 * y, 3 * y**2 - 3 * x])
Hh = lambda x, y: np.array([[6 * x, -3.0], [-3.0, 6 * y]])
for pc, vv in (((0.0, 0.0), np.array([0.1, -0.1])), ((1.0, 1.0), np.array([0.1, 0.1])),
               ((0.0, 0.0), np.array([0.1, 0.1])), ((1.0, 1.0), np.array([0.1, -0.1]))):
    H = Hh(*pc)
    lam, V = np.linalg.eigh(H)
    real = hfun(*(np.array(pc) + vv)) - hfun(*pc)
    print(f"punto {pc}: h = {hfun(*pc)}, grad = {gradh(*pc)}, H = {H.tolist()}, autovalores {lam}, "
          f"autovectores (columnas)\n{V}")
    print(f"   pasito {vv}: (1/2) v^T H v = {0.5 * vv @ H @ vv:.4f}; cambio real = {real:.4f}")

# ---------------------------------------------------------------- E4
titulo("E4 Newton, dos circunferencias")


def newton(A, B, dA, dB, x0, n=6, verbose=True):
    x = np.array(x0, dtype=float)
    hist = [x.copy()]
    for k in range(n):
        uA, uB = x - A, x - B
        lA, lB = np.linalg.norm(uA), np.linalg.norm(uB)
        F = np.array([lA - dA, lB - dB])
        J = np.vstack([uA / lA, uB / lB])
        delta = np.linalg.solve(J, -F)
        if verbose:
            print(f" it {k}: x = {x.round(6)}, dist = ({lA:.4f}, {lB:.4f}), F = {F.round(4)}")
            if k == 0:
                print("   J =\n", J.round(5), "\n   det J =", round(np.linalg.det(J), 5),
                      "\n   delta =", delta.round(4))
        x = x + delta
        hist.append(x.copy())
    if verbose:
        for k, xk in enumerate(hist):
            print(f"   x_{k} = ({xk[0]:.6f}, {xk[1]:.6f})   error = {np.linalg.norm(xk - hist[-1]):.2e}")
    return np.array(hist)


A, B = np.array([0.0, 0.0]), np.array([100.0, 0.0])
hist4 = newton(A, B, 80.0, 60.0, (60.0, 40.0), n=5)

# ---------------------------------------------------------------- A
titulo("A  propagación de errores de una radiación")
E0, N0 = 5_512_340.00, 6_172_480.00
dA_, AzA = 1500.0, np.radians(52.5)
sAz = 5 * SEG


def sigma_d(dd):
    return 0.003 + 2e-6 * dd


def radiacion(dd, az):
    return np.array([E0 + dd * np.sin(az), N0 + dd * np.cos(az)])


def jac_rad(dd, az):
    return np.array([[np.sin(az), dd * np.cos(az)], [np.cos(az), -dd * np.sin(az)]])


def propagar(dd, az, sd, sa):
    J = jac_rad(dd, az)
    S = J @ np.diag([sd**2, sa**2]) @ J.T
    lam, V = np.linalg.eigh(S)
    return J, S, lam, V


sd = sigma_d(dA_)
J, S, lam, V = propagar(dA_, AzA, sd, sAz)
Pt = radiacion(dA_, AzA)
print(f"sigma_Az = 5″ = {sAz:.6e} rad; sigma_d = {sd * 1000:.1f} mm; d sigma_Az = {dA_ * sAz * 1000:.2f} mm")
print(f"punto radiado: E = {Pt[0]:.3f}, N = {Pt[1]:.3f}")
print("J =\n", J)
print("Sigma_EN (mm²) =\n", (S * 1e6).round(3))
print(f"autovalores (mm²) = {(lam * 1e6).round(3)}, semiejes (mm) = {(np.sqrt(lam) * 1000).round(2)}")
for i in range(2):
    vv = V[:, i]
    az = np.degrees(np.arctan2(vv[0], vv[1])) % 180
    print(f"   autovector {i}: {vv.round(4)}  acimut del eje = {az:.2f}° (o +180°)")
print(f"sigma_E = {np.sqrt(S[0, 0]) * 1000:.2f} mm, sigma_N = {np.sqrt(S[1, 1]) * 1000:.2f} mm, "
      f"correlación = {S[0, 1] / np.sqrt(S[0, 0] * S[1, 1]):.4f}")
rng = np.random.default_rng(2026)
n = 10_000
dd = dA_ + sd * rng.standard_normal(n)
aa = AzA + sAz * rng.standard_normal(n)
pts = radiacion(dd, aa).T
Semp = np.cov(pts.T)
rel = np.linalg.norm(Semp - S) / np.linalg.norm(S)
lam_e = np.linalg.eigvalsh(Semp)
print("Sigma empírica (mm²) =\n", (Semp * 1e6).round(3))
print(f"diferencia relativa (Frobenius) = {rel:.4f} = {100 * rel:.2f} %")
print(f"semiejes empíricos (mm) = {(np.sqrt(lam_e) * 1000).round(2)}")
print(f"media de los puntos - punto exacto (mm) = {((pts.mean(axis=0) - Pt) * 1000).round(3)}")
# misma simulación, ¿cuánto del error es por linealizar? (sin ruido de muestreo: F exacta vs lineal)
m2 = np.einsum("ij,jk,ik->i", pts - Pt, np.linalg.inv(S), pts - Pt)
print(f"fracción dentro de la elipse de 1 desvío = {np.mean(m2 <= 1):.4f}; "
      f"dentro de la del 95 % (k² = 5,991) = {np.mean(m2 <= 5.991):.4f}")
lin_pts = Pt + (J @ np.vstack([dd - dA_, aa - AzA])).T
print(f"máx |F exacta - lineal| sobre la muestra = {np.abs(pts - lin_pts).max() * 1e6:.4f} µm")
print("tabla d, sigma_d, d sigma_Az (mm), cociente")
for D in (500.0, 1000.0, 1500.0, 2000.0):
    print(f"   d = {D:.0f}: sigma_d = {sigma_d(D) * 1000:.1f}, d sigma_Az = {D * sAz * 1000:.1f}, "
          f"cociente = {D * sAz / sigma_d(D):.2f}")
dcruce = 0.003 / (sAz - 2e-6)
print(f"cruce d sigma_Az = sigma_d en d = {dcruce:.1f} m")

# ---------------------------------------------------------------- X1
titulo("X1")
F1 = lambda x, y: np.array([x**2 - y, x * y])
JF1 = np.array([[4.0, -1.0], [1.0, 2.0]])
v1 = np.array([0.1, -0.1])
print("F(2,1) =", F1(2, 1), " lineal =", F1(2, 1) + JF1 @ v1, " exacto =", F1(2.1, 0.9),
      " det J =", np.linalg.det(JF1))

# ---------------------------------------------------------------- X2
titulo("X2")
r2, t2 = 2.0, np.radians(30)
x2, y2 = P(r2, t2)
fila = np.array([y2, x2])
print("(x,y) =", (x2, y2), " fila dh =", fila, " dh J =", fila @ JP(r2, t2),
      " directo: (r sin2t, r² cos2t) =", (r2 * np.sin(2 * t2), r2**2 * np.cos(2 * t2)))

# ---------------------------------------------------------------- X3
titulo("X3")
H3 = np.array([[-2.0, 1.0], [1.0, -4.0]])
lam3, V3 = np.linalg.eigh(H3)
print("H =", H3.tolist(), " autovalores", lam3, " -3±√2 =", -3 - np.sqrt(2), -3 + np.sqrt(2),
      " det =", np.linalg.det(H3), "\n autovectores\n", V3)
h3 = lambda x, y: 100 - x**2 + x * y - 2 * y**2
print(" h(0,0) =", h3(0, 0), " h(1,1) =", h3(1, 1), " (1/2)vHv =", 0.5 * np.array([1, 1]) @ H3 @ np.array([1, 1]))

# ---------------------------------------------------------------- X4
titulo("X4")
hist_x4 = newton(np.array([0.0, 0.0]), np.array([50.0, 0.0]), 30.0, 40.0, (20.0, 20.0), n=4)

# ---------------------------------------------------------------- X5
titulo("X5")
d5, az5, sa5 = 800.0, np.radians(300.0), 10 * SEG
J5, S5, lam5, V5 = propagar(d5, az5, sigma_d(d5), sa5)
print(f"sigma_d = {sigma_d(d5) * 1000:.1f} mm, d sigma_Az = {d5 * sa5 * 1000:.2f} mm")
print("J =\n", J5, "\nSigma (mm²) =\n", (S5 * 1e6).round(3))
print("semiejes (mm) =", (np.sqrt(lam5) * 1000).round(2))
for i in range(2):
    print("  eje", i, V5[:, i].round(4), f"acimut {np.degrees(np.arctan2(V5[0, i], V5[1, i])) % 180:.2f}°")

# ================================================================ figuras
# 1) polar
fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.2))
a0 = ax[0]
for rr in np.arange(1.0, 3.01, 0.25):
    a0.plot([rr, rr], [0, 90], color=GRIS, lw=0.6)
for tt in np.arange(0, 91, 10):
    a0.plot([1, 3], [tt, tt], color=GRIS, lw=0.6)
a0.add_patch(Polygon([[r0, 30], [r0 + dr * 4, 30], [r0 + dr * 4, 30 + np.degrees(dt * 4)], [r0, 30 + np.degrees(dt * 4)]],
                     closed=True, fc=TEAL, alpha=0.35, ec=TEAL, lw=1.5))
a0.plot(r0, 30, "o", color="k")
a0.set_xlabel("r"); a0.set_ylabel("θ (grados)")
a0.set_title("plano (r, θ): rectángulo 4dr × 4dθ")
a1 = ax[1]
for rr in np.arange(1.0, 3.01, 0.25):
    tt = np.radians(np.linspace(0, 90, 100))
    a1.plot(rr * np.cos(tt), rr * np.sin(tt), color=GRIS, lw=0.6)
for tt in np.radians(np.arange(0, 91, 10)):
    a1.plot([np.cos(tt), 3 * np.cos(tt)], [np.sin(tt), 3 * np.sin(tt)], color=GRIS, lw=0.6)
DR, DT = 4 * dr, 4 * dt
ss = np.linspace(0, 1, 40)
borde = np.vstack([P(r0 + DR * s, t0) for s in ss] + [P(r0 + DR, t0 + DT * s) for s in ss]
                  + [P(r0 + DR * (1 - s), t0 + DT) for s in ss] + [P(r0, t0 + DT * (1 - s)) for s in ss])
a1.add_patch(Polygon(borde, closed=True, fc=TEAL, alpha=0.35, ec=TEAL, lw=1.5, label="imagen exacta"))
p0 = P(r0, t0)
para = np.array([p0, p0 + J1 @ [DR, 0], p0 + J1 @ [DR, DT], p0 + J1 @ [0, DT]])
a1.add_patch(Polygon(para, closed=True, fill=False, ec=RUST, lw=1.6, ls="--", label="J·(dr, dθ): paralelogramo tangente"))
a1.annotate("", p0 + J1 @ [DR, 0], p0, arrowprops=dict(arrowstyle="->", color=RUST, lw=1.4))
a1.annotate("", p0 + J1 @ [0, DT], p0, arrowprops=dict(arrowstyle="->", color=RUST, lw=1.4))
a1.plot(*p0, "o", color="k")
a1.set_aspect("equal"); a1.set_xlim(0, 3.1); a1.set_ylim(0, 3.1)
a1.set_title("plano (x, y): imagen por P"); a1.legend(loc="upper right", fontsize=8)
fig.tight_layout(); fig.savefig(SALIDA / "der_polar.png", dpi=150); plt.close(fig)

# 2) hessiana
fig, ax = plt.subplots(1, 2, figsize=(9.6, 4.4))
for a, pc, tit in ((ax[0], (1.0, 1.0), "cuenca en (1, 1): autovalores 3 y 9"),
                   (ax[1], (0.0, 0.0), "silla en (0, 0): autovalores −3 y 3")):
    xs = np.linspace(pc[0] - 0.6, pc[0] + 0.6, 200)
    ys = np.linspace(pc[1] - 0.6, pc[1] + 0.6, 200)
    X, Y = np.meshgrid(xs, ys)
    Z = hfun(X, Y) - hfun(*pc)
    H = Hh(*pc)
    Q = 0.5 * (H[0, 0] * (X - pc[0]) ** 2 + 2 * H[0, 1] * (X - pc[0]) * (Y - pc[1]) + H[1, 1] * (Y - pc[1]) ** 2)
    niveles = [-0.4, -0.2, -0.1, -0.03, 0.03, 0.1, 0.2, 0.4] if pc == (0.0, 0.0) else [0.03, 0.1, 0.2, 0.4, 0.7]
    cs = a.contour(X, Y, Z, levels=niveles, colors=TEAL, linewidths=1.2, linestyles="solid")
    a.clabel(cs, fontsize=7, fmt="%.2f")
    a.contour(X, Y, Q, levels=niveles, colors=RUST, linewidths=1.0, linestyles="--")
    lamh, Vv = np.linalg.eigh(H)
    for i in range(2):
        a.annotate("", np.array(pc) + 0.45 * Vv[:, i], pc, arrowprops=dict(arrowstyle="->", color=GOLD, lw=1.6))
        a.text(*(np.array(pc) + 0.5 * Vv[:, i]), f"λ = {lamh[i]:.0f}".replace("-", "−"), color="k", fontsize=8)
    a.plot(*pc, "o", color="k")
    a.set_aspect("equal"); a.set_title(tit, fontsize=10)
ax[0].plot([], [], color=TEAL, label="h − h(p)"); ax[0].plot([], [], color=RUST, ls="--", label="½ vᵀHv")
ax[0].legend(loc="lower left", fontsize=8)
fig.tight_layout(); fig.savefig(SALIDA / "der_hessiana.png", dpi=150); plt.close(fig)

# 3) newton
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.4), gridspec_kw=dict(width_ratios=[1.45, 1]))
tt = np.linspace(0, np.pi, 600)
x0n = hist4[0]
for ax, lims in ((axs[0], (-5, 110, -3, 70)), (axs[1], (57, 67, 38.5, 51))):
    ax.plot(80 * np.cos(tt), 80 * np.sin(tt), color=TEAL, lw=1.3, label="d(A) = 80")
    ax.plot(100 + 60 * np.cos(tt), 60 * np.sin(tt), color=RUST, lw=1.3, label="d(B) = 60")
    for C, dC, col in ((A, 80.0, TEAL), (B, 60.0, RUST)):
        u = (x0n - C) / np.linalg.norm(x0n - C)
        foot = C + dC * u
        tdir = np.array([-u[1], u[0]])
        seg = np.array([foot - 25 * tdir, foot + 25 * tdir])
        ax.plot(*seg.T, color=col, lw=1.0, ls=":")
    ax.plot(*hist4[:4].T, "-o", color=GOLD, ms=5, lw=1.2, label="iteraciones de Newton")
    ax.set_aspect("equal"); ax.set_xlim(*lims[:2]); ax.set_ylim(*lims[2:])
    ax.set_xlabel("x (m)")
axs[0].plot(*A, "ks"); axs[0].text(A[0] + 2, A[1] + 2, "A"); axs[0].plot(*B, "ks"); axs[0].text(B[0] - 7, B[1] + 2, "B")
axs[0].set_ylabel("y (m)"); axs[0].legend(loc="upper left", fontsize=8)
axs[0].plot([57, 67, 67, 57, 57], [38.5, 38.5, 51, 51, 38.5], color=GRIS, lw=0.8)
for k, xk in enumerate(hist4[:3]):
    dx, dy = {0: (0.25, -0.6), 1: (-0.75, 0.15), 2: (0.25, -0.55)}[k]
    axs[1].text(xk[0] + dx, xk[1] + dy, f"x{k}", fontsize=9)
axs[1].set_title("ampliación: punteadas = rectas de la linealización en x0", fontsize=9)
fig.tight_layout(); fig.savefig(SALIDA / "der_newton.png", dpi=150); plt.close(fig)

# 4) radiación
fig, ax = plt.subplots(figsize=(6.0, 5.0))
rel_pts = (pts - Pt) * 1000
ax.plot(rel_pts[:, 0], rel_pts[:, 1], ".", ms=1.0, color=TEAL, alpha=0.18, label="10 000 puntos simulados", zorder=1)
ang = np.degrees(np.arctan2(V[1, 1], V[0, 1]))
for k, ls in ((1, "-"), (2.448, "--")):
    ax.add_patch(Ellipse((0, 0), 2 * k * np.sqrt(lam[1]) * 1000, 2 * k * np.sqrt(lam[0]) * 1000, angle=ang,
                         fill=False, ec=RUST, lw=1.8, ls=ls, zorder=3))
ax.plot([], [], color=RUST, label="elipse de 1 desvío (J Σ Jᵀ)")
ax.plot([], [], color=RUST, ls="--", label="elipse del 95 %")
u = np.array([np.sin(AzA), np.cos(AzA)])
base = np.array([-55.0, -65.0])
ax.annotate("", base - 30 * u, base, arrowprops=dict(arrowstyle="->", color="k", lw=1.2))
ax.text(-50, -62, "hacia la estación", fontsize=8)
ax.set_aspect("equal"); ax.set_xlim(-110, 110); ax.set_ylim(-110, 110)
ax.set_xlabel("ΔE (mm)"); ax.set_ylabel("ΔN (mm)"); ax.legend(loc="upper left", fontsize=8)
ax.set_title("radiación d = 1500 m, Az = 52°30′, σ_d = 6 mm, σ_Az = 5″", fontsize=9)
fig.tight_layout(); fig.savefig(SALIDA / "der_radiacion.png", dpi=150); plt.close(fig)
print("\nfiguras en", SALIDA)
