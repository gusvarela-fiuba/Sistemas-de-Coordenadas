---
clase: 9
titulo: "Clase 9: derivada, gradiente y jacobiano"
idea: "La derivada es la mejor aproximación lineal local: el gradiente es una forma lineal y el jacobiano de una superficie es una $3\\times2$ cuyo producto $J^TJ$ mide longitudes."
que_se_estudia: ["Derivada como aproximación lineal, de $\\mathbb R$ a $\\mathbb R^n$", "Gradiente como forma lineal y curva de nivel", "Jacobiano, grilla $(u,v)$ sobre una superficie y plano tangente", "Función implícita y superficie paramétrica", "Primera forma fundamental $g=J^TJ$ y hessiana"]
conceptos_previos: ["Formas lineales y curvas de nivel (clase 4)", "Producto vectorial (clase 5)", "Líneas coordenadas (clase 2)", "Cambio de base (clase 8)"]
apunte: ["derivada"]
unidades: ["00_fundamentos", "10_jacobiano_primera_forma"]
animaciones: ["01_dualidad_gradiente"]
ejercicios_sugeridos: ["Calcular $r_\\varphi$, $r_\\lambda$ y $E,F,G$ de la esfera y ver qué pasa en el polo", "Hallar $J$, la normal y la primera forma de $(u,v)\\mapsto(u,v,u^2+v^2)$ en $(1,1)$", "Clasificar el punto crítico de $f=xy$ y de $f=x^2+y^2$ con la hessiana"]
---

# Clase 9: derivada, gradiente y jacobiano

La derivada es la mejor aproximación lineal local: el gradiente es una forma lineal y el jacobiano de una superficie es una $3\times2$ cuyo producto $J^TJ$ mide longitudes.

## Qué se estudia

- Derivada como aproximación lineal, de $\mathbb R$ a $\mathbb R^n$
- Gradiente como forma lineal y curva de nivel
- Jacobiano, grilla $(u,v)$ sobre una superficie y plano tangente
- Función implícita y superficie paramétrica
- Primera forma fundamental $g=J^TJ$ y hessiana

**Derivada como aproximación lineal.** Álgebra: $f(v+\epsilon)\approx f(v)+Df(v)\,\epsilon$. Se ve: zoom en un punto hasta que la curva parece recta, la superficie parece plana. $Df$ es esa recta o ese plano, y es una transformación lineal: entra un pasito, sale un pasito. Escalera: en $\mathbb R$, $f'(x)$ es un número (la pendiente); en $\mathbb R^2\to\mathbb R$, el gradiente: una forma lineal con dos números; en $\mathbb R^2\to\mathbb R^3$, la jacobiana $3\times2$; en general $m\times n$.

**Gradiente.** Álgebra: $\nabla f(p)\,h=\partial_xf\,h_1+\partial_yf\,h_2$, una fila por una columna. Se ve: una regla graduada de rectas paralelas (clase 4); la recta de nivel cero de esa regla, corrida al punto, es la tangente a la curva de nivel de $f$. Ser perpendicular a la curva de nivel es lo mismo que ser el vector de la forma perpendicular a sus rectas de nivel. No es una flecha que vive en la superficie: es la máquina de medir cuánto sube $f$ con cada pasito.

**Jacobiano.** Álgebra: $J=\begin{pmatrix}r_u&r_v\end{pmatrix}$, columnas = derivadas parciales. Se ve: la grilla $(u,v)$ dibujada sobre la superficie como líneas coordenadas (clase 2); en un punto, los pasitos $du$, $dv$ van a $r_u\,du+r_v\,dv$, el plano tangente. El cuadradito $du\times dv$ va a un paralelogramo de lados $r_u$, $r_v$. La normal $r_u\times r_v$ es la dirección inaccesible: lo que la transformación lineal local no alcanza (el espacio inaccesible de la salida de la clase 10).

**Función implícita.** Álgebra: $F(x,y,z)=0$ define $z=g(x,y)$ cerca de $p$ si $\partial_zF(p)\neq0$. Se ve: el gradiente de $F$ (normal a la superficie de nivel) tiene que tener sombra sobre el eje $z$; si la normal está acostada en el plano $xy$, la superficie está de canto vista desde arriba y no es gráfica de ninguna función de $(x,y)$ ahí. En $\mathbb R$: $F(x,y)=0$ define $y=g(x)$ si $\partial_yF\neq0$; la circunferencia falla en $(\pm1,0)$, donde la tangente es vertical.

**Superficie paramétrica.** Álgebra: $r(u,v)$, con $J$ de rango 2 salvo en puntos singulares. Se ve: en el polo, $r_\lambda=0$; la línea coordenada de longitud se contrajo a un punto; la jacobiana pierde una columna y el paralelogramo tangente se aplasta.

**Primera forma fundamental** . Álgebra: $ds^2=E\,du^2+2F\,du\,dv+G\,dv^2$ con $E=r_u\cdot r_u$, $F=r_u\cdot r_v$, $G=r_v\cdot r_v$; en matriz, $g=J^{T}J$. Se ve: la regla para medir longitudes del pasito en la superficie usando sólo los números $(du,dv)$. $E$ y $G$ son los cuadrados de los lados del paralelogramo tangente, $F$ dice si es rectángulo ($F=0$) o no. Con un cambio de coordenadas, $g'=J^{T}gJ$: el mismo patrón que las rotaciones, y el mismo que el cambio de base de la clase 8 pero para una forma cuadrática.

**Hessiana** . Álgebra: $f(p+h)\approx f(p)+\nabla f(p)\,h+\tfrac12\,h^{T}Hh$. Se ve: después del plano tangente, el siguiente término es una forma cuadrática que dice si la gráfica queda arriba del plano (mínimo), abajo (máximo) o lo cruza (silla). Sus autovectores son las direcciones principales de curvatura de la gráfica; sus autovalores, cuánto se curva en cada una. Es la puerta a la curvatura (clase 12).

## Conceptos previos

- Formas lineales y curvas de nivel (clase 4)
- Producto vectorial (clase 5)
- Líneas coordenadas (clase 2)
- Cambio de base (clase 8)

## En el apunte

- La derivada como aproximación lineal: jacobiano, gradiente y hessiana (`cap:derivada`)

## Unidades interactivas

- Fundamentos: cuerpos, grupos, puntos, formas lineales y métrica (el idioma de la materia) (`00_fundamentos`)
- Jacobiano y primera forma fundamental (`10_jacobiano_primera_forma`)

## Animaciones

- `01_dualidad_gradiente`

## Ejercicios sugeridos

- Calcular $r_\varphi$, $r_\lambda$ y $E,F,G$ de la esfera y ver qué pasa en el polo
- Hallar $J$, la normal y la primera forma de $(u,v)\mapsto(u,v,u^2+v^2)$ en $(1,1)$
- Clasificar el punto crítico de $f=xy$ y de $f=x^2+y^2$ con la hessiana
