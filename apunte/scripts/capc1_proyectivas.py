"""Números del complemento C1 (Transformaciones proyectivas).

Cubre, en este orden:
  R1  Conteo de correspondencias de cuatro vértices del pentágono: 5*4*3*2 = 120,
      y familias a menos de las 10 simetrías del pentágono.
  R2  Ejemplo «Razón doble de cuatro puntos»: (0,1;3,7) y su imagen por
      x -> (2x+1)/(x+3).
  R3  Figura de la proyección central: coordenadas de los puntos sobre las dos
      rectas, distancias y razón doble antes y después.
  R4  Pentágono, caso (c): H_c, autovalores, recta de puntos fijos (diagonal BD),
      centro O_c e imagen del quinto vértice.

Determinista, sin azar. Ejecutar:
  uv run --with numpy python apunte/scripts/capc1_proyectivas.py
"""
import math
from fractions import Fraction
from itertools import permutations

import numpy as np

np.set_printoptions(precision=4, suppress=True)


def razon_doble(a, b, c, d):
    return ((c - a) * (d - b)) / ((c - b) * (d - a))


# ---------------------------------------------------------------- R1
print("R1  correspondencias ordenadas de ABCD en cuatro vértices:", math.perm(5, 4))
# simetrías del pentágono como permutaciones de los índices 0..4 (A..E)
sim = [tuple((k + i) % 5 for i in range(5)) for k in range(5)]
sim += [tuple((k - i) % 5 for i in range(5)) for k in range(5)]
assert len(set(sim)) == 10
corr = list(permutations(range(5), 4))
familias = set()
for t in corr:
    orbita = frozenset(tuple(g[i] for i in t) for g in sim)
    familias.add(orbita)
print("R1  simetrías del pentágono:", len(sim), "| familias a menos de simetría:", len(familias))

# ---------------------------------------------------------------- R2
pts = [Fraction(0), Fraction(1), Fraction(3), Fraction(7)]
f = lambda x: (2 * x + 1) / (x + 3)
img = [f(x) for x in pts]
print("R2  puntos:", [str(x) for x in pts], "-> imágenes:", [str(x) for x in img])
print("R2  (c-a)(d-b) =", (pts[2] - pts[0]) * (pts[3] - pts[1]),
      " (c-b)(d-a) =", (pts[2] - pts[1]) * (pts[3] - pts[0]))
r0 = razon_doble(*pts)
r1 = razon_doble(*img)
print("R2  razón doble antes:", r0, "=", float(r0))
print("R2  imagen: (c'-a')(d'-b') =", (img[2] - img[0]) * (img[3] - img[1]),
      " (c'-b')(d'-a') =", (img[2] - img[1]) * (img[3] - img[0]))
print("R2  razón doble después:", r1, "=", float(r1))
print("R2  determinante alpha*delta - beta*gamma =", 2 * 3 - 1 * 1)
print("R2  razones simples (b-a)/(c-a): antes", (pts[1] - pts[0]) / (pts[2] - pts[0]),
      " después", (img[1] - img[0]) / (img[2] - img[0]))
assert r0 == r1

# ---------------------------------------------------------------- R3
# recta r: y = 0, puntos x = 0, 1, 3, 7 (escala 0.6 en la figura)
esc = 0.6
P = [np.array([x * esc, 0.0]) for x in (0, 1, 3, 7)]
O = np.array([-1.6, 3.4])            # centro de proyección
S0, S1 = np.array([-1.0, 1.9]), np.array([5.0, 0.4])   # recta s
u = (S1 - S0) / np.linalg.norm(S1 - S0)


def corte(p):
    # O + t (p - O) = S0 + s u
    M = np.column_stack([p - O, -u])
    t, s = np.linalg.solve(M, S0 - O)
    return O + t * (p - O), s


Q, s_par = zip(*[corte(p) for p in P])
print("R3  centro O =", O, " recta s por", S0, "y", S1)
for n, p, q in zip("abcd", P, Q):
    print(f"R3  {n} = ({p[0]:.3f}, {p[1]:.3f})  ->  {n}' = ({q[0]:.3f}, {q[1]:.3f})")
xr = [p[0] for p in P]
print("R3  distancias en r  ab, bc, cd:", np.round(np.diff(xr), 3))
print("R3  distancias en s  a'b', b'c', c'd':", np.round(np.diff(s_par), 3))
print("R3  razón doble en r:", round(razon_doble(*xr), 4),
      " en s:", round(razon_doble(*s_par), 4))

# ---------------------------------------------------------------- R4
ang = np.deg2rad(90 + 72 * np.arange(5))
V = np.c_[np.cos(ang), np.sin(ang), np.ones(5)]
A, B, C, D, E = V


def patron(Pm):
    M = Pm[:, :3]
    lam = np.linalg.solve(M, Pm[:, 3])
    return M * lam


def homografia(src, dst):
    K1 = patron(np.column_stack(src))
    K2 = patron(np.column_stack(dst))
    H = K2 @ np.linalg.inv(K1)
    return H / H[2, 2]


Hc = homografia((A, B, C, D), (C, B, A, D))
print("R4  H_c =\n", Hc)
lams = np.linalg.eigvals(Hc)
print("R4  autovalores:", np.sort(lams.real))
# recta de puntos fijos: núcleo de H_c - 0.8541 I tiene dimensión 2
ld = max(lams.real)
N = Hc - ld * np.eye(3)
print("R4  rango de H_c - %.4f I:" % ld, np.linalg.matrix_rank(N, tol=1e-6))
for nombre, p in (("A", A), ("B", B), ("C", C), ("D", D), ("E", E)):
    w = Hc @ p
    fijo = np.allclose(w / w[2], p / p[2], atol=1e-9)
    print(f"R4  H_c {nombre} -> ({w[0]/w[2]:.4f}, {w[1]/w[2]:.4f})  fijo: {fijo}")
recta_BD = np.cross(B, D)
recta_BD = recta_BD / recta_BD[1]
print("R4  recta BD (a menos de escala):", recta_BD)
for t in (-0.5, 0.25, 0.5, 2.0):     # puntos de la recta BD
    p = (1 - t) * B + t * D
    w = Hc @ p
    print(f"R4  punto (1-t)B+tD con t={t}: fijo", np.allclose(w / w[2], p, atol=1e-9))
# los fijos son exactamente la recta BD: autoespacio de 0.8541 = span(B, D)
Rk = np.linalg.matrix_rank(np.column_stack([B, D, np.linalg.svd(N)[2][-1]]), tol=1e-6)
Rk2 = np.linalg.matrix_rank(np.column_stack([B, D, np.linalg.svd(N)[2][-2]]), tol=1e-6)
print("R4  autoespacio de", round(ld, 4), "contenido en span(B,D):", Rk == 2 and Rk2 == 2)
lc = min(lams.real)
M = Hc - lc * np.eye(3)
v = np.cross(M[0], M[1])
print("R4  centro O_c:", v / v[2])
print("R4  AC pasa por O_c:", abs(np.cross(A, C) @ v) < 1e-9,
      "| BD es diagonal (B y D no adyacentes)")
w = Hc @ E
print("R4  E'_c =", w[:2] / w[2])
print("R4  W en A..E:", (Hc @ V.T)[2])

# familias de los casos (a), (b), (c) en R1 (índices: A=0, ..., E=4)
def familia(t):
    return frozenset(tuple(g[i] for i in t) for g in sim)


ca, cb, cc = familia((1, 2, 3, 4)), familia((1, 0, 2, 3)), familia((2, 1, 0, 3))
print("R1  (a) en la familia de la identidad:", ca == familia((0, 1, 2, 3)),
      "| (a),(b),(c) pertenecen a tres familias distintas:", len({ca, cb, cc}) == 3)
print("R3  escala por tramo (s/r):", np.round(np.diff(s_par) / np.diff(xr), 2))
