#!/usr/bin/env python3
"""Genera el sitio estático `site/` de Sistemas de Coordenadas (CB104).

Entradas (relativas a la raíz del repo):
  mapa/mapa.yaml                        mapa de conceptos (esquema en mapa/ESQUEMA.md)
  clases/*.md                           fichas por capítulo (el id de la ficha es interno; el rótulo usa la numeración del PDF)
  unidades/*.py                         notebooks marimo
  apunte/Apunte_Sistemas_de_Coordenadas.pdf
  apunte/Apunte_Sistemas_de_Coordenadas.tex y los contenido/*.tex que incluye: sólo para validar las claves
                                        `apunte:` (cada clave X es un \\label{cap:X}: "rotaciones", "rot3d", …) y leer su título

Salida:
  site/index.html                       portada = el hilo conductor: entradas (Empezar / Seguir el programa / Repasar / Autoevaluación)
                                        y una entrada por unidad (pregunta, gancho, estado, capítulos, enlaces),
                                        más la última unidad "Lo que viene" con los capítulos sin unidad
  site/mapa.html                        mapa de conceptos (SVG inline) con filtro de ruta y "hasta el capítulo N",
                                        y la lista de capítulos
  site/capitulos/<id>.html              fichas (markdown → html, KaTeX desde CDN; apunte, unidades y animaciones desde el frontmatter)
  site/unidades/<id>/index.html         notebooks exportados a WASM (marimo export html-wasm) desde la copia
  site/_build/<archivo>.py              generada con unidades/cb104.py embebido en la celda `# cb104:inline`
  site/apunte.pdf                       copia del apunte
  site/cad/index.html, site/cad/dxf/    laboratorio CAD: página desde cad/index.md (las secciones «## Capítulo N»
                                        llevan id="capN") y copia de cad/dxf/**/*.dxf (antes del menú, que la enlaza)
  site/menu.html, site/menu.pdf         piezas por capítulo para el aula (tools/menu.py, al final, antes de las menciones prohibidas)
  site/menu-por-capitulo.html           entradas, platos y postres por capítulo, A4 apaisado (tools/menu_por_capitulo/gen.py, después del menú)
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
MAESTRO_APUNTE = RAIZ / "apunte" / "Apunte_Sistemas_de_Coordenadas.tex"
DIR_CLASES = RAIZ / "clases"

ESTADOS_UNIDAD = ("piloto", "migrada", "legacy", "pendiente")
ESTADOS_EXPORTABLES = ("piloto", "migrada")
TITULO_CAMINO = "Sistemas de Coordenadas — Hilo conductor y lecciones interactivas"
TITULO_MAPA = "Sistemas de Coordenadas — mapa de conceptos"

# paleta del apunte
TEAL, RUST, GOLD = "#1b6f6a", "#b5532a", "#c9a227"
FONDO_NODO = "#e3f1f0"
# avance interno del programa (no se publica): fichas con capítulo desarrollado; "Seguir el programa" salta a la unidad siguiente
PROGRAMA_AVANCE = ["01", "02", "03", "03p", "04", "05", "06", "07", "08", "09"]
# Capítulo del PDF que corresponde a cada ficha (id de ficha -> rótulo): la ficha 03 cubre los capítulos 3 y 4,
# la 03p es el complemento C1 y de la 04 a la 14 el capítulo es el id más uno.
CAPITULO_DE_FICHA = {"01": "1", "02": "2", "03": "3 y 4", "03p": "C1", "04": "5", "05": "6", "06": "7", "07": "8",
                     "08": "9", "09": "10", "10": "11", "11": "12", "12": "13", "13": "14", "14": "15"}


def rotulo_ficha(cid: str) -> str:
    """«Capítulo 1», «Capítulos 3 y 4» o «Complemento C1» según la numeración del PDF."""
    n = CAPITULO_DE_FICHA.get(cid, cid)
    if n.startswith("C"):
        return f"Complemento {n}"
    return f"Capítulos {n}" if " y " in n else f"Capítulo {n}"


def rotulo_hasta(cid: str) -> str:
    """«hasta el capítulo 1», «hasta los capítulos 3 y 4», «hasta el complemento C1»."""
    r = rotulo_ficha(cid)
    return f"hasta {'los' if r.startswith('Capítulos') else 'el'} {r[0].lower()}{r[1:]}"


NIVELES = ("troncal", "complementario", "avanzado")
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
.capitulos {{ list-style: none; padding: 0; margin: 0; }}
.capitulo {{ border: 1px solid var(--linea); border-left: 5px solid var(--c); border-radius: 6px; background: #fff;
          padding: 10px 14px; margin: 0 0 10px; }}
.capitulo .cab {{ display: flex; flex-wrap: wrap; gap: 6px 12px; align-items: baseline; }}
.capitulo .id {{ font-weight: 700; color: var(--c); }}
.capitulo .tit {{ font-weight: 600; font-size: 1.05rem; }}
.links {{ display: flex; flex-wrap: wrap; gap: 6px; font-size: .92rem; margin: 6px 0 0; }}
.links span {{ display: inline-block; max-width: 100%; white-space: normal; overflow-wrap: anywhere; border: 1px solid var(--linea);
               border-radius: 10px; padding: 1px 9px; background: #f7f5ef; }}
.links span.pend {{ color: var(--gris); }}
.pend {{ color: var(--gris); }}
.topnav {{ display: flex; flex-wrap: wrap; gap: 6px 16px; padding: 10px 0 4px; font-size: .9rem; border-bottom: 1px solid var(--linea); }}
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
/* etiquetas (nivel) */
.etqs {{ display: flex; flex-wrap: wrap; gap: 6px; margin: 0; }}
.etq {{ display: inline-block; font-size: .78rem; line-height: 1.5; border-radius: 10px; padding: 1px 9px;
        border: 1.5px solid var(--c, var(--gris)); color: var(--c, var(--gris)); background: #fff; white-space: nowrap; }}
.etq.solida {{ color: #fff; background: var(--c, var(--gris)); }}
.ficha .vinculos {{ padding-left: 1.2em; }}
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
.unidad .sus-capitulos {{ list-style: none; padding: 0; margin: 6px 0 0; }}
.unidad .sus-capitulos li {{ display: flex; flex-wrap: wrap; gap: 4px 8px; align-items: baseline; font-size: .93rem;
                             padding: 3px 0; border-top: 1px dashed var(--linea); }}
.unidad .sus-capitulos .cid {{ font-weight: 600; white-space: nowrap; }}
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


RE_ENCABEZADO = re.compile(r"\\(?:chapter|section|subsection|capituloComplemento)\*?(?:\[[^\]]*\])?\{([^}]*)\}")


def capitulos_apunte() -> dict[str, str]:
    """{'rotaciones': 'Rotaciones: girar es multiplicar', 'rot3d': '…', …} en el orden del apunte.

    Cada clave X es un \\label{cap:X} de los .tex que el maestro incluye con \\input (o del maestro
    mismo); el valor es el título del encabezado de esa línea. El enlace es `apunte.pdf#nameddest=cap:X`.
    """
    res: dict[str, str] = {}
    if not MAESTRO_APUNTE.exists():
        return res
    maestro = MAESTRO_APUNTE.read_text(encoding="utf-8")
    archivos = [MAESTRO_APUNTE] + [MAESTRO_APUNTE.parent / f"{m}.tex"
                                   for m in re.findall(r"^\\input\{(contenido/[^}]+)\}", maestro, re.M)]
    for p in archivos:
        try:
            texto = p.read_text(encoding="utf-8")
        except OSError:
            continue
        for linea in texto.split("\n"):
            if linea.lstrip().startswith("%"):
                continue
            for lab in re.findall(r"\\label\{cap:([^}]+)\}", linea):
                m = RE_ENCABEZADO.search(linea)
                res.setdefault(lab, m.group(1).strip() if m else p.stem)
    return res


NUMERACION_JSON = MAESTRO_APUNTE.parent / "numeracion.json"


def numeracion_apunte() -> dict:
    """{'cap:X': {'numero', 'rotulo', 'titulo'}} de apunte/numeracion.json (lo escribe apunte/scripts/numeracion.py)."""
    if not NUMERACION_JSON.exists():
        raise SystemExit(f"ERROR: falta {NUMERACION_JSON}; compilar el apunte y correr "
                         "`uv run python apunte/scripts/numeracion.py`")
    return json.loads(NUMERACION_JSON.read_text(encoding="utf-8"))


# compatibilidad: el resto del build llama «prefijos» a las claves de capítulo
prefijos_apunte_existentes = capitulos_apunte


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
                errores.append(f"{donde}: clave de apunte '{pref}' sin \\label{{cap:{pref}}} en el apunte")

    for c in datos["clases"]:
        if "id" not in c:
            continue
        donde = f"clase {c['id']}"
        ficha = c.get("ficha")
        if ficha:
            if not (RAIZ / ficha).exists():
                avisos.append(f"{donde}: la ficha {ficha} todavía no existe")
        else:
            avisos.append(f"{donde}: sin 'ficha'")
        if "apunte" in c:
            c["apunte"] = [str(x) for x in (c["apunte"] or [])]
            chequear_apunte(c["apunte"], donde)
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
        if k.get("unidades"):
            # campo opcional: varias unidades para un nodo transversal; el nodo linkea a la primera
            k["unidades"] = [str(x) for x in k["unidades"]]
            for extra in k["unidades"]:
                if extra not in ids_unidades:
                    errores.append(f"{donde}: unidades '{extra}' no existe")
            if k.get("unidad") is None:
                k["unidad"] = k["unidades"][0]
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
    # el banco de autoevaluación vive en un módulo generado (unidades/banco_autoevaluacion.py); en el
    # export no hay archivos vecinos, así que su texto reemplaza al bloque de import marcado en cb104
    ini, fin = fuente.find("# banco:begin"), fuente.find("# banco:end")
    if ini != -1 and fin != -1:
        banco = MODULO_COMUN.with_name("banco_autoevaluacion.py")
        if not banco.exists():
            raise RuntimeError(f"{archivo}: cb104 importa el banco pero falta {banco.name}; "
                               "correr `uv run python tools/merge_banco.py`")
        fuente = fuente[:ini] + banco.read_text(encoding="utf-8") + fuente[fin + len("# banco:end"):]
    sangria = m.group("sangria")
    bloque = (
        f"{sangria}import types as _types\n"
        f'{sangria}lib = _types.ModuleType("cb104")\n'
        f'{sangria}exec(compile({fuente!r}, "cb104.py", "exec"), lib.__dict__)'
    )
    return texto[: m.start()] + bloque + texto[m.end():], True


# ancho útil de la columna de celdas en pantallas anchas: marimo define `--content-width-medium: 1110px` y la columna
# es `div.max-w-(--content-width-medium)`; en 16:9 la llevamos a 1240 px para que el hstack 10:6 (figura | controles)
# entre sin apilar. Por debajo de 1300 px de viewport queda el ancho normal de marimo.
ESTILO_ANCHO = ('<style id="cb104-ancho">'
                '@media (min-width: 1300px){:root{--content-width-medium:1240px !important}}'
                '</style>')


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
    # marimo export copia un CLAUDE.md (instrucciones para asistentes, del paquete marimo) dentro de cada export:
    # no es parte del material y no se publica
    for _p in destino.rglob("CLAUDE.md"):
        _p.unlink()
    _idx = destino / "index.html"
    _html = _idx.read_text(encoding="utf-8")
    if ESTILO_ANCHO not in _html:
        if "</head>" not in _html:
            raise RuntimeError(f"{_idx}: no encuentro </head> para inyectar el ancho 16:9")
        _idx.write_text(_html.replace("</head>", ESTILO_ANCHO + "</head>", 1), encoding="utf-8")
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


def nav_superior(raiz_rel: str = "") -> str:
    """Barra de enlaces de arriba de cada página; raiz_rel es el prefijo para llegar a la raíz del sitio ("" o "../")."""
    return (
        '<nav class="topnav">'
        f'<a href="{raiz_rel}index.html">Portada</a>'
        f'<a href="{raiz_rel}mapa.html">Mapa</a>'
        f'<a href="{raiz_rel}apunte.pdf">Apunte</a>'
        f'<a href="{raiz_rel}autoevaluacion.html">Autoevaluación</a>'
        "</nav>"
    )


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
{nav_superior(raiz_rel)}
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


VOLVER = '<p class="volver"><a href="../index.html">← hilo conductor</a><a href="../mapa.html">mapa</a></p>'


CAMPOS_FICHA = ("clase", "titulo", "idea", "que_se_estudia", "conceptos_previos", "apunte", "unidades", "animaciones", "ejercicios_sugeridos")
SECCIONES_FICHA = ("Qué se estudia", "Conceptos previos", "En el apunte", "Unidades interactivas", "Animaciones", "Ejercicios sugeridos")


def frontmatter(texto: str) -> dict:
    """El frontmatter YAML de una ficha ({} si no tiene)."""
    if not texto.startswith("---\n"):
        return {}
    fin = texto.find("\n---\n", 4)
    return (yaml.safe_load(texto[4:fin]) or {}) if fin != -1 else {}


def validar_fichas(datos: dict) -> list[str]:
    """Chequea el frontmatter de cada ficha de clases/ contra el esquema (README de clases/). Devuelve los errores."""
    errores: list[str] = []
    caps = capitulos_apunte()
    numeracion = numeracion_apunte()
    unidades = {u["id"] for u in datos["unidades"]}
    animaciones = {p.stem for p in (RAIZ / "animaciones").glob("*.mp4")}
    for src in sorted(DIR_CLASES.glob("[0-9]*.md")):
        fm = frontmatter(src.read_text(encoding="utf-8"))
        donde = src.name
        for campo in CAMPOS_FICHA:
            if campo not in fm:
                errores.append(f"{donde}: falta '{campo}'")
        if not 3 <= len(fm.get("que_se_estudia") or []) <= 6:
            errores.append(f"{donde}: 'que_se_estudia' tiene que tener de 3 a 6 ítems")
        if not 2 <= len(fm.get("ejercicios_sugeridos") or []) <= 4:
            errores.append(f"{donde}: 'ejercicios_sugeridos' tiene que tener de 2 a 4 ítems")
        for k in fm.get("apunte") or []:
            if str(k) not in caps:
                errores.append(f"{donde}: clave de apunte '{k}' sin \\label{{cap:{k}}}")
            elif f"cap:{k}" not in numeracion:
                errores.append(f"{donde}: clave de apunte '{k}' sin entrada en numeracion.json "
                               "(correr apunte/scripts/numeracion.py)")
        for u in fm.get("unidades") or []:
            if u not in unidades:
                errores.append(f"{donde}: unidad '{u}' no está en el mapa")
        for a in fm.get("animaciones") or []:
            if a not in animaciones:
                errores.append(f"{donde}: animación '{a}' no existe en animaciones/")
    return errores


def _lista_html(items: list[str]) -> str:
    return '<ul class="vinculos">' + "".join(f"<li>{i}</li>" for i in items) + "</ul>"


def secciones_vinculos(fm: dict, datos: dict, exportadas: set[str], hay_pdf: bool) -> dict[str, str]:
    """HTML de las secciones «En el apunte», «Unidades interactivas» y «Animaciones», con enlaces (desde `../`)."""
    numeracion = numeracion_apunte()
    unidades = {u["id"]: u for u in datos["unidades"]}
    res: dict[str, str] = {}
    items = []
    for k in fm.get("apunte") or []:
        e = numeracion[f"cap:{k}"]
        tit = html.escape(f'{e["rotulo"]} {e["numero"]}. {e["titulo"]}')
        items.append(f'<a href="../apunte.pdf#nameddest=cap:{html.escape(str(k))}">{tit}</a>' if hay_pdf else tit)
    if items:
        res["En el apunte"] = _lista_html(items)
    items = []
    for uid in fm.get("unidades") or []:
        tit = html.escape(unidades.get(uid, {}).get("titulo", uid))
        items.append(f'<a href="../unidades/{html.escape(uid)}/index.html">{tit}</a>' if uid in exportadas else f"{tit} (en preparación)")
    if items:
        res["Unidades interactivas"] = _lista_html(items)
    items = []
    for a in fm.get("animaciones") or []:
        items.append(f'<a href="../animaciones/{html.escape(a)}.mp4">{html.escape(a.replace("_", " "))}</a> '
                     f'(<a href="../animaciones/{html.escape(a)}.gif">gif</a>)')
    if items:
        res["Animaciones"] = _lista_html(items)
    return res


def ficha_html(texto: str, datos: dict, exportadas: set[str], hay_pdf: bool) -> str:
    """Markdown de la ficha → html; las secciones de apunte, unidades y animaciones se arman desde el frontmatter."""
    fm = frontmatter(texto)
    cuerpo = sin_front_matter(texto)
    trozos = re.split(r"^## ", cuerpo, flags=re.M)
    vinc = secciones_vinculos(fm, datos, exportadas, hay_pdf)
    partes = [md_a_html(trozos[0])]
    for tr in trozos[1:]:
        titulo, _, resto = tr.partition("\n")
        titulo = titulo.strip()
        if titulo in vinc:
            partes.append(f"<h2>{html.escape(titulo)}</h2>\n{vinc[titulo]}")
        else:
            partes.append(md_a_html("## " + titulo + "\n" + resto))
    return "\n".join(partes)


def generar_fichas(datos: dict, out: Path, exportadas: set[str] = frozenset(), hay_pdf: bool = True) -> dict[str, str]:
    """Convierte las fichas. Devuelve {id_ficha: 'capitulos/<id>.html'} para las que existen."""
    destino = out / "capitulos"
    destino.mkdir(parents=True, exist_ok=True)
    generadas: dict[str, str] = {}
    for c in datos["clases"]:
        ficha = c.get("ficha")
        if not ficha:
            continue
        src = RAIZ / ficha
        if not src.exists():
            continue
        texto = src.read_text(encoding="utf-8")
        titulo = titulo_de_md(sin_front_matter(texto), f"{rotulo_ficha(c['id'])}: {c.get('titulo', '')}")
        cuerpo = f'{VOLVER}\n<div class="ficha">\n{ficha_html(texto, datos, exportadas, hay_pdf)}\n</div>'
        (destino / f"{c['id']}.html").write_text(pagina(titulo, cuerpo, katex=True, raiz_rel="../"), encoding="utf-8")
        generadas[c["id"]] = f"capitulos/{c['id']}.html"
    return generadas


# ----------------------------------------------------------------------------
# laboratorio CAD (cad/index.md + cad/dxf → site/cad/)
# ----------------------------------------------------------------------------

DIR_CAD = RAIZ / "cad"
_RE_H2_CAPITULO = re.compile(r'<h2(?: id="[^"]*")?>Capítulo (\d+)</h2>')


def generar_cad(out: Path) -> list[Path]:
    """Copia cad/dxf/**/*.dxf a site/cad/dxf/ (misma estructura) y genera site/cad/index.html desde cad/index.md.

    Cada «## Capítulo N» queda con id="capN", el ancla que usan el menú (cad/#capN) y las fichas
    (../cad/#capN). Devuelve los DXF copiados; si no hay cad/index.md no genera la página.
    """
    destino = out / "cad"
    origen_dxf = DIR_CAD / "dxf"
    copiados: list[Path] = []
    if origen_dxf.is_dir():
        shutil.rmtree(destino / "dxf", ignore_errors=True)
        for f in sorted(origen_dxf.rglob("*.dxf")):
            d = destino / "dxf" / f.relative_to(origen_dxf)
            d.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(f, d)
            copiados.append(d)
    src = DIR_CAD / "index.md"
    if src.exists():
        texto = src.read_text(encoding="utf-8")
        cuerpo = _RE_H2_CAPITULO.sub(lambda m: f'<h2 id="cap{m.group(1)}">Capítulo {m.group(1)}</h2>', md_a_html(texto))
        titulo = titulo_de_md(texto, "Laboratorio CAD")
        destino.mkdir(parents=True, exist_ok=True)
        (destino / "index.html").write_text(
            pagina(titulo, f'{VOLVER}\n<div class="ficha">\n{cuerpo}\n</div>', katex=True, raiz_rel="../"),
            encoding="utf-8")
    return copiados


# ----------------------------------------------------------------------------
# mapa de conceptos → SVG
# ----------------------------------------------------------------------------

ANCHO_COL = 210          # ancho de cada columna (capítulo)
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
    unidades_por_id = {u["id"]: u for u in datos["unidades"]}
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
    # atributos para los controles de mapa.html: orden (1..n) y nivel de la clase de cada nodo
    orden_clase = {c["id"]: i + 1 for i, c in enumerate(clases)}
    nivel_clase = {c["id"]: c.get("nivel", "troncal") for c in clases}
    clase_de = {k["id"]: k["clase"] for k in conceptos}

    def attrs(cid: str) -> str:
        return f'data-capitulo="{html.escape(cid)}" data-orden="{orden_clase.get(cid, 0)}" data-nivel="{html.escape(nivel_clase.get(cid, "troncal"))}"'

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
        color = TEAL
        if col > 0:
            partes.append(f'<line x1="{x0}" y1="8" x2="{x0}" y2="{alto - 8}" stroke="#eee" stroke-width="1"/>')
        cx = x0 + ANCHO_COL / 2
        partes.append(f'<g class="cabecera" {attrs(c["id"])}>')
        partes.append(f'<text x="{cx}" y="{MARGEN_SUP + 12}" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">{html.escape(rotulo_ficha(c["id"]))}</text>')
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
        color, fondo = TEAL, FONDO_NODO
        if k.get("unidad") and k["unidad"] in exportadas:
            href = f"unidades/{k['unidad']}/index.html"
        elif k["clase"] in fichas:
            href = fichas[k["clase"]]
        else:
            href = None
        hover = k.get("hecho_geometrico") or k.get("nombre", "")
        if k.get("que_se_conserva"):
            hover += f" — se conserva: {k['que_se_conserva']}"
        if len(k.get("unidades") or []) > 1:
            hover += " — unidades: " + ", ".join(unidades_por_id.get(u, {}).get("titulo", u) for u in k["unidades"])
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
    """{'rotaciones': 'Rotaciones: girar es multiplicar', 'rot3d': '…', …} (ver capitulos_apunte)."""
    return capitulos_apunte()


def indice_avance(clases: list[dict]) -> int:
    """Posición (0-based) de la última clase de PROGRAMA_AVANCE en el orden del programa; -1 si no hay."""
    ids = [c["id"] for c in clases]
    return max((ids.index(i) for i in PROGRAMA_AVANCE if i in ids), default=-1)


def enlace_apunte(pref: str, titulos: dict[str, str], hay_pdf: bool) -> str:
    """Capítulo del apunte como enlace `apunte.pdf#nameddest=cap:<clave>` (los \\label{cap:…} viven en el .tex)."""
    tit = titulos.get(pref, pref)
    texto = f"apunte: {html.escape(tit)}"
    if hay_pdf:
        return f'<span><a href="apunte.pdf#nameddest=cap:{html.escape(pref)}" title="apunte, cap:{html.escape(pref)}">{texto}</a></span>'
    return f'<span class="pend">{texto}</span>'


def prefijos_apunte_de_clase(c: dict, conceptos_por_clase: dict[str, list[dict]]) -> list[str]:
    """Los `apunte` declarados en la clase, o la unión de los de sus conceptos."""
    prefs: list[str] = list(c.get("apunte") or [])
    if not prefs:
        for k in conceptos_por_clase.get(c["id"], []):
            for pr in k["apunte"]:
                if pr not in prefs:
                    prefs.append(pr)
    orden = list(capitulos_apunte())
    return sorted(prefs, key=lambda x: orden.index(x) if x in orden else len(orden))


JS_MAPA = r"""
(function () {
  var svg = document.querySelector('.mapa svg');
  if (!svg) return;
  var ruta = document.getElementById('ruta');
  var hasta = document.getElementById('hasta');
  var rotulo = document.getElementById('hasta-rotulo');
  var ids = JSON.parse(document.getElementById('capitulos-orden').textContent);
  var nodos = svg.querySelectorAll('.nodo, .cabecera');
  var aristas = svg.querySelectorAll('.arista');
  function aplicar() {
    var soloTroncal = ruta.value === 'troncal';
    var n = parseInt(hasta.value, 10);
    rotulo.textContent = ids[n - 1];
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
    """site/mapa.html: el SVG de conceptos con filtro de ruta y deslizador "hasta el capítulo N", y la lista de capítulos."""
    unidades = {u["id"]: u for u in datos["unidades"]}
    titulos_apunte = titulos_secciones_apunte()
    conceptos_por_clase: dict[str, list[dict]] = {c["id"]: [] for c in datos["clases"]}
    for k in datos["conceptos"]:
        conceptos_por_clase[k["clase"]].append(k)
    clases = datos["clases"]
    n_default = indice_avance(clases) + 1 or len(clases)

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
        f'<label><span id="hasta-rotulo">{html.escape(rotulo_hasta(clases[n_default - 1]["id"]))}</span> '
        f'<input type="range" id="hasta" min="1" max="{len(clases)}" value="{n_default}" step="1"></label>'
        "</div>"
    )
    partes.append(f'<script id="capitulos-orden" type="application/json">{json.dumps([rotulo_hasta(c["id"]) for c in clases], ensure_ascii=False)}</script>')
    partes.append('<div class="mapa">' + svg_mapa(datos, fichas, exportadas) + "</div>")
    partes.append('<p class="leyenda"><span style="--c:#777;--f:#fff">flecha: lo que un concepto requiere → el concepto</span></p>')
    partes.append('<p class="guia">Cada nodo lleva a la unidad interactiva si existe, si no a la ficha del capítulo. Pasando el mouse se ve el hecho geométrico. '
                  "El filtro de ruta esconde los capítulos complementarios y avanzados; el deslizador atenúa lo que viene después del capítulo elegido.</p>")
    partes.append(f"<script>{JS_MAPA}</script>")

    partes.append(f"<h2>Capítulos ({len(clases)})</h2>")
    partes.append('<ul class="capitulos">')
    for c in clases:
        color = TEAL
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
                links.append(f'<span class="pend">unidad: {html.escape(u.get("titulo", uid))} (en preparación)</span>')
        for pr in prefijos_apunte_de_clase(c, conceptos_por_clase):
            links.append(enlace_apunte(pr, titulos_apunte, hay_pdf))
        partes.append(
            f'<li class="capitulo" style="--c:{color}">'
            f'<div class="cab"><span class="id">{html.escape(rotulo_ficha(c["id"]))}</span>'
            f'<span class="tit">{html.escape(c.get("titulo", ""))}</span>'
            f'{etiqueta(c.get("nivel", ""), "#777")}</div>'
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


def generar_indice(datos: dict, fichas: dict[str, str], exportadas: set[str], hay_pdf: bool, out: Path) -> None:
    """site/index.html: el hilo conductor. Tres entradas y una entrada por unidad (más "Lo que viene")."""
    titulos_apunte = titulos_secciones_apunte()
    clases = datos["clases"]
    por_id = {c["id"]: c for c in clases}
    conceptos_por_clase: dict[str, list[dict]] = {c["id"]: [] for c in clases}
    for k in datos["conceptos"]:
        conceptos_por_clase[k["clase"]].append(k)

    # unidades de la portada: una por unidad de unidades.yaml, en ese orden; al final, las clases sin unidad
    unidades_portada: list[dict] = []
    cubiertas: set[str] = set()
    for u in datos["unidades"]:
        cl = [por_id[cid] for cid in u["clases"] if cid in por_id]
        cubiertas.update(c["id"] for c in cl)
        unidades_portada.append({
            "unidad": u, "titulo": u.get("titulo", u["id"]), "clases": cl,
            "pregunta": u.get("pregunta", ""), "gancho": u.get("gancho_agrimensura", ""), "nivel": u.get("nivel", ""),
        })
    sin_unidad = [c for c in clases if c["id"] not in cubiertas]
    if sin_unidad:
        unidades_portada.append({
            "unidad": None, "titulo": "Lo que viene", "clases": sin_unidad,
            "pregunta": "", "gancho": "Capítulos del programa que todavía no tienen unidad interactiva.",
            "nivel": "",
        })

    # entrada "seguir el programa": la unidad siguiente a la última que cubre una clase de PROGRAMA_AVANCE
    marcadas = set(PROGRAMA_AVANCE)
    ultima_u = max((i for i, e in enumerate(unidades_portada) if any(c["id"] in marcadas for c in e["clases"])), default=0)
    n_seguir = min(ultima_u + 1, len(unidades_portada) - 1)

    partes: list[str] = []
    partes.append(f"<h1>{html.escape(TITULO_CAMINO)}</h1>")
    if datos.get("pregunta_guia"):
        partes.append(f'<p class="guia">Pregunta guía: {html.escape(datos["pregunta_guia"])}</p>')
    seguir_sub = f"unidad {n_seguir}: {html.escape(unidades_portada[n_seguir]['titulo'])}"
    partes.append(
        '<nav class="entradas">'
        f'<a class="entrada" href="#unidad-0"><b>Empezar</b><small>unidad 0: {html.escape(unidades_portada[0]["titulo"])}</small></a>'
        f'<a class="entrada" href="#unidad-{n_seguir}"><b>Seguir el programa</b><small>{seguir_sub}</small></a>'
        '<a class="entrada" href="mapa.html"><b>Repasar</b><small>el mapa de conceptos completo</small></a>'
        '<a class="entrada" href="autoevaluacion.html"><b>Autoevaluación (120 preguntas)</b><small>practicamos, hacemos un simulacro o rendimos la evaluación</small></a>'
        '<a class="entrada" href="menu.html"><b>Para el aula: qué hay para cada capítulo</b><small>piezas por capítulo, con duración y estado; también en PDF</small></a>'
        '<a class="entrada" href="menu-por-capitulo.html"><b>Para el aula: entradas, platos y postres por capítulo</b><small>un menú por capítulo para elegir qué servir; A4 apaisado, para imprimir</small></a>'
        "</nav>"
    )

    partes.append(f"<h2>Recorrido paso a paso ({len(unidades_portada)} unidades interactivas)</h2>")
    partes.append('<ol class="hilo">')
    for i, e in enumerate(unidades_portada, start=0):
        color = TEAL
        num = "Unidad 0 — Fundamentos" if i == 0 else f"Unidad {i}"
        cab = [f'<span class="num">{num}</span>', f'<span class="tit">{html.escape(e["titulo"])}</span>',
               ]
        if e["nivel"]:
            cab.append(etiqueta(e["nivel"], "#777"))
        cuerpo = [f'<div class="cab">{"".join(cab)}</div>']
        if e["pregunta"]:
            cuerpo.append(f'<p class="pregunta">{html.escape(e["pregunta"])}</p>')
        if e["gancho"]:
            cuerpo.append(f'<p class="gancho">{html.escape(e["gancho"])}</p>')
        # clases que cubre
        filas = []
        for c in e["clases"]:
            ficha = f'<a href="{fichas[c["id"]]}">ficha</a>' if c["id"] in fichas else '<span class="pend">ficha pendiente</span>'
            filas.append(f'<li><span class="cid">{html.escape(rotulo_ficha(c["id"]))}</span><span>{html.escape(c.get("titulo", ""))}</span>'
                         f'<span>{ficha}</span></li>')
        cuerpo.append(f'<ul class="sus-capitulos">{"".join(filas)}</ul>')
        # enlaces: unidad, apunte
        links: list[str] = []
        u = e["unidad"]
        if u is not None:
            if u["id"] in exportadas:
                links.append(f'<span><a href="unidades/{html.escape(u["id"])}/index.html">abrir la unidad interactiva</a></span>')
            else:
                links.append('<span class="pend">unidad en preparación</span>')
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


BANCO_PY = RAIZ / "unidades" / "banco_autoevaluacion.py"
XML_MOODLE = RAIZ / "moodle" / "moodle_banco_120_preguntas_cb104.xml"

AUTOEVAL_PLANTILLA = r"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Autoevaluación — Sistemas de Coordenadas (CB104)</title>
  <style>/*__CSS__*/
main { overflow-wrap: anywhere; }
.modos { display: flex; flex-wrap: wrap; gap: 8px; margin: 1em 0; }
.modos button { flex: 1 1 140px; }
button { font: inherit; cursor: pointer; border: 1.5px solid var(--teal); background: #fff; color: var(--teal);
         border-radius: 8px; padding: 8px 12px; }
button:hover { border-color: var(--rust); color: var(--rust); }
button.activo { background: var(--teal); color: #fff; }
button.primario { background: var(--teal); color: #fff; }
button.peligro { border-color: var(--rust); color: var(--rust); }
button.peligro.armado { background: var(--rust); color: #fff; }
button:disabled { opacity: .5; cursor: default; }
.controles { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin: .8em 0; }
.controles label { display: flex; flex-direction: column; font-size: .85rem; color: var(--gris); min-width: 0; flex: 1 1 180px; }
select { font: inherit; padding: 6px; border: 1px solid var(--linea); border-radius: 6px; background: #fff; max-width: 100%; }
.preg { border: 1px solid var(--linea); border-left: 4px solid var(--teal); border-radius: 8px; background: #fff; padding: 10px 14px; margin: 14px 0; }
.preg .meta { font-size: .8rem; color: var(--gris); margin-bottom: 4px; }
.preg .enun p { margin: .4em 0; }
.opc { display: block; width: 100%; text-align: left; margin: 6px 0; padding: 8px 10px; border: 1.5px solid var(--linea); color: var(--tinta); background: #fff; }
.opc:hover { border-color: var(--teal); color: var(--tinta); }
.opc.sel { border-color: var(--teal); background: #e6f1f1; }
.opc.ok { border-color: #2e7d32; background: #e8f3e8; }
.opc.mal { border-color: var(--rust); background: #f8e6dd; }
.fb { margin: 4px 0 6px 12px; padding: 6px 10px; border-left: 3px solid var(--gold); background: #fbf5e1; font-size: .95rem; }
.fb.bien { border-color: #2e7d32; background: #e8f3e8; }
.fb.mal { border-color: var(--rust); background: #f8e6dd; }
.resumen { border: 2px solid var(--teal); border-radius: 8px; padding: 10px 14px; background: #fff; margin: 14px 0; }
.resumen table { border-collapse: collapse; }
.resumen td, .resumen th { padding: 2px 10px 2px 0; text-align: left; font-weight: normal; }
.acc { display: flex; flex-wrap: wrap; gap: 8px; margin: 12px 0; }
.bien-t { color: #2e7d32; } .mal-t { color: var(--rust); }
.hist li { margin: 3px 0; }
.katex-display { overflow-x: auto; overflow-y: hidden; max-width: 100%; }
.aviso { color: var(--gris); font-size: .9rem; }
</style>
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
</head>
<body>
<main>
__NAV__
<h1>Autoevaluación</h1>
<p>Reunimos 120 preguntas de opción múltiple, seis por unidad (dos elementales, dos medias y dos avanzadas). Podemos practicar con devolución inmediata, hacer un simulacro de una pregunta por unidad o rendir la evaluación, que admite cuatro intentos.</p>
<div class="modos" id="modos">
  <button data-modo="practica">Práctica</button>
  <button data-modo="simulacro">Simulacro</button>
  <button data-modo="evaluacion">Evaluación (4 intentos)</button>
</div>
<div id="app"></div>
<p class="pie"><a href="moodle_banco_120_preguntas_cb104.xml">Banco para Moodle (XML, 120 preguntas)</a> · <a href="index.html">Volver a la portada</a></p>
</main>
<script id="banco" type="application/json">__BANCO_JSON__</script>
<script>
(function () {
  "use strict";
  var DATOS = JSON.parse(document.getElementById("banco").textContent);
  var UNIDADES = DATOS.unidades;
  var BANCO = DATOS.banco;
  var NIVELES = ["elemental", "medio", "avanzado"];
  var MAX_INTENTOS = 4;
  var CLAVE = "cb104_evaluacion";
  var app = document.getElementById("app");
  var modoActual = "practica";
  var estado = {};

  // ---------- utilidades ----------
  function baraja(a) {
    var r = a.slice();
    for (var i = r.length - 1; i > 0; i--) {
      var j = Math.floor(Math.random() * (i + 1));
      var t = r[i]; r[i] = r[j]; r[j] = t;
    }
    return r;
  }
  function elige(a) { return a[Math.floor(Math.random() * a.length)]; }
  function el(tag, cls, texto) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (texto != null) e.textContent = texto;
    return e;
  }
  function esc(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  function inline(s) {
    return esc(s).replace(/`([^`]+)`/g, "<code>$1</code>")
      .replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>")
      .replace(/(^|[^*\w])\*([^*\s][^*]*)\*(?![*\w])/g, "$1<i>$2</i>");
  }
  // markdown mínimo que deja intactas las fórmulas $...$ y $$...$$
  function md(texto) {
    var partes = String(texto).split(/(\$\$[\s\S]+?\$\$|\$[^$\n]+?\$)/);
    var out = "";
    for (var i = 0; i < partes.length; i++) {
      if (i % 2 === 1) { out += esc(partes[i]); }
      else { out += inline(partes[i]).replace(/\n\n+/g, "</p><p>").replace(/\n/g, "<br>"); }
    }
    return "<p>" + out + "</p>";
  }
  function mdInline(texto) { return md(texto).replace(/^<p>/, "").replace(/<\/p>$/, ""); }
  function mate(nodo) {
    if (window.renderMathInElement) {
      window.renderMathInElement(nodo, {
        delimiters: [
          { left: "$$", right: "$$", display: true },
          { left: "$", right: "$", display: false }
        ],
        throwOnError: false
      });
    }
  }
  function tituloUnidad(id) {
    for (var i = 0; i < UNIDADES.length; i++) if (UNIDADES[i].id === id) return UNIDADES[i].titulo;
    return id;
  }
  function indiceUnidad(id) {
    for (var i = 0; i < UNIDADES.length; i++) if (UNIDADES[i].id === id) return i;
    return 999;
  }
  function todasLasPreguntas() {
    var r = [];
    UNIDADES.forEach(function (u) {
      (BANCO[u.id] || []).forEach(function (q) { r.push({ q: q, unidad: u.id }); });
    });
    return r;
  }
  function armaItem(p) {
    return { q: p.q, unidad: p.unidad, orden: baraja(p.q.opciones), elegida: null };
  }
  function correctaDe(item) {
    for (var i = 0; i < item.q.opciones.length; i++) if (item.q.opciones[i].correcta) return item.q.opciones[i];
    return null;
  }
  function acerto(item) {
    return item.elegida !== null && item.elegida.correcta === true;
  }
  function unaPorUnidad() {
    var r = [];
    UNIDADES.forEach(function (u) {
      var lista = BANCO[u.id] || [];
      if (!lista.length) return;
      var nivel = elige(NIVELES);
      var delNivel = lista.filter(function (q) { return q.nivel === nivel; });
      r.push({ q: elige(delNivel.length ? delNivel : lista), unidad: u.id });
    });
    return r;
  }
  function porOrdenDeUnidad(items) {
    return items.map(function (it, k) { return { it: it, k: k }; })
      .sort(function (a, b) {
        var d = indiceUnidad(a.it.unidad) - indiceUnidad(b.it.unidad);
        return d !== 0 ? d : a.k - b.k;
      }).map(function (x) { return x.it; });
  }
  function armaSimulacro(total) {
    var base = unaPorUnidad();
    if (total > base.length) {
      var usadas = {};
      base.forEach(function (p) { usadas[p.q.id] = true; });
      var resto = baraja(todasLasPreguntas().filter(function (p) { return !usadas[p.q.id]; }));
      base = base.concat(resto.slice(0, total - base.length));
    }
    return porOrdenDeUnidad(base.map(armaItem));
  }

  // ---------- dibujo de una pregunta ----------
  // fase: "inmediato" (práctica), "abierta" (sin devolución), "corregida" (con explicaciones)
  function dibujaPregunta(item, n, fase, alElegir) {
    var caja = el("div", "preg");
    var meta = el("div", "meta", "Pregunta " + n + " · " + tituloUnidad(item.unidad) + " · nivel " + item.q.nivel);
    caja.appendChild(meta);
    var enun = el("div", "enun");
    enun.innerHTML = md(item.q.enunciado);
    caja.appendChild(enun);
    var correcta = correctaDe(item);
    var contFb = el("div");
    var botones = [];
    item.orden.forEach(function (op, i) {
      var b = el("button", "opc");
      b.type = "button";
      b.innerHTML = "<b>" + "ABCD".charAt(i) + ")</b> " + mdInline(op.texto);
      botones.push({ b: b, op: op });
      b.addEventListener("click", function () {
        if (fase === "corregida") return;
        if (fase === "inmediato" && item.elegida !== null) return;
        item.elegida = op;
        if (fase === "abierta") {
          botones.forEach(function (x) { x.b.classList.toggle("sel", x.op === op); });
          if (alElegir) alElegir();
        } else {
          pinta();
        }
      });
      caja.appendChild(b);
    });
    caja.appendChild(contFb);
    function pinta() {
      contFb.innerHTML = "";
      botones.forEach(function (x) {
        x.b.classList.remove("ok", "mal");
        if (item.elegida === x.op) x.b.classList.add(x.op.correcta ? "ok" : "mal");
        if (item.elegida !== null && !x.op.correcta && item.elegida !== x.op) { /* sin marca */ }
        if (item.elegida !== null && x.op.correcta) x.b.classList.add("ok");
      });
      if (item.elegida === null) {
        if (fase === "corregida") contFb.appendChild(avisoSinResponder());
        return;
      }
      var f1 = el("div", "fb " + (item.elegida.correcta ? "bien" : "mal"));
      f1.innerHTML = "<b>" + (item.elegida.correcta ? "Correcta." : "Incorrecta.") + "</b> " + mdInline(item.elegida.explicacion || "");
      contFb.appendChild(f1);
      if (!item.elegida.correcta && correcta) {
        var f2 = el("div", "fb");
        f2.innerHTML = "<b>La correcta era:</b> " + mdInline(correcta.texto) + "<br>" + mdInline(correcta.explicacion || "");
        contFb.appendChild(f2);
      }
      mate(contFb);
    }
    function avisoSinResponder() {
      var f = el("div", "fb mal");
      f.innerHTML = "<b>Sin responder.</b> La correcta era: " + (correcta ? mdInline(correcta.texto) + "<br>" + mdInline(correcta.explicacion || "") : "");
      return f;
    }
    if (fase === "corregida") pinta();
    return caja;
  }

  // ---------- modo práctica ----------
  function vistaPractica() {
    var st = estado.practica || (estado.practica = { unidad: "todas", nivel: "todos", items: null });
    app.innerHTML = "";
    var ctl = el("div", "controles");
    var lu = el("label", null, "Unidad");
    var su = el("select");
    su.appendChild(new Option("Todas las unidades", "todas"));
    UNIDADES.forEach(function (u, i) { su.appendChild(new Option(i + ". " + u.titulo, u.id)); });
    su.value = st.unidad;
    lu.appendChild(su);
    var ln = el("label", null, "Nivel");
    var sn = el("select");
    sn.appendChild(new Option("Todos los niveles", "todos"));
    NIVELES.forEach(function (n) { sn.appendChild(new Option(n, n)); });
    sn.value = st.nivel;
    ln.appendChild(sn);
    var bm = el("button", "primario", "🔀 Mezclar");
    bm.type = "button";
    ctl.appendChild(lu); ctl.appendChild(ln); ctl.appendChild(bm);
    app.appendChild(ctl);
    var lista = el("div");
    app.appendChild(lista);

    function arma() {
      var base = todasLasPreguntas().filter(function (p) {
        return (st.unidad === "todas" || p.unidad === st.unidad) && (st.nivel === "todos" || p.q.nivel === st.nivel);
      });
      st.items = baraja(base).map(armaItem);
      dibuja();
    }
    function dibuja() {
      lista.innerHTML = "";
      var c = el("p", "aviso", st.items.length + (st.items.length === 1 ? " pregunta" : " preguntas") + ". Elegimos una opción y vemos al instante si acertamos y por qué.");
      lista.appendChild(c);
      st.items.forEach(function (it, i) { lista.appendChild(dibujaPregunta(it, i + 1, "inmediato")); });
      mate(lista);
    }
    su.addEventListener("change", function () { st.unidad = su.value; arma(); });
    sn.addEventListener("change", function () { st.nivel = sn.value; arma(); });
    bm.addEventListener("click", arma);
    if (st.items) dibuja(); else arma();
  }

  // ---------- simulacro y evaluación: núcleo común ----------
  function resumenPorNivel(items) {
    var t = el("table");
    NIVELES.forEach(function (n) {
      var tot = 0, ok = 0;
      items.forEach(function (it) { if (it.q.nivel === n) { tot++; if (acerto(it)) ok++; } });
      if (!tot) return;
      var tr = el("tr");
      tr.appendChild(el("th", null, "Nivel " + n));
      tr.appendChild(el("td", null, ok + " de " + tot));
      t.appendChild(tr);
    });
    return t;
  }
  function puntaje(items) {
    var ok = 0;
    items.forEach(function (it) { if (acerto(it)) ok++; });
    return ok;
  }
  function sinResponder(items) {
    return items.filter(function (it) { return it.elegida === null; }).length;
  }

  // ---------- modo simulacro ----------
  function vistaSimulacro() {
    var st = estado.simulacro;
    if (!st) { st = estado.simulacro = { items: armaSimulacro(20), entregado: false }; }
    app.innerHTML = "";
    app.appendChild(el("p", "aviso", "Veinte preguntas, una por unidad y en el orden de las unidades. No hay devolución hasta que entregamos."));
    var lista = el("div");
    app.appendChild(lista);
    var barra = el("div", "acc");
    app.appendChild(barra);
    var resultado = el("div");
    app.appendChild(resultado);
    var bEntregar = el("button", "primario", "Entregar");
    bEntregar.type = "button";
    var bNuevo = el("button", null, "Nuevo simulacro");
    bNuevo.type = "button";
    barra.appendChild(bEntregar); barra.appendChild(bNuevo);
    var contador = el("p", "aviso");
    app.insertBefore(contador, barra);

    function actualiza() {
      var faltan = sinResponder(st.items);
      contador.textContent = st.entregado ? "" : (faltan ? "Nos faltan " + faltan + " por responder." : "Respondimos todas; podemos entregar.");
    }
    function dibuja() {
      lista.innerHTML = "";
      st.items.forEach(function (it, i) {
        lista.appendChild(dibujaPregunta(it, i + 1, st.entregado ? "corregida" : "abierta", actualiza));
      });
      resultado.innerHTML = "";
      if (st.entregado) {
        var r = el("div", "resumen");
        r.appendChild(el("h2", null, "Puntaje: " + puntaje(st.items) + " de " + st.items.length));
        r.appendChild(resumenPorNivel(st.items));
        resultado.appendChild(r);
        bEntregar.disabled = true;
      } else {
        bEntregar.disabled = false;
      }
      actualiza();
      mate(lista);
    }
    bEntregar.addEventListener("click", function () {
      st.entregado = true; dibuja();
      resultado.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
    bNuevo.addEventListener("click", function () {
      estado.simulacro = null; vistaSimulacro(); window.scrollTo(0, 0);
    });
    dibuja();
  }

  // ---------- modo evaluación ----------
  function leeRegistro() {
    try {
      var r = JSON.parse(window.localStorage.getItem(CLAVE) || "null");
      if (r && Array.isArray(r.intentos)) return r;
    } catch (e) { /* sin registro */ }
    return { intentos: [] };
  }
  function guardaRegistro(r) {
    try { window.localStorage.setItem(CLAVE, JSON.stringify(r)); return true; }
    catch (e) { return false; }
  }
  function fechaLinda(iso) {
    var d = new Date(iso);
    return isNaN(d.getTime()) ? iso : d.toLocaleString("es-AR");
  }
  function textoResultado(intento, k, items) {
    var l = [];
    l.push("Autoevaluación CB104 Sistemas de Coordenadas — Evaluación");
    l.push("Fecha: " + intento.fecha);
    l.push("Intento " + k + " de " + MAX_INTENTOS);
    l.push("Puntaje: " + intento.puntaje + " de " + intento.total);
    l.push("");
    intento.preguntas.forEach(function (p, i) {
      l.push((i + 1) + ". " + tituloUnidad(p.unidad) + " | nivel " + p.nivel + " | " + p.id + " | " + (p.ok ? "acertada" : "fallada"));
    });
    l.push("");
    return l.join("\n");
  }
  function descarga(nombre, texto) {
    var blob = new Blob([texto], { type: "text/plain;charset=utf-8" });
    var url = URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url; a.download = nombre;
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }
  function dibujaHistorial(contenedor, reg) {
    contenedor.innerHTML = "";
    if (!reg.intentos.length) return;
    contenedor.appendChild(el("h2", null, "Historial"));
    var ul = el("ul", "hist");
    var mejor = 0;
    reg.intentos.forEach(function (it, i) {
      if (it.puntaje > mejor) mejor = it.puntaje;
      ul.appendChild(el("li", null, "Intento " + (i + 1) + " (" + fechaLinda(it.fecha) + "): " + it.puntaje + " de " + it.total));
    });
    contenedor.appendChild(ul);
    contenedor.appendChild(el("p", null, "Mejor nota: " + mejor + " de " + reg.intentos[0].total + "."));
  }
  function botonBorrar(reg, alBorrar) {
    var b = el("button", "peligro", "Borrar historial");
    b.type = "button";
    var armado = false;
    b.addEventListener("click", function () {
      if (!armado) {
        armado = true;
        b.classList.add("armado");
        b.textContent = "Hacemos clic de nuevo para confirmar el borrado";
        return;
      }
      try { window.localStorage.removeItem(CLAVE); } catch (e) { /* nada */ }
      alBorrar();
    });
    return b;
  }

  function vistaEvaluacion() {
    var reg = leeRegistro();
    app.innerHTML = "";
    if (reg.intentos.length >= MAX_INTENTOS) {
      app.appendChild(el("h2", null, "Agotamos los " + MAX_INTENTOS + " intentos"));
      var h = el("div");
      dibujaHistorial(h, reg);
      app.appendChild(h);
      var acc = el("div", "acc");
      acc.appendChild(botonBorrar(reg, function () { estado.evaluacion = null; vistaEvaluacion(); }));
      app.appendChild(acc);
      app.appendChild(el("p", "aviso", "El registro vive sólo en este navegador; si lo borramos, empezamos de cero."));
      return;
    }
    var st = estado.evaluacion;
    if (!st) { st = estado.evaluacion = { items: armaSimulacro(30), entregado: false, k: reg.intentos.length + 1 }; }
    var k = st.k;
    app.appendChild(el("h2", null, "Intento " + k + " de " + MAX_INTENTOS));
    app.appendChild(el("p", "aviso", "Treinta preguntas: una por unidad más diez al azar. Al entregar vemos el puntaje y qué unidades acertamos, sin explicaciones. El intento se anota en este navegador."));
    var lista = el("div");
    var contador = el("p", "aviso");
    var barra = el("div", "acc");
    var resultado = el("div");
    var histo = el("div");
    app.appendChild(lista); app.appendChild(contador); app.appendChild(barra);
    app.appendChild(resultado); app.appendChild(histo);
    var bEntregar = el("button", "primario", "Entregar");
    bEntregar.type = "button";
    barra.appendChild(bEntregar);

    function actualiza() {
      var faltan = sinResponder(st.items);
      contador.textContent = st.entregado ? "" : (faltan ? "Nos faltan " + faltan + " por responder." : "Respondimos todas; podemos entregar.");
    }
    function dibujaEntregado() {
      var intento = st.intento;
      var r = el("div", "resumen");
      r.appendChild(el("h2", null, "Puntaje: " + intento.puntaje + " de " + intento.total));
      r.appendChild(resumenPorNivel(st.items));
      var ul = el("ul", "hist");
      st.items.forEach(function (it) {
        var li = el("li");
        var ok = acerto(it);
        li.innerHTML = (ok ? '<span class="bien-t">Acertada</span>' : '<span class="mal-t">Fallada</span>') + " — " + esc(tituloUnidad(it.unidad)) + " (" + it.q.nivel + ")";
        ul.appendChild(li);
      });
      r.appendChild(ul);
      if (!st.guardado) r.appendChild(el("p", "aviso", "No pudimos guardar el intento en este navegador; conviene descargar el resultado."));
      resultado.appendChild(r);
      barra.innerHTML = "";
      var bd = el("button", "primario", "Descargar resultado");
      bd.type = "button";
      bd.addEventListener("click", function () {
        descarga("resultado_evaluacion_cb104_intento" + k + ".txt", textoResultado(intento, k, st.items));
      });
      barra.appendChild(bd);
      if (k < MAX_INTENTOS) {
        var bs = el("button", null, "Siguiente intento");
        bs.type = "button";
        bs.addEventListener("click", function () { estado.evaluacion = null; vistaEvaluacion(); window.scrollTo(0, 0); });
        barra.appendChild(bs);
      } else {
        var bh = el("button", null, "Ver el cierre de los intentos");
        bh.type = "button";
        bh.addEventListener("click", function () { estado.evaluacion = null; vistaEvaluacion(); window.scrollTo(0, 0); });
        barra.appendChild(bh);
      }
      dibujaHistorial(histo, leeRegistro());
    }
    function dibuja() {
      if (st.entregado) { lista.innerHTML = ""; contador.textContent = ""; dibujaEntregado(); return; }
      lista.innerHTML = "";
      st.items.forEach(function (it, i) { lista.appendChild(dibujaPregunta(it, i + 1, "abierta", actualiza)); });
      actualiza();
      dibujaHistorial(histo, reg);
      mate(lista);
    }
    bEntregar.addEventListener("click", function () {
      if (st.entregado) return;
      var intento = {
        fecha: new Date().toISOString(),
        puntaje: puntaje(st.items),
        total: st.items.length,
        preguntas: st.items.map(function (it) {
          return { id: it.q.id, unidad: it.unidad, nivel: it.q.nivel, ok: acerto(it) };
        })
      };
      var r2 = leeRegistro();
      r2.intentos.push(intento);
      st.guardado = guardaRegistro(r2);
      st.intento = intento;
      st.entregado = true;
      dibuja();
      resultado.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
    dibuja();
  }

  // ---------- pestañas ----------
  function muestra(modo) {
    modoActual = modo;
    var bs = document.querySelectorAll("#modos button");
    for (var i = 0; i < bs.length; i++) bs[i].classList.toggle("activo", bs[i].getAttribute("data-modo") === modo);
    if (modo === "practica") vistaPractica();
    else if (modo === "simulacro") vistaSimulacro();
    else vistaEvaluacion();
  }
  var bs = document.querySelectorAll("#modos button");
  for (var i = 0; i < bs.length; i++) {
    bs[i].addEventListener("click", function () { muestra(this.getAttribute("data-modo")); });
  }
  muestra("practica");
  window.addEventListener("load", function () { mate(app); });
})();
</script>
</body>
</html>
"""


def generar_autoevaluacion(datos_mapa: dict, out: Path) -> None:
    """site/autoevaluacion.html: página autocontenida (JS inline + KaTeX por CDN) con práctica, simulacro y evaluación."""
    import importlib.util
    if not BANCO_PY.exists():
        raise RuntimeError(f"no existe {BANCO_PY.relative_to(RAIZ)}; corré `uv run python tools/merge_banco.py`")
    spec = importlib.util.spec_from_file_location("banco_autoevaluacion", BANCO_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    banco = mod.BANCO_AUTOEVALUACION
    unidades = [{"id": u["id"], "titulo": u.get("titulo", u["id"])} for u in datos_mapa["unidades"] if u["id"] in banco]
    carga = json.dumps({"unidades": unidades, "banco": banco}, ensure_ascii=False).replace("</", "<\\/")
    htm = (AUTOEVAL_PLANTILLA.replace("/*__CSS__*/", CSS)
           .replace("__NAV__", nav_superior())
           .replace("__BANCO_JSON__", carga))
    (out / "autoevaluacion.html").write_text(htm, encoding="utf-8")


# ----------------------------------------------------------------------------
# main
# ----------------------------------------------------------------------------


REDIRECCIONES = {"unidades/00_desaprender_el_cbc/index.html": "../00_fundamentos/"}
# las fichas vivían en site/clases/<id>.html y pasaron a site/capitulos/<id>.html
for _id in ("01", "02", "03", "03p", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"):
    REDIRECCIONES[f"clases/{_id}.html"] = f"../capitulos/{_id}.html"


def generar_redirecciones(out: Path) -> None:
    """Páginas mínimas de redirección para enlaces viejos (unidad renombrada, fichas movidas a capitulos/)."""
    for ruta, destino in REDIRECCIONES.items():
        d = html.escape(destino)
        nombre = html.escape(destino.strip("/").split("/")[-1])
        ficha = ruta.startswith("clases/")
        pagina = (
            '<!doctype html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n'
            f'<meta http-equiv="refresh" content="0; url={d}">\n'
            f'<link rel="canonical" href="{d}">\n'
            "<title>Redirección</title>\n</head>\n<body>\n"
            f'<p><a href="{d}">Esta página se movió: {nombre if ficha else "unidades/" + nombre + "/"}</a></p>\n</body>\n</html>\n'
        )
        dest = out / ruta
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(pagina, encoding="utf-8")
        print(f"  redirección: {ruta} -> {destino}")


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
    shutil.rmtree(out / "_build", ignore_errors=True)   # intermedios: nunca quedan en el sitio

    t_total = time.perf_counter()
    print(f"== mapa: {Path(args.mapa).relative_to(RAIZ) if Path(args.mapa).is_relative_to(RAIZ) else args.mapa}")
    try:
        datos = cargar_mapa(Path(args.mapa))
        avisos = validar(datos)
        errores_fichas = validar_fichas(datos)
        if errores_fichas:
            raise ErrorMapa("\n".join(errores_fichas))
    except ErrorMapa as e:
        print(f"ERROR en mapa.yaml:\n{e}", file=sys.stderr)
        return 1
    for a in avisos:
        print(f"  aviso: {a}")
    print(f"  {len(datos['clases'])} fichas, {len(datos['conceptos'])} conceptos, {len(datos['unidades'])} unidades")

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
        if not args.only:
            shutil.rmtree(out / "_build", ignore_errors=True)
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

    print("== redirecciones")
    generar_redirecciones(out)

    print("== fichas")
    fichas = generar_fichas(datos, out, exportadas, PDF_APUNTE.exists())
    print(f"  {len(fichas)} fichas generadas: {sorted(fichas) or 'ninguna'}")

    print("== apunte")
    hay_pdf = PDF_APUNTE.exists()
    if hay_pdf:
        shutil.copy2(PDF_APUNTE, out / "apunte.pdf")
        print(f"  copiado apunte.pdf ({PDF_APUNTE.stat().st_size / 1e6:.1f} MB)")
    anim = RAIZ / "animaciones"
    if anim.is_dir():
        dest = out / "animaciones"
        dest.mkdir(exist_ok=True)
        for f in sorted(anim.glob("*.mp4")) + sorted(anim.glob("*.gif")):
            shutil.copy2(f, dest / f.name)
        print(f"  copiadas {len(list(dest.iterdir()))} animaciones a site/animaciones/")
    else:
        print(f"  aviso: no existe {PDF_APUNTE.relative_to(RAIZ)}; el índice no linkea el PDF")

    print("== autoevaluación")
    if not BANCO_PY.exists():
        print(f"ERROR: falta {BANCO_PY.relative_to(RAIZ)}; corré `uv run python tools/merge_banco.py`", file=sys.stderr)
        return 1
    subprocess.run([sys.executable, str(RAIZ / "tools" / "exportar_moodle_xml.py")], check=True)
    shutil.copy2(XML_MOODLE, out / XML_MOODLE.name)
    generar_autoevaluacion(datos, out)
    print(f"  {out / 'autoevaluacion.html'}")
    print(f"  {out / XML_MOODLE.name}")

    print("== portada y mapa"
    )
    generar_indice(datos, fichas, exportadas, hay_pdf, out)
    generar_mapa(datos, fichas, exportadas, hay_pdf, out)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"  {out / 'index.html'}")
    print(f"  {out / 'mapa.html'}")

    print("== laboratorio CAD")
    dxf_cad = generar_cad(out)
    if (out / "cad" / "index.html").exists():
        print(f"  {out / 'cad' / 'index.html'}")
    print(f"  {len(dxf_cad)} DXF copiados a {out.name}/cad/dxf/")

    if tiempos:
        print("== tiempos de export WASM")
        for k, v in tiempos.items():
            print(f"  {k}: {v:.1f}s")
    for _p in out.rglob("CLAUDE.md"):   # por si quedó alguno de un export anterior
        _p.unlink()
    shutil.rmtree(out / "_build", ignore_errors=True)
    print("== menú: piezas por capítulo")
    import menu
    if menu.main(["--site", str(out)]) != 0:
        print("ERROR: tools/menu.py falló (enlace roto o mención prohibida en el menú)", file=sys.stderr)
        return 1
    print("== menú por capítulo")
    import importlib.util
    _spec = importlib.util.spec_from_file_location("menu_por_capitulo", RAIZ / "tools" / "menu_por_capitulo" / "gen.py")
    menu_por_capitulo = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(menu_por_capitulo)
    if menu_por_capitulo.main(["--site", str(out)]) != 0:
        print("ERROR: tools/menu_por_capitulo/gen.py falló (enlace roto en menu-por-capitulo.html)", file=sys.stderr)
        return 1
    print("== menciones prohibidas")
    sys.path.insert(0, str(RAIZ / "apunte" / "scripts"))
    import prohibidas
    _proh = prohibidas.revisar_archivos(prohibidas.archivos_site(out), out)
    for _r, _n, _l in _proh:
        print(f"  {_r}:{_n}: {_l[:200]}")
    if _proh:
        print(f"  TOTAL: {len(_proh)} coincidencias fuera de las excepciones")
        return 1
    print(f"== listo en {time.perf_counter() - t_total:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
