#!/usr/bin/env python3
"""Genera apunte/ESTADO.md: inventario por archivo de lo que incluye el maestro.

Uso (desde la raíz del repo): uv run python apunte/scripts/estado.py [--md RUTA]
Solo biblioteca estándar.
"""
import argparse, datetime, glob, re, subprocess, unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
APUNTE = ROOT / "apunte"
MAESTRO = APUNTE / "Apunte_Sistemas_de_Coordenadas.tex"
PROHIB = re.compile(r"profesor|clavijo|resumen de clase|cursada|en clase|dictad|palabras del|pizarr|campus|donaci|licencia", re.I)
MOLDE = ["La idea", "Construcciones, cuentas y ejemplos", "En profundidad"]


def norm(s):
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode().lower()


def sin_comentarios(txt):
    return "\n".join(re.sub(r"(?<!\\)%.*", "", l) for l in txt.split("\n"))


def titulo(m):
    """Extrae el argumento entre llaves balanceadas desde la posición m."""
    i = m
    while i < len(m_txt) and m_txt[i] != "{":
        i += 1
    d, j = 0, i
    while j < len(m_txt):
        d += m_txt[j] == "{"
        d -= m_txt[j] == "}"
        j += 1
        if d == 0:
            break
    return m_txt[i + 1:j - 1]


def cap_titulo(txt):
    global m_txt
    m_txt = txt
    for pat in (r"\\chapter\*?(?:\[[^\]]*\])?", r"\\capituloComplemento\b(?:\[[^\]]*\])?", r"\\capituloPreliminar\b(?:\[[^\]]*\])?", r"\\section\*?(?:\[[^\]]*\])?"):
        m = re.search(pat, txt)
        if m:
            k = m.group(0).split("[")[0]
            t = titulo(m.end())
            t = re.sub(r"\s+", " ", t).strip()
            return (k.lstrip("\\") + ": " + t)[:60]
    return "-"


def analizar(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    txt = sin_comentarios(raw)
    c = lambda p: len(re.findall(p, txt))
    secs = re.findall(r"\\(?:section|subsection)\*?(?:\[[^\]]*\])?\{((?:[^{}]|\{[^{}]*\})*)\}", txt)
    secs_n = [re.sub(r"\s*\([^)]*\)\s*$", "", re.sub(r"\s+", " ", s)).strip() for s in secs]
    d = dict(
        archivo=str(path.relative_to(APUNTE)),
        cap=cap_titulo(txt),
        lineas=sum(1 for l in raw.split("\n") if l.strip()),
        fig=c(r"\\begin\{tikzpicture\}") + c(r"\\includegraphics"),
        ej=c(r"\\begin\{ejemplo\}"),
        dpt=c(r"\\begin\{definicion\}") + c(r"\\begin\{proposicion\}") + c(r"\\begin\{teorema\}"),
        dem=c(r"\\begin\{demostracion\}"),
        ejer=c(r"\\begin\{ejercicio\}"),
        sol=c(r"\\solucion\{"),
        sim=c(r"\\linkUnidadId") + len(re.findall(r"\\linkUnidad(?!Id)", txt)) + c(r"\\href\{\\sitioURL") + c(r"\\urlsitio"),
        aplic="sí" if any("aplicacion" in norm(s) for s in secs) else "no",
        prohib=sum(1 for l in raw.split("\n") if PROHIB.search(l)),
    )
    n = sum(1 for m in MOLDE if m in secs_n)
    d["molde"] = "sí" if n == 3 else ("parcial" if n else "no")
    falta = []
    if d["ej"] < 2: falta.append("ejemplos<2")
    if d["fig"] < 3: falta.append("figuras<3")
    if d["sol"] < 4: falta.append("soluciones<4")
    if d["aplic"] != "sí": falta.append("aplicación")
    if d["sim"] < 2: falta.append("simulaciones<2")
    if d["prohib"]: falta.append("prohibidas")
    d["cumple"] = "sí" if not falta else "no"
    d["falta"] = ", ".join(falta)
    return d


COLS = [("Archivo", "archivo"), ("Capítulo", "cap"), ("Líneas", "lineas"), ("Fig", "fig"), ("Ej", "ej"),
        ("Def+Prop+Teo", "dpt"), ("Dem", "dem"), ("Ejerc", "ejer"), ("Con sol", "sol"), ("Sim", "sim"),
        ("Aplic", "aplic"), ("Molde", "molde"), ("Prohib", "prohib"), ("Cumple", "cumple"), ("Falta", "falta")]


def tabla(rows):
    out = ["| " + " | ".join(h for h, _ in COLS) + " |", "|" + "---|" * len(COLS)]
    for r in rows:
        out.append("| " + " | ".join(str(r[k]).replace("|", "/") for _, k in COLS) + " |")
    num = [k for _, k in COLS if isinstance(rows[0][k], int)] if rows else []
    tot = {k: sum(r[k] for r in rows) for k in num}
    out.append("| **Total** | | " + " | ".join(str(tot.get(k, "")) if k in tot else "" for _, k in COLS[2:]) + " |")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", default=str(APUNTE / "ESTADO.md"))
    a = ap.parse_args()
    maestro = sin_comentarios(MAESTRO.read_text(encoding="utf-8"))
    ins = re.findall(r"\\input\{(contenido/[^}]+)\}", maestro)
    cont = []
    for i in ins:
        p = APUNTE / (i if i.endswith(".tex") else i + ".tex")
        if p.exists():
            cont.append(analizar(p))
    prep = [analizar(Path(p)) for p in sorted(glob.glob(str(APUNTE / "preparacion" / "*.tex")))]
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    pags = "n/d"
    pdfs = sorted(glob.glob("/tmp/build_A/*.pdf")) or glob.glob(str(ROOT / "site" / "apunte.pdf"))
    if pdfs:
        try:
            o = subprocess.run(["pdfinfo", pdfs[0]], capture_output=True, text=True).stdout
            pags = re.search(r"Pages:\s+(\d+)", o).group(1) + f" ({pdfs[0]})"
        except Exception:
            pass
    md = ["# Estado del apunte", "", "Generado por `apunte/scripts/estado.py`. No editar a mano.", "",
          "Mínimo: Ejemplos ≥ 2, Figuras ≥ 3, Ejercicios con solución ≥ 4, Aplicación topográfica, Simulaciones ≥ 2, Prohibidas = 0.", "",
          "## Archivos incluidos por el maestro (en orden)", "", tabla(cont), "",
          "## Preparación (no incluidos en el maestro)", "", tabla(prep) if prep else "(ninguno)", "",
          f"- Fecha: {datetime.date.today().isoformat()}", f"- HEAD: {head}", f"- Páginas del último PDF: {pags}",
          f"- Archivos que cumplen el mínimo: {sum(r['cumple']=='sí' for r in cont)} de {len(cont)}", ""]
    Path(a.md).write_text("\n".join(md), encoding="utf-8")
    print(f"escrito {a.md}")


if __name__ == "__main__":
    main()
