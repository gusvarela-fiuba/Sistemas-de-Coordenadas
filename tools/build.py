#!/usr/bin/env python3
"""Genera el sitio estático `site/` de Sistemas de Coordenadas (CB104).

Entradas (relativas a la raíz del repo):
  mapa/mapa.yaml                        mapa de conceptos (esquema en mapa/ESQUEMA.md)
  clases/*.md                           fichas por clase
  unidades/*.py                         notebooks marimo
  apunte/Apunte_Sistemas_de_Coordenadas.pdf
  apunte/contenido/NN-*.tex             sólo para validar prefijos y leer títulos de sección

Salida:
  site/index.html                       portada = el hilo conductor: tres entradas (Empezar / Seguir la cursada / Repasar)
                                        y una entrada por unidad (pregunta, gancho, estado, clases, enlaces),
                                        más la última unidad "Lo que viene" con las clases sin unidad
  site/mapa.html                        mapa de conceptos (SVG inline) con filtro de ruta y "hasta la clase N",
                                        y la lista de clases con fechas y estado
  site/clases/<id>.html                 fichas (markdown → html, KaTeX desde CDN) con etiquetas de procedencia y validación
  site/unidades/<id>/index.html         notebooks exportados a WASM (marimo export html-wasm) desde la copia
  site/_build/<archivo>.py              generada con unidades/cb104.py embebido en la celda `# cb104:inline`
  site/apunte.pdf                       copia del apunte
  site/.nojekyll                        para GitHub Pages

Uso:  uv run tools/build.py [--skip-wasm] [--only <unidad_id>] [--out site]
"""

from __future__ import annotations

import argparse
import datetime as _dt
import html
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import markdown
import yaml

RAIZ = Path(__file__).resolve().parent.parent
MAPA = RAIZ / "mapa" / "mapa.yaml"
CONTENIDO_APUNTE = RAIZ / "apunte" / "contenido"
PDF_APUNTE = RAIZ / "apunte" / "Apunte_Sistemas_de_Coordenadas.pdf"
DIR_CLASES = RAIZ / "clases"

ESTADOS_CLASE = ("con-transcripcion", "reconstruida", "no-dictada", "anticipada")
ESTADOS_UNIDAD = ("piloto", "migrada", "legacy", "pendiente")
ESTADOS_EXPORTABLES = ("piloto", "migrada")
TITULO_CAMINO = "Sistemas de Coordenadas — Hilo conductor y lecciones interactivas"
TITULO_MAPA = "Sistemas de Coordenadas — mapa de conceptos"

# paleta del apunte
TEAL, RUST, GOLD = "#1b6f6a", "#b5532a", "#c9a227"
VIOLETA = "#7a4e9e"  # procedencia "anticipada" (armada antes de dictarse)
COLOR_ESTADO = {
    "con-transcripcion": (TEAL, "#e3f1f0"),
    "reconstruida": (GOLD, "#faf3dc"),
    "no-dictada": (RUST, "#f8e6dd"),
    "anticipada": (VIOLETA, "#ece4f3"),
}
ETIQUETA_ESTADO = {
    "con-transcripcion": "con transcripción",
    "reconstruida": "reconstruida",
    "no-dictada": "no dictada",
    "anticipada": "anticipación, pendiente de validar",
}
ETIQUETA_ESTADO_UNIDAD = {
    "piloto": "piloto",
    "migrada": "migrada",
    "legacy": "legacy (no publicada)",
    "pendiente": "pendiente",
}
NIVELES = ("troncal", "complementario", "avanzado")
VALIDACIONES = ("pendiente", "revisado", "validado-catedra")
ETIQUETA_VALIDACION = {
    "pendiente": "validación pendiente",
    "revisado": "revisado",
    "validado-catedra": "validado por la cátedra",
}
# estado de una unidad en la portada (calculado, no viene del yaml)
ETIQUETA_UNIDAD = {
    "lista": ("lista", TEAL),
    "en-clase": ("en clase", GOLD),
    "todavia-no": ("todavía no", RUST),
}

KATEX_VERSION = "0.16.11"
KATEX_CDN = f"https://cdnjs.cloudflare.com/ajax/libs/KaTeX/{KATEX_VERSION}"

CSS = f"""
:root {{ --teal: {TEAL}; --rust: {RUST}; --gold: {GOLD}; --tinta: #222; --gris: #666; --fondo: #fdfcf9; --linea: #e4e0d6; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; padding: 0 16px 48px; background: var(--fondo); color: var(--tinta);
       font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; line-height: 1.5; }}
main {{ max-width: 960px; margin: 0 auto; }}
h1 {{ color: var(--teal); font-size: 1.7rem; margin: 1.2em 0 .2em; line-height: 1.2; }}
h2 {{ color: var(--rust); font-size: 1.25rem; margin: 1.6em 0 .5em; border-bottom: 2px solid var(--linea); padding-bottom: .2em; }}
h3 {{ font-size: 1.05rem; margin: 1.2em 0 .4em; }}
a {{ color: var(--teal); }}
a:hover {{ color: var(--rust); }}
.guia {{ color: var(--gris); font-style: italic; margin: 0 0 1em; }}
.mapa {{ overflow-x: auto; border: 1px solid var(--linea); border-radius: 6px; background: #fff; padding: 8px; }}
.mapa svg {{ display: block; height: auto; }}
.leyenda {{ display: flex; flex-wrap: wrap; gap: 14px; font-size: .9rem; color: var(--gris); margin: .5em 0 0; }}
.leyenda span::before {{ content: ""; display: inline-block; width: 14px; height: 14px; border-radius: 3px; margin-right: 6px;
                          vertical-align: -2px; border: 2px solid var(--c); background: var(--f); }}
.clases {{ list-style: none; padding: 0; margin: 0; }}
.clase {{ border: 1px solid var(--linea); border-left: 5px solid var(--c); border-radius: 6px; background: #fff;
          padding: 10px 14px; margin: 0 0 10px; }}
.clase .cab {{ display: flex; flex-wrap: wrap; gap: 6px 12px; align-items: baseline; }}
.clase .id {{ font-weight: 700; color: var(--c); }}
.clase .tit {{ font-weight: 600; font-size: 1.05rem; }}
.clase .estado {{ font-size: .8rem; color: #fff; background: var(--c); border-radius: 10px; padding: 1px 9px; }}
.clase .fechas {{ color: var(--gris); font-size: .9rem; margin: 2px 0; }}
.links {{ display: flex; flex-wrap: wrap; gap: 6px; font-size: .92rem; margin: 6px 0 0; }}
.links span {{ display: inline-block; max-width: 100%; white-space: normal; overflow-wrap: anywhere; border: 1px solid var(--linea);
               border-radius: 10px; padding: 1px 9px; background: #f7f5ef; }}
.links span.pend {{ color: var(--gris); }}
.pend {{ color: var(--gris); }}
.pie {{ color: var(--gris); font-size: .85rem; margin-top: 3em; border-top: 1px solid var(--linea); padding-top: .8em; }}
/* fichas */
.ficha table {{ border-collapse: collapse; margin: 1em 0; }}
.ficha th, .ficha td {{ border: 1px solid var(--linea); padding: 4px 10px; }}
.ficha th {{ background: #f3efe4; }}
.ficha pre {{ background: #f3efe4; padding: 10px 12px; overflow-x: auto; border-radius: 4px; font-size: .9rem; }}
.ficha code {{ font-family: Menlo, Consolas, monospace; }}
.ficha blockquote {{ border-left: 4px solid var(--gold); margin: 1em 0; padding: 2px 12px; color: var(--gris); }}
.ficha img {{ max-width: 100%; }}
.volver {{ font-size: .9rem; margin: 1em 0 0; }}
.volver a {{ margin-right: 14px; }}
.katex-display {{ overflow-x: auto; overflow-y: hidden; }}
/* etiquetas (procedencia, validación, nivel, estado de unidad) */
.etqs {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0; }}
.etq {{ display: inline-block; font-size: .78rem; line-height: 1.5; border-radius: 10px; padding: 1px 9px;
        border: 1.5px solid var(--c, var(--gris)); color: var(--c, var(--gris)); background: #fff; white-space: nowrap; }}
.etq.solida {{ color: #fff; background: var(--c, var(--gris)); }}
.ficha-etqs {{ margin: 1em 0 -.6em; }}
/* portada: entradas y unidades (el hilo conductor) */
.entradas {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 10px; margin: 1em 0 1.5em; }}
.entrada {{ display: block; border: 1.5px solid var(--teal); border-radius: 8px; padding: 10px 14px; background: #fff;
            text-decoration: none; color: var(--tinta); }}
.entrada:hover {{ border-color: var(--rust); color: var(--tinta); }}
.entrada b {{ display: block; color: var(--teal); font-size: 1.05rem; }}
.entrada:hover b {{ color: var(--rust); }}
.entrada small {{ color: var(--gris); }}
.hilo {{ list-style: none; padding: 0; margin: 0; }}
.unidad {{ border: 1px solid var(--linea); border-left: 5px solid var(--c); border-radius: 6px; background: #fff;
             padding: 12px 14px; margin: 0 0 12px; }}
.unidad .cab {{ display: flex; flex-wrap: wrap; gap: 6px 12px; align-items: baseline; }}
.unidad .num {{ font-weight: 700; color: var(--c); }}
.unidad .tit {{ font-weight: 600; font-size: 1.1rem; }}
.unidad .pregunta {{ margin: 6px 0 2px; font-size: 1.02rem; }}
.unidad .gancho {{ margin: 0 0 6px; color: var(--gris); font-style: italic; font-size: .95rem; }}
.unidad .sus-clases {{ list-style: none; padding: 0; margin: 6px 0 0; }}
.unidad .sus-clases li {{ display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: baseline; font-size: .93rem;
                             padding: 3px 0; border-top: 1px dashed var(--linea); }}
.unidad .sus-clases .cid {{ font-weight: 600; white-space: nowrap; }}
/* mapa: controles */
.controles {{ display: flex; flex-wrap: wrap; gap: 10px 24px; align-items: center; margin: .6em 0; font-size: .95rem; }}
.controles label {{ display: inline-flex; align-items: center; gap: 6px; }}
.controles input[type=range] {{ width: min(260px, 60vw); }}
.mapa .atenuado {{ opacity: 0.25; }}
.mapa .oculto {{ display: none; }}
"""


# ----------------------------------------------------------------------------
# carga y validación
# ----------------------------------------------------------------------------


class ErrorMapa(Exception):
    pass


def cargar_mapa(ruta: Path) -> dict:
    if not ruta.exists():
        raise ErrorMapa(f"no existe {ruta.relative_to(RAIZ)}")
    with ruta.open(encoding="utf-8") as f:
        datos = yaml.safe_load(f) or {}
    for clave in ("clases", "conceptos", "unidades"):
        datos.setdefault(clave, [])
        if not isinstance(datos[clave], list):
            raise ErrorMapa(f"'{clave}' tiene que ser una lista")
    datos.setdefault("titulo", "Sistemas de Coordenadas — mapa de conceptos")
    datos.setdefault("pregunta_guia", "")
    return datos


def prefijos_apunte_existentes() -> dict[str, Path]:
    """{'07': Path('.../07-bloque-rotaciones.tex'), ...}"""
    res: dict[str, Path] = {}
    if CONTENIDO_APUNTE.is_dir():
        for p in sorted(CONTENIDO_APUNTE.glob("*.tex")):
            m = re.match(r"(\d{2})-", p.name)
            if m:
                res[m.group(1)] = p
    return res


def validar(datos: dict) -> list[str]:
    """Devuelve la lista de avisos; lanza ErrorMapa con todos los errores si hay alguno."""
    errores: list[str] = []
    avisos: list[str] = []
    prefijos = prefijos_apunte_existentes()

    def ids_unicos(lista: list[dict], nombre: str) -> set[str]:
        vistos: set[str] = set()
        for i, item in enumerate(lista):
            if not isinstance(item, dict) or "id" not in item:
                errores.append(f"{nombre}[{i}] sin 'id'")
                continue
            iid = str(item["id"])
            item["id"] = iid
            if iid in vistos:
                errores.append(f"{nombre}: id duplicado '{iid}'")
            vistos.add(iid)
        return vistos

    ids_clases = ids_unicos(datos["clases"], "clases")
    ids_conceptos = ids_unicos(datos["conceptos"], "conceptos")
    ids_unidades = ids_unicos(datos["unidades"], "unidades")

    def chequear_apunte(lista, donde: str) -> None:
        for pref in lista or []:
            pref = str(pref)
            if pref not in prefijos:
                errores.append(f"{donde}: prefijo de apunte '{pref}' sin archivo en apunte/contenido/")

    for c in datos["clases"]:
        if "id" not in c:
            continue
        donde = f"clase {c['id']}"
        if c.get("estado") not in ESTADOS_CLASE:
            errores.append(f"{donde}: estado '{c.get('estado')}' no es uno de {ESTADOS_CLASE}")
        ficha = c.get("ficha")
        if ficha:
            if not (RAIZ / ficha).exists():
                avisos.append(f"{donde}: la ficha {ficha} todavía no existe")
        else:
            avisos.append(f"{donde}: sin 'ficha'")
        c["fechas_2026"] = [str(x) for x in (c.get("fechas_2026") or [])]
        if c.get("fecha_2025") is not None:
            c["fecha_2025"] = str(c["fecha_2025"])
        if c.get("fecha_2025_estimada") is not None:
            c["fecha_2025_estimada"] = str(c["fecha_2025_estimada"])
        if "apunte" in c:
            c["apunte"] = [str(x) for x in (c["apunte"] or [])]
            chequear_apunte(c["apunte"], donde)
        if c.get("validacion") not in VALIDACIONES:
            errores.append(f"{donde}: validacion '{c.get('validacion')}' no es uno de {VALIDACIONES}")
        if c.get("nivel") not in NIVELES:
            errores.append(f"{donde}: nivel '{c.get('nivel')}' no es uno de {NIVELES}")
        if not c.get("pregunta"):
            avisos.append(f"{donde}: sin 'pregunta'")

    for k in datos["conceptos"]:
        if "id" not in k:
            continue
        donde = f"concepto {k['id']}"
        k["clase"] = str(k.get("clase", ""))
        if k["clase"] not in ids_clases:
            errores.append(f"{donde}: clase '{k['clase']}' no existe")
        if k.get("unidad") is not None:
            k["unidad"] = str(k["unidad"])
            if k["unidad"] not in ids_unidades:
                errores.append(f"{donde}: unidad '{k['unidad']}' no existe")
        k["requiere"] = [str(x) for x in (k.get("requiere") or [])]
        for r in k["requiere"]:
            if r not in ids_conceptos:
                errores.append(f"{donde}: requiere '{r}' que no es un concepto")
            elif r == k["id"]:
                errores.append(f"{donde}: se requiere a sí mismo")
        k["apunte"] = [str(x) for x in (k.get("apunte") or [])]
        chequear_apunte(k["apunte"], donde)
        if not k.get("hecho_geometrico"):
            avisos.append(f"{donde}: sin 'hecho_geometrico'")
        if not k.get("nombre"):
            errores.append(f"{donde}: sin 'nombre'")

    for u in datos["unidades"]:
        if "id" not in u:
            continue
        donde = f"unidad {u['id']}"
        estado = u.get("estado")
        if estado not in ESTADOS_UNIDAD:
            errores.append(f"{donde}: estado '{estado}' no es uno de {ESTADOS_UNIDAD}")
        archivo = u.get("archivo")
        if estado in ESTADOS_EXPORTABLES:
            if not archivo:
                errores.append(f"{donde}: sin 'archivo'")
            elif not (RAIZ / archivo).exists():
                errores.append(f"{donde}: archivo {archivo} no existe")
        else:
            avisos.append(f"{donde}: estado '{estado}', no se exporta")
        if u.get("nivel") not in NIVELES:
            errores.append(f"{donde}: nivel '{u.get('nivel')}' no es uno de {NIVELES}")
        u["clases"] = [str(x) for x in (u.get("clases") or [])]
        if not u["clases"]:
            errores.append(f"{donde}: sin 'clases'")
        for cid in u["clases"]:
            if cid not in ids_clases:
                errores.append(f"{donde}: clases incluye '{cid}', que no existe")
        for campo in ("pregunta", "gancho_agrimensura"):
            if not u.get(campo):
                avisos.append(f"{donde}: sin '{campo}'")

    if errores:
        raise ErrorMapa("\n".join(f"  - {e}" for e in errores))
    return avisos


# ----------------------------------------------------------------------------
# exportación WASM
# ----------------------------------------------------------------------------


MODULO_COMUN = RAIZ / "unidades" / "cb104.py"
MARCA_INLINE = "# cb104:inline"
_RE_IMPORT_INLINE = re.compile(r"^(?P<sangria>[ \t]*)import cb104 as lib[ \t]*" + re.escape(MARCA_INLINE) + r"[ \t]*$", re.MULTILINE)
_RE_IMPORT_CB104 = re.compile(r"^[ \t]*(?:import cb104\b|from cb104 import\b)", re.MULTILINE)


def embeber_modulo_comun(texto: str, archivo: str) -> tuple[str, bool]:
    """Reemplaza la línea `import cb104 as lib  # cb104:inline` por el módulo embebido como literal.

    El export WASM no lleva archivos vecinos: el notebook sólo puede usar `cb104.py` si el código viaja
    adentro de una celda. Devuelve (texto nuevo, True) si lo reemplazó, (texto, False) si no importa cb104.
    Si importa cb104 sin el marcador, lanza RuntimeError (en el navegador fallaría con ModuleNotFoundError).
    """
    m = _RE_IMPORT_INLINE.search(texto)
    if m is None:
        if _RE_IMPORT_CB104.search(texto):
            raise RuntimeError(
                f"{archivo}: importa cb104 sin la celda marcada. Para exportar a WASM la celda tiene que ser "
                "exactamente `import cb104 as lib  # cb104:inline` (una celda propia que devuelve `lib`); "
                "el build la reemplaza por una copia embebida del módulo. Ver tools/README.md, "
                "sección 'Módulo común y export WASM'."
            )
        return texto, False
    if not MODULO_COMUN.exists():
        raise RuntimeError(f"{archivo}: usa cb104 pero no existe {MODULO_COMUN.relative_to(RAIZ)}")
    fuente = MODULO_COMUN.read_text(encoding="utf-8")
    sangria = m.group("sangria")
    bloque = (
        f"{sangria}import types as _types\n"
        f'{sangria}lib = _types.ModuleType("cb104")\n'
        f'{sangria}exec(compile({fuente!r}, "cb104.py", "exec"), lib.__dict__)'
    )
    return texto[: m.start()] + bloque + texto[m.end():], True


def exportar_unidad(u: dict, out: Path) -> float:
    fuente = RAIZ / u["archivo"]
    texto = fuente.read_text(encoding="utf-8")
    if "# /// script" not in texto:
        raise RuntimeError(
            f"{u['archivo']}: falta la cabecera PEP 723 (`# /// script` ... `# ///` con `dependencies`). "
            "Sin ella Pyodide no instala numpy/plotly/matplotlib y el notebook falla en el navegador "
            "(ModuleNotFoundError). Ver tools/README.md, sección 'Molde de unidad'."
        )
    # copia generada con el módulo común embebido (si el notebook lo usa); el export se hace sobre la copia
    texto, embebido = embeber_modulo_comun(texto, u["archivo"])
    dir_build = out / "_build"
    dir_build.mkdir(parents=True, exist_ok=True)
    copia = dir_build / fuente.name
    copia.write_text(texto, encoding="utf-8")
    destino = out / "unidades" / u["id"]
    if destino.exists():
        shutil.rmtree(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # mismo intérprete del venv (equivale a `uv run marimo ...` sin anidar uv)
    cmd = [
        sys.executable, "-m", "marimo", "export", "html-wasm",
        "--mode", "run", "--no-show-code", "--force",
        "-o", str(destino), str(copia),
    ]
    print(f"  exportando {u['id']} ({u['archivo']}{', cb104 embebido' if embebido else ''}) ...", flush=True)
    t0 = time.perf_counter()
    r = subprocess.run(cmd, cwd=RAIZ, capture_output=True, text=True)
    dt = time.perf_counter() - t0
    if r.returncode != 0:
        print(r.stdout)
        print(r.stderr, file=sys.stderr)
        raise RuntimeError(f"marimo export falló para {u['id']} (código {r.returncode})")
    if not (destino / "index.html").exists():
        raise RuntimeError(f"marimo export no dejó {destino / 'index.html'}")
    print(f"  listo {u['id']} en {dt:.1f}s", flush=True)
    return dt


# ----------------------------------------------------------------------------
# fichas (markdown → html)
# ----------------------------------------------------------------------------

_RE_MATH = re.compile(r"(\$\$.+?\$\$|(?<!\\)\$(?!\s)[^$\n]+?(?<!\s)\$)", re.DOTALL)


def _proteger_math(texto: str) -> tuple[str, list[str]]:
    """Saca las fórmulas antes de pasar por markdown (si no, `_` y `*` se vuelven énfasis)."""
    guardadas: list[str] = []

    def _sub(m: re.Match) -> str:
        guardadas.append(m.group(0))
        return f"\u0000MATH{len(guardadas) - 1}\u0000"

    return _RE_MATH.sub(_sub, texto), guardadas


def _restaurar_math(htm: str, guardadas: list[str]) -> str:
    for i, g in enumerate(guardadas):
        htm = htm.replace(f"\u0000MATH{i}\u0000", html.escape(g, quote=False))
    return htm


def sin_front_matter(texto: str) -> str:
    """Quita el front-matter YAML (`---` ... `---` al inicio); si no hay, devuelve el texto tal cual."""
    if not texto.startswith("---\n"):
        return texto
    fin = texto.find("\n---\n", 4)
    if fin == -1:
        return texto
    return texto[fin + len("\n---\n"):]


def md_a_html(texto: str) -> str:
    protegido, guardadas = _proteger_math(texto)
    cuerpo = markdown.markdown(protegido, extensions=["tables", "fenced_code", "toc"])
    return _restaurar_math(cuerpo, guardadas)


def pagina(titulo: str, cuerpo: str, *, katex: bool = False, raiz_rel: str = "") -> str:
    cabeza_katex = ""
    if katex:
        cabeza_katex = f"""
  <link rel="stylesheet" href="{KATEX_CDN}/katex.min.css">
  <script defer src="{KATEX_CDN}/katex.min.js"></script>
  <script defer src="{KATEX_CDN}/contrib/auto-render.min.js"
    onload="renderMathInElement(document.body, {{delimiters: [
      {{left: '$$', right: '$$', display: true}},
      {{left: '$', right: '$', display: false}},
      {{left: '\\\\(', right: '\\\\)', display: false}},
      {{left: '\\\\[', right: '\\\\]', display: true}}], throwOnError: false}});"></script>"""
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titulo)}</title>
  <style>{CSS}</style>{cabeza_katex}
</head>
<body>
<main>
{cuerpo}
</main>
</body>
</html>
"""


def titulo_de_md(texto: str, defecto: str) -> str:
    m = re.search(r"^#\s+(.+)$", texto, re.MULTILINE)
    return m.group(1).strip() if m else defecto


def etiqueta(texto: str, color: str, *, solida: bool = False) -> str:
    clase = "etq solida" if solida else "etq"
    return f'<span class="{clase}" style="--c:{color}">{html.escape(texto)}</span>'


def etiquetas_clase(c: dict) -> str:
    """Procedencia (`estado`) y validación de una clase, como dos etiquetas."""
    color, _ = COLOR_ESTADO.get(c.get("estado"), (RUST, "#eee"))
    proc = ETIQUETA_ESTADO.get(c.get("estado"), c.get("estado", ""))
    val = ETIQUETA_VALIDACION.get(c.get("validacion"), c.get("validacion", ""))
    color_val = TEAL if c.get("validacion") == "validado-catedra" else "#777"
    return etiqueta(f"procedencia: {proc}", color, solida=True) + etiqueta(val, color_val)


VOLVER = '<p class="volver"><a href="../index.html">← hilo conductor</a><a href="../mapa.html">mapa</a></p>'


def generar_fichas(datos: dict, out: Path) -> dict[str, str]:
    """Convierte las fichas. Devuelve {id_clase: 'clases/<id>.html'} para las que existen."""
    destino = out / "clases"
    destino.mkdir(parents=True, exist_ok=True)
    generadas: dict[str, str] = {}
    usados: set[Path] = set()
    for c in datos["clases"]:
        ficha = c.get("ficha")
        if not ficha:
            continue
        src = RAIZ / ficha
        if not src.exists():
            continue
        texto = sin_front_matter(src.read_text(encoding="utf-8"))
        titulo = titulo_de_md(texto, f"Clase {c['id']} — {c.get('titulo', '')}")
        cuerpo = (
            f'{VOLVER}\n<p class="etqs ficha-etqs">{etiquetas_clase(c)}</p>\n'
            f'<div class="ficha">\n{md_a_html(texto)}\n</div>'
        )
        (destino / f"{c['id']}.html").write_text(pagina(titulo, cuerpo, katex=True), encoding="utf-8")
        generadas[c["id"]] = f"clases/{c['id']}.html"
        usados.add(src.resolve())
    # fichas sueltas no referidas por el yaml (sin README ni _borradores)
    if DIR_CLASES.is_dir():
        for src in sorted(DIR_CLASES.glob("*.md")):
            if src.resolve() in usados or src.stem.isupper() or src.name.startswith("_"):
                continue  # README, PLANTILLA y _borradores no son fichas
            if False:
                continue
            texto = sin_front_matter(src.read_text(encoding="utf-8"))
            titulo = titulo_de_md(texto, src.stem)
            cuerpo = f'{VOLVER}\n<div class="ficha">\n{md_a_html(texto)}\n</div>'
            (destino / f"{src.stem}.html").write_text(pagina(titulo, cuerpo, katex=True), encoding="utf-8")
    return generadas


# ----------------------------------------------------------------------------
# mapa de conceptos → SVG
# ----------------------------------------------------------------------------

ANCHO_COL = 210          # ancho de cada columna (clase)
ANCHO_NODO_MIN = 120     # la caja se ajusta al texto entre estos límites
ANCHO_NODO_MAX = ANCHO_COL - 22
PX_POR_CARACTER = 6.4    # estimación para 12 px de fuente sans
ALTO_LINEA = 15
RELLENO_NODO = 10        # arriba + abajo
SEP_FILA = 18            # espacio entre cajas de una misma columna
MARGEN_X = 20
MARGEN_SUP = 12
MARGEN_INF = 20
MAX_CHARS_NODO = 22
MAX_LINEAS_NODO = 3
MAX_CHARS_CAB = 28
MAX_LINEAS_CAB = 4


def _partir_nombre(nombre: str, maximo: int = MAX_CHARS_NODO, max_lineas: int = MAX_LINEAS_NODO) -> list[str]:
    """Parte el texto en hasta `max_lineas` líneas de ~`maximo` caracteres; si no entra, recorta con '…'."""
    nombre = " ".join(nombre.split())
    if len(nombre) <= maximo:
        return [nombre]
    lineas: list[str] = []
    actual = ""
    for p in nombre.split():
        cand = (actual + " " + p).strip()
        if len(cand) > maximo and actual:
            lineas.append(actual)
            actual = p
        else:
            actual = cand
    if actual:
        lineas.append(actual)
    if len(lineas) > max_lineas:
        resto = " ".join(lineas[max_lineas - 1:])
        lineas = lineas[: max_lineas - 1] + [resto]
        if len(lineas[-1]) > maximo:
            lineas[-1] = lineas[-1][: maximo - 1].rstrip() + "…"
    return lineas


def _partir_titulo_col(titulo: str) -> list[str]:
    return _partir_nombre(titulo, MAX_CHARS_CAB, MAX_LINEAS_CAB)


def _ancho_nodo(lineas: list[str]) -> float:
    ancho = max(len(ln) for ln in lineas) * PX_POR_CARACTER + 16
    return max(ANCHO_NODO_MIN, min(ANCHO_NODO_MAX, ancho))


def svg_mapa(datos: dict, fichas: dict[str, str], exportadas: set[str]) -> str:
    clases = datos["clases"]
    conceptos = datos["conceptos"]
    por_clase: dict[str, list[dict]] = {c["id"]: [] for c in clases}
    for k in conceptos:
        por_clase[k["clase"]].append(k)

    # cabeceras: su alto depende de la que más líneas ocupe
    cab_lineas = {c["id"]: _partir_titulo_col(c.get("titulo", "")) for c in clases}
    lineas_cab_max = max([len(v) for v in cab_lineas.values()] + [1])
    alto_cabecera = MARGEN_SUP + 18 + lineas_cab_max * ALTO_LINEA + 14

    # posiciones: cada columna apila sus nodos; el alto de cada caja depende de sus líneas
    pos: dict[str, tuple[float, float, float, float, int, list[str]]] = {}  # id -> (x, y, w, h, col, lineas)
    alto_col_max = 0.0
    for col, c in enumerate(clases):
        x0 = MARGEN_X + col * ANCHO_COL
        y = float(alto_cabecera)
        for k in por_clase[c["id"]]:
            lineas = _partir_nombre(k.get("nombre", k["id"]))
            w = _ancho_nodo(lineas)
            h = RELLENO_NODO + len(lineas) * ALTO_LINEA + 4
            x = x0 + (ANCHO_COL - w) / 2
            pos[k["id"]] = (x, y, w, h, col, lineas)
            y += h + SEP_FILA
        alto_col_max = max(alto_col_max, y)
    ancho = MARGEN_X * 2 + ANCHO_COL * max(len(clases), 1)
    alto = int(alto_col_max - SEP_FILA + MARGEN_INF)
    estado_clase = {c["id"]: c.get("estado", "no-dictada") for c in clases}
    # atributos para los controles de mapa.html: orden (1..n) y nivel de la clase de cada nodo
    orden_clase = {c["id"]: i + 1 for i, c in enumerate(clases)}
    nivel_clase = {c["id"]: c.get("nivel", "troncal") for c in clases}
    clase_de = {k["id"]: k["clase"] for k in conceptos}

    def attrs(cid: str) -> str:
        return f'data-clase="{html.escape(cid)}" data-orden="{orden_clase.get(cid, 0)}" data-nivel="{html.escape(nivel_clase.get(cid, "troncal"))}"'

    partes: list[str] = []
    partes.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" '
        f'role="img" aria-label="Mapa de conceptos" font-family="-apple-system, BlinkMacSystemFont, Segoe UI, Helvetica, Arial, sans-serif">'
    )
    partes.append(
        '<defs><marker id="flecha" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        '<path d="M 0 0 L 10 5 L 0 10 z" fill="#777"/></marker></defs>'
    )
    # separadores y cabeceras de columna
    for col, c in enumerate(clases):
        x0 = MARGEN_X + col * ANCHO_COL
        color, _ = COLOR_ESTADO.get(c.get("estado"), (RUST, "#eee"))
        if col > 0:
            partes.append(f'<line x1="{x0}" y1="8" x2="{x0}" y2="{alto - 8}" stroke="#eee" stroke-width="1"/>')
        cx = x0 + ANCHO_COL / 2
        partes.append(f'<g class="cabecera" {attrs(c["id"])}>')
        partes.append(f'<text x="{cx}" y="{MARGEN_SUP + 12}" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">Clase {html.escape(c["id"])}</text>')
        for i, ln in enumerate(cab_lineas[c["id"]]):
            partes.append(f'<text x="{cx}" y="{MARGEN_SUP + 30 + i * ALTO_LINEA}" text-anchor="middle" font-size="12" fill="#444">{html.escape(ln)}</text>')
        partes.append("</g>")

    # aristas (requerido → concepto)
    for k in conceptos:
        if k["id"] not in pos:
            continue
        x2, y2, w2, h2, c2, _ = pos[k["id"]]
        for r in k["requiere"]:
            if r not in pos:
                continue
            x1, y1, w1, h1, c1, _ = pos[r]
            if c1 < c2:
                ax, ay = x1 + w1, y1 + h1 / 2
                bx, by = x2, y2 + h2 / 2
                dx = (bx - ax) * 0.6
                d = f"M {ax:.1f} {ay:.1f} C {ax + dx:.1f} {ay:.1f}, {bx - dx:.1f} {by:.1f}, {bx:.1f} {by:.1f}"
            elif c1 > c2:
                ax, ay = x1, y1 + h1 / 2
                bx, by = x2 + w2, y2 + h2 / 2
                dx = (ax - bx) * 0.6
                d = f"M {ax:.1f} {ay:.1f} C {ax - dx:.1f} {ay - 20:.1f}, {bx + dx:.1f} {by - 20:.1f}, {bx:.1f} {by:.1f}"
            else:
                # misma columna: salir por el costado derecho y volver a entrar
                arriba = y1 < y2
                ax, ay = x1 + w1, y1 + (h1 - 8 if arriba else 8)
                bx, by = x2 + w2, y2 + (8 if arriba else h2 - 8)
                d = f"M {ax:.1f} {ay:.1f} C {ax + 28:.1f} {ay:.1f}, {bx + 28:.1f} {by:.1f}, {bx:.1f} {by:.1f}"
            partes.append(
                f'<path class="arista" data-de="{html.escape(r)}" data-a="{html.escape(k["id"])}" '
                f'data-orden-max="{max(orden_clase.get(clase_de.get(r, ""), 0), orden_clase.get(k["clase"], 0))}" '
                f'data-niveles="{html.escape(nivel_clase.get(clase_de.get(r, ""), "troncal"))} {html.escape(nivel_clase.get(k["clase"], "troncal"))}" '
                f'd="{d}" fill="none" stroke="#777" stroke-width="1.3" marker-end="url(#flecha)" opacity="0.5"/>'
            )

    # nodos
    for k in conceptos:
        if k["id"] not in pos:
            continue
        x, y, w, h, _, lineas = pos[k["id"]]
        color, fondo = COLOR_ESTADO.get(estado_clase.get(k["clase"]), (RUST, "#eee"))
        if k.get("unidad") and k["unidad"] in exportadas:
            href = f"unidades/{k['unidad']}/index.html"
        elif k["clase"] in fichas:
            href = fichas[k["clase"]]
        else:
            href = None
        hover = k.get("hecho_geometrico") or k.get("nombre", "")
        if k.get("que_se_conserva"):
            hover += f" — se conserva: {k['que_se_conserva']}"
        # texto centrado verticalmente: la primera línea arranca según la cantidad de líneas
        y_texto0 = y + h / 2 - (len(lineas) - 1) * ALTO_LINEA / 2 + 4
        tam = "12.5" if len(lineas) == 1 else "12"
        texto = "".join(
            f'<text x="{x + w / 2:.1f}" y="{y_texto0 + i * ALTO_LINEA:.1f}" text-anchor="middle" font-size="{tam}" fill="#222">{html.escape(ln)}</text>'
            for i, ln in enumerate(lineas)
        )
        nodo = (
            f'<title>{html.escape(hover)}</title>'
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="7" ry="7" fill="{fondo}" stroke="{color}" stroke-width="2"/>'
            + texto
        )
        a = f'class="nodo" data-id="{html.escape(k["id"])}" {attrs(k["clase"])}'
        if href:
            partes.append(f'<a href="{html.escape(href)}" style="cursor:pointer" {a}>{nodo}</a>')
        else:
            partes.append(f"<g {a}>{nodo}</g>")
    partes.append("</svg>")
    return "\n".join(partes)


# ----------------------------------------------------------------------------
# índice
# ----------------------------------------------------------------------------


def titulos_secciones_apunte() -> dict[str, str]:
    """{'07': 'Bloque geométrico: fundamentos y rotaciones', ...} a partir del primer \\section{} de cada .tex."""
    res: dict[str, str] = {}
    for pref, p in prefijos_apunte_existentes().items():
        try:
            texto = p.read_text(encoding="utf-8")
        except OSError:
            continue
        m = re.search(r"\\(?:section|chapter)\*?\{([^}]*)\}", texto)
        res[pref] = m.group(1).strip() if m else p.stem
    return res


def hoy() -> _dt.date:
    return _dt.date.today()


def clase_dictada(c: dict, fecha: _dt.date) -> bool:
    """True si alguna `fechas_2026` de la clase es ≤ `fecha`."""
    for f in c.get("fechas_2026") or []:
        try:
            if _dt.date.fromisoformat(str(f)) <= fecha:
                return True
        except ValueError:
            continue
    return False


def ultima_clase_dictada(clases: list[dict], fecha: _dt.date) -> dict | None:
    """La clase con la fecha dictada más reciente (≤ fecha); empate → la de mayor orden en la cursada."""
    mejor: tuple[_dt.date, int] | None = None
    res = None
    for i, c in enumerate(clases):
        for f in c.get("fechas_2026") or []:
            try:
                d = _dt.date.fromisoformat(str(f))
            except ValueError:
                continue
            if d <= fecha and (mejor is None or (d, i) > mejor):
                mejor, res = (d, i), c
    return res


def enlace_apunte(pref: str, titulos: dict[str, str], hay_pdf: bool) -> str:
    """Sección del apunte como enlace `apunte.pdf#nameddest=cap:NN` (los \\label{cap:NN} viven en el .tex)."""
    tit = titulos.get(pref, pref)
    texto = f"apunte §{html.escape(pref)}: {html.escape(tit)}"
    if hay_pdf:
        return f'<span><a href="apunte.pdf#nameddest=cap:{html.escape(pref)}" title="apunte, sección {html.escape(pref)}">{texto}</a></span>'
    return f'<span class="pend">{texto}</span>'


def prefijos_apunte_de_clase(c: dict, conceptos_por_clase: dict[str, list[dict]]) -> list[str]:
    """Los `apunte` declarados en la clase, o la unión de los de sus conceptos."""
    prefs: list[str] = list(c.get("apunte") or [])
    if not prefs:
        for k in conceptos_por_clase.get(c["id"], []):
            for pr in k["apunte"]:
                if pr not in prefs:
                    prefs.append(pr)
    return sorted(prefs)


JS_MAPA = r"""
(function () {
  var svg = document.querySelector('.mapa svg');
  if (!svg) return;
  var ruta = document.getElementById('ruta');
  var hasta = document.getElementById('hasta');
  var rotulo = document.getElementById('hasta-rotulo');
  var ids = JSON.parse(document.getElementById('clases-orden').textContent);
  var nodos = svg.querySelectorAll('.nodo, .cabecera');
  var aristas = svg.querySelectorAll('.arista');
  function aplicar() {
    var soloTroncal = ruta.value === 'troncal';
    var n = parseInt(hasta.value, 10);
    rotulo.textContent = 'hasta la clase ' + ids[n - 1];
    nodos.forEach(function (el) {
      var oculto = soloTroncal && el.getAttribute('data-nivel') !== 'troncal';
      var aten = parseInt(el.getAttribute('data-orden'), 10) > n;
      el.classList.toggle('oculto', oculto);
      el.classList.toggle('atenuado', !oculto && aten);
    });
    aristas.forEach(function (el) {
      var niveles = el.getAttribute('data-niveles').split(' ');
      var oculto = soloTroncal && (niveles[0] !== 'troncal' || niveles[1] !== 'troncal');
      var aten = parseInt(el.getAttribute('data-orden-max'), 10) > n;
      el.classList.toggle('oculto', oculto);
      el.classList.toggle('atenuado', !oculto && aten);
    });
  }
  ruta.addEventListener('change', aplicar);
  hasta.addEventListener('input', aplicar);
  aplicar();
})();
"""


def generar_mapa(datos: dict, fichas: dict[str, str], exportadas: set[str], hay_pdf: bool, out: Path) -> None:
    """site/mapa.html: el SVG de conceptos con filtro de ruta y deslizador "hasta la clase N", y la lista de clases."""
    unidades = {u["id"]: u for u in datos["unidades"]}
    titulos_apunte = titulos_secciones_apunte()
    conceptos_por_clase: dict[str, list[dict]] = {c["id"]: [] for c in datos["clases"]}
    for k in datos["conceptos"]:
        conceptos_por_clase[k["clase"]].append(k)
    clases = datos["clases"]
    ultima = ultima_clase_dictada(clases, hoy())
    n_default = (clases.index(ultima) + 1) if ultima else len(clases)

    partes: list[str] = []
    partes.append('<p class="volver"><a href="index.html">← hilo conductor</a></p>')
    partes.append(f"<h1>{html.escape(TITULO_MAPA)}</h1>")
    if datos.get("pregunta_guia"):
        partes.append(f'<p class="guia">Pregunta guía: {html.escape(datos["pregunta_guia"])}</p>')

    partes.append("<h2>Mapa de conceptos</h2>")
    opciones = "".join(
        f'<option value="{v}">{t}</option>' for v, t in (("todo", "todo"), ("troncal", "sólo troncal"))
    )
    partes.append(
        '<div class="controles">'
        f'<label>Ruta: <select id="ruta">{opciones}</select></label>'
        f'<label><span id="hasta-rotulo">hasta la clase {html.escape(ultima["id"] if ultima else clases[-1]["id"])}</span> '
        f'<input type="range" id="hasta" min="1" max="{len(clases)}" value="{n_default}" step="1"></label>'
        "</div>"
    )
    partes.append(f'<script id="clases-orden" type="application/json">{json.dumps([c["id"] for c in clases])}</script>')
    partes.append('<div class="mapa">' + svg_mapa(datos, fichas, exportadas) + "</div>")
    leyenda = "".join(
        f'<span style="--c:{COLOR_ESTADO[e][0]};--f:{COLOR_ESTADO[e][1]}">{ETIQUETA_ESTADO[e]}</span>' for e in ESTADOS_CLASE
    )
    partes.append(f'<p class="leyenda">{leyenda}<span style="--c:#777;--f:#fff">flecha: lo que un concepto requiere → el concepto</span></p>')
    partes.append('<p class="guia">Cada nodo lleva a la unidad interactiva si existe, si no a la ficha de la clase. Pasando el mouse se ve el hecho geométrico. '
                  "El filtro de ruta esconde las clases complementarias y avanzadas; el deslizador atenúa lo que viene después de la clase elegida (por default, la última dictada).</p>")
    partes.append(f"<script>{JS_MAPA}</script>")

    partes.append(f"<h2>Clases ({len(clases)})</h2>")
    partes.append('<ul class="clases">')
    for c in clases:
        color, _ = COLOR_ESTADO.get(c.get("estado"), (RUST, "#eee"))
        fechas = []
        if c.get("fecha_2025"):
            fechas.append(f"2025: {html.escape(c['fecha_2025'])}")
        elif c.get("fecha_2025_estimada"):
            fechas.append(f"2025: {html.escape(c['fecha_2025_estimada'])} (est.)")
        if c.get("fechas_2026"):
            fechas.append("2026: " + ", ".join(html.escape(f) for f in c["fechas_2026"]))
        else:
            fechas.append("2026: sin fecha")
        links: list[str] = []
        if c["id"] in fichas:
            links.append(f'<span><a href="{fichas[c["id"]]}">ficha</a></span>')
        else:
            links.append('<span class="pend">ficha pendiente</span>')
        ids_u: list[str] = []
        for k in conceptos_por_clase[c["id"]]:
            if k.get("unidad") and k["unidad"] not in ids_u:
                ids_u.append(k["unidad"])
        for uid in ids_u:
            u = unidades[uid]
            if uid in exportadas:
                links.append(f'<span><a href="unidades/{html.escape(uid)}/index.html">unidad: {html.escape(u.get("titulo", uid))}</a></span>')
            else:
                nota = f" — {html.escape(u['nota'])}" if u.get("nota") else ""
                links.append(f'<span class="pend">unidad: {html.escape(u.get("titulo", uid))} ({ETIQUETA_ESTADO_UNIDAD.get(u.get("estado"), u.get("estado", ""))}{nota})</span>')
        for pr in prefijos_apunte_de_clase(c, conceptos_por_clase):
            links.append(enlace_apunte(pr, titulos_apunte, hay_pdf))
        partes.append(
            f'<li class="clase" style="--c:{color}">'
            f'<div class="cab"><span class="id">Clase {html.escape(c["id"])}</span>'
            f'<span class="tit">{html.escape(c.get("titulo", ""))}</span>'
            f'{etiquetas_clase(c)}'
            f'{etiqueta(c.get("nivel", ""), "#777")}</div>'
            f'<div class="fechas">{" · ".join(fechas)}</div>'
            f'<div class="links">{"".join(links)}</div>'
            "</li>"
        )
    partes.append("</ul>")

    partes.append("<h2>Apunte</h2>")
    if hay_pdf:
        partes.append('<p><a href="apunte.pdf">Apunte de Sistemas de Coordenadas (PDF)</a> — anexo de demostraciones y guías resueltas.</p>')
    else:
        partes.append('<p class="pend">El PDF del apunte no está compilado en este build.</p>')
    partes.append(PIE)
    (out / "mapa.html").write_text(pagina(TITULO_MAPA, "\n".join(partes)), encoding="utf-8")


PIE = ('<p class="pie">Material de estudio de CB104 Sistemas de Coordenadas (Agrimensura, FIUBA), hecho por Gustavo Varela como alumno. '
       "Las unidades interactivas corren en el navegador (marimo + Pyodide); la primera carga tarda unos segundos.</p>")


def estado_unidad(clases_est: list[dict], exportada: bool, fecha: _dt.date) -> str:
    if exportada:
        return "lista"
    if any(clase_dictada(c, fecha) for c in clases_est):
        return "en-clase"
    return "todavia-no"


def generar_indice(datos: dict, fichas: dict[str, str], exportadas: set[str], hay_pdf: bool, out: Path) -> None:
    """site/index.html: el hilo conductor. Tres entradas y una entrada por unidad (más "Lo que viene")."""
    titulos_apunte = titulos_secciones_apunte()
    clases = datos["clases"]
    por_id = {c["id"]: c for c in clases}
    conceptos_por_clase: dict[str, list[dict]] = {c["id"]: [] for c in clases}
    for k in datos["conceptos"]:
        conceptos_por_clase[k["clase"]].append(k)
    fecha = hoy()

    # unidades de la portada: una por unidad de unidades.yaml, en ese orden; al final, las clases sin unidad
    unidades_portada: list[dict] = []
    cubiertas: set[str] = set()
    for u in datos["unidades"]:
        cl = [por_id[cid] for cid in u["clases"] if cid in por_id]
        cubiertas.update(c["id"] for c in cl)
        unidades_portada.append({
            "unidad": u, "titulo": u.get("titulo", u["id"]), "clases": cl,
            "pregunta": u.get("pregunta", ""), "gancho": u.get("gancho_agrimensura", ""), "nivel": u.get("nivel", ""),
            "estado": estado_unidad(cl, u["id"] in exportadas, fecha),
        })
    sin_unidad = [c for c in clases if c["id"] not in cubiertas]
    if sin_unidad:
        unidades_portada.append({
            "unidad": None, "titulo": "Lo que viene", "clases": sin_unidad,
            "pregunta": "", "gancho": "Clases del esqueleto del profesor que todavía no se dictaron en 2026; no se anticipan como contenido de la cátedra.",
            "nivel": "", "estado": estado_unidad(sin_unidad, False, fecha),
        })

    # entrada "seguir la cursada": la unidad de la última clase dictada
    ultima = ultima_clase_dictada(clases, fecha)
    n_seguir = 0
    if ultima:
        for i, e in enumerate(unidades_portada, start=0):
            if i > 0 and any(c["id"] == ultima["id"] for c in e["clases"]):
                n_seguir = i   # la unidad 0 cubre 01, 04 y 09 como fundamentos: no es "seguir la cursada"
                break

    partes: list[str] = []
    partes.append(f"<h1>{html.escape(TITULO_CAMINO)}</h1>")
    if datos.get("pregunta_guia"):
        partes.append(f'<p class="guia">Pregunta guía: {html.escape(datos["pregunta_guia"])}</p>')
    seguir_sub = f"unidad {n_seguir}, clase {html.escape(ultima['id'])} ({html.escape(max(ultima['fechas_2026']))})" if ultima else "todavía no se dictó ninguna clase"
    partes.append(
        '<nav class="entradas">'
        f'<a class="entrada" href="#unidad-0"><b>Empezar</b><small>unidad 0: {html.escape(unidades_portada[0]["titulo"])}</small></a>'
        f'<a class="entrada" href="#unidad-{n_seguir}"><b>Seguir la cursada</b><small>{seguir_sub}</small></a>'
        '<a class="entrada" href="mapa.html"><b>Repasar</b><small>el mapa de conceptos completo</small></a>'
        "</nav>"
    )

    partes.append(f"<h2>Recorrido paso a paso ({len(unidades_portada)} unidades interactivas)</h2>")
    partes.append('<ol class="hilo">')
    for i, e in enumerate(unidades_portada, start=0):
        rot, color = ETIQUETA_UNIDAD[e["estado"]]
        num = "Unidad 0 — Fundamentos" if i == 0 else f"Unidad {i}"
        cab = [f'<span class="num">{num}</span>', f'<span class="tit">{html.escape(e["titulo"])}</span>',
               etiqueta(rot, color, solida=True)]
        if e["nivel"]:
            cab.append(etiqueta(e["nivel"], "#777"))
        cuerpo = [f'<div class="cab">{"".join(cab)}</div>']
        if e["pregunta"]:
            cuerpo.append(f'<p class="pregunta">{html.escape(e["pregunta"])}</p>')
        if e["gancho"]:
            cuerpo.append(f'<p class="gancho">{html.escape(e["gancho"])}</p>')
        # clases que cubre, con procedencia y validación
        filas = []
        for c in e["clases"]:
            ficha = f'<a href="{fichas[c["id"]]}">ficha</a>' if c["id"] in fichas else '<span class="pend">ficha pendiente</span>'
            filas.append(f'<li><span class="cid">Clase {html.escape(c["id"])}</span><span>{html.escape(c.get("titulo", ""))}</span>'
                         f'{etiquetas_clase(c)}<span>{ficha}</span></li>')
        cuerpo.append(f'<ul class="sus-clases">{"".join(filas)}</ul>')
        # enlaces: unidad, apunte
        links: list[str] = []
        u = e["unidad"]
        if u is not None:
            if u["id"] in exportadas:
                links.append(f'<span><a href="unidades/{html.escape(u["id"])}/index.html">abrir la unidad interactiva</a></span>')
            else:
                nota = f" — {html.escape(u['nota'])}" if u.get("nota") else ""
                links.append(f'<span class="pend">unidad {ETIQUETA_ESTADO_UNIDAD.get(u.get("estado"), u.get("estado", ""))}{nota}</span>')
        prefs: list[str] = []
        for c in e["clases"]:
            for pr in prefijos_apunte_de_clase(c, conceptos_por_clase):
                if pr not in prefs:
                    prefs.append(pr)
        for pr in sorted(prefs):
            links.append(enlace_apunte(pr, titulos_apunte, hay_pdf))
        if links:
            cuerpo.append(f'<div class="links">{"".join(links)}</div>')
        partes.append(f'<li class="unidad" id="unidad-{i}" style="--c:{color}">{"".join(cuerpo)}</li>')
    partes.append("</ol>")

    partes.append("<h2>Apunte y mapa</h2>")
    if hay_pdf:
        partes.append('<p><a href="apunte.pdf">Apunte de Sistemas de Coordenadas (PDF)</a> — anexo de demostraciones y guías resueltas. '
                      '<a href="mapa.html">Mapa de conceptos</a> — todos los nodos y lo que requiere cada uno.</p>')
    else:
        partes.append('<p class="pend">El PDF del apunte no está compilado en este build.</p><p><a href="mapa.html">Mapa de conceptos</a>.</p>')
    partes.append(PIE)
    (out / "index.html").write_text(pagina(TITULO_CAMINO, "\n".join(partes)), encoding="utf-8")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------


def main() -> int:
    ap = argparse.ArgumentParser(description="Genera el sitio estático en site/ a partir de mapa/mapa.yaml.")
    ap.add_argument("--skip-wasm", action="store_true", help="no exporta las unidades marimo (deja lo que ya haya en site/unidades/)")
    ap.add_argument("--only", metavar="UNIDAD_ID", help="exporta sólo esa unidad (el resto del sitio se genera igual)")
    ap.add_argument("--out", default="site", help="directorio de salida (default: site, relativo a la raíz del repo)")
    ap.add_argument("--mapa", default=str(MAPA), help=argparse.SUPPRESS)
    args = ap.parse_args()
    sys.stdout.reconfigure(line_buffering=True)

    out = Path(args.out)
    if not out.is_absolute():
        out = RAIZ / out
    out.mkdir(parents=True, exist_ok=True)

    t_total = time.perf_counter()
    print(f"== mapa: {Path(args.mapa).relative_to(RAIZ) if Path(args.mapa).is_relative_to(RAIZ) else args.mapa}")
    try:
        datos = cargar_mapa(Path(args.mapa))
        avisos = validar(datos)
    except ErrorMapa as e:
        print(f"ERROR en mapa.yaml:\n{e}", file=sys.stderr)
        return 1
    for a in avisos:
        print(f"  aviso: {a}")
    print(f"  {len(datos['clases'])} clases, {len(datos['conceptos'])} conceptos, {len(datos['unidades'])} unidades")

    # unidades
    exportables = [u for u in datos["unidades"] if u.get("estado") in ESTADOS_EXPORTABLES]
    if args.only:
        if args.only not in {u["id"] for u in datos["unidades"]}:
            print(f"ERROR: --only {args.only}: no es una unidad del mapa", file=sys.stderr)
            return 1
        exportables = [u for u in exportables if u["id"] == args.only]
        if not exportables:
            print(f"ERROR: --only {args.only}: la unidad no tiene estado exportable ({ESTADOS_EXPORTABLES})", file=sys.stderr)
            return 1
    print("== unidades")
    tiempos: dict[str, float] = {}
    if args.skip_wasm:
        print("  --skip-wasm: no se exporta nada")
    else:
        for u in exportables:
            try:
                tiempos[u["id"]] = exportar_unidad(u, out)
            except RuntimeError as e:
                print(f"ERROR: {e}", file=sys.stderr)
                return 1
    # lo que efectivamente hay en site/unidades (incluye exports previos si --skip-wasm/--only)
    exportadas = {
        u["id"] for u in datos["unidades"] if (out / "unidades" / u["id"] / "index.html").exists()
    }
    print(f"  unidades disponibles en {out.name}/unidades: {sorted(exportadas) or 'ninguna'}")

    print("== fichas")
    fichas = generar_fichas(datos, out)
    print(f"  {len(fichas)} fichas generadas: {sorted(fichas) or 'ninguna'}")

    print("== apunte")
    hay_pdf = PDF_APUNTE.exists()
    if hay_pdf:
        shutil.copy2(PDF_APUNTE, out / "apunte.pdf")
        print(f"  copiado apunte.pdf ({PDF_APUNTE.stat().st_size / 1e6:.1f} MB)")
    else:
        print(f"  aviso: no existe {PDF_APUNTE.relative_to(RAIZ)}; el índice no linkea el PDF")

    print("== portada y mapa")
    generar_indice(datos, fichas, exportadas, hay_pdf, out)
    generar_mapa(datos, fichas, exportadas, hay_pdf, out)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"  {out / 'index.html'}")
    print(f"  {out / 'mapa.html'}")

    if tiempos:
        print("== tiempos de export WASM")
        for k, v in tiempos.items():
            print(f"  {k}: {v:.1f}s")
    print(f"== listo en {time.perf_counter() - t_total:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
