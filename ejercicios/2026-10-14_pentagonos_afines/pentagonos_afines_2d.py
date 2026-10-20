#!/usr/bin/env python
"""
Transformaciones afines en 2D sobre dos pentágonos (regular e irregular).

Port fiel a Python (numpy + matplotlib.animation.FuncAnimation) de
`julia/affine_pentagons.jl` (Javis/Luxor). Mismas 6 fases, mismos parámetros,
mismos textos, 1280×720 a 30 fps, 60 frames por fase.

Convención de coordenadas: se conserva la de Luxor (píxeles, origen en el
centro de la pantalla, eje y hacia ABAJO). Por eso el eje y de matplotlib se
invierte: lo que el Julia dibuja con y = -60 queda arriba, igual que en el gif
de referencia. Una rotación con θ > 0 se ve en pantalla en sentido horario.

Salidas (mismo nombre base que este script):
    pentagonos_afines_2d.mp4        1280×720, 30 fps (ffmpeg)
    pentagonos_afines_2d.gif        640×360, 15 fps (pillow)
    pentagonos_afines_2d_fases.png  lámina 2×3 con el último frame de cada fase

Correr:  uv run python pentagonos_afines_2d.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FFMpegWriter, FuncAnimation, PillowWriter  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402
from PIL import Image  # noqa: E402

# ==============================================================================
# Configuración y parámetros (idénticos al Julia)
# ==============================================================================
ANCHO, ALTO, FPS = 1280, 720, 30
DPI = 100  # 12.8 in × 7.2 in a 100 dpi = 1280 × 720 px
FRAMES_POR_FASE = 60
NUM_FASES = 6
TOTAL_FRAMES = NUM_FASES * FRAMES_POR_FASE  # 360 frames = 12 s

CENTRO_IZQ = np.array([-300.0, 40.0])
CENTRO_DER = np.array([300.0, 40.0])

R = 110.0  # radio del pentágono regular, en px

AQUI = Path(__file__).resolve().parent
NOMBRE = Path(__file__).stem

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FUENTE_SANS = ["Helvetica", "DejaVu Sans"]
FUENTE_MONO = ["Courier", "DejaVu Sans Mono"]  # Courier del sistema no tiene θ/φ/Δ


def px(v: float) -> float:
    """Convierte píxeles (unidad de Luxor) a puntos tipográficos de matplotlib."""
    return v * 72.0 / DPI


# ==============================================================================
# GUÍA DIDÁCTICA DE PYTHON Y NUMPY PARA ESTUDIAR ESTE SCRIPT
# ==============================================================================
# 1. Transformación vectorizada de una nube de puntos (`puntos @ M.T`):
#    Guardamos los N vértices de un polígono en una matriz `puntos` de forma
#    `(N, 2)`, donde cada fila es un punto `(x, y)`. Si en el papel escribimos
#    vectores columna `x' = A x + b`, para transformar todas las filas a la vez
#    en NumPy multiplicamos a derecha por la transpuesta: `puntos @ A.T + b`.
#    Por *broadcasting*, NumPy suma el vector `b` (de largo 2) a cada una de
#    las N filas automáticamente.
#
# 2. Fórmula del agrimensor con `np.roll` (`area_poligono`):
#    `np.roll(y, -1)` desplaza circularmente el vector `y` un lugar hacia la
#    izquierda (`[y1, y2, ..., y0]`), lo que permite calcular la suma de
#    productos cruzados `x_i y_{i+1} - y_i x_{i+1}` con dos productos internos
#    (`np.dot`) sin escribir ningún bucle `for`.
#
# 3. División entera `//` y resto `%` en `estado_afin`:
#    Con índices que arrancan en 0 (`frame` de 0 a 359) y 60 cuadros por fase,
#    `frame // 60` da el índice de fase (0 a 5) y `frame % 60` da el cuadro
#    dentro de esa fase (0 a 59).
# ==============================================================================


# ==============================================================================
# Geometría pura (reutilizable en una unidad marimo)
# ==============================================================================
def pentagono_regular(R: float, n: int = 5) -> np.ndarray:
    """Vértices (n×2) de un polígono regular de radio R, el primero 'arriba'
    (ángulo -π/2 en coordenadas de pantalla con y hacia abajo)."""
    ang = 2 * np.pi * np.arange(n) / n - np.pi / 2
    return np.column_stack([R * np.cos(ang), R * np.sin(ang)])


def pentagono_irregular() -> np.ndarray:
    """Cinco vértices asimétricos pero claramente distinguibles (del Julia)."""
    return np.array([
        [0.0, -115.0],    # superior
        [125.0, -35.0],   # derecho superior
        [85.0, 110.0],    # derecho inferior
        [-70.0, 95.0],    # izquierdo inferior
        [-120.0, -15.0],  # izquierdo
    ])


def aplicar(M: np.ndarray, puntos: np.ndarray) -> np.ndarray:
    """Aplica la matriz M (2×2 o 3×3) a una nube de puntos N×2 o N×3.
    Cada fila p se transforma como M @ p; vectorizado es puntos @ M.T."""
    return puntos @ M.T


def aplicar_afin(A: np.ndarray, b: np.ndarray, puntos: np.ndarray) -> np.ndarray:
    """T(x) = A·x + b sobre cada fila de `puntos`."""
    return aplicar(A, puntos) + b


def suavizar(t: float) -> float:
    """Easing coseno (smoothstep): arranca y frena suave, t ∈ [0, 1]."""
    t = float(np.clip(t, 0.0, 1.0))
    return 0.5 * (1.0 - np.cos(np.pi * t))


def rotacion(theta: float) -> np.ndarray:
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def escala(sx: float, sy: float) -> np.ndarray:
    return np.diag([sx, sy])


def cizalla_x(kx: float) -> np.ndarray:
    """Shear horizontal: x' = x + kx·y, y' = y."""
    return np.array([[1.0, kx], [0.0, 1.0]])


def area_poligono(p: np.ndarray) -> float:
    """Fórmula del cordón (shoelace); útil para verificar det(A) = razón de áreas."""
    x, y = p[:, 0], p[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


# ==============================================================================
# Estado de la transformación afín por frame (fases idénticas al Julia)
# ==============================================================================
def estado_afin(frame: int) -> tuple[np.ndarray, np.ndarray, str, str]:
    """Devuelve (A 2×2, b 2, descripción, fórmula) para el frame 0-based."""
    fase = frame // FRAMES_POR_FASE + 1
    t_raw = (frame % FRAMES_POR_FASE) / (FRAMES_POR_FASE - 1)
    t = suavizar(t_raw)
    I2 = np.eye(2)

    if fase == 1:
        # Fase 1: identidad. Todo se conserva: es la referencia.
        A, b = I2, np.zeros(2)
        desc = "1. Estado Inicial (Identidad)"
        formula = "T(x) = I · x + 0"

    elif fase == 2:
        # Fase 2: traslación pura. Conserva forma, tamaño, ángulos y orientación;
        # sólo cambia la posición (A = I, b ≠ 0). No es lineal: T(0) ≠ 0.
        b = t * np.array([0.0, -60.0])  # y negativo = hacia arriba en pantalla
        A = I2
        desc = "2. Traslación Pura: b = [Δx, Δy]"
        formula = f"T(x) = x + [{b[0]:.1f}, {b[1]:.1f}]"

    elif fase == 3:
        # Fase 3: rotación de 0 a 72° (= 2π/5, el pentágono regular vuelve a sí mismo).
        # Isometría: conserva distancias, ángulos y áreas; det(A) = 1.
        theta = t * (2 * np.pi / 5)
        A, b = rotacion(theta), np.zeros(2)
        desc = "3. Rotación Pura: R(θ)"
        formula = f"θ = {np.degrees(theta):.1f}° | Preserva distancias y ángulos"

    elif fase == 4:
        # Fase 4: escalamiento no uniforme sx = 1.35, sy = 0.65. Conserva el
        # paralelismo y la dirección de los ejes, NO los ángulos ni las distancias.
        # Razón de áreas = det(A) = sx·sy.
        sx, sy = 1.0 + t * 0.35, 1.0 - t * 0.35
        A, b = escala(sx, sy), np.zeros(2)
        desc = "4. Escalamiento No Uniforme: Diag(sx, sy)"
        formula = f"sx = {sx:.2f},  sy = {sy:.2f} (Deforma proporciones)"

    elif fase == 5:
        # Fase 5: cizallamiento horizontal kx de 0 a 0.65. Conserva paralelismo
        # y ÁREA (det = 1) pero no ángulos ni longitudes.
        kx = t * 0.65
        A, b = cizalla_x(kx), np.zeros(2)
        desc = "5. Cizallamiento (Shear): Preserva paralelismo pero no ángulos"
        formula = f"Matriz Shear: [1.0  {kx:.2f}; 0.0  1.0]"

    else:
        # Fase 6: afín general = interpolación entre I y (rotación · escala-shear),
        # más traslación. Única propiedad que sobrevive: rectas → rectas y
        # paralelismo; razón de áreas = det(A).
        theta = 0.4 * t
        R_mat = rotacion(theta)
        S_mat = np.array([[1.0 + 0.2 * t, 0.4 * t], [0.0, 1.0 - 0.2 * t]])
        A = (1 - t) * I2 + t * (R_mat @ S_mat)
        b = t * np.array([30.0, -35.0])
        desc = "6. Transformación Afín General: A · x + b"
        formula = "Transformación lineal combinada + desplazamiento"

    return A, b, desc, formula


def texto_matriz(A: np.ndarray, b: np.ndarray) -> str:
    """Bloque de 3 líneas con A y b (el Julia lo escribía así, pero Luxor no
    interpreta '\\n' y lo mostraba en una sola línea; acá sí sale en bloque)."""
    return (
        f"    [ {A[0, 0]:+.2f}  {A[0, 1]:+.2f} ]          [ {b[0]:+.1f} ]\n"
        f"A = [               ]    b = [        ]\n"
        f"    [ {A[1, 0]:+.2f}  {A[1, 1]:+.2f} ]          [ {b[1]:+.1f} ]"
    )


# ==============================================================================
# Escena: figura en coordenadas de píxel (y hacia abajo) + artistas actualizables
# ==============================================================================
class Escena2D:
    def __init__(self) -> None:
        self.fig = plt.figure(figsize=(ANCHO / DPI, ALTO / DPI), dpi=DPI)
        self.fig.patch.set_facecolor("#0d1117")
        ax = self.fig.add_axes([0, 0, 1, 1])
        ax.set_xlim(-ANCHO / 2, ANCHO / 2)
        ax.set_ylim(ALTO / 2, -ALTO / 2)  # y invertido: convención Luxor
        ax.set_aspect("equal")
        ax.set_axis_off()
        ax.set_facecolor("#0d1117")
        self.ax = ax

        # --- fondo: rejilla sutil cada 80 px
        for x in range(-640, 641, 80):
            ax.plot([x, x], [-360, 360], color="#161b22", lw=px(1), zorder=0)
        for y in range(-360, 361, 80):
            ax.plot([-640, 640], [y, y], color="#161b22", lw=px(1), zorder=0)

        # --- UI estática
        ax.text(0, -315, "Transformaciones Afines en 2D:  T(x) = A · x + b",
                color="#58a6ff", fontsize=px(26), fontweight="bold",
                family=FUENTE_SANS, ha="center", va="baseline", zorder=5)
        self.t_desc = ax.text(0, -275, "", color="#f0883e", fontsize=px(20),
                              fontweight="bold", family=FUENTE_SANS,
                              ha="center", va="baseline", zorder=5)
        self.t_formula = ax.text(0, -245, "", color="#8b949e", fontsize=px(15),
                                 fontweight="bold", family=FUENTE_MONO,
                                 ha="center", va="baseline", zorder=5)
        self.t_matriz = ax.text(0, 280, "", color="#79c0ff", fontsize=px(14),
                                family=FUENTE_MONO, ha="center", va="center",
                                multialignment="left", linespacing=1.3, zorder=5)
        ax.plot([0, 0], [-210, 230], color="#21262d", lw=px(1.5), zorder=1)

        # --- los dos paneles
        self.reg = self._panel(CENTRO_IZQ, pentagono_regular(R), "Pentágono Regular",
                               "#7ee787", (0.12, 0.43, 0.92, 0.25), "#58a6ff", "#1f6feb")
        self.irr = self._panel(CENTRO_DER, pentagono_irregular(), "Pentágono Irregular",
                               "#ffa657", (0.85, 0.40, 0.10, 0.25), "#ff7b72", "#ff7b72")

    def _panel(self, centro, base, etiqueta, color_et, relleno, borde, punto):
        ax = self.ax
        cx, cy = centro
        # ejes locales
        ax.plot([cx - 150, cx + 150], [cy, cy], color="#30363d", lw=px(1), zorder=2)
        ax.plot([cx, cx], [cy - 150, cy + 150], color="#30363d", lw=px(1), zorder=2)
        ax.text(cx, cy - 165, etiqueta, color=color_et, fontsize=px(17),
                fontweight="bold", family=FUENTE_SANS, ha="center", va="baseline", zorder=5)
        # figura original "fantasma"
        ax.add_patch(Polygon(base + centro, closed=True, fill=False, edgecolor="#38444d",
                             lw=px(1.5), linestyle=(0, (4, 4)), zorder=3))
        # figura transformada: relleno + borde + vértices (blanco afuera, color adentro)
        p_fill = Polygon(base + centro, closed=True, facecolor=relleno, edgecolor="none", zorder=4)
        p_edge = Polygon(base + centro, closed=True, fill=False, edgecolor=borde, lw=px(3), zorder=5)
        ax.add_patch(p_fill)
        ax.add_patch(p_edge)
        (v_out,) = ax.plot([], [], "o", color="#ffffff", ms=px(9), zorder=6)
        (v_in,) = ax.plot([], [], "o", color=punto, ms=px(5), zorder=7)
        return dict(centro=centro, base=base, fill=p_fill, edge=p_edge, v_out=v_out, v_in=v_in)

    def actualizar(self, frame: int):
        A, b, desc, formula = estado_afin(frame)
        self.t_desc.set_text(desc)
        self.t_formula.set_text(formula)
        self.t_matriz.set_text(texto_matriz(A, b))
        for panel in (self.reg, self.irr):
            pts = aplicar_afin(A, b, panel["base"]) + panel["centro"]
            panel["fill"].set_xy(pts)
            panel["edge"].set_xy(pts)
            panel["v_out"].set_data(pts[:, 0], pts[:, 1])
            panel["v_in"].set_data(pts[:, 0], pts[:, 1])
        return (self.t_desc, self.t_formula, self.t_matriz)

    def frame_rgb(self, frame: int) -> np.ndarray:
        """Renderiza un frame a un array H×W×3 (para la lámina estática)."""
        self.actualizar(frame)
        self.fig.canvas.draw()
        return np.asarray(self.fig.canvas.buffer_rgba())[..., :3].copy()


# ==============================================================================
# Salidas
# ==============================================================================
def lamina_fases(escena: Escena2D, destino: Path) -> None:
    """Grilla 2×3 con el último frame de cada fase, cada panel a 640×360."""
    w, h, gap = 640, 360, 8
    lienzo = Image.new("RGB", (3 * w + 4 * gap, 2 * h + 3 * gap), "#0d1117")
    for k in range(NUM_FASES):
        img = Image.fromarray(escena.frame_rgb((k + 1) * FRAMES_POR_FASE - 1))
        img = img.resize((w, h), Image.LANCZOS)
        fila, col = divmod(k, 3)
        lienzo.paste(img, (gap + col * (w + gap), gap + fila * (h + gap)))
    lienzo.save(destino)


class GifWriter(PillowWriter):
    """PillowWriter con duraciones en múltiplos de 10 ms (límite del formato GIF).
    int(1000/15) = 66 ms se truncaría a 60 ms (16.7 fps, animación 8 % más corta);
    el patrón 70/70/60 promedia 66.7 ms = 15 fps exactos y conserva la duración total."""

    def finish(self):
        n = len(self._frames)
        dur = ([70, 70, 60] * (n // 3 + 1))[:n]
        self._frames[0].save(self.outfile, save_all=True, append_images=self._frames[1:],
                             duration=dur, loop=0)


def animar(escena: Escena2D, frames) -> FuncAnimation:
    return FuncAnimation(escena.fig, escena.actualizar, frames=frames,
                         init_func=lambda: escena.actualizar(0), blit=False,
                         interval=1000 / FPS)


def main() -> int:
    escena = Escena2D()
    salida_mp4 = AQUI / f"{NOMBRE}.mp4"
    salida_gif = AQUI / f"{NOMBRE}.gif"
    salida_png = AQUI / f"{NOMBRE}_fases.png"

    print(f"Lámina de fases -> {salida_png.name}")
    lamina_fases(escena, salida_png)

    print(f"MP4 {ANCHO}x{ALTO} @ {FPS} fps, {TOTAL_FRAMES} frames -> {salida_mp4.name}")
    ok_mp4 = True
    try:
        matplotlib.rcParams["animation.ffmpeg_path"] = FFMPEG
        writer = FFMpegWriter(fps=FPS, codec="libx264",
                              extra_args=["-pix_fmt", "yuv420p", "-crf", "20"])
        animar(escena, range(TOTAL_FRAMES)).save(salida_mp4, writer=writer, dpi=DPI)
    except Exception as e:  # ffmpeg ausente o roto: seguimos con el gif
        ok_mp4 = False
        print(f"  [aviso] no se pudo escribir el mp4: {e}", file=sys.stderr)

    # GIF reducido: mitad de resolución (dpi 50 -> 640×360) y mitad de fps (15)
    fps_gif = 15
    print(f"GIF 640x360 @ {fps_gif} fps -> {salida_gif.name}")
    animar(escena, range(0, TOTAL_FRAMES, FPS // fps_gif)).save(
        salida_gif, writer=GifWriter(fps=fps_gif), dpi=DPI // 2)

    for p in (salida_mp4, salida_gif, salida_png):
        if p.exists():
            print(f"  {p.name}: {p.stat().st_size / 1e6:.2f} MB")
    return 0 if ok_mp4 else 2


if __name__ == "__main__":
    sys.exit(main())
