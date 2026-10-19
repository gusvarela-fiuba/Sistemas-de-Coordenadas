"""Pruebas de los ejercicios CAD de los capítulos 6 (área, SCALE y determinante) y 9
(UCS alineado con el frente AB: cambio de base).

Correr con: uv run pytest tools/cad -q
"""
import json
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

AREA_PARCELA = 655.0
TOL = 1e-6


def par_respuesta(tmp_path, nombre, respuesta):
    orig = tmp_path / "orig.dxf"
    esp = tmp_path / "esp.dxf"
    g.construir(nombre).saveas(orig)
    g.construir_respuesta(nombre, respuesta).saveas(esp)
    return orig, esp


# ---------------------------------------------------------------- capítulo 6
def test_area_de_la_parcela_por_cunas():
    assert g.area_con_signo(g.PARCELA) == pytest.approx(AREA_PARCELA)
    assert g.cunas(g.PARCELA) == pytest.approx([-85.0, 272.0, 328.0, 270.0, -130.0])
    assert sum(g.cunas(g.PARCELA)) == pytest.approx(AREA_PARCELA)
    # recorrida al revés, el área cambia de signo; trasladada, no cambia
    assert g.area_con_signo(g.PARCELA[::-1]) == pytest.approx(-AREA_PARCELA)
    assert g.area_con_signo(g.PARCELA - g.PARCELA[0]) == pytest.approx(AREA_PARCELA)
    assert qm.area_poligono(g.PARCELA) == pytest.approx(AREA_PARCELA)


def test_cap06_area_cunas_identidad(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap06_area", "cap06_area_cunas"))
    assert r["familia"] == "identidad"
    assert r["area_original"] == pytest.approx(AREA_PARCELA)
    assert r["area_transformado"] == pytest.approx(AREA_PARCELA)
    assert r["cociente_areas"] == pytest.approx(1.0)


def test_cap06_area_cunas_trae_los_triangulos(tmp_path):
    _, esp = par_respuesta(tmp_path, "cap06_area", "cap06_area_cunas")
    msp = ezdxf.readfile(esp).modelspace()
    textos = sorted(e.dxf.text for e in msp.query("TEXT[layer=='CUNAS']"))
    assert textos == sorted(["-85", "+272", "+328", "+270", "-130"])
    assert len(msp.query("LINE[layer=='CUNAS']")) == 5
    assert [e.dxf.text for e in msp.query("TEXT[layer=='AREA']")] == ["S = 655 m2"]


def test_cap06_scale_2_multiplica_el_area_por_4(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap06_scale", "cap06_scale_2"))
    assert r["familia"] == "similaridad"
    assert r["det"] == pytest.approx(4.0, abs=TOL)
    assert r["lectura"]["factor"] == pytest.approx(2.0, abs=TOL)
    assert r["lectura"]["centro_es_vertice"] == "A"
    assert r["area_original"] == pytest.approx(AREA_PARCELA)
    assert r["area_transformado"] == pytest.approx(4 * AREA_PARCELA)
    assert r["cociente_areas"] == pytest.approx(abs(r["det"]))


def test_cap06_scale_hecho_con_ezdxf_coincide_con_la_respuesta(tmp_path):
    """SCALE x2 desde A aplicado a las entidades (como el CAD) da lo mismo que la respuesta."""
    orig = tmp_path / "orig.dxf"
    g.construir("cap06_scale").saveas(orig)
    doc = g.construir("cap06_scale")
    m = g.matriz44(*g.F_SCALE_2)
    for e in doc.modelspace():
        if e.dxf.layer in ("PARCELA", "VERTICES", "ETIQUETAS"):
            e.transform(m)
    doc.saveas(tmp_path / "trans.dxf")
    r = qm.analizar(orig, tmp_path / "trans.dxf")
    assert np.allclose(r["M"], g.F_SCALE_2[0], atol=TOL)
    assert np.allclose(r["t"], g.F_SCALE_2[1], atol=1e-5)
    assert r["cociente_areas"] == pytest.approx(4.0)


def test_cap06_bloque_x2_y1_duplica_el_area(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap06_scale", "cap06_bloque_x2_y1_area"))
    assert r["familia"] == "afinidad"
    assert r["det"] == pytest.approx(2.0, abs=TOL)
    assert r["area_transformado"] == pytest.approx(2 * AREA_PARCELA)
    assert r["cociente_areas"] == pytest.approx(2.0)
    assert any("INSERT" in a for a in r["avisos"])


def test_reflexion_conserva_el_area(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap04_bloque", "cap04_bloque_xm1"))
    assert r["det"] == pytest.approx(-1.0, abs=TOL)
    assert r["cociente_areas"] == pytest.approx(1.0)


def test_stretch_cambia_el_area_sin_ser_afin(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap04_stretch", "cap04_stretch_10"))
    assert r["familia"] == "no_afin"
    assert r["cociente_areas"] != pytest.approx(abs(r["det"]), abs=1e-3)


# ---------------------------------------------------------------- capítulo 9
NUEVAS_FRENTE = {"A": (0.0, 0.0), "B": (25.0, 0.0), "C": (36.08, 16.56),
                 "D": (21.28, 22.96), "E": (2.32, 22.24)}


def test_base_del_frente_ortonormal():
    C = g.C_FRENTE
    assert np.allclose(C[:, 0], [0.96, 0.28])
    assert np.allclose(C[:, 1], [-0.28, 0.96])
    assert np.allclose(C.T @ C, np.eye(2))
    assert np.linalg.det(C) == pytest.approx(1.0)


def test_coordenadas_en_el_ucs_del_frente():
    C, A = g.C_FRENTE, g.PARCELA[0]
    for s, p in zip("ABCDE", g.PARCELA):
        nuevo = np.linalg.solve(C, p - A)  # C^{-1}(p - A)
        assert np.allclose(nuevo, NUEVAS_FRENTE[s], atol=1e-9)
        assert np.allclose(g.aplicar(g.F_UCS_FRENTE, [p])[0], nuevo, atol=1e-9)


def test_cap09_ucs_frente_lectura_pasiva(tmp_path):
    orig, esp = par_respuesta(tmp_path, "cap09_ucs", "cap09_ucs_frente")
    r = qm.analizar(orig, esp)
    assert r["familia"] == "rotacion"
    assert r["det"] == pytest.approx(1.0, abs=TOL)
    assert np.allclose(r["M"], g.C_FRENTE.T, atol=TOL)
    assert np.allclose(r["t"], [-12.4, -6.8], atol=1e-5)
    assert r["lectura"]["angulo"] == pytest.approx(-16.2602, abs=1e-4)
    assert r["cociente_areas"] == pytest.approx(1.0)
    leidos = qm.extraer(esp)["vertices"]
    for s, v in NUEVAS_FRENTE.items():
        assert np.allclose(leidos[s], v, atol=1e-9)


def test_cap09_ucs_activa_misma_matriz_centro_A(tmp_path):
    r = qm.analizar(*par_respuesta(tmp_path, "cap09_ucs", "cap09_ucs_activa"))
    assert r["familia"] == "rotacion"
    assert np.allclose(r["M"], g.C_FRENTE.T, atol=TOL)
    assert np.allclose(r["t"], [-2.4, 3.2], atol=1e-5)
    assert r["lectura"]["centro_es_vertice"] == "A"
    assert r["cociente_areas"] == pytest.approx(1.0)


# ---------------------------------------------------------------- generales
def test_capas_nuevas_solo_en_los_dxf_nuevos():
    for nombre in g.EJERCICIOS:
        tiene = "CUNAS" in g.construir(nombre).layers
        assert tiene == nombre.startswith(("cap06", "cap09"))


def test_cli_imprime_el_area_y_el_cociente(tmp_path):
    orig, esp = par_respuesta(tmp_path, "cap06_scale", "cap06_scale_2")
    p = subprocess.run([sys.executable, str(AQUI / "que_matriz.py"), str(orig), str(esp)],
                       capture_output=True, text=True)
    assert p.returncode == 0
    assert ("Área (A, B, C, D, E, en ese orden): 655,000 m² → 2620,000 m² "
            "(cociente = 4,000; |det M| = 4,000)") in p.stdout
    p = subprocess.run([sys.executable, str(AQUI / "que_matriz.py"), str(orig), str(esp),
                        "--json"], capture_output=True, text=True)
    assert json.loads(p.stdout)["cociente_areas"] == pytest.approx(4.0)
