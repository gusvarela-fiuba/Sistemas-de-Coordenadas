# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Estación 0 — Antes de empezar: cuatro cosas para desaprender del CBC (molde v2 sobre cb104).

Encuadre propio del autor, elaborado a partir de las clases 1, 4 y 9; no es contenido dictado por la cátedra. Cuatro
cambios de chip respecto del álgebra del CBC: (1) todo vector es un punto o un desplazamiento entre mojones; (2) una
forma lineal (y el gradiente) no es una flecha sino una regla graduada, que se arrastra con A⁻¹; (3) las coordenadas son
etiquetas de una grilla, para medir hace falta una métrica; (4) derivar es usar una matriz en el parche tangente.

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
    # Estación 0 — Antes de empezar: cuatro cosas para desaprender del CBC

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Esto es un encuadre mío, no contenido dictado por la cátedra: lo armé a partir de las clases 1, 4 y 9 para leer el
    resto del camino con una sola cabeza. En el CBC el álgebra lineal y el análisis fueron dos materias con dos
    cuadernos; acá son **una sola herramienta geométrica sobre el terreno**, y para que eso cierre hay que cambiar
    cuatro chips. Ninguno es difícil; lo difícil es soltar el reflejo.

    Colores, iguales en figura y álgebra: lo de **antes** en gris, lo de **después** en
    <span style="color:#1b6f6a">**teal**</span> (segunda columna en <span style="color:#b5451b">**rust**</span>,
    tercera en <span style="color:#c9a227">**gold**</span>), el objeto que importa en
    <span style="color:#7a4e9e">**violeta**</span>.
    """)
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
        """Ángulo en grados entre a y b medido con la métrica g (matriz 2×2 simétrica definida positiva):
        cos = aᵀ g b / √(aᵀ g a · bᵀ g b). Con g = I es el ángulo de siempre."""
        a, b, g = (np.asarray(t, dtype=float) for t in (a, b, g))
        c = (a @ g @ b) / np.sqrt((a @ g @ a) * (b @ g @ b))
        return float(np.degrees(np.arccos(np.clip(c, -1.0, 1.0))))

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

    return altura, angulo_g, direccion_entera, esfera3d, grad_altura, loma3d


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
        options={
            "dirección " + lib.vec_plano(candidatos["ingenua"]) + ": los dos números del gradiente, como flecha": "ingenua",
            "dirección " + lib.vec_plano(candidatos["perp-dibujo"]) + ": perpendicular a las curvas tal como se ven en el plano": "perp-dibujo",
            "dirección " + lib.vec_plano(candidatos["correcta"]): "correcta",
            "dirección " + lib.vec_plano(candidatos["curva"]) + ": a lo largo de la curva de nivel": "curva",
        },
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

        El plano que tengo en la mesa está dibujado con el **eje Este estirado por 2** (como una planilla con columnas de
        distinto paso): el punto de terreno $(x, y)$ aparece en $(2x, y)$. Las curvas de nivel se ven como elipses y el
        mojón cae en $(4, 2)$. La pregunta de campo: si dibujo sobre ese plano la flecha de "hacia dónde baja el agua",
        **¿para dónde la dibujo?** Las cuatro direcciones están en unidades del dibujo.
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
                    r"empinada. Los números del gradiente son los de una regla; para convertirlos en flecha hace falta saber cuánto "
                    r"mide cada paso de la grilla."),
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
                     r"Eso es lo que esta estación quiere dejar instalado antes de la primera rotación."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.vstack([
        mo.callout(mo.md(_texto), kind=_kind),
        mo.md(r"""
        El profesor lo dijo en vivo el 14/10 (clase 9), corrigiéndose a sí mismo: "el gradiente de una función es un
        vector… no, mentí, lo dije mal. **El gradiente es una forma lineal, no un vector**; lo es porque me permite hacer
        una aproximación lineal de la función" (transcripción auto-traducida del inglés, `fuentes/transcripciones/2026-10-14.md`).
        Lo que sigue es qué cambia en la cabeza para que esa frase sea obvia.
        """),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico: los cuatro cambios de chip

    **¿Qué se conserva?** El terreno. Mojones, cotas, distancias y ángulos están ahí antes de que yo elija ejes, grilla o
    escala del dibujo; lo que cambia con mis elecciones son los **números**. Cada chip es una manera de no confundir los
    números con el terreno.

    **Chip 1 — No hay flechas flotando.** En el CBC un vector era una flecha que se podía deslizar por la hoja. En el
    campo, todo vector es **un punto** (un mojón, con sus coordenadas desde el origen) o **un desplazamiento entre dos
    mojones** (la diferencia de sus coordenadas). Y una matriz $A$ hace una de dos cosas: mueve los puntos ($x \mapsto Ax$,
    el mojón cambia de lugar) o cambia la grilla con la que los leo (el mojón queda, cambian sus números). La misma cuenta,
    dos lecturas: [Rotaciones I](../01a_punto_quieto/index.html) arranca exactamente ahí.

    **Chip 2 — El gradiente no es una flecha, es una regla.** Una forma lineal $w^T$ toma un punto y devuelve un número:
    $w^T x = w_1 x_1 + w_2 x_2$. No vive en el plano de los puntos sino en el **dual** $V^*$; su dibujo no es una flecha
    sino un **mazo de curvas de nivel** equiespaciadas (las marcas de una regla), y evalúa sin producto interno: $w^T x$
    es fila por columna, nada más. Cuando el plano se estira con $A$ y los puntos van a $Ax$, las marcas se arrastran
    **al revés**, con $A^{-1}$: $w'^T = w^T A^{-1}$, de modo que $w'^T (Ax) = w^T x$ y cada mojón conserva su cota. El
    gradiente es esta regla: en un punto, $\nabla h$ es la forma que lee cuánto sube $h$ con cada pasito.

    **Chip 3 — Las coordenadas son etiquetas, no metros.** $(u, v)$ en una grilla, o $(\varphi, \lambda)$ en el
    elipsoide, nombran al punto pero no dicen cuánto mide un paso. Para medir largos y ángulos hace falta una
    **métrica**: en el plano, un producto interno $\langle a, b\rangle = a^T g\, b$ (con $g = I$ si la grilla mide metros
    en los dos ejes); en una superficie, la primera forma fundamental $E, F, G$. "Perpendicular" y "más corto" son
    preguntas a la métrica, no a la grilla. Por eso en la sección 0 la perpendicular del papel no era la del terreno.

    **Chip 4 — Álgebra y análisis son la misma materia.** Derivar es **usar una matriz en el parche plano tangente**:
    el jacobiano $J$ manda un pasito $(du, dv)$ de la grilla al pasito $J\,(du, dv)$ sobre la superficie, y sus columnas
    son los ejes locales. Curvarse (la hessiana, la segunda forma) es una **forma cuadrática**: un número por cada
    dirección. Todo lo de las clases 1 a 8 vuelve en las clases 9 a 14 con el mismo dibujo, hecho chiquito.

    | | se escribe | qué es en el terreno | con $x \mapsto Ax$ |
    |---|---|---|---|
    | punto en $V$ | columna $x$ | un mojón, o un desplazamiento entre mojones | $x' = Ax$ |
    | forma en $V^*$ | fila $w^T$; $w^T x$ es un número | una regla: las curvas de nivel de la cota | $w'^T = w^T A^{-1}$ (la lectura no cambia) |
    | métrica | $g$ simétrica; $\lvert x\rvert^2 = x^T g\, x$ | cuánto mide cada paso de la grilla | $g' = A^{-T} g\, A^{-1}$ (los largos no cambian) |

    La escalera, con el chip 2 y 3 juntos: en $\mathbb R$ la regla es $w x$ y la métrica un número ($\lvert x\rvert = \sqrt{g}\,\lvert x\rvert_{\text{grilla}}$:
    la escala); en $\mathbb R^2$ las marcas son rectas paralelas y $g$ es $2\times2$; en $\mathbb R^3$ las marcas son
    planos paralelos y $g$ es $3\times3$. Esto es una **muestra**; las demostraciones viven en el apunte (anexo).
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- sección 2: selector de objeto y casos precargados para (a) y (b) ----------
    casos = {
        "identidad": (np.eye(2), r"nada se mueve: los dos dibujos coinciden."),
        "estirar Este ×2: diag(2, 1)": (np.diag([2.0, 1.0]), r"los puntos se estiran en $x$; la regla se divide, $(1, 1) \mapsto (\tfrac12, 1)$; la perpendicular del dibujo deja de ser la del terreno."),
        "cizalla [[1, 1], [0, 1]]": (np.array([[1.0, 1.0], [0.0, 1.0]]), r"la grilla se acuesta; la regla se corta al revés, $(1, 1) \mapsto (1, 0)$: después sólo lee $x$."),
        "rotación 30°": (lib.rot2(np.deg2rad(30)), r"$A^{-1} = A^T$: la regla gira igual que los puntos y la flecha sigue perpendicular. Con un giro el chip 2 no se nota."),
    }
    parches = {
        "la loma r = (u, v, 2·exp(−(u²+v²)/8))": ("loma", (-3.0, 3.0, 0.25, 2.0, 1.0), (-3.0, 3.0, 0.25, 1.0, 1.0)),
        "trozo de esfera de radio 2 (φ, λ en grados)": ("esfera", (-80.0, 80.0, 5.0, 45.0, np.pi / 180), (-150.0, 150.0, 5.0, 0.0, np.pi / 180)),
    }
    objeto_sel = mo.ui.dropdown(options=["(a) punto x", "(b) regla graduada wᵀ (el gradiente)", "(c) parche curvo r(u, v)"],
                                value="(b) regla graduada wᵀ (el gradiente)", label="objeto")
    caso = mo.ui.dropdown(options=list(casos), value="estirar Este ×2: diag(2, 1)", label="A (casos a y b)")
    parche = mo.ui.dropdown(options=list(parches), value="la loma r = (u, v, 2·exp(−(u²+v²)/8))", label="parche (caso c)")
    mo.vstack([
        mo.md(r"""
        ## 2. Manipulación

        Un selector con los tres objetos de la tabla. **(a)** Un punto $x = (1, 2)$ y una parcela: van con $A$. **(b)** La
        regla $w^T = (1, 1)$ (la cota $h = x + y$): sus marcas se arrastran con $A^{-1}$ y el mojón conserva su cota; se
        dibujan además la flecha perpendicular a las marcas nuevas **en el papel** y la bajada real del terreno, $Aw$,
        que es la perpendicular **con la métrica**. **(c)** Un parche curvo: el jacobiano arma la grilla tangente y
        $E, F, G$ dicen cuánto mide cada paso. Tres capas: gris antes, teal después, violeta el objeto. En (a) y (b),
        **reproducir** va de la identidad a $A$.
        """),
        mo.hstack([objeto_sel, caso, parche], widths="equal"),
    ])
    return caso, casos, objeto_sel, parche, parches


@app.cell
def _(mo, parche, parches):
    _tipo, _u, _v = parches[parche.value]
    u0 = mo.ui.slider(_u[0], _u[1], value=_u[3], step=_u[2], label="u₀ (φ) del punto", show_value=True)
    v0 = mo.ui.slider(_v[0], _v[1], value=_v[3], step=_v[2], label="v₀ (λ) del punto", show_value=True)
    return u0, v0


@app.cell
def _(angulo_g, caso, casos, esfera3d, go, lib, loma3d, mo, np, objeto_sel, parche, parches, u0, v0):
    A, que_pasa = casos[caso.value]
    x_pt = np.array([1.0, 2.0])
    w = np.array([1.0, 1.0])
    parcela = np.array([[1.0, 2.0], [3.0, 1.0], [3.0, 3.0], [2.0, 4.0]])
    rango = 6
    w_despues = lib.forma_transformada(w, A)
    g_despues = np.linalg.inv(A).T @ np.linalg.inv(A)  # la métrica del terreno, escrita en la grilla nueva
    tangente_despues = A @ lib.perp2(w)  # la curva de nivel, dibujada después
    ang_papel = angulo_g(A @ w, tangente_despues, np.eye(2))
    ang_terreno = angulo_g(A @ w, tangente_despues, g_despues)
    _es_rot = bool(np.allclose(A.T @ A, np.eye(2)))
    if _es_rot and not np.allclose(A, np.eye(2)):
        camino = [lib.rot2(t) for t in np.linspace(0, np.deg2rad(30), 30)]
    else:
        camino = [np.eye(2) + s * (A - np.eye(2)) for s in np.linspace(0, 1, 30)]
    _objeto = objeto_sel.value[:3]

    def _dinamicas_a(i):
        Mi = camino[i]
        f = go.Figure()
        lib.capa_despues(f, Mi, rango)
        lib.objeto(f, lib.transformar(parcela, Mi), nombre="parcela después", estelas=lib.estelas(parcela, camino[: i + 1]))
        lib.punto(f, Mi @ x_pt, nombre="x después = A x", texto=lib.vec_plano(Mi @ x_pt))
        return list(f.data)

    def _dinamicas_b(i):
        Mi = camino[i]
        wi = lib.forma_transformada(w, Mi)
        f = go.Figure()
        lib.capa_despues(f, Mi, rango, cuadrado=False, columnas=False)
        lib.rectas_de_nivel(f, wi, np.arange(-12, 13), rango, lib.TEAL_DESPUES, "marcas después: wᵀA⁻¹", destacar=0)
        lib.flecha(f, Mi @ x_pt, Mi @ x_pt + wi / np.linalg.norm(wi) * 1.5, lib.TEAL_DESPUES, "⊥ a las marcas en el papel", ancho=3)
        lib.flecha(f, Mi @ x_pt, Mi @ x_pt + Mi @ w / np.linalg.norm(Mi @ w) * 1.5, lib.COLORES[2], "A w: la subida real del terreno", ancho=4)
        lib.punto(f, Mi @ x_pt, nombre="mojón después", texto=f"cota {wi @ (Mi @ x_pt):g}")
        return list(f.data)

    if _objeto in ("(a)", "(b)"):
        _din = _dinamicas_a if _objeto == "(a)" else _dinamicas_b
        figura = lib.figura_plano(rango, f"{objeto_sel.value} · {caso.value}")
        lib.capa_antes(figura, rango, cuadrado=(_objeto == "(a)"))
        if _objeto == "(a)":
            lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
        else:
            lib.rectas_de_nivel(figura, w, np.arange(-12, 13), rango, lib.GRIS_ANTES, "marcas antes: wᵀ = (1, 1)", etiquetas=False, destacar=None, ancho=0.8)
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
        else:
            _vivos = rf"""
            **Números vivos (b)**

            - $A = {lib.matriz_coloreada(A)}$, $w^T = {lib.pmat(w.reshape(1, 2), dec=0)}$, $w'^T = w^T A^{{-1}} = {lib.pmat(w_despues.reshape(1, 2))}$
            - cota del mojón: antes $w^T x = {lib.num_tex(w @ x_pt)}$, después $w'^T (Ax) = {lib.num_tex(w_despues @ (A @ x_pt))}$ → `np.allclose`: `{bool(np.allclose(w @ x_pt, w_despues @ (A @ x_pt)))}`
            - métrica del terreno en la grilla nueva: $g' = A^{{-T}} A^{{-1}} = {lib.pmat(g_despues)}$
            - ángulo entre $Aw$ (gold) y la marca: en el papel $\mathbf{{{ang_papel:.1f}°}}$; con $g'$, $\mathbf{{{ang_terreno:.1f}°}}$
            """
        _panel = mo.md(_vivos + "\n\n**Qué pasa acá:** " + que_pasa)
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
        _panel = mo.vstack([u0, v0, mo.md(rf"""
            **Números vivos (c)** (radianes adentro)

            $$J = {lib.matriz_coloreada(J)}\ (3\times2), \qquad J^T J = {lib.pmat([[E, F], [F, G]])}$$

            - un paso $du = 1$ de la grilla mide $\sqrt{{E}} = {np.sqrt(E):.3f}$ sobre el parche; un paso $dv = 1$ mide $\sqrt{{G}} = {np.sqrt(G):.3f}$
            - ángulo entre los ejes locales $r_u$ y $r_v$: ${np.degrees(lib.angulo(J[:, 0], J[:, 1])):.1f}°$ ($F = 0$ si es recto)
            - chip 4: derivar es esta matriz; chip 3: $E, F, G$ es la métrica. Lo desarrolla [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html).
            """)], gap=0.6)
    mo.vstack([mo.ui.plotly(figura), _panel])
    return A, ang_papel, ang_terreno, g_despues, tangente_despues, w, w_despues, x_pt


@app.cell
def _(angulo_g, mo, np):
    A3 = np.diag([2.0, 1.0])
    w3 = np.array([1.0, 1.0])
    x3 = np.array([1.0, 2.0])
    w3_despues = w3 @ np.linalg.inv(A3)
    g3 = np.linalg.inv(A3).T @ np.linalg.inv(A3)
    t3 = A3 @ np.array([1.0, -1.0])
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, el cuaderno; derecha, numpy. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La cota no cambia (chip 2).** $A = \mathrm{diag}(2, 1)$, $w^T = (1, 1)$, $x = (1, 2)$.

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
            **3.2 El ángulo recto vive en el terreno (chip 3).** En el terreno la marca de la regla $(1, 1)$ tiene
            dirección $(1, -1)$ y la subida $w = (1, 1)$: $\langle (1,1), (1,-1)\rangle = 0$, recto. Dibujados con $A$:
            la marca va a $A(1, -1) = (2, -1)$ y la subida a $Aw = (2, 1)$.

            En el papel: $\cos\theta = \dfrac{(2,1)\cdot(2,-1)}{\sqrt5\,\sqrt5} = \dfrac{3}{5}$, $\theta = 53.1°$.

            Con la métrica del terreno escrita en el papel, $g' = A^{-T}A^{-1} = \mathrm{diag}(\tfrac14, 1)$:

            $$(2, 1)\,g'\,\binom{2}{-1} = 2\cdot\tfrac14\cdot2 + 1\cdot1\cdot(-1) = 1 - 1 = 0 \ \Rightarrow\ \theta = 90°.\ \checkmark$$

            La perpendicular del papel, $(\tfrac12, 1)$, es la regla $w^T A^{-1}$ leída como flecha: perpendicular con
            $g = I$, no con $g'$.
            """),
            mo.vstack([
                mo.md("```python\nAi = np.linalg.inv(A)\ng2 = Ai.T @ Ai\nsub = A @ w            # (2, 1)\nmarca = A @ [1., -1.]  # (2, -1)\ndef ang(a, b, g):\n    c = a @ g @ b\n    c /= np.sqrt((a@g@a)*(b@g@b))\n    return np.degrees(np.arccos(c))\nang(sub, marca, np.eye(2))\nang(sub, marca, g2)\n```"),
                mo.md(f"`g2` = `{np.round(g3, 3).tolist()}` · `sub` = `{(A3 @ w3).tolist()}` · `marca` = `{t3.tolist()}`  \n"
                      f"en el papel: `{angulo_g(A3 @ w3, t3, np.eye(2)):.1f}`° · con `g2`: `{angulo_g(A3 @ w3, t3, g3):.1f}`°"),
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

        Tres reflejos nuevos. **Una forma es un array fila** y la pongo **a la izquierda** de la matriz: `w @ A`; un punto
        va a la derecha, `A @ x` (numpy no distingue fila de columna, la diferencia la pongo yo con el lado).
        **No invierto si puedo resolver**: `w @ np.linalg.inv(A)` y `np.linalg.solve(A.T, w)` dan la misma fila, pero
        `solve` no arma la inversa entera. **El jacobiano se calcula**: `lib.jacobiana_numerica(r, u, v)` evalúa $r$ en
        $u \pm h$, $v \pm h$ y apila las dos columnas; `J.T @ J` es la tabla $E, F, G$ de la grilla tangente.
        """),
        mo.md("```python\nA = np.array([[2., 1.], [0., 1.]]); w = np.array([1., 1.])\nw @ np.linalg.inv(A)            # la regla arrastrada\nnp.linalg.solve(A.T, w)         # lo mismo, sin invertir\nJ = lib.jacobiana_numerica(loma3d, 2.0, 1.0)   # (3, 2)\nJ.T @ J                         # [[E, F], [F, G]]\n```"),
        mo.md(f"`w @ inv(A)` = `{np.round(_w @ np.linalg.inv(_A), 3).tolist()}` · `solve(A.T, w)` = `{np.round(np.linalg.solve(_A.T, _w), 3).tolist()}` · "
              f"`J.shape` = `{_J.shape}` · `J.T @ J` =\n```\n{np.round(_J.T @ _J, 3)}\n```"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Dos ejercicios de diagnóstico

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
        desplazamiento $(3, \tfrac12)$: no es la subida más empinada. Chip 1 (flecha = desplazamiento) y chip 3 (la grilla no mide metros).
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_b = mo.ui.code_editor(
        value="def angulo_g(a, b, g):\n    # a, b: arrays de 2; g: matriz 2x2 de la metrica\n    cos = ...          # a g b / sqrt((a g a)(b g b))\n    return ...         # en grados\n",
        language="python", min_height=120, label="ejercicio (b)",
    )
    mo.vstack([
        mo.md(r"""
        **(b) Código con hueco — medio** *("hay transformaciones que se definen completamente por qué propiedades de los
        objetos transformados mantienen").* Completá `angulo_g(a, b, g)`: el ángulo **en grados** entre `a` y `b` medido
        con la métrica `g`. Tenés `np`. Se verifica con `np.allclose` sobre $g' = \mathrm{diag}(\tfrac14, 1)$ (la de la
        sección 3) y diez métricas al azar; con `g = I` tiene que dar el ángulo de siempre.
        """),
        editor_b,
    ])
    return (editor_b,)


@app.cell
def _(angulo_g, editor_b, mo, np):
    _rng = np.random.default_rng(56798)
    _casos = [(np.array([2.0, 1.0]), np.array([2.0, -1.0]), np.diag([0.25, 1.0]))]
    while len(_casos) < 11:
        _B = _rng.uniform(-2, 2, (2, 2))
        _g = _B.T @ _B + 0.5 * np.eye(2)  # simétrica definida positiva
        _casos.append((_rng.uniform(-3, 3, 2), _rng.uniform(-3, 3, 2), _g))
    _esperado = np.array([angulo_g(a, b, g) for a, b, g in _casos])
    _ns = {"np": np}
    try:
        exec(editor_b.value, _ns)
        _obtenido = np.array([float(_ns["angulo_g"](a.copy(), b.copy(), g.copy())) for a, b, g in _casos])
        if np.allclose(_obtenido, _esperado, atol=1e-6):
            _res = mo.callout(mo.md(f"✅ coincide en los 11 casos: con $g'$ el ángulo de la sección 3 da `{_obtenido[0]:.1f}`°. El ángulo es una pregunta a la métrica."), kind="success")
        elif np.allclose(_obtenido, [angulo_g(a, b, np.eye(2)) for a, b, g in _casos], atol=1e-6):
            _res = mo.callout(mo.md(r"❌ ese es el ángulo con $g = I$: olvidaste la métrica. El producto interno es `a @ g @ b`, y los largos `np.sqrt(a @ g @ a)`."), kind="warn")
        elif np.allclose(_obtenido, np.radians(_esperado), atol=1e-6):
            _res = mo.callout(mo.md("❌ está en radianes: falta `np.degrees(...)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para `a = [2, 1]`, `b = [2, -1]`, `g = diag(1/4, 1)` esperaba `{_esperado[0]:.1f}` y obtuve `{_obtenido[0]:.3f}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré los cuatro chips con un ejemplo cada uno. Lo que los sostiene:

    - [apunte, sección 3: la mirada geométrica](../../apunte.pdf#nameddest=cap:03) ·
      [apunte, sección 4: el punto y sus coordenadas no son lo mismo](../../apunte.pdf#nameddest=cap:04)
    - [ficha de la clase 1](../../clases/01.html) · [ficha de la clase 4](../../clases/04.html) ·
      [ficha de la clase 9](../../clases/09.html) · [el camino](../../index.html)

    Dónde vuelve cada chip: el 1 en [Rotaciones I](../01a_punto_quieto/index.html); el 2 en
    [Formas lineales y dualidad](../06_formas_lineales/index.html); el 3 en
    [Producto interno](../02_producto_interno/index.html) y [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html);
    el 4 en esa misma y en [Curvatura](../12_curvatura/index.html).

    **Lo que viene:** [Rotaciones I — el punto no se movió](../01a_punto_quieto/index.html): el mismo mojón, dos
    sistemas de ejes, y la primera matriz recién al final.
    """)
    return


@app.cell
def _(A, A3, A_plano, ang_papel, ang_terreno, angulo_g, bajada, candidatos, esfera3d, g3, g_despues, lib, loma3d, mo, mojon, np, t3, tangente_despues, w, w3, w3_despues, w_despues, w_mojon, x3, x_pt):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _ok = lib.exacto
    _J = lib.jacobiana_numerica(esfera3d, np.deg2rad(45), 0.0)
    _checks = [
        ("predicción: cuatro candidatos distintos; gradiente (−1, −1), bajada (1, 1); ingenua (1, 1), ⊥ papel (1, 2), correcta (2, 1), curva (2, −1)",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4 and _ok(w_mojon, [-1, -1]) and _ok(bajada, [1, 1])
         and _ok(candidatos["ingenua"], [1, 1]) and _ok(candidatos["perp-dibujo"], [1, 2]) and _ok(candidatos["correcta"], [2, 1]) and _ok(candidatos["curva"], [2, -1])),
        ("la bajada dibujada es perpendicular a la curva dibujada con la métrica del terreno, no con la del papel",
         _ok(angulo_g(candidatos["correcta"], candidatos["curva"], np.linalg.inv(A_plano).T @ np.linalg.inv(A_plano)), 90.0, tol=1e-6)
         and not _ok(angulo_g(candidatos["correcta"], candidatos["curva"], np.eye(2)), 90.0, tol=1.0) and _ok(A_plano @ mojon, [4, 2])),
        ("sección 2: la cota del mojón se conserva con la regla arrastrada; g' = A⁻ᵀA⁻¹; Aw ⊥ marca con g' (90°) para la A elegida",
         _ok(w_despues @ (A @ x_pt), w @ x_pt) and _ok(w_despues, lib.forma_transformada(w, A)) and _ok(g_despues, np.linalg.inv(A).T @ np.linalg.inv(A))
         and _ok(tangente_despues, A @ lib.perp2(w)) and _ok(ang_terreno, 90.0, tol=1e-6) and 0.0 <= ang_papel <= 90.0 + 1e-9),
        ("3.1: (1, 1) diag(2, 1)⁻¹ = (1/2, 1) y lee 3 sobre (2, 2); (Aw)·(Ax) = 6",
         _ok(w3_despues, [0.5, 1]) and _ok(w3_despues @ (A3 @ x3), 3) and _ok((A3 @ w3) @ (A3 @ x3), 6)),
        ("3.2: g' = diag(1/4, 1); ángulo en el papel 53.13°, con g' 90°",
         _ok(g3, np.diag([0.25, 1.0])) and _ok(angulo_g(A3 @ w3, t3, np.eye(2)), np.degrees(np.arccos(0.6)), tol=1e-9) and _ok(angulo_g(A3 @ w3, t3, g3), 90.0, tol=1e-9)),
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
