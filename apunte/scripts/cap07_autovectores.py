"""Números y figuras del capítulo «Subespacios invariantes: autovalores y autovectores».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  I   La idea: A = [[4,1],[2,3]]; polinomio característico, autovalores 5 y 2, autovectores
      (1,1) y (1,-2); un vector de prueba (1,0) que sí gira (ángulo entre v y Av).
  E1  Ejemplo «Simétrica 2x2 y ejes principales»: S = [[5,2],[2,2]]; autovalores, autovectores
      ortogonales, traza y determinante, semiejes de la elipse x^T S x = 1.
  E2  Ejemplo «Cizalla: autovalor repetido con una sola dirección»: C = [[2,1],[0,2]] y,
      para comparar, 2I; rango de C - 2I.
  E3  Ejemplo «Tres direcciones en R^3»: M = [[2,1,0],[1,3,1],[0,1,2]]; polinomio
      característico, autovalores 1, 2, 4, autovectores por cuña de filas de M - λI,
      ortogonalidad, traza = suma, det = producto.
  K   Los cuatro casos 2x2 (figura): discriminante tr^2 - 4 det de A, 2I, C y la rotación con
      escala [[1,-1],[1,1]] = sqrt(2) R(45°), autovalores 1 ± i = sqrt(2) e^{±i 45°}.
  R   Rotación compuesta R = Rz(90°) Ry(90°): eje por cuña de filas de R - I, ángulo por la
      traza (1 + 2 cos θ), plano invariante -x + y + z = 0 y su imagen.
  A   Aplicación topográfica: red de tres puntos en Gauss-Krüger faja 5 medida en dos épocas;
      transformación afín exacta x2 = F x1 + t con coordenadas reducidas al baricentro;
      tensor de deformación E = (F + F^T)/2 - I, giro ω (parte antisimétrica); autovalores
      de E en microstrain (µε) y acimutes de las direcciones principales; dilatación (traza)
      y cizalla máxima (diferencia); control Δd/d ≈ u^T E u en los tres lados.
  X1  Ejercicio 1: A = [[1,2],[3,2]].
  X2  Ejercicio 2: clasificar [[3,-2],[1,1]], [[3,1],[0,3]], [[0,1],[1,0]].
  X3  Ejercicio 3: R = Rx(90°) Rz(90°): eje por cuña de filas y ángulo por la traza.
  X4  Ejercicio 4: elipse 3x^2 + 2xy + 3y^2 = 1: ejes, semiejes y área.
  X5  Ejercicio 5: tensor de deformación E = [[30,10],[10,-10]] µε: deformaciones y
      direcciones principales, alargamiento de una base de 1500 m en dirección Norte.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/autovectores/:
  autovec_grilla.png        grilla deformada por A = [[4,1],[2,3]] con sus dos direcciones
                            invariantes y un vector de prueba que gira.
  autovec_elipse.png        elipse x^T S x = 1, S = [[5,2],[2,2]], con sus ejes principales.
  autovec_cuatro_casos.png  los cuatro casos 2x2: círculo unidad, su imagen y las direcciones
                            invariantes (o ninguna).
  autovec_red.png           red de control de la aplicación: desplazamientos exagerados y
                            direcciones principales de deformación.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap07_autovectores.py
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
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})


def rot2(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def Rx(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def Rz(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def cuna_filas(B):
    """Autovector (núcleo de B, rango 2) como cuña de dos filas no paralelas."""
    for i, j in ((0, 1), (0, 2), (1, 2)):
        v = np.cross(B[i], B[j])
        if np.linalg.norm(v) > 1e-9:
            return (i + 1, j + 1), v
    return None, None


def angulo(u, v):
    return np.degrees(np.arctan2(u[0] * v[1] - u[1] * v[0], u @ v))


# ---------------------------------------------------------------- I
print("=== I  la idea: A = [[4,1],[2,3]] ===")
A = np.array([[4.0, 1], [2, 3]])
print("tr =", np.trace(A), " det =", round(np.linalg.det(A), 10), " poly =", np.poly(A), " raíces =", np.roots(np.poly(A)))
for lam, v in ((5, (1, 1)), (2, (1, -2))):
    v = np.array(v, float)
    print(f"  λ={lam}: A-λI =", (A - lam * np.eye(2)).tolist(), " A v =", A @ v)
v0 = np.array([1.0, 0])
print("vector de prueba (1,0): A v =", A @ v0, " ángulo girado =", round(angulo(v0, A @ v0), 2), "°")
print("ángulo entre (1,1) y (1,-2) =", round(np.degrees(np.arccos((1 - 2) / np.sqrt(2 * 5))), 2), "°")

# ---------------------------------------------------------------- E1
print("\n=== E1  simétrica S = [[5,2],[2,2]] ===")
S = np.array([[5.0, 2], [2, 2]])
w, V = np.linalg.eigh(S)
print("poly =", np.poly(S), " autovalores =", w)
print("S-6I =", (S - 6 * np.eye(2)).tolist(), " S-I =", (S - np.eye(2)).tolist())
print("S(2,1) =", S @ [2, 1], " S(1,-2) =", S @ [1, -2], " (2,1).(1,-2) =", np.dot([2, 1], [1, -2]))
print("tr =", np.trace(S), " det =", np.linalg.det(S))
print("semiejes 1/sqrt(λ):", 1 / np.sqrt(6), 1 / np.sqrt(1), " área elipse π/sqrt(det) =", np.pi / np.sqrt(6))
print("acimut del eje corto (2,1) respecto del eje x:", round(np.degrees(np.arctan2(1, 2)), 4), "°")

# ---------------------------------------------------------------- E2
print("\n=== E2  cizalla C = [[2,1],[0,2]] ===")
C = np.array([[2.0, 1], [0, 2]])
print("poly =", np.poly(C), " rango(C-2I) =", np.linalg.matrix_rank(C - 2 * np.eye(2)),
      " rango(2I-2I) =", np.linalg.matrix_rank(np.zeros((2, 2))))
print("C(0,1) =", C @ [0, 1], " C(1,0) =", C @ [1, 0], " C(1,1) =", C @ [1, 1])

# ---------------------------------------------------------------- E3
print("\n=== E3  M = [[2,1,0],[1,3,1],[0,1,2]] ===")
M = np.array([[2.0, 1, 0], [1, 3, 1], [0, 1, 2]])
print("poly =", np.round(np.poly(M), 10), " autovalores =", np.round(np.linalg.eigvalsh(M), 10))
vs = {}
for lam in (1, 2, 4):
    B = M - lam * np.eye(3)
    par, v = cuna_filas(B)
    vs[lam] = v
    print(f"  λ={lam}: M-λI = {B.tolist()}  filas {par}: cuña = {v}  M v = {M @ v}")
print("productos internos:", vs[1] @ vs[2], vs[1] @ vs[4], vs[2] @ vs[4])
print("tr =", np.trace(M), " suma =", 1 + 2 + 4, " det =", round(np.linalg.det(M), 10), " producto =", 1 * 2 * 4)

# ---------------------------------------------------------------- K
print("\n=== K  los cuatro casos ===")
casos = [
    ("dos reales distintos", A),
    ("repetido, todas las direcciones", 2 * np.eye(2)),
    ("repetido, una sola dirección", C),
    ("complejos: rotación con escala", np.array([[1.0, -1], [1, 1]])),
]
for nom, K in casos:
    tr, de = np.trace(K), np.linalg.det(K)
    print(f"  {nom}: tr={tr:g} det={de:g} disc={tr**2 - 4 * de:g} autovalores={np.linalg.eigvals(K)}")
Q = casos[3][1]
lq = np.linalg.eigvals(Q)
print("  |λ| =", abs(lq[0]), " arg =", np.degrees(np.angle(lq)), "°")

fig, axs = plt.subplots(1, 4, figsize=(13, 4.0))
tt = np.linspace(0, 2 * np.pi, 200)
circ = np.vstack([np.cos(tt), np.sin(tt)])
titulos = ["dos autovalores reales distintos\n$\\lambda=5,\\ 2$",
           "autovalor doble, dos direcciones\n$2I$: $\\lambda=2$, todo invariante",
           "autovalor doble, una dirección\ncizalla: $\\lambda=2$, sólo el eje $x$",
           "autovalores complejos\n$1\\pm i=\\sqrt{2}\\,e^{\\pm i45^\\circ}$: todo gira"]
for ax, (nom, K), tit in zip(axs, casos, titulos):
    img = K @ circ
    ax.plot(*circ, color=GRIS, lw=1)
    ax.plot(*img, color=TEAL, lw=1.6)
    for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        p = np.array([np.cos(a), np.sin(a)])
        ax.annotate("", K @ p, p, arrowprops=dict(arrowstyle="-|>", color=RUST, lw=.8, alpha=.8))
    if nom.startswith("dos"):
        for d in ((1, 1), (1, -2)):
            d = np.array(d) / np.linalg.norm(d)
            ax.plot([-6 * d[0], 6 * d[0]], [-6 * d[1], 6 * d[1]], "k--", lw=1)
    elif nom.startswith("repetido, todas"):
        for a in np.linspace(0, np.pi, 8, endpoint=False):
            ax.plot([-6 * np.cos(a), 6 * np.cos(a)], [-6 * np.sin(a), 6 * np.sin(a)], color=GOLD, lw=.8, ls="--")
    elif nom.startswith("repetido, una"):
        ax.plot([-6, 6], [0, 0], "k--", lw=1)
    ax.set_xlim(-5.2, 5.2); ax.set_ylim(-5.2, 5.2); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([]); ax.set_title(tit, fontsize=9.5)
fig.tight_layout(); fig.subplots_adjust(top=0.84); fig.savefig(SALIDA / "autovec_cuatro_casos.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- R
print("\n=== R  rotación Rz(90°) Ry(90°) ===")
R = np.round(Rz(np.pi / 2) @ Ry(np.pi / 2), 12)
print("R =", R.tolist())
par, eje = cuna_filas(R - np.eye(3))
print("filas", par, "de R-I: eje =", eje, " R eje =", R @ eje)
print("tr =", np.trace(R), " cos θ =", (np.trace(R) - 1) / 2, " θ =", np.degrees(np.arccos((np.trace(R) - 1) / 2)), "°")
print("autovalores =", np.round(np.linalg.eigvals(R), 6))
p = np.array([1.0, 1, 0])  # -1 + 1 + 0 = 0: está en el plano -x+y+z=0
print("p =", p, " n.p =", eje @ p, " R p =", R @ p, " n.Rp =", eje @ (R @ p))

# ---------------------------------------------------------------- A: aplicación
print("\n=== A  red de control, dos épocas ===")
P1 = np.array([[5432118.437, 6151874.215],
               [5434602.881, 6152593.062],
               [5433041.590, 6154210.774]])
# deformación verdadera (para generar la época 2): e1 = +40 µε a acimut 60°, e2 = -15 µε,
# giro antihorario de 2", traslación de (12, -8) mm. Las coordenadas de la época 2 se redondean al mm.
az = np.radians(60.0)
u1 = np.array([np.sin(az), np.cos(az)]); u2 = np.array([np.cos(az), -np.sin(az)])
Etrue = 40e-6 * np.outer(u1, u1) - 15e-6 * np.outer(u2, u2)
om = np.radians(2 / 3600)
Ftrue = np.eye(2) + Etrue + np.array([[0, -om], [om, 0]])
c1 = P1.mean(axis=0)
P2 = np.round((P1 - c1) @ Ftrue.T + c1 + np.array([0.012, -0.008]), 3)
D = P2 - P1
print("época 1 =\n", P1)
print("época 2 =\n", P2)
print("desplazamientos (mm) =\n", np.round(D * 1000, 1))
c2 = P2.mean(axis=0)
X1, X2 = P1 - c1, P2 - c2
print("baricentro 1 =", np.round(c1, 4), " baricentro 2 =", np.round(c2, 4))
print("reducidas época 1 =\n", np.round(X1, 4))
print("reducidas época 2 =\n", np.round(X2, 4))
F = X2[:2].T @ np.linalg.inv(X1[:2].T)
print("F (de los puntos 1 y 2) =\n", F)
print("F - I (x1e6) =\n", np.round((F - np.eye(2)) * 1e6, 3))
print("control punto 3: F x1 - x2 =", (F @ X1[2] - X2[2]))
t = c2 - F @ c1
print("t = c2 - F c1 =", np.round(t, 4), " traslación del baricentro c2 - c1 (mm) =", np.round((c2 - c1) * 1000, 2))
print("control residuos todos los puntos:", np.abs(P1 @ F.T + t - P2).max())
E = 0.5 * (F + F.T) - np.eye(2)
omg = 0.5 * (F[1, 0] - F[0, 1])
print("E (µε) =\n", np.round(E * 1e6, 3))
print("ω =", omg, "rad =", round(np.degrees(omg) * 3600, 3), '"')
ev, EV = np.linalg.eigh(E)
ev, EV = ev[::-1], EV[:, ::-1]
for k in range(2):
    v = EV[:, k] * np.sign(EV[1, k] if abs(EV[1, k]) > 1e-12 else EV[0, k])
    azk = np.degrees(np.arctan2(v[0], v[1])) % 180
    print(f"  e{k+1} = {ev[k]*1e6:.3f} µε  dirección (E,N) = {np.round(v, 5)}  acimut = {azk:.2f}°")
trE, detE = np.trace(E), np.linalg.det(E)
disc = np.sqrt((trE / 2) ** 2 - detE)
print("tr E (µε) =", round(trE * 1e6, 3), " det E (µε²) =", round(detE * 1e12, 3), " sqrt((tr/2)^2-det) =", round(disc * 1e6, 3))
print("dilatación = tr E =", round(trE * 1e6, 3), "µε;  cizalla máxima e1-e2 =", round((ev[0] - ev[1]) * 1e6, 3), "µε")
for i, j in ((0, 1), (1, 2), (2, 0)):
    d1v, d2v = P1[j] - P1[i], P2[j] - P2[i]
    d1, d2 = np.linalg.norm(d1v), np.linalg.norm(d2v)
    u = d1v / d1
    azl = np.degrees(np.arctan2(u[0], u[1])) % 360
    pred = u @ E @ u
    print(f"  lado P{i+1}P{j+1}: d1 = {d1:.4f} m  d2 = {d2:.4f} m  Δd = {(d2-d1)*1000:.2f} mm  "
          f"acimut = {azl:.2f}°  Δd/d = {(d2-d1)/d1*1e6:.3f} µε  u^T E u = {pred*1e6:.3f} µε  "
          f"Δd predicho = {pred*d1*1000:.2f} mm")

fig, ax = plt.subplots(figsize=(6.2, 5.6))
X = 5000  # exageración de los desplazamientos
Pk = (P1 - c1) / 1000
ax.add_patch(Polygon(Pk, closed=True, fill=False, ec=GRIS, lw=1.2, ls="--"))
Pe = Pk + D * X / 1000
ax.add_patch(Polygon(Pe, closed=True, fill=False, ec=TEAL, lw=1.6))
for k in range(3):
    ax.annotate("", Pe[k], Pk[k], arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.3))
    ax.text(Pk[k, 0] + .08, Pk[k, 1] - .18, f"$P_{k+1}$", fontsize=11)
    ax.text(Pk[k, 0] + .08, Pk[k, 1] - .38, f"{np.linalg.norm(D[k])*1000:.0f} mm", fontsize=8, color=RUST)
for k, col in ((0, "black"), (1, GOLD)):
    v = EV[:, k]
    ax.plot([-1.6 * v[0], 1.6 * v[0]], [-1.6 * v[1], 1.6 * v[1]], color=col, ls="-.", lw=1.2)
    ax.text(1.7 * v[0], 1.7 * v[1], f"$e_{k+1}={ev[k]*1e6:+.2f}$ µε".replace(".", ",").replace("-", "−"), fontsize=9, color=col,
            ha="center")
ax.annotate("N", (-1.75, 1.85), (-1.75, 1.35), arrowprops=dict(arrowstyle="-|>", color="black"), ha="center")
ax.set_xlim(-2.0, 2.0); ax.set_ylim(-1.8, 2.0); ax.set_aspect("equal")
ax.set_xlabel("E − E$_c$ (km)"); ax.set_ylabel("N − N$_c$ (km)")
ax.grid(color="#eeece6", lw=.6)
ax.set_title("red en la época 1 (gris) y en la época 2 (teal), desplazamientos ×5.000", fontsize=9.5)
fig.tight_layout(); fig.savefig(SALIDA / "autovec_red.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- figuras I y E1
fig, ax = plt.subplots(figsize=(6.4, 5.4))
for k in range(-3, 4):
    for seg in (np.array([[k, -3], [k, 3]]), np.array([[-3, k], [3, k]])):
        ax.plot(*seg.T, color="#dddad3", lw=.7)
        ax.plot(*(seg @ A.T).T, color=TEAL, lw=.7, alpha=.55)
for d, lam, col in (((1, 1), 5, "black"), ((1, -2), 2, GOLD)):
    d = np.array(d, float)
    ax.plot([-8 * d[0], 8 * d[0]], [-8 * d[1], 8 * d[1]], color=col, ls="--", lw=1.2)
    ax.annotate("", A @ d, (0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2.2))
    ax.annotate("", d, (0, 0), arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=2.2))
    ax.text(*(A @ d + [.2, -.1 if lam == 5 else -.5]), f"$Av={lam}v$", color=col)
ax.annotate("", A @ v0, (0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=2))
ax.annotate("", v0, (0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.4, alpha=.5))
ax.text(*(A @ v0 + [.15, -.45]), "$A(1,0)$ gira", color=RUST)
ax.set_xlim(-6, 7); ax.set_ylim(-6, 6.5); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
ax.set_title("grilla deformada por $A$ y sus dos direcciones invariantes", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "autovec_grilla.png", dpi=150); plt.close(fig)

fig, ax = plt.subplots(figsize=(5.4, 5.0))
# x^T S x = 1  <=>  x = V diag(1/sqrt(λ)) (cos, sin)
el = V @ np.diag(1 / np.sqrt(w)) @ circ
ax.fill(*el, color=TEAL, alpha=.15); ax.plot(*el, color=TEAL, lw=1.8)
for k, col in ((1, "black"), (0, GOLD)):
    d = V[:, k] / np.sqrt(w[k])
    ax.plot([-1.3 * V[0, k], 1.3 * V[0, k]], [-1.3 * V[1, k], 1.3 * V[1, k]], color=col, ls="--", lw=1)
    ax.annotate("", d, (0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
ax.text(.42, .02, r"$1/\sqrt{6}\approx0{,}408$" + "\n" + r"sobre $(2,1)$, $\lambda=6$", fontsize=8.5)
ax.text(.47, -.95, r"$1/\sqrt{1}=1$ sobre $(1,-2)$, $\lambda=1$", fontsize=8.5, color="#8a6d00")
ax.axhline(0, color=GRIS, lw=.6); ax.axvline(0, color=GRIS, lw=.6)
ax.set_xlim(-1.3, 1.3); ax.set_ylim(-1.3, 1.3); ax.set_aspect("equal")
ax.set_title(r"$5x^2+4xy+2y^2=1$ y sus ejes principales", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "autovec_elipse.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- Ejercicios
print("\n=== X1  A = [[1,2],[3,2]] ===")
A1 = np.array([[1.0, 2], [3, 2]])
print("poly =", np.poly(A1), " autovalores =", np.roots(np.poly(A1)), " A(2,3) =", A1 @ [2, 3], " A(1,-1) =", A1 @ [1, -1])
print("\n=== X2 ===")
for K in ([[3, -2], [1, 1]], [[3, 1], [0, 3]], [[0, 1], [1, 0]]):
    K = np.array(K, float)
    tr, de = np.trace(K), np.linalg.det(K)
    lk = np.linalg.eigvals(K)
    print(f"  {K.tolist()}: tr={tr:g} det={de:g} disc={tr**2-4*de:g} λ={lk} |λ|={abs(lk)} arg={np.degrees(np.angle(lk))}")
print("  sqrt(5) =", np.sqrt(5), " atan(1/2) =", np.degrees(np.arctan(.5)))
print("\n=== X3  R = Rx(90°) Rz(90°) ===")
R3 = np.round(Rx(np.pi / 2) @ Rz(np.pi / 2), 12)
par, e3 = cuna_filas(R3 - np.eye(3))
print("R =", R3.tolist(), " R-I =", (R3 - np.eye(3)).tolist())
print("filas", par, ": eje =", e3, " R eje =", R3 @ e3, " tr =", np.trace(R3), " θ =", np.degrees(np.arccos((np.trace(R3) - 1) / 2)))
print("\n=== X4  3x^2+2xy+3y^2 = 1 ===")
S4 = np.array([[3.0, 1], [1, 3]])
w4 = np.linalg.eigvalsh(S4)
print("autovalores =", w4, " semiejes =", 1 / np.sqrt(w4), " área =", np.pi / np.sqrt(np.linalg.det(S4)))
print("\n=== X5  E = [[30,10],[10,-10]] µε ===")
E5 = np.array([[30.0, 10], [10, -10]])
w5, V5 = np.linalg.eigh(E5)
print("tr =", np.trace(E5), " det =", np.linalg.det(E5), " autovalores =", w5[::-1])
l51 = w5[-1]
print("λ1 = 10 + sqrt(500) =", 10 + np.sqrt(500), " sqrt(500) =", np.sqrt(500))
v51 = np.array([10, l51 - 30])  # fila 1 de E - λ1 I: (30-λ1, 10) ⟂ (10, λ1-30)
print("E - λ1 I fila 1 =", E5[0] - [l51, 0], " dirección e1 (E,N) ∝", v51, " control:", E5 @ v51 - l51 * v51)
az51 = np.degrees(np.arctan2(v51[0], v51[1]))
print("acimut e1 =", az51, "°  acimut e2 =", az51 + 90, "°")
print("base N 1500 m: u^T E u =", np.array([0, 1]) @ E5 @ [0, 1], "µε → Δd =", -10e-6 * 1500 * 1000, "mm")
