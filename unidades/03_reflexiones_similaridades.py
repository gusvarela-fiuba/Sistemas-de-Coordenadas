# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Reflexiones y similaridades (unidad 03, molde v2 sobre cb104). Clase 3, reconstruida: sin transcripción.

Una sola idea: la reflexión (det = −1) conserva todo pero da vuelta la orientación, y dos seguidas son una rotación;
la similaridad k·R(θ) x + t conserva forma y ángulos, escala todo por k y tiene un centro fijo: con dos puntos se
superpone un plano viejo sobre el relevamiento. Menciona homotecia, trayectoria y líneas coordenadas (clase 2).

Chequear:  uv run marimo check --select MW unidades/03_reflexiones_similaridades.py
Exportar:  uv run python tools/build.py --only 03_reflexiones_similaridades
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
    # Reflexiones y similaridades

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Seguimos la clase 3. *La clase 3 no tiene transcripción: esta lección está reconstruida desde el esqueleto 2025 del
    profesor, la guía de seis teoremas y el apunte.* La pregunta: **¿qué movimiento conserva la forma pero no el
    tamaño, y cuál da vuelta la orientación?** El gancho: *un plano viejo en otra escala y con el norte para otro lado
    hay que superponerlo sobre el relevamiento nuevo.*

    Entre [Rotaciones II](../01b_rotacion_plano/index.html) y la [afinidad general](../04_afines_homogeneas/index.html)
    hay dos movimientos con nombre: la **reflexión** y la **similaridad**. Colores, iguales en la figura y en el álgebra:
    **primera columna** <span style="color:#1b6f6a">**teal**</span>, **segunda** <span style="color:#b5451b">**rust**</span>,
    corrimiento y centro en <span style="color:#c9a227">**gold**</span>; la parcela en <span style="color:#7a4e9e">**violeta**</span>.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("03_reflexiones_similaridades"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación: los números salen de acá, nunca a mano ----------
    P_viejo = np.array([[1.0, 2.0], [4.0, 1.0], [2.0, 4.0]])  # tres mojones leídos en el plano viejo (cm de papel)
    Q_nuevo = np.array([[2.0, 1.0], [6.0, 3.0]])  # los dos primeros, medidos en el relevamiento nuevo (m)
    A_sit, t_sit = lib.similaridad_por_dos_puntos(P_viejo[0], P_viejo[1], Q_nuevo[0], Q_nuevo[1])
    k_sit, th_sit = lib.partes_similaridad(A_sit)
    centro_sit = lib.centro_fijo(A_sit, t_sit)
    d_viejo = float(np.linalg.norm(P_viejo[1] - P_viejo[0]))
    d_nuevo = float(np.linalg.norm(Q_nuevo[1] - Q_nuevo[0]))
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            "Una rotación más un corrimiento: con un mojón alcanza, las distancias no cambian.": "rotacion",
            "Una similaridad: giro, cambio de escala y corrimiento; con los dos mojones alcanza.": "correcta",
            "Una reflexión: si el norte está para otro lado hay que dar vuelta el plano.": "reflexion",
            "Una afinidad cualquiera: hacen falta tres mojones, como en la unidad 04.": "afinidad",
        }),
        value=None,
        label="**Predicción.** ¿Qué transformación superpone el plano viejo sobre el relevamiento, y con cuántos mojones?",
    )
    mo.vstack([
        mo.md(rf"""
        ## 0. Situación de campo y predicción

        Tenemos un **plano viejo** de la parcela, a otra escala y con el norte para otro lado, y el **relevamiento
        nuevo** en metros. El plano viejo está bien dibujado, con regla y transportador: los ángulos son los del terreno
        y todas las distancias están reducidas por el mismo factor.

        Dos mojones aparecen en los dos: en el plano viejo los leemos en ${lib.vec_tex(P_viejo[0])}$ y
        ${lib.vec_tex(P_viejo[1])}$; en el relevamiento están en ${lib.vec_tex(Q_nuevo[0])}$ y ${lib.vec_tex(Q_nuevo[1])}$.
        Distan $\sqrt{{10}} \approx {d_viejo:.2f}$ en el papel y $\sqrt{{20}} \approx {d_nuevo:.2f}$ en el terreno. Un tercer
        mojón, ${lib.vec_tex(P_viejo[2])}$ en el plano viejo, todavía no lo medimos.
        """),
        prediccion,
    ])
    return A_sit, P_viejo, Q_nuevo, centro_sit, d_nuevo, d_viejo, k_sit, prediccion, t_sit, th_sit


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Girar, escalar por un mismo factor y correr son cuatro números ($k$, $\theta$ y el corrimiento); cada "
                     r"mojón conocido en los dos planos da dos ecuaciones. Dos alcanzan y el tercero controla. En la sección 3 lo "
                     r"calculamos con un solo número complejo."),
        "rotacion": ("warn",
                     r"**No.** Un giro más un corrimiento conserva las distancias, pero los mojones distan $\sqrt{10}$ en el papel y "
                     r"$\sqrt{20}$ en el terreno: la escala cambió. Y con un solo mojón no sabríamos cuánto girar. Falta el factor $k$: "
                     r"el escalón que separa la rotación de la similaridad."),
        "reflexion": ("warn",
                      r"**No.** Que el norte apunte para otro lado es un **giro**, no un espejo. Un espejo daría vuelta la parcela como "
                      r"un guante: los vértices irían antihorario en el terreno y horario en el plano. Un plano dibujado mirando el "
                      r"terreno desde arriba no hace eso; en la sección 2 el área con signo lo delata."),
        "afinidad": ("warn",
                     r"**No es la mejor.** Con tres mojones y la receta de la unidad 04 sale una afinidad que pasa exacto por los tres, "
                     r"pero cualquier error de lectura entra como un estiramiento distinto en cada eje, que el plano no tiene. Si los "
                     r"ángulos se conservan hay sólo cuatro incógnitas: dos mojones, y el tercero controla."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **La reflexión conserva todo y da vuelta la hoja.** Elegimos una recta como espejo; cada punto va al otro lado, sobre
    su perpendicular, a la misma distancia. Distancias y ángulos quedan iguales, pero lo que iba antihorario ahora va
    horario: $\det = -1$. Hacerla dos veces devuelve cada punto a su lugar: es su propia inversa. Y **dos espejos
    seguidos** respecto de rectas que se cortan en $o$ son una **rotación** alrededor de $o$ por el doble del ángulo
    entre ellas (muestra en la sección 2; demostración en el apunte, «Guía resuelta: reflexión respecto de un punto», teorema 4).

    **La similaridad conserva la forma, no el tamaño.** Gira $\theta$, multiplica **todas** las longitudes por un mismo
    $k$ y corre $t$: $S(x) = k\,R(\theta)\,x + t$. Conserva ángulos y **razones** de distancias; el área va $\times k^2$.
    Si $k \neq 1$ tiene un único punto quieto, el **centro** $c$, solución de $(I - A)\,c = t$; con el origen en $c$ es
    sólo girar y escalar (apunte, «Composición afín práctica: rotación y escala»). Con $\theta = 0$ es una **homotecia**: todo se agranda desde el centro, sobre rayos.

    | | reflexión | similaridad |
    |---|---|---|
    | $\mathbb R$ | $x \mapsto -x$: el espejo es el $0$ | $x \mapsto kx + b$: estirar y correr |
    | $\mathbb R^2$ | $H(\alpha) = \begin{pmatrix} \textcolor{#1b6f6a}{\cos 2\alpha} & \textcolor{#b5451b}{\sin 2\alpha} \\ \textcolor{#1b6f6a}{\sin 2\alpha} & \textcolor{#b5451b}{-\cos 2\alpha} \end{pmatrix}$, espejo de ángulo $\alpha$ | $k\,R(\theta)\,x + t$, $\det = k^2$ |
    | $\mathbb R^3$ | espejo respecto de un **plano**: $\mathrm{diag}(1, 1, -1)$ para el plano $xy$ | $k\,R\,x + t$, $R$ una rotación 3D |

    Las columnas de $H(\alpha)$ son a dónde van $e_1$ y $e_2$: $e_1$ está a $\alpha$ de un lado del espejo y cae a
    $\alpha$ del otro, al ángulo $2\alpha$. Demostración en el apunte, secciones 8 y 9.

    **Qué conserva cada escalón** (cada uno suelta un invariante y gana transformaciones):

    | | distancias | ángulos | orientación | razones de distancias | paralelas | área |
    |---|---|---|---|---|---|---|
    | rotación (01b) | sí | sí | sí | sí | sí | $\times 1$ |
    | reflexión | sí | sí | **no** | sí | sí | $\times (-1)$ |
    | similaridad | **no** | sí | sí (directa) | sí | sí | $\times k^2$ |
    | afinidad (04) | no | **no** | según $\det$ | sólo sobre cada recta | sí | $\times \det A$ |
    """)
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (tipo, ángulo fijo, deslizadores (lo, hi, paso, valor, etiqueta), qué pasa) ----------
    _k_th = [(0.3, 2.0, 0.1, 1.4, "k"), (-180, 180, 1, 45, "θ (°)")]
    casos = {
        "espejo del eje x": ("reflexion", 0, [], r"$H(0°) = \mathrm{diag}(1, -1)$: distancias iguales, orientación al revés, $\det = -1$."),
        "espejo de la diagonal y = x": ("reflexion", 45, [], r"$H(45°)$ intercambia las coordenadas, $(x, y) \mapsto (y, x)$; $\det = -1$."),
        "espejo de la recta de ángulo α": ("reflexion", None, [(-90, 90, 1, 30, "α (°)")], r"la recta queda fija punto a punto; $e_1$ va al ángulo $2\alpha$; $H\,H = I$."),
        "dos espejos seguidos: eje x y después recta de ángulo β": ("dos", None, [(-90, 90, 1, 30, "β (°)")],
                                                                    r"dos espejos devuelven la orientación: es $R(2\beta)$, $\det = +1$. Reproducir muestra las dos etapas."),
        "similaridad k·R(θ) con centro en el origen": ("sim", None, _k_th, r"misma forma, otro tamaño: ángulos iguales, longitudes $\times k$, área $\times k^2$."),
        "similaridad con centro: k·R(θ) x + (3, −2), la del plano viejo": ("sim-centro", None, _k_th,
                                                                          r"el corrimiento no es el centro: el centro $c$ (gold) es el punto que $S$ deja quieto."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="espejo de la recta de ángulo α", label="caso precargado")
    rango = 6
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # la misma de Rotaciones II
    mo.md(r"""
    ## 2. Manipulación

    Tres capas: **gris**, grilla y cuadrado unitario antes; **teal**, los mismos después, con las columnas de la
    matriz como flechas; **violeta**, la parcela con estelas. En los espejos dibujamos la recta espejo (a rayas); en la
    similaridad con centro, el centro fijo en gold. Mirá el **área con signo**: cambia de signo con un espejo, vuelve
    a ser positiva con dos, y va $\times k^2$ con la similaridad. A la derecha de la figura, el panel con el caso,
    los deslizadores y los números vivos.
    """)
    return caso, casos, parcela, rango


@app.cell
def _(caso, casos, mo):
    _specs = casos[caso.value][2]
    params = mo.ui.array([mo.ui.slider(lo, hi, value=v, step=paso, label=etq, show_value=True) for lo, hi, paso, v, etq in _specs]
                         or [mo.ui.slider(0, 1, value=0, step=1, label="(sin parámetro)", disabled=True)])
    n_pasos = mo.ui.slider(1, 16, value=8, step=1, label="n (repeticiones)", show_value=True)
    return n_pasos, params


@app.cell
def _(caso, casos, go, lib, mo, np, params, parcela, rango, t_sit):
    _tipo, _dato, _, que_pasa = casos[caso.value]
    _v = [float(x) for x in params.value]
    _I = np.eye(2)
    t_M = np.zeros(2)
    espejos = []
    if _tipo == "reflexion":
        _alpha = np.deg2rad(_dato if _dato is not None else _v[0])
        M = lib.reflexion2(_alpha)
        espejos = [_alpha]
        camino = [(_I + u * (M - _I), t_M) for u in np.linspace(0, 1, 36)]
    elif _tipo == "dos":
        _beta = np.deg2rad(_v[0])
        _H0 = lib.reflexion2(0.0)
        M = lib.reflexion2(_beta) @ _H0
        espejos = [0.0, _beta]
        camino = [(_I + u * (_H0 - _I), t_M) for u in np.linspace(0, 1, 18)] + [(_H0 + u * (M - _H0), t_M) for u in np.linspace(0, 1, 18)]
    else:
        _k, _th = _v[0], np.deg2rad(_v[1])
        M, t_M = lib.similaridad(_k, _th, t_sit if _tipo == "sim-centro" else (0, 0))
        camino = [lib.similaridad(1 + u * (_k - 1), u * _th, u * t_M) for u in np.linspace(0, 1, 36)]
    con_t = _tipo == "sim-centro"
    centro = lib.centro_fijo(M, t_M) if con_t else None

    def _dinamicas(i):
        Ai, ti = camino[i]
        f = go.Figure()
        lib.capa_despues_afin(f, Ai, ti, rango) if con_t else lib.capa_despues(f, Ai, rango)
        lib.objeto(f, lib.transformar_afin(parcela, Ai, ti), lib.VIOLETA_OBJETO, "parcela después",
                   estelas=lib.estelas_afin(parcela[[1, 2, 3]], camino[: i + 1]))
        return list(f.data)

    figura = lib.figura_plano(rango + 1, caso.value)
    lib.capa_antes(figura, rango)
    lib.objeto(figura, parcela, lib.GRIS_ANTES, "parcela antes", relleno=False)
    for _j, _a in enumerate(espejos):
        _d = np.array([np.cos(_a), np.sin(_a)]) * (rango + 1)
        figura.add_trace(go.Scatter(x=[-_d[0], _d[0]], y=[-_d[1], _d[1]], mode="lines", name=f"espejo {_j + 1}", line=dict(color="#444", width=1.5, dash="dash"), hoverinfo="skip"))
    if centro is not None:
        lib.punto(figura, centro, lib.COLORES[2], "centro fijo", texto="c")
    for _tr in _dinamicas(len(camino) - 1):
        figura.add_trace(_tr)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    area_antes = lib.area_poligono(parcela)
    area_despues = lib.area_poligono(lib.transformar_afin(parcela, M, t_M))
    if _tipo in ("reflexion", "dos"):
        _extra = rf"- $M\,M = I$: `{bool(np.allclose(M @ M, _I))}` · $M^TM = I$: `{bool(np.allclose(M.T @ M, _I))}`"
    elif centro is not None:
        _extra = rf"- centro fijo $c = {lib.vec_tex(centro)}$; $S(c) = {lib.vec_tex(M @ centro + t_M)}$"
    else:
        _extra = r"- traslación pura, **sin centro**" if con_t else r"- el centro es el origen: $S(0) = 0$"
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, mo.vstack(params.elements),
        mo.md(rf"""
        **Números vivos**

        - $\det = \mathbf{{{lib.num_tex(np.linalg.det(M), 3)}}}$; área con signo de la parcela: antes ${lib.num_tex(area_antes, 2)}$, después $\mathbf{{{lib.num_tex(area_despues, 3)}}}$
        - el vértice $(4, 1)$ va a ${lib.vec_tex(M @ [4, 1] + t_M)}$
        {_extra}

        $$M = {lib.matriz_coloreada(M)}{(r",\quad t = " + lib.vec_tex(t_M)) if con_t else ""}$$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, area_antes, area_despues, centro, t_M


@app.cell
def _(go, lib, mo, n_pasos, np):
    # ---------- trayectorias: qué dibuja un punto cuando repito la transformación ----------
    p0 = np.array([3.0, 0.0])
    _n = n_pasos.value
    tray_R = lib.trayectoria(lib.rot2(np.deg2rad(30)), [0, 0], p0, _n)
    tray_H = lib.trayectoria(0.85 * np.eye(2), [0, 0], p0, _n)
    tray_S = lib.trayectoria(0.85 * lib.rot2(np.deg2rad(30)), [0, 0], p0, _n)
    fig_t = lib.figura_plano(3.6, "trayectorias: rotación, homotecia y similaridad repetidas")
    for _tr, _col, _nom in ((tray_R, lib.COLORES[0], "R(30°) repetida: círculo"), (tray_H, lib.COLORES[2], "0.85·I repetida: rayo"),
                            (tray_S, lib.VIOLETA_OBJETO, "0.85·R(30°) repetida: espiral")):
        fig_t.add_trace(go.Scatter(x=_tr[:, 0], y=_tr[:, 1], mode="lines+markers", line=dict(color=_col, width=2), marker=dict(size=6), name=_nom))
    lib.punto(fig_t, p0, "#444", "p", texto="p")
    mo.vstack([
        mo.md(r"""
        **Trayectorias y líneas coordenadas** (clase 2). Lo que deja un punto al repetir una transformación,
        $p, Ap, A^2p, \dots$, la identifica: la **rotación** lo pasea por una circunferencia, la **homotecia** por un
        rayo, y la **similaridad**, las dos a la vez, por una espiral que se acerca al centro si $k < 1$ y se aleja si
        $k > 1$. Rotación y homotecia con el mismo centro **conmutan**; sus trayectorias, círculos y rayos, son las
        **líneas coordenadas** polares: cada punto es "cuánto giramos y cuánto escalamos". Las rectas de la grilla, en cambio,
        siempre van a rectas (la grilla teal de arriba): eso es lo afín.
        """),
        lib.mesa_interactiva(mo, mo.ui.plotly(fig_t), mo.md("**Controles**"), n_pasos,
                             mo.md(rf"**Números vivos**\n\ntras $n = {_n}$ pasos: círculo ${lib.vec_tex(tray_R[-1], 2)}$, rayo ${lib.vec_tex(tray_H[-1], 2)}$, espiral ${lib.vec_tex(tray_S[-1], 2)}$")),
    ])
    return p0, tray_H, tray_R, tray_S


@app.cell
def _(A_sit, P_viejo, Q_nuevo, k_sit, lib, mo, np, t_sit, th_sit):
    _H45, _H30, _H0 = lib.reflexion2(np.pi / 4), lib.reflexion2(np.deg2rad(30)), lib.reflexion2(0.0)
    _z = [complex(*p) for p in (*P_viejo[:2], *Q_nuevo)]
    a_c = (_z[3] - _z[2]) / (_z[1] - _z[0])
    b_c = _z[2] - a_c * _z[0]
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy. Si no dicen lo mismo, algo está mal en alguna de las dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 El espejo de $y = x$ sobre el vértice $(4, 1)$.** Con $\alpha = 45°$, $\cos 90° = 0$, $\sin 90° = 1$:

            $$H(45°)\begin{pmatrix} 4 \\ 1 \end{pmatrix} = \begin{pmatrix} \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} \\ \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{0} \end{pmatrix}\begin{pmatrix} 4 \\ 1 \end{pmatrix}
            = 4\,\textcolor{#1b6f6a}{\binom{0}{1}} + 1\,\textcolor{#b5451b}{\binom{1}{0}} = \begin{pmatrix} 1 \\ 4 \end{pmatrix}.$$

            Las coordenadas se intercambian: el punto cruza la diagonal. Mismo largo $\sqrt{17}$; $\det = 0 - 1 = -1$.

            **3.2 Dos espejos a $30°$ son $R(60°)$.** Primero el eje $x$, después la recta de $30°$:

            $$H(30°)\,H(0°) = \begin{pmatrix} \tfrac12 & \tfrac{\sqrt3}{2} \\ \tfrac{\sqrt3}{2} & -\tfrac12 \end{pmatrix}\begin{pmatrix} 1 & 0 \\ 0 & -1 \end{pmatrix}
            = \begin{pmatrix} \textcolor{#1b6f6a}{\tfrac12} & \textcolor{#b5451b}{-\tfrac{\sqrt3}{2}} \\ \textcolor{#1b6f6a}{\tfrac{\sqrt3}{2}} & \textcolor{#b5451b}{\tfrac12} \end{pmatrix} = R(60°).$$

            El doble del ángulo entre los espejos, y $\det = (-1)(-1) = +1$: la orientación vuelve.
            """),
            mo.vstack([
                mo.md("```python\nH45 = lib.reflexion2(np.pi / 4)\nH45 @ np.array([4.0, 1.0])\nnp.linalg.det(H45)\n\nH30, H0 = lib.reflexion2(np.deg2rad(30)), lib.reflexion2(0.0)\nnp.allclose(H30 @ H0, lib.rot2(np.deg2rad(60)))\n```"),
                mo.md(f"`H45 @ [4, 1]` = `{np.round(_H45 @ [4, 1], 3).tolist()}` · `det` = `{np.linalg.det(_H45):.1f}`  \n`H30 @ H0` = `{np.round(_H30 @ _H0, 3).tolist()}` · `{bool(np.allclose(_H30 @ _H0, lib.rot2(np.deg2rad(60))))}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(rf"""
            **3.3 La similaridad del plano viejo, con un número complejo.** Si $(x, y)$ es $z = x + iy$, una similaridad
            directa es $z \mapsto a z + b$: $\lvert a \rvert$ es la escala, $\arg a$ el giro, $b$ el corrimiento. Los mojones
            $P_1 = 1 + 2i \mapsto Q_1 = 2 + i$ y $P_2 = 4 + i \mapsto Q_2 = 6 + 3i$ dan

            $$a = \frac{{Q_2 - Q_1}}{{P_2 - P_1}} = \frac{{4 + 2i}}{{3 - i}} = \frac{{(4 + 2i)(3 + i)}}{{10}} = 1 + i,\qquad
            b = Q_1 - a\,P_1 = (2 + i) - (1 + i)(1 + 2i) = 3 - 2i.$$

            $\lvert a \rvert = \sqrt2$, $\arg a = 45°$: escala $1 : \sqrt2$ y giro de $45°$. Como matriz,
            $A = {lib.matriz_coloreada(A_sit, dec=0)}$, $t = {lib.vec_tex(t_sit)}$. Control con el tercer mojón:
            $a\,(2 + 4i) + b = (-2 + 6i) + (3 - 2i) = 1 + 4i$: en el terreno tiene que estar en $(1, 4)$.
            """),
            mo.vstack([
                mo.md("```python\nP1, P2, Q1, Q2 = 1 + 2j, 4 + 1j, 2 + 1j, 6 + 3j\na = (Q2 - Q1) / (P2 - P1)\nb = Q1 - a * P1\nabs(a), np.rad2deg(np.angle(a))\na * (2 + 4j) + b                  # el tercer mojón\nlib.similaridad_por_dos_puntos([1, 2], [4, 1], [2, 1], [6, 3])\n```"),
                mo.md(f"`a` = `{a_c}` · `b` = `{b_c}` · `abs(a)` = `{abs(a_c):.4f}` · `angle` = `{np.rad2deg(np.angle(a_c)):.1f}`°  \n"
                      f"tercer mojón: `{a_c * complex(*P_viejo[2]) + b_c}` · `k` = `{k_sit:.4f}`, `θ` = `{np.rad2deg(th_sit):.1f}`°, `t` = `{np.round(t_sit, 3).tolist()}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return a_c, b_c


@app.cell
def _(A_sit, P_viejo, a_c, b_c, lib, mo, np, t_sit):
    _z = P_viejo[:, 0] + 1j * P_viejo[:, 1]
    _w = a_c * _z + b_c
    _via_complejos = np.column_stack([_w.real, _w.imag])
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **una similaridad es un número complejo**. La nube $N\times2$ se vuelve un array de complejos con
        `z = puntos[:, 0] + 1j * puntos[:, 1]`, la similaridad entera es `a * z + b` (sin matrices) y volvemos con
        `np.column_stack([w.real, w.imag])`. Es la misma cuenta que `puntos @ A.T + t` de la unidad 04, con
        $A = \lvert a \rvert\,R(\arg a)$. El centro sale de `np.linalg.solve(np.eye(2) - A, t)`, o en complejos de $c = b / (1 - a)$.
        """),
        mo.md("```python\nz = puntos[:, 0] + 1j * puntos[:, 1]      # shape (N,), complejos\nw = a * z + b                              # la similaridad entera\nnp.column_stack([w.real, w.imag])          # de vuelta a (N, 2)\nnp.linalg.solve(np.eye(2) - A, t)          # el centro: (I − A) c = t\n```"),
        mo.md(f"los tres mojones del plano viejo, `{P_viejo.shape}` → en el terreno:\n```\n{np.round(_via_complejos, 3)}\n```\n"
              f"`np.allclose` con `puntos @ A.T + t`: `{bool(np.allclose(_via_complejos, P_viejo @ A_sit.T + t_sit))}` · centro: "
              f"`{np.round(np.linalg.solve(np.eye(2) - A_sit, t_sit), 3).tolist()}` = `b / (1 - a)` = `{b_c / (1 - a_c)}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("un par de reflexiones sucesivas no altera las distancias, pero tiene un punto fijo,
        así que tiene que ser una rotación").* $H(0°) = \mathrm{diag}(1, -1)$ conserva todas las distancias, igual que una
        rotación. ¿Por qué **no** es una rotación? Dos razones: una con un número y otra con un dibujo.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        Con un número: $\det H = -1$ y toda rotación tiene $\det = +1$; no hay $\theta$ con $\cos\theta = 1$ y
        $\cos\theta = -1$ a la vez en la diagonal. Con un dibujo: la parcela recorrida antihorario queda recorrida
        horario (el área con signo cambia de signo), y un giro nunca hace eso. Además un espejo deja quieta una **recta
        entera**; una rotación distinta de la identidad sólo deja quieto el centro. Para un giro hacen falta **dos** espejos.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("el punto $o$ es la intersección de las rectas $A$ y $B$, y es el punto fijo de la
        transformación").* La similaridad $z \mapsto 2i\,z + 1$: ¿cuánto escala, cuánto gira, y cuál es su centro?
        Verificá que el centro no se mueve.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $a = 2i$: $\lvert a \rvert = 2$ (todo el doble) y $\arg a = 90°$ (un cuarto de vuelta). El centro cumple
        $c = 2i\,c + 1$, o sea $c\,(1 - 2i) = 1$, $c = \dfrac{1}{1 - 2i} = \dfrac{1 + 2i}{5} = 0.2 + 0.4i$: el punto
        $(0.2, 0.4)$. Control: $2i\,(0.2 + 0.4i) + 1 = 0.4i - 0.8 + 1 = 0.2 + 0.4i$. ✓ En matrices es $(I - A)\,c = t$
        con $A = \begin{pmatrix} 0 & -2 \\ 2 & 0 \end{pmatrix}$, $t = (1, 0)$.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def reflexion(alpha):\n    c, s = ...          # ¿coseno y seno de qué ángulo?\n    return np.array(...)   # 2×2: columnas = a dónde van e1 y e2\n",
        language="python", min_height=120, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("la reflexión, considerando una línea de base y sus perpendiculares, sobre
        las que todas las distancias se escalaban por −1").* Completá `reflexion(alpha)`: la matriz $2\times2$ del
        espejo respecto de la recta por el origen de ángulo `alpha` (radianes). Tenés `np`. Se verifica con
        `np.allclose` en dos ángulos.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _ns = {"np": np}
    _angs = [np.deg2rad(20), np.deg2rad(-50)]
    try:
        exec(editor_c.value, _ns)
        _obt = [np.asarray(_ns["reflexion"](a), dtype=float) for a in _angs]
        _a, _H = _angs[0], _obt[0]
        _c1, _s1, _c2, _s2 = np.cos(_a), np.sin(_a), np.cos(2 * _a), np.sin(2 * _a)
        if _H.shape != (2, 2):
            _res = mo.callout(mo.md(f"❌ la forma es `{_H.shape}`; tiene que ser `(2, 2)`."), kind="danger")
        elif all(np.allclose(h, lib.reflexion2(a)) for h, a in zip(_obt, _angs)):
            _res = mo.callout(mo.md(r"✅ coincide con la referencia en 20° y −50°: $H\,H = I$, $\det = -1$ y la recta queda quieta."), kind="success")
        elif np.allclose(_H, [[_c1, _s1], [_s1, -_c1]]):
            _res = mo.callout(mo.md(r"❌ usaste $\alpha$ donde va $2\alpha$: $e_1$ está a $\alpha$ de un lado del espejo y cae a $\alpha$ del otro, al ángulo $2\alpha$."), kind="warn")
        elif np.allclose(_H, [[_c2, _s2], [_s2, _c2]]):
            _res = mo.callout(mo.md(r"❌ el signo de la diagonal: la segunda columna es $(\sin 2\alpha, -\cos 2\alpha)$; con $+\cos 2\alpha$ el determinante no da $-1$."), kind="warn")
        elif np.allclose(_H, lib.rot2(2 * _a)) or np.allclose(_H, lib.rot2(_a)):
            _res = mo.callout(mo.md(r"❌ eso es una **rotación** ($\det = +1$): el espejo es simétrico, $H = H^T$, con $-\cos 2\alpha$ abajo a la derecha."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para 20°: esperado\n```\n{np.round(lib.reflexion2(_a), 3)}\n```\nobtenido\n```\n{np.round(_H, 3)}\n```"), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def similaridad_por_dos_puntos(P1, P2, Q1, Q2):\n    a = ...        # complejo: giro y escala del segmento P1P2 → Q1Q2\n    b = ...        # complejo: lo que falta para que P1 caiga en Q1\n    A = ...        # 2×2 = |a| R(arg a)\n    t = ...        # (2,)\n    return A, t\n",
        language="python", min_height=150, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado: superponer el plano viejo** *("dado un triángulo y su imagen puede hallarse
        el punto $o$").* Completá `similaridad_por_dos_puntos(P1, P2, Q1, Q2)`: dos puntos del plano viejo y sus
        imágenes en el terreno (arrays de dos números) → `(A, t)` con $A = \lvert a \rvert\,R(\arg a)$. Tenés `np` y
        `rot2`. Se verifica con `np.allclose` sobre otro par de mojones y un tercero de control.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _P1, _P2, _Q1, _Q2, _P3 = (np.array(p, dtype=float) for p in ([1, 1], [3, 2], [-1, 2], [1, 6], [2, 3]))
    A_ref, t_ref = lib.similaridad_por_dos_puntos(_P1, _P2, _Q1, _Q2)
    _k_ref, _th_ref = lib.partes_similaridad(A_ref)
    _ns = {"np": np, "rot2": lib.rot2}
    try:
        exec(editor_d.value, _ns)
        _A, _t = _ns["similaridad_por_dos_puntos"](_P1, _P2, _Q1, _Q2)
        _A, _t = np.asarray(_A, dtype=float), np.asarray(_t, dtype=float).reshape(-1)
        if _A.shape != (2, 2) or _t.shape != (2,):
            _res = mo.callout(mo.md(f"❌ `A` tiene forma `{_A.shape}` y `t` `{_t.shape}`; tienen que ser `(2, 2)` y `(2,)`."), kind="danger")
        elif np.allclose(_A, A_ref) and np.allclose(_t, t_ref):
            _res = mo.callout(mo.md(rf"✅ $k = {lib.num_tex(_k_ref)}$, $\theta = {np.rad2deg(_th_ref):.2f}°$, $t = {lib.vec_tex(t_ref)}$; el mojón de control "
                                    rf"$(2, 3)$ cae en ${lib.vec_tex(A_ref @ _P3 + t_ref)}$ y el centro es ${lib.vec_tex(lib.centro_fijo(A_ref, t_ref))}$."), kind="success")
        elif np.allclose(_A, _k_ref * np.eye(2)):
            _res = mo.callout(mo.md(r"❌ escalaste sin girar: $a$ es el **cociente complejo** $(Q_2 - Q_1)/(P_2 - P_1)$, no el cociente de los largos."), kind="warn")
        elif np.allclose(_A, A_ref) and np.allclose(_t, _Q1 - _P1):
            _res = mo.callout(mo.md(r"❌ calculaste el corrimiento **antes** de girar y escalar: $t = Q_1 - A\,P_1$, no $Q_1 - P_1$. ¿$P_1$ cae en $Q_1$?"), kind="warn")
        elif np.allclose(_A, np.linalg.inv(A_ref)) or np.allclose(_A, -A_ref):
            _res = mo.callout(mo.md(r"❌ el orden de los puntos: $a = (Q_2 - Q_1)/(P_2 - P_1)$, del plano viejo **al** terreno, restando en el mismo orden."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. `A` esperada\n```\n{np.round(A_ref, 3)}\n```\n`t` esperado `{np.round(t_ref, 3).tolist()}`, obtenido `{np.round(_t, 3).tolist()}`."), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return A_ref, t_ref


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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "03_reflexiones_similaridades")
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

    Acá verificamos; las demostraciones (reflexión por proyección sobre el espejo, dos espejos = giro del doble, el centro de
    una similaridad por Apolonio, el punto fijo $(I - A)^{-1} t$):

    - [apunte, «Bloque geométrico: transformaciones euclídeas y similaridades» (la guía de seis teoremas)](../../apunte.pdf#nameddest=cap:08) · [apunte, «Guía resuelta: reflexión respecto de un punto» (guía resuelta)](../../apunte.pdf#nameddest=cap:09)
    - [apunte, «Composición afín práctica: rotación y escala» (rotar alrededor de un centro, escalar alrededor de otro, y el punto fijo)](../../apunte.pdf#nameddest=cap:16)
    - [ficha de la clase 3](../../clases/03.html) · [el hilo conductor](../../index.html) · [Rotaciones II](../01b_rotacion_plano/index.html)

    **Lo que viene:** [Afinidades y coordenadas homogéneas](../04_afines_homogeneas/index.html): cuando los ángulos ya
    no se conservan, cada eje se estira distinto, hacen falta tres puntos y la traslación entra en una $3\times3$.
    """)
    return


@app.cell
def _(A_ref, A_sit, M, P_viejo, Q_nuevo, area_antes, area_despues, centro, centro_sit, d_nuevo, d_viejo, k_sit, lib, mo, np, p0, t_M, t_ref, t_sit, th_sit, tray_H, tray_R, tray_S):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _H = lib.reflexion2
    _angs = np.linspace(-np.pi / 2, np.pi / 2, 13)
    _checks = [
        ("sección 0: z ↦ (1 + i) z + (3 − 2i), k = √2, θ = 45°, centro (2, 3), distancias √10 y √20",
         lib.exacto(A_sit, [[1, -1], [1, 1]]) and lib.exacto(t_sit, [3, -2]) and lib.exacto([k_sit, th_sit], [np.sqrt(2), np.pi / 4])
         and lib.exacto(centro_sit, [2, 3]) and lib.exacto(P_viejo[:2] @ A_sit.T + t_sit, Q_nuevo) and lib.exacto([d_viejo, d_nuevo], [np.sqrt(10), np.sqrt(20)])),
        ("sección 1: H(α) ortogonal, det −1, involución, deja quieta su recta",
         all(lib.exacto(_H(a).T @ _H(a), np.eye(2)) and lib.exacto(np.linalg.det(_H(a)), -1.0) and lib.exacto(_H(a) @ _H(a), np.eye(2))
             and lib.exacto(_H(a) @ [np.cos(a), np.sin(a)], [np.cos(a), np.sin(a)]) for a in _angs)),
        ("sección 2: área después = det · área antes; si hay centro, S(c) = c",
         lib.exacto(area_despues, np.linalg.det(M) * area_antes, tol=1e-6) and (centro is None or lib.exacto(M @ centro + t_M, centro))),
        ("trayectorias: círculo de radio 3, rayo sobre el eje x, espiral ×0.85 por paso",
         lib.exacto(np.linalg.norm(tray_R, axis=1), np.full(len(tray_R), 3.0)) and lib.exacto(tray_H[:, 1], 0 * tray_H[:, 1]) and lib.exacto(tray_R[0], p0)
         and lib.exacto(np.linalg.norm(tray_S[1:], axis=1), 0.85 * np.linalg.norm(tray_S[:-1], axis=1))),
        ("sección 3: H(45°)(4, 1) = (1, 4); H(30°) H(0°) = R(60°); (2, 4) ↦ (1, 4)",
         lib.exacto(_H(np.pi / 4) @ [4, 1], [1, 4]) and lib.exacto(_H(np.deg2rad(30)) @ _H(0.0), lib.rot2(np.deg2rad(60))) and lib.exacto(A_sit @ [2, 4] + t_sit, [1, 4])),
        ("ejercicios (b) y (d): centro de z ↦ 2i z + 1 en (0.2, 0.4); la referencia de (d) lleva P1 ↦ Q1, P2 ↦ Q2 con k = 2",
         lib.exacto(lib.centro_fijo([[0, -2], [2, 0]], [1, 0]), [0.2, 0.4]) and bool(np.isclose(2j * (0.2 + 0.4j) + 1, 0.2 + 0.4j))
         and lib.exacto(A_ref @ [1, 1] + t_ref, [-1, 2]) and lib.exacto(A_ref @ [3, 2] + t_ref, [1, 6]) and lib.exacto(lib.partes_similaridad(A_ref)[0], 2.0)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
