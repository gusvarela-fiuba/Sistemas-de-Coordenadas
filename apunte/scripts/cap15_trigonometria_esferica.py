"""Números y figuras del capítulo «Coordenadas sobre la esfera y trigonometría esférica».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «El octante»: A = (0,0,1), B = (1,0,0), C = (0,1,0); lados, ángulos, exceso,
      fracción de la esfera.
  E2  Ejemplo «Tres ciudades»: Buenos Aires (-34,6; -58,4), Córdoba (-31,4; -64,2),
      Mendoza (-32,9; -68,8) sobre la esfera de 6371 km: lados por producto interno, ángulos
      por normales, teoremas del coseno (lados y ángulos) y del seno, exceso por la suma de
      ángulos, por L'Huilier y por la fórmula del determinante; área; Legendre en Buenos Aires.
  E3  Ejemplo «Recorrer el triángulo con rotaciones»: composición de las rotaciones a lo largo
      de los tres lados del triángulo de E2; eje y ángulo de la composición contra el exceso.
  A1  Aplicación topográfica: Buenos Aires -> Mendoza. Problema inverso sobre la esfera de
      radio sqrt(MN) en la latitud media y sobre la de radio medio R1 = (2a+b)/3 (GRS80);
      control con pyproj.Geod(ellps='GRS80').inv; diferencias en m y ppm. Problema directo
      aplicado al resultado del inverso. Constante de Clairaut. Loxodromia Buenos Aires ->
      Mendoza (rumbo y largo) contra el círculo máximo.
  A2  Red de control: triángulo de lados de 46 a 55 km (vértices aproximados, declarados);
      radio sqrt(MN), ángulos esféricos, exceso en segundos, S/R^2 con S de Herón, corrección
      de Legendre por ángulo y su residuo contra el triángulo plano de los mismos lados.
  L   Loxodromia y círculo máximo Buenos Aires -> Ciudad del Cabo (figura): largos, rumbo,
      latitud extrema del círculo máximo por Clairaut.
  X1  Ejercicio 1: b = 50°, c = 70°, A = 80°: a, B, C, exceso.
  X2  Ejercicio 2: triángulo equilátero de ángulos 100°: lado por la fórmula polar, exceso, área.
  X3  Ejercicio 3: directo desde (0°, 0°) con acimut 45° y sigma = 90°; luego el inverso.
  X4  Ejercicio 4: triángulo equilátero de 40 km sobre R = 6371 km: S, exceso, Legendre.
  X5  Ejercicio 5: dos puntos sobre el paralelo -34,6° separados 10° de longitud: arco de
      paralelo contra arco de círculo máximo; acimut de partida.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/esfera/:
  esfera_triangulo.png    triángulo esférico: vectores A, B, C, lados a, b, c como ángulos al
                          centro, ángulos A, B, C entre tangentes.
  esfera_lunulas.png      los tres husos (lúnulas) de Girard y el triángulo común a los tres.
  esfera_loxodromia.png   círculo máximo y loxodromia Buenos Aires -> Ciudad del Cabo, en
                          Mercator y sobre la esfera.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap15_trigonometria_esferica.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pyproj import Geod

np.set_printoptions(precision=6, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "esfera"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, TINTA = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#2b2b2b"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
META = {"Software": None}

D = np.pi / 180
SEG = 3600 / D  # radianes -> segundos de arco

# GRS80
A_GRS = 6378137.0
F_GRS = 1 / 298.257222101
B_GRS = A_GRS * (1 - F_GRS)
E2_GRS = F_GRS * (2 - F_GRS)


def unit(phi, lam):
    """Vector unitario r(phi, lam) en grados."""
    p, l = phi * D, lam * D
    return np.array([np.cos(p) * np.cos(l), np.cos(p) * np.sin(l), np.sin(p)])


def ang(u, v):
    """Ángulo entre vectores por atan2(|u x v|, u.v) (estable para ángulos chicos)."""
    return np.arctan2(np.linalg.norm(np.cross(u, v)), np.dot(u, v))


def triangulo(A, B, C):
    """Lados (a, b, c) y ángulos (A, B, C) en radianes."""
    a, b, c = ang(B, C), ang(A, C), ang(A, B)
    An = ang(np.cross(A, B), np.cross(A, C))
    Bn = ang(np.cross(B, C), np.cross(B, A))
    Cn = ang(np.cross(C, A), np.cross(C, B))
    return np.array([a, b, c]), np.array([An, Bn, Cn])


def lhuilier(a, b, c):
    s = (a + b + c) / 2
    t = np.tan(s / 2) * np.tan((s - a) / 2) * np.tan((s - b) / 2) * np.tan((s - c) / 2)
    return 4 * np.arctan(np.sqrt(t))


def exceso_det(A, B, C):
    """tan(eps/2) = |det[A B C]| / (1 + A.B + B.C + C.A)."""
    num = abs(np.linalg.det(np.column_stack([A, B, C])))
    den = 1 + A @ B + B @ C + C @ A
    return 2 * np.arctan2(num, den)


def rot(k, t):
    """Rotación de ángulo t alrededor del eje unitario k (Rodrigues)."""
    k = k / np.linalg.norm(k)
    K = np.array([[0, -k[2], k[1]], [k[2], 0, -k[0]], [-k[1], k[0], 0]])
    return np.eye(3) + np.sin(t) * K + (1 - np.cos(t)) * K @ K


def este_norte(phi, lam):
    p, l = phi * D, lam * D
    e = np.array([-np.sin(l), np.cos(l), 0.0])
    n = np.array([-np.sin(p) * np.cos(l), -np.sin(p) * np.sin(l), np.cos(p)])
    return e, n


def inverso(phi1, lam1, phi2, lam2):
    """Distancia angular y acimutes (partida y llegada, hacia adelante), en grados."""
    p1, p2, dl = phi1 * D, phi2 * D, (lam2 - lam1) * D
    s = np.arccos(np.sin(p1) * np.sin(p2) + np.cos(p1) * np.cos(p2) * np.cos(dl))
    a1 = np.arctan2(np.cos(p2) * np.sin(dl), np.cos(p1) * np.sin(p2) - np.sin(p1) * np.cos(p2) * np.cos(dl))
    a2 = np.arctan2(np.cos(p1) * np.sin(dl), -np.sin(p1) * np.cos(p2) + np.cos(p1) * np.sin(p2) * np.cos(dl))
    return s / D, (a1 / D) % 360, (a2 / D) % 360


def directo(phi1, lam1, a1, s):
    """Punto de llegada y acimut de llegada (hacia adelante), en grados."""
    p1, al, sg = phi1 * D, a1 * D, s * D
    p2 = np.arcsin(np.sin(p1) * np.cos(sg) + np.cos(p1) * np.sin(sg) * np.cos(al))
    dl = np.arctan2(np.sin(al) * np.sin(sg), np.cos(sg) * np.cos(p1) - np.sin(sg) * np.cos(al) * np.sin(p1))
    a2 = np.arctan2(np.sin(al) * np.cos(p1), np.cos(sg) * np.cos(p1) * np.cos(al) - np.sin(p1) * np.sin(sg))
    return p2 / D, lam1 + dl / D, (a2 / D) % 360


def directo_vectorial(phi1, lam1, a1, s):
    P = unit(phi1, lam1)
    e, n = este_norte(phi1, lam1)
    t = np.sin(a1 * D) * e + np.cos(a1 * D) * n
    return np.cos(s * D) * P + np.sin(s * D) * t


def MN(phi):
    s2 = np.sin(phi * D) ** 2
    W = np.sqrt(1 - E2_GRS * s2)
    return A_GRS * (1 - E2_GRS) / W**3, A_GRS / W


def psi(phi):
    return np.log(np.tan(np.pi / 4 + phi * D / 2))


def loxodromia(phi1, lam1, phi2, lam2):
    """Rumbo (grados) y largo angular (radianes) de la loxodromia sobre la esfera."""
    dpsi, dl = psi(phi2) - psi(phi1), (lam2 - lam1) * D
    alfa = np.arctan2(dl, dpsi)
    largo = (phi2 - phi1) * D / np.cos(alfa)
    return (alfa / D) % 360, largo


def dms(x):
    """Grados decimales -> texto g° m' s,ss''."""
    sg = "-" if x < 0 else ""
    x = abs(x)
    gr = int(x); mi = int((x - gr) * 60); se = (x - gr - mi / 60) * 3600
    if round(se, 2) >= 60:
        mi, se = mi + 1, se - 60
    return f"{sg}{gr}° {mi:02d}' {se:05.2f}''"


print("=" * 70)
print("E1  Octante")
A0, B0, C0 = np.array([0, 0, 1.0]), np.array([1.0, 0, 0]), np.array([0, 1.0, 0])
l0, g0 = triangulo(A0, B0, C0)
print("  lados (°)", l0 / D, " ángulos (°)", g0 / D)
e0 = g0.sum() - np.pi
print(f"  exceso = {e0:.6f} rad = pi/2? {np.isclose(e0, np.pi / 2)}; fracción = {e0 / (4 * np.pi):.4f}")

print("=" * 70)
print("E2  Buenos Aires - Córdoba - Mendoza, R = 6371 km")
R6371 = 6371.0
BA, CO, MZ = (-34.6, -58.4), (-31.4, -64.2), (-32.9, -68.8)
VA, VB, VC = unit(*BA), unit(*CO), unit(*MZ)
print("  r(BA) =", VA, " r(Co) =", VB, " r(Mz) =", VC)
lad, angs = triangulo(VA, VB, VC)
a, b, c = lad
An, Bn, Cn = angs
for nom, x in zip("abc", lad):
    print(f"  lado {nom} = {x / D:.4f}° = {x * R6371:.2f} km")
for nom, x in zip(["A (BA)", "B (Co)", "C (Mz)"], angs):
    print(f"  ángulo {nom} = {x / D:.4f}°")
print(f"  suma = {angs.sum() / D:.4f}°")
print(f"  coseno: cos a = {np.cos(a):.6f}; cos b cos c + sin b sin c cos A = "
      f"{np.cos(b) * np.cos(c) + np.sin(b) * np.sin(c) * np.cos(An):.6f}")
print(f"  coseno ángulos: cos A = {np.cos(An):.6f}; -cos B cos C + sin B sin C cos a = "
      f"{-np.cos(Bn) * np.cos(Cn) + np.sin(Bn) * np.sin(Cn) * np.cos(a):.6f}")
print("  seno: sin a/sin A, sin b/sin B, sin c/sin C =",
      [round(np.sin(x) / np.sin(y), 6) for x, y in zip(lad, angs)])
eps2 = angs.sum() - np.pi
print(f"  exceso suma = {eps2:.7e} rad = {eps2 / D:.4f}° = {eps2 * SEG:.1f}''")
print(f"  exceso L'Huilier = {lhuilier(a, b, c):.7e}; diferencia {abs(lhuilier(a, b, c) - eps2):.1e}")
print(f"  exceso det = {exceso_det(VA, VB, VC):.7e}; diferencia {abs(exceso_det(VA, VB, VC) - eps2):.1e}")
print(f"  área = eps R^2 = {eps2 * R6371**2:,.0f} km²")
# Legendre en BA: triángulo plano de lados R a, R b, R c
la, lb, lc = R6371 * lad
Aplano = np.arccos((lb**2 + lc**2 - la**2) / (2 * lb * lc))
print(f"  Legendre: A plano = {Aplano / D:.6f}°, A esf - eps/3 = {(An - eps2 / 3) / D:.6f}°, "
      f"dif = {(An - eps2 / 3 - Aplano) * SEG:.2f}''")

print("=" * 70)
print("E3  Rotaciones a lo largo de los lados (triángulo de E2)")
RAB = rot(np.cross(VA, VB), c)
RBC = rot(np.cross(VB, VC), a)
RCA = rot(np.cross(VC, VA), b)
print("  R_AB A = B?", np.allclose(RAB @ VA, VB), " R_BC B = C?", np.allclose(RBC @ VB, VC),
      " R_CA C = A?", np.allclose(RCA @ VC, VA))
Rtot = RCA @ RBC @ RAB
th = np.arccos((np.trace(Rtot) - 1) / 2)
w = np.array([Rtot[2, 1] - Rtot[1, 2], Rtot[0, 2] - Rtot[2, 0], Rtot[1, 0] - Rtot[0, 1]])
eje = w / np.linalg.norm(w)
print(f"  ángulo de la composición = {th:.7e} rad; exceso = {eps2:.7e}; dif = {abs(th - eps2):.1e}")
print(f"  eje . A = {eje @ VA:+.9f}  (±1: el eje es A)")
orient = np.sign(np.linalg.det(np.column_stack([VA, VB, VC])))
print(f"  det[A B C] = {np.linalg.det(np.column_stack([VA, VB, VC])):.6e} (signo del recorrido)")
# tangente en A hacia B y su imagen
tAB = VB - (VA @ VB) * VA
tAB /= np.linalg.norm(tAB)
tim = Rtot @ tAB
giro = np.arctan2(VA @ np.cross(tAB, tim), tAB @ tim)
print(f"  giro con signo de la tangente en A (alrededor de +A) = {giro:.7e} rad")

print("=" * 70)
print("A1  Buenos Aires -> Mendoza")
phim = (BA[0] + MZ[0]) / 2
M, N = MN(phim)
Rmn = np.sqrt(M * N)
R1 = (2 * A_GRS + B_GRS) / 3
print(f"  latitud media = {phim:.2f}°, M = {M:.1f} m, N = {N:.1f} m, sqrt(MN) = {Rmn:.1f} m")
print(f"  R1 = (2a+b)/3 = {R1:.1f} m")
sig, az1, az2 = inverso(*BA, *MZ)
print(f"  inverso: sigma = {sig:.6f}°, Az partida = {az1:.4f}°, Az llegada = {az2:.4f}°")
print(f"  contraacimut en Mendoza = {(az2 + 180) % 360:.4f}°; cambio de acimut = {az2 - az1:.4f}°")
d_mn, d_r1 = Rmn * sig * D, R1 * sig * D
g = Geod(ellps="GRS80")
gaz1, gaz21, gdist = g.inv(BA[1], BA[0], MZ[1], MZ[0])
gaz2 = (gaz21 + 180) % 360
print(f"  esfera sqrt(MN): {d_mn:.1f} m; esfera R1: {d_r1:.1f} m; GRS80 (pyproj): {gdist:.1f} m")
print(f"  dif sqrt(MN) - GRS80 = {d_mn - gdist:+.1f} m = {(d_mn - gdist) / gdist * 1e6:+.0f} ppm")
print(f"  dif R1 - GRS80 = {d_r1 - gdist:+.1f} m = {(d_r1 - gdist) / gdist * 1e6:+.0f} ppm")
print(f"  GRS80 Az partida = {gaz1 % 360:.4f}°, Az llegada = {gaz2:.4f}°; "
      f"dif esfera - elipsoide: {(az1 - gaz1 % 360) * 3600:+.0f}'' y {(az2 - gaz2) * 3600:+.0f}''")
# radio de curvatura en el acimut medio (Euler) como lectura del resultado
alm = (az1 + az2) / 2 * D
Ralfa = M * N / (N * np.cos(alm) ** 2 + M * np.sin(alm) ** 2)
print(f"  acimut medio = {(az1 + az2) / 2:.2f}°; R_alfa (Euler) = {Ralfa:.1f} m; "
      f"sigma*R_alfa - GRS80 = {Ralfa * sig * D - gdist:+.2f} m = {(Ralfa * sig * D - gdist) / gdist * 1e6:+.2f} ppm")
# Tolerancia declarada: una esfera aproxima al elipsoide con error relativo acotado por la
# diferencia relativa entre los radios principales, (N - M)/M <= e^2 (unos 6700 ppm).
TOL_PPM = E2_GRS * 1e6
print(f"  tolerancia declarada e^2 = {TOL_PPM:.0f} ppm; (N - M)/M en phi_m = {(N - M) / M * 1e6:.0f} ppm")
assert abs(d_mn - gdist) / gdist * 1e6 < TOL_PPM and abs(d_r1 - gdist) / gdist * 1e6 < TOL_PPM
assert abs(Ralfa * sig * D - gdist) / gdist * 1e6 < 10
p2, l2, a2d = directo(BA[0], BA[1], az1, sig)
print(f"  directo(inverso): phi2 = {p2:.10f}°, lam2 = {l2:.10f}°, Az llegada = {a2d:.10f}°")
err = max(abs(p2 - MZ[0]), abs(l2 - MZ[1])) * D * Rmn
print(f"  error de cierre en posición = {err:.1e} m; dif Az = {abs(a2d - az2) * 3600:.1e}''")
assert err < 1e-6
Pv = directo_vectorial(BA[0], BA[1], az1, sig)
print(f"  forma vectorial: |P2 - r(Mz)| = {np.linalg.norm(Pv - unit(*MZ)):.1e}")
k1 = np.cos(BA[0] * D) * np.sin(az1 * D)
k2 = np.cos(MZ[0] * D) * np.sin(az2 * D)
print(f"  Clairaut: cos(phi1) sin(Az1) = {k1:.6f}; cos(phi2) sin(Az2) = {k2:.6f}")
rb, lx = loxodromia(*BA, *MZ)
print(f"  loxodromia: rumbo = {rb:.4f}°, largo = {lx * Rmn:.1f} m; "
      f"exceso sobre el círculo máximo = {lx * Rmn - d_mn:.1f} m")

print("=" * 70)
print("A2  Red de control (vértices aproximados)")
P1, P2, P3 = (-34.60, -58.40), (-34.90, -58.75), (-34.42, -58.90)
phim2 = (P1[0] + P2[0] + P3[0]) / 3
M2, N2 = MN(phim2)
R2 = np.sqrt(M2 * N2)
print(f"  latitud media = {phim2:.4f}°, sqrt(MN) = {R2:.1f} m")
W1, W2, W3 = unit(*P1), unit(*P2), unit(*P3)
lr, ar = triangulo(W1, W2, W3)
for nom, x in zip(["a (2-3)", "b (1-3)", "c (1-2)"], lr):
    print(f"  lado {nom} = {x * R2 / 1000:.3f} km")
for nom, x in zip(["1", "2", "3"], ar):
    print(f"  ángulo en {nom} = {x / D:.6f}° ")
epsr = ar.sum() - np.pi
print(f"  suma - 180° = {epsr * SEG:.3f}''")
sa, sb, sc = lr * R2
s = (sa + sb + sc) / 2
S = np.sqrt(s * (s - sa) * (s - sb) * (s - sc))
print(f"  S (Herón, lados) = {S / 1e6:.2f} km²; S/R^2 = {S / R2**2 * SEG:.3f}''; "
      f"dif con la suma = {(S / R2**2 - epsr) * SEG:.1e}''")
Sbc = 0.5 * sb * sc * np.sin(ar[0])
print(f"  (1/2) b c sin A / R^2 = {Sbc / R2**2 * SEG:.3f}''")
print(f"  corrección de Legendre por ángulo = eps/3 = {epsr / 3 * SEG:.3f}''")
Ap = [np.arccos((sb**2 + sc**2 - sa**2) / (2 * sb * sc)),
      np.arccos((sa**2 + sc**2 - sb**2) / (2 * sa * sc)),
      np.arccos((sa**2 + sb**2 - sc**2) / (2 * sa * sb))]
for k in range(3):
    print(f"  ángulo {k + 1}: esférico {dms(ar[k] / D)}, corregido {dms((ar[k] - epsr / 3) / D)}")
    print(f"  ángulo {k + 1}: plano = {Ap[k] / D:.6f}°, esf - eps/3 = {(ar[k] - epsr / 3) / D:.6f}°, "
          f"residuo = {(ar[k] - epsr / 3 - Ap[k]) * SEG:.1e}''")
print(f"  sin corregir, el error de cierre plano sería {epsr * SEG:.2f}''")
lg = []
for i, j in [(1, 2), (0, 2), (0, 1)]:
    Pi, Pj = (P1, P2, P3)[i], (P1, P2, P3)[j]
    lg.append(g.inv(Pi[1], Pi[0], Pj[1], Pj[0])[2])
    print(f"    GRS80 lado {i + 1}-{j + 1}: {lg[-1] / 1000:.3f} km; esfera - GRS80 = "
          f"{(lr[len(lg) - 1] * R2 - lg[-1]):+.1f} m")
ga, gb, gc_ = lg
sg_ = (ga + gb + gc_) / 2
Sg = np.sqrt(sg_ * (sg_ - ga) * (sg_ - gb) * (sg_ - gc_))
print(f"  con los lados GRS80: S = {Sg / 1e6:.2f} km², S/R^2 = {Sg / R2**2 * SEG:.3f}'', "
      f"eps/3 = {Sg / R2**2 / 3 * SEG:.3f}''")

print("=" * 70)
print("L  Buenos Aires -> Ciudad del Cabo (esfera R1)")
CT = (-33.9, 18.4)
sgc, azc1, azc2 = inverso(*BA, *CT)
rbc, lxc = loxodromia(*BA, *CT)
print(f"  círculo máximo: {sgc * D * R1 / 1000:.0f} km, Az partida = {azc1:.2f}°, llegada = {azc2:.2f}°")
print(f"  loxodromia: rumbo = {rbc:.2f}°, {lxc * R1 / 1000:.0f} km; "
      f"diferencia = {(lxc - sgc * D) * R1 / 1000:.0f} km")
phiext = np.arccos(np.cos(BA[0] * D) * abs(np.sin(azc1 * D))) / D
print(f"  latitud extrema del círculo máximo (Clairaut) = -{phiext:.2f}°; "
      f"{phiext + BA[0]:.2f}° al sur de Buenos Aires; giro del rumbo = {azc1 - azc2:.2f}°")

print("=" * 70)
print("X1  b = 50°, c = 70°, A = 80°")
b1, c1, A1 = 50 * D, 70 * D, 80 * D
a1 = np.arccos(np.cos(b1) * np.cos(c1) + np.sin(b1) * np.sin(c1) * np.cos(A1))
B1 = np.arccos((np.cos(b1) - np.cos(a1) * np.cos(c1)) / (np.sin(a1) * np.sin(c1)))
C1 = np.arccos((np.cos(c1) - np.cos(a1) * np.cos(b1)) / (np.sin(a1) * np.sin(b1)))
print(f"  cos a = {np.cos(a1):.6f}, a = {a1 / D:.4f}°, B = {B1 / D:.4f}°, C = {C1 / D:.4f}°")
print("  seno:", [round(np.sin(x) / np.sin(y), 6) for x, y in zip([a1, b1, c1], [A1, B1, C1])])
print(f"  exceso = {(A1 + B1 + C1 - np.pi) / D:.4f}°")

print("=" * 70)
print("X2  Equilátero de ángulos 100°")
Aq = 100 * D
cosa = (np.cos(Aq) + np.cos(Aq) ** 2) / np.sin(Aq) ** 2
print(f"  cos a = {cosa:.6f}, a = {np.arccos(cosa) / D:.4f}°; exceso = {(3 * Aq - np.pi) / D:.1f}° "
      f"= {(3 * Aq - np.pi) / np.pi:.4f} pi; fracción = {(3 * Aq - np.pi) / (4 * np.pi):.4f}")
print(f"  sobre R = 6371 km: lado = {np.arccos(cosa) * R6371:.0f} km, área = {(3 * Aq - np.pi) * R6371**2:,.0f} km²")

print("=" * 70)
print("X3  Directo desde (0,0), Az 45°, sigma 90°")
p3, l3, a3 = directo(0.0, 0.0, 45.0, 90.0)
print(f"  llegada ({p3:.6f}°, {l3:.6f}°), Az llegada = {a3:.6f}°")
print("  inverso de vuelta:", inverso(0, 0, p3, l3))
print(f"  Clairaut: {np.cos(0) * np.sin(45 * D):.6f} = {np.cos(p3 * D) * np.sin(a3 * D):.6f}")

print("=" * 70)
print("X4  Equilátero de 40 km sobre R = 6371 km")
L4 = 40.0
S4 = np.sqrt(3) / 4 * L4**2
e4 = S4 / R6371**2
print(f"  S = {S4:.2f} km², eps ≈ S/R^2 = {e4:.4e} rad = {e4 * SEG:.3f}''; eps/3 = {e4 / 3 * SEG:.3f}''")
s4 = L4 / R6371
e4x = lhuilier(s4, s4, s4)
S1 = np.sqrt(3) / 4
print(f"  equilátero de 1 km: S = {S1:.3f} km², eps = {S1 / R6371**2 * SEG:.4f}''")
print(f"  exacto (L'Huilier) = {e4x * SEG:.3f}''; ángulo esférico = {(np.pi / 3 + e4x / 3) / D:.7f}°")
cosA4 = (np.cos(s4) - np.cos(s4) ** 2) / np.sin(s4) ** 2
print(f"  ángulo esférico por el coseno = {np.arccos(cosA4) / D:.7f}°; "
      f"60° + eps/3 = 60° {e4 / 3 * SEG:.3f}''")

print("=" * 70)
print("X5  Paralelo -34,6°, Delta lambda = 10°")
s5, a51, a52 = inverso(-34.6, -58.4, -34.6, -68.4)
par = np.cos(34.6 * D) * 10 * D
print(f"  arco de paralelo = {par * R6371:.2f} km; círculo máximo = {s5 * D * R6371:.2f} km; "
      f"dif = {(par - s5 * D) * R6371:.2f} km")
print(f"  Az partida = {a51:.4f}°, Az llegada = {a52:.4f}° (rumbo del paralelo = 270°)")
phx = np.arccos(np.cos(34.6 * D) * abs(np.sin(a51 * D))) / D
print(f"  latitud extrema del círculo máximo = -{phx:.4f}°")


# ---------------------------------------------------------------- figuras
def esfera_malla(ax, alfa=0.25):
    for ph in range(-60, 90, 30):
        l = np.linspace(0, 360, 181)
        P = np.array([unit(ph, x) for x in l])
        ax.plot(*P.T, color=GRIS, lw=0.4, alpha=alfa)
    for la in range(0, 360, 30):
        p = np.linspace(-90, 90, 91)
        P = np.array([unit(x, la) for x in p])
        ax.plot(*P.T, color=GRIS, lw=0.4, alpha=alfa)


def arco(P, Q, n=80):
    t = ang(P, Q)
    k = np.cross(P, Q)
    return np.array([rot(k, s) @ P for s in np.linspace(0, t, n)])


def visible(ax, P, elev, azim):
    v = np.array([np.cos(elev * D) * np.cos(azim * D), np.cos(elev * D) * np.sin(azim * D), np.sin(elev * D)])
    return P @ v


def preparar(ax, elev, azim, zoom=1.45):
    ax.set_box_aspect((1, 1, 1), zoom=zoom)
    ax.view_init(elev=elev, azim=azim)
    ax.set_xlim(-1, 1); ax.set_ylim(-1, 1); ax.set_zlim(-1, 1)
    ax.set_axis_off()


# Figura 1: triángulo esférico y sus elementos
EL, AZ = 22, 20
fig = plt.figure(figsize=(5.6, 5.4))
ax = fig.add_subplot(projection="3d", computed_zorder=False)
preparar(ax, EL, AZ)
esfera_malla(ax)
TA, TB, TC = unit(62, 15), unit(8, -20), unit(14, 48)
for (P, Q) in [(TB, TC), (TA, TC), (TA, TB)]:
    ax.plot(*arco(P, Q).T, color=TEAL, lw=2.6)
for V, nom, col in [(TA, "A", TEAL), (TB, "B", RUST), (TC, "C", GOLD)]:
    ax.plot([0, V[0]], [0, V[1]], [0, V[2]], color=col, lw=1.4)
    ax.scatter(*V, color=col, s=28)
    ax.text(*(1.1 * V), nom, color=col, fontsize=13, weight="bold")
ax.scatter(0, 0, 0, color=TINTA, s=14)
ax.text(-0.02, -0.12, 0.03, "O", color=TINTA, fontsize=11)
# ángulo al centro del lado a (entre OB y OC)
arc_a = 0.32 * arco(TB, TC)
ax.plot(*arc_a.T, color=RUST, lw=1.2)
ax.text(*(0.2 * (TB + TC) / np.linalg.norm(TB + TC) + np.array([0, 0, 0.02])), "a", color=RUST, fontsize=10)
# rótulos de lados
for P, Q, nom in [(TB, TC, "a"), (TA, TC, "b"), (TA, TB, "c")]:
    m = (P + Q) / np.linalg.norm(P + Q)
    ax.text(*(1.08 * m), nom, color=TEAL, fontsize=12, style="italic")
# ángulos en los vértices: arco chico entre las tangentes
for V, P, Q, nom in [(TA, TB, TC, "A"), (TB, TC, TA, "B"), (TC, TA, TB, "C")]:
    tP = P - (V @ P) * V; tP /= np.linalg.norm(tP)
    tQ = Q - (V @ Q) * V; tQ /= np.linalg.norm(tQ)
    ax.plot(*np.array([V, V + 0.25 * tP]).T, color=TINTA, lw=0.9, ls="--")
    ax.plot(*np.array([V, V + 0.25 * tQ]).T, color=TINTA, lw=0.9, ls="--")
    t = ang(tP, tQ)
    k = np.cross(tP, tQ)
    pts = np.array([V + 0.15 * (rot(k, s) @ tP) for s in np.linspace(0, t, 30)])
    ax.plot(*pts.T, color=TINTA, lw=1.1)
ax.set_title("Triángulo esférico: lados = ángulos al centro, ángulos = diedros", fontsize=10)
fig.tight_layout()
fig.savefig(SALIDA / "esfera_triangulo.png", dpi=150, metadata=META)
plt.close(fig)

# Figura 2: lúnulas de Girard
EL2, AZ2 = 20, 15
fig = plt.figure(figsize=(5.6, 5.4))
ax = fig.add_subplot(projection="3d", computed_zorder=False)
preparar(ax, EL2, AZ2)
nA, nB, nC = np.cross(TB, TC), np.cross(TC, TA), np.cross(TA, TB)
if nA @ TA < 0:
    nA, nB, nC = -nA, -nB, -nC
uu, vv = np.meshgrid(np.linspace(-np.pi / 2, np.pi / 2, 361), np.linspace(-np.pi, np.pi, 721), indexing="ij")
X, Y, Z = np.cos(uu) * np.cos(vv), np.cos(uu) * np.sin(vv), np.sin(uu)
Pm = np.stack([X, Y, Z], axis=-1)
sA, sB, sC = Pm @ nA > 0, Pm @ nB > 0, Pm @ nC > 0
col = np.empty(X.shape + (4,))
col[:] = matplotlib.colors.to_rgba("#f2f1ee", 0.35)
col[sB & sC] = matplotlib.colors.to_rgba(TEAL, 0.8)   # huso de A
col[sA & sC] = matplotlib.colors.to_rgba(RUST, 0.8)   # huso de B
col[sA & sB] = matplotlib.colors.to_rgba(GOLD, 0.85)   # huso de C
col[sA & sB & sC] = matplotlib.colors.to_rgba(TINTA, 0.9)  # triángulo
col[visible(ax, Pm, EL2, AZ2) < 0] = (1, 1, 1, 0)  # cara oculta: transparente
ax.plot_surface(X, Y, Z, facecolors=col, rstride=1, cstride=1, linewidth=0, shade=False)
for n in (nA, nB, nC):
    k = n / np.linalg.norm(n)
    u0 = np.cross(k, [0, 0, 1.0]); u0 /= np.linalg.norm(u0)
    circ = np.array([rot(k, s) @ u0 for s in np.linspace(0, 2 * np.pi, 361)]) * 1.003
    vis = visible(ax, circ, EL2, AZ2) > 0
    c2 = circ.copy(); c2[~vis] = np.nan
    ax.plot(*c2.T, color=TINTA, lw=1.0)
for V, nom, cc in [(TA, "A", TEAL), (TB, "B", RUST), (TC, "C", GOLD)]:
    ax.text(*(1.12 * V), nom, color=cc, fontsize=13, weight="bold")
ax.set_title("Husos de ángulo A (teal), B (rust) y C (gold); el triángulo, común a los tres", fontsize=9.5)
fig.tight_layout()
fig.savefig(SALIDA / "esfera_lunulas.png", dpi=150, metadata=META)
plt.close(fig)

# Figura 3: círculo máximo vs loxodromia Buenos Aires -> Ciudad del Cabo
Pba, Pct = unit(*BA), unit(*CT)
gc = arco(Pba, Pct, 300)
gc_phi = np.arcsin(gc[:, 2]) / D
gc_lam = np.arctan2(gc[:, 1], gc[:, 0]) / D
lam_lx = np.linspace(BA[1], CT[1], 300)
psi_lx = psi(BA[0]) + (psi(CT[0]) - psi(BA[0])) * (lam_lx - BA[1]) / (CT[1] - BA[1])
phi_lx = (2 * np.arctan(np.exp(psi_lx)) - np.pi / 2) / D
fig = plt.figure(figsize=(10.5, 4.6))
ax1 = fig.add_subplot(1, 2, 1)
for ph in range(-60, 1, 10):
    ax1.axhline(psi(ph), color=GRIS, lw=0.4)
for la in range(-80, 41, 20):
    ax1.axvline(la, color=GRIS, lw=0.4)
ax1.plot(gc_lam, psi(gc_phi), color=TEAL, lw=2.2, label=f"círculo máximo ({sgc * D * R1 / 1000:.0f} km)")
ax1.plot(lam_lx, psi(phi_lx), color=RUST, lw=2.2, ls="--", label=f"loxodromia ({lxc * R1 / 1000:.0f} km)")
for (ph, la), nom in [(BA, "Buenos Aires"), (CT, "Ciudad del Cabo")]:
    ax1.plot(la, psi(ph), "o", color=TINTA, ms=5)
    ax1.annotate(nom, (la, psi(ph)), textcoords="offset points", xytext=(-10, 8), fontsize=9)
ax1.set_yticks([psi(p) for p in range(-60, 1, 10)])
ax1.set_yticklabels([f"{p}°" for p in range(-60, 1, 10)])
ax1.set_xticks(range(-80, 41, 20))
ax1.set_xticklabels([f"{x}°" for x in range(-80, 41, 20)])
ax1.set_xlim(-75, 30); ax1.set_ylim(psi(-62), psi(-15))
ax1.set_xlabel("longitud"); ax1.set_ylabel("latitud (escala de Mercator)")
ax1.set_title("Mercator: la loxodromia es recta", fontsize=10)
ax1.legend(loc="lower left", fontsize=8.5, framealpha=0.95)
ax2 = fig.add_subplot(1, 2, 2, projection="3d", computed_zorder=False)
EL3, AZ3 = -30, -20
preparar(ax2, EL3, AZ3, zoom=1.9)
esfera_malla(ax2, 0.3)
lx3 = np.array([unit(p, l) for p, l in zip(phi_lx, lam_lx)])
ax2.plot(*gc.T, color=TEAL, lw=2.2)
ax2.plot(*lx3.T, color=RUST, lw=2.2, ls="--")
for P, nom in [(Pba, "BA"), (Pct, "CdC")]:
    ax2.scatter(*P, color=TINTA, s=16)
    ax2.text(*(1.08 * P), nom, fontsize=9)
ax2.set_title("Sobre la esfera: el círculo máximo baja hacia el polo", fontsize=10)
fig.tight_layout()
fig.savefig(SALIDA / "esfera_loxodromia.png", dpi=150, metadata=META)
plt.close(fig)
print("=" * 70)
print("Figuras en", SALIDA.relative_to(Path(__file__).resolve().parents[2]))
