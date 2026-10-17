# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Transformaciones proyectivas — Clase II

Autor: Gustavo Varela
Sistemas de Coordenadas · Agrimensura · FIUBA · 2026
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from fractions import Fraction
    from math import gcd, lcm

    return Fraction, gcd, lcm, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Transformaciones proyectivas — Clase II

    **Gustavo Varela** · Sistemas de Coordenadas · Agrimensura · FIUBA · 2026 · clase del 16/9

    **Enunciado.** Las transformaciones proyectivas mantienen rectas las rectas y, por eso, quedan definidas por un
    cuadrilátero (cuatro puntos y sus cuatro imágenes). Dado un pentágono $ABCDE$:

    1. ¿Cuáles son las transformaciones proyectivas posibles donde **cuatro vértices caen sobre otros cuatro**?
    2. ¿Cómo se calculan?
    3. ¿Dónde cae el **vértice restante**?
    4. ¿La transformación tiene **punto fijo**? (al menos un punto o una dirección fija: propio o impropio)

    **Foto mental del pentágono.** Coordenadas fijadas para toda la clase:

    $$A = (-2, -1), \quad B = (-3, 1), \quad C = (0, 3), \quad D = (3, 1), \quad E = (2, -1)$$

    Es un pentágono simétrico respecto del eje $y$: $C$ es la "punta" de arriba, $B$ y $D$ los hombros,
    $A$ y $E$ la base. Se recorre $A \to B \to C \to D \to E$ en sentido horario. Con esta forma, la "cíclica"
    $ABCD \to BCDE$ es un giro de un quinto de vuelta *proyectivo* (no euclídeo: el pentágono no es regular) y la
    "reflexión" $ABCD \to EDCB$ es exactamente la simetría $x \mapsto -x$.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## A. Teoría en cinco renglones

    **Coordenadas homogéneas.** El punto $(x, y)$ se representa por cualquier múltiplo no nulo de $p = (x, y, 1)^T$;
    los vectores $(a, b, 0)^T$ son los **puntos impropios** (del infinito), uno por cada dirección $(a, b)$.

    **Homografía.** Una transformación proyectiva del plano es una matriz $H \in \mathbb{R}^{3\times 3}$ invertible que actúa como

    $$p' \sim H\,p \qquad (\sim \text{ significa "igual salvo un factor de escala"}).$$

    $H$ y $kH$ son la misma transformación: de los 9 coeficientes quedan **8 grados de libertad**. Cada correspondencia
    $p_i \mapsto q_i$ impone 2 ecuaciones, así que **4 puntos** (sin tres alineados) la determinan por completo.
    Las rectas $\ell = (a, b, c)^T$ (ecuación $ax + by + c = 0$, o sea $\ell^T p = 0$) se transforman como $\ell' \sim H^{-T}\ell$.

    **Construcción por base canónica.** Sea $M = [\,p_1\; p_2\; p_3\,]$ la matriz con los tres primeros puntos como columnas
    y $\lambda = M^{-1} p_4$. Entonces

    $$A = M\,\mathrm{diag}(\lambda)$$

    manda $e_1, e_2, e_3, e_1 + e_2 + e_3$ exactamente a $p_1, p_2, p_3, p_4$. Haciendo lo mismo con los destinos ($B$) queda

    $$H = B\,A^{-1}.$$

    **La recta que se va al infinito.** $w' = h_{31}x + h_{32}y + h_{33}$: los puntos con $w' = 0$ son los que $H$ manda al
    infinito. La **tercera fila de $H$** es esa recta. Si es $(0, 0, k)$ la transformación es **afín** (el infinito queda en el infinito).

    **Puntos y rectas fijas.** $p$ es fijo si $H p \sim p$, es decir, si es **autovector** de $H$. Las rectas fijas son
    los autovectores de $H^T$. El polinomio característico es de grado 3 con coeficientes reales, así que **siempre hay al menos
    un autovalor real** $\Rightarrow$ al menos un punto fijo real, propio (con coordenadas) o impropio (una dirección fija).
    Según los autovalores:

    | autovalores | puntos fijos | nombre |
    |---|---|---|
    | tres reales distintos | tres, no alineados | triángulo invariante |
    | uno real + par complejo | uno solo (real) | rotación proyectiva |
    | repetidos, $H$ diagonalizable | una recta de puntos fijos + un centro | homología |
    | repetidos, $H$ no diagonalizable | un punto y una recta (incidentes) | elación |

    **Jerarquía.**

    | grupo | forma de $H$ | grados de libertad | invariantes |
    |---|---|---|---|
    | isometría | $\begin{pmatrix} R & t \\ 0 & 1\end{pmatrix}$, $R^T R = I$ | 3 | longitudes, ángulos, áreas |
    | semejanza | $\begin{pmatrix} sR & t \\ 0 & 1\end{pmatrix}$ | 4 | ángulos, razones de longitudes |
    | afín | $\begin{pmatrix} M & t \\ 0 & 1\end{pmatrix}$, $\det M \neq 0$ | 6 | paralelismo, razones sobre una recta, la recta del infinito |
    | proyectiva | $H$ cualquiera, $\det H \neq 0$ | 8 | rectas, incidencia, razón doble |
    """)
    return


@app.cell
def _():
    PTS = {"A": (-2, -1), "B": (-3, 1), "C": (0, 3), "D": (3, 1), "E": (2, -1)}
    NOMBRES = ["A", "B", "C", "D", "E"]
    return NOMBRES, PTS


@app.cell
def _(Fraction, gcd, lcm, np):
    # ---------- núcleo: homografías, exactas (Fraction) y en float ----------

    def hom(p):
        """(x, y) -> vector homogéneo (x, y, 1), float."""
        return np.array([float(p[0]), float(p[1]), 1.0])

    def dehom(v):
        """(x, y, w) -> array (x/w, y/w). Devuelve None si el punto es impropio (|w| < 1e-12 relativo)."""
        v = np.asarray(v, dtype=float)
        if abs(v[2]) < 1e-12 * max(1.0, float(np.abs(v).max())):
            return None
        return v[:2] / v[2]

    def _fr_hom(p):
        return np.array([Fraction(p[0]), Fraction(p[1]), Fraction(1)], dtype=object)

    def _det3(M):
        return (
            M[0, 0] * (M[1, 1] * M[2, 2] - M[1, 2] * M[2, 1])
            - M[0, 1] * (M[1, 0] * M[2, 2] - M[1, 2] * M[2, 0])
            + M[0, 2] * (M[1, 0] * M[2, 1] - M[1, 1] * M[2, 0])
        )

    def _inv3(M):
        """Inversa exacta 3x3 por adjunta (M con Fractions)."""
        d = _det3(M)
        if d == 0:
            raise ValueError("matriz singular: hay tres puntos alineados")
        inv = np.empty((3, 3), dtype=object)
        for i in range(3):
            for j in range(3):
                # inv[i][j] = cofactor(j, i) / det ; con índices cíclicos el signo sale solo
                inv[i, j] = (
                    M[(j + 1) % 3, (i + 1) % 3] * M[(j + 2) % 3, (i + 2) % 3]
                    - M[(j + 1) % 3, (i + 2) % 3] * M[(j + 2) % 3, (i + 1) % 3]
                ) / d
        return inv

    def canon_matrix(pts4):
        """A = M·diag(λ), con M = [p1 p2 p3] y λ = M⁻¹ p4. Manda e1, e2, e3, e1+e2+e3 a los cuatro puntos. Exacta."""
        M = np.empty((3, 3), dtype=object)
        for j in range(3):
            M[:, j] = _fr_hom(pts4[j])
        lam = _inv3(M) @ _fr_hom(pts4[3])
        if any(l == 0 for l in lam):
            raise ValueError("el cuarto punto está alineado con dos de los otros")
        A = np.empty((3, 3), dtype=object)
        for j in range(3):
            A[:, j] = M[:, j] * lam[j]
        return A

    def homography(src4, dst4):
        """H con H·src_i ~ dst_i. Devuelve (H_int, H_float): la entera (coprimos, H[2,2] > 0) y su copia en float."""
        A = canon_matrix(src4)
        B = canon_matrix(dst4)
        H = B @ _inv3(A)  # exacta, Fractions
        den = 1
        for x in H.flat:
            den = lcm(den, x.denominator)
        Hi = [[int(x * den) for x in fila] for fila in H]
        g = 0
        for fila in Hi:
            for x in fila:
                g = gcd(g, abs(x))
        Hi = [[x // g for x in fila] for fila in Hi]
        pivote = Hi[2][2] if Hi[2][2] != 0 else next(x for fila in Hi for x in fila if x != 0)
        if pivote < 0:
            Hi = [[-x for x in fila] for fila in Hi]
        H_int = np.array(Hi, dtype=np.int64)
        return H_int, H_int.astype(float)

    def apply_h(H, pts):
        """Aplica H a una lista de puntos (x, y). Devuelve array (n, 3) homogéneo en float (deshomogeneizar con dehom)."""
        P = np.array([hom(p) for p in pts])
        return (np.asarray(H, dtype=float) @ P.T).T

    def _nullspace(M, tol):
        _u, s, vt = np.linalg.svd(M)
        rank = int(np.sum(s > tol))
        return vt[rank:].T  # columnas = base del núcleo

    def _grupos_reales(H):
        """Autovalores agrupados: lista de [λ, mult. algebraica] reales y lista de complejos."""
        w = np.linalg.eigvals(H)
        scale = max(float(np.abs(w).max()), 1e-300)
        tol = 1e-6 * scale
        reales = sorted(float(z.real) for z in w if abs(z.imag) <= tol)
        complejos = [complex(z) for z in w if abs(z.imag) > tol]
        grupos = []
        for lam in reales:
            if grupos and abs(lam - grupos[-1][-1]) <= tol:
                grupos[-1].append(lam)
            else:
                grupos.append([lam])
        return grupos, complejos

    def _normaliza_vec(v):
        v = np.real(v)
        v = v / np.abs(v).max()
        primero = next(x for x in v if abs(x) > 1e-12)
        return v if primero > 0 else -v

    def fixed_points(H):
        """Puntos fijos de H (autovectores). Lista de dicts con autovalor, tipo, punto homogéneo, xy o dirección."""
        H = np.asarray(H, dtype=float)
        grupos, complejos = _grupos_reales(H)
        tol_n = 1e-8 * max(float(np.abs(H).max()), 1.0)
        out = []
        for g in grupos:
            lam = float(np.mean(g))
            N = _nullspace(H - lam * np.eye(3), tol_n)
            k = N.shape[1]
            base = dict(autovalor=lam, mult_alg=len(g), mult_geo=k)
            if k >= 3:
                out.append(dict(base, tipo="todo"))
            elif k == 2:
                l = _normaliza_vec(np.cross(N[:, 0], N[:, 1]))
                out.append(dict(base, tipo="recta", recta=l))
            else:
                if k == 0:  # no debería pasar; fallback a eig
                    w, V = np.linalg.eig(H)
                    N = V[:, [int(np.argmin(np.abs(w - lam)))]]
                v = _normaliza_vec(N[:, 0])
                if abs(v[2]) > 1e-9:
                    v = v / v[2]
                    out.append(dict(base, tipo="propio", v=v, xy=v[:2].copy()))
                else:
                    d = v[:2] / np.linalg.norm(v[:2])
                    out.append(dict(base, tipo="impropio", v=v, dir=d))
        for z in complejos:
            out.append(dict(autovalor=z, mult_alg=1, mult_geo=0, tipo="complejo"))
        return out

    def fixed_lines(H):
        """Rectas fijas de H (autovectores de Hᵀ). Lista de dicts con autovalor, tipo y coeficientes (a, b, c)."""
        H = np.asarray(H, dtype=float)
        grupos, complejos = _grupos_reales(H)
        tol_n = 1e-8 * max(float(np.abs(H).max()), 1.0)
        out = []
        for g in grupos:
            lam = float(np.mean(g))
            N = _nullspace(H.T - lam * np.eye(3), tol_n)
            k = N.shape[1]
            base = dict(autovalor=lam, mult_alg=len(g), mult_geo=k)
            if k >= 3:
                out.append(dict(base, tipo="todas"))
            elif k == 2:
                centro = _normaliza_vec(np.cross(N[:, 0], N[:, 1]))
                out.append(dict(base, tipo="haz", centro=centro, centro_xy=dehom(centro)))
            else:
                if k == 0:
                    w, V = np.linalg.eig(H.T)
                    N = V[:, [int(np.argmin(np.abs(w - lam)))]]
                out.append(dict(base, tipo="recta", l=_normaliza_vec(N[:, 0])))
        for z in complejos:
            out.append(dict(autovalor=z, mult_alg=1, mult_geo=0, tipo="complejo"))
        return out

    def vanishing_line(H):
        """Recta que H manda al infinito: tercera fila (a, b, c) → ax + by + c = 0."""
        return np.asarray(H, dtype=float)[2].copy()

    def classify(H):
        """Tipo de homografía según los autovalores."""
        H = np.asarray(H, dtype=float)
        s = float(np.abs(H).max())
        if np.allclose(H, H[0, 0] * np.eye(3), atol=1e-9 * s) and abs(H[0, 0]) > 0:
            return "identidad"
        grupos, complejos = _grupos_reales(H)
        if complejos:
            return "uno real + par complejo: rotación proyectiva"
        if len(grupos) == 3:
            return "tres reales distintos: triángulo invariante"
        pf = fixed_points(H)
        rep = next(p for p in pf if p["mult_alg"] >= 2)
        if rep["mult_geo"] >= 2:
            det = "homología (una recta de puntos fijos y un centro; si el centro está en la recta es una elación)"
            # homología con centro sobre el eje ⇒ autovalor triple
            if rep["mult_alg"] == 3:
                det = "elación (autovalor triple, recta de puntos fijos y centro sobre ella)"
        else:
            det = "no diagonalizable: un solo punto fijo para el autovalor doble (bloque de Jordan)"
        return "autovalores repetidos: homología/elación — " + det

    return (
        apply_h,
        canon_matrix,
        classify,
        dehom,
        fixed_lines,
        fixed_points,
        hom,
        homography,
        vanishing_line,
    )


@app.cell
def _(Fraction, np):
    # ---------- ayudantes de formato (LaTeX) y geometría de la ventana ----------

    def pmat(M, fmt=lambda x: f"{x}"):
        filas = r" \\ ".join(" & ".join(fmt(x) for x in fila) for fila in M)
        return r"\begin{pmatrix}" + filas + r"\end{pmatrix}"

    def frac_tex(f):
        f = Fraction(f)
        if f.denominator == 1:
            return str(f.numerator)
        signo = "-" if f < 0 else ""
        return rf"{signo}\tfrac{{{abs(f.numerator)}}}{{{f.denominator}}}"

    def rat_tex(x, maxden=500, tol=1e-12):
        """Fracción exacta si el float 'es' un racional chico (a precisión de máquina); si no, None."""
        f = Fraction(float(x)).limit_denominator(maxden)
        return frac_tex(f) if abs(float(f) - float(x)) <= tol * max(1.0, abs(float(x))) else None

    def num_tex(x, dec=4):
        r = rat_tex(x)
        return r if r is not None else f"{float(x):.{dec}f}"

    def cplx_tex(z):
        z = complex(z)
        if abs(z.imag) < 1e-9 * max(1.0, abs(z)):
            return num_tex(z.real)
        return rf"{z.real:.4f} {'+' if z.imag >= 0 else '-'} {abs(z.imag):.4f}\,i"

    def pt_tex(xy):
        return rf"({num_tex(xy[0])},\ {num_tex(xy[1])})"

    def _coefs_lindos(l):
        l = np.asarray(l, dtype=float)
        l = l / np.abs(l).max()
        for k in range(1, 400):
            m = l * k
            if np.allclose(m, np.round(m), atol=1e-7):
                ints = [int(round(x)) for x in m]
                g = 0
                for x in ints:
                    g = np.gcd(g, abs(x))
                ints = [x // g for x in ints]
                primero = next(x for x in ints if x != 0)
                return [-x for x in ints] if primero < 0 else ints
        primero = next(x for x in l if abs(x) > 1e-12)
        return list(-l if primero < 0 else l)

    def line_tex(l):
        """(a, b, c) → 'ax + by + c = 0' con coeficientes enteros si se puede."""
        a, b, c = _coefs_lindos(l)
        partes = []
        for coef, var in ((a, "x"), (b, "y"), (c, "")):
            if isinstance(coef, (int, np.integer)):
                if coef == 0:
                    continue
                mag = abs(coef)
                cuerpo = var if (mag == 1 and var) else f"{mag}{var}"
            else:
                if abs(coef) < 1e-12:
                    continue
                mag = abs(coef)
                cuerpo = f"{mag:.3f}{var}"
            signo = "-" if coef < 0 else "+"
            partes.append((signo, cuerpo))
        if not partes:
            return "0 = 0"
        s = ("-" if partes[0][0] == "-" else "") + partes[0][1]
        for signo, cuerpo in partes[1:]:
            s += f" {signo} {cuerpo}"
        return s + " = 0"

    def segment_in_box(l, xlim, ylim):
        """Dos puntos donde la recta ax+by+c=0 corta el borde de la ventana, o None si no la cruza."""
        a, b, c = (float(x) for x in l)
        cand = []
        if abs(b) > 1e-12:
            for x in xlim:
                y = -(a * x + c) / b
                if ylim[0] - 1e-9 <= y <= ylim[1] + 1e-9:
                    cand.append((x, y))
        if abs(a) > 1e-12:
            for y in ylim:
                x = -(b * y + c) / a
                if xlim[0] - 1e-9 <= x <= xlim[1] + 1e-9:
                    cand.append((x, y))
        unicos = []
        for p in cand:
            if all(abs(p[0] - q[0]) + abs(p[1] - q[1]) > 1e-9 for q in unicos):
                unicos.append(p)
        if len(unicos) < 2:
            return None
        unicos.sort()
        return unicos[0], unicos[-1]

    return cplx_tex, frac_tex, line_tex, num_tex, pmat, pt_tex, rat_tex, segment_in_box


@app.cell
def _(mo):
    mo.md(r"""
    ## B. Elegí la correspondencia

    Cuatro vértices de origen y cuatro de destino, **en orden**: el $i$-ésimo del origen va al $i$-ésimo del destino.
    El quinto vértice del origen (el que no elegiste) es el "vértice restante" cuya imagen queremos ver.

    **Cuántas hay.** Se eligen 4 de los 5 vértices como origen ($\binom{5}{4} = 5$ formas) y una asignación inyectiva
    de esos 4 sobre los 5 vértices ($5 \cdot 4 \cdot 3 \cdot 2 = 120$): en total $5 \cdot 120 = 600$ transformaciones
    proyectivas distintas donde cuatro vértices caen sobre vértices (la identidad incluida, cinco veces). Los ocho selectores
    permiten $120 \cdot 120 = 14400$ combinaciones, pero reordenar origen y destino *a la vez* da la misma $H$: por eso
    conviene dejar el origen en $ABCD$ y jugar sólo con el destino.

    **Presets vs. selectores.** En marimo cada variable global se define en una sola celda, así que un preset no puede
    "escribir" en los selectores ya creados. Lo que hago es el patrón de *UI dinámica*: la celda que crea los ocho
    selectores **depende del preset** y se vuelve a ejecutar con los valores del preset como defaults. Después podés cambiar
    cualquier selector a mano — los selectores siempre mandan; el preset sólo los inicializa (la opción "Personalizada"
    arranca en $ABCD \to BCDE$ y sirve para marcar que el mapeo es tuyo).
    """)
    return


@app.cell
def _(mo):
    preset = mo.ui.dropdown(
        options=[
            "Cíclica ABCD→BCDE",
            "Reflexión ABCD→EDCB",
            "ABCD→ECBD (tres puntos fijos)",
            "Personalizada",
        ],
        value="Cíclica ABCD→BCDE",
        label="Preset",
    )
    return (preset,)


@app.cell
def _(NOMBRES, mo, preset):
    _defaults = {
        "Cíclica ABCD→BCDE": ("ABCD", "BCDE"),
        "Reflexión ABCD→EDCB": ("ABCD", "EDCB"),
        "ABCD→ECBD (tres puntos fijos)": ("ABCD", "ECBD"),
        "Personalizada": ("ABCD", "BCDE"),
    }
    _o, _d = _defaults[preset.value]

    def _dd(v, label):
        return mo.ui.dropdown(options=NOMBRES, value=v, label=label)

    s1, s2, s3, s4 = (_dd(_o[i], f"origen {i + 1}") for i in range(4))
    d1, d2, d3, d4 = (_dd(_d[i], f"destino {i + 1}") for i in range(4))

    mo.vstack(
        [
            preset,
            mo.hstack([mo.md("**Origen**"), s1, s2, s3, s4], justify="start", gap=1),
            mo.hstack([mo.md("**Destino**"), d1, d2, d3, d4], justify="start", gap=1),
        ],
        gap=0.6,
    )
    return d1, d2, d3, d4, s1, s2, s3, s4


@app.cell
def _(
    NOMBRES,
    PTS,
    apply_h,
    classify,
    d1,
    d2,
    d3,
    d4,
    dehom,
    fixed_lines,
    fixed_points,
    homography,
    mo,
    np,
    s1,
    s2,
    s3,
    s4,
    vanishing_line,
):
    origen = [s1.value, s2.value, s3.value, s4.value]
    destino = [d1.value, d2.value, d3.value, d4.value]
    _rep_o = len(set(origen)) < 4
    _rep_d = len(set(destino)) < 4
    mo.stop(
        _rep_o or _rep_d,
        mo.callout(
            mo.md(
                "**Selección inválida.** "
                + ("Hay vértices repetidos en el **origen**. " if _rep_o else "")
                + ("Hay vértices repetidos en el **destino**. " if _rep_d else "")
                + "Cuatro puntos distintos de cada lado, si no la homografía no queda definida."
            ),
            kind="danger",
        ),
    )

    resto = next(n for n in NOMBRES if n not in origen)  # el vértice restante
    H_int, H_f = homography([PTS[n] for n in origen], [PTS[n] for n in destino])

    # Verificación exacta H p_i = s_i q_i (todo entero)
    verif = []
    for _no, _nd in zip(origen, destino):
        _v = H_int @ np.array([PTS[_no][0], PTS[_no][1], 1], dtype=np.int64)
        _s = int(_v[2])
        _ok = int(_v[0]) == _s * PTS[_nd][0] and int(_v[1]) == _s * PTS[_nd][1] and _s != 0
        verif.append((_no, _nd, [int(x) for x in _v], _s, _ok))

    v5 = [int(x) for x in H_int @ np.array([PTS[resto][0], PTS[resto][1], 1], dtype=np.int64)]
    l_inf = vanishing_line(H_int)
    autovalores = np.linalg.eigvals(H_f)
    pfijos = fixed_points(H_f)
    rfijas = fixed_lines(H_f)
    clase = classify(H_f)
    imagen = {n: dehom(apply_h(H_f, [PTS[n]])[0]) for n in NOMBRES}  # None si se fue al infinito

    mo.md(
        "Correspondencia activa: "
        + ", ".join(rf"${o} \mapsto {d}$" for o, d in zip(origen, destino))
        + rf". Vértice restante: ${resto}$."
    )
    return (
        H_f,
        H_int,
        autovalores,
        clase,
        destino,
        imagen,
        l_inf,
        origen,
        pfijos,
        resto,
        rfijas,
        v5,
        verif,
    )


@app.cell
def _(
    Fraction,
    H_int,
    PTS,
    autovalores,
    clase,
    cplx_tex,
    destino,
    frac_tex,
    line_tex,
    mo,
    num_tex,
    origen,
    pfijos,
    pmat,
    pt_tex,
    resto,
    rfijas,
    v5,
    verif,
):
    # Polinomio característico exacto (enteros): λ³ + c2 λ² + c1 λ + c0
    _M = [[int(x) for x in fila] for fila in H_int]
    _tr = _M[0][0] + _M[1][1] + _M[2][2]
    _m = (
        _M[0][0] * _M[1][1] - _M[0][1] * _M[1][0]
        + _M[0][0] * _M[2][2] - _M[0][2] * _M[2][0]
        + _M[1][1] * _M[2][2] - _M[1][2] * _M[2][1]
    )
    _det = (
        _M[0][0] * (_M[1][1] * _M[2][2] - _M[1][2] * _M[2][1])
        - _M[0][1] * (_M[1][0] * _M[2][2] - _M[1][2] * _M[2][0])
        + _M[0][2] * (_M[1][0] * _M[2][1] - _M[1][1] * _M[2][0])
    )

    def _term(c, mono):
        if c == 0:
            return ""
        s = " - " if c < 0 else " + "
        mag = "" if abs(c) == 1 and mono else str(abs(c))
        return s + mag + mono

    _charpoly = r"\lambda^3" + _term(-_tr, r"\lambda^2") + _term(_m, r"\lambda") + _term(-_det, "")

    _filas_ver = "\n".join(
        rf"| ${o} \mapsto {d}$ | $({v[0]},\ {v[1]},\ {v[2]})$ | ${s}$ | $({frac_tex(Fraction(v[0], s)) if s else '-'},\ {frac_tex(Fraction(v[1], s)) if s else '-'})$ | {'✓' if ok else '✗'} |"
        for o, d, v, s, ok in verif
    )

    if v5[2] != 0:
        _fx, _fy = Fraction(v5[0], v5[2]), Fraction(v5[1], v5[2])
        _img5 = (
            rf"$H\,{resto} = ({v5[0]},\ {v5[1]},\ {v5[2]}) \;\Rightarrow\; {resto}' = \left({frac_tex(_fx)},\ {frac_tex(_fy)}\right) "
            rf"= ({float(_fx):.4f},\ {float(_fy):.4f})$"
        )
    else:
        _img5 = (
            rf"$H\,{resto} = ({v5[0]},\ {v5[1]},\ 0)$: **punto impropio**, dirección $({v5[0]},\ {v5[1]})$ "
            rf"— el vértice restante está sobre la recta que se va al infinito."
        )

    _pf_lineas = []
    for p in pfijos:
        lam = cplx_tex(p["autovalor"])
        if p["tipo"] == "propio":
            _pf_lineas.append(rf"- $\lambda = {lam}$: punto fijo **propio** ${pt_tex(p['xy'])}$")
        elif p["tipo"] == "impropio":
            _pf_lineas.append(rf"- $\lambda = {lam}$: punto fijo **impropio**, dirección $({num_tex(p['dir'][0])},\ {num_tex(p['dir'][1])})$")
        elif p["tipo"] == "recta":
            _pf_lineas.append(rf"- $\lambda = {lam}$ (multiplicidad {p['mult_alg']}): **recta de puntos fijos** ${line_tex(p['recta'])}$")
        elif p["tipo"] == "todo":
            _pf_lineas.append(rf"- $\lambda = {lam}$: todos los puntos son fijos (identidad)")
        else:
            _pf_lineas.append(rf"- $\lambda = {lam}$: autovalor complejo, el punto fijo es imaginario (no hay punto real)")

    _rf_lineas = []
    for r in rfijas:
        lam = cplx_tex(r["autovalor"])
        if r["tipo"] == "recta":
            _rf_lineas.append(rf"- $\mu = {lam}$: recta fija ${line_tex(r['l'])}$")
        elif r["tipo"] == "haz":
            if r["centro_xy"] is not None:
                _rf_lineas.append(rf"- $\mu = {lam}$ (multiplicidad {r['mult_alg']}): **haz de rectas fijas** por el punto ${pt_tex(r['centro_xy'])}$")
            else:
                _rf_lineas.append(rf"- $\mu = {lam}$ (multiplicidad {r['mult_alg']}): **haz de rectas fijas** paralelas de dirección $({num_tex(r['centro'][0])},\ {num_tex(r['centro'][1])})$")
        elif r["tipo"] == "todas":
            _rf_lineas.append(rf"- $\mu = {lam}$: todas las rectas son fijas (identidad)")
        else:
            _rf_lineas.append(rf"- $\mu = {lam}$: complejo, sin recta fija real")

    _es_afin = abs(int(H_int[2, 0])) == 0 and abs(int(H_int[2, 1])) == 0

    mo.md(
        rf"""
    ## C. Resultados para ${''.join(origen)} \to {''.join(destino)}$

    **Matriz** (entera, normalizada al mínimo común múltiplo de los denominadores de $B A^{{-1}}$, coprimos, $h_{{33}} > 0$):

    $$H = {pmat(H_int)}$$

    **Verificación $H p_i \sim q_i$** (el factor de escala $s_i$ es la tercera componente porque $q_i$ tiene $w = 1$):

    | correspondencia | $H p_i = (x, y, w)$ | $s_i$ | $(x/w,\ y/w)$ | |
    |---|---|---|---|---|
    {_filas_ver}

    **Imagen del vértice restante ${resto} = {pt_tex(PTS[resto])}$:** {_img5}

    **Recta que se va al infinito** (tercera fila de $H$): {
        rf"$w' = {int(H_int[2, 2])}\,w$, no hay recta propia que se vaya al infinito: la recta del infinito $w = 0$ es fija y la transformación es **afín**."
        if _es_afin else rf"${line_tex([int(x) for x in H_int[2]])}$"
    }

    **Polinomio característico:** ${_charpoly} = 0$ &nbsp;·&nbsp; **autovalores:** {", ".join(rf"${cplx_tex(z)}$" for z in autovalores)}

    **Puntos fijos** (autovectores de $H$):

    {chr(10).join(_pf_lineas)}

    **Rectas fijas** (autovectores de $H^T$):

    {chr(10).join(_rf_lineas)}

    **Clasificación:** {clase}.
    """
    )
    return


@app.cell
def _(
    NOMBRES,
    PTS,
    imagen,
    l_inf,
    np,
    pfijos,
    plt,
    resto,
    rfijas,
    segment_in_box,
    v5,
):
    # ---------- gráfico principal ----------
    _orig = np.array([PTS[n] for n in NOMBRES])
    _img_fin = {n: p for n, p in imagen.items() if p is not None}
    _prop = [p["xy"] for p in pfijos if p["tipo"] == "propio"]

    # ventana: original + imagen + puntos fijos propios, con margen, acotada a [-12, 12].
    # Un punto fijo (o una imagen) más allá de ±12 no entra en la ventana: se anota en el título.
    _dentro = lambda p: bool(np.abs(p).max() <= 12.0)  # noqa: E731
    _pts_win = list(_orig) + [p for p in _img_fin.values() if _dentro(p)] + [np.asarray(p) for p in _prop if _dentro(p)]
    _P = np.array(_pts_win, dtype=float)
    _lo = np.maximum(_P.min(axis=0) - 1.0, -13.0)
    _hi = np.minimum(_P.max(axis=0) + 1.0, 13.0)
    _lado = float(max(_hi - _lo))
    _c = (_lo + _hi) / 2
    _xlim = (float(_c[0] - _lado / 2), float(_c[0] + _lado / 2))
    _ylim = (float(_c[1] - _lado / 2), float(_c[1] + _lado / 2))
    _fuera = [
        p for p in _prop
        if not (_xlim[0] <= p[0] <= _xlim[1] and _ylim[0] <= p[1] <= _ylim[1])
    ]
    _img_fuera = [n for n, p in _img_fin.items() if not (_xlim[0] <= p[0] <= _xlim[1] and _ylim[0] <= p[1] <= _ylim[1])]

    _fig, _ax = plt.subplots(figsize=(6.4, 6.4), dpi=90)

    # pentágono original (gris)
    _cyc = np.vstack([_orig, _orig[:1]])
    _ax.plot(_cyc[:, 0], _cyc[:, 1], "-o", color="gray", lw=1.5, ms=5, label="original")
    for _n, _p in zip(NOMBRES, _orig):
        _ax.annotate(rf"${_n}$", _p, textcoords="offset points", xytext=(6, 6), color="dimgray", fontsize=11)

    # imagen (rojo): polígono con los vértices finitos, en el orden A..E
    _img_seq = [imagen[n] for n in NOMBRES]
    _seg = np.array([p if p is not None else [np.nan, np.nan] for p in _img_seq] + [_img_seq[0] if _img_seq[0] is not None else [np.nan, np.nan]], dtype=float)
    _ax.plot(_seg[:, 0], _seg[:, 1], "-", color="tab:red", lw=1.8, label="imagen $H$")
    for _n in NOMBRES:
        _p = imagen[_n]
        if _p is None:
            continue
        if _n == resto:
            _ax.plot(_p[0], _p[1], marker="D", color="tab:red", ms=9, mec="black", mew=1.2, ls="none",
                     label=rf"${resto}'$ (vértice restante)")
        else:
            _ax.plot(_p[0], _p[1], "o", color="tab:red", ms=5)
        _ax.annotate(rf"${_n}'$", _p, textcoords="offset points", xytext=(6, -12), color="tab:red", fontsize=11)

    # quinto vértice al infinito: flecha de dirección desde el centroide de la imagen
    if imagen[resto] is None:
        _cen = np.mean(list(_img_fin.values()), axis=0)
        _d = np.array(v5[:2], dtype=float)
        _d = _d / np.linalg.norm(_d) * _lado * 0.35
        _ax.annotate("", xy=_cen + _d, xytext=_cen,
                     arrowprops=dict(arrowstyle="-|>", color="tab:red", lw=2))
        _ax.annotate(rf"${resto}' \to \infty$", _cen + _d, textcoords="offset points", xytext=(4, 4), color="tab:red")

    # recta que se va al infinito (naranja punteada)
    _sv = segment_in_box(l_inf, _xlim, _ylim)
    if _sv is not None:
        (_x0, _y0), (_x1, _y1) = _sv
        _ax.plot([_x0, _x1], [_y0, _y1], ls=":", color="tab:orange", lw=2, label=r"recta $\to \infty$ (fila 3 de $H$)")

    # rectas fijas (verde punteado fino) y puntos fijos propios (estrellas verdes)
    _lab_rf = False
    for _r in rfijas:
        for _l in ([_r["l"]] if _r["tipo"] == "recta" else []):
            _s = segment_in_box(_l, _xlim, _ylim)
            if _s is not None:
                (_x0, _y0), (_x1, _y1) = _s
                _ax.plot([_x0, _x1], [_y0, _y1], ls="--", color="tab:green", lw=0.9,
                         label=None if _lab_rf else "rectas fijas")
                _lab_rf = True
    for _p in pfijos:
        if _p["tipo"] == "recta":
            _s = segment_in_box(_p["recta"], _xlim, _ylim)
            if _s is not None:
                (_x0, _y0), (_x1, _y1) = _s
                _ax.plot([_x0, _x1], [_y0, _y1], ls="-", color="tab:green", lw=2.2, alpha=0.6, label="recta de puntos fijos")
    _lab_pf = False
    for _p in _prop:
        _ax.plot(_p[0], _p[1], marker="*", color="tab:green", ms=16, mec="darkgreen", ls="none",
                 label=None if _lab_pf else "punto fijo propio")
        _lab_pf = True
    for _p in pfijos:
        if _p["tipo"] == "impropio":
            _d = np.asarray(_p["dir"]) * _lado * 0.25
            _ax.annotate("", xy=_d, xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", color="tab:green", lw=1.5, ls="--"))
            _ax.annotate("dirección fija", _d, textcoords="offset points", xytext=(4, 4), color="tab:green", fontsize=9)

    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.set_xlim(*_xlim)
    _ax.set_ylim(*_ylim)
    _ax.set_aspect("equal")
    _ax.legend(loc="upper left", fontsize=8)
    _titulo = rf"$ABCDE \mapsto H(ABCDE)$ — vértice restante ${resto}$"
    _notas = []
    if _fuera:
        _notas.append(f"{len(_fuera)} punto(s) fijo(s) fuera de la ventana [-12, 12]: " + ", ".join(f"({p[0]:.1f}, {p[1]:.1f})" for p in _fuera))
    if _img_fuera:
        _notas.append("imagen fuera de la ventana: " + ", ".join(f"${n}'$" for n in _img_fuera))
    if _sv is None and abs(l_inf[0]) + abs(l_inf[1]) > 1e-12:
        _notas.append(r"recta $\to\infty$ fuera de la ventana")
    if any(_r["tipo"] == "recta" and segment_in_box(_r["l"], _xlim, _ylim) is None for _r in rfijas):
        _notas.append("alguna recta fija fuera de la ventana")
    if _notas:
        _titulo += "\n(" + "; ".join(_notas) + ")"
    _ax.set_title(_titulo, fontsize=10)
    _fig
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## D. Explorá: de la identidad a $H$

    Para "ver" la transformación conviene recorrerla de a poco. Lo ideal sería la **geodésica** $H_t = \exp(t \log H)$
    (que requeriría `scipy.linalg.logm/expm`, no disponible acá). En su lugar usamos la **interpolación lineal en el
    espacio de matrices**

    $$H_t = (1 - t)\,I + t\,\tilde H, \qquad t \in [0, 1],$$

    con $\tilde H = H / \lambda_*$, donde $\lambda_*$ es el autovalor real de mayor módulo (el positivo si hay empate,
    como en la reflexión; así el punto fijo principal tiene autovalor $1$ y $\tilde H$ "apunta" del mismo lado que la identidad). **Advertencia:** no es una geodésica, es un
    camino recto entre dos matrices; en el medio $H_t$ puede pasar por matrices singulares (por ejemplo en la reflexión,
    que tiene un autovalor $-1$: en $t = 1/2$ todo el plano se aplasta sobre el eje).

    Lo que sí es exacto para cualquier $t$: **los autovectores de $H$ son autovectores de $H_t$** (con autovalor
    $(1 - t) + t\lambda$), así que los puntos fijos se quedan quietos durante todo el viaje. Mové el slider y mirá cómo el
    vértice restante viaja hacia su imagen mientras la estrella verde no se mueve.
    """)
    return


@app.cell
def _(mo):
    t_sl = mo.ui.slider(start=0.0, stop=1.0, step=0.01, value=0.5, label="t")
    return (t_sl,)


@app.cell
def _(H_f, NOMBRES, PTS, apply_h, dehom, mo, np, pfijos, plt, pmat, resto, t_sl):
    _w = np.linalg.eigvals(H_f)
    _reales = [z.real for z in _w if abs(z.imag) < 1e-6 * np.abs(_w).max()]
    lam_p = max(_reales, key=lambda z: (round(abs(z), 9), z))  # mayor módulo; en empate, el positivo
    H_n = H_f / lam_p  # autovalor real principal = 1
    t = float(t_sl.value)
    H_t = (1 - t) * np.eye(3) + t * H_n

    _orig = np.array([PTS[n] for n in NOMBRES], dtype=float)
    _cyc = np.vstack([_orig, _orig[:1]])

    def _poly_at(tt):
        Hh = (1 - tt) * np.eye(3) + tt * H_n
        return [dehom(v) for v in apply_h(Hh, _orig)]

    _act = _poly_at(t)
    _fin = _poly_at(1.0)

    # trayectorias t: 0 → 1 (NaN donde el punto se va al infinito o muy lejos)
    _ts = np.linspace(0, 1, 201)
    _tray = np.full((len(NOMBRES), len(_ts), 2), np.nan)
    for _i, _tt in enumerate(_ts):
        for _j, _p in enumerate(_poly_at(_tt)):
            if _p is not None and np.abs(_p).max() <= 40:
                _tray[_j, _i] = _p

    _prop = [p["xy"] for p in pfijos if p["tipo"] == "propio"]
    _dentro = lambda p: bool(np.abs(p).max() <= 12.0)  # noqa: E731
    _pts_win = list(_orig) + [p for p in _fin + _act if p is not None and _dentro(p)] + [np.asarray(p) for p in _prop if _dentro(p)]
    _P = np.array(_pts_win, dtype=float)
    _lo = np.maximum(_P.min(axis=0) - 1.0, -13.0)
    _hi = np.minimum(_P.max(axis=0) + 1.0, 13.0)
    _lado = float(max(_hi - _lo))
    _c = (_lo + _hi) / 2

    _fig, _ax = plt.subplots(figsize=(5.6, 5.6), dpi=90)
    _ax.plot(_cyc[:, 0], _cyc[:, 1], "-o", color="gray", lw=1.2, ms=4, label="$t = 0$ (original)")
    _seg_fin = np.array([p if p is not None else [np.nan, np.nan] for p in _fin + [_fin[0]]], dtype=float)
    _ax.plot(_seg_fin[:, 0], _seg_fin[:, 1], "-", color="tab:red", lw=1.0, alpha=0.35, label="$t = 1$ (imagen)")
    for _j, _n in enumerate(NOMBRES):
        _ax.plot(_tray[_j, :, 0], _tray[_j, :, 1], "-", color="tab:blue", lw=0.8, alpha=0.5)
    _seg_act = np.array([p if p is not None else [np.nan, np.nan] for p in _act + [_act[0]]], dtype=float)
    _ax.plot(_seg_act[:, 0], _seg_act[:, 1], "-o", color="tab:blue", lw=2, ms=5, label=rf"$H_t$, $t = {t:.2f}$")
    for _j, _n in enumerate(NOMBRES):
        _p = _act[_j]
        if _p is None:
            continue
        if _n == resto:
            _ax.plot(_p[0], _p[1], marker="D", color="tab:blue", ms=9, mec="black", mew=1.2, ls="none")
        _ax.annotate(rf"${_n}$", _p, textcoords="offset points", xytext=(5, 5), color="tab:blue", fontsize=10)
    for _p in _prop:
        _ax.plot(_p[0], _p[1], marker="*", color="tab:green", ms=16, mec="darkgreen", ls="none", label="punto fijo")

    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.set_xlim(float(_c[0] - _lado / 2), float(_c[0] + _lado / 2))
    _ax.set_ylim(float(_c[1] - _lado / 2), float(_c[1] + _lado / 2))
    _ax.set_aspect("equal")
    _ax.legend(loc="upper left", fontsize=8)
    _ax.set_title(rf"$H_t = (1-t)\,I + t\,\tilde H$,  $t = {t:.2f}$", fontsize=10)

    _controles = mo.vstack(
        [
            mo.md("**Controles**"),
            t_sl,
            mo.md(rf"$\lambda_* = {lam_p:.4f}$, $\tilde H = H/\lambda_*$"),
            mo.md(rf"$H_t = {pmat(H_t, lambda x: f'{x:.3f}')}$"),
            mo.md(rf"$\det H_t = {np.linalg.det(H_t):.4f}$"),
            mo.md("Trazos azules finos: trayectoria de cada vértice con $t$ de 0 a 1."),
        ],
        gap=0.6,
    )
    mo.hstack([_controles, _fig], justify="start", align="start", gap=2)
    return


@app.cell
def _(
    PTS,
    apply_h,
    classify,
    dehom,
    fixed_lines,
    fixed_points,
    homography,
    mo,
    np,
):
    # ---------- verificación automática contra valores de referencia ----------
    _fallas = []

    def _chk(cond, msg):
        if not cond:
            _fallas.append(msg)

    def _mapa(o, d):
        return homography([PTS[c] for c in o], [PTS[c] for c in d])

    def _tiene(vals, z, tol=1e-6):
        return any(abs(v - z) <= tol * max(1.0, abs(z)) for v in vals)

    def _norm_l(l):
        l = np.asarray(l, float)
        l = l / np.abs(l).max()
        i = next(k for k in range(3) if abs(l[k]) > 1e-9)
        return l / l[i]

    try:
        # 1) Cíclica ABCD → BCDE
        _Hi, _Hf = _mapa("ABCD", "BCDE")
        _ref = np.array([[24, 60, 12], [-30, 23, -5], [6, 5, 49]])
        _chk(np.array_equal(_Hi, _ref), f"cíclica: H = {_Hi.tolist()} ≠ {_ref.tolist()}")
        _E = dehom(apply_h(_Hf, [PTS["E"]])[0])
        _chk(_E is not None and np.allclose(_E, [0, -11 / 7]), f"cíclica: E' = {_E} ≠ (0, -11/7)")
        _chk(np.allclose(_norm_l(_Hf[2]), _norm_l([6, 5, 49])), "cíclica: recta al infinito ≠ 6x+5y+49=0")
        _w = np.linalg.eigvals(_Hf)
        _chk(_tiene(_w, 48) and _tiene(_w, 24 + 24j * np.sqrt(3)) and _tiene(_w, 24 - 24j * np.sqrt(3)),
             f"cíclica: autovalores {_w} ≠ 48, 24±24√3 i")
        _pf = [p for p in fixed_points(_Hf) if p["tipo"] in ("propio", "impropio", "recta")]
        _chk(len(_pf) == 1 and _pf[0]["tipo"] == "propio" and np.allclose(_pf[0]["xy"], [0, -0.2]),
             f"cíclica: puntos fijos {_pf} ≠ único propio (0, -1/5)")
        _rf = [r for r in fixed_lines(_Hf) if r["tipo"] in ("recta", "haz")]
        _chk(len(_rf) == 1 and _rf[0]["tipo"] == "recta" and np.allclose(_norm_l(_rf[0]["l"]), _norm_l([0, 1, 5])),
             f"cíclica: rectas fijas {_rf} ≠ única y = -5")
        _chk(classify(_Hf).startswith("uno real + par complejo"), f"cíclica: clasificación '{classify(_Hf)}'")

        # 2) Reflexión ABCD → EDCB
        _Hi, _Hf = _mapa("ABCD", "EDCB")
        _chk(np.array_equal(_Hi, np.diag([-1, 1, 1])), f"reflexión: H = {_Hi.tolist()} ≠ diag(-1,1,1)")
        _E = dehom(apply_h(_Hf, [PTS["E"]])[0])
        _chk(_E is not None and np.allclose(_E, PTS["A"]), f"reflexión: E' = {_E} ≠ A")
        _w = np.sort(np.real(np.linalg.eigvals(_Hf)))
        _chk(np.allclose(_w, [-1, 1, 1]), f"reflexión: autovalores {_w} ≠ -1, 1, 1")
        _chk(classify(_Hf).startswith("autovalores repetidos"), f"reflexión: clasificación '{classify(_Hf)}'")

        # 3) ABCD → ECBD (tres puntos fijos)
        _Hi, _Hf = _mapa("ABCD", "ECBD")
        _ref = np.array([[48, -24, 168], [34, -13, 7], [22, -31, 61]])
        _chk(np.array_equal(_Hi, _ref), f"ECBD: H = {_Hi.tolist()} ≠ {_ref.tolist()}")
        _E = dehom(apply_h(_Hf, [PTS["E"]])[0])
        _chk(_E is not None and np.allclose(_E, [36 / 17, 11 / 17]), f"ECBD: E' = {_E} ≠ (36/17, 11/17)")
        _w = np.linalg.eigvals(_Hf)
        _chk(_tiene(_w, 96) and _tiene(_w, 24 * np.sqrt(2)) and _tiene(_w, -24 * np.sqrt(2)),
             f"ECBD: autovalores {_w} ≠ 96, ±24√2")
        _pf = fixed_points(_Hf)
        _chk(any(p["tipo"] == "propio" and np.allclose(p["xy"], PTS["D"]) for p in _pf),
             f"ECBD: D no aparece como punto fijo en {_pf}")
        _chk(classify(_Hf).startswith("tres reales distintos"), f"ECBD: clasificación '{classify(_Hf)}'")

        # 4) identidad
        _Hi, _Hf = _mapa("ABCD", "ABCD")
        _chk(np.array_equal(_Hi, np.eye(3, dtype=int)), f"identidad: H = {_Hi.tolist()}")
        _chk(classify(_Hf) == "identidad", f"identidad: clasificación '{classify(_Hf)}'")
    except Exception as _e:  # noqa: BLE001
        _fallas.append(f"excepción: {type(_e).__name__}: {_e}")

    verificacion_ok = not _fallas
    mo.output.append(mo.callout(
        mo.md(
            "**Verificación OK** — H entera, imagen de $E$, recta al infinito, autovalores, puntos y rectas fijas "
            "coinciden con los valores de referencia para $ABCD \\to BCDE$, $ABCD \\to EDCB$, $ABCD \\to ECBD$ y la identidad."
        )
        if verificacion_ok
        else mo.md("**Verificación FALLÓ**\n\n" + "\n".join(f"- {f}" for f in _fallas)),
        kind="success" if verificacion_ok else "danger",
    ))
    assert verificacion_ok, "\n".join(_fallas)
    return


if __name__ == "__main__":
    app.run()
