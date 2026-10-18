# Sistemas de Coordenadas (CB104) — guía de estudio interactiva y apunte

Guía de estudio de la materia CB104 Sistemas de Coordenadas (Agrimensura, FIUBA), escrita por Gustavo Varela como alumno de la cursada 2026 (2C2026, profesor Javier Clavijo). No es material oficial de la cátedra: es la manera en que un alumno recorre la materia, con dos objetivos, aprobarla y dejar una herramienta interactiva reutilizable para quien venga después.

Todo se usa desde el navegador, sin instalar nada:

- **Curso interactivo online (20 unidades en el navegador):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/
- **Apunte formal y guías resueltas en PDF (137 páginas):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/apunte.pdf
- **Mapa interactivo de conceptos:** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/mapa.html
- **Autoevaluación (120 preguntas, 3 modos):** https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/autoevaluacion.html

**[Instructivo de uso, guía pedagógica y cómo clonar o adoptar este repositorio para la cátedra (`INSTRUCTIVO_DE_USO.md`)](INSTRUCTIVO_DE_USO.md)**

**[Curso interactivo: las 20 simulaciones con sus controles, ejercicios y enlaces (`CURSO_INTERACTIVO.md`)](CURSO_INTERACTIVO.md)**

## Cómo usar y navegar este material

### Autoevaluación

Cada unidad cierra con seis preguntas de opción múltiple (dos elementales, dos medias, dos avanzadas), y la página [autoevaluacion.html](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/autoevaluacion.html) reúne las 120 en tres modos: práctica con devolución inmediata, simulacro de 20 preguntas y evaluación de 4 intentos. El banco completo para importar en Moodle está en [`campus/`](campus/).

### Las tres capas

De la más guiada a la más completa:

1. **El hilo conductor** (la portada del sitio): las 20 unidades interactivas, construidas ladrillo a ladrillo, una por lección, en el orden en que el profesor da la materia. Cada unidad tiene su pregunta de campo, su gancho de agrimensura, su estado de procedencia y la lección, que corre en el navegador. Es el recorrido para cursar.
2. **El mapa de conceptos** ([mapa.html](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/mapa.html)): los conceptos de las 14 clases como grafo, con filtro de ruta (troncal / todo) y un control "hasta la clase N" que oculta lo que todavía no se dio. Es la herramienta de repaso: sirve para ver de qué depende cada concepto y qué habilita.
3. **El apunte formal** ([apunte.pdf](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/apunte.pdf)): las demostraciones en LaTeX, las guías resueltas y las deducciones completas. Cada unidad enlaza por sección a la parte del apunte que la respalda, así que se puede ir de la pantalla al papel sin buscar.

### Por qué empieza en la Unidad 0 — Fundamentos

La Unidad 0 es encuadre complementario del curso, no contenido de la cátedra: el idioma que la materia usa desde la primera clase y que el CBC no da. Son cinco ladrillos, en este orden:

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

El orden es el del hilo conductor de la portada. "Clase del curso" es la clase del esqueleto del profesor que cubre cada unidad.

| Unidad | Lección (enlace) | Clase del curso | Qué construye |
|---|---|---|---|
| Unidad 0 | [Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia)](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/00_desaprender_el_cbc/index.html) | clases 01, 04 y 09 (desarrollo complementario) | Los cinco ladrillos: grupo de transformaciones, cuerpos R y C, todo vector es un punto, el dual donde vive el gradiente, y la métrica G. La loma donde el gradiente no es un vector. |
| Unidad 1 | [Rotaciones I: el punto no se movió](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01a_punto_quieto/index.html) | clase 01 | La rotación pasiva: giran los ejes, cambian las coordenadas, el mojón no se mueve. |
| Unidad 2 | [Rotaciones II: la rotación en el plano](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01b_rotacion_plano/index.html) | clase 01 | La rotación activa como matriz ortogonal de determinante +1: sus columnas son adónde van los ejes, y el mismo giro como número complejo. |
| Unidad 3 | [Rotaciones III: tres ejes y el orden importa](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01c_rotaciones_3d/index.html) | clases 01–02 | Las rotaciones alrededor de cada eje de R3, la composición que no conmuta y Euler–Rodrigues: toda composición es un solo giro alrededor de un eje. |
| Unidad 4 | [Producto interno: proyección, longitud, ángulo](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/02_producto_interno/index.html) | clase 01 | La cuenta que mide largo, ángulo y proyección desde las coordenadas, y por qué una rotación la conserva. |
| Unidad 5 | [Reflexiones y similaridades](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/03_reflexiones_similaridades/index.html) | clases 02–03 | La reflexión (determinante −1) y la similaridad: rotar, escalar y trasladar, con su centro fijo. |
| Unidad 6 | [Afinidades y coordenadas homogéneas](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/04_afines_homogeneas/index.html) | clase 03 | La afinidad como matriz de 3×3 sobre coordenadas homogéneas: la traslación entra en la matriz, componer es multiplicar y el área se multiplica por el determinante. |
| Unidad 7 | [Proyectivas: la foto del dron y el pentágono del profesor](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/05_proyectivas/index.html) | clase 03p | La homografía sobre rayos, la recta al infinito y la razón doble. El pentágono proyectivo del pizarrón del profesor como caso precargado. |
| Unidad 8 | [Formas lineales y dualidad](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/06_formas_lineales/index.html) | clase 04 | La forma lineal como regla graduada, el espacio dual y la regla arrastrada para que la lectura no cambie. El ejercicio de formas lineales del 30/9 y una aplicación a Support Vector Machines (SVM): una SVM es una forma lineal con margen. |
| Unidad 9 | [Cuña y determinante: el detector de colinealidad](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07a_cuna_determinante/index.html) | clase 05 | El producto cuña y el determinante como área o volumen orientado: cero exactamente cuando hay colinealidad. |
| Unidad 10 | [Núcleo y autovectores: las direcciones que no giran](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07b_nucleo_autovectores/index.html) | clases 05–06 | El núcleo y los autovectores: las direcciones que caen sobre sí mismas, encontradas con el polinomio característico. |
| Unidad 11 | [Autovalores en 3D y puntos fijos proyectivos](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/07c_autovalores_3d_puntos_fijos/index.html) | clase 06 | Autovectores en R3 por producto cruz de dos filas: el eje de una rotación y los puntos fijos de una homografía. |
| Unidad 12 | [Cambio de base y diagonalización](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/08_cambio_de_base/index.html) | clase 08 | La matriz de cambio de base (columnas = ejes nuevos), la transformación vista en la grilla nueva y la diagonalización. Las dos grillas y el esquema de los muñequitos del pizarrón del 30/9. |
| Unidad 13 | [Cambio de base, SVD e inversas](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/09_cambio_de_base_svd/index.html) | clases 07 y 10 | La SVD: dos bases ortonormales, la inversa y la pseudoinversa con sus cuatro subespacios. La SVD en vivo sobre el DEM real de la Precordillera de Mendoza, con el rango elegido a mano. |
| Unidad 14 | [Jacobiano y primera forma fundamental](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/10_jacobiano_primera_forma/index.html) | clase 09 | El jacobiano de 3×2 de una superficie y la primera forma fundamental: el largo de un paso medido sólo con los números de la grilla. |
| Unidad 15 | [Cuatro problemas: regresión, círculos, Procrustes, regresión total](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/11_cuatro_problemas/index.html) | clase 11 | Las ecuaciones normales cuatro veces: recta de ajuste (regresión), punto por distancias (intersección de círculos), Procrustes y regresión total. Los cuatro problemas de la clase 11 resueltos. |
| Unidad 16 | [Curvatura como forma cuadrática](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/12_curvatura/index.html) | clase 12 | La segunda forma fundamental, la curvatura normal en cada rumbo, las curvaturas principales como autovalores y la curvatura de Gauss. |
| Unidad 17 | [Geometría del elipsoide](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/13_elipsoide/index.html) | clase 13 | El elipsoide de revolución GRS80: los radios de curvatura M y N, las tres latitudes y el paso de (latitud, longitud, altura) a cartesianas. |
| Unidad 18 | [Trigonometría esférica](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/14_trigonometria_esferica/index.html) | clase 14 | El triángulo esférico como tres vectores desde el centro: lados por producto interno, ángulos por producto cruz, ley del seno y el exceso esférico igual al área. |
| Unidad 19 | [Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/15_transformaciones_conformes/index.html) | clases 13–14 (desarrollo complementario) | Las cuatro caras de la conformidad (multiplicar por un complejo, una matriz [[a, −b], [b, a]], un jacobiano con σ₁ = σ₂, un círculo de Tissot que sigue siendo círculo), la latitud isométrica, Mercator y Gauss-Krüger: el arco que empezó en los complejos de la Clase 1 se cierra en el plano cartográfico. |

Las unidades 13 y 15 a 19 se anticipan a clases que todavía no se dictaron (ver Procedencia y trazabilidad).

## Guías de problemas y entregas resueltas

### En el apunte (PDF)

El apéndice "Material de clase y notebooks" del apunte tiene un índice general que dice dónde está resuelto cada tipo de problema (en el apunte, en `entregas/` o en los ejercicios de las unidades). Lo que hay resuelto en el PDF:

- **Guía de transformaciones euclídeas y similaridades** (reflexiones puntuales y axiales, traslación, rotación, homotecia, similaridades; teoremas 1 a 6): enunciados originales y resolución completa, ejercicio por ejercicio.
- **Guía de afinidades**: los seis ejercicios de la clase del 9/9, más la composición práctica de rotación y escala.
- **El pentágono proyectivo**: teoría de homografías, puntos y rectas fijas, y el ejercicio del pentágono regular con cuentas y script.
- **SVM como formas lineales**: la aplicación a Inteligencia Artificial, con la máquina de vectores de soporte vista como una forma lineal con margen.
- **SVD sobre el DEM de la Precordillera de Mendoza**: dos SVD a mano y la compresión por rango de un modelo digital de elevación real.
- **Los cuatro problemas de la clase 11**: guía resuelta de regresión, intersección de círculos, Procrustes y regresión total.
- **Deducciones del elipsoide**: latitudes, radios de curvatura y conversión (GRS80 en 45° y en −34,6°), arco de meridiano y proyecciones, trigonometría esférica con el octante y tres ciudades.
- **Fe de erratas de las fuentes**: precisiones sobre la guía de euclídeas y afinidades, y cuatro erratas del apunte del elipsoide del profesor confirmadas con una cuenta nuestra en NumPy.

### En `entregas/`

Trabajos prácticos entregados al campus (alumno Gustavo Varela, padrón 56798), con PDF listo, fuente LaTeX y scripts de verificación NumPy:

- `Afinidades_Ejercicios_Varela_56798.pdf` — los seis ejercicios de la clase del 9/9 (fuente en `afinidades/`).
- `Pentagono_Proyectivas_Varela_56798.pdf` — ejercicio del 16/9 con la aclaración del 18/9: pentágono regular (tres casos y composiciones) y el mismo problema sobre un pentágono irregular con enteros, más la parte conceptual (fuente en `pentagono/`, con un notebook marimo interactivo y su export estático). La carpeta `Pentagono_Proyectivas_Varela_56798/` es el paquete para mandar al profesor; `entregas/README.md` aclara cuál de las dos versiones del PDF vale.
- `Afinidades_Triangulo_Varela_56798.pdf` — llevar un triángulo sobre otro con afinidades axiales; material extra, no fue pedido.

## Procedencia y trazabilidad

Cada clase lleva dos etiquetas independientes, visibles en las fichas y en las unidades de la portada:

- **Procedencia** (de dónde sale el contenido): `con transcripción` (hay transcripción de la clase dictada en 2026); `reconstruida` (armada desde el material del campus y la cursada 2025, sin transcripción); `no dictada` (la clase no se dio: todavía no llegó, o en 2C2026 se salteó, como la 02); `anticipación, pendiente de validar` (lección armada antes de que la clase se dicte; hoy las clases 10–14, es decir las lecciones 11, 12, 13, 14 y 15; la clase 07 se dictó el 7/10 sin transcripción).
- **Validación** (cuánto se revisó): `validación pendiente`; `revisado` (revisada contra el material, todavía sin la cátedra); `validado por la cátedra` (confirmada por el profesor). Hoy todas las clases están en `pendiente`.

Nada se presenta como contenido de la cátedra si no se dio. Las lecciones tienen además un estado propio (`piloto`, `migrada`, `legacy`, `pendiente`) que dice si se exportan; el estado de cada unidad (lista / en clase / todavía no) lo calcula el build.

El diseño del hilo conductor (principios, secuencia de una lección, datos que lo alimentan, estado actual) está en `docs/camino.md`.

## Para desarrolladores: ejecución local, estructura, publicación y licencia

### Cómo correr local

Todo Python va por `uv`; no se usa el Python del sistema.

```
uv sync
uv run python tools/build.py --skip-wasm      # portada, mapa, fichas y apunte.pdf en site/ (sin exportar lecciones)
uv run python -m http.server -d site 8765     # http://localhost:8765/
```

`uv run python tools/build.py` sin `--skip-wasm` exporta además las 20 lecciones a WebAssembly (1–2 s cada una, ~27 MB por lección en `site/unidades/`); para una sola, `--only NN_nombre`. Las lecciones exportadas necesitan HTTP, no andan desde `file://`. Para editar una lección: `uv run marimo edit unidades/NN_nombre.py`. El flujo completo, el molde de lección y cómo agregar una están en `tools/README.md`.

Para usar o tocar una lección sin romper nada (detalle en la Parte 3, Paso 4 de [INSTRUCTIVO_DE_USO.md](INSTRUCTIVO_DE_USO.md)):

```
uv run marimo run unidades/08_cambio_de_base.py                          # sólo usar: abre la lección sin mostrar el código y sin tocar el archivo
cp unidades/08_cambio_de_base.py unidades/_ensayo_08.py && uv run marimo edit unidades/_ensayo_08.py   # borrador seguro: se edita la copia
uv run marimo check --select MW unidades/08_cambio_de_base.py            # revisa la unidad editada (0 avisos = bien) y después: uv run python tools/build.py --only 08_cambio_de_base
git checkout -- unidades/08_cambio_de_base.py                            # botón de pánico: descarta los cambios locales de ese archivo
```

El apunte se compila aparte con TeX Live (LuaLaTeX, tres pasadas desde `apunte/`, ver `apunte/README.md`); el PDF compilado está commiteado y el build lo copia a `site/apunte.pdf`, así que ni el runner de GitHub ni quien clona necesitan TeX.

### Estructura

```
unidades/   lecciones marimo (NN_nombre.py), módulo común cb104.py y PLANTILLA_leccion.py
mapa/       fuente editable del mapa (_fragmentos/*.yaml), mapa.yaml generado, ESQUEMA.md y CONCEPTOS.md
clases/     fichas por clase, siguiendo el esqueleto del profesor
apunte/     apunte LaTeX (fuente por capítulo) y el PDF compilado
docs/       camino.md (diseño de la guía y estado) y auditoria.md (auditoría del material)
tools/      build.py (sitio), merge_mapa.py (mapa), bootstrap_github.sh y el README con el flujo
ejercicios/ resoluciones del material Julia del curso y sus ports a Python
entregas/   trabajos prácticos entregados
fuentes/    transcripciones de clase y material del campus
datos/      datos de apoyo (los archivos pesados quedan fuera del repo)
site/       salida del build (ignorada por git); la publica .github/workflows/pages.yml
```

### Publicación

Cada push a `main` corre `.github/workflows/pages.yml`: `uv sync --frozen`, verificación de que `mapa/mapa.yaml` coincide con los fragmentos, `marimo check` de las lecciones, `tools/build.py` y despliegue a GitHub Pages. En los pull requests corre sólo el build, como CI. Una vez por repo: Settings → Pages → Source: GitHub Actions.

### Licencia

Doble esquema: el contenido (texto de las lecciones, fichas, apunte y mapa de conceptos) es CC BY-SA 4.0 (`LICENSE`) y el código (`tools/`, `unidades/cb104.py` y el código de los notebooks) es MIT (`LICENSE-CODE`); titular Gustavo Varela, 2026.
No están cubiertos los PDFs de la cátedra ni la bibliografía citada: son de sus autores y no se redistribuyen en el repo, salvo los del profesor ya incluidos en `apunte/` (`01_Ejercicios_original.pdf`, `02_afinidad_original.pdf`), que quedan como material de la cátedra.
La licencia está pendiente de confirmación.
