"""Comprobaciones del capítulo 6: subespacios, cuña y determinante.

Cada función `test_<etiqueta>` corresponde a un resultado del capítulo; ver README.md.
"""
import itertools

import numpy as np
import sympy as sp
from scipy.spatial import ConvexHull

TOL = 1e-9


def area_con_signo(P):
    """Fórmula del agrimensor: (1/2) suma de p_i cuña p_(i+1), vértices en las filas de P."""
    Q = np.roll(P, -1, axis=0)
    return 0.5 * np.sum(P[:, 0] * Q[:, 1] - Q[:, 0] * P[:, 1])


def poligono_estrellado(rng, n):
    """Polígono simple, recorrido antihorario: n vértices con ángulos crecientes alrededor de un
    centro al azar y saltos de ángulo menores que pi (el centro ve todo el polígono)."""
    saltos = rng.uniform(0.6, 1.0, n)
    ang = rng.uniform(0, 2 * np.pi) + np.cumsum(2 * np.pi * saltos / saltos.sum())
    r = rng.uniform(0.5, 2.0, n)
    return rng.normal(size=2) + np.column_stack([r * np.cos(ang), r * np.sin(ang)])


def volumen_paralelepipedo(B):
    """Volumen geométrico (sin determinantes) del paralelepípedo de aristas las columnas de B:
    cápsula convexa de sus 8 vértices, sumas de subconjuntos de las aristas."""
    vertices = np.array([B @ np.array(e) for e in itertools.product((0, 1), repeat=3)])
    return ConvexHull(vertices).volume


def test_prop_det_factor(rng):
    """prop:det-factor
    NUMERICA
    Área con signo de M(P) = det M por área con signo de P (polígonos al azar); en R^3, volumen del paralelepípedo = |det[u v w]| y vol(M·paralelepípedo) = |det M|·vol.
    """
    CASOS = 200
    # >>> fragmento
    for _ in range(CASOS):
        M = rng.normal(size=(2, 2))
        P = poligono_estrellado(rng, rng.integers(3, 12))   # región: polígono simple
        assert np.isclose(area_con_signo(P @ M.T), np.linalg.det(M) * area_con_signo(P), atol=TOL)
        M3, B = rng.normal(size=(3, 3)), rng.normal(size=(3, 3))   # columnas de B: u, v, w
        V, VM = volumen_paralelepipedo(B), volumen_paralelepipedo(M3 @ B)   # cápsula convexa
        assert np.isclose(V, abs(np.linalg.det(B)), rtol=1e-7)
        assert np.isclose(VM, abs(np.linalg.det(M3)) * V, rtol=1e-7)
    # <<< fragmento


def test_prop_det_producto():
    """prop:det-producto
    SIMBOLICA
    det(AB) = det A det B para matrices genéricas de 2x2 y de 3x3 con entradas simbólicas.
    """
    # >>> fragmento
    for n in (2, 3):
        A = sp.Matrix(n, n, sp.symbols(f"a:{n * n}"))
        B = sp.Matrix(n, n, sp.symbols(f"b:{n * n}"))
        assert sp.expand((A * B).det() - A.det() * B.det()) == 0
    # <<< fragmento


def test_prop_area_poligono(rng):
    """prop:area-poligono
    NUMERICA
    La fórmula del agrimensor no cambia al trasladar el origen ni al rotar; cambia de signo al invertir el recorrido.
    """
    CASOS = 200
    # >>> fragmento
    for _ in range(CASOS):
        P = poligono_estrellado(rng, rng.integers(3, 12))   # recorrido antihorario
        S, c, t = area_con_signo(P), rng.normal(size=2), rng.uniform(0, 2 * np.pi)
        Rt = np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])
        assert S > 0 and np.isclose(area_con_signo(P[::-1]), -S, atol=TOL)
        assert np.isclose(area_con_signo(P - c), S, atol=TOL)
        assert np.isclose(area_con_signo(P @ Rt.T), S, atol=TOL)
    # <<< fragmento
