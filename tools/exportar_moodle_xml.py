#!/usr/bin/env python3
"""Exporta el banco de autoevaluación (`unidades/banco_autoevaluacion.py`) a Moodle XML.

Genera `moodle/moodle_banco_120_preguntas_cb104.xml`: por cada unidad del hilo (orden de
mapa/_fragmentos/unidades.yaml) y cada nivel (elemental, medio, avanzado) una pregunta de categoría
`$course$/top/CB104_Sistemas_de_Coordenadas/Unidad_NN_<id>/<nivel>` seguida de sus dos preguntas
`multichoice` (4 opciones, una correcta, la explicación de cada opción como feedback).

Las fórmulas `$...$` pasan a `\\( ... \\)` y `$$...$$` a `\\[ ... \\]` (filtro MathJax de Moodle); el Markdown
mínimo (`**negrita**`, `` `código` ``, saltos de línea) se convierte a HTML.

Uso:  uv run python tools/merge_banco.py && uv run python tools/exportar_moodle_xml.py [--salida ARCHIVO] [--parcial]
      --salida   archivo de salida (default: moodle/moodle_banco_120_preguntas_cb104.xml)
      --parcial  admite un banco con menos de 20 unidades (mientras se redacta)
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
if str(RAIZ) not in sys.path:
    sys.path.insert(0, str(RAIZ))

from unidades.banco_autoevaluacion import BANCO_AUTOEVALUACION  # noqa: E402

SALIDA_DEFAULT = RAIZ / "moodle" / "moodle_banco_120_preguntas_cb104.xml"
NIVELES = ("elemental", "medio", "avanzado")
CATEGORIA_RAIZ = "$course$/top/CB104_Sistemas_de_Coordenadas"
UNIDADES_ESPERADAS = 20

# ---------------------------------------------------------------------------------------------------
# Unidades del hilo: orden e información de mapa/_fragmentos/unidades.yaml
# ---------------------------------------------------------------------------------------------------


def unidades_hilo() -> list[dict]:
    datos = yaml.safe_load((RAIZ / "mapa" / "_fragmentos" / "unidades.yaml").read_text(encoding="utf-8"))
    return [{"id": u["id"], "titulo": str(u.get("titulo", "")).strip()} for u in datos["unidades"]]


# ---------------------------------------------------------------------------------------------------
# Texto: Markdown mínimo + fórmulas → HTML para el filtro MathJax de Moodle
# ---------------------------------------------------------------------------------------------------

# Primero `$$...$$` (display), después `$...$` (inline), y protegemos el código entre acentos graves.
# Un `\$` no abre ni cierra fórmula. DOTALL para que una fórmula display pueda ocupar varias líneas.
_TOKENS = re.compile(
    r"(?<!\\)\$\$(?P<display>.+?)(?<!\\)\$\$"
    r"|(?<!\\)\$(?P<inline>[^$\n]+?)(?<!\\)\$"
    r"|`(?P<codigo>[^`\n]+)`",
    re.DOTALL,
)
_NEGRITA = re.compile(r"\*\*(.+?)\*\*", re.DOTALL)


def escapar(texto: str) -> str:
    """Escapa `&`, `<` y `>`. Lo usamos también adentro de los CDATA: así el HTML queda bien formado,
    MathJax lee el texto ya decodificado y nunca puede aparecer la secuencia `]]>`."""
    return texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _prosa_a_html(texto: str) -> str:
    html = escapar(texto)
    html = _NEGRITA.sub(r"<strong>\1</strong>", html)
    return html.replace("\\$", "$")


def convertir_fragmento(texto: str) -> str:
    """Convierte una cadena de prosa + fórmulas a HTML (sin envolver en párrafos)."""
    partes: list[str] = []
    pos = 0
    for m in _TOKENS.finditer(texto):
        partes.append(_prosa_a_html(texto[pos:m.start()]))
        if m.group("display") is not None:
            partes.append("\\[" + escapar(m.group("display").strip()) + "\\]")
        elif m.group("inline") is not None:
            partes.append("\\(" + escapar(m.group("inline").strip()) + "\\)")
        else:
            partes.append("<code>" + escapar(m.group("codigo")) + "</code>")
        pos = m.end()
    partes.append(_prosa_a_html(texto[pos:]))
    return "".join(partes)


def a_html(texto: str) -> str:
    """Texto completo → uno o más `<p>`; líneas en blanco separan párrafos, saltos simples son `<br>`."""
    parrafos = [p.strip() for p in re.split(r"\n\s*\n", texto.strip()) if p.strip()]
    salida = []
    for p in parrafos:
        lineas = [convertir_fragmento(l.strip()) for l in p.split("\n")]
        salida.append("<p>" + "<br>".join(lineas) + "</p>")
    return "".join(salida)


def cdata(html: str) -> str:
    assert "]]>" not in html, "un CDATA no puede contener ']]>'"
    return f"<![CDATA[{html}]]>"


# ---------------------------------------------------------------------------------------------------
# Armado del XML
# ---------------------------------------------------------------------------------------------------


def pregunta_categoria(ruta: str, info_html: str = "") -> str:
    return (
        '  <question type="category">\n'
        "    <category>\n"
        f"      <text>{escapar(ruta)}</text>\n"
        "    </category>\n"
        '    <info format="html">\n'
        f"      <text>{cdata(info_html) if info_html else ''}</text>\n"
        "    </info>\n"
        "  </question>\n"
    )


def pregunta_multichoice(p: dict, unidad_id: str, nn: str, nivel: str) -> str:
    pid = str(p["id"])
    nombre = f"{pid} · Unidad {nn} · {nivel}"
    lineas = [
        '  <question type="multichoice">\n',
        f"    <name><text>{escapar(nombre)}</text></name>\n",
        f'    <questiontext format="html">\n      <text>{cdata(a_html(p["enunciado"]))}</text>\n    </questiontext>\n',
        '    <generalfeedback format="html"><text></text></generalfeedback>\n',
        "    <defaultgrade>1</defaultgrade>\n",
        "    <penalty>0.3333333</penalty>\n",
        "    <hidden>0</hidden>\n",
        f"    <idnumber>{escapar(pid)}</idnumber>\n",
        "    <single>true</single>\n",
        "    <shuffleanswers>true</shuffleanswers>\n",
        "    <answernumbering>abc</answernumbering>\n",
        "    <showstandardinstruction>0</showstandardinstruction>\n",
        '    <correctfeedback format="html"><text>Correcto.</text></correctfeedback>\n',
        '    <partiallycorrectfeedback format="html"><text></text></partiallycorrectfeedback>\n',
        '    <incorrectfeedback format="html"><text>Incorrecto.</text></incorrectfeedback>\n',
    ]
    for o in p["opciones"]:
        fraction = "100" if o.get("correcta") is True else "0"
        lineas.append(
            f'    <answer fraction="{fraction}" format="html">\n'
            f"      <text>{cdata(a_html(o['texto']))}</text>\n"
            f'      <feedback format="html"><text>{cdata(a_html(o["explicacion"]))}</text></feedback>\n'
            "    </answer>\n"
        )
    lineas.append(
        "    <tags>\n"
        "      <tag><text>cb104</text></tag>\n"
        f"      <tag><text>{escapar(nivel)}</text></tag>\n"
        f"      <tag><text>{escapar(unidad_id)}</text></tag>\n"
        "    </tags>\n"
    )
    lineas.append("  </question>\n")
    return "".join(lineas)


def validar_banco(banco: dict[str, list[dict]], hilo: list[dict], parcial: bool) -> list[str]:
    errores = []
    ids_hilo = [u["id"] for u in hilo]
    faltan = [uid for uid in ids_hilo if uid not in banco]
    if faltan and not parcial:
        errores.append(f"banco incompleto: faltan {len(faltan)} de {len(ids_hilo)} unidades ({', '.join(faltan)}); "
                       "usar --parcial para exportar lo que hay")
    extra = sorted(set(banco) - set(ids_hilo))
    if extra:
        errores.append(f"unidades que no están en el hilo: {extra}")
    for uid, preguntas in banco.items():
        for p in preguntas:
            pid = p.get("id", "?")
            if p.get("nivel") not in NIVELES:
                errores.append(f"{pid}: nivel desconocido {p.get('nivel')!r}")
            ops = p.get("opciones", [])
            if len(ops) != 4:
                errores.append(f"{pid}: {len(ops)} opciones, se esperan 4")
            if sum(1 for o in ops if o.get("correcta") is True) != 1:
                errores.append(f"{pid}: debe haber exactamente una opción correcta")
    return errores


def generar(banco: dict[str, list[dict]], hilo: list[dict]) -> tuple[str, dict[str, int]]:
    partes = ['<?xml version="1.0" encoding="UTF-8"?>\n<quiz>\n']
    conteo = {"unidades": 0, "categorias": 0, "preguntas": 0}
    for n, u in enumerate(hilo):
        uid = u["id"]
        if uid not in banco:
            continue
        conteo["unidades"] += 1
        nn = f"{n:02d}"
        preguntas = banco[uid]
        for nivel in NIVELES:
            del_nivel = [p for p in preguntas if p.get("nivel") == nivel]
            if not del_nivel:
                continue
            ruta = f"{CATEGORIA_RAIZ}/Unidad_{nn}_{uid}/{nivel}"
            info = f"<p>Unidad {nn}: {escapar(u['titulo'])} — nivel {nivel}</p>" if u["titulo"] else ""
            partes.append(pregunta_categoria(ruta, info))
            conteo["categorias"] += 1
            for p in del_nivel:
                partes.append(pregunta_multichoice(p, uid, nn, nivel))
                conteo["preguntas"] += 1
    partes.append("</quiz>\n")
    return "".join(partes), conteo


def verificar(ruta: Path, esperadas: int) -> None:
    root = ET.parse(ruta).getroot()
    assert root.tag == "quiz", f"raíz {root.tag!r}, se esperaba 'quiz'"
    mc = root.findall("question[@type='multichoice']")
    assert len(mc) == esperadas, f"{len(mc)} preguntas multichoice en el XML, el banco tiene {esperadas}"
    for q in mc:
        nombre = q.findtext("name/text")
        respuestas = q.findall("answer")
        assert len(respuestas) == 4, f"{nombre}: {len(respuestas)} respuestas"
        correctas = [a for a in respuestas if a.get("fraction") == "100"]
        assert len(correctas) == 1, f"{nombre}: {len(correctas)} respuestas con fraction=100"
        assert q.findtext("questiontext/text", "").strip(), f"{nombre}: enunciado vacío"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--salida", type=Path, default=SALIDA_DEFAULT)
    ap.add_argument("--parcial", action="store_true")
    args = ap.parse_args()

    hilo = unidades_hilo()
    errores = validar_banco(BANCO_AUTOEVALUACION, hilo, args.parcial)
    if errores:
        print("\n".join("  - " + e for e in errores), file=sys.stderr)
        return 1

    xml, conteo = generar(BANCO_AUTOEVALUACION, hilo)
    salida: Path = args.salida if args.salida.is_absolute() else RAIZ / args.salida
    salida.parent.mkdir(parents=True, exist_ok=True)
    salida.write_text(xml, encoding="utf-8")
    verificar(salida, conteo["preguntas"])

    tam = salida.stat().st_size
    try:
        mostrar = salida.relative_to(RAIZ)
    except ValueError:
        mostrar = salida
    print(f"escrito {mostrar}: {conteo['unidades']}/{len(hilo)} unidades, {conteo['categorias']} categorías, "
          f"{conteo['preguntas']} preguntas, {tam / 1024:.1f} KiB")
    if conteo["unidades"] < UNIDADES_ESPERADAS:
        print(f"aviso: banco parcial ({conteo['unidades']} de {UNIDADES_ESPERADAS} unidades)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
