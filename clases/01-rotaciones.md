---
clase: 1
titulo: "Capítulo 1: rotaciones, de los complejos a la exponencial"
idea: "Una rotación es la transformación que fija un punto y conserva distancias, ángulos y orientación; se escribe con complejos, con matrices ortogonales y, en lo pequeño, con la exponencial."
que_se_estudia: ["Rotación con y sin centro en el origen, y su escritura con números complejos y con matrices 2x2", "Producto interno y matrices ortogonales: qué significa conservar distancias y ángulos", "Rotaciones en el espacio: R_x, R_y, R_z y el orden de composición", "Rotaciones infinitesimales: Id + P con P antisimétrica", "Exponencial de matrices y logaritmo: la rotación como repetición de pasos chicos"]
conceptos_previos: ["Transformación lineal y matriz 2x2 (CBC)", "Producto interno y módulo de un vector", "Números complejos (secundario)"]
apunte: ["rotaciones", "rot3d", "infinitesimales", "repaso-algebra"]
unidades: ["00_fundamentos", "01a_punto_quieto", "01b_rotacion_plano", "01c_rotaciones_3d", "02_producto_interno"]
animaciones: []
ejercicios_sugeridos: ["Rotar $3+i$ noventa grados con el complejo y con la matriz, y comprobar que $R^TR=Id$ y $\\det R=1$", "Comparar $R_xR_yR_z$ con $R_zR_yR_x$ para ángulos de 1, 0,1 y 0,01 rad", "Aproximar la rotación de 120 grados alrededor de $(1,1,1)$ repitiendo pasos chicos, y verificar con `scipy.linalg.logm` que la norma del vector eje es el ángulo"]
---

# Capítulo 1: rotaciones, de los complejos a la exponencial

Una rotación es la transformación que fija un punto y conserva distancias, ángulos y orientación; se escribe con complejos, con matrices ortogonales y, en lo pequeño, con la exponencial.

## Qué se estudia

- Rotación con y sin centro en el origen, y su escritura con números complejos y con matrices 2x2
- Producto interno y matrices ortogonales: qué significa conservar distancias y ángulos
- Rotaciones en el espacio: R_x, R_y, R_z y el orden de composición
- Rotaciones infinitesimales: Id + P con P antisimétrica
- Exponencial de matrices y logaritmo: la rotación como repetición de pasos chicos

### Rotación

Álgebra: $x' = c + R(\theta)(x-c)$, con $R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta\\ \sin\theta & \cos\theta\end{pmatrix}$. Se ve: un punto quieto (el centro), los demás recorren circunferencias concéntricas; se conservan distancias, ángulos y orientación. Es lineal sólo si $c=0$. Escalera: en $\mathbb R$ no hay rotación (lo único ortogonal es $\pm1$: identidad o reflexión); en $\mathbb R^2$ un ángulo y todas conmutan; en $\mathbb R^3$ hace falta además un eje, tres parámetros, y dejan de conmutar; en $\mathbb R^n$ se rota en planos, $n(n-1)/2$ parámetros.

### Números complejos como transformaciones del plano

Álgebra: $(a+ib)(x+iy) = (ax-by) + i(bx+ay)$, o sea la matriz $\begin{pmatrix}a&-b\\b&a\end{pmatrix}$. Se ve: multiplicar por un complejo es rotar y estirar a la vez (dos números libres), frente a los cuatro de una $2\times2$ cualquiera que además puede cizallar o aplastar. Los puntos del plano son números: los vectores son puntos.

### Fórmula de Euler

Álgebra: $e^{i\theta} = \cos\theta + i\sin\theta$, y $\frac{d}{d\theta}e^{i\theta} = i\,e^{i\theta}$. Se ve: $z\,e^{i\theta}$ es $z$ girado $\theta$; la derivada respecto del ángulo es el mismo punto girado un cuarto de vuelta, es decir, el vector tangente a la circunferencia. Multiplicar por $i$ es la "derivada de la rotación".

### Producto interno

Álgebra: $\langle Av, Au\rangle = \langle v,u\rangle$ para todo par. Se ve: la regla y el transportador dan lo mismo antes y después; conservar el producto interno es conservar longitudes y ángulos de una vez. No hay base privilegiada salvo por el producto interno: la canónica es especial sólo porque en ella la cuenta $\sum x_iy_i$ mide.

### Matriz ortogonal

Álgebra: $A^TA = Id$; las columnas son perpendiculares y de longitud 1. Se ve: la grilla cuadrada sigue siendo cuadrada, pero puede haberse dado vuelta como en un espejo. $\det A = +1$ dice "sin espejo" (rotación), $\det A = -1$ dice reflexión. Escalera: en $\mathbb R$, $a^2=1$; en $\mathbb R^2$ dos familias ($R(\theta)$ y las reflexiones); en $\mathbb R^3$ idem más las rotorreflexiones.

### Rotaciones en tres dimensiones

Álgebra: $R_x(\alpha), R_y(\beta), R_z(\gamma)$, cada una "la rotación 2D empotrada en 3D, con un 1 en la diagonal para el eje que queda quieto":
$$R_x(\alpha) = \begin{pmatrix}1&0&0\\0&\cos\alpha&-\sin\alpha\\0&\sin\alpha&\cos\alpha\end{pmatrix},\quad R_y(\alpha) = \begin{pmatrix}\cos\alpha&0&\sin\alpha\\0&1&0\\-\sin\alpha&0&\cos\alpha\end{pmatrix},\quad R_z(\alpha) = \begin{pmatrix}\cos\alpha&-\sin\alpha&0\\\sin\alpha&\cos\alpha&0\\0&0&1\end{pmatrix}.$$
Las columnas son las imágenes de $e_x, e_y, e_z$. Se ve: toda rotación de $\mathbb R^3$ deja fija una recta (el eje, que más adelante será el autovector de autovalor 1) y gira el plano perpendicular; componer básicas en distinto orden deja el cuerpo en lugares distintos (los dedos).

### Rotación infinitesimal

Álgebra: $R(\varepsilon) \approx Id + \varepsilon A$ con $A$ antisimétrica ($A^T=-A$); $A_x v = e_x\times v$. Se ve: el arco de circunferencia y su tangente son indistinguibles en un tramo chiquito; $\varepsilon A v$ es el pasito tangente. El orden sólo aparece en $\varepsilon^2$: "a primer orden las rotaciones pequeñas se suman; a segundo orden aparece el orden".

### Exponencial de matrices

Álgebra: $e^A = \sum A^n/n!$; $R(\varphi) = \lim (Id + \tfrac{\varphi}{n}M)^n = e^{\varphi M}$; $\log R$ es antisimétrica y sus tres entradas forman el vector eje cuya norma es el ángulo. Se ve: una rotación grande es muchísimas rotaciones chiquitas iguales (ir a lo chico para volver a lo grande); $e^{t\log R}$, $t\in[0,1]$, es la trayectoria suave de la identidad hasta $R$. Con $M_z$, $M^2 = \mathrm{diag}(-1,-1,0)$, $M^3 = -M$: las potencias impares arman $\sin\varphi$, las pares $1-\cos\varphi$, y sale $R_z(\varphi)$.

## Conceptos previos

- Transformación lineal y matriz 2x2 (CBC)
- Producto interno y módulo de un vector
- Números complejos (secundario)

## En el apunte

- Capítulo 1. Rotaciones: girar es multiplicar
- Apéndice A.1. Construcción geométrica de las matrices de rotación 3D
- Apéndice A.2. Rotaciones infinitesimales y orden de composición
- Sección 0.4. Repaso de álgebra lineal desde la geometría

## Unidades interactivas

- Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia) (`00_fundamentos`)
- Rotaciones I: el punto no se movió (`01a_punto_quieto`)
- Rotaciones II: la rotación en el plano (`01b_rotacion_plano`)
- Rotaciones III: tres ejes y el orden importa (`01c_rotaciones_3d`)
- Producto interno: proyección, longitud, ángulo (`02_producto_interno`)

## Ejercicios sugeridos

- Rotar $3+i$ noventa grados con el complejo y con la matriz, y comprobar que $R^TR=Id$ y $\det R=1$
- Comparar $R_xR_yR_z$ con $R_zR_yR_x$ para ángulos de 1, 0,1 y 0,01 rad
- Aproximar la rotación de 120 grados alrededor de $(1,1,1)$ repitiendo pasos chicos, y verificar con `scipy.linalg.logm` que la norma del vector eje es el ángulo
