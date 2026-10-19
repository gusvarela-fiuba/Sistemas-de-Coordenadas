---
clase: 5
titulo: "Capítulo 6: subespacios, producto cuña y determinante"
idea: "Unir, cortar y detectar colinealidad son una misma operación: el producto cuña, cuyo caso de tamaño $n$ es el determinante."
que_se_estudia: ["Subespacios lineales y afines, y las tres escrituras de una recta", "Producto vectorial: la recta por dos puntos y el punto de corte de dos rectas", "Producto cuña y determinante como volumen orientado", "Colinealidad: $\\det[p\\,q\\,r]=0$", "Núcleo visto desde las filas"]
conceptos_previos: ["Producto interno (capítulo 1)", "Coordenadas homogéneas (capítulo 4)", "Formas lineales (capítulo 5)"]
apunte: ["subespacios"]
unidades: ["07a_cuna_determinante", "07b_nucleo_autovectores"]
animaciones: []
ejercicios_sugeridos: ["Calcular $p\\times q$ y $\\det[p\\,q\\,r]$ para $p=(1,2,3)$, $q=(4,5,-1)$, $r=(0,0,1)$ y comparar", "Unir $A$ y $C$ y cortar con $BD$ en el pentágono entero usando productos cruz", "Hallar el núcleo de una $3\\times3$ de filas coplanares con la cruz de dos filas"]
---

# Capítulo 6: subespacios, producto cuña y determinante

Unir, cortar y detectar colinealidad son una misma operación: el producto cuña, cuyo caso de tamaño $n$ es el determinante.

## Qué se estudia

- Subespacios lineales y afines, y las tres escrituras de una recta
- Producto vectorial: la recta por dos puntos y el punto de corte de dos rectas
- Producto cuña y determinante como volumen orientado
- Colinealidad: $\det[p\,q\,r]=0$
- Núcleo visto desde las filas

### Subespacio afín

Álgebra: $p+S$ con $S$ subespacio lineal: $\{p+\mu v\}$, $\{p+\mu v+\nu w\}$.
Se ve: una recta o un plano cualquiera, no necesariamente por el origen; es "la noción intuitiva de
subespacio". Tres escrituras de la misma recta: paramétrica ($p+\mu v$), implícita (una forma lineal
igualada a $c$: $n\cdot x=c$), y en homogéneas (una terna $\ell$ con $\ell\cdot(x,y,1)=0$).
Escalera: en $\mathbb{R}$ un subespacio afín es un punto; en $\mathbb{R}^2$ puntos y rectas; en
$\mathbb{R}^3$ además planos.

### Subespacio lineal

Álgebra: cerrado por suma y escala, contiene al cero. Se ve: rectas y planos
*por el origen*; en homogéneas, un subespacio lineal de $\mathbb{R}^3$ (un rayo) es un punto del
plano y un plano por el origen es una recta. Conviene pensar todo en términos de espacios y subespacios. Los planos elementales $e_1\wedge e_2$, $e_1\wedge e_3$,
$e_2\wedge e_3$ son los subespacios coordenados de dimensión 2.

### Producto vectorial (producto cruz)

Álgebra: $p\times q$ ortogonal a ambos, lineal en cada argumento,
$p\times p=0$; coordenadas $(p_2q_3-p_3q_2,\ p_3q_1-p_1q_3,\ p_1q_2-p_2q_1)$. Se ve: la recta que
une dos puntos ($\ell=p\times q$) y, por la simetría de la incidencia, el punto donde se cortan dos
rectas ($\ell\times m$; dos paralelas dan un punto ideal, su dirección común). Su norma es el área
del paralelogramo. Sólo existe en $\mathbb{R}^3$.

### Producto cuña (exterior)

Álgebra: $u\wedge v$, definido sólo por linealidad y antisimetría; el resultado
es un bivector (área orientada), $(u\wedge v)\wedge w=\det[u\,v\,w]\,e_1\wedge e_2\wedge e_3$. Se
ve: el paralelogramo orientado de lados $u,v$; con $w$, el paralelepípedo. Escalera: en $\mathbb{R}$
es $|a|$ con signo; en $\mathbb{R}^2$ el área $ad-bc$; en $\mathbb{R}^3$ el volumen; en
$\mathbb{R}^n$ hipervolumen, y la misma mecánica da "el vector ortogonal a un subespacio", lo que se
necesita para autovectores grandes. El producto cuña es un detector de colinealidad: vale cero
exactamente cuando los vectores se aplastan a algo de menor dimensión.

### Determinante

Álgebra: la única operación de $n$ vectores lineal en cada uno y nula cuando dos
coinciden; $\det[p\,q\,r]=(p\times q)\cdot r$; cambia de signo al intercambiar filas; desarrollo por
menores con signos $+,-,+$. Se ve: volumen orientado de la figura que forman los vectores; cuánto
agranda la transformación un cubo unidad y si invierte la orientación. Escalera: $|a|$, área,
volumen. Cero ⇔ dependientes ⇔ (en homogéneas) tres puntos alineados.

### Colinealidad (tres puntos alineados)

Álgebra: $\det[p\,q\,r]=0$ para ternas homogéneas; $(p\times q)\cdot r=0$. Se ve:
$r$ está en la recta que une $p$ y $q$ (y, simétricamente, cada uno en la recta de los otros dos).
Es la condición "sin tres alineados" para que cuatro puntos fijen una homografía (03p) y lo que
detecta el producto cuña en cualquier dimensión.

### Núcleo (espacio nulo)

Álgebra: $\{v: Av=0\}$; no trivial ⇔ $\det A=0$. Se ve: las direcciones que la
transformación aplasta a un punto; visto desde las filas, el vector donde todas las reglas (formas
lineales) marcan cero: ortogonal a todas las filas, que entonces caben en un plano. Escalera: en
$\mathbb{R}$, $ax=0$ tiene núcleo sólo si $a=0$; en $\mathbb{R}^2$ dos reglas con marcas cero
paralelas; en $\mathbb{R}^3$ tres filas coplanares. Construir una transformación con un vector dado en el núcleo es lo que hace $A-\lambda I$ en el capítulo 7.

## Conceptos previos

- Producto interno (capítulo 1)
- Coordenadas homogéneas (capítulo 4)
- Formas lineales (capítulo 5)

## En el apunte

- Capítulo 6. Subespacios, producto cuña y determinante

## Unidades interactivas

- Cuña y determinante: el detector de colinealidad (`07a_cuna_determinante`)
- Núcleo y autovectores: las direcciones que no giran (`07b_nucleo_autovectores`)

## Ejercicios sugeridos

- Calcular $p\times q$ y $\det[p\,q\,r]$ para $p=(1,2,3)$, $q=(4,5,-1)$, $r=(0,0,1)$ y comparar
- Unir $A$ y $C$ y cortar con $BD$ en el pentágono entero usando productos cruz
- Hallar el núcleo de una $3\times3$ de filas coplanares con la cruz de dos filas
