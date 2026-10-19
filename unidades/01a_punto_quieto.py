# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Rotaciones I — el punto no se movió (unidad 01a, molde v2 sobre el módulo común cb104).

Sistemas de Coordenadas (CB104) · Agrimensura · FIUBA · Gustavo Varela.
Una sola idea: todo vector es un punto; si giramos los ejes, el punto (el mojón) se queda quieto y
lo que cambian son sus coordenadas (rotación pasiva). Girar el punto con los ejes quietos es la rotación activa, y una
es la transpuesta de la otra. La matriz R(θ) aparece recién al final, como la cuenta que hace lo que ya se vio.

Chequear:  uv run marimo check --select MW unidades/01a_punto_quieto.py
Exportar:  uv run python tools/build.py --only 01a_punto_quieto
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
    # Rotaciones I — el punto no se movió

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    La pregunta de esta lección es una sola: **si giramos los ejes 30°, ¿se mueve el mojón o se mueven
    sus coordenadas?** Lo que viene después (la matriz, qué conserva, el 3D) queda para las lecciones II y III.

    Código de colores, igual en la figura y en el álgebra: lo que estaba **antes** va en gris, lo que queda **después**
    en <span style="color:#1b6f6a">**teal**</span> (y <span style="color:#b5451b">**rust**</span> para el segundo eje),
    y el objeto que importa, el mojón, en <span style="color:#7a4e9e">**violeta**</span>. Ángulos en grados en los
    controles; adentro numpy trabaja en radianes. Giro positivo = antihorario.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("01a_punto_quieto"))
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0. Situación de campo y predicción

    Una parcela y, adentro, un **mojón** clavado en el terreno. En el sistema de la obra (origen en un vértice, eje $x$
    a lo largo del frente) el mojón es $P = (4, 3)$, en metros. Ahora plantamos un instrumento que mide ángulos y distancias
    en el mismo origen, pero mide **en sus propios ejes**: su eje $x$ apunta $30°$ a la izquierda del frente. El mojón
    no se tocó; es el mismo pedazo de hierro.

    La pregunta de campo es la de siempre en este oficio: las lecturas de la estación hay que pasarlas al sistema de
    la parcela, y al revés. Antes de ver cómo, una predicción.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- los números de la predicción salen de acá, nunca a mano ----------
    mojon = np.array([4.0, 3.0])
    R30 = lib.rot2(np.deg2rad(30))
    candidatos = {
        "pasiva": R30.T @ mojon,  # giran los ejes +30°, el mojón queda: coordenadas nuevas = R(30°)ᵀ P = R(−30°) P
        "activa": R30 @ mojon,  # gira el mojón +30°, los ejes quedan
        "reflexion": np.diag([1.0, -1.0]) @ mojon,  # espejo respecto del eje x
        "mismas": mojon.copy(),
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            lib.vec_plano(candidatos["activa"]): "activa",
            lib.vec_plano(candidatos["mismas"]) + "  (las mismas)": "mismas",
            lib.vec_plano(candidatos["pasiva"]): "pasiva",
            lib.vec_plano(candidatos["reflexion"]): "reflexion",
        }),
        value=None,
        label=r"**Predicción.** Los ejes de la estación están girados $30°$ antihorario respecto de los de la obra y el "
        r"mojón $P = (4, 3)$ se queda quieto. Las coordenadas que lee la estación son…",
    )
    prediccion
    return R30, candidatos, mojon, prediccion


@app.cell
def _(candidatos, lib, mo, prediccion):
    _a, _p, _r = (lib.vec_tex(candidatos[k]) for k in ("activa", "pasiva", "reflexion"))
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "activa": ("warn",
                   rf"**No.** ${_a}$ son las coordenadas del **mojón girado** $30°$ con los ejes quietos: giraste el punto, "
                   r"no los ejes. Cuando los ejes giran $+30°$ y el punto queda, los números cambian como si el punto hubiera "
                   r"girado $-30°$. En la sección 2 se ve: el mojón no se mueve, la grilla teal sí."),
        "mismas": ("warn",
                   r"**No.** El mojón no se movió, pero una coordenada es un número **respecto de unos ejes**. Si los ejes "
                   r"giran, los números cambian aunque el punto no. Si no cambiaran, la estación y la obra dirían lo mismo, "
                   r"y no lo dicen: por eso hay que transformar las lecturas."),
        "reflexion": ("warn",
                      rf"**No.** ${_r}$ es el mojón **reflejado** respecto del eje $x$: cambia el signo de una sola coordenada, "
                      r"que es lo que hace un espejo, no un giro. Un giro **mezcla** las dos coordenadas: las dos nuevas dependen "
                      r"de las dos viejas."),
        "pasiva": ("success",
                   rf"**Sí.** El mojón queda y los ejes giran $30°$: la estación lee ${_p}$, como si el punto hubiera girado "
                   r"$-30°$. Eso es lo que muestra la lección: con los ejes girados $\theta$, las coordenadas nuevas se leen "
                   r"proyectando el mismo punto sobre los ejes nuevos. La cuenta que lo hace aparece recién en la sección 3."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Todo vector es un punto.** El mojón es un lugar del terreno; $(4, 3)$ es su **etiqueta** en unos ejes. Cambiá los
    ejes y cambia la etiqueta, no el lugar. Con la soga lo vemos: la geometría no exige coordenadas;
    las coordenadas son algo que le ponemos por comodidad.

    Hay dos maneras de girar, y conviene tenerlas separadas desde el principio:

    - **Pasiva:** giran los ejes $\theta$, el punto queda. Cambian los números. Es lo que hace el instrumento.
    - **Activa:** giran los puntos $\theta$, los ejes quedan. Cambia el lugar. Es lo que hace un plano al rotarlo.

    Lo que se ve en la figura de abajo: girar los ejes $+\theta$ y leer, da los mismos números que girar el punto
    $-\theta$ y leer en los ejes viejos. **Una es la inversa de la otra**, y para una rotación la inversa es la
    transpuesta (eso lo verificamos en la sección 3; la demostración está en el apunte, «Rotaciones»).

    | | ¿qué podemos girar? | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | nada: en una recta el único "giro" es dar vuelta la regla, $x \mapsto -x$ | el mojón queda; cambia el signo de su número |
    | $\mathbb R^2$ | los dos ejes a la vez, un ángulo $\theta$ | el mojón queda; sus dos números se mezclan con senos y cosenos |
    | $\mathbb R^3$ | hace falta decir **alrededor de qué eje** | lección III: tres giros básicos, y el orden importa |
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Manipulación

    Tres capas. En **gris**, la grilla de la obra (los ejes de antes). En **teal**, la grilla de la estación: los mismos
    ejes girados $\theta$, con el eje $x'$ en teal y el eje $y'$ en rust. En **violeta**, el mojón, que no se mueve, y el
    **camino de lectura**: para leer sus coordenadas en los ejes nuevos avanzamos por $x'$ y después paralelo a $y'$.
    Los dos tramos de ese camino son los dos números que anota la estación.

    Movelo: cambiá $\theta$ y mirá que el punto queda clavado mientras los números cambian. Cambiá el punto y mirá qué
    pasa con uno que está sobre el eje $x'$ (su segunda coordenada nueva es $0$). Apretá **reproducir** para ver los
    ejes girar de $0$ a $\theta$.
    """)
    return


@app.cell
def _(mo):
    angulo = mo.ui.slider(-180, 180, value=30, step=1, label="θ (°): giro de los ejes", show_value=True)
    px = mo.ui.slider(-5, 5, value=4.0, step=0.5, label="x del mojón (ejes de la obra)", show_value=True)
    py = mo.ui.slider(-5, 5, value=3.0, step=0.5, label="y del mojón (ejes de la obra)", show_value=True)
    return angulo, px, py


@app.cell
def _(angulo, go, lib, mo, np, px, py):
    rango = 5
    theta = np.deg2rad(angulo.value)
    P = np.array([px.value, py.value])
    R = lib.rot2(theta)  # columnas: los ejes girados x′ (teal) e y′ (rust)
    coords_nuevas = lib.coordenadas_en_base(P, R)  # = Rᵀ P: lo que lee la estación
    camino = [lib.rot2(t) for t in np.linspace(0, theta, 36)]

    def _dinamicas(i):
        """Las trazas que cambian con el cuadro i: grilla girada, los dos ejes nuevos y el camino de lectura."""
        Mi = camino[i]
        f = go.Figure()
        lib.capa_despues(f, Mi, rango, cuadrado=False, columnas=False)
        lib.flecha(f, (0, 0), 2 * Mi[:, 0], lib.COLORES[0], "eje x′ (girado)")
        lib.flecha(f, (0, 0), 2 * Mi[:, 1], lib.COLORES[1], "eje y′ (girado)")
        lib.lectura_coordenadas(f, P, Mi)
        return list(f.data)

    figura = lib.figura_plano(rango + 1, f"ejes girados θ = {angulo.value}° · el mojón no se mueve")
    lib.capa_antes(figura, rango, cuadrado=False)
    lib.flecha(figura, (0, 0), (2, 0), lib.GRIS_ANTES, "eje x (obra)", ancho=3)
    lib.flecha(figura, (0, 0), (0, 2), lib.GRIS_ANTES, "eje y (obra)", ancho=3)
    _n_est = len(figura.data)
    _din = _dinamicas(len(camino) - 1)
    for _t in _din:
        figura.add_trace(_t)
    lib.punto(figura, P, nombre="mojón (quieto)", texto="P")  # último: queda arriba de la grilla
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))], indices=list(range(_n_est, _n_est + len(_din))))

    _panel = mo.vstack([
        mo.md("**Controles**"),
        angulo, px, py,
        mo.md(rf"""
        **Números vivos**

        - el mojón, en los ejes de la obra: $P = {lib.vec_tex(P)}$ (no cambia con $\theta$)
        - el mismo mojón, leído en los ejes girados: $\mathbf{{{lib.vec_tex(coords_nuevas)}}}$
        - distancia al origen: antes ${lib.num_tex(np.linalg.norm(P))}$, después ${lib.num_tex(np.linalg.norm(coords_nuevas))}$

        Las dos lecturas son etiquetas del **mismo lugar**. Lo que se conserva es la distancia al origen (y, en
        general, toda distancia y todo ángulo: lección II).
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return P, R, coords_nuevas, theta


@app.cell
def _(R30, go, lib, mo, mojon, np):
    # ---------- la cuenta que hace lo que se acaba de ver: recién ahora aparece la matriz ----------
    _c, _s = np.cos(np.deg2rad(30)), np.sin(np.deg2rad(30))
    _lect = R30.T @ mojon
    _f = lib.figura_plano(1.4, "las columnas de R(30°) son los ejes girados", ancho=300, alto=300)
    _f.update_layout(margin=dict(l=20, r=10, t=40, b=20), showlegend=False)
    lib.flecha(_f, (0, 0), (1, 0), lib.GRIS_ANTES, "", ancho=3)
    lib.flecha(_f, (0, 0), (0, 1), lib.GRIS_ANTES, "", ancho=3)
    lib.flechas_columnas(_f, R30, "R")
    mo.vstack([
        mo.md(r"""
        ## 3. La cuenta que hace lo que acabás de ver

        Recién ahora, la matriz. Los dos ejes girados son dos flechas de largo $1$; si las ponemos como **columnas** de
        una matriz, la primera columna es el eje $x'$ (teal) y la segunda el eje $y'$ (rust):
        """),
        mo.hstack([
            mo.md(rf"""

            $$R(\theta) = \begin{{pmatrix}} \textcolor{{#1b6f6a}}{{\cos\theta}} & \textcolor{{#b5451b}}{{-\sin\theta}} \\
            \textcolor{{#1b6f6a}}{{\sin\theta}} & \textcolor{{#b5451b}}{{\cos\theta}} \end{{pmatrix}}, \qquad
            R(30°) = {lib.matriz_coloreada(R30)}$$

            La coordenada nueva $x'$ es "cuánto de $P$ cae sobre el eje $x'$": el producto interno de $P$ con la
            primera columna. Igual $y'$ con la segunda. Las dos cuentas juntas son **$R^T$ por $P$** (las columnas
            pasan a ser filas):

            $$\begin{{pmatrix}} x' \\ y' \end{{pmatrix}} = R(30°)^T \begin{{pmatrix}} 4 \\ 3 \end{{pmatrix}}
            = \begin{{pmatrix}} 4\cos30° + 3\sin30° \\ -4\sin30° + 3\cos30° \end{{pmatrix}}
            = \begin{{pmatrix}} 4\cdot{lib.num_tex(_c)} + 3\cdot{lib.num_tex(_s)} \\ -4\cdot{lib.num_tex(_s)} + 3\cdot{lib.num_tex(_c)} \end{{pmatrix}}
            = {lib.pmat(_lect.reshape(2, 1))}.$$

            Y la otra manera de girar, la **activa**, es $R(\theta)\,P$ sin transponer: mueve el punto $+\theta$. Como
            $R(\theta)^T = R(-\theta)$ (cambiá el signo del seno y fijate), **pasiva con $+\theta$ = activa con $-\theta$**.
            """),
            mo.vstack([
                mo.ui.plotly(_f),
                mo.md("```python\nR = lib.rot2(np.deg2rad(30))\nP = np.array([4.0, 3.0])\nR.T @ P   # pasiva: lo que lee la estación\nR @ P     # activa: el punto girado\n```"),
                mo.md(f"`R.T @ P` = `{np.round(_lect, 3).tolist()}`  \n`R @ P` = `{np.round(R30 @ mojon, 3).tolist()}`  \n"
                      f"`np.allclose(R.T, lib.rot2(np.deg2rad(-30)))` = `{bool(np.allclose(R30.T, lib.rot2(np.deg2rad(-30))))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(lib, mo, np):
    _R = lib.rot2(np.deg2rad(30))
    _P = np.array([4.0, 3.0])
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **grados en la interfaz, radianes adentro**, y `.T` transpone. `np.deg2rad(30)` convierte;
        `R.T` es la matriz con filas y columnas intercambiadas; `@` multiplica. Un punto es un array de dos números y
        `R.T @ P` es un punto nuevo del mismo tamaño.
        """),
        mo.md("```python\ntheta = np.deg2rad(30)        # 0.5236 rad\nR = lib.rot2(theta)\nP = np.array([4.0, 3.0])\nR.T @ P                       # shape (2,)\n```"),
        mo.md(f"`theta` = `{np.deg2rad(30):.4f}` · `R.T` =\n```\n{np.round(_R.T, 3)}\n```\n`R.T @ P` = `{np.round(_R.T @ _P, 3).tolist()}` · `(R.T @ P).shape` = `{(_R.T @ _P).shape}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *Idea central: las matrices y las transformaciones lineales tienen una correspondencia 1 a 1.*
        El mojón está en $(2, 0)$ y la estación tiene sus ejes girados $90°$ antihorario. Sin matriz, con un dibujo:
        ¿qué lee la estación? Después hacé la cuenta $R(90°)^T\binom{2}{0}$ y comprobá que da lo mismo.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        Con los ejes girados $90°$, el eje $x'$ apunta hacia $+y$ y el eje $y'$ hacia $-x$. El mojón $(2,0)$ está sobre
        el eje $-y'$, a distancia $2$: la estación lee $(0, -2)$.
        $R(90°)^T = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$, y $R(90°)^T\binom{2}{0} = \binom{0\cdot2 + 1\cdot0}{-1\cdot2 + 0\cdot0} = \binom{0}{-2}$. ✓
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_b = mo.ui.code_editor(
        value="def lectura(p, theta_grados):\n    theta = ...                     # a radianes\n    c, s = np.cos(theta), np.sin(theta)\n    R = np.array([[c, -s], [s, c]])\n    return ...                      # lo que lee la estación con los ejes girados theta\n",
        language="python",
        min_height=150,
        label="ejercicio (b)",
    )
    mo.vstack([
        mo.md(r"""
        **(b) Código con hueco — medio** *Idea central: hay transformaciones que se definen completamente por qué propiedades de los
        objetos transformados mantienen.* Completá `lectura(p, theta_grados)`: recibe un punto (array de 2) en los ejes
        de la obra y el giro de los ejes de la estación **en grados**, y devuelve lo que lee la estación. Tenés `np`.
        Se verifica con `np.allclose` contra la referencia en 20 puntos al azar.
        """),
        editor_b,
    ])
    return (editor_b,)


@app.cell
def _(editor_b, lib, mo, np):
    _rng = np.random.default_rng(0xDDDE)
    _puntos = _rng.uniform(-5, 5, size=(20, 2))
    _grados = 37.0
    _R = lib.rot2(np.deg2rad(_grados))
    _esperado = lib.transformar(_puntos, _R.T)
    _ns = {"np": np}
    try:
        exec(editor_b.value, _ns)
        _obtenido = np.array([_ns["lectura"](p, _grados) for p in _puntos], dtype=float)
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ para un punto devolvés algo de forma `{_obtenido.shape[1:]}`; tiene que ser `(2,)`."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide con la referencia en los 20 puntos (θ = 37°): giraste los ejes, no el punto."), kind="success")
        elif np.allclose(_obtenido, lib.transformar(_puntos, _R)):
            _res = mo.callout(mo.md("❌ devolvés `R @ p`: ese es el **punto girado** (activa). La estación lee con los ejes girados: `R.T @ p`."), kind="warn")
        elif np.allclose(_obtenido, lib.transformar(_puntos, lib.rot2(_grados).T)):
            _res = mo.callout(mo.md("❌ usaste los grados como si fueran radianes. Falta `np.deg2rad(theta_grados)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para `{np.round(_puntos[0], 3).tolist()}` se esperaba `{np.round(_esperado[0], 3).tolist()}` y se obtuvo `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "01a_punto_quieto")
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

    En esta unidad demostramos que el punto no se mueve y que las coordenadas nuevas son $R^T P$. La demostración de que la inversa de
    una rotación es su transpuesta (y por qué) está en el apunte:

    - [apunte, «Rotaciones» (rotaciones)](../../apunte.pdf#nameddest=cap:rotaciones)
    - [ficha del capítulo 1](../../capitulos/01.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** [Rotaciones II — la rotación en el plano](../01b_rotacion_plano/index.html): qué conserva
    $R(\theta)$, por qué sus columnas son "a dónde van $e_1$ y $e_2$", y el mismo giro escrito como número complejo.
    """)
    return


@app.cell
def _(P, R, R30, candidatos, coords_nuevas, lib, mo, mojon, np, theta):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _checks = [
        ("los cuatro candidatos de la predicción son distintos entre sí",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == len(candidatos)),
        ("pasiva = R(30°)ᵀ P = R(−30°) P", lib.exacto(candidatos["pasiva"], lib.rot2(np.deg2rad(-30)) @ mojon)),
        ("activa = R(30°) P", lib.exacto(candidatos["activa"], R30 @ mojon)),
        ("sección 3: R(30°)ᵀ (4, 3) a mano", lib.exacto(R30.T @ mojon, [4 * np.cos(np.pi / 6) + 1.5, -2 + 3 * np.cos(np.pi / 6)])),
        ("la lectura en los ejes girados es Rᵀ P", lib.exacto(coords_nuevas, R.T @ P)),
        ("Rᵀ = R(−θ) para el θ del deslizador", lib.exacto(R.T, lib.rot2(-theta))),
        ("la distancia al origen no cambia", lib.exacto(np.linalg.norm(coords_nuevas), np.linalg.norm(P), tol=1e-9)),
        ("ejercicio (a): R(90°)ᵀ (2, 0) = (0, −2)", lib.exacto(lib.rot2(np.pi / 2).T @ [2, 0], [0, -2])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
