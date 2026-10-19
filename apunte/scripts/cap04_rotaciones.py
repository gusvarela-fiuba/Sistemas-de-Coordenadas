"""Verificación numérica del capítulo «Rotaciones» (apunte/contenido/04-rotaciones.tex).

Cubre, en este orden:
  E1  punto vs. coordenadas: p=(3,1), giro activo R(90°)p y cambio pasivo de ejes R(-90°)p.
  E2  rotación de p=(3,1) en 30° alrededor de c=(1,1) (ejemplo resuelto con figura).
  E3  conversión acimut <-> theta y orientación de una estación total.
  E4  composición rho_{c2,90°} o rho_{c1,90°}, c1=(0,0), c2=(4,0): centro (2,-2), ángulo 180°,
      por cuentas matriciales y por la construcción con dos reflexiones; experimento con un triángulo.
  E5  números complejos: (3+i)·e^{i pi/2}.
  E6  orden de rotaciones 3D: R_y R_x e_z vs R_x R_y e_z.
  E7  experimento de 121 pasos con eps=0.01 alrededor de (1,1,1); eje y ángulo de P.
  E8  exponencial de tau·J y generador antisimétrico de P.
  Ejercicios 1-6 del final del capítulo.
Determinista: no usa azar.
"""
import numpy as np

np.set_printoptions(precision=6, suppress=True)
deg = np.pi / 180


def R(t):
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def rot_c(c, t, p):
    c, p = np.asarray(c, float), np.asarray(p, float)
    return c + R(t) @ (p - c)


def Rx(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])


def Ry(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])


def Rz(t):
    c, s = np.cos(t), np.sin(t)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def homog(A, t):
    H = np.eye(3)
    H[:2, :2] = A
    H[:2, 2] = t
    return H


def centro_y_angulo(H):
    A, t = H[:2, :2], H[:2, 2]
    ang = np.arctan2(A[1, 0], A[0, 0])
    c = np.linalg.solve(np.eye(2) - A, t)
    return c, ang


def S(delta):
    """Reflexión respecto de la recta por el origen con ángulo de dirección delta."""
    return np.array([[np.cos(2 * delta), np.sin(2 * delta)], [np.sin(2 * delta), -np.cos(2 * delta)]])


def eje_angulo(M):
    ang = np.arccos(np.clip((np.trace(M) - 1) / 2, -1, 1))
    w = np.array([M[2, 1] - M[1, 2], M[0, 2] - M[2, 0], M[1, 0] - M[0, 1]]) / (2 * np.sin(ang))
    return w / np.linalg.norm(w), ang


print("== E1 punto vs coordenadas ==")
p = np.array([3.0, 1.0])
print("activo R(90)p =", R(90 * deg) @ p)
print("pasivo R(-90)p =", R(-90 * deg) @ p)

print("== E2 rotar p=(3,1) 30° alrededor de c=(1,1) ==")
c = np.array([1.0, 1.0])
print("R(30) =", R(30 * deg))
print("p-c =", p - c)
v = R(30 * deg) @ (p - c)
print("R(30)(p-c) =", v, " sqrt3 =", np.sqrt(3))
pp = c + v
print("p' =", pp)
print("|p-c| =", np.linalg.norm(p - c), " |p'-c| =", np.linalg.norm(pp - c))
print("forma afín: R p + (I-R)c =", R(30 * deg) @ p + (np.eye(2) - R(30 * deg)) @ c)
print("(I-R(30))c =", (np.eye(2) - R(30 * deg)) @ c)

print("== E3 acimut ==")
lec_ref, az_ref = 352.5, 40.0
delta = (az_ref - lec_ref) % 360
print("corrección de orientación Delta =", delta)
lec_p = 100.0
az_p = (lec_p + delta) % 360
th_p = (90 - az_p) % 360
print("Az_P =", az_p, " theta_P =", th_p)
d = 50.0
print("dE,dN por acimut =", d * np.sin(az_p * deg), d * np.cos(az_p * deg))
print("dx,dy por theta  =", d * np.cos(th_p * deg), d * np.sin(th_p * deg))

print("== E4 composición de rotaciones c1=(0,0) a=90, c2=(4,0) b=90 ==")
c1, c2 = np.array([0.0, 0.0]), np.array([4.0, 0.0])
H1 = homog(R(90 * deg), (np.eye(2) - R(90 * deg)) @ c1)
H2 = homog(R(90 * deg), (np.eye(2) - R(90 * deg)) @ c2)
H = H2 @ H1
print("H1 =\n", H1)
print("H2 =\n", H2)
print("H = H2 H1 =\n", H)
cc, ang = centro_y_angulo(H)
print("centro =", cc, " angulo (deg) =", ang / deg)
# construcción: M1 por c1 con ángulo -a/2, M2 por c2 con ángulo +b/2; recta común L = eje x
d1, d2 = -45 * deg, 45 * deg
u1, u2 = np.array([np.cos(d1), np.sin(d1)]), np.array([np.cos(d2), np.sin(d2)])
st = np.linalg.solve(np.column_stack([u1, -u2]), c2 - c1)
print("intersección M1∩M2 =", c1 + st[0] * u1)
print("S(0)S(-45) = R(90)?", np.allclose(S(0) @ S(-45 * deg), R(90 * deg)))
print("S(45)S(0) = R(90)?", np.allclose(S(45 * deg) @ S(0), R(90 * deg)))
tri = np.array([[1.0, 1.0], [3.0, 1.0], [1.0, 2.0]])
for q in tri:
    q1 = rot_c(c1, 90 * deg, q)
    q2 = rot_c(c2, 90 * deg, q1)
    qd = rot_c(cc, 180 * deg, q)
    print("vértice", q, "-> tras rho1", q1, "-> tras rho2", q2, " directo rho_(2,-2),180:", qd)

print("== E5 complejos ==")
z = 3 + 1j
print("(3+i) e^{i pi/2} =", z * np.exp(1j * np.pi / 2))

print("== E6 orden 3D ==")
ez = np.array([0, 0, 1.0])
print("Rx(90) ez =", Rx(90 * deg) @ ez)
print("Ry(90) Rx(90) ez =", Ry(90 * deg) @ Rx(90 * deg) @ ez)
print("Ry(90) ez =", Ry(90 * deg) @ ez)
print("Rx(90) Ry(90) ez =", Rx(90 * deg) @ Ry(90 * deg) @ ez)

print("== E7 experimento 121 pasos ==")
eps = 0.01
Q = Rz(eps) @ Ry(eps) @ Rx(eps)
n_ideal = (2 * np.pi / 3) / (eps * np.sqrt(3))
print("n ideal = (2pi/3)/(eps sqrt3) =", n_ideal)
Theta = 121 * eps * np.sqrt(3)
print("Theta aprox =", Theta, "rad =", Theta / deg, "deg")
Qn = np.linalg.matrix_power(Q, 121)
u, a = eje_angulo(Qn)
print("Q^121 =\n", Qn)
print("eje de Q^121 =", u, " ángulo =", a / deg)
P = np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0.0]])
print("max |Q^121 - P| =", np.abs(Qn - P).max())
uP, aP = eje_angulo(P)
print("eje de P =", uP, " ángulo P =", aP / deg, " traza P =", np.trace(P))
print("(P-I)(1,1,1) =", (P - np.eye(3)) @ np.ones(3))

print("== E8 exponencial ==")
J = np.array([[0, -1], [1, 0.0]])
tau = np.pi / 6
E = np.eye(2)
term = np.eye(2)
for k in range(1, 30):
    term = term @ (tau * J) / k
    E = E + term
print("e^{tau J} (tau=pi/6) =", E, " R(pi/6) =", R(tau))
omega = aP * uP
print("omega de P =", omega, " |omega| =", np.linalg.norm(omega), " 2pi/(3 sqrt3) =", 2 * np.pi / (3 * np.sqrt(3)))

print("== Ejercicios ==")
p1 = rot_c([2, -1], 60 * deg, [5, 2])
print("Ej1 rotar (5,2) 60° alrededor de (2,-1):", p1, " R(60)(3,3) =", R(60 * deg) @ np.array([3.0, 3.0]))
print("Ej1 |p-c| =", np.hypot(3, 3), " |p1-c| =", np.linalg.norm(p1 - np.array([2.0, -1.0])))
Hej = np.array([[0, -1, 4], [1, 0, 2], [0, 0, 1.0]])
cj, aj = centro_y_angulo(Hej)
print("Ej2 centro =", cj, " ángulo deg =", aj / deg, " verif H c =", Hej @ np.array([*cj, 1]))
Ha = homog(R(90 * deg), np.zeros(2))
Hb = homog(R(-90 * deg), (np.eye(2) - R(-90 * deg)) @ np.array([2.0, 0]))
print("Ej3 rho_{(2,0),-90} o rho_{0,90} =\n", Hb @ Ha)
e3 = 0.02
q = np.array([100.0, 0])
exa, apx = R(e3) @ q, (np.eye(2) + e3 * J) @ q
print("Ej4 exacta =", exa, " aprox =", apx, " error =", np.linalg.norm(exa - apx), " |aprox| =", np.linalg.norm(apx))
ey = np.array([0, 1.0, 0])
print("Ej5 Rz(90)Rx(90) ey =", Rz(90 * deg) @ Rx(90 * deg) @ ey, " Rx(90)Rz(90) ey =", Rx(90 * deg) @ Rz(90 * deg) @ ey)
print("Ej6 Az=230 -> theta =", (90 - 230) % 360, "; theta=30 -> Az =", (90 - 30) % 360)

print("== Generadores: conmutador y orden a segundo orden ==")
Ax = np.array([[0, 0, 0], [0, 0, -1], [0, 1, 0.0]])
Ay = np.array([[0, 0, 1], [0, 0, 0], [-1, 0, 0.0]])
Az = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 0.0]])
print("AxAy - AyAx = Az?", np.allclose(Ax @ Ay - Ay @ Ax, Az))
e = 0.01
Dif = Rx(e) @ Ry(e) - Ry(e) @ Rx(e)
print("Rx(0.01)Ry(0.01) - Ry(0.01)Rx(0.01) =\n", Dif)
print("eps^2 Az =\n", e**2 * Az)
