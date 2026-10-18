"""Animación 04 — SVD: A = U Σ Vᵀ lleva la circunferencia unidad a la elipse A·círculo en tres pasos.

A = [[2, 1], [0, 1]] (lección 09). (1) Vᵀ gira la entrada hasta que v₁, v₂ caen sobre los ejes
(interpolamos el ángulo), (2) Σ estira los ejes por σ₁, σ₂, (3) U gira la salida hasta la elipse final.
La meta (A·círculo) se dibuja siempre en gold punteado.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch

from unidades import cb104 as lib

from ._comun import PALETA, etapas, guardar_frame, nueva_figura, rotulo

A = np.array([[2.0, 1.0], [0.0, 1.0]])
U, SIGMA, VT = lib.svd2(A)
assert np.linalg.det(VT) > 0 and np.linalg.det(U) > 0, (np.linalg.det(VT), np.linalg.det(U))
assert np.allclose(U @ np.diag(SIGMA) @ VT, A)
THETA_V = float(np.arctan2(VT[0, 1], VT[0, 0]))   # v₁ = primera fila de Vᵀ; Vᵀ = R(−θ_v)
THETA_U = float(np.arctan2(U[1, 0], U[0, 0]))     # U = R(θ_u)
assert np.allclose(lib.rot2(-THETA_V), VT) and np.allclose(lib.rot2(THETA_U), U)

XLIM, YLIM = (-3.0, 3.0), (-2.2, 2.2)
ROTULOS = [
    "1. Vᵀ: giramos la entrada hasta los ejes",
    f"2. Σ: estiramos σ₁ = {SIGMA[0]:.2f}, σ₂ = {SIGMA[1]:.2f} sobre los ejes",
    "3. U: giramos la salida: A = U Σ Vᵀ",
]
ETIQUETAS = [("v₁", "v₂"), ("σ₁ e₁", "σ₂ e₂"), ("σ₁ u₁", "σ₂ u₂")]


def matriz(s: float) -> tuple[np.ndarray, tuple[float, float, float]]:
    a, b, c = etapas(s, 3)
    escala = np.diag(1.0 + (SIGMA - 1.0) * b)
    return lib.rot2(THETA_U * c) @ escala @ lib.rot2(-THETA_V * a), (a, b, c)


def render(out_dir: Path, s: np.ndarray) -> None:
    fig, ax = nueva_figura()
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal", adjustable="box")
    ax.axhline(0, color=PALETA["gris"], lw=0.8, alpha=0.6)
    ax.axvline(0, color=PALETA["gris"], lw=0.8, alpha=0.6)

    circ = lib.cerrar(lib.circulo(240))            # N×2
    meta = circ @ A.T
    ax.plot(meta[:, 0], meta[:, 1], color=PALETA["gold"], lw=2.0, ls=(0, (4, 3)), alpha=0.8, zorder=2)
    ax.text(meta[60, 0] + 0.08, meta[60, 1] + 0.08, "A·círculo", color=PALETA["gold"], fontsize=11, zorder=6)

    (curva,) = ax.plot([], [], color=PALETA["gris"], lw=2.4, zorder=3)
    marcas = lib.circulo(12)                       # 12 marcas sobre la circunferencia: se ve el giro
    sc = ax.scatter(marcas[:, 0], marcas[:, 1], s=22, color=PALETA["gris"], zorder=4)
    v = VT.T                                       # columnas v₁, v₂ (vectores singulares de entrada)
    fl1 = FancyArrowPatch((0, 0), (1, 0), color=PALETA["teal"], lw=2.5, arrowstyle="-|>", mutation_scale=20, zorder=7)
    fl2 = FancyArrowPatch((0, 0), (0, 1), color=PALETA["rust"], lw=2.5, arrowstyle="-|>", mutation_scale=20, zorder=7)
    ax.add_patch(fl1)
    ax.add_patch(fl2)
    et1 = ax.text(0, 0, "", color=PALETA["teal"], fontsize=12, ha="left", va="bottom", zorder=8)
    et2 = ax.text(0, 0, "", color=PALETA["rust"], fontsize=12, ha="left", va="bottom", zorder=8)

    caja = dict(facecolor=PALETA["paper"], edgecolor="none", alpha=0.85, pad=3)
    rotulo(ax, "")
    titulo = ax.texts[-1]
    titulo.set_bbox(caja)
    info = ax.text(0.01, 0.92, "", transform=ax.transAxes, fontsize=12, color=PALETA["tinta"], va="top",
                   ha="left", bbox=caja)
    ax.text(0.99, 0.03, f"A = [[2, 1], [0, 1]];  θ_v = {np.degrees(THETA_V):.1f}°, θ_u = {np.degrees(THETA_U):.1f}°",
            transform=ax.transAxes, fontsize=11, color=PALETA["gris"], va="bottom", ha="right", bbox=caja)

    for i, si in enumerate(s):
        M, (a, b, c) = matriz(float(si))
        k = 0 if si < 1 / 3 else (1 if si < 2 / 3 else 2)
        titulo.set_text(ROTULOS[k])
        pts = circ @ M.T
        curva.set_data(pts[:, 0], pts[:, 1])
        sc.set_offsets(marcas @ M.T)
        w1, w2 = M @ v[:, 0], M @ v[:, 1]
        fl1.set_positions((0, 0), tuple(w1))
        fl2.set_positions((0, 0), tuple(w2))
        e1, e2 = ETIQUETAS[k]
        et1.set_text(e1)
        et2.set_text(e2)
        et1.set_position((w1[0] + 0.08, w1[1] + 0.08))
        et2.set_position((w2[0] + 0.08, w2[1] + 0.08))
        if k == 0:
            info.set_text(f"R(−θ_v·u), u = {a:.2f}: los vectores singulares de entrada caen sobre e₁, e₂")
        elif k == 1:
            info.set_text(f"diag(1 + (σ₁−1)u, 1 + (σ₂−1)u), u = {b:.2f}: semiejes {1 + (SIGMA[0] - 1) * b:.2f} y "
                          f"{1 + (SIGMA[1] - 1) * b:.2f}")
        else:
            info.set_text(f"R(θ_u·u), u = {c:.2f}: la elipse cae sobre A·círculo; semiejes σ₁ u₁, σ₂ u₂")
        guardar_frame(fig, out_dir, i)
    plt.close(fig)
