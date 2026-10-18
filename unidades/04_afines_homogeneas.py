# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Afinidades y coordenadas homogéneas (lección 04, molde v2 sobre cb104). Clase 3.

Una sola idea: la matriz es lo que le pasa a la grilla (cada columna, a dónde va un eje; paralelogramos; área × det).
La traslación no entra en una 2×2: tercera coordenada, 3×3. Tres puntos conocidos determinan la afinidad.

Chequear:  uv run marimo check --select MW unidades/04_afines_homogeneas.py
Exportar:  uv run python tools/build.py --only 04_afines_homogeneas
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
    # Afinidades y coordenadas homogéneas

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Seguimos la clase 3. La pregunta: **¿Cómo metemos la traslación adentro de la matriz para componer rotar, escalar y mover
    con una sola cuenta?** El gancho: *un plano escaneado que quedó estirado distinto en cada eje: las paralelas siguen
    paralelas y tres puntos conocidos alcanzan para corregirlo.*

    Colores, iguales en la figura y en el álgebra: **primera columna** <span style="color:#1b6f6a">**teal**</span>,
    **segunda** <span style="color:#b5451b">**rust**</span>, **tercera** <span style="color:#c9a227">**gold**</span>.
    Cada columna es a dónde va un vector de la base (la tercera, a dónde va el origen). La parcela va en
    <span style="color:#7a4e9e">**violeta**</span>, lo de antes en gris, lo de después en teal.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("04_afines_homogeneas"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    A_esc = np.array([[1.5, 0.5], [0.0, 1.25]])  # el escaneo: estira 1.5 en x, 1.25 en y, e inclina el eje y
    t_esc = np.array([1.0, 1.0])
    mojones = np.array([[1.0, 1.0], [1.0, 5.0], [1.0, 3.0]])  # lado oeste: dos esquinas y el mojón intermedio
    mojones_esc = lib.transformar_afin(mojones, A_esc, t_esc)
    _m1, _m2 = mojones_esc[0], mojones_esc[1]
    candidatos = {
        "correcta": mojones_esc[2],
        "rotacion": _m1 + 2.0 * (_m2 - _m1) / np.linalg.norm(_m2 - _m1),  # conserva los 2 m: como si fuera un giro
        "traslacion": _m1 + (mojones[2] - mojones[0]),  # corre el mojón sin estirar ni inclinar
        "mismas": mojones[2].copy(),
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({lib.vec_plano(candidatos[k]): k for k in ("rotacion", "mismas", "correcta", "traslacion")}),
        value=None,
        label=r"**Predicción.** En el escaneo las esquinas aparecen en $(3,\ 2.25)$ y $(5,\ 7.25)$. El mojón intermedio aparece en…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Escaneamos un plano viejo de una parcela y la hoja pasó torcida por el rodillo: quedó **estirada distinto en cada
        eje y un poco inclinada**. Lo sabemos porque las cuadrículas del plano, que eran cuadrados, en la imagen son
        paralelogramos iguales. Nada se curvó ni se cruzó.

        Sobre el lado oeste hay tres mojones: las esquinas, en el terreno $(1, 1)$ y $(1, 5)$, y uno intermedio a mitad
        del lado, $(1, 3)$ (metros). En la imagen medimos dónde cayeron las esquinas. ¿Dónde tiene que aparecer el intermedio?
        """),
        prediccion,
    ])
    return A_esc, candidatos, mojones, mojones_esc, prediccion, t_esc


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** $(4, 4.75)$ es el **punto medio** de las esquinas escaneadas. Una afinidad estira, inclina y corre, "
                     r"pero conserva las **razones sobre cada recta**: lo que estaba a mitad de camino sigue a mitad de camino, "
                     r"sin conocer la deformación. En la sección 3 la calculamos igual, a partir de tres puntos."),
        "rotacion": ("warn",
                     r"**No.** Dejaste el mojón a $2$ unidades de la esquina, como si el escaneo fuera un **giro** que conserva "
                     r"distancias. Pero el lado de $4$ m aparece con largo $\sqrt{29} \approx 5.39$: se estiró. Una afinidad no "
                     r"conserva longitudes; conserva **proporciones** sobre la recta."),
        "traslacion": ("warn",
                       r"**No.** $(3, 4.25)$ es la esquina escaneada más el desplazamiento del terreno $(0, 2)$, como si el escaneo "
                       r"sólo **corriera** la hoja. Ese punto ni está sobre el segmento entre las esquinas escaneadas, y una afinidad "
                       r"lleva rectas a rectas: el intermedio tiene que caer sobre ese segmento."),
        "mismas": ("warn",
                   r"**No.** $(1, 3)$ son las coordenadas en el **terreno**. El mojón no se movió, pero preguntamos dónde aparece en la "
                   r"**imagen**, donde las esquinas ya no están en $(1,1)$ y $(1,5)$: cambió la hoja, no la parcela."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** Una afinidad lleva **rectas a rectas, paralelas a paralelas** y conserva las **razones sobre
    cada recta**. No conserva longitudes ni ángulos: un cuadrado va a un paralelogramo cualquiera, un círculo a una
    elipse. El área se multiplica siempre por el mismo número, $\det A$; si $\det A < 0$ la figura además **se da
    vuelta** (ahí vive la reflexión).

    **La matriz es lo que le pasa a la grilla.** Alcanza con saber a dónde van $e_1$ y $e_2$: esas imágenes, como
    columnas, son $A$, y la grilla cuadrada se vuelve la grilla de paralelogramos que generan. Un punto
    $x\,e_1 + y\,e_2$ va a $x\,Ae_1 + y\,Ae_2$.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $x \mapsto ax + b$ | estirar la recta por $a$ (da vuelta si $a<0$) y correrla $b$ |
    | $\mathbb R^2$ | $x \mapsto Ax + t$, columnas $\textcolor{#1b6f6a}{Ae_1}$, $\textcolor{#b5451b}{Ae_2}$ | grilla de paralelogramos corrida $t$; área $\times \det A$ |
    | $\mathbb R^3$ | $x \mapsto Ax + t$, tres columnas | grilla de paralelepípedos; volumen $\times \det A$ |

    **Lo que la $2\times2$ no puede hacer: mover el origen.** $A\,0 = 0$ siempre; la traslación queda afuera y componer
    obliga a arrastrar los $t$ a mano. La salida: $(x, y)$ pasa a ser $(x, y, 1)$ y la afinidad, una $3\times3$ cuya
    **tercera columna** es a dónde va el origen:

    $$\begin{pmatrix} x' \\ y' \\ 1 \end{pmatrix} = \begin{pmatrix} \textcolor{#1b6f6a}{a} & \textcolor{#b5451b}{b} & \textcolor{#c9a227}{e} \\ \textcolor{#1b6f6a}{c} & \textcolor{#b5451b}{d} & \textcolor{#c9a227}{f} \\ 0 & 0 & 1 \end{pmatrix}\begin{pmatrix} x \\ y \\ 1 \end{pmatrix}.$$

    Componer vuelve a ser multiplicar. Esto es una **muestra**; la demostración de que $Ax + t$ conserva paralelas
    está en el apunte, sección 10.
    """)
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (tipo, deslizador (min, max, paso, valor, etiqueta) o matriz, qué pasa) ----------
    casos = {
        "identidad": ("fijo", None, r"no cambia nada: $\det = 1$."),
        "escala anisótropa diag(1.5, s)": ("escala", (0.2, 2.0, 0.1, 0.6, "s (factor en y)"),
                                           r"estira distinto en cada eje: paralelas y razones sí, ángulos no; $\det = 1.5\,s$."),
        "corte [[1, s], [0, 1]]": ("corte", (-1.5, 1.5, 0.1, 0.6, "s (corte)"),
                                   r"inclina el eje $y$ y deja fijo el eje $x$; $\det = 1$: **conserva el área**, no los ángulos."),
        "reflexión diag(1, −1)": ("fijo", np.diag([1.0, -1.0]), r"espejo: conserva longitudes pero **da vuelta la orientación**, $\det = -1$."),
        "rotación + escala 0.8·R(θ)": ("rotescala", (-180, 180, 1, 30, "θ (°)"),
                                       r"similaridad: gira y achica; conserva ángulos y razones de distancias; $\det = 0.64$."),
        "afinidad axial: eje x, dirección (1, 1), factor s": ("axial", (-2.0, 3.0, 0.1, 2.0, "s (factor)"),
                                                               r"el eje $x$ queda fijo y cada punto se desliza por su paralela a $(1, 1)$, $s$ veces más lejos; $\det = s$."),
        "general (a, b, c, d)": ("general", None, r"cualquier $2\times2$: las columnas son los lados del paralelogramo unitario."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="escala anisótropa diag(1.5, s)", label="caso precargado")
    rango = 6
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # la misma de Rotaciones II
    mo.md(r"""
    ## 2. Manipulación

    Tres capas: **gris**, grilla y cuadrado unitario antes; **teal**, los mismos después, con las columnas de $A$ como
    flechas; **violeta**, la parcela con estelas. La grilla sigue siendo de **paralelogramos iguales** en todos los
    casos, y el área de la parcela se multiplica por $\det A$. Con un caso precargado manda un deslizador; en
    *general* mandan los cuatro números. **Reproducir** muestra el camino desde la identidad. A la derecha de la
    figura, el panel con el caso, los deslizadores y los números vivos.
    """)
    return caso, casos, parcela, rango


@app.cell
def _(caso, casos, mo):
    _tipo, _spec, _ = casos[caso.value]
    if isinstance(_spec, tuple):
        _lo, _hi, _paso, _val, _etq = _spec
        param = mo.ui.slider(_lo, _hi, value=_val, step=_paso, label=_etq, show_value=True)
    else:
        param = mo.ui.slider(0, 1, value=0, step=1, label="(sin parámetro)", disabled=True)
    abcd = mo.ui.array([mo.ui.slider(-2, 2, value=v, step=0.1, label=f"{n} =", show_value=True)
                        for n, v in zip("abcd", (1.2, 0.5, -0.3, 0.9))])
    return abcd, param


@app.cell
def _(abcd, caso, casos, go, lib, mo, np, param, parcela, rango):
    _tipo, _spec, que_pasa = casos[caso.value]
    _s = param.value
    if _tipo == "escala":
        M = np.diag([1.5, _s])
    elif _tipo == "corte":
        M = np.array([[1.0, _s], [0.0, 1.0]])
    elif _tipo == "rotescala":
        M = 0.8 * lib.rot2(np.deg2rad(_s))
    elif _tipo == "axial":
        _B = np.array([[1.0, 1.0], [0.0, 1.0]])  # columnas: u = (1, 0) sobre el eje, d = (1, 1) la dirección
        M = _B @ np.diag([1.0, _s]) @ np.linalg.inv(_B)
    elif _tipo == "general":
        _a, _b, _c, _d = (float(v) for v in abcd.value)
        M = np.array([[_a, _b], [_c, _d]])
    else:
        M = np.eye(2) if _spec is None else np.asarray(_spec, dtype=float)
    if _tipo == "rotescala":
        camino = [(1 - 0.2 * u) * lib.rot2(u * np.deg2rad(_s)) for u in np.linspace(0, 1, 36)]
    else:
        camino = [np.eye(2) + u * (M - np.eye(2)) for u in np.linspace(0, 1, 36)]

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

    area_antes = lib.area_poligono(parcela)
    area_despues = lib.area_poligono(lib.transformar(parcela, M))
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, param, abcd if _tipo == "general" else mo.md(""),
        mo.md(rf"""
        **Números vivos**

        - $\det A = \mathbf{{{lib.num_tex(np.linalg.det(M), 3)}}}$
        - área con signo de la parcela: antes ${lib.num_tex(area_antes, 2)}$, después $\mathbf{{{lib.num_tex(area_despues, 3)}}}$
          (cociente ${lib.num_tex(area_despues / area_antes, 3)}$)
        - el origen va a ${lib.vec_tex(M @ [0, 0])}$: una $2\times2$ **nunca lo mueve**

        $$A = {lib.matriz_coloreada(M)}$$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, area_antes, area_despues


@app.cell
def _(mo):
    giro = mo.ui.slider(-180, 180, value=30, step=1, label="θ (°)", show_value=True)
    escala = mo.ui.slider(0.4, 2.0, value=1.2, step=0.1, label="k (escala)", show_value=True)
    tx = mo.ui.slider(-3, 3, value=2.0, step=0.5, label="tₓ", show_value=True)
    ty = mo.ui.slider(-3, 3, value=1.0, step=0.5, label="tᵧ", show_value=True)
    orden = mo.ui.radio(options=["girar, escalar y después mover", "mover y después girar y escalar"],
                        value="girar, escalar y después mover", label="orden de composición")
    mo.md(r"""
    **La traslación entra por la tercera columna.** Tres matrices $3\times3$: $R$ gira, $S$ escala, $T$ mueve.
    Componemos multiplicando (la de la derecha actúa primero) y leemos en $H$ la parte lineal $A$ (teal y rust) y a
    dónde fue el origen (gold). Cambiá el orden (en el panel de la derecha): $A$ es la misma, $t$ no, porque mover
    antes de girar gira también el corrimiento.
    """)
    return escala, giro, orden, tx, ty


@app.cell
def _(escala, giro, lib, mo, np, orden, parcela, rango, tx, ty):
    _R = lib.matriz_afin(lib.rot2(np.deg2rad(giro.value)), [0, 0])
    _S = lib.matriz_afin(escala.value * np.eye(2), [0, 0])
    _T = lib.matriz_afin(np.eye(2), [tx.value, ty.value])
    primero_mover = orden.value.startswith("mover")
    H = (_S @ _R @ _T) if primero_mover else (_T @ _S @ _R)
    A_h, t_h = lib.partes_afin(H)
    _nombre = "SRT" if primero_mover else "TSR"
    fig_t = lib.figura_plano(rango + 1, f"H = {_nombre}: la grilla se deforma y se corre")
    lib.capa_antes(fig_t, rango)
    lib.capa_despues_afin(fig_t, A_h, t_h, rango)
    lib.objeto(fig_t, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    lib.objeto(fig_t, lib.dehom(lib.hom(parcela) @ H.T), lib.VIOLETA_OBJETO, "parcela después")
    lib.punto(fig_t, t_h, lib.COLORES[2], "imagen del origen", texto="F(0)")
    _panel = mo.vstack([
        mo.md("**Controles**"), orden, giro, escala, tx, ty,
        mo.md(rf"""
        **Números vivos**

        $$H = {_nombre[0]}\,{_nombre[1]}\,{_nombre[2]} = {lib.matriz_coloreada(H)}$$

        - $A\,(0,0) = (0, 0)$ con la $2\times2$; con la $3\times3$, $H\,(0, 0, 1)^T = {lib.vec_tex(H @ lib.hom([0, 0]))}$: el origen **sí** se mueve.
        - $\det A = {lib.num_tex(np.linalg.det(A_h), 3)}$ ($= k^2$); $t = {lib.vec_tex(t_h)}$.
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(fig_t), _panel)
    return A_h, H, t_h


@app.cell
def _(A_esc, lib, mo, np, t_esc):
    _p = np.array([4.0, 2.0])
    _H = lib.matriz_afin(A_esc, t_esc)
    _qh = _H @ lib.hom(_p)
    P3 = np.array([[1.0, 1.0], [3.0, 1.0], [1.0, 2.0]])
    Q3 = np.array([[2.0, 2.0], [4.0, 2.0], [3.0, 3.0]])
    A3, t3 = lib.afin_por_tres_puntos(P3, Q3)
    _M = np.linalg.solve(lib.hom(P3), Q3).T
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy. Primero con la matriz del escaneo de la sección 0.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La $2\times2$ como combinación de columnas.** Con $p = (4, 2)$:

            $$Ap = \begin{pmatrix} \textcolor{#1b6f6a}{1.5} & \textcolor{#b5451b}{0.5} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1.25} \end{pmatrix}\begin{pmatrix} 4 \\ 2 \end{pmatrix}
            = 4\,\textcolor{#1b6f6a}{\binom{1.5}{0}} + 2\,\textcolor{#b5451b}{\binom{0.5}{1.25}} = \begin{pmatrix} 7 \\ 2.5 \end{pmatrix}.$$

            Cuatro veces la flecha teal más dos veces la rust: el punto conserva sus **coordenadas** en la grilla nueva.

            **3.2 La $3\times3$ sobre el punto homogéneo** $(4, 2, 1)$: el $1$ "enciende" la columna gold:

            $$H\begin{pmatrix} 4 \\ 2 \\ 1 \end{pmatrix} = 4\,\textcolor{#1b6f6a}{\binom{1.5}{0}_{\!0}} + 2\,\textcolor{#b5451b}{\binom{0.5}{1.25}_{\!0}} + 1\,\textcolor{#c9a227}{\binom{1}{1}_{\!1}} = \begin{pmatrix} 8 \\ 3.5 \\ 1 \end{pmatrix} = \binom{Ap + t}{1}.$$

            La última fila $(0\ 0\ 1)$ garantiza que el $1$ sigue siendo $1$.
            """),
            mo.vstack([
                mo.md("```python\nA = np.array([[1.5, 0.5], [0.0, 1.25]])\nt = np.array([1.0, 1.0])\np = np.array([4.0, 2.0])\nA @ p\nH = lib.matriz_afin(A, t)      # [[A, t], [0, 0, 1]]\nH @ lib.hom(p)                 # hom(p) = (4, 2, 1)\nnp.allclose(lib.dehom(H @ lib.hom(p)), A @ p + t)\n```"),
                mo.md(f"`A @ p` = `{np.round(A_esc @ _p, 3).tolist()}`  \n`H` =\n```\n{np.round(_H, 3)}\n```\n`H @ lib.hom(p)` = `{np.round(_qh, 3).tolist()}` · "
                      f"`{bool(np.allclose(lib.dehom(_qh), A_esc @ _p + t_esc))}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 Tres puntos determinan la afinidad.** $a = (1,1)$, $b = (3,1)$, $c = (1,2)$ van a $a' = (2,2)$,
            $b' = (4,2)$, $c' = (3,3)$ (apunte, apéndice 17). Seis incógnitas, seis ecuaciones: cada par da
            $x' = ax + by + e$, $y' = cx + dy + f$. A mano, restando, $A(b - a) = b' - a'$ y $A(c - a) = c' - a'$:
            $A\binom{2}{0} = \binom{2}{0}$, $A\binom{0}{1} = \binom{1}{1}$, luego

            $$A = \begin{pmatrix} \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} \end{pmatrix},\qquad t = a' - Aa = \binom{2}{2} - \binom{2}{1} = \binom{0}{1}.$$

            En numpy son **dos sistemas $3\times3$ con la misma matriz** $\mathrm{hom}(P)$, uno por coordenada de salida;
            `solve` resuelve los dos a la vez y la traspuesta deja $[\,A \mid t\,]$. Control con un cuarto punto: $d = (3, 2) \mapsto (5, 3)$.
            """),
            mo.vstack([
                mo.md("```python\nP = np.array([[1., 1.], [3., 1.], [1., 2.]])   # a, b, c\nQ = np.array([[2., 2.], [4., 2.], [3., 3.]])   # a', b', c'\nM = np.linalg.solve(lib.hom(P), Q).T          # 2×3 = [A | t]\nA, t = M[:, :2], M[:, 2]\nnp.array([3., 2.]) @ A.T + t                  # el cuarto punto\n```"),
                mo.md(f"`M` =\n```\n{np.round(_M, 3)}\n```\n`lib.afin_por_tres_puntos(P, Q)` da lo mismo: `{bool(np.allclose(_M[:, :2], A3) and np.allclose(_M[:, 2], t3))}`  \n"
                      f"$d = (3, 2) \\mapsto {lib.vec_tex(A3 @ [3, 2] + t3)}$"),
            ]),
        ], widths="equal", align="start"),
    ])
    return A3, P3, Q3, t3


@app.cell
def _(A_esc, lib, mo, mojones, mojones_esc, np, t_esc):
    _via_hom = lib.dehom(lib.hom(mojones) @ lib.matriz_afin(A_esc, t_esc).T)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **la afinidad entera sobre una nube $N\times2$ es `puntos @ A.T + t`**. El `@ A.T` es la lineal
        (filas = puntos, se transpone, como en Rotaciones II); el `+ t` suma la misma fila a todas. La versión homogénea
        hace lo mismo con una sola matriz: `lib.hom(puntos)` agrega la columna de unos ($N\times3$), `@ H.T` aplica la
        $3\times3$, y `lib.dehom` saca la columna de unos (dividiendo por ella).
        """),
        mo.md("```python\nmojones = np.array([[1., 1.], [1., 5.], [1., 3.]])   # shape (3, 2)\nmojones @ A.T + t                                     # Ax + t, fila por fila\nH = lib.matriz_afin(A, t)\nlib.dehom(lib.hom(mojones) @ H.T)                     # (3, 2) → (3, 3) → (3, 3) → (3, 2)\n```"),
        mo.md(f"`lib.hom(mojones).shape` = `{lib.hom(mojones).shape}` → resultado:\n```\n{np.round(_via_hom, 3)}\n```\n"
              f"Las esquinas escaneadas y el mojón intermedio de la sección 0; `np.allclose` con `mojones @ A.T + t`: `{bool(np.allclose(_via_hom, mojones_esc))}`."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("una afinidad conserva paralelas las paralelas").* $A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$,
        $t = (1, 0)$. Calculá las imágenes de los cuatro vértices del cuadrado unitario y el área de la figura que forman.
        ¿Puede un escaneo afín convertir el rectángulo de la parcela en un **trapecio** (dos lados que, prolongados, se cruzan)?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $(0,0) \mapsto (1,0)$, $(1,0) \mapsto (3,0)$, $(1,1) \mapsto (4,1)$, $(0,1) \mapsto (2,1)$: paralelogramo de base $2$ y
        altura $1$, área $2 = \det A$. Los lados paralelos siguen paralelos: los vértices de cada lado difieren en el mismo
        vector y $A$ lo manda al mismo vector. Un trapecio **no** puede salir; que dos paralelas se crucen es una
        transformación proyectiva (lección 05).
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("definir la imagen de un triángulo ya nos define completamente la afinidad").*
        $a = (0,0) \mapsto (1,2)$, $b = (1,0) \mapsto (3,3)$, $c = (0,1) \mapsto (2,4)$. Hallá $A$ y $t$, el factor de
        área y la imagen de $d = (1,1)$.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $t = a' = (1,2)$ porque $a$ es el origen. $Ae_1 = b' - a' = (2,1)$, $Ae_2 = c' - a' = (1,2)$:
        $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$, $\det A = 3$ (las áreas se triplican). $d \mapsto (3,3) + (1,2) = (4,5)$.
        Yapa: $(I - A)x = t$ es $-x - y = 1$ y $-x - y = 2$, incompatible: esta afinidad **no tiene punto fijo**.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def girar_y_mover(puntos, theta, t):\n    R = rot2(theta)\n    H = ...        # 3×3: primero girar theta, después mover t\n    return ...     # hom(puntos) → @ H.T → dehom; una fila por punto\n",
        language="python", min_height=130, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("un tema insistente de la clase fue la composición como una operación entre
        transformaciones").* Completá `girar_y_mover(puntos, theta, t)`: gira la nube $N\times2$ un ángulo `theta`
        (radianes) alrededor del origen y **después** la mueve `t`, con una sola matriz homogénea. Tenés `np`, `rot2`,
        `hom`, `dehom` y `matriz_afin(A, t)`. Se verifica con `np.allclose` sobre 20 puntos al azar.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _puntos = np.random.default_rng(56798).uniform(-5, 5, size=(20, 2))
    _theta, _t = np.deg2rad(37), np.array([2.0, -1.0])
    _R = lib.rot2(_theta)
    _esperado = lib.transformar_afin(_puntos, _R, _t)
    _ns = {"np": np, "rot2": lib.rot2, "hom": lib.hom, "dehom": lib.dehom, "matriz_afin": lib.matriz_afin}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.asarray(_ns["girar_y_mover"](_puntos, _theta, _t), dtype=float)
        if _obtenido.shape == (20, 3):
            _res = mo.callout(mo.md("❌ devolviste la nube homogénea `(20, 3)`: falta `dehom` para volver a `(20, 2)`."), kind="danger")
        elif _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ la forma es `{_obtenido.shape}`; tiene que ser `{_esperado.shape}` (una fila por punto)."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide con la referencia en los 20 puntos (θ = 37°, t = (2, −1))."), kind="success")
        elif np.allclose(_obtenido, lib.transformar(_puntos, _R)):
            _res = mo.callout(mo.md(r"❌ giró pero no se movió: te olvidaste la traslación. En $H$ va en la tercera columna."), kind="warn")
        elif np.allclose(_obtenido, lib.transformar_afin(_puntos, _R, _R @ _t)):
            _res = mo.callout(mo.md(r"❌ orden invertido: $R\,T$ mueve primero y el corrimiento sale girado. Primero girar es $H = T\,R$ (la de la derecha actúa primero)."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primer punto: esperado `{np.round(_esperado[0], 3).tolist()}`, obtenido `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="# esc: 3×2 (mojones en el escaneo), terr: 3×2 (los mismos en el terreno), esc4: el cuarto mojón en el escaneo\nM = ...          # 2×3 = [A | t] del escaneo AL terreno (np.linalg.solve con hom)\nA, t = ..., ...\ncuarto = ...     # el cuarto mojón, en el terreno\n",
        language="python", min_height=120, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado: corregir el plano escaneado** *("tres puntos conocidos alcanzan para
        corregirlo").* Tres mojones tienen coordenadas conocidas en el terreno, `terr`, y las leemos en el escaneo, `esc`.
        El cuarto sólo lo tenemos en el escaneo, `esc4`. Hallá la afinidad **del escaneo al terreno** y ubicá el cuarto
        mojón. Tenés `np`, `hom`, `dehom` y los tres arrays cargados.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(A_esc, editor_d, lib, mo, np, t_esc):
    terr = np.array([[1.0, 1.0], [1.0, 5.0], [5.0, 1.0]])
    esc = lib.transformar_afin(terr, A_esc, t_esc)
    cuarto_terr = np.array([5.0, 5.0])
    esc4 = lib.transformar_afin(cuarto_terr[None, :], A_esc, t_esc)[0]
    A_corr, t_corr = lib.afin_por_tres_puntos(esc, terr)
    _ns = {"np": np, "hom": lib.hom, "dehom": lib.dehom, "esc": esc.copy(), "terr": terr.copy(), "esc4": esc4.copy()}
    try:
        exec(editor_d.value, _ns)
        _c = np.asarray(_ns["cuarto"], dtype=float).reshape(-1)
        if _c.shape != (2,):
            _res = mo.callout(mo.md(f"❌ `cuarto` tiene forma `{np.shape(_ns['cuarto'])}`; tiene que ser un punto `(2,)`."), kind="danger")
        elif np.allclose(_c, cuarto_terr):
            _res = mo.callout(mo.md(rf"✅ el cuarto mojón está en ${lib.vec_tex(cuarto_terr)}$: la parcela era un cuadrado de $4$ m de lado. "
                                    rf"Corrección: $A = {lib.pmat(A_corr)}$, $t = {lib.vec_tex(t_corr)}$."), kind="success")
        elif np.allclose(_c, lib.transformar_afin(esc4[None, :], A_esc, t_esc)[0]):
            _res = mo.callout(mo.md("❌ armaste la afinidad al revés (del terreno al escaneo). `solve(hom(esc), terr)` va del escaneo al terreno."), kind="warn")
        elif np.allclose(_c, A_corr @ esc4):
            _res = mo.callout(mo.md("❌ aplicaste sólo la parte lineal: te olvidaste de sumar `t`."), kind="warn")
        elif np.allclose(_c, esc4 @ A_corr + t_corr):
            _res = mo.callout(mo.md("❌ casi: `esc4 @ A` es $A^T$ aplicada al punto. Con el punto como fila va `esc4 @ A.T + t`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide: obtuviste `{np.round(_c, 3).tolist()}`. Verificá que `esc @ A.T + t` devuelva `terr`."), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return A_corr, cuarto_terr, esc, esc4, t_corr, terr


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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "04_afines_homogeneas")
    respuestas_radio
    return preguntas_tanda, respuestas_radio


@app.cell
def _(lib, mo, preguntas_tanda, respuestas_radio):
    lib.corregir_autoevaluacion(mo, preguntas_tanda, respuestas_radio)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá verificamos; las demostraciones (por qué $Ax + t$ conserva paralelas, puntos fijos, composición por bloques):

    - [apunte, sección 10: transformaciones afines y coordenadas homogéneas](../../apunte.pdf#nameddest=cap:10) · [sección 5: puntos como rayos](../../apunte.pdf#nameddest=cap:05)
    - [apunte, sección 8: la guía de reflexiones y similaridades](../../apunte.pdf#nameddest=cap:08) · [sección 9: guía resuelta](../../apunte.pdf#nameddest=cap:09)
    - [apéndice 16: rotar alrededor de un centro y escalar alrededor de otro](../../apunte.pdf#nameddest=cap:16) · [apéndice 17: los seis ejercicios de afinidades](../../apunte.pdf#nameddest=cap:17)
    - [ficha de la clase 3](../../clases/03.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** [Proyectivas](../05_proyectivas/index.html): sin la restricción de la última fila $(0\ 0\ 1)$ las
    paralelas **sí** se cruzan, como los alambrados en una foto, y hacen falta cuatro puntos en vez de tres.
    """)
    return


@app.cell
def _(A3, A_corr, A_esc, A_h, H, M, P3, Q3, area_antes, area_despues, candidatos, cuarto_terr, esc, esc4, lib, mo, mojones, mojones_esc, np, t3, t_corr, t_esc, t_h, terr):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _Hesc = lib.matriz_afin(A_esc, t_esc)
    _Ab, _tb = np.array([[2.0, 1.0], [1.0, 2.0]]), np.array([1.0, 2.0])
    _B = np.array([[1.0, 1.0], [0.0, 1.0]])
    _checks = [
        ("sección 0: candidatos distintos; esquinas escaneadas (3, 2.25) y (5, 7.25); el intermedio es su punto medio",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4 and lib.exacto(mojones_esc[:2], [[3, 2.25], [5, 7.25]])
         and lib.exacto(candidatos["correcta"], mojones_esc[:2].mean(axis=0))),
        ("sección 2: área después = det · área antes; la 2×2 deja quieto el origen; la axial con factor 2 es [[1, 1], [0, 2]]",
         lib.exacto(area_despues, np.linalg.det(M) * area_antes, tol=1e-6) and lib.exacto(M @ [0, 0], [0, 0])
         and lib.exacto(_B @ np.diag([1.0, 2.0]) @ np.linalg.inv(_B), [[1, 1], [0, 2]])),
        ("sección 2: H tiene última fila (0 0 1), mueve el origen a t, det A = k²",
         lib.exacto(H[2], [0, 0, 1]) and lib.exacto(lib.dehom(H @ lib.hom([0, 0])), t_h) and lib.exacto(np.linalg.det(A_h), H[0, 0] ** 2 + H[1, 0] ** 2)),
        ("sección 3: A(4, 2) = (7, 2.5), H(4, 2, 1) = (8, 3.5, 1); tres puntos dan A = [[1, 1], [0, 1]], t = (0, 1), (3, 2) → (5, 3)",
         lib.exacto(A_esc @ [4, 2], [7, 2.5]) and lib.exacto(_Hesc @ lib.hom([4, 2]), [8, 3.5, 1]) and lib.exacto(A3, [[1, 1], [0, 1]])
         and lib.exacto(t3, [0, 1]) and lib.exacto(lib.transformar_afin(P3, A3, t3), Q3) and lib.exacto(A3 @ [3, 2] + t3, [5, 3])),
        ("sección 4: dehom(hom(x) Hᵀ) = A x + t", lib.exacto(lib.dehom(lib.hom(mojones) @ _Hesc.T), mojones_esc)),
        ("ejercicios (a) y (b): paralelogramo de área 2; A = [[2, 1], [1, 2]], t = (1, 2), d → (4, 5), sin punto fijo",
         lib.exacto(lib.area_poligono(lib.transformar_afin([[0, 0], [1, 0], [1, 1], [0, 1]], [[2, 1], [0, 1]], [1, 0])), 2.0)
         and lib.exacto(lib.transformar_afin([[0, 0], [1, 0], [0, 1]], _Ab, _tb), [[1, 2], [3, 3], [2, 4]]) and lib.exacto(_Ab @ [1, 1] + _tb, [4, 5])
         and np.linalg.matrix_rank(np.eye(2) - _Ab) < np.linalg.matrix_rank(np.column_stack([np.eye(2) - _Ab, _tb]))),
        ("ejercicio (d): la corrección invierte el escaneo y ubica el cuarto mojón en (5, 5)",
         lib.exacto(lib.matriz_afin(A_corr, t_corr) @ _Hesc, np.eye(3)) and lib.exacto(lib.transformar_afin(esc, A_corr, t_corr), terr)
         and lib.exacto(A_corr @ esc4 + t_corr, cuarto_terr)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
