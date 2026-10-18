# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Cuña y determinante: el detector de colinealidad (unidad 07a, molde v2 sobre cb104). Clase 5.

Una sola idea: el área orientada de dos vectores (producto cuña) es una cuenta con coordenadas; vale cero si están
alineados; el determinante de una matriz es cuánto agranda el área (en 3D el volumen) y su signo dice si da vuelta
la orientación. Escalera R (|a|, factor de longitud) → R² (área) → R³ (volumen, producto vectorial como cuña).

Chequear:  uv run marimo check --select MW unidades/07a_cuna_determinante.py
Exportar:  uv run python tools/build.py --only 07a_cuna_determinante
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
    # Cuña y determinante: el detector de colinealidad

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Seguimos la clase 5. La pregunta: **¿cómo detectamos con una cuenta, sin medir ningún ángulo, que unos vectores (o unos
    mojones) se aplastaron a algo de menor dimensión?** El gancho: *tres mojones que deberían estar alineados: el
    determinante de sus coordenadas homogéneas los delata.*

    Colores, iguales en la figura y en el álgebra: **primera columna** <span style="color:#1b6f6a">**teal**</span>,
    **segunda** <span style="color:#b5451b">**rust**</span>, **tercera** <span style="color:#c9a227">**gold**</span>;
    acá las columnas son los lados del paralelogramo (en 3D, de la caja). La parcela va en
    <span style="color:#7a4e9e">**violeta**</span>, lo de antes en gris, lo de después en teal.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("07a_cuna_determinante"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    mojones = np.array([[1.0, 1.0], [4.0, 3.0], [7.0, 6.0]])  # A, B, C: el alambrado debería ser recto
    AB, AC = mojones[1] - mojones[0], mojones[2] - mojones[0]
    candidatos = {
        "correcta": lib.cuna2(AB, AC),
        "cero": 0.0,
        "signo": lib.cuna2(AC, AB),
        "mitad": 0.5 * lib.cuna2(AB, AC),
    }
    distancia_C = abs(candidatos["correcta"]) / float(np.linalg.norm(AB))  # cuánto se salió C de la recta AB
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            f"{lib.num_tex(candidatos['cero'])}: están alineados": "cero",
            lib.num_tex(candidatos["correcta"]): "correcta",
            lib.num_tex(candidatos["signo"]): "signo",
            lib.num_tex(candidatos["mitad"], 1): "mitad",
        }),
        value=None,
        label=r"**Predicción.** El detector sobre $A = (1, 1)$, $B = (4, 3)$, $C = (7, 6)$, o sea $(B - A) \wedge (C - A)$, da…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Relevamos tres mojones de un alambrado que, según el título, es **recto**: $A = (1, 1)$, $B = (4, 3)$ y
        $C = (7, 6)$ (metros). Si los tres están alineados, el vector $B - A = (3, 2)$ y el vector $C - A = (6, 5)$
        tienen que ser **paralelos**: uno es un múltiplo del otro, y entre los dos no arman ningún área.

        El detector de colinealidad del profesor es justamente esa área, calculada con coordenadas:
        $u \wedge v = u_1 v_2 - u_2 v_1$. Antes de mirar la figura: ¿qué número da con estos tres mojones?
        """),
        prediccion,
    ])
    return AB, AC, candidatos, distancia_C, mojones, prediccion


@app.cell
def _(distancia_C, lib, mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** $(3, 2) \wedge (6, 5) = 3 \cdot 5 - 2 \cdot 6 = 3$. No es cero: $C$ **no** está sobre la recta $AB$. El $3$ es "
                     rf"el área del paralelogramo de lados $AB$ y $AC$, con signo $+$ porque de $AB$ a $AC$ se gira antihorario. "
                     rf"Dividido por el largo de $AB$ da cuánto se salió $C$: ${lib.num_tex(distancia_C, 2)}$ m."),
        "cero": ("warn",
                 rf"**No.** Cero sería con $C = (7, 5)$: $(3, 2) \wedge (6, 4) = 12 - 12 = 0$, un múltiplo exacto. Con $C = (7, 6)$ da "
                 rf"$15 - 12 = 3$: el mojón está ${lib.num_tex(distancia_C, 2)}$ m fuera del alambrado. El detector no perdona un metro."),
        "signo": ("warn",
                  r"**No.** $-3$ es la cuenta en el **otro orden**, $(C - A) \wedge (B - A)$: la misma área, orientación opuesta. "
                  r"Recorrer $A \to B \to C$ gira antihorario, y eso es signo $+$. El signo es lo que distingue un giro de un espejo (sección 2)."),
        "mitad": ("warn",
                  r"**No.** $1.5$ es el área del **triángulo** $ABC$; el detector mide el **paralelogramo** de lados $AB$ y $AC$, el doble. "
                  r"Los dos detectan lo mismo, pero el número de la cuenta $u_1 v_2 - u_2 v_1$, y del determinante, es el del paralelogramo."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué mide?** Dos vectores del plano arman un paralelogramo; el producto cuña $u \wedge v$ es su **área con
    signo**: positiva si de $u$ a $v$ se gira antihorario, negativa si horario, y **cero exactamente cuando $u$ y $v$
    son colineales**, porque el paralelogramo se aplastó a un segmento. Por eso el profesor lo llama *detector de
    colinealidad*. Dos reglas lo calculan con coordenadas: es lineal en cada vector, y $v \wedge v = 0$ (de donde
    $v \wedge u = -\,u \wedge v$: "el único elemento igual a su opuesto es el cero").

    **El determinante de una matriz es lo mismo** sobre sus columnas: $\det M = Me_1 \wedge Me_2$, el área del
    cuadrado unitario después de transformar. Es **cuánto agranda el área** $M$ (de cualquier figura) y, por el
    signo, **si da vuelta la orientación**.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | un vector es un número $a$; $\det[a] = a$ | $\lvert a \rvert$ es el **factor de longitud**, el signo dice si da vuelta la recta; cero: la recta se aplasta a un punto |
    | $\mathbb R^2$ | $u \wedge v = u_1 v_2 - u_2 v_1 = \det\begin{pmatrix} u_1 & v_1 \\ u_2 & v_2 \end{pmatrix}$ | **área orientada** del paralelogramo; cero: $u$ y $v$ colineales |
    | $\mathbb R^3$ | $(u \wedge v) \wedge w = (u \times v) \cdot w = \det[u\ v\ w]$ | **volumen orientado** de la caja; cero: los tres en un plano |

    En $\mathbb R^3$, $u \wedge v$ tiene tres componentes, una por plano coordenado: son los números del **producto
    vectorial** $u \times v$ (el del medio con el signo cambiado); pegarle $w$ deja un solo número, el volumen. Esto es
    una **muestra**; la demostración de que el determinante es la única operación con esas dos reglas está en el apunte,
    sección 11.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- casos precargados: etiqueta → (tipo, dato, qué pasa) ----------
    u0, v0 = np.array([3.0, 1.0]), np.array([1.0, 2.0])
    casos = {
        "u = (3, 1), v = (1, 2): área 5": ("fijo", np.column_stack([u0, v0]), r"$u \wedge v = 3 \cdot 2 - 1 \cdot 1 = 5$: el cuadrado unitario pasa a un paralelogramo de área $5$, sin darse vuelta."),
        "v gira alrededor de u = (3, 1)": ("gira", 63, r"el área sube y baja con el ángulo; vale $0$ cuando $v$ apunta como $u$ o como $-u$, y cambia de signo al cruzar esa recta."),
        "v = 2u: colineales, área 0": ("fijo", np.column_stack([u0, 2 * u0]), r"$u \wedge 2u = 3 \cdot 2 - 1 \cdot 6 = 0$: **el detector se dispara**, el plano entero se aplasta sobre la recta de $u$."),
        "orden invertido: columnas v, u: área −5": ("fijo", np.column_stack([v0, u0]), r"$v \wedge u = -5$: la misma área, pero de la columna 1 a la 2 se gira horario; la parcela sale dada vuelta."),
        "espejo diag(1, −1): det −1": ("fijo", np.diag([1.0, -1.0]), r"$\det = -1$: no agranda nada, pero **da vuelta la orientación**; la parcela sale como un guante al revés."),
        "giro de 40°: det 1": ("fijo", lib.rot2(np.deg2rad(40)), r"$\det = \cos^2 + \sin^2 = 1$: un giro no agranda ni da vuelta nada."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="v gira alrededor de u = (3, 1)", label="caso precargado")
    rango = 6
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # la misma de Rotaciones II
    mo.md(r"""
    ## 2. Manipulación

    $M = [\,u \mid v\,]$ tiene a $u$ y $v$ como columnas. **Gris**: grilla y cuadrado unitario antes. **Teal**: los
    mismos después; el cuadrado unitario es ahora **el paralelogramo de $u$ y $v$** (flechas teal y rust).
    **Violeta**: la parcela con estelas; su área se multiplica por $\det M$, sea cual sea su forma. **Reproducir**
    muestra el camino desde la identidad. A la derecha de la figura, el panel con el caso, el deslizador y los
    números vivos.
    """)
    return caso, casos, parcela, rango, u0, v0


@app.cell
def _(caso, casos, mo):
    _tipo, _dato, _ = casos[caso.value]
    gira = _tipo == "gira"
    angulo_v = mo.ui.slider(0, 360, value=_dato if gira else 0, step=1, label="ángulo de v (°)", show_value=True, disabled=not gira)
    return angulo_v, gira


@app.cell
def _(angulo_v, caso, casos, gira, go, lib, mo, np, parcela, rango, u0):
    _tipo, _dato, que_pasa = casos[caso.value]
    if gira:
        _r = np.sqrt(5.0)  # |v| = |(1, 2)|

        def _M_de(t):
            return np.column_stack([u0, _r * np.array([np.cos(t), np.sin(t)])])

        theta_v = np.deg2rad(angulo_v.value)
        M = _M_de(theta_v)
        camino = [_M_de(t) for t in np.linspace(0, theta_v, 36)]
    else:
        M = np.asarray(_dato, dtype=float)
        camino = [np.eye(2) + s * (M - np.eye(2)) for s in np.linspace(0, 1, 36)]

    def _dinamicas(i):
        f = go.Figure()
        lib.capa_despues(f, camino[i], rango)
        lib.objeto(f, lib.transformar(parcela, camino[i]), lib.VIOLETA_OBJETO, "parcela después",
                   estelas=lib.estelas(parcela[[1, 2, 3]], camino[: i + 1]))
        return list(f.data)

    figura = lib.figura_plano(rango + 1, caso.value)
    lib.capa_antes(figura, rango)
    lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    cuna_uv = lib.cuna2(M[:, 0], M[:, 1])
    area_antes = lib.area_poligono(parcela)
    area_despues = lib.area_poligono(lib.transformar(parcela, M))
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, angulo_v,
        mo.md(rf"""
        **Números vivos**

        - $u \wedge v = u_1 v_2 - u_2 v_1 = \mathbf{{{lib.num_tex(cuna_uv, 3)}}}$ · `np.linalg.det(M)` $= {lib.num_tex(np.linalg.det(M), 3)}$
        - área con signo de la parcela: antes ${lib.num_tex(area_antes)}$, después $\mathbf{{{lib.num_tex(area_despues, 3)}}}$
          (cociente ${lib.num_tex(area_despues / area_antes, 3)}$)

        $$M = [\,\textcolor{{#1b6f6a}}{{u}} \mid \textcolor{{#b5451b}}{{v}}\,] = {lib.matriz_coloreada(M)}$$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, area_antes, area_despues, cuna_uv


@app.cell
def _(mo):
    s_w = mo.ui.slider(0, 1.5, value=1.0, step=0.05, label="s (posición de w)", show_value=True)
    mo.md(r"""
    **Un piso más arriba: la caja.** $u = (1, 2, 0)$ y $v = (0, 1, 1)$ quedan fijos y arman el plano gris. El tercer
    lado $w$ viaja en línea recta desde $w_0 = (1, 0, 2)$ hasta $u + v = (1, 3, 1)$, que **está en ese plano**:
    $w(s) = (1 - s)\,w_0 + s\,(u + v)$. El volumen orientado $\det[u\ v\ w]$ baja hasta cero cuando la caja se
    vuelve una lámina, y pasado $s = 1$ cambia de signo: $w$ cruzó al otro lado del plano. El deslizador $s$ va en el
    panel de la derecha.
    """)
    return (s_w,)


@app.cell
def _(lib, mo, np, s_w):
    u3, v3, w0 = np.array([1.0, 2.0, 0.0]), np.array([0.0, 1.0, 1.0]), np.array([1.0, 0.0, 2.0])
    w3 = (1 - s_w.value) * w0 + s_w.value * (u3 + v3)
    vol = lib.cuna3(u3, v3, w3)
    _vert, _aristas = lib.paralelepipedo(u3, v3, w3)
    fig3 = lib.figura_espacio((-0.6, 3.4), f"s = {s_w.value:.2f}: det[u v w] = {vol:+.2f}")
    lib.plano_3d(fig3, u3, v3, k=1.2, origen=0.5 * (u3 + v3), nombre="plano de u y v")
    _x, _y, _z = lib.segmentos_3d(_vert, _aristas)
    fig3.add_trace(dict(type="scatter3d", x=_x, y=_y, z=_z, mode="lines", line=dict(color=lib.TEAL_DESPUES, width=4), name="caja de u, v, w"))
    lib.flechas_columnas_3d(fig3, np.column_stack([u3, v3, w3]), "M")
    _cruz = np.cross(u3, v3)
    _panel = mo.vstack([
        mo.md("**Controles**"), s_w,
        mo.md(rf"""
        **Números vivos**

        - $w(s) = {lib.vec_tex(w3, 2)}$
        - $u \times v = {lib.vec_tex(_cruz)}$: perpendicular al plano gris, de largo el área del paralelogramo de $u$ y $v$
        - $(u \times v) \cdot w = \mathbf{{{lib.num_tex(vol, 3)}}}$ · `np.linalg.det` $= {lib.num_tex(np.linalg.det(np.column_stack([u3, v3, w3])), 3)}$

        Columnas: $u$ <span style="color:{lib.COLORES[0]}">teal</span>, $v$ <span style="color:{lib.COLORES[1]}">rust</span>,
        $w$ <span style="color:{lib.COLORES[2]}">gold</span>. La caja es el cubo unitario transformado por $[u\ v\ w]$.
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(fig3), _panel)
    return u3, v3, vol, w0, w3


@app.cell
def _(AB, AC, lib, mo, mojones, np, u3, v3, w0):
    _u, _v = np.array([3.0, 1.0]), np.array([1.0, 2.0])
    _H = lib.hom(mojones)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy con el código a la vista.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 El área con las dos reglas.** $u = (3, 1)$, $v = (1, 2)$. Escribimos cada uno en la base y distribuimos, con
            $e_1 \wedge e_1 = e_2 \wedge e_2 = 0$ y $e_2 \wedge e_1 = -\,e_1 \wedge e_2$:

            $$u \wedge v = (3e_1 + e_2) \wedge (e_1 + 2e_2) = 3 \cdot 2\; e_1 \wedge e_2 + 1 \cdot 1\; e_2 \wedge e_1 = (6 - 1)\; e_1 \wedge e_2 .$$

            Área $5$, signo $+$. Al revés, $v \wedge u = 1 \cdot 1 - 2 \cdot 3 = -5$. Colineales: $u \wedge 2u = 3 \cdot 2 - 1 \cdot 6 = 0$.
            """),
            mo.vstack([
                mo.md("```python\nu = np.array([3., 1.])\nv = np.array([1., 2.])\nlib.cuna2(u, v)            # u1 v2 − u2 v1\n# columnas u, v\nnp.linalg.det(np.column_stack([u, v]))\nlib.cuna2(v, u), lib.cuna2(u, 2 * u)\n```"),
                mo.md(f"`{lib.cuna2(_u, _v):.0f}` · `{np.linalg.det(np.column_stack([_u, _v])):.1f}` · `{lib.cuna2(_v, _u):.0f}`, `{lib.cuna2(_u, 2 * _u):.0f}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 El volumen, un piso más arriba.** Con $u = (1, 2, 0)$, $v = (0, 1, 1)$ las mismas reglas dejan tres áreas:
            $u \wedge v = 1\, e_1 \wedge e_2 + 1\, e_1 \wedge e_3 + 2\, e_2 \wedge e_3$, los números de $u \times v = (2, -1, 1)$.
            Pegarle $w = (1, 0, 2)$ sólo deja vivo, en cada término, el versor que falta:
            $(u \wedge v) \wedge w = (2 \cdot 1 - 1 \cdot 0 + 1 \cdot 2)\; e_1 \wedge e_2 \wedge e_3$: es $(u \times v) \cdot w = \det[u\ v\ w] = 4$.
            Con $w = u + v$ da $2 - 3 + 1 = 0$: en el plano.
            """),
            mo.vstack([
                mo.md("```python\nu = np.array([1., 2., 0.])\nv = np.array([0., 1., 1.])\nw = np.array([1., 0., 2.])\nnp.cross(u, v)\nnp.cross(u, v) @ w         # (u × v) · w\nnp.linalg.det(np.column_stack([u, v, w]))\nlib.cuna3(u, v, u + v)\n```"),
                mo.md(f"`{np.cross(u3, v3).tolist()}` · `{np.cross(u3, v3) @ w0:.0f}`  \n"
                      f"`{np.linalg.det(np.column_stack([u3, v3, w0])):.1f}` · `{lib.cuna3(u3, v3, u3 + v3):.0f}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 Los tres mojones, en homogéneas.** Cada mojón como terna $(x, y, 1)$, las tres como filas; desarrollamos
            por la columna de unos:

            $$\det\begin{pmatrix} 1 & 1 & 1 \\ 4 & 3 & 1 \\ 7 & 6 & 1 \end{pmatrix} = (24 - 21) - (6 - 7) + (3 - 4) = 3 .$$

            El mismo $3$ que $(B - A) \wedge (C - A)$: "tres puntos alineados" es "tres vectores en un plano por el origen",
            y el volumen cero lo detecta. Es la condición "sin tres alineados" de la unidad 05.
            """),
            mo.vstack([
                mo.md("```python\n# A, B, C, una fila por mojón\nP = np.array([[1., 1.], [4., 3.], [7., 6.]])\nnp.linalg.det(lib.hom(P))   # filas (x, y, 1)\nlib.cuna2(P[1] - P[0], P[2] - P[0])\nlib.alineados(P[0], P[1], P[2])\n```"),
                mo.md(f"`{np.linalg.det(_H):.1f}` · `{lib.cuna2(AB, AC):.0f}` · `{lib.alineados(*mojones)}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(lib, mo, np):
    _p, _q, _r = np.array([1.0, 2.0, 3.0]), np.array([4.0, 5.0, -1.0]), np.array([0.0, 0.0, 1.0])
    _M = np.column_stack([_p, _q, _r])
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **`np.column_stack([u, v, w])` arma la matriz con esos vectores como columnas**, y
        `np.linalg.det` es el detector en cualquier dimensión; en 3D `np.cross(u, v) @ w` es el mismo número. Dan
        `float`: "¿es cero?" con decimales se pregunta con `np.isclose(det, 0)`, nunca con `det == 0`.
        """),
        mo.md("```python\np, q, r = np.array([1., 2., 3.]), np.array([4., 5., -1.]), np.array([0., 0., 1.])\nM = np.column_stack([p, q, r])      # shape (3, 3): columnas p, q, r\nnp.linalg.det(M)\nnp.cross(p, q) @ r                  # la apuesta del 16/9\nnp.isclose(np.linalg.det(M), 0)\n```"),
        mo.md(f"`M.shape` = `{_M.shape}` → `np.linalg.det(M)` = `{np.linalg.det(_M):.1f}` · `np.cross(p, q)` = `{np.cross(_p, _q).tolist()}` · "
              f"`np.cross(p, q) @ r` = `{np.cross(_p, _q) @ _r:.0f}` · alineados: `{bool(np.isclose(np.linalg.det(_M), 0))}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("hagan el producto cruz y después el producto interno: eso es el determinante").*
        La apuesta de clase del 16/9: $p = (1, 2, 3)$, $q = (4, 5, -1)$, $r = (0, 0, 1)$. Calculá $p \times q$, después
        $(p \times q) \cdot r$, y controlá con el determinante desarrollado por la fila de $r$ (la que tiene ceros).
        ¿Están alineados, como puntos homogéneos del plano?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $p \times q = (2 \cdot (-1) - 3 \cdot 5,\ 3 \cdot 4 - 1 \cdot (-1),\ 1 \cdot 5 - 2 \cdot 4) = (-17, 13, -3)$, y
        $(p \times q) \cdot r = -3$. Por la tercera fila: $0 - 0 + 1 \cdot (1 \cdot 5 - 2 \cdot 4) = -3$. ✓ No es cero:
        $p = (1/3, 2/3)$, $q = (-4, -5)$ y $r$ (el origen) **no** están alineados; el volumen de la caja es $3$.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("cuánto agranda un cubo unidad y si invierte la orientación").* La parcela de la
        sección 2 tiene área $12$. ¿Qué área tiene después de $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$? ¿Y qué
        área **con signo** después del espejo $\mathrm{diag}(1, -1)$? ¿Puede una matriz con $\det = 0$ dejarle algo de área?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $\det A = 4 - 1 = 3$: área $36$, sin importar la forma (la grilla entera se agranda $3$ veces). Con el espejo,
        $\det = -1$: área $-12$, el mismo tamaño recorrido al revés. Con $\det = 0$ la parcela cae entera sobre una recta:
        área $0$, y no hay forma de deshacerlo (no existe $A^{-1}$, como no existe $1/0$).
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def alineados(p, q, r):\n    M = ...        # 3×3: las ternas (x, y, 1) de los tres puntos\n    return ...     # True si el detector da (casi) cero\n",
        language="python", min_height=120, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("si da cero, $R$ está en la recta de $P$ y $Q$").* Completá `alineados(p, q, r)`:
        recibe tres puntos del plano como arrays de dos coordenadas y devuelve `True` si están alineados. Tenés `np` y
        `hom`. Se verifica con `np.allclose` sobre seis ternas, tres alineadas (algunas con decimales) y tres no.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _ternas = []
    for _k in range(3):  # alineadas: r = p + t (q − p)
        _p, _q = _rng.uniform(-5, 5, size=2), _rng.uniform(-5, 5, size=2)
        _ternas.append((_p, _q, _p + _rng.uniform(-2, 3) * (_q - _p), True))
    for _k in range(3):
        _p, _q, _r = (_rng.uniform(-5, 5, size=2) for _ in range(3))
        _ternas.append((_p, _q, _r, lib.alineados(_p, _q, _r)))
    _ns = {"np": np, "hom": lib.hom}
    try:
        exec(editor_c.value, _ns)
        _obt = [bool(_ns["alineados"](p, q, r)) for p, q, r, _ in _ternas]
        _esp = [e for _, _, _, e in _ternas]
        if _obt == _esp:
            _res = mo.callout(mo.md("✅ `alineados` acierta en las seis ternas (tres alineadas, tres no)."), kind="success")
        elif not any(_obt):
            _res = mo.callout(mo.md("❌ dice que ninguna terna está alineada. Con decimales el determinante da `1e-15`, no `0`: compará con `np.isclose(det, 0)`."), kind="warn")
        elif all(_obt):
            _res = mo.callout(mo.md("❌ dice que todas están alineadas. ¿Armaste la matriz con las ternas `(x, y, 1)`, o le faltó la columna de unos (`hom`)?"), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide: esperado `{_esp}`, obtenido `{_obt}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def volumen(u, v, w):\n    cruz = ...      # u × v con sumas y productos de coordenadas: (u2 w3 − u3 w2, ..., ...)\n    return ...      # (u × v) · w\n",
        language="python", min_height=120, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("los mismos números del producto cruz, con un signo cambiado en el del
        medio").* Completá `volumen(u, v, w)`: el volumen orientado $\det[u\ v\ w]$ escrito **sólo con sumas y productos
        de coordenadas**, sin `np.cross` ni `np.linalg.det` (están bloqueados). Tenés `np`. Se verifica con `np.allclose`
        contra el determinante en 20 ternas al azar.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _ternas = [_rng.uniform(-3, 3, size=(3, 3)) for _ in range(20)]
    _esperado = np.array([lib.cuna3(*t) for t in _ternas])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _obt = np.array([float(_ns["volumen"](*t)) for t in _ternas])
        if "cross" in editor_d.value or "det" in editor_d.value:
            _res = mo.callout(mo.md("❌ `np.cross` y `np.linalg.det` están bloqueados acá: la idea es escribir las seis multiplicaciones."), kind="warn")
        elif np.allclose(_obt, _esperado):
            _res = mo.callout(mo.md("✅ coincide con `np.linalg.det` en las 20 ternas: escribiste el determinante 3×3 a mano."), kind="success")
        elif np.allclose(_obt, -_esperado):
            _res = mo.callout(mo.md(r"❌ te quedó la orientación al revés (todo con signo cambiado): revisá el orden de cada resta, $u_2 w_3 - u_3 w_2$ y no al revés, o el signo del término del medio."), kind="warn")
        elif np.allclose(np.abs(_obt), np.abs(_esperado)):
            _res = mo.callout(mo.md("❌ el tamaño está bien pero el signo falla en algunas ternas: un término tiene el signo cambiado."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primera terna: esperado `{_esperado[0]:.3f}`, obtenido `{_obt[0]:.3f}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "07a_cuna_determinante")
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

    Acá verificamos; las demostraciones (el determinante como la única operación lineal en cada vector y nula con dos
    iguales, el producto exterior en cualquier dimensión, incidencia y alineación en homogéneas):

    - [apunte, «Bloque algebraico-geométrico: productos, determinante y autovectores» (productos, determinante y autovectores)](../../apunte.pdf#nameddest=cap:11) · [apunte, «Coordenadas homogéneas: puntos como rayos» (la misma idea en cada dimensión)](../../apunte.pdf#nameddest=cap:05)
    - [ficha de la clase 5](../../clases/05.html) · [el hilo conductor](../../index.html) · [unidad 04: afinidades](../04_afines_homogeneas/index.html) (el área $\times \det A$)

    **Lo que viene:** [Núcleo y autovectores: las direcciones que no giran](../07b_nucleo_autovectores/index.html):
    cuando el detector da cero hay una dirección entera que va al cero (el núcleo), y restando $\lambda I$ se usa
    eso para encontrar las direcciones que una transformación no gira.
    """)
    return


@app.cell
def _(AB, AC, M, area_antes, area_despues, candidatos, casos, cuna_uv, lib, mo, mojones, np, parcela, u3, v3, vol, w0, w3):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _ap = lambda Mx: lib.area_poligono(lib.transformar(parcela, Mx))  # noqa: E731
    _checks = [
        ("sección 0: candidatos distintos; (3, 2) ∧ (6, 5) = 3 = det de las ternas; C = (7, 5) sí alinearía",
         len({round(v, 6) for v in candidatos.values()}) == 4 and lib.exacto(candidatos["correcta"], 3.0)
         and lib.exacto(np.linalg.det(lib.hom(mojones)), lib.cuna2(AB, AC)) and lib.alineados(mojones[0], mojones[1], [7, 5])),
        ("sección 2: u ∧ v = det M; área después = det M · área antes; parcela de área 12; casos fijos 5, 0, −5, −1, 1",
         lib.exacto(cuna_uv, np.linalg.det(M), tol=1e-6) and lib.exacto(area_despues, np.linalg.det(M) * area_antes, tol=1e-6)
         and lib.exacto(lib.area_poligono(parcela), 12.0) and lib.exacto([np.linalg.det(d) for t, d, _ in casos.values() if t == "fijo"], [5, 0, -5, -1, 1])),
        ("caja: (u × v) · w = det[u v w]; u × v = (2, −1, 1); w₀ da 4 y u + v da 0",
         lib.exacto(vol, np.linalg.det(np.column_stack([u3, v3, w3]))) and lib.exacto(np.cross(u3, v3), [2, -1, 1])
         and lib.exacto(lib.cuna3(u3, v3, w0), 4.0) and lib.exacto(lib.cuna3(u3, v3, u3 + v3), 0.0)),
        ("3.1 y (a): 5, −5, 0; p × q = (−17, 13, −3) y (p × q) · r = −3",
         lib.exacto([lib.cuna2([3, 1], [1, 2]), lib.cuna2([1, 2], [3, 1]), lib.cuna2([3, 1], [6, 2])], [5, -5, 0])
         and lib.exacto(np.cross([1, 2, 3], [4, 5, -1]), [-17, 13, -3]) and lib.exacto(lib.cuna3([1, 2, 3], [4, 5, -1], [0, 0, 1]), -3.0)),
        ("ejercicio (b): det A = 3 → área 36; espejo → −12; det 0 → 0",
         lib.exacto([_ap([[2, 1], [1, 2]]), _ap(np.diag([1, -1])), _ap([[1, 2], [2, 4]])], [36, -12, 0])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
