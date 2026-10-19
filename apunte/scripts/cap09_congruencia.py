"""Conjugación y congruencia (capítulo «Cambio de base: las coordenadas son etiquetas»).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  K1  Conjugación activa: rotación de 45° alrededor del centro c = (3, 1) como T_c R T_c^{-1}
      en coordenadas homogéneas; parte de traslación (I - R) c; el centro queda fijo.
  K2  Reflexión en la recta y = x/2 como R_a S R_a^{-1}, con S = diag(1, -1) y
      a = arctan(1/2): coincide con (1/5) [[3, 4], [4, -3]] del ejemplo de la reflexión.
  T   La tabla «Cada objeto cambia con su regla», verificada fila por fila con un ejemplo
      numérico aleatorio (semilla fija 9): vector C^{-1} v (módulo conservado sólo si C es
      ortogonal), forma lineal w C (valor w(v) conservado), transformación C^{-1} A C (det,
      traza, autovalores), forma cuadrática C^T Q C (signatura y valor x^T Q x). Se comprueba
      además que las cuatro reglas están escritas en el .tex entre los marcadores
      «% tabla-regla:inicio» y «% tabla-regla:fin».
  P   Proposición: con C ortogonal, C^{-1} A C = C^T A C.
  X   Contraejemplo: la elipse de tolerancia Q de la aplicación de obra (acimut 127°30',
      semiejes 20 y 5 mm) en la base oblicua b1 = (3, 1), b2 = (1, 2): C'^T Q C' frente a
      C'^{-1} Q C' (traza, autovalores, determinante, signatura) y q del punto P2, d = (7, 2) mm,
      con cada regla.
  E   Ejercicio: Q = [[2, 1], [1, 2]], base b1 = (1, 0), b2 = (1, 1); congruencia frente a
      semejanza, punto x = (2, 1).
Sale con código 1 si alguna verificación falla.

Figura (PDF determinista, sin fecha ni productor, legible en escala de grises) en
apunte/figuras/cambio-de-base/:
  cap09_conjugacion.pdf  tres paneles: llevar el centro c al origen (T_c^{-1}), rotar 45°
                         alrededor del origen (R), volver (T_c); la figura original en
                         punteado gris y la imagen de cada etapa en trazo continuo.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap09_congruencia.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "apunte" / "figuras" / "cambio-de-base"
SALIDA.mkdir(parents=True, exist_ok=True)
TEX = RAIZ / "apunte" / "contenido" / "09-cambio-de-base.tex"
# Paleta del proyecto (tools/animaciones/_comun.py, PALETA): teal, gris, tinta.
TEAL, GRIS, TINTA = "#01696F", "#9AA0A6", "#2b2b2b"
plt.rcParams.update({"font.size": 9, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "pdf.compression": 9, "axes.formatter.use_locale": False})
deg = np.pi / 180
FALLAS = []


def chequear(cond, texto):
    print(("  [ok]    " if cond else "  [FALLA] ") + texto)
    if not cond:
        FALLAS.append(texto)


def rot(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def homog(M=None, v=(0.0, 0.0)):
    H = np.eye(3)
    if M is not None:
        H[:2, :2] = M
    H[:2, 2] = v
    return H


def signatura(S):
    ev = np.linalg.eigvalsh((S + S.T) / 2)
    return int((ev > 1e-12).sum()), int((ev < -1e-12).sum())


# ---------------------------------------------------------------- K1
print("K1  Rotación de 45° alrededor de c = (3, 1): T_c R T_c^{-1}")
c = np.array([3.0, 1.0])
R45 = rot(45 * deg)
Tc, Tci, Rh = homog(v=c), homog(v=-c), homog(R45)
H1 = Tc @ Rh @ Tci
print("    T_c R T_c^{-1} =\n", H1)
print("    (I - R) c =", (np.eye(2) - R45) @ c)
chequear(np.allclose(H1[:2, 2], (np.eye(2) - R45) @ c), "parte de traslación = (I - R) c")
chequear(np.allclose(H1 @ np.r_[c, 1], np.r_[c, 1]), "el centro c queda fijo")
chequear(np.allclose(H1[:2, 2], [1.58578644, -1.82842712]), "(I - R) c ≈ (1,5858; -1,8284)")

# ---------------------------------------------------------------- K2
print("K2  Reflexión en y = x/2 como R_a S R_a^{-1}")
a = np.arctan(0.5)
S = np.diag([1.0, -1.0])
Ma = rot(a) @ S @ rot(a).T
print("    alfa =", a / deg, "°;  R_a S R_a^{-1} =\n", Ma)
chequear(np.allclose(Ma, np.array([[3, 4], [4, -3]]) / 5), "R_a S R_a^{-1} = (1/5)[[3,4],[4,-3]]")
chequear(np.allclose(rot(a), np.array([[2, -1], [1, 2]]) / np.sqrt(5)), "R_a = C/sqrt5 del ejemplo")

# ---------------------------------------------------------------- T
print("T   Tabla «Cada objeto cambia con su regla» (semilla 9)")
rng = np.random.default_rng(9)
C = rng.normal(size=(2, 2)) + 2 * np.eye(2)          # base oblicua cualquiera
U, _ = np.linalg.qr(rng.normal(size=(2, 2)))         # base ortonormal
Ci = np.linalg.inv(C)
v = rng.normal(size=2)
w = rng.normal(size=2)                               # fila
A = rng.normal(size=(2, 2))
Qi = np.array([[1.0, 2.0], [2.0, -1.0]])             # simétrica indefinida, signatura (1, 1)
print("    C =\n", C, "\n    det C =", np.linalg.det(C))
# vector
vb = Ci @ v
print("    vector: |v|_e =", np.linalg.norm(v), " |C^{-1}v| =", np.linalg.norm(vb),
      " |U^T v| =", np.linalg.norm(U.T @ v))
chequear(np.allclose(C @ vb, v), "vector: C [v]_b = [v]_e")
chequear(np.isclose(np.linalg.norm(U.T @ v), np.linalg.norm(v)), "vector: módulo igual con U ortogonal")
chequear(not np.isclose(np.linalg.norm(vb), np.linalg.norm(v)), "vector: módulo distinto con C oblicua")
# forma lineal
wb = w @ C
print("    forma: w(v) =", w @ v, " [w]_b [v]_b =", wb @ vb)
chequear(np.isclose(w @ v, wb @ vb), "forma lineal: w C · C^{-1} v = w · v")
# transformación
Ab = Ci @ A @ C
print("    transf.: det", np.linalg.det(A), np.linalg.det(Ab), " traza", np.trace(A), np.trace(Ab))
chequear(np.allclose(C @ (Ab @ vb), A @ v), "transformación: C^{-1}AC lleva [v]_b a [Av]_b")
chequear(np.isclose(np.linalg.det(A), np.linalg.det(Ab)) and np.isclose(np.trace(A), np.trace(Ab)),
         "transformación: det y traza iguales")
chequear(np.allclose(np.sort_complex(np.linalg.eigvals(A)), np.sort_complex(np.linalg.eigvals(Ab))),
         "transformación: autovalores iguales")
# forma cuadrática
Qb = C.T @ Qi @ C
print("    forma cuadr.: x^TQx =", v @ Qi @ v, " [x]_b^T Q_b [x]_b =", vb @ Qb @ vb,
      " signaturas", signatura(Qi), signatura(Qb), " trazas", np.trace(Qi), np.trace(Qb))
chequear(np.isclose(v @ Qi @ v, vb @ Qb @ vb), "forma cuadrática: valor x^T Q x igual")
chequear(signatura(Qi) == signatura(Qb) == (1, 1), "forma cuadrática: signatura (1,1) igual")
chequear(not np.isclose(np.trace(Qi), np.trace(Qb)), "forma cuadrática: la traza cambia")
# las reglas, escritas en el .tex
tex = TEX.read_text(encoding="utf-8")
m = re.search(r"% tabla-regla:inicio(.*?)% tabla-regla:fin", tex, re.S)
chequear(m is not None, "marcadores de la tabla en el .tex")
if m:
    filas = [f for f in m.group(1).split(r"\\") if "&" in f]
    esperado = [("Vector", r"C^{-1}[v]_e"), ("Forma lineal", r"[\omega]_e\,C"),
                ("Transformación lineal", r"C^{-1}A_e\,C"), ("Forma bilineal o cuadrática", r"C^TQ_e\,C")]
    chequear(len(filas) == 4, "la tabla tiene cuatro filas")
    for (obj, regla), fila in zip(esperado, filas):
        chequear(obj in fila and regla in fila, f"fila «{obj}» con la regla {regla}")

# ---------------------------------------------------------------- P
print("P   C ortogonal: C^{-1} A C = C^T A C")
chequear(np.allclose(np.linalg.inv(U) @ A @ U, U.T @ A @ U), "con U ortogonal las dos reglas coinciden")
chequear(not np.allclose(Ci @ A @ C, C.T @ A @ C), "con C oblicua no coinciden")

# ---------------------------------------------------------------- X
print("X   Contraejemplo: elipse de tolerancia de la obra en una base oblicua")
az = (127 + 30 / 60) * deg
uL = np.array([np.sin(az), np.cos(az)])
uT = np.array([np.sin(az + 90 * deg), np.cos(az + 90 * deg)])
Cobra = np.column_stack([uL, uT])
D = np.diag([1 / 400, 1 / 25])
Q = Cobra @ D @ Cobra.T
print("    Q (10^-3 mm^-2) =\n", Q * 1e3)
print("    traza Q =", np.trace(Q), " autovalores", np.linalg.eigvalsh(Q), " det", np.linalg.det(Q))
Cp = np.array([[3.0, 1.0], [1.0, 2.0]])
Qc = Cp.T @ Q @ Cp
Qs = np.linalg.inv(Cp) @ Q @ Cp
evc = np.linalg.eigvalsh(Qc)
evs = np.sort(np.linalg.eigvals(Qs).real)
print("    congruencia C'^T Q C' =\n", Qc)
print("      traza", np.trace(Qc), " autovalores", evc, " det", np.linalg.det(Qc), " signatura", signatura(Qc))
print("    semejanza  C'^{-1} Q C' =\n", Qs)
print("      traza", np.trace(Qs), " autovalores", evs, " det", np.linalg.det(Qs))
d = np.array([7.0, 2.0])
db = np.linalg.solve(Cp, d)
qe, qc, qs = d @ Q @ d, db @ Qc @ db, db @ Qs @ db
print("    P2: d =", d, " [d]_b =", db, " q_EN =", qe, " q congruencia =", qc, " q semejanza =", qs)
chequear(np.allclose(Qc, [[0.2823, 0.2282], [0.2282, 0.1933]], atol=6e-5), "C'^T Q C' ≈ [[0,2823; 0,2282],[0,2282; 0,1933]]")
chequear(np.allclose(Qs, [[0.01083, 0.00698], [0.03480, 0.03167]], atol=6e-6), "C'^{-1} Q C' ≈ [[0,01083; 0,00698],[0,03480; 0,03167]]")
chequear(np.isclose(np.trace(Qc), 0.4756, atol=5e-5), "traza congruencia ≈ 0,4756")
chequear(np.allclose(evc, [0.00532, 0.4703], atol=5e-5), "autovalores congruencia ≈ 0,00532 y 0,4703")
chequear(np.isclose(np.linalg.det(Qc), 0.0025), "det congruencia = 0,0025 = 5^2 · 10^-4")
chequear(np.isclose(np.trace(Qs), 0.0425) and np.allclose(evs, [0.0025, 0.04]), "semejanza: traza 0,0425, autovalores 0,0025 y 0,04")
chequear(signatura(Qc) == signatura(Q) == (2, 0), "signatura (2,0) en las dos bases")
chequear(not np.allclose(Qs, Qs.T), "C'^{-1} Q C' no es simétrica")
chequear(np.allclose(db, [2.4, -0.2]), "[d]_b = (2,4; -0,2)")
chequear(np.isclose(qe, qc) and abs(qc - 1.4150) < 5e-5, "q congruencia = q en E,N = 1,4150")
chequear(abs(qs - 0.0436) < 5e-5, "q con semejanza ≈ 0,0436 (falso)")

# ---------------------------------------------------------------- E
print("E   Ejercicio: Q = [[2,1],[1,2]], b1 = (1,0), b2 = (1,1)")
Qe = np.array([[2.0, 1.0], [1.0, 2.0]])
Ce = np.array([[1.0, 1.0], [0.0, 1.0]])
Qec = Ce.T @ Qe @ Ce
Qes = np.linalg.inv(Ce) @ Qe @ Ce
x = np.array([2.0, 1.0])
xb = np.linalg.solve(Ce, x)
print("    C^T Q C =\n", Qec, "\n    C^{-1} Q C =\n", Qes)
print("    autovalores Q", np.linalg.eigvalsh(Qe), " congr.", np.linalg.eigvalsh(Qec), " sem.",
      np.sort(np.linalg.eigvals(Qes).real), " 4±sqrt13 =", 4 - np.sqrt(13), 4 + np.sqrt(13))
print("    x_b =", xb, " q =", x @ Qe @ x, xb @ Qec @ xb, xb @ Qes @ xb, " Qx =", Qe @ x,
      " [Qx]_b =", np.linalg.solve(Ce, Qe @ x), " (C^{-1}QC) x_b =", Qes @ xb)
chequear(np.allclose(Qec, [[2, 3], [3, 6]]) and np.allclose(Qes, [[1, 0], [1, 3]]), "matrices del ejercicio")
chequear(np.allclose(xb, [1, 1]) and np.isclose(x @ Qe @ x, 14) and np.isclose(xb @ Qec @ xb, 14)
         and np.isclose(xb @ Qes @ xb, 5), "q = 14 (congruencia) y 5 (semejanza)")
chequear(np.allclose(Qes @ xb, np.linalg.solve(Ce, Qe @ x)) and np.allclose(Qes @ xb, [1, 4]),
         "como transformación: (C^{-1}QC)(1,1) = (1,4) = [Qx]_b")
chequear(np.allclose(np.linalg.eigvalsh(Qec), [4 - np.sqrt(13), 4 + np.sqrt(13)]), "autovalores 4 ± sqrt13")

# ---------------------------------------------------------------- figura
print("Figura cap09_conjugacion.pdf")
casa = np.array([[4.0, 1.5], [5.6, 1.5], [5.6, 2.5], [4.8, 3.2], [4.0, 2.5], [4.0, 1.5]])


def aplicar(H, P):
    return (H @ np.c_[P, np.ones(len(P))].T).T[:, :2]


etapas = [("1. llevar $c$ al origen: $T_c^{-1}$", casa, aplicar(Tci, casa)),
          ("2. rotar $45^\\circ$ en el origen: $R$", aplicar(Tci, casa), aplicar(Rh @ Tci, casa)),
          ("3. volver: $T_c$", aplicar(Rh @ Tci, casa), aplicar(H1, casa))]
fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.5))
for ax, (tit, P0, P1) in zip(axs, etapas):
    ax.axhline(0, color=GRIS, lw=0.6); ax.axvline(0, color=GRIS, lw=0.6)
    ax.plot(*casa.T, color=GRIS, lw=1.0, ls=(0, (1, 2)))
    ax.plot(*P0.T, color=TINTA, lw=1.0, ls="--")
    ax.fill(*P1.T, color=TEAL, alpha=0.18, lw=0)
    ax.plot(*P1.T, color=TEAL, lw=1.8)
    ax.plot(*P1[0], "o", color=TEAL, ms=4)
    ax.plot(*P0[0], "o", mfc="white", mec=TINTA, ms=4)
    ax.annotate("", xy=P1[3], xytext=P0[3],
                arrowprops=dict(arrowstyle="->", color=TINTA, lw=0.8))
    ax.plot(*c, "x", color=TINTA, ms=7, mew=1.6)
    ax.annotate("$c$", c, xytext=(4, -11), textcoords="offset points", color=TINTA)
    ax.plot(0, 0, "+", color=TINTA, ms=8, mew=1.2)
    ax.set_title(tit, fontsize=9, color=TINTA)
    ax.set_xlim(-3.5, 6.5); ax.set_ylim(-1.5, 5.5); ax.set_aspect("equal")
    ax.set_xticks(range(-3, 7)); ax.set_yticks(range(-1, 6)); ax.tick_params(labelsize=7, colors=TINTA)
    ax.grid(True, color=GRIS, lw=0.3, alpha=0.5)
fig.tight_layout()
destino = SALIDA / "cap09_conjugacion.pdf"
fig.savefig(destino, metadata={"CreationDate": None, "ModDate": None, "Producer": None, "Creator": None})
plt.close(fig)
print("    ->", destino.relative_to(RAIZ))
chequear(np.allclose(aplicar(H1, casa), aplicar(homog(R45, (np.eye(2) - R45) @ c), casa)),
         "figura: las tres etapas componen la rotación alrededor de c")

if FALLAS:
    print(f"{len(FALLAS)} verificación(es) fallaron")
    sys.exit(1)
print("Todas las verificaciones pasaron.")
