"""Números y figuras del capítulo «La SVD: leer la forma de las curvas de nivel».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  N   Nube sintética de N = 200 posiciones GNSS de un mismo punto (desvíos este/norte en
      metros, dispersión anisótropa, semilla fija): SVD de la matriz centrada, semiejes
      sigma_i / sqrt(N-1) = sqrt(lambda_i), orientación (acimut), elipse del 95 % con el
      factor sqrt(chi2_2(0,95)) = sqrt(-2 ln 0,05) = 2,448 y conteo de posiciones dentro.
      Se usa en la pregunta de campo (figura svd_nube.png) y en la aplicación topográfica.
  E1  Ejemplo «SVD a mano de A = [[3,0],[4,5]]»: A^T A, autovalores, sigma, v_i, u_i
      (signos de numpy), semiejes de ||Ax|| = 1, imagen del círculo, sigma1*sigma2 = |det A|,
      reconstrucción U Sigma V^T, autovectores de A para la comparación.
  E2  Ejemplo «Plano ajustado a 8 puntos» (semilla fija): centroide, sigma, normal v3,
      distancias y RMS.
  R   Rotación de 90°: valores singulares.
  X1  Ejercicio 1: SVD de [[1,2],[0,1]] y semiejes de ||Ax|| = 1.
  X2  Ejercicio 2: [[1,2],[2,4]] (sigma2 = 0): bandas y segmento.
  X3  Ejercicio 3: covarianza [[13.6, 4.8],[4.8, 6.4]] mm^2: semiejes y orientación.
  X4  Ejercicio 4: desdeformar la elipse de A = [[3,0],[4,5]]: Sigma^-1 U^T y V Sigma^-1 U^T.

Figuras (PNG, fondo blanco) en apunte/figuras/svd/:
  svd_nube.png    nube de lecturas con sus elipses de error de 1 y 2 desvíos.
  svd_grilla.png  grilla deformada por A en la base canónica y en la base de los v_i (dos paneles).
(Las figuras de curvas de nivel y del círculo a la elipse están en TikZ, con los números de E1.)

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap07_svd.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "svd"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})

rng = np.random.default_rng(2026)

# ---------------------------------------------------------------- N: nube de la estación total
print("=== N  nube sintética de posiciones GNSS (m) ===")
n = 200
ang = np.deg2rad(30.0)                     # dirección del eje mayor "verdadero", desde el este
R = np.array([[np.cos(ang), -np.sin(ang)], [np.sin(ang), np.cos(ang)]])
nube = (rng.standard_normal((n, 2)) * [1.5, 0.6]) @ R.T   # columnas: este, norte (m)
media = nube.mean(axis=0)
X = nube - media                            # matriz centrada N x 2
C = X.T @ X / (n - 1)
lam, W = np.linalg.eigh(C)
lam, W = lam[::-1], W[:, ::-1]
Un, sn, Vtn = np.linalg.svd(X, full_matrices=False)
print("N =", n, " media =", media)
print("sigma de X =", sn, " sqrt(N-1) =", np.sqrt(n - 1), " sigma/sqrt(N-1) =", sn / np.sqrt(n - 1))
print("v1 (SVD de X) =", Vtn[0], " v2 =", Vtn[1])
print("covarianza C =\n", C, "\nautovalores de C =", lam, " sqrt =", np.sqrt(lam), " autovector mayor =", W[:, 0])
thN = np.degrees(np.arctan2(Vtn[0, 1], Vtn[0, 0])) % 180
print("ángulo eje mayor desde el este (°) =", thN, " respecto del norte (acimut, °) =", (90 - thN) % 180)
k95 = np.sqrt(-2 * np.log(0.05))
print("k95 = sqrt(-2 ln 0.05) =", k95, " k95^2 =", k95 ** 2)
print("semiejes 95 % =", k95 * np.sqrt(lam))
m2 = np.sum((X @ Vtn.T) ** 2 / lam, axis=1)
print("posiciones dentro de 1 desvío =", np.sum(m2 <= 1), " dentro del 95 % =", np.sum(m2 <= k95 ** 2), "de", n)
fig, ax = plt.subplots(figsize=(6.4, 4.6))
ax.scatter(nube[:, 0], nube[:, 1], s=10, color=TEAL, alpha=.8, label="posiciones (sintéticas)", zorder=3)
for k, ls, lab in ((1.0, "-", "elipse de 1 desvío"), (k95, "--", "elipse del 95 %")):
    ax.add_patch(Ellipse(media, 2 * k * np.sqrt(lam[0]), 2 * k * np.sqrt(lam[1]), angle=thN,
                         fill=False, color=RUST, lw=1.6, ls=ls, label=lab))
for k, col in ((0, RUST), (1, GOLD)):
    d = Vtn[k] * np.sqrt(lam[k])
    ax.annotate("", media + d, media, arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8))
ax.text(*(media + Vtn[0] * np.sqrt(lam[0]) * 1.08), r"$\sqrt{\lambda_1}\,v_1$", color=RUST)
ax.text(*(media + Vtn[1] * np.sqrt(lam[1]) * 1.6), r"$\sqrt{\lambda_2}\,v_2$", color="#8a6d10")
ax.set_aspect("equal"); ax.grid(color="#e4e2dc", lw=.6)
ax.set_xlabel("desvío en el este (m)"); ax.set_ylabel("desvío en el norte (m)")
ax.legend(loc="lower right", fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(SALIDA / "svd_nube.png", dpi=200); plt.close(fig)

# ---------------------------------------------------------------- E1: A = [[3,0],[4,5]]
print("\n=== E1  SVD de A = [[3,0],[4,5]] ===")
A = np.array([[3.0, 0.0], [4.0, 5.0]])
AtA = A.T @ A
print("A^T A =\n", AtA)
print("autovalores de A^T A =", np.linalg.eigvalsh(AtA)[::-1])
U, s, Vt = np.linalg.svd(A)
print("sigma =", s, " (3*sqrt5 =", 3 * np.sqrt(5), ", sqrt5 =", np.sqrt(5), ")")
print("U =\n", U, "\nVt =\n", Vt)
print("v1 =", Vt[0], " v2 =", Vt[1])
print("u1 =", U[:, 0], " u2 =", U[:, 1], "  (1,3)/sqrt10 =", np.array([1, 3]) / np.sqrt(10))
print("A v1 / sigma1 =", A @ Vt[0] / s[0], " A v2 / sigma2 =", A @ Vt[1] / s[1])
print("semiejes de ||Ax|| = 1: 1/sigma =", 1 / s)
print("sigma1*sigma2 =", s.prod(), " det A =", np.linalg.det(A))
print("U Sigma V^T =\n", U @ np.diag(s) @ Vt, " allclose:", np.allclose(U @ np.diag(s) @ Vt, A))
print("det U =", np.linalg.det(U), " det V =", np.linalg.det(Vt.T))
print("sigma1 u1 =", s[0] * U[:, 0], " sigma2 u2 =", s[1] * U[:, 1])
print("ángulo de u1 (°) =", np.degrees(np.arctan2(U[1, 0], U[0, 0])))
lA, PA = np.linalg.eig(A)
print("autovalores de A =", lA, " autovectores (columnas) =\n", PA)
print("||A||_2 = sigma1 =", np.linalg.norm(A, 2))

# Figura: grilla deformada en dos bases
def grilla(ax, base, img, M, titulo, cols):
    t = np.linspace(-1, 1, 5)
    for c in t:
        for d0, d1 in ((base[:, 0], base[:, 1]), (base[:, 1], base[:, 0])):
            seg = np.array([c * d1 + a * d0 for a in (-1, 1)])
            if img:
                seg = seg @ M.T
            ax.plot(seg[:, 0], seg[:, 1], color=GRIS if not img else TEAL, lw=.8, alpha=.9)
    th = np.linspace(0, 2 * np.pi, 200)
    circ = np.c_[np.cos(th), np.sin(th)]
    ax.plot(*(circ @ M.T).T, color=RUST, lw=1.6)
    for k, col in enumerate(cols):
        vec = M @ base[:, k]
        ax.annotate("", vec, (0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8))
    ax.set_title(titulo, fontsize=9.5)
    ax.set_aspect("equal"); ax.set_xlim(-10, 10); ax.set_ylim(-10, 10)
    ax.axhline(0, color="#d8d6cf", lw=.6, zorder=0); ax.axvline(0, color="#d8d6cf", lw=.6, zorder=0)
    ax.set_xticks([-8, -4, 0, 4, 8]); ax.set_yticks([-8, -4, 0, 4, 8])

V = Vt.T
fig, axs = plt.subplots(1, 2, figsize=(8.4, 4.3))
grilla(axs[0], np.eye(2), True, A, "imagen de la grilla canónica:\nparalelogramos oblicuos", (GOLD, GOLD))
grilla(axs[1], V, True, A, "imagen de la grilla de los $v_i$:\nrectángulos sobre $u_1$, $u_2$", (RUST, GOLD))
axs[0].text(3.3, 4.6, r"$Ae_1$", color="#8a6d10"); axs[0].text(-1.9, 5.3, r"$Ae_2$", color="#8a6d10")
axs[1].text(-3.7, -5.6, r"$\sigma_1u_1$", color=RUST); axs[1].text(-2.6, 1.6, r"$\sigma_2u_2$", color="#8a6d10")
fig.tight_layout(); fig.savefig(SALIDA / "svd_grilla.png", dpi=200); plt.close(fig)

# ---------------------------------------------------------------- E2: plano por 8 puntos
print("\n=== E2  plano ajustado a 8 puntos (m) ===")
rng_plano = np.random.default_rng(8)        # generador propio: el plano no depende de la nube
xy = rng_plano.uniform(0, 20, (8, 2))
z = 100 + 0.05 * xy[:, 0] - 0.02 * xy[:, 1] + rng_plano.normal(0, 0.03, 8)
P = np.round(np.c_[xy, z], 3)
print("puntos (x, y, z) =\n", P)
cen = P.mean(axis=0)
Pc = P - cen
_, s3, Vt3 = np.linalg.svd(Pc)
nrm = Vt3[2]
d = Pc @ nrm
print("centroide =", cen)
print("sigma =", s3)
print("normal v3 =", nrm)
print("distancias con signo =", d)
print("RMS =", np.sqrt(np.mean(d ** 2)), " = sigma3/sqrt(8) =", s3[2] / np.sqrt(8))
print("pendiente: inclinación del plano (°) =", np.degrees(np.arccos(abs(nrm[2]))))

# ---------------------------------------------------------------- R: rotación de 90°
print("\n=== R  rotación de 90° ===")
R90 = np.array([[0.0, -1.0], [1.0, 0.0]])
print("autovalores =", np.linalg.eigvals(R90), " sigma =", np.linalg.svd(R90)[1])

# ---------------------------------------------------------------- Ejercicios
print("\n=== X1  A = [[1,2],[0,1]] ===")
B = np.array([[1.0, 2.0], [0.0, 1.0]])
Ub, sb, Vtb = np.linalg.svd(B)
print("B^T B =\n", B.T @ B, " autovalores =", np.linalg.eigvalsh(B.T @ B)[::-1])
print("sigma =", sb, " (1+sqrt2 =", 1 + np.sqrt(2), ", sqrt2-1 =", np.sqrt(2) - 1, ")")
print("v1 =", Vtb[0], " v2 =", Vtb[1], " u1 =", Ub[:, 0], " u2 =", Ub[:, 1])
print("ángulo de v1 (°) =", np.degrees(np.arctan2(Vtb[0, 1], Vtb[0, 0])))
print("semiejes ||Bx|| = 1:", 1 / sb, " producto sigma =", sb.prod())

print("\n=== X2  A = [[1,2],[2,4]] ===")
D = np.array([[1.0, 2.0], [2.0, 4.0]])
Ud, sd, Vtd = np.linalg.svd(D)
print("sigma =", sd, " v1 =", Vtd[0], " v2 =", Vtd[1], " u1 =", Ud[:, 0])
print("distancia de las rectas ||Ax|| = 1 al origen = 1/sigma1 =", 1 / sd[0])

print("\n=== X3  covarianza [[13.6,4.8],[4.8,6.4]] mm^2 ===")
C3 = np.array([[13.6, 4.8], [4.8, 6.4]])
l3, W3 = np.linalg.eigh(C3)
l3, W3 = l3[::-1], W3[:, ::-1]
print("autovalores =", l3, " semiejes =", np.sqrt(l3), " eje mayor =", W3[:, 0])
th3 = np.degrees(np.arctan2(W3[1, 0], W3[0, 0])) % 180
print("ángulo desde el este (°) =", th3, " azimut (°) =", (90 - th3) % 180)
print("correlación =", C3[0, 1] / np.sqrt(C3[0, 0] * C3[1, 1]))

print("\n=== X4  desdeformar la elipse de A = [[3,0],[4,5]] ===")
W1 = np.diag(1 / s) @ U.T
W2 = Vt.T @ np.diag(1 / s) @ U.T
print("Sigma^-1 U^T =\n", W1)
print("V Sigma^-1 U^T =\n", W2, "\nA^-1 =\n", np.linalg.inv(A), " (15 A^-1 =\n", 15 * np.linalg.inv(A), ")")
print("Sigma^-1 U^T (sigma1 u1) =", W1 @ (s[0] * U[:, 0]), "  V Sigma^-1 U^T (sigma1 u1) =", W2 @ (s[0] * U[:, 0]))
