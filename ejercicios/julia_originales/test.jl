using LinearAlgebra

# Definir una matriz 3x3
A = [4.0 2.0 1.0;
     2.0 5.0 3.0;
     1.0 3.0 6.0]

# Sistema de ecuaciones: Ax = b
b = [7.0, 10.0, 10.0]

# Resolver el sistema
x = A \ b
println("Solución del sistema: ", x)

# Autovalores y autovectores
vals, vecs = eigen(A)
println("\nAutovalores: ", vals)

# Descomposición LU
F = lu(A)
println("\nMatriz L:\n", F.L)
println("\nMatriz U:\n", F.U)

# Inversa y determinante
println("\nDeterminante: ", det(A))
println("\nInversa:\n", inv(A))

# Normas
println("\nNorma Frobenius: ", norm(A))
println("Número de condición: ", cond(A))