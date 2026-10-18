"""Figura del apunte: curvas de nivel del DEM de la Precordillera sobre Z y sobre aproximaciones de rango k (SVD).

Uso, desde la raíz del repo:  uv run python apunte/figuras/svd/gen_dem_curvas_nivel.py
Escribe apunte/figuras/svd/dem_curvas_nivel.png. Determinista (no usa aleatoriedad).
Datos: lib.dem_precordillera() de unidades/cb104.py, el mismo recorte 512×512 que usa la unidad 09.
"""

from pathlib import Path
import sys

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

RAIZ = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "unidades"))
import cb104 as lib  # noqa: E402

KS = (2, 5, 20)            # rangos que se muestran junto al original
EQUIDISTANCIA = 50.0       # m, la misma en los cuatro paneles
MAESTRA = 250.0            # m, curvas maestras (trazo más grueso)
DX, DY = 26.19, 30.80      # m por celda, este-oeste y norte-sur, a la latitud media del recorte

Z = lib.dem_precordillera().astype(float)
n_filas, n_cols = Z.shape
U, s, Vt = np.linalg.svd(Z, full_matrices=False)

niveles = np.arange(np.ceil(Z.min() / EQUIDISTANCIA) * EQUIDISTANCIA, Z.max(), EQUIDISTANCIA)
maestras = niveles[np.isclose(np.mod(niveles, MAESTRA), 0)]
normales = niveles[~np.isclose(np.mod(niveles, MAESTRA), 0)]
extent = (0, n_cols * DX / 1000, 0, n_filas * DY / 1000)  # km; fila 0 = norte arriba

plt.rcParams.update({"font.size": 11, "font.family": "serif", "axes.titlesize": 11})
fig, ejes = plt.subplots(2, 2, figsize=(7.2, 7.6), constrained_layout=True)
paneles = [("Z original (512 × 512)", Z)]
for k in KS:
    Zk = (U[:, :k] * s[:k]) @ Vt[:k]
    rms = float(np.sqrt(np.mean((Z - Zk) ** 2)))
    paneles.append((f"Z$_{{{k}}}$: rango {k}, RMS = {rms:.1f} m".replace(".", ","), Zk))

for ax, (titulo, F) in zip(ejes.ravel(), paneles):
    ax.imshow(F, cmap="Greys", vmin=Z.min() - 600, vmax=Z.max() + 200, extent=extent, origin="upper",
              interpolation="bilinear")
    ax.contour(F, levels=normales, colors="#1b6f6a", linewidths=0.45, extent=extent, origin="upper")
    cs = ax.contour(F, levels=maestras, colors="#123f3c", linewidths=1.1, extent=extent, origin="upper")
    ax.clabel(cs, fmt=lambda v: f"{v:.0f}", fontsize=7, inline=True, inline_spacing=2)
    ax.set_title(titulo)
    ax.set_xticks([0, 5, 10])
    ax.set_yticks([0, 5, 10, 15])
    ax.tick_params(labelsize=9, length=2.5, color="#777777")
    for borde in ax.spines.values():
        borde.set_color("#777777")
        borde.set_linewidth(0.6)
for ax in ejes[1]:
    ax.set_xlabel("este (km)", fontsize=10)
for ax in ejes[:, 0]:
    ax.set_ylabel("norte (km)", fontsize=10)

salida = Path(__file__).with_name("dem_curvas_nivel.png")
fig.savefig(salida, dpi=220)
print(f"escrito {salida.relative_to(RAIZ)}; niveles {niveles[0]:.0f}–{niveles[-1]:.0f} m cada {EQUIDISTANCIA:.0f} m")
