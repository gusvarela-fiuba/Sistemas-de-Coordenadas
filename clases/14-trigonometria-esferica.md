---
clase: "14"
titulo: "Clase 14: Polígonos geodésicos sobre la esfera: Trigonometría esférica, y Máxima para el elipsoide"
fecha_2025: null
fechas_2026: []
estado: no-dictada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-14-polígonos-geodésicos-sobre-la-esfera-trigonometría-esférica-y-máxima-para-el-elipsoide
  - "Bibliografia/Clavijo - Apunte Teoría Elipsoide (guía para clase).pdf (La forma de la tierra)"
  - fuentes/transcripciones/2026-10-14.md
conceptos: [trigonometria-esferica, poligono-geodesico]
apunte: ["formas-lineales", "esfera"]
unidad: 14_trigonometria_esferica
---

# Clase 14 — Polígonos geodésicos sobre la esfera: trigonometría esférica, y Máxima para el elipsoide

> **Estado:** no dictada todavía en 2C2026. Ficha esqueleto: en el campus sólo está el título. El hilo se arma con el título, la introducción del apunte del profesor sobre el elipsoide y el álgebra de las clases 1 y 5 (producto interno y vectorial). Donde dice "hilo propuesto" no hay fuente del profesor.

## El hilo del profesor (cursada 2025)
Campus: sólo el título *(profesor, resumen 2025)*. El título ya dice el orden: primero polígonos de geodésicas sobre la esfera, donde hay fórmulas cerradas (trigonometría esférica); después el elipsoide, donde no las hay y entra el CAS ("Máxima" es wxMaxima, el que usa el profesor desde la clase 2).

La motivación está en el apunte del profesor sobre el elipsoide, sección "La forma de la tierra": el observador puede "desarrollar la solución de los diversos problemas que plantea la medición sobre la superficie de la esfera —los llamados problemas geodésicos— y construir una poligonal cerrada sobre la tierra, verificando si el error obtenido al regresar al punto de origen es compatible con la precisión de los instrumentos" (figura 1: "Una poligonal geodésica de ejemplo"). Y el cierre de la clase 12 en el campus: la curvatura "nos ayuda a entender ... qué son las líneas geodésicas" *(profesor, resumen 2025)*.

Hilo propuesto: triángulo esférico como tres vectores desde el centro → lados y ángulos son ángulos → ley de cosenos esférica con producto interno y vectorial → exceso esférico = área/$R^2$ → polígono de $n$ lados → qué pasa en el elipsoide: los problemas directo e inverso no cierran en fórmula y se resuelven con series o numéricamente, que es donde entra Maxima.

## Lo que pasó en 2C2026
No se dictó. Lo único de 2026 es del 2026-10-14: "¿cuál es la línea que me lleva de un punto a otro más rápido? En el plano, la recta; en esto tenemos una geodésica. ¿Cómo la calculo? En la esfera no es tan difícil, en el elipsoide es mucho más difícil. Depende de las propiedades locales de la superficie" *(transcripción auto-traducida)*; y sobre Maxima: "lo hice con Maxima, analíticamente, no gráficamente" *(transcripción auto-traducida)*, a propósito de la SVD.

Falta confirmar: fecha (es la última del esqueleto; puede no llegar a dictarse); si el profesor deduce la ley de cosenos con vectores o la da; si muestra un notebook de Maxima para el elipsoide (problema directo/inverso, arco de meridiano); si pide una poligonal como tarea.

## Hecho geométrico
**Trigonometría esférica** (requiere producto-interno, producto-vectorial, geodesica). Pregunta: tres puntos sobre la esfera unidad, unidos por círculos máximos; ¿qué relación hay entre los tres lados y los tres ángulos? Lo que se ve: un triángulo esférico son tres planos por el centro; cada lado es el ángulo entre dos radios, cada ángulo es el diedro entre dos de esos planos. Nada mide en metros: todo son ángulos, y la esfera de radio $R$ sólo multiplica los lados por $R$. Álgebra: si $A,B,C$ son los vectores unitarios de los vértices, el lado $a$ (opuesto a $A$) cumple $\cos a=B\cdot C$ (clase 1: el producto interno mide ángulos); el ángulo en $A$ es el ángulo entre las normales de los planos $OAB$ y $OAC$, es decir entre $A\times B$ y $A\times C$ (clase 5: el producto vectorial da la normal del plano por dos puntos). Juntando las dos:
$$\cos a=\cos b\cos c+\sin b\sin c\cos A,$$
la ley de cosenos esférica. Escalera: en el plano, $a^2=b^2+c^2-2bc\cos A$; sobre la esfera los lados chicos ($\sin b\approx b$, $\cos b\approx1-b^2/2$) devuelven la fórmula plana. Es "ir a lo chico para volver a lo grande": una Tierra lo bastante chica es plana.

Exceso esférico: en el plano los ángulos suman $\pi$; en la esfera suman más, y el sobrante es el área: $A+B+C-\pi=\text{Área}/R^2$ (Girard). Lo que se ve: el triángulo "abomba" y los ángulos se abren; cuanto más grande, más se abren. Sin fuente del profesor, hilo propuesto: para topografía la consecuencia es Legendre, un triángulo esférico chico se calcula como plano restando $\varepsilon/3$ a cada ángulo.

**Polígono geodésico** (requiere geodesica). Pregunta: una poligonal cerrada de $n$ lados geodésicos; ¿cuánto suman sus ángulos? Álgebra: cortando en triángulos, $\sum\text{ángulos}-(n-2)\pi=\text{Área}/R^2$. Lo que se ve: es lo que el apunte del profesor describe como la poligonal cerrada cuyo error de cierre delata que la Tierra no es plana (ni esfera); en una poligonal de agrimensura el "error angular" tiene una parte que no es error sino exceso esférico, y hay que separarla antes de compensar. Sobre el elipsoide los lados son geodésicas que no son círculos (los meridianos sí, los paralelos no), y no hay ley de cosenos cerrada: problema directo (punto + azimut + distancia → punto) y problema inverso (dos puntos → distancia y azimutes) se resuelven con series como la del arco de meridiano del apunte del profesor, o numéricamente. Ahí entra Maxima: el profesor hace en CAS lo que en la esfera se hace a mano.

## Cuentas chicas
**Ley de cosenos con dos puntos en la esfera unidad.** Pongo el vértice $A$ en el polo, $A=(0,0,1)$. El vértice $B$ a distancia angular $c$ sobre el meridiano $\lambda=0$: $B=(\sin c,0,\cos c)$. El vértice $C$ a distancia $b$ sobre el meridiano $\lambda=A$ (el ángulo en el polo es la diferencia de longitudes): $C=(\sin b\cos A,\sin b\sin A,\cos b)$. Entonces
$$\cos a=B\cdot C=\sin c\sin b\cos A+\cos c\cos b.$$
Es la ley de cosenos, y salió de un solo producto interno. Versión sin coordenadas: $(A\times B)\cdot(A\times C)=(A\cdot A)(B\cdot C)-(A\cdot C)(A\cdot B)=\cos a-\cos b\cos c$, y $|A\times B|=\sin c$, $|A\times C|=\sin b$, de donde $\cos A=\dfrac{\cos a-\cos b\cos c}{\sin b\sin c}$.

**Octante.** $A$ = polo, $B=(1,0,0)$, $C=(0,1,0)$: $b=c=90^\circ$, $A=90^\circ$. $\cos a=0+0=0$, $a=90^\circ$. Los tres ángulos son rectos: suman $270^\circ$, exceso $90^\circ=\pi/2$, área $=\pi R^2/2=\tfrac18\cdot4\pi R^2$, un octavo de la esfera. Cierra.

**Triángulo chico.** Lados de 1 km sobre $R=6371$ km: área $\approx0{,}433$ km², exceso $\approx0{,}433/6371^2\approx1{,}07\cdot10^{-8}$ rad $\approx0{,}002''$. Lados de 100 km: exceso $\approx0{,}0001$ rad $\approx22''$. Verificación en marimo: `numpy` con los tres vectores y `arccos` de los productos internos; en GeoGebra 3D, tres puntos sobre `Esfera((0,0,0),1)` y los arcos de círculo máximo.

## Dónde está desarrollado
- Apunte v3: `08-algebra-transformaciones.tex` §"Producto interno: incidencia" y §"Producto vectorial: unir dos puntos, cortar dos rectas" (las dos herramientas); `11-superficies-geodesia.tex` §"Métrica y primera forma fundamental" (esfera: $ds^2=R^2\cos^2\varphi\,d\lambda^2+R^2d\varphi^2$) y §"Esfera, elipsoide y curvatura". No hay trigonometría esférica ni polígonos geodésicos en el apunte: hueco entero.
- Apunte del profesor (Clavijo, elipsoide): la introducción (poligonal cerrada), la definición de azimut vía geodésica y el arco de meridiano en serie; no trata el problema directo/inverso.
- Unidad marimo (**anticipada**, 2026-10-17, pendiente de validar por la cátedra): `unidades/14_trigonometria_esferica.py`, tres vértices sobre la esfera (octante, triángulo chico, tres ciudades argentinas, o $C$ con deslizadores), lados y ángulos por producto interno y cuña, exceso vs área, con las cuentas chicas de esta ficha (octante, ley del coseno) verificadas en `cb104.py`. No está en la serie propuesta de `21-apendice-notebooks.tex`.
- Material de clase del profesor: existen notebooks wxMaxima en `Bibliografia/material de clase 2C2025/` (`Algun_ejemplo_de_rotacion.wxmx`, `Formas_Lineales.wxmx`); son de rotaciones y formas lineales, no del elipsoide. Un notebook "Máxima para el elipsoide" no está en el repo.
- Bibliografía del campus: ninguna entrada comentada por el profesor sobre trigonometría esférica; Coxeter, *Geometría*, tiene un capítulo, sin comentario del profesor para esta clase.
- Cierre del arco: `unidades/15_transformaciones_conformes.py` (desarrollo complementario, pendiente de validar por la cátedra): después de medir sobre la esfera y el elipsoide, cómo llevarlos al plano sin torcer los ángulos (proyecciones conformes, Mercator, Gauss-Krüger).

## Enlaces del mapa
- Viene de: producto-interno (clase 1), producto-vectorial (clase 5), rotacion-3d (los vértices como vectores unitarios girados), geodesica y curvatura (clase 12), elipsoide (clase 13).
- Lleva a: fuera de la materia, a Topografía (compensación de poligonales, exceso esférico) y Geodesia (problemas directo e inverso sobre el elipsoide).
- Qué se conserva: al rotar la esfera, lados, ángulos y área del triángulo no cambian (el producto interno es invariante por rotaciones, clase 1); lo que *no* se conserva al pasar de esfera a elipsoide es la simetría total, y por eso se pierden las fórmulas cerradas.

## Huecos y dudas
- Sin resumen del profesor: todo el contenido entre el título y la motivación del apunte del elipsoide es hilo propuesto.
- "Máxima para el elipsoide": no hay en el repo ni en `Bibliografia/` un notebook `.wxmx` del elipsoide. Si existe en el campus 2025, bajarlo.
- Legendre y el reparto del exceso en topografía son nota de agrimensura, no del profesor.
- Las cifras de exceso para 1 km y 100 km son cálculo propio, orientativas.
- La página Notion de Gustavo parametriza la esfera con $\varphi$ medido desde el polo ($G=R^2\sin^2\varphi$) y el apunte v3 con latitud ($\cos^2\varphi$). Mismo objeto, distinta convención; unificar en latitud, que es la del profesor.
- Si esta clase no se dicta en 2C2026, decidir si la ficha queda como material propio o se archiva.
