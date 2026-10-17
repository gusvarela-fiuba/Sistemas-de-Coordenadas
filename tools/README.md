# tools/

Scripts auxiliares del repo. Todo Python corre con `uv run` (nunca el Python del sistema).

## `build.py` — generar el sitio estático

```
uv run tools/build.py                      # build completo en site/
uv run tools/build.py --skip-wasm          # sin exportar notebooks (deja lo que ya haya en site/unidades/)
uv run tools/build.py --only 07_cuna_autovectores   # exporta sólo esa unidad; el resto del sitio se regenera igual
uv run tools/build.py --out /ruta/otro     # otro directorio de salida (default: site/, relativo a la raíz)
```

Correr desde cualquier directorio: el script ubica la raíz del repo por su propia ruta.

Qué lee:

- `mapa/mapa.yaml` — el mapa de conceptos (esquema documentado en `mapa/ESQUEMA.md`). Se valida antes de generar nada: ids únicos, referencias cruzadas (concepto → clase, concepto → unidad, `requiere` → conceptos), prefijos de `apunte` contra `apunte/contenido/NN-*.tex`, archivos de las unidades exportables. Referencia rota = error y salida 1; ficha de clase inexistente = aviso y sigue.
- `clases/*.md` — fichas por clase. Se convierten con el paquete `markdown` (extensiones `tables`, `fenced_code`, `toc`); las fórmulas `$…$` / `$$…$$` se protegen del parser y las renderiza KaTeX desde cdnjs en el navegador. `README.md`, `PLANTILLA.md` (cualquier nombre en mayúsculas) y `_*.md` se ignoran.
- `unidades/*.py` — notebooks marimo con estado `piloto` o `migrada` en el yaml. Cada uno se exporta con `marimo export html-wasm --mode run --no-show-code` (se invoca `python -m marimo` del mismo venv; equivale a `uv run marimo export …`). `legacy` y `pendiente` no se exportan.
- `apunte/Apunte_Sistemas_de_Coordenadas.pdf` — se copia si existe; si no, el índice lo marca como no compilado.

Qué genera en `site/` (ignorado por git):

```
site/index.html                  índice: título, pregunta guía, mapa de conceptos (SVG inline generado en Python,
                                 sin JS), lista de clases con fechas/estado/links, link al apunte
site/clases/<id_clase>.html      fichas
site/unidades/<id_unidad>/       export WASM de cada unidad (index.html + assets/ de marimo, ~27 MB por unidad)
site/apunte.pdf
site/.nojekyll                   para que GitHub Pages no pase el sitio por Jekyll
```

Probar local (los notebooks WASM no andan desde `file://`, necesitan HTTP):

```
uv run python -m http.server 8765 --directory site
# http://localhost:8765/
```

Tiempos de referencia en la MBA (M-series): la exportación WASM tarda 1–2 s por unidad (no ejecuta el notebook; el código corre en el navegador con Pyodide). La primera vez que se corre `marimo export` después de `uv sync` puede tardar ~40 s.

### Patrón recomendado para animaciones en WASM

`_prueba_plotly.py` es un notebook mínimo (slider + figura plotly con `frames` y botón play) que muestra el patrón recomendado para las unidades nuevas: plotly con frames en vez de `mo.iframe(FuncAnimation.to_jshtml())`. La figura se construye en Pyodide y la anima plotly.js en la página; no hay iframe ni scripts inyectados. No es una unidad, no está en el yaml.

```
uv run marimo run tools/_prueba_plotly.py
```

Nota: el export WASM (sin `--execute`) no embebe salidas; el HTML contiene el código de las celdas y todo se calcula en el navegador. `--execute` intenta correr el notebook en un entorno aislado y, al no declarar dependencias en el script, falla con `No module named 'numpy'`; no se usa.

### Molde de unidad (piloto: `unidades/01_rotaciones.py`)

Toda unidad nueva copia la estructura de `01_rotaciones.py`: un `marimo.App(width="medium")`, Python puro, sólo `numpy`
y `plotly` (los dos están en Pyodide; nada de matplotlib, `mo.iframe` ni `to_jshtml()`, que no andan en WASM), grados en
la interfaz y radianes adentro, rotación/transformación activa por default, fórmulas en `mo.md` con `$…$` / `$$…$$`
(KaTeX: sin `\newtheorem` ni entornos de LaTeX). Cinco secciones, en este orden y con encabezado `##` visible:

1. **Hecho geométrico.** La pregunta "¿qué se conserva?" antes que la fórmula; la escalera R → R² → R³ en una tabla
   (álgebra | lo que se ve); cada fórmula con su hecho geométrico al lado. Una figura chica, estática, si ayuda.
2. **Manipulación.** La figura de tres capas: (a) gris = antes (grilla de referencia + cuadrado/cubo unitario),
   (b) teal = después (grilla transformada + imágenes de la base, las columnas de la matriz), (c) un objeto reconocible
   (parcela 2D de vértices enteros con norte; cubo + terreno N×3 en 3D) con estelas. Números vivos al lado de los
   controles: lo que se conserva como número (área del cuadrado unitario, una distancia) y la matriz actual.
   Layout `mo.hstack([mo.vstack(controles), mo.ui.plotly(figura)], widths=[1, 2])`. Controles en una celda aparte
   de la figura (el slider/checkbox/dropdown se define en una celda y se *muestra* dentro del `vstack` de la otra).
3. **Cuenta a mano y código lado a lado.** `mo.hstack([mo.md(latex), mo.vstack([mo.md("```python …```"), salida])],
   widths="equal")`, un hstack por cuenta, enteros y valores exactos; el código del bloque es el mismo que corre en la celda.
4. **Python de hoy.** Una sola idea nueva de Python por unidad (en 01: nube = array N×d con una fila por punto y
   `transformar(nube, R) = nube @ R.T`). Mostrar `shape` y un ejemplo de tres puntos.
5. **Ejercicios.** Cuatro: dos de lápiz con respuesta en `mo.accordion({"Ver respuesta": …})` y dos de código con hueco
   en `mo.ui.code_editor` (en el export el notebook corre en modo app, así que el alumno no puede editar celdas: el hueco
   va en un editor y una celda aparte hace `exec(editor.value, {"np": np, …})` y verifica con `np.allclose`, mostrando
   `mo.callout(…, kind="success" | "warn" | "danger")`; el `try/except` atrapa el `...` sin completar). Cada ejercicio
   con el nivel de la rúbrica del profesor (elemental / medio / avanzado) y la frase de la rúbrica a la que apunta.

Cierre: una celda "Enlaces del mapa" con links relativos desde `site/unidades/<id>/index.html`
(`../../clases/NN.html`, `../../apunte.pdf`, `../../index.html`, `../<otra_unidad>/index.html`) y una celda final de
`assert np.allclose(…)` silenciosos que valida todas las cuentas del notebook (corre en el navegador al cargar; si
falla, marimo muestra el error en esa celda). Las funciones de la unidad (`rot2`, `rot_x`, … , `transformar`) van en
una sola celda al principio, con docstring; los objetos fijos de cada figura (parcela, cubo, terreno) en otra.

Patrones plotly que funcionan en WASM:

- Figuras: `go.Figure` + `go.Scatter` (2D) / `go.Scatter3d` (3D, `scene.aspectmode="cube"`, cámara libre), mostradas
  con `mo.ui.plotly(fig)`. Polilíneas con cortes: un solo trazo con `None` entre segmentos (grillas, aristas, mallas).
- Animación: `frames=[go.Frame(name=str(i), data=[…trazas dinámicas…], traces=[índices]) …]` (36 cuadros de 0 a θ,
  el último coincide con el estado del slider) y botón `updatemenus=[dict(type="buttons", buttons=[dict(label="▶ reproducir",
  method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=False)]), …])]`. Las trazas
  estáticas van primero en `data` y no aparecen en los frames; `traces` indica qué índices reemplaza cada frame.
  Al mover un control marimo reconstruye la figura (y sus frames). Ver también `_prueba_plotly.py`.
- Verificación antes de commitear: `uv run marimo check unidades/<id>.py`, ejecución headless
  (`uv run python -c "…app.run()"`, corre las celdas y los asserts) y `uv run tools/build.py --only <id>` +
  `http.server` + curl 200. La extensión Claude in Chrome sirve para la revisión visual si está disponible.

### Tamaño del sitio

Cada unidad exportada copia los assets completos de marimo (~27 MB, 710 archivos). Con 14 unidades el sitio pasaría de 350 MB; si eso molesta en GitHub Pages, una mejora posible es compartir un único `site/assets/` reescribiendo las rutas `./assets/` de cada `index.html` (no está hecho; hay que verificar que los chunks que marimo carga en forma diferida sigan resolviendo).

## Pendiente fase 5 — GitHub Actions

Idea del workflow (`.github/workflows/pages.yml`, todavía no escrito):

1. `on: push` a `main` (y `workflow_dispatch`).
2. `actions/checkout`, `astral-sh/setup-uv`, `uv sync`.
3. `uv run tools/build.py` (el PDF del apunte se compila aparte o se commitea; el runner no tiene TeX Live).
4. `actions/upload-pages-artifact` con `path: site` y `actions/deploy-pages`.
5. Permisos `pages: write`, `id-token: write`; en el repo, Settings → Pages → Source: GitHub Actions.

El build ya deja `site/.nojekyll`, así que no hay que configurar nada más del lado de Pages.

## `bootstrap_github.sh`

Registra el PAT de la cuenta `gusvarela-fiuba` en el llavero, crea el repo en GitHub si no existe y configura `origin`. Se corre una vez por máquina.
