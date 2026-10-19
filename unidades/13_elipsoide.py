# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Geometría del elipsoide (unidad 13, molde v2 sobre cb104). Clase 13 del esqueleto 2025, no dictada en 2C2026.

Lección anticipada (esqueleto 2025 "deducciones a partir de la simetría" + apunte del profesor sobre el elipsoide +
apunte v3), pendiente de validar por la cátedra. Una sola idea: el elipsoide de revolución es una elipse girada
alrededor de su eje menor, y de eso solo sale casi todo: la normal no pasa por el centro (tres latitudes), M ≠ N,
(φ, λ, h) → (X, Y, Z) con N, y la primera forma E = M², F = 0, G = N² cos²φ.

Chequear:  uv run marimo check --select MW unidades/13_elipsoide.py
Exportar:  uv run python tools/build.py --only 13_elipsoide
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
    # Geometría del elipsoide

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    *Lección anticipada: la clase no se dictó todavía; lo que sigue desarrolla el esqueleto 2025 y el apunte de la cátedra,
    pendiente de validar por la cátedra.*

    Seguimos la clase 13 del esqueleto. La pregunta: **¿Qué se deduce del elipsoide con sólo saber que todos sus
    meridianos son la misma elipse?** El gancho: *la latitud geodésica y la geocéntrica no coinciden porque la normal
    al elipsoide no pasa por el centro; eso cambia las coordenadas de todo mojón.*

    Colores, iguales en la figura y en el álgebra: el elipsoide y su grilla $(\varphi, \lambda)$ en **gris**; el
    **meridiano** del punto en <span style="color:#1b6f6a">**teal**</span> y su **paralelo** en
    <span style="color:#c9a227">**gold**</span>; la **normal** (la vertical elipsoidal) en
    <span style="color:#b5451b">**rust**</span>; la recta al centro en gris; el mojón en
    <span style="color:#7a4e9e">**violeta**</span>. Seguimos la notación del apunte del profesor (*Geometría del
    Elipsoide y cálculos Geodésicos*): $a, b, f, e^2, e'^2$, $M$, $N$, $x'$ el radio del paralelo.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("13_elipsoide"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    grs80 = lib.elipsoide_grs80()
    phi_sit = np.deg2rad(45.0)
    psi_sit, beta_sit = lib.latitudes(phi_sit, grs80["e2"])
    dif_sit = 45.0 - np.rad2deg(psi_sit)
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({
            "45°, el mismo ángulo: la normal pasa por el centro": "misma",
            f"{lib.gms(np.rad2deg(psi_sit))}, unos {dif_sit * 60:.0f}′ menos": "correcta",
            f"{lib.gms(45.0 + dif_sit)}, unos {dif_sit * 60:.0f}′ más": "mas",
            "no se puede saber sin conocer la altura h del mojón": "altura",
        }),
        value=None,
        label="**Predicción.** La recta del mojón al centro de la Tierra forma con el plano del ecuador un ángulo de…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Un mojón sobre el elipsoide GRS80 ($h = 0$). El receptor GNSS dice latitud $\varphi = 45°$: es la **latitud
        geodésica**, el ángulo entre la **normal** al elipsoide en el mojón (la vertical elipsoidal, la plomada
        idealizada) y el plano del ecuador. El elipsoide está achatado: $a = 6378137$ m, $f = 1/298.257$.
        """),
        prediccion,
    ])
    return beta_sit, dif_sit, grs80, phi_sit, prediccion, psi_sit


@app.cell
def _(dif_sit, lib, mo, np, prediccion, psi_sit):
    _psi = lib.gms(np.rad2deg(psi_sit))
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** Es la **latitud geocéntrica** $\psi$: $\tan\psi = (1 - e^2)\tan\varphi$; con $\varphi = 45°$, "
                     rf"$\psi = \arctan(1 - e^2) = {_psi}$, {dif_sit * 60:.1f}′ menos. La normal es más empinada que el radio: corta "
                     r"el eje polar **debajo** del centro. Abajo lo mostramos en la elipse meridiana."),
        "misma": ("warn",
                  r"**No.** Vale en la esfera, donde toda normal es un radio. En la elipse la normal es perpendicular a la tangente, "
                  r"y la tangente no es perpendicular al radio salvo en los vértices: la normal en $45°$ corta el eje polar a "
                  rf"$N e^2 \sin\varphi \approx 30$ km del centro. Diferencia: $45° - {_psi} = {dif_sit * 60:.1f}′$."),
        "mas": ("warn",
                r"**No.** El signo: $\tan\psi = (1 - e^2)\tan\varphi < \tan\varphi$, la geocéntrica es **menor** en módulo: el achatamiento "
                r"acuesta la recta al centro respecto de la normal."),
        "altura": ("warn",
                   r"**No** con $h = 0$: sobre el elipsoide $\psi$ sale sólo de $\varphi$ y $e^2$. Con $h \ne 0$ sí cambia (el punto sube "
                   r"por la normal, no por el radio), pero el mojón está en la superficie."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** Al girar el elipsoide alrededor del eje polar cae sobre sí mismo; al reflejarlo en un
    plano meridiano, también. Eso es "todos los meridianos son la misma elipse y los paralelos son círculos", y de
    ahí deducimos (nuestra lectura del título del esqueleto):

    1. nada métrico depende de $\lambda$: $M$, $N$, $K$ y la primera forma son funciones de $\varphi$ sola;
    2. el plano meridiano es plano de simetría: la forma cuadrática de la curvatura (unidad 12) es simétrica
       respecto del rumbo del meridiano y sus extremos están a $90°$, así que las direcciones principales **tienen
       que ser** el meridiano y el **primer vertical** (la sección normal perpendicular), sin calcular nada;
    3. en los polos pasan todos los meridianos: todos los rumbos son iguales y $M = N$ (punto umbilical);
    4. en el ecuador y los polos la normal cae sobre un eje de simetría de la elipse, que pasa por el centro: ahí
       las tres latitudes coinciden; en cualquier otro punto, no.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R^2$ | elipse meridiana $x'^2/a^2 + z^2/b^2 = 1$, $b = a(1 - f)$, $e^2 = (a^2 - b^2)/a^2 = 2f - f^2$; normal $\propto (x'/a^2,\ z/b^2)$ | una circunferencia estirada: $x' = a\cos\beta$, $z = b\sin\beta$; la normal no pasa por el centro salvo en los vértices |
    | $\mathbb R^3$ | $r(\varphi, \lambda) = \big(N\cos\varphi\cos\lambda,\ N\cos\varphi\sin\lambda,\ N(1 - e^2)\sin\varphi\big)$ | meridianos: la misma elipse girada; paralelos: círculos de radio $x' = N\cos\varphi$ |

    **Tres latitudes** del mismo punto: la **geodésica** $\varphi$ (ángulo de la normal con el ecuador, la que da el
    GNSS), la **geocéntrica** $\psi$ (ángulo del radio) y la **reducida** $\beta$ (ángulo del punto de la
    circunferencia auxiliar de radio $a$ con la misma $x'$):

    $$\tan\psi = (1 - e^2)\tan\varphi, \qquad \tan\beta = \sqrt{1 - e^2}\,\tan\varphi, \qquad |\psi| \le |\beta| \le |\varphi|.$$

    **Dos radios de curvatura** (apunte v3, «Coordenadas curvilíneas y bases locales»; deducción en el apunte del profesor):

    $$N = \frac{a}{\sqrt{1 - e^2\sin^2\varphi}}\ \text{(primer vertical)}, \qquad
      M = \frac{a(1 - e^2)}{(1 - e^2\sin^2\varphi)^{3/2}}\ \text{(meridiano)}, \qquad K = \frac{1}{MN}.$$

    $N$ es también la distancia del punto al eje polar **a lo largo de la normal** (Meusnier: el paralelo, de radio
    $x' = N\cos\varphi$, es una sección oblicua de la del primer vertical). $M \le N$, iguales sólo en los polos; los dos
    crecen del ecuador al polo. Con $f = 0$, la esfera: $M = N = a$.

    **De $(\varphi, \lambda, h)$ a cartesianas geocéntricas**, con $h$ sobre la normal:
    $X = (N + h)\cos\varphi\cos\lambda$, $Y = (N + h)\cos\varphi\sin\lambda$, $Z = \big(N(1 - e^2) + h\big)\sin\varphi$
    ($X$ hacia el meridiano origen; el apunte del profesor escribe $x = x'\sin\lambda$, $y = x'\cos\lambda$, otra
    convención de ejes). La **primera forma** (unidad 10) sale de $\|r_\varphi\| = M$ y $\|r_\lambda\| = x'$:
    $E = M^2$, $F = 0$, $G = N^2\cos^2\varphi$ (la esfera de la unidad 10 es $M = N = R$). Es una **muestra**; el
    enlace con la unidad 12 es que $1/M$ y $1/N$ son $\kappa_1$ y $\kappa_2$ de la segunda forma.
    """)
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("05_elipsoide_euler_meusnier", "Giramos el plano normal en acimut y el radio del círculo osculador pasa de M a N (Euler); después lo inclinamos hasta el paralelo, de radio N·cos φ (Meusnier), y volvemos sobre los mismos pasos."))
    return


@app.cell
def _(mo):
    # ---------- casos precargados: etiqueta → (a, f, unidad, φ inicial, λ inicial, qué pasa) ----------
    casos = {
        "esfera (f = 0)": (1.0, 0.0, "", 45.0, 30.0,
                           r"la normal es un radio: $\varphi = \psi = \beta$ y $M = N = a$ en todo punto; es la grilla de la unidad 10."),
        "elipsoide exagerado (f = 0.3)": (1.0, 0.3, "", 45.0, 30.0,
                                          r"achatado a ojo: la normal corta el eje polar lejos del centro y $\varphi - \psi$ llega a decenas de grados; $M < N$ salvo en los polos."),
        "elipsoide de juguete a = 5, b = 4": (5.0, 0.2, "", 45.0, 30.0,
                                             r"los números de la ficha: ecuador $M = b^2/a = 3.2$, $N = a = 5$; polo $M = N = a^2/b = 6.25$."),
        "GRS80 (f = 1/298.257)": (6378137.0, 1 / 298.257222101, " m", -34.6, -58.4,
                                  r"la Tierra: el achatamiento no se ve ($b$ es $21$ km más corto que $a$), pero $\varphi - \psi$ llega a $11.5′$ y $N - M$ a $42.7$ km."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="elipsoide exagerado (f = 0.3)", label="caso precargado")
    mo.md(r"""
    ## 2. Manipulación

    La figura va en unidades de $a$; los **números vivos** (panel de la derecha) usan el $a$ del caso. En **gris**, el
    elipsoide con su grilla y la recta al centro; en **teal** el meridiano del punto, en **gold** su paralelo; en
    **rust** la normal, desde el eje polar hasta el punto y un poco más: el tramo hasta el eje mide exactamente $N$.
    """)
    return caso, casos


@app.cell
def _(caso, casos, mo):
    _, _, _, _phi0, _lam0, _ = casos[caso.value]
    phi_s = mo.ui.slider(-85, 85, value=_phi0, step=1, label="φ geodésica (°)", show_value=True)
    lam_s = mo.ui.slider(-180, 180, value=_lam0, step=5, label="λ (°)", show_value=True)
    return lam_s, phi_s


@app.cell
def _(caso, casos, go, lam_s, lib, mo, np, phi_s):
    a, f, unidad, _, _, que_pasa = casos[caso.value]
    el = lib.elipsoide(a, f)
    phi, lam = np.deg2rad(phi_s.value), np.deg2rad(lam_s.value)
    M, N = lib.radios_curvatura(phi, a, el["e2"])
    psi, beta = lib.latitudes(phi, el["e2"])
    P = lib.geodesica_a_cartesiana(phi, lam, 0.0, a, el["e2"])
    n = lib.normal_elipsoide(phi, lam)
    r1 = lambda p, l: lib.geodesica_a_cartesiana(p, l, 0.0, 1.0, el["e2"])  # noqa: E731  (en unidades de a)

    figura = lib.figura_espacio((-1.25, 1.25), f"{caso.value} · φ = {phi_s.value}°, λ = {lam_s.value}°")
    lib.superficie_malla(figura, r1, np.deg2rad(np.arange(-90, 91, 15)), np.deg2rad(np.arange(-180, 181, 15)), color=lib.GRIS_ANTES,
                         nombre="elipsoide", ancho=1, opacidad=0.5)
    _m = r1(np.linspace(-np.pi / 2, np.pi / 2, 91), lam)
    figura.add_trace(go.Scatter3d(x=_m[:, 0], y=_m[:, 1], z=_m[:, 2], mode="lines", line=dict(color=lib.COLORES[0], width=6), name="meridiano del punto (la misma elipse)"))
    _q = r1(phi, np.linspace(-np.pi, np.pi, 121))
    figura.add_trace(go.Scatter3d(x=_q[:, 0], y=_q[:, 1], z=_q[:, 2], mode="lines", line=dict(color=lib.COLORES[2], width=6), name=f"paralelo, radio x′ = N cos φ = {N * np.cos(phi) / a:.3f} a"))
    _p1 = P / a
    lib.flecha_3d(figura, _p1 - (N / a) * n, _p1 + 0.35 * n, lib.COLORES[1], f"normal: del eje polar al punto mide N = {N / a:.3f} a", ancho=7)
    figura.add_trace(go.Scatter3d(x=[0, _p1[0]], y=[0, _p1[1]], z=[0, _p1[2]], mode="lines", line=dict(color="#555", width=4, dash="dash"), name="recta al centro (geocéntrica)"))
    figura.add_trace(go.Scatter3d(x=[_p1[0]], y=[_p1[1]], z=[_p1[2]], mode="markers", marker=dict(size=6, color=lib.VIOLETA_OBJETO), name="mojón"))
    _fmt = (lambda v: f"{v:,.2f}{unidad}") if a > 100 else (lambda v: f"{v:.4f}")
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, phi_s, lam_s,
        mo.md(rf"""
        **Números vivos** ($a = {a:g}$, $f = {f:.6g}$, $e^2 = {el['e2']:.6g}$)

        - latitudes: geodésica $\varphi = {lib.gms(phi_s.value)}$, geocéntrica $\psi = {lib.gms(np.rad2deg(psi), 1)}$, reducida $\beta = {lib.gms(np.rad2deg(beta), 1)}$; ángulo normal–radio $\varphi - \psi = {lib.gms(phi_s.value - np.rad2deg(psi), 1)}$
        - radios: $M = {_fmt(M)}$ (meridiano), $N = {_fmt(N)}$ (primer vertical), $N - M = {_fmt(N - M)}$; $K = 1/(MN) = {1 / (M * N):.4g}$
        - cartesianas: $X = {_fmt(P[0])}$, $Y = {_fmt(P[1])}$, $Z = {_fmt(P[2])}$; control $X^2/a^2 + Y^2/a^2 + Z^2/b^2 = {(P[0]**2 + P[1]**2) / a**2 + P[2]**2 / el['b']**2:.6f}$
        - primera forma $E = M^2$, $G = N^2\cos^2\varphi$: $1′$ de $\varphi$ mide ${_fmt(M * np.deg2rad(1 / 60))}$; $1′$ de $\lambda$, ${_fmt(N * np.cos(phi) * np.deg2rad(1 / 60))}$

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, N, P, a, beta, el, f, phi, psi


@app.cell
def _(N, a, beta, el, go, lib, mo, np, phi, psi):
    # ---------- la elipse meridiana (plano x′ z, en unidades de a) con las tres latitudes ----------
    _e2 = el["e2"]
    _b = 1 - el["f"]
    _t = np.linspace(0, 2 * np.pi, 241)
    xp, zp = (N / a) * np.cos(phi), (N / a) * (1 - _e2) * np.sin(phi)  # el punto
    _pie = np.array([(N / a) * _e2 * np.cos(phi), 0.0])  # donde la normal corta al ecuador
    _eje = np.array([0.0, -(N / a) * _e2 * np.sin(phi)])  # donde corta al eje polar
    fig2 = lib.figura_plano((-1.3, 1.3), "elipse meridiana: φ (normal), ψ (radio), β (círculo auxiliar)")
    fig2.add_trace(go.Scatter(x=np.cos(_t), y=np.sin(_t), mode="lines", line=dict(color=lib.GRIS_ANTES, width=1, dash="dash"), name="círculo auxiliar de radio a"))
    fig2.add_trace(go.Scatter(x=np.cos(_t), y=_b * np.sin(_t), mode="lines", line=dict(color=lib.COLORES[0], width=2.5), name="meridiano (elipse a, b)"))
    lib.flecha(fig2, _eje, (xp, zp) + 0.3 * np.array([np.cos(phi), np.sin(phi)]), lib.COLORES[1], "normal (φ con el ecuador)", ancho=4)
    lib.flecha(fig2, (0, 0), (xp, zp), "#555", "radio (ψ)", ancho=3)
    lib.flecha(fig2, (0, 0), (np.cos(beta), np.sin(beta)), lib.COLORES[2], "al punto del círculo auxiliar (β)", ancho=3)
    fig2.add_trace(go.Scatter(x=[xp, np.cos(beta)], y=[zp, np.sin(beta)], mode="lines", line=dict(color=lib.COLORES[2], width=1, dash="dot"), name="misma x′", hoverinfo="skip"))
    lib.arco_angulo(fig2, [1, 0], [np.cos(phi), np.sin(phi)], 0.22, lib.COLORES[1], "", "φ")
    fig2.data[-2].update(x=np.asarray(fig2.data[-2].x) + _pie[0])
    fig2.data[-1].update(x=np.asarray(fig2.data[-1].x) + _pie[0])
    lib.arco_angulo(fig2, [1, 0], [xp, zp], 0.34, "#555", "", "ψ")
    lib.arco_angulo(fig2, [1, 0], [np.cos(beta), np.sin(beta)], 0.46, lib.COLORES[2], "", "β")
    lib.punto(fig2, (xp, zp), nombre="mojón", texto="P")
    lib.mesa_interactiva(mo, mo.ui.plotly(fig2), mo.md(rf"""
    **La misma cosa en el plano del meridiano.** El punto $P = (x', z) = (N\cos\varphi,\ N(1 - e^2)\sin\varphi)$,
    en unidades de $a$. La normal (rust) corta el ecuador en $x' = N e^2\cos\varphi = {_pie[0]:.3f}\,a$ y el eje polar en
    $z = -N e^2\sin\varphi = {_eje[1]:.3f}\,a$: pasa por el centro sólo si $e^2 = 0$ o $\varphi \in \{{0, \pm 90°\}}$. Los tres
    arcos son $\varphi = {lib.gms(np.rad2deg(phi))}$, $\psi = {lib.gms(np.rad2deg(psi), 1)}$ y $\beta = {lib.gms(np.rad2deg(beta), 1)}$.
    Se mueve con los deslizadores de arriba.
    """))
    return


@app.cell
def _(grs80, lib, mo, np):
    _phi, _lam = np.deg2rad(45.0), np.deg2rad(30.0)
    _M, _N = lib.radios_curvatura(_phi, grs80["a"], grs80["e2"])
    _P = lib.geodesica_a_cartesiana(_phi, _lam, 0.0, grs80["a"], grs80["e2"])
    _psi = np.rad2deg(lib.latitudes(_phi, grs80["e2"])[0])
    ok_mano = bool(np.allclose([_N, _M], [6388838.29, 6367381.82], atol=0.01)) and bool(np.allclose(_P, [3912348.47, 2258795.44, 4487348.41], atol=0.01)) and bool(np.isclose(_psi, 44.80758, atol=1e-5))
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy con `np.allclose` contra los números de la izquierda.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 De dónde sale $N$.** La normal a $x'^2/a^2 + z^2/b^2 = 1$ es $\propto (x'/a^2, z/b^2)$ y forma $\varphi$
            con el ecuador: $\tan\varphi = \dfrac{a^2}{b^2}\dfrac{z}{x'}$, o sea $z = (1 - e^2)\,x'\tan\varphi$ (de paso,
            $\tan\psi = z/x' = (1 - e^2)\tan\varphi$). En la elipse:

            $$\frac{x'^2}{a^2}\big(1 + (1 - e^2)\tan^2\varphi\big) = 1 \ \Rightarrow\ x' = \frac{a\cos\varphi}{\sqrt{\cos^2\varphi + (1 - e^2)\sin^2\varphi}} = \frac{a\cos\varphi}{\sqrt{1 - e^2\sin^2\varphi}} = N\cos\varphi.$$

            **3.2 GRS80 en $\varphi = 45°$, $\lambda = 30°$.** $e^2 = 2f - f^2 = 0.00669438$, $\sin^2 45° = 1/2$,
            $w = \sqrt{1 - e^2/2} = 0.99832500$. $N = a/w = 6\,388\,838.29$ m; $M = a(1 - e^2)/w^3 = 6\,335\,439.33/0.99498 = 6\,367\,381.82$ m.
            $X = N\cos 45°\cos 30° = 3\,912\,348.47$, $Y = N\cos 45°\sin 30° = 2\,258\,795.44$, $Z = N(1 - e^2)\sin 45° = 4\,487\,348.41$ m.
            $\tan\psi = 1 - e^2$: $\psi = 44.80758° = 44° 48′ 27″$.
            """),
            mo.vstack([
                mo.md("```python\ng = lib.elipsoide_grs80()   # a, f, b, e2, ep2\nphi, lam = np.deg2rad(45.0), np.deg2rad(30.0)\na, e2 = g[\"a\"], g[\"e2\"]\nM, N = lib.radios_curvatura(phi, a, e2)\nP = lib.geodesica_a_cartesiana(phi, lam, 0.0,\n                               a, e2)\npsi, beta = lib.latitudes(phi, e2)\nnp.allclose([N, M],\n            [6388838.29, 6367381.82], atol=0.01)\nnp.allclose(P, [3912348.47, 2258795.44,\n                4487348.41], atol=0.01)\n```"),
                mo.md(f"`N, M` = `{_N:.2f}, {_M:.2f}` · `P` = `{np.round(_P, 2).tolist()}` · `psi` = `{_psi:.5f}°` = {lib.gms(_psi)}\n\n`allclose` (las tres) = `{ok_mano}` · `e2` = `{grs80['e2']:.8f}` · `b` = `{grs80['b']:.3f}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return (ok_mano,)


@app.cell
def _(grs80, lib, mo, np):
    _phis, _lams = np.meshgrid(np.deg2rad([-34.6, 0.0, 45.0]), np.deg2rad([-58.4, 0.0]), indexing="ij")
    _XYZ = lib.geodesica_a_cartesiana(_phis, _lams, 0.0, grs80["a"], grs80["e2"])
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        **Broadcasting: la misma función para un punto y para una grilla.** `lib.geodesica_a_cartesiana` usa `np.cos`,
        `np.sin` y `np.stack(..., axis=-1)`: con dos escalares devuelve una terna `(3,)`; con dos grillas de `np.meshgrid`,
        `(n, m, 3)`, una terna por nudo y ningún bucle. Así se dibujó el elipsoide de la sección 2. Y `np.deg2rad` siempre
        antes: la trigonometría de numpy trabaja en radianes.
        """),
        mo.md("```python\nphis, lams = np.meshgrid(np.deg2rad([-34.6, 0.0, 45.0]), np.deg2rad([-58.4, 0.0]), indexing=\"ij\")\nXYZ = lib.geodesica_a_cartesiana(phis, lams, 0.0, g[\"a\"], g[\"e2\"])   # (3, 2, 3)\nXYZ[2, 1]                                                            # φ = 45°, λ = 0\n```"),
        mo.md(f"`phis.shape` = `{_phis.shape}` → `XYZ.shape` = `{_XYZ.shape}` · `XYZ[2, 1]` = `{np.round(_XYZ[2, 1], 2).tolist()}` ($Y = 0$ porque $\\lambda = 0$)."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("deducciones a partir de la simetría").* Explicá, sin fórmulas primero y con
        $\tan\psi = (1 - e^2)\tan\varphi$ después, por qué en el ecuador y en los polos coinciden las tres latitudes.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        En los vértices de la elipse la tangente es perpendicular a un eje de simetría (ecuador o eje polar), así que
        la normal **es** ese eje, que pasa por el centro: $\varphi = \psi$; y el punto del círculo auxiliar con la misma
        $x'$ es el mismo vértice, $\beta = \varphi$. Con la fórmula: $\varphi = 0$ da $\psi = 0$; $\varphi \to 90°$ da
        $\tan\psi \to \infty$, $\psi \to 90°$ (igual para $\beta$). En cualquier otro punto $0 < 1 - e^2 < 1$ achica la tangente.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("los radios mayor y menor tienen que ser el de la sección meridiana y el del primer
        vertical").* Calculá $N - M$ en el ecuador en función de $a$ y $e^2$, y su valor en metros para GRS80
        ($a = 6378137$ m, $e^2 = 0.00669438$). ¿Cuánto vale en los polos?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        En $\varphi = 0$: $N = a$ y $M = a(1 - e^2) = b^2/a$, así que $N - M = a e^2 = (a^2 - b^2)/a$. GRS80:
        $6378137 \times 0.00669438 = 42\,698$ m: en el ecuador el elipsoide es más curvo a lo largo del meridiano
        ($M$ chico) que a lo ancho. En los polos $M = N = a^2/b$, diferencia cero. Juguete $a = 5$, $b = 4$: $5 - 3.2 = 1.8$.
        """)}),
    ])
    return


@app.cell
def _(mo, np):
    _rng = np.random.default_rng(56798)
    puntos_cd = np.column_stack([_rng.uniform(-80, 80, 20), _rng.uniform(-180, 180, 20), _rng.uniform(0, 3000, 20)])  # φ°, λ°, h m
    editor_c = mo.ui.code_editor(
        value="def geodesica_a_cartesiana(phi, lam, h):\n    # phi, lam en GRADOS; a y e2 (GRS80) ya están definidos\n    phi, lam = ...                     # a radianes\n    N = ...                            # radio del primer vertical\n    X = ...\n    Y = ...\n    Z = ...                            # ojo con el (1 - e2)\n    return np.array([X, Y, Z])\n",
        language="python", min_height=190, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("las ecuaciones de transformación entre cartesianas y elipsoidales").*
        Completá `geodesica_a_cartesiana(phi, lam, h)` con los ángulos en **grados**. Tenés `np`, `a` y `e2` de GRS80.
        Se verifica con `np.allclose` en 20 puntos al azar con $h$ entre $0$ y $3000$ m.
        """),
        editor_c,
    ])
    return editor_c, puntos_cd


@app.cell
def _(editor_c, grs80, lib, mo, np, puntos_cd):
    _a, _e2 = grs80["a"], grs80["e2"]
    _ph, _la, _h = np.deg2rad(puntos_cd[:, 0]), np.deg2rad(puntos_cd[:, 1]), puntos_cd[:, 2]
    _esperado = lib.geodesica_a_cartesiana(_ph, _la, _h, _a, _e2)
    _N = _a / np.sqrt(1 - _e2 * np.sin(_ph) ** 2)
    _ns = {"np": np, "a": _a, "e2": _e2}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.array([np.asarray(_ns["geodesica_a_cartesiana"](*p), dtype=float).ravel() for p in puntos_cd])
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ devolvés algo de forma `{_obtenido.shape[1:]}` por punto; tiene que ser `(3,)`."), kind="danger")
        elif np.allclose(_obtenido, _esperado, atol=1e-3):
            _res = mo.callout(mo.md("✅ coincide en los 20 puntos, al milímetro."), kind="success")
        elif np.allclose(_obtenido[:, :2], _esperado[:, :2], atol=1e-3) and np.allclose(_obtenido[:, 2], (_N + _h) * np.sin(_ph), atol=1e-3):
            _res = mo.callout(mo.md(r"❌ $X$ e $Y$ están bien pero en $Z$ olvidaste el $(1 - e^2)$: es $Z = (N(1 - e^2) + h)\sin\varphi$, porque la normal corta el eje polar debajo del centro (el error es $N e^2 \sin\varphi$: unos 30 km en $45°$, hasta unos 43 km cerca del polo)."), kind="warn")
        elif np.allclose(_obtenido[:, :2], np.column_stack([(_a + _h) * np.cos(_ph) * np.cos(_la), (_a + _h) * np.cos(_ph) * np.sin(_la)]), atol=1e-3):
            _res = mo.callout(mo.md(r"❌ usaste $a$ donde va $N = a/\sqrt{1 - e^2\sin^2\varphi}$: la distancia del punto al eje polar por la normal cambia con la latitud (hasta 21 km)."), kind="warn")
        elif np.allclose(_obtenido, lib.geodesica_a_cartesiana(puntos_cd[:, 0], puntos_cd[:, 1], _h, _a, _e2), atol=1e-3):
            _res = mo.callout(mo.md(r"❌ pasaste los grados directo a `np.cos` y `np.sin`, que trabajan en radianes: `np.deg2rad` primero."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para el primer punto se esperaba `{np.round(_esperado[0], 2).tolist()}` y se obtuvo `{np.round(_obtenido[0], 2).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def latitud_geocentrica(phi):\n    # phi geodésica en GRADOS → ψ en GRADOS; e2 (GRS80) ya está definido\n    return ...\n",
        language="python", min_height=100, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado** *("la latitud es el ángulo entre la vertical elipsoidal y el plano XY").*
        Completá `latitud_geocentrica(phi)`: $\tan\psi = (1 - e^2)\tan\varphi$, grados adentro y grados afuera. Tenés
        `np` y `e2`. Se verifica con `np.allclose` en los 20 puntos de (c), más el ecuador y los polos.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, grs80, lib, mo, np, puntos_cd):
    _e2 = grs80["e2"]
    _phis = np.concatenate([puntos_cd[:, 0], [0.0, 90.0, -90.0]])
    _esperado = np.rad2deg(lib.latitudes(np.deg2rad(_phis), _e2)[0])
    _ns = {"np": np, "e2": _e2}
    try:
        exec(editor_d.value, _ns)
        _obtenido = np.array([float(_ns["latitud_geocentrica"](p)) for p in _phis])
        if np.allclose(_obtenido, _esperado, atol=1e-6):
            _res = mo.callout(mo.md(r"✅ coincide, también en el ecuador y los polos (ahí $\psi = \varphi$)."), kind="success")
        elif np.allclose(_obtenido, _phis, atol=1e-6):
            _res = mo.callout(mo.md(r"❌ devolvés $\varphi$: sin el factor $(1 - e^2)$ la geocéntrica es la geodésica, y eso sólo vale en la esfera."), kind="warn")
        elif np.allclose(_obtenido, np.rad2deg(lib.latitudes(np.deg2rad(_phis), _e2)[1]), atol=1e-6):
            _res = mo.callout(mo.md(r"❌ eso es la latitud **reducida** $\beta$: usaste $\sqrt{1 - e^2}$ en vez de $(1 - e^2)$."), kind="warn")
        elif np.allclose(_obtenido, np.rad2deg(np.arctan((1 - _e2) * np.tan(_phis))), atol=1e-6, equal_nan=True) or np.allclose(_obtenido, np.arctan((1 - _e2) * np.tan(np.deg2rad(_phis))), atol=1e-6):
            _res = mo.callout(mo.md(r"❌ los grados: `np.tan` y `np.arctan` trabajan en radianes. `np.deg2rad` al entrar y `np.rad2deg` al salir."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para $\\varphi = {_phis[0]:.4f}°$ se esperaba `{_esperado[0]:.6f}` y se obtuvo `{_obtenido[0]:.6f}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "13_elipsoide")
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

    Acá verificamos que de la elipse girada salen las tres latitudes, $M \ne N$, la conversión a cartesianas y la primera
    forma. Las demostraciones:

    - [apunte, sección "Geometría del elipsoide: latitudes, radios y conversión"](../../apunte.pdf#nameddest=cap:elipsoide):
      la elipse meridiana y la latitud, la deducción de $M$ (curvatura de la elipse meridiana) y de $N$ (Meusnier),
      las tres latitudes (geodésica, geocéntrica $\tan\psi = (1 - e^2)\tan\varphi$, reducida), la primera forma
      $ds^2 = M^2\,d\varphi^2 + N^2\cos^2\varphi\,d\lambda^2$ y los valores de control en GRS80
      · [sección "Arco de meridiano"](../../apunte.pdf#nameddest=cap:elipsoide): serie binomial, potencias del seno
      como cosenos de ángulos múltiples, la tabla de coeficientes $A \ldots E$ y el resultado "Longitud del arco de
      meridiano" con sus controles numéricos
    - fe de erratas del apunte del profesor, verificada numéricamente en GRS80: las cajas "Errata confirmada" de esas
      secciones y el cierre [Material y fuentes: fe de erratas y precisiones](../../apunte.pdf#nameddest=cap:22)
    - [apunte, «Superficies, elipsoide, curvatura…» (esfera, elipsoide, curvatura y representación plana)](../../apunte.pdf#nameddest=cap:elipsoide) ($e^2 = 2f - f^2$, $M$, $N$,
      $K = 1/(MN)$)
    - apunte del profesor *Geometría del Elipsoide y cálculos Geodésicos* (campus, clase 12): latitud elipsoidal,
      conversión $\varphi, \lambda \to X, Y, Z$, radios $M$ (meridiano) y $N$ (primer vertical, Meusnier), arco de meridiano
    - [ficha de la clase 13](../../clases/13.html) · [el hilo conductor](../../index.html) · [unidad 12](../12_curvatura/index.html)

    **Lo que viene:** [Trigonometría esférica](../14_trigonometria_esferica/index.html) (clase 14): triángulos de lados
    geodésicos sobre la esfera, cuyos ángulos suman más de $180°$; y "Máxima para el elipsoide", donde ya no hay fórmula cerrada.
    """)
    return


@app.cell
def _(M, N, P, a, beta_sit, dif_sit, el, f, grs80, lib, mo, np, ok_mano, phi, phi_sit, psi, psi_sit):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _ff = lib.formas_fundamentales(lambda p, l: lib.geodesica_a_cartesiana(p, l, 0.0, a, el["e2"]), phi, 0.3)
    _k = lib.curvaturas_principales(*(_ff[k] for k in "EFGLMN"))[:2]
    _checks = [
        ("sección 0: φ = 45° → ψ = 44° 48′ 27″, unos 11.5′ menos, y ψ < β < φ",
         lib.exacto(np.rad2deg(psi_sit), 44.807576783, tol=1e-8) and lib.exacto(dif_sit * 60, 11.5454, tol=1e-3) and psi_sit < beta_sit < phi_sit),
        ("sección 1: ecuador y polos, las tres latitudes coinciden",
         lib.exacto(lib.latitudes(0.0, grs80["e2"]), [0, 0]) and lib.exacto(lib.latitudes(np.pi / 2, grs80["e2"]), [np.pi / 2] * 2)),
        ("sección 2: el mojón está sobre el elipsoide, tan ψ = (1 − e²) tan φ, M ≤ N",
         lib.exacto((P[0] ** 2 + P[1] ** 2) / a**2 + P[2] ** 2 / el["b"] ** 2, 1.0, tol=1e-9) and lib.exacto(np.tan(psi), (1 - el["e2"]) * np.tan(phi), tol=1e-9) and M <= N + 1e-9),
        ("sección 2: primera forma E = M², F = 0, G = N² cos²φ y curvaturas principales 1/M, 1/N (unidad 12)",
         bool(np.allclose([_ff["E"], _ff["F"], _ff["G"]], [M**2, 0.0, N**2 * np.cos(phi) ** 2], rtol=1e-5, atol=1e-6 * a**2))
         and bool(np.allclose(_k, [1 / M, 1 / N], rtol=1e-4))),
        ("sección 3: GRS80 en 45°: N = 6388838.29, M = 6367381.82, X, Y, Z y ψ a mano = código", ok_mano),
        ("ejercicio (b): N − M en el ecuador = a e² = 42697.67 m",
         lib.exacto(np.subtract(*lib.radios_curvatura(0.0, grs80["a"], grs80["e2"])[::-1]), grs80["a"] * grs80["e2"], tol=1e-6) and lib.exacto(grs80["a"] * grs80["e2"], 42697.67, tol=0.01)),
        ("esfera: f = 0 da M = N = a", f > 0 or lib.exacto([M, N], [a, a], tol=1e-9)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
