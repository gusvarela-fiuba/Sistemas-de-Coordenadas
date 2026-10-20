#!/usr/bin/env python3
"""Control automático de la hoja de estilo (apunte/ESTILO.md) sobre los .tex del maestro.

Uso (desde la raíz del repo):
    uv run python apunte/scripts/estilo.py [--md RUTA] [--estricto] [--alcance apunte|interactivo|todo | --todo]

Con --alcance interactivo revisa la prosa de unidades/, clases/, mapa/, moodle/ y los .md de la raíz con
los chequeos que tienen sentido fuera de LaTeX (ver el bloque «Alcance interactivo» más abajo); --todo
hace los dos alcances. Sin --alcance (o con --alcance apunte) el comportamiento es el de siempre:

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
    r"radiad[oa]s?", r"radiacion(?:es)?", r"nivelacion(?:es)?", r"desnivel(?:es)?", r"poligonal(?:es)?",
    r"ajust(?:e|es|ar|ada|adas|ado|ados)", r"red(?:es)? libres?", r"propagacion de errores",
    r"helmert", r"elipses? de error(?:es)?", r"grs80", r"wgs84", r"mercator",
    r"latitud(?:es)? geodesicas?", r"dem", r"marcos? de referencia", r"grillas?",
    r"puntos? fijos?", r"mojon(?:es)?", r"estacion(?:es)?",
]
RE_CAMPO = re.compile(r"(?<![a-z0-9])(?:" + "|".join(TERMINOS_CAMPO) + r")(?![a-z0-9])")
# Excepciones del chequeo 9: nombres propios que contienen un término de campo y que el texto no puede
# evitar. «Copernicus DEM GLO-30» es el nombre del producto de datos del recorte de C3 y el crédito de
# la figura lo exige tal cual (decisión del editor, 2026-10-19); se quita del texto antes de contar.
EXCEPCIONES_CAMPO = re.compile(r"copernicus dem glo-30")
# Chequeo 10 (advertencia): instrumentos.
INSTRUMENTOS = [r"estacion(?:es)? total(?:es)?", r"niveles? opticos?", r"gnss", r"limbos?", r"teodolitos?",
                r"distanciometros?"]
RE_INSTR = re.compile(r"(?<![a-z0-9])(?:" + "|".join(INSTRUMENTOS) + r")(?![a-z0-9])")
# Chequeo 11 (advertencia): preguntas o experimentos mentales en «La idea».
RE_IDEA = re.compile(r"\\section\{La idea\}")
RE_SECCION = re.compile(r"\\section\*?\{")
RE_IMPERATIVO = re.compile(r"^\s*(?:\\item\s*)?(?:Imaginá|Pensá|Probá|Suponé|Tomá|Mirá)")

# Entornos cuyo contenido no se revisa (código) y entornos donde solo se revisa el texto de los nodos.
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
    campo = len(RE_CAMPO.findall(EXCEPCIONES_CAMPO.sub(" ", norm)))
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



# ----------------------------------------------------------------------------------------------------
# Alcance interactivo (--alcance interactivo | --todo): unidades/, clases/, mapa/, moodle/ y los .md de
# la raíz. Fuera de LaTeX solo tienen sentido algunos chequeos; se aplican a la prosa que ve el lector:
#   .py   cadenas de texto (incluidas las partes literales de los f-strings) que tienen al menos dos
#         palabras, salvo docstrings y el código de mo.ui.code_editor;
#   .md   el archivo entero, sin el frontmatter YAML, los bloques de código ni el código en línea;
#   .yaml el valor de cada línea `clave: valor` (sin comentarios); las comillas son sintaxis YAML;
#   .xml  el texto de los CDATA (Moodle), sin las etiquetas HTML.
# En todos los casos se quitan la matemática ($…$, $$…$$, \(…\), \[…\]) salvo para el decimal, las
# etiquetas HTML, las URL y los nombres de controles entre « » (se copian tal cual de la unidad).
# Chequeos (los números coinciden con los del modo apunte cuando la regla es la misma):
#   1 tilde      «sólo» o demostrativo con tilde
#   2 comillas   comillas rectas en la prosa: ", '…', `` o '' (fuera de la matemática y del código)
#   3 decimal    número con punto decimal en la prosa o en la matemática escrita a mano (no en los
#                números que calcula el código, que salen por interpolación)
#   5 es-decir   «es decir» más de una vez cada 100 líneas del archivo
#   6 desarrollo párrafo que empieza con «Desarrollo.»
#   10 instrumento  estación total, nivel óptico, GNSS, limbo, teodolito, distanciómetro: en este
#                alcance es bloqueante (ESTILO.md §8 regla 4)
#   12 desaprender  «desaprender» y sus formas (reformular: «dejar de lado una costumbre»)
#   13 voseo     imperativo de tú o de usted al comienzo de oración (Mueve, Mueva, Observa, Calcule…)
# Excepciones (EXCLUIDOS_INTERACTIVO): archivos que contienen a propósito lo que se busca.
# ----------------------------------------------------------------------------------------------------
import ast, io, tokenize

DIRS_INTERACTIVO = (("unidades/", (".py", ".md")), ("clases/", (".md",)), ("mapa/", (".md", ".yaml", ".yml")),
                    ("moodle/", (".xml", ".md")))
# Rutas relativas a la raíz que no se revisan. Vacío: la hoja de estilo (apunte/ESTILO.md) y este script, que
# contienen a propósito las palabras que se buscan, quedan fuera del alcance por ubicación (apunte/).
EXCLUIDOS_INTERACTIVO = set()
CHEQUEOS_INTERACTIVO = [("1", "tilde"), ("2", "comillas"), ("3", "decimal"), ("5", "es-decir"),
                        ("6", "desarrollo"), ("10", "instrumento"), ("12", "desaprender"), ("13", "voseo")]
RE_DESAPRENDER = re.compile(r"desaprend\w*", re.I)
# Imperativos de tú y de usted frecuentes en consignas. Solo al comienzo de oración, para no confundir
# «el punto se mueve» (indicativo) con «Mueve el deslizador» (imperativo).
# De tú, solo las formas que al comienzo de oración casi nunca son indicativo («Cambia de signo», «Gira el
# mismo ángulo» son indicativo y no se buscan).
_TU = ("Fíjate|Haz|Supón|Pon|Elige|Imagina|Piensa|Recuerda|Mira|Observa|Arrastra|Escribe|Compara|Calcula|"
       "Comprueba|Verifica|Considera|Anota|Selecciona|Pulsa|Ejecuta|Intenta")
_USTED = ("Mueva|Mire|Observe|Calcule|Compruebe|Elija|Cambie|Fíjese|Considere|Recuerde|Verifique|Haga|Suponga|"
          "Imagine|Piense|Arrastre|Escriba|Compare|Active|Desactive|Ajuste|Gire|Lea|Note|Anote|Busque|Encuentre|"
          "Pulse|Seleccione|Ejecute|Modifique|Intente|Vuelva|Deje|Ponga|Suba|Baje|Responda|Dibuje|Marque|Agregue|Pruebe|Use")
RE_VOSEO = re.compile(r"(?:^\s*|[.!?:]\s+|¿|¡|\*\*|^\s*[-*]\s+|^\s*\d+\.\s+)(%s|%s)\b" % (_TU, _USTED), re.M)
RE_RECTAS = re.compile(r"\"|``|''|(?<![\w'])'[^'\n]+'(?![\w'])")
# Número con punto decimal; puede ir pegado a una letra (\\cdot5.6, 0.4i) pero no ser parte de una versión
# (0.24.2, v0.24).
RE_DECIMAL_PROSA = re.compile(r"(?<![\d.vV])\d+\.\d+(?!\.?\d)")
RE_MATE_PROSA = re.compile(r"\$\$.*?\$\$|(?<![\\$])\$(?!\$).*?(?<!\\)\$|\\\(.*?\\\)|\\\[.*?\\\]", re.S)
RE_HTML = re.compile(r"</?[A-Za-z][^<>]*>")
RE_URL = re.compile(r"https?://\S+|\]\([^)]*\)")
RE_GUILLEMETS = re.compile(r"«[^»\n]*»")
RE_COD_FENCE = re.compile(r"```.*?```", re.S)
RE_COD_LINEA = re.compile(r"`[^`\n]*`")
RE_PALABRAS = re.compile(r"[A-Za-zÁÉÍÓÚÑáéíóúñü]{2,}")


def _tapar_re(txt, rx):
    return rx.sub(lambda m: re.sub(r"[^\n]", " ", m.group(0)), txt)


# Números de sección: «**3.2 …**», «sección 3.2», «secciones 3.1 y 3.2», «(Rotaciones II, 3.2)».
RE_NUM_SECCION = re.compile(r"(?:\*\*|^\s*#+\s+|[Ss]ecci[oó]n(?:es)?\s+(?:\d\.\d(?:,\s*|\s+[yo]\s+))*|[IVX]+,\s+)\d{1,2}\.\d{1,2}(?!\d)", re.M)


# Excepción del chequeo 3: número de problema, sección o capítulo entre paréntesis justo después de la palabra
# («los problemas (12.5)», «la sección (3.2)», «capítulo (9.4)»). No es un decimal sino una referencia; solo se
# tapa el paréntesis con el número (\d+.\d+), así que «el problema vale (0.5)» sin la palabra delante, o «problema
# con 0.5», siguen marcándose.
RE_NUM_PROBLEMA = re.compile(r"(?<!\w)(?:[Pp]roblemas?|[Ss]ecci[oó]n(?:es)?|[Cc]ap[ií]tulos?)\s+\(\d+\.\d+\)")


def _quitar_secciones(con_mate, sin_mate):
    """Tapa en con_mate los números de sección que están fuera de la matemática (visibles en sin_mate), y los
    números de problema, sección o capítulo entre paréntesis (RE_NUM_PROBLEMA)."""
    for m in list(RE_NUM_SECCION.finditer(sin_mate)) + list(RE_NUM_PROBLEMA.finditer(sin_mate)):
        if m.group(0).strip():
            con_mate = con_mate[:m.start()] + re.sub(r"[^\n]", " ", m.group(0)) + con_mate[m.end():]
    return con_mate


def _limpiar(txt, mate=True):
    """Tapa con espacios (conservando líneas) código, HTML, URL, « » y, si mate, la matemática."""
    for rx in (RE_COD_FENCE, RE_COD_LINEA, RE_HTML, RE_URL, RE_GUILLEMETS):
        txt = _tapar_re(txt, rx)
    return _tapar_re(txt, RE_MATE_PROSA) if mate else txt


RE_NOMBRE_CHEQUEOS = re.compile(r"_?checks?\w*$")


def es_prosa(valor):
    """Una cadena es prosa si tiene al menos dos palabras fuera de la matemática, o si tiene matemática."""
    return len(RE_PALABRAS.findall(_limpiar(valor))) >= 2 or bool(RE_MATE_PROSA.search(_limpiar(valor, mate=False)))


def _col_char(lineas, lineno, col_offset):
    if not lineas or not (1 <= lineno <= len(lineas)):
        return col_offset
    return len(lineas[lineno - 1].encode("utf-8")[:col_offset].decode("utf-8", errors="replace"))


def _rangos_py(arbol, lineas=None):
    """(fuera, tecnico): rangos ((l0, c0), (l1, c1)) de cadenas que no son prosa (docstrings, código de
    mo.ui.code_editor, assert, raise) y de cadenas técnicas para el decimal: comparaciones, claves de diccionario (nombres de casos
    precargados), argumentos label/options/value de mo.ui (nombres de controles, que el apunte copia
    tal cual entre « ») y las descripciones de las verificaciones (`_checks = [...]`)."""
    rango = lambda n: (
        (n.lineno, _col_char(lineas, n.lineno, n.col_offset)),
        (n.end_lineno, _col_char(lineas, n.end_lineno, n.end_col_offset)),
    )
    fuera, tecnico = [], []
    for nodo in ast.walk(arbol):
        if isinstance(nodo, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and nodo.body:
            d = nodo.body[0]
            if isinstance(d, ast.Expr) and isinstance(d.value, ast.Constant) and isinstance(d.value.value, str):
                fuera.append(rango(d))
        if isinstance(nodo, ast.Call):
            f = nodo.func
            if getattr(f, "attr", None) == "code_editor":
                fuera.append(rango(nodo))
            elif isinstance(f, ast.Attribute) and isinstance(f.value, ast.Attribute) and f.value.attr == "ui":
                tecnico += [rango(k.value) for k in nodo.keywords if k.arg in ("label", "options", "value")]
        if isinstance(nodo, (ast.Assert, ast.Raise)):
            fuera.append(rango(nodo))           # autoverificaciones y errores de programación: no se muestran
        if isinstance(nodo, ast.Compare):
            tecnico.append(rango(nodo))         # cadenas que se comparan con lo que devuelve el código
        if isinstance(nodo, ast.Dict):
            tecnico += [rango(k) for k in nodo.keys if k is not None]
        if isinstance(nodo, ast.Assign) and any(isinstance(x, ast.Name) and RE_NOMBRE_CHEQUEOS.match(x.id)
                                                 for x in nodo.targets):
            tecnico.append(rango(nodo.value))
    return fuera, tecnico


def _dentro(pos, rangos):
    return any(a <= pos < b for a, b in rangos)


def prosa_py(fuente, archivo="<py>"):
    """[(línea inicial, texto, técnico)] de las cadenas de un .py que se muestran como prosa. Los
    f-strings se rearman con ¤ en lugar de cada {expresión} (no se revisa lo que calcula el código) y
    las cadenas contiguas ("a" "b", una por renglón) se juntan en una sola, con un salto por renglón."""
    lineas = fuente.split("\n")
    try:
        fuera, tecnico = _rangos_py(ast.parse(fuente), lineas)
    except SyntaxError as exc:
        print(f"estilo.py: advertencia: error de sintaxis en {archivo}: {exc}", file=sys.stderr)
        fuera, tecnico = [], []
    out, pila, grupo = [], [], []   # pila: [inicio, profundidad de llaves, partes] por f-string abierto

    def cerrar_grupo():
        if grupo:
            (l0, c0), _ = grupo[0]
            texto, linea = "", l0
            for (l, _c), v in grupo:
                texto += "\n" * (l - linea) + v
                linea = l + v.count("\n")
            if not _dentro((l0, c0), fuera) and es_prosa(texto):
                out.append((l0, texto, _dentro((l0, c0), tecnico)))
            grupo.clear()

    def literal(inicio, valor, triple):
        if not triple:
            valor = valor.replace("\n", " ")   # "\n" escrito como escape: no cambia de renglón en el fuente
        grupo.append((inicio, valor))

    try:
        for tok in tokenize.generate_tokens(io.StringIO(fuente).readline):
            tipo = tokenize.tok_name[tok.type]
            if pila:
                if tipo == "FSTRING_END":
                    inicio, _, partes, triple = pila.pop()
                    if not pila:
                        literal(inicio, "".join(partes), triple)
                elif tipo == "OP" and tok.string in "{}":
                    if tok.string == "{":
                        if pila[-1][1] == 0:
                            pila[-1][2].append("¤")
                        pila[-1][1] += 1
                    else:
                        pila[-1][1] -= 1
                elif tipo == "FSTRING_MIDDLE" and pila[-1][1] == 0:
                    pila[-1][2].append(tok.string)
                elif tipo == "FSTRING_START":
                    pila.append([tok.start, 0, [], tok.string.endswith(('"""', "'''"))])
                continue
            if tipo == "FSTRING_START":
                pila.append([tok.start, 0, [], tok.string.endswith(('"""', "'''"))])
            elif tipo == "STRING":
                try:
                    valor = ast.literal_eval(tok.string)
                except Exception:
                    continue
                if isinstance(valor, str):
                    literal(tok.start, valor, tok.string.endswith(('"""', "'''")))
            elif tipo not in ("NL", "COMMENT", "INDENT", "DEDENT"):
                cerrar_grupo()
    except (tokenize.TokenError, IndentationError, SyntaxError):
        pass
    cerrar_grupo()
    return out


def prosa_md(fuente):
    if fuente.startswith("---\n"):
        fin = fuente.find("\n---", 4)
        if fin > 0:
            fuente = re.sub(r"[^\n]", " ", fuente[:fin + 4]) + fuente[fin + 4:]
    return [(1, fuente, False)]


def prosa_yaml(fuente):
    out = []
    for n, l in enumerate(fuente.split("\n"), 1):
        if l.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s*(?:-\s+)?(?:[\w.-]+:\s*)?(.*)$", l)
        v = m.group(1).strip() if m else ""
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if v:
            out.append((n, v, False))
    return out


def prosa_xml(fuente):
    out = []
    for m in re.finditer(r"<!\[CDATA\[(.*?)\]\]>", fuente, re.S):
        out.append((linea_de(fuente, m.start()), m.group(1), False))
    return out


def archivos_interactivo():
    rutas = sorted(p for p in ROOT.glob("*.md") if p.is_file())
    for d, exts in DIRS_INTERACTIVO:
        rutas += sorted(p for p in (ROOT / d).rglob("*") if p.is_file() and p.suffix in exts
                        and "__pycache__" not in p.parts and "__marimo__" not in p.parts)
    return [p for p in rutas if str(p.relative_to(ROOT)) not in EXCLUIDOS_INTERACTIVO]


def analizar_interactivo(path):
    fuente = path.read_text(encoding="utf-8", errors="ignore")
    lineas = fuente.split("\n")
    suf = path.suffix
    if suf == ".py":
        trozos = prosa_py(fuente, path)
    else:
        trozos = {".md": prosa_md, ".xml": prosa_xml}.get(suf, prosa_yaml)(fuente)
    hall = defaultdict(set)
    ed = []
    for n0, txt, tecnico in trozos:
        sin_mate = _limpiar(txt)
        con_mate = _limpiar(txt, mate=False)
        # números de sección («**3.2 …**», «sección 3.2», «Rotaciones II, 3.2») fuera de la matemática
        con_mate = _quitar_secciones(con_mate, sin_mate)
        for i, (l, lm) in enumerate(zip(sin_mate.split("\n"), con_mate.split("\n"))):
            n = n0 + i
            if RE_TILDE.search(l):
                hall["1"].add(n)
            if suf != ".yaml" and suf != ".yml" and RE_RECTAS.search(l):
                hall["2"].add(n)
            if not tecnico and RE_DECIMAL_PROSA.search(lm):
                hall["3"].add(n)
            ed += [n] * len(RE_ES_DECIR.findall(l))
            if re.match(r"\s*(\*\*|\\textbf\{)?Desarrollo\.", l):
                hall["6"].add(n)
            if RE_INSTR.search(normalizar(l)):
                hall["10"].add(n)
            if RE_DESAPRENDER.search(l):
                hall["12"].add(n)
            if RE_VOSEO.search(l):
                hall["13"].add(n)
    permitidas = max(1, math.ceil(len(lineas) / 100))
    if len(ed) > permitidas:
        hall["5"] = set(ed[permitidas:])
    linea = lambda n: lineas[n - 1].strip()[:160] if 0 < n <= len(lineas) else ""
    hall = {k: [(n, linea(n)) for n in sorted(v)] for k, v in hall.items()}
    conteo = {k: len(hall.get(k, [])) for k, _ in CHEQUEOS_INTERACTIVO}
    try:
        archivo = str(path.resolve().relative_to(ROOT))
    except ValueError:
        archivo = str(path)
    return dict(archivo=archivo, hallazgos=hall, conteo=conteo, total=sum(conteo.values()))


def analizar_interactivo_todo():
    return [analizar_interactivo(p) for p in archivos_interactivo()]


def informe_interactivo(rows):
    out = ["# Estilo del material interactivo", "",
           "Generado por `apunte/scripts/estilo.py --alcance interactivo` (reglas en `apunte/ESTILO.md`).", "",
           "Chequeos: " + "; ".join(f"{k} = {n}" for k, n in CHEQUEOS_INTERACTIVO) + ".", "",
           "| Archivo | " + " | ".join(k for k, _ in CHEQUEOS_INTERACTIVO) + " | Total |",
           "|---|" + "---:|" * (len(CHEQUEOS_INTERACTIVO) + 1)]
    for r in rows:
        if r["total"]:
            out.append(f"| {r['archivo']} | " + " | ".join(str(r["conteo"][k]) for k, _ in CHEQUEOS_INTERACTIVO)
                       + f" | {r['total']} |")
    out.append("| **Total** (" + str(len(rows)) + " archivos) | "
               + " | ".join(str(sum(r["conteo"][k] for r in rows)) for k, _ in CHEQUEOS_INTERACTIVO)
               + f" | {sum(r['total'] for r in rows)} |")
    out += ["", "## Detalle", ""]
    for r in rows:
        if not r["total"]:
            continue
        out += [f"### {r['archivo']}", ""]
        for k, nombre in CHEQUEOS_INTERACTIVO:
            for n, l in r["hallazgos"].get(k, []):
                out.append(f"- `{k} {nombre}` L{n}: {l.replace('|', '/')}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--md", help="escribir el informe en esta ruta (markdown)")
    ap.add_argument("--estricto", action="store_true", help="exit 1 si hay hallazgos")
    ap.add_argument("--alcance", choices=("apunte", "interactivo", "todo"), default="apunte",
                    help="apunte (default): los .tex del maestro; interactivo: unidades/, clases/, mapa/, moodle/ "
                         "y los .md de la raíz; todo: los dos")
    ap.add_argument("--todo", dest="alcance", action="store_const", const="todo", help="alias de --alcance todo")
    a = ap.parse_args()
    partes, total = [], 0
    if a.alcance in ("apunte", "todo"):
        rows = analizar_todo()
        partes.append(informe(rows))
        total += sum(r["total"] for r in rows)
    if a.alcance in ("interactivo", "todo"):
        rows_i = analizar_interactivo_todo()
        partes.append(informe_interactivo(rows_i))
        total += sum(r["total"] for r in rows_i)
    txt = "\n".join(partes)
    if a.md:
        Path(a.md).write_text(txt + "\n", encoding="utf-8")
        print(f"escrito {a.md}")
    print(txt)
    return 1 if (a.estricto and total) else 0


if __name__ == "__main__":
    sys.exit(main())
