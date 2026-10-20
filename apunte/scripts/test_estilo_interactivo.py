"""Pruebas del alcance interactivo de estilo.py (`--alcance interactivo`).

Correr desde la raíz: uv run pytest -q apunte/scripts/test_estilo_interactivo.py
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import estilo  # noqa: E402

UNIDAD = '''"""Docstring con sólo y "comillas": no es prosa."""
import marimo
app = marimo.App()


@app.cell
def _(mo, lib, x):
    mo.md(r"""
    ## 3.2 Sección con número

    **3.1 La cuenta.** El valor es $0{,}5$ y la flecha va en <span style="color:#1b6f6a">teal</span>.
    Elegí «escala 0.85·I» en el menú y mirá `np.round(x, 2)` = `1.5`.
    """)
    casos = {"corte [[1, 0.5], [0, 1]]": ("matriz", r"Un corte conserva el área.")}
    editor = mo.ui.code_editor(value="x = 1.5  # sólo código", label="Código")
    assert lib.pmat([[0.5]]) == "0.500", "sólo un mensaje"
    mo.md(f"El giro es de {x:.2f} grados y el resultado se ve en la figura.")
    return
'''

MALA = '''import marimo
app = marimo.App()


@app.cell
def _(mo):
    mo.md(r"""
    Esto sólo vale si "la matriz" es $0.5$ veces la otra.
    Mueva el deslizador. Hay que desaprender la costumbre.
    La estación total mide ángulos.
    """)
    _ok = ("success", "Bien: la cuenta da 'lo mismo' "
                      "en los dos casos.")
    return
'''


def _analizar(tmp_path, nombre, texto):
    p = tmp_path / nombre
    p.write_text(texto, encoding="utf-8")
    return estilo.analizar_interactivo(p)


def test_unidad_limpia_no_tiene_hallazgos(tmp_path):
    r = _analizar(tmp_path, "unidad.py", UNIDAD)
    assert r["total"] == 0, r["hallazgos"]


def test_unidad_con_errores(tmp_path):
    r = _analizar(tmp_path, "mala.py", MALA)
    c = r["conteo"]
    assert c["1"] == 1            # sólo
    assert c["2"] == 2            # "la matriz" y 'lo mismo' (cadena partida en dos renglones)
    assert c["3"] == 1            # $0.5$
    assert c["13"] == 1           # Mueva
    assert c["12"] == 1           # desaprender
    assert c["10"] == 1           # estación total


def test_es_decir_y_desarrollo(tmp_path):
    md = "\n".join(["Es decir, uno.", "Es decir, dos.", "Desarrollo. Empezamos."] + ["texto"] * 10)
    r = _analizar(tmp_path, "ficha.md", md)
    assert r["conteo"]["5"] == 1 and r["conteo"]["6"] == 1


def test_md_frontmatter_y_codigo(tmp_path):
    md = '---\ntitulo: "Capítulo 1"\n---\n\nTexto con `"código"` y\n\n```python\nx = "sólo 1.5"\n```\n\nUn «control 0.5».\n'
    r = _analizar(tmp_path, "ficha.md", md)
    assert r["total"] == 0, r["hallazgos"]


def test_yaml_no_mira_comillas_de_sintaxis(tmp_path):
    y = 'unidades:\n  - id: "01a"\n    pregunta: "¿Se mueve el mojón?"\n    gancho: "Esto sólo pasa una vez."\n'
    r = _analizar(tmp_path, "mapa.yaml", y)
    assert r["conteo"]["2"] == 0 and r["conteo"]["1"] == 1


def test_offset_utf8_y_syntax_error(tmp_path, capsys):
    # Caracteres multibyte (tildes, símbolos matemáticos) en la misma línea antes de mo.ui / assert
    codigo = 'import marimo\n_x = ("áéíóú—αβγ", mo.ui.slider(0, 1, label="escala 0.85·I"))\n'
    r = _analizar(tmp_path, "utf8.py", codigo)
    assert r["total"] == 0, r["hallazgos"]

    # Error de sintaxis emite advertencia clara a stderr
    _analizar(tmp_path, "roto.py", "def f(:\n    pass\n")
    err = capsys.readouterr().err
    assert "advertencia: error de sintaxis" in err


def test_lo_interactivo_del_repo_esta_limpio():
    """unidades/, clases/, mapa/ y moodle/ (los .md de la raíz se revisan en CI con el mismo script)."""
    malos = [(r["archivo"], r["conteo"]) for r in estilo.analizar_interactivo_todo()
             if "/" in r["archivo"] and r["total"]]
    assert not malos, malos
