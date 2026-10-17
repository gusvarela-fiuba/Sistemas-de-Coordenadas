using Javis
using LinearAlgebra
using Printf

# ==============================================================================
# Configuración y Parámetros
# ==============================================================================
WIDTH  = 1280
HEIGHT = 720
FPS    = 30

# Duración de cada fase en frames (60 frames a 30 fps = 2 segundos por fase)
PHASE_FRAMES = 50
NUM_PHASES   = 6
TOTAL_FRAMES = NUM_PHASES * PHASE_FRAMES # 300 frames = 10 segundos

# Centros en la pantalla (2D) para ubicar los dos objetos
CENTER_LEFT  = Point(-300, 40)
CENTER_RIGHT = Point(300, 40)

# Parámetros de la cámara de perspectiva
D_CAMERA = 600.0  # Distancia focal / distancia de la cámara al origen

# ------------------------------------------------------------------------------
# Definición de Geometría 3D (Vértices en R³)
# ------------------------------------------------------------------------------
# 1. Pentágono Regular 2D inmerso en 3D (plano XY, Z = 0)
R = 120.0
regular_pentagon_3d = [
    [R * cos(2π * i / 5 - π/2), R * sin(2π * i / 5 - π/2), 0.0]
    for i in 0:4
]

# 2. Prisma Pentagonal 3D (Base inferior en Z = -H/2, Base superior en Z = +H/2)
H = 90.0 # Altura de extrusión
prism_bottom = [
    [R * cos(2π * i / 5 - π/2), R * sin(2π * i / 5 - π/2), -H / 2]
    for i in 0:4
]
prism_top = [
    [R * cos(2π * i / 5 - π/2), R * sin(2π * i / 5 - π/2), H / 2]
    for i in 0:4
]

# Caras del prisma pentagonal (índices de vértices):
# Base inferior (1:5), Base superior (6:10), y 5 caras laterales (cuadriláteros)
prism_vertices_all = vcat(prism_bottom, prism_top)

struct Face3D
    indices::Vector{Int}
    base_color::NTuple{3, Float64} # RGB (0 a 1)
end

prism_faces = Face3D[
    # Base inferior (Z = -H/2)
    Face3D([5, 4, 3, 2, 1], (0.15, 0.45, 0.85)),
    # Base superior (Z = +H/2)
    Face3D([6, 7, 8, 9, 10], (0.25, 0.65, 1.0)),
    # 5 caras laterales rectangulares
    Face3D([1, 2, 7, 6], (0.95, 0.55, 0.20)),
    Face3D([2, 3, 8, 7], (0.90, 0.45, 0.25)),
    Face3D([3, 4, 9, 8], (0.85, 0.35, 0.30)),
    Face3D([4, 5, 10, 9], (0.80, 0.40, 0.40)),
    Face3D([5, 1, 6, 10], (0.90, 0.50, 0.30))
]

# Vector de luz direccional (iluminación tipo Phong / Lambertiana)
LIGHT_DIR = normalize([0.5, -0.7, 1.0])

# ------------------------------------------------------------------------------
# Interpolación suave (Cosine Easing)
# ------------------------------------------------------------------------------
function smooth_progress(t::Float64)
    t = clamp(t, 0.0, 1.0)
    return 0.5 * (1.0 - cos(π * t))
end

# ------------------------------------------------------------------------------
# Matrices de Transformación 3D elementales
# ------------------------------------------------------------------------------
rot_x(θ) = [
    1.0    0.0     0.0;
    0.0 cos(θ) -sin(θ);
    0.0 sin(θ)  cos(θ)
]

rot_y(θ) = [
     cos(θ) 0.0 sin(θ);
        0.0 1.0    0.0;
    -sin(θ) 0.0 cos(θ)
]

rot_z(θ) = [
    cos(θ) -sin(θ) 0.0;
    sin(θ)  cos(θ) 0.0;
       0.0     0.0 1.0
]

# ------------------------------------------------------------------------------
# Estado de la Transformación 3D según el frame
# Retorna:
#   A: Matriz 3x3
#   b: Vector de traslación 3D [bx, by, bz]
#   desc: Nombre de la transformación
#   math_str: Notación matemática
# ------------------------------------------------------------------------------
function get_affine_state_3d(frame::Int)
    phase = div(frame - 1, PHASE_FRAMES) + 1
    t_raw = mod(frame - 1, PHASE_FRAMES) / (PHASE_FRAMES - 1)
    t = smooth_progress(t_raw)

    I3 = Matrix{Float64}(I, 3, 3)

    if phase == 1
        # Fase 1: Identidad (Orientación neutra con leve ángulo para apreciar el 3D)
        # Rotación base suave (vista isométrica ligera)
        A = rot_x(0.35) * rot_y(-0.45)
        b = [0.0, 0.0, 0.0]
        desc = "1. Estado Inicial en R³ (Vista Perspectiva)"
        math_str = "T(x) = I₃ · x + 0   |   Proyección a 2D: x' = (x·d)/(z+d)"

    elseif phase == 2
        # Fase 2: Rotación 3D en el Eje Y (Yaw)
        θ_y = -0.45 + t * 2π
        A = rot_x(0.35) * rot_y(θ_y)
        b = [0.0, 0.0, 0.0]
        desc = "2. Rotación 3D alrededor del Eje Y: Ry(θ)"
        math_str = @sprintf("θ_y = %.1f°  |  Matriz ortogonal: det(R) = 1, R^T R = I", rad2deg(t * 2π))

    elseif phase == 3
        # Fase 3: Rotación 3D en el Eje X (Pitch)
        θ_x = 0.35 + t * 2π
        A = rot_x(θ_x) * rot_y(-0.45)
        b = [0.0, 0.0, 0.0]
        desc = "3. Rotación 3D alrededor del Eje X: Rx(φ)"
        math_str = @sprintf("φ_x = %.1f°  |  Giro espacial que muestra ambas caras", rad2deg(t * 2π))

    elseif phase == 4
        # Fase 4: Traslación en el Eje Z (Profundidad / Zoom de Perspectiva)
        # Δz oscila entre 0 y -200 (se aleja) y luego vuelve o se acerca
        Δz = -180.0 * sin(π * t)
        A = rot_x(0.4) * rot_y(-0.5)
        b = [0.0, 0.0, Δz]
        desc = "4. Traslación en Profundidad: Δz (Efecto Perspectiva)"
        math_str = @sprintf("b = [0, 0, %+.1f]  |  Al variar Z cambia la escala aparente", Δz)

    elseif phase == 5
        # Fase 5: Escalado 3D Anisotrópico (Diag(sx, sy, sz))
        # Estiramos en Z y variamos X e Y
        sx = 1.0 - 0.35 * sin(π * t)
        sy = 1.0 + 0.30 * sin(π * t)
        sz = 1.0 + 0.90 * sin(π * t) # estiramiento notable del prisma en Z
        S = [sx 0.0 0.0; 0.0 sy 0.0; 0.0 0.0 sz]
        A = rot_x(0.4) * rot_y(-0.5) * S
        b = [0.0, 0.0, 0.0]
        desc = "5. Escalamiento No Uniforme 3D: S = Diag(sx, sy, sz)"
        math_str = @sprintf("sx = %.2f,  sy = %.2f,  sz = %.2f (Deformación de volumen)", sx, sy, sz)

    else
        # Fase 6: Cizallamiento 3D (Shear espacial) + Rotación continua
        kx = 0.65 * sin(π * t)
        kz = 0.40 * sin(π * t)
        Shear3D = [1.0 kx kz; 0.0 1.0 0.0; 0.0 0.0 1.0]
        θ_spin = 0.45 + t * π
        A = rot_x(0.35) * rot_y(θ_spin) * Shear3D
        b = [0.0, 0.0, 0.0]
        desc = "6. Cizallamiento 3D (Shear) + Rotación General"
        math_str = @sprintf("Shear 3D: k_xy = %.2f, k_xz = %.2f  (Preserva volumen)", kx, kz)
    end

    return A, b, desc, math_str
end

# ------------------------------------------------------------------------------
# Proyección de R³ a R² (Cámara en perspectiva)
# ------------------------------------------------------------------------------
function project_to_2d(v::Vector{Float64})
    x, y, z = v[1], v[2], v[3]
    # Factor de escala por perspectiva: objetos con mayor z (más lejos) se ven más pequeños
    # Asumiendo que el ojo está en z = -D_CAMERA
    scale = D_CAMERA / (D_CAMERA + z)
    return Point(x * scale, y * scale)
end

# ------------------------------------------------------------------------------
# Dibujo de Fondo y Cuadrícula
# ------------------------------------------------------------------------------
function draw_background(args...)
    background("#0d1117")

    sethue("#161b22")
    setline(1)
    for x in -640:80:640
        line(Point(x, -360), Point(x, 360), :stroke)
    end
    for y in -360:80:360
        line(Point(-640, y), Point(640, y), :stroke)
    end
end

# ------------------------------------------------------------------------------
# Interfaz de Usuario: Título, Fase, Matrices 3x3 y vector b
# ------------------------------------------------------------------------------
function draw_ui(video, object, frame)
    A, b, desc, math_str = get_affine_state_3d(frame)

    # Título principal
    sethue("#58a6ff")
    fontsize(26)
    fontface("Helvetica-Bold")
    text("Transformaciones Afines en 3D:  T(x) = A · x + b", Point(0, -315), halign=:center)

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

    # Matriz A (3x3) y vector b (3x1) en pantalla
    mat_text = @sprintf(
        "A (3x3) = [ %+.2f  %+.2f  %+.2f ]          b (3x1) = [ %+.1f ]\n          [ %+.2f  %+.2f  %+.2f ]                    [ %+.1f ]\n          [ %+.2f  %+.2f  %+.2f ]                    [ %+.1f ]",
        A[1,1], A[1,2], A[1,3], b[1],
        A[2,1], A[2,2], A[2,3], b[2],
        A[3,1], A[3,2], A[3,3], b[3]
    )
    sethue("#79c0ff")
    fontsize(13)
    fontface("Courier")
    text(mat_text, Point(0, 280), halign=:center)

    # Separador vertical sutil
    sethue("#21262d")
    setline(1.5)
    line(Point(0, -210), Point(0, 225), :stroke)
end

# ------------------------------------------------------------------------------
# Dibujar Ejes Coordenados 3D locales (Rojo=X, Verde=Y, Azul=Z)
# ------------------------------------------------------------------------------
function draw_axes_3d(A::Matrix{Float64}, b::Vector{Float64}, axis_len::Float64 = 100.0)
    origin_3d = A * [0.0, 0.0, 0.0] + b
    p0 = project_to_2d(origin_3d)

    axes_dirs = [
        ([axis_len, 0.0, 0.0], "#ff5555", "X"),
        ([0.0, axis_len, 0.0], "#55ff55", "Y"),
        ([0.0, 0.0, axis_len], "#5599ff", "Z")
    ]

    for (d, color_hex, label) in axes_dirs
        p_end_3d = A * d + b
        p1 = project_to_2d(p_end_3d)

        sethue(color_hex)
        setline(2.0)
        line(p0, p1, :stroke)

        fontsize(11)
        fontface("Helvetica-Bold")
        text(label, p1 + Point(5, 5))
    end
end

# ------------------------------------------------------------------------------
# Renderizado de la Escena 3D
# ------------------------------------------------------------------------------
function draw_scene_3d(video, object, frame)
    A, b, _, _ = get_affine_state_3d(frame)

    # ==========================================================================
    # 1. PENTÁGONO PLANO EN EL ESPACIO 3D (Lado Izquierdo)
    # ==========================================================================
    @layer begin
        translate(CENTER_LEFT)

        sethue("#7ee787")
        fontsize(17)
        fontface("Helvetica-Bold")
        text("Pentágono Plano en R³", Point(0, -170), halign=:center)

        # Dibujar ejes 3D
        draw_axes_3d(A, b, 90.0)

        # Transformar vértices del pentágono regular 3D
        v_trans = [A * v + b for v in regular_pentagon_3d]
        pts_2d = [project_to_2d(v) for v in v_trans]

        # Calcular vector normal de la cara en 3D
        e1 = v_trans[2] - v_trans[1]
        e2 = v_trans[3] - v_trans[1]
        normal = normalize(cross(e1, e2))
        cos_light = abs(dot(normal, LIGHT_DIR))
        diffuse = clamp(0.3 + 0.7 * cos_light, 0.25, 1.0)

        # Relleno con sombreado según la normal
        setcolor(0.12 * diffuse, 0.43 * diffuse, 0.92 * diffuse, 0.75)
        poly(pts_2d, :fill, close=true)

        # Borde brillante
        sethue("#58a6ff")
        setline(3)
        poly(pts_2d, :stroke, close=true)

        # Dibujar normal proyectada como vector sutil desde el centro
        center_3d = sum(v_trans) / length(v_trans)
        center_2d = project_to_2d(center_3d)
        normal_tip_2d = project_to_2d(center_3d + normal * 50.0)
        sethue("#e3b341")
        setline(2)
        line(center_2d, normal_tip_2d, :stroke)
        circle(normal_tip_2d, 3, :fill)

        # Vértices 3D proyectados
        for p in pts_2d
            sethue("#ffffff")
            circle(p, 4.5, :fill)
            sethue("#1f6feb")
            circle(p, 2.5, :fill)
        end
    end

    # ==========================================================================
    # 2. PRISMA PENTAGONAL 3D (Lado Derecho)
    # ==========================================================================
    @layer begin
        translate(CENTER_RIGHT)

        sethue("#ffa657")
        fontsize(17)
        fontface("Helvetica-Bold")
        text("Prisma Pentagonal 3D (Extrusión)", Point(0, -170), halign=:center)

        # Dibujar ejes 3D locales
        draw_axes_3d(A, b, 90.0)

        # Transformar todos los vértices del prisma
        trans_vertices = [A * v + b for v in prism_vertices_all]
        pts2d_all = [project_to_2d(v) for v in trans_vertices]

        # Para renderizar correctamente en 3D usamos el Algoritmo del Pintor (Painter's Algorithm):
        # Ordenamos las caras desde la más lejana (mayor Z) hasta la más cercana (menor Z).
        face_depths = Float64[]
        for face in prism_faces
            # Z promedio de los vértices que componen la cara
            z_avg = sum(trans_vertices[idx][3] for idx in face.indices) / length(face.indices)
            push!(face_depths, z_avg)
        end

        # Ordenar caras de atrás hacia adelante (Z descendente / más alejado primero)
        sorted_indices = sortperm(face_depths, rev=true)

        for f_idx in sorted_indices
            face = prism_faces[f_idx]
            face_pts = [pts2d_all[i] for i in face.indices]
            face_v3d = [trans_vertices[i] for i in face.indices]

            # Calcular normal 3D de la cara
            u = face_v3d[2] - face_v3d[1]
            w = face_v3d[3] - face_v3d[1]
            n = cross(u, w)
            n_len = norm(n)
            normal = n_len > 1e-6 ? n / n_len : [0.0, 0.0, 1.0]

            # Iluminación Lambertiana
            cos_light = dot(normal, LIGHT_DIR)
            diffuse = clamp(0.25 + 0.75 * max(0.0, cos_light), 0.2, 1.0)

            r, g, b_col = face.base_color
            setcolor(r * diffuse, g * diffuse, b_col * diffuse, 0.88)
            poly(face_pts, :fill, close=true)

            # Contorno de las aristas
            sethue("#ffffff")
            setline(1.5)
            poly(face_pts, :stroke, close=true)
        end

        # Vértices visibles
        for p in pts2d_all
            sethue("#ffffff")
            circle(p, 3.5, :fill)
            sethue("#ff7b72")
            circle(p, 2.0, :fill)
        end
    end
end

# ==============================================================================
# Definición del Video y Renderizado
# ==============================================================================
video = Video(WIDTH, HEIGHT)

Background(1:TOTAL_FRAMES, draw_background)
Object(1:TOTAL_FRAMES, draw_ui)
Object(1:TOTAL_FRAMES, draw_scene_3d)

output_file = "transformaciones_3d_pentagono.gif"
println("Generando animación 3D en: ", output_file, " (", TOTAL_FRAMES, " frames)...")

render(
    video;
    pathname = output_file,
    framerate = FPS
)

println("¡Animación 3D generada con éxito en: ", output_file, "!")
