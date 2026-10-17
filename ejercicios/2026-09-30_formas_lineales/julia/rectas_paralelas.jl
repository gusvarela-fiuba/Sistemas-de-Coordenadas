# rectas_paralelas.jl — familias de rectas paralelas a u = [1, 1] y v = [-1, 2],
# y las mismas familias después de multiplicar por inv(A), con A la de matriz2x2.jl.
#
# Idea geométrica: la recta paralela a u que pasa por P es  r(t) = P + t·u.
# Tomando P_k = k·v (múltiplos del OTRO vector) las paralelas a u quedan igualmente
# espaciadas y, junto con las paralelas a v que pasan por k·u, forman la grilla
# oblicua de la base {u, v}. Cada nodo es un punto a·u + b·v con a, b enteros.
#
# Como inv(A) es lineal, manda rectas en rectas y paralelas en paralelas: la grilla
# de {u, v} se transforma en la grilla de {inv(A)·u, inv(A)·v}. Cambia el ángulo
# entre las familias y el espaciado, pero no la estructura de grilla.

using Plots
gr()

A = [ 1.2  0.5;
     -0.1  1.3 ]
Ainv = [A[2,2] -A[1,2]; -A[2,1] A[1,1]] ./ (A[1,1]*A[2,2] - A[1,2]*A[2,1])   # adj(A)/det(A)

u = [ 1.0, 1.0]
v = [-1.0, 2.0]
u2 = Ainv * u          # ≈ [0.497, 0.807]
v2 = Ainv * v          # ≈ [-1.429, 1.429]

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

p1 = grilla!(ejes("Base {u, v}"), u, v)
p2 = grilla!(ejes("Base {inv(A)·u, inv(A)·v}"), u2, v2; nombre_u = "inv(A)·u", nombre_v = "inv(A)·v")

plt = plot(p1, p2; layout = (1, 2), size = (1400, 700))

salida = joinpath(@__DIR__, "rectas_paralelas.png")
savefig(plt, salida)
println("Guardado en ", salida)
display(plt)
