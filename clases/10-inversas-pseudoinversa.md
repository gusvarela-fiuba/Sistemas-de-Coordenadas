---
clase: "10"
titulo: Inversas — respecto de una operación, los cuatro subespacios y la pseudoinversa
fecha_2025: null
fechas_2026: []
estado: no-dictada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-10
  - fuentes/transcripciones/2026-09-30.md
  - fuentes/transcripciones/2026-10-14.md
conceptos: [inversa, cuatro-subespacios, pseudoinversa, sistema-sobredeterminado]
apunte: ["02", "inversas"]
unidad: 09_cambio_de_base_svd
---

# Clase 10 — Inversas

> **Estado:** no dictada todavía en 2C2026. Reconstruida sin transcripción a partir del resumen 2025, el apunte y los anuncios del 2026-10-14 (SVD aplicada a regresión y ajuste de puntos, que es donde entra la pseudoinversa).

## El hilo del profesor (cursada 2025)

"En esta clase trabajamos con el concepto de inversa. Si bien lo aplicamos a las transformaciones lineales tratamos de encararlo en forma más general" *(profesor, resumen 2025)*. Cuatro bloques:

**Autovectores vs. vectores singulares.** A partir de la exploración en marimo de la clase 8, la pregunta: "¿coincide para una misma transformación en $\mathbb R^2$ un autovector con algún vector singular?". El profesor admite que "dije algo que estaba mal o era confuso" y corrige: "si en $\mathbb R^2$ un autovector es también un vector singular, entonces la dirección normal a la de ese vector también es un autovector y un vector singular. Esto se deduce de la ortogonalidad de los vectores singulares tanto a la salida como a la entrada. En conclusión: las matrices simétricas no son 'un caso' de coincidencia sino que (al menos en $\mathbb R^2$) son 'El caso', y por tanto cuando coincide un vector coinciden todos. Es pertinente preguntarse: ¿es así en $\mathbb R^3$?" *(profesor, resumen 2025)*.

**Invertir con las descomposiciones.**
$$A=C^{-1}_{e\mapsto av}\,\Lambda\,C_{e\mapsto av}\ \Rightarrow\ A^{-1}=C^{-1}_{e\mapsto av}\,\tfrac{1}{\Lambda}\,C_{e\mapsto av},\qquad A=U\Sigma V^{T}\ \Rightarrow\ A^{-1}=V\,\tfrac1\Sigma\,U^{T}.$$
"Hago énfasis en escribir $1/\Lambda$ o $1/\Sigma$ para reforzar el hecho de que invertir una matriz diagonal es tomar los recíprocos de las entradas. Lo cual nos lleva a preguntarnos ¿por qué llamamos inversas a cosas tan distintas como el recíproco multiplicativo o la inversa de una TL?"

**¿Qué es una inversa?** Vuelta "a algo que hablamos muuuuy al principio de la cursada: la relación entre operaciones, elementos y transformaciones". La inversa es siempre "respecto de...": "un elemento de un conjunto que, al operar con otro resulta en el elemento neutro respecto de esa operación". La lista del profesor: enteros con la suma (neutro 0), racionales/reales con el producto (neutro 1), funciones con la composición (neutro $f(x)=x$), TL con la composición (neutro $A(\vec x)=\vec x$), matrices con el producto (neutro $Id$). Consecuencia: "una transformación lineal que pierda dimensiones puede tener una inversa. ¿Qué implicancias tiene esto al resolver un sistema de ecuaciones [...]? ¿Es única esa inversa? ¿Existe algo similar para transformaciones que 'ganen' dimensiones?"

**Los subespacios relevantes y la pseudoinversa.** "El núcleo (vectores de la entrada que caen al 0); el rango o co-dominio o imagen (espacio de vectores de salida posible); la co-imagen, rango de entrada o podríamos llamar contra-núcleo (vectores de la entrada que no van al 0); el espacio inaccesible de la salida (la llamaría contra-imagen), los vectores que forman parte del espacio dentro del cual está incrustada la imagen pero no son parte de la imagen" *(profesor, resumen 2025)*. Con eso, "encontramos la forma de resolver un sistema de ecuaciones sobre-determinado y encontrar el punto de la entrada que corresponde en la salida a lo más cercano al término independiente del sistema de ecuaciones. Esto es algo que mencionamos como pseudo-inversa de Moore-Penrose". Cierre: punteo de lo que se construye con la pseudoinversa, adelanto de los cuatro problemas de la clase 11.

## Lo que pasó en 2C2026

No se dictó. **Reconstruida sin transcripción.** Lo que se infiere:

- Ya se usó la inversa de una matriz $2\times2$ sin discutirla: el 2026-09-30 el profesor calculó $T^{-1}$ "con la matriz de cofactores, la adjunta, dividida por el determinante" y comentó que "más de $4\times4$ conviene Gauss" *(transcripción auto-traducida)*; también recordó el método de "poner la identidad al lado y hacer operaciones por filas" que un alumno traía del CBC. La escalera "inversa respecto de una operación" no se dio.
- Los cuatro subespacios aparecieron de costado el 2026-10-14: las columnas de la jacobiana "generan el plano que puedo recorrer a la salida" y "el espacio que no puedo recorrer" es la normal (eso es imagen y contra-imagen de una $3\times2$).
- El 2026-10-14 el profesor anunció que la próxima clase usa la SVD "para resolver problemas: regresión, ajuste de puntos" *(transcripción auto-traducida)*. La pseudoinversa es el puente, así que es probable que inversas y clase 11 se den juntas.

Falta confirmar: fecha; si el bloque filosófico "inversa respecto de una operación" se da o se da por sabido; si el profesor retoma la pregunta "¿coinciden autovectores y vectores singulares en $\mathbb R^3$?".

## Hecho geométrico

**Escalera obligatoria de la inversa.**
- En $\mathbb R$: $x\mapsto ax$ se deshace con $x\mapsto x/a$. El neutro es $1$, la inversa es $1/a$. **No existe si $a=0$**: todo se aplastó al cero y no hay forma de saber de dónde vino cada punto.
- En $\mathbb R^2$: $A$ se deshace con $A^{-1}$; neutro $I$. $A^{-1}A=I$ significa "ir y volver no mueve nada". **No existe si $\det A=0$**: el cuadrado unidad se aplastó a un segmento (área cero), una dirección entera cayó a un punto (el núcleo, clase 5), y no se puede desplegar lo aplastado.
- En $\mathbb R^3$ y $\mathbb R^n$: igual; $\det=0$ ↔ algún valor singular es cero ↔ la elipse (elipsoide) perdió un semieje.
- Más allá: cuando no hay inversa, o cuando la matriz ni siquiera es cuadrada, se pregunta "¿qué es lo más parecido a deshacer?". Esa es la pseudoinversa.

**Inversa respecto de una operación.** Álgebra: $x\circ x^{-1}=e$. Se ve: deshacer el movimiento. Sumar 3 se deshace restando 3; rotar 30° se deshace rotando $-30°$ (clase 1: $R(\theta)^{-1}=R(-\theta)=R(\theta)^{T}$); reflejar se deshace reflejando de nuevo (es su propia inversa); escalar por 2 se deshace escalando por $\tfrac12$. En base de autovectores, invertir es tomar recíprocos en la diagonal: deshacer cada estiramiento por separado. En SVD, $A^{-1}=V\,(1/\Sigma)\,U^{T}$: desgirar lo último, desestirar, desgirar lo primero. Las tres cosas que la SVD descompone se deshacen en orden inverso.

**Los cuatro subespacios** (nombres del profesor). Una matriz $m\times n$ parte la entrada $\mathbb R^n$ en dos pedazos perpendiculares y la salida $\mathbb R^m$ en otros dos:
- Núcleo: lo que entra y cae al $0$. Se ve: la dirección aplastada.
- Co-imagen (contra-núcleo): lo que entra y no cae al $0$; perpendicular al núcleo. Se ve: las direcciones que sí se distinguen a la salida.
- Imagen: lo alcanzable a la salida. Se ve: el plano (recta) donde cae todo.
- Contra-imagen (espacio inaccesible): lo perpendicular a la imagen. Se ve: adonde no llega nada.
Restringida de co-imagen a imagen, la transformación sí se invierte: ahí no se aplastó nada. En SVD: los $v_i$ con $\sigma_i>0$ generan la co-imagen, los $v_i$ con $\sigma_i=0$ el núcleo, los $u_i$ con $\sigma_i>0$ la imagen, los $u_i$ sobrantes la contra-imagen. Escalera: para la jacobiana $3\times2$ de la clase 9, co-imagen = todo el plano $(u,v)$, imagen = plano tangente, contra-imagen = la normal, núcleo = $\{0\}$ (salvo en el polo, donde $r_\lambda=0$ y aparece núcleo).

**Pseudoinversa.** Álgebra: $A^{+}=V\,\Sigma^{+}U^{T}$ con $\Sigma^{+}$ = recíprocos de los $\sigma_i\neq0$ y ceros donde había ceros. Se ve: proyectar el término independiente sobre la imagen (descartar la parte en la contra-imagen, que no se puede alcanzar) y deshacer sólo la parte invertible; si había núcleo, elegir la solución de norma mínima (no inventar nada en la dirección aplastada). En $\mathbb R$: la pseudoinversa de $a=0$ es $0$.

**Sistema sobredeterminado.** Álgebra: $Ax=b$ con más ecuaciones que incógnitas; $b$ en general no está en la imagen; la solución de mínimos cuadrados es $x=A^{+}b$, equivalente a las ecuaciones normales $A^{T}Ax=A^{T}b$. Se ve: tres puntos no alineados no admiten recta; se elige la recta cuyo vector de residuos es perpendicular a la imagen (a las columnas de $A$). "El punto de la entrada que corresponde en la salida a lo más cercano al término independiente."

## Cuentas chicas

**Ajuste de una recta a $(0,0)$, $(1,1)$, $(2,3)$ por ecuaciones normales.** Buscamos $y=a+bx$. Las tres ecuaciones que no se pueden cumplir a la vez:
$$\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix}\begin{pmatrix}a\\b\end{pmatrix}=\begin{pmatrix}0\\1\\3\end{pmatrix},\qquad A=\begin{pmatrix}1&0\\1&1\\1&2\end{pmatrix},\ b=\begin{pmatrix}0\\1\\3\end{pmatrix}.$$
Los tres puntos no están alineados (pendientes $1$ y $2$), así que $b$ no está en la imagen de $A$ (que es un plano dentro de $\mathbb R^3$). Ecuaciones normales:
$$A^{T}A=\begin{pmatrix}3&3\\3&5\end{pmatrix},\qquad A^{T}b=\begin{pmatrix}0+1+3\\0+1+6\end{pmatrix}=\begin{pmatrix}4\\7\end{pmatrix}.$$
$3a+3b=4$ y $3a+5b=7$; restando, $2b=3$, $b=\tfrac32$; entonces $3a=4-\tfrac92=-\tfrac12$, $a=-\tfrac16$. La recta: $y=-\tfrac16+\tfrac32x$.

Residuos: $b-A\hat x=(0,1,3)-(-\tfrac16,\ \tfrac43,\ \tfrac{17}6)=(\tfrac16,\ -\tfrac13,\ \tfrac16)$. Chequeo geométrico: el residuo es perpendicular a las dos columnas de $A$: $\tfrac16-\tfrac13+\tfrac16=0$ y $0\cdot\tfrac16+1\cdot(-\tfrac13)+2\cdot\tfrac16=0$. El residuo vive en la contra-imagen; $A\hat x$ es la proyección de $b$ sobre la imagen. Verificado con `np.linalg.lstsq(A, b)` y `np.linalg.pinv(A) @ b`: $(-0{,}1667,\ 1{,}5)$.

Lo mismo con la pseudoinversa explícita: $A^{+}=(A^{T}A)^{-1}A^{T}=\tfrac16\begin{pmatrix}5&-3\\-3&3\end{pmatrix}\begin{pmatrix}1&1&1\\0&1&2\end{pmatrix}=\tfrac16\begin{pmatrix}5&2&-1\\-3&0&3\end{pmatrix}$, y $A^{+}b=\tfrac16(0+2-3,\ 0+0+9)=(-\tfrac16,\ \tfrac32)$.

**Inversa por la diagonal.** $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}=P\,\mathrm{diag}(3,1)\,P^{-1}$ (clase 8). $A^{-1}=P\,\mathrm{diag}(\tfrac13,1)\,P^{-1}=\tfrac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}\tfrac13&0\\0&1\end{pmatrix}\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\tfrac13\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$. Chequeo: $AA^{-1}=\tfrac13\begin{pmatrix}3&0\\0&3\end{pmatrix}=I$. Y por adjunta: $\det A=3$, adjunta $\begin{pmatrix}2&-1\\-1&2\end{pmatrix}$, mismo resultado.

**Sin inversa.** $B=\begin{pmatrix}1&1\\1&1\end{pmatrix}$: $\det=0$, núcleo $(1,-1)$, imagen la recta $(1,1)$. $Bx=(1,0)$ no tiene solución ($(1,0)$ no está en la imagen). Pseudoinversa: $B=U\Sigma V^{T}$ con $\sigma_1=2$, $\sigma_2=0$, $u_1=v_1=\tfrac1{\sqrt2}(1,1)$; $B^{+}=v_1\,\tfrac12\,u_1^{T}=\tfrac14\begin{pmatrix}1&1\\1&1\end{pmatrix}$. $B^{+}(1,0)=(\tfrac14,\tfrac14)$: proyecta $(1,0)$ sobre la recta imagen (da $(\tfrac12,\tfrac12)$), deshace el estiramiento por 2, y no pone nada en la dirección del núcleo.

**Verificación.** En Excel: `ESTIMACION.LINEAL` o `PENDIENTE`/`INTERSECCION.EJE` sobre los tres puntos dan $1{,}5$ y $-0{,}1667$. En GeoGebra: `AjusteLineal({(0,0),(1,1),(2,3)})`. En numpy: `lstsq`, `pinv`, y `np.linalg.svd(A)` para ver $\sigma$ y las cuatro bases.

## Dónde está desarrollado

- **Apunte: cubierto desde la versión 3 (2026-10-17)** en `09-svd.tex`, sección `sec:pseudoinversa`, anticipado y pendiente de validar por la cátedra. Lo que sigue describe el estado anterior: La inversa como concepto y la pseudoinversa no tienen sección propia. Menciones: `02-hilo-de-la-materia.tex` (fila 10: "inversa = deshacer el movimiento; una transformación que pierde dimensiones aplasta y no se deshace del todo; la pseudoinversa elige el punto de la imagen más cercano", marcada "pseudoinversa pendiente"); `06-afines-homogeneas.tex` §La misma idea en cada dimensión (`sec:misma-idea`: la cita de la clase 10 y la fila "Inversa: $1/a$, no existe si $a=0$ / $A^{-1}$, no existe si $\det A=0$ / deshacer el movimiento"); `09-svd.tex` §Sistemas de ecuaciones (`sec:sistemas-ecuaciones`: "ajustar coordenadas a partir de observaciones redundantes", bloque "a precisar con los enunciados de la cátedra"); `08-algebra-transformaciones.tex` §Núcleo (`sec:nucleo`) para el subespacio que impide invertir. Tabla de propuesta en `19-apendice-rubricas.tex` (última fila: recíprocos, inversa respecto de una operación, Moore-Penrose como proyección sobre la imagen).
- **Unidad marimo:** `unidades/09_cambio_de_base_svd.py` (lección **anticipada**, 2026-10-17: $A^{-1} = V\,(1/\Sigma)\,U^{T}$, pseudoinversa de $\begin{pmatrix}1&2\\2&4\end{pmatrix}$ a mano y con `pinv`, los cuatro subespacios de la $3\times2$ del ajuste $(0,0),(1,1),(2,y_3)$ con el residuo sobre $u_3$; pendiente de validar por la cátedra).
- **Bibliografía del campus:** Noble & Daniel, *Álgebra Lineal Aplicada* (sólo parte 1); Strang; Calvetti & Somersalo (ver ficha 07); Lay ("los primeros dos capítulos sirven como introducción, bastante enfocada a resolver operaciones"). Sin comentario textual del profesor sobre inversas o pseudoinversa en la lista del campus.
- **Material del profesor:** ninguno específico; la exploración marimo de la clase 8 (2025) es el antecedente.

## Enlaces del mapa

- Viene de: `composicion` (clase 2: la inversa es respecto de la composición), `determinante` y `nucleo` (clase 5: $\det=0$ ↔ hay núcleo ↔ no hay inversa), `transformacion-afin` (clase 3: resolver un sistema con la inversa de una matriz cuadrada), `diagonalizacion` (clase 8: $1/\Lambda$), `svd` (clase 7: $V\,(1/\Sigma)\,U^{T}$), `matriz-ortogonal` (clase 1: $U^{-1}=U^{T}$), `jacobiano` (clase 9: imagen y normal de una $3\times2$).
- Lleva a: `regresion-simple`, `interseccion-de-circulos`, `procrustes`, `regresion-total` (clase 11: los cuatro problemas se resuelven con pseudoinversa o SVD), la meta GPS anunciada el 2026-09-30.
- Qué se conserva: el neutro. La pregunta del profesor es "¿a qué llamamos inversa cuando estamos sumando, multiplicando, componiendo?", y la respuesta es siempre "lo que compuesto con el otro da el elemento que no hace nada".

## Huecos y dudas

- Sin fecha 2025 ni 2026. Posible que se funda con la clase 11.
- La pregunta abierta del profesor: ¿en $\mathbb R^3$, si un autovector coincide con un vector singular, coinciden todos? (Pista para pensar: si $v_1$ es autovector y vector singular, el plano perpendicular queda invariante y en él se repite la pregunta de $\mathbb R^2$.) No está resuelta en las fuentes.
- La fórmula $A=C^{-1}_{e\mapsto av}\Lambda\,C_{e\mapsto av}$ del resumen usa $C_{e\mapsto av}$ actuando primero sobre un vector en canónica, que es la convención de la clase 7, no la de la clase 8. Misma duda de notación que en la ficha 08.
- El "punteo rápido de las distintas cosas que podemos construir a partir de la pseudoinversa" no está detallado en el resumen; se supone que son los cuatro problemas de la clase 11.
- "Inversa de una transformación que gana dimensiones" (la $3\times2$): el resumen lo deja como pregunta; la respuesta es la pseudoinversa por la izquierda, $(A^{T}A)^{-1}A^{T}$, que es la que se usa en el ajuste de recta. Confirmar que el profesor la presenta así.
- El apunte deja §Sistemas de ecuaciones "a precisar con los enunciados de la cátedra"; esta ficha aporta el único ejemplo numérico hasta que haya guía.
