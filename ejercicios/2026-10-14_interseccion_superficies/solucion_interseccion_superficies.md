# Problema: Intersección de Superficies y Recta Tangente Paralela a un Plano

## Enunciado
Dadas las superficies:
1. **Superficie $S_1$ (Paraboloide circular):**
   $$x^2 + y^2 + z = 1$$
2. **Superficie $S_2$ (Plano vertical):**
   $$x + y = 1$$

Ambas superficies se intersecan determinando una curva $C = S_1 \cap S_2$.

**Objetivo:** Encontrar el punto $P(x, y, z) \in C$ donde la recta tangente a $C$ sea paralela al plano:
$$\pi: x - z = 0$$

---

## Solución Paso a Paso

### 1. Parametrización de la curva $C$
De la ecuación del plano $S_2$, despejamos $y$:
$$y = 1 - x$$

Sustituyendo esta expresión en la ecuación del paraboloide $S_1$:
$$x^2 + (1 - x)^2 + z = 1$$
$$x^2 + (1 - 2x + x^2) + z = 1$$
$$2x^2 - 2x + 1 + z = 1$$
$$z = 2x - 2x^2$$

Tomando como parámetro $x = t$, obtenemos la función vectorial de la curva $C$:
$$\mathbf{r}(t) = \left(t,\; 1 - t,\; 2t - 2t^2\right), \quad t \in \mathbb{R}$$

---

### 2. Vector Tangente a la Curva $C$
El vector tangente se obtiene derivando $\mathbf{r}(t)$ respecto al parámetro $t$:
$$\mathbf{T}(t) = \mathbf{r}'(t) = \frac{d}{dt}\left(t,\; 1 - t,\; 2t - 2t^2\right)$$
$$\mathbf{T}(t) = (1,\; -1,\; 2 - 4t)$$

---

### 3. Condición Geométrica de Paralelismo
El plano de referencia es:
$$\pi: x - z = 0 \iff 1\cdot x + 0\cdot y - 1\cdot z = 0$$

Su vector normal es:
$$\mathbf{n}_\pi = (1,\; 0,\; -1)$$

> **Condición:** Una recta con vector director $\mathbf{T}$ es paralela a un plano $\pi$ con vector normal $\mathbf{n}_\pi$ si y solo si $\mathbf{T}$ es ortogonal a $\mathbf{n}_\pi$:
> $$\mathbf{T}(t) \cdot \mathbf{n}_\pi = 0$$

Calculamos el producto escalar:
$$(1)(1) + (-1)(0) + (2 - 4t)(-1) = 0$$
$$1 - (2 - 4t) = 0$$
$$1 - 2 + 4t = 0$$
$$-1 + 4t = 0 \implies t = \frac{1}{4}$$

---

### 4. Coordenadas del Punto $P$
Evaluando el parámetro $t = \frac{1}{4}$ en la parametrización $\mathbf{r}(t)$:

- **Coordenada $x$:**
  $$x = \frac{1}{4}$$

- **Coordenada $y$:**
  $$y = 1 - \frac{1}{4} = \frac{3}{4}$$

- **Coordenada $z$:**
  $$z = 2\left(\frac{1}{4}\right) - 2\left(\frac{1}{4}\right)^2 = \frac{1}{2} - \frac{1}{8} = \frac{3}{8}$$

Por lo tanto, el punto buscado es:
$$\mathbf{P = \left(\frac{1}{4},\; \frac{3}{4},\; \frac{3}{8}\right)}$$

---

## Verificación

1. **Pertenencia a $S_1$ (Paraboloide):**
   $$x^2 + y^2 + z = \left(\frac{1}{4}\right)^2 + \left(\frac{3}{4}\right)^2 + \frac{3}{8} = \frac{1}{16} + \frac{9}{16} + \frac{6}{16} = \frac{16}{16} = 1 \quad \checkmark$$

2. **Pertenencia a $S_2$ (Plano):**
   $$x + y = \frac{1}{4} + \frac{3}{4} = 1 \quad \checkmark$$

3. **Dirección de la tangente:**
   $$\mathbf{T}\left(\frac{1}{4}\right) = (1,\; -1,\; 2 - 4(1/4)) = (1,\; -1,\; 1)$$
   $$\mathbf{T} \cdot \mathbf{n}_\pi = (1)(1) + (-1)(0) + (1)(-1) = 1 - 1 = 0 \quad \checkmark$$

---

## Método Alternativo: Gradientes y Producto Vectorial

Definimos las superficies de nivel:
- $F(x, y, z) = x^2 + y^2 + z - 1 = 0 \implies \nabla F = (2x,\; 2y,\; 1)$
- $G(x, y, z) = x + y - 1 = 0 \implies \nabla G = (1,\; 1,\; 0)$

El vector tangente a la curva de intersección $C$ en cualquier punto viene dado por el producto cruz de las normales:
$$\mathbf{T} \propto \nabla F \times \nabla G = \begin{vmatrix} \mathbf{i} & \mathbf{j} & \mathbf{k} \\ 2x & 2y & 1 \\ 1 & 1 & 0 \end{vmatrix} = (-1,\; 1,\; 2x - 2y)$$

Imponiendo la perpendicularidad con $\mathbf{n}_\pi = (1, 0, -1)$:
$$\mathbf{T} \cdot \mathbf{n}_\pi = 0 \implies (-1)(1) + (1)(0) + (2x - 2y)(-1) = 0$$
$$-1 - (2x - 2y) = 0 \implies 2y - 2x = 1$$

Como además el punto pertenece a $x + y = 1 \implies y = 1 - x$:
$$2(1 - x) - 2x = 1 \implies 2 - 4x = 1 \implies 4x = 1 \implies x = \frac{1}{4}$$
Lo cual conduce idénticamente a:
$$y = \frac{3}{4}, \quad z = \frac{3}{8}$$
