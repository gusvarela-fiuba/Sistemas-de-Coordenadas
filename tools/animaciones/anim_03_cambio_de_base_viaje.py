"""Animación 03 — el viaje del cambio de base: T = A T_diag A⁻¹ en tres etapas.

A = [v₁ | v₂] con v₁ = (1, 1), v₂ = (1, −1) y λ = (3, 1): T = A diag(3, 1) A⁻¹ = [[2, 1], [1, 2]] (lección 08).
(1) leemos p en la base de autovectores (c = A⁻¹ p), (2) estiramos cada dirección propia sin mezclar
(T_diag), (3) volvemos a la base canónica y leemos T p. Todo se dibuja en función de s: la vuelta deshace
las tres etapas en orden inverso.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from ._comun import PALETA, etapas, guardar_frame, nueva_figura, rotulo

V1 = np.array([1.0, 1.0])
V2 = np.array([1.0, -1.0])
A = np.column_stack([V1, V2])
LAMBDA = np.array([3.0, 1.0])
T = A @ np.diag(LAMBDA) @ np.linalg.inv(A)
assert np.allclose(T, [[2.0, 1.0], [1.0, 2.0]]), T

P = np.array([2.0, 0.5])
C = np.linalg.solve(A, P)          # c = A⁻¹ p = (1.25, 0.75)
TP = T @ P                         # T p = (4.5, 3)
assert np.allclose(C[0] * LAMBDA[0] * V1 + C[1] * LAMBDA[1] * V2, TP)

XLIM, YLIM = (-1.0, 6.0), (-2.0, 4.0)
ROTULOS = [
    "1. leemos p en la base de autovectores: c = A⁻¹ p",
    "2. estiramos cada dirección propia: λ₁ = 3, λ₂ = 1 (T_diag)",
    "3. volvemos a la base canónica: T p = A T_diag A⁻¹ p",
]


def render(out_dir: Path, s: np.ndarray) -> None:
    fig, ax = nueva_figura()
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect("equal", adjustable="box")

    # grilla canónica (fija, gris) y ejes
    for x in range(int(XLIM[0]), int(XLIM[1]) + 1):
        ax.axvline(x, color=PALETA["gris"], lw=0.8 if x else 1.4, alpha=0.5 if x else 0.9, zorder=1)
    for y in range(int(YLIM[0]), int(YLIM[1]) + 1):
        ax.axhline(y, color=PALETA["gris"], lw=0.8 if y else 1.4, alpha=0.5 if y else 0.9, zorder=1)

    # grilla oblicua: líneas paralelas a v1 (teal) indexadas por j (fijas) y paralelas a v2 (rust)
    # indexadas por i (se separan a lo largo de v1 en la etapa 2)
    t = np.array([-12.0, 12.0])
    lineas_v1 = []
    for j in range(-4, 6):
        base = j * V2
        pts = base[None, :] + t[:, None] * V1[None, :]
        (ln,) = ax.plot(pts[:, 0], pts[:, 1], color=PALETA["teal"], lw=1.6 if j else 2.4, zorder=2)
        lineas_v1.append(ln)
    lineas_v2 = []
    for i in range(-3, 7):
        (ln,) = ax.plot([], [], color=PALETA["rust"], lw=1.6 if i else 2.4, zorder=2)
        lineas_v2.append((i, ln))

    # descomposición de p: paralelogramo c1 v1 + c2 v2
    (seg_t1,) = ax.plot([], [], color=PALETA["teal"], lw=2.5, zorder=4)     # 0 -> c1 v1
    (seg_r1,) = ax.plot([], [], color=PALETA["rust"], lw=2.5, zorder=4)     # c1 v1 -> p
    (seg_r2,) = ax.plot([], [], color=PALETA["rust"], lw=1.6, ls="--", zorder=4)  # 0 -> c2 v2
    (seg_t2,) = ax.plot([], [], color=PALETA["teal"], lw=1.6, ls="--", zorder=4)  # c2 v2 -> p
    et_c1 = ax.text(0, 0, "", color=PALETA["teal"], fontsize=12, ha="center", va="bottom", zorder=6)
    et_c2 = ax.text(0, 0, "", color=PALETA["rust"], fontsize=12, ha="left", va="center", zorder=6)

    # punto, su fantasma de partida y lectura canónica de T p
    (fantasma,) = ax.plot([P[0]], [P[1]], "o", ms=10, mfc="none", mec=PALETA["violeta"], mew=1.6, zorder=5)
    (punto,) = ax.plot([], [], "o", ms=12, color=PALETA["violeta"], mec=PALETA["tinta"], mew=1.5, zorder=7)
    et_p = ax.text(0, 0, "", color=PALETA["violeta"], fontsize=12, ha="left", va="bottom", zorder=8)
    (lect_x,) = ax.plot([TP[0], TP[0]], [0, TP[1]], color=PALETA["violeta"], lw=1.6, ls=":", zorder=5)
    (lect_y,) = ax.plot([0, TP[0]], [TP[1], TP[1]], color=PALETA["violeta"], lw=1.6, ls=":", zorder=5)
    et_x = ax.text(TP[0], -0.12, f"{TP[0]:g}", color=PALETA["violeta"], fontsize=12, ha="center", va="top", zorder=8)
    et_y = ax.text(-0.12, TP[1], f"{TP[1]:g}", color=PALETA["violeta"], fontsize=12, ha="right", va="center", zorder=8)

    caja = dict(facecolor=PALETA["paper"], edgecolor="none", alpha=0.85, pad=3)
    rotulo(ax, "")
    titulo = ax.texts[-1]
    titulo.set_bbox(caja)
    info = ax.text(0.01, 0.92, "", transform=ax.transAxes, fontsize=12, color=PALETA["tinta"], va="top",
                   ha="left", bbox=caja)
    ax.text(0.99, 0.03, "v₁ = (1, 1), v₂ = (1, −1);  T = [[2, 1], [1, 2]]", transform=ax.transAxes,
            fontsize=11, color=PALETA["gris"], va="bottom", ha="right", bbox=caja)

    for i_frame, si in enumerate(s):
        a, b, c = etapas(float(si), 3)
        k = 0 if si < 1 / 3 else (1 if si < 2 / 3 else 2)
        titulo.set_text(ROTULOS[k])

        alfa_grilla = 0.75 * a * (1.0 - c)          # aparece en (1), se desvanece en (3)
        for ln in lineas_v1:
            ln.set_alpha(alfa_grilla)
        f = 1.0 + (LAMBDA[0] - 1.0) * b             # separación de las líneas rust a lo largo de v1
        for i, ln in lineas_v2:
            base = i * f * V1
            pts = base[None, :] + t[:, None] * V2[None, :]
            ln.set_data(pts[:, 0], pts[:, 1])
            ln.set_alpha(alfa_grilla)

        c1 = C[0] * f
        q = c1 * V1 + C[1] * V2                     # el punto: de p a T p sin mezclar direcciones
        alfa_desc = a * (1.0 - c)
        v_t1, v_r2 = c1 * V1, C[1] * V2
        seg_t1.set_data([0, v_t1[0]], [0, v_t1[1]])
        seg_r1.set_data([v_t1[0], q[0]], [v_t1[1], q[1]])
        seg_r2.set_data([0, v_r2[0]], [0, v_r2[1]])
        seg_t2.set_data([v_r2[0], q[0]], [v_r2[1], q[1]])
        for art in (seg_t1, seg_r1, seg_r2, seg_t2, et_c1, et_c2):
            art.set_alpha(alfa_desc)
        et_c1.set_text(f"c₁ v₁ = {c1:.2f} v₁" if b > 0 else f"c₁ v₁ = {C[0]:.2f} v₁")
        et_c1.set_position((v_t1[0] * 0.5 - 0.3, v_t1[1] * 0.5 + 0.2))
        et_c2.set_text(f"c₂ v₂ = {C[1]:.2f} v₂")
        et_c2.set_position((v_t1[0] + v_r2[0] * 0.5 + 0.12, v_t1[1] + v_r2[1] * 0.5))

        punto.set_data([q[0]], [q[1]])
        fantasma.set_alpha(0.9 if b > 0 else 0.0)
        et_p.set_position((q[0] + 0.15, q[1] + 0.12))
        et_p.set_text("p = (2, 0.5)" if b <= 0 else (f"T p = ({TP[0]:g}, {TP[1]:g})" if b >= 1 else ""))

        for art in (lect_x, lect_y, et_x, et_y):
            art.set_alpha(c)
        if k == 0:
            info.set_text(f"c = A⁻¹ p = ({C[0]:.2f}, {C[1]:.2f}):  p = c₁ v₁ + c₂ v₂")
        elif k == 1:
            info.set_text(f"T_diag c = (λ₁ c₁, λ₂ c₂) = ({c1:.2f}, {C[1]:.2f})   [u = {b:.2f}]")
        else:
            info.set_text(f"T p = λ₁ c₁ v₁ + λ₂ c₂ v₂ = ({TP[0]:g}, {TP[1]:g})")
        guardar_frame(fig, out_dir, i_frame)
    plt.close(fig)
