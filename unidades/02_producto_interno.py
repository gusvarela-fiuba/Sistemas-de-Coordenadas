# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Producto interno: proyección, longitud, ángulo (lección 02, molde v2 sobre cb104). Clase 1.

Una sola idea: una sola cuenta con las coordenadas (suma de productos) mide cuánto de un vector cae sobre otro; de ahí
salen longitud, distancia, ángulo y perpendicularidad, y es lo que una rotación conserva. Entre Rotaciones III y Reflexiones.

Chequear:  uv run marimo check --select MW unidades/02_producto_interno.py
Exportar:  uv run python tools/build.py --only 02_producto_interno
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
    # Producto interno: proyección, longitud, ángulo

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Sigo la clase 1. La pregunta: **¿qué cuenta con dos columnas de coordenadas me da la distancia entre dos mojones, el
    ángulo entre dos lados y cuánto de un lado cae sobre el otro?** El gancho: con las coordenadas de tres mojones
    calculo el ángulo en el vértice sin medirlo, y proyecto un lado sobre el rumbo de la línea de base.

    Colores: $u$, sobre el que proyecto, en <span style="color:#1b6f6a">**teal**</span>; $v$, el proyectado, en
    <span style="color:#b5451b">**rust**</span>; su sombra en <span style="color:#c9a227">**gold**</span>. Grados en los
    controles, radianes adentro.

    ## 0. Situación de campo y predicción

    Tres mojones en el sistema de la obra, en metros: $A = (6, 4)$, $B = (2, 1)$, $C = (6, -2)$; la línea de base es
    $BA$. Quiero dos números sin volver al campo: el **ángulo en $B$** entre $BA$ y $BC$, y **cuánto de $BC$ cae sobre la
    dirección $BA$** (su sombra sobre la línea de base). Los vectores salen restando coordenadas: $BA = A - B = (4, 3)$ y
    $BC = C - B = (4, -3)$, los dos de largo $5$.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("02_producto_interno"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- los números de la predicción salen de acá, nunca a mano ----------
    A, B, C = np.array([6.0, 4.0]), np.array([2.0, 1.0]), np.array([6.0, -2.0])
    BA, BC = A - B, C - B
    candidatos = {
        "correcta": float(BC @ BA) / np.linalg.norm(BA),  # sombra de BC sobre BA: ⟨BC, BA⟩ / |BA|
        "distancia": float(np.linalg.norm(BC)),  # el largo entero de BC
        "seno": float(np.linalg.norm(BC) * np.sin(lib.angulo(BC, BA))),  # la parte perpendicular, no la sombra
        "sumar": float(BC.sum()),  # sumar coordenadas en vez de multiplicar y sumar
    }
    prediccion = mo.ui.radio(
        options={f"{candidatos[k]:g} m": k for k in ("sumar", "correcta", "seno", "distancia")},
        value=None,
        label=r"**Predicción.** De los $5$ m del lado $BC = (4, -3)$, sobre la dirección de $BA = (4, 3)$ caen…",
    )
    prediccion
    return A, B, BA, BC, C, candidatos, prediccion


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success",
                     r"**Sí.** Coordenada por coordenada y sumo: $4\cdot4 + (-3)\cdot3 = 7$; dividido por el largo de $BA$, "
                     r"$7/5 = 1.4$ m. Esa cuenta es el **producto interno**, y de ella sale también el ángulo: "
                     r"$\cos\hat B = 7/(5\cdot5) = 0.28$, $\hat B \approx 73.7°$. La sección 2 lo muestra como sombra."),
        "distancia": ("warn",
                      r"**No.** $5$ m es el largo **entero** de $BC$; sobre $BA$ cae sólo su sombra, más corta salvo que los dos "
                      r"apunten igual. Confundiste proyección con distancia: la proyección es la distancia **por el coseno**."),
        "seno": ("warn",
                 r"**No.** $4.8 = 5\sin\hat B$ es la parte de $BC$ **perpendicular** a $BA$: lo que queda afuera de la "
                 r"sombra, no la sombra. La sombra va con el coseno: $5\cos\hat B = 1.4$. Pitágoras lo cierra: "
                 r"$1.4^2 + 4.8^2 = 25 = 5^2$."),
        "sumar": ("warn",
                  r"**No.** $4 + (-3) = 1$ suma las coordenadas de $BC$, y eso no mide nada: cambia si giro los ejes aunque el "
                  r"mojón no se mueva (lección I). La cuenta que mide multiplica coordenada **con** coordenada del otro vector y "
                  r"recién después suma: $4\cdot4 + (-3)\cdot3 = 7$."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **Una sola cuenta mide cuánto de un vector cae sobre otro.** Con la regla mido largos y con el transportador
    ángulos; el producto interno hace las dos cosas de una vez con las coordenadas:

    $$\langle v, u\rangle = |v|\,|u|\cos\theta = x_1 x_2 + y_1 y_2.$$

    A la izquierda, geometría: la sombra de $v$ sobre $u$ (que mide $|v|\cos\theta$) por el largo de $u$. A la derecha,
    aritmética: coordenada por coordenada, y sumo. Que den lo mismo se **muestra** así: con $u = (|u|, 0)$ sobre el eje
    $x$ y $v = (|v|\cos\theta, |v|\sin\theta)$, la suma de productos da $|u|\,|v|\cos\theta$ directo; para un par
    cualquiera giro los dos hasta que $u$ caiga sobre el eje $x$, y girar no cambia la cuenta (Rotaciones II, 3.2). La
    demostración está en el apunte, sección 7.

    | | la cuenta | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $\langle v, u\rangle = v\,u$, dos números multiplicados | el signo dice si apuntan para el mismo lado; $v\,v = \lvert v\rvert^2$ |
    | $\mathbb R^2$ | $x_1x_2 + y_1y_2$ | la sombra de $v$ sobre $u$, por el largo de $u$ |
    | $\mathbb R^3$ | $x_1x_2 + y_1y_2 + z_1z_2$ | la misma sombra; la fórmula sólo suma un término |
    | $\mathbb R^n$ | $\sum_i x_i y_i$ | la fórmula no se entera de la dimensión |

    **Cuatro consecuencias, cuatro líneas:**

    - longitud: $|v| = \sqrt{\langle v, v\rangle}$ (la sombra de $v$ sobre sí mismo es $v$ entero);
    - distancia entre dos mojones: $d(A, B) = |B - A| = \sqrt{\langle B - A, B - A\rangle}$;
    - ángulo: $\cos\theta = \dfrac{\langle v, u\rangle}{|v|\,|u|}$;
    - perpendiculares $\iff \langle v, u\rangle = 0$ (sombra nula).

    Y la frase del profesor: **no hay base privilegiada salvo por el producto interno**. La canónica es especial sólo
    porque sobre ella la cuenta $\sum x_i y_i$ mide de verdad, y eso pasa porque sus ejes son perpendiculares y de largo
    $1$. Conservar esa cuenta es conservar regla y transportador: es lo que define a una rotación (Rotaciones II).
    """)
    return


@app.cell
def _(mo, np):
    mo.md(r"""
    ## 2. Manipulación

    $u$ en **teal** (fijo: $(4, 3)$, la línea de base $BA$), $v$ en **rust**, en **gold** la sombra de $v$ sobre $u$,
    punteado el pie de la perpendicular, y el arco marca $\theta$. Elegí un caso o pasá a **a mano** y mové ángulo y
    largo de $v$: mirá cuándo la sombra se achica, cuándo cambia de signo y cuándo es $0$.
    """)
    casos = {
        "el triángulo de mojones: v = BC": ("fijo", np.array([4.0, -3.0]), r"$\langle v,u\rangle = 7 > 0$: ángulo agudo, la sombra apunta como $u$."),
        "perpendiculares": ("fijo", np.array([-3.0, 4.0]), r"$\langle v,u\rangle = 0$: sombra nula, $\theta = 90°$. El producto interno **detecta** la perpendicular."),
        "paralelos": ("fijo", np.array([2.0, 1.5]), r"$v$ es media vez $u$: la sombra es $v$ entero, $\cos\theta = 1$."),
        "opuestos": ("fijo", np.array([-4.0, -3.0]), r"$\langle v,u\rangle = -25 < 0$: la sombra apunta al revés, $\theta = 180°$."),
        "a mano": ("mano", None, r"$\theta$ es el ángulo del deslizador; la sombra vale $|v|\cos\theta$, positiva, nula o negativa."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="el triángulo de mojones: v = BC", label="caso precargado")
    u = np.array([4.0, 3.0])
    return caso, casos, u


@app.cell
def _(caso, casos, mo):
    # los deslizadores sólo mandan en "a mano"; en los casos precargados quedan deshabilitados
    a_mano = casos[caso.value][0] == "mano"
    phi = mo.ui.slider(-180, 180, value=60, step=1, label="θ (°): ángulo de v respecto de u", show_value=True, disabled=not a_mano)
    largo = mo.ui.slider(0.5, 6, value=4.0, step=0.5, label="|v|", show_value=True, disabled=not a_mano)
    return a_mano, largo, phi


@app.cell
def _(a_mano, caso, casos, go, largo, lib, mo, np, phi, u):
    _, _v_fijo, que_pasa = casos[caso.value]
    v = largo.value * (lib.rot2(np.deg2rad(phi.value)) @ (u / np.linalg.norm(u))) if a_mano else _v_fijo
    vu = float(v @ u)
    nv, nu = float(np.linalg.norm(v)), float(np.linalg.norm(u))
    theta = lib.angulo(v, u)
    sombra = vu / nu  # proyección escalar
    p = lib.proyeccion(v, u)  # proyección vectorial

    rango = 6
    figura = lib.figura_plano(rango, f"⟨v, u⟩ = {vu:.2f} · θ = {np.degrees(theta):.1f}°")
    lib.capa_antes(figura, rango, cuadrado=False)
    _d = u / nu * rango
    figura.add_trace(go.Scatter(x=[-_d[0], _d[0]], y=[-_d[1], _d[1]], mode="lines", line=dict(color=lib.GRIS_ANTES, width=1, dash="dash"),
                                name="recta de u", hoverinfo="skip"))
    figura.add_trace(go.Scatter(x=[v[0], p[0]], y=[v[1], p[1]], mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=1.5, dash="dot"),
                                name="pie de la perpendicular", hoverinfo="skip"))
    lib.flecha(figura, (0, 0), p, lib.COLORES[2], "sombra de v sobre u", ancho=7)
    lib.flecha(figura, (0, 0), u, lib.COLORES[0], "u = (4, 3)")
    lib.flecha(figura, (0, 0), v, lib.COLORES[1], "v")
    lib.arco_angulo(figura, u, v, radio=1.2, texto="θ")
    _R = lib.rot2(np.deg2rad(37))  # girar los dos juntos no cambia la cuenta (Rotaciones II, 3.2)

    _panel = mo.vstack([
        mo.md("**Controles**"), caso, phi, largo,
        mo.md(rf"""
        **Números vivos**

        - $\langle v, u\rangle = {lib.num_tex(vu)}$ · $|v| = {lib.num_tex(nv)}$ · $|u| = {lib.num_tex(nu)}$
        - $\cos\theta = {lib.num_tex(vu / (nv * nu))}$ · $\theta = \mathbf{{{np.degrees(theta):.1f}°}}$
        - sombra (proyección escalar) $= |v|\cos\theta = {lib.num_tex(sombra)}$
        - proyección vectorial $= \dfrac{{\langle v,u\rangle}}{{\langle u,u\rangle}}\,u = {lib.vec_tex(p)}$

        **Qué pasa acá:** {que_pasa} Girados los dos $37°$: $\langle Rv, Ru\rangle = {lib.num_tex((_R @ v) @ (_R @ u))}$, el
        mismo número; una rotación conserva la cuenta, y con ella largos, ángulos y sombras
        ([Rotaciones II](../01b_rotacion_plano/index.html)).
        """),
    ], gap=0.6)
    mo.hstack([_panel, mo.ui.plotly(figura)], widths=[1, 2], align="start")
    return p, sombra, theta, v, vu


@app.cell
def _(BA, BC, lib, mo, np):
    _vu, _nBA, _nBC = float(BC @ BA), float(np.linalg.norm(BA)), float(np.linalg.norm(BC))
    _theta = lib.angulo(BC, BA)
    _p = lib.proyeccion(BC, BA)
    _AC2 = float((BA - BC) @ (BA - BC))
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        El triángulo de mojones de la sección 0: $u = BA = (4, 3)$, $v = BC = (4, -3)$. Izquierda, el cuaderno; derecha,
        numpy. Si no coinciden, algo está mal en uno de los dos.
        """),
        mo.hstack([
            mo.md(r"""

            $$\langle v, u\rangle = \textcolor{#b5451b}{4}\cdot\textcolor{#1b6f6a}{4} + \textcolor{#b5451b}{(-3)}\cdot\textcolor{#1b6f6a}{3} = 16 - 9 = 7$$
            $$|u| = \sqrt{16 + 9} = 5, \qquad |v| = \sqrt{16 + 9} = 5$$
            $$\cos\hat B = \frac{7}{5\cdot5} = 0.28, \qquad \hat B = \arccos 0.28 \approx 73.74°$$
            $$\text{sombra} = \frac{7}{5} = 1.4, \qquad \text{proyección} = \frac{7}{25}\,(4, 3) = (1.12,\ 0.84)$$

            Control por la ley del coseno: $|AC|^2 = |BA|^2 + |BC|^2 - 2\langle BA, BC\rangle = 25 + 25 - 14 = 36$, y en
            efecto $AC = C - A = (0, -6)$ mide $6$.
            """),
            mo.vstack([
                mo.md("```python\nBA, BC = A - B, C - B\nvu = BC @ BA\ncos_B = vu / (np.linalg.norm(BC) * np.linalg.norm(BA))\nang_B = np.degrees(np.arccos(cos_B))\nsombra = vu / np.linalg.norm(BA)\nproy = vu / (BA @ BA) * BA\nAC = C - A\nnp.allclose(AC @ AC, BA @ BA + BC @ BC - 2 * vu)\n```"),
                mo.md(f"`vu` = `{_vu:g}` · `cos_B` = `{_vu / (_nBC * _nBA):.2f}` · `ang_B` = `{np.degrees(_theta):.2f}`  \n"
                      f"`sombra` = `{_vu / _nBA:g}` · `proy` = `{np.round(_p, 3).tolist()}`  \n"
                      f"ley del coseno: `{bool(np.allclose(_AC2, _nBA**2 + _nBC**2 - 2 * _vu))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(BA, BC, mo, np):
    V = np.vstack([BA, BC])  # una fila por vector: los dos lados que salen de B
    G = V @ V.T
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        `v @ u` es el producto interno, `np.linalg.norm(v)` el largo, y el ángulo es
        `np.arccos(np.clip(v @ u / (norm(v) * norm(u)), -1, 1))`: el `clip` está porque con paralelos el cociente puede
        dar $1.0000000000000002$ y `arccos` devuelve `nan`. La idea nueva: con los vectores como filas de un array
        $N\times2$, **`V @ V.T` es la tabla de todos los productos internos de una vez**, largos al cuadrado en la
        diagonal y productos cruzados afuera: largos y ángulos del conjunto en una matriz. En la fase de superficies
        esa tabla vuelve con nombre propio: $E$, $F$, $G$.
        """),
        mo.md("```python\nV = np.vstack([BA, BC])      # shape (2, 2): una fila por vector\nG = V @ V.T                  # tabla de productos internos\n```"),
        mo.md(f"`V.shape` = `{V.shape}` → `G` =\n```\n{G.astype(int)}\n```\n"
              f"`G[0, 0]` = $|BA|^2$ = `{G[0, 0]:g}`, `G[1, 1]` = $|BC|^2$ = `{G[1, 1]:g}`, `G[0, 1]` = $\\langle BA, BC\\rangle$ = `{G[0, 1]:g}`."),
    ])
    return G, V


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("El producto interno puede servir como base para definir tipos de transformaciones").*
        $u = (3, 4)$. Calculá $|u|$ y el vector de largo $1$ en su dirección. Después decidí, sin dibujar, si
        $w = (4, -3)$ es perpendicular a $u$, y cuánto vale la sombra de $(6, 2)$ sobre $u$.
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $|u| = \sqrt{9 + 16} = 5$; el unitario es $u/5 = (0.6, 0.8)$. $\langle w, u\rangle = 12 - 12 = 0$: perpendicular.
        Sombra de $(6, 2)$: $\langle (6,2), u\rangle / |u| = (18 + 8)/5 = 5.2$.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("Hay transformaciones que se definen completamente por qué propiedades de los objetos
        transformados mantienen").* Mojones $A = (7, 6)$, $B = (10, 10)$, $C = (14, 7)$. Sin transportador: ¿cuánto vale
        el ángulo en $B$? Calculá $|AC|$ de dos maneras: restando coordenadas y por la ley del coseno. Después girá los
        tres mojones $90°$ alrededor del origen y repetí la primera cuenta: ¿qué cambió?
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $BA = (-3, -4)$, $BC = (4, -3)$: $\langle BA, BC\rangle = -12 + 12 = 0$, así que $\hat B = 90°$ sin medir nada.
        $AC = C - A = (7, 1)$, $|AC| = \sqrt{50} \approx 7.07$; por la ley del coseno $|AC|^2 = 25 + 25 - 0 = 50$. ✓
        Girados $90°$: $BA \mapsto (4, -3)$, $BC \mapsto (3, 4)$, y $12 - 12 = 0$ otra vez. Cambiaron todas las
        coordenadas; el producto interno, no: la rotación conserva regla y transportador.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def angulo(v, u):\n    cos = ...          # ⟨v,u⟩ / (|v||u|), protegido con np.clip\n    return ...         # en GRADOS\n",
        language="python", min_height=120, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio.** Completá `angulo(v, u)`: dos vectores (arrays de 2) → el ángulo entre ellos
        **en grados**, en $[0°, 180°]$. Tenés `np`. Se verifica con `np.allclose` sobre pares al azar más tres con trampa:
        perpendiculares, opuestos y paralelos.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _rng = np.random.default_rng(56798)
    _pares = [(_rng.uniform(-5, 5, 2), _rng.uniform(-5, 5, 2)) for _ in range(10)]
    _pares += [(np.array([4.0, 3.0]), np.array([-3.0, 4.0])), (np.array([1.0, 0.0]), np.array([-2.0, 0.0])), (0.3 * np.array([0.1, 0.6]), np.array([0.1, 0.6]))]
    _esperado = np.array([np.degrees(lib.angulo(v, u)) for v, u in _pares])
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        with np.errstate(invalid="ignore"):
            _obtenido = np.array([float(_ns["angulo"](v, u)) for v, u in _pares])
        _cos = np.array([float(v @ u) / (np.linalg.norm(v) * np.linalg.norm(u)) for v, u in _pares])
        if np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los 13 pares, incluidos los paralelos (ahí sin `clip` daba `nan`)."), kind="success")
        elif np.isnan(_obtenido).any() and np.allclose(_obtenido[~np.isnan(_obtenido)], _esperado[~np.isnan(_obtenido)]):
            _res = mo.callout(mo.md("❌ casi: en el par paralelo devolvés `nan`. El cociente dio $1.0000000000000002$ y `arccos` no lo acepta: falta `np.clip(..., -1, 1)`."), kind="warn")
        elif np.allclose(_obtenido, np.radians(_esperado)):
            _res = mo.callout(mo.md("❌ devolvés **radianes**. Falta `np.degrees(...)` al final."), kind="warn")
        elif np.allclose(_obtenido, np.degrees(np.arcsin(np.clip(_cos, -1, 1)))):
            _res = mo.callout(mo.md("❌ usaste `arcsin`: el cociente $\\langle v,u\\rangle/(|v||u|)$ es el **coseno** del ángulo (la sombra), no el seno. Va `np.arccos`."), kind="warn")
        else:
            _i = int(np.argmax(~np.isclose(_obtenido, _esperado)))
            _res = mo.callout(mo.md(f"❌ no coincide. Para `v = {np.round(_pares[_i][0], 2).tolist()}`, `u = {np.round(_pares[_i][1], 2).tolist()}` esperaba `{_esperado[_i]:.2f}` y obtuve `{_obtenido[_i]:.2f}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="def proyeccion(v, u):\n    return ...     # el VECTOR sombra de v sobre u (array de 2)\n",
        language="python", min_height=90, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado.** Completá `proyeccion(v, u)`: la **proyección vectorial** de $v$ sobre $u$, el
        vector gold de la sección 2. Pista: es un múltiplo de $u$, y el múltiplo no es la sombra sino la sombra dividida
        por $|u|$. Se verifica con `np.allclose` sobre pares al azar.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _rng = np.random.default_rng(2026)
    _pares = [(_rng.uniform(-5, 5, 2), _rng.uniform(-5, 5, 2)) for _ in range(12)]
    _esperado = np.array([lib.proyeccion(v, u) for v, u in _pares])
    _ns = {"np": np}
    try:
        exec(editor_d.value, _ns)
        _obtenido = np.array([np.asarray(_ns["proyeccion"](v, u), dtype=float).reshape(-1) for v, u in _pares])
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ para un par devolvés algo de forma `{_obtenido.shape[1:]}`; tiene que ser un vector `(2,)`, no la sombra como número."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide en los 12 pares: $\\langle v,u\\rangle / \\langle u,u\\rangle$ por $u$."), kind="success")
        elif np.allclose(_obtenido, [float(v @ u) / np.linalg.norm(u) * u for v, u in _pares]):
            _res = mo.callout(mo.md("❌ dividiste por $|u|$: eso da la sombra (un largo) por $u$ entero, y queda $|u|$ veces más largo. El múltiplo es $\\langle v,u\\rangle / |u|^2 = \\langle v,u\\rangle / \\langle u,u\\rangle$."), kind="warn")
        elif np.allclose(_obtenido, [lib.proyeccion(u, v) for v, u in _pares]):
            _res = mo.callout(mo.md("❌ proyectaste $u$ sobre $v$: el resultado tiene que ser un múltiplo de $u$, el vector sobre el que cae la sombra."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primer par: esperaba `{np.round(_esperado[0], 3).tolist()}`, obtuve `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Dónde está la demostración, y lo que viene

    Acá mostré que una sola cuenta da sombra, largo, distancia y ángulo, y que una rotación la deja igual. Las demostraciones:

    - [apunte, sección 7: rotaciones y lo que conservan](../../apunte.pdf#nameddest=cap:07)
    - [apunte, sección 11: producto interno como incidencia, formas y "fila por columna"](../../apunte.pdf#nameddest=cap:11)
    - [ficha de la clase 1](../../clases/01.html) · [lección anterior: Rotaciones III](../01c_rotaciones_3d/index.html) · [el hilo conductor](../../index.html)

    **Lo que viene:** reflexiones y similaridades (unidad 03): las ortogonales con $\det = -1$ y la escala, que conserva
    ángulos pero no largos. Más adelante, en las superficies, los ejes locales ya no son perpendiculares ni de largo $1$,
    y la métrica $E, F, G$ es justamente la tabla $V V^T$ de sus productos internos.
    """)
    return


@app.cell
def _(A, B, BA, BC, C, G, candidatos, lib, mo, np, p, sombra, theta, u, v, vu):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _R = lib.rot2(np.deg2rad(37))
    _checks = [
        ("los cuatro candidatos de la predicción son distintos entre sí", len({round(x, 6) for x in candidatos.values()}) == 4),
        ("BA = (4, 3), BC = (4, −3), ⟨BC, BA⟩ = 7", lib.exacto(BA, [4, 3]) and lib.exacto(BC, [4, -3]) and lib.exacto(BC @ BA, 7.0)),
        ("sombra 1.4, ángulo en B = arccos(0.28), proyección (1.12, 0.84)",
         lib.exacto(candidatos["correcta"], 1.4) and lib.exacto(lib.angulo(BC, BA), np.arccos(0.28)) and lib.exacto(lib.proyeccion(BC, BA), [1.12, 0.84])),
        ("Pitágoras: sombra² + perpendicular² = |BC|²; ley del coseno: |AC| = 6",
         lib.exacto(candidatos["correcta"] ** 2 + candidatos["seno"] ** 2, 25.0) and lib.exacto((C - A) @ (C - A), BA @ BA + BC @ BC - 2 * (BA @ BC)) and lib.exacto(np.linalg.norm(C - A), 6.0)),
        ("sección 2: ⟨v, u⟩ = |v||u| cos θ y la proyección es paralela a u",
         lib.exacto(vu, np.linalg.norm(v) * np.linalg.norm(u) * np.cos(theta)) and lib.exacto(p, sombra * u / np.linalg.norm(u))),
        ("sección 2: el pie de la perpendicular es perpendicular a u", lib.exacto((v - p) @ u, 0.0, tol=1e-9)),
        ("una rotación conserva ⟨v, u⟩, |v| y θ",
         lib.exacto((_R @ v) @ (_R @ u), vu) and lib.exacto(np.linalg.norm(_R @ v), np.linalg.norm(v)) and lib.exacto(lib.angulo(_R @ v, _R @ u), theta)),
        ("sección 4: G = V Vᵀ = [[25, 7], [7, 25]]", lib.exacto(G, [[25, 7], [7, 25]])),
        ("ejercicio (a): (4, −3) ⊥ (3, 4); sombra de (6, 2) sobre (3, 4) = 5.2", lib.exacto(np.array([4, -3]) @ [3, 4], 0.0) and lib.exacto(np.array([6, 2]) @ [3, 4] / 5, 5.2)),
        ("ejercicio (b): ángulo recto en B y |AC| = √50", lib.exacto(np.array([-3, -4]) @ [4, -3], 0.0) and lib.exacto(np.linalg.norm([7, 1]) ** 2, 50.0)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
