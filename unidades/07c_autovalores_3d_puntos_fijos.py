# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Autovalores en 3D y puntos fijos proyectivos (unidad 07c, complementaria, molde v2 sobre cb104).
Una sola idea: en 3D el polinomio característico es de grado 3 y siempre tiene una raíz real, así que siempre hay una
recta que cae sobre sí misma; el eje de una rotación es su autovector de autovalor 1 (cruz de dos filas de R − I);
y un autovector de la 3×3 homogénea es un punto fijo de la proyectiva: la recta invariante pincha el plano z = 1.

Chequear:  uv run marimo check --select MW unidades/07c_autovalores_3d_puntos_fijos.py
Exportar:  uv run python tools/build.py --only 07c_autovalores_3d_puntos_fijos
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
    # Autovalores en 3D y puntos fijos proyectivos

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    La pregunta: **¿qué recta del espacio deja quieta una rotación compuesta,
    y qué tiene que ver eso con los puntos fijos del pentágono?** El gancho: *el eje de una rotación es la dirección
    que no gira; en la foto rectificada, un punto fijo es un autovector de la $3\times3$.*

    Colores: **columnas** <span style="color:#1b6f6a">**teal**</span>, <span style="color:#b5451b">**rust**</span>,
    <span style="color:#c9a227">**gold**</span> (a dónde van $e_1, e_2, e_3$); las **rectas invariantes** en negro a
    rayas; el pentágono de la unidad 05 en <span style="color:#7a4e9e">**violeta**</span>, lo de antes en gris, lo de
    después en teal.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("07c_autovalores_3d_puntos_fijos"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    R_sit = lib.rot_z(np.pi / 2) @ lib.rot_y(np.pi / 2)
    eje_sit, ang_sit = lib.eje_angulo(R_sit)
    _ez, _ey = np.array([0.0, 0.0, 1.0]), np.array([0.0, 1.0, 0.0])
    candidatos = {"correcta": eje_sit * np.sqrt(3), "ultimo": _ez, "primero": _ey, "ninguna": None}
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            f"el eje z, {lib.vec_plano(_ez)}: el del último giro": "ultimo",
            f"la diagonal {lib.vec_plano(np.round(candidatos['correcta']))}": "correcta",
            f"el eje y, {lib.vec_plano(_ey)}: el del primer giro": "primero",
            "ninguna: dos giros seguidos no dejan nada quieto": "ninguna",
        }),
        value=None,
        label=r"**Predicción.** $R = R_z(90°)\,R_y(90°)$ (primero $y$, después $z$). La dirección que $R$ deja quieta es…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Nivelamos la estación total girando $90°$ alrededor del eje $y$ y después la orientamos girando $90°$ alrededor del eje
        $z$ (unidad 01c). El resultado es **un solo giro** alrededor de un eje nuevo: la única dirección del espacio que
        la rotación compuesta deja quieta. Es la dirección $v$ con $Rv = v$: un autovector de autovalor $1$.

        Columnas de $R$: $e_x \mapsto (0, 0, -1)$, $e_y \mapsto (-1, 0, 0)$, $e_z \mapsto (0, 1, 0)$: los tres ejes se
        permutan con signos. Antes de mirar la figura:
        """),
        prediccion,
    ])
    return R_sit, ang_sit, candidatos, eje_sit, prediccion


@app.cell
def _(R_sit, lib, mo, np, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** $R(-1, 1, 1) = (-1, 1, 1)$: la diagonal es el eje, y el giro es de ${lib.num_tex(np.rad2deg(lib.eje_angulo(R_sit)[1]), 0)}°$ "
                     rf"(tres veces y vuelve: $R^3 = I$). Sale sin polinomio: una rotación tiene **un solo** autovalor real, $1$, y el autovector "
                     rf"es la cruz de dos filas de $R - I$ (sección 3)."),
        "ultimo": ("warn",
                   rf"**No.** $R\,e_z = {lib.vec_tex(R_sit @ [0, 0, 1])}$: el eje $z$ se fue a $y$. El último giro deja quieto a $e_z$, pero el "
                   rf"primero ya lo había movido ($R_y$ lo manda a $e_x$). El eje de la composición no es ninguno de los dos."),
        "primero": ("warn",
                    rf"**No.** $R\,e_y = {lib.vec_tex(R_sit @ [0, 1, 0])}$: el primer giro deja quieto a $e_y$, pero el segundo lo gira a $-e_x$. "
                    rf"El eje de la composición es otro, y no está en ningún plano coordenado."),
        "ninguna": ("warn",
                    r"**No.** Toda rotación de $\mathbb R^3$ tiene eje (Euler): $\det(R - \lambda I)$ es de grado $3$, grado impar, y un "
                    r"polinomio real de grado impar tiene **siempre** una raíz real. Para una rotación esa raíz es $1$. "
                    r"Lo que no existe son dos giros que **conmuten**, no un eje."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Lo mismo que en el plano, un piso más arriba.** $Av = \lambda v$ es $(A - \lambda I)v = 0$: $v$ está en el núcleo
    de la versión modificada, y el detector $\det(A - \lambda I) = 0$ dice para qué $\lambda$ las tres filas de
    $A - \lambda I$ se vuelven **coplanares**. Es un polinomio de grado $3$: tres raíces reales, o una real y dos
    complejas conjugadas (en un polinomio real las complejas vienen de a pares). **Siempre hay una real**, así que en
    $\mathbb R^3$ siempre hay una recta que cae sobre sí misma. Los $\lambda$ complejos no dan vectores de $\mathbb R^3$:
    dicen que en algún plano hay un giro.

    **El autovector es la cruz de dos filas.** Las tres filas de $A - \lambda I$ son reglas que marcan cero sobre $v$:
    $v$ es perpendicular a las tres, y el producto vectorial de dos de ellas lo da. Si ese par da cero (filas paralelas)
    tomamos otro par; si **todos** los pares dan cero, $\lambda$ es raíz doble y el núcleo es un plano entero de autovectores.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R^2$ | autovector $=$ perpendicular a **una** fila de $A - \lambda I$ | la dirección que las dos reglas no ven (unidad 07b) |
    | $\mathbb R^3$ | autovector $=$ cruz de **dos** filas de $A - \lambda I$; rotación: $\lambda = 1$ y nada más real | el **eje**: la recta que la rotación deja quieta; reflexión: $\lambda = -1$ en la normal, $1$ doble en el plano del espejo |
    | $\mathbb P^2$ (homogéneas) | autovector $v$ de la $3\times3$ $H$ con $Hv = \lambda v$ | la recta invariante de $\mathbb R^3$ **pincha** el plano $z = 1$ en un **punto fijo** $(v_1/v_3, v_2/v_3)$; si $v_3 = 0$ es paralela: punto fijo **impropio** |

    En una frase: *los puntos fijos de una transformación proyectiva del plano son los subespacios
    invariantes de $\mathbb R^3$*. Esto es una **muestra**; la demostración está en el apunte, «Bloque algebraico-geométrico: productos, determinante y autovectores», y el caso del
    pentágono en el apunte, «Pentágono regular: cuentas y script».
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- casos precargados: etiqueta → (tipo, matriz o None, rango de la figura, qué pasa) ----------
    _c = np.array([2.0, 1.0])
    _Hg = lib.matriz_afin(lib.rot2(np.deg2rad(72)), _c - lib.rot2(np.deg2rad(72)) @ _c)  # giro de 72° alrededor de (2, 1)
    casos = {
        "R_z(θ) R_y(90°): una rotación, el eje es su único autovector": ("rotacion", None, 3.0, r"un solo autovalor real, $\lambda = 1$; los otros dos son complejos (el giro en el plano perpendicular). En $z = 1$: un solo punto fijo propio, donde el eje pincha."),
        "reflexión diag(1, 1, −1): λ = 1 doble (plano xy) y λ = −1 (eje z)": ("fijo", np.diag([1.0, 1.0, -1.0]), 3.0, r"el núcleo de $A - I$ es el plano $z = 0$ entero (raíz doble, cruces nulas) y el eje $z$ se invierte. Como proyectiva: la simetría central $(x, y) \mapsto (-x, -y)$, centro en el origen y recta de puntos fijos impropios."),
        "H_c del pentágono (unidad 05): homología, recta de puntos fijos y centro": ("fijo", np.array([[2.0, -4.0, 8.0], [0.0, -4.0, 12.0], [0.0, -1.0, 4.0]]), 7.0, r"$\lambda = 2$ doble con cruces nulas: **una recta entera de puntos fijos**, $y = 2$ ($B$ y $D$ quedan quietos); $\lambda = -2$ en $(4, 6, 1)$: el centro. La homología del caso (c)."),
        "giro de 72° alrededor de (2, 1): un solo punto fijo propio": ("fijo", _Hg, 4.5, r"$\lambda = 1$ en $(2, 1, 1)$, el centro del giro, y $e^{\pm i\,72°}$ complejos: un solo punto fijo propio, como la rotación cíclica del pentágono."),
        "traslación (1, 2): el punto fijo es impropio": ("fijo", lib.matriz_afin(np.eye(2), [1.0, 2.0]), 4.5, r"$\lambda = 1$ triple y el núcleo de $H - I$ es el plano $z = 0$: **toda** dirección es fija, ningún punto propio. La recta fija es la del infinito."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="R_z(θ) R_y(90°): una rotación, el eje es su único autovector", label="caso precargado")
    pentagono = np.array([[0, 0], [0, 2], [2, 3], [4, 2], [4, 0]], dtype=float)  # A, B, C, D, E de la unidad 05
    mo.md(r"""
    ## 2. Manipulación

    **Gris**: el cubo unitario antes y el plano $z = 1$ con el pentágono $ABCDE$ de la unidad 05. **Teal**: el cubo
    después, con las columnas como flechas. **Negro a rayas**: las rectas invariantes (autovectores reales) y el
    **rombo** donde pinchan $z = 1$: el punto fijo; un autovalor doble con cruces nulas da un plano entero de
    autovectores (gold), que corta $z = 1$ en una recta de puntos fijos. **Violeta**: el pentágono después, proyectado
    sobre $z = 1$ (dividido por $w$). **Reproducir** anima el camino.
    """)
    return caso, casos, pentagono


@app.cell
def _(caso, casos, mo):
    _tipo, _dato, _, _ = casos[caso.value]
    es_rotacion = _tipo == "rotacion"
    theta_z = mo.ui.slider(-180, 180, value=90, step=1, label="θ de R_z (°)", show_value=True, disabled=not es_rotacion)
    return es_rotacion, theta_z


@app.cell
def _(caso, casos, es_rotacion, go, lib, mo, np, pentagono, theta_z):
    _tipo, _dato, _rango, que_pasa = casos[caso.value]
    if es_rotacion:
        M = lib.rot_z(np.deg2rad(theta_z.value)) @ lib.rot_y(np.pi / 2)
        _eje, _ang = lib.eje_angulo(M)
        camino = [lib.rodrigues(_eje, s * _ang) for s in np.linspace(0, 1, 30)]
    else:
        M = np.asarray(_dato, dtype=float)
        camino = [np.eye(3) + s * (M - np.eye(3)) for s in np.linspace(0, 1, 30)]
    fijos = lib.puntos_fijos_proyectivos(M)
    cubo, aristas = lib.cubo_unitario()
    P_hom = lib.hom(pentagono)

    def _dinamicas(i):
        f = go.Figure()
        _x, _y, _z = lib.segmentos_3d(lib.transformar(cubo, camino[i]), aristas)
        f.add_trace(go.Scatter3d(x=_x, y=_y, z=_z, mode="lines", line=dict(color=lib.TEAL_DESPUES, width=4), name="cubo después"))
        lib.flechas_columnas_3d(f, camino[i], "M")
        _q = lib.dehom(lib.transformar(P_hom, camino[i]))
        _q = lib.cerrar(np.where(np.isfinite(_q), _q, np.nan))
        f.add_trace(go.Scatter3d(x=_q[:, 0], y=_q[:, 1], z=np.ones(len(_q)), mode="lines+markers", line=dict(color=lib.VIOLETA_OBJETO, width=5),
                                 marker=dict(size=3, color=lib.VIOLETA_OBJETO), name="pentágono después (en z = 1)"))
        return list(f.data)

    _L = _rango
    figura = lib.figura_espacio((-_L, _L), caso.value.split(":")[0])
    lib.plano_3d(figura, [1, 0, 0], [0, 1, 0], k=_L, origen=(0, 0, 1), nombre="plano z = 1")
    _x, _y, _z = lib.segmentos_3d(cubo, aristas)
    figura.add_trace(go.Scatter3d(x=_x, y=_y, z=_z, mode="lines", line=dict(color=lib.GRIS_ANTES, width=3), name="cubo antes"))
    _p = lib.cerrar(pentagono)
    figura.add_trace(go.Scatter3d(x=_p[:, 0], y=_p[:, 1], z=np.ones(len(_p)), mode="lines", line=dict(color=lib.GRIS_ANTES, width=4), name="pentágono antes (en z = 1)"))
    lineas = []
    for _f in fijos:
        if _f["plano"]:
            _n = _f["recta"]
            _u = np.cross(_n, [1, 0, 0]) if abs(_n[0]) < 0.9 else np.cross(_n, [0, 1, 0])  # dos direcciones del plano de autovectores
            lib.plano_3d(figura, _u / np.linalg.norm(_u), np.cross(_n, _u) / np.linalg.norm(np.cross(_n, _u)), k=_L, color=lib.COLORES[2],
                         nombre=f"plano de autovectores, λ = {lib.num_tex(_f['lam'], 2)}", opacidad=0.3)
            lineas.append(rf"- $\lambda = {lib.num_tex(_f['lam'], 2)}$ **doble**, cruces nulas: plano entero de autovectores; corta $z = 1$ en la recta ${lib.vec_tex(_f['recta'], 2)} \cdot (x, y, 1) = 0$.")
            continue
        _d = _f["v"] / np.linalg.norm(_f["v"])
        figura.add_trace(go.Scatter3d(x=[-2 * _L * _d[0], 2 * _L * _d[0]], y=[-2 * _L * _d[1], 2 * _L * _d[1]], z=[-2 * _L * _d[2], 2 * _L * _d[2]], mode="lines",
                                      line=dict(color="#222", width=4, dash="dash"), name=f"recta invariante, λ = {lib.num_tex(_f['lam'], 2)}"))
        if _f["punto"] is not None:
            figura.add_trace(go.Scatter3d(x=[_f["punto"][0]], y=[_f["punto"][1]], z=[1], mode="markers", marker=dict(size=9, color="#222", symbol="diamond"),
                                          name=f"punto fijo {lib.vec_plano(_f['punto'], 2)}"))
            lineas.append(rf"- $\lambda = {lib.num_tex(_f['lam'], 2)}$: autovector ${lib.vec_tex(_f['v'], 2)}$, cruz de las filas {_f['filas'][0] + 1} y {_f['filas'][1] + 1}; pincha $z = 1$ en el punto fijo ${lib.vec_tex(_f['punto'], 2)}$.")
        else:
            lineas.append(rf"- $\lambda = {lib.num_tex(_f['lam'], 2)}$: autovector ${lib.vec_tex(_f['v'], 2)}$ con $v_3 = 0$: paralelo al plano, punto fijo **impropio** (dirección fija).")
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))], duracion=70)
    _w = np.linalg.eigvals(M)
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, theta_z,
        mo.md(rf"""
        **Números vivos**

        $$M = {lib.matriz_coloreada(M, 2)}$$

        - `np.linalg.eigvals`: ${", ".join(lib.num_tex(z.real, 2) + (rf" {'+' if z.imag >= 0 else '-'} {lib.num_tex(abs(z.imag), 2)}\,i" if abs(z.imag) > 1e-9 else "") for z in _w)}$
        {chr(10).join(lineas)}

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, fijos


@app.cell
def _(R_sit, lib, mo, np):
    _A = np.diag([1.0, 1.0, -1.0])
    _B1 = R_sit - np.eye(3)
    _Hc = np.array([[2.0, -4.0, 8.0], [0.0, -4.0, 12.0], [0.0, -1.0, 4.0]])
    _pf = lib.puntos_fijos_proyectivos(_Hc)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy con el código a la vista.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 La reflexión $A = \mathrm{diag}(1, 1, -1)$.** $\det(A - \lambda I) = (1 - \lambda)^2(-1 - \lambda)$: raíces
            $1$ (doble) y $-1$. $\lambda = -1$: $A + I = \mathrm{diag}(2, 2, 0)$, cruz de las filas 1 y 2:
            $(2, 0, 0) \times (0, 2, 0) = (0, 0, 4)$, el eje $z$; $A(0, 0, 1) = (0, 0, -1)$ ✓, se invierte. $\lambda = 1$:
            $A - I = \mathrm{diag}(0, 0, -2)$, dos filas nulas, **toda cruz da cero**: el núcleo es el plano $xy$ entero,
            cada vector del espejo queda quieto ("dos autovectores con el mismo autovalor").
            """),
            mo.vstack([
                mo.md("```python\nA = np.diag([1., 1., -1.])\nnp.poly(A)            # det(λI − A)\nI = np.eye(3)\nnp.cross((A + I)[0], (A + I)[1])   # λ = −1\nnp.cross((A - I)[0], (A - I)[1])   # λ = 1: cero\nlib.autovectores_cuna(A)\n```"),
                mo.md(f"`{np.round(np.poly(_A), 6).tolist()}` · `{np.cross((_A + np.eye(3))[0], (_A + np.eye(3))[1]).tolist()}` · `{np.cross((_A - np.eye(3))[0], (_A - np.eye(3))[1]).tolist()}`  \n"
                      + "  \n".join(f"λ = {p['lam']:.0f}: " + ("plano entero" if p["plano"] else f"v = `{p['v'].tolist()}`, filas {p['filas'][0] + 1} y {p['filas'][1] + 1}") for p in lib.autovectores_cuna(_A))),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 El eje de $R = R_z(90°)R_y(90°)$, sin polinomio.** Es rotación (la armamos componiendo rotaciones):
            $\lambda = 1$ y listo. Filas de $R - I$: $(-1, -1, 0)$, $(0, -1, 1)$, $(-1, 0, -1)$. Cruz de las dos primeras:

            $$(-1, -1, 0) \times (0, -1, 1) = \big((-1)(1) - 0(-1),\ 0 \cdot 0 - (-1)(1),\ (-1)(-1) - (-1)(0)\big) = (-1, 1, 1).$$

            Control: $R(-1, 1, 1) = (-1, 1, 1)$ ✓. Filas 2 y 3 dan $(1, -1, -1)$: la misma recta. En una planilla
            alcanza con `MMULT(R; eje)` y mirar que no cambie.
            """),
            mo.vstack([
                mo.md("```python\nR = lib.rot_z(np.pi / 2) @ lib.rot_y(np.pi / 2)\nB = R - np.eye(3)\neje = np.cross(B[0], B[1])\nnp.allclose(R @ eje, eje)\nnp.cross(B[1], B[2])   # otro par: misma recta\nlib.eje_angulo(R)      # (eje unitario, ángulo)\n```"),
                mo.md(f"`eje` = `{np.round(np.cross(_B1[0], _B1[1]), 6).tolist()}` · `{bool(np.allclose(R_sit @ np.cross(_B1[0], _B1[1]), np.cross(_B1[0], _B1[1])))}` · `{np.round(np.cross(_B1[1], _B1[2]), 6).tolist()}`  \n"
                      f"`eje_angulo`: `{np.round(lib.eje_angulo(R_sit)[0], 4).tolist()}`, `{np.rad2deg(lib.eje_angulo(R_sit)[1]):.0f}°`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.3 Puente a la unidad 05: $H_c$ del pentágono.** $\det(H_c - \lambda I) = (2 - \lambda)\big[(-4 - \lambda)(4 - \lambda) + 12\big] = (2 - \lambda)(\lambda^2 - 4)$:
            raíces $2, 2, -2$. Las filas de $H_c - 2I$ son múltiplos de $(0, -1, 2)$: cruces nulas, **recta de puntos fijos**
            $y = 2$. Filas de $H_c + 2I$: $(4, -4, 8) \times (0, -2, 12) = (-32, -48, -8) \sim (4, 6, 1)$: el **centro** $(4, 6)$,
            $H_c(4, 6, 1) = -2\,(4, 6, 1)$ ✓. Una homología: la foto en perspectiva de una reflexión.
            """),
            mo.vstack([
                mo.md("```python\nHc = np.array([[2., -4., 8.],\n               [0., -4., 12.],\n               [0., -1., 4.]])\nnp.linalg.eigvals(Hc)\nK = Hc + 2 * np.eye(3)\nnp.cross(K[0], K[1])\nlib.dehom(Hc @ lib.hom([4., 6.]))\nlib.puntos_fijos_proyectivos(Hc)\n```"),
                mo.md(f"`{np.round(np.linalg.eigvals(_Hc), 6).real.tolist()}` · `{np.cross((_Hc + 2 * np.eye(3))[0], (_Hc + 2 * np.eye(3))[1]).tolist()}` · `{lib.dehom(_Hc @ lib.hom([4.0, 6.0])).tolist()}`  \n"
                      + "  \n".join(f"λ = {p['lam']:.0f}: " + (f"recta `{np.round(p['recta'], 3).tolist()}`" if p["plano"] else f"punto fijo `{np.round(p['punto'], 6).tolist()}`") for p in _pf)),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(R_sit, lib, mo, np):
    _w, _V = np.linalg.eig(R_sit)
    _reales = [k for k in range(3) if abs(_w[k].imag) < 1e-9]
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **`np.linalg.eig` devuelve complejos cuando hay giro, y nos quedamos con los reales**. `w` es el array
        de autovalores (`dtype complex`), `V` tiene los autovectores por columnas; filtramos con `abs(w.imag) < 1e-9`, tomamos
        `.real` y escalamos la columna como convenga (un autovector es una dirección: cualquier múltiplo sirve).
        """),
        mo.md("```python\nw, V = np.linalg.eig(R)\nreales = [k for k in range(3) if abs(w[k].imag) < 1e-9]\nv = V[:, reales[0]].real\nv / np.abs(v).max()               # escalado para leerlo\n```"),
        mo.md(f"`w` = `{np.round(_w, 4).tolist()}` → reales en las posiciones `{_reales}` · `v` escalado = `{np.round((_V[:, _reales[0]].real / np.abs(_V[:, _reales[0]].real).max()), 6).tolist()}`"),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *Idea central: conserva $x$ e $y$, da vuelta $z$.* $A = \mathrm{diag}(1, -1, 1)$, la reflexión
        respecto del plano $xz$. Autovalores, autovectores por cruz de filas, y qué transformación del plano $z = 1$ es:
        ¿cuáles son sus puntos fijos propios e impropios?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $\lambda = 1$ (doble) y $-1$. $\lambda = -1$: $A + I = \mathrm{diag}(2, 0, 2)$, $(2, 0, 0) \times (0, 0, 2) = (0, -4, 0)$:
        el eje $y$, con $v_3 = 0$: punto fijo **impropio**, la dirección vertical del plano. $\lambda = 1$: $A - I =
        \mathrm{diag}(0, -2, 0)$, cruces nulas: plano $xz$ entero, que corta $z = 1$ en la recta $y = 0$: **recta de puntos
        fijos**. En el plano, $(x, y) \mapsto (x, -y)$: el espejo respecto del eje $x$. Es una homología armónica
        ($A^2 = I$) con eje $y = 0$ y centro impropio.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *Idea central: tres raíces: todas reales, o una real y dos complejas conjugadas.* ¿Por qué toda
        transformación proyectiva del plano tiene al menos un punto fijo real (propio o impropio)? ¿Y por qué una
        afinidad que es un giro de $72°$ alrededor de un centro tiene exactamente uno propio?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $\det(H - \lambda I)$ es de grado $3$, impar: tiene una raíz real, con autovector real $v$. Si $v_3 \neq 0$ es un
        punto fijo propio; si $v_3 = 0$, impropio. El giro afín: $H = \begin{pmatrix} R & t \\ 0 & 1 \end{pmatrix}$, y
        $\det(H - \lambda I) = (1 - \lambda)\det(R - \lambda I)$; $R(72°)$ aporta $e^{\pm i\,72°}$, complejos. Queda sólo
        $\lambda = 1$, cuyo autovector $(c, 1)$ es el centro ($Hc = c$): un único punto fijo, propio.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def eje(R):\n    B = ...                 # la versión modificada con λ = 1\n    v = ...                 # cruz de dos filas de B (si da cero, probá otro par)\n    return v / np.linalg.norm(v)\n",
        language="python", min_height=130, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *Idea central: hacemos el producto cruz de dos filas y nos tiene que dar el eje.* Completá
        `eje(R)`: recibe una rotación $3\times3$ y devuelve su eje unitario, por la cruz de dos filas de $R - I$. Tenés `np`.
        Se verifica con `np.allclose(R @ v, v)` en cinco rotaciones al azar (`rodrigues`), y que `|v| = 1`.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(0xDDDE)
    _Rs = [lib.rodrigues(_rng.normal(size=3), _rng.uniform(0.3, 3.0)) for _ in range(5)]
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _vs = [np.asarray(_ns["eje"](R), dtype=float).reshape(-1) for R in _Rs]
        _ok = [bool(v.shape == (3,) and np.isfinite(v).all() and np.allclose(np.linalg.norm(v), 1) and np.allclose(R @ v, v)) for R, v in zip(_Rs, _vs)]
        if all(_ok):
            _res = mo.callout(mo.md("✅ las cinco rotaciones: `R @ v == v` y `|v| = 1`. Es la misma cuenta que `lib.eje_angulo`."), kind="success")
        elif any(not np.isfinite(v).all() for v in _vs):
            _res = mo.callout(mo.md("❌ salió `nan`: la cruz dio el vector nulo (dos filas paralelas, o usaste `R` en vez de `R − I`). Probá otro par de filas."), kind="warn")
        elif all(np.allclose(R @ v, v) for R, v in zip(_Rs, _vs)):
            _res = mo.callout(mo.md("❌ la dirección está bien pero el largo no es 1: dividí por `np.linalg.norm(v)`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ `R @ v != v` en las rotaciones `{[i + 1 for i, o in enumerate(_ok) if not o]}`. ¿Las filas son de `R − np.eye(3)`?"), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def puntos_fijos(H):\n    w, V = np.linalg.eig(H)\n    puntos = []\n    for k in range(3):\n        if ...:                      # λ real y tercera coordenada no nula\n            v = V[:, k].real\n            puntos.append(...)       # (x, y) = (v1 / v3, v2 / v3)\n    return puntos\n",
        language="python", min_height=190, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado: los puntos fijos de la tarea** *Idea central: los puntos fijos son los autovectores de la
        transformación.* Completá `puntos_fijos(H)`: recibe una $3\times3$ homogénea y devuelve la lista de sus puntos
        fijos **propios** $(x, y)$ (autovalores reales, $v_3 \neq 0$). Tenés `np`. Se verifica que cada punto cumpla
        `H p ~ p` y que no falte ni sobre ninguno, en el giro de $72°$ alrededor de $(2, 1)$ y en una escala alrededor de $(1, 3)$.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _c1, _c2 = np.array([2.0, 1.0]), np.array([1.0, 3.0])
    _H1 = lib.matriz_afin(lib.rot2(np.deg2rad(72)), _c1 - lib.rot2(np.deg2rad(72)) @ _c1)
    _H2 = lib.matriz_afin(0.5 * np.eye(2), _c2 - 0.5 * _c2)
    _esperados = [(_H1, [_c1]), (_H2, [_c2])]
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _fallas = []
        for _i, (_H, _esp) in enumerate(_esperados, 1):
            _obt = [np.asarray(p, dtype=float).reshape(-1) for p in _ns["puntos_fijos"](_H)]
            if any(p.shape == (3,) for p in _obt):
                _fallas.append(f"H{_i}: devolviste ternas; falta dividir por la tercera coordenada")
            elif any(not np.allclose(lib.dehom(_H @ lib.hom(p)), p) for p in _obt):
                _fallas.append(f"H{_i}: algún punto no es fijo (¿tomaste autovalores complejos?)")
            elif len(_obt) != len(_esp):
                _fallas.append(f"H{_i}: esperaba {len(_esp)} punto(s) fijo(s), devolviste {len(_obt)}")
        _res = (mo.callout(mo.md("✅ los dos casos: el centro del giro $(2, 1)$ y el de la escala $(1, 3)$, y nada más."), kind="success")
                if not _fallas else mo.callout(mo.md("❌ " + "; ".join(_fallas) + "."), kind="warn"))
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "07c_autovalores_3d_puntos_fijos")
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

    Acá verificamos; las demostraciones (cuántas raíces reales, el método de la cruz de filas, los dos ejemplos resueltos,
    puntos y rectas fijas de una homografía, la homología del pentágono):

    - [apunte, «Álgebra de las transformaciones» (productos, determinante y autovectores)](../../apunte.pdf#nameddest=cap:autovectores) · [apunte, «Proyectivas» (puntos fijos y rectas fijas de una homografía)](../../apunte.pdf#nameddest=cap:proyectivas)
    - [apunte, «Pentágono regular: cuentas y script» (pentágono regular, autovector por producto cruz)](../../apunte.pdf#nameddest=cap:18) · [apunte, «Construcción geométrica de las matrices de rotación 3D» (rotaciones 3D)](../../apunte.pdf#nameddest=cap:14)
    - [ficha del capítulo 7](../../capitulos/06.html) · [unidad anterior: núcleo y autovectores](../07b_nucleo_autovectores/index.html) · [unidad 05: proyectivas](../05_proyectivas/index.html) · [unidad 01c: rotaciones 3D](../01c_rotaciones_3d/index.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** [Cambio de base y diagonalización](../08_cambio_de_base/index.html): si armamos una base con los
    autovectores, en esa grilla la transformación es sólo estirar cada eje por su $\lambda$.
    """)
    return


@app.cell
def _(M, R_sit, ang_sit, candidatos, eje_sit, fijos, lib, mo, np):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _A = np.diag([1.0, 1.0, -1.0])
    _Hc = np.array([[2.0, -4.0, 8.0], [0.0, -4.0, 12.0], [0.0, -1.0, 4.0]])
    _pf = lib.puntos_fijos_proyectivos(_Hc)
    _c = np.array([2.0, 1.0])
    _Hg = lib.matriz_afin(lib.rot2(np.deg2rad(72)), _c - lib.rot2(np.deg2rad(72)) @ _c)
    _B1 = R_sit - np.eye(3)
    _checks = [
        ("sección 0: R = Rz(90)Ry(90) tiene eje (−1, 1, 1)/√3 y ángulo 120°; R e_z = e_y, R e_y = −e_x",
         lib.exacto(candidatos["correcta"], [-1, 1, 1]) and lib.exacto(ang_sit, 2 * np.pi / 3) and lib.exacto(R_sit @ eje_sit, eje_sit)
         and lib.exacto(R_sit @ [0, 0, 1], [0, 1, 0]) and lib.exacto(R_sit @ [0, 1, 0], [-1, 0, 0])),
        ("sección 2: cada autovector dibujado cumple M v = λ v, y cada punto fijo cumple dehom(M hom p) = p",
         all(lib.exacto(M @ f["v"], f["lam"] * f["v"], tol=1e-6) for f in fijos if not f["plano"])
         and all(lib.exacto(lib.dehom(M @ lib.hom(f["punto"])), f["punto"], tol=1e-6) for f in fijos if f["punto"] is not None)),
        ("3.1 y 3.2: reflexión λ = 1 doble (plano) y −1 en (0, 0, 1); filas 1, 2 de R − I dan (−1, 1, 1) y filas 2, 3 dan (1, −1, −1)",
         [a["lam"] for a in lib.autovectores_cuna(_A)] == [1.0, -1.0] and lib.autovectores_cuna(_A)[0]["plano"]
         and lib.exacto(np.cross((_A + np.eye(3))[0], (_A + np.eye(3))[1]), [0, 0, 4])
         and lib.exacto(np.cross(_B1[0], _B1[1]), [-1, 1, 1]) and lib.exacto(np.cross(_B1[1], _B1[2]), [1, -1, -1])),
        ("3.3: H_c: λ = 2 doble con recta y = 2, λ = −2 con centro (4, 6); B y D quedan quietos",
         [p["lam"] for p in _pf] == [2.0, -2.0] and _pf[0]["plano"] and lib.exacto(_pf[0]["recta"], [0, -0.5, 1]) and lib.exacto(_pf[1]["punto"], [4, 6])
         and lib.exacto(lib.dehom(_Hc @ lib.hom([0, 2])), [0, 2]) and lib.exacto(lib.dehom(_Hc @ lib.hom([4, 2])), [4, 2])),
        ("ejercicios: diag(1, −1, 1) → (0, −4, 0) impropio y plano xz; el giro afín de 72° tiene un solo punto fijo propio, (2, 1)",
         lib.exacto(np.cross([2, 0, 0], [0, 0, 2]), [0, -4, 0]) and lib.autovectores_cuna(np.diag([1.0, -1.0, 1.0]))[0]["plano"]
         and [tuple(np.round(p["punto"], 6)) for p in lib.puntos_fijos_proyectivos(_Hg) if p["punto"] is not None] == [(2.0, 1.0)]),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
