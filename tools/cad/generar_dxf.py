"""Laboratorio CAD: genera los DXF de los ejercicios y sus respuestas esperadas.

Cada ejercicio es un DXF chico (R2000, AC1015) con:
  PARCELA    la parcela como LWPOLYLINE cerrada,
  VERTICES   un POINT por vértice,
  ETIQUETAS  un TEXT por vértice (A, B, C, ...), centrado a distancia fija del vértice,
  EJES       dos LINE desde el origen con sus TEXT «E» y «N»,
más capas propias de cada ejercicio (ACIMUT, ESPEJOS, DESTINO, VENTANA).
Unidades: metros, coordenadas locales chicas (origen cerca de la parcela).

Para cada ejercicio se escribe también la versión transformada esperada en
cad/dxf/esperado/: la geometría transformada con la transformación conocida y las
mismas etiquetas. En las respuestas la parcela se vuelve a dibujar con las
coordenadas transformadas (texto derecho, legible); en cap04_bloque la respuesta es
un INSERT del bloque PARCELA_BLOQUE con la escala pedida, como lo haría el CAD.

Determinismo: ezdxf escribe fechas y GUID en el encabezado; con
ezdxf.options.write_fixed_meta_data_for_testing = True los fija ($TDCREATE,
$TDUPDATE, $VERSIONGUID, $FINGERPRINTGUID), y $HANDSEED sale igual porque las
entidades se crean siempre en el mismo orden. Dos corridas dan archivos idénticos
byte a byte.

Ejecutar desde la raíz del repo:
  uv run python tools/cad/generar_dxf.py
"""
from __future__ import annotations

import math
from pathlib import Path

import ezdxf
import numpy as np
from ezdxf.enums import TextEntityAlignment
from ezdxf.math import Matrix44

ezdxf.options.write_fixed_meta_data_for_testing = True

RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "cad" / "dxf"
ESPERADO = SALIDA / "esperado"
VERSION_DXF = "R2000"

# Parcela de la primera tanda: cuadrilátero irregular A B C E con un vértice de quiebre D
# entre C y E. AB mide 25 m (24, 7), lo que da números lindos en ALIGN.
PARCELA = np.array([[10.0, 10.0], [34.0, 17.0], [40.0, 36.0], [24.0, 38.0], [6.0, 32.0]])
# Triángulo chico cerca del origen para ARRAYPOLAR.
TRIANGULO = np.array([[6.0, 2.0], [9.0, 2.0], [7.0, 4.5]])

CAPAS = {  # nombre: color ACI
    "PARCELA": 7, "VERTICES": 1, "ETIQUETAS": 3, "EJES": 8,
    "ACIMUT": 5, "ESPEJOS": 6, "DESTINO": 4, "VENTANA": 2,
}

# Parámetros de los ejercicios (también los usan las pruebas).
ANG_ROTATE = 30.0                       # ROTATE 30° alrededor de A
ACIMUT_UNITS = 60.0                     # LINE desde A con acimut 60°
ANG_UCS = 30.0                          # UCS rotado 30° alrededor del origen
ANG_ARRAY = 60.0                        # ARRAYPOLAR de 6 copias: paso 60° alrededor del origen
V_MOVE = np.array([12.0, 4.0])          # MOVE
ANG_MOVE_ROTATE = 90.0                  # ROTATE alrededor del origen
X_ESPEJO_1, X_ESPEJO_2 = 50.0, 60.0     # espejos paralelos verticales
I_ESPEJOS = np.array([20.0, -10.0])     # espejos que se cortan: y = -10 y y = x - 30 (45°)
A_RIGIDO = np.array([70.0, 10.0])       # ALIGN rígido: A -> A', B -> B' (giro 90°)
B_RIGIDO = np.array([63.0, 34.0])
A_SIMIL = np.array([90.0, 10.0])        # ALIGN con escala: A -> A'', B -> B'' (giro 90°, x2)
B_SIMIL = np.array([76.0, 58.0])
V_STRETCH = np.array([10.0, 0.0])       # STRETCH de C y D
VENTANA_STRETCH = (18.0, 33.0, 46.0, 41.0)


def rot(grados: float) -> np.ndarray:
    t = math.radians(grados)
    return np.array([[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]])


def reflexion_recta(punto, direccion):
    """(M, t) de la reflexión en la recta que pasa por `punto` con `direccion`."""
    u = np.asarray(direccion, float) / np.linalg.norm(direccion)
    M = 2 * np.outer(u, u) - np.eye(2)
    p = np.asarray(punto, float)
    return M, p - M @ p


def componer(f2, f1):
    """f2 ∘ f1 con f = (M, t)."""
    (M2, t2), (M1, t1) = f2, f1
    return M2 @ M1, M2 @ t1 + t2


def rotacion_alrededor(grados, centro):
    M = rot(grados)
    c = np.asarray(centro, float)
    return M, c - M @ c


def align(a, b, a2, b2, escalar):
    """(M, t) del ALIGN que lleva a -> a2 y la dirección ab a la de a2b2."""
    u, v = b - a, b2 - a2
    ang = math.degrees(math.atan2(v[1], v[0]) - math.atan2(u[1], u[0]))
    k = np.linalg.norm(v) / np.linalg.norm(u) if escalar else 1.0
    M = k * rot(ang)
    return M, a2 - M @ a


def matriz44(M, t) -> Matrix44:
    """Matrix44 de ezdxf (vectores fila) para p' = M p + t en el plano."""
    M, t = np.asarray(M, float), np.asarray(t, float)
    filas = [[M[0, 0], M[1, 0], 0, 0], [M[0, 1], M[1, 1], 0, 0], [0, 0, 1, 0], [t[0], t[1], 0, 1]]
    return Matrix44([float(x) for fila in filas for x in fila])


def aplicar(f, P):
    M, t = f
    return np.asarray(P, float) @ np.asarray(M).T + t


def etiquetas(n: int):
    return [chr(ord("A") + i) for i in range(n)]


# ---------------------------------------------------------------- dibujo
def nuevo_doc():
    doc = ezdxf.new(VERSION_DXF, setup=False)
    doc.header["$INSUNITS"] = 6      # metros
    doc.header["$MEASUREMENT"] = 1   # métrico
    doc.header["$LUNITS"] = 2        # decimal
    doc.header["$LUPREC"] = 3
    for nombre, color in CAPAS.items():
        doc.layers.add(nombre, color=color)
    return doc


def _texto(contenedor, s, pos, alto, capa):
    contenedor.add_text(s, height=alto, dxfattribs={"layer": capa}).set_placement(
        (float(pos[0]), float(pos[1])), align=TextEntityAlignment.MIDDLE_CENTER)


def dibujar_poligono(contenedor, P, nombres=None, alto=1.2, sep=1.5):
    """LWPOLYLINE cerrada en PARCELA, POINT en VERTICES y TEXT en ETIQUETAS.

    Cada etiqueta queda centrada a `sep` metros del vértice, hacia afuera del
    centroide del polígono.
    """
    P = np.asarray(P, float)
    nombres = nombres or etiquetas(len(P))
    contenedor.add_lwpolyline([tuple(map(float, p)) for p in P], close=True,
                              dxfattribs={"layer": "PARCELA"})
    g = P.mean(axis=0)
    for p, s in zip(P, nombres):
        contenedor.add_point(tuple(map(float, p)), dxfattribs={"layer": "VERTICES"})
        d = p - g
        _texto(contenedor, s, p + sep * d / np.linalg.norm(d), alto, "ETIQUETAS")


def dibujar_ejes(msp, largo=10.0, alto=1.2):
    msp.add_line((0, 0), (largo, 0), dxfattribs={"layer": "EJES"})
    msp.add_line((0, 0), (0, largo), dxfattribs={"layer": "EJES"})
    _texto(msp, "E", (largo + alto, 0), alto, "EJES")
    _texto(msp, "N", (0, largo + alto), alto, "EJES")


def linea(msp, p, q, capa):
    msp.add_line(tuple(map(float, p)), tuple(map(float, q)), dxfattribs={"layer": capa})


def punto_destino(msp, p, s, alto=1.2):
    msp.add_point(tuple(map(float, p)), dxfattribs={"layer": "DESTINO"})
    _texto(msp, s, np.asarray(p) + np.array([1.5, 1.5]), alto, "DESTINO")


# ---------------------------------------------------------------- ejercicios
def _extra_units(msp, f=None):
    a = PARCELA[0]
    az = math.radians(ACIMUT_UNITS)
    fin = a + 20.0 * np.array([math.sin(az), math.cos(az)])
    p, q = (a, fin) if f is None else np.round(aplicar(f, [a, fin]), 9) + 0.0
    linea(msp, p, q, "ACIMUT")


def _extra_mirror(msp):
    linea(msp, (X_ESPEJO_1, 0), (X_ESPEJO_1, 45), "ESPEJOS")
    linea(msp, (X_ESPEJO_2, 0), (X_ESPEJO_2, 45), "ESPEJOS")
    linea(msp, (-20, -10), (60, -10), "ESPEJOS")
    linea(msp, (0, -30), (50, 20), "ESPEJOS")


def _extra_align(msp):
    punto_destino(msp, A_RIGIDO, "A'")
    punto_destino(msp, B_RIGIDO, "B'")
    punto_destino(msp, A_SIMIL, "A''")
    punto_destino(msp, B_SIMIL, "B''")


def _extra_stretch(msp):
    x0, y0, x1, y1 = VENTANA_STRETCH
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], close=True,
                       dxfattribs={"layer": "VENTANA"})


def _bloque(doc):
    blk = doc.blocks.new("PARCELA_BLOQUE", base_point=(0, 0))
    dibujar_poligono(blk, PARCELA)
    return blk


# Cada ejercicio: polígono, parámetros de dibujo, extras y lista de respuestas
# (nombre, transformación (M, t) aplicada al polígono, función de extras para la respuesta).
F_ROTATE = rotacion_alrededor(ANG_ROTATE, PARCELA[0])
F_UCS_ACTIVA = rotacion_alrededor(ANG_UCS, (0, 0))
F_UCS_PASIVA = rotacion_alrededor(-ANG_UCS, (0, 0))
F_BISECTRIZ = reflexion_recta((0, 0), (1, 1))
F_ARRAY = rotacion_alrededor(ANG_ARRAY, (0, 0))
F_MOVE = (np.eye(2), V_MOVE)
F_ROT_O = rotacion_alrededor(ANG_MOVE_ROTATE, (0, 0))
F_MOVE_ROTATE = componer(F_ROT_O, F_MOVE)
F_ROTATE_MOVE = componer(F_MOVE, F_ROT_O)
F_ESPEJO_1 = reflexion_recta((X_ESPEJO_1, 0), (0, 1))
F_ESPEJO_2 = reflexion_recta((X_ESPEJO_2, 0), (0, 1))
F_PARALELOS = componer(F_ESPEJO_2, F_ESPEJO_1)
F_CORTAN = componer(reflexion_recta(I_ESPEJOS, (1, 1)), reflexion_recta(I_ESPEJOS, (1, 0)))
F_ALIGN_RIGIDO = align(PARCELA[0], PARCELA[1], A_RIGIDO, B_RIGIDO, escalar=False)
F_ALIGN_SIMIL = align(PARCELA[0], PARCELA[1], A_SIMIL, B_SIMIL, escalar=True)
F_BLOQUE_X2 = (np.diag([2.0, 1.0]), np.zeros(2))
F_BLOQUE_XM1 = (np.diag([-1.0, 1.0]), np.zeros(2))

EJERCICIOS = {
    "cap01_rotate": dict(respuestas=[("cap01_rotate_30", F_ROTATE)]),
    "cap01_ucs": dict(respuestas=[("cap01_ucs_activa_30", F_UCS_ACTIVA),
                                  ("cap01_ucs_pasiva_30", F_UCS_PASIVA)]),
    "cap01_units": dict(extra=_extra_units,
                        respuestas=[("cap01_units_bisectriz", F_BISECTRIZ)]),
    "cap01_arraypolar": dict(poligono=TRIANGULO, alto=0.5, sep=0.6, ejes=4.0,
                             respuestas=[("cap01_arraypolar_60", F_ARRAY)]),
    "cap02_move_rotate": dict(respuestas=[("cap02_move_rotate", F_MOVE_ROTATE),
                                          ("cap02_rotate_move", F_ROTATE_MOVE)]),
    "cap03_mirror": dict(extra=_extra_mirror,
                         respuestas=[("cap03_mirror_x50", F_ESPEJO_1),
                                     ("cap03_mirror_paralelos", F_PARALELOS),
                                     ("cap03_mirror_cortan", F_CORTAN)]),
    "cap03_align": dict(extra=_extra_align,
                        respuestas=[("cap03_align_rigido", F_ALIGN_RIGIDO),
                                    ("cap03_align_similaridad", F_ALIGN_SIMIL)]),
    "cap04_bloque": dict(bloque=True,
                         respuestas=[("cap04_bloque_x2_y1", F_BLOQUE_X2),
                                     ("cap04_bloque_xm1", F_BLOQUE_XM1)]),
    "cap04_stretch": dict(extra=_extra_stretch, respuestas=[("cap04_stretch_10", None)]),
}


def construir(nombre: str):
    """Documento ezdxf del ejercicio original."""
    e = EJERCICIOS[nombre]
    doc = nuevo_doc()
    if e.get("bloque"):
        _bloque(doc)
    msp = doc.modelspace()
    dibujar_ejes(msp, e.get("ejes", 10.0), e.get("alto", 1.2))
    dibujar_poligono(msp, e.get("poligono", PARCELA), alto=e.get("alto", 1.2),
                     sep=e.get("sep", 1.5))
    if "extra" in e:
        e["extra"](msp)
    return doc


def construir_respuesta(nombre: str, respuesta: str):
    """Documento ezdxf de la respuesta esperada `respuesta` del ejercicio `nombre`."""
    e = EJERCICIOS[nombre]
    f = dict(e["respuestas"])[respuesta]
    P = np.asarray(e.get("poligono", PARCELA), float)
    doc = nuevo_doc()
    msp = doc.modelspace()
    dibujar_ejes(msp, e.get("ejes", 10.0), e.get("alto", 1.2))
    if e.get("bloque"):
        _bloque(doc)
        M, _ = f
        msp.add_blockref("PARCELA_BLOQUE", (0, 0),
                         dxfattribs={"xscale": float(M[0, 0]), "yscale": float(M[1, 1])})
        return doc
    if f is None:  # STRETCH: C y D se corren, A, B y E quedan
        Q = P.copy()
        Q[2:4] += V_STRETCH
    else:
        Q = np.round(aplicar(f, P), 9) + 0.0  # sin ruido de punto flotante ni -0
    dibujar_poligono(msp, Q, alto=e.get("alto", 1.2), sep=e.get("sep", 1.5))
    if nombre == "cap01_units":
        _extra_units(msp, f)
    elif "extra" in e:
        e["extra"](msp)  # espejos, destinos y ventana quedan donde estaban
    return doc


def guardar(doc, ruta: Path):
    ruta.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(ruta)


def main():
    generados = []
    for nombre, e in EJERCICIOS.items():
        ruta = SALIDA / f"{nombre}.dxf"
        guardar(construir(nombre), ruta)
        generados.append(ruta)
        for respuesta, _ in e["respuestas"]:
            ruta = ESPERADO / f"{respuesta}.dxf"
            guardar(construir_respuesta(nombre, respuesta), ruta)
            generados.append(ruta)
    for r in generados:
        print(r.relative_to(RAIZ))


if __name__ == "__main__":
    main()
