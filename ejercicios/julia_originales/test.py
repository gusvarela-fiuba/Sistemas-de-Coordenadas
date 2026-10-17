# test.py — port fiel de test.jl (sistema 3x3, autovalores, LU, inversa, determinante, normas)
# con numpy/scipy. Misma salida de texto que `julia test.jl`.
#
# Correr desde esta carpeta:  uv run python test.py

import numpy as np
from scipy.linalg import lu


# Impresión al estilo Julia: vectores "[a, b, c]" y matrices "[a b c; d e f; ...]"
def jl_vec(v):
    return "[" + ", ".join(repr(float(x)) for x in v) + "]"


def jl_mat(M):
    return "[" + "; ".join(" ".join(repr(float(x)) for x in fila) for fila in M) + "]"


# Definir una matriz 3x3
A = np.array([[4.0, 2.0, 1.0],
              [2.0, 5.0, 3.0],
              [1.0, 3.0, 6.0]])

# Sistema de ecuaciones: Ax = b
b = np.array([7.0, 10.0, 10.0])

# Resolver el sistema
x = np.linalg.solve(A, b)
print("Solución del sistema: ", jl_vec(x), sep="")

# Autovalores y autovectores (A es simétrica: Julia usa la rutina simétrica, acá eigh)
vals, vecs = np.linalg.eigh(A)
print("\nAutovalores: ", jl_vec(vals), sep="")

# Descomposición LU (con pivoteo parcial: A = P L U)
P, L, U = lu(A)
print("\nMatriz L:\n", jl_mat(L), sep="")
print("\nMatriz U:\n", jl_mat(U), sep="")

# Inversa y determinante
print("\nDeterminante: ", repr(float(np.linalg.det(A))), sep="")
print("\nInversa:\n", jl_mat(np.linalg.inv(A)), sep="")

# Normas
print("\nNorma Frobenius: ", repr(float(np.linalg.norm(A))), sep="")
print("Número de condición: ", repr(float(np.linalg.cond(A))), sep="")
