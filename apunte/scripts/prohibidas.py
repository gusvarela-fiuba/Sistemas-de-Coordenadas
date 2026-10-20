#!/usr/bin/env python3
"""Patrón único de menciones prohibidas y chequeo del árbol versionado y del sitio generado.

Uso (desde la raíz del repo):
  uv run python apunte/scripts/prohibidas.py [--dir RUTA | --site RUTA] [--solo-arbol | --solo-site]
  --dir RUTA revisa SOLO ese directorio (artefacto publicado), sin el árbol git, e incluye el
  texto de los *.pdf vía `pdftotext -layout` (requerido; si falta, falla).
Imprime `ruta:línea: texto` por cada coincidencia fuera de EXCEPCIONES.
Regla «guía»: «guía resuelta»/«la guía» solo se admiten en .md de la raíz, mapa/ y docs/ (árbol git);
  nunca en apunte/, unidades/, tools/, clases/ ni en el sitio/PDF (--dir).
Exit 1 si hay alguna. Solo biblioteca estándar.
"""
import argparse, re, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATRON = re.compile(r"profesor|docente|clavijo|resumen de clase|cursada|en clase|dictad|palabras del|pizarr|campus|anticipad|pendiente de validar|validación pendiente|2C2026|transcripci|procedencia|CC-BY|CC BY|padr[oó]n|56798|donaci|licencia|cátedra|alumno de|Dropbox|/Users/|esqueleto|sesi[oó]n|gu[ií]a resuelta|(?:la|las) gu[ií]as?|Ejercicios\.pdf|afinidad\.pdf|facsimil|enunciados originales|se reproduce|resúmenes de clase|CEIA|\bclases?\b(?!/)", re.I)

# Regla (no por archivo): «guía resuelta» / «la guía» solo se admiten en archivos .md de documentación del repo
# que NO van al PDF ni al sitio: los .md de la raíz y los de mapa/ y docs/. NUNCA en apunte/, unidades/, tools/,
# clases/ (las fichas clases/*.md se convierten a HTML y van al sitio) ni en el sitio/PDF (--dir).
GUIA = re.compile(r"gu[ií]a resuelta|(?:la|las) gu[ií]as?", re.I)
DIRS_GUIA_OK = ("mapa", "docs")

# (ruta relativa a la raíz, None = todo el archivo | fragmento literal que debe estar en la línea)
EXCEPCIONES = [
    # Ahí se declara la donación y las condiciones de uso; solo vive en el repo.
    ("NOTA_DE_DONACION.md", None),
    # Sección «Cómo citar»: enlace a la nota de donación.
    ("README.md", "NOTA_DE_DONACION.md"),
    # Licencia de un dato externo (Copernicus DEM).
    ("datos/dem_copernicus/README.md", "Licencia: Copernicus DEM licence"),
    # Herramienta para que otro curso adopte el material: la palabra es su propósito (solo árbol, no va al sitio).
    ("tools/adoptar_para_catedra.py", None),
    # El patrón mismo.
    ("apunte/scripts/prohibidas.py", None),
    # Archivos de condiciones de uso pedidos por el editor (2026-10): el texto de las dos licencias y la cita.
    ("LICENSE", None),
    ("CITATION.cff", None),
]

# Línea única de condiciones de uso, visible en el pie del sitio y en la página legal del PDF. Se admite SÓLO esta frase
# literal, SÓLO en los archivos de FRASE_CC_ARBOL (árbol git) o en el sitio/PDF (--dir), y SÓLO si sacándola de la línea
# no queda otra coincidencia del patrón. Cualquier otra mención (suelta, parafraseada o en otro archivo) sigue prohibida.
FRASE_CC = "Texto, figuras y preguntas: CC BY-SA 4.0. Código: MIT. Ver LICENSE."
FRASE_CC_ARBOL = {"tools/build.py", "apunte/Apunte_Sistemas_de_Coordenadas.tex"}


def _frase_cc_ok(ruta_rel, linea, arbol):
    if FRASE_CC not in linea or (arbol and ruta_rel not in FRASE_CC_ARBOL):
        return False
    return not PATRON.search(linea.replace(FRASE_CC, ""))

EXT_SITE = {".html", ".md", ".xml", ".js", ".py", ".txt", ".yaml", ".yml", ".json", ".css"}


# «clase» (palabra suelta) está prohibida como texto visible: el sitio y el PDF hablan de capítulos. `clases/…` (ruta de las
# fichas fuente) no cuenta. Excepción: los identificadores del esquema del mapa, que no se renombran, en los archivos que
# los definen o documentan (el texto que ve el lector sale de build.py y se revisa igual con --dir site).
CLASE = re.compile(r"\bclases?\b(?!/)", re.I)
CLASE_ESQUEMA_TODO = {"tools/build.py", "tools/merge_mapa.py", "tools/README.md", "mapa/ESQUEMA.md", "mapa/README.md",
                      "mapa/CONCEPTOS.md", "clases/README.md"}
CLASE_ESQUEMA_COMENT = re.compile(r"\bclases?\[|,clase,")   # comentarios que citan el esquema: clases[id,…] / nombre,clase,unidad
CLASE_CLAVE_YAML = re.compile(r"^\s*(?:- )?clases?:")   # claves `clase:` / `clases:` de mapa/ y del frontmatter de las fichas


def _clase_esquema_ok(ruta_rel, linea):
    """True si TODAS las coincidencias de la línea son la palabra «clase» como identificador del esquema."""
    if ruta_rel in CLASE_ESQUEMA_TODO:
        resto = CLASE.sub("", linea)
    elif (ruta_rel.startswith("mapa/") and ruta_rel.endswith(".yaml")) or (ruta_rel.startswith("clases/") and ruta_rel.endswith(".md")):
        clave = CLASE_CLAVE_YAML.match(linea) or (linea.lstrip().startswith("#") and CLASE_ESQUEMA_COMENT.search(linea))
        resto = CLASE.sub("", linea) if clave else linea
    else:
        return False
    return not PATRON.search(resto)


def coincidencias_en_texto(texto):
    return [(i, l) for i, l in enumerate(texto.split("\n"), 1) if PATRON.search(l)]


def _guia_ok(ruta_rel, linea):
    """True si TODAS las coincidencias de la línea son de la regla «guía» y la ruta es un .md admitido."""
    partes = Path(ruta_rel).parts
    if not ruta_rel.endswith(".md") or not (len(partes) == 1 or partes[0] in DIRS_GUIA_OK):
        return False
    return all(GUIA.fullmatch(m.group(0)) for m in PATRON.finditer(linea))


# Nombre de la página para quien da la materia (pedido del editor): el archivo PARA_EL_DOCENTE.md, la página
# para-el-docente.html (y su id de encabezado) y su título «Para el docente» (encabezado `# `, <title>, <h1>,
# texto del enlace de la portada, y ese rótulo en negrita donde el instructivo describe la portada).
# Se quitan sólo esos literales (sensibles a mayúsculas); el resto de la línea y el contenido se siguen revisando.
NOMBRE_PAGINA_DOCENTE = re.compile(r"PARA_EL_DOCENTE\.md|para-el-docente(?:\.html)?|^# Para el docente$|>Para el docente<|\*\*Para el docente\.\*\*")


def _nombre_pagina_ok(linea):
    """True si la línea sólo coincide con el patrón por el nombre del archivo o el título de esa página."""
    resto = NOMBRE_PAGINA_DOCENTE.sub("", linea.strip())
    return resto != linea.strip() and not PATRON.search(resto)


def permitida(ruta_rel, linea, arbol=True):
    ruta_rel = str(ruta_rel)
    if _nombre_pagina_ok(linea):
        return True
    if arbol and _guia_ok(ruta_rel, linea):
        return True
    if arbol and _clase_esquema_ok(ruta_rel, linea):
        return True
    if _frase_cc_ok(ruta_rel, linea, arbol):
        return True
    for r, frag in EXCEPCIONES:
        if r == ruta_rel and (frag is None or frag in linea):
            return True
    return False


def _leer(p):
    try:
        b = Path(p).read_bytes()
    except OSError:
        return None
    if b"\0" in b:
        return None
    try:
        return b.decode("utf-8")
    except UnicodeDecodeError:
        return None


def revisar_archivos(rutas, raiz, arbol=True):
    raiz = Path(raiz).resolve()
    out = []
    for p in rutas:
        p = Path(p)
        t = _leer(p)
        if t is None:
            continue
        try:
            rel = str(p.resolve().relative_to(raiz))
        except ValueError:
            rel = p.name
        for n, l in coincidencias_en_texto(t):
            if not permitida(rel, l, arbol):
                out.append((rel, n, l.strip()))
    return out


def archivos_arbol(raiz=ROOT):
    o = subprocess.run(["git", "ls-files", "-z"], cwd=raiz, capture_output=True, text=True).stdout
    return [Path(raiz) / f for f in o.split("\0") if f and (Path(raiz) / f).is_file()]


def archivos_site(site):
    site = Path(site)
    out = []
    for p in sorted(site.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXT_SITE:
            continue
        rel = p.relative_to(site).parts
        # unidades/*/assets/ es el frontend de marimo/pyodide copiado del wheel: no es contenido.
        if len(rel) >= 3 and rel[0] == "unidades" and "assets" in rel[2:-1]:
            continue
        out.append(p)
    return out


def pdfs_site(site):
    return sorted(p for p in Path(site).rglob("*.pdf") if p.is_file())


def revisar_pdfs(pdfs, site):
    """Aplica el patrón al texto de cada PDF (pdftotext -layout). Reporta ruta.pdf:pág N:línea."""
    if not pdfs:
        return []
    if not shutil.which("pdftotext"):
        print("ERROR: pdftotext no está instalado (poppler-utils); no se puede revisar el texto del PDF", file=sys.stderr)
        sys.exit(2)
    out = []
    for p in pdfs:
        r = subprocess.run(["pdftotext", "-layout", str(p), "-"], capture_output=True, text=True)
        if r.returncode != 0:
            print(f"ERROR: pdftotext falló en {p}: {r.stderr.strip()}", file=sys.stderr)
            sys.exit(2)
        rel = str(p.relative_to(site))
        for pag, txt in enumerate(r.stdout.split("\f"), 1):
            for n, l in coincidencias_en_texto(txt):
                if not permitida(rel, l, False):
                    out.append((f"{rel}:pág {pag}", n, l.strip()))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Búsqueda de menciones prohibidas. Regla «guía»: «guía resuelta»/«la guía» solo admitidas en .md de la raíz, mapa/ y docs/ (no en apunte/, unidades/, tools/, clases/, site/ ni PDF). Sin opciones: árbol git + site/. "
                                 "Con --dir/--site RUTA: solo ese directorio (más PDF), sin el árbol git.")
    ap.add_argument("--dir", "--site", dest="dir", default=None, metavar="RUTA",
                    help="directorio a revisar (artefacto publicado); al pasarlo NO se revisa el árbol git "
                         "salvo que se agregue --con-arbol. --site es alias.")
    ap.add_argument("--con-arbol", action="store_true", help="con --dir, revisar además el árbol git")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--solo-arbol", action="store_true")
    g.add_argument("--solo-site", action="store_true")
    a = ap.parse_args(argv)
    res = []
    cuenta = Counter()
    site = Path(a.dir) if a.dir else ROOT / "site"
    if a.dir and not site.is_dir():
        print(f"ERROR: {site} no es un directorio", file=sys.stderr)
        return 2
    revisar_arbol = not a.solo_site and (not a.dir or a.con_arbol)
    if a.solo_arbol:
        revisar_arbol = True
    if revisar_arbol:
        res += revisar_archivos(archivos_arbol(), ROOT)
    if not a.solo_arbol and site.is_dir():
        fs = archivos_site(site)
        cuenta.update(f.suffix.lower().lstrip(".") for f in fs)
        res += [(f"[site] {r}", n, l) for r, n, l in revisar_archivos(fs, site, False)]
        pdfs = pdfs_site(site)
        cuenta["pdf"] += len(pdfs)
        res += [(f"[site] {r}", n, l) for r, n, l in revisar_pdfs(pdfs, site)]
    for r, n, l in res:
        print(f"{r}:{n}: {l[:200]}")
    if cuenta:
        print("revisados: " + ", ".join(f"{v} {k}" for k, v in sorted(cuenta.items(), key=lambda x: -x[1])))
    print(f"TOTAL: {len(res)} coincidencias fuera de las excepciones")
    return 1 if res else 0


if __name__ == "__main__":
    sys.exit(main())
