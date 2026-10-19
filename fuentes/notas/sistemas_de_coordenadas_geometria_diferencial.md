---
title: Sistemas de coordenadas sobre superficies
---

# Sistemas de Coordenadas

**Idea central.** Una superficie en 3D se describe con dos parámetros $u$ y $v$; cada par $(u, v)$ da un punto de la superficie. En la Tierra: $u$ = latitud, $v$ = longitud.

## 1. Vectores tangentes

$$
\mathbf{r}_u = \frac{\partial \mathbf{r}}{\partial u}, \qquad \mathbf{r}_v = \frac{\partial \mathbf{r}}{\partial v}
$$

Estos dos vectores definen el **plano tangente** a la superficie en el punto.

## 2. El pasito

$$
d\mathbf{r} = \mathbf{r}_u\, du + \mathbf{r}_v\, dv
$$

$du$ y $dv$ son escalares (cuánto me muevo en cada parámetro); $\mathbf{r}_u$ y $\mathbf{r}_v$ son vectores (hacia dónde me lleva cada parámetro).

## 3. Primera forma fundamental

$$
ds^2 = \langle d\mathbf{r}, d\mathbf{r} \rangle = E\, du^2 + 2F\, du\, dv + G\, dv^2
$$

con

- $E = \langle \mathbf{r}_u, \mathbf{r}_u \rangle$: longitud² en la dirección $u$.
- $F = \langle \mathbf{r}_u, \mathbf{r}_v \rangle$: ángulo entre las direcciones; vale 0 si son perpendiculares.
- $G = \langle \mathbf{r}_v, \mathbf{r}_v \rangle$: longitud² en la dirección $v$.

## 4. Tensor métrico

$$
g = \begin{pmatrix} E & F \\ F & G \end{pmatrix}
$$

El tensor métrico codifica toda la geometría local de la superficie.

## 5. Esfera

$$
\mathbf{r}(\varphi, \lambda) = (R \sin\varphi \cos\lambda,\; R \sin\varphi \sin\lambda,\; R \cos\varphi)
$$

$$
ds^2 = R^2\, d\varphi^2 + R^2 \sin^2\varphi\, d\lambda^2
$$

$E = R^2$, $F = 0$, $G = R^2 \sin^2\varphi$.

**1° de longitud vale** ($R = 6371$ km, $1° = 0.01745$ rad):

| Lugar | Latitud | 1° de longitud |
|---|---|---|
| Ecuador | 0° | 111 km |
| Buenos Aires | 34° | 62 km |
| Oslo | 60° | 55 km |
| Polo Norte | 90° | 0 km |

## 6. Matrices de rotación

$$
R_x(\alpha) = \begin{pmatrix} 1 & 0 & 0 \\ 0 & \cos\alpha & -\sin\alpha \\ 0 & \sin\alpha & \cos\alpha \end{pmatrix}
$$

$$
R_y(\alpha) = \begin{pmatrix} \cos\alpha & 0 & \sin\alpha \\ 0 & 1 & 0 \\ -\sin\alpha & 0 & \cos\alpha \end{pmatrix}
$$

$$
R_z(\alpha) = \begin{pmatrix} \cos\alpha & -\sin\alpha & 0 \\ \sin\alpha & \cos\alpha & 0 \\ 0 & 0 & 1 \end{pmatrix}
$$

**Regla:** cada una es la rotación 2D empotrada en 3D, con un $1$ en la diagonal para el eje que queda quieto.

## 7. Por qué el orden importa

Con $\alpha$ grande, $R_x \cdot R_y \neq R_y \cdot R_x$: los términos en $\alpha^2$ no son despreciables.

Con $\alpha$ infinitesimal coinciden: $\alpha^2$ desaparece y

$$
R \approx I + \alpha M
$$

## 8. Exponencial de matrices

$$
R(\varphi) = \lim_{n \to \infty} \left( I + \frac{\varphi}{n} M \right)^n = e^{\varphi M}
$$

Con

$$
M_z = \begin{pmatrix} 0 & -1 & 0 \\ 1 & 0 & 0 \\ 0 & 0 & 0 \end{pmatrix}
$$

las potencias son cíclicas: $M^2$ es un bloque diagonal negativo, $M^3 = -M$, $M^4 = -M^2$. Las potencias impares se agrupan en $\sin\varphi$, las pares en $(1 - \cos\varphi)$, y el resultado es

$$
e^{\varphi M_z} = R_z(\varphi)
$$

## 9. Conexión profunda

- Las rotaciones infinitesimales conmutan, igual que los pasitos $du$, $dv$.
- Lo infinitesimal simplifica; lo finito se construye por acumulación.
- El tensor métrico se transforma con la jacobiana $J$ como

$$
g' = J^{\mathsf{T}}\, g\, J
$$

el mismo patrón que las rotaciones.
