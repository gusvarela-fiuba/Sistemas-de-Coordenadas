# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Proyectivas: la foto del dron y el pentágono del profesor (unidad 05, molde v2 sobre cb104). Clase 03p.

Una sola idea: un punto del plano es un rayo por el origen de R³ y la foto de una cámara inclinada es una 3×3 que
actúa sobre esos rayos; al dividir por la tercera coordenada las rectas siguen rectas pero las paralelas se cortan.
Cuatro puntos fijan la homografía (sistema con un λ por punto, como el profesor, o la forma estándar DLT).

Chequear:  uv run marimo check --select MW unidades/05_proyectivas.py
Exportar:  uv run python tools/build.py --only 05_proyectivas
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
    # Proyectivas: la foto del dron y el pentágono del profesor

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Seguimos la clase extra del 16/9 y 23/9. La pregunta: **¿por qué en la foto los alambrados paralelos se juntan en un
    punto, y con cuántos puntos enderezamos la imagen?** El gancho: *una foto de dron inclinada sobre un lote plano: cuatro
    mojones de coordenadas conocidas la rectifican.* Y el problema del profesor: un pentágono regular, una proyectiva
    que deja dos vértices quietos e intercambia otros dos; ¿dónde cae el quinto?

    Colores, iguales en la figura y en el álgebra: **primera columna** <span style="color:#1b6f6a">**teal**</span>,
    **segunda** <span style="color:#b5451b">**rust**</span>, **tercera** <span style="color:#c9a227">**gold**</span>.
    En una $3\times3$ proyectiva las dos primeras columnas son a dónde van los **puntos impropios** de los ejes (los
    puntos de fuga) y la tercera, a dónde va el origen. El objeto va en <span style="color:#7a4e9e">**violeta**</span>,
    lo de antes en gris, lo de después en teal.
    """)
    return


@app.cell
def _(lib, mo):
    mo.md(lib.bloque_hilo_conductor("05_proyectivas"))
    return


@app.cell
def _(lib, mo, np):
    # ---------- la situación y los números de la predicción salen de acá, nunca a mano ----------
    terr = np.array([[0.0, 0.0], [4.0, 0.0], [4.0, 4.0], [0.0, 4.0]])  # los cuatro mojones en el terreno (decámetros)
    foto = np.array([[0.0, 0.0], [4.0, 0.0], [3.0, 2.0], [1.0, 2.0]])  # los mismos, leídos en la foto
    H_foto = lib.homografia_4puntos(terr, foto)  # terreno → foto
    centro = np.array([2.0, 2.0])
    _c_hom = H_foto @ lib.hom(centro)
    candidatos = {
        "correcta": lib.dehom(_c_hom),
        "sin-dividir": _c_hom[:2].copy(),  # el error típico: olvidarse de dividir por W
        "afin": foto.mean(axis=0),  # el promedio de las cuatro esquinas: lo que haría una afinidad
        "mismas": centro.copy(),
    }
    prediccion = mo.ui.radio(
        options=lib.opciones_barajadas({lib.vec_plano(candidatos[k]): k for k in ("afin", "mismas", "correcta", "sin-dividir")}),
        value=None,
        label=r"**Predicción.** El mojón del centro del lote, $(2, 2)$ en el terreno, aparece en la foto en…",
    )
    mo.vstack([
        mo.md(r"""
        ## 0. Situación de campo y predicción

        Un dron fotografió un lote plano y cuadrado de $40$ m de lado, pero la cámara estaba **inclinada**: en la foto
        el lote es un trapecio, y los alambrados que en el terreno son paralelos se van juntando hacia arriba. Trabajamos
        en decámetros para que la grilla se lea: las esquinas están en el terreno en $(0,0)$, $(4,0)$, $(4,4)$, $(0,4)$
        y en la foto las leemos en $(0,0)$, $(4,0)$, $(3,2)$, $(1,2)$.

        Hay un quinto mojón, en el centro del lote, $(2, 2)$. En la unidad 04 una afinidad mandaba el punto medio al
        punto medio. Acá la cámara **no** hace una afinidad: lo que sigue valiendo es que las rectas van a rectas, así
        que el centro, que está sobre las dos diagonales, tiene que caer **donde se cruzan las diagonales de la foto**.
        """),
        prediccion,
    ])
    return H_foto, candidatos, centro, foto, prediccion, terr


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success", r"**Sí.** $(2, 1.333)$ es el cruce de las diagonales de la foto, $y = \tfrac{2}{3}x$ con $y = -\tfrac{2}{3}(x - 4)$. "
                     r"El centro quedó **más arriba que la mitad** de la altura del trapecio, hacia el lado lejano: la mitad lejana del lote "
                     r"se achica en la foto y ocupa menos alto, así que el centro sube. En la sección 3 sale de la cuenta $H\,(2, 2, 1)^T = (3, 2, 1.5)^T$ y la división por $1.5$."),
        "sin-dividir": ("warn", r"**No.** $(3, 2)$ son las dos primeras coordenadas de $H\,(2, 2, 1)^T = (3, 2, 1.5)^T$ **sin dividir por la "
                        r"tercera**. En homogéneas el punto es el rayo entero: hay que volver al plano $W = 1$ dividiendo por $1.5$, y queda $(2, 1.333)$."),
        "afin": ("warn", r"**No.** $(2, 1)$ es el promedio de las cuatro esquinas de la foto, lo que haría una **afinidad** (punto medio al punto "
                 r"medio). Pero una afinidad conserva paralelas, y en la foto los lados $x = 0$ y $x = 4$ ya no lo son: no está sobre las diagonales."),
        "mismas": ("warn", r"**No.** $(2, 2)$ es el centro en el **terreno**. Preguntamos dónde aparece en la **foto**, donde las esquinas de arriba ya "
                   r"se corrieron a $(1, 2)$ y $(3, 2)$: cambió la imagen, no el lote."),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** Una proyectiva lleva **rectas a rectas** y conserva la **incidencia** (si tres puntos estaban
    alineados, siguen alineados; si dos rectas se cortaban en un punto, sus imágenes se cortan en la imagen del punto).
    Nada más: no las paralelas, no las razones sobre una recta (el punto medio deja de ser el medio), no los ángulos. Lo
    único métrico que sobrevive es la **razón doble** de cuatro puntos alineados.

    **El punto como rayo.** El plano de dibujo es el plano $W = 1$ dentro de $\mathbb R^3$; el punto $(x, y)$ es la terna
    $(x, y, 1)$ y también cualquier múltiplo $(\lambda x, \lambda y, \lambda)$: **el rayo** que sale del origen y lo
    atraviesa. Una cámara hace exactamente eso: todos los puntos de un mismo rayo caen en el mismo lugar de la foto.
    Una matriz $3\times3$ invertible manda rayos a rayos, y leyendo cada rayo donde corta a $W = 1$ queda la
    **homografía** $p' \sim Hp$, con la división por $W = h_{31}x + h_{32}y + h_{33}$.

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $t \mapsto \dfrac{at + b}{ct + d}$; la recta más un punto, $(t, 1) \sim (1, 0)$ | una regla fotografiada de costado: los centímetros se achican hacia el fondo; el punto $t = -d/c$ se va al infinito |
    | $\mathbb R^2$ | $p' \sim Hp$, $H$ de $3\times3$; ternas $(x, y, W)$ a menos de escala | la foto del lote: rectas siguen rectas, las paralelas convergen a un **punto de fuga**; cuatro puntos fijan $H$ |
    | $\mathbb R^3$ | rayos por el origen de $\mathbb R^3$: cada punto del plano es uno; $(a, b, 0)$ es un rayo **paralelo** al plano | el **punto impropio** de la dirección $(a, b)$: donde se juntan todas las paralelas de esa dirección |

    **La fila 3 es la recta que se va al infinito.** Los puntos con $W = 0$ no tienen imagen en el plano: es la recta
    $h_{31}x + h_{32}y + h_{33} = 0$. Si $h_{31} = h_{32} = 0$ ningún punto propio se va, $W$ vale siempre lo mismo y la
    transformación es **afín** (la unidad 04). Si la recta atraviesa la figura, la imagen **se parte**: un lado que la
    cruza se vuelve dos semirrectas unidas por el infinito. Nueve números menos la escala son **8 grados de libertad**,
    dos por cada par punto–imagen: **cuatro puntos**, sin tres alineados, la fijan. Esto es una **muestra**; la
    demostración está en el apunte, secciones 5 y 12.
    """)
    return


@app.cell
def _(lib, mo, np):
    # ---------- figura chica y estática: el punto como rayo por el origen de R³ ----------
    _p = np.array([1.5, 1.0, 1.0])  # el punto (1.5, 1) del plano W = 1
    _d = np.array([1.0, 0.5, 0.0])  # un rayo paralelo al plano: el punto impropio de la dirección (1, 0.5)
    fig_rayos = lib.figura_espacio((-0.5, 3.2), "el plano W = 1 y dos rayos: uno lo corta, el otro es paralelo", ancho=520, alto=460)
    lib.plano_3d(fig_rayos, [1, 0, 0], [0, 1, 0], k=1.6, origen=[1.3, 1.3, 1.0], color=lib.GRIS_ANTES, nombre="plano W = 1")
    lib.flecha_3d(fig_rayos, [0, 0, 0], 2.0 * _p, lib.VIOLETA_OBJETO, "rayo de (1.5, 1): cualquier λ(1.5, 1, 1)")
    lib.flecha_3d(fig_rayos, [0, 0, 0], 2.5 * _d, lib.COLORES[1], "rayo (1, 0.5, 0): nunca llega al plano", ancho=5)
    fig_rayos.add_trace(dict(type="scatter3d", x=[_p[0]], y=[_p[1]], z=[_p[2]], mode="markers+text", text=["(1.5, 1, 1)"],
                             marker=dict(size=6, color=lib.VIOLETA_OBJETO), name="donde corta a W = 1"))
    mo.hstack([
        mo.md(r"""
        **Lo que muestra la figura.** El rayo violeta corta al plano gris en $(1.5, 1, 1)$: ese corte es el punto
        $(1.5, 1)$, y $(3, 2, 2)$ es **el mismo punto**. El rayo rust, $(1, 0.5, 0)$, corre paralelo al plano y no lo
        corta nunca: es el punto impropio de la dirección $(1, 0.5)$, donde se encuentran todas las rectas paralelas a
        ella. Una $3\times3$ puede girar un rayo paralelo hasta que corte al plano (un punto de fuga aparece en la
        foto) y, al revés, mandar un rayo que cortaba a uno paralelo (una recta propia se va al infinito).
        """),
        mo.ui.plotly(fig_rayos),
    ], widths=[1, 2], align="start")
    return


@app.cell
def _(lib, mo):
    mo.Html(lib.video_loop("02_homogeneas_pentagono_3d", "Vemos el pentágono como cinco rayos que salen del origen y cortan la lámina z = 1: H(s) mueve los rayos, el pentágono se deforma proyectivamente y a la vuelta recupera su forma."))
    return


@app.cell
def _(H_foto, lib, mo, np):
    # ---------- casos precargados: etiqueta → (tipo, dato, objeto, rango, paso, qué pasa) ----------
    pent = lib.pentagono_profesor()  # A..E, D = (0, 1), horario
    H_pent, lam_pent = lib.homografia_lambda(pent[[0, 1, 2, 4]], pent[[0, 1, 4, 2]])  # A, B fijos; C ↔ E
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # la misma de Rotaciones II
    H_afin = H_foto.copy()
    H_afin[2] = [0.0, 0.0, 1.0]
    casos = {
        "identidad": ("fijo", np.eye(3), parcela, 6, 1, r"no cambia nada: $W = 1$ en todo el plano."),
        "afinidad: la misma A, última fila (0 0 1)": ("fijo", H_afin, parcela, 6, 1,
                                                     r"el corte de la foto sin la fila 3: las paralelas **siguen paralelas**, las columnas 1 y 2 siguen impropias (flechas)."),
        "foto de dron: cámara inclinada (k)": ("inclinacion", (-0.4, 0.4, 0.05, 0.25), parcela, 6, 1,
                                              r"$h_{32} = k$: las rectas $x = $ cte convergen al punto de fuga (columna 2, ×); con $k = 0.25$ es la foto de la sección 0. Con $k < 0$ la recta $y = -1/k$ atraviesa la parcela y la imagen **se parte**."),
        "pentágono del profesor: A y B fijos, C ↔ E": ("fijo", H_pent, pent, 2, 0.5,
                                                      r"$D$ **cae en el centro** $(0, 0)$. $W$ es negativa en $A$ y $B$ y positiva en $C$, $D$, $E$: la recta $4y + 1 = 0$ cruza el pentágono y la imagen se parte. Es una homología armónica: eje $AB$, centro $(0, 0.309)$, $H^2 \sim I$."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="foto de dron: cámara inclinada (k)", label="caso precargado")
    mo.md(r"""
    ## 2. Manipulación

    Tres capas: **gris**, grilla y cuadrado unitario antes; **teal**, los mismos después (la grilla sigue hecha de
    rectas, pero ya no paralelas), con las columnas de $H$ leídas como puntos: × teal y rust son los **puntos de
    fuga** de las rectas $y = $ cte y $x = $ cte (si siguen impropios, una flecha con la dirección), el punto gold es
    la imagen del origen; **violeta**, el objeto con estelas. Con el caso del dron manda el deslizador $k$;
    **reproducir** muestra el camino desde la identidad (en el pentágono, pasando por el espejo). A la derecha de la
    figura, el panel con el caso, el deslizador y los números vivos.
    """)
    return H_pent, caso, casos, lam_pent, parcela, pent


@app.cell
def _(caso, casos, mo):
    _tipo, _dato, _, _, _, _ = casos[caso.value]
    inclina = _tipo == "inclinacion"
    _lo, _hi, _paso, _val = _dato if inclina else (0, 1, 1, 0)
    k_incl = mo.ui.slider(_lo, _hi, value=_val, step=_paso, label="k (inclinación, h₃₂)", show_value=True, disabled=not inclina)
    return inclina, k_incl


@app.cell
def _(caso, casos, go, inclina, k_incl, lib, mo, np):
    _tipo, _dato, objeto, rango, paso, que_pasa = casos[caso.value]
    if inclina:
        def _H_de(k):
            return np.array([[1.0, 0.5, 0.0], [0.0, 1.0, 0.0], [0.0, k, 1.0]])
        H = _H_de(k_incl.value)
        camino = [_H_de(s * k_incl.value) for s in np.linspace(0, 1, 36)]
    else:
        H = np.asarray(_dato, dtype=float)
        _reales = lib.autovalores_reales(H)
        lam_p = max(_reales, key=lambda z: (round(abs(z), 6), z))  # el real de mayor módulo; en empate, el positivo
        camino = [(1 - s) * np.eye(3) + s * H / lam_p for s in np.linspace(0, 1, 36)]
    limite = 3.0 * rango

    def _dinamicas(i):
        f = go.Figure()
        lib.capa_despues_proyectiva(f, camino[i], rango, paso)
        ex, ey = lib.estelas_proyectivas(objeto, camino[: i + 1], limite)
        f.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=1.5, dash="dot"),
                               name="estelas", hoverinfo="skip"))
        cx, cy = lib.curva_proyectiva(objeto, camino[i], limite=limite)
        f.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=lib.VIOLETA_OBJETO, width=2.5), name="objeto después"))
        _v = lib.aplicar_proyectiva(objeto, camino[i])
        _ok = np.isfinite(_v).all(axis=1) & (np.abs(_v).max(axis=1) <= limite)
        f.add_trace(go.Scatter(x=_v[_ok, 0], y=_v[_ok, 1], mode="markers+text", text=[c for c, o in zip("ABCDE", _ok) if o],
                               textposition="top right", marker=dict(size=7, color=lib.VIOLETA_OBJETO), name="vértices después"))
        return list(f.data)

    figura = lib.figura_plano(rango + 1 if rango > 2 else 3, caso.value)
    lib.capa_antes(figura, rango, paso)
    lib.objeto(figura, objeto, lib.GRIS_ANTES, "objeto antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    W = lib.hom(objeto) @ H[2]
    _l = lib.recta_al_infinito(H)
    _texto_inf = (r"ninguna: $h_{31} = h_{32} = 0$, es afín" if abs(_l[0]) + abs(_l[1]) < 1e-9
                  else rf"${lib.num_tex(_l[0], 2)}\,x + {lib.num_tex(_l[1], 2)}\,y + {lib.num_tex(_l[2], 2)} = 0$")
    _fijos = []
    for _p in lib.puntos_fijos_proyectivos(H):
        _lam, _r = rf"$\lambda = {lib.num_tex(_p['lam'], 3)}$: ", _p["recta"]
        if _p["plano"]:
            _fijos.append(_lam + ("**todo el plano** (identidad)" if _r is None else
                                  rf"**recta de puntos fijos** ${lib.num_tex(_r[0], 2)}\,x + {lib.num_tex(_r[1], 2)}\,y + {lib.num_tex(_r[2], 3)} = 0$"))
        elif _p["punto"] is None:
            _fijos.append(_lam + rf"dirección fija ${lib.vec_tex(_p['v'][:2], 2)}$ (punto impropio)")
        else:
            _fijos.append(_lam + rf"punto fijo ${lib.vec_tex(_p['punto'], 3)}$")
    _panel = mo.vstack([
        mo.md("**Controles**"), caso, k_incl,
        mo.md(rf"""
        **Números vivos**

        $$H = {lib.matriz_coloreada(H)}$$

        - recta que se va al infinito (fila 3): {_texto_inf}
        - $W$ de cada vértice: ${", ".join(lib.num_tex(w, 2) for w in W)}$ {"— **cambia de signo: la imagen se parte**" if W.min() < 0 < W.max() else ""}
        - fijos: {"; ".join(_fijos) if _fijos else "ninguno real"}

        **Qué pasa acá:** {que_pasa}
        """),
    ], gap=0.55)
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return H, W, objeto


@app.cell
def _(H_pent, lam_pent, lib, mo, np, pent):
    _o, _d = pent[[0, 1, 2, 4]], pent[[0, 1, 4, 2]]
    _M, _b = lib.sistema_lambda(_o, _d)
    _x = np.linalg.solve(_M, _b)
    _HD = H_pent @ lib.hom(pent[3])
    mo.vstack([
        mo.md(r"""
        ## 3. Cuenta a mano y código lado a lado

        Izquierda, la cuenta del cuaderno; derecha, la misma en numpy. Primero el pentágono como lo hizo el profesor en
        su planilla, después la foto del dron con la forma estándar.
        """),
        mo.hstack([
            mo.md(r"""
            **3.1 Un $\lambda$ por punto (la planilla del profesor).** Pentágono regular centrado, $D = (0, 1)$ y los
            demás vértices por giros de $72°$: $A = (0.588, -0.809)$, $B = (-0.588, -0.809)$, $C = (-0.951, 0.309)$,
            $E = (0.951, 0.309)$. Queremos $H$ con $A$ y $B$ fijos y $C \leftrightarrow E$. Como $Hp$ es el punto **a
            menos de escala**, cada par da tres ecuaciones con una incógnita más:

            $$H\begin{pmatrix} a_x \\ a_y \\ 1 \end{pmatrix} = \lambda_A \begin{pmatrix} a_x \\ a_y \\ 1 \end{pmatrix},\quad
            H\,\vec B = \lambda_B \vec B,\quad H\,\vec C = \lambda_C \vec E,\quad H\,\vec E = \lambda_E \vec C .$$

            Doce ecuaciones, nueve $h_{ij}$ y cuatro $\lambda$: trece incógnitas; la decimotercera ecuación fija la
            escala, $h_{33} = 1$. Se resuelve con la inversa (o `solve`) y queda

            $$H = \begin{pmatrix} \textcolor{#1b6f6a}{-\sqrt5} & \textcolor{#b5451b}{0} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{-1} & \textcolor{#c9a227}{1} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{4} & \textcolor{#c9a227}{1} \end{pmatrix},\qquad
            \lambda = (-\sqrt5,\ -\sqrt5,\ \sqrt5,\ \sqrt5).$$

            Control: $H\vec A = (-\sqrt5\,a_x,\ -a_y + 1,\ 4a_y + 1) = (-1.314,\ 1.809,\ -2.236) = -\sqrt5\,\vec A$ ✓.
            El quinto: $H\vec D = (0,\ -1 + 1,\ 4 + 1) = (0, 0, 5)$, o sea $D' = (0, 0)$: **el centro**. Los $\lambda$
            negativos de $A$ y $B$ dicen que la recta $4y + 1 = 0$ pasa entre $AB$ y $CE$: la imagen se parte.
            """),
            mo.vstack([
                mo.md("```python\nP = lib.pentagono_profesor()        # A..E\no, d = P[[0, 1, 2, 4]], P[[0, 1, 4, 2]]\nM, b = lib.sistema_lambda(o, d)     # 13×13\nx = np.linalg.solve(M, b)\nH, lam = x[:9].reshape(3, 3), x[9:]\nH @ lib.hom(P[3])                   # D\n```"),
                mo.md(f"`M.shape` = `{_M.shape}` → `H` =\n```\n{np.round(_x[:9].reshape(3, 3), 3)}\n```\n`lam` = `{np.round(_x[9:], 3).tolist()}`  \n"
                      f"`H @ hom(D)` = `{np.round(_HD, 3).tolist()}` → `{np.round(lib.dehom(_HD), 3).tolist()}`  \n"
                      f"`lib.homografia_lambda(o, d)` da lo mismo: `{bool(np.allclose(_x[:9].reshape(3, 3), H_pent) and np.allclose(_x[9:], lam_pent))}`"),
            ]),
        ], widths="equal", align="start"),
    ])
    return


@app.cell
def _(H_foto, foto, lib, mo, np, terr):
    _A, _b = [], []
    for (_x, _y), (_u, _v) in zip(terr, foto):
        _A.append([_x, _y, 1, 0, 0, 0, -_u * _x, -_u * _y])
        _b.append(_u)
        _A.append([0, 0, 0, _x, _y, 1, -_v * _x, -_v * _y])
        _b.append(_v)
    _h = np.linalg.solve(np.array(_A), _b)
    H8 = np.append(_h, 1.0).reshape(3, 3)
    H_rect = np.linalg.inv(H_foto)
    H_rect = H_rect / H_rect[2, 2]
    mo.hstack([
        mo.md(r"""
        **3.2 La forma estándar (DLT) con la foto del dron.** Cada par $(x, y) \mapsto (u, v)$ dice $u = \dfrac{h_{11}x + h_{12}y + h_{13}}{h_{31}x + h_{32}y + h_{33}}$ y lo mismo
        para $v$; multiplicando por el denominador quedan **dos ecuaciones lineales** en los $h_{ij}$ por punto. Con
        $h_{33} = 1$ son ocho ecuaciones y ocho incógnitas.

        A mano, con las cuatro esquinas: $(0,0) \mapsto (0,0)$ da $h_{13} = h_{23} = 0$. $(4,0) \mapsto (4,0)$ da
        $h_{21} = 0$ y $h_{11} = 1 + 4h_{31}$. $(0,4) \mapsto (1,2)$: $4h_{12} = 1 + 4h_{32}$ y $4h_{22} = 2(1 + 4h_{32})$.
        $(4,4) \mapsto (3,2)$: $4h_{22} = 2(1 + 4h_{31} + 4h_{32})$, que con la anterior da $h_{31} = 0$, luego $h_{11} = 1$,
        y $4 + 4h_{12} = 3(1 + 4h_{32})$ da $h_{32} = \tfrac14$, $h_{12} = \tfrac12$, $h_{22} = 1$:

        $$H = \begin{pmatrix} \textcolor{#1b6f6a}{1} & \textcolor{#b5451b}{0.5} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{1} & \textcolor{#c9a227}{0} \\ \textcolor{#1b6f6a}{0} & \textcolor{#b5451b}{0.25} & \textcolor{#c9a227}{1} \end{pmatrix}.$$

        Fila 3: la recta $0.25y + 1 = 0$, $y = -4$, se va al infinito: está abajo del lote, la foto sale entera.
        Columna 2: el punto impropio de las rectas $x = $ cte va a $(0.5, 1, 0.25) \sim (2, 4)$, el punto de fuga.
        **Rectificar** es aplicar $H^{-1}$ a lo que leemos en la foto.
        """),
        mo.vstack([
            mo.md("```python\nA, b = [], []\nfor (x, y), (u, v) in zip(terr, foto):\n    A.append([x, y, 1, 0, 0, 0, -u*x, -u*y])\n    b.append(u)\n    A.append([0, 0, 0, x, y, 1, -v*x, -v*y])\n    b.append(v)\nh = np.linalg.solve(np.array(A), b)   # 8×8\nH = np.append(h, 1).reshape(3, 3)\nlib.homografia_4puntos(terr, foto)   # 8×9\nnp.linalg.inv(H)                      # rectifica\n```"),
            mo.md(f"`H` =\n```\n{np.round(H8, 3)}\n```\n`lib.homografia_4puntos` coincide: `{bool(np.allclose(H8, H_foto))}`  \n"
                  f"`inv(H)` (con $h_{{33}} = 1$) =\n```\n{np.round(H_rect, 3)}\n```"),
        ]),
    ], widths="equal", align="start")
    return H8, H_rect


@app.cell
def _(H_foto, lib, mo, np, terr):
    _P = lib.hom(terr)
    _Q = _P @ H_foto.T
    _res = _Q[:, :2] / _Q[:, 2:3]
    _terr5 = np.vstack([terr, [[2.0, 2.0]]])
    _foto5 = lib.aplicar_proyectiva(_terr5, H_foto)
    _H5 = lib.homografia_4puntos(_terr5, _foto5)
    mo.vstack([
        mo.md(r"""
        ## 4. Python de hoy

        Una sola idea: **aplicar una homografía a una nube es `hom(puntos) @ H.T` y después dividir cada fila por su
        tercera columna**, `Q[:, :2] / Q[:, 2:3]` (el `2:3` conserva la forma `(N, 1)` para que la división se
        reparta fila a fila). Es `lib.aplicar_proyectiva`. Para hallar $H$: `np.linalg.solve` cuando el sistema es
        cuadrado (el $8\times8$ con $h_{33} = 1$ o el $13\times13$ del profesor); con **más de cuatro mojones** el sistema
        tiene más ecuaciones que incógnitas y va `np.linalg.lstsq(A, b, rcond=None)[0]`, que es lo que hace
        `lib.homografia_4puntos` por la SVD cuando le pasamos $N > 4$ pares.
        """),
        mo.md("```python\nP = lib.hom(terr)                 # (4, 3): una terna por mojón\nQ = P @ H.T                       # (4, 3): x, y, W\nQ[:, :2] / Q[:, 2:3]              # (4, 2): dividir por W\nlib.aplicar_proyectiva(terr, H)   # lo mismo\nlib.homografia_4puntos(terr5, foto5)   # 5 pares: 10×9, mínimos cuadrados\n```"),
        mo.md(f"`P.shape` = `{_P.shape}`, `Q.shape` = `{_Q.shape}` → resultado:\n```\n{np.round(_res, 3)}\n```\n"
              f"Las cuatro esquinas de la foto. Con cinco pares (las esquinas y el centro) la $H$ de mínimos cuadrados coincide: "
              f"`{bool(np.allclose(_H5, H_foto))}`."),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        ## 5. Ejercicios

        **(a) Lápiz — elemental** *("mantienen rectas las rectas").* Con la $H$ de la foto, calculá a dónde van los dos
        puntos impropios $(1, 0, 0)$ y $(0, 1, 0)$. ¿Qué pasa en la foto con los alambrados paralelos al eje $x$? ¿Y con
        los paralelos al eje $y$? ¿Dónde se cruzan estos últimos?
        """),
        mo.accordion({"Ver respuesta (a)": mo.md(r"""
        $H(1, 0, 0)^T = (1, 0, 0)^T$: la columna 1; sigue impropio, así que las rectas $y = $ cte siguen **paralelas** en la
        foto (la cámara se inclinó sólo hacia adelante). $H(0, 1, 0)^T = (0.5, 1, 0.25)^T \sim (2, 4)$: la columna 2, un
        punto propio. Todas las rectas $x = $ cte, que en el terreno son paralelas, en la foto **se cruzan en $(2, 4)$**: el
        punto de fuga. Está arriba del lote, por eso el trapecio se angosta hacia arriba.
        """)}),
        mo.md(r"""
        **(b) Lápiz — medio** *("¿dónde cae el vértice restante? ¿tiene punto fijo?").* Con la $H$ del pentágono del
        profesor, verificá que $B$ queda fijo, calculá $H^2$ y decí qué significa. Sobre la recta $x = 0$ están $D = (0, 1)$,
        su imagen $D' = (0, 0)$, el centro $O = (0, 0.309)$ y el corte con el eje $AB$, $X = (0, -0.809)$: calculá la razón
        doble $(D, D'; O, X)$ con la coordenada $y$.
        """),
        mo.accordion({"Ver respuesta (b)": mo.md(r"""
        $H\vec B = (-\sqrt5 \cdot (-0.588),\ 0.809 + 1,\ 4 \cdot (-0.809) + 1) = (1.314,\ 1.809,\ -2.236) = -\sqrt5\,\vec B$: fijo ✓.
        $H^2 = \begin{pmatrix} 5 & 0 & 0 \\ 0 & 1 + 4 & -1 + 1 \\ 0 & -4 + 4 & 4 + 1 \end{pmatrix} = 5I$: aplicarla dos veces
        es la identidad, un **espejo proyectivo** (homología armónica) con eje $AB$ y centro $O$. Razón doble:
        $\dfrac{(0.309 - 1)(-0.809 - 0)}{(0.309 - 0)(-0.809 - 1)} = \dfrac{0.559}{-0.559} = -1$: cuaterna armónica, el
        centro es el conjugado armónico del corte con el eje respecto de $D$ y $D'$. El punto medio entre $O$ y $X$,
        $y = -0.25$, es justo la recta que se va al infinito.
        """)}),
    ])
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def aplicar(H, puntos):\n    P = hom(puntos)     # (N, 3)\n    Q = ...             # (N, 3): x, y, W\n    return ...          # (N, 2): dividir por W\n",
        language="python", min_height=120, label="ejercicio (c)",
    )
    mo.vstack([
        mo.md(r"""
        **(c) Código con hueco — medio** *("se normaliza dividiendo por la tercera coordenada").* Completá
        `aplicar(H, puntos)`: aplica la homografía `H` a una nube $N\times2$ y devuelve la nube $N\times2$ de las
        imágenes, ya divididas por $W$. Tenés `np` y `hom`. Se verifica con `np.allclose` sobre 20 puntos al azar con la
        $H$ de la foto.
        """),
        editor_c,
    ])
    return (editor_c,)


@app.cell
def _(H_foto, editor_c, lib, mo, np):
    _puntos = np.random.default_rng(56798).uniform(0, 4, size=(20, 2))
    _esperado = lib.aplicar_proyectiva(_puntos, H_foto)
    _ns = {"np": np, "hom": lib.hom}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.asarray(_ns["aplicar"](H_foto, _puntos), dtype=float)
        if _obtenido.shape == (20, 3):
            _res = mo.callout(mo.md("❌ devolviste la nube homogénea `(20, 3)`: falta dividir por la tercera columna y quedarte con las dos primeras."), kind="danger")
        elif _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ la forma es `{_obtenido.shape}`; tiene que ser `{_esperado.shape}` (una fila por punto)."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide con la referencia en los 20 puntos."), kind="success")
        elif np.allclose(_obtenido, (lib.hom(_puntos) @ H_foto.T)[:, :2]):
            _res = mo.callout(mo.md(r"❌ te quedaste con $x, y$ sin dividir por $W$: eso es el rayo, no el punto del plano $W = 1$."), kind="warn")
        elif np.allclose(_obtenido, lib.dehom(lib.hom(_puntos) @ H_foto)):
            _res = mo.callout(mo.md(r"❌ usaste `P @ H` en vez de `P @ H.T`: con los puntos como filas hay que transponer $H$."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primer punto: esperado `{np.round(_esperado[0], 3).tolist()}`, obtenido `{np.round(_obtenido[0], 3).tolist()}`."), kind="danger")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="# foto4: 4×2 (mojones en la foto), terr4: 4×2 (los mismos en el terreno), foto5: el pozo, en la foto\nH = ...          # 3×3 de la foto AL terreno (homografia_4puntos)\npozo = ...       # el pozo en el terreno, (2,)\n",
        language="python", min_height=110, label="ejercicio (d)",
    )
    mo.vstack([
        mo.md(r"""
        **(d) Código con hueco — avanzado: rectificar la foto** *("cuatro mojones de coordenadas conocidas la
        rectifican").* Cuatro mojones tienen coordenadas conocidas en el terreno, `terr4`, y los leemos en la foto, `foto4`.
        Un pozo sólo lo tenemos en la foto, `foto5`. Hallá la homografía **de la foto al terreno** y ubicá el pozo. Tenés
        `np`, `hom`, `dehom`, `homografia_4puntos(origen, destino)`, `aplicar_proyectiva(nube, H)` y los tres arrays.
        """),
        editor_d,
    ])
    return (editor_d,)


@app.cell
def _(H_foto, editor_d, foto, lib, mo, np, terr):
    pozo_terr = np.array([3.0, 1.0])
    foto5 = lib.aplicar_proyectiva(pozo_terr[None, :], H_foto)[0]  # (2.8, 0.8)
    H_ft = lib.homografia_4puntos(foto, terr)
    _ns = {"np": np, "hom": lib.hom, "dehom": lib.dehom, "homografia_4puntos": lib.homografia_4puntos,
           "aplicar_proyectiva": lib.aplicar_proyectiva, "foto4": foto.copy(), "terr4": terr.copy(), "foto5": foto5.copy()}
    try:
        exec(editor_d.value, _ns)
        _p = np.asarray(_ns["pozo"], dtype=float).reshape(-1)
        if _p.shape == (3,):
            _res = mo.callout(mo.md("❌ `pozo` tiene tres coordenadas: es la terna homogénea, falta `dehom` (dividir por $W$)."), kind="danger")
        elif _p.shape != (2,):
            _res = mo.callout(mo.md(f"❌ `pozo` tiene forma `{np.shape(_ns['pozo'])}`; tiene que ser un punto `(2,)`."), kind="danger")
        elif np.allclose(_p, pozo_terr):
            _res = mo.callout(mo.md(rf"✅ el pozo está en ${lib.vec_tex(pozo_terr)}$ del terreno (a $30$ m del lado oeste y $10$ m del sur). "
                                    rf"Rectificación: $H^{{-1}} = {lib.pmat(H_ft)}$."), kind="success")
        elif np.allclose(_p, lib.aplicar_proyectiva(foto5[None, :], H_foto)[0]):
            _res = mo.callout(mo.md("❌ armaste la homografía al revés (del terreno a la foto). `homografia_4puntos(foto4, terr4)` va de la foto al terreno."), kind="warn")
        elif np.allclose(_p, (H_ft @ lib.hom(foto5))[:2]):
            _res = mo.callout(mo.md(r"❌ te faltó dividir por $W$: $(x, y, W)$ es el rayo; el punto es $(x/W, y/W)$."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide: obtuviste `{np.round(_p, 3).tolist()}`. Verificá que `aplicar_proyectiva(foto4, H)` devuelva `terr4`."), kind="danger")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return H_ft, foto5, pozo_terr


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
    preguntas_tanda, respuestas_radio = lib.preparar_autoevaluacion(mo, "05_proyectivas")
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

    Acá verificamos; las demostraciones (por qué un rayo es un punto, por qué cuatro puntos alcanzan y tres no, la
    clasificación por autovalores, el pentágono regular con los tres casos y la tabla de verificación):

    - [apunte, «Proyectivas» (homogéneas y proyectivas)](../../apunte.pdf#nameddest=cap:07) ·
      [apunte, «Pentágono regular: cuentas y script» (el pentágono)](../../apunte.pdf#nameddest=cap:18)
    - [ficha de la clase 03p](../../clases/03p.html) · [el hilo conductor](../../index.html) ·
      [unidad 04: afinidades y homogéneas](../04_afines_homogeneas/index.html) (el caso $W = 1$)

    **Lo que viene:** [Formas lineales y dualidad](../06_formas_lineales/index.html): las rectas $\ell^T p = 0$ son
    formas lineales y se transforman al revés que los puntos, $\ell' \sim H^{-T}\ell$; es lo que hace falta para las
    rectas fijas, que acá aparecieron como el eje de la homología.
    """)
    return


@app.cell
def _(H, H8, H_foto, H_ft, H_pent, H_rect, W, candidatos, centro, foto, foto5, lam_pent, lib, mo, np, objeto, pent, pozo_terr, terr):
    # ---------- verificación silenciosa de las cuentas de la lección ----------
    _r5 = np.sqrt(5.0)
    _checks = [
        ("sección 0: candidatos distintos; H de la foto = [[1, 0.5, 0], [0, 1, 0], [0, 0.25, 1]]; el centro cae en (2, 4/3) = cruce de las diagonales",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == 4 and lib.exacto(H_foto, [[1, 0.5, 0], [0, 1, 0], [0, 0.25, 1]])
         and lib.exacto(candidatos["correcta"], [2, 4 / 3]) and lib.exacto(H_foto @ lib.hom(centro), [3, 2, 1.5])
         and lib.exacto(lib.aplicar_proyectiva(terr, H_foto), foto)),
        ("sección 2: W de cada vértice es la fila 3 por el punto; el pentágono del profesor: A, B fijos, C ↔ E, D al centro, λ = (−√5, −√5, √5, √5)",
         lib.exacto(W, lib.hom(objeto) @ lib.recta_al_infinito(H))
         and lib.exacto(H_pent, [[-_r5, 0, 0], [0, -1, 1], [0, 4, 1]]) and lib.exacto(lam_pent, [-_r5, -_r5, _r5, _r5])
         and lib.exacto(lib.aplicar_proyectiva(pent, H_pent), np.vstack([pent[[0, 1, 4]], [[0, 0]], pent[[2]]]))),
        ("sección 3: el 13×13 y el 8×8 coinciden con homografia_4puntos; H D = (0, 0, 5); H⁻¹ H = I; H² = 5 I",
         lib.exacto(H8, H_foto) and lib.exacto(H_pent @ lib.hom(pent[3]), [0, 0, 5]) and lib.exacto(H_rect @ H_foto, np.eye(3))
         and lib.exacto(H_pent @ H_pent, 5 * np.eye(3)) and lib.exacto(lib.recta_al_infinito(H_pent), [0, 4, 1])),
        ("ejercicio (a): (1, 0, 0) sigue impropio; (0, 1, 0) va a (2, 4)",
         lib.dehom(H_foto @ [1, 0, 0]) is None and lib.exacto(lib.dehom(H_foto @ [0, 1, 0]), [2, 4])),
        ("ejercicio (b): B fijo; razón doble (D, D'; O, X) = −1; el centro (0, 0.309) y el eje AB son los fijos",
         lib.exacto(H_pent @ lib.hom(pent[1]), -_r5 * lib.hom(pent[1])) and lib.exacto(lib.razon_doble(1.0, 0.0, 1 / (1 + _r5), pent[0, 1]), -1.0)
         and lib.exacto(lib.puntos_fijos_proyectivos(H_pent)[0]["punto"], [0, 1 / (1 + _r5)], tol=1e-5) and lib.puntos_fijos_proyectivos(H_pent)[1]["plano"]),
        ("ejercicio (d): la rectificación es H⁻¹ y ubica el pozo (2.8, 0.8) de la foto en (3, 1) del terreno",
         lib.exacto(H_ft @ H_foto, np.eye(3)) and lib.exacto(foto5, [2.8, 0.8]) and lib.exacto(lib.aplicar_proyectiva(foto5[None, :], H_ft)[0], pozo_terr)),
    ]
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
