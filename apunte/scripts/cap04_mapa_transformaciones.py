"""Mapa de las transformaciones del plano (capítulo «Afinidades y coordenadas homogéneas»).

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  P   El predio: pentágono convexo A B C D E con AB paralelo a DE, la diagonal AC, su punto
      medio M y el punto Q a un cuarto de AC (para la razón doble de A, Q, M, C).
  T   Las ocho transformaciones con sus parámetros: traslación, rotación, reflexión,
      movimiento rígido, similaridad, afín, proyectiva y conforme. Similaridad, afín y
      proyectiva tienen además una variante con determinante negativo (sólo para la medición
      del sentido de giro; la figura muestra la variante directa).
  M   Medición antes y después: cocientes de distancias entre vértices, ángulos entre las
      curvas imagen en cada vértice (con la jacobiana), sentido de giro (signo del área),
      cociente de áreas (contorno muestreado), paralelismo de AB y DE, rectas (desvío de los
      lados muestreados respecto de su cuerda), punto medio de AC y razón doble de A, Q, M, C.
      Para la conforme se repite la medición en el predio achicado alrededor de su centroide
      (factor s = 1; 0,1; 0,01) y se comprueba que la discrepancia decrece.
  T1  La tabla «Qué se conserva» medida, comparada celda por celda con TABLA1 (la tabla tal
      como está escrita en el .tex) y con el texto del .tex entre los marcadores
      «% tabla-conserva:inicio» y «% tabla-conserva:fin». Si algo no coincide, exit 1.
  E1  Ejercicio 1: tres pares de puntos homólogos; residuos de los ajustes rígido,
      similaridad y afín.
  E2  Ejercicio 2: plano escaneado con cinco puntos de apoyo; residuos de los ajustes rígido,
      similaridad, afín y proyectivo (mínimos cuadrados).

Figura (PDF determinista, sin fecha ni productor) en apunte/figuras/afines/:
  cap04_mapa_transformaciones.pdf  grilla 2 x 4, el mismo predio (gris, punteado) y su imagen
                                   (teal, continuo) por cada una de las ocho familias.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap04_mapa_transformaciones.py
"""
import re
import sys
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=6, suppress=True)
RAIZ = Path(__file__).resolve().parents[2]
SALIDA = RAIZ / "apunte" / "figuras" / "afines"
SALIDA.mkdir(parents=True, exist_ok=True)
TEX = RAIZ / "apunte" / "contenido" / "04-afinidades-homogeneas.tex"
# Paleta del proyecto (tools/animaciones/_comun.py, PALETA): teal, gris, tinta.
TEAL, GRIS, TINTA = "#01696F", "#9AA0A6", "#2b2b2b"
plt.rcParams.update({"font.size": 8, "axes.edgecolor": GRIS, "savefig.facecolor": "white",
                     "pdf.compression": 9})
deg = np.pi / 180
TOL = 1e-8


def R(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


# ---------------------------------------------------------------- P
print("=== P  predio ===")
NOMBRES = "ABCDE"
PREDIO = np.array([[0.0, 0.0], [4.0, 0.0], [5.0, 1.8], [3.0, 3.0], [0.5, 3.0]])
for n, p in zip(NOMBRES, PREDIO):
    print(f"{n} = ({p[0]:g}, {p[1]:g})")
print("AB paralelo a DE; diagonal AC; M = punto medio de AC; Q = A + (C - A)/4")


def puntos_notables(P):
    A, C = P[0], P[2]
    return {"M": (A + C) / 2, "Q": A + (C - A) / 4}


# ---------------------------------------------------------------- T
def afin(A, b):
    A, b = np.asarray(A, float), np.asarray(b, float)
    return lambda X: np.atleast_2d(np.asarray(X, float)) @ A.T + b


def proyectiva(H):
    H = np.asarray(H, float)

    def f(X):
        X = np.atleast_2d(np.asarray(X, float))
        Y = np.c_[X, np.ones(len(X))] @ H.T
        return Y[:, :2] / Y[:, 2:]
    return f


EPS = 0.12
Z0 = np.array([3.0, 2.6])


def conforme(X):
    """f(z) = z0 + (exp(eps z) - 1)/eps, con z = x + i y: analítica, f'(z) = exp(eps z) != 0."""
    X = np.atleast_2d(np.asarray(X, float))
    z = X[:, 0] + 1j * X[:, 1]
    w = (np.exp(EPS * z) - 1) / EPS
    return np.c_[w.real, w.imag] + Z0


# Parámetros (los del texto)
V_TRAS = np.array([4.5, 3.0])
C_ROT, TH_ROT = np.array([0.0, 0.0]), 50 * deg
# Reflexión en la recta L: n . x = h con n = (1, 1), h = 7 (la recta x + y = 7)
N_REF, H_REF = np.array([1.0, 1.0]), 7.0
A_REF = np.eye(2) - 2 * np.outer(N_REF, N_REF) / (N_REF @ N_REF)
B_REF = 2 * H_REF / (N_REF @ N_REF) * N_REF
TH_RIG, V_RIG = -30 * deg, np.array([4.0, 5.0])
LAM_SIM, TH_SIM, T_SIM = 0.6, 110 * deg, np.array([8.0, 2.5])
A_AF, B_AF = np.array([[1.25, 0.55], [0.15, 0.75]]), np.array([3.8, 2.6])
H_PR = np.array([[1.0, 0.15, 4.0], [0.05, 0.95, 3.0], [0.07, 0.05, 1.0]])
REFL_X = np.diag([1.0, -1.0])

FAMILIAS = ["traslacion", "rotacion", "reflexion", "rigido", "similaridad", "afin", "proyectiva",
            "conforme"]
ROTULO = {"traslacion": "Traslación", "rotacion": "Rotación", "reflexion": "Reflexión",
          "rigido": "Movimiento rígido", "similaridad": "Similaridad", "afin": "Afín",
          "proyectiva": "Proyectiva", "conforme": "Conforme"}
# (función, det de la parte lineal o de H); la primera variante es la que se dibuja
VARIANTES = {
    "traslacion": [(afin(np.eye(2), V_TRAS), 1.0)],
    "rotacion": [(afin(R(TH_ROT), (np.eye(2) - R(TH_ROT)) @ C_ROT), 1.0)],
    "reflexion": [(afin(A_REF, B_REF), np.linalg.det(A_REF))],
    "rigido": [(afin(R(TH_RIG), V_RIG), 1.0)],
    "similaridad": [(afin(LAM_SIM * R(TH_SIM), T_SIM), LAM_SIM ** 2),
                    (afin(LAM_SIM * R(TH_SIM) @ REFL_X, T_SIM), -LAM_SIM ** 2)],
    "afin": [(afin(A_AF, B_AF), np.linalg.det(A_AF)),
             (afin(A_AF @ REFL_X, B_AF), np.linalg.det(A_AF @ REFL_X))],
    "proyectiva": [(proyectiva(H_PR), np.linalg.det(H_PR)),
                   (proyectiva(H_PR @ np.diag([1.0, -1.0, 1.0])),
                    np.linalg.det(H_PR @ np.diag([1.0, -1.0, 1.0])))],
    "conforme": [(conforme, None)],
}

print("\n=== T  transformaciones ===")
print(f"traslación: v = {V_TRAS}")
print(f"rotación: centro c = {C_ROT}, theta = {TH_ROT / deg:g}°")
print(f"reflexión: recta L: x + y = {H_REF:g};  A = {A_REF.tolist()}, b = {B_REF}, det = "
      f"{np.linalg.det(A_REF):+.0f}")
print(f"movimiento rígido: R({TH_RIG / deg:g}°) x + {V_RIG}")
print(f"similaridad: {LAM_SIM:g} R({TH_SIM / deg:g}°) x + {T_SIM}  (variante inversa con diag(1,-1))")
print(f"afín: A = {A_AF.tolist()}, b = {B_AF}, det A = {np.linalg.det(A_AF):.4f}")
print(f"proyectiva: H = {H_PR.tolist()}, det H = {np.linalg.det(H_PR):.6f}")
W = np.c_[PREDIO, np.ones(5)] @ H_PR[2]
print(f"  W en los vértices = {np.round(W, 3)} (todos > 0: la recta que va al infinito no corta "
      "al predio)")
print(f"conforme: f(z) = z0 + (exp(eps z) - 1)/eps, eps = {EPS:g}, z0 = {Z0}; "
      f"k(p) = |f'(p)| = exp(eps x)")
kv = np.exp(EPS * PREDIO[:, 0])
print(f"  k en los vértices = {np.round(kv, 3)}  (de {kv.min():.3f} a {kv.max():.3f})")


# ---------------------------------------------------------------- M
def jacobiana(f, p, h=1e-5):
    J = np.zeros((2, 2))
    for j in range(2):
        e = np.zeros(2)
        e[j] = h
        J[:, j] = (f(p + e)[0] - f(p - e)[0]) / (2 * h)
    return J


def contorno(P, n=400):
    t = np.linspace(0, 1, n, endpoint=False)[:, None]
    return np.vstack([P[i] + t * (P[(i + 1) % len(P)] - P[i]) for i in range(len(P))])


def area_signada(X):
    x, y = X[:, 0], X[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def angulo(u, v):
    return np.arctan2(abs(u[0] * v[1] - u[1] * v[0]), u @ v)


def razon_doble(a, b, c, d):
    return (c - a) * (d - b) / ((c - b) * (d - a))


def medir(f, P):
    """Discrepancias de cada propiedad entre el predio P y su imagen por f."""
    n = len(P)
    I = f(P)
    pares = [(i, j) for i in range(n) for j in range(i + 1, n)]
    r = np.array([np.linalg.norm(I[i] - I[j]) / np.linalg.norm(P[i] - P[j]) for i, j in pares])
    ang = []
    for i in range(n):
        u, v = P[(i + 1) % n] - P[i], P[i - 1] - P[i]
        J = jacobiana(f, P[i])
        ang.append(abs(angulo(J @ u, J @ v) - angulo(u, v)))
    a0, a1 = area_signada(contorno(P)), area_signada(f(contorno(P)))
    u, v = I[1] - I[0], I[3] - I[4]
    paral = abs(u[0] * v[1] - u[1] * v[0]) / (np.linalg.norm(u) * np.linalg.norm(v))
    desv = 0.0
    t = np.linspace(0, 1, 51)[:, None]
    for i, j in [(k, (k + 1) % n) for k in range(n)] + [(0, 2)]:
        S = f(P[i] + t * (P[j] - P[i]))
        d = S[-1] - S[0]
        nrm = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        desv = max(desv, np.max(np.abs((S - S[0]) @ nrm)) / np.linalg.norm(d))
    pn = puntos_notables(P)
    fA, fC = I[0], I[2]
    fM, fQ = f(pn["M"])[0], f(pn["Q"])[0]
    medio = np.linalg.norm(fM - (fA + fC) / 2) / np.linalg.norm(fC - fA)
    u = fC - fA
    coord = lambda X: (X - fA) @ u / (u @ u)
    rd0 = razon_doble(0.0, 0.25, 0.5, 1.0)
    rd1 = razon_doble(0.0, coord(fQ), coord(fM), 1.0)
    return dict(r=r, ang=max(ang), a0=a0, a1=a1, paral=paral, desv=desv, medio=medio,
                rd=abs(rd1 - rd0), rd1=rd1, I=I)


def clasificar_global(m, det):
    r = m["r"]
    c = {}
    if np.max(np.abs(r - 1)) < TOL:
        c["distancias"] = "si"
    elif np.ptp(r) / r.mean() < TOL:
        c["distancias"] = "xk"
    else:
        c["distancias"] = "no"
    c["angulos"] = "si" if m["ang"] < 1e-6 else "no"
    c["sentido"] = "si" if np.sign(m["a0"]) == np.sign(m["a1"]) else "no"
    rho = m["a1"] / m["a0"]
    if abs(abs(rho) - 1) < 1e-6:
        c["areas"] = "si"
    elif c["distancias"] == "xk" and abs(abs(rho) - r.mean() ** 2) < 1e-6:
        c["areas"] = "xk2"
    elif det is not None and m["paral"] < TOL and abs(abs(rho) - abs(det)) < 1e-6:
        c["areas"] = "xdet"
    else:
        c["areas"] = "no"
    c["paralelismo"] = "si" if m["paral"] < TOL else "no"
    c["rectas"] = "si" if m["desv"] < TOL else "no"
    c["medio"] = "si" if m["medio"] < TOL else "no"
    c["razon_doble"] = "si" if m["rd"] < TOL else "no"
    return c


FILAS = ["distancias", "angulos", "sentido", "areas", "paralelismo", "rectas", "medio",
         "razon_doble"]
ROT_FILA = {"distancias": "Distancias", "angulos": "Ángulos", "sentido": "Sentido de giro",
            "areas": "Áreas", "paralelismo": "Paralelismo", "rectas": "Rectas",
            "medio": "Punto medio (razón simple)", "razon_doble": "Razón doble"}

print("\n=== M  medición (predio de tamaño real) ===")
MEDIDO = {}
for fam in FAMILIAS:
    cods = []
    for f, det in VARIANTES[fam]:
        m = medir(f, PREDIO)
        cods.append((clasificar_global(m, det), det, m))
    # combinar variantes: si el sentido de giro difiere, tiene que seguir al signo del det
    comb = {}
    for fila in FILAS:
        vals = [c[fila] for c, _, _ in cods]
        if len(set(vals)) == 1:
            comb[fila] = vals[0]
        elif fila == "sentido" and all((v == "si") == (d > 0) for v, (_, d, _) in zip(vals, cods)):
            comb[fila] = "sgn"
        else:
            comb[fila] = "?" + "/".join(vals)
    MEDIDO[fam] = comb
    m = cods[0][2]
    print(f"{ROTULO[fam]:18s} d'/d en [{m['r'].min():.4f}, {m['r'].max():.4f}]  "
          f"máx |Δángulo| = {m['ang'] / deg:.3f}°  área: {m['a0']:.3f} -> {m['a1']:+.3f} "
          f"(x{m['a1'] / m['a0']:+.4f})  sen(AB, DE) = {m['paral']:.4f} "
          f"({np.degrees(np.arcsin(m['paral'])):.2f}°)  "
          f"desvío de rectas = {m['desv']:.4f}  punto medio = {m['medio']:.4f}  "
          f"razón doble = {m['rd1']:.4f} (antes 1,5)")
    if fam in ("similaridad", "afin", "proyectiva"):
        for c, d, mm in cods:
            print(f"    variante det = {d:+.4f}: área con signo {mm['a0']:.3f} -> {mm['a1']:+.3f}")

# Conforme: «localmente» = la discrepancia decrece al achicar el predio alrededor de su centroide G
print("\n--- conforme: predio achicado alrededor del centroide G ---")
_x, _y = PREDIO[:, 0], PREDIO[:, 1]
_c = _x * np.roll(_y, -1) - np.roll(_x, -1) * _y
G = np.array([np.sum((_x + np.roll(_x, -1)) * _c), np.sum((_y + np.roll(_y, -1)) * _c)]) \
    / (3 * np.sum(_c))
kG = np.exp(EPS * G[0])
print(f"G (centroide del área) = {np.round(G, 4)}, k(G) = {kG:.6f}")
LOCAL = {}
disc = {k: [] for k in FILAS}
for s in (1.0, 0.1, 0.01):
    Ps = G + s * (PREDIO - G)
    m = medir(conforme, Ps)
    disc["distancias"].append(np.max(np.abs(m["r"] / kG - 1)))
    disc["areas"].append(abs(m["a1"] / m["a0"] / kG ** 2 - 1))
    disc["paralelismo"].append(m["paral"])
    disc["rectas"].append(m["desv"])
    disc["medio"].append(m["medio"])
    disc["razon_doble"].append(m["rd"])
    disc["angulos"].append(m["ang"])
    disc["sentido"].append(float(np.sign(m["a0"]) != np.sign(m["a1"])))
    print(f"s = {s:<5g} máx|d'/d / k(G) - 1| = {disc['distancias'][-1]:.2e}  "
          f"|área'/área / k(G)^2 - 1| = {disc['areas'][-1]:.2e}  sen(AB, DE) = {m['paral']:.2e}  "
          f"rectas = {m['desv']:.2e}  punto medio = {m['medio']:.2e}  "
          f"razón doble = {m['rd']:.2e}  ángulos = {m['ang']:.1e} rad")
for fila in ("distancias", "areas", "paralelismo", "rectas", "medio", "razon_doble"):
    d = disc[fila]
    LOCAL[fila] = d[0] > 1e-3 and d[1] < d[0] and d[2] < d[1] and d[2] / d[0] < 0.05

# ---------------------------------------------------------------- T1
TEXTO = {"si": "sí", "no": "no", "xk": r"\(\times k\)", "xk2": r"\(\times k^2\)",
         "xdet": r"\(\times\lvert\det A\rvert\)", "sgn": r"si \(\det>0\)\(^{a}\)",
         "lock": r"local\(^{b}\) \(\times k(p)\)", "lock2": r"local\(^{b}\) \(\times k(p)^2\)",
         "loc": r"local\(^{b}\)"}
# La tabla 1 tal como está escrita en el .tex (sección «Mapa de las transformaciones»)
TABLA1 = {
    "distancias":  dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="xk", afin="no", proyectiva="no", conforme="lock"),
    "angulos":     dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="si", afin="no", proyectiva="no", conforme="si"),
    "sentido":     dict(traslacion="si", rotacion="si", reflexion="no", rigido="si",
                        similaridad="sgn", afin="sgn", proyectiva="sgn", conforme="si"),
    "areas":       dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="xk2", afin="xdet", proyectiva="no", conforme="lock2"),
    "paralelismo": dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="si", afin="si", proyectiva="no", conforme="loc"),
    "rectas":      dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="si", afin="si", proyectiva="si", conforme="loc"),
    "medio":       dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="si", afin="si", proyectiva="no", conforme="loc"),
    "razon_doble": dict(traslacion="si", rotacion="si", reflexion="si", rigido="si",
                        similaridad="si", afin="si", proyectiva="si", conforme="loc"),
}

print("\n=== T1  tabla «Qué se conserva» medida ===")
errores = []
ancho = 13
print(" " * 28 + "".join(f"{ROTULO[f][:ancho - 1]:<{ancho}}" for f in FAMILIAS))
for fila in FILAS:
    linea = f"{ROT_FILA[fila]:<28}"
    for fam in FAMILIAS:
        med = MEDIDO[fam][fila]
        esc = TABLA1[fila][fam]
        if fam == "conforme" and esc in ("lock", "lock2", "loc"):
            ok = med == "no" and LOCAL[fila]
            med = esc if ok else med + "(no local)"
        else:
            ok = med == esc
        linea += f"{med:<{ancho}}"
        if not ok:
            errores.append(f"{ROT_FILA[fila]} / {ROTULO[fam]}: medido {med}, escrito {esc}")
    print(linea)

# El texto del .tex entre los marcadores tiene que ser el de TABLA1
tex = TEX.read_text(encoding="utf-8")
mt = re.search(r"% tabla-conserva:inicio\n(.*?)% tabla-conserva:fin", tex, re.S)
if not mt:
    errores.append("no se encontraron los marcadores de la tabla en el .tex")
else:
    filas_tex = [l.strip() for l in mt.group(1).strip().split("\n") if l.strip()]
    for fila, ltex in zip(FILAS, filas_tex):
        esperado = ROT_FILA[fila] + " & " + " & ".join(TEXTO[TABLA1[fila][f]] for f in FAMILIAS) \
            + r"\\"
        if ltex != esperado:
            errores.append(f"fila «{ROT_FILA[fila]}» del .tex:\n  {ltex}\n  esperado:\n  {esperado}")
    if len(filas_tex) != len(FILAS):
        errores.append(f"el .tex tiene {len(filas_tex)} filas entre los marcadores, no {len(FILAS)}")
if errores:
    print("\nERROR: la tabla escrita no coincide con lo medido:")
    for e in errores:
        print("  -", e)
    sys.exit(1)
print("La tabla escrita en el .tex coincide con lo medido en todas las celdas.")


# ---------------------------------------------------------------- ajustes
def ajuste_rigido(p, q):
    pc, qc = p - p.mean(0), q - q.mean(0)
    U, _, Vt = np.linalg.svd(qc.T @ pc)
    Rm = U @ np.diag([1, np.sign(np.linalg.det(U @ Vt))]) @ Vt
    t = q.mean(0) - Rm @ p.mean(0)
    return lambda X: X @ Rm.T + t, (Rm, t)


def ajuste_similaridad(p, q):
    n = len(p)
    M = np.zeros((2 * n, 4))
    M[0::2] = np.c_[p[:, 0], -p[:, 1], np.ones(n), np.zeros(n)]
    M[1::2] = np.c_[p[:, 1], p[:, 0], np.zeros(n), np.ones(n)]
    a, b, tx, ty = np.linalg.lstsq(M, q.reshape(-1), rcond=None)[0]
    A = np.array([[a, -b], [b, a]])
    return lambda X: X @ A.T + np.array([tx, ty]), (A, np.array([tx, ty]))


def ajuste_afin(p, q):
    U = np.c_[p, np.ones(len(p))]
    X = np.linalg.lstsq(U, q, rcond=None)[0]
    A, b = X[:2].T, X[2]
    return lambda Y: Y @ A.T + b, (A, b)


def ajuste_proyectivo(p, q):
    # arranque: DLT con h33 = 1 (lineal); después Gauss-Newton sobre los residuos geométricos
    n = len(p)
    M, y = [], []
    for (x, yy), (u, v) in zip(p, q):
        M.append([x, yy, 1, 0, 0, 0, -u * x, -u * yy]); y.append(u)
        M.append([0, 0, 0, x, yy, 1, -v * x, -v * yy]); y.append(v)
    h = np.linalg.lstsq(np.array(M), np.array(y), rcond=None)[0]

    def res(h):
        return (proyectiva(np.r_[h, 1.0].reshape(3, 3))(p) - q).reshape(-1)
    for _ in range(50):
        r0 = res(h)
        J = np.zeros((2 * n, 8))
        for j in range(8):
            dh = np.zeros(8)
            dh[j] = 1e-7 * max(1.0, abs(h[j]))
            J[:, j] = (res(h + dh) - r0) / dh[j]
        paso = np.linalg.lstsq(J, -r0, rcond=None)[0]
        h = h + paso
        if np.linalg.norm(paso) < 1e-12:
            break
    H = np.r_[h, 1.0].reshape(3, 3)
    return proyectiva(H), H


def rms(f, p, q):
    r = q - f(p)
    return np.sqrt(np.mean(np.sum(r ** 2, axis=1))), r


# ---------------------------------------------------------------- E1
print("\n=== E1  ejercicio: tres pares de puntos homólogos ===")
p1 = np.array([[0.0, 0.0], [40.0, 0.0], [0.0, 30.0]])
A1, t1 = np.array([[1.0, -0.75], [0.75, 1.0]]), np.array([100.0, 200.0])
q1 = p1 @ A1.T + t1
for i, (a, b) in enumerate(zip(p1, q1), 1):
    print(f"p{i} = ({a[0]:g}, {a[1]:g})  ->  q{i} = ({b[0]:g}, {b[1]:g})")
for i, j in [(0, 1), (0, 2), (1, 2)]:
    print(f"|p{i + 1}p{j + 1}| = {np.linalg.norm(p1[i] - p1[j]):g}   "
          f"|q{i + 1}q{j + 1}| = {np.linalg.norm(q1[i] - q1[j]):g}   cociente = "
          f"{np.linalg.norm(q1[i] - q1[j]) / np.linalg.norm(p1[i] - p1[j]):g}")
for nombre, ajuste, npar in (("rígido", ajuste_rigido, 3), ("similaridad", ajuste_similaridad, 4),
                             ("afín", ajuste_afin, 6)):
    f, par = ajuste(p1, q1)
    e, r = rms(f, p1, q1)
    print(f"{nombre:12s} ({npar} parámetros, redundancia {6 - npar}): RMS = {e:.3f}  "
          f"|residuos| = {np.round(np.linalg.norm(r, axis=1), 3)}")
    if nombre == "rígido":
        print(f"    giro = {np.arctan2(par[0][1, 0], par[0][0, 0]) / deg:.3f}°, t = {np.round(par[1], 3)}")
    if nombre == "similaridad":
        A = par[0]
        print(f"    lambda = {np.hypot(A[0, 0], A[1, 0]):.4f}, theta = "
              f"{np.arctan2(A[1, 0], A[0, 0]) / deg:.4f}°, t = {np.round(par[1], 3)}")

# ---------------------------------------------------------------- E2
print("\n=== E2  ejercicio: plano escaneado, cinco puntos de apoyo ===")
uv = np.array([[20.0, 30.0], [280.0, 25.0], [290.0, 190.0], [30.0, 200.0], [150.0, 110.0]])
A2 = R(2.0 * deg) @ np.diag([1.000, 0.996])          # m por mm: escala 1:1000, papel encogido
t2 = np.array([1000.0, 5000.0])
ruido2 = np.array([[0.02, -0.03], [-0.03, 0.01], [0.01, 0.03], [0.02, -0.01], [-0.02, 0.0]])
en2 = np.round(uv @ A2.T + t2 + ruido2, 2)
for i, (a, b) in enumerate(zip(uv, en2), 1):
    print(f"P{i}: (u; v) = ({a[0]:g}; {a[1]:g}) mm   (E; N) = ({b[0]:.2f}; {b[1]:.2f}) m")
for nombre, ajuste, npar in (("rígido", ajuste_rigido, 3), ("similaridad", ajuste_similaridad, 4),
                             ("afín", ajuste_afin, 6), ("proyectiva", ajuste_proyectivo, 8)):
    f, par = ajuste(uv, en2)
    e, r = rms(f, uv, en2)
    print(f"{nombre:12s} ({npar} parámetros, redundancia {10 - npar}): RMS = {100 * e:.1f} cm  "
          f"|residuos| (cm) = {np.round(100 * np.linalg.norm(r, axis=1), 1)}")
    if nombre == "afín":
        A, b = par
        print(f"    A = {np.round(A, 5).tolist()}, b = {np.round(b, 3)}; escalas de columna "
              f"{np.linalg.norm(A[:, 0]):.4f} y {np.linalg.norm(A[:, 1]):.4f} m/mm, ángulo entre "
              f"columnas {np.degrees(angulo(A[:, 0], A[:, 1])):.3f}°")
    if nombre == "similaridad":
        A = par[0]
        print(f"    lambda = {np.hypot(A[0, 0], A[1, 0]):.4f} m/mm")
    if nombre == "proyectiva":
        print(f"    h31 = {par[2, 0]:.2e}, h32 = {par[2, 1]:.2e} (por mm)")

# ---------------------------------------------------------------- figura
CORTO = {"traslacion": r"$x+v$", "rotacion": r"$\rho_{c,\,50^\circ}$",
         "reflexion": r"$\sigma_L$", "rigido": r"$R(-30^\circ)\,x+v$",
         "similaridad": r"$0{,}6\,R(110^\circ)\,x+t$", "afin": r"$Ax+b$",
         "proyectiva": r"$p\mapsto Hp$", "conforme": r"$z_0+(e^{\varepsilon z}-1)/\varepsilon$"}
plt.rcParams["axes.formatter.use_locale"] = False
fig, ejes = plt.subplots(2, 4, figsize=(6.9, 2.8))
cont0 = contorno(PREDIO, 200)
todos = [cont0] + [VARIANTES[f][0][0](cont0) for f in FAMILIAS]
xy = np.vstack(todos)
lo, hi = xy.min(0) - 0.6, xy.max(0) + 0.6
pn = puntos_notables(PREDIO)


def dibujar(ax, X, Xd, Mm, Ab, color, estilo, ancho, z, relleno):
    ax.fill(X[:, 0], X[:, 1], color=color, alpha=relleno, lw=0, zorder=z)
    Xc = np.vstack([X, X[:1]])
    ax.plot(Xc[:, 0], Xc[:, 1], color=color, ls=estilo, lw=ancho, zorder=z + 1)
    ax.plot(Xd[:, 0], Xd[:, 1], color=color, ls=estilo, lw=0.7 * ancho, zorder=z + 1)
    cara = "white" if estilo != "-" else color
    ax.plot(*Mm, "o", ms=3.2, mfc=cara, mec=color, mew=0.9, zorder=z + 2)
    ax.plot(*Ab[0], "s", ms=3.0, mfc=cara, mec=color, mew=0.9, zorder=z + 2)
    # flecha a mitad del lado AB: sentido del recorrido A -> B
    a, b = Ab[1], Ab[2]
    ax.annotate("", xy=b, xytext=a, zorder=z + 2,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=0.9, ls="-",
                                mutation_scale=7, shrinkA=0, shrinkB=0))


t = np.linspace(0, 1, 60)[:, None]
diag0 = PREDIO[0] + t * (PREDIO[2] - PREDIO[0])
AB0 = PREDIO[0] + np.array([[0.0], [0.42], [0.62]]) * (PREDIO[1] - PREDIO[0])
for ax, fam in zip(ejes.ravel(), FAMILIAS):
    f = VARIANTES[fam][0][0]
    dibujar(ax, cont0, diag0, pn["M"], AB0, GRIS, (0, (2.2, 1.6)), 0.9, 1, 0.10)
    dibujar(ax, f(cont0), f(diag0), f(pn["M"])[0], f(AB0), TEAL, "-", 1.2, 4, 0.16)
    if fam == "reflexion":
        xs = np.array([lo[0], hi[0]])
        ax.plot(xs, H_REF - xs, color=TINTA, lw=0.6, ls=(0, (6, 2, 1, 2)), zorder=0)
        ax.text(1.4, H_REF - 1.4 + 0.25, "$L$", color=TINTA, fontsize=7)
    if fam == "rotacion":
        ax.plot(*C_ROT, "+", color=TINTA, ms=6, mew=0.9, zorder=8)
        ax.text(C_ROT[0] + 0.25, C_ROT[1] - 0.75, "$c$", color=TINTA, fontsize=7)
    ax.set_xlim(lo[0], hi[0])
    ax.set_ylim(lo[1], hi[1])
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_linewidth(0.5)
    ax.set_title(ROTULO[fam], fontsize=8, color=TINTA, pad=2, fontweight="bold")
    ax.set_xlabel(CORTO[fam], fontsize=7, color=TINTA, labelpad=1.5)
fig.subplots_adjust(left=0.01, right=0.99, bottom=0.065, top=0.93, wspace=0.04, hspace=0.36)
destino = SALIDA / "cap04_mapa_transformaciones.pdf"
plt.savefig(destino, metadata={"CreationDate": None, "Producer": None, "Creator": None})
print(f"\nFigura: {destino.relative_to(RAIZ)}")
print(f"encuadre común: x en [{lo[0]:.2f}, {hi[0]:.2f}], y en [{lo[1]:.2f}, {hi[1]:.2f}]")
