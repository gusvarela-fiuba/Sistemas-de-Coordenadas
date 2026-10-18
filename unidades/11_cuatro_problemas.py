# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Cuatro problemas: regresión, círculos, Procrustes, regresión total (lección 11, molde v2 sobre cb104). Clase 11.

LECCIÓN ANTICIPADA: la clase no se dictó todavía en 2C2026; lectura del esqueleto 2025, pendiente de validar por la
cátedra. Una sola idea: los cuatro problemas son el mismo (más mediciones que incógnitas) y la mejor solución deja el
residuo perpendicular a lo que la matriz puede producir. Ecuaciones normales y `lstsq`; SVD y pseudoinversa en la 09.

Chequear:  uv run marimo check --select MW unidades/11_cuatro_problemas.py
Exportar:  uv run python tools/build.py --only 11_cuatro_problemas
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
    # Cuatro problemas: regresión, círculos, Procrustes, regresión total

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    *Lección anticipada: la clase no se dictó todavía; lo que sigue desarrolla el esqueleto 2025, pendiente de validar
    por la cátedra.*

    Seguimos la clase 11. La pregunta: **¿Qué tienen en común ajustar una recta, ubicar un punto por distancias, superponer
    dos relevamientos y ajustar una recta con error en las dos coordenadas?** El gancho: *compensar un relevamiento con
    más mediciones que incógnitas: la misma cuenta resuelve la recta de ajuste y la transformación entre dos sistemas de
    mojones.*

    Colores: lo **medido** en <span style="color:#7a4e9e">**violeta**</span>, la **solución** (recta, punto, nube
    llevada) en <span style="color:#1b6f6a">**teal**</span>, los **residuos** como segmentos finos punteados. En las
    matrices, primera columna teal y segunda rust, como siempre.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("11_cuatro_problemas"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    mojones = np.array([[0.0, 0.0], [8.0, 0.0], [8.0, 7.0], [1.0, 8.0]])
    punto_real = np.array([3.0, 4.0])
    dist_medidas = np.array([5.05, 6.35, 5.90, 4.45])  # cinta: las exactas son 5, 6.403, 5.831, 4.472
    p_mc, r_mc = lib.punto_por_distancias(mojones, dist_medidas)
    p_tres, _ = lib.punto_por_distancias(mojones[:3], dist_medidas[:3])
    errores_mc = np.linalg.norm(mojones - p_mc, axis=1) - dist_medidas
    errores_tres = np.linalg.norm(mojones - p_tres, axis=1) - dist_medidas
    prediccion = mo.ui.radio(
        options={
            "usamos tres mojones, resolvemos exacto y descartamos la cuarta distancia": "tres",
            "no hay punto: las cuatro distancias se contradicen": "ninguno",
            "el punto que deja las cuatro diferencias lo más chicas posible en conjunto": "correcta",
            "el promedio de los cuatro mojones, pesado por las distancias": "promedio",
        },
        value=None,
        label="**Predicción.** ¿Qué punto anotamos como posición del poste?",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Tenemos que ubicar un poste en el sistema del lote. Cuatro mojones de coordenadas conocidas, en metros:
        $M_1 = (0, 0)$, $M_2 = (8, 0)$, $M_3 = (8, 7)$, $M_4 = (1, 8)$. Medimos con cinta las distancias del poste a cada
        uno: $5.05$, $6.35$, $5.90$ y $4.45$ m. Dos distancias ya definen el punto (salvo el espejo); con cuatro sobran
        dos. Y la cinta tiene error: ningún punto está **exactamente** a esas cuatro distancias. Dos incógnitas, cuatro mediciones.
        """),
        prediccion,
    ])
    return dist_medidas, errores_mc, errores_tres, mojones, p_mc, p_tres, prediccion, punto_real, r_mc


@app.cell
def _(errores_mc, errores_tres, lib, mo, p_mc, p_tres, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** Es la idea de toda la lección: con más mediciones que incógnitas no buscamos el punto que cumple todo "
                     rf"(no existe) sino el que deja el **residuo** más chico en conjunto, suma de cuadrados: $p = {lib.vec_tex(p_mc, 3)}$, "
                     rf"diferencias $({', '.join(lib.num_tex(e, 3) for e in errores_mc)})$ m repartidas entre las cuatro cintas. "
                     rf"La sección 1 dice **por qué** ese residuo queda perpendicular a lo que las ecuaciones pueden producir."),
        "tres": ("warn",
                 rf"**No.** Con tres mojones las dos rectas de la sección 1 se cortan en un punto, $p = {lib.vec_tex(p_tres, 3)}$, pero "
                 rf"ese punto tampoco cumple las cintas (tienen error) y la cuarta queda con ${lib.num_tex(errores_tres[3], 3)}$ m que nadie "
                 rf"reparte. Peor: depende de **cuáles** tres elegimos. Con las cuatro: $({', '.join(lib.num_tex(e, 3) for e in errores_mc)})$ m."),
        "ninguno": ("warn",
                    r"**No.** Que se contradigan es lo normal: toda medición tiene error. La pregunta cambia de '¿qué punto cumple "
                    r"las cuatro?' a '¿cuál las cumple **lo mejor posible**?', y esa sí tiene respuesta única."),
        "promedio": ("warn",
                     r"**No.** Promediar mojones da un punto adentro del lote, pero no usa las distancias como distancias: nada "
                     r"dice que el error de las cintas quedó chico. La solución sí es 'un promedio', pero de las **ecuaciones**, "
                     r"con los pesos que impone la geometría ($A^\top A$)."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Más ecuaciones que incógnitas: $A x = y$ no tiene solución.** $A$ es alta ($n$ filas, $2$ columnas) y lo que puede
    producir, $\{A x\}$, es apenas un plano (la **imagen**, 07b) adentro de $\mathbb R^n$; el vector $y$ de mediciones no
    cae en él. Lo mejor es el punto del plano **más cercano** a $y$: su sombra, la proyección ortogonal (lección 02). Y
    la sombra se reconoce por una sola propiedad: lo que sobra, el **residuo** $r = y - A x$, es **perpendicular al
    plano**, o sea a cada columna de $A$:

    $$A^\top (y - A x) = 0 \iff A^\top A\, x = A^\top y \qquad \text{(ecuaciones normales).}$$

    El sistema alto se volvió uno de $2\times2$. Esto es una **muestra**; la demostración (que la sombra minimiza
    $|r|^2$) está en Strang, y la pseudoinversa $A^+ = (A^\top A)^{-1}A^\top$ y la SVD se desarrollan en la unidad 09.

    | | la cuenta | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $n$ medidas de **un** largo: $A$ es una columna de unos, $A^\top A = n$, $A^\top y = \sum y_i$ | el **promedio**; el residuo suma cero |
    | $\mathbb R^2$ | $A = [\,x \mid 1\,]$, $x = (a, b)$: la recta $y = ax + b$ | residuos verticales, perpendiculares a las dos columnas |
    | $\mathbb R^n$ | cualquier $A$ alta: $A^\top A\, x = A^\top y$ | la fórmula no se entera de cuántas mediciones hay |

    **Los cuatro problemas son este mismo problema**, con la incógnita cambiando de ropa:

    - **(a) recta de ajuste**: incógnitas $(a, b)$, $A = [\,x \mid 1\,]$, directo.
    - **(b) punto por distancias**: cada mojón da un círculo $(x - a_i)^2 + (y - b_i)^2 = d_i^2$, no lineal; pero
      **restar dos círculos cancela $x^2 + y^2$** y deja una recta (el eje radical). $m$ mojones, $m - 1$ rectas, $A x \approx b$.
    - **(c) Procrustes**: dos relevamientos del mismo lote; la incógnita es **giro, escala y traslación**. Centramos las
      nubes y la rotación sale de la SVD de $H = P_0^\top Q_0$: $R = V U^\top$ (una frase; la SVD es de la unidad 09).
    - **(d) regresión total**: la recta que minimiza las distancias **perpendiculares**. Pasa por el centroide con la
      **dirección propia de mayor autovalor** de $C = X_0^\top X_0$ (07b, 08); la normal es la de menor, y ese
      autovalor es la suma de residuos al cuadrado.

    **¿Qué se conserva?** (a), (b): el residuo perpendicular a la imagen. (c): distancias y ángulos dentro de cada
    nube. (d): la dirección que menos cambia bajo $C$.
    """)
    return


@app.cell
def _(mo):
    casos = {
        "(a) recta de ajuste: y = ax + b por nueve puntos": ("recta", "ruido en y (m)"),
        "(b) punto por distancias a cuatro mojones": ("circulos", "error de cinta (m)"),
        "(c) Procrustes: dos relevamientos del mismo lote": ("procrustes", "ruido del segundo relevamiento (m)"),
        "(d) regresión total: error en x y en y": ("total", "ruido en x y en y (m)"),
    }
    caso = mo.ui.dropdown(options=list(casos), value=list(casos)[0], label="problema")
    mo.md(r"""
    ## 2. Manipulación

    Elegí el problema y subí el **ruido** en el panel de la derecha (misma semilla: el ruido es la única diferencia).
    Los residuos (punteados) crecen pero siguen **repartidos**, y la comprobación $A^\top r \approx 0$ no cambia. Con
    ruido $0$ la solución es exacta.
    """)
    return caso, casos


@app.cell
def _(caso, casos, mo):
    ruido = mo.ui.slider(0, 1, value=0.3, step=0.05, label=casos[caso.value][1], show_value=True)
    return (ruido,)


@app.cell
def _(caso, casos, go, lib, mo, np, ruido):
    tipo = casos[caso.value][0]
    _rng = np.random.default_rng(56798)
    sig = ruido.value
    rango = (-1, 11)
    figura = lib.figura_plano(rango, caso.value)
    lib.capa_antes(figura, rango, cuadrado=False)

    def _segs(P, Q, nombre):
        _xs, _ys = [], []
        for _p, _q in zip(P, Q):
            _xs += [_p[0], _q[0], None]
            _ys += [_p[1], _q[1], None]
        figura.add_trace(go.Scatter(x=_xs, y=_ys, mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=1.2, dash="dot"), name=nombre, hoverinfo="skip"))

    def _nube(P, color, nombre, tam=8):
        figura.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="markers", marker=dict(size=tam, color=color), name=nombre))

    def _recta(c, d, color, nombre, dash=None):
        _a, _b = c - 9 * d, c + 9 * d
        figura.add_trace(go.Scatter(x=[_a[0], _b[0]], y=[_a[1], _b[1]], mode="lines", line=dict(color=color, width=2.5, dash=dash), name=nombre))

    xs9 = np.arange(1.0, 10.0)
    if tipo == "recta":
        ys9 = 0.6 * xs9 + 1.5 + sig * _rng.normal(size=9)
        A = np.column_stack([xs9, np.ones(9)])
        sol, res = lib.minimos_cuadrados(A, ys9)
        _P = np.column_stack([xs9, ys9])
        _segs(_P, np.column_stack([xs9, A @ sol]), "residuos (verticales)")
        _nube(_P, lib.VIOLETA_OBJETO, "puntos medidos")
        _recta(np.array([0, sol[1]]), np.array([1, sol[0]]) / np.hypot(1, sol[0]), lib.TEAL_DESPUES, f"ajuste: y = {sol[0]:.3f}x + {sol[1]:.3f}")
        numeros = rf"""
        - $A = [\,x \mid 1\,]$ de $9\times2$ · $A^\top A = {lib.matriz_coloreada(A.T @ A, 1)}$ · $A^\top y = {lib.vec_tex(A.T @ ys9, 2)}$
        - $(a, b) = \mathbf{{{lib.vec_tex(sol, 3)}}}$ (sin ruido: $(0.6, 1.5)$) · $\lvert r\rvert = {lib.num_tex(np.linalg.norm(res), 3)}$
        - comprobación $A^\top r = {lib.vec_tex(A.T @ res, 6)}$: perpendicular a la columna $x$ y a la de unos (suma cero).
        """
    elif tipo == "circulos":
        M = np.array([[0.0, 0.0], [8.0, 0.0], [8.0, 7.0], [1.0, 8.0]])
        d = np.linalg.norm(M - [3.0, 4.0], axis=1) + sig * _rng.normal(size=4)
        sol, res = lib.punto_por_distancias(M, d)
        A = 2.0 * (M[1:] - M[0])
        _b = d[0] ** 2 - d[1:] ** 2 - M[0] @ M[0] + np.sum(M[1:] ** 2, axis=1)
        for _i, (_m, _d) in enumerate(zip(M, d)):
            _c = lib.circulo() * _d + _m
            figura.add_trace(go.Scatter(x=_c[:, 0], y=_c[:, 1], mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=1), opacity=0.6, name=f"cinta desde M{_i + 1}: {_d:.2f} m", hoverinfo="skip"))
            lib.punto(figura, _m, lib.GRIS_ANTES, f"mojón M{_i + 1}", tam=11, texto=f"M{_i + 1}")
        _dir = (sol - M) / np.linalg.norm(sol - M, axis=1)[:, None]
        _segs(np.tile(sol, (4, 1)), M + d[:, None] * _dir, "residuos (a cada círculo)")
        lib.punto(figura, sol, lib.TEAL_DESPUES, f"poste: ({sol[0]:.3f}, {sol[1]:.3f})", tam=13, texto="p")
        numeros = rf"""
        - tres ejes radicales: $A = {lib.matriz_coloreada(A, 0)}$, $b = {lib.vec_tex(_b, 2)}$ · $A^\top A = {lib.matriz_coloreada(A.T @ A, 0)}$
        - $p = \mathbf{{{lib.vec_tex(sol, 3)}}}$ (real: $(3, 4)$) · $\lvert r\rvert = {lib.num_tex(np.linalg.norm(res), 3)}$ · $A^\top r = {lib.vec_tex(A.T @ res, 6)}$
        - diferencias cinta a cinta: $({', '.join(lib.num_tex(e, 3) for e in np.linalg.norm(M - sol, axis=1) - d)})$ m.
        """
    elif tipo == "procrustes":
        P = np.array([[1.0, 1.0], [4.0, 1.0], [5.0, 3.0], [3.0, 5.0], [1.0, 4.0], [3.0, 3.0], [2.0, 2.0]])
        Q = 1.2 * lib.transformar(P, lib.rot2(np.deg2rad(25))) + [1.5, 0.5] + sig * _rng.normal(size=P.shape)
        R, esc, tras, rms = lib.procrustes(P, Q)
        Pl = esc * lib.transformar(P, R) + tras
        _H = (P - P.mean(0)).T @ (Q - Q.mean(0))
        lib.objeto(figura, P[:5], lib.GRIS_ANTES, "relevamiento 1 (su sistema)", relleno=False)
        _segs(Pl, Q, "residuos")
        lib.objeto(figura, Q[:5], lib.VIOLETA_OBJETO, "relevamiento 2 (medido)", relleno=False)
        _nube(Q[5:], lib.VIOLETA_OBJETO, "interiores, relevamiento 2")
        lib.objeto(figura, Pl[:5], lib.TEAL_DESPUES, "relevamiento 1 llevado: s R p + t")
        numeros = rf"""
        - $H = P_0^\top Q_0 = {lib.matriz_coloreada(_H, 2)}$ · $R = {lib.matriz_coloreada(R)}$, giro $\theta = \mathbf{{{np.degrees(np.arctan2(R[1, 0], R[0, 0])):.2f}°}}$
        - $s = \mathbf{{{lib.num_tex(esc, 4)}}}$ · $t = {lib.vec_tex(tras, 3)}$ · rms $= {lib.num_tex(rms, 3)}$ m (sin ruido: $25°$, $1.2$, $(1.5, 0.5)$)
        - comprobación $\sum_i \langle r_i, R p_{{0i}}\rangle = {lib.num_tex(np.sum((Q - Pl) * lib.transformar(P - P.mean(0), R)), 6)}$: residuo perpendicular a la nube llevada.
        """
    else:
        X = np.column_stack([xs9, 0.6 * xs9 + 1.5]) + sig * _rng.normal(size=(9, 2))
        cen, dvec, nvec, r2 = lib.regresion_total(X)
        ab = lib.recta_ajuste(X[:, 0], X[:, 1])
        _C = (X - cen).T @ (X - cen)
        _lam = np.linalg.eigvalsh(_C)
        _pie = cen + ((X - cen) @ dvec)[:, None] * dvec
        _segs(X, _pie, "residuos (perpendiculares)")
        _nube(X, lib.VIOLETA_OBJETO, "puntos medidos")
        _recta(cen, dvec, lib.TEAL_DESPUES, "regresión total")
        _recta(np.array([0, ab[1]]), np.array([1, ab[0]]) / np.hypot(1, ab[0]), lib.COLORES[1], "regresión simple (vertical), para comparar", "dash")
        numeros = rf"""
        - $C = X_0^\top X_0 = {lib.matriz_coloreada(_C, 2)}$ · autovalores $\lambda = ({lib.num_tex(_lam[1], 3)},\ {lib.num_tex(_lam[0], 3)})$
        - dirección $d = \mathbf{{{lib.vec_tex(dvec, 4)}}}$ (pendiente ${lib.num_tex(dvec[1] / dvec[0], 3)}$; la simple da ${lib.num_tex(ab[0], 3)}$) · normal $n = {lib.vec_tex(nvec, 4)}$
        - $\sum r_i^2 = \lambda_{{\min}} = {lib.num_tex(r2, 4)}$ · comprobación $d^\top C\, n = {lib.num_tex(dvec @ _C @ nvec, 6)}$: residuos perpendiculares a la recta, sin correlación con el avance sobre ella.
        """
    _panel = mo.vstack([mo.md("**Controles**"), caso, ruido, mo.md("**Números vivos**\n" + numeros)], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return


@app.cell
def _(lib, mo, np):
    _A = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    _y = np.array([0.0, 1.0, 3.0])
    _x, _r = lib.minimos_cuadrados(_A, _y)
    _x2 = np.linalg.lstsq(_A, _y, rcond=None)[0]
    _p, _rp = lib.punto_por_distancias([[0, 0], [6, 0], [3, 7]], [5, 5, 3])
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, el cuaderno; derecha, numpy. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Recta por tres puntos.** Un alambrado que debería ser recto, relevado en $(0, 0)$, $(1, 1)$, $(2, 3)$:
            no están alineados (pendientes $1$ y $2$). Buscamos $y = ax + b$:

            $$A = \begin{pmatrix} \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{2} & \textcolor{#b5451b}{1} \end{pmatrix},\quad
            A^\top A = \begin{pmatrix} 5 & 3 \\ 3 & 3 \end{pmatrix},\quad A^\top y = \begin{pmatrix} 7 \\ 4 \end{pmatrix}.$$

            $5a + 3b = 7$ y $3a + 3b = 4$; restando, $2a = 3$, $a = \tfrac32$; entonces $3b = 4 - \tfrac92$, $b = -\tfrac16$.
            Residuo $r = (\tfrac16, -\tfrac13, \tfrac16)$: suma cero (columna de unos) y
            $0\cdot\tfrac16 - \tfrac13 + 2\cdot\tfrac16 = 0$ (columna $x$): perpendicular a las dos.
            """),
            mo.vstack([
                mo.md("```python\nA = np.column_stack([[0., 1., 2.], np.ones(3)])\ny = np.array([0., 1., 3.])\nx = np.linalg.solve(A.T @ A, A.T @ y)\nr = y - A @ x\nA.T @ r\nnp.allclose(x, np.linalg.lstsq(A, y, rcond=None)[0])\n```"),
                mo.md(f"`x` = `{np.round(_x, 4).tolist()}` · `r` = `{np.round(_r, 4).tolist()}`  \n`A.T @ r` = `{np.round(_A.T @ _r, 12).tolist()}` · `lstsq` coincide: `{bool(np.allclose(_x, _x2))}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 Tres círculos, un punto.** Mojones $(0, 0)$, $(6, 0)$, $(3, 7)$ a distancias $5$, $5$, $3$:

            $$x^2 + y^2 = 25,\qquad (x - 6)^2 + y^2 = 25,\qquad (x - 3)^2 + (y - 7)^2 = 9.$$

            Primero menos segundo: $12x - 36 = 0$, $x = 3$. Primero menos tercero: $6x + 14y - 58 = 16$, o sea
            $6x + 14y = 74$; con $x = 3$, $y = 4$. Las dos rectas son los ejes radicales y
            $A = 2\,(M_i - M_1)$ por filas: $\begin{pmatrix} 12 & 0 \\ 6 & 14 \end{pmatrix}$, $b = (36, 74)$.
            Control: $9 + 16 = 25$ ✓, $9 + 16 = 25$ ✓, $0 + 9 = 9$ ✓. Sin el tercero quedaban $(3, \pm4)$: la tercera cinta elige.
            """),
            mo.vstack([
                mo.md("```python\nM = np.array([[0., 0.], [6., 0.], [3., 7.]])\nd = np.array([5., 5., 3.])\nA = 2 * (M[1:] - M[0])\nb = d[0]**2 - d[1:]**2 - M[0] @ M[0] + np.sum(M[1:]**2, axis=1)\np = np.linalg.solve(A, b)\nnp.allclose(np.linalg.norm(M - p, axis=1), d)\n```"),
                mo.md(f"`p` = `{np.round(_p, 6).tolist()}` · residuo `{np.round(_rp, 12).tolist()}` · distancias: `{bool(np.allclose(np.linalg.norm(np.array([[0, 0], [6, 0], [3, 7]]) - _p, axis=1), [5, 5, 3]))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(mo, np):
    _A = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    _sol = np.linalg.lstsq(_A, np.array([0.0, 1.0, 3.0]), rcond=None)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **`np.linalg.lstsq(A, y, rcond=None)` resuelve el sistema alto** y devuelve cuatro cosas: la
        solución, la suma de residuos al cuadrado, el rango de $A$ y sus valores singulares (unidad 09). La matriz alta
        se arma con `np.column_stack([xs, np.ones(n)])`: una columna por incógnita, una fila por medición. `lstsq` no
        forma $A^\top A$ (va por SVD, más estable), pero da la misma respuesta.
        """),
        mo.md("```python\nA = np.column_stack([[0., 1., 2.], np.ones(3)])    # shape (3, 2)\nx, res2, rango, sigmas = np.linalg.lstsq(A, [0., 1., 3.], rcond=None)\n```"),
        mo.md(f"`x` = `{np.round(_sol[0], 4).tolist()}` · `res2` = `{np.round(_sol[1], 4).tolist()}` ($= \\lvert r\\rvert^2 = \\tfrac16$) · `rango` = `{_sol[2]}` · `sigmas` = `{np.round(_sol[3], 4).tolist()}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("el punto de la entrada que corresponde en la salida a lo más cercano al término
        independiente").* Medimos tres veces el mismo lado: $12.1$, $11.9$ y $12.3$ m. Escribí $Ax = y$ con $A$ la columna
        de unos, las ecuaciones normales, la solución y el residuo. ¿Qué cuenta conocida es?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $A = (1, 1, 1)^\top$, $A^\top A = 3$, $A^\top y = 36.3$: $x = 12.1$, el **promedio**. Residuo $(0, -0.2, 0.2)$,
        que suma cero: perpendicular a la columna de unos. Promediar es proyectar sobre la recta de $(1, 1, 1)$.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("resolver un sistema de ecuaciones sobre-determinado").* Puntos $(-1, 1)$, $(0, 1)$,
        $(1, 4)$. Ajustá $y = ax + b$ con las ecuaciones normales (fijate que $A^\top A$ sale diagonal porque las $x$
        están centradas), calculá el residuo y comprobá que es perpendicular a las dos columnas.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $A^\top A = \begin{pmatrix} 2 & 0 \\ 0 & 3 \end{pmatrix}$, $A^\top y = (3, 6)$: $a = \tfrac32$, $b = 2$, recta
        $y = \tfrac32 x + 2$. Residuo $r = (1 - \tfrac12,\ 1 - 2,\ 4 - \tfrac72) = (\tfrac12, -1, \tfrac12)$: suma cero
        y $-\tfrac12 + 0 + \tfrac12 = 0$ contra la columna $x$. ✓
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def ajustar_recta(xs, ys):\n    A = ...            # una fila por punto: [x_i, 1]\n    x = ...            # resolver las ecuaciones normales (o lstsq)\n    return x[0], x[1]  # (a, b) de y = a x + b\n",
        language="python", min_height=130, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio.** Completá `ajustar_recta(xs, ys)`: dos arrays de $n$ → `(a, b)` de la recta de
        mínimos cuadrados $y = ax + b$. Tenés `np`. Se verifica con `np.allclose` sobre tres nubes al azar y la de la sección 3.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(11)
    _nubes = [(np.array([0.0, 1.0, 2.0]), np.array([0.0, 1.0, 3.0]))] + [(_rng.uniform(0, 10, 8), _rng.uniform(-5, 5, 8)) for _ in range(3)]
    _esp = np.array([lib.recta_ajuste(x, y) for x, y in _nubes])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obt = np.array([[float(v) for v in _ns["ajustar_recta"](x, y)] for x, y in _nubes])
        _sin_unos = np.array([[float(x @ y / (x @ x)), 0.0] for x, y in _nubes])
        _mal_div = np.array([[float(((x - x.mean()) @ (y - y.mean())) / ((y - y.mean()) @ (y - y.mean()))), np.nan] for x, y in _nubes])
        if np.allclose(_obt, _esp):
            _res = mo.callout(mo.md("✅ coincide en las cuatro nubes: $(a, b) = (A^\\top A)^{-1} A^\\top y$."), kind="success")
        elif np.allclose(_obt, _esp[:, ::-1]):
            _res = mo.callout(mo.md("❌ devolvés `(b, a)`: las columnas de `A` son `[x, 1]`, así que la **primera** incógnita es la pendiente."), kind="warn")
        elif np.allclose(_obt, _sin_unos):
            _res = mo.callout(mo.md("❌ te olvidaste la **columna de unos**: así la recta pasa por el origen a la fuerza ($b = 0$) y la pendiente queda $\\sum x y / \\sum x^2$."), kind="warn")
        elif np.allclose(_obt[:, 0], _mal_div[:, 0]):
            _res = mo.callout(mo.md("❌ dividiste por la dispersión de $y$: la pendiente es $S_{xy} / S_{xx}$, y sale sola de $A^\\top A$ (no hace falta centrar)."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para la nube de la sección 3 se esperaba `{np.round(_esp[0], 4).tolist()}` y se obtuvo `{np.round(_obt[0], 4).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def punto_por_distancias(M, d):\n    A = ...      # (m−1)×2: restar el primer mojón a los demás, por 2\n    b = ...      # d0² − di² − |M0|² + |Mi|²\n    p, r = minimos_cuadrados(A, b)\n    return p\n",
        language="python", min_height=140, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado.** Completá `punto_por_distancias(M, d)`: `M` es $m\times2$ (mojones), `d` las
        $m$ distancias; devolvé $p$. Tenés `np` y `minimos_cuadrados(A, b)` (devuelve `(x, r)`). Se verifica con el caso
        de la sección 3 y dos juegos de cuatro mojones al azar.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(14)
    _casos = [(np.array([[0.0, 0.0], [6.0, 0.0], [3.0, 7.0]]), np.array([3.0, 4.0]))] + [(_rng.uniform(0, 10, (4, 2)), _rng.uniform(0, 10, 2)) for _ in range(2)]
    _ns = {"np": np, "minimos_cuadrados": lib.minimos_cuadrados}
    try:
        exec(editor_d.value, _ns)
        _fallas = []
        for _i, (_M, _p) in enumerate(_casos, 1):
            _d = np.linalg.norm(_M - _p, axis=1)
            _obt = np.asarray(_ns["punto_por_distancias"](_M, _d), dtype=float).reshape(-1)
            _A = 2 * (_M[1:] - _M[0])
            _b = _d[0] ** 2 - _d[1:] ** 2 - _M[0] @ _M[0] + np.sum(_M[1:] ** 2, axis=1)
            if np.allclose(_obt, _p):
                continue
            if np.allclose(_obt, lib.minimos_cuadrados(_A, -_b)[0]):
                _fallas.append(f"caso {_i}: signo al revés en `b` (restaste los círculos en un orden en `A` y en el otro en `b`)")
            elif np.allclose(_obt, 2 * _p):
                _fallas.append(f"caso {_i}: falta el factor 2 en `A` (el punto sale el doble de lejos)")
            else:
                _fallas.append(f"caso {_i}: se esperaba `{np.round(_p, 3).tolist()}`, se obtuvo `{np.round(_obt, 3).tolist()}`; ¿restaste la primera ecuación a las demás? Sin restar no es lineal")
        _res = (mo.callout(mo.md("✅ los tres casos: el punto está a las distancias pedidas de todos los mojones."), kind="success")
                if not _fallas else mo.callout(mo.md("❌ " + "; ".join(_fallas) + "."), kind="warn"))
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá verificamos que los cuatro problemas se resuelven dejando el residuo perpendicular a lo que la matriz puede producir.
    Las demostraciones (la proyección minimiza $|r|^2$; por qué $R = VU^\top$; por qué la dirección propia mayor es la
    recta total) están desarrolladas en la guía resuelta del apunte; de fondo, Strang y Calvetti–Somersalo, nombrados
    por el profesor el 2026-10-14.

    - [apunte, sección "Guía resuelta de los cuatro problemas (Clase 11)"](../../apunte.pdf#nameddest=sec:cuatro-problemas):
      Problema 1, regresión simple (la mejor recta como proyección ortogonal, residuo perpendicular a las columnas) ·
      Problema 2, intersección de círculos (trilateración) · Problema 3, Procrustes ortogonal (SVD de $H$, $R = UV^\top$,
      con la caja sobre la convención de $H$) · Problema 4, regresión total (la dirección de la recta es $v_1$, la
      normal es $v_2$, el menor valor singular); cierra con el resultado "Los cuatro con la misma maquinaria"
    - [apunte, sección "Sistemas de ecuaciones y aplicaciones"](../../apunte.pdf#nameddest=sec:sistemas-ecuaciones) · [sección 11: producto interno y núcleo](../../apunte.pdf#nameddest=cap:11)
    - [ficha de la clase 11](../../clases/11.html) · [lección anterior: cambio de base](../08_cambio_de_base/index.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** [curvatura como forma cuadrática](../12_curvatura/index.html): la matriz $C = X_0^\top X_0$ de la
    regresión total es una forma cuadrática, y sus direcciones propias vuelven como direcciones principales de una
    superficie. La [unidad 09 (SVD y pseudoinversa)](../09_cambio_de_base_svd/index.html) le pone nombre a lo que acá
    hizo `lstsq`.
    """)
    return


@app.cell
def _(dist_medidas, errores_mc, errores_tres, lib, mo, mojones, np, p_mc, p_tres, punto_real, r_mc):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _A = 2 * (mojones[1:] - mojones[0])
    _A3 = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    _x3, _r3 = lib.minimos_cuadrados(_A3, [0.0, 1.0, 3.0])
    _Ab = np.column_stack([[-1.0, 0.0, 1.0], np.ones(3)])
    _xb, _rb = lib.minimos_cuadrados(_Ab, [1.0, 1.0, 4.0])
    _checks = [
        ("sección 0: p a menos de 10 cm del real, Aᵀr = 0",
         np.linalg.norm(p_mc - punto_real) < 0.1 and lib.exacto(_A.T @ r_mc, [0, 0], tol=1e-8)),
        ("sección 0: con tres mojones la cuarta cinta lleva el error máximo; con cuatro baja",
         abs(errores_tres[3]) == np.abs(errores_tres).max() and np.abs(errores_mc).max() < abs(errores_tres[3])),
        ("3.1: y = 1.5x − 1/6, r = (1/6, −1/3, 1/6), Aᵀr = 0, igual que lstsq",
         lib.exacto(_x3, [1.5, -1 / 6]) and lib.exacto(_r3, [1 / 6, -1 / 3, 1 / 6]) and lib.exacto(_A3.T @ _r3, [0, 0])
         and lib.exacto(_x3, np.linalg.lstsq(_A3, np.array([0.0, 1.0, 3.0]), rcond=None)[0])),
        ("3.2: tres círculos → (3, 4); sin el tercero, (3, −4) también cumple",
         lib.exacto(lib.punto_por_distancias([[0, 0], [6, 0], [3, 7]], [5, 5, 3])[0], [3, 4])
         and lib.exacto(np.linalg.norm(np.array([[0, 0], [6, 0]]) - [3, -4], axis=1), [5, 5])),
        ("ejercicio (a): el promedio 12.1 con residuo de suma cero",
         lib.exacto(lib.minimos_cuadrados(np.ones((3, 1)), [12.1, 11.9, 12.3])[0], [12.1]) and lib.exacto(np.sum([0, -0.2, 0.2]), 0.0)),
        ("ejercicio (b): y = 1.5x + 2, r = (1/2, −1, 1/2), Aᵀr = 0",
         lib.exacto(_xb, [1.5, 2]) and lib.exacto(_rb, [0.5, -1, 0.5]) and lib.exacto(_Ab.T @ _rb, [0, 0])),
        ("las cintas de la situación no son las exactas",
         not lib.exacto(dist_medidas, np.linalg.norm(mojones - punto_real, axis=1), tol=1e-3)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
