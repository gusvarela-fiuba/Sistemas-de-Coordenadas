#!/usr/bin/env python3
"""Cobertura de las comprobaciones con código: qué resultados del apunte tienen la suya.

Uso (desde la raíz del repo): uv run python apunte/scripts/verificar_comprobaciones.py [--estricto]

Recorre los archivos de contenido/ que incluye el maestro y, por cada entorno proposicion,
teorema, lema o corolario, informa su etiqueta, si hay un \\comprobacion{<etiqueta>}{…} entre el
enunciado y las 40 líneas siguientes a su demostración (o al enunciado, si no la sigue una) y si
existe test_<etiqueta> en apunte/demostraciones/. Un resultado cuenta «con comprobación» si tiene
las dos cosas. Imprime una tabla y «N de M resultados con comprobación».
Sin --estricto siempre sale con 0; con --estricto, 1 si falta alguna (para CI con cobertura completa).
"""
import argparse, re, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from extraer_fragmentos import pruebas

ROOT = Path(__file__).resolve().parents[2]
APUNTE = ROOT / "apunte"
MAESTRO = APUNTE / "Apunte_Sistemas_de_Coordenadas.tex"
ENTORNOS = ("proposicion", "teorema", "lema", "corolario")
VENTANA = 40
BEGIN = re.compile(r"\\begin\{(" + "|".join(ENTORNOS) + r")\}")
LABEL = re.compile(r"\\label\{([^}]+)\}")


def sin_comentario(l):
    return re.sub(r"(?<!\\)%.*", "", l)


def archivos():
    """Archivos de contenido/ incluidos por el maestro, en orden."""
    txt = "\n".join(sin_comentario(l) for l in MAESTRO.read_text(encoding="utf-8").split("\n"))
    out = []
    for i in re.findall(r"\\input\{(contenido/[^}]+)\}", txt):
        p = APUNTE / (i if i.endswith(".tex") else i + ".tex")
        if p.exists():
            out.append(p)
    return out


def resultados(path):
    """Lista de dicts (entorno, etiqueta, linea, comprobacion) de un .tex."""
    L = [sin_comentario(l) for l in path.read_text(encoding="utf-8").split("\n")]
    out = []
    for i, l in enumerate(L):
        m = BEGIN.search(l)
        if not m:
            continue
        env = m.group(1)
        fin = next((j for j in range(i, len(L)) if f"\\end{{{env}}}" in L[j]), i)
        lab = next((LABEL.search(L[j]).group(1) for j in range(i, fin + 1) if LABEL.search(L[j])), None)
        ancla = fin
        k = fin + 1
        while k < len(L) and not L[k].strip():
            k += 1
        if k < len(L) and L[k].lstrip().startswith("\\begin{demostracion}"):
            ancla = next((j for j in range(k, len(L)) if "\\end{demostracion}" in L[j]), k)
        ventana = "\n".join(L[i:ancla + 1 + VENTANA])
        con = bool(lab) and re.search(r"\\comprobacion\{" + re.escape(lab) + r"\}", ventana) is not None
        out.append(dict(entorno=env, etiqueta=lab, linea=i + 1, comprobacion=con))
    return out


def tipos_por_etiqueta():
    """{etiqueta: tipo} leído de los docstrings de apunte/demostraciones/ (ignora los inválidos)."""
    return {p["etiqueta"]: p["tipo"] for p in pruebas([])}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--estricto", action="store_true", help="exit 1 si algún resultado no tiene comprobación")
    a = ap.parse_args()
    tipos = tipos_por_etiqueta()
    filas = []
    for p in archivos():
        for r in resultados(p):
            r["archivo"] = str(p.relative_to(APUNTE))
            r["prueba"] = tipos.get(r["etiqueta"])
            filas.append(r)
    ancho = max([len(r["etiqueta"] or "(sin etiqueta)") for r in filas] + [8])
    print(f"{'Archivo':<46} {'Línea':>5}  {'Entorno':<11} {'Etiqueta':<{ancho}}  {'\\comprobacion':<13}  Prueba")
    for r in filas:
        print(f"{r['archivo']:<46} {r['linea']:>5}  {r['entorno']:<11} {(r['etiqueta'] or '(sin etiqueta)'):<{ancho}}  "
              f"{'sí' if r['comprobacion'] else 'no':<13}  {r['prueba'] or 'no'}")
    n = sum(1 for r in filas if r["comprobacion"] and r["prueba"])
    print(f"\nCon \\comprobacion: {sum(r['comprobacion'] for r in filas)}; con prueba: {sum(bool(r['prueba']) for r in filas)}")
    print(f"{n} de {len(filas)} resultados con comprobación")
    if a.estricto and n < len(filas):
        sys.exit(1)


if __name__ == "__main__":
    main()
