# Para el docente

## Qué es

Material para Sistemas de Coordenadas (CB104, Agrimensura, FIUBA). Tiene un apunte en PDF, 20 unidades interactivas que corren en el navegador y un banco de 120 preguntas. Las unidades siguen el programa, de la 0 a la 19. Todas tienen las mismas seis secciones: situación de campo y predicción, hecho geométrico, manipulación, cuenta a mano y código, Python de hoy y ejercicios. No hay que instalar nada ni crear cuentas.

## Un solo encuentro: una unidad en 20 minutos

Un ejemplo con la [Unidad 1, Rotaciones I: el punto no se movió](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/unidades/01a_punto_quieto/index.html), proyectada.

1. **Predicción (6 min).** Sección 0. Un mojón está en P = (4, 3) en los ejes de la obra. Un instrumento en el mismo origen mide en sus propios ejes, girados 30° antihorario. ¿Qué coordenadas lee? La unidad da cuatro opciones. Antes de marcar, cada uno escribe su respuesta en papel, con un croquis a mano alzada de los dos pares de ejes. Después se marca: cada opción incorrecta explica su error.
2. **Hecho geométrico (3 min).** Sección 1. El mojón queda; giran los ejes. Giro pasivo y giro activo, uno inverso del otro.
3. **Manipulación (7 min).** Sección 2. Deslizador `θ (°): giro de los ejes` y botón reproducir. La grilla teal gira y el mojón violeta queda clavado. Se vuelve a los croquis y se comparan.
4. **La cuenta (4 min).** Sección 3. R(30°)ᵀ P, en lápiz y en NumPy, lado a lado.

Los ejercicios y las seis preguntas del final quedan para después del aula.

## Qué piezas son independientes

Cada pieza se usa sola, sin las otras.

- **El banco para Moodle** ([XML, 120 preguntas](moodle/moodle_banco_120_preguntas_cb104.xml)): seis por unidad, en tres niveles, para importar en el aula virtual.
- **[Qué hay para cada capítulo](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/menu.html)**: las piezas de cada capítulo, con duración y estado; también en PDF.
- **[Entradas, platos y postres por capítulo](https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/menu-por-capitulo.html)**: un menú por capítulo en A4 apaisado, para imprimir.
- **Los problemas por capítulo del PDF**: cada capítulo, del 1 al 15, cierra con una sección «Problemas» graduada por dificultad. Las respuestas están en un apéndice.
- **[El apunte entero](apunte/Apunte_Sistemas_de_Coordenadas.pdf)**.
- **Las unidades**: cada una se abre desde su propio enlace, sin pasar por la portada.

## Qué es optativo

El Python. El código de la sección 3, la sección 4 y los ejercicios de código de cada unidad se pueden saltear. La predicción, la manipulación y la cuenta en lápiz no dependen de ellos.

Las secciones «En profundidad» del apunte. Reúnen las demostraciones largas y las conexiones con el resto del programa. El capítulo se entiende sin ellas.

## Cómo se actualiza o se adopta

Todo sale del repositorio. Se edita la fuente y se vuelve a generar el sitio con `uv run python tools/build.py`. Para publicarlo bajo otra cuenta, con otra firma, están los pasos en la [Parte 4 del instructivo: cómo adoptar y publicar este curso bajo otra cuenta](INSTRUCTIVO_DE_USO.md#parte-4--cómo-adoptar-y-publicar-este-curso-bajo-otra-cuenta).
