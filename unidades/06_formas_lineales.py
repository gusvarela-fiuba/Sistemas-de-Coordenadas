# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Formas lineales y dualidad (lección 06, molde v2 sobre cb104). Clase 4 (parte dictada el 2026-09-30).

Una sola idea: una forma lineal es una regla graduada tirada en el plano (ℓ(p) = a x + b y, curvas de nivel = rectas
paralelas, se escribe como fila). Si los puntos van con A, la regla va al revés (ℓ' = ℓ A⁻¹) para que la lectura no
cambie: eso es la dualidad, y por eso una recta (una forma igualada a cero) cambia al revés que un punto.

Chequear:  uv run marimo check --select MW unidades/06_formas_lineales.py
Exportar:  uv run python tools/build.py --only 06_formas_lineales
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
    # Formas lineales y dualidad

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Sigo la clase 4 (la parte dictada el 30/9). La pregunta: **¿Qué es una regla graduada tirada en el plano, y por qué
    una recta se transforma al revés que un punto?** El gancho: *las curvas de nivel de un plano acotado son las marcas
    de una regla: cerca de cada punto, la cota es una forma lineal.*

    Colores: grilla de la obra en **gris**, parcela en <span style="color:#7a4e9e">**violeta**</span>, la regla (sus
    rectas de nivel) en <span style="color:#1b6f6a">**teal**</span>. En las matrices, la **primera columna** es
    <span style="color:#1b6f6a">**teal**</span> y la **segunda** <span style="color:#b5451b">**rust**</span>.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    fila = np.array([2.0, 1.0])  # la cota es h(x, y) = 2x + y + 100: la fila (2, 1) más la constante
    h0 = 100.0
    A_pred = np.array([[2.0, 1.0], [0.0, 1.0]])  # la deformación del plano digitalizado: no es un giro, a propósito
    p_pred = np.array([1.0, 1.0])
    candidatos = {
        "correcta": lib.forma_transformada(fila, A_pred),  # ℓ A⁻¹
        "como-punto": A_pred @ fila,  # la fila movida como si fuera un punto
        "hacia-atras": fila @ A_pred,  # ℓ A: la regla que sobre el p ORIGINAL lee lo que ℓ lee sobre A p
        "mismas": fila.copy(),
    }
    prediccion = mo.ui.radio(
        options={lib.vec_plano(candidatos[k]) + ("  (la misma)" if k == "mismas" else ""): k
                 for k in ("como-punto", "mismas", "correcta", "hacia-atras")},
        value=None,
        label=r"**Predicción.** Si los puntos del plano van a $p' = Ap$, la fila que da la cota sobre $p'$ es…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Un lote plano pero inclinado: la cota, en metros, es $h(x, y) = 2x + y + 100$ sobre la grilla de la obra. Las
        curvas de nivel $h = 101, 102, 103, \ldots$ son **rectas paralelas**: la cota es la fila $(2, 1)$ más una
        constante. El mojón $p = (1, 1)$ está a $h = 103$.

        El plano digitalizado quedó deformado: cada punto mío aparece en $p' = Ap$ con
        $A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$ (dobla $x$ y la corre con $y$). La cota del mojón **no**
        cambió; necesito la fila que, aplicada a $p' = (3, 1)$, siga dando $3$. Si la deformación fuera un giro de
        $90°$ la fila giraría igual que los puntos, $(2, 1) \mapsto (-1, 2)$ de las dos maneras, y no se vería nada
        raro; por eso elegí una $A$ que no es un giro.
        """),
        prediccion,
    ])
    return A_pred, candidatos, fila, h0, p_pred, prediccion


@app.cell
def _(A_pred, candidatos, lib, mo, p_pred, prediccion):
    _pp = A_pred @ p_pred
    _lee = {k: lib.num_tex(v @ _pp) for k, v in candidatos.items()}
    _cp, _ha = lib.vec_tex(candidatos["como-punto"]), lib.vec_tex(candidatos["hacia-atras"])
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** $(1, 0)$ es $\ell A^{{-1}}$: la fila por la inversa, **a la derecha**. Control: $(1, 0)\cdot(3, 1) = "
                     rf"{_lee['correcta']}$, lo mismo que $(2, 1)\cdot(1, 1)$. Las marcas quedaron verticales: la regla se deformó **con** la figura."),
        "como-punto": ("warn",
                       rf"**No.** ${_cp}$ es $A\,\ell^T$: moviste la fila como si fuera un punto, y sobre $p' = (3, 1)$ lee ${_lee['como-punto']}$, "
                       r"no $3$. Una fila no es una flecha sino una familia de rectas; para seguir midiendo lo mismo va con $A^{-1}$, no con $A$."),
        "hacia-atras": ("warn",
                        rf"**No.** ${_ha}$ es $\ell A$, sin invertir. Esa regla responde otra pregunta: sobre el $p$ **original** lee lo que "
                        rf"$\ell$ lee sobre $Ap$ (${_ha}\cdot(1, 1) = 7 = (2, 1)\cdot(3, 1)$); sobre $p'$ da ${_lee['hacia-atras']}$. Para "
                        r"arrastrar la regla con la figura hay que deshacer $A$: $\ell A^{-1}$."),
        "mismas": ("warn",
                   rf"**No.** Con la misma fila, $(2, 1)\cdot(3, 1) = {_lee['mismas']}$: el mojón subiría $4$ m sin moverse. Los números de "
                   r"la fila son coeficientes **respecto de unas coordenadas**: si cambian las de los puntos, cambian los de la fila, al revés."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    _texto = mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** La lectura. Si los puntos van con $A$ y la regla con $A^{-1}$, cada punto sigue marcando el
    mismo número en cada regla; en homogéneas, sigue estando en las mismas rectas. "Convertimos todo para que nada
    cambie" (el profesor, 30/9).

    **Una forma lineal es una regla graduada.** Toma un vector y devuelve un número respetando sumas y escalas. En
    coordenadas es una **fila**: $\ell = (a, b)$ y $\ell(p) = ax + by$, fila por columna. "No existe el vector fila.
    Lo que comúnmente llamamos vector fila se llama *forma lineal*" (profesor, 30/9, transcripción auto-traducida).

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $\ell(x) = ax$ | la escala de la regla: marcas $0, 1, 2, \ldots$ a distancia $1/a$ |
    | $\mathbb R^2$ | $\ell(x, y) = ax + by$, la fila $(a, b)$ | rectas paralelas equiespaciadas, separación $1/\lvert(a, b)\rvert$ |
    | $\mathbb R^3$ | $\ell(x, y, z) = ax + by + cz$ | planos paralelos equiespaciados |

    La separación, en palabras del profesor: "cuanto más largo el vector, más apretadas las curvas. Si el módulo es
    $1$ la separación es $1$; si mide $2$, $\tfrac12$; si mide $4$, $\tfrac14$". Y "si tengo dos formas lineales tengo
    una grilla": un vector queda ubicado por qué par de marcas lo cruza. $\mathsf x = (1, 0)$ y $\mathsf y = (0, 1)$
    son la **base dual**, las reglas que leen cada coordenada; cualquier forma es $a\,\mathsf x + b\,\mathsf y$, y
    todas juntas forman el espacio **dual**.

    **La flecha $(a, b)$ es perpendicular a las marcas sólo en la base canónica**, donde $\ell(p) = \langle (a, b),
    p\rangle$ y la forma se disfraza de vector ([Producto interno](../02_producto_interno/index.html): "no hay base
    privilegiada salvo por el producto interno"). Si deformo el plano con una $A$ que no lo conserva, $A(a, b)^T$ deja
    de ser perpendicular a las rectas nuevas; la regla, no.

    **Dualidad: la regla se transforma al revés.** Si $p' = Ap$, la fila que lee lo mismo sobre $p'$ es

    $$\ell' = \ell A^{-1} \qquad\text{porque}\qquad \ell'(p') = \ell A^{-1} A\,p = \ell(p).$$

    "Los puntos se transforman con la transformación; las formas lineales con la inversa, del otro lado. Así todas las
    relaciones se conservan" (profesor, 30/9). Una recta es una forma igualada a cero, $\ell p = 0$ en homogéneas: por
    eso cambia con $A^{-1}$ a la derecha (o $A^{-T}$ como columna) mientras un punto cambia con $A$. En
    [Cambio de base](../08_cambio_de_base/index.html), $c = B^{-1}p$ y la fila pasa a $\ell B$.

    | | punto $p$ | forma $\ell$ |
    |---|---|---|
    | se escribe | columna | fila |
    | se transforma | $p' = Ap$ (a la izquierda) | $\ell' = \ell A^{-1}$ (a la derecha) |
    | se dibuja | una flecha | una familia de rectas de nivel |
    | juntos | $\ell\,p$ es un número: la medición | $\ell\,p = 0$ es una recta |

    Esto es una **muestra**; la demostración está en el apunte, sección 11.
    """)
    mo.vstack([_texto, mo.callout(mo.md(r"""
    **El recordatorio del 14/10 (clase 9).** El profesor se corrigió en vivo: "el gradiente de una función es un
    vector… no, mentí, lo dije mal. **El gradiente es una forma lineal, no un vector**: me permite hacer una
    aproximación lineal de la función" (transcripción auto-traducida del inglés, línea 114). Es esta misma regla:
    cerca de un punto, los escalones de altura son las marcas de $\nabla h = (h_x, h_y)$. Dibujarlo como flecha
    perpendicular a las curvas de nivel sólo tiene sentido con un producto interno fijado: si cambio de unidades en un
    eje (metros en $x$, pies en $y$), o estoy en el plano $(d\varphi, d\lambda)$ del elipsoide, donde un paso en
    $\varphi$ y uno en $\lambda$ no miden lo mismo ($M \ne N\cos\varphi$), la flecha perpendicular en la grilla **no**
    es perpendicular en el terreno. La regla sigue valiendo; lo que falta es la métrica:
    [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html). Es el segundo de los cuatro cambios de chip de
    la [Estación 0](../00_desaprender_el_cbc/index.html).
    """), kind="neutral")])
    return


@app.cell
def _(lib, mo, np):
    # ---------- casos precargados: etiqueta → (tipo, deslizador (min, max, valor, paso, etiqueta) o None, A(param), qué pasa) ----------
    B_08 = np.array([[3.0, 1.0], [1.0, 2.0]])  # la base oblicua de frentes y lados (Cambio de base)
    casos = {
        "la cota 2x + y, sin deformar": ("fijo", None, lambda s: np.eye(2),
            r"la regla $(2, 1)$: marcas cada $1/\sqrt5 = 0.447$, perpendiculares a la flecha $(2, 1)$. El mojón está en la marca $3$."),
        "giro de 30°": ("rotacion", (-180, 180, 30, 1, "θ (°)"), lambda t: lib.rot2(np.deg2rad(t)),
            r"$A^{-1} = A^T$: la fila gira como un punto y la flecha sigue perpendicular. Con una rotación la dualidad no se ve."),
        "escala anisótropa diag(2, 1)": ("param", (0.5, 2.5, 2.0, 0.1, "k: factor en x"), lambda k: np.diag([k, 1.0]),
            r"los puntos se estiran en $x$ por $k$; la fila se divide: $(2/k, 1)$. Las marcas se separan y $A(2, 1)^T$ **deja de ser perpendicular** a ellas."),
        "cizalla [[1, 1], [0, 1]]": ("param", (-1.5, 1.5, 1.0, 0.1, "s: corte"), lambda s: np.array([[1.0, s], [0.0, 1.0]]),
            r"$A^{-1}$ corta al revés: $(2, 1) \mapsto (2, 1 - 2s)$. Con $s = \tfrac12$ las marcas quedan verticales: la regla sólo lee $x$."),
        "a la base oblicua de 08 (A = B⁻¹)": ("fijo", None, lambda s: np.linalg.inv(B_08),
            r"coordenadas nuevas $c = B^{-1}p$ y fila $\ell B = (7, 4)$: en frentes y lados la cota es $7c_1 + 4c_2 + 100$. Mismo mojón, misma cota, otros números."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="escala anisótropa diag(2, 1)", label="caso precargado")
    mo.vstack([
        mo.md(r"""
        ## 2. Manipulación

        Tres capas. En **gris**, grilla, parcela y regla antes, y la fila $(2, 1)$ llevada **como si fuera un punto**
        ($A(2, 1)^T$, flecha gruesa). En **teal**, la regla después ($\ell A^{-1}$, marca $0$ gruesa, valor de cada
        marca) y la flecha $(\ell A^{-1})^T$, que sí es perpendicular a las marcas nuevas. En **violeta**, la parcela
        deformada y el mojón con su cota. **Reproducir** va de la identidad a $A$: la regla acompaña a la figura y la
        lectura del mojón no cambia.
        """),
        caso,
    ])
    return B_08, caso, casos


@app.cell
def _(caso, casos, mo):
    # el deslizador depende del caso: rango y etiqueta son los del caso; en los fijos queda deshabilitado
    _tipo, _spec, _, _ = casos[caso.value]
    _lo, _hi, _v, _paso, _etq = _spec if _spec else (0, 1, 0, 1, "sin parámetro en este caso")
    param = mo.ui.slider(_lo, _hi, value=_v, step=_paso, label=_etq, show_value=bool(_spec), disabled=_spec is None)
    return (param,)


@app.cell
def _(caso, casos, fila, go, h0, lib, mo, np, param):
    _tipo, _, _fn, que_pasa = casos[caso.value]
    A = np.asarray(_fn(param.value), dtype=float)
    if _tipo == "rotacion":
        camino = [lib.rot2(t) for t in np.linspace(0, np.deg2rad(param.value), 30)]
    else:
        camino = [np.eye(2) + s * (A - np.eye(2)) for s in np.linspace(0, 1, 30)]
    parcela = np.array([[1.0, 1.0], [3.0, 1.0], [3.0, 2.0], [2.0, 3.0], [1.0, 3.0]])
    mojon = parcela[0]
    niveles = np.arange(-40, 41, 2)
    rango = 8
    fila_despues = lib.forma_transformada(fila, A)
    mojon_despues = A @ mojon

    def _dinamicas(i):
        """Las trazas que cambian con el cuadro i, siempre en el mismo orden (7 trazas)."""
        Mi = camino[i]
        li = lib.forma_transformada(fila, Mi)
        f = go.Figure()
        lib.rectas_de_nivel(f, li, niveles, rango, lib.TEAL_DESPUES, "regla después: ℓ A⁻¹", destacar=0)
        lib.objeto(f, lib.transformar(parcela, Mi), lib.VIOLETA_OBJETO, "parcela después")
        lib.flecha(f, (0, 0), Mi @ fila, lib.GRIS_ANTES, "A(2, 1)ᵀ: la fila llevada como punto", ancho=4)
        lib.flecha(f, (0, 0), li, lib.TEAL_DESPUES, "(ℓ A⁻¹)ᵀ: perpendicular a las marcas nuevas", ancho=3)
        lib.punto(f, Mi @ mojon, nombre="mojón después", texto=f"h = {h0 + li @ (Mi @ mojon):.1f}")
        return list(f.data)

    figura = lib.figura_plano(rango, f"{caso.value} · la lectura del mojón no cambia")
    lib.capa_antes(figura, rango, cuadrado=False)
    lib.rectas_de_nivel(figura, fila, niveles, rango, lib.GRIS_ANTES, "regla antes: (2, 1)", etiquetas=False, destacar=None, ancho=0.8)
    lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    _ang = np.degrees(lib.angulo(A @ fila, lib.perp2(fila_despues)))
    _ang = min(_ang, 180 - _ang)
    _panel = mo.vstack([
        mo.md("**Controles**"), param,
        mo.md(rf"""
        **Números vivos**

        - $\ell = {lib.pmat(fila.reshape(1, 2), dec=0)}$, $A = {lib.matriz_coloreada(A)}$, $A^{{-1}} = {lib.pmat(np.linalg.inv(A))}$
        - $\ell' = \ell A^{{-1}} = {lib.pmat(fila_despues.reshape(1, 2))}$; separación entre marcas: antes
          ${lib.num_tex(1 / np.linalg.norm(fila))}$, después ${lib.num_tex(1 / np.linalg.norm(fila_despues))}$
        - mojón: $\ell p = {lib.num_tex(fila @ mojon)}$; $p' = Ap = {lib.vec_tex(mojon_despues)}$;
          $\ell' p' = {lib.num_tex(fila_despues @ mojon_despues)}$ → `np.allclose`: `{bool(np.allclose(fila @ mojon, fila_despues @ mojon_despues))}`
        - ángulo entre $A(2, 1)^T$ y las marcas nuevas: $\mathbf{{{_ang:.1f}°}}$ ($90°$ sólo si $A$ conserva el producto interno)

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.6)
    mo.vstack([mo.ui.plotly(figura), _panel])
    return A, fila_despues, mojon, mojon_despues


@app.cell
def _(lib, mo, np):
    _A = np.diag([2.0, 1.0])
    _l, _p = np.array([2.0, 1.0]), np.array([1.0, 1.0])
    _lp = lib.forma_transformada(_l, _A)
    T = np.array([[1.2, 0.5], [-0.1, 1.3]])
    v_prof = np.array([3.0, 4.0])
    formas_prof = np.array([[1.0, 1.0], [-1.0, 2.0]])  # una fila por forma
    formas_prof_despues = np.array([lib.forma_transformada(f, T) for f in formas_prof])
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, el cuaderno; derecha, numpy. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La regla arrastrada por una escala.** $A = \mathrm{diag}(2, 1)$, $\ell = (2, 1)$, $p = (1, 1)$:

            $$\ell p = 2 + 1 = 3, \qquad p' = Ap = \begin{pmatrix} \textcolor{#1b6f6a}{2} & \textcolor{#b5451b}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} \end{pmatrix}\binom11 = \binom21.$$

            $A^{-1} = \mathrm{diag}(\tfrac12, 1)$ y la fila va a la derecha:

            $$\ell' = \ell A^{-1} = (2\cdot\tfrac12 + 1\cdot0,\ 2\cdot0 + 1\cdot1) = (1, 1), \qquad \ell' p' = 2 + 1 = 3.\ \checkmark$$

            Lo que **no** hay que hacer: $A\ell^T = (4, 1)$ y $(4, 1)\cdot(2, 1) = 9 \ne 3$.
            """),
            mo.vstack([
                mo.md("```python\nA = np.diag([2., 1.])\nl = np.array([2., 1.])\np = np.array([1., 1.])\n# la fila, a la derecha\nlp = l @ np.linalg.inv(A)\nnp.allclose(l @ p, lp @ (A @ p))\n```"),
                mo.md(f"`l @ p` = `{_l @ _p:g}` · `lp` = `{np.round(_lp, 3).tolist()}`  \n"
                      f"`lp @ (A @ p)` = `{_lp @ (_A @ _p):g}` · `allclose` = `{bool(np.allclose(_l @ _p, _lp @ (_A @ _p)))}`  \n"
                      f"mal: `A @ l` = `{np.round(_A @ _l, 3).tolist()}` → lee `{(_A @ _l) @ (_A @ _p):g}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 El ejercicio del 30/9.** Formas $(1, 1)$ y $(-1, 2)$, vector $v = (3, 4)$,
            $T = \begin{pmatrix} \textcolor{#1b6f6a}{1.2} & \textcolor{#b5451b}{0.5} \\ \textcolor{#1b6f6a}{-0.1} & \textcolor{#b5451b}{1.3} \end{pmatrix}$.
            Antes: $(1, 1)\cdot v = 7$ y $(-1, 2)\cdot v = 5$: $v$ está en "la séptima con la quinta".
            $\det T = 1.61$ y, por adjunta sobre determinante, $T^{-1} = \tfrac1{1.61}\begin{pmatrix} 1.3 & -0.5 \\ 0.1 & 1.2 \end{pmatrix}$:

            $$Tv = \binom{5.6}{4.9}, \qquad (1, 1)\,T^{-1} = \tfrac{(1.4,\ 0.7)}{1.61} = (0.870,\ 0.435), \qquad (-1, 2)\,T^{-1} = \tfrac{(-1.1,\ 2.9)}{1.61} = (-0.683,\ 1.801).$$

            Después: $0.870\cdot5.6 + 0.435\cdot4.9 = 7.00$ y $-0.683\cdot5.6 + 1.801\cdot4.9 = 5.00$: el mismo
            cruce. La $(1, 1)$ "quedó más acostada" ($45° \to 26.6°$) y más corta: sus marcas se separaron.
            """),
            mo.vstack([
                mo.md("```python\nT = np.array([[1.2, 0.5], [-0.1, 1.3]])\nv = np.array([3., 4.])\n# una fila por forma\nF = np.array([[1., 1.], [-1., 2.]])\nF @ v                   # lecturas antes\n# las formas arrastradas\nF2 = F @ np.linalg.inv(T)\nF2 @ (T @ v)            # lecturas después\n```"),
                mo.md(f"`det(T)` = `{np.linalg.det(T):.2f}` · `T @ v` = `{np.round(T @ v_prof, 3).tolist()}` · `F @ v` = `{np.round(formas_prof @ v_prof, 3).tolist()}`  \n"
                      f"`F2` =\n```\n{np.round(formas_prof_despues, 3)}\n```\n`F2 @ (T @ v)` = `{np.round(formas_prof_despues @ (T @ v_prof), 3).tolist()}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return T, formas_prof, formas_prof_despues, v_prof


@app.cell
def _(mo, np):
    _l = np.array([2.0, 1.0])
    _A = np.array([[2.0, 1.0], [0.0, 1.0]])
    _P = np.array([[1.0, 1.0], [3.0, 1.0], [2.0, 3.0]])
    _lp = _l @ np.linalg.inv(_A)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        numpy no distingue fila de columna: un array `(2,)` es las dos cosas, y `l @ p` y `p @ l` dan el mismo número.
        **La diferencia la pongo yo con el lado de la matriz**: `A @ p` mueve un punto (columna, a la derecha de $A$);
        `l @ A` aplica la fila a la izquierda. La fila arrastrada es `l @ np.linalg.inv(A)` o, sin invertir,
        `np.linalg.solve(A.T, l)`, que resuelve $A^T x = \ell^T$, o sea $(\ell A^{-1})^T$. Con una nube $N\times2$
        (una fila por punto), `P @ l` lee la marca de cada punto de una vez: las curvas de nivel de toda la nube.
        """),
        mo.md("```python\nl = np.array([2., 1.]); A = np.array([[2., 1.], [0., 1.]])\nP = np.array([[1., 1.], [3., 1.], [2., 3.]])   # (3, 2): tres puntos\nl @ np.linalg.inv(A)       # ℓ A⁻¹\nnp.linalg.solve(A.T, l)    # lo mismo, sin invertir\nP @ l                      # (3,): la cota (menos 100) de cada punto\n(P @ A.T) @ (l @ np.linalg.inv(A))   # puntos movidos, leídos con la regla arrastrada\n```"),
        mo.md(f"`l @ inv(A)` = `{np.round(_lp, 3).tolist()}` · `solve(A.T, l)` = `{np.round(np.linalg.solve(_A.T, _l), 3).tolist()}` · `P @ l` = `{(_P @ _l).tolist()}` · "
              f"`(P @ A.T) @ lp` = `{np.round((_P @ _A.T) @ _lp, 3).tolist()}` · `(P @ l).shape` = `{(_P @ _l).shape}`"),
    ])
    return


@app.cell
def _(lib, mo, np):
    # ---------- aporte propio (CEIA): dos nubes separables y su SVM de margen duro, sin scikit-learn ----------
    nube_A = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [0.5, 0.5]])  # mojones de la parcela A
    nube_B = np.array([[4.0, 3.0], [6.0, 3.0], [4.0, 5.0], [5.0, 6.0]])  # mojones de la parcela B
    svm = lib.svm_margen_duro_2d(nube_A, nube_B)
    deformaciones = {
        "identidad": np.eye(2),
        "estirar x al doble: diag(2, 1)": np.diag([2.0, 1.0]),
        "cizalla [[1, 1], [0, 1]]": np.array([[1.0, 1.0], [0.0, 1.0]]),
    }
    deformacion = mo.ui.radio(options=list(deformaciones), value="identidad", label="deformación A del plano")
    mo.vstack([
        mo.md(r"""
        ### 4b. Conexión con IA (aporte desde la CEIA): una SVM es una forma lineal con margen

        Esto **no es contenido de la cátedra**: lo traigo de la especialización en IA, porque es la misma regla
        graduada de esta lección con otro nombre. Dos parcelas vecinas, cada una con sus mojones relevados, y la
        pregunta de una *máquina de vectores de soporte* (SVM): ¿cuál es la **calle más ancha** que pasa entre las dos
        nubes? La respuesta es una forma lineal afín, $w^T x + b$: la marca $0$ es la divisoria, las marcas $-1$ y $+1$
        son los bordes de la calle y **apoyan contra los mojones más cercanos**, los *puntos de soporte*. El ancho de la
        calle es $2/\lVert w\rVert$, dos separaciones entre marcas (sección 1), y la SVM elige la regla que lo hace
        máximo. En homogéneas $(x, y, 1)$ toda la SVM es **una sola forma lineal** $(w_1, w_2, b)$: la divisoria es su
        marca cero, como la recta $\ell\,\tilde p = 0$ de la sección 1.

        La dualidad se aplica tal cual. Si deformo el plano con $A$, los mojones van a $Ax$ y la regla se arrastra con
        $A^{-1}$: $(w^T A^{-1},\ b)$ sigue leyendo $-1$, $0$, $+1$ sobre los mismos puntos. Lo que **sí** cambia es el
        ancho físico $2/\lVert w A^{-1}\rVert$, porque el largo de $w$ lo da el producto interno, no la regla. Por eso,
        si vuelvo a entrenar la SVM sobre los puntos deformados, elige **otra** divisoria (punteada, en negro): la calle
        más ancha medida con el producto interno de la grilla nueva. Reescalar los datos antes de entrenar no es un
        detalle de implementación: cambia el producto interno, y con él qué cuenta como margen. El helper
        `lib.svm_margen_duro_2d` es numpy puro: prueba los pares y tríos de soporte posibles y se queda con la franja
        factible más ancha.
        """),
        deformacion,
    ])
    return deformacion, deformaciones, nube_A, nube_B, svm


@app.cell
def _(deformacion, deformaciones, go, lib, mo, np, nube_A, nube_B, svm):
    A_svm = deformaciones[deformacion.value]
    w_svm, b_svm = svm["w"], svm["b"]
    w_def = lib.forma_transformada(w_svm, A_svm)  # la regla arrastrada: (w A⁻¹, b)
    nube_A_def, nube_B_def = lib.transformar(nube_A, A_svm), lib.transformar(nube_B, A_svm)
    svm_def = lib.svm_margen_duro_2d(nube_A_def, nube_B_def)  # re-entrenada sobre los puntos deformados
    _todo = np.vstack([nube_A, nube_B, nube_A_def, nube_B_def])
    rango_svm = (float(_todo.min()) - 2.0, float(_todo.max()) + 2.0)

    def _regla(f, ww, bb, color, nombre, ancho=1.3, etiquetas=True, dash=None):
        """Las marcas −1, 0, +1 de la regla w·x + b: los cortes de w·x = k − b con la caja; la marca 0 más gruesa."""
        for k in (-1, 0, 1):
            P = lib.cortes_caja(ww, k - bb, rango_svm)
            if len(P) < 2:
                continue
            f.add_trace(go.Scatter(x=P[:, 0], y=P[:, 1], mode="lines+text" if etiquetas else "lines",
                                   text=["", f"{k:+d}" if k else "0"], textposition="top left",
                                   textfont=dict(size=11, color=color), hoverinfo="skip",
                                   line=dict(color=color, width=2.5 * ancho if k == 0 else ancho, dash=dash),
                                   name=nombre, legendgroup=nombre, showlegend=(k == -1)))

    figura_svm = lib.figura_plano(rango_svm, f"{deformacion.value} · las marcas siguen apoyando en los mismos mojones", alto=560)
    lib.capa_antes(figura_svm, rango_svm, cuadrado=False)
    _regla(figura_svm, w_svm, b_svm, lib.GRIS_ANTES, "regla antes: (w, b)", etiquetas=False)
    for _N, _nombre in ((nube_A, "parcela A antes"), (nube_B, "parcela B antes")):
        figura_svm.add_trace(go.Scatter(x=_N[:, 0], y=_N[:, 1], mode="markers", name=_nombre, hoverinfo="skip",
                                        marker=dict(size=7, color="white", line=dict(color=lib.GRIS_ANTES, width=1.5))))
    _regla(figura_svm, w_def, b_svm, lib.TEAL_DESPUES, "regla arrastrada: (w A⁻¹, b)")
    _regla(figura_svm, svm_def["w"], svm_def["b"], "#222", "SVM re-entrenada sobre A·x", ancho=1.0, etiquetas=False, dash="dot")
    for _N, _color, _nombre in ((nube_A_def, lib.VIOLETA_OBJETO, "parcela A después"), (nube_B_def, lib.COLORES[1], "parcela B después")):
        figura_svm.add_trace(go.Scatter(x=_N[:, 0], y=_N[:, 1], mode="markers", marker=dict(size=10, color=_color), name=_nombre))
    _S = lib.transformar(np.vstack([svm["soporte_1"], svm["soporte_2"]]), A_svm)
    figura_svm.add_trace(go.Scatter(x=_S[:, 0], y=_S[:, 1], mode="markers", name="puntos de soporte",
                                    marker=dict(size=17, color="rgba(0,0,0,0)", line=dict(color="#222", width=2))))

    _lee_A, _lee_B = nube_A_def @ w_def + b_svm, nube_B_def @ w_def + b_svm
    _mismo = bool(np.allclose(_lee_A, nube_A @ w_svm + b_svm) and np.allclose(_lee_B, nube_B @ w_svm + b_svm))
    _nota = ("coincide con la arrastrada: con la identidad no hay nada que re-entrenar" if np.allclose(A_svm, np.eye(2))
             else "otra divisoria: el margen se mide con el producto interno de la grilla nueva")
    _panel = mo.md(rf"""
    **Números vivos**

    - SVM sobre los mojones originales: $w = {lib.pmat(w_svm.reshape(1, 2))}$, $b = {lib.num_tex(b_svm)}$; en homogéneas, la
      forma $(w_1, w_2, b) = {lib.pmat(np.append(w_svm, b_svm).reshape(1, 3))}$. Ancho de la calle $2/\lVert w\rVert =
      {lib.num_tex(svm["margen"])}$; puntos de soporte: {len(svm["soporte_1"])} de A y {len(svm["soporte_2"])} de B.
    - $A = {lib.matriz_coloreada(A_svm)}$; regla arrastrada $w A^{{-1}} = {lib.pmat(w_def.reshape(1, 2))}$, mismo $b$.
      Lecturas sobre $Ax$: parcela A `{np.round(_lee_A, 3).tolist()}`, parcela B `{np.round(_lee_B, 3).tolist()}`;
      iguales a las de antes → `np.allclose`: `{_mismo}`.
    - Ancho físico de la regla arrastrada: $2/\lVert w A^{{-1}}\rVert = {lib.num_tex(2 / np.linalg.norm(w_def))}$. SVM
      re-entrenada sobre $Ax$: $w'' = {lib.pmat(svm_def["w"].reshape(1, 2))}$, $b'' = {lib.num_tex(svm_def["b"])}$, ancho
      ${lib.num_tex(svm_def["margen"])}$ ({_nota}).
    """)
    mo.vstack([mo.ui.plotly(figura_svm), _panel])
    return A_svm, svm_def, w_def


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("las más básicas de esas funciones son las selectoras de coordenadas").* La regla
        $\ell = (3, 4)$. ¿Qué dirección no mide (su núcleo)? ¿A qué distancia están sus marcas enteras? ¿Qué marca pasa
        por $(2, 1)$, y cuál es su ecuación? Escribí $\ell$ como combinación de $\mathsf x$ y $\mathsf y$.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        No mide la dirección $(4, -3)$: $12 - 12 = 0$ (toda la recta $3x + 4y = 0$). $\lvert\ell\rvert = 5$: marcas cada
        $1/5 = 0.2$. $\ell(2, 1) = 6 + 4 = 10$: la recta $3x + 4y = 10$. Y $\ell = 3\,\mathsf x + 4\,\mathsf y$.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("una forma lineal se transforma del lado contrario que un vector").* El ejemplo del
        apunte: $A = \begin{pmatrix} 1 & 1 \\ 0 & 2 \end{pmatrix}$, $\varphi = (2, 3)$, $v = (1, 1)$. Calculá $Av$,
        $\varphi(Av)$, $\varphi A$ y $\varphi A^{-1}$. ¿Cuál de las dos filas lee sobre $v$ lo que $\varphi$ lee sobre
        $Av$, y cuál es la regla arrastrada junto con la figura? Verificá cada una con una lectura.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $Av = (2, 2)$, $\varphi(Av) = 10$. $\varphi A = (2, 8)$ y $(2, 8)\cdot(1, 1) = 10$: lee sobre el $v$ **original**
        lo que $\varphi$ lee sobre $Av$ ($\varphi(Av) = (\varphi A)(v)$). $A^{-1} = \begin{pmatrix} 1 & -\tfrac12 \\ 0 & \tfrac12 \end{pmatrix}$
        y $\varphi A^{-1} = (2, \tfrac12)$: la regla **arrastrada**, que sobre $Av = (2, 2)$ lee $4 + 1 = 5 = \varphi(v)$.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def forma_transformada(l, A):\n    # l: la fila (array de 2); A: la matriz que mueve los puntos (p' = A p)\n    return ...   # la fila que sobre A p lee lo mismo que l sobre p\n",
        language="python", min_height=110, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("¿cómo transformo las rectas para que los puntos sigan estando en las mismas
        rectas?").* Completá `forma_transformada(l, A)`. Tenés `np`. Se verifica con `np.allclose` sobre la $A$ de la
        predicción y diez matrices al azar con $\det \ne 0$.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _casos = [(np.array([2.0, 1.0]), np.array([[2.0, 1.0], [0.0, 1.0]]))]
    while len(_casos) < 11:
        _M = _rng.uniform(-3, 3, (2, 2))
        if abs(np.linalg.det(_M)) > 0.5:
            _casos.append((_rng.uniform(-3, 3, 2), _M))
    _esperado = np.array([lib.forma_transformada(l, A) for l, A in _casos])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.array([np.asarray(_ns["forma_transformada"](l.copy(), A.copy()), dtype=float).reshape(-1) for l, A in _casos])
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ devolvés algo de forma `{_obtenido.shape[1:]}`; tiene que ser una fila `(2,)`."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los 11 casos: la fila por $A^{-1}$ **a la derecha**, y cada lectura se conserva."), kind="success")
        elif np.allclose(_obtenido, [A @ l for l, A in _casos]):
            _res = mo.callout(mo.md(r"❌ `A @ l`: moviste la fila como si fuera un punto. Una fila va con la **inversa** y a la **derecha**: `l @ np.linalg.inv(A)`."), kind="warn")
        elif np.allclose(_obtenido, [l @ A for l, A in _casos]):
            _res = mo.callout(mo.md(r"❌ `l @ A` (o `A.T @ l`, el mismo número): el lado es correcto pero falta invertir. Esa regla lee sobre el $p$ original lo que $\ell$ lee sobre $Ap$ (ejercicio b); para arrastrarla: `l @ np.linalg.inv(A)`."), kind="warn")
        elif np.allclose(_obtenido, [np.linalg.inv(A) @ l for l, A in _casos]):
            _res = mo.callout(mo.md(r"❌ `inv(A) @ l`: la inversa está, pero del lado de la columna: eso es $\ell A^{-T}$. La fila va a la derecha: `l @ np.linalg.inv(A)` o `solve(A.T, l)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para `l = {_casos[0][0].tolist()}` y `A = {_casos[0][1].tolist()}` esperaba `{np.round(_esperado[0], 3).tolist()}` y obtuve `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def recta_por_dos_puntos(p, q):\n    # p, q: puntos del plano (arrays de 2)\n    pt = ...   # p en homogéneas: (x, y, 1)\n    qt = ...\n    return ...   # la fila (a, b, c) con a x + b y + c = 0, vía producto vectorial\n",
        language="python", min_height=140, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("las rectas se representan por vectores fila y los puntos por vectores
        columna").* Completá `recta_por_dos_puntos(p, q)`: la recta por $p$ y $q$ como **fila homogénea** $(a, b, c)$,
        con $ax + by + c = 0$. La cuña de las dos ternas homogéneas (`np.cross`) da una fila que marca cero sobre las
        dos. Tenés `np`. Se verifica que la fila lea $0$ en $p$ y en $q$ en diez pares al azar; signo y escala no
        importan: es la misma recta.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(2026)
    _pares = [(np.array([1.0, 1.0]), np.array([3.0, 2.0]))] + [(_rng.uniform(-5, 5, 2), _rng.uniform(-5, 5, 2)) for _ in range(9)]
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _obt = [np.asarray(_ns["recta_por_dos_puntos"](p.copy(), q.copy()), dtype=float).reshape(-1) for p, q in _pares]
        _tam = {o.size for o in _obt}
        if _tam == {1}:
            _res = mo.callout(mo.md(r"❌ devolvés **un número**: la cuña de $p$ y $q$ en el plano (un área), no una recta. Faltó homogeneizar: agregá el $1$ a cada punto y recién ahí `np.cross`."), kind="warn")
        elif _tam != {3}:
            _res = mo.callout(mo.md(f"❌ devolvés algo de tamaño `{sorted(_tam)}`; la fila homogénea tiene tres números $(a, b, c)$."), kind="danger")
        else:
            _lee = np.array([[o @ lib.hom(p), o @ lib.hom(q)] for o, (p, q) in zip(_obt, _pares)])
            if all(np.linalg.norm(o) > 1e-9 for o in _obt) and np.allclose(_lee, 0.0, atol=1e-6):
                _nota = " Devolvés $q \\times p$: signo cambiado, misma recta (la cuña es antisimétrica)." if np.allclose(_obt[0], -lib.recta_por_dos_puntos(*_pares[0])) else ""
                _res = mo.callout(mo.md(f"✅ la fila marca $0$ en $p$ y en $q$ en los 10 pares: por $(1, 1)$ y $(3, 2)$ da `{np.round(_obt[0], 3).tolist()}`, la recta $-x + 2y - 1 = 0$.{_nota}"), kind="success")
            elif np.allclose(_obt, [lib.hom(p) - lib.hom(q) for p, q in _pares]) or np.allclose(_obt, [lib.hom(q) - lib.hom(p) for p, q in _pares]):
                _res = mo.callout(mo.md(r"❌ restaste las ternas: eso es la **dirección** de la recta (un punto impropio), no la fila. La recta por dos puntos es su cuña: `np.cross(pt, qt)`."), kind="warn")
            else:
                _res = mo.callout(mo.md(f"❌ la fila no pasa por los puntos: en $(1, 1)$ y $(3, 2)$ lee `{np.round(_lee[0], 3).tolist()}` en vez de `[0, 0]`. ¿Homogeneizaste con un $1$ y usaste `np.cross` sobre las ternas?"), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré que una forma lineal es una regla, que sus marcas son rectas paralelas y que se transforma con $A^{-1}$
    para que la lectura no cambie. Las demostraciones:

    - [apunte, sección 11: "Formas lineales: la recta como máquina de medir" (selectoras y dual, pila de formas,
      $\varphi A$ y $\varphi A^{-1}$, el gradiente como forma, caja "Dualidad en pocas palabras")](../../apunte.pdf#nameddest=cap:11)
    - [apunte, sección 5: tabla "la misma idea en cada dimensión", la recta como forma $n\cdot x = c$](../../apunte.pdf#nameddest=cap:05)
    - [ficha de la clase 4](../../clases/04.html) · [el camino](../../index.html) ·
      [Producto interno](../02_producto_interno/index.html) · [Cambio de base](../08_cambio_de_base/index.html)

    **Lo que viene:** [la cuña y el determinante](../07a_cuna_determinante/index.html), el detector de colinealidad,
    que acá ya apareció como la recta por dos puntos ($\tilde p \times \tilde q$). Y en
    [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html), el gradiente en un punto es exactamente
    esto: una forma lineal cuya marca cero es la tangente a la curva de nivel.
    """)
    return


@app.cell
def _(A, A_pred, A_svm, B_08, T, candidatos, fila, fila_despues, formas_prof, formas_prof_despues, lib, mo, mojon, mojon_despues, np, nube_A, nube_B, p_pred, svm, svm_def, v_prof, w_def):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _R, _D, _pp, _ft, _ok = lib.rot2(np.deg2rad(30)), np.diag([2.0, 1.0]), A_pred @ p_pred, lib.forma_transformada, lib.exacto
    _Ab = [[1, 1], [0, 2]]
    _checks = [
        ("predicción: cuatro candidatos distintos; ℓ A⁻¹ = (1, 0) lee 3 sobre A p = (3, 1); los errores leen 16, 15 y 7",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4 and _ok(candidatos["correcta"], [1, 0]) and _ok(_pp, [3, 1])
         and _ok([candidatos[k] @ _pp for k in ("correcta", "como-punto", "hacia-atras", "mismas")], [3, 16, 15, 7]) and _ok(candidatos["hacia-atras"] @ p_pred, fila @ _pp)),
        ("con un giro de 90° la fila va a (−1, 2) de las dos maneras", _ok(_ft(fila, lib.rot2(np.pi / 2)), [-1, 2]) and _ok(lib.rot2(np.pi / 2) @ fila, [-1, 2])),
        ("sección 2: la lectura del mojón se conserva; con una rotación la flecha sigue perpendicular, con diag(2, 1) no; en la base de 08 la fila es (7, 4)",
         _ok(fila_despues @ mojon_despues, fila @ mojon) and _ok(mojon_despues, A @ mojon) and _ok(lib.angulo(_R @ fila, lib.perp2(_ft(fila, _R))), np.pi / 2)
         and not _ok(lib.angulo(_D @ fila, lib.perp2(_ft(fila, _D))), np.pi / 2, tol=1e-3) and _ok(_ft(fila, np.linalg.inv(B_08)), [7, 4])),
        ("3.1: (2, 1) diag(2, 1)⁻¹ = (1, 1); 3.2: det T = 1.61, T v = (5.6, 4.9), formas (1.4, 0.7)/1.61 y (−1.1, 2.9)/1.61, lecturas 7 y 5",
         _ok(_ft([2, 1], _D), [1, 1]) and _ok(np.linalg.det(T), 1.61) and _ok(T @ v_prof, [5.6, 4.9]) and _ok(formas_prof @ v_prof, [7, 5])
         and _ok(formas_prof_despues @ (T @ v_prof), [7, 5]) and _ok(formas_prof_despues, np.array([[1.4, 0.7], [-1.1, 2.9]]) / 1.61)),
        ("ejercicios: (3, 4) ⊥ (4, −3), marcas cada 0.2, ℓ(2, 1) = 10; φA = (2, 8), φA⁻¹ = (2, 1/2) lee 5; la recta por (1, 1) y (3, 2) es −x + 2y − 1 = 0",
         _ok(np.array([3, 4]) @ [4, -3], 0.0) and _ok(1 / np.linalg.norm([3, 4]), 0.2) and _ok(np.array([3, 4]) @ [2, 1], 10) and _ok(np.array([2, 3]) @ _Ab, [2, 8])
         and _ok(_ft([2, 3], _Ab), [2, 0.5]) and _ok(_ft([2, 3], _Ab) @ [2, 2], 5) and _ok(lib.recta_por_dos_puntos([1, 1], [3, 2]), [-1, 2, -1])),
        ("4b (aporte CEIA): SVM de las dos parcelas w = (0.4, 0.4), b = −1.8, ancho 5/√2, soportes (2,0), (0,2), (4,3); la regla arrastrada lee lo mismo sobre A x; "
         "con diag(2, 1) el ancho físico pasa a √20 y la SVM re-entrenada da ancho 5; la re-entrenada nunca es más angosta que la arrastrada",
         _ok(svm["w"], [0.4, 0.4]) and _ok(svm["b"], -1.8) and _ok(svm["margen"], 5 / np.sqrt(2)) and _ok(svm["soporte_1"], [[2, 0], [0, 2]]) and _ok(svm["soporte_2"], [[4, 3]])
         and _ok(lib.transformar(nube_A, A_svm) @ w_def + svm["b"], nube_A @ svm["w"] + svm["b"]) and _ok(w_def, _ft(svm["w"], A_svm))
         and _ok(2 / np.linalg.norm(_ft(svm["w"], _D)), np.sqrt(20)) and _ok(lib.svm_margen_duro_2d(lib.transformar(nube_A, _D), lib.transformar(nube_B, _D))["margen"], 5.0)
         and svm_def["margen"] >= 2 / np.linalg.norm(w_def) - 1e-9),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
