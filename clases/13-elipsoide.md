---
clase: "13"
titulo: "Clase 13: Geometría del elipsoide (deducciones a partir de la simetría)"
fecha_2025: null
fechas_2026: []
estado: no-dictada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-13-geometría-del-elipsoide-deducciones-a-partir-de-la-simetría
  - "Bibliografia/Clavijo - Apunte Teoría Elipsoide (guía para clase).pdf"
  - fuentes/transcripciones/2026-10-14.md
  - fuentes/notion/sistemas_de_coordenadas_geometria_diferencial.md
conceptos: [elipsoide, simetria]
apunte: ["06", "13"]
unidad: null
---

# Clase 13 — Geometría del elipsoide (deducciones a partir de la simetría)

> **Estado:** no dictada todavía en 2C2026. Ficha esqueleto: en el campus sólo está el título. La fuente que la sostiene es el apunte del propio profesor sobre el elipsoide (20 páginas, CC-BY-SA, figuras de Mariano Harguinteguy), adjunto a la clase 12.

## El hilo del profesor (cursada 2025)
Campus: sólo el título *(profesor, resumen 2025)*. El hilo lo da su apunte "Geometría del Elipsoide y cálculos Geodésicos", con estos títulos propios:

- *La forma de la tierra*: un observador que mida una poligonal cerrada o un grado de latitud en distintos lugares encuentra que "el modelo esférico no se ajusta perfectamente": el error de cierre es mayor que el instrumental, y "la estimación del radio terrestre varía con la latitud". De ahí el elipsoide de revolución.
- *El elipsoide de revolución*: cuádrica $x^2/a_1^2+y^2/a_2^2+z^2/b^2=1$ con $a_1=a_2$, construida al girar la elipse meridiana $x^2/a^2+z^2/b^2=1$ alrededor del eje $Z$. Tabla de parámetros: aplastamiento $f=(a-b)/a$, excentricidad lineal $E=\sqrt{a^2-b^2}$, primera $e^2=(a^2-b^2)/a^2$, segunda $e'^2=(a^2-b^2)/b^2$.
- *Coordenadas*: latitud = ángulo entre la vertical elipsoidal (normal a la superficie) y el plano $XY$; longitud = ángulo diedro entre planos meridianos; azimut = diedro entre el plano meridiano y el plano vertical que contiene la tangente a la geodésica.
- *Hoja de ruta*: radio de una sección plana → dos demostraciones (máximos y mínimos de la curvatura normal; Meusnier) → "los radios mayor y menor del elipsoide de revolución en un punto tienen que ser inevitablemente el radio de la sección meridiana y el de otra perpendicular a esta, llamada primer vertical" → relacionar esos radios con los módulos de los vectores base de $(\varphi,\lambda)$ → calcular $M$ y $N$ en función de $a,e,\varphi$ → de paso, la conversión $\varphi,\lambda\to X,Y,Z$ → arco de meridiano.
- *Radios de curvatura*: definición $\chi=|\partial\alpha/\partial v|/\|v\|$; prueba 1 (forma cuadrática en $\alpha$, extremos a $90^\circ$, radio medio $R=\sqrt{R_{\min}R_{\max}}$ por integración de $1/\chi$); prueba 2 (Meusnier, remitido a un apunte aparte).
- *Significado de la latitud elipsoidal*: la latitud se lee en la tangente a la elipse meridiana, $\partial z/\partial x'=\tan(\pi/2-\varphi)$; de ahí $z^2=\dfrac{\sin^2\varphi}{\cos^2\varphi}\dfrac{b^4}{a^4}x'^2$.
- *Conversión $\varphi,\lambda\to X,Y,Z$*: $x'=\dfrac{a\cos\varphi}{\sqrt{1-e^2\sin^2\varphi}}$ (radio del paralelo), $z=\dfrac{b\sin\varphi}{\sqrt{1+e'^2\cos^2\varphi}}$, luego $x,y$ con $\lambda$.
- *Radio meridiano (revisita)*: $M=\dfrac{a(1-e^2)}{(1-e^2\sin^2\varphi)^{3/2}}$, y "$\|\varphi\|=M$".
- *Radio del primer vertical*: por Meusnier, el paralelo de radio $x'$ es sección oblicua de la normal: $x'=N\cos\varphi$, $N=\dfrac{a}{\sqrt{1-e^2\sin^2\varphi}}$.
- *Arco de meridiano*: $S=\int M\,d\varphi$, serie binomial en $e^2\sin^2\varphi$, potencias de seno pasadas a cosenos de $2\varphi,4\varphi,\dots$, coeficientes $A\ldots E$ tabulados ($x_n$: 1/2, 1, 3, 10, 35 …) "para minimizar los errores a la hora de programar las fórmulas en una planilla". Ejercicio: graficar el decrecimiento de $x_n$ y estimar en metros el aporte de cada término.
- *Conclusión y puntapié inicial*: con conversión, módulos $\|\varphi\|,\|\lambda\|$ y arcos, bosquejar Mercator, cilíndrica equivalente, equidistante, elipsoide→esfera equiárea, Mercator transversa.

## Lo que pasó en 2C2026
No se dictó. Lo único de 2026 es la motivación del 2026-10-14: "lo que estoy describiendo es un pedacito de elipsoide, que es un parche que tiene una curvatura... En cada lugar, en cada lugarcito alrededor de un punto puedo evaluar: cuando avanzo en esta dirección, ¿en qué dirección avanzo acá? Si dibujo una línea así, ¿qué curva es esa línea acá? ¿Y a qué velocidad avanzo?" *(transcripción auto-traducida)*; y el caso degenerado del polo: "mover la latitud me saca del polo, pero mover la longitud no me mueve... es una cuestión de derivadas: tengo que derivar mi parametrización de la superficie respecto de $\varphi$" *(transcripción auto-traducida)*.

Falta confirmar: fecha; si el profesor sigue el apunte en el orden de su hoja de ruta; qué significa exactamente "deducciones a partir de la simetría" en el título (hilo propuesto abajo); si llega al arco de meridiano o lo deja como tarea; qué elipsoide numérico usa (WGS84/GRS80).

## Hecho geométrico
**Elipsoide** (requiere superficie-parametrica, primera-forma-fundamental, curvatura). Escalera: en $\mathbb R^2$ una elipse es una circunferencia estirada en un eje ($x=a\cos t$, $z=b\sin t$); en $\mathbb R^3$ el elipsoide de revolución es esa elipse girada alrededor de su eje menor: todos los meridianos son la *misma* elipse. Parametrización en $(\varphi,\lambda)$: $r=(N\cos\varphi\cos\lambda,\;N\cos\varphi\sin\lambda,\;N(1-e^2)\sin\varphi)$. Lo que se ve: el paralelo de latitud $\varphi$ es una circunferencia de radio $x'=N\cos\varphi$; $N$ es la distancia desde el punto hasta el eje polar *medida a lo largo de la normal*. Primera forma fundamental (hilo propuesto, no está en el apunte del profesor pero sale de $\|\varphi\|=M$ y $\|\lambda\|=x'$): $ds^2=M^2\,d\varphi^2+N^2\cos^2\varphi\,d\lambda^2$. La esfera del apunte v3, $ds^2=R^2d\varphi^2+R^2\cos^2\varphi\,d\lambda^2$, es el caso $M=N=R$.

Latitud geodésica vs geocéntrica: en la esfera la normal pasa por el centro y las dos latitudes coinciden; en el elipsoide la normal *no* pasa por el centro (salvo en ecuador y polos). De la parametrización, $\tan\varphi_{\text{geoc}}=z/x'=(1-e^2)\tan\varphi$: la geocéntrica es siempre menor en módulo. Lo que se ve: la vertical del lugar (la plomada idealizada) apunta "más al polo" que la línea al centro.

**Simetría** (requiere curvatura). Hilo propuesto para "deducciones a partir de la simetría": el plano meridiano es plano de simetría de la superficie (reflejarlo deja el elipsoide igual, clase 3). Entonces la forma cuadrática de la curvatura en un punto es simétrica respecto de la dirección del meridiano, y por la clase 12 sus extremos están a $90^\circ$: las direcciones principales *tienen que* ser meridiano y primer vertical, sin calcular nada. Es lo que el apunte dice "mostraremos en forma sencilla". La simetría de revolución agrega que nada métrico depende de $\lambda$: $M$, $N$, $K=1/(MN)$ son funciones de $\varphi$ sola. Tercera consecuencia: en los polos todas las direcciones son meridianos, así que $M=N$ ahí (punto umbilical); en el ecuador $M=b^2/a$ es el mínimo y $N=a$ es el máximo del primer vertical.

Radios de curvatura, lo que se ve: $M$ (meridiano) es el radio del círculo osculador de la elipse meridiana, crece del ecuador al polo; $N$ (primer vertical) es el radio de la sección normal perpendicular al meridiano y también crece. Como $M<N$ en todo punto salvo los polos, el elipsoide es "más curvo" a lo largo del meridiano que a lo ancho.

## Cuentas chicas
**Elipsoide de juguete** $a=5$, $b=4$: $e^2=1-16/25=0{,}36$, $e'^2=9/16$, $f=1/5$. En el ecuador ($\varphi=0$): $M=a(1-e^2)=3{,}2=b^2/a$, $N=a=5$, $x'=5$, $z=0$. En el polo ($\varphi=90^\circ$): $\sqrt{1-e^2}=0{,}8$, $M=3{,}2/0{,}512=6{,}25=a^2/b$, $N=5/0{,}8=6{,}25$: iguales, como manda la simetría. A $\varphi=45^\circ$: $\sin^2\varphi=\tfrac12$, $1-e^2\sin^2\varphi=0{,}82$, $N=5/\sqrt{0{,}82}\approx5{,}52$, $M=3{,}2/0{,}82^{3/2}\approx4{,}31$; $x'=N\cos\varphi\approx3{,}90$, $z=N(1-e^2)\sin\varphi\approx2{,}50$; se verifica $x'^2/25+z^2/16\approx0{,}609+0{,}391=1$. Latitud geocéntrica: $\tan\varphi_{\text{geoc}}=0{,}64$, $\varphi_{\text{geoc}}\approx32{,}6^\circ$ contra $45^\circ$ geodésicos.

**Tierra (GRS80)** $a=6378{,}137$ km, $f=1/298{,}257$: $M_{\text{ec}}\approx6335{,}4$ km, $N_{\text{ec}}=a$, $M_{\text{polo}}=N_{\text{polo}}\approx6399{,}6$ km. La diferencia geodésica–geocéntrica a $45^\circ$ es $\approx11'$. Verificación: planilla con las dos fórmulas y un slider en $\varphi$, o `pyproj`/`GeographicLib` en marimo.

## Dónde está desarrollado
- Apunte v3: `13-tercera-lectura.tex` §"Esfera, elipsoide y curvatura" ($e^2=2f-f^2$, $M$, $N$, $K=1/(MN)$, figura de la normal que no pasa por el centro) y §"Conexión con la práctica de Agrimensura" (fila "Radios $M,N$: variación geométrica con la latitud"); `06-primera-lectura-superficies.tex` §"Esfera, elipsoide y representación plana" (panorama). Falta en el apunte: la deducción de $M$ y $N$, la conversión $\varphi,\lambda\to X,Y,Z$, la latitud geocéntrica, el arco de meridiano.
- Apunte del profesor (Clavijo, elipsoide): fuente completa, resumida arriba.
- Unidad marimo: `unidades/13_elipsoide.py` (**anticipada**: la clase no se dictó; lectura del alumno sobre el esqueleto 2025, el apunte del profesor y el v3, pendiente de validar por la cátedra): elipsoide 3D con meridiano, paralelo, normal y recta al centro; elipse meridiana con las tres latitudes; $M$, $N$, $(\varphi,\lambda,h)\to(X,Y,Z)$ y $E = M^2$, $G = N^2\cos^2\varphi$ con GRS80 en $45°$.
- Página Notion de Gustavo: §5 esfera (tabla de 1° de longitud por latitud), útil como contraste.
- Bibliografía del campus: ninguna entrada comentada por el profesor sobre elipsoide; Sáenz, *Cálculo vectorial*, y Fortney, para superficies paramétricas (sin comentario).

## Enlaces del mapa
- Viene de: reflexion (clase 3: plano de simetría), rotacion-3d (clase 1: superficie de revolución), superficie-parametrica y jacobiano (clase 9), primera-forma-fundamental (apunte 13), curvatura y forma-cuadratica (clase 12).
- Lleva a: geodesica y poligono-geodesico (clase 14: "Máxima para el elipsoide"), proyecciones cartográficas (el "puntapié inicial" del apunte del profesor; apunte v3 §"Proyecciones cartográficas").
- Qué se conserva: al girar alrededor del eje polar, el elipsoide cae sobre sí mismo ($\lambda$ no aparece en $M$, $N$, $ds^2$); al reflejar en un plano meridiano, también. Lo que cambia con $\varphi$ es la curvatura, y eso es lo que distingue al elipsoide de la esfera.

## Huecos y dudas
- "Deducciones a partir de la simetría" es interpretación: el apunte del profesor demuestra que los extremos están a $90^\circ$ (prueba 1) y "muestra en forma sencilla" que caen en meridiano y primer vertical; la lectura por plano de simetría es hilo propuesto.
- En el apunte del profesor la conversión termina con $x=x'\sin\lambda$, $y=x'\cos\lambda$ (convención invertida respecto de la usual $x=x'\cos\lambda$). Confirmar si es deliberado (eje $X$ hacia el meridiano origen o no).
- La expresión final de $z$ "en términos de $e^2$" del apunte del profesor lleva $\cos^2\varphi$ bajo la raíz donde $x'$ lleva $\sin^2\varphi$; la forma $z=b\sin\varphi/\sqrt{1+e'^2\cos^2\varphi}$ es correcta y equivale a $z=a(1-e^2)\sin\varphi/\sqrt{1-e^2\sin^2\varphi}$. Puede ser error de extracción del PDF; verificar en el original.
- El apunte de Meusnier (de Lozada y Puga) y el GeoGebra asociado no están en `Bibliografia/`.
- Las cifras GRS80 son de memoria, orientativas; recalcular en la unidad marimo antes de citarlas.
