# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Curvatura como forma cuadrática (unidad 12, molde v2 sobre cb104).
Una sola idea: la primera forma (unidad 10) es la regla; la curvatura es cuánto se aparta la
superficie del plano tangente al dar un paso en cada rumbo, y eso es otra forma cuadrática (L, M, N). Sus rumbos
propios son las direcciones principales (autovectores de solve(I, II)), la curvatura de Gauss es su producto
(det II / det I), e ir derecho sobre la superficie es no doblar dentro de ella.

Chequear:  uv run marimo check --select MW unidades/12_curvatura.py
Exportar:  uv run python tools/build.py --only 12_curvatura
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
    # Curvatura como forma cuadrática

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    La pregunta: **¿Cuánto se aparta la superficie de su plano tangente en cada
    rumbo, y qué quiere decir ir derecho sobre ella?** El gancho: *un instrumento con burbuja apoyado en el terreno: la curvatura dice
    cuánto cambia la vertical al dar un paso en cada rumbo.*

    Colores, iguales en la figura y en el álgebra: la superficie y su grilla en **gris**; el rumbo elegido, su
    sección normal y el círculo osculador en <span style="color:#7a4e9e">**violeta**</span>; las dos direcciones
    principales en <span style="color:#1b6f6a">**teal**</span> ($\kappa_1$, la máxima) y
    <span style="color:#b5451b">**rust**</span> ($\kappa_2$, la mínima), que son las columnas de la matriz $D$;
    la normal en <span style="color:#c9a227">**gold**</span>. Todo lo de [la unidad 10](../10_jacobiano_primera_forma/index.html)
    sigue valiendo: $E, F, G$ es la regla; acá se le suma $L, M, N$.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("12_curvatura"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    def silla(x, y):
        return (x**2 - y**2) / 4

    apart = {k: float(silla(np.cos(np.deg2rad(a)), np.sin(np.deg2rad(a)))) for k, a in (("este", 0), ("norte", 90), ("45°", 45))}
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            f"sube {apart['este']:.2f} m en todos los rumbos: es un pozo": "pozo",
            f"baja {apart['este']:.2f} m en todos los rumbos: es una cima": "cima",
            f"sube {apart['este']:.2f} m hacia el este, baja {apart['este']:.2f} m hacia el norte y a 45° no se aparta": "correcta",
            "no se aparta en ningún rumbo: en el punto la tangente es horizontal": "plano",
        }),
        value=None,
        label="**Predicción.** Damos un paso de 1 m desde el punto más bajo del paso. Respecto del plano horizontal, el terreno…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Estamos parados en un **paso de montaña**: hacia el este y el oeste el terreno sube (los dos cerros), hacia el
        norte y el sur baja (los dos valles). Apoyamos en el punto más bajo del paso un instrumento con burbuja: la burbuja centra, el
        plano que marca es horizontal. Medido en metros desde ese punto, el terreno cerca de ahí es la silla
        $z = (x^2 - y^2)/4$, con $x$ hacia el este y $y$ hacia el norte.
        """),
        prediccion,
    ])
    return apart, prediccion, silla


@app.cell
def _(apart, mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** Hacia el este $z = 1/4 = {apart['este']:+.2f}$ m, hacia el norte $z = -1/4 = {apart['norte']:+.2f}$ m, y a $45°$ "
                     rf"$z = (\tfrac12 - \tfrac12)/4 = {apart['45°']:.0f}$. El apartamiento **depende del rumbo** y cambia de signo: eso es lo que "
                     r"mide la curvatura, y abajo mostramos que es una forma cuadrática en el rumbo."),
        "pozo": ("warn",
                 r"**No.** Un pozo sube en todos los rumbos ($z = (x^2 + y^2)/4$); el paso sube hacia los cerros y **baja** hacia los valles: "
                 r"el signo de $-y^2$ lo dice. La burbuja centrada solo dice que el plano tangente es horizontal, no cómo se aparta el terreno de él."),
        "cima": ("warn",
                 r"**No.** Una cima baja en todos los rumbos ($z = -(x^2 + y^2)/4$). Hacia el este el paso sube: $z = x^2/4 > 0$. En el paso "
                 r"hay rumbos que suben y rumbos que bajan: las dos curvaturas principales tienen signos opuestos."),
        "plano": ("warn",
                  r"**No.** Tangente horizontal quiere decir que el término **lineal** es cero, no el cuadrático: $z \approx \tfrac12 f_{xx} x^2 + f_{xy}\,xy + \tfrac12 f_{yy} y^2$. "
                  r"A un paso de 1 m el terreno ya está $0{,}25$ m arriba o abajo del plano horizontal según el rumbo."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** Si giramos los ejes dentro del plano tangente cambian $L, M, N$ pero no las dos curvaturas
    principales ni su producto (autovalores, unidad 08); si doblamos la superficie sin estirarla (una hoja, un cilindro)
    cambian $\kappa_1$ y $\kappa_2$ pero no $K = \kappa_1 \kappa_2$ (Gauss; ver el ejercicio b).

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $y = f(x)$ con tangente horizontal: $f(x) \approx \tfrac12 f''(0)\,x^2$ | cuánto se aparta el gráfico de la recta tangente: la segunda derivada |
    | $\mathbb R^2$ | curva plana: $\kappa = 1/R$ del círculo osculador; con tangente horizontal, $\kappa = f''$ | el círculo que mejor besa la curva en el punto; recta: $R = \infty$, $\kappa = 0$ |
    | $\mathbb R^3$ | superficie: en el rumbo $d = (du, dv)$, $\kappa_n(d) = \dfrac{II(d)}{I(d)} = \dfrac{L\,du^2 + 2M\,du\,dv + N\,dv^2}{E\,du^2 + 2F\,du\,dv + G\,dv^2}$ | a un paso $s$ en el rumbo $d$ la superficie se aparta $\tfrac12 \kappa_n s^2$ del plano tangente |

    **La segunda forma fundamental.** $I(d) = d^{\mathsf T}\begin{pmatrix} E & F \\ F & G\end{pmatrix} d$ es la regla:
    el cuadrado del largo del paso. $II(d) = d^{\mathsf T}\begin{pmatrix} L & M \\ M & N\end{pmatrix} d$, con
    $L = r_{uu}\cdot n$, $M = r_{uv}\cdot n$, $N = r_{vv}\cdot n$, es cuánto de la segunda derivada del paso cae
    sobre la normal $n$. Las dos son **formas cuadráticas**: un número que sale de un vector pasando por una matriz
    simétrica, como $\|v\|^2 = v^{\mathsf T} v$ con otra matriz en el medio. Con la grilla $(x, y)$ de un gráfico
    $z = f(x, y)$ y tangente horizontal, $I$ es la identidad y $II$ es la hessiana de la unidad 10: la prueba 1 del apunte llega a $\kappa_n(\alpha) = L\cos^2\alpha + 2M\cos\alpha\sin\alpha + N\sin^2\alpha$
    y a que *los máximos y mínimos se dan a intervalos de $\pi/2$*. (Algunos textos llaman $N$ al término mixto y $M$ a
    $f_{yy}$; usamos la notación usual, $M$ mixto, la de la unidad 10 y la bibliografía.)

    **Direcciones principales.** El máximo y el mínimo de $II(d)$ entre los rumbos con $I(d) = 1$ son los
    autovalores de $S = I^{-1} II$ (`solve(I, II)`): $\kappa_1 \ge \kappa_2$, con autovectores $d_1, d_2$ (las columnas
    de $D$), perpendiculares sobre la superficie. En el rumbo a $\alpha$ de $d_1$ vale $\kappa_n = \kappa_1\cos^2\alpha + \kappa_2\sin^2\alpha$
    (Euler). Escalera por casos: **esfera**, todas iguales a $1/R$, ningún rumbo privilegiado; **cilindro**, una vale
    $1/R$ y la otra $0$; **silla**, signos opuestos. La **curvatura de Gauss** es el producto,
    $K = \kappa_1\kappa_2 = \det II / \det I$ ($\det S$, unidad 07a: cuánto agranda el área la aplicación normal de Gauss, que lleva cada punto a su normal sobre la esfera unidad), y la media es $H = (\kappa_1 + \kappa_2)/2$.

    **Geodésica.** La aceleración de una curva sobre la superficie tiene una parte normal (la que la superficie le
    obliga, $\kappa_n$) y una tangencial (la que dobla **dentro** de la superficie, $\kappa_g$). Ir derecho es
    $\kappa_g = 0$: el volante recto, el hilo tenso sobre la cáscara. En la esfera, los círculos máximos; un paralelo
    no, salvo el ecuador. Euler y los extremos a
    $\pi/2$ se demuestran en el apunte (ver el cierre).
    """)
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("05_elipsoide_euler_meusnier", "Sobre el elipsoide, giramos el plano normal en acimut (Euler: el radio del círculo osculador va de M a N) y después lo inclinamos hasta el paralelo (Meusnier: radio N·cos φ); el bucle vuelve sobre sus pasos."))
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (f(x, y) vectorizada, rumbo inicial en °, qué pasa) ----------
    _R = 2.5
    casos = {
        "esfera: cuenco de radio 2.5": (lambda x, y: _R - np.sqrt(_R**2 - x**2 - y**2), 30,
                                        r"todas las curvaturas valen $1/R = 0{,}4$: $II = I/R$, ningún rumbo es especial (punto umbilical) y $K = 1/R^2 = 0{,}16$."),
        "cilindro: canaleta de radio 2.5 (eje y)": (lambda x, y: _R - np.sqrt(_R**2 - x**2) + 0 * y, 0,
                                                   r"en el rumbo $x$ se curva como un círculo de radio $2{,}5$; en el rumbo $y$ la sección es una recta, $\kappa_2 = 0$ y $K = 0$: se desenrolla sobre el plano sin estirar."),
        "silla z = (x² − y²)/4": (lambda x, y: (x**2 - y**2) / 4, 45,
                                  r"sube en $x$ y baja en $y$: $\kappa_1 > 0 > \kappa_2$, $K < 0$. A $45°$ de las direcciones principales la sección normal no se curva."),
        "loma: terreno suave": (lambda x, y: 0.6 * np.sin(1.2 * x) * np.cos(0.9 * y), 0,
                                r"las direcciones principales **no** siguen la grilla $(x, y)$: hay que diagonalizar $S = I^{-1}II$ para encontrarlas, y $F$, $M$ ya no son cero."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="silla z = (x² − y²)/4", label="caso precargado")
    x0 = mo.ui.slider(-1.0, 1.0, value=0.4, step=0.1, label="x₀", show_value=True)
    y0 = mo.ui.slider(-1.0, 1.0, value=0.2, step=0.1, label="y₀", show_value=True)
    mo.md(r"""
    ## 2. Manipulación

    En **gris**, la superficie con su grilla $(x, y)$ y el plano tangente; en **gold**, la normal. En **violeta**,
    el rumbo $\alpha$ (desde el eje $x$, dentro del plano tangente), la **sección normal** (el corte con el plano
    que contiene al rumbo y a la normal) y su **círculo osculador**, de radio $1/\kappa_n$. En **teal** y
    **rust**, las direcciones principales: la curvatura normal con signo es máxima en teal ($\kappa_1$) y mínima en rust ($\kappa_2$); si las dos son positivas, el radio es mínimo en teal y máximo en rust (en la esfera, no cambia).
    En el panel de la derecha: el caso, el punto $(x_0, y_0)$ y el rumbo.
    """)
    return caso, casos, x0, y0


@app.cell
def _(caso, casos, mo):
    rumbo = mo.ui.slider(0, 180, value=casos[caso.value][1], step=5, label="rumbo α (°) desde el eje x", show_value=True)
    return (rumbo,)


@app.cell
def _(caso, casos, go, lib, mo, np, rumbo, x0, y0):
    f, _, que_pasa = casos[caso.value]
    r = lambda x, y: lib.xyz(x, y, f(x, y))  # noqa: E731
    ff = lib.formas_fundamentales(r, x0.value, y0.value)
    E, F, G, L, M, N = (ff[k] for k in "EFGLMN")
    p, n = ff["p"], ff["n"]
    k1, k2, D = lib.curvaturas_principales(E, F, G, L, M, N)
    K, H = lib.curvatura_gauss(E, F, G, L, M, N)
    _a = np.deg2rad(rumbo.value)
    kn = lib.curvatura_normal(E, F, G, L, M, N, np.cos(_a), np.sin(_a))
    t = np.cos(_a) * ff["r_u"] + np.sin(_a) * ff["r_v"]
    t = t / np.linalg.norm(t)

    figura = lib.figura_espacio((-1.6, 1.6), f"{caso.value.split(':')[0]} · punto ({x0.value}, {y0.value}) · α = {rumbo.value}°")
    _u = np.linspace(-1.5, 1.5, 13)
    lib.superficie_malla(figura, r, _u, _u, color=lib.GRIS_ANTES, nombre="superficie", ancho=1.5, opacidad=0.6)
    lib.plano_3d(figura, ff["r_u"], ff["r_v"], k=0.5, origen=p, nombre="plano tangente", opacidad=0.25)
    lib.flecha_3d(figura, p, p + 0.7 * n, lib.COLORES[2], "normal n")
    for _k, (_kap, _nom) in enumerate(((k1, "κ₁"), (k2, "κ₂"))):
        _d = D[0, _k] * ff["r_u"] + D[1, _k] * ff["r_v"]
        lib.flecha_3d(figura, p - 0.8 * _d, p + 0.8 * _d, lib.color_columna(_k), f"dirección principal {_nom} = {lib.num_tex(_kap)}", ancho=6)
    _sec = lib.seccion_normal(f, p, t, n, largo=1.1, m=45)
    figura.add_trace(go.Scatter3d(x=_sec[:, 0], y=_sec[:, 1], z=_sec[:, 2], mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=7),
                                  name="sección normal en el rumbo α"))
    lib.flecha_3d(figura, p, p + 0.8 * t, lib.VIOLETA_OBJETO, "rumbo α (tangente)", ancho=5)
    if abs(kn) > 0.06:
        _c = lib.circulo_3d(p + n / kn, t, n, 1 / abs(kn))
        figura.add_trace(go.Scatter3d(x=_c[:, 0], y=_c[:, 1], z=_c[:, 2], mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=3, dash="dot"),
                                      name=f"círculo osculador, radio {1 / abs(kn):.2f}"))
        _radio = rf"radio del círculo osculador $1/\lvert\kappa_n\rvert = {1 / abs(kn):.3f}$"
    else:
        _radio = r"$\lvert\kappa_n\rvert < 0{,}06$: radio mayor que $16$, la sección es casi una recta y el círculo no entra en la figura"
    figura.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", marker=dict(size=6, color=lib.VIOLETA_OBJETO), name="punto"))
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, x0, y0, rumbo,
        mo.md(rf"""
        **Números vivos** (en el punto, con la grilla $(x, y)$)

        $$I = {lib.pmat([[E, F], [F, G]])}, \qquad II = {lib.pmat([[L, M], [M, N]])}$$

        - rumbo $\alpha = {rumbo.value}°$: $\kappa_n = II(d)/I(d) = {lib.num_tex(kn)}$; {_radio}
        - principales: $\kappa_1 = {lib.num_tex(k1)}$, $\kappa_2 = {lib.num_tex(k2)}$, direcciones $D = {lib.matriz_coloreada(D)}$ (columnas en $(dx, dy)$)
        - Gauss $K = \kappa_1\kappa_2 = {lib.num_tex(K, 4)}$, media $H = {lib.num_tex(H, 4)}$; control $\det II/\det I = {lib.num_tex((L * N - M**2) / (E * G - F**2), 4)}$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return D, E, F, G, H, K, L, M, N, ff, k1, k2, kn


@app.cell
def _(lib, mo, np):
    _R = 2.0
    _esf = lambda x, y: lib.xyz(x, y, _R - np.sqrt(_R**2 - x**2 - y**2))  # noqa: E731
    _cil = lambda x, y: lib.xyz(x, y, _R - np.sqrt(_R**2 - x**2) + 0 * y)  # noqa: E731
    _fe, _fc = lib.formas_fundamentales(_esf, 0.3, -0.2), lib.formas_fundamentales(_cil, 0.3, -0.2)
    _ke, _kc = lib.curvaturas_principales(*(_fe[k] for k in "EFGLMN")), lib.curvaturas_principales(*(_fc[k] for k in "EFGLMN"))
    _Ke, _Kc = lib.curvatura_gauss(*(_fe[k] for k in "EFGLMN"))[0], lib.curvatura_gauss(*(_fc[k] for k in "EFGLMN"))[0]
    ok_esfera = bool(np.allclose([_ke[0], _ke[1], _Ke], [1 / _R, 1 / _R, 1 / _R**2], atol=1e-5))
    ok_cilindro = bool(np.allclose([_kc[0], _kc[1], _Kc], [1 / _R, 0, 0], atol=1e-5))
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        A mano elegimos el punto cómodo: el fondo del cuenco, donde la tangente es horizontal y la grilla $(x, y)$ es
        la regla misma ($I$ = identidad). El código mide en un punto cualquiera, $(0{,}3;\ -0{,}2)$, con diferencias
        finitas: ahí $E, F, G, L, M, N$ cambian, pero las curvaturas principales y $K$ dan lo mismo.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Esfera de radio $R = 2$**, cuenco $z = R - \sqrt{R^2 - x^2 - y^2}$. En $(0, 0)$: $f_x = f_y = 0$,
            $f_{xx} = f_{yy} = 1/R = 0{,}5$, $f_{xy} = 0$:

            $$I = \begin{pmatrix} 1 & 0 \\ 0 & 1 \end{pmatrix},\quad II = \begin{pmatrix} 0{,}5 & 0 \\ 0 & 0{,}5 \end{pmatrix} = \tfrac1R I$$

            $S = I^{-1}II = \tfrac1R I$: $\kappa_1 = \kappa_2 = 1/R = 0{,}5$ en todo rumbo, $K = 1/R^2 = 0{,}25$.
            """),
            mo.vstack([
                mo.md("```python\nR = 2.0\nr = lambda x, y: lib.xyz(x, y, R - np.sqrt(R**2 - x**2 - y**2))\nff = lib.formas_fundamentales(r, 0.3, -0.2)\nk1, k2, D = lib.curvaturas_principales(*(ff[k] for k in \"EFGLMN\"))\nK, H = lib.curvatura_gauss(*(ff[k] for k in \"EFGLMN\"))\nnp.allclose([k1, k2, K], [1/R, 1/R, 1/R**2], atol=1e-5)\n```"),
                mo.md(f"`E, F, G` = `{[round(_fe[k], 4) for k in 'EFG']}` · `L, M, N` = `{[round(_fe[k], 4) for k in 'LMN']}`\n\n`k1, k2, K` = `{[round(v, 5) for v in (_ke[0], _ke[1], _Ke)]}` · `allclose` = `{ok_esfera}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(r"""
            **3.2 Cilindro de radio $R = 2$**, canaleta $z = R - \sqrt{R^2 - x^2}$ (no depende de $y$). En $(0, 0)$:
            $f_{xx} = 1/R = 0{,}5$, $f_{yy} = 0$, $f_{xy} = 0$:

            $$II = \begin{pmatrix} 0{,}5 & 0 \\ 0 & 0 \end{pmatrix}, \quad \kappa_1 = 0{,}5 \text{ (rumbo } x),\ \kappa_2 = 0 \text{ (rumbo } y),\ K = 0.$$

            Como una hoja se enrolla en un cilindro sin estirarse, el *Theorema Egregium* obliga a que tenga el mismo $K$ que el plano: $K = 0$.
            """),
            mo.vstack([
                mo.md("```python\nr = lambda x, y: lib.xyz(x, y, R - np.sqrt(R**2 - x**2) + 0*y)\nff = lib.formas_fundamentales(r, 0.3, -0.2)\nk1, k2, D = lib.curvaturas_principales(*(ff[k] for k in \"EFGLMN\"))\nnp.allclose([k1, k2, K], [1/R, 0, 0], atol=1e-5)\n```"),
                mo.md(f"`L, M, N` = `{[round(_fc[k], 4) for k in 'LMN']}` · `k1, k2, K` = `{[round(v, 5) for v in (_kc[0], _kc[1], _Kc)]}` · `allclose` = `{ok_cilindro}`\n\n`D` =\n```\n{np.round(_kc[2], 3)}\n```"),
            ]),
        ], widths="equal", align="start"),
    ])
    return ok_cilindro, ok_esfera


@app.cell
def _(mo, np):
    _g = lambda x: np.sqrt(4.0 - x**2)  # noqa: E731
    _x = 0.3
    _exacta = -4.0 / (4.0 - _x**2) ** 1.5
    _filas = "\n".join(f"| `{h:g}` | `{(_g(_x + h) - 2 * _g(_x) + _g(_x - h)) / h**2:.9f}` | `{abs((_g(_x + h) - 2 * _g(_x) + _g(_x - h)) / h**2 - _exacta):.1e}` |"
                       for h in (1e-1, 1e-2, 1e-3, 1e-5, 1e-7))
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        **Diferencias finitas centradas.** La segunda derivada sin derivar a mano:
        $f''(x) \approx \dfrac{f(x+h) - 2f(x) + f(x-h)}{h^2}$ (y la mixta, con los cuatro puntos $(x \pm h, y \pm h)$ sobre $4h^2$).
        Es lo que hace `lib.formas_fundamentales`. El paso $h$ no puede ser ni grande (error de truncamiento, $\sim h^2$) ni
        minúsculo (al dividir por $h^2$ el redondeo de `float64` se agranda): abajo, $f(x) = \sqrt{4 - x^2}$ en $x = 0{,}3$,
        con $f'' = -4/(4 - x^2)^{3/2}$ exacta.
        """),
        mo.md(f"| $h$ | aproximación | error |\n|---|---|---|\n{_filas}\n\nexacta: `{_exacta:.9f}`. El mínimo está cerca de $h = 10^{{-3}}$, el valor por defecto."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *Idea central: la curvatura tiene que ser una forma cuadrática.* Para la silla
        $z = (x^2 - y^2)/4$ en el origen escribí $I$ y $II$, las curvaturas principales con sus rumbos, $K$ y los dos
        rumbos en los que $\kappa_n = 0$. ¿Qué signo tiene $K$ y qué dice eso de la superficie?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $f_x = f_y = 0$ en el origen: $I$ es la identidad. $f_{xx} = 1/2$, $f_{yy} = -1/2$, $f_{xy} = 0$:
        $II = \mathrm{diag}(1/2, -1/2)$, ya diagonal: $\kappa_1 = 1/2$ en el rumbo $x$ (sube), $\kappa_2 = -1/2$ en el rumbo
        $y$ (baja). $K = -1/4 < 0$: la superficie cruza su plano tangente, está de un lado en unos rumbos y del otro en
        otros. $\kappa_n(\alpha) = \tfrac12\cos^2\alpha - \tfrac12\sin^2\alpha = \tfrac12\cos 2\alpha = 0$ en $\alpha = \pm 45°$:
        por ahí la sección normal es (a segundo orden) recta.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *Idea central: nos ayuda a entender la curvatura del elipsoide.* Un mapa plano de la Tierra que
        conserve **todas** las distancias: ¿puede existir? Usá $K$ y lo que mostró el cilindro.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        No. El cilindro mostró que doblar sin estirar no cambia $K$ (la hoja plana tiene $K = 0$ y la canaleta también:
        $\kappa_1 = 1/R$, $\kappa_2 = 0$). Gauss demostró que eso vale siempre: $K$ se calcula solo con la regla $E, F, G$
        y sus derivadas, así que cualquier mapa que conserve distancias conserva $K$ (su *theorema egregium*; acá lo
        mostramos, no lo demostramos). Pero el plano tiene $K = 0$ y la esfera $K = 1/R^2 > 0$ (y el elipsoide, $K = 1/(MN) > 0$,
        unidad 13): no hay mapa plano sin deformación. Toda proyección elige qué sacrificar.
        """)}),
    ])
    return


@app.cell
def _(mo, np):
    _rng = np.random.default_rng(0xDDDE)
    casos_cd = []  # 20 pares (I, II): I = JᵀJ (regla oblicua), II simétrica al azar
    for _ in range(20):
        _J, _A = _rng.normal(size=(3, 2)), _rng.normal(size=(2, 2))
        _I, _II = _J.T @ _J, (_A + _A.T) / 2
        casos_cd.append((_I[0, 0], _I[0, 1], _I[1, 1], _II[0, 0], _II[0, 1], _II[1, 1]))
    editor_c = mo.ui.code_editor(
        value="def curvaturas_principales(E, F, G, L, M, N):\n    I = np.array([[E, F], [F, G]])\n    II = ...            # la segunda forma, simétrica\n    S = ...             # I⁻¹ II, sin invertir: np.linalg.solve\n    w = np.linalg.eigvals(S).real\n    return ...          # (κ₁, κ₂) con κ₁ ≥ κ₂\n",
        language="python", min_height=150, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *Idea central: los máximos y mínimos se dan a intervalos de $\pi/2$.* Completá
        `curvaturas_principales(E, F, G, L, M, N)`: devuelve `(k1, k2)` con $\kappa_1 \ge \kappa_2$. Tenés `np`. Se verifica con
        `np.allclose` contra la referencia en 20 pares $(I, II)$ al azar, con $I$ una regla oblicua ($F \ne 0$).
        """),
        editor_c,
    ])
    return casos_cd, editor_c


@app.cell
def _(casos_cd, editor_c, lib, mo, np):
    _casos = casos_cd
    _esperado = np.array([lib.curvaturas_principales(*c)[:2] for c in _casos])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.array([np.sort(np.asarray(_ns["curvaturas_principales"](*c), dtype=float).ravel())[::-1] for c in _casos])
        _solo_II = np.array([np.sort(np.linalg.eigvalsh([[c[3], c[4]], [c[4], c[5]]]))[::-1] for c in _casos])
        _sin_FM = np.array([sorted([c[3] / c[0], c[5] / c[2]], reverse=True) for c in _casos])
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ devolvés algo de forma `{_obtenido.shape[1:]}` por caso; tienen que ser dos números."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md(r"✅ coincide en los 20 casos: los autovalores de $S = I^{-1}II$."), kind="success")
        elif np.allclose(_obtenido, _solo_II):
            _res = mo.callout(mo.md(r"❌ usaste los autovalores de $II$ sola. Eso ignora la regla: $II(d)$ se compara con el largo $I(d)$ del paso, y la grilla no es ortonormal. `np.linalg.solve(I, II)`."), kind="warn")
        elif np.allclose(_obtenido, _sin_FM):
            _res = mo.callout(mo.md(r"❌ te quedaste con $L/E$ y $N/G$: olvidaste $F$ y $M$. Solo vale cuando la grilla es ortogonal **y** las direcciones principales la siguen."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para el primer caso se esperaba `{np.round(_esperado[0], 4).tolist()}` y se obtuvo `{np.round(_obtenido[0], 4).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def gauss(E, F, G, L, M, N):\n    det_I = ...     # det de la primera forma\n    det_II = ...    # det de la segunda forma\n    return ...      # K\n",
        language="python", min_height=120, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *Idea central: la curvatura de Gauss es el producto de las principales.* Completá
        `gauss(E, F, G, L, M, N)` $= \det II / \det I = \kappa_1 \kappa_2$. Se verifica con `np.allclose` contra
        $\kappa_1\kappa_2$ de la referencia en los mismos 20 casos.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(casos_cd, editor_d, lib, mo, np):
    _casos = casos_cd
    _esperado = np.array([lib.curvaturas_principales(*c)[0] * lib.curvaturas_principales(*c)[1] for c in _casos])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _obtenido = np.array([float(_ns["gauss"](*c)) for c in _casos])
        if np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md(r"✅ coincide: $K = \det II / \det I = \kappa_1\kappa_2$ en los 20 casos."), kind="success")
        elif np.allclose(_obtenido, [c[3] * c[5] - c[4] ** 2 for c in _casos]):
            _res = mo.callout(mo.md(r"❌ devolvés $\det II$ solo. Hay que dividir por $\det I = EG - F^2$: el área que mide la regla."), kind="warn")
        elif np.allclose(_obtenido, [(c[3] * c[5] - c[4] ** 2) / (c[0] * c[2]) for c in _casos]):
            _res = mo.callout(mo.md(r"❌ en $\det I$ olvidaste $F$: es $EG - F^2$, no $EG$."), kind="warn")
        elif np.allclose(_obtenido, [(c[3] * c[5]) / (c[0] * c[2] - c[1] ** 2) for c in _casos]):
            _res = mo.callout(mo.md(r"❌ en $\det II$ olvidaste $M$: es $LN - M^2$."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para el primer caso se esperaba `{_esperado[0]:.4f}` y se obtuvo `{_obtenido[0]:.4f}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "12_curvatura")
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

    Acá verificamos que el apartamiento del plano tangente es una forma cuadrática en el rumbo, que sus rumbos propios
    son perpendiculares y que $K$ sobrevive al doblado. Las demostraciones:

    - [apunte, capítulo «Curvatura como forma cuadrática»](../../apunte.pdf#nameddest=cap:curvatura):
      [sección «La segunda forma fundamental»](../../apunte.pdf#nameddest=sec:segunda-forma) (la curvatura normal es
      la segunda forma evaluada en el rumbo; en un punto crítico, la hessiana) ·
      [sección «Curvaturas principales, direcciones principales y fórmula de Euler»](../../apunte.pdf#nameddest=sec:curvaturas-principales)
      ([teorema de Euler](../../apunte.pdf#nameddest=teo:euler): los extremos a $\pi/2$, con la precisión de que la
      perpendicularidad es sobre la superficie, $d_1^T I\, d_2 = 0$; la curvatura de Gauss) ·
      [teorema de Meusnier](../../apunte.pdf#nameddest=teo:meusnier) ($x' = N\cos\varphi$ en el paralelo) ·
      [las dos formas cambian por congruencia](../../apunte.pdf#nameddest=prop:II-congruencia)
    - [apunte, capítulo «Geometría del elipsoide», sección «Radios de curvatura M y N»](../../apunte.pdf#nameddest=sec:radios-MN):
      $M$, $N$, $K = 1/(MN)$, el radio medio $R = \sqrt{MN}$ y por qué meridiano y primer vertical son las
      direcciones principales del elipsoide
    - [apunte, capítulo «Coordenadas sobre la esfera y trigonometría esférica»](../../apunte.pdf#nameddest=cap:esfera):
      los círculos máximos como las «rectas» de la esfera
    - [ficha del capítulo 13](../../capitulos/12.html) · [el hilo conductor](../../index.html) · [unidad 10](../10_jacobiano_primera_forma/index.html)

    **Lo que viene:** [Geometría del elipsoide](../13_elipsoide/index.html) (unidad 13): una superficie donde $\kappa_1 = 1/M$
    y $\kappa_2 = 1/N$ se deducen de una sola simetría, y la normal no pasa por el centro.
    """)
    return


@app.cell
def _(D, E, F, G, H, K, L, M, N, apart, k1, k2, kn, lib, mo, np, ok_cilindro, ok_esfera, silla):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _ff = lib.formas_fundamentales(lambda x, y: lib.xyz(x, y, silla(x, y)), 0.0, 0.0)
    _checks = [
        ("sección 0: silla, apartamientos +0.25 (este), −0.25 (norte), 0 (45°)", lib.exacto([apart["este"], apart["norte"], apart["45°"]], [0.25, -0.25, 0.0])),
        ("sección 2: K = κ₁κ₂ = det II / det I y H = (κ₁ + κ₂)/2", lib.exacto(K, k1 * k2, tol=1e-9) and lib.exacto(K, (L * N - M**2) / (E * G - F**2), tol=1e-9) and lib.exacto(H, (k1 + k2) / 2, tol=1e-9)),
        ("sección 2: κ₂ ≤ κₙ(α) ≤ κ₁ y las direcciones principales son I-ortonormales", k2 - 1e-9 <= kn <= k1 + 1e-9 and lib.exacto(D.T @ np.array([[E, F], [F, G]]) @ D, np.eye(2), tol=1e-6)),
        ("sección 3: esfera κ₁ = κ₂ = 1/R, K = 1/R²; cilindro κ = (1/R, 0), K = 0", ok_esfera and ok_cilindro),
        ("ejercicio (a): silla en el origen, II = diag(1/2, −1/2), K = −1/4, κₙ(45°) = 0",
         lib.exacto([_ff[k] for k in "LMN"], [0.5, 0, -0.5], tol=1e-7) and lib.exacto(lib.curvatura_gauss(*(_ff[k] for k in "EFGLMN"))[0], -0.25, tol=1e-7)
         and lib.exacto(lib.curvatura_normal(*(_ff[k] for k in "EFGLMN"), 1, 1), 0.0, tol=1e-7)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
