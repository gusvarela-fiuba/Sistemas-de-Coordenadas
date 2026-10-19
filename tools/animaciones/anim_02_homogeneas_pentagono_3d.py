"""Animación 02 — coordenadas homogéneas en 3D: los puntos del plano son rayos por el origen y la lámina
z = 1 es la foto. Una homografía H mueve los rayos; su corte con la lámina deforma el pentágono
proyectivamente.

Elegimos la homografía "foto del dron inclinada" H = [[1, 0, 0], [0, 1, 0], [0, k, 1]] con k = 0.6: la del
pentágono (A y B fijas, C ↔ E) anula la tercera coordenada de A y B a mitad de la mezcla lineal
(1 − s) I + s H, o sea que esos vértices se van al infinito y el rayo cruza la lámina por el lado opuesto.
Con la del dron (H(s) p)_z = 1 + s k y ≥ 0.51 en todo el ciclo y el pentágono deformado queda dentro de
la lámina.
"""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import to_rgb
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

from unidades import cb104 as lib

from ._comun import PALETA, guardar_frame, nueva_figura, rotulo

K_DRON = 0.6
H_DRON = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, K_DRON, 1.0]])
LADO_LAMINA = 1.8          # la lámina es [-LADO, LADO]² a z = 1
EXTENSION_RAYO = 1.28      # los rayos siguen más allá de la lámina (en múltiplos de la altura z = 1)
LIMITE_XY = 1.95
LIMITE_Z = 1.45


def homografia_parcial(s: float) -> np.ndarray:
    """H(s) = (1 − s) I + s H: el camino recto en el espacio de matrices entre la identidad y H."""
    return (1.0 - s) * np.eye(3) + s * H_DRON


def vertices_en_lamina(P_hom: np.ndarray, Hs: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """(direcciones H(s) p, cortes con la lámina H(s) p / (H(s) p)_z) de los vértices homogéneos (N×3)."""
    q = P_hom @ Hs.T
    return q, q / q[:, 2:3]


def _mezcla(c1: str, c2: str, t: float) -> tuple[float, float, float]:
    a, b = np.array(to_rgb(c1)), np.array(to_rgb(c2))
    return tuple((1.0 - t) * a + t * b)


def verificar() -> None:
    """Chequeos numéricos de la consigna: ningún (H(s) p)_z se acerca a 0 y los cortes quedan en la lámina."""
    P_hom = lib.hom(lib.pentagono_ejemplo())
    z_min, xy_max = np.inf, 0.0
    for s in np.linspace(0.0, 1.0, 201):
        q, corte = vertices_en_lamina(P_hom, homografia_parcial(s))
        z_min = min(z_min, float(np.abs(q[:, 2]).min()))
        xy_max = max(xy_max, float(np.abs(corte[:, :2]).max()))
    assert z_min > 0.4, f"(H(s)p)_z se acerca a 0: mínimo {z_min:.3f}"
    assert xy_max < LADO_LAMINA, f"un vértice se sale de la lámina: |xy| máximo {xy_max:.3f}"
    esperado = lib.aplicar_proyectiva(lib.pentagono_ejemplo(), H_DRON)
    _, corte_1 = vertices_en_lamina(P_hom, homografia_parcial(1.0))
    assert np.allclose(corte_1[:, :2], esperado), "el corte con la lámina no coincide con aplicar_proyectiva"


def render(out_dir: Path, s: np.ndarray) -> None:
    verificar()
    P = lib.pentagono_ejemplo()              # 5×2, vértices A..E
    P_hom = lib.hom(P)                        # 5×3, (x, y, 1)
    letras = "ABCDE"

    fig, ax = nueva_figura(proyeccion_3d=True)
    ax.computed_zorder = False
    ax.view_init(elev=27, azim=-57)
    ax.set_xlim(-LIMITE_XY, LIMITE_XY)
    ax.set_ylim(-LIMITE_XY, LIMITE_XY)
    ax.set_zlim(0.0, LIMITE_Z)
    ax.set_box_aspect((1.0, 1.0, 0.62), zoom=1.16)
    for eje in (ax.xaxis, ax.yaxis, ax.zaxis):
        eje.pane.set_facecolor(PALETA["paper"])
        eje.pane.set_edgecolor("#e4e1d8")
        eje._axinfo["grid"]["color"] = "#e4e1d8"
        eje._axinfo["grid"]["linewidth"] = 0.5
    ax.set_xticks([-1, 0, 1])
    ax.set_yticks([-1, 0, 1])
    ax.set_zticks([0, 1])
    ax.tick_params(colors=PALETA["gris"], labelsize=8, pad=-2)
    ax.set_xlabel("x", color=PALETA["gris"], labelpad=-6)
    ax.set_ylabel("y", color=PALETA["gris"], labelpad=-6)
    ax.set_zlabel("z", color=PALETA["gris"], labelpad=-6)

    # Lámina z = 1 (la foto)
    L = LADO_LAMINA
    lamina = Poly3DCollection([[(-L, -L, 1), (L, -L, 1), (L, L, 1), (-L, L, 1)]],
                              facecolor=PALETA["gris"], alpha=0.14, edgecolor=PALETA["gris"],
                              linewidth=0.8, zorder=3)
    ax.add_collection3d(lamina)
    ax.text(L, -L, 1.0, "  lámina z = 1", color=PALETA["gris"], fontsize=10, zorder=9)

    # Origen O y pentágono original (referencia tenue, violeta)
    ax.plot([0], [0], [0], "o", color=PALETA["tinta"], markersize=5, zorder=2)
    ax.text(0.0, 0.0, -0.02, "O", color=PALETA["tinta"], fontsize=11, ha="right", va="top", zorder=9)
    orig = lib.cerrar(P)
    ax.plot(orig[:, 0], orig[:, 1], np.ones(len(orig)), "-", color=PALETA["violeta"], alpha=0.45,
            linewidth=1.0, zorder=4)
    rayos_orig = [ax.plot([0, x * EXTENSION_RAYO], [0, y * EXTENSION_RAYO], [0, EXTENSION_RAYO], "--",
                          color=PALETA["gris"], alpha=0.55, linewidth=0.8, zorder=1)[0] for x, y in P]
    del rayos_orig

    # Pentágono deformado (relleno interpolado violeta → rust) y sus rayos (teal), partidos en el tramo
    # bajo la lámina (dibujado debajo) y el tramo que la atraviesa (dibujado encima)
    poligono = Poly3DCollection([P_hom], facecolor=PALETA["violeta"], alpha=0.38,
                                edgecolor=PALETA["violeta"], linewidth=1.6, zorder=5)
    ax.add_collection3d(poligono)
    rayos_abajo = [ax.plot([0, 0], [0, 0], [0, 0], "-", color=PALETA["teal"], linewidth=1.5,
                           alpha=0.9, zorder=2)[0] for _ in range(5)]
    rayos_arriba = [ax.plot([0, 0], [0, 0], [0, 0], "-", color=PALETA["teal"], linewidth=1.5,
                            alpha=0.9, zorder=6)[0] for _ in range(5)]
    puntos = ax.plot(P_hom[:, 0], P_hom[:, 1], P_hom[:, 2], "o", color=PALETA["teal"], markersize=5,
                     zorder=7)[0]
    etiquetas = [ax.text(x, y, 1.0, f" {letra}", color=PALETA["tinta"], fontsize=11, zorder=9)
                 for (x, y), letra in zip(P, letras)]

    rotulo(ax, "los puntos son rayos por el origen; la lámina z = 1 es la foto:\n"
               "H mueve los rayos y el pentágono se deforma proyectivamente")
    rotulo(ax, "", color=PALETA["gris"], y=0.905)
    detalle = ax.texts[-1]
    detalle.set_fontsize(11)

    for i, si in enumerate(s):
        si = float(si)
        q, corte = vertices_en_lamina(P_hom, homografia_parcial(si))
        color = _mezcla(PALETA["violeta"], PALETA["rust"], si)
        poligono.set_verts([corte])
        poligono.set_facecolor((*color, 0.38))
        poligono.set_edgecolor((*color, 1.0))
        for k in range(5):
            x, y = corte[k, 0], corte[k, 1]
            rayos_abajo[k].set_data_3d([0, x], [0, y], [0, 1])
            rayos_arriba[k].set_data_3d([x, x * EXTENSION_RAYO], [y, y * EXTENSION_RAYO],
                                        [1, EXTENSION_RAYO])
            etiquetas[k].set_position_3d((x, y, 1.0))
        puntos.set_data_3d(corte[:, 0], corte[:, 1], corte[:, 2])
        detalle.set_text(f"H(s) = (1 − s) I + s H,  s = {si:.2f};   H = [[1, 0, 0], [0, 1, 0], [0, k, 1]], "
                         f"k = {K_DRON} (la foto inclinada del dron)")
        guardar_frame(fig, out_dir, i)
    plt.close(fig)
