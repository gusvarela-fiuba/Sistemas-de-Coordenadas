#!/usr/bin/env python3
"""Escribe apunte/numeracion.json: número, rótulo y título de cada \\label{cap:X} del apunte.

Uso (desde la raíz del repo), después de compilar el apunte (latexmk deja el .aux):
    uv run python apunte/scripts/numeracion.py

El número y el tipo salen del .aux (\\newlabel{cap:X}{{NUM}{PAG}{...}{tipo.NUM}...}); el título, del
.tex (misma regla que capitulos_apunte() de tools/build.py). El JSON se versiona: el runner de
GitHub Actions no compila LaTeX y build.py lo lee. Solo biblioteca estándar.
"""
import json, re, sys
from pathlib import Path

APUNTE = Path(__file__).resolve().parents[1]
MAESTRO = APUNTE / "Apunte_Sistemas_de_Coordenadas.tex"
AUX = MAESTRO.with_suffix(".aux")
SALIDA = APUNTE / "numeracion.json"
RE_ENCABEZADO = re.compile(r"\\(?:chapter|section|subsection|capituloComplemento)\*?(?:\[[^\]]*\])?\{([^}]*)\}")
RE_LABEL_AUX = re.compile(r"\\newlabel\{cap:([^}]+)\}\{\{([^}]*)\}\{[^}]*\}\{.*?\}\{([^}]*)\}")


def titulos() -> dict[str, str]:
    maestro = MAESTRO.read_text(encoding="utf-8")
    archivos = [MAESTRO] + [APUNTE / f"{m}.tex" for m in re.findall(r"^\\input\{(contenido/[^}]+)\}", maestro, re.M)]
    res: dict[str, str] = {}
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


def rotulo(numero: str, tipo: str) -> str:
    if tipo.startswith("chapter"):
        return "Complemento" if numero.startswith("C") else "Capítulo"
    if numero.startswith("A") and numero.count(".") <= 1:
        return "Apéndice"  # «A» (el apéndice) o «A.n» (sus secciones)
    return "Sección"


def main() -> int:
    if not AUX.exists():
        print(f"ERROR: falta {AUX.name}; compilar el apunte con latexmk -lualatex primero", file=sys.stderr)
        return 1
    tit = titulos()
    res: dict[str, dict[str, str]] = {}
    for linea in AUX.read_text(encoding="utf-8").split("\n"):
        m = RE_LABEL_AUX.match(linea)
        if not m:
            continue
        clave, numero, tipo = m.groups()
        if clave not in tit:
            print(f"AVISO: cap:{clave} está en el .aux pero no en los .tex", file=sys.stderr)
            continue
        res.setdefault(f"cap:{clave}", {"numero": numero, "rotulo": rotulo(numero, tipo), "titulo": tit[clave]})
    faltan = sorted(set(tit) - {k[4:] for k in res})
    if faltan:
        print(f"ERROR: labels de los .tex sin número en el .aux: {faltan}", file=sys.stderr)
        return 1
    SALIDA.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(res)} claves en {SALIDA.relative_to(APUNTE.parent)}")
    for k, v in res.items():
        print(f"  {k}: {v['rotulo']} {v['numero']}. {v['titulo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
