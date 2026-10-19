"""Números y figuras del capítulo «Cambio de base: las coordenadas son etiquetas».

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  E1  Ejemplo «El mismo vector en dos bases, ida y vuelta»: base oblicua b1 = (3,1),
      b2 = (1,2); C = [b1 b2], det C, C^{-1}; v = (7,4) -> [v]_b = C^{-1} v y vuelta C [v]_b;
      forma lineal phi = (1,1): [phi]_b = phi C y phi(v) en las dos bases; matriz de Gram
      G = C^T C y |v|^2 = [v]_b^T G [v]_b (sección de bases ortonormales).
  E2  Ejemplo «Reflexión respecto de una recta inclinada por semejanza»: recta de dirección
      (2,1), C = [(2,1) (-1,2)], M = C diag(1,-1) C^{-1}; imagen de (5,0); invariantes
      (det, traza, autovalores) de M y de diag(1,-1); versión con base ortonormal C/sqrt5.
  E3  Ejemplo «Diagonalizar una simétrica: potencias y raíz cuadrada»: M = [[5,2],[2,2]],
      autovalores 6 y 1, autovectores (2,1), (-1,2); M^10 = A D^10 A^{-1} (enteros);
      M^{1/2} = A D^{1/2} A^{-1} y control R^2 = M; trayectoria M^t (1,0) en t = 1/2.
  E4  Ejemplo «Activa y pasiva»: v = (3,1), theta = 30°: R v (girar el vector) y R^T v
      (girar los ejes); módulo igual.
  A   Aplicación topográfica: eje de obra de acimut 127°30'; u_L, u_T (a la derecha), C,
      det C = -1, C^T C = I; tres puntos en Gauss-Krüger faja 5, dos campañas;
      desplazamientos en mm (E, N) -> (L, T) = C^T d; módulos en las dos bases;
      tolerancia D = diag(1/20^2, 1/5^2) en la base de obra, Q = C D C^T en (E, N);
      q = x^T Q x en las dos bases y decisión q <= 1.
  X1  Ejercicio 1: base b1 = (1,1), b2 = (-1,2); v = (1,7); forma (2,-1).
  X2  Ejercicio 2: proyección ortogonal sobre la recta de dirección (3,4) desde diag(1,0).
  X3  Ejercicio 3: M = [[4,1],[2,3]]: autovalores, autovectores, M^3 por A D^3 A^{-1}, traza, det.
  X4  Ejercicio 4: raíz cuadrada de M = [[10,6],[6,10]].

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/cambio-de-base/:
  cb_dos_grillas.png      el vector v = (7,4) sobre la grilla canónica (7,4) y sobre la grilla
                          oblicua de b1, b2 (coordenadas (2,1)).
  cb_autovectores.png     M = [[5,2],[2,2]] aplicada a la grilla canónica (se deforma) y a la
                          grilla de autovectores (sólo se estira: x6 y x1).
  cb_activa_pasiva.png    v = (3,1): girar el vector 30° (activa) o girar los ejes 30° (pasiva).
  cb_obra.png             eje de obra, base (u_L, u_T), elipse de tolerancia (escala mm) y los
                          tres desplazamientos.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/cap09_cambio_de_base.py
"""
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

np.set_printoptions(precision=4, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "cambio-de-base"
SALIDA.mkdir(parents=True, exist_ok=True)
TEAL, RUST, GOLD, GRIS, VIOLETA = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780", "#7a4e9e"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})


def flecha(ax, a, b, color, lw=2.0):
    ax.annotate("", b, a, arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, shrinkA=0, shrinkB=0))


def grilla(ax, b1, b2, k, color, lw=.7, alpha=1.0, ls="-"):
    for i in range(-k, k + 1):
        p, q = i * b1 - k * b2, i * b1 + k * b2
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, alpha=alpha, ls=ls)
        p, q = i * b2 - k * b1, i * b2 + k * b1
        ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, alpha=alpha, ls=ls)


# ---------------------------------------------------------------- E1
print("=== E1  mismo vector, dos bases ===")
b1, b2 = np.array([3.0, 1.0]), np.array([1.0, 2.0])
C1 = np.column_stack([b1, b2])
C1inv = np.linalg.inv(C1)
v = np.array([7.0, 4.0])
vb = C1inv @ v
print("C =", C1.tolist(), " det C =", round(np.linalg.det(C1), 6), " 5 C^{-1} =", np.round(5 * C1inv, 6).tolist())
print("[v]_b = C^{-1} v =", vb, "  vuelta C [v]_b =", C1 @ vb)
phi = np.array([1.0, 1.0])
print("[phi]_b = phi C =", phi @ C1, "  phi(v) canónica =", phi @ v, "  en b =", (phi @ C1) @ vb)
print("(error típico) C^{-1} phi^T =", C1inv @ phi, " producto con [v]_b =", (C1inv @ phi) @ vb)
G = C1.T @ C1
print("Gram G = C^T C =", G.tolist(), "  |v|^2 canónica =", v @ v, "  [v]_b^T G [v]_b =", vb @ G @ vb, "  (2,1).(2,1) ingenuo =", vb @ vb)

# ---------------------------------------------------------------- E2
print("\n=== E2  reflexión por semejanza ===")
C2 = np.array([[2.0, -1.0], [1.0, 2.0]])
D2 = np.diag([1.0, -1.0])
M2 = C2 @ D2 @ np.linalg.inv(C2)
print("C^{-1}*5 =", np.round(5 * np.linalg.inv(C2), 6).tolist())
print("M = C diag(1,-1) C^{-1} =", M2, " 5M =", np.round(5 * M2, 6).tolist())
print("M (5,0) =", M2 @ [5, 0], " M (2,1) =", M2 @ [2, 1], " M (-1,2) =", M2 @ [-1, 2], " M^2 =", np.round(M2 @ M2, 6).tolist())
print("det, traza M =", round(np.linalg.det(M2), 6), round(np.trace(M2), 6), " autovalores =", np.round(np.linalg.eigvals(M2), 6))
U2 = C2 / np.sqrt(5)
print("U = C/sqrt5: U^T U =", np.round(U2.T @ U2, 6).tolist(), " U D U^T =", np.round(U2 @ D2 @ U2.T, 6).tolist())
th = np.degrees(np.arctan2(1, 2))
print("ángulo de la recta =", round(th, 4), " cos 2th, sin 2th =", round(np.cos(np.radians(2 * th)), 6), round(np.sin(np.radians(2 * th)), 6))

# ---------------------------------------------------------------- E3
print("\n=== E3  diagonalización, potencias, raíz ===")
M3 = np.array([[5.0, 2.0], [2.0, 2.0]])
A3 = np.array([[2.0, -1.0], [1.0, 2.0]])
w, _ = np.linalg.eig(M3)
print("autovalores =", np.sort(w)[::-1], " traza, det =", np.trace(M3), round(np.linalg.det(M3), 6))
print("M (2,1) =", M3 @ [2, 1], " M (-1,2) =", M3 @ [-1, 2])
print("A^{-1} M A =", np.round(np.linalg.inv(A3) @ M3 @ A3, 6).tolist())
M3i = np.array([[5, 2], [2, 2]], dtype=object)
P10 = np.linalg.matrix_power(M3i, 10)
print("6^10 =", 6 ** 10, "  M^10 (exacta) =", P10.tolist())
print("fórmula: (4*6^10+1)/5, (2*6^10-2)/5, (6^10+4)/5 =", (4 * 6 ** 10 + 1) / 5, (2 * 6 ** 10 - 2) / 5, (6 ** 10 + 4) / 5)
R3 = A3 @ np.diag(np.sqrt([6.0, 1.0])) @ np.linalg.inv(A3)
print("sqrt6 =", round(np.sqrt(6), 6), "  M^{1/2} =", np.round(R3, 4).tolist(), "  R^2 =", np.round(R3 @ R3, 10).tolist())
print("M^{1/2} entradas exactas: (4r+1)/5, (2r-2)/5, (r+4)/5 con r = sqrt6:",
      round((4 * np.sqrt(6) + 1) / 5, 4), round((2 * np.sqrt(6) - 2) / 5, 4), round((np.sqrt(6) + 4) / 5, 4))
print("M^{1/2} (1,0) =", np.round(R3 @ [1, 0], 4), "  autovalores de M^{1/2} =", np.round(np.linalg.eigvals(R3), 4))

# ---------------------------------------------------------------- E4
print("\n=== E4  activa / pasiva ===")
t = np.radians(30)
R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
v4 = np.array([3.0, 1.0])
print("activa R v =", np.round(R @ v4, 3), "  pasiva R^T v =", np.round(R.T @ v4, 3))
print("módulos:", round(np.linalg.norm(v4), 3), round(np.linalg.norm(R @ v4), 3), round(np.linalg.norm(R.T @ v4), 3))

# ---------------------------------------------------------------- A
print("\n=== A  aplicación: coordenadas de obra ===")
az = np.radians(127.5)
uL = np.array([np.sin(az), np.cos(az)])
uT = np.array([np.sin(az + np.pi / 2), np.cos(az + np.pi / 2)])
CA = np.column_stack([uL, uT])
print("u_L =", np.round(uL, 4), " u_T =", np.round(uT, 4), " det C =", round(np.linalg.det(CA), 6), " C^T C =", np.round(CA.T @ CA, 10).tolist())
camp1 = np.array([[5512340.215, 6178905.480], [5512419.550, 6178844.604], [5512498.886, 6178783.728]])
desp_mm = np.array([[8, -10], [7, 2], [-15, 9]])
camp2 = camp1 + desp_mm / 1000
for i in range(3):
    print(f"P{i+1}: campaña 1 = ({camp1[i,0]:.3f}, {camp1[i,1]:.3f})  campaña 2 = ({camp2[i,0]:.3f}, {camp2[i,1]:.3f})")
# control: los puntos están sobre el eje (distancias entre ellos a lo largo de u_L)
for j in (1, 2):
    d12 = camp1[j] - camp1[0]
    print(f"P1->P{j+1}:", np.round(d12, 3), " L =", round(d12 @ uL, 3), " T =", round(d12 @ uT, 3))
D = np.diag([1 / 20 ** 2, 1 / 5 ** 2])
Q = CA @ D @ CA.T
print("D =", np.diag(D), "  Q = C D C^T =", np.round(Q, 6).tolist(), "  Q*1000 =", np.round(1000 * Q, 4).tolist())
print("traza D, traza Q =", np.trace(D), round(np.trace(Q), 6), "  det D, det Q =", D[0, 0] * D[1, 1], round(np.linalg.det(Q), 10))
for i in range(3):
    d = np.round((camp2[i] - camp1[i]) * 1000, 6)
    lt = CA.T @ d
    qEN, qLT = d @ Q @ d, lt @ D @ lt
    print(f"P{i+1}: d(E,N) mm = {d}  (L,T) = {np.round(lt, 2)}  |d| EN = {np.linalg.norm(d):.2f}  |d| LT = {np.linalg.norm(lt):.2f}"
          f"  q EN = {qEN:.4f}  q LT = {qLT:.4f}  -> {'dentro' if qLT <= 1 else 'FUERA'}"
          f"  términos L^2/400 = {lt[0]**2/400:.4f}  T^2/25 = {lt[1]**2/25:.4f}")
    print(f"     isótropo con radio 20 mm: |d|/20 = {np.linalg.norm(d)/20:.3f}")
    print(f"     términos en E,N (x1000): Q11 dE^2 = {1000*Q[0,0]*d[0]**2:.2f}  2 Q12 dE dN = {2000*Q[0,1]*d[0]*d[1]:.2f}  Q22 dN^2 = {1000*Q[1,1]*d[1]**2:.2f}")

# ---------------------------------------------------------------- X1
print("\n=== X1 ===")
C = np.array([[1.0, -1.0], [1.0, 2.0]])
print("det =", round(np.linalg.det(C), 6), " 3 C^{-1} =", np.round(3 * np.linalg.inv(C), 6).tolist())
vb = np.linalg.solve(C, [1, 7]); f = np.array([2.0, -1.0])
print("[v]_b =", vb, " control C vb =", C @ vb, " [f]_b = f C =", f @ C, " f(v) =", f @ [1, 7], (f @ C) @ vb)

# ---------------------------------------------------------------- X2
print("\n=== X2 ===")
u = np.array([3.0, 4.0]) / 5; n = np.array([-4.0, 3.0]) / 5
U = np.column_stack([u, n])
P = U @ np.diag([1.0, 0.0]) @ U.T
print("P =", P, " 25P =", np.round(25 * P, 6).tolist(), " P^2 - P =", np.round(P @ P - P, 12).tolist())
print("det, traza =", round(np.linalg.det(P), 10), np.trace(P), " P (5,0) =", P @ [5, 0], " P (-4,3) =", P @ [-4, 3])

# ---------------------------------------------------------------- X3
print("\n=== X3 ===")
M = np.array([[4.0, 1.0], [2.0, 3.0]])
print("autovalores =", np.sort(np.linalg.eigvals(M))[::-1], " traza, det =", np.trace(M), round(np.linalg.det(M), 6))
A = np.array([[1.0, 1.0], [1.0, -2.0]])
print("M (1,1) =", M @ [1, 1], " M (1,-2) =", M @ [1, -2], " det A =", round(np.linalg.det(A), 6), " 3 A^{-1} =", np.round(3 * np.linalg.inv(A), 6).tolist())
M3 = A @ np.diag([125.0, 8.0]) @ np.linalg.inv(A)
print("M^3 = A D^3 A^{-1} =", np.round(M3, 6).tolist(), " directo =", np.linalg.matrix_power(M, 3).tolist())
print("u1.u2 =", A[:, 0] @ A[:, 1], "  A^T A =", (A.T @ A).tolist())

# ---------------------------------------------------------------- X4
print("\n=== X4 ===")
M = np.array([[10.0, 6.0], [6.0, 10.0]])
print("autovalores =", np.sort(np.linalg.eigvals(M))[::-1])
A = np.array([[1.0, 1.0], [1.0, -1.0]])
R = A @ np.diag([4.0, 2.0]) @ np.linalg.inv(A)
print("R = A diag(4,2) A^{-1} =", R.tolist(), " R^2 =", (R @ R).tolist())
R2 = A @ np.diag([-4.0, 2.0]) @ np.linalg.inv(A)
print("otra raíz A diag(-4,2) A^{-1} =", R2.tolist(), " cuadrado =", (R2 @ R2).tolist())

# ================================================================ FIGURAS
# --- figura 1: dos grillas
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.4))
v = np.array([7.0, 4.0])
for ax, (e1, e2, tit, coords, k) in zip(axs, (
        (np.array([1.0, 0]), np.array([0, 1.0]), "grilla canónica: $v = 7e_1 + 4e_2$", (7, 4), 9),
        (b1, b2, "grilla oblicua: $v = 2b_1 + 1b_2$", (2, 1), 4))):
    grilla(ax, e1, e2, k, "#d8d5ce" if k == 9 else "#9cc7cf", lw=.8)
    flecha(ax, (0, 0), e1, TEAL, 2.2); flecha(ax, (0, 0), e2, RUST, 2.2)
    n1, n2 = ("e_1", "e_2") if k == 9 else ("b_1", "b_2")
    ax.text(*(e1 + [.1, -.55]), f"${n1}$", color=TEAL, fontsize=12)
    ax.text(*(e2 + [-.75, .15]), f"${n2}$", color=RUST, fontsize=12)
    c1, c2 = coords
    camino = [np.zeros(2), c1 * e1, c1 * e1 + c2 * e2]
    ax.plot([camino[0][0], camino[1][0]], [camino[0][1], camino[1][1]], color=TEAL, lw=1.4, ls="--")
    ax.plot([camino[1][0], camino[2][0]], [camino[1][1], camino[2][1]], color=RUST, lw=1.4, ls="--")
    flecha(ax, (0, 0), v, VIOLETA, 2.6)
    ax.text(v[0] - 1.2, v[1] + .35, f"$v$: $({c1},\\,{c2})$", color=VIOLETA, fontsize=12)
    ax.set_xlim(-1, 8.5); ax.set_ylim(-1, 6); ax.set_aspect("equal")
    ax.set_title(tit, fontsize=11); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(SALIDA / "cb_dos_grillas.png", dpi=150); plt.close(fig)

# --- figura 2: transformación en la base de autovectores
M3 = np.array([[5.0, 2.0], [2.0, 2.0]])
a1, a2 = np.array([2.0, 1.0]) / np.sqrt(5), np.array([-1.0, 2.0]) / np.sqrt(5)
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.6))
for ax, (e1, e2, tit) in zip(axs, (
        (np.array([1.0, 0]), np.array([0, 1.0]), "grilla canónica: los cuadrados se tuercen"),
        (a1, a2, "grilla de autovectores: sólo se estira ($\\times6$, $\\times1$)"))):
    grilla(ax, e1, e2, 3, "#d8d5ce", lw=.7)
    grilla(ax, M3 @ e1, M3 @ e2, 3, "#9cc7cf", lw=.8)
    sq = np.array([np.zeros(2), e1, e1 + e2, e2])
    ax.add_patch(Polygon(sq, closed=True, fc=GRIS, alpha=.25, ec=GRIS, lw=1.2))
    ax.add_patch(Polygon((M3 @ sq.T).T, closed=True, fc=TEAL, alpha=.25, ec=TEAL, lw=1.5))
    flecha(ax, (0, 0), M3 @ e1, TEAL, 2.2); flecha(ax, (0, 0), M3 @ e2, RUST, 2.2)
    flecha(ax, (0, 0), e1, GRIS, 1.6); flecha(ax, (0, 0), e2, GRIS, 1.6)
    ax.set_xlim(-3.5, 7.5); ax.set_ylim(-3, 5.5); ax.set_aspect("equal")
    ax.set_title(tit, fontsize=10); ax.set_xticks([]); ax.set_yticks([])
axs[0].text(5.1, 2.3, "$Me_1=(5,2)$", color=TEAL); axs[0].text(2.2, 2.6, "$Me_2=(2,2)$", color=RUST)
axs[1].text(4.2, 3.0, "$Mu_1=6u_1$", color=TEAL); axs[1].text(-2.8, 1.4, "$Mu_2=u_2$", color=RUST)
fig.tight_layout(); fig.savefig(SALIDA / "cb_autovectores.png", dpi=150); plt.close(fig)

# --- figura 3: activa vs pasiva
t = np.radians(30)
R = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
v4 = np.array([3.0, 1.0])
fig, axs = plt.subplots(1, 2, figsize=(9.6, 4.2))
ax = axs[0]
for e in (np.array([1.0, 0]), np.array([0, 1.0])):
    flecha(ax, (0, 0), 3.6 * e, GRIS, 1.2)
flecha(ax, (0, 0), v4, VIOLETA, 1.6); flecha(ax, (0, 0), R @ v4, TEAL, 2.4)
tt = np.linspace(np.arctan2(1, 3), np.arctan2(1, 3) + t, 30)
ax.plot(1.8 * np.cos(tt), 1.8 * np.sin(tt), color=TEAL, lw=1.2)
ax.text(3.05, .85, "$v=(3,1)$", color=VIOLETA); ax.text(1.2, 2.5, "$Rv=(2{,}098;\\ 2{,}366)$", color=TEAL)
ax.text(3.65, -.15, "$x$", color=GRIS); ax.text(-.1, 3.7, "$y$", color=GRIS)
ax.set_title("activa: gira el vector, los ejes quedan", fontsize=10)
ax = axs[1]
for e in (np.array([1.0, 0]), np.array([0, 1.0])):
    ax.plot(*np.array([[0, 0], 3.6 * e]).T, color=GRIS, lw=.8, ls=":")
ex, ey = R @ [1, 0], R @ [0, 1]
flecha(ax, (0, 0), 3.6 * ex, TEAL, 1.6); flecha(ax, (0, 0), 3.0 * ey, TEAL, 1.6)
ax.text(*(3.6 * ex + [.05, .05]), "$x'$", color=TEAL); ax.text(*(3.0 * ey + [-.3, .1]), "$y'$", color=TEAL)
c = R.T @ v4
ax.plot(*np.array([[0, 0], c[0] * ex, c[0] * ex + c[1] * ey]).T, color=TEAL, lw=1.1, ls="--")
flecha(ax, (0, 0), v4, VIOLETA, 2.4)
ax.text(1.3, -.55, "$v$: $(3{,}098;\\ -0{,}634)$ en $x'y'$", color=VIOLETA)
ax.set_title("pasiva: giran los ejes, el vector queda", fontsize=10)
for ax in axs:
    ax.set_xlim(-1.6, 4.6); ax.set_ylim(-1, 4); ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
fig.tight_layout(); fig.savefig(SALIDA / "cb_activa_pasiva.png", dpi=150); plt.close(fig)

# --- figura 4: obra
fig, ax = plt.subplots(figsize=(6.4, 6.0))
s = np.linspace(-26, 26, 2)
ax.plot(s * uL[0], s * uL[1], color=GRIS, lw=1, ls="-.")
ax.text(*(22 * uL + [-9, -6]), "eje de obra\nAz $127^\\circ30'$", color=GRIS, fontsize=9)
tt = np.linspace(0, 2 * np.pi, 200)
ell = (CA @ np.vstack([20 * np.cos(tt), 5 * np.sin(tt)])).T
ax.fill(ell[:, 0], ell[:, 1], color=TEAL, alpha=.12); ax.plot(ell[:, 0], ell[:, 1], color=TEAL, lw=1.4)
flecha(ax, (0, 0), 10 * uL, TEAL, 2); flecha(ax, (0, 0), 10 * uT, RUST, 2)
ax.text(*(10 * uL + [.6, .4]), "$u_L$", color=TEAL, fontsize=12); ax.text(*(10 * uT + [-3.2, -.8]), "$u_T$", color=RUST, fontsize=12)
for i, d in enumerate(desp_mm):
    q = (CA.T @ d) @ D @ (CA.T @ d)
    col = VIOLETA if q <= 1 else "#222222"
    flecha(ax, (0, 0), d, col, 1.8)
    ax.text(d[0] + .6, d[1] + .4, f"$P_{i+1}$", color=col, fontsize=11)
flecha(ax, (-24, -20), (-24, -12), "black", 1.0); ax.text(-24.8, -11, "N", fontsize=9)
ax.axhline(0, color="#d8d5ce", lw=.6); ax.axvline(0, color="#d8d5ce", lw=.6)
ax.set_xlim(-26, 26); ax.set_ylim(-22, 22); ax.set_aspect("equal")
ax.set_xlabel("$\\Delta E$ (mm)"); ax.set_ylabel("$\\Delta N$ (mm)")
ax.set_title("tolerancia: 20 mm longitudinal, 5 mm transversal", fontsize=10)
fig.tight_layout(); fig.savefig(SALIDA / "cb_obra.png", dpi=150); plt.close(fig)
print("\nFiguras en", SALIDA)
