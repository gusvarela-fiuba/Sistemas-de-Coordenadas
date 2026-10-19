# Laboratorio CAD

Herramientas para trabajar las transformaciones del apunte con un CAD de verdad. Cada comando de edición es una transformación: ROTATE es una rotación, MOVE una traslación, MIRROR una reflexión, SCALE una homotecia, ALIGN una similaridad o un movimiento rígido, un bloque insertado con escala X distinta de Y una afinidad, STRETCH no es una transformación afín única y UCS es un cambio de base.

## Scripts

- `generar_dxf.py`: genera los DXF de los ejercicios en `cad/dxf/` y sus respuestas en `cad/dxf/esperado/`. Es determinista: dos corridas dan archivos idénticos byte a byte.
- `que_matriz.py ORIGINAL.dxf TRANSFORMADO.dxf`: empareja los vértices por etiqueta, estima la afín \(p' = Mp + t\) (y la homografía si hay cuatro o más vértices) e informa \(M\), \(t\), el determinante, el residuo RMS, la familia mínima y la lectura geométrica. `--json` da la salida para las pruebas; `--tol` cambia el residuo máximo (por defecto 0,005 m) por encima del cual informa «no afín». Sale con código 2 si faltan etiquetas.
- `test_que_matriz.py`: pruebas (`uv run pytest tools/cad -q`).

```
uv run python tools/cad/generar_dxf.py
uv run python tools/cad/que_matriz.py cad/dxf/cap01_rotate.dxf cad/dxf/esperado/cap01_rotate_30.dxf
uv run pytest tools/cad -q
```

## Los DXF

Versión R2000 (AC1015), unidades en metros, coordenadas locales chicas. Capas: `PARCELA` (LWPOLYLINE cerrada), `VERTICES` (un POINT por vértice), `ETIQUETAS` (TEXT A, B, C, …), `EJES` (dos LINE desde el origen con «E» y «N») y, según el ejercicio, `ACIMUT`, `ESPEJOS`, `DESTINO` (A', B' para el ALIGN rígido; A'', B'' para el ALIGN con escala) y `VENTANA` (la ventana del STRETCH). `cap04_bloque.dxf` trae además el bloque `PARCELA_BLOQUE` definido con punto base en el origen.

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

Se abren directamente en AutoCAD (OPEN, tipo DXF), LibreCAD (Archivo → Abrir) o QCAD (File → Open). Si no se ve nada, ZOOM EXTENTS (en LibreCAD, Ver → Zoom automático).

## Guardar el transformado para `que_matriz.py`

1. Abrir el DXF del ejercicio y aplicar el comando (ROTATE, MIRROR, …).
2. Seleccionar **todo** lo de la parcela: la polilínea, los POINT y los TEXT. Si se transforma sólo la polilínea, los puntos quedan donde estaban: `que_matriz.py` avisa que no coinciden y usa la fuente que queda más cerca de las etiquetas, pero si las etiquetas tampoco se movieron el resultado es la identidad.
3. Borrar el original si se trabajó sobre una copia (las etiquetas no pueden estar repetidas).
4. Guardar como DXF (R2000 o R12; en LibreCAD, «Guardar como» con tipo DXF) con otro nombre y correr `que_matriz.py ORIGINAL.dxf TRANSFORMADO.dxf`.

Cómo empareja: en cada archivo toma los POINT de `VERTICES` y los vértices de la polilínea de `PARCELA` (LWPOLYLINE o POLYLINE de R12), y asigna cada etiqueta de `ETIQUETAS` al vértice más cercano (asignación uno a uno). Si no hay capa `ETIQUETAS`, usa los TEXT de una sola letra de cualquier capa salvo `EJES`. Si hay un INSERT con vértices etiquetados, usa los del INSERT. Entre los dos archivos empareja las etiquetas comunes; hacen falta tres no alineadas.

La familia mínima sigue el criterio de `apunte/scripts/cap04_mapa_transformaciones.py`: identidad, traslación, rotación (todo movimiento rígido directo que no es traslación es una rotación alrededor de un centro), reflexión, movimiento rígido (isometría inversa con deslizamiento), similaridad, afinidad o no afín.

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
  Residuo RMS = 0,000 m (tolerancia 0,005 m)

Familia mínima: reflexión
  Eje de reflexión: pasa por (50,000; 0,000), dirección 90,000° desde el eje E (antihorario)

Homografía (h33 = 1)
    [  -1,000    0,000  100,000 ]
    [   0,000    1,000    0,000 ]
    [   0,000    0,000    1,000 ]
  Residuo RMS = 0,000 m
```
