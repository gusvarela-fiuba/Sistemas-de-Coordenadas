using Plots
gr()

println("="^70)
println(" Visualización 3D en Julia: Intersección de Superficies y Recta Tangente")
println("="^70)

# ==============================================================================
# 1. Definición Matemática del Problema
# ==============================================================================
# - Superficie S1: Paraboloide circular z = 1 - (x^2 + y^2)
# - Superficie S2: Plano secante vertical x + y = 1  =>  y = 1 - x
# - Curva C: r(t) = (t, 1 - t, 2t - 2t^2)
# - Plano π: x - z = 0  =>  z = x  (vector normal n = (1, 0, -1))
# - Punto solución P: (1/4, 3/4, 3/8)
# - Vector tangente T: r'(1/4) = (1, -1, 1)  =>  T · n = 1(1) + (-1)(0) + 1(-1) = 0

# Punto solución P
P = [0.25, 0.75, 0.375]
T = [1.0, -1.0, 1.0]

# Rango de parámetros para la curva C
t_vals = range(-0.25, 1.25, length=150)
x_curve = t_vals
y_curve = 1.0 .- t_vals
z_curve = 2.0 .* t_vals .- 2.0 .* (t_vals .^ 2)

# Rango para la recta tangente en P
s_vals = range(-0.55, 0.55, length=100)
x_tan = P[1] .+ s_vals .* T[1]
y_tan = P[2] .+ s_vals .* T[2]
z_tan = P[3] .+ s_vals .* T[3]

# Malla para el paraboloide z = 1 - (x^2 + y^2)
x_parab = range(-1.15, 1.15, length=35)
y_parab = range(-1.15, 1.15, length=35)
f_parab(x, y) = 1.0 - (x^2 + y^2)

# Malla para el plano de referencia x - z = 0  =>  z(x, y) = x
x_ref = range(-0.4, 1.2, length=15)
y_ref = range(-0.4, 1.4, length=15)
f_ref(x, y) = x

# ==============================================================================
# 2. Función auxiliar para construir el gráfico 3D
# ==============================================================================
function construir_grafico_3d(azim=45, elev=22)
    # 1. Paraboloide S1
    p3d = surface(
        x_parab, y_parab, f_parab,
        color=:blues, alpha=0.35, colorbar=false,
        camera=(azim, elev),
        title="Perspectiva 3D: Curva C, Recta Tangente y Planos",
        xlabel="X", ylabel="Y", zlabel="Z",
        xlims=(-0.8, 1.5), ylims=(-0.6, 1.5), zlims=(-0.6, 1.2),
        legend=:topright,
        label=""
    )

    # 2. Plano de referencia π: x - z = 0 (z = x)
    surface!(
        p3d, x_ref, y_ref, f_ref,
        color=:purple, alpha=0.22, colorbar=false,
        label="Plano ref: x - z = 0"
    )

    # 3. Plano secante vertical S2: x + y = 1 (malla de líneas)
    for zv in range(-0.5, 1.1, length=7)
        plot3d!(p3d, [-0.4, 1.4], [1.4, -0.4], [zv, zv], color=:orange, lw=1.2, alpha=0.6, label="")
    end
    for xv in range(-0.4, 1.4, length=7)
        plot3d!(p3d, [xv, xv], [1.0 - xv, 1.0 - xv], [-0.5, 1.1], color=:orange, lw=1.2, alpha=0.6, label="")
    end

    # 4. Curva de intersección C
    plot3d!(p3d, x_curve, y_curve, z_curve, color=:red, lw=3.5, label="Curva C = S1 ∩ S2")

    # 5. Recta tangente a C en P
    plot3d!(p3d, x_tan, y_tan, z_tan, color=:forestgreen, lw=3, linestyle=:dash, label="Recta Tangente T=(1,-1,1)")

    # 6. Punto P
    scatter3d!(p3d, [P[1]], [P[2]], [P[3]], color=:black, markersize=5.5, label="P(1/4, 3/4, 3/8)")

    return p3d
end

# ==============================================================================
# 3. Vista 2D de perfil (Ejes X-Z) para comprobación analítica visual
# ==============================================================================
function construir_grafico_perfil_xz()
    x_line = range(-0.2, 1.2, length=100)
    z_ref_line = x_line # z = x (pendiente 1)

    p2d = plot(
        x_line, z_ref_line,
        color=:purple, lw=2.5,
        label="Plano ref: z = x (m = 1)",
        xlabel="Eje X", ylabel="Eje Z",
        title="Vista de perfil (X-Z): Paralelismo evidente",
        legend=:bottomright,
        aspect_ratio=:equal,
        xlims=(-0.2, 1.2), ylims=(-0.2, 1.0)
    )

    # Recta tangente proyectada: dz/dx = 1/1 = 1
    plot!(p2d, x_tan, z_tan, color=:forestgreen, lw=3, linestyle=:dash, label="Recta Tangente (m = 1)")

    # Curva C proyectada en XZ: z = 2x - 2x^2
    plot!(p2d, x_curve, z_curve, color=:red, lw=2, label="Curva C: z = 2x - 2x²")

    # Punto P proyectado
    scatter!(p2d, [P[1]], [P[3]], color=:black, markersize=6, label="P(1/4, 3/8)")

    # Anotación explicativa
    annotate!(p2d, P[1] + 0.28, P[3] + 0.18, text("P(1/4, 3/8)\nTangente || a (z = x)", 10, :black))

    return p2d
end

# ==============================================================================
# 4. Generación y Guardado de Resultados
# ==============================================================================
println("-> Generando figura estática comparativa (3D + 2D Perfil)...")
p_3d = construir_grafico_3d(45, 22)
p_2d = construir_grafico_perfil_xz()
p_final = plot(p_3d, p_2d, layout=(1, 2), size=(1300, 600))

png_path = "ilustracion_3d_julia.png"
savefig(p_final, png_path)
println("   ✓ Imagen guardada en: $png_path")

println("-> Generando animación rotatoria 3D de 360° en Julia...")
anim = @animate for azim in 0:4:356
    construir_grafico_3d(azim, 24)
end
gif_path = "ilustracion_3d_rotacion.gif"
gif(anim, gif_path, fps=20)
println("   ✓ Animación 3D guardada en: $gif_path")

println("="^70)
println(" Proceso finalizado con éxito.")
println("="^70)
