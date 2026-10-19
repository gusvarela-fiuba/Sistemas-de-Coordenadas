"""Números y figuras de la aplicación del complemento C1 «Transformaciones proyectivas»:
enderezar la foto de una fachada.

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  F0  Pared sintética, en metros, con el origen en el vértice inferior izquierdo de la
      ventana, x hacia la derecha e y hacia arriba: ventana de 1,50 x 1,20 m (V1..V4) y
      puerta (P1..P4) con x de 2,40 a 3,30 e y de -0,95 a 1,10 (0,90 x 2,05 m).
  F1  La foto: una homografía conocida H_v (pared -> foto) armada como la de una cámara
      de distancia focal 1300 px y centro (800, 600) en una imagen de 1600 x 1200 px,
      girada 40 grados respecto de la pared y levantada 12 grados. Coordenadas de imagen
      (c, f): columna y fila en píxeles, la fila crece hacia abajo. A cada vértice se le
      suma ruido normal de 0,5 px (numpy default_rng, semilla 2026) y se redondea a 0,1 px.
  F2  DLT con h33 = 1: sistema 8 x 8 con los cuatro vértices de la ventana (foto -> pared),
      matriz H; comprobación con el método del patrón H = K2 K1^{-1} del complemento.
  F3  Paralelismo perdido: pendientes de los lados de la ventana en la foto, punto de fuga
      de los horizontales F_h y de los verticales F_v, recta del horizonte F_h x F_v y su
      comparación con la tercera fila de H.
  F4  Rectas que siguen rectas: el punto medio en la foto del borde izquierdo de la
      puerta, su imagen alineada con los extremos (determinante) y la altura a la que cae
      (la razón simple no se conserva).
  F5  Razón doble sobre la recta del alféizar (y = 0 en la pared): V1, V2 y los cortes Q, R
      de esa recta con los bordes de la puerta, en la foto (coordenada c) y en la pared
      enderezada (coordenada x); valor de la pared verdadera, 16/11.
  F6  Medidas de la puerta en la pared enderezada (lados y promedio) contra 0,90 x 2,05 m,
      y la medida ingenua «con regla» sobre la foto.
  F7  Ejercicios: punto medio del alféizar en la foto (imagen de (0,75; 0) y conjugado
      armónico de F_h respecto de V1, V2 sobre la coordenada c).

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/proyectivas/:
  c1_fachada_foto.png        la foto (marco 1600 x 1200) con la ventana y la puerta, las
                             prolongaciones de los lados hasta los puntos de fuga y el horizonte.
  c1_fachada_enderezada.png  la pared enderezada por H, con las medidas de la puerta y los
                             cuatro puntos de la razón doble sobre la recta y = 0.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/c1_proyectivas.py
"""
from fractions import Fraction
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "proyectivas"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, TINTA = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#3d3a35"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "svg.hashsalt": "c1", "path.simplify": False})
deg = np.pi / 180


def hom(p):
    p = np.atleast_2d(p)
    return np.c_[p, np.ones(len(p))]


def aplicar(H, p):
    q = (H @ hom(p).T).T
    return q[:, :2] / q[:, 2:]


def razon_doble(a, b, c, d):
    return ((c - a) * (d - b)) / ((c - b) * (d - a))


def patron(P):
    """Matriz K con K e_i ~ p_i (cuatro puntos en homogéneas como columnas)."""
    M = P[:, :3]
    lam = np.linalg.solve(M, P[:, 3])
    return M * lam


def fmt(x, n=1):
    return f"{x:.{n}f}".replace(".", ",")


# ---------------------------------------------------------------- F0
print("=== F0  pared ===")
VENT = np.array([[0, 0], [1.5, 0], [1.5, 1.2], [0, 1.2]], float)          # V1..V4
PUER = np.array([[2.4, -0.95], [3.3, -0.95], [3.3, 1.1], [2.4, 1.1]], float)  # P1..P4
print("ventana 1,50 x 1,20; puerta 0,90 x 2,05")

# ---------------------------------------------------------------- F1
print("\n=== F1  foto sintética ===")


def Rx(b):
    c, s = np.cos(b), np.sin(b)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(a):
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


Kc = np.array([[1300.0, 0, 800], [0, 1300, 600], [0, 0, 1]])
Rc = Rx(-12 * deg) @ Ry(-40 * deg)
Hv = Kc @ np.column_stack([Rc @ [1, 0, 0], Rc @ [0, -1, 0], Rc @ [0.8, -0.5, 4.0]])
Hv = Hv / Hv[2, 2]
print("H_v (pared -> foto) =\n", Hv)
rng = np.random.default_rng(2026)
ruido = rng.normal(0, 0.5, size=(8, 2))
FOTO = np.round(aplicar(Hv, np.r_[VENT, PUER]) + ruido, 1)
v_f, p_f = FOTO[:4], FOTO[4:]
for nom, q in zip(["V1", "V2", "V3", "V4", "P1", "P2", "P3", "P4"], FOTO):
    print(f"{nom}: c = {q[0]:.1f}, f = {q[1]:.1f}")
assert np.all((FOTO[:, 0] > 0) & (FOTO[:, 0] < 1600) & (FOTO[:, 1] > 0) & (FOTO[:, 1] < 1200))
FOTO_TXT = [[93.3, 692.1], [567.7, 730.9], [581.0, 405.2], [139.2, 290.2],
            [768.2, 997.9], [935.5, 985.7], [925.3, 516.3], [770.9, 477.9]]
assert np.array_equal(FOTO, np.array(FOTO_TXT))

# ---------------------------------------------------------------- F2
print("\n=== F2  DLT con h33 = 1 ===")
A8, b8 = [], []
for (c, f), (x, y) in zip(v_f, VENT):
    A8.append([c, f, 1, 0, 0, 0, -c * x, -f * x]); b8.append(x)
    A8.append([0, 0, 0, c, f, 1, -c * y, -f * y]); b8.append(y)
A8, b8 = np.array(A8), np.array(b8)
h = np.linalg.solve(A8, b8)
H = np.r_[h, 1.0].reshape(3, 3)
print("filas del sistema que aporta V2:\n", A8[2:4], b8[2:4])
assert np.allclose(A8[2], [567.7, 730.9, 1, 0, 0, 0, -851.55, -1096.35]) and np.allclose(A8[3, 6:], 0)
print("H (foto -> pared) =\n", H)
for i in range(3):
    print("  fila", i + 1, "  ".join(f"{v:.6e}" for v in H[i]))
assert np.allclose(aplicar(H, v_f), VENT, atol=1e-9)
H2 = patron(hom(VENT).T) @ np.linalg.inv(patron(hom(v_f).T))
H2 = H2 / H2[2, 2]
assert np.allclose(H2, H, rtol=1e-8, atol=1e-12)
print("método del patrón: coincide")
# valores redondeados que cita el texto
H_TXT = np.array([[2.5710, 0.2936, -443.09], [0.2342, -2.8633, 1959.87], [-0.4539, 0.1072, 1000]])
TOL = np.array([[5e-5, 5e-5, 5e-3], [5e-5, 5e-5, 5e-3], [5e-5, 5e-5, 0]]) + 1e-12
assert np.all(np.abs(1000 * H - H_TXT) <= TOL), 1000 * H

# ---------------------------------------------------------------- F3
print("\n=== F3  puntos de fuga y horizonte ===")
V = hom(v_f)
abajo, arriba = np.cross(V[0], V[1]), np.cross(V[3], V[2])
izq, der = np.cross(V[0], V[3]), np.cross(V[1], V[2])
ang = lambda p, q: np.degrees(np.arctan2(-(q[1] - p[1]), q[0] - p[0]))  # fila hacia abajo
a_ab, a_ar = ang(v_f[0], v_f[1]), ang(v_f[3], v_f[2])
a_iz, a_de = ang(v_f[0], v_f[3]), ang(v_f[1], v_f[2])
print(f"inclinación lado de abajo {a_ab:.2f}°, de arriba {a_ar:.2f}°")
print(f"inclinación lado izquierdo {a_iz:.2f}°, derecho {a_de:.2f}°")
Fh = np.cross(abajo, arriba); Fh = Fh / Fh[2]
Fv = np.cross(izq, der); Fv = Fv / Fv[2]
print("F_h =", Fh[:2], " F_v =", Fv[:2])
horiz = np.cross(Fh, Fv)
horiz = horiz / horiz[2]
fila3 = H[2] / H[2, 2]
print("horizonte (normalizado) =", horiz, " tercera fila de H =", fila3)
assert np.allclose(horiz, fila3, rtol=1e-6)
assert abs((H @ Fh)[2]) < 1e-9 * np.linalg.norm(H @ Fh) and abs((H @ Fv)[2]) < 1e-9 * np.linalg.norm(H @ Fv)
TXT_F3 = dict(a_ab=-4.68, a_ar=-14.59, a_iz=83.48, a_de=87.66, Fh=(2411.6, 881.7), Fv=(834.2, -5795.1))
assert abs(a_ab - TXT_F3["a_ab"]) < 0.006 and abs(a_ar - TXT_F3["a_ar"]) < 0.006
assert abs(a_iz - TXT_F3["a_iz"]) < 0.006 and abs(a_de - TXT_F3["a_de"]) < 0.006
assert np.allclose(np.round(Fh[:2], 1), TXT_F3["Fh"]) and np.allclose(np.round(Fv[:2], 1), TXT_F3["Fv"])
# la pendiente del horizonte en la foto: f = -(h31 c + 1)/h32 ... recta h31 c + h32 f + 1 = 0
print(f"horizonte: f = {-1 / fila3[1]:.1f} {-fila3[0] / fila3[1]:+.4f} c")

# ---------------------------------------------------------------- F4
print("\n=== F4  rectas en rectas, razón simple perdida ===")
m_f = (p_f[0] + p_f[3]) / 2
tres = aplicar(H, np.array([p_f[0], m_f, p_f[3]]))
det = np.linalg.det(hom(tres))
print("punto medio en la foto =", m_f, " -> pared", tres[1])
print("det de los tres puntos en la pared =", det)
assert abs(det) < 1e-9
t = (tres[1, 1] - tres[0, 1]) / (tres[2, 1] - tres[0, 1])
print(f"altura del punto: {tres[1, 1]:.3f} m; fracción del borde = {t:.3f} (no 0,5)")
assert np.allclose(m_f, [769.55, 737.9])
assert abs(t - 0.480) < 5e-4 and abs(tres[1, 1] - 0.037) < 5e-4 and abs(tres[1, 0] - 2.401) < 5e-4

# ---------------------------------------------------------------- F5
print("\n=== F5  razón doble sobre la recta y = 0 ===")
P = hom(p_f)
Q = np.cross(abajo, np.cross(P[0], P[3])); Q = Q / Q[2]
Rr = np.cross(abajo, np.cross(P[1], P[2])); Rr = Rr / Rr[2]
cs = [v_f[0, 0], v_f[1, 0], Q[0], Rr[0]]
xs_pts = aplicar(H, np.array([v_f[0], v_f[1], Q[:2], Rr[:2]]))
assert np.allclose(xs_pts[:, 1], 0, atol=1e-9)
xs = xs_pts[:, 0]
rd_foto, rd_pared = razon_doble(*cs), razon_doble(*xs)
rd_real = razon_doble(Fraction(0), Fraction(3, 2), Fraction(12, 5), Fraction(33, 10))
print("foto: c =", np.round(cs, 1), " razón doble =", rd_foto)
print("pared: x =", np.round(xs, 3), " razón doble =", rd_pared)
print("pared verdadera: (0, 1,5; 2,4, 3,3) =", rd_real, "=", float(rd_real))
assert abs(rd_foto - rd_pared) < 1e-9
assert rd_real == Fraction(16, 11)
assert abs(rd_foto - 1.4523) < 5e-5
assert np.allclose(np.round(cs, 1), [93.3, 567.7, 769.5, 930.6])
assert np.allclose(np.round(xs, 3), [0, 1.5, 2.401, 3.296])
rs_foto = (cs[1] - cs[0]) / (cs[2] - cs[0])
print(f"razón simple V1V2/V1Q: foto {rs_foto:.3f}, pared {xs[1] / xs[2]:.3f}, real {1.5 / 2.4:.3f}")
assert abs(rs_foto - 0.702) < 5e-4 and abs(xs[1] / xs[2] - 0.625) < 5e-4

# ---------------------------------------------------------------- F6
print("\n=== F6  la puerta medida en la pared enderezada ===")
pz = aplicar(H, p_f)
print("puerta enderezada:\n", pz)
lados = {"abajo": np.linalg.norm(pz[1] - pz[0]), "arriba": np.linalg.norm(pz[2] - pz[3]),
         "izquierdo": np.linalg.norm(pz[3] - pz[0]), "derecho": np.linalg.norm(pz[2] - pz[1])}
for k, v in lados.items():
    print(f"  lado {k}: {v:.3f} m")
ancho = (lados["abajo"] + lados["arriba"]) / 2
alto = (lados["izquierdo"] + lados["derecho"]) / 2
print(f"ancho {ancho:.3f} m  alto {alto:.3f} m  (verdaderos 0,900 y 2,050)")
ang_bordes = np.degrees(np.arctan2(pz[3, 0] - pz[0, 0], pz[3, 1] - pz[0, 1])
                        - np.arctan2(pz[2, 0] - pz[1, 0], pz[2, 1] - pz[1, 1]))
ang_bordes_foto = ang(p_f[0], p_f[3]) - ang(p_f[1], p_f[2])
print(f"ángulo entre bordes verticales de la puerta: foto {ang_bordes_foto:.2f}°, pared {ang_bordes:.2f}°")
TXT_F6 = dict(ab=0.899, ar=0.891, iz=2.047, de=2.044, ancho=0.895, alto=2.045, af=-1.54, ap=0.23)
for k, kk in (("abajo", "ab"), ("arriba", "ar"), ("izquierdo", "iz"), ("derecho", "de")):
    assert abs(lados[k] - TXT_F6[kk]) < 5e-4, (k, lados[k])
assert abs(ancho - TXT_F6["ancho"]) < 5e-4 and abs(alto - TXT_F6["alto"]) < 5e-4
assert abs(ang_bordes_foto - TXT_F6["af"]) < 0.006 and abs(ang_bordes - TXT_F6["ap"]) < 0.006
# medida ingenua: regla sobre la foto, escala de la ventana
esc_ab = 1.5 / np.linalg.norm(v_f[1] - v_f[0])
ing_ancho = np.linalg.norm(p_f[1] - p_f[0]) * esc_ab
esc_iz = 1.2 / np.linalg.norm(v_f[3] - v_f[0])
ing_alto = np.linalg.norm(p_f[3] - p_f[0]) * esc_iz
print(f"ingenuo: ventana abajo {np.linalg.norm(v_f[1] - v_f[0]):.1f} px, izquierda "
      f"{np.linalg.norm(v_f[3] - v_f[0]):.1f} px; puerta abajo {np.linalg.norm(p_f[1] - p_f[0]):.1f} px, "
      f"izquierda {np.linalg.norm(p_f[3] - p_f[0]):.1f} px")
print(f"ingenuo: ancho {ing_ancho:.2f} m, alto {ing_alto:.2f} m")
assert np.allclose(np.round([np.linalg.norm(v_f[1] - v_f[0]), np.linalg.norm(v_f[3] - v_f[0]),
                             np.linalg.norm(p_f[1] - p_f[0]), np.linalg.norm(p_f[3] - p_f[0])], 1),
                   [476.0, 404.5, 167.7, 520.0])
assert abs(ing_ancho - 0.53) < 0.005 and abs(ing_alto - 1.54) < 0.005

# ---------------------------------------------------------------- F7
print("\n=== F7  ejercicios ===")
Hinv = np.linalg.inv(H)
Hinv = Hinv / Hinv[2, 2]
mid_v = aplicar(Hinv, np.array([[0.75, 0.0]]))[0]
mid_foto = (v_f[0] + v_f[1]) / 2
print("punto medio del alféizar en la foto (imagen de (0,75; 0)) =", mid_v, " promedio de V1 y V2 =", mid_foto)
assert np.allclose(np.round(mid_v, 1), [357.5, 713.7]) and np.allclose(mid_foto, [330.5, 711.5])
# el mismo punto como conjugado armónico de F_h respecto de V1 y V2, con la coordenada c
a_, b_, d_ = v_f[0, 0], v_f[1, 0], Fh[0]
c_arm = a_ + (b_ - a_) * (d_ - a_) / (2 * (d_ - a_) - (b_ - a_))
print(f"conjugado armónico de F_h: c = {c_arm:.1f}; razón doble = {razon_doble(a_, b_, c_arm, d_):.6f}")
assert abs(c_arm - mid_v[0]) < 1e-6 and abs(c_arm - 357.5) < 0.05
print(f"ejercicio: b - a = {b_ - a_:.1f}, d - a = {d_ - a_:.1f}")
assert abs(b_ - a_ - 474.4) < 0.05 and abs(d_ - a_ - 2318.3) < 0.05

# ---------------------------------------------------------------- figuras
def poli(ax, P, **kw):
    ax.plot(*np.r_[P, P[:1]].T, **kw)


# Figura 1: la foto (izquierda) y la misma foto vista de lejos, con fugas y horizonte (derecha)
OFF = {"V1": (-22, -4), "V2": (6, 4), "V3": (6, -2), "V4": (-24, -2),
       "P1": (-20, 4), "P2": (6, 2), "P3": (6, -2), "P4": (-22, -8)}
fig, (ax, bx) = plt.subplots(1, 2, figsize=(10.5, 5.6), gridspec_kw={"width_ratios": [1.35, 1]})
for eje, lejos in ((ax, False), (bx, True)):
    eje.add_patch(plt.Rectangle((0, 0), 1600, 1200, fill=lejos, fc="#f4f2ee", ec=TINTA, lw=1.2))
    poli(eje, v_f, color=TEAL, lw=2)
    poli(eje, p_f, color=RUST, lw=2)
    for a_, b_ in ((v_f[0], v_f[1]), (v_f[3], v_f[2]), (p_f[0], p_f[1]), (p_f[3], p_f[2])):
        eje.plot([a_[0], Fh[0]], [a_[1], Fh[1]], color=GRIS, lw=0.7, ls="--")
    for a_, b_ in ((v_f[0], v_f[3]), (v_f[1], v_f[2]), (p_f[0], p_f[3]), (p_f[1], p_f[2])):
        eje.plot([a_[0], Fv[0]], [a_[1], Fv[1]], color=GRIS, lw=0.7, ls=":")
    eje.set_aspect("equal")
    eje.grid(alpha=0.2)
    eje.set_xlabel("columna c (px)")
for nom, q in zip(["V1", "V2", "V3", "V4", "P1", "P2", "P3", "P4"], FOTO):
    ax.annotate(nom, q, xytext=OFF[nom], textcoords="offset points", fontsize=8,
                color=TEAL if nom[0] == "V" else RUST)
ax.set_xlim(0, 1600); ax.set_ylim(1200, 0)
ax.set_ylabel("fila f (px, crece hacia abajo)")
ax.set_title("la foto, 1600 × 1200 px", fontsize=10)
cc = np.array([-1000, 3200])
bx.plot(cc, -(fila3[0] * cc + 1) / fila3[1], color=GOLD, lw=1.6)
for F, nom in ((Fh, r"$F_h$"), (Fv, r"$F_v$")):
    bx.plot(*F[:2], "x", color=TINTA, ms=9, mew=2)
    bx.annotate(nom, F[:2], xytext=(10, 4), textcoords="offset points")
mh = (Fh[:2] + Fv[:2]) / 2
bx.text(mh[0] + 150, mh[1], "horizonte", color=GOLD)
bx.set_xlim(-800, 3200); bx.set_ylim(1500, -6500)
bx.set_title("vista de lejos: puntos de fuga", fontsize=10)
fig.tight_layout()
fig.savefig(SALIDA / "c1_fachada_foto.png", dpi=150, metadata={"Software": None})
plt.close(fig)

# Figura 2: la pared enderezada
fig, ax = plt.subplots(figsize=(7.2, 4.4))
poli(ax, aplicar(H, v_f), color=TEAL, lw=2)
poli(ax, pz, color=RUST, lw=2)
ax.axhline(0, color=GRIS, lw=0.8, ls="--")
for x, nom in zip(xs, ["V1", "V2", "Q", "R"]):
    ax.plot(x, 0, "o", color=GOLD, ms=6, zorder=5)
    ax.annotate(nom, (x, 0), xytext=(3, -14), textcoords="offset points", fontsize=9)
ax.annotate(f"ancho {fmt(lados['abajo'], 3)} m", (pz[0, 0] + 0.05, pz[0, 1] + 0.05), fontsize=8, color=RUST)
ax.annotate(f"ancho {fmt(lados['arriba'], 3)} m", (pz[3, 0] + 0.02, pz[3, 1] + 0.07), fontsize=8, color=RUST)
ax.annotate(f"alto {fmt(lados['izquierdo'], 3)} m", (pz[0, 0] - 0.62, 0.45), fontsize=8, color=RUST)
ax.annotate(f"alto {fmt(lados['derecho'], 3)} m", (pz[1, 0] + 0.05, 0.45), fontsize=8, color=RUST)
ax.text(0.2, 0.55, "ventana\n1,50 × 1,20 m", color=TEAL, fontsize=9)
ax.text(-0.3, -0.25, f"razón doble (V1, V2; Q, R) = {fmt(rd_pared, 4)}", fontsize=8, color=TINTA)
ax.set_xlim(-0.5, 4.2); ax.set_ylim(-1.2, 1.5)
ax.set_aspect("equal")
ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(SALIDA / "c1_fachada_enderezada.png", dpi=150, metadata={"Software": None})
plt.close(fig)
print("\nfiguras escritas en", SALIDA)
