using Javis
using LinearAlgebra
using Printf

# ==============================================================================
# Configuración y Parámetros
# ==============================================================================
WIDTH  = 1280
HEIGHT = 720
FPS    = 30

# Duración de cada fase en frames (cada fase ~ 50-60 frames a 30 fps ≈ 2 seg)
PHASE_FRAMES = 60
NUM_PHASES   = 6
TOTAL_FRAMES = NUM_PHASES * PHASE_FRAMES # 360 frames = 12 segundos

# Centros de referencia para los dos pentágonos
CENTER_LEFT  = Point(-300, 40)
CENTER_RIGHT = Point(300, 40)

# ------------------------------------------------------------------------------
# Definición de los vértices (en coordenadas locales centradas en (0,0))
# ------------------------------------------------------------------------------
# 1. Pentágono Regular (radio = 110 px)
R = 110.0
regular_vertices = [
    Point(R * cos(2π * i / 5 - π/2), R * sin(2π * i / 5 - π/2))
    for i in 0:4
]

# 2. Pentágono Irregular (5 vértices asimétricos pero claramente distinguibles)
irregular_vertices = [
    Point(0.0, -115.0),    # Vértice superior
    Point(125.0, -35.0),   # Vértice derecho superior
    Point(85.0, 110.0),    # Vértice derecho inferior
    Point(-70.0, 95.0),    # Vértice izquierdo inferior
    Point(-120.0, -15.0)   # Vértice izquierdo
]

# ------------------------------------------------------------------------------
# Función de interpolación suave (Smoothstep / Cosine Easing)
# ------------------------------------------------------------------------------
function smooth_progress(t::Float64)
    t = clamp(t, 0.0, 1.0)
    return 0.5 * (1.0 - cos(π * t))
end

# ------------------------------------------------------------------------------
# Función que calcula el estado de la transformación afín para cada frame:
# Retorna:
#   A: Matriz 2x2
#   b: Vector de traslación [bx, by]
#   nombre: Descripción de la transformación
#   formula: Representación matemática
# ------------------------------------------------------------------------------
function get_affine_state(frame::Int)
    phase = div(frame - 1, PHASE_FRAMES) + 1
    t_raw = mod(frame - 1, PHASE_FRAMES) / (PHASE_FRAMES - 1)
    t = smooth_progress(t_raw)

    I2 = [1.0 0.0; 0.0 1.0]

    if phase == 1
        # Fase 1: Identidad (Reposo y presentación)
        A = I2
        b = [0.0, 0.0]
        desc = "1. Estado Inicial (Identidad)"
        math_str = "T(x) = I · x + 0"

    elseif phase == 2
        # Fase 2: Traslación pura (b varía)
        # Desplazamiento hacia la derecha y arriba
        b_target = [0.0, -60.0]
        b = t * b_target
        A = I2
        desc = "2. Traslación Pura: b = [Δx, Δy]"
        math_str = @sprintf("T(x) = x + [%.1f, %.1f]", b[1], b[2])

    elseif phase == 3
        # Fase 3: Rotación (R(θ))
        # Rotación de 0 a 72° (2π/5 rad)
        θ = t * (2π / 5)
        A = [cos(θ) -sin(θ); sin(θ) cos(θ)]
        b = [0.0, 0.0]
        desc = "3. Rotación Pura: R(θ)"
        math_str = @sprintf("θ = %.1f° | Preserva distancias y ángulos", rad2deg(θ))

    elseif phase == 4
        # Fase 4: Escalamiento no uniforme (anisotrópico)
        # sx = 1.35, sy = 0.65
        sx = 1.0 + t * 0.35
        sy = 1.0 - t * 0.35
        A = [sx 0.0; 0.0 sy]
        b = [0.0, 0.0]
        desc = "4. Escalamiento No Uniforme: Diag(sx, sy)"
        math_str = @sprintf("sx = %.2f,  sy = %.2f (Deforma proporciones)", sx, sy)

    elseif phase == 5
        # Fase 5: Cizallamiento (Shear) horizontal
        # Inclinación k_x de 0 a 0.65
        kx = t * 0.65
        A = [1.0 kx; 0.0 1.0]
        b = [0.0, 0.0]
        desc = "5. Cizallamiento (Shear): Preserva paralelismo pero no ángulos"
        math_str = @sprintf("Matriz Shear: [1.0  %.2f; 0.0  1.0]", kx)

    else
        # Fase 6: Transformación Afín Compuesta Completa (Rotación + Escala + Shear + Traslación)
        # Matriz general arbitraria invertible
        θ = 0.4 * t
        R_mat = [cos(θ) -sin(θ); sin(θ) cos(θ)]
        S_mat = [1.0 + 0.2*t 0.4*t; 0.0 1.0 - 0.2*t]
        A = (1 - t) * I2 + t * (R_mat * S_mat)
        b = t * [30.0, -35.0]
        desc = "6. Transformación Afín General: A · x + b"
        math_str = "Transformación lineal combinada + desplazamiento"
    end

    return A, b, desc, math_str
end

# ------------------------------------------------------------------------------
# Aplicar transformación afín a una lista de puntos
# P_trans = A * [p.x, p.y] + b
# ------------------------------------------------------------------------------
function apply_affine(pts::Vector{Point}, A::Matrix{Float64}, b::Vector{Float64})
    transformed = Point[]
    for p in pts
        v = [p.x, p.y]
        v_new = A * v + b
        push!(transformed, Point(v_new[1], v_new[2]))
    end
    return transformed
end

# ==============================================================================
# Funciones de Dibujo en Luxor / Javis
# ==============================================================================

function draw_background(args...)
    # Fondo degradado o color oscuro moderno
    background("#0d1117")

    # Rejilla sutil de fondo
    sethue("#161b22")
    setline(1)
    for x in -640:80:640
        line(Point(x, -360), Point(x, 360), :stroke)
    end
    for y in -360:80:360
        line(Point(-640, y), Point(640, y), :stroke)
    end
end

function draw_ui(video, object, frame)
    A, b, desc, math_str = get_affine_state(frame)

    # Título principal
    sethue("#58a6ff")
    fontsize(26)
    fontface("Helvetica-Bold")
    text("Transformaciones Afines en 2D:  T(x) = A · x + b", Point(0, -315), halign=:center)

    # Subtítulo con la fase actual
    sethue("#f0883e")
    fontsize(20)
    fontface("Helvetica-Bold")
    text(desc, Point(0, -275), halign=:center)

    # Fórmula / Parámetros matemáticos
    sethue("#8b949e")
    fontsize(15)
    fontface("Courier-Bold")
    text(math_str, Point(0, -245), halign=:center)

    # Matriz A y vector b numéricos en pantalla
    mat_text = @sprintf("[ %+.2f  %+.2f ]          [ %+.1f ]\nA = [               ]    b = [        ]\n  [ %+.2f  %+.2f ]          [ %+.1f ]",
        A[1,1], A[1,2], b[1],
        A[2,1], A[2,2], b[2]
    )
    sethue("#79c0ff")
    fontsize(14)
    fontface("Courier")
    text(mat_text, Point(0, 280), halign=:center)

    # Separador sutil vertical entre ambas figuras
    sethue("#21262d")
    setline(1.5)
    line(Point(0, -210), Point(0, 230), :stroke)
end

function draw_pentagon_scene(video, object, frame)
    A, b, _, _ = get_affine_state(frame)

    # ==========================
    # 1. PENTÁGONO REGULAR (IZQ)
    # ==========================
    @layer begin
        translate(CENTER_LEFT)

        # Ejes coordenados locales
        sethue("#30363d")
        setline(1)
        line(Point(-150, 0), Point(150, 0), :stroke)
        line(Point(0, -150), Point(0, 150), :stroke)

        # Etiqueta
        sethue("#7ee787")
        fontsize(17)
        fontface("Helvetica-Bold")
        text("Pentágono Regular", Point(0, -165), halign=:center)

        # Forma original "fantasma" (línea discontinua)
        sethue("#38444d")
        setline(1.5)
        setdash("dashed")
        poly(regular_vertices, :stroke, close=true)
        setdash("solid")

        # Pentágono transformado
        reg_trans = apply_affine(regular_vertices, A, b)

        # Relleno semi-transparente
        sethue("#1f6feb")
        # Luxor color transparente
        setcolor(0.12, 0.43, 0.92, 0.25)
        poly(reg_trans, :fill, close=true)

        # Borde brillante
        sethue("#58a6ff")
        setline(3)
        poly(reg_trans, :stroke, close=true)

        # Vértices (puntos resaltados)
        for (i, p) in enumerate(reg_trans)
            sethue("#ffffff")
            circle(p, 4.5, :fill)
            sethue("#1f6feb")
            circle(p, 2.5, :fill)
        end
    end

    # ============================
    # 2. PENTÁGONO IRREGULAR (DER)
    # ============================
    @layer begin
        translate(CENTER_RIGHT)

        # Ejes coordenados locales
        sethue("#30363d")
        setline(1)
        line(Point(-150, 0), Point(150, 0), :stroke)
        line(Point(0, -150), Point(0, 150), :stroke)

        # Etiqueta
        sethue("#ffa657")
        fontsize(17)
        fontface("Helvetica-Bold")
        text("Pentágono Irregular", Point(0, -165), halign=:center)

        # Forma original "fantasma" (línea discontinua)
        sethue("#38444d")
        setline(1.5)
        setdash("dashed")
        poly(irregular_vertices, :stroke, close=true)
        setdash("solid")

        # Pentágono transformado
        irreg_trans = apply_affine(irregular_vertices, A, b)

        # Relleno semi-transparente
        setcolor(0.85, 0.40, 0.10, 0.25)
        poly(irreg_trans, :fill, close=true)

        # Borde brillante
        sethue("#ff7b72")
        setline(3)
        poly(irreg_trans, :stroke, close=true)

        # Vértices (puntos resaltados)
        for (i, p) in enumerate(irreg_trans)
            sethue("#ffffff")
            circle(p, 4.5, :fill)
            sethue("#ff7b72")
            circle(p, 2.5, :fill)
        end
    end
end

# ==============================================================================
# Definición del Video y Renderizado
# ==============================================================================
video = Video(WIDTH, HEIGHT)

Background(1:TOTAL_FRAMES, draw_background)
Object(1:TOTAL_FRAMES, draw_ui)
Object(1:TOTAL_FRAMES, draw_pentagon_scene)

output_file = "transformaciones_afines.gif"
println("Generando animación en: ", output_file, " (", TOTAL_FRAMES, " frames)...")

render(
    video;
    pathname = output_file,
    framerate = FPS
)

println("¡Animación generada con éxito en: ", output_file, "!")
