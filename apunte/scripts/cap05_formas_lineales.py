"""Números y figuras del capítulo «Formas lineales: el gradiente no es un vector».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Base dual de una base oblicua»: b1 = (2,0), b2 = (1,1); filas de B^-1 como base
      dual e^1, e^2; componentes del vector v = (3,2) y de la forma phi = (2,3) en esas bases;
      phi(v) calculado de las dos maneras.
  E2  Ejemplo «El gradiente de h(x,y) = x^2 + x y + 2 y en (1,2)»: dh = (4,3), acción sobre
      cuatro desplazamientos chicos, cambio real de h y error; recta tangente a la curva de nivel.
  E3  Ejemplo «Cambiar la unidad del eje x»: P = diag(2,1); fila dh P, columna P^-1 v, producto
      invariante; lo que daría tratar al gradiente como vector (P^-1 dh^T).
  E4  Ejemplo «El mismo gradiente con una métrica oblicua»: G = [[1, 1/2],[1/2, 1]]; vector
      asociado G^-1 dh^T, ángulos, separación entre niveles 1/sqrt(dh G^-1 dh^T).
  A   Aplicación topográfica: plano por tres cotas (Gauss-Krüger faja 5), forma dh = (a,b),
      pendiente máxima (%), acimut, pendiente en acimut 120°, dirección de la curva de nivel,
      verificación con desplazamientos de 50 m; mismo cálculo con N en km.
  X1  Ejercicio 1: forma con phi(1,2) = 5, phi(3,-1) = 1; núcleo y separación entre niveles.
  X2  Ejercicio 2: base dual de b1 = (1,1), b2 = (-1,2); componentes de v = (1,4) y de omega = (3,1).
  X3  Ejercicio 3: h = x^2 y en (1,3) y base b1 = (1,0), b2 = (1,1): fila, columna, invariancia.
  X4  Ejercicio 4: la selectora x con ejes a 60° (G = [[1, 1/2],[1/2, 1]]): vector asociado,
      largo y separación entre niveles.
  X5  Ejercicio 5: pendiente de 3 % hacia acimut 210°: forma dh y cambio de cota a 40 m al este.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/formas-lineales/:
  fl_pila_vs_flecha.png  la forma dh = (4,3) de E2 como pila de niveles (cuenta de rectas cruzadas)
                         frente a la flecha (4,3) (dos paneles).
  fl_base_oblicua.png    base oblicua b1, b2 de E1 con las rectas de nivel de e^1 y e^2: el vector
                         v = (3,2) leído como 0,5 b1 + 2 b2.
  fl_metrica.png         la misma forma con métrica euclídea y con ejes a 60° (E4): niveles
                         idénticos, «vector gradiente» distinto.
  fl_terreno.png         aplicación: tres puntos acotados, curvas de nivel del plano ajustado,
                         dirección de máxima pendiente y de la curva de nivel.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap05_formas_lineales.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "formas-lineales"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, TEALD, RUST, GOLD, GRIS = "#01696F", "#0C4E54", "#A84B2F", "#D19900", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "figure.facecolor": "white"})


def az(v):
    """Acimut (grados, desde el norte, horario) de un vector (E, N)."""
    return np.rad2deg(np.arctan2(v[0], v[1])) % 360


# ---------------------------------------------------------------- E1
print("=== E1  base dual de b1=(2,0), b2=(1,1) ===")
B = np.array([[2.0, 1.0], [0.0, 1.0]])
Binv = np.linalg.inv(B)
print("B^-1 =\n", Binv, "\n e^1 =", Binv[0], " e^2 =", Binv[1])
print("e^i(b_j) =\n", Binv @ B)
v = np.array([3.0, 2.0]); phi = np.array([2.0, 3.0])
cv = Binv @ v; cphi = phi @ B
print("componentes de v:", cv, " componentes de phi (phi(b1), phi(b2)):", cphi)
print("phi(v) canónico =", phi @ v, " con componentes =", cphi @ cv)

# ---------------------------------------------------------------- E2
print("\n=== E2  h = x^2 + x y + 2 y en (1,2) ===")
h = lambda x, y: x**2 + x * y + 2 * y
p0 = np.array([1.0, 2.0])
dh = np.array([2 * p0[0] + p0[1], p0[0] + 2])
print("h(p0) =", h(*p0), " dh =", dh)
for w in ([0.1, 0.0], [0.0, 0.1], [0.08, 0.06], [0.06, -0.08], [-0.03, 0.04]):
    w = np.array(w)
    real = h(*(p0 + w)) - h(*p0)
    print(f"  w={w}: dh(w)={dh @ w:.4f}  real={real:.4f}  error={real - dh @ w:.4f}")
print("separación entre niveles de dh: 1/|dh| =", 1 / np.linalg.norm(dh))

# ---------------------------------------------------------------- E3
print("\n=== E3  P = diag(2,1) ===")
P = np.diag([2.0, 1.0])
w = np.array([0.1, 0.0])
print("fila nueva dh P =", dh @ P, " columna nueva P^-1 w =", np.linalg.solve(P, w),
      " producto =", (dh @ P) @ np.linalg.solve(P, w))
print("si fuera vector: P^-1 dh =", np.linalg.solve(P, dh), " daría",
      np.linalg.solve(P, dh) @ np.linalg.solve(P, w))
w2 = np.array([0.08, 0.06])
print("w2 =", w2, " nueva columna", np.linalg.solve(P, w2), " dh P · =", (dh @ P) @ np.linalg.solve(P, w2))

# ---------------------------------------------------------------- E4
print("\n=== E4  métrica oblicua G = [[1,1/2],[1/2,1]] ===")
G = np.array([[1.0, 0.5], [0.5, 1.0]])
g = np.linalg.solve(G, dh)
print("g = G^-1 dh =", g, " g^T G w para w=(0.1,0):", g @ G @ np.array([0.1, 0.0]))
nG = np.sqrt(dh @ np.linalg.solve(G, dh))
print("|dh|_G* =", nG, " separación entre niveles =", 1 / nG, " (euclídea:", 1 / np.linalg.norm(dh), ")")
# dibujo: ejes a 60°: e1=(1,0), e2=(cos60, sin60)
Emb = np.array([[1.0, 0.5], [0.0, np.sqrt(3) / 2]])
print("comprobación E^T E =", Emb.T @ Emb)
print("g dibujado en el papel (E g) =", Emb @ g, " ángulo con la horizontal =",
      np.rad2deg(np.arctan2(*(Emb @ g)[::-1])))
print("(4,3) como columna en el papel (E dh) =", Emb @ dh, " ángulo =", np.rad2deg(np.arctan2(*(Emb @ dh)[::-1])))
print("ángulo de (4,3) euclídeo =", np.rad2deg(np.arctan2(3, 4)))
# perpendicularidad: núcleo de dh = (3,-4) en coordenadas; g^T G (3,-4)
print("g^T G (3,-4) =", g @ G @ np.array([3.0, -4.0]))

# ---------------------------------------------------------------- A
print("\n=== A  aplicación topográfica ===")
pts = np.array([[5512340.00, 6172480.00, 32.45],
                [5512420.00, 6172510.00, 34.27],
                [5512360.00, 6172580.00, 33.98]])
d = pts[1:, :2] - pts[0, :2]
dhz = pts[1:, 2] - pts[0, 2]
a, b = np.linalg.solve(d, dhz)
print("ΔE,ΔN =", d.tolist(), " Δh =", dhz)
print(f"a = {a:.6f}  b = {b:.6f}")
gm = np.hypot(a, b)
print(f"pendiente máxima = {gm:.6f} = {100 * gm:.3f} %  acimut = {az([a, b]):.2f}°  ángulo = {np.rad2deg(np.arctan(gm)):.3f}°")
u120 = np.array([np.sin(np.deg2rad(120)), np.cos(np.deg2rad(120))])
s120 = np.array([a, b]) @ u120
print(f"versor az 120 = {u120}, pendiente = {s120:.6f} = {100 * s120:.3f} %")
nucleo = np.array([-b, a]) / gm
print(f"curva de nivel: versor {nucleo}, acimut {az(nucleo):.2f}° / {az(-nucleo):.2f}°")
umax = np.array([a, b]) / gm
for nombre, u in (("máx", umax), ("nivel", nucleo), ("az120", u120)):
    D = 50 * u
    Pn = pts[0, :2] + D
    hn = pts[0, 2] + a * D[0] + b * D[1]
    print(f"  50 m {nombre}: ΔE={D[0]:.3f} ΔN={D[1]:.3f} punto=({Pn[0]:.3f}; {Pn[1]:.3f}) Δh={a * D[0] + b * D[1]:.4f} h={hn:.4f}")
# comprobación de las tres cotas
for k in range(3):
    dd = pts[k, :2] - pts[0, :2]
    print("  cota ajustada", k + 1, pts[0, 2] + a * dd[0] + b * dd[1])
# N en km
print("--- N en km ---")
a2, b2 = a, 1000 * b
print(f"forma en (E m, N km): ({a2:.6f}, {b2:.4f})")
fl = np.array([a2, b2])            # «flecha» si se la toma como vector en (ΔE m, ΔN km)
fl_m = np.array([fl[0], 1000 * fl[1]])   # en metros sobre el terreno
print(f"flecha en terreno (m) = {fl_m}, acimut = {az(fl_m):.4f}°  (correcto {az([a, b]):.2f}°)")
D = 50 * umax
Dkm = np.array([D[0], D[1] / 1000])
print(f"desplazamiento máx en (m, km) = ({Dkm[0]:.3f}; {Dkm[1]:.6f}), forma da {fl @ Dkm:.4f}")
Dfl = 50 * fl_m / np.linalg.norm(fl_m)
print(f"50 m según la flecha mal levantada: ΔE={Dfl[0]:.4f} ΔN={Dfl[1]:.4f}  Δh = {a * Dfl[0] + b * Dfl[1]:.4f}")
Gkm = np.diag([1.0, 1e6])
gup = np.linalg.solve(Gkm, fl)
print("levantado con G = diag(1, 10^6):", gup, " en metros:", [gup[0], 1000 * gup[1]])

# ---------------------------------------------------------------- X1
print("\n=== X1 ===")
M = np.array([[1.0, 2.0], [3.0, -1.0]])
w1 = np.linalg.solve(M, [5.0, 1.0])
print("phi =", w1, " separación 1/|phi| =", 1 / np.linalg.norm(w1), " phi(2,-1) =", w1 @ [2, -1],
      " phi(4,1) =", w1 @ [4, 1])

# ---------------------------------------------------------------- X2
print("\n=== X2 ===")
B2 = np.array([[1.0, -1.0], [1.0, 2.0]])
B2i = np.linalg.inv(B2)
print("det =", np.linalg.det(B2), " B^-1 =\n", B2i)
print("componentes v=(1,4):", B2i @ [1, 4], " componentes omega=(3,1):", np.array([3.0, 1.0]) @ B2,
      " omega(v) =", np.array([3, 1]) @ [1, 4])

# ---------------------------------------------------------------- X3
print("\n=== X3 ===")
dh3 = np.array([2 * 1 * 3, 1.0])
P3 = np.array([[1.0, 1.0], [0.0, 1.0]])
w3 = np.array([0.2, 0.1])
print("dh =", dh3, " dh P =", dh3 @ P3, " P^-1 w =", np.linalg.solve(P3, w3),
      " productos:", dh3 @ w3, (dh3 @ P3) @ np.linalg.solve(P3, w3))
print("como vector: P^-1 dh =", np.linalg.solve(P3, dh3), " daría", np.linalg.solve(P3, dh3) @ np.linalg.solve(P3, w3))
hx = lambda x, y: x**2 * y
print("cambio real h(1.2,3.1)-h(1,3) =", hx(1.2, 3.1) - hx(1, 3))

# ---------------------------------------------------------------- X4
print("\n=== X4 ===")
g4 = np.linalg.solve(G, [1.0, 0.0])
n4 = np.sqrt(np.array([1.0, 0.0]) @ g4)
print("g =", g4, " largo =", n4, " separación =", 1 / n4, " sin60 =", np.sin(np.deg2rad(60)))
print("g en el papel =", Emb @ g4)

# ---------------------------------------------------------------- X5
print("\n=== X5 ===")
a5, b5 = 0.03 * np.sin(np.deg2rad(210)), 0.03 * np.cos(np.deg2rad(210))
print(f"dh = ({a5:.5f}, {b5:.5f})  Δh 40 m al este = {40 * a5:.3f}  40 m al norte = {40 * b5:.4f}")
u300 = np.array([np.sin(np.deg2rad(300)), np.cos(np.deg2rad(300))])
print(f"az 300: pendiente = {100 * np.array([a5, b5]) @ u300:.3f} %")

# ================================================================ figuras
def niveles(ax, w, valores, xr, yr, M=np.eye(2), **kw):
    """Rectas w·c = k en coordenadas c, dibujadas en el papel con la matriz M (papel = M c)."""
    nuc = np.array([-w[1], w[0]])
    for k in valores:
        c0 = w * k / (w @ w)
        ts = np.linspace(-20, 20, 2)
        seg = np.array([c0 + t * nuc for t in ts]) @ M.T
        ax.plot(seg[:, 0], seg[:, 1], **kw)


# fl_pila_vs_flecha.png
fig, axs = plt.subplots(1, 2, figsize=(9, 4.3))
for ax in axs:
    ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.3, 1.1); ax.set_aspect("equal")
    ax.axhline(0, color=GRIS, lw=.6); ax.axvline(0, color=GRIS, lw=.6)
ax = axs[0]
niveles(ax, dh, np.arange(-2, 8), None, None, color=TEAL, lw=.9)
niveles(ax, dh, [0], None, None, color=TEAL, lw=2)
for k in range(0, 6):
    c = dh * k / (dh @ dh) + np.array([-3.0, 4.0]) * 0.045
    ax.text(*c, str(k), color=TEAL, fontsize=8, ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=.5))
wv = np.array([0.8, 0.0])
ax.annotate("", xy=wv, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.6))
ax.text(0.45, -0.12, r"$w=(0{,}8;\ 0)$: cruza 3,2 marcas", color=RUST, ha="center", fontsize=9)
wv2 = np.array([0.6, 0.8])
ax.annotate("", xy=wv2, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.6))
ax.text(0.62, 0.86, r"$w=(0{,}6;\ 0{,}8)$: 4,8 marcas", color="#8a6500", fontsize=9)
ax.set_title("la forma $dh=(4,3)$: marcas cada $1/5$\n(niveles $0, 1, 2, \\ldots$ de $dh$)", fontsize=10)
ax = axs[1]
ax.annotate("", xy=dh / 5, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=TEALD, lw=2))
ax.text(0.83, 0.62, "flecha $(4,3)/5$", color=TEALD, fontsize=9)
ax.annotate("", xy=wv, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=1.6))
ax.text(0.45, -0.12, r"$w=(0{,}8;\ 0)$", color=RUST, ha="center", fontsize=9)
ax.set_title("la flecha: necesita producto interno\n($(4,3)\\cdot w$) para medir", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "fl_pila_vs_flecha.png", dpi=150); plt.close(fig)

# fl_base_oblicua.png
fig, ax = plt.subplots(figsize=(6.2, 4.6))
ax.set_xlim(-1.2, 5.2); ax.set_ylim(-1.2, 3.4); ax.set_aspect("equal")
niveles(ax, Binv[0], np.arange(-2, 6, 0.5), None, None, color=TEAL, lw=.7, alpha=.8)
niveles(ax, Binv[1], np.arange(-2, 5, 0.5), None, None, color=RUST, lw=.7, alpha=.8)
for vec, col, lab, off in ((B[:, 0], TEALD, "$b_1=(2,0)$", (0.05, -0.3)), (B[:, 1], "#7a2f1a", "$b_2=(1,1)$", (-0.75, 0.1))):
    ax.annotate("", xy=vec, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=col, lw=2))
    ax.text(vec[0] + off[0], vec[1] + off[1], lab, color=col, fontsize=10)
ax.annotate("", xy=v, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="k", lw=1.8))
ax.plot([0, 1, 3], [0, 0, 2], ls="--", color="k", lw=.9)
ax.text(3.05, 2.05, "$v=(3,2)=0{,}5\\,b_1+2\\,b_2$", fontsize=10)
ax.text(-1.1, 3.1, "teal: niveles de $e^1=(\\frac{1}{2},-\\frac{1}{2})$ (paralelos a $b_2$)", color=TEAL, fontsize=8.5)
ax.text(-1.1, 2.8, "óxido: niveles de $e^2=(0,1)$ (paralelos a $b_1$)", color=RUST, fontsize=8.5)
ax.set_title("base oblicua y base dual: niveles $0, \\frac{1}{2}, 1, \\ldots$ de $e^1$ y $e^2$", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "fl_base_oblicua.png", dpi=150); plt.close(fig)

# fl_metrica.png
fig, axs = plt.subplots(1, 2, figsize=(9, 4.3))
for ax, Mm, tit, gg in ((axs[0], np.eye(2), "ejes ortogonales ($G=I$)", dh),
                        (axs[1], Emb, "ejes a $60^\\circ$ ($G=E^TE$)", g)):
    ax.set_xlim(-0.6, 1.5); ax.set_ylim(-0.6, 1.2); ax.set_aspect("equal")
    for k in np.arange(-3, 4):
        s = np.array([[k, -5], [k, 5]]) @ Mm.T
        ax.plot(s[:, 0], s[:, 1], color="#d8d6d0", lw=.6)
        s = np.array([[-5, k], [5, k]]) @ Mm.T
        ax.plot(s[:, 0], s[:, 1], color="#d8d6d0", lw=.6)
    niveles(ax, dh, np.arange(-3, 8), None, None, M=Mm, color=TEAL, lw=.9)
    niveles(ax, dh, [0], None, None, M=Mm, color=TEAL, lw=2)
    for e, lab in ((Mm[:, 0], "$x$"), (Mm[:, 1], "$y$")):
        ax.annotate("", xy=e, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GRIS, lw=1.2))
        ax.text(*(e * 1.08), lab, color=GRIS)
    niveles(ax, dh, [3], None, None, M=Mm, color=GOLD, lw=1.4, ls="--")
    p = Mm @ (3 * gg / (dh @ gg))          # vector asociado G^-1 dh^T, escalado hasta el nivel 3
    q = Mm @ (3 * dh / (dh @ dh))          # la fila (4,3) tomada como columna, escalada hasta el nivel 3
    if not np.allclose(p, q):
        ax.annotate("", xy=q, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=GOLD, lw=1.8))
        ax.text(q[0] + .03, q[1] + .04, "$(4,3)$ como columna", color="#8a6500", fontsize=8.5)
    ax.annotate("", xy=p, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=2))
    ax.text(p[0] + .03, p[1] - .1, "$G^{-1}dh^T$", color=RUST, fontsize=9)
    ax.set_title(tit + "\nmisma fila $dh=(4,3)$; nivel 3 punteado", fontsize=9.5)
fig.tight_layout(); fig.savefig(SALIDA / "fl_metrica.png", dpi=150); plt.close(fig)

# fl_terreno.png
fig, ax = plt.subplots(figsize=(6.2, 5.2))
E0, N0 = pts[0, 0], pts[0, 1]
EE, NN = np.meshgrid(np.linspace(-30, 130, 200), np.linspace(-30, 130, 200))
HH = pts[0, 2] + a * EE + b * NN
cs = ax.contour(EE, NN, HH, levels=np.arange(31.5, 36.6, 0.5), colors=TEAL, linewidths=.8)
ax.clabel(cs, fmt=lambda x: f"{x:.1f}".replace(".", ","), fontsize=7)
for k, (lab, off) in enumerate((("$P_1$", (-14, -9)), ("$P_2$", (4, -9)), ("$P_3$", (4, 3)))):
    dE, dN = pts[k, 0] - E0, pts[k, 1] - N0
    ax.plot(dE, dN, "o", color="k", ms=4)
    ax.text(dE + off[0], dN + off[1], lab + f" {pts[k, 2]:.2f} m".replace(".", ","), fontsize=9)
ax.annotate("", xy=50 * umax, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=RUST, lw=2))
ax.text(*(50 * umax + [2, 2]), "máxima pendiente\n(50 m)", color=RUST, fontsize=8.5)
ax.annotate("", xy=50 * nucleo, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color=TEALD, lw=2))
ax.text(*(50 * nucleo + [3, 4]), "curva de nivel (50 m)", color=TEALD, fontsize=8.5)
ax.set_aspect("equal"); ax.set_xlabel("$\\Delta E$ (m) desde $P_1$"); ax.set_ylabel("$\\Delta N$ (m) desde $P_1$")
ax.set_title("plano ajustado: curvas cada 0,5 m", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "fl_terreno.png", dpi=150); plt.close(fig)
print("\nfiguras en", SALIDA)
