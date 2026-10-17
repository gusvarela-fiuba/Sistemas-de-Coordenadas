# Pentágonos afines — animaciones 2D y 3D en Python

Port a Python (numpy + matplotlib `FuncAnimation`) de las dos animaciones
Javis/Luxor que están en `julia/`. Muestran qué le pasa a un pentágono cuando
se le aplica una transformación afín `T(x) = A·x + b`, fase por fase, con la
matriz `A` y el vector `b` en pantalla en todo momento.

| Script | Fases | Frames | Salidas |
|---|---|---|---|
| `pentagonos_afines_2d.py` | 6 × 60 frames (12 s) | 360 | `.mp4` 1280×720 @ 30 fps, `.gif` 640×360 @ 15 fps, `_fases.png` |
| `pentagonos_afines_3d.py` | 6 × 50 frames (10 s) | 300 | ídem |

## Cómo correr

Desde esta carpeta (el entorno lo maneja `uv` desde la raíz del repo; ffmpeg se
toma de `/opt/homebrew/bin/ffmpeg`):

```sh
uv run python pentagonos_afines_2d.py
uv run python pentagonos_afines_3d.py
```

Cada script tarda ~45 s y escribe, con su mismo nombre base, el `.mp4`, el
`.gif` reducido y la lámina `_fases.png` (grilla 2×3, un panel por fase, para
verlo sin reproducir nada). Si ffmpeg no está, el script avisa por stderr, deja
igual el gif y la lámina, y termina con código 2.

## Convención de coordenadas

Se conserva la de Luxor: píxeles con origen en el centro de la pantalla y eje
**y hacia abajo** (en matplotlib el eje y está invertido). Consecuencias que
conviene tener presentes al leer los números en pantalla:

- una traslación `b = [0, -60]` mueve la figura **hacia arriba**;
- una rotación `R(θ)` con `θ > 0` se ve en pantalla en sentido **horario**
  (en el plano matemático usual, con y hacia arriba, sería antihorario).

Las funciones geométricas son puras y están separadas de la animación, para
reutilizarlas en una unidad marimo: `pentagono_regular(R)`,
`pentagono_irregular()`, `aplicar(M, puntos)` (nube N×2 o N×3 vía `puntos @ M.T`),
`aplicar_afin(A, b, puntos)`, `rotacion`, `escala`, `cizalla_x`,
`area_poligono`, `suavizar` (easing coseno) y `estado_afin(frame)` en el 2D;
`pentagono_regular_3d`, `prisma_pentagonal(R, H)`, `proyectar_perspectiva(puntos3d, d)`,
`rot_x/rot_y/rot_z`, `normal_cara` y `estado_afin_3d(frame)` en el 3D.

## `pentagonos_afines_2d.py` — qué muestra cada fase

Dos pentágonos, uno regular (radio 110 px, izquierda, azul) y uno irregular
(derecha, naranja), con la figura original "fantasma" en línea punteada y
ejes locales. A los dos se les aplica la misma `A` y el mismo `b`. El
progreso dentro de cada fase usa un easing coseno `t = ½(1 − cos πt_raw)`.

| Fase | Transformación | Parámetros | Hecho geométrico |
|---|---|---|---|
| 1 | Identidad | `A = I`, `b = 0` | Referencia. Todo se conserva. |
| 2 | Traslación pura | `b` va de `[0, 0]` a `[0, −60]` | Conserva forma, tamaño, ángulos, orientación; sólo cambia la posición. No es lineal: `T(0) ≠ 0`. |
| 3 | Rotación pura | `θ` de 0° a 72° (= 2π/5) | Isometría: conserva distancias, ángulos y áreas; `det A = 1`. A 72° el pentágono regular cae sobre sí mismo; el irregular no (se ve que rotó). |
| 4 | Escalamiento no uniforme | `sx` 1 → 1.35, `sy` 1 → 0.65 | Conserva paralelismo y la dirección de los ejes; no conserva ángulos ni distancias. Razón de áreas `= det A = sx·sy`. |
| 5 | Cizallamiento horizontal | `kx` 0 → 0.65, `A = [[1, kx], [0, 1]]` | Conserva paralelismo y **área** (`det = 1`); no conserva ángulos ni longitudes. La base horizontal queda fija, lo demás se inclina. |
| 6 | Afín general | `A = (1−t)·I + t·R(0.4t)·S(t)` con `S = [[1+0.2t, 0.4t], [0, 1−0.2t]]`, `b = t·[30, −35]` | Sólo sobreviven: rectas → rectas, paralelismo, razón de áreas `= det A`. |

Debajo de las figuras aparecen `A` (2×2) y `b` numéricos en cada frame.

## `pentagonos_afines_3d.py` — qué muestra cada fase

Izquierda: pentágono regular (radio 120) inmerso en R³ sobre el plano `z = 0`,
con su normal dibujada en amarillo y sombreado según `|n·L|` (se ven ambas
caras). Derecha: prisma pentagonal recto de altura 90 (extrusión del mismo
pentágono), 7 caras dibujadas con algoritmo del pintor (de la más lejana a la
más cercana, por `z` medio) e iluminación lambertiana con luz direccional
`L ∝ (0.5, −0.7, 1)`. En ambos paneles se dibujan los ejes locales X (rojo),
Y (verde), Z (azul) transformados por la misma `A`.

La cámara es en perspectiva con el ojo en `z = −d`, `d = 600`:
`x' = x·d/(d+z)`, `y' = y·d/(d+z)`. Lo que tiene más `z` está más lejos y se
ve más chico.

| Fase | Transformación | Parámetros | Hecho geométrico |
|---|---|---|---|
| 1 | "Identidad" vista inclinada | `A = Rx(0.35)·Ry(−0.45)`, `b = 0` | Orientación fija para que se aprecie la profundidad; nada se deforma. |
| 2 | Rotación alrededor de Y | `θy` de −0.45 a −0.45 + 2π (una vuelta) | Matriz ortogonal: `RᵀR = I`, `det = 1`; conserva distancias, ángulos y volumen. |
| 3 | Rotación alrededor de X | `φx` de 0.35 a 0.35 + 2π | Ídem; el pentágono plano muestra las dos caras y el sombreado cambia con la normal. |
| 4 | Traslación en profundidad | `b = [0, 0, −180·sin(πt)]` (se acerca y vuelve) | La geometría 3D no cambia; cambia la **escala aparente** por la perspectiva, y las paralelas de la escena dejan de proyectarse paralelas. |
| 5 | Escalamiento anisotrópico | `sx = 1 − 0.35 sin πt`, `sy = 1 + 0.30 sin πt`, `sz = 1 + 0.90 sin πt`, compuesto con `Rx(0.4)·Ry(−0.5)` | Conserva paralelismo; razón de volúmenes `= sx·sy·sz`; el prisma se estira notablemente en Z. |
| 6 | Cizallamiento 3D + giro | `x' = x + kx·y + kz·z` con `kx = 0.65 sin πt`, `kz = 0.40 sin πt`, y `Ry(0.45 + πt)` | Conserva paralelismo y **volumen** (`det = 1`); no conserva ángulos. |

Debajo aparecen `A` (3×3) y `b` (3×1) numéricos.

Como las fases 2 y 3 dan una vuelta completa y las 4–6 van y vuelven con
`sin(πt)`, el **último** frame de cada fase 3D coincide con el inicial; por
eso la lámina `pentagonos_afines_3d_fases.png` muestra el frame **central**
de cada fase (`t = 0.5`, efecto máximo). La lámina 2D sí usa el último frame,
que es donde cada transformación está completa.

## Qué cambió respecto del Julia

Los parámetros (matrices, ángulos, factores, duraciones, colores, posiciones,
tamaños de fuente en px) son los mismos. Los textos ya estaban en castellano
en el original y se mantienen tal cual (incluida la palabra "Shear" entre
paréntesis). Se verificó frame a frame contra `julia/*.gif` abriendo frames
con PIL: orden y forma de las fases coinciden, y los valores numéricos de `A`
y `b` en pantalla son iguales.

Diferencias:

- **Bloque de matriz.** El Julia escribe `A` y `b` en tres líneas, pero
  `Luxor.text` no interpreta `\n`, así que en los gifs de referencia la matriz
  sale aplastada en una sola línea y parcialmente fuera de pantalla. Acá se
  renderiza como bloque de tres líneas, que era la intención evidente.
- **Letras griegas.** En los gifs de referencia `θ` y `φ` de la línea de
  fórmula aparecen como un cuadradito (Courier no tiene griego). Acá se usa
  `['Courier', 'DejaVu Sans Mono']` como familia con fallback por glifo, y las
  letras se ven.
- **Marcadores de vértice** en matplotlib son círculos de diámetro en puntos
  convertidos desde los radios en px del Julia (4.5/2.5 px), con antialiasing
  distinto; el aspecto es equivalente, no idéntico al píxel.
- **GIF reducido.** El Julia genera el gif a 1280×720 @ 30 fps. Acá el gif es
  640×360 @ 15 fps (un frame de cada dos) para que pese < 3 MB. Como el
  formato GIF sólo admite duraciones en múltiplos de 10 ms, 66 ms se truncaría
  a 60 ms (16.7 fps y animación 8 % más corta); los scripts usan un
  `GifWriter` que alterna 70/70/60 ms (promedio 66.7 ms = 15 fps exactos), de
  modo que la duración total es la original (12 s y 10 s). Pillow además
  fusiona frames consecutivos idénticos (la fase 1 es estática), así que el gif
  tiene menos frames que 180/150 pero la misma duración. La versión completa a
  30 fps es el `.mp4`.
- **Orden de dibujo.** Se respeta el del Julia: ejes 3D antes de las figuras
  (quedan tapados por las caras que los cubren), vértices arriba de todo.

## Originales

Los scripts Javis originales quedan en `julia/`:
`affine_pentagons.jl`, `affine_pentagons_3d.jl` y sus salidas
`transformaciones_afines.gif` y `transformaciones_3d_pentagono.gif`.
`julia/test.png` es un gráfico de prueba de Plots.jl sin relación con los
pentágonos.
