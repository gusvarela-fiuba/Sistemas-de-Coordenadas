"""Números y figura de la aplicación topográfica del capítulo «Afinidades y coordenadas homogéneas».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  D   Datos: ortofoto de dron sin georreferenciar (4000 x 3000 px, GSD ~ 3 cm/px); cuatro
      puntos de apoyo P1..P4 con coordenadas de imagen (columna c, fila f; f crece hacia
      abajo) y de terreno (E, N) Gauss-Krüger faja 5, y un quinto punto de control P5 que no
      entra en el ajuste. Los datos se generan con una afinidad «verdadera» (giro, escalas
      algo distintas en c y f, cizalla mínima) más errores fijos de unos centímetros.
  A   Ajuste afín de 6 parámetros E = a0 + a1 c + a2 f, N = b0 + b1 c + b2 f por mínimos
      cuadrados con los 4 puntos (8 ecuaciones, 6 incógnitas): bloque U = [1 c f],
      ecuaciones normales U^T U x = U^T E' y U^T U y = U^T N' (E' = E - 5 432 000,
      N' = N - 6 154 000), parámetros, matriz homogénea 3x3, residuos por punto en cm, RMS;
      vector w del núcleo de U^T (los residuos de E y de N son múltiplos de w).
  A2  Interpretación de la parte lineal: escalas de columna y fila (normas de las columnas),
      ángulos de las columnas, cizalla (apartamiento de 90°), det; descomposición
      A = R(theta) S diag(1, -1) con S simétrica definida positiva (polar, vía SVD).
  S   Similaridad de 4 parámetros (capítulo 3) ajustada a los mismos 4 puntos; como la fila
      crece hacia abajo, es inversa: E = t_E + a c + b f, N = t_N + b c - a f. Escala,
      giro, residuos en cm y RMS.
  V   Verificación con P5: predicción afín y por similaridad, diferencia con lo medido en cm.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/afines/:
  afinidad_ortofoto.png  izquierda, la imagen en píxeles (fila hacia abajo) con los puntos;
                         derecha, el terreno (E, N reducidas) con los residuos de la afinidad
                         y de la similaridad amplificados.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap04_afinidad_ortofoto.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "afines"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, TINTA = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#3d3a35"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
deg = np.pi / 180
E_RED, N_RED = 5_432_000.0, 6_154_000.0


def R(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


# ---------------------------------------------------------------- D
print("=== D  datos ===")
theta_v, sc_v, sf_v, cz_v = 3.5 * deg, 0.03000, 0.03009, 0.08 * deg
A_v = R(theta_v) @ np.array([[1, np.tan(cz_v)], [0, 1]]) @ np.diag([sc_v, -sf_v])
t_v = np.array([5_432_180.000, 6_154_760.000])
img = np.array([[412, 287], [3611, 352], [3548, 2716], [377, 2659], [1980, 2905]], float)
ruido = np.array([[0.012, -0.008], [-0.009, 0.014], [0.006, -0.011], [-0.010, 0.007],
                  [0.008, 0.010]])
ter = np.round(img @ A_v.T + t_v + ruido, 3)
for i, (p, q) in enumerate(zip(img, ter), 1):
    print(f"P{i}: c = {p[0]:.0f}, f = {p[1]:.0f}   E = {q[0]:.3f}, N = {q[1]:.3f}")
print("A verdadera =\n", A_v)

ci, ti = img[:4], ter[:4]
U = np.column_stack([np.ones(4), ci])           # columnas 1, c, f
Er, Nr = ti[:, 0] - E_RED, ti[:, 1] - N_RED

# ---------------------------------------------------------------- A
print("\n=== A  ajuste afín (6 parámetros) ===")
UtU = U.T @ U
print("U^T U =\n", UtU)
print("U^T E' =", np.round(U.T @ Er, 3), "  U^T N' =", np.round(U.T @ Nr, 3))
xa = np.linalg.solve(UtU, U.T @ Er)
xb = np.linalg.solve(UtU, U.T @ Nr)
a0, a1, a2 = xa[0] + E_RED, xa[1], xa[2]
b0, b1, b2 = xb[0] + N_RED, xb[1], xb[2]
print(f"reducidos: a0' = {xa[0]:.3f}, b0' = {xb[0]:.3f}")
print(f"a0 = {a0:.3f}  a1 = {a1:.7f}  a2 = {a2:.7f}")
print(f"b0 = {b0:.3f}  b1 = {b1:.7f}  b2 = {b2:.7f}")
M = np.array([[a1, a2, a0], [b1, b2, b0], [0, 0, 1]])
print("M homogénea =\n", M)
A = M[:2, :2]
pred = (M @ np.column_stack([ci, np.ones(4)]).T).T[:, :2]
res_a = ti - pred
for i, r in enumerate(res_a, 1):
    print(f"P{i}: residuo (dato - predicho) = ({100*r[0]:+.1f}, {100*r[1]:+.1f}) cm, "
          f"módulo {100*np.hypot(*r):.1f} cm")
rms_a = np.sqrt(np.sum(res_a**2) / 4)
print(f"RMS afín (por punto) = {100*rms_a:.1f} cm;  suma residuos E, N =", res_a.sum(0))
print(f"sigma0 = sqrt(sum r^2 / (8-6)) = {100*np.sqrt(np.sum(res_a**2)/2):.1f} cm")
w = np.linalg.svd(U.T)[2][-1]
w = w / np.abs(w).max()
print("núcleo de U^T (residuos E y N son múltiplos de w): w =", w)

# ---------------------------------------------------------------- A2
print("\n=== A2  interpretación ===")
sc, sf = np.linalg.norm(A[:, 0]), np.linalg.norm(A[:, 1])
ang_c = np.arctan2(A[1, 0], A[0, 0]) / deg          # columna c respecto del eje E
ang_mf = np.arctan2(A[0, 1], -A[1, 1]) / deg        # -columna f (fila hacia arriba) respecto de N, antihorario
ang_entre = np.arccos(A[:, 0] @ A[:, 1] / (sc * sf)) / deg
print(f"escala columnas sc = {100*sc:.4f} cm/px, escala filas sf = {100*sf:.4f} cm/px, "
      f"cociente sf/sc = {sf/sc:.5f}  ({(sf/sc-1)*100:.2f} %)")
print(f"ángulo de la columna c respecto de E (antihorario) = {ang_c:.3f}°")
print(f"ángulo de -columna f (fila hacia arriba) respecto de N (antihorario) = {ang_mf:.3f}°;  "
      f"diferencia = {ang_c-ang_mf:.3f}°")
print(f"ángulo entre columnas = {ang_entre:.3f}°  -> cizalla = {ang_entre-90:.3f}°")
print(f"det A = {np.linalg.det(A):.8f}  (sc*sf = {sc*sf:.8f}), área de 1 px = {abs(np.linalg.det(A))*1e4:.4f} cm²")
F = np.diag([1.0, -1.0])
Ap = A @ F                                           # parte con det > 0
Uu, s, Vt = np.linalg.svd(Ap)
Rp = Uu @ Vt
S = Vt.T @ np.diag(s) @ Vt
th = np.arctan2(Rp[1, 0], Rp[0, 0]) / deg
print("A diag(1,-1) =\n", Ap)
print(f"polar: R(theta) con theta = {th:.3f}°;  S =\n", S)
print("S en cm/px =\n", 100 * S)
ev, evec = np.linalg.eigh(S)
print("autovalores de S (cm/px) =", 100 * ev, " autovectores (columnas) =\n", evec)
print(f"dirección del autovalor mayor respecto del eje c = {np.arctan2(evec[1, 1], evec[0, 1]) / deg:.1f}°;"
      f" cociente de autovalores = {ev[1]/ev[0]:.5f}")
print("verificación R S diag(1,-1) - A =", np.abs(Rp @ S @ F - A).max())

# ---------------------------------------------------------------- S
print("\n=== S  similaridad (4 parámetros, inversa) ===")
Bs = np.zeros((8, 4))
Bs[0::2] = np.column_stack([ci[:, 0], ci[:, 1], np.ones(4), np.zeros(4)])    # E = a c + b f + tE
Bs[1::2] = np.column_stack([-ci[:, 1], ci[:, 0], np.zeros(4), np.ones(4)])   # N = b c - a f + tN
ls = np.empty(8); ls[0::2] = Er; ls[1::2] = Nr
xs = np.linalg.solve(Bs.T @ Bs, Bs.T @ ls)
a, b, tE, tN = xs
print(f"a = {a:.7f}  b = {b:.7f}  tE = {tE+E_RED:.3f}  tN = {tN+N_RED:.3f}")
lam, ths = np.hypot(a, b), np.arctan2(b, a) / deg
print(f"escala lambda = {100*lam:.4f} cm/px,  giro = {ths:.3f}°")
pred_s = (Bs @ xs).reshape(4, 2) + np.array([E_RED, N_RED])
res_s = ti - pred_s
for i, r in enumerate(res_s, 1):
    print(f"P{i}: residuo similaridad = ({100*r[0]:+.1f}, {100*r[1]:+.1f}) cm, módulo {100*np.hypot(*r):.1f} cm")
rms_s = np.sqrt(np.sum(res_s**2) / 4)
print(f"RMS similaridad = {100*rms_s:.1f} cm;  cociente RMS sim/afín = {rms_s/rms_a:.1f}")
df = ci[2:, 1].mean() - ci[:2, 1].mean()
print(f"separación en f entre los apoyos de arriba y de abajo = {df:.1f} px = {df*sf:.1f} m; "
      f"efecto de la diferencia de escala sobre ella = {100*df*(sf-sc):.1f} cm")

# ---------------------------------------------------------------- V
print("\n=== V  verificación con P5 ===")
p5, q5 = img[4], ter[4]
pa = A @ p5 + np.array([a0, b0])
ps = np.array([a * p5[0] + b * p5[1] + tE + E_RED, b * p5[0] - a * p5[1] + tN + N_RED])
print("M (c5, f5, 1) =", M @ np.array([*p5, 1.0]))
for nom, pp in (("afín", pa), ("similaridad", ps)):
    d = q5 - pp
    print(f"{nom}: predicho E = {pp[0]:.3f}, N = {pp[1]:.3f}; medido - predicho = "
          f"({100*d[0]:+.1f}, {100*d[1]:+.1f}) cm, módulo {100*np.hypot(*d):.1f} cm")

# ---------------------------------------------------------------- figura
AMP = 300
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.6))
ax1.add_patch(plt.Rectangle((0, 0), 4000, 3000, fill=False, ec=GRIS, lw=1))
ax1.scatter(ci[:, 0], ci[:, 1], marker="^", s=60, c=TEAL, zorder=3, label="puntos de apoyo")
ax1.scatter(*p5, marker="s", s=45, c=TINTA, zorder=3, label="control P5")
for i, p in enumerate(img, 1):
    ax1.annotate(f"P{i}", p, xytext=(6, 6), textcoords="offset points")
ax1.set_xlim(-250, 4250); ax1.set_ylim(3250, -250)      # fila hacia abajo
ax1.set_aspect("equal"); ax1.set_xlabel("columna c (px)"); ax1.set_ylabel("fila f (px)")
ax1.set_title("imagen (sin georreferenciar)"); ax1.legend(loc="center", fontsize=8)
ax1.xaxis.set_label_position("top"); ax1.xaxis.tick_top()

esq = np.array([[0, 0], [4000, 0], [4000, 3000], [0, 3000], [0, 0]], float)
borde = esq @ A.T + np.array([a0, b0]) - np.array([E_RED, N_RED])
ax2.plot(borde[:, 0], borde[:, 1], color=GRIS, lw=1)
tr = ti - np.array([E_RED, N_RED])
ax2.scatter(tr[:, 0], tr[:, 1], marker="^", s=30, c=TEAL, zorder=3)
q5r = q5 - np.array([E_RED, N_RED])
ax2.scatter(*q5r, marker="s", s=25, c=TINTA, zorder=3)
for i, p in enumerate(np.vstack([tr, q5r]), 1):
    ax2.annotate(f"P{i}", p, xytext=(-16, 6), textcoords="offset points")
d5a, d5s = q5 - pa, q5 - ps
puntos = np.vstack([tr, q5r])
for res, col, nom in ((np.vstack([res_a, d5a]), RUST, "afinidad"),
                      (np.vstack([res_s, d5s]), GOLD, "similaridad")):
    ax2.quiver(puntos[:, 0], puntos[:, 1], AMP * res[:, 0], AMP * res[:, 1], angles="xy",
               scale_units="xy", scale=1, color=col, width=0.005, zorder=4,
               label=f"residuo {nom} (×{AMP})")
ax2.set_aspect("equal"); ax2.set_xlabel(f"E − {E_RED:,.0f} (m)".replace(",", " "))
ax2.set_ylabel(f"N − {N_RED:,.0f} (m)".replace(",", " "))
ax2.set_xlim(150, 335); ax2.set_ylim(640, 795)
ax2.set_title("terreno (Gauss-Krüger faja 5)")
ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.13), ncol=2, fontsize=8, frameon=False)
ax2.grid(color="#e4e2dc", lw=.6)
fig.tight_layout(); fig.savefig(SALIDA / "afinidad_ortofoto.png", dpi=150, bbox_inches="tight", pad_inches=0.1); plt.close(fig)
print("\nfigura:", SALIDA / "afinidad_ortofoto.png")
