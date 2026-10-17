"""cb104 — módulo común de las unidades marimo de Sistemas de Coordenadas (CB104, Agrimensura FIUBA).

Vive en `unidades/`, el mismo directorio que los notebooks: marimo pone ese directorio en `sys.path`,
así que en `marimo edit` / `marimo run` alcanza con `import cb104 as lib`. Para el export WASM el
módulo no existe en el navegador: `tools/build.py` reemplaza la celda marcada con `# cb104:inline`
por una que embebe este archivo (ver tools/README.md, "Módulo común y export WASM").

Reglas: sólo numpy (y plotly, importado adentro de las funciones que dibujan). Ángulos en radianes.
Nube de puntos = array N×d, una fila por punto. Paleta del apunte: teal, rust, gold.

Probar:  uv run python unidades/cb104.py
"""

from __future__ import annotations

import numpy as np

__all__ = [
    # paleta
    "COLORES", "GRIS_ANTES", "TEAL_DESPUES", "VIOLETA_OBJETO", "color_columna",
    # álgebra y geometría
    "rot2", "rot_x", "rot_y", "rot_z", "rodrigues", "transformar", "hom", "dehom",
    "area_poligono", "perp2", "pot_real", "circulo", "pentagono_regular", "grilla_oblicua",
    "cerrar", "estelas", "segmentos_a_trazo", "coordenadas_en_base", "eje_angulo",
    # LaTeX
    "matriz_coloreada", "pmat", "vec_tex", "vec_plano", "num_tex",
    # plotly 2D
    "figura_plano", "grilla_segmentos", "capa_antes", "capa_despues", "objeto", "punto", "flecha",
    "flechas_columnas", "lectura_coordenadas", "animar",
    # plotly 3D
    "figura_espacio", "cubo_unitario", "malla_pares", "terreno_suave", "segmentos_3d", "flechas_columnas_3d",
    # verificación
    "verificar", "exacto",
    # producto interno (lección 02)
    "proyeccion", "angulo", "arco_angulo",
    # afinidades (lección 04)
    "transformar_afin", "matriz_afin", "partes_afin", "afin_por_tres_puntos", "capa_despues_afin",
    # cambio de base y diagonalización (lección 08)
    "diagonalizar", "capa_base", "capa_ejes_propios",
    # cuña, núcleo y autovectores (lecciones 07a, 07b, 07c)
    "cuna2", "cuna3", "alineados", "paralelogramo", "paralelepipedo", "plano_3d", "nucleo2",
    "autovalores_reales", "autovectores_cuna", "direcciones_propias", "puntos_fijos_proyectivos",
    # jacobiano y primera forma fundamental (lección 10)
    "xyz", "jacobiana_numerica", "primera_forma", "longitud_paso", "longitud_poligonal", "flecha_3d",
    "superficie_malla", "plano_tangente",
    # mínimos cuadrados: los cuatro problemas (lección 11)
    "minimos_cuadrados", "recta_ajuste", "punto_por_distancias", "procrustes", "regresion_total",
    # trigonometría esférica (lección 14)
    "punto_esfera", "esfera_malla", "arco_maximo", "lado_esferico", "angulo_esferico", "angulo_vertice",
    "triangulo_esferico", "exceso_esferico",
    # curvatura y segunda forma fundamental (lección 12)
    "formas_fundamentales", "curvatura_normal", "curvaturas_principales", "curvatura_gauss", "seccion_normal",
    "circulo_3d",
    # elipsoide de revolución (lección 13)
    "elipsoide", "elipsoide_grs80", "radios_curvatura", "latitudes", "geodesica_a_cartesiana", "normal_elipsoide", "gms",
]

# ----------------------------------------------------------------------------
# paleta (la de apunte-formato.sty; igual en el álgebra y en la figura)
# ----------------------------------------------------------------------------

COLORES = ("#1b6f6a", "#b5451b", "#c9a227")  # columna 1 teal, columna 2 rust, columna 3 gold
GRIS_ANTES = "#9aa0a6"  # capa "antes": grilla de referencia, cuadrado/cubo unitario original
TEAL_DESPUES = COLORES[0]  # capa "después": grilla transformada
VIOLETA_OBJETO = "#7a4e9e"  # el objeto reconocible (parcela) y sus estelas


def color_columna(i):
    """Color de la columna i (0, 1, 2) de una matriz: teal, rust, gold. Cicla si hay más columnas."""
    return COLORES[i % len(COLORES)]


# ----------------------------------------------------------------------------
# álgebra y geometría (numpy puro)
# ----------------------------------------------------------------------------


def rot2(theta):
    """Matriz de rotación antihoraria del plano. theta en radianes."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def rot_x(a):
    """Rotación de R³ alrededor del eje x: deja quieta la coordenada x, gira el plano (y, z)."""
    c, s = np.cos(a), np.sin(a)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def rot_y(a):
    """Rotación alrededor del eje y: deja quieta y, gira el plano (z, x). Mano derecha: e_z → e_x."""
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def rot_z(a):
    """Rotación alrededor del eje z: deja quieta z, gira el plano (x, y)."""
    c, s = np.cos(a), np.sin(a)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def rodrigues(eje, theta):
    """Rotación 3×3 de ángulo theta (radianes) alrededor de `eje` (se normaliza; no puede ser nulo).

    Fórmula de Rodrigues: R = I + sin θ · K + (1 − cos θ) · K², con K la matriz antisimétrica del eje
    unitario (K v = k × v). Sentido antihorario mirando desde la punta del eje (mano derecha).
    """
    k = np.asarray(eje, dtype=float).reshape(3)
    norma = np.linalg.norm(k)
    if norma == 0.0:
        raise ValueError("el eje de rotación no puede ser el vector nulo")
    kx, ky, kz = k / norma
    K = np.array([[0.0, -kz, ky], [kz, 0.0, -kx], [-ky, kx, 0.0]])
    return np.eye(3) + np.sin(theta) * K + (1.0 - np.cos(theta)) * (K @ K)


def transformar(nube, M):
    """Nube N×d (una fila por punto) transformada por M: nube @ M.T (equivale a M p para cada fila p)."""
    return np.asarray(nube, dtype=float) @ np.asarray(M, dtype=float).T


def hom(p):
    """(x, y) → vector homogéneo (x, y, 1), float. Una nube N×2 → N×3 (columna de unos al final)."""
    p = np.asarray(p, dtype=float)
    if p.ndim == 2:
        return np.column_stack([p[:, :2], np.ones(len(p))])
    return np.array([p[0], p[1], 1.0])


def dehom(v):
    """(x, y, w) → array (x/w, y/w). Devuelve None si el punto es impropio (w ≈ 0).

    Una nube N×3 → N×2 (fila a fila, cada una dividida por su w; una fila impropia da inf/nan, no None).
    """
    v = np.asarray(v, dtype=float)
    if v.ndim == 2:
        with np.errstate(divide="ignore", invalid="ignore"):
            return v[:, :2] / v[:, 2:3]
    if abs(v[2]) < 1e-12 * max(1.0, float(np.abs(v).max())):
        return None
    return v[:2] / v[2]


def area_poligono(p):
    """Fórmula del cordón de zapato: área CON SIGNO de un polígono dado por sus vértices N×2 en orden.

    Positiva si los vértices van en sentido antihorario; una reflexión la vuelve negativa.
    """
    p = np.asarray(p, dtype=float)
    x, y = p[:, 0], p[:, 1]
    return 0.5 * float(np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def perp2(v):
    """En 2D: el perpendicular de (a, b) es (b, −a) (la cruz (a, b, 0) × (0, 0, 1))."""
    a, b = (float(x) for x in v)
    return np.array([b, -a])


def pot_real(A, t):
    """A^t para t real, vía diagonalización A = P D P⁻¹ (pensado para autovalores reales positivos)."""
    w, P = np.linalg.eig(np.asarray(A, dtype=float))
    return np.real(P @ np.diag(w.astype(complex) ** t) @ np.linalg.inv(P))


def circulo(n=240):
    """Circunferencia unitaria como nube n×2 (una fila por punto), cerrada (el último punto repite el primero)."""
    t = np.linspace(0, 2 * np.pi, n)
    return np.column_stack([np.cos(t), np.sin(t)])


def pentagono_regular(R, n=5):
    """Vértices n×2 de un polígono regular de radio R, el primero arriba (sobre el eje +y), antihorario."""
    ang = 2 * np.pi * np.arange(n) / n + np.pi / 2
    return np.column_stack([R * np.cos(ang), R * np.sin(ang)])


def grilla_oblicua(u, v, k=4):
    """Segmentos de la grilla oblicua de la base {u, v}: paralelas a u por j·v y paralelas a v por j·u, |j| ≤ k.

    Devuelve un array (n, 2, 2): n segmentos, cada uno con sus dos extremos. No dibuja nada;
    para plotly, pasarlo por `segmentos_a_trazo`.
    """
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    segs = []
    for j in range(-k, k + 1):
        segs.append([j * v - k * u, j * v + k * u])  # paralela a u
        segs.append([j * u - k * v, j * u + k * v])  # paralela a v
    return np.array(segs)


def cerrar(poligono):
    """Agrega el primer vértice al final para dibujar el contorno cerrado."""
    poligono = np.asarray(poligono, dtype=float)
    return np.vstack([poligono, poligono[:1]])


def estelas(puntos, camino, transpuesta=False):
    """Trayectoria de cada punto a lo largo de un camino de matrices, como un trazo con cortes (xs, ys).

    Para rotaciones de 0 a θ es un arco; para un contraejemplo (de I a la matriz, en línea recta) es un segmento.
    transpuesta=True sigue Mᵀ p (rotación pasiva: las coordenadas en el sistema girado).
    """
    xs, ys = [], []
    for p in np.asarray(puntos, dtype=float):
        tray = np.array([(M.T if transpuesta else M) @ p for M in camino])
        xs += list(tray[:, 0]) + [None]
        ys += list(tray[:, 1]) + [None]
    return xs, ys


def segmentos_a_trazo(segmentos):
    """Array (n, 2, 2) de segmentos → (xs, ys) de un solo trazo plotly con cortes (None) entre segmentos."""
    xs, ys = [], []
    for (x0, y0), (x1, y1) in np.asarray(segmentos, dtype=float):
        xs += [x0, x1, None]
        ys += [y0, y1, None]
    return xs, ys


def coordenadas_en_base(p, B):
    """Coordenadas del punto p en la base dada por las COLUMNAS de B: el c tal que B c = p.

    Si B es una rotación R(θ) (los ejes girados θ), c = Rᵀ p: lo que anota quien mide con los ejes girados.
    """
    return np.linalg.solve(np.asarray(B, dtype=float), np.asarray(p, dtype=float))


def eje_angulo(R):
    """(eje unitario, ángulo en radianes ∈ [0, π]) de una rotación 3×3: la recta que R deja quieta y cuánto gira.

    El ángulo sale de la traza (tr R = 1 + 2 cos θ); el eje, de la parte antisimétrica (R − Rᵀ) o, si θ ≈ π,
    del autovector de autovalor 1. Para θ ≈ 0 devuelve el eje z por convención.
    """
    R = np.asarray(R, dtype=float)
    theta = float(np.arccos(np.clip((np.trace(R) - 1.0) / 2.0, -1.0, 1.0)))
    if theta < 1e-9:
        return np.array([0.0, 0.0, 1.0]), 0.0
    w = np.array([R[2, 1] - R[1, 2], R[0, 2] - R[2, 0], R[1, 0] - R[0, 1]])
    if np.linalg.norm(w) > 1e-6:
        return w / np.linalg.norm(w), theta
    vals, vecs = np.linalg.eig(R)  # θ ≈ π: R − Rᵀ ≈ 0, el eje es el autovector real de autovalor 1
    k = int(np.argmin(np.abs(vals - 1.0)))
    eje = np.real(vecs[:, k])
    return eje / np.linalg.norm(eje), theta


# ----------------------------------------------------------------------------
# LaTeX (KaTeX en mo.md)
# ----------------------------------------------------------------------------


def num_tex(x, dec=3):
    """Número → texto: enteros sin decimales, el resto con `dec` decimales (sin '-0.000')."""
    x = float(x)
    if abs(x - round(x)) < 1e-9:
        return str(int(round(x)))
    if abs(x) < 10 ** (-dec) / 2:
        x = 0.0
    return f"{x:.{dec}f}"


def vec_plano(v, dec=3):
    """Vector como texto plano "(1.964, 4.598)": para etiquetas de radio/dropdown, que no pasan por KaTeX."""
    return "(" + ", ".join(f"{float(x):.{dec}f}".rstrip("0").rstrip(".") for x in np.asarray(v).ravel()) + ")"


def vec_tex(v, dec=3):
    """Vector → '(a,\\ b,\\ c)' con el formato de num_tex."""
    return "(" + ",\\ ".join(num_tex(x, dec) for x in np.asarray(v).ravel()) + ")"


def pmat(M, dec=3):
    """Matriz (o vector) → pmatrix de LaTeX, enteros sin decimales."""
    filas = r" \\ ".join(" & ".join(num_tex(x, dec) for x in fila) for fila in np.atleast_2d(M))
    return r"\begin{pmatrix}" + filas + r"\end{pmatrix}"


def matriz_coloreada(M, dec=3, colores=COLORES):
    """pmatrix con cada columna pintada (\\textcolor) del color de su vector en la figura (teal, rust, gold)."""
    filas = []
    for fila in np.atleast_2d(M):
        celdas = []
        for i, x in enumerate(fila):
            x = 0.0 if abs(float(x)) < 10 ** (-dec) / 2 else float(x)  # evita el "-0.000"
            celdas.append(rf"\textcolor{{{colores[i % len(colores)]}}}{{{x:.{dec}f}}}")
        filas.append(" & ".join(celdas))
    return r"\begin{pmatrix}" + r" \\ ".join(filas) + r"\end{pmatrix}"


# ----------------------------------------------------------------------------
# plotly 2D
# ----------------------------------------------------------------------------


def _rango2(rango):
    """Un número r → (−r, r); una tupla (a, b) → (a, b)."""
    if np.isscalar(rango):
        return (-float(rango), float(rango))
    a, b = rango
    return (float(a), float(b))


def figura_plano(rango=5, titulo="", ancho=600, alto=600):
    """Figura 2D vacía con ejes iguales, grilla fina y el cero marcado. `rango` = semilado o (min, max)."""
    import plotly.graph_objects as go

    a, b = _rango2(rango)
    ejes = dict(range=[a, b], zeroline=True, zerolinecolor="#444", zerolinewidth=1.2,
                gridcolor="#eceae4", gridwidth=1, showgrid=True)
    fig = go.Figure(layout=go.Layout(
        width=ancho, height=alto, margin=dict(l=30, r=10, t=56, b=30),
        xaxis=dict(title="x", scaleanchor="y", scaleratio=1, **ejes),
        yaxis=dict(title="y", **ejes),
        legend=dict(orientation="h", y=-0.08, font=dict(size=10)),
        title=dict(text=titulo, font=dict(size=14), x=0.01, xanchor="left", y=0.985, yanchor="top"),
        plot_bgcolor="white",
    ))
    return fig


def grilla_segmentos(M, rango=5, paso=1):
    """Las líneas x = k, y = k (|k| ≤ semilado) transformadas por M, como un solo trazo con cortes: (xs, ys)."""
    a, b = _rango2(rango)
    M = np.asarray(M, dtype=float)
    ks = np.arange(np.ceil(a / paso) * paso, b + paso / 2, paso)
    xs, ys = [], []
    for k in ks:
        for seg in (np.array([[k, a], [k, b]]), np.array([[a, k], [b, k]])):
            seg_r = seg @ M.T
            xs += [seg_r[0, 0], seg_r[1, 0], None]
            ys += [seg_r[0, 1], seg_r[1, 1], None]
    return xs, ys


def _cuadrado_unitario():
    return np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)


def capa_antes(fig, rango=5, paso=1, cuadrado=True):
    """Capa gris: la grilla de referencia y (opcional) el cuadrado unitario original. Devuelve fig."""
    import plotly.graph_objects as go

    gx, gy = grilla_segmentos(np.eye(2), rango, paso)
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=GRIS_ANTES, width=1), opacity=0.5,
                             name="grilla antes", hoverinfo="skip"))
    if cuadrado:
        c = cerrar(_cuadrado_unitario())
        fig.add_trace(go.Scatter(x=c[:, 0], y=c[:, 1], mode="lines", fill="toself", fillcolor="rgba(154,160,166,0.25)",
                                 line=dict(color=GRIS_ANTES, width=2), name="cuadrado unitario antes"))
    return fig


def capa_despues(fig, M, rango=5, paso=1, cuadrado=True, columnas=True):
    """Capa teal: la grilla transformada por M, el cuadrado unitario transformado y las columnas como flechas. Devuelve fig."""
    import plotly.graph_objects as go

    M = np.asarray(M, dtype=float)
    gx, gy = grilla_segmentos(M, rango, paso)
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=TEAL_DESPUES, width=1), opacity=0.45,
                             name="grilla después", hoverinfo="skip"))
    if cuadrado:
        c = cerrar(transformar(_cuadrado_unitario(), M))
        fig.add_trace(go.Scatter(x=c[:, 0], y=c[:, 1], mode="lines", fill="toself", fillcolor="rgba(27,111,106,0.25)",
                                 line=dict(color=TEAL_DESPUES, width=2), name="cuadrado unitario después"))
    if columnas:
        flechas_columnas(fig, M)
    return fig


def objeto(fig, puntos, color=VIOLETA_OBJETO, nombre="objeto", estelas=None, relleno=True):
    """Polígono reconocible (N×2, se cierra solo) con marcadores; `estelas` = (xs, ys) de `estelas()`. Devuelve fig."""
    import plotly.graph_objects as go

    if estelas is not None:
        ex, ey = estelas
        fig.add_trace(go.Scatter(x=ex, y=ey, mode="lines", line=dict(color=color, width=1.5, dash="dot"),
                                 name=f"estelas de {nombre}", hoverinfo="skip"))
    p = cerrar(puntos)
    extra = dict(fill="toself", fillcolor=_rgba(color, 0.25)) if relleno else {}
    fig.add_trace(go.Scatter(x=p[:, 0], y=p[:, 1], mode="lines+markers", line=dict(color=color, width=2.5),
                             marker=dict(size=7), name=nombre, **extra))
    return fig


def flecha(fig, origen, destino, color=TEAL_DESPUES, nombre="", ancho=5):
    """Flecha 2D de origen a destino como trazo con punto en la punta (el patrón de 01). Devuelve fig."""
    import plotly.graph_objects as go

    o, d = np.asarray(origen, dtype=float), np.asarray(destino, dtype=float)
    fig.add_trace(go.Scatter(x=[o[0], d[0]], y=[o[1], d[1]], mode="lines+markers", line=dict(color=color, width=ancho),
                             marker=dict(size=[0, 2 * ancho], color=color), name=nombre, showlegend=bool(nombre)))
    return fig


_SUB = "₁₂₃₄"


def flechas_columnas(fig, M, nombre="M"):
    """Cada columna de M (2×2) como flecha desde el origen, del color de su columna ('columna k = M eₖ'). Devuelve fig."""
    M = np.asarray(M, dtype=float)
    for k in range(M.shape[1]):
        flecha(fig, (0, 0), M[:, k], color_columna(k), f"columna {k + 1} = {nombre} e{_SUB[k]}")
    return fig


def punto(fig, p, color=VIOLETA_OBJETO, nombre="punto", tam=12, texto=None):
    """Un solo punto 2D como marcador grande (el mojón que no se mueve), con etiqueta opcional. Devuelve fig."""
    import plotly.graph_objects as go

    p = np.asarray(p, dtype=float)
    fig.add_trace(go.Scatter(x=[p[0]], y=[p[1]], mode="markers+text" if texto else "markers", text=[texto or ""],
                             textposition="top right", textfont=dict(size=13, color=color),
                             marker=dict(size=tam, color=color, line=dict(color="white", width=1.5)), name=nombre))
    return fig


def lectura_coordenadas(fig, p, B, color=VIOLETA_OBJETO, nombre="lectura en los ejes girados"):
    """Cómo se leen las coordenadas de p sobre los ejes dados por las columnas de B: el camino punteado
    origen → c₁·b₁ → p (primero a lo largo del eje 1, después paralelo al eje 2). Devuelve fig."""
    import plotly.graph_objects as go

    B = np.asarray(B, dtype=float)
    p = np.asarray(p, dtype=float)
    c = coordenadas_en_base(p, B)
    codo = c[0] * B[:, 0]
    fig.add_trace(go.Scatter(x=[0, codo[0], p[0]], y=[0, codo[1], p[1]], mode="lines+markers",
                             line=dict(color=color, width=2, dash="dash"), marker=dict(size=[0, 6, 0], color=color),
                             name=nombre, hoverinfo="skip"))
    return fig


def animar(fig, cuadros, titulo=None, indices=None, duracion=50):
    """Agrega frames y los botones reproducir/pausa (arriba a la derecha, fuera del título). Devuelve fig.

    `cuadros`: lista de listas de trazas; cada lista reemplaza, en orden, las trazas de `indices`
    (default: las últimas len(cuadros[0]) trazas de fig.data, que son las dinámicas). El último cuadro
    tiene que coincidir con lo que muestra la figura quieta.
    """
    import plotly.graph_objects as go

    if indices is None:
        n = len(cuadros[0]) if cuadros else 0
        indices = list(range(len(fig.data) - n, len(fig.data)))
    fig.frames = [go.Frame(name=str(i), data=list(d), traces=list(indices)) for i, d in enumerate(cuadros)]
    layout = dict(
        margin=dict(t=56),
        updatemenus=[dict(
            type="buttons", showactive=False, direction="right", x=1.0, y=1.0, xanchor="right", yanchor="bottom",
            pad=dict(t=0, b=2),
            buttons=[
                dict(label="▶ reproducir", method="animate",
                     args=[None, dict(frame=dict(duration=duracion, redraw=True), fromcurrent=False, transition=dict(duration=0))]),
                dict(label="⏸ pausa", method="animate", args=[[None], dict(mode="immediate", frame=dict(duration=0))]),
            ],
        )],
    )
    if titulo is not None:
        layout["title"] = dict(text=titulo, font=dict(size=14), x=0.01, xanchor="left", y=0.985, yanchor="top")
    fig.update_layout(**layout)
    return fig


def _rgba(hexcolor, alpha):
    h = hexcolor.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return f"rgba({r},{g},{b},{alpha})"


# ----------------------------------------------------------------------------
# plotly 3D
# ----------------------------------------------------------------------------


def figura_espacio(rango=2.6, titulo="", ancho=640, alto=660):
    """Figura 3D vacía con los tres ejes dibujados, aspecto cúbico y cámara libre. `rango` = semilado o (min, max)."""
    import plotly.graph_objects as go

    a, b = _rango2(rango)
    L = 0.6 * max(abs(a), abs(b))
    ejes = [go.Scatter3d(x=[0, L * (i == 0)], y=[0, L * (i == 1)], z=[0, L * (i == 2)], mode="lines+text", text=["", n],
                         line=dict(color="#444", width=3), showlegend=False, hoverinfo="skip") for i, n in enumerate("xyz")]
    fig = go.Figure(data=ejes, layout=go.Layout(
        width=ancho, height=alto, margin=dict(l=0, r=0, t=30, b=0),
        scene=dict(xaxis=dict(range=[a, b]), yaxis=dict(range=[a, b]), zaxis=dict(range=[a, b]), aspectmode="cube"),
        legend=dict(orientation="h", y=-0.02, font=dict(size=10)),
        title=dict(text=titulo, font=dict(size=14)),
    ))
    return fig


def cubo_unitario():
    """(vertices 8×3, aristas): los vértices del cubo [0,1]³ y los 12 pares de índices que une una arista."""
    v = np.array([[x, y, z] for x in (0, 1) for y in (0, 1) for z in (0, 1)], dtype=float)
    aristas = [(a, b) for a in range(8) for b in range(a + 1, 8) if np.sum(np.abs(v[a] - v[b])) == 1]
    return v, aristas


def malla_pares(nx, ny=None):
    """Pares de índices (vecinos en fila y en columna) de una malla nx×ny de puntos numerados fila por fila."""
    ny = nx if ny is None else ny
    return [(i * ny + j, i * ny + j + 1) for i in range(nx) for j in range(ny - 1)] + [
        (i * ny + j, (i + 1) * ny + j) for i in range(nx - 1) for j in range(ny)
    ]


def terreno_suave(n=7, semilado=2.0, z0=-1.2):
    """Un terreno de ejemplo: (puntos n²×3 con alturas suaves, pares de la malla). Una fila por punto."""
    u = np.linspace(-semilado, semilado, n)
    X, Y = np.meshgrid(u, u)
    Z = 0.35 * np.sin(1.2 * X) * np.cos(0.9 * Y) + z0
    return np.column_stack([X.ravel(), Y.ravel(), Z.ravel()]), malla_pares(n)


def segmentos_3d(puntos, pares):
    """Un trazo con cortes (xs, ys, zs) que une los pares de índices dados (aristas, mallas)."""
    puntos = np.asarray(puntos, dtype=float)
    xs, ys, zs = [], [], []
    for a, b in pares:
        xs += [puntos[a, 0], puntos[b, 0], None]
        ys += [puntos[a, 1], puntos[b, 1], None]
        zs += [puntos[a, 2], puntos[b, 2], None]
    return xs, ys, zs


def flechas_columnas_3d(fig, M, nombre="R"):
    """Las columnas de M (3×3) como flechas desde el origen, del color de su columna. Devuelve fig."""
    import plotly.graph_objects as go

    M = np.asarray(M, dtype=float)
    for k in range(M.shape[1]):
        c = color_columna(k)
        fig.add_trace(go.Scatter3d(x=[0, M[0, k]], y=[0, M[1, k]], z=[0, M[2, k]], mode="lines+markers",
                                   line=dict(color=c, width=9), marker=dict(size=[0, 6], color=c),
                                   name=f"columna {k + 1} = {nombre} e{_SUB[k]}"))
    return fig


# ----------------------------------------------------------------------------
# verificación
# ----------------------------------------------------------------------------


def exacto(a, b, tol=1e-9):
    """True si a y b coinciden a menos de tol (np.allclose con atol=tol, rtol=0)."""
    return bool(np.allclose(np.asarray(a, dtype=float), np.asarray(b, dtype=float), atol=tol, rtol=0))


def verificar(checks):
    """Lista de (descripción, bool) → markdown con ✓/✗ por ítem y una línea final con el balance."""
    lineas = [f"- {'✓' if bool(ok) else '✗'} {texto}" for texto, ok in checks]
    fallas = sum(1 for _, ok in checks if not bool(ok))
    if not checks:
        final = "*Sin verificaciones.*"
    elif fallas == 0:
        final = f"**Todo verificado** ({len(checks)} de {len(checks)})."
    else:
        final = f"**{fallas} de {len(checks)} fallan.**"
    return "\n".join(lineas + ["", final])


# ----------------------------------------------------------------------------
# producto interno (lección 02): proyección, ángulo y el arco que lo marca
# ----------------------------------------------------------------------------


def proyeccion(v, u):
    """Proyección vectorial de v sobre u: la sombra de v sobre la recta de u, (⟨v,u⟩ / ⟨u,u⟩) u. u no puede ser nulo."""
    v = np.asarray(v, dtype=float)
    u = np.asarray(u, dtype=float)
    uu = float(u @ u)
    if uu == 0.0:
        raise ValueError("no se puede proyectar sobre el vector nulo")
    return (float(v @ u) / uu) * u


def angulo(v, u):
    """Ángulo entre v y u en radianes, en [0, π]: arccos(⟨v,u⟩ / (|v||u|)) con clip (sin clip, paralelos dan nan)."""
    v = np.asarray(v, dtype=float)
    u = np.asarray(u, dtype=float)
    nv, nu = np.linalg.norm(v), np.linalg.norm(u)
    if nv == 0.0 or nu == 0.0:
        raise ValueError("el ángulo con el vector nulo no está definido")
    return float(np.arccos(np.clip(float(v @ u) / (nv * nu), -1.0, 1.0)))


def arco_angulo(fig, u, v, radio=1.0, color="#444", nombre="ángulo", texto=None, n=40):
    """Arco de radio `radio` desde la dirección de u hasta la de v por el camino corto (|θ| ≤ π), con etiqueta
    opcional en el medio. Devuelve fig. Sólo 2D."""
    import plotly.graph_objects as go

    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    a0 = float(np.arctan2(u[1], u[0]))
    th = angulo(v, u)
    cruz = float(u[0] * v[1] - u[1] * v[0])
    if cruz < 0:  # v está del lado horario de u: el arco va para abajo
        th = -th
    t = np.linspace(a0, a0 + th, n)
    fig.add_trace(go.Scatter(x=radio * np.cos(t), y=radio * np.sin(t), mode="lines", line=dict(color=color, width=2),
                             name=nombre, showlegend=bool(nombre), hoverinfo="skip"))
    if texto:
        m = t[n // 2]
        fig.add_trace(go.Scatter(x=[1.3 * radio * np.cos(m)], y=[1.3 * radio * np.sin(m)], mode="text", text=[texto],
                                 textfont=dict(size=13, color=color), showlegend=False, hoverinfo="skip"))
    return fig


# ----------------------------------------------------------------------------
# afinidades F(x) = Ax + t (lección 04)
# ----------------------------------------------------------------------------


def transformar_afin(nube, A, t):
    """Nube N×2 bajo F(x) = Ax + t: nube @ A.T + t (una fila por punto)."""
    return transformar(nube, A) + np.asarray(t, dtype=float)


def matriz_afin(A, t):
    """F(x) = Ax + t como matriz homogénea 3×3 [[A, t], [0 0 1]]: la última columna es a dónde va el origen."""
    H = np.eye(3)
    H[:2, :2] = np.asarray(A, dtype=float)
    H[:2, 2] = np.asarray(t, dtype=float)
    return H


def partes_afin(H):
    """(A 2×2, t) de una homogénea afín 3×3 (se normaliza por H[2, 2]; la última fila tiene que ser (0 0 w))."""
    H = np.asarray(H, dtype=float) / float(H[2, 2])
    return H[:2, :2].copy(), H[:2, 2].copy()


def afin_por_tres_puntos(origen, destino):
    """(A, t) de la afinidad que lleva tres puntos no alineados (3×2) a otros tres (3×2).

    Dos sistemas 3×3 con la misma matriz hom(origen): uno da (a, b, e) con x' = ax + by + e,
    el otro (c, d, f) con y' = cx + dy + f. Es `np.linalg.solve(hom(origen), destino).T` = [A | t].
    """
    M = np.linalg.solve(hom(origen), np.asarray(destino, dtype=float)).T
    return M[:, :2], M[:, 2]


def capa_despues_afin(fig, A, t, rango=5, paso=1, cuadrado=True, columnas=True):
    """Capa teal de F(x) = Ax + t: grilla y cuadrado unitario transformados, y las columnas de A como flechas
    que salen de F(0) = t (a donde fue a parar el origen), más t en gold. Devuelve fig."""
    import plotly.graph_objects as go

    A = np.asarray(A, dtype=float)
    t = np.asarray(t, dtype=float)
    gx, gy = grilla_segmentos(A, rango, paso)
    gx = [None if x is None else x + t[0] for x in gx]
    gy = [None if y is None else y + t[1] for y in gy]
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=TEAL_DESPUES, width=1), opacity=0.45,
                             name="grilla después", hoverinfo="skip"))
    if cuadrado:
        c = cerrar(transformar_afin(_cuadrado_unitario(), A, t))
        fig.add_trace(go.Scatter(x=c[:, 0], y=c[:, 1], mode="lines", fill="toself", fillcolor="rgba(27,111,106,0.25)",
                                 line=dict(color=TEAL_DESPUES, width=2), name="cuadrado unitario después"))
    if columnas:
        for k in range(2):
            flecha(fig, t, t + A[:, k], color_columna(k), f"columna {k + 1} = A e{_SUB[k]} (desde F(0))")
        flecha(fig, (0, 0), t, color_columna(2), "columna 3 = F(0) = t")
    return fig


# ----------------------------------------------------------------------------
# cambio de base y diagonalización (lección 08)
# ----------------------------------------------------------------------------


def diagonalizar(A):
    """(autovalores, B) de una matriz con autovalores reales: λ ordenados de mayor a menor y, como columnas de B,
    los autovectores unitarios (primera componente no nula positiva), en el mismo orden. A = B diag(λ) B⁻¹.

    ValueError si hay autovalores complejos (una rotación: ningún eje propio) o si los autovectores son
    dependientes (una cizalla: un solo eje propio): en los dos casos no hay grilla propia con la que diagonalizar.
    """
    A = np.asarray(A, dtype=float)
    w, V = np.linalg.eig(A)
    if np.abs(np.imag(w)).max() > 1e-9:
        raise ValueError("autovalores complejos: no hay ejes propios reales")
    w, V = np.real(w), np.real(V)
    orden = np.argsort(-w, kind="stable")
    w, V = w[orden], V[:, orden].copy()
    for k in range(V.shape[1]):
        j = int(np.argmax(np.abs(V[:, k]) > 1e-12))
        if V[j, k] < 0:
            V[:, k] = -V[:, k]
    if abs(np.linalg.det(V)) < 1e-9:
        raise ValueError("autovectores dependientes: un solo eje propio, no se diagonaliza")
    return w, V


def capa_base(fig, B, k=4, nombre="B"):
    """Capa teal de una base: la grilla oblicua que generan las columnas de B (`grilla_oblicua`, |j| ≤ k) y las
    columnas como flechas (b₁ teal, b₂ rust: 'columna k = B eₖ'). Devuelve fig."""
    import plotly.graph_objects as go

    B = np.asarray(B, dtype=float)
    gx, gy = segmentos_a_trazo(grilla_oblicua(B[:, 0], B[:, 1], k))
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=TEAL_DESPUES, width=1), opacity=0.45,
                             name="grilla de la base nueva", hoverinfo="skip"))
    flechas_columnas(fig, B, nombre)
    return fig


def capa_ejes_propios(fig, A, rango=5):
    """Los ejes propios de A (vía `diagonalizar`): por cada autovector real, la recta por el origen (punteada), la
    flecha bₖ del color de la columna k y un rombo en A bₖ = λₖ bₖ, sobre la misma recta. Devuelve fig."""
    import plotly.graph_objects as go

    lam, B = diagonalizar(A)
    a, b = _rango2(rango)
    L = 1.5 * max(abs(a), abs(b))
    for k in range(B.shape[1]):
        v, c = B[:, k], color_columna(k)
        fig.add_trace(go.Scatter(x=[-L * v[0], L * v[0]], y=[-L * v[1], L * v[1]], mode="lines",
                                 line=dict(color=c, width=1.5, dash="dash"), hoverinfo="skip",
                                 name=f"eje propio {k + 1} (λ{_SUB[k]} = {num_tex(lam[k])})"))
        flecha(fig, (0, 0), v, c, f"b{_SUB[k]} (autovector)", ancho=3)
        q = lam[k] * v
        fig.add_trace(go.Scatter(x=[q[0]], y=[q[1]], mode="markers", marker=dict(size=10, color=c, symbol="diamond"),
                                 name=f"A b{_SUB[k]} = {num_tex(lam[k])} b{_SUB[k]}"))
    return fig


# ----------------------------------------------------------------------------
# cuña, núcleo y autovectores (lecciones 07a, 07b, 07c)
# ----------------------------------------------------------------------------


def cuna2(u, v):
    """Producto cuña en el plano: u ∧ v = u₁v₂ − u₂v₁, el área ORIENTADA del paralelogramo de lados u y v
    (= det[u v] con u, v como columnas). Positiva si de u a v se gira antihorario; cero si y sólo si son
    colineales: el "detector de colinealidad" del profesor."""
    u = np.asarray(u, dtype=float).reshape(2)
    v = np.asarray(v, dtype=float).reshape(2)
    return float(u[0] * v[1] - u[1] * v[0])


def cuna3(u, v, w):
    """(u ∧ v) ∧ w = (u × v) · w = det[u v w]: volumen orientado del paralelepípedo. Cero si los tres son coplanares."""
    u, v, w = (np.asarray(x, dtype=float).reshape(3) for x in (u, v, w))
    return float(np.cross(u, v) @ w)


def alineados(p, q, r, tol=1e-9):
    """True si los tres puntos del plano están alineados: el determinante de sus ternas homogéneas es cero
    (equivale a cuna2(q − p, r − p) = 0, el área del triángulo pqr es cero)."""
    return abs(float(np.linalg.det(np.array([hom(p), hom(q), hom(r)])))) < tol


def paralelogramo(u, v):
    """Vértices 4×2 del paralelogramo de lados u y v desde el origen (0, u, u + v, v), para `objeto`."""
    u = np.asarray(u, dtype=float).reshape(2)
    v = np.asarray(v, dtype=float).reshape(2)
    return np.array([[0.0, 0.0], u, u + v, v])


def paralelepipedo(u, v, w):
    """(vértices 8×3, aristas) del paralelepípedo de lados u, v, w: el cubo unitario transformado por [u v w]."""
    c, aristas = cubo_unitario()
    return transformar(c, np.column_stack([u, v, w])), aristas


def plano_3d(fig, u, v, k=1.5, origen=(0, 0, 0), color=GRIS_ANTES, nombre="plano", opacidad=0.18):
    """Trozo del plano por `origen` generado por u y v (el paralelogramo ±k u ± k v) como malla translúcida. Devuelve fig."""
    import plotly.graph_objects as go

    o = np.asarray(origen, dtype=float).reshape(3)
    u = np.asarray(u, dtype=float).reshape(3)
    v = np.asarray(v, dtype=float).reshape(3)
    p = np.array([o - k * u - k * v, o + k * u - k * v, o + k * u + k * v, o - k * u + k * v])
    fig.add_trace(go.Mesh3d(x=p[:, 0], y=p[:, 1], z=p[:, 2], i=[0, 0], j=[1, 2], k=[2, 3], color=color,
                            opacity=opacidad, name=nombre, showlegend=True, hoverinfo="skip"))
    return fig


def nucleo2(A, tol=1e-9):
    """Un vector no nulo del núcleo de una 2×2 singular: la perpendicular (perp2) a la primera fila no nula.
    Si A = 0 devuelve e₁ (todo el plano es núcleo). Si det A ≠ 0 lanza ValueError: el núcleo es sólo {0}."""
    A = np.asarray(A, dtype=float)
    if abs(np.linalg.det(A)) > tol * max(1.0, float(np.abs(A).max()) ** 2):
        raise ValueError("det A ≠ 0: el núcleo es sólo el vector nulo")
    normas = np.linalg.norm(A, axis=1)
    if normas.max() < tol:
        return np.array([1.0, 0.0])
    return perp2(A[0] if normas[0] >= tol else A[1])  # la primera fila no nula


def autovalores_reales(A, tol=1e-7):
    """Raíces reales de det(A − λI), sin repetir, de mayor a menor. Las complejas se descartan: no dan vectores reales."""
    w = np.linalg.eigvals(np.asarray(A, dtype=float))
    reales = sorted({round(float(z.real), 6) for z in w if abs(z.imag) < tol}, reverse=True)
    return [float(x) for x in reales]


def autovectores_cuna(A, tol=1e-7):
    """Autovalores reales y autovectores por el método del profesor ("la cruz de dos filas").

    Para cada raíz real λ de det(A − λI), las filas de B = A − λI son reglas que marcan cero sobre el autovector:
    en 3×3 el autovector es el producto cruz de dos filas de B (el par que no da cero); en 2×2, la perpendicular a
    una fila no nula. Si todos los pares dan cero, el núcleo de B es un plano entero (raíz doble: `plano=True`).
    Devuelve una lista de dicts {lam, B, filas, cruz, v, plano}; v se escala para que su mayor componente valga 1.
    """
    A = np.asarray(A, dtype=float)
    n = A.shape[0]
    salida = []
    for lam in autovalores_reales(A, tol):
        B = A - lam * np.eye(n)
        escala = max(1.0, float(np.abs(B).max()))
        if n == 2:
            normas = np.linalg.norm(B, axis=1)
            i = int(np.argmax(normas))
            if normas[i] < tol * escala:
                salida.append(dict(lam=lam, B=B, filas=(), cruz=None, v=None, plano=True))
                continue
            c = perp2(B[i])
            filas = (i,)
        else:
            mejor = None
            for i, j in ((0, 1), (0, 2), (1, 2)):
                c = np.cross(B[i], B[j])
                if mejor is None or np.linalg.norm(c) > np.linalg.norm(mejor[1]):
                    mejor = ((i, j), c)
            filas, c = mejor
            if np.linalg.norm(c) < tol * escala ** 2:
                salida.append(dict(lam=lam, B=B, filas=(), cruz=None, v=None, plano=True))
                continue
        v = c / float(np.abs(c).max())
        salida.append(dict(lam=lam, B=B, filas=filas, cruz=c, v=np.where(np.abs(v) < 1e-12, 0.0, v), plano=False))
    return salida


def direcciones_propias(fig, A, rango=5, color="#222", nombre="dirección propia"):
    """Capa de direcciones propias de una 2×2: por cada autovalor real, la recta por el origen del autovector
    (trazo a rayas) y la flecha λ·v̂ que muestra cuánto se estira (o se invierte). Un giro (sin reales) o una
    homotecia (plano entero) no dibujan nada. Devuelve la lista de `autovectores_cuna(A)`."""
    import plotly.graph_objects as go

    a, b = _rango2(rango)
    L = 1.5 * max(abs(a), abs(b))
    info = autovectores_cuna(A)
    for inf in info:
        if inf["plano"]:
            continue
        d = inf["v"] / np.linalg.norm(inf["v"])
        fig.add_trace(go.Scatter(x=[-L * d[0], L * d[0]], y=[-L * d[1], L * d[1]], mode="lines",
                                 line=dict(color=color, width=1.5, dash="dash"),
                                 name=f"{nombre} λ = {num_tex(inf['lam'], 2)}: {vec_plano(inf['v'], 2)}", hoverinfo="skip"))
        flecha(fig, (0, 0), inf["lam"] * d, color, f"λ·v̂ con λ = {num_tex(inf['lam'], 2)}", ancho=4)
    return info


def puntos_fijos_proyectivos(H, tol=1e-7):
    """Los autovectores reales de una 3×3 homogénea leídos como puntos del plano. Lista de dicts
    {lam, v, punto, plano, recta, filas}: `punto` = (x, y) = (v₁/v₃, v₂/v₃) si v₃ ≠ 0, None si es impropio (dirección
    fija); si el autovector es un plano entero (raíz doble con cruces nulas), `plano=True` y `recta` es la terna
    de la recta de puntos fijos (una fila no nula de H − λI)."""
    salida = []
    for inf in autovectores_cuna(H, tol):
        if inf["plano"]:
            B = inf["B"]
            fila = B[int(np.argmax(np.linalg.norm(B, axis=1)))]
            recta = fila / float(np.abs(fila).max()) if np.abs(fila).max() > 0 else None
            salida.append(dict(lam=inf["lam"], v=None, punto=None, plano=True, recta=recta, filas=()))
            continue
        salida.append(dict(lam=inf["lam"], v=inf["v"], punto=dehom(inf["v"]), plano=False, recta=None, filas=inf["filas"]))
    return salida


# ----------------------------------------------------------------------------
# jacobiano y primera forma fundamental (lección 10)
# ----------------------------------------------------------------------------


def xyz(x, y, z):
    """Tres componentes (escalares o arrays que broadcastean) → un array (..., 3): para escribir una superficie
    r(u, v) vectorizada en una línea. Con u, v escalares devuelve (3,); con arrays de n, (n, 3)."""
    return np.stack(np.broadcast_arrays(np.asarray(x, dtype=float), np.asarray(y, dtype=float),
                                        np.asarray(z, dtype=float)), axis=-1)


def jacobiana_numerica(r, u, v, h=1e-6):
    """Jacobiana m×2 de r(u, v) → array de m, por diferencias finitas centradas: columnas r_u, r_v.

    Es la matriz que manda un pasito (du, dv) de la grilla al pasito r_u du + r_v dv sobre la superficie; sus
    columnas son los ejes locales en el punto. Para h chico coincide con la derivada exacta (error ~h²).
    """
    r_u = (np.asarray(r(u + h, v), dtype=float) - np.asarray(r(u - h, v), dtype=float)) / (2 * h)
    r_v = (np.asarray(r(u, v + h), dtype=float) - np.asarray(r(u, v - h), dtype=float)) / (2 * h)
    return np.column_stack([r_u, r_v])


def primera_forma(J):
    """(E, F, G) de una jacobiana m×2: la tabla de productos internos de los ejes locales, g = Jᵀ J = [[E, F], [F, G]]
    con E = ⟨r_u, r_u⟩, F = ⟨r_u, r_v⟩, G = ⟨r_v, r_v⟩ (la V Vᵀ de la lección 02, con los ejes como columnas)."""
    J = np.asarray(J, dtype=float)
    g = J.T @ J
    return float(g[0, 0]), float(g[0, 1]), float(g[1, 1])


def longitud_paso(E, F, G, du, dv):
    """Largo sobre la superficie de un pasito (du, dv) de la grilla, a primer orden: √(E du² + 2F du dv + G dv²).
    du, dv pueden ser arrays (una nube de pasos → una longitud por paso)."""
    du = np.asarray(du, dtype=float)
    dv = np.asarray(dv, dtype=float)
    return np.sqrt(E * du**2 + 2 * F * du * dv + G * dv**2)


def longitud_poligonal(puntos):
    """Largo de la poligonal que une los puntos N×d en orden (suma de los tramos): medir "con cinta" un camino."""
    p = np.asarray(puntos, dtype=float)
    return float(np.sum(np.linalg.norm(np.diff(p, axis=0), axis=1)))


def flecha_3d(fig, origen, destino, color=TEAL_DESPUES, nombre="", ancho=8):
    """Flecha 3D de origen a destino como trazo con punto en la punta (el patrón de `flechas_columnas_3d`). Devuelve fig."""
    import plotly.graph_objects as go

    o, d = np.asarray(origen, dtype=float).reshape(3), np.asarray(destino, dtype=float).reshape(3)
    fig.add_trace(go.Scatter3d(x=[o[0], d[0]], y=[o[1], d[1]], z=[o[2], d[2]], mode="lines+markers",
                               line=dict(color=color, width=ancho), marker=dict(size=[0, 5], color=color),
                               name=nombre, showlegend=bool(nombre)))
    return fig


def superficie_malla(fig, r, us, vs, color=TEAL_DESPUES, nombre="superficie", fino=40, ancho=2, opacidad=0.8):
    """La grilla (u, v) dibujada sobre la superficie r(u, v): las líneas coordenadas u = cte (una por valor de `us`) y
    v = cte (una por valor de `vs`), cada una muestreada con `fino` puntos para que se curve, como un solo trazo con
    cortes. `r` tiene que aceptar arrays (vectorizada, ver `xyz`) y devolver (..., 3). Con un r plano
    (u, v) ↦ (u, v, z₀) dibuja la grilla "antes". Devuelve fig."""
    import plotly.graph_objects as go

    us, vs = np.asarray(us, dtype=float), np.asarray(vs, dtype=float)
    uf, vf = np.linspace(us[0], us[-1], fino), np.linspace(vs[0], vs[-1], fino)
    xs, ys, zs = [], [], []
    for u in us:  # línea u = cte: recorre v
        P = np.asarray(r(np.full(fino, u), vf), dtype=float)
        xs += list(P[:, 0]) + [None]
        ys += list(P[:, 1]) + [None]
        zs += list(P[:, 2]) + [None]
    for v in vs:  # línea v = cte: recorre u
        P = np.asarray(r(uf, np.full(fino, v)), dtype=float)
        xs += list(P[:, 0]) + [None]
        ys += list(P[:, 1]) + [None]
        zs += list(P[:, 2]) + [None]
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=ancho), opacity=opacidad,
                               name=nombre, hoverinfo="skip"))
    return fig


def plano_tangente(fig, p, ru, rv, k=0.6, normal=True):
    """El plano tangente en p (trozo ±k r_u ± k r_v, con `plano_3d`) y los ejes locales como flechas desde p: r_u teal
    (columna 1 de J) y r_v rust (columna 2); opcional, la normal r_u × r_v normalizada, en gris oscuro: la dirección
    inaccesible. Devuelve fig."""
    p = np.asarray(p, dtype=float).reshape(3)
    ru = np.asarray(ru, dtype=float).reshape(3)
    rv = np.asarray(rv, dtype=float).reshape(3)
    plano_3d(fig, ru, rv, k, origen=p, color=TEAL_DESPUES, nombre="plano tangente", opacidad=0.22)
    flecha_3d(fig, p, p + ru, color_columna(0), "r_u = columna 1 de J")
    flecha_3d(fig, p, p + rv, color_columna(1), "r_v = columna 2 de J")
    if normal:
        n = np.cross(ru, rv)
        if np.linalg.norm(n) > 1e-12:
            flecha_3d(fig, p, p + n / np.linalg.norm(n), "#444", "normal r_u × r_v (lo inaccesible)", ancho=4)
    return fig


# ----------------------------------------------------------------------------
# mínimos cuadrados: los cuatro problemas (lección 11)   # lección 11 / 14 (cb104)
# ----------------------------------------------------------------------------


def minimos_cuadrados(A, y):
    """Solución de A x ≈ y con más ecuaciones que incógnitas, por ecuaciones normales AᵀA x = Aᵀy. Devuelve (x, r)
    con r = y − A x el residuo, que queda perpendicular a todo lo que A puede producir: Aᵀ r = 0. Las columnas de A
    tienen que ser independientes (si no, AᵀA es singular y no hay una sola solución)."""
    A = np.asarray(A, dtype=float)
    y = np.asarray(y, dtype=float).reshape(-1)
    x = np.linalg.solve(A.T @ A, A.T @ y)
    return x, y - A @ x


def recta_ajuste(xs, ys):
    """(a, b) de la recta y = a x + b que minimiza las distancias VERTICALES a los puntos: A = [xs | 1], mínimos cuadrados."""
    xs = np.asarray(xs, dtype=float).reshape(-1)
    return minimos_cuadrados(np.column_stack([xs, np.ones(len(xs))]), ys)[0]


def punto_por_distancias(mojones, distancias):
    """Punto p = (x, y) a las distancias dadas de m ≥ 3 mojones conocidos (m×2). Restar la ecuación del primer círculo
    a las demás cancela x² + y² y deja m − 1 rectas (los ejes radicales): 2 (Mᵢ − M₀)·p = d₀² − dᵢ² − |M₀|² + |Mᵢ|².
    Con tres mojones es un sistema 2×2 exacto; con más, mínimos cuadrados. Devuelve (p, r), r el residuo de esas rectas."""
    M = np.asarray(mojones, dtype=float)
    d = np.asarray(distancias, dtype=float).reshape(-1)
    if len(M) < 3:
        raise ValueError("hacen falta al menos tres mojones: con dos quedan dos candidatos simétricos")
    A = 2.0 * (M[1:] - M[0])
    b = d[0] ** 2 - d[1:] ** 2 - M[0] @ M[0] + np.sum(M[1:] ** 2, axis=1)
    return minimos_cuadrados(A, b)


def procrustes(P, Q):
    """Rotación R, escala s y traslación t que mejor superponen la nube P (N×2) sobre Q (N×2): qᵢ ≈ s R pᵢ + t.
    Se centran las dos nubes, H = P₀ᵀ Q₀ (la covarianza cruzada), H = U Σ Vᵀ y R = V Uᵀ (si saliera un espejo se corrige
    el signo), s = tr Σ / ‖P₀‖², t = q̄ − s R p̄. Devuelve (R, s, t, rms), rms la raíz del residuo cuadrático medio."""
    P = np.asarray(P, dtype=float)
    Q = np.asarray(Q, dtype=float)
    pm, qm = P.mean(axis=0), Q.mean(axis=0)
    P0, Q0 = P - pm, Q - qm
    U, S, Vt = np.linalg.svd(P0.T @ Q0)
    D = np.diag([1.0, float(np.sign(np.linalg.det(Vt.T @ U.T)))])
    R = Vt.T @ D @ U.T
    s = float(np.trace(np.diag(S) @ D)) / float(np.sum(P0 ** 2))
    t = qm - s * R @ pm
    rms = float(np.sqrt(np.mean(np.sum((s * transformar(P, R) + t - Q) ** 2, axis=1))))
    return R, s, t, rms


def regresion_total(puntos):
    """Recta que minimiza las distancias PERPENDICULARES a una nube N×2: pasa por el centroide c con la dirección d
    propia de mayor autovalor de la covarianza C = X₀ᵀ X₀ (X₀ = puntos − c); la normal n = perp2(d) es la de menor
    autovalor, y ese autovalor es la suma de los residuos al cuadrado. Devuelve (c, d, n, residuo2)."""
    X = np.asarray(puntos, dtype=float)
    c = X.mean(axis=0)
    X0 = X - c
    lam, V = np.linalg.eigh(X0.T @ X0)  # ascendente
    d = V[:, 1] if V[0, 1] > 0 or (V[0, 1] == 0 and V[1, 1] > 0) else -V[:, 1]
    return c, d, perp2(d), float(lam[0])


# ----------------------------------------------------------------------------
# trigonometría esférica (lección 14)
# ----------------------------------------------------------------------------


def punto_esfera(phi, lam, R=1.0):
    """Vector (x, y, z) del punto de latitud phi (desde el ecuador) y longitud lam, en radianes, sobre la esfera de radio R.
    Acepta arrays en phi o en lam (devuelve 3×n)."""
    return R * np.array([np.cos(phi) * np.cos(lam), np.cos(phi) * np.sin(lam), np.sin(phi) * np.ones_like(lam)])


def esfera_malla(fig, R=1.0, paso=30, color=GRIS_ANTES, nombre="esfera"):
    """Meridianos y paralelos cada `paso` grados de la esfera de radio R, como un solo trazo gris con cortes. Devuelve fig."""
    import plotly.graph_objects as go

    xs, ys, zs = [], [], []
    t = np.linspace(-np.pi / 2, np.pi / 2, 61)
    for lam in np.deg2rad(np.arange(0, 360, paso)):
        p = punto_esfera(t, lam, R)
        xs += list(p[0]) + [None]
        ys += list(p[1]) + [None]
        zs += list(p[2]) + [None]
    u = np.linspace(0, 2 * np.pi, 121)
    for phi in np.deg2rad(np.arange(-90 + paso, 90, paso)):
        p = punto_esfera(phi, u, R)
        xs += list(p[0]) + [None]
        ys += list(p[1]) + [None]
        zs += list(p[2]) + [None]
    fig.add_trace(go.Scatter3d(x=xs, y=ys, z=zs, mode="lines", line=dict(color=color, width=1), opacity=0.5,
                               name=nombre, hoverinfo="skip"))
    return fig


def arco_maximo(p, q, n=60):
    """Puntos n×3 del arco corto de círculo máximo entre p y q (mismo radio): interpolación sobre la esfera.
    p y q no pueden ser antípodas (habría infinitos arcos)."""
    p = np.asarray(p, dtype=float).reshape(3)
    q = np.asarray(q, dtype=float).reshape(3)
    R = np.linalg.norm(p)
    u, v = p / R, q / np.linalg.norm(q)
    th = angulo(u, v)
    if th < 1e-12:
        return np.tile(p, (n, 1))
    if np.pi - th < 1e-9:
        raise ValueError("puntos antípodas: el círculo máximo no es único")
    t = np.linspace(0, 1, n)[:, None]
    return R * (np.sin((1 - t) * th) * u + np.sin(t * th) * v) / np.sin(th)


def lado_esferico(p, q):
    """Lado del triángulo esférico entre los vértices p y q: el ángulo central, en radianes (arccos del producto interno
    de los unitarios, con clip). Sobre la esfera de radio R el arco mide R veces esto."""
    return angulo(p, q)


def angulo_esferico(a, b, c):
    """Ángulo A opuesto al lado a, en radianes, por la ley del coseno esférica: cos a = cos b cos c + sin b sin c cos A."""
    sbsc = float(np.sin(b) * np.sin(c))
    if abs(sbsc) < 1e-12:
        raise ValueError("un lado nulo (o de 180°): el ángulo en ese vértice no está definido")
    return float(np.arccos(np.clip((np.cos(a) - np.cos(b) * np.cos(c)) / sbsc, -1.0, 1.0)))


def angulo_vertice(A, B, C):
    """Ángulo en el vértice A del triángulo esférico ABC, en radianes, directo de los vectores: es el ángulo entre las
    normales A × B y A × C de los dos planos por el centro; con sin b sin c sin A = |(A ∧ B) ∧ C| (la cuña, lección 07a)
    y sin b sin c cos A = (A × B)·(A × C) sale A = arctan2(·, ·), sin cancelaciones para triángulos chicos."""
    A, B, C = (np.asarray(v, dtype=float).reshape(3) / np.linalg.norm(v) for v in (A, B, C))
    nb, nc = np.cross(A, B), np.cross(A, C)
    return float(np.arctan2(abs(cuna3(A, B, C)), float(nb @ nc)))


def triangulo_esferico(A, B, C):
    """Lados y ángulos (radianes) del triángulo esférico de vértices A, B, C (vectores desde el centro): devuelve
    ((a, b, c), (α, β, γ)) con a el lado opuesto a A (ángulo entre B y C) y α el ángulo en A."""
    lados = (lado_esferico(B, C), lado_esferico(A, C), lado_esferico(A, B))
    return lados, (angulo_vertice(A, B, C), angulo_vertice(B, C, A), angulo_vertice(C, A, B))


def exceso_esferico(A, B, C):
    """Exceso esférico α + β + γ − π del triángulo de vértices A, B, C: su área dividida por R² (Girard)."""
    return float(sum(triangulo_esferico(A, B, C)[1]) - np.pi)


# ----------------------------------------------------------------------------
# curvatura: primera y segunda forma fundamental (lección 12)
# ----------------------------------------------------------------------------


def formas_fundamentales(r, u, v, h=1e-3):
    """Primera y segunda forma fundamental de la superficie r(u, v) (función de dos números → array de 3) en el
    punto (u, v), por diferencias finitas centradas de paso h. Devuelve un dict con p = r(u, v); r_u, r_v (la base
    local); n (normal unitaria r_u × r_v / ‖r_u × r_v‖); E, F, G (primera forma: la regla de la lección 10) y
    L, M, N (segunda forma: cuánto se aparta la superficie del plano tangente, r_uu·n, r_uv·n, r_vv·n).
    La curvatura es positiva cuando la superficie se dobla hacia n. Para un gráfico z = f(x, y) usar
    r = lambda x, y: np.array([x, y, f(x, y)]); ahí n apunta hacia arriba."""
    def R(a, b):
        return np.asarray(r(a, b), dtype=float).reshape(3)

    p = R(u, v)
    r_u = (R(u + h, v) - R(u - h, v)) / (2 * h)
    r_v = (R(u, v + h) - R(u, v - h)) / (2 * h)
    r_uu = (R(u + h, v) - 2 * p + R(u - h, v)) / h**2
    r_vv = (R(u, v + h) - 2 * p + R(u, v - h)) / h**2
    r_uv = (R(u + h, v + h) - R(u + h, v - h) - R(u - h, v + h) + R(u - h, v - h)) / (4 * h**2)
    n = np.cross(r_u, r_v)
    norma = np.linalg.norm(n)
    if norma < 1e-12:
        raise ValueError("r_u y r_v son paralelos: no hay plano tangente (punto singular de la parametrización)")
    n = n / norma
    return dict(p=p, r_u=r_u, r_v=r_v, n=n, E=float(r_u @ r_u), F=float(r_u @ r_v), G=float(r_v @ r_v),
                L=float(r_uu @ n), M=float(r_uv @ n), N=float(r_vv @ n))


def curvatura_normal(E, F, G, L, M, N, du, dv):
    """Curvatura normal en el rumbo (du, dv) del plano de parámetros: II(d, d) / I(d, d), cociente de las dos formas
    cuadráticas. No depende del largo de (du, dv). Es 1/radio del círculo osculador de la sección normal."""
    return float((L * du**2 + 2 * M * du * dv + N * dv**2) / (E * du**2 + 2 * F * du * dv + G * dv**2))


def curvaturas_principales(E, F, G, L, M, N):
    """(κ₁, κ₂, D): curvaturas principales, κ₁ ≥ κ₂, y direcciones principales como columnas de D en coordenadas
    (du, dv), normalizadas con la primera forma (I(d, d) = 1). Son los autovalores y autovectores de S = I⁻¹ II
    (`solve(I, II)`): el máximo y el mínimo de II(d, d) entre los rumbos con I(d, d) = 1. Si F = M = 0, S ya es
    diagonal y las direcciones principales son las líneas de la grilla. Punto umbilical (esfera): κ₁ = κ₂."""
    I = np.array([[E, F], [F, G]], dtype=float)
    II = np.array([[L, M], [M, N]], dtype=float)
    w, V = np.linalg.eig(np.linalg.solve(I, II))
    w, V = np.real(w), np.real(V)
    orden = np.argsort(-w, kind="stable")
    w, V = w[orden], V[:, orden].copy()
    for k in range(2):
        V[:, k] /= np.sqrt(V[:, k] @ I @ V[:, k])
        j = int(np.argmax(np.abs(V[:, k]) > 1e-12))
        if V[j, k] < 0:
            V[:, k] = -V[:, k]
    return float(w[0]), float(w[1]), V


def curvatura_gauss(E, F, G, L, M, N):
    """(K, H): curvatura de Gauss K = det II / det I = κ₁ κ₂ y curvatura media H = (κ₁ + κ₂)/2."""
    det_I = E * G - F**2
    return float((L * N - M**2) / det_I), float((E * N - 2 * F * M + G * L) / (2 * det_I))


def seccion_normal(f, p, t, n, largo=1.0, m=41, iteraciones=12):
    """Sección normal de un gráfico z = f(x, y) (f vectorizada) en el punto p por la dirección tangente unitaria t:
    la curva en que el plano p + s t + w n corta a la superficie, s ∈ [−largo, largo]. Para cada s se resuelve w
    por Newton con derivada numérica. Devuelve m×3 (nan donde f no está definida)."""
    p, t, n = (np.asarray(x, dtype=float).reshape(3) for x in (p, t, n))
    s = np.linspace(-largo, largo, m)
    w = np.zeros(m)

    def g(w):
        q = p + np.outer(s, t) + np.outer(w, n)
        return q[:, 2] - f(q[:, 0], q[:, 1])

    with np.errstate(all="ignore"):
        for _ in range(iteraciones):
            gw = g(w)
            w = w - gw / ((g(w + 1e-6) - gw) / 1e-6)
    return p + np.outer(s, t) + np.outer(w, n)


def circulo_3d(centro, u, v, radio, m=73):
    """Circunferencia m×3 de centro `centro` y radio `radio` en el plano generado por u y v (unitarios, perpendiculares)."""
    th = np.linspace(0, 2 * np.pi, m)
    c, u, v = (np.asarray(x, dtype=float).reshape(3) for x in (centro, u, v))
    return c + radio * (np.outer(np.cos(th), u) + np.outer(np.sin(th), v))




# ----------------------------------------------------------------------------
# elipsoide de revolución (lección 13): ángulos en radianes, longitudes en las unidades de a
# ----------------------------------------------------------------------------


def elipsoide(a, f):
    """Parámetros del elipsoide de revolución de semieje mayor a y aplastamiento f = (a − b)/a: dict con a, f, b,
    e2 (primera excentricidad al cuadrado, e² = (a² − b²)/a² = 2f − f²) y ep2 (segunda, e'² = (a² − b²)/b²).
    f = 0 es la esfera. Notación del apunte del profesor (Clavijo, Geometría del Elipsoide)."""
    a, f = float(a), float(f)
    e2 = 2 * f - f**2
    return dict(a=a, f=f, b=a * (1 - f), e2=e2, ep2=e2 / (1 - e2))


def elipsoide_grs80():
    """GRS80: a = 6378137 m, 1/f = 298.257222101 (e² ≈ 0.00669438)."""
    return elipsoide(6378137.0, 1 / 298.257222101)


_GRS80 = elipsoide_grs80()


def radios_curvatura(phi, a=_GRS80["a"], e2=_GRS80["e2"]):
    """(M, N) en la latitud geodésica phi (radianes): M = a(1 − e²)/(1 − e² sin²φ)^{3/2}, radio de curvatura del
    meridiano; N = a/√(1 − e² sin²φ), radio de curvatura del primer vertical y distancia del punto al eje polar
    medida a lo largo de la normal. M ≤ N; iguales en los polos; en el ecuador M = b²/a y N = a. Vectorizado."""
    w = np.sqrt(1 - e2 * np.sin(np.asarray(phi, dtype=float)) ** 2)
    return a * (1 - e2) / w**3, a / w


def latitudes(phi, e2=_GRS80["e2"]):
    """(ψ, β): latitud geocéntrica y reducida a partir de la geodésica φ (radianes): tan ψ = (1 − e²) tan φ,
    tan β = √(1 − e²) tan φ. En módulo ψ ≤ β ≤ φ; coinciden en el ecuador y en los polos. Vectorizado."""
    phi = np.asarray(phi, dtype=float)
    psi = np.arctan2((1 - e2) * np.sin(phi), np.cos(phi))
    beta = np.arctan2(np.sqrt(1 - e2) * np.sin(phi), np.cos(phi))
    return psi, beta


def geodesica_a_cartesiana(phi, lam, h=0.0, a=_GRS80["a"], e2=_GRS80["e2"]):
    """(φ, λ, h) → (X, Y, Z) cartesianas geocéntricas: X = (N + h) cos φ cos λ, Y = (N + h) cos φ sin λ,
    Z = (N(1 − e²) + h) sin φ, con N el radio del primer vertical y h la altura sobre la normal. Radianes.
    Vectorizado: devuelve un array (..., 3), una terna por punto."""
    phi, lam, h = np.broadcast_arrays(np.asarray(phi, dtype=float), np.asarray(lam, dtype=float), np.asarray(h, dtype=float))
    N = a / np.sqrt(1 - e2 * np.sin(phi) ** 2)
    return np.stack([(N + h) * np.cos(phi) * np.cos(lam), (N + h) * np.cos(phi) * np.sin(lam), (N * (1 - e2) + h) * np.sin(phi)], axis=-1)


def normal_elipsoide(phi, lam):
    """Normal unitaria al elipsoide (la vertical elipsoidal) en (φ, λ): (cos φ cos λ, cos φ sin λ, sin φ). Es la
    definición de la latitud geodésica: el ángulo de esa normal con el plano del ecuador."""
    return np.array([np.cos(phi) * np.cos(lam), np.cos(phi) * np.sin(lam), np.sin(phi)], dtype=float)


def gms(grados, dec=0):
    """Ángulo en grados decimales → texto 'g° mm′ ss″' (texto plano, para etiquetas de radio y dropdown)."""
    signo = "−" if grados < 0 else ""
    x = abs(float(grados))
    g = int(x)
    m = int((x - g) * 60)
    s = round(((x - g) * 60 - m) * 60, dec)
    if s >= 60:
        s, m = 0.0, m + 1
    if m >= 60:
        m, g = 0, g + 1
    ancho = 2 if dec == 0 else 3 + dec
    return f"{signo}{g}° {m:02d}′ {s:0{ancho}.{dec}f}″"


# ----------------------------------------------------------------------------
# asserts rápidos
# ----------------------------------------------------------------------------

if __name__ == "__main__":
    e1, e2, e3 = np.eye(3)
    th = np.deg2rad(37.0)
    assert exacto(rot2(np.pi / 2) @ [1, 0], [0, 1]), "rot2(90°) debe mandar e1 a e2"
    assert exacto(area_poligono(_cuadrado_unitario()), 1.0), "área del cuadrado unitario = 1"
    assert exacto(area_poligono(transformar(_cuadrado_unitario(), np.diag([1, -1]))), -1.0), "reflexión → área −1"
    assert exacto(rodrigues(e3, th), rot_z(th)), "rodrigues(z, θ) == rot_z(θ)"
    assert exacto(rodrigues(e1, th), rot_x(th)) and exacto(rodrigues(e2, th), rot_y(th))
    assert exacto(rodrigues([0, 0, 5], th), rot_z(th)), "el eje se normaliza"
    p = (3.0, -2.0)
    assert exacto(dehom(hom(p)), p) and dehom([1, 2, 0]) is None, "hom/dehom ida y vuelta"
    assert exacto(dehom(2 * hom(p)), p), "escalar el homogéneo no cambia el punto"
    assert exacto(transformar(np.array([[1, 0], [0, 1]]), rot2(np.pi / 2)), [[0, 1], [-1, 0]])
    assert exacto(perp2([1, 2]) @ [1, 2], 0.0)
    A = np.array([[2.0, 1.0], [1.0, 2.0]])
    assert exacto(pot_real(A, 0.5) @ pot_real(A, 0.5), A)
    assert exacto(abs(area_poligono(pentagono_regular(1.0))), 2.5 * np.sin(2 * np.pi / 5))
    assert circulo(10).shape == (10, 2) and exacto(circulo(10)[0], circulo(10)[-1])
    assert grilla_oblicua([1, 0], [0, 1], 2).shape == (10, 2, 2)
    assert pmat([[1, 0.5], [0, 1]]) == r"\begin{pmatrix}1 & 0.500 \\ 0 & 1\end{pmatrix}"
    assert vec_tex([1, 2.25]) == r"(1,\ 2.250)" and num_tex(-1e-12) == "0"
    assert r"\textcolor{#1b6f6a}{1.000}" in matriz_coloreada(np.eye(2))
    assert "✓" in verificar([("uno", True)]) and "1 de 2 fallan" in verificar([("a", True), ("b", False)])
    v, ar = cubo_unitario()
    assert v.shape == (8, 3) and len(ar) == 12
    xs, ys = segmentos_a_trazo(grilla_oblicua([1, 0], [0, 1], 1))
    assert len(xs) == 3 * 6 and xs[2] is None
    assert exacto(coordenadas_en_base([4, 3], rot2(th)), rot2(th).T @ [4, 3]), "ejes girados θ: coordenadas = Rᵀ p"
    assert exacto(coordenadas_en_base([4, 3], np.eye(2)), [4, 3])
    Rd = rot_z(np.pi / 2) @ rot_y(np.pi / 2)
    ej, an = eje_angulo(Rd)
    assert exacto(abs(ej @ ([-1, 1, 1] / np.sqrt(3))), 1.0, tol=1e-9) and exacto(an, 2 * np.pi / 3), "Rz(90)Ry(90): eje (−1,1,1)/√3, 120°"
    assert exacto(rodrigues(ej, an), Rd), "eje_angulo invierte a rodrigues"
    ej, an = eje_angulo(rot_x(np.pi))
    assert exacto(abs(ej[0]), 1.0) and exacto(an, np.pi), "θ = π: el eje sale del autovector"
    assert eje_angulo(np.eye(3))[1] == 0.0
    t, pares = terreno_suave(7)
    assert t.shape == (49, 3) and len(pares) == 2 * 7 * 6 and len(malla_pares(2, 3)) == 2 * 2 + 1 * 3
    assert exacto(proyeccion([4, -3], [4, 3]), [1.12, 0.84]) and exacto(proyeccion([1, 1], [2, 0]), [1, 0])
    assert exacto(angulo([4, -3], [4, 3]), np.arccos(0.28)) and exacto(angulo([1, 0], [0, 1]), np.pi / 2)
    assert exacto(angulo([0.3 * 0.1, 0.3 * 0.6], [0.1, 0.6]), 0.0) and exacto(angulo([1, 0], [-2, 0]), np.pi), "clip: paralelos y opuestos"
    assert exacto(angulo(rot2(th) @ [4, -3], rot2(th) @ [4, 3]), angulo([4, -3], [4, 3])), "una rotación conserva el ángulo"
    try:
        angulo([0, 0], [1, 0])
        raise AssertionError("ángulo con el nulo tiene que fallar")
    except ValueError:
        pass
    nube = np.array([[1.0, 2.0], [3.0, 4.0]])
    assert hom(nube).shape == (2, 3) and exacto(hom(nube)[:, 2], [1, 1]) and exacto(dehom(2 * hom(nube)), nube)
    Aa, ta = np.array([[1.0, 1.0], [0.0, 1.0]]), np.array([0.0, 1.0])
    Ha = matriz_afin(Aa, ta)
    assert exacto(Ha[2], [0, 0, 1]) and exacto(Ha[:2, 2], ta), "matriz_afin: última fila (0 0 1), última columna t"
    assert exacto(transformar_afin(nube, Aa, ta), dehom(hom(nube) @ Ha.T)), "Ax + t == dehom(H hom(x))"
    assert exacto(transformar_afin(nube, Aa, ta), (Aa @ nube.T).T + ta)
    A2, t2 = partes_afin(2 * Ha)
    assert exacto(A2, Aa) and exacto(t2, ta), "partes_afin normaliza por H[2,2]"
    P3, Q3 = np.array([[1.0, 1.0], [3.0, 1.0], [1.0, 2.0]]), np.array([[2.0, 2.0], [4.0, 2.0], [3.0, 3.0]])
    A3, t3 = afin_por_tres_puntos(P3, Q3)
    assert exacto(A3, Aa) and exacto(t3, ta), "apunte 17, ejercicio 6: A = [[1,1],[0,1]], t = (0,1)"
    assert exacto(transformar_afin(P3, A3, t3), Q3)
    H1 = matriz_afin(rot2(np.pi / 4), (np.eye(2) - rot2(np.pi / 4)) @ [3, 1])
    H2 = matriz_afin(0.5 * np.eye(2), 0.5 * np.array([-1, 2]))
    assert exacto(dehom((H2 @ H1) @ hom([1 - np.sqrt(2) / 2] * 2)), [1 - np.sqrt(2) / 2] * 2), "apunte 16: punto fijo"
    lam, Bd = diagonalizar(A)
    assert exacto(lam, [3, 1]) and exacto(Bd[:, 0], [1, 1] / np.sqrt(2)) and exacto(Bd[:, 1], [1, -1] / np.sqrt(2)), "diagonalizar [[2,1],[1,2]]: λ = 3, 1; ejes (1,1), (1,−1)"
    assert exacto(Bd @ np.diag(lam) @ np.linalg.inv(Bd), A) and exacto(np.linalg.inv(Bd) @ A @ Bd, np.diag(lam)), "A = B Λ B⁻¹"
    assert exacto(Bd @ np.diag(lam**5) @ np.linalg.inv(Bd), np.linalg.matrix_power(A, 5)), "A⁵ = B Λ⁵ B⁻¹"
    assert exacto(diagonalizar([[3, 1], [0, 2]])[0], [3, 2]), "orden decreciente también sin simetría"
    for singular in (rot2(np.pi / 3), np.array([[1.0, 1.0], [0.0, 1.0]])):
        try:
            diagonalizar(singular)
            raise AssertionError("rotación y cizalla no se diagonalizan")
        except ValueError:
            pass
    assert exacto(coordenadas_en_base([4, 3], np.array([[3.0, 1.0], [1.0, 2.0]])), [1, 1]), "lección 08: (4,3) = b₁ + b₂"
    assert exacto(cuna2([3, 1], [1, 2]), 5.0) and exacto(cuna2([1, 2], [3, 1]), -5.0) and exacto(cuna2([3, 1], [6, 2]), 0.0)
    assert exacto(cuna2([3, 1], [1, 2]), np.linalg.det(np.column_stack([[3, 1], [1, 2]]))), "u ∧ v = det[u v]"
    assert exacto(cuna3([1, 2, 0], [0, 1, 1], [1, 0, 2]), 4.0) and exacto(cuna3([1, 2, 0], [0, 1, 1], [1, 3, 1]), 0.0)
    assert exacto(cuna3([1, 2, 3], [4, 5, -1], [0, 0, 1]), -3.0), "la apuesta del 16/9: (p × q) · r = −3"
    assert alineados([1, 1], [4, 3], [7, 5]) and not alineados([1, 1], [4, 3], [7, 6])
    assert exacto(area_poligono(paralelogramo([3, 1], [1, 2])), cuna2([3, 1], [1, 2])), "el área del paralelogramo es la cuña"
    vp, ap = paralelepipedo([1, 2, 0], [0, 1, 1], [1, 0, 2])
    assert vp.shape == (8, 3) and len(ap) == 12 and exacto(vp[7], [2, 3, 3])
    assert exacto(nucleo2([[1, 2], [2, 4]]), [2, -1]) and exacto(np.array([[1, 2], [2, 4]]) @ nucleo2([[1, 2], [2, 4]]), [0, 0])
    assert exacto(nucleo2([[0, 0], [2, 4]]), [4, -2]), "nucleo2 usa la fila no nula"
    try:
        nucleo2(np.eye(2))
        raise AssertionError("nucleo2 de una invertible tiene que fallar")
    except ValueError:
        pass
    assert autovalores_reales([[2, 1], [1, 2]]) == [3.0, 1.0] and autovalores_reales(rot2(0.5)) == []
    av = autovectores_cuna([[2, 1], [1, 2]])
    assert [a["lam"] for a in av] == [3.0, 1.0] and exacto(av[0]["v"], [1, 1]) and exacto(av[1]["v"], [1, -1])
    assert all(exacto(np.array([[2, 1], [1, 2]]) @ a["v"], a["lam"] * a["v"]) for a in av), "A v = λ v"
    assert autovectores_cuna(2 * np.eye(2))[0]["plano"], "homotecia: el núcleo de A − 2I es todo el plano"
    av3 = autovectores_cuna(np.diag([1.0, 1.0, -1.0]))
    assert [a["lam"] for a in av3] == [1.0, -1.0] and av3[0]["plano"] and exacto(av3[1]["v"], [0, 0, 1]) and av3[1]["filas"] == (0, 1)
    Rzy = rot_z(np.pi / 2) @ rot_y(np.pi / 2)
    av3 = autovectores_cuna(Rzy)
    assert len(av3) == 1 and exacto(av3[0]["lam"], 1.0) and exacto(av3[0]["v"], [-1, 1, 1]), "eje de Rz(90)Ry(90) por cruz de filas"
    assert exacto(Rzy @ av3[0]["v"], av3[0]["v"])
    Hc = np.array([[2.0, -4.0, 8.0], [0.0, -4.0, 12.0], [0.0, -1.0, 4.0]])
    pf = puntos_fijos_proyectivos(Hc)
    assert [p["lam"] for p in pf] == [2.0, -2.0] and pf[0]["plano"] and exacto(pf[0]["recta"], [0, -0.5, 1]) and exacto(pf[1]["punto"], [4, 6])
    assert exacto(dehom(Hc @ hom([4, 6])), [4, 6]), "el centro de la homología es punto fijo"
    pf = puntos_fijos_proyectivos(matriz_afin(np.eye(2), [1, 2]))
    assert len(pf) == 1 and pf[0]["plano"] and exacto(pf[0]["recta"], [0, 0, 1]), "traslación: fija la recta del infinito"
    # lección 10: jacobiano y primera forma
    esf = lambda f, l: xyz(2 * np.cos(f) * np.cos(l), 2 * np.cos(f) * np.sin(l), 2 * np.sin(f))  # noqa: E731
    assert xyz(1, 2, 3).shape == (3,) and esf(np.zeros(5), np.linspace(0, 1, 5)).shape == (5, 3)
    f0, l0 = np.deg2rad(45), np.deg2rad(20)
    J10 = jacobiana_numerica(esf, f0, l0)
    assert J10.shape == (3, 2) and exacto(J10[:, 0], [-2 * np.sin(f0) * np.cos(l0), -2 * np.sin(f0) * np.sin(l0), 2 * np.cos(f0)], tol=1e-7)
    assert exacto(J10[:, 1], [-2 * np.cos(f0) * np.sin(l0), 2 * np.cos(f0) * np.cos(l0), 0], tol=1e-7)
    E10, F10, G10 = primera_forma(J10)
    assert exacto([E10, F10, G10], [4, 0, 4 * np.cos(f0) ** 2], tol=1e-6), "esfera: E = R², F = 0, G = R² cos²φ"
    assert exacto(np.linalg.norm(np.cross(J10[:, 0], J10[:, 1])) ** 2, E10 * G10 - F10**2, tol=1e-6), "|r_u × r_v|² = EG − F²"
    assert exacto(longitud_paso(E10, F10, G10, 0, np.deg2rad(1)), 2 * np.cos(f0) * np.deg2rad(1), tol=1e-9), "1° de longitud a 45°"
    assert longitud_paso(1, 0, 1, [3, 0], [4, 1]).shape == (2,) and exacto(longitud_paso(1, 0, 1, [3, 0], [4, 1]), [5, 1])
    assert exacto(longitud_poligonal([[0, 0, 0], [3, 0, 0], [3, 4, 0]]), 7.0)
    assert exacto(primera_forma(jacobiana_numerica(lambda u, v: xyz(u, v, 1 + 0.4 * u + 0.3 * v), 0.3, -1.0)), [1.16, 0.12, 1.09], tol=1e-7)
    # lección 11: mínimos cuadrados
    A11 = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    x11, r11 = minimos_cuadrados(A11, [0.0, 1.0, 3.0])
    assert exacto(x11, [1.5, -1 / 6]) and exacto(r11, [1 / 6, -1 / 3, 1 / 6]), "ficha 10: y = 1.5x − 1/6, residuos (1/6, −1/3, 1/6)"
    assert exacto(A11.T @ r11, [0, 0]), "el residuo es perpendicular a las columnas de A"
    assert exacto(x11, np.linalg.lstsq(A11, np.array([0.0, 1.0, 3.0]), rcond=None)[0]) and exacto(recta_ajuste([0, 1, 2], [0, 1, 3]), [1.5, -1 / 6])
    assert exacto(recta_ajuste([-1, 0, 1], [1, 1, 4]), [1.5, 2.0]), "ficha 11, problema 1: y = 1.5x + 2"
    assert exacto(minimos_cuadrados(np.ones((3, 1)), [12.1, 11.9, 12.3])[0], [12.1]), "en R, mínimos cuadrados es el promedio"
    p11, rr = punto_por_distancias([[0, 0], [6, 0], [3, 7]], [5, 5, 3])
    assert exacto(p11, [3, 4]) and exacto(rr, [0, 0]), "ficha 11, problema 2: tres círculos → (3, 4)"
    try:
        punto_por_distancias([[0, 0], [6, 0]], [5, 5])
        raise AssertionError("dos mojones no alcanzan")
    except ValueError:
        pass
    Pc = np.array([[1.0, 0.0], [0.0, 1.0], [-1.0, 0.0], [0.0, -1.0]])
    Rc, sc, tc, rmsc = procrustes(Pc, transformar(Pc, rot2(np.pi / 2)))
    assert exacto(Rc, rot2(np.pi / 2)) and exacto(sc, 1.0) and exacto(tc, [0, 0]) and exacto(rmsc, 0.0), "ficha 11, problema 3: el cuadrado girado 90°"
    Pc2 = np.array([[1.0, 1.0], [4.0, 1.0], [5.0, 3.0], [3.0, 5.0], [1.0, 4.0]])
    Rc, sc, tc, rmsc = procrustes(Pc2, 1.5 * transformar(Pc2, rot2(0.4)) + [2.0, -1.0])
    assert exacto(Rc, rot2(0.4)) and exacto(sc, 1.5) and exacto(tc, [2, -1]) and exacto(rmsc, 0.0, tol=1e-9), "procrustes recupera giro, escala y traslación"
    assert exacto(np.linalg.det(Rc), 1.0), "sin espejo"
    cT, dT, nT, r2T = regresion_total([[1.0, 0.0], [-1.0, 0.0], [0.0, 2.0], [0.0, -2.0]])
    assert exacto(cT, [0, 0]) and exacto(np.abs(dT), [0, 1]) and exacto(r2T, 2.0) and exacto(dT @ nT, 0.0), "ficha 11, problema 4: recta x = 0, residuo 2"
    assert exacto(recta_ajuste([1, -1, 0, 0], [0, 0, 2, -2]), [0, 0]), "misma nube, regresión simple: y = 0"
    # lección 14: trigonometría esférica
    pol, ex_, ey_ = punto_esfera(np.pi / 2, 0.0), punto_esfera(0.0, 0.0), punto_esfera(0.0, np.pi / 2)
    assert exacto(pol, e3) and exacto(ex_, e1) and exacto(ey_, e2)
    assert punto_esfera(np.linspace(0, 1, 5), 0.3).shape == (3, 5) and punto_esfera(0.3, np.linspace(0, 1, 7)).shape == (3, 7)
    lados_o, ang_o = triangulo_esferico(pol, ex_, ey_)
    assert exacto(lados_o, [np.pi / 2] * 3) and exacto(ang_o, [np.pi / 2] * 3), "octante: tres lados y tres ángulos rectos"
    assert exacto(exceso_esferico(pol, ex_, ey_), np.pi / 2), "octante: exceso π/2 = un octavo de 4π"
    assert exacto(angulo_esferico(np.pi / 2, np.pi / 2, np.pi / 2), np.pi / 2)
    B60 = punto_esfera(np.pi / 2 - np.pi / 3, 0.0)
    C60 = punto_esfera(np.pi / 2 - np.pi / 3, np.pi / 2)
    (a_, b_, c_), (al_, be_, ga_) = triangulo_esferico(pol, B60, C60)
    assert exacto([b_, c_, al_], [np.pi / 3, np.pi / 3, np.pi / 2]) and exacto(a_, np.arccos(0.25)), "b = c = 60°, A = 90°: cos a = 1/4"
    assert exacto(angulo_esferico(a_, b_, c_), al_) and exacto(angulo_esferico(b_, a_, c_), be_), "ley del coseno y vectores coinciden"
    assert exacto(be_, ga_) and exacto(np.cos(be_), 0.375 / (np.sin(a_) * np.sin(np.pi / 3)))
    assert exacto(abs(cuna3(pol, B60, C60)), np.sin(b_) * np.sin(c_) * np.sin(al_)), "ley del seno: [A, B, C] = sin b sin c sin A"
    chico = (punto_esfera(0, 0), punto_esfera(0, np.deg2rad(1)), punto_esfera(np.deg2rad(1), 0))
    assert exacto(triangulo_esferico(*chico)[0][0], np.arccos(np.cos(np.deg2rad(1)) ** 2)), "triángulo chico: a = arccos(cos² 1°)"
    assert 0 < exceso_esferico(*chico) < 1e-3 and exacto(exceso_esferico(*chico), np.deg2rad(1) ** 2 / 2, tol=1e-6), "exceso ≈ área del triángulo rectángulo"
    arc = arco_maximo(2 * ex_, 2 * ey_, 5)
    assert arc.shape == (5, 3) and exacto(np.linalg.norm(arc, axis=1), 2.0) and exacto(arc[2], np.sqrt(2) * np.array([1, 1, 0]))
    try:
        arco_maximo(ex_, -ex_)
        raise AssertionError("antípodas tiene que fallar")
    except ValueError:
        pass
    try:
        angulo_esferico(0.3, 0.0, 0.3)
        raise AssertionError("lado nulo tiene que fallar")
    except ValueError:
        pass
    # lección 12: esfera (cuenco) y cilindro (canaleta) de radio 2 por diferencias finitas, silla exacta
    _esf = lambda x, y: np.array([x, y, 2.0 - np.sqrt(4.0 - x**2 - y**2)])  # noqa: E731
    _ff = formas_fundamentales(_esf, 0.3, -0.2)
    _k1, _k2, _D = curvaturas_principales(_ff["E"], _ff["F"], _ff["G"], _ff["L"], _ff["M"], _ff["N"])
    assert exacto([_k1, _k2], [0.5, 0.5], tol=1e-5) and exacto(_ff["L"] / _ff["E"], 0.5, tol=1e-5), "esfera R = 2: κ₁ = κ₂ = 1/R, II = I/R"
    assert exacto(curvatura_gauss(_ff["E"], _ff["F"], _ff["G"], _ff["L"], _ff["M"], _ff["N"]), [0.25, 0.5], tol=1e-5), "esfera: K = 1/R², H = 1/R"
    assert exacto(_D.T @ np.array([[_ff["E"], _ff["F"]], [_ff["F"], _ff["G"]]]) @ _D, np.eye(2), tol=1e-6), "direcciones principales: I(d, d) = 1"
    _ff = formas_fundamentales(lambda x, y: np.array([x, y, 2.0 - np.sqrt(4.0 - x**2)]), 0.3, -0.2)
    assert exacto(curvaturas_principales(*(_ff[k] for k in "EFGLMN"))[:2], [0.5, 0.0], tol=1e-5), "cilindro R = 2: κ = (1/R, 0)"
    assert exacto(curvatura_gauss(*(_ff[k] for k in "EFGLMN"))[0], 0.0, tol=1e-6), "cilindro: K = 0"
    _ff = formas_fundamentales(lambda x, y: np.array([x, y, (x**2 - y**2) / 4]), 0.0, 0.0)
    assert exacto([_ff[k] for k in "EFGLMN"], [1, 0, 1, 0.5, 0, -0.5], tol=1e-7), "silla en el origen: I = identidad, II = diag(1/2, −1/2)"
    assert exacto(curvatura_gauss(*(_ff[k] for k in "EFGLMN")), [-0.25, 0.0], tol=1e-7), "silla: K = −1/4, H = 0"
    assert exacto(curvatura_normal(*(_ff[k] for k in "EFGLMN"), 1, 1), 0.0, tol=1e-7), "silla: a 45° la curvatura normal es cero"
    _c = seccion_normal(lambda x, y: (x**2 - y**2) / 4, _ff["p"], [1, 0, 0], _ff["n"], 0.8, 9)
    assert _c.shape == (9, 3) and exacto(_c[:, 2], (_c[:, 0] ** 2 - _c[:, 1] ** 2) / 4, tol=1e-9), "la sección normal está sobre la superficie"
    assert circulo_3d([0, 0, 1], [1, 0, 0], [0, 1, 0], 2.0, 5).shape == (5, 3) and exacto(circulo_3d([0, 0, 1], [1, 0, 0], [0, 1, 0], 2.0, 5)[1], [0, 2, 1])
    # lección 13: GRS80 en φ = 45°, ecuador y polo; las tres latitudes; conversión y primera forma del elipsoide
    _g = elipsoide_grs80()
    assert exacto([_g["a"], _g["b"]], [6378137.0, 6356752.3141], tol=1e-4) and exacto(_g["e2"], 0.00669438002290, tol=1e-12)
    _phi = np.deg2rad(45.0)
    _M, _N = radios_curvatura(_phi)
    assert exacto([_M, _N], [6367381.8156, 6388838.2902], tol=1e-3), "GRS80, φ = 45°: M = 6367381.82 m, N = 6388838.29 m"
    assert exacto(radios_curvatura(0.0), [_g["b"] ** 2 / _g["a"], _g["a"]], tol=1e-6), "ecuador: M = b²/a, N = a"
    assert exacto(radios_curvatura(np.pi / 2), [_g["a"] ** 2 / _g["b"]] * 2, tol=1e-6), "polo: M = N = a²/b"
    _psi, _beta = latitudes(_phi)
    assert exacto(np.rad2deg(_psi), 44.807576783, tol=1e-8) and _psi < _beta < _phi, "φ = 45°: ψ = 44° 48′ 27″, ψ < β < φ"
    assert exacto(latitudes(0.0), [0, 0]) and exacto(latitudes(np.pi / 2), [np.pi / 2] * 2), "ecuador y polos: las tres latitudes coinciden"
    _P = geodesica_a_cartesiana(_phi, np.deg2rad(30.0))
    assert exacto(_P, [3912348.465, 2258795.439, 4487348.409], tol=1e-3), "GRS80, φ = 45°, λ = 30°, h = 0"
    assert exacto((_P[0] ** 2 + _P[1] ** 2) / _g["a"] ** 2 + _P[2] ** 2 / _g["b"] ** 2, 1.0, tol=1e-12), "el punto está sobre el elipsoide"
    assert exacto(geodesica_a_cartesiana(0.0, 0.0), [_g["a"], 0, 0]) and exacto(geodesica_a_cartesiana(np.pi / 2, 0.0), [0, 0, _g["b"]], tol=1e-6)
    assert geodesica_a_cartesiana(np.zeros((3, 4)), np.zeros((3, 4))).shape == (3, 4, 3), "vectorizado: una terna por punto"
    assert exacto(geodesica_a_cartesiana(_phi, 0.3, 100.0) - geodesica_a_cartesiana(_phi, 0.3), 100.0 * normal_elipsoide(_phi, 0.3), tol=1e-6), "h va sobre la normal"
    _ff = formas_fundamentales(lambda p, l: geodesica_a_cartesiana(p, l), _phi, 0.3)
    assert np.allclose([_ff["E"], _ff["F"], _ff["G"]], [_M**2, 0.0, _N**2 * np.cos(_phi) ** 2], rtol=1e-5, atol=1.0), "elipsoide: E = M², F = 0, G = N² cos²φ"
    assert np.allclose(curvaturas_principales(*(_ff[k] for k in "EFGLMN"))[:2], [1 / _M, 1 / _N], rtol=1e-5), "curvaturas principales del elipsoide: 1/M (meridiano) y 1/N (primer vertical)"
    assert exacto(_ff["n"], -normal_elipsoide(_phi, 0.3), tol=1e-6), "r_φ × r_λ apunta hacia adentro"
    assert gms(44.8) == "44° 48′ 00″" and gms(-0.5) == "−0° 30′ 00″" and gms(59.99999) == "60° 00′ 00″" and gms(12.3456, 1) == "12° 20′ 44.2″"
    print("cb104: asserts OK")
