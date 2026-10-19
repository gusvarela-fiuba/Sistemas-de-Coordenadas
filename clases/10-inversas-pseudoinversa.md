---
clase: 10
titulo: "Clase 10: inversas, cuatro subespacios y pseudoinversa"
idea: "Invertir es deshacer el movimiento; cuando la transformación aplasta una dirección no hay inversa, y la pseudoinversa deshace lo que se puede."
que_se_estudia: ["Inversa respecto de una operación, de $\\mathbb R$ a $\\mathbb R^n$", "Núcleo, co-imagen, imagen y contra-imagen", "Pseudoinversa $A^+=V\\Sigma^+U^T$", "Sistemas sobredeterminados y mínimos cuadrados"]
conceptos_previos: ["Composición (clase 2)", "Determinante y núcleo (clase 5)", "Diagonalización (clase 8)", "SVD (clase 7)"]
apunte: ["inversas"]
unidades: ["09_cambio_de_base_svd"]
animaciones: []
ejercicios_sugeridos: ["Ajustar una recta a $(0,0)$, $(1,1)$, $(2,3)$ con las ecuaciones normales y comprobar que el residuo es perpendicular a las columnas", "Invertir $\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$ por la diagonal y por la adjunta", "Calcular la pseudoinversa de $\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}$ y resolver $Bx=(1,0)$ en mínimos cuadrados"]
---

# Clase 10: inversas, cuatro subespacios y pseudoinversa

Invertir es deshacer el movimiento; cuando la transformación aplasta una dirección no hay inversa, y la pseudoinversa deshace lo que se puede.

## Qué se estudia

- Inversa respecto de una operación, de $\mathbb R$ a $\mathbb R^n$
- Núcleo, co-imagen, imagen y contra-imagen
- Pseudoinversa $A^+=V\Sigma^+U^T$
- Sistemas sobredeterminados y mínimos cuadrados

**Escalera obligatoria de la inversa.**
- En $\mathbb R$: $x\mapsto ax$ se deshace con $x\mapsto x/a$. El neutro es $1$, la inversa es $1/a$. **No existe si $a=0$**: todo se aplastó al cero y no hay forma de saber de dónde vino cada punto.
- En $\mathbb R^2$: $A$ se deshace con $A^{-1}$; neutro $I$. $A^{-1}A=I$ significa ir y volver no mueve nada. **No existe si $\det A=0$**: el cuadrado unidad se aplastó a un segmento (área cero), una dirección entera cayó a un punto (el núcleo, clase 5), y no se puede desplegar lo aplastado.
- En $\mathbb R^3$ y $\mathbb R^n$: igual; $\det=0$ ↔ algún valor singular es cero ↔ la elipse (elipsoide) perdió un semieje.
- Más allá: cuando no hay inversa, o cuando la matriz ni siquiera es cuadrada, se pregunta "¿qué es lo más parecido a deshacer?". Esa es la pseudoinversa.

**Inversa respecto de una operación.** Álgebra: $x\circ x^{-1}=e$. Se ve: deshacer el movimiento. Sumar 3 se deshace restando 3; rotar 30° se deshace rotando $-30°$ (clase 1: $R(\theta)^{-1}=R(-\theta)=R(\theta)^{T}$); reflejar se deshace reflejando de nuevo (es su propia inversa); escalar por 2 se deshace escalando por $\tfrac12$. En base de autovectores, invertir es tomar recíprocos en la diagonal: deshacer cada estiramiento por separado. En SVD, $A^{-1}=V\,(1/\Sigma)\,U^{T}$: desgirar lo último, desestirar, desgirar lo primero. Las tres cosas que la SVD descompone se deshacen en orden inverso.

**Los cuatro subespacios** . Una matriz $m\times n$ parte la entrada $\mathbb R^n$ en dos pedazos perpendiculares y la salida $\mathbb R^m$ en otros dos:
- Núcleo: lo que entra y cae al $0$. Se ve: la dirección aplastada.
- Co-imagen (contra-núcleo): lo que entra y no cae al $0$; perpendicular al núcleo. Se ve: las direcciones que sí se distinguen a la salida.
- Imagen: lo alcanzable a la salida. Se ve: el plano (recta) donde cae todo.
- Contra-imagen (espacio inaccesible): lo perpendicular a la imagen. Se ve: adonde no llega nada.
Restringida de co-imagen a imagen, la transformación sí se invierte: ahí no se aplastó nada. En SVD: los $v_i$ con $\sigma_i>0$ generan la co-imagen, los $v_i$ con $\sigma_i=0$ el núcleo, los $u_i$ con $\sigma_i>0$ la imagen, los $u_i$ sobrantes la contra-imagen. Escalera: para la jacobiana $3\times2$ de la clase 9, co-imagen = todo el plano $(u,v)$, imagen = plano tangente, contra-imagen = la normal, núcleo = $\{0\}$ (salvo en el polo, donde $r_\lambda=0$ y aparece núcleo).

**Pseudoinversa.** Álgebra: $A^{+}=V\,\Sigma^{+}U^{T}$ con $\Sigma^{+}$ = recíprocos de los $\sigma_i\neq0$ y ceros donde había ceros. Se ve: proyectar el término independiente sobre la imagen (descartar la parte en la contra-imagen, que no se puede alcanzar) y deshacer sólo la parte invertible; si había núcleo, elegir la solución de norma mínima (no inventar nada en la dirección aplastada). En $\mathbb R$: la pseudoinversa de $a=0$ es $0$.

**Sistema sobredeterminado.** Álgebra: $Ax=b$ con más ecuaciones que incógnitas; $b$ en general no está en la imagen; la solución de mínimos cuadrados es $x=A^{+}b$, equivalente a las ecuaciones normales $A^{T}Ax=A^{T}b$. Se ve: tres puntos no alineados no admiten recta; se elige la recta cuyo vector de residuos es perpendicular a la imagen (a las columnas de $A$). El punto de la entrada que corresponde en la salida a lo más cercano al término independiente."

## Conceptos previos

- Composición (clase 2)
- Determinante y núcleo (clase 5)
- Diagonalización (clase 8)
- SVD (clase 7)

## En el apunte

- Capítulo 11. Inversas y pseudoinversa: los cuatro subespacios

## Unidades interactivas

- Cambio de base, SVD e inversas (`09_cambio_de_base_svd`)

## Ejercicios sugeridos

- Ajustar una recta a $(0,0)$, $(1,1)$, $(2,3)$ con las ecuaciones normales y comprobar que el residuo es perpendicular a las columnas
- Invertir $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ por la diagonal y por la adjunta
- Calcular la pseudoinversa de $\begin{pmatrix}1&1\\1&1\end{pmatrix}$ y resolver $Bx=(1,0)$ en mínimos cuadrados
