# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Unidad 0 — Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia).

Repaso fundacional de desarrollo complementario (procedencia: clases 1, 4 y 9 + bibliografía del campus); no es contenido
dictado por la cátedra. Cinco ladrillos en orden deductivo, al estilo de Apostol pero con el vocabulario del profesor
y con el terreno como ejemplo: (1) conjuntos, operaciones y grupos; (2) los cuerpos R y C, con C como matrices 2×2;
(3) espacio afín (mojones) vs. espacio vectorial (nace al plantar un origen); (4) el dual V*: una fila es una forma
lineal y el gradiente también; (5) producto interno y métrica G: la cinta métrica que V y V* solos no tienen. Las
frases entre comillas atribuidas al profesor están en `fuentes/` (resúmenes 2025 o transcripciones 2026); lo demás es
desarrollo del apunte.

Chequear:  uv run marimo check --select MW unidades/00_desaprender_el_cbc.py
Exportar:  uv run python tools/build.py --only 00_desaprender_el_cbc
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import cb104 as lib  # cb104:inline
    return (lib,)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


@app.cell
def _(mo):
    mo.md(r"""
    # Unidad 0 — Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia)

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Esto es un repaso de desarrollo complementario, no contenido dictado: lo armamos a partir de las clases 1, 4 y 9 y de la
    bibliografía del campus, para que el resto de las lecciones se lea con una sola cabeza. En el CBC el álgebra lineal
    y el análisis fueron dos materias con dos cuadernos; acá son **una sola herramienta geométrica sobre el terreno**.
    Para que eso cierre hacen falta cinco ladrillos, cada uno con su definición (precisa, sin aparato), su traducción al
    vocabulario del profesor, un ejemplo de campo y su línea de NumPy.

    Colores, iguales en figura y álgebra: lo de **antes** en gris, lo de **después** en
    <span style="color:#1b6f6a">**teal**</span> (segunda columna en <span style="color:#b5451b">**rust**</span>,
    tercera en <span style="color:#c9a227">**gold**</span>), el objeto que importa en
    <span style="color:#7a4e9e">**violeta**</span>.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("00_desaprender_el_cbc"))
    return


@app.cell
def _(lib, np):
    # ---------- funciones de la lección (lo que no está en cb104 se define acá) ----------
    def direccion_entera(v):
        """Un vector no nulo escalado para que su componente más chica (en módulo) valga 1: (2, 1), (1, 2), (1, 1)."""
        v = np.asarray(v, dtype=float)
        m = np.min(np.abs(v[np.abs(v) > 1e-12]))
        return v / m

    def angulo_g(a, b, g):
        """Ángulo en grados entre a y b medido con la métrica g (simétrica definida positiva):
        cos = aᵀ g b / √(aᵀ g a · bᵀ g b). Con g = I es el ángulo de siempre."""
        a, b, g = (np.asarray(t, dtype=float) for t in (a, b, g))
        c = (a @ g @ b) / np.sqrt((a @ g @ a) * (b @ g @ b))
        return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))

    def subida_metrica(w, g):
        """La forma w (fila) levantada a vector con la métrica g: el v que cumple g v = w. Es la dirección de máxima
        pendiente en el terreno cuando w es el gradiente y g la métrica de la grilla en que está escrito."""
        return np.linalg.solve(np.asarray(g, dtype=float), np.asarray(w, dtype=float))

    def matriz_complejo(z):
        """El complejo z = a + ib como la matriz 2×2 que hace lo mismo sobre el plano: [[a, −b], [b, a]]."""
        z = complex(z)
        return np.array([[z.real, -z.imag], [z.imag, z.real]])

    def altura(x, y):
        """La loma de la sección 0: h(x, y) = 100 − (x² + y²)/4, en metros, sobre coordenadas de terreno en metros."""
        return 100.0 - (np.asarray(x, dtype=float) ** 2 + np.asarray(y, dtype=float) ** 2) / 4.0

    def grad_altura(x, y):
        """El gradiente de la loma, a mano: (−x/2, −y/2). Es la fila que lee cuánto sube h con cada pasito."""
        return np.array([-x / 2.0, -y / 2.0])

    def loma3d(u, v):
        """El parche curvo (c) de la sección 2: una loma suave r(u, v) = (u, v, 2·exp(−(u² + v²)/8))."""
        return lib.xyz(u, v, 2.0 * np.exp(-(np.asarray(u) ** 2 + np.asarray(v) ** 2) / 8.0))

    def esfera3d(phi, lam):
        """Trozo de esfera de radio 2 con etiquetas (φ latitud, λ longitud) en radianes."""
        return lib.xyz(2.0 * np.cos(phi) * np.cos(lam), 2.0 * np.cos(phi) * np.sin(lam), 2.0 * np.sin(phi))

    return altura, angulo_g, direccion_entera, esfera3d, grad_altura, loma3d, matriz_complejo, subida_metrica


@app.cell
def _(altura, direccion_entera, go, grad_altura, lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    A_plano = np.diag([2.0, 1.0])  # el plano dibuja el Este estirado por 2: (X, Y) = (2x, y)
    mojon = np.array([2.0, 2.0])  # en metros, sobre el terreno
    w_mojon = grad_altura(*mojon)  # la regla de la cota en el mojón: (−1, −1)
    bajada = -w_mojon  # hacia dónde baja el agua, en el terreno: (1, 1)
    candidatos = {
        "ingenua": direccion_entera(bajada),  # los dos números puestos como flecha en el dibujo
        "perp-dibujo": direccion_entera(lib.forma_transformada(bajada, A_plano)),  # ⊥ a las curvas tal como se ven
        "correcta": direccion_entera(A_plano @ bajada),  # la bajada real del terreno, dibujada
        "curva": direccion_entera(A_plano @ lib.perp2(bajada)),  # a lo largo de la curva de nivel
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            "dirección " + lib.vec_plano(candidatos["ingenua"]) + ": los dos números del gradiente, como flecha": "ingenua",
            "dirección " + lib.vec_plano(candidatos["perp-dibujo"]) + ": perpendicular a las curvas tal como se ven en el plano": "perp-dibujo",
            "dirección " + lib.vec_plano(candidatos["correcta"]): "correcta",
            "dirección " + lib.vec_plano(candidatos["curva"]) + ": a lo largo de la curva de nivel": "curva",
        }),
        value=None,
        label=r"**Predicción.** En el plano dibujado (Este estirado por 2), ¿hacia dónde baja el agua desde el mojón?",
    )
    _niveles = [99, 98, 97, 96, 95, 94]
    _t = np.linspace(0, 2 * np.pi, 121)
    _xs, _ys, _tx, _ty, _tt = [], [], [], [], []
    for _c in _niveles:
        _r = 2.0 * np.sqrt(100.0 - _c)  # radio en el terreno; en el plano, el Este va por 2
        _xs += list(2.0 * _r * np.cos(_t)) + [None]
        _ys += list(_r * np.sin(_t)) + [None]
        _tx.append(0.0)
        _ty.append(_r)
        _tt.append(f"{_c}")
    figura_plano0 = lib.figura_plano((-10, 10), "el plano de la loma · Este estirado por 2", ancho=560, alto=380)
    figura_plano0.update_layout(yaxis=dict(range=[-5, 5]), xaxis=dict(title="Este, en el dibujo (2 por metro)"), yaxis_title="Norte (1 por metro)")
    lib.capa_antes(figura_plano0, (-10, 10), cuadrado=False)
    figura_plano0.add_trace(go.Scatter(x=_xs, y=_ys, mode="lines", line=dict(color=lib.TEAL_DESPUES, width=1.5), name="curvas de nivel (m)", hoverinfo="skip"))
    figura_plano0.add_trace(go.Scatter(x=_tx, y=_ty, mode="text", text=_tt, textposition="top center", textfont=dict(size=10, color=lib.TEAL_DESPUES), showlegend=False, hoverinfo="skip"))
    lib.punto(figura_plano0, A_plano @ mojon, nombre="mojón", texto=f"h = {altura(*mojon):g}")
    mo.vstack([
        mo.md(rf"""
        ## 0. Situación de campo y predicción

        Una loma. Sobre el terreno, con coordenadas en metros, la cota es $h(x, y) = 100 - \tfrac{{x^2 + y^2}}{{4}}$: la
        cima en el origen, y las curvas de nivel son círculos. El mojón está en $(2, 2)$, a $h = {altura(*mojon):g}$ m.
        El gradiente en el mojón, con las derivadas parciales del CBC, es
        $\left(\tfrac{{\partial h}}{{\partial x}}, \tfrac{{\partial h}}{{\partial y}}\right) = {lib.vec_tex(w_mojon)}$:
        el agua baja hacia $-\nabla h$, o sea en la dirección ${lib.vec_tex(bajada)}$ sobre el terreno.

        El plano que tenemos en la mesa está dibujado con el **eje Este estirado por 2** (como una planilla con columnas de
        distinto paso): el punto de terreno $(x, y)$ aparece en $(2x, y)$. Las curvas de nivel se ven como elipses y el
        mojón cae en $(4, 2)$. La pregunta de campo: si dibujamos sobre ese plano la flecha de "hacia dónde baja el agua",
        **¿para dónde la dibujamos?** Las cuatro direcciones están en unidades del dibujo.
        """),
        mo.ui.plotly(figura_plano0),
        prediccion,
    ])
    return A_plano, bajada, candidatos, mojon, prediccion, w_mojon


@app.cell
def _(candidatos, lib, mo, prediccion):
    _i, _p, _c = (lib.vec_tex(candidatos[k]) for k in ("ingenua", "perp-dibujo", "correcta"))
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "ingenua": ("warn",
                    rf"**No.** ${_i}$ es poner los dos números $(h_x, h_y)$ como si fueran una flecha en una grilla que **no mide "
                    r"metros**. En el terreno, ese trazo del dibujo es el desplazamiento $(\tfrac12, 1)$, que no es la bajada más "
                    r"empinada. Los números del gradiente son los de una regla (ladrillo 4); para convertirlos en flecha hace falta "
                    r"saber cuánto mide cada paso de la grilla (ladrillo 5)."),
        "perp-dibujo": ("warn",
                        rf"**No.** ${_p}$ es perpendicular a las elipses **en el papel**, pero el papel está estirado: el ángulo "
                        r"recto del terreno se deformó al dibujar. Perpendicular en una grilla es perpendicular sólo con la métrica de "
                        r"esa grilla; la del dibujo no es la del terreno. Es el error que la sección 2 (b) muestra con números."),
        "curva": ("warn",
                  r"**No.** A lo largo de la curva de nivel la cota **no cambia**: por ahí el agua no baja. La curva de nivel es "
                  r"la marca de la regla; la bajada la cruza. Lo que sí es cierto es que la bajada del terreno no se ve "
                  r"perpendicular a la curva en el dibujo, y ésa es la trampa."),
        "correcta": ("success",
                     rf"**Sí.** ${_c}$ es la bajada real $(1, 1)$ del terreno, dibujada con el Este por 2. No es perpendicular a "
                     r"las elipses del papel, y está bien que no lo sea: el ángulo recto vive en el terreno, no en el dibujo. "
                     r"Eso es lo que esta unidad quiere dejar instalado antes de la primera rotación."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.vstack([
        mo.callout(mo.md(_texto), kind=_kind),
        mo.md(r"""
        El profesor lo dijo en vivo el 14/10 (clase 9), corrigiéndose a sí mismo: "el gradiente de una función es un
        vector… no, mentí, lo dije mal. **El gradiente es una forma lineal, no un vector**; lo es porque me permite hacer
        una aproximación lineal de la función" (transcripción auto-traducida del inglés, `fuentes/transcripciones/2026-10-14.md`).
        Y el resumen 2025 de la misma clase lo llama "dato clave: el gradiente es una forma lineal no un vector". Los cinco
        ladrillos que siguen son lo que hace falta para que esa frase sea obvia.
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico: los cinco ladrillos fundacionales

    **¿Qué se conserva?** El terreno. Mojones, cotas, distancias y ángulos están ahí antes de que elijamos origen, ejes,
    grilla o escala del dibujo; lo que cambia con nuestras elecciones son los **números**. Los ladrillos van en orden
    deductivo: cada uno usa sólo los anteriores, y cada uno pone un nombre a algo que ya hacemos en el campo.

    ### Ladrillo 1 — Conjuntos, operaciones y grupos

    **Definición.** Un *grupo* es un conjunto con una operación interna (combina dos elementos y devuelve otro del
    conjunto) que es asociativa, tiene un *neutro* (no cambia nada) y da a cada elemento una *inversa* (lo deshace). Si
    además el orden no importa, el grupo *conmuta*.

    **En el vocabulario del profesor.** "Transformaciones y Operaciones (por ahora definidas coloquialmente) son dos
    conceptos que van atravesando la materia" (resumen 2025, clase 1). Y la inversa, dicha para todos los casos a la
    vez: "la inversa es un elemento de un conjunto que, al operar con otro resulta en el elemento neutro respecto de
    esa operación" (resumen 2025, clase 10): el $-3$ respecto de la suma, el $\tfrac13$ respecto del producto, $A^{-1}$
    respecto de la composición.

    **En el campo.** Los giros de la estación total alrededor de su eje vertical forman un grupo: girar $30°$ y después
    $50°$ es girar $80°$ (operación interna), no girar es el neutro, girar $-30°$ deshace el $30°$. Las traslaciones
    (mover la estación total de un mojón a otro) también, y conmutan en cualquier dimensión. Los giros conmutan en el
    plano; en 3D no: un giro horizontal y un cabeceo
    en distinto orden dejan el anteojo apuntando a lugares distintos; "la composición de transformaciones lineales no
    es conmutativa" (resumen 2025, clase 1) y "otro ejemplo de operaciones que no conmutan son las rotaciones y las
    traslaciones" (19/8). Lo mide [Rotaciones III](../01c_rotaciones_3d/index.html).

    **En NumPy.** La operación es `A @ B` (primero $B$, después $A$); el neutro, `np.eye(n)`; la inversa aplicada a un
    dato, `np.linalg.solve(A, y)` (el $x$ tal que $Ax = y$); la pregunta "¿conmutan?", `np.allclose(A @ B, B @ A)`.

    ### Ladrillo 2 — Los cuerpos $\mathbb R$ y $\mathbb C$

    **Definición.** Un *cuerpo* es un conjunto con dos operaciones, suma y producto, tales que con la suma es un grupo
    conmutativo (neutro $0$), con el producto los elementos distintos de $0$ son un grupo conmutativo (neutro $1$), y
    el producto distribuye sobre la suma. Los escalares de esta materia viven en dos cuerpos: $\mathbb R$ y $\mathbb C$.

    **Lo que hacen sobre el terreno.** Un real $a$ actúa sobre la recta como $x \mapsto ax$: *escala*; su inversa es
    $\tfrac1a$, su determinante es $a$ y $\lvert a\rvert$ es cuánto escala la longitud. Agregar un $i$ con $i^2 = -1$ equivale **exactamente** a pasar
    de números a matrices: $z = a + ib$ actúa sobre el plano como

    $$M(z) = \begin{pmatrix} \textcolor{#1b6f6a}{a} & \textcolor{#b5451b}{-b} \\ \textcolor{#1b6f6a}{b} & \textcolor{#b5451b}{a} \end{pmatrix},
    \qquad M(z_1 + z_2) = M(z_1) + M(z_2),\quad M(z_1 z_2) = M(z_1)\,M(z_2),\quad M(1/z) = M(z)^{-1},$$

    y multiplicar por $z$ es **rotar** $\arg z$ y **escalar** $\lvert z\rvert$ a la vez ($\det M(z) = \lvert z\rvert^2$).
    Las matrices $2\times2$ de esa forma, con suma y producto de matrices, son el mismo cuerpo $\mathbb C$ con otro
    ropaje (ejercicio E1).

    **En el vocabulario del profesor.** "La matriz de rotación de 2x2 que vimos en algebra del CBC hace exactamente la
    misma operación que hacíamos con los complejos" (resumen 2025, clase 1); la "interesantísima equivalencia en la
    estructura de los numeros complejos y algunas matrices de 2x2" la deja para leer en Gentile, *Complejos y
    Generalización* (bibliografía del campus, clase 1), y "multiplicar por $i$ es rotar $\pi/2$" es un ítem de la
    rúbrica elemental. Lo desarrolla [Rotaciones II](../01b_rotacion_plano/index.html).

    **En NumPy.** `z = 2 + 1j`, `abs(z)`, `np.degrees(np.angle(z))`, y la matriz `np.array([[z.real, -z.imag], [z.imag, z.real]])`.

    ### Ladrillo 3 — Espacio afín (mojones) y espacio vectorial (nace al plantar un origen)

    **Definición.** Un *espacio vectorial* $V$ sobre un cuerpo es un conjunto con suma y producto por escalar que
    respetan linealidad. Una *combinación lineal* es $\lambda_1 v_1 + \dots + \lambda_k v_k$; los $v_i$ son
    *independientes* si la única combinación que da $0$ es la trivial; una *base* es un conjunto independiente que
    genera todo $V$; la *dimensión* es cuántos vectores tiene cualquier base. Un *espacio afín* es un conjunto de puntos
    sin origen: la diferencia de dos puntos es un vector de $V$, y a un punto se le puede sumar un vector.

    **En el campo.** En el terreno hay mojones $P$, $Q$, no flechas: el terreno es afín. Un desplazamiento $Q - P$ sí es
    un vector. Cuando plantamos la estación total en un mojón $O$ y lo declaramos origen, cada mojón se vuelve el vector
    $P - O$ y **nace $V$**: recién ahí hay combinaciones, bases y coordenadas. La otra manera de que nazca es
    homogeneizar: el punto $(x, y)$ pasa a ser el vector $(x, y, 1)$ de $\mathbb R^3$, y las traslaciones, que no son
    lineales porque "las transformaciones lineales conservan el cero" (19/8), pasan a ser matrices $3\times3$
    ([Afines](../04_afines_homogeneas/index.html)).

    **En el vocabulario del profesor.** "Un espacio vectorial es básicamente un conjunto al que se asocian dos
    operaciones (suma y producto por escalar) que cumplen con algunas propiedades básicas a las que llamamos
    'linealidad'" (resumen 2025, clase 4). Sobre los campos vectoriales, el 14/10: "no tiene sentido pensarlos como
    vectores, tiene sentido pensarlos como puntos" (transcripción auto-traducida). Y el 19/8: "la geometría no me exige
    coordenadas, las coordenadas es algo que yo le pongo por comodidad para trabajar". En el espíritu de todo eso: en
    esta materia **todo vector es un punto** (un mojón visto desde $O$) o un desplazamiento entre dos.

    **En NumPy.** Un punto y un desplazamiento son el mismo `np.array([x, y])`; la diferencia la ponemos nosotros. Independencia:
    `np.linalg.matrix_rank(np.column_stack([u, v])) == 2`. Homogeneizar: `np.append(p, 1.0)` (`lib.hom`).
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Ladrillo 4 — El espacio dual $V^*$: una fila es una forma lineal

    **Definición.** Una *forma lineal* es una función lineal $\omega: V \to \mathbb R$. Las formas lineales de $V$
    forman un espacio vectorial, el *dual* $V^*$, de la misma dimensión que $V$; su base natural son las *selectoras de
    coordenadas* $\mathsf x(v) = v_1$, $\mathsf y(v) = v_2$, y toda forma es $\omega = w_1 \mathsf x + w_2 \mathsf y$.
    Se escribe como fila $w^T$ y evalúa por fila por columna: $w^T x = w_1 x_1 + w_2 x_2$, **sin producto interno**.

    **Lo que se ve.** Una forma es una **regla graduada** tirada sobre el plano: sus conjuntos de nivel
    $\{x : w^T x = c\}$ son rectas paralelas equiespaciadas (marcas a distancia $1/\lvert w\rvert$ en la cinta canónica), y leer un punto es
    ver qué marca lo atraviesa. Dos formas dan una grilla. Si los puntos se mueven con $x' = Ax$, las marcas se
    arrastran con la **inversa**, $w'^T = w^T A^{-1}$, para que cada mojón conserve su lectura: $w'^T x' = w^T A^{-1} A x = w^T x$.
    La derivada de una función escalar es de este tipo: $df = \nabla f\,dx$ toma un pasito $dx \in V$ y devuelve cuánto
    sube $f$; $\nabla f$ **vive en $V^*$**.

    **En el vocabulario del profesor.** "No existe el vector fila. Lo que comúnmente llamamos vector fila se llama
    forma lineal" (30/9, transcripción auto-traducida); "las más básicas de esas funciones son las funciones
    selectoras de coordenadas" (resumen 2025, clase 4); "una forma lineal se transforma con una transformación lineal
    del lado 'contrario' que un vector" (resumen 2025, clase 4); "dato clave: el gradiente es una forma lineal no un
    vector" (resumen 2025, clase 9). Lo desarrollan [Formas lineales](../06_formas_lineales/index.html) y
    [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html).

    **En NumPy.** La forma es un array fila y va **a la izquierda**: `w @ x` lee; `w @ np.linalg.inv(A)` o, sin invertir,
    `np.linalg.solve(A.T, w)` la arrastra.

    ### Ladrillo 5 — Producto interno y métrica $G$: la cinta métrica

    **Definición.** Un *producto interno* es una función $\langle u, v\rangle_G = u^T G\, v$ con $G$ simétrica y definida
    positiva ($u^T G u > 0$ si $u \ne 0$). Con él, y recién con él, hay largos $\lvert u\rvert = \sqrt{u^T G u}$ y
    ángulos $\cos\theta = \langle u, v\rangle_G / (\lvert u\rvert\,\lvert v\rvert)$. $V$ y $V^*$ solos no tienen ni lo uno
    ni lo otro: la métrica es un dato **extra**, y es el único puente entre los dos espacios: *baja* un vector a forma,
    $w = Gv$, y *sube* una forma a vector, $v = G^{-1} w$. "El gradiente es perpendicular a la curva de nivel" es la
    frase sobre $G^{-1}\nabla f$, no sobre $\nabla f$.

    **En el vocabulario del profesor.** "Lo único que define a la base que llamamos canónica es que sobre ella tenemos
    definida la noción de distancia a través del producto interno" (resumen 2025, clase 6), y "¿qué tiene de especial
    la base canónica? que es la que nos define el producto interno del espacio vectorial" (resumen 2025, clase 8). O
    sea: en la base canónica $G = I$ y la cinta métrica coincide con la grilla; en cualquier otra, no.

    **En el campo.** La grilla del dibujo estirado tiene $G' = A^{-T} A^{-1}$ (sección 3.2). La grilla $(\varphi,
    \lambda)$ del elipsoide, o la $(u, v)$ de un parche curvo, tiene por métrica la **primera forma fundamental**
    $G = J^T J = \begin{pmatrix} E & F \\ F & G\end{pmatrix}$, que cambia de punto a punto: por eso $(\varphi, \lambda)$ son
    etiquetas y no metros. Lo desarrollan [Producto interno](../02_producto_interno/index.html) y
    [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html).

    **En NumPy.** `a @ g @ b` es $\langle a, b\rangle_G$; `np.sqrt(a @ g @ a)` el largo; `np.linalg.solve(g, w)` sube la
    forma $w$ a vector; `J.T @ J` arma $E, F, G$ a partir de la jacobiana.

    ### Los tres objetos en una tabla, y el puente al cálculo

    | | se escribe | qué es en el terreno | con $x \mapsto Ax$ |
    |---|---|---|---|
    | punto en $V$ (ladrillo 3) | columna $x$ | un mojón visto desde $O$, o un desplazamiento | $x' = Ax$ |
    | forma en $V^*$ (ladrillo 4) | fila $w^T$; $w^T x$ es un número | una regla: las curvas de nivel de la cota | $w'^T = w^T A^{-1}$ (la lectura no cambia) |
    | métrica (ladrillo 5) | $G$ simétrica; $\lvert x\rvert^2 = x^T G\, x$ | cuánto mide cada paso de la grilla | $G' = A^{-T} G\, A^{-1}$ (los largos no cambian) |

    La escalera: en $\mathbb R$ la regla es $wx$ y la métrica un número (la escala); en $\mathbb R^2$ las marcas son
    rectas y $G$ es $2\times2$; en $\mathbb R^3$ las marcas son planos y $G$ es $3\times3$. **El puente al cálculo**, que
    es lo que hace de las clases 9 a 14 la misma materia: derivar una parametrización es usar una matriz lineal, la
    jacobiana $J$, en el parche tangente (ladrillos 1 y 3); el gradiente es una forma (ladrillo 4); $J^T J$ es la
    métrica del tangente (ladrillo 5); y curvarse (hessiana, segunda forma) es una forma cuadrática, un número por cada
    dirección. Esto es una **muestra**; las demostraciones viven en el apunte (anexo).
    """)
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("01_dualidad_gradiente", "Estiramos el Este por 2 y volvemos: los mojones (violeta) viajan con A, las marcas de la regla wᵀ (teal) con A⁻¹, el mojón conserva su cota y la flecha ingenua Aw (rust) pierde la perpendicularidad."))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Las tres ecuaciones maestras de la materia ($Ax = b$, $Ax = \lambda x$, $Ax \approx b$)

    Fijados los cinco ladrillos, casi todas las cuentas lineales del curso responden a una de tres preguntas (las que
    quedan afuera son las de medir con la métrica, $J$ y $J^T J$, en las unidades 02, 10, 13 y 14):

    | ecuación | pregunta de campo | dónde la desarrollamos |
    |---|---|---|
    | $Ax = b$ | **Transformar o deshacer.** Evaluar $Ax$ es transformar: conocemos $A$ y calculamos a dónde va un mojón. Resolver $Ax = b$ es la pregunta inversa: conocemos $A$ y el resultado $b$ y buscamos de dónde vino, $x = A^{-1}b$; leer un punto en otra base es eso mismo (las coordenadas nuevas son la $x$ que cumple $Px = b$). Hallar la homografía que rectifica los cuatro puntos de una foto de dron también es un $Ax = b$, pero con la matriz como incógnita: un sistema lineal $8\times8$ en los coeficientes de $H$. | [Rotaciones I](../01a_punto_quieto/index.html), [II](../01b_rotacion_plano/index.html) y [III](../01c_rotaciones_3d/index.html); [Reflexiones y similaridades](../03_reflexiones_similaridades/index.html); [Afines](../04_afines_homogeneas/index.html); [Proyectivas](../05_proyectivas/index.html); [Formas lineales y dualidad](../06_formas_lineales/index.html); [Cambio de base](../08_cambio_de_base/index.html) |
    | $Ax = \lambda x$ y $Av_i = \sigma_i u_i$ | **Buscar direcciones privilegiadas.** Las que no giran (autovectores): el eje de giro en $\mathbb R^3$, los puntos fijos de una afinidad o proyectiva, las direcciones principales de curvatura del elipsoide, cuyas curvaturas principales $1/M$ y $1/N$ son los autovalores de $I^{-1}II$ (el operador de forma). Y, con la SVD, el par de bases perpendiculares que sigue perpendicular: los $v_i$ (direcciones propias de $A^T A$) van a los $u_i$ girando, pero sin perder el ángulo recto; son los semiejes de la elipse de Tissot. | preparación: [Cuña y determinante](../07a_cuna_determinante/index.html); [Núcleo y autovectores](../07b_nucleo_autovectores/index.html); [Autovalores en 3D y puntos fijos](../07c_autovalores_3d_puntos_fijos/index.html); [Cambio de base](../08_cambio_de_base/index.html); [Cambio de base, SVD e inversas](../09_cambio_de_base_svd/index.html); [Curvatura](../12_curvatura/index.html); [Geometría del elipsoide](../13_elipsoide/index.html); [Transformaciones conformes](../15_transformaciones_conformes/index.html) |
    | $Ax \approx b$ | **Aproximar cuando sobran mediciones y hay error de campaña.** Hay más ecuaciones que incógnitas y el vector medido $b$ cae fuera de la imagen de $A$; buscamos $\hat{x} = A^+ b$, cuya imagen $A\hat{x}$ es la proyección perpendicular de $b$ sobre el subespacio columna $\mathrm{Im}(A)$: regresión e intersección de círculos por distancias. Procrustes y regresión total también son mínimos cuadrados, con otra geometría (restricción ortogonal; distancia perpendicular), y se resuelven con la SVD de una matriz armada con los datos. | [Producto interno](../02_producto_interno/index.html); [Cambio de base, SVD e inversas](../09_cambio_de_base_svd/index.html); [Cuatro problemas](../11_cuatro_problemas/index.html) |

    Los cinco ladrillos son el idioma de la materia, y estas tres ecuaciones son las tres frases que se dicen con él:
    transformamos o deshacemos, buscamos direcciones privilegiadas, o proyectamos lo medido sobre lo que el modelo puede
    explicar. Cada vez que aparezca una cuenta nueva, nos preguntamos cuál de las tres es.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- sección 2: selector de objeto y casos precargados ----------
    casos = {
        "identidad": (np.eye(2), r"nada se mueve: los dos dibujos coinciden."),
        "estirar Este ×2: diag(2, 1)": (np.diag([2.0, 1.0]), r"los puntos se estiran en $x$; la regla se divide, $(1, 1) \mapsto (\tfrac12, 1)$; la perpendicular del dibujo deja de ser la del terreno."),
        "cizalla [[1, 1], [0, 1]]": (np.array([[1.0, 1.0], [0.0, 1.0]]), r"la grilla se acuesta; la regla se corta al revés, $(1, 1) \mapsto (1, 0)$: después sólo lee $x$."),
        "rotación 30°": (lib.rot2(np.deg2rad(30)), r"$A^{-1} = A^T$: la regla gira igual que los puntos y la flecha sigue perpendicular. Con un giro el ladrillo 4 no se nota."),
    }
    parches = {
        "la loma r = (u, v, 2·exp(−(u²+v²)/8))": ("loma", (-3.0, 3.0, 0.25, 2.0, 1.0), (-3.0, 3.0, 0.25, 1.0, 1.0)),
        "trozo de esfera de radio 2 (φ, λ en grados)": ("esfera", (-80.0, 80.0, 5.0, 45.0, np.pi / 180), (-150.0, 150.0, 5.0, 0.0, np.pi / 180)),
    }
    complejos = {
        "z = i (giro 90°)": 1j,
        "z = 1 + i (giro 45°, escala √2)": 1.0 + 1j,
        "z = 2 (escala 2, sin giro)": 2.0 + 0j,
        "z = 0.6 − 0.8i (giro −53.13°, escala 1)": 0.6 - 0.8j,
        "z = −1 (giro 180°)": -1.0 + 0j,
    }
    objeto_sel = mo.ui.dropdown(options=["(a) punto x", "(b) regla graduada wᵀ (el gradiente)", "(c) parche curvo r(u, v)", "(d) complejo z como matriz"],
                                value="(b) regla graduada wᵀ (el gradiente)", label="objeto")
    caso = mo.ui.dropdown(options=list(casos), value="estirar Este ×2: diag(2, 1)", label="A (casos a y b)")
    parche = mo.ui.dropdown(options=list(parches), value="la loma r = (u, v, 2·exp(−(u²+v²)/8))", label="parche (caso c)")
    zeta = mo.ui.dropdown(options=list(complejos), value="z = 1 + i (giro 45°, escala √2)", label="z (caso d)")
    mo.md(r"""
    ## 2. Manipulación

    Un selector con los tres objetos de la tabla y el cuerpo $\mathbb C$ del ladrillo 2, en el panel de la derecha de
    la figura. **(a)** Un punto $x = (1, 2)$ y una parcela: van con $A$. **(b)** La regla $w^T = (1, 1)$ (la cota
    $h = x + y$): sus marcas se arrastran con $A^{-1}$ y el mojón conserva su cota; se dibujan además la flecha
    perpendicular a las marcas nuevas **en el papel** y la bajada real del terreno, $Aw = G'^{-1} w'$, que es la
    perpendicular **con la métrica**. **(c)** Un parche curvo: el jacobiano arma la grilla tangente y $E, F, G$ dicen
    cuánto mide cada paso. **(d)** Multiplicar el plano por un complejo $z$: la matriz $M(z)$ rota y escala. Tres capas:
    gris antes, teal después, violeta el objeto. En (a), (b) y (d), **reproducir** va de la identidad a la transformación.
    """)
    return caso, casos, complejos, objeto_sel, parche, parches, zeta


@app.cell
def _(mo, parche, parches):
    _tipo, _u, _v = parches[parche.value]
    u0 = mo.ui.slider(_u[0], _u[1], value=_u[3], step=_u[2], label="u₀ (φ) del punto", show_value=True)
    v0 = mo.ui.slider(_v[0], _v[1], value=_v[3], step=_v[2], label="v₀ (λ) del punto", show_value=True)
    return u0, v0


@app.cell
def _(angulo_g, caso, casos, complejos, esfera3d, go, lib, loma3d, matriz_complejo, mo, np, objeto_sel, parche, parches, subida_metrica, u0, v0, zeta):
    A, que_pasa = casos[caso.value]
    x_pt = np.array([1.0, 2.0])
    w = np.array([1.0, 1.0])
    parcela = np.array([[1.0, 2.0], [3.0, 1.0], [3.0, 3.0], [2.0, 4.0]])
    rango = 6
    w_despues = lib.forma_transformada(w, A)
    g_despues = np.linalg.inv(A).T @ np.linalg.inv(A)  # la métrica del terreno, escrita en la grilla nueva
    tangente_despues = A @ lib.perp2(w)  # la curva de nivel, dibujada después
    subida_despues = subida_metrica(w_despues, g_despues)  # G'⁻¹ w' = A w: la subida real, dibujada
    ang_papel = angulo_g(A @ w, tangente_despues, np.eye(2))
    ang_terreno = angulo_g(A @ w, tangente_despues, g_despues)
    z = complejos[zeta.value]
    Mz = matriz_complejo(z)
    _objeto = objeto_sel.value[:3]
    if _objeto == "(d)":
        camino = [matriz_complejo(abs(z) ** s * np.exp(1j * s * np.angle(z))) for s in np.linspace(0, 1, 30)]
    elif bool(np.allclose(A.T @ A, np.eye(2))) and not np.allclose(A, np.eye(2)):
        camino = [lib.rot2(t) for t in np.linspace(0, np.deg2rad(30), 30)]
    else:
        camino = [np.eye(2) + s * (A - np.eye(2)) for s in np.linspace(0, 1, 30)]

    def _dinamicas_a(i, etiqueta="x después = A x"):
        Mi = camino[i]
        f = go.Figure()
        lib.capa_despues(f, Mi, rango)
        lib.objeto(f, lib.transformar(parcela, Mi), nombre="parcela después", estelas=lib.estelas(parcela, camino[: i + 1]))
        lib.punto(f, Mi @ x_pt, nombre=etiqueta, texto=lib.vec_plano(Mi @ x_pt))
        return list(f.data)

    def _dinamicas_b(i):
        Mi = camino[i]
        wi = lib.forma_transformada(w, Mi)
        f = go.Figure()
        lib.capa_despues(f, Mi, rango, cuadrado=False, columnas=False)
        lib.rectas_de_nivel(f, wi, np.arange(-12, 13), rango, lib.TEAL_DESPUES, "marcas después: wᵀA⁻¹", destacar=0)
        lib.flecha(f, Mi @ x_pt, Mi @ x_pt + wi / np.linalg.norm(wi) * 1.5, lib.TEAL_DESPUES, "⊥ a las marcas en el papel", ancho=3)
        lib.flecha(f, Mi @ x_pt, Mi @ x_pt + Mi @ w / np.linalg.norm(Mi @ w) * 1.5, lib.COLORES[2], "A w = G'⁻¹ w': la subida real del terreno", ancho=4)
        lib.punto(f, Mi @ x_pt, nombre="mojón después", texto=f"cota {wi @ (Mi @ x_pt):g}")
        return list(f.data)

    if _objeto in ("(a)", "(b)", "(d)"):
        _din = _dinamicas_b if _objeto == "(b)" else (_dinamicas_a if _objeto == "(a)" else (lambda i: _dinamicas_a(i, "z·x después")))
        _titulo = f"{objeto_sel.value} · {zeta.value if _objeto == '(d)' else caso.value}"
        figura = lib.figura_plano(rango, _titulo)
        lib.capa_antes(figura, rango, cuadrado=(_objeto != "(b)"))
        if _objeto == "(b)":
            lib.rectas_de_nivel(figura, w, np.arange(-12, 13), rango, lib.GRIS_ANTES, "marcas antes: wᵀ = (1, 1)", etiquetas=False, destacar=None, ancho=0.8)
        else:
            lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
        lib.punto(figura, x_pt, lib.GRIS_ANTES, "x antes", texto=lib.vec_plano(x_pt))
        for _t in _din(len(camino) - 1):
            figura.add_trace(_t)
        lib.animar(figura, [_din(i) for i in range(len(camino))])
        if _objeto == "(a)":
            _vivos = rf"""
            **Números vivos (a)**

            - $A = {lib.matriz_coloreada(A)}$; las flechas teal y rust son sus columnas: a dónde van $e_1$ y $e_2$
            - $x = {lib.vec_tex(x_pt)} \mapsto Ax = {lib.vec_tex(A @ x_pt)}$; la parcela va vértice por vértice con la misma cuenta
            - área con signo del cuadrado unitario después: ${lib.num_tex(np.linalg.det(A))}$ (lo que $A$ hace con la grilla)
            """
        elif _objeto == "(b)":
            _vivos = rf"""
            **Números vivos (b)**

            - $A = {lib.matriz_coloreada(A)}$, $w^T = {lib.pmat(w.reshape(1, 2), dec=0)}$, $w'^T = w^T A^{{-1}} = {lib.pmat(w_despues.reshape(1, 2))}$
            - cota del mojón: antes $w^T x = {lib.num_tex(w @ x_pt)}$, después $w'^T (Ax) = {lib.num_tex(w_despues @ (A @ x_pt))}$ → `np.allclose`: `{bool(np.allclose(w @ x_pt, w_despues @ (A @ x_pt)))}`
            - métrica del terreno en la grilla nueva: $G' = A^{{-T}} A^{{-1}} = {lib.pmat(g_despues)}$; la subida real $G'^{{-1}} w' = {lib.vec_tex(subida_despues)} = Aw$
            - ángulo entre $Aw$ (gold) y la marca: en el papel $\mathbf{{{ang_papel:.1f}°}}$; con $G'$, $\mathbf{{{ang_terreno:.1f}°}}$
            """
        else:
            _zx = z * complex(x_pt[0], x_pt[1])
            _vivos = rf"""
            **Números vivos (d)**

            - $z = {z.real:g} {'+' if z.imag >= 0 else '−'} {abs(z.imag):g}i$, $\lvert z\rvert = {abs(z):.3f}$, $\arg z = {np.degrees(np.angle(z)):.2f}°$; $M(z) = {lib.matriz_coloreada(Mz)}$, $\det M(z) = \lvert z\rvert^2 = {np.linalg.det(Mz):.3f}$
            - $x = 1 + 2i$: como complejo, $z \cdot x = {_zx.real:g} {'+' if _zx.imag >= 0 else '−'} {abs(_zx.imag):g}i$; como matriz, $M(z)\,x = {lib.vec_tex(Mz @ x_pt)}$ → `np.allclose`: `{bool(np.allclose(Mz @ x_pt, [_zx.real, _zx.imag]))}`
            - la columna teal es $M(z) e_1 = (a, b)$: el propio $z$ dibujado; la rust es $z \cdot i$, el mismo girado $90°$
            """
        _texto_caso = que_pasa if _objeto != "(d)" else r"la grilla gira $\arg z$ y se estira $\lvert z\rvert$, nada más: dos números, no cuatro. Las cizallas y proyecciones de (a) no son complejos."
        _selector = zeta if _objeto == "(d)" else caso
        _panel = mo.vstack([mo.md("**Controles**"), objeto_sel, _selector, mo.md(_vivos + "\n\n**Qué pasa acá:** " + _texto_caso)], gap=0.55)
    else:
        _tipo, _u, _v = parches[parche.value]
        r = loma3d if _tipo == "loma" else esfera3d
        _fu, _fv = _u[4], _v[4]
        uu, vv = u0.value * _fu, v0.value * _fv
        J = lib.jacobiana_numerica(r, uu, vv)
        E, F, G = lib.primera_forma(J)
        p = np.asarray(r(uu, vv), dtype=float)
        _us = np.linspace(_u[0], _u[1], 13) * _fu
        _vs = np.linspace(_v[0], _v[1], 13) * _fv
        _antes = (lambda u, v: lib.xyz(u, v, 0.0 * u)) if _tipo == "loma" else (lambda f_, l_: lib.xyz(0.9 * l_, 1.5 * f_, -2.9 + 0.0 * f_))
        figura = lib.figura_espacio(3.2, f"{objeto_sel.value} · E = {E:.3f} · F = {F:.3f} · G = {G:.3f}")
        lib.superficie_malla(figura, _antes, _us, _vs, lib.GRIS_ANTES, "grilla (u, v) antes: etiquetas", fino=2, ancho=1.5, opacidad=0.6)
        lib.superficie_malla(figura, r, _us, _vs, lib.TEAL_DESPUES, "grilla sobre el parche", opacidad=0.55)
        lib.plano_tangente(figura, p, J[:, 0], J[:, 1])
        figura.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", marker=dict(size=6, color=lib.VIOLETA_OBJETO), name="r(u₀, v₀)"))
        _panel = mo.vstack([mo.md("**Controles**"), objeto_sel, parche, u0, v0, mo.md(rf"""
            **Números vivos (c)** (radianes adentro)

            $$J = {lib.matriz_coloreada(J)}\ (3\times2), \qquad J^T J = {lib.pmat([[E, F], [F, G]])}$$

            - un paso $du = 1$ de la grilla mide $\sqrt{{E}} = {np.sqrt(E):.3f}$ sobre el parche; un paso $dv = 1$ mide $\sqrt{{G}} = {np.sqrt(G):.3f}$
            - ángulo entre los ejes locales $r_u$ y $r_v$: ${np.degrees(lib.angulo(J[:, 0], J[:, 1])):.1f}°$ ($F = 0$ si es recto)
            - el puente: derivar es esta matriz (ladrillos 1 y 3); $E, F, G$ es la métrica (ladrillo 5). Lo desarrolla [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html).
            """)], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return A, Mz, ang_papel, ang_terreno, g_despues, subida_despues, tangente_despues, w, w_despues, x_pt, z


@app.cell
def _(angulo_g, matriz_complejo, mo, np):
    A3 = np.diag([2.0, 1.0])
    w3 = np.array([1.0, 1.0])
    x3 = np.array([1.0, 2.0])
    w3_despues = w3 @ np.linalg.inv(A3)
    g3 = np.linalg.inv(A3).T @ np.linalg.inv(A3)
    t3 = A3 @ np.array([1.0, -1.0])
    z3, x3c = 1 + 1j, 2 + 1j
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, el cuaderno; derecha, numpy. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La cota no cambia (ladrillo 4).** $A = \mathrm{diag}(2, 1)$, $w^T = (1, 1)$, $x = (1, 2)$.

            $$w^T x = 1 + 2 = 3, \qquad Ax = \begin{pmatrix} \textcolor{#1b6f6a}{2} & \textcolor{#b5451b}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} \end{pmatrix}\binom12 = \binom22.$$

            $A^{-1} = \mathrm{diag}(\tfrac12, 1)$ y la fila va a la derecha:

            $$w^T A^{-1} = (1\cdot\tfrac12,\ 1\cdot1) = (\tfrac12, 1), \qquad (\tfrac12, 1)\binom22 = 1 + 2 = 3.\ \checkmark$$

            Lo que **no** hay que hacer: $Aw = (2, 1)$ como regla nueva: $(2, 1)\cdot(2, 2) = 6 \ne 3$.
            """),
            mo.vstack([
                mo.md("```python\nA = np.diag([2., 1.])\nw = np.array([1., 1.])\nx = np.array([1., 2.])\nw2 = w @ np.linalg.inv(A)\nnp.allclose(w @ x, w2 @ (A @ x))\n```"),
                mo.md(f"`w @ x` = `{w3 @ x3:g}` · `w2` = `{np.round(w3_despues, 3).tolist()}`  \n"
                      f"`w2 @ (A @ x)` = `{w3_despues @ (A3 @ x3):g}` · `allclose` = `{bool(np.allclose(w3 @ x3, w3_despues @ (A3 @ x3)))}`  \n"
                      f"mal: `(A @ w) @ (A @ x)` = `{(A3 @ w3) @ (A3 @ x3):g}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 El ángulo recto vive en el terreno (ladrillo 5).** En el terreno la marca de la regla $(1, 1)$ tiene
            dirección $(1, -1)$ y la subida $w = (1, 1)$: $\langle (1,1), (1,-1)\rangle = 0$, recto. Dibujados con $A$:
            la marca va a $A(1, -1) = (2, -1)$ y la subida a $Aw = (2, 1)$.

            En el papel: $\cos\theta = \dfrac{(2,1)\cdot(2,-1)}{\sqrt5\,\sqrt5} = \dfrac{3}{5}$, $\theta = 53.1°$.

            Con la métrica del terreno escrita en el papel, $G' = A^{-T}A^{-1} = \mathrm{diag}(\tfrac14, 1)$:

            $$(2, 1)\,G'\,\binom{2}{-1} = 2\cdot\tfrac14\cdot2 + 1\cdot1\cdot(-1) = 1 - 1 = 0 \ \Rightarrow\ \theta = 90°.\ \checkmark$$

            Y la subida es la forma levantada con $G'$: $G'^{-1} w' = \mathrm{diag}(4, 1)\binom{1/2}{1} = \binom21 = Aw$.
            La perpendicular del papel, $(\tfrac12, 1)$, es la regla $w^T A^{-1}$ leída como flecha: perpendicular con
            $G = I$, no con $G'$.
            """),
            mo.vstack([
                mo.md("```python\nAi = np.linalg.inv(A)\ng2 = Ai.T @ Ai\nsub = A @ w            # (2, 1)\nmarca = A @ [1., -1.]  # (2, -1)\ndef ang(a, b, g):\n    c = a @ g @ b\n    c /= np.sqrt((a@g@a)*(b@g@b))\n    return np.degrees(np.arccos(c))\nang(sub, marca, np.eye(2))\nang(sub, marca, g2)\nnp.linalg.solve(g2, w2)   # sube w2\n```"),
                mo.md(f"`g2` = `{np.round(g3, 3).tolist()}` · `sub` = `{(A3 @ w3).tolist()}` · `marca` = `{t3.tolist()}`  \n"
                      f"en el papel: `{angulo_g(A3 @ w3, t3, np.eye(2)):.1f}`° · con `g2`: `{angulo_g(A3 @ w3, t3, g3):.1f}`°  \n"
                      f"`solve(g2, w2)` = `{np.round(np.linalg.solve(g3, w3_despues), 3).tolist()}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 Un complejo es una matriz (ladrillo 2).** $z = 1 + i$, $x = 2 + i$.

            $$z \cdot x = (1 + i)(2 + i) = 2 + i + 2i + i^2 = 1 + 3i.$$

            $$M(z)\,x = \begin{pmatrix} \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{-1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{1} \end{pmatrix}\binom21 = \binom{2 - 1}{2 + 1} = \binom13.\ \checkmark$$

            $\lvert z\rvert = \sqrt2$, $\arg z = 45°$: $x$ giró $45°$ y se estiró $\sqrt2$ ($\lvert 1 + 3i\rvert = \sqrt{10} = \sqrt2\cdot\sqrt5$).
            """),
            mo.vstack([
                mo.md("```python\nz, x = 1 + 1j, 2 + 1j\nMz = np.array([[z.real, -z.imag],\n               [z.imag,  z.real]])\nz * x\nMz @ [x.real, x.imag]\nabs(z), np.degrees(np.angle(z))\n```"),
                mo.md(f"`z * x` = `{z3 * x3c}` · `Mz @ x` = `{(matriz_complejo(z3) @ [x3c.real, x3c.imag]).tolist()}`  \n"
                      f"`abs(z)` = `{abs(z3):.4f}` · `angle` = `{np.degrees(np.angle(z3)):g}`°"),
            ]),
        ], widths="equal", align="start"),
    ])
    return A3, g3, t3, w3, w3_despues, x3


@app.cell
def _(lib, loma3d, mo, np):
    _A = np.array([[2.0, 1.0], [0.0, 1.0]])
    _w = np.array([1.0, 1.0])
    _J = lib.jacobiana_numerica(loma3d, 2.0, 1.0)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Cuatro reflejos. **`eye`, `inv`, `solve` son el neutro y la inversa del ladrillo 1**: `np.eye(2)` es el
        neutro; `np.linalg.inv(A)` arma la inversa entera; `np.linalg.solve(A, y)` aplica la inversa a un solo dato sin
        armarla (más rápido y más estable). **numpy no distingue fila de columna**: `np.array([1., 1.])` es un punto si
        va a la derecha (`A @ x`) y una forma si va a la izquierda (`w @ A`); la diferencia la ponemos nosotros con el lado.
        **Una forma se arrastra con `solve(A.T, w)`**, que es `w @ inv(A)` sin invertir. **El jacobiano se calcula**:
        `lib.jacobiana_numerica(r, u, v)` evalúa $r$ en $u \pm h$, $v \pm h$ y apila las dos columnas; `J.T @ J` es
        la tabla $E, F, G$.
        """),
        mo.md("```python\nA = np.array([[2., 1.], [0., 1.]])\nw = np.array([1., 1.])\nnp.linalg.solve(A, [3., 1.])   # A⁻¹ (3, 1)\nw @ np.linalg.inv(A)           # la regla\nnp.linalg.solve(A.T, w)        # lo mismo\nJ = lib.jacobiana_numerica(loma3d, 2., 1.)\nJ.shape, J.T @ J               # [[E, F], [F, G]]\n```"),
        mo.md(f"`solve(A, [3, 1])` = `{np.round(np.linalg.solve(_A, [3.0, 1.0]), 3).tolist()}` · `w @ inv(A)` = `{np.round(_w @ np.linalg.inv(_A), 3).tolist()}` · "
              f"`solve(A.T, w)` = `{np.round(np.linalg.solve(_A.T, _w), 3).tolist()}` · `J.shape` = `{_J.shape}` · `J.T @ J` =\n```\n{np.round(_J.T @ _J, 3)}\n```"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("las matrices y las transformaciones lineales tienen una correspondencia 1 a 1").*
        La cota es $h = 3x + y$ (regla $w^T = (3, 1)$) y el plano se dibuja con el **Norte** estirado por 2:
        $A = \mathrm{diag}(1, 2)$. El mojón está en $x = (2, 1)$. Calculá la cota, el mojón dibujado $Ax$, la regla
        arrastrada $w^T A^{-1}$ y comprobá que lee la misma cota. Después decidí: la flecha $(3, 1)$ dibujada en el
        papel, ¿es la subida más empinada del terreno?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $w^T x = 6 + 1 = 7$. $Ax = (2, 2)$. $A^{-1} = \mathrm{diag}(1, \tfrac12)$, así que $w^T A^{-1} = (3, \tfrac12)$, y
        $(3, \tfrac12)\cdot(2, 2) = 6 + 1 = 7$. ✓ La subida más empinada del terreno es $w = (3, 1)$ **en metros**; dibujada
        con el Norte por 2 es $Aw = (3, 2)$. La flecha $(3, 1)$ puesta tal cual en el papel es, en el terreno, el
        desplazamiento $(3, \tfrac12)$: no es la subida más empinada. Ladrillo 3 (flecha = desplazamiento), 4 (la regla
        se arrastra al revés) y 5 (la grilla no mide metros).
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_e1 = mo.ui.code_editor(
        value="def matriz_complejo(z):\n    # z: un complejo de Python (a + bj)\n    a, b = z.real, z.imag\n    return np.array(...)   # la 2x2 que hace lo mismo que z sobre el plano\n",
        language="python", min_height=120, label="ejercicio E1",
    )
    mo.vstack([
        mo.md(r"""
        **E1. Código con hueco — elemental** *("hay una equivalencia entre operaciones en $\mathbb C$ y en $\mathbb R^2$").*
        Completá `matriz_complejo(z)`: la matriz $2\times2$ que hace sobre $(x, y)$ lo mismo que $z$ sobre $x + iy$.
        Tenés `np`. Se verifica que $M(z)\,e_1 = (a, b)$ y que $M$ respeta la suma, el producto y el inverso sobre diez
        pares de complejos al azar: $M(z_1 + z_2) = M(z_1) + M(z_2)$, $M(z_1 z_2) = M(z_1)M(z_2)$, $M(1/z) = M(z)^{-1}$.
        """),
        editor_e1,
    ])
    return (editor_e1,)


@app.cell
def _(editor_e1, matriz_complejo, mo, np):
    _rng = np.random.default_rng(56798)
    _zs = [1j, 1.0 + 1j] + [complex(*_rng.uniform(-3, 3, 2)) for _ in range(10)]
    _pares = list(zip(_zs[:-1], _zs[1:]))
    _ns = {"np": np}
    try:
        exec(editor_e1.value, _ns)
        _M = lambda z: np.asarray(_ns["matriz_complejo"](z), dtype=float)
        _formas = {_M(z).shape for z in _zs}
        if _formas != {(2, 2)}:
            _res = mo.callout(mo.md(f"❌ devolvés algo de forma `{sorted(_formas)}`; tiene que ser una matriz `(2, 2)`."), kind="danger")
        elif all(np.allclose(_M(z), matriz_complejo(z)) for z in _zs):
            _ok_suma = all(np.allclose(_M(z1 + z2), _M(z1) + _M(z2)) for z1, z2 in _pares)
            _ok_prod = all(np.allclose(_M(z1 * z2), _M(z1) @ _M(z2)) for z1, z2 in _pares)
            _ok_inv = all(np.allclose(_M(1 / z), np.linalg.inv(_M(z))) for z in _zs)
            _res = mo.callout(mo.md(f"✅ coincide. Suma `{_ok_suma}`, producto `{_ok_prod}`, inverso `{_ok_inv}` en los 12 complejos: las matrices $\\begin{{pmatrix}} a & -b \\\\ b & a\\end{{pmatrix}}$ **son** $\\mathbb C$, y multiplicar por $z$ rota $\\arg z$ y escala $\\lvert z\\rvert$."), kind="success")
        elif all(np.allclose(_M(z), matriz_complejo(z).T) for z in _zs):
            _res = mo.callout(mo.md(r"❌ eso es $M(\bar z)$, la **transpuesta**: rota al revés. $M(z) e_1$ tiene que ser el propio $z = (a, b)$: la primera **columna** es $(a, b)$, así que el $-b$ va arriba a la derecha."), kind="warn")
        elif all(np.allclose(_M(z), np.array([[z.real, z.imag], [z.imag, z.real]])) for z in _zs):
            _res = mo.callout(mo.md(r"❌ `[[a, b], [b, a]]` es simétrica: respeta la suma pero no el producto (probá $z = i$: $M(i)^2$ tendría que ser $M(-1) = -I$). Hace falta el signo: `[[a, -b], [b, a]]`."), kind="warn")
        elif all(np.allclose(_M(z1 + z2), _M(z1) + _M(z2)) for z1, z2 in _pares):
            _res = mo.callout(mo.md(r"❌ respeta la suma (es lineal en $a, b$) pero no el producto: $M(i)^2$ tiene que dar $-I$ y $M(z) e_1 = (a, b)$. Revisá dónde van $a$, $b$ y el signo."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para `z = 1+1j` se esperaba `{matriz_complejo(1 + 1j).tolist()}` y se obtuvo `{np.round(_M(1 + 1j), 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_e2 = mo.ui.code_editor(
        value="def arrastrar_punto_y_forma(A, x, w):\n    # A: 2x2 que mueve los puntos; x: punto (columna); w: forma (fila)\n    x2 = ...   # el punto movido\n    w2 = ...   # la forma arrastrada, sin armar la inversa entera\n    return x2, w2\n",
        language="python", min_height=140, label="ejercicio E2",
    )
    mo.vstack([
        mo.md(r"""
        **E2. Código con hueco — medio** *("una forma lineal se transforma con una transformación lineal del lado
        'contrario' que un vector").* Completá `arrastrar_punto_y_forma(A, x, w)`: devuelve el par `(x2, w2)` con el
        punto movido y la regla arrastrada, de modo que la lectura no cambie: `w2 @ x2 == w @ x`. Tenés `np`; usá
        `np.linalg.solve` en vez de `inv`. Se verifica sobre $A = \mathrm{diag}(2, 1)$ y diez matrices al azar con
        $\det \ne 0$, y se chequea la invariancia de la cota en cada caso.
        """),
        editor_e2,
    ])
    return (editor_e2,)


@app.cell
def _(editor_e2, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _casos = [(np.diag([2.0, 1.0]), np.array([1.0, 2.0]), np.array([1.0, 1.0]))]
    while len(_casos) < 11:
        _M = _rng.uniform(-3, 3, (2, 2))
        if abs(np.linalg.det(_M)) > 0.5:
            _casos.append((_M, _rng.uniform(-3, 3, 2), _rng.uniform(-3, 3, 2)))
    _ns = {"np": np}
    try:
        exec(editor_e2.value, _ns)
        _sal = [_ns["arrastrar_punto_y_forma"](A.copy(), x.copy(), w.copy()) for A, x, w in _casos]
        _x2 = np.array([np.asarray(s[0], dtype=float).reshape(-1) for s in _sal])
        _w2 = np.array([np.asarray(s[1], dtype=float).reshape(-1) for s in _sal])
        _x_ok = np.array([A @ x for A, x, w in _casos])
        _w_ok = np.array([lib.forma_transformada(w, A) for A, x, w in _casos])
        if _x2.shape != _x_ok.shape or _w2.shape != _w_ok.shape:
            _res = mo.callout(mo.md(f"❌ las formas son `{_x2.shape[1:]}` y `{_w2.shape[1:]}`; las dos tienen que ser `(2,)`."), kind="danger")
        elif not np.allclose(_x2, _x_ok):
            _res = mo.callout(mo.md(r"❌ el punto no está bien movido: un punto va con $A$ **por la izquierda**, `A @ x` (ladrillo 3)."), kind="warn")
        elif np.allclose(_w2, _w_ok):
            _lect = np.array([[w @ x, w2 @ x2] for (A, x, w), w2, x2 in zip(_casos, _w2, _x2)])
            _res = mo.callout(mo.md(f"✅ coincide en los 11 casos y la cota se conserva: `allclose(w @ x, w2 @ x2)` = `{bool(np.allclose(_lect[:, 0], _lect[:, 1]))}`. Punto con $A$, forma con $A^{{-1}}$ **a la derecha**: 'convertimos todo para que nada cambie'."), kind="success")
        elif np.allclose(_w2, [A @ w for A, x, w in _casos]):
            _res = mo.callout(mo.md(r"❌ `A @ w`: moviste la fila como si fuera un punto. La regla va con la **inversa** y a la **derecha**: `np.linalg.solve(A.T, w)` (que es `w @ inv(A)`)."), kind="warn")
        elif np.allclose(_w2, [w @ A for A, x, w in _casos]):
            _res = mo.callout(mo.md(r"❌ `w @ A` (o `A.T @ w`): el lado es correcto pero falta invertir; esa regla lee sobre el $x$ original. Para arrastrarla: `np.linalg.solve(A.T, w)`."), kind="warn")
        elif np.allclose(_w2, [np.linalg.solve(A, w) for A, x, w in _casos]):
            _res = mo.callout(mo.md(r"❌ `solve(A, w)` es `inv(A) @ w`: la inversa está, pero del lado de la columna ($A^{-1}w$ en vez de $wA^{-1}$). La fila va a la derecha: `solve(A.T, w)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ el punto está bien pero la forma no. Para `A = diag(2, 1)`, `w = [1, 1]` se esperaba `{_w_ok[0].tolist()}` y se obtuvo `{np.round(_w2[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_e3 = mo.ui.code_editor(
        value="def angulo_g(a, b, g):\n    # a, b: arrays de 2; g: matriz 2x2 de la metrica\n    cos = ...          # a g b / sqrt((a g a)(b g b))\n    return ...         # en grados\n\ndef subida_metrica(w, g):\n    # w: la forma (fila); g: la metrica de la grilla\n    return ...         # el v con g v = w\n",
        language="python", min_height=170, label="ejercicio E3",
    )
    mo.vstack([
        mo.md(r"""
        **E3. Código con hueco — avanzado** *("lo único que define a la base que llamamos canónica es que sobre ella
        tenemos definida la noción de distancia a través del producto interno").* Completá las dos funciones del
        ladrillo 5: `angulo_g(a, b, g)`, el ángulo **en grados** entre `a` y `b` medido con la métrica `g`, y
        `subida_metrica(w, g)`, la forma `w` levantada a vector con `g` (el $v$ que cumple $g\,v = w$: el puente entre
        la forma gradiente y la dirección de máxima pendiente en el terreno). Tenés `np`. Se verifica sobre
        $G' = \mathrm{diag}(\tfrac14, 1)$ y diez métricas al azar; con `g = I` el ángulo es el de siempre y la subida es
        la fila transpuesta.
        """),
        editor_e3,
    ])
    return (editor_e3,)


@app.cell
def _(angulo_g, editor_e3, mo, np, subida_metrica):
    _rng = np.random.default_rng(56798)
    _casos = [(np.array([2.0, 1.0]), np.array([2.0, -1.0]), np.diag([0.25, 1.0]), np.array([0.5, 1.0]))]
    while len(_casos) < 11:
        _B = _rng.uniform(-2, 2, (2, 2))
        _g = _B.T @ _B + 0.5 * np.eye(2)  # simétrica definida positiva
        _casos.append((_rng.uniform(-3, 3, 2), _rng.uniform(-3, 3, 2), _g, _rng.uniform(-3, 3, 2)))
    _ang_ok = np.array([angulo_g(a, b, g) for a, b, g, w in _casos])
    _sub_ok = np.array([subida_metrica(w, g) for a, b, g, w in _casos])
    _ns = {"np": np}
    try:
        exec(editor_e3.value, _ns)
        _ang = np.array([float(_ns["angulo_g"](a.copy(), b.copy(), g.copy())) for a, b, g, w in _casos])
        if np.allclose(_ang, [angulo_g(a, b, np.eye(2)) for a, b, g, w in _casos], atol=1e-6):
            _res = mo.callout(mo.md(r"❌ `angulo_g`: ese es el ángulo con $g = I$, olvidaste la métrica. El producto interno es `a @ g @ b` y los largos `np.sqrt(a @ g @ a)`."), kind="warn")
        elif np.allclose(_ang, np.radians(_ang_ok), atol=1e-6):
            _res = mo.callout(mo.md("❌ `angulo_g` está en radianes: falta `np.degrees(...)`."), kind="warn")
        elif not np.allclose(_ang, _ang_ok, atol=1e-6):
            _res = mo.callout(mo.md(f"❌ `angulo_g` no coincide. Para `a = [2, 1]`, `b = [2, -1]`, `g = diag(1/4, 1)` se esperaba `{_ang_ok[0]:.1f}` y se obtuvo `{_ang[0]:.3f}`."), kind="danger")
        else:
            _sub = np.array([np.asarray(_ns["subida_metrica"](w.copy(), g.copy()), dtype=float).reshape(-1) for a, b, g, w in _casos])
            if _sub.shape != _sub_ok.shape:
                _res = mo.callout(mo.md(f"❌ `subida_metrica` devuelve algo de forma `{_sub.shape[1:]}`; tiene que ser un vector `(2,)`."), kind="danger")
            elif np.allclose(_sub, _sub_ok):
                _res = mo.callout(mo.md(f"✅ las dos coinciden en los 11 casos. Con $G'$ el ángulo de la sección 3 da `{_ang[0]:.1f}`°, y la forma $w' = (\\tfrac12, 1)$ sube a `{np.round(_sub[0], 3).tolist()}` $= Aw$: la flecha gold de la sección 2. El ángulo y la subida son preguntas a la métrica."), kind="success")
            elif np.allclose(_sub, [w for a, b, g, w in _casos]):
                _res = mo.callout(mo.md(r"❌ `subida_metrica` devuelve `w` tal cual: es la fila puesta como flecha, perpendicular **en el papel** ($g = I$). Para subirla con la métrica hay que resolver $g\,v = w$: `np.linalg.solve(g, w)`."), kind="warn")
            elif np.allclose(_sub, [g @ w for a, b, g, w in _casos]):
                _res = mo.callout(mo.md(r"❌ `g @ w` va al revés: $g$ **baja** un vector a forma. Para **subir** una forma a vector hace falta $g^{-1}$: `np.linalg.solve(g, w)`."), kind="warn")
            else:
                _res = mo.callout(mo.md(f"❌ `angulo_g` bien, `subida_metrica` no. Para `w = [1/2, 1]`, `g = diag(1/4, 1)` se esperaba `{_sub_ok[0].tolist()}` y se obtuvo `{np.round(_sub[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ### Autoevaluación: seis preguntas sobre esta unidad

    Dos elementales, dos medias y dos avanzadas, con las opciones en un orden distinto cada vez. Respondemos cada una
    y leemos la explicación: la corrección aparece abajo a medida que elegimos. El botón vuelve a barajar preguntas y
    respuestas, para repasar sin memorizar la letra.
    """)
    return


@app.cell
def _(mo):
    mezclar = mo.ui.button(label="🔀 Mezclar preguntas y orden de respuestas", value=0, on_click=lambda v: v + 1)
    mezclar
    return (mezclar,)


@app.cell
def _(lib, mezclar, mo):
    _vez = mezclar.value  # al apretar el botón esta celda vuelve a correr y baraja de nuevo
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "00_desaprender_el_cbc")
    mo.vstack(respuestas_radio.elements, gap=1.0)
    return preguntas_tanda, respuestas_radio


@app.cell
def _(lib, mo, preguntas_tanda, respuestas_radio):
    lib.corregir_autoevaluacion(mo, preguntas_tanda, respuestas_radio)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    En esta unidad presentamos los cinco ladrillos con un ejemplo cada uno. Lo que los sostiene:

    - [apunte, «Cómo leer este apunte» (cómo leer, los cinco ladrillos)](../../apunte.pdf#nameddest=cap:00) ·
      [apunte, «La mirada geométrica»](../../apunte.pdf#nameddest=cap:03) ·
      [apunte, «El punto y sus coordenadas no son lo mismo»](../../apunte.pdf#nameddest=cap:04)
    - [ficha de la clase 1](../../clases/01.html) · [ficha de la clase 4](../../clases/04.html) ·
      [ficha de la clase 9](../../clases/09.html) · [el hilo conductor](../../index.html)

    Dónde vuelve cada ladrillo: el 1 en [Rotaciones I](../01a_punto_quieto/index.html) y
    [Rotaciones III](../01c_rotaciones_3d/index.html); el 2 en [Rotaciones II](../01b_rotacion_plano/index.html); el 3
    en [Afines](../04_afines_homogeneas/index.html); el 4 en [Formas lineales y dualidad](../06_formas_lineales/index.html); el 5 en
    [Producto interno](../02_producto_interno/index.html) y [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html);
    el puente al cálculo en esa misma y en [Curvatura](../12_curvatura/index.html).

    **Lo que viene:** [Rotaciones I — el punto no se movió](../01a_punto_quieto/index.html): el mismo mojón, dos
    sistemas de ejes, y la primera matriz recién al final.
    """)
    return


@app.cell
def _(A, A3, A_plano, Mz, ang_papel, ang_terreno, angulo_g, bajada, candidatos, esfera3d, g3, g_despues, lib, loma3d, matriz_complejo, mo, mojon, np, subida_despues, subida_metrica, t3, tangente_despues, w, w3, w3_despues, w_despues, w_mojon, x3, x_pt, z):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _ok = lib.exacto
    _J = lib.jacobiana_numerica(esfera3d, np.deg2rad(45), 0.0)
    _z1, _z2 = 1.0 + 1j, 2.0 - 0.5j
    _Rx, _Rz = lib.rot_x(np.deg2rad(90)), lib.rot_z(np.deg2rad(90))
    _checks = [
        ("predicción: cuatro candidatos distintos; gradiente (−1, −1), bajada (1, 1); ingenua (1, 1), ⊥ papel (1, 2), correcta (2, 1), curva (2, −1)",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4 and _ok(w_mojon, [-1, -1]) and _ok(bajada, [1, 1])
         and _ok(candidatos["ingenua"], [1, 1]) and _ok(candidatos["perp-dibujo"], [1, 2]) and _ok(candidatos["correcta"], [2, 1]) and _ok(candidatos["curva"], [2, -1])),
        ("la bajada dibujada es perpendicular a la curva dibujada con la métrica del terreno, no con la del papel",
         _ok(angulo_g(candidatos["correcta"], candidatos["curva"], np.linalg.inv(A_plano).T @ np.linalg.inv(A_plano)), 90.0, tol=1e-6)
         and not _ok(angulo_g(candidatos["correcta"], candidatos["curva"], np.eye(2)), 90.0, tol=1.0) and _ok(A_plano @ mojon, [4, 2])),
        ("ladrillo 1: las rotaciones del plano conmutan y las de R³ no; eye es neutro y solve deshace",
         _ok(lib.rot2(0.3) @ lib.rot2(0.8), lib.rot2(0.8) @ lib.rot2(0.3)) and not _ok(_Rx @ _Rz, _Rz @ _Rx, tol=1e-6)
         and _ok(np.eye(3) @ _Rx, _Rx) and _ok(np.linalg.solve(A3, A3 @ x3), x3)),
        ("ladrillo 2: M(z) respeta suma, producto e inverso; M(i)² = −I; det M(z) = |z|²",
         _ok(matriz_complejo(_z1 + _z2), matriz_complejo(_z1) + matriz_complejo(_z2)) and _ok(matriz_complejo(_z1 * _z2), matriz_complejo(_z1) @ matriz_complejo(_z2))
         and _ok(matriz_complejo(1 / _z2), np.linalg.inv(matriz_complejo(_z2))) and _ok(matriz_complejo(1j) @ matriz_complejo(1j), -np.eye(2))
         and _ok(np.linalg.det(Mz), abs(z) ** 2) and _ok(matriz_complejo(1 + 1j) @ [2, 1], [1, 3])),
        ("ladrillo 3: una transformación lineal manda el 0 al 0; la traslación no",
         _ok(A @ np.zeros(2), np.zeros(2)) and not _ok(np.zeros(2) + np.array([1.0, 0.0]), np.zeros(2))),
        ("sección 2: la cota del mojón se conserva con la regla arrastrada; G' = A⁻ᵀA⁻¹; Aw ⊥ marca con G' (90°); G'⁻¹ w' = Aw",
         _ok(w_despues @ (A @ x_pt), w @ x_pt) and _ok(w_despues, lib.forma_transformada(w, A)) and _ok(g_despues, np.linalg.inv(A).T @ np.linalg.inv(A))
         and _ok(tangente_despues, A @ lib.perp2(w)) and _ok(ang_terreno, 90.0, tol=1e-6) and 0.0 <= ang_papel <= 90.0 + 1e-9
         and _ok(subida_despues, A @ w, tol=1e-9)),
        ("3.1: (1, 1) diag(2, 1)⁻¹ = (1/2, 1) y lee 3 sobre (2, 2); (Aw)·(Ax) = 6",
         _ok(w3_despues, [0.5, 1]) and _ok(w3_despues @ (A3 @ x3), 3) and _ok((A3 @ w3) @ (A3 @ x3), 6)),
        ("3.2: G' = diag(1/4, 1); ángulo en el papel 53.13°, con G' 90°; solve(G', w') = (2, 1)",
         _ok(g3, np.diag([0.25, 1.0])) and _ok(angulo_g(A3 @ w3, t3, np.eye(2)), np.degrees(np.arccos(0.6)), tol=1e-9) and _ok(angulo_g(A3 @ w3, t3, g3), 90.0, tol=1e-9)
         and _ok(subida_metrica(w3_despues, g3), [2, 1])),
        ("la esfera a 45°: E = 4, F = 0, G = 2; la loma en la cima: J = [[1,0],[0,1],[0,0]]",
         _ok(lib.primera_forma(_J), [4, 0, 2], tol=1e-5) and _ok(lib.jacobiana_numerica(loma3d, 0.0, 0.0), [[1, 0], [0, 1], [0, 0]], tol=1e-5)),
        ("ejercicio (a): w x = 7, A x = (2, 2), w A⁻¹ = (3, 1/2) lee 7, A w = (3, 2)",
         _ok(np.array([3, 1]) @ [2, 1], 7) and _ok(np.diag([1, 2]) @ [2, 1], [2, 2]) and _ok(lib.forma_transformada([3, 1], np.diag([1, 2])), [3, 0.5])
         and _ok(lib.forma_transformada([3, 1], np.diag([1, 2])) @ [2, 2], 7) and _ok(np.diag([1, 2]) @ [3, 1], [3, 2])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
