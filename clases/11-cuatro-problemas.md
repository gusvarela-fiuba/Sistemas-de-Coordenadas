---
clase: "11"
titulo: "Clase 11 - 4 problemas"
fecha_2025: null
fechas_2026: []
estado: no-dictada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-11-4-problemas
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-10-inversas
  - fuentes/transcripciones/2026-10-14.md
  - datos/dem_copernicus/README.md
conceptos: [regresion-simple, interseccion-de-circulos, procrustes, regresion-total]
apunte: ["09"]
unidad: 11_cuatro_problemas
---

# Clase 11 — Cuatro problemas

> **Estado:** no dictada todavía en 2C2026. Ficha esqueleto: en el campus 2025 la clase es sólo una lista de cuatro títulos; el hilo de abajo se arma desde el cierre de la clase 10, el anuncio del 2026-10-14 y el álgebra ya vista. Donde dice "hilo propuesto" no hay fuente del profesor.

## El hilo del profesor (cursada 2025)
El campus da sólo la lista *(profesor, resumen 2025)*: "Problema 1: Regresión simple · Problema 2: Intersección de círculos · Problema 3: Procrustes · Problema 4: Regresión total".

El hilo real viene del final de la clase 10: "En base a eso encontramos la forma de resolver un sistema de ecuaciones sobre-determinado y encontrar el punto de la entrada que corresponde en la salida a lo más cercano al término independiente del sistema de ecuaciones. Esto es algo que mencionamos como pseudo-inversa de Moore-Penrose. En el último segmento de la clase hicimos un punteo rápido de las distintas cosas que podemos construir a partir de este concepto (de pseudoinversa), como adelanto de las clases que siguen" *(profesor, resumen 2025)*. Los cuatro problemas son ese punteo desarrollado: cuatro preguntas de medición que se contestan con la misma maquinaria (cuatro subespacios, pseudoinversa, SVD).

Hilo propuesto, sin fuente del profesor: los problemas van de menos a más álgebra. El 1 y el 2 se resuelven con ecuaciones normales (pseudoinversa de una matriz alta); el 2 necesita antes un truco para volverse lineal; el 3 y el 4 ya no usan la pseudoinversa sino la SVD de una matriz chica armada con los datos, y en el 4 la respuesta está en el *menor* valor singular, no en el mayor.

## Lo que pasó en 2C2026
No se dictó. El 2026-10-14 el profesor anunció el tema y su requisito: "Lo que quiero explicar la semana que viene es cómo usamos la descomposición en valores singulares para resolver algunos problemas que tienen que ver con la red. Regresión, [ajuste de] puntos, etc. Para eso necesito que vean un concepto llamado formas cuadráticas, que no es tan complicado pero tampoco tan simple, y en el campus hay una nota sobre eso que les había pedido leer" *(transcripción auto-traducida)*. También dijo que para SVD "está en el de Strang, y hay uno en inglés, Calvetti y Somersalo, que para mí es el que lo explica mejor" *(transcripción auto-traducida)*, y pidió como tarea reproducir en GeoGebra, con un sistema 2×3 o 3×2, lo que él hizo en Maxima analíticamente.

Falta confirmar: fecha (la clase siguiente al 2026-10-14 es el 2026-10-21, pero el profesor dijo "ver rápido formas cuadráticas" primero, así que los cuatro problemas pueden correrse); si los cuatro problemas se dan en una clase o en dos; qué números usa; si Procrustes se presenta con nombre propio o como "ajuste de dos sistemas de coordenadas".

## Hecho geométrico
**Regresión simple** (requiere pseudoinversa, sistema sobredeterminado). Pregunta: $n$ puntos $(x_i,y_i)$ que "deberían" estar en una recta $y=ax+b$ pero no están; ¿qué recta? Álgebra: el sistema $A\theta=y$ con $A$ de $n\times 2$ (columna de las $x$, columna de unos) y $\theta=(a,b)$ no tiene solución; las ecuaciones normales $A^{\mathsf T}A\,\theta=A^{\mathsf T}y$ dan $\theta=A^{+}y$. Lo que se ve: en $\mathbb R^n$ el vector $y$ no está en el plano generado por las dos columnas de $A$; la solución es la proyección ortogonal de $y$ sobre ese plano (clase 10: la imagen y su complemento). Ojo: la distancia que se minimiza es la vertical en cada $x_i$, no la perpendicular a la recta. Eso es lo que la separa del problema 4.

**Intersección de círculos** (requiere pseudoinversa, nucleo). Pregunta: tres o más círculos conocidos (centro y radio) que deberían cortarse en un punto; ¿cuál? Álgebra: cada círculo es cuadrático, $(x-a_i)^2+(y-b_i)^2=r_i^2$, pero al restar dos ecuaciones se cancelan $x^2+y^2$ y queda una recta: $2(a_j-a_i)x+2(b_j-b_i)y=r_i^2-r_j^2-a_i^2+a_j^2-b_i^2+b_j^2$. Con $m$ círculos salen $m-1$ rectas: sistema lineal, sobredeterminado si $m\ge4$, pseudoinversa. Lo que se ve: restar dos círculos da la recta que pasa por sus dos puntos de corte (eje radical); tres círculos, dos rectas, un punto. Conexión con Topografía (sin desarrollar): es la trilateración, y es el esqueleto del posicionamiento por distancias.

**Procrustes** (requiere svd, producto-interno). Pregunta: una nube de puntos medida en un sistema y la misma nube en otro; ¿qué rotación (y escala) superpone mejor una sobre la otra? Álgebra: centrar las dos nubes, armar $H=P^{\mathsf T}Q$ ($2\times2$, la "matriz de correlación" de las coordenadas), descomponer $H=U\Sigma V^{\mathsf T}$; la rotación es $R=VU^{\mathsf T}$ y la escala $\operatorname{tr}\Sigma/\|P\|^2$. Lo que se ve: la SVD de $H$ separa "cuánto giro" ($U$, $V$) de "cuánto estiro" ($\Sigma$); si las nubes son la misma figura girada, $\Sigma$ es un múltiplo de la identidad y $R$ es exactamente el giro. Conexión con Topografía (sin desarrollar): es la transformación de Helmert 2D, el ajuste de dos sistemas de coordenadas con puntos comunes.

**Regresión total** (requiere svd, valores-singulares). Pregunta: la misma nube del problema 1, pero ahora las $x$ también tienen error; ¿cuál es la recta que minimiza las distancias *perpendiculares*? Álgebra: centrar, armar la matriz de datos $X$ ($n\times2$), SVD $X=U\Sigma V^{\mathsf T}$; la dirección de la recta es el primer vector singular derecho (mayor $\sigma$), la normal es el segundo (menor $\sigma$), y $\sigma_{\min}^2$ es la suma de residuos al cuadrado. Lo que se ve: la nube tiene una elipse de dispersión; la recta total es su eje mayor; la dirección de menor varianza es la que "no explica nada" y es la normal. Es la misma imagen de la clase 7 (circunferencia que se vuelve elipse) leída al revés: datos → elipse → ejes.

Escalera: en $\mathbb R$, ajustar $n$ medidas $y_i\approx c$ es tomar el promedio (proyección sobre la columna de unos). En $\mathbb R^2$ aparece la recta y la diferencia vertical/perpendicular. En $\mathbb R^n$ todo sigue igual: columnas de $A$, proyección, SVD. El remate del proyecto está en `datos/dem_copernicus/README.md`: la SVD de un DEM de $512\times512$ es el problema 4 en grande, con la nota didáctica de que "la energía acumulada engaña (99,6 % con $k=1$) porque la media domina $\sigma_1$" — restar la media antes, igual que centrar la nube.

## Cuentas chicas
**Problema 1.** Puntos $(-1,1),(0,1),(1,4)$. Con las $x$ centradas, $A^{\mathsf T}A=\begin{pmatrix}2&0\\0&3\end{pmatrix}$, $A^{\mathsf T}y=\begin{pmatrix}3\\6\end{pmatrix}$, entonces $a=3/2$, $b=2$: recta $y=\tfrac32x+2$. Residuos $(\tfrac12,-1,\tfrac12)$: suman cero y $\sum x_i\,r_i=-\tfrac12+0+\tfrac12=0$, es decir el residuo es ortogonal a las dos columnas de $A$. Verificación: Excel, `=ESTIMACION.LINEAL`, o GeoGebra `AjusteLineal`.

**Problema 2.** Círculos $x^2+y^2=25$, $(x-6)^2+y^2=25$, $(x-3)^2+(y-7)^2=9$. Primero menos segundo: $12x=36$, $x=3$. Primero menos tercero: $6x+14y=74$, con $x=3$ da $y=4$. Punto $(3,4)$; se chequea en los tres círculos ($9+16=25$, $9+16=25$, $0+9=9$). Sin el tercer círculo quedaban dos candidatos, $(3,\pm4)$: la tercera ecuación es la que elige.

**Problema 4.** Puntos $(1,0),(-1,0),(0,2),(0,-2)$, ya centrados. $X^{\mathsf T}X=\begin{pmatrix}2&0\\0&8\end{pmatrix}$: $\sigma_{\max}^2=8$ en la dirección $y$, $\sigma_{\min}^2=2$ en la dirección $x$. La regresión total da la recta vertical $x=0$ (residuo total $2$). La regresión simple de $y$ sobre $x$ da $a=\sum x_iy_i/\sum x_i^2=0$: recta horizontal $y=0$ (residuo $8$). Mismos cuatro puntos, dos rectas perpendiculares: la pregunta cambia la respuesta.

**Problema 3.** Cuadrado $P$: $(1,0),(0,1),(-1,0),(0,-1)$; $Q$ es el mismo cuadrado girado $90^\circ$. $H=P^{\mathsf T}Q=\begin{pmatrix}0&2\\-2&0\end{pmatrix}=2\,R(-90^\circ)$, con $\Sigma=2I$; la receta $R=VU^{\mathsf T}$ devuelve $R(90^\circ)$ y escala $4/4=1$. Verificación en marimo con `numpy.linalg.svd(H)`.

## Dónde está desarrollado
- Apunte: `09-svd.tex` §"Sistemas de ecuaciones y aplicaciones" sólo enumera ("ajustar coordenadas a partir de observaciones redundantes", "determinar intersecciones") y dice "este bloque deberá precisarse con los enunciados y ejemplos que presente la cátedra"; `08-algebra-transformaciones.tex` tiene producto interno y núcleo. Ninguno de los cuatro problemas está desarrollado en el apunte.
- Unidad marimo (**anticipada**, 2026-10-17, pendiente de validar por la cátedra): `unidades/11_cuatro_problemas.py`, los cuatro problemas como un solo problema (residuo perpendicular a la imagen; ecuaciones normales y `lstsq`, autocontenida porque la unidad 09 de SVD/pseudoinversa sigue pendiente), con las cuentas chicas de esta ficha (problemas 1 a 4) verificadas en `cb104.py`. La serie propuesta (`21-apendice-notebooks.tex`) tiene el nº 9 "Cambio de base y SVD: ... inversa y pseudoinversa"; el prototipo `datos/dem_copernicus/svd_dem_proto.py` ya hace el problema 4 sobre un DEM (reconstrucciones $k=1\ldots100$, RMS vs $k$).
- Bibliografía del campus: Strang, *Álgebra lineal y sus aplicaciones*; Calvetti y Somersalo, *Less is More Linear Algebra* (ambos nombrados el 2026-10-14 para SVD, sin comentario escrito del profesor); Efimov, *Formas cuadráticas y matrices* (sin comentario).
- Material de clase: la "nota sobre formas cuadráticas" del campus que el profesor pidió leer no está bajada en `fuentes/`.

## Enlaces del mapa
- Viene de: pseudoinversa, sistema-sobredeterminado, cuatro-subespacios (clase 10); svd, valores-singulares, base-privilegiada (clase 7); producto-interno (clase 1); forma-cuadratica (clase 12, anunciada como requisito el 2026-10-14).
- Lleva a: forma-cuadratica (la hessiana y $X^{\mathsf T}X$ son la misma cosa), curvatura (direcciones principales = problema 4 sobre una superficie), y, en Topografía, Helmert y trilateración.
- Qué se conserva: en los problemas 1 y 2, el residuo ortogonal a la imagen (lo que queda es perpendicular a lo que se explica); en el 3, distancias y ángulos de la nube (sólo giro y escala); en el 4, la dirección que menos cambia bajo $X^{\mathsf T}X$.

## Huecos y dudas
- Sin resumen del profesor para esta clase: todo el hilo entre los cuatro títulos es propuesto.
- No está claro si "regresión simple" es el ajuste con la vertical (ecuaciones normales) o si el profesor lo plantea directo con la pseudoinversa de la clase 10; el resultado es el mismo, el camino no.
- "Intersección de círculos": la linealización por resta es la que se usa; el profesor podría linealizar por Taylor (jacobiano, clase 9) en vez de restar. Preguntar.
- Procrustes: la fórmula $R=VU^{\mathsf T}$ depende de convenciones (puntos por filas o por columnas); fijar la del profesor antes de la unidad marimo.
- La nota de formas cuadráticas del campus no está en el repo; bajarla y citarla en esta ficha y en la 12.
- La conexión con Helmert 2D y trilateración es nota de agrimensura, no del profesor.
