"""Animaciones del curso: un módulo por animación, cada uno con `render(out_dir, s)`.

`s` es la línea de tiempo ping-pong (array en [0, 1]): ida suave 0 -> 1, pausa, vuelta 1 -> 0, pausa.
Cada módulo escribe `frame_NNNN.png` en `out_dir`, uno por valor de `s`. La codificación (mp4 + gif)
la hace tools/gen_animaciones.py con ffmpeg.
"""
