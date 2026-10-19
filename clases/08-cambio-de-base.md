---
clase: 8
titulo: "Clase 8: cambio de base y diagonalización"
idea: "Cambiar de base es medir la misma flecha con otra grilla: se convierten todos los objetos a la vez para que nada cambie."
que_se_estudia: ["Cambio de base: $[v]_{nueva}=C^{-1}[v]_{can}$", "Vectores, formas y transformaciones cambian de base de forma distinta", "Diagonalización $T=ADA^{-1}$ y grilla de autovectores", "Potencias enteras y reales de una matriz: la trayectoria continua $A^t$"]
conceptos_previos: ["Formas lineales y dualidad (clase 4)", "Autovectores (clase 6)", "SVD (clase 7)"]
apunte: ["cambio-base"]
unidades: ["08_cambio_de_base"]
animaciones: ["03_cambio_de_base_viaje"]
ejercicios_sugeridos: ["Diagonalizar $\\begin{pmatrix}2&1\\\\1&2\\end{pmatrix}$ y calcular $A^5$ por la diagonal", "Calcular $A^{1/2}$ y la trayectoria de $(1,0)$ bajo $A^t$", "Transformar una forma y un vector con $T$ y comprobar que su valor se conserva"]
---

# Clase 8: cambio de base y diagonalización

Cambiar de base es medir la misma flecha con otra grilla: se convierten todos los objetos a la vez para que nada cambie.

## Qué se estudia

- Cambio de base: $[v]_{nueva}=C^{-1}[v]_{can}$
- Vectores, formas y transformaciones cambian de base de forma distinta
- Diagonalización $T=ADA^{-1}$ y grilla de autovectores
- Potencias enteras y reales de una matriz: la trayectoria continua $A^t$

**Cambio de base.** Álgebra: $[v]_{\text{nueva}}=C^{-1}[v]_{\text{can}}$ con $C$ = base nueva en columnas. Se ve: la misma flecha medida con otra grilla. La flecha no se movió; cambiaron los números. Escalera: en $\mathbb R$, cambiar de base es cambiar de unidad (metros a centímetros: el número se multiplica por 100, la longitud no cambia); en $\mathbb R^2$ la grilla puede ser oblicua y con pasos distintos en cada eje; en $\mathbb R^3$ lo mismo con tres direcciones; en $\mathbb R^n$ es una matriz $n\times n$ invertible.

**Los tres tipos de objeto cambian de base distinto.** Vectores (puntos) con $A$, formas lineales (rectas) con $A^{-1}$ del otro lado, transformaciones con $A\,T\,A^{-1}$. Se ve: si todo se convierte a la vez, cada punto sigue en su recta y cada transformación sigue llevando cada punto adonde lo llevaba. Se convierte todo para que nada cambie.

**Diagonalización.** Álgebra: $T=A\,D\,A^{-1}$ con $D$ diagonal y $A$ = autovectores en columnas. Se ve: la grilla formada por las curvas de nivel de los autovectores se estira en cada dirección por su autovalor, sin romperse; el cuadrado se vuelve paralelogramo y el paralelogramo de autovectores queda más largo en una dirección y más corto en otra. La transformación no tiene interpretación fácil en la grilla común, pero en la grilla propia es dos estiramientos independientes. Escalera: en $\mathbb R$ toda matriz es diagonal ($a$); en $\mathbb R^2$ hace falta que haya dos direcciones propias reales; una rotación no tiene ninguna y no se diagonaliza en reales (de ahí la SVD, clase 7).

**Potencias de matrices.** Álgebra: $T^n=A\,D^n\,A^{-1}$, y si los autovalores son positivos, $T^t=A\,D^t\,A^{-1}$ para $t$ real. Se ve: aplicar $n$ veces es estirar $n$ veces cada eje propio; $t$ real convierte la transformación en una película y el punto recorre una trayectoria continua. La transformación se identifica con la trayectoria que genera. Es la misma jugada de ir a lo chico para volver a lo grande de la exponencial de matrices (clase 1), ahora con autovalores reales en lugar de giros.

## Conceptos previos

- Formas lineales y dualidad (clase 4)
- Autovectores (clase 6)
- SVD (clase 7)

## En el apunte

- Cambio de base: las coordenadas son etiquetas (`cap:cambio-base`)

## Unidades interactivas

- Cambio de base y diagonalización (`08_cambio_de_base`)

## Animaciones

- `03_cambio_de_base_viaje`

## Ejercicios sugeridos

- Diagonalizar $\begin{pmatrix}2&1\\1&2\end{pmatrix}$ y calcular $A^5$ por la diagonal
- Calcular $A^{1/2}$ y la trayectoria de $(1,0)$ bajo $A^t$
- Transformar una forma y un vector con $T$ y comprobar que su valor se conserva
