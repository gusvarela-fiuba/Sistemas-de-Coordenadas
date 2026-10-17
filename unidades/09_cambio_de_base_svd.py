# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Cambio de base, SVD e inversas (lección 09, molde v2 sobre cb104). Clases 7 y 10.

LECCIÓN ANTICIPADA: las clases 7 y 10 no se dictaron todavía en 2C2026; lectura del esqueleto 2025, pendiente de
validar por la cátedra. Una sola idea: toda matriz manda algún par de direcciones perpendiculares a otro par
perpendicular, estiradas por los valores singulares: A = U Σ Vᵀ es rotar, estirar, rotar. La inversa lo deshace si
ninguna σ es cero; si no, lo más parecido a deshacer es la pseudoinversa A⁺ = V Σ⁺ Uᵀ.

Chequear:  uv run marimo check --select MW unidades/09_cambio_de_base_svd.py
Exportar:  uv run python tools/build.py --only 09_cambio_de_base_svd
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
    # Cambio de base, SVD e inversas

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    *Lección anticipada: las clases 7 y 10 no se dictaron todavía; lo que sigue es mi lectura del esqueleto 2025, de la
    nota de formas cuadráticas del campus y del apunte, pendiente de validar por la cátedra.*

    Sigo las clases 7 y 10. La pregunta: **¿Qué direcciones perpendiculares siguen perpendiculares después de
    transformar, y qué es lo más parecido a deshacer cuando no hay inversa?** El gancho: *más mediciones que incógnitas
    (una recta por puntos que no están alineados): la pseudoinversa elige la que deja el residuo perpendicular.*

    Colores: las direcciones de **entrada** $v_1$ (<span style="color:#1b6f6a">**teal**</span>) y $v_2$
    (<span style="color:#b5451b">**rust**</span>) son las columnas de $V$; sus imágenes $\sigma_1u_1$, $\sigma_2u_2$
    van del mismo color. Círculo unitario y elipse imagen en <span style="color:#7a4e9e">**violeta**</span>; grilla
    gris antes, teal después. En [Cambio de base](../08_cambio_de_base/index.html) busqué **una** grilla en la que
    $A$ sólo estira, y no siempre existe; acá uso dos, una a la entrada y otra a la salida, y siempre existe.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    A_pred = np.array([[2.0, 1.0], [0.0, 1.0]])
    U_pred, s_pred, Vt_pred = lib.svd2(A_pred)
    lam_pred, B_pred = lib.diagonalizar(A_pred)
    candidatos = {
        "ejes": float((A_pred @ [1, 0]) @ (A_pred @ [0, 1])),  # ⟨A e₁, A e₂⟩
        "propias": float((A_pred @ B_pred[:, 0]) @ (A_pred @ B_pred[:, 1])),  # ⟨A b₁, A b₂⟩, autovectores
        "entre-propias": float(B_pred[:, 0] @ B_pred[:, 1]),  # ⟨b₁, b₂⟩
        "singulares": float((A_pred @ Vt_pred[0]) @ (A_pred @ Vt_pred[1])),  # ⟨A v₁, A v₂⟩
    }
    prediccion = mo.ui.radio(
        options={
            "una elipse; sólo las direcciones propias de la unidad 08 siguen perpendiculares": "propias",
            "una elipse; cualquier par de direcciones perpendiculares sigue perpendicular": "siempre",
            "una elipse; ningún par perpendicular sigue perpendicular, porque A no es simétrica": "nunca",
            "una elipse; hay un par de direcciones perpendiculares que sigue perpendicular, y no son las propias": "correcta",
        },
        value=None,
        label=r"**Predicción.** Aplico $A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$ al disco unitario. Sale…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Alrededor de un mojón dibujo el **disco de 1 m** que marca con qué incertidumbre lo ubiqué: igual en todas
        las direcciones. Después paso las coordenadas a otro marco con $A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$,
        que estira el doble en $x$ y además **corre** (cizalla): el disco se vuelve la elipse de error de Topografía.
        ¿Qué le pasa a dos direcciones perpendiculares del disco? Dato: las direcciones propias de esta $A$ (unidad 08)
        son $(1, 0)$ y $(1, -1)$, que **no** son perpendiculares entre sí.
        """),
        prediccion,
    ])
    return A_pred, B_pred, U_pred, Vt_pred, candidatos, lam_pred, prediccion, s_pred


@app.cell
def _(A_pred, B_pred, Vt_pred, candidatos, lib, mo, prediccion, s_pred):
    _v1, _v2 = Vt_pred[0], Vt_pred[1]
    _par = rf"$v_1 = {lib.vec_tex(_v1)}$ y $v_2 = {lib.vec_tex(_v2)}$"
    _pi = lib.num_tex(candidatos["singulares"], 6)
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** {_par} van a $Av_1 = {lib.vec_tex(A_pred @ _v1)}$ y $Av_2 = {lib.vec_tex(A_pred @ _v2)}$, con producto interno ${_pi}$: "
                     rf"siguen perpendiculares y son los **semiejes de la elipse**, de largos $\sigma_1 = {lib.num_tex(s_pred[0])}$ y $\sigma_2 = {lib.num_tex(s_pred[1])}$. "
                     r"Abajo muestro que ese par siempre existe."),
        "siempre": ("warn",
                    rf"**No.** Los ejes $e_1, e_2$ van a $(2, 0)$ y $(1, 1)$, con producto interno ${lib.num_tex(candidatos['ejes'])} \ne 0$: la cizalla "
                    r"los cierra. Sólo un giro o una reflexión conservan **todos** los ángulos; una matriz cualquiera conserva el ángulo recto de un solo par."),
        "nunca": ("warn",
                  rf"**No.** Que $A$ no sea simétrica quita las direcciones propias perpendiculares, no las singulares: con {_par} las imágenes tienen "
                  rf"producto interno ${_pi}$. Ese par existe para **toda** matriz, también para un giro, que no tiene autovectores reales."),
        "propias": ("warn",
                    rf"**No.** Los autovectores $b_1 = {lib.vec_tex(B_pred[:, 0])}$ y $b_2 = {lib.vec_tex(B_pred[:, 1])}$ no son perpendiculares entre sí "
                    rf"($\langle b_1, b_2\rangle = {lib.num_tex(candidatos['entre-propias'])}$) ni sus imágenes (${lib.num_tex(candidatos['propias'])}$). Diagonalizar pregunta "
                    r"qué direcciones **caen sobre sí mismas**; la SVD, qué par perpendicular **sigue perpendicular**. Coinciden sólo si $A$ es simétrica."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** La perpendicularidad de **un** par de direcciones bien elegido de la entrada: "siempre existe
    una base ortogonal del espacio de entrada que se asigna a una base ortogonal de la salida" (el profesor, resumen
    2025). Los largos no se conservan: cada dirección se estira por su **valor singular** $\sigma_k \ge 0$, nunca complejo.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $a = (\pm 1)\cdot\lvert a\rvert$: signo a la salida, estiramiento $\lvert a\rvert$ | dar vuelta y estirar |
    | $\mathbb R^2$ | $A = U\Sigma V^\top$, $\Sigma = \mathrm{diag}(\sigma_1, \sigma_2)$ | el círculo unitario va a una **elipse** de semiejes $\sigma_1u_1$, $\sigma_2u_2$, que vienen de $v_1 \perp v_2$ |
    | $\mathbb R^3$ | lo mismo, $3\times3$ | la esfera va a un elipsoide de tres semiejes |

    **Rotar, estirar, rotar.** $A v_k = \sigma_k u_k$ con $V = [\textcolor{#1b6f6a}{v_1}\ \textcolor{#b5451b}{v_2}]$
    y $U = [u_1\ u_2]$ ortogonales. De derecha a izquierda, $A = U\Sigma V^\top$: $V^\top$ **gira** la entrada hasta
    que $v_1, v_2$ caen sobre los ejes, $\Sigma$ **estira** cada eje, $U$ **gira** (o refleja) al lugar final. Es la
    "base privilegiada" que buscaba el profesor: una grilla a la entrada, otra a la salida, y entre las dos la matriz
    es diagonal. Si $A$ es simétrica, $U = V$ y $\sigma_k = \lvert\lambda_k\rvert$: la diagonalización de la unidad 08.
    Si $A$ gira, $\Sigma = I$.

    **Inversa.** Deshacer tres movimientos es deshacerlos al revés: $A^{-1} = V\,\Sigma^{-1}U^\top$, "invertir una
    matriz diagonal es tomar recíprocos". Existe si ninguna $\sigma$ es $0$; $\det A = \pm\sigma_1\sigma_2$. Si
    $\sigma_2 = 0$ la elipse se aplastó en un segmento y no se sabe de dónde vino cada punto: no hay inversa, como $1/0$.

    **Pseudoinversa.** Si $\sigma_2 = 0$, o si $A$ es $N\times2$ (más mediciones que incógnitas), lo más parecido a
    deshacer es $A^{+} = V\,\Sigma^{+}U^\top$, con $1/\sigma$ sólo donde $\sigma \ne 0$ y ceros donde había ceros: la
    solución de **mínimos cuadrados** de norma mínima, que proyecta el término independiente sobre lo que $A$ puede
    producir y deshace sólo esa parte. En $\mathbb R$, la pseudoinversa de $0$ es $0$.

    **Los cuatro subespacios** (nombres del profesor), para $A$ de $m\times n$:

    | | quién lo genera | qué es |
    |---|---|---|
    | **imagen** de $A$ | los $u_k$ con $\sigma_k \ne 0$ | lo alcanzable a la salida |
    | **contra-imagen** (núcleo de $A^\top$) | los $u_k$ restantes | lo inaccesible, perpendicular a la imagen: **ahí vive el residuo** |
    | **co-imagen** (imagen de $A^\top$) | los $v_k$ con $\sigma_k \ne 0$ | lo que entra y se distingue a la salida |
    | **núcleo** de $A$ | los $v_k$ con $\sigma_k = 0$ | lo que entra y cae al $0$ (unidad 07b) |

    Esto es una **muestra**; la demostración de que $U, \Sigma, V$ existen está en Strang, no en el apunte (ver el cierre).
    """)
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (matriz, qué pasa) ----------
    casos = {
        "simétrica [[3, 1], [1, 2]]": (np.array([[3.0, 1.0], [1.0, 2.0]]),
                                        r"simétrica: $U = V$ y $\sigma = \lvert\lambda\rvert$; las direcciones singulares **son** las propias (unidad 08)."),
        "no simétrica [[2, 1], [0, 1]]": (np.array([[2.0, 1.0], [0.0, 1.0]]),
                                           r"la de la predicción: $U \ne V$. Las propias $(1, 0)$ y $(1, -1)$ no son perpendiculares; las singulares sí."),
        "aplastante [[1, 2], [2, 4]] (σ₂ = 0)": (np.array([[1.0, 2.0], [2.0, 4.0]]),
                                                  r"$\sigma_2 = 0$: la elipse es un **segmento**; $v_2$ es el núcleo, $u_2$ la contra-imagen, $\det = 0$, no hay inversa."),
        "rotación pura 40° (σ = 1, 1)": (np.array([[np.cos(np.deg2rad(40)), -np.sin(np.deg2rad(40))], [np.sin(np.deg2rad(40)), np.cos(np.deg2rad(40))]]),
                                          r"un giro: sin autovectores reales pero con SVD: $\Sigma = I$, el círculo sigue círculo y el giro queda en $U$ ($V = I$)."),
        "general (deslizadores)": (np.array([[1.0, -2.0], [1.5, 0.5]]),
                                   r"movelos; con $\det < 0$ la tercera etapa es una **reflexión** y la animación la hace en línea recta."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="no simétrica [[2, 1], [0, 1]]", label="caso precargado")
    mo.vstack([
        mo.md(r"""
        ## 2. Manipulación

        Tres capas. En **gris**, la grilla antes y el círculo unitario con sus direcciones singulares $v_1$ (teal) y
        $v_2$ (rust). En **teal**, la grilla después. En **violeta**, la elipse imagen con sus semiejes $\sigma_1u_1$ y
        $\sigma_2u_2$. **Reproducir** recorre las tres etapas: $V^\top$ gira (los $v_k$ caen sobre los ejes), $\Sigma$
        estira los ejes, $U$ gira al lugar final. Los deslizadores sólo se habilitan en el caso general.
        """),
        caso,
    ])
    return caso, casos


@app.cell
def _(caso, casos, mo):
    _A0, _ = casos[caso.value]
    es_general = caso.value.startswith("general")
    s_a, s_b, s_c, s_d = [mo.ui.slider(-4, 4, value=float(_v), step=0.1, label=f"{_n} = A{_i}", show_value=True, disabled=not es_general)
                          for _n, _i, _v in zip("abcd", ("₁₁", "₁₂", "₂₁", "₂₂"), _A0.ravel())]
    y3 = mo.ui.slider(0.0, 5.0, value=3.0, step=0.1, label="tercera medición y₃", show_value=True)
    return es_general, s_a, s_b, s_c, s_d, y3


@app.cell
def _(caso, casos, es_general, go, lib, mo, np, s_a, s_b, s_c, s_d):
    _A0, que_pasa = casos[caso.value]
    A = np.array([[s_a.value, s_b.value], [s_c.value, s_d.value]]) if es_general else np.asarray(_A0, dtype=float)
    U, s, Vt = lib.svd2(A)
    V = Vt.T
    _rango, _n = 5, 12
    # tres etapas: girar con Vᵀ (svd2 lo da como rotación), estirar con Σ, girar o reflejar con U
    _thV = np.arctan2(Vt[1, 0], Vt[0, 0])
    camino = [lib.rot2(t * _thV) for t in np.linspace(0, 1, _n)]
    camino += [np.diag(1 + t * (s - 1)) @ Vt for t in np.linspace(0, 1, _n)]
    if np.linalg.det(U) > 0:
        _thU = np.arctan2(U[1, 0], U[0, 0])
        camino += [lib.rot2(t * _thU) @ np.diag(s) @ Vt for t in np.linspace(0, 1, _n)]
    else:
        camino += [(np.eye(2) + t * (U - np.eye(2))) @ np.diag(s) @ Vt for t in np.linspace(0, 1, _n)]
    _circ = lib.circulo()

    def _dinamicas(i):
        f = go.Figure()
        lib.capa_despues(f, camino[i], _rango - 1, cuadrado=False, columnas=False)
        e = lib.transformar(_circ, camino[i])
        f.add_trace(go.Scatter(x=e[:, 0], y=e[:, 1], mode="lines", fill="toself", fillcolor="rgba(122,78,158,0.2)",
                               line=dict(color=lib.VIOLETA_OBJETO, width=2.5), name="imagen del círculo"))
        for k in range(2):
            lib.flecha(f, (0, 0), camino[i] @ V[:, k], lib.color_columna(k), f"A v{'₁₂'[k]} = σ{'₁₂'[k]} u{'₁₂'[k]}")
        return list(f.data)

    figura = lib.figura_plano(_rango, f"{caso.value}: rotar, estirar, rotar")
    lib.capa_antes(figura, _rango - 1, cuadrado=False)
    figura.add_trace(go.Scatter(x=_circ[:, 0], y=_circ[:, 1], mode="lines", line=dict(color=lib.GRIS_ANTES, width=2), name="círculo unitario antes"))
    lib.capa_direcciones_singulares(figura, A, despues=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))], duracion=60)

    det_A = float(np.linalg.det(A))
    if s[1] < 1e-9 * max(s[0], 1e-12):
        _cond, _inv = r"\infty", r"**no hay inversa** ($\sigma_2 = 0$): queda la pseudoinversa, sección 3.3"
    else:
        _cond, _inv = lib.num_tex(s[0] / s[1]), rf"$A^{{-1}} = V\Sigma^{{-1}}U^\top = {lib.pmat(V @ np.diag(1 / s) @ U.T)}$"
    _panel = mo.vstack([
        mo.md("**Controles**"), s_a, s_b, s_c, s_d,
        mo.md(rf"""
        **Números vivos**

        $$A = {lib.matriz_coloreada(A)} = U\Sigma V^\top,\quad U = {lib.pmat(U)},\ \Sigma = {lib.pmat(np.diag(s))},\ V^\top = {lib.pmat(Vt)}$$

        - $\sigma_1 = {lib.num_tex(s[0])}$, $\sigma_2 = {lib.num_tex(s[1])}$; $\det A = {lib.num_tex(det_A)} = \pm\sigma_1\sigma_2 = \pm{lib.num_tex(s[0] * s[1])}$
        - `np.allclose(U @ S @ Vt, A)` = `{bool(np.allclose(U @ np.diag(s) @ Vt, A))}` · número de condición $\sigma_1/\sigma_2 = {_cond}$
        - {_inv}

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.6)
    mo.vstack([mo.ui.plotly(figura), _panel])
    return A, U, V, Vt, camino, det_A, figura, que_pasa, s


@app.cell
def _(lib, mo, np, y3):
    A3 = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    y_med = np.array([0.0, 1.0, y3.value])
    x_mc, r_mc = lib.minimos_cuadrados(A3, y_med)
    sub = lib.cuatro_subespacios(A3)
    u3 = sub["contra_imagen"][:, 0]
    x_pinv = lib.pseudoinversa(A3) @ y_med
    mo.vstack([
        mo.md(r"""
        **Más mediciones que incógnitas: los cuatro subespacios en una $3\times2$.** Tres puntos $(0, 0)$, $(1, 1)$,
        $(2, y_3)$ y una recta $y = ax + b$: tres ecuaciones, dos incógnitas, $A = [\,x \mid 1\,]$. $A$ manda el plano
        $(a, b)$ a un **plano** dentro de $\mathbb R^3$ (la imagen, generada por $u_1, u_2$); la tercera dirección $u_3$
        es la contra-imagen, y las mediciones $y$ en general no caen en el plano. La solución de mínimos cuadrados (la
        de [Cuatro problemas](../11_cuatro_problemas/index.html)) es $A^{+}y$ y deja el residuo $r = y - Ax$ **sobre
        $u_3$**, perpendicular a todo lo que $A$ produce. Con $y_3 = 2$ los puntos quedan alineados y $r = 0$.
        """),
        y3,
        mo.md(rf"""
        - $A = {lib.matriz_coloreada(A3, 0)}$, $\sigma = {lib.vec_tex(sub['s'])}$, rango $2$ · $x = (a, b) = A^{{+}}y = \mathbf{{{lib.vec_tex(x_pinv)}}}$;
          por ecuaciones normales ${lib.vec_tex(x_mc)}$ (`np.allclose` = `{bool(np.allclose(x_mc, x_pinv))}`)
        - $r = y - Ax = {lib.vec_tex(r_mc)}$ · $A^\top r = {lib.vec_tex(A3.T @ r_mc, 6)}$ · $\langle r, u_3\rangle\,u_3 = {lib.vec_tex(float(r_mc @ u3) * u3)}$: **el residuo entero vive en la contra-imagen**
        - los cuatro subespacios: imagen (en $\mathbb R^3$) $= \langle u_1, u_2\rangle$ con $u_1 = {lib.vec_tex(sub['imagen'][:, 0])}$, $u_2 = {lib.vec_tex(sub['imagen'][:, 1])}$;
          contra-imagen $= \langle u_3\rangle$, $u_3 = {lib.vec_tex(u3)}$; co-imagen (en $\mathbb R^2$) $= \langle v_1, v_2\rangle$ = todo el plano $(a, b)$;
          núcleo $= \{{0\}}$ (dimensiones {sub['imagen'].shape[1]}, {sub['contra_imagen'].shape[1]}, {sub['coimagen'].shape[1]}, {sub['nucleo'].shape[1]})
        """),
    ])
    return A3, r_mc, sub, u3, x_mc, x_pinv, y_med


@app.cell
def _(lib, mo, np):
    _Ud, _sd, _Vtd = lib.svd2(np.diag([3.0, -2.0]))
    _A = np.array([[2.0, 1.0], [0.0, 1.0]])
    _U, _s, _Vt = np.linalg.svd(_A)
    _mu = np.linalg.eigvalsh(_A.T @ _A)[::-1]
    _P = np.array([[1.0, 2.0], [2.0, 4.0]])
    _Pp = np.linalg.pinv(_P)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        A mano alcanza con $A^\top A$: es simétrica, se diagonaliza como en la unidad 08 y sus autovalores son los
        $\sigma^2$ (ejercicio (a)). Izquierda, el cuaderno; derecha, numpy.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Ya diagonal: $D = \begin{pmatrix} 3 & 0 \\ 0 & -2 \end{pmatrix}$.** Los ejes van a los ejes ($v_k = e_k$), los
            estiramientos son $3$ y $2$ y el signo del $-2$ se lo lleva $U$: $D = \begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}\begin{pmatrix} 3 & 0 \\ 0 & 2 \end{pmatrix} I$,
            como $a = (\pm1)\lvert a\rvert$. $\det D = -6 = -\sigma_1\sigma_2$.
            """),
            mo.vstack([
                mo.md("```python\nU, s, Vt = lib.svd2(np.diag([3., -2.]))   # signos fijos; np.linalg.svd igual salvo signos\n```"),
                mo.md(f"`s` = `{np.round(_sd, 3).tolist()}` · `U` = `{np.round(_Ud, 3).tolist()}` · `Vt` = `{np.round(_Vtd, 3).tolist()}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 La de la predicción: $A = \begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix}$.**
            $$A^\top A = \begin{pmatrix} 2 & 0 \\ 1 & 1 \end{pmatrix}\begin{pmatrix} 2 & 1 \\ 0 & 1 \end{pmatrix} = \begin{pmatrix} 4 & 2 \\ 2 & 2 \end{pmatrix},\quad
            \mu^2 - 6\mu + 4 = 0 \Rightarrow \mu = 3 \pm \sqrt5.$$
            $\sigma_1 = \sqrt{3 + \sqrt5} = \tfrac{1 + \sqrt5}{\sqrt2} \approx 2.288$, $\sigma_2 = \tfrac{\sqrt5 - 1}{\sqrt2} \approx 0.874$;
            control $\sigma_1\sigma_2 = \tfrac{5 - 1}{2} = 2 = \det A$. Los $v_k$ son los autovectores de $A^\top A$ y $u_k = Av_k/\sigma_k$.
            """),
            mo.vstack([
                mo.md("```python\nA = np.array([[2., 1.], [0., 1.]])\nU, s, Vt = np.linalg.svd(A)\nmu = np.linalg.eigvalsh(A.T @ A)[::-1]   # autovalores de AᵀA, de mayor a menor\nnp.allclose(s**2, mu), np.allclose(U @ np.diag(s) @ Vt, A)\n```"),
                mo.md(f"`s` = `{np.round(_s, 3).tolist()}` · `mu` = `{np.round(_mu, 3).tolist()}` · `allclose` = `{bool(np.allclose(_s**2, _mu))}`, `{bool(np.allclose(_U @ np.diag(_s) @ _Vt, _A))}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 Pseudoinversa de la aplastante $P = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$.** $P^\top P = \begin{pmatrix} 5 & 10 \\ 10 & 20 \end{pmatrix}$,
            $\mu = 25, 0$: $\sigma_1 = 5$, $\sigma_2 = 0$, $v_1 = \tfrac{1}{\sqrt5}(1, 2)$, $u_1 = Pv_1/5 = v_1$.
            $$P^{+} = v_1\,\tfrac15\,u_1^\top = \tfrac1{25}\begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix};\qquad PP^{+}P = \tfrac1{25}P^3 = P.\ ✓$$
            El $1/\sigma_2 = 1/0$ no se toma: ahí va un $0$.
            """),
            mo.vstack([
                mo.md("```python\nP = np.array([[1., 2.], [2., 4.]])\nPp = np.linalg.pinv(P)\nnp.allclose(P @ Pp @ P, P), np.allclose(Pp, P / 25)\n```"),
                mo.md(f"`Pp` =\n```\n{np.round(_Pp, 4)}\n```\n`allclose` = `{bool(np.allclose(_P @ _Pp @ _P, _P))}`, `{bool(np.allclose(_Pp, _P / 25))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(mo):
    k_svd = mo.ui.slider(1, 12, value=3, step=1, label="k (valores singulares que conservo)", show_value=True)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Cuatro funciones de `np.linalg`: `svd(A)` devuelve `(U, s, Vt)`, `s` de mayor a menor y **`Vt` ya
        transpuesta**; `pinv(A)` es $A^{+}$; `lstsq(A, y, rcond=None)` resuelve el sistema alto (lo que usó la unidad 11:
        adentro hace $A^{+}y$ con la SVD); `cond(A)` es $\sigma_1/\sigma_2$, cuánto amplifica $A$ los errores. Y una
        idea: una **matriz de alturas** también es una transformación, y `U[:, :k] @ np.diag(s[:k]) @ Vt[:k]` es su mejor
        aproximación de rango $k$. Acá un terreno sintético de $40\times40$; con el DEM real de la Precordillera
        ($512\times512$, `datos/dem_copernicus/`) el RMS baja de $103$ m ($k = 1$) a $17$ m ($k = 10$) y $2$ m ($k = 100$).
        """),
        k_svd,
    ])
    return (k_svd,)


@app.cell
def _(go, k_svd, lib, mo, np):
    _u = np.linspace(-3, 3, 40)
    _X, _Y = np.meshgrid(_u, _u)
    Z = 1600 + 250 * np.exp(-((_X - 1) ** 2 + (_Y + 0.5) ** 2) / 2) + 180 * np.sin(1.3 * _X) * np.cos(0.8 * _Y) + 40 * _X - 25 * _Y
    Uz, sz, Vtz = np.linalg.svd(Z)
    Zk = lib.truncar_svd(Uz, sz, Vtz, k_svd.value)
    rms_k = float(np.sqrt(np.mean((Z - Zk) ** 2)))
    _fig = go.Figure()
    _fig.add_trace(go.Heatmap(z=Z, colorscale="Earth", showscale=False, xaxis="x", yaxis="y", name="terreno"))
    _fig.add_trace(go.Heatmap(z=Zk, colorscale="Earth", showscale=False, xaxis="x2", yaxis="y2", name=f"rango {k_svd.value}"))
    _fig.update_layout(width=620, height=330, margin=dict(l=10, r=10, t=40, b=10),
                       xaxis=dict(domain=[0, 0.48], visible=False), xaxis2=dict(domain=[0.52, 1], visible=False),
                       yaxis=dict(visible=False), yaxis2=dict(visible=False, anchor="x2"),
                       title=dict(text=f"alturas (izquierda) y su aproximación de rango k = {k_svd.value} (derecha): RMS = {rms_k:.1f} m", font=dict(size=13)))
    mo.vstack([
        mo.md("```python\nU, s, Vt = np.linalg.svd(Z)                    # Z: 40×40 de alturas\nZk = U[:, :k] @ np.diag(s[:k]) @ Vt[:k]      # rango k\nrms = np.sqrt(np.mean((Z - Zk) ** 2))\n```"),
        mo.md(f"`s[:6]` = `{np.round(sz[:6], 1).tolist()}` · `np.linalg.cond(Z)` = `{np.linalg.cond(Z):.3g}` · con k = {k_svd.value}: `rms` = `{rms_k:.2f}` m, de `{Z.std():.0f}` m de desvío. $\\sigma_1$ es casi la altura media por $40$: el primer término es la meseta."),
        mo.ui.plotly(_fig),
    ])
    return Uz, Vtz, Z, Zk, rms_k, sz


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("existe una base ortogonal de la entrada que va a una base ortogonal de la salida").*
        Si $A = U\Sigma V^\top$, calculá $A^\top A$ y explicá por qué los $\sigma_k^2$ son sus autovalores y los $v_k$ sus
        autovectores. ¿Por qué eso garantiza que los $\sigma$ nunca son complejos?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $A^\top A = V\Sigma^\top U^\top U\Sigma V^\top = V\,\Sigma^2\,V^\top$ porque $U^\top U = I$: es $B\Lambda B^{-1}$
        de la unidad 08 con $B = V$ ($V^{-1} = V^\top$), diagonal en la grilla de los $v_k$ con $\sigma_k^2$ en la
        diagonal. $A^\top A$ es simétrica (autovalores reales) y $\langle v, A^\top Av\rangle = \lVert Av\rVert^2 \ge 0$
        (no negativos): $\sigma_k = \sqrt{\mu_k}$ existe siempre. Que $U$ también salga ortogonal lo demuestra Strang.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("invertir una matriz diagonal es tomar recíprocos").* ¿Cuándo $A^{+} = A^{-1}$? Calculá
        las dos para $D = \begin{pmatrix} 3 & 0 \\ 0 & -2 \end{pmatrix}$ y para $P = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$, y decí qué hace $A^{+}A$ con un vector.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        Coinciden cuando $A$ es cuadrada y **ningún $\sigma$ es cero** ($\det A \ne 0$): $\Sigma^{+} = \Sigma^{-1}$ y
        $V\Sigma^{-1}U^\top$ es la inversa. $D$: $D^{-1} = D^{+} = \mathrm{diag}(\tfrac13, -\tfrac12)$, $D^{+}D = I$.
        $P$: $\sigma_2 = 0$, no hay $P^{-1}$; $P^{+} = \tfrac1{25}P$ (3.3) y $P^{+}P = \tfrac15P$ es la **proyección** sobre la
        recta de $(1, 2)$: deshace lo que $P$ no aplastó y manda a $0$ el núcleo $(2, -1)$. En $\mathbb R$: $1/a$ si $a \ne 0$, $0$ si $a = 0$.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def reconstruir(U, s, Vt, k):\n    # U, s, Vt como los devuelve np.linalg.svd; k: cuántos valores singulares conservo\n    return ...   # la aproximación de rango k, misma forma que la matriz original\n",
        language="python", min_height=110, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("quedarse con los $k$ primeros es la mejor aproximación de rango $k$").*
        Completá `reconstruir(U, s, Vt, k)`. Tenés `np`. Se verifica con `np.allclose` en una matriz $6\times6$ al azar
        con $k = 2$ y $k = 6$ (con $k = 6$ tiene que devolver la matriz entera).
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _M = np.random.default_rng(56798).normal(size=(6, 6))
    _U, _s, _Vt = np.linalg.svd(_M)
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _r2 = np.asarray(_ns["reconstruir"](_U.copy(), _s.copy(), _Vt.copy(), 2), dtype=float)
        _r6 = np.asarray(_ns["reconstruir"](_U.copy(), _s.copy(), _Vt.copy(), 6), dtype=float)
        if _r2.shape != (6, 6):
            _res = mo.callout(mo.md(f"❌ la forma del resultado es `{_r2.shape}`; tiene que ser `(6, 6)`. Recortá columnas de `U`, entradas de `s` y filas de `Vt`."), kind="danger")
        elif np.allclose(_r2, lib.truncar_svd(_U, _s, _Vt, 2)) and np.allclose(_r6, _M):
            _res = mo.callout(mo.md("✅ coincide: rango 2 con `U[:, :2] @ np.diag(s[:2]) @ Vt[:2]`, y con k = 6 vuelve la matriz."), kind="success")
        elif np.allclose(_r2, _M):
            _res = mo.callout(mo.md(r"❌ con $k = 2$ devolvés la matriz entera: usaste `np.diag(s)` sin recortar. Quedate con `s[:k]`, `U[:, :k]` y `Vt[:k]`."), kind="warn")
        elif np.allclose(_r6, _U @ np.diag(_s) @ _Vt.T) or np.allclose(_r2, _U[:, :2] @ np.diag(_s[:2]) @ _Vt.T[:2]):
            _res = mo.callout(mo.md(r"❌ transpusiste `Vt`: `np.linalg.svd` ya devuelve $V^\top$, se usa `Vt[:k]` tal cual (filas = los $v_k^\top$)."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para k = 2 el error RMS contra la referencia es `{np.sqrt(np.mean((_r2 - lib.truncar_svd(_U, _s, _Vt, 2)) ** 2)):.3f}`."), kind="danger")
    except ValueError as _e:  # las formas no encajan: casi siempre un Vt[:k].T
        _res = mo.callout(mo.md(f"❌ las formas no encajan (`{_e}`): seguramente transpusiste `Vt`. `np.linalg.svd` ya devuelve $V^\\top$; usá `Vt[:k]` tal cual."), kind="warn")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def pseudoinversa(A, tol=1e-10):\n    U, s, Vt = np.linalg.svd(A, full_matrices=False)\n    s_plus = ...   # 1/σ donde σ > tol, 0 donde σ = 0\n    return ...     # V Σ⁺ Uᵀ\n",
        language="python", min_height=130, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("la pseudoinversa elige el punto de la imagen más cercano").* Completá
        `pseudoinversa(A)` desde la SVD. Tenés `np`. Se verifica con `np.allclose` contra `np.linalg.pinv` en
        $P = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$, en la no simétrica $\begin{pmatrix} 1 & 1 \\ 2 & 2 \end{pmatrix}$ y en la $3\times2$ de la sección 2.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(A3, editor_d, mo, np):
    _pruebas = [np.array([[1.0, 2.0], [2.0, 4.0]]), np.array([[1.0, 1.0], [2.0, 2.0]]), A3]
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        with np.errstate(divide="ignore", invalid="ignore"):
            _obt = [np.asarray(_ns["pseudoinversa"](M.copy()), dtype=float) for M in _pruebas]
        _ok = all(o.shape == np.linalg.pinv(M).shape and np.allclose(o, np.linalg.pinv(M)) for o, M in zip(_obt, _pruebas))
        _M1 = _pruebas[1]
        _U1, _s1, _Vt1 = np.linalg.svd(_M1, full_matrices=False)
        _sp1 = np.array([1 / x if x > 1e-10 else 0.0 for x in _s1])
        if _ok:
            _res = mo.callout(mo.md("✅ coincide con `np.linalg.pinv` en las tres matrices: $A^{+} = V\\Sigma^{+}U^\\top$ con ceros donde $\\sigma = 0$."), kind="success")
        elif any(not np.all(np.isfinite(o)) for o in _obt):
            _res = mo.callout(mo.md(r"❌ aparecen `inf` o `nan`: invertiste un $\sigma = 0$. Donde $\sigma$ es cero va un $0$ en $\Sigma^{+}$, no $1/0$ (`np.where(s > tol, 1/s, 0)`)."), kind="warn")
        elif _obt[1].shape == (2, 2) and np.allclose(_obt[1], _U1 @ np.diag(_sp1) @ _Vt1):
            _res = mo.callout(mo.md(r"❌ $U$ y $V$ en el orden de $A$: la pseudoinversa deshace al revés, $V\Sigma^{+}U^\top$ (`Vt.T @ np.diag(s_plus) @ U.T`). En una simétrica no se nota; en $\begin{pmatrix} 1 & 1 \\ 2 & 2 \end{pmatrix}$ sí."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para la no simétrica obtuve\n```\n{np.round(_obt[1], 4)}\n```\ny `pinv` da\n```\n{np.round(np.linalg.pinv(_M1), 4)}\n```"), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré que toda matriz es rotar, estirar, rotar; que la inversa lo deshace al revés y que la pseudoinversa
    deshace sólo lo que no se aplastó, dejando el residuo en la contra-imagen. La SVD **no tiene sección propia en el
    apunte v3** (figura como pendiente en el hilo y como propuesta en las rúbricas). La demostración de que $U$,
    $\Sigma$, $V$ existen y de que $A^{+}y$ minimiza $\lVert y - Ax\rVert$ está en Strang, *Álgebra lineal y sus
    aplicaciones*, y en Calvetti–Somersalo, nombrados por el profesor el 2026-10-14.

    - [apunte, sección 11: bloque algebraico](../../apunte.pdf#nameddest=cap:11) · [sección 19: cambio de base y SVD,
      propuesta](../../apunte.pdf#nameddest=cap:19) · [sección 2: el hilo](../../apunte.pdf#nameddest=cap:02)
    - [ficha de la clase 7](../../clases/07.html) · [ficha de la clase 10](../../clases/10.html) · [el camino](../../index.html)
    - viene de: [cambio de base](../08_cambio_de_base/index.html) (la SVD es la versión que siempre existe) ·
      [núcleo y autovectores](../07b_nucleo_autovectores/index.html) (los $v_k$ con $\sigma_k = 0$) ·
      [producto interno](../02_producto_interno/index.html) (el residuo perpendicular)

    **Lo que viene:** [Cuatro problemas](../11_cuatro_problemas/index.html): regresión, círculos, Procrustes y
    regresión total son `lstsq`, o sea $A^{+}$, cuatro veces; y [Jacobiano y primera forma](../10_jacobiano_primera_forma/index.html):
    una $3\times2$ cuya imagen es el plano tangente y cuya contra-imagen es la normal.
    """)
    return


@app.cell
def _(A, A3, A_pred, U, V, Vt, candidatos, camino, det_A, lam_pred, lib, mo, np, r_mc, s, sub, u3, x_mc, x_pinv):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _sp = lib.svd2(A_pred)[1]
    _P = np.array([[1.0, 2.0], [2.0, 4.0]])
    _checks = [
        ("sección 0: imágenes de e₁, e₂ y de los autovectores no perpendiculares; las de v₁, v₂ sí; λ = (2, 1)",
         abs(candidatos["ejes"]) > 0.5 and abs(candidatos["propias"]) > 0.5 and abs(candidatos["entre-propias"]) > 0.5
         and abs(candidatos["singulares"]) < 1e-9 and lib.exacto(lam_pred, [2, 1])),
        ("sección 3: σ = ((1+√5)/√2, (√5−1)/√2) con σ₁σ₂ = 2; diag(3, −2) → σ = (3, 2); P⁺ = P/25",
         lib.exacto(_sp, [(1 + np.sqrt(5)) / np.sqrt(2), (np.sqrt(5) - 1) / np.sqrt(2)]) and lib.exacto(_sp[0] * _sp[1], 2.0)
         and lib.exacto(lib.svd2(np.diag([3.0, -2.0]))[1], [3, 2]) and lib.exacto(lib.pseudoinversa(_P), _P / 25)),
        ("sección 2: A = U Σ Vᵀ, V rotación, det A = ±σ₁σ₂, la animación va de I a A",
         lib.exacto(U @ np.diag(s) @ Vt, A, tol=1e-9) and lib.exacto(np.linalg.det(V), 1.0) and lib.exacto(abs(det_A), s[0] * s[1], tol=1e-9)
         and lib.exacto(camino[-1], A, tol=1e-9) and lib.exacto(camino[0], np.eye(2))),
        ("sección 2: A⁺y = ecuaciones normales = lstsq; Aᵀr = 0; r ∥ u₃; imagen ⊥ contra-imagen",
         lib.exacto(x_pinv, x_mc, tol=1e-9) and lib.exacto(x_mc, np.linalg.lstsq(A3, A3 @ x_mc + r_mc, rcond=None)[0], tol=1e-9)
         and lib.exacto(A3.T @ r_mc, [0, 0], tol=1e-9) and lib.exacto(float(r_mc @ u3) * u3, r_mc, tol=1e-9)
         and lib.exacto(sub["imagen"].T @ sub["contra_imagen"], [[0], [0]]) and sub["nucleo"].shape == (2, 0)),
        ("sección 2, y₃ = 3: x = (1.5, −1/6), r = (1/6, −1/3, 1/6) como en la ficha 10",
         lib.exacto(lib.pseudoinversa(A3) @ [0, 1, 3], [1.5, -1 / 6]) and lib.exacto([0, 1, 3] - A3 @ lib.minimos_cuadrados(A3, [0, 1, 3])[0], [1 / 6, -1 / 3, 1 / 6])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
