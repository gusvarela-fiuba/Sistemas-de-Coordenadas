# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Unidad 01 — Rotaciones (piloto del molde de unidad).

Sistemas de Coordenadas (CB104) · Agrimensura · FIUBA · 2C2026
Alumno: Gustavo Varela (padrón 56798). Profesor: Javier Clavijo.

Molde (cinco secciones, en este orden):
  1. Hecho geométrico        — la pregunta "¿qué se conserva?" antes que la fórmula.
  2. Manipulación            — figura de tres capas (grilla gris / grilla teal / parcela) en 2D y 3D.
  3. Cuenta a mano y código  — LaTeX a la izquierda, numpy a la derecha, mismas cuentas.
  4. Python de hoy           — una sola idea nueva: nube = array N×2, transformar = nube @ R.T.
  5. Ejercicios              — dos de lápiz, dos de código con hueco, con nivel de la rúbrica.
Cierre: enlaces del mapa + asserts silenciosos.

Convenciones: grados en la interfaz, radianes adentro; rotación activa por default; sólo numpy y plotly
(los dos están en Pyodide, así que el export `marimo export html-wasm` corre en el navegador sin servidor).

Probar local:   uv run marimo run unidades/01_rotaciones.py
Chequear:       uv run marimo check unidades/01_rotaciones.py
Exportar:       uv run tools/build.py --only 01_rotaciones
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


@app.cell
def _(mo):
    mo.md(r"""
    # Unidad 01 — Rotaciones

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    Esta unidad sigue la clase 1 (rotaciones en el plano, complejos, matrices ortogonales, rotaciones en 3D) y el comienzo
    de la clase 2 (el orden de las rotaciones). Tiene cinco partes, siempre las mismas en todas las unidades:
    **1. el hecho geométrico · 2. manipulación · 3. cuenta a mano y código lado a lado · 4. el Python de hoy · 5. ejercicios.**

    Convenciones: ángulos en **grados** en los controles (adentro, numpy trabaja en radianes); giro positivo = antihorario;
    rotación **activa** (se mueve la figura, los ejes quedan quietos) salvo que se marque lo contrario; todo alrededor del origen.
    """)
    return


@app.cell
def _(np):
    # ---------- las cuatro funciones de la unidad (se usan en todas las secciones) ----------

    def rot2(theta):
        """Matriz de rotación antihoraria del plano. theta en radianes."""
        c, s = np.cos(theta), np.sin(theta)
        return np.array([[c, -s], [s, c]])

    def rot_x(a):
        """Rotación de R³ alrededor del eje x: deja quieta la coordenada x, gira el plano (y, z)."""
        c, s = np.cos(a), np.sin(a)
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])

    def rot_y(a):
        """Rotación alrededor del eje y: deja quieta y, gira el plano (z, x). Mano derecha: e_z -> e_x."""
        c, s = np.cos(a), np.sin(a)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    def rot_z(a):
        """Rotación alrededor del eje z: deja quieta z, gira el plano (x, y)."""
        c, s = np.cos(a), np.sin(a)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    def transformar(nube, R):
        """Una nube de puntos es un array N×d (una fila por punto). Devuelve la nube transformada por R."""
        return nube @ R.T

    return rot2, rot_x, rot_y, rot_z, transformar


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. El hecho geométrico: ¿qué se conserva?

    Antes de cualquier fórmula, un dibujo en el cuaderno. Marcá un punto y dejalo quieto. Marcá otro y movelo, pero sin
    cambiar la distancia al primero (el profesor lo hizo con un cable de celular como soga: un extremo fijo, el otro gira).
    Ahora el resto de la hoja se acomoda sola: cada punto tiene que seguir a la misma distancia de los dos que ya ubicaste,
    y con los mismos ángulos. **Eso es una rotación: dejar quieto un punto, mover otro, y acomodar a todos los demás
    conservando distancias y ángulos.** Lo que se conserva es lo que define a la transformación.

    Lo que se ve: cada punto recorre una **circunferencia** centrada en el punto quieto. Esa es su *trayectoria*, "la línea
    de los lugares posibles a los que caer". Dos puntos a distinta distancia del centro recorren circunferencias distintas,
    y ninguna rotación puede llevar uno al otro. En la clase 2 esas trayectorias van a ser las líneas coordenadas.

    ### La escalera $\mathbb R \to \mathbb R^2 \to \mathbb R^3$

    | | ¿qué puede hacer una transformación que conserva distancias y deja quieto el $0$? | lo que se ve |
    |---|---|---|
    | $\mathbb R$ | $x \mapsto a\,x$ con $\lvert a\rvert = 1$: sólo $a = 1$ (nada) o $a = -1$ (reflexión) | en la recta **no hay giro**: lo único que se puede hacer es dar vuelta el signo |
    | $\mathbb R^2$ | aparece el **giro** de ángulo $\theta$: un número alcanza para describirlo | cada punto recorre una circunferencia; todas las rotaciones del plano conmutan entre sí |
    | $\mathbb R^3$ | hace falta además un **eje**: una recta que queda quieta; el plano perpendicular gira como en 2D | tres parámetros (eje y ángulo); componer giros de ejes distintos **depende del orden** |

    ### Los complejos: el giro como multiplicación

    Si pensamos el punto $(x, y)$ como el número $z = x + iy$, la fórmula de Euler
    $$e^{i\theta} = \cos\theta + i\,\sin\theta$$
    describe el círculo unidad: cuando $\theta$ crece, $e^{i\theta}$ **lo recorre** a velocidad 1. Multiplicar por $e^{i\theta}$
    gira cualquier $z$ un ángulo $\theta$ sin cambiarle el módulo ($\lvert e^{i\theta}\rvert = 1$). El caso más chico:
    multiplicar por $i = e^{i\pi/2}$ es girar un cuarto de vuelta. Y derivando respecto del ángulo,
    $\frac{d}{d\theta}e^{i\theta} = i\,e^{i\theta}$: la velocidad es el mismo punto girado un cuarto de vuelta, es decir,
    **tangente a la circunferencia**. "La derivada de la rotación es $i$."
    """)
    return


@app.cell
def _(go, mo, np):
    # el círculo unidad y la fórmula de Euler: e^{iθ} para θ = 60°, y su derivada i·e^{iθ} (tangente)
    _t = np.linspace(0, 2 * np.pi, 181)
    _th = np.deg2rad(60)
    _z = np.exp(1j * _th)
    _dz = 1j * _z
    _arc = np.linspace(0, _th, 40)
    _fig = go.Figure()
    _fig.add_trace(go.Scatter(x=np.cos(_t), y=np.sin(_t), mode="lines", line=dict(color="#9aa0a6", width=1), name="círculo unidad"))
    _fig.add_trace(go.Scatter(x=[0, 1], y=[0, 0], mode="lines+markers", line=dict(color="#9aa0a6", width=3), name="1"))
    _fig.add_trace(go.Scatter(x=np.cos(_arc), y=np.sin(_arc), mode="lines", line=dict(color="#1b6f6a", width=2, dash="dot"), name="θ"))
    _fig.add_trace(go.Scatter(x=[0, _z.real], y=[0, _z.imag], mode="lines+markers", line=dict(color="#1b6f6a", width=4), name="e^{iθ}"))
    _fig.add_trace(go.Scatter(x=[_z.real, _z.real + 0.5 * _dz.real], y=[_z.imag, _z.imag + 0.5 * _dz.imag], mode="lines+markers",
                              line=dict(color="#b5451b", width=3), name="i·e^{iθ} (tangente)"))
    _fig.update_layout(
        width=360, height=360, margin=dict(l=20, r=20, t=30, b=20), showlegend=True,
        legend=dict(x=0.02, y=0.98, bgcolor="rgba(255,255,255,0.7)"),
        xaxis=dict(range=[-1.3, 1.6], scaleanchor="y", zeroline=True, title="Re"),
        yaxis=dict(range=[-1.3, 1.6], zeroline=True, title="Im"),
        title=dict(text="e^{iθ} recorre el círculo; su derivada es tangente", font=dict(size=13)),
    )
    mo.hstack(
        [
            mo.ui.plotly(_fig),
            mo.md(r"""
            Con $\theta = 60°$: $e^{i\theta} = \tfrac12 + i\tfrac{\sqrt3}{2}$ (teal) y
            $i\,e^{i\theta} = -\tfrac{\sqrt3}{2} + i\tfrac12$ (naranja), perpendicular al radio.

            **Lo que hay que llevarse:** girar es multiplicar por un número de módulo 1.
            El módulo no cambia (distancias) y los argumentos se suman (ángulos).
            """),
        ],
        align="center",
    )
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Manipulación

    ### 2a. El plano: grilla, cuadrado unitario y una parcela

    Tres capas: en **gris**, el plano antes de la rotación (grilla y cuadrado unitario). En **teal**, el mismo plano después
    (la grilla transformada, el cuadrado transformado y las imágenes de $e_1$ y $e_2$: las columnas de la matriz). Y una
    **parcela** de cinco vértices con un norte marcado, para que se vea qué le pasa a un objeto reconocible. Tres de sus
    vértices dejan **estela**: el arco de circunferencia que recorren.

    Dos números vivos: el **área del cuadrado unitario transformado** (siempre $1$: eso es "se conserva") y la **distancia
    entre dos vértices** de la parcela, antes y después.

    El checkbox cambia entre rotación **activa** (gira la parcela, el sistema de ejes queda) y **pasiva** (gira el sistema de
    ejes y la parcela queda quieta: es lo que hace el agrimensor cuando cambia de norte; la parcela es la misma, cambian los
    números que anota). En modo pasivo, la parcela punteada muestra las coordenadas que anota el nuevo sistema: son las de
    la parcela girada $-\theta$.
    """)
    return


@app.cell
def _(mo):
    angulo_2d = mo.ui.slider(-180, 180, value=35, step=1, label="ángulo θ (°)", show_value=True)
    modo_pasivo = mo.ui.checkbox(value=False, label="pasiva: gira el sistema de ejes (cambio de norte); sin marcar: activa, gira la figura")
    return angulo_2d, modo_pasivo


@app.cell
def _(np):
    # ---------- objetos fijos de la figura 2D ----------
    L2 = 6  # semilado de la grilla
    parcela = np.array([[1, 1], [4, 1], [5, 3], [3, 5], [1, 4]], dtype=float)  # 5 vértices con enteros
    cuadrado_unitario = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    norte = np.array([[3.0, 3.0], [3.0, 4.2]])  # flecha "N" dentro de la parcela, apunta a +y
    vertices_con_estela = [1, 2, 3]  # índices de los vértices que dejan arco
    par_distancia = (0, 2)  # distancia viva entre estos dos vértices

    def grilla_segmentos(R, semilado=L2):
        """Las líneas de la grilla (x = k, y = k) transformadas por R, como un solo trazo con cortes (None)."""
        xs, ys = [], []
        for k in range(-semilado, semilado + 1):
            for seg in (np.array([[k, -semilado], [k, semilado]], float), np.array([[-semilado, k], [semilado, k]], float)):
                seg_r = seg @ R.T
                xs += [seg_r[0, 0], seg_r[1, 0], None]
                ys += [seg_r[0, 1], seg_r[1, 1], None]
        return xs, ys

    def cerrar(poligono):
        """Agrega el primer vértice al final para dibujar el contorno cerrado."""
        return np.vstack([poligono, poligono[:1]])

    def area_poligono(poligono):
        """Fórmula del cordón de zapato: área (con signo) de un polígono dado por sus vértices en orden."""
        x, y = poligono[:, 0], poligono[:, 1]
        return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)

    def arcos(puntos, theta, n=30):
        """Arcos de circunferencia desde cada punto hasta su imagen girada theta (un trazo con cortes)."""
        xs, ys = [], []
        for p in puntos:
            r, phi0 = np.hypot(*p), np.arctan2(p[1], p[0])
            phis = phi0 + np.linspace(0, theta, n)
            xs += list(r * np.cos(phis)) + [None]
            ys += list(r * np.sin(phis)) + [None]
        return xs, ys

    return (
        L2,
        arcos,
        area_poligono,
        cerrar,
        cuadrado_unitario,
        grilla_segmentos,
        norte,
        par_distancia,
        parcela,
        vertices_con_estela,
    )


@app.cell
def _(
    L2,
    angulo_2d,
    arcos,
    area_poligono,
    cerrar,
    cuadrado_unitario,
    go,
    grilla_segmentos,
    mo,
    modo_pasivo,
    norte,
    np,
    par_distancia,
    parcela,
    rot2,
    transformar,
    vertices_con_estela,
):
    theta_2d = np.deg2rad(angulo_2d.value)
    pasiva = modo_pasivo.value
    R_2d = rot2(theta_2d)

    def _capas(t):
        """Todo lo que cambia con el ángulo t: devuelve las trazas dinámicas en orden fijo."""
        R = rot2(t)
        gx, gy = grilla_segmentos(R)
        cuad = transformar(cuadrado_unitario, R)
        e1, e2 = R[:, 0], R[:, 1]
        # activa: la parcela gira t; pasiva: la parcela queda y el "fantasma" muestra las coordenadas en el sistema girado
        parc = transformar(parcela, R) if not pasiva else parcela
        nor = transformar(norte, R) if not pasiva else norte
        fantasma = transformar(parcela, R.T) if pasiva else parcela  # en activa coincide con la parcela original (gris)
        ax, ay = arcos(parcela[vertices_con_estela], t if not pasiva else -t)
        cc = cerrar(cuad)
        pc = cerrar(parc)
        fc = cerrar(fantasma)
        return [
            go.Scatter(x=gx, y=gy, mode="lines", line=dict(color="#1b6f6a", width=1), opacity=0.45, name="grilla después", hoverinfo="skip"),
            go.Scatter(x=cc[:, 0], y=cc[:, 1], mode="lines", fill="toself", fillcolor="rgba(27,111,106,0.25)", line=dict(color="#1b6f6a", width=2), name="cuadrado unitario después"),
            go.Scatter(x=[0, e1[0]], y=[0, e1[1]], mode="lines+markers", line=dict(color="#0d4f4b", width=4), marker=dict(size=[0, 9]), name="R e₁ (columna 1)"),
            go.Scatter(x=[0, e2[0]], y=[0, e2[1]], mode="lines+markers", line=dict(color="#3fa39c", width=4), marker=dict(size=[0, 9]), name="R e₂ (columna 2)"),
            go.Scatter(x=ax, y=ay, mode="lines", line=dict(color="#b5451b", width=1.5, dash="dot"), name="estelas (arcos)", hoverinfo="skip"),
            go.Scatter(x=fc[:, 0], y=fc[:, 1], mode="lines", line=dict(color="#b5451b", width=1.5, dash="dash"), name="coordenadas en el sistema girado", visible=pasiva),
            go.Scatter(x=pc[:, 0], y=pc[:, 1], mode="lines+markers", fill="toself", fillcolor="rgba(181,69,27,0.25)", line=dict(color="#b5451b", width=2.5), marker=dict(size=7), name="parcela"),
            go.Scatter(x=nor[:, 0], y=nor[:, 1], mode="lines+text", line=dict(color="#b5451b", width=3), text=["", "N"], textposition="top center", textfont=dict(size=14, color="#b5451b"), name="norte", hoverinfo="skip"),
        ]

    # capas estáticas (gris): grilla y cuadrado unitario antes, y la parcela original como contorno tenue
    _gx0, _gy0 = grilla_segmentos(np.eye(2))
    _c0 = cerrar(cuadrado_unitario)
    _p0 = cerrar(parcela)
    _estaticas = [
        go.Scatter(x=_gx0, y=_gy0, mode="lines", line=dict(color="#9aa0a6", width=1), opacity=0.5, name="grilla antes", hoverinfo="skip"),
        go.Scatter(x=_c0[:, 0], y=_c0[:, 1], mode="lines", fill="toself", fillcolor="rgba(154,160,166,0.25)", line=dict(color="#9aa0a6", width=2), name="cuadrado unitario antes"),
        go.Scatter(x=_p0[:, 0], y=_p0[:, 1], mode="lines", line=dict(color="#9aa0a6", width=1.5), name="parcela antes", hoverinfo="skip"),
    ]
    _n_est = len(_estaticas)
    _dinamicas = _capas(theta_2d)
    _idx = list(range(_n_est, _n_est + len(_dinamicas)))

    # 36 cuadros: de 0 hasta θ (el último cuadro coincide con lo que muestra el slider)
    _frames = [go.Frame(name=str(i), data=_capas(t), traces=_idx) for i, t in enumerate(np.linspace(0, theta_2d, 36))]

    figura_2d = go.Figure(
        data=_estaticas + _dinamicas,
        frames=_frames,
        layout=go.Layout(
            width=600, height=600, margin=dict(l=30, r=10, t=40, b=30),
            xaxis=dict(range=[-L2 - 1, L2 + 1], scaleanchor="y", zeroline=True, zerolinecolor="#444", title="x"),
            yaxis=dict(range=[-L2 - 1, L2 + 1], zeroline=True, zerolinecolor="#444", title="y"),
            legend=dict(orientation="h", y=-0.08, font=dict(size=10)),
            title=dict(text=f"θ = {angulo_2d.value}°  ·  {'pasiva (gira el sistema de ejes)' if pasiva else 'activa (gira la figura)'}", font=dict(size=14)),
            updatemenus=[dict(
                type="buttons", showactive=False, x=0.0, y=1.08, xanchor="left",
                buttons=[
                    dict(label="▶ reproducir", method="animate", args=[None, dict(frame=dict(duration=50, redraw=True), fromcurrent=False, transition=dict(duration=0))]),
                    dict(label="⏸ pausa", method="animate", args=[[None], dict(mode="immediate", frame=dict(duration=0))]),
                ],
            )],
        ),
    )

    # números vivos
    cuadrado_despues = transformar(cuadrado_unitario, R_2d)
    area_cuadrado = area_poligono(cuadrado_despues)
    parcela_despues = transformar(parcela, R_2d)
    _i, _j = par_distancia
    dist_antes = np.linalg.norm(parcela[_i] - parcela[_j])
    dist_despues = np.linalg.norm(parcela_despues[_i] - parcela_despues[_j])
    _v = parcela[2]
    _v_coord = (R_2d.T @ _v) if pasiva else (R_2d @ _v)

    _panel = mo.vstack([
        mo.md("**Controles**"),
        angulo_2d,
        modo_pasivo,
        mo.md(rf"""
        **Números vivos**

        - área del cuadrado unitario transformado: $\mathbf{{{area_cuadrado:.4f}}}$ (y $\det R = {np.linalg.det(R_2d):.4f}$)
        - distancia entre los vértices ${_i}$ y ${_j}$ de la parcela: antes ${dist_antes:.4f}$, después $\mathbf{{{dist_despues:.4f}}}$
        - vértice $(5, 3)$ → $({_v_coord[0]:.3f},\ {_v_coord[1]:.3f})$ {'(sus coordenadas en el sistema girado)' if pasiva else '(su imagen)'}

        $$R({angulo_2d.value}°) = \begin{{pmatrix}} {R_2d[0,0]:.3f} & {R_2d[0,1]:.3f} \\ {R_2d[1,0]:.3f} & {R_2d[1,1]:.3f} \end{{pmatrix}}$$

        Las columnas son $Re_1$ y $Re_2$ (los dos vectores teal). Apretá **reproducir** para ver el giro de $0$ a $\theta$
        en 36 cuadros: cada vértice recorre su arco.
        """),
    ], gap=0.6)
    mo.hstack([_panel, mo.ui.plotly(figura_2d)], widths=[1, 2], align="start")
    return R_2d, area_cuadrado, dist_antes, dist_despues, parcela_despues, theta_2d


@app.cell
def _(mo):
    mo.md(r"""
    ### 2b. El espacio: cubo unitario y un terreno

    En $\mathbb R^3$ no alcanza un ángulo: hace falta un **eje**. Las tres rotaciones básicas $R_x(\alpha)$, $R_y(\beta)$,
    $R_z(\gamma)$ dejan quieto un eje coordenado y giran el plano perpendicular (la rotación 2D "empotrada", con un $1$ en
    la diagonal para la coordenada que no se mueve). Acá se componen las tres: el cubo unitario y un **terreno** (malla de
    $7\times 7$ puntos con alturas, un array $49\times 3$) giran con $R = R_z R_y R_x$ (primero $x$, después $y$, después $z$:
    la matriz de la derecha actúa primero) o con el orden inverso, según el menú.

    En **línea de puntos naranja** se dibuja el cubo con el **otro orden**. La distancia entre los dos resultados es el número
    vivo que importa: con ángulos grandes son dos cubos distintos ("no conmutan"); con ángulos chicos casi coinciden
    ("sí conmutan a primer orden"). Probá con $\alpha = \beta = \gamma = 90°$ y después con $5°$. La cámara se mueve con el mouse.
    """)
    return


@app.cell
def _(mo):
    alfa = mo.ui.slider(-180, 180, value=40, step=1, label="α (°), alrededor de x", show_value=True)
    beta = mo.ui.slider(-180, 180, value=25, step=1, label="β (°), alrededor de y", show_value=True)
    gama = mo.ui.slider(-180, 180, value=60, step=1, label="γ (°), alrededor de z", show_value=True)
    orden = mo.ui.dropdown(
        options={"x → y → z   (R = Rz·Ry·Rx)": "xyz", "z → y → x   (R = Rx·Ry·Rz)": "zyx"},
        value="x → y → z   (R = Rz·Ry·Rx)",
        label="orden de aplicación",
    )
    return alfa, beta, gama, orden


@app.cell
def _(np):
    # ---------- objetos fijos de la figura 3D ----------
    _v = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)], dtype=float)
    cubo_vertices = _v  # 8×3
    cubo_aristas = [(a, b) for a in range(8) for b in range(a + 1, 8) if np.sum(np.abs(_v[a] - _v[b])) == 1]  # 12 aristas

    _u = np.linspace(-2, 2, 7)
    _X, _Y = np.meshgrid(_u, _u)
    _Z = 0.35 * np.sin(1.2 * _X) * np.cos(0.9 * _Y) - 1.2  # alturas suaves, por debajo del cubo
    terreno = np.column_stack([_X.ravel(), _Y.ravel(), _Z.ravel()])  # 49×3: una fila por punto

    def segmentos_3d(puntos, pares):
        """Un trazo con cortes que une los pares de índices dados (para aristas y mallas)."""
        xs, ys, zs = [], [], []
        for a, b in pares:
            xs += [puntos[a, 0], puntos[b, 0], None]
            ys += [puntos[a, 1], puntos[b, 1], None]
            zs += [puntos[a, 2], puntos[b, 2], None]
        return xs, ys, zs

    # pares de la malla del terreno (filas y columnas de la grilla 7×7)
    _n = 7
    malla_pares = [(i * _n + j, i * _n + j + 1) for i in range(_n) for j in range(_n - 1)] + [
        (i * _n + j, (i + 1) * _n + j) for i in range(_n - 1) for j in range(_n)
    ]
    return cubo_aristas, cubo_vertices, malla_pares, segmentos_3d, terreno


@app.cell
def _(
    alfa,
    beta,
    cubo_aristas,
    cubo_vertices,
    gama,
    go,
    malla_pares,
    mo,
    np,
    orden,
    rot_x,
    rot_y,
    rot_z,
    segmentos_3d,
    terreno,
    transformar,
):
    a_rad, b_rad, g_rad = (np.deg2rad(s.value) for s in (alfa, beta, gama))
    R_xyz = rot_z(g_rad) @ rot_y(b_rad) @ rot_x(a_rad)  # primero x, después y, después z
    R_zyx = rot_x(a_rad) @ rot_y(b_rad) @ rot_z(g_rad)  # primero z, después y, después x
    R_3d, R_otro = (R_xyz, R_zyx) if orden.value == "xyz" else (R_zyx, R_xyz)

    cubo_despues = transformar(cubo_vertices, R_3d)
    cubo_otro_orden = transformar(cubo_vertices, R_otro)
    terreno_despues = transformar(terreno, R_3d)
    dist_ordenes = np.linalg.norm(R_xyz - R_zyx)  # norma de Frobenius de la diferencia de matrices
    dist_vertice = np.linalg.norm(cubo_despues[7] - cubo_otro_orden[7])  # el vértice (1,1,1) en los dos órdenes

    _ejes = [go.Scatter3d(x=[0, 1.6 * (i == 0)], y=[0, 1.6 * (i == 1)], z=[0, 1.6 * (i == 2)], mode="lines+text", text=["", n],
                          line=dict(color="#444", width=3), showlegend=False, hoverinfo="skip") for i, n in enumerate("xyz")]
    _cx, _cy, _cz = segmentos_3d(cubo_vertices, cubo_aristas)
    _dx, _dy, _dz = segmentos_3d(cubo_despues, cubo_aristas)
    _ox, _oy, _oz = segmentos_3d(cubo_otro_orden, cubo_aristas)
    _tx, _ty, _tz = segmentos_3d(terreno, malla_pares)
    _ux, _uy, _uz = segmentos_3d(terreno_despues, malla_pares)
    figura_3d = go.Figure(
        data=_ejes + [
            go.Scatter3d(x=_cx, y=_cy, z=_cz, mode="lines", line=dict(color="#9aa0a6", width=3), name="cubo antes"),
            go.Scatter3d(x=_tx, y=_ty, z=_tz, mode="lines", line=dict(color="#9aa0a6", width=2), opacity=0.5, name="terreno antes", hoverinfo="skip"),
            go.Scatter3d(x=_dx, y=_dy, z=_dz, mode="lines", line=dict(color="#1b6f6a", width=6), name="cubo después"),
            go.Scatter3d(x=_ox, y=_oy, z=_oz, mode="lines", line=dict(color="#b5451b", width=3, dash="dot"), name="cubo con el otro orden"),
            go.Scatter3d(x=_ux, y=_uy, z=_uz, mode="lines", line=dict(color="#1b6f6a", width=2), name="terreno después", hoverinfo="skip"),
            go.Scatter3d(x=terreno_despues[:, 0], y=terreno_despues[:, 1], z=terreno_despues[:, 2], mode="markers",
                         marker=dict(size=3, color=terreno[:, 2], colorscale="Earth", showscale=False), name="puntos del terreno"),
        ],
        layout=go.Layout(
            width=600, height=560, margin=dict(l=0, r=0, t=30, b=0),
            scene=dict(xaxis=dict(range=[-2.6, 2.6]), yaxis=dict(range=[-2.6, 2.6]), zaxis=dict(range=[-2.6, 2.6]), aspectmode="cube"),
            legend=dict(orientation="h", y=-0.02, font=dict(size=10)),
            title=dict(text=f"α={alfa.value}°, β={beta.value}°, γ={gama.value}°  ·  orden {orden.value}", font=dict(size=14)),
        ),
    )

    def _pm(M):
        return r"\begin{pmatrix}" + r"\\".join(" & ".join(f"{x:.3f}" for x in fila) for fila in M) + r"\end{pmatrix}"

    _panel = mo.vstack([
        mo.md("**Controles**"),
        alfa, beta, gama, orden,
        mo.md(rf"""
        **Números vivos**

        - $\lVert R_zR_yR_x - R_xR_yR_z\rVert = \mathbf{{{dist_ordenes:.4f}}}$ (diferencia entre los dos órdenes)
        - el vértice $(1,1,1)$ del cubo cae a distancia $\mathbf{{{dist_vertice:.4f}}}$ de donde cae con el otro orden
        - $R^TR = I$: {bool(np.allclose(R_3d.T @ R_3d, np.eye(3)))} · $\det R = {np.linalg.det(R_3d):.4f}$

        $$R = {_pm(R_3d)}$$

        Bajá los tres ángulos a $5°$: la diferencia cae a ~$10^{{-2}}$; a $1°$, a ~$10^{{-3}}$. Es cuadrática en el ángulo:
        la no conmutatividad vive en el segundo orden (anexo 15 del apunte).
        """),
    ], gap=0.5)
    mo.hstack([_panel, mo.ui.plotly(figura_3d)], widths=[1, 2], align="start")
    return R_3d, R_xyz, R_zyx, cubo_despues, dist_ordenes, terreno_despues


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Cuenta a mano y código, lado a lado

    Izquierda: la cuenta como va en el cuaderno, con enteros. Derecha: la misma cuenta en numpy, con el código a la vista
    y lo que devuelve. Si las dos columnas no dicen lo mismo, algo está mal en alguna de las dos.
    """)
    return


@app.cell
def _(mo, np, rot2):
    # 3.1  R(90°) aplicada a (2, 1)
    _R90 = rot2(np.pi / 2)
    _v = np.array([2.0, 1.0])
    _w = _R90 @ _v
    mo.hstack([
        mo.md(r"""
        **3.1 Un cuarto de vuelta.** Con $\theta = 90°$: $\cos 90° = 0$, $\sin 90° = 1$.

        $$R(90°) = \begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}, \qquad
        R(90°)\begin{pmatrix} 2 \\ 1 \end{pmatrix} = \begin{pmatrix} 0\cdot2 - 1\cdot1 \\ 1\cdot 2 + 0\cdot 1\end{pmatrix}
        = \begin{pmatrix} -1 \\ 2 \end{pmatrix}.$$

        Lo que se ve: $(2,1)$ y $(-1,2)$ tienen el mismo largo $\sqrt5$ y forman ángulo recto. Es la regla "un cuarto de
        vuelta antihorario: $(x, y) \mapsto (-y, x)$", la misma que multiplicar $2 + i$ por $i$: $2i + i^2 = -1 + 2i$.
        """),
        mo.vstack([
            mo.md("""
            ```python
            R90 = rot2(np.pi / 2)        # grados en la UI, radianes adentro
            v = np.array([2.0, 1.0])
            w = R90 @ v
            ```
            """),
            mo.md(f"`R90` =\n```\n{np.round(_R90, 3)}\n```\n`w` = `{np.round(_w, 3)}` · `np.linalg.norm(v)` = `{np.linalg.norm(_v):.4f}` · `np.linalg.norm(w)` = `{np.linalg.norm(_w):.4f}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(mo, np, rot2):
    # 3.2  R(θ) deducida de las imágenes de e1 y e2, y desde los complejos
    _th = np.deg2rad(30)
    _R = rot2(_th)
    _e1_img = _R @ np.array([1.0, 0.0])
    _e2_img = _R @ np.array([0.0, 1.0])
    _z = 1 + 0j
    _zr = _z * np.exp(1j * _th)
    mo.hstack([
        mo.md(r"""
        **3.2 De dónde sale $R(\theta)$.** Una transformación lineal queda determinada por lo que hace con $e_1$ y $e_2$,
        y la matriz tiene esas imágenes como **columnas**. Girando $\theta$:
        $e_1 = (1, 0) \mapsto (\cos\theta, \sin\theta)$ y $e_2 = (0, 1) \mapsto (-\sin\theta, \cos\theta)$
        (es $e_1$ girado un cuarto de vuelta más). Entonces
        $$R(\theta) = \begin{pmatrix} \cos\theta & -\sin\theta \\ \sin\theta & \cos\theta \end{pmatrix}.$$

        **La misma cuenta con complejos:** $(x + iy)(\cos\theta + i\sin\theta) = (x\cos\theta - y\sin\theta) + i\,(x\sin\theta + y\cos\theta)$.
        La parte real es la primera fila de $R(\theta)\binom{x}{y}$, la parte imaginaria la segunda. Multiplicar por
        $e^{i\theta}$ y multiplicar por $R(\theta)$ son la **misma operación** escrita de dos formas. Con $\theta = 30°$:
        $\cos 30° = \tfrac{\sqrt3}{2} \approx 0.866$, $\sin 30° = \tfrac12$.
        """),
        mo.vstack([
            mo.md("""
            ```python
            th = np.deg2rad(30)
            R = rot2(th)
            e1_img = R @ np.array([1.0, 0.0])   # primera columna
            e2_img = R @ np.array([0.0, 1.0])   # segunda columna
            zr = (1 + 0j) * np.exp(1j * th)     # e1 como complejo, girado
            ```
            """),
            mo.md(f"`R` =\n```\n{np.round(_R, 3)}\n```\n`e1_img` = `{np.round(_e1_img, 3)}` · `e2_img` = `{np.round(_e2_img, 3)}`  \n`zr` = `{np.round(_zr, 3)}` → `(zr.real, zr.imag)` coincide con `e1_img`: `{bool(np.allclose([_zr.real, _zr.imag], _e1_img))}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(mo, np, rot2):
    # 3.3  el producto interno se conserva: <Rv, Rw> = <v, w>
    _R = rot2(np.pi / 2)
    _v, _w = np.array([2.0, 1.0]), np.array([1.0, 3.0])
    _Rv, _Rw = _R @ _v, _R @ _w
    mo.hstack([
        mo.md(r"""
        **3.3 Se conserva el producto interno.** Con $v = (2, 1)$, $w = (1, 3)$ y $R = R(90°)$:
        $$\langle v, w\rangle = 2\cdot1 + 1\cdot3 = 5, \qquad Rv = (-1, 2),\ Rw = (-3, 1), \qquad
        \langle Rv, Rw\rangle = (-1)(-3) + 2\cdot1 = 5.$$

        Lo que se ve: la regla y el transportador miden lo mismo antes y después. Como $\lVert v\rVert^2 = \langle v, v\rangle$
        y $\cos\angle(v,w) = \frac{\langle v,w\rangle}{\lVert v\rVert\lVert w\rVert}$, conservar el producto interno es conservar
        **longitudes y ángulos de una sola vez**. Eso es lo que define a una rotación.
        """),
        mo.vstack([
            mo.md("""
            ```python
            R = rot2(np.pi / 2)
            v, w = np.array([2.0, 1.0]), np.array([1.0, 3.0])
            antes = v @ w            # producto interno = suma de productos
            despues = (R @ v) @ (R @ w)
            ```
            """),
            mo.md(f"`antes` = `{_v @ _w:.1f}` · `despues` = `{_Rv @ _Rw:.1f}` · `np.isclose(antes, despues)` = `{bool(np.isclose(_v @ _w, _Rv @ _Rw))}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(mo, np, rot2):
    # 3.4  R^T R = I  y  det R = 1
    _R = rot2(np.pi / 2)
    _RtR = _R.T @ _R
    _th = np.deg2rad(30)
    _R30 = rot2(_th)
    mo.hstack([
        mo.md(r"""
        **3.4 Ortogonal, y sin espejo.** Conservar $\langle v, w\rangle$ para todo par equivale a $R^TR = I$ (la matriz es
        **ortogonal**: columnas perpendiculares y de largo 1). Con $R(90°)$:
        $$R^TR = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}\begin{pmatrix} 0 & -1 \\ 1 & 0 \end{pmatrix}
        = \begin{pmatrix} 0+1 & 0+0 \\ 0+0 & 1+0 \end{pmatrix} = I.$$
        Y en general $R^TR = \begin{pmatrix}\cos^2\theta + \sin^2\theta & 0 \\ 0 & \sin^2\theta + \cos^2\theta\end{pmatrix} = I$.

        Pero $\mathrm{diag}(1, -1)$ también cumple $A^TA = I$ y es un **espejo** (la grilla sigue cuadrada, pero dada vuelta).
        Lo que distingue a la rotación es el determinante: $\det R(\theta) = \cos^2\theta + \sin^2\theta = 1$ (área
        conservada, orientación conservada), mientras que $\det\mathrm{diag}(1,-1) = -1$.
        """),
        mo.vstack([
            mo.md("""
            ```python
            R = rot2(np.pi / 2)
            RtR = R.T @ R
            det = np.linalg.det(R)
            espejo = np.diag([1.0, -1.0])
            ```
            """),
            mo.md(f"`RtR` =\n```\n{np.round(_RtR, 3)}\n```\n`det` = `{np.linalg.det(_R):.1f}` · `np.linalg.det(rot2(np.deg2rad(30)))` = `{np.linalg.det(_R30):.4f}`  \n`espejo.T @ espejo` es `I`: `{bool(np.allclose(np.diag([1.0, -1.0]).T @ np.diag([1.0, -1.0]), np.eye(2)))}` · `np.linalg.det(espejo)` = `{np.linalg.det(np.diag([1.0, -1.0])):.1f}`"),
        ]),
    ], widths="equal", align="start")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. El Python de hoy: una nube de puntos es un array $N \times 2$

    Una sola idea nueva. En vez de rotar un punto a la vez, ponemos **todos los puntos en un array con una fila por punto**:
    la parcela es un array $5\times2$, la grilla un array $M\times2$, el terreno un array $49\times3$. Una transformación es
    entonces **una función que recibe la nube y devuelve otra nube** de la misma forma.

    La cuenta "matriz por vector" es $R\,v$ con $v$ columna. Si los puntos están en filas, hay que **transponer**:
    $(R\,v)^T = v^T R^T$. Por eso la función es `nube @ R.T`: cada fila $v^T$ se multiplica por $R^T$ y sale la fila
    $(Rv)^T$. Una línea, y sirve igual para 2D y 3D.
    """)
    return


@app.cell
def _(R_2d, R_3d, mo, np, parcela, rot2, terreno, transformar):
    _tres = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]])  # tres puntos: e1, e2 y (2, 1)
    _tres_90 = transformar(_tres, rot2(np.pi / 2))
    _parc = transformar(parcela, R_2d)
    _terr = transformar(terreno, R_3d)
    mo.vstack([
        mo.md("""
        ```python
        def transformar(nube, R):
            \"\"\"nube: array N×d, una fila por punto. Devuelve la nube transformada por R.\"\"\"
            return nube @ R.T

        tres = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]])   # shape (3, 2)
        transformar(tres, rot2(np.pi / 2))                       # cada fila girada 90°
        ```
        """),
        mo.md(f"`tres.shape` = `{_tres.shape}` → resultado:\n```\n{np.round(_tres_90, 3)}\n```\n"
              f"Las filas son $(0,1)$, $(-1,0)$ y $(-1,2)$: las imágenes de $e_1$, $e_2$ y $(2,1)$, como en la sección 3.  \n\n"
              f"La **misma función** sirve para la parcela (`parcela.shape` = `{parcela.shape}` → `{_parc.shape}`), para la grilla "
              f"y para el terreno 3D (`terreno.shape` = `{terreno.shape}` → `{_terr.shape}`, con la $R$ de $3\\times3$ de la sección 2b). "
              f"Primera fila del terreno transformado: `{np.round(_terr[0], 3)}`."),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Ejercicios

    Cada ejercicio trae el nivel de la rúbrica de autoevaluación del profesor (elemental / medio / avanzado) con la frase
    de la rúbrica a la que apunta. Los de lápiz tienen la respuesta escondida; los de código se verifican solos.
    """)
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        **(a) Lápiz — elemental** *("Multiplicar por $i$ es rotar $\pi/2$"; "las matrices y las transformaciones lineales
        tienen una correspondencia 1 a 1").*
        Rotá el punto $(3, 4)$ un ángulo de $90°$ y después de $-90°$. Hacelo de las dos formas: con la matriz $R(\pm90°)$
        y multiplicando $3 + 4i$ por $\pm i$. Dibujá los tres puntos y el círculo que los une.
        """),
        mo.accordion({
            "Ver respuesta": mo.md(r"""
            $R(90°)\binom{3}{4} = \binom{0\cdot3 - 1\cdot4}{1\cdot3 + 0\cdot4} = \binom{-4}{3}$ y
            $(3 + 4i)\,i = 3i + 4i^2 = -4 + 3i$. ✓

            $R(-90°) = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$, $R(-90°)\binom{3}{4} = \binom{4}{-3}$ y
            $(3 + 4i)(-i) = -3i - 4i^2 = 4 - 3i$. ✓

            Los tres puntos están sobre la circunferencia de radio $5$: $3^2 + 4^2 = 4^2 + 3^2 = 25$.
            """)
        }),
    ])
    return


@app.cell
def _(mo):
    mo.vstack([
        mo.md(r"""
        **(b) Lápiz — medio** *("Hay transformaciones que se definen completamente por qué propiedades de los objetos
        transformados mantienen").*
        ¿Qué ángulo $\theta$ lleva $(1, 0)$ a $(0, -1)$? Escribí $R(\theta)$ con números y verificá que la distancia de
        $(1,0)$ al origen no cambia. ¿Hay otra matriz ortogonal, que **no** sea una rotación, que también lleve $(1,0)$ a
        $(0,-1)$? ¿Qué la distingue?
        """),
        mo.accordion({
            "Ver respuesta": mo.md(r"""
            La primera columna de $R(\theta)$ es la imagen de $e_1 = (1, 0)$: $(\cos\theta, \sin\theta) = (0, -1)$, así que
            $\theta = -90°$ (o $270°$). $R(-90°) = \begin{pmatrix} 0 & 1 \\ -1 & 0 \end{pmatrix}$.
            Distancia al origen: antes $\sqrt{1^2 + 0^2} = 1$, después $\sqrt{0^2 + (-1)^2} = 1$. ✓

            Sí: $A = \begin{pmatrix} 0 & -1 \\ -1 & 0 \end{pmatrix}$ (reflexión respecto de la recta $y = -x$) también lleva
            $(1,0)$ a $(0,-1)$ y cumple $A^TA = I$. Pero $\det A = 0 - 1 = -1$: es un espejo. Mandar un solo punto no alcanza
            para fijar la transformación; conservar distancias **y orientación** sí.
            """)
        }),
    ])
    return


@app.cell
def _(mo):
    mo.md(r"""
    **(c) Código con hueco — medio** *("Hay una equivalencia entre operaciones en $\mathbb C$ y en $\mathbb R^2$"; la idea
    de la sección 4: nube $N\times2$ y `@ R.T`).*
    Completá `rotar(puntos, theta)`: recibe una nube $N\times2$ y un ángulo en **radianes** y devuelve la nube girada.
    Tenés `np` disponible. Se verifica contra la implementación de referencia con `np.allclose` sobre 20 puntos al azar
    (editá y hacé clic fuera del editor, o Ctrl/Cmd + Enter).
    """)
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def rotar(puntos, theta):\n    c, s = np.cos(theta), np.sin(theta)\n    R = ...   # armá la matriz 2×2\n    return ...   # una fila por punto: ¿quién va transpuesto?\n",
        language="python",
        min_height=140,
        label="ejercicio (c)",
    )
    editor_c
    return (editor_c,)


@app.cell
def _(editor_c, mo, np, rot2, transformar):
    _rng = np.random.default_rng(56798)
    _puntos = _rng.uniform(-5, 5, size=(20, 2))
    _theta = np.deg2rad(37)
    _esperado = transformar(_puntos, rot2(_theta))
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.asarray(_ns["rotar"](_puntos, _theta), dtype=float)
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ la forma del resultado es `{_obtenido.shape}`; tiene que ser `{_esperado.shape}` (una fila por punto)."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ `rotar` coincide con la referencia en los 20 puntos (θ = 37°). También con θ = 90°: " +
                                    f"`{bool(np.allclose(np.asarray(_ns['rotar'](_puntos, np.pi / 2)), transformar(_puntos, rot2(np.pi / 2))))}`."), kind="success")
        elif np.allclose(_obtenido, transformar(_puntos, rot2(-_theta))):
            _res = mo.callout(mo.md("❌ gira para el otro lado: te quedó $R(-\\theta)$. ¿El seno negativo va arriba a la derecha o abajo a la izquierda?"), kind="warn")
        elif np.allclose(_obtenido, _puntos @ rot2(_theta)):
            _res = mo.callout(mo.md("❌ casi: usaste `puntos @ R`, que es $R^T$ aplicada a cada fila. Con filas = puntos va `puntos @ R.T`."), kind="warn")
        else:
            _res = mo.callout(mo.md(f"❌ no coincide. Primer punto: esperado `{np.round(_esperado[0], 3)}`, obtenido `{np.round(_obtenido[0], 3)}`."), kind="danger")
    except Exception as _e:  # el hueco sin completar (Ellipsis) cae acá
        _res = mo.callout(mo.md(f"⏳ todavía no corre: `{type(_e).__name__}: {_e}`"), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    **(d) Código con hueco — avanzado** *("Combinación de rotaciones son rotaciones"; el eje como dirección que queda fija,
    que en la clase 6 va a ser "autovector de autovalor 1").*
    Armá $R = R_z(90°)\,R_y(90°)$ (primero gira alrededor de $y$, después alrededor de $z$), aplicala a $(1, 0, 0)$ y
    verificá que el eje $u = (-1, 1, 1)/\sqrt3$ queda fijo: `np.allclose(R @ u, u)`. Tenés `np`, `rot_x`, `rot_y`, `rot_z`.
    Pregunta para el cuaderno: ¿por qué $R$ **tiene** que dejar quieta alguna dirección?
    """)
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="R = ...                       # Rz(90°) · Ry(90°), en radianes\nimagen = R @ np.array([1.0, 0.0, 0.0])\nu = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)\nfijo = ...                    # np.allclose(...)\n",
        language="python",
        min_height=140,
        label="ejercicio (d)",
    )
    editor_d
    return (editor_d,)


@app.cell
def _(editor_d, mo, np, rot_x, rot_y, rot_z):
    _R_ref = rot_z(np.pi / 2) @ rot_y(np.pi / 2)
    _u = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    _ns = {"np": np, "rot_x": rot_x, "rot_y": rot_y, "rot_z": rot_z}
    try:
        exec(editor_d.value, _ns)
        _R = np.asarray(_ns["R"], dtype=float)
        _imagen = np.asarray(_ns["imagen"], dtype=float)
        _fijo = _ns["fijo"]
        if _R.shape != (3, 3):
            _res = mo.callout(mo.md(f"❌ `R` tiene forma `{_R.shape}`; tiene que ser `(3, 3)`."), kind="danger")
        elif np.allclose(_R, rot_y(np.pi / 2) @ rot_z(np.pi / 2)):
            _res = mo.callout(mo.md("❌ armaste $R_y R_z$: ese orden aplica primero $z$. La matriz de la derecha actúa primero; "
                                    "$R_z(90°) R_y(90°)$ es `rot_z(...) @ rot_y(...)`."), kind="warn")
        elif not np.allclose(_R, _R_ref):
            _res = mo.callout(mo.md(f"❌ `R` no es $R_z(90°)R_y(90°)$. ¿Pasaste los ángulos en radianes (`np.pi / 2`)? Primera columna esperada `[0, 0, -1]`, obtenida `{np.round(_R[:, 0], 3)}`."), kind="danger")
        elif not np.allclose(_imagen, [0, 0, -1]):
            _res = mo.callout(mo.md(f"❌ `R` está bien pero `imagen` = `{np.round(_imagen, 3)}`; $R\\,e_x$ es la primera columna, $(0, 0, -1)$."), kind="warn")
        elif _fijo is not True:
            _res = mo.callout(mo.md(f"❌ `R` e `imagen` están bien; `fijo` vale `{_fijo!r}`, tiene que ser `np.allclose(R @ u, u)` → `True`."), kind="warn")
        else:
            _res = mo.callout(mo.md(r"✅ $R = R_z(90°)R_y(90°)$ manda $e_x \mapsto (0,0,-1)$ y deja fijo $u = (-1,1,1)/\sqrt3$: ese es el eje de la "
                                    r"rotación compuesta. Dos giros de $90°$ alrededor de ejes distintos dan **un** giro alrededor de un eje nuevo "
                                    r"(de $120°$: $R^3 = I$, verificalo). En la clase 6, $Ru = u$ se lee \"$u$ es autovector de autovalor 1\"."), kind="success")
    except Exception as _e:
        _res = mo.callout(mo.md(f"⏳ todavía no corre: `{type(_e).__name__}: {_e}`"), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Enlaces del mapa

    - **Ficha de la clase 1** (hilo del profesor, rúbrica, lo que pasó el 19/8, cuentas chicas): [clases/01.html](../../clases/01.html)
    - **Ficha de la clase 2** (composición, conmutatividad, trayectoria): [clases/02.html](../../clases/02.html)
    - **Apunte** (PDF): [apunte.pdf](../../apunte.pdf) — bloque 07 "Rotaciones" (plano, complejos, 3D, eje y exponencial),
      anexo 14 "Construcción geométrica de las matrices de rotación 3D" (por qué $R_y$ tiene los signos cambiados de lado; fórmula
      de Rodrigues) y anexo 15 "Rotaciones infinitesimales y orden de composición" (la demostración de que el orden aparece recién
      en el segundo orden: $R_x(\varepsilon)R_y(\delta) - R_y(\delta)R_x(\varepsilon) \approx \varepsilon\delta\,[A_x, A_y]$).
    - **Mapa de conceptos** y lista de unidades: [índice](../../index.html). Próxima unidad: 03 reflexiones y similaridades
      (las ortogonales con $\det = -1$; pendiente). Ya disponible: [07 producto cuña, determinante, núcleo y autovectores](../07_cuna_autovectores/index.html),
      donde el eje de la rotación reaparece como autovector.

    Viene de: transformación lineal y matrices del CBC, producto interno, complejos del secundario.
    Lleva a: composición y conmutatividad (clase 2), reflexiones y afines (clase 3), autovectores (clase 6), exponencial de matrices (clase 8).
    """)
    return


@app.cell
def _(
    R_2d,
    R_3d,
    R_xyz,
    R_zyx,
    area_cuadrado,
    dist_antes,
    dist_despues,
    dist_ordenes,
    np,
    parcela,
    parcela_despues,
    rot2,
    rot_x,
    rot_y,
    rot_z,
    terreno,
    terreno_despues,
    theta_2d,
    transformar,
):
    # ---------- asserts silenciosos: validan todas las cuentas de la unidad ----------
    _I2, _I3 = np.eye(2), np.eye(3)
    # sección 3
    assert np.allclose(rot2(np.pi / 2), [[0, -1], [1, 0]])
    assert np.allclose(rot2(np.pi / 2) @ [2, 1], [-1, 2])
    assert np.allclose(rot2(np.pi / 2) @ [3, 1], [-1, 3])  # cuenta chica 1 de la ficha
    assert np.allclose(rot2(np.deg2rad(30)) @ [1, 0], [np.sqrt(3) / 2, 0.5])
    _z = (2 + 1j) * 1j
    assert np.allclose([_z.real, _z.imag], rot2(np.pi / 2) @ [2, 1])
    _v, _w = np.array([2.0, 1.0]), np.array([1.0, 3.0])
    assert np.isclose(_v @ _w, 5) and np.isclose((rot2(np.pi / 2) @ _v) @ (rot2(np.pi / 2) @ _w), 5)
    for _t in np.linspace(-np.pi, np.pi, 13):
        assert np.allclose(rot2(_t).T @ rot2(_t), _I2) and np.isclose(np.linalg.det(rot2(_t)), 1)
    assert np.isclose(np.linalg.det(np.diag([1.0, -1.0])), -1)
    assert np.allclose(rot2(0.3) @ rot2(0.5), rot2(0.8))  # R(α)R(β) = R(α+β)
    # sección 2a: lo que se conserva
    assert np.isclose(area_cuadrado, 1) and np.isclose(np.linalg.det(R_2d), 1)
    assert np.isclose(dist_antes, dist_despues)
    assert np.allclose(parcela_despues, (R_2d @ parcela.T).T)  # nube @ R.T == (R @ columnas).T
    assert np.allclose(np.linalg.norm(parcela_despues, axis=1), np.linalg.norm(parcela, axis=1))
    assert np.allclose(rot2(theta_2d).T, rot2(-theta_2d))  # pasiva = activa con −θ
    # sección 2b
    for _rot, _e in ((rot_x, [1, 0, 0]), (rot_y, [0, 1, 0]), (rot_z, [0, 0, 1])):
        assert np.allclose(_rot(0.7) @ _e, _e) and np.allclose(_rot(0.7).T @ _rot(0.7), _I3) and np.isclose(np.linalg.det(_rot(0.7)), 1)
    assert np.allclose(rot_y(np.pi / 2) @ [1, 0, 0], [0, 0, -1]) and np.allclose(rot_y(np.pi / 2) @ [0, 0, 1], [1, 0, 0])
    assert np.allclose(rot_y(np.pi / 2) @ rot_x(np.pi / 2) @ [0, 0, 1], [0, -1, 0])  # cuenta chica 2 de la ficha
    assert np.allclose(rot_x(np.pi / 2) @ rot_y(np.pi / 2) @ [0, 0, 1], [1, 0, 0])
    assert np.allclose(R_3d.T @ R_3d, _I3) and np.isclose(np.linalg.det(R_3d), 1)
    assert np.isclose(np.linalg.norm(R_xyz - R_zyx), dist_ordenes)
    assert terreno_despues.shape == terreno.shape == (49, 3)
    assert np.allclose(np.linalg.norm(terreno_despues, axis=1), np.linalg.norm(terreno, axis=1))
    # la no conmutatividad es de segundo orden: con ε la diferencia es ~ε², con ε/10 es ~100 veces menor
    _d = lambda e: np.linalg.norm(rot_z(e) @ rot_y(e) @ rot_x(e) - rot_x(e) @ rot_y(e) @ rot_z(e))
    assert 50 < _d(0.1) / _d(0.01) < 200
    # ejercicios
    assert np.allclose(rot2(np.pi / 2) @ [3, 4], [-4, 3]) and np.allclose(rot2(-np.pi / 2) @ [3, 4], [4, -3])
    assert np.allclose(rot2(-np.pi / 2) @ [1, 0], [0, -1])
    _A = np.array([[0.0, -1.0], [-1.0, 0.0]])
    assert np.allclose(_A @ [1, 0], [0, -1]) and np.allclose(_A.T @ _A, _I2) and np.isclose(np.linalg.det(_A), -1)
    _Rd = rot_z(np.pi / 2) @ rot_y(np.pi / 2)
    _u = np.array([-1.0, 1.0, 1.0]) / np.sqrt(3)
    assert np.allclose(_Rd, [[0, -1, 0], [0, 0, 1], [-1, 0, 0]])
    assert np.allclose(_Rd @ [1, 0, 0], [0, 0, -1]) and np.allclose(_Rd @ _u, _u)
    assert np.allclose(np.linalg.matrix_power(_Rd, 3), _I3)  # giro de 120°
    _P = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]], float)  # cuenta chica 3 de la ficha: la permutación fija (1,1,1)
    assert np.allclose(_P @ [1, 1, 1], [1, 1, 1]) and np.isclose(np.linalg.det(_P), 1)
    assert np.isclose(385 * (np.pi / 1000) * np.sqrt(3), np.deg2rad(120), atol=2e-3)
    # sección 4
    assert transformar(np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]]), rot2(np.pi / 2)).tolist() == [[0, 1], [-1, 0], [-1, 2]] or np.allclose(
        transformar(np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 1.0]]), rot2(np.pi / 2)), [[0, 1], [-1, 0], [-1, 2]]
    )
    return


if __name__ == "__main__":
    app.run()
