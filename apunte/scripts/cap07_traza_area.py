"""Números y figura de la subsección «La traza como derivada del determinante» (capítulo 7).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  P   Proposición det(I + εE) = 1 + ε tr E + O(ε²): en 2x2 la igualdad exacta
      det(I + εE) = 1 + ε tr E + ε² det E para las tres matrices de la figura; en 3x3, el
      cociente (det(I + εE) - 1 - ε tr E)/ε² se estabiliza al achicar ε.
  L   Otras lecturas de la traza: tr R = 1 + 2 cos θ (3D), 2 cos θ (2D); traza de los
      proyectores del capítulo 11 (= rango); tr(AᵀA) = Σ‖A e_i‖² = Σσ_i² para la matriz del
      ejemplo de SVD a mano del capítulo 8.
  D   Aplicación «red deformada entre dos épocas»: con la F exacta de los tres puntos,
      det F - 1 frente a tr(F - I) = tr E = e1 + e2.
  F   Figura: el cuadrado unidad bajo I + εE (ε = 0,1) para tres matrices E (traza positiva,
      traza cero con cizalla, traza negativa); área medida con la fórmula de Gauss frente a
      1 + ε tr E.
  X   Ejercicio: red de cuatro puntos en dos épocas; F - I por mínimos cuadrados con
      coordenadas reducidas al baricentro; tr E; cambio relativo de área del cuadrilátero por
      la fórmula de Gauss.

Figura (PDF, determinista, legible en gris) en apunte/figuras/autovectores/:
  cap07_traza_area.pdf

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap07_traza_area.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "autovectores"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "svg.hashsalt": "cap07", "pdf.fonttype": 42})
META = {"CreationDate": None, "Producer": None, "Creator": None}


def coma(x, nd=4):
    return f"{x:.{nd}f}".replace(".", ",").replace("-", "−")


def area_gauss(P):
    """Área con signo de un polígono por la fórmula de Gauss (suma de cuñas, cap. 6)."""
    x, y = P[:, 0], P[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


I2 = np.eye(2)

# ---------------------------------------------------------------- P
print("== P  det(I + eps E) = 1 + eps tr E + eps^2 det E (2x2, exacto)")
EPS = 0.1
CASOS = [
    ("traza positiva", np.array([[1.0, 0.5], [0.3, 2.0]])),
    ("traza cero, con cizalla", np.array([[1.0, 2.0], [0.0, -1.0]])),
    ("traza negativa", np.array([[-2.0, 0.5], [-0.5, -1.0]])),
]
CUAD = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
RES = []
for nombre, E in CASOS:
    A = I2 + EPS * E
    S = area_gauss(CUAD @ A.T)
    lin = 1 + EPS * np.trace(E)
    print(f"  E = {E.tolist()}  ({nombre})")
    print(f"    tr E = {np.trace(E):g}, det E = {np.linalg.det(E):.4f}")
    print(f"    área medida (Gauss) = {S:.4f}, det(I+eps E) = {np.linalg.det(A):.4f}, "
          f"1 + eps tr E = {lin:.4f}, diferencia = {S - lin:+.4f} = eps^2 det E = {EPS**2 * np.linalg.det(E):+.4f}")
    RES.append((nombre, E, A, S, lin))

print("== P  3x3: (det(I + eps E) - 1 - eps tr E)/eps^2 al achicar eps")
E3 = np.array([[2.0, 1.0, -1.0], [0.5, -1.0, 3.0], [1.0, 2.0, 0.5]])
print(f"  E = {E3.tolist()}, tr E = {np.trace(E3):g}")
for e in (1e-1, 1e-2, 1e-3):
    q = (np.linalg.det(np.eye(3) + e * E3) - 1 - e * np.trace(E3)) / e**2
    print(f"    eps = {e:g}: cociente = {q:.4f}")
# el límite es la suma de los menores principales 2x2 (coeficiente c2)
c2 = sum(np.linalg.det(E3[np.ix_([i, j], [i, j])]) for i, j in ((0, 1), (0, 2), (1, 2)))
print(f"    suma de menores principales 2x2 = {c2:.4f}")

# ---------------------------------------------------------------- L
print("== L  otras lecturas de la traza")
th = np.deg2rad(120)
Rz = np.array([[np.cos(th), -np.sin(th), 0], [np.sin(th), np.cos(th), 0], [0, 0, 1]])
print(f"  tr Rz(120°) = {np.trace(Rz):.4f} = 1 + 2 cos 120° = {1 + 2 * np.cos(th):.4f}")
print(f"  tr R(120°) 2x2 = {np.trace(Rz[:2, :2]):.4f} = 2 cos 120°")
A11 = np.array([[0, 1], [1, 1], [2, 1], [3, 1]], dtype=float)
P11 = A11 @ np.linalg.pinv(A11)
print(f"  proyector de la recta por cuatro puntos (cap. 11): tr P = {np.trace(P11):.4f}, rango = {np.linalg.matrix_rank(A11)}")
A8 = np.array([[3.0, 0.0], [4.0, 5.0]])
s = np.linalg.svd(A8, compute_uv=False)
print(f"  A = {A8.tolist()} (cap. 8): tr(A^T A) = {np.trace(A8.T @ A8):g}, "
      f"sum ||A e_i||^2 = {sum(np.linalg.norm(A8[:, i])**2 for i in range(2)):g}, "
      f"sigma^2 = {np.round(s**2, 6).tolist()}, suma = {np.sum(s**2):g}")

# ---------------------------------------------------------------- D
print("== D  red de tres puntos del capítulo: det F - 1 frente a tr E")
X1 = np.array([[5432118.437, 6151874.215], [5434602.881, 6152593.062], [5433041.590, 6154210.774]])
X2 = np.array([[5432118.405, 6151874.170], [5434602.924, 6152593.100], [5433041.615, 6154210.757]])
R1, R2 = X1 - X1.mean(0), X2 - X2.mean(0)
F = R2[:2].T @ np.linalg.inv(R1[:2].T)
G = F - I2
Es = 0.5 * (G + G.T)
ev = np.linalg.eigvalsh(Es)
print(f"  tr(F - I) = {np.trace(G) * 1e6:.3f} µε, tr E = {np.trace(Es) * 1e6:.3f} µε, e1 + e2 = {ev.sum() * 1e6:.3f} µε")
print(f"  det F - 1 = {(np.linalg.det(F) - 1) * 1e6:.3f} µε; det(F - I) = {np.linalg.det(G) * 1e12:.1f} µε² (término de segundo orden)")

# ---------------------------------------------------------------- F
fig, axs = plt.subplots(1, 3, figsize=(10.2, 3.9))
for ax, (nombre, E, A, S, lin) in zip(axs, RES):
    img = CUAD @ A.T
    ax.add_patch(Polygon(CUAD, closed=True, fill=False, ec="black", ls="--", lw=1.1))
    ax.add_patch(Polygon(img, closed=True, fc=TEAL, alpha=.18, ec="none"))
    ax.add_patch(Polygon(img, closed=True, fill=False, ec=TEAL, lw=1.8, hatch="///"))
    ax.set_xlim(-.35, 1.55); ax.set_ylim(-.62, 1.42); ax.set_aspect("equal")
    ax.set_xticks([0, 1]); ax.set_yticks([0, 1])
    f = [f"{v:g}".replace(".", ",").replace("-", "−") for v in E.ravel()]
    ax.set_title(f"{nombre}\nE = [ {f[0]}   {f[1]} ;  {f[2]}   {f[3]} ]", fontsize=9.5)
    texto = (f"tr E = {coma(np.trace(E), 0)}\n"
             f"área medida = {coma(S)}\n"
             f"1 + ε tr E = {coma(lin)}\n"
             f"diferencia = ε² det E = {coma(S - lin)}")
    ax.text(-.3, -.58, texto, fontsize=8, va="bottom",
            bbox=dict(fc="white", ec=GRIS, lw=.6))
fig.suptitle("Cuadrado unidad (a trazos) y su imagen por I + εE (rayada), ε = 0,1", fontsize=10.5)
fig.tight_layout()
fig.savefig(SALIDA / "cap07_traza_area.pdf", metadata=META)
plt.close(fig)
print("  figura:", SALIDA / "cap07_traza_area.pdf")

# ---------------------------------------------------------------- X
print("== X  red de cuatro puntos, F por mínimos cuadrados")
XA = np.array([[1000.0, 1000.0], [3400.0, 1200.0], [3000.0, 3300.0], [1200.0, 2900.0]])  # época 1, m
D = np.array([[39.0, -4.0], [84.0, -11.0], [95.0, 3.0], [60.0, 8.0]])  # desplazamientos, mm
XB = XA + D / 1000
c = XA.mean(0); dbar = D.mean(0)
Xr = XA - c; Dr = D - dbar
print(f"  baricentro época 1 = {c}, desplazamiento medio = {dbar} mm")
print(f"  coordenadas reducidas (m):\n{Xr}")
print(f"  desplazamientos reducidos (mm):\n{Dr}")
N = Xr.T @ Xr
print(f"  X^T X = {N.tolist()}, det = {np.linalg.det(N):.6g}")
b = Xr.T @ (Dr / 1000)
print(f"  X^T d_E = {(Xr.T @ Dr[:, 0]).tolist()} m·mm, X^T d_N = {(Xr.T @ Dr[:, 1]).tolist()} m·mm")
Gx = np.linalg.solve(N, b).T  # filas: (g11 g12), (g21 g22)
print(f"  F - I = {np.round(Gx * 1e6, 3).tolist()} ·1e-6")
Ex = 0.5 * (Gx + Gx.T)
print(f"  E = {np.round(Ex * 1e6, 3).tolist()} µε, tr E = {np.trace(Ex) * 1e6:.3f} µε, "
      f"omega = {0.5 * (Gx[1, 0] - Gx[0, 1]) * 1e6:.3f} µrad")
res = Dr - Xr @ Gx.T * 1000
print(f"  residuos (mm):\n{np.round(res, 2)}")
S1, S2 = area_gauss(XA), area_gauss(XB)
print(f"  S1 = {S1:.4f} m², S2 = {S2:.4f} m², ΔS = {S2 - S1:.4f} m², ΔS/S1 = {(S2 - S1) / S1 * 1e6:.3f} µε")
print(f"  det F - 1 = {(np.linalg.det(I2 + Gx) - 1) * 1e6:.3f} µε; diferencia tr E - ΔS/S = "
      f"{(np.trace(Ex) - (S2 - S1) / S1) * 1e6:.3f} µε")
print(f"  brecha (tr E - ΔS/S)·S1 = {(np.trace(Ex) - (S2 - S1) / S1) * S1:.4f} m²; "
      f"residuo máximo = {np.abs(res).max():.2f} mm; ΔS previsto por tr E = {np.trace(Ex) * S1:.4f} m²")
per = np.sum(np.linalg.norm(np.roll(XA, -1, 0) - XA, axis=1))
print(f"  perímetro = {per:.2f} m; corrimiento medio hacia afuera ΔS/perímetro = {(S2 - S1) / per * 1000:.1f} mm")
