"""Verificación numérica del capítulo «Traslaciones y movimientos rígidos»
(apunte/contenido/02-traslaciones-movimientos-rigidos.tex).

Ejecutar:  uv run python apunte/scripts/cap02_traslaciones.py   (requiere numpy)

Cubre: E1 círculo descentrado; E2 fórmula del punto fijo; E3 composición de rotaciones de
centros distintos; E4 T3 (traslación = dos reflexiones); E5 T4 (rotación = dos reflexiones);
E6 aplicación topográfica (poligonal local -> obra); E7 grupo homogéneo; ejercicios 2.1-2.4.
Determinista: no usa azar.
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True)
deg = np.pi / 180


def R(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def S(d):
    return np.array([[np.cos(2 * d), np.sin(2 * d)], [np.sin(2 * d), -np.cos(2 * d)]])


def refl(q, d, p):
    q, p = np.asarray(q, float), np.asarray(p, float)
    return q + S(d) @ (p - q)


def rot_c(c, t, p):
    c, p = np.asarray(c, float), np.asarray(p, float)
    return c + R(t) @ (p - c)


def fijo(t, v):
    return np.linalg.solve(np.eye(2) - R(t), np.asarray(v, float))


def hom(M, v):
    H = np.eye(3)
    H[:2, :2], H[:2, 2] = M, v
    return H


def gauss(P):
    x, y = P[:, 0], P[:, 1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))


print("== E1 círculo descentrado: F(x)=R(90°)x+(2,0)")
v = np.array([2.0, 0.0])
c = fijo(90 * deg, v)
print("punto fijo:", c, " det(I-R)=2-2cos(90°)=", np.linalg.det(np.eye(2) - R(90 * deg)))
F = lambda x: R(90 * deg) @ x + v
for p in [(0, 0), (1, 0), (0, 1), (-1, 0)]:
    p = np.array(p, float)
    print("F", p, "->", F(p), "  rot_c((1,1),90°):", rot_c(c, 90 * deg, p))
print("F(0)=", F(np.zeros(2)))

print("== E2 punto fijo de una composición: det(I-R)=2-2cos(theta)")
for th in (30, 60, 90, 180):
    print(th, "det:", round(np.linalg.det(np.eye(2) - R(th * deg)), 6), 2 - 2 * np.cos(th * deg))
th, v = 90 * deg, np.array([1.0, 2.0])
cp = fijo(th, R(th) @ v)
print("rho(0,90)∘tau_(1,2): v'=R v =", R(th) @ v, " centro:", cp)
print("tau∘rho: centro c'=(I-R)^-1 v =", fijo(th, v))

print("== E3 composición de rotaciones (cap. conservado)")
c1, c2 = np.array([0.0, 0]), np.array([4.0, 0])
H1, H2 = hom(R(90 * deg), (np.eye(2) - R(90 * deg)) @ c1), hom(R(90 * deg), (np.eye(2) - R(90 * deg)) @ c2)
print("H2 H1 =\n", H2 @ H1)
print("centro:", fijo(180 * deg, (H2 @ H1)[:2, 2]))
T = np.array([[1, 1], [3, 1], [1, 2]], float)
print("tras rho_c1:", [rot_c(c1, 90 * deg, p) for p in T])
print("tras rho_c2:", [rot_c(c2, 90 * deg, rot_c(c1, 90 * deg, p)) for p in T])
print("rotación única (2,-2),180°:", [rot_c([2, -2], np.pi, p) for p in T])
print("orden inverso (rho_c1 tras rho_c2) de (1,1):", rot_c(c1, 90 * deg, rot_c(c2, 90 * deg, np.array([1.0, 1])))),
print("centro orden inverso:", fijo(180 * deg, (hom(R(90 * deg), (np.eye(2) - R(90 * deg)) @ c1) @ H2)[:2, 2]))

print("== E4 T3: tau_(4,0) = sigma_{x=2} ∘ sigma_{x=0}")
p = np.array([1.0, 3.0])
a = refl([0, 0], 90 * deg, p)
b = refl([2, 0], 90 * deg, a)
print("p=", p, " tras x=0:", a, " tras x=2:", b, " p+v:", p + np.array([4.0, 0]))

print("== E5 T4: rho_{0,90°} = sigma_{y=x} ∘ sigma_{y=0}")
p = np.array([2.0, 1.0])
a = refl([0, 0], 0.0, p)
b = refl([0, 0], 45 * deg, a)
print("p=", p, " tras y=0:", a, " tras y=x:", b, " R(90°)p:", R(90 * deg) @ p)

print("== E6 aplicación topográfica")
L = np.array([[0, 0], [48.215, 12.630], [71.480, 60.905], [23.117, 84.992]])
E = np.array([1000.0, 2000.0])
Az0 = 37.25
kappa = (90 - Az0) * deg
print("kappa (grados):", 90 - Az0)
print("R(kappa)=\n", R(kappa))
Hm = hom(R(kappa), E)
print("H (homogénea 3x3)=\n", Hm)
O = (Hm @ np.c_[L, np.ones(len(L))].T).T[:, :2]
print("vértices obra:\n", np.round(O, 3))
dl = [np.linalg.norm(L[i] - L[(i + 1) % 4]) for i in range(4)]
do = [np.linalg.norm(O[i] - O[(i + 1) % 4]) for i in range(4)]
print("lados local:", np.round(dl, 3), " lados obra:", np.round(do, 3))
print("diagonales local:", round(np.linalg.norm(L[0] - L[2]), 3), round(np.linalg.norm(L[1] - L[3]), 3),
      " obra:", round(np.linalg.norm(O[0] - O[2]), 3), round(np.linalg.norm(O[1] - O[3]), 3))
print("área Gauss local:", round(gauss(L), 3), " obra:", round(gauss(O), 3))
print("relativo a E (ΔE,ΔN):\n", np.round(O - E, 3))
mal = R(kappa) @ (L + E).T
print("orden equivocado (trasladar y luego rotar):\n", np.round(mal.T, 3))
print("vértice 2 correcto:", np.round(O[1], 3), " equivocado:", np.round(mal.T[1], 3),
      " distancia entre ambos:", round(np.linalg.norm(O[1] - mal.T[1]), 3))
print("vértice 1 (origen local) equivocado:", np.round(mal.T[0], 3))
print("(R-I)E =", np.round((R(kappa) - np.eye(2)) @ E, 3))

print("== E7 grupo de movimientos rígidos")
th, v = 30 * deg, np.array([2.0, 1.0])
H = hom(R(th), v)
Hinv = hom(R(th).T, -R(th).T @ v)
print("H @ Hinv =\n", H @ Hinv)

print("== Ejercicios")
print("2.1 punto fijo de x->R(60°)x+(3,0):", fijo(60 * deg, [3, 0]), " (3/2, 3√3/2)=", (1.5, 1.5 * 3 ** .5))
print("2.2a tau(3,-1)∘tau(1,2) =", np.array([3, -1]) + np.array([1, 2]))
p = np.array([3.0, 1.0]); v = np.array([1.0, 2.0])
print("2.2b rho_{0,90}∘tau_v (3,1):", R(90 * deg) @ (p + v), "  tau_v∘rho_{0,90}:", R(90 * deg) @ p + v)
print("2.2b centro de rho∘tau:", fijo(90 * deg, R(90 * deg) @ v), " de tau∘rho:", fijo(90 * deg, v))
p = np.array([2.0, 1.0])
a = refl([0, 0], 0.0, p); b = refl([0, 3], 0.0, a)
print("2.3 v=(0,6): y=0 y y=3; p=(2,1):", a, b, p + np.array([0, 6.0]))
kap = (90 - 120) * deg
x = np.array([50.0, 20.0])
print("2.4 Az0=120°, kappa=", 90 - 120, " E+R(kappa)(50,20)=", E + R(kap) @ x, " R(kappa)x=", R(kap) @ x)

print("== Complementos")
print("orden inverso, triángulo T:", [rot_c([2, 2], np.pi, p) for p in T], " (1,1)->", rot_c(c1, 90 * deg, rot_c(c2, 90 * deg, np.array([1.0, 1]))))
print("ej 2.1 rho_{(2,0),-90}∘rho_{0,90} en (1,1): desplazamiento", rot_c([2, 0], -90 * deg, R(90 * deg) @ np.array([1.0, 1])) - np.array([1.0, 1]))
