"""Línea de tiempo ping-pong, paleta y figura HD comunes a las cinco animaciones."""
from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

PALETA = {
    "paper": "#FAF8F2",
    "teal": "#01696F",
    "rust": "#A84B2F",
    "gold": "#D19900",
    "violeta": "#7A4E9E",
    "gris": "#9AA0A6",
    "tinta": "#2b2b2b",
}

FPS = 60
ANCHO, ALTO = 1280, 720   # HD 16:9


def smoothstep(t: np.ndarray) -> np.ndarray:
    """Interpolación cosenoidal 0 -> 1 (velocidad nula en los extremos: el bucle no salta)."""
    return 0.5 * (1.0 - np.cos(np.pi * np.clip(t, 0.0, 1.0)))


def pingpong(seg_ida: float = 2.5, seg_pausa: float = 0.6, fps: int = FPS) -> np.ndarray:
    """s(t) para un ciclo completo: ida (0 -> 1), pausa en 1, vuelta (1 -> 0), pausa en 0."""
    n_ida = int(round(seg_ida * fps))
    n_pausa = int(round(seg_pausa * fps))
    ida = smoothstep(np.linspace(0.0, 1.0, n_ida, endpoint=False))
    return np.concatenate([ida, np.ones(n_pausa), ida[::-1], np.zeros(n_pausa)])


def etapas(s: float, n: int) -> list[float]:
    """Reparte s en [0, 1] en `n` etapas encadenadas: devuelve el avance (0..1) de cada una."""
    out = []
    for k in range(n):
        out.append(float(np.clip(s * n - k, 0.0, 1.0)))
    return out


def nueva_figura(proyeccion_3d: bool = False):
    """Figura 1280x720 con fondo paper y sin márgenes sobrantes."""
    fig = plt.figure(figsize=(ANCHO / 100, ALTO / 100), dpi=100, facecolor=PALETA["paper"])
    if proyeccion_3d:
        ax = fig.add_axes([0.02, 0.02, 0.96, 0.96], projection="3d")
        ax.set_facecolor(PALETA["paper"])
    else:
        ax = fig.add_axes([0.07, 0.09, 0.90, 0.84])
        ax.set_facecolor(PALETA["paper"])
        for lado in ("top", "right"):
            ax.spines[lado].set_visible(False)
        for lado in ("left", "bottom"):
            ax.spines[lado].set_color(PALETA["gris"])
        ax.tick_params(colors=PALETA["gris"], labelsize=9)
    return fig, ax


def guardar_frame(fig, out_dir: Path, i: int) -> None:
    fig.savefig(out_dir / f"frame_{i:04d}.png", dpi=100, facecolor=fig.get_facecolor())


def rotulo(ax, texto: str, color: str | None = None, x: float = 0.01, y: float = 0.985) -> None:
    """Rótulo superior izquierdo (en coordenadas de axes), sirve en 2D y 3D."""
    ax.text2D(x, y, texto, transform=ax.transAxes, fontsize=13, color=color or PALETA["tinta"],
              va="top", ha="left") if hasattr(ax, "text2D") else \
        ax.text(x, y, texto, transform=ax.transAxes, fontsize=13, color=color or PALETA["tinta"],
                va="top", ha="left")
