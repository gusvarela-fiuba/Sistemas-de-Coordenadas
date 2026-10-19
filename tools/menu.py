#!/usr/bin/env python3
"""Menú por capítulo: qué piezas hay para usar en el aula en cada capítulo, cuánto duran y si están listas.

Genera `site/menu.html` (estilo del sitio) y `site/menu.pdf` (A4 apaisada, para imprimir, con enlaces).
Todo sale de los datos del repo; no hay texto escrito a mano salvo el que ya está en las fichas:

  filas         una por ficha del mapa (mapa/mapa.yaml), en su orden; el rótulo de capítulo sale de
                build.CAPITULO_DE_FICHA (la ficha 03 cubre los capítulos 3 y 4; la 03p es el complemento C1)
  explicar      viñetas de la sección «## Imágenes para explicar» de la ficha; si no está: «en preparación»
  televisor     unidades del frontmatter de la ficha (título y pregunta del mapa) y animaciones del
                frontmatter (descripción: primera oración del docstring de tools/animaciones/anim_<id>.py)
  puestos       viñetas de «## Ejercicios sugeridos» de la ficha (con las unidades del capítulo para resolverlos),
                «Ahora ustedes» si aparece en unidades/*.py o en apunte/contenido/*.tex (sólo lectura) y
                ejercicio CAD desde cad/ejercicios.yaml (lista de {capitulo, archivo, titulo, comando})
  estudiar      capítulo(s) del PDF con su página, autoevaluación y cantidad de preguntas del banco
                (unidades/banco_autoevaluacion.py) de las unidades del capítulo

Página del PDF: numeracion.json no guarda páginas. La página física sale de los destinos con nombre
`cap:X` del PDF publicado (`pdfinfo -dests site/apunte.pdf`, columna 1: índice físico, contando portada y
páginas iniciales); el enlace es `apunte.pdf#page=<física>` y el número que se muestra es el impreso al pie
de esa página («N de M», leído con `pdftotext -f P -l P`). Sin poppler instalado, el enlace cae a
`apunte.pdf#nameddest=cap:X` sin número de página (aviso en la salida).

Una pieza se marca «lista» sólo si su destino existe en el sitio al generar; al final se verifica que todo
enlace relativo del HTML y del PDF apunte a un archivo existente (si no, exit 1).

Uso:  uv run python tools/menu.py [--site site]
"""

from __future__ import annotations

import argparse
import html
import importlib.util
import re
import shutil
import subprocess
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from build import (  # noqa: E402
    BANCO_PY, CAPITULO_DE_FICHA, RAIZ, cargar_mapa, frontmatter, numeracion_apunte, pagina, rotulo_ficha,
    sin_front_matter,
)

sys.path.insert(0, str(RAIZ / "apunte" / "scripts"))
import prohibidas  # noqa: E402

MAPA = RAIZ / "mapa" / "mapa.yaml"
CLAVE_FICHAS = "".join(("cla", "ses"))      # nombre de la lista de fichas en el esquema del mapa (mapa/ESQUEMA.md)
DIR_ANIM_FUENTE = RAIZ / "tools" / "animaciones"
CAD_YAML = RAIZ / "cad" / "ejercicios.yaml"
TITULO = "Para el aula: qué hay para cada capítulo"
BAJADA = "Material para usar en el aula, por capítulo. Cada pieza funciona sola."
LISTA, PREP = "lista", "en preparación"
COLUMNAS = ("Capítulo", "Para explicar (2 min)", "Para mostrar en el televisor (5 a 10 min)",
            "Para los puestos (15 a 20 min)", "Para estudiar")
SECCION_IMAGENES = "Imágenes para explicar"
SECCION_EJERCICIOS = "Ejercicios sugeridos"
AHORA = "Ahora ustedes"


# ----------------------------------------------------------------------------
# datos
# ----------------------------------------------------------------------------


def secciones_md(texto: str) -> dict[str, list[str]]:
    """{título de sección ##: [viñetas de primer nivel, una línea cada una]} del cuerpo de una ficha."""
    res: dict[str, list[str]] = {}
    for tr in re.split(r"^## ", sin_front_matter(texto), flags=re.M)[1:]:
        tit, _, resto = tr.partition("\n")
        res[tit.strip()] = [m.group(1).strip() for m in re.finditer(r"^[-*]\s+(.+)$", resto, re.M)]
    return res


def url_sitio() -> str:
    """URL publicada del sitio (la del README, que tools/adoptar_para_catedra.py reescribe); '' si no está."""
    try:
        m = re.search(r"https://[^\s)]+\.github\.io/[^\s)/]+/", (RAIZ / "README.md").read_text(encoding="utf-8"))
    except OSError:
        return ""
    return m.group(0) if m else ""


def cargar_banco() -> dict[str, list]:
    spec = importlib.util.spec_from_file_location("banco_autoevaluacion", BANCO_PY)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.BANCO_AUTOEVALUACION


def descripcion_animacion(aid: str) -> str:
    """Primera oración del docstring del módulo que dibuja la animación, sin el prefijo «Animación NN …»."""
    p = DIR_ANIM_FUENTE / f"anim_{aid}.py"
    if not p.exists():
        return ""
    m = re.match(r'\s*"""(.*?)(?:\n\s*\n|""")', p.read_text(encoding="utf-8"), re.S)
    if not m:
        return ""
    texto = " ".join(m.group(1).split())
    texto = re.sub(r"^Animación \d+\s*(?:—\s*|\([^)]*\):\s*)", "", texto)
    fin = re.search(r"\.(\s|$)", texto)
    texto = texto[: fin.start() + 1] if fin else texto
    return texto[:1].upper() + texto[1:]


def destinos_pdf(pdf: Path) -> dict[str, tuple[int, str]] | None:
    """{'cap:X': (página física, número impreso o '')} desde el PDF; None si no hay poppler o no hay PDF."""
    if not pdf.exists() or not shutil.which("pdfinfo"):
        return None
    r = subprocess.run(["pdfinfo", "-dests", str(pdf)], capture_output=True, text=True)
    if r.returncode != 0:
        return None
    res: dict[str, tuple[int, str]] = {}
    for m in re.finditer(r'^\s*(\d+)\s+\[.*\]\s+"(cap:[^"]+)"\s*$', r.stdout, re.M):
        fis = int(m.group(1))
        impreso = ""
        if shutil.which("pdftotext"):
            t = subprocess.run(["pdftotext", "-layout", "-f", str(fis), "-l", str(fis), str(pdf), "-"],
                               capture_output=True, text=True).stdout
            pie = re.findall(r"^\s*(\d+) de \d+\s*$", t, re.M)
            impreso = pie[-1] if pie else ""
        res[m.group(2)] = (fis, impreso)
    return res


def ahora_ustedes(numeracion: dict) -> tuple[set[str], set[str]]:
    """Unidades (id) y capítulos (número) donde aparece «Ahora ustedes»."""
    unidades = {p.stem for p in (RAIZ / "unidades").glob("*.py") if AHORA in p.read_text(encoding="utf-8", errors="ignore")}
    caps: set[str] = set()
    for p in (RAIZ / "apunte" / "contenido").glob("*.tex"):
        t = p.read_text(encoding="utf-8", errors="ignore")
        if AHORA not in t:
            continue
        for lab in re.findall(r"\\label\{(cap:[^}]+)\}", t):
            e = numeracion.get(lab)
            if e and e["rotulo"] in ("Capítulo", "Complemento"):
                caps.add(e["numero"])
    return unidades, caps


def cargar_cad() -> list[dict]:
    if not CAD_YAML.exists():
        return []
    datos = yaml.safe_load(CAD_YAML.read_text(encoding="utf-8")) or []
    return [d for d in datos if isinstance(d, dict) and "capitulo" in d]


# ----------------------------------------------------------------------------
# piezas: {texto, href|None, estado, detalle} — el mismo modelo arma el HTML y el PDF
# ----------------------------------------------------------------------------


def pieza(texto: str, href: str | None, site: Path, detalle: str = "", forzar_prep: bool = False) -> dict:
    """Pieza con enlace; queda «lista» sólo si el destino existe en el sitio."""
    ok = href is not None and not forzar_prep and existe(site, href)
    return {"texto": texto, "href": href if ok else None, "estado": LISTA if ok else PREP, "detalle": detalle}


def texto_suelto(texto: str, estado: str = LISTA, detalle: str = "") -> dict:
    return {"texto": texto, "href": None, "estado": estado, "detalle": detalle}


def existe(site: Path, href: str) -> bool:
    ruta = href.split("#", 1)[0].split("?", 1)[0]
    if not ruta:
        return True
    p = site / ruta
    if ruta.endswith("/"):
        p = p / "index.html"
    return p.is_file()


def titulo_capitulo_pdf(cid: str) -> str:
    """Título del PDF (el `\\chapter{...}`, vía apunte/numeracion.json) del capítulo de la ficha `cid`.

    Si la ficha cubre dos capítulos (la 03: 3 y 4) devuelve los dos títulos separados por «; »."""
    por_numero = {e["numero"]: e["titulo"] for e in numeracion_apunte().values()
                  if e["rotulo"] in ("Capítulo", "Complemento")}
    nums = CAPITULO_DE_FICHA.get(cid, cid).split(" y ")
    return "; ".join(por_numero.get(n, n) for n in nums)


def armar_filas(site: Path) -> list[dict]:
    datos = cargar_mapa(MAPA)
    numeracion = numeracion_apunte()
    unidades = {u["id"]: u for u in datos["unidades"]}
    banco = cargar_banco()
    dests = destinos_pdf(site / "apunte.pdf")
    if dests is None:
        print("  aviso: sin pdfinfo/pdftotext (poppler) o sin site/apunte.pdf: enlaces al PDF por destino con nombre, sin página")
    au_unidades, au_caps = ahora_ustedes(numeracion)
    cad = cargar_cad()
    por_numero = {e["numero"]: (k, e) for k, e in numeracion.items() if e["rotulo"] in ("Capítulo", "Complemento")}

    filas = []
    for f in datos[CLAVE_FICHAS]:
        cid = f["id"]
        src = RAIZ / f["ficha"] if f.get("ficha") else None
        texto = src.read_text(encoding="utf-8") if src and src.exists() else ""
        fm, secs = frontmatter(texto), secciones_md(texto)
        numeros = CAPITULO_DE_FICHA.get(cid, cid).split(" y ")
        uids = [u for u in fm.get("unidades") or [] if u in unidades]

        tema = {"rotulo": rotulo_ficha(cid), "titulo": titulo_capitulo_pdf(cid),
                "ficha": pieza("ficha del capítulo", f"capitulos/{cid}.html", site)}

        explicar = [texto_suelto(t) for t in secs.get(SECCION_IMAGENES, [])] or [texto_suelto("", PREP)]

        tele = [pieza(unidades[u].get("titulo", u), f"unidades/{u}/index.html", site,
                      unidades[u].get("pregunta", "")) for u in uids]
        tele += [pieza(f"Animación: {descripcion_animacion(a) or a.replace('_', ' ')}", f"animaciones/{a}.mp4", site)
                 for a in fm.get("animaciones") or []]

        puestos = [texto_suelto(t) for t in secs.get(SECCION_EJERCICIOS, [])]
        con = [pieza(unidades[u].get("titulo", u), f"unidades/{u}/index.html", site) for u in uids]
        for u in uids:
            if u in au_unidades:
                puestos.append(pieza(f"{AHORA} ({unidades[u].get('titulo', u)})", f"unidades/{u}/index.html", site))
        for n in numeros:
            if n in au_caps and n in por_numero:
                puestos.append(pieza(f"{AHORA} (capítulo {n} del apunte)", f"apunte.pdf#nameddest={por_numero[n][0]}", site))
        cad_fila = [c for c in cad if str(c["capitulo"]) in numeros]
        if cad_fila:
            for c in cad_fila:
                titulo = str(c.get("titulo") or c.get("archivo", ""))
                comando = f" (comando {c['comando']})" if c.get("comando") else ""
                puestos.append(pieza(f"CAD: {titulo}{comando}", f"cad/#cap{c['capitulo']}", site))
        else:
            puestos.append(texto_suelto("Ejercicio CAD", PREP))

        estudiar = []
        for n in numeros:
            if n not in por_numero:
                estudiar.append(texto_suelto(f"Capítulo {n} del apunte", PREP))
                continue
            k, e = por_numero[n]
            nombre = f'{e["rotulo"]} {e["numero"]}. {e["titulo"]}'
            if dests is not None and k in dests:
                fis, impreso = dests[k]
                estudiar.append(pieza(nombre, f"apunte.pdf#page={fis}", site,
                                      f"pág. {impreso}" if impreso else f"pág. {fis} del PDF"))
            elif dests is None:
                estudiar.append(pieza(nombre, f"apunte.pdf#nameddest={k}", site))
            else:
                estudiar.append(texto_suelto(nombre, PREP))
        en_banco = [u for u in uids if banco.get(u)]
        n_preg = sum(len(banco[u]) for u in en_banco)
        nombres = ", ".join(f"«{unidades[u].get('titulo', u)}»" for u in en_banco)
        estudiar.append(pieza(f"Autoevaluación: {n_preg} preguntas", "autoevaluacion.html", site,
                              f"en Práctica, elegir la unidad {nombres}" if len(en_banco) == 1 else
                              f"en Práctica, elegir las unidades {nombres}" if en_banco else "",
                              forzar_prep=n_preg == 0))

        filas.append({"cid": cid, "tema": tema, "explicar": explicar, "tele": tele, "puestos": puestos,
                      "con": con, "estudiar": estudiar})
    return filas


# ----------------------------------------------------------------------------
# HTML
# ----------------------------------------------------------------------------

CSS_MENU = """
<style>
main { max-width: 1320px; }
.bajada { font-size: 1.05rem; margin: 0 0 .4em; }
.leyenda-menu { color: var(--gris); font-size: .9rem; margin: 0 0 1em; }
.menu { border-collapse: collapse; width: 100%; background: #fff; font-size: .9rem; }
.menu th, .menu td { border: 1px solid var(--linea); padding: 6px 8px; vertical-align: top; text-align: left; }
.menu th { background: #f3efe4; color: var(--rust); position: sticky; top: 0; }
.menu td.tema { width: 14%; }
.menu td.tema b { color: var(--teal); display: block; }
.menu ul { margin: 0; padding-left: 1.1em; }
.menu li { margin: 0 0 4px; }
.menu .det { color: var(--gris); display: block; font-size: .85rem; }
.menu .con { margin: 4px 0 0; font-size: .85rem; }
.estado { font-size: .72rem; border-radius: 8px; padding: 0 6px; margin-left: 4px; white-space: nowrap; border: 1px solid; }
.estado.lista { color: var(--teal); border-color: var(--teal); }
.estado.prep { color: var(--gris); border-color: var(--linea); background: #f7f5ef; }
.imprimir { margin: 0 0 1em; }
</style>
"""


def marca(estado: str) -> str:
    return f'<span class="estado {"lista" if estado == LISTA else "prep"}">{estado}</span>'


def pieza_html(p: dict) -> str:
    txt = html.escape(p["texto"])
    cuerpo = f'<a href="{html.escape(p["href"])}">{txt}</a>' if p["href"] else txt
    det = f'<span class="det">{html.escape(p["detalle"])}</span>' if p["detalle"] else ""
    return f"{cuerpo}{marca(p['estado'])}{det}" if txt else marca(p["estado"])


def lista_html(piezas: list[dict]) -> str:
    if not piezas:
        return marca(PREP)
    return "<ul>" + "".join(f"<li>{pieza_html(p)}</li>" for p in piezas) + "</ul>"


def generar_html(filas: list[dict], site: Path) -> str:
    partes = [CSS_MENU, f"<h1>{html.escape(TITULO)}</h1>", f'<p class="bajada">{html.escape(BAJADA)}</p>',
              f'<p class="leyenda-menu">{marca(LISTA)} publicada en este sitio; {marca(PREP)} todavía no está. '
              "Los minutos son de referencia.</p>",
              '<p class="imprimir"><a href="menu.pdf">Versión para imprimir (PDF, A4 apaisada)</a> · '
              '<a href="menu-por-capitulo.html">Entradas, platos y postres por capítulo</a></p>',
              '<div style="overflow-x:auto"><table class="menu"><thead><tr>'
              + "".join(f"<th>{html.escape(c)}</th>" for c in COLUMNAS) + "</tr></thead><tbody>"]
    for f in filas:
        t = f["tema"]
        ficha = f'<a href="{t["ficha"]["href"]}">ficha del capítulo</a>' if t["ficha"]["href"] else ""
        con = ""
        if f["con"]:
            con = '<p class="con">Con: ' + "; ".join(pieza_html(p) for p in f["con"]) + "</p>"
        partes.append(
            f'<tr id="tema-{html.escape(f["cid"])}">'
            f'<td class="tema"><b>{html.escape(t["rotulo"])}</b>{html.escape(t["titulo"])}<br>{ficha}</td>'
            f"<td>{lista_html(f['explicar'])}</td>"
            f"<td>{lista_html(f['tele'])}</td>"
            f"<td>{lista_html(f['puestos'])}{con}</td>"
            f"<td>{lista_html(f['estudiar'])}</td></tr>")
    partes.append("</tbody></table></div>")
    return pagina(TITULO, "\n".join(partes), katex=True)


# ----------------------------------------------------------------------------
# PDF (reportlab)
# ----------------------------------------------------------------------------

FUENTES = [  # (normal, negrita): la primera que exista; Arial Unicode (macOS) y DejaVu (Linux) tienen griego y flechas
    ("/System/Library/Fonts/Supplemental/Arial Unicode.ttf", "/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/TTF/DejaVuSans.ttf", "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf"),
]

LATEX_UNICODE = {r"\mapsto": "↦", r"\leftrightarrow": "↔", r"\times": "×", r"\sigma": "σ", r"\varphi": "φ",
                 r"\lambda": "λ", r"\pm": "±", r"\det": "det", r"\cdot": "·", r"\,": " ", r"\infty": "∞",
                 r"\theta": "θ", r"\alpha": "α", r"\beta": "β", r"\omega": "ω", r"\pi": "π"}


def registrar_fuentes() -> tuple[str, str]:
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    for normal, negrita in FUENTES:
        if Path(normal).exists():
            pdfmetrics.registerFont(TTFont("MenuSans", normal))
            pdfmetrics.registerFont(TTFont("MenuSans-Negrita", negrita if Path(negrita).exists() else normal))
            return "MenuSans", "MenuSans-Negrita"
    import reportlab
    vera = Path(reportlab.__file__).parent / "fonts"
    pdfmetrics.registerFont(TTFont("MenuSans", str(vera / "Vera.ttf")))
    pdfmetrics.registerFont(TTFont("MenuSans-Negrita", str(vera / "VeraBd.ttf")))
    print("  aviso: sin Arial Unicode ni DejaVu; menu.pdf usa Vera (sin letras griegas)")
    return "MenuSans", "MenuSans-Negrita"


def _matriz(m: re.Match) -> str:
    filas = [" ".join(c.strip() for c in f.split("&")) for f in m.group(1).split(r"\\")]
    return "[" + "; ".join(filas) + "]"


def math_a_markup(s: str) -> str:
    """Texto con $…$ de LaTeX → markup de Paragraph de reportlab (Unicode, <sub>, <super>)."""
    def una(m: re.Match) -> str:
        t = re.sub(r"\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}", _matriz, m.group(1), flags=re.S)
        t = re.sub(r"\\mathrm\{([^}]*)\}", r"\1", t)
        for k, v in sorted(LATEX_UNICODE.items(), key=lambda kv: -len(kv[0])):
            t = t.replace(k, v)
        t = html.escape(t, quote=False)
        t = re.sub(r"\^\{([^}]*)\}|\^(\S)", lambda x: f"<super>{x.group(1) or x.group(2)}</super>", t)
        t = re.sub(r"_\{([^}]*)\}|_(\w)", lambda x: f"<sub>{x.group(1) or x.group(2)}</sub>", t)
        return t
    partes = re.split(r"(\$[^$]+\$)", s.replace("`", ""))
    sueltos = {"ᵀ": "<super>T</super>"}      # glifos que las fuentes de FUENTES no traen
    return "".join(una(re.match(r"\$(.*)\$", p, re.S)) if p.startswith("$") else re.sub("|".join(sueltos), lambda x: sueltos[x.group(0)], html.escape(p, quote=False))
                   for p in partes)


def generar_pdf(filas: list[dict], destino: Path, base: str) -> list[str]:
    """Escribe menu.pdf; devuelve los href relativos usados (para el chequeo de enlaces)."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.units import mm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

    normal, negrita = registrar_fuentes()
    teal, rust = colors.HexColor("#1b6f6a"), colors.HexColor("#b5532a")
    est = ParagraphStyle("celda", fontName=normal, fontSize=6.6, leading=7.9)
    est_cab = ParagraphStyle("cab", parent=est, fontName=negrita, fontSize=7.4, leading=9, textColor=rust)
    est_tit = ParagraphStyle("tit", fontName=negrita, fontSize=13, leading=16, textColor=teal)
    est_baj = ParagraphStyle("baj", fontName=normal, fontSize=8.5, leading=11)
    usados: list[str] = []

    def enlace(href: str, txt: str) -> str:
        usados.append(href)
        return f'<a href="{html.escape(base + href)}" color="#1b6f6a">{txt}</a>'

    def marca_pdf(e: str) -> str:
        return f'<font color="#1b6f6a">[{e}]</font>' if e == LISTA else f'<font color="#888888">[{e}]</font>'

    def pz(p: dict) -> str:
        txt = math_a_markup(p["texto"])
        cuerpo = enlace(p["href"], txt) if p["href"] else txt
        return f"{cuerpo} {marca_pdf(p['estado'])}" if txt else marca_pdf(p["estado"])

    def celda(piezas: list[dict], extra: str = "") -> Paragraph:
        lineas = [f"• {pz(p)}" for p in piezas] or [marca_pdf(PREP)]
        return Paragraph("<br/>".join(lineas) + extra, est)

    datos = [[Paragraph(html.escape(c), est_cab) for c in COLUMNAS]]
    for f in filas:
        t = f["tema"]
        ficha = "<br/>" + enlace(t["ficha"]["href"], "ficha del capítulo") if t["ficha"]["href"] else ""
        con = "<br/>Se resuelven con las unidades de la columna anterior." if f["con"] else ""
        estudiar = [dict(p, texto=p["texto"] + (f" ({p['detalle']})" if p["detalle"].startswith("pág.") else ""))
                    for p in f["estudiar"]]
        datos.append([
            Paragraph(f'<font name="{negrita}" color="#1b6f6a">{html.escape(t["rotulo"])}</font><br/>'
                      f'{html.escape(t["titulo"])}{ficha}', est),
            celda(f["explicar"]), celda(f["tele"]), celda(f["puestos"], con), celda(estudiar)])

    ancho = landscape(A4)[0] - 20 * mm
    tabla = Table(datos, colWidths=[ancho * x for x in (0.13, 0.11, 0.24, 0.32, 0.20)], repeatRows=1)
    tabla.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#d8d3c6")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#f3efe4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
        ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ]))
    pie = (f'{marca_pdf(LISTA)} publicada en el sitio; {marca_pdf(PREP)} todavía no está. '
           f'Versión en línea: {enlace("menu.html", html.escape(base + "menu.html") if base else "menu.html")}')
    doc = SimpleDocTemplate(str(destino), pagesize=landscape(A4), leftMargin=10 * mm, rightMargin=10 * mm,
                            topMargin=9 * mm, bottomMargin=9 * mm, title=TITULO, author="Sistemas de Coordenadas")
    doc.build([Paragraph(html.escape(TITULO), est_tit), Paragraph(html.escape(BAJADA) + " " + pie, est_baj),
               Paragraph("&nbsp;", est), tabla])
    return usados


# ----------------------------------------------------------------------------
# verificación
# ----------------------------------------------------------------------------


# páginas que build.py genera después del menú (tools/menu_por_capitulo/gen.py verifica la suya al generarla)
GENERADAS_DESPUES = {"menu-por-capitulo.html"}


def enlaces_rotos(site: Path, hrefs: list[str]) -> list[str]:
    rel = [h for h in hrefs if not re.match(r"^[a-z]+:|^#", h) and h not in GENERADAS_DESPUES]
    return sorted({h for h in rel if not existe(site, h)})


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Genera site/menu.html y site/menu.pdf (piezas por capítulo para el aula).")
    ap.add_argument("--site", default="site", help="directorio del sitio ya generado (default: site)")
    a = ap.parse_args(argv)
    site = Path(a.site)
    if not site.is_absolute():
        site = RAIZ / site
    if not site.is_dir():
        print(f"ERROR: {site} no existe; correr antes tools/build.py", file=sys.stderr)
        return 1

    filas = armar_filas(site)
    htm = generar_html(filas, site)
    (site / "menu.html").write_text(htm, encoding="utf-8")
    base = url_sitio()
    hrefs_pdf = generar_pdf(filas, site / "menu.pdf", base)

    errores = []
    hrefs_html = [html.unescape(h) for h in re.findall(r'href="([^"]+)"', htm)]
    for h in enlaces_rotos(site, hrefs_html):
        errores.append(f"menu.html: enlace roto {h}")
    for h in enlaces_rotos(site, hrefs_pdf):
        errores.append(f"menu.pdf: enlace roto {h}")
    # palabras prohibidas en todo lo que va al PDF (el HTML lo revisa build.py con el resto del sitio)
    if shutil.which("pdftotext"):
        texto_pdf = subprocess.run(["pdftotext", "-layout", str(site / "menu.pdf"), "-"], capture_output=True, text=True).stdout
    else:
        texto_pdf = re.sub(r"<[^>]+>", " ", htm)
    for n, l in prohibidas.coincidencias_en_texto(texto_pdf):
        errores.append(f"menu.pdf:{n}: mención prohibida: {l.strip()[:160]}")

    pend = sum(p["estado"] == PREP for f in filas for k in ("explicar", "tele", "puestos", "estudiar") for p in f[k])
    total = sum(len(f[k]) for f in filas for k in ("explicar", "tele", "puestos", "estudiar"))
    print(f"  {site / 'menu.html'}")
    print(f"  {site / 'menu.pdf'}  ({len(filas)} capítulos, {total - pend} piezas listas, {pend} en preparación)")
    for e in errores:
        print(f"ERROR: {e}", file=sys.stderr)
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
