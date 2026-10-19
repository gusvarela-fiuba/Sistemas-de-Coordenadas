"""Números y figuras del complemento C4 «Marcos de referencia, grillas y remuestreo»
(apunte/contenido/c4-marcos-grillas.tex).

Cubre, en este orden (cada número que cita el texto se imprime con su etiqueta y se verifica
con assert contra el valor escrito en el .tex):
  F   Fajas Gauss-Krüger de POSGAR 2007 (EPSG:5343 a 5349, «POSGAR 2007 / Argentina k»):
      parámetros que informa pyproj (meridiano central, falso este, factor de escala); punto
      de ejemplo de latitud -34,6° y longitud -58,4° (geográficas POSGAR 2007, EPSG:5340)
      proyectado a las fajas 4, 5 y 6 con
      Transformer.from_crs("EPSG:5340", "EPSG:534x", always_xy=True); primer dígito del Este;
      factor de escala en el punto en cada faja (Proj.get_factors, meridional_scale).
  B   Interpolación bilineal en una celda de una malla de correcciones de juguete:
      nodos 12, 18, 10, 25 (cm), punto u = 0,3, v = 0,6; centro de la celda (ejercicio).
  R   Remuestreo de una imagen sintética 8x8 con un borde vertical (columnas 0-3 valen 0,
      columnas 4-7 valen 1) a una cuadrícula girada 20° alrededor del centro (3,5; 3,5):
      vecino más próximo y bilineal; un píxel calculado a mano (fila 2, columna 3).
  M   Cambio de marco POSGAR 94 -> POSGAR 2007 con
      Transformer.from_crs("EPSG:4694", "EPSG:5340", always_xy=True): descripción, precisión
      declarada y definición de la operación elegida; tres puntos sintéticos; diferencias en
      segundos de arco y en metros con el radio medio R1 = (2a+b)/3 de GRS80; verificación
      independiente con numpy (geográficas -> cartesianas -> traslación -> geográficas) y con
      la proyección de la traslación sobre los versores este y norte del lugar; otras
      operaciones candidatas (TransformerGroup); distancia espacial entre dos puntos antes y
      después (no cambia).
  X   Ejercicios: centro de la celda; escala de 2 ppm sobre 5 km; norma de la traslación;
      faja y distancia al meridiano central a partir de un Este.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/marcos-grillas/:
  fajas_este.png        Este del punto de ejemplo según la faja usada; fajas 1 a 7.
  bilineal_celda.png    celda con los cuatro nodos, superficie interpolada y el punto (u, v).
  remuestreo.png        imagen original con la cuadrícula girada; vecino más próximo; bilineal.
  cambio_marco.png      corrimiento POSGAR 94 -> POSGAR 2007 que da pyproj en una malla de
                        puntos del país (flechas exageradas).

Datos: todos sintéticos salvo lo que se pide a pyproj (pyproj 3.8.0, PROJ 9.8.1).
Determinista: no usa azar.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/c4_marcos_grillas.py
"""
import warnings
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pyproj
from pyproj import CRS, Proj, Transformer
from pyproj.transformer import TransformerGroup

warnings.filterwarnings("ignore")
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "marcos-grillas"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
META = {"Software": None}


def guardar(fig, nombre):
    fig.tight_layout()
    fig.savefig(SALIDA / nombre, dpi=150, metadata=META)
    plt.close(fig)


def cerca(x, y, tol):
    assert abs(x - y) <= tol, (x, y)


assert pyproj.__version__ == "3.8.0", pyproj.__version__
assert pyproj.proj_version_str == "9.8.1", pyproj.proj_version_str
print("pyproj", pyproj.__version__, "PROJ", pyproj.proj_version_str)

# ---------------------------------------------------------------- F: fajas
LON, LAT = -58.4, -34.6
print("== F fajas POSGAR 2007")
FAJAS = {}
for k in range(1, 8):
    crs = CRS.from_epsg(5342 + k)
    assert crs.name == f"POSGAR 2007 / Argentina {k}", crs.name
    par = {p["name"]: p["value"] for p in crs.to_json_dict()["conversion"]["parameters"]}
    lon0, fe, k0, lat0, fn = (par["Longitude of natural origin"], par["False easting"],
                              par["Scale factor at natural origin"],
                              par["Latitude of natural origin"], par["False northing"])
    assert lon0 == -72 + 3 * (k - 1) and fe == k * 1_000_000 + 500_000 and k0 == 1
    assert lat0 == -90 and fn == 0
    t = Transformer.from_crs("EPSG:5340", f"EPSG:{5342 + k}", always_xy=True)
    E, N = t.transform(LON, LAT)
    esc = Proj(crs).get_factors(LON, LAT).meridional_scale
    FAJAS[k] = dict(lon0=lon0, fe=fe, E=E, N=N, esc=esc, t=t)
    print(f"faja {k}: EPSG:{5342 + k} lon0={lon0} FE={fe} E={E:.3f} N={N:.3f} escala={esc:.6f}")
for k in (4, 5, 6):
    assert str(int(FAJAS[k]["E"]))[0] == str(k) and len(str(int(FAJAS[k]["E"]))) == 7
cerca(FAJAS[5]["E"], 5_646_775.117, 5e-4); cerca(FAJAS[5]["N"], 6_170_583.695, 5e-4)
cerca(FAJAS[4]["E"], 4_922_120.965, 5e-4); cerca(FAJAS[4]["N"], 6_162_113.168, 5e-4)
cerca(FAJAS[6]["E"], 6_371_573.173, 5e-4); cerca(FAJAS[6]["N"], 6_170_856.526, 5e-4)
cerca(FAJAS[5]["E"] - 5_500_000, 146_775.117, 5e-4)
cerca(FAJAS[4]["E"] - 4_500_000, 422_120.965, 5e-4)
cerca(FAJAS[6]["E"] - 6_500_000, -128_426.827, 5e-4)
cerca(FAJAS[5]["esc"], 1.00027, 5e-6); cerca(FAJAS[4]["esc"], 1.00220, 5e-6)
cerca(FAJAS[6]["esc"], 1.00020, 5e-6)
# ida y vuelta
lo, la = FAJAS[5]["t"].transform(FAJAS[5]["E"], FAJAS[5]["N"], direction="INVERSE")
cerca(lo, LON, 1e-9); cerca(la, LAT, 1e-9)

fig, ax = plt.subplots(figsize=(7.6, 4.0))
for k, f in FAJAS.items():
    lons = np.linspace(f["lon0"] - 5, f["lon0"] + 5, 81)
    E = f["t"].transform(lons, np.full_like(lons, LAT))[0] / 1e6
    ax.plot(lons, E, color=GRIS, lw=0.8, ls=":")
    dentro = np.abs(lons - f["lon0"]) <= 1.5
    ax.plot(lons[dentro], E[dentro], color=TEAL, lw=2.2)
    ax.text(f["lon0"], k + 0.62, f"faja {k}", ha="center", fontsize=8, color=TEAL)
    ax.axvline(f["lon0"] - 1.5, color="#dddddd", lw=0.6, zorder=0)
ax.axvline(-52.5, color="#dddddd", lw=0.6, zorder=0)
for k, c in ((4, RUST), (5, GOLD), (6, RUST)):
    E = FAJAS[k]["E"]
    ax.plot(LON, E / 1e6, "o", color=c, ms=6, zorder=5)
    txt = f"{E:,.0f}".replace(",", ".")
    ax.annotate(f"faja {k}: E = {txt}", (LON, E / 1e6), xytext=(LON + 1.2, E / 1e6 - 0.18),
                fontsize=8, color=c, arrowprops=dict(arrowstyle="-", color=c, lw=0.6))
ax.axvline(LON, color=RUST, lw=0.8, ls="--")
ax.set_xlabel("longitud (grados; negativa al oeste de Greenwich)")
ax.set_ylabel("Este E (millones de metros)")
ax.set_xlim(-74, -52); ax.set_ylim(0.6, 8.0)
ax.set_xticks(range(-72, -50, 3))
ax.set_title("Este del mismo punto (latitud -34,6°) según la faja que se use", fontsize=10)
guardar(fig, "fajas_este.png")

# ---------------------------------------------------------------- B: bilineal
print("== B bilineal")
D00, D10, D01, D11 = 12.0, 18.0, 10.0, 25.0


def bil(u, v, d00=D00, d10=D10, d01=D01, d11=D11):
    return (1 - u) * (1 - v) * d00 + u * (1 - v) * d10 + (1 - u) * v * d01 + u * v * d11


u0, v0 = 0.3, 0.6
pesos = [(1 - u0) * (1 - v0), u0 * (1 - v0), (1 - u0) * v0, u0 * v0]
val = bil(u0, v0)
print("pesos", pesos, "suma", sum(pesos), "valor", val)
cerca(pesos[0], 0.28, 1e-12); cerca(pesos[1], 0.12, 1e-12)
cerca(pesos[2], 0.42, 1e-12); cerca(pesos[3], 0.18, 1e-12); cerca(sum(pesos), 1, 1e-12)
cerca(val, 14.22, 1e-12)
# por etapas: primero sobre los lados inferior y superior, después en v
abajo, arriba = (1 - u0) * D00 + u0 * D10, (1 - u0) * D01 + u0 * D11
cerca(abajo, 13.8, 1e-12); cerca(arriba, 14.5, 1e-12)
cerca((1 - v0) * abajo + v0 * arriba, val, 1e-12)
# coeficientes a + b u + c v + d uv
a, b, c, d = D00, D10 - D00, D01 - D00, D11 - D10 - D01 + D00
print("coeficientes", a, b, c, d)
assert (a, b, c, d) == (12.0, 6.0, -2.0, 9.0)
cerca(a + b * u0 + c * v0 + d * u0 * v0, val, 1e-12)
centro = bil(0.5, 0.5)
cerca(centro, 16.25, 1e-12); cerca(centro, (D00 + D10 + D01 + D11) / 4, 1e-12)

fig, ax = plt.subplots(figsize=(4.8, 4.2))
uu, vv = np.meshgrid(np.linspace(0, 1, 101), np.linspace(0, 1, 101))
im = ax.contourf(uu, vv, bil(uu, vv), levels=np.arange(10, 25.5, 1), cmap="GnBu")
ax.contour(uu, vv, bil(uu, vv), levels=np.arange(10, 25.5, 1), colors="white", linewidths=0.4)
fig.colorbar(im, ax=ax, label="corrimiento interpolado (cm)")
for (x, y, dv, nom) in ((0, 0, D00, "00"), (1, 0, D10, "10"), (0, 1, D01, "01"), (1, 1, D11, "11")):
    ax.plot(x, y, "s", color=TEAL, ms=9, clip_on=False, zorder=5)
    ax.text(x + (0.04 if x == 0 else -0.04), y + (0.05 if y == 0 else -0.08),
            rf"$\Delta_{{{nom}}}={dv:.0f}$", ha="left" if x == 0 else "right", fontsize=9)
ax.plot(u0, v0, "o", color=RUST, ms=7, zorder=6)
ax.text(u0 + 0.03, v0 + 0.03, "(0,3; 0,6)\n14,22 cm", color=RUST, fontsize=9)
ax.plot([0, 1], [v0, v0], color=RUST, lw=0.6, ls="--"); ax.plot([u0, u0], [0, 1], color=RUST, lw=0.6, ls="--")
ax.set_xlabel("u"); ax.set_ylabel("v"); ax.set_aspect("equal")
ax.set_xticks([0, 0.5, 1], ["0", "0,5", "1"]); ax.set_yticks([0, 0.5, 1], ["0", "0,5", "1"])
ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.02)
guardar(fig, "bilineal_celda.png")

# ---------------------------------------------------------------- R: remuestreo
print("== R remuestreo")
n = 8
IMG = np.zeros((n, n)); IMG[:, 4:] = 1.0      # fila r (hacia abajo), columna c; borde vertical
TH = np.deg2rad(20.0)
CEN = np.array([3.5, 3.5])
ROT = np.array([[np.cos(TH), -np.sin(TH)], [np.sin(TH), np.cos(TH)]])


def origen(r, c):
    """Centro del píxel (r, c) de la cuadrícula nueva, en coordenadas (x, y) = (columna, fila)
    de la imagen original: la cuadrícula nueva es la vieja girada 20° alrededor del centro."""
    return CEN + ROT @ (np.array([c, r], float) - CEN)


def vecino(x, y):
    ci, ri = int(np.floor(x + 0.5)), int(np.floor(y + 0.5))
    if 0 <= ri < n and 0 <= ci < n:
        return IMG[ri, ci]
    return np.nan


def bilin(x, y):
    c0, r0 = int(np.floor(x)), int(np.floor(y))
    if not (0 <= r0 < n - 1 and 0 <= c0 < n - 1):
        return np.nan
    uu_, vv_ = x - c0, y - r0
    return bil(uu_, vv_, IMG[r0, c0], IMG[r0, c0 + 1], IMG[r0 + 1, c0], IMG[r0 + 1, c0 + 1])


NN = np.full((n, n), np.nan); BL = np.full((n, n), np.nan)
for r in range(n):
    for c_ in range(n):
        x, y = origen(r, c_)
        NN[r, c_], BL[r, c_] = vecino(x, y), bilin(x, y)
print("vecino\n", NN); print("bilineal\n", np.round(BL, 2))
assert set(np.unique(NN[~np.isnan(NN)])) == {0.0, 1.0}
inter = BL[(~np.isnan(BL)) & (BL > 0) & (BL < 1)]
print("píxeles bilineales intermedios:", inter.size, "sin dato:", int(np.isnan(BL).sum()), int(np.isnan(NN).sum()))
assert inter.size == 6 and int(np.isnan(BL).sum()) == 16 and int(np.isnan(NN).sum()) == 8
# un píxel a mano
rx, cx = 2, 3
x, y = origen(rx, cx)
print("píxel (2,3) ->", x, y, "vecino", vecino(x, y), "bilineal", bilin(x, y))
cerca(x, 3.5432, 5e-5); cerca(y, 1.9195, 5e-5)
assert vecino(x, y) == 1.0                    # columna 4, fila 2 de la original
cerca(x - 3, 0.5432, 5e-5); cerca(y - 1, 0.9195, 5e-5)       # celda filas 1-2, columnas 3-4
cerca(bilin(x, y), 0.5432, 5e-5)              # columna 3 vale 0 y columna 4 vale 1: queda u

fig, axs = plt.subplots(1, 3, figsize=(9.6, 3.6))
cmap = matplotlib.colormaps["Greys"].copy(); cmap.set_bad("#f3e6c8")
for ax, A, tit in ((axs[0], IMG, "original 8×8 y cuadrícula nueva"),
                   (axs[1], NN, "vecino más próximo"), (axs[2], BL, "bilineal")):
    ax.imshow(np.ma.masked_invalid(A), cmap=cmap, vmin=-0.15, vmax=1.15, origin="upper",
              extent=(-0.5, n - 0.5, n - 0.5, -0.5))
    ax.set_xticks(range(n)); ax.set_yticks(range(n)); ax.tick_params(labelsize=7)
    ax.set_title(tit, fontsize=9)
    ax.set_xlabel("columna", fontsize=8); ax.set_ylabel("fila", fontsize=8)
for r in range(n + 1):
    a_ = np.array([origen(r - 0.5, c_ - 0.5) for c_ in (0, n)])
    b_ = np.array([origen(c_ - 0.5, r - 0.5) for c_ in (0, n)])
    axs[0].plot(a_[:, 0], a_[:, 1], color=RUST, lw=0.7); axs[0].plot(b_[:, 0], b_[:, 1], color=RUST, lw=0.7)
ctr = np.array([origen(r, c_) for r in range(n) for c_ in range(n)])
axs[0].plot(ctr[:, 0], ctr[:, 1], ".", color=RUST, ms=3)
axs[0].plot(x, y, "o", color=GOLD, ms=6, mec="k", mew=0.5)
axs[0].set_xlim(-1.5, n + 0.5); axs[0].set_ylim(n + 0.5, -1.5)
for r in range(n):
    for c_ in range(n):
        v_ = BL[r, c_]
        if not np.isnan(v_):
            axs[2].text(c_, r, f"{v_:.2f}".replace(".", ","), ha="center", va="center", fontsize=5.5,
                        color="white" if v_ > 0.55 else "black")
for ax in axs[1:]:
    ax.add_patch(plt.Rectangle((cx - 0.5, rx - 0.5), 1, 1, fill=False, ec=GOLD, lw=1.6))
guardar(fig, "remuestreo.png")

# ---------------------------------------------------------------- M: cambio de marco
print("== M cambio de marco POSGAR 94 -> POSGAR 2007")
A_GRS80, F_GRS80 = 6_378_137.0, 1 / 298.257222101
B_GRS80 = A_GRS80 * (1 - F_GRS80)
R1 = (2 * A_GRS80 + B_GRS80) / 3
cerca(R1, 6_371_008.771, 5e-4)
tm = Transformer.from_crs("EPSG:4694", "EPSG:5340", always_xy=True)
PUNTOS = {"P": (-58.4, -34.6), "Q": (-65.0, -27.0), "S": (-68.5, -45.0)}
SAL = {}
for nom, (lo, la) in PUNTOS.items():
    lo2, la2 = tm.transform(lo, la)
    dlo, dla = lo2 - lo, la2 - la
    de = R1 * np.cos(np.deg2rad(la)) * np.deg2rad(dlo)
    dn = R1 * np.deg2rad(dla)
    SAL[nom] = dict(lo2=lo2, la2=la2, dlo_s=dlo * 3600, dla_s=dla * 3600, de=de, dn=dn, h=np.hypot(de, dn))
    print(nom, f"lon {lo2:.9f} lat {la2:.9f}  dlon {dlo*3600:.4f}\" dlat {dla*3600:.4f}\" "
          f"dE {de:.3f} dN {dn:.3f} |d| {np.hypot(de, dn):.3f} m")
grupo = TransformerGroup("EPSG:4694", "EPSG:5340", always_xy=True)
for tr in grupo.transformers:
    print("candidata:", tr.description, "| precisión", tr.accuracy, "|", tr.transform(*PUNTOS["P"]))
assert [tr.accuracy for tr in grupo.transformers] == [1.5, 2.0, 10.0]
# from_crs no fija la operación de antemano (su descripción dice «unavailable until proj_trans
# is called»); lo que devuelve coincide con la primera candidata, la de menor incertidumbre.
primera = grupo.transformers[0]
print("primera candidata:", primera.description)
print("definición:", primera.definition)
assert primera.description.startswith("POSGAR 94 to WGS 84 (1) + Inverse of POSGAR 2007 to WGS 84 (2)")
assert "helmert x=0.41 y=-0.46 z=0.35" in primera.definition and "ellps=WGS84" in primera.definition
for nom, (lo, la) in PUNTOS.items():
    lo1, la1 = primera.transform(lo, la)
    assert (lo1, la1) == (SAL[nom]["lo2"], SAL[nom]["la2"])
assert all(tr.transform(*PUNTOS["P"]) == PUNTOS["P"] for tr in grupo.transformers[1:])

# verificación independiente con numpy (elipsoide WGS84, el que declara la definición)
A_W, F_W = 6_378_137.0, 1 / 298.257223563
E2 = F_W * (2 - F_W)
T = np.array([0.41, -0.46, 0.35])
cerca(np.linalg.norm(T), 0.709, 5e-4)


def a_cart(lo, la, h=0.0):
    lo, la = np.deg2rad(lo), np.deg2rad(la)
    Nn = A_W / np.sqrt(1 - E2 * np.sin(la) ** 2)
    return np.array([(Nn + h) * np.cos(la) * np.cos(lo), (Nn + h) * np.cos(la) * np.sin(lo),
                     (Nn * (1 - E2) + h) * np.sin(la)])


def a_geo(X):
    x, y, z = X
    lo = np.arctan2(y, x); p = np.hypot(x, y); la = np.arctan2(z, p * (1 - E2))
    for _ in range(10):
        Nn = A_W / np.sqrt(1 - E2 * np.sin(la) ** 2)
        h = p / np.cos(la) - Nn
        la = np.arctan2(z, p * (1 - E2 * Nn / (Nn + h)))
    return np.rad2deg(lo), np.rad2deg(la), h


for nom, (lo, la) in PUNTOS.items():
    lo2, la2, _ = a_geo(a_cart(lo, la) + T)
    cerca(lo2, SAL[nom]["lo2"], 1e-10); cerca(la2, SAL[nom]["la2"], 1e-10)
    # versores este y norte del lugar
    l_, f_ = np.deg2rad(lo), np.deg2rad(la)
    ue = np.array([-np.sin(l_), np.cos(l_), 0.0])
    un = np.array([-np.sin(f_) * np.cos(l_), -np.sin(f_) * np.sin(l_), np.cos(f_)])
    te, tn = ue @ T, un @ T
    SAL[nom].update(te=te, tn=tn)
    print(nom, f"t·e = {te:.3f}  t·n = {tn:.3f}")
    cerca(te, SAL[nom]["de"], 0.003); cerca(tn, SAL[nom]["dn"], 0.003)
# primer orden: M dphi = t·n y N cos(phi) dlambda = t·e (elipsoide WGS84, h = 0)
for nom, (lo, la) in PUNTOS.items():
    f_ = np.deg2rad(la); w = np.sqrt(1 - E2 * np.sin(f_) ** 2)
    Mr, Nr = A_W * (1 - E2) / w ** 3, A_W / w
    dfi = np.deg2rad(SAL[nom]["la2"] - la); dla = np.deg2rad(SAL[nom]["lo2"] - lo)
    print(nom, f"M dphi = {Mr * dfi:.4f}  N cos dlam = {Nr * np.cos(f_) * dla:.4f}  M = {Mr:.1f}")
    cerca(Mr * dfi, SAL[nom]["tn"], 1e-5); cerca(Nr * np.cos(f_) * dla, SAL[nom]["te"], 1e-5)
    if nom == "P":
        cerca(Mr, 6_356_008.1, 0.05); cerca(R1 / Mr, 1.0024, 5e-5)
cerca(SAL["P"]["te"], 0.108, 5e-4); cerca(SAL["P"]["tn"], 0.633, 5e-4)
# distancia espacial entre P y Q antes y después: una traslación no la cambia
XP, XQ = a_cart(*PUNTOS["P"]), a_cart(*PUNTOS["Q"])
dist0 = np.linalg.norm(XQ - XP); dist1 = np.linalg.norm((XQ + T) - (XP + T))
print("distancia PQ espacial", dist0, dist1)
cerca(dist0, dist1, 1e-6)

fig, ax = plt.subplots(figsize=(4.6, 5.6))
lons, lats = np.arange(-72, -52, 3.0), np.arange(-54, -21, 4.0)
LO, LA = np.meshgrid(lons, lats)
lo2, la2 = tm.transform(LO, LA)
DE = R1 * np.cos(np.deg2rad(LA)) * np.deg2rad(lo2 - LO)
DN = R1 * np.deg2rad(la2 - LA)
q = ax.quiver(LO, LA, DE, DN, angles="xy", scale_units="xy", scale=0.25, color=TEAL, width=0.006)
ax.quiverkey(q, 0.22, 0.04, 0.5, "0,5 m", labelpos="E", coordinates="axes")
for nom, (lo, la) in PUNTOS.items():
    ax.plot(lo, la, "o", color=RUST, ms=5); ax.text(lo + 0.5, la + 0.4, nom, color=RUST)
ax.set_xlabel("longitud (grados)"); ax.set_ylabel("latitud (grados)")
ax.set_xlim(-75, -50); ax.set_ylim(-57, -19); ax.set_aspect(1 / np.cos(np.deg2rad(38)))
ax.set_title("Corrimiento POSGAR 94 → POSGAR 2007\n(pyproj; flechas muy exageradas)", fontsize=9)
guardar(fig, "cambio_marco.png")

# ---------------------------------------------------------------- X: ejercicios
print("== X ejercicios")
mu = 2e-6
cerca(mu * 5000, 0.01, 1e-12)                 # 2 ppm sobre 5 km = 1 cm
Ex = 3_412_500.0                              # Este de ejemplo
assert str(int(Ex))[0] == "3" and Ex - 3_500_000 == -87_500
print("listo")


def test_numeros():
    """pytest: el script corre entero y sus asserts pasan al importarlo."""
    assert FAJAS[5]["E"] > 5e6 and abs(val - 14.22) < 1e-12
