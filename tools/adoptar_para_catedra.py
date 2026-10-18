#!/usr/bin/env python3
"""Adoptar el material para la cátedra: reemplaza la firma del alumno por el membrete institucional.

Uso (desde cualquier directorio; las rutas se resuelven respecto a la raíz del repo):

    uv run python tools/adoptar_para_catedra.py --dry-run
    uv run python tools/adoptar_para_catedra.py
    uv run python tools/adoptar_para_catedra.py \
        --autor "Cátedra Sistemas de Coordenadas (CB104) · Agrimensura FIUBA" \
        --url-sitio "https://catedra-cb104.github.io/Sistemas-de-Coordenadas/"

Qué toca (y nada más):

  1. unidades/*.py (las lecciones y PLANTILLA_leccion.py; no cb104.py ni _legacy/):
     la línea de firma bajo el H1 `**Sistemas de Coordenadas** · Agrimensura · FIUBA · <cola>`
     y, en el docstring inicial, `Sistemas de Coordenadas (CB104) · Agrimensura · FIUBA · <cola>.`
     La cola se reemplaza por --autor. Las semillas `default_rng(56798)` no se tocan.
  2. tools/build.py: en la constante PIE, el tramo entre `(Agrimensura, FIUBA), ` y el primer `. ` pasa a `publicado por <autor>`.
  3. LaTeX: pdfauthor={...} y \\newcommand/\\providecommand{\\portadaAutor}{...} en
     apunte/Apunte_Sistemas_de_Coordenadas.tex, apunte/portada/portada-standalone.tex y
     apunte/portada/portada-tikz.tex. Se escapan & % # _ del autor para LaTeX.
  4. Con --url-sitio: la URL del sitio publicado en README.md, INSTRUCTIVO_DE_USO.md y
     CURSO_INTERACTIVO.md, y la línea `\\newcommand{\\sitioURL}{...}` (sin barra final) de
     apunte/apunte-formato.sty. Si el .sty todavía no tiene esa línea, se avisa y se sigue.

Es idempotente: una segunda corrida con los mismos argumentos no cambia nada.
Sólo stdlib. Sale con 0. Después de correrlo hay que regenerar el sitio y el apunte
(los comandos se imprimen al final).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

AUTOR_DEFAULT = "Cátedra Sistemas de Coordenadas (CB104) · Agrimensura FIUBA"
URL_ACTUAL = "https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/"

ARCHIVOS_LATEX = (
    "apunte/Apunte_Sistemas_de_Coordenadas.tex",
    "apunte/portada/portada-standalone.tex",
    "apunte/portada/portada-tikz.tex",
)
ARCHIVOS_URL = ("README.md", "INSTRUCTIVO_DE_USO.md", "CURSO_INTERACTIVO.md")
ARCHIVO_STY = "apunte/apunte-formato.sty"
# `\newcommand{\sitioURL}{https://...}` del .sty: la URL va SIN barra final (el .tex le agrega las rutas).
RE_SITIOURL = re.compile(r"^\\newcommand\{\\sitioURL\}\{[^}]*\}", re.M)

# Firma bajo el H1 de cada lección (markdown dentro de mo.md).
RE_FIRMA = re.compile(r"^(\s*\*\*Sistemas de Coordenadas\*\* · Agrimensura · FIUBA · ).*$", re.M)
# Mención en el docstring inicial (hoy sólo 01a_punto_quieto.py).
RE_DOCSTRING = re.compile(r"^(Sistemas de Coordenadas \(CB104\) · Agrimensura · FIUBA · ).*\.$", re.M)
# Tramo de autoría dentro de la constante PIE de build.py.
RE_PIE = re.compile(r"^(PIE = \(.*?\(Agrimensura, FIUBA\), ).*?(?=\. )", re.M)
# Valor con llaves balanceadas de un nivel (admite \textperiodcentered{} adentro).
_LLAVES = r"\{(?:[^{}]|\{[^{}]*\})*\}"
RE_PDFAUTHOR = re.compile(r"(pdfauthor=)" + _LLAVES)
RE_PORTADA_AUTOR = re.compile(r"(\\(?:newcommand|providecommand)\{\\portadaAutor\})" + _LLAVES)


def _sustituir(regex: re.Pattern, texto: str, armar: callable) -> tuple[str, int]:
    """Aplica `armar(match) -> str` a cada match; cuenta sólo los que cambian algo."""
    n = 0

    def repl(m: re.Match) -> str:
        nonlocal n
        nuevo = armar(m)
        if nuevo != m.group(0):
            n += 1
        return nuevo

    return regex.sub(repl, texto), n


def escapar_latex(s: str) -> str:
    return re.sub(r"([&%#_])", r"\\\1", s)


def adoptar_leccion(texto: str, autor: str) -> tuple[str, int]:
    texto, n1 = _sustituir(RE_FIRMA, texto, lambda m: m.group(1) + autor)
    texto, n2 = _sustituir(RE_DOCSTRING, texto, lambda m: m.group(1) + autor + ".")
    return texto, n1 + n2


def adoptar_build(texto: str, autor: str) -> tuple[str, int]:
    return _sustituir(RE_PIE, texto, lambda m: m.group(1) + "publicado por " + autor)


def adoptar_latex(texto: str, autor: str) -> tuple[str, int]:
    valor = "{" + escapar_latex(autor) + "}"
    texto, n1 = _sustituir(RE_PDFAUTHOR, texto, lambda m: m.group(1) + valor)
    texto, n2 = _sustituir(RE_PORTADA_AUTOR, texto, lambda m: m.group(1) + valor)
    return texto, n1 + n2


def adoptar_url(texto: str, url_nueva: str) -> tuple[str, int]:
    if url_nueva == URL_ACTUAL:
        return texto, 0
    n = texto.count(URL_ACTUAL)
    return texto.replace(URL_ACTUAL, url_nueva), n


def adoptar_sty(texto: str, url_nueva: str) -> tuple[str, int]:
    """Reescribe `\\newcommand{\\sitioURL}{...}` con la URL nueva sin barra final; si no está, avisa y no toca nada."""
    if not RE_SITIOURL.search(texto):
        print(f"  [aviso] {ARCHIVO_STY}: no tiene la línea \\newcommand{{\\sitioURL}}{{...}}; se omite (agregarla y volver a correr)")
        return texto, 0
    nueva = r"\newcommand{\sitioURL}{" + url_nueva.rstrip("/") + "}"
    return _sustituir(RE_SITIOURL, texto, lambda m: nueva)


def lecciones() -> list[Path]:
    return sorted(p for p in (RAIZ / "unidades").glob("*.py") if p.name != "cb104.py")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--autor", default=AUTOR_DEFAULT, help=f"membrete que reemplaza al alumno (default: {AUTOR_DEFAULT!r})")
    ap.add_argument("--url-sitio", default=None,
                    help="URL nueva del sitio publicado (reemplaza la de README, INSTRUCTIVO_DE_USO y CURSO_INTERACTIVO, "
                         "y \\sitioURL en apunte/apunte-formato.sty, sin barra final)")
    ap.add_argument("--dry-run", action="store_true", help="mostrar qué cambiaría sin escribir nada")
    args = ap.parse_args(argv)

    autor = args.autor.strip()
    url = args.url_sitio.strip().rstrip("/") + "/" if args.url_sitio else None

    # (ruta, función) en el orden en que se reportan.
    tareas: list[tuple[Path, callable]] = []
    tareas += [(p, lambda t, a=autor: adoptar_leccion(t, a)) for p in lecciones()]
    tareas.append((RAIZ / "tools/build.py", lambda t, a=autor: adoptar_build(t, a)))
    tareas += [(RAIZ / rel, lambda t, a=autor: adoptar_latex(t, a)) for rel in ARCHIVOS_LATEX]
    if url:
        tareas += [(RAIZ / rel, lambda t, u=url: adoptar_url(t, u)) for rel in ARCHIVOS_URL]
        tareas.append((RAIZ / ARCHIVO_STY, lambda t, u=url: adoptar_sty(t, u)))

    modo = "DRY-RUN (no se escribe nada)" if args.dry_run else "aplicando"
    print(f"adoptar_para_catedra · raíz: {RAIZ} · {modo}")
    print(f"  autor: {autor}")
    if url:
        print(f"  url-sitio: {url}")

    total = 0
    tocados = 0
    for ruta, fn in tareas:
        rel = ruta.relative_to(RAIZ)
        if not ruta.exists():
            print(f"  [falta] {rel}: no existe, se omite")
            continue
        original = ruta.read_text(encoding="utf-8")
        nuevo, n = fn(original)
        if n == 0 or nuevo == original:
            continue
        total += n
        tocados += 1
        print(f"  {rel}: {n} reemplazo{'s' if n != 1 else ''}")
        if not args.dry_run:
            ruta.write_text(nuevo, encoding="utf-8")

    if total == 0:
        print("\nResumen: sin cambios (ya está adoptado con estos valores).")
    else:
        verbo = "cambiaría" if args.dry_run else "cambió"
        print(f"\nResumen: {total} reemplazos en {tocados} archivos ({verbo}).")
    if total and not args.dry_run:
        print("\nPara regenerar el sitio y el apunte:")
        print("  uv run python tools/build.py")
        print("  cd apunte && lualatex -interaction=nonstopmode Apunte_Sistemas_de_Coordenadas.tex   # tres pasadas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
