---
clase: 3
titulo: "Capítulos 3 y 4: reflexiones, similaridades y afinidades"
idea: "Las reflexiones generan las isometrías; con homotecias dan las similaridades, y las afinidades $x\\mapsto Ax+t$ caben en una matriz $3\\times3$ con coordenadas homogéneas."
que_se_estudia: ["Reflexión por un punto y por una recta; composición de dos reflexiones", "Afinidad axial y similaridad; punto fijo de una similaridad", "Transformación afín $F(x)=Ax+t$ y su determinación por tres puntos", "Coordenadas homogéneas: la traslación entra en la matriz", "Punto fijo y traslación como límite con centro en el infinito"]
conceptos_previos: ["Rotaciones y matrices ortogonales (capítulo 1)", "Composición y conmutatividad (capítulo 2)", "Homotecia (capítulo 2)"]
apunte: ["reflexiones", "afines", "composicion-afin", "traslaciones"]
unidades: ["03_reflexiones_similaridades", "04_afines_homogeneas"]
animaciones: ["02_homogeneas_pentagono_3d"]
ejercicios_sugeridos: ["Componer tres reflexiones puntuales y reconocer el resultado", "Mostrar que dos reflexiones en rectas secantes son una rotación del doble del ángulo entre ellas", "Hallar la afinidad que lleva un triángulo en otro y su punto fijo si lo tiene", "Escribir en homogéneas la composición de una rotación y una traslación"]
---

# Capítulos 3 y 4: reflexiones, similaridades y afinidades

Las reflexiones generan las isometrías; con homotecias dan las similaridades, y las afinidades $x\mapsto Ax+t$ caben en una matriz $3\times3$ con coordenadas homogéneas.

## Qué se estudia

- Reflexión por un punto y por una recta; composición de dos reflexiones
- Afinidad axial y similaridad; punto fijo de una similaridad
- Transformación afín $F(x)=Ax+t$ y su determinación por tres puntos
- Coordenadas homogéneas: la traslación entra en la matriz
- Punto fijo y traslación como límite con centro en el infinito

### Reflexión (por un punto, por una recta)

Álgebra: por un punto, $\rho_b(x) = 2b - x$; por una recta con normal $n$ y ecuación $n\cdot x = c$, $\varphi_B(x) = x - 2\frac{n\cdot x - c}{\|n\|^2}n$; matriz ortogonal con $\det = -1$. Se ve: el espejo. Aplicada dos veces, nada (involución). Dos espejos seguidos devuelven la orientación: puntuales dan traslación $x + 2(a-b)$; ejes paralelos, traslación perpendicular de longitud $2h$; ejes secantes en $o$ con ángulo $\theta$, rotación $R_{o,2\theta}$. Las reflexiones son los átomos: con ellas se arma toda isometría. Escalera: en $\mathbb R$, $x\mapsto 2b - x$ es la única reflexión; en $\mathbb R^2$ hay por punto y por recta; en $\mathbb R^3$, por plano.

### Afinidad axial (eje, dirección y factor)

Álgebra: eje $e$, dirección $\vec d$ no paralela al eje, factor $f$: $X\mapsto X_0 + f(X - X_0)$ con $X_0$ el corte de la paralela a $\vec d$ por $X$ con el eje; en matrices $B\,\mathrm{diag}(1,f)\,B^{-1}$ con $B = (\vec u\ \vec d)$, $\det = f$. Se ve: una faja que se estira (o se da vuelta, $f<0$) desde una recta fija, cada punto deslizando por su paralela a $\vec d$. $f=-1$ con $\vec d\perp e$ es la reflexión ortogonal; $f=-1$ oblicua es la reflexión oblicua. Tres de estas, con el eje por los dos vértices que quedan quietos, llevan cualquier triángulo sobre cualquier otro; el producto de los factores es el cociente de áreas.

### Similaridad

Álgebra: $S(x) = o + \lambda R(x-o)$, o $S = \varphi_A\varphi_B\eta_o^\lambda$. Se ve: misma forma, otro tamaño y otra orientación; conserva ángulos y razones entre distancias. El centro $o$ es el único punto fijo (si $\lambda\neq1$ o el giro no es nulo); se halla con dos círculos de Apolonio o resolviendo $(I - \lambda R)o = a' - \lambda R a$. Es la composición rotación-alrededor-de-$c$ y escala-alrededor-de-$d$ del ejercicio: la parte lineal $kR$ gira y achica, y el punto fijo de la composición no es ni $c$ ni $d$.

### Transformación afín

Álgebra: $F(x) = Ax + t$, $\det A\neq0$; seis números. Se ve: paralelogramo va a paralelogramo, cuadrado a paralelogramo, círculo a elipse; las proporciones sobre cada recta se conservan. Por eso la imagen de un triángulo la determina del todo: todo punto es $A + \lambda\overrightarrow{AB} + \mu\overrightarrow{AC}$ y tiene que ir a $A' + \lambda\overrightarrow{A'B'} + \mu\overrightarrow{A'C'}$. Las preguntas que se le hacen a $A$ y $t$: ¿invertible? ($\det A$), ¿conserva orientación? (signo), ¿puntos fijos? ($(I-A)x = t$), ¿direcciones invariantes? (autovectores), ¿cómo cambia áreas? ($|\det A|$).

### Coordenadas homogéneas

Álgebra: $(x,y)\leftrightarrow(x,y,1)$, y la afinidad es $\begin{pmatrix}a&b&e\\c&d&f\\0&0&1\end{pmatrix}$; componer afinidades es multiplicar $3\times3$, la traslación entra en la matriz. Se ve: el plano es el plano $z=1$ de $\mathbb R^3$ y cada punto es la recta por el origen que lo atraviesa; $(x,y,1)\sim\lambda(x,y,1)$. Un vector con tercera coordenada 0 es una dirección, un punto impropio: las rectas paralelas lo comparten. Escalera: la recta afín es $z=1$ en $\mathbb R^2$; el plano afín, $z=1$ en $\mathbb R^3$; $\mathbb R^n$ afín, $w=1$ en $\mathbb R^{n+1}$.

### Punto fijo

Álgebra: $F(x_*) = x_*$, es decir $(I - A)x_* = t$; en homogéneas, autovector de $H$ con $\lambda = 1$ y $w\neq0$. Se ve: el lugar alrededor del cual la transformación "gira": rotar y trasladar repetidamente dibuja círculos alrededor del punto fijo; una rotación con centro fuera del origen tiene centro $c$ con $t = (I-R)c$; una traslación no tiene (el sistema es incompatible, el autovector de $\lambda=1$ tiene $w=0$: el punto fijo "se fue al infinito"). Si hay punto fijo, poniendo el origen ahí la afinidad queda lineal. Una rotación de $\mathbb R^3$ tiene autovalor 1 porque el polinomio característico es de grado impar y los autovalores tienen módulo 1.

### Traslación

Álgebra: $A = I$, $F(x) = x + v$. Se ve: todo se desplaza igual; es la única afinidad sin punto fijo propio (y conmuta con las demás traslaciones, no con rotaciones: $T_vQ_c \neq Q_cT_v$, mismo giro, centros distintos). Nace de dos reflexiones (puntuales o en ejes paralelos) y es el límite de rotaciones cuyo centro se va al infinito. En homogéneas su punto fijo es impropio: la dirección $v$.

## Conceptos previos

- Rotaciones y matrices ortogonales (capítulo 1)
- Composición y conmutatividad (capítulo 2)
- Homotecia (capítulo 2)

## En el apunte

- Capítulo 3. Reflexiones, isometrías y similaridades
- Capítulo 4. Afinidades y coordenadas homogéneas
- Apéndice A.3. Composición afín práctica: rotación y escala
- Capítulo 2. Traslaciones y movimientos rígidos

## Unidades interactivas

- Reflexiones y similaridades (`03_reflexiones_similaridades`)
- Afinidades y coordenadas homogéneas (`04_afines_homogeneas`)

## Animaciones

- `02_homogeneas_pentagono_3d`

## Ejercicios sugeridos

- Componer tres reflexiones puntuales y reconocer el resultado
- Mostrar que dos reflexiones en rectas secantes son una rotación del doble del ángulo entre ellas
- Hallar la afinidad que lleva un triángulo en otro y su punto fijo si lo tiene
- Escribir en homogéneas la composición de una rotación y una traslación
