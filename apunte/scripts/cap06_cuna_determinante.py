"""Números y figuras del capítulo «Subespacios, producto cuña y determinante».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Área orientada por cuña»: u = (3,1), v = (1,2); u^v, v^u; triángulo
      a = (1,1), b = (5,2), c = (2,4) con área (b-a)^(c-a)/2 y su sentido.
  E2  Ejemplo «Recta por dos puntos e intersección por cuñas homogéneas»: l = p x q con
      p = (1,2), q = (4,3); m = r x s con r = (0,4), s = (5,0); punto x = l x m.
  E3  Ejemplo «Núcleo de una matriz 2x3 por cuña de filas»: A = [[1,2,-1],[2,0,3]].
  E4  Ejemplo «Determinante 3x3 como volumen con signo»: columnas u = (1,2,0), v = (0,1,1),
      w = (1,0,2); intercambio de columnas; det(AB) = det A det B con A = [[2,1],[0,1]],
      B = [[1,0],[1,3]].
  G   Matriz de la grilla deformada M = [[3,1],[1,2]] (columnas u, v de E1): det = factor de área.
  P   Polígono de la figura de triángulos desde el origen (parcela de la unidad 07a):
      áreas con signo de cada triángulo O p_i p_{i+1} y suma.
  A   Aplicación topográfica: parcela de 6 vértices en coordenadas Gauss-Krüger faja 5;
      fórmula de Gauss (suma de cuñas) con coordenadas completas y reducidas al vértice 1,
      en doble precisión y con aritmética de 12 cifras significativas (decimal); sentido de
      recorrido; triángulos en abanico desde el vértice 1 con cuña y con Herón; rotación de
      30° de las coordenadas reducidas (det = 1); resultado en m² y ha.
  X1  Ejercicio 1: cuñas (2,-1)^(-6,3) y (2,5)^(4,-1).
  X2  Ejercicio 2: recta por (2,1) y (5,3), corte con x + y = 6 y con una paralela.
  X3  Ejercicio 3: A = [[1,2,3],[4,5,6],[7,8,9]]: det, núcleo, rango, imagen.
  X4  Ejercicio 4: plano por (1,0,0), (0,2,0), (0,0,3): normal, ecuación, subespacio lineal
      paralelo, volumen del tetraedro con el origen.
  X5  Ejercicio 5: cuadrilátero (0,0), (120,10), (130,95), (-5,80) en metros.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/cuna-determinante/:
  cuna_paralelogramo.png   paralelogramo de u, v con área +5 y de v, u con área -5.
  cuna_grilla.png          grilla y cuadrado unidad deformados por M, factor de área det M = 5.
  cuna_poligono.png        polígono descompuesto en triángulos orientados desde el origen.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap06_cuna_determinante.py
"""
from decimal import Decimal, getcontext
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "cuna-determinante"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})


def cuna(u, v):
    return u[0] * v[1] - u[1] * v[0]


def h(p):
    return np.array([p[0], p[1], 1.0])


def gauss(P):
    """Área con signo por suma de cuñas (fórmula del agrimensor)."""
    return 0.5 * sum(cuna(P[i], P[(i + 1) % len(P)]) for i in range(len(P)))


# ---------------------------------------------------------------- E1
print("=== E1  área orientada ===")
u, v = np.array([3.0, 1.0]), np.array([1.0, 2.0])
print("u^v =", cuna(u, v), " v^u =", cuna(v, u))
a, b, c = np.array([1.0, 1.0]), np.array([5.0, 2.0]), np.array([2.0, 4.0])
print("b-a =", b - a, " c-a =", c - a, " (b-a)^(c-a) =", cuna(b - a, c - a), " área triángulo =", cuna(b - a, c - a) / 2)
print("orden a,c,b: ", cuna(c - a, b - a) / 2)

# ---------------------------------------------------------------- E2
print("\n=== E2  recta e intersección homogéneas ===")
p, q, r, s = h((1, 2)), h((4, 3)), h((0, 4)), h((5, 0))
l = np.cross(p, q); m = np.cross(r, s); x = np.cross(l, m)
print("l = p x q =", l, " chequeo l.p, l.q =", l @ p, l @ q)
print("m = r x s =", m)
print("x = l x m =", x, " afín =", x[:2] / x[2], " = (35/17, 40/17) =", 35 / 17, 40 / 17)
print("chequeo l.x, m.x =", l @ x, m @ x)

# ---------------------------------------------------------------- E3
print("\n=== E3  núcleo 2x3 ===")
A3 = np.array([[1.0, 2, -1], [2, 0, 3]])
n3 = np.cross(A3[0], A3[1])
print("fila1 x fila2 =", n3, " A n =", A3 @ n3, " rango =", np.linalg.matrix_rank(A3))

# ---------------------------------------------------------------- E4
print("\n=== E4  det 3x3 ===")
U3 = np.column_stack([[1.0, 2, 0], [0, 1, 1], [1, 0, 2]])
print("det[u v w] =", round(np.linalg.det(U3), 6), " det[v u w] =", round(np.linalg.det(U3[:, [1, 0, 2]]), 6))
print("(u x v).w =", np.cross(U3[:, 0], U3[:, 1]) @ U3[:, 2], " u x v =", np.cross(U3[:, 0], U3[:, 1]))
Aa, Bb = np.array([[2.0, 1], [0, 1]]), np.array([[1.0, 0], [1, 3]])
print("AB =", (Aa @ Bb).tolist(), " det A, det B, det AB =", np.linalg.det(Aa), np.linalg.det(Bb), round(np.linalg.det(Aa @ Bb), 6))

# ---------------------------------------------------------------- G: figura grilla
print("\n=== G  grilla deformada ===")
M = np.column_stack([u, v])
print("M =", M.tolist(), " det M =", np.linalg.det(M))
fig, axs = plt.subplots(1, 2, figsize=(9, 4.2))
for ax, T, tit in ((axs[0], np.eye(2), "antes: cuadrado unidad, área 1"), (axs[1], M, r"después de $M$: área $\det M = 5$")):
    for k in range(-1, 4):
        seg = np.array([[k, -1], [k, 3]]).T; ax.plot(*(T @ seg), color="#d8d5ce", lw=.8)
        seg = np.array([[-1, k], [3, k]]).T; ax.plot(*(T @ seg), color="#d8d5ce", lw=.8)
    sq = T @ np.array([[0, 1, 1, 0], [0, 0, 1, 1]])
    ax.add_patch(Polygon(sq.T, closed=True, fc=TEAL, alpha=.25, ec=TEAL, lw=1.5))
    for col, cc, lab in ((0, TEAL, "u" if T is M else "e_1"), (1, RUST, "v" if T is M else "e_2")):
        d = T[:, col]
        ax.annotate("", d, (0, 0), arrowprops=dict(arrowstyle="-|>", color=cc, lw=2))
        ax.text(d[0] * 1.08 + .1, d[1] * 1.08, f"${lab}$", color=cc, fontsize=12)
    ax.set_xlim(-2.5, 6.5) if T is M else ax.set_xlim(-1.5, 3.5)
    ax.set_ylim(-1.8, 4.8) if T is M else ax.set_ylim(-1.5, 3.5)
    ax.set_aspect("equal"); ax.axhline(0, color=GRIS, lw=.6); ax.axvline(0, color=GRIS, lw=.6)
    ax.set_title(tit, fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "cuna_grilla.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- figura paralelogramo
fig, axs = plt.subplots(1, 2, figsize=(9, 3.6))
for ax, (p1, p2, n1, n2, signo) in zip(axs, ((u, v, "u", "v", "+5"), (v, u, "v", "u", "−5"))):
    par = np.array([[0, 0], p1, p1 + p2, p2])
    col = TEAL if signo == "+5" else RUST
    ax.add_patch(Polygon(par, closed=True, fc=col, alpha=.25, ec=col, lw=1.5))
    ax.annotate("", p1, (0, 0), arrowprops=dict(arrowstyle="-|>", color="black", lw=2))
    ax.annotate("", p2, (0, 0), arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=2))
    ax.text(*(p1 * 1.06 + [.05, -.3]), f"${n1}$ (primero)", fontsize=10)
    ax.text(*(p2 * 1.06 + [-.6, .1]), f"${n2}$", fontsize=10, color=GRIS)
    # arco de giro de p1 a p2
    t1, t2 = np.arctan2(p1[1], p1[0]), np.arctan2(p2[1], p2[0])
    tt = np.linspace(t1, t2, 30)
    ax.plot(.9 * np.cos(tt), .9 * np.sin(tt), color=col, lw=1.4)
    ax.annotate("", (.9 * np.cos(tt[-1]), .9 * np.sin(tt[-1])), (.9 * np.cos(tt[-3]), .9 * np.sin(tt[-3])),
                arrowprops=dict(arrowstyle="-|>", color=col, lw=1.4))
    sentido = "antihorario" if signo == "+5" else "horario"
    ax.set_title(fr"${n1}\wedge {n2} = {signo.replace(chr(0x2212), '-')}$  (giro {sentido})", fontsize=10)
    ax.text(*(0.5 * (p1 + p2) - [.25, 0]), signo, fontsize=14, color=col)
    ax.set_xlim(-.6, 4.6); ax.set_ylim(-.6, 3.4); ax.set_aspect("equal")
    ax.set_xticks(range(0, 5)); ax.set_yticks(range(0, 4))
    ax.axhline(0, color=GRIS, lw=.6); ax.axvline(0, color=GRIS, lw=.6)
fig.tight_layout(); fig.savefig(SALIDA / "cuna_paralelogramo.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- P: polígono
print("\n=== P  polígono con triángulos desde el origen ===")
Pp = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)
tri = [cuna(Pp[i], Pp[(i + 1) % 5]) / 2 for i in range(5)]
print("vértices =", Pp.tolist())
print("áreas con signo O p_i p_i+1 =", tri, " suma =", sum(tri))
fig, ax = plt.subplots(figsize=(5.2, 4.8))
for i in range(5):
    t = np.array([[0, 0], Pp[i], Pp[(i + 1) % 5]])
    col = TEAL if tri[i] > 0 else RUST
    ax.add_patch(Polygon(t, closed=True, fc=col, alpha=.18, ec=col, lw=.8))
    cg = t.mean(axis=0)
    ax.text(*(cg - [.2, .05]), f"{tri[i]:+g}".replace(".", ",").replace("-", "−"), color=col, fontsize=9)
ax.add_patch(Polygon(Pp, closed=True, fill=False, ec="black", lw=1.8))
for i, pt in enumerate(Pp):
    ax.plot(*pt, "ko", ms=3); ax.text(pt[0] + (-.45 if i == 4 else .12), pt[1] + .1, f"$p_{i+1}$")
ax.plot(0, 0, "ko", ms=3); ax.text(-.35, -.35, "$O$")
ax.set_xlim(-.6, 6); ax.set_ylim(-.6, 5.8); ax.set_aspect("equal"); ax.grid(color="#eeece6", lw=.6)
ax.set_title(f"suma de triángulos orientados = {sum(tri):g}", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "cuna_poligono.png", dpi=150); plt.close(fig)

# ---------------------------------------------------------------- A: aplicación
print("\n=== A  parcela Gauss-Krüger faja 5 ===")
GK = [("5431218.47", "6152304.12"), ("5431507.83", "6152351.60"), ("5431596.25", "6152158.94"),
      ("5431472.10", "6151987.33"), ("5431260.66", "6151962.78"), ("5431149.39", "6152121.05")]
P = np.array([[float(e), float(n)] for e, n in GK])
S = gauss(P)
print("vértices (E, N) =\n", P)
print("término típico x1*y2 =", P[0, 0] * P[1, 1])
print("Gauss con coordenadas completas (float64): S =", S)
Pr = P - P[0]
print("coordenadas reducidas al vértice 1 =\n", Pr)
Sr = gauss(Pr)
print("Gauss reducidas (float64): S =", Sr, " diferencia =", S - Sr)
print("términos x_i y_i+1 - x_i+1 y_i (reducidas) =", [round(cuna(Pr[i], Pr[(i + 1) % 6]), 4) for i in range(6)])
print("recorrido inverso: S =", gauss(Pr[::-1]))
print("área =", abs(Sr), "m2 =", abs(Sr) / 1e4, "ha")
getcontext().prec = 12
D = [(Decimal(e), Decimal(n)) for e, n in GK]
S12 = sum((D[i][0] * D[(i + 1) % 6][1] - D[(i + 1) % 6][0] * D[i][1]) for i in range(6)) / 2
D0 = D[0]
Dr = [(e - D0[0], n - D0[1]) for e, n in D]
S12r = sum((Dr[i][0] * Dr[(i + 1) % 6][1] - Dr[(i + 1) % 6][0] * Dr[i][1]) for i in range(6)) / 2
print("12 cifras, completas: S =", S12, " error =", float(S12) - Sr)
print("12 cifras, reducidas: S =", S12r, " error =", float(S12r) - Sr)
fan = [cuna(Pr[i], Pr[i + 1]) / 2 for i in range(1, 5)]
print("abanico desde V1 (cuña): triángulos V1 V_i V_i+1 =", [round(t, 3) for t in fan], " suma =", sum(fan))


def heron(a, b, c):
    la, lb, lc = np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)
    sp = (la + lb + lc) / 2
    return np.sqrt(sp * (sp - la) * (sp - lb) * (sp - lc)), (la, lb, lc)


her = [heron(P[0], P[i], P[i + 1]) for i in range(1, 5)]
print("Herón: ", [(round(t, 3), tuple(round(x, 3) for x in L)) for t, L in her], " suma =", sum(t for t, _ in her))
th = np.deg2rad(30)
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
Prot = Pr @ R.T
print("R(30°) =", R.tolist(), " det =", np.linalg.det(R))
print("rotadas =\n", Prot)
print("Gauss rotadas: S =", gauss(Prot), " diferencia =", gauss(Prot) - Sr)

# ---------------------------------------------------------------- Ejercicios
print("\n=== X1 ===")
print("(2,-1)^(-6,3) =", cuna((2, -1), (-6, 3)), " (2,5)^(4,-1) =", cuna((2, 5), (4, -1)))
print("\n=== X2 ===")
l2 = np.cross(h((2, 1)), h((5, 3))); m2 = np.array([1.0, 1, -6]); x2 = np.cross(l2, m2)
print("l =", l2, " m =", m2, " l x m =", x2, " afín =", x2[:2] / x2[2])
par = np.array([-2.0, 3, 4]); print("paralela", par, " l x par =", np.cross(l2, par))
print("\n=== X3 ===")
A9 = np.arange(1.0, 10).reshape(3, 3)
print("det =", round(np.linalg.det(A9), 10), " f1 x f2 =", np.cross(A9[0], A9[1]), " A n =", A9 @ np.cross(A9[0], A9[1]),
      " rango =", np.linalg.matrix_rank(A9), " c1 x c2 =", np.cross(A9[:, 0], A9[:, 1]))
print("\n=== X4 ===")
p1, p2, p3 = np.array([1.0, 0, 0]), np.array([0.0, 2, 0]), np.array([0.0, 0, 3])
nn = np.cross(p2 - p1, p3 - p1)
print("normal =", nn, " d = n.p1 =", nn @ p1, " det[p1 p2 p3] =", np.linalg.det(np.column_stack([p1, p2, p3])),
      " volumen tetraedro =", abs(np.linalg.det(np.column_stack([p1, p2, p3]))) / 6)
print("\n=== X5 ===")
Q = np.array([[0.0, 0], [120, 10], [130, 95], [-5, 80]])
print("términos =", [cuna(Q[i], Q[(i + 1) % 4]) for i in range(4)], " S =", gauss(Q), " ha =", gauss(Q) / 1e4)
print("trasladado por (5431000, 6152000): S =", gauss(Q + [5431000, 6152000]))
