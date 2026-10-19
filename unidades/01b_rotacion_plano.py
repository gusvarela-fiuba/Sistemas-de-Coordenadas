# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Rotaciones II — la rotación en el plano (unidad 01b, molde v2 sobre cb104).
Una sola idea: R(θ) es "a dónde van e1 y e2"; conserva longitudes, ángulos, producto interno y área (det = 1);
R(α)R(β) = R(α+β); e^{iθ} es la misma rotación. Casos precargados con contraejemplos, estelas, parcela girando.

Chequear:  uv run marimo check --select MW unidades/01b_rotacion_plano.py
Exportar:  uv run python tools/build.py --only 01b_rotacion_plano
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
    # Rotaciones II — la rotación en el plano

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    En la lección I el mojón quedaba quieto y giraban los ejes. Acá giramos la **parcela entera** con los
    ejes quietos (rotación activa) y nos preguntamos **qué le pasa y qué no le pasa**: eso define a la rotación.

    Código de colores, igual en la figura y en el álgebra: la **primera columna** de una matriz es
    <span style="color:#1b6f6a">**teal**</span> y la **segunda** <span style="color:#b5451b">**rust**</span>; cada
    columna es la imagen de un vector de la base y se dibuja como flecha del mismo color. La parcela va en
    <span style="color:#7a4e9e">**violeta**</span>, lo de antes en gris, lo de después en teal.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("01b_rotacion_plano"))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0. Situación de campo y predicción

    Relevamos una parcela de cinco vértices con el eje $x$ a lo largo del frente. Para dibujarla con el norte para arriba
    tenemos que girar el plano entero **un cuarto de vuelta antihorario**, $90°$. Giran los cinco vértices a la vez, y
    con ellos cada distancia, cada ángulo entre lados y el área que figura en el título de propiedad.

    El vértice del frente es $(4, 1)$. Antes de mirar la figura: ¿a dónde va?
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- los números de la predicción salen de acá, nunca a mano ----------
    vertice = np.array([4.0, 1.0])
    R90 = lib.rot2(np.pi / 2)
    candidatos = {
        "correcta": R90 @ vertice,
        "sentido-contrario": R90.T @ vertice,  # R(−90°): giró para el otro lado
        "reflexion": np.diag([1.0, -1.0]) @ vertice,  # espejo respecto del eje x
        "intercambio": vertice[::-1].copy(),  # (y, x): espejo respecto de la diagonal
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            lib.vec_plano(candidatos["intercambio"]): "intercambio",
            lib.vec_plano(candidatos["correcta"]): "correcta",
            lib.vec_plano(candidatos["reflexion"]): "reflexion",
            lib.vec_plano(candidatos["sentido-contrario"]): "sentido-contrario",
        }),
        value=None,
        label=r"**Predicción.** Giramos la parcela $90°$ antihorario alrededor del origen. El vértice $(4, 1)$ va a parar a…",
    )
    prediccion
    return R90, candidatos, prediccion, vertice


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Un cuarto de vuelta antihorario es $(x, y) \mapsto (-y, x)$: el $4$ que estaba sobre el eje $x$ pasa "
                     r"al eje $y$, y el $1$ que estaba sobre $y$ pasa a $-x$. En la sección 2 el vértice recorre un arco y el largo "
                     r"$\sqrt{17}$ no cambia."),
        "sentido-contrario": ("warn",
                              r"**No.** $(1, -4)$ es el vértice girado $90°$ **horario**: lo mandaste para el otro lado. Antihorario "
                              r"es de $+x$ hacia $+y$: $(4, 0)$ va a $(0, 4)$, no a $(0, -4)$. El caso precargado de $-90°$ muestra el tuyo."),
        "reflexion": ("warn",
                      r"**No.** $(4, -1)$ es el vértice **reflejado** respecto del eje $x$: un espejo cambia el signo de una sola "
                      r"coordenada y da vuelta la parcela como un guante. Un giro mezcla las dos coordenadas y no la da vuelta; "
                      r"el área con signo lo delata (sección 2)."),
        "intercambio": ("warn",
                        r"**No.** $(1, 4)$ es $(4, 1)$ con las coordenadas intercambiadas: el espejo respecto de la diagonal "
                        r"$y = x$, no un giro. Le falta el signo: un cuarto de vuelta es $(x, y) \mapsto (-y, x)$; sin el menos la "
                        r"parcela queda dada vuelta."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** Dejamos quieto un punto, movemos otro sin cambiarle la distancia al primero, y el resto de la hoja
    se acomoda sola, cada punto a la misma distancia y con los mismos ángulos que antes. Eso es una rotación:
    **conserva distancias y ángulos**, y no da vuelta la hoja. Lo que se ve: cada punto recorre una circunferencia.

    **La matriz es "a dónde van $e_1$ y $e_2$".** Como la rotación es lineal, alcanza con saber qué hace con la base:
    $e_1 = (1, 0)$ va a $(\cos\theta, \sin\theta)$ y $e_2 = (0, 1)$, un cuarto de vuelta más adelante, va a
    $(-\sin\theta, \cos\theta)$. Esas dos imágenes, como columnas, son $R(\theta)$; un punto $x\,e_1 + y\,e_2$ va a
    $x\,Re_1 + y\,Re_2$.

    | | ¿qué conserva distancias y deja quieto el $0$? | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $x \mapsto \pm x$: nada, o espejo | en la recta **no hay giro** |
    | $\mathbb R^2$ | el giro $R(\theta)$; los espejos se descartan pidiendo $\det = +1$ | circunferencias; dos giros son un giro: $R(\alpha)R(\beta) = R(\alpha + \beta)$ |
    | $\mathbb R^3$ | hace falta además un **eje** | lección III |

    **El mismo giro como número.** Si $(x, y)$ es el complejo $z = x + iy$, multiplicar por $e^{i\theta} = \cos\theta +
    i\sin\theta$ es girarlo $\theta$: el módulo no cambia y el argumento se suma; multiplicar por $i$ es un cuarto de
    vuelta. Es la **misma operación** que $R(\theta)$ con dos números en vez de cuatro (sección 3). La demostración de
    que conservar el producto interno obliga a $R^TR = I$ está en el apunte, «Rotaciones».
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Manipulación

    Tres capas: en **gris**, grilla y cuadrado unitario antes; en **teal**, los mismos después, con las imágenes de
    $e_1$ y $e_2$ como flechas <span style="color:#1b6f6a">teal</span> y <span style="color:#b5451b">rust</span> (las
    columnas de la matriz del panel); en **violeta**, la parcela, con **estelas** en tres vértices.

    El menú trae rotaciones y **tres contraejemplos que no son rotaciones**: espejo, corte y proyección. Con una
    rotación manda el deslizador; con un contraejemplo la matriz es fija y los números vivos muestran qué falla.
    Apretá **reproducir** para ver el camino desde la identidad.
    """)
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (tipo, dato, qué se conserva y qué no) ----------
    casos = {
        "identidad (0°)": ("rotacion", 0, r"no pasa nada: área $1$, distancias, ángulos y orientación ($\det = +1$)."),
        "un cuarto de vuelta (90°)": ("rotacion", 90, r"se conserva todo: área $1$, distancias, ángulos y orientación ($\det = +1$)."),
        "media vuelta (180°)": ("rotacion", 180, r"se conserva todo; cada punto va a su opuesto, $R(180°) = -I$."),
        "giro de 30°": ("rotacion", 30, r"se conserva todo: área $1$, distancias, ángulos y orientación ($\det = +1$)."),
        "−90° (horario)": ("rotacion", -90, r"se conserva todo; gira para el otro lado: $R(-90°) = R(90°)^T$."),
        "espejo diag(1, −1) — no es rotación": ("matriz", np.diag([1.0, -1.0]),
                                               r"conserva distancias pero **da vuelta la orientación**: $\det = -1$, el área con signo da $-1$."),
        "corte [[1, 0.5], [0, 1]] — no es rotación": ("matriz", np.array([[1.0, 0.5], [0.0, 1.0]]),
                                                      r"conserva el área ($\det = 1$) pero **no las distancias ni los ángulos**: $R^TR \neq I$."),
        "proyección [[1, 0], [0, 0]] — no es rotación": ("matriz", np.array([[1.0, 0.0], [0.0, 0.0]]),
                                                         r"**no conserva nada**: área $0$, todo cae sobre el eje $x$, no hay vuelta atrás."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="giro de 30°", label="caso precargado")
    # ---------- objetos fijos de la figura ----------
    rango = 6
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # cinco vértices enteros; el frente es (4, 1)
    con_estela = [1, 2, 3]
    par_distancia = (0, 2)
    return caso, casos, con_estela, par_distancia, parcela, rango


@app.cell
def _(caso, casos, mo):
    # el deslizador depende del caso: arranca en el ángulo del caso y queda deshabilitado en los contraejemplos
    _tipo, _dato, _ = casos[caso.value]
    es_rotacion = _tipo == "rotacion"
    angulo = mo.ui.slider(-180, 180, value=_dato if es_rotacion else 0, step=1, label="θ (°)", show_value=True, disabled=not es_rotacion)
    return angulo, es_rotacion


@app.cell
def _(angulo, caso, casos, con_estela, es_rotacion, go, lib, mo, np, par_distancia, parcela, rango):
    _tipo, _dato, que_conserva = casos[caso.value]
    if es_rotacion:
        theta = np.deg2rad(angulo.value)
        M = lib.rot2(theta)
        camino = [lib.rot2(t) for t in np.linspace(0, theta, 36)]
    else:
        theta = 0.0
        M = np.asarray(_dato, dtype=float)
        camino = [np.eye(2) + s * (M - np.eye(2)) for s in np.linspace(0, 1, 36)]

    def _dinamicas(i):
        """Las trazas que cambian con el cuadro i, en orden fijo."""
        Mi = camino[i]
        f = go.Figure()
        lib.capa_despues(f, Mi, rango)
        lib.objeto(f, lib.transformar(parcela, Mi), lib.VIOLETA_OBJETO, "parcela después",
                   estelas=lib.estelas(parcela[con_estela], camino[: i + 1]))
        return list(f.data)

    _titulo = f"R({angulo.value}°) · activa: gira la parcela" if es_rotacion else f"{caso.value}"
    figura = lib.figura_plano(rango + 1, _titulo)
    lib.capa_antes(figura, rango)
    lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    cuadrado = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    area_cuadrado = lib.area_poligono(lib.transformar(cuadrado, M))
    parcela_despues = lib.transformar(parcela, M)
    _i, _j = par_distancia
    dist_antes = float(np.linalg.norm(parcela[_i] - parcela[_j]))
    dist_despues = float(np.linalg.norm(parcela_despues[_i] - parcela_despues[_j]))
    _nombre = f"R({angulo.value}°)" if es_rotacion else "M"
    _panel = mo.vstack([
        mo.md("**Controles**"),
        caso,
        angulo,
        mo.md(rf"""
        **Números vivos**

        - área con signo del cuadrado unitario después: $\mathbf{{{lib.num_tex(area_cuadrado, 4)}}}$ ($\det = {lib.num_tex(np.linalg.det(M), 4)}$)
        - distancia entre los vértices ${_i}$ y ${_j}$: antes ${lib.num_tex(dist_antes, 4)}$, después $\mathbf{{{lib.num_tex(dist_despues, 4)}}}$
        - el vértice $(4, 1)$ va a ${lib.vec_tex(parcela_despues[1])}$

        $${_nombre} = {lib.matriz_coloreada(M)}$$

        Columna 1 = <span style="color:{lib.COLORES[0]}">$Me_1$</span>, columna 2 = <span style="color:{lib.COLORES[1]}">$Me_2$</span>:
        las dos flechas. **Qué pasa acá:** {que_conserva}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, area_cuadrado, dist_antes, dist_despues, parcela_despues, theta


@app.cell
def _(lib, mo, np):
    # 3.1  un cuarto de vuelta: matriz y complejo
    _R90 = lib.rot2(np.pi / 2)
    _v = np.array([2.0, 1.0])
    _w = _R90 @ _v
    _z = (2 + 1j) * 1j
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno con enteros; derecha, la misma en numpy con el código a la vista. Si no dicen
        lo mismo, algo está mal en alguna de las dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Un cuarto de vuelta, de dos maneras.** $\cos 90° = 0$, $\sin 90° = 1$:

            $$R(90°)\begin{pmatrix} 2 \\ 1 \end{pmatrix} = \begin{pmatrix} \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{-1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{0} \end{pmatrix}\begin{pmatrix} 2 \\ 1 \end{pmatrix}
            = 2\,\textcolor{#1b6f6a}{\binom{0}{1}} + 1\,\textcolor{#b5451b}{\binom{-1}{0}} = \begin{pmatrix} -1 \\ 2 \end{pmatrix}.$$

            El resultado es $2\,Re_1 + 1\,Re_2$: dos veces la flecha teal más una vez la rust.

            Con complejos: $(2 + i)\,i = 2i + i^2 = -1 + 2i$. El mismo punto. Y $(2,1)$ y $(-1,2)$ tienen el mismo largo
            $\sqrt5$ y forman ángulo recto.
            """),
            mo.vstack([
                mo.md("```python\nR90 = lib.rot2(np.pi / 2)\nv = np.array([2.0, 1.0])\nw = R90 @ v\nz = (2 + 1j) * 1j            # el mismo giro, en complejos\n```"),
                mo.md(f"`w` = `{np.round(_w, 3).tolist()}` · `z` = `{_z}`  \n`np.linalg.norm(v)` = `{np.linalg.norm(_v):.4f}` · `np.linalg.norm(w)` = `{np.linalg.norm(_w):.4f}` · `v @ w` = `{float(_v @ _w):.1f}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(lib, mo, np):
    # 3.2  qué se conserva: producto interno, RᵀR = I, det = 1 (y el espejo que no)
    _R = lib.rot2(np.pi / 2)
    _v, _w = np.array([2.0, 1.0]), np.array([1.0, 3.0])
    _espejo = np.diag([1.0, -1.0])
    mo.hstack([
        mo.md(r"""
        **3.2 Lo que se conserva, como cuenta.** Con $v = (2,1)$, $w = (1,3)$:
        $\langle v, w\rangle = 2 + 3 = 5$; $Rv = (-1, 2)$, $Rw = (-3, 1)$, $\langle Rv, Rw\rangle = 3 + 2 = 5$.
        Conservar el producto interno es conservar **largos y ángulos de una vez**. Que valga para todo par equivale a

        $$R^TR = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix} = I$$

        (en general, $\cos^2\theta + \sin^2\theta = 1$ en la diagonal). El **espejo** $\mathrm{diag}(1,-1)$ también cumple
        $A^TA = I$; lo separa el determinante: $\det R(\theta) = 1$ (área y orientación conservadas), $\det\mathrm{diag}(1,-1) = -1$.
        """),
        mo.vstack([
            mo.md("```python\nR = lib.rot2(np.pi / 2)\nv, w = np.array([2.0, 1.0]), np.array([1.0, 3.0])\nantes, despues = v @ w, (R @ v) @ (R @ w)\nRtR = R.T @ R\nespejo = np.diag([1.0, -1.0])\n```"),
            mo.md(f"`antes` = `{float(_v @ _w):.1f}` · `despues` = `{float((_R @ _v) @ (_R @ _w)):.1f}`  \n`RtR` =\n```\n{np.round(_R.T @ _R, 3)}\n```\n"
                  f"`np.linalg.det(R)` = `{np.linalg.det(_R):.1f}` · `espejo.T @ espejo` es `I`: `{bool(np.allclose(_espejo.T @ _espejo, np.eye(2)))}` · `np.linalg.det(espejo)` = `{np.linalg.det(_espejo):.1f}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(lib, mo, np):
    # 3.3  dos giros seguidos son un giro
    _Ra, _Rb = lib.rot2(np.deg2rad(30)), lib.rot2(np.deg2rad(60))
    mo.hstack([
        mo.md(r"""
        **3.3 Dos giros seguidos son un giro.** $R(30°)$ y después $R(60°)$, o al revés, da $R(90°)$: en el plano las
        rotaciones **conmutan** y los ángulos se suman. Es el $e^{i\alpha}e^{i\beta} = e^{i(\alpha+\beta)}$ de los complejos.

        $$R(60°)R(30°) = R(30°)R(60°) = R(90°) = \begin{pmatrix} \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{-1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{0} \end{pmatrix}.$$

        En 3D esto deja de ser cierto (lección III).
        """),
        mo.vstack([
            mo.md("```python\nRa, Rb = lib.rot2(np.deg2rad(30)), lib.rot2(np.deg2rad(60))\nnp.allclose(Rb @ Ra, lib.rot2(np.pi / 2))\nnp.allclose(Ra @ Rb, Rb @ Ra)\n```"),
            mo.md(f"`Rb @ Ra` =\n```\n{np.round(_Rb @ _Ra, 3)}\n```\n`{bool(np.allclose(_Rb @ _Ra, lib.rot2(np.pi / 2)))}` · `{bool(np.allclose(_Ra @ _Rb, _Rb @ _Ra))}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(M, lib, mo, np, parcela):
    _tres = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]])
    _salida = lib.transformar(_tres, lib.rot2(np.pi / 2))
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **una nube de puntos es un array $N\times2$, una fila por punto**, y se gira entera con una línea.
        La cuenta "matriz por vector" es $Rv$ con $v$ columna; con los puntos en filas hay que transponer,
        $(Rv)^T = v^T R^T$, y por eso la función es `puntos @ R.T`. Eso es `lib.transformar(puntos, R)`.
        """),
        mo.md("```python\ntres = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]])   # shape (3, 2): e1, e2 y (2, 1)\ntres @ lib.rot2(np.pi / 2).T                             # cada fila girada 90°\n```"),
        mo.md(f"`tres.shape` = `{_tres.shape}` → resultado:\n```\n{np.round(_salida, 3)}\n```\nLas filas son $(0,1)$, $(-1,0)$ y $(-1,2)$: las imágenes de $e_1$, $e_2$ y $(2,1)$, como en 3.1. "
              f"La misma línea gira la parcela (`{parcela.shape}` → `{lib.transformar(parcela, M).shape}`) y la grilla entera."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — medio** *("Hay transformaciones que se definen completamente por qué propiedades de los objetos
        transformados mantienen").* ¿Qué ángulo $\theta$ lleva $(1, 0)$ a $(0, -1)$? Escribí $R(\theta)$ con números y
        verificá que el largo de $(1,0)$ no cambia. ¿Hay otra matriz ortogonal, que **no** sea una rotación, que también
        lleve $(1,0)$ a $(0,-1)$? ¿Qué la distingue?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        La primera columna de $R(\theta)$ es la imagen de $e_1$: $(\cos\theta, \sin\theta) = (0, -1)$, así que
        $\theta = -90°$. $R(-90°) = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$; el largo es $1$ antes y después. ✓

        Sí: $A = \begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}$ (espejo respecto de $y = -x$) también manda $(1,0)$ a
        $(0,-1)$ y cumple $A^TA = I$. Pero $\det A = -1$. Mandar un solo punto no fija la transformación; conservar
        distancias **y orientación** sí.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_b = mo.ui.code_editor(
        value="def rotar(puntos, theta):\n    c, s = np.cos(theta), np.sin(theta)\n    R = ...   # armá la matriz 2×2\n    return ...   # una fila por punto: ¿quién va transpuesto?\n",
        language="python",
        min_height=140,
        label="ejercicio (b)",
    )
    mo.vstack([
        mo.md(r"""
        **(b) Código con hueco — medio** *("Hay una equivalencia entre operaciones en $\mathbb C$ y en $\mathbb R^2$"; la
        idea de la sección 4).* Completá `rotar(puntos, theta)`: recibe una nube $N\times2$ y un ángulo en **radianes** y
        devuelve la nube girada. Tenés `np`. Se verifica con `np.allclose` sobre 20 puntos al azar.
        """),
        editor_b,
    ])
    return (editor_b,)


@app.cell
def _(editor_b, lib, mo, np):
    _puntos = np.random.default_rng(0xDDDE).uniform(-5, 5, size=(20, 2))
    _theta = np.deg2rad(37)
    _esperado = lib.transformar(_puntos, lib.rot2(_theta))
    _ns = {"np": np}
    try:
        exec(editor_b.value, _ns)
        _obtenido = np.asarray(_ns["rotar"](_puntos, _theta), dtype=float)
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ la forma del resultado es `{_obtenido.shape}`; tiene que ser `{_esperado.shape}` (una fila por punto)."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ `rotar` coincide con la referencia en los 20 puntos (θ = 37°)."), kind="success")
        elif np.allclose(_obtenido, lib.transformar(_puntos, lib.rot2(-_theta))):
            _res = mo.callout(mo.md(r"❌ gira para el otro lado: te quedó $R(-\theta)$. ¿El seno negativo va arriba a la derecha o abajo a la izquierda?"), kind="warn")
        elif np.allclose(_obtenido, _puntos @ lib.rot2(_theta)):
            _res = mo.callout(mo.md(r"❌ casi: usaste `puntos @ R`, que es $R^T$ aplicada a cada fila. Con filas = puntos va `puntos @ R.T`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primer punto: esperado `{np.round(_esperado[0], 3).tolist()}`, obtenido `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "01b_rotacion_plano")
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

    En esta unidad demostramos qué conserva una rotación y qué no conservan el espejo, el corte y la proyección. Las demostraciones
    (producto interno $\Rightarrow R^TR = I$, el determinante como orientación, complejos $\leftrightarrow$ matriz):

    - [apunte, «Rotaciones» (rotaciones)](../../apunte.pdf#nameddest=cap:rotaciones)
    - [ficha de la clase 1](../../clases/01.html) · [unidad anterior: Rotaciones I](../01a_punto_quieto/index.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** [Rotaciones III — tres ejes y el orden importa](../01c_rotaciones_3d/index.html): en 3D hay un
    giro por cada eje, no conmutan, y toda composición es un solo giro alrededor de un eje fijo.
    """)
    return


@app.cell
def _(M, R90, area_cuadrado, candidatos, casos, dist_antes, dist_despues, es_rotacion, lib, mo, np, parcela, parcela_despues, theta, vertice):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _checks = [
        ("los cuatro candidatos de la predicción son distintos entre sí",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == len(candidatos)),
        ("R(90°)(4, 1) = (−1, 4)", lib.exacto(candidatos["correcta"], [-1, 4]) and lib.exacto(R90 @ vertice, [-1, 4])),
        ("3.1: R(90°)(2, 1) = (−1, 2) y (2 + i)·i = −1 + 2i", lib.exacto(R90 @ [2, 1], [-1, 2]) and (2 + 1j) * 1j == -1 + 2j),
        ("3.2: el producto interno se conserva", lib.exacto((R90 @ [2, 1]) @ (R90 @ [1, 3]), 5.0)),
        ("3.2: RᵀR = I y det = 1 para 13 ángulos",
         all(lib.exacto(lib.rot2(t).T @ lib.rot2(t), np.eye(2)) and lib.exacto(np.linalg.det(lib.rot2(t)), 1.0) for t in np.linspace(-np.pi, np.pi, 13))),
        ("3.3: R(60°)R(30°) = R(90°)", lib.exacto(lib.rot2(np.deg2rad(60)) @ lib.rot2(np.deg2rad(30)), R90)),
        ("sección 2: transformar(parcela, M) = (M parcelaᵀ)ᵀ", lib.exacto(parcela_despues, (M @ parcela.T).T)),
        ("los contraejemplos no son rotaciones",
         all(not (lib.exacto(_d.T @ _d, np.eye(2)) and lib.exacto(np.linalg.det(_d), 1.0)) for _t, _d, _ in casos.values() if _t == "matriz")),
        ("ejercicio (a): R(−90°) y el espejo de y = −x mandan (1, 0) a (0, −1)",
         lib.exacto(lib.rot2(-np.pi / 2) @ [1, 0], [0, -1]) and lib.exacto(np.array([[0, -1], [-1, 0]]) @ [1, 0], [0, -1])),
    ]
    if es_rotacion:
        _checks += [
            ("una rotación conserva el área del cuadrado unitario", lib.exacto(area_cuadrado, 1.0, tol=1e-6)),
            ("una rotación conserva la distancia entre vértices", lib.exacto(dist_antes, dist_despues, tol=1e-6)),
            ("Rᵀ = R(−θ)", lib.exacto(M.T, lib.rot2(-theta))),
        ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
