#!/usr/bin/env python3
"""Genera el sitio estático `site/` de Sistemas de Coordenadas (CB104).

Entradas (relativas a la raíz del repo):
  mapa/mapa.yaml                        mapa de conceptos (esquema en mapa/ESQUEMA.md)
  clases/*.md                           fichas por clase
  unidades/*.py                         notebooks marimo
  apunte/Apunte_Sistemas_de_Coordenadas.pdf
  apunte/contenido/NN-*.tex             sólo para validar prefijos y leer títulos de sección

Salida:
  site/index.html                       índice con el mapa de conceptos (SVG inline) y la lista de clases
  site/clases/<id>.html                 fichas (markdown → html, KaTeX desde CDN)
  site/unidades/<id>/index.html         notebooks exportados a WASM (marimo export html-wasm)
  site/apunte.pdf                       copia del apunte
  site/.nojekyll                        para GitHub Pages

Uso:  uv run tools/build.py [--skip-wasm] [--only <unidad_id>] [--out site]
"""

from __future__ import annotations

import argparse
import html
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

ESTADOS_CLASE = ("con-transcripcion", "reconstruida", "no-dictada")
ESTADOS_UNIDAD = ("piloto", "migrada", "legacy", "pendiente")
ESTADOS_EXPORTABLES = ("piloto", "migrada")

# paleta del apunte
TEAL, RUST, GOLD = "#1b6f6a", "#b5532a", "#c9a227"
COLOR_ESTADO = {
    "con-transcripcion": (TEAL, "#e3f1f0"),
    "reconstruida": (GOLD, "#faf3dc"),
    "no-dictada": (RUST, "#f8e6dd"),
}
ETIQUETA_ESTADO = {
    "con-transcripcion": "con transcripción",
    "reconstruida": "reconstruida",
    "no-dictada": "no dictada",
}
ETIQUETA_ESTADO_UNIDAD = {
    "piloto": "piloto",
    "migrada": "migrada",
    "legacy": "legacy (no publicada)",
    "pendiente": "pendiente",
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
.clase .links {{ font-size: .95rem; margin: 4px 0 0; }}
.clase .links span {{ margin-right: 12px; white-space: nowrap; }}
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
.katex-display {{ overflow-x: auto; overflow-y: hidden; }}
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

    if errores:
        raise ErrorMapa("\n".join(f"  - {e}" for e in errores))
    return avisos


# ----------------------------------------------------------------------------
# exportación WASM
# ----------------------------------------------------------------------------


def exportar_unidad(u: dict, out: Path) -> float:
    destino = out / "unidades" / u["id"]
    if destino.exists():
        shutil.rmtree(destino)
    destino.parent.mkdir(parents=True, exist_ok=True)
    # mismo intérprete del venv (equivale a `uv run marimo ...` sin anidar uv)
    cmd = [
        sys.executable, "-m", "marimo", "export", "html-wasm",
        "--mode", "run", "--no-show-code", "--force",
        "-o", str(destino), str(RAIZ / u["archivo"]),
    ]
    print(f"  exportando {u['id']} ({u['archivo']}) ...", flush=True)
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
        texto = src.read_text(encoding="utf-8")
        titulo = titulo_de_md(texto, f"Clase {c['id']} — {c.get('titulo', '')}")
        cuerpo = f'<p class="volver"><a href="../index.html">← índice</a></p>\n<div class="ficha">\n{md_a_html(texto)}\n</div>'
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
            texto = src.read_text(encoding="utf-8")
            titulo = titulo_de_md(texto, src.stem)
            cuerpo = f'<p class="volver"><a href="../index.html">← índice</a></p>\n<div class="ficha">\n{md_a_html(texto)}\n</div>'
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
        partes.append(f'<text x="{cx}" y="{MARGEN_SUP + 12}" text-anchor="middle" font-size="13" font-weight="700" fill="{color}">Clase {html.escape(c["id"])}</text>')
        for i, ln in enumerate(cab_lineas[c["id"]]):
            partes.append(f'<text x="{cx}" y="{MARGEN_SUP + 30 + i * ALTO_LINEA}" text-anchor="middle" font-size="12" fill="#444">{html.escape(ln)}</text>')

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
            partes.append(f'<path d="{d}" fill="none" stroke="#777" stroke-width="1.3" marker-end="url(#flecha)" opacity="0.5"/>')

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
        if href:
            partes.append(f'<a href="{html.escape(href)}" style="cursor:pointer">{nodo}</a>')
        else:
            partes.append(f"<g>{nodo}</g>")
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


def generar_indice(datos: dict, fichas: dict[str, str], exportadas: set[str], hay_pdf: bool, out: Path) -> None:
    unidades = {u["id"]: u for u in datos["unidades"]}
    titulos_apunte = titulos_secciones_apunte()
    conceptos_por_clase: dict[str, list[dict]] = {c["id"]: [] for c in datos["clases"]}
    for k in datos["conceptos"]:
        conceptos_por_clase[k["clase"]].append(k)

    partes: list[str] = []
    partes.append(f"<h1>{html.escape(datos['titulo'])}</h1>")
    if datos.get("pregunta_guia"):
        partes.append(f'<p class="guia">Pregunta guía: {html.escape(datos["pregunta_guia"])}</p>')

    partes.append("<h2>Mapa de conceptos</h2>")
    partes.append('<div class="mapa">' + svg_mapa(datos, fichas, exportadas) + "</div>")
    leyenda = "".join(
        f'<span style="--c:{COLOR_ESTADO[e][0]};--f:{COLOR_ESTADO[e][1]}">{ETIQUETA_ESTADO[e]}</span>' for e in ESTADOS_CLASE
    )
    partes.append(f'<p class="leyenda">{leyenda}<span style="--c:#777;--f:#fff">flecha: lo que un concepto requiere → el concepto</span></p>')
    partes.append('<p class="guia">Cada nodo lleva a la unidad interactiva si existe, si no a la ficha de la clase. Pasando el mouse se ve el hecho geométrico.</p>')

    partes.append(f"<h2>Clases ({len(datos['clases'])})</h2>")
    partes.append('<ul class="clases">')
    for c in datos["clases"]:
        color, _ = COLOR_ESTADO.get(c.get("estado"), (RUST, "#eee"))
        estado = ETIQUETA_ESTADO.get(c.get("estado"), c.get("estado", ""))
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
        # unidades de los conceptos de la clase (sin repetir, en orden)
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
        # secciones del apunte: las de la clase, o la unión de las de sus conceptos
        prefs: list[str] = list(c.get("apunte") or [])
        if not prefs:
            for k in conceptos_por_clase[c["id"]]:
                for p in k["apunte"]:
                    if p not in prefs:
                        prefs.append(p)
        for p in sorted(prefs):
            tit = titulos_apunte.get(p, p)
            if hay_pdf:
                links.append(f'<span><a href="apunte.pdf" title="apunte, capítulo {html.escape(p)}">apunte §{html.escape(p)}: {html.escape(tit)}</a></span>')
            else:
                links.append(f'<span class="pend">apunte §{html.escape(p)}: {html.escape(tit)}</span>')
        partes.append(
            f'<li class="clase" style="--c:{color}">'
            f'<div class="cab"><span class="id">Clase {html.escape(c["id"])}</span>'
            f'<span class="tit">{html.escape(c.get("titulo", ""))}</span>'
            f'<span class="estado">{html.escape(estado)}</span></div>'
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

    partes.append('<p class="pie">Material de estudio de CB104 Sistemas de Coordenadas (Agrimensura, FIUBA), hecho por Gustavo Varela como alumno. '
                  "Las unidades interactivas corren en el navegador (marimo + Pyodide); la primera carga tarda unos segundos.</p>")

    (out / "index.html").write_text(pagina(datos["titulo"], "\n".join(partes)), encoding="utf-8")


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

    print("== índice")
    generar_indice(datos, fichas, exportadas, hay_pdf, out)
    (out / ".nojekyll").write_text("", encoding="utf-8")
    print(f"  {out / 'index.html'}")

    if tiempos:
        print("== tiempos de export WASM")
        for k, v in tiempos.items():
            print(f"  {k}: {v:.1f}s")
    print(f"== listo en {time.perf_counter() - t_total:.1f}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
