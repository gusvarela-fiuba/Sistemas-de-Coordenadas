# Ejercicio del 14/10/2026 — intersección de superficies y tangente paralela a un plano

Material de la clase 09 (14/10/2026; ficha `clases/09-analisis-derivada-jacobiano.md`).

Enunciado: sea C la curva intersección del paraboloide x² + y² + z = 1 con el plano x + y = 1. Hallar el punto de C donde la recta tangente es paralela al plano x − z = 0.
Resultado: C se parametriza r(t) = (t, 1 − t, 2t − 2t²), la tangente r'(t) = (1, −1, 2 − 4t) debe ser ortogonal a la normal (1, 0, −1), lo que da t = 1/4 y P = (1/4, 3/4, 3/8), con T = (1, −1, 1).

## Archivos

- `solucion_interseccion_superficies.md`: el enunciado resuelto paso a paso (parametrización, tangente, condición de paralelismo, verificación, método alternativo por gradientes y producto vectorial).
- `visualizar_solucion.py`: figura estática `ilustracion_3d.png` (perspectiva 3D con paraboloide, plano secante, curva C, tangente, plano de referencia y P; al lado el perfil X-Z donde se ve que la tangente tiene la misma pendiente que la traza z = x) y la versión interactiva plotly `ilustracion_3d_interactiva.html`.
- `visualizar_solucion_3d.py`: port con matplotlib de `julia/visualizar_solucion_3d.jl`; genera sólo lo que el Julia tenía de más, el gif de cámara girando 360° `ilustracion_3d_rotacion.gif` (560×420, 60 cuadros, 20 fps, ~2.4 MB). La figura estática del `.jl` ya la cubre `visualizar_solucion.py`, no se duplicó.
- `interseccion_3d.py`: script estilo notebook (`# %%`) con el marco teórico (gradientes como normales, tangente = ∇F₁ × ∇F₂), la parábola de intersección con su vértice (1/2, 1/2, 1/2) y los cortes con z = 0, figura `interseccion_3d_matplotlib.png` e interactiva `interseccion_3d_interactiva.html`.
- `build_notebook.py` → `interseccion_3d.ipynb`: arma el notebook a partir del script (requiere `nbformat`, que no está en el entorno del repo; el `.ipynb` ya generado está en la carpeta).
- `julia/`: el original en Julia (Plots) con su PNG y su gif.

Los `.html` de plotly pesan ~5 MB y se regeneran con los scripts; están excluidos del repo (`ejercicios/**/*.html` en `.gitignore`).

## Cómo correr

Desde esta carpeta:

```
uv run python visualizar_solucion.py       # ilustracion_3d.png + ilustracion_3d_interactiva.html
uv run python visualizar_solucion_3d.py    # ilustracion_3d_rotacion.gif (~30 s)
uv run python interseccion_3d.py           # interseccion_3d_matplotlib.png + interseccion_3d_interactiva.html
```

`interseccion_3d.py` termina con `plt.show()` y `fig_plotly.show()`: en una terminal con escritorio abre la figura y el navegador; sin navegador (SSH, `MPLBACKEND=Agg`) el `fig_plotly.show()` queda esperando a que alguien pida la página, los archivos ya están escritos cuando eso pasa y se puede cortar con Ctrl-C.

Referencia Julia: `cd julia && julia visualizar_solucion_3d.jl` (Julia 1.12 con Plots).
