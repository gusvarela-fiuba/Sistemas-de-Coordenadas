"""Configuración común de las comprobaciones del apunte (pytest).

`rng`: generador de números aleatorios con semilla fija, el mismo en cada prueba, para que
toda comprobación NUMERICA sea reproducible caso por caso.
"""
import numpy as np
import pytest

SEMILLA = 104


@pytest.fixture
def rng():
    return np.random.default_rng(SEMILLA)
