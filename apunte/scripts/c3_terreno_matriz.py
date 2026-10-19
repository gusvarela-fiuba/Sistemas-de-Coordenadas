"""Números y figuras del complemento C3 «El terreno como matriz».

Datos: sintéticos. Un terreno de juguete generado por este script con la semilla 2026
(numpy.random.default_rng(2026) elige, redondeados, los centros y las alturas de una loma
y de una hondonada); nada sale de mediciones reales.

Cubre, en este orden (cada número que aparece en el texto se imprime con su etiqueta):
  T   El terreno: h(x,y) = 100 + A1 exp(-d1^2/800) - A2 exp(-d2^2/200), con d1, d2 las
      distancias a los centros de la loma y de la hondonada; cuadrícula de 21 x 21 nodos
      cada 5 m (x hacia el este, y hacia el norte, fila 0 al norte); matriz Z, mínimo,
      máximo, esquina noroeste 3 x 3.
  E1  Ejemplo «Pendiente y orientación en un nodo»: ventana 3 x 3 alrededor del nodo
      (fila 10, columna 13), diferencias centradas con paso 5 m y con paso 10 m, gradiente
      exacto, pendiente en por ciento y en grados, orientación de la bajada (Az).
  E2  Ejemplo «Volumen de una celda y de todo el desmonte»: prisma de la celda
      (filas 10-11, columnas 8-9) sobre el plano z0 = 95 m; suma de los 400 prismas;
      integral exacta con erf; error; la suma ingenua de 441 columnas de 5 x 5 m.
  A   Aplicación: pendiente máxima y dónde, volumen del desmonte, remuestreo a una
      cuadrícula de 10 m con origen corrido 3 m al este y 3 m al norte (10 x 10 nodos):
      vecino más próximo y bilineal contra la fórmula (error RMS y máximo, volumen sobre
      el cuadrado [3, 93]^2 contra su integral exacta, pendiente máxima en la cuadrícula
      gruesa).
  X1  Ejercicio 1: planilla 3 x 3 cada 10 m; gradiente, pendiente y orientación en el centro.
  X2  Ejercicio 2: volumen sobre el plano de 99 m de la misma planilla (4 prismas) y la
      suma ingenua de 9 columnas.
  X3  Ejercicio 3: celda (1496, 1504, 1508, 1498) del recorte; bilineal en (0,3; 0,6),
      vecino más próximo; integral de la bilineal = promedio de las esquinas.
  X4  Ejercicio 4: efecto sobre pendiente, orientación y volumen de sumar 10 m, duplicar
      y espejar norte-sur la planilla del ejercicio 1.

Figuras (PNG, fondo blanco, dpi 150) en apunte/figuras/terreno-matriz/:
  terreno_planilla.png     la matriz Z como imagen con curvas de nivel cada 1 m y la
                           superficie en perspectiva sobre el plano de 95 m.
  terreno_pendiente.png    mapa de pendiente (por ciento) con flechas de la bajada.
  terreno_remuestreo.png   error del remuestreo a 10 m: vecino más próximo y bilineal.

Ejecutar desde la raíz del repo:
  uv run python apunte/scripts/c3_terreno_matriz.py
"""
from math import erf, sqrt, pi, atan, atan2, degrees, hypot
from pathlib import Path

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=3, suppress=True)
SALIDA = Path(__file__).resolve().parents[1] / "figuras" / "terreno-matriz"
TEAL, RUST, GOLD, GRIS = "#1f7a8c", "#b5533c", "#c9a227", "#8a8780"
plt.rcParams.update({"font.size": 10, "axes.edgecolor": GRIS, "savefig.facecolor": "white"})
META = {"Software": None}


def titulo(t):
    print("\n" + "=" * 8 + " " + t)


def cerca(a, b, tol):
    assert abs(a - b) <= tol, (a, b)


# ---------------------------------------------------------------- T  el terreno
_rng = np.random.default_rng(2026)
X1, Y1 = (float(v) for v in np.round(_rng.uniform(35, 45, 2)))
X2, Y2 = (float(v) for v in np.round(_rng.uniform(65, 80, 2)))
A1 = float(np.round(_rng.uniform(7, 9), 1))
A2 = float(np.round(_rng.uniform(2.5, 3.5), 1))
B1, B2 = 800.0, 200.0          # denominadores de las exponenciales (2 s^2 con s = 20 y 10 m)
BASE, Z0, PASO, N = 100.0, 95.0, 5.0, 21


def h(x, y):
    return (BASE + A1 * np.exp(-((x - X1) ** 2 + (y - Y1) ** 2) / B1)
            - A2 * np.exp(-((x - X2) ** 2 + (y - Y2) ** 2) / B2))


def grad_h(x, y):
    e1 = A1 * np.exp(-((x - X1) ** 2 + (y - Y1) ** 2) / B1)
    e2 = A2 * np.exp(-((x - X2) ** 2 + (y - Y2) ** 2) / B2)
    return (-2 * (x - X1) / B1 * e1 + 2 * (x - X2) / B2 * e2,
            -2 * (y - Y1) / B1 * e1 + 2 * (y - Y2) / B2 * e2)


xs = PASO * np.arange(N)                 # columnas: x = 5 j
ys = PASO * (N - 1 - np.arange(N))       # filas: y = 100 - 5 i (fila 0 al norte)
XX, YY = np.meshgrid(xs, ys)
Z = h(XX, YY)

titulo("T  terreno")
print(f"loma: centro ({X1:.0f}, {Y1:.0f}), altura {A1}; hondonada: centro ({X2:.0f}, {Y2:.0f}), profundidad {A2}")
print("Z shape", Z.shape, " min %.2f  max %.2f" % (Z.min(), Z.max()))
print("esquina noroeste 3x3:\n", np.round(Z[:3, :3], 2))
assert (X1, Y1, X2, Y2, A1, A2) == (37.0, 41.0, 72.0, 71.0, 7.7, 3.3), (X1, Y1, X2, Y2, A1, A2)
cerca(Z.max(), 107.65, 0.005); cerca(Z.min(), 97.30, 0.005)
assert Z.min() > Z0


# ---------------------------------------------------------------- E1  pendiente y orientación
def gradiente_centrado(M, i, j, paso, k=1):
    """Diferencias centradas en el nodo (i, j) con salto de k nodos; y hacia el norte (fila 0 al norte)."""
    gx = (M[i, j + k] - M[i, j - k]) / (2 * k * paso)
    gy = (M[i - k, j] - M[i + k, j]) / (2 * k * paso)
    return gx, gy


def pend_orient(gx, gy):
    p = hypot(gx, gy)
    az = degrees(atan2(-gx, -gy)) % 360   # dirección de la bajada, desde el norte, horario
    return p, 100 * p, degrees(atan(p)), az


titulo("E1  pendiente en el nodo (10, 13)")
I0, J0 = 10, 13
x0, y0 = xs[J0], ys[I0]
print("nodo: x =", x0, " y =", y0, " h =", round(float(Z[I0, J0]), 2))
print("ventana 3x3:\n", np.round(Z[I0 - 1:I0 + 2, J0 - 1:J0 + 2], 2))
gx5, gy5 = gradiente_centrado(Z, I0, J0, PASO, 1)
gx10, gy10 = gradiente_centrado(Z, I0, J0, PASO, 2)
gxe, gye = grad_h(x0, y0)
p5, pc5, pg5, az5 = pend_orient(gx5, gy5)
pe, pce, pge, aze = pend_orient(gxe, gye)
p10, pc10, pg10, az10 = pend_orient(gx10, gy10)
print("centradas paso 5:  (%.4f, %.4f)  pend %.2f %%  %.2f°  Az %.1f°" % (gx5, gy5, pc5, pg5, az5))
print("centradas paso 10: (%.4f, %.4f)  pend %.2f %%  %.2f°  Az %.1f°" % (gx10, gy10, pc10, pg10, az10))
print("exacto:            (%.4f, %.4f)  pend %.2f %%  %.2f°  Az %.1f°" % (gxe, gye, pce, pge, aze))
err5 = hypot(gx5 - gxe, gy5 - gye); err10 = hypot(gx10 - gxe, gy10 - gye)
print("error |grad| paso 5: %.5f  paso 10: %.5f  razón %.2f" % (err5, err10, err10 / err5))
W = np.round(Z[I0 - 1:I0 + 2, J0 - 1:J0 + 2], 2)
assert (x0, y0) == (65.0, 50.0)
assert W.tolist() == [[102.66, 101.54, 100.65], [103.41, 102.33, 101.43], [103.84, 102.74, 101.82]], W.tolist()
cerca(gx5, -0.1988, 0.00005); cerca(gy5, -0.1201, 0.00005)
cerca(gxe, -0.2027, 0.00005); cerca(gye, -0.1186, 0.00005)
cerca(gx10, -0.1879, 0.00005); cerca(gy10, -0.1218, 0.00005); cerca(pc10, 22.39, 0.005); cerca(az10, 57.1, 0.05)
cerca(pc5, 23.22, 0.005); cerca(pce, 23.49, 0.005); cerca(pg5, 13.07, 0.005); cerca(pge, 13.22, 0.005)
cerca(az5, 58.9, 0.05); cerca(aze, 59.7, 0.05)
cerca(err10 / err5, 3.56, 0.005); cerca(err5, 0.00425, 0.000005); cerca(err10, 0.01515, 0.000005)
# la cuenta a mano con los números redondeados de la ventana
gx_m = (W[1, 2] - W[1, 0]) / 10; gy_m = (W[0, 1] - W[2, 1]) / 10
cerca(gx_m, -0.198, 1e-9); cerca(gy_m, -0.120, 1e-9)
pm, pcm, pgm, azm = pend_orient(gx_m, gy_m)
print("a mano: (%.3f, %.3f) pend %.2f %% %.2f° Az %.1f°" % (gx_m, gy_m, pcm, pgm, azm))
cerca(pcm, 23.15, 0.005); cerca(pgm, 13.04, 0.005); cerca(azm, 58.8, 0.05)


# ---------------------------------------------------------------- E2  volumen
def prismas(M, paso, z0):
    """Suma de prismas: cada celda, área paso^2 por el promedio de sus cuatro esquinas sobre z0."""
    medias = (M[:-1, :-1] + M[1:, :-1] + M[:-1, 1:] + M[1:, 1:]) / 4
    return paso ** 2 * float(np.sum(medias - z0))


def integral_gauss_1d(a, b, c, B):
    """∫_a^b exp(-(t-c)^2/B) dt."""
    s = sqrt(B)
    return sqrt(pi) * s / 2 * (erf((b - c) / s) - erf((a - c) / s))


def integral_exacta(xa, xb, ya, yb, z0):
    area = (xb - xa) * (yb - ya)
    return ((BASE - z0) * area
            + A1 * integral_gauss_1d(xa, xb, X1, B1) * integral_gauss_1d(ya, yb, Y1, B1)
            - A2 * integral_gauss_1d(xa, xb, X2, B2) * integral_gauss_1d(ya, yb, Y2, B2))


titulo("E2  volumen sobre el plano de 95 m")
ic, jc = 10, 8   # celda entre filas 10-11 y columnas 8-9
esq = np.round([Z[ic, jc], Z[ic, jc + 1], Z[ic + 1, jc + 1], Z[ic + 1, jc]], 2)
vcel = 25 * (esq.mean() - Z0)
print("celda esquinas (NO, NE, SE, SO):", esq, " media %.4f  volumen %.2f m3" % (esq.mean(), vcel))
V = prismas(Z, PASO, Z0)
Vex = integral_exacta(0, 100, 0, 100, Z0)
ingenua = 25 * float(np.sum(Z - Z0))
print("suma de 400 prismas: %.1f m3   integral exacta: %.1f m3   diferencia %.1f m3 (%.4f %%)" % (V, Vex, V - Vex, 100 * (V - Vex) / Vex))
print("ingenua 441 columnas: %.1f m3  (exceso %.1f m3, %.2f %%)" % (ingenua, ingenua - Vex, 100 * (ingenua - Vex) / Vex))
print("altura media sobre el plano: %.3f m" % (V / 1e4))
assert esq.tolist() == [106.88, 106.41, 106.96, 107.46], esq.tolist()
cerca(vcel, 298.19, 0.005)
cerca(V, 66218.9, 0.05); cerca(Vex, 66242.4, 0.05); cerca(V - Vex, -23.5, 0.05); cerca(V / 1e4, 6.622, 0.0005)
cerca(ingenua, 71641.0, 0.5); cerca(100 * (V - Vex) / Vex, -0.0355, 0.00005)
cerca(100 * (ingenua - Vex) / Vex, 8.15, 0.005)


# ---------------------------------------------------------------- A  aplicación
titulo("A  pendiente máxima en la cuadrícula de 5 m (nodos interiores)")
GX = (Z[1:-1, 2:] - Z[1:-1, :-2]) / (2 * PASO)
GY = (Z[:-2, 1:-1] - Z[2:, 1:-1]) / (2 * PASO)
P = 100 * np.hypot(GX, GY)
im, jm = np.unravel_index(np.argmax(P), P.shape)
print("pendiente máxima %.2f %% en fila %d, columna %d (x=%.0f, y=%.0f)" % (P.max(), im + 1, jm + 1, xs[jm + 1], ys[im + 1]))
PE = 100 * np.hypot(*grad_h(XX, YY))
print("pendiente máxima exacta sobre los nodos: %.2f %%" % PE.max())
pmax5 = float(P.max())
cerca(pmax5, 31.99, 0.005); cerca(float(PE.max()), 33.58, 0.005)
assert (im + 1, jm + 1) == (7, 12), (im + 1, jm + 1)
print("pendiente media (nodos interiores): %.2f %%" % P.mean())
cerca(P.mean(), 13.29, 0.005)

titulo("A  remuestreo a 10 m con origen (3, 3)")
xg = 3.0 + 10.0 * np.arange(10)
yg = 3.0 + 10.0 * np.arange(10)[::-1]   # fila 0 al norte
XG, YG = np.meshgrid(xg, yg)
VERDAD = h(XG, YG)


def a_indices(x, y):
    """Posición (fraccionaria) en la matriz Z: columna = x/5, fila = (100 - y)/5."""
    return (100.0 - y) / PASO, x / PASO


def vecino(M, x, y):
    fi, fj = a_indices(x, y)
    return M[np.rint(fi).astype(int), np.rint(fj).astype(int)]


def bilineal(M, x, y):
    fi, fj = a_indices(x, y)
    i0 = np.floor(fi).astype(int); j0 = np.floor(fj).astype(int)
    t = fi - i0; s = fj - j0
    return ((1 - s) * (1 - t) * M[i0, j0] + s * (1 - t) * M[i0, j0 + 1]
            + (1 - s) * t * M[i0 + 1, j0] + s * t * M[i0 + 1, j0 + 1])


ZV = vecino(Z, XG, YG)
ZB = bilineal(Z, XG, YG)
eV = ZV - VERDAD; eB = ZB - VERDAD
rmsV, rmsB = float(np.sqrt(np.mean(eV ** 2))), float(np.sqrt(np.mean(eB ** 2)))
maxV, maxB = float(np.abs(eV).max()), float(np.abs(eB).max())
print("vecino:   RMS %.3f m  máx %.3f m" % (rmsV, maxV))
print("bilineal: RMS %.3f m  máx %.3f m" % (rmsB, maxB))
VexG = integral_exacta(3, 93, 3, 93, Z0)
VV, VB = prismas(ZV, 10.0, Z0), prismas(ZB, 10.0, Z0)
VT = prismas(VERDAD, 10.0, Z0)
print("la misma cuadrícula de 10 m con alturas exactas: %.0f (%+.0f)" % (VT, VT - VexG))
print("volumen [3,93]^2 exacto %.0f  vecino %.0f (%+.0f, %+.2f %%)  bilineal %.0f (%+.0f, %+.2f %%)" % (
    VexG, VV, VV - VexG, 100 * (VV - VexG) / VexG, VB, VB - VexG, 100 * (VB - VexG) / VexG))
# pendiente máxima en la cuadrícula de 10 m (bilineal), diferencias centradas paso 10
GXg = (ZB[1:-1, 2:] - ZB[1:-1, :-2]) / 20
GYg = (ZB[:-2, 1:-1] - ZB[2:, 1:-1]) / 20
pmax10 = float(100 * np.hypot(GXg, GYg).max())
print("pendiente máxima en la de 10 m: %.2f %%" % pmax10)
# el corrimiento del vecino: 2 m al este y 2 m al norte en todos los nodos
fi, fj = a_indices(XG, YG)
dx = PASO * (np.rint(fj) - fj); dy = -PASO * (np.rint(fi) - fi)
assert np.allclose(dx, 2.0) and np.allclose(dy, 2.0)
cerca(rmsV, 0.319, 0.0005); cerca(maxV, 0.959, 0.0005)
cerca(rmsB, 0.039, 0.0005); cerca(maxB, 0.197, 0.0005)
cerca(VexG, 56317.0, 0.5)
cerca(VV, 55882.0, 0.5); cerca(VB, 56178.0, 0.5); cerca(VT, 56213.0, 0.5)
cerca(100 * (VV - VexG) / VexG, -0.77, 0.005); cerca(100 * (VB - VexG) / VexG, -0.25, 0.005)
cerca(pmax10, 26.70, 0.005)
cerca(round(VB) - round(VT), -35, 0); cerca(round(VV) - round(VT), -331, 0); cerca(100 * (VT - VexG) / VexG, -0.18, 0.005)
assert 8 <= rmsV / rmsB < 8.5; cerca(2 * sqrt(2), 2.83, 0.005); cerca(0.32 * 2 * sqrt(2), 0.9, 0.01)
cerca(23.5 / 66242.4, 3.55e-4, 0.005e-4)


# ---------------------------------------------------------------- X1  ejercicio 1
titulo("X1  planilla 3x3 cada 10 m")
Q = np.array([[104.0, 106.0, 109.0], [101.0, 103.0, 107.0], [99.0, 100.0, 104.0]])
qx, qy = gradiente_centrado(Q, 1, 1, 10.0)
q = pend_orient(qx, qy)
print("grad (%.2f, %.2f)  pend %.1f %%  %.1f°  Az %.0f°" % (qx, qy, q[1], q[2], q[3]))
assert (qx, qy) == (0.3, 0.3)
cerca(q[1], 42.4, 0.05); cerca(q[2], 23.0, 0.05); cerca(q[3], 225.0, 1e-9); cerca(q[0], 0.424, 0.0005)

# ---------------------------------------------------------------- X2  ejercicio 2
titulo("X2  volumen sobre 99 m")
medias_q = (Q[:-1, :-1] + Q[1:, :-1] + Q[:-1, 1:] + Q[1:, 1:]) / 4
vq = prismas(Q, 10.0, 99.0)
ing_q = 100 * float(np.sum(Q - 99.0))
print("medias de las celdas:", medias_q.tolist(), " volumen %.0f m3  ingenua %.0f m3" % (vq, ing_q))
pesos = np.array([[1, 2, 1], [2, 4, 2], [1, 2, 1]]) / 4
assert np.isclose(100 * np.sum(pesos * (Q - 99)), vq)
assert medias_q.tolist() == [[103.5, 106.25], [100.75, 103.5]]
assert vq == 1800.0 and ing_q == 4200.0

# ---------------------------------------------------------------- X3  ejercicio 3
titulo("X3  bilineal en la celda del recorte")
f00, f10, f11, f01 = 1496.0, 1504.0, 1508.0, 1498.0
fb = lambda s, t: f00 + (f10 - f00) * s + (f01 - f00) * t + (f00 - f10 + f11 - f01) * s * t
s3, t3 = 0.3, 0.6
print("bilineal(0,3; 0,6) = %.2f  vecino más próximo: (0,1) -> %.0f" % (fb(s3, t3), f01))
cerca(fb(s3, t3), 1499.96, 1e-9)
assert np.isclose(1500 - fb(s3, t3), 0.04) and np.isclose(fb(0.3, 0.6), 1496 + 2.4 + 1.2 + 0.36)
# integral de la bilineal en la celda = promedio de las esquinas
integ = f00 + (f10 - f00) / 2 + (f01 - f00) / 2 + (f00 - f10 + f11 - f01) / 4
print("integral en la celda %.1f  promedio de esquinas %.1f" % (integ, (f00 + f10 + f11 + f01) / 4))
assert integ == (f00 + f10 + f11 + f01) / 4 == 1501.5

# ---------------------------------------------------------------- X4  ejercicio 4
titulo("X4  sumar, duplicar, espejar")
for nombre, M, z0 in (("+10 m", Q + 10, 99.0), ("x2 sobre 99", 99 + 2 * (Q - 99), 99.0), ("espejo N-S", Q[::-1], 99.0)):
    g = gradiente_centrado(M, 1, 1, 10.0); r = pend_orient(*g)
    print("%-11s grad (%.2f, %.2f) pend %.1f %% Az %.0f°  volumen sobre 99 m: %.0f" % (nombre, g[0], g[1], r[1], r[3], prismas(M, 10.0, z0)))
assert prismas(Q + 10, 10.0, 99.0) == 1800.0 + 4 * 100 * 10 == 5800.0
assert prismas(Q[::-1], 10.0, 99.0) == 1800.0
Q2 = 99 + 2 * (Q - 99)
cerca(pend_orient(*gradiente_centrado(Q2, 1, 1, 10.0))[1], 84.9, 0.05)
assert pend_orient(*gradiente_centrado(Q2, 1, 1, 10.0))[3] == 225.0
assert pend_orient(*gradiente_centrado(Q[::-1], 1, 1, 10.0))[3] == 315.0
assert prismas(Q2, 10.0, 99.0) == 3600.0


# ---------------------------------------------------------------- U  consigna de la unidad 10
titulo("U  la loma de la unidad 10: h = 2 exp(-(u^2+v^2)/8) en (2, 1)")
hl = lambda u, v: 2 * np.exp(-(u ** 2 + v ** 2) / 8)
hu_ex, hv_ex = -2 / 4 * hl(2, 1), -1 / 4 * hl(2, 1)
hu_dc = (hl(2.25, 1) - hl(1.75, 1)) / 0.5
hv_dc = (hl(2, 1.25) - hl(2, 0.75)) / 0.5
print("h(2,1) = %.4f  h(2,25;1) = %.4f  h(1,75;1) = %.4f" % (hl(2, 1), hl(2.25, 1), hl(1.75, 1)))
print("h(2;1,25) = %.4f  h(2;0,75) = %.4f" % (hl(2, 1.25), hl(2, 0.75)))
print("exacto (%.4f, %.4f)  centradas paso 0,25 (%.4f, %.4f)" % (hu_ex, hv_ex, hu_dc, hv_dc))
cerca(hl(2, 1), 1.0705, 0.00005); cerca(hl(2.25, 1), 0.9374, 0.00005); cerca(hl(1.75, 1), 1.2036, 0.00005)
cerca(hu_ex, -0.5353, 0.00005); cerca(hv_ex, -0.2676, 0.00005)
assert (round(hu_ex, 3), round(hv_ex, 3)) == (-0.535, -0.268)
cerca(hu_dc, -0.5325, 0.00005); cerca((0.9374 - 1.2036) / 0.5, -0.5324, 1e-9)


# ---------------------------------------------------------------- figuras
def figuras():
    SALIDA.mkdir(parents=True, exist_ok=True)
    ext = [-2.5, 102.5, -2.5, 102.5]
    # 1. la planilla y el terreno
    fig = plt.figure(figsize=(10, 4.3))
    ax = fig.add_subplot(1, 2, 1)
    im_ = ax.imshow(Z, cmap="Greys", extent=ext, origin="upper")
    cs = ax.contour(XX, YY, Z, levels=np.arange(97, 108, 1.0), colors=TEAL, linewidths=0.8)
    ax.clabel(cs, fmt="%d", fontsize=7)
    ax.plot([X1], [Y1], "^", color=RUST); ax.plot([X2], [Y2], "v", color=RUST)
    ax.set_xlabel("x (m, hacia el este) · columna j = x/5")
    ax.set_ylabel("y (m, hacia el norte) · fila i = (100 - y)/5")
    ax.set_title("la matriz Z de 21 × 21 como imagen")
    fig.colorbar(im_, ax=ax, shrink=0.8, label="altura (m)")
    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    ax3.plot_surface(XX, YY, Z, cmap="Greys", edgecolor=TEAL, linewidth=0.3, alpha=0.9)
    xx = np.array([[0, 100], [0, 100]]); yy = np.array([[0, 0], [100, 100]])
    ax3.plot_surface(xx, yy, np.full((2, 2), Z0), color=GOLD, alpha=0.35)
    ax3.set_zlim(94, 109); ax3.view_init(elev=28, azim=-60)
    ax3.set_xlabel("x (m)"); ax3.set_ylabel("y (m)"); ax3.set_zlabel("altura (m)")
    ax3.set_title("el mismo terreno sobre el plano de 95 m")
    fig.savefig(SALIDA / "terreno_planilla.png", dpi=150, metadata=META, bbox_inches="tight"); plt.close(fig)

    # 2. pendiente y orientación
    fig, ax = plt.subplots(figsize=(6.2, 5))
    Pfull = np.full_like(Z, np.nan); Pfull[1:-1, 1:-1] = P
    im_ = ax.imshow(Pfull, cmap="Oranges", extent=ext, origin="upper", vmin=0)
    ax.contour(XX, YY, Z, levels=np.arange(97, 108, 1.0), colors=GRIS, linewidths=0.6)
    sl = (slice(1, -1, 2), slice(1, -1, 2))
    ax.quiver(XX[1:-1, 1:-1][sl], YY[1:-1, 1:-1][sl], -GX[sl], -GY[sl], color=TEAL, angles="xy", scale=2.2, width=0.004)
    ax.plot([x0], [y0], "o", ms=8, mfc="none", mec=RUST, mew=1.6)
    ax.annotate("nodo del ejemplo", (x0, y0), xytext=(x0 + 6, y0 - 12), color=RUST, fontsize=9,
                arrowprops=dict(arrowstyle="-", color=RUST))
    ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    ax.set_title("pendiente (por ciento) y hacia dónde baja el agua")
    fig.colorbar(im_, ax=ax, shrink=0.85, label="pendiente (por ciento)")
    fig.tight_layout(); fig.savefig(SALIDA / "terreno_pendiente.png", dpi=150, metadata=META); plt.close(fig)

    # 3. remuestreo
    fig, axs = plt.subplots(1, 2, figsize=(10, 4.4))
    lim = float(np.abs(eV).max())
    extg = [-2, 98, -2, 98]
    coma = lambda v: ("%.2f" % v).replace(".", ",")
    for ax, e, t in ((axs[0], eV, "vecino más próximo: RMS %s m, máx. %s m" % (coma(rmsV), coma(maxV))),
                     (axs[1], eB, "bilineal: RMS %s m, máx. %s m" % (coma(rmsB), coma(maxB)))):
        im_ = ax.imshow(e, cmap="RdBu_r", vmin=-lim, vmax=lim, extent=extg, origin="upper")
        ax.contour(XX, YY, Z, levels=np.arange(97, 108, 1.0), colors=GRIS, linewidths=0.5)
        ax.plot(XG.ravel(), YG.ravel(), ".", color="k", ms=2)
        ax.set_xlim(0, 100); ax.set_ylim(0, 100)
        ax.set_title(t, fontsize=10); ax.set_xlabel("x (m)"); ax.set_ylabel("y (m)")
    fig.colorbar(im_, ax=axs, shrink=0.85, label="altura remuestreada − altura de la fórmula (m)")
    fig.savefig(SALIDA / "terreno_remuestreo.png", dpi=150, metadata=META, bbox_inches="tight"); plt.close(fig)


# ---------------------------------------------------------------- pruebas (pytest las recoge si el archivo se copia a demostraciones/)
def test_diferencia_centrada_cuadratica():
    assert 3 < err10 / err5 < 4.5


def test_bilineal_exacta_en_nodos():
    assert np.allclose(bilineal(Z, XX[:-1, :-1], YY[:-1, :-1]), Z[:-1, :-1])


def test_prismas_exactos_para_bilineal():
    rng = np.random.default_rng(1)
    c = rng.normal(size=4)
    f = lambda s, t: c[0] + c[1] * s + c[2] * t + c[3] * s * t
    exacta = c[0] + c[1] / 2 + c[2] / 2 + c[3] / 4
    assert np.isclose((f(0, 0) + f(1, 0) + f(0, 1) + f(1, 1)) / 4, exacta)


if __name__ == "__main__":
    figuras()
    test_diferencia_centrada_cuadratica(); test_bilineal_exacta_en_nodos(); test_prismas_exactos_para_bilineal()
    print("\nfiguras en", SALIDA)
