#!/usr/bin/env python3
"""Genera los problemas por capítulo y sus respuestas.

Cada número de cada respuesta sale de una cuenta hecha acá (numpy), no está escrito a mano.
Salidas (en el directorio indicado con --salida, por defecto el actual):
  problemas/pNN.tex      sección «Problemas» de cada capítulo (1 a 15), sin soluciones
  ap6-respuestas.tex     apéndice con las respuestas
  problemas.html         versión para leer en el navegador (KaTeX)
Uso: python3 tools/problemas/gen.py --salida apunte/contenido
"""
import argparse, math, pathlib, html
import numpy as np

D = math.radians
G = math.degrees


def n(x, d=2, tex=True):
    """Número con coma decimal y espacio fino de miles (estilo del apunte)."""
    if round(x, d) == 0:
        x = 0.0
    s = f"{x:,.{d}f}" if d > 0 else f"{round(x):,}"
    ent, _, dec = s.partition(".")
    neg = ent.startswith("-")
    ent = ent.lstrip("-").replace(",", "\\," if tex else "\u2009")
    if neg:
        ent = "-" + ent
    if not tex:
        ent = ent.replace("-", "−")
    return ent + (("{,}" if tex else ",") + dec if dec else "")


def ang(x, d=2):
    return n(x, d) + "^\\circ"


def vec(*xs, d=2):
    sep = "," if d == 0 else ";\\ "
    return "(" + sep.join(n(x, d) for x in xs) + ")"


def rot(t):
    c, s = math.cos(D(t)), math.sin(D(t))
    return np.array([[c, -s], [s, c]])


C = {}  # capítulo -> (título, [ (nivel, enunciado, respuesta) ])

# ---------------------------------------------------------------- 1 Rotaciones
p = rot(30) @ np.array([4, 1])
E3 = 1000 + 120 * math.sin(D(135)); N3 = 2000 + 120 * math.cos(D(135))
q4 = np.array([2, 1]) + rot(90) @ (np.array([5, 1]) - np.array([2, 1]))
corr = 2000 * D(1 / 3600) * 1000
C[1] = ("Rotaciones: girar es multiplicar", [
 (1, "Rotá el punto \\(p=(4,1)\\) un ángulo de \\(30^\\circ\\) en sentido antihorario alrededor del origen. Comprobá que la distancia al origen no cambió.",
  f"\\(p'={vec(*p, d=3)}\\); \\(\\lVert p'\\rVert=\\lVert p\\rVert=\\sqrt{{17}}\\approx{n(math.sqrt(17),3)}\\)."),
 (1, "Con números complejos: multiplicá \\(z=3+4i\\) por \\(i\\). ¿Qué ángulo giró \\(z\\)? ¿Cambió su módulo?",
  "\\(iz=-4+3i\\): giró \\(90^\\circ\\) en sentido antihorario y el módulo sigue siendo \\(5\\)."),
 (2, "Desde una estación \\(S=(1000;\\ 2000)\\) m, en coordenadas \\((E,N)\\), se mide un punto a \\(120\\) m con acimut \\(\\mathrm{Az}=135^\\circ\\). Calculá sus coordenadas. ¿Cuánto vale el ángulo matemático \\(\\theta\\), medido desde el este en sentido antihorario?",
  f"\\(E={n(E3)}\\) m, \\(N={n(N3)}\\) m. \\(\\theta=90^\\circ-\\mathrm{{Az}}=-45^\\circ\\) (o \\(315^\\circ\\))."),
 (2, "Girá \\(p=(5,1)\\) un ángulo de \\(90^\\circ\\) antihorario, pero alrededor del centro \\(c=(2,1)\\), no del origen. Hacelo en tres pasos: llevar \\(c\\) al origen, girar y volver.",
  f"\\(p-c=(3,0)\\), girado da \\((0,3)\\), y al volver queda \\(p'={vec(*q4, d=0)}\\)."),
 (3, "Hay instrumentos que miden ángulos con precisión de un segundo de arco. Si el ángulo hacia un punto que está a \\(2\\) km cambia \\(1''\\), ¿cuánto se corre el punto de costado? Y en el espacio: aplicá a \\(e_1\\) primero un giro de \\(90^\\circ\\) alrededor del eje \\(z\\) y después uno de \\(90^\\circ\\) alrededor del eje \\(x\\); repetí en el otro orden. ¿Da lo mismo?",
  f"Se corre unos {n(corr,1)} mm (\\(2000\\cdot 1''\\) en radianes). En el espacio no da lo mismo: primero \\(z\\) y después \\(x\\) lleva \\(e_1\\to e_2\\to e_3\\); en el otro orden, \\(e_1\\to e_1\\to e_2\\)."),
])

# ---------------------------------------------------------------- 2 Traslaciones
R90 = rot(90); Cc = np.array([0, 3]); v = np.array([2, -1])
TR = R90 @ (Cc + v); RT = R90 @ Cc + v
B = np.array([4, 0]); tvec = B - rot(-90) @ B
cc = np.array([10, 10]); R30 = rot(30); tt = cc - R30 @ cc
C[2] = ("Traslaciones y movimientos rígidos", [
 (1, "Al triángulo \\(A=(0,0)\\), \\(B=(4,0)\\), \\(C=(0,3)\\) aplicale primero la traslación de vector \\(v=(2,-1)\\) y después el giro de \\(90^\\circ\\) alrededor del origen. Repetí en el otro orden. ¿Dónde termina \\(C\\) en cada caso?",
  f"Trasladar y después girar: \\(C\\to{vec(*TR, d=0)}\\). Girar y después trasladar: \\(C\\to{vec(*RT, d=0)}\\). El orden importa."),
 (2, "Girás \\(90^\\circ\\) alrededor de \\(A=(0,0)\\) y después \\(-90^\\circ\\) alrededor de \\(B=(4,0)\\). Mostrá que el resultado es una traslación y encontrá su vector.",
  f"Los ángulos suman \\(0^\\circ\\), así que queda una traslación, de vector \\({vec(*tvec, d=0)}\\). Comprobación: el origen va a \\((0,0)\\) y después a \\((4,4)\\)."),
 (2, "Escribí la matriz \\(3\\times3\\) en coordenadas homogéneas del giro de \\(30^\\circ\\) alrededor de \\(c=(10,10)\\).",
  f"\\(\\begin{{pmatrix}}{n(R30[0,0],4)}&{n(R30[0,1],4)}&{n(tt[0],4)}\\\\{n(R30[1,0],4)}&{n(R30[1,1],4)}&{n(tt[1],4)}\\\\0&0&1\\end{{pmatrix}}\\); la última columna es \\(c-Rc\\)."),
 (2, "Caminar y girar: arrancás en \\((0,0)\\) mirando al norte. Caminás \\(10\\) m, girás \\(90^\\circ\\) a la derecha, caminás \\(10\\) m, girás \\(45^\\circ\\) a la izquierda y caminás \\(10\\sqrt2\\) m. ¿Dónde terminás y hacia dónde mirás?",
  "Terminás en \\((20,20)\\) m, mirando al noreste: acimut \\(45^\\circ\\)."),
 (3, "Escribí el punto \\((3,4)\\) en coordenadas polares. Dibujá las dos líneas coordenadas que pasan por él (la de \\(r\\) constante y la de \\(\\theta\\) constante) y explicá por qué se cortan en ángulo recto.",
  f"\\(r=5\\), \\(\\theta\\approx{ang(G(math.atan2(4,3)))}\\). Son la circunferencia de radio \\(5\\) y la semirrecta que sale del origen; se cortan en ángulo recto porque la tangente a una circunferencia es perpendicular al radio."),
])

# ---------------------------------------------------------------- 3 Reflexiones
def refl_linea(t):
    c, s = math.cos(2 * D(t)), math.sin(2 * D(t))
    return np.array([[c, s], [s, -c]])
p3 = refl_linea(25) @ refl_linea(0) @ np.array([1, 0])
a = (complex(1, 5) - complex(1, 1)) / 2; b = complex(1, 1); z = a * complex(1, 1) + b
C[3] = ("Reflexiones, isometrías y similaridades", [
 (1, "Reflejá \\(p=(5,1)\\) respecto de la recta \\(y=x\\) y respecto de la recta \\(x+y=2\\).",
  "Respecto de \\(y=x\\): \\((1,5)\\). Respecto de \\(x+y=2\\), con normal \\(n=(1,1)\\): \\(p-\\frac{2(5+1-2)}{2}(1,1)=(1,-3)\\)."),
 (2, "Dos espejos pasan por el origen: uno a lo largo del eje \\(x\\) y otro a \\(25^\\circ\\) de él. Reflejá \\((1,0)\\) primero en el eje \\(x\\) y después en el otro espejo. ¿Qué transformación es la composición?",
  f"Es el giro de \\(50^\\circ\\), el doble del ángulo entre los espejos: \\((1,0)\\to{vec(*p3, d=3)}=(\\cos50^\\circ,\\sin50^\\circ)\\)."),
 (2, "Una similaridad \\(z\\mapsto az+b\\) lleva \\(0\\mapsto 1+i\\) y \\(2\\mapsto 1+5i\\). Encontrá \\(a\\) y \\(b\\), decí cuánto gira y cuánto agranda, y calculá la imagen de \\(1+i\\).",
  f"\\(b=1+i\\), \\(a=2i\\): gira \\(90^\\circ\\) y agranda \\(2\\) veces. La imagen de \\(1+i\\) es \\({n(z.real,0)}+{n(z.imag,0)}i\\)."),
 (1, "Un plano a escala \\(1:500\\) se fotocopia ampliado al \\(141\\)\\,\\%. ¿Qué escala tiene la copia? ¿Por cuánto se multiplican las áreas dibujadas?",
  f"Escala \\(1:{n(500/1.41,1)}\\): cerca de \\(1:355\\). Las áreas se multiplican por \\(1{{,}}41^2\\approx{n(1.41**2,3)}\\)."),
 (3, "Reflejá en el eje \\(x\\) y después trasladá \\((3,0)\\) (una reflexión con deslizamiento). ¿Tiene puntos fijos? ¿Qué da al aplicarla dos veces? Calculá la imagen de \\((0,2)\\).",
  "No tiene puntos fijos: cambia el signo de \\(y\\) y siempre suma \\(3\\) a \\(x\\). Aplicada dos veces da la traslación \\((6,0)\\). La imagen de \\((0,2)\\) es \\((3,-2)\\)."),
])

# ---------------------------------------------------------------- 4 Afinidades
A4 = np.array([[3, 1], [1, 3]]); t4 = np.array([2, 1])
A5 = np.array([[0, -0.5], [0.5, 0]]); t5 = np.array([3, 1]); fp = np.linalg.solve(np.eye(2) - A5, t5)
fac = 1 / 0.996
C[4] = ("Afinidades y coordenadas homogéneas", [
 (1, "Encontrá la afinidad \\(x\\mapsto Ax+b\\) que lleva \\((0,0)\\), \\((1,0)\\) y \\((0,1)\\) a \\((2,1)\\), \\((5,2)\\) y \\((3,4)\\). ¿A dónde va \\((1,1)\\)? ¿Por cuánto multiplica las áreas?",
  f"\\(b=(2,1)\\) y \\(A=\\begin{{pmatrix}}3&1\\\\1&3\\end{{pmatrix}}\\), con las columnas \\((5,2)-b\\) y \\((3,4)-b\\). \\((1,1)\\mapsto(6,5)\\). Las áreas se multiplican por \\(\\det A={int(round(np.linalg.det(A4)))}\\)."),
 (2, "Con la afinidad del problema anterior, comprobá que el punto medio de \\((0,0)\\) y \\((2,2)\\) va al punto medio de las imágenes. ¿Pasa lo mismo con los ángulos?",
  "Las imágenes son \\((2,1)\\) y \\((10,9)\\), con punto medio \\((6,5)\\), que es la imagen de \\((1,1)\\). Los ángulos, en cambio, no se conservan: \\((1,0)\\) y \\((0,1)\\) van a \\((3,1)\\) y \\((1,3)\\), que ya no son perpendiculares."),
 (2, "Un plano escaneado se encogió un \\(0{,}4\\)\\,\\% en sentido horizontal y nada en vertical. Escribí la afinidad que lo corrige. Un lote mide \\(30\\times20\\) m sobre el plano escaneado (\\(30\\) en horizontal): ¿cuál es su superficie real?",
  f"\\(x'=x/0{{,}}996\\approx{n(fac,6)}\\,x\\), \\(y'=y\\). La superficie real es \\(600\\cdot{n(fac,6)}\\approx{n(600*fac,2)}\\) m\\(^2\\)."),
 (2, "En coordenadas homogéneas, escribí las matrices de «trasladar \\((2,3)\\)» y de «escalar \\(\\times2\\) desde el origen». Aplicá a \\((1,1)\\) las dos en un orden y en el otro.",
  "Trasladar y después escalar: \\((1,1)\\to(3,4)\\to(6,8)\\). Escalar y después trasladar: \\((1,1)\\to(2,2)\\to(4,5)\\)."),
 (3, "La afinidad \\(x\\mapsto Ax+b\\), con \\(A=\\begin{pmatrix}0&-0{,}5\\\\0{,}5&0\\end{pmatrix}\\) y \\(b=(3,1)\\), gira \\(90^\\circ\\) y achica a la mitad. Encontrá su punto fijo, resolviendo \\((I-A)p=b\\).",
  f"\\(p={vec(*fp, d=0)}\\). Comprobación: \\(Ap+b=p\\)."),
])

# ---------------------------------------------------------------- 5 Formas lineales
g = np.array([0.02, -0.01]); az = G(math.atan2(g[0], g[1])) % 360
C[5] = ("Formas lineales: el gradiente no es un vector", [
 (1, "Para la forma \\(\\omega(x,y)=3x-2y\\), calculá \\(\\omega(4,1)\\). Dibujá las rectas \\(\\omega=0\\), \\(\\omega=1\\) y \\(\\omega=2\\): ¿qué distancia hay entre dos consecutivas?",
  f"\\(\\omega(4,1)=10\\). Son rectas paralelas \\(3x-2y=k\\), separadas \\(1/\\sqrt{{13}}\\approx{n(1/math.sqrt(13),3)}\\)."),
 (2, "Un terreno plano tiene altura \\(h=100+0{,}02\\,E-0{,}01\\,N\\) (en metros). ¿Cuánto subís si caminás \\(50\\) m al este y \\(30\\) m al norte? ¿Qué forma lineal da esa subida?",
  "Subís \\(0{,}02\\cdot50-0{,}01\\cdot30=0{,}70\\) m. La forma es \\(dh=(0{,}02;\\ -0{,}01)\\): a cada paso \\((\\Delta E,\\Delta N)\\) le asigna cuánto subiste."),
 (2, "Repetí la cuenta del problema anterior para el paso \\((3,4)\\) m, pero midiendo los pasos en centímetros. ¿Cómo cambian las componentes del paso y las de la forma? ¿Cambia la subida?",
  "El paso pasa a ser \\((300,400)\\) cm, y la forma, \\((0{,}0002;\\ -0{,}0001)\\) m por cm: uno se multiplica por \\(100\\) y la otra se divide por \\(100\\). La subida no cambia: \\(0{,}02\\) m."),
 (2, "Encontrá la base dual de \\(b_1=(1,1)\\), \\(b_2=(1,-1)\\): las dos formas \\(e^1\\), \\(e^2\\) que valen \\(1\\) en su vector y \\(0\\) en el otro.",
  "\\(e^1=(\\tfrac12,\\tfrac12)\\) y \\(e^2=(\\tfrac12,-\\tfrac12)\\). Comprobación: \\(e^1(b_1)=1\\), \\(e^1(b_2)=0\\), y lo mismo con \\(e^2\\)."),
 (3, "En el terreno del problema 2, ¿hacia qué acimut se sube más rápido? ¿Cuál es esa pendiente máxima, en porcentaje?",
  f"Hacia la dirección del gradiente \\((0{{,}}02;\\ -0{{,}}01)\\), con acimut \\(\\mathrm{{Az}}\\approx{ang(az)}\\). La pendiente máxima es \\(\\lVert g\\rVert\\approx{n(np.linalg.norm(g)*100,2)}\\)\\,\\%."),
])

# ---------------------------------------------------------------- 6 Cuña y determinante
P6 = np.array([(0, 0), (40, 0), (50, 30), (10, 40)], float)
area = 0.5 * abs(sum(P6[i, 0] * P6[(i + 1) % 4, 1] - P6[(i + 1) % 4, 0] * P6[i, 1] for i in range(4)))
C[6] = ("Subespacios, producto cuña y determinante", [
 (1, "Calculá con el producto cuña el área del triángulo de vértices \\((0,0)\\), \\((6,1)\\) y \\((2,5)\\).",
  "\\(\\tfrac12\\,|(6,1)\\wedge(2,5)|=\\tfrac12|6\\cdot5-1\\cdot2|=14\\)."),
 (1, "¿Están alineados los mojones \\((1,2)\\), \\((3,5)\\) y \\((7,11)\\)?",
  "Sí: \\((2,3)\\wedge(6,9)=18-18=0\\). El triángulo que forman no tiene área."),
 (2, "Un lote tiene vértices \\((E,N)\\) en metros: \\((0,0)\\), \\((40,0)\\), \\((50,30)\\), \\((10,40)\\), en ese orden. Calculá su superficie sumando cuñas.",
  f"\\(\\tfrac12\\sum p_i\\wedge p_{{i+1}}=\\tfrac12(0+1200+1700+0)={n(area,0)}\\) m\\(^2\\). El signo positivo indica que los vértices van en sentido antihorario."),
 (2, "Aplicale al lote del problema anterior la transformación \\(A=\\begin{pmatrix}2&1\\\\1&3\\end{pmatrix}\\). ¿Qué superficie tiene la imagen? ¿Se invierte el sentido del recorrido?",
  f"\\(\\det A=5\\): la superficie pasa a \\({n(area*5,0)}\\) m\\(^2\\). Como el determinante es positivo, el sentido se conserva."),
 (3, "Para \\(A=\\begin{pmatrix}1&2\\\\2&4\\end{pmatrix}\\), calculá \\(\\det A\\), el núcleo y la imagen. ¿En qué se convierte el cuadrado de lados \\(e_1\\) y \\(e_2\\)?",
  "\\(\\det A=0\\). El núcleo es la recta generada por \\((2,-1)\\) y la imagen, la generada por \\((1,2)\\). El cuadrado se aplasta sobre esa recta: queda un segmento, de área \\(0\\)."),
])

# ---------------------------------------------------------------- 7 Autovalores
Et = np.array([[-200, 150], [150, 400]]); ev = np.linalg.eigvalsh(Et)[::-1]
wv7, Vv7 = np.linalg.eigh(Et); th = G(math.atan2(Vv7[1, -1], Vv7[0, -1])) % 180
C[7] = ("Subespacios invariantes: autovalores y autovectores", [
 (1, "Encontrá los autovalores y autovectores de \\(A=\\begin{pmatrix}3&1\\\\0&2\\end{pmatrix}\\).",
  "\\(\\lambda=3\\) con \\((1,0)\\) y \\(\\lambda=2\\) con \\((1,-1)\\)."),
 (2, "Hacé lo mismo con la simétrica \\(S=\\begin{pmatrix}5&2\\\\2&2\\end{pmatrix}\\) y comprobá que los autovectores son perpendiculares.",
  "\\(\\lambda=6\\) con \\((2,1)\\) y \\(\\lambda=1\\) con \\((1,-2)\\). El producto interno da \\(2-2=0\\)."),
 (2, "Mostrá que el giro de \\(30^\\circ\\) del plano no tiene autovalores reales. ¿Qué significa eso geométricamente?",
  f"El polinomio es \\(\\lambda^2-2\\cos30^\\circ\\,\\lambda+1\\), con discriminante \\(4\\cos^2 30^\\circ-4={n(4*math.cos(D(30))**2-4,0)}<0\\). Ninguna dirección queda sin girar."),
 (2, "La matriz que lleva \\(e_1\\to e_2\\), \\(e_2\\to e_3\\) y \\(e_3\\to e_1\\) es un giro del espacio. Encontrá su eje (el autovector de autovalor \\(1\\)) y el ángulo de giro.",
  "El eje es \\((1,1,1)\\) y el ángulo, \\(120^\\circ\\): tres aplicaciones devuelven cada eje a su lugar."),
 (3, "En una placa se mide el tensor de deformación \\(E=\\begin{pmatrix}-200&150\\\\150&400\\end{pmatrix}\\) (en microdeformaciones, \\(\\mu\\varepsilon\\)). Calculá las deformaciones principales \\(e_1\\), \\(e_2\\) y el ángulo de la dirección principal con el eje \\(x\\).",
  f"\\(e_1\\approx{n(ev[0],1)}\\ \\mu\\varepsilon\\) (estiramiento) y \\(e_2\\approx{n(ev[1],1)}\\ \\mu\\varepsilon\\) (acortamiento). La dirección de \\(e_1\\) forma \\({ang(th)}\\) con el eje \\(x\\): está cerca del eje \\(y\\), que es donde la placa más se estira."),
])

# ---------------------------------------------------------------- 8 SVD
s3 = np.linalg.svd(np.array([[1, 1], [0, 1]]), compute_uv=False)
Sg = np.array([[4, 1.5], [1.5, 1]]); w, V = np.linalg.eigh(Sg); semi = np.sqrt(w[::-1])
thE = G(0.5 * math.atan2(2 * 1.5, 4 - 1)); azE = 90 - thE
A8 = np.array([[1, 1], [1, 1.01]]); s8 = np.linalg.svd(A8, compute_uv=False)
C[8] = ("La SVD: leer la forma de las curvas de nivel", [
 (1, "¿En qué elipse convierte \\(A=\\begin{pmatrix}3&0\\\\0&1\\end{pmatrix}\\) a la circunferencia unidad? ¿Cuáles son sus valores singulares?",
  "En la elipse de semiejes \\(3\\) (sobre \\(x\\)) y \\(1\\) (sobre \\(y\\)). Los valores singulares son \\(3\\) y \\(1\\)."),
 (2, "Hacé lo mismo con \\(A=\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}\\). ¿En qué direcciones quedan los ejes de la elipse?",
  "Semiejes \\(3\\) en la dirección \\((1,1)\\) y \\(1\\) en la dirección \\((1,-1)\\). Como \\(A\\) es simétrica con autovalores positivos, los valores singulares son sus autovalores."),
 (2, "Calculá los valores singulares de la cizalla \\(A=\\begin{pmatrix}1&1\\\\0&1\\end{pmatrix}\\) y comprobá que su producto es \\(|\\det A|\\).",
  f"\\(\\sigma_1\\approx{n(s3[0],3)}\\) y \\(\\sigma_2\\approx{n(s3[1],3)}\\), que son \\(\\sqrt{{(3\\pm\\sqrt5)/2}}\\). El producto es \\(1=\\det A\\): la cizalla no cambia áreas."),
 (2, "La incertidumbre de un punto medido tiene matriz de covarianza \\(\\Sigma_{EN}=\\begin{pmatrix}4&1{,}5\\\\1{,}5&1\\end{pmatrix}\\) cm\\(^2\\), en \\((E,N)\\). Calculá los semiejes de la elipse de error (las raíces de los autovalores) y el acimut del eje mayor.",
  f"Semiejes \\(\\approx{n(semi[0],2)}\\) cm y \\(\\approx{n(semi[1],2)}\\) cm. El eje mayor forma \\({ang(thE,1)}\\) con el este: acimut \\({ang(azE,1)}\\)."),
 (3, "Para \\(A=\\begin{pmatrix}1&1\\\\1&1{,}01\\end{pmatrix}\\), calculá los valores singulares y su cociente. ¿Qué forma tiene la elipse? ¿Qué pasa si resolvés \\(Ax=b\\) con datos que tienen un poco de error?",
  f"\\(\\sigma_1\\approx{n(s8[0],3)}\\) y \\(\\sigma_2\\approx{n(s8[1],4)}\\), con cociente \\(\\approx{n(s8[0]/s8[1],0)}\\). La elipse es casi un segmento: el plano casi se aplasta. Un error relativo chico en \\(b\\) puede convertirse en un error relativo hasta unas {n(s8[0]/s8[1],0)} veces mayor en \\(x\\)."),
])

# ---------------------------------------------------------------- 9 Cambio de base
Eo = 1000 + 20 * math.cos(D(30)) - 10 * math.sin(D(30)); No = 500 + 20 * math.sin(D(30)) + 10 * math.cos(D(30))
A9 = np.array([[4, 1], [2, 3]]); A9_5 = np.linalg.matrix_power(A9, 5)
Rf = refl_linea(30)
C[9] = ("Cambio de base: las coordenadas son etiquetas", [
 (1, "Escribí \\(v=(5,5)\\) en la base \\(b_1=(3,1)\\), \\(b_2=(1,2)\\).",
  "\\(v=1\\,b_1+2\\,b_2\\): las coordenadas son \\((1,2)\\)."),
 (2, "En una obra, el eje \\(x\\) forma \\(30^\\circ\\) con el este (en sentido antihorario) y el origen está en \\((E,N)=(1000;\\ 500)\\) m. Un punto tiene coordenadas de obra \\((20,10)\\) m. ¿Cuáles son sus coordenadas \\((E,N)\\)?",
  f"\\(E={n(Eo)}\\) m y \\(N={n(No)}\\) m: se gira \\((20,10)\\) un ángulo de \\(30^\\circ\\) y se le suma el origen."),
 (2, "Diagonalizá \\(A=\\begin{pmatrix}4&1\\\\2&3\\end{pmatrix}\\) y usá \\(A=CDC^{-1}\\) para calcular \\(A^5\\).",
  f"\\(\\lambda=5\\) con \\((1,1)\\) y \\(\\lambda=2\\) con \\((1,-2)\\). \\(A^5=C\\,\\mathrm{{diag}}(3125,32)\\,C^{{-1}}=\\begin{{pmatrix}}{A9_5[0,0]}&{A9_5[0,1]}\\\\{A9_5[1,0]}&{A9_5[1,1]}\\end{{pmatrix}}\\)."),
 (2, "La reflexión en la recta que forma \\(30^\\circ\\) con el eje \\(x\\), en una base alineada con esa recta y su perpendicular, es \\(\\mathrm{diag}(1,-1)\\). Pasala a la base canónica.",
  f"\\(\\begin{{pmatrix}}\\cos60^\\circ&\\sin60^\\circ\\\\\\sin60^\\circ&-\\cos60^\\circ\\end{{pmatrix}}=\\begin{{pmatrix}}{n(Rf[0,0],3)}&{n(Rf[0,1],3)}\\\\{n(Rf[1,0],3)}&{n(Rf[1,1],3)}\\end{{pmatrix}}\\)."),
 (3, "La forma \\(\\omega=(2,1)\\) está escrita en la base canónica. Escribila en la base \\(b_1=(3,1)\\), \\(b_2=(1,2)\\), calculando \\(\\omega(b_1)\\) y \\(\\omega(b_2)\\). Comprobá que \\(\\omega(v)\\) da lo mismo en las dos bases, con \\(v=(5,5)\\) del problema 1.",
  "\\([\\omega]_b=(7,4)\\). En la base canónica, \\(\\omega(5,5)=15\\). En la base \\(b\\), \\((7,4)\\cdot(1,2)=15\\). El valor no depende de la base."),
])

# ---------------------------------------------------------------- 10 Derivada
dE, dN = -120.0, 50.0; d = math.hypot(dE, dN); azp = G(math.atan2(dE, dN)) % 360
sAz = dN / d**2 * 0.01; sAz_s = G(sAz) * 3600
ex = math.hypot(3.02, 3.97); ap = 5 + 0.6 * 0.02 + 0.8 * (-0.03)
H = np.array([[2, 3], [3, 2]]); mu = np.linalg.eigvalsh(H)[::-1]
C[10] = ("La derivada como aproximación lineal: jacobiano, gradiente y hessiana", [
 (1, "Calculá el jacobiano de \\((r,\\theta)\\mapsto(r\\cos\\theta,\\ r\\sin\\theta)\\) en \\(r=10\\), \\(\\theta=30^\\circ\\), y su determinante. ¿Qué dice ese número sobre las áreas?",
  f"\\(J=\\begin{{pmatrix}}\\cos\\theta&-r\\sin\\theta\\\\\\sin\\theta&r\\cos\\theta\\end{{pmatrix}}=\\begin{{pmatrix}}{n(math.cos(D(30)),3)}&{n(-10*math.sin(D(30)),0)}\\\\{n(math.sin(D(30)),1)}&{n(10*math.cos(D(30)),2)}\\end{{pmatrix}}\\), con \\(\\det J=r=10\\): un rectangulito \\(dr\\,d\\theta\\) se convierte en un área \\(10\\) veces mayor."),
 (2, "Desde una estación, un punto está en \\(\\Delta E=-120\\) m, \\(\\Delta N=50\\) m. Calculá la distancia y el acimut. Si el punto se corre \\(1\\) cm al este, ¿cuánto cambian la distancia y el acimut? Usá el jacobiano de \\(\\mathrm{Pol}\\).",
  f"\\(d={n(d,0)}\\) m y \\(\\mathrm{{Az}}\\approx{ang(azp)}\\). La distancia cambia \\(\\Delta E/d\\cdot1\\) cm \\(\\approx{n(dE/d,3)}\\) cm. El acimut cambia \\(\\Delta N/d^2\\cdot0{{,}}01\\) m \\(\\approx{n(sAz*1e5,2)}\\cdot10^{{-5}}\\) rad, unos \\({n(sAz_s,1)}''\\)."),
 (2, "Aproximá \\(\\sqrt{x^2+y^2}\\) en \\((3{,}02;\\ 3{,}97)\\) con su aproximación lineal en \\((3,4)\\) y compará con el valor exacto.",
  f"Con el gradiente \\((0{{,}}6;\\ 0{{,}}8)\\) en \\((3,4)\\): \\(5+0{{,}}6\\cdot0{{,}}02+0{{,}}8\\cdot(-0{{,}}03)={n(ap,3)}\\). El valor exacto es \\({n(ex,5)}\\)."),
 (2, "Un terreno tiene cota \\(z=100-0{,}002\\,x^2-0{,}001\\,y^2\\). En el punto \\((100,50)\\), ¿hacia dónde corre el agua y con qué pendiente?",
  f"\\(\\nabla z=(-0{{,}}4;\\ -0{{,}}1)\\). El agua corre hacia \\(-\\nabla z=(0{{,}}4;\\ 0{{,}}1)\\), con pendiente \\(\\lVert\\nabla z\\rVert\\approx{n(math.hypot(.4,.1),3)}\\), un {n(math.hypot(.4,.1)*100,1)}\\,\\%."),
 (3, "Para \\(h(x,y)=x^2+3xy+y^2\\), calculá la hessiana en el origen y sus autovalores \\(\\mu_1\\), \\(\\mu_2\\). ¿El origen es un mínimo, un máximo o una silla?",
  f"\\(H=\\begin{{pmatrix}}2&3\\\\3&2\\end{{pmatrix}}\\), con \\(\\mu_1={n(mu[0],0)}\\) y \\(\\mu_2={n(mu[1],0)}\\). Como tienen signos distintos, el origen es una silla: sube en la dirección \\((1,1)\\) y baja en la \\((1,-1)\\)."),
])

# ---------------------------------------------------------------- 11 Inversas
X = np.array([[1, 0], [1, 1], [1, 2]], float); y = np.array([1, 2, 2], float)
coef = np.linalg.lstsq(X, y, rcond=None)[0]; res = y - X @ coef
bb = np.array([1, 2, 2.0]); u = np.array([1, 1, 0.0]); pp = bb @ u / (u @ u) * u
Ap = np.linalg.pinv(np.array([[1, 1], [1, 1.0]])); xp = Ap @ np.array([2, 4.0])
C[11] = ("Inversas y pseudoinversa: los cuatro subespacios", [
 (1, "Calculá la inversa de \\(A=\\begin{pmatrix}2&1\\\\5&3\\end{pmatrix}\\) y comprobá que \\(AA^{-1}=I\\).",
  "\\(\\det A=1\\) y \\(A^{-1}=\\begin{pmatrix}3&-1\\\\-5&2\\end{pmatrix}\\)."),
 (2, "Sea \\(R\\) el giro de \\(90^\\circ\\) y \\(S=\\mathrm{diag}(2,1)\\). La transformación «primero \\(S\\), después \\(R\\)» es \\(RS\\). ¿Cuál es su inversa? Comprobalo con el punto \\((1,1)\\).",
  "\\((RS)^{-1}=S^{-1}R^{-1}\\): primero se deshace el giro y después el estiramiento. \\(RS(1,1)=R(2,1)=(-1,2)\\), y \\(S^{-1}R^{-1}(-1,2)=S^{-1}(2,1)=(1,1)\\)."),
 (2, "Buscá la recta \\(y=a+bx\\) que mejor pasa por \\((0,1)\\), \\((1,2)\\) y \\((2,2)\\), por cuadrados mínimos verticales. Calculá los residuos y comprobá que suman cero.",
  f"\\(a\\approx{n(coef[0],4)}\\) y \\(b={n(coef[1],1)}\\). Los residuos son \\({n(res[0],4)}\\), \\({n(res[1],4)}\\) y \\({n(res[2],4)}\\), y suman \\(0\\)."),
 (2, "Se conoce la altura del punto \\(A\\): \\(10{,}000\\) m. Se mide cuánto más alto está cada punto que el anterior (el desnivel) en un recorrido que vuelve al punto de partida: \\(A\\to B=+1{,}250\\), \\(B\\to C=+0{,}830\\) y \\(C\\to A=-2{,}074\\) m. Si las medidas fueran perfectas, sumarían cero. ¿Por cuánto no cierran? Repartí la diferencia en partes iguales y calculá las alturas de \\(B\\) y \\(C\\).",
  "Suman \\(+0{,}006\\) m. Se corrige \\(-0{,}002\\) en cada tramo: \\(H_B=11{,}248\\) m y \\(H_C=12{,}076\\) m. Son tres ecuaciones para dos incógnitas, y este reparto es justamente la solución de cuadrados mínimos (con las tres medidas igual de confiables)."),
 (3, "\\(A=\\begin{pmatrix}1&1\\\\1&1\\end{pmatrix}\\) no tiene inversa. Calculá su pseudoinversa \\(A^+\\) y la solución \\(x^+=A^+b\\) para \\(b=(2,4)\\). ¿Qué es \\(Ax^+\\)?",
  f"\\(A^+=\\tfrac14\\begin{{pmatrix}}1&1\\\\1&1\\end{{pmatrix}}\\) y \\(x^+={vec(*xp, d=1)}\\). Entonces \\(Ax^+=(3,3)\\), que es la proyección de \\(b\\) sobre la imagen (la recta \\(y=x\\)): la respuesta más cercana posible."),
])

# ---------------------------------------------------------------- 12 Cuatro problemas de ajuste
m = np.array([25.432, 25.428, 25.437]); mm = m.mean()
pts = np.array([(0, 0), (1, 1), (2, 1), (3, 3)], float)
bv = np.polyfit(pts[:, 0], pts[:, 1], 1)[0]
Pc = pts - pts.mean(0); wv, Vv = np.linalg.eigh(Pc.T @ Pc); dv = Vv[:, -1]; bt = dv[1] / dv[0]
s12, th12 = 1.0, G(math.atan2(80, 60)); R12 = rot(th12); g3 = np.array([500, 200]) + R12 @ np.array([50, 50])
cp = np.array([(10, 0), (0, 10), (-10, 0), (0, -9.8)])
M = np.c_[cp, np.ones(4)]; rhs = -(cp**2).sum(1); Dd, Ee, Ff = np.linalg.lstsq(M, rhs, rcond=None)[0]
xc, yc = -Dd / 2, -Ee / 2; rc = math.sqrt(xc**2 + yc**2 - Ff)
C[12] = ("Cuatro problemas de ajuste", [
 (1, "En un calco, dos puntos están en \\((1,0)\\) y \\((0,1)\\); en otro calco del mismo plano, los mismos puntos aparecen en \\((0,1)\\) y \\((-1,0)\\). ¿Qué giro alrededor del origen superpone el primer calco sobre el segundo?",
  "El giro de \\(90^\\circ\\) en sentido antihorario: lleva \\((1,0)\\to(0,1)\\) y \\((0,1)\\to(-1,0)\\). Es el caso más simple de Procrustes: los datos coinciden exactamente y el residuo es cero."),
 (1, "Encontrá la circunferencia que pasa exactamente por \\((0,0)\\), \\((4,0)\\) y \\((0,2)\\), escribiéndola como \\(x^2+y^2+Dx+Ey+F=0\\).",
  "\\(F=0\\), \\(D=-4\\) y \\(E=-2\\): centro \\((2,1)\\) y radio \\(\\sqrt5\\approx2{,}236\\). Con tres puntos no hay nada que ajustar; con más de tres, sí."),
 (2, "Ajustá una recta a \\((0,0)\\), \\((1,1)\\), \\((2,1)\\) y \\((3,3)\\) de dos maneras: midiendo el error en vertical y midiendo el error perpendicular a la recta. Compará las pendientes.",
  f"En vertical, la pendiente es \\({n(bv,2)}\\). En perpendicular (la dirección principal de los puntos centrados), \\(\\approx{n(bt,3)}\\). Distinta forma de medir el error, distinta recta."),
 (2, "Dos puntos tienen coordenadas locales \\((0,0)\\) y \\((100,0)\\), y coordenadas generales \\((500,200)\\) y \\((560,280)\\). Encontrá la escala, el giro y la traslación, y pasá a coordenadas generales el punto local \\((50,50)\\).",
  f"Escala \\({n(s12,0)}\\) (los dos tramos miden \\(100\\)), giro \\({ang(th12)}\\) y traslación \\((500,200)\\). El punto \\((50,50)\\) va a \\({vec(*g3, d=0)}\\)."),
 (3, "Se midieron cuatro puntos del borde de una rotonda, en metros: \\[(10,0),\\quad(0,10),\\quad(-10,0),\\quad(0;\\ -9{,}8).\\] Ajustá una circunferencia escribiéndola como \\(x^2+y^2+Dx+Ey+F=0\\), que es lineal en \\(D\\), \\(E\\) y \\(F\\), y resolviendo por cuadrados mínimos. Calculá el centro y el radio.",
  f"Centro \\(\\approx{vec(xc,yc,d=3)}\\) m y radio \\(\\approx{n(rc,3)}\\) m, con centro \\((-D/2,\\,-E/2)\\) y \\(r=\\sqrt{{D^2/4+E^2/4-F}}\\)."),
])

# ---------------------------------------------------------------- 13 Curvatura
k50 = 0.01 / (1 + 0.25) ** 1.5
k30 = 0.02 * math.cos(D(30))**2 + 0.005 * math.sin(D(30))**2
C[13] = ("Curvatura como forma cuadrática", [
 (1, "¿Qué curvatura tiene una ruta recta? ¿Y una rotonda de \\(20\\) m de radio?",
  "Cero, y \\(1/20=0{,}05\\) m\\(^{-1}\\)."),
 (2, "Un camino sigue el perfil \\(y=x^2/200\\) (en metros). Calculá la curvatura y el radio en \\(x=0\\) y en \\(x=50\\).",
  f"En \\(x=0\\): \\(\\kappa=0{{,}}01\\) m\\(^{{-1}}\\) y \\(R=100\\) m. En \\(x=50\\): \\(\\kappa=y''/(1+y'^2)^{{3/2}}\\approx{n(k50,5)}\\) m\\(^{{-1}}\\) y \\(R\\approx{n(1/k50,1)}\\) m."),
 (2, "Cerca de su punto más bajo, una superficie es \\(z=\\frac{x^2}{2\\cdot50}+\\frac{y^2}{2\\cdot200}\\). Calculá las curvaturas principales, la curvatura de Gauss y, con la fórmula de Euler, la curvatura en la dirección que forma \\(30^\\circ\\) con el eje \\(x\\).",
  f"\\(\\kappa_1=0{{,}}02\\) y \\(\\kappa_2=0{{,}}005\\) m\\(^{{-1}}\\). \\(K=\\kappa_1\\kappa_2=10^{{-4}}\\) m\\(^{{-2}}\\). A \\(30^\\circ\\): \\(\\kappa_1\\cos^2+\\kappa_2\\sin^2={n(k30,5)}\\) m\\(^{{-1}}\\)."),
 (2, "La silla \\(z=xy/100\\): calculá las curvaturas principales en el origen y sus direcciones. ¿Qué signo tiene la curvatura de Gauss?",
  "La hessiana es \\(\\begin{pmatrix}0&0{,}01\\\\0{,}01&0\\end{pmatrix}\\). Las curvaturas son \\(\\pm0{,}01\\) m\\(^{-1}\\), en las direcciones \\((1,1)\\) (sube) y \\((1,-1)\\) (baja). \\(K=-10^{-4}<0\\): es una silla."),
 (3, "Sobre una esfera de radio \\(R=6371\\) km se corta con un plano que contiene una recta tangente y forma \\(60^\\circ\\) con la normal. ¿Qué radio tiene la circunferencia del corte? (Fórmula de Meusnier.)",
  f"\\(r=R\\cos60^\\circ={n(6371*0.5,1)}\\) km: la curvatura del corte es la normal dividida por \\(\\cos60^\\circ\\)."),
])

# ---------------------------------------------------------------- 14 Elipsoide (GRS80)
aa = 6378137.0; f = 1 / 298.257222101; e2 = 2 * f - f * f; bsem = aa * (1 - f)
def MN(phi):
    s = math.sin(D(phi)); w = math.sqrt(1 - e2 * s * s)
    return aa * (1 - e2) / w**3, aa / w
Mm, Nm = MN(-32.89)
M0, _ = MN(0); M60, _ = MN(60)
_, Nb = MN(-34.6); _, Nu = MN(-54.8); par = Nu * math.cos(D(-54.8))
ph, la, hh = D(-34.6), D(-58.4), 25.0
Xc = (Nb + hh) * math.cos(ph) * math.cos(la); Yc = (Nb + hh) * math.cos(ph) * math.sin(la); Zc = (Nb * (1 - e2) + hh) * math.sin(ph)
C[14] = ("Geometría del elipsoide", [
 (1, "Para el elipsoide GRS80 (\\(a=6\\,378\\,137\\) m, \\(1/f=298{,}257222101\\)), calculá el semieje menor \\(b\\) y la excentricidad al cuadrado \\(e^2=2f-f^2\\).",
  f"\\(b={n(bsem,3)}\\) m y \\(e^2\\approx{n(e2,8)}\\)."),
 (2, "Calculá los radios de curvatura \\(M\\) (en el meridiano) y \\(N\\) (en el primer vertical) en la latitud de Mendoza, \\(\\varphi=-32{,}89^\\circ\\). ¿En qué dirección es más curva la Tierra ahí?",
  f"\\(M\\approx{n(Mm,0)}\\) m y \\(N\\approx{n(Nm,0)}\\) m. Como \\(M<N\\), es más curva en dirección norte-sur."),
 (2, "¿Cuánto mide un grado de latitud en el ecuador y a \\(60^\\circ\\) de latitud? (Un grado de meridiano mide \\(M\\,\\pi/180\\).)",
  f"En el ecuador, \\(\\approx{n(M0*math.pi/180,0)}\\) m. A \\(60^\\circ\\), \\(\\approx{n(M60*math.pi/180,0)}\\) m. Hacia el polo la Tierra es más chata, y el grado se alarga."),
 (2, "En Ushuaia (\\(\\varphi=-54{,}8^\\circ\\)), calculá el radio del paralelo (\\(N\\cos\\varphi\\)) y cuánto mide un grado de longitud. ¿Qué fracción es de lo que mide en el ecuador?",
  f"Radio del paralelo \\(\\approx{n(par,0)}\\) m. Un grado de longitud mide \\(\\approx{n(par*math.pi/180,0)}\\) m, un {n(par/aa*100,1)}\\,\\% de lo que mide en el ecuador (\\({n(aa*math.pi/180,0)}\\) m)."),
 (3, "Pasá a coordenadas cartesianas geocéntricas el punto \\(\\varphi=-34{,}6^\\circ\\), \\(\\lambda=-58{,}4^\\circ\\), \\(h=25\\) m. Usá \\(X=(N+h)\\cos\\varphi\\cos\\lambda\\), \\(Y=(N+h)\\cos\\varphi\\sin\\lambda\\), \\(Z=(N(1-e^2)+h)\\sin\\varphi\\).",
  f"\\(X\\approx{n(Xc,0)}\\) m, \\(Y\\approx{n(Yc,0)}\\) m y \\(Z\\approx{n(Zc,0)}\\) m."),
])

# ---------------------------------------------------------------- 15 Esfera
Rk = 6371.0
def dist_az(p1, l1, p2, l2):
    p1, l1, p2, l2 = map(D, (p1, l1, p2, l2))
    c = math.sin(p1) * math.sin(p2) + math.cos(p1) * math.cos(p2) * math.cos(l2 - l1)
    s = math.acos(c)
    az = math.atan2(math.sin(l2 - l1) * math.cos(p2), math.cos(p1) * math.sin(p2) - math.sin(p1) * math.cos(p2) * math.cos(l2 - l1))
    return s * Rk, G(az) % 360
dBM, azBM = dist_az(-34.6, -58.4, 40.4, -3.7)
eps = 3500 / (Rk * 1000) ** 2; eps_s = G(eps) * 3600
k72 = 1 / math.cos(D(72))
C[15] = ("Coordenadas sobre la esfera y trigonometría esférica", [
 (1, "En una esfera de radio \\(6371\\) km, ¿cuánto mide el arco del ecuador entre las longitudes \\(0^\\circ\\) y \\(90^\\circ\\)?",
  f"Un cuarto de circunferencia: \\(\\pi R/2\\approx{n(math.pi*Rk/2,1)}\\) km."),
 (2, "Un triángulo tiene un vértice en el polo y dos en el ecuador, separados \\(60^\\circ\\) de longitud. ¿Cuánto valen sus tres ángulos? Calculá su exceso esférico y su área. ¿Qué fracción de la esfera es?",
  "Dos ángulos rectos en el ecuador y \\(60^\\circ\\) en el polo: suman \\(240^\\circ\\). El exceso es \\(60^\\circ=\\pi/3\\) rad y el área, \\(\\varepsilon R^2=\\tfrac{\\pi}{3}R^2\\): un doceavo de la esfera (\\(4\\pi R^2\\))."),
 (2, "Tomando la Tierra como esfera de \\(6371\\) km, calculá la distancia por el camino más corto entre Buenos Aires (\\(-34{,}6^\\circ\\); \\(-58{,}4^\\circ\\)) y Madrid (\\(40{,}4^\\circ\\); \\(-3{,}7^\\circ\\)), y el acimut con el que hay que salir.",
  f"\\(\\approx{n(dBM,0)}\\) km, saliendo con acimut \\(\\approx{ang(azBM,1)}\\). Ese acimut cambia a lo largo del camino."),
 (2, "Un triángulo rectángulo dibujado en una cancha tiene catetos de \\(100\\) y \\(70\\) m. ¿Cuál es su exceso esférico, en segundos de arco?",
  f"\\(\\varepsilon=\\text{{área}}/R^2\\approx{n(eps*1e11,1)}\\cdot10^{{-11}}\\) rad, unos \\({n(eps_s*1e5,1)}\\cdot10^{{-5}}\\,''\\). Es despreciable: en la cancha, los ángulos suman \\(180^\\circ\\) a todos los efectos."),
 (3, "En la proyección de Mercator, el factor de escala en la latitud \\(\\varphi\\) es \\(1/\\cos\\varphi\\). ¿Cuánto se agrandan las distancias y las áreas a \\(72^\\circ\\) de latitud, en el centro de Groenlandia, respecto del ecuador?",
  f"Las distancias se agrandan \\(\\approx{n(k72,2)}\\) veces y las áreas \\(\\approx{n(k72**2,1)}\\) veces. Por eso Groenlandia parece casi tan grande como África."),
])

NIV = {1: "{\\star}", 2: "{\\star}{\\star}", 3: "{\\star}{\\star}{\\star}"}
NIVH = {1: "★", 2: "★★", 3: "★★★"}


import re
UNI = re.compile(r"\\\) (m|cm|mm|km)\b")


def nb(t):
    return UNI.sub(lambda m: "\\)~" + m.group(1), t)


def tex(salida):
    d = pathlib.Path(salida); (d / "problemas").mkdir(parents=True, exist_ok=True)
    resp = ["% Apéndice: respuestas de los problemas. Generado por tools/problemas/gen.py; no editar a mano.",
            "\\section{Respuestas de los problemas}\\label{cap:respuestas}\\label{ap:respuestas}", "",
            "Los problemas de cada capítulo están graduados: \\(\\star\\) directo, \\(\\star\\star\\) para pensar, "
            "\\(\\star\\star\\star\\) desafío. Todos los valores de estas respuestas se calcularon con "
            "\\file{tools/problemas/gen.py}.", ""]
    for cap, (tit, pbs) in C.items():
        L = [f"% Problemas del capítulo {cap}. Generado por tools/problemas/gen.py; no editar a mano.",
             f"\\section{{Problemas}}\\label{{sec:problemas-{cap:02d}}}", "",
             "Graduados: \\(\\star\\) directo, \\(\\star\\star\\) para pensar, \\(\\star\\star\\star\\) desafío. "
             "Las respuestas están en el apéndice~\\ref{ap:respuestas}; conviene intentarlos antes de mirarlas.", ""]
        resp += [f"\\paragraph{{Capítulo {cap}: {tit}.}}", "\\begin{itemize}"]
        for i, (nv, en, rs) in enumerate(pbs, 1):
            L += [f"\\begin{{problema}}[\\({NIV[nv]}\\)]\\label{{pb:{cap:02d}-{i}}}", nb(en), "\\end{problema}", ""]
            resp.append(f"  \\item[\\ref{{pb:{cap:02d}-{i}}}] {nb(rs)}")
        resp += ["\\end{itemize}", ""]
        (d / "problemas" / f"p{cap:02d}.tex").write_text("\n".join(L), encoding="utf-8")
    (d / "ap6-respuestas.tex").write_text("\n".join(resp), encoding="utf-8")


def html_out(ruta):
    a = ['<!doctype html><html lang="es"><meta charset="utf-8"><title>Problemas por capítulo</title>',
         '<link rel="stylesheet" href="katex/katex.min.css"><script src="katex/katex.min.js"></script>',
         '<script src="katex/auto-render.min.js"></script>',
         '<style>body{font-family:"DejaVu Serif",serif;max-width:860px;margin:2em auto;padding:0 1em;color:#1d2327;line-height:1.5}'
         'h1{color:#0f4c5c}h2{color:#0f4c5c;border-bottom:1px solid #c9d3d6;margin-top:1.6em}'
         '.pb{margin:.8em 0}.nv{color:#8a4a1c;font-size:.9em}details{margin:.3em 0 0 1.2em;color:#333}'
         'summary{cursor:pointer;color:#0f4c5c}@media print{details{display:block}details>summary{display:none}}</style>',
         '<h1>Sistemas de Coordenadas: problemas por capítulo</h1>',
         '<p>Cinco problemas por capítulo, graduados: ★ directo, ★★ para pensar, ★★★ desafío. '
         'La respuesta de cada uno se abre debajo. Todos los valores se calcularon con un script.</p>']
    for cap, (tit, pbs) in C.items():
        a.append(f'<h2>Capítulo {cap}: {html.escape(tit)}</h2>')
        for i, (nv, en, rs) in enumerate(pbs, 1):
            a.append(f'<div class="pb"><b>{cap}.{i}</b> <span class="nv">{NIVH[nv]}</span> {en}'
                     f'<details><summary>Respuesta</summary>{rs}</details></div>')
    a.append('<script>renderMathInElement(document.body,{delimiters:[{left:"\\\\(",right:"\\\\)",display:false},{left:"\\\\[",right:"\\\\]",display:true}],'
             'macros:{"\\\\R":"\\\\mathbb{R}"}});</script></html>')
    pathlib.Path(ruta).write_text("\n".join(a), encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=".")
    ap.add_argument("--html", default=None)
    x = ap.parse_args()
    tex(x.salida)
    if x.html:
        html_out(x.html)
    print(sum(len(v[1]) for v in C.values()), "problemas en", len(C), "capítulos")
