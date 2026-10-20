"""Laboratorio CAD: ¿qué matriz aplicó el CAD?

Uso (desde la raíz del repo):
  uv run python tools/cad/que_matriz.py ORIGINAL.dxf TRANSFORMADO.dxf [--json] [--tol 0.005]

Lee los dos DXF, empareja los vértices por etiqueta y estima por mínimos cuadrados la
transformación afín p' = M p + t (y la homografía, normalizada con h33 = 1, si hay
cuatro o más vértices). Informa M, t, det M, el área encerrada por los vértices
emparejados en cada archivo y su cociente (que, para una afín, es |det M|), el residuo
RMS en metros, la familia mínima que la explica y su lectura geométrica (ángulo,
centro, factor, eje).

Área: fórmula del agrimensor (la mitad de la suma de los cuñas p_i ∧ p_{i+1}) sobre los
vértices emparejados recorridos en el orden alfabético de sus letras (A, B, C, ...), que
en los DXF del laboratorio es el orden del contorno. Se informa en valor absoluto; el
cociente es área transformada / área original.

Emparejamiento de etiquetas, en cada archivo:
  * vértices: los POINT de la capa VERTICES y los vértices de la polilínea de la capa
    PARCELA (LWPOLYLINE o POLYLINE de R12; si no hay capa PARCELA, la polilínea
    cerrada con más vértices). Se usan las dos fuentes y gana la que queda más cerca
    de las etiquetas; si no coinciden entre sí, se avisa (por ejemplo, si se movió
    la polilínea y no los puntos).
  * etiquetas: TEXT o MTEXT de la capa ETIQUETAS con una letra mayúscula (A, B, ...,
    se admite A', A''). Si no hay capa ETIQUETAS, cualquier TEXT/MTEXT de una sola
    letra fuera de la capa EJES (las «E» y «N» de los ejes no cuentan).
  * cada etiqueta va al vértice más cercano, con asignación óptima uno a uno
    (algoritmo húngaro sobre las distancias).
  * los INSERT se descomponen; si el archivo tiene un INSERT con vértices
    etiquetados, se usan sólo esos (es la copia insertada).
Entre los dos archivos se emparejan las etiquetas comunes; hacen falta tres no
alineadas.

Familia mínima: mismo criterio que apunte/scripts/cap04_mapa_transformaciones.py
(clasificar_global): se mira si se conservan las distancias (sí / por un factor k /
no) y el sentido de giro (signo del determinante). Ese script no se importa porque al
importarlo corre todo el capítulo y escribe figuras; acá el criterio se evalúa
directamente sobre M: distancias «sí» si los dos valores singulares valen 1,
«por k» si son iguales entre sí. Con eso:
  identidad, traslación (M = I), rotación (distancias sí, det > 0; todo movimiento
  rígido directo que no es traslación es una rotación alrededor de un centro),
  reflexión (distancias sí, det < 0, sin deslizamiento), movimiento rígido
  (distancias sí, det < 0, con deslizamiento: isometría inversa), similaridad
  (distancias por k), afinidad (el resto), no afín (residuo RMS mayor que --tol).

Exit 0 si pudo estimar; exit 2 si faltan etiquetas o no hay emparejamiento posible.
"""
from __future__ import annotations

import argparse
import json
import math
import re
import sys
from pathlib import Path

import ezdxf
import numpy as np
from ezdxf import recover
from scipy.optimize import linear_sum_assignment

TOL_RESIDUO = 0.005   # m: por encima, «no afín» (se cambia con --tol)
TOL_MATRIZ = 1e-4     # adimensional: para decidir M = I, valores singulares iguales, etc.
TOL_AREA_REL = 2e-2   # 2 % de tolerancia relativa entre cociente de áreas y |det M|
PATRON_ETIQUETA = re.compile(r"^[A-Z]'{0,2}$")
PATRON_LETRA = re.compile(r"^[A-Z]$")


# ==============================================================================
# GUÍA DIDÁCTICA DE PYTHON, NUMPY, SCIPY Y EZDXF
# ==============================================================================
# Este programa es también material de estudio para aprender Python aplicado a
# Geometría y Agrimensura. Algunas claves de lectura si venís de Julia o MATLAB:
#
# 1. Indexación en base 0 y rangos semiabiertos:
#    - En Python el primer elemento es `v[0]` (no `v[1]`) y el último es `v[-1]`.
#    - Un recorte (*slice*) `X[:2]` toma los índices 0 y 1 (el límite superior 2
#      queda excluido). `P[:-1]` toma todos los elementos salvo el último.
#
# 2. Arreglos de NumPy y producto matricial:
#    - `np.array(...)` crea arreglos n-dimensionales.
#    - El operador `@` calcula el producto matricial o producto interno
#      (`M @ p` o `p @ M.T`), mientras que `*` multiplica elemento a elemento
#      (como `.*` en MATLAB/Julia).
#    - `np.c_[p, np.ones(len(p))]` apila columnas (equivale a `[p ones(n,1)]`),
#      ideal para pasar de coordenadas cartesianas (x, y) a homogéneas (x, y, 1).
#
# 3. Broadcasting (difusión de dimensiones):
#    - En `L[:, None, :] - V[None, :, :]`, insertar `None` (o `np.newaxis`)
#      expande `(N, 2)` y `(M, 2)` a `(N, 1, 2)` y `(1, M, 2)` para calcular
#      todas las diferencias de pares `(i, j)` en un tensor `(N, M, 2)` sin
#      escribir bucles `for` anidados.
#
# 4. Álgebra lineal numérica (`np.linalg` y `scipy.optimize`):
#    - `np.linalg.lstsq(U, q, rcond=None)` resuelve sistemas sobredeterminados
#      en mínimos cuadrados (la pseudoinversa del capítulo 11).
#    - `np.linalg.svd(M)` calcula la descomposición en valores singulares
#      (capítulo 8), que acá usamos tanto para clasificar la matriz M según
#      sus estiramientos principales (σ₁, σ₂) como para estimar homografías.
#    - `linear_sum_assignment(D)` resuelve el problema de asignación óptima
#      (algoritmo húngaro) sobre la matriz de distancias D entre etiquetas y
#      vértices.
#
# 5. Geometría computacional con `np.roll`:
#    - En la fórmula del agrimensor (área por coordenadas), `np.roll(y, -1)`
#      desplaza el vector cíclicamente para aparear (x_i, y_{i+1}) en una sola
#      operación vectorial vectorizada, sin índices explícitos.
#
# 6. Tolerancia a fallos y lectura de CAD con `ezdxf`:
#    - `ezdxf.recover.readfile` permite rescatar archivos DXF que tienen
#      inconsistencias menores en su tabla de cabeceras, garantizando que el
#      laboratorio funcione con planos exportados desde distintos motores CAD.
#
# 7. Formato pedagógico y localización:
#    - La función `num(x)` garantiza la salida con coma decimal estándar en
#      castellano (`12,345` en lugar de `12.345`), manteniendo coherencia con
#      la notación del apunte teórico de la materia.
# ==============================================================================


class ErrorEmparejamiento(Exception):
    """Faltan etiquetas o no se pueden emparejar los vértices."""


# ---------------------------------------------------------------- lectura
def leer_doc(ruta):
    """Abre un archivo DXF con ezdxf; si tiene pequeños errores de formato, usa recover."""
    try:
        return ezdxf.readfile(ruta)
    except ezdxf.DXFStructureError:
        doc, _ = recover.readfile(ruta)
        return doc
    except OSError as e:
        raise ErrorEmparejamiento(f"no se puede leer {ruta}: {e}") from e


def _entidades(msp):
    """(entidad, viene_de_insert) del espacio modelo, con los INSERT descompuestos.

    En Python, `yield` y `yield from` definen un *generador*: produce los elementos
    uno por uno a medida que se los recorre, sin armar listas intermedias en memoria.
    """
    def recorrer(ents, de_insert, nivel):
        for e in ents:
            if e.dxftype() == "INSERT":
                if nivel < 8:
                    yield from recorrer(e.virtual_entities(), True, nivel + 1)
            else:
                yield e, de_insert
    yield from recorrer(msp, False, 0)


def _xy(v):
    """Extrae las dos primeras coordenadas (x, y) como vector de punto flotante de NumPy."""
    return np.array([float(v[0]), float(v[1])])


def _capa(e):
    return e.dxf.get("layer", "0").upper()


def _texto(e):
    """(cadena, punto de referencia WCS) de un TEXT o MTEXT."""
    if e.dxftype() == "MTEXT":
        return e.plain_text().strip(), _xy(e.dxf.insert)
    alineado = e.dxf.get("halign", 0) or e.dxf.get("valign", 0)
    p = e.dxf.align_point if alineado and e.dxf.hasattr("align_point") else e.dxf.insert
    return e.dxf.text.strip(), _xy(e.ocs().to_wcs(p))


def _polilinea(e):
    """Devuelve los vértices (N, 2) y si la polilínea es cerrada (LWPOLYLINE o POLYLINE R12)."""
    if e.dxftype() == "LWPOLYLINE":
        P = [_xy(v) for v in e.vertices_in_wcs()]
        cerrada = e.closed
    else:  # POLYLINE 2D (R12)
        if not e.is_2d_polyline:
            P = [_xy(v.dxf.location) for v in e.vertices]
        else:
            ocs = e.ocs()
            P = [_xy(ocs.to_wcs(v.dxf.location)) for v in e.vertices]
        cerrada = e.is_closed
    # reshape(-1, 2) asegura que la matriz tenga 2 columnas aunque venga vacía;
    # si el primer y último vértice coinciden, descartamos el duplicado con P[:-1].
    P = np.array(P, float).reshape(-1, 2)
    if len(P) > 1 and np.allclose(P[0], P[-1]):
        P, cerrada = P[:-1], True
    return P, cerrada


def extraer(ruta):
    """Vértices etiquetados de un DXF: dict con etiquetas, fuente y avisos."""
    doc = leer_doc(ruta)
    ents = list(_entidades(doc.modelspace()))
    grupos = [[(e, c) for e, c in ents if c], [(e, c) for e, c in ents if not c]]
    ultimo_error = None
    for grupo in grupos:
        if not grupo:
            continue
        try:
            return _extraer_de(grupo, ruta, de_insert=grupo[0][1])
        except ErrorEmparejamiento as err:
            ultimo_error = err
    raise ultimo_error or ErrorEmparejamiento(f"{ruta}: el espacio modelo está vacío")


def _extraer_de(grupo, ruta, de_insert):
    puntos, polis, textos_capa, textos_otros = [], [], [], []
    for e, _ in grupo:
        t, capa = e.dxftype(), _capa(e)
        if t == "POINT" and capa == "VERTICES":
            puntos.append(_xy(e.dxf.location))
        elif t in ("LWPOLYLINE", "POLYLINE"):
            P, cerrada = _polilinea(e)
            polis.append((capa == "PARCELA", cerrada, P))
        elif t in ("TEXT", "MTEXT"):
            s, p = _texto(e)
            if capa == "ETIQUETAS" and PATRON_ETIQUETA.match(s):
                textos_capa.append((s, p))
            elif capa != "EJES" and PATRON_LETRA.match(s):
                textos_otros.append((s, p))
    avisos = []
    textos = textos_capa or textos_otros
    if not textos:
        raise ErrorEmparejamiento(f"{ruta}: no hay etiquetas (TEXT de una letra) para los vértices")
    if not textos_capa:
        avisos.append("no hay capa ETIQUETAS: se usaron los TEXT de una letra de cualquier capa")
    nombres = [s for s, _ in textos]
    repetidas = sorted({s for s in nombres if nombres.count(s) > 1})
    if repetidas:
        raise ErrorEmparejamiento(f"{ruta}: etiquetas repetidas: {', '.join(repetidas)}")
    L = np.array([p for _, p in textos])

    fuentes = {}
    if puntos:
        fuentes["puntos (VERTICES)"] = np.array(puntos)
    if polis:
        polis.sort(key=lambda x: (x[0], x[1], len(x[2])), reverse=True)
        en_parcela, _, P = polis[0]
        fuentes["polilínea (PARCELA)" if en_parcela else "polilínea (otra capa)"] = P
    if not fuentes:
        raise ErrorEmparejamiento(f"{ruta}: no hay POINT en VERTICES ni polilínea de la parcela")

    mejor = None
    for nombre, V in fuentes.items():
        if len(V) < len(L):
            continue
        D = np.linalg.norm(L[:, None, :] - V[None, :, :], axis=2)
        fil, col = linear_sum_assignment(D)
        costo = D[fil, col].mean()
        if mejor is None or costo < mejor[0]:
            mejor = (costo, nombre, V, fil, col, D)
    if mejor is None:
        raise ErrorEmparejamiento(f"{ruta}: hay más etiquetas ({len(L)}) que vértices")
    _, fuente, V, fil, col, D = mejor

    if len(fuentes) == 2:
        A, B = fuentes.values()
        dAB = np.linalg.norm(A[:, None] - B[None], axis=2)
        if dAB.min(axis=1).max() > 1e-3 or dAB.min(axis=0).max() > 1e-3:
            avisos.append("los POINT de VERTICES y la polilínea de PARCELA no coinciden "
                          "(¿se movió sólo una parte?); se usó " + fuente +
                          ", que queda más cerca de las etiquetas")
    lado = np.linalg.norm(V[:, None] - V[None], axis=2)
    lados_pos = lado[lado > 0]
    lado = lados_pos.min() if len(lados_pos) > 0 else 1.0
    lejos = [nombres[i] for i, j in zip(fil, col) if D[i, j] > 0.4 * lado]
    if lejos:
        avisos.append("etiquetas lejos de su vértice (¿se movieron sin los vértices?): "
                      + ", ".join(sorted(lejos)))
    vert = {nombres[i]: V[j] for i, j in zip(fil, col)}
    if de_insert:
        avisos.append("se usaron los vértices del INSERT (bloque insertado)")
    return dict(vertices=vert, fuente=fuente, avisos=avisos)


# ---------------------------------------------------------------- ajuste
def ajuste_afin(p, q):
    """Estima la transformación afín q ≈ p @ M.T + t por mínimos cuadrados (capítulo 11 y 12).

    Armamos la matriz de diseño U = [p | 1] de tamaño (N, 3) agregando una columna de unos
    con `np.c_`. Al resolver U @ X ≈ q con `np.linalg.lstsq`, las dos primeras filas de X
    son M.T y la tercera fila (índice 2 en base 0) es el vector de traslación t.
    """
    U = np.c_[p, np.ones(len(p))]
    X = np.linalg.lstsq(U, q, rcond=None)[0]
    return X[:2].T, X[2]


def ajuste_homografia(p, q):
    """DLT normalizado (Hartley) con h33 = 1 (complemento C1 de transformaciones proyectivas).

    Cada par de puntos homólogos (x, y) -> (u, v) aporta dos ecuaciones lineales homogéneas
    en las 9 entradas de H. La solución de norma unitaria que minimiza el residuo algebraico
    es la última fila de V^T en la SVD (`np.linalg.svd(...)[2][-1]`), que corresponde al
    menor valor singular.
    """
    def normalizar(X):
        c = X.mean(axis=0)
        s = math.sqrt(2) / max(np.mean(np.linalg.norm(X - c, axis=1)), 1e-12)
        return np.array([[s, 0, -s * c[0]], [0, s, -s * c[1]], [0, 0, 1]])
    Tp, Tq = normalizar(p), normalizar(q)
    ph = (np.c_[p, np.ones(len(p))]) @ Tp.T
    qh = (np.c_[q, np.ones(len(q))]) @ Tq.T
    filas = []
    for (x, y, _), (u, v, _) in zip(ph, qh):
        filas.append([x, y, 1, 0, 0, 0, -u * x, -u * y, -u])
        filas.append([0, 0, 0, x, y, 1, -v * x, -v * y, -v])
    Hn = np.linalg.svd(np.array(filas))[2][-1].reshape(3, 3)
    H = np.linalg.inv(Tq) @ Hn @ Tp
    if abs(H[2, 2]) < 1e-12:
        return None
    return H / H[2, 2]


def aplicar_h(H, p):
    """Aplica la matriz de homografía 3×3 en coordenadas homogéneas y deshomogeneiza dividiendo por w.

    Si algún denominador w_i está muy próximo a 0 (puntos que caen sobre la recta límite
    o el infinito proyectivo), se reemplaza por NaN para evitar divisiones por cero no controladas.
    """
    X = np.c_[p, np.ones(len(p))] @ H.T
    w = X[:, 2:]
    w_seguro = np.where(np.abs(w) < 1e-12, np.nan, w)
    return X[:, :2] / w_seguro


def area_poligono(P):
    """Área con signo por la fórmula del agrimensor: (1/2) suma de p_i ∧ p_{i+1}.

    `np.roll(y, -1)` desplaza el vector una posición hacia la izquierda (de modo que el
    elemento i queda enfrentado con el i+1, y el último con el primero), evitando escribir
    un bucle `for` con índices módulo N.
    """
    P = np.asarray(P, float)
    x, y = P[:, 0], P[:, 1]
    return float(0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y))


def rms(r):
    """Raíz del promedio de los cuadrados de las normas de los vectores fila de `r`.

    Si algún residuo contiene valores indefinidos (NaN o infinito), se devuelve inf.
    """
    if np.any(np.isnan(r)):
        return float("inf")
    return float(np.sqrt(np.mean(np.sum(r ** 2, axis=1))))


def clasificar(M, t, residuo, tol, tol_m=TOL_MATRIZ):
    """Familia mínima y lectura geométrica (criterio de cap04_mapa_transformaciones.py).

    Usa los valores singulares (s1, s2) y el signo del determinante de M:
      - s1 ≈ 1 y s2 ≈ 1: isometría (rotación si det > 0; reflexión o reflexión deslizada si det < 0).
      - s1 ≈ s2 ≠ 1 (con s2 > 0): similaridad de factor k = √|det M| (directa si det > 0: rotación + escala;
        inversa si det < 0: roto-reflexión / reflexión + escala).
      - s1 ≠ s2 o matriz degenerada: afinidad general.
    """
    escala = max(1.0, float(np.abs(t).max()))
    det = float(np.linalg.det(M))
    s1, s2 = np.linalg.svd(M, compute_uv=False)
    lectura = {}
    if residuo > tol:
        return "no_afin", lectura
    if np.allclose(M, np.eye(2), atol=tol_m):
        if np.abs(t).max() < tol:
            return "identidad", lectura
        lectura["desplazamiento"] = [float(t[0]), float(t[1])]
        return "traslacion", lectura
    # Para similaridad ('xk') requerimos que s2 > 1e-8 (matriz no singular), evitando
    # divisiones por cero si la transformación colapsa la figura a un punto o recta.
    distancias = ("si" if abs(s1 - 1) < tol_m and abs(s2 - 1) < tol_m
                  else "xk" if s2 > 1e-8 and abs(s1 - s2) < tol_m * max(1.0, s1) else "no")
    directo = det > 0
    if distancias == "no":
        lectura["escalas_principales"] = [float(s1), float(s2)]
        lectura["factor_area"] = abs(det)
        lectura["sentido"] = "se conserva" if directo else "se invierte"
        return "afinidad", lectura
    k = float(math.sqrt(abs(det)))
    if directo:
        ang = math.degrees(math.atan2(M[1, 0], M[0, 0]))
        lectura["angulo"] = ang
        if distancias == "xk":
            lectura["factor"] = k
            lectura["sentido"] = "se conserva"
        c = np.linalg.solve(np.eye(2) - M, t)
        lectura["centro"] = [float(c[0]), float(c[1])]
        return ("rotacion" if distancias == "si" else "similaridad"), lectura
    # inversa (det < 0): M = k * reflexión en una recta de dirección u (autovector de autovalor +k)
    w, V = np.linalg.eig(M / k)
    u = np.real(V[:, np.argmin(np.abs(w - 1))])
    u = u / np.linalg.norm(u)
    if u[0] < -1e-12 or (abs(u[0]) <= 1e-12 and u[1] < 0):
        u = -u
    ang_eje = math.degrees(math.atan2(u[1], u[0]))
    lectura["direccion_eje"] = ang_eje
    if distancias == "xk":
        lectura["factor"] = k
        lectura["sentido"] = "se invierte"
        c = np.linalg.solve(np.eye(2) - M, t)
        lectura["centro"] = [float(c[0]), float(c[1])]
        lectura["eje_por"] = lectura["centro"]
        return "similaridad", lectura
    desliz = float(t @ u)
    n = t - desliz * u
    lectura["eje_por"] = [float(n[0] / 2), float(n[1] / 2)]
    if abs(desliz) < tol:
        return "reflexion", lectura
    lectura["deslizamiento"] = desliz
    return "rigido", lectura


ROTULO = {"identidad": "identidad", "traslacion": "traslación", "rotacion": "rotación",
          "reflexion": "reflexión", "rigido": "movimiento rígido (isometría inversa: "
          "reflexión con deslizamiento)", "similaridad": "similaridad",
          "afinidad": "afinidad", "no_afin": "no afín (ninguna afín explica los puntos)"}


def analizar(original, transformado, tol=TOL_RESIDUO):
    """Resultado como dict (lo que imprime --json). Lanza ErrorEmparejamiento."""
    a, b = extraer(original), extraer(transformado)
    comunes = sorted(set(a["vertices"]) & set(b["vertices"]))
    if len(comunes) < 3:
        raise ErrorEmparejamiento(
            f"hacen falta al menos 3 etiquetas comunes; hay {len(comunes)} "
            f"({', '.join(comunes) or 'ninguna'})")
    p = np.array([a["vertices"][s] for s in comunes])
    q = np.array([b["vertices"][s] for s in comunes])
    pc = p - p.mean(axis=0)
    sv = np.linalg.svd(pc, compute_uv=False)
    if sv[1] < 1e-9 * max(sv[0], 1.0):
        raise ErrorEmparejamiento("los vértices emparejados están alineados: no determinan M")
    M, t = ajuste_afin(p, q)
    res = q - (p @ M.T + t)
    r = rms(res)
    familia, lectura = clasificar(M, t, r, tol)
    if "centro" in lectura:
        c = np.array(lectura["centro"])
        cerca = [s for s in comunes if np.linalg.norm(a["vertices"][s] - c) < tol]
        if cerca:
            lectura["centro_es_vertice"] = cerca[0]
    det = float(np.linalg.det(M))
    familia_texto = (
        "similaridad inversa (reflexión + escala)"
        if familia == "similaridad" and det < 0
        else ROTULO[familia]
    )
    salida = dict(
        original=str(original), transformado=str(transformado),
        etiquetas=comunes, fuente_original=a["fuente"], fuente_transformado=b["fuente"],
        avisos=[f"original: {x}" for x in a["avisos"]]
        + [f"transformado: {x}" for x in b["avisos"]],
        M=M.tolist(), t=t.tolist(), det=det, rms=r, tol=tol,
        area_original=abs(area_poligono(p)), area_transformado=abs(area_poligono(q)),
        residuos={s: float(np.linalg.norm(v)) for s, v in zip(comunes, res)},
        familia=familia, familia_texto=familia_texto, lectura=lectura,
    )
    salida["cociente_areas"] = (salida["area_transformado"] / salida["area_original"]
                                if salida["area_original"] > 0 else None)
    # Verificación de área con tolerancia relativa de 2e-2 (2 %) para no dar falsos positivos
    # cuando el plano fue editado manualmente en CAD con pequeños redondeos.
    if (familia != "no_afin" and salida["cociente_areas"] is not None
            and abs(salida["cociente_areas"] - abs(det)) > TOL_AREA_REL * max(1.0, abs(det))):
        salida["avisos"].append(
            "el cociente de áreas difiere de |det M| en más del 2 % "
            "(¿polilínea editada a mano o vértices desordenados?)"
        )
    if len(comunes) >= 4:
        H = ajuste_homografia(p, q)
        if H is not None:
            salida["homografia"] = dict(H=H.tolist(), rms=rms(q - aplicar_h(H, p)))
    return salida


# ---------------------------------------------------------------- salida
def num(x, dec=3):
    s = f"{x:.{dec}f}"
    if float(s) == 0:
        s = f"{0:.{dec}f}"
    return s.replace(".", ",")


def punto(v):
    return f"({num(v[0])}; {num(v[1])})"


def matriz(A, sangria):
    filas = [[num(x) for x in fila] for fila in A]
    ancho = max(len(x) for fila in filas for x in fila)
    return "\n".join(sangria + "[ " + "  ".join(x.rjust(ancho) for x in fila) + " ]"
                     for fila in filas)


def texto(r):
    lin = [f"Original:     {r['original']}  [{r['fuente_original']}]",
           f"Transformado: {r['transformado']}  [{r['fuente_transformado']}]",
           f"Vértices emparejados por etiqueta: {', '.join(r['etiquetas'])}"]
    lin += [f"Aviso: {x}" for x in r["avisos"]]
    lin += ["", "Transformación afín  p' = M p + t", "  M ="]
    lin.append(matriz(r["M"], "    "))
    if r["cociente_areas"] is None:
        area = "el área original es nula (vértices alineados o mal ordenados)"
    else:
        area = (f"{num(r['area_original'])} m² → {num(r['area_transformado'])} m² "
                f"(cociente = {num(r['cociente_areas'])}; |det M| = {num(abs(r['det']))})")
    lin += [f"  t = {punto(r['t'])} m", f"  det M = {num(r['det'])}",
            f"  Área ({', '.join(r['etiquetas'])}, en ese orden): {area}",
            f"  Residuo RMS = {num(r['rms'])} m (tolerancia {num(r['tol'])} m)",
            "", f"Familia mínima: {r['familia_texto']}"]
    le = r["lectura"]
    if "desplazamiento" in le:
        lin.append(f"  Desplazamiento: {punto(le['desplazamiento'])} m")
    if "angulo" in le:
        lin.append(f"  Ángulo de rotación: {num(le['angulo'])}° (antihorario)")
    if "factor" in le:
        lin.append(f"  Factor de escala: {num(le['factor'])} (áreas por {num(le['factor'] ** 2)})")
    if "centro" in le:
        extra = f" = vértice {le['centro_es_vertice']}" if "centro_es_vertice" in le else ""
        lin.append(f"  Centro (punto fijo): {punto(le['centro'])}{extra}")
    if "direccion_eje" in le:
        lin.append(f"  Eje de reflexión: pasa por {punto(le['eje_por'])}, dirección "
                   f"{num(le['direccion_eje'])}° desde el eje E (antihorario)")
    if "deslizamiento" in le:
        lin.append(f"  Deslizamiento a lo largo del eje: {num(le['deslizamiento'])} m")
    if "escalas_principales" in le:
        s1, s2 = le["escalas_principales"]
        lin.append(f"  Escalas principales (valores singulares): {num(s1)} y {num(s2)}")
        lin.append(f"  Factor de áreas |det M|: {num(le['factor_area'])}; "
                   f"el sentido de giro {le['sentido']}")
    if r["familia"] == "no_afin":
        peor = max(r["residuos"], key=r["residuos"].get)
        lin.append(f"  Mayor residuo: vértice {peor}, {num(r['residuos'][peor])} m")
    if "homografia" in r:
        h = r["homografia"]
        lin += ["", "Homografía (h33 = 1)", matriz(h["H"], "    "),
                f"  Residuo RMS = {num(h['rms'])} m"]
        if r["familia"] == "no_afin" and h["rms"] <= r["tol"]:
            lin.append("  La homografía sí explica los puntos: es una transformación proyectiva.")
    return "\n".join(lin)


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="Estima la matriz que lleva un DXF original a su versión transformada.")
    ap.add_argument("original", type=Path)
    ap.add_argument("transformado", type=Path)
    ap.add_argument("--json", action="store_true", help="salida en JSON (para las pruebas)")
    ap.add_argument("--tol", type=float, default=TOL_RESIDUO,
                    help=f"residuo RMS máximo en metros para aceptar una afín "
                         f"(por defecto {TOL_RESIDUO})")
    args = ap.parse_args(argv)
    try:
        r = analizar(args.original, args.transformado, args.tol)
    except ErrorEmparejamiento as e:
        print(f"Error: {e}", file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if args.json else texto(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
