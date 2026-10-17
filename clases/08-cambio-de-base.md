---
clase: "08"
titulo: Cambios de base, más autovectores y experimentar con marimo
fecha_2025: null
fechas_2026: ["2026-09-30"]
estado: con-transcripcion
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-8
  - fuentes/transcripciones/2026-09-30.md
conceptos: [cambio-de-base, diagonalizacion, potencias-de-matrices]
apunte: ["02", "19"]
unidad: 08_cambio_de_base
---

# Clase 8 — Cambios de base, más autovectores y experimentar con marimo

> **Estado:** con transcripción del miércoles 2026-09-30 (resumen Notion + transcript auto-traducido al inglés). El bloque de potencias reales de matrices en marimo (2025) no apareció todavía en 2C2026.

## El hilo del profesor (cursada 2025)

Empezó "haciendo un repaso sobre cambios de base, pensando en que la idea de trabajar con autovectores era tener una base 'conveniente'" *(profesor, resumen 2025)*. El orden:

1. Qué significa cambiar de base: "expresar vectores que vienen dados como combinaciones lineales de un conjunto de vectores como combinación lineal de otro conjunto de vectores".
2. "No parece haber un conjunto de vectores privilegiado a-priori. Esta observación choca con el hecho de que 'lo normal' sea usar la base que llamamos 'canónica'. ¿Y qué tiene de especial la base canónica? Que es la que nos define el producto interno del espacio vectorial. [...] En un espacio vectorial donde la magnitud de un vector no sea algo que esté definido o que importe, la base canónica no tiene nada especial" *(profesor, resumen 2025)*.
3. El cambio de base es lineal, así que es una matriz, "que tiene en sus columnas los vectores de una base expresada en la otra".
4. Cambiar la base de la matriz de una transformación es "componer esta transformación con las transformaciones de cambio de base que correspondan": $M_{av}=C_{av\mapsto e}\cdot M\cdot C_{e\mapsto av}$ *(notación del resumen; ver Huecos)*.
5. Repaso del cambio de base de la SVD: "son dos transformaciones distintas las que aparecen, porque las bases de entrada y salida de la transformación son distintas (ya sea por elección o por obligación si el espacio vectorial es distinto)".
6. Exploración en marimo de "una transformación cualquiera de $\mathbb R^2$ a $\mathbb R^2$". Aplicación: la base de autovectores permite potencias enteras ("aplicar $n$ veces la transformación") y "también potencias reales en el caso de que los autovalores sean reales. [...] Eso nos permite pensar en la transformación como un proceso continuo y graficar la trayectoria que sigue un punto a medida que se va transformando" *(profesor, resumen 2025)*.

## Lo que pasó en 2C2026

**Miércoles 2026-09-30.** El profesor arrancó diciendo que la clase anterior había prometido cambio de base y no había llegado. Tres bloques:

**Cambio de base como concepto.** Retomó el esquema de puntos y rectas en homogéneas: un punto $P$ (columna) está en la recta $L$ (fila) si $L\,P=0$. "Lo que comúnmente llamamos vector fila en realidad se llama forma lineal; no existe tal cosa como un vector fila" *(transcripción auto-traducida)*. Si transformo todo con una matriz $A$, los puntos van como $AP$ y las rectas como $LA^{-1}$, para que $LA^{-1}AP=LP$ siga dando cero: "las cosas se cancelan". Y una transformación $T$ que llevaba el punto a la recta tiene que convertirse en $T^{*}=A\,T\,A^{-1}$ para que $T^{*}(AP)$ siga cayendo en $LA^{-1}$. La frase que pidió que "quede grabado a fuego": "no hacemos nada, **convertimos todo para que nada cambie**" *(transcripción auto-traducida)*. "Si pagara 4 horas pero se quedan con la idea de que el cambio de base no modifica nada, ya gané."

**Ejercicio en clase (con dibujo, en hoja grande y centrada).** Formas lineales $(1,1)$ y $(-1,2)$, vector $(3,4)$, transformación
$$T=\begin{pmatrix}1{,}2&0{,}5\\-0{,}1&1{,}3\end{pmatrix},$$
elegida "no muy distinta de la identidad" y con determinante positivo. Consigna: dibujar las curvas de nivel de las dos formas (familias de rectas paralelas; la de nivel 1 pasa por donde el producto da 1, perpendicular al vector de la forma), ubicar el vector en la grilla, transformar el vector con $T$ y las formas con $T^{-1}$ (por adjunta sobre determinante: $\det T=1{,}61$), redibujar y verificar que el vector transformado cae en la misma intersección. Números de la clase: $T(3,4)=(5{,}6,\ 4{,}9)$; la forma $(1,1)$ pasa a $\approx(0{,}86,\ 0{,}43)$ ("se acostó un poco") y $(-1,2)$ queda "un poco más vertical" (en la cuenta: $(-0{,}68,\ 1{,}80)$). El vector estaba "en la séptima curva de una y la quinta de la otra" y ahí sigue: $(1,1)\cdot(3,4)=7$ y $(-1,2)\cdot(3,4)=5$ se conservan. De paso: "cuanto más largo el vector de la forma, más apretadas las curvas: módulo 1 → separación 1, módulo 2 → separación 1/2, módulo 4 → separación 1/4".

**Autovectores y diagonalización.** Pregunta disparadora: "¿qué ganaría pensando la transformación en la base de sus autovalores y autovectores?" En un mundo ideal sin complejos, si sé que un vector se estira al doble y otro se achica a la mitad, sé qué le pasa a cualquier suma de ellos: "la clave es la **independencia**: puedo estirar primero una grilla y después la otra" *(transcripción auto-traducida)*. Pensando los autovectores como formas lineales, la grilla de sus curvas de nivel "se estira o se comprime pero no se rompe": eso es lo que hace una matriz diagonal, como $\begin{pmatrix}1&0\\0&2\end{pmatrix}$ con el cuadrado unidad. La matriz de cambio de base $A$ "tiene los autovectores como columnas", porque al entrar $(1,0)$ en base de autovectores tiene que salir el autovector 1 en canónica. Entonces $T_{\text{can}}=A\,D\,A^{-1}$ y, despejando, $D=A^{-1}\,T_{\text{can}}\,A$. La imagen del "muñequito": entra en canónica como $(1,1)$, el cambio de base le pregunta "¿en qué división de la grilla de autovectores estás?" y lo convierte en algo como $(0{,}3,\ 1{,}2)$, la diagonal le dice "vas a salir como la mitad del autovector 1 más dos veces el autovector 2", y vuelve a canónica.

Jordan: "es importante para resolver sistemas, pero para nosotros la interpretación geométrica es todo" *(transcripción auto-traducida)*. Anuncio de la SVD (ficha 07) y de la meta GPS. No hubo marimo ni potencias de matrices.

## Hecho geométrico

**Cambio de base.** Álgebra: $[v]_{\text{nueva}}=C^{-1}[v]_{\text{can}}$ con $C$ = base nueva en columnas. Se ve: la misma flecha medida con otra grilla. La flecha no se movió; cambiaron los números. Escalera: en $\mathbb R$, cambiar de base es cambiar de unidad (metros a centímetros: el número se multiplica por 100, la longitud no cambia); en $\mathbb R^2$ la grilla puede ser oblicua y con pasos distintos en cada eje; en $\mathbb R^3$ lo mismo con tres direcciones; en $\mathbb R^n$ es una matriz $n\times n$ invertible.

**Los tres tipos de objeto cambian de base distinto.** Vectores (puntos) con $A$, formas lineales (rectas) con $A^{-1}$ del otro lado, transformaciones con $A\,T\,A^{-1}$. Se ve: si todo se convierte a la vez, cada punto sigue en su recta y cada transformación sigue llevando cada punto adonde lo llevaba. "Convertimos todo para que nada cambie."

**Diagonalización.** Álgebra: $T=A\,D\,A^{-1}$ con $D$ diagonal y $A$ = autovectores en columnas. Se ve: la grilla formada por las curvas de nivel de los autovectores se estira en cada dirección por su autovalor, sin romperse; el cuadrado se vuelve paralelogramo y el paralelogramo de autovectores queda más largo en una dirección y más corto en otra. La transformación "no tiene interpretación fácil en la grilla común", pero en la grilla propia es dos estiramientos independientes. Escalera: en $\mathbb R$ toda matriz es diagonal ($a$); en $\mathbb R^2$ hace falta que haya dos direcciones propias reales; una rotación no tiene ninguna y no se diagonaliza en reales (de ahí la SVD, ficha 07).

**Potencias de matrices.** Álgebra: $T^n=A\,D^n\,A^{-1}$, y si los autovalores son positivos, $T^t=A\,D^t\,A^{-1}$ para $t$ real. Se ve: aplicar $n$ veces es estirar $n$ veces cada eje propio; $t$ real convierte la transformación en una película y el punto recorre una trayectoria continua. "La transformación se identifica con la trayectoria que genera." Es la misma jugada de "ir a lo chico para volver a lo grande" de la exponencial de matrices (clase 1), ahora con autovalores reales en lugar de giros.

## Cuentas chicas

**Diagonalizar $A=\begin{pmatrix}2&1\\1&2\end{pmatrix}$ y calcular $A^5$ por la diagonal.**

Polinomio característico: $(2-\lambda)^2-1=0\Rightarrow\lambda=3,\ 1$.
Autovectores: para $\lambda=3$, $(A-3I)v=0$ con filas $(-1,1)$: $v_1=(1,1)$. Para $\lambda=1$, filas $(1,1)$: $v_2=(1,-1)$. Son perpendiculares (la matriz es simétrica).

Cambio de base con los autovectores en columnas y su inversa:
$$P=\begin{pmatrix}1&1\\1&-1\end{pmatrix},\qquad P^{-1}=\frac{1}{-2}\begin{pmatrix}-1&-1\\-1&1\end{pmatrix}=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}.$$
Chequeo de la diagonal: $P^{-1}AP=\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}3&1\\3&-1\end{pmatrix}=\frac12\begin{pmatrix}6&0\\0&2\end{pmatrix}=\begin{pmatrix}3&0\\0&1\end{pmatrix}$.

La quinta potencia:
$$A^5=P\begin{pmatrix}3^5&0\\0&1\end{pmatrix}P^{-1}=\begin{pmatrix}1&1\\1&-1\end{pmatrix}\begin{pmatrix}243&0\\0&1\end{pmatrix}\frac12\begin{pmatrix}1&1\\1&-1\end{pmatrix}=\frac12\begin{pmatrix}244&242\\242&244\end{pmatrix}=\begin{pmatrix}122&121\\121&122\end{pmatrix}.$$
Lectura: el vector $(1,0)=\tfrac12(1,1)+\tfrac12(1,-1)$; la parte en $(1,1)$ se multiplica por $243$ y la parte en $(1,-1)$ queda igual: $\tfrac12(243,243)+\tfrac12(1,-1)=(122,121)$, la primera columna. Verificado con `np.linalg.matrix_power(A,5)`.

**Potencia real.** $A^{1/2}=P\,\mathrm{diag}(\sqrt3,1)\,P^{-1}=\frac12\begin{pmatrix}\sqrt3+1&\sqrt3-1\\\sqrt3-1&\sqrt3+1\end{pmatrix}\approx\begin{pmatrix}1{,}366&0{,}366\\0{,}366&1{,}366\end{pmatrix}$; al cuadrado da $A$ ($1{,}366^2+0{,}366^2=2$). La trayectoria de $(1,0)$ es $A^t(1,0)=\tfrac12(3^t+1,\ 3^t-1)$: empieza en $(1,0)$, pasa por $(1{,}37,0{,}37)$ en $t=\tfrac12$ y llega a $(2,1)$ en $t=1$. Eso es lo que se grafica en marimo con un slider en $t$.

**El ejercicio del 2026-09-30, verificado.** $T^{-1}=\frac1{1{,}61}\begin{pmatrix}1{,}3&-0{,}5\\0{,}1&1{,}2\end{pmatrix}$. Forma $(1,1)$ transformada: $(1,1)\,T^{-1}=\frac{1}{1{,}61}(1{,}4,\ 0{,}7)=(0{,}87,\ 0{,}43)$. Vector transformado: $T(3,4)=(5{,}6,\ 4{,}9)$. Producto: $0{,}87\cdot5{,}6+0{,}43\cdot4{,}9=4{,}87+2{,}13=7{,}0$. Sigue en la curva de nivel 7. Con $(-1,2)\,T^{-1}=\frac1{1{,}61}(-1{,}1,\ 2{,}9)=(-0{,}68,\ 1{,}80)$: $-0{,}68\cdot5{,}6+1{,}80\cdot4{,}9=-3{,}8+8{,}8=5{,}0$. Curva de nivel 5. En Excel: dos columnas para la forma, dos para el vector, `SUMAPRODUCTO`.

## Dónde está desarrollado

- Resolución propia en Julia del ejercicio del 30/9 (grilla de {u, v} y su imagen por inv(A), inversa por adjunta): `ejercicios/2026-09-30_formas_lineales/`.

- **Apunte: cubierto desde la versión 3 (2026-10-17)** en `11-bloque-algebraico.tex`, sección `sec:cambio-base`, anticipado y pendiente de validar por la cátedra. Lo que sigue describe el estado anterior: El cambio de base no tiene sección propia en el apunte v3. `02-hilo-de-la-materia.tex` (fila 8: "cambio de base = la misma flecha medida con otra grilla; potencia real de una matriz = trayectoria continua de un punto bajo la transformación", marcada "Pendiente"). Relacionado: `11-bloque-algebraico.tex` §Formas lineales (`sec:formas-lineales`) tiene el ejemplo de la forma arrastrada $\psi=\varphi A^{-1}$ con verificación numérica, que es el mismo mecanismo del ejercicio del 2026-09-30, y `10-bloque-afines.tex` §Autovalores y geometría (`sec:autovalores-geom`). La tabla "Cambio de base y SVD (propuesta de la ayudantía)" en `19-apendice-rubricas.tex` ordena los conceptos en tres niveles.
- **Unidad marimo:** `unidades/08_cambio_de_base.py` (molde v2, piloto): el mojón de Rotaciones I leído en una base oblicua, `A = [[2,1],[1,2]]` en su grilla propia con película `A^t`, `A^n` por la diagonal y los ejercicios con hueco. Lo que la clase 2025 hizo en marimo (potencias reales y trayectoria) no tiene archivo propio en el repo; la película `A^t` de la unidad lo cubre en parte.
- **Bibliografía del campus:** Axler, *Linear Algebra Done Right* y Butler, *Facts About Eigenvalues* (sin comentario del profesor); Lay, *Álgebra lineal y sus aplicaciones* ("un libro muy popular en internet (aunque no me guste tanto) [...] los primeros dos capítulos sirven como introducción"). Clase 7/8 del 2025: artículos de Molina & Oktaç y González et al. sobre cómo se enseña la transformación lineal.
- **Material del profesor:** la exploración en marimo del 2025 no está en el campus; el ejercicio del 2026-09-30 se hizo en papel.

## Enlaces del mapa

- Viene de: `transformacion-lineal`, `forma-lineal`, `dualidad`, `curvas-de-nivel` (clase 4: la forma como familia de rectas; vectores y formas se transforman distinto), `coordenadas-homogeneas` (clase 3: puntos y rectas como vectores de $\mathbb R^3$), `autovector`, `autovalor` (clase 6), `inversa` (clase 10, pero ya se usó: adjunta sobre determinante), `producto-interno` (lo único que hace especial a la canónica).
- Lleva a: `svd` (clase 7: dos cambios de base distintos, uno a cada lado), `inversa` y `pseudoinversa` (clase 10: $A^{-1}=P\,(1/D)\,P^{-1}$), `exponencial-de-matrices` y `trayectoria` (potencia real como proceso continuo), `primera-forma-fundamental` (clase 9: $g'=J^{T}gJ$ es un cambio de base de una forma cuadrática), `forma-cuadratica` (clase 12).
- Qué se conserva: todas las relaciones entre los elementos. Incidencias ($LP=0$), valores de las formas sobre los vectores, qué transformación lleva qué punto adónde. "Convertimos todo para que nada cambie."

## Huecos y dudas

- **Notación del resumen 2025.** La clase 7 escribe $A=B_{av\mapsto e}\,D\,B_{e\mapsto av}$ (el de la derecha lleva de canónica a autovectores, actúa primero) y la clase 8 escribe $M_{av}=C_{av\mapsto e}\,M\,C_{e\mapsto av}$, que leída con la misma convención no cierra (un vector en base $av$ entraría primero a $C_{e\mapsto av}$). En clase (2026-09-30) quedó $T_{\text{can}}=A\,D\,A^{-1}$ con $A$ = autovectores en columnas, o sea $D=A^{-1}\,T\,A$. Preguntar qué convención de subíndice usa el profesor para no mezclar.
- El transcript dice que $(1,1)$ pasó a "$0{,}86,\ 0{,}43$"; la cuenta da $0{,}87,\ 0{,}43$. Redondeo de pizarrón.
- Los números "$0{,}3$ y $1{,}2$" del muñequito en base de autovectores son ilustrativos (no se dijo qué matriz); no reconstruirlos.
- Faltó en 2C2026 el bloque de potencias reales y trayectorias en marimo. Puede reaparecer con la SVD o quedar para la unidad.
- Sin fecha 2025 en el campus.
- La frase "no hay base privilegiada a priori; lo especial de la canónica es el producto interno" es del resumen 2025; en el transcript 2026 no aparece dicha así. Vale igual como hilo del profesor.
