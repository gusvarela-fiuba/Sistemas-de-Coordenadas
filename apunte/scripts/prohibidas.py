#!/usr/bin/env python3
"""Patrón único de menciones prohibidas y chequeo del árbol versionado y del sitio generado.

Uso (desde la raíz del repo):
  uv run python apunte/scripts/prohibidas.py [--dir RUTA | --site RUTA] [--solo-arbol | --solo-site]
  --dir RUTA revisa SÓLO ese directorio (artefacto publicado), sin el árbol git, e incluye el
  texto de los *.pdf vía `pdftotext -layout` (requerido; si falta, falla).
Imprime `ruta:línea: texto` por cada coincidencia fuera de EXCEPCIONES.
Exit 1 si hay alguna. Solo biblioteca estándar.
"""
import argparse, re, shutil, subprocess, sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PATRON = re.compile(r"profesor|docente|clavijo|resumen de clase|cursada|en clase|dictad|palabras del|pizarr|campus|anticipad|pendiente de validar|validación pendiente|2C2026|transcripci|procedencia|CC-BY|CC BY|padr[oó]n|56798|donaci|licencia|cátedra del|alumno de|Dropbox|/Users/", re.I)

# (ruta relativa a la raíz, None = todo el archivo | fragmento literal que debe estar en la línea)
EXCEPCIONES = [
    # Ahí se declara la donación y las condiciones de uso; sólo vive en el repo.
    ("NOTA_DE_DONACION.md", None),
    # Sección «Cómo citar»: enlace a la nota de donación.
    ("README.md", "NOTA_DE_DONACION.md"),
    # Licencia de un dato externo (Copernicus DEM).
    ("datos/dem_copernicus/README.md", "Licencia: Copernicus DEM licence"),
    # El patrón mismo.
    ("apunte/scripts/prohibidas.py", None),
]

EXT_SITE = {".html", ".md", ".xml", ".js", ".py", ".txt", ".yaml", ".yml", ".json", ".css"}


def coincidencias_en_texto(texto):
    return [(i, l) for i, l in enumerate(texto.split("\n"), 1) if PATRON.search(l)]


def permitida(ruta_rel, linea):
    ruta_rel = str(ruta_rel)
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


def revisar_archivos(rutas, raiz):
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
            if not permitida(rel, l):
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
                if not permitida(rel, l):
                    out.append((f"{rel}:pág {pag}", n, l.strip()))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Búsqueda de menciones prohibidas. Sin opciones: árbol git + site/. "
                                 "Con --dir/--site RUTA: sólo ese directorio (más PDF), sin el árbol git.")
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
        res += [(f"[site] {r}", n, l) for r, n, l in revisar_archivos(fs, site)]
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
