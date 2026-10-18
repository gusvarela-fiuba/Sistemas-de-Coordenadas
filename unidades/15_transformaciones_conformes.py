# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Transformaciones conformes (unidad 15, molde v2 sobre cb104). Cierre del arco: clases 13 y 14.

DESARROLLO COMPLEMENTARIO del curso, pendiente de validar por la cátedra. Una sola idea: una transformación es
conforme cuando, mirada con lupa, es una similaridad directa; eso se escribe de cuatro maneras equivalentes (Jacobiano
k·R(θ) = número complejo; σ₁ = σ₂, Tissot círculo; F = 0 y E = G; Cauchy-Riemann) y resuelve el "puntapié inicial" del
apunte del elipsoide del profesor: Mercator con la latitud isométrica, las cilíndricas equidistante y equivalente, y
Gauss-Krüger como función analítica de q + iΔλ.

Chequear:  uv run marimo check --select MW unidades/15_transformaciones_conformes.py
Exportar:  uv run python tools/build.py --only 15_transformaciones_conformes
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
    # Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    *Desarrollo complementario del curso, cierre del arco: no corresponde a una clase dictada; toma el "puntapié
    inicial" de la última página del apunte del profesor sobre el elipsoide, pendiente de validar por la cátedra.*

    Cerramos el arco que abrió la clase 1. La pregunta: **¿qué tiene que cumplir una transformación para conservar los
    ángulos, y cómo se lleva el elipsoide al plano sin torcer una sola visual?** El gancho: *dos visuales a $90°$
    medidas con la estación total siguen a $90°$ en la hoja sólo si la proyección es conforme: Mercator, Gauss-Krüger,
    POSGAR.*

    Colores, iguales en la figura y en el álgebra: el **terreno** y su grilla métrica en **gris**; las imágenes por la
    proyección en <span style="color:#1b6f6a">**teal**</span>; las dos visuales de la estación en
    <span style="color:#b5451b">**rust**</span> y <span style="color:#c9a227">**gold**</span>; el círculo de Tissot
    del punto elegido en <span style="color:#7a4e9e">**violeta**</span>. En las matrices, la **primera columna** es
    teal y la **segunda** rust, como en todas las unidades. Grados en los controles, radianes adentro.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("15_transformaciones_conformes"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    grs80 = lib.elipsoide_grs80()
    phi_sit = np.deg2rad(-54.0)
    _M_sit, _N_sit = lib.radios_curvatura(phi_sit, grs80["a"], grs80["e2"])
    razon_sit = _N_sit * np.cos(phi_sit) / _M_sit  # cuánto mide el paralelo respecto del meridiano, en −54°
    J_sit = np.diag([1 / (_N_sit * np.cos(phi_sit)), 1 / _M_sit])  # (este, norte) en metros → (Δλ, Δφ) en radianes
    d_ne = np.array([np.sin(np.deg2rad(45.0)), np.cos(np.deg2rad(45.0))])  # visual a 45° (NE), (este, norte)
    d_se = np.array([np.sin(np.deg2rad(135.0)), np.cos(np.deg2rad(135.0))])  # visual a 135° (SE)
    ang_sit = np.rad2deg(lib.angulo(J_sit @ d_ne, J_sit @ d_se))
    omega_sit = lib.defecto_conformidad_jacobiano(J_sit)["def_angular_max_deg"]
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            "siguen a 90°: cambiar la escala de los ejes no cambia los ángulos": "misma",
            f"se cierran: el ángulo entre las visuales queda en unos {ang_sit:.0f}°": "correcta",
            f"se abren: el ángulo entre las visuales queda en unos {180 - ang_sit:.0f}°": "abren",
            "se tuercen apenas, menos de 1°: un grado de latitud y uno de longitud miden casi lo mismo": "poco",
        }),
        value=None,
        label="**Predicción.** En la hoja cuadriculada (λ, φ), las dos visuales que en el terreno forman 90° exactos…",
    )
    mo.vstack([
        mo.md(rf"""
        ## 0. Situación de campo y predicción

        Plantamos la estación total en Tierra del Fuego, $\varphi = -54°$, sobre GRS80. Medimos dos visuales que
        forman **$90°$ exactos**: una al rumbo $45°$ (NE) y otra al rumbo $135°$ (SE). Volcamos los puntos visados en
        una hoja cuadriculada usando directamente $(x, y) = (\lambda, \varphi)$, grados por grados, sin corregir la
        escala del meridiano: un cuadradito de la hoja es $1°$ de longitud por $1°$ de latitud.

        Lo que sabemos de la unidad 13: en $\varphi = -54°$ el paralelo mide $N\cos\varphi = {_N_sit * np.cos(phi_sit) / 1000:,.1f}$ km
        por radián y el meridiano $M = {_M_sit / 1000:,.1f}$ km por radián; un grado de longitud mide
        ${razon_sit:.3f}$ veces lo que un grado de latitud.
        """),
        prediccion,
    ])
    return J_sit, ang_sit, d_ne, d_se, grs80, omega_sit, phi_sit, prediccion, razon_sit


@app.cell
def _(ang_sit, lib, mo, np, omega_sit, prediccion, razon_sit, J_sit):
    _Js = J_sit / J_sit[1, 1]  # la misma matriz en unidades de "grados de latitud": diag(M/(N cos φ), 1)
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** El cuadradito del terreno se vuelve un rectángulo en la hoja: la hoja estira el este-oeste "
                     rf"${1 / razon_sit:.3f}$ veces respecto del norte-sur. El Jacobiano de terreno a hoja, en unidades de grados de "
                     rf"latitud, es $J = {lib.matriz_coloreada(_Js)}$: aplicado a las dos visuales el ángulo pasa de $90°$ a "
                     rf"${ang_sit:.1f}°$, una torcedura de ${90 - ang_sit:.1f}°$, casi la máxima posible en ese punto: "
                     rf"$\omega_{{\max}} = 2\arcsin\frac{{\sigma_1 - \sigma_2}}{{\sigma_1 + \sigma_2}} = {omega_sit:.1f}°$ (Tissot). "
                     r"La salida es estirar también el norte-sur, con la **latitud isométrica**: eso es Mercator."),
        "misma": ("warn",
                  rf"**No.** Una escala *uniforme* no cambia ángulos; acá la escala es distinta en cada eje "
                  rf"(${1 / razon_sit:.3f}$ en este-oeste contra $1$ en norte-sur) y eso es una afinidad, no una similaridad: "
                  rf"el ángulo baja a ${ang_sit:.1f}°$. Lo que el agrimensor no negocia es el ángulo; la hoja $(\lambda, \varphi)$ lo negocia."),
        "abren": ("warn",
                  rf"**No**, el sentido: la hoja estira el este-oeste (un grado de longitud vale ${razon_sit:.3f}$ grados de latitud "
                  rf"en el terreno y en la hoja vale $1$). Las dos visuales se acuestan hacia el eje este y el ángulo entre ellas, "
                  rf"que lo contiene, se **cierra** a ${ang_sit:.1f}°$."),
        "poco": ("warn",
                 rf"**No.** En el ecuador sí ($N\cos\varphi \approx M$), pero en $-54°$ el paralelo mide ${razon_sit:.3f}$ del "
                 rf"meridiano y la torcedura es de ${90 - ang_sit:.1f}°$: más de ${np.floor(90 - ang_sit):.0f}°$, nada de apenas. "
                 r"A la latitud de Buenos Aires ya son más de $10°$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **El problema.** La unidad 12 dejó $K = 1/(MN) > 0$ para el elipsoide y el plano tiene $K = 0$. Gauss (*theorema
    egregium*): la curvatura no cambia al doblar sin estirar; entonces **no existe** ninguna transformación del
    elipsoide al plano que conserve todas las distancias, ni siquiera en un entorno chico. Algo hay que sacrificar.
    Lo que el agrimensor no negocia es el **ángulo**: la estación mide direcciones, y la poligonal se calcula con
    ellas. Eso define la **transformación conforme**: la que conserva ángulos entre curvas, aunque cambie la escala
    de un punto a otro.

    **¿Qué se conserva?** Los ángulos; y con ellos la *forma* de las figuras chicas. Lo que cambia es la escala
    $k(P)$, que depende del punto. Esto se escribe de **cuatro maneras equivalentes**, una por unidad del curso:

    | cara | álgebra | lo que se ve |
    |---|---|---|
    | **A** · similaridad (unidad 03) | con lupa infinitesimal, $J = k(P)\,R(\theta)$: rotación más escala uniforme | un cuadradito del terreno va a un cuadradito girado, más grande o más chico |
    | **B** · SVD (unidad 09) | $\sigma_1 = \sigma_2$ y $\det J > 0$; la elipse imagen del círculo unitario es un círculo, recorrido en el mismo sentido | la **indicatriz de Tissot** es un círculo; si no, elipse, y la deformación angular máxima es $\omega_{\max} = 2\arcsin\dfrac{\sigma_1 - \sigma_2}{\sigma_1 + \sigma_2}$ |
    | **C** · primera forma (unidad 10) | en bases ortonormales (metros) del terreno y del mapa, $F = 0$ y $E = G = k^2$, con $\det J > 0$: $ds^2_{\text{mapa}} = k^2\,ds^2_{\text{terreno}}$ | las líneas coordenadas se cortan a $90°$ y los dos pasos de grilla miden lo mismo: cuadraditos a cuadraditos |
    | **D** · número complejo (unidades 00 y 01a-01c, clase 1) | entre planos, $J = \begin{pmatrix} a & -b \\ b & a \end{pmatrix}$: multiplicar por $a + ib$; $u_x = v_y$, $u_y = -v_x$ (**Cauchy-Riemann**) | toda función analítica $w = f(z)$ con $f'(z) \ne 0$ es conforme: la lupa ve "multiplicar por el complejo $f'(z)$" |

    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    > **⚠ ¿Sobre qué Jacobiano pedimos $J^T J = k^2 I$? Coordenadas $(\varphi, \lambda)$ vs. metros en el plano tangente**
    >
    > **En coordenadas.** Si derivamos la carta $\Phi(\varphi, \lambda) = (x, y)$ respecto de las coordenadas geodésicas en
    > radianes, obtenemos el Jacobiano de coordenadas $J_{\varphi,\lambda} = \partial(x,y)/\partial(\varphi,\lambda)$.
    > Pero $(\varphi, \lambda)$ no están en metros ni son isótropas: el elipsoide tiene la primera forma fundamental
    > $\mathbf{G} = \operatorname{diag}(M^2,\, N^2\cos^2\varphi)$ (la matriz de la primera forma: $E = M^2$, $F = 0$, $G = N^2\cos^2\varphi$). La condición exacta de conformidad es entonces
    > $$J_{\varphi,\lambda}^T\, J_{\varphi,\lambda} = k(\varphi,\lambda)^2\, \mathbf{G} = k^2 \begin{pmatrix} M^2 & 0 \\ 0 & N^2\cos^2\varphi \end{pmatrix}.$$
    > Pedir $J_{\varphi,\lambda}^T J_{\varphi,\lambda} = k^2 I$ directo sobre $(\varphi, \lambda)$ sería el error de la hoja
    > cuadriculada de la sección 0: tratar radianes de latitud y de longitud como si midieran lo mismo.
    >
    > **En metros.** Cuando pasamos a la base ortonormal en metros del plano tangente ($ds_{\text{mer}} = M\, d\varphi$,
    > $ds_{\text{par}} = N\cos\varphi\, d\lambda$), el Jacobiano físico es
    > $$\tilde{J} = J_{\varphi,\lambda}\, \mathbf{G}^{-1/2} = J_{\varphi,\lambda}\, \operatorname{diag}\!\left(\frac{1}{M},\, \frac{1}{N\cos\varphi}\right),$$
    > y recién ahí la condición toma la forma euclídea $\tilde{J}^T \tilde{J} = k^2 I$ (con $\det \tilde{J} > 0$ para
    > conservar la orientación). El $\tilde{J}$ es el que mira la unidad (la cara A de la tabla), y $h$ y $k$ son sus
    > escalas en meridiano y paralelo. (El $J = \begin{pmatrix} 3 & -4 \\ 4 & 3 \end{pmatrix}$ de la sección 3.1 es de este
    > tipo: físico, en metros.)
    >
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **Conforme es una propiedad local.** Una proyección conforme conserva exactamente el ángulo en el punto donde se
    cortan dos curvas y lleva circulitos infinitesimales en circulitos. Pero el factor de escala $k(P)$ varía con la
    posición, así que las figuras extensas no mantienen ni su área ni su forma global (Groenlandia en Mercator parece
    del tamaño de África). Por eso, en la Argentina, POSGAR divide el país en 7 fajas de Gauss-Krüger de $3^\circ$ de
    ancho: no para "mantener la conformidad" (Gauss-Krüger ya es conforme a cualquier distancia del meridiano
    central), sino para acotar la deformación lineal $k - 1 \approx \tfrac{1}{2}\,\Delta\lambda^2 \cos^2\varphi$ (con
    $\Delta\lambda$ en radianes) por debajo de unos $3{,}4 \times 10^{-4}$, es decir $34$ cm/km, en el borde de la faja
    ($\Delta\lambda = 1{,}5^\circ$). Lo calculamos:
    """)
    return


@app.cell
def _(mo, np):
    _dl = np.radians(1.5)
    _filas = []
    for _nombre, _phi in [("ecuador, $\\varphi = 0$", 0.0), ("Buenos Aires, $\\varphi = -34{,}6^\\circ$", -34.6)]:
        _kk = 0.5 * _dl**2 * np.cos(np.radians(_phi)) ** 2
        _filas.append(f"| {_nombre} | {_kk:.2e} | {_kk * 1e5:.1f} |")
    mo.md(
        "| lugar (borde de faja, $\\Delta\\lambda = 1{,}5^\\circ$) | $k - 1$ | cm/km |\n|---|---|---|\n"
        + "\n".join(_filas)
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    La escalera: en $\mathbb R$ toda transformación $x \mapsto kx$ con $k > 0$ conserva "el ángulo" (no hay otro que
    $0$ o $180°$); en $\mathbb R^2$ conservar ángulos obliga a $J = kR(\theta)$, que es el número complejo de la
    clase 1; en $\mathbb R^3$ las conformes son mucho más pocas (Liouville: similaridades e inversiones), por eso la
    cartografía es un problema del plano.

    **Las cinco preguntas de la última página del apunte del elipsoide** (el "puntapié inicial" del profesor) se
    responden con esto. En las cilíndricas normales tomamos $x = a\lambda$ y queda por elegir $y(\varphi)$; la escala a
    lo largo del paralelo es siempre $k = \dfrac{a}{N\cos\varphi}$ y a lo largo del meridiano $h = \dfrac{y'(\varphi)}{M}$:

    1. **Mercator** (conforme): pedimos $h = k$, o sea $y' = \dfrac{aM}{N\cos\varphi}$. La integral es la **latitud
       isométrica** $q(\varphi) = \ln\tan\!\left(\dfrac{\pi}{4} + \dfrac{\varphi}{2}\right) - \dfrac{e}{2}\ln\dfrac{1 + e\sin\varphi}{1 - e\sin\varphi}$
       y $y = a\,q(\varphi)$. Con $q$ como coordenada norte, $ds^2 = N^2\cos^2\varphi\,(dq^2 + d\lambda^2)$: cara C.
    2. **Cilíndrica equidistante**: $h = 1$, $y = S(\varphi) = \int_0^\varphi M\,du$, el arco de meridiano del apunte.
    3. **Cilíndrica equivalente**: $hk = 1$, $y = \dfrac{1}{a}\int_0^\varphi MN\cos u\,du$; conserva áreas y aplasta ángulos.
    4. **Esfera autálica**: la esfera de igual área que el elipsoide, con la latitud $\beta_A$ tal que $\sin\beta_A$ es
       proporcional a la misma integral de 3: elipsoide $\to$ esfera equivalente, y de ahí cualquier proyección esférica.
    5. **Mercator transversa / Gauss-Krüger** (la de POSGAR): el cilindro tangente a un meridiano, no al ecuador. Por la
       cara D, es $w = f(q + i\,\Delta\lambda)$ con $f$ analítica, elegida para que sobre el meridiano central
       ($\Delta\lambda = 0$) la ordenada sea $S(\varphi)$. Lo planteamos en la sección 3.

    Esto es una **muestra** (la figura y los números lo muestran); la **demostración** de que las cuatro caras son la
    misma cosa, y la deducción de $q(\varphi)$, están en el apunte (ver anexo).
    """)
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("06_conforme_tissot_mercator", "Lado a lado, la cilíndrica equidistante (no conforme) y Mercator (conforme) con los círculos de Tissot y dos visuales a 90°: en la primera los círculos se vuelven elipses y el ángulo se tuerce; en Mercator los círculos crecen pero siguen círculos y el ángulo sigue en 90°."))
    return


@app.cell
def _(mo):
    # ---------- casos precargados: etiqueta → (tipo, qué pasa) ----------
    casos = {
        "Mercator (conforme: h = k, círculos en círculos)": (
            "conforme_mercator",
            r"$y = a\,q(\varphi)$: $h = k = a/(N\cos\varphi)$ en todo punto, $\omega_{\max} = 0$; los círculos de Tissot crecen hacia el polo pero siguen círculos y las dos visuales siguen a $90°$.",
        ),
        "cilíndrica equidistante (h = 1, estira en E-O)": (
            "equidistante",
            r"$y = S(\varphi)$: el meridiano se dibuja a escala $1$ pero el paralelo se estira $k = a/(N\cos\varphi)$; los círculos se vuelven elipses acostadas y el ángulo entre las visuales se cierra.",
        ),
        "cilíndrica equivalente (h·k = 1, conserva áreas, aplasta ángulos)": (
            "equivalente",
            r"$y = \frac{1}{a}\int_0^\varphi MN\cos u\,du$: lo que el paralelo se estira ($k$) el meridiano se aplasta ($h = 1/k$); la elipse de Tissot tiene el área del círculo y el ángulo se tuerce casi el doble que en la equidistante.",
        ),
        "mapa complejo en el plano: w = z², e^z o z + α z̄": (
            "complejo",
            r"$z^2$ y $e^z$ son analíticas: su Jacobiano es multiplicar por el complejo $f'(z)$, los cuadraditos van a cuadraditos curvos y el círculo sigue círculo. $z + \alpha\bar z$ no es analítica ($\bar z$ rompe Cauchy-Riemann): con $\alpha \ne 0$ el círculo se vuelve elipse.",
        ),
    }
    caso = mo.ui.dropdown(options=list(casos), value="cilíndrica equidistante (h = 1, estira en E-O)", label="caso precargado")
    mo.md(r"""
    ## 2. Manipulación

    A la izquierda, dos paneles: el **terreno** (grilla de cuadraditos métricos, en unidades de $a$, con un círculo de
    Tissot en los paralelos $0°$, $-34.6°$, $-54°$ y $-65°$ y las dos visuales a $90°$ en la latitud elegida) y el
    **mapa** proyectado. Las imágenes son por el Jacobiano de la proyección en cada punto (la lupa infinitesimal, dibujada
    grande). En el modo complejo, el panel izquierdo es un trozo del plano $z$ y el derecho su imagen por $w = f(z)$. A la
    derecha, los controles y los números vivos: el Jacobiano $J$ en el punto elegido, $h$, $k$, $hk = \det J$, $\omega_{\max}$ y
    el ángulo entre las dos visuales antes y después.
    """)
    return caso, casos


@app.cell
def _(caso, casos, mo):
    _tipo, _ = casos[caso.value]
    es_complejo = _tipo == "complejo"
    phi_s = mo.ui.slider(-75, 75, value=-54, step=1, label="latitud φ (°)", show_value=True, disabled=es_complejo)
    rumbo_s = mo.ui.slider(0, 180, value=45, step=1, label="rumbo α (°) de la primera visual", show_value=True)
    alfa_s = mo.ui.slider(0, 0.8, value=0.3, step=0.05, label="α no conforme (sólo en z + α z̄)", show_value=True, disabled=not es_complejo)
    funcion = mo.ui.dropdown(options=["w = z²", "w = e^z", "w = z + α·z̄"], value="w = z²", label="función compleja", disabled=not es_complejo)
    return alfa_s, es_complejo, funcion, phi_s, rumbo_s


@app.cell
def _(alfa_s, caso, casos, es_complejo, funcion, go, grs80, lib, mo, np, phi_s, rumbo_s):
    tipo, _que_pasa = casos[caso.value]
    _a, _e2 = grs80["a"], grs80["e2"]
    _t = np.linspace(0, 2 * np.pi, 121)
    _circ = np.column_stack([np.cos(_t), np.sin(_t)])
    _cuad = np.array([[-1, -1], [1, -1], [1, 1], [-1, 1], [-1, -1]], dtype=float)
    _alpha = np.deg2rad(rumbo_s.value)
    d1 = np.array([np.sin(_alpha), np.cos(_alpha)])  # (este, norte): rumbo desde el norte, horario
    d2 = np.array([np.sin(_alpha + np.pi / 2), np.cos(_alpha + np.pi / 2)])

    def _trazo(fig, puntos, color, nombre, ancho=2, relleno=None, mostrar=True, dash=None):
        fig.add_trace(go.Scatter(x=puntos[:, 0], y=puntos[:, 1], mode="lines", line=dict(color=color, width=ancho, dash=dash),
                                 fill=relleno, fillcolor=lib._rgba(color, 0.12) if relleno else None,
                                 name=nombre, showlegend=mostrar, hoverinfo="skip"))

    if not es_complejo:
        _r = 0.07  # radio del círculo de Tissot, en unidades de a (≈ 450 km): la lupa, dibujada grande
        _phis_ref = [0.0, -34.6, -54.0, -65.0]
        _phi = np.deg2rad(phi_s.value)
        _S = lambda p: lib.arco_meridiano(p, _a, _e2) / _a  # noqa: E731
        _proy = lambda p: lib.escalas_proyeccion_cilindrica(p, tipo, grs80)  # noqa: E731
        _y_v, h_v, k_v, omega_v = _proy(_phi)
        J = np.diag([k_v, h_v])  # (este, norte) del terreno → (x, y) del mapa

        _ymin = min(_S(np.deg2rad(-75.0)), _proy(np.deg2rad(-75.0))[0] / _a) - 0.45
        _f_terreno = lib.figura_plano((_ymin, 0.4), "terreno (unidades de a)", ancho=370, alto=470)
        _f_terreno.update_xaxes(range=[-0.75, 0.75], title="este / a (local)")
        _f_terreno.update_yaxes(title="S(φ) / a")
        _f_mapa = lib.figura_plano((_ymin, 0.4), f"mapa: {caso.value.split(' (')[0]}", ancho=370, alto=470)
        _f_mapa.update_xaxes(range=[-0.75, 0.75], title="x = a λ  (/ a)")
        _f_mapa.update_yaxes(title="y / a")
        for _x in (-0.6, -0.3, 0.0, 0.3, 0.6):
            _f_mapa.add_trace(go.Scatter(x=[_x, _x], y=[_ymin, 0.4], mode="lines", line=dict(color="#d8d3c8", width=1), showlegend=False, hoverinfo="skip"))
        for _i, _pd in enumerate(_phis_ref):
            _p = np.deg2rad(_pd)
            _c = np.array([0.0, _S(_p)])
            _ym, _h, _k, _ = _proy(_p)
            _cm = np.array([0.0, _ym / _a])
            _Ji = np.diag([_k, _h])
            _f_terreno.add_trace(go.Scatter(x=[-0.75, 0.75], y=[_c[1], _c[1]], mode="lines", line=dict(color="#d8d3c8", width=1), showlegend=False, hoverinfo="skip"))
            _f_mapa.add_trace(go.Scatter(x=[-0.75, 0.75], y=[_cm[1], _cm[1]], mode="lines", line=dict(color="#d8d3c8", width=1), showlegend=False, hoverinfo="skip"))
            _trazo(_f_terreno, _c + _r * _cuad, lib.GRIS_ANTES, "cuadradito métrico", mostrar=_i == 0)
            _trazo(_f_terreno, _c + _r * _circ, lib.TEAL_DESPUES, "círculo de Tissot (terreno)", relleno="toself", mostrar=_i == 0)
            _trazo(_f_mapa, _cm + lib.transformar(_r * _cuad, _Ji), lib.GRIS_ANTES, "imagen del cuadradito", mostrar=_i == 0)
            _trazo(_f_mapa, _cm + lib.transformar(_r * _circ, _Ji), lib.TEAL_DESPUES, "indicatriz de Tissot", relleno="toself", mostrar=_i == 0)
            _f_terreno.add_trace(go.Scatter(x=[-0.55], y=[_c[1] + 0.05], mode="text", text=[f"φ = {_pd:g}°"], textfont=dict(size=10, color="#555"), showlegend=False, hoverinfo="skip"))
        _c = np.array([0.0, _S(_phi)])
        _cm = np.array([0.0, _y_v / _a])
        _trazo(_f_terreno, _c + _r * _circ, lib.VIOLETA_OBJETO, f"círculo en φ = {phi_s.value}°", ancho=2.5)
        _trazo(_f_mapa, _cm + lib.transformar(_r * _circ, J), lib.VIOLETA_OBJETO, f"su imagen en φ = {phi_s.value}°", ancho=2.5)
        _L = 1.7 * _r
        lib.flecha(_f_terreno, _c, _c + _L * d1, lib.COLORES[1], f"visual al rumbo {rumbo_s.value}°", ancho=4)
        lib.flecha(_f_terreno, _c, _c + _L * d2, lib.COLORES[2], f"visual al rumbo {rumbo_s.value + 90}°", ancho=4)
        lib.flecha(_f_mapa, _cm, _cm + _L * (J @ d1), lib.COLORES[1], "imagen de la primera visual", ancho=4)
        lib.flecha(_f_mapa, _cm, _cm + _L * (J @ d2), lib.COLORES[2], "imagen de la segunda", ancho=4)
        _dc = lib.defecto_conformidad_jacobiano(J)
        _lineas_vivas = [
            rf"- escalas: $h = {h_v:.4f}$ (meridiano), $k = {k_v:.4f}$ (paralelo); $hk = \det J = {h_v * k_v:.4f}$",
            rf"- Tissot: $\sigma_1 = {_dc['sigmas'][0]:.4f}$, $\sigma_2 = {_dc['sigmas'][1]:.4f}$, $\sigma_1/\sigma_2 = {_dc['razon']:.4f}$",
            rf"- $y(\varphi) = {_y_v / 1000:,.1f}$ km; en el ecuador las tres proyecciones dan $h = k = 1$",
        ]
    else:
        _alfa = alfa_s.value
        _z0 = np.array([1.4, 1.0])
        if funcion.value == "w = z²":
            _f = lambda P: np.column_stack([P[:, 0] ** 2 - P[:, 1] ** 2, 2 * P[:, 0] * P[:, 1]])  # noqa: E731
            J = np.array([[2 * _z0[0], -2 * _z0[1]], [2 * _z0[1], 2 * _z0[0]]])
        elif funcion.value == "w = e^z":
            _f = lambda P: np.column_stack([np.exp(P[:, 0]) * np.cos(P[:, 1]), np.exp(P[:, 0]) * np.sin(P[:, 1])])  # noqa: E731
            J = np.exp(_z0[0]) * lib.rot2(_z0[1])
        else:
            _f = lambda P: np.column_stack([(1 + _alfa) * P[:, 0], (1 - _alfa) * P[:, 1]])  # noqa: E731
            J = np.diag([1 + _alfa, 1 - _alfa])
        _r = 0.12
        _xs, _ys = np.arange(0.8, 2.01, 0.2), np.arange(0.4, 1.61, 0.2)
        _lineas = [np.column_stack([np.full(41, x), np.linspace(0.4, 1.6, 41)]) for x in _xs] + \
                  [np.column_stack([np.linspace(0.8, 2.0, 41), np.full(41, y)]) for y in _ys]
        _im = [_f(l) for l in _lineas]
        _todo = np.vstack(_im)
        _f_terreno = lib.figura_plano((0.0, 2.4), "plano z: cuadraditos y círculo", ancho=370, alto=470)
        _f_terreno.update_xaxes(title="x = Re z")
        _f_terreno.update_yaxes(title="y = Im z")
        _lo, _hi = _todo.min(axis=0) - 0.3, _todo.max(axis=0) + 0.3
        _f_mapa = lib.figura_plano((min(_lo), max(_hi)), f"plano w: {funcion.value}", ancho=370, alto=470)
        _f_mapa.update_xaxes(range=[_lo[0], _hi[0]], title="u = Re w")
        _f_mapa.update_yaxes(range=[_lo[1], _hi[1]], title="v = Im w")
        for _i, (_l, _w) in enumerate(zip(_lineas, _im)):
            _trazo(_f_terreno, _l, lib.GRIS_ANTES, "grilla", ancho=1, mostrar=_i == 0)
            _trazo(_f_mapa, _w, lib.TEAL_DESPUES, "imagen de la grilla", ancho=1.5, mostrar=_i == 0)
        _trazo(_f_terreno, _z0 + _r * _circ, lib.VIOLETA_OBJETO, "círculo de Tissot", ancho=2.5, relleno="toself")
        _trazo(_f_mapa, _f(_z0 + _r * _circ), lib.VIOLETA_OBJETO, "su imagen (exacta)", ancho=2.5, relleno="toself")
        _w0 = _f(_z0.reshape(1, 2))[0]
        _L = 2.0 * _r
        lib.flecha(_f_terreno, _z0, _z0 + _L * d1, lib.COLORES[1], f"visual al rumbo {rumbo_s.value}°", ancho=4)
        lib.flecha(_f_terreno, _z0, _z0 + _L * d2, lib.COLORES[2], f"visual al rumbo {rumbo_s.value + 90}°", ancho=4)
        lib.flecha(_f_mapa, _w0, _w0 + _L * (J @ d1), lib.COLORES[1], "imagen por J de la primera", ancho=4)
        lib.flecha(_f_mapa, _w0, _w0 + _L * (J @ d2), lib.COLORES[2], "imagen por J de la segunda", ancho=4)
        _dc = lib.defecto_conformidad_jacobiano(J)
        h_v, k_v = _dc["sigmas"]
        omega_v = _dc["def_angular_max_deg"]
        _lineas_vivas = [
            rf"- en $z_0 = {_z0[0]:g} + {_z0[1]:g}i$: $\sigma_1 = {h_v:.4f}$, $\sigma_2 = {k_v:.4f}$, $\sigma_1/\sigma_2 = {_dc['razon']:.4f}$; $\det J = {np.linalg.det(J):.4f}$",
            rf"- parte conforme ${lib.pmat(_dc['parte_conforme'])}$, parte anticonforme ${lib.pmat(_dc['parte_anticonforme'])}$",
        ]
    ang_despues = np.rad2deg(lib.angulo(J @ d1, J @ d2))
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, phi_s, rumbo_s, funcion, alfa_s,
        mo.md("\n".join([
            "**Números vivos**", "",
            rf"$$J = {lib.matriz_coloreada(J, dec=4)}$$", "",
            *_lineas_vivas,
            rf"- deformación angular máxima $\omega_{{\max}} = 2\arcsin\frac{{\sigma_1 - \sigma_2}}{{\sigma_1 + \sigma_2}} = \mathbf{{{omega_v:.3f}°}}$",
            rf"- ángulo entre las dos visuales: antes $90°$, después $\mathbf{{{ang_despues:.3f}°}}$", "",
            f"**Qué pasa acá:** {_que_pasa}",
        ])),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.hstack([mo.ui.plotly(_f_terreno), mo.ui.plotly(_f_mapa)], widths="equal", gap=0.5), _panel)
    return J, ang_despues, d1, d2, h_v, k_v, omega_v, tipo


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Cuenta a mano y código lado a lado

    Izquierda, la cuenta del cuaderno; derecha, la misma en numpy con los helpers de `cb104` y `np.allclose` contra
    los números de la izquierda.
    """)
    return


@app.cell
def _(lib, mo, np):
    _J = np.array([[3.0, -4.0], [4.0, 3.0]])
    _JtJ = _J.T @ _J
    _dc = lib.defecto_conformidad_jacobiano(_J)
    ok_31 = bool(np.allclose(_JtJ, 25 * np.eye(2))) and bool(np.allclose(_dc["sigmas"], [5, 5])) and _dc["def_angular_max_deg"] == 0.0
    mo.hstack([
        mo.md(rf"""
        **3.1 Por qué $\begin{{pmatrix}} a & -b \\ b & a \end{{pmatrix}}$ conserva ángulos.** Con $a = 3$, $b = 4$:

        $$J^T J = {lib.pmat(_J.T, dec=0)} {lib.matriz_coloreada(_J, dec=0)} = {lib.pmat(_JtJ, dec=0)} = (a^2 + b^2)\,I.$$

        Entonces $\langle Ju, Jv\rangle = u^T J^T J v = 25\,\langle u, v\rangle$ y $\lVert Ju \rVert = 5\lVert u \rVert$: el coseno
        del ángulo no cambia. Los valores singulares son las raíces de los autovalores de $J^T J$:
        $\sigma_1 = \sigma_2 = \sqrt{{a^2 + b^2}} = 5$, y $\omega_{{\max}} = 2\arcsin\frac{{0}}{{10}} = 0$. Es multiplicar por el
        complejo $3 + 4i$: módulo $5$, giro $\arctan(4/3)$.
        """),
        mo.vstack([
            mo.md("```python\nJ = np.array([[3.0, -4.0], [4.0, 3.0]])\nJ.T @ J                 # 25 I\nd = lib.defecto_conformidad_jacobiano(J)\nd[\"sigmas\"], d[\"def_angular_max_deg\"]\nnp.allclose(J.T @ J, 25 * np.eye(2))\n```"),
            mo.md(f"`J.T @ J` = `{_JtJ.tolist()}` · `sigmas` = `{tuple(round(s, 6) for s in _dc['sigmas'])}` · `ω` = `{_dc['def_angular_max_deg']}` · `allclose` = `{ok_31}`"),
        ]),
    ], widths="equal", align="start")
    return (ok_31,)


@app.cell
def _(grs80, lib, mo, np):
    _e = np.sqrt(grs80["e2"])
    _filas = []
    for _pd in (-34.6, -54.0):
        _p = np.deg2rad(_pd)
        _q = float(lib.latitud_isometrica(_p, _e))
        _fila = [f"| ${_pd:g}°$ | ${_q:.5f}$ "]
        for _tipo, _nom in (("conforme_mercator", "Mercator"), ("equidistante", "equidistante"), ("equivalente", "equivalente")):
            _y, _h, _k, _w = lib.escalas_proyeccion_cilindrica(_p, _tipo, grs80)
            _fila.append(f"| ${_y / 1000:,.1f}$ · ${_h:.4f}$ · ${_k:.4f}$ · ${_w:.2f}°$ ")
        _filas.append("".join(_fila) + "|")
    _tabla = "\n        ".join(_filas)
    _q54 = float(lib.latitud_isometrica(np.deg2rad(-54.0), _e))
    _q54_esf = float(np.log(np.tan(np.pi / 4 - np.deg2rad(27.0))))
    ok_32 = bool(np.isclose(_q54, -1.11875, atol=5e-6)) and bool(np.isclose(lib.escalas_proyeccion_cilindrica(np.deg2rad(-54.0), "conforme_mercator")[1], 1.69757, atol=5e-6))
    mo.hstack([
        mo.md(rf"""
        **3.2 Latitud isométrica y las tres cilíndricas en GRS80.** Con $e = \sqrt{{e^2}} = {_e:.6f}$ y $\varphi = -54°$:
        $\ln\tan(45° - 27°) = {_q54_esf:.5f}$ (sería la esfera) y la corrección del elipsoide
        $-\frac{{e}}{{2}}\ln\frac{{1 + e\sin\varphi}}{{1 - e\sin\varphi}} = {_q54 - _q54_esf:+.5f}$: $q(-54°) = {_q54:.5f}$. Mercator pone
        $y = a\,q = {grs80["a"] * _q54 / 1000:,.1f}$ km y la escala $h = k = a/(N\cos\varphi) = 1.6976$. La equidistante pone
        $y = S(-54°)$ con $h = 1$ y la equivalente $h = 1/k = 0.5891$. Columnas: $y$ (km) · $h$ · $k$ · $\omega_{{\max}}$.

        | $\varphi$ | $q(\varphi)$ | Mercator | equidistante | equivalente |
        |---|---|---|---|---|
        {_tabla}
        """),
        mo.vstack([
            mo.md("```python\ng = lib.elipsoide_grs80()\ne = np.sqrt(g[\"e2\"])\nphi = np.deg2rad(-54.0)\nq = lib.latitud_isometrica(phi, e)\nfor t in (\"conforme_mercator\",\n          \"equidistante\", \"equivalente\"):\n    y, h, k, w = (\n        lib.escalas_proyeccion_cilindrica(\n            phi, t, g))\n    print(t, y, h, k, w)\nnp.isclose(q, -1.11875, atol=5e-6)\n```"),
            mo.md(f"`q(-54°)` = `{_q54:.6f}` · `isclose` (q y h de Mercator) = `{ok_32}`"),
        ]),
    ], widths="equal", align="start")
    return (ok_32,)


@app.cell
def _(grs80, lib, mo, np):
    _a, _e2 = grs80["a"], grs80["e2"]
    _e = np.sqrt(_e2)
    _phi = np.deg2rad(-34.6)
    _M, _N = lib.radios_curvatura(_phi, _a, _e2)
    _dq = 1e-6
    # S como función de q: derivamos numéricamente S(φ(q)) respecto de q con dφ = dq · N cos φ / M
    _dphi = _dq * _N * np.cos(_phi) / _M
    _dS_dq = (lib.arco_meridiano(_phi + _dphi, _a, _e2) - lib.arco_meridiano(_phi - _dphi, _a, _e2)) / (2 * _dq)
    ok_33 = bool(np.isclose(_dS_dq, _N * np.cos(_phi), rtol=1e-6))
    mo.hstack([
        mo.md(rf"""
        **3.3 Gauss-Krüger: el planteo.** Tomamos la coordenada compleja del elipsoide $\zeta = q + i\,\Delta\lambda$ (con
        $q$ y $\lambda$ la grilla es conforme, cara C) y buscamos $w = N_{{\text{{orte}}}} + i\,E_{{\text{{ste}}}} = f(\zeta)$ con $f$
        **analítica** (cara D: conforme) y una sola condición: sobre el meridiano central, $\Delta\lambda = 0$, la ordenada es el
        arco de meridiano, $f(q) = S(\varphi(q))$. Eso fija $f$: una función analítica que es real sobre el eje real queda
        determinada por sus valores ahí. Taylor en $i\,\Delta\lambda$:

        $$f(q + i\,\Delta\lambda) = S + i\,\Delta\lambda\,\frac{{dS}}{{dq}} - \frac{{\Delta\lambda^2}}{{2}}\frac{{d^2S}}{{dq^2}} - \cdots,
        \qquad \frac{{dS}}{{dq}} = M\frac{{d\varphi}}{{dq}} = N\cos\varphi.$$

        El primer término de $E$ es $N\cos\varphi\,\Delta\lambda$, el arco de paralelo: lejos del meridiano central la escala
        crece como $1 + \frac{{1}}{{2}}\cos^2\varphi\,\Delta\lambda^2$. La serie completa (hasta $\Delta\lambda^8$ en POSGAR) es cuenta,
        no idea: la idea es $w = f(q + i\,\Delta\lambda)$. En $\varphi = -34.6°$: $dS/dq = N\cos\varphi = {_N * np.cos(_phi) / 1000:,.3f}$ km.
        """),
        mo.vstack([
            mo.md("```python\ng = lib.elipsoide_grs80()\na, e2 = g[\"a\"], g[\"e2\"]\nphi = np.deg2rad(-34.6)\nM, N = lib.radios_curvatura(phi, a, e2)\ndq = 1e-6\ndphi = dq * N * np.cos(phi) / M\nS = lambda p: lib.arco_meridiano(p, a, e2)\ndS_dq = (S(phi + dphi)\n         - S(phi - dphi)) / (2 * dq)\nnp.isclose(dS_dq, N * np.cos(phi),\n           rtol=1e-6)\n```"),
            mo.md(f"`dS_dq` = `{_dS_dq:,.3f}` · `N cos φ` = `{_N * np.cos(_phi):,.3f}` · `isclose` = `{ok_33}`"),
        ]),
    ], widths="equal", align="start")
    return (ok_33,)


@app.cell
def _(go, grs80, lib, mo, np):
    _phis = np.arange(0.0, 70.01, 1.0)
    _curvas = {"conforme_mercator": "Mercator (h = k)", "equidistante": "equidistante (h = 1)", "equivalente": "equivalente (hk = 1)"}
    _col = dict(zip(_curvas, lib.COLORES))
    _dash = dict(conforme_mercator="solid", equidistante="dash", equivalente="dot")
    _res = {t: np.array([lib.escalas_proyeccion_cilindrica(np.deg2rad(p), t, grs80)[1:] for p in _phis]) for t in _curvas}
    _fig_hk = go.Figure(layout=go.Layout(width=380, height=380, margin=dict(l=40, r=10, t=50, b=40), plot_bgcolor="white",
                                        title=dict(text="escalas h (meridiano) y k (paralelo)", font=dict(size=14), x=0.01),
                                        xaxis=dict(title="|φ| (°)", gridcolor="#eceae4"), yaxis=dict(title="escala", gridcolor="#eceae4", range=[0, 3.2]),
                                        legend=dict(orientation="h", y=-0.25, font=dict(size=10))))
    _fig_w = go.Figure(layout=go.Layout(width=380, height=380, margin=dict(l=40, r=10, t=50, b=40), plot_bgcolor="white",
                                       title=dict(text="deformación angular máxima ω_max", font=dict(size=14), x=0.01),
                                       xaxis=dict(title="|φ| (°)", gridcolor="#eceae4"), yaxis=dict(title="ω_max (°)", gridcolor="#eceae4"),
                                       legend=dict(orientation="h", y=-0.25, font=dict(size=10))))
    for _t, _nom in _curvas.items():
        _fig_hk.add_trace(go.Scatter(x=_phis, y=_res[_t][:, 0], mode="lines", line=dict(color=_col[_t], width=2.5, dash=_dash[_t]), name=f"h · {_nom}"))
        _fig_w.add_trace(go.Scatter(x=_phis, y=_res[_t][:, 2], mode="lines", line=dict(color=_col[_t], width=2.5, dash=_dash[_t]), name=_nom))
    _fig_hk.add_trace(go.Scatter(x=_phis, y=_res["equidistante"][:, 1], mode="lines", line=dict(color="#555", width=1.5), name="k (las tres: a/(N cos φ))"))
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        **Una función que devuelve una tupla, y una comprensión que la apila.** `lib.escalas_proyeccion_cilindrica` devuelve
        `(y, h, k, ω)`; `[f(p)[1:] for p in phis]` toma las tres últimas de cada latitud y `np.array(...)` las apila en una
        matriz `(71, 3)`: una fila por latitud, columnas `h`, `k`, `ω`. Las curvas salen de indexar columnas, `res[:, 0]`,
        sin un solo bucle de dibujo. $k$ es la misma para las tres familias (todas tienen $x = a\lambda$); lo que cambia es $h$,
        y con él $\omega_{\max}$: $0$ en Mercator, casi el doble en la equivalente que en la equidistante ($\sin\frac{\omega}{2} = \tanh(\ln k)$ contra $\tanh(\tfrac12\ln k)$).
        """),
        mo.md("```python\nphis = np.arange(0.0, 70.01, 1.0)\nres = np.array([lib.escalas_proyeccion_cilindrica(np.deg2rad(p), \"equidistante\", g)[1:] for p in phis])   # (71, 3): h, k, ω\nres[:, 2]   # ω_max en grados, una por latitud\n```"),
        mo.hstack([mo.ui.plotly(_fig_hk), mo.ui.plotly(_fig_w)], widths="equal", gap=0.5),
        mo.md(f"`res.shape` = `{_res['equidistante'].shape}` · en $70°$: equidistante $\\omega = {_res['equidistante'][-1, 2]:.1f}°$, equivalente ${_res['equivalente'][-1, 2]:.1f}°$, Mercator ${_res['conforme_mercator'][-1, 2]:.1f}°$."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("toda función analítica es conforme").* Multiplicá dos matrices de la forma
        $\begin{pmatrix} a & -b \\ b & a \end{pmatrix}$ y $\begin{pmatrix} c & -d \\ d & c \end{pmatrix}$ y mostrá que el
        producto tiene la misma forma. ¿Qué dice eso de componer dos transformaciones conformes, y qué número complejo es?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $$\begin{pmatrix} a & -b \\ b & a \end{pmatrix}\begin{pmatrix} c & -d \\ d & c \end{pmatrix}
        = \begin{pmatrix} ac - bd & -(ad + bc) \\ ad + bc & ac - bd \end{pmatrix},$$

        que es $\begin{pmatrix} p & -q \\ q & p \end{pmatrix}$ con $p = ac - bd$, $q = ad + bc$: exactamente el producto
        $(a + ib)(c + id)$ de la clase 1. Componer dos conformes da una conforme, y la escala se multiplica
        ($\sqrt{p^2 + q^2} = \sqrt{a^2 + b^2}\sqrt{c^2 + d^2}$) mientras los giros se suman. Por la regla de la cadena, el
        Jacobiano de $g \circ f$ es $J_g J_f$: por eso una proyección conforme seguida de una similaridad (cambiar de faja,
        girar la hoja) sigue siendo conforme.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("cilíndrica equivalente").* En una cilíndrica normal $x = a\lambda$, $y = y(\varphi)$ sobre el
        elipsoide, deducí la condición sobre $y(\varphi)$ para que conserve áreas, y resolvela en la esfera ($M = N = R$).
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        Las escalas son $k = \dfrac{a}{N\cos\varphi}$ (paralelo) y $h = \dfrac{y'(\varphi)}{M}$ (meridiano); el Jacobiano es
        $\operatorname{diag}(k, h)$ y el área se multiplica por $\det J = hk$. Conservar áreas es $hk = 1$:

        $$y'(\varphi) = \frac{MN\cos\varphi}{a} \quad\Rightarrow\quad y(\varphi) = \frac{1}{a}\int_0^\varphi MN\cos u\,du.$$

        En la esfera, $y' = R\cos\varphi$ y $y = R\sin\varphi$: la cilíndrica equivalente de Lambert, que aplasta los polos
        contra $y = \pm R$. Sobre el elipsoide la integral es la misma que define la latitud autálica (pregunta 4 del
        apunte del profesor), y es elemental: $\int MN\cos u\,du = a^2(1 - e^2)\int \frac{\cos u\,du}{(1 - e^2\sin^2 u)^2}$.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def es_jacobiano_conforme(J, tol=1e-9):\n    J = np.asarray(J, dtype=float)\n    G = ...                 # J^T J\n    k2 = ...                # la escala al cuadrado: G[0, 0]\n    conserva_angulos = ...  # G == k2 * I, a menos de tol\n    directa = ...           # det J > 0 (sin espejo)\n    return bool(conserva_angulos and directa)\n",
        language="python", min_height=190, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("Jacobiano = similaridad directa").* Completá `es_jacobiano_conforme(J, tol)`:
        `True` si $J^T J = k^2 I$ con $k > 0$ (conserva ángulos) **y** $\det J > 0$ (no refleja). Tenés `np`. Se verifica
        con `np.allclose` sobre una lista de ocho matrices: similaridades, una reflexión, una afinidad, un corte y la nula.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _casos = [
        ("rotación de 37°", lib.rot2(np.deg2rad(37.0)), True),
        ("[[3, −4], [4, 3]]", np.array([[3.0, -4.0], [4.0, 3.0]]), True),
        ("homotecia 0.5 I", 0.5 * np.eye(2), True),
        ("reflexión diag(1, −1)", np.diag([1.0, -1.0]), False),
        ("reflexión [[3, 4], [4, −3]]", np.array([[3.0, 4.0], [4.0, -3.0]]), False),
        ("afinidad diag(2, 1)", np.diag([2.0, 1.0]), False),
        ("corte [[1, 0.5], [0, 1]]", np.array([[1.0, 0.5], [0.0, 1.0]]), False),
        ("matriz nula", np.zeros((2, 2)), False),
    ]
    _esperado = np.array([e for _, _, e in _casos])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.array([bool(_ns["es_jacobiano_conforme"](J)) for _, J, _ in _casos])
        if np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en las ocho matrices: conformes sólo las tres similaridades directas."), kind="success")
        elif np.allclose(_obtenido[:5], [True, True, True, True, True]) and np.allclose(_obtenido[5:], _esperado[5:]):
            _res = mo.callout(mo.md(r"❌ aceptás las reflexiones: $J^T J = k^2 I$ también vale para los espejos; falta pedir $\det J > 0$ (una reflexión conserva el tamaño de los ángulos pero invierte su sentido)."), kind="warn")
        elif bool(_obtenido[-1]):
            _res = mo.callout(mo.md(r"❌ la matriz nula no es conforme: $J^T J = 0 \cdot I$ pasa el test de ángulos con $k = 0$, pero $\det J = 0$, no $> 0$."), kind="warn")
        else:
            _fallas = [n for (n, _, _), o, e in zip(_casos, _obtenido, _esperado) if o != e]
            _res = mo.callout(mo.md(f"❌ no coincide. Se esperaba `{_esperado.tolist()}` y se obtuvo `{_obtenido.tolist()}`; fallan: {', '.join(_fallas)}."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def latitud_isometrica_elipsoide(phi_deg, e):\n    # phi en GRADOS; devuelve q(phi) (adimensional)\n    phi = ...                       # a radianes\n    esfera = ...                    # ln tan(pi/4 + phi/2)\n    correccion = ...                # (e/2) ln((1 + e sin)/(1 - e sin))\n    return esfera - correccion\n",
        language="python", min_height=160, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("Mercator sobre el elipsoide").* Completá `latitud_isometrica_elipsoide(phi_deg, e)`
        con $q(\varphi) = \ln\tan\!\left(\frac{\pi}{4} + \frac{\varphi}{2}\right) - \frac{e}{2}\ln\frac{1 + e\sin\varphi}{1 - e\sin\varphi}$,
        grados adentro, vectorizada (acepta un array de latitudes). Tenés `np`. Se verifica con `np.allclose` contra
        `lib.latitud_isometrica` en 20 latitudes al azar entre $-80°$ y $80°$, con $e$ de GRS80 y con $e = 0$.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, grs80, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _phis = _rng.uniform(-80, 80, 20)
    _e = np.sqrt(grs80["e2"])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _f = _ns["latitud_isometrica_elipsoide"]
        _ob = np.asarray(_f(_phis, _e), dtype=float)
        _ob0 = np.asarray(_f(_phis, 0.0), dtype=float)
        _esp = lib.latitud_isometrica(np.deg2rad(_phis), _e)
        _esp0 = lib.latitud_isometrica(np.deg2rad(_phis), 0.0)
        if _ob.shape != _esp.shape:
            _res = mo.callout(mo.md(f"❌ la forma del resultado es `{_ob.shape}`; tiene que ser `{_esp.shape}` (una $q$ por latitud: usá `np.tan`, `np.log`, no `math`)."), kind="danger")
        elif np.allclose(_ob, _esp, atol=1e-9) and np.allclose(_ob0, _esp0, atol=1e-9):
            _res = mo.callout(mo.md(r"✅ coincide con `lib.latitud_isometrica` en las 20 latitudes, con $e$ de GRS80 y en la esfera."), kind="success")
        elif np.allclose(_ob, _esp0, atol=1e-9):
            _res = mo.callout(mo.md(r"❌ devolvés la $q$ de la esfera: falta restar la corrección $\frac{e}{2}\ln\frac{1 + e\sin\varphi}{1 - e\sin\varphi}$ (en $-54°$ vale $0.0054$, unos $35$ km en Mercator)."), kind="warn")
        elif np.allclose(_ob, lib.latitud_isometrica(np.deg2rad(_phis), _e**2), atol=1e-9):
            _res = mo.callout(mo.md(r"❌ usaste $e^2$ donde va $e$: la fórmula lleva la excentricidad $e = \sqrt{e^2} = 0.0818$, no $e^2 = 0.0067$."), kind="warn")
        elif np.allclose(_ob, 2 * _esp0 - _esp, atol=1e-9):
            _res = mo.callout(mo.md(r"❌ el signo de la corrección: es **menos** $\frac{e}{2}\ln(\cdots)$; el elipsoide achica $\lvert q \rvert$ respecto de la esfera."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para $\\varphi = {_phis[0]:.4f}°$ se esperaba `{_esp[0]:.6f}` y se obtuvo `{_ob[0]:.6f}` (¿pasaste los grados a radianes con `np.deg2rad`?)."), kind="danger")
    except Exception as _e_:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e_).__name__}: {_e_}`. Completá los `...`."), kind="neutral")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "15_transformaciones_conformes")
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

    Acá verificamos que las cuatro caras de "conforme" dan lo mismo y que Mercator, con la latitud isométrica, deja las
    visuales a $90°$. Las demostraciones:

    - [apunte, sección "Transformaciones conformes"](../../apunte.pdf#nameddest=sec:transformaciones-conformes):
      similaridad infinitesimal $\iff$ $\sigma_1 = \sigma_2$ $\iff$ $F = 0$, $E = G$ $\iff$ Cauchy-Riemann; la indicatriz de
      Tissot y $\omega_{\max}$; la deducción de la latitud isométrica $q(\varphi)$ y de las tres cilíndricas; el planteo de
      Gauss-Krüger como $w = f(q + i\,\Delta\lambda)$
    - [apunte, sección "Geometría del elipsoide"](../../apunte.pdf#nameddest=sec:elipsoide): $M$, $N$, la primera forma
      $ds^2 = M^2\,d\varphi^2 + N^2\cos^2\varphi\,d\lambda^2$ y el arco de meridiano $S(\varphi)$ que usan las tres proyecciones
    - [apunte, «Coordenadas curvilíneas y bases locales» (esfera, elipsoide y curvatura)](../../apunte.pdf#nameddest=cap:13) ($K = 1/(MN)$, lo que
      impide la isometría) · [apunte, «Pasar del plano a una superficie» (esfera, elipsoide y representación plana)](../../apunte.pdf#nameddest=cap:06)
    - apunte del profesor *Geometría del Elipsoide y cálculos Geodésicos* (campus, clase 12), última página: las cinco
      preguntas (Mercator, equidistante, equivalente, esfera autálica, Mercator transversa) que esta unidad responde
    - [ficha de la clase 13](../../clases/13.html) · [ficha de la clase 14](../../clases/14.html) ·
      [el hilo conductor](../../index.html) · [unidad anterior: trigonometría esférica](../14_trigonometria_esferica/index.html)

    **Lo que viene:** nada; es la última unidad. El arco se cierra donde empezó: en la clase 1 un número complejo giraba
    un punto sin moverlo; acá el mismo número complejo, $f'(z)$, es la lupa con la que una proyección conforme mira el
    elipsoide. Lo que sigue es de Topografía y Geodesia: las fajas Gauss-Krüger de POSGAR, la reducción de distancias y
    la convergencia de meridianos, que son los números de esta unidad aplicados en el campo.
    """)
    return


@app.cell
def _(J, J_sit, ang_despues, ang_sit, d1, d2, d_ne, d_se, grs80, h_v, k_v, lib, mo, np, ok_31, ok_32, ok_33, omega_sit, omega_v, phi_sit, razon_sit, tipo):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _M, _N = lib.radios_curvatura(phi_sit, grs80["a"], grs80["e2"])
    _ang_hoja = np.rad2deg(lib.angulo(J_sit @ d_ne, J_sit @ d_se))
    _checks = [
        ("sección 0: en −54° el paralelo mide 0.589 M y las visuales a 45°/135° pasan de 90° a ≈ 61°; torcedura ≈ 29°, apenas menor que ω_max ≈ 30°",
         lib.exacto(razon_sit, 0.5892, tol=1e-4) and lib.exacto(_ang_hoja, ang_sit) and 60.5 < ang_sit < 61.5
         and omega_sit - 1.5 < 90 - ang_sit < omega_sit and 29.5 < omega_sit < 30.5),
        ("sección 1: q es impar, q(0) = 0 y dq/dφ = M/(N cos φ) en −54°",
         lib.exacto(lib.latitud_isometrica(0.0), 0.0) and lib.exacto(lib.latitud_isometrica(phi_sit), -lib.latitud_isometrica(-phi_sit))
         and lib.exacto((lib.latitud_isometrica(phi_sit + 1e-6) - lib.latitud_isometrica(phi_sit - 1e-6)) / 2e-6, _M / (_N * np.cos(phi_sit)), tol=1e-6)),
        ("sección 2: Mercator h = k y ω = 0; equidistante h = 1; equivalente hk = 1 (en la latitud elegida)",
         {"conforme_mercator": lib.exacto(h_v, k_v) and omega_v == 0.0, "equidistante": h_v == 1.0,
          "equivalente": lib.exacto(h_v * k_v, 1.0), "complejo": True}[tipo]),
        ("sección 2: el ángulo después de J coincide con la cuenta directa; es 90° si y sólo si ω = 0 o las visuales van por las direcciones principales (autovectores de JᵀJ)",
         lib.exacto(ang_despues, np.rad2deg(lib.angulo(J @ d1, J @ d2)))
         and (lib.exacto(ang_despues, 90.0, tol=1e-6) == (omega_v < 1e-9 or abs(lib.cuna2(J.T @ J @ d1, d1)) < 1e-9 * np.linalg.norm(J.T @ J)))),
        ("sección 3.1: [[3, −4], [4, 3]] tiene JᵀJ = 25 I, σ = 5, ω = 0", ok_31),
        ("sección 3.2: q(−54°) = −1.11875 y h = k = 1.69757 en Mercator GRS80", ok_32),
        ("sección 3.3: dS/dq = N cos φ en −34.6°", ok_33),
        ("ecuador: las tres cilíndricas dan h = k = 1",
         all(lib.exacto(lib.escalas_proyeccion_cilindrica(0.0, t, grs80)[1:3], [1.0, 1.0]) for t in ("conforme_mercator", "equidistante", "equivalente"))),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
