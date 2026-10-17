---
clase: "05"
titulo: Subespacios afines y lineales, producto cuña, determinante y núcleo
fecha_2025: null
fecha_2025_estimada: "2025-09-18"   # clase 1 = jueves 2025-08-21, ritmo semanal; no está escrita en el campus
fechas_2026: ["2026-09-16"]
estado: con-transcripcion
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-5
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-4
  - fuentes/transcripciones/2026-09-16.md
conceptos: [subespacio-lineal, subespacio-afin, producto-vectorial, producto-cuna, determinante, nucleo, colinealidad]
apunte: ["11", "05"]
unidad: 07a_cuna_determinante   # y 07b_nucleo_autovectores (núcleo)
---

# Clase 5 — Subespacios, producto cuña, determinante y núcleo

> **Estado:** con transcripción del miércoles 2026-09-16 (secciones "Dot Product and Lines in Homogeneous Coordinates", "Cross Product and Its Algebraic Properties", "The Determinant as the Unique Operation", "Generalization: The Exterior (Wedge) Product", "Null Space of a Matrix"). La parte de subespacios afines/lineales del 2025 no tuvo bloque propio en 2C2026 y se reconstruye del resumen y de los videos que el profesor dejó.

## El hilo del profesor (cursada 2025)
Tres bloques, en sus palabras. Primero los subespacios: "vimos subespacios afines, porque mi postura
es que la noción intuitiva de subesacio es esa, aunque después la noción que necesitamos aprender es
la de subespacio lineal" *(profesor, resumen 2025)*; se apoyó en cuatro videos cortos y en un
"intermedio donde reflexionamos sobre tres formas distintas de escribir la ecuación de una linea o
un plano, y qué significa eso".

Segundo: "el producto cuña, una operación relacionada al determinante que sirve para armar formas
lineales" *(profesor, resumen 2025)*. Dejó dos videos propios ("no me gusta del todo"; "aún más
caótica que la otra").

Tercero, la motivación de todo lo que sigue: "pensar para qué nos va a servir este producto para
idenificar subespacios y qué subespacios nos podría llegar interesar identificar [...]. El ejemplo
era básicamente construir una Transformación lineal que tuviera un vector especial (o varios) en el
núcleo" *(profesor, resumen 2025)*. Ese ejercicio es el punto de partida de la clase 6: "Tomando
como punto de partida el ejercicio final de la clase anterior, donde había una transformación lineal
y se trataba de construir otra que tuviera en el núcleo un vector en específico".

La clase 4 lo había anunciado: "Terminamos la clase pensando como puede haber formas lineales de
distintas dimensiones, y cómo estas se relacionan con el área y el determinante". Y en la clase 7 le
puso nombre: "traemos a la mesa a nuestro 'detector de colinealidad': el producto cuña".

## Lo que pasó en 2C2026

**Miércoles 2026-09-16, primer bloque (antes del intervalo de las 17:20).** El objetivo declarado
*(transcripción auto-traducida)*: "estoy tratando de que la parte geométrica se parezca a la parte
algebraica para que se conecten [...]. Estas propiedades mágicas, como la magia del determinante,
que siempre me vuelan la cabeza: ¿por qué me sirve para esto?".

La construcción, en orden:
1. Producto interno: "sirve para proyecciones, y para ver si dos vectores son ortogonales. En
   coordenadas homogéneas, si pienso que tanto las rectas como los puntos se representan por
   vectores, el producto interno me sirve para preguntar si un punto está en una recta." Dibuja
   puntos y rectas con símbolos distintos: "no es lo mismo $L$, que es un vector pero representa la
   normal, que $P$, que representa un punto".
2. Qué operación une dos puntos: "el punto $P$ está en la recta $PQ$, claramente, eso da cero. [...]
   Para que funcione como tiene que funcionar, la operación entre dos puntos iguales tiene que dar
   cero. Es la parte clave del producto vectorial: ustedes lo aprendieron en álgebra para encontrar
   un plano". Lo llama producto cruz: "en $\mathbb{R}^3$ es el producto vectorial, yo le digo
   producto cruz, perdón".
3. Tres puntos alineados: "¿$R$ está en la recta de $P$ y $Q$? Eso da cero si $P$ y $Q$ generan una
   recta donde está $R$. Y hay una simetría completa: si $R$ está en $PQ$, $P$ está en $QR$ y $Q$
   está en $PR$". Esa operación "tiene relación con el determinante": "ponían los tres vectores en
   una matriz, calculaban el determinante y si daba cero eran linealmente dependientes. Esa
   operación termina siendo el determinante: es un producto cruz y después un producto interno".
4. Apuesta numérica en el pizarrón: $p=(1,2,3)$, $q=(4,5,-1)$, $r=(0,0,1)$ "para que sea fácil, con
   ceros". Sale $p\times q=(-17,13,-3)$ y el desarrollo por la tercera fila da lo mismo: "lo que
   hicimos es exactamente el determinante. No podía ser distinto. No hay otra operación que cumpla
   esas condiciones más que el determinante". Alguien calculó por Sarrus, otro recordó la HP-15 con
   matrices.
5. Las dos propiedades que lo definen: "quiero que sea lineal, poder sacar constantes:
   $(2v)\wedge w=2(v\wedge w)$. Y $v\wedge w=-\,w\wedge v$: ¿se acuerdan que al intercambiar filas
   el determinante cambia de signo? Estas dos propiedades son la misma, porque el único elemento
   igual a su opuesto es el cero." Son "las propiedades del área": "si quieren el área del
   paralelogramo hagan el producto cruz; el volumen del prisma de tres vectores, el determinante.
   ¡Magia pura! Si los tres están en el mismo plano no forman volumen, da cero. Son áreas
   orientadas".
6. Producto exterior: "una operación que viene de un tal Hermann Grassmann [...]. Opero dos vectores
   y obtengo un bivector, un plano orientado; opero con un tercero y obtengo un elemento de
   volumen". Escribe $u=ae_1+be_2+ce_3$, $v=de_1+ee_2+fe_3$, distribuye, tacha $e_i\wedge e_i$,
   reordena con signo y quedan
   $(ae-bd)\,e_1\wedge e_2+(af-cd)\,e_1\wedge e_3+(bf-ce)\,e_2\wedge e_3$: "los mismos números del
   producto cruz, con un signo cambiado en el del medio, porque la regla de la mano derecha de $x$ a
   $z$ da $-y$". Con el tercero $w=ge_1+he_2+ie_3$ ("no se asusten, no es la unidad imaginaria")
   sólo sobreviven los términos que completan $e_1\wedge e_2\wedge e_3$, y de ahí "los más, menos,
   más del desarrollo por menores".
7. Conteo: "en $\mathbb{R}^3$ hay tres tipos de planos elementales pero un solo tipo de volumen, por
   eso el resultado es un número. En $\mathbb{R}^4$: 4 direcciones, 6 planos, 4 volúmenes, 1
   hipervolumen. Es mecánico en cualquier dimensión, y lo necesito porque el producto cruz sólo
   existe en $\mathbb{R}^3$ y quiero autovectores de matrices grandes". Y la idea que deja flotando:
   "de todos los vectores de norma 1, el ortogonal a un subespacio es el que forma mayor volumen con
   él; los otros dan un prisma inclinado".
8. Núcleo (paréntesis antes de autovectores): "¿vieron el espacio nulo de una matriz? Hay vectores
   de entrada que van al cero. Pienso $Av$ fila por fila: cada coordenada es el producto interno de
   una fila con $v$. Si las tres dan cero, $v$ es perpendicular a las tres filas, las tres filas
   están en un plano, no son linealmente independientes, y el determinante da cero. Esa propiedad
   del determinante, la que detecta si el núcleo es vacío o no, es la que se usa para calcular los
   autovalores".

No hubo bloque de subespacios afines ni de "tres maneras de escribir una recta" como en 2025; la
incidencia homogénea ocupó ese lugar.

## Hecho geométrico

**subespacio-afin.** Álgebra: $p+S$ con $S$ subespacio lineal: $\{p+\mu v\}$, $\{p+\mu v+\nu w\}$.
Se ve: una recta o un plano cualquiera, no necesariamente por el origen; es "la noción intuitiva de
subespacio". Tres escrituras de la misma recta: paramétrica ($p+\mu v$), implícita (una forma lineal
igualada a $c$: $n\cdot x=c$), y en homogéneas (una terna $\ell$ con $\ell\cdot(x,y,1)=0$).
Escalera: en $\mathbb{R}$ un subespacio afín es un punto; en $\mathbb{R}^2$ puntos y rectas; en
$\mathbb{R}^3$ además planos.

**subespacio-lineal.** Álgebra: cerrado por suma y escala, contiene al cero. Se ve: rectas y planos
*por el origen*; en homogéneas, un subespacio lineal de $\mathbb{R}^3$ (un rayo) es un punto del
plano y un plano por el origen es una recta. "Es súper importante que la cabeza quede formateada en
términos de espacios y subespacios" (16/9). Los planos elementales $e_1\wedge e_2$, $e_1\wedge e_3$,
$e_2\wedge e_3$ son los subespacios coordenados de dimensión 2.

**producto-vectorial.** Álgebra: $p\times q$ ortogonal a ambos, lineal en cada argumento,
$p\times p=0$; coordenadas $(p_2q_3-p_3q_2,\ p_3q_1-p_1q_3,\ p_1q_2-p_2q_1)$. Se ve: la recta que
une dos puntos ($\ell=p\times q$) y, por la simetría de la incidencia, el punto donde se cortan dos
rectas ($\ell\times m$; dos paralelas dan un punto ideal, su dirección común). Su norma es el área
del paralelogramo. Sólo existe en $\mathbb{R}^3$.

**producto-cuna.** Álgebra: $u\wedge v$, definido sólo por linealidad y antisimetría; el resultado
es un bivector (área orientada), $(u\wedge v)\wedge w=\det[u\,v\,w]\,e_1\wedge e_2\wedge e_3$. Se
ve: el paralelogramo orientado de lados $u,v$; con $w$, el paralelepípedo. Escalera: en $\mathbb{R}$
es $|a|$ con signo; en $\mathbb{R}^2$ el área $ad-bc$; en $\mathbb{R}^3$ el volumen; en
$\mathbb{R}^n$ hipervolumen, y la misma mecánica da "el vector ortogonal a un subespacio", lo que se
necesita para autovectores grandes. "El producto cuña como detector de colinealidad": vale cero
exactamente cuando los vectores se aplastan a algo de menor dimensión.

**determinante.** Álgebra: la única operación de $n$ vectores lineal en cada uno y nula cuando dos
coinciden; $\det[p\,q\,r]=(p\times q)\cdot r$; cambia de signo al intercambiar filas; desarrollo por
menores con signos $+,-,+$. Se ve: volumen orientado de la figura que forman los vectores; cuánto
agranda la transformación un cubo unidad y si invierte la orientación. Escalera: $|a|$, área,
volumen. Cero ⇔ dependientes ⇔ (en homogéneas) tres puntos alineados.

**colinealidad.** Álgebra: $\det[p\,q\,r]=0$ para ternas homogéneas; $(p\times q)\cdot r=0$. Se ve:
$r$ está en la recta que une $p$ y $q$ (y, simétricamente, cada uno en la recta de los otros dos).
Es la condición "sin tres alineados" para que cuatro puntos fijen una homografía (03p) y lo que
detecta el producto cuña en cualquier dimensión.

**nucleo.** Álgebra: $\{v: Av=0\}$; no trivial ⇔ $\det A=0$. Se ve: las direcciones que la
transformación aplasta a un punto; visto desde las filas, el vector donde todas las reglas (formas
lineales) marcan cero: ortogonal a todas las filas, que entonces caben en un plano. Escalera: en
$\mathbb{R}$, $ax=0$ tiene núcleo sólo si $a=0$; en $\mathbb{R}^2$ dos reglas con marcas cero
paralelas; en $\mathbb{R}^3$ tres filas coplanares. Lo que el profesor dejó en 2025 como tarea
("construir una TL con un vector dado en el núcleo") es lo que hace $A-\lambda I$ en la clase 6.

## Cuentas chicas

**La apuesta del 16/9.** $p=(1,2,3)$, $q=(4,5,-1)$, $r=(0,0,1)$.
$$p\times q=\begin{pmatrix}2\cdot(-1)-3\cdot5\\ 3\cdot4-1\cdot(-1)\\ 1\cdot5-2\cdot4\end{pmatrix}=\begin{pmatrix}-17\\13\\-3\end{pmatrix},\qquad (p\times q)\cdot r=-3 .$$
Determinante por la tercera fila: $0\cdot(\ldots)-0\cdot(\ldots)+1\cdot(1\cdot5-2\cdot4)=-3$.
Coinciden. Hecho geométrico: $r$ no está en la recta $pq$ (en homogéneas, $p=(1/3,2/3)$ y
$q=(-4,-5)$ no están alineados con el origen $r$); el volumen del paralelepípedo es 3. Por Sarrus
también da $-3$; desarrollar por la fila con ceros es más corto, y es exactamente "un producto cruz
con las otras dos filas y luego un producto interno".

**Área en $\mathbb{R}^2$ (unidad 07, bloque A).** $u=(3,1)$, $v=(1,2)$:
$u\wedge v=3\cdot2-1\cdot1=5$; $v\wedge u=-5$ (orientación); $u\wedge(2u)=3\cdot2-1\cdot6=0$
(colineales). En $\mathbb{R}$: $a\wedge b$ no existe, sólo queda $|a|$.

**Unir y cortar en homogéneas.** $A=(0,0)$, $B=(0,2)$, $C=(2,3)$ del pentágono entero (03p). Recta
$AC=\vec A\times\vec C=(0,0,1)\times(2,3,1)=(0\cdot1-1\cdot3,\ 1\cdot2-0\cdot1,\ 0)=(-3,2,0)$: la
recta $-3x+2y=0$, o sea $y=\tfrac32x$ ✓. Recta $BD$ con $D=(4,2)$:
$(0,2,1)\times(4,2,1)=(2-2,\ 4-0,\ 0-8)=(0,4,-8)\sim(0,1,-2)$: $y=2$ ✓. Corte
$AC\cap BD=(-3,2,0)\times(0,1,-2)=(-4,-6,-3)\sim(\tfrac43,2,1)$: el punto $F=(\tfrac43,2)$ de la
ficha 03p. Alineación:
$\det[\vec A\,\vec B\,\vec C]=\det\begin{pmatrix}0&0&1\\0&2&1\\2&3&1\end{pmatrix}=1\cdot(0-4)=-4\neq0$:
no alineados.

**Núcleo visto por filas (apunte 11).** $B=\begin{pmatrix}2&3\\4&6\end{pmatrix}$: segunda regla
$=2\times$ primera, $\det B=0$, núcleo $\{2x+3y=0\}$, por ejemplo $(3,-2)$: $B(3,-2)^T=(0,0)^T$. En
$\mathbb{R}^3$: $M=\begin{pmatrix}1&0&1\\0&1&1\\1&1&2\end{pmatrix}$, fila 3 $=$ fila 1 $+$ fila 2,
$\det M=0$; el vector del núcleo es la cruz de dos filas, $(1,0,1)\times(0,1,1)=(-1,-1,1)$, y
$M(-1,-1,1)^T=(0,0,0)^T$ ✓.

Verificación con `uv run --with numpy python` (`np.cross`, `np.linalg.det`), hecha el 2026-10-17:
$p\times q=(-17,13,-3)$, $\det=-3$, $\det B=0$. En Excel: `MDETERM`; en GeoGebra: `Determinante`,
`ProductoVectorial`.

## Dónde está desarrollado
- Apunte: `11-bloque-algebraico.tex` secciones "Producto interno: incidencia", "Producto vectorial:
  unir dos puntos, cortar dos rectas" (las dos propiedades, área orientada, paralelas → punto
  ideal), "Tres puntos alineados: el determinante" (unicidad, verificación $-3$), "Producto
  exterior: la misma idea en cualquier dimensión" (bivectores, conteo $3/3/1$ y $4/6/4/1$,
  "ortogonal es lo que maximiza el volumen"), "Núcleo de una matriz y determinante nulo"; y la
  subsección "La matriz como pila de formas" dentro de formas lineales (núcleo desde las filas).
  `05-primera-lectura-homogeneas-proyectivas.tex`: tabla "La misma idea en cada dimensión" (filas
  Tamaño con signo, Producto) y tabla "Del álgebra a la geometría: qué pregunta cada operación" con
  la cadena incidencia → unión → alineación → determinante → núcleo → autovectores → puntos fijos.
- Unidades marimo (molde v2 sobre `cb104`, 2026-10-17): `unidades/07a_cuna_determinante.py`
  (área orientada y detector de colinealidad, volumen y tres vectores en un plano, los tres mojones en
  homogéneas; escalera $\mathbb{R}\to\mathbb{R}^2\to\mathbb{R}^3$) y `unidades/07b_nucleo_autovectores.py`
  (núcleo: los vectores que van al cero, visto por filas, como puerta a los autovectores de la clase 6).
  El notebook anterior de una pieza quedó en `unidades/_legacy/07_cuna_autovectores_v1.py`.
- Bibliografía del campus: Winitzki, *Linear Algebra via Exterior Products* (sin comentario del
  profesor; es el enfoque de Grassmann que usó en clase); Grassmann, teoría de la extensión (Google
  Books, "lo más importante son los primeros dos capítulos"; clase 4); Strang, *Álgebra lineal y sus
  aplicaciones* (sin comentario); Lay (introducción "enfocada a resolver operaciones"); Fortney, *A
  Visual Introduction to Differential Forms* (sin comentario; dibuja formas y áreas).
- Material de clase del profesor: dos videos propios de producto cuña embebidos en el campus (no
  descargables) y los cuatro videos cortos de subespacios; ningún archivo para esta clase en
  `material de clase 2C2025/`.

## Enlaces del mapa
- Viene de: producto-interno (clase 01: "la operación que teníamos que conservar"; acá, incidencia),
  coordenadas-homogeneas (clase 03), forma-lineal (clase 04: "formas lineales de distintas
  dimensiones [...] área y determinante"), rotacion-3d y matriz-ortogonal (clase 01: "pedir
  determinante 1 [...] el producto vectorial tiene que ver con el determinante y su signo depende de
  la orientación").
- Lleva a: autovector y polinomio-caracteristico (clase 06: $\det(A-\lambda I)=0$ y cruz de filas),
  homografia y recta-fija (03p: "sin tres alineados", puntos fijos), cuatro-subespacios e inversa
  (clase 10: núcleo, imagen, co-imagen), svd (clase 07).
- Qué se conserva: nada se "conserva" acá; la pregunta es qué se *aplasta*. El determinante mide
  cuánto se agranda el volumen y si se invierte la orientación; cero significa que una dirección
  entera cayó a un punto. Pregunta guía: "¿qué subespacios nos podría interesar identificar?"

## Huecos y dudas
- fecha_2025 inferida (jueves 2025-09-18); no figura en el campus.
- En la transcripción la cuenta de la apuesta aparece como "$-17+13-3=-7$": es ruido de la
  traducción automática (el profesor dudaba en voz alta y luego confirmó con Sarrus); el valor
  correcto es $-3$ y así lo registra el apunte 11.
- El apunte 11 rotula el dictado como "clase del 18 de septiembre"; la transcripción es del
  miércoles 16. Ver ficha 03p.
- La idea "el ortogonal es el que maximiza el volumen" quedó enunciada, no desarrollada ("eso lo
  hago la próxima clase"); no aparece desarrollada en las transcripciones posteriores ni en el
  apunte más allá de un párrafo.
- Subespacios afines, lineales y las "tres formas de escribir una recta" de 2025 no tienen versión
  2026 ni material del profesor ("debería armar algo de material sobre eso").
- Los videos de producto cuña del profesor no están en el repo; sólo embebidos en el campus.
