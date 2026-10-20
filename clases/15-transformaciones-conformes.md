---
clase: 15
titulo: "Complemento C2: transformaciones conformes, de Cauchy-Riemann a Gauss-Krüger"
idea: "Una transformación es conforme cuando su matriz jacobiana es, en cada punto, una similaridad directa: conserva todos los ángulos y estira por igual en todas las direcciones con un factor puntual $k(P)$."
que_se_estudia: ["Condición de conformidad: $J = k\\,R(\\theta)$, ecuaciones de Cauchy-Riemann y valores singulares $\\sigma_1 = \\sigma_2 = k$", "Indicatriz de Tissot: la elipse imagen de un círculo infinitesimal, deformación angular y de área", "Latitud isométrica $q(\\varphi)$ y proyección cilíndrica conforme de Mercator", "Proyección de Gauss-Krüger (Mercator transversa) y las 7 fajas POSGAR de la Argentina"]
conceptos_previos: ["Números complejos y similaridades (capítulos 1 y 3)", "Matriz jacobiana y primera forma fundamental (capítulo 10)", "Descomposición en valores singulares (capítulo 8)", "Geometría del elipsoide y radios $M$, $N$ (capítulo 14)"]
apunte: ["conformes", "elipsoide", "esfera"]
unidades: ["15_transformaciones_conformes"]
animaciones: ["06_conforme_tissot_mercator"]
ejercicios_sugeridos: ["Comprobar que la función compleja $(x+iy)^2 = (x^2-y^2) + i(2xy)$ cumple Cauchy-Riemann y que su matriz jacobiana tiene la forma $\\begin{pmatrix}a&-b\\\\b&a\\end{pmatrix}$", "Calcular la latitud isométrica esférica $q(\\varphi)$ y el factor de escala de Mercator en $\\varphi = 34^\\circ$ y $\\varphi = 60^\\circ$", "Determinar a qué faja de Gauss-Krüger pertenece un punto de longitud $64^\\circ\\text{ O}$ y estimar el factor de escala $k \\approx 1 + \\tfrac{1}{2}\\cos^2\\varphi\\,\\Delta\\lambda^2$ a $1^\\circ$ del meridiano central"]
---

# Complemento C2: transformaciones conformes, de Cauchy-Riemann a Gauss-Krüger

Una transformación es conforme cuando su matriz jacobiana es, en cada punto, una similaridad directa: conserva todos los ángulos y estira por igual en todas las direcciones con un factor puntual $k(P)$.

## Qué se estudia

- Condición de conformidad: $J = k\,R(\theta)$, ecuaciones de Cauchy-Riemann y valores singulares $\sigma_1 = \sigma_2 = k$
- Indicatriz de Tissot: la elipse imagen de un círculo infinitesimal, deformación angular y de área
- Latitud isométrica $q(\varphi)$ y proyección cilíndrica conforme de Mercator
- Proyección de Gauss-Krüger (Mercator transversa) y las 7 fajas POSGAR de la Argentina

### Transformación conforme y ecuaciones de Cauchy-Riemann

Álgebra: una aplicación diferenciable $(u,v)\mapsto(x(u,v),y(u,v))$ es conforme y directa cuando su matriz jacobiana tiene la forma de un número complejo no nulo (capítulo 1):
$$J = \begin{pmatrix}x_u & x_v \\ y_u & y_v\end{pmatrix} = \begin{pmatrix}a & -b \\ b & a\end{pmatrix} = k\,R(\theta),\qquad k = \sqrt{a^2+b^2} > 0,$$
lo que equivale a las ecuaciones de Cauchy-Riemann $x_u = y_v$, $x_v = -y_u$. En términos de la primera forma fundamental (capítulo 10), $J^{\mathsf T}J = k^2 I$, o sea $E = G = k^2$ y $F = 0$; en términos de la descomposición en valores singulares (capítulo 8), $\sigma_1 = \sigma_2 = k$. Se ve: con una lupa alrededor de cada punto $P$, una grilla de cuadraditos infinitesimales se gira un ángulo $\theta(P)$ y se agranda por el factor de escala puntual $k(P)$ sin cizallarse; dos curvas que se cortan con un ángulo en el terreno se cortan con el mismo ángulo en el plano. Escalera: en $\mathbb R^2\to\mathbb R^2$ las funciones holomorfas $w=f(z)$ con $f'(z)\neq 0$ dan todas las transformaciones conformes directas; del elipsoide al plano, como la curvatura de Gauss $K = 1/(MN)$ es positiva (capítulo 13 y capítulo 14), no existe ninguna carta que conserve todas las distancias ($k$ no puede ser constante igual a $1$), así que conservar los ángulos exige aceptar que la escala $k(P)$ varíe suavemente de punto a punto.

### Indicatriz de Tissot

Álgebra: un círculo infinitesimal de radio unidad en el plano tangente al elipsoide se transforma mediante la matriz jacobiana de la proyección en una elipse de semiejes $\sigma_1 \ge \sigma_2 > 0$ (sus valores singulares). La deformación angular máxima es $\omega = 2\arcsin\frac{\sigma_1-\sigma_2}{\sigma_1+\sigma_2}$ y el factor de área es $\sigma_1\sigma_2 = \det J$. Se ve: dibujar esa elipse en distintos puntos del mapa revela de un vistazo qué conserva y qué deforma la proyección: es un círculo en todo punto ($\sigma_1 = \sigma_2$, $\omega = 0$) si y solo si la proyección es conforme; mantiene área unidad ($\sigma_1\sigma_2 = 1$) si la proyección es equivalente; y mantiene un semieje igual a $1$ ($h=1$) si es equidistante a lo largo del meridiano.

### Latitud isométrica y proyección de Mercator

Álgebra: sobre el elipsoide de revolución (capítulo 14), el elemento de arco es $ds^2 = M^2\,d\varphi^2 + N^2\cos^2\varphi\,d\lambda^2 = N^2\cos^2\varphi\left(\frac{M^2}{N^2\cos^2\varphi}\,d\varphi^2 + d\lambda^2\right)$. Definiendo la *latitud isométrica* $q(\varphi)$ por $dq = \frac{M(\varphi)}{N(\varphi)\cos\varphi}\,d\varphi$, es decir
$$q(\varphi) = \ln\tan\!\left(\frac{\pi}{4}+\frac{\varphi}{2}\right) - \frac{e}{2}\ln\frac{1+e\sin\varphi}{1-e\sin\varphi},$$
la primera forma fundamental queda isotrópica: $ds^2 = N^2\cos^2\varphi\,(dq^2 + d\lambda^2)$. La proyección de Mercator pone simplemente $x = a\,\lambda$, $y = a\,q(\varphi)$. Se ve: como al subir hacia el polo los paralelos se achican como $\cos\varphi$, para que los cuadraditos sigan siendo cuadrados hay que estirar los meridianos en la misma proporción; por eso en Mercator las regiones de alta latitud se inflan con factor de escala $k(\varphi) = \frac{a}{N(\varphi)\cos\varphi}$ y las loxodromias (curvas que cortan todos los meridianos con el mismo acimut) se ven como rectas.

### Gauss-Krüger y las fajas POSGAR de la Argentina

Álgebra: toda función holomorfa $x + iy = f(\Delta\lambda + i\,q)$ de las coordenadas isométricas $(\Delta\lambda, q)$ —donde $\Delta\lambda = \lambda - \lambda_0$ es la longitud respecto de un meridiano central $\lambda_0$— conserva la conformidad por la regla de la cadena (composición de matrices tipo complejo). La proyección de Gauss-Krüger elige la única función analítica $f$ tal que sobre el meridiano central ($\Delta\lambda = 0$) la coordenada norte coincida exactamente con el arco de meridiano $S(\varphi) = \int_0^\varphi M(\varphi)\,d\varphi$. A segundo orden en $\Delta\lambda$, el factor de escala puntual es
$$k(\varphi,\Delta\lambda) \approx 1 + \frac{1}{2}\cos^2\varphi\,\Delta\lambda^2 \approx 1 + \frac{y_{\text{este}}^2}{2\,M(\varphi)N(\varphi)}.$$
Se ve: en lugar de apoyar el cilindro en el ecuador como Mercator, Gauss-Krüger lo apoya tangente al meridiano central $\lambda_0$. Sobre ese meridiano la escala es exacta ($k=1$) y crece cuadráticamente al alejarse hacia el este o el oeste. Como la Argentina es alargada de norte a sur, el marco oficial POSGAR divide el país en 7 fajas meridianas de $3^\circ$ de ancho, numeradas de 1 a 7 con meridianos centrales en $72^\circ, 69^\circ, 66^\circ, 63^\circ, 60^\circ, 57^\circ$ y $54^\circ$ oeste (y falso este de $500\,000\text{ m}$ precedido por el número de faja), manteniendo la distorsión de escala por debajo de $1{,}00015$ ($15\text{ cm}$ por kilómetro) en el borde de cada faja.

## Conceptos previos

- Números complejos y similaridades (capítulos 1 y 3)
- Matriz jacobiana y primera forma fundamental (capítulo 10)
- Descomposición en valores singulares (capítulo 8)
- Geometría del elipsoide y radios $M$, $N$ (capítulo 14)

## En el apunte

- Complemento C2. Transformaciones conformes
- Capítulo 14. Geometría del elipsoide
- Capítulo 15. Coordenadas sobre la esfera y trigonometría esférica

## Unidades interactivas

- Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico (`15_transformaciones_conformes`)

## Animaciones

- `06_conforme_tissot_mercator`

## Ejercicios sugeridos

- Comprobar que la función compleja $(x+iy)^2 = (x^2-y^2) + i(2xy)$ cumple Cauchy-Riemann y que su matriz jacobiana tiene la forma $\begin{pmatrix}a&-b\\b&a\end{pmatrix}$
- Calcular la latitud isométrica esférica $q(\varphi)$ y el factor de escala de Mercator en $\varphi = 34^\circ$ y $\varphi = 60^\circ$
- Determinar a qué faja de Gauss-Krüger pertenece un punto de longitud $64^\circ\text{ O}$ y estimar el factor de escala $k \approx 1 + \tfrac{1}{2}\cos^2\varphi\,\Delta\lambda^2$ a $1^\circ$ del meridiano central
