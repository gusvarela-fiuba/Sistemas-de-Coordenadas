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

- `mapa/mapa.yaml` — el mapa de conceptos (esquema documentado en `mapa/ESQUEMA.md`; se genera con `uv run tools/merge_mapa.py` a partir de `mapa/_fragmentos/`). Se valida antes de generar nada: ids únicos, referencias cruzadas (concepto → clase, concepto → unidad, unidad → `clases`, `requiere` → conceptos), vocabularios de `estado`, `validacion` y `nivel`, prefijos de `apunte` contra `apunte/contenido/NN-*.tex`, archivos de las unidades exportables. Referencia rota = error y salida 1; ficha de clase inexistente = aviso y sigue.
- `clases/*.md` — fichas por clase. Se convierten con el paquete `markdown` (extensiones `tables`, `fenced_code`, `toc`); las fórmulas `$…$` / `$$…$$` se protegen del parser y las renderiza KaTeX desde cdnjs en el navegador. `README.md`, `PLANTILLA.md` (cualquier nombre en mayúsculas) y `_*.md` se ignoran.
- `unidades/*.py` — notebooks marimo con estado `piloto` o `migrada` en el yaml. Cada uno se exporta con `marimo export html-wasm --mode run --no-show-code` (se invoca `python -m marimo` del mismo venv; equivale a `uv run marimo export …`). `legacy` y `pendiente` no se exportan.
- `apunte/Apunte_Sistemas_de_Coordenadas.pdf` — se copia si existe; si no, el índice lo marca como no compilado.

Qué genera en `site/` (ignorado por git):

```
site/index.html                  portada = el camino (docs/camino.md): tres entradas (Empezar → estación 1; Seguir la
                                 cursada → la estación de la última clase con fechas_2026 ≤ hoy; Repasar → mapa.html) y
                                 una estación por unidad de mapa/_fragmentos/unidades.yaml, en ese orden, con número,
                                 título, pregunta, gancho de agrimensura, estado calculado (lista / en clase / todavía no),
                                 las clases que cubre con etiquetas de procedencia y validación, y enlaces a la unidad,
                                 las fichas y las secciones del apunte (apunte.pdf#nameddest=cap:NN). Última estación
                                 "Lo que viene": las clases sin unidad (11–14).
site/mapa.html                   mapa de conceptos (SVG inline generado en Python) con dos controles en JS inline: filtro
                                 de ruta (troncal / todo, por el `nivel` de la clase de cada nodo) y deslizador "hasta la
                                 clase N" (atenúa a opacity 0.25 los nodos y aristas de clases posteriores; default N =
                                 última clase dictada). Debajo, la lista de clases con fechas/etiquetas/links y el apunte.
site/clases/<id_clase>.html      fichas, con dos etiquetas arriba del título: procedencia (`estado`) y `validacion`
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

### Molde de unidad v2 (piloto: `unidades/01_rotaciones.py`; secuencia en `docs/camino.md`)

**Cabecera obligatoria.** Toda unidad DEBE empezar (antes del docstring) con el bloque de metadata PEP 723 que declara
lo que importa; es lo que marimo embebe en el HTML y lo que Pyodide instala con micropip al cargar. Sin él, el export
WASM muere en la celda de imports con `ModuleNotFoundError: No module named 'plotly'` y todas las figuras caen en cascada.
`build.py` se niega a exportar una unidad que no lo tenga.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
```

(Las unidades legacy que usan matplotlib declaran `"matplotlib"` en lugar de `"plotly"`; `scipy` también existe como
paquete Pyodide si hiciera falta. La biblioteca estándar, `fractions`, `math`, no se declara.)

Toda unidad nueva copia la estructura de `01_rotaciones.py`: un `marimo.App(width="medium")`, Python puro, sólo `numpy`
y `plotly` (los dos están en Pyodide; nada de matplotlib, `mo.iframe` ni `to_jshtml()`, que no andan en WASM), grados en
la interfaz y radianes adentro, rotación/transformación activa por default, fórmulas en `mo.md` con `$…$` / `$$…$$`
(KaTeX: sin `\newtheorem` ni entornos de LaTeX). Seis secciones (0 a 5), en este orden y con encabezado `##` visible:

0. **Situación de campo y predicción.** Antes del hecho geométrico: una situación concreta de agrimensura (en 01: el mismo
   mojón con tres etiquetas de coordenadas; sin fajas ni EPSG) y una **predicción** con `mo.ui.radio` (opciones = dict
   etiqueta → clave; `value=None` para que arranque sin elegir). Los números de las opciones salen de una celda numpy del
   mismo notebook (las correctas, las del error típico, las de una reflexión, "las mismas"), nunca a mano. Una celda aparte
   mapea `radio.value` → `mo.callout(kind="warn" | "success" | "neutral")`: cada opción incorrecta explica **el error
   concreto** ("giraste el punto, no los ejes"), la correcta confirma y adelanta qué va a mostrar la unidad. Los candidatos
   entran a la celda de asserts (son distintos entre sí y coinciden con `rot2`).

1. **Hecho geométrico.** La pregunta "¿qué se conserva?" antes que la fórmula; la escalera R → R² → R³ en una tabla
   (álgebra | lo que se ve); cada fórmula con su hecho geométrico al lado. Una figura chica, estática, si ayuda.
2. **Manipulación.** La figura de tres capas: (a) gris = antes (grilla de referencia + cuadrado/cubo unitario),
   (b) teal = después (grilla transformada), con las **imágenes de la base como flechas del color de su columna**
   (`COLORES = ("#1b6f6a" teal, "#b5451b" rust, "#c9a227" gold)`, leyenda `columna k = R eₖ`), (c) un objeto reconocible
   (parcela 2D violeta de vértices enteros con norte; cubo + terreno N×3 en 3D) con estelas. Números vivos al lado de los
   controles: lo que se conserva como número (área **con signo** del cuadrado unitario, una distancia) y la matriz actual
   con `matriz_coloreada(M)` (pmatrix con `\textcolor{#hex}{…}` por columna: KaTeX lo renderiza en WASM; para prosa fuera
   de `$…$` sirve `<span style="color:#hex">` dentro del mismo `mo.md`).
   **Casos precargados**: un `mo.ui.dropdown` arriba del deslizador con identidad (0°), 90°, 35°, −35° y tres
   contraejemplos que no son rotaciones (reflexión `diag(1,−1)`, corte `[[1,0.5],[0,1]]`, proyección `[[1,0],[0,0]]`),
   en un dict `casos = {etiqueta: (tipo, dato, "qué se conserva y qué no")}`. El **slider se crea en una celda que depende
   del dropdown** (`value=` el ángulo del caso, `disabled=` si es contraejemplo): así al elegir una rotación el slider
   arranca ahí y después manda él; con un contraejemplo la figura usa la matriz fija, los números vivos muestran qué falla
   (área −1 o 0, distancia distinta) y se fuerza modo activo. La animación recorre un `camino` de matrices: `rot2(t)` de 0
   a θ para rotaciones, `I + s·(M − I)` para contraejemplos; las estelas son la trayectoria de cada vértice por ese camino
   (arco o segmento). Los asserts de los números vivos van bajo `if es_rotacion:`.
   Layout `mo.hstack([mo.vstack(controles), mo.ui.plotly(figura)], widths=[1, 2])`. Controles en una celda aparte
   de la figura (el slider/checkbox/dropdown se define en una celda y se *muestra* dentro del `vstack` de la otra).
   3D: `height ≥ 600` y `scene.aspectmode="cube"`.
3. **Cuenta a mano y código lado a lado.** `mo.hstack([mo.md(latex), mo.vstack([mo.md("```python …```"), salida])],
   widths="equal")`, un hstack por cuenta, enteros y valores exactos; el código del bloque es el mismo que corre en la celda.
   Las matrices del LaTeX llevan cada columna en `\textcolor{…}` con los mismos colores que las flechas de la figura.
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
  Para que los botones no pisen el título: título a la izquierda (`title=dict(x=0.01, xanchor="left", y=0.985,
  yanchor="top")`), botones a la derecha (`updatemenus` con `x=1, xanchor="right", y=1, yanchor="bottom"`) y
  `margin.t=56`.
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
