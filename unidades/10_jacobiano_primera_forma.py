# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Jacobiano y primera forma fundamental (lección 10, molde v2 sobre cb104). Clase 9 (14/10/2026).

Una sola idea: r_u, r_v son los ejes locales de la superficie; la jacobiana los tiene como columnas; E, F, G es su tabla
de productos internos (la V Vᵀ de la lección 02) y mide pasitos, ángulos y áreas chicas desde los números (u, v).

Chequear:  uv run marimo check --select MW unidades/10_jacobiano_primera_forma.py
Exportar:  uv run python tools/build.py --only 10_jacobiano_primera_forma
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
    # Jacobiano y primera forma fundamental

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Sigo la clase 9 (14/10/2026). La pregunta: **¿Cómo mido una distancia chica sobre una superficie curva usando sólo
    los números (u, v) de la grilla?** El gancho: *sobre el terreno, un pasito en latitud y otro en longitud no miden lo
    mismo en metros: la primera forma fundamental es la regla que los convierte.*

    Colores, iguales en la figura y en el álgebra: la **primera columna** de la jacobiana es $r_u$, en
    <span style="color:#1b6f6a">**teal**</span>; la **segunda**, $r_v$, en <span style="color:#b5451b">**rust**</span>: los
    **ejes locales**. La grilla $(u, v)$ "antes" va en gris, levantada sobre la superficie en teal, el pasito en
    <span style="color:#7a4e9e">**violeta**</span>. Grados en los controles, radianes adentro.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- la loma y los números de la predicción salen de acá, nunca a mano ----------
    def loma(u, v):
        return lib.xyz(u, v, 2.0 * np.exp(-(u**2 + v**2) / 8.0))

    J_cima, J_ladera = lib.jacobiana_numerica(loma, 0.0, 0.0), lib.jacobiana_numerica(loma, 2.0, 1.0)
    E_c = lib.primera_forma(J_cima)[0]
    E_l, F_l, G_l = lib.primera_forma(J_ladera)
    _t = np.linspace(0, 1, 400)
    cinta_ladera = lib.longitud_poligonal(loma(2.0 + _t, 1.0 + 0 * _t))  # el paso real, medido con cinta
    candidatos = {
        "correcta": (np.sqrt(E_c), np.sqrt(E_l)),
        "siempre-1": (1.0, 1.0),
        "pendiente": (np.sqrt(E_c), 1.0 + abs(J_ladera[2, 0])),  # 1 + |h_u|: sumar la bajada en vez de Pitágoras
        "paso-v": (np.sqrt(E_c), np.sqrt(G_l)),  # el paso en v, no el paso en u
    }
    prediccion = mo.ui.radio(
        options={f"{candidatos[k][0]:.2f} m en la cima, {candidatos[k][1]:.2f} m en la ladera": k
                 for k in ("siempre-1", "pendiente", "correcta", "paso-v")},
        value=None,
        label=r"**Predicción.** El mismo paso $\Delta u = 1$, $\Delta v = 0$ desde la cima $(0, 0)$ y desde la ladera $(2, 1)$. Con cinta, sobre el terreno, mide…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Relevé una loma con el dron y la tengo como modelo digital: a cada par $(u, v)$ de la grilla, en metros, le
        corresponde la altura $h(u, v) = 2\,e^{-(u^2+v^2)/8}$: el punto del terreno es $r(u, v) = (u, v, h(u, v))$. La cima
        está en $(0, 0)$, a $2$ m; en $(2, 1)$ estoy sobre la ladera. Desde los dos puntos doy **el mismo paso en la grilla**:
        una unidad en $u$, nada en $v$.
        """),
        prediccion,
    ])
    return E_c, E_l, F_l, G_l, J_cima, J_ladera, candidatos, cinta_ladera, loma, prediccion


@app.cell
def _(E_l, J_ladera, cinta_ladera, mo, np, prediccion):
    _hu, _hv = J_ladera[2, 0], J_ladera[2, 1]
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     rf"**Sí.** En la cima la loma es horizontal: el paso mide $1$. En la ladera, al avanzar $1$ en $u$ bajo "
                     rf"$h_u = {_hu:.3f}$: el paso es la hipotenusa $\sqrt{{1 + h_u^2}} = {np.sqrt(E_l):.2f}$ m. Ese $1 + h_u^2$ es $E$, el largo al "
                     rf"cuadrado del eje local $r_u = (1, 0, h_u)$. Con cinta mediría ${cinta_ladera:.2f}$ m, porque la pendiente afloja a "
                     rf"lo largo del paso: la regla vale **a primer orden**, para pasitos (sección 2)."),
        "siempre-1": ("warn",
                      r"**No.** $1$ en la grilla es $1$ sobre el terreno sólo donde es horizontal (la cima). En la ladera el paso además "
                      r"baja: el largo es la hipotenusa, más que $1$. La grilla es el plano del dibujo; la superficie, *otro espacio, "
                      r"completamente desconectado* (profesor); entre los dos hay una regla."),
        "pendiente": ("warn",
                      rf"**No.** Sumaste la bajada: $1 + \lvert h_u \rvert = {1 + abs(_hu):.2f}$. El avance $1$ y la bajada $h_u$ son "
                      rf"**perpendiculares**: Pitágoras, $\sqrt{{1 + h_u^2}} = {np.sqrt(E_l):.2f}$, el largo del vector $r_u = (1, 0, h_u)$."),
        "paso-v": ("warn",
                   rf"**No.** ${np.sqrt(1 + _hv**2):.2f}$ m es lo que mide en la ladera un paso de $1$ **en $v$**, donde la loma está "
                   rf"menos empinada ($h_v = {_hv:.3f}$). Pregunté por el paso en $u$: cada eje tiene su largo, $E$ para $u$ y $G$ para $v$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **La derivada es la mejor aproximación lineal en un punto: entra un pasito, sale un pasito.** Hago zoom en un punto
    hasta que la curva parece recta y la superficie parece plana; la derivada es esa recta o ese plano, una transformación
    lineal ("la matriz es lo que le pasa a la grilla", [lección 04](../04_afines_homogeneas/index.html)) que cambia de
    punto a punto. El profesor, con una pelota: *"cortás un pedacito y le hacés zoom, cortás uno más chico y lo escalás de
    nuevo… hay un momento en que el pedazo parece plano. La matriz jacobiana describe esa transformación lineal local."*

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R \to \mathbb R$ | $f(x + \epsilon) \approx f(x) + f'(x)\,\epsilon$: un número | la pendiente: cuánto sube $f$ por cada $dx$ |
    | $\mathbb R \to \mathbb R^2$ | curva $r(t)$: $r'(t)$, un vector | la tangente a la curva; su largo, la velocidad |
    | $\mathbb R^2 \to \mathbb R^3$ | superficie $r(u, v)$: $J = \begin{pmatrix} \textcolor{#1b6f6a}{r_u} & \textcolor{#b5451b}{r_v} \end{pmatrix}$, $3 \times 2$ | dos tangentes, los **ejes locales**; generan el plano tangente |

    **La jacobiana es la matriz que manda la grilla $(u, v)$ al plano tangente.** Entra un vector de $\mathbb R^2$, sale
    uno de $\mathbb R^3$: $3 \times 2$. Columna 1 = a dónde va el eje $u$ ($r_u = \partial r/\partial u$),
    columna 2 = a dónde va el eje $v$; el pasito $(du, dv)$ va a $dr = r_u\,du + r_v\,dv$ y el cuadradito $du \times dv$,
    a un paralelogramo de lados $r_u$, $r_v$. Lo que no se puede recorrer a la salida es la normal $r_u \times r_v$:
    *"el espacio que no puedo recorrer es la normal, por eso el producto cruz"*.

    **La primera forma fundamental es la tabla de productos internos de los ejes locales**, la $V V^T$ sembrada en la
    [lección 02](../02_producto_interno/index.html), con los ejes como columnas:

    $$J^T J = \begin{pmatrix} E & F \\ F & G \end{pmatrix}, \qquad E = \langle r_u, r_u\rangle, \quad F = \langle r_u, r_v\rangle, \quad G = \langle r_v, r_v\rangle.$$

    $E$ y $G$ son los largos al cuadrado de los ejes locales; $F$ dice qué ángulo forman ($F = 0$: perpendiculares). Con
    esa tabla mido sin salir de la grilla: el largo del pasito, $ds^2 = \langle dr, dr\rangle = E\,du^2 + 2F\,du\,dv + G\,dv^2$;
    el ángulo entre dos pasitos (el coseno de la lección 02 con esta tabla); el área del cuadradito,
    $\lvert r_u \times r_v \rvert\,du\,dv = \sqrt{EG - F^2}\,du\,dv$.

    **¿Qué se conserva?** A primer orden, el pasito: direcciones y largos de lo chico. Lo que cambia es la regla: en el
    plano cartesiano $E = G = 1$, $F = 0$ en todos lados; sobre una superficie la tabla depende del punto, y en el polo una
    columna se anula: *"mover la latitud me saca del polo, mover la longitud no me mueve"*.

    Dos cosas más de la clase, en la [ficha 9](../../clases/09.html): el **gradiente** de $h$ *"es una forma lineal, no
    un vector"*, la regla graduada que mide cuánto sube $h$ con cada pasito, $h_u\,du + h_v\,dv$; y la **función implícita**,
    $F(x, y, z) = 0$ define $z = g(x, y)$ cerca de un punto si la normal "le hace sombra" al eje $z$ ($\partial F/\partial z \neq 0$).
    Todo esto es una **muestra**; la demostración está en el apunte, secciones 6 y 13.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- superficies precargadas: r vectorizada; u, v = (lo, hi, paso, valor, etiqueta, factor deslizador→radianes);
    # `antes` = la grilla plana de abajo; qué pasa ----------
    _d = np.pi / 180
    casos = {
        "la loma r = (u, v, 2·exp(−(u²+v²)/8))": dict(
            r=lambda u, v: lib.xyz(u, v, 2.0 * np.exp(-(u**2 + v**2) / 8.0)),
            u=(-3.0, 3.0, 0.25, 2.0, "u", 1.0), v=(-3.0, 3.0, 0.25, 1.0, "v", 1.0),
            antes=lambda u, v: lib.xyz(u, v, 0.0 * u),
            que_pasa=r"$E = 1 + h_u^2$, $F = h_u h_v$, $G = 1 + h_v^2$: en la cima la regla es la identidad; en la ladera los ejes se alargan y se cierran."),
        "plano inclinado z = 1 + 0.4u + 0.3v": dict(
            r=lambda u, v: lib.xyz(u, v, 1.0 + 0.4 * u + 0.3 * v),
            u=(-3.0, 3.0, 0.25, 1.0, "u", 1.0), v=(-3.0, 3.0, 0.25, -1.0, "v", 1.0),
            antes=lambda u, v: lib.xyz(u, v, 0.0 * u),
            que_pasa=r"$r_u = (1, 0, 0.4)$, $r_v = (0, 1, 0.3)$ no dependen del punto: $E, F, G$ **constantes** ($1.16$, $0.12$, $1.09$), como una afinidad."),
        "cilindro de radio 1.5 (u ángulo, v altura)": dict(
            r=lambda u, v: lib.xyz(1.5 * np.cos(u), 1.5 * np.sin(u), v),
            u=(-180.0, 180.0, 5.0, 30.0, "u (°)", _d), v=(-2.0, 2.0, 0.25, 0.5, "v", 1.0),
            antes=lambda u, v: lib.xyz(0.9 * u, v, -2.9 + 0.0 * u),
            que_pasa=r"$E = R^2$, $F = 0$, $G = 1$, constantes: el cilindro se desenrolla sobre el plano sin deformar (es *desarrollable*)."),
        "esfera de radio 2 (φ latitud, λ longitud)": dict(
            r=lambda f, l: lib.xyz(2.0 * np.cos(f) * np.cos(l), 2.0 * np.cos(f) * np.sin(l), 2.0 * np.sin(f)),
            u=(-80.0, 80.0, 5.0, 45.0, "φ (°)", _d), v=(-150.0, 150.0, 5.0, 0.0, "λ (°)", _d),
            antes=lambda f, l: lib.xyz(0.9 * l, 1.5 * f, -2.9 + 0.0 * f),
            que_pasa=r"$E = R^2 = 4$ siempre, $F = 0$ (paralelos ⊥ meridianos), $G = R^2\cos^2\varphi$: a $45°$ vale $2$, hacia el polo $r_\lambda$ desaparece. El caso de agrimensura."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="la loma r = (u, v, 2·exp(−(u²+v²)/8))", label="superficie precargada")
    mo.vstack([
        mo.md(r"""
        ## 2. Manipulación

        Tres capas: **gris**, la grilla $(u, v)$ plana, abajo; **teal**, la misma grilla levantada sobre la superficie, con
        el plano tangente y los ejes locales $r_u$ (teal) y $r_v$ (rust) saliendo del punto; **violeta**, un pasito $(du, dv)$
        en la grilla, su imagen sobre la superficie (curva) y en el plano tangente (punteado, $J\,(du, dv)$). Mové el punto
        y mirá los ejes locales y la tabla $E, F, G$; agrandá el pasito y mirá cuándo la fórmula deja de coincidir con la cinta.
        """),
        caso,
    ])
    return caso, casos


@app.cell
def _(caso, casos, mo):
    _c = casos[caso.value]
    _lo, _hi, _paso, _val, _etq, _f = _c["u"]
    u0 = mo.ui.slider(_lo, _hi, value=_val, step=_paso, label=_etq + " del punto", show_value=True)
    du = (mo.ui.slider(-30, 30, value=10, step=5, label="d" + _etq, show_value=True) if _f != 1.0
          else mo.ui.slider(-1.0, 1.0, value=0.25, step=0.05, label="du", show_value=True))
    _lo, _hi, _paso, _val, _etq, _f = _c["v"]
    v0 = mo.ui.slider(_lo, _hi, value=_val, step=_paso, label=_etq + " del punto", show_value=True)
    dv = (mo.ui.slider(-30, 30, value=5, step=5, label="d" + _etq, show_value=True) if _f != 1.0
          else mo.ui.slider(-1.0, 1.0, value=0.1, step=0.05, label="dv", show_value=True))
    return du, dv, u0, v0


@app.cell
def _(caso, casos, du, dv, go, lib, mo, np, u0, v0):
    _c = casos[caso.value]
    r, antes = _c["r"], _c["antes"]
    _fu, _fv = _c["u"][5], _c["v"][5]
    uu, vv, ddu, ddv = u0.value * _fu, v0.value * _fv, du.value * _fu, dv.value * _fv
    J = lib.jacobiana_numerica(r, uu, vv)
    r_u, r_v = J[:, 0], J[:, 1]
    E, F, G = lib.primera_forma(J)
    p = np.asarray(r(uu, vv), dtype=float)
    factor_area = float(np.linalg.norm(np.cross(r_u, r_v)))
    ang_ejes = np.degrees(lib.angulo(r_u, r_v)) if factor_area > 1e-9 else float("nan")
    l_formula = float(lib.longitud_paso(E, F, G, ddu, ddv))
    _t = np.linspace(0, 1, 200)
    camino = np.asarray(r(uu + _t * ddu, vv + _t * ddv), dtype=float)
    l_cinta = lib.longitud_poligonal(camino)
    coincide = bool(np.allclose(l_formula, l_cinta, rtol=0.01))

    _us = np.linspace(_c["u"][0], _c["u"][1], 13) * _fu
    _vs = np.linspace(_c["v"][0], _c["v"][1], 13) * _fv
    figura = lib.figura_espacio(3.2, f"E = {E:.3f} · F = {F:.3f} · G = {G:.3f}")
    lib.superficie_malla(figura, antes, _us, _vs, lib.GRIS_ANTES, "grilla (u, v) antes", fino=2, ancho=1.5, opacidad=0.6)
    lib.superficie_malla(figura, r, _us, _vs, lib.TEAL_DESPUES, "grilla sobre la superficie", opacidad=0.55)
    _V = lib.VIOLETA_OBJETO
    for _P, _nombre, _linea in ((np.array([antes(uu, vv), antes(uu + ddu, vv + ddv)]), "pasito (du, dv) en la grilla", dict(color=_V, width=7)),
                                (camino, "el pasito sobre la superficie", dict(color=_V, width=7)),
                                (np.array([p, p + J @ [ddu, ddv]]), "J·(du, dv) en el plano tangente", dict(color=_V, width=4, dash="dash"))):
        figura.add_trace(go.Scatter3d(x=_P[:, 0], y=_P[:, 1], z=_P[:, 2], mode="lines", line=_linea, name=_nombre))
    lib.plano_tangente(figura, p, r_u, r_v)
    figura.add_trace(go.Scatter3d(x=[p[0]], y=[p[1]], z=[p[2]], mode="markers", marker=dict(size=6, color="#222"), name="r(u₀, v₀)"))

    _panel = mo.vstack([
        mo.md("**Controles**"), u0, v0, du, dv,
        mo.md(rf"""
        **Números vivos** (radianes adentro)

        $$J = {lib.matriz_coloreada(J)} \ (3 \times 2), \qquad J^T J = {lib.pmat([[E, F], [F, G]])}$$

        - ejes locales: $\lvert r_u \rvert = \sqrt{{E}} = {np.sqrt(E):.3f}$, $\lvert r_v \rvert = \sqrt{{G}} = {np.sqrt(G):.3f}$, ángulo entre ellos $\mathbf{{{ang_ejes:.1f}°}}$
        - factor de área: $\lvert r_u \times r_v \rvert = {factor_area:.3f}$ y $\sqrt{{EG - F^2}} = {np.sqrt(max(E * G - F**2, 0.0)):.3f}$
        - pasito $(du, dv) = ({ddu:.3f}, {ddv:.3f})$: por la fórmula $\sqrt{{E\,du^2 + 2F\,du\,dv + G\,dv^2}} = \mathbf{{{l_formula:.4f}}}$;
          con cinta sobre la superficie (200 tramos) ${l_cinta:.4f}$; `np.allclose(rtol=1%)` → `{coincide}`

        **Qué pasa acá:** {_c["que_pasa"]}
        """),
    ], gap=0.5)
    mo.vstack([mo.ui.plotly(figura), _panel])
    return E, F, G, J, ddu, ddv, factor_area, l_cinta, l_formula, p, r, r_u, r_v, uu, vv


@app.cell
def _(lib, mo, np):
    _R = 6371.0

    def _esfera(phi, lam):
        return lib.xyz(_R * np.cos(phi) * np.cos(lam), _R * np.cos(phi) * np.sin(lam), _R * np.sin(phi))

    _phi, _lam = np.deg2rad(45.0), np.deg2rad(-58.4)
    _J = lib.jacobiana_numerica(_esfera, _phi, _lam)
    _Jx = np.column_stack([[-_R * np.sin(_phi) * np.cos(_lam), -_R * np.sin(_phi) * np.sin(_lam), _R * np.cos(_phi)],
                           [-_R * np.cos(_phi) * np.sin(_lam), _R * np.cos(_phi) * np.cos(_lam), 0.0]])
    _E, _F, _G = lib.primera_forma(_J)
    _ok_J = bool(np.allclose(_J, _Jx))
    _ok_EFG = bool(np.allclose([_E, _F, _G], [_R**2, 0.0, _R**2 * np.cos(_phi) ** 2]))
    paso_1grado = float(lib.longitud_paso(_E, _F, _G, 0.0, np.deg2rad(1.0)))
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        La esfera de radio $R$ con latitud $\varphi$ y longitud $\lambda$ (mi página de Notion usa colatitud; acá, latitud,
        como el apunte). Izquierda, el cuaderno; derecha, numpy: diferencias finitas contra la derivada exacta.
        """),
        mo.hstack([
            mo.md(r"""

            $$r(\varphi, \lambda) = (R\cos\varphi\cos\lambda,\ R\cos\varphi\sin\lambda,\ R\sin\varphi)$$
            $$\textcolor{#1b6f6a}{r_\varphi} = (-R\sin\varphi\cos\lambda,\ -R\sin\varphi\sin\lambda,\ R\cos\varphi), \qquad
            \textcolor{#b5451b}{r_\lambda} = (-R\cos\varphi\sin\lambda,\ R\cos\varphi\cos\lambda,\ 0)$$

            $$E = R^2\sin^2\varphi\,(\cos^2\lambda + \sin^2\lambda) + R^2\cos^2\varphi = R^2, \qquad
            F = R^2\sin\varphi\cos\varphi\,(\cos\lambda\sin\lambda - \sin\lambda\cos\lambda) = 0$$

            $$G = R^2\cos^2\varphi\,(\sin^2\lambda + \cos^2\lambda) = R^2\cos^2\varphi, \qquad ds^2 = R^2\,d\varphi^2 + R^2\cos^2\varphi\,d\lambda^2$$

            Un paso de $1°$ en longitud ($d\lambda = \pi/180$) a latitud $45°$: $ds = \sqrt{G}\,d\lambda = R\cos 45°\cdot\pi/180 = 0.01234\,R$;
            con $R = 6371$ km, $78.6$ km. El mismo grado vale $111.2$ km en el ecuador y $0$ en el polo; un grado de
            latitud, $\sqrt{E}\,d\varphi = 111.2$ km en todos lados.
            """),
            mo.vstack([
                mo.md("```python\nR = 6371.0\ndef esfera(phi, lam):\n    return lib.xyz(R*np.cos(phi)*np.cos(lam), R*np.cos(phi)*np.sin(lam), R*np.sin(phi))\nphi, lam = np.deg2rad(45), np.deg2rad(-58.4)\nJ = lib.jacobiana_numerica(esfera, phi, lam)   # diferencias finitas\nJ_exacta = np.column_stack([r_phi, r_lam])     # las fórmulas de la izquierda\nnp.allclose(J, J_exacta)\nE, F, G = lib.primera_forma(J)                # J.T @ J\nnp.allclose([E, F, G], [R**2, 0, R**2*np.cos(phi)**2])\nlib.longitud_paso(E, F, G, 0, np.deg2rad(1))  # 1° de longitud a 45°\n```"),
                mo.md(f"`J` =\n```\n{np.round(_J, 3)}\n```\n`np.allclose(J, J_exacta)` = `{_ok_J}`  \n"
                      f"`E, F, G` = `{_E:.1f}, {_F:.4f}, {_G:.1f}` · `allclose` con $R^2, 0, R^2\\cos^2\\varphi$: `{_ok_EFG}`  \n"
                      f"1° de longitud a 45°: `{paso_1grado:.2f}` km"),
            ]),
        ], widths="equal", align="start"),
    ])
    return (paso_1grado,)


@app.cell
def _(E_l, F_l, G_l, J_ladera, lib, mo, np):
    _g = J_ladera.T @ J_ladera
    pasos = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0], [0.5, -0.5]])
    largos = np.sqrt(np.sum((pasos @ _g) * pasos, axis=1))
    _ok = bool(np.allclose(largos, lib.longitud_paso(E_l, F_l, G_l, pasos[:, 0], pasos[:, 1])))
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **la jacobiana por diferencias finitas, y una nube de pasos medida de una vez**.
        `lib.jacobiana_numerica(r, u, v)` evalúa $r$ en $u \pm h$ y $v \pm h$ y apila las dos columnas ($3\times2$); `J.T @ J`
        es la tabla $E, F, G$ y `np.linalg.norm(np.cross(J[:, 0], J[:, 1]))` el factor de área. Con los pasos como filas
        de un array $N\times2$, `np.sum((pasos @ g) * pasos, axis=1)` es la forma cuadrática fila por fila, sin bucles.
        """),
        mo.md("```python\nJ = lib.jacobiana_numerica(loma, 2.0, 1.0)      # la ladera de la sección 0\ng = J.T @ J                                     # [[E, F], [F, G]]\nnp.linalg.norm(np.cross(J[:, 0], J[:, 1]))     # = sqrt(E G - F²)\npasos = np.array([[1, 0], [0, 1], [1, 1], [0.5, -0.5]])   # shape (4, 2): una fila por paso\nlargos = np.sqrt(np.sum((pasos @ g) * pasos, axis=1))     # shape (4,)\n```"),
        mo.md(f"`g` =\n```\n{np.round(_g, 4)}\n```\n`pasos.shape` = `{pasos.shape}` → `largos` = `{np.round(largos, 4).tolist()}`; "
              f"factor de área `{np.linalg.norm(np.cross(J_ladera[:, 0], J_ladera[:, 1])):.4f}`; `lib.longitud_paso` da lo mismo: `{_ok}`."),
    ])
    return largos, pasos


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("la matriz jacobiana describe esa transformación lineal local").* Cilindro de radio
        $R = 10$ m, $r(u, v) = (R\cos u,\ R\sin u,\ v)$ con $u$ el ángulo y $v$ la altura. Calculá $r_u$, $r_v$ y la tabla
        $E, F, G$. ¿Cuánto mide sobre el cilindro un paso de $1°$ en $u$? ¿Y uno de $1$ m en $v$?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $r_u = (-R\sin u,\ R\cos u,\ 0)$, $r_v = (0, 0, 1)$. $E = R^2\sin^2 u + R^2\cos^2 u = R^2 = 100$, $F = 0$, $G = 1$:
        constantes. Paso de $1°$ en $u$: $\sqrt{E}\,du = 10\cdot\pi/180 = 0.1745$ m (el arco); de $1$ m en $v$: $\sqrt{G}\,dv = 1$ m.
        Es la regla del plano con el eje $u$ reescalado por $R$: el cilindro se desenrolla sin deformar.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("no hay base privilegiada salvo por el producto interno").* ¿Por qué $F = 0$ significa
        ejes locales perpendiculares? Después, para el plano inclinado $z = 1 + 0.4u + 0.3v$ de la sección 2, calculá a
        qué ángulo se cruzan sobre el plano las líneas de la grilla, perpendiculares en el papel.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $F = \langle r_u, r_v\rangle = \lvert r_u \rvert\,\lvert r_v \rvert \cos\theta$ (lección 02). Si ninguno es nulo,
        $F = 0 \iff \cos\theta = 0 \iff \theta = 90°$: la sombra de un eje sobre el otro es nula. Plano inclinado:
        $r_u = (1, 0, 0.4)$, $r_v = (0, 1, 0.3)$; $E = 1.16$, $G = 1.09$, $F = 0.12$; $\cos\theta = 0.12/\sqrt{1.16 \cdot 1.09} = 0.1067$,
        $\theta \approx 83.9°$: a $90°$ en el papel, a $83.9°$ sobre el plano.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def primera_forma(r, u, v):\n    J = jacobiana(r, u, v)    # 3×2: columnas r_u, r_v\n    E = ...\n    F = ...\n    G = ...\n    return E, F, G\n",
        language="python", min_height=150, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio.** Completá `primera_forma(r, u, v)`: la terna $(E, F, G)$ de la superficie `r` en
        `(u, v)`. Tenés `np` y `jacobiana(r, u, v)`, que devuelve la $3\times2$. Se verifica con `np.allclose` sobre la
        esfera, la loma y el plano inclinado.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, loma, mo, np):
    _casos = [
        (lambda f, l: lib.xyz(2 * np.cos(f) * np.cos(l), 2 * np.cos(f) * np.sin(l), 2 * np.sin(f)), np.deg2rad(45), np.deg2rad(20)),
        (loma, 2.0, 1.0),
        (lambda u, v: lib.xyz(u, v, 1 + 0.4 * u + 0.3 * v), 0.3, -1.0),
    ]
    _Js = [lib.jacobiana_numerica(r, u, v) for r, u, v in _casos]
    _esperado = np.array([lib.primera_forma(J) for J in _Js])
    _ns = {"np": np, "jacobiana": lib.jacobiana_numerica}
    try:
        exec(editor_c.value, _ns)
        _salidas = [_ns["primera_forma"](r, u, v) for r, u, v in _casos]
        _obtenido = np.array(_salidas, dtype=float) if all(np.shape(s) == (3,) for s in _salidas) else None
        if _obtenido is None and any(np.shape(s) == (3, 3) for s in _salidas):
            _res = mo.callout(mo.md("❌ devolvés una $3\\times3$: `J @ J.T`, los productos de las **filas** ($x, y, z$). La tabla de los ejes locales es `J.T @ J`, $2\\times2$."), kind="danger")
        elif _obtenido is None:
            _res = mo.callout(mo.md(f"❌ el resultado tiene forma `{np.shape(_salidas[0])}`; tiene que ser una terna `(E, F, G)`."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los tres casos: $E, F, G$ son la diagonal y la esquina de `J.T @ J`."), kind="success")
        elif np.allclose(_obtenido, [(J[0] @ J[0], J[0] @ J[1], J[1] @ J[1]) for J in _Js]):
            _res = mo.callout(mo.md("❌ multiplicaste **filas** (`J[0] @ J[1]`). Los ejes locales son las **columnas**, `J[:, 0]` y `J[:, 1]`."), kind="warn")
        elif np.allclose(_obtenido, np.column_stack([np.sqrt(_esperado[:, 0]), _esperado[:, 1], np.sqrt(_esperado[:, 2])])):
            _res = mo.callout(mo.md("❌ olvidaste el cuadrado: $E = \\lvert r_u \\rvert^2$, no $\\lvert r_u \\rvert$ (lo mismo $G$). En la esfera tiene que dar $R^2 = 4$, no $2$."), kind="warn")
        elif np.allclose(_obtenido, _esperado[:, ::-1]):
            _res = mo.callout(mo.md("❌ $E$ y $G$ al revés: $E$ va con la **primera** columna ($r_u$, teal), $G$ con la segunda. En la esfera $E = R^2$ es el constante."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Esfera en $(45°, 20°)$: esperaba `{np.round(_esperado[0], 4).tolist()}`, obtuve `{np.round(_obtenido[0], 4).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def longitud_paso(E, F, G, du, dv):\n    return ...     # el largo del pasito (du, dv) sobre la superficie\n",
        language="python", min_height=90, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado.** Completá `longitud_paso(E, F, G, du, dv)`: el largo sobre la superficie de
        un pasito $(du, dv)$ con la tabla del punto. Tenés `np`. Se verifica con `np.allclose` sobre tablas y pasos al
        azar, más el grado de longitud a $45°$ de la sección 3.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _E, _G = _rng.uniform(0.5, 4.0, 12), _rng.uniform(0.5, 4.0, 12)
    _F = _rng.uniform(-0.8, 0.8, 12) * np.sqrt(_E * _G)  # EG − F² > 0: tablas de verdad
    _du, _dv = _rng.uniform(-1, 1, 12), _rng.uniform(-1, 1, 12)
    _E, _F, _G = np.append(_E, 6371.0**2), np.append(_F, 0.0), np.append(_G, 6371.0**2 * np.cos(np.deg2rad(45)) ** 2)
    _du, _dv = np.append(_du, 0.0), np.append(_dv, np.deg2rad(1.0))
    _esperado = lib.longitud_paso(_E, _F, _G, _du, _dv)
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _obtenido = np.array([float(_ns["longitud_paso"](e, f, g, a, b)) for e, f, g, a, b in zip(_E, _F, _G, _du, _dv)])
        if np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los 13 casos, incluido el grado de longitud a 45° (78.6 km)."), kind="success")
        elif np.allclose(_obtenido, _esperado**2):
            _res = mo.callout(mo.md("❌ devolvés $ds^2$, el largo **al cuadrado**: falta la raíz, como $\\lvert v \\rvert = \\sqrt{\\langle v, v\\rangle}$ en la lección 02."), kind="warn")
        elif np.allclose(_obtenido, np.sqrt(_E * _du**2 + _F * _du * _dv + _G * _dv**2)):
            _res = mo.callout(mo.md("❌ falta el $2$ en $2F\\,du\\,dv$: al desarrollar $\\langle r_u du + r_v dv,\\ r_u du + r_v dv\\rangle$ el término cruzado aparece dos veces."), kind="warn")
        else:
            _i = int(np.argmax(~np.isclose(_obtenido, _esperado)))
            _res = mo.callout(mo.md(f"❌ no coincide. Con `E, F, G = {_E[_i]:.3f}, {_F[_i]:.3f}, {_G[_i]:.3f}`, `du, dv = {_du[_i]:.3f}, {_dv[_i]:.3f}`: esperaba `{_esperado[_i]:.4f}`, obtuve `{_obtenido[_i]:.4f}`."), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré que los ejes locales son las columnas de la jacobiana y que su tabla de productos internos mide desde la
    grilla. Las demostraciones:

    - [apunte, sección 6: pasar del plano a una superficie](../../apunte.pdf#nameddest=cap:06)
    - [apunte, sección 13: coordenadas curvilíneas, espacio tangente, métrica](../../apunte.pdf#nameddest=cap:13)
    - [ficha de la clase 9](../../clases/09.html) (gradiente como forma lineal, función implícita) ·
      [lección 02](../02_producto_interno/index.html) · [el camino](../../index.html)

    **Lo que viene:** [curvatura](../12_curvatura/index.html) (anticipada, pendiente de validar): cuánto se aparta la
    superficie de su plano tangente, la **segunda forma fundamental**. El hilo: $E, F, G$ es la regla; la curvatura es
    cuánto se dobla.
    """)
    return


@app.cell
def _(E, E_c, E_l, F, F_l, G, G_l, J, J_cima, J_ladera, candidatos, cinta_ladera, ddu, ddv, factor_area, l_cinta, l_formula, largos, lib, loma, mo, np, p, paso_1grado, pasos, r, r_u, r_v, uu, vv):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _hu, _hv = J_ladera[2, 0], J_ladera[2, 1]
    _t = np.linspace(0, 1, 200)
    _chico = lib.longitud_poligonal(r(uu + _t * ddu / 10, vv + _t * ddv / 10))  # el pasito diez veces más chico
    _checks = [
        ("sección 0: cuatro candidatos distintos; en la cima el paso mide 1",
         len({round(b, 6) for _, b in candidatos.values()}) == 4 and lib.exacto(E_c, 1.0, tol=1e-7) and lib.exacto(J_cima[2], [0, 0], tol=1e-7)),
        ("sección 0: ladera E = 1 + h_u², F = h_u h_v, G = 1 + h_v²; la cinta mide menos que √E",
         lib.exacto([E_l, F_l, G_l], [1 + _hu**2, _hu * _hv, 1 + _hv**2], tol=1e-7) and 1.0 < cinta_ladera < np.sqrt(E_l)),
        ("sección 2: Jᵀ J = [[E, F], [F, G]], |r_u × r_v|² = EG − F², columnas r_u, r_v, p sobre la superficie",
         lib.exacto(J.T @ J, [[E, F], [F, G]], tol=1e-7) and lib.exacto(factor_area**2, E * G - F**2, tol=1e-6)
         and lib.exacto(J[:, 0], r_u) and lib.exacto(J[:, 1], r_v) and lib.exacto(p, r(uu, vv))),
        ("sección 2: la fórmula es |J·(du, dv)|; con el pasito ÷10 coincide con la cinta al 0.1% (primer orden)",
         lib.exacto(l_formula, np.linalg.norm(J @ [ddu, ddv]), tol=1e-9) and abs(_chico - l_formula / 10) <= 1e-3 * l_formula / 10
         and abs(l_cinta - l_formula) <= 0.05 * l_formula),
        ("sección 3: 1° de longitud a 45° = R cos45° π/180 = 78.6 km",
         lib.exacto(paso_1grado, 6371.0 * np.cos(np.deg2rad(45)) * np.deg2rad(1), tol=1e-6) and abs(paso_1grado - 78.6) < 0.05),
        ("sección 4: la nube de pasos da los largos de la fórmula; el paso (1, 0) mide √E",
         lib.exacto(largos, lib.longitud_paso(E_l, F_l, G_l, pasos[:, 0], pasos[:, 1])) and lib.exacto(largos[0], np.sqrt(E_l))),
        ("ejercicios: cilindro R = 10 → (100, 0, 1); plano inclinado 83.9°; la loma es la misma r en toda la lección",
         lib.exacto(lib.primera_forma(lib.jacobiana_numerica(lambda u, v: lib.xyz(10 * np.cos(u), 10 * np.sin(u), v), 0.7, 1.0)), [100, 0, 1], tol=1e-5)
         and abs(np.degrees(lib.angulo([1, 0, 0.4], [0, 1, 0.3])) - 83.9) < 0.05 and lib.exacto(loma(2.0, 1.0), [2, 1, 2 * np.exp(-5 / 8)])),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
