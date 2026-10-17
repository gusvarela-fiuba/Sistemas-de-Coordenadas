---
clase: "03p"
titulo: Transformaciones proyectivas (clase extra 2C2026, el pentágono)
fecha_2025: null            # en 2025 no fue clase propia: se mencionó al cierre de la clase 3 y en la clase 6
fechas_2026: ["2026-09-16", "2026-09-23"]
estado: con-transcripcion   # 09-16 con transcripción; 09-23 reconstruida (nota de Notion vacía)
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-3
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-6
  - fuentes/transcripciones/2026-09-16.md
  - fuentes/transcripciones/2026-09-30.md
  - entregas/pentagono/Pentagono_Proyectivas_Varela_56798.tex
  - entregas/pentagono/Problema_transformaciones_proyectivas.pdf
  - fuentes/campus/profesor/2026-09-16_pizarron_pentagono.jpg
  - fuentes/campus/profesor/Proyectivas_del_pentagono.xlsx
conceptos: [plano-proyectivo, punto-impropio, homografia, recta-fija, razon-doble]
apunte: ["05", "12", "18"]
unidad: 05_proyectivas
---

# Clase 03p — Transformaciones proyectivas: el pentágono

> **Estado:** con transcripción del miércoles 2026-09-16 (consigna del pentágono, último bloque de la clase) / el miércoles 2026-09-23 (discusión de la entrega) está **reconstruido sin transcripción** a partir de la entrega, del apunte y de lo que el profesor recordó el 2026-09-30.

## El hilo del profesor (cursada 2025)
En 2025 las proyectivas no tuvieron clase propia. Aparecen dos veces en los resúmenes, siempre como
la segunda escritura algebraica de lo afín y como el lugar donde los autovectores se vuelven puntos
fijos.

Al cerrar la clase 3: "Terminamos con dos formas de expresión algebraica, una en R2 y otra en el
plano proyectivo, que aproveché para explicar coordenadas homogeneas, que más adelante vamos a
volver a ver. Sobre el espacio proyectivo nos preguntamos especialmente qué pasaba con los puntos
impropios y cómo se expresaría una transformación con puntos fijos" *(profesor, resumen 2025)*. Y
dejó los PDF de Pamfilos, entre ellos *Plano proyectivo*, porque "tienen muy buenos gráficos para
todos estos ejemplos que hicimos en el pizarrón".

En la clase 6 volvió desde el otro lado: "estos espacios invariantes ya habían aparecido cuando
usábamos las coordenadas homogéneas para analizar transformaciones afines o proyectivas. En ese caso
los sub-espacios invariantes de la transformación lineal de ℝ³ correspondían a los puntos fijos en
ℙℝ²" *(profesor, resumen 2025)*.

La dualidad quedó prometida en la clase 4: "hay un tema con esto de las formas lineales que es a lo
que normalmente se llama 'dualidad', que es algo que viene de la geometría proyectiva, pero todavía
no lo expliqué por el orden que le di este cuatrimestre" *(profesor, resumen 2025)*.

En 2C2026 el orden cambió: rotaciones → reflexiones y similaridades → afinidades y homogéneas →
**proyectivas** → productos, determinante y autovectores (apunte 02, caja "Segundo cuatrimestre
2026"). Por eso esta ficha existe como clase aparte.

## Lo que pasó en 2C2026

**Miércoles 2026-09-16.** La clase fue el bloque algebraico (ver fichas 05 y 06) y cerró con la
consigna. El enunciado manuscrito, transcripto en `Problema_transformaciones_proyectivas.pdf`: "Las
transformaciones proyectivas mantienen rectas las rectas y quedan definidas por un cuadrilátero.
Pentágono ABCDE. 1. ¿Cuáles son las posibles transformaciones proyectivas en las que cuatro vértices
caen en otros cuatro? 2. ¿Cómo se calculan? 3. ¿Dónde cae el vértice restante? 4. ¿Tiene punto
fijo?"

La foto del pizarrón de ese día (16:28, `fuentes/campus/profesor/2026-09-16_pizarron_pentagono.jpg`,
mandada por el profesor por Google Chat el 2026-10-17) muestra las mismas cuatro preguntas y dos
dibujos: el pentágono ABCDE con su centro F y un punto G debajo, y una segunda figura con los
vértices reubicados y el C con signo de pregunta.

Cómo lo contó el profesor *(transcripción auto-traducida)*: "mi idea era pensar un pentágono
regular, construir una transformación proyectiva que intercambie los vértices y preguntarnos dónde
cae. Una proyectiva sólo puede venir de cuatro puntos. Entonces cuando intercambio un vértice o lo
que sea, ¿dónde cae el quinto?". Y el ejemplo que lo inquieta: "si dejo A y D quietos y cambio B y D
[sic], ¿dónde diablos cae C? No sé." Clasificó los casos: "hay tres casos posibles: no intercambiar
ningún vértice y sólo correrlo, intercambiar vértices adyacentes, o intercambiar no adyacentes. Y
eso combinado con rotaciones. Mi idea es pensar todas las clases posibles, dónde cae el vértice y si
la transformación tiene punto fijo."

Pista que dio para la cuenta: centrar el pentágono en el origen, porque entonces en el caso más
simple "ese punto fijo ya lo vimos hoy, va a ser (0,0,1)", es decir, el autovector de la rotación es
el centro. Y la conexión con lo que acababa de explicar: "cuando hablábamos de transformaciones
proyectivas, los autovectores eran los puntos fijos de la transformación, porque caen sobre la misma
recta".

Logística: entrega en un único PDF por el campus (o por mail), fotos de avances al grupo; "depende
de cómo avancen con esto les digo si tomamos un ejercicio de proyectivas en la sexta semana".

**Miércoles 2026-09-23 — reconstruida sin transcripción.** La nota de Notion de ese día está vacía.
Lo que se infiere:
- La entrega de Gustavo está fechada 23 de septiembre de 2026 y su enunciado dice "en la clase
  siguiente se precisó: tomar el pentágono *regular*, mirar tres casos (a) correr, (b) intercambiar
  dos adyacentes, (c) intercambiar dos no adyacentes, y sus combinaciones con las rotaciones; el
  punto fijo es un autovector de la matriz". El `LEEME.md` lo llama "aclaración del 18/9", así que
  la precisión pudo haber llegado por el grupo el viernes 18 y no en clase.
- El 2026-09-30 el profesor arrancó recordando la clase anterior *(transcripción auto-traducida)*:
  "¿rotaron esas proyecciones? — Todas no, porque eran 120 casos distintos, pero hicimos algunas.
  Hicimos una planilla en Excel", y "había dicho al principio de la clase pasada que íbamos a cambio
  de base, que bajábamos un poco el ritmo [...] y eso fue lo que no hicimos". Es decir: el 23 se
  discutió el pentágono con planilla y el cambio de base quedó para el 30.
- Esa planilla es `fuentes/campus/profesor/Proyectivas_del_pentagono.xlsx` (mandada por el
  profesor el 2026-10-17): pentágono regular centrado en el origen con $D=(0,1)$ y los demás
  vértices por rotaciones de 72°, como la pista del 16/9; sistema $13\times13$ (los nueve
  coeficientes de la matriz $3\times3$ más un $\lambda$ por punto, con $t=1$) para la proyectiva
  que deja fijos $A$ y $B$ e intercambia $C$ con $E$; se resuelve con la inversa y se verifica
  dónde cae cada vértice en $z=1$. Según leo las fórmulas, la imagen de $D$ queda sobre el eje $x$.
- Los 120 = 5·4·3·2 son las correspondencias ordenadas de cuatro vértices sobre cuatro vértices,
  para un origen fijo; la entrega cuenta 600 contando también qué vértice queda afuera.

Falta confirmar: si la precisión "regular + tres casos" fue el 18 por el grupo o el 23 en clase; qué
en clase se corrieron más casos que el de la planilla ($A$, $B$ fijos, $C\leftrightarrow E$); si el profesor comentó la entrega en clase o sólo en el PDF.

## Hecho geométrico

**plano-proyectivo.** Lo que dice el álgebra: un punto del plano es una terna $(x,y,w)$ a menos de
escala, $(x,y,1)\sim(\lambda x,\lambda y,\lambda)$. Lo que se ve: el plano de dibujo es el plano
$w=1$ dentro de $\mathbb{R}^3$, y cada punto es el *rayo* que sale del origen y lo atraviesa. La
foto de una cámara: todos los puntos de un mismo rayo caen en el mismo lugar de la imagen. Escalera:
en $\mathbb{R}$, la recta proyectiva es la recta más un punto; en $\mathbb{R}^2$, el plano más una
recta de puntos ideales.

**punto-impropio.** Álgebra: terna con $w=0$, $(a,b,0)$. Se ve: la dirección $(a,b)$, el "punto de
fuga" común a todas las paralelas de esa dirección. Una recta afín $p+\mu v$ es $(p,1)+\mu(v,0)$;
cuando $\mu\to\infty$ domina $(v,0)$. Las paralelas se cortan ahí, como los alambrados en la foto
del dron.

**homografia.** Álgebra: $p'\sim Hp$ con $H$ de $3\times3$ invertible; se normaliza dividiendo por
la tercera coordenada $W=h_{31}x+h_{32}y+h_{33}$. Se ve: lo que hace una cámara inclinada con un
lote plano: las rectas siguen rectas, nada más se conserva (ni paralelas, ni razones, ni puntos
medios). Nueve números menos la escala: 8 grados de libertad, 2 por cada par punto-imagen, **cuatro
puntos** la fijan (sin tres alineados). La afinidad es el caso $h_3=(0,0,1)$: $W$ vale siempre 1,
nadie se va al infinito. En una proyectiva general la recta $h_3\cdot p=0$ "se va al infinito"; si
atraviesa la figura, la imagen se parte (un segmento que la cruza se vuelve dos semirrectas unidas
por el infinito).

**recta-fija.** Álgebra: $p$ fijo si $Hp=\lambda p$, autovector real de $H$; una recta $\ell$ es
fija si $H^{-T}\ell\sim\ell$, autovector de $H^{T}$ (cruz de dos *columnas* de $H-\lambda I$). Se
ve: el polinomio característico es de grado 3, así que siempre hay una raíz real: **toda proyectiva
del plano deja algo fijo**, un punto propio o una dirección. Clasificación por autovalores (apunte
12 y unidad 05): tres reales distintos → triángulo invariante; uno real y dos complejos → "rotación
proyectiva", un solo punto fijo; raíz doble con cruz de filas nula → una recta entera de puntos
fijos (el eje) más un centro: *homología*; si además los autovalores son opuestos, $H^2\sim I$ y es
*armónica*, un espejo proyectivo. Es la misma cadena de la clase 6: incidencia → determinante →
núcleo → autovector → punto fijo.

**razon-doble.** Álgebra: para cuatro puntos alineados con coordenada $t$,
$(A,B;C,D)=\frac{(C-A)(D-B)}{(C-B)(D-A)}$; es lo único métrico que una homografía conserva (la razón
simple ya no). Se ve: en una homología armónica, sobre cada recta por el centro $O$ que corta al eje
en $X$, los puntos intercambiados $A,B$ cumplen $(A,B;O,X)=-1$: $O$ es el *conjugado armónico* de
$X$ respecto de $A$ y $B$. Escalera: en $\mathbb{R}$ es la reflexión $u\mapsto-u$ vista en
perspectiva, $t\mapsto\frac{t}{2t-1}$, con polo en $t=\tfrac12$: el punto medio entre centro y eje
se va al infinito. El apunte 12 no desarrolla la razón doble; la entrega la usa para explicar el
$\varphi$ del pentágono regular.

## Cuentas chicas

Pentágono con enteros (de la entrega): $A(0,0)$, $B(0,2)$, $C(2,3)$, $D(4,2)$, $E(4,0)$. Ternas
$(x,y,1)$. Patrón del origen $ABCD$: resolver $(\vec A\ \vec B\ \vec C)\lambda=\vec D$ de abajo
hacia arriba da $\lambda=(1,-2,2)$, o sea $\vec D=\vec A-2\vec B+2\vec C$, y
$$K_1=\begin{pmatrix}0&0&4\\0&-4&6\\1&-2&2\end{pmatrix},\qquad \det K_1=16 .$$

**Ciclo de cuatro, $ABCD\mapsto BCDA$.** $H=K_2K_1^{-1}$, multiplicada por 8 para que quede entera:
$$H=\begin{pmatrix}-2&4&0\\-3&-2&16\\0&-2&8\end{pmatrix},\qquad H\vec C=\begin{pmatrix}8\\4\\2\end{pmatrix}\sim\vec D\ \checkmark,\qquad H\vec E=\begin{pmatrix}-8\\4\\8\end{pmatrix}\Rightarrow E'=(-1,\tfrac12).$$
Punto fijo sin autovectores: $AC\to BD$ y $BD\to CA$, así que $F=AC\cap BD$ va a sí mismo.
$AC:\ y=\tfrac32x$, $BD:\ y=2$ dan $F=(\tfrac43,2)$ y $H(\tfrac43,2,1)^T=(\tfrac{16}3,8,4)^T=4F$ ✓.
Autovalores $4,\ \pm4i$: $H^4\sim I$, un cuarto de giro proyectivo alrededor de $F$. Órbita del
quinto:
$E\mapsto(-1,\tfrac12)\mapsto(\tfrac47,\tfrac{18}7)\mapsto(\tfrac{16}5,\tfrac{16}5)\mapsto E$. Recta
que se va al infinito: $8-2y=0$, $y=4$, arriba de todo: la imagen sale entera.

**No adyacentes, $A\leftrightarrow C$ con $B,D$ quietos.**
$H_c\sim\begin{pmatrix}2&-4&8\\0&-4&12\\0&-1&4\end{pmatrix}$; control
$H_c\vec A=(8,12,4)^T\sim\vec C$ ✓; $E\mapsto(4,3)$, justo arriba de $D$. Autovalores $2$ (doble),
$-2$. Filas de $H_c-2I$: $(0,-4,8),(0,-6,12),(0,-1,2)$, todas múltiplos de $(0,-1,2)$: cruz nula,
rango 1, **recta de puntos fijos** $y=2$, que es $BD$. Centro: cruz de dos filas de $H_c+2I$,
$(4,-4,8)\times(0,-2,12)=(-32,-48,-8)\sim(4,6,1)$: $O_c=(4,6)$ sobre $AC$ prolongada. $H_c^2=4I$:
homología armónica. Razón doble sobre $AC$ (coordenada $x$):
$A=0,\ C=2,\ O_c=4,\ Q=AC\cap BD=\tfrac43$: $\frac{(4-0)(\frac43-2)}{(4-2)(\frac43-0)}=-1$ ✓.

**Adyacentes, $A\leftrightarrow B$.**
$H_b\sim\begin{pmatrix}-8&0&0\\-4&-16&32\\-3&-6&16\end{pmatrix}$, $E\mapsto(-8,4)$; eje $CD$, centro
$(0,\tfrac43)$ sobre $AB$, $H_b^2=64I$. $W$ vale $16,4,-8,-8,4$ en $A..E$: la recta
$x+2y=\tfrac{16}3$ atraviesa el pentágono y la imagen **se parte** (pasa en todo pentágono convexo:
el centro cae dentro del segmento $AB$ y la paralela media entre centro y eje cruza la figura).

**Pentágono regular** (centrado, radio 1): (a) correr $=$ rotación de $72^\circ$, $E\mapsto A$
(cierra), único punto fijo el centro, cruz de filas de $H_a-I$ da $(0,0,1.382)\sim(0,0,1)$; (b)
$A\leftrightarrow B$: autovalores $\pm5.8541$, eje $CD$, imagen partida; (c) $A\leftrightarrow C$:
$\pm0.8541$, eje $BD$, $E\mapsto(0,-1.2361)$, imagen entera. El $\varphi=1.618$ que aparece en
$\lambda=(1,-\varphi,\varphi)$ es el conjugado armónico, no magia del pentágono: en el de enteros
ese número es 2.

Verificación: `uv run --with numpy python entregas/pentagono/verificacion_pentagono.py` (salida en
`verificacion_pentagono_salida.txt`); las cuentas de esta ficha se rehicieron con numpy el
2026-10-17 y coinciden. Interactivo: `unidades/05_proyectivas.py` (Fraction, exacto).

## Dónde está desarrollado
- Apunte: `05-primera-lectura-homogeneas-proyectivas.tex` (puntos como rayos, puntos en el infinito,
  "conservar rectas, nada más", por qué un cuadrilátero, la cadena incidencia→punto fijo);
  `12-bloque-proyectivas.tex` (homografías, $H=K_2K_1^{-1}$ por el cuadrilátero patrón, puntos y
  rectas fijas, clasificación, jerarquía isometría→similaridad→afinidad→proyectiva, el pentágono
  regular con los tres casos y ejercicios de consolidación); `18-apendice-pentagono.tex` (tabla de
  verificación, autovector por cruz en el caso (c), figura de la imagen partida, script).
- Unidad marimo: `unidades/05_proyectivas.py` — existe, migrada. Pentágono
  $A(-2,-1),B(-3,1),C(0,3),D(3,1),E(2,-1)$ con aritmética exacta, elección de correspondencia,
  polinomio característico entero, rectas fijas, trayectoria de la identidad a $H$. Además
  `entregas/pentagono/pentagono_marimo.py` (regular, irregular, controles).
- Bibliografía del campus: Pamfilos, *ProjectivePlane* ("tienen muy buenos gráficos para todos estos
  ejemplos que hicimos en el pizarrón"; Teorema 13, existencia de la proyectiva entre dos
  cuaternas); Richter-Gebert, *Perspectives on Projective Geometry* (Teoremas 3.2–3.4; sin
  comentario del profesor); Coxeter, *Geometría* ("un libro clásico de geometría"); Lay ("tiene el
  ejemplo de coordenadas homogéneas cerca del final del capítulo 2").
- Material del profesor: enunciado manuscrito del 16/9
  (`entregas/pentagono/Problema_transformaciones_proyectivas.pdf`); la planilla Excel del 23/9 no
  está en el repo.

## Enlaces del mapa
- Viene de: coordenadas-homogeneas y transformacion-afin (clase 03, el "$W=1$" como caso
  particular), punto-fijo (clase 03, "cómo se expresaría una transformación con puntos fijos"),
  determinante y colinealidad (clase 05, "sin tres alineados"), autovector (clase 06).
- Lleva a: dualidad y forma-lineal (clase 04: las rectas son formas, $\ell\cdot p=0$; el profesor
  retomó la dualidad el 2026-09-30 desde acá), cambio-de-base (clase 08: "convertimos todo para que
  nada cambie", mismo esquema $ATA^{-1}$), svd (clase 07).
- Qué se conserva: sólo rectas e incidencia (y la razón doble). "Transformaciones proyectivas:
  mantienen rectas las rectas ⇒ quedan definidas por un cuadrilátero" (dictado 16/9). Cada familia
  de la jerarquía conserva menos y necesita un punto más para fijarse: 2, 2, 3, 4.

## Huecos y dudas
- Fecha del dictado: el apunte 12 y 18 dicen "clase del 18 de septiembre", la transcripción es del
  miércoles 16; el 18 fue viernes y el `LEEME.md` habla de "aclaración del 18/9". Probable: consigna
  el 16 en clase, precisión (regular, tres casos) el 18 por el grupo. Confirmar.
- 2026-09-23 sin transcripción: no se sabe qué casos se corrieron en Excel ni si se discutió la
  razón doble o la homología armónica (el apunte 12 dice explícitamente que la razón doble "no se
  desarrolla").
- El profesor dijo en el 16/9 que preveía un ejercicio de proyectivas "en la sexta semana"; no hay
  registro de si se tomó.
- Rotulación del pentágono: la entrega pone $C$ arriba y recorre en sentido horario; el apunte 12
  pone $A$ arriba y recorre antihorario. Mismas transformaciones, otros números en las matrices;
  cuidado al comparar.
- La transcripción tiene el ejemplo "dejo A y D quietos y cambio B y D" con un vértice repetido;
  seguramente dijo "B y E" o "cambio A por C". No se reconstruye.
