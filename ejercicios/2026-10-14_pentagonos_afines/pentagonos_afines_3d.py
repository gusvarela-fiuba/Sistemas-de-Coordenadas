#!/usr/bin/env python
"""
Transformaciones afines en 3D: pentágono plano inmerso en R³ y prisma
pentagonal, vistos con una cámara en perspectiva.

Port fiel a Python (numpy + matplotlib.animation.FuncAnimation) de
`julia/affine_pentagons_3d.jl` (Javis/Luxor). Mismas 6 fases, mismos
parámetros, mismos textos, 1280×720 a 30 fps, 50 frames por fase.

Convención de coordenadas: la de Luxor (píxeles, origen en el centro, eje y
hacia ABAJO; el eje y de matplotlib se invierte). En 3D el ojo está en
z = -d y los puntos con z mayor están más lejos y se ven más chicos:
proyección x' = x·d/(d+z), y' = y·d/(d+z).

El prisma se dibuja con el algoritmo del pintor (caras ordenadas de la más
lejana a la más cercana) e iluminación lambertiana contra una luz direccional.

Salidas (mismo nombre base que este script):
    pentagonos_afines_3d.mp4        1280×720, 30 fps (ffmpeg)
    pentagonos_afines_3d.gif        640×360, 15 fps (pillow)
    pentagonos_afines_3d_fases.png  lámina 2×3 con el frame central de cada fase

Correr:  uv run python pentagonos_afines_3d.py
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
DPI = 100
FRAMES_POR_FASE = 50
NUM_FASES = 6
TOTAL_FRAMES = NUM_FASES * FRAMES_POR_FASE  # 300 frames = 10 s

CENTRO_IZQ = np.array([-300.0, 40.0])
CENTRO_DER = np.array([300.0, 40.0])

D_CAMARA = 600.0  # distancia focal / distancia del ojo al origen
R = 120.0         # radio del pentágono
H = 90.0          # altura de extrusión del prisma
LARGO_EJES = 90.0

LUZ = np.array([0.5, -0.7, 1.0])
LUZ = LUZ / np.linalg.norm(LUZ)

AQUI = Path(__file__).resolve().parent
NOMBRE = Path(__file__).stem

FFMPEG = "/opt/homebrew/bin/ffmpeg"
FUENTE_SANS = ["Helvetica", "DejaVu Sans"]
FUENTE_MONO = ["Courier", "DejaVu Sans Mono"]  # Courier del sistema no tiene θ/φ/Δ


def px(v: float) -> float:
    """Píxeles (unidad de Luxor) → puntos tipográficos de matplotlib."""
    return v * 72.0 / DPI


# ==============================================================================
# Geometría pura (reutilizable en una unidad marimo)
# ==============================================================================
def pentagono_regular(R: float, n: int = 5) -> np.ndarray:
    """Vértices n×2 de un polígono regular de radio R, el primero 'arriba'."""
    ang = 2 * np.pi * np.arange(n) / n - np.pi / 2
    return np.column_stack([R * np.cos(ang), R * np.sin(ang)])


def pentagono_regular_3d(R: float, z: float = 0.0) -> np.ndarray:
    """El mismo pentágono inmerso en R³ sobre el plano z = cte (n×3)."""
    p = pentagono_regular(R)
    return np.column_stack([p, np.full(len(p), z)])


def prisma_pentagonal(R: float, H: float) -> tuple[np.ndarray, list[tuple[list[int], tuple]]]:
    """Prisma recto de base pentagonal: 10 vértices (base inferior z=-H/2,
    base superior z=+H/2) y 7 caras (índices 0-based + color RGB base).
    Los índices replican los del Julia (allí 1-based)."""
    vertices = np.vstack([pentagono_regular_3d(R, -H / 2), pentagono_regular_3d(R, +H / 2)])
    caras = [
        ([4, 3, 2, 1, 0], (0.15, 0.45, 0.85)),   # base inferior
        ([5, 6, 7, 8, 9], (0.25, 0.65, 1.00)),   # base superior
        ([0, 1, 6, 5], (0.95, 0.55, 0.20)),      # 5 caras laterales
        ([1, 2, 7, 6], (0.90, 0.45, 0.25)),
        ([2, 3, 8, 7], (0.85, 0.35, 0.30)),
        ([3, 4, 9, 8], (0.80, 0.40, 0.40)),
        ([4, 0, 5, 9], (0.90, 0.50, 0.30)),
    ]
    return vertices, caras


def aplicar(M: np.ndarray, puntos: np.ndarray) -> np.ndarray:
    """Aplica M (2×2 o 3×3) a una nube N×2 o N×3: cada fila p → M @ p."""
    return puntos @ M.T


def aplicar_afin(A: np.ndarray, b: np.ndarray, puntos: np.ndarray) -> np.ndarray:
    """T(x) = A·x + b fila a fila."""
    return aplicar(A, puntos) + b


def proyectar_perspectiva(puntos3d: np.ndarray, d: float = D_CAMARA) -> np.ndarray:
    """Cámara en perspectiva con el ojo en z = -d mirando hacia +z.
    Cada punto se escala por d/(d+z): más z (más lejos) → más chico.
    Devuelve N×2."""
    p = np.atleast_2d(puntos3d)
    s = d / (d + p[:, 2])
    return np.column_stack([p[:, 0] * s, p[:, 1] * s])


def suavizar(t: float) -> float:
    """Easing coseno, t ∈ [0, 1]."""
    t = float(np.clip(t, 0.0, 1.0))
    return 0.5 * (1.0 - np.cos(np.pi * t))


def rot_x(th: float) -> np.ndarray:
    c, s = np.cos(th), np.sin(th)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]], dtype=float)


def rot_y(th: float) -> np.ndarray:
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)


def rot_z(th: float) -> np.ndarray:
    c, s = np.cos(th), np.sin(th)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=float)


def normal_cara(p: np.ndarray) -> np.ndarray:
    """Normal unitaria de una cara plana dada por sus vértices (≥3, N×3), con
    el producto vectorial de las dos primeras aristas. Si es degenerada, +z."""
    n = np.cross(p[1] - p[0], p[2] - p[0])
    largo = np.linalg.norm(n)
    return n / largo if largo > 1e-6 else np.array([0.0, 0.0, 1.0])


# ==============================================================================
# Estado de la transformación 3D por frame (fases idénticas al Julia)
# ==============================================================================
def estado_afin_3d(frame: int) -> tuple[np.ndarray, np.ndarray, str, str]:
    """Devuelve (A 3×3, b 3, descripción, fórmula) para el frame 0-based."""
    fase = frame // FRAMES_POR_FASE + 1
    t_raw = (frame % FRAMES_POR_FASE) / (FRAMES_POR_FASE - 1)
    t = suavizar(t_raw)

    if fase == 1:
        # Fase 1: "identidad" vista desde una orientación fija (Rx·Ry leve) para
        # que se aprecie la profundidad. Nada se deforma.
        A = rot_x(0.35) @ rot_y(-0.45)
        b = np.zeros(3)
        desc = "1. Estado Inicial en R³ (Vista Perspectiva)"
        formula = "T(x) = I₃ · x + 0   |   Proyección a 2D: x' = (x·d)/(z+d)"

    elif fase == 2:
        # Fase 2: vuelta completa alrededor del eje Y. Isometría: R^T R = I,
        # det = 1; conserva distancias, ángulos y volumen.
        th_y = -0.45 + t * 2 * np.pi
        A = rot_x(0.35) @ rot_y(th_y)
        b = np.zeros(3)
        desc = "2. Rotación 3D alrededor del Eje Y: Ry(θ)"
        formula = f"θ_y = {np.degrees(t * 2 * np.pi):.1f}°  |  Matriz ortogonal: det(R) = 1, R^T R = I"

    elif fase == 3:
        # Fase 3: vuelta completa alrededor del eje X. El pentágono plano
        # muestra las dos caras (el sombreado cambia con la normal).
        th_x = 0.35 + t * 2 * np.pi
        A = rot_x(th_x) @ rot_y(-0.45)
        b = np.zeros(3)
        desc = "3. Rotación 3D alrededor del Eje X: Rx(φ)"
        formula = f"φ_x = {np.degrees(t * 2 * np.pi):.1f}°  |  Giro espacial que muestra ambas caras"

    elif fase == 4:
        # Fase 4: traslación en z (se acerca al ojo y vuelve). La geometría 3D
        # no cambia; cambia la escala APARENTE por la perspectiva. Las
        # paralelas de la escena ya no se proyectan paralelas.
        dz = -180.0 * np.sin(np.pi * t)
        A = rot_x(0.4) @ rot_y(-0.5)
        b = np.array([0.0, 0.0, dz])
        desc = "4. Traslación en Profundidad: Δz (Efecto Perspectiva)"
        formula = f"b = [0, 0, {dz:+.1f}]  |  Al variar Z cambia la escala aparente"

    elif fase == 5:
        # Fase 5: escalamiento anisotrópico. Conserva paralelismo y ortogonalidad
        # de los ejes, no los ángulos en general; razón de volúmenes = sx·sy·sz.
        sx = 1.0 - 0.35 * np.sin(np.pi * t)
        sy = 1.0 + 0.30 * np.sin(np.pi * t)
        sz = 1.0 + 0.90 * np.sin(np.pi * t)
        A = rot_x(0.4) @ rot_y(-0.5) @ np.diag([sx, sy, sz])
        b = np.zeros(3)
        desc = "5. Escalamiento No Uniforme 3D: S = Diag(sx, sy, sz)"
        formula = f"sx = {sx:.2f},  sy = {sy:.2f},  sz = {sz:.2f} (Deformación de volumen)"

    else:
        # Fase 6: cizallamiento 3D (x' = x + kx·y + kz·z) mientras gira media
        # vuelta. Conserva paralelismo y VOLUMEN (det = 1), no ángulos.
        kx = 0.65 * np.sin(np.pi * t)
        kz = 0.40 * np.sin(np.pi * t)
        shear = np.array([[1.0, kx, kz], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]])
        th_spin = 0.45 + t * np.pi
        A = rot_x(0.35) @ rot_y(th_spin) @ shear
        b = np.zeros(3)
        desc = "6. Cizallamiento 3D (Shear) + Rotación General"
        formula = f"Shear 3D: k_xy = {kx:.2f}, k_xz = {kz:.2f}  (Preserva volumen)"

    return A, b, desc, formula


def texto_matriz(A: np.ndarray, b: np.ndarray) -> str:
    """Bloque de 3 líneas con A (3×3) y b (3×1); en Luxor salía en una línea."""
    f = [[f"{A[i, j]:+.2f}" for j in range(3)] for i in range(3)]
    return (
        f"A (3x3) = [ {f[0][0]}  {f[0][1]}  {f[0][2]} ]          b (3x1) = [ {b[0]:+.1f} ]\n"
        f"          [ {f[1][0]}  {f[1][1]}  {f[1][2]} ]                    [ {b[1]:+.1f} ]\n"
        f"          [ {f[2][0]}  {f[2][1]}  {f[2][2]} ]                    [ {b[2]:+.1f} ]"
    )


# ==============================================================================
# Escena
# ==============================================================================
class Escena3D:
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

        for x in range(-640, 641, 80):
            ax.plot([x, x], [-360, 360], color="#161b22", lw=px(1), zorder=0)
        for y in range(-360, 361, 80):
            ax.plot([-640, 640], [y, y], color="#161b22", lw=px(1), zorder=0)

        ax.text(0, -315, "Transformaciones Afines en 3D:  T(x) = A · x + b",
                color="#58a6ff", fontsize=px(26), fontweight="bold",
                family=FUENTE_SANS, ha="center", va="baseline", zorder=5)
        self.t_desc = ax.text(0, -275, "", color="#f0883e", fontsize=px(20),
                              fontweight="bold", family=FUENTE_SANS,
                              ha="center", va="baseline", zorder=5)
        self.t_formula = ax.text(0, -245, "", color="#8b949e", fontsize=px(15),
                                 fontweight="bold", family=FUENTE_MONO,
                                 ha="center", va="baseline", zorder=5)
        self.t_matriz = ax.text(0, 280, "", color="#79c0ff", fontsize=px(13),
                                family=FUENTE_MONO, ha="center", va="center",
                                multialignment="left", linespacing=1.3, zorder=5)
        ax.plot([0, 0], [-210, 225], color="#21262d", lw=px(1.5), zorder=1)

        ax.text(*(CENTRO_IZQ + [0, -170]), "Pentágono Plano en R³", color="#7ee787",
                fontsize=px(17), fontweight="bold", family=FUENTE_SANS,
                ha="center", va="baseline", zorder=5)
        ax.text(*(CENTRO_DER + [0, -170]), "Prisma Pentagonal 3D (Extrusión)", color="#ffa657",
                fontsize=px(17), fontweight="bold", family=FUENTE_SANS,
                ha="center", va="baseline", zorder=5)

        # ejes locales (X rojo, Y verde, Z azul) en cada panel: se dibujan ANTES
        # de las figuras, como en el Julia (quedan tapados donde corresponde)
        self.ejes = [self._ejes(), self._ejes()]

        # --- panel izquierdo: pentágono plano
        self.penta_base = pentagono_regular_3d(R)
        self.penta_fill = Polygon(np.zeros((5, 2)), closed=True, edgecolor="none", zorder=10)
        self.penta_edge = Polygon(np.zeros((5, 2)), closed=True, fill=False,
                                  edgecolor="#58a6ff", lw=px(3), zorder=11)
        ax.add_patch(self.penta_fill)
        ax.add_patch(self.penta_edge)
        (self.normal_linea,) = ax.plot([], [], color="#e3b341", lw=px(2), zorder=12)
        (self.normal_punta,) = ax.plot([], [], "o", color="#e3b341", ms=px(6), zorder=12)
        (self.penta_v_out,) = ax.plot([], [], "o", color="#ffffff", ms=px(9), zorder=13)
        (self.penta_v_in,) = ax.plot([], [], "o", color="#1f6feb", ms=px(5), zorder=14)

        # --- panel derecho: prisma
        self.prisma_base, self.caras = prisma_pentagonal(R, H)
        self.cara_patches = []
        for idx, _ in self.caras:
            p = Polygon(np.zeros((len(idx), 2)), closed=True, edgecolor="#ffffff",
                        lw=px(1.5), zorder=20)
            ax.add_patch(p)
            self.cara_patches.append(p)
        (self.prisma_v_out,) = ax.plot([], [], "o", color="#ffffff", ms=px(7), zorder=30)
        (self.prisma_v_in,) = ax.plot([], [], "o", color="#ff7b72", ms=px(4), zorder=31)

    def _ejes(self):
        artistas = []
        for color, etiqueta in (("#ff5555", "X"), ("#55ff55", "Y"), ("#5599ff", "Z")):
            (linea,) = self.ax.plot([], [], color=color, lw=px(2), zorder=6)
            texto = self.ax.text(0, 0, etiqueta, color=color, fontsize=px(11),
                                 fontweight="bold", family=FUENTE_SANS,
                                 ha="left", va="baseline", zorder=6)
            artistas.append((linea, texto))
        return artistas

    def _actualizar_ejes(self, artistas, A, b, centro):
        p0 = proyectar_perspectiva(A @ np.zeros(3) + b)[0] + centro
        for (linea, texto), d in zip(artistas, LARGO_EJES * np.eye(3)):
            p1 = proyectar_perspectiva(A @ d + b)[0] + centro
            linea.set_data([p0[0], p1[0]], [p0[1], p1[1]])
            texto.set_position(p1 + [5, 5])

    def actualizar(self, frame: int):
        A, b, desc, formula = estado_afin_3d(frame)
        self.t_desc.set_text(desc)
        self.t_formula.set_text(formula)
        self.t_matriz.set_text(texto_matriz(A, b))
        self._actualizar_ejes(self.ejes[0], A, b, CENTRO_IZQ)
        self._actualizar_ejes(self.ejes[1], A, b, CENTRO_DER)

        # --- pentágono plano: sombreado por |n·L| (se ven ambas caras)
        v = aplicar_afin(A, b, self.penta_base)
        pts = proyectar_perspectiva(v) + CENTRO_IZQ
        n = normal_cara(v)
        difuso = float(np.clip(0.3 + 0.7 * abs(n @ LUZ), 0.25, 1.0))
        self.penta_fill.set_xy(pts)
        self.penta_fill.set_facecolor((0.12 * difuso, 0.43 * difuso, 0.92 * difuso, 0.75))
        self.penta_edge.set_xy(pts)
        centro3d = v.mean(axis=0)
        c2 = proyectar_perspectiva(centro3d)[0] + CENTRO_IZQ
        n2 = proyectar_perspectiva(centro3d + n * 50.0)[0] + CENTRO_IZQ
        self.normal_linea.set_data([c2[0], n2[0]], [c2[1], n2[1]])
        self.normal_punta.set_data([n2[0]], [n2[1]])
        self.penta_v_out.set_data(pts[:, 0], pts[:, 1])
        self.penta_v_in.set_data(pts[:, 0], pts[:, 1])

        # --- prisma: pintor (más lejos = mayor z, se dibuja primero) + Lambert
        vp = aplicar_afin(A, b, self.prisma_base)
        pp = proyectar_perspectiva(vp) + CENTRO_DER
        profundidades = [vp[idx, 2].mean() for idx, _ in self.caras]
        orden = np.argsort(profundidades)[::-1]  # z descendente
        for rango, k in enumerate(orden):
            idx, (r, g, bb) = self.caras[k]
            nk = normal_cara(vp[idx])
            dif = float(np.clip(0.25 + 0.75 * max(0.0, nk @ LUZ), 0.2, 1.0))
            patch = self.cara_patches[k]
            patch.set_xy(pp[idx])
            patch.set_facecolor((r * dif, g * dif, bb * dif, 0.88))
            patch.set_zorder(20 + rango)
        self.prisma_v_out.set_data(pp[:, 0], pp[:, 1])
        self.prisma_v_in.set_data(pp[:, 0], pp[:, 1])
        return (self.t_desc,)

    def frame_rgb(self, frame: int) -> np.ndarray:
        self.actualizar(frame)
        self.fig.canvas.draw()
        return np.asarray(self.fig.canvas.buffer_rgba())[..., :3].copy()


# ==============================================================================
# Salidas
# ==============================================================================
def lamina_fases(escena: Escena3D, destino: Path) -> None:
    """Grilla 2×3, un panel por fase a 640×360. En 3D el ÚLTIMO frame de cada
    fase vuelve al estado inicial (vueltas de 360° en 2–3, sin(π·t) en 4–6), así
    que se muestra el frame de mitad de fase (t = 0.5), donde el efecto es máximo."""
    w, h, gap = 640, 360, 8
    lienzo = Image.new("RGB", (3 * w + 4 * gap, 2 * h + 3 * gap), "#0d1117")
    for k in range(NUM_FASES):
        img = Image.fromarray(escena.frame_rgb(k * FRAMES_POR_FASE + FRAMES_POR_FASE // 2))
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


def animar(escena: Escena3D, frames) -> FuncAnimation:
    return FuncAnimation(escena.fig, escena.actualizar, frames=frames,
                         init_func=lambda: escena.actualizar(0), blit=False,
                         interval=1000 / FPS)


def main() -> int:
    escena = Escena3D()
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
    except Exception as e:
        ok_mp4 = False
        print(f"  [aviso] no se pudo escribir el mp4: {e}", file=sys.stderr)

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
