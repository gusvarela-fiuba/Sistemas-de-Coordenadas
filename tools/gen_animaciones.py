#!/usr/bin/env python
"""Genera las seis animaciones ping-pong del curso en mp4 (60 fps HD, sin controles) y gif (paleta
optimizada, 600 px) con ffmpeg, en `animaciones/` (versionada) y en `site/animaciones/` si existe.

    uv run python tools/gen_animaciones.py            # las seis
    uv run python tools/gen_animaciones.py --only 03  # una sola (por prefijo)
    uv run python tools/gen_animaciones.py --rapido   # 20 fps, para probar

Cada animación es un módulo de tools/animaciones/ con `render(out_dir, s)` que escribe un PNG por
valor de la línea de tiempo `s` (ida 0 -> 1, pausa, vuelta 1 -> 0, pausa: el bucle es continuo).
"""
from __future__ import annotations

import argparse
import importlib
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "tools"))
sys.path.insert(0, str(RAIZ))          # para `import unidades.cb104` desde las animaciones

from animaciones._comun import FPS, pingpong  # noqa: E402

FFMPEG = "/opt/homebrew/bin/ffmpeg"
ANIMACIONES = [
    "01_dualidad_gradiente",
    "02_homogeneas_pentagono_3d",
    "03_cambio_de_base_viaje",
    "04_svd_circulo_a_elipse",
    "05_elipsoide_euler_meusnier",
    "06_conforme_tissot_mercator",
]
DESTINO = RAIZ / "animaciones"
SITE = RAIZ / "site" / "animaciones"


def codificar(frames: Path, nombre: str, fps: int) -> tuple[Path, Path]:
    DESTINO.mkdir(exist_ok=True)
    mp4 = DESTINO / f"{nombre}.mp4"
    gif = DESTINO / f"{nombre}.gif"
    entrada = ["-framerate", str(fps), "-i", str(frames / "frame_%04d.png")]
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", *entrada,
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", "-preset", "slow",
                    "-movflags", "+faststart", str(mp4)], check=True)
    fps_gif = 20
    filtro = f"fps={fps_gif},scale=600:-1:flags=lanczos"
    with tempfile.TemporaryDirectory() as tmp:
        paleta = Path(tmp) / "paleta.png"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", *entrada,
                        "-vf", f"{filtro},palettegen=stats_mode=diff", str(paleta)], check=True)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", *entrada, "-i", str(paleta),
                        "-lavfi", f"{filtro} [x]; [x][1:v] paletteuse=dither=bayer:bayer_scale=5",
                        "-loop", "0", str(gif)], check=True)
    return mp4, gif


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--only", help="prefijo de la animación (p. ej. 03)")
    ap.add_argument("--rapido", action="store_true", help="20 fps en vez de 60, para probar")
    args = ap.parse_args()
    fps = 20 if args.rapido else FPS
    s = pingpong(fps=fps)
    nombres = [n for n in ANIMACIONES if not args.only or n.startswith(args.only)]
    if not nombres:
        print(f"ninguna animación empieza con {args.only!r}", file=sys.stderr)
        return 1
    for nombre in nombres:
        t0 = time.perf_counter()
        mod = importlib.import_module(f"animaciones.anim_{nombre}")
        with tempfile.TemporaryDirectory() as tmp:
            frames = Path(tmp)
            mod.render(frames, s)
            n = len(list(frames.glob("frame_*.png")))
            if n != len(s):
                raise RuntimeError(f"{nombre}: {n} frames, se esperaban {len(s)}")
            mp4, gif = codificar(frames, nombre, fps)
        if SITE.parent.exists():
            SITE.mkdir(exist_ok=True)
            shutil.copy2(mp4, SITE / mp4.name)
            shutil.copy2(gif, SITE / gif.name)
        print(f"  {nombre}: {len(s)} frames, mp4 {mp4.stat().st_size / 1e3:.0f} KB, "
              f"gif {gif.stat().st_size / 1e6:.2f} MB, {time.perf_counter() - t0:.0f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
