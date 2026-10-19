"""Números del capítulo 6 (Afinidades y coordenadas homogéneas).

Cubre, en este orden:
  E1  Ejemplo «Escalado no uniforme y corte» (círculo -> elipse, factor de área).
  E2  Ejemplo «Georreferenciar una imagen de dron» (A, b, det, matriz 3x3, píxeles).
  E3  Ejemplo «Una afinidad axial» (eje y = 0, dirección (1,1), razón 2).
  E4  Ejemplo «Afinidad a partir de tres puntos de control» (sistema de 6 incógnitas,
      verificación con un cuarto punto y residuo).
  E5  Ejemplo «Rotación alrededor de un centro y escala alrededor de otro» (figura en T).
  E6  Ejemplo «Direcciones propias de la afinidad axial» (autovalores de E3).
  X1..X6  Soluciones de los ejercicios propuestos.

Determinista, sin azar. Ejecutar:
  uv run python apunte/scripts/cap06_afines.py
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True)


def hom(A, b):
    M = np.eye(3)
    M[:2, :2] = A
    M[:2, 2] = b
    return M


def aplicar(M, p):
    v = M @ np.array([p[0], p[1], 1.0])
    return v[:2] / v[2]


def punto_fijo(A, b):
    return np.linalg.solve(np.eye(2) - A, b)


print("=== E1 escalado no uniforme y corte ===")
S = np.diag([2.0, 1.0])
print("det S =", np.linalg.det(S), " área círculo unidad =", np.pi, " área elipse =", np.pi * abs(np.linalg.det(S)))
for p in [(1, 0), (0, 1), (np.sqrt(2) / 2, np.sqrt(2) / 2)]:
    print("S", p, "->", S @ np.array(p))
C = np.array([[1.0, 1.0], [0.0, 1.0]])
print("corte C, det =", np.linalg.det(C))
for p in [(0, 0), (1, 0), (1, 1), (0, 1)]:
    print("C", p, "->", C @ np.array(p))

print("\n=== E2 dron ===")
A = np.array([[0.5, 0.0], [0.0, -0.5]])
b = np.array([5000.0, 8000.0])
M = hom(A, b)
print("det A =", np.linalg.det(A))
print("M =\n", M)
for px in [(0, 0), (200, 100), (400, 0), (0, 300), (400, 300)]:
    print("pixel", px, "->", aplicar(M, px))
print("punto impropio (1,0,0) ->", M @ np.array([1.0, 0, 0]))
print("punto impropio (0,1,0) ->", M @ np.array([0.0, 1, 0]))

print("\n=== E3 afinidad axial ===")
Ax = np.array([[1.0, 1.0], [0.0, 2.0]])
for p in [(1, 2), (0, 0), (3, 0), (2, 1)]:
    print("axial", p, "->", Ax @ np.array(p))

print("\n=== E4 tres puntos de control ===")
uv = np.array([[10.0, 20.0], [110.0, 30.0], [40.0, 120.0]])
# Coordenadas de terreno de los puntos de control (al centímetro). Se generan con una
# afinidad de referencia para que el ejemplo sea reproducible; el texto las presenta como datos.
A_ref = np.array([[0.498, 0.042], [0.041, -0.497]])
b_ref = np.array([1000.0, 2000.0])
EN = np.round(uv @ A_ref.T + b_ref, 2)
print("puntos de control (u,v) -> (E,N):")
for a_, e_ in zip(uv, EN):
    print("  ", a_, "->", e_)
# sistema 6x6: incógnitas (a11, a12, b1, a21, a22, b2)
K = np.zeros((6, 6))
r = np.zeros(6)
for i, ((u, v), (E, N)) in enumerate(zip(uv, EN)):
    K[2 * i, 0:3] = [u, v, 1]
    r[2 * i] = E
    K[2 * i + 1, 3:6] = [u, v, 1]
    r[2 * i + 1] = N
U = np.column_stack([uv, np.ones(3)])
print("U =\n", U, " det U =", round(np.linalg.det(U), 6))
print("K =\n", K)
print("r =", r)
sol = np.linalg.solve(K, r)
print("solución (a11,a12,b1,a21,a22,b2) =", np.round(sol, 3))
print("K^-1 r sin redondear =", sol)
A4 = np.array([[sol[0], sol[1]], [sol[3], sol[4]]])
b4 = np.array([sol[2], sol[5]])
print("det A =", round(np.linalg.det(A4), 6))
# control vía A = P' P^{-1}
P = np.column_stack([uv[1] - uv[0], uv[2] - uv[0]])
Pp = np.column_stack([EN[1] - EN[0], EN[2] - EN[0]])
print("P =\n", P, "\nP' =\n", Pp, "\nP' P^-1 =\n", Pp @ np.linalg.inv(P))
q4 = np.array([80.0, 80.0])
medido = np.array([1043.23, 1963.49])  # medición del cuarto punto (dato)
pred = A4 @ q4 + b4
print("cuarto punto", q4, "predicho", np.round(pred, 3), "medido", medido)
res = medido - pred
print("residuo", np.round(res, 3), " norma", round(np.linalg.norm(res), 3))

print("\n=== E5 rotación 45 alrededor de c y homotecia 1/2 alrededor de o ===")
th = np.pi / 4
R = np.array([[np.cos(th), -np.sin(th)], [np.sin(th), np.cos(th)]])
c = np.array([3.0, 1.0])
o = np.array([-1.0, 2.0])
k = 0.5
M1 = hom(R, (np.eye(2) - R) @ c)
M2 = hom(k * np.eye(2), (1 - k) * o)
Mc = M2 @ M1
print("M1 =\n", np.round(M1, 3), "\nM2 =\n", np.round(M2, 3), "\nM = M2 M1 =\n", np.round(Mc, 3))
print("M1 M2 =\n", np.round(M1 @ M2, 3))
q = (2.0, 2.0)
q1 = aplicar(M1, q)
q2 = aplicar(M2, q1)
print("q", q, "q1", np.round(q1, 3), "q2", np.round(q2, 3), "M q", np.round(aplicar(Mc, q), 3))
ps = punto_fijo(Mc[:2, :2], Mc[:2, 2])
print("punto fijo p* =", np.round(ps, 4), " 1-sqrt2/2 =", 1 - np.sqrt(2) / 2)
print("M p* =", np.round(aplicar(Mc, ps), 4))
T = np.array([[-2, 2], [2, 2], [2, 1], [0.5, 1], [0.5, -2], [-0.5, -2], [-0.5, 1], [-2, 1]])
print("T rotada:", [tuple(np.round(aplicar(M1, p), 3)) for p in T])
print("T final:", [tuple(np.round(aplicar(Mc, p), 3)) for p in T])
w, V = np.linalg.eig(Mc)
print("autovalores de M:", np.round(w, 4))
i1 = np.argmin(abs(w - 1))
v1 = np.real(V[:, i1])
print("autovector de 1 normalizado:", np.round(v1 / v1[2], 4))

print("\n=== E6 direcciones propias de la axial ===")
w, V = np.linalg.eig(Ax)
print("autovalores", w)
print("autovectores (columnas)\n", V / np.abs(V).max(axis=0))

print("\n=== Ejercicios ===")
R90 = np.array([[0.0, -1.0], [1.0, 0.0]])
c1 = np.array([1.0, 2.0])
Mr = hom(R90, (np.eye(2) - R90) @ c1)
Mt = hom(np.eye(2), [3.0, 0.0])
X1 = Mt @ Mr
print("X1 M_rot =\n", Mr, "\nX1 T M_rot =\n", X1)
print("X1 imagen de (0,0):", aplicar(X1, (0, 0)), " de c:", aplicar(X1, c1))
print("X1 punto fijo:", punto_fijo(X1[:2, :2], X1[:2, 2]))

src = np.array([[0.0, 0], [1, 0], [0, 1]])
dst = np.array([[1.0, 1], [3, 2], [0, 3]])
P = np.column_stack([src[1] - src[0], src[2] - src[0]])
Pp = np.column_stack([dst[1] - dst[0], dst[2] - dst[0]])
A2 = Pp @ np.linalg.inv(P)
print("X2 A =", A2, " b =", dst[0] - A2 @ src[0])

A3 = np.array([[2.0, 1.0], [0.0, 3.0]])
b3 = np.array([1.0, -4.0])
p3 = punto_fijo(A3, b3)
print("X3 punto fijo", p3, " verif", A3 @ p3 + b3)

A4x = np.array([[1.0, 2.0], [3.0, 4.0]])
tri = np.array([[0.0, 0], [1, 0], [0, 1]])
img = (A4x @ tri.T).T
area = lambda t: 0.5 * np.linalg.det(np.column_stack([t[1] - t[0], t[2] - t[0]]))
print("X4 det", np.linalg.det(A4x), " imagen triángulo", img.tolist(), " área orientada", area(tri), "->", area(img))

A5 = np.array([[2.0, 0.0], [1.0, 1.0]])
b5 = np.array([4.0, -1.0])
A5i = np.linalg.inv(A5)
print("X5 A^-1 =", A5i, " -A^-1 b =", -A5i @ b5)
print("X5 M^-1 =\n", np.linalg.inv(hom(A5, b5)))
print("X5 control f^-1(f(1,1)):", aplicar(np.linalg.inv(hom(A5, b5)), aplicar(hom(A5, b5), (1, 1))))

src = np.array([[0.0, 0], [2, 0], [0, 1]])
dst = np.array([[1.0, 1], [5, 2], [2, 4]])
P = np.column_stack([src[1] - src[0], src[2] - src[0]])
Pp = np.column_stack([dst[1] - dst[0], dst[2] - dst[0]])
A6 = Pp @ np.linalg.inv(P)
b6 = dst[0] - A6 @ src[0]
print("X6 P =", P.tolist(), " P' =", Pp.tolist(), " A =", A6.tolist(), " b =", b6, " det A =", np.linalg.det(A6))
