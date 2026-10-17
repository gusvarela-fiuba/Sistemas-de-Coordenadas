# tools/

Scripts auxiliares del repo. Todo Python corre con `uv run` (nunca el Python del sistema).

## `build.py` — generar el sitio estático

```
uv run tools/build.py                      # build completo en site/
uv run tools/build.py --skip-wasm          # sin exportar notebooks (deja lo que ya haya en site/unidades/)
uv run tools/build.py --only 07a_cuna_determinante  # exporta sólo esa unidad; el resto del sitio se regenera igual
uv run tools/build.py --out /ruta/otro     # otro directorio de salida (default: site/, relativo a la raíz)
```

Correr desde cualquier directorio: el script ubica la raíz del repo por su propia ruta.

Qué lee:

- `mapa/mapa.yaml` — el mapa de conceptos (esquema documentado en `mapa/ESQUEMA.md`; se genera con `uv run tools/merge_mapa.py` a partir de `mapa/_fragmentos/`). Se valida antes de generar nada: ids únicos, referencias cruzadas (concepto → clase, concepto → unidad, unidad → `clases`, `requiere` → conceptos), vocabularios de `estado`, `validacion` y `nivel`, prefijos de `apunte` contra `apunte/contenido/NN-*.tex`, archivos de las unidades exportables. Referencia rota = error y salida 1; ficha de clase inexistente = aviso y sigue.
- `clases/*.md` — fichas por clase. Se convierten con el paquete `markdown` (extensiones `tables`, `fenced_code`, `toc`); las fórmulas `$…$` / `$$…$$` se protegen del parser y las renderiza KaTeX desde cdnjs en el navegador. `README.md`, `PLANTILLA.md` (cualquier nombre en mayúsculas) y `_*.md` se ignoran.
- `unidades/*.py` — notebooks marimo con estado `piloto` o `migrada` en el yaml. Cada uno se exporta con `marimo export html-wasm --mode run --no-show-code` (se invoca `python -m marimo` del mismo venv; equivale a `uv run marimo export …`) sobre una copia en `site/_build/` con el módulo común embebido (ver "Módulo común y export WASM"). `legacy` y `pendiente` no se exportan.
- `apunte/Apunte_Sistemas_de_Coordenadas.pdf` — se copia si existe; si no, el índice lo marca como no compilado.

Qué genera en `site/` (ignorado por git):

```
site/index.html                  portada = el hilo conductor (docs/camino.md): tres entradas (Empezar → unidad 0; Seguir
                                 la cursada → la unidad de la última clase con fechas_2026 ≤ hoy; Repasar → mapa.html) y
                                 una entrada por unidad de mapa/_fragmentos/unidades.yaml, en ese orden, con número,
                                 título, pregunta, gancho de agrimensura, estado calculado (lista / en clase / todavía no),
                                 las clases que cubre con etiquetas de procedencia y validación, y enlaces a la unidad,
                                 las fichas y las secciones del apunte (apunte.pdf#nameddest=cap:NN). Última unidad
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

### Molde de unidad v2 (lecciones piloto: `unidades/01a_punto_quieto.py`, `01b_rotacion_plano.py`, `01c_rotaciones_3d.py`; el piloto de una pieza quedó en `unidades/_legacy/01_rotaciones_v2.py`; secuencia en `docs/camino.md`)

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

Toda unidad nueva copia la estructura de `PLANTILLA_leccion.py` (o de `01a_punto_quieto.py`): un `marimo.App(width="medium")`, Python puro, sólo `numpy`
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

### Módulo común y export WASM

`unidades/cb104.py` es el módulo común de las unidades (paleta `COLORES`, `rot2`/`rot_x`/`rot_y`/`rot_z`/`rodrigues`,
`transformar`, `hom`/`dehom`, `area_poligono`, `matriz_coloreada`/`pmat`/`vec_tex`/`num_tex`, las figuras plotly de tres
capas `figura_plano`/`capa_antes`/`capa_despues`/`objeto`/`flechas_columnas`/`animar`, las 3D `figura_espacio`/
`cubo_unitario`/`flechas_columnas_3d`, y `verificar`/`exacto`). Sólo depende de numpy; plotly se importa adentro de las
funciones que dibujan. `uv run python unidades/cb104.py` corre sus asserts.

Como vive en el mismo directorio que los notebooks, en `marimo edit` / `marimo run` alcanza con importarlo. Pero el export
WASM no lleva archivos vecinos (en el navegador no existe `cb104.py`), así que la convención es **una celda exactamente así**:

```python
@app.cell
def _():
    import cb104 as lib  # cb104:inline
    return (lib,)
```

`build.py` no exporta el notebook original sino una copia en `site/_build/<archivo>.py` donde esa línea se reemplaza por

```python
    import types as _types
    lib = _types.ModuleType("cb104")
    exec(compile('<fuente de cb104.py como literal repr()>', "cb104.py", "exec"), lib.__dict__)
```

(el `return (lib,)` queda igual, así el grafo de celdas de marimo no cambia). Reglas:

- el marcador `# cb104:inline` va en la misma línea que `import cb104 as lib`; cualquier otra forma de importar cb104
  (`from cb104 import …`, `import cb104` sin marcador) hace fallar el build con un mensaje que lo explica, porque en el
  navegador terminaría en `ModuleNotFoundError`;
- el módulo se embebe en cada export: cambiar `cb104.py` obliga a re-exportar las unidades que lo usan (`tools/build.py`);
- no importar nada en `cb104.py` que no esté en Pyodide (hoy: numpy y plotly);
- la plantilla `unidades/PLANTILLA_leccion.py` ya trae la celda marcada y las seis secciones del molde v2; se copia a
  `unidades/NN_<tema>.py`, no va en `unidades.yaml` (`build.py` ignora todo lo que no esté en el yaml).

### Tamaño del sitio

Cada unidad exportada copia los assets completos de marimo (~27 MB, 710 archivos). Con 14 unidades el sitio pasaría de 350 MB; si eso molesta en GitHub Pages, una mejora posible es compartir un único `site/assets/` reescribiendo las rutas `./assets/` de cada `index.html` (no está hecho; hay que verificar que los chunks que marimo carga en forma diferida sigan resolviendo).

## Cómo agregar una lección en 5 pasos

1. Copiar la plantilla y completar los corchetes: `cp unidades/PLANTILLA_leccion.py unidades/NN_nombre.py`. Reemplazar todo lo que está entre `[…]`, borrar las notas "PLANTILLA:" y respetar las seis secciones del molde v2 (0 a 5, más el anexo). La cabecera PEP 723 y la celda `import cb104 as lib  # cb104:inline` ya vienen en la plantilla.
2. Dar de alta la unidad en `mapa/_fragmentos/unidades.yaml` (la posición en la lista es la de la unidad en la portada). Los campos son exactamente estos (`nota` es opcional):

   ```yaml
     - id: NN_nombre                       # único; nombre de la carpeta site/unidades/<id>/
       archivo: unidades/NN_nombre.py      # tiene que existir si el estado es piloto o migrada
       titulo: "Título de la lección"
       estado: piloto                      # piloto | migrada se exportan; legacy | pendiente no
       clases: ["NN"]                      # ids de clase que cubre, como strings ("03", "03p")
       pregunta: "¿Qué le pasa a … cuando …?"            # una sola línea: la pregunta de campo
       gancho_agrimensura: "Situación concreta de campo." # una sola línea, sin fajas ni EPSG
       nivel: troncal                      # troncal | complementario | avanzado
   ```

3. Apuntar los conceptos a la lección: en el `mapa/_fragmentos/bloque-*.yaml` que corresponda a su clase, poner `unidad: NN_nombre` en cada concepto que la lección desarrolla (el nodo del mapa pasa a linkear a la lección en vez de a la ficha). Si el concepto es nuevo, antes agregarlo a `mapa/CONCEPTOS.md`.
4. Verificar: `uv run tools/merge_mapa.py && uv run marimo check --select MW unidades/NN_nombre.py && uv run python unidades/NN_nombre.py` (el último corre el notebook headless: todas las celdas y los `assert`; si algo falla, lo imprime).
5. Exportar y mirar: `uv run python tools/build.py --only NN_nombre`, servir con `uv run python -m http.server -d site 8765` y abrir `http://localhost:8765/unidades/NN_nombre/index.html` (el WASM no anda desde `file://`). Commit de `unidades/NN_nombre.py`, los fragmentos y `mapa/mapa.yaml` regenerado; push a `main`: el workflow publica.

Gotchas conocidos:

- Las etiquetas de `mo.ui.radio` / `mo.ui.dropdown` no pasan por KaTeX: para mostrar vectores en las opciones usar `lib.vec_plano`, no `$…$`.
- Un `|` dentro de `$…$` en una tabla markdown parte la celda: escribir `\lvert … \rvert`.
- En los `r"""…"""` los escapes van simples (`\.`, `\,`), no dobles (`\\.`): el string crudo ya los conserva.
- `mo.hstack` con un panel largo tapa el texto de la figura: usar `mo.vstack([figura, panel])`.
- Los helpers nuevos van a `unidades/cb104.py` con su `assert` en el bloque `__main__`, no a la lección.
- La celda `import cb104 as lib  # cb104:inline` tiene que quedar exactamente así (una celda propia que devuelve `lib`); cualquier otra forma de importar cb104 hace fallar el build.

## Publicación — GitHub Actions

`.github/workflows/pages.yml` corre en cada push a `main` (y a mano con *Run workflow*): `uv sync --frozen`, `uv run tools/merge_mapa.py` seguido de `git diff --exit-code mapa/mapa.yaml` (si el mapa commiteado no coincide con los fragmentos, falla), `uv run marimo check --select MW unidades/[01]*.py`, `uv run python tools/build.py` y despliegue con `actions/upload-pages-artifact` + `actions/deploy-pages`. En los pull requests corre el mismo build sin desplegar. El runner no necesita TeX (el PDF del apunte está commiteado y el build lo copia) ni red para el export WASM (el frontend sale del wheel de marimo; Pyodide lo baja el navegador del alumno). Una vez por repo: Settings → Pages → Source: GitHub Actions. El build ya deja `site/.nojekyll`.

## `bootstrap_github.sh`

Registra el PAT de la cuenta `gusvarela-fiuba` en el llavero, crea el repo en GitHub si no existe y configura `origin`. Se corre una vez por máquina.
