---
clase: "3p"
titulo: "Complemento C1: transformaciones proyectivas"
idea: "Una homografía es lo que hace una cámara inclinada con un terreno plano: conserva rectas y nada más, y cuatro puntos la determinan."
que_se_estudia: ["Plano proyectivo: puntos como rayos por el origen", "Puntos impropios: el punto de fuga común a las paralelas", "Homografía $p'\\sim Hp$, ocho grados de libertad y cuadrilátero patrón", "Puntos y rectas fijos, clasificación por autovalores, homologías", "Razón doble: lo único métrico que se conserva"]
conceptos_previos: ["Coordenadas homogéneas y afinidades (capítulo 4)", "Determinante y colinealidad (capítulo 6)", "Autovectores (capítulo 7)"]
apunte: ["proyectivas", "18"]
unidades: ["05_proyectivas"]
animaciones: ["02_homogeneas_pentagono_3d"]
ejercicios_sugeridos: ["Hallar la homografía que lleva $ABCD\\mapsto BCDA$ en el pentágono de enteros y su punto fijo", "Clasificar por autovalores las homografías $A\\leftrightarrow C$ y $A\\leftrightarrow B$", "Verificar que la razón doble sobre la recta $AC$ da $-1$ en la homología armónica"]
---

# Complemento C1: transformaciones proyectivas

Una homografía es lo que hace una cámara inclinada con un terreno plano: conserva rectas y nada más, y cuatro puntos la determinan.

## Qué se estudia

- Plano proyectivo: puntos como rayos por el origen
- Puntos impropios: el punto de fuga común a las paralelas
- Homografía $p'\sim Hp$, ocho grados de libertad y cuadrilátero patrón
- Puntos y rectas fijos, clasificación por autovalores, homologías
- Razón doble: lo único métrico que se conserva

### Plano proyectivo

Lo que dice el álgebra: un punto del plano es una terna $(x,y,w)$ a menos de
escala, $(x,y,1)\sim(\lambda x,\lambda y,\lambda)$. Lo que se ve: el plano de dibujo es el plano
$w=1$ dentro de $\mathbb{R}^3$, y cada punto es el *rayo* que sale del origen y lo atraviesa. La
foto de una cámara: todos los puntos de un mismo rayo caen en el mismo lugar de la imagen. Escalera:
en $\mathbb{R}$, la recta proyectiva es la recta más un punto; en $\mathbb{R}^2$, el plano más una
recta de puntos ideales.

### Punto impropio (punto en el infinito)

Álgebra: terna con $w=0$, $(a,b,0)$. Se ve: la dirección $(a,b)$, el "punto de
fuga" común a todas las paralelas de esa dirección. Una recta afín $p+\mu v$ es $(p,1)+\mu(v,0)$;
cuando $\mu\to\infty$ domina $(v,0)$. Las paralelas se cortan ahí, como los alambrados en la foto
del dron.

### Homografía (transformación proyectiva)

Álgebra: $p'\sim Hp$ con $H$ de $3\times3$ invertible; se normaliza dividiendo por
la tercera coordenada $W=h_{31}x+h_{32}y+h_{33}$. Se ve: lo que hace una cámara inclinada con un
lote plano: las rectas siguen rectas, nada más se conserva (ni paralelas, ni razones, ni puntos
medios). Nueve números menos la escala: 8 grados de libertad, 2 por cada par punto-imagen, **cuatro
puntos** la fijan (sin tres alineados). La afinidad es el caso $h_3=(0,0,1)$: $W$ vale siempre 1,
nadie se va al infinito. En una proyectiva general la recta $h_3\cdot p=0$ "se va al infinito"; si
atraviesa la figura, la imagen se parte (un segmento que la cruza se vuelve dos semirrectas unidas
por el infinito).

### Puntos y rectas fijas de una homografía

Álgebra: $p$ fijo si $Hp=\lambda p$, autovector real de $H$; una recta $\ell$ es
fija si $H^{-T}\ell\sim\ell$, autovector de $H^{T}$ (cruz de dos *columnas* de $H-\lambda I$). Se
ve: el polinomio característico es de grado 3, así que siempre hay una raíz real: **toda proyectiva
del plano deja algo fijo**, un punto propio o una dirección. Clasificación por autovalores: tres reales distintos → triángulo invariante; uno real y dos complejos → "rotación
proyectiva", un solo punto fijo; raíz doble con cruz de filas nula → una recta entera de puntos
fijos (el eje) más un centro: *homología*; si además los autovalores son opuestos, $H^2\sim I$ y es
*armónica*, un espejo proyectivo. Es la misma cadena del capítulo 7: incidencia → determinante →
núcleo → autovector → punto fijo.

### Razón doble

Álgebra: para cuatro puntos alineados con coordenada $t$,
$(A,B;C,D)=\frac{(C-A)(D-B)}{(C-B)(D-A)}$; es lo único métrico que una homografía conserva (la razón
simple ya no). Se ve: en una homología armónica, sobre cada recta por el centro $O$ que corta al eje
en $X$, los puntos intercambiados $A,B$ cumplen $(A,B;O,X)=-1$: $O$ es el *conjugado armónico* de
$X$ respecto de $A$ y $B$. Escalera: en $\mathbb{R}$ es la reflexión $u\mapsto-u$ vista en
perspectiva, $t\mapsto\frac{t}{2t-1}$, con polo en $t=\tfrac12$: el punto medio entre centro y eje
se va al infinito. La razón doble explica el
$\varphi$ del pentágono regular.

## Conceptos previos

- Coordenadas homogéneas y afinidades (capítulo 4)
- Determinante y colinealidad (capítulo 6)
- Autovectores (capítulo 7)

## En el apunte

- Complemento C1. Transformaciones proyectivas
- Sección C1.3.2. El pentágono

## Unidades interactivas

- Proyectivas: la foto del dron y el pentágono (`05_proyectivas`)

## Animaciones

- `02_homogeneas_pentagono_3d`

## Ejercicios sugeridos

- Hallar la homografía que lleva $ABCD\mapsto BCDA$ en el pentágono de enteros y su punto fijo
- Clasificar por autovalores las homografías $A\leftrightarrow C$ y $A\leftrightarrow B$
- Verificar que la razón doble sobre la recta $AC$ da $-1$ en la homología armónica
