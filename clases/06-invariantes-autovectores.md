---
clase: 6
titulo: "Capítulo 7: subespacios invariantes, autovalores y autovectores"
idea: "Un autovector es una dirección que la transformación no hace girar: es el núcleo de $A-\\lambda I$ y se calcula con un producto cruz de filas."
que_se_estudia: ["Subespacio invariante y dirección que cae sobre sí misma", "Autovector y autovalor; autovector por producto cruz de dos filas de $A-\\lambda I$", "Polinomio característico como detector de colinealidad", "El eje de una rotación 3D y los puntos fijos de una proyectiva"]
conceptos_previos: ["Núcleo, determinante y producto cuña (capítulo 6)", "Formas lineales (capítulo 5)", "Punto fijo (capítulos 3 y 4)", "Rotaciones 3D (capítulo 1)"]
apunte: ["autovectores", "pentagono", "proyectivas"]
unidades: ["07b_nucleo_autovectores", "07c_autovalores_3d_puntos_fijos"]
animaciones: []
ejercicios_sugeridos: ["Hallar autovalores y autovectores de $\\mathrm{diag}(1,1,-1)$ con la cruz de filas", "Hallar el eje de $R_z(90°)R_y(90°)$ y comprobar que es $(-1,1,1)$", "Diagonalizar $\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$ con la perpendicular a una fila"]
---

# Capítulo 7: subespacios invariantes, autovalores y autovectores

Un autovector es una dirección que la transformación no hace girar: es el núcleo de $A-\lambda I$ y se calcula con un producto cruz de filas.

## Qué se estudia

- Subespacio invariante y dirección que cae sobre sí misma
- Autovector y autovalor; autovector por producto cruz de dos filas de $A-\lambda I$
- Polinomio característico como detector de colinealidad
- El eje de una rotación 3D y los puntos fijos de una proyectiva

### Subespacio invariante

Álgebra: $S$ con $A(S)\subseteq S$. Se ve: una recta por el origen que,
al transformar, cae sobre sí misma (quizá estirada o invertida); un plano que cae sobre sí mismo. El
$\{0\}$ siempre es invariante (el cero va al cero). En homogéneas, una recta invariante de
$\mathbb{R}^3$ es un punto fijo del plano, un plano invariante es una recta fija. Escalera: en
$\mathbb{R}$ todo es invariante (sólo hay una dirección); en $\mathbb{R}^2$ hay 0, 1, 2 direcciones
invariantes o todas (homotecia); en $\mathbb{R}^3$ siempre hay al menos una.

### Autovector

Álgebra: $v\neq0$ con $Av=\lambda v$; está en el núcleo de $A-\lambda I$; se calcula
como cruz (cuña) de dos filas de $A-\lambda I$. Se ve: la dirección que no gira, sólo se escala; el
eje de una rotación; los puntos fijos de una proyectiva. Una versión modificada de la
transformación que tenga al autovector en el núcleo: restar $\lambda I$ es correr cada regla de la
matriz hasta que las tres marquen cero sobre $v$. Si todos los pares de filas dan cruz nula, hay un
plano entero (en homogéneas, una recta entera de puntos fijos: el eje de una homología).

### Autovalor

Álgebra: raíz real de $\det(A-\lambda I)=0$. Se ve: cuánto se estira la dirección
fija: $1$ queda quieta (eje de rotación, puntos fijos "de verdad"), $-1$ se invierte (reflexión),
$|\lambda|>1$ estira, $0$ aplasta (la matriz tiene núcleo). Escalera: en $\mathbb{R}$,
$a\cdot x=\lambda x$ es trivial, $\lambda=a$ y todo $x$ sirve; en $\mathbb{R}^2$ sólo algunas
direcciones, o ninguna real si hay giro; en $\mathbb{R}^3$ al menos una real. Los autovalores
complejos no dan vectores de $\mathbb{R}^3$: dicen que en un plano hay un giro (los
$e^{\pm i72^\circ}$ de la rotación del pentágono; los $\pm4i$ del ciclo de cuatro, $H^4\sim I$).

### Polinomio característico

Álgebra: $\det(A-\lambda I)$, grado $n$; sus raíces son los
autovalores; en $3\times3$, grado impar ⇒ una raíz real. Se ve: es el "detector de colinealidad"
aplicado a las filas de $A-\lambda I$: para qué valores de $\lambda$ las tres reglas corridas se
vuelven coplanares. Una raíz doble con cruz nula es un plano de autovectores; las complejas vienen
de a pares conjugados. Una matriz genérica da raíces irracionales y feas: por eso el método tiene
que funcionar en planilla o en código, no sólo a mano.

## Conceptos previos

- Núcleo, determinante y producto cuña (capítulo 6)
- Formas lineales (capítulo 5)
- Punto fijo (capítulos 3 y 4)
- Rotaciones 3D (capítulo 1)

## En el apunte

- Capítulo 7. Subespacios invariantes: autovalores y autovectores
- Sección C1.3.2. El pentágono
- Complemento C1. Transformaciones proyectivas

## Unidades interactivas

- Núcleo y autovectores: las direcciones que no giran (`07b_nucleo_autovectores`)
- Autovalores en 3D y puntos fijos proyectivos (`07c_autovalores_3d_puntos_fijos`)

## Ejercicios sugeridos

- Hallar autovalores y autovectores de $\mathrm{diag}(1,1,-1)$ con la cruz de filas
- Hallar el eje de $R_z(90°)R_y(90°)$ y comprobar que es $(-1,1,1)$
- Diagonalizar $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ con la perpendicular a una fila
