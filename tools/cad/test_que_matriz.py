"""Pruebas del laboratorio CAD: se transforma un DXF con ezdxf y que_matriz.py tiene que
recuperar la matriz, el determinante, la familia y un residuo nulo.

Correr con: uv run pytest tools/cad -q
"""
import json
import math
import subprocess
import sys
from pathlib import Path

import ezdxf
import numpy as np
import pytest

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import generar_dxf as g  # noqa: E402
import que_matriz as qm  # noqa: E402

CAPAS_PARCELA = ("PARCELA", "VERTICES", "ETIQUETAS")
TOL = 1e-6


def guardar(doc, ruta):
    doc.saveas(ruta)
    return ruta


def transformar(doc, f, capas=CAPAS_PARCELA):
    """Aplica (M, t) con ezdxf (entity.transform) a las entidades de esas capas."""
    m = g.matriz44(*f)
    for e in doc.modelspace():
        if e.dxf.layer in capas:
            e.transform(m)
    return doc


def par(tmp_path, nombre, *fs, capas=CAPAS_PARCELA):
    """Original y transformado (composición de fs, en orden) guardados en tmp_path."""
    orig = guardar(g.construir(nombre), tmp_path / "orig.dxf")
    doc = g.construir(nombre)
    for f in fs:
        transformar(doc, f, capas)
    return orig, guardar(doc, tmp_path / "trans.dxf")


def comprobar(r, f, familia, det):
    M, t = f
    assert np.allclose(r["M"], M, atol=TOL)
    assert np.allclose(r["t"], t, atol=1e-5)
    assert r["det"] == pytest.approx(det, abs=TOL)
    assert r["familia"] == familia
    assert r["rms"] < 1e-6


def test_rotate_30_alrededor_de_A(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap01_rotate", g.F_ROTATE))
    comprobar(r, g.F_ROTATE, "rotacion", 1.0)
    assert r["lectura"]["angulo"] == pytest.approx(30.0, abs=TOL)
    assert np.allclose(r["lectura"]["centro"], g.PARCELA[0], atol=1e-5)
    assert r["lectura"]["centro_es_vertice"] == "A"
    assert r["homografia"]["rms"] < 1e-6


def test_move(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap02_move_rotate", g.F_MOVE))
    comprobar(r, g.F_MOVE, "traslacion", 1.0)
    assert np.allclose(r["lectura"]["desplazamiento"], g.V_MOVE)


def test_move_rotate_no_conmutan(tmp_path):
    r1 = qm.analizar(*par(tmp_path, "cap02_move_rotate", g.F_MOVE, g.F_ROT_O))
    comprobar(r1, g.F_MOVE_ROTATE, "rotacion", 1.0)
    r2 = qm.analizar(*par(tmp_path, "cap02_move_rotate", g.F_ROT_O, g.F_MOVE))
    comprobar(r2, g.F_ROTATE_MOVE, "rotacion", 1.0)
    assert not np.allclose(r1["t"], r2["t"])


def test_mirror_una_vez_es_reflexion(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap03_mirror", g.F_ESPEJO_1))
    comprobar(r, g.F_ESPEJO_1, "reflexion", -1.0)
    assert r["lectura"]["direccion_eje"] == pytest.approx(90.0, abs=TOL)
    assert r["lectura"]["eje_por"][0] == pytest.approx(g.X_ESPEJO_1, abs=1e-5)


def test_mirror_paralelos_dos_veces_es_traslacion(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap03_mirror", g.F_ESPEJO_1, g.F_ESPEJO_2))
    comprobar(r, (np.eye(2), [2 * (g.X_ESPEJO_2 - g.X_ESPEJO_1), 0.0]), "traslacion", 1.0)


def test_mirror_que_se_cortan_es_rotacion_del_doble(tmp_path):
    e1 = g.reflexion_recta(g.I_ESPEJOS, (1, 0))
    e2 = g.reflexion_recta(g.I_ESPEJOS, (1, 1))  # 45° entre los espejos
    r = qm.analizar(*par(tmp_path, "cap03_mirror", e1, e2))
    comprobar(r, g.F_CORTAN, "rotacion", 1.0)
    assert r["lectura"]["angulo"] == pytest.approx(90.0, abs=TOL)
    assert np.allclose(r["lectura"]["centro"], g.I_ESPEJOS, atol=1e-5)


def test_scale_2_multiplica_areas_por_4(tmp_path):
    f = (2 * np.eye(2), g.PARCELA[0] - 2 * g.PARCELA[0])
    r = qm.analizar(*par(tmp_path, "cap01_rotate", f))
    comprobar(r, f, "similaridad", 4.0)
    assert r["familia_texto"] == "similaridad"
    assert r["lectura"]["factor"] == pytest.approx(2.0, abs=TOL)
    assert r["lectura"]["sentido"] == "se conserva"
    assert np.allclose(r["lectura"]["centro"], g.PARCELA[0], atol=1e-5)


def test_similaridad_inversa_reflexion_y_escala(tmp_path):
    f = (np.diag([-2.0, 2.0]), np.array([4.0, -6.0]))
    r = qm.analizar(*par(tmp_path, "cap01_rotate", f))
    comprobar(r, f, "similaridad", -4.0)
    assert r["familia_texto"] == "similaridad inversa (reflexión + escala)"
    assert r["lectura"]["factor"] == pytest.approx(2.0, abs=TOL)
    assert r["lectura"]["sentido"] == "se invierte"


def test_bloque_x2_y1_det_2(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap04_bloque", g.F_BLOQUE_X2))
    comprobar(r, g.F_BLOQUE_X2, "afinidad", 2.0)
    assert sorted(r["lectura"]["escalas_principales"]) == pytest.approx([1.0, 2.0])


def test_bloque_xm1_det_menos_1_reflexion(tmp_path):
    r = qm.analizar(*par(tmp_path, "cap04_bloque", g.F_BLOQUE_XM1))
    comprobar(r, g.F_BLOQUE_XM1, "reflexion", -1.0)
    assert r["lectura"]["direccion_eje"] == pytest.approx(90.0, abs=TOL)


@pytest.mark.parametrize("escala,familia,det", [((2.0, 1.0), "afinidad", 2.0),
                                                ((-1.0, 1.0), "reflexion", -1.0)])
def test_bloque_insertado_como_insert(tmp_path, escala, familia, det):
    orig = guardar(g.construir("cap04_bloque"), tmp_path / "orig.dxf")
    doc = g.construir("cap04_bloque")
    msp = doc.modelspace()
    for e in [e for e in msp if e.dxf.layer in CAPAS_PARCELA]:
        msp.delete_entity(e)
    msp.add_blockref("PARCELA_BLOQUE", (0, 0), dxfattribs={"xscale": escala[0],
                                                           "yscale": escala[1]})
    r = qm.analizar(orig, guardar(doc, tmp_path / "trans.dxf"))
    comprobar(r, (np.diag(escala), np.zeros(2)), familia, det)


def stretch(doc, ventana, v):
    """STRETCH a mano: se corren los vértices, puntos y etiquetas dentro de la ventana."""
    x0, y0, x1, y1 = ventana
    dentro = lambda p: x0 <= p[0] <= x1 and y0 <= p[1] <= y1
    for e in doc.modelspace():
        if e.dxf.layer == "PARCELA":
            pts = [(x + v[0], y + v[1]) if dentro((x, y)) else (x, y)
                   for x, y in e.get_points("xy")]
            e.set_points(pts, format="xy")
        elif e.dxf.layer == "VERTICES" and dentro(e.dxf.location):
            e.dxf.location = e.dxf.location + (v[0], v[1], 0)
        elif e.dxf.layer == "ETIQUETAS" and dentro(e.dxf.align_point):
            e.dxf.align_point = e.dxf.align_point + (v[0], v[1], 0)
            e.dxf.insert = e.dxf.insert + (v[0], v[1], 0)
    return doc


def test_stretch_no_es_afin(tmp_path):
    orig = guardar(g.construir("cap04_stretch"), tmp_path / "orig.dxf")
    x0, y0, x1, y1 = g.VENTANA_STRETCH
    doc = stretch(g.construir("cap04_stretch"), (x0, y0, x1, y1 + 3), g.V_STRETCH)
    r = qm.analizar(orig, guardar(doc, tmp_path / "trans.dxf"))
    assert r["familia"] == "no_afin"
    assert r["rms"] > 1.0
    assert r["homografia"]["rms"] > qm.TOL_RESIDUO


@pytest.mark.parametrize("f,escalar,familia,det", [
    (g.F_ALIGN_RIGIDO, False, "rotacion", 1.0),
    (g.F_ALIGN_SIMIL, True, "similaridad", 4.0),
])
def test_align_dos_pares(tmp_path, f, escalar, familia, det):
    r = qm.analizar(*par(tmp_path, "cap03_align", f))
    comprobar(r, f, familia, det)
    M, t = np.array(r["M"]), np.array(r["t"])
    a2, b2 = (g.A_SIMIL, g.B_SIMIL) if escalar else (g.A_RIGIDO, g.B_RIGIDO)
    assert np.allclose(M @ g.PARCELA[0] + t, a2, atol=1e-5)
    assert np.allclose(M @ g.PARCELA[1] + t, b2, atol=1e-5)
    s = np.linalg.svd(M, compute_uv=False)
    assert s == pytest.approx([2.0, 2.0] if escalar else [1.0, 1.0])


RESPUESTAS = [(n, resp, f) for n, e in g.EJERCICIOS.items() for resp, f in e["respuestas"]]


@pytest.mark.parametrize("nombre,respuesta,f", RESPUESTAS, ids=[x[1] for x in RESPUESTAS])
def test_respuestas_esperadas(tmp_path, nombre, respuesta, f):
    orig = guardar(g.construir(nombre), tmp_path / "orig.dxf")
    esp = guardar(g.construir_respuesta(nombre, respuesta), tmp_path / "esp.dxf")
    r = qm.analizar(orig, esp)
    if f is None:
        assert r["familia"] == "no_afin"
    else:
        assert np.allclose(r["M"], f[0], atol=TOL)
        assert np.allclose(r["t"], f[1], atol=1e-5)
        assert r["rms"] < 1e-6


def test_generacion_determinista(tmp_path):
    for nombre, e in g.EJERCICIOS.items():
        a = guardar(g.construir(nombre), tmp_path / "a.dxf").read_bytes()
        b = guardar(g.construir(nombre), tmp_path / "b.dxf").read_bytes()
        assert a == b
        assert ezdxf.readfile(tmp_path / "a.dxf").dxfversion == "AC1015"


def test_solo_polilinea_y_textos_en_otra_capa(tmp_path):
    """Sin POINT ni capa ETIQUETAS: vértices de la polilínea y TEXT de una letra."""
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    doc = g.construir("cap01_rotate")
    msp = doc.modelspace()
    for e in [e for e in msp if e.dxf.layer == "VERTICES"]:
        msp.delete_entity(e)
    for e in msp:
        if e.dxf.layer == "ETIQUETAS":
            e.dxf.layer = "0"
    transformar(doc, g.F_ROTATE, capas=("PARCELA", "0"))
    r = qm.analizar(orig, guardar(doc, tmp_path / "trans.dxf"))
    comprobar(r, g.F_ROTATE, "rotacion", 1.0)
    assert r["fuente_transformado"] == "polilínea (PARCELA)"
    assert any("ETIQUETAS" in a for a in r["avisos"])


def test_solo_se_movio_la_polilinea(tmp_path):
    """Polilínea y etiquetas rotadas, POINT quietos: gana la polilínea y se avisa."""
    r = qm.analizar(*par(tmp_path, "cap01_rotate", g.F_ROTATE, capas=("PARCELA", "ETIQUETAS")))
    comprobar(r, g.F_ROTATE, "rotacion", 1.0)
    assert r["fuente_transformado"] == "polilínea (PARCELA)"
    assert any("no coinciden" in a for a in r["avisos"])


def test_dxf_r12_con_polyline(tmp_path):
    """Un DXF R12 (POLYLINE en vez de LWPOLYLINE), como puede guardarlo LibreCAD."""
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    Q = g.aplicar(g.F_ROTATE, g.PARCELA)
    doc = ezdxf.new("R12")
    msp = doc.modelspace()
    msp.add_polyline2d([tuple(p) for p in Q], close=True, dxfattribs={"layer": "PARCELA"})
    for s, p in zip("ABCDE", Q):
        msp.add_text(s, height=1.2, dxfattribs={"layer": "ETIQUETAS", "insert": (p[0] + 1, p[1] + 1)})
    r = qm.analizar(orig, guardar(doc, tmp_path / "r12.dxf"))
    comprobar(r, g.F_ROTATE, "rotacion", 1.0)


def correr(*args):
    return subprocess.run([sys.executable, str(AQUI / "que_matriz.py"), *map(str, args)],
                          capture_output=True, text=True)


def test_cli_json_y_texto(tmp_path):
    orig, trans = par(tmp_path, "cap01_rotate", g.F_ROTATE)
    p = correr(orig, trans, "--json")
    assert p.returncode == 0
    r = json.loads(p.stdout)
    assert r["familia"] == "rotacion"
    p = correr(orig, trans)
    assert p.returncode == 0
    assert "Ángulo de rotación: 30,000°" in p.stdout
    assert "= vértice A" in p.stdout


def test_cli_tol(tmp_path):
    orig = guardar(g.construir("cap04_stretch"), tmp_path / "orig.dxf")
    esp = guardar(g.construir_respuesta("cap04_stretch", "cap04_stretch_10"), tmp_path / "e.dxf")
    assert json.loads(correr(orig, esp, "--json").stdout)["familia"] == "no_afin"
    assert json.loads(correr(orig, esp, "--json", "--tol", "10").stdout)["familia"] == "afinidad"


def test_cli_sin_etiquetas_exit_2(tmp_path):
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    doc = g.construir("cap01_rotate")
    msp = doc.modelspace()
    for e in [e for e in msp if e.dxftype() == "TEXT"]:
        msp.delete_entity(e)
    p = correr(orig, guardar(doc, tmp_path / "sin.dxf"))
    assert p.returncode == 2
    assert "etiquetas" in p.stderr


def test_cli_pocas_etiquetas_comunes_exit_2(tmp_path):
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    tri = guardar(g.construir("cap01_arraypolar"), tmp_path / "tri.dxf")
    doc = g.construir("cap01_rotate")
    for e in doc.modelspace():
        if e.dxftype() == "TEXT" and e.dxf.text in "CDE" and e.dxf.layer == "ETIQUETAS":
            e.dxf.text = {"C": "X", "D": "Y", "E": "Z"}[e.dxf.text]
    p = correr(orig, guardar(doc, tmp_path / "pocas.dxf"))
    assert p.returncode == 2
    assert "3 etiquetas comunes" in p.stderr
    assert correr(tri, tri).returncode == 0


# ---------------------------------------------------------------- Casos de borde
def test_edge_case_archivo_inexistente(tmp_path):
    """Un archivo inexistente debe reportar error de emparejamiento con código 2."""
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    p = correr(orig, tmp_path / "no_existe.dxf")
    assert p.returncode == 2
    assert "no se puede leer" in p.stderr


def test_edge_case_etiquetas_repetidas(tmp_path):
    """Dos textos con la misma letra mayúscula en ETIQUETAS deben detectarse como repetidas."""
    orig = guardar(g.construir("cap01_rotate"), tmp_path / "orig.dxf")
    doc = g.construir("cap01_rotate")
    for e in doc.modelspace():
        if e.dxftype() == "TEXT" and e.dxf.text == "B":
            e.dxf.text = "A"  # Ahora hay dos etiquetas 'A'
            break
    p = correr(orig, guardar(doc, tmp_path / "repetidas.dxf"))
    assert p.returncode == 2
    assert "etiquetas repetidas: A" in p.stderr


def test_edge_case_vertices_colineales(tmp_path):
    """Si los vértices emparejados están alineados en una recta, no determinan una afín 2D."""
    doc = ezdxf.new("R2000")
    msp = doc.modelspace()
    # 3 puntos en la recta y = 2x
    pts = [(0.0, 0.0), (1.0, 2.0), (2.0, 4.0)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": "PARCELA"})
    for s, p in zip("ABC", pts):
        msp.add_point(p, dxfattribs={"layer": "VERTICES"})
        msp.add_text(s, height=1.0, dxfattribs={"layer": "ETIQUETAS", "insert": (p[0] + 0.1, p[1] + 0.1)})
    dxf_col = guardar(doc, tmp_path / "colineales.dxf")
    with pytest.raises(qm.ErrorEmparejamiento, match="alineados"):
        qm.analizar(dxf_col, dxf_col)


def test_edge_case_clasificar_matriz_singular():
    """Una matriz nula o singular (determinante cero) no debe causar ZeroDivisionError."""
    M_cero = np.zeros((2, 2))
    familia, lectura = qm.clasificar(M_cero, np.zeros(2), 0.0, 0.01)
    assert familia == "afinidad"
    assert lectura["factor_area"] == 0.0
    assert lectura["escalas_principales"] == [0.0, 0.0]


def test_edge_case_espacio_modelo_vacio(tmp_path):
    """Un DXF sin ninguna entidad debe lanzar ErrorEmparejamiento."""
    doc = ezdxf.new("R2000")
    dxf_vacio = guardar(doc, tmp_path / "vacio.dxf")
    with pytest.raises(qm.ErrorEmparejamiento, match="espacio modelo está vacío"):
        qm.analizar(dxf_vacio, dxf_vacio)


def test_edge_case_vertices_coincidentes(tmp_path):
    """Vértices coincidentes (degenerados a un punto) deben manejarse sin lanzar ValueError no controlado."""
    # Caso 1: Original con todos los vértices colapsados a un único punto -> debe lanzar ErrorEmparejamiento
    doc_orig = ezdxf.new("R2000")
    msp_orig = doc_orig.modelspace()
    pts_coinc = [(5.0, 5.0), (5.0, 5.0), (5.0, 5.0)]
    msp_orig.add_lwpolyline(pts_coinc, close=True, dxfattribs={"layer": "PARCELA"})
    for s, p in zip("ABC", pts_coinc):
        msp_orig.add_point(p, dxfattribs={"layer": "VERTICES"})
        msp_orig.add_text(s, height=1.0, dxfattribs={"layer": "ETIQUETAS", "insert": (p[0] + 0.1, p[1] + 0.1)})
    dxf_coinc = guardar(doc_orig, tmp_path / "coincidentes.dxf")

    with pytest.raises(qm.ErrorEmparejamiento, match="alineados"):
        qm.analizar(dxf_coinc, dxf_coinc)

    # Caso 2: Original normal, pero transformado colapsado a un punto por transformación singular
    orig_normal = guardar(g.construir("cap01_rotate"), tmp_path / "orig_normal.dxf")
    r = qm.analizar(orig_normal, dxf_coinc)
    assert r["familia"] == "afinidad"
    assert r["det"] == pytest.approx(0.0, abs=1e-9)


