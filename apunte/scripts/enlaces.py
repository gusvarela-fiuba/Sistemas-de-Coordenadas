#!/usr/bin/env python3
"""Verifica los enlaces a unidades y animaciones en los .tex incluidos por el maestro.

Uso (desde la raíz del repo): uv run python apunte/scripts/enlaces.py
Exit code 1 si hay enlaces rotos. Solo biblioteca estándar.
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APUNTE = ROOT / "apunte"
MAESTRO = APUNTE / "Apunte_Sistemas_de_Coordenadas.tex"
UNI = re.compile(r"\\(linkUnidadId|linkUnidad|unidadInteractiva)\{([^}]*)\}")
ANI = re.compile(r"\\(linkAnimacion|animacion)\{([^}]*)\}")


def sin_comentarios(txt):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in txt.split("\n"))


def archivos():
    maestro = sin_comentarios(MAESTRO.read_text(encoding="utf-8"))
    out = []
    for i in re.findall(r"\\input\{(contenido/[^}]+)\}", maestro):
        p = APUNTE / (i if i.endswith(".tex") else i + ".tex")
        if p.exists():
            out.append(p)
    return out


def analizar(path):
    txt = sin_comentarios(path.read_text(encoding="utf-8", errors="ignore"))
    uni = [(k, i.replace("\\_", "_")) for k, i in UNI.findall(txt)]
    ani = [(k, n.replace("\\_", "_")) for k, n in ANI.findall(txt)]
    rotos = [f"unidades/{i}.py" for _, i in uni if not (ROOT / "unidades" / f"{i}.py").exists()]
    rotos += [f"animaciones/{n}.mp4" for _, n in ani if not (ROOT / "animaciones" / f"{n}.mp4").exists()]
    return dict(archivo=str(path.relative_to(APUNTE)), unidades=len(uni), animaciones=len(ani),
                recuadros=sum(k == "unidadInteractiva" for k, _ in uni), rotos=rotos)


def analizar_todo():
    return [analizar(p) for p in archivos()]


def main():
    rows = analizar_todo()
    for r in rows:
        if r["unidades"] or r["animaciones"] or r["recuadros"] or r["rotos"]:
            print(f"{r['archivo']}: unidades={r['unidades']} animaciones={r['animaciones']} "
                  f"recuadros={r['recuadros']} rotos={len(r['rotos'])}")
            for b in r["rotos"]:
                print(f"  ROTO: {b}")
    rotos = [b for r in rows for b in r["rotos"]]
    print(f"TOTAL: unidades={sum(r['unidades'] for r in rows)} animaciones={sum(r['animaciones'] for r in rows)} "
          f"recuadros={sum(r['recuadros'] for r in rows)} rotos={len(rotos)}")
    return 1 if rotos else 0


if __name__ == "__main__":
    sys.exit(main())
