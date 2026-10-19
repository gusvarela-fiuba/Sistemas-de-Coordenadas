#!/usr/bin/env python3
"""Control automático de la hoja de estilo (apunte/ESTILO.md) sobre los .tex del maestro.

Uso (desde la raíz del repo):
    uv run python apunte/scripts/estilo.py [--md RUTA] [--estricto]

Recorre los .tex que el maestro incluye con \\input (misma lógica que enlaces.py) y reporta, por
archivo, con línea y texto:
  1 tilde   «sólo» o demostrativo con tilde sin «% ambigüedad» en la línea
  2 comillas  `` o '' escritas a mano (fuera de lstlisting/verbatim y de la matemática)
  3 decimal número con punto decimal fuera de código, URL, comentarios y argumentos técnicos
  4 semejanza «semejanza» aplicada a matrices (matriz, C^{-1} o conjugad… a menos de 80 caracteres)
  5 es-decir  «es decir» más de una vez cada 100 líneas (cuenta el exceso)
  6 desarrollo  \\textbf{Desarrollo.} o párrafo que empieza con «Desarrollo.»
  7 label-num  \\label{cap:NN} numérica
  8 def-dup   \\begin{definicion}[Título] con el mismo título en dos archivos
Salida: tabla por archivo con el conteo por chequeo y el total, y la lista detallada.

Además, tres contadores de advertencia (ESTILO.md §8, «Voz para el aula»); no entran en el total ni
en --estricto y se muestran en una segunda tabla por archivo:
  9 términos de campo  apariciones de TERMINOS_CAMPO (acimut, cota, faja, ajuste, mínimos cuadrados…)
    fuera de comentarios y de código, y su densidad cada 100 líneas
  10 instrumentos  estación total, nivel óptico, GNSS, limbo, teodolito, distanciómetro (se listan
    con archivo y línea al final del detalle)
  11 preguntas en «La idea»  líneas con «?» o que empiezan con Imaginá, Pensá, Probá, Suponé, Tomá o
    Mirá, dentro de la primera \\section{La idea} (— si el archivo no la tiene)
Objetivo (solo capítulos 00 a 11; en el resto «—»): menos de 4 términos cada 100 líneas, cero
instrumentos y al menos una pregunta o experimento mental en «La idea».
Con --md escribe la misma salida en RUTA (markdown). Con --estricto, exit 1 si hay hallazgos.
Solo biblioteca estándar.
"""
import argparse, math, re, sys, unicodedata
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import enlaces

ROOT = Path(__file__).resolve().parents[2]
APUNTE = ROOT / "apunte"

CHEQUEOS = [("1", "tilde"), ("2", "comillas"), ("3", "decimal"), ("4", "semejanza"),
            ("5", "es-decir"), ("6", "desarrollo"), ("7", "label-num"), ("8", "def-dup")]

RE_TILDE = re.compile(r"(?<![\w\\])(sólo|éste|ésta|ése|ésa|éstos|éstas|ésos|ésas|aquél|aquélla)(?!\w)", re.I)
RE_COMILLAS = re.compile(r"``|''")
RE_DECIMAL = re.compile(r"(?<![\w.])\d*\d\.\d+")
RE_UNIDAD = re.compile(r"\s*(pt|mm|cm|em|ex|in|bp|sp|\\textwidth|\\linewidth|\\columnwidth|\\textheight|\\baselineskip|\\paperwidth)\b")
RE_SEMEJANZA = re.compile(r"semejanza", re.I)
RE_SEM_CONTEXTO = re.compile(r"matri[zc]|C\^\{-1\}|C\^\{\s*-1\s*\}|conjugad", re.I)
RE_ES_DECIR = re.compile(r"es decir", re.I)
RE_DESARROLLO = re.compile(r"\\(textbf|emph|textit)\{Desarrollo\.\}")
RE_LABEL_NUM = re.compile(r"\\label\{cap:\d+\}")
RE_DEF = re.compile(r"\\begin\{definicion\}\[")

# Chequeo 9 (advertencia): términos de campo y de ajuste. Es la lista de la hoja de estilo §8 y se
# amplía a mano. Se escribe sin tildes y en minúscula; el texto se normaliza igual antes de buscar.
TERMINOS_CAMPO = [
    r"acimut(?:al(?:es)?|es)?", r"cotas?", r"gauss-kruger", r"fajas?", r"posgar",
    r"minimos cuadrados", r"residuos?", r"tolerancias?", r"redundancias?", r"covarianzas?",
    r"radiad[oa]s?", r"radiacion(?:es)?", r"nivelacion(?:es)?", r"desniveles?", r"poligonal(?:es)?",
    r"ajust(?:e|es|ar|ada|adas|ado|ados)", r"red(?:es)? libres?", r"propagacion de errores",
    r"helmert", r"elipses? de error(?:es)?", r"grs80", r"wgs84", r"mercator",
    r"latitud(?:es)? geodesicas?", r"dem", r"marcos? de referencia", r"grillas?",
    r"puntos? fijos?", r"mojon(?:es)?", r"estacion(?:es)?",
]
RE_CAMPO = re.compile(r"(?<![a-z0-9])(?:" + "|".join(TERMINOS_CAMPO) + r")(?![a-z0-9])")
# Chequeo 10 (advertencia): instrumentos.
INSTRUMENTOS = [r"estacion(?:es)? totales?", r"niveles? opticos?", r"gnss", r"limbos?", r"teodolitos?",
                r"distanciometros?"]
RE_INSTR = re.compile(r"(?<![a-z0-9])(?:" + "|".join(INSTRUMENTOS) + r")(?![a-z0-9])")
# Chequeo 11 (advertencia): preguntas o experimentos mentales en «La idea».
RE_IDEA = re.compile(r"\\section\{La idea\}")
RE_SECCION = re.compile(r"\\section\*?\{")
RE_IMPERATIVO = re.compile(r"^\s*(?:\\item\s*)?(?:Imaginá|Pensá|Probá|Suponé|Tomá|Mirá)")

# Entornos cuyo contenido no se revisa (código) y entornos donde sólo se revisa el texto de los nodos.
CODIGO = ("lstlisting", "verbatim", "Verbatim", "minted")
DIBUJO = ("tikzpicture", "axis")
MATE_ENTORNOS = ("equation", "equation*", "align", "align*", "gather", "gather*", "multline", "multline*",
                 "displaymath", "math", "alignat", "alignat*", "flalign", "flalign*")
# Comandos cuyo primer argumento es técnico (rutas, URL, etiquetas, nombres de archivo).
ARG_TECNICO = ("texttt", "url", "href", "file", "nolinkurl", "input", "include", "includegraphics", "label",
               "ref", "eqref", "pageref", "nameref", "autoref", "linkUnidad", "linkUnidadId", "unidadInteractiva",
               "animacion", "linkAnimacion", "linkFicha", "comprobacion", "cite", "lstinline", "detokenize",
               "includepdf", "usetikzlibrary", "hypersetup", "definecolor", "setlength", "vspace", "hspace",
               "vspace*", "hspace*", "rule", "resizebox", "scalebox", "setcounter", "addtolength")


def sin_comentario(linea):
    return re.sub(r"(?<!\\)%.*", "", linea)


def normalizar(txt):
    """Minúsculas y sin tildes, carácter por carácter (conserva longitudes y saltos de línea)."""
    return "".join(unicodedata.normalize("NFD", c.lower())[0] for c in txt)


def llave(txt, i):
    """Índice siguiente al cierre de la llave que abre en txt[i] (txt[i] == '{')."""
    d = 0
    for j in range(i, len(txt)):
        if txt[j] == "{" and (j == 0 or txt[j - 1] != "\\"):
            d += 1
        elif txt[j] == "}" and (j == 0 or txt[j - 1] != "\\"):
            d -= 1
            if d == 0:
                return j + 1
    return len(txt)


def corchete(txt, i):
    d = 0
    for j in range(i, len(txt)):
        if txt[j] == "[":
            d += 1
        elif txt[j] == "]":
            d -= 1
            if d == 0:
                return j + 1
    return len(txt)


def tapar(txt, a, b):
    """Reemplaza txt[a:b] por espacios conservando los saltos de línea (y por lo tanto las líneas)."""
    return txt[:a] + re.sub(r"[^\n]", " ", txt[a:b]) + txt[b:]


def mascaras(txt):
    """Devuelve (txt_texto, txt_decimal) a partir del texto sin comentarios.

    txt_texto: el código (lstlisting, verbatim, \\verb) tapado.
    txt_decimal: además, los argumentos técnicos, opciones entre corchetes de comandos y entornos, y el
    interior de los dibujos salvo el texto de los nodos.
    """
    t = txt
    for env in CODIGO:
        for m in reversed(list(re.finditer(r"\\begin\{%s\}.*?\\end\{%s\}" % (env, env), t, re.S))):
            t = tapar(t, m.start(), m.end())
    for m in reversed(list(re.finditer(r"\\verb\*?(.).*?\1", t))):
        t = tapar(t, m.start(), m.end())
    texto = t
    d = t
    # argumentos técnicos
    for m in reversed(list(re.finditer(r"\\(%s)\b\s*" % "|".join(re.escape(c) for c in ARG_TECNICO), d))):
        i = m.end()
        while i < len(d) and d[i] == "[":
            i = corchete(d, i)
        if i < len(d) and d[i] == "{":
            d = tapar(d, m.start(), llave(d, i))
    # opciones [..] de \begin{...}[..] y de comandos (\includegraphics[width=0.9\linewidth], node[scale=0.8])
    for m in reversed(list(re.finditer(r"(\\begin\{[^}]*\}|\\[A-Za-z]+\*?|node|draw|fill|path|scope)\s*\[", d))):
        if m.group(1).startswith("\\begin{definicion") or m.group(1).startswith("\\begin{ejemplo"):
            continue
        i = m.end() - 1
        d = tapar(d, i, corchete(d, i))
    # \renewcommand{\arraystretch}{1.2} y similares (parámetros de formato)
    for m in reversed(list(re.finditer(r"\\(re)?newcommand\{\\[A-Za-z]+\}\{[^{}]*\}", d))):
        d = tapar(d, m.start(), m.end())
    # nombres literales de botones y controles de las unidades, entre « » (se copian tal cual)
    for m in reversed(list(re.finditer(r"«[^»\n]*»", d))):
        d = tapar(d, m.start(), m.end())
    # dibujos: se tapa todo salvo el texto entre llaves de los nodos
    for env in DIBUJO:
        for m in reversed(list(re.finditer(r"\\begin\{%s\}.*?\\end\{%s\}" % (env, env), d, re.S))):
            bloque = d[m.start():m.end()]
            keep = []
            for n in re.finditer(r"node\s*(\([^)]*\))?\s*(at\s*\([^)]*\))?\s*\{", bloque):
                i = n.end() - 1
                keep.append((i, llave(bloque, i)))
            nuevo = re.sub(r"[^\n]", " ", bloque)
            for a, b in keep:
                nuevo = nuevo[:a] + bloque[a:b] + nuevo[b:]
            d = d[:m.start()] + nuevo + d[m.end():]
    return texto, d


def mate_spans(txt):
    """Intervalos [a, b) en modo matemático: \\( \\), \\[ \\], $ $, $$ $$ y entornos de ecuaciones."""
    spans = []
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]|\$\$(.*?)\$\$|(?<![\\$])\$(?!\$)(.*?)(?<!\\)\$", txt, re.S):
        spans.append((m.start(), m.end()))
    for env in MATE_ENTORNOS:
        e = re.escape(env)
        for m in re.finditer(r"\\begin\{%s\}.*?\\end\{%s\}" % (e, e), txt, re.S):
            spans.append((m.start(), m.end()))
    return spans


def en_spans(pos, spans):
    return any(a <= pos < b for a, b in spans)


def linea_de(txt, pos):
    return txt.count("\n", 0, pos) + 1


def titulos_definicion(txt):
    out = []
    for m in RE_DEF.finditer(txt):
        i = m.end() - 1
        j = corchete(txt, i)
        t = re.sub(r"\s+", " ", txt[i + 1:j - 1]).strip()
        out.append((linea_de(txt, m.start()), t))
    return out


def analizar(path):
    raw = path.read_text(encoding="utf-8", errors="ignore")
    lineas_raw = raw.split("\n")
    sc = "\n".join(sin_comentario(l) for l in lineas_raw)
    texto, dec = mascaras(sc)
    hall = defaultdict(list)  # chequeo -> [(línea, texto)]
    linea = lambda n: lineas_raw[n - 1].strip()[:160]

    # 1 tilde
    for n, l in enumerate(texto.split("\n"), 1):
        if RE_TILDE.search(l) and "% ambigüedad" not in lineas_raw[n - 1] and "%ambigüedad" not in lineas_raw[n - 1]:
            hall["1"].append((n, linea(n)))
    # 2 comillas a mano, fuera de la matemática (f'' es una derivada segunda)
    ms = mate_spans(texto)
    for m in RE_COMILLAS.finditer(texto):
        if not en_spans(m.start(), ms):
            n = linea_de(texto, m.start())
            if not hall["2"] or hall["2"][-1][0] != n:
                hall["2"].append((n, linea(n)))
    # 3 punto decimal
    vistos = set()
    for m in RE_DECIMAL.finditer(dec):
        if RE_UNIDAD.match(dec, m.end()):
            continue
        n = linea_de(dec, m.start())
        if n not in vistos:
            vistos.add(n)
            hall["3"].append((n, linea(n)))
    # 4 semejanza aplicada a matrices (sin contar los nombres de etiquetas)
    t4 = re.sub(r"\\(label|ref|eqref|nameref|pageref)\{[^}]*\}", lambda m: " " * len(m.group(0)), texto)
    for m in RE_SEMEJANZA.finditer(t4):
        ventana = t4[max(0, m.start() - 80): m.end() + 80]
        if RE_SEM_CONTEXTO.search(ventana):
            n = linea_de(t4, m.start())
            if not hall["4"] or hall["4"][-1][0] != n:
                hall["4"].append((n, linea(n)))
    # 5 «es decir» más de una vez cada 100 líneas
    ed = [linea_de(texto, m.start()) for m in RE_ES_DECIR.finditer(texto)]
    permitidas = max(1, math.ceil(len(lineas_raw) / 100))
    exceso = max(0, len(ed) - permitidas)
    if exceso:
        hall["5"] = [(n, f"[{len(ed)} en {len(lineas_raw)} líneas, permitidas {permitidas}] " + linea(n)) for n in ed][-exceso:]
    # 6 «Desarrollo.»
    for n, l in enumerate(texto.split("\n"), 1):
        if RE_DESARROLLO.search(l) or l.strip().startswith("Desarrollo."):
            hall["6"].append((n, linea(n)))
    # 7 etiquetas cap:NN
    for m in RE_LABEL_NUM.finditer(texto):
        n = linea_de(texto, m.start())
        hall["7"].append((n, linea(n)))
    # advertencias 9, 10 y 11 (no entran en el total)
    norm = normalizar(texto)
    campo = len(RE_CAMPO.findall(norm))
    instr = []
    for n, l in enumerate(norm.split("\n"), 1):
        for _ in RE_INSTR.finditer(l):
            instr.append((n, linea(n)))
    ideas = None
    mi = RE_IDEA.search(texto)
    if mi:
        ms_ = RE_SECCION.search(texto, mi.end())
        bloque = texto[mi.end(): ms_.start() if ms_ else len(texto)]
        ideas = sum(1 for l in bloque.split("\n") if "?" in l or RE_IMPERATIVO.search(l))
    voz = dict(lineas=len(lineas_raw), campo=campo, instr=instr, ideas=ideas)
    return dict(archivo=str(path.relative_to(APUNTE)), hallazgos=hall, definiciones=titulos_definicion(texto), voz=voz)


def analizar_todo():
    rows = [analizar(p) for p in enlaces.archivos()]
    # 8 títulos de definición repetidos en dos o más archivos
    donde = defaultdict(set)
    for r in rows:
        for _, t in r["definiciones"]:
            donde[t.lower()].add(r["archivo"])
    for r in rows:
        for n, t in r["definiciones"]:
            otros = sorted(donde[t.lower()] - {r["archivo"]})
            if otros:
                r["hallazgos"]["8"].append((n, f"[{t}] también en {', '.join(otros)}"))
    for r in rows:
        r["conteo"] = {k: len(r["hallazgos"].get(k, [])) for k, _ in CHEQUEOS}
        r["total"] = sum(r["conteo"].values())
    return rows


def totales_por_archivo():
    """{'contenido/01-rotaciones.tex': total de hallazgos} (lo usa estado.py)."""
    return {r["archivo"]: r["total"] for r in analizar_todo()}


def es_capitulo_exigido(archivo):
    m = re.match(r"(\d\d)-", Path(archivo).name)
    return bool(m) and int(m.group(1)) <= 11


def fila_voz(r):
    v = r["voz"]
    dens = v["campo"] * 100 / max(1, v["lineas"])
    ideas = v["ideas"]
    if es_capitulo_exigido(r["archivo"]):
        ok = dens < 4 and not v["instr"] and (ideas is None or ideas >= 1)
        obj = "sí" if ok else "no"
    else:
        obj = "—"
    return [r["archivo"], str(v["lineas"]), str(v["campo"]), f"{dens:.1f}".replace(".", ","),
            str(len(v["instr"])), "—" if ideas is None else str(ideas), obj]


def tabla_voz(rows):
    out = ["## Voz para el aula (advertencia)", "",
           "Chequeos 9, 10 y 11 (ESTILO.md §8); no entran en el total ni en `--estricto`.", "",
           "| Archivo | Líneas | Términos de campo | Términos cada 100 líneas | Instrumentos "
           "| Preguntas en «La idea» | Objetivo |",
           "|---|---:|---:|---:|---:|---:|:---:|"]
    for r in rows:
        out.append("| " + " | ".join(fila_voz(r)) + " |")
    return out


def informe(rows):
    out = ["# Estilo del apunte", "", "Generado por `apunte/scripts/estilo.py` (reglas en `apunte/ESTILO.md`).", "",
           "Chequeos: " + "; ".join(f"{k} = {n}" for k, n in CHEQUEOS)
           + "; 9 = términos de campo, 10 = instrumentos, 11 = preguntas en «La idea» (9–11 son advertencias).", "",
           "| Archivo | " + " | ".join(k for k, _ in CHEQUEOS) + " | Total |",
           "|---|" + "---:|" * (len(CHEQUEOS) + 1)]
    for r in rows:
        out.append(f"| {r['archivo']} | " + " | ".join(str(r["conteo"][k]) for k, _ in CHEQUEOS) + f" | {r['total']} |")
    out.append("| **Total** | " + " | ".join(str(sum(r["conteo"][k] for r in rows)) for k, _ in CHEQUEOS)
               + f" | {sum(r['total'] for r in rows)} |")
    out += ["", "## Detalle", ""]
    for r in rows:
        if not r["total"]:
            continue
        out.append(f"### {r['archivo']}")
        out.append("")
        for k, nombre in CHEQUEOS:
            for n, l in sorted(r["hallazgos"].get(k, [])):
                out.append(f"- `{k} {nombre}` L{n}: {l.replace('|', '/')}")
        out.append("")
    out += tabla_voz(rows)
    listados = [r for r in rows if r["voz"]["instr"]]
    if listados:
        out += ["", "### Instrumentos nombrados (chequeo 10)", ""]
        for r in listados:
            for n, l in r["voz"]["instr"]:
                out.append(f"- `10 instrumento` {r['archivo']} L{n}: {l.replace('|', '/')}")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", help="escribir el informe en esta ruta (markdown)")
    ap.add_argument("--estricto", action="store_true", help="exit 1 si hay hallazgos")
    a = ap.parse_args()
    rows = analizar_todo()
    txt = informe(rows)
    if a.md:
        Path(a.md).write_text(txt + "\n", encoding="utf-8")
        print(f"escrito {a.md}")
    print(txt)
    total = sum(r["total"] for r in rows)
    return 1 if (a.estricto and total) else 0


if __name__ == "__main__":
    sys.exit(main())
