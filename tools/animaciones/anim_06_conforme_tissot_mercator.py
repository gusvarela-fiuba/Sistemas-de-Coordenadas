"""Animación 06 (Unidad 15, transformaciones conformes): del elipsoide GRS80 al plano, lado a lado, con la
cilíndrica equidistante (h = 1, k = a/(N cos φ): NO conforme) y con Mercator (h = k: conforme).

Mostramos el mismo parche del elipsoide en los dos paneles: cuatro fajas de "cuadraditos métricos" (lado Δ,
igual al norte y al este) centradas en los paralelos 0°, −34,6° (Buenos Aires), −54° (Ushuaia) y −65°, entre
λ = 0° y λ = 40°, cada una con una indicatriz de Tissot (círculo de radio r en el terreno) y dos visuales a 90°
(NE, azimut 45°, y SE, azimut 135°). Con s = 0 ("terreno") cada faja está en coordenadas métricas locales
(e = N cos φ · λ hacia el este, n = M · dφ hacia el norte); con s = 1 ("mapa") cada punto está en su posición
proyectada; en el medio interpolamos linealmente punto a punto (es una morfosis, no una proyección intermedia).
En la equidistante los cuadraditos se estiran en E-O, las indicatrices se vuelven elipses y el ángulo entre las
visuales se tuerce; en Mercator los cuadraditos siguen cuadraditos (más grandes hacia el polo), las indicatrices
siguen círculos y el ángulo sigue siendo 90°.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.lines import Line2D
from matplotlib.patches import Polygon

from unidades import cb104 as lib

from ._comun import PALETA, guardar_frame, rotulo

ELIP = lib.elipsoide_grs80()
A, E2 = ELIP["a"], ELIP["e2"]
E = np.sqrt(E2)
KM = 1000.0

# Paralelos de referencia (hemisferio sur) y parche en longitud.
PARALELOS = [(0.0, "0° · ecuador"), (-34.6, "−34,6° · Buenos Aires"), (-54.0, "−54° · Ushuaia"), (-65.0, "−65°")]
LAM_MAX = np.radians(40.0)
DELTA = 900 * KM         # lado de los cuadraditos métricos (igual al norte y al este)
R_TISSOT = 250 * KM      # radio de la indicatriz en el terreno
LARGO_VISUAL = 1.5 * R_TISSOT
N_CIRC = 72


# ---------------------------------------------------------------- geometría del elipsoide y de las proyecciones
_PHI_GRID = np.linspace(np.radians(-80.0), np.radians(5.0), 85_001)
_M_GRID, _ = lib.radios_curvatura(_PHI_GRID)
_S_GRID = np.concatenate([[0.0], np.cumsum(0.5 * (_M_GRID[1:] + _M_GRID[:-1]) * np.diff(_PHI_GRID))])
_S_GRID -= np.interp(0.0, _PHI_GRID, _S_GRID)   # S(0) = 0: arco de meridiano medido desde el ecuador


def arco_meridiano(phi):
    """S(φ) = ∫₀^φ M dφ (trapecios sobre una grilla fina de 85 001 nodos)."""
    return np.interp(phi, _PHI_GRID, _S_GRID)


def q_mercator(phi, e=E):
    """Latitud isométrica q(φ) = ln tan(π/4 + φ/2) − (e/2) ln((1 + e sin φ)/(1 − e sin φ)). e = 0 → esfera."""
    phi = np.asarray(phi, dtype=float)
    return np.log(np.tan(np.pi / 4 + phi / 2)) - (e / 2) * np.log((1 + e * np.sin(phi)) / (1 - e * np.sin(phi)))


def dq_dphi(phi, e=E):
    """dq/dφ = (1 − e²)/((1 − e² sin²φ) cos φ)."""
    phi = np.asarray(phi, dtype=float)
    return (1 - e**2) / ((1 - e**2 * np.sin(phi) ** 2) * np.cos(phi))


def escalas(phi, proy):
    """(h, k) en el paralelo φ: h a lo largo del meridiano, k a lo largo del paralelo (ambas direcciones
    principales en las dos cilíndricas). Equidistante: h = 1; Mercator: h = a q'(φ)/M. En ambas k = a/(N cos φ)."""
    M, N = lib.radios_curvatura(phi)
    k = A / (N * np.cos(phi))
    h = np.ones_like(k) if proy == "eq" else A * dq_dphi(phi) / M
    return h, k


def omega_max(h, k):
    """Deformación angular máxima de Tissot (grados): sin(ω/2) = |h − k|/(h + k)."""
    return np.degrees(2 * np.arcsin(np.abs(h - k) / (h + k)))


def proyectar(phi, lam, proy):
    """(x, y) de la cilíndrica equidistante (x = aλ, y = S(φ)) o de Mercator (x = aλ, y = a q(φ))."""
    x = A * lam
    y = arco_meridiano(phi) if proy == "eq" else A * q_mercator(phi)
    return x, y


def _verificar():
    phis = np.radians([p for p, _ in PARALELOS])
    assert abs(q_mercator(0.0)) < 1e-12, "q(0) debe ser 0"
    phi_t = np.radians([-70.0, -34.6, -10.0, 20.0, 60.0])
    assert np.allclose(q_mercator(phi_t, e=0.0), np.log(np.tan(np.pi / 4 + phi_t / 2)), atol=1e-12), \
        "para e = 0, q(φ) = ln tan(π/4 + φ/2)"
    d = 1e-5
    assert np.allclose((q_mercator(phi_t + d) - q_mercator(phi_t - d)) / (2 * d), dq_dphi(phi_t), rtol=1e-6)
    h, k = escalas(phis, "mer")
    assert np.all(np.abs(h - k) < 1e-9), f"Mercator: h ≠ k, {h - k}"
    h, k = escalas(phis, "eq")
    assert np.all(h == 1.0)
    M, _ = lib.radios_curvatura(phis)
    d = 1e-4
    h_num = (arco_meridiano(phis + d) - arco_meridiano(phis - d)) / (2 * d) / M
    assert np.allclose(h_num, 1.0, atol=1e-6), f"equidistante: dS/dφ / M ≠ 1, {h_num}"


_verificar()


# ---------------------------------------------------------------- las fajas de cuadraditos con su indicatriz
class Faja:
    """Faja de cuadraditos métricos centrada en el paralelo φ_j, con indicatriz, visuales y arco del ángulo.
    Guarda los puntos en el terreno (métrica local) y en los dos mapas; `posicion(s, proy)` los interpola."""

    def __init__(self, phi_deg: float, nombre: str):
        self.nombre = nombre
        self.phi = np.radians(phi_deg)
        M, N = lib.radios_curvatura(self.phi)
        self.M, self.N = float(M), float(N)
        largo = self.N * np.cos(self.phi) * LAM_MAX          # largo del paralelo entre λ = 0° y 40°
        self.n_cuad = max(1, int(largo // DELTA))
        e_fin = self.n_cuad * DELTA
        # Segmentos de la grilla (bordes de los cuadraditos): rectas en ambas proyecciones → alcanzan los extremos.
        segs = [((i * DELTA, -DELTA / 2), (i * DELTA, DELTA / 2)) for i in range(self.n_cuad + 1)]
        segs += [((0.0, -DELTA / 2), (e_fin, -DELTA / 2)), ((0.0, DELTA / 2), (e_fin, DELTA / 2))]
        self.segs = np.array(segs)                           # (nseg, 2, 2) en (e, n)
        self.e_c = 1.5 * DELTA if self.n_cuad >= 2 else 0.5 * DELTA
        t = np.linspace(0, 2 * np.pi, N_CIRC, endpoint=False)
        circ = np.column_stack([self.e_c + R_TISSOT * np.cos(t), R_TISSOT * np.sin(t)])
        az = np.radians([45.0, 135.0])                       # NE y SE (azimut desde el norte, horario)
        vis = np.column_stack([self.e_c + LARGO_VISUAL * np.sin(az), LARGO_VISUAL * np.cos(az)])
        ta = np.linspace(np.radians(-45.0), np.radians(45.0), 25)   # arco entre las visuales (ángulo matemático)
        arco = np.column_stack([self.e_c + 0.55 * R_TISSOT * np.cos(ta), 0.55 * R_TISSOT * np.sin(ta)])
        centro = np.array([[self.e_c, 0.0]])
        puntos = np.vstack([self.segs.reshape(-1, 2), circ, vis, arco, centro])
        n_seg = self.segs.shape[0] * 2
        self.i_seg = slice(0, n_seg)
        self.i_circ = slice(n_seg, n_seg + N_CIRC)
        self.i_vis = slice(n_seg + N_CIRC, n_seg + N_CIRC + 2)
        self.i_arco = slice(n_seg + N_CIRC + 2, n_seg + N_CIRC + 2 + len(ta))
        self.i_centro = n_seg + N_CIRC + 2 + len(ta)
        e, n = puntos[:, 0], puntos[:, 1]
        self.terreno = np.column_stack([e, arco_meridiano(self.phi) + n])
        phi_p = self.phi + n / self.M
        lam_p = e / (self.N * np.cos(self.phi))
        self.mapa = {p: np.column_stack(proyectar(phi_p, lam_p, p)) for p in ("eq", "mer")}
        self.hk = {p: tuple(float(v) for v in escalas(self.phi, p)) for p in ("eq", "mer")}

    def posicion(self, s: float, proy: str) -> np.ndarray:
        return (1.0 - s) * self.terreno + s * self.mapa[proy]


def _nan_segmentos(pts: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Puntos (2·nseg, 2) → una sola polilínea con NaN entre segmentos."""
    seg = pts.reshape(-1, 2, 2)
    nan = np.full((seg.shape[0], 1, 2), np.nan)
    out = np.concatenate([seg, nan], axis=1).reshape(-1, 2)
    return out[:, 0], out[:, 1]


def _num(v: float, dec: int = 3) -> str:
    return f"{v:.{dec}f}".replace(".", ",")


def _angulo_visuales(h: float, k: float) -> float:
    """Ángulo entre las visuales NE y SE tras aplicar el jacobiano diag(k, h) a (1, 1)/√2 y (1, −1)/√2:
    2·atan(h/k). Es la medida diferencial (en el centro de la indicatriz), no la cuerda finita de 375 km."""
    return float(np.degrees(2 * np.arctan2(h, k)))


# ---------------------------------------------------------------- render
def render(out_dir: Path, s: np.ndarray) -> None:
    fajas = [Faja(p, nombre) for p, nombre in PARALELOS]
    proys = ("eq", "mer")
    titulos = {"eq": "Cilíndrica equidistante: h = 1, k = 1/cos φ (no conforme)",
               "mer": "Mercator: h = k (conforme)"}

    # Límites fijos, iguales en los dos paneles (unión de terreno y ambos mapas: el mapa es el estado más extenso).
    todos = np.vstack([f.terreno for f in fajas] + [f.mapa[p] for f in fajas for p in proys])
    y_min, y_max = todos[:, 1].min() - 250 * KM, todos[:, 1].max() + 1050 * KM
    rects = [(0.03, 0.02, 0.46, 0.80), (0.52, 0.02, 0.46, 0.80)]
    razon_caja = (12.8 * rects[0][2]) / (7.2 * rects[0][3])
    x_min = -350 * KM
    x_max = x_min + (y_max - y_min) * razon_caja
    x_label = A * LAM_MAX + 300 * KM                     # ninguna faja pasa de λ = 40° → x = a·40°

    fig = plt.figure(figsize=(12.8, 7.2), dpi=100, facecolor=PALETA["paper"])
    fig.text(0.5, 0.965, "conforme = la indicatriz de Tissot es un círculo en todo punto: "
             "cuadraditos a cuadraditos, ángulos intactos", ha="center", va="center", fontsize=13,
             color=PALETA["tinta"])
    fig.text(0.5, 0.932, f"GRS80 · cuadraditos de {DELTA / KM:.0f} km de lado · indicatriz de radio "
             f"{R_TISSOT / KM:.0f} km · visuales NE y SE (90° en el terreno) · "
             "ida y vuelta terreno ⇄ mapa (morfosis lineal punto a punto)",
             ha="center", va="center", fontsize=9.5, color=PALETA["gris"])
    ax_bar = fig.add_axes([0.44, 0.889, 0.12, 0.012])
    ax_bar.set_xlim(0, 1); ax_bar.set_ylim(0, 1); ax_bar.axis("off")
    ax_bar.plot([0, 1], [0.5, 0.5], color=PALETA["gris"], lw=1.2, solid_capstyle="round")
    (marca,) = ax_bar.plot([0], [0.5], "o", color=PALETA["gold"], ms=6, mec=PALETA["tinta"], mew=0.6)
    fig.text(0.432, 0.895, "terreno", ha="right", va="center", fontsize=9, color=PALETA["gris"])
    fig.text(0.568, 0.895, "mapa", ha="left", va="center", fontsize=9, color=PALETA["gris"])

    artistas = {}   # (proy, j) → dict de artistas
    for proy, rect in zip(proys, rects):
        ax = fig.add_axes(rect)
        ax.set_facecolor(PALETA["paper"])
        ax.set_xlim(x_min, x_max); ax.set_ylim(y_min, y_max)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(titulos[proy], fontsize=12, color=PALETA["tinta"], pad=4, loc="left", x=0.0)
        h54, k54 = next(f for f in fajas if f.nombre.startswith("−54")).hk[proy]
        texto = (f"h = {_num(h54)} · k = {_num(k54)} · ω_max = {_num(omega_max(h54, k54))}°"
                 if proy == "eq" else
                 f"h = k = {_num(k54)} · ω_max = {_num(omega_max(h54, k54))}°")
        rotulo(ax, "en −54° (Ushuaia), mapa:  " + texto, PALETA["teal"] if proy == "mer" else PALETA["rust"])
        for j, faja in enumerate(fajas):
            grilla = Line2D([], [], color=PALETA["tinta"], lw=0.9, alpha=0.75, zorder=2)
            ax.add_line(grilla)
            circ = Polygon(np.zeros((N_CIRC, 2)), closed=True, facecolor=PALETA["violeta"], alpha=0.22,
                           edgecolor=PALETA["violeta"], lw=1.4, zorder=3)
            ax.add_patch(circ)
            arco = Line2D([], [], color=PALETA["gold"], lw=1.6, zorder=4)
            ax.add_line(arco)
            vis_ne = Line2D([], [], color=PALETA["teal"], lw=2.0, zorder=5, solid_capstyle="round")
            vis_se = Line2D([], [], color=PALETA["rust"], lw=2.0, zorder=5, solid_capstyle="round")
            ax.add_line(vis_ne); ax.add_line(vis_se)
            etiq = ax.text(x_label, 0.0, "", fontsize=9.5, color=PALETA["tinta"], va="center", ha="left",
                           linespacing=1.35)
            artistas[(proy, j)] = dict(grilla=grilla, circ=circ, arco=arco, ne=vis_ne, se=vis_se, etiq=etiq)

    for i, si in enumerate(s):
        si = float(si)
        marca.set_data([si], [0.5])
        for proy in proys:
            for j, faja in enumerate(fajas):
                pos = faja.posicion(si, proy)
                art = artistas[(proy, j)]
                art["grilla"].set_data(*_nan_segmentos(pos[faja.i_seg]))
                art["circ"].set_xy(pos[faja.i_circ])
                art["arco"].set_data(pos[faja.i_arco][:, 0], pos[faja.i_arco][:, 1])
                c = pos[faja.i_centro]
                for key, idx in (("ne", 0), ("se", 1)):
                    v = pos[faja.i_vis][idx]
                    art[key].set_data([c[0], v[0]], [c[1], v[1]])
                h, k = faja.hk[proy]
                h_s, k_s = (1 - si) + si * h, (1 - si) + si * k        # escalas de la figura interpolada
                ang = _angulo_visuales(h_s, k_s)
                art["etiq"].set_position((x_label, c[1]))
                art["etiq"].set_text(f"φ = {faja.nombre}\n"
                                     f"h = {_num(h_s)}  k = {_num(k_s)}  ω = {_num(omega_max(h_s, k_s), 2)}°  "
                                     f"∠ = {_num(ang, 1)}°")
        guardar_frame(fig, out_dir, i)
    plt.close(fig)
