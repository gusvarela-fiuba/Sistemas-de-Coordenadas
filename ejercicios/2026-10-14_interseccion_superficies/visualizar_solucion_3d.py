# visualizar_solucion_3d.py — animación de cámara girando 360° alrededor de la escena
# (port con matplotlib de julia/visualizar_solucion_3d.jl, sección 4: el gif).
#
# La figura estática (perspectiva 3D + perfil X-Z) ya la genera visualizar_solucion.py
# (ilustracion_3d.png); acá sólo se agrega lo que el .jl tenía de más: el gif de rotación.
#
# Problema:
#   S1: paraboloide x² + y² + z = 1  =>  z = 1 - (x² + y²)
#   S2: plano secante vertical x + y = 1  =>  y = 1 - x
#   C = S1 ∩ S2: r(t) = (t, 1 - t, 2t - 2t²)
#   π: plano de referencia x - z = 0 (normal n = (1, 0, -1))
#   P = (1/4, 3/4, 3/8): punto de C donde la tangente T = r'(1/4) = (1, -1, 1) es paralela a π
#   (T · n = 1·1 + (-1)·0 + 1·(-1) = 0).
#
# Salida: ilustracion_3d_rotacion.gif (560×420, 60 cuadros a 20 fps, pillow writer; < 3 MB).
# Correr desde esta carpeta:  uv run python visualizar_solucion_3d.py
#
# ==============================================================================
# GUÍA DIDÁCTICA: ANIMACIONES 3D EN MATPLOTLIB (`FuncAnimation`)
# ==============================================================================
# En lugar de volver a dibujar las superficies en cada fotograma (lo que sería
# lento), `construir_grafico_3d(ax)` arma la escena 3D una sola vez y la función
# `cuadro(i)` únicamente actualiza el ángulo de la cámara con
# `ax.view_init(elev=24, azim=azimuts[i])`. `PillowWriter(fps=20)` ensambla los
# cuadros en un archivo `.gif` sin requerir herramientas externas.
# ==============================================================================

from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

print("=" * 70)
print(" Visualización 3D (matplotlib): Intersección de Superficies y Recta Tangente")
print("=" * 70)

# ==============================================================================
# 1. Definición matemática del problema
# ==============================================================================
P = np.array([0.25, 0.75, 0.375])
T = np.array([1.0, -1.0, 1.0])

# Curva C
t_vals = np.linspace(-0.25, 1.25, 150)
x_curve = t_vals
y_curve = 1.0 - t_vals
z_curve = 2.0 * t_vals - 2.0 * t_vals**2

# Recta tangente en P
s_vals = np.linspace(-0.55, 0.55, 100)
x_tan = P[0] + s_vals * T[0]
y_tan = P[1] + s_vals * T[1]
z_tan = P[2] + s_vals * T[2]

# Malla del paraboloide z = 1 - (x² + y²)
xp = np.linspace(-1.15, 1.15, 35)
X_parab, Y_parab = np.meshgrid(xp, xp)
Z_parab = 1.0 - (X_parab**2 + Y_parab**2)

# Malla del plano de referencia x - z = 0  =>  z = x
X_ref, Y_ref = np.meshgrid(np.linspace(-0.4, 1.2, 15), np.linspace(-0.4, 1.4, 15))
Z_ref = X_ref


# ==============================================================================
# 2. Construcción de la escena 3D (una sola vez; la animación sólo mueve la cámara)
# ==============================================================================
def construir_grafico_3d(ax, azim=45, elev=22):
    # 1. Paraboloide S1
    ax.plot_surface(X_parab, Y_parab, Z_parab, cmap="Blues", alpha=0.35, edgecolor="none")

    # 2. Plano de referencia π: x - z = 0 (z = x)
    ax.plot_surface(X_ref, Y_ref, Z_ref, color="purple", alpha=0.22, edgecolor="none")
    ax.plot([], [], [], color="purple", lw=6, alpha=0.4, label="Plano ref: x - z = 0")  # proxy para la leyenda

    # 3. Plano secante vertical S2: x + y = 1 (malla de líneas)
    for zv in np.linspace(-0.5, 1.1, 7):
        ax.plot([-0.4, 1.4], [1.4, -0.4], [zv, zv], color="orange", lw=1.2, alpha=0.6)
    for xv in np.linspace(-0.4, 1.4, 7):
        ax.plot([xv, xv], [1.0 - xv, 1.0 - xv], [-0.5, 1.1], color="orange", lw=1.2, alpha=0.6)

    # 4. Curva de intersección C
    ax.plot(x_curve, y_curve, z_curve, color="red", lw=3.5, label="Curva C = S1 ∩ S2")

    # 5. Recta tangente a C en P
    ax.plot(x_tan, y_tan, z_tan, color="forestgreen", lw=3, linestyle="--", label="Recta Tangente T=(1,-1,1)")

    # 6. Punto P
    ax.scatter([P[0]], [P[1]], [P[2]], color="black", s=40, label="P(1/4, 3/4, 3/8)")

    ax.set_title("Perspectiva 3D: Curva C, Recta Tangente y Planos", fontsize=10)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_xlim(-0.8, 1.5)
    ax.set_ylim(-0.6, 1.5)
    ax.set_zlim(-0.6, 1.2)
    ax.legend(loc="upper right", fontsize=7)
    ax.view_init(elev=elev, azim=azim)
    return ax


# ==============================================================================
# 3. Animación rotatoria 3D de 360°
# ==============================================================================
print("-> Generando animación rotatoria 3D de 360° con matplotlib...")
fig = plt.figure(figsize=(5.6, 4.2), dpi=100)   # 560×420 px
ax = fig.add_subplot(projection="3d")
construir_grafico_3d(ax, 0, 24)

azimuts = list(range(0, 360, 6))   # el .jl usa 0:4:356; acá paso de 6° para que el gif quede < 3 MB


def cuadro(i):
    ax.view_init(elev=24, azim=azimuts[i])
    return ()


anim = FuncAnimation(fig, cuadro, frames=len(azimuts), interval=50)
gif_path = Path(__file__).resolve().parent / "ilustracion_3d_rotacion.gif"
anim.save(gif_path, writer=PillowWriter(fps=20))
print(f"   ✓ Animación 3D guardada en: {gif_path.name} ({gif_path.stat().st_size / 1e6:.2f} MB)")

print("=" * 70)
print(" Proceso finalizado con éxito.")
print("=" * 70)
