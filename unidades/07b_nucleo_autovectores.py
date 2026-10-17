# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Núcleo y autovectores: las direcciones que no giran (lección 07b, molde v2 sobre cb104). Clases 5 y 6.

Una sola idea: el núcleo son los vectores que van al cero (ahí la transformación aplasta: det = 0); un autovector es
una dirección que la transformación no gira, sólo estira por λ; encontrarlos es buscar el núcleo de A − λI, y el
detector det(A − λI) = 0 dice para qué λ ese núcleo existe. El autovector sale como la perpendicular a una fila
(en 3D, la cruz de dos filas): el método del profesor.

Chequear:  uv run marimo check --select MW unidades/07b_nucleo_autovectores.py
Exportar:  uv run python tools/build.py --only 07b_nucleo_autovectores
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
    # Núcleo y autovectores: las direcciones que no giran

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Sigo las clases 5 y 6. La pregunta: **¿qué direcciones caen sobre sí mismas al transformar, y cómo las encuentro
    con una cuenta?** El gancho: *un plano deformado por el escáner: casi todos los rumbos giran, pero hay dos que
    salen con el mismo rumbo que entraron; el eje de una rotación es la dirección que no gira.*

    Colores, iguales en la figura y en el álgebra: **primera columna** <span style="color:#1b6f6a">**teal**</span>,
    **segunda** <span style="color:#b5451b">**rust**</span> (a dónde van $e_1$ y $e_2$). Las direcciones propias van en
    **negro a rayas**, la parcela y la flecha de prueba en <span style="color:#7a4e9e">**violeta**</span>, lo de antes
    en gris, lo de después en teal.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    A_esc = np.array([[2.0, 1.0], [1.0, 2.0]])  # la deformación del escáner
    propios_esc = lib.autovectores_cuna(A_esc)
    n_propias = sum(1 for p in propios_esc if not p["plano"])
    etiquetas = {0: "ninguno", 1: "uno solo", 2: "dos", 3: "todos"}
    candidatos = {"correcta": n_propias, "giro": 0, "corte": 1, "homotecia": 3}
    prediccion = mo.ui.radio(
        options={etiquetas[candidatos[k]]: k for k in ("giro", "corte", "correcta", "homotecia")},
        value=None,
        label=r"**Predicción.** Después de $A$, ¿cuántos rumbos de la parcela salen con **el mismo rumbo** que entraron (estirados o no)?",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Un plano viejo pasó por un escáner que lo deformó con la matriz $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$
        (lección 04): $e_1 = (1, 0)$ va a $(2, 1)$ y $e_2 = (0, 1)$ va a $(1, 2)$. Los dos ejes **giran**: el eje $x$ se
        levanta y el eje $y$ se acuesta, y con ellos gira casi cualquier lado de la parcela.

        Casi cualquiera. Un lado cuyo rumbo **no gira** (sale paralelo a como entró, aunque cambie de largo) es lo que
        voy a llamar dirección propia o **autovector**. Antes de mirar la figura:
        """),
        prediccion,
    ])
    return A_esc, candidatos, n_propias, prediccion, propios_esc


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Dos rumbos: $(1, 1)$ sale como $(3, 3)$, el mismo rumbo estirado $\times 3$, y $(1, -1)$ sale como "
                     r"$(1, -1)$, intacto. Cualquier otro rumbo gira. El lado del fondo de la parcela, de rumbo $(-1, 1)$, sale "
                     r"igual que entró; la sección 3 muestra cómo encontrar esos dos rumbos sin probar."),
        "giro": ("warn",
                 r"**No.** Que ningún rumbo quede es lo que pasa con un **giro**: todo rota el mismo ángulo. Pero $A$ no es un giro: "
                 r"estira $\times 3$ la diagonal $(1, 1)$ ($A(1,1) = (3, 3)$). En la sección 2 el caso *giro de 30°* muestra el tuyo: "
                 r"$\det(R - \lambda I)$ no tiene raíces reales."),
        "corte": ("warn",
                  r"**No.** Una sola dirección es el caso del **corte** $\begin{pmatrix} 1 & 1 \\ 0 & 1 \end{pmatrix}$: el eje $x$ "
                  r"queda y todo lo demás se inclina hacia él ($\lambda = 1$ doble). $A$ tiene dos raíces distintas, $1$ y $3$, "
                  r"y una dirección propia por cada una."),
        "homotecia": ("warn",
                      r"**No.** Que **ningún** rumbo cambie es una homotecia $kI$: todo se estira igual. $A$ no es múltiplo de $I$: "
                      r"manda $(1, 0)$ a $(2, 1)$, que ya giró. Sólo dos rumbos se salvan."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Primero el núcleo.** En una transformación lineal el cero siempre va al cero. El **núcleo** son *todos* los vectores
    que van al cero: si tiene algo más que el $0$, una dirección entera se aplasta a un punto, el plano cae sobre una
    recta y no hay vuelta atrás (no existe $A^{-1}$, como no existe $1/0$). El detector lo anuncia: filas colineales,
    $\det A = 0$. Y la dirección que se aplasta es la que **todas las filas ven como cero**: la perpendicular a una fila.

    **Después, las direcciones que no giran.** $Av = \lambda v$: la recta de $v$ cae sobre sí misma, sólo estirada por
    el **autovalor** $\lambda$ ($1$ queda quieta, $-1$ se invierte, $0$ es el núcleo). El pase de magia del profesor:
    $Av = \lambda v$ es lo mismo que $(A - \lambda I)\,v = 0$: **$v$ está en el núcleo de $A - \lambda I$**, una versión
    modificada de la transformación. Y ya sé cuándo un núcleo no es trivial: cuando el detector da cero,
    $\det(A - \lambda I) = 0$. Esa ecuación en $\lambda$ es el **polinomio característico**; sus raíces reales son los
    autovalores, y para cada una el autovector es la perpendicular a una fila de $A - \lambda I$.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $a x = 0$ sólo con $x = 0$, salvo $a = 0$; $a x = \lambda x$ para **todo** $x$ con $\lambda = a$ | el núcleo es $\{0\}$ o la recta entera; **toda** dirección es propia (hay una sola) |
    | $\mathbb R^2$ | núcleo $\{0\}$, una recta o todo; $\det(A - \lambda I)$ de grado $2$: $0$, $1$ ó $2$ raíces reales | a lo sumo dos direcciones que no giran; un giro no tiene ninguna; una homotecia, todas |
    | $\mathbb R^3$ | grado $3$: **siempre** una raíz real; autovector $=$ cruz de dos filas | siempre hay una recta que cae sobre sí misma: el eje (lección 07c) |

    Esto es una **muestra**; la demostración está en el apunte, sección 11.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- casos precargados: etiqueta → (matriz, qué pasa) ----------
    casos = {
        "A = [[2, 1], [1, 2]]: dos direcciones perpendiculares": (np.array([[2.0, 1.0], [1.0, 2.0]]), r"$\lambda = 3$ en $(1, 1)$ y $\lambda = 1$ en $(1, -1)$: simétrica, direcciones propias a $90°$."),
        "B = [[3, 1], [0, 2]]: dos direcciones, no perpendiculares": (np.array([[3.0, 1.0], [0.0, 2.0]]), r"$\lambda = 3$ en $(1, 0)$ y $\lambda = 2$ en $(1, -1)$: no simétrica, las direcciones no son perpendiculares."),
        "corte [[1, 1], [0, 1]]: una sola dirección": (np.array([[1.0, 1.0], [0.0, 1.0]]), r"$\lambda = 1$ doble pero una sola dirección, el eje $x$; todo lo demás se inclina hacia él."),
        "giro de 30°: ninguna dirección real": (lib.rot2(np.deg2rad(30)), r"$\det(R - \lambda I) = \lambda^2 - 2\cos 30°\,\lambda + 1$ no tiene raíces reales: **todo gira**."),
        "proyección [[1, 2], [2, 4]]: det 0, el núcleo": (np.array([[1.0, 2.0], [2.0, 4.0]]), r"$\lambda = 0$ en $(2, -1)$: el **núcleo**, va al cero; $\lambda = 5$ en $(1, 2)$: la recta sobre la que cae todo."),
        "homotecia 2I: todas las direcciones": (2.0 * np.eye(2), r"$\lambda = 2$ doble y el núcleo de $A - 2I$ es el plano entero: ningún rumbo gira."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="A = [[2, 1], [1, 2]]: dos direcciones perpendiculares", label="caso precargado")
    rango = 6
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # el lado (5, 3) → (3, 5) tiene rumbo (−1, 1)
    mo.vstack([
        mo.md(r"""
        ## 2. Manipulación

        **Gris**: grilla y parcela antes. **Teal**: la grilla deformada, con las columnas como flechas. **Negro a rayas**:
        las direcciones propias, con la flecha $\lambda\,\hat v$ que muestra cuánto se estiran. **Violeta**: la parcela
        con estelas y una **flecha de prueba** $v$ que elegís con el deslizador ($v$ gris, $Av$ violeta): sobre una
        dirección propia no gira ($0°$ ó $180°$); en cualquier otra, sí. **Reproducir** muestra el camino desde la identidad.
        """),
        caso,
    ])
    return caso, casos, parcela, rango


@app.cell
def _(mo):
    phi = mo.ui.slider(0, 180, value=20, step=1, label="rumbo de la flecha de prueba (°)", show_value=True)
    return (phi,)


@app.cell
def _(caso, casos, go, lib, mo, np, parcela, phi, rango):
    A, que_pasa = casos[caso.value]
    v_prueba = 2.0 * np.array([np.cos(np.deg2rad(phi.value)), np.sin(np.deg2rad(phi.value))])
    Av = A @ v_prueba
    camino = [np.eye(2) + s * (A - np.eye(2)) for s in np.linspace(0, 1, 36)]

    def _dinamicas(i):
        f = go.Figure()
        lib.capa_despues(f, camino[i], rango)
        lib.objeto(f, lib.transformar(parcela, camino[i]), lib.VIOLETA_OBJETO, "parcela después",
                   estelas=lib.estelas(parcela[[1, 2, 3]], camino[: i + 1]))
        lib.flecha(f, (0, 0), camino[i] @ v_prueba, lib.VIOLETA_OBJETO, "A v (la flecha de prueba, después)", ancho=5)
        return list(f.data)

    figura = lib.figura_plano(rango + 1, caso.value)
    lib.capa_antes(figura, rango)
    lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    lib.flecha(figura, (0, 0), v_prueba, lib.GRIS_ANTES, "v (la flecha de prueba, antes)", ancho=5)
    propios = lib.direcciones_propias(figura, A, rango)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    giro_v = np.rad2deg(lib.angulo(v_prueba, Av)) if np.linalg.norm(Av) > 1e-12 else float("nan")
    _lams = ", ".join(lib.num_tex(p["lam"], 3) for p in propios) or "ninguno real"
    _panel = mo.vstack([
        mo.md("**Controles**"), phi,
        mo.md(rf"""
        **Números vivos**

        - $\det A = {lib.num_tex(np.linalg.det(A), 3)}$ · autovalores reales: ${_lams}$
        - $v = {lib.vec_tex(v_prueba, 2)}$, $Av = {lib.vec_tex(Av, 2)}$: la flecha giró $\mathbf{{{lib.num_tex(giro_v, 1)}°}}$

        $$A = {lib.matriz_coloreada(A)}$$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.6)
    mo.hstack([_panel, mo.ui.plotly(figura)], widths=[1, 2], align="start")
    return A, Av, giro_v, propios, v_prueba


@app.cell
def _(mo):
    lam = mo.ui.slider(0, 4, value=2.0, step=0.05, label="λ", show_value=True)
    mo.vstack([
        mo.md(r"""
        **El detector sobre $A - \lambda I$.** Con $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, la versión
        modificada $A - \lambda I$ aplicada a la circunferencia unitaria da una elipse (teal). A la derecha, el detector
        $p(\lambda) = \det(A - \lambda I)$. Llevá $\lambda$ a $1$ y a $3$: la elipse **se aplasta a un segmento**
        (apareció un núcleo) justo donde $p(\lambda) = 0$. El segmento queda perpendicular al autovector, que es la
        dirección que fue al cero.
        """),
        lam,
    ])
    return (lam,)


@app.cell
def _(A_esc, go, lam, lib, mo, np):
    B_lam = A_esc - lam.value * np.eye(2)
    _circ = lib.circulo()
    _el = lib.transformar(_circ, B_lam)
    fig_el = lib.figura_plano(3.5, f"(A − λI) · circunferencia, λ = {lam.value:.2f}", ancho=380, alto=380)
    fig_el.add_trace(go.Scatter(x=_circ[:, 0], y=_circ[:, 1], mode="lines", line=dict(color=lib.GRIS_ANTES, width=1.5), name="circunferencia"))
    fig_el.add_trace(go.Scatter(x=_el[:, 0], y=_el[:, 1], mode="lines", line=dict(color=lib.TEAL_DESPUES, width=2.5), name="(A − λI) · circunferencia"))
    lib.direcciones_propias(fig_el, A_esc, 3.5)
    _ls = np.linspace(0, 4, 161)
    _ps = [np.linalg.det(A_esc - l * np.eye(2)) for l in _ls]
    fig_p = go.Figure(layout=go.Layout(width=380, height=380, margin=dict(l=40, r=10, t=56, b=40), plot_bgcolor="white",
                                      title=dict(text="p(λ) = det(A − λI) = λ² − 4λ + 3", font=dict(size=14), x=0.01, xanchor="left"),
                                      xaxis=dict(title="λ", gridcolor="#eceae4"), yaxis=dict(title="p(λ)", gridcolor="#eceae4", zeroline=True, zerolinecolor="#444"),
                                      showlegend=False))
    fig_p.add_trace(go.Scatter(x=_ls, y=_ps, mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=2)))
    fig_p.add_trace(go.Scatter(x=[lam.value], y=[np.linalg.det(B_lam)], mode="markers", marker=dict(size=11, color="#222")))
    mo.vstack([
        mo.hstack([mo.ui.plotly(fig_el), mo.ui.plotly(fig_p)], widths="equal"),
        mo.md(rf"$A - \lambda I = {lib.matriz_coloreada(B_lam, 2)}$, $\det(A - \lambda I) = \mathbf{{{lib.num_tex(np.linalg.det(B_lam), 3)}}}$"),
    ])
    return (B_lam,)


@app.cell
def _(A_esc, lib, mo, np):
    _N = np.array([[1.0, 2.0], [2.0, 4.0]])
    _k = lib.nucleo2(_N)
    _raices = np.sort(np.roots(np.poly(A_esc)))
    _av = lib.autovectores_cuna(A_esc)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy con el código a la vista.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 El núcleo.** $N = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$: $\det N = 4 - 4 = 0$, la segunda fila
            es el doble de la primera. $Nv = 0$ pide que **cada fila por $v$** dé cero: $v_1 + 2 v_2 = 0$. La perpendicular
            a la fila $(1, 2)$ es $(2, -1)$ (la perpendicular a $(a, b)$ es $(b, -a)$: la cruz de $(a, b, 0)$ con $e_3$).
            $$N\begin{pmatrix} 2 \\ -1 \end{pmatrix} = \begin{pmatrix} 2 - 2 \\ 4 - 4 \end{pmatrix} = \begin{pmatrix} 0 \\ 0 \end{pmatrix}.$$
            Todo el plano cae sobre la recta de la columna $(1, 2)$: $N(x, y) = (x + 2y)\,(1, 2)$.
            """),
            mo.vstack([
                mo.md("```python\nN = np.array([[1., 2.], [2., 4.]])\nnp.linalg.det(N)\nk = lib.perp2(N[0])        # (b, −a) de la fila (a, b)\nN @ k\nlib.nucleo2(N)             # lo mismo, eligiendo la fila no nula\n```"),
                mo.md(f"`{np.linalg.det(_N):.1f}` · `k` = `{lib.perp2(_N[0]).tolist()}` · `N @ k` = `{(_N @ _k).tolist()}` · `{_k.tolist()}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 Los autovalores, con el detector.** $A - \lambda I = \begin{pmatrix} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{pmatrix}$ y
            $$\det(A - \lambda I) = (2 - \lambda)^2 - 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 1)(\lambda - 3).$$
            Sólo para $\lambda = 1$ y $\lambda = 3$ las filas son colineales y hay algo en el núcleo.

            **3.3 Los autovectores, por la fila.** $\lambda = 3$: $A - 3I = \begin{pmatrix} -1 & 1 \\ 1 & -1 \end{pmatrix}$, perpendicular
            a la fila $(-1, 1)$: $v = (1, 1)$; control $A(1, 1) = (3, 3) = 3\,(1, 1)$ ✓. $\lambda = 1$: $A - I = \begin{pmatrix} 1 & 1 \\ 1 & 1 \end{pmatrix}$,
            perpendicular a $(1, 1)$: $v = (1, -1)$; control $A(1, -1) = (1, -1)$ ✓. En $\mathbb R^2$ "la cruz de dos filas"
            se reduce a "la perpendicular a una fila".
            """),
            mo.vstack([
                mo.md("```python\nA = np.array([[2., 1.], [1., 2.]])\nnp.poly(A)                        # [1, −4, 3]: λ² − 4λ + 3\nnp.roots(np.poly(A))\nv3 = lib.perp2((A - 3 * np.eye(2))[0])\nnp.allclose(A @ v3, 3 * v3)\nlib.autovectores_cuna(A)          # el método entero\n```"),
                mo.md(f"`{np.round(np.poly(A_esc), 6).tolist()}` · raíces `{np.round(_raices, 6).tolist()}` · `v3` = `{lib.perp2((A_esc - 3 * np.eye(2))[0]).tolist()}` · `{bool(np.allclose(A_esc @ [1, 1], [3, 3]))}`  \n"
                      + "  \n".join(f"λ = {p['lam']:.0f}: v = `{p['v'].tolist()}`, fila usada {p['filas'][0] + 1}" for p in _av)),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(A_esc, lib, mo, np):
    _w, _V = np.linalg.eig(A_esc)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **`np.linalg.eig(A)` devuelve dos cosas**, el array de autovalores `w` y una matriz `V` cuyas
        **columnas** son los autovectores (unitarios), en el mismo orden: `A @ V[:, k]` es `w[k] * V[:, k]`. Los
        autovalores salen complejos si hay giro, y `eig` no los ordena. `lib.autovectores_cuna(A)` hace la cuenta del
        profesor y devuelve, además, qué fila usó y si el núcleo era un plano entero.
        """),
        mo.md("```python\nw, V = np.linalg.eig(A)       # w: autovalores; V: autovectores por columnas\nnp.allclose(A @ V[:, 0], w[0] * V[:, 0])\nnp.linalg.eigvals(lib.rot2(0.5))   # un giro: complejos\n```"),
        mo.md(f"`w` = `{np.round(_w, 6).tolist()}` · `V` =\n```\n{np.round(_V, 4)}\n```\n`A @ V[:, 0] == w[0] V[:, 0]`: `{bool(np.allclose(A_esc @ _V[:, 0], _w[0] * _V[:, 0]))}` · "
              f"`eigvals(rot2(0.5))` = `{np.round(np.linalg.eigvals(lib.rot2(0.5)), 4).tolist()}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("hay vectores de entrada que van al cero").* $B = \begin{pmatrix} 2 & 3 \\ 4 & 6 \end{pmatrix}$.
        ¿Tiene núcleo no trivial? Encontrá un vector del núcleo y decí sobre qué recta cae el plano entero.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $\det B = 12 - 12 = 0$ (fila 2 $= 2\times$ fila 1): sí. Perpendicular a la fila $(2, 3)$: $v = (3, -2)$, y
        $B(3, -2) = (6 - 6, 12 - 12) = (0, 0)$ ✓. Todo cae sobre la recta de la columna $(2, 4)$, o sea la de $(1, 2)$:
        $B(x, y) = (2x + 3y)(1, 2)$.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("buscamos los valores de $\lambda$ que hagan que el núcleo no esté vacío").*
        $B = \begin{pmatrix} 3 & 1 \\ 0 & 2 \end{pmatrix}$. Hallá los autovalores con el detector y un autovector por cada
        uno con la perpendicular a una fila. ¿Son perpendiculares entre sí? ¿Por qué un giro $R(\theta)$ con
        $0 < \theta < 180°$ no tiene ninguno?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $\det(B - \lambda I) = (3 - \lambda)(2 - \lambda)$: $\lambda = 3, 2$. $\lambda = 3$: $B - 3I = \begin{pmatrix} 0 & 1 \\ 0 & -1 \end{pmatrix}$,
        perpendicular a $(0, 1)$: $(1, 0)$; $B(1, 0) = (3, 0)$ ✓. $\lambda = 2$: $B - 2I = \begin{pmatrix} 1 & 1 \\ 0 & 0 \end{pmatrix}$,
        perpendicular a $(1, 1)$: $(1, -1)$; $B(1, -1) = (2, -2)$ ✓. No son perpendiculares: $(1, 0) \cdot (1, -1) = 1$
        ($B$ no es simétrica). Un giro: $\det(R - \lambda I) = \lambda^2 - 2\cos\theta\,\lambda + 1$, discriminante
        $4\cos^2\theta - 4 < 0$: raíces complejas, ninguna dirección real queda quieta.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def nucleo(A):\n    fila = ...      # una fila NO nula de A (ojo: la primera puede ser (0, 0))\n    return ...      # la perpendicular (b, −a) a esa fila\n",
        language="python", min_height=120, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("un vector ortogonal a todas sus filas").* Completá `nucleo(A)`: recibe una
        $2\times2$ con $\det A = 0$ y devuelve un vector **no nulo** de su núcleo. Tenés `np` y `perp2`. Se verifica con
        `np.allclose(A @ v, 0)` en cinco matrices singulares, una de ellas con la primera fila nula.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _casos = [np.array([[1.0, 2.0], [2.0, 4.0]]), np.array([[2.0, 3.0], [4.0, 6.0]]), np.array([[0.0, 0.0], [1.0, -3.0]]),
              np.array([[1.5, -0.5], [-3.0, 1.0]]), np.array([[0.0, 2.0], [0.0, 7.0]])]
    _ns = {"np": np, "perp2": lib.perp2}
    try:
        exec(editor_c.value, _ns)
        _vs = [np.asarray(_ns["nucleo"](A), dtype=float).reshape(-1) for A in _casos]
        _nulos = [bool(np.linalg.norm(v) < 1e-9) for v in _vs]
        _ok = [bool(v.shape == (2,) and np.linalg.norm(v) > 1e-9 and np.allclose(A @ v, 0)) for A, v in zip(_casos, _vs)]
        if all(_ok):
            _res = mo.callout(mo.md("✅ en las cinco matrices `A @ v` es cero y `v` no es el vector nulo."), kind="success")
        elif _nulos[2] and all(_ok[:2]):
            _res = mo.callout(mo.md("❌ en la tercera matriz devolviste `(0, 0)`: su primera fila es nula y la perpendicular a `(0, 0)` es `(0, 0)`. Elegí la fila que no es nula."), kind="warn")
        elif any(_nulos):
            _res = mo.callout(mo.md("❌ devolviste el vector nulo: el núcleo siempre lo tiene; buscamos el **otro**, el que no es trivial."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ falla en las matrices `{[i + 1 for i, o in enumerate(_ok) if not o]}`. ¿Usaste `(b, −a)` y no `(a, b)` ni `(−b, a)` con otra fila?"), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def autovectores(A):\n    traza, det = ..., ...\n    lams = np.roots([1, -traza, det])      # raíces de λ² − (tr A) λ + det A\n    salida = []\n    for lam in lams:\n        B = ...                              # la versión modificada A − λI\n        v = ...                              # perpendicular a una fila no nula de B\n        salida.append((lam, v))\n    return salida\n",
        language="python", min_height=200, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado: la máquina del profesor** *("construir una versión modificada de la
        transformación que tenga al autovector en el núcleo").* Completá `autovectores(A)`: para una $2\times2$ con
        autovalores reales distintos devuelve una lista de pares `(λ, v)`. Tenés `np` y `perp2`. Se verifica que cada
        par cumpla `np.allclose(A @ v, λ v)` en tres matrices, y que los $\lambda$ coincidan con `np.linalg.eigvals`.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _casos = [np.array([[2.0, 1.0], [1.0, 2.0]]), np.array([[3.0, 1.0], [0.0, 2.0]]), np.array([[1.0, 2.0], [2.0, 4.0]])]
    _ns = {"np": np, "perp2": lib.perp2}
    try:
        exec(editor_d.value, _ns)
        _fallas = []
        for _i, _A in enumerate(_casos, 1):
            _pares = [(float(np.real(l)), np.asarray(v, dtype=float).reshape(-1)) for l, v in _ns["autovectores"](_A)]
            _lams_ok = np.allclose(np.sort([l for l, _ in _pares]), np.sort(np.real(np.linalg.eigvals(_A))))
            _vs_ok = all(np.linalg.norm(v) > 1e-9 and np.allclose(_A @ v, l * v) for l, v in _pares)
            if not _lams_ok:
                _fallas.append(f"matriz {_i}: los λ no coinciden con `eigvals`")
            elif not _vs_ok:
                _fallas.append(f"matriz {_i}: los λ están bien, pero algún v no cumple A v = λ v (¿la fila es de A − λI, no de A?)")
        _res = (mo.callout(mo.md("✅ las tres matrices: cada `(λ, v)` cumple `A @ v == λ v` y los λ coinciden con `eigvals`."), kind="success")
                if not _fallas else mo.callout(mo.md("❌ " + "; ".join(_fallas) + "."), kind="warn"))
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré; las demostraciones (núcleo no trivial $\Leftrightarrow$ $\det = 0$, el pase de magia $(A - \lambda I)v = 0$,
    cuántas raíces reales, el método de la cruz de filas):

    - [apunte, sección 11: productos, determinante y autovectores](../../apunte.pdf#nameddest=cap:11) · [sección 5: la misma idea en cada dimensión](../../apunte.pdf#nameddest=cap:05)
    - [ficha de la clase 5](../../clases/05.html) · [ficha de la clase 6](../../clases/06.html) · [lección anterior: cuña y determinante](../07a_cuna_determinante/index.html) · [el camino](../../index.html)

    **Lo que viene:** [Autovalores en 3D y puntos fijos proyectivos](../07c_autovalores_3d_puntos_fijos/index.html):
    en 3D el autovector es la cruz de dos filas, el eje de una rotación es su autovector de autovalor $1$, y un
    autovector de la $3\times3$ homogénea es un punto fijo del plano. Después, en
    [cambio de base](../08_cambio_de_base/index.html), la grilla de autovectores es la grilla donde $A$ es sólo estirar.
    """)
    return


@app.cell
def _(A, A_esc, Av, B_lam, candidatos, casos, giro_v, lam, lib, mo, n_propias, np, propios, propios_esc, v_prueba):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _B = np.array([[3.0, 1.0], [0.0, 2.0]])
    _checks = [
        ("sección 0: candidatos distintos; A tiene dos direcciones propias, (1, 1) con λ = 3 y (1, −1) con λ = 1",
         len(set(candidatos.values())) == 4 and n_propias == 2 and lib.exacto([p["lam"] for p in propios_esc], [3, 1])
         and lib.exacto(propios_esc[0]["v"], [1, 1]) and lib.exacto(propios_esc[1]["v"], [1, -1])),
        ("sección 2: cada dirección propia dibujada cumple A v = λ v; el giro no tiene reales, la homotecia es el plano entero, la proyección tiene λ = 0",
         all(lib.exacto(A @ p["v"], p["lam"] * p["v"]) for p in propios if not p["plano"]) and lib.exacto(Av, A @ v_prueba) and (np.isnan(giro_v) or 0 <= giro_v <= 180)
         and lib.autovalores_reales(casos["giro de 30°: ninguna dirección real"][0]) == [] and lib.autovectores_cuna(2 * np.eye(2))[0]["plano"]
         and 0.0 in lib.autovalores_reales(np.array([[1.0, 2.0], [2.0, 4.0]]))),
        ("detector: det(A − λI) = λ² − 4λ + 3 en el λ del deslizador; cero en 1 y 3",
         lib.exacto(np.linalg.det(B_lam), lam.value ** 2 - 4 * lam.value + 3, tol=1e-9) and lib.exacto(np.roots(np.poly(A_esc)), [3, 1])),
        ("3.1: (2, −1) está en el núcleo de [[1, 2], [2, 4]]; 3.3: A(1, 1) = 3(1, 1), A(1, −1) = (1, −1)",
         lib.exacto(np.array([[1, 2], [2, 4]]) @ lib.nucleo2([[1, 2], [2, 4]]), [0, 0]) and lib.exacto(A_esc @ [1, 1], [3, 3]) and lib.exacto(A_esc @ [1, -1], [1, -1])),
        ("ejercicios (a) y (b): B(3, −2) = 0; [[3, 1], [0, 2]] tiene λ = 3, 2 con (1, 0) y (1, −1), no perpendiculares",
         lib.exacto(np.array([[2, 3], [4, 6]]) @ [3, -2], [0, 0]) and lib.exacto(_B @ [1, 0], [3, 0]) and lib.exacto(_B @ [1, -1], [2, -2])
         and not lib.exacto(np.array([1, 0]) @ [1, -1], 0.0)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
