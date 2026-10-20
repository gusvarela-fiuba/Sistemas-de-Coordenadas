---
clase: 4
titulo: "Capítulo 5: formas lineales y dualidad"
idea: "Una forma lineal es una regla graduada: sus marcas son rectas paralelas, y al deformar el plano la regla se transforma al revés que los vectores."
que_se_estudia: ["Espacio vectorial y transformación lineal como grilla que se deforma", "Forma lineal como regla graduada y curvas de nivel", "Dualidad: los vectores van con $A$ y las formas con $A^{-1}$", "El gradiente como forma lineal"]
conceptos_previos: ["Producto interno (capítulo 1)", "Coordenadas homogéneas (capítulo 4)", "Homografías: puntos con $H$, rectas con $H^{-T}$ (complemento C1)"]
apunte: ["formas-lineales"]
unidades: ["00_fundamentos", "06_formas_lineales"]
animaciones: ["01_dualidad_gradiente"]
ejercicios_sugeridos: ["Transformar un vector y dos formas con $T$ y $T^{-1}$ y comprobar que las lecturas de marcas se conservan", "Dibujar las curvas de nivel de $2x+3y$ y hallar su núcleo", "Ver que $\\begin{pmatrix}2&3\\\\4&6\\end{pmatrix}$ tiene núcleo y $\\begin{pmatrix}2&3\\\\1&-1\\end{pmatrix}$ no"]
---

# Capítulo 5: formas lineales y dualidad

Una forma lineal es una regla graduada: sus marcas son rectas paralelas, y al deformar el plano la regla se transforma al revés que los vectores.

## Qué se estudia

- Espacio vectorial y transformación lineal como grilla que se deforma
- Forma lineal como regla graduada y curvas de nivel
- Dualidad: los vectores van con $A$ y las formas con $A^{-1}$
- El gradiente como forma lineal

### Espacio vectorial

Álgebra: un conjunto con suma y producto por escalar que respetan linealidad.
Se ve: flechas que se encadenan (paralelogramo) y se estiran; el cero queda quieto. Escalera:
$\mathbb{R}$ es un espacio vectorial donde todo es «multiplicar por un número»; $\mathbb{R}^2$
agrega direcciones; $\mathbb{R}^n$ no agrega nada nuevo salvo que ya no se dibuja. Vocabulario de la
materia: los vectores son puntos, y en homogéneas los puntos del plano son vectores de
$\mathbb{R}^3$.

### Transformación lineal y su matriz

Álgebra: $T(v+u)=T(v)+T(u)$, $T(\lambda v)=\lambda T(v)$; el cero va al
cero. Se ve: la grilla cuadrada se vuelve una grilla de paralelogramos, pero sigue siendo grilla
(rectas paralelas equiespaciadas). Cada coordenada de salida es una regla que mide la entrada: por
eso la matriz es una pila de ecuaciones de rectas. La matriz es una pila de formas
(filas) o una hilera de vectores (columnas: adónde van $e_1,e_2$).

### Forma lineal

Álgebra: $\varphi:\mathbb{R}^n\to\mathbb{R}$ lineal; en coordenadas, una fila
$(a,b)$ y $\varphi(x,y)=ax+by$. Se ve: una regla graduada tirada en el plano: sus marcas son rectas
paralelas equiespaciadas, perpendiculares al vector $(a,b)$, con separación $1/\|(a,b)\|$. En
$\mathbb{R}$: multiplicar por $a$, marcas a distancia $1/a$. En $\mathbb{R}^3$: planos paralelos.
Las selectoras $\mathsf{x},\mathsf{y}$ son las reglas de los ejes; cualquier forma es combinación de
ellas. Incidencia proyectiva: la recta $\ell=(a,b,c)$ *es* una forma, y $\ell\cdot p=0$ dice que $p$
está en su marca cero.

### Dualidad vectores–formas

Álgebra: las formas forman un espacio vectorial del mismo tamaño (el dual); fila por
columna es un número; al transformar el plano con $A$ los vectores van con $A$ (columna, a la
izquierda) y las formas con $A^{-1}$ (fila, a la derecha) para que $\varphi(v)$ no cambie; o bien
«qué regla mide lo mismo sobre el $v$ original»: $(\varphi A)(v)=\varphi(Av)$. Se ve: si deformo la
figura, la regla que la mide se deforma *con* ella, y por eso sus coeficientes cambian «al revés».
Sin producto interno, una forma y un vector son objetos distintos; el producto interno es lo que
permite disfrazar la forma $(2,3)$ de vector $(2,3)$ (no hay base privilegiada salvo por el
producto interno). En proyectivas, intercambiar puntos y rectas es la dualidad.

### Curvas de nivel de una forma lineal

Álgebra: $\{v:\varphi(v)=c\}$ para $c=0,\pm1,\pm2,\ldots$ Se ve: la familia de
rectas paralelas de la regla; dos formas dan una grilla y un vector queda ubicado por qué par de
marcas lo cruza (por ejemplo, la séptima con la quinta). Si la transformación estira el autovector, su grilla
se comprime (forma con $A^{-1}$); una matriz diagonal estira grillas independientemente y no las
rompe. El gradiente de una función en un punto es una forma lineal: su recta de nivel cero es la
tangente a la curva de nivel (ir a lo chico para volver a lo grande).

## Conceptos previos

- Producto interno (capítulo 1)
- Coordenadas homogéneas (capítulo 4)
- Homografías: puntos con $H$, rectas con $H^{-T}$ (complemento C1)

## En el apunte

- Capítulo 5. Formas lineales: el gradiente no es un vector

## Unidades interactivas

- El idioma de la materia: puntos, flechas, reglas y distancias (`00_fundamentos`)
- Formas lineales y dualidad (`06_formas_lineales`)

## Animaciones

- `01_dualidad_gradiente`

## Ejercicios sugeridos

- Transformar un vector y dos formas con $T$ y $T^{-1}$ y comprobar que las lecturas de marcas se conservan
- Dibujar las curvas de nivel de $2x+3y$ y hallar su núcleo
- Ver que $\begin{pmatrix}2&3\\4&6\end{pmatrix}$ tiene núcleo y $\begin{pmatrix}2&3\\1&-1\end{pmatrix}$ no
