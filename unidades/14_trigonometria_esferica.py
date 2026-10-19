# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Trigonometría esférica (unidad 14, molde v2 sobre cb104).
Una sola idea: un triángulo sobre la esfera tiene lados que son ángulos (arcos de círculo máximo
medidos desde el centro) y sus ángulos suman más de 180°; el exceso es el área (Girard), y las leyes del coseno y del
seno salen de productos internos y cuñas de los tres vectores unitarios de los vértices (unidades 02 y 07a).

Chequear:  uv run marimo check --select MW unidades/14_trigonometria_esferica.py
Exportar:  uv run python tools/build.py --only 14_trigonometria_esferica
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
    # Trigonometría esférica

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · Gustavo Varela

    La pregunta: **¿Cómo se relacionan lados y ángulos de un triángulo trazado sobre la esfera, y por
    qué sus ángulos suman más de 180°?** El gancho: *entre tres vértices lejanos la suma de ángulos de la poligonal trae
    un exceso esférico; corregirlo es parte del cálculo.*

    Colores: los tres vértices como vectores desde el centro, $A$ en <span style="color:#1b6f6a">**teal**</span>, $B$ en
    <span style="color:#b5451b">**rust**</span>, $C$ en <span style="color:#c9a227">**gold**</span>; los lados (arcos de
    círculo máximo) en teal grueso; la esfera en gris. Grados en los controles y en los números, radianes adentro.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("14_trigonometria_esferica"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    R_TIERRA = 6371.0
    ciudades = {"Buenos Aires": (-34.6037, -58.3816), "Mendoza": (-32.8895, -68.8458), "Ushuaia": (-54.8019, -68.3030)}
    V_ciudades = [lib.punto_esfera(np.deg2rad(f), np.deg2rad(l)) for f, l in ciudades.values()]
    lados_c, angulos_c = lib.triangulo_esferico(*V_ciudades)
    exceso_c = lib.exceso_esferico(*V_ciudades)
    suma_c = np.degrees(sum(angulos_c))
    candidatos = {"plano": 180.0, "correcta": suma_c, "defecto": 360.0 - suma_c, "octante": 270.0}
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({f"{candidatos[k]:.2f}°": k for k in ("defecto", "plano", "correcta", "octante")}),
        value=None,
        label="**Predicción.** Los tres ángulos del triángulo Buenos Aires – Mendoza – Ushuaia suman…",
    )
    mo.vstack([
        mo.md(rf"""
        ## 0. Situación de campo y predicción

        Una red de tres vértices que no caben en ningún plano: Buenos Aires, Mendoza y Ushuaia, con lados de
        ${R_TIERRA * lados_c[2]:.0f}$, ${R_TIERRA * lados_c[0]:.0f}$ y ${R_TIERRA * lados_c[1]:.0f}$ km (por el camino más corto sobre la
        Tierra, que tomamos como esfera de radio $6371$ km). En cada vértice medimos el ángulo entre las dos líneas más
        cortas que salen hacia los otros dos. En el plano, los tres ángulos suman $180°$ y con eso cerramos la poligonal.
        """),
        prediccion,
    ])
    return R_TIERRA, V_ciudades, angulos_c, candidatos, ciudades, exceso_c, lados_c, prediccion, suma_c


@app.cell
def _(R_TIERRA, exceso_c, mo, np, prediccion, suma_c):
    _area = exceso_c * R_TIERRA**2
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** Suman ${suma_c:.2f}°$: sobran ${np.degrees(exceso_c):.2f}°$, y ese sobrante no es error de medición, es el "
                     rf"**exceso esférico**, igual al área del triángulo dividida por $R^2$: ${_area:,.0f}$ km² $/ 6371^2 = {exceso_c:.4f}$ rad. "
                     rf"La sección 1 muestra de dónde sale."),
        "plano": ("warn",
                  rf"**No.** $180°$ es la suma en el plano. Sobre la esfera el triángulo 'abomba' y los ángulos se abren: suman "
                  rf"${suma_c:.2f}°$. Con lados de pocos km la diferencia es invisible; con miles de km, no: acá son ${np.degrees(exceso_c):.2f}°$ de más."),
        "defecto": ("warn",
                    rf"**No.** Restaste: pensaste que la curvatura 'cierra' los ángulos. En una silla de montar (curvatura negativa) "
                    rf"sí hay defecto; en la esfera la curvatura es positiva y hay **exceso**: ${suma_c:.2f}°$."),
        "octante": ("warn",
                    rf"**No.** $270°$ es la suma del **octante**, el triángulo de tres ángulos rectos que cubre un octavo de la esfera. El de "
                    rf"las tres ciudades cubre el ${100 * exceso_c / (4 * np.pi):.3f}\,\%$ de la esfera, y el exceso es proporcional al área: "
                    rf"${np.degrees(exceso_c):.2f}°$, no $90°$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Un triángulo esférico son tres planos por el centro.** Los vértices son tres vectores unitarios $A, B, C$ desde el
    centro de la esfera. Cada lado es un arco de **círculo máximo** (el corte de la esfera con el plano por el centro y
    los dos vértices: el camino más corto sobre la esfera, su geodésica), y se mide por el **ángulo central**: el lado
    $a$, opuesto a $A$, es el ángulo entre $B$ y $C$. Nada mide en metros: sobre la esfera de radio $R$ el arco mide
    $R\,a$. Cada **ángulo** es el que forman dos planos (el diedro), o sea el ángulo entre sus normales.

    Con eso, las dos herramientas de las unidades 02 y 07a alcanzan:

    - **lado = producto interno**: $\cos a = \langle B, C\rangle$;
    - **ángulo = ángulo entre normales**: las normales de los planos $OAB$ y $OAC$ son $A \times B$ y $A \times C$, y
      $\langle A\times B, A\times C\rangle = \langle B, C\rangle - \langle A, C\rangle\langle A, B\rangle = \cos a - \cos b\cos c$,
      con $|A\times B| = \sin c$, $|A\times C| = \sin b$. Dividiendo:

    $$\cos a = \cos b\,\cos c + \sin b\,\sin c\,\cos A \qquad\text{(ley del coseno esférica)};$$

    - **la cuña da la ley del seno**: el volumen orientado $[A, B, C] = (A\wedge B)\wedge C$ (07a) vale
      $\sin b\,\sin c\,\sin A$ mirado desde $A$, y lo mismo desde $B$ o $C$; igualando,
      $\dfrac{\sin A}{\sin a} = \dfrac{\sin B}{\sin b} = \dfrac{\sin C}{\sin c}$.

    **Los ángulos suman más de $180°$, y el sobrante es el área** (Girard): $A + B + C - \pi = \text{área}/R^2$. Se
    **muestra** así: los tres círculos máximos cortan la esfera en seis husos; el huso de ángulo $A$ tiene área
    $2A R^2$ (es la fracción $A/2\pi$ de $4\pi R^2$). Cada vértice da **dos** husos opuestos de ángulo $A$ (uno contiene
    al triángulo, el otro a su antípoda), así que los seis husos suman $2(2A + 2B + 2C)R^2 = 4(A + B + C)R^2$. Esos seis
    husos cubren la esfera entera: cada punto fuera del triángulo y de su antípoda cae en exactamente uno, mientras que el
    triángulo cae en los tres husos de sus vértices y la antípoda en los tres opuestos. Contamos así la esfera una vez y
    el triángulo y su antípoda dos veces de más cada uno: $4(A + B + C)R^2 = 4\pi R^2 + 4\,\text{área}$, que es
    $A + B + C - \pi = \text{área}/R^2$. Control con el octante: $4 \cdot \tfrac{3\pi}{2} = 4\pi + 4\cdot\tfrac{\pi}{2}$.
    En el apunte, la sección [Polígonos geodésicos y trigonometría esférica](../../apunte.pdf#nameddest=cap:esfera)
    deduce los teoremas del coseno y del seno con producto interno y determinante, enuncia el exceso de Girard con el
    control del octante y resuelve el triángulo entre tres ciudades; la demostración completa del exceso por husos está
    en Coxeter, *Geometría*, de la bibliografía.

    | | la cuenta | lo que se ve |
    |---|---|---|
    | plano | $a^2 = b^2 + c^2 - 2bc\cos A$; $A + B + C = 180°$ | lados en metros, suma fija |
    | esfera | $\cos a = \cos b\cos c + \sin b\sin c\cos A$; $A + B + C = 180° + \text{área}/R^2$ | lados que son ángulos; el exceso crece con el área |
    | elipsoide | sin fórmula cerrada: los lados son geodésicas que no son círculos | problemas directo e inverso por series o con Maxima (unidad 14) |

    **¿Qué se conserva?** Al rotar la esfera (unidad 01c) no cambian ni lados, ni ángulos, ni área: el producto interno
    y la cuña son invariantes por rotaciones. Y para lados chicos ($\sin b \approx b$, $\cos b \approx 1 - b^2/2$) la ley
    del coseno esférica se vuelve la plana: una Tierra lo bastante chica es plana.
    """)
    return


@app.cell
def _(ciudades, mo):
    casos = {
        "octante: tres ángulos rectos": [(90.0, 0.0), (0.0, 0.0), (0.0, 90.0)],
        "triángulo chico: lados de 1°, casi plano": [(0.0, 0.0), (0.0, 1.0), (1.0, 0.0)],
        "tres ciudades argentinas": list(ciudades.values()),
        "a mano: A y B fijos, C con los deslizadores": [(0.0, 0.0), (0.0, 60.0), None],
    }
    caso = mo.ui.dropdown(options=list(casos), value="a mano: A y B fijos, C con los deslizadores", label="caso precargado")
    mo.md(r"""
    ## 2. Manipulación

    **Gris**: la esfera unitaria. **Teal, rust, gold**: los vectores $A$, $B$, $C$ desde el centro, con sus
    latitudes y longitudes. **Teal grueso**: los tres lados, arcos de círculo máximo. Arranca **a mano**: mové el
    vértice $C$ con los deslizadores y mirá cómo cambian lados y ángulos, y cómo el exceso sigue al área; los otros
    casos (selector del panel) fijan los tres vértices. Arrastrá la figura para girarla.
    """)
    return caso, casos


@app.cell
def _(caso, casos, mo):
    a_mano = casos[caso.value][2] is None
    phi_c = mo.ui.slider(-85, 85, value=45, step=1, label="latitud de C (°)", show_value=True, disabled=not a_mano)
    lam_c = mo.ui.slider(-170, 170, value=30, step=1, label="longitud de C (°)", show_value=True, disabled=not a_mano)
    return a_mano, lam_c, phi_c


@app.cell
def _(R_TIERRA, a_mano, caso, casos, go, lam_c, lib, mo, np, phi_c):
    _vert = list(casos[caso.value])
    if a_mano:
        _vert[2] = (float(phi_c.value), float(lam_c.value))
    V = [lib.punto_esfera(np.deg2rad(f), np.deg2rad(l)) for f, l in _vert]
    lados, angulos = lib.triangulo_esferico(*V)
    exceso = lib.exceso_esferico(*V)

    figura = lib.figura_espacio(1.25, caso.value.split(":")[0])
    lib.esfera_malla(figura)
    for (_p, _q), _n in zip(((V[1], V[2]), (V[0], V[2]), (V[0], V[1])), "abc"):
        _arc = lib.arco_maximo(_p, _q)
        figura.add_trace(go.Scatter3d(x=_arc[:, 0], y=_arc[:, 1], z=_arc[:, 2], mode="lines", line=dict(color=lib.TEAL_DESPUES, width=7), name=f"lado {_n}"))
    for _k, (_v, _fl) in enumerate(zip(V, _vert)):
        _c = lib.color_columna(_k)
        figura.add_trace(go.Scatter3d(x=[0, _v[0]], y=[0, _v[1]], z=[0, _v[2]], mode="lines+markers+text", text=["", "ABC"[_k]],
                                      textfont=dict(size=15, color=_c), line=dict(color=_c, width=6), marker=dict(size=[0, 7], color=_c),
                                      name=f"{'ABC'[_k]} = (φ {_fl[0]:.1f}°, λ {_fl[1]:.1f}°)"))
    _cos_ley = np.cos(lados[1]) * np.cos(lados[2]) + np.sin(lados[1]) * np.sin(lados[2]) * np.cos(angulos[0])
    _seno = [np.sin(an) / np.sin(la) for an, la in zip(angulos, lados)]
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, phi_c, lam_c,
        mo.md(rf"""
        **Números vivos**

        - lados $a, b, c = ({np.degrees(lados[0]):.3f}°,\ {np.degrees(lados[1]):.3f}°,\ {np.degrees(lados[2]):.3f}°)$; sobre la Tierra
          $({R_TIERRA * lados[0]:.0f},\ {R_TIERRA * lados[1]:.0f},\ {R_TIERRA * lados[2]:.0f})$ km
        - ángulos $A, B, C = ({np.degrees(angulos[0]):.3f}°,\ {np.degrees(angulos[1]):.3f}°,\ {np.degrees(angulos[2]):.3f}°)$
        - suma $= \mathbf{{{np.degrees(sum(angulos)):.4f}°}}$ · exceso $= {np.degrees(exceso):.5f}° = {exceso:.6f}$ rad
        - área $= \varepsilon R^2$: ${exceso:.5f}$ en la esfera unitaria (el ${100 * exceso / (4 * np.pi):.3f}\,\%$ de $4\pi$), ${exceso * R_TIERRA**2:,.0f}$ km² en la Tierra
        - ley del coseno: $\cos a = {np.cos(lados[0]):.6f}$ y $\cos b\cos c + \sin b\sin c\cos A = {_cos_ley:.6f}$ · ley del seno:
          $\sin A/\sin a = {_seno[0]:.4f}$, $\sin B/\sin b = {_seno[1]:.4f}$, $\sin C/\sin c = {_seno[2]:.4f}$
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return V, angulos, exceso, lados


@app.cell
def _(lib, mo, np):
    _e1, _e2, _e3 = np.eye(3)
    _lo, _ao = lib.triangulo_esferico(_e3, _e1, _e2)
    _g = np.deg2rad(1.0)
    _P, _Q, _Rr = lib.punto_esfera(0, 0), lib.punto_esfera(0, _g), lib.punto_esfera(_g, 0)
    (_a, _b, _c), (_A, _B, _C) = lib.triangulo_esferico(_P, _Q, _Rr)
    _B_ley = lib.angulo_esferico(_b, _a, _c)
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, el cuaderno; derecha, numpy con los tres vectores. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 El octante.** $A = e_3$ (polo), $B = e_1$, $C = e_2$. Lados: $\cos a = \langle e_1, e_2\rangle = 0$,
            $a = 90°$; igual $b = c = 90°$. Ángulo en $A$ por la ley del coseno:

            $$\cos A = \frac{\cos a - \cos b\cos c}{\sin b\,\sin c} = \frac{0 - 0}{1} = 0,\quad A = 90°,$$

            y por simetría $B = C = 90°$. Suma $270°$, exceso $90° = \pi/2$, área $= \tfrac{\pi}{2}R^2 = \tfrac18\cdot4\pi R^2$:
            un octavo de la esfera, como se ve. Cierra.
            """),
            mo.vstack([
                mo.md("```python\nA, B, C = np.eye(3)[2], np.eye(3)[0], np.eye(3)[1]\nlados, angulos = lib.triangulo_esferico(A, B, C)\nexceso = sum(angulos) - np.pi\nnp.allclose(exceso, np.pi / 2)\n```"),
                mo.md(f"lados `{np.round(np.degrees(_lo), 6).tolist()}` · ángulos `{np.round(np.degrees(_ao), 6).tolist()}`  \nexceso `{sum(_ao) - np.pi:.6f}` · `np.allclose(exceso, np.pi / 2)`: `{bool(np.allclose(sum(_ao) - np.pi, np.pi / 2))}`"),
            ]),
        ], widths="equal", align="start"),
        mo.hstack([
            mo.md(rf"""
            **3.2 Un triángulo chico.** $A$ en el ecuador, $B$ a $1°$ de longitud, $C$ a $1°$ de latitud: $b = c = 1°$ y
            el ángulo en $A$ es recto (meridiano contra ecuador). Ley del coseno con $\cos 90° = 0$:
            $\cos a = \cos^2 1°$, $a = \arccos(\cos^2 1°) = {np.degrees(_a):.5f}°$; Pitágoras plano daría
            $\sqrt2° = 1.41421°$. El ángulo en $B$: $\cos B = \dfrac{{\cos b - \cos a\cos c}}{{\sin a\,\sin c}}$,
            $B = {np.degrees(_B_ley):.5f}°$, y $C = B$. Suma ${np.degrees(_A + 2 * _B_ley):.5f}°$: el exceso,
            ${np.degrees(_A + 2 * _B_ley) - 180:.5f}°$, es el área del triángulo rectángulo, $\tfrac12 (1°)^2$ en radianes:
            $\tfrac12(\pi/180)^2 = {0.5 * _g**2:.3e}$ rad $= {np.degrees(0.5 * _g**2):.5f}°$.
            """),
            mo.vstack([
                mo.md("```python\ng = np.deg2rad(1.0)\nA, B, C = punto_esfera(0, 0), punto_esfera(0, g), punto_esfera(g, 0)\n(a, b, c), (alfa, beta, gama) = lib.triangulo_esferico(A, B, C)\nnp.allclose(a, np.arccos(np.cos(g) ** 2))\nnp.allclose(beta, lib.angulo_esferico(b, a, c))\nnp.allclose(alfa + beta + gama - np.pi, g**2 / 2, rtol=1e-4)\n```"),
                mo.md(f"`a` = `{np.degrees(_a):.5f}°` · `alfa` = `{np.degrees(_A):.5f}°` · `beta` = `{np.degrees(_B):.5f}°`  \n"
                      f"`{bool(np.allclose(_a, np.arccos(np.cos(_g) ** 2)))}` · `{bool(np.allclose(_B, _B_ley))}` · exceso vs área: `{bool(np.allclose(_A + _B + _C - np.pi, _g**2 / 2, rtol=1e-4))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(lib, mo, np):
    _p = lib.punto_esfera(np.radians(45.0), np.radians(30.0))
    _q = _p.copy()  # el mismo punto dos veces
    _cos = float(_p @ _q / (np.linalg.norm(_p) * np.linalg.norm(_q)))
    with np.errstate(invalid="ignore"):
        _sin_clip = float(np.arccos(_cos))
    _robusto = float(np.arctan2(np.linalg.norm(np.cross(_p, _q)), _cos))
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **el ángulo entre dos vectores sale más robusto de `np.arctan2(|p × q|, p · q)` que de
        `np.arccos(p · q / (|p||q|))`**. El coseno así calculado puede salirse de $[-1, 1]$ por redondeo: con el punto
        $(45°, 30°)$ contra sí mismo, el cociente da $1.0000000000000002$ (abajo, en vivo) y `arccos` devuelve `nan`.
        Por eso con `arccos` hay que proteger con `np.clip(..., -1, 1)`; además, para ángulos chicos pierde precisión
        porque $\cos$ es plano cerca de $0$ (un error de $10^{-16}$ en el coseno es un error de $10^{-8}$ rad en el ángulo).
        `arctan2` usa el seno (la cuña, $|p\times q|$) y el coseno a la vez, no necesita clip y es exacto en todo el rango:
        es lo que hace `lib.angulo_vertice`. Convertir con `np.degrees` sólo para mostrar.
        """),
        mo.md("```python\np = punto_esfera(np.radians(45), np.radians(30)); q = p.copy()\nnp.arccos(p @ q / (np.linalg.norm(p) * np.linalg.norm(q)))  # nan: el cociente da 1.0000000000000002\nnp.arctan2(np.linalg.norm(np.cross(p, q)), p @ q)  # 0.0\n```"),
        mo.md(f"`p @ q / (|p||q|)` = `{_cos!r}` · `arccos` → `{_sin_clip}` · `arctan2` → `{_robusto}`"),
    ])
    return


@app.cell
def _(R_TIERRA, lib, mo, np):
    _a60 = np.arccos(0.25)
    _B60 = lib.angulo_esferico(np.pi / 3, _a60, np.pi / 3)
    _ex60 = np.pi / 2 + 2 * _B60 - np.pi
    _area10 = np.sqrt(3) / 4 * 10.0**2
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("los problemas geodésicos sobre la superficie de la esfera").* Triángulo con $b = c = 60°$
        y ángulo $A = 90°$. Calculá el lado $a$, los ángulos $B$ y $C$ (ley del coseno), la suma y el exceso. ¿Qué
        fracción de la esfera cubre?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(rf"""
        $\cos a = \cos60°\cos60° + \sin60°\sin60°\cos90° = \tfrac14$, $a = \arccos\tfrac14 = {np.degrees(_a60):.2f}°$.
        $\cos B = \dfrac{{\cos b - \cos a\cos c}}{{\sin a\sin c}} = \dfrac{{0.5 - 0.125}}{{\sin a \cdot 0.866}} = {np.cos(_B60):.4f}$,
        $B = C = {np.degrees(_B60):.2f}°$. Suma ${90 + 2 * np.degrees(_B60):.2f}°$, exceso ${np.degrees(_ex60):.2f}° = {_ex60:.4f}$ rad: área
        ${_ex60:.4f}\,R^2$, el ${100 * _ex60 / (4 * np.pi):.2f}\,\%$ de la esfera.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("verificando si el error obtenido al regresar al punto de origen es compatible con la
        precisión de los instrumentos").* Una poligonal triangular de campo con lados de $10$ km sobre la Tierra
        ($R = 6371$ km). ¿Cuánto exceso esférico trae la suma de sus tres ángulos? ¿Y con lados de $100$ km? ¿Puede un
        cuadrilátero sobre la esfera tener los cuatro ángulos rectos?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(rf"""
        El triángulo es casi plano: área $\approx \tfrac{{\sqrt3}}{{4}}\,10^2 = {_area10:.1f}$ km²; exceso
        $\varepsilon = {_area10:.1f}/6371^2 = {_area10 / R_TIERRA**2:.2e}$ rad $= {np.degrees(_area10 / R_TIERRA**2) * 3600:.2f}''$. Con $100$ km el área es
        $100$ veces mayor: $\varepsilon \approx {np.degrees(100 * _area10 / R_TIERRA**2) * 3600:.0f}''$, ya del orden de lo que mide un teodolito. Nota de
        agrimensura: en topografía se reparte restando $\varepsilon/3$ a cada ángulo (Legendre) y se
        calcula como plano. Cuadrilátero de cuatro rectos: imposible; cortado en dos triángulos la suma es
        $360° + \text{{área}}/R^2 > 360°$.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def lado(p, q):\n    cos = ...          # ⟨p, q⟩ / (|p||q|), protegido con np.clip\n    return ...         # en GRADOS\n",
        language="python", min_height=110, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio.** Completá `lado(p, q)`: dos vectores desde el centro (arrays de 3, no
        necesariamente unitarios) → el lado del triángulo esférico entre ellos, **en grados**. Tenés `np`. Se verifica
        con pares al azar más dos con trampa: el mismo punto dos veces y dos antípodas.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(0xDDDE)
    _pares = [(_rng.normal(size=3), _rng.normal(size=3)) for _ in range(8)]
    _pp = lib.punto_esfera(np.radians(45.0), np.radians(30.0))  # cociente 1.0000000000000002 y −1.0000000000000002
    _pares += [(_pp, _pp.copy()), (2 * _pp, -3 * _pp)]
    _esp = np.array([np.degrees(lib.lado_esferico(p, q)) for p, q in _pares])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        with np.errstate(invalid="ignore"):
            _obt = np.array([float(_ns["lado"](p, q)) for p, q in _pares])
        if np.allclose(_obt, _esp):
            _res = mo.callout(mo.md("✅ coincide en los diez pares, incluidos el punto repetido ($0°$) y las antípodas ($180°$)."), kind="success")
        elif np.isnan(_obt).any() and np.allclose(_obt[~np.isnan(_obt)], _esp[~np.isnan(_obt)]):
            _res = mo.callout(mo.md("❌ casi: en el punto repetido o en las antípodas devolvés `nan`. El cociente se salió de $[-1, 1]$ por redondeo (±1.0000000000000002) y `arccos` no lo acepta: falta `np.clip(..., -1, 1)` (o `arctan2`, sección 4)."), kind="warn")
        elif np.allclose(_obt, np.radians(_esp)):
            _res = mo.callout(mo.md("❌ devolvés **radianes**. Falta `np.degrees(...)` al final."), kind="warn")
        else:
            _i = int(np.argmax(~np.isclose(_obt, _esp)))
            _res = mo.callout(mo.md(f"❌ no coincide. Para el par {_i + 1} se esperaba `{_esp[_i]:.3f}°` y se obtuvo `{_obt[_i]:.3f}`. ¿Dividiste por los dos largos?"), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def angulo_esferico(a, b, c):\n    a, b, c = ...                      # a radianes\n    cos_A = ...                        # despejar de cos a = cos b cos c + sin b sin c cos A\n    return ...                         # en GRADOS\n",
        language="python", min_height=130, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado.** Completá `angulo_esferico(a, b, c)`: tres lados **en grados** → el ángulo
        $A$ opuesto al lado $a$, **en grados**, por la ley del coseno. Tenés `np`. Se verifica con el octante, el
        triángulo del ejercicio (a) y triángulos al azar (los lados salen de tres vectores, así que siempre existe).
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(14)
    _tri = [(90.0, 90.0, 90.0), (np.degrees(np.arccos(0.25)), 60.0, 60.0)]
    for _ in range(6):
        _V = [v / np.linalg.norm(v) for v in _rng.normal(size=(3, 3))]
        _tri.append(tuple(np.degrees(lib.triangulo_esferico(*_V)[0])))
    _esp = np.array([np.degrees(lib.angulo_esferico(*np.radians(t))) for t in _tri])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        with np.errstate(invalid="ignore"):
            _obt = np.array([float(_ns["angulo_esferico"](*t)) for t in _tri])
        _r = [np.radians(t) for t in _tri]
        _sin_dividir = np.array([np.degrees(np.arccos(np.clip(np.cos(a) - np.cos(b) * np.cos(c), -1, 1))) for a, b, c in _r])
        _lado_por_angulo = np.array([np.degrees(np.arccos(np.clip(np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(a), -1, 1))) for a, b, c in _r])
        _en_grados = np.array([np.degrees(np.arccos(np.clip((np.cos(a) - np.cos(b) * np.cos(c)) / (np.sin(b) * np.sin(c)), -1, 1))) for a, b, c in _tri])
        if np.allclose(_obt, _esp):
            _res = mo.callout(mo.md("✅ coincide en los ocho triángulos: $\\cos A = (\\cos a - \\cos b\\cos c)/(\\sin b\\sin c)$."), kind="success")
        elif np.allclose(_obt, _sin_dividir, equal_nan=True):
            _res = mo.callout(mo.md("❌ despejaste mal: falta dividir por $\\sin b\\,\\sin c$ antes del `arccos` (en el octante da lo mismo, por eso ahí no se nota)."), kind="warn")
        elif np.allclose(_obt, _lado_por_angulo):
            _res = mo.callout(mo.md("❌ confundiste lado con ángulo: usaste $a$ como si fuera el ángulo $A$ y calculaste un **lado**. La ley del coseno se despeja para $\\cos A$."), kind="warn")
        elif np.allclose(_obt, _en_grados, equal_nan=True):
            _res = mo.callout(mo.md("❌ le pasaste **grados** a `np.cos` y `np.sin`: convertí con `np.radians` primero."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Para el triángulo (a): se esperaba `{_esp[1]:.3f}°`, se obtuvo `{_obt[1]:.3f}`."), kind="danger")
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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "14_trigonometria_esferica")
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

    Acá verificamos que lados y ángulos de un triángulo esférico salen de productos internos y cuñas de tres vectores, y que
    el exceso es el área. En el apunte está en la sección
    [Polígonos geodésicos y trigonometría esférica](../../apunte.pdf#nameddest=cap:esfera): el triángulo
    como tres planos por el centro, los teoremas del coseno y del seno deducidos con producto interno y determinante, el
    exceso esférico con el control del octante y el problema resuelto entre tres ciudades. Las herramientas y la esfera
    como superficie:

    - [apunte, «Álgebra de las transformaciones» (producto interno y producto vectorial)](../../apunte.pdf#nameddest=cap:formas-lineales) · [apunte, «Superficies, elipsoide, curvatura…» (esfera, métrica y curvatura)](../../apunte.pdf#nameddest=cap:esfera)
    - [ficha de la clase 14](../../clases/14.html) (con la bibliografía: Coxeter, *Geometría*; el apunte sobre el elipsoide) · [unidad anterior: el elipsoide](../13_elipsoide/index.html)

    **Lo que viene:** [Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico](../15_transformaciones_conformes/index.html),
    la unidad que cierra el hilo conductor. De la rotación que deja un mojón quieto a un triángulo sobre la Tierra que no
    cierra en $180°$, todo fue producto interno, cuña y cambio de coordenadas. Para repasar: volvé a
    [la portada](../../index.html) y recorré [el mapa de conceptos](../../mapa.html) con el filtro "hasta la clase N".
    Lo que sigue después es de Topografía y Geodesia: compensar poligonales con el exceso separado, y los problemas directo e
    inverso sobre el elipsoide.
    """)
    return


@app.cell
def _(R_TIERRA, V, V_ciudades, angulos, candidatos, exceso, exceso_c, lados, lados_c, lib, mo, np, suma_c):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _e1, _e2, _e3 = np.eye(3)
    _g = np.deg2rad(1.0)
    _chico = (lib.punto_esfera(0, 0), lib.punto_esfera(0, _g), lib.punto_esfera(_g, 0))
    _a60 = np.arccos(0.25)
    _B60 = lib.angulo_esferico(np.pi / 3, _a60, np.pi / 3)
    _checks = [
        ("sección 0: candidatos distintos; la suma de las tres ciudades supera 180° en el exceso (~1.66°), área ≈ 0.23 % de la esfera",
         len({round(v, 6) for v in candidatos.values()}) == 4 and lib.exacto(suma_c, 180 + np.degrees(exceso_c)) and 1.6 < np.degrees(exceso_c) < 1.7 and 0.2 < 100 * exceso_c / (4 * np.pi) < 0.3),
        ("sección 0: lados de las ciudades entre 900 y 2600 km; ley del seno en las ciudades",
         all(900 < R_TIERRA * l < 2600 for l in lados_c) and lib.exacto(abs(lib.cuna3(*V_ciudades)), np.sin(lados_c[1]) * np.sin(lados_c[2]) * np.sin(lib.triangulo_esferico(*V_ciudades)[1][0]))),
        ("sección 2: el caso elegido cumple la ley del coseno y exceso = suma − π",
         lib.exacto(np.cos(lados[0]), np.cos(lados[1]) * np.cos(lados[2]) + np.sin(lados[1]) * np.sin(lados[2]) * np.cos(angulos[0]), tol=1e-9)
         and lib.exacto(exceso, sum(angulos) - np.pi) and all(np.linalg.norm(v) > 0.999 for v in V)),
        ("3.1: octante, exceso π/2 = un octavo de 4π", lib.exacto(lib.exceso_esferico(_e3, _e1, _e2), np.pi / 2) and lib.exacto(lib.triangulo_esferico(_e3, _e1, _e2)[1], [np.pi / 2] * 3)),
        ("3.2: a = arccos(cos² 1°), B por ley del coseno = B por vectores, exceso ≈ (1°)²/2",
         lib.exacto(lib.triangulo_esferico(*_chico)[0][0], np.arccos(np.cos(_g) ** 2))
         and lib.exacto(lib.triangulo_esferico(*_chico)[1][1], lib.angulo_esferico(lib.triangulo_esferico(*_chico)[0][1], lib.triangulo_esferico(*_chico)[0][0], lib.triangulo_esferico(*_chico)[0][2]))
         and abs(lib.exceso_esferico(*_chico) / (_g**2 / 2) - 1) < 1e-4),
        ("ejercicio (a): a = arccos(1/4) ≈ 75.52°, B = C ≈ 63.43°, exceso ≈ 36.87°",
         abs(np.degrees(_a60) - 75.52) < 0.01 and abs(np.degrees(_B60) - 63.43) < 0.01 and abs(np.degrees(np.pi / 2 + 2 * _B60 - np.pi) - 36.87) < 0.01
         and lib.exacto(_B60, lib.triangulo_esferico(_e3, lib.punto_esfera(np.pi / 6, 0), lib.punto_esfera(np.pi / 6, np.pi / 2))[1][1])),
        ("ejercicio (b): exceso de 10 km ≈ 0.22″ y de 100 km ≈ 22″",
         abs(np.degrees(np.sqrt(3) / 4 * 100 / R_TIERRA**2) * 3600 - 0.22) < 0.01 and abs(np.degrees(np.sqrt(3) / 4 * 1e4 / R_TIERRA**2) * 3600 - 22) < 0.5),
        ("sección 4 y ejercicio (c): (45°, 30°) contra sí mismo da coseno > 1 y contra su antípoda < −1 (sin clip, arccos → nan)",
         (lambda p: p @ p / np.linalg.norm(p) ** 2 > 1 and (2 * p) @ (-3 * p) / (np.linalg.norm(2 * p) * np.linalg.norm(-3 * p)) < -1)(lib.punto_esfera(np.radians(45.0), np.radians(30.0)))),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
