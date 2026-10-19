"""Números y figuras del complemento C2 «Transformaciones conformes».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta y se
verifica con assert contra el valor que cita el .tex):
  E1  Ejemplo w = z² en z0 = 1 + i: f'(z0), escala k = |f'(z0)| y giro θ = arg f'(z0); imágenes
      de dos pasitos perpendiculares de largo h = 0,1 y h = 0,01 (ángulo y largo de las imágenes).
  E2  Ejemplo «foto estirada»: J = diag(1,5; 1). Imagen de las direcciones de 45° y 135° (ángulo
      entre ellas), deformación angular máxima de Tissot ω y la dirección donde ocurre.
  A   Aplicación: factor de escala de Gauss-Krüger en la faja 5 de POSGAR 2007 (EPSG:5347) con
      pyproj 3.8.0 / PROJ 9.8.1. Puntos sintéticos a la latitud φ = -34,6° y a ΔE = 0, 50, 100 y
      150 km al este del meridiano central (λ hallada con brentq sobre la proyección directa).
      Para cada uno: λ, escala meridional y paralela y convergencia de meridianos de
      pyproj.Proj.get_factors; k - 1 en cm/km; aproximación k ≈ 1 + ΔE²/(2R²) con
      R = R1 = (2a+b)/3 de GRS80 (el radio medio del capítulo del elipsoide) y con R = √(MN) en
      φ = -34,6°; Δλ sen φ como control de la convergencia. Medio ancho de la faja en esa
      latitud (ΔE del borde λ = -58,5°). Control de la serie de segundo orden
      k ≈ 1 + ½ Δλ² cos²φ · N/M en el borde, contra pyproj.
  X1  Ejercicio: e^z en z = ln 2 + iπ/6 (k = 2, θ = 30°) y Cauchy-Riemann numérico.
  X2  Ejercicio: foto estirada un 10 por ciento, diag(1,1; 1): ω y ángulo entre 45° y 135°.
  X3  Ejercicio: un lado de 1000 m a 100 km del meridiano central, largo en el plano.
  X4  Ejercicio: ΔE donde k - 1 = 1e-4 (10 cm/km), por la aproximación y por pyproj.
  X5  Ejercicio: convergencia de meridianos a 100 km, pyproj y Δλ sen φ.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/conformes/:
  conf_cuadricula.png  cuadrícula chica alrededor de 1 + i, su imagen por w = z² (conforme) y por
                       el estiramiento diag(1,5; 1) (no conforme), con una cruz de visuales a 90°
                       y un circulito en el centro.
  conf_k_DeltaE.png    k - 1 (cm/km) de pyproj en función de ΔE a φ = -34,6°, con la aproximación,
                       los cuatro puntos y el borde de la faja.
  conf_exacta_aprox.png diferencia (pyproj - aproximación) en mm/km, con R1 y con √(MN).

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/c2_conformes.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker
import pyproj
from scipy.optimize import brentq

SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "conformes"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, TEALD = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#14505c"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
META = {"Software": None}


def cerca(x, y, tol):
    return abs(x - y) <= tol


def ang(v):
    return np.degrees(np.arctan2(v[1], v[0]))


def angulo_entre(u, v):
    c = np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v))
    return np.degrees(np.arccos(np.clip(c, -1, 1)))


def omega_tissot(s1, s2):
    return np.degrees(2 * np.arcsin(abs(s1 - s2) / (s1 + s2)))


# ---------------------------------------------------------------- E1: w = z² en 1 + i
print("== E1  w = z^2 en z0 = 1 + i")
z0 = 1 + 1j
fp = 2 * z0
k_e1, th_e1 = abs(fp), np.degrees(np.angle(fp))
print(f"f'(z0) = {fp}  k = {k_e1:.4f}  theta = {th_e1:.1f} deg")
assert cerca(k_e1, 2.8284, 5e-5) and cerca(th_e1, 45.0, 1e-9)
e1 = {}
for h in (0.1, 0.01):
    d1 = (z0 + h) ** 2 - z0**2
    d2 = (z0 + 1j * h) ** 2 - z0**2
    a = angulo_entre([d1.real, d1.imag], [d2.real, d2.imag])
    e1[h] = (d1, d2, a, abs(d1) / h, abs(d2) / h)
    print(f"h = {h}: d1 = {d1:.4f}  d2 = {d2:.4f}  angulo = {a:.4f} deg  |d1|/h = {abs(d1)/h:.4f}")
assert cerca(e1[0.1][2], 92.79, 5e-3) and cerca(e1[0.01][2], 90.29, 5e-3)
assert cerca(e1[0.1][3], 2.9000, 5e-5) and cerca(e1[0.01][3], 2.8355, 5e-5)

# ---------------------------------------------------------------- E2: foto estirada
print("== E2  J = diag(1.5, 1)")
J2 = np.diag([1.5, 1.0])
u45, u135 = J2 @ [1, 1], J2 @ [-1, 1]
a45, a_e2 = ang(u45), angulo_entre(u45, u135)
om_e2 = omega_tissot(1.5, 1.0)
alfa_max = np.degrees(np.arctan(np.sqrt(1.5)))
print(f"45 -> {a45:.2f} deg; angulo entre imagenes = {a_e2:.2f}; omega = {om_e2:.2f}; "
      f"alfa del maximo = {alfa_max:.2f}; imagen = {np.degrees(np.arctan(1/np.sqrt(1.5))):.2f}")
assert cerca(a45, 33.69, 5e-3) and cerca(a_e2, 112.62, 5e-3) and cerca(om_e2, 23.07, 5e-3)
assert cerca(alfa_max, 50.77, 5e-3)

# ---------------------------------------------------------------- A: Gauss-Krüger faja 5
print("== A  Gauss-Kruger faja 5 (EPSG:5347)")
print("pyproj", pyproj.__version__, "PROJ", pyproj.proj_version_str)
assert pyproj.__version__ == "3.8.0" and pyproj.proj_version_str == "9.8.1"
crs = pyproj.CRS("EPSG:5347")
par = {p.name: p.value for p in crs.coordinate_operation.params}
LON0 = par["Longitude of natural origin"]
K0 = par["Scale factor at natural origin"]
FE = par["False easting"]
print(f"CRS: {crs.name} | elipsoide declarado: {crs.ellipsoid.name} | lon0 = {LON0} | k0 = {K0} | FE = {FE}")
assert LON0 == -60 and K0 == 1 and FE == 5500000
P = pyproj.Proj("EPSG:5347")
PHI = -34.6

# GRS80 y radios (los del capítulo del elipsoide)
a_g, inv_f = 6378137.0, 298.257222101
f_g = 1 / inv_f
b_g = a_g * (1 - f_g)
e2_g = 2 * f_g - f_g**2
R1 = (2 * a_g + b_g) / 3
W = np.sqrt(1 - e2_g * np.sin(np.radians(PHI)) ** 2)
M_g, N_g = a_g * (1 - e2_g) / W**3, a_g / W
RG = np.sqrt(M_g * N_g)
print(f"R1 = (2a+b)/3 = {R1:.3f} m   sqrt(MN) = {RG:.3f} m")
assert cerca(R1, 6371008.771, 1e-3) and cerca(RG, 6370503.553, 1e-3)


def este(lon):
    return P(lon, PHI)[0] - FE


def lon_de(dE):
    if dE == 0:
        return float(LON0)
    return brentq(lambda l: este(l) - dE, LON0, LON0 + 5, xtol=1e-13)


def factores(dE):
    lon = lon_de(dE)
    f = P.get_factors(lon, PHI)
    return lon, f.meridional_scale, f.parallel_scale, f.meridian_convergence


borde = este(-58.5)
print(f"medio ancho de la faja en phi = -34.6 (lambda = -58.5): {borde/1000:.1f} km")
assert cerca(borde / 1000, 137.6, 0.05)

# serie de segundo orden (En profundidad): k ≈ 1 + ½ Δλ² cos²φ · N/M, en el borde (Δλ = 1,5°)
fb = P.get_factors(-58.5, PHI)
dlb = np.radians(1.5)
s_sin = 0.5 * dlb**2 * np.cos(np.radians(PHI)) ** 2
s_con = s_sin * N_g / M_g
print(f"borde: pyproj k-1 = {fb.meridional_scale-1:.4e}  1/2 dl^2 cos^2 = {s_sin:.4e}  "
      f"x N/M = {s_con:.4e}  N/M = {N_g/M_g:.5f}  E borde = {borde:.1f} m  E^2/(2MN) = {borde**2/(2*M_g*N_g):.4e}")
assert cerca((fb.meridional_scale - 1) * 1e4, 2.333, 5e-4) and cerca(s_sin * 1e4, 2.322, 5e-4)
assert cerca(s_con * 1e4, 2.333, 5e-4) and cerca(N_g / M_g, 1.00457, 5e-6)

filas = {}
for dkm in (0, 50, 100, 150):
    dE = dkm * 1000.0
    lon, h, k, conv = factores(dE)
    ka = 1 + dE**2 / (2 * R1**2)
    kg = 1 + dE**2 / (2 * RG**2)
    dl = lon - LON0
    conv_a = dl * np.sin(np.radians(PHI))
    filas[dkm] = dict(lon=lon, h=h, k=k, conv=conv, ka=ka, kg=kg, conv_a=conv_a)
    print(f"dE = {dkm:3d} km  lon = {lon:.4f}  h = {h:.8f}  k = {k:.8f}  k-1 = {(k-1)*1e5:.2f} cm/km  "
          f"aprox R1 = {(ka-1)*1e5:.2f} cm/km  dif = {(k-ka)*1e6:+.3f} mm/km  "
          f"aprox sqrt(MN) dif = {(k-kg)*1e6:+.3f} mm/km  conv = {conv:.4f}  dl sin phi = {conv_a:.4f}")
    assert cerca(h, k, 1e-9)  # conforme: las dos escalas coinciden (error numérico de get_factors)

# valores citados en el .tex (tabla de la aplicación)
cita = {0: (-60.0, 0.00, 0.00, 0.0), 50: (-59.4549, 3.08, 3.08, -0.3095),
        100: (-58.9099, 12.32, 12.32, -0.6191), 150: (-58.3648, 27.72, 27.72, -0.9287)}
for dkm, (lon_c, kc, kac, conv_c) in cita.items():
    r = filas[dkm]
    assert cerca(r["lon"], lon_c, 5e-5), (dkm, r["lon"])
    assert cerca((r["k"] - 1) * 1e5, kc, 5e-3), (dkm, (r["k"] - 1) * 1e5)
    assert cerca((r["ka"] - 1) * 1e5, kac, 5e-3), (dkm, (r["ka"] - 1) * 1e5)
    assert cerca(r["conv"], conv_c, 5e-5), (dkm, r["conv"])
# la aproximación con R1 y con sqrt(MN) difieren de pyproj en menos de 0,1 mm/km dentro de 150 km
dif_R1 = max(abs(filas[d]["k"] - filas[d]["ka"]) for d in filas) * 1e6
dif_RG = max(abs(filas[d]["k"] - filas[d]["kg"]) for d in filas) * 1e6
print(f"max |pyproj - aprox|: R1 {dif_R1:.3f} mm/km, sqrt(MN) {dif_RG:.3f} mm/km")
assert dif_R1 < 0.1 and dif_RG < 0.02
# área: factor de área = k² (conforme)
area150 = (filas[150]["k"] ** 2 - 1) * 1e4
print(f"a 150 km, una hectarea en el plano: k^2 = 1 + {area150:.2f} m2 por ha")
assert cerca(area150, 5.55, 5e-3)

# ---------------------------------------------------------------- Ejercicios
print("== X1  e^z en ln2 + i pi/6")
zx = np.log(2) + 1j * np.pi / 6
fx = np.exp(zx)
assert cerca(abs(fx), 2.0, 1e-12) and cerca(np.degrees(np.angle(fx)), 30.0, 1e-9)
u, v, hh = zx.real, zx.imag, 1e-6
X = lambda u, v: np.exp(u) * np.cos(v)
Y = lambda u, v: np.exp(u) * np.sin(v)
xu = (X(u + hh, v) - X(u - hh, v)) / (2 * hh); xv = (X(u, v + hh) - X(u, v - hh)) / (2 * hh)
yu = (Y(u + hh, v) - Y(u - hh, v)) / (2 * hh); yv = (Y(u, v + hh) - Y(u, v - hh)) / (2 * hh)
print(f"x_u = {xu:.6f} y_v = {yv:.6f}  x_v = {xv:.6f} -y_u = {-yu:.6f}")
assert cerca(xu, yv, 1e-8) and cerca(xv, -yu, 1e-8) and cerca(xu, np.sqrt(3), 1e-8) and cerca(yu, 1.0, 1e-8)

print("== X2  diag(1.1, 1)")
om_x2 = omega_tissot(1.1, 1.0)
a_x2 = angulo_entre([1.1, 1], [-1.1, 1])
print(f"omega = {om_x2:.2f} deg  angulo 45/135 -> {a_x2:.2f} deg")
assert cerca(om_x2, 5.46, 5e-3) and cerca(a_x2, 95.45, 5e-3)

print("== X3  lado de 1000 m a 100 km")
d3 = (filas[100]["k"] - 1) * 1000
print(f"1000 m -> 1000 + {d3*100:.1f} cm")
assert cerca(d3 * 100, 12.3, 0.05)

print("== X4  dE con k-1 = 1e-4")
dE4a = R1 * np.sqrt(2e-4)
dE4 = brentq(lambda d: factores(d)[2] - 1 - 1e-4, 1e4, 1.5e5, xtol=1e-3)
print(f"aprox {dE4a/1000:.2f} km  pyproj {dE4/1000:.2f} km")
assert cerca(dE4a / 1000, 90.10, 5e-3) and cerca(dE4 / 1000, 90.09, 5e-3)

print("== X5  convergencia a 100 km")
r = filas[100]
print(f"pyproj {r['conv']:.4f} deg  dl sin phi {r['conv_a']:.4f} deg  dl = {r['lon']-LON0:.4f}")
print(f"pyproj {r['conv']*3600:.1f}''  dl sin phi {r['conv_a']*3600:.1f}''")
assert cerca(r["lon"] - LON0, 1.0901, 5e-5) and cerca(r["conv"], -0.6191, 5e-5) and cerca(r["conv_a"], -0.6190, 5e-5)
assert cerca(r["conv"] * 3600, -2228.7, 0.05) and cerca(r["conv_a"] * 3600, -2228.5, 0.05)

# ---------------------------------------------------------------- Figuras
# F1: cuadrícula, z² y estiramiento
def malla(n=9, lado=0.8, c=z0, m=60):
    s = np.linspace(-lado / 2, lado / 2, n)
    t = np.linspace(-lado / 2, lado / 2, m)
    lineas = [c + si + 1j * t for si in s] + [c + t + 1j * si for si in s]
    return lineas


def estira(z):
    return 1.5 * (z - z0).real + 1j * (z - z0).imag + z0


transf = [("plano original", lambda z: z, "terreno"),
          ("w = z²: conforme", lambda z: z**2, "conforme"),
          ("estirar 1,5 en horizontal: no conforme", estira, "estirada")]
fig, axs = plt.subplots(1, 3, figsize=(11, 4.3))
r_c, l_v = 0.12, 0.3
for ax, (tit, T, tipo) in zip(axs, transf):
    for ln in malla():
        w = T(ln)
        ax.plot(w.real, w.imag, color=GRIS, lw=0.7)
    cen = T(z0)
    th = np.linspace(0, 2 * np.pi, 200)
    circ = T(z0 + r_c * np.exp(1j * th)) if tipo != "conforme" else cen + fp * r_c * np.exp(1j * th)
    ax.fill(circ.real, circ.imag, color=GOLD, alpha=0.35, lw=0)
    ax.plot(circ.real, circ.imag, color=GOLD, lw=1.2)
    for dirc, col in ((np.exp(1j * np.pi / 4), TEAL), (np.exp(3j * np.pi / 4), RUST)):
        if tipo == "conforme":
            w = cen + fp * l_v * dirc  # imagen por la jacobiana en z0 (la lupa)
        else:
            w = T(z0 + l_v * dirc)
        ax.annotate("", xy=(w.real, w.imag), xytext=(cen.real, cen.imag),
                    arrowprops=dict(arrowstyle="-|>", color=col, lw=1.8))
    if tipo == "terreno":
        a_t = 90.0
    elif tipo == "conforme":
        a_t = angulo_entre([(fp * np.exp(1j * np.pi / 4)).real, (fp * np.exp(1j * np.pi / 4)).imag],
                           [(fp * np.exp(3j * np.pi / 4)).real, (fp * np.exp(3j * np.pi / 4)).imag])
    else:
        a_t = a_e2
    ax.set_title(f"{tit}\nángulo entre flechas: {a_t:.1f}°".replace(".", ","), fontsize=9.5)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.subplots_adjust(top=0.86); fig.savefig(SALIDA / "conf_cuadricula.png", dpi=150, metadata=META); plt.close(fig)

# F2: k - 1 en función de ΔE
dEs = np.linspace(0, 200e3, 81)
kex = np.array([factores(d)[2] for d in dEs])
kap = 1 + dEs**2 / (2 * R1**2)
kgg = 1 + dEs**2 / (2 * RG**2)
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(dEs / 1000, (kex - 1) * 1e5, color=TEAL, lw=2.2, label="pyproj (EPSG:5347), exacto")
ax.plot(dEs / 1000, (kap - 1) * 1e5, color=RUST, lw=1.2, ls="--", label=r"$1+\Delta E^2/(2R_1^2)$")
for dkm in (0, 50, 100, 150):
    ax.plot(dkm, (filas[dkm]["k"] - 1) * 1e5, "o", color=TEALD, ms=6)
    ax.annotate(f"{abs(filas[dkm]['k'] - 1) * 1e5:.2f}".replace(".", ","), (dkm, (filas[dkm]["k"] - 1) * 1e5),
                textcoords="offset points", xytext=(-30, 6), fontsize=9)
ax.axvline(borde / 1000, color=GOLD, lw=1.4, ls=":")
ax.text(borde / 1000 + 2, 2, "borde de la faja\n" + r"($\lambda=-58{,}5^\circ$)", color="#7a6418", fontsize=9)
ax.set_xlabel(r"distancia al meridiano central $\Delta E$ (km)")
ax.set_ylabel(r"$k-1$ (cm por km)")
ax.set_title(r"Factor de escala en la faja 5, $\varphi=-34{,}6^\circ$")
ax.legend(loc="upper left", frameon=False); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(SALIDA / "conf_k_DeltaE.png", dpi=150, metadata=META); plt.close(fig)

# F3: diferencia exacta - aproximada
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(dEs / 1000, (kex - kap) * 1e6, color=RUST, lw=1.8, label=r"con $R_1=(2a+b)/3$")
ax.plot(dEs / 1000, (kex - kgg) * 1e6, color=TEAL, lw=1.8, label=r"con $R=\sqrt{MN}$ en $-34{,}6^\circ$")
ax.axhline(0, color=GRIS, lw=0.8)
ax.axvline(borde / 1000, color=GOLD, lw=1.4, ls=":")
ax.set_xlabel(r"$\Delta E$ (km)")
ax.set_ylabel("exacto − aproximado (mm por km)")
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda y, _: f"{y:.2f}".replace(".", ",")))
ax.set_title("Cuánto se equivoca la aproximación")
ax.legend(loc="upper left", frameon=False); ax.grid(alpha=0.3)
fig.tight_layout(); fig.savefig(SALIDA / "conf_exacta_aprox.png", dpi=150, metadata=META); plt.close(fig)
print("figuras en", SALIDA)
