"""Enlaces de la portada al apunte (tools/enlaces_portada.yaml, leído por tools/build.py).

Falla si una unidad del mapa queda sin enlace principal, si enlaza más de tres secciones, si
repite una etiqueta, si un enlace apunta a un \\label inexistente en el apunte o si dos unidades
consecutivas (en el orden de la portada) tienen la misma lista. También comprueba que la portada
generada respete la tabla.
"""
import importlib.util
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def build():
    spec = importlib.util.spec_from_file_location("build_portada", RAIZ / "tools" / "build.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["build_portada"] = mod
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def datos(build):
    return build.cargar_mapa(build.MAPA)


@pytest.fixture(scope="module")
def tabla(build):
    return build.enlaces_portada()


@pytest.fixture(scope="module")
def etiquetas(build):
    return build.etiquetas_apunte()


def orden_portada(datos):
    return [str(u["id"]) for u in datos["unidades"]]


def test_cada_unidad_tiene_principal(datos, tabla):
    faltan = [u for u in orden_portada(datos) if not tabla.get(u)]
    assert not faltan, f"unidades sin enlace principal: {faltan}"
    sobran = [u for u in tabla if u not in orden_portada(datos)]
    assert not sobran, f"entradas que no son unidades del mapa: {sobran}"


def test_como_maximo_tres_y_sin_repetir(tabla, build):
    for uid, lista in tabla.items():
        assert len(lista) <= build.MAX_ENLACES_PORTADA == 3, f"{uid}: {len(lista)} enlaces"
        assert len(set(lista)) == len(lista), f"{uid}: etiqueta repetida {lista}"


def test_etiquetas_existen(tabla, etiquetas):
    rotas = [(uid, lab) for uid, lista in tabla.items() for lab in lista if lab not in etiquetas]
    assert not rotas, f"etiquetas inexistentes en el apunte: {rotas}"


def test_consecutivas_distintas(datos, tabla):
    orden = orden_portada(datos)
    iguales = [(a, b) for a, b in zip(orden, orden[1:]) if tabla.get(a) and tabla.get(a) == tabla.get(b)]
    assert not iguales, f"unidades consecutivas con la misma lista: {iguales}"


def test_validador_del_build_en_cero(build, datos, tabla, etiquetas):
    assert build.validar_enlaces_portada(datos, tabla, etiquetas) == []


def test_validador_detecta_errores(build, datos, tabla, etiquetas):
    orden = orden_portada(datos)
    mala = dict(tabla)
    mala[orden[0]] = []                                     # sin principal
    mala[orden[2]] = list(tabla[orden[2]]) + ["sec:no-existe"]  # cuatro enlaces, uno roto
    mala[orden[4]] = list(tabla[orden[5]])                  # igual a la siguiente
    errores = "\n".join(build.validar_enlaces_portada(datos, mala, etiquetas))
    assert "no tiene enlace principal" in errores
    assert "máximo 3" in errores
    assert "sec:no-existe" in errores
    assert "consecutivas" in errores


def test_portada_respeta_la_tabla(build, datos, tabla, tmp_path):
    build.validar(datos)
    build.generar_indice(datos, {}, set(), True, tmp_path)
    portada = (tmp_path / "index.html").read_text(encoding="utf-8")
    for i, uid in enumerate(orden_portada(datos)):
        m = re.search(rf'<li class="unidad" id="unidad-{i}".*?</li>\s*(?=<li class="unidad"|</ol>)', portada, re.S)
        assert m, f"no encuentro la entrada de la unidad {i} ({uid})"
        destinos = re.findall(r'href="apunte\.pdf#nameddest=([^"]+)"', m.group(0))
        assert destinos == tabla[uid], f"{uid}: la portada enlaza {destinos}, la tabla dice {tabla[uid]}"
