"""Números y figura de la aplicación «Acimut y estación total» del capítulo «Rotaciones».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  D   Datos: estación A y referencia B en coordenadas Gauss-Krüger (faja 5, metros);
      ángulos horizontales beta_P, beta_Q (horarios, desde la visual a B) en grados,
      minutos y segundos, con su conversión a grados decimales y a radianes;
      distancias horizontales d_P, d_Q.
  R   Acimut de referencia Az_AB desde coordenadas con atan2(dE, dN), llevado a [0, 360);
      distancia AB; acimut inverso Az_BA = Az_AB + 180 (mod 360).
  O   Orientación: Az_P = Az_AB + beta_P y Az_Q = Az_AB + beta_Q (mod 360), en decimal y
      en grados-minutos-segundos.
  M   Matriz R(-Az) = [[cos Az, sin Az], [-sin Az, cos Az]] para P y Q, y radiado
      (dE, dN) = R(-Az) (0, d); coordenadas finales E, N de P y Q.
  C   Comprobación de la factorización R(-Az) = R(-beta) R(-Az_AB) (diferencia máxima).
  V   Verificación: distancia PQ desde coordenadas, desde el sistema del instrumento
      (eje y' hacia B) y por la ley del coseno con d_P, d_Q y gamma = beta_Q - beta_P.
  I   Acimut P->Q con atan2 (cuadrante correcto) versus el arctan(dE/dN) ingenuo;
      acimut inverso Q->P.

Figura (PNG, fondo blanco, dpi 150) en apunte/figuras/rotaciones/:
  acimut_radiado.png  croquis en coordenadas relativas a la estación: norte, visual a B
                      con Az_AB, ángulos beta y radiados a P y Q, segmento PQ.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap01_acimut_estacion_total.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Arc

SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "rotaciones"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, INK = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#2b2b2b"


def gms_a_dec(g, m, s):
    return g + m / 60 + s / 3600


def dec_a_gms(x):
    x = x % 360
    g = int(x)
    resto = (x - g) * 60
    m = int(resto)
    s = (resto - m) * 60
    if round(s, 1) >= 60:
        s -= 60
        m += 1
    if m >= 60:
        m -= 60
        g += 1
    return f"{g}° {m:02d}' {s:04.1f}\""


def acimut(de, dn):
    return np.degrees(np.arctan2(de, dn)) % 360


def R(theta_deg):
    t = np.radians(theta_deg)
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


# ---------------------------------------------------------------- D: datos
A = np.array([5_412_837.425, 6_171_254.318])   # estación
B = np.array([5_413_096.512, 6_171_618.903])   # referencia
beta_gms = {"P": (47, 23, 15), "Q": (128, 41, 38)}
d = {"P": 86.452, "Q": 143.217}

print("== D: datos ==")
print(f"A (estación)   E = {A[0]:.3f}  N = {A[1]:.3f}")
print(f"B (referencia) E = {B[0]:.3f}  N = {B[1]:.3f}")
beta = {}
for k, (g, m, s) in beta_gms.items():
    beta[k] = gms_a_dec(g, m, s)
    print(f"beta_{k} = {g}° {m:02d}' {s:02d}\" = {g} + {m}/60 + {s}/3600 = {beta[k]:.6f}° "
          f"= {np.radians(beta[k]):.6f} rad ; d_{k} = {d[k]:.3f} m")

# ---------------------------------------------------------------- R: referencia
dAB = B - A
Az_AB = acimut(*dAB)
dist_AB = np.hypot(*dAB)
Az_BA = (Az_AB + 180) % 360
print("\n== R: acimut de referencia ==")
print(f"dE_AB = {dAB[0]:.3f} m  dN_AB = {dAB[1]:.3f} m  (ambos > 0: primer cuadrante)")
print(f"Az_AB = atan2(dE, dN) = {Az_AB:.6f}° = {dec_a_gms(Az_AB)}")
print(f"dist_AB = {dist_AB:.3f} m")
print(f"Az_BA = Az_AB + 180 = {Az_BA:.6f}° = {dec_a_gms(Az_BA)}")
print(f"comprobación atan2(-dE, -dN) = {acimut(*(-dAB)):.6f}°")

# ---------------------------------------------------------------- O, M: orientación y radiado
print("\n== O, M: orientación y radiado ==")
Az, pts, inc = {}, {}, {}
for k in ("P", "Q"):
    Az[k] = (Az_AB + beta[k]) % 360
    M = R(-Az[k])
    inc[k] = M @ np.array([0.0, d[k]])
    pts[k] = A + inc[k]
    print(f"Az_{k} = Az_AB + beta_{k} = {Az_AB:.6f} + {beta[k]:.6f} = {Az[k]:.6f}° = {dec_a_gms(Az[k])}")
    print(f"  R(-Az_{k}) = [[{M[0,0]:.6f}, {M[0,1]:.6f}], [{M[1,0]:.6f}, {M[1,1]:.6f}]]")
    print(f"  (dE, dN) = R(-Az_{k}) (0, {d[k]:.3f}) = ({inc[k][0]:.3f}, {inc[k][1]:.3f}) m")
    print(f"  {k}: E = {pts[k][0]:.3f}  N = {pts[k][1]:.3f}")

# ---------------------------------------------------------------- C: factorización
print("\n== C: R(-Az) = R(-beta) R(-Az_AB) ==")
for k in ("P", "Q"):
    dif = np.abs(R(-Az[k]) - R(-beta[k]) @ R(-Az_AB)).max()
    print(f"{k}: max |R(-Az) - R(-beta)R(-Az_AB)| = {dif:.1e}")

# ---------------------------------------------------------------- V: verificación de distancias
print("\n== V: distancia PQ por tres caminos ==")
dPQ_coord = np.linalg.norm(pts["Q"] - pts["P"])
loc = {k: R(-beta[k]) @ np.array([0.0, d[k]]) for k in ("P", "Q")}   # sistema del instrumento
dPQ_loc = np.linalg.norm(loc["Q"] - loc["P"])
gamma = beta["Q"] - beta["P"]
dPQ_cos = np.sqrt(d["P"] ** 2 + d["Q"] ** 2 - 2 * d["P"] * d["Q"] * np.cos(np.radians(gamma)))
for k in ("P", "Q"):
    print(f"{k} en el sistema del instrumento (x', y' hacia B): ({loc[k][0]:.3f}, {loc[k][1]:.3f})")
print(f"gamma = beta_Q - beta_P = {gamma:.6f}° = {dec_a_gms(gamma)}")
print(f"PQ desde coordenadas E,N      = {dPQ_coord:.3f} m")
print(f"PQ en el sistema del instrumento = {dPQ_loc:.3f} m")
print(f"PQ por ley del coseno         = {dPQ_cos:.3f} m")
print(f"diferencia máxima = {max(abs(dPQ_coord-dPQ_loc), abs(dPQ_coord-dPQ_cos)):.1e} m")
for k in ("P", "Q"):
    print(f"|A{k}| desde coordenadas = {np.linalg.norm(pts[k]-A):.3f} m (d_{k} = {d[k]:.3f})")

# ---------------------------------------------------------------- I: acimut P->Q
print("\n== I: acimut P->Q y cuadrantes ==")
dPQ = pts["Q"] - pts["P"]
Az_PQ = acimut(*dPQ)
ingenuo = np.degrees(np.arctan(dPQ[0] / dPQ[1]))
print(f"dE_PQ = {dPQ[0]:.3f} m  dN_PQ = {dPQ[1]:.3f} m")
print(f"arctan(dE/dN) ingenuo = {ingenuo:.6f}°")
print(f"Az_PQ = atan2(dE, dN) = {Az_PQ:.6f}° = {dec_a_gms(Az_PQ)}")
print(f"Az_QP = Az_PQ + 180 (mod 360) = {(Az_PQ + 180) % 360:.6f}° = {dec_a_gms(Az_PQ + 180)}")

# ---------------------------------------------------------------- figura
fig, ax = plt.subplots(figsize=(6.4, 6.4), facecolor="white")
ax.set_facecolor("white")
rel = {k: pts[k] - A for k in ("P", "Q")}
uB = dAB / dist_AB * 150
ax.annotate("", xy=(0, 165), xytext=(0, 0),
            arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.2))
ax.text(4, 160, "N", color=GRIS, fontsize=12)
ax.annotate("", xy=(165, 0), xytext=(-40, 0),
            arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.0))
ax.text(160, 5, "E", color=GRIS, fontsize=12)
ax.plot([0, uB[0]], [0, uB[1]], color=INK, lw=1.2, ls="--")
ax.text(uB[0] + 3, uB[1] + 2, "hacia B\n(referencia)", color=INK, fontsize=9)
for k, col in (("P", TEAL), ("Q", RUST)):
    ax.plot([0, rel[k][0]], [0, rel[k][1]], color=col, lw=1.8)
    ax.plot(*rel[k], "o", color=col, ms=7)
    ax.text(rel[k][0] + 4, rel[k][1] + 4, f"{k}", color=col, fontsize=12, weight="bold")
ax.plot([rel["P"][0], rel["Q"][0]], [rel["P"][1], rel["Q"][1]], color=GOLD, lw=1.2, ls=":")
# arcos (matplotlib mide ángulos antihorarios desde el este: theta = 90 - Az)
ax.add_patch(Arc((0, 0), 70, 70, theta1=90 - Az_AB, theta2=90, color=INK, lw=1.2))
ax.text(8, 40, r"Az$_{AB}$", color=INK, fontsize=10)
ax.add_patch(Arc((0, 0), 110, 110, theta1=90 - Az["P"], theta2=90 - Az_AB, color=TEAL, lw=1.2))
ax.text(50, 30, r"$\beta_P$", color=TEAL, fontsize=12)
ax.add_patch(Arc((0, 0), 150, 150, theta1=90 - Az["Q"], theta2=90 - Az_AB, color=RUST, lw=1.2))
ax.text(80, -42, r"$\beta_Q$", color=RUST, fontsize=12)
ax.plot(0, 0, "^", color=INK, ms=9)
ax.text(-50, -16, "A (estación)", color=INK, fontsize=10)
ax.set_aspect("equal")
ax.set_xlim(-50, 185)
ax.set_ylim(-160, 180)
ax.set_xlabel("ΔE desde A [m]")
ax.set_ylabel("ΔN desde A [m]")
ax.grid(True, color="#e6e4df", lw=0.6)
for s in ("top", "right"):
    ax.spines[s].set_visible(False)
fig.tight_layout()
fig.savefig(SALIDA / "acimut_radiado.png", dpi=150, facecolor="white")
print(f"\nFigura: {SALIDA / 'acimut_radiado.png'}")
