"""Números y figuras del capítulo «Geometría del elipsoide».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  P   Parámetros GRS80 (a = 6378137 m, 1/f = 298.257222101) y WGS84 (1/f = 298.257223563):
      f, b, e², e'², b/a; diferencia de b, M y N entre ambos en la latitud de Buenos Aires.
  T   Tabla de control en φ = 0°, 45°, -34.6°, 90°: M, N, x' = N cos φ, z = N(1-e²) sin φ, ψ, β,
      φ - ψ, R = √(MN); chequeo x'²/a² + z²/b² = 1.
  G   El gran normal: dónde corta la normal al eje polar y al plano del ecuador (φ = -34.6°).
  L   Latitudes: máximo de φ - ψ y de φ - β (latitud donde ocurre y valor en minutos).
  D   Derivación de M: comprobación numérica de dx'/dφ = -M sin φ, dz/dφ = M cos φ y de la
      curvatura de la elipse meridiana (diferencias finitas).
  K   Curvaturas en Buenos Aires: K = 1/(MN), H = (1/M + 1/N)/2, R = √(MN), media de los radios
      de las secciones normales en todos los acimutes (cuadratura) = √(MN).
  S   Arco de meridiano: coeficientes exactos (fracciones) de la serie A..E, valores en GRS80,
      comparación serie / quad: ecuador → 45°, ecuador → -34.6°, cuadrante.
  E1  Ejemplo «elipsoide de juguete» a = 5, b = 4: e², M y N en ecuador, 45° y polo; latitudes en 45°.
  A   Aplicación topográfica (Buenos Aires, φ = -34.6°, GRS80): M, N, 1" de latitud y de longitud,
      10 km de meridiano y de paralelo en segundos; base de 10 km hacia el N y hacia el E:
      distancia sobre el elipsoide y sobre la esfera de radio √(MN) y R1 = (2a+b)/3 con las mismas
      coordenadas; flecha (sagita) de la base en cada dirección. Control independiente con
      pyproj.Geod(ellps='GRS80').inv (control, no fuente).
  X1  Ejercicio: radio de la sección normal en acimut 45° en Buenos Aires (Euler).
  X2  Ejercicio: N - M en el ecuador (= a e²) y M, N en el polo.
  X3  Ejercicio: latitudes de un punto con z/x' dado (geocéntrica 30°).
  X4  Ejercicio: arco de paralelo de 1° en φ = -34.6° y en 60°; arco de 1° de meridiano en BA.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/elipsoide/:
  elip_meridiana.png    elipse meridiana exagerada (b/a = 0.6) con φ, ψ, β, la normal y su gran normal.
  elip_radios.png       M, N y √(MN) en función de φ (GRS80), con Buenos Aires marcado.
  elip_esfera_local.png esfera local: (izq.) circunferencias de radios M, N y √(MN) tangentes en P sobre
                        la elipse exagerada; (der.) radio de la sección normal en función del acimut en BA.
  elip_latitudes.png    φ - ψ y φ - β en minutos de arco, en función de φ (GRS80).

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap14_elipsoide.py
"""
from fractions import Fraction
from math import comb, factorial
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import brentq

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "elipsoide"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, TEALD = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#14505c"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "svg.hashsalt": "cap14"})
META = {"Software": None}
SEG = np.pi / 648000  # un segundo de arco en radianes


def elipsoide(a, inv_f):
    f = 1 / inv_f
    e2 = 2 * f - f * f
    b = a * (1 - f)
    return dict(a=a, f=f, b=b, e2=e2, ep2=e2 / (1 - e2))


def radios(phi, a, e2):
    w = np.sqrt(1 - e2 * np.sin(phi) ** 2)
    return a * (1 - e2) / w**3, a / w


def latitudes(phi, e2):
    psi = np.arctan2((1 - e2) * np.sin(phi), np.cos(phi))
    beta = np.arctan2(np.sqrt(1 - e2) * np.sin(phi), np.cos(phi))
    return psi, beta


def meridiana(phi, a, e2):
    """(x', z) del punto de latitud geodésica phi sobre la elipse meridiana."""
    _, N = radios(phi, a, e2)
    return N * np.cos(phi), N * (1 - e2) * np.sin(phi)


def arco_quad(p0, p1, a, e2):
    return quad(lambda t: radios(t, a, e2)[0], p0, p1, epsabs=1e-9, epsrel=1e-13, limit=200)[0]


def m(x, d=3):
    """Número con coma decimal y espacio fino de miles, para pegar en el texto."""
    s = f"{x:,.{d}f}".replace(",", " ").replace(".", ",")
    return s


GRS = elipsoide(6378137.0, 298.257222101)
WGS = elipsoide(6378137.0, 298.257223563)
a, e2, b = GRS["a"], GRS["e2"], GRS["b"]
PHI_BA = np.deg2rad(-34.6)

# ---------------------------------------------------------------- P
print("=== P  parámetros ===")
for nom, g in (("GRS80", GRS), ("WGS84", WGS)):
    print(f"{nom}: f = {g['f']:.12f}  b = {g['b']:.4f}  e2 = {g['e2']:.10f}  ep2 = {g['ep2']:.10f}  b/a = {g['b'] / g['a']:.10f}  sqrt(1-e2) = {np.sqrt(1 - g['e2']):.10f}")
print(f"a - b (GRS80) = {a - b:.3f} m")
print(f"b_GRS80 - b_WGS84 = {(GRS['b'] - WGS['b']) * 1000:.4f} mm")
Mg, Ng = radios(PHI_BA, a, GRS["e2"]); Mw, Nw = radios(PHI_BA, a, WGS["e2"])
print(f"en BA: M_GRS - M_WGS = {(Mg - Mw) * 1000:.4f} mm   N_GRS - N_WGS = {(Ng - Nw) * 1000:.4f} mm")
for ph in (0.0, 90.0):
    M1, N1 = radios(np.deg2rad(ph), a, GRS["e2"]); M2, N2 = radios(np.deg2rad(ph), a, WGS["e2"])
    print(f"   φ = {ph}: dM = {(M1 - M2) * 1000:.4f} mm  dN = {(N1 - N2) * 1000:.4f} mm")

# ---------------------------------------------------------------- T
print("\n=== T  tabla de control GRS80 ===")
for ph in (0.0, 45.0, -34.6, 90.0):
    p = np.deg2rad(ph)
    M, N = radios(p, a, e2)
    xp, z = meridiana(p, a, e2)
    psi, beta = latitudes(p, e2)
    chk = xp**2 / a**2 + z**2 / b**2
    print(f"φ = {ph:6.1f}: M = {m(M)}  N = {m(N)}  x' = {m(xp)}  z = {m(z)}  ψ = {np.rad2deg(psi):.6f}°  "
          f"β = {np.rad2deg(beta):.6f}°  φ-ψ = {(ph - np.rad2deg(psi)) * 60:.3f}'  φ-β = {(ph - np.rad2deg(beta)) * 60:.3f}'  "
          f"R = {m(np.sqrt(M * N))}  control-1 = {chk - 1:.1e}")

# ---------------------------------------------------------------- G
print("\n=== G  gran normal en φ = -34.6° ===")
M, N = radios(PHI_BA, a, e2)
xp, z = meridiana(PHI_BA, a, e2)
eje = z - N * np.sin(PHI_BA)          # corte con el eje polar: x' = 0
ecu = xp - N * (1 - e2) * np.cos(PHI_BA)  # corte con el ecuador: z = 0
print(f"corte con eje polar: z = {m(eje)} m  (= -N e2 sin φ = {m(-N * e2 * np.sin(PHI_BA))})")
print(f"corte con ecuador: x' = {m(ecu)} m  (= N e2 cos φ = {m(N * e2 * np.cos(PHI_BA))});  tramo P-ecuador = N(1-e2) = {m(N * (1 - e2))}")
print(f"distancia del corte con el eje al centro: {m(abs(eje))} m")

# ---------------------------------------------------------------- L
print("\n=== L  diferencias de latitud ===")
k = 1 - e2
phm = np.arctan(1 / np.sqrt(k)); dpsi = phm - np.arctan(k * np.tan(phm))
print(f"máx φ-ψ en φ = {np.rad2deg(phm):.4f}° : {np.rad2deg(dpsi) * 60:.3f}'  = {np.rad2deg(dpsi) * 3600:.1f}\"")
k2 = np.sqrt(1 - e2)
phb = np.arctan(1 / np.sqrt(k2)); dbet = phb - np.arctan(k2 * np.tan(phb))
print(f"máx φ-β en φ = {np.rad2deg(phb):.4f}° : {np.rad2deg(dbet) * 60:.3f}'")
psi_ba, beta_ba = latitudes(PHI_BA, e2)
print(f"BA: ψ = {np.rad2deg(psi_ba):.6f}°, β = {np.rad2deg(beta_ba):.6f}°, φ-ψ = {np.rad2deg(PHI_BA - psi_ba) * 60:.3f}', φ-β = {np.rad2deg(PHI_BA - beta_ba) * 60:.3f}'")

# ---------------------------------------------------------------- D
print("\n=== D  derivación de M ===")
hh = 1e-6
for ph in (0.0, -34.6, 60.0):
    p = np.deg2rad(ph)
    M, N = radios(p, a, e2)
    (x1, z1), (x2, z2) = meridiana(p - hh, a, e2), meridiana(p + hh, a, e2)
    dx, dz = (x2 - x1) / (2 * hh), (z2 - z1) / (2 * hh)
    print(f"φ = {ph}: dx'/dφ = {dx:.3f} vs -M sin φ = {-M * np.sin(p):.3f};  dz/dφ = {dz:.3f} vs M cos φ = {M * np.cos(p):.3f}")
# curvatura de la elipse x'^2/a^2 + z^2/b^2 = 1 en el punto, por la fórmula de la curva implícita
p = PHI_BA; xp, z = meridiana(p, a, e2)
Fx, Fz, Fxx, Fzz = 2 * xp / a**2, 2 * z / b**2, 2 / a**2, 2 / b**2
kap = abs(Fz**2 * Fxx + Fx**2 * Fzz) / (Fx**2 + Fz**2) ** 1.5
print(f"BA: 1/curvatura de la elipse (implícita) = {m(1 / kap)}  M = {m(radios(p, a, e2)[0])}")

# ---------------------------------------------------------------- K
print("\n=== K  curvaturas en Buenos Aires ===")
M, N = radios(PHI_BA, a, e2)
R = np.sqrt(M * N); R1 = (2 * a + b) / 3
print(f"M = {m(M)}  N = {m(N)}  N - M = {m(N - M)}  R = sqrt(MN) = {m(R)}  R1 = (2a+b)/3 = {m(R1)}")
print(f"K = 1/(MN) = {1 / (M * N):.6e} m^-2   H = (1/M+1/N)/2 = {(1 / M + 1 / N) / 2:.6e} m^-1   1/H = {m(2 * M * N / (M + N))}")
media = quad(lambda al: 1 / (np.cos(al) ** 2 / M + np.sin(al) ** 2 / N), 0, 2 * np.pi, epsabs=1e-9, epsrel=1e-14)[0] / (2 * np.pi)
print(f"media de ρ(α) en [0, 2π) = {m(media)}  (√(MN) = {m(R)}; diferencia {media - R:.2e} m)")
print(f"(M+N)/2 = {m((M + N) / 2)}")
print(f"N/M = {N / M:.8f}  1 + e'2 cos²φ = {1 + GRS['ep2'] * np.cos(PHI_BA) ** 2:.8f}")

# ---------------------------------------------------------------- S
print("\n=== S  arco de meridiano: serie ===")
NT = 5  # términos n = 0..4
# coeficiente de cos(2kφ) en (1 - e² sin² φ)^{-3/2} = Σ_n c_n e^{2n} sin^{2n} φ, con
# sin^{2n} = 4^{-n} [ C(2n,n) + 2 Σ_k (-1)^k C(2n, n-k) cos 2kφ ]
cn = [Fraction(factorial(2 * n + 1), (2**n * factorial(n)) ** 2) for n in range(NT)]
print("c_n =", [str(c) for c in cn])
coef = []
for kk in range(NT):
    terms = []
    for n in range(kk, NT):
        base = Fraction(comb(2 * n, n), 4**n) if kk == 0 else Fraction(2 * (-1) ** kk * comb(2 * n, n - kk), 4**n)
        terms.append(cn[n] * base)
    coef.append(terms)
    print(f"cos {2 * kk}φ: " + " + ".join(f"({t})e^{2 * (n + kk)}" for n, t in enumerate(terms)))
val = [sum(float(t) * e2 ** (n + kk) for n, t in enumerate(terms)) for kk, terms in enumerate(coef)]
nombres = "ABCDE"
for nm, v in zip(nombres, val):
    print(f"{nm} = {v:.10e}")


def arco_serie(phi, nterm=5):
    s = val[0] * phi
    for kk in range(1, nterm):
        s += val[kk] / (2 * kk) * np.sin(2 * kk * phi)
    return a * (1 - e2) * s


for ph in (45.0, -34.6, 90.0):
    p = np.deg2rad(ph)
    sq, ss = arco_quad(0, p, a, e2), arco_serie(p)
    print(f"ecuador → {ph}°: quad = {m(sq)}  serie = {m(ss)}  dif = {(ss - sq) * 1000:.2e} mm")
for nt in (1, 2, 3):
    print(f"   con {nt} término(s), ecuador → -34.6: serie - quad = {m(arco_serie(PHI_BA, nt) - arco_quad(0, PHI_BA, a, e2))} m")

# ---------------------------------------------------------------- E1
print("\n=== E1  elipsoide de juguete a = 5, b = 4 ===")
aj, bj = 5.0, 4.0
e2j = 1 - (bj / aj) ** 2
print(f"e2 = {e2j:.4f}  e'2 = {e2j / (1 - e2j):.4f}  f = {(aj - bj) / aj}")
for ph in (0.0, 45.0, 90.0):
    Mj, Nj = radios(np.deg2rad(ph), aj, e2j)
    xj, zj = meridiana(np.deg2rad(ph), aj, e2j)
    print(f"φ = {ph}: M = {Mj:.6f}  N = {Nj:.6f}  x' = {xj:.6f}  z = {zj:.6f}  √(MN) = {np.sqrt(Mj * Nj):.6f}")
psj, bej = latitudes(np.deg2rad(45.0), e2j)
print(f"45°: ψ = {np.rad2deg(psj):.4f}°  β = {np.rad2deg(bej):.4f}°  tanψ = {np.tan(psj):.4f} tanβ = {np.tan(bej):.4f}")
Nj45 = radios(np.deg2rad(45.0), aj, e2j)[1]
print(f"45°: W² = 1 - e2/2 = {1 - e2j / 2:.4f}, W = {np.sqrt(1 - e2j / 2):.6f}; gran normal corta el eje en z = {-Nj45 * e2j * np.sin(np.pi / 4):.6f}, el ecuador en x' = {Nj45 * e2j * np.cos(np.pi / 4):.6f}")

# ---------------------------------------------------------------- A
print("\n=== A  aplicación: Buenos Aires, φ = -34.6°, GRS80 ===")
M, N = radios(PHI_BA, a, e2)
r_par = N * np.cos(PHI_BA)
print(f"M = {m(M)}  N = {m(N)}  N cos φ = {m(r_par)}")
print(f"1\" de latitud = {m(M * SEG, 4)} m   1\" de longitud = {m(r_par * SEG, 4)} m")
dphi_lin = 10000 / M / SEG; dlam = 10000 / r_par / SEG
print(f"10 km de meridiano ≈ {dphi_lin:.4f}\" (10000/M)   10 km de paralelo = {dlam:.4f}\" = {dlam / 60:.4f}'")
print(f"esfera R1: 1\" de latitud = {m(R1 * SEG, 4)} m, 1\" de longitud = {m(R1 * np.cos(PHI_BA) * SEG, 4)} m")
print(f"esfera √(MN): 1\" de latitud = {m(R * SEG, 4)} m, 1\" de longitud = {m(R * np.cos(PHI_BA) * SEG, 4)} m")
print(f"cociente 1\"lon/1\"lat: elipsoide {r_par / M:.6f}, esfera cos φ = {np.cos(PHI_BA):.6f}")
M45, N45 = radios(np.pi / 4, a, e2)
print(f"unidad, GRS80 en 45°: 1' de φ = {m(M45 * np.pi / 10800, 2)} m, 1' de λ = {m(N45 * np.cos(np.pi / 4) * np.pi / 10800, 2)} m, N - M = {m(N45 - M45, 2)} (exacto {m(N45 - M45, 4)})")
# base N: de φ_BA hacia el norte, arco exacto de 10 km
phi2 = brentq(lambda t: arco_quad(PHI_BA, t, a, e2) - 10000.0, PHI_BA, PHI_BA + 0.01, xtol=1e-15)
dphi = (phi2 - PHI_BA) / SEG
print(f"base N: φ2 = {np.rad2deg(phi2):.9f}°, Δφ exacto = {dphi:.4f}\" (dif con 10000/M: {dphi - dphi_lin:.2e}\")")
s_par = r_par * np.deg2rad(dlam / 3600)  # = 10000 exacto por construcción
print(f"base E: Δλ = {dlam:.4f}\"; arco de paralelo = {s_par:.6f} m")
for nom, Rs in (("√(MN)", R), ("R1=(2a+b)/3", R1)):
    dN = Rs * (phi2 - PHI_BA)
    # gran círculo entre (φ, 0) y (φ, Δλ) en la esfera de radio Rs con las mismas coordenadas
    dl = np.deg2rad(dlam / 3600)
    sig = 2 * np.arcsin(np.cos(PHI_BA) * np.sin(dl / 2))
    dE = Rs * sig
    print(f"esfera {nom} = {m(Rs)}: N: {m(dN)} m (dif {m(dN - 10000)} m = {(dN / 10000 - 1) * 1e6:.0f} ppm);  "
          f"E: {m(dE)} m (dif {m(dE - 10000)} m = {(dE / 10000 - 1) * 1e6:.0f} ppm)")
print(f"razones: R/M - 1 = {(R / M - 1) * 1e6:.1f} ppm, R/N - 1 = {(R / N - 1) * 1e6:.1f} ppm, √(N/M) = {np.sqrt(N / M):.8f}")
print(f"R1/M - 1 = {(R1 / M - 1) * 1e6:.1f} ppm, R1/N - 1 = {(R1 / N - 1) * 1e6:.1f} ppm")
# flecha (sagita) de la base de 10 km: s²/(2ρ)
for nom, rho in (("M (N-S)", M), ("N (E-O)", N), ("√(MN)", R), ("R1", R1)):
    print(f"flecha de 10 km con radio {nom}: {10000**2 / (2 * rho) * 1000:.1f} mm   arco - cuerda: {10000**3 / (24 * rho**2) * 1000:.4f} mm")

# control independiente con pyproj
from pyproj import Geod  # noqa: E402

g = Geod(ellps="GRS80")
lat1 = -34.6
_, _, dn = g.inv(0.0, lat1, 0.0, np.rad2deg(phi2))
_, _, de = g.inv(0.0, lat1, dlam / 3600, lat1)
_, _, s1 = g.inv(0.0, lat1, 0.0, lat1 + 1 / 3600)
_, _, s1l = g.inv(0.0, lat1, 1 / 3600, lat1)
az12, _, _ = g.inv(0.0, lat1, dlam / 3600, lat1)
print(f"CONTROL pyproj: base N = {dn:.6f} m (fórmula: 10000; dif {(dn - 10000) * 1000:.2e} mm)")
print(f"CONTROL pyproj: base E (geodésica entre extremos del arco de paralelo) = {de:.6f} m; paralelo - geodésica = {(10000 - de) * 1000:.4f} mm; acimut inicial {az12:.6f}°")
print(f"CONTROL pyproj: 1\" lat = {s1:.6f} m (fórmula M·1\" = {M * SEG:.6f}; dif {(s1 - M * SEG) * 1000:.4f} mm)")
print(f"CONTROL pyproj: 1\" lon = {s1l:.6f} m (fórmula N cosφ·1\" = {r_par * SEG:.6f}; dif {(s1l - r_par * SEG) * 1000:.2e} mm)")
_, _, cuad = g.inv(0.0, 0.0, 0.0, 90.0)
print(f"CONTROL pyproj: cuadrante = {cuad:.4f} m vs quad {arco_quad(0, np.pi / 2, a, e2):.4f} m; dif {(cuad - arco_quad(0, np.pi / 2, a, e2)) * 1000:.2e} mm")
_, _, sba = g.inv(0.0, 0.0, 0.0, -34.6)
print(f"CONTROL pyproj: ecuador → -34.6 = {sba:.4f} m vs quad {arco_quad(0, PHI_BA, a, e2):.4f}")
TOL = 1e-3  # m (1 mm) para el control
assert abs(dn - 10000) < TOL and abs(s1 - M * SEG) < TOL and abs(de - 10000) < TOL
assert abs(cuad - arco_quad(0, np.pi / 2, a, e2)) < TOL

# ---------------------------------------------------------------- X1..X4
print("\n=== X1  sección normal en acimut 45° en BA ===")
rho45 = 1 / (np.cos(np.pi / 4) ** 2 / M + np.sin(np.pi / 4) ** 2 / N)
print(f"ρ(45°) = {m(rho45)}  = 2MN/(M+N); √(MN) = {m(R)}; dif = {m(R - rho45)}")
for al in (30.0, 60.0):
    r_ = 1 / (np.cos(np.deg2rad(al)) ** 2 / M + np.sin(np.deg2rad(al)) ** 2 / N)
    print(f"ρ({al}°) = {m(r_)}")

print("\n=== X2  ecuador y polo ===")
M0, N0 = radios(0.0, a, e2); M9, N9 = radios(np.pi / 2, a, e2)
print(f"ecuador: M = {m(M0)} = b²/a = {m(b**2 / a)}, N = {m(N0)}; N - M = {m(N0 - M0)} = a e2 = {m(a * e2)}")
print(f"polo: M = N = {m(M9)} = a²/b = {m(a**2 / b)}; polo - ecuador en M: {m(M9 - M0)}")
print(f"1° de meridiano: en el ecuador ≈ {m(M0 * np.pi / 180)} m, en el polo ≈ {m(M9 * np.pi / 180)} m")
print(f"1° de meridiano exacto: 0→1: {m(arco_quad(0, np.deg2rad(1), a, e2))}, 89→90: {m(arco_quad(np.deg2rad(89), np.pi / 2, a, e2))}")

print("\n=== X3  geocéntrica 30° ===")
psi3 = np.deg2rad(30.0)
phi3 = np.arctan(np.tan(psi3) / (1 - e2)); beta3 = np.arctan(np.sqrt(1 - e2) * np.tan(phi3))
print(f"ψ = 30°: φ = {np.rad2deg(phi3):.6f}° (φ-ψ = {(np.rad2deg(phi3) - 30) * 60:.3f}'), β = {np.rad2deg(beta3):.6f}° (β-ψ = {(np.rad2deg(beta3) - 30) * 60:.3f}')")
print(f"control tan β² = tanφ tanψ: {np.tan(beta3) ** 2:.10f} vs {np.tan(phi3) * np.tan(psi3):.10f}")

print("\n=== X4  arcos de 1° ===")
for ph in (-34.6, 60.0):
    Mx, Nx = radios(np.deg2rad(ph), a, e2)
    print(f"φ = {ph}: 1° de paralelo = {m(Nx * np.cos(np.deg2rad(ph)) * np.pi / 180)} m;  N = {m(Nx)}, cos φ = {np.cos(np.deg2rad(ph)):.6f}")
s1g = arco_quad(np.deg2rad(-35.1), np.deg2rad(-34.1), a, e2)
print(f"1° de meridiano centrado en -34.6 (de -35.1 a -34.1): {m(s1g)} m;  M(-34.6)·π/180 = {m(M * np.pi / 180)}")
_, _, s1gp = g.inv(0.0, -35.1, 0.0, -34.1)
print(f"CONTROL pyproj: {s1gp:.4f}")
# en una esfera de radio R1, 1° de paralelo en -34.6 y en 60
for ph in (-34.6, 60.0):
    print(f"esfera R1: 1° de paralelo en {ph} = {m(R1 * np.cos(np.deg2rad(ph)) * np.pi / 180)}")

# ================================================================= figuras
# --- 1. elipse meridiana exagerada
ae, be = 1.0, 0.6
e2e = 1 - be**2
ph = np.deg2rad(50.0)
Me, Ne = radios(ph, ae, e2e)
xp, zp = meridiana(ph, ae, e2e)
pse, bee = latitudes(ph, e2e)
t = np.linspace(0, 2 * np.pi, 400)
fig, ax = plt.subplots(figsize=(6.4, 6.0))
ax.plot(np.cos(t), np.sin(t), color=GRIS, lw=0.8, ls="--", label="circunferencia auxiliar de radio $a$")
ax.plot(np.cos(t), be * np.sin(t), color=TEAL, lw=2, label="elipse meridiana ($b/a=0{,}6$)")
ax.axhline(0, color=GRIS, lw=0.6); ax.axvline(0, color=GRIS, lw=0.6)
pe = np.array([0.0, -Ne * e2e * np.sin(ph)])
pq = np.array([Ne * e2e * np.cos(ph), 0.0])
P = np.array([xp, zp])
nvec = np.array([np.cos(ph), np.sin(ph)])
ax.plot([pe[0], P[0] + 0.25 * nvec[0]], [pe[1], P[1] + 0.25 * nvec[1]], color=RUST, lw=1.8, label="normal en $P$")
ax.plot([0, P[0]], [0, P[1]], color=TEALD, lw=1.3, label="recta al centro")
Q = np.array([np.cos(bee), np.sin(bee)])
ax.plot([0, Q[0]], [0, Q[1]], color=GOLD, lw=1.3, label="radio a $Q$ (misma $x'$)")
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=GOLD, lw=0.8, ls=":")
tg = np.array([-np.sin(ph), np.cos(ph)])
ax.plot([P[0] - 0.45 * tg[0], P[0] + 0.45 * tg[0]], [P[1] - 0.45 * tg[1], P[1] + 0.45 * tg[1]], color=GRIS, lw=0.9)
for (r0, ang, col, lab, c0) in ((0.16, ph, RUST, r"$\varphi$", pq), (0.30, pse, TEALD, r"$\psi$", (0, 0)), (0.45, bee, GOLD, r"$\beta$", (0, 0))):
    tt = np.linspace(0, ang, 40)
    ax.plot(c0[0] + r0 * np.cos(tt), c0[1] + r0 * np.sin(tt), color=col, lw=1.2)
    ax.text(c0[0] + (r0 + 0.04) * np.cos(ang / 2), c0[1] + (r0 + 0.04) * np.sin(ang / 2), lab, color=col, fontsize=11, va="center")
ax.plot(*P, "o", color="black", ms=5); ax.text(P[0] + 0.03, P[1] - 0.09, "$P$", fontsize=11)
ax.plot(*Q, "o", color=GOLD, ms=4); ax.text(Q[0] + 0.02, Q[1] + 0.03, "$Q$", fontsize=11)
ax.plot(*pe, "o", color=RUST, ms=4); ax.text(pe[0] + 0.04, pe[1] - 0.02, "corte con el eje polar", fontsize=8, color=RUST)
ax.plot(*pq, "o", color=RUST, ms=4)
mid = (P + pe) / 2
ax.text(mid[0] - 0.09 * np.sin(ph), mid[1] + 0.09 * np.cos(ph), r"$N$", color=RUST, fontsize=12, ha="center", va="center")
ax.text(1.02, -0.07, "$x'$", fontsize=10); ax.text(0.03, 1.02, "$z$", fontsize=10)
ax.set_aspect("equal"); ax.set_xlim(-0.3, 1.3); ax.set_ylim(-0.75, 1.1)
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=2, fontsize=7.5, frameon=False)
ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(SALIDA / "elip_meridiana.png", dpi=150, metadata=META); plt.close(fig)
print(f"\nfig1: φ = 50°, b/a = 0.6: ψ = {np.rad2deg(pse):.2f}°, β = {np.rad2deg(bee):.2f}°, N = {Ne:.3f} a, M = {Me:.3f} a, corte eje z = {pe[1]:.3f} a")

# --- 2. M, N, √(MN) en función de φ
phs = np.linspace(0, 90, 361)
Ms, Ns = radios(np.deg2rad(phs), a, e2)
fig, ax = plt.subplots(figsize=(6.4, 3.8))
ax.plot(phs, Ns / 1000, color=GOLD, lw=2, label=r"$N$ (primer vertical)")
ax.plot(phs, np.sqrt(Ms * Ns) / 1000, color=TEALD, lw=1.4, ls="--", label=r"$\sqrt{MN}$")
ax.plot(phs, Ms / 1000, color=TEAL, lw=2, label=r"$M$ (meridiano)")
ax.axhline(R1 / 1000, color=GRIS, lw=0.8, ls=":", label=r"$R_1=(2a+b)/3$")
ax.axvline(34.6, color=RUST, lw=0.8)
ax.text(35.2, 6338, r"Buenos Aires, $|\varphi|=34{,}6^\circ$", color=RUST, fontsize=8)
ax.set_xlabel(r"$|\varphi|$ (grados)"); ax.set_ylabel("radio (km)")
ax.set_xlim(0, 90); ax.grid(alpha=0.3)
ax.legend(loc="upper left", fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(SALIDA / "elip_radios.png", dpi=150, metadata=META); plt.close(fig)

# --- 3. esfera local
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.3), gridspec_kw={"width_ratios": [1.05, 1]})
ax = axs[0]
ph = np.deg2rad(50.0)
Me, Ne = radios(ph, ae, e2e); xp, zp = meridiana(ph, ae, e2e)
P = np.array([xp, zp]); nvec = np.array([np.cos(ph), np.sin(ph)])
ax.plot(np.cos(t), be * np.sin(t), color=TEAL, lw=2.2, label="elipse meridiana")
for rho, col, ls, lab in ((Me, TEAL, "-", r"radio $M$ (osculadora)"), (Ne, GOLD, "-", r"radio $N$ (centro en el eje)"),
                          (np.sqrt(Me * Ne), TEALD, "--", r"radio $\sqrt{MN}$")):
    c = P - rho * nvec
    ax.plot(c[0] + rho * np.cos(t), c[1] + rho * np.sin(t), color=col, lw=1, ls=ls, label=lab)
    ax.plot(*c, "o", color=col, ms=3)
ax.plot([P[0] - Ne * nvec[0], P[0] + 0.15 * nvec[0]], [P[1] - Ne * nvec[1], P[1] + 0.15 * nvec[1]], color=RUST, lw=1)
ax.plot(*P, "o", color="black", ms=5); ax.text(P[0] + 0.04, P[1] + 0.02, "$P$")
ax.axhline(0, color=GRIS, lw=0.5); ax.axvline(0, color=GRIS, lw=0.5)
ax.set_aspect("equal"); ax.set_xlim(-0.6, 1.3); ax.set_ylim(-0.75, 1.05)
ax.set_xticks([]); ax.set_yticks([])
ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.01), ncol=2, fontsize=7, frameon=False)
ax.set_title(r"plano meridiano, $b/a=0{,}6$, $\varphi=50^\circ$", fontsize=9)
ax = axs[1]
M, N = radios(PHI_BA, a, e2)
al = np.linspace(0, 180, 361)
rho = 1 / (np.cos(np.deg2rad(al)) ** 2 / M + np.sin(np.deg2rad(al)) ** 2 / N)
ax.plot(al, rho / 1000, color=RUST, lw=2, label=r"$\rho(\alpha)$ elipsoide (Euler)")
ax.axhline(R / 1000, color=TEALD, lw=1.2, ls="--", label=r"esfera $\sqrt{MN}$")
ax.axhline(R1 / 1000, color=GRIS, lw=1, ls=":", label=r"esfera $R_1$")
ax.set_xlabel(r"acimut $\alpha$ de la sección normal (grados)"); ax.set_ylabel("radio (km)")
ax.set_xlim(0, 180); ax.set_xticks([0, 45, 90, 135, 180]); ax.grid(alpha=0.3)
ax.legend(loc="lower center", fontsize=8, frameon=False)
ax.set_title(r"Buenos Aires, GRS80", fontsize=9)
fig.tight_layout(); fig.savefig(SALIDA / "elip_esfera_local.png", dpi=150, metadata=META); plt.close(fig)

# --- 4. diferencias de latitud
phs = np.linspace(0, 90, 361)
ps, bs = latitudes(np.deg2rad(phs), e2)
fig, ax = plt.subplots(figsize=(6.4, 3.4))
ax.plot(phs, (phs - np.rad2deg(ps)) * 60, color=TEALD, lw=2, label=r"$\varphi-\psi$ (geodésica $-$ geocéntrica)")
ax.plot(phs, (phs - np.rad2deg(bs)) * 60, color=GOLD, lw=2, label=r"$\varphi-\beta$ (geodésica $-$ reducida)")
ax.axvline(34.6, color=RUST, lw=0.8)
ax.set_xlabel(r"$|\varphi|$ (grados)"); ax.set_ylabel("minutos de arco")
ax.set_xlim(0, 90); ax.set_ylim(0, 15); ax.grid(alpha=0.3)
ax.legend(loc="upper right", fontsize=8, frameon=False)
fig.tight_layout(); fig.savefig(SALIDA / "elip_latitudes.png", dpi=150, metadata=META); plt.close(fig)
print("figuras en", SALIDA.relative_to(Path(__file__).resolve().parents[2]))
