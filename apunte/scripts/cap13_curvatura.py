"""Números y figuras del capítulo «Curvatura como forma cuadrática».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «Paraboloide z = x²/2 + y²/8»: en el origen II = hessiana, curvaturas 1 y 1/4;
      en el punto (1, 2): E, F, G, L, M, N, curvaturas principales, direcciones, K, H y la
      curvatura normal en la dirección del eje x.
  E2  Ejemplo «Silla z = (x² − y²)/4»: curvaturas ±1/2, direcciones asintóticas.
  E3  Esfera de radio R y cilindro de radio R: L, M, N por diferencias finitas (control) y
      comparación con la curvatura de la Tierra.
  MS  Meusnier sobre el paraboloide: sección oblicua por el eje x inclinada φ = 40° respecto
      de la normal; curvatura numérica de la curva de corte contra κ_n / cos φ.
  EL  Elipsoide GRS80 (el de los capítulos 0 y 14) en la latitud del recorte: radios M y N, curvaturas 1/M y 1/N, K.
  A   Aplicación topográfica: DEM Copernicus GLO-30 (recorte 512 × 512 de la precordillera);
      paso de grilla en metros desde la latitud; cuadrática local por mínimos cuadrados en
      ventanas de 7 × 7 celdas alrededor de una loma, una vaguada y una silla; hessiana,
      I, II, curvaturas principales en 1/km, radios, acimutes; verificación de Euler a lo
      largo de la máxima pendiente (fórmula y perfil del DEM interpolado); Meusnier a lo largo
      de la curva de nivel; sensibilidad a la ventana (5 × 5, 7 × 7, 9 × 9).
  X1  Ejercicio 1: z = x² + xy + y² en el origen.
  X2  Ejercicio 2: silla z = xy.
  X3  Ejercicio 3: hélice sobre un cilindro de radio 3 y paso 2π·4 (Euler + Meusnier).
  X4  Ejercicio 4: I = [[2,1],[1,1]], II = [[3,1],[1,1]]: autovalores de I⁻¹II contra los de II.
  X5  Ejercicio 5: cuadrática ajustada en un punto de pendiente nula, d = −4, e = 3, f = 1
      (en 10⁻³ 1/m): clasificación y acimutes.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/curvatura/:
  curv_secciones.png   paraboloide con plano tangente, normal y las dos secciones principales;
                       a la derecha, los dos perfiles con sus círculos osculadores.
  curv_euler.png       κ_n(θ) por Euler (paraboloide, silla, cilindro) e indicatriz de Dupin.
  curv_meusnier.png    corte perpendicular a la tangente: osculadores normal y oblicuo.
  curv_dem.png         relieve sombreado con curvas de nivel y los tres puntos; mapa de la
                       curvatura media H (1/km) con ventana de 7 × 7.

Dato: datos/dem_copernicus/dem_precordillera_512.npy (no se modifica). Lo generó
datos/dem_copernicus/crop_dem.py a partir del tile Copernicus_DSM_COG_10_S33_00_W069_00_DEM.tif
(filas 512–1024, columnas 0–512; fila 0 del tile = latitud −32°, columna 0 = longitud −69°):
  cd datos/dem_copernicus && uv run --with rasterio python crop_dem.py
Los centros de celda están en segundos enteros: lat = −32° − (512 + fila)″, lon = −69° + columna″.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap13_curvatura.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource, TwoSlopeNorm
from numpy.lib.stride_tricks import sliding_window_view

np.set_printoptions(precision=5, suppress=True)
RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "apunte" / "figuras" / "curvatura"
SALIDA.mkdir(parents=True, exist_ok=True)
DEM = RAIZ / "datos" / "dem_copernicus" / "dem_precordillera_512.npy"
TEAL, RUST, GOLD, GRIS, VIOLETA = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#6a4c93"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "svg.hashsalt": "cap13"})
META = {"Software": None}


def guardar(fig, nombre):
    fig.savefig(SALIDA / nombre, dpi=150, metadata=META)
    plt.close(fig)


def formas_grafico(hx, hy, hxx, hxy, hyy):
    """I y II de un gráfico z = h(x, y) con la normal hacia arriba."""
    W = np.sqrt(1 + hx**2 + hy**2)
    I = np.array([[1 + hx**2, hx * hy], [hx * hy, 1 + hy**2]])
    II = np.array([[hxx, hxy], [hxy, hyy]]) / W
    return I, II, W


def principales(I, II):
    """Autovalores (κ1 ≥ κ2) y autovectores de I⁻¹II, normalizados con I(d) = 1.

    Se reduce a una simétrica por congruencia: I = C Cᵀ (Cholesky), A = C⁻¹ II C⁻ᵀ.
    """
    C = np.linalg.cholesky(I)
    Ci = np.linalg.inv(C)
    lam, Wv = np.linalg.eigh(Ci @ II @ Ci.T)
    orden = np.argsort(lam)[::-1]
    lam, Wv = lam[orden], Wv[:, orden]
    D = Ci.T @ Wv
    for k in range(2):  # signo: primera componente no negativa (o la segunda, si la primera es 0)
        j = 0 if abs(D[0, k]) > 1e-12 else 1
        D[:, k] *= np.sign(D[j, k])
    return lam, D


def kn(I, II, d):
    return (d @ II @ d) / (d @ I @ d)


def acimut(d):
    """Acimut (desde el norte, horario) de la dirección horizontal (dE, dN), en [0, 180)."""
    return np.rad2deg(np.arctan2(d[0], d[1])) % 180.0


# ---------------------------------------------------------------- E1
print("=== E1  paraboloide z = x²/2 + y²/8 ===")
a1, b1 = 0.5, 0.125
I0, II0, _ = formas_grafico(0, 0, 2 * a1, 0, 2 * b1)
lam0, _ = principales(I0, II0)
print("origen: I =", I0.tolist(), " II =", II0.tolist(), " κ1, κ2 =", lam0, " radios =", 1 / lam0)
p = np.array([1.0, 2.0])
hx, hy = 2 * a1 * p[0], 2 * b1 * p[1]
I1, II1, W1 = formas_grafico(hx, hy, 2 * a1, 0, 2 * b1)
lam1, D1 = principales(I1, II1)
print("punto (1,2): z =", a1 * p[0] ** 2 + b1 * p[1] ** 2, " h_x, h_y =", hx, hy, " W =", W1)
print("  E, F, G =", I1[0, 0], I1[0, 1], I1[1, 1], " det I =", np.linalg.det(I1))
print("  L, M, N =", II1[0, 0], II1[0, 1], II1[1, 1])
print("  I^-1 II =", np.linalg.solve(I1, II1))
print("  κ1, κ2 =", lam1, " radios =", 1 / lam1)
print("  direcciones (columnas, I(d)=1) =\n", D1)
print("  I-ortogonalidad d1ᵀ I d2 =", D1[:, 0] @ I1 @ D1[:, 1], " producto euclídeo =", D1[:, 0] @ D1[:, 1])
print("  K =", lam1.prod(), " = det II / det I =", np.linalg.det(II1) / np.linalg.det(I1), " H =", lam1.mean())
print("  κ_n eje x =", kn(I1, II1, np.array([1.0, 0])), " eje y =", kn(I1, II1, np.array([0, 1.0])))
print("  autovalores de la hessiana (1 y 0,25) ≠ κ; autovalores de II sola =", np.linalg.eigvalsh(II1)[::-1])
S1 = np.linalg.solve(I1, II1)
print("  27·S =", (27 * S1).round(6).tolist(), " traza·27 =", 27 * np.trace(S1), " det·729 =", 729 * np.linalg.det(S1), " det II =", np.linalg.det(II1))
print("  (7±√13)/27 =", (7 + np.sqrt(13)) / 27, (7 - np.sqrt(13)) / 27, " d1 = (1, 3−√13) =", 3 - np.sqrt(13), " d2 = (1, 3+√13) =", 3 + np.sqrt(13),
      " d1·d2 =", 1 + (3 - np.sqrt(13)) * (3 + np.sqrt(13)), " d1ᵀId2 =", np.array([1, 3 - np.sqrt(13)]) @ I1 @ np.array([1, 3 + np.sqrt(13)]))

# ---------------------------------------------------------------- E2
print("\n=== E2  silla z = (x² − y²)/4 ===")
Is, IIs, _ = formas_grafico(0, 0, 0.5, 0, -0.5)
lams, _ = principales(Is, IIs)
th_as = np.rad2deg(np.arctan(np.sqrt(-lams[0] / lams[1])))
print("κ1, κ2 =", lams, " K =", lams.prod(), " H =", lams.mean(), " θ asintótica =", th_as)
for t in (0, 30, 45, 60, 90):
    tt = np.deg2rad(t)
    print(f"  θ = {t}°: κ_n = {lams[0] * np.cos(tt)**2 + lams[1] * np.sin(tt)**2:.4f}")

# ---------------------------------------------------------------- E3
print("\n=== E3  esfera y cilindro (diferencias finitas, normal exterior) ===")


def formas_param(r, u, v, h=1e-4):
    ru = (r(u + h, v) - r(u - h, v)) / (2 * h)
    rv = (r(u, v + h) - r(u, v - h)) / (2 * h)
    ruu = (r(u + h, v) - 2 * r(u, v) + r(u - h, v)) / h**2
    rvv = (r(u, v + h) - 2 * r(u, v) + r(u, v - h)) / h**2
    ruv = (r(u + h, v + h) - r(u + h, v - h) - r(u - h, v + h) + r(u - h, v - h)) / (4 * h * h)
    n = np.cross(ru, rv); n /= np.linalg.norm(n)
    I = np.array([[ru @ ru, ru @ rv], [ru @ rv, rv @ rv]])
    II = np.array([[ruu @ n, ruv @ n], [ruv @ n, rvv @ n]])
    return I, II, n


R = 2.0
esf = lambda lam_, phi: R * np.array([np.cos(phi) * np.cos(lam_), np.cos(phi) * np.sin(lam_), np.sin(phi)])
Ie, IIe, ne = formas_param(esf, 0.3, 0.5)
print("esfera R=2 en (λ, φ) = (0.3, 0.5): n·r/R =", ne @ esf(0.3, 0.5) / R)
print("  I =", Ie.round(5).tolist(), " II =", IIe.round(4).tolist(), " κ =", principales(Ie, IIe)[0])
cil = lambda th, z: np.array([R * np.cos(th), R * np.sin(th), z])
Ic, IIc, nc = formas_param(cil, 0.3, 0.5)
print("cilindro R=2: I =", Ic.round(5).tolist(), " II =", IIc.round(4).tolist(), " κ =", principales(Ic, IIc)[0])
RT = 6371.0
print(f"Tierra como esfera R = {RT} km: κ = 1/R = {1 / RT:.6f} 1/km")

# ---------------------------------------------------------------- MS
print("\n=== MS  Meusnier sobre el paraboloide ===")
phi = np.deg2rad(40.0)
m_dir = np.array([0.0, np.sin(phi), np.cos(phi)])  # el plano contiene t = (1,0,0) y m_dir


def q_de_s(s):
    # punto s·t + q·m sobre z = a x² + b y²:  q cos φ = a s² + b (q sin φ)²  (raíz chica)
    A, B, Cc = b1 * np.sin(phi) ** 2, -np.cos(phi), a1 * s**2
    return (-B - np.sqrt(B * B - 4 * A * Cc)) / (2 * A)


hs = 1e-3
qpp = (q_de_s(hs) - 2 * q_de_s(0.0) + q_de_s(-hs)) / hs**2
print("φ =", np.rad2deg(phi), " curvatura numérica del corte =", qpp, " κ_n/cos φ =", 2 * a1 / np.cos(phi),
      " radio =", 1 / qpp, " = R_n cos φ =", np.cos(phi) / (2 * a1))

# ---------------------------------------------------------------- EL + paso de grilla
print("\n=== EL  elipsoide GRS80 y paso de grilla ===")
A_GRS, F_GRS = 6378137.0, 1 / 298.257222101
E2_GRS = 2 * F_GRS - F_GRS**2
ARCSEC = np.deg2rad(1 / 3600)


def radios(lat_deg):
    s = np.sin(np.deg2rad(lat_deg))
    w = np.sqrt(1 - E2_GRS * s * s)
    return A_GRS * (1 - E2_GRS) / w**3, A_GRS / w


lat_c = -32.0 - (512 + 256) / 3600
Mc, Nc = radios(lat_c)
print(f"latitud centro del recorte = {lat_c:.4f}°  M = {Mc:.1f} m  N = {Nc:.1f} m")
print(f"  1/M = {1e3 / Mc:.7f} 1/km  1/N = {1e3 / Nc:.7f} 1/km  K = 1/(MN) = {1e6 / (Mc * Nc):.4e} 1/km²  sqrt(MN) = {np.sqrt(Mc * Nc) / 1e3:.1f} km")
print(f"  paso N-S = M·1″ = {Mc * ARCSEC:.2f} m   paso E-O = N cos φ·1″ = {Nc * np.cos(np.deg2rad(lat_c)) * ARCSEC:.2f} m")
print(f"  paralelo: radio N cos φ = {Nc * np.cos(np.deg2rad(lat_c)) / 1e3:.1f} km")

# ---------------------------------------------------------------- A: DEM
print("\n=== A  DEM Copernicus GLO-30, recorte 512 ===")
Z = np.load(DEM).astype(float)
print("forma", Z.shape, f" z mín {Z.min():.0f} m, máx {Z.max():.0f} m, media {Z.mean():.0f} m")


def paso(fila):
    lat = -32.0 - (512 + fila) / 3600
    M_, N_ = radios(lat)
    return N_ * np.cos(np.deg2rad(lat)) * ARCSEC, M_ * ARCSEC, lat


def diseño(k, dx, dy):
    xs = np.arange(-k, k + 1) * dx
    ys = -np.arange(-k, k + 1) * dy  # la fila crece hacia el sur
    X, Y = np.meshgrid(xs, ys)
    x, y = X.ravel(), Y.ravel()
    return np.column_stack([np.ones_like(x), x, y, x * x, x * y, y * y])


def ajuste(fila, col, k=3):
    dx, dy, lat = paso(fila)
    A = diseño(k, dx, dy)
    z = Z[fila - k:fila + k + 1, col - k:col + k + 1].ravel()
    coef = np.linalg.solve(A.T @ A, A.T @ z)  # ecuaciones normales
    res = z - A @ coef
    return coef, np.sqrt(res @ res / (z.size - 6)), dx, dy, lat


def bilineal(fi, co):
    f0, c0 = int(np.floor(fi)), int(np.floor(co))
    tf, tc = fi - f0, co - c0
    return ((1 - tf) * (1 - tc) * Z[f0, c0] + (1 - tf) * tc * Z[f0, c0 + 1]
            + tf * (1 - tc) * Z[f0 + 1, c0] + tf * tc * Z[f0 + 1, c0 + 1])


PUNTOS = [("loma", 48, 466), ("vaguada", 420, 252), ("silla", 31, 118)]
resultados = {}
for nombre, fi, co in PUNTOS:
    coef, rms, dx, dy, lat = ajuste(fi, co)
    a, b, c, d, e, f = coef
    H = np.array([[2 * d, e], [e, 2 * f]])
    I, II, W = formas_grafico(b, c, 2 * d, e, 2 * f)
    lam, D = principales(I, II)
    lamH, VH = np.linalg.eigh(H); lamH = lamH[::-1]
    g = np.hypot(b, c)
    print(f"\n--- {nombre}: fila {fi}, col {co}  lat {lat:.4f}°  lon {-69 + co / 3600:.4f}°  z celda {Z[fi, co]:.1f} m")
    print(f"  dx = {dx:.2f} m, dy = {dy:.2f} m; ventana 7×7 = {6 * dx:.0f} m × {6 * dy:.0f} m")
    print(f"  coef: a = {a:.2f} m, b = {b:.4f}, c = {c:.4f}, d = {d * 1e3:.4f}e-3, e = {e * 1e3:.4f}e-3, f = {f * 1e3:.4f}e-3 (1/m); rms residuo {rms:.2f} m")
    desc = -np.array([b, c]) / g
    print(f"  pendiente |∇h| = {g:.4f} = {np.rad2deg(np.arctan(g)):.1f}° ({100 * g:.1f} %), acimut de bajada {np.rad2deg(np.arctan2(desc[0], desc[1])) % 360:.1f}°,  W = {W:.4f}")
    print(f"  hessiana (1/km) = {(H * 1e3).round(3).tolist()}  autovalores {lamH * 1e3}")
    print(f"  I = {I.round(4).tolist()}  II (1/km) = {(II * 1e3).round(3).tolist()}")
    print(f"  κ1, κ2 = {lam[0] * 1e3:.3f}, {lam[1] * 1e3:.3f} 1/km;  radios {1 / lam[0]:.0f} m, {1 / lam[1]:.0f} m")
    print(f"  acimutes (proyección horizontal) d1 {acimut(D[:, 0]):.1f}°, d2 {acimut(D[:, 1]):.1f}°;  d1ᵀ I d2 = {D[:, 0] @ I @ D[:, 1]:.1e}")
    print(f"  K = {lam.prod() * 1e6:.3f} 1/km²,  H = {lam.mean() * 1e3:.3f} 1/km")
    print(f"  diferencia relativa hessiana vs κ: {100 * abs(lamH[0] - lam[0]) / abs(lam[0]):.1f} %, {100 * abs(lamH[1] - lam[1]) / abs(lam[1]):.1f} %;  ángulo entre proyecciones {acimut(D[:, 1]) - acimut(D[:, 0]):.1f}°")
    # Euler a lo largo de la máxima pendiente (sección vertical = sección normal)
    cos_t = (desc @ I @ D[:, 0]) / np.sqrt(desc @ I @ desc)
    th = np.rad2deg(np.arccos(np.clip(abs(cos_t), 0, 1)))
    k_euler = lam[0] * cos_t**2 + lam[1] * (1 - cos_t**2)
    k_dir = kn(I, II, desc)
    k_perfil_q = (desc @ H @ desc) / (1 + g * g) ** 1.5
    # perfil del DEM interpolado (bilineal) a lo largo de la máxima pendiente, ±3 celdas
    ss = np.linspace(-3 * 0.5 * (dx + dy), 3 * 0.5 * (dx + dy), 25)
    zz = np.array([bilineal(fi - s * desc[1] / dy, co + s * desc[0] / dx) for s in ss])
    p2, p1, _ = np.polyfit(ss, zz, 2)
    k_perfil_dem = 2 * p2 / (1 + p1 * p1) ** 1.5
    print(f"  |perfil DEM − Euler| = {abs(k_perfil_dem - k_euler) * 1e3:.2f} 1/km")
    print(f"  máx. pendiente: θ desde d1 = {th:.1f}°;  Euler {k_euler * 1e3:.3f}, II/I {k_dir * 1e3:.3f}, perfil de la cuadrática {k_perfil_q * 1e3:.3f}, perfil del DEM {k_perfil_dem * 1e3:.3f} 1/km (pendiente del perfil {p1:.4f})")
    # Meusnier a lo largo de la curva de nivel
    ec = np.array([-desc[1], desc[0]])
    kv = ec @ H @ ec
    print(f"  curva de nivel (acimut {acimut(ec):.1f}°): sección vertical {kv * 1e3:.3f} 1/km, cos φ = 1/W = {1 / W:.4f}, producto {kv / W * 1e3:.3f} = κ_n {kn(I, II, ec) * 1e3:.3f} 1/km")
    sens = []
    for k in (2, 3, 4):
        cf = ajuste(fi, co, k)[0]
        Ik, IIk, _ = formas_grafico(cf[1], cf[2], 2 * cf[3], cf[4], 2 * cf[5])
        sens.append(principales(Ik, IIk)[0] * 1e3)
    print("  ventana 5×5, 7×7, 9×9: κ1, κ2 (1/km) =", [s.round(2).tolist() for s in sens])
    resultados[nombre] = dict(fi=fi, co=co, lam=lam, D=D, desc=desc)

print(f"\ncociente curvatura del terreno / curvatura terrestre (vaguada κ1 vs 1/√(MN)): {resultados['vaguada']['lam'][0] * np.sqrt(Mc * Nc):.0f}")

# mapa de curvatura media con ventana 7×7 (paso de la fila central)
dxc, dyc, _ = paso(256)
P = np.linalg.pinv(diseño(3, dxc, dyc))
win = sliding_window_view(Z, (7, 7)).reshape(506, 506, 49)
cf = win @ P.T
bm, cm, dm, em, fm = (cf[..., i] for i in range(1, 6))
Wm = np.sqrt(1 + bm**2 + cm**2)
detI = 1 + bm**2 + cm**2
Lm, Mm, Nm = 2 * dm / Wm, em / Wm, 2 * fm / Wm
Hm = (Lm * (1 + cm**2) - 2 * Mm * bm * cm + Nm * (1 + bm**2)) / (2 * detI)
Km = (Lm * Nm - Mm**2) / detI
print(f"mapa: fracción de celdas con K>0 {np.mean(Km > 0):.3f}, K<0 {np.mean(Km < 0):.3f};  H percentiles 5/50/95 (1/km) {np.percentile(Hm * 1e3, [5, 50, 95]).round(2)}")

# ---------------------------------------------------------------- X
print("\n=== X1  z = x² + xy + y² ===")
I_, II_, _ = formas_grafico(0, 0, 2, 1, 2)
l_, D_ = principales(I_, II_)
print("κ =", l_, " direcciones =", D_.T, " Euler θ=45°:", l_[0] * 0.5 + l_[1] * 0.5)
print("\n=== X2  z = xy ===")
I_, II_, _ = formas_grafico(0, 0, 0, 1, 0)
l_, D_ = principales(I_, II_)
print("κ =", l_, " direcciones =", D_.T, " K =", l_.prod(), " H =", l_.mean())
print("\n=== X3  hélice (3 cos t, 3 sin t, 4 t) ===")
Rh, ch = 3.0, 4.0
t = 0.7; hh = 1e-4
gam = lambda t: np.array([Rh * np.cos(t), Rh * np.sin(t), ch * t])
v1 = (gam(t + hh) - gam(t - hh)) / (2 * hh); v2 = (gam(t + hh) - 2 * gam(t) + gam(t - hh)) / hh**2
kap = np.linalg.norm(np.cross(v1, v2)) / np.linalg.norm(v1) ** 3
cos2 = Rh**2 / (Rh**2 + ch**2)
print("γ'×γ'' =", np.cross(v1, v2).round(4), " |γ'×γ''| =", np.linalg.norm(np.cross(v1, v2)).round(4), " |γ'| =", np.linalg.norm(v1).round(4))
print("κ numérica =", kap, " R/(R²+c²) =", Rh / (Rh**2 + ch**2), " Euler (1/R) cos²θ =", cos2 / Rh, " cos²θ =", cos2,
      " θ =", np.rad2deg(np.arccos(np.sqrt(cos2))))
print("\n=== X4  I = [[2,1],[1,1]], II = [[3,1],[1,1]] ===")
I_, II_ = np.array([[2.0, 1], [1, 1]]), np.array([[3.0, 1], [1, 1]])
l_, D_ = principales(I_, II_)
print("I^-1 II =", np.linalg.solve(I_, II_).tolist(), " κ =", l_, " direcciones =", (D_ / D_[np.argmax(abs(D_), axis=0), [0, 1]]).T)
print("  K =", np.linalg.det(II_) / np.linalg.det(I_), " H =", l_.mean(), " autovalores de II sola =", np.linalg.eigvalsh(II_)[::-1])
print("\n=== X5  d = -4, e = 3, f = 1 (1e-3 1/m), pendiente nula ===")
H5 = np.array([[-8.0, 3], [3, 2]])
l5, V5 = np.linalg.eigh(H5); l5 = l5[::-1]; V5 = V5[:, ::-1]
print("pendiente del autovector de κ1: y/x =", V5[1, 0] / V5[0, 0], " −3 ± √34 =", -3 + np.sqrt(34), -3 - np.sqrt(34))
print("hessiana (1/km) =", H5.tolist(), " κ =", l5, " acimutes =", [acimut(V5[:, k]) for k in range(2)],
      " K =", l5.prod(), " radios (m) =", 1e3 / l5)

# ---------------------------------------------------------------- figura secciones
fig = plt.figure(figsize=(10, 4.4))
ax = fig.add_subplot(1, 2, 1, projection="3d")
u = np.linspace(-1.6, 1.6, 33)
X, Y = np.meshgrid(u, u)
ax.plot_wireframe(X, Y, a1 * X**2 + b1 * Y**2, color=GRIS, lw=0.4, alpha=0.7)
pl = np.linspace(-1.2, 1.2, 2)
PX, PY = np.meshgrid(pl, pl)
ax.plot_surface(PX, PY, 0 * PX, color=GOLD, alpha=0.18)
ax.plot(u, 0 * u, a1 * u**2, color=TEAL, lw=2.5, label=r"sección $y=0$: $\kappa_1=1$")
ax.plot(0 * u, u, b1 * u**2, color=RUST, lw=2.5, label=r"sección $x=0$: $\kappa_2=1/4$")
ax.plot([0, 0], [0, 0], [0, 1.1], color="black", lw=1.5)
ax.text(0, 0, 1.18, "$n$")
ax.view_init(elev=24, azim=-58)
ax.set_xlabel("$x$"); ax.set_ylabel("$y$"); ax.set_zlabel("$z$")
ax.set_box_aspect((1, 1, 0.7))
ax.legend(loc="upper left", fontsize=8, frameon=False)
ax.set_title(r"$z=x^2/2+y^2/8$, plano tangente en el origen", fontsize=10)
ax2 = fig.add_subplot(1, 2, 2)
s = np.linspace(-2.5, 2.5, 200)
ax2.plot(s, a1 * s**2, color=TEAL, lw=2, label=r"perfil $y=0$")
ax2.plot(s, b1 * s**2, color=RUST, lw=2, label=r"perfil $x=0$")
tt = np.linspace(0, 2 * np.pi, 300)
ax2.plot(np.cos(tt), 1 + np.sin(tt), color=TEAL, lw=1, ls="--", label="osculador, radio 1")
ax2.plot(4 * np.cos(tt), 4 + 4 * np.sin(tt), color=RUST, lw=1, ls="--", label="osculador, radio 4")
ax2.axhline(0, color=GRIS, lw=0.8)
ax2.set_xlim(-2.5, 2.5); ax2.set_ylim(-0.3, 2.3); ax2.set_aspect("equal")
ax2.set_xlabel("avance sobre el plano tangente"); ax2.set_ylabel("apartamiento sobre la normal")
ax2.legend(fontsize=8, loc="upper center", ncol=2, frameon=False)
ax2.set_title("las dos secciones principales y sus círculos osculadores", fontsize=10)
fig.tight_layout(); guardar(fig, "curv_secciones.png")

# ---------------------------------------------------------------- figura Euler
fig, axs = plt.subplots(1, 2, figsize=(10, 4.0))
th = np.linspace(0, 180, 361)
tr = np.deg2rad(th)
for (k1_, k2_), col, lab in (((1.0, 0.25), TEAL, r"paraboloide: $\kappa_1=1,\ \kappa_2=1/4$"),
                             ((0.5, -0.5), RUST, r"silla: $\kappa_1=1/2,\ \kappa_2=-1/2$"),
                             ((0.5, 0.0), GOLD, r"cilindro $R=2$: $\kappa_1=1/2,\ \kappa_2=0$")):
    axs[0].plot(th, k1_ * np.cos(tr) ** 2 + k2_ * np.sin(tr) ** 2, color=col, lw=2, label=lab)
axs[0].axhline(0, color=GRIS, lw=0.8)
for xv in (45, 90, 135):
    axs[0].axvline(xv, color=GRIS, lw=0.5, ls=":")
axs[0].set_xticks([0, 45, 90, 135, 180])
axs[0].set_xlabel(r"$\theta$ (grados) desde la primera dirección principal")
axs[0].set_ylabel(r"$\kappa_n(\theta)=\kappa_1\cos^2\theta+\kappa_2\sin^2\theta$")
axs[0].legend(fontsize=8, frameon=False, loc="lower left")
axs[0].set_title("fórmula de Euler", fontsize=10)
g = np.linspace(-3, 3, 401)
GX, GY = np.meshgrid(g, g)
axs[1].contour(GX, GY, 1.0 * GX**2 + 0.25 * GY**2, levels=[1], colors=TEAL, linewidths=2)
axs[1].contour(GX, GY, 0.5 * GX**2 - 0.5 * GY**2, levels=[-1, 1], colors=RUST, linewidths=2)
axs[1].plot(g, g, color=RUST, lw=0.8, ls="--"); axs[1].plot(g, -g, color=RUST, lw=0.8, ls="--")
axs[1].set_aspect("equal"); axs[1].set_xlim(-3, 3); axs[1].set_ylim(-3, 3)
axs[1].axhline(0, color=GRIS, lw=0.6); axs[1].axvline(0, color=GRIS, lw=0.6)
axs[1].set_xlabel(r"$y_1$ (dirección $d_1$)"); axs[1].set_ylabel(r"$y_2$ (dirección $d_2$)")
axs[1].set_title(r"indicatriz de Dupin: $\kappa_1y_1^2+\kappa_2y_2^2=\pm1$", fontsize=10)
fig.tight_layout(); guardar(fig, "curv_euler.png")

# ---------------------------------------------------------------- figura Meusnier
fig, ax = plt.subplots(figsize=(6.4, 4.4))
Rn = 2.0
ph = np.deg2rad(40)
tt = np.linspace(0, 2 * np.pi, 400)
ax.plot(Rn * np.cos(tt), Rn + Rn * np.sin(tt), color=GRIS, lw=1, ls=":")
ax.plot([0, 0], [-0.3, 2 * Rn + 0.3], color=TEAL, lw=1.5)
ax.text(0.08, 2 * Rn + 0.2, r"$n$ (traza del plano normal)", color=TEAL, fontsize=9)
dirm = np.array([np.sin(ph), np.cos(ph)])
ax.plot(*np.column_stack([-0.3 * dirm, 4.3 * dirm]), color=RUST, lw=1.5)
ax.text(*(4.0 * dirm + [-1.2, 0.25]), "traza del plano oblicuo", color=RUST, fontsize=9)
C = np.array([0, Rn]); Cp = (C @ dirm) * dirm
ax.plot(*C, "o", color=TEAL); ax.text(C[0] - 1.0, C[1] + 0.12, r"centro $C_n$", color=TEAL, fontsize=9)
ax.plot(*Cp, "o", color=RUST); ax.text(Cp[0] + 0.12, Cp[1] - 0.1, r"centro $C$", color=RUST, fontsize=9)
ax.plot([C[0], Cp[0]], [C[1], Cp[1]], color="black", lw=0.8, ls="--")
ax.plot([0, Cp[0]], [0, Cp[1]], color=RUST, lw=3, alpha=0.6)
ax.plot(0, 0, "ko"); ax.text(0.1, -0.25, "$p$", fontsize=11)
aa = np.linspace(np.pi / 2 - ph, np.pi / 2, 30)
ax.plot(0.8 * np.cos(aa), 0.8 * np.sin(aa), color="black", lw=1)
ax.text(0.12, 0.9, r"$\varphi$", fontsize=11)
ax.text(1.05, 0.5, r"$|pC| = R_n\cos\varphi$", color=RUST, fontsize=10)
ax.text(-3.55, 3.75, r"esfera de radio $R_n=1/\kappa_n$" + "\n" + r"centrada en $C_n$ (traza)", color=GRIS, fontsize=9)
ax.set_aspect("equal"); ax.set_xlim(-3.6, 3.6); ax.set_ylim(-0.6, 4.6); ax.axis("off")
ax.set_title("corte perpendicular a la tangente común en $p$", fontsize=10)
fig.tight_layout(); guardar(fig, "curv_meusnier.png")

# ---------------------------------------------------------------- figura DEM
ext = [0, 512 * dxc / 1e3, 0, 512 * dyc / 1e3]  # km desde la esquina SO del recorte
ext_in = [3 * dxc / 1e3, 509 * dxc / 1e3, 3 * dyc / 1e3, 509 * dyc / 1e3]
fig, axs = plt.subplots(1, 2, figsize=(10.4, 5.0))
ls = LightSource(azdeg=315, altdeg=45)
axs[0].imshow(ls.hillshade(Z, vert_exag=1, dx=dxc, dy=dyc), cmap="gray", extent=ext, origin="upper")
Xk = (np.arange(512) + 0.5) * dxc / 1e3
Yk = (511 - np.arange(512) + 0.5) * dyc / 1e3
cs = axs[0].contour(Xk, Yk, Z, levels=np.arange(1100, 3000, 100), colors=GOLD, linewidths=0.5)
axs[0].set_title("relieve sombreado y curvas de nivel cada 100 m", fontsize=10)
nrm = TwoSlopeNorm(vmin=-5, vcenter=0, vmax=5)
im = axs[1].imshow(np.clip(Hm * 1e3, -5, 5), cmap="RdBu", norm=nrm, extent=ext_in, origin="upper")
axs[1].set_title(r"curvatura media $H$ (1/km), ventana $7\times7$", fontsize=10)
cb = fig.colorbar(im, ax=axs[1], shrink=0.85)
cb.set_label("azul: cóncava (vaguada); rojo: convexa (loma)", fontsize=8)
for ax in axs:
    for nombre, fi, co in PUNTOS:
        xk, yk = (co + 0.5) * dxc / 1e3, (511 - fi + 0.5) * dyc / 1e3
        ax.plot(xk, yk, "o", ms=8, mfc="none", mec="black", mew=1.8)
        ax.annotate(nombre, (xk, yk), (6, 6), textcoords="offset points", fontsize=9,
                    bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))
    ax.set_xlabel("este (km)"); ax.set_ylabel("norte (km)")
    ax.set_xlim(ext[0], ext[1]); ax.set_ylim(ext[2], ext[3])
fig.tight_layout(); guardar(fig, "curv_dem.png")
print("\nfiguras en", SALIDA.relative_to(RAIZ))
