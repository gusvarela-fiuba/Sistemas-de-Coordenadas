#!/usr/bin/env julia
#=
rotacion3d.jl — Rotaciones en 3D con la fórmula de Rodrigues.

Material de estudio para Sistemas de Coordenadas (Agrimensura).
Port a Julia de rotacion3d.py (misma semántica, salida equivalente).

Qué hace este script:
  1. Construye la matriz de rotación R(θ) alrededor de un eje arbitrario
     (fórmula de Rodrigues).
  2. Rota un vector de forma INCREMENTAL, en pasos pequeños, y verifica que
     el resultado coincide con la rotación DIRECTA de una sola vez.
  3. Calcula autovalores y autovectores de R(θ) y los interpreta
     geométricamente: el eje de rotación es el autovector de autovalor 1,
     y los otros dos autovalores son e^{±iθ}.
  4. Verifica las propiedades clásicas: traza = 1 + 2cosθ, det = 1,
     R·Rᵀ = I (ortogonalidad).

Uso:
    julia rotacion3d.jl                      # defaults: eje z, v=(1,0,0), 0→90°, 9 pasos
    julia rotacion3d.jl --eje 1 1 1 --vector 1 0 0 --inicio 30 --fin 120 --pasos 6
    julia rotacion3d.jl -h                   # ayuda

Las funciones son usables desde el REPL sin ejecutar el main:
    julia> include("rotacion3d.jl")
    julia> matriz_rotacion([0, 0, 1], 90)

Dependencias: sólo la biblioteca estándar (LinearAlgebra, Printf).
=#

using LinearAlgebra
using Printf


# ---------------------------------------------------------------------------
# 1. Matriz de rotación (Rodrigues)
# ---------------------------------------------------------------------------

"""
    matriz_antisimetrica(k) -> Matrix{Float64}

Devuelve la matriz antisimétrica K asociada al vector k = (kx, ky, kz).

K es la matriz tal que K·v = k × v (producto vectorial) para todo v:

        [  0   -kz   ky ]
    K = [  kz   0   -kx ]
        [ -ky   kx   0  ]

Se llama "antisimétrica" porque Kᵀ = -K.
"""
function matriz_antisimetrica(k::AbstractVector{<:Real})::Matrix{Float64}
    length(k) == 3 || throw(ArgumentError("k debe tener exactamente 3 componentes."))
    kx, ky, kz = Float64.(k)
    return [ 0.0  -kz    ky;
             kz    0.0  -kx;
            -ky    kx    0.0]
end


"""
    matriz_rotacion(eje, angulo_grados) -> Matrix{Float64}

Matriz de rotación 3x3 alrededor de `eje` un ángulo `angulo_grados`.

Fórmula de Rodrigues:
    R = I + sinθ · K + (1 − cosθ) · K²
donde K es la matriz antisimétrica del eje UNITARIO.

El sentido de giro es antihorario (regla de la mano derecha) mirando
desde la punta del eje hacia el origen.

# Parámetros
- `eje`: dirección del eje de rotación (3 componentes). No hace falta que
  esté normalizado; acá se normaliza. No puede ser el vector nulo.
- `angulo_grados`: ángulo de rotación en grados.

# Devuelve
`Matrix{Float64}` de 3x3.
"""
function matriz_rotacion(eje::AbstractVector{<:Real}, angulo_grados::Real)::Matrix{Float64}
    length(eje) == 3 || throw(ArgumentError("El eje debe tener exactamente 3 componentes."))
    k = Float64.(collect(eje))
    norma = norm(k)
    norma == 0.0 && throw(ArgumentError("El eje de rotación no puede ser el vector nulo."))
    k = k ./ norma

    θ = deg2rad(Float64(angulo_grados))
    K = matriz_antisimetrica(k)
    return I + sin(θ) * K + (1.0 - cos(θ)) * (K * K)
end


# ---------------------------------------------------------------------------
# 2. Rotación incremental
# ---------------------------------------------------------------------------

"""
    rotar_incremental(vector, eje, angulo_inicio, angulo_fin, pasos) -> Vector{Vector{Float64}}

Rota `vector` alrededor de `eje` desde `angulo_inicio` hasta `angulo_fin`
en `pasos` incrementos iguales.

Procedimiento:
  - Se parte de v0 = R(θ0)·v  (el vector ya rotado al ángulo inicial).
  - Se aplica `pasos` veces la matriz R(Δθ), con Δθ = (θ1 − θ0) / pasos.
    Cada aplicación gira Δθ más, así que tras k pasos el vector está a
    θ0 + k·Δθ.

Idea didáctica: componer rotaciones alrededor del MISMO eje es sumar
ángulos, R(a)·R(b) = R(a+b). Por eso el resultado final debe coincidir
con R(θ1)·v aplicado de una vez (salvo error de redondeo).

# Devuelve
Lista de `pasos + 1` vectores de 3 componentes, incluyendo el inicial.
"""
function rotar_incremental(vector::AbstractVector{<:Real}, eje::AbstractVector{<:Real},
                           angulo_inicio::Real, angulo_fin::Real, pasos::Integer)::Vector{Vector{Float64}}
    pasos >= 1 || throw(ArgumentError("La cantidad de pasos debe ser un entero ≥ 1."))
    length(vector) == 3 || throw(ArgumentError("El vector debe tener exactamente 3 componentes."))

    v = Float64.(collect(vector))
    delta = (Float64(angulo_fin) - Float64(angulo_inicio)) / pasos

    R_inicio = matriz_rotacion(eje, angulo_inicio)
    R_paso = matriz_rotacion(eje, delta)

    actual = R_inicio * v
    trayectoria = Vector{Vector{Float64}}([actual])
    for _ in 1:pasos
        actual = R_paso * actual
        push!(trayectoria, actual)
    end
    return trayectoria
end


# ---------------------------------------------------------------------------
# Utilidades numéricas y de impresión
# ---------------------------------------------------------------------------

"""
    cerca(a, b) -> Bool

Comparación aproximada con las tolerancias por defecto de `numpy.isclose`
(rtol = 1e-5, atol = 1e-8). Se usa atol > 0 porque `isapprox` de Julia
tiene atol = 0 por defecto y fallaría al comparar contra 0 exacto
(por ejemplo, traza = 1 + 2cos(120°) = 0).
"""
cerca(a, b; rtol=1e-5, atol=1e-8) = isapprox(a, b; rtol=rtol, atol=atol)


"""
    fmt(x, precision) -> String

Formatea un número real con `precision` decimales, ancho fijo (precision + 8).
"""
function fmt(x::Real, precision::Int)::String
    return Printf.format(Printf.Format("%$(precision + 8).$(precision)f"), x)
end


"""
    fmt_dec(x, precision) -> String

Formatea un número real con `precision` decimales, sin ancho fijo.
"""
function fmt_dec(x::Real, precision::Int)::String
    return Printf.format(Printf.Format("%.$(precision)f"), x)
end


"""
    fmt_complejo(z, precision) -> String

Formatea un número complejo como 'a + bi' con `precision` decimales.
"""
function fmt_complejo(z::Number, precision::Int)::String
    z = ComplexF64(z)
    signo = imag(z) >= 0 ? "+" : "-"
    return fmt_dec(real(z), precision) * " " * signo * " " * fmt_dec(abs(imag(z)), precision) * "i"
end


"""
    fmt_vector(v, precision) -> String

Formatea un vector real como '[a, b, c]' con `precision` decimales
(equivalente a imprimir `np.round(v, precision)`).
"""
function fmt_vector(v::AbstractVector{<:Real}, precision::Int)::String
    return "[" * join((fmt_dec(x, precision) for x in v), ", ") * "]"
end


"""
    imprimir_matriz(M, precision; titulo=nothing)

Imprime una matriz fila por fila, con `precision` decimales.
"""
function imprimir_matriz(M::AbstractMatrix{<:Real}, precision::Int; titulo::Union{Nothing,String}=nothing)
    titulo === nothing || println(titulo)
    for i in 1:size(M, 1)
        println("   [" * join((fmt(x, precision) for x in M[i, :]), " ") * " ]")
    end
end


"""
    angulo_entre(u, v) -> Float64

Ángulo en grados entre dos vectores u y v (entre 0° y 180°).
Se recorta el coseno a [-1, 1] para evitar NaN por redondeo.
"""
function angulo_entre(u::AbstractVector{<:Real}, v::AbstractVector{<:Real})::Float64
    cos_ang = dot(u, v) / (norm(u) * norm(v))
    return rad2deg(acos(clamp(cos_ang, -1.0, 1.0)))
end


# ---------------------------------------------------------------------------
# Secciones del informe
# ---------------------------------------------------------------------------

"""
    seccion_incremental(vector, eje, inicio, fin, pasos, precision)

Imprime la tabla de rotación incremental y la verificación vs directa.
Devuelve la trayectoria.
"""
function seccion_incremental(vector::Vector{Float64}, eje::Vector{Float64},
                             inicio::Float64, fin::Float64, pasos::Int, precision::Int)
    println("=" ^ 78)
    println("ROTACIÓN INCREMENTAL")
    println("=" ^ 78)
    eje_u = eje ./ norm(eje)
    println("Eje (ingresado):  [", join(eje, ", "), "]")
    println("Eje (unitario):   ", fmt_vector(eje_u, precision))
    println("Vector inicial:   [", join(vector, ", "), "]")
    delta = (fin - inicio) / pasos
    println("Ángulo: $(inicio)° → $(fin)° en $(pasos) pasos (Δθ = $(fmt_dec(delta, precision))°)")
    println()

    trayectoria = rotar_incremental(vector, eje, inicio, fin, pasos)

    ancho = precision + 8
    cab = lpad("paso", 5) * " " * lpad("ángulo°", ancho) * " " * lpad("x", ancho) * " " *
          lpad("y", ancho) * " " * lpad("z", ancho) * " " * lpad("norma", ancho)
    println(cab)
    println("-" ^ length(cab))
    for (k, v) in enumerate(trayectoria)
        paso = k - 1                       # enumerate arranca en 1; el paso 0 es el inicial
        ang = inicio + paso * delta
        println(lpad(string(paso), 5), " ", fmt(ang, precision), " ", fmt(v[1], precision), " ",
                fmt(v[2], precision), " ", fmt(v[3], precision), " ",
                fmt(norm(v), precision))
    end
    println()

    # Verificación: incremental vs directa
    v_directo = matriz_rotacion(eje, fin) * vector
    v_incremental = trayectoria[end]
    diff_max = maximum(abs.(v_incremental .- v_directo))
    coincide = cerca(v_incremental, v_directo)

    println("Verificación: rotación incremental vs. rotación directa R(θ1)·v")
    println("   incremental: ", fmt_vector(v_incremental, precision))
    println("   directa:     ", fmt_vector(v_directo, precision))
    @printf("   diferencia máxima |Δ| = %.3e\n", diff_max)
    println("   isapprox → ", coincide)
    println()
    return trayectoria
end


"""
    seccion_autovalores(eje, fin, precision)

Autovalores/autovectores de R(θ1) e interpretación geométrica.
"""
function seccion_autovalores(eje::Vector{Float64}, fin::Float64, precision::Int)
    println("=" ^ 78)
    println("AUTOVALORES Y AUTOVECTORES DE R(θ1), θ1 = $(fin)°")
    println("=" ^ 78)
    R = matriz_rotacion(eje, fin)
    imprimir_matriz(R, precision; titulo="R(θ1) =")
    println()

    # `eigen` devuelve reales si todos los autovalores son reales (θ múltiplo
    # de 180°) y complejos en el caso general; unificamos a ComplexF64.
    F = eigen(R)
    autovalores = ComplexF64.(F.values)
    autovectores = ComplexF64.(F.vectors)

    println("Autovalores λ_i y su módulo |λ_i|:")
    for (i, lam) in enumerate(autovalores)
        println("   λ$(i) = $(fmt_complejo(lam, precision))   |λ$(i)| = $(fmt_dec(abs(lam), precision))")
    end
    println("   (todos tienen módulo 1: una rotación no cambia longitudes)")
    println()

    println("Autovectores (por columnas, uno por autovalor, normalizados):")
    for i in 1:3
        col = autovectores[:, i]
        comps = join((fmt_complejo(c, precision) for c in col), ", ")
        println("   v$(i) = [ $(comps) ]")
    end
    println()

    # --- Interpretación: autovalor real 1 ↔ eje de rotación -----------------
    println("Interpretación geométrica")
    println("-" ^ 78)
    eje_u = eje ./ norm(eje)

    # El autovalor más cercano a 1 (parte imaginaria ~0) es el del eje.
    idx_eje = argmin(abs.(autovalores .- 1.0))
    v_eje = autovectores[:, idx_eje]
    # `eigen` puede devolver una fase compleja aunque el vector sea real:
    # nos quedamos con la parte real, normalizada.
    v_eje = real.(v_eje)
    v_eje = v_eje ./ norm(v_eje)

    ang = angulo_entre(v_eje, eje_u)
    # "Hasta el signo": si el autovector apunta al revés, el ángulo es ~180°.
    ang_hasta_signo = min(ang, 180.0 - ang)

    println("* Autovalor real λ$(idx_eje) ≈ 1 → su autovector es el EJE de rotación")
    println("  (los puntos sobre el eje no se mueven al rotar: R·k = k).")
    println("     autovector (real, unitario): ", fmt_vector(v_eje, precision))
    println("     eje ingresado (unitario):    ", fmt_vector(eje_u, precision))
    println("     ángulo entre ambos: $(fmt_dec(ang, precision))°  " *
            "(hasta el signo: $(fmt_dec(ang_hasta_signo, precision))°)")
    println("     paralelos → ", isapprox(ang_hasta_signo, 0.0; atol=1e-6))
    println()

    # --- Interpretación: autovalores complejos e^{±iθ} ----------------------
    otros = [i for i in 1:3 if i != idx_eje]
    theta_mod = mod(fin + 180.0, 360.0) - 180.0   # θ1 llevado a [-180°, 180°)
    println("* Los otros dos autovalores son complejos conjugados e^{±iθ1}:")
    println("  describen el giro en el plano perpendicular al eje.")
    println("     θ1 = $(fin)°  (equivalente en (-180°, 180°]: $(fmt_dec(theta_mod, precision))°)")
    args_ok = true
    for i in otros
        lam = autovalores[i]
        arg_deg = rad2deg(angle(lam))
        # El argumento debe coincidir con +θ1 o con -θ1 (módulo 360°).
        ok = isapprox(arg_deg, theta_mod; atol=1e-6) || isapprox(arg_deg, -theta_mod; atol=1e-6)
        args_ok = args_ok && ok
        arg_str = Printf.format(Printf.Format("%$(precision + 9).$(precision)f"), arg_deg)
        println("     arg(λ$(i)) = $(arg_str)°   coincide con ±θ1 → $(ok)")
    end
    println("     argumentos = ±θ1 → ", args_ok)
    if isapprox(sin(deg2rad(fin)), 0.0; atol=1e-12)
        println("     (nota: con sinθ1 = 0 los tres autovalores son reales, " *
                "±1; los 'complejos' degeneran a reales)")
    end
    println()

    # --- Propiedades numéricas ---------------------------------------------
    println("Propiedades de una matriz de rotación")
    println("-" ^ 78)
    traza = tr(R)
    traza_teorica = 1.0 + 2.0 * cos(deg2rad(fin))
    determinante = det(R)
    RRt = R * transpose(R)
    println("* traza(R) = $(fmt_dec(traza, precision))   vs.  1 + 2cosθ1 = $(fmt_dec(traza_teorica, precision))" *
            "   → $(cerca(traza, traza_teorica))")
    println("* det(R)   = $(fmt_dec(determinante, precision))   vs.  1" *
            "   → $(cerca(determinante, 1.0))")
    println("* R·Rᵀ = I  (ortogonalidad)  → ", cerca(RRt, Matrix{Float64}(I, 3, 3)))
    imprimir_matriz(RRt, precision; titulo="  R·Rᵀ =")
    println("  (además, el producto de los autovalores = det = " *
            "$(fmt_dec(real(prod(autovalores)), precision)), " *
            "y su suma = traza = $(fmt_dec(real(sum(autovalores)), precision)))")
    println()
end


# ---------------------------------------------------------------------------
# CLI (parseo manual de ARGS, sin paquetes externos)
# ---------------------------------------------------------------------------

"""
Excepción para errores de sintaxis de la línea de comandos. Se captura en
`main` y se informa en español a stderr con exit code 1, igual que los
errores de validación.
"""
struct ErrorCLI <: Exception
    msg::String
end


"""
Opciones del programa con sus valores por defecto.
"""
Base.@kwdef mutable struct Opciones
    eje::Vector{Float64} = [0.0, 0.0, 1.0]
    vector::Vector{Float64} = [1.0, 0.0, 0.0]
    inicio::Float64 = 0.0
    fin::Float64 = 90.0
    pasos::Int = 9
    precision::Int = 4
end


const NOMBRE_PROGRAMA = "rotacion3d.jl"


"""
    texto_ayuda() -> String

Ayuda del programa (en español), al estilo de argparse.
"""
function texto_ayuda()::String
    return """
    uso: $(NOMBRE_PROGRAMA) [-h] [--eje X Y Z] [--vector X Y Z] [--inicio GRADOS]
                        [--fin GRADOS] [--pasos N] [--precision DECIMALES]

    Rotación 3D alrededor de un eje arbitrario (fórmula de Rodrigues): rotación
    incremental de un vector, verificación contra la rotación directa, y análisis
    de autovalores/autovectores de la matriz R(θ1).

    opciones:
      -h, --help            muestra esta ayuda y termina
      --eje X Y Z           eje de rotación (3 componentes; se normaliza). Default: 0 0 1
      --vector X Y Z        vector a rotar (3 componentes). Default: 1 0 0
      --inicio GRADOS       ángulo inicial en grados. Default: 0
      --fin GRADOS          ángulo final en grados. Default: 90
      --pasos N             cantidad de pasos incrementales (entero ≥ 1). Default: 9
      --precision DECIMALES decimales al imprimir. Default: 4

    Ejemplos:
      julia $(NOMBRE_PROGRAMA)
      julia $(NOMBRE_PROGRAMA) --eje 1 1 1 --vector 1 0 0 --inicio 30 --fin 120 --pasos 6
      julia $(NOMBRE_PROGRAMA) --eje 0 1 0 --fin 180 --precision 6"""
end


"""
    es_opcion(token) -> Bool

Un token es una opción si empieza con '-' y NO es un número (así `-1` o
`-0.5` se aceptan como valores negativos).
"""
es_opcion(token::AbstractString)::Bool = startswith(token, "-") && tryparse(Float64, token) === nothing


"""
    tomar_valores(args, i, n, nombre) -> Vector{String}

Devuelve los `n` tokens que siguen a la posición `i` (la de la opción
`nombre`), verificando que existan y que no sean otras opciones.
"""
function tomar_valores(args::AbstractVector{<:AbstractString}, i::Int, n::Int, nombre::String)::Vector{String}
    valores = String[]
    for j in (i + 1):(i + n)
        if j > length(args) || es_opcion(args[j])
            cuantos = n == 1 ? "se esperaba 1 valor" : "se esperaban $(n) valores"
            throw(ErrorCLI("argumento $(nombre): $(cuantos)"))
        end
        push!(valores, String(args[j]))
    end
    return valores
end


"""
    a_float(s, nombre) -> Float64

Convierte un token a Float64 o lanza ErrorCLI con mensaje en español.
"""
function a_float(s::AbstractString, nombre::String)::Float64
    x = tryparse(Float64, s)
    x === nothing && throw(ErrorCLI("argumento $(nombre): valor numérico inválido: '$(s)'"))
    return x
end


"""
    a_int(s, nombre) -> Int

Convierte un token a Int o lanza ErrorCLI con mensaje en español.
"""
function a_int(s::AbstractString, nombre::String)::Int
    x = tryparse(Int, s)
    x === nothing && throw(ErrorCLI("argumento $(nombre): valor entero inválido: '$(s)'"))
    return x
end


"""
    parsear_args(args) -> Union{Opciones, Nothing}

Parsea la línea de comandos a mano. Devuelve `nothing` si se pidió la ayuda
(ya impresa a stdout); lanza `ErrorCLI` ante errores de sintaxis.
"""
function parsear_args(args::AbstractVector{<:AbstractString})::Union{Opciones,Nothing}
    op = Opciones()
    no_reconocidos = String[]
    i = 1
    while i <= length(args)
        tok = args[i]
        if tok == "-h" || tok == "--help"
            println(texto_ayuda())
            return nothing
        elseif tok == "--eje"
            vals = tomar_valores(args, i, 3, tok)
            op.eje = [a_float(s, tok) for s in vals]
            i += 4
        elseif tok == "--vector"
            vals = tomar_valores(args, i, 3, tok)
            op.vector = [a_float(s, tok) for s in vals]
            i += 4
        elseif tok == "--inicio"
            op.inicio = a_float(tomar_valores(args, i, 1, tok)[1], tok)
            i += 2
        elseif tok == "--fin"
            op.fin = a_float(tomar_valores(args, i, 1, tok)[1], tok)
            i += 2
        elseif tok == "--pasos"
            op.pasos = a_int(tomar_valores(args, i, 1, tok)[1], tok)
            i += 2
        elseif tok == "--precision"
            op.precision = a_int(tomar_valores(args, i, 1, tok)[1], tok)
            i += 2
        else
            push!(no_reconocidos, String(tok))
            i += 1
        end
    end
    isempty(no_reconocidos) || throw(ErrorCLI("argumentos no reconocidos: " * join(no_reconocidos, " ")))
    return op
end


"""
    validar(op) -> Union{String, Nothing}

Valida los argumentos; devuelve un mensaje de error o `nothing` si está todo bien.
"""
function validar(op::Opciones)::Union{String,Nothing}
    length(op.eje) == 3 || return "El eje debe tener exactamente 3 componentes."
    all(isfinite, op.eje) || return "El eje tiene componentes no finitas (nan/inf)."
    norm(op.eje) == 0.0 && return "El eje de rotación no puede ser el vector nulo (0 0 0)."

    length(op.vector) == 3 || return "El vector debe tener exactamente 3 componentes."
    all(isfinite, op.vector) || return "El vector tiene componentes no finitas (nan/inf)."

    isfinite(op.inicio) || return "El ángulo inicial no es finito (nan/inf)."
    isfinite(op.fin) || return "El ángulo final no es finito (nan/inf)."

    op.pasos >= 1 || return "La cantidad de pasos debe ser ≥ 1 (se recibió $(op.pasos))."
    op.precision >= 0 || return "La precisión debe ser ≥ 0 (se recibió $(op.precision))."
    return nothing
end


"""
    main(args) -> Int

Punto de entrada. Devuelve el exit code (0 ok, 1 error).
"""
function main(args::AbstractVector{<:AbstractString}=ARGS)::Int
    op = try
        parsear_args(args)
    catch e
        e isa ErrorCLI || rethrow()
        println(stderr, "Error: ", e.msg)
        println(stderr, "Usá -h para ver la ayuda.")
        return 1
    end
    op === nothing && return 0          # se imprimió la ayuda

    error = validar(op)
    if error !== nothing
        println(stderr, "Error: ", error)
        println(stderr, "Usá -h para ver la ayuda.")
        return 1
    end

    seccion_incremental(op.vector, op.eje, op.inicio, op.fin, op.pasos, op.precision)
    seccion_autovalores(op.eje, op.fin, op.precision)
    return 0
end


# Sólo se ejecuta el main si el archivo se corre como script
# (`julia rotacion3d.jl ...`); con `include("rotacion3d.jl")` desde el REPL
# quedan definidas las funciones sin correr nada.
if abspath(PROGRAM_FILE) == @__FILE__
    exit(main(ARGS))
end
