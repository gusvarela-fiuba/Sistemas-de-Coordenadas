---
clase: 7
titulo: "Clase 7: la SVD, de la circunferencia a la elipse"
idea: "Toda matriz lleva una base ortonormal de la entrada en una base ortogonal de la salida, estirada por los valores singulares: circunferencia a elipse."
que_se_estudia: ["La pregunta de la SVD: qué direcciones perpendiculares siguen perpendiculares", "$A=U\\Sigma V^T$ como giro, estiramiento y giro", "Valores singulares, determinante y núcleo", "Matriz simétrica: vectores singulares y autovectores coinciden", "Aproximación de rango $k$ de una matriz de alturas"]
conceptos_previos: ["Autovectores y autovalores (clase 6)", "Matrices ortogonales (clase 1)", "Núcleo (clase 5)"]
apunte: ["svd", "dem"]
unidades: ["09_cambio_de_base_svd"]
animaciones: ["04_svd_circulo_a_elipse"]
ejercicios_sugeridos: ["Calcular a mano la SVD de $\\begin{pmatrix}3&0\\\\4&5\\end{pmatrix}$ y comprobar $\\sigma_1\\sigma_2=15$", "Mostrar que la rotación de 90° tiene valores singulares $1,1$ y ningún autovector real", "Reconstruir una matriz de alturas con los primeros $k$ valores singulares y medir el error"]
---

# Clase 7: la SVD, de la circunferencia a la elipse

Toda matriz lleva una base ortonormal de la entrada en una base ortogonal de la salida, estirada por los valores singulares: circunferencia a elipse.

## Qué se estudia

- La pregunta de la SVD: qué direcciones perpendiculares siguen perpendiculares
- $A=U\Sigma V^T$ como giro, estiramiento y giro
- Valores singulares, determinante y núcleo
- Matriz simétrica: vectores singulares y autovectores coinciden
- Aproximación de rango $k$ de una matriz de alturas

**La pregunta antes que la fórmula.** Diagonalizar pregunta ¿qué direcciones caen sobre sí mismas?. Pero una rotación de 90° no deja ninguna dirección quieta, y el polinomio característico lo dice con raíces complejas. La SVD cambia la pregunta: ¿qué direcciones perpendiculares de la entrada siguen perpendiculares a la salida?. Esa pregunta siempre tiene respuesta real.

**Escalera.**
- En $\mathbb R$: $x\mapsto a x$. "Diagonalizar" es trivial (todo $x$ es autovector). La SVD de un número es $a = (\pm1)\cdot|a|\cdot 1$: un signo a la salida, un estiramiento $|a|$, nada a la entrada. El valor singular es $|a|$; el signo quedó en la "base de salida".
- En $\mathbb R^2$: la circunferencia unidad va a una elipse. Los semiejes de la elipse son $\sigma_1\ge\sigma_2\ge0$ (valores singulares); sus direcciones $u_1,u_2$ son la base ortonormal de salida; las direcciones de la circunferencia que van a parar a esos semiejes, $v_1,v_2$, son la base ortonormal de entrada. $A v_i = \sigma_i u_i$. Hecho central: **circunferencia → elipse, con bases ortonormales a ambos lados.**
- En $\mathbb R^3$: esfera → elipsoide, tres semiejes. Si la matriz es $3\times2$ (como la jacobiana de una superficie parametrizada, clase 9), la circunferencia del plano $(u,v)$ va a una elipse que vive en el plano tangente dentro de $\mathbb R^3$; el tercer vector $u_3$ apunta a la dirección "inaccesible" (la normal). Ese es el cambio de base rectangular: $U$ es $3\times3$, $V$ es $2\times2$, $\Sigma$ es $3\times2$.
- En $\mathbb R^n$: una matriz $512\times512$ es una transformación de $\mathbb R^{512}$, y sus 512 valores singulares ordenados dicen cuánta "forma" hay en cada dirección principal. Quedarse con los $k$ primeros es la mejor aproximación de rango $k$ (ver el remate con el DEM).

**Lo que dice el álgebra ↔ lo que se ve.**
- $A = U\Sigma V^{T}$ ↔ girar (o reflejar) con $V^{T}$, estirar en los ejes con $\Sigma$, girar con $U$. Tres movimientos que entendemos por separado (clases 1 y 3).
- $\Sigma$ diagonal con entradas $\ge0$, nunca complejas ↔ no hay giro escondido que arruine la cuenta, porque el giro se lo llevaron $U$ y $V$.
- $\sigma_1\cdots\sigma_n = |\det A|$ ↔ el área (volumen) de la elipse es el de la circunferencia por el producto de los semiejes.
- $\sigma_k = 0$ ↔ la elipse se aplastó en esa dirección: $v_k$ está en el núcleo, $u_k$ queda fuera de la imagen. Las dos bases relacionadas con el núcleo y la imagen son exactamente $V$ y $U$.
- Base privilegiada ↔ no hay base privilegiada salvo por el producto interno: la SVD la construye a partir del producto interno (ortogonalidad), no a partir de direcciones fijas. Por eso siempre existe.
- Matriz simétrica ↔ la elipse tiene los ejes en las direcciones propias: $U=V$ y $\sigma_i=|\lambda_i|$. Este caso reaparece en la clase 10.

## Conceptos previos

- Autovectores y autovalores (clase 6)
- Matrices ortogonales (clase 1)
- Núcleo (clase 5)

## En el apunte

- Capítulo 8. La SVD: leer la forma de las curvas de nivel
- Complemento C3. El terreno como matriz

## Unidades interactivas

- Cambio de base, SVD e inversas (`09_cambio_de_base_svd`)

## Animaciones

- `04_svd_circulo_a_elipse`

## Ejercicios sugeridos

- Calcular a mano la SVD de $\begin{pmatrix}3&0\\4&5\end{pmatrix}$ y comprobar $\sigma_1\sigma_2=15$
- Mostrar que la rotación de 90° tiene valores singulares $1,1$ y ningún autovector real
- Reconstruir una matriz de alturas con los primeros $k$ valores singulares y medir el error
