"""Animación 01 — dualidad: la forma lineal ω se arrastra con A⁻¹ (no con A).

A(s) = (1 - s) I + s diag(2, 1) estira el plano en x. Los mojones (puntos) van con A; las rectas de nivel
de ω = (2, 1) van con ω' = ω A⁻¹, de modo que el mojón (1, 1) sigue clavado en la recta ω'x' = 3. La flecha
"ingenua" A ωᵀ pierde la perpendicularidad a las rectas de nivel; ω'ᵀ la conserva.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

from ._comun import PALETA, guardar_frame, nueva_figura, rotulo

OMEGA = np.array([2.0, 1.0])
P_MOJON = np.array([1.0, 1.0])
NIVELES = range(-6, 7)
XLIM, YLIM = (-6.0, 6.0), (-4.0, 4.0)


def A_de(s: float) -> np.ndarray:
    return (1.0 - s) * np.eye(2) + s * np.diag([2.0, 1.0])


# verificación: ω A⁻¹ (A p) = ω p para todo s (la forma arrastrada lee lo mismo sobre el punto arrastrado)
for _s in np.linspace(0.0, 1.0, 11):
    _A = A_de(_s)
    assert np.isclose(OMEGA @ np.linalg.inv(_A) @ (_A @ P_MOJON), OMEGA @ P_MOJON), _s


def _nube() -> np.ndarray:
    rng = np.random.default_rng(56798)
    return rng.uniform(-2.5, 2.5, size=(12, 2))


def _recta(omega: np.ndarray, k: float, t: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Puntos de la recta ω·x = k: pie k ω/|ω|² más la dirección perpendicular."""
    pie = k * omega / (omega @ omega)
    perp = np.array([-omega[1], omega[0]])
    pts = pie[None, :] + t[:, None] * perp[None, :]
    return pts[:, 0], pts[:, 1]


def render(out_dir: Path, s: np.ndarray) -> None:
    fig, ax = nueva_figura()
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=PALETA["gris"], lw=0.8, alpha=0.6)
    ax.axvline(0, color=PALETA["gris"], lw=0.8, alpha=0.6)

    t = np.linspace(-30.0, 30.0, 2)
    rectas = {}
    for k in NIVELES:
        destacada = (k == OMEGA @ P_MOJON)
        (ln,) = ax.plot([], [], color=PALETA["teal"], lw=2.4 if destacada else 1.4,
                        alpha=1.0 if destacada else 0.45, zorder=2)
        rectas[k] = ln
    etiqueta_k = ax.text(0, 0, "ω'x' = 3", color=PALETA["teal"], fontsize=11, zorder=6,
                         ha="left", va="bottom")

    nube = _nube()
    sc = ax.scatter(nube[:, 0], nube[:, 1], s=36, color=PALETA["violeta"], alpha=0.8, zorder=4)
    (mojon,) = ax.plot([], [], "o", ms=13, color=PALETA["violeta"], mec=PALETA["tinta"], mew=1.8, zorder=5)
    etiqueta_p = ax.text(0, 0, "A(1, 1)", color=PALETA["violeta"], fontsize=11, ha="left", va="top", zorder=6)

    fl_correcta = FancyArrowPatch((0, 0), (1, 1), color=PALETA["teal"], lw=2.4, arrowstyle="-|>",
                                  mutation_scale=18, zorder=7)
    fl_ingenua = FancyArrowPatch((0, 0), (1, 1), color=PALETA["rust"], lw=2.4, arrowstyle="-|>",
                                 mutation_scale=18, linestyle="--", zorder=7)
    ax.add_patch(fl_correcta)
    ax.add_patch(fl_ingenua)
    et_correcta = ax.text(0, 0, "ω'ᵀ = (ω A⁻¹)ᵀ", color=PALETA["teal"], fontsize=11, ha="left", va="bottom", zorder=8)
    et_ingenua = ax.text(0, 0, "A ωᵀ", color=PALETA["rust"], fontsize=11, ha="left", va="top", zorder=8)

    caja = dict(facecolor=PALETA["paper"], edgecolor="none", alpha=0.85, pad=3)
    rotulo(ax, "la forma lineal se arrastra con A⁻¹: el mojón (1, 1) sigue en la recta ω'x' = 3;\n"
               "la flecha A ωᵀ (rust) ya no es perpendicular")
    ax.texts[-1].set_bbox(caja)
    info = ax.text(0.01, 0.885, "", transform=ax.transAxes, fontsize=12, color=PALETA["tinta"], va="top",
                   ha="left", bbox=caja)
    angulo_txt = ax.text(0.99, 0.03, "", transform=ax.transAxes, fontsize=12, color=PALETA["rust"],
                         va="bottom", ha="right", bbox=caja)

    for i, si in enumerate(s):
        A = A_de(float(si))
        Ainv = np.linalg.inv(A)
        omega_p = OMEGA @ Ainv          # forma arrastrada: ω' x' = k
        for k, ln in rectas.items():
            ln.set_data(*_recta(omega_p, k, t))
        sc.set_offsets(nube @ A.T)
        p = A @ P_MOJON
        mojon.set_data([p[0]], [p[1]])
        etiqueta_p.set_position((p[0] + 0.15, p[1] - 0.15))
        pie3 = 3.0 * omega_p / (omega_p @ omega_p)
        perp = np.array([-omega_p[1], omega_p[0]]) / np.linalg.norm(omega_p)
        q = pie3 - 3.3 * perp                       # etiqueta sobre el tramo inferior de la recta destacada
        etiqueta_k.set_position((q[0] + 0.12, q[1] + 0.05))

        ingenua = A @ OMEGA
        fl_correcta.set_positions((0, 0), tuple(omega_p))
        fl_ingenua.set_positions((0, 0), tuple(ingenua))
        et_correcta.set_position((omega_p[0] + 0.1, omega_p[1] + 0.15))
        et_ingenua.set_position((ingenua[0] + 0.1, ingenua[1] - 0.15))

        cosang = (ingenua @ omega_p) / (np.linalg.norm(ingenua) * np.linalg.norm(omega_p))
        ang = np.degrees(np.arccos(np.clip(cosang, -1.0, 1.0)))
        info.set_text(f"A(s) = diag({1 + si:.2f}, 1),  s = {si:.2f};   ω = (2, 1),  ω' = ω A⁻¹ = "
                      f"({omega_p[0]:.2f}, {omega_p[1]:.2f})")
        angulo_txt.set_text(f"ángulo entre A ωᵀ y la normal a las rectas de nivel: {ang:.1f}°")
        guardar_frame(fig, out_dir, i)
    plt.close(fig)
