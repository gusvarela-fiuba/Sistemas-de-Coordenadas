"""Comprobaciones del capítulo 2: traslaciones y movimientos rígidos.

Cada función `test_<etiqueta>` corresponde a un resultado del capítulo; ver README.md.
"""
import numpy as np
import sympy as sp

TOL = 1e-9


def rot(t):
    """Matriz de rotación R(t) (numérica)."""
    return np.array([[np.cos(t), -np.sin(t)], [np.sin(t), np.cos(t)]])


def R(t):
    """Matriz de rotación R(t) (simbólica)."""
    return sp.Matrix([[sp.cos(t), -sp.sin(t)], [sp.sin(t), sp.cos(t)]])


def S(d):
    """Matriz de la reflexión respecto de una recta de dirección d (simbólica)."""
    return sp.Matrix([[sp.cos(2 * d), sp.sin(2 * d)], [sp.sin(2 * d), -sp.cos(2 * d)]])


def es_cero(M):
    return all(sp.simplify(sp.expand_trig(e)) == 0 for e in M)


def test_prop_puntos_fijos(rng):
    """prop:puntos-fijos
    NUMERICA
    F(x) = R(t)x + w con t no nulo: det(I - R) = 2 - 2 cos t y c' = (I - R)^(-1) w es fijo.
    """
    CASOS = 200
    # >>> fragmento
    for _ in range(CASOS):
        t = rng.uniform(0.1, 2 * np.pi - 0.1)        # t lejos de 0 (mod 2 pi)
        w = rng.normal(size=2)
        A = np.eye(2) - rot(t)
        assert np.isclose(np.linalg.det(A), 2 - 2 * np.cos(t), atol=TOL)
        c = np.linalg.solve(A, w)                    # único, porque det(A) > 0
        assert np.allclose(rot(t) @ c + w, c, atol=TOL)
    # <<< fragmento


def test_prop_dos_reflexiones():
    """prop:dos-reflexiones
    SIMBOLICA
    S(d2) S(d1) = R(2(d2 - d1)) para ángulos simbólicos d1, d2; con d2 = d1 da la identidad.
    """
    # >>> fragmento
    d1, d2 = sp.symbols("delta1 delta2", real=True)
    producto = S(d2) * S(d1)
    assert es_cero(producto - R(2 * (d2 - d1)))
    assert es_cero(producto.subs(d2, d1) - sp.eye(2))   # rectas paralelas
    # <<< fragmento


def test_teo_clasificacion_rigidos():
    """teo:clasificacion-rigidos
    SIMBOLICA
    Con c = (I - R)^(-1) v, R(t)x + v = c + R(t)(x - c) para t, v y x simbólicos.
    """
    t = sp.symbols("theta", real=True)
    v = sp.Matrix(sp.symbols("v1 v2", real=True))
    x = sp.Matrix(sp.symbols("x1 y1", real=True))
    # >>> fragmento
    A = sp.eye(2) - R(t)
    assert sp.simplify(A.det() - (2 - 2 * sp.cos(t))) == 0   # invertible si t no es 0
    c = A.inv() * v                                          # el punto fijo
    F = R(t) * x + v
    assert es_cero(F - (c + R(t) * (x - c)))   # rotación de centro c
    # <<< fragmento
