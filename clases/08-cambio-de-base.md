---
clase: 8
titulo: "Capítulo 9: cambio de base y diagonalización"
idea: "Cambiar de base es medir la misma flecha con otra grilla: se convierten todos los objetos a la vez para que nada cambie."
que_se_estudia: ["Cambio de base: $[v]_{nueva}=C^{-1}[v]_{can}$", "Vectores, formas y transformaciones cambian de base de forma distinta", "Diagonalización $T=CDC^{-1}$ y grilla de autovectores", "Potencias enteras y reales de una matriz: la trayectoria continua $T^t$"]
conceptos_previos: ["Formas lineales y dualidad (capítulo 5)", "Autovectores (capítulo 7)", "SVD (capítulo 8)"]
apunte: ["cambio-base"]
unidades: ["08_cambio_de_base"]
animaciones: ["03_cambio_de_base_viaje"]
ejercicios_sugeridos: ["Diagonalizar $\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$ y calcular $T^5$ por la diagonal", "Calcular $T^{1/2}$ y la trayectoria de $(1,0)$ bajo $T^t$", "Transformar una forma y un vector con $C$ y comprobar que su valor se conserva"]
---

# Capítulo 9: cambio de base y diagonalización

Cambiar de base es medir la misma flecha con otra grilla: se convierten todos los objetos a la vez para que nada cambie.

## Qué se estudia

- Cambio de base: $[v]_{nueva}=C^{-1}[v]_{can}$
- Vectores, formas y transformaciones cambian de base de forma distinta
- Diagonalización $T=CDC^{-1}$ y grilla de autovectores
- Potencias enteras y reales de una matriz: la trayectoria continua $T^t$

**Cambio de base.** Álgebra: $[v]_{\text{nueva}}=C^{-1}[v]_{\text{can}}$ con $C$ = base nueva en columnas (por ejemplo, si la base nueva son los ejes girados un ángulo $\theta$, $C = R(\theta) = \begin{pmatrix}\cos\theta & -\sin\theta \\ \sin\theta & \cos\theta\end{pmatrix}$ y $C^{-1} = R(-\theta) = C^{\mathsf T}$). Se ve: la misma flecha medida con otra grilla. La flecha no se movió; cambiaron los números. Escalera: en $\mathbb R$, cambiar de base es cambiar de unidad (metros a centímetros: el número se multiplica por 100, la longitud no cambia); en $\mathbb R^2$ la grilla puede ser oblicua y con pasos distintos en cada eje; en $\mathbb R^3$ lo mismo con tres direcciones; en $\mathbb R^n$ es una matriz $n\times n$ invertible.

**Los tres tipos de objeto cambian de base distinto.** Al pasar de la base canónica a la nueva (con $C$ la matriz que tiene la base nueva en columnas), los vectores (puntos) cambian con $C^{-1}$ ($[v]_{\text{nueva}}=C^{-1}[v]_{\text{can}}$), las formas lineales (rectas) con $C$ del otro lado ($[\varphi]_{\text{nueva}}=[\varphi]_{\text{can}}C$), y las transformaciones con $C^{-1}\,T\,C$ ($[T]_{\text{nueva}}=C^{-1}\,T\,C$, de modo que $T=C\,[T]_{\text{nueva}}\,C^{-1}$). Se ve: si todo se convierte a la vez, cada punto sigue en su recta y cada transformación sigue llevando cada punto adonde lo llevaba. Se convierte todo para que nada cambie.

**Diagonalización.** Álgebra: $T=C\,D\,C^{-1}$ (o sea $D=C^{-1}\,T\,C$) con $D$ diagonal y $C$ = autovectores en columnas. Se ve: la grilla formada por las curvas de nivel de los autovectores se estira en cada dirección por su autovalor, sin romperse; el cuadrado se vuelve paralelogramo y el paralelogramo de autovectores queda más largo en una dirección y más corto en otra. La transformación no tiene interpretación fácil en la grilla común, pero en la grilla propia es dos estiramientos independientes. Escalera: en $\mathbb R$ toda matriz es diagonal ($a$); en $\mathbb R^2$ hace falta que haya dos direcciones propias reales; una rotación no tiene ninguna y no se diagonaliza en reales (de ahí la SVD, capítulo 8).

**Potencias de matrices.** Álgebra: $T^n=C\,D^n\,C^{-1}$, y si los autovalores son positivos, $T^t=C\,D^t\,C^{-1}$ para $t$ real. Se ve: aplicar $n$ veces es estirar $n$ veces cada eje propio; $t$ real convierte la transformación en una película y el punto recorre una trayectoria continua. La transformación se identifica con la trayectoria que genera. Es la misma jugada de ir a lo chico para volver a lo grande de la exponencial de matrices (capítulo 1), ahora con autovalores reales en lugar de giros.

## Conceptos previos

- Formas lineales y dualidad (capítulo 5)
- Autovectores (capítulo 7)
- SVD (capítulo 8)

## En el apunte

- Capítulo 9. Cambio de base: las coordenadas son etiquetas

## Unidades interactivas

- Cambio de base y diagonalización (`08_cambio_de_base`)

## Animaciones

- `03_cambio_de_base_viaje`

## Ejercicios sugeridos

- Diagonalizar $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ y calcular $T^5$ por la diagonal
- Calcular $T^{1/2}$ y la trayectoria de $(1,0)$ bajo $T^t$
- Transformar una forma y un vector con $C$ y comprobar que su valor se conserva

## En el CAD

- [`UCS` alineado con el frente: las coordenadas cambian con $C^{-1}$](../cad/#cap9)
