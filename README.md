# Sistemas de Coordenadas (CB104) — guía de estudio interactiva y apunte

Trabajo final de Sistemas de Coordenadas (CB104, FIUBA), Gustavo Varela. Es una guía de estudio de la materia (Agrimensura): un apunte formal y un recorrido interactivo, pensados como herramienta reutilizable para quien venga después.

Todo se usa desde el navegador, sin instalar nada:

- **Curso interactivo online (20 unidades en el navegador):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/
- **Apunte formal y guías resueltas en PDF (137 páginas):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/apunte.pdf
- **Mapa interactivo de conceptos:** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/mapa.html
- **Autoevaluación (120 preguntas, 3 modos):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/autoevaluacion.html

**[Instructivo de uso, guía pedagógica y cómo clonar o adoptar este repositorio (`INSTRUCTIVO_DE_USO.md`)](INSTRUCTIVO_DE_USO.md)**

**[Curso interactivo: las 20 simulaciones con sus controles, ejercicios y enlaces (`CURSO_INTERACTIVO.md`)](CURSO_INTERACTIVO.md)**

## Cómo usar y navegar este material

### Autoevaluación

Cada unidad cierra con seis preguntas de opción múltiple (dos elementales, dos medias, dos avanzadas), y la página [autoevaluacion.html](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/autoevaluacion.html) reúne las 120 en tres modos: práctica con devolución inmediata, simulacro de 20 preguntas y evaluación de 4 intentos. El banco completo para importar en Moodle está en [`moodle/`](moodle/).

### Las tres capas

De la más guiada a la más completa:

1. **El hilo conductor** (la portada del sitio): las 20 unidades interactivas, construidas ladrillo a ladrillo, una por unidad, en el orden del programa de la materia. Cada unidad tiene su pregunta de campo, su gancho de agrimensura y la unidad interactiva, que corre en el navegador. Es el recorrido para estudiar.
2. **El mapa de conceptos** ([mapa.html](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/mapa.html)): los conceptos de los capítulos del apunte como grafo, con filtro de ruta (troncal / todo) y un control "hasta el capítulo N" que oculta lo posterior. Es la herramienta de repaso: sirve para ver de qué depende cada concepto y qué habilita.
3. **El apunte formal** ([apunte.pdf](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/apunte.pdf)): las demostraciones en LaTeX, las guías resueltas y las deducciones completas. Se organiza así: capítulo 0 (Antes de empezar), capítulos 1 a 15 por tema, complementos C1 a C4 y apéndices. Cada unidad enlaza por sección a la parte del apunte que la respalda, así que se puede ir de la pantalla al papel sin buscar.

### Por qué empieza en la Unidad 0 — Fundamentos

La Unidad 0 es el encuadre del curso: el idioma que la materia usa desde el primer día y que el CBC no da. Son cinco ladrillos, en este orden:

1. **Conjuntos, operaciones y grupos:** las transformaciones forman un grupo; componer y deshacer son las operaciones.
2. **Los cuerpos R y C:** los números con los que se escriben las coordenadas, y por qué multiplicar por un complejo ya es girar.
3. **Espacio afín (mojones) y espacio vectorial:** los puntos del terreno son una cosa; los vectores nacen al plantar un origen, y desde ahí todo vector es un punto.
4. **El espacio dual V\*:** una fila es una forma lineal, una regla que mide vectores. El gradiente vive ahí y no es un vector.
5. **Producto interno y métrica G:** la cinta métrica que vectores y formas solos no tienen; es la que después se vuelve la primera forma fundamental.

La situación de campo de la Unidad 0 es una loma con sus curvas de nivel: calcular hacia dónde sube más empinado con los dos números del gradiente "como flecha" da mal cuando la grilla no es cuadrada, y eso muestra por qué el gradiente es una regla y no una flecha.

### Los 6 pasos de cada unidad

Todas las unidades siguen el mismo molde, siempre de lo conceptual y geométrico al cálculo. Los nombres de sección son fijos:

- **0. Situación de campo y predicción.** Un problema de agrimensura concreto y una predicción sin cuentas (opción múltiple); cada respuesta equivocada explica el error concreto, no dice sólo "incorrecto".
- **1. Hecho geométrico.** Qué se conserva y qué cambia, antes de cualquier fórmula.
- **2. Manipulación.** Figuras Plotly de tres capas (grilla antes en gris, grilla después en teal, y el objeto), con deslizadores y casos precargados (identidad, 90°, un ángulo cualquiera, y los contraejemplos: reflexión, corte, determinante cero). Álgebra y figura comparten el código de colores: cada columna de la matriz se pinta del color del vector que representa.
- **3. Cuenta a mano y código lado a lado.** La misma cuenta en lápiz y en NumPy, con la matriz coloreada por columnas.
- **4. Python de hoy.** Las dos o tres líneas de Python que la unidad deja aprendidas, aplicadas al problema de campo.
- **5. Ejercicios.** Lápiz y código con hueco en un editor en vivo, con autocorrección (`np.allclose` contra la referencia).

Al cierre, un anexo "Dónde está la demostración" enlaza las secciones del apunte. Lo interactivo es una muestra; las demostraciones formales son las del apunte.

### Seis animaciones en bucle

Seis bucles cortos de ida y vuelta (en `animaciones/`, como `.mp4` en las unidades y `.gif` acá) sintetizan el hecho geométrico antes de la manipulación:

![Dualidad punto–gradiente](animaciones/01_dualidad_gradiente.gif)

*Dualidad punto–gradiente* — al estirar el Este por 2 los mojones van con A, las rectas de nivel de ω = (2, 1) van con A⁻¹, el mojón (1, 1) sigue leyendo 3 y la flecha ingenua Aωᵀ pierde la perpendicularidad. Unidad 0 (Fundamentos) y Unidad 8 (Formas lineales y dualidad).

![Coordenadas homogéneas: pentágono en 3D](animaciones/02_homogeneas_pentagono_3d.gif)

*Coordenadas homogéneas en 3D* — los vértices del pentágono son rayos desde el origen que cortan la lámina z = 1; H(s) mueve los rayos y el pentágono se deforma proyectivamente. Unidad 7 (Proyectivas); también sirve en la Unidad 6 (Afinidades y coordenadas homogéneas).

![Cambio de base: el viaje de T = A T_diag A⁻¹](animaciones/03_cambio_de_base_viaje.gif)

*El viaje del cambio de base* — las tres etapas de T = A·T_diag·A⁻¹: leer p en la base de autovectores, estirar cada dirección propia (λ₁ = 3, λ₂ = 1) y volver a la canónica. Unidad 12 (Cambio de base y diagonalización).

![SVD: del círculo unidad a la elipse](animaciones/04_svd_circulo_a_elipse.gif)

*SVD: del círculo a la elipse* — el círculo unidad con v₁, v₂ encadena Vᵀ (giro de entrada), Σ (estiramientos) y U (giro de salida); la vuelta deshace el camino. Unidad 13 (Cambio de base, SVD e inversas).

![Elipsoide: Euler y Meusnier](animaciones/05_elipsoide_euler_meusnier.gif)

*Euler y Meusnier sobre el elipsoide* — el plano normal gira en acimut (Euler: el círculo osculador entre M y N) y luego se inclina hasta el paralelo de radio N cos φ (Meusnier). Unidad 16 (Curvatura como forma cuadrática) y Unidad 17 (Geometría del elipsoide).

![Tissot: equidistante vs. Mercator](animaciones/06_conforme_tissot_mercator.gif)

*Tissot: cilíndrica equidistante contra Mercator* — lado a lado, la cilíndrica equidistante (h = 1, no conforme) aplasta los círculos de Tissot en elipses y tuerce las dos visuales a 90°, mientras Mercator, con la latitud isométrica, manda cuadraditos a cuadraditos y conserva los círculos y el ángulo. Unidad 19 (Transformaciones conformes).

## Recorrido de las 20 unidades

El orden es el del hilo conductor de la portada. "Tema del programa" indica qué parte del programa cubre cada unidad.

| Unidad | Unidad (enlace) | Tema del programa | Qué construye |
|---|---|---|---|
| Unidad 0 | [Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia)](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/00_fundamentos/index.html) | capítulos 1, 5 y 10 (desarrollo complementario) | Los cinco ladrillos: grupo de transformaciones, cuerpos R y C, todo vector es un punto, el dual donde vive el gradiente, y la métrica G. La loma donde el gradiente no es un vector. |
| Unidad 1 | [Rotaciones I: el punto no se movió](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01a_punto_quieto/index.html) | capítulo 1 | La rotación pasiva: giran los ejes, cambian las coordenadas, el mojón no se mueve. |
| Unidad 2 | [Rotaciones II: la rotación en el plano](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01b_rotacion_plano/index.html) | capítulo 1 | La rotación activa como matriz ortogonal de determinante +1: sus columnas son adónde van los ejes, y el mismo giro como número complejo. |
| Unidad 3 | [Rotaciones III: tres ejes y el orden importa](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01c_rotaciones_3d/index.html) | capítulos 1 y 2 | Las rotaciones alrededor de cada eje de R3, la composición que no conmuta y Euler–Rodrigues: toda composición es un solo giro alrededor de un eje. |
| Unidad 4 | [Producto interno: proyección, longitud, ángulo](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/02_producto_interno/index.html) | capítulo 1 | La cuenta que mide largo, ángulo y proyección desde las coordenadas, y por qué una rotación la conserva. |
| Unidad 5 | [Reflexiones y similaridades](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/03_reflexiones_similaridades/index.html) | capítulos 2 a 4 | La reflexión (determinante −1) y la similaridad: rotar, escalar y trasladar, con su centro fijo. |
| Unidad 6 | [Afinidades y coordenadas homogéneas](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/04_afines_homogeneas/index.html) | capítulos 3 y 4 | La afinidad como matriz de 3×3 sobre coordenadas homogéneas: la traslación entra en la matriz, componer es multiplicar y el área se multiplica por el determinante. |
| Unidad 7 | [Proyectivas: la foto del dron y el pentágono](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/05_proyectivas/index.html) | complemento C1 | La homografía sobre rayos, la recta al infinito y la razón doble. El pentágono proyectivo como caso precargado. |
| Unidad 8 | [Formas lineales y dualidad](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/06_formas_lineales/index.html) | capítulo 5 | La forma lineal como regla graduada, el espacio dual y la regla arrastrada para que la lectura no cambie. Un ejercicio de formas lineales y una aplicación a Support Vector Machines (SVM): una SVM es una forma lineal con margen. |
| Unidad 9 | [Cuña y determinante: el detector de colinealidad](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07a_cuna_determinante/index.html) | capítulo 6 | El producto cuña y el determinante como área o volumen orientado: cero exactamente cuando hay colinealidad. |
| Unidad 10 | [Núcleo y autovectores: las direcciones que no giran](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07b_nucleo_autovectores/index.html) | capítulos 6 y 7 | El núcleo y los autovectores: las direcciones que caen sobre sí mismas, encontradas con el polinomio característico. |
| Unidad 11 | [Autovalores en 3D y puntos fijos proyectivos](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07c_autovalores_3d_puntos_fijos/index.html) | capítulo 7 | Autovectores en R3 por producto cruz de dos filas: el eje de una rotación y los puntos fijos de una homografía. |
| Unidad 12 | [Cambio de base y diagonalización](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/08_cambio_de_base/index.html) | capítulo 9 | La matriz de cambio de base (columnas = ejes nuevos), la transformación vista en la grilla nueva y la diagonalización. Las dos grillas y el esquema de cambio de base. |
| Unidad 13 | [Cambio de base, SVD e inversas](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/09_cambio_de_base_svd/index.html) | capítulos 8 y 11 | La SVD: dos bases ortonormales, la inversa y la pseudoinversa con sus cuatro subespacios. La SVD en vivo sobre el DEM real de la Precordillera de Mendoza, con el rango elegido a mano. |
| Unidad 14 | [Jacobiano y primera forma fundamental](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/10_jacobiano_primera_forma/index.html) | capítulo 10 | El jacobiano de 3×2 de una superficie y la primera forma fundamental: el largo de un paso medido sólo con los números de la grilla. |
| Unidad 15 | [Cuatro problemas: regresión, círculos, Procrustes, regresión total](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/11_cuatro_problemas/index.html) | capítulo 12 | Las ecuaciones normales cuatro veces: recta de ajuste (regresión), punto por distancias (intersección de círculos), Procrustes y regresión total. Los cuatro problemas resueltos. |
| Unidad 16 | [Curvatura como forma cuadrática](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/12_curvatura/index.html) | capítulo 13 | La segunda forma fundamental, la curvatura normal en cada rumbo, las curvaturas principales como autovalores y la curvatura de Gauss. |
| Unidad 17 | [Geometría del elipsoide](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/13_elipsoide/index.html) | capítulo 14 | El elipsoide de revolución GRS80: los radios de curvatura M y N, las tres latitudes y el paso de (latitud, longitud, altura) a cartesianas. |
| Unidad 18 | [Trigonometría esférica](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/14_trigonometria_esferica/index.html) | capítulo 15 | El triángulo esférico como tres vectores desde el centro: lados por producto interno, ángulos por producto cruz, ley del seno y el exceso esférico igual al área. |
| Unidad 19 | [Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/15_transformaciones_conformes/index.html) | capítulos 14 y 15 (desarrollo complementario) | Las cuatro caras de la conformidad (multiplicar por un complejo, una matriz [[a, −b], [b, a]], un jacobiano con σ₁ = σ₂, un círculo de Tissot que sigue siendo círculo), la latitud isométrica, Mercator y Gauss-Krüger: el arco que empezó en los números complejos se cierra en el plano cartográfico. |

## Guías de problemas resueltas

### En el apunte (PDF)

El apéndice "Material de práctica y notebooks" del apunte tiene un índice general que dice dónde está resuelto cada tipo de problema (en el apunte o en los ejercicios de las unidades). Lo que hay resuelto en el PDF:

- **Guía de transformaciones euclídeas y similaridades** (reflexiones puntuales y axiales, traslación, rotación, homotecia, similaridades; teoremas 1 a 6): enunciados y resolución completa, ejercicio por ejercicio.
- **Guía de afinidades**: sus ejercicios resueltos, cada uno en los «Ejercicios con solución» del capítulo de su tema (afinidades en el 4, reflexiones en el 3, autovalores de matrices ortogonales en el 7), más la composición práctica de rotación y escala.
- **El pentágono proyectivo**: teoría de homografías, puntos y rectas fijas, y el ejercicio del pentágono regular con cuentas y script.
- **SVM como formas lineales**: la aplicación a Inteligencia Artificial, con la máquina de vectores de soporte vista como una forma lineal con margen.
- **SVD sobre el DEM de la Precordillera de Mendoza**: dos SVD a mano y la compresión por rango de un modelo digital de elevación real.
- **Los cuatro problemas**: guía resuelta de regresión, intersección de círculos, Procrustes y regresión total.
- **Deducciones del elipsoide**: latitudes, radios de curvatura y conversión (GRS80 en 45° y en −34,6°), arco de meridiano y proyecciones, trigonometría esférica con el octante y tres ciudades.

## Cómo citar

Varela, G. (2026). *Sistemas de Coordenadas: apunte, unidades interactivas y ejercicios*. Trabajo final de Sistemas de Coordenadas, CB104, FIUBA.

Metadatos de cita en [`CITATION.cff`](CITATION.cff); condiciones de uso en la [nota de donación](NOTA_DE_DONACION.md).

## Para desarrolladores: ejecución local, estructura y publicación

### Cómo correr local

Todo Python va por `uv`; no se usa el Python del sistema.

```
uv sync
uv run python tools/build.py --skip-wasm      # portada, mapa, fichas y apunte.pdf en site/ (sin exportar unidades)
uv run python -m http.server -d site 8765     # http://localhost:8765/
```

`uv run python tools/build.py` sin `--skip-wasm` exporta además las 20 unidades a WebAssembly (1–2 s cada una, ~27 MB por unidad en `site/unidades/`); para una sola, `--only NN_nombre`. Las unidades exportadas necesitan HTTP, no andan desde `file://`. Para editar una unidad: `uv run marimo edit unidades/NN_nombre.py`. El flujo completo, el molde de unidad y cómo agregar una están en `tools/README.md`.

Para usar o tocar una unidad sin romper nada (detalle en la Parte 3, Paso 4 de [INSTRUCTIVO_DE_USO.md](INSTRUCTIVO_DE_USO.md)):

```
uv run marimo run unidades/08_cambio_de_base.py                          # sólo usar: abre la unidad sin mostrar el código y sin tocar el archivo
cp unidades/08_cambio_de_base.py unidades/_ensayo_08.py && uv run marimo edit unidades/_ensayo_08.py   # borrador seguro: se edita la copia
uv run marimo check --select MW unidades/08_cambio_de_base.py            # revisa la unidad editada (0 avisos = bien) y después: uv run python tools/build.py --only 08_cambio_de_base
git checkout -- unidades/08_cambio_de_base.py                            # botón de pánico: descarta los cambios locales de ese archivo
```

El apunte se compila aparte con TeX Live (LuaLaTeX, tres pasadas desde `apunte/`, ver `apunte/README.md`); el PDF compilado está commiteado y el build lo copia a `site/apunte.pdf`, así que ni el runner de GitHub ni quien clona necesitan TeX.

Para regenerar el PDF sin riesgo de commitear una copia truncada: `scripts/compilar_pdf.sh` desde la raíz, y activar una vez por clon el hook que lo verifica con `git config core.hooksPath .githooks` (ver `scripts/README.md`).

### Estructura

```
unidades/   unidades interactivas en marimo (NN_nombre.py), módulo común cb104.py y PLANTILLA_leccion.py
mapa/       fuente editable del mapa (_fragmentos/*.yaml), mapa.yaml generado, ESQUEMA.md y CONCEPTOS.md
clases/     fichas temáticas por capítulo
apunte/     apunte LaTeX (fuente por capítulo) y el PDF compilado
tools/      build.py (sitio), merge_mapa.py (mapa), bootstrap_github.sh y el README con el flujo
ejercicios/ resoluciones del material Julia del curso y sus ports a Python
moodle/     banco de preguntas para importar en Moodle
datos/      datos de apoyo (los archivos pesados quedan fuera del repo)
site/       salida del build (ignorada por git); la publica .github/workflows/pages.yml
```

### Publicación

Cada push a `main` corre `.github/workflows/pages.yml`: `uv sync --frozen`, verificación de que `mapa/mapa.yaml` coincide con los fragmentos, `marimo check` de las unidades, `tools/build.py` y despliegue a GitHub Pages. En los pull requests corre sólo el build, como CI. Una vez por repo: Settings → Pages → Source: GitHub Actions.
