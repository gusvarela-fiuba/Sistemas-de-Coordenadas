#!/usr/bin/env python3
"""Genera apunte/ESTADO.md: inventario por archivo de lo que incluye el maestro.

Uso (desde la raíz del repo): uv run python apunte/scripts/estado.py [--md RUTA]
Solo biblioteca estándar.
"""
import argparse, datetime, glob, re, subprocess, sys, unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enlaces
import estilo
import verificar_comprobaciones as vc
from prohibidas import PATRON, permitida

ROOT = Path(__file__).resolve().parents[2]
APUNTE = ROOT / "apunte"
MAESTRO = APUNTE / "Apunte_Sistemas_de_Coordenadas.tex"
MOLDE = ["La idea", "Construcciones, cuentas y ejemplos", "En profundidad"]
_ESTILO = None  # {archivo: total de hallazgos de estilo.py}
_TIPOS = None  # {etiqueta: SIMBOLICA|NUMERICA|CONTRAEJEMPLO}, de los docstrings de apunte/demostraciones/


def comprobaciones(path):
    """(resultados, con \\comprobacion, tipo dominante S/N/C o «—») de un .tex."""
    global _TIPOS
    if _TIPOS is None:
        _TIPOS = vc.tipos_por_etiqueta()
    rs = vc.resultados(path)
    tipos = [_TIPOS[r["etiqueta"]] for r in rs if r["etiqueta"] in _TIPOS]
    dom = max(("SIMBOLICA", "NUMERICA", "CONTRAEJEMPLO"), key=tipos.count)[0] if tipos else "—"
    return len(rs), sum(r["comprobacion"] for r in rs), dom


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


def estilo_total(path):
    global _ESTILO
    if _ESTILO is None:
        _ESTILO = estilo.totales_por_archivo()
    return _ESTILO.get(str(path.relative_to(APUNTE)), 0)


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
        sim=c(r"\\unidadInteractiva\{") + c(r"\\linkUnidadId") + len(re.findall(r"\\linkUnidad(?!Id)", txt)) + c(r"\\href\{\\sitioURL") + c(r"\\urlsitio"),
        aplic="sí" if any("aplicacion" in norm(s) for s in secs) else "no",
        recuadros=c(r"\\unidadInteractiva\{"),
        rotos=len(enlaces.analizar(path)["rotos"]),
        **dict(zip(("res", "conc", "tcomp"), comprobaciones(path))),
        prohib=sum(1 for l in raw.split("\n") if PATRON.search(l) and not permitida(str(path.relative_to(ROOT)), l)),
        estilo=estilo_total(path),
    )
    n = sum(1 for m in MOLDE if m in secs_n)
    d["molde"] = "sí" if n == 3 else ("parcial" if n else "no")
    nombre = path.name
    d["tipo"] = ("cap0" if re.match(r"00-", nombre) else "cap" if re.match(r"(0[1-9]|1[0-5])-", nombre)
                 else "comp" if re.match(r"c\d", nombre) else "ap" if re.match(r"ap\d", nombre) else "otro")
    falta = []
    if d["tipo"] == "cap0":
        secs_l = [norm(s) for s in secs]
        for etiqueta, claves in (("orientación (cómo usar)", ("como usar",)), ("notación", ("notacion",)),
                                 ("leyenda de símbolos", ("simbolos", "leyenda")), ("cómo usar las unidades", ("unidades",)),
                                 ("repaso", ("repaso",))):
            if not any(k in s for s in secs_l for k in claves):
                falta.append(etiqueta)
        m = re.search(r"\\section\*?(?:\[[^\]]*\])?\{[^{}]*[Rr]epaso", txt)
        if m:
            fin = re.search(r"\\section\b", txt[m.end():])
            tr = txt[m.start(): m.end() + (fin.start() if fin else len(txt))]
            if len(re.findall(r"\\begin\{ejemplo\}", tr)) < 2:
                falta.append("repaso con ejemplos<2")
        elif "repaso" not in falta:
            falta.append("repaso")
        if d["prohib"]: falta.append("prohibidas")
    elif d["tipo"] == "ap":
        if d["prohib"]: falta.append("prohibidas")
    else:
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
        ("Def+Prop+Teo", "dpt"), ("Dem", "dem"), ("Resultados", "res"), ("Con comprobación", "conc"), ("Tipo", "tcomp"), ("Ejerc", "ejer"), ("Con sol", "sol"), ("Sim", "sim"), ("Recuadros", "recuadros"), ("Enlaces rotos", "rotos"),
        ("Aplic", "aplic"), ("Molde", "molde"), ("Prohib", "prohib"), ("Estilo", "estilo"), ("Cumple", "cumple"), ("Falta", "falta")]


COLS_AP = [("Archivo", "archivo"), ("Capítulo", "cap"), ("Líneas", "lineas"), ("Fig", "fig"), ("Sim", "sim"),
           ("Resultados", "res"), ("Con comprobación", "conc"), ("Tipo", "tcomp"),
           ("Enlaces rotos", "rotos"), ("Prohib", "prohib"), ("Estilo", "estilo")]


def tabla(rows, COLS=COLS):
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
    caps = [r for r in cont if r["tipo"] in ("cap0", "cap")]
    comps = [r for r in cont if r["tipo"] == "comp"]
    aps = [r for r in cont if r["tipo"] == "ap"]
    otros = [r for r in cont if r["tipo"] == "otro"]
    prep = [analizar(Path(p)) for p in sorted(glob.glob(str(APUNTE / "preparacion" / "*.tex")))]
    enl = enlaces.analizar_todo()
    rotos = [b for r in enl for b in r['rotos']]
    head = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    pags = "n/d"
    pdfs = [p for p in (APUNTE / "Apunte_Sistemas_de_Coordenadas.pdf", ROOT / "site" / "apunte.pdf") if p.exists()]
    if pdfs:
        try:
            o = subprocess.run(["pdfinfo", str(pdfs[0])], capture_output=True, text=True).stdout
            p0 = pdfs[0].resolve()
            try:
                nombre = str(p0.relative_to(ROOT))
            except ValueError:
                nombre = p0.name
            pags = re.search(r"Pages:\s+(\d+)", o).group(1) + f" ({nombre})"
        except Exception:
            pass
    md = ["# Estado del apunte", "", "Generado por `apunte/scripts/estado.py`. No editar a mano.", "",
          "Mínimo: Ejemplos ≥ 2, Figuras ≥ 3, Ejercicios con solución ≥ 4, Aplicación topográfica, Simulaciones ≥ 2, Prohibidas = 0.", "",
          "Estilo: hallazgos de `apunte/scripts/estilo.py` (reglas en `apunte/ESTILO.md`); informativo, no entra en «Cumple».", "",
          "Capítulo 0: criterio propio (orientación, notación, leyenda de símbolos, uso de las unidades, repaso con ≥ 2 ejemplos).", "",
          "## Capítulos (0 a 15)", "", tabla(caps), "",
          "## Complementos (C1 a C4)", "", tabla(comps), "",
          "## Apéndices (sin molde)", "", tabla(aps, COLS_AP), "",
          *(["## Otros archivos", "", tabla(otros), ""] if otros else []),
          *(["## Preparación (no incluidos en el maestro)", "", tabla(prep), ""] if prep else []),
          "## Enlaces", "",
          f"- Total de enlaces a unidades: {sum(r['unidades'] for r in enl)}; a animaciones: {sum(r['animaciones'] for r in enl)}; recuadros: {sum(r['recuadros'] for r in enl)}",
          f"- Enlaces rotos: {len(rotos)}", *[f"  - {b}" for b in rotos], "",
          f"- Fecha: {datetime.date.today().isoformat()}", f"- HEAD: {head}", f"- Páginas del último PDF: {pags}",
          f"- Capítulos que cumplen el mínimo: {sum(r['cumple']=='sí' for r in caps if r['tipo']=='cap')} de {sum(r['tipo']=='cap' for r in caps)}",
          f"- Complementos que cumplen el mínimo: {sum(r['cumple']=='sí' for r in comps)} de {len(comps)}",
          f"- Resultados (proposición, teorema, lema, corolario) con comprobación: {sum(r['conc'] for r in cont)} de {sum(r['res'] for r in cont)}",
          "  (Tipo: dominante entre S = simbólica, N = numérica, C = contraejemplo; ver apunte/demostraciones/README.md)",
          f"- Capítulo 0 (criterio propio): {'cumple' if all(r['cumple']=='sí' for r in caps if r['tipo']=='cap0') else 'no cumple'}", ""]
    Path(a.md).write_text("\n".join(md), encoding="utf-8")
    print(f"escrito {a.md}")


if __name__ == "__main__":
    main()
