---
clase: 12
titulo: "Clase 12: curvatura y formas cuadráticas"
idea: "La curvatura de una superficie en un punto es una forma cuadrática: diagonalizar la hessiana da las dos curvaturas principales."
que_se_estudia: ["Curvatura de una curva y círculo osculador", "Forma cuadrática de la hessiana y direcciones principales", "Fórmula de Euler $\\chi(\\alpha)=\\kappa_1\\cos^2\\alpha+\\kappa_2\\sin^2\\alpha$", "Geodésicas como curvas que no se tuercen dentro de la superficie"]
conceptos_previos: ["Derivada, hessiana y primera forma (clase 9)", "Autovectores y diagonalización (clases 6 a 8)", "SVD (clase 7)"]
apunte: ["curvatura"]
unidades: ["12_curvatura"]
animaciones: ["05_elipsoide_euler_meusnier"]
ejercicios_sugeridos: ["Hallar la curvatura de $y=x^2/2$ en $x=0$ y en $x=1$", "Diagonalizar la hessiana de $z=x^2+xy+y^2$ y comprobar Euler a 45°", "Calcular la hessiana de la esfera en el polo"]
---

# Clase 12: curvatura y formas cuadráticas

La curvatura de una superficie en un punto es una forma cuadrática: diagonalizar la hessiana da las dos curvaturas principales.

## Qué se estudia

- Curvatura de una curva y círculo osculador
- Forma cuadrática de la hessiana y direcciones principales
- Fórmula de Euler $\chi(\alpha)=\kappa_1\cos^2\alpha+\kappa_2\sin^2\alpha$
- Geodésicas como curvas que no se tuercen dentro de la superficie

**Curvatura de una línea** (requiere derivada-aproximacion-lineal). En $\mathbb R$ no hay curvatura: una función de una variable se curva sólo al mirar su gráfico en $\mathbb R^2$. Definición: $\chi=\left|\dfrac{\partial\alpha/\partial v}{\|v\|}\right|$, la tasa de cambio del ángulo de la tangente respecto del avance sobre la curva; para un círculo, $\chi=1/R$. Lo que se ve: en cada punto hay un círculo que besa a la curva (osculador); la curvatura es $1/R$ de ese círculo. Recta: $R=\infty$, $\chi=0$. Para un gráfico $y=f(x)$: $\chi=\dfrac{|f''|}{(1+f'^2)^{3/2}}$; en un punto con tangente horizontal queda $\chi=|f''|$, la segunda derivada *es* la curvatura.

**Forma cuadrática** (requiere hessiana, svd). Pregunta: en un punto de una superficie $z=f(x,y)$ con tangente horizontal, ¿cuánto se curva la superficie si avanzo en la dirección $\alpha$? Álgebra: cortar con el plano vertical que contiene a $(\cos\alpha,\sin\alpha)$ da una curva plana cuya curvatura es
$$\chi(\alpha)=\begin{pmatrix}\cos\alpha&\sin\alpha\end{pmatrix}\begin{pmatrix}f_{xx}&f_{xy}\\f_{xy}&f_{yy}\end{pmatrix}\begin{pmatrix}\cos\alpha\\\sin\alpha\end{pmatrix},$$
la hessiana de la clase 9 evaluada en la dirección. Eso es una forma cuadrática: un número que sale de un vector pasando por una matriz simétrica, como $\|v\|^2=v^{\mathsf T}v$ pero con otra matriz en el medio. Lo que se ve: la hessiana es simétrica, y la clase 10 ya dijo que en las simétricas autovectores y vectores singulares coinciden y son ortogonales: hay dos direcciones perpendiculares, de curvatura máxima y mínima (direcciones principales, $\kappa_1,\kappa_2$), y en cualquier otra dirección $\chi(\alpha)=\kappa_1\cos^2\alpha+\kappa_2\sin^2\alpha$ (Euler; el apunte lo escribe $\chi=|A|+|B|\cos2\alpha$). Diagonalizar la hessiana es rotar los ejes hasta que desaparezca el término cruzado. En $\mathbb R^2$ esto es el problema 4 de la clase 11 (eje mayor y menor de una elipse); en $\mathbb R^n$ es la SVD de una matriz simétrica. El producto $\kappa_1\kappa_2=\det(\text{hessiana})$ es la curvatura de Gauss $K$, que el capítulo «Curvatura como forma cuadrática» del apunte escribe para el elipsoide como $K=1/(MN)$; el determinante vuelve a ser cuánto área (clase 5), ahora de la imagen de la normal.

**Geodésica** (requiere primera-forma-fundamental). Pregunta: ¿qué es ir derecho sobre una superficie? Una curva es geodésica cuando no se tuerce *dentro* de la superficie, es decir cuando toda su curvatura es la que la superficie le obliga (su aceleración es normal a la superficie, componente tangencial cero). Lo que se ve: es la trayectoria de un hilo tenso sobre la cáscara, o de un auto que va con el volante derecho; es la más corta entre puntos cercanos. En la esfera son los círculos máximos; en el elipsoide, los meridianos lo son y los paralelos no (salvo el ecuador). El azimut es el ángulo diedro entre el plano meridiano del lugar $a$ y el plano vertical que contiene al vector tangente a la geodésica que une $a$ con $b$.

Escalera: $\mathbb R$ (segunda derivada), $\mathbb R^2$ (curvatura de una curva, un número por punto), $\mathbb R^3$ (superficie: una forma cuadrática por punto, dos curvaturas principales), $\mathbb R^n$ (hessiana $n\times n$, $n$ curvaturas principales por diagonalización).

## Conceptos previos

- Derivada, hessiana y primera forma (clase 9)
- Autovectores y diagonalización (clases 6 a 8)
- SVD (clase 7)

## En el apunte

- Capítulo 13. Curvatura

## Unidades interactivas

- Curvatura como forma cuadrática (`12_curvatura`)

## Animaciones

- `05_elipsoide_euler_meusnier`

## Ejercicios sugeridos

- Hallar la curvatura de $y=x^2/2$ en $x=0$ y en $x=1$
- Diagonalizar la hessiana de $z=x^2+xy+y^2$ y comprobar Euler a 45°
- Calcular la hessiana de la esfera en el polo
