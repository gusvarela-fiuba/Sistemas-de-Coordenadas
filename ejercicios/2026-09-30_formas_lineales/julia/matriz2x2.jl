# matriz2x2.jl — adjunta, determinante e inversa de una matriz 2x2
#
# Para A = [a b; c d]:
#   det(A)  = a*d - b*c
#   cof(A)  = [ d -c; -b a ]        (matriz de cofactores)
#   adj(A)  = cof(A)'  = [ d -b; -c a ]   (adjunta = traspuesta de los cofactores)
#   inv(A)  = adj(A) / det(A)       (solo si det(A) != 0)

using LinearAlgebra   # solo para verificar contra inv() y det() de la librería
using Plots           # para la grilla de rectas paralelas (sección final)

"Matriz de cofactores de una 2x2."
function cofactores2x2(A)
    a, b = A[1,1], A[1,2]
    c, d = A[2,1], A[2,2]
    return [ d  -c;
            -b   a ]
end

"Adjunta (adjugada) de una 2x2: traspuesta de la matriz de cofactores."
adjunta2x2(A) = transpose(cofactores2x2(A))

"Determinante de una 2x2 por la regla a*d - b*c."
determinante2x2(A) = A[1,1]*A[2,2] - A[1,2]*A[2,1]

"Inversa de una 2x2 vía adj(A)/det(A). Devuelve `nothing` si es singular."
function inversa2x2(A)
    Δ = determinante2x2(A)
    if Δ == 0
        return nothing
    end
    return adjunta2x2(A) ./ Δ
end

function mostrar(A)
    println("A =")
    display(A)
    Δ = determinante2x2(A)
    println("\ndet(A) = $(A[1,1])·$(A[2,2]) − $(A[1,2])·$(A[2,1]) = $Δ")
    println("\nCofactores de A =")
    display(cofactores2x2(A))
    println("\nadj(A) = cofactores' =")
    display(adjunta2x2(A))
    Ainv = inversa2x2(A)
    if Ainv === nothing
        println("\nA es singular (det = 0): no tiene inversa.")
    else
        println("\ninv(A) = adj(A) / det(A) =")
        display(Ainv)
        println("\nVerificación A · inv(A) =")
        display(A * Ainv)
        println("\n¿Coincide con LinearAlgebra.inv? ", isapprox(Ainv, inv(A)))
    end
    println()
end

# --- Programa principal ---
A = [ 1.2  0.5;
     -0.1  1.3 ]

mostrar(A)

# --- Gráfico: rectas paralelas a u y v, antes y después de multiplicar por inv(A) ---
#
# Idea geométrica: la recta paralela a u que pasa por P es  r(t) = P + t·u.
# Tomando P_k = k·v (múltiplos del OTRO vector) las paralelas a u quedan igualmente
# espaciadas y, junto con las paralelas a v que pasan por k·u, forman la grilla
# oblicua de la base {u, v}. Cada nodo es un punto a·u + b·v con a, b enteros.
#
# Como inv(A) es lineal, manda rectas en rectas y paralelas en paralelas: la grilla
# de {u, v} se transforma en la grilla de {inv(A)·u, inv(A)·v}. Cambia el ángulo
# entre las familias y el espaciado, pero no la estructura de grilla. El área de
# cada paralelogramo se multiplica por det(inv(A)) = 1/det(A).

gr()

u = [ 1.0, 1.0]
v = [-1.0, 2.0]

k_max = 4                          # rectas a cada lado del origen
t     = range(-20, 20; length = 2) # parámetro: bastan 2 puntos por recta (rango amplio para que crucen todo el cuadro)

fmt(w) = "[" * join(round.(w; digits = 3), ", ") * "]"

"Dibuja en `plt` la grilla oblicua de la base {u, v}: paralelas a u por k·v, paralelas a v por k·u."
function grilla!(plt, u, v; nombre_u = "u", nombre_v = "v")
    # Rectas paralelas a u:  r_k(t) = k·v + t·u
    for k in -k_max:k_max
        plot!(plt, [k*v[1] + s*u[1] for s in t], [k*v[2] + s*u[2] for s in t];
              color = :steelblue, lw = (k == 0 ? 2.5 : 1), alpha = (k == 0 ? 1 : 0.6),
              label = (k == 0 ? "paralelas a $nombre_u" : ""))
    end
    # Rectas paralelas a v:  s_k(t) = k·u + t·v
    for k in -k_max:k_max
        plot!(plt, [k*u[1] + s*v[1] for s in t], [k*u[2] + s*v[2] for s in t];
              color = :firebrick, lw = (k == 0 ? 2.5 : 1), alpha = (k == 0 ? 1 : 0.6),
              label = (k == 0 ? "paralelas a $nombre_v" : ""))
    end
    # Vectores desde el origen
    plot!(plt, [0, u[1]], [0, u[2]]; arrow = true, color = :navy,    lw = 3, label = "$nombre_u = $(fmt(u))")
    plot!(plt, [0, v[1]], [0, v[2]]; arrow = true, color = :darkred, lw = 3, label = "$nombre_v = $(fmt(v))")
    # Nodos a·u + b·v
    nodos = [a*u + b*v for a in -k_max:k_max, b in -k_max:k_max]
    scatter!(plt, first.(nodos), last.(nodos); ms = 2.5, color = :black, label = "")
    return plt
end

ejes(tit) = plot(; aspect_ratio = :equal, xlims = (-8, 8), ylims = (-8, 8),
                   framestyle = :origin, legend = :topleft, legendfontsize = 8, title = tit)

Ainv = inversa2x2(A)
if Ainv === nothing
    println("A es singular: no se puede graficar la grilla transformada por inv(A).")
else
    u2 = Ainv * u
    v2 = Ainv * v
    println("inv(A)·u = ", fmt(u2))
    println("inv(A)·v = ", fmt(v2))

    p1 = grilla!(ejes("Base {u, v}"), u, v)
    p2 = grilla!(ejes("Base {inv(A)·u, inv(A)·v}"), u2, v2; nombre_u = "inv(A)·u", nombre_v = "inv(A)·v")
    plt = plot(p1, p2; layout = (1, 2), size = (1400, 700))

    salida = joinpath(@__DIR__, "matriz2x2_rectas.png")
    savefig(plt, salida)
    println("Gráfico guardado en ", salida)
    display(plt)
end
