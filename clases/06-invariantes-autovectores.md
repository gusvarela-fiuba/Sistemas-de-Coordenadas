---
clase: "06"
titulo: Subespacios invariantes, autovalores y autovectores
fecha_2025: null
fecha_2025_estimada: "2025-09-25"   # clase 1 = jueves 2025-08-21, ritmo semanal; no está escrita en el campus
fechas_2026: ["2026-09-16"]
estado: con-transcripcion
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-6
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-7
  - fuentes/transcripciones/2026-09-16.md
  - fuentes/transcripciones/2026-09-30.md
conceptos: [subespacio-invariante, autovector, autovalor, polinomio-caracteristico]
apunte: ["autovectores", "18", "proyectivas"]
unidad: 07b_nucleo_autovectores   # y 07c_autovalores_3d_puntos_fijos (3D, puntos fijos)
---

# Clase 6 — Subespacios invariantes, autovalores y autovectores

> **Estado:** con transcripción del miércoles 2026-09-16 (secciones "Eigenvalues and Eigenvectors", "Worked Example: Reflection Matrix", "Worked Example: Rotation Matrix", segundo bloque después del intervalo de las 17:20). La parte "una TL tiene una única matriz" y "el cero va al cero" del 2025 no se dictó aparte en 2C2026.

## El hilo del profesor (cursada 2025)
El profesor avisa que "los segmentos de esta clase no los tengo ordenados" *(profesor, resumen
2025)*. Tres hilos:

1. Matrices y transformaciones. Desde la linealidad $T(\lambda v)=\lambda T(v)$, $T(v+u)=T(v)+T(u)$:
   "si una forma lineal de ℝⁿ quedaba definida por el lugar al que caían n vectores, lo mismo pasará
   con las transformaciones lineales, y de esa manera es que se establece la asignación entre
   transformaciones lineales y matrices" *(profesor, resumen 2025)*. "La composición de
   transformaciones lineales y el producto de matrices funcionan de la misma manera."
2. El cero y los subespacios que caen sobre sí mismos. "Una buena parte de la clase trató sobre la
   conclusión de que el cero tiene que ir al cero [...]. De forma que tenemos ahí un conjunto
   bastante trivial {0⃗}, que es un sub-espacio. ¿cómo funcionan otros sub-espacios ante una
   transformación?" Y: "algo interesante para mirar es si existen subespacios que caigan sobre ellos
   mismos en el caso de que estemos trabajando con un operador lineal ℝⁿ→ℝⁿ". El puente con lo
   anterior: "estos espacios invariantes ya habían aparecido cuando usábamos las coordenadas
   homogéneas [...] los sub-espacios invariantes de la transformación lineal de ℝ³ correspondían a
   los puntos fijos en ℙℝ²" *(profesor, resumen 2025)*.
3. El método. Textual: "𝐴(𝑣⃗)=𝜆𝑣⃗ → 𝐴(𝑣⃗)−(𝜆𝐼𝑑)⋅𝑣⃗=0 → (𝐴−𝜆𝐼𝑑)⋅𝑣⃗=0. Lo que significa que hay un
   vector que está en el núcleo de 𝐴−𝜆𝐼𝑑. [...] buscamos los valores de 𝜆 que hagan que el núcleo de
   la transformación no esté vacío. Esto lo podemos ver en el valor del determinante [...]. Una vez
   que tenemos valores candidatos de 𝜆, podemos usar el producto cuña para construir vectores
   ortogonales a los vectores que aparecen como fila en la TL 𝐴−𝜆𝐼𝑑" *(profesor, resumen 2025)*.
   Casos difíciles anotados: "¿que pasa si dos auto-vectores tienen asociado el mismo auto-valor?
   ¿que pasa si la transformación ya tenía algo en el núcleo?"

La frase que la materia repite: "algo notablemente anti-intuitivo es que no existe una base
vectorial privilegiada de ℝⁿ, y lo único que define a la base que llamamos canónica es que sobre
ella tenemos definida la noción de distancia a través del producto interno" *(profesor, resumen
2025)*. Y los comentarios sobre Grassmann y Möbius: "la idea de ponerle coordenadas con números a
las transformaciones lineales es independiente del concepto de linealidad".

La clase 7 retoma: "Nos aprovechamos de la propiedad 𝐴𝑣⃗=𝜆𝑣⃗ del subespacio invariante para crear
una versión modificada de la transformación que tenga a un autovector en el subespacio nulo. Luego,
traemos a la mesa a nuestro 'detector de colinealidad': el producto cuña, y lo usamos primero para
constuir un polinomio cuyas raíces son los autovalores, y luego para hallar los autovectores"
*(profesor, resumen 2025)*.

## Lo que pasó en 2C2026

**Miércoles 2026-09-16, segundo bloque.** Arranque *(transcripción auto-traducida)*: "tenemos una
herramienta que da cero cuando unos vectores son linealmente dependientes, y eso tenía que ver con
detectar si una matriz tiene núcleo no vacío. Con eso vamos a construir nuestra máquina de encontrar
autovectores y autovalores. Un autovector es un vector que, transformado, cae sobre sí mismo o sobre
un múltiplo. Por eso cuando hablábamos de proyectivas los autovectores eran los puntos fijos."
Aviso: "los autovectores son una herramienta para encontrar otra cosa todavía" (la SVD), y "van a
oírme confundir autovalores con autovectores todo el tiempo".

**El pase de magia.** "$Av=\lambda v$. Lo que se hace es un pase de magia: esto es lo mismo que
$(A-\lambda I)v=0$, porque son operaciones lineales. Esta matriz tiene un vector no nulo que cae al
cero: un vector ortogonal a todas sus filas. Entonces sus filas no ocupan todo el espacio, forman un
plano y no un volumen, y el determinante de esta porquería es cero." Escribe la genérica
$\begin{pmatrix}a-\lambda&b&c\\d&e-\lambda&f\\g&h&i-\lambda\end{pmatrix}$: "el determinante es un
choclo, pero es un polinomio de grado 3 en $\lambda$: $\lambda^3+B\lambda^2+C\lambda+D=0$. Se llama
polinomio característico."

**Cuántas raíces.** "Tres raíces: todas reales, o una real y dos complejas conjugadas. No pueden ser
todas complejas: en un polinomio real las complejas vienen de a pares. A cada autovalor real le
corresponde un autovector real; a un complejo no le corresponde nada, porque un vector complejo de
$\mathbb{R}^3$ no significa nada." Ejemplo clave: "una matriz que tiene un solo autovalor real es la
de rotación: el único vector que queda sobre su recta es el del eje, y además no se estira, así que
ese autovalor es 1. Los otros dos son complejos."

**Cómo se encuentra el autovector.** "Las filas de $A-\lambda I$ son todas perpendiculares a mi
autovector. Tomo dos y hago el producto cruz. Si da cero porque esas dos filas son paralelas, tomo
otro par. Si todos los pares dan cero, $\lambda$ era raíz doble."

**Ejemplo 1, reflexión respecto del plano $xy$.** $A=\mathrm{diag}(1,1,-1)$: "conserva $x$ e $y$, da
vuelta $z$". $\det(A-\lambda I)=(1-\lambda)^2(-1-\lambda)$; lo desarrolló completo ("había que
hacerlo entero, muchachos") hasta $-\lambda^3+\lambda^2+\lambda-1$, con un alumno sugiriendo la
diferencia de cuadrados; raíces $1$ (doble) y $-1$. Para $\lambda=-1$: $A+I=\mathrm{diag}(2,2,0)$,
"$(2,0,0)\times(0,2,0)=(0,0,4)$: ese vector y cualquiera en esa dirección es autovector con
autovalor $-1$; $A(0,0,4)=(0,0,-4)$, obvio". La raíz doble: "hay todo un subespacio de autovectores
con el mismo autovalor: cualquier vector del plano $xy$ cae sobre sí mismo". Y la advertencia: "si
en vez de $1,1,-1$ pongo $1,2,-1$, cada eje tiene su autovalor y no hay un plano entero; el caso del
plano es el menos normal. Los ejercicios de álgebra están diseñados para dar números lindos y no
representan una matriz cualquiera".

**Ejemplo 2, eje de una rotación compuesta.** Arma $R=R_z(\theta)R_y(\theta)$ con las dos básicas:
"sé que es rotación porque la construí componiendo rotaciones, así que ni necesito el polinomio:
tiene un único autovalor real que es 1 y su autovector es el eje. Las raíces complejas no me
importan: me darían vectores complejos". Resta la identidad, hace el producto cruz de dos filas de
$R-I$ y verifica con `MMULT` que "si lo aplico a la matriz no tiene que cambiar". Lo hizo en
planilla, porque "en el pizarrón empiezan a multiplicar 0.87 por 0.63 por 0.91 y todo explota"; hubo
"un boicot: la gente quería 'No al Excel'" (Octave, Python). El apunte 11 fija el caso
$90^\circ$–$90^\circ$ para hacerlo a mano.

**Miércoles 2026-09-30** (segundo bloque, ficha 08): "cuando una matriz tiene autovectores reales,
si armo una base con ellos y cambio de base, la matriz queda diagonal"; los autovectores "son los
vectores especiales que no cambian de dirección, sólo se escalan"; grilla de autovectores,
$T=A\,D\,A^{-1}$ con los autovectores como columnas de $A$.

## Hecho geométrico

**subespacio-invariante.** Álgebra: $S$ con $A(S)\subseteq S$. Se ve: una recta por el origen que,
al transformar, cae sobre sí misma (quizá estirada o invertida); un plano que cae sobre sí mismo. El
$\{0\}$ siempre es invariante ("el cero va al cero"). En homogéneas, una recta invariante de
$\mathbb{R}^3$ es un punto fijo del plano, un plano invariante es una recta fija. Escalera: en
$\mathbb{R}$ todo es invariante (sólo hay una dirección); en $\mathbb{R}^2$ hay 0, 1, 2 direcciones
invariantes o todas (homotecia); en $\mathbb{R}^3$ siempre hay al menos una.

**autovector.** Álgebra: $v\neq0$ con $Av=\lambda v$; está en el núcleo de $A-\lambda I$; se calcula
como cruz (cuña) de dos filas de $A-\lambda I$. Se ve: la dirección que no gira, sólo se escala; el
eje de una rotación; los puntos fijos de una proyectiva. "Una versión modificada de la
transformación que tenga al autovector en el núcleo": restar $\lambda I$ es correr cada regla de la
matriz hasta que las tres marquen cero sobre $v$. Si todos los pares de filas dan cruz nula, hay un
plano entero (en homogéneas, una recta entera de puntos fijos: el eje de una homología).

**autovalor.** Álgebra: raíz real de $\det(A-\lambda I)=0$. Se ve: cuánto se estira la dirección
fija: $1$ queda quieta (eje de rotación, puntos fijos "de verdad"), $-1$ se invierte (reflexión),
$|\lambda|>1$ estira, $0$ aplasta (la matriz tiene núcleo). Escalera: en $\mathbb{R}$,
$a\cdot x=\lambda x$ es trivial, $\lambda=a$ y todo $x$ sirve; en $\mathbb{R}^2$ sólo algunas
direcciones, o ninguna real si hay giro; en $\mathbb{R}^3$ al menos una real. Los autovalores
complejos no dan vectores de $\mathbb{R}^3$: dicen que en un plano hay un giro (los
$e^{\pm i72^\circ}$ de la rotación del pentágono; los $\pm4i$ del ciclo de cuatro, $H^4\sim I$).

**polinomio-caracteristico.** Álgebra: $\det(A-\lambda I)$, grado $n$; sus raíces son los
autovalores; en $3\times3$, grado impar ⇒ una raíz real. Se ve: es el "detector de colinealidad"
aplicado a las filas de $A-\lambda I$: para qué valores de $\lambda$ las tres reglas corridas se
vuelven coplanares. Una raíz doble con cruz nula es un plano de autovectores; las complejas vienen
de a pares conjugados. Una matriz genérica da raíces irracionales y feas: por eso el método tiene
que funcionar en planilla o en código, no sólo a mano.

## Cuentas chicas

**Reflexión $A=\mathrm{diag}(1,1,-1)$.**
$$\det(A-\lambda I)=(1-\lambda)(1-\lambda)(-1-\lambda)=-(1-\lambda)^2(1+\lambda)=0\ \Rightarrow\ \lambda=1\ (\text{doble}),\ \lambda=-1 .$$
Para $\lambda=-1$: $A+I=\mathrm{diag}(2,2,0)$, filas $(2,0,0)$ y $(0,2,0)$:
$$(2,0,0)\times(0,2,0)=(0\cdot0-0\cdot2,\ 0\cdot0-2\cdot0,\ 2\cdot2-0\cdot0)=(0,0,4)\sim(0,0,1):$$
el eje $z$, y $A(0,0,1)^T=(0,0,-1)^T$ ✓ (se invierte). Para $\lambda=1$:
$A-I=\mathrm{diag}(0,0,-2)$; cruz de cualquier par de filas: $(0,0,0)\times(0,0,0)=0$,
$(0,0,0)\times(0,0,-2)=0$. Raíz doble: todo el plano $xy$ es de autovectores, porque la reflexión lo
deja quieto punto a punto. En homogéneas ($w=z$): una recta entera de puntos fijos más el punto
ideal vertical invertido; es una homología armónica como las del pentágono.

**Eje de $R=R_z(90^\circ)\,R_y(90^\circ)$.** Con $\cos90^\circ=0$, $\sin90^\circ=1$:
$$R=\begin{pmatrix}0&-1&0\\1&0&0\\0&0&1\end{pmatrix}\begin{pmatrix}0&0&1\\0&1&0\\-1&0&0\end{pmatrix}=\begin{pmatrix}0&-1&0\\0&0&1\\-1&0&0\end{pmatrix}.$$
Control de que es rotación: columnas ortonormales, $\det R=0\cdot(0-0)-(-1)\cdot(0+1)+0=1$. Sin
polinomio: $\lambda=1$. Filas de $R-I$: $(-1,-1,0)$, $(0,-1,1)$, $(-1,0,-1)$.
$$(-1,-1,0)\times(0,-1,1)=\big((-1)\cdot1-0\cdot(-1),\ 0\cdot0-(-1)\cdot1,\ (-1)(-1)-(-1)\cdot0\big)=(-1,\,1,\,1).$$
Verificación: $R(-1,1,1)^T=(0+(-1)\cdot1+0,\ 0+0+1,\ 1+0+0)^T=(-1,1,1)^T$ ✓. Control con otro par:
fila 2 $\times$ fila 3 $=(1,-1,-1)$, la misma recta. El eje es la diagonal $(-1,1,1)$: la
composición de dos cuartos de vuelta es un tercio de vuelta alrededor de ella (los otros autovalores
son $-\tfrac12\pm\tfrac{\sqrt3}2i=e^{\pm i120^\circ}$, y $R^3=I$). Se ve en la planilla: $R$ manda
$e_1\mapsto -e_3\mapsto -e_2\mapsto e_1$: los ejes se permutan con signos y en tres pasos vuelve.

**Con la cuña en $\mathbb{R}^2$ (unidad 07, bloque E).** $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$:
$\det(A-\lambda I)=(2-\lambda)^2-1=0$, $\lambda=1,3$. Para $\lambda=3$, fila de $A-3I$: $(-1,1)$; el
autovector es la perpendicular a esa regla, $(1,1)$, y $A(1,1)^T=(3,3)^T$ ✓. Para $\lambda=1$: fila
$(1,1)$, autovector $(1,-1)$, $A(1,-1)^T=(1,-1)^T$ ✓. En $\mathbb{R}^2$ "cruz de dos filas" se
reduce a "perpendicular a una fila".

**Puente a 03p.** Caso (c) del pentágono entero:
$H_c=\begin{pmatrix}2&-4&8\\0&-4&12\\0&-1&4\end{pmatrix}$,
$\det(H_c-\lambda I)=(2-\lambda)\big[(-4-\lambda)(4-\lambda)+12\big]=(2-\lambda)(\lambda^2-4)$:
raíces $2,2,-2$. Las filas de $H_c-2I$ son múltiplos de $(0,-1,2)$: cruz nula, recta de puntos fijos
$y=2$. Filas de $H_c+2I$: $(4,-4,8)\times(0,-2,12)=(-32,-48,-8)\sim(4,6,1)$, el centro $(4,6)$,
$H_c(4,6,1)^T=(-8,-12,-2)^T=-2\,(4,6,1)^T$ ✓.

Verificación con `uv run --with numpy python` el 2026-10-17: `np.linalg.eigvals`, `np.cross` de
filas, `R @ eje == eje`, $R^TR=I$, $\det R=1$. En Excel, como en clase: `MMULT` para armar $R$,
restar la identidad, producto cruz a mano con tres `=`, y `MMULT(R; eje)`.

## Dónde está desarrollado
- Apunte: `08-algebra-transformaciones.tex` sección "Autovalores y autovectores" (el pase de magia, cuántos
  autovalores reales, método del producto cruz, Ejemplo 1 reflexión, Ejemplo 2
  $R_z(90^\circ)R_y(90^\circ)$ con eje $(-1,1,1)$ y el caso genérico $R_z(30^\circ)R_y(50^\circ)$
  con eje $(-0.2263,0.8446,0.4853)$, caja "Sobre los números lindos"). `07-proyectivas.tex`
  "Puntos fijos y rectas fijas de una homografía" (autovectores de $H$ y de $H^T$, clasificación por
  autovalores, homología). `18-apendice-pentagono.tex` (autovector por cruz en el caso (c) del
  regular, raíz doble → recta fija). `06-afines-homogeneas.tex`: fila
  "Autovector" de la tabla por dimensiones y caja "En palabras del profesor" (clase 6).
- Unidades marimo (molde v2 sobre `cb104`, 2026-10-17): `unidades/07b_nucleo_autovectores.py`
  (autovectores: las direcciones que no giran; $A-\lambda I$ y el detector con la elipse que se
  aplasta; "en 2D la perpendicular a una fila"; método del profesor en `lib.autovectores_cuna`) y
  `unidades/07c_autovalores_3d_puntos_fijos.py` (complementaria: reflexión y eje de $R_zR_y$ por cruz
  de dos filas, rectas invariantes que pinchan $z=1$, $H_c$ del pentágono como homología). El notebook
  anterior de una pieza, con su rúbrica, quedó en `unidades/_legacy/07_cuna_autovectores_v1.py`.
- Bibliografía del campus: Butler, *Facts About Eigenvalues* (sin comentario); Axler, *Linear
  Algebra Done Right* (todo operador en dimensión impar tiene autovalor; citado en la entrega del
  pentágono); Allardice, *The barycentric calculus of Möbius* y Möbius, *On the composition of line
  segments* ("plantean las mismas ideas de linealidad pero no a partir de poner coordenadas sino a
  partir de hacer operaciones geométricas con segmentos"); Molina–Oktaç y González–Roa sobre
  enseñanza de transformaciones lineales ("no me parecen excepcionales pero [...] hablan de
  distintas formas de generar intuición", clase 7); Strang y Lay para el cálculo estándar.
- Material de clase del profesor: `material de clase 2C2025/Algun_ejemplo_de_rotacion.wxmx` (Maxima
  2025.2.2, 25-08-2025): "aparece una yapa relativa a autovectores"; la planilla Excel del 16/9 con
  $R_z R_y$ no está en el repo. Videos de la clase 7 sobre SVD embebidos en el campus.

## Enlaces del mapa
- Viene de: nucleo, determinante y producto-cuna (clase 05: $\det(A-\lambda I)=0$ y cruz de filas),
  forma-lineal (clase 04: las filas de $A-\lambda I$ son reglas que marcan cero sobre $v$),
  punto-fijo y coordenadas-homogeneas (clase 03), rotacion-3d (clase 01: el eje), homografia (03p:
  "el punto fijo es un autovector").
- Lleva a: recta-fija (03p: clasificación por autovalores, homología), diagonalizacion y
  cambio-de-base (clase 08: base de autovectores, $A\,D\,A^{-1}$, potencias y trayectorias), svd y
  base-privilegiada (clase 07: "siempre existe una base ortogonal que se conserva ortogonal", sin
  complejos), inversa (clase 10: $A^{-1}=C^{-1}(1/\Lambda)C$), hessiana y forma-cuadratica (clase 09
  y 12).
- Qué se conserva: la dirección. Un autovector es la trayectoria más simple que genera la
  transformación: una recta que cae sobre sí misma ("las transformaciones se identifican con las
  trayectorias que generan"). Pregunta guía: "¿existen subespacios que caigan sobre ellos mismos?"

## Huecos y dudas
- fecha_2025 inferida (jueves 2025-09-25).
- En 2026 el ejemplo de rotación se hizo con ángulos genéricos en planilla; los ángulos exactos no
  se oyen en la transcripción. El apunte 11 fija $90^\circ$–$90^\circ$ (a mano) y
  $30^\circ$–$50^\circ$ (NumPy) como reconstrucción; no es seguro que fueran los de la clase.
- "¿Qué pasa si la transformación ya tenía algo en el núcleo?" ($\lambda=0$) quedó enunciado en 2025
  y no se trató en 2026.
- La afirmación "no hay base privilegiada salvo por el producto interno" está en los resúmenes 2025
  (clases 6 y 8); en 2026 apareció el 30/9 como "la base canónica acá no tiene sentido", sin la
  frase completa. Confirmar si se dijo.
- El apunte 11 dice "clase del 18 de septiembre" para este dictado; la transcripción es del 16. Ver
  ficha 03p.
- La transcripción tiene un tramo largo ilegible en el desarrollo del polinomio de la reflexión
  (repeticiones de "$-\lambda$, 1"); se reconstruyó desde el apunte.
