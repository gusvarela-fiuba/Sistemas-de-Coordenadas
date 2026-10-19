#!/usr/bin/env python3
"""Extrae el fragmento de cada comprobación de apunte/demostraciones/ a apunte/generado/fragmentos/.

Uso (desde la raíz del repo): uv run python apunte/scripts/extraer_fragmentos.py
Lo corre también latexmk al arrancar (apunte/.latexmkrc).

Por cada función `test_<etiqueta>` de apunte/demostraciones/*.py escribe
apunte/generado/fragmentos/<archivo>.tex, donde <archivo> es la etiqueta LaTeX con «:» → «_»
(prop:det-factor → prop_det-factor.tex). El .tex contiene:
  \\comprobacionDatos{<TIPO>}{<casos>}{<módulo>}{<línea>}   (casos vacío salvo NUMERICA)
  \\begin{lstlisting} … \\end{lstlisting}                   (las líneas entre los marcadores)
  \\comprobacionPie
El aspecto lo define \\comprobacion en apunte/apunte-formato.sty.

Falla (exit 1) si: falta el docstring o no tiene tres líneas (etiqueta, tipo, qué verifica); el
tipo no es SIMBOLICA, NUMERICA o CONTRAEJEMPLO; la etiqueta del docstring no corresponde al
nombre de la función; una NUMERICA no fija `CASOS = <n>` con n ≥ 200; faltan los marcadores o el
fragmento tiene menos de 3 o más de 8 líneas; dos funciones usan la misma etiqueta.
Borra los .tex de etiquetas que ya no existen. Determinista: misma entrada, mismos bytes.
"""
import ast, re, sys, textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEMOS = ROOT / "apunte" / "demostraciones"
SALIDA = ROOT / "apunte" / "generado" / "fragmentos"
TIPOS = ("SIMBOLICA", "NUMERICA", "CONTRAEJEMPLO")
MIN_LINEAS, MAX_LINEAS, MIN_CASOS = 3, 8, 200
INICIO = re.compile(r"^\s*# >>> fragmento\s*$")
FIN = re.compile(r"^\s*# <<< fragmento\s*$")


def nombre_funcion(etiqueta):
    """prop:det-factor → test_prop_det_factor."""
    return "test_" + re.sub(r"[:\-]", "_", etiqueta)


def archivo_tex(etiqueta):
    """prop:det-factor → prop_det-factor (nombre del .tex, sin extensión)."""
    return etiqueta.replace(":", "_")


def _casos(fn):
    for nodo in ast.walk(fn):
        if (isinstance(nodo, ast.Assign) and len(nodo.targets) == 1 and isinstance(nodo.targets[0], ast.Name)
                and nodo.targets[0].id == "CASOS" and isinstance(nodo.value, ast.Constant)
                and isinstance(nodo.value.value, int)):
            return nodo.value.value
    return None


def pruebas(errores=None):
    """Lista de dicts (etiqueta, tipo, que, casos, modulo, linea, fragmento, funcion, ruta)."""
    errores = [] if errores is None else errores
    out = []
    for ruta in sorted(DEMOS.glob("*.py")):
        if ruta.name == "conftest.py":
            continue
        fuente = ruta.read_text(encoding="utf-8")
        lineas = fuente.split("\n")
        rel = ruta.relative_to(ROOT)
        cuerpo_mod = ast.parse(fuente).body
        for k, fn in enumerate(cuerpo_mod):
            if not (isinstance(fn, ast.FunctionDef) and fn.name.startswith("test_")):
                continue
            donde = f"{rel}:{fn.lineno} {fn.name}"
            doc = ast.get_docstring(fn)
            partes = [l.strip() for l in doc.strip().split("\n")] if doc else []
            if len(partes) != 3 or not all(partes):
                errores.append(f"{donde}: el docstring debe tener tres líneas (etiqueta, tipo, qué verifica)")
                continue
            etiqueta, tipo, que = partes
            if tipo not in TIPOS:
                errores.append(f"{donde}: tipo «{tipo}» no es uno de {', '.join(TIPOS)}")
                continue
            if nombre_funcion(etiqueta) != fn.name:
                errores.append(f"{donde}: la etiqueta «{etiqueta}» pide la función {nombre_funcion(etiqueta)}")
                continue
            casos = _casos(fn)
            if tipo == "NUMERICA" and (casos is None or casos < MIN_CASOS):
                errores.append(f"{donde}: una NUMERICA fija CASOS = n con n ≥ {MIN_CASOS} (encontrado: {casos})")
                continue
            # hasta el nodo siguiente del módulo: el marcador final es un comentario y queda fuera de end_lineno
            hasta = cuerpo_mod[k + 1].lineno - 1 if k + 1 < len(cuerpo_mod) else len(lineas)
            cuerpo = range(fn.lineno - 1, hasta)
            ini = [i for i in cuerpo if INICIO.match(lineas[i])]
            fin = [i for i in cuerpo if FIN.match(lineas[i])]
            if len(ini) != 1 or len(fin) != 1 or fin[0] <= ini[0]:
                errores.append(f"{donde}: hace falta un par «# >>> fragmento» / «# <<< fragmento»")
                continue
            frag = lineas[ini[0] + 1:fin[0]]
            n = sum(1 for l in frag if l.strip())
            if not MIN_LINEAS <= n <= MAX_LINEAS or len(frag) > MAX_LINEAS:
                errores.append(f"{donde}: el fragmento tiene {len(frag)} líneas; van de {MIN_LINEAS} a {MAX_LINEAS}")
                continue
            out.append(dict(etiqueta=etiqueta, tipo=tipo, que=que, casos=casos if tipo == "NUMERICA" else None,
                            modulo=ruta.stem, linea=ini[0] + 2, fragmento=textwrap.dedent("\n".join(frag)),
                            funcion=fn.name, ruta=str(rel)))
    vistas = {}
    for p in out:
        if p["etiqueta"] in vistas:
            errores.append(f"etiqueta repetida «{p['etiqueta']}»: {vistas[p['etiqueta']]} y {p['ruta']}")
        vistas[p["etiqueta"]] = p["ruta"]
    return out


def tex(p):
    if "\\end{lstlisting}" in p["fragmento"]:
        raise ValueError(f"{p['ruta']}: el fragmento no puede contener \\end{{lstlisting}}")
    return ("% Generado por apunte/scripts/extraer_fragmentos.py a partir de "
            f"{p['ruta']} ({p['funcion']}). No editar.\n"
            f"\\comprobacionDatos{{{p['tipo']}}}{{{p['casos'] or ''}}}{{{p['modulo']}}}{{{p['linea']}}}%\n"
            "\\begin{lstlisting}\n" + p["fragmento"].rstrip() + "\n\\end{lstlisting}\n"
            "\\comprobacionPie\n")


def main():
    errores = []
    ps = pruebas(errores)
    if errores:
        for e in errores:
            print("ERROR", e, file=sys.stderr)
        sys.exit(1)
    SALIDA.mkdir(parents=True, exist_ok=True)
    nuevos = {archivo_tex(p["etiqueta"]) + ".tex": tex(p) for p in ps}
    cambios = 0
    for nombre, contenido in sorted(nuevos.items()):
        f = SALIDA / nombre
        if not f.exists() or f.read_text(encoding="utf-8") != contenido:
            f.write_text(contenido, encoding="utf-8")
            cambios += 1
    for f in sorted(SALIDA.glob("*.tex")):
        if f.name not in nuevos:
            f.unlink()
            cambios += 1
    print(f"extraer_fragmentos: {len(nuevos)} fragmentos en {SALIDA.relative_to(ROOT)} ({cambios} cambios)")


if __name__ == "__main__":
    main()
