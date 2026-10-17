---
clase: "04"
titulo: Espacios lineales, transformaciones lineales y formas lineales (dualidad)
fecha_2025: null
fecha_2025_estimada: "2025-09-11"   # clase 1 = jueves 2025-08-21, ritmo semanal; Formas_Lineales.wxmx está fechado 10-09-2025
fechas_2026: ["2026-09-30"]  # sólo la parte de formas lineales; espacios vectoriales y TL no tuvieron clase propia en 2C2026
estado: con-transcripcion
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-4
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-6
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-9
  - fuentes/transcripciones/2026-09-30.md
conceptos: [espacio-vectorial, transformacion-lineal, forma-lineal, dualidad, curvas-de-nivel]
apunte: ["11", "05"]
unidad: 06_formas_lineales
---

# Clase 4 — Espacios lineales, transformaciones lineales y formas lineales

> **Estado:** con transcripción del miércoles 2026-09-30 para la parte de formas lineales (secciones "Representation of Points and Lines", "Level Curves of Linear Forms", "Assigned In-Class Exercise"); la parte de espacios vectoriales y transformaciones lineales no se dictó como clase propia en 2C2026 y se reconstruye desde el resumen 2025 y el apunte.

## El hilo del profesor (cursada 2025)
Dos bloques. El primero, repaso con intención: "un espacio vectorial es básicamente un conjunto al
que se asocian dos operaciones (suma y producto por escalar) que cumplen con algunas propiedades
básicas a las que llamamos 'linealidad'", y "las transformaciones lineales eran las transformaciones
de estos espacios que conservaban esas propiedades de la operaciones básicas" *(profesor, resumen
2025)*. De ahí la observación que arma todo lo que sigue: "el producto de matriz con un vector era
efectivamente una transformación lineal, y notamos que parecía estar formado por ecuaciones de
rectas".

El segundo bloque es el que el profesor considera propio: "hablamos de las formas lineales,
funciones que van de un espacio vectorial a un escalar. Vimos que las más básicas de esas funciones
son las funciones selectoras de coordenadas, y después vimos que se comportan igual que las
ecuaciones de las rectas o los planos" *(profesor, resumen 2025)*. Y el salto: "las formas lineales
forman un espacio vectorial, y también que podíamos usar eso para demostrar que cualquier
transformación lineal se compone de formas lineales y por lo tanto puede ser representada por una
matriz". La relación "entre el producto de matrices y el producto interno, y la relación del
producto interno con estas formas lineales".

Lo que después vuelve en cada clase: "una forma lineal se transforma con una transformación lineal
del lado 'contrario' que un vector, y planteamos el ejemplo que puede resumirse en la expresión
𝜙(𝐴(𝑣⃗))=𝐴(𝜙)(𝑣⃗). Este ejemplo es el que luego trabajamos en máxima" *(profesor, resumen 2025)*.
Cierre: "pensando como puede haber formas lineales de distintas dimensiones, y cómo estas se
relacionan con el área y el determinante", que es la puerta a la clase 5.

Sobre por qué lo da acá: "todos los libros que hay que dicen 'Álgebra' empiezan con un capitulo
sobre espacios vectoriales. El tema de las formas lineales en general lo tratan más adelante [...].
A mi me parece siempre bien tratarlo inmediatamente después de la definición del espacio"
*(profesor, resumen 2025)*. Y la deuda: "hay un tema con esto de las formas lineales que es a lo que
normalmente se llama 'dualidad', que es algo que viene de la geometría proyectiva, pero todavía no
lo expliqué".

Dos ecos en clases posteriores. Clase 6: "si una forma lineal de ℝⁿ quedaba definida por el lugar al
que caían n vectores, lo mismo pasará con las transformaciones lineales, y de esa manera es que se
establece la asignación entre transformaciones lineales y matrices (de alguna manera esto está
basado en la dualidad entre formas lineales y vectores)". Clase 9: "Dato clave: el gradiente es una
forma lineal no un vector...".

## Lo que pasó en 2C2026

**Miércoles 2026-09-30, primer bloque.** El profesor entró a las formas lineales desde la geometría
proyectiva, pagando la deuda de 2025. Frases *(transcripción auto-traducida)*:

- "Las rectas se representan por vectores fila y los puntos por vectores columna. Y en realidad lo
  que pasa es que **no existe el vector fila**. Lo que comúnmente llamamos vector fila se llama
  *forma lineal*." Escribe la incidencia como $L^{T}P=0$ y, con la convención fila-columna, $LP=0$.
- "Los puntos se transforman con la transformación a la derecha; las formas lineales con la
  **inversa**, a la izquierda. Así todas las relaciones [de incidencia] se conservan." Esquema de
  cajas en el pizarrón: punto transformado, recta transformada, y el "doblemente transformado" que
  obliga a que una cancele a la otra.
- Rectas de nivel: con la forma $(2,1)$, "$2x+1y=0$ es una recta; si vale 1 es otra un poco más
  lejos. ¿A qué distancia perpendicular? [...] Estas rectas son *curvas de nivel* de un plano que
  sale del pizarrón; esta cosa se llama forma lineal." La forma $(0,1)$ "es básicamente $y$": sus
  curvas de nivel son las horizontales $y=0,1,2,\ldots$
- La escala: "cuanto más largo el vector, más apretadas las curvas. Si el módulo es 1 la separación
  es 1; si mide 2, la separación es $\tfrac12$; si mide 4, $\tfrac14$. Es inversa al módulo." Y el
  porqué, el producto interno: norma por norma por coseno.
- Dos formas dan una **grilla**: "si tengo dos formas lineales tengo una grilla. Un vector está en
  la roja número tanto con la azul número tanto."

**Ejercicio dado en clase** (todos con los mismos números, "no quiero que mis compañeros hagan uno y
yo otro"): formas $(1,1)$ y $(-1,2)$; vector $(3,4)$; transformación
$$T=\begin{pmatrix}1.2&0.5\\-0.1&1.3\end{pmatrix},$$
elegida "no muy distinta de la identidad, para que las cosas no se rompan", con determinante
positivo. Pasos: dibujar las curvas de nivel de las dos formas en una hoja grande, ubicar el vector
en el cruce de la grilla, transformar el vector con $T$ y las dos formas con $T^{-1}$, redibujar y
verificar que el vector transformado cae en el mismo cruce. El profesor hizo $T^{-1}$ "por adjunta
sobre determinante: $1.61$ es el determinante". Resultado leído en clase: "la que era $(1,1)$ ahora
es $(0.86,0.43)$, tiene una orientación más acostada; la $(-1,2)$ quedó un poco más vertical"; el
vector transformado es $(5.6,4.9)$ y cae en "la séptima curva de nivel de una con la quinta de la
otra", igual que el original.

**Segundo bloque** (va a las fichas 06 y 08): autovectores como grilla propia de la transformación,
"en esa base la transformación es diagonal: estira una dirección y comprime la otra, no rompe la
grilla"; cambio de base $T^*=ATA^{-1}$ con los autovectores como columnas de $A$; "convertimos todo
para que nada cambie". Anuncio: SVD como "lo que siempre funciona, aunque no haya autovectores
reales"; Jordan "sirve en álgebra, no tiene interpretación geométrica y acá la interpretación
geométrica es todo".

## Hecho geométrico

**espacio-vectorial.** Álgebra: un conjunto con suma y producto por escalar que respetan linealidad.
Se ve: flechas que se encadenan (paralelogramo) y se estiran; el cero queda quieto. Escalera:
$\mathbb{R}$ es un espacio vectorial donde todo es "multiplicar por un número"; $\mathbb{R}^2$
agrega direcciones; $\mathbb{R}^n$ no agrega nada nuevo salvo que ya no se dibuja. Vocabulario de la
materia: "los vectores son puntos", y en homogéneas los puntos del plano son vectores de
$\mathbb{R}^3$.

**transformacion-lineal.** Álgebra: $T(v+u)=T(v)+T(u)$, $T(\lambda v)=\lambda T(v)$; el cero va al
cero. Se ve: la grilla cuadrada se vuelve una grilla de paralelogramos, pero sigue siendo grilla
(rectas paralelas equiespaciadas). Cada coordenada de salida es una regla que mide la entrada: por
eso "la matriz parecía estar formada por ecuaciones de rectas". La matriz es una pila de formas
(filas) o una hilera de vectores (columnas: adónde van $e_1,e_2$).

**forma-lineal.** Álgebra: $\varphi:\mathbb{R}^n\to\mathbb{R}$ lineal; en coordenadas, una fila
$(a,b)$ y $\varphi(x,y)=ax+by$. Se ve: una regla graduada tirada en el plano: sus marcas son rectas
paralelas equiespaciadas, perpendiculares al vector $(a,b)$, con separación $1/\|(a,b)\|$. En
$\mathbb{R}$: multiplicar por $a$, marcas a distancia $1/a$. En $\mathbb{R}^3$: planos paralelos.
Las selectoras $\mathsf{x},\mathsf{y}$ son las reglas de los ejes; cualquier forma es combinación de
ellas. Incidencia proyectiva: la recta $\ell=(a,b,c)$ *es* una forma, y $\ell\cdot p=0$ dice que $p$
está en su marca cero.

**dualidad.** Álgebra: las formas forman un espacio vectorial del mismo tamaño (el dual); fila por
columna es un número; al transformar el plano con $A$ los vectores van con $A$ (columna, a la
izquierda) y las formas con $A^{-1}$ (fila, a la derecha) para que $\varphi(v)$ no cambie; o bien
"qué regla mide lo mismo sobre el $v$ original": $(\varphi A)(v)=\varphi(Av)$. Se ve: si deformo la
figura, la regla que la mide se deforma *con* ella, y por eso sus coeficientes cambian "al revés".
Sin producto interno, una forma y un vector son objetos distintos; el producto interno es lo que
permite disfrazar la forma $(2,3)$ de vector $(2,3)$ ("no hay base privilegiada salvo por el
producto interno"). En proyectivas, intercambiar puntos y rectas es la dualidad.

**curvas-de-nivel.** Álgebra: $\{v:\varphi(v)=c\}$ para $c=0,\pm1,\pm2,\ldots$ Se ve: la familia de
rectas paralelas de la regla; dos formas dan una grilla y un vector queda ubicado por qué par de
marcas lo cruza (la "séptima con la quinta"). Si la transformación estira el autovector, su grilla
se comprime (forma con $A^{-1}$); una matriz diagonal estira grillas independientemente y no las
rompe. El gradiente de una función en un punto es una forma lineal: su recta de nivel cero es la
tangente a la curva de nivel (ir a lo chico para volver a lo grande).

## Cuentas chicas

**El ejercicio del 30/9, a mano.** $\det T=1.2\cdot1.3-0.5\cdot(-0.1)=1.56+0.05=1.61$. Adjunta
(intercambio la diagonal, cambio el signo de la otra):
$$T^{-1}=\frac{1}{1.61}\begin{pmatrix}1.3&-0.5\\0.1&1.2\end{pmatrix}=\begin{pmatrix}0.8075&-0.3106\\0.0621&0.7453\end{pmatrix}.$$
Vector, con $T$ a la izquierda de la columna:
$T\binom34=\binom{3.6+2.0}{-0.3+5.2}=\binom{5.6}{4.9}$.
Formas, fila por $T^{-1}$ a la derecha:
$$(1,1)\,T^{-1}=\tfrac1{1.61}(1.3+0.1,\ -0.5+1.2)=\tfrac1{1.61}(1.4,\,0.7)=(0.8696,\,0.4348),$$
$$(-1,2)\,T^{-1}=\tfrac1{1.61}(-1.3+0.2,\ 0.5+2.4)=\tfrac1{1.61}(-1.1,\,2.9)=(-0.6832,\,1.8012).$$
Lectura de marcas antes: $(1,1)\cdot(3,4)=7$, $(-1,2)\cdot(3,4)=5$. Después:
$0.8696\cdot5.6+0.4348\cdot4.9=4.870+2.130=7.00$ y
$-0.6832\cdot5.6+1.8012\cdot4.9=-3.826+8.826=5.00$. El vector transformado cae en el cruce de la
séptima con la quinta, como dijo el profesor. La primera forma pasó de $45^\circ$ a
$\arctan(0.4348/0.8696)=26.6^\circ$ ("más acostada") y se acortó de $\sqrt2=1.41$ a $0.97$: sus
marcas se separaron. Control de lo que *no* hay que hacer: si la forma se transformara con $T$ en
vez de $T^{-1}$, $(1,1)T\cdot(3,4)=10.5\neq7$.

**La regla en $\mathbb{R}$ y en $\mathbb{R}^2$ (apunte 11).** $\varphi(x)=2x$: marcas $0,1,2,3$ en
$x=0,\tfrac12,1,\tfrac32$. $\varphi(x,y)=2x+3y$: $\varphi(1,0)=2$, $\varphi(0,1)=3$,
$\varphi(1,1)=5$, $\varphi(3,-2)=0$: la dirección $(3,-2)$ es la que la regla no ve (su núcleo),
$(2,3)$ es perpendicular a las marcas. Pila de formas: $A=\begin{pmatrix}2&3\\1&-1\end{pmatrix}$ lee
dos reglas a la vez; $A\binom12=\binom{8}{-1}$; su núcleo es $\{2x+3y=0\}\cap\{x-y=0\}=\{0\}$ porque
$\det A=-5\neq0$. Con $B=\begin{pmatrix}2&3\\4&6\end{pmatrix}$ las dos reglas son la misma escalada:
núcleo toda la recta $2x+3y=0$, $\det B=0$.

Verificación hecha con `uv run --with numpy python` el 2026-10-17 (`np.linalg.inv(T)` coincide con
la adjunta; las lecturas 7 y 5 se conservan). En Excel: `MINVERSE`, `MMULT` para $T^{-1}$, $Tv$ y
fila por matriz; en GeoGebra, las rectas $x+y=c$ y $-x+2y=c$ para $c=0..8$ y su imagen por $T$.

## Dónde está desarrollado
- Apunte: `11-bloque-algebraico.tex`, sección "Formas lineales: la recta como máquina de medir"
  (`sec:formas-lineales`): primero en $\mathbb{R}$, el ejemplo $2x+3y$, figura de la regla graduada,
  selectoras y espacio dual, matriz como pila de formas y núcleo visto desde las filas, cómo se
  transforma una forma ($\varphi A$ y $\varphi A^{-1}$ con verificación numérica), el gradiente como
  forma lineal, caja "Dualidad en pocas palabras". `05-primera-lectura-homogeneas-proyectivas.tex`,
  tabla "La misma idea en cada dimensión" (fila "Recta": forma lineal $n\cdot x=c$) y sección "Del
  álgebra a la geometría". `13-tercera-lectura.tex` para el gradiente y el plano tangente.
- Unidad marimo: `06_formas_lineales` — **pendiente**. Plan en apunte 21 (tabla de notebooks, fila
  6): "rectas de nivel, pila de formas, transformación del lado contrario". Debería incluir el
  ejercicio del 30/9 con sliders sobre $T$.
- Bibliografía del campus: Juan de Burgos, *Álgebra Lineal y Geometría Cartesiana* ("en castellano
  el libro que trata lo de formas lineales es el de burgos (El capitulo que dice 'espacio dual')";
  "el escaneo es francamente malo"); Axler, *Linear Algebra Done Right* ("el libro del que yo
  primero saqué el tema y concluí que era importante es el de Axler, que está en inglés"); Gerlach,
  *Dual of a Vector Space* (sin comentario); Lay ("los primeros dos capítulos sirven como
  introducción, bastante enfocada a resolver operaciones, pero de muy fácil lectura"); Amoretti,
  *Equipolencia* ("un trabajo muy viejo [...] relativamente fácil de leer"); Grassmann, teoría de la
  extensión (Google Books, "los primeros dos capítulos"). Serie de videos de afinidades desde
  transformaciones lineales: https://www.youtube.com/watch?v=fWRm9dISpNk ("aparece un concepto que
  va a ser clave: sub-espacios").
- Material de clase del profesor: `material de clase 2C2025/Formas_Lineales.wxmx` (wxMaxima,
  10-09-2025), el ejemplo $\phi(A(v))=A(\phi)(v)$.

## Enlaces del mapa
- Viene de: producto-interno (clase 01: la fila por la columna *es* el producto interno),
  coordenadas-homogeneas (clase 03: rectas como ternas), homografia (03p: puntos con $H$, rectas con
  $H^{-T}$).
- Lleva a: producto-cuna y nucleo (clase 05: "formas lineales de distintas dimensiones [...] área y
  determinante"; el núcleo es donde todas las reglas marcan cero), autovector (clase 06: el
  autovector es ortogonal a todas las formas de $A-\lambda I$), cambio-de-base (clase 08:
  $ATA^{-1}$, la grilla de autovectores), gradiente (clase 09: "el gradiente es una forma lineal, no
  un vector"), primera-forma-fundamental (clase 09).
- Qué se conserva: la lectura. Transformando vectores con $T$ y formas con $T^{-1}$, cada vector
  sigue marcando el mismo número en cada regla; en homogéneas, la incidencia punto-recta. Pregunta
  guía del profesor: "¿cómo transformo las rectas para que los puntos sigan estando en las mismas
  rectas?"

## Huecos y dudas
- fecha_2025 inferida (jueves 2025-09-11) a partir de "Clase 21 de Agosto" y del `.wxmx` del
  10-09-2025; no está escrita en el campus.
- Espacios vectoriales y transformaciones lineales como tema propio no se dictaron en 2C2026 (el
  profesor los dio por sabidos del CBC); no hay ejemplos numéricos del 2026 para ese bloque.
- La transcripción del 30/9 está muy degradada en el tramo del dibujo (líneas repetidas); los
  números $0.86$, $0.43$, $5.6$, $4.9$, $1.61$ sí se oyen y coinciden con la cuenta.
- Separación de curvas de nivel $=1/\|\varphi\|$: dicho en clase, no está en el apunte 11 con esa
  fórmula; agregar a la unidad 06.
- El profesor planteó "qué distancia perpendicular hay entre las rectas" como pregunta; en la
  transcripción no queda claro si la respondió con el producto interno o lo dejó para la casa.
- Dualidad "en serio" (intercambio punto↔recta en teoremas proyectivos) sigue sin dictarse; el
  apunte 11 la resume en una caja y el 12 la usa en $\ell'=H^{-T}\ell$.
