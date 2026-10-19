# Laboratorio CAD

Herramientas para trabajar las transformaciones del apunte con un CAD de verdad. Cada comando de edición es una transformación: ROTATE es una rotación, MOVE una traslación, MIRROR una reflexión, SCALE una homotecia, ALIGN una similaridad o un movimiento rígido, un bloque insertado con escala X distinta de Y una afinidad, STRETCH no es una transformación afín única y UCS es un cambio de base. AREA mide lo que la fórmula del agrimensor calcula con los vértices, y el determinante dice por cuánto se multiplica esa área al transformar.

## Scripts

- `generar_dxf.py`: genera los DXF de los ejercicios en `cad/dxf/` y sus respuestas en `cad/dxf/esperado/`. Es determinista: dos corridas dan archivos idénticos byte a byte.
- `que_matriz.py ORIGINAL.dxf TRANSFORMADO.dxf`: empareja los vértices por etiqueta, estima la afín \(p' = Mp + t\) (y la homografía si hay cuatro o más vértices) e informa \(M\), \(t\), el determinante, el área encerrada por los vértices en cada archivo y su cociente (que, para una afín, es \(|\det M|\)), el residuo RMS, la familia mínima y la lectura geométrica. `--json` da la salida para las pruebas; `--tol` cambia el residuo máximo (por defecto 0,005 m) por encima del cual informa «no afín». Sale con código 2 si faltan etiquetas.
- `test_que_matriz.py` (capítulos 1 a 4) y `test_cad_cap06_cap09.py` (capítulos 6 y 9): pruebas (`uv run pytest tools/cad -q`).

```
uv run python tools/cad/generar_dxf.py
uv run python tools/cad/que_matriz.py cad/dxf/cap01_rotate.dxf cad/dxf/esperado/cap01_rotate_30.dxf
uv run pytest tools/cad -q
```

## Los DXF

Versión R2000 (AC1015), unidades en metros, coordenadas locales chicas. Capas: `PARCELA` (LWPOLYLINE cerrada), `VERTICES` (un POINT por vértice), `ETIQUETAS` (TEXT A, B, C, …), `EJES` (dos LINE desde el origen con «E» y «N») y, según el ejercicio, `ACIMUT`, `ESPEJOS`, `DESTINO` (A', B' para el ALIGN rígido; A'', B'' para el ALIGN con escala) y `VENTANA` (la ventana del STRETCH). Los DXF de los capítulos 6 y 9 suman dos capas, `CUNAS` (los triángulos desde el origen y el área con signo de cada uno) y `AREA` (el área total como texto); se agregan sólo en esos archivos, así los de los capítulos 1 a 4 no cambian. `cap04_bloque.dxf` y `cap06_scale.dxf` traen además el bloque `PARCELA_BLOQUE` definido con punto base en el origen.

| Ejercicio | Respuesta en `esperado/` |
|---|---|
| `cap01_rotate` | `cap01_rotate_30`: ROTATE 30° alrededor de A |
| `cap01_ucs` | `cap01_ucs_activa_30` (objeto rotado 30° alrededor del origen) y `cap01_ucs_pasiva_30` (coordenadas leídas en un UCS rotado 30°) |
| `cap01_units` | `cap01_units_bisectriz`: pasar de ángulo antihorario desde el este a acimut horario desde el norte es reflejar en la recta \(y = x\) |
| `cap01_arraypolar` | `cap01_arraypolar_60`: la primera copia del ARRAYPOLAR (60° alrededor del origen) |
| `cap02_move_rotate` | `cap02_move_rotate` (MOVE 12, 4 y después ROTATE 90° alrededor del origen) y `cap02_rotate_move` (al revés) |
| `cap03_mirror` | `cap03_mirror_x50` (espejo x = 50), `cap03_mirror_paralelos` (x = 50 y después x = 60) y `cap03_mirror_cortan` (y = −10 y después y = x − 30, a 45°) |
| `cap03_align` | `cap03_align_rigido` (A → A', B → B') y `cap03_align_similaridad` (A → A'', B → B'', con escala) |
| `cap04_bloque` | `cap04_bloque_x2_y1` y `cap04_bloque_xm1`: INSERT del bloque con esas escalas |
| `cap04_stretch` | `cap04_stretch_10`: STRETCH que corre C y D 10 m al este |
| `cap06_area` | `cap06_area_cunas`: la misma parcela con los cinco triángulos desde el origen y su área con signo (−85, +272, +328, +270 y −130 m²; suman 655 m²) |
| `cap06_scale` | `cap06_scale_2` (SCALE ×2 con punto base A: área 2620 m², cuatro veces 655) y `cap06_bloque_x2_y1_area` (INSERT del bloque con escala X = 2, Y = 1: área 1310 m², el doble) |
| `cap09_ucs` | `cap09_ucs_frente` (lectura pasiva: las coordenadas en el UCS con origen en A y eje X según AB) y `cap09_ucs_activa` (ROTATE alrededor de A hasta dejar AB horizontal: la misma matriz, lectura activa) |

Se abren directamente en AutoCAD (OPEN, tipo DXF), LibreCAD (Archivo → Abrir) o QCAD (File → Open). Si no se ve nada, ZOOM EXTENTS (en LibreCAD, Ver → Zoom automático).

## Guardar el transformado para `que_matriz.py`

1. Abrir el DXF del ejercicio y aplicar el comando (ROTATE, MIRROR, …).
2. Seleccionar **todo** lo de la parcela: la polilínea, los POINT y los TEXT. Si se transforma sólo la polilínea, los puntos quedan donde estaban: `que_matriz.py` avisa que no coinciden y usa la fuente que queda más cerca de las etiquetas, pero si las etiquetas tampoco se movieron el resultado es la identidad.
3. Borrar el original si se trabajó sobre una copia (las etiquetas no pueden estar repetidas).
4. Guardar como DXF (R2000 o R12; en LibreCAD, «Guardar como» con tipo DXF) con otro nombre y correr `que_matriz.py ORIGINAL.dxf TRANSFORMADO.dxf`.

Cómo empareja: en cada archivo toma los POINT de `VERTICES` y los vértices de la polilínea de `PARCELA` (LWPOLYLINE o POLYLINE de R12), y asigna cada etiqueta de `ETIQUETAS` al vértice más cercano (asignación uno a uno). Si no hay capa `ETIQUETAS`, usa los TEXT de una sola letra de cualquier capa salvo `EJES`. Si hay un INSERT con vértices etiquetados, usa los del INSERT. Entre los dos archivos empareja las etiquetas comunes; hacen falta tres no alineadas.

La familia mínima sigue el criterio de `apunte/scripts/cap04_mapa_transformaciones.py`: identidad, traslación, rotación (todo movimiento rígido directo que no es traslación es una rotación alrededor de un centro), reflexión, movimiento rígido (isometría inversa con deslizamiento), similaridad, afinidad o no afín.

## Los números de los capítulos 6 y 9

Área de la parcela por la fórmula del agrimensor (la mitad de la suma de los cuñas \(p_i \wedge p_{i+1}\) de vértices consecutivos, recorridos A, B, C, D, E en sentido antihorario):

| tramo | \(x_i y_{i+1} - x_{i+1} y_i\) | mitad (triángulo O \(p_i\) \(p_{i+1}\)) |
|---|---|---|
| A → B | −170 | −85 |
| B → C | 544 | 272 |
| C → D | 656 | 328 |
| D → E | 540 | 270 |
| E → A | −260 | −130 |
| suma | 1310 | **655 m²** |

Con el origen en A (coordenadas reducidas) los términos son 0, 414, 476, 420 y 0: suman otra vez 1310. SCALE ×2 desde A da 2620 m² (\(\det = 4\)); el bloque con escala X = 2, Y = 1 da 1310 m² (\(\det = 2\)).

UCS del frente: \(C\) tiene por columnas el versor de AB, \(b_1 = (24, 7)/25 = (0{,}96;\ 0{,}28)\), y su perpendicular a la izquierda, \(b_2 = (-0{,}28;\ 0{,}96)\); \(\det C = 1\). Las coordenadas en el UCS son \(C^{-1}(p - A) = C^T(p - A)\):

| vértice | en el sistema del dibujo | en el UCS del frente |
|---|---|---|
| A | (10,000; 10,000) | (0,000; 0,000) |
| B | (34,000; 17,000) | (25,000; 0,000) |
| C | (40,000; 36,000) | (36,080; 16,560) |
| D | (24,000; 38,000) | (21,280; 22,960) |
| E | (6,000; 32,000) | (2,320; 22,240) |

El giro es de −16,260° (el ángulo de AB con el eje E es 16,260°). El área medida en el UCS sigue siendo 655 m².

## Ejemplos de salida

ROTATE 30° alrededor de A:

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap01_rotate.dxf cad/dxf/esperado/cap01_rotate_30.dxf
Original:     cad/dxf/cap01_rotate.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap01_rotate_30.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E

Transformación afín  p' = M p + t
  M =
    [  0,866  -0,500 ]
    [  0,500   0,866 ]
  t = (6,340; -3,660) m
  det M = 1,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 655,000 m² (cociente = 1,000; |det M| = 1,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: rotación
  Ángulo de rotación: 30,000° (antihorario)
  Centro (punto fijo): (10,000; 10,000) = vértice A

Homografía (h33 = 1)
    [  0,866  -0,500   6,340 ]
    [  0,500   0,866  -3,660 ]
    [  0,000   0,000   1,000 ]
  Residuo RMS = 0,000 m
```

MIRROR con el espejo x = 50:

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap03_mirror.dxf cad/dxf/esperado/cap03_mirror_x50.dxf
Original:     cad/dxf/cap03_mirror.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap03_mirror_x50.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E

Transformación afín  p' = M p + t
  M =
    [ -1,000   0,000 ]
    [  0,000   1,000 ]
  t = (100,000; 0,000) m
  det M = -1,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 655,000 m² (cociente = 1,000; |det M| = 1,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: reflexión
  Eje de reflexión: pasa por (50,000; 0,000), dirección 90,000° desde el eje E (antihorario)

Homografía (h33 = 1)
    [  -1,000    0,000  100,000 ]
    [   0,000    1,000    0,000 ]
    [   0,000    0,000    1,000 ]
  Residuo RMS = 0,000 m
```

SCALE ×2 con punto base A (capítulo 6): el área se multiplica por 4, el determinante:

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap06_scale.dxf cad/dxf/esperado/cap06_scale_2.dxf
Original:     cad/dxf/cap06_scale.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap06_scale_2.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E

Transformación afín  p' = M p + t
  M =
    [ 2,000  0,000 ]
    [ 0,000  2,000 ]
  t = (-10,000; -10,000) m
  det M = 4,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 2620,000 m² (cociente = 4,000; |det M| = 4,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: similaridad
  Ángulo de rotación: 0,000° (antihorario)
  Factor de escala: 2,000 (áreas por 4,000)
  Centro (punto fijo): (10,000; 10,000) = vértice A

Homografía (h33 = 1)
    [   2,000    0,000  -10,000 ]
    [   0,000    2,000  -10,000 ]
    [   0,000    0,000    1,000 ]
  Residuo RMS = 0,000 m
```

Bloque con escala X = 2, Y = 1 (capítulo 6): el área se duplica:

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap06_scale.dxf cad/dxf/esperado/cap06_bloque_x2_y1_area.dxf
Original:     cad/dxf/cap06_scale.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap06_bloque_x2_y1_area.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E
Aviso: transformado: se usaron los vértices del INSERT (bloque insertado)

Transformación afín  p' = M p + t
  M =
    [ 2,000  0,000 ]
    [ 0,000  1,000 ]
  t = (0,000; 0,000) m
  det M = 2,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 1310,000 m² (cociente = 2,000; |det M| = 2,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: afinidad
  Escalas principales (valores singulares): 2,000 y 1,000
  Factor de áreas |det M|: 2,000; el sentido de giro se conserva

Homografía (h33 = 1)
    [ 2,000  0,000  0,000 ]
    [ 0,000  1,000  0,000 ]
    [ 0,000  0,000  1,000 ]
  Residuo RMS = 0,000 m
```

UCS con origen en A y eje X según AB (capítulo 9, lectura pasiva):

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap09_ucs.dxf cad/dxf/esperado/cap09_ucs_frente.dxf
Original:     cad/dxf/cap09_ucs.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap09_ucs_frente.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E

Transformación afín  p' = M p + t
  M =
    [  0,960   0,280 ]
    [ -0,280   0,960 ]
  t = (-12,400; -6,800) m
  det M = 1,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 655,000 m² (cociente = 1,000; |det M| = 1,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: rotación
  Ángulo de rotación: -16,260° (antihorario)
  Centro (punto fijo): (-30,000; 40,000)

Homografía (h33 = 1)
    [   0,960    0,280  -12,400 ]
    [  -0,280    0,960   -6,800 ]
    [   0,000    0,000    1,000 ]
  Residuo RMS = 0,000 m
```

ROTATE alrededor de A hasta dejar AB horizontal (capítulo 9, lectura activa): la misma \(M\), con centro en A:

```
$ uv run python tools/cad/que_matriz.py cad/dxf/cap09_ucs.dxf cad/dxf/esperado/cap09_ucs_activa.dxf
Original:     cad/dxf/cap09_ucs.dxf  [puntos (VERTICES)]
Transformado: cad/dxf/esperado/cap09_ucs_activa.dxf  [puntos (VERTICES)]
Vértices emparejados por etiqueta: A, B, C, D, E

Transformación afín  p' = M p + t
  M =
    [  0,960   0,280 ]
    [ -0,280   0,960 ]
  t = (-2,400; 3,200) m
  det M = 1,000
  Área (A, B, C, D, E, en ese orden): 655,000 m² → 655,000 m² (cociente = 1,000; |det M| = 1,000)
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: rotación
  Ángulo de rotación: -16,260° (antihorario)
  Centro (punto fijo): (10,000; 10,000) = vértice A

Homografía (h33 = 1)
    [  0,960   0,280  -2,400 ]
    [ -0,280   0,960   3,200 ]
    [  0,000   0,000   1,000 ]
  Residuo RMS = 0,000 m
```
