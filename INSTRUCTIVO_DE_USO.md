# Instructivo de uso — Sistemas de Coordenadas (CB104)

Este documento explica cómo usar la guía de estudio interactiva de CB104 Sistemas de Coordenadas (Agrimensura, FIUBA): cómo entrar y navegar desde el navegador, cuál es la lógica pedagógica del recorrido, cómo clonar el repositorio en una computadora propia y cómo adoptarlo y publicarlo a nombre de la cátedra. La guía la escribió Gustavo Varela como alumno de la cursada 2C2026 (profesor Javier Clavijo); no es material oficial de la cátedra. La descripción general del contenido está en el [README](README.md).

Contenido:

1. [Cómo entrar y navegar (sin instalar nada)](#parte-1--cómo-entrar-y-navegar-sin-instalar-nada)
2. [Guía pedagógica del hilo conductor](#parte-2--guía-pedagógica-del-hilo-conductor-el-edificio-ladrillo-a-ladrillo)
3. [Cómo clonar el repositorio para usarlo o editarlo](#parte-3--cómo-clonar-el-repositorio-para-usarlo-o-editarlo-en-una-computadora)
4. [Cómo adoptar y publicar este curso a nombre de la cátedra](#parte-4--cómo-adoptar-y-publicar-este-curso-a-nombre-de-la-cátedra)
5. [Autoevaluación y banco de preguntas para Moodle](#parte-5--autoevaluación-y-banco-de-preguntas-para-moodle)

**[Curso interactivo: las 20 simulaciones con sus controles, ejercicios y enlaces (`CURSO_INTERACTIVO.md`)](CURSO_INTERACTIVO.md)** — el mapa unidad por unidad para ir directo a cada simulación.

## Parte 1 — Cómo entrar y navegar (sin instalar nada)

### Los tres accesos directos

Todo corre en el navegador; no hace falta instalar nada ni tener cuenta en ningún lado.

- **Curso interactivo (portada con las 20 unidades):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/
- **Apunte formal en PDF (demostraciones y guías resueltas):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/apunte.pdf
- **Mapa interactivo de conceptos:** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/mapa.html

La dirección va con mayúsculas en `Sistemas-de-Coordenadas`; escrita en minúsculas da 404.

### Los tres botones de arriba de la portada

La portada es el hilo conductor: las 20 unidades en orden, cada una con su pregunta de campo, su gancho de agrimensura, su estado y los enlaces a la lección, a las fichas de clase y a las secciones del apunte. Arriba de todo hay tres entradas:

- **Empezar.** Lleva a la Unidad 0 (Fundamentos), el punto de partida del recorrido. Es la entrada para quien arranca la materia o quiere ponerse el idioma antes de la primera clase.
- **Seguir la cursada.** Lleva a la unidad que cubre la última clase dictada según el calendario 2026 cargado en el mapa; debajo del botón se lee a qué unidad y a qué clase apunta, con la fecha. Si todavía no se dictó ninguna clase, el botón lo dice. La Unidad 0 nunca es el destino de este botón, aunque cubra temas de las clases 1, 4 y 9: es encuadre, no cursada.
- **Repasar.** Abre el mapa de conceptos completo (`mapa.html`), que tiene dos controles: el selector **Ruta** (`todo` / `sólo troncal`) y el deslizador **hasta la clase N**, que atenúa los conceptos y las flechas de las clases posteriores a la elegida. Por defecto el deslizador queda en la última clase dictada, así que al abrirlo se ve exactamente lo que ya se dio. Debajo del mapa está la lista de clases con fechas, etiquetas y enlaces.

Más abajo en la portada está el "Recorrido paso a paso" con las 20 unidades; cada una se abre desde ahí.

### Cómo usar una unidad (en clase con el proyector o estudiando en casa)

Cada lección se abre en `https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/<id>/index.html` (los enlaces de cada unidad están en la [tabla del README](README.md#recorrido-de-las-20-unidades)). Las lecciones corren adentro del navegador con WebAssembly (Python ejecutándose en la página, sin servidor): la primera carga tarda unos segundos mientras se descargan el intérprete y las bibliotecas; después todo responde al instante. Los deslizadores, los menús de casos precargados, los botones de reproducir y el editor de código de los ejercicios se usan directamente en la página.

Todas las unidades siguen el mismo molde de seis secciones, siempre de lo conceptual y geométrico al cálculo. Los nombres son fijos (los de `unidades/PLANTILLA_leccion.py`):

0. **Situación de campo y predicción.** Un problema concreto de agrimensura y una predicción sin cuentas, en opción múltiple. Conviene detenerse acá: en clase, pedir que cada uno elija antes de seguir; en casa, elegir en serio antes de mirar la respuesta. Cada opción incorrecta explica el error concreto que la produce, no dice sólo "incorrecto".
1. **Hecho geométrico.** Qué se conserva y qué cambia, antes de cualquier fórmula, con la escalera R → R² → R³ en una tabla. Es la parte para leer en voz alta con el proyector.
2. **Manipulación.** La figura interactiva de tres capas: la grilla de antes (gris), la grilla después de la transformación (teal) y un objeto reconocible (una parcela, un cubo). Arriba del deslizador hay casos precargados (identidad, 90°, un ángulo cualquiera y los contraejemplos: reflexión, corte, determinante cero); al lado, los "números vivos" (área con signo, determinante) y la matriz actual con cada columna pintada del color de la flecha que representa en la figura. El botón de reproducir anima el camino desde la identidad hasta la transformación elegida.
3. **Cuenta a mano y código lado a lado.** La misma cuenta en lápiz (LaTeX con las columnas coloreadas) y en NumPy, una al lado de la otra. El código que se muestra es el mismo que corre en la celda.
4. **Python de hoy.** Una sola idea nueva de Python por unidad, aplicada al problema de campo, con el `shape` de los arrays y un ejemplo chico.
5. **Ejercicios.** Dos de lápiz, con la respuesta escondida en un desplegable "Ver respuesta", y dos de código con hueco: se completan los `...` en un editor en vivo y una celda de abajo verifica el resultado contra la referencia con `np.allclose`, mostrando si coincide, si la forma del array está mal o si todavía no corre. Cada ejercicio lleva el nivel de la rúbrica del profesor (elemental / medio / avanzado).

Al cierre, el anexo **"Dónde está la demostración"** enlaza las secciones del apunte PDF que respaldan la unidad, más la ficha de la clase, el hilo conductor y las unidades anterior y siguiente. Lo interactivo muestra; las demostraciones son las del apunte.

En las lecciones publicadas no se pueden editar las celdas del notebook (corren en modo aplicación); lo editable son los controles y los editores de los ejercicios. Para editar la lección entera hay que clonar el repositorio (Parte 3).

## Parte 2 — Guía pedagógica del hilo conductor (el edificio ladrillo a ladrillo)

### Por qué arranca en la Unidad 0

La Unidad 0 (Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica) es encuadre complementario del curso, no contenido de la cátedra. Resuelve un problema concreto: la materia usa desde la primera clase un idioma que el CBC no da, y sin ese idioma cada transformación se aprende aparte, sin manera de encadenarlas. Son cinco ladrillos, en orden deductivo (cada uno usa sólo los anteriores), y cada uno está escrito con la definición, la frase del profesor que lo respalda, lo que significa en el campo y cómo se escribe en NumPy:

1. **Conjuntos, operaciones y grupos.** Las transformaciones forman un grupo: componer es la operación, no hacer nada es el neutro, deshacer es la inversa. Los giros de la estación total son el ejemplo; en el plano conmutan, en 3D no.
2. **Los cuerpos R y C.** Los escalares de la materia. Un real escala la recta; multiplicar por un complejo ya es rotar y escalar a la vez: las matrices 2×2 de la forma `[[a, -b], [b, a]]` son C con otro ropaje.
3. **Espacio afín (mojones) y espacio vectorial (nace al plantar un origen).** El terreno es afín: hay mojones, no flechas. Al plantar la estación en un mojón y declararlo origen nace el espacio vectorial, y desde ahí **todo vector es un punto** (un mojón visto desde el origen) o un desplazamiento entre dos.
4. **El espacio dual V\*: una fila es una forma lineal.** Una fila no es un "vector fila": es una regla graduada que lee vectores. Las formas lineales se arrastran con la inversa de la transformación, al revés que los puntos, y el gradiente vive ahí: **el gradiente es una forma lineal, no un vector** (lo dijo el profesor en la clase 9).
5. **Producto interno y métrica G: la cinta métrica.** Vectores y formas solos no tienen largos ni ángulos; la métrica es un dato extra, el único puente entre V y V\*. En la base canónica G = I; sobre una superficie, G es la primera forma fundamental y cambia de punto a punto.

La situación de campo de la Unidad 0 es una loma con curvas de nivel: calcular hacia dónde sube más empinado tratando al gradiente como flecha da mal cuando la grilla no es cuadrada, y eso muestra por qué el gradiente es una regla y no una flecha.

### Cómo se apoya cada bloque en el anterior

Cada unidad declara de qué ladrillo viene y hacia cuál va (es el diccionario `HILO_CONDUCTOR` de `unidades/cb104.py`, que la propia lección muestra al principio como "venimos de / vamos hacia"). Resumido, el edificio es este:

- **Unidad 0 → Rotaciones (unidades 1 a 3).** Con el idioma puesto, la primera transformación del grupo: la rotación. Primero la pasiva (giran los ejes, el mojón se queda quieto, unidad 1); después la activa como matriz ortogonal de determinante +1 cuyas columnas dicen adónde van los ejes, y el mismo giro como número complejo (unidad 2); después los tres ejes de R³, donde el orden importa y toda composición es un solo giro alrededor de un eje (unidad 3).
- **Rotaciones → Producto interno (unidad 4).** Lo que la rotación conserva, largos y ángulos, es una cuenta uᵀv; para medir desde las coordenadas hay que aislar esa cuenta.
- **Producto interno → Reflexiones y similaridades (unidad 5).** Con largos y ángulos medibles se clasifica lo que los conserva dando vuelta la hoja (reflexión, determinante −1) y lo que sólo conserva ángulos (similaridad: rotar, escalar y trasladar, con su centro fijo).
- **Similaridades → Afinidades y homogéneas (unidad 6).** Si cada eje se estira distinto se pierden los ángulos, y la traslación sigue sumada afuera de la matriz; meterla adentro pide una matriz 3×3 sobre coordenadas homogéneas: componer es multiplicar y el área se multiplica por el determinante.
- **Afinidades → Proyectivas (unidad 7).** La fila (0 0 1) es lo que mantiene las paralelas; al liberarla, las paralelas se cruzan como en una foto y hacen falta cuatro puntos: la homografía, la recta al infinito y la razón doble.
- **Proyectivas → Formas lineales (unidad 8).** Las rectas se transforman con la inversa transpuesta, al revés que los puntos; para entender eso hace falta el dual: la forma lineal como regla graduada y la regla arrastrada para que la lectura no cambie.
- **Formas lineales → Cuña y determinante (unidad 9) → Núcleo y autovectores (unidad 10) → Autovalores en 3D y puntos fijos (unidad 11).** La recta por dos puntos salió de un producto cruz sin nombre: la cuña y el determinante como área o volumen orientado, cero exactamente cuando hay colinealidad. Cuando el determinante da cero una dirección entera va al cero (el núcleo), y restando λI aparecen las direcciones que no giran (los autovectores). En R³ el polinomio es cúbico y siempre tiene una raíz real: el eje de una rotación y los puntos fijos de una homografía.
- **Autovectores → Cambio de base y diagonalización (unidad 12).** Con los autovectores como ejes nuevos la matriz se vuelve diagonal: la matriz de cambio de base (columnas = ejes nuevos) y la transformación vista en la grilla nueva.
- **Diagonalización → SVD e inversas (unidad 13).** La grilla propia no siempre existe (un giro no tiene ejes propios reales); con dos grillas ortogonales, una a la entrada y otra a la salida, siempre existe: la SVD, la inversa y la pseudoinversa con sus cuatro subespacios.
- **SVD → Jacobiano y primera forma fundamental (unidad 14).** El terreno no es una matriz fija sino una transformación lineal que cambia de punto a punto: el jacobiano 3×2 de una superficie y la primera forma fundamental G = JᵀJ, con la que el largo de un paso se mide sólo con los números de la grilla.
- **Primera forma → Cuatro problemas (unidad 15).** La tabla JᵀJ de productos internos de las columnas reaparece como AᵀA en las ecuaciones normales: con más mediciones que incógnitas, la solución deja el residuo perpendicular a las columnas. Cuatro veces: recta de ajuste, punto por distancias, Procrustes y regresión total.
- **Cuatro problemas → Curvatura (unidad 16).** La regresión total termina en una forma cuadrática cuyas direcciones propias son extremos; sobre una superficie esa misma estructura mide cuánto se aparta del plano tangente: la segunda forma fundamental, las curvaturas principales como autovalores y la curvatura de Gauss.
- **Curvatura → Elipsoide GRS80 (unidad 17).** Una superficie concreta donde todo sale de una sola simetría: los radios de curvatura M y N, las tres latitudes y el paso de (latitud, longitud, altura) a cartesianas.
- **Elipsoide → Trigonometría esférica (unidad 18).** Entre tres vértices lejanos sobre la superficie los lados son arcos y los ángulos no suman 180°; sobre la esfera hay fórmula cerrada: el triángulo esférico como tres vectores desde el centro, ley del seno y exceso esférico igual al área. Queda abierto para Topografía y Geodesia lo que ya no tiene fórmula cerrada.
- **Trigonometría esférica → Transformaciones conformes (unidad 19).** Medida la superficie, falta volcarla al papel sin torcer los ángulos: la condición conforme es que el jacobiano estire lo mismo en todas las direcciones (h = k, σ₁ = σ₂, el círculo de Tissot sigue siendo círculo), y sobre el elipsoide eso se consigue con la latitud isométrica, que es lo que hacen Mercator y Gauss-Krüger. El arco se cierra en los números complejos de la Clase 1: multiplicar por un complejo era rotar y escalar a la vez, y una matriz [[a, −b], [b, a]] es exactamente un jacobiano conforme.

Los enlaces a cada lección, la clase del curso que cubre y qué construye están en la [tabla de las 20 unidades del README](README.md#recorrido-de-las-20-unidades). Las unidades 13 y 15 a 19 se anticipan a clases que todavía no se dictaron y están marcadas como "anticipación, pendiente de validar".

## Parte 3 — Cómo clonar el repositorio para usarlo o editarlo en una computadora

Sirve para Windows, Mac o Linux. Hace falta Git (para bajar el repositorio) y `uv` (que instala Python y las dependencias solo; no se usa el Python del sistema).

### Paso 1 — Instalar Git y uv

- Git: https://git-scm.com/downloads (en Mac y Linux suele venir instalado o se instala con el gestor de paquetes; en Windows, el instalador de esa página).
- uv: https://docs.astral.sh/uv/getting-started/installation/ . Según esa documentación:

  En Mac o Linux, en una terminal:

  ```
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

  En Windows, en PowerShell:

  ```
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

  Después de instalar, cerrar y volver a abrir la terminal para que `uv` quede en el PATH.

### Paso 2 — Clonar el repositorio

```
git clone https://github.com/gusvarela-fiuba/Sistemas-de-Coordenadas.git
```

### Paso 3 — Instalar las dependencias

```
cd Sistemas-de-Coordenadas
uv sync
```

`uv sync` crea un entorno aislado dentro de la carpeta (`.venv`) con la versión de Python y las bibliotecas exactas del archivo `uv.lock`. No toca nada fuera del repositorio.

### Paso 4 — Abrir, probar y modificar una lección Marimo sin romper el repositorio

Cada lección es un archivo `.py` de marimo. Hay cuatro maneras de trabajar con él, de la más segura a la más libre. Los archivos de las 20 lecciones son `unidades/NN_nombre.py` (los nombres están en la tabla del README; por ejemplo `00_fundamentos`, `01a_punto_quieto`, `14_trigonometria_esferica`, `15_transformaciones_conformes`). Para crear una lección nueva, el molde es `unidades/PLANTILLA_leccion.py` y el procedimiento está en `tools/README.md` ("Cómo agregar una lección en 5 pasos").

**1. Modo proyección, sólo uso (`marimo run`).** No toca el archivo:

```
uv run marimo run unidades/08_cambio_de_base.py
```

Abre la unidad en el navegador sobre el Python local, sin mostrar las celdas de código y sin modificar nunca el `.py`. Es lo ideal para proyectar la lección en clase o para que un alumno la pruebe.

**2. Modo borrador seguro (copia con guion bajo inicial).** Para experimentar con las celdas sin riesgo:

```
cp unidades/08_cambio_de_base.py unidades/_ensayo_08.py
uv run marimo edit unidades/_ensayo_08.py
```

Se abre marimo con la lección completa, celdas incluidas: se puede cambiar el texto, los números de la situación de campo, los casos precargados o los ejercicios, y ver el efecto al momento. Como la copia queda en `unidades/`, encuentra el módulo común `cb104.py`; y como no figura en `mapa/_fragmentos/unidades.yaml`, `tools/build.py` nunca la exporta ni rompe el sitio (el build sólo exporta las unidades listadas ahí; no recorre la carpeta). El guion bajo es la convención para reconocer a simple vista que es un borrador. Conviene no commitearlo, o borrarlo al terminar.

**3. Editar una unidad original sin romper la exportación a WebAssembly.** Si se edita directamente `unidades/08_cambio_de_base.py` (con `uv run marimo edit unidades/08_cambio_de_base.py`), hay tres reglas de oro:

1. No borrar el encabezado `# /// script … # ///` del principio del archivo ni el comentario `# cb104:inline` de la celda `import cb104 as lib  # cb104:inline`: el build los usa para declarar las dependencias e inyectar la biblioteca `cb104.py` dentro de la lección exportada.
2. Las variables que se usan sólo dentro de una celda llevan guion bajo (`_fig`, `_panel`, `_res`). Marimo exige nombres únicos entre celdas y, así, no chocan con las de otras.
3. Antes de dar por bueno un cambio, correr el chequeo; si da 0 avisos (no imprime nada), exportar sólo esa unidad para probar que sigue andando:

```
uv run marimo check --select MW unidades/08_cambio_de_base.py
uv run python tools/build.py --only 08_cambio_de_base
```

**4. Botón de pánico.** Si algo salió mal:

```
git checkout -- unidades/08_cambio_de_base.py
```

Descarta los cambios locales de ese archivo y restaura la versión del repositorio. No deshace lo que ya se commiteó; para eso están `git log` (ver la historia) y `git revert` (deshacer un commit puntual).

**Resumen de los cuatro comandos:**

```
uv run marimo run unidades/08_cambio_de_base.py                          # sólo usar: abre la lección sin mostrar el código y sin tocar el archivo
cp unidades/08_cambio_de_base.py unidades/_ensayo_08.py && uv run marimo edit unidades/_ensayo_08.py   # borrador seguro: se edita la copia
uv run marimo check --select MW unidades/08_cambio_de_base.py            # revisa la unidad editada (0 avisos = bien) y después: uv run python tools/build.py --only 08_cambio_de_base
git checkout -- unidades/08_cambio_de_base.py                            # botón de pánico: descarta los cambios locales de ese archivo
```

### Paso 5 — Levantar el sitio entero en la computadora

```
uv run python tools/build.py
uv run python -m http.server -d site 8765
```

y abrir http://localhost:8765/ en el navegador. El primer comando genera la portada, el mapa, las fichas de clase, copia el apunte y exporta las 20 lecciones a WebAssembly en `site/` (1 a 2 segundos por lección; la primera exportación después de `uv sync` puede tardar unos 40 segundos). El segundo sirve esa carpeta por HTTP, que es necesario: las lecciones exportadas no andan abriendo el archivo directamente con `file://`.

Dos atajos de `tools/build.py` (detalle en `tools/README.md`):

- `uv run python tools/build.py --skip-wasm` regenera portada, mapa, fichas y apunte sin volver a exportar las lecciones (deja lo que ya haya en `site/unidades/`).
- `uv run python tools/build.py --only 08_cambio_de_base` exporta sólo esa lección; el resto del sitio se regenera igual.

### El apunte PDF

El apunte (`apunte/Apunte_Sistemas_de_Coordenadas.pdf`) ya viene compilado y commiteado; el build lo copia a `site/apunte.pdf`, así que ni quien clona ni el servidor de GitHub necesitan TeX. Recompilarlo (después de editar el fuente LaTeX en `apunte/contenido/`) requiere TeX Live con LuaLaTeX y las fuentes Linux Libertine O y DejaVu; desde la carpeta `apunte/`:

```
lualatex Apunte_Sistemas_de_Coordenadas.tex
```

tres pasadas (índice, número total de páginas y referencias cruzadas). Sólo `lualatex`; `xelatex` falla por fuentes. El detalle está en `apunte/README.md`.

## Parte 4 — Cómo adoptar y publicar este curso a nombre de la cátedra

El repositorio está pensado para que la cátedra o un docente lo tome, lo publique bajo su propia cuenta y reemplace o quite el nombre del alumno de la firma. Son cuatro pasos.

### Paso 1 — Fork o clon bajo la cuenta de la cátedra

La vía más simple es el **fork** desde GitHub (botón "Fork" en https://github.com/gusvarela-fiuba/Sistemas-de-Coordenadas): el repositorio queda en `https://github.com/<usuario>/Sistemas-de-Coordenadas`, donde `<usuario>` es la cuenta de la cátedra o del docente. Después se clona ese fork como en la Parte 3 (`git clone https://github.com/<usuario>/Sistemas-de-Coordenadas.git`, `uv sync`).

La alternativa es clonar el original, crear un repositorio vacío en la cuenta de la cátedra y cambiar el `origin` con `git remote set-url origin https://github.com/<usuario>/Sistemas-de-Coordenadas.git`.

### Paso 2 — Cambiar la firma con `tools/adoptar_para_catedra.py`

Desde la raíz del repositorio clonado, primero en seco para ver qué cambiaría:

```
uv run python tools/adoptar_para_catedra.py --dry-run --autor "Cátedra Sistemas de Coordenadas (CB104) — FIUBA" --url-sitio "https://<usuario>.github.io/Sistemas-de-Coordenadas/"
```

y, si el listado es el esperado, el mismo comando sin `--dry-run`:

```
uv run python tools/adoptar_para_catedra.py --autor "Cátedra Sistemas de Coordenadas (CB104) — FIUBA" --url-sitio "https://<usuario>.github.io/Sistemas-de-Coordenadas/"
```

Las opciones son tres:

- `--autor`: el texto que reemplaza el nombre del alumno. Si no se pasa, usa `Cátedra Sistemas de Coordenadas (CB104) · Agrimensura FIUBA`.
- `--url-sitio`: opcional; la URL donde va a quedar publicado el sitio del fork.
- `--dry-run`: muestra qué cambiaría sin tocar ningún archivo.

Qué reemplaza:

- el nombre del alumno en la línea de firma de las 20 unidades interactivas (`unidades/NN_nombre.py`);
- el pie de todas las páginas del sitio web (la constante `PIE` de `tools/build.py`);
- la portada y los metadatos del apunte LaTeX (`\portadaAutor` y `pdfauthor` en `apunte/`);
- si se pasó `--url-sitio`, la URL del sitio en `README.md` y en este `INSTRUCTIVO_DE_USO.md`.

No hace nada más: no toca el contenido de las lecciones ni del apunte, ni la mención del alumno como autor original en los textos del README (esa queda como atribución, ver la nota de donación más abajo).

### Paso 3 — Si se quiere actualizar la portada del PDF

El sitio publica el PDF que está commiteado en `apunte/`, no lo recompila. Para que la portada del apunte muestre el autor nuevo hay que recompilarlo en una computadora con TeX Live, desde la carpeta `apunte/`:

```
lualatex Apunte_Sistemas_de_Coordenadas.tex
```

tres pasadas, y commitear el `Apunte_Sistemas_de_Coordenadas.pdf` regenerado. Si no se hace, el sitio sigue sirviendo el PDF con la firma original; todo lo demás (lecciones y pie del sitio) ya queda con la firma nueva.

### Paso 4 — Commit, push y activar GitHub Pages

```
git add -A
git commit -m "Adopción por la cátedra: firma y URL del sitio"
git push
```

Una vez por repositorio, en GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**. A partir de ahí, cada push a `main` dispara el workflow `.github/workflows/pages.yml`, que instala las dependencias con `uv sync --frozen`, verifica que el mapa de conceptos commiteado coincida con sus fragmentos, corre `marimo check` sobre las lecciones, genera el sitio con `tools/build.py` y lo despliega. El sitio queda en `https://<usuario>.github.io/Sistemas-de-Coordenadas/` en unos minutos; el progreso se sigue en la pestaña "Actions" del repositorio. En los pull requests el mismo workflow corre sólo el build, como verificación.

### Nota de donación

Ver [`NOTA_DE_DONACION.md`](NOTA_DE_DONACION.md).

## Parte 5 — Autoevaluación y banco de preguntas para Moodle

### Qué hay

Armamos un banco de 120 preguntas de opción múltiple: seis por unidad, dos elementales, dos medias y dos avanzadas. Cada pregunta tiene cuatro opciones, una sola correcta, y una explicación para cada opción. Las preguntas aparecen en dos lugares: dentro de cada unidad, al final de los ejercicios, y en una página propia, `autoevaluacion.html` (https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/autoevaluacion.html), que tiene tres modos:

- **Práctica.** Elegimos una unidad (o todas) y un nivel (o todos). Al marcar una opción vemos de inmediato si acertamos y por qué; si fallamos, también cuál era la correcta. El botón "Mezclar" vuelve a barajar preguntas y opciones. No guarda nada.
- **Simulacro.** Veinte preguntas, una por unidad y en el orden de las unidades, con el nivel sorteado. No hay devolución hasta "Entregar"; entonces vemos el puntaje total, el puntaje por nivel y la corrección completa con explicaciones. "Nuevo simulacro" sortea otro. No guarda nada.
- **Evaluación (4 intentos).** Treinta preguntas: una por unidad más diez al azar. Al entregar vemos el puntaje y qué unidades acertamos, sin explicaciones. Cada intento se anota (fecha, puntaje y nivel de cada pregunta) y se pueden hacer cuatro; al agotarlos queda el historial, la mejor nota y un botón para borrarlo (pide un segundo clic para confirmar). También se puede descargar el resultado como archivo de texto.

El registro de la evaluación vive sólo en el navegador de cada alumno (`localStorage`, clave `cb104_evaluacion`): no se envía a ningún servidor, no lo ve la cátedra y se pierde si se borran los datos del sitio o se cambia de navegador o de computadora. Por eso el botón "Descargar resultado" es la forma de dejar constancia.

### Cómo importar el banco en Moodle

El archivo es `moodle/moodle_banco_120_preguntas_cb104.xml` (el sitio publica una copia en `moodle_banco_120_preguntas_cb104.xml`, enlazada al pie de la página de autoevaluación). Para cargarlo:

1. En el curso de Moodle, entramos en **Más → Banco de preguntas → Importar**.
2. Elegimos el formato **Moodle XML** y subimos el archivo.
3. Al importar se crean las categorías: una por unidad y, dentro de cada una, una por nivel (60 categorías en total, con las 120 preguntas repartidas).
4. Cada pregunta queda con puntaje 100 para la opción correcta y 0 para las otras, y con penalidad de 0,33 por intento fallido.

Para armar un cuestionario con preguntas al azar por categoría: creamos el cuestionario, entramos en **Editar cuestionario → Agregar → una pregunta aleatoria** y elegimos una categoría (por ejemplo, el nivel medio de una unidad). Repetimos por cada unidad o nivel que queramos incluir; así cada alumno recibe una combinación distinta. El detalle del procedimiento está en `campus/README.md`.

### Cómo editar o agregar preguntas

La fuente editable son los archivos `unidades/_banco/bloque_N.py`, uno por bloque de unidades; el esquema de cada pregunta está en `unidades/_banco/README.md` (identificador, nivel, enunciado con LaTeX entre `$...$`, cuatro opciones con una correcta y la explicación de cada una). `unidades/banco_autoevaluacion.py` es generado: no se edita a mano. Después de tocar un bloque:

```
uv run python tools/merge_banco.py
uv run python tools/build.py
```

El primer comando valida los fragmentos y regenera el módulo del banco. El segundo regenera todo el sitio, incluidos `autoevaluacion.html` y el XML de Moodle (`moodle/moodle_banco_120_preguntas_cb104.xml`, que `tools/build.py` vuelve a generar y copia a `site/`).
