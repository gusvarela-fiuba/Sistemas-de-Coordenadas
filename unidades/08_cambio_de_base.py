# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Cambio de base y diagonalización (unidad 08, molde v2 sobre cb104).
Una sola idea: los autovectores son los ejes propios del sistema. La flecha no se movió; cambiamos la grilla con que la
medimos y los números cambian por B (columnas = ejes nuevos escritos en los viejos; coordenadas nuevas = B⁻¹ p). En la
grilla de los autovectores una transformación es sólo estirar por λ en cada eje (A = B Λ B⁻¹) y Aⁿ sale sola.
Generaliza a una base oblicua lo que Rotaciones I (01a) mostró con una base girada.

Chequear:  uv run marimo check --select MW unidades/08_cambio_de_base.py
Exportar:  uv run python tools/build.py --only 08_cambio_de_base
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
    # Cambio de base y diagonalización

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    La pregunta: **Si la flecha no se movió pero cambiamos la grilla, ¿cómo cambian los números, y
    en qué grilla una transformación es sólo estirar?** El gancho: *el mismo mojón con coordenadas en tres marcos:
    cambia la grilla con que se mide, no el punto.*

    Colores, iguales en la figura y en el álgebra: la **primera columna** de una matriz es
    <span style="color:#1b6f6a">**teal**</span> y la **segunda** <span style="color:#b5451b">**rust**</span>. Acá la
    matriz que importa es $B$, la de cambio de base: sus columnas $b_1$ y $b_2$ son los **ejes nuevos** dibujados en la
    grilla vieja (gris). El mojón va en <span style="color:#7a4e9e">**violeta**</span>. En
    [Rotaciones I](../01a_punto_quieto/index.html) los ejes nuevos eran los viejos girados; acá son dos direcciones
    cualesquiera, y la cuenta con la transpuesta ya no alcanza.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("08_cambio_de_base"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    b1_parcela, b2_parcela = np.array([3.0, 1.0]), np.array([1.0, 2.0])
    B_parcela = np.column_stack([b1_parcela, b2_parcela])
    mojon = np.array([4.0, 3.0])
    candidatos = {
        "correcta": lib.coordenadas_en_base(mojon, B_parcela),  # resuelve B c = p
        "proyeccion": np.array([mojon @ b1_parcela / (b1_parcela @ b1_parcela), mojon @ b2_parcela / (b2_parcela @ b2_parcela)]),
        "por-B": B_parcela @ mojon,  # multiplicar en vez de resolver
        "mismas": mojon.copy(),
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({lib.vec_plano(candidatos[k]) + ("  (las mismas)" if k == "mismas" else ""): k
                 for k in ("proyeccion", "mismas", "correcta", "por-B")}),
        value=None,
        label=r"**Predicción.** Con $b_1 = (3, 1)$ y $b_2 = (1, 2)$ como ejes, las coordenadas del mojón $P = (4, 3)$ son…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        El mismo mojón de Rotaciones I: en la grilla de la obra, $P = (4, 3)$ metros. Pero la parcela no está alineada
        con la obra: su **frente** sigue el rumbo $b_1 = (3, 1)$ y su **lado** el rumbo $b_2 = (1, 2)$, los dos en
        metros de la obra, y forman $45°$, no $90°$. Quien mide la parcela mide **en frentes y lados**: cuántas veces
        $b_1$ y cuántas veces $b_2$ hay que avanzar para llegar al mojón. El hierro no se tocó; cambia la etiqueta.
        """),
        prediccion,
    ])
    return B_parcela, b1_parcela, b2_parcela, candidatos, mojon, prediccion


@app.cell
def _(candidatos, lib, mo, prediccion):
    _pr, _pb = lib.vec_tex(candidatos["proyeccion"]), lib.vec_tex(candidatos["por-B"])
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Un frente más un lado: $1\,b_1 + 1\,b_2 = (3,1) + (1,2) = (4,3)$. Las coordenadas nuevas son el $c$ "
                     r"que **resuelve** $Bc = p$, con $B$ la matriz que tiene a $b_1$ y $b_2$ como columnas: $c = B^{-1}p$. "
                     r"Abajo lo mostramos con la grilla y el camino de lectura."),
        "proyeccion": ("warn",
                       rf"**No.** ${_pr}$ sale de proyectar $P$ sobre cada eje con el producto interno, "
                       r"$\langle P, b_k\rangle / \langle b_k, b_k\rangle$. Valió en Rotaciones I porque los ejes girados seguían "
                       r"perpendiculares; a $45°$ cada proyección arrastra parte de la otra. Controlá: $1.5\,b_1 + 2\,b_2 = (6.5,\ 5.5) \ne P$."),
        "por-B": ("warn",
                  rf"**No.** ${_pb}$ es $B\,P$: multiplicaste por $B$, que lleva de coordenadas **nuevas a viejas** "
                  r"($p = Bc$: tantos $b_1$ más tantos $b_2$). Para ir al revés hay que resolver $Bc = p$, o sea $B^{-1}$."),
        "mismas": ("warn",
                   rf"**No.** El mojón no se movió, pero una coordenada es un número **respecto de unos ejes**. Con ejes de otro "
                   rf"largo y otra dirección los números cambian: $(4, 3)$ frentes y lados sería el punto $4b_1 + 3b_2 = {_pb}$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** El punto, y con él toda la geometría: distancias, ángulos, qué punto está en qué recta, a
    dónde lleva cada transformación a cada punto. Lo que cambia son los **números**. Convertimos todo para que nada
    cambie. No hay base privilegiada: la canónica sólo es especial porque en ella el producto
    interno es $x_1x_2 + y_1y_2$.

    **La matriz de cambio de base.** Si los ejes nuevos $b_1, b_2$ (escritos en la grilla vieja) son las columnas de
    $B$, el punto de coordenadas nuevas $c$ es

    $$p = c_1\,\textcolor{#1b6f6a}{b_1} + c_2\,\textcolor{#b5451b}{b_2} = B\,c, \qquad c = B^{-1}p.$$

    $B$ lleva de nuevas a viejas; $B^{-1}$, de viejas a nuevas. Para leer hay que **resolver**, no multiplicar. Sólo
    con ejes perpendiculares de largo $1$ vale $B^{-1} = B^T$ y resolver es proyectar: eso fue Rotaciones I.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $B = (u)$, un número: la unidad nueva. $c = p/u$ (metros a pies: $u = 0.3048$) | la misma longitud, otro número |
    | $\mathbb R^2$ | $B$ $2\times2$ con columnas $b_1, b_2$; $c = B^{-1}p$ | la misma flecha medida con una grilla oblicua |
    | $\mathbb R^3$ | $B$ $3\times3$, tres columnas | lo mismo con tres direcciones |

    **Una transformación vista en otra base.** Si $A$ actúa en la grilla vieja, en la grilla de $B$ la misma
    transformación se escribe $A' = B^{-1} A\, B$: convertir a la vieja, aplicar $A$, volver a la nueva (la de la
    derecha actúa primero). Misma transformación, otros números; no cambian $\det$, traza ni autovalores.

    **Diagonalizar.** Si las columnas de $B$ son los **autovectores** de $A$ ($A\,b_k = \lambda_k b_k$), cada $A\,b_k$
    leído en la grilla nueva es $\lambda_k e_k$: $B^{-1}AB = \Lambda = \mathrm{diag}(\lambda_1, \lambda_2)$. En su
    grilla propia $A$ **sólo estira** cada eje por su autovalor, sin romper la grilla. Entonces $A = B\Lambda B^{-1}$ y

    $$A^n = (B\Lambda B^{-1})(B\Lambda B^{-1})\cdots = B\,\Lambda^n B^{-1},$$

    porque los $B^{-1}B$ del medio se cancelan: aplicar $n$ veces es estirar $n$ veces cada eje propio. Con $t$ real,
    $A^t = B\Lambda^tB^{-1}$ convierte la transformación en una película.

    Escalera: en $\mathbb R$ toda matriz ya es diagonal; en $\mathbb R^2$ hacen falta dos ejes propios reales e
    independientes: una rotación no tiene ninguno y una cizalla tiene uno solo, y ninguna se diagonaliza (la SVD,
    unidad 09, la esquiva con dos bases distintas). El argumento general cabe en una línea, columna por columna:
    $A\,b_k = \lambda_k b_k$ para cada $k$ es lo mismo que $AB = B\Lambda$, y si las columnas son independientes
    $B$ se invierte y queda $B^{-1}AB = \Lambda$. Otra notación habitual escribe $T = A\,D\,A^{-1}$ con $A$ = autovectores en columnas; acá
    esa matriz es $B$, para no confundirla con la transformación.
    """)
    return


@app.cell
def _(mo):
    mo.callout(mo.md(r"""
    **La matriz de cambio de base y el despeje de la diagonalización.**

    En este recuadro seguimos esa otra notación: $A = [\,v_1 \mid v_2\,]$ es la matriz de cambio de base (la $B$ del resto de la unidad) y la transformación se llama $T$. Fuera del recuadro, $A$ es la transformación y $B$ el cambio de base.

    **(1) Quién se transforma con qué.** El diagrama de conmutatividad, escrito en orden de aplicación:

    $$(P)\to(A)\to[\,A^{-1}\to T\to A\,]\to(A^{-1})\to(\ell).$$

    Los puntos se transforman con $A$ y las formas (las rectas) con $A^{-1}$, para que la incidencia $\ell\,P = 0$
    siga dando cero. Con el sentido que fija la definición de (2), $A$ de la base de autovectores a la canónica, la
    caja del medio recibe coordenadas canónicas y devuelve coordenadas canónicas: el $T$ de adentro es la diagonal
    $T_{\text{diag}}$ (actúa en la base de autovectores) y la caja entera, leída como producto (lo que se aplica
    último va a la izquierda), es $A\,T_{\text{diag}}\,A^{-1} = T_{\text{can}}$, la misma transformación escrita en
    la base vieja. La diagonal $T_{\text{diag}} = A^{-1}\,T_{\text{can}}\,A$ es lo que queda adentro cuando la
    despejamos en (3).

    **(2) Los autovectores en columnas.** Definimos $A = [\,v_1 \mid v_2\,]$ con los autovectores como columnas y lo
    probamos con el vector $(1, 0)^T$: $A\,(1, 0)^T$ devuelve la primera columna, $v_1$, escrita en canónica. Entra un
    vector en **base de autovectores** (una unidad de $v_1$, nada de $v_2$) y sale el mismo vector en **base
    canónica**: $A$ traduce de la base de autovectores a la canónica, y $A^{-1}$ de la canónica a la de autovectores.
    Es la $B$ de esta lección. Ejemplo: el punto $(1, 1) = 1\,e_x + 1\,e_y$ pasa con $A^{-1}$ a coordenadas
    $(c_1, c_2)$ en la base de autovectores, $(1, 1) = c_1 v_1 + c_2 v_2$. Ahí la transformación es diagonal: cada
    coordenada se multiplica por su autovalor, $(c_1, c_2) \mapsto (\lambda_1 c_1,\ \lambda_2 c_2)$. Después $A$
    devuelve el resultado a la canónica: $\lambda_1 c_1 v_1 + \lambda_2 c_2 v_2$, otra vez en $e_x, e_y$.

    **(3) El camino en tres pasos y el despeje.** Lo de (2) dice que, con $A$ de autovectores a canónica,

    $$T_{\text{can}} = A\,T_{\text{diag}}\,A^{-1},$$

    leída de derecha a izquierda: entrar con $A^{-1}$, estirar con $T_{\text{diag}}$, salir con $A$. Para despejar la
    diagonal multiplicamos por $A^{-1}$ a la izquierda y por $A$ a la derecha,

    $$A^{-1}\,T_{\text{can}}\,A = A^{-1}A\;T_{\text{diag}}\;A\,A^{-1} = T_{\text{diag}},$$

    porque los dos pares $A^{-1}A = I$ y $A\,A^{-1} = I$ se cancelan. Es la misma cuenta que $B^{-1}AB = \Lambda$ de
    arriba, con el nombre $A$ en el lugar de $B$ y $T$ en el lugar de $A$.
    """), kind="info")
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("03_cambio_de_base_viaje", "Recorremos las tres etapas de T = A·T_diag·A⁻¹ y las deshacemos: leemos p en la base de autovectores, estiramos cada dirección propia (λ₁ = 3, λ₂ = 1) y volvemos a la grilla canónica."))
    return


@app.cell
def _(mo):
    mo.callout(mo.md(r"""
    **Diagonalizabilidad no tiene nada que ver con invertibilidad: cuatro matrices testigo.** Quedan
    abiertas dos preguntas: ¿qué pasa si hay algo en el núcleo?, ¿y si un autovalor repetido no alcanza para armar una
    base? Las respondemos con cuatro matrices $2\times2$. Una cosa es **invertir** (no aplastar nada: $\det \ne 0$) y
    otra **diagonalizar** (tener dos rectas propias independientes que armen una grilla).

    | | matriz | hecho geométrico | $\det$ | ¿base de autovectores? |
    |---|---|---|---|---|
    | 1. diagonalizable e invertible | $\begin{pmatrix}2&0\\0&1\end{pmatrix}$ | estira el eje $x$ al doble y deja el $y$; dos direcciones propias independientes, $e_1, e_2$ | $2$ | sí |
    | 2. diagonalizable, **no** invertible | $\begin{pmatrix}1&0\\0&0\end{pmatrix}$ | proyecta sobre el eje $x$ y aplasta todo el eje $y$ al origen (ese eje es el núcleo) | $0$ | sí: $e_1, e_2$ con $\lambda_1 = 1$, $\lambda_2 = 0$ |
    | 3a. invertible, **no** diagonalizable | $\begin{pmatrix}1&1\\0&1\end{pmatrix}$ | corte (cizalladura): el eje $x$ queda fijo y las demás rectas se inclinan | $1$ | no: un solo autovector |
    | 3b. invertible, **no** diagonalizable en $\mathbb R$ | $\begin{pmatrix}0&-1\\1&0\end{pmatrix}$ | giro de $90^\circ$: ninguna recta real queda fija | $1$ | no: $\lambda = \pm i$ |
    | 4. ni una ni otra | $\begin{pmatrix}0&1\\0&0\end{pmatrix}$ | aplasta todo sobre el eje $x$ y además manda $e_2$ a $e_1$ | $0$ | no: un solo autovector |

    **Matriz 2: tener autovalor $0$ impide invertir, no impide diagonalizar.** Ya es diagonal: $\Lambda = A$. El
    núcleo es justamente la recta propia de $\lambda_2 = 0$, y junto con la de $\lambda_1 = 1$ arma la base completa.

    **Matriz 3a.** Es invertible, con inversa $\begin{pmatrix}1&-1\\0&1\end{pmatrix}$ (el corte hacia el otro lado). Su
    polinomio característico es $(\lambda - 1)^2 = 0$: raíz doble $\lambda = 1$, **multiplicidad algebraica** $2$.
    Pero $(A - I)v = 0$ da $v_2 = 0$, o sea sólo el eje $x$: **multiplicidad geométrica** $1$. Falta un segundo
    autovector para armar la grilla, así que no hay $B$ invertible con $B^{-1}AB$ diagonal.

    **Matriz 3b.** El polinomio es $\lambda^2 + 1 = 0$, sin raíces reales: un giro no deja ninguna recta en su lugar.

    **Matriz 4.** $\lambda = 0$ doble (algebraica $2$), pero $Av = 0$ sólo para $v = (x, 0)$: un único autovector,
    $e_1$ (geométrica $1$). Tiene núcleo **y** le falta una dirección propia.

    El defecto de las matrices 3a, 3b y 4 es exactamente la razón por la que en la [unidad siguiente](../09_cambio_de_base_svd/index.html)
    pasamos a la SVD, $A = U\Sigma V^T$: con una base ortonormal a la entrada ($V$) y **otra distinta** a la salida
    ($U$), toda matriz, incluso un corte o una rectangular, se lee como diagonal. Ojo: es diagonal entre dos grillas
    distintas, no es una semejanza. $\Sigma$ no es "$A$ en otra base", los $\sigma$ no son autovalores (en el corte
    $\sigma = (\sqrt5 \pm 1)/2$ y $\lambda = 1$ doble) y no sirve para potencias: $A^n \ne U\Sigma^nV^T$. Las dos
    descomposiciones coinciden sólo si $A$ es simétrica semidefinida positiva.
    """), kind="info")
    return


@app.cell
def _(mo, np):
    _testigos = {
        "1. diag(2, 1)": np.array([[2.0, 0.0], [0.0, 1.0]]),
        "2. proyección diag(1, 0)": np.array([[1.0, 0.0], [0.0, 0.0]]),
        "3a. corte": np.array([[1.0, 1.0], [0.0, 1.0]]),
        "3b. giro 90°": np.array([[0.0, -1.0], [1.0, 0.0]]),
        "4. nilpotente": np.array([[0.0, 1.0], [0.0, 0.0]]),
    }
    _filas = []
    for _nombre, _M in _testigos.items():
        _w, _V = np.linalg.eig(_M)
        _base = np.isreal(_w).all() and np.linalg.matrix_rank(_V, tol=1e-8) == 2
        _auto = ", ".join(f"{_x:.2f}".replace("+0.00j", "").replace("-0.00j", "") for _x in _w)
        _filas.append(
            f"| {_nombre} | ${np.linalg.det(_M):.0f}$ | ${_auto}$ | {'sí' if _base else 'no'} |"
        )
    mo.md(
        "Verificación con numpy de los cuatro casos:\n\n"
        "| matriz | $\\det$ | autovalores | ¿base de autovectores? |\n|---|---|---|---|\n"
        + "\n".join(_filas)
    )
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (b₁, b₂ del caso, A que se mira en esa base o None, qué pasa) ----------
    casos = {
        "base girada 30° (Rotaciones I)": (
            (np.cos(np.pi / 6), np.sin(np.pi / 6)), (-np.sin(np.pi / 6), np.cos(np.pi / 6)), None,
            r"los ejes viejos girados: perpendiculares y de largo $1$, $B^{-1} = B^T$ y la proyección coincide con $c$. "
            r"Es [Rotaciones I](../01a_punto_quieto/index.html). Girá $b_2$ y mirá cuándo deja de coincidir."),
        "base oblicua de la parcela": (
            (3.0, 1.0), (1.0, 2.0), None,
            r"la grilla de frentes y lados: $B^{-1} \ne B^T$, la proyección **no** da $c$; hay que resolver."),
        "base de autovectores de A = [[2, 1], [1, 2]]": (
            (1.0, 1.0), (1.0, -1.0), np.array([[2.0, 1.0], [1.0, 2.0]]),
            r"los ejes propios de $A$: $B^{-1}AB$ es **diagonal**, $A$ estira $\times 3$ a lo largo de $b_1$ y deja quieto "
            r"$b_2$. Girá $b_2$ y la diagonal se rompe: la grilla propia es una sola."),
        "cizalla [[1, 1], [0, 1]]: un solo autovector": (
            (1.0, 0.0), (0.0, 1.0), np.array([[1.0, 1.0], [0.0, 1.0]]),
            r"la cizalla sólo deja en su dirección a $b_1 = (1, 0)$. Cualquier $b_2$ sirve para leer coordenadas, pero "
            r"$B^{-1}AB$ **nunca** es diagonal: sin segundo eje propio no se diagonaliza."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="base oblicua de la parcela", label="caso precargado")
    mo.md(r"""
    ## 2. Manipulación

    Tres capas. En **gris**, la grilla de la obra. En **teal**, la grilla **oblicua** que generan los ejes nuevos
    $b_1$ (teal) y $b_2$ (rust) con todas sus paralelas. En **violeta**, el mojón, que no se mueve, y el **camino
    de lectura**: avanzamos $c_1$ veces $b_1$ y después $c_2$ veces $b_2$; los dos tramos son las coordenadas nuevas.
    Los deslizadores desvían $b_2$ respecto del caso (giro y largo); con $b_2$ paralelo a $b_1$ no hay base.
    """)
    return caso, casos


@app.cell
def _(mo):
    desvio = mo.ui.slider(-90, 90, value=0, step=1, label="giro extra de b₂ (°)", show_value=True)
    factor = mo.ui.slider(0.5, 2.0, value=1.0, step=0.1, label="factor de largo de b₂", show_value=True)
    return desvio, factor


@app.cell
def _(caso, casos, desvio, factor, lib, mo, mojon, np):
    _b1, _b2, A_caso, que_pasa = casos[caso.value]
    b1 = np.asarray(_b1, dtype=float)
    b2 = factor.value * (lib.rot2(np.deg2rad(desvio.value)) @ np.asarray(_b2, dtype=float))
    B = np.column_stack([b1, b2])
    P = mojon
    singular = abs(np.linalg.det(B)) < 1e-6
    _rango = 6
    figura = lib.figura_plano(_rango, f"{caso.value} · el mojón no se mueve")
    lib.capa_antes(figura, _rango - 1, cuadrado=False)
    lib.flecha(figura, (0, 0), (2, 0), lib.GRIS_ANTES, "eje x (obra)", ancho=3)
    lib.flecha(figura, (0, 0), (0, 2), lib.GRIS_ANTES, "eje y (obra)", ancho=3)
    if singular:
        c = None
        _numeros = r"**$b_2$ es paralelo a $b_1$**: $\det B = 0$, las dos columnas generan una sola recta y no hay grilla. Movelo."
    else:
        _k = min(12, int(np.ceil(1.5 * _rango / min(np.linalg.norm(b1), np.linalg.norm(b2)))))
        lib.capa_base(figura, B, _k)
        lib.lectura_coordenadas(figura, P, B, nombre="camino de lectura")
        c = lib.coordenadas_en_base(P, B)
        _proy = np.array([P @ b1 / (b1 @ b1), P @ b2 / (b2 @ b2)])
        _perp = lib.exacto(_proy, c, tol=1e-6)
        _numeros = rf"""
        - $B = {lib.matriz_coloreada(B)}$, $\det B = {lib.num_tex(np.linalg.det(B))}$, $B^{{-1}} = {lib.pmat(np.linalg.inv(B))}$
        - el mojón en la obra: $P = {lib.vec_tex(P)}$; en la base nueva: $\mathbf{{c = B^{{-1}}P = {lib.vec_tex(c)}}}$; control $Bc = {lib.vec_tex(B @ c)}$
        - proyección $\langle P, b_k\rangle/\langle b_k, b_k\rangle = {lib.vec_tex(_proy)}$: {"**coincide** con $c$ (ejes perpendiculares)" if _perp else "**no** es $c$ (ejes no perpendiculares)"}
        """
        if A_caso is not None:
            _Ap = np.linalg.inv(B) @ A_caso @ B
            _diag = lib.exacto(_Ap, np.diag(np.diag(_Ap)), tol=1e-6)
            _numeros += rf"""
        - $A = {lib.pmat(A_caso)}$ vista en esta base: $B^{{-1}}AB = {lib.pmat(_Ap)}$ → {"**diagonal**: acá $A$ sólo estira" if _diag else "no es diagonal: no es la grilla propia de $A$"}
        """
    lib.punto(figura, P, nombre="mojón (quieto)", texto="P")
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, desvio, factor,
        mo.md("**Números vivos**\n" + "\n".join(_l.strip() for _l in _numeros.splitlines()) + f"\n**Qué pasa acá:** {que_pasa}"),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return B, P, c, singular


@app.cell
def _(mo):
    n_pot = mo.ui.slider(1, 8, value=5, step=1, label="n (potencia)", show_value=True)
    mo.md(r"""
    **La transformación en su grilla propia.** Ahora la grilla no la elegimos nosotros: la elige
    $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$. En gris, la grilla de la obra y el cuadrado de vértices
    $\pm b_1$, $\pm b_2$; en teal, la grilla después de $A$ (los cuadrados pasan a paralelogramos: así "no se
    entiende"). Las rectas punteadas son los **ejes propios**: $b_1 = (1, 1)$ con $\lambda_1 = 3$ y $b_2 = (1, -1)$
    con $\lambda_2 = 1$; el rombo se estira $\times 3$ a lo largo de $b_1$ y queda igual a lo largo de $b_2$.
    **Reproducir** recorre $A^t$ de $t = 0$ a $1$: la película, con las estelas curvándose hacia el eje de
    $\lambda = 3$. En el panel, $A^n$ multiplicando $n$ veces y por $B\Lambda^nB^{-1}$.
    """)
    return (n_pot,)


@app.cell
def _(go, lib, mo, n_pot, np):
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    lam, _V = lib.diagonalizar(A)
    B_prop = np.array([[1.0, 1.0], [1.0, -1.0]])  # los mismos ejes que _V, con enteros
    Lam = np.diag(lam)
    _rango = 6
    rombo = np.array([[1.0, 1.0], [1.0, -1.0], [-1.0, -1.0], [-1.0, 1.0]])  # ±b₁, ±b₂
    camino = [lib.pot_real(A, t) for t in np.linspace(0, 1, 36)]

    def _dinamicas(i):
        f = go.Figure()
        lib.capa_despues(f, camino[i], _rango - 1, columnas=False)
        lib.objeto(f, lib.transformar(rombo, camino[i]), lib.VIOLETA_OBJETO, "rombo después",
                   estelas=lib.estelas(rombo, camino[: i + 1]))
        return list(f.data)

    fig_A = lib.figura_plano(_rango, "A en su grilla propia: estira ×3 a lo largo de b₁, deja b₂")
    lib.capa_antes(fig_A, _rango - 1, cuadrado=False)
    lib.capa_ejes_propios(fig_A, A, _rango)
    lib.objeto(fig_A, rombo, lib.GRIS_ANTES, "rombo antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        fig_A.add_trace(_t)
    lib.animar(fig_A, [_dinamicas(i) for i in range(len(camino))])

    An_mult = np.linalg.matrix_power(A, n_pot.value)
    An_diag = B_prop @ np.diag(lam ** n_pot.value) @ np.linalg.inv(B_prop)
    _panel = mo.vstack([
        mo.md("**Controles**"), n_pot,
        mo.md(rf"""
        **Números vivos**

        $$\Lambda = {lib.pmat(Lam)}, \quad B = {lib.matriz_coloreada(B_prop, dec=0)}$$

        $$B^{{-1}}AB = {lib.pmat(np.linalg.inv(B_prop) @ A @ B_prop)}$$

        $$A^{{{n_pot.value}}} = {lib.pmat(An_mult)} \text{{ (multiplicando)}}$$

        $$B\,\Lambda^{{{n_pot.value}}}B^{{-1}} = {lib.pmat(An_diag)}$$

        - `np.allclose` entre las dos: `{bool(np.allclose(An_mult, An_diag))}`. $\Lambda^n$ es elevar dos números; $A^n$ a mano son $n - 1$ productos.
        - $\det A = {lib.num_tex(np.linalg.det(A))} = \lambda_1\lambda_2$, traza $= {lib.num_tex(np.trace(A))} = \lambda_1 + \lambda_2$: no cambian con la base.
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(fig_A), _panel)
    return A, An_diag, An_mult, B_prop, Lam, lam


@app.cell
def _(A, B_parcela, B_prop, lib, mo, mojon, np):
    _c = np.linalg.solve(B_parcela, mojon)
    _w, _V = np.linalg.eig(A)
    _A5 = np.linalg.matrix_power(A, 5)
    _A5d = B_prop @ np.diag([3.0 ** 5, 1.0]) @ np.linalg.inv(B_prop)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno con enteros; derecha, la misma en numpy.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Leer el mojón en la base de la parcela.** $Bc = P$ es un sistema $2\times2$:

            $$\begin{pmatrix} \textcolor{#1b6f6a}{3} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{2} \end{pmatrix}\binom{c_1}{c_2} = \binom{4}{3}
            \;\Rightarrow\; \begin{cases} 3c_1 + c_2 = 4 \\ c_1 + 2c_2 = 3 \end{cases}$$

            De la segunda, $c_1 = 3 - 2c_2$; en la primera, $9 - 5c_2 = 4$: $c_2 = 1$, $c_1 = 1$. O con la inversa:
            $B^{-1} = \frac15\begin{pmatrix} 2 & -1 \\ -1 & 3 \end{pmatrix}$ y $B^{-1}\binom{4}{3} = \binom{1}{1}$.
            """),
            mo.vstack([
                mo.md("```python\nB = np.array([[3., 1.], [1., 2.]])   # columnas: b1, b2\np = np.array([4., 3.])\nnp.linalg.solve(B, p)               # resuelve B c = p\n```"),
                mo.md(f"`solve(B, p)` = `{np.round(_c, 3).tolist()}` · `inv(B) @ p` = `{np.round(np.linalg.inv(B_parcela) @ mojon, 3).tolist()}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 Diagonalizar $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$.** $\det(A - \lambda I) = (2-\lambda)^2 - 1 = 0
            \Rightarrow \lambda = 3,\ 1$. Para $\lambda = 3$, $(A - 3I)v = 0$ con filas $(-1, 1)$: $v = (1, 1)$; para
            $\lambda = 1$, filas $(1, 1)$: $v = (1, -1)$.

            $$B = \begin{pmatrix} \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{-1} \end{pmatrix},\quad
            B^{-1} = \tfrac12\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix},\quad
            B^{-1}AB = \tfrac12\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} 3 & 1 \\ 3 & -1 \end{pmatrix} = \begin{pmatrix} 3 & 0 \\ 0 & 1 \end{pmatrix}.$$

            `eig` da los autovectores de largo $1$ y a veces con otro signo: el **eje** es el mismo.
            """),
            mo.vstack([
                mo.md("```python\nA = np.array([[2., 1.], [1., 2.]])\nw, V = np.linalg.eig(A)     # autovalores; autovectores en columnas\nnp.linalg.inv(V) @ A @ V    # diagonal\n```"),
                mo.md(f"`w` = `{np.round(_w, 3).tolist()}` · `V` =\n```\n{np.round(_V, 3)}\n```\n`inv(V) @ A @ V` =\n```\n{np.round(np.linalg.inv(_V) @ A @ _V, 3)}\n```"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 $A^5$ sin multiplicar cinco veces.** $\Lambda^5 = \mathrm{diag}(3^5, 1) = \mathrm{diag}(243, 1)$:

            $$A^5 = B\Lambda^5B^{-1} = \begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}\begin{pmatrix} 243 & 0 \\ 0 & 1 \end{pmatrix}\tfrac12\begin{pmatrix} 1 & 1 \\ 1 & -1 \end{pmatrix}
            = \tfrac12\begin{pmatrix} 244 & 242 \\ 242 & 244 \end{pmatrix} = \begin{pmatrix} 122 & 121 \\ 121 & 122 \end{pmatrix}.$$

            Lectura: $e_1 = \tfrac12 b_1 + \tfrac12 b_2$; la parte en $b_1$ se multiplica por $243$, la de $b_2$ queda:
            $\tfrac12(243, 243) + \tfrac12(1, -1) = (122, 121)$.
            """),
            mo.vstack([
                mo.md("```python\nB = np.array([[1., 1.], [1., -1.]])\nA5 = B @ np.diag([3.**5, 1.]) @ np.linalg.inv(B)\nnp.allclose(A5, np.linalg.matrix_power(A, 5))\n```"),
                mo.md(f"`A5` =\n```\n{np.round(_A5d, 3)}\n```\n`matrix_power(A, 5)` =\n```\n{np.round(_A5, 3)}\n```\n`allclose` = `{bool(np.allclose(_A5, _A5d))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(B_parcela, mo, np):
    _P = np.array([[4.0, 3.0], [3.0, 1.0], [0.0, 5.0]])
    _C = np.linalg.solve(B_parcela, _P.T).T
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Tres funciones de `np.linalg` y una idea: **resolver, no invertir**. `solve(B, p)` da el $c$ con $Bc = p$ sin
        calcular $B^{-1}$ (más exacto y más barato). `eig(A)` devuelve `(w, V)`: $\Lambda = $ `diag(w)`, $B = $ `V`.
        `matrix_power(A, n)` es $A^n$ multiplicando (`A ** n` eleva cada número por separado: otra cosa). Y una nube
        $N\times2$ de mojones se re-expresa entera: `solve(B, P.T)` resuelve un sistema por columna y la transpuesta
        vuelve a una fila por punto.
        """),
        mo.md("```python\nP = np.array([[4., 3.], [3., 1.], [0., 5.]])   # shape (3, 2): tres mojones en la obra\nC = np.linalg.solve(B, P.T).T                  # (2, 3) → (3, 2): los mismos en frentes y lados\n```"),
        mo.md(f"`C` =\n```\n{np.round(_C, 3)}\n```\n`C.shape` = `{_C.shape}` · control `np.allclose(C @ B.T, P)` = `{bool(np.allclose(_C @ B_parcela.T, _P))}` (volver es $p = Bc$, fila por fila)."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("la matriz tiene en sus columnas los vectores de una base expresada en la otra").*
        Ejes nuevos $b_1 = (2, 0)$ y $b_2 = (1, 1)$, mojón $p = (5, 3)$. Hallá sus coordenadas nuevas resolviendo
        $Bc = p$. Después calculá $\langle p, b_k\rangle / \langle b_k, b_k\rangle$: ¿por qué no da lo mismo?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $B = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$: $2c_1 + c_2 = 5$, $c_2 = 3$, luego $c_1 = 1$: $c = (1, 3)$.
        Control: $1\,(2,0) + 3\,(1,1) = (5, 3)$. ✓ Las proyecciones dan $10/4 = 2.5$ y $8/2 = 4$: distinto, porque
        $\langle b_1, b_2\rangle = 2 \ne 0$ y la sombra sobre un eje incluye parte del otro. Proyectar sólo lee
        coordenadas en bases ortogonales.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("en la base de autovectores la transformación es diagonal").*
        $A = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$. Hallá autovalores y autovectores, armá $B$ y $B^{-1}$,
        verificá que $B^{-1}AB$ es diagonal y calculá $A^3$ por la diagonal. Controlá multiplicando.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        Triangular: $\lambda = 3, 2$. Para $\lambda = 3$, filas $(0, 1)$: $v = (1, 0)$; para $\lambda = 2$, filas $(1, 1)$:
        $v = (1, -1)$. No son perpendiculares ($A$ no es simétrica). $B = \begin{pmatrix} 1 & 1 \\ 0 & -1 \end{pmatrix}$
        y $B^{-1} = B$ (verificá $B^2 = I$); $B^{-1}AB = B\begin{pmatrix} 3 & 2 \\ 0 & -2 \end{pmatrix} = \begin{pmatrix} 3 & 0 \\ 0 & 2 \end{pmatrix}$. ✓
        $A^3 = B\,\mathrm{diag}(27, 8)\,B = B\begin{pmatrix} 27 & 27 \\ 0 & -8 \end{pmatrix} = \begin{pmatrix} 27 & 19 \\ 0 & 8 \end{pmatrix}$;
        control: $A^2 = \begin{pmatrix} 9 & 5 \\ 0 & 4 \end{pmatrix}$, $A^2A = \begin{pmatrix} 27 & 19 \\ 0 & 8 \end{pmatrix}$. ✓
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def coordenadas_en(B, p):\n    # B: 2×2 con los ejes nuevos como COLUMNAS; p: el punto en la grilla vieja\n    return ...   # las coordenadas de p en la base nueva (array de 2)\n",
        language="python", min_height=110, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("expresar vectores dados en una base como combinación lineal de otra").*
        Completá `coordenadas_en(B, p)`. Tenés `np`. Se verifica con `np.allclose` en 20 puntos al azar con la base del
        ejercicio (a).
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _B = np.array([[2.0, 1.0], [0.0, 1.0]])  # la base del ejercicio (a): no es simétrica, así B.T se distingue de B
    _puntos = np.random.default_rng(0xDDDE).uniform(-5, 5, size=(20, 2))
    _esperado = np.linalg.solve(_B, _puntos.T).T
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.array([_ns["coordenadas_en"](_B.copy(), p) for p in _puntos], dtype=float)
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ para un punto devolvés algo de forma `{_obtenido.shape[1:]}`; tiene que ser `(2,)`."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los 20 puntos: resolviste $Bc = p$."), kind="success")
        elif np.allclose(_obtenido, lib.transformar(_puntos, _B)):
            _res = mo.callout(mo.md(r"❌ devolvés `B @ p`: eso lleva de nuevas a **viejas**. Para leer hay que resolver: `np.linalg.solve(B, p)`."), kind="warn")
        elif np.allclose(_obtenido, np.array([[p @ _B[:, k] / (_B[:, k] @ _B[:, k]) for k in range(2)] for p in _puntos])):
            _res = mo.callout(mo.md(r"❌ proyectaste con el producto interno sobre cada eje. Sólo vale con ejes perpendiculares; acá forman $45°$."), kind="warn")
        elif np.allclose(_obtenido, np.linalg.solve(_B.T, _puntos.T).T):
            _res = mo.callout(mo.md(r"❌ usaste los ejes como **filas** (`B.T`). Las columnas de $B$ son los ejes nuevos: `solve(B, p)`, sin transponer."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para `{np.round(_puntos[0], 3).tolist()}` esperaba `{np.round(_esperado[0], 3).tolist()}` y obtuve `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def potencia(A, n):\n    w, V = np.linalg.eig(A)   # autovalores w, autovectores en las columnas de V\n    Lam_n = ...               # Λⁿ: diagonal con los autovalores elevados a n\n    return ...                # B Λⁿ B⁻¹, con B = V\n",
        language="python", min_height=130, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("la base de autovectores permite aplicar $n$ veces la transformación").*
        Completá `potencia(A, n)` por diagonalización. Tenés `np`. Se verifica con `np.allclose` contra
        `np.linalg.matrix_power` en $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ con $n = 5$ y en la $A$ de (b) con $n = 3$.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(A, editor_d, mo, np):
    _Ab = np.array([[3.0, 1.0], [0.0, 2.0]])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _ok = all(np.allclose(np.real(_ns["potencia"](M.copy(), n)), np.linalg.matrix_power(M, n)) for M, n in ((A, 5), (_Ab, 3)))
        _r = np.real(np.asarray(_ns["potencia"](A.copy(), 5), dtype=complex))
        _w, _V = np.linalg.eig(A)
        if _ok:
            _res = mo.callout(mo.md("✅ coincide con `matrix_power` en las dos matrices: $A^n = B\\Lambda^nB^{-1}$."), kind="success")
        elif np.allclose(_r, A):
            _res = mo.callout(mo.md(r"❌ devolvés $A$: armaste $B\Lambda B^{-1}$ sin elevar. Es `np.diag(w ** n)`."), kind="warn")
        elif np.allclose(_r, np.linalg.inv(_V) @ np.diag(_w ** 5) @ _V):
            _res = mo.callout(mo.md(r"❌ $B$ y $B^{-1}$ invertidos: $B^{-1}\Lambda^nB$ es otra matriz. Se entra por $B^{-1}$ (a la derecha, actúa primero), se estira, se sale por $B$."), kind="warn")
        elif np.allclose(_r, A ** 5):
            _res = mo.callout(mo.md(r"❌ `A ** n` eleva cada número por separado; $A^n$ es multiplicar matrices. Con la diagonal: `V @ np.diag(w ** n) @ np.linalg.inv(V)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para $A$ y $n = 5$ obtuve\n```\n{np.round(_r, 3)}\n```\ny esperaba `[[122, 121], [121, 122]]`."), kind="danger")
    except Exception as _e:
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "08_cambio_de_base")
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

    Acá verificamos que los números cambian con $B^{-1}$ y que en la grilla propia $A$ sólo estira. Las demostraciones:

    - [apunte, sección "Cambio de base y diagonalización"](../../apunte.pdf#nameddest=sec:cambio-base): el resultado
      "La matriz de cambio de base", el párrafo "Diagonalizar es elegir la grilla de los autovectores" (el ejemplo
      numérico de $P^{-1}AP = D$; el argumento general, $AB = B\Lambda$ columna por columna, está en la sección 1 de
      esta unidad) y el párrafo sobre la clase del 30 de
      septiembre, con las grillas y el despeje $T_{\mathrm{diag}} = A^{-1}\,T_{\mathrm{can}}\,A$
      · [apunte, «Álgebra de las transformaciones» (autovectores, formas lineales, cambio de base)](../../apunte.pdf#nameddest=cap:cambio-base)
    - [ficha de la clase 8](../../clases/08.html) · [el hilo conductor](../../index.html) · [Rotaciones I](../01a_punto_quieto/index.html)

    **Lo que viene:** la SVD (unidad 09): dos bases perpendiculares, una a la entrada y otra a la
    salida, para que toda matriz sea "sólo estirar" de una grilla a otra, también las que no tienen ejes propios. Y las superficies
    (unidad 10): la grilla $(u, v)$ dibujada sobre el terreno.
    """)
    return


@app.cell
def _(A, An_diag, An_mult, B, B_parcela, B_prop, Lam, P, b1_parcela, b2_parcela, c, candidatos, lam, lib, mo, np, singular):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _A5 = [[122, 121], [121, 122]]
    _checks = [
        ("candidatos de la predicción distintos entre sí", len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4),
        ("sección 0: b₁, b₂ a 45°; c = (1, 1); proyección (1.5, 2); B P = (15, 10)",
         lib.exacto(lib.angulo(b1_parcela, b2_parcela), np.pi / 4) and lib.exacto(candidatos["correcta"], [1, 1])
         and lib.exacto(candidatos["proyeccion"], [1.5, 2]) and lib.exacto(candidatos["por-B"], [15, 10])),
        ("sección 3.1: B⁻¹ = (1/5)[[2, −1], [−1, 3]]", lib.exacto(np.linalg.inv(B_parcela), np.array([[2, -1], [-1, 3]]) / 5)),
        ("sección 3.2: λ = (3, 1), B⁻¹AB = Λ", lib.exacto(lam, [3, 1]) and lib.exacto(np.linalg.inv(B_prop) @ A @ B_prop, Lam)),
        ("sección 3.3: A⁵ = [[122, 121], [121, 122]] por las dos vías",
         lib.exacto(np.linalg.matrix_power(A, 5), _A5) and lib.exacto(B_prop @ np.diag([243, 1]) @ np.linalg.inv(B_prop), _A5)),
        ("sección 2: Aⁿ multiplicando = B Λⁿ B⁻¹ para el n del deslizador", lib.exacto(An_mult, An_diag, tol=1e-6)),
        ("sección 2: en la base de la figura, B c = P", singular or lib.exacto(B @ c, P, tol=1e-9)),
        ("ejercicio (a): c = (1, 3)", lib.exacto(lib.coordenadas_en_base([5, 3], [[2, 1], [0, 1]]), [1, 3])),
        ("ejercicio (b): A³ = [[27, 19], [0, 8]]", lib.exacto(np.linalg.matrix_power([[3.0, 1.0], [0.0, 2.0]], 3), [[27, 19], [0, 8]])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
