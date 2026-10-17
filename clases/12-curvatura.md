---
clase: "12"
titulo: "Clase 12: Curvatura"
fecha_2025: null
fechas_2026: []
estado: no-dictada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-12-curvatura
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-9-repaso-de-análisis-con-álgebra-de-contrabando
  - fuentes/transcripciones/2026-10-14.md
  - "Bibliografia/Clavijo - Apunte Teoría Elipsoide (guía para clase).pdf (sección Radios de curvatura)"
conceptos: [curvatura, forma-cuadratica, geodesica]
apunte: ["13", "06"]
unidad: null
---

# Clase 12 — Curvatura

> **Estado:** no dictada todavía en 2C2026. Ficha esqueleto: el campus tiene una sola oración del profesor y un adjunto; el resto es la escalera que esa oración pide, apoyada en el apunte del profesor sobre el elipsoide. Donde dice "hilo propuesto" no hay fuente del profesor.

## El hilo del profesor (cursada 2025)
Todo el resumen es esto: "La curvatura de una línea y la idea de que la curvatura tiene que ser una forma cuadrática nos ayuda a entender la curvatura del elipsoide y qué son las líneas geodésicas" *(profesor, resumen 2025)*. Recurso adjunto: "Apunte sobre Elipsoide", que es `Clavijo - Apunte Teoría Elipsoide (guía para clase).pdf`.

La oración tiene tres escalones y el orden importa: (1) curvatura de una línea, (2) la curvatura de una superficie en un punto depende de la dirección y esa dependencia *tiene que* ser una forma cuadrática, (3) con eso se entienden el elipsoide (clase 13) y las geodésicas (clase 14). El escalón 2 ya asomó en la clase 9: "Vimos que aparecía por ahí una forma cuadrática (la matriz hessiana), y tratamos de lograr algún tipo de intuición sobre cómo tenía que comportarse y por qué" *(profesor, resumen 2025)*. El "por qué tiene que ser cuadrática" lo demuestra el propio apunte del profesor (sección "Radios de curvatura", prueba 1): la curvatura normal en dirección $\alpha$ sale como $L\cos^2\alpha+2M\cos\alpha\sin\alpha+N\sin^2\alpha$, y de ahí "los máximos y mínimos se darán a intervalos de $\pi/2$".

## Lo que pasó en 2C2026
No se dictó. El 2026-10-14 el profesor ubicó el tema en el calendario: "por eso me interesa hacer un repaso de análisis más o menos a esta altura de la cursada, porque una vez visto lo que vamos a hacer acá, lo siguiente que vemos es curvatura, la superficie del elipsoide, y van a pensar: no, otra vez análisis" *(transcripción auto-traducida)*. Y anunció el requisito: "la próxima clase, formas cuadráticas, ya tienen una nota para leer" *(transcripción auto-traducida)*. Formas cuadráticas aparece entonces dos veces en el plan 2026: como herramienta para SVD (clase 11) y como lenguaje de la curvatura (esta clase). El mismo día dio la motivación geodésica: "¿cuáles son las rectas de esta superficie? Tengo este punto y este otro, ¿cuál es la línea que me lleva de uno a otro más rápido? ... eso es una geodésica. ¿Cómo la calculo? En la esfera no es tan difícil, en el elipsoide es mucho más difícil" *(transcripción auto-traducida)*.

Falta confirmar: fecha; si formas cuadráticas se da como clase propia o dentro de la 11; si el profesor sigue el apunte (curvatura por $\partial\alpha/\partial s$, Euler, Meusnier) o va directo por la hessiana; qué ejemplos numéricos usa.

## Hecho geométrico
**Curvatura de una línea** (requiere derivada-aproximacion-lineal). En $\mathbb R$ no hay curvatura: una función de una variable se curva sólo al mirar su gráfico en $\mathbb R^2$. Definición del apunte del profesor: $\chi=\left|\dfrac{\partial\alpha/\partial v}{\|v\|}\right|$, "la tasa de cambio del ángulo de la tangente a una curva con respecto al avance sobre dicha curva"; "podemos verificar que para un círculo $\chi=1/R$". Lo que se ve: en cada punto hay un círculo que besa a la curva (osculador); la curvatura es $1/R$ de ese círculo. Recta: $R=\infty$, $\chi=0$. Para un gráfico $y=f(x)$: $\chi=\dfrac{|f''|}{(1+f'^2)^{3/2}}$; en un punto con tangente horizontal queda $\chi=|f''|$, la segunda derivada *es* la curvatura.

**Forma cuadrática** (requiere hessiana, svd). Pregunta: en un punto de una superficie $z=f(x,y)$ con tangente horizontal, ¿cuánto se curva la superficie si avanzo en la dirección $\alpha$? Álgebra (apunte del profesor): cortar con el plano vertical que contiene a $(\cos\alpha,\sin\alpha)$ da una curva plana cuya curvatura es
$$\chi(\alpha)=\begin{pmatrix}\cos\alpha&\sin\alpha\end{pmatrix}\begin{pmatrix}f_{xx}&f_{xy}\\f_{xy}&f_{yy}\end{pmatrix}\begin{pmatrix}\cos\alpha\\\sin\alpha\end{pmatrix},$$
la hessiana de la clase 9 evaluada en la dirección. Eso es una forma cuadrática: un número que sale de un vector pasando por una matriz simétrica, "igual que $\|v\|^2=v^{\mathsf T}v$ pero con otra matriz en el medio". Lo que se ve: la hessiana es simétrica, y la clase 10 ya dijo que en las simétricas autovectores y vectores singulares coinciden y son ortogonales: hay dos direcciones perpendiculares, de curvatura máxima y mínima (direcciones principales, $\kappa_1,\kappa_2$), y en cualquier otra dirección $\chi(\alpha)=\kappa_1\cos^2\alpha+\kappa_2\sin^2\alpha$ (Euler; el apunte lo escribe $\chi=|A|+|B|\cos2\alpha$). Diagonalizar la hessiana es rotar los ejes hasta que desaparezca el término cruzado. En $\mathbb R^2$ esto es el problema 4 de la clase 11 (eje mayor y menor de una elipse); en $\mathbb R^n$ es la SVD de una matriz simétrica. Sin fuente del profesor, hilo propuesto: el producto $\kappa_1\kappa_2=\det(\text{hessiana})$ es la curvatura de Gauss $K$, que el apunte v3 escribe para el elipsoide como $K=1/(MN)$; el determinante vuelve a ser "cuánto área" (clase 5), ahora de la imagen de la normal.

**Geodésica** (requiere primera-forma-fundamental). Pregunta: ¿qué es "ir derecho" sobre una superficie? Hilo propuesto: una curva es geodésica cuando no se tuerce *dentro* de la superficie, es decir cuando toda su curvatura es la que la superficie le obliga (su aceleración es normal a la superficie, componente tangencial cero). Lo que se ve: es la trayectoria de un hilo tenso sobre la cáscara, o de un auto que va con el volante derecho; es la más corta entre puntos cercanos. En la esfera son los círculos máximos; en el elipsoide, los meridianos lo son y los paralelos no (salvo el ecuador). El apunte del profesor la usa sin definirla: el azimut es "ángulo diedro entre el plano meridiano del lugar $a$ y el plano vertical que contiene al vector tangente a la trayectoria geodésica que une los puntos $a$ y $b$".

Escalera: $\mathbb R$ (segunda derivada), $\mathbb R^2$ (curvatura de una curva, un número por punto), $\mathbb R^3$ (superficie: una forma cuadrática por punto, dos curvaturas principales), $\mathbb R^n$ (hessiana $n\times n$, $n$ curvaturas principales por diagonalización).

## Cuentas chicas
**Parábola.** $y=x^2/2$ en el origen: $f'=0$, $f''=1$, $\chi=1$: círculo osculador de radio 1 centrado en $(0,1)$. En $x=1$: $f'=1$, $f''=1$, $\chi=1/2^{3/2}\approx0{,}35$, radio $\approx2{,}83$. GeoGebra: `CírculoOsculador(f, (0,0))`.

**Silla sin término cruzado y con término cruzado.** $z=x^2+xy+y^2$ en el origen: hessiana $\begin{pmatrix}2&1\\1&2\end{pmatrix}$, autovalores $3$ y $1$, autovectores $(1,1)$ y $(1,-1)$. En la dirección $45^\circ$: $\tfrac12(2+1+1+2)=3$; en $-45^\circ$: $\tfrac12(2-1-1+2)=1$; en la dirección del eje $x$: $f_{xx}=2$. Euler con $\alpha$ medido desde $(1,1)$: el eje $x$ está a $45^\circ$ de la dirección principal, $3\cos^2 45^\circ+1\sin^2 45^\circ=2$, cierra. $K=\det=3$. Verificación en marimo: `numpy.linalg.eigh` sobre la hessiana y comparar con `numpy.linalg.svd` (coinciden porque es simétrica).

**Esfera.** $z=\sqrt{R^2-x^2-y^2}$ en el polo: hessiana $-\tfrac1R I$, $\kappa_1=\kappa_2=1/R$ en toda dirección: no hay direcciones principales, todas lo son. Es el caso que el apunte del profesor llama "intuitivo, y no requería un análisis más detallado, por el hecho de ser constante".

## Dónde está desarrollado
- Apunte v3: `13-tercera-lectura.tex` §"Métrica y primera forma fundamental" (métrica $E,F,G$, $ds^2$ matricial, esfera) y §"Esfera, elipsoide y curvatura" (sólo las fórmulas de $M$, $N$ y $K=1/(MN)$, sin deducción); `06-primera-lectura-superficies.tex` (panorama, "de lo global a lo local"). Falta en el apunte: la definición de curvatura de una curva, la segunda forma fundamental, la fórmula de Euler, Meusnier y cualquier definición de geodésica.
- Apunte del profesor (Clavijo, elipsoide): secciones "Radios de curvatura", "Prueba 1" (curvatura normal como forma cuadrática y máximos a $\pi/2$), "Prueba 2: Teorema de Meusnier" (remite a un apunte de Cristóbal de Lozada y Puga y a una construcción en GeoGebra, ninguno en el repo).
- Unidad marimo: `unidades/12_curvatura.py` (**anticipada**: la clase no se dictó; lectura del alumno sobre el esqueleto 2025, el apunte del profesor y el v3, pendiente de validar por la cátedra): segunda forma $L, M, N$, direcciones principales por `solve(I, II)`, $K = \det II/\det I$, sección normal y círculo osculador sobre esfera, cilindro, silla y loma.
- Página Notion de Gustavo: §3 primera forma fundamental, §4 tensor métrico, §5 esfera (tabla de "1° de longitud vale").
- Bibliografía del campus: Efimov, *Formas cuadráticas y matrices* (sin comentario del profesor; escaneo sin capa de texto); Fortney, *A Visual Introduction to Differential Forms* (sin comentario).

## Enlaces del mapa
- Viene de: hessiana, derivada-aproximacion-lineal, superficie-parametrica (clase 9); autovector, diagonalizacion (clases 6–8); svd (clase 7); primera-forma-fundamental (apunte 13).
- Lleva a: elipsoide (clase 13: $M$ y $N$ son las curvaturas principales en meridiano y primer vertical), poligono-geodesico y trigonometria-esferica (clase 14), regresion-total (misma diagonalización).
- Qué se conserva: al rotar los ejes en el plano tangente la forma cuadrática no cambia de valor, sólo de escritura; lo invariante son las dos curvaturas principales (y su producto $K$, que ni siquiera cambia al doblar la superficie sin estirarla).

## Huecos y dudas
- La nota de "formas cuadráticas" del campus no está en el repo: es la fuente primaria de esta clase y hay que bajarla.
- El apunte del profesor escribe la forma cuadrática con $L=f_{xx}$, $N=f_{yy}$, $M=f_{xy}$ (el mixto es $M$); la notación usual tiene $M$ como mixto y $N=f_{yy}$. Coincide en el fondo, no en las letras; fijar cuál usa en clase.
- El paso "$(\nabla f\cdot t)^2=0$ en el punto analizado" del apunte vale sólo con tangente horizontal (ejes puestos en el plano tangente); en coordenadas generales aparece la primera forma fundamental dividiendo. El apunte v3 no lo dice.
- La curvatura de Gauss como determinante y la definición de geodésica por aceleración normal son hilo propuesto, no del profesor.
- Meusnier: el apunte de de Lozada y Puga y el GeoGebra que el profesor "provee aparte" no están en `Bibliografia/`.
