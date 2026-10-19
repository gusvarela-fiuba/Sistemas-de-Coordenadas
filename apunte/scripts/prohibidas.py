#!/usr/bin/env python3
"""Patrón único de menciones prohibidas y chequeo del árbol versionado y del sitio generado.

Uso (desde la raíz del repo):
  uv run python apunte/scripts/prohibidas.py [--site RUTA] [--solo-arbol | --solo-site]
Imprime `ruta:línea: texto` por cada coincidencia fuera de EXCEPCIONES.
Exit 1 si hay alguna. Solo biblioteca estándar.
"""
import argparse, re, subprocess, sys
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
        if rel[0] == "_build":
            continue
        if len(rel) >= 3 and rel[0] == "unidades" and "assets" in rel[2:-1]:
            continue
        out.append(p)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--site", default=str(ROOT / "site"))
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--solo-arbol", action="store_true")
    g.add_argument("--solo-site", action="store_true")
    a = ap.parse_args(argv)
    res = []
    if not a.solo_site:
        res += revisar_archivos(archivos_arbol(), ROOT)
    site = Path(a.site)
    if not a.solo_arbol and site.is_dir():
        res += [(f"[site] {r}", n, l) for r, n, l in revisar_archivos(archivos_site(site), site)]
    for r, n, l in res:
        print(f"{r}:{n}: {l[:200]}")
    print(f"TOTAL: {len(res)} coincidencias fuera de las excepciones")
    return 1 if res else 0


if __name__ == "__main__":
    sys.exit(main())
