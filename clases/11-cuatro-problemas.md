---
clase: 11
titulo: "Capítulo 12: cuatro problemas de ajuste"
idea: "Regresión simple, intersección de círculos, Procrustes y regresión total son un solo problema: hallar el residuo perpendicular a una imagen."
que_se_estudia: ["Regresión simple por ecuaciones normales", "Intersección de círculos: restar ecuaciones deja un sistema lineal", "Procrustes: rotación y escala óptimas por SVD de $H=P^TQ$", "Regresión total: la recta de menor distancia perpendicular"]
conceptos_previos: ["Pseudoinversa y sistemas sobredeterminados (capítulo 11)", "SVD y valores singulares (capítulo 8)", "Producto interno (capítulo 1)"]
apunte: ["cuatro-problemas"]
unidades: ["11_cuatro_problemas"]
animaciones: []
ejercicios_sugeridos: ["Ajustar la recta a $(-1,1)$, $(0,1)$, $(1,4)$ y comprobar la ortogonalidad del residuo", "Hallar la intersección de tres círculos dados restando sus ecuaciones", "Recuperar con SVD la rotación entre un cuadrado y el mismo cuadrado girado 90°", "Comparar regresión simple y total sobre los puntos $(\\pm1,0)$, $(0,\\pm2)$"]
---

# Capítulo 12: cuatro problemas de ajuste

Regresión simple, intersección de círculos, Procrustes y regresión total son un solo problema: hallar el residuo perpendicular a una imagen.

## Qué se estudia

- Regresión simple por ecuaciones normales
- Intersección de círculos: restar ecuaciones deja un sistema lineal
- Procrustes: rotación y escala óptimas por SVD de $H=P^TQ$
- Regresión total: la recta de menor distancia perpendicular

**Regresión simple** (requiere pseudoinversa, sistema sobredeterminado). Pregunta: $n$ puntos $(x_i,y_i)$ que «deberían» estar en una recta $y=ax+b$ pero no están; ¿qué recta? Álgebra: el sistema $A\theta=y$ con $A$ de $n\times 2$ (columna de las $x$, columna de unos) y $\theta=(a,b)$ no tiene solución; las ecuaciones normales $A^{\mathsf T}A\,\theta=A^{\mathsf T}y$ dan $\theta=A^{+}y$. Lo que se ve: en $\mathbb R^n$ el vector $y$ no está en el plano generado por las dos columnas de $A$; la solución es la proyección ortogonal de $y$ sobre ese plano (capítulo 11: la imagen y su complemento). Ojo: la distancia que se minimiza es la vertical en cada $x_i$, no la perpendicular a la recta. Eso es lo que la separa del problema 4.

**Intersección de círculos** (requiere pseudoinversa, nucleo). Pregunta: tres o más círculos conocidos (centro y radio) que deberían cortarse en un punto; ¿cuál? Álgebra: cada círculo es cuadrático, $(x-a_i)^2+(y-b_i)^2=r_i^2$, pero al restar dos ecuaciones se cancelan $x^2+y^2$ y queda una recta: $2(a_j-a_i)x+2(b_j-b_i)y=r_i^2-r_j^2-a_i^2+a_j^2-b_i^2+b_j^2$. Con $m$ círculos salen $m-1$ rectas: sistema lineal, sobredeterminado si $m\ge4$, pseudoinversa. Lo que se ve: restar dos círculos da la recta que pasa por sus dos puntos de corte (eje radical); tres círculos, dos rectas, un punto. Conexión con Topografía (sin desarrollar): es la trilateración, y es la base del posicionamiento por distancias.

**Procrustes** (requiere svd, producto-interno). Pregunta: una nube de puntos medida en un sistema y la misma nube en otro; ¿qué rotación (y escala) superpone mejor una sobre la otra? Álgebra: centrar las dos nubes, armar $H=P^{\mathsf T}Q$ ($2\times2$, la «matriz de correlación» de las coordenadas), descomponer $H=U\Sigma V^{\mathsf T}$; la rotación es $R=VU^{\mathsf T}$ y la escala $\operatorname{tr}\Sigma/\|P\|^2$. Lo que se ve: la SVD de $H$ separa «cuánto giro» ($U$, $V$) de «cuánto estiro» ($\Sigma$); si las nubes son la misma figura girada, $\Sigma$ es un múltiplo de la identidad y $R$ es exactamente el giro. Conexión con Topografía (sin desarrollar): es la transformación de Helmert 2D, el ajuste de dos sistemas de coordenadas con puntos comunes.

**Regresión total** (requiere svd, valores-singulares). Pregunta: la misma nube del problema 1, pero ahora las $x$ también tienen error; ¿cuál es la recta que minimiza las distancias *perpendiculares*? Álgebra: centrar, armar la matriz de datos $X$ ($n\times2$), SVD $X=U\Sigma V^{\mathsf T}$; la dirección de la recta es el primer vector singular derecho (mayor $\sigma$), la normal es el segundo (menor $\sigma$), y $\sigma_{\min}^2$ es la suma de residuos al cuadrado. Lo que se ve: la nube tiene una elipse de dispersión; la recta total es su eje mayor; la dirección de menor varianza es la que «no explica nada» y es la normal. Es la misma imagen del capítulo 8 (circunferencia que se vuelve elipse) leída al revés: datos → elipse → ejes.

Escalera: en $\mathbb R$, ajustar $n$ medidas $y_i\approx c$ es tomar el promedio (proyección sobre la columna de unos). En $\mathbb R^2$ aparece la recta y la diferencia vertical/perpendicular. En $\mathbb R^n$ todo sigue igual: columnas de $A$, proyección, SVD. El remate del proyecto está en `datos/dem_copernicus/README.md`: la SVD de un DEM de $512\times512$ es el problema 4 en grande, con la nota didáctica de que “la energía acumulada engaña (99,6 % con $k=1$) porque la media domina $\sigma_1$” — restar la media antes, igual que centrar la nube.

## Conceptos previos

- Pseudoinversa y sistemas sobredeterminados (capítulo 11)
- SVD y valores singulares (capítulo 8)
- Producto interno (capítulo 1)

## En el apunte

- Capítulo 12. Cuatro problemas de ajuste

## Unidades interactivas

- Cuatro problemas: regresión, círculos, Procrustes, regresión total (`11_cuatro_problemas`)

## Ejercicios sugeridos

- Ajustar la recta a $(-1,1)$, $(0,1)$, $(1,4)$ y comprobar la ortogonalidad del residuo
- Hallar la intersección de tres círculos dados restando sus ecuaciones
- Recuperar con SVD la rotación entre un cuadrado y el mismo cuadrado girado 90°
- Comparar regresión simple y total sobre los puntos $(\pm1,0)$, $(0,\pm2)$
