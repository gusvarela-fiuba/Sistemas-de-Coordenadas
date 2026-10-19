---
clase: "07"
titulo: Transformaciones lineales II — subespacios y la SVD
fecha_2025: null
fechas_2026: ["2026-10-07"]
estado: reconstruida
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-7
  - fuentes/transcripciones/2026-09-30.md
  - fuentes/transcripciones/2026-10-14.md
  - datos/dem_copernicus/README.md
  - fuentes/campus/profesor/LaSVD.wxmx
conceptos: [svd, valores-singulares, base-privilegiada]
apunte: ["02", "svd"]
unidad: 09_cambio_de_base_svd
---

# Clase 7 — Transformaciones lineales II: subespacios y la SVD

> **Estado:** no dictada todavía en 2C2026. Anunciada dos veces (2026-09-30 y 2026-10-14) como la clase que viene después de formas cuadráticas. Esta ficha reconstruye el hilo desde el resumen 2025 y los anuncios del profesor; no hay ejercicios numéricos de la cátedra para esta clase.

## El hilo del profesor (cursada 2025)

La clase partió "del conocimiento que teníamos sobre subespacios para intentar encontrar formas de reescribir (factorizar) la matriz de una transformación lineal de tal forma que nos dé información útil" *(profesor, resumen 2025)*. El orden fue:

1. Un ejercicio traído por los alumnos: una transformación de un vector a un real, no lineal, pero que conserve el producto por escalar. La conclusión fue que "la restricción que se nos ponía era como una restricción independiente para cada sub-espacio posible de dimensión uno en la entrada" *(profesor, resumen 2025)*. De paso, estrategias para resolver problemas: Polya.
2. Autovectores y autovalores. Si la transformación "tiene subespacios unidimensionales invariantes, tantos como dimensión tenga, se puede escribir la matriz en base de autovectores y queda diagonal" *(profesor, resumen 2025)*: $A = B_{av\mapsto e}\cdot D\cdot B_{e\mapsto av}$. Interpretación gráfica: "en cierto sentido se relaciona con aplicar dos afinidades axiales sucesivas".
3. Cómo se hallan: $A\vec v = \lambda\vec v$ se convierte en una transformación modificada que tiene al autovector en el núcleo, y entra "nuestro 'detector de colinealidad': el producto cuña" para armar el polinomio cuyas raíces son los autovalores y después el núcleo que da los autovectores.
4. El problema: "al ser un polinomio el que nos da los autovalores ya nos aparece el problema de las raíces complejas". Entonces, por analogía, "podría existir una forma de descomponer la transformación que no tuviera estos problemas, y vimos que era cuestión de encontrar una 'base privilegiada' de la transformación".
5. El enunciado central, mostrado gráficamente: "siempre existe una base ortogonal del espacio de entrada de una transformación que se conserva ortogonal a la salida (o mejor dicho se asigna al transformar hacia una base ortogonal de la salida)" *(profesor, resumen 2025)*.
6. Consecuencia: "si pudiéramos expresar la matriz en esta base 'mezclada' (distinta para la salida que para la entrada), podríamos tener la matriz en forma diagonal y garantizado que no aparecen números complejos".

Cierre: videos recomendados "fervientemente" (embebidos en el campus, no descargables), un video propio de clase sobre SVD, y dos artículos sobre cómo enseñar transformaciones lineales (Molina & Oktaç; González, Rojas, Roa, Fuentes), porque "el concepto de cambio de base resulta (me resulta) complicado de explicar".

## Lo que pasó en 2C2026

Dictada el miércoles 2026-10-07, junto con la continuación del cambio de base, según el cronograma que el profesor confirmó en el chat del curso el 2026-10-17 ("7/10: Cambio de Base y SVD"). No hay nota de Notion ni transcripción de ese día; esta ficha se reconstruye desde el resumen 2025, el cuaderno `fuentes/campus/profesor/LaSVD.wxmx` (la SVD "con Maxima, analíticamente" que el profesor dijo el 14/10 haber mostrado y mandado por el grupo) y los dos anuncios que la rodean:

- **2026-09-30** ("Upcoming Topics"): la SVD es "una adaptación de eso [la diagonalización] que siempre funciona, no sólo con autovectores reales" *(transcripción auto-traducida)*. Aparecen "dos bases" especiales, relacionadas "con los espacios importantes: el núcleo y la imagen", y "un cambio de base medio raro, rectangular, con una base a la entrada que no sale" *(transcripción auto-traducida)*. Jordan se descartó explícitamente: "es importante para resolver sistemas, pero la interpretación geométrica no es tan importante; para nosotros la interpretación geométrica es todo". La meta declarada: "hay un problema de GPS que se resuelve con álgebra bastante bien y siempre quiero llegar a ese punto".
- **2026-10-14** ("Next Class: Quadratic Forms and SVD Applications"): la próxima clase son formas cuadráticas (hay una nota en el campus que hay que leer antes) y con eso "usar la descomposición en valores singulares para resolver problemas: regresión, ajuste de puntos, etc." *(transcripción auto-traducida)*. Referencias: "está en el Strang, y hay uno en inglés, Calvetti y Somersalo, que para mí es el que lo explica mejor". El profesor dijo que la SVD ya la había mostrado "con Maxima, analíticamente, no gráficamente" y la había mandado por el grupo; la tarea es intentar en GeoGebra "cualquier sistema 2×3 o 3×2" y mandar dudas por el grupo.

Falta confirmar: qué parte de la SVD se dio el 7/10 (sólo la analítica 2×3 del cuaderno, o también círculo → elipse), y si la clase de formas cuadráticas y la de SVD aplicada son una sola o dos. El archivo de Maxima que circuló por el grupo es `fuentes/campus/profesor/LaSVD.wxmx` (mandado por el profesor el 2026-10-17).

## Hecho geométrico

**La pregunta antes que la fórmula.** Diagonalizar pregunta "¿qué direcciones caen sobre sí mismas?". Pero una rotación de 90° no deja ninguna dirección quieta, y el polinomio característico lo dice con raíces complejas. La SVD cambia la pregunta: "¿qué direcciones perpendiculares de la entrada siguen perpendiculares a la salida?". Esa pregunta siempre tiene respuesta real.

**Escalera.**
- En $\mathbb R$: $x\mapsto a x$. "Diagonalizar" es trivial (todo $x$ es autovector). La SVD de un número es $a = (\pm1)\cdot|a|\cdot 1$: un signo a la salida, un estiramiento $|a|$, nada a la entrada. El valor singular es $|a|$; el signo quedó en la "base de salida".
- En $\mathbb R^2$: la circunferencia unidad va a una elipse. Los semiejes de la elipse son $\sigma_1\ge\sigma_2\ge0$ (valores singulares); sus direcciones $u_1,u_2$ son la base ortonormal de salida; las direcciones de la circunferencia que van a parar a esos semiejes, $v_1,v_2$, son la base ortonormal de entrada. $A v_i = \sigma_i u_i$. Hecho central: **circunferencia → elipse, con bases ortonormales a ambos lados.**
- En $\mathbb R^3$: esfera → elipsoide, tres semiejes. Si la matriz es $3\times2$ (como la jacobiana de una superficie parametrizada, clase 9), la circunferencia del plano $(u,v)$ va a una elipse que vive en el plano tangente dentro de $\mathbb R^3$; el tercer vector $u_3$ apunta a la dirección "inaccesible" (la normal). Ese es el "cambio de base rectangular" del anuncio: $U$ es $3\times3$, $V$ es $2\times2$, $\Sigma$ es $3\times2$.
- En $\mathbb R^n$: una matriz $512\times512$ es una transformación de $\mathbb R^{512}$, y sus 512 valores singulares ordenados dicen cuánta "forma" hay en cada dirección principal. Quedarse con los $k$ primeros es la mejor aproximación de rango $k$ (ver el remate con el DEM).

**Lo que dice el álgebra ↔ lo que se ve.**
- $A = U\Sigma V^{T}$ ↔ girar (o reflejar) con $V^{T}$, estirar en los ejes con $\Sigma$, girar con $U$. Tres movimientos que entendemos por separado (clases 1 y 3).
- $\Sigma$ diagonal con entradas $\ge0$, nunca complejas ↔ no hay giro escondido que arruine la cuenta, porque el giro se lo llevaron $U$ y $V$.
- $\sigma_1\cdots\sigma_n = |\det A|$ ↔ el área (volumen) de la elipse es el de la circunferencia por el producto de los semiejes.
- $\sigma_k = 0$ ↔ la elipse se aplastó en esa dirección: $v_k$ está en el núcleo, $u_k$ queda fuera de la imagen. Las "dos bases relacionadas con el núcleo y la imagen" del anuncio son exactamente $V$ y $U$.
- Base privilegiada ↔ "no hay base privilegiada salvo por el producto interno": la SVD la construye a partir del producto interno (ortogonalidad), no a partir de direcciones fijas. Por eso siempre existe.
- Matriz simétrica ↔ la elipse tiene los ejes en las direcciones propias: $U=V$ y $\sigma_i=|\lambda_i|$. Este es el "caso" que va a aparecer en la clase 10.

## Cuentas chicas

**Ejemplo 1: $A=\begin{pmatrix}3&0\\4&5\end{pmatrix}$, SVD a mano con enteros.**

La base de entrada sale de $A^{T}A$, que es simétrica:
$$A^{T}A=\begin{pmatrix}3&4\\0&5\end{pmatrix}\begin{pmatrix}3&0\\4&5\end{pmatrix}=\begin{pmatrix}25&20\\20&25\end{pmatrix}.$$
Autovalores: $(25-\mu)^2-400=0 \Rightarrow \mu=45,\ 5$. Autovectores: $(1,1)$ y $(1,-1)$. Entonces $\sigma_1=\sqrt{45}=3\sqrt5\approx6{,}71$, $\sigma_2=\sqrt5\approx2{,}24$, y $v_1=\tfrac1{\sqrt2}(1,1)$, $v_2=\tfrac1{\sqrt2}(1,-1)$.

La base de salida se obtiene transformando: $u_i = A v_i/\sigma_i$.
$$A\begin{pmatrix}1\\1\end{pmatrix}=\begin{pmatrix}3\\9\end{pmatrix}\ \Rightarrow\ u_1=\tfrac{1}{\sqrt{10}}(1,3),\qquad A\begin{pmatrix}1\\-1\end{pmatrix}=\begin{pmatrix}3\\-1\end{pmatrix}\ \Rightarrow\ u_2=\tfrac1{\sqrt{10}}(3,-1).$$
Chequeo: $u_1\cdot u_2 = (3-3)/10 = 0$. La base ortogonal $\{(1,1),(1,-1)\}$ de la entrada fue a parar a la base ortogonal $\{(1,3),(3,-1)\}$ de la salida. Chequeo del área: $\sigma_1\sigma_2 = 3\sqrt5\cdot\sqrt5=15=\det A$.

Comparar con los autovectores de $A$: $\lambda=3$ con $(1,-2)$ y $\lambda=5$ con $(0,1)$. No son perpendiculares entre sí y no coinciden con $v_1,v_2$. Mismo producto $3\cdot5=15$, pero ejes distintos: la diagonalización mira las direcciones que caen sobre sí mismas; la SVD mira las direcciones perpendiculares que siguen perpendiculares.

**Ejemplo 2: la rotación de 90°, $R=\begin{pmatrix}0&-1\\1&0\end{pmatrix}$.** Polinomio característico $\lambda^2+1=0$: autovalores $\pm i$, ningún autovector real. $R^{T}R=I$: valores singulares $1,1$. La circunferencia sigue siendo circunferencia; la SVD dice "no estira nada, sólo gira", que es lo que se ve.

**Ejemplo 3: la simétrica $\begin{pmatrix}2&1\\1&2\end{pmatrix}$.** Autovalores $3,1$ con autovectores $(1,1),(1,-1)$ (clase 8). Valores singulares: $3,1$, mismas direcciones. Acá autovectores y vectores singulares coinciden.

**Verificación.** En numpy, `np.linalg.svd(A)` devuelve `U, s, Vt` (los signos de las columnas pueden venir cambiados; sólo importa la dirección). En GeoGebra, como pidió el profesor: dibujar la circunferencia unidad, aplicar la matriz con `AplicaMatriz`, y medir los semiejes de la elipse que sale; tienen que dar $6{,}71$ y $2{,}24$ en las direcciones $(1,3)$ y $(3,-1)$.

**Remate: SVD de un modelo digital de elevación** (`datos/dem_copernicus/`). Un recorte $512\times512$ del Copernicus DEM GLO-30 sobre la Precordillera de Mendoza (alturas entre 1014 y 2989 m) se trata como matriz y se reconstruye con los $k$ primeros valores singulares. El error RMS en metros, según `svd_results_512.json`: $k=1\to103$, $2\to66$, $5\to31$, $10\to17$, $20\to9{,}8$, $50\to4{,}4$, $100\to2{,}0$. "El relieve aparece en $k\approx20$". Trampa didáctica anotada en el README: la energía acumulada da 99,6 % ya con $k=1$ porque la altura media (~1600 m) domina $\sigma_1$; conviene mirar RMS o restar la media. La SVD del recorte tarda 0,06 s en un M1 y la reconstrucción con $U,\Sigma,V^{T}$ cacheados menos de 2 ms, así que entra con un slider en marimo.

## Dónde está desarrollado

- **Apunte: cubierto desde la versión 3 (2026-10-17)** en `09-svd.tex`, sección `sec:svd`, anticipado y pendiente de validar por la cátedra. Lo que sigue describe el estado anterior: La SVD no tiene sección propia en el apunte v3. Sólo menciones: `02-hilo-de-la-materia.tex` (fila 7 de la tabla: "SVD = la circunferencia unidad se vuelve elipse, con ejes ortogonales antes y después"; marcada "SVD pendiente"), `10-transformaciones-conformes.tex` §Proyecciones cartográficas ("sus valores singulares describen las escalas principales de deformación; su determinante describe el cambio local de área"), y las tablas de propuesta en `19-apendice-rubricas.tex` (filas "existe una base ortogonal de la entrada que va a una base ortogonal de la salida" / "$A=U\Sigma V^T$" / "matrices simétricas") y `21-apendice-notebooks.tex` (notebook 9 propuesto).
- **Unidad marimo:** `unidades/09_cambio_de_base_svd.py` (lección **anticipada**, 2026-10-17: círculo → elipse en tres etapas, $v_k$ y $\sigma_k u_k$, inversa y pseudoinversa, cuatro subespacios en una $3\times2$, aproximación de rango $k$ de una matriz de alturas; pendiente de validar por la cátedra). El prototipo del DEM (`datos/dem_copernicus/svd_dem_proto.py`: espectro, energía, RMS vs $k$, reconstrucciones en hillshade, vectores singulares como perfiles) quedó integrado el 17/10/2026: la unidad carga el DEM real con `lib.dem_precordillera()` (en el navegador una submuestra $128\times128$ embebida en `cb104.py`; con el repo clonado el recorte $512\times512$), con slider de $k$, casilla para restar la media y la tabla de RMS vs $k$ del recorte 512 (`svd_results_512.json`).
- **Bibliografía del campus:** Strang, *Álgebra lineal y sus aplicaciones* (sólo parte 1 descargada) y Calvetti & Somersalo, *Less is More Linear Algebra*; el profesor dijo en clase (2026-10-14) que el segundo "es el que lo explica mejor, pero está en inglés" *(transcripción auto-traducida)*. Sin comentario textual del profesor en la lista del campus para estos dos. Para la clase 7 del 2025: Polya, *Cómo plantear y resolver problemas* ("un libro muy muy bueno sobre el tema"), y los artículos de Molina & Oktaç y González-Rojas-Roa-Fuentes ("no me parecen excepcionales pero me parecía interesante ojearlos").
- **Material del profesor:** videos embebidos sobre SVD (no descargables); `fuentes/campus/profesor/LaSVD.wxmx`, la SVD analítica en wxMaxima de $A=\begin{pmatrix}1&2&4\\-3&-2&3\end{pmatrix}$ ($AA^T$ y $A^TA$, polinomio característico, autovectores, ortogonalidad de a pares, $U$ y $V^T$ normalizados, $\Sigma$ con las raíces de los autovalores y la verificación $U\Sigma V^T=A$; circuló por el grupo y el profesor lo reenvió el 2026-10-17); GeoGebra anunciado para la próxima clase.

## Enlaces del mapa

- Viene de: `autovector`, `autovalor`, `polinomio-caracteristico` (clase 6: el problema de las raíces complejas), `producto-cuna` (detector de colinealidad para hallar autovalores), `matriz-ortogonal` y `producto-interno` (clase 1: qué significa que una base sea ortonormal), `nucleo` (clase 5: dónde están los $\sigma=0$).
- Lleva a: `cambio-de-base` (clase 8: la SVD como cambio de base con bases distintas a la entrada y la salida), `inversa` y `pseudoinversa` (clase 10: $A^{-1}=V\,(1/\Sigma)\,U^{T}$), `cuatro-subespacios`, `regresion-simple`, `procrustes`, `regresion-total` (clase 11: los cuatro problemas), `forma-cuadratica` (clase 12 y la nota de formas cuadráticas), `jacobiano` (clase 9: los valores singulares de la jacobiana son las escalas de deformación de una proyección).
- Qué se conserva: la ortogonalidad de una base bien elegida de la entrada. La pregunta del profesor es "¿qué base ortogonal de la entrada se asigna a una base ortogonal de la salida?".

## Huecos y dudas

- La clase 7 del 2025 mezcla autovectores (que la clase 6 ya había empezado; el profesor mismo duda: "tengo dudas sobre si esto se había ya visto la semana anterior") con la SVD. En 2C2026 los autovectores entraron el 2026-09-16 y la diagonalización el 2026-09-30, así que lo que queda para esta clase es sólo la SVD y sus aplicaciones.
- No hay fecha 2025 confirmada; el resumen del campus no las trae para las clases 7 a 10.
- El resumen 2025 escribe $A=B_{av\mapsto e}\,D\,B_{e\mapsto av}$; el 2026-09-30 el profesor escribió $T_{\text{can}}=A\,D\,A^{-1}$ con $A$ = autovectores en columnas. Son lo mismo con $A=B_{av\mapsto e}$. Ver la duda de notación en la ficha 08.
- Qué quiere decir exactamente "localización GPS" como meta: en el transcript del 2026-09-30 el profesor habla de la señal que se repite cada 20 cm y la ambigüedad de ciclos, pero no dice cómo entra la SVD. A preguntar.
- Falta la nota de formas cuadráticas del campus (pedida el 2026-10-14) en `fuentes/campus/`.
- El ejercicio inicial del 2025 (transformación no lineal que conserva el producto por escalar) no tiene enunciado completo; no se reconstruye.
