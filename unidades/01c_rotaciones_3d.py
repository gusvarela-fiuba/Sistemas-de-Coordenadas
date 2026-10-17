# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Rotaciones III — tres ejes y el orden importa (lección 01c, molde v2 sobre cb104). Clases 1 y 2.

Una sola idea: en 3D hay una rotación por cada eje coordenado, no conmutan, y toda composición es una sola rotación
alrededor de un eje fijo (Euler; la fórmula es la de Rodrigues). Cubo unitario y terreno con figura_espacio;
tres ángulos; Rz·Ry ≠ Ry·Rz con el mismo cubo.

Chequear:  uv run marimo check --select MW unidades/01c_rotaciones_3d.py
Exportar:  uv run python tools/build.py --only 01c_rotaciones_3d
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
    # Rotaciones III — tres ejes y el orden importa

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Sigo el final de la clase 1 y el comienzo de la 2. En el plano alcanzaba un ángulo. En el espacio hay que decir
    **alrededor de qué eje**, hay un giro básico por cada eje coordenado, y **el orden en que los encadeno cambia el
    resultado**. La parte buena: por más giros que encadene, el resultado es **un solo giro** alrededor de algún eje.

    Colores: la **primera columna** de la matriz es <span style="color:#1b6f6a">**teal**</span>, la **segunda**
    <span style="color:#b5451b">**rust**</span> y la **tercera** <span style="color:#c9a227">**gold**</span>: las tres
    flechas desde el origen, las imágenes de $e_x, e_y, e_z$. El eje fijo va en <span style="color:#7a4e9e">**violeta**</span>.
    Grados en los controles, radianes adentro; mano derecha.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0. Situación de campo y predicción

    Para nivelar la estación total la inclino alrededor de un eje horizontal y después la giro alrededor del eje
    vertical para apuntar al mojón. Un compañero hace lo mismo al revés: primero gira, después inclina. Con
    correcciones chiquitas los dos terminan casi igual. Con giros grandes, no.

    Un caso extremo, con un punto de prueba: el extremo del eje $x$ del instrumento, $e_x = (1, 0, 0)$. Lo giro $90°$
    alrededor de $y$ y **después** $90°$ alrededor de $z$ (mano derecha: antihorario mirando desde la punta del eje).
    ¿Dónde termina?
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- los números de la predicción salen de acá, nunca a mano ----------
    ex = np.array([1.0, 0.0, 0.0])
    Ry90, Rz90 = lib.rot_y(np.pi / 2), lib.rot_z(np.pi / 2)
    candidatos = {
        "correcta": Rz90 @ Ry90 @ ex,  # primero y, después z: la matriz de la derecha actúa primero
        "otro-orden": Ry90 @ Rz90 @ ex,  # primero z, después y
        "mismas": ex.copy(),
        "reflexion": -ex,
    }
    prediccion = mo.ui.radio(
        options={
            lib.vec_plano(candidatos["otro-orden"]): "otro-orden",
            lib.vec_plano(candidatos["mismas"]) + "  (no se mueve)": "mismas",
            lib.vec_plano(candidatos["correcta"]): "correcta",
            lib.vec_plano(candidatos["reflexion"]): "reflexion",
        },
        value=None,
        label=r"**Predicción.** Giro $e_x = (1, 0, 0)$ primero $90°$ alrededor de $y$ y después $90°$ alrededor de $z$. Termina en…",
    )
    prediccion
    return Ry90, Rz90, candidatos, ex, prediccion


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Alrededor de $y$, $e_x$ baja a $-e_z$ (mano derecha: $e_z \to e_x \to -e_z$). Y el giro alrededor de "
                     r"$z$ deja quieto todo lo que está sobre el eje $z$: $-e_z$ se queda. En la sección 2 fijate que en el otro "
                     r"orden termina en otro lado."),
        "otro-orden": ("warn",
                       r"**No.** $(0, 1, 0)$ es donde termina si giro **primero alrededor de $z$** ($e_x \to e_y$) y después alrededor "
                       r"de $y$ ($e_y$ queda quieto). Invertiste el orden, y en 3D el orden cambia el resultado: eso es lo que "
                       r"muestra la lección."),
        "mismas": ("warn",
                   r"**No.** $e_x$ no está sobre el eje $y$ ni sobre el eje $z$, así que ninguno de los dos giros lo deja quieto. "
                   r"Sólo queda quieto lo que está sobre el eje de giro."),
        "reflexion": ("warn",
                      r"**No.** $(-1, 0, 0)$ sería dar vuelta $e_x$ como en un espejo (o girarlo $180°$ alrededor de $z$), y acá "
                      r"cada giro es de $90°$. El primer giro ya lo saca del eje $x$: va a parar a $-e_z$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Un giro básico por cada eje.** $R_x$, $R_y$, $R_z$ dejan quieto un eje coordenado y giran el plano perpendicular
    como en 2D: es la matriz $R(\theta)$ "empotrada", con un $1$ en la diagonal para la coordenada que no se mueve.
    Cada columna sigue siendo "a dónde va $e_k$".

    $$R_x(\alpha) = \begin{pmatrix} \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{\cos\alpha} & \textcolor{#c9a227}{-\sin\alpha} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{\sin\alpha} & \textcolor{#c9a227}{\cos\alpha} \end{pmatrix}, \quad
    R_y(\beta) = \begin{pmatrix} \textcolor{#1b6f6a}{\cos\beta} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{\sin\beta} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{-\sin\beta} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{\cos\beta} \end{pmatrix}, \quad
    R_z(\gamma) = \begin{pmatrix} \textcolor{#1b6f6a}{\cos\gamma} & \textcolor{#b5451b}{-\sin\gamma} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{\sin\gamma} & \textcolor{#b5451b}{\cos\gamma} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{1} \end{pmatrix}.$$

    ($R_y$ parece tener los signos cambiados de lado: el plano que gira es el $(z, x)$, en ese orden, para que la mano
    derecha valga en los tres; apunte, sección 14.)

    **El orden importa.** Hacer $R_y$ y después $R_z$ es la matriz $R_z R_y$: **la de la derecha actúa primero**. Y
    $R_z R_y \neq R_y R_z$: la predicción de arriba son dos destinos distintos para el mismo punto. Con ángulos chicos
    la diferencia es de segundo orden (apunte, sección 15).

    **Toda composición es un solo giro.** El producto sigue cumpliendo $R^TR = I$ y $\det R = 1$, y toda matriz así deja
    fija una recta (el **eje**) y gira el plano perpendicular (teorema de Euler). La fórmula que arma la matriz desde
    eje y ángulo es la de Rodrigues (apunte, sección 14; `lib.rodrigues`). La figura lo muestra: el eje violeta no se mueve.

    | | giros que dejan quieto el $0$ | lo que se ve |
    |---|---|---|
    | $\mathbb R^2$ | un ángulo; todos conmutan | circunferencias |
    | $\mathbb R^3$ | eje y ángulo (tres números); no conmutan | el eje queda, el resto gira en planos perpendiculares a él |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Manipulación

    El **cubo unitario** y un **terreno** ($7\times7$ puntos con alturas, un array $49\times3$) giran con
    $R = R_z(\gamma)\,R_y(\beta)\,R_x(\alpha)$ (primero $x$, después $y$, después $z$) o con el orden inverso, según el
    menú. Gris = antes, teal = después; las tres flechas son las columnas de $R$. En **línea de puntos rust**, el cubo
    con el **otro orden**: la distancia entre los dos cubos es el número vivo que importa. En **violeta**, el eje de la
    rotación compuesta: la recta que $R$ deja quieta.

    Arranca con $\alpha = 0$, $\beta = \gamma = 90°$, que es exactamente $R_zR_y$ contra $R_yR_z$. Después bajá los tres
    a $5°$ y mirá cómo se acercan los dos cubos. La cámara se mueve con el mouse.
    """)
    return


@app.cell
def _(mo):
    alfa = mo.ui.slider(-180, 180, value=0, step=1, label="α (°), alrededor de x", show_value=True)
    beta = mo.ui.slider(-180, 180, value=90, step=1, label="β (°), alrededor de y", show_value=True)
    gama = mo.ui.slider(-180, 180, value=90, step=1, label="γ (°), alrededor de z", show_value=True)
    orden = mo.ui.dropdown(
        options={"x → y → z   (R = Rz·Ry·Rx)": "xyz", "z → y → x   (R = Rx·Ry·Rz)": "zyx"},
        value="x → y → z   (R = Rz·Ry·Rx)",
        label="orden de aplicación",
    )
    return alfa, beta, gama, orden


@app.cell
def _(alfa, beta, gama, go, lib, mo, np, orden):
    a_rad, b_rad, g_rad = (np.deg2rad(s.value) for s in (alfa, beta, gama))
    R_xyz = lib.rot_z(g_rad) @ lib.rot_y(b_rad) @ lib.rot_x(a_rad)  # primero x, después y, después z
    R_zyx = lib.rot_x(a_rad) @ lib.rot_y(b_rad) @ lib.rot_z(g_rad)  # primero z, después y, después x
    R, R_otro = (R_xyz, R_zyx) if orden.value == "xyz" else (R_zyx, R_xyz)
    eje, ang = lib.eje_angulo(R)

    cubo, aristas = lib.cubo_unitario()
    terreno, malla = lib.terreno_suave(7)
    cubo_despues = lib.transformar(cubo, R)
    cubo_otro = lib.transformar(cubo, R_otro)
    terreno_despues = lib.transformar(terreno, R)
    dist_ordenes = float(np.linalg.norm(R_xyz - R_zyx))
    dist_vertice = float(np.linalg.norm(cubo_despues[7] - cubo_otro[7]))  # el vértice (1,1,1)

    figura = lib.figura_espacio(2.6, f"α={alfa.value}°, β={beta.value}°, γ={gama.value}° · orden {orden.value}")
    for _pts, _pares, _col, _w, _nom in ((cubo, aristas, lib.GRIS_ANTES, 3, "cubo antes"), (terreno, malla, lib.GRIS_ANTES, 2, "terreno antes"),
                                         (cubo_despues, aristas, lib.TEAL_DESPUES, 6, "cubo después"), (terreno_despues, malla, lib.TEAL_DESPUES, 2, "terreno después")):
        _x, _y, _z = lib.segmentos_3d(_pts, _pares)
        figura.add_trace(go.Scatter3d(x=_x, y=_y, z=_z, mode="lines", line=dict(color=_col, width=_w), name=_nom, hoverinfo="skip"))
    _x, _y, _z = lib.segmentos_3d(cubo_otro, aristas)
    figura.add_trace(go.Scatter3d(x=_x, y=_y, z=_z, mode="lines", line=dict(color=lib.COLORES[1], width=3, dash="dot"), name="cubo con el otro orden"))
    lib.flechas_columnas_3d(figura, R)
    figura.add_trace(go.Scatter3d(x=[-2.4 * eje[0], 2.4 * eje[0]], y=[-2.4 * eje[1], 2.4 * eje[1]], z=[-2.4 * eje[2], 2.4 * eje[2]], mode="lines",
                                  line=dict(color=lib.VIOLETA_OBJETO, width=5, dash="dash"), name="eje de R (queda quieto)"))

    _panel = mo.vstack([
        mo.md("**Controles**"),
        alfa, beta, gama, orden,
        mo.md(rf"""
        **Números vivos**

        - $\lVert R_zR_yR_x - R_xR_yR_z\rVert = \mathbf{{{lib.num_tex(dist_ordenes, 4)}}}$ (diferencia entre los dos órdenes)
        - el vértice $(1,1,1)$ cae a distancia $\mathbf{{{lib.num_tex(dist_vertice, 4)}}}$ de donde cae con el otro orden
        - $R^TR = I$: {bool(np.allclose(R.T @ R, np.eye(3)))} · $\det R = {lib.num_tex(np.linalg.det(R), 4)}$
        - eje de $R$: ${lib.vec_tex(eje)}$, ángulo ${lib.num_tex(np.rad2deg(ang), 1)}°$; $R\,\mathrm{{eje}} = \mathrm{{eje}}$: {bool(np.allclose(R @ eje, eje))}

        $$R = {lib.matriz_coloreada(R)}$$

        Columnas: $Re_x$ (<span style="color:{lib.COLORES[0]}">teal</span>), $Re_y$ (<span style="color:{lib.COLORES[1]}">rust</span>),
        $Re_z$ (<span style="color:{lib.COLORES[2]}">gold</span>): perpendiculares entre sí y de largo $1$. Tres giros
        encadenados, y lo que queda es **un** giro de ${lib.num_tex(np.rad2deg(ang), 1)}°$ alrededor del eje violeta.
        """),
    ], gap=0.5)
    mo.hstack([_panel, mo.ui.plotly(figura)], widths=[1, 2], align="start")
    return R, R_xyz, R_zyx, ang, dist_ordenes, eje, terreno, terreno_despues


@app.cell
def _(Ry90, Rz90, ex, lib, mo, np):
    # 3.1  Rz(90°)·Ry(90°) columna por columna, y los dos órdenes
    _R = Rz90 @ Ry90
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La composición, columna por columna.** Para armar $R = R_z(90°)R_y(90°)$ no hace falta multiplicar
            nueve por nueve: la columna $k$ es "a dónde va $e_k$", y lo sigo giro por giro (primero $y$, después $z$):

            - $e_x \xrightarrow{R_y} -e_z \xrightarrow{R_z} -e_z$ (sobre el eje $z$, $R_z$ no lo toca): columna 1 $= \textcolor{#1b6f6a}{(0, 0, -1)}$
            - $e_y \xrightarrow{R_y} e_y \xrightarrow{R_z} -e_x$: columna 2 $= \textcolor{#b5451b}{(-1, 0, 0)}$
            - $e_z \xrightarrow{R_y} e_x \xrightarrow{R_z} e_y$: columna 3 $= \textcolor{#c9a227}{(0, 1, 0)}$

            $$R_z(90°)R_y(90°) = \begin{pmatrix} \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{-1} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{1} \\ \textcolor{#1b6f6a}{-1} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{0} \end{pmatrix}.$$

            En el otro orden, $e_x \xrightarrow{R_z} e_y \xrightarrow{R_y} e_y$: la primera columna de $R_yR_z$ es $(0, 1, 0)$. Dos matrices distintas.
            """),
            mo.vstack([
                mo.md("```python\nRy, Rz = lib.rot_y(np.pi / 2), lib.rot_z(np.pi / 2)\nR = Rz @ Ry                 # primero y, después z\nR[:, 0]                     # a dónde va e_x\n(Ry @ Rz)[:, 0]             # el otro orden\nnp.allclose(Rz @ Ry, Ry @ Rz)\n```"),
                mo.md(f"`R` =\n```\n{np.round(_R, 3)}\n```\n`R[:, 0]` = `{np.round(_R @ ex, 3).tolist()}` · `(Ry @ Rz)[:, 0]` = `{np.round(Ry90 @ Rz90 @ ex, 3).tolist()}`  \n`np.allclose(Rz @ Ry, Ry @ Rz)` = `{bool(np.allclose(_R, Ry90 @ Rz90))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(Ry90, Rz90, lib, mo, np):
    # 3.2  el eje fijo de la composición y Rodrigues
    _R = Rz90 @ Ry90
    _u = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    _eje, _ang = lib.eje_angulo(_R)
    mo.hstack([
        mo.md(r"""
        **3.2 Un solo giro.** $R = R_z(90°)R_y(90°)$ es ortogonal con $\det = 1$, así que tiene que dejar quieta una recta.
        Pruebo $u = (-1, 1, 1)/\sqrt3$:
        $$R\,u = \tfrac{1}{\sqrt3}\begin{pmatrix} 0\cdot(-1) - 1\cdot1 + 0 \\ 0 + 0 + 1\cdot1 \\ -1\cdot(-1) + 0 + 0 \end{pmatrix} = \tfrac{1}{\sqrt3}\begin{pmatrix} -1 \\ 1 \\ 1 \end{pmatrix} = u.$$
        Ese es el eje. El ángulo sale de la traza: $\operatorname{tr} R = 0 = 1 + 2\cos\theta$, $\theta = 120°$: y
        $R^3 = I$, tres veces el giro es la vuelta entera. Rodrigues arma la misma matriz desde $(u, 120°)$.
        """),
        mo.vstack([
            mo.md("```python\nu = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)\nnp.allclose(R @ u, u)\neje, ang = lib.eje_angulo(R)          # (eje unitario, radianes)\nnp.allclose(lib.rodrigues(u, np.deg2rad(120)), R)\nnp.allclose(np.linalg.matrix_power(R, 3), np.eye(3))\n```"),
            mo.md(f"`np.allclose(R @ u, u)` = `{bool(np.allclose(_R @ _u, _u))}`  \n`eje` = `{np.round(_eje, 4).tolist()}` · `np.rad2deg(ang)` = `{np.rad2deg(_ang):.1f}`  \n"
                  f"`rodrigues` = `{bool(np.allclose(lib.rodrigues(_u, np.deg2rad(120)), _R))}` · `R³ = I`: `{bool(np.allclose(np.linalg.matrix_power(_R, 3), np.eye(3)))}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(lib, mo, np, terreno, terreno_despues):
    _a = lib.rot_x(0.3)
    _b = lib.rot_z(0.5)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **`@` encadena de derecha a izquierda**, igual que la composición. `rot_z(g) @ rot_y(b) @ rot_x(a)`
        aplica primero $x$, y como `A @ B` no es `B @ A`, el orden de escritura es el orden (al revés) de aplicación.
        La misma línea de la lección II, `nube @ R.T`, gira un terreno $N\times3$ entero.
        """),
        mo.md("```python\nA, B = lib.rot_x(0.3), lib.rot_z(0.5)\nnp.allclose(A @ B, B @ A)                # False: el orden importa\nterreno_despues = terreno @ R.T          # (49, 3) → (49, 3)\n```"),
        mo.md(f"`np.allclose(A @ B, B @ A)` = `{bool(np.allclose(_a @ _b, _b @ _a))}` · `np.linalg.norm(A @ B - B @ A)` = `{np.linalg.norm(_a @ _b - _b @ _a):.4f}`  \n"
              f"`terreno.shape` = `{terreno.shape}` → `{terreno_despues.shape}`; primera fila antes `{np.round(terreno[0], 3).tolist()}`, después `{np.round(terreno_despues[0], 3).tolist()}` (mismo largo: `{np.linalg.norm(terreno[0]):.4f}` y `{np.linalg.norm(terreno_despues[0]):.4f}`)."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("Las rotaciones son matrices ortogonales con determinante mayor a 0").* Escribí
        $R_z(90°)$ con números y aplicala a $(1, 2, 3)$. Verificá que la tercera coordenada no cambia, que el largo
        tampoco, y que $R_z(90°)$ aplicada dos veces es $R_z(180°) = \mathrm{diag}(-1, -1, 1)$.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $R_z(90°) = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 1 \end{pmatrix}$, $R_z(90°)(1,2,3) = (-2, 1, 3)$:
        la $z$ queda, el plano $(x, y)$ gira como en 2D. Largo: $\sqrt{1+4+9} = \sqrt{4+1+9} = \sqrt{14}$. ✓
        $R_z(90°)^2$: $e_x \to e_y \to -e_x$, $e_y \to -e_x \to -e_y$, $e_z$ queda: $\mathrm{diag}(-1,-1,1)$. ✓
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_b = mo.ui.code_editor(
        value="R = ...                       # Rz(90°) · Ry(90°), en radianes\nimagen = R @ np.array([1.0, 0.0, 0.0])\nu = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)\nfijo = ...                    # np.allclose(...)\n",
        language="python",
        min_height=140,
        label="ejercicio (b)",
    )
    mo.vstack([
        mo.md(r"""
        **(b) Código con hueco — avanzado** *("Combinación de rotaciones son rotaciones"; el eje como dirección que queda
        fija, que en la clase 6 va a ser "autovector de autovalor 1").* Armá $R = R_z(90°)\,R_y(90°)$ (primero gira
        alrededor de $y$, después alrededor de $z$), aplicala a $(1, 0, 0)$ y verificá que $u = (-1, 1, 1)/\sqrt3$ queda
        fijo: `np.allclose(R @ u, u)`. Tenés `np`, `rot_x`, `rot_y`, `rot_z`. Para el cuaderno: ¿por qué $R$ **tiene**
        que dejar quieta alguna dirección?
        """),
        editor_b,
    ])
    return (editor_b,)


@app.cell
def _(editor_b, lib, mo, np):
    _R_ref = lib.rot_z(np.pi / 2) @ lib.rot_y(np.pi / 2)
    _u = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    _ns = {"np": np, "rot_x": lib.rot_x, "rot_y": lib.rot_y, "rot_z": lib.rot_z}
    try:
        exec(editor_b.value, _ns)
        _R = np.asarray(_ns["R"], dtype=float)
        _imagen = np.asarray(_ns["imagen"], dtype=float)
        _fijo = _ns["fijo"]
        if _R.shape != (3, 3):
            _res = mo.callout(mo.md(f"❌ `R` tiene forma `{_R.shape}`; tiene que ser `(3, 3)`."), kind="danger")
        elif np.allclose(_R, lib.rot_y(np.pi / 2) @ lib.rot_z(np.pi / 2)):
            _res = mo.callout(mo.md("❌ armaste $R_y R_z$: ese orden aplica primero $z$. La matriz de la derecha actúa primero; "
                                    "$R_z(90°) R_y(90°)$ es `rot_z(...) @ rot_y(...)`."), kind="warn")
        elif not np.allclose(_R, _R_ref):
            _res = mo.callout(mo.md(f"❌ `R` no es $R_z(90°)R_y(90°)$. ¿Pasaste los ángulos en radianes (`np.pi / 2`)? Primera columna esperada `[0, 0, -1]`, obtenida `{np.round(_R[:, 0], 3).tolist()}`."), kind="danger")
        elif not np.allclose(_imagen, [0, 0, -1]):
            _res = mo.callout(mo.md(f"❌ `R` está bien pero `imagen` = `{np.round(_imagen, 3).tolist()}`; $R\\,e_x$ es la primera columna, $(0, 0, -1)$."), kind="warn")
        elif _fijo is not True:
            _res = mo.callout(mo.md(f"❌ `R` e `imagen` están bien; `fijo` vale `{_fijo!r}`, tiene que ser `np.allclose(R @ u, u)` → `True`."), kind="warn")
        else:
            _res = mo.callout(mo.md(r"✅ $R = R_z(90°)R_y(90°)$ manda $e_x \mapsto (0,0,-1)$ y deja fijo $u = (-1,1,1)/\sqrt3$: ese es el eje de la "
                                    r"rotación compuesta, un giro de $120°$ ($R^3 = I$). En la clase 6, $Ru = u$ se lee \"$u$ es autovector de autovalor 1\". "
                                    r"Y la respuesta del cuaderno: $R$ es ortogonal con $\det = 1$, y toda matriz así deja fija una recta (Euler)."), kind="success")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré que los giros básicos no conmutan y que la composición deja un eje quieto. Las demostraciones:

    - [apunte, sección 7: rotaciones](../../apunte.pdf#nameddest=cap:07) (el orden importa, el ejemplo de $90°$)
    - [apunte, sección 14: $R_x, R_y, R_z$ por columnas y Rodrigues](../../apunte.pdf#nameddest=cap:14)
    - [apunte, sección 15: por qué el orden aparece recién en el segundo orden](../../apunte.pdf#nameddest=cap:15)
    - [ficha de la clase 1](../../clases/01.html) · [ficha de la clase 2](../../clases/02.html) · [lección anterior: Rotaciones II](../01b_rotacion_plano/index.html) · [el camino](../../index.html)

    **Lo que viene:** reflexiones y similaridades (clase 3): las ortogonales con $\det = -1$ y la escala. Ya disponible:
    [autovalores en 3D y puntos fijos proyectivos](../07c_autovalores_3d_puntos_fijos/index.html), donde el eje reaparece como
    autovector de autovalor $1$.
    """)
    return


@app.cell
def _(R, R_xyz, R_zyx, Ry90, Rz90, ang, candidatos, dist_ordenes, eje, ex, lib, mo, np, terreno, terreno_despues):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _Rd = Rz90 @ Ry90
    _u = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    _d = lambda e: np.linalg.norm(lib.rot_z(e) @ lib.rot_y(e) @ lib.rot_x(e) - lib.rot_x(e) @ lib.rot_y(e) @ lib.rot_z(e))
    _checks = [
        ("los cuatro candidatos de la predicción son distintos entre sí",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == len(candidatos)),
        ("Rz(90°)Ry(90°) e_x = (0, 0, −1) y Ry(90°)Rz(90°) e_x = (0, 1, 0)",
         lib.exacto(candidatos["correcta"], [0, 0, -1]) and lib.exacto(candidatos["otro-orden"], [0, 1, 0])),
        ("3.1: la matriz armada por columnas", lib.exacto(_Rd, [[0, -1, 0], [0, 0, 1], [-1, 0, 0]])),
        ("3.2: u es el eje, 120°, R³ = I y Rodrigues la reconstruye",
         lib.exacto(_Rd @ _u, _u) and lib.exacto(lib.eje_angulo(_Rd)[1], np.deg2rad(120)) and lib.exacto(np.linalg.matrix_power(_Rd, 3), np.eye(3))
         and lib.exacto(lib.rodrigues(_u, np.deg2rad(120)), _Rd)),
        ("cada giro básico deja quieto su eje y es ortogonal con det 1",
         all(lib.exacto(f(0.7) @ e, e) and lib.exacto(f(0.7).T @ f(0.7), np.eye(3)) and lib.exacto(np.linalg.det(f(0.7)), 1.0)
             for f, e in ((lib.rot_x, [1, 0, 0]), (lib.rot_y, [0, 1, 0]), (lib.rot_z, [0, 0, 1])))),
        ("sección 2: R es ortogonal con det 1 y deja fijo su eje", lib.exacto(R.T @ R, np.eye(3)) and lib.exacto(np.linalg.det(R), 1.0) and lib.exacto(R @ eje, eje, tol=1e-6)),
        ("sección 2: Rodrigues(eje, ángulo) reconstruye R", lib.exacto(lib.rodrigues(eje, ang), R, tol=1e-6)),
        ("sección 2: el número vivo es ‖R_xyz − R_zyx‖", lib.exacto(np.linalg.norm(R_xyz - R_zyx), dist_ordenes)),
        ("el terreno conserva los largos", terreno_despues.shape == terreno.shape == (49, 3)
         and lib.exacto(np.linalg.norm(terreno_despues, axis=1), np.linalg.norm(terreno, axis=1))),
        ("la no conmutatividad es de segundo orden (ε/10 → ~100 veces menos)", 50 < _d(0.1) / _d(0.01) < 200),
        ("ejercicio (a): Rz(90°)(1, 2, 3) = (−2, 1, 3) y Rz(90°)² = diag(−1, −1, 1)",
         lib.exacto(Rz90 @ [1, 2, 3], [-2, 1, 3]) and lib.exacto(Rz90 @ Rz90, np.diag([-1.0, -1.0, 1.0]))),
        ("ejercicio (b): la imagen de e_x es la primera columna", lib.exacto(_Rd @ ex, _Rd[:, 0])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
