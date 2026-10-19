---
clase: "09"
titulo: Repaso de análisis (con álgebra de contrabando) — derivada, gradiente, jacobiano
fecha_2025: null
fechas_2026: ["2026-10-14"]
estado: con-transcripcion
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-9
  - fuentes/transcripciones/2026-10-14.md
  - fuentes/notion/sistemas_de_coordenadas_geometria_diferencial.md
conceptos: [derivada-aproximacion-lineal, gradiente, jacobiano, hessiana, funcion-implicita, superficie-parametrica, primera-forma-fundamental]
apunte: ["11"]
unidad: 10_jacobiano_primera_forma
---

# Clase 9 — Repaso de análisis (con álgebra de contrabando)

> **Estado:** con transcripción del miércoles 2026-10-14 (resumen Notion + transcript auto-traducido al inglés). La hessiana (máximos y mínimos, 2025) no se tocó en 2C2026; quedó para la clase de formas cuadráticas.

## El hilo del profesor (cursada 2025)

"Hicimos clase de repaso de análisis. Resolvimos tres ejercicios" *(profesor, resumen 2025)*:

1. Composición de funciones y de derivadas, "pensando la derivada o las derivadas como objetos que aproximan linealmente funciones", con una definición amplia:
$$\lim_{\epsilon\to0}\frac{f(x+\epsilon)-f(x)}{\epsilon}=f'(x)\quad\Rightarrow\quad f(x+\epsilon)-f(x)\approx f'(x)\,\epsilon,$$
y si la función es vectorial, $f(\vec v+\vec\epsilon)-f(\vec v)\approx Df(\vec v)\,\vec\epsilon$, "donde $Df$ puede ser el gradiente, o una matriz jacobiana, etc.". **"Dato clave: el gradiente es una forma lineal no un vector..."** *(profesor, resumen 2025)*.
2. Planos tangentes con el gradiente: "la propiedad de que el gradiente es perpendicular a una superficie/curva de nivel. Vimos que esto tenía que ver justamente con que el gradiente es una forma lineal, y la curva de nivel 0 de esa forma lineal es el plano tangente a la gráfica de la función". Coherente con "la derivada es la mejor aproximación lineal a una función en determinado punto".
3. Máximos y mínimos: "aparecía por ahí una forma cuadrática (la matriz hessiana), y tratamos de lograr algún tipo de intuición sobre cómo tenía que comportarse y por qué".

Cierre: JAX, "una librería de python que sabe derivar", y tarea: "exploren la relación entre SVD, autovalores y autovectores, e inversa de una transformación lineal" (eso abre la clase 10).

## Lo que pasó en 2C2026

**Miércoles 2026-10-14.** Después de una charla inicial sobre el abuso de poder docente, tres ejercicios de la guía de análisis y una explicación de por qué esto importa para la materia.

**Plano normal a una curva intersección.** Una función $F$ de tres variables (en $\mathbb R^4$ como gráfica) con conjunto de nivel $\Sigma_1$ que contiene al punto $(1,-1,1)$, y una superficie paramétrica $\Sigma_2$ en $u,v$. Se pide el plano normal a la curva $C=\Sigma_1\cap\Sigma_2$ en $P$. Primera confusión, del profesor: "estos ejercicios confunden porque están en una dimensión más de la que uno puede imaginar"; el punto dado no está en la gráfica (en $\mathbb R^4$) sino en la proyección del conjunto de nivel a $\mathbb R^3$. Segunda confusión: leyó "plano tangente a la curva", explicó que "una curva no tiene plano tangente, tiene infinitos", y al releer: "dice plano *normal* a la curva. Qué tonto" *(transcripción auto-traducida)*. Resolución, propuesta por un alumno (Francisco) y validada: la normal a $\Sigma_1$ es el gradiente de $F$; la normal a $\Sigma_2$ es $r_u\times r_v$; el producto cruz de las dos normales da la tangente a $C$, "la aproximación lineal de la curva como intersección de las dos aproximaciones lineales de las superficies"; con esa tangente y $P$ se arma el plano normal.

**Corrección en vivo.** "El gradiente de una función es un vector... no, mentí, lo dije mal, gracias por preguntar. **El gradiente es una forma lineal, no un vector.** Es una forma lineal porque me permite hacer una aproximación lineal de la función. [...] Las formas lineales representan planos; la aproximación lineal a mi función es ese plano; por eso es normal a la superficie de nivel" *(transcripción auto-traducida)*. Fuente: `fuentes/transcripciones/2026-10-14.md`, línea 114 del transcript crudo ("The gradient of a function is a vector... No, I lied"); el resumen de Notion lo registra en la línea 35. Es el mismo objeto de la clase 4 (ficha 04, 30/9: "no existe el vector fila, lo que llamamos vector fila se llama forma lineal"): la regla graduada que lee cuánto sube $f$ con cada pasito, y que se transforma con la inversa. La flecha "perpendicular a la curva de nivel" aparece recién cuando fijo un producto interno; sobre una superficie ese producto interno es la primera forma fundamental $E, F, G$ de abajo, y por eso la perpendicular dibujada en la grilla $(\varphi, \lambda)$ no es la perpendicular sobre el terreno. Quedó como caja de recordatorio en las unidades 06 (sección 1, y la 4b con la SVM) y 10 (sección 1), y es uno de los cuatro cambios de chip de la Unidad 0: Fundamentos y lenguaje de la cátedra (`unidades/00_desaprender_el_cbc.py`: "el gradiente no es un vector").

**Jacobiana de una superficie paramétrica.** $r:\mathbb R^2\to\mathbb R^3$ pensada con los dos espacios separados: "el plano $(u,v)$ acá y el $\mathbb R^3$ allá, completamente desconectados; cuando recorro todo el plano recorro toda la superficie". Imagen: cortar un pedacito de la pelota y hacerle zoom hasta que parece plano. "La matriz jacobiana describe esa transformación lineal local"; sus columnas $r_u$, $r_v$ "generan el plano que puedo recorrer a la salida" y "el espacio que no puedo recorrer es la normal, por eso el producto cruz". El profesor dijo "dos filas y tres columnas" y escribió las derivadas de $x,y,z$ respecto de $u,v$: es $3\times2$ (ver Huecos).

**Teorema de la función implícita.** Probar que $\ln(x+y^2-z^2)-xyz=1$ define $x=g(y,z)$ cerca de un punto dado. Las tres condiciones: la función grande vale cero en el punto, es $C^1$, y la derivada respecto de la variable que se despeja no es cero. Lectura geométrica, que es lo que le importaba: $\partial F/\partial x\neq0$ dice que "la normal a la superficie tiene componente en $x$"; si la normal fuera perpendicular al eje que quiero despejar, un plano paralelo a los otros dos ejes "no puede recortar un pedacito chiquito de superficie, siempre me queda media superficie". Ejemplo: la esfera $x^2+y^2+z^2=R^2$ define $z=g(x,y)$ arriba, pero no define $x=g(y,z)$ donde la normal es perpendicular al eje $x$. La imagen: "un plano tiene que hacerle sombra al otro". "Mecánicamente es más fácil, pero no tiene sentido; la deducción sí tiene sentido."

**Por qué esto es la materia.** "Como agrimensor, lo que hago siempre es describir posiciones, y uso unos números para describir posiciones en otro espacio. [...] La conversión de coordenadas es una $f$ de $\mathbb R^2$ a $\mathbb R^3$, o de $\mathbb R^2$ a $\mathbb R^2$: por eso se llama sistema de coordenadas" *(transcripción auto-traducida)*. Un parche del elipsoide es un pedacito curvo descripto con dos coordenadas; en cada punto se pregunta "si avanzo en esta dirección acá, en qué dirección y a qué velocidad avanzo allá", y "cuál es la línea más corta entre dos puntos" (geodésica, fácil en la esfera, difícil en el elipsoide). Singularidad del polo: con latitud y longitud, "mover la latitud me saca del polo, mover la longitud no me mueve: cualquier longitud a 90° es quedarse en el polo". Eso es una pregunta de derivadas: derivar la parametrización respecto de $\varphi$ y ver qué pasa. También: un campo vectorial "para esta teoría no es un espacio lleno de flechas; es una función de $\mathbb R^n$ a $\mathbb R^n$, todos los vectores implantados en el cero; tiene sentido pensarlos como puntos". Cuaterniones: descartados ("agregan complicaciones que oscurecen la materia").

Tarea: leer la nota de formas cuadráticas del campus antes de la próxima clase; probar SVD en GeoGebra con sistemas $2\times3$ o $3\times2$. (El trámite de equivalencias de Gustavo, al final de la grabación, no es parte de la clase.)

## Hecho geométrico

**Derivada como aproximación lineal.** Álgebra: $f(v+\epsilon)\approx f(v)+Df(v)\,\epsilon$. Se ve: zoom en un punto hasta que la curva parece recta, la superficie parece plana. $Df$ es esa recta o ese plano, y es una transformación lineal: entra un pasito, sale un pasito. Escalera: en $\mathbb R$, $f'(x)$ es un número (la pendiente); en $\mathbb R^2\to\mathbb R$, el gradiente: una forma lineal con dos números; en $\mathbb R^2\to\mathbb R^3$, la jacobiana $3\times2$; en general $m\times n$.

**Gradiente.** Álgebra: $\nabla f(p)\,h=\partial_xf\,h_1+\partial_yf\,h_2$, una fila por una columna. Se ve: una regla graduada de rectas paralelas (clase 4); la recta de nivel cero de esa regla, corrida al punto, es la tangente a la curva de nivel de $f$. "Perpendicular a la curva de nivel" es lo mismo que "el vector de la forma es perpendicular a sus rectas de nivel". No es una flecha que vive en la superficie: es la máquina de medir cuánto sube $f$ con cada pasito.

**Jacobiano.** Álgebra: $J=\begin{pmatrix}r_u&r_v\end{pmatrix}$, columnas = derivadas parciales. Se ve: la grilla $(u,v)$ dibujada sobre la superficie como líneas coordenadas (clase 2); en un punto, los pasitos $du$, $dv$ van a $r_u\,du+r_v\,dv$, el plano tangente. El cuadradito $du\times dv$ va a un paralelogramo de lados $r_u$, $r_v$. La normal $r_u\times r_v$ es la dirección inaccesible: lo que la transformación lineal local no alcanza (el "espacio inaccesible de la salida" de la clase 10).

**Función implícita.** Álgebra: $F(x,y,z)=0$ define $z=g(x,y)$ cerca de $p$ si $\partial_zF(p)\neq0$. Se ve: el gradiente de $F$ (normal a la superficie de nivel) tiene que tener sombra sobre el eje $z$; si la normal está acostada en el plano $xy$, la superficie está "de canto" vista desde arriba y no es gráfica de ninguna función de $(x,y)$ ahí. En $\mathbb R$: $F(x,y)=0$ define $y=g(x)$ si $\partial_yF\neq0$; la circunferencia falla en $(\pm1,0)$, donde la tangente es vertical.

**Superficie paramétrica.** Álgebra: $r(u,v)$, con $J$ de rango 2 salvo en puntos singulares. Se ve: en el polo, $r_\lambda=0$; la línea coordenada de longitud se contrajo a un punto; la jacobiana pierde una columna y el paralelogramo tangente se aplasta.

**Primera forma fundamental** (página de Notion de Gustavo; apunte 13). Álgebra: $ds^2=E\,du^2+2F\,du\,dv+G\,dv^2$ con $E=r_u\cdot r_u$, $F=r_u\cdot r_v$, $G=r_v\cdot r_v$; en matriz, $g=J^{T}J$. Se ve: la regla para medir longitudes del pasito en la superficie usando sólo los números $(du,dv)$. $E$ y $G$ son los cuadrados de los lados del paralelogramo tangente, $F$ dice si es rectángulo ($F=0$) o no. Con un cambio de coordenadas, $g'=J^{T}gJ$: "el mismo patrón que las rotaciones" (Notion), y el mismo que el cambio de base de la clase 8 pero para una forma cuadrática.

**Hessiana** (2025; en 2026 quedó para formas cuadráticas). Álgebra: $f(p+h)\approx f(p)+\nabla f(p)\,h+\tfrac12\,h^{T}Hh$. Se ve: después del plano tangente, el siguiente término es una forma cuadrática que dice si la gráfica queda arriba del plano (mínimo), abajo (máximo) o lo cruza (silla). Sus autovectores son las direcciones principales de curvatura de la gráfica; sus autovalores, cuánto se curva en cada una. Es la puerta a la curvatura (clase 12).

## Cuentas chicas

**Esfera de radio 1, latitud $\varphi$ y longitud $\lambda$:** $r(\varphi,\lambda)=(\cos\varphi\cos\lambda,\ \cos\varphi\sin\lambda,\ \sin\varphi)$.
$$r_\varphi=(-\sin\varphi\cos\lambda,\ -\sin\varphi\sin\lambda,\ \cos\varphi),\qquad r_\lambda=(-\cos\varphi\sin\lambda,\ \cos\varphi\cos\lambda,\ 0).$$
En $\varphi=\lambda=0$ (el punto $(1,0,0)$ sobre el ecuador): $r_\varphi=(0,0,1)$, $r_\lambda=(0,1,0)$. Entonces $E=1$, $F=0$, $G=1$: el paralelogramo tangente es un cuadrado unidad, y $ds^2=d\varphi^2+d\lambda^2$. En general $E=1$, $F=0$, $G=\cos^2\varphi$, que es el $ds^2=R^2\,d\varphi^2+R^2\cos^2\varphi\,d\lambda^2$ del apunte. En $\varphi=60°$: $G=\tfrac14$, o sea $r_\lambda$ mide la mitad: un grado de longitud vale $111\cdot\tfrac12\approx55$ km (Oslo en la tabla de Notion). En $\varphi=90°$: $r_\lambda=(0,0,0)$, $G=0$, la jacobiana tiene una columna nula: el polo.

**Jacobiana de $(u,v)\mapsto(u,\ v,\ u^2+v^2)$ en $(1,1)$.**
$$J=\begin{pmatrix}1&0\\0&1\\2u&2v\end{pmatrix}\Bigg|_{(1,1)}=\begin{pmatrix}1&0\\0&1\\2&2\end{pmatrix},\qquad r_u=(1,0,2),\ r_v=(0,1,2).$$
Normal: $r_u\times r_v=(0\cdot2-2\cdot1,\ 2\cdot0-1\cdot2,\ 1\cdot1-0\cdot0)=(-2,-2,1)$. Chequeo con la otra lectura: la misma superficie es el nivel cero de $F(x,y,z)=x^2+y^2-z$, y $\nabla F(1,1,2)=(2,2,-1)$: la misma dirección, signo opuesto. Las dos normales del ejercicio del 2026-10-14 son estas dos cuentas. Primera forma en ese punto: $E=5$, $F=4$, $G=5$; el paralelogramo tangente tiene lados $\sqrt5$ y no es rectángulo. Verificado con `np.cross`.

**Hessiana chica.** $f(x,y)=xy$ en el origen: gradiente $(0,0)$, $H=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, autovalores $\pm1$ con autovectores $(1,1)$ y $(1,-1)$: sube en una diagonal, baja en la otra, silla. $f=x^2+y^2$: $H=2I$, mínimo.

**Verificación como la haría el profesor.** En GeoGebra 3D: `Superficie(cos(u)cos(v), cos(u)sin(v), sin(u), u, -π/2, π/2, v, 0, 2π)` y mirar cómo se achican los paralelos hacia el polo. En Python, JAX (`jax.jacfwd`) o sympy para derivar $r$ y multiplicar $J^{T}J$.

## Dónde está desarrollado

- **Apunte:** `11-superficies-geodesia.tex` §Pasar del plano a una superficie (`sec:plano-superficie`: la métrica como primera traducción algebraica, "de lo global a lo local", y la cita del resumen 2025 sobre el gradiente como forma lineal); `11-superficies-geodesia.tex` §Coordenadas curvilíneas (`sec:curvilineas`: $r_u$, $r_v$, base local), §Variedades y espacio tangente (`sec:variedades`: "el plano tangente es la mejor aproximación lineal local"; $dF_p$ entre tangentes), §Métrica y primera forma fundamental (`sec:metrica`: $E,F,G$, la esfera con $\cos^2\varphi$), en `10-transformaciones-conformes.tex` §Proyecciones (valores singulares de $dP_p$ como escalas de deformación). También `08-algebra-transformaciones.tex` §Formas lineales, párrafo "El gradiente es una forma lineal" (ejemplo $f=x^2+y$ en $(1,1)$ con la forma $2h+k$), y la fila "Derivada" de la tabla de `06-afines-homogeneas.tex`. La hessiana y la función implícita no están en el apunte.
- **Unidad marimo:** `unidades/10_jacobiano_primera_forma.py` (piloto, 2026-10-17): loma, plano, cilindro y esfera $(\varphi,\lambda)$ con ejes locales $r_u, r_v$, plano tangente, $J$ coloreada y $E,F,G$ vivos; gradiente como forma lineal y función implícita como mención con enlace a esta ficha; la hessiana no entra (va con formas cuadráticas).
- **Ejercicio resuelto:** `ejercicios/2026-10-14_interseccion_superficies/` (clase 09, 14/10/2026): curva $C$ = paraboloide $x^2+y^2+z=1$ ∩ plano $x+y=1$, punto $P=(1/4,3/4,3/8)$ donde la tangente $r'(t)=(1,-1,2-4t)$ es paralela a $x-z=0$; resolución en `solucion_interseccion_superficies.md`, figuras con matplotlib/plotly y gif de cámara girando.
- **Bibliografía del campus:** Sáenz, *Cálculo Vectorial*; Fortney, *A Visual Introduction to Differential Forms and Calculus* (el gradiente como forma); Efimov, *Formas cuadráticas y matrices* (hessiana, próxima clase). Sin comentario textual del profesor para estos tres en la lista del campus. Página propia de Gustavo en Notion (2026-08-22): primera forma, tabla de 1° de longitud, $g'=J^{T}gJ$.
- **Material del profesor:** JAX mencionado en 2025 (sin archivo); nota de formas cuadráticas en el campus (pendiente de bajar).

## Enlaces del mapa

- Viene de: `forma-lineal`, `curvas-de-nivel`, `dualidad` (clase 4: el gradiente es una de ellas), `transformacion-lineal` (la derivada es una), `producto-vectorial` (clase 5: la normal), `lineas-coordenadas` (clase 2: la grilla $(u,v)$ sobre la superficie), `cambio-de-base` (clase 8: $g'=J^{T}gJ$), `rotacion-infinitesimal` (clase 1: "ir a lo chico para volver a lo grande").
- Lleva a: `svd` (clase 7: los valores singulares de $J$ son las escalas principales de una proyección), `forma-cuadratica` y `curvatura` (clase 12: hessiana, segunda forma), `elipsoide` (clase 13: parches y normales), `geodesica` (clase 12/14: la línea más corta depende de $E,F,G$), `cuatro-subespacios` (clase 10: imagen de $J$ = plano tangente, inaccesible = normal).
- Qué se conserva: a primer orden, el pasito. La pregunta del profesor es "si avanzo en esta dirección en las coordenadas, en qué dirección y a qué velocidad avanzo en la superficie".

## Huecos y dudas

- La función $F$ del primer ejercicio y la parametrización de $\Sigma_2$ no se recuperan del transcript (sale "u + b², u + b, u − b" y es ilegible). Conseguir el enunciado de la guía de análisis.
- El profesor dijo "dos filas y tres columnas" para la jacobiana de $\mathbb R^2\to\mathbb R^3$ pero la escribió por derivadas de $x,y,z$ respecto de $u,v$: es $3\times2$ (un vector de $\mathbb R^2$ entra, uno de $\mathbb R^3$ sale). Confirmar que fue un lapsus.
- El punto del ejercicio 1 aparece como $(1,-1,1)$ en el resumen y como "1, 1, 1" en el transcript. Tomar el del resumen hasta ver la guía.
- La página de Notion de Gustavo usa colatitud ($\sin\varphi$ en $x,y$, $G=R^2\sin^2\varphi$); el apunte y esta ficha usan latitud ($\cos\varphi$). Son la misma esfera con $\varphi$ medida desde el polo o desde el ecuador. Unificar en la unidad.
- La hessiana del 2025 (ejercicio de máximos y mínimos) no tiene enunciado y no se dio en 2026; la nota de formas cuadráticas del campus la va a cubrir.
- Sin fecha 2025 en el campus.
