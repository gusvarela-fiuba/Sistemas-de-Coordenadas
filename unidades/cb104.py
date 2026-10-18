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

import random

import numpy as np

# banco:begin
try:
    from banco_autoevaluacion import BANCO_AUTOEVALUACION
except ImportError:
    from unidades.banco_autoevaluacion import BANCO_AUTOEVALUACION
# banco:end

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
    # reflexiones y similaridades (lección 03)
    "reflexion2", "similaridad", "partes_similaridad", "centro_fijo", "similaridad_por_dos_puntos", "trayectoria",
    "estelas_afin",
    # formas lineales y dualidad (lección 06)
    "forma_transformada", "recta_por_dos_puntos", "cortes_caja", "rectas_de_nivel",
    # SVD, inversa y pseudoinversa (lección 09)
    "svd2", "pseudoinversa", "cuatro_subespacios", "truncar_svd", "elipse_imagen", "capa_direcciones_singulares",
    # DEM Precordillera (lección 09)
    "dem_precordillera", "rms_rango_k",
    # proyectivas (lección 05)
    "pentagono_profesor", "aplicar_proyectiva", "recta_al_infinito", "sistema_lambda", "homografia_lambda",
    "homografia_4puntos", "razon_doble", "curva_proyectiva", "grilla_proyectiva", "estelas_proyectivas",
    "capa_despues_proyectiva",
    # SVM de margen duro (lección 06, aporte CEIA)
    "svm_margen_duro_2d",
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


def figura_plano(rango=5, titulo="", ancho=540, alto=500):
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


def figura_espacio(rango=2.6, titulo="", ancho=540, alto=520):
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


def latitud_isometrica(phi, e=np.sqrt(_GRS80["e2"])):
    """Latitud isométrica q(φ) = ln tan(π/4 + φ/2) − (e/2) ln[(1 + e sin φ)/(1 − e sin φ)] (radianes; e = primera
    excentricidad, e = 0 es la esfera). Es la coordenada norte que estira el meridiano hasta que un paso dq mide lo
    mismo que un paso dλ: dq = M dφ/(N cos φ), así ds² = N² cos²φ (dq² + dλ²) y la grilla (λ, q) es conforme.
    q(0) = 0, impar, q → ±∞ en los polos. Mercator es y = a q(φ). Vectorizado."""
    phi = np.asarray(phi, dtype=float)
    es = e * np.sin(phi)
    return np.log(np.tan(np.pi / 4 + phi / 2)) - (e / 2) * np.log((1 + es) / (1 - es))


def arco_meridiano(phi, a=_GRS80["a"], e2=_GRS80["e2"], n=2000):
    """S(φ) = ∫₀^φ M(u) du, largo del meridiano desde el ecuador (metros si a está en metros), por Simpson compuesto
    con n (par) subintervalos. Vectorizado sobre φ (un Simpson por valor)."""
    phi = np.asarray(phi, dtype=float)

    def _s(p):
        u = np.linspace(0.0, p, n + 1)
        M = radios_curvatura(u, a, e2)[0]
        w = np.ones(n + 1)
        w[1:-1:2], w[2:-1:2] = 4.0, 2.0
        return float((p / (3 * n)) * np.sum(w * M))

    return np.vectorize(_s, otypes=[float])(phi) if phi.ndim else _s(float(phi))


def escalas_proyeccion_cilindrica(phi, tipo, elipsoide=_GRS80):
    """(y_m, h, k, ω_max°) de una proyección cilíndrica normal x = a λ en la latitud φ (radianes), sobre el elipsoide
    dado (dict de `elipsoide`). h = escala a lo largo del meridiano, k = a lo largo del paralelo (siempre
    k = a/(N cos φ) porque x = a λ), ω_max = 2 arcsin(|h − k|/(h + k)) la deformación angular máxima (Tissot).
      'conforme_mercator': y = a q(φ) (latitud isométrica), h = k, ω = 0;
      'equidistante':      y = S(φ) (arco de meridiano), h = 1;
      'equivalente':       y = (1/a) ∫₀^φ M N cos u du, h = 1/k (conserva áreas).
    Las tres coinciden en el ecuador: h = k = 1."""
    a, e2 = elipsoide["a"], elipsoide["e2"]
    phi = float(phi)
    M, N = radios_curvatura(phi, a, e2)
    k = a / (N * np.cos(phi))
    if tipo == "conforme_mercator":
        y, h = a * float(latitud_isometrica(phi, np.sqrt(e2))), k
    elif tipo == "equidistante":
        y, h = arco_meridiano(phi, a, e2), 1.0
    elif tipo == "equivalente":
        n = 2000
        u = np.linspace(0.0, phi, n + 1)
        Mu, Nu = radios_curvatura(u, a, e2)
        w = np.ones(n + 1)
        w[1:-1:2], w[2:-1:2] = 4.0, 2.0
        y, h = float((phi / (3 * n)) * np.sum(w * Mu * Nu * np.cos(u))) / a, 1.0 / k
    else:
        raise ValueError(f"tipo {tipo!r}: usar 'conforme_mercator', 'equidistante' o 'equivalente'")
    omega = float(np.rad2deg(2 * np.arcsin(abs(h - k) / (h + k))))
    return float(y), float(h), float(k), omega


def defecto_conformidad_jacobiano(J):
    """Cuánto le falta a una jacobiana 2×2 para ser conforme: dict con `sigmas` (σ₁ ≥ σ₂ de la SVD: semiejes de la
    indicatriz de Tissot), `razon` σ₁/σ₂, `def_angular_max_deg` = 2 arcsin((σ₁ − σ₂)/(σ₁ + σ₂)) en grados (0 si y
    sólo si J es una similaridad), `parte_conforme` ½[[j₁₁ + j₂₂, j₁₂ − j₂₁], [j₂₁ − j₁₂, j₁₁ + j₂₂]] (la parte de la
    forma [[a, −b], [b, a]] del número complejo, Cauchy-Riemann) y `parte_anticonforme` = J − parte_conforme."""
    J = np.asarray(J, dtype=float).reshape(2, 2)
    s = np.linalg.svd(J, compute_uv=False)
    s1, s2 = float(s[0]), float(s[1])
    a, b = (J[0, 0] + J[1, 1]) / 2, (J[1, 0] - J[0, 1]) / 2
    conforme = np.array([[a, -b], [b, a]])
    return dict(
        sigmas=(s1, s2),
        razon=s1 / s2 if s2 > 0 else np.inf,
        def_angular_max_deg=float(np.rad2deg(2 * np.arcsin((s1 - s2) / (s1 + s2)))) if s1 + s2 > 0 else 0.0,
        parte_conforme=conforme,
        parte_anticonforme=J - conforme,
    )


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
# reflexiones y similaridades (lección 03)
# ----------------------------------------------------------------------------


def reflexion2(alpha):
    """Reflexión del plano respecto de la recta por el origen de ángulo alpha (radianes):
    [[cos 2α, sin 2α], [sin 2α, −cos 2α]]. Columnas: a dónde van e₁ y e₂. Ortogonal con det = −1, es su propia
    inversa; reflexion2(a) @ reflexion2(b) = rot2(2(a − b)) (dos espejos seguidos giran el doble del ángulo entre ellos)."""
    c, s = np.cos(2 * alpha), np.sin(2 * alpha)
    return np.array([[c, s], [s, -c]])


def similaridad(k, theta, t=(0.0, 0.0)):
    """(A, t) de la similaridad directa x ↦ k R(θ) x + t: gira θ, multiplica todas las longitudes por k y corre t."""
    return float(k) * rot2(theta), np.asarray(t, dtype=float).reshape(2)


def partes_similaridad(A, tol=1e-9):
    """(k, θ) de una matriz 2×2 de la forma k R(θ), k > 0. ValueError si A no tiene esa forma (no conserva ángulos)."""
    A = np.asarray(A, dtype=float)
    a, b = A[0, 0], A[1, 0]
    k = float(np.hypot(a, b))
    if k < tol or not np.allclose(A, k * rot2(np.arctan2(b, a)), atol=tol * max(1.0, k), rtol=0):
        raise ValueError("la matriz no es k·R(θ): no es una similaridad directa")
    return k, float(np.arctan2(b, a))


def centro_fijo(A, t, tol=1e-9):
    """El punto fijo de F(x) = Ax + t, resolviendo (I − A) c = t. None si I − A es singular (identidad, traslación,
    o una afinidad con una recta de puntos fijos o ninguno): entonces no hay un único centro."""
    A = np.asarray(A, dtype=float)
    M = np.eye(2) - A
    if abs(np.linalg.det(M)) < tol * max(1.0, float(np.abs(M).max()) ** 2):
        return None
    return np.linalg.solve(M, np.asarray(t, dtype=float).reshape(2))


def similaridad_por_dos_puntos(P1, P2, Q1, Q2):
    """(A, t) de la similaridad directa que lleva P1 ↦ Q1 y P2 ↦ Q2 (P1 ≠ P2).

    Con complejos: z ↦ a z + b, a = (Q2 − Q1)/(P2 − P1) (el giro y la escala del segmento), b = Q1 − a P1.
    A = [[Re a, −Im a], [Im a, Re a]] = |a| R(arg a), t = (Re b, Im b).
    """
    z = [complex(float(p[0]), float(p[1])) for p in (P1, P2, Q1, Q2)]
    if abs(z[1] - z[0]) == 0.0:
        raise ValueError("P1 y P2 tienen que ser distintos")
    a = (z[3] - z[2]) / (z[1] - z[0])
    b = z[2] - a * z[0]
    return np.array([[a.real, -a.imag], [a.imag, a.real]]), np.array([b.real, b.imag])


def trayectoria(A, t, p, n):
    """Los n + 1 puntos p, F(p), F²(p), …, Fⁿ(p) bajo F(x) = Ax + t, como nube (n + 1)×2. Rotación: sobre una
    circunferencia; homotecia: sobre un rayo; similaridad: una espiral que converge al centro si k < 1."""
    A = np.asarray(A, dtype=float)
    t = np.asarray(t, dtype=float).reshape(2)
    pts = [np.asarray(p, dtype=float).reshape(2)]
    for _ in range(int(n)):
        pts.append(A @ pts[-1] + t)
    return np.array(pts)


def estelas_afin(puntos, camino):
    """Como `estelas`, pero el camino es una lista de pares (A, t): la trayectoria de cada punto bajo A p + t."""
    xs, ys = [], []
    for p in np.asarray(puntos, dtype=float):
        tray = np.array([np.asarray(A, dtype=float) @ p + np.asarray(t, dtype=float) for A, t in camino])
        xs += list(tray[:, 0]) + [None]
        ys += list(tray[:, 1]) + [None]
    return xs, ys


# ----------------------------------------------------------------------------
# asserts rápidos
# ----------------------------------------------------------------------------


# ----------------------------------------------------------------------------
# formas lineales y dualidad (lección 06)
# ----------------------------------------------------------------------------


def forma_transformada(l, A):
    """La fila ℓ arrastrada junto con la figura cuando los puntos van con A: ℓ' = ℓ A⁻¹, la regla que sobre A p lee
    lo mismo que ℓ sobre p (ℓ'(A p) = ℓ(p)). Resuelve Aᵀ x = ℓᵀ en vez de invertir. ValueError si det A = 0."""
    A = np.asarray(A, dtype=float)
    l = np.asarray(l, dtype=float).reshape(-1)
    if abs(np.linalg.det(A)) < 1e-12 * max(1.0, float(np.abs(A).max()) ** A.shape[0]):
        raise ValueError("det A = 0: A aplasta el plano y la regla no se puede arrastrar")
    return np.linalg.solve(A.T, l)


def recta_por_dos_puntos(p, q):
    """La recta por p y q como fila homogénea (a, b, c), con a x + b y + c = 0: la cuña (producto cruz) de las ternas
    homogéneas p̃ × q̃. Definida a menos de escala (q̃ × p̃ es la misma recta con signo cambiado). ValueError si p = q."""
    l = np.cross(hom(p), hom(q))
    if np.linalg.norm(l) < 1e-12:
        raise ValueError("p y q son el mismo punto: no determinan una recta")
    return l


def cortes_caja(l, c, rango=5):
    """Los puntos donde la recta de nivel ℓ·p = c corta el borde de la caja [a, b]² (`rango` = semilado o (min, max)),
    como array k×2 con k ∈ {0, 1, 2} (vacío si la recta no pasa por la caja). ℓ no puede ser nulo."""
    a, b = _rango2(rango)
    l = np.asarray(l, dtype=float).reshape(2)
    if np.linalg.norm(l) == 0.0:
        raise ValueError("la forma nula no tiene rectas de nivel")
    tol = 1e-9 * (b - a)
    puntos = []
    for i in (0, 1):  # fijamos la coordenada i en cada borde y despejamos la otra
        j = 1 - i
        if abs(l[j]) < 1e-12:
            continue
        for borde in (a, b):
            otra = (c - l[i] * borde) / l[j]
            if a - tol <= otra <= b + tol:
                p = np.zeros(2)
                p[i], p[j] = borde, float(np.clip(otra, a, b))
                if not any(np.linalg.norm(p - q) < tol for q in puntos):
                    puntos.append(p)
    return np.array(puntos).reshape(-1, 2)


def rectas_de_nivel(fig, l, niveles, rango=5, color=TEAL_DESPUES, nombre="rectas de nivel", etiquetas=True,
                    ancho=1.3, destacar=0):
    """La forma lineal ℓ dibujada como regla graduada: las rectas ℓ·p = c para cada c de `niveles`, recortadas a la
    caja, en un solo trazo; la de c = `destacar` aparte y más gruesa (None: ninguna); opcional, la etiqueta c en el
    corte de más a la derecha. Agrega SIEMPRE tres trazas (rectas, destacada, etiquetas), para que una animación
    pueda reemplazarlas en orden. Devuelve fig."""
    import plotly.graph_objects as go

    xs, ys, dx, dy, tx, ty, tt = [], [], [], [], [], [], []
    for c in niveles:
        P = cortes_caja(l, c, rango)
        if len(P) < 2:
            continue
        if destacar is not None and abs(float(c) - float(destacar)) < 1e-9:
            dx += [P[0, 0], P[1, 0], None]
            dy += [P[0, 1], P[1, 1], None]
        else:
            xs += [P[0, 0], P[1, 0], None]
            ys += [P[0, 1], P[1, 1], None]
        if etiquetas:
            k = int(np.argmax(P[:, 0] + 1e-3 * P[:, 1]))
            tx.append(P[k, 0])
            ty.append(P[k, 1])
            tt.append(f"{float(c):g}")
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines", line=dict(color=color, width=ancho), name=nombre, hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=dx, y=dy, mode="lines", line=dict(color=color, width=2.5 * ancho), hoverinfo="skip",
                             name=f"{nombre}: c = {destacar}", showlegend=bool(dx)))
    fig.add_trace(go.Scatter(x=tx, y=ty, mode="text", text=tt, textposition="middle left", hoverinfo="skip",
                             textfont=dict(size=10, color=color), showlegend=False))
    return fig

# ----------------------------------------------------------------------------
# SVD, inversa y pseudoinversa (lección 09)
# ----------------------------------------------------------------------------


def svd2(A):
    """SVD de una 2×2 con los signos fijos: (U, s, Vt) con A = U diag(s) Vt, s[0] ≥ s[1] ≥ 0, V una ROTACIÓN
    (det V = +1, v₁ con primera componente no nula positiva) y U ortogonal con det U = signo de det A: si A refleja,
    la reflexión queda en U. Si σ₁ = σ₂ (un giro, una homotecia) la elección de V es libre y se toma V = I: todo el
    giro queda en U. `np.linalg.svd` deja los signos de las columnas librados a la rutina; acá quedan fijos para
    dibujar v₁, v₂ y para animar Vᵀ como un giro."""
    A = np.asarray(A, dtype=float)
    U, s, Vt = np.linalg.svd(A)
    if abs(s[0] - s[1]) < 1e-9 * max(s[0], 1.0):  # σ₁ = σ₂ (un giro, una homotecia): cualquier V sirve; elegimos V = I
        Vt = np.eye(2)
        U = A / s[0] if s[0] > 1e-12 else np.eye(2)
    if np.linalg.det(Vt) < 0:  # cambiar el signo de v₂ y de u₂ a la vez no cambia el producto
        Vt[1] = -Vt[1]
        U[:, 1] = -U[:, 1]
    j = int(np.argmax(np.abs(Vt[0]) > 1e-12))
    if Vt[0, j] < 0:  # (−U) Σ (−Vᵀ) = U Σ Vᵀ y V sigue siendo rotación
        Vt, U = -Vt, -U
    return U, s, Vt


def pseudoinversa(A, tol=1e-10):
    """A⁺ = V Σ⁺ Uᵀ de una matriz m×n: recíprocos de los σ mayores que tol·σ₁ y ceros donde σ = 0. Es `np.linalg.pinv`
    hecha a mano. Si A es cuadrada y ningún σ es cero coincide con A⁻¹; en general A⁺y es la solución de mínimos
    cuadrados de norma mínima de A x ≈ y (proyecta y sobre la imagen y deshace sólo lo que no se aplastó)."""
    A = np.asarray(A, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    corte = tol * (s[0] if len(s) and s[0] > 0 else 1.0)
    s_plus = np.array([1.0 / x if x > corte else 0.0 for x in s])
    return Vt.T @ np.diag(s_plus) @ U.T


def cuatro_subespacios(A, tol=1e-10):
    """Los cuatro subespacios de una m×n, con los nombres del profesor, como bases ortonormales en columnas:
    `imagen` (los uₖ con σₖ ≠ 0, en Rᵐ), `contra_imagen` (los uₖ restantes: el núcleo de Aᵀ, perpendicular a la
    imagen, donde vive el residuo), `coimagen` (los vₖ con σₖ ≠ 0, en Rⁿ: la imagen de Aᵀ) y `nucleo` (los vₖ con
    σₖ = 0). También `s` (los σ) y `rango`. Una base vacía es un array con cero columnas."""
    A = np.asarray(A, dtype=float)
    U, s, Vt = np.linalg.svd(A, full_matrices=True)
    corte = tol * (s[0] if len(s) and s[0] > 0 else 1.0)
    r = int(np.sum(s > corte))
    return dict(s=s, rango=r, imagen=U[:, :r], contra_imagen=U[:, r:], coimagen=Vt[:r].T, nucleo=Vt[r:].T)


def truncar_svd(U, s, Vt, k):
    """Aproximación de rango k a partir de la SVD: U[:, :k] diag(s[:k]) Vt[:k]. Con k = len(s) devuelve la matriz
    original; es la mejor aproximación de rango k (Eckart–Young), para comprimir una matriz de alturas."""
    k = int(k)
    return np.asarray(U)[:, :k] @ np.diag(np.asarray(s)[:k]) @ np.asarray(Vt)[:k]


def elipse_imagen(A, n=240):
    """La imagen del círculo unitario por A como nube n×2 cerrada: la elipse de semiejes σ₁u₁, σ₂u₂ (o un segmento si
    σ₂ = 0). Es `transformar(circulo(n), A)`."""
    return transformar(circulo(n), A)


def capa_direcciones_singulares(fig, A, antes=True, despues=True, nombre="A"):
    """Las direcciones singulares de una 2×2 (vía `svd2`): con `antes`, v₁ (teal) y v₂ (rust) como flechas finas desde
    el origen; con `despues`, sus imágenes A vₖ = σₖ uₖ (los semiejes de la elipse) con los mismos colores y más gruesas.
    Columna k de V = flecha del color k, igual que `flechas_columnas`. Devuelve (U, s, Vt)."""
    U, s, Vt = svd2(A)
    for k in range(2):
        c = color_columna(k)
        if antes:
            flecha(fig, (0, 0), Vt[k], c, f"v{_SUB[k]} (entrada)", ancho=3)
        if despues:
            flecha(fig, (0, 0), s[k] * U[:, k], c, f"{nombre} v{_SUB[k]} = σ{_SUB[k]} u{_SUB[k]}")
    return U, s, Vt


# ----------------------------------------------------------------------------
# --- Proyectivas (lección 05) ---
# homografías p' ~ H p: cuatro puntos la fijan; la fila 3 es la recta que se va al infinito
# ----------------------------------------------------------------------------


def pentagono_profesor():
    """Los vértices A..E (5×2) del pentágono regular de la planilla del profesor (23/9): D = (0, 1) y los demás por
    giros de 72° alrededor del origen, C = R(72°) D, B = R(144°) D, A = R(216°) D, E = R(288°) D. Recorrido
    A → B → C → D → E horario; el centro (0, 0) es el punto fijo (0, 0, 1) de cualquier giro."""
    giros = dict(A=216, B=144, C=72, D=0, E=288)
    return np.array([rot2(np.deg2rad(giros[k])) @ [0.0, 1.0] for k in "ABCDE"])


def aplicar_proyectiva(nube, H):
    """Nube N×2 bajo la homografía H (3×3): hom(nube) @ H.T y división por la tercera coordenada W, fila a fila.
    Una fila sobre la recta que se va al infinito (W = 0) da inf/nan (ver `dehom`)."""
    return dehom(hom(nube) @ np.asarray(H, dtype=float).T)


def recta_al_infinito(H):
    """La recta que H manda al infinito: su tercera fila (a, b, c), o sea los puntos con W = a x + b y + c = 0.
    Si a = b = 0 ninguna recta propia se va: H es afín y la recta del infinito queda fija."""
    return np.asarray(H, dtype=float)[2].copy()


def sistema_lambda(origen, destino):
    """El sistema 13×13 del profesor para la homografía que lleva cuatro puntos (4×2) a otros cuatro (4×2):
    incógnitas (h11, h12, h13, h21, …, h33, λ1, λ2, λ3, λ4); por cada punto las tres ecuaciones H pᵢ − λᵢ qᵢ = 0
    (pᵢ, qᵢ en homogéneas con w = 1) y la decimotercera h33 = 1. Devuelve (M, b) con M x = b."""
    P, Q = hom(origen), hom(destino)
    M, b = np.zeros((13, 13)), np.zeros(13)
    for i in range(4):
        for k in range(3):
            M[3 * i + k, 3 * k:3 * k + 3] = P[i]
            M[3 * i + k, 9 + i] = -Q[i, k]
    M[12, 8], b[12] = 1.0, 1.0
    return M, b


def homografia_lambda(origen, destino):
    """(H, λ) resolviendo `sistema_lambda` con np.linalg.solve: H pᵢ = λᵢ qᵢ exactamente, con h33 = 1.
    λᵢ es la W de cada punto: si cambia de signo entre dos vértices, el lado que los une cruza la recta que se va
    al infinito y la imagen se parte."""
    M, b = sistema_lambda(origen, destino)
    x = np.linalg.solve(M, b)
    return x[:9].reshape(3, 3), x[9:]


def homografia_4puntos(origen, destino):
    """H (3×3) que lleva N ≥ 4 puntos (N×2, sin tres alineados) a otros N, por la forma estándar (DLT): cada par
    da dos ecuaciones homogéneas en los nueve hᵢⱼ, u W = h₁·p y v W = h₂·p con W = h₃·p, matriz 2N×9, y H es el
    vector del núcleo (último vector singular derecho; con N > 4, el de mínimos cuadrados). Se normaliza con
    h33 = 1, o con módulo máximo 1 si h33 = 0."""
    P, Q = hom(origen), np.asarray(destino, dtype=float)
    filas = []
    for p, (u, v) in zip(P, Q):
        filas.append(np.concatenate([p, [0.0, 0.0, 0.0], -u * p]))
        filas.append(np.concatenate([[0.0, 0.0, 0.0], p, -v * p]))
    H = np.linalg.svd(np.array(filas))[2][-1].reshape(3, 3)
    escala = H[2, 2] if abs(H[2, 2]) > 1e-9 * np.abs(H).max() else np.abs(H).max()
    return H / escala


def razon_doble(a, b, c, d):
    """Razón doble (a, b; c, d) = (c − a)(d − b) / ((c − b)(d − a)) de cuatro números de la recta o de cuatro
    puntos 2D alineados (se leen por su coordenada a lo largo de la recta ab). Es lo único métrico que una
    homografía conserva; vale −1 en una cuaterna armónica (centro y eje de una homología armónica respecto de
    dos puntos intercambiados)."""
    a, b, c, d = (np.asarray(x, dtype=float) for x in (a, b, c, d))
    if a.ndim:
        u = (b - a) / float((b - a) @ (b - a))
        a, b, c, d = [float((x - a) @ u) for x in (a, b, c, d)]
    return float((c - a) * (d - b) / ((c - b) * (d - a)))


def _trazo_proyectivo(segmentos, H, n=40, limite=None):
    """Imagen por H de segmentos (m, 2, 2) muestreados con n puntos, como (xs, ys) con cortes (None) donde W
    cambia de signo (el segmento cruza la recta que se va al infinito) o la imagen se sale de |coord| > limite."""
    H = np.asarray(H, dtype=float)
    xs, ys = [], []
    for p, q in np.asarray(segmentos, dtype=float):
        t = np.linspace(0, 1, n)[:, None]
        w_prev = None
        for x, y, w in hom(p + t * (q - p)) @ H.T:
            ok = abs(w) > 1e-9 and (limite is None or max(abs(x / w), abs(y / w)) <= limite)
            if not ok or (w_prev is not None and w * w_prev < 0):
                xs.append(None)
                ys.append(None)
            if ok:
                xs.append(x / w)
                ys.append(y / w)
            w_prev = w if ok else None
        xs.append(None)
        ys.append(None)
    return xs, ys


def curva_proyectiva(puntos, H, cerrada=True, n=40, limite=None):
    """La imagen por H de la poligonal N×2 (cerrada por default), como (xs, ys) con cortes donde cruza la recta
    que se va al infinito: así se dibuja un objeto cuya imagen se parte. `limite` recorta lo que se va lejos."""
    P = np.asarray(puntos, dtype=float)
    if cerrada:
        P = np.vstack([P, P[:1]])
    return _trazo_proyectivo(np.stack([P[:-1], P[1:]], axis=1), H, n, limite)


def grilla_proyectiva(H, rango=5, paso=1, n=40, limite=None):
    """Las líneas x = k, y = k (|k| ≤ semilado) transformadas por la homografía H, como un solo trazo con cortes
    (`_trazo_proyectivo`). Siguen siendo rectas, pero dejan de ser paralelas: convergen al punto de fuga de su
    dirección. `limite` por default es tres veces el rango."""
    a, b = _rango2(rango)
    if limite is None:
        limite = 3.0 * max(abs(a), abs(b))
    ks = np.arange(np.ceil(a / paso) * paso, b + paso / 2, paso)
    segs = [[[k, a], [k, b]] for k in ks] + [[[a, k], [b, k]] for k in ks]
    return _trazo_proyectivo(segs, H, n, limite)


def estelas_proyectivas(puntos, camino, limite=None):
    """Trayectoria de cada punto (N×2) a lo largo de un camino de homografías, como (xs, ys) con cortes donde el
    punto pasa por el infinito (W cambia de signo) o se sale de |coord| > limite."""
    xs, ys = [], []
    for p in np.asarray(puntos, dtype=float):
        w_prev = None
        for H in camino:
            x, y, w = np.asarray(H, dtype=float) @ hom(p)
            ok = abs(w) > 1e-9 and (limite is None or max(abs(x / w), abs(y / w)) <= limite)
            if not ok or (w_prev is not None and w * w_prev < 0):
                xs.append(None)
                ys.append(None)
            if ok:
                xs.append(x / w)
                ys.append(y / w)
            w_prev = w if ok else None
        xs.append(None)
        ys.append(None)
    return xs, ys


def capa_despues_proyectiva(fig, H, rango=5, paso=1, cuadrado=True, columnas=True):
    """Capa teal de la homografía H: la grilla transformada (`grilla_proyectiva`), el cuadrado unitario
    transformado y las columnas de H leídas como puntos: columna 1 (teal) y 2 (rust) son las imágenes de los
    puntos impropios de los ejes, o sea los **puntos de fuga** de las rectas y = cte y x = cte (marcador ×; si
    h3k = 0 siguen impropios y se dibuja la dirección como flecha desde la imagen del origen); columna 3 (gold)
    es la imagen del origen. Devuelve fig."""
    import plotly.graph_objects as go

    H = np.asarray(H, dtype=float)
    a, b = _rango2(rango)
    limite = 3.0 * max(abs(a), abs(b))
    gx, gy = grilla_proyectiva(H, rango, paso, limite=limite)
    fig.add_trace(go.Scatter(x=gx, y=gy, mode="lines", line=dict(color=TEAL_DESPUES, width=1), opacity=0.45,
                             name="grilla después", hoverinfo="skip"))
    if cuadrado:
        cx, cy = curva_proyectiva(_cuadrado_unitario(), H, limite=limite)
        fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=TEAL_DESPUES, width=2),
                                 name="cuadrado unitario después"))
    if columnas:
        o = dehom(H[:, 2])
        nombres = ("punto de fuga de las rectas y = cte (columna 1)", "punto de fuga de las rectas x = cte (columna 2)")
        for k in range(2):
            c, col = color_columna(k), H[:, k]
            if abs(col[2]) > 1e-9 * max(1.0, np.abs(H).max()):
                f = col[:2] / col[2]
                fig.add_trace(go.Scatter(x=[f[0]], y=[f[1]], mode="markers", marker=dict(size=12, color=c, symbol="x"),
                                         name=nombres[k]))
            elif o is not None:
                d = col[:2] / np.linalg.norm(col[:2])
                flecha(fig, o, o + d, c, f"columna {k + 1}: sigue impropia (dirección)", ancho=3)
        if o is not None:
            fig.add_trace(go.Scatter(x=[o[0]], y=[o[1]], mode="markers", marker=dict(size=10, color=color_columna(2)),
                                     name="imagen del origen (columna 3)"))
    return fig


# ----------------------------------------------------------------------------
# --- DEM Precordillera (lección 09) ---
# ----------------------------------------------------------------------------

_DEM_NPY = "datos/dem_copernicus/dem_precordillera_512.npy"

# Submuestra del DEM embebida como texto. La escribe datos/dem_copernicus/embed_dem.py; no editar a mano.
# dem-blob:begin  (128×128 = dem_precordillera_512.npy[::4, ::4], int16 al metro, delta por filas, zlib, base85: 21200 caracteres)
_DEM_N = 128
_DEM_B85 = (
    "c-nP+X^dpob>8W9x~gY-_Kic%a1n=#L`o(tilQZ1k}cVi6*#dSDKe74iD4kH6aNViBmtZNwh_QcfJDfT0FjNvix$d~D6YeGI"
    "17hE&c5`lJ-zQ;)m?kNwd&?O-#zuZdc>g6UE8bo?m74D+nXQSD;L}u*K!s2unfyFchp^TtFGwEF2N&mb$qv3?vr^uFS!+0#b"
    "-T|xMkPC_bJ{_x(T;kdL+U*mR*2fB(CW~*LGLk{gRUcei`CdH9Xev{W6ZI;@2@g8<3WBu3tjF^S?{^ZG_*qaCC^z0=(*#B93"
    "g}ySB?=r71oYTr<GK;V8X+8|T|DLo$NLR{Z5<hit;yKQDXaF?mY<iF{HX5$ERJb$8w!$NCQBdgY`mxoNiv5X`%m-7UOZ#v|d"
    "Hdt}!2;hQ}&2b=`>q=n}NJeRPdK78B6k$2oy9Mg2;Zdk@$0jq2S(lW5}s3-;-gli5k&Jdm$zs^Y;&mn&w@fRWRlkk%!zO4hg"
    "GQR1RHJl;Bu?da}`AG5Uc3>{Xkq-YG_^)e?0mTrY&g0uXvJcR22mFu7m*jC=?aT7p^2<189Pr;GKXvEaG53w!7P$gUY{K_d_"
    "qscUGgh&m<6Kh%JF|qV_u)JWeTlHefUV(n<992#uI}zK;4k9a5U&fsPX%k=FS?IgrG#@daE^Jbxkjw$FG_9*m<e%&(n3N=^n"
    "b7Pil>Btd*1+5b-s5vG6rQTtQEZK0miq8;;Ik-bzf58aFgs3{o5{^@qe4_l)dtc@(KAk{`Se&<!PM#y1M{Om)$7N^+&lT_C)"
    "cVVpo6QcFAd%m!s|jd{)DirtpmbmlZ&@jP>a1E8HQ4Wmu+gP2Jlf9<dvdWxQ*X4<3+yTuU*b-&WlqFgb;_*1$!2y((z61{ix"
    "KF&YqHOfgvHyVU7BhwoCXGr-wvfLVXh#4$CTxd)WoD+8k6D0Q^)ZWuV(hW+1+HTU6fk9<}hmfiA<JS3l!XMu%9cNy#13|e0S"
    "CcdAG@NNzJQNmd+;!5-G755Hkqk>hg;Im<zQ|WaI?<$17f=}!C%VDo{hpvMD`(+RhrNmWyHzG;{d!@;BE3Q^~{s^yc;@TyCx"
    "`Oq#$z=)YJ0=$^zUrj$fSjUONccXrW6JnODJsC{J))oYOG5dP1LP_jhKYgQatO44FSy{7@<ll)zayUpZCnE+2l4+3@V)4+<w"
    "hW%*09<Y!10&vB~bo#@_(-^Kq@rdew=F>GH#i&r$)R8crpYB+`%VzKoMKOsX4%}JW>VpEmE#R7ILl1FN-*D1=miodjq0$u2L"
    "-_mnozXrQslOlj8W8yDm6WM4Cvr{~_@f5UUM-6XQFTla3rPB)TW}W5pwYbQ}Kf1qD1P9|Qcq0ooswF97m;Wx~A&>d(nVcOv&"
    "SV5$t5rriH>e}$dDgR|bo|84ko1}oYEN?CL&gOqnGxNcrn$Qx}?NsUxk!m4&i75~ei^JQSNjw4IJMNT|zM>t~>R4@ejq}WyX"
    "BL3egDdl4mXIjIt$`57IipqepK^A}xMFR4gqs)tOjWT6|a=s&udH~@L(ESLgeH%2uZtVW&z`Gv@7QO&nehwO7x10f;-^AJ%A"
    "m=2%S$+YMV%B}n{k?nFoy9qqfSn7#hwj(?kmo9)RJP6IS$A`@6nRt?(qbN;PvccDxcwsGzky?hu!<6-{~0$+jaTFT#h{orKB"
    ";jh2c=0qN~r@QQb24p6Ora4oNXAgvqkJEwGUu_Ys5%G4hZ=_!4aMcloLj9?Ry~qVo>f7^v_|?@w4(vz{Z1+1^)q`p9b`&vCh"
    "+gZ(IHW;OJHC^qLz3#8Y_nj(ZWB;TFy-*jtq?y6;7B$TI#<<I^5!!x|{$K|J3E$E<>y+W7q@P~8CN;6A`PiDM`D+c8i<kF*H"
    "&EO$`#_6qft!q`LjQ^QeYbRFQDTSX~E<$plETctG6V?~tbQ~Y*`6yT-5VqqI7b{OB@2TUBmZXX2Q{4@EQJSVH}3Hc`Ie-`%6"
    "5!yW1k^D1Q+pF%c0YMe;jbS}kK?l<~(+uF6#5((c!8v?eARhW4HD)P;+n@-CUo2r4)ar;J2OK5f3O=iWP6X6b!HQRLWa{RPU"
    "zc!>GH9fL&xb|jZ_6N$vBQz!K)HWdyltcMuS8n$xQHkL6pupw3Mo~T3sT^0r#yiD9}zufKQQoh`4w>g??5Au;jAAA_cz_Efb"
    "o66@y+}pz;nd?*!_+B8TPA0NGGtyWn5*Bx?z>v-{OuaMm7Pvb^Nvno*$>|S;CG7l$Hfoqg{3j^t}bNFbSGELk=1QT@(R%gPJ"
    "m;Bx_^seWbC7wxq(<ClR?}klMxT!Gu<2Oj)DcRH9~R@;og{120Qb>cD$J^P90}57GwsjC@PJ3Jd6~;Myag)%&robKsNLpyTh"
    "j|Crw;KY+!1-Ms;te+$&y#Qv)WSR?Fp$Ufz`0m!@pzO7+h1Hj-4Xki5U<TTD0U|m&OdA;EJh%}SKN{1jFj^o@BE#+0(Gv2~e"
    "sFepc0rz#YayNmu)#CO?<fLl+5EGwD1*&`NgwfIZ@LZxtv`Ims(ZF_CJIb|tp$Q(6--q@43Hhg3>v8v8NWO!hgGC&-1c<M?K"
    "gd4~x%DIW9Y{X?%?eh0)LjDYcVxa&ltQbTt{3~cipKzL&#l1on~)<Fd>3-xbvNd4)E4ZVa?ce|lG<xUT&+dj7|@a%5QVnv)+"
    "ps_ZjUs$gSrB>=2XT9#9K<c*wcEQXYhJs4O*x|y;0*Q3b*HjHg;n(Am0Yg-vit4cL4ua<sU&J{S=bzd)URViPBRM@IUYVRsK"
    "1751)P)->M&QA0Rw~$0DFmEvIt50Bx{{<LB^wg?ep`9?f3LzYFAx7OjJrntTM7@p-&g{$8flSa+)Jb#*nso<IXf)LjYAw3#%"
    "W(B}zh50>d)HO>C1a?ksr8@Gx|3$?&2_^b(vsS%?c+36@96%%`))9!&DsJq{V<@Z_a|F>}L^X>$8`i6TBGT|mx`37Xbzt5|`"
    "an$`!aQ_MH*&Oz)04gYf&WFK6F(~m2c77i4tF=Doln<J;@)|ft56;vpb*{XH-7Z50&f*+PI75JQEYd^Rif7f%C35_BsnNSzr"
    "Y84rwz2P3)2|`@z?jc!-L8=u3Y3a!@hcV@lr;e<J|XqB%wtpuyA?a12NgaJzW>*-{(b?{zlvRc1@K>U&&W4KS9l$=`(Nab0F"
    "PVbCCG+p?AkcieFl=@1}&L2TI%ZiQ~~ih(tvt@6-whiS*9J|q-?60Wv0?#l=5F!+2W1|w9g%RJtVX-{l_X{SC6_6*YX}fFKy"
    "YBHlx~^F)d-mo>JHf_gH=18g2MCai|iaK`)|BJoLiyJph0AG0^`n%kRMoRJwi{cFkWv_kR`oVF~)Zi2Z*cKL=<(E0;jW)AU="
    "W+~0yv#`&&JdKXw!s;zsm*Q5BRO!-`OpAz*LE0k_E<K#N=p>kl2mU@*|gx}E$Eg#ibYDcTb+W_1xLa4at6@T6uHEz*lyy}r9"
    "(qRPp9F!WZp*lH2=}B=pDEhuet*lpb?f~}ucjXDl>feVAblM%pS$gC<z`^%{!+S)d3DelkAoo6~dk8#t3Hx59+*K>Ei1Vmqn"
    "*~P7+}o7+oxo>m(d~dWaS%t00UtfU&lG++P3}-HH#F~6SK2QD;cl25pD|lsaWVugP@^AMClx49sh*r57gQ<fT0FiAs&7&j?g"
    "M=kNc|OFBOylnBxSrHrd8E~_xWW&e^|aPzXcifAz<8#_eUY~UdLK4;40IE?4kV2`0g#>Lam}HoN=>U$MpxG+56=xjvdFfE4E"
    "`za@qi7=@!5og3m{x6Ezl6=H4&SPFCqvGaJV9LqLzFVLp+!ULwO%0{-(>Or1WW_w1UKYsyz@Kj~htk?K?u=5cM+g#s$^aiU)"
    "Cf6U*sDPwj)-#rIw?_02j)V{feRX+;v;4N4_Q{2TGp<2$(;3{{Z^={yNY8OvJ)~SxG((X~X3*5;v@Kxd3bmar|cP~OF^ueNB"
    "!U~oMkNQGBR-?PHO8Yl8n=K|jLh7=FK83gSRp+&FTpMQ}pl>mV?-%gB`aJXaw8%J*YMnY|p6XtW9|-ogX?BA0zEIMrFLV!Je"
    ";Ts?i=v+Q67+t-Jp@dAh`nE<P73M6KbCKSX5RtycOV(>Kmv||7N+o6q`$XD8jZ2b)5M9=<QgUN04&}rWJey7<r;1EY1(GPqT"
    "ashq-DZZH!H<Q_!JN7BdnNos2B~j$%884RIiu$Nu3_C+73->*bz~xceG2w%<A`^WMtk`O#RnGd;d9DKPtmt#IH3LwH;VJf?q"
    "G;+*=u`X}CYh56B0A`Lw$XeQ*O@@B#L86j++YRa7e}t=$3qDv=lX>oPGHW2Gg^s#A<eY=c#pFwW5;6<0|QYLg8zN|oZ9KJ3o"
    "`Ww-J|nI27G-v6Mq$-52e@f5P8UzD@Pc$VFw@^_6sXh?X{%!eMJ=iM~kQagG`{w4g~LDAURWvqP$d#|)O&DASiZpPWvx_T#n"
    "4R+5dSc2m?D#lL!5L)sAt~!f%i@5Gp(9#kkf;GnNmTBiJ@2KUjSlKD+0nY$?P2*{=(|d9K0dQ+bnhA-Ww#9vQy{buT)c8%>P"
    "EiIy!q<)(Ky}10BZqa9iZT7($mo8Mc0<hT)yxtX(EgLKe+DUUui&@6fWO8a_purE&D0|Oc77F-|2^>k1aP|>G<edz2Kes){#"
    ")RTJggbjE|XaKpiI&ZQhX~dsJsgp`BI60i(I94K$WrYVO(G3;4-<lN$pr*%s^=Q4$_ueqh##ROD6)bPS1*myl8BrNSad(Qs!"
    "?GVxXUrq(%-?3!z3j(<sV)uuczPXQuJKN7`ILXpeyYvz~P@e-)H=6B_Rn&YA<a)$#f?{rsDZi`7Z(C0@Oknph>e#>-Zz_2(("
    "K^_&{Z@s?p5uM3m{p0?}2j>b}RvK1V#2-pi;XFyI5Etb{M42i9@Md{(=Kyela3rv>AwDk2iMaxJuDHrESxyp4rD7l)nhy0N-"
    "uNLqMUQhficN1$X<ES@4`z6LBmT4QUWcGfA)Lyr!V}q+50A(*xH!CHyade%&i0(&;dZ5nesqV=dUX3t@dKowo`55+4C=;r{h"
    "4*1%@=ih+>lXd-GO+2qe-P7#Dmx!jZIO;Oa+brHHSXAUx}$1Uui~uw{V?OhJ};113^B22Tx@>zw{x?Ea{<3uA=CwW{Hv7y3V"
    "%Y2XN6LDkUX<Q+cf2hmmyW>AkhmrZW!`ug1;NYF3&*<HHc%Cw?)ePIwL?8SSJy)Dgiy}z^F1Y`5j~tpiV3(;&~!^qmjixV@8"
    ">k0}4*9sD9Ih5%C{nF(Jp?hQ_8t>c-He<|*s@Kgrc0>%3%luz;>YUd&T(t93L<X*@=}N0$3)l3ts%Jy)3%X_5YvFLliee5Y1"
    "uKxx&Wv@FwxSix^<fLZrxL{z&Jjc%H>{sUSFj%N%kE7Gu6HLf_YIPbFM2?AQ*0rjM2MfOR7k~w7bHMOXiN)XMlwTV5COUL~`"
    "kqe>sQpW#JL;K$bOvh;b7r17Pe?+i$m+;)C#tQK&HlH_S96{HhS1XeGVnz*GTzSac;ceQ+1+3B0Qrsh6CKlb}QefP-U)toU2"
    "4#vyR=vdPXp@-qu`V6dgZ37jdIHPTxSgY7MhCYryHsb~C?v-EMUUtgpHJvKw&ykOKjrp|`avJ!T*n~)-oz(0{#L1Zzi1Xr?Y"
    "jkhu2)<o^i|5?ig9}dcqy6wYEcGzkH1W>U%68`eu}Y^BA!R-Z74nNXOz#!n7nPJ61!>Eo~M6}jXOqt^Wv{Q2>UCglya2LA#u"
    "~oyr^os7Az9Y<NC;8i@BDL1W2hzR7%IWVXS8!vi^NYz>DPlNxZu4dYQetiF0ql`ZOY-_RTVLMV*}~GaH)_Cq?s1JDyL8T2G`"
    "+nNnsXLm_!cbT>3-{2`-QRi`;x^?KJB1*s5oDjyQ+l!W}yB92$-C8&+LM7nR2AJ?dFn}q5R<o}w{`ZV=rLhHK3V;onTW;lu6"
    "4|9h_b3N~2HD~d-2{`VNla$mNy-=M$N6DtrWs%-(Y@Se+T6@j7wMn?^MxlL-<F3+*kGZ-!b-sGDL(qavSRJZgCzx3pl6z_46"
    "!5A|-=tw#-2@sfG~E+2|E;=vfN^H^*4vcp1zyq7_w5HRTa;d#>33Jit=?j7@u4{B;NcH*c~~O{<b8O(=YcWR0VPWNGI_O0-?"
    "czpRW)0{`|cHBZH^J~rb(`leyYf3xntI7iM&>&j0_p|+XQ=Xh`xA@*7hVN&JA2q;TpmjHEXHztm%AoOXDOJ%SHED&bZ{ZF!P"
    "u=A3ae2cPsUYz&2Z=7p*Jw^#UpQOeM!uhJn<1>QCLj%UuW5Tj0N+<Vq7@p~$FRk?>btng472tI?O8r~V5~7tD~Z_4CN`^uD&"
    "id-=-s^T1!sSk?%vGR^xRV4iLcl6QfBnniKUgeaG#xOR{1XB^1qcvK$x9P<FEbx^$AkHF!P^BL4WU^b<62+TWZP}VK-buX(B"
    "s^rO*(SM7a^_|?9MnPcjDrMzl#=V98n8lhVDT_6mze?_nS$DC@>H($sMT^5UNfTw0d!hMs4MLow9GbW6RWJN8-KD+o#J51E&"
    "VUC-apfXCfg=6OMW?xi5^VOvqS5poM$`ktsq%>0=z)0+F{}@tFR3wt6jIx7k`}R}x@ed5T3pdfr3yV$54~dIuX97tPd>{ukM"
    "+Jp+4`Y7fql?C&pc^j73b0DPMy&R<)k^<F`>nH>J}ZTF~1R#?jv%@60PRcj#Rx=abJ*!<sf4|XW@B_!P|&Hn^o>~K&!b<d<M"
    "{z8vShYd@-!+Wk45F(gkLL)oB6siT8)ShaEzS^iikGnm^d7lxP~AmJE7$Z@E(Dhp&MTuY;z}K>wYhEVx3O&HE<vSmPX}j>q6"
    "_dSu>qYf#%axX%seGnOq}J*9;9Iy|L^rvCjy@)^i!h5r(44vjm`Q!2Gc-vPOIl)03KQ!iaJT9NZ~pq@vG@y66@MrzC~I9d<R"
    "vMZ70jUv*B&yU8L_UjdA6&0!bwS3XC)hRgnCZ5%gJ&JXWI*kl!^~(hFcV3Put=1_Ee1x`6tTrq|>*G5S;~<_YBFdSB*3KYpm"
    "JqwDk+~k`$;ZKG3#=ee3QH*^tF%5^)U6FlpuE(HA)k?oNgWMlQDciMg@iq}Oh|0Gki@ioN|<YW<?W#!#@qt;-{JpW#5y#>wu"
    "0-Pz!9_Vb@!6{u{#G`X!OO)fRgJ_O3faPtg@+T`p;)38>R&tmbFXFR+wZYZ$LB>wF7%P3oW}qpJ@=%ZpC&~ErDs~VmnsQ0zK"
    "Z4{05Jel}0V|`Mh_iv|O>+zav#7#6sAGfrOZGhS$LSp)chRiudm{%j3OW%@Vx^eR#>KZ?KH(&#-<&W5V;SUP~zxDwHx_>o<s"
    "nx>a;FjNfbAkrl>(tE5x)%{Bw_U628%DR~p8l`11rqPOL%$~1T8m{W>r<qp6SS*8{aGTY0MuVbr;X=M?i)S`hMOW$V`5~Kdq"
    "b#m?gZ#wq?sd7+m!u}n>K4_iNJML}wihC9Oe+Ro(r=6kRY|(5m?*rB>j#IZduc!aWWI#Z<r94<LT9{|vaw~T2f_qq|=`-s-?"
    "EvR%<&Iush2EQHGt}N*VqIb{b0c+LchO=ZA-(#L^*@?BX;RxI2A6+chr9E-O^Qe<0~&n(&$-7%IqWG&{`at|d!V6ma^Ah*UW"
    "OJ(DF>Gz>#D4`Dp2dG<}R7d*EAmR`|l|sCQVc<x8waxjfQBpO#Sua*!O*azs6sw@6&b%MJ4Sf^1fqzKtRbp$DC`KJl>Hvohp"
    "gMs{WEJ?-ym1o@SUxyS$w=v;X}OEq8zJQBlqEIB4z_!1^dF<Sv5(jzKQW<C6tim&<rvp+xf*U_h9Cq~24%uScn}{voB`v{@R"
    "Y&5nP+4b(LWzPib5!2sh=5vu_N^zSQRoJE8p=rEP_N^jdq8S`9&&!KMQ>z2Li(6_VbyMLE#fIsQ_r9K|ZeSp1uRvwfqSo=9h"
    "+J|w~E%F2Ae8;i60&77R=&R40lxt8<_<FF2d#v&yA%8S%{VK)0cGe8&AzHlC_;!>$p_!s4C6&*9I_k=p^$!EIWSXpIOjs?s0"
    "&LY8qw&$bqzkr|!QRnteuvvuPth_ArIsV^epVd)Ztghfybc^+U=`CMIb*+!gYt{aG1VBQ_SS!s)<~G?c^^?N8D;3&X8=i+F)"
    "PiVUp9L~Eg7|6Z<Au~1CNPZbJr}h<}HZWvR(bOaCXZg-v{)OCmFMDQs*@(fm&S@z7Bb`0SmsWrj>boiCF>bk}`4Mg8jb;X|H"
    "iCjZvt-wra7OdS>_6&CYG`bw}&_|4r()1}QnE?c=TeopKD8L}yo(V$1Z9x5y{qA@#^*@YfW*eWmI(i*ZI4$<>t(Ny)rQv1~="
    "tU`q`KUnd%8kEn|i)~O=t;*oB=>AUabrm&6)z<q|*ye012RpYm^={fKDb$Gpz#X$p$Pc`WIXoT-JGvli1c0!}v;ioCRcCXua"
    "up(8flr`^ghxwFQ`Xz1WcQ(x8yD2RkU*)5cagKDAW|d-zLEM3UJ-)dPecFYMZkgD5J`eb>K-0bH)FNqNMJ?JnGqC=&er1uc7"
    "px+&!fLQZO1kETh_K(MqMM;DS!7JQlPgqRtr2g{bw4bhhV4HrY8#&h=ZyoZac0UQ);gz*HYZuGEXg2rj7oN*xKT#yaRzIA7g"
    "oCELDEGx-58k2y#YuyYrP3FP-~(cqm(CL1Aa)$x6Fuem6qqMMZ-ImUPt$@%L9FXi+0aEIa~QwBT<jTa?(icA$bZuuvU=PoyH"
    "t)vC>lMyTRCKN?+Dn&K-)5GI--INTa);PO>Uu{~T@Lgzi^~$prm7ojZlK-z!>ccb}*&th#I3{m31``WCw4;yxzsYhbHp@yEs"
    "iP4jU)6%<$nwM0Cw(dRlS2jKA($O}90`U%L%2|)e<u2g2Fsm9P_`l%sfs~sJmW)_Puf?e6L%kc&rbmM287h<!2)?<I`wo&RH"
    "$d7~mwt_En@Ib17e;KQJ)BOy8=OK4ziGyXv@Ydn4P%bvj=7};ND9+-wDdXH)O&++t;CAi8(DN_gn~y{OMZk|{Ui93fkdrlfV"
    "2)ALUaJ>LtZyXBxTtJc@%bH}Uth;V^bs@>cUe6hiLfsH6Zd<0?S~kG-KUw#WoWD);PEPS(<Q*K{>eNg;R<<r)uKVw%ob``l|"
    "z(qfyaQuS=+4d>SeU8&B}@zV*$@e%pCg-o=dB(7FZLyNNM7&rn-5O9S_gvtOAP)cKoV!xLbE|N4!D)$6cB~-XIJAHop~nF^#"
    "M56zx#?uG6ZpMNsAu*n=m5hefOVU9+5!_m;dDSU2ex8YMItsi|8GAU0|aSOJ?dVxhem4@r$x!`JCuJLV6|<S7B26rGQJdziz"
    "lDmXMe)LAR(J>3#HD$ep_-O$DxtfCIg>-6CN7xR0h#E9P<KDo*$@GU_9Havhg@i>Ra9N{k011=f=SG&C6hUr2NZPRwHL5sad"
    "0@Dw5T8h1*nfC!`|7G$*%e>SX_6=x6Z<4j;f%8^<=zJ7B%%qyv6fxrpHKX{HR-3boOSnP$w>I#?#z*X)8r~w;-EmlZ*Kr+%{"
    "C!vgxA6acX2UcmG>a9j(i$w<?pHTNgX?Ay1m+C~M!nwduQEccl?XmoQ0eM(@+;Nus~+|%H0T4|w9K*J+XjzWhd;H<V5jOMCB"
    "*9$!2Z*Am!ycy<L$;kM<)F7@F+Z;HyHi)(a5*C<1YaRml)-n0|zXTOV@Lv)vP9}ZgG%$Mh8hI5d(|THmFkqMkK1Np<ZLWJ2F"
    "2e1ov$dt#Z(a>!f)R9$%4l#Rc454`D#)VrtCTb~t2gEY5t7^e*|(Z5zcFHCL(ehr@5MhU*R}|04JOZTAz<!Y$~h)A(eZmEd0"
    "buNohevzT}%D()>}kB8835N1|__mTozV~#$}S!Rb7Pxrvz%F_p4qKwsQ>jhf-b&Jw@h{DVg2pHpOTUS7fSV%IPAT)}PyQE^!"
    "Wexb8XlgOCKO3He96pJ^D^BaUUIHbk-E$kTzX85DP7BRrKzF{t7)^~*pq5F2M&=_ltUkcUXge~YqZfCHBL*(BzpfWn!2QsPk"
    "BL&p1XeY{m`91VK~<|6^f}GA>wjcCo@73N=6!r^gwKgZlo_$vI<eW{aTXhDTQx=7{qNxg@Y`*`e1rWTXYlSVSSHJW{zuRN?|"
    "}nuPzMxP!7&eP6zH|ptlG1q2b*RI*0|gCtlmr4P%_Tk3`=MQ?=_MfF*7<W+W#}dzQ_i#+H%ttU#Mkr)q4?9M$7AZ!SlJZ2w0"
    "r$ablVBxJv@YT@tZv$Nkx`%ArZh`8#;rVC~m+_m2B99&fNm;v(~58vmKYxATmBmAK~(lkK6|!T~W+VOPp3tNc4Op!JzOG9ve"
    "i_7m)oF~;V#8}I?SK_5%2q^Iy|+Nz>_oVG$dHcW<fG+oE$Nv$#>F)5drzuCc3YW{+!j&-@<=|N*he=r<T9v1-nI4IyMDBv7)"
    "|Lg8W?EZ0gg%yE|tcSS9=-X{KXZv60qrx?MIaen|#I$9WvX0)A)lhBLjebn3tp8XA4J<GwzE{*%c9e^16-?3FXj*0^vMigg3"
    "-NtY&T`$+1`MR;-FM=io+2VrhnE5E%=QnhizsoAV*k}bQxANR`+v&)5b(dt9FTTNy~fHg%|vK-%p~)Ib@G1MaNx78P3wU0k;"
    "opo;u_}9Xgulx?DXTZ;It?An$zyIi-7u^RY7-Z$u#?S$D+`kIB&q-flgg~i?t5vUDj<%`_dU*`#O(KRIqKBNV?*~iP;xzcOz"
    "eOBeZ<`rAS-<9OVB?u>Vg&Mr&l?EcX8fFi<v6sA4%$9}StsyM9RUC8NoZUb}M2GV5kz*5+#7YZrS@@56qNx@VxNwCYfM@Dis"
    "op@d^DFk`26$-XN%$Z8rx(^rA<K-{Ity{`9h?S!}v2(#N@^~CmFM5&jMnsmkgEw5Egd*F|^7=^2X{(lPiUjXNS2w6Bu4`mFm"
    "Zc_HIu|7rPyjQIUM>`WV+w65wnbNqQ-Qr8MWCKci?L>c6Gy}X-)FWy`x@eu9_J<voHY+fCMZ1mXS!JXY)hBbbqdWd@Wcn@6q"
    "CjzG^CVW&kaT5$)@}Wk$^TBwxXs*xMoOQ{YahWOnRbqu`ySYz?@;o+4(``1@Raq&uCN-Uflrpq`Y*B%u5SH5TA#Z`YK-7Tlo"
    "BZ;UIFWIHv=b+%448_!=Qb=`b*6HUBESV0{_$Wx?`)kOROKh%6Pknyq7&qS{GCx<k4MGjZXA8q^I1maay+Lv2_Whu2T!=Bj<"
    "mbKMH-PHA;uDF9&2FxZnj)|A&wO#{fkEw6AeWU8iFVJYgQ#ce`m8e3d!*HQH$RW5={UXO~=}9PDHnwIihr-v1hGo}HXeFerZ"
    "m-FgQ&(3r}8sWbC2!@9{%HaReBs#6&k8V7VNg4p&w$>QCexOQZgVZzwDuh0=$kBoI}hnD-hymmyK#QyG;r{w^4q6m180s}`O"
    "`HymaON@zXmBO4={{+-nb#hdlGasg`r`3_OHse~?m?<8x>J{w{-Xp&XJ{V?)?jU;+j^O-t_CId3uF5q^zI87uG%qsD-bG#T$"
    "C>{Vcf~Y1QO<<&&`W|A`6xE}k4!JN+z<2bV*lTEe}`2(C7*|s`T%zSC9HlF8t^zMew^CBNT1|3yJED0TD#O{S&^vzi({8W$Z"
    "C151lRuCcQ`F!js0N0D*t}K-v({m$LQ`AMwql0f0C8gO=f$_77t&CImlr5&zhf$G8-V?5asR8ekEPi@om$N?XGN~w;}&i{xb"
    "IAW%oQF`;2@_w4?KNc!3wN_A8Lk<LvvtL5aM|%Aggj*3+k_v?_aB9qZ*|R-W#GjMp4mksgC%zFO;Zw#h#htqnc|3{>f39Rr>"
    "(vQD5z|G#DxbREst%&Pu^uDoBE!5{uylrQ;+7}vVyOHEU1otl>ipUIc7tH)vMz68ni3DL~kIY__@*!dXyehg6fxXcQ>zY2_k"
    ")@iAh%?k7tMhT-mQ~1pR?EgMF0j;5up~Rd;#cAcwugZQ%hdx+=Y76~@y(r84%`zowi*e&1>lO*ka|kmVSSz4bT_cNdcKi16T"
    "^??-A=bY!`W;)x{HFYQtXe(a*RYRIV7=P6p+3(CkO>R4cC}OaHmhQ_nrVjd%>_!PC31!O#zX92iP`VI4?C@r@Lh7-BG;}H54"
    "Oo?p=mU;6SB(ZB~acxt4e2x(Iv}>2Ik=hmN$vBSXcyJsxs3S-IeW$e=f?KZlH=ZlaTAU(9b4wS7_y_roRf_nqb}G6g#0-;RR"
    "1y^@D1N8GPCRb*l|H1e;~j_*>_jEHJ{M^I#Ui{~v=UT!egYQSz#$)T+0fd<A-N2mY3r8+^r`X18^N9@CV~1qidc=P;A{Q5FS"
    "_GcPFKkR8|<<4QkLCd6I&-_AEr=3k+GKL%QS9vrV(`4(-r0x3SUh)0F|u3aE?)@iAPAEPvEFju?A$rhSdUxuuI5PLled}>A8"
    "qUkTK$N!8x3_KLs6M7Z)&jnm-hIV47bFh<13A!dBtjE2=EG8QNT)Z>QWPbc}&~``tHp+=_<}Y9cr=S6U3cauX?H#UYkv@OTV"
    "t$pZgRjO2wZ<p5$O`FJZ8w$5zVBb_z>Dr)NWgheRm{qXDr>9mfo^#Q)W1*E*RSH5AL947Sb5VY)2?o_LVTTC#F$y>BOvcY^u"
    "sP&FzMRy_^t@wdM!l!5pwd+^EaS{-h-Tb0cRV9#@8H{M!i<y1>c5z*2-v={PUy%-+Nf1%+kJ4UlTRO>LktAFO!2001JoY3@N"
    "3~-PKCSee#5S0rtRV(U{tKP~13m-YhfB^-QCC{%>(UOVkzJ_4UtD7CDPHNWP7>{@ryi8!@s@3I8Uqlz0NPs2b@*R{Uuk=q*~"
    "O*VxOiR6M~LMhNRor@{=%46~M1R;s90)Cf*qnw%G<v@rl3aEaDh-PSw>>H0J*K<&<of$8^f-ATxuDx?2Z*1dE*bRRbfY|=|i"
    "i?(cY1n!1+<G#ilu<%jYuXsas%qQ|atWVH>|0!zwJ6O{TuuZfYT&4aj{c#`n*Z93gYcyLvPm5J;9PO{TNqbPaAdkN>$bcR2W"
    "{Os`+@Mc30{!~ykdnJaE1*Qi+~2r28SN~Ps_Lw)DqH-vl~KC4hr8umbQiSo21&QE79#E9kNB=5Q@5Ji&&gdq(ED21dJ9m$ir"
    "s$;Hh_A+bM)@UvaCnMoOqG-$%C8_p!M4+yCp-$F?H(KY5Z+rrJ|pEmQYUYgYWkx*g;!i|19FX6Yj6U1=oSk61|(6#fp74rOK"
    "|35@kWULC>Wda^CBF5dR!?q+J>Cv`ZqcQ^S$mAyH0KFa0W@Z-C~H;BgG}d4=+Dkrg;aQs_J@9emV3W|z;9EHEmfD_*cpeXV%"
    "j!z%6){riMAkWP7fO1>eR`AX|p7a)1w0q<$tWzo9&V%F$(GO9^et&5}Owmu=od;aU4a>>utJ|tZf@c-k4Kgww>;xIe)COH45"
    "0Ny+fZSWqbf6DT>zH+y2G4O~Li9XuZBii>`h8@3Ks?2#u^kIfL17n4ii+k`oU}f{Cu>U$yN$F(GX|C%HP}_N%Hxki;ESm+8v"
    "d&*bB+jheAj>I)T~&WA%RS#+;}vg^dTH15Iwd@qJ1jaQMr4W>|2XB^IA_6V=jd%(`~~*q`q>U;&csmfM`L#5PWwCW&<h+ErQ"
    "8WtE2Z?V7Z@>&q5JL;)de4uU%~$Gq^78_v-4HJeuP~YzW+I3_FE&TdC>`Dp~bxG^x0~x4UVh>CF+WQsCQep`j}+H&L<z?8>}"
    "C5e&|VX;{o>4T;}Y<9=Qk&bqlX=GBbOVwWw?4{eB!bW?j6gn`S;db$RwPO|lDEVB6{Jt&5b}I*n<O)si}`ui`!l3$W@Q0tVD"
    "N&}lfMz~cq1dyKVVT3@PBaqUhW<SdA$>(oAaj;Ps;v<ABb)_eJe#m}&--Iep~wh5Duu!8>2&;YE}Uu1>)0(RmY{FEbDgVqB~"
    "!Us6de)t7W^(rueUjt86+z=<Nsn$@BZ=WcB6eg{9(>iC(NaR>!eBD(U+tdoS$2osc>0e_9M*-7iR@tfL;b;7`++Jz1Qpiu2+"
    "#`dG4K=8R9q3VOC>xyg*knac#~$3wUhjfgjO`6pZ~74w;a`1s=zXX20aIGy8u`8ly!jf|p|cyONfQ%*E9A6|5_weXQJ2|K*k"
    "o<?G-p(-l5=*7?@rRJ@;r6fBKUl(Xs%kn|02$w7xk01d+|j`+^wLfD!D-?8w^M%gOkv5(7q3yKez@9rD?vAuMb<}9F(TbrU="
    "O&Emk*2T~McY?Rd9FQ19gb4*d-4dm3jNB^6$zo?e1p-U@p)Vpiw^ZM-Jq&{fOv#jMS0vBD+bH8nyvLatQ{_EEV^>tNn`L$rr"
    "Zd)}Ur)y!uZ7R@t`nf%_)p1sI2-Yv^|_?Y@OcGa$8CjyJyHaH)u(-U0FB0{Oj%8i;X?W%Z6x_n@z{}*BPJtf;=t&IWl_qc0y"
    ">qMzA9y!g(Nn{e&Pu+<bx8KVSyEfnJjGOJ8mZ$w@d*v$g8_Vn~Q7>5gU2k#r-W2xlv%tonyv<md?xwG3s9R<$$tpb}*3)Y3>"
    ";f(10;3m2@YV`53vJ8&bnIc5RfgSN0k}~TbYiA|I&>2ns00q40;gAKi`QB0QKZC4ITuy^^;Mg*k`v!=S*DIF;}`1x>V#0uU<"
    "HiftG2uWyp3DcdW)7!%t)Vl{>$(V)}Z~h^Km~rqibE=|52C6=QG=joWe6{(yzf85vfho@sqKfRUNfhsUCf#S8zA)D+azabj|"
    "7HzG-&2jMID3*y$F=Ew!5}VIR|8(H=F`#UnDu8MfNRxE-IiSg);<#+F&3tld$5l7m`y6-IS-F#@<o+6_5BXbKp(?7qUus3qo"
    "8LW8-U#p)x=Bl{}T0_V*58Hy3*g71av^p`ZqHO_Jp8>!%KEUeeY_Y94*vmvBz8I(h!)7_S7dt8SWSYyS$&cM6_Uahh_rAV68"
    "x_ymZ?_kH1=6A*zA6+C37Fjj1S(J;E!c+E=4B<@L+oh800?zx3!0R<uSgg{!jI86cM*Wd8mhb)Hls0z64vy43<j5*N(ri|2#"
    "O!**ByT6%8+FlreAoWJvq|$HTi8eEV4pk===XDKpVnyXkeihJzX15Juuig{5xoYz9?jot6}$G{jc^j=`+#!ADt0snT;Z&tJU"
    "!@H_VzpqYeOqbXP|X*oFA+`r*)h0*s#c6Xg*Mr_2V(U0-srKnI{}trAKI84WadkuTKY!tvV>l>YiiEh<3-o+@_dzjpBI<bo$"
    "${h4w<eT&7H0WHs|n=&w_>*2Y*38rxJija%)aKOb<m$yHVh2DIgOu)k@6nco7esv;*?Rowx305Vo{36F`Ne{<Gd;UuvwHV4p"
    "GH-%ZQw?Vz{xuIm$#=`#kwqYvHra~l)%m>WW#n}YwsH@)p?rgzt4z)=AT5)z7kp8B88v7r@|Jg}7zXq7Lf>YHV3gHu|e!RsM"
    "t}t?Uzi9V~#!D66ikoDFsBYaqo=yv#q2(vxJPO<I6+m2LACu+{Cah*_8+#*b%t4CyiE@rR?<=7jmer29*QwP$`m9cnRgcHk6"
    "&JEvGR$Zs?2`KHo?z;JFqAN^tr@Pf@L`^muK@#U{|-xqy$?%(sUK@Q2(MPB{V6T`84>Dr>;u$`j0r9=3Q}eLu%G;<`g4uiE1"
    "^}ZRDMt%kvCao>#OBe+nl$^(g^&J1~JuQPQ}N5yw|7xV{8_pk105ttD2a!OR{{xAT>(a=qT#?c0C5(ssCsVX?MXKYhK@hefn"
    "`&sGpLDK%3j3r=~f*bOEoGKR$$Yc$FTZmjRB`U1nH4q5l1x&A(Qev<dRyKF)5s#ag9h>J+X2dlr~cIiVH3lZ+XjW`~JN?|Vi"
    "2M~B4QKV|E!59#3zuzJ+nKdI#bomE!(ynEgDRj8|LRxcK3b#swb5X4>9&{uM6@ZPSvlkE0VOZZ9ox;zNkrakI)Nc6X{FNc7S"
    "SKM3f5@f`A=BBIcdRSxJsL9%mChIb%vRWs#iFG>674}W_lK!=Z=u?oU?=quwnYrcLoH&qJrOO`KCKXy!tLE7RX5Z)p;J_*ed"
    "nvEWoDLXK4*6qz)o9hG5xTB<kx`dlly=F#KhB-PIxaEtdB^<*?6OaS(hmb-_0wm-73Uzc9+8voCFX=K!6%xs>MV^Hl}OoT%B"
    "CDAtJcj{+9o<1!*_GH*c%Yj4jPcpWA$h8+jsHpHOQ-eIY-N*M2)ryzOs4?+c_E5XD^*qln&GGX>p#UpGQ}vUzM`X*yo!ojKW"
    "npoy5<E>)6|2R~)Q^ga4Ylf^{5mr#L0*SLDlB-C^+IPEm_}(dnG*&w}^fa<6kj)@64FpZUB{f%VW^I3d5p=?1fuIes?40B7S"
    "1qa(|Ny+TW=2&?A_*cLi%OX)zRtwtJ)oI29OS#}RXs_d02t?pIpU-y<!Ui=Pg{kNYHUI2a8>3Nq4`y3~rF3^Too3w895}9O7"
    "x~k_A_r2V^ocnPNJUI{k|FnDw^m$nJ0SDWm(Nt3H1^2(;w3|n3V&4Zx&sarVi4&)b*q1SOJdKhfOPu79r+;*v*`o>0plZMt7"
    "{T6r9`v*yI%Ni2cLEgOFN)J?dRl&3+(S6$E>=mT?8)iOw+K1g%fD+d+g@fpqE4X7lVh69Ij9v}pw?(vWTf4d0|-nCs7!b<cO"
    "B55VFsk?{-N9}4}$|9#^V4WyH4$^(>l(&<5=BA9Q77nPcq`C{*BIBFYu@;qhk>?!cEw=7u^VD`3yK~6raC<qkBawJsR$}AY*"
    "sI3b@JMLiH$4g3Fd5X>KqN8ghR2s@uUCT`lH28?=KW+W(uRX`J2W#Ht|~XWXN~S+$P2wUoJnCcCJ-#_QC;#TgH%%($An#4h|"
    "FV<$8^^?63;ehJWj43enCICPO!Q0ED~*2O5_stj1b`43`+lbixJ&B)kJPJ$l+4&LM36t%{WVGVx?*w#RgI=k@e^6Stuci0En"
    "Ck1w#pI`;*DAzvE{q7avw2TVxk5OXJvrdN(IoCt8l)jsMmAU7TSnyopb4PxbuCE`_t^z-WL}X*v(7D_zoc?wZSARsF0^HAn{"
    "vY7X`~woxig+C~e~K02*ElKd1IGC7kONzQLj8xWj0?r&JU^rJGAt;Sj`zta_S0Nt)^G@W_YL_6@|ftfkzUSc(_WA>fc+AvVb"
    "&(1R5&NE&X|aDn9j0WWt^`?F4uTZL@O*|{_P3TYP@-N8>P&|I99E9s;>R6=f!)=>$9*{bI0A!+)wb!E%4e8%U7_2pO9z32TB"
    "1dU*3e~dl9sGg7mNXk?Zu}3Y?Zxayn^x+-$K0;6Xb%Zo`tg1o*c=B5aqVkQlGf#!)ERkf-0oHQvTGHST_m(n+JO+6y<vZlLS"
    "r?N0TlP{OC|j+k&e#oKmmPE!j>otk-3IeN=%;5KVZn}l_dG+ehjU`NkXvR>(W?g%(qtM&F{EjQekz?+}Oc^{SgAp?6k59IIN"
    "Yrw)WO1=w_7MkVP{;g3~3Y59ZB0ZQA>v%@w7W05Q$)$=T4r8zXo_Cee88vmtzi-3BdL9(fCw}5wN*Y{Z4z3J}N^uUQ-2(d$Q"
    "_eVCBa}sAq|Lc!+Bxm)9u?ZbrX9mm>_Y9Ax=kPnnZ51je9@E>G9#;f@LI5%8^u*lbGC9H_Uutmz?0z4`|y5*RVv58`7d)O_P"
    "gNzH(3$2NE^6}9UP;L=)1#L=*KKzWg6Wc!`ZiqdP|SVPdHJyX7hVKCEtRLq4rb*QeJ1=pJT1X5+`9aIO$`vtTL7yaMEXJGn7"
    "=vZ{w7kHtjB7TbCC<pER(Zv>s}1jTZDna;q)c+K>fk^E?6bsZZvMfaoe@txjZ7&;D6Zz+upT-L(8A@a`MH!TX$vFbxT?NRQp"
    "mYtg#JWvhkPO2F;V`T?a{!aE(PcKA5#o0H%cKg+7>)W+TfZ=wvmehOSx23?)P->k(hcFQ31BMoL(=IGI>b*ma=Py&m1t&xgb"
    "gji=|>m74$GUndkY~~^O**gCv?yCP-kA`+?NdImAeXMO2QffQvGJ2u;4vXFism@&BQSkkFNI;d6TK{~56|$F^v0P=p@CxUFm"
    "#s6X#@Yte1`WGY&pcp!SbhXpXY5`LJE3QE#=OHhzX+K-jc?xOIn|QgPEJl4L1=KUO~Gbf?h>D4t<ksfUa`Md(kAM}70zNE;N"
    "-bM&K-<tK}MO>U(XG-4JUt|f0MfOUf^pV=ParI--+XIg4f4Ex36PuXE~8WJGMUr2fP8=o?vcgl{L^~TzQjOq6&Swlr=9AGar"
    "%D?#CH-l=C#T#$zY;{1~MCFzD@9<#E`0+I@0`HFU$!Jt^bpMN;V^x!2GAFR>cM&qL}5y~fOqYzFMB%m%E{&s05;(uYzSQG0W"
    "-D^KoeW_>!!|H!X_XIE&2?qC<nec*o0hUvcR6ws^e4p_p@zX2;j`yy|W+fKMqtAy3;xW7|Eryrzj{ZRqE|3_d8YhSU}(wA&<"
    ")EHw`o8@!3_Fi1=8tYD)@HKQ&Pfk)sHp`qFqqzi~Yo$7UnG!_j=){y03Hf-<W}~QF@KLZi#x9%AV`cfS7`SA!;70S>l~AN-s"
    "oHsmC?#AV)R(c|gcA#<Km|Gx<G9l~X{VsAuW(MHuaWVON>^u4g_Sb};y@?+Cam;da=zB%9$fD%yBxIgeh=l2_La0j`-h~;cv"
    "9Ua`VDjPO~WR`JDamU$mz!ssV$(L6Ir#R(&0A9o2{~DlQ$w(as}4!6jK*^%UCh-vEd=n$w3v)q1z|hIc5A3GoPcJ%2dLRzs@"
    "|ZRz$0%dIQuy2F_Ttxj1Xq4_ME7<9ruSLe5&@eIaJ7dSc4yor(J73b3mc0)sNnJE&;|(N;=b?fM_!{Ew7)ZCW2>+%*?=y&^2"
    "-?914u+YC}yj598ta1O4sDGl+4xiIT-&_5W~yTxetM@qTd<Q#OZcAsS@icZecdVsee``=|v^ilj>!ipCyZo5j!S0dc2+<{HZ"
    "VrnGR*Xpm*a~-5^E|7OszWWTC-l=7r_nXjcLL-~)8(1_a=&JSX^npcLq^r9o%J+Q?iB9v5jmM)b_OV_w8g1y0{pZ8IkoWhC@"
    "9<U|?FzlY1?;fi4PgS%Ebx9oFJk{s1NIjo1<pWvk2BW2#OR){jw#S5sL@aLmF(Vj)0~IqLe*+sv^hX!+moG?NAr|Xk?nLR0^"
    "D@*hTc~{;Wf3%-3>xnrN^1j&hs(AeybS?@1mD@1Lit3@N2^dMXfOPSk5tO(j;GB12nf-{i656&{;UsoK^L*dx11?3a>}G?iF"
    "f*IxSwsn#$kM=x>-YD~)_<C+uxzgZ%8Z-LQ-YSuIne>{`m^x_0(y6DL&rPViodtu8RMn(nG~umqeB=If#_*>uJvs}bpjKj_L"
    "Stv|jzJP2*4(Y;fUNfYFllyQS8-XB71-nB;gd*Fc&cvrBipnx~Q30EK?CW)(r6@jXMC-K_@QlbZ=9bcN2*L>k&(TRQ^u(xAG"
    "R+&4~{EF`OL7Z`#z094Sxy1I=-xttlSsT^?8f6*a&eRE=e6|PsHy}R)#rE-z5m7cH;-h3n)HNsJnPL59k6dGH=QRFrX1D$ws"
    "~h*Z?=!G}v?FMg@sLSag0F!JPBRX?0&I=pvnI3B*ZG^G+b3ENv{lrLO=;!oM42U8F{|`Lw}S!}m`5t`E@6TB{$9>^@|jKR)@"
    "oXmv&Cpzo_VPXEzK>kF3PlcQcf%yl2yBZTHGZi;ti5w{q?tobvEtmtn|4BSl{E+eVzKb==985qjLt3Yn8Uv>!0O(*fr3?F~G"
    "VVP@RXxpq8CRI&_wh&Wi09e=i2Dgjaff7E<6<@Rxc62gG+c4f1YGntjrHQ!H@ex}Q0dTHLc{J+2L#XjEq%RltmU#JG6CO6pD"
    "YDutC7gW$3u+7s*3PvQ-jSg)Vg$LEHdfa(}K@0ze_W&zKLY{S|vIgJC}FCjaDf8u6Y?{<RSQKOs|zL_;AYqTeByT5~-I7`es"
    "?we+Ohh>*Mg4OMUX8R%UD$>t-F`c4PvFSmA?;gi77uatW+I(&iKli0!wd#Ru8o$?>ZSb8ZO-|%&aZZ1mks+^7w2rUc)d}5^_"
    "EA@E)IXjcz65D@22h`+hSt9CJvhrrVB|^OKTb0ory%#<VO3WFFx+y_vvcJ-BYpRX=k<&3`;754S+%1wRp+{n;QPloUF%((TW"
    "$WQ<yFvqmG=D{qq&D*59|CT?T4GNJ6Z^{?xAHlQ^J~B<f3Z5;BDt8UN_DD*~FQ?+aL|b8L94<cmodBEr7_X>);y>*LmI7A=6"
    "GU27Quuk<`wIC$aVinX$cym4Co{!p(C=%~{?{Mkg5Gz|ph37o_IL&VrU|j5F<qC3%@MiU;Hgc~&$w^E~XQ9=w~Pc9{bvPC{;"
    "M#xEa-O?1xb{X}oma%eH0Fl6`tYSIF1X8F6CX~U4&a(@rKCTqqNb2~x3>X&M*x{v#IcfPi4@?X=er=$5{?9)Z;uJ>$oCdCd|"
    "XZOnqaJN>nAH@3RSrt1433&{EV>s`1P|X~0eUf?YgmVJ@tVVxF$9p*iSG(R0$|tD%ACVt13Z%4t5|~_bPvE>4N!yQsL(W6uO"
    "v278QKRTxpmbt$FZZy{9rt$!>#>>kUJ?i+U5jS#=p89M-n7r`I`2)^>5PoCZh`LV!2gopCiCoiJi_`dweS}>1+&FFI~<mWI6"
    "Hq9JEL`7AFyvz<wOs2L>jf5z-}LB2lsWxC1;%PsnklM1Ja`3uHCOw?z?!ki}yj*%*R83;1V;LPvX;4oVu+smDuXVJ%{?4zp2"
    "f;XxcRF$m+#<I0@R%bkvAPi__*cd(vR_!ZpgLR@cP)ja8t}<{yw*YMV2F>J8H0W#)4W^d2AMJ#<GTWxehg^I139v73W*(CPK"
    "(Sfg|mIMaKpgzSz^DB*@!>$+Vkocr-<y#7Au=utU~BXw@@Fy{@acl)&TQQ{uu%-yQZ{POkCo!RG|2^WsF8NL!rBZ6vSG<m17"
    "koSjdu-8iG%WUVY>2sWWED~FPhL4UeSuU`d+l5tLa+>YX7|(!w$Vso0Zk*j;dIjxPdI+2_&hDEJ+1GG}vCNnG3!R*GmbG&gV"
    "C6mby~eDT(ffa-%+|ND+k0>&J?BqoAvEcso^)F2_?$%asHS+Q*hQ;vb=K*>-T@z&ACNFBky?)3%Y?d3h1K4|K6YUgX-BD_IL"
    "ExokkswIAp;Uyo!MM&g7+vMfSwux$Lcg9?~&XFL~n5xiB7D23g2(${A%q2y2_6AOOS$ZgB}LtGx9p#UF1ZU8Z-Ji_VRkV)mY"
    "7L$oQuv&pgr!s4~y`FvX+rex<vC_eFXXzHcwcy8k+zK5e_xS<7|mUz^!Hkia~Llw4V%O*qFXlD;}v<wsup%#{Jo)^w&<-puL"
    "j^BSn~VXR^pUcek<Sl0p9o1l4(`j#Qh^gfy@xekj)BW?n2t%<)1Z{Q95;t(iG@0wS(s*%pUuL8F||KK6k{{NVF?kjV)$PHlW"
    "I_v8--gcRiXHX)O=Kc;KjqLuw-Q9lv-jB|7xHHdx$?nbIb9^EzoO<u?quH|Q6iutE>7&gbx$ore1sDDdR_Rl`Z)pfkP=I7s-"
    "Fg8MK|P(Dj43D%o&b&>7LANd0}`F=s?oy<-Ya<3dbyf5yCrl%HW^MI4|BpzFW`Ity#6Bac87Nh*O<g7LCf!hg8V(feXOEk6w"
    "oyLH@>UqvoqbMGZ7`WyHDw4%~eJo{BeVlm!?f7a3)DwRx1>{zsQY&{#Aw@fQ;5PP66iaa*$JKCqM(b(^vFPv7B1Hl@+S5@gA"
    "YCxi#KNeZ`{BTJ>{@vB1#g0fpH_B>nb2aKJsF``x0}gWhGp&pA%q$5{!Q7vHs9wP{)nt0joC-ruClhHqv4&rvoT#mn~!YXef"
    "&$a$}?*K(=8LZF?+1`_Q53~NxAnZJG<G;x_8%mG$yEpP|VfLgVmJrC+vYTYHeS4CRv1;%0>E3h?Vd7j$S(?O?~IWX+&U5WH="
    "ypvA5LoWb-H|h2HJOB9mBsFbzP-OSN46{eKCm(0pyp>J32s7I*&88xUcCV$n?Y5)!7*k8vs1yDl4rz3S"
)
# dem-blob:end


def _dem_embebido():
    """Decodifica la submuestra embebida: base85 → zlib → int16 (columna 0 absoluta, el resto deltas) → cumsum."""
    import base64
    import zlib

    d = np.frombuffer(zlib.decompress(base64.b85decode(_DEM_B85)), dtype="<i2").reshape(_DEM_N, _DEM_N)
    return np.cumsum(d, axis=1, dtype=np.int32).astype(np.float32)


def dem_precordillera():
    """Matriz de alturas (m, float32) del recorte de la Precordillera de Mendoza del DEM Copernicus GLO-30
    (`datos/dem_copernicus/README.md`): filas de norte a sur, columnas de oeste a este.

    Con el repo clonado carga `datos/dem_copernicus/dem_precordillera_512.npy` (512×512, paso 1″ ≈ 30 m, alturas
    1014.5–2988.8 m, media 1626 m), resuelto desde `__file__`, no desde el cwd. En el export WASM no hay disco ni
    `__file__`: devuelve la submuestra 128×128 (`a[::4, ::4]`, paso ≈ 120 m, alturas redondeadas al metro,
    1019–2982 m, media 1631 m) embebida en este archivo. Las dos dan casi la misma curva RMS vs k: para
    k = 1/2/5/10/20/50 el 512 da 102.9/66.0/30.6/16.9/9.8/4.4 m y la submuestra 103.5/66.4/30.8/17.0/9.8/3.8 m."""
    archivo = globals().get("__file__")
    if archivo:
        from pathlib import Path

        ruta = Path(archivo).resolve().parent.parent / _DEM_NPY
        if ruta.exists():
            return np.load(ruta).astype(np.float32)
    return _dem_embebido()


def rms_rango_k(Z, ks, centrar=False):
    """RMS (m) del error de la mejor aproximación de rango k de Z, para cada k de `ks`: {k: rms}. Con `centrar`
    trunca Z − media y vuelve a sumar la media, así la meseta no entra en la SVD (lección 09, sección 4)."""
    Z = np.asarray(Z, dtype=float)
    media = Z.mean() if centrar else 0.0
    U, s, Vt = np.linalg.svd(Z - media, full_matrices=False)
    return {int(k): float(np.sqrt(np.mean((Z - media - truncar_svd(U, s, Vt, k)) ** 2))) for k in ks}


# ----------------------------------------------------------------------------
# --- SVM de margen duro (lección 06, aporte CEIA) ---
# ----------------------------------------------------------------------------


def svm_margen_duro_2d(C1, C2):
    """El separador de margen máximo entre dos nubes 2D linealmente separables (SVM de margen duro), sin
    scikit-learn: la forma lineal afín w·x + b que lee ≤ −1 sobre C1 y ≥ +1 sobre C2 con el ancho 2/|w| máximo.

    Método: pares y tríos de soporte. En el plano, la franja más ancha entre dos envolventes convexas disjuntas es
    la mediatriz del segmento más corto entre ellas, y ese segmento va de vértice a vértice o de vértice a lado.
    Pruebo todos los candidatos geométricos: (i) un punto de cada clase, con la divisoria perpendicular al segmento
    que los une y por su punto medio; (ii) dos puntos de una clase y uno de la otra, con la divisoria paralela al
    lado y a mitad de camino del tercero. Cada candidato se normaliza para que sus puntos definitorios lean ∓1,
    se descarta si algún punto queda del lado equivocado o dentro de la franja, y entre los factibles gana el de
    ancho 2/|w| máximo (el óptimo es factible y está en la lista; ningún factible lo supera). Es O(n³) en la
    cantidad de puntos: alcanza para las nubes chicas de una lección; con nubes grandes o en más dimensiones hay
    que resolver el problema cuadrático dual, que es lo que hace una SVM de verdad.

    Devuelve un dict: `w` (2,), `b` (float), `margen` = 2/|w|, `u` = w/|w| (la normal unitaria, de C1 hacia C2),
    `soporte_1` y `soporte_2` (los puntos de cada clase que leen exactamente ∓1, arrays k×2). ValueError si las
    nubes no son linealmente separables (las envolventes se tocan)."""
    C1 = np.asarray(C1, dtype=float).reshape(-1, 2)
    C2 = np.asarray(C2, dtype=float).reshape(-1, 2)
    if len(C1) == 0 or len(C2) == 0:
        raise ValueError("hacen falta puntos de las dos clases")
    eps = 1e-9 * max(1.0, float(np.abs(np.vstack([C1, C2])).max()))

    def candidato(u, d1, d2):
        """u unitario de C1 hacia C2; d1, d2 = niveles u·x de los soportes de cada clase. Devuelve (w, b) o None."""
        gap = d2 - d1
        if gap <= eps:
            return None
        w, b = 2.0 * u / gap, -(d1 + d2) / gap  # así los soportes leen exactamente −1 y +1
        if np.all(C1 @ w + b <= -1 + 1e-7) and np.all(C2 @ w + b >= 1 - 1e-7):
            return w, float(b)
        return None

    candidatos = []
    for p in C1:  # (i) vértice–vértice
        for q in C2:
            n = np.linalg.norm(q - p)
            if n > eps:
                u = (q - p) / n
                candidatos.append(candidato(u, u @ p, u @ q))
    for X, Y, hacia_C2 in ((C1, C2, True), (C2, C1, False)):  # (ii) lado de una clase, vértice de la otra
        for i in range(len(X)):
            for j in range(i + 1, len(X)):
                e = X[j] - X[i]
                ne = np.linalg.norm(e)
                if ne <= eps:
                    continue
                for q in Y:
                    r = q - X[i]
                    n = r - (r @ e) / ne**2 * e  # la componente de r perpendicular al lado
                    nn = np.linalg.norm(n)
                    if nn <= eps:
                        continue
                    u = n / nn if hacia_C2 else -n / nn
                    candidatos.append(candidato(u, u @ X[i], u @ q) if hacia_C2 else candidato(u, u @ q, u @ X[i]))
    factibles = [c for c in candidatos if c is not None]
    if not factibles:
        raise ValueError("las dos nubes no son linealmente separables: no hay franja que las deje a los lados")
    w, b = max(factibles, key=lambda c: 2.0 / np.linalg.norm(c[0]))
    return {
        "w": w, "b": b, "margen": float(2.0 / np.linalg.norm(w)), "u": w / np.linalg.norm(w),
        "soporte_1": C1[np.abs(C1 @ w + b + 1.0) < 1e-6], "soporte_2": C2[np.abs(C2 @ w + b - 1.0) < 1e-6],
    }


# ----------------------------------------------------------------------------
# --- Hilo conductor (las 20 unidades) ---
# Cada unidad agrega un ladrillo sobre el anterior. `HILO_CONDUCTOR` dice, por unidad, de qué ladrillo se viene
# (y qué límite tenía), cuál se agrega hoy (con su escritura en numpy / cb104) y qué destraba en la siguiente.
# `bloque_hilo_conductor(id)` arma el bloque markdown que va debajo del título H1 de cada lección (mo.md).
# Las claves son los ids de mapa/_fragmentos/unidades.yaml, en el mismo orden; `anterior`/`siguiente` encadenan.
# ----------------------------------------------------------------------------

HILO_CONDUCTOR: dict[str, dict[str, str]] = {
    "00_desaprender_el_cbc": {
        "titulo": "Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia)",
        "venimos_de": (
            "Del CBC: vectores como flechas sueltas, el gradiente como una flecha más, la distancia siempre "
            r"$\sqrt{x^2 + y^2}$ y cada transformación resuelta aparte, sin un idioma común para encadenarlas."
        ),
        "ladrillo_de_hoy": (
            "Cinco ladrillos de idioma: las transformaciones forman un grupo (componer es `A @ B`, deshacer es "
            r"`np.linalg.inv`), los cuerpos $\mathbb R$ y $\mathbb C$, todo vector es un punto (`np.array([x, y])` es el "
            r"mojón y su flecha desde el origen a la vez), el dual $V^*$ donde el gradiente vive como fila $w^T$, y la "
            r"métrica $G$ que da el largo $v^T G v$ y será la primera forma fundamental."
        ),
        "vamos_hacia": (
            "Con el idioma puesto, la primera transformación del grupo: la rotación, donde el mojón se queda quieto "
            "y cambian sus coordenadas (unidad 01a)."
        ),
        "anterior": "",
        "siguiente": "01a_punto_quieto",
    },
    "01a_punto_quieto": {
        "titulo": "Rotaciones I: el punto no se movió",
        "venimos_de": (
            "La unidad 0 dejó el idioma (un vector es un punto, las transformaciones se componen), pero todavía "
            "ninguna transformación concreta."
        ),
        "ladrillo_de_hoy": (
            r"La rotación pasiva: giran los ejes $\theta$ y las coordenadas nuevas son $R^T p$, con `lib.rot2(theta)` "
            "y `lib.coordenadas_en_base(p, R)`; el punto no se mueve."
        ),
        "vamos_hacia": (
            r"Si en vez de los ejes giramos la parcela entera (rotación activa, $R\,p$), hace falta saber qué conserva $R$ "
            "y por qué su inversa es la transpuesta: unidad 01b."
        ),
        "anterior": "00_desaprender_el_cbc",
        "siguiente": "01b_rotacion_plano",
    },
    "01b_rotacion_plano": {
        "titulo": "Rotaciones II: la rotación en el plano",
        "venimos_de": (
            r"La unidad 01a dejó la rotación pasiva $R^T p$ y la inversa como transpuesta, sin decir qué define a una "
            "rotación ni por qué un espejo no lo es."
        ),
        "ladrillo_de_hoy": (
            r"La rotación activa $R(\theta)$ como matriz ortogonal, $R^T R = I$ y $\det R = +1$: sus columnas son a "
            r"dónde van $e_1, e_2$ (`lib.rot2`, `lib.transformar(nube, R)`), y el mismo giro como $e^{i\theta}$."
        ),
        "vamos_hacia": (
            r"En $\mathbb R^3$ un ángulo no alcanza: hay que decir alrededor de qué eje, y el orden de los giros "
            "importa: unidad 01c."
        ),
        "anterior": "01a_punto_quieto",
        "siguiente": "01c_rotaciones_3d",
    },
    "01c_rotaciones_3d": {
        "titulo": "Rotaciones III: tres ejes y el orden importa",
        "venimos_de": (
            r"La unidad 01b dejó $R(\theta)$ con $R^T R = I$, $\det = 1$ y $R(\alpha)R(\beta) = R(\alpha + \beta)$: "
            "en el plano los giros conmutan y no hay eje."
        ),
        "ladrillo_de_hoy": (
            r"Las rotaciones $R_x, R_y, R_z$ de $\mathbb R^3$ (`lib.rot_x`, `lib.rot_y`, `lib.rot_z`), la composición "
            "no conmutativa `Rz @ Ry` y Euler–Rodrigues: toda composición es un solo giro alrededor de un eje "
            "(`lib.rodrigues(eje, ang)`, `lib.eje_angulo(R)`)."
        ),
        "vamos_hacia": (
            r"Lo que $R$ conserva (largos, ángulos) es una cuenta $u^T v$; para medir desde las coordenadas hay que "
            "aislar esa cuenta: unidad 02."
        ),
        "anterior": "01b_rotacion_plano",
        "siguiente": "02_producto_interno",
    },
    "02_producto_interno": {
        "titulo": "Producto interno: proyección, longitud, ángulo",
        "venimos_de": (
            "La unidad 01c dejó las rotaciones 3D y la promesa de que conservan largos y ángulos, sin una cuenta que "
            "los mida desde las coordenadas."
        ),
        "ladrillo_de_hoy": (
            r"El producto interno $\langle u, v\rangle = u^T v$ (`u @ v`): largo $\sqrt{v^T v}$, ángulo por $\arccos$ y "
            r"proyección (`lib.proyeccion`, `lib.angulo`); invariante bajo $R$ porque $R^T R = I$."
        ),
        "vamos_hacia": (
            r"Con largos y ángulos medibles podemos clasificar lo que los conserva dando vuelta la hoja (espejo, "
            r"$\det = -1$) y lo que sólo conserva ángulos (similaridad $k\,R$): unidad 03."
        ),
        "anterior": "01c_rotaciones_3d",
        "siguiente": "03_reflexiones_similaridades",
    },
    "03_reflexiones_similaridades": {
        "titulo": "Reflexiones y similaridades",
        "venimos_de": (
            "La unidad 02 dejó el producto interno y la rotación como lo que lo conserva; faltaban las otras "
            r"ortogonales ($\det = -1$) y qué pasa al cambiar la escala."
        ),
        "ladrillo_de_hoy": (
            r"La reflexión $H(\alpha)$ con $\det = -1$ (`lib.reflexion2`) y la similaridad $S(x) = k\,R(\theta)\,x + t$ "
            r"con su centro fijo $(I - A)^{-1} t$ (`lib.similaridad`, `lib.centro_fijo`, `lib.similaridad_por_dos_puntos`)."
        ),
        "vamos_hacia": (
            r"Si cada eje se estira distinto se pierden los ángulos, y la traslación $t$ sigue sumada afuera de la "
            r"matriz; meterla adentro pide una $3\times3$: unidad 04."
        ),
        "anterior": "02_producto_interno",
        "siguiente": "04_afines_homogeneas",
    },
    "04_afines_homogeneas": {
        "titulo": "Afinidades y coordenadas homogéneas",
        "venimos_de": (
            r"La unidad 03 dejó la similaridad $k\,R\,x + t$, con $t$ sumado aparte y una $2\times2$ que no puede mover "
            "el origen."
        ),
        "ladrillo_de_hoy": (
            r"La afinidad $A x + t$ como $3\times3$ sobre homogéneas $(x, y, 1)$ (`lib.hom`, `lib.dehom`, "
            "`lib.matriz_afin(A, t)`, `lib.afin_por_tres_puntos`): componer es `M2 @ M1` y el área va "
            r"$\times \det A$."
        ),
        "vamos_hacia": (
            r"La fila $(0\ 0\ 1)$ es lo que mantiene las paralelas; si la liberamos, las paralelas se cruzan como en una "
            "foto y hacen falta cuatro puntos: unidad 05."
        ),
        "anterior": "03_reflexiones_similaridades",
        "siguiente": "05_proyectivas",
    },
    "05_proyectivas": {
        "titulo": "Proyectivas: la foto del dron y el pentágono del profesor",
        "venimos_de": (
            r"La unidad 04 dejó la $3\times3$ afín con última fila $(0\ 0\ 1)$: paralelas a paralelas y tres puntos la "
            "fijan; una foto inclinada no cumple eso."
        ),
        "ladrillo_de_hoy": (
            r"La homografía $p' \sim H p$ sobre rayos $(x, y, W)$ con $H$ de $3\times3$ cualquiera "
            r"(`lib.homografia_4puntos`, `lib.aplicar_proyectiva`), la recta al infinito $W = 0$ "
            "(`lib.recta_al_infinito`) y la razón doble (`lib.razon_doble`)."
        ),
        "vamos_hacia": (
            r"Las rectas $\ell^T p = 0$ se transforman con $H^{-T}$, al revés que los puntos; para entender eso "
            "necesitamos el dual: unidad 06."
        ),
        "anterior": "04_afines_homogeneas",
        "siguiente": "06_formas_lineales",
    },
    "06_formas_lineales": {
        "titulo": "Formas lineales y dualidad",
        "venimos_de": (
            r"La unidad 05 dejó puntos como rayos y rectas como ternas $\ell$ con $\ell^T p = 0$, sin explicar por qué "
            "la recta se transforma al revés que el punto."
        ),
        "ladrillo_de_hoy": (
            r"La forma lineal $w^T$ como fila (una regla graduada, `w @ p`), el espacio dual $V^*$ y la regla "
            r"arrastrada $w A^{-1}$ para que la lectura no cambie (`lib.forma_transformada`, `lib.rectas_de_nivel`, "
            "`lib.recta_por_dos_puntos`)."
        ),
        "vamos_hacia": (
            r"La recta por dos puntos salió de un producto cruz $\tilde p \times \tilde q$: detectar que tres mojones "
            "están alineados pide la cuña y el determinante: unidad 07a."
        ),
        "anterior": "05_proyectivas",
        "siguiente": "07a_cuna_determinante",
    },
    "07a_cuna_determinante": {
        "titulo": "Cuña y determinante: el detector de colinealidad",
        "venimos_de": (
            r"La unidad 06 dejó la forma lineal $w^T$ y la recta por dos puntos como $\tilde p \times \tilde q$, un "
            "producto que todavía no tenía nombre ni reglas."
        ),
        "ladrillo_de_hoy": (
            r"El producto cuña $u \wedge v = u_1 v_2 - u_2 v_1$ (`lib.cuna2`, `lib.cuna3`) y el determinante "
            "`np.linalg.det` como área o volumen orientado: cero exactamente cuando hay colinealidad (`lib.alineados`)."
        ),
        "vamos_hacia": (
            r"Cuando el determinante da cero una dirección entera va al cero (el núcleo), y restando $\lambda I$ "
            "aparecen las direcciones que no giran: unidad 07b."
        ),
        "anterior": "06_formas_lineales",
        "siguiente": "07b_nucleo_autovectores",
    },
    "07b_nucleo_autovectores": {
        "titulo": "Núcleo y autovectores: las direcciones que no giran",
        "venimos_de": (
            r"La unidad 07a dejó $\det A = 0$ como detector de colapso, sin decir qué dirección se aplasta ni cuáles "
            "sobreviven sin girar."
        ),
        "ladrillo_de_hoy": (
            r"El núcleo $\{v : A v = 0\}$ (`lib.nucleo2`) y los autovectores $A v = \lambda v$ vía "
            r"$\det(A - \lambda I) = 0$ (`lib.autovalores_reales`, `lib.autovectores_cuna`, `np.linalg.eig`)."
        ),
        "vamos_hacia": (
            r"En $\mathbb R^3$ el polinomio es cúbico y siempre tiene una raíz real: el eje de la rotación y el punto "
            r"fijo de la $3\times3$ homogénea: unidad 07c."
        ),
        "anterior": "07a_cuna_determinante",
        "siguiente": "07c_autovalores_3d_puntos_fijos",
    },
    "07c_autovalores_3d_puntos_fijos": {
        "titulo": "Autovalores en 3D y puntos fijos proyectivos",
        "venimos_de": (
            r"La unidad 07b dejó $A v = \lambda v$ en el plano, con el autovector perpendicular a una fila de "
            r"$A - \lambda I$; en 3D hace falta la cruz de dos filas."
        ),
        "ladrillo_de_hoy": (
            r"Autovectores en $\mathbb R^3$ como `np.cross` de dos filas de $A - \lambda I$: el eje de una rotación "
            r"($\lambda = 1$) y los puntos fijos de una homografía (`lib.puntos_fijos_proyectivos(H)`), que son los "
            r"subespacios invariantes de $\mathbb R^3$."
        ),
        "vamos_hacia": (
            r"Con los autovectores como ejes nuevos la matriz se vuelve diagonal: el cambio de base $B^{-1} A B$, "
            "unidad 08."
        ),
        "anterior": "07b_nucleo_autovectores",
        "siguiente": "08_cambio_de_base",
    },
    "08_cambio_de_base": {
        "titulo": "Cambio de base y diagonalización",
        "venimos_de": (
            "La unidad 07c dejó los autovectores como direcciones que no giran, sin usarlos todavía como grilla para "
            "medir."
        ),
        "ladrillo_de_hoy": (
            r"La matriz de cambio de base $B$ (columnas = ejes nuevos): $c = B^{-1} p$ (`np.linalg.solve(B, p)`), la "
            r"transformación en la grilla nueva $B^{-1} A B$ y la diagonalización $A = B \Lambda B^{-1}$ "
            "(`lib.diagonalizar`)."
        ),
        "vamos_hacia": (
            "La grilla propia no siempre existe (un giro no tiene ejes propios reales); con dos grillas ortogonales, "
            "una a la entrada y otra a la salida, siempre existe: la SVD, unidad 09."
        ),
        "anterior": "07c_autovalores_3d_puntos_fijos",
        "siguiente": "09_cambio_de_base_svd",
    },
    "09_cambio_de_base_svd": {
        "titulo": "Cambio de base, SVD e inversas",
        "venimos_de": (
            r"La unidad 08 dejó $A = B \Lambda B^{-1}$, que sólo existe con autovectores reales y sobre una base en "
            "general oblicua."
        ),
        "ladrillo_de_hoy": (
            r"La SVD $A = U \Sigma V^T$ (`np.linalg.svd`, `lib.svd2`): dos bases ortonormales con "
            r"$A^T A = V \Sigma^2 V^T$, la inversa $V \Sigma^{-1} U^T$ y la pseudoinversa $A^{+}$ "
            "(`lib.pseudoinversa`, `np.linalg.lstsq`) con sus cuatro subespacios (`lib.cuatro_subespacios`)."
        ),
        "vamos_hacia": (
            r"Una $3\times2$ cuya imagen es un plano tangente y cuya contra-imagen es la normal: la jacobiana de una "
            "superficie, unidad 10."
        ),
        "anterior": "08_cambio_de_base",
        "siguiente": "10_jacobiano_primera_forma",
    },
    "10_jacobiano_primera_forma": {
        "titulo": "Jacobiano y primera forma fundamental",
        "venimos_de": (
            "La unidad 09 dejó la SVD y la pseudoinversa para una matriz fija; el terreno no es una matriz fija sino "
            "una transformación lineal que cambia de punto a punto."
        ),
        "ladrillo_de_hoy": (
            r"El jacobiano $J = [\,r_u\ r_v\,]$ de $3\times2$ (`lib.jacobiana_numerica`) y la primera forma "
            r"fundamental $G = J^T J$ con $E, F, G$ (`lib.primera_forma`): el largo de un paso $d$ es "
            r"$\sqrt{d^T G d}$ (`lib.longitud_paso`)."
        ),
        "vamos_hacia": (
            r"La tabla $J^T J$ de productos internos de las columnas reaparece como $A^T A$ en las ecuaciones normales: "
            "con más mediciones que incógnitas, la solución es la que deja el residuo perpendicular a las columnas, "
            "unidad 11."
        ),
        "anterior": "09_cambio_de_base_svd",
        "siguiente": "11_cuatro_problemas",
    },
    "11_cuatro_problemas": {
        "titulo": "Cuatro problemas: regresión, círculos, Procrustes, regresión total",
        "venimos_de": (
            r"La unidad 10 dejó $J^T J$, la tabla de productos internos de las columnas; con mediciones redundantes "
            r"$A x = y$ no tiene solución y la misma tabla $A^T A$ decide."
        ),
        "ladrillo_de_hoy": (
            r"Las ecuaciones normales $A^T A\, x = A^T y$ (`np.linalg.lstsq`, `lib.minimos_cuadrados`) cuatro veces: "
            r"recta de ajuste, punto por distancias, Procrustes $R = V U^T$ y regresión total por el autovector menor "
            r"de $X_0^T X_0$ (`lib.recta_ajuste`, `lib.punto_por_distancias`, `lib.procrustes`, `lib.regresion_total`)."
        ),
        "vamos_hacia": (
            r"$X_0^T X_0$ es una forma cuadrática y sus direcciones propias son extremos; sobre una superficie esa "
            "misma estructura mide cuánto se aparta del plano tangente: la curvatura, unidad 12."
        ),
        "anterior": "10_jacobiano_primera_forma",
        "siguiente": "12_curvatura",
    },
    "12_curvatura": {
        "titulo": "Curvatura como forma cuadrática",
        "venimos_de": (
            r"La unidad 11 dejó la forma cuadrática $x^T C x$ con sus direcciones propias como extremos; la primera "
            r"forma $I = d^T G d$ de la unidad 10 mide largos pero no cuánto se dobla la superficie."
        ),
        "ladrillo_de_hoy": (
            r"La segunda forma fundamental $II(d) = L\,du^2 + 2M\,du\,dv + N\,dv^2$ (`lib.formas_fundamentales`), la "
            r"curvatura normal $\kappa_n = II / I$ (`lib.curvatura_normal`), las principales como autovalores de "
            r"$I^{-1} II$ (`lib.curvaturas_principales`) y $K = \kappa_1 \kappa_2$ (`lib.curvatura_gauss`)."
        ),
        "vamos_hacia": (
            r"Una superficie concreta donde todo sale de una sola simetría: el elipsoide, con $\kappa_1 = 1/M$, "
            r"$\kappa_2 = 1/N$ y la normal que no pasa por el centro: unidad 13."
        ),
        "anterior": "11_cuatro_problemas",
        "siguiente": "13_elipsoide",
    },
    "13_elipsoide": {
        "titulo": "Geometría del elipsoide",
        "venimos_de": (
            r"La unidad 12 dejó $\kappa_1, \kappa_2$ y $K$ para una superficie genérica; falta la superficie que usa "
            "la geodesia."
        ),
        "ladrillo_de_hoy": (
            r"El elipsoide de revolución $a, f, e^2 = 2f - f^2$ (`lib.elipsoide`, `lib.elipsoide_grs80`): los radios "
            r"$M$ y $N$ (`lib.radios_curvatura`), las tres latitudes $\varphi, \psi, \beta$ (`lib.latitudes`) y "
            r"$(\varphi, \lambda, h) \to (X, Y, Z)$ (`lib.geodesica_a_cartesiana`)."
        ),
        "vamos_hacia": (
            r"Entre tres vértices lejanos sobre la superficie los lados son arcos y los ángulos no suman $180°$; "
            "sobre la esfera hay fórmula cerrada: unidad 14."
        ),
        "anterior": "12_curvatura",
        "siguiente": "14_trigonometria_esferica",
    },
    "14_trigonometria_esferica": {
        "titulo": "Trigonometría esférica",
        "venimos_de": (
            r"La unidad 13 dejó el elipsoide con sus radios $M, N$ y la conversión a cartesianas; faltan los "
            "triángulos trazados sobre la superficie."
        ),
        "ladrillo_de_hoy": (
            "El triángulo esférico como tres vectores unitarios desde el centro: lados por producto interno "
            r"$\cos a = \langle B, C\rangle$, ángulos entre normales `np.cross`, ley del seno por la cuña $[A, B, C]$ y "
            r"el exceso $A + B + C - \pi$ igual al área (`lib.triangulo_esferico`, `lib.exceso_esferico`)."
        ),
        "vamos_hacia": (
            "Queda abierto para Topografía y Geodesia: compensar poligonales con el exceso separado y los problemas "
            "directo e inverso sobre el elipsoide, donde ya no hay fórmula cerrada."
        ),
        "anterior": "13_elipsoide",
        "siguiente": "15_transformaciones_conformes",
    },
    "15_transformaciones_conformes": {
        "titulo": "Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico",
        "venimos_de": (
            "La unidad 14 cerró la geometría sobre la esfera y el elipsoide, y la unidad 12 (curvatura) mostró que "
            r"$K = 1/(MN) > 0$: no hay manera de aplanar el elipsoide sin deformar; falta decidir qué se sacrifica."
        ),
        "ladrillo_de_hoy": (
            r"Conforme $\iff$ Jacobiano = similaridad directa $\iff$ $\sigma_1 = \sigma_2$ (Tissot círculo) $\iff$ "
            r"$F = 0$, $E = G$ $\iff$ Cauchy-Riemann; la latitud isométrica $q(\varphi)$ y Mercator "
            "(`lib.latitud_isometrica`, `lib.escalas_proyeccion_cilindrica`, `lib.defecto_conformidad_jacobiano`)."
        ),
        "vamos_hacia": (
            r"Gauss-Krüger / POSGAR como función analítica de $q + i\,\Delta\lambda$: el cierre del arco, de la "
            "clase 1 (el número complejo que gira) a la clase 13 (el elipsoide que se proyecta)."
        ),
        "anterior": "14_trigonometria_esferica",
        "siguiente": "",
    },
}



def mesa_interactiva(mo_mod, figura_o_widget, *controles_y_bloques, proporcion=(10, 6)):
    """Layout estándar de las secciones interactivas: figura a la IZQUIERDA (10/16) y, a la DERECHA (6/16),
    el panel con el selector de caso, los deslizadores y los números vivos. Pensado para pantallas 16:9 con la
    columna de marimo ensanchada a 1240 px (tools/build.py inyecta ese ancho en el export).

    Uso: `lib.mesa_interactiva(mo, mo.ui.plotly(fig), mo.md("**Controles**"), caso, s1, s2, mo.md(numeros))`.
    Si ya tenés el panel armado como un vstack, pasalo como único bloque."""
    bloques = list(controles_y_bloques)
    panel = bloques[0] if len(bloques) == 1 else mo_mod.vstack(bloques, gap=0.55)
    return mo_mod.hstack([figura_o_widget, panel], widths=list(proporcion), align="start", gap=1.25)

def video_loop(nombre_base, pie=""):
    """HTML de una animación en bucle (`animaciones/<nombre_base>.mp4`) para `mo.Html(...)`: se reproduce sola,
    en bucle continuo, muda y sin controles, como un GIF en HD. La ruta es relativa al export en
    `site/unidades/<id>/` (tools/build.py copia `animaciones/` a `site/animaciones/`). `pie`: una frase al pie."""
    return (
        f'<figure style="margin:0.5rem 0;text-align:center">'
        f'<video src="../../animaciones/{nombre_base}.mp4" autoplay loop muted playsinline '
        f'style="max-width:100%;border-radius:8px;border:1px solid #d8d3c8"></video>'
        f'<figcaption style="font-size:0.85rem;color:#5f6368;margin-top:0.25rem">{pie}</figcaption></figure>'
    )

def bloque_hilo_conductor(unidad_id):
    """Markdown para `mo.md(...)`: el hilo conductor de una unidad (de dónde viene, qué ladrillo agrega, a dónde va)
    con enlaces relativos a la unidad anterior y a la siguiente (`../<id>/index.html`, como en los anexos)."""
    if unidad_id not in HILO_CONDUCTOR:
        raise KeyError(f"{unidad_id!r} no es una unidad de HILO_CONDUCTOR: {list(HILO_CONDUCTOR)}")
    h = HILO_CONDUCTOR[unidad_id]
    lineas = [
        "**El hilo conductor (ladrillo a ladrillo)**",
        "",
        f"- **Venimos de:** {h['venimos_de']}",
        f"- **Ladrillo de hoy:** {h['ladrillo_de_hoy']}",
        f"- **Vamos hacia:** {h['vamos_hacia']}",
    ]
    enlaces = []
    if h["anterior"]:
        enlaces.append(f"[← Unidad anterior: {HILO_CONDUCTOR[h['anterior']]['titulo']}](../{h['anterior']}/index.html)")
    if h["siguiente"]:
        enlaces.append(f"[Unidad siguiente: {HILO_CONDUCTOR[h['siguiente']]['titulo']} →](../{h['siguiente']}/index.html)")
    if enlaces:
        lineas += ["", " · ".join(enlaces)]
    return "\n".join(lineas)


_NIVELES = ("elemental", "medio", "avanzado")


def opciones_barajadas(opciones, semilla=None):
    """Devuelve un dict nuevo con los mismos pares etiqueta → valor de `opciones`, en orden barajado.
    Con `semilla` el orden es reproducible; sin ella cambia en cada llamada. Uso:
    `mo.ui.radio(options=lib.opciones_barajadas({...}))`."""
    azar = random.Random(semilla) if semilla is not None else random.Random()
    pares = list(opciones.items())
    azar.shuffle(pares)
    return dict(pares)


def preparar_autoevaluacion(mo_mod, unidad_id, semilla=None):
    """Arma la tanda de autoevaluación de una unidad: devuelve `(tanda, radios)`. `tanda` son las 6 preguntas del
    banco (copias), ordenadas elemental → medio → avanzado con orden aleatorio dentro de cada nivel y las 4
    opciones barajadas; `radios` es un `mo.ui.array` con un `mo.ui.radio` por pregunta (sin respuesta marcada,
    valor = id de la opción elegida). Con `semilla` es reproducible."""
    if unidad_id not in BANCO_AUTOEVALUACION:
        raise KeyError(f"{unidad_id!r} no está en BANCO_AUTOEVALUACION: {list(BANCO_AUTOEVALUACION)}")
    azar = random.Random(semilla) if semilla is not None else random.Random()
    banco = BANCO_AUTOEVALUACION[unidad_id]
    tanda = []
    for nivel in _NIVELES:
        del_nivel = [dict(q, opciones=[dict(o) for o in q["opciones"]]) for q in banco if q["nivel"] == nivel]
        azar.shuffle(del_nivel)
        tanda += del_nivel
    for q in tanda:
        azar.shuffle(q["opciones"])
    radios = []
    for n, q in enumerate(tanda, start=1):
        opciones = {}
        for o in q["opciones"]:
            clave = o["texto"]
            while clave in opciones:
                clave += " "
            opciones[clave] = o["id"]
        radios.append(mo_mod.ui.radio(options=opciones, value=None, label=f"**{n}. ({q['nivel']})** {q['enunciado']}"))
    return tanda, mo_mod.ui.array(radios)


def corregir_autoevaluacion(mo_mod, tanda, radios):
    """Corrección de la tanda: un callout por pregunta respondida (verde si acierta, ámbar si no, con la
    explicación y la opción correcta) y, al final, el puntaje total con el desglose por nivel cuando están
    todas respondidas (si no, cuántas faltan). Devuelve un `mo.vstack`."""
    elegidas = list(radios.value) if radios.value is not None else [None] * len(tanda)
    bloques = []
    aciertos = {n: [0, 0] for n in _NIVELES}
    faltan = 0
    for i, (q, elegida) in enumerate(zip(tanda, elegidas), start=1):
        if elegida is None:
            faltan += 1
            continue
        por_id = {o["id"]: o for o in q["opciones"]}
        correcta = next(o for o in q["opciones"] if o["correcta"])
        aciertos[q["nivel"]][1] += 1
        if elegida == correcta["id"]:
            aciertos[q["nivel"]][0] += 1
            bloques.append(mo_mod.callout(mo_mod.md(f"**{i}. Correcto.** {correcta['explicacion']}"), kind="success"))
        else:
            bloques.append(mo_mod.callout(mo_mod.md(
                f"**{i}. No.** {por_id[elegida]['explicacion']} **La correcta era:** {correcta['texto']} "
                f"{correcta['explicacion']}"), kind="warn"))
    if faltan:
        bloques.append(mo_mod.callout(mo_mod.md(f"Faltan responder {faltan} preguntas"), kind="neutral"))
    else:
        k = sum(a for a, _ in aciertos.values())
        total = len(tanda)
        desglose = " · ".join(f"{n} {a}/{t}" for n, (a, t) in aciertos.items())
        bloques.append(mo_mod.callout(mo_mod.md(f"**Puntaje: {k} de {total}**  \n{desglose}"),
                                      kind="success" if k == total else "info"))
    return mo_mod.vstack(bloques)


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
    # lección 03: reflexiones y similaridades
    assert exacto(reflexion2(0.0), np.diag([1, -1])) and exacto(reflexion2(np.pi / 4), [[0, 1], [1, 0]]), "espejos del eje x y de y = x"
    assert exacto(reflexion2(th) @ reflexion2(th), np.eye(2)) and exacto(np.linalg.det(reflexion2(th)), -1.0), "involución, det −1"
    assert exacto(reflexion2(np.deg2rad(30)) @ reflexion2(0.0), rot2(np.deg2rad(60))), "dos espejos a 30° = R(60°)"
    assert exacto(reflexion2(th) @ reflexion2(0.3), rot2(2 * (th - 0.3))), "H(a) H(b) = R(2(a − b))"
    _As, _ts = similaridad(np.sqrt(2), np.pi / 4, [3, -2])
    assert exacto(_As, [[1, -1], [1, 1]]) and exacto(_ts, [3, -2]) and exacto(np.linalg.det(_As), 2.0), "√2·R(45°): det = k²"
    assert exacto(partes_similaridad(_As), [np.sqrt(2), np.pi / 4]) and exacto(partes_similaridad(0.5 * rot2(-1.2)), [0.5, -1.2])
    try:
        partes_similaridad([[1, 0.5], [0, 1]])
        raise AssertionError("un corte no es similaridad")
    except ValueError:
        pass
    assert exacto(centro_fijo(_As, _ts), [2, 3]) and exacto(_As @ [2, 3] + _ts, [2, 3]), "centro (2, 3): F(c) = c"
    assert centro_fijo(np.eye(2), [1, 0]) is None, "una traslación no tiene centro"
    assert exacto(centro_fijo(0.5 * rot2(np.pi / 4), [0.29289322, 0.08578644]), [1 - np.sqrt(2) / 2] * 2, tol=1e-7), "apunte 16"
    _A2, _t2 = similaridad_por_dos_puntos([1, 2], [4, 1], [2, 1], [6, 3])
    assert exacto(_A2, _As) and exacto(_t2, _ts) and exacto(_A2 @ [2, 4] + _t2, [1, 4]), "z ↦ (1 + i) z + (3 − 2i); (2, 4) ↦ (1, 4)"
    _tr = trayectoria(rot2(np.pi / 2), [0, 0], [1, 0], 4)
    assert _tr.shape == (5, 2) and exacto(_tr[1], [0, 1]) and exacto(_tr[4], [1, 0]), "cuatro cuartos de vuelta cierran el círculo"
    assert exacto(trayectoria(2 * np.eye(2), [0, 0], [1, 1], 3)[-1], [8, 8]), "homotecia: sobre el rayo"
    _xs, _ys = estelas_afin([[1, 0]], [(np.eye(2), [0, 0]), (_As, _ts)])
    assert len(_xs) == 3 and _xs[2] is None and exacto([_xs[1], _ys[1]], _As @ [1, 0] + _ts)
    # lección 06: formas lineales
    assert exacto(forma_transformada([2, 1], np.diag([2.0, 1.0])), [1, 1]), "lección 06: (2,1) diag(2,1)⁻¹ = (1,1)"
    A06 = np.array([[1.2, 0.5], [-0.1, 1.3]])
    assert exacto(forma_transformada([1, 1], A06) @ (A06 @ [3, 4]), 7.0) and exacto(forma_transformada([-1, 2], A06) @ (A06 @ [3, 4]), 5.0), "30/9: la séptima con la quinta"
    assert exacto(forma_transformada([1, 1], A06), np.array([1.4, 0.7]) / 1.61), "30/9: (1,1) T⁻¹ por adjunta sobre determinante"
    assert exacto(forma_transformada([2, 3], [[1, 1], [0, 2]]), [2, 0.5]), "apunte 11: ψ = φ A⁻¹ = (2, 1/2)"
    assert exacto(forma_transformada([2, 1], rot2(th)), rot2(th) @ [2, 1]), "con una rotación la fila gira como un punto"
    try:
        forma_transformada([1, 1], [[1, 2], [2, 4]])
        raise AssertionError("forma_transformada con det 0 tiene que fallar")
    except ValueError:
        pass
    r06 = recta_por_dos_puntos([1, 1], [3, 2])
    assert exacto(r06, [-1, 2, -1]) and exacto(r06 @ hom([1, 1]), 0.0) and exacto(r06 @ hom([3, 2]), 0.0), "recta por (1,1) y (3,2): −x + 2y − 1 = 0"
    assert exacto(recta_por_dos_puntos([3, 2], [1, 1]), -r06), "la cuña es antisimétrica: misma recta, otro signo"
    try:
        recta_por_dos_puntos([1, 1], [1, 1])
        raise AssertionError("recta por un solo punto tiene que fallar")
    except ValueError:
        pass
    assert cortes_caja([2, 1], 0, 5).shape == (2, 2) and cortes_caja([2, 1], 100, 5).shape == (0, 2) and cortes_caja([1, 0], 3, 5).shape == (2, 2)
    assert exacto(np.sort(cortes_caja([1, 0], 3, 5)[:, 1]), [-5, 5]) and exacto(cortes_caja([2, 1], 0, 5) @ [2, 1], [0, 0])
    assert cortes_caja([1, 1], 10, 5).shape == (1, 2), "la recta por la esquina corta una sola vez"
    f06 = figura_plano(5)
    rectas_de_nivel(f06, [2, 1], range(-10, 11, 2), 5)
    assert len(f06.data) == 3, "rectas_de_nivel agrega tres trazas"
    # lección 09: SVD, inversa y pseudoinversa
    _A9 = np.array([[2.0, 1.0], [0.0, 1.0]])
    _U9, _s9, _Vt9 = svd2(_A9)
    assert exacto(_U9 @ np.diag(_s9) @ _Vt9, _A9) and exacto(np.linalg.det(_Vt9), 1.0) and _Vt9[0, 0] > 0, "svd2: A = U Σ Vᵀ con V rotación"
    assert exacto(_s9, [(1 + np.sqrt(5)) / np.sqrt(2), (np.sqrt(5) - 1) / np.sqrt(2)]) and exacto(_s9[0] * _s9[1], 2.0), "σ de [[2,1],[0,1]]: ((1+√5)/√2, (√5−1)/√2)"
    assert exacto(_s9**2, np.linalg.eigvalsh(_A9.T @ _A9)[::-1]), "σ² = autovalores de AᵀA"
    assert exacto((_A9 @ _Vt9[0]) @ (_A9 @ _Vt9[1]), 0.0), "v₁ ⊥ v₂ y sus imágenes siguen perpendiculares"
    _Ud, _sd, _Vtd = svd2(np.diag([3.0, -2.0]))
    assert exacto(_sd, [3, 2]) and exacto(_Ud, np.diag([1, -1])) and exacto(_Vtd, np.eye(2)), "diag(3, −2): el signo va a U"
    assert exacto(svd2(rot2(0.7))[1], [1, 1]) and exacto(svd2(rot2(0.7))[0], rot2(0.7)), "un giro: Σ = I, el giro en U"
    _Us, _ss, _Vts = svd2([[3.0, 1.0], [1.0, 2.0]])
    assert exacto(_ss, np.abs(diagonalizar([[3.0, 1.0], [1.0, 2.0]])[0])) and exacto(np.abs(_Us), np.abs(_Vts.T)), "simétrica: σ = |λ| y U = V salvo signos"
    _P9 = np.array([[1.0, 2.0], [2.0, 4.0]])
    assert exacto(pseudoinversa(_P9), _P9 / 25) and exacto(_P9 @ pseudoinversa(_P9) @ _P9, _P9), "P⁺ = P/25, P P⁺ P = P"
    assert exacto(pseudoinversa(np.diag([3.0, -2.0])), np.diag([1 / 3, -1 / 2])), "sin σ = 0, A⁺ = A⁻¹"
    _A3 = np.column_stack([[0.0, 1.0, 2.0], np.ones(3)])
    assert exacto(pseudoinversa(_A3), np.linalg.pinv(_A3)) and exacto(pseudoinversa(_A3) @ [0, 1, 3], [1.5, -1 / 6]), "ficha 10: A⁺y = (1.5, −1/6)"
    assert exacto(pseudoinversa([[1.0, 1.0], [2.0, 2.0]]), np.linalg.pinv([[1.0, 1.0], [2.0, 2.0]])), "no simétrica singular: coincide con pinv"
    _c4 = cuatro_subespacios(_A3)
    assert _c4["rango"] == 2 and _c4["imagen"].shape == (3, 2) and _c4["contra_imagen"].shape == (3, 1) and _c4["coimagen"].shape == (2, 2) and _c4["nucleo"].shape == (2, 0)
    assert exacto(_A3.T @ _c4["contra_imagen"], [[0], [0]]), "la contra-imagen es el núcleo de Aᵀ"
    _r9 = np.array([0, 1, 3]) - _A3 @ minimos_cuadrados(_A3, [0, 1, 3])[0]
    assert exacto(float(_r9 @ _c4["contra_imagen"][:, 0]) * _c4["contra_imagen"][:, 0], _r9), "el residuo vive en la contra-imagen"
    _c4 = cuatro_subespacios(_P9)
    assert _c4["rango"] == 1 and exacto(np.abs(_c4["nucleo"][:, 0]), [2, 1] / np.sqrt(5)) and exacto(_P9 @ _c4["nucleo"][:, 0], [0, 0]), "núcleo de [[1,2],[2,4]]: (2, −1)"
    _M9 = np.random.default_rng(9).normal(size=(5, 4))
    _U9, _s9, _Vt9 = np.linalg.svd(_M9)
    assert exacto(truncar_svd(_U9, _s9, _Vt9, 4), _M9) and np.linalg.matrix_rank(truncar_svd(_U9, _s9, _Vt9, 2)) == 2, "truncar_svd: k = todo devuelve la matriz; k = 2 tiene rango 2"
    assert elipse_imagen(np.diag([3.0, 2.0]), 5).shape == (5, 2) and exacto(elipse_imagen(np.diag([3.0, 2.0]), 5)[0], [3, 0])
    # --- Proyectivas (lección 05) ---
    _P5 = pentagono_profesor()
    assert exacto(_P5[3], [0, 1]) and exacto(np.linalg.norm(_P5, axis=1), np.ones(5)) and exacto(_P5[2], rot2(np.deg2rad(72)) @ [0, 1]), "planilla: D = (0, 1), C = R(72°) D"
    assert exacto(abs(area_poligono(_P5)), abs(area_poligono(pentagono_regular(1.0)))) and area_poligono(_P5) < 0, "el mismo pentágono que pentagono_regular(1), recorrido horario"
    _Hp, _lam = homografia_lambda(_P5[[0, 1, 2, 4]], _P5[[0, 1, 4, 2]])
    assert exacto(_Hp, [[-np.sqrt(5), 0, 0], [0, -1, 1], [0, 4, 1]]), "planilla del profesor: H = [[−√5, 0, 0], [0, −1, 1], [0, 4, 1]]"
    assert exacto(_lam, [-np.sqrt(5), -np.sqrt(5), np.sqrt(5), np.sqrt(5)]), "λ = (−√5, −√5, √5, √5): A y B con W negativa, la imagen se parte"
    assert exacto(aplicar_proyectiva(_P5, _Hp), np.vstack([_P5[[0, 1, 4]], [[0, 0]], _P5[[2]]])), "A, B fijos, C ↔ E y D cae en el centro"
    assert exacto(homografia_4puntos(_P5[[0, 1, 2, 4]], _P5[[0, 1, 4, 2]]), _Hp), "DLT (8×9) y sistema λ (13×13) dan la misma H"
    assert exacto(_Hp @ _Hp, 5 * np.eye(3)) and exacto(recta_al_infinito(_Hp), [0, 4, 1]), "homología armónica H² ~ I; se va al infinito la recta 4y + 1 = 0"
    _pf5 = puntos_fijos_proyectivos(_Hp)
    assert [p["lam"] for p in _pf5] == [round(np.sqrt(5), 6), round(-np.sqrt(5), 6)] and exacto(_pf5[0]["punto"], [0, 1 / (1 + np.sqrt(5))], tol=1e-5) and _pf5[1]["plano"], "centro (0, 0.309) sobre CE; eje = recta de puntos fijos"
    assert exacto(_pf5[1]["recta"] / _pf5[1]["recta"][1], [0, 1, -_P5[0, 1]], tol=1e-5), "el eje es la recta AB: y = −0.809"
    assert exacto(razon_doble(1.0, 0.0, 1 / (1 + np.sqrt(5)), _P5[0, 1]), -1.0) and exacto(razon_doble([0, 1], [0, 0], [0, 1 / (1 + np.sqrt(5))], [0, _P5[0, 1]]), -1.0), "(D, D'; O, X) = −1: cuaterna armónica"
    assert exacto(razon_doble(0, 2, 1, 3), -1 / 3) and exacto(razon_doble(0, 1, 2, 3), 4 / 3)
    _terr5 = np.array([[0, 0], [4, 0], [4, 4], [0, 4]], dtype=float)
    _foto5 = np.array([[0, 0], [4, 0], [3, 2], [1, 2]], dtype=float)
    _Hf = homografia_4puntos(_terr5, _foto5)
    assert exacto(_Hf, [[1, 0.5, 0], [0, 1, 0], [0, 0.25, 1]]), "foto de dron: H = [[1, 0.5, 0], [0, 1, 0], [0, 0.25, 1]]"
    assert exacto(aplicar_proyectiva(_terr5, _Hf), _foto5) and exacto(aplicar_proyectiva([[2, 2]], _Hf), [[2, 4 / 3]]), "el centro del lote cae en (2, 4/3), el cruce de las diagonales"
    assert exacto(dehom(_Hf @ [0, 1, 0]), [2, 4]) and dehom(_Hf @ [1, 0, 0]) is None, "punto de fuga de las rectas x = cte en (2, 4); las y = cte siguen paralelas"
    assert exacto(homografia_4puntos(np.vstack([_terr5, [[2, 2]]]), np.vstack([_foto5, [[2, 4 / 3]]])), _Hf), "con cinco pares compatibles, lstsq da la misma H"
    assert exacto(homografia_lambda(_terr5, _foto5)[0], _Hf) and exacto(homografia_4puntos(_foto5, _terr5) @ _Hf, np.eye(3)), "la rectificación es H⁻¹"
    _cx, _cy = curva_proyectiva(_P5, _Hp)
    assert sum(x is None for x in _cx) > 5 and any(x is not None and abs(x) > 2 for x in _cx), "el pentágono partido: cortes extra y puntos que se van lejos"
    _gx, _gy = grilla_proyectiva(np.eye(3), 2, 1, n=3)
    assert len(_gx) == 10 * 4 and exacto([v for v in _gx if v is not None][:3], [-2, -2, -2]), "con H = I la grilla proyectiva es la grilla"
    _ex, _ey = estelas_proyectivas([[0, 1]], [np.eye(3), _Hp])
    assert len(_ex) == 3 and exacto([_ex[0], _ey[0], _ex[1], _ey[1]], [0, 1, 0, 0]), "estela de D: de (0, 1) al centro"
    # --- DEM Precordillera (lección 09): submuestra embebida y, si está en disco, el 512 completo ---
    _D = _dem_embebido()
    assert _D.shape == (128, 128) and _D.dtype == np.float32, "submuestra embebida 128×128 float32"
    assert 1018 <= _D.min() <= 1020 and 2981 <= _D.max() <= 2983 and 1625 <= _D.mean() <= 1636, "submuestra: alturas 1019–2982 m, media ≈ 1631 m"
    _r = rms_rango_k(_D, [1, 10])
    assert 102 <= _r[1] <= 105 and 16.5 <= _r[10] <= 17.5, "submuestra: RMS k = 1 ≈ 103.5 m, k = 10 ≈ 17.0 m"
    assert rms_rango_k(_D, [1], centrar=True)[1] < _r[1], "con la media restada, k = 1 sin meseta aproxima mejor"
    _Z = dem_precordillera()
    if _Z.shape == (512, 512):  # con el repo clonado: el recorte completo, los números de svd_results_512.json
        assert 1014 <= _Z.min() <= 1015 and 2988 <= _Z.max() <= 2989 and 1625 <= _Z.mean() <= 1627, "512: alturas 1014.5–2988.8 m, media 1626 m"
        _r = rms_rango_k(_Z, [1, 10])
        assert 102 <= _r[1] <= 105 and 16.5 <= _r[10] <= 17.5, "512: RMS k = 1 = 102.9 m, k = 10 = 16.9 m"
        assert exacto(_Z[::4, ::4], _D, tol=0.5), "la submuestra embebida es a[::4, ::4] al metro"
    else:
        assert _Z.shape == (128, 128), "sin el .npy en disco se usa la submuestra"
    # --- SVM de margen duro (lección 06, aporte CEIA) ---
    _s = svm_margen_duro_2d([[0, 0], [1, 0], [0, 1]], [[3, 3], [4, 3], [3, 4]])
    assert exacto(_s["w"], [0.4, 0.4]) and exacto(_s["b"], -1.4) and exacto(_s["margen"], 5 / np.sqrt(2)), "lado (1,0)–(0,1) contra (3,3): x + y = 3.5, ancho 5/√2"
    assert exacto(_s["soporte_1"], [[1, 0], [0, 1]]) and exacto(_s["soporte_2"], [[3, 3]]) and exacto(_s["u"], [1, 1] / np.sqrt(2)), "tres soportes: (1,0), (0,1) y (3,3)"
    _s = svm_margen_duro_2d([[0, 0], [1, 0], [0, 1]], [[3, 0], [4, 0], [3, 1]])
    assert exacto(_s["w"], [1, 0]) and exacto(_s["b"], -2.0) and exacto(_s["margen"], 2.0) and exacto(_s["soporte_1"], [[1, 0]]), "vértice–vértice (1,0)–(3,0): x = 2, ancho 2 (el lado x + y = 1 da sólo √2)"
    _nA, _nB = np.array([[0, 0], [2, 0], [0, 2], [0.5, 0.5]], dtype=float), np.array([[4, 3], [6, 3], [4, 5], [5, 6]], dtype=float)
    _s = svm_margen_duro_2d(_nA, _nB)
    assert exacto(_s["w"], [0.4, 0.4]) and exacto(_s["b"], -1.8) and exacto(_s["soporte_1"], [[2, 0], [0, 2]]) and exacto(_s["soporte_2"], [[4, 3]]), "las dos parcelas de 06: x + y = 4.5, soportes (2,0), (0,2), (4,3)"
    _t = svm_margen_duro_2d(_nB, _nA)
    assert exacto(_t["w"], -_s["w"]) and exacto(_t["b"], -_s["b"]), "intercambiar las clases cambia el signo de la forma"
    _D2 = np.diag([2.0, 1.0])
    assert exacto(transformar(_nA, _D2) @ forma_transformada(_s["w"], _D2) + _s["b"], _nA @ _s["w"] + _s["b"]), "la regla arrastrada (w A⁻¹, b) lee lo mismo sobre A x"
    assert exacto(2 / np.linalg.norm(forma_transformada(_s["w"], _D2)), np.sqrt(20)), "pero el ancho físico cambia: 5/√2 → √20"
    _s2 = svm_margen_duro_2d(transformar(_nA, _D2), transformar(_nB, _D2))
    assert exacto(_s2["w"], [0.32, 0.24]) and exacto(_s2["margen"], 5.0) and exacto(_s2["soporte_1"], [[4, 0]]) and exacto(_s2["soporte_2"], [[8, 3]]), "re-entrenada sobre A x: otra divisoria, ancho 5 > √20"
    try:
        svm_margen_duro_2d([[0, 0], [2, 2]], [[1, 1], [3, 0]])
        raise AssertionError("nubes que se tocan tienen que dar ValueError")
    except ValueError:
        pass
    # --- transformaciones conformes (lección 15): latitud isométrica, escalas cilíndricas, defecto de conformidad ---
    _e = np.sqrt(_GRS80["e2"])
    assert exacto(latitud_isometrica(0.0), 0.0), "q(0) = 0"
    _ph = np.deg2rad(np.array([-54.0, -34.6, 10.0, 60.0]))
    assert exacto(latitud_isometrica(_ph, 0.0), np.log(np.tan(np.pi / 4 + _ph / 2))), "con e = 0, q = ln tan(π/4 + φ/2)"
    assert exacto(latitud_isometrica(-_ph), -latitud_isometrica(_ph)), "q es impar"
    _d = 1e-5
    _qp = (latitud_isometrica(0.5 + _d) - latitud_isometrica(0.5 - _d)) / (2 * _d)
    _M5, _N5 = radios_curvatura(0.5)
    assert abs(_qp - _M5 / (_N5 * np.cos(0.5))) / (_M5 / (_N5 * np.cos(0.5))) < 1e-6, "dq/dφ = M/(N cos φ)"
    assert exacto(arco_meridiano(0.0), 0.0) and exacto(arco_meridiano(np.pi / 2), 10001965.729, tol=0.01), "S(90°) GRS80 = 10 001 965.729 m"
    assert exacto(arco_meridiano(np.pi / 2, 1.0, 0.0), np.pi / 2), "esfera unidad: S(90°) = π/2"
    for _p in np.deg2rad([-54.0, -34.6, 20.0, 65.0]):
        _y, _h, _k, _w = escalas_proyeccion_cilindrica(_p, "conforme_mercator")
        assert abs(_h - _k) < 1e-12 and _w == 0.0, "Mercator: h = k, ω = 0"
        assert exacto(_y, _GRS80["a"] * latitud_isometrica(_p)), "Mercator: y = a q(φ)"
        _y, _h, _k, _w = escalas_proyeccion_cilindrica(_p, "equidistante")
        assert _h == 1.0 and exacto(_y, arco_meridiano(_p)), "equidistante: h = 1, y = S(φ)"
        _y, _h, _k, _w = escalas_proyeccion_cilindrica(_p, "equivalente")
        assert abs(_h * _k - 1) < 1e-12, "equivalente: h k = 1"
        assert _w > 0 and exacto(_w, np.rad2deg(2 * np.arcsin(abs(_h - _k) / (_h + _k)))), "ω_max = 2 arcsin(|h − k|/(h + k))"
    for _t in ("conforme_mercator", "equidistante", "equivalente"):
        _y, _h, _k, _w = escalas_proyeccion_cilindrica(0.0, _t)
        assert exacto([_y, _h, _k, _w], [0.0, 1.0, 1.0, 0.0]), f"{_t}: en el ecuador h = k = 1"
    _y54 = escalas_proyeccion_cilindrica(np.deg2rad(-54.0), "equivalente")[0]
    assert exacto(_y54, -np.sin(np.deg2rad(54.0)) * _GRS80["a"], tol=0.01 * _GRS80["a"]), "equivalente: y ≈ a sin φ (esfera) a menos de 1 %"
    try:
        escalas_proyeccion_cilindrica(0.3, "gnomonica")
        raise AssertionError("tipo desconocido tiene que dar ValueError")
    except ValueError:
        pass
    _Jc = np.array([[3.0, -4.0], [4.0, 3.0]])
    _dc = defecto_conformidad_jacobiano(_Jc)
    assert exacto(_dc["parte_anticonforme"], np.zeros((2, 2))) and exacto(_dc["razon"], 1.0) and exacto(_dc["def_angular_max_deg"], 0.0), "[[a, −b], [b, a]] es conforme"
    assert exacto(_dc["sigmas"], [5.0, 5.0]), "σ = √(a² + b²)"
    _dd = defecto_conformidad_jacobiano(np.diag([2.0, 1.0]))
    assert exacto(_dd["def_angular_max_deg"], np.rad2deg(2 * np.arcsin(1 / 3))) and exacto(_dd["sigmas"], [2.0, 1.0]), "diag(2, 1): ω = 2 arcsin(1/3)"
    _Jr = np.array([[1.0, 2.0], [-0.5, 3.0]])
    _dr = defecto_conformidad_jacobiano(_Jr)
    assert exacto(_dr["parte_conforme"] + _dr["parte_anticonforme"], _Jr), "conforme + anticonforme = J"
    assert exacto(_dr["parte_conforme"], [[2.0, 1.25], [-1.25, 2.0]]), "parte conforme de [[1, 2], [−0.5, 3]]"
    _J54 = np.diag(escalas_proyeccion_cilindrica(np.deg2rad(-54.0), "equidistante")[1:3][::-1])  # diag(k, h)
    assert 29.0 < defecto_conformidad_jacobiano(_J54)["def_angular_max_deg"] < 31.0, "equidistante en −54°: ω_max ≈ 30°"
    # --- Hilo conductor (las 20 unidades): claves = ids de unidades.yaml en orden, cadenas consistentes ---
    import re as _re
    from pathlib import Path as _Path
    _yaml_txt = (_Path(__file__).resolve().parent.parent / "mapa" / "_fragmentos" / "unidades.yaml").read_text(encoding="utf-8")
    try:
        import yaml as _yaml
        _ids_yaml = [u["id"] for u in _yaml.safe_load(_yaml_txt)["unidades"]]
    except ImportError:
        _ids_yaml = _re.findall(r"^  - id: (\S+)\s*$", _yaml_txt, flags=_re.M)
    assert len(_ids_yaml) == 20, f"unidades.yaml debería listar 20 unidades, lista {len(_ids_yaml)}"
    assert list(HILO_CONDUCTOR) == _ids_yaml, f"HILO_CONDUCTOR != unidades.yaml:\n{list(HILO_CONDUCTOR)}\n{_ids_yaml}"
    _campos = ("titulo", "venimos_de", "ladrillo_de_hoy", "vamos_hacia", "anterior", "siguiente")
    for _i, (_uid, _h) in enumerate(HILO_CONDUCTOR.items()):
        assert tuple(_h) == _campos, f"{_uid}: campos {tuple(_h)}"
        for _c in _campos:
            if (_uid, _c) in {(_ids_yaml[0], "anterior"), (_ids_yaml[-1], "siguiente")}:
                assert _h[_c] == "", f"{_uid}.{_c} tiene que ser vacío en el extremo"
            else:
                assert _h[_c].strip(), f"{_uid}.{_c} vacío"
        assert _h["anterior"] == ("" if _i == 0 else _ids_yaml[_i - 1]), f"{_uid}.anterior"
        assert _h["siguiente"] == ("" if _i == len(_ids_yaml) - 1 else _ids_yaml[_i + 1]), f"{_uid}.siguiente"
        for _k in ("anterior", "siguiente"):
            assert _h[_k] == "" or _h[_k] in HILO_CONDUCTOR, f"{_uid}.{_k} = {_h[_k]!r} no es una unidad"
        if _h["siguiente"]:
            assert HILO_CONDUCTOR[_h["siguiente"]]["anterior"] == _uid, f"cadena rota en {_uid} → {_h['siguiente']}"
        if _h["anterior"]:
            assert HILO_CONDUCTOR[_h["anterior"]]["siguiente"] == _uid, f"cadena rota en {_h['anterior']} → {_uid}"
        for _c in ("venimos_de", "ladrillo_de_hoy", "vamos_hacia"):
            for _m in _re.findall(r"\$[^$]*\$", _h[_c]):
                assert "|" not in _m, f"{_uid}.{_c}: '|' dentro de $..$ ({_m}); usar \\lvert \\rvert"
            assert "estaci" not in _h[_c].lower(), f"{_uid}.{_c}: se dice 'unidad', no 'estación'"
            for _fn in _re.findall(r"`lib\.(\w+)", _h[_c]):
                assert _fn in globals() and callable(globals()[_fn]), f"{_uid}.{_c}: lib.{_fn} no existe en cb104"
        _b = bloque_hilo_conductor(_uid)
        assert "Ladrillo de hoy" in _b and "Venimos de" in _b and "Vamos hacia" in _b and "estaci" not in _b.lower()
        assert ("Unidad anterior" in _b) == bool(_h["anterior"]) and ("Unidad siguiente" in _b) == bool(_h["siguiente"])
        if _h["siguiente"]:
            assert f"](../{_h['siguiente']}/index.html)" in _b, f"{_uid}: falta el enlace a la siguiente"
    assert "Unidad anterior" not in bloque_hilo_conductor(_ids_yaml[0]) and "Unidad siguiente" in bloque_hilo_conductor(_ids_yaml[0])
    assert "Unidad siguiente" not in bloque_hilo_conductor(_ids_yaml[-1]) and "Unidad anterior" in bloque_hilo_conductor(_ids_yaml[-1])
    try:
        bloque_hilo_conductor("99_no_existe")
        raise AssertionError("un id desconocido tiene que dar KeyError")
    except KeyError:
        pass
    # --- autoevaluación (banco + motor) ---
    assert set(HILO_CONDUCTOR) <= set(BANCO_AUTOEVALUACION), "faltan unidades en el banco"
    for _uid, _qs in BANCO_AUTOEVALUACION.items():
        assert len(_qs) == 6 and [sum(q["nivel"] == n for q in _qs) for n in _NIVELES] == [2, 2, 2], _uid
        for _q in _qs:
            assert _q["enunciado"].strip(), _uid
            assert [o["id"] for o in _q["opciones"]] == list("abcd"), (_uid, _q["id"])
            assert sum(bool(o["correcta"]) for o in _q["opciones"]) == 1, (_uid, _q["id"])
            assert all(o["texto"].strip() and o["explicacion"].strip() for o in _q["opciones"]), (_uid, _q["id"])
    _d = {f"op{i}": i for i in range(8)}
    assert list(opciones_barajadas(_d, 3)) == list(opciones_barajadas(_d, 3))
    assert dict(opciones_barajadas(_d, 3)) == _d and len(opciones_barajadas(_d)) == 8
    _s2 = next(s for s in range(100) if list(opciones_barajadas(_d, s)) != list(opciones_barajadas(_d, 3)))
    assert list(opciones_barajadas(_d, _s2)) != list(opciones_barajadas(_d, 3))

    class _Mock:
        class ui:
            array = staticmethod(lambda elementos: types.SimpleNamespace(elementos=list(elementos), value=None))
            radio = staticmethod(lambda **kw: types.SimpleNamespace(**kw))
        md = staticmethod(lambda t: ("md", t))
        callout = staticmethod(lambda c, kind="neutral": ("callout", kind, c))
        vstack = staticmethod(lambda b: list(b))

    import types
    _uid0 = next(iter(HILO_CONDUCTOR))
    _copia = repr(BANCO_AUTOEVALUACION)
    _t, _r = preparar_autoevaluacion(_Mock, _uid0, semilla=1)
    assert repr(BANCO_AUTOEVALUACION) == _copia, "el banco no se debe mutar"
    assert len(_t) == 6 and len(_r.elementos) == 6
    assert [q["nivel"] for q in _t] == ["elemental"] * 2 + ["medio"] * 2 + ["avanzado"] * 2
    assert all(r.value is None and len(r.options) == 4 for r in _r.elementos)
    assert _r.elementos[0].label.startswith("**1. (elemental)**")
    try:
        preparar_autoevaluacion(_Mock, "99_no_existe")
        raise AssertionError("un id desconocido tiene que dar KeyError")
    except KeyError:
        pass
    _r.value = [next(o["id"] for o in q["opciones"] if o["correcta"]) for q in _t]
    _c = corregir_autoevaluacion(_Mock, _t, _r)
    assert [x[1] for x in _c] == ["success"] * 6 + ["success"] and "Puntaje: 6 de 6" in _c[-1][2][1]
    _r.value = [None] * 5 + [next(o["id"] for o in _t[5]["opciones"] if not o["correcta"])]
    _c = corregir_autoevaluacion(_Mock, _t, _r)
    assert [x[1] for x in _c] == ["warn", "neutral"] and "Faltan responder 5" in _c[-1][2][1]
    print("cb104: asserts OK")
