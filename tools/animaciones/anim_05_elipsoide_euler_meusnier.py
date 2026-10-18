"""Animación 05 — curvaturas sobre el elipsoide de revolución: Euler y Meusnier en un punto P.

Elipsoide exagerado (a = 1, f = 0.25; GRS80 tiene f ≈ 1/298) para que se note. P en φ = 40°, λ = 0.
Etapa 1 (Euler): el plano normal en P gira en acimut α de 0° (meridiano, radio M) a 90° (primer vertical,
radio N); la sección normal es la intersección exacta del plano con el elipsoide y el círculo osculador
tiene radio 1/R = cos²α/M + sin²α/N.
Etapa 2 (Meusnier): el plano, que contiene la dirección este, se inclina desde el plano normal hasta el
plano del paralelo (ángulo φ): el círculo de curvatura pasa de radio N a r = N cos φ, el paralelo.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from unidades import cb104 as lib

from ._comun import PALETA, etapas, guardar_frame, nueva_figura, rotulo

A_EXAG, F_EXAG = 1.0, 0.25
ELI = lib.elipsoide(A_EXAG, F_EXAG)         # a, f, b, e2, ep2
PHI = np.deg2rad(40.0)
LIMITE = 1.45
PLANO_U, PLANO_V = 1.25, (-2.2, 0.35)        # extensión del rectángulo del plano: ancho y a lo largo de la normal


def punto_y_marco(phi: float, lam: float = 0.0) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """P sobre el elipsoide y el triedro local (n normal, t_N hacia el norte, t_E hacia el este)."""
    P = lib.geodesica_a_cartesiana(phi, lam, 0.0, a=ELI["a"], e2=ELI["e2"])
    n = lib.normal_elipsoide(phi, lam)
    t_N = np.array([-np.sin(phi) * np.cos(lam), -np.sin(phi) * np.sin(lam), np.cos(phi)])
    t_E = np.array([-np.sin(lam), np.cos(lam), 0.0])
    return P, n, t_N, t_E


def _Q(x: np.ndarray) -> np.ndarray:
    """Forma cuadrática del elipsoide: Q(x) = x²/a² + y²/a² + z²/b²; la superficie es Q = 1."""
    return (x[..., 0] ** 2 + x[..., 1] ** 2) / ELI["a"] ** 2 + x[..., 2] ** 2 / ELI["b"] ** 2


def seccion_plana(P: np.ndarray, d1: np.ndarray, d2: np.ndarray, n_pts: int = 241) -> np.ndarray:
    """Intersección exacta del plano por P generado por (d1, d2) con el elipsoide: para cada dirección
    w(θ) = cos θ d1 + sin θ d2 del plano, el rayo P + t w corta la cuádrica en t = −2 B(P, w)/Q(w)
    (la otra raíz es t = 0, el propio P). Devuelve la curva cerrada (n_pts × 3)."""
    th = np.linspace(0.0, 2 * np.pi, n_pts)
    w = np.outer(np.cos(th), d1) + np.outer(np.sin(th), d2)
    D = np.array([1 / ELI["a"] ** 2, 1 / ELI["a"] ** 2, 1 / ELI["b"] ** 2])
    Qw = np.sum(D * w * w, axis=1)
    Bw = np.sum(D * P * w, axis=1)
    t = -2.0 * Bw / Qw
    return P + t[:, None] * w


def circulo_3d(centro: np.ndarray, d1: np.ndarray, d2: np.ndarray, r: float, n_pts: int = 181) -> np.ndarray:
    th = np.linspace(0.0, 2 * np.pi, n_pts)
    return centro + r * (np.outer(np.cos(th), d1) + np.outer(np.sin(th), d2))


def rectangulo_plano(P: np.ndarray, d_ancho: np.ndarray, d_largo: np.ndarray) -> list[tuple[float, ...]]:
    u, (v0, v1) = PLANO_U, PLANO_V
    return [tuple(P - u * d_ancho + v0 * d_largo), tuple(P + u * d_ancho + v0 * d_largo),
            tuple(P + u * d_ancho + v1 * d_largo), tuple(P - u * d_ancho + v1 * d_largo)]


def _mezcla(c1: str, c2: str, t: float) -> tuple[float, float, float]:
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2))
    return tuple((1.0 - t) * a + t * b)


def render(out_dir: Path, s: np.ndarray) -> None:
    a, b, e2 = ELI["a"], ELI["b"], ELI["e2"]
    M, N = lib.radios_curvatura(PHI, a=a, e2=e2)
    M, N = float(M), float(N)
    P, n, t_N, t_E = punto_y_marco(PHI)
    assert np.isclose(_Q(P), 1.0) and np.isclose(np.linalg.norm(P - N * n - np.array([0, 0, P[2] - N * n[2]])), 0.0)
    r_paralelo = N * np.cos(PHI)
    assert np.isclose(r_paralelo, float(np.hypot(P[0], P[1])))

    fig, ax = nueva_figura(proyeccion_3d=True)
    ax.computed_zorder = False
    ax.view_init(elev=46, azim=-55)   # desde elev 22 el primer vertical se ve de canto
    ax.set_xlim(-LIMITE, LIMITE)
    ax.set_ylim(-LIMITE, LIMITE)
    ax.set_zlim(-LIMITE, LIMITE)
    ax.set_box_aspect((1.0, 1.0, 1.0), zoom=1.22)
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        eje.pane.set_facecolor(PALETA["paper"])
        eje.pane.set_edgecolor("#e4e1d8")
        eje._axinfo["grid"]["color"] = "#e4e1d8"
        eje._axinfo["grid"]["linewidth"] = 0.5
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([-1, 0, 1])
    ax.tick_params(colors=PALETA["gris"], labelsize=8, pad=-2)
    ax.set_xlabel("X", color=PALETA["gris"], labelpad=-6)
    ax.set_ylabel("Y", color=PALETA["gris"], labelpad=-6)
    ax.set_zlabel("Z", color=PALETA["gris"], labelpad=-6)

    # Elipsoide en malla tenue (latitud reducida β y longitud λ cada 15°) + eje polar + meridiano de P
    beta = np.linspace(-np.pi / 2, np.pi / 2, 73)
    lam = np.linspace(-np.pi, np.pi, 145)
    B, Lm = np.meshgrid(beta, lam, indexing="ij")
    ax.plot_wireframe(a * np.cos(B) * np.cos(Lm), a * np.cos(B) * np.sin(Lm), b * np.sin(B),
                      rstride=6, cstride=6, color=PALETA["gris"], alpha=0.28, linewidth=0.5, zorder=1)
    ax.plot([0, 0], [0, 0], [-b - 0.25, b + 0.25], "-.", color=PALETA["gris"], linewidth=0.8, zorder=2)
    meridiano = seccion_plana(P, t_N, n)
    ax.plot(meridiano[:, 0], meridiano[:, 1], meridiano[:, 2], "-", color=PALETA["teal"], alpha=0.35,
            linewidth=0.9, zorder=2)
    ecuador = circulo_3d(np.zeros(3), np.array([1.0, 0, 0]), np.array([0, 1.0, 0]), a)
    ax.plot(ecuador[:, 0], ecuador[:, 1], ecuador[:, 2], "-", color=PALETA["gris"], alpha=0.5,
            linewidth=0.7, zorder=2)

    # Plano (rectángulo), sección, círculo de curvatura, radio, normal y punto P
    plano = Poly3DCollection([rectangulo_plano(P, t_N, n)], facecolor=PALETA["gris"], alpha=0.16,
                             edgecolor=PALETA["gris"], linewidth=0.6, zorder=3)
    ax.add_collection3d(plano)
    seccion = ax.plot([], [], [], "-", color=PALETA["teal"], linewidth=2.0, zorder=5)[0]
    circulo = ax.plot([], [], [], "--", color=PALETA["teal"], linewidth=1.3, zorder=5)[0]
    radio = ax.plot([], [], [], "-", color=PALETA["teal"], linewidth=1.0, alpha=0.9, zorder=6)[0]
    centro = ax.plot([], [], [], "o", color=PALETA["teal"], markersize=4, zorder=6)[0]
    # La normal: del pie sobre el eje (a distancia N, por definición) hasta un poco por encima de P
    pie_N = P - N * n
    ax.plot([pie_N[0], P[0] + 0.35 * n[0]], [pie_N[1], P[1] + 0.35 * n[1]], [pie_N[2], P[2] + 0.35 * n[2]],
            "-", color=PALETA["tinta"], alpha=0.75, linewidth=1.2, zorder=6)
    punta = P + 0.44 * n
    ax.text(punta[0], punta[1], punta[2], "n", color=PALETA["tinta"], fontsize=11, zorder=9)
    ax.plot([P[0]], [P[1]], [P[2]], "o", color=PALETA["tinta"], markersize=5, zorder=7)
    ax.text(P[0] + 0.12, P[1] + 0.04, P[2] - 0.16, "P", color=PALETA["tinta"], fontsize=12, zorder=9)
    etiqueta_R = ax.text(0, 0, 0, "", color=PALETA["teal"], fontsize=11, zorder=9)

    rotulo(ax, "")
    titulo = ax.texts[-1]
    rotulo(ax, "", color=PALETA["gris"], y=0.905)
    detalle = ax.texts[-1]
    detalle.set_fontsize(11)
    ax.text2D(0.01, 0.855, f"elipsoide de revolución exagerado: a = 1, f = {F_EXAG} (GRS80: f ≈ 1/298);  "
                           f"P en φ = 40°;  M = {M:.3f} a,  N = {N:.3f} a,  N cos φ = {r_paralelo:.3f} a",
              transform=ax.transAxes, fontsize=10, color=PALETA["gris"], va="top", ha="left")

    for i, si in enumerate(s):
        e1, e2_ = etapas(float(si), 2)
        if e2_ <= 0.0:
            # Etapa 1 — Euler: plano normal en acimut α
            alfa = e1 * np.pi / 2
            d = np.cos(alfa) * t_N + np.sin(alfa) * t_E          # dirección tangente de la sección
            nu = -n                                              # hacia el centro de curvatura
            R = 1.0 / (np.cos(alfa) ** 2 / M + np.sin(alfa) ** 2 / N)
            color = _mezcla(PALETA["teal"], PALETA["rust"], e1)
            titulo.set_text("1. Euler: giramos el plano normal;  1/R = cos²α/M + sin²α/N")
            detalle.set_text(f"α = {np.rad2deg(alfa):4.0f}°   →   R(α) = {R:.3f} a"
                             + ("   (meridiano: R = M)" if e1 < 1e-9 else "")
                             + ("   (primer vertical: R = N)" if e1 > 1 - 1e-9 else ""))
            texto_R = f"R = {R:.3f} a"
        else:
            # Etapa 2 — Meusnier: el plano que contiene el este se inclina β desde la normal hacia el paralelo
            beta_ = e2_ * PHI
            d = t_E
            nu = -(np.cos(beta_) * n - np.sin(beta_) * t_N)      # normal de la curva dentro del plano (giro
            #                                                       de n alrededor de t_E; en β = φ es −X̂)
            R = N * np.cos(beta_)
            color = _mezcla(PALETA["rust"], PALETA["gold"], e2_)
            titulo.set_text("2. Meusnier: inclinamos el plano hasta el paralelo:  r = N cos φ")
            detalle.set_text(f"inclinación β = {np.rad2deg(beta_):4.0f}°   →   r = N cos β = {R:.3f} a"
                             + (f"   (β = φ: el paralelo, r = N cos φ = {r_paralelo:.3f} a)"
                                if e2_ > 1 - 1e-9 else ""))
            texto_R = f"r = {R:.3f} a"
        curva = seccion_plana(P, d, nu)
        C = P + R * nu
        circ = circulo_3d(C, d, nu, R)
        plano.set_verts([rectangulo_plano(P, d, -nu)])
        seccion.set_data_3d(curva[:, 0], curva[:, 1], curva[:, 2])
        seccion.set_color(color)
        circulo.set_data_3d(circ[:, 0], circ[:, 1], circ[:, 2])
        circulo.set_color(color)
        radio.set_data_3d([C[0], P[0]], [C[1], P[1]], [C[2], P[2]])
        radio.set_color(color)
        centro.set_data_3d([C[0]], [C[1]], [C[2]])
        centro.set_color(color)
        medio = P + 0.55 * R * nu
        etiqueta_R.set_position_3d((medio[0], medio[1] + 0.1, medio[2] + 0.08))
        etiqueta_R.set_text(texto_R)
        etiqueta_R.set_color(color)
        guardar_frame(fig, out_dir, i)
    plt.close(fig)
