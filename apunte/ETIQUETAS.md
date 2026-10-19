# Etiquetas fijadas para el trabajo en paralelo

Cuando varios capítulos se escriben a la vez, cada uno cita a los otros con `\ref` a estas etiquetas, existan o no todavía en el árbol. La compilación conjunta las resuelve. Quien escribe la sección es responsable de poner la etiqueta exactamente con este nombre; quien la cita no la inventa distinta.

## Capítulo 4

| Etiqueta | Qué marca |
|---|---|
| `sec:mapa-transformaciones` | Sección «Mapa de las transformaciones» (ya existe) |
| `tab:conserva` | Cuadro de invariantes por familia (ya existe) |

## Capítulo 5

| Etiqueta | Qué marca |
|---|---|
| `sec:transpuesta-normales` | Subsección «Cómo se transforman las mediciones»: ⟨Au, v⟩ = ⟨u, Aᵀv⟩, normales con A⁻ᵀ |
| `def:transpuesta-adjunta` | Definición de la transpuesta como adjunta geométrica |

## Capítulo 6

| Etiqueta | Qué marca |
|---|---|
| `sec:producto-mixto` | Producto mixto u·(v×w) = det[u v w] como volumen con signo |
| `def:producto-mixto` | Su definición |

## Capítulo 7

| Etiqueta | Qué marca |
|---|---|
| `sec:traza-derivada-det` | Subsección «La traza como derivada del determinante» |
| `prop:traza-derivada-det` | det(I + εE) = 1 + ε tr E + O(ε²) |

## Capítulo 9

| Etiqueta | Qué marca |
|---|---|
| `sec:conjugacion` | Conjugación o semejanza: B = C⁻¹AC, lectura activa |
| `def:conjugacion` | Definición de matrices conjugadas o semejantes |
| `sec:congruencia` | Subsección «Cada objeto cambia con su regla» |
| `prop:congruencia-ortogonal` | Si C es ortogonal, C⁻¹AC = CᵀAC |
| `tab:regla-de-cada-objeto` | Tabla vector / forma lineal / transformación / forma cuadrática |

## Capítulo 11

| Etiqueta | Qué marca |
|---|---|
| `def:adjugada` | Adjugada adj(A), transpuesta de la matriz de cofactores; A⁻¹ = adj(A)/det A |

## Capítulo 0

| Etiqueta | Qué marca |
|---|---|
| `caja:convencion-en` | Caja «Coordenadas (E, N) y planillas oficiales» (ya existe) |
| `tab:operaciones` | Tabla de referencia «Qué mide cada operación» |
| `sec:glosario` | Glosario (conjugación o semejanza, congruencia, conjugado complejo, conjugado armónico, adjugada, adjunta) |
| `caja:comprobaciones` | Caja «Tres tipos de comprobación con código» en «Cómo usar este apunte» |

## Complementos C1 y C2

| Etiqueta | Qué marca |
|---|---|
| `sec:conjugado-armonico` | Conjugado armónico, (A, B; C, D) = −1, cuadrilátero completo (C1) |
| `def:conjugado-armonico` | Su definición (C1) |
| `sec:conjugado-complejo` | J(z̄) = J(z)ᵀ = S J(z) S, reflexión en el eje real (C2) |
| `prop:conjugado-complejo` | La proposición (C2) |

## Capítulos 12 a 15 (fase E, lote 1)

| Etiqueta | Qué marca |
|---|---|
| `cap:cuatro-problemas` | Capítulo 12 (ya existe) |
| `sec:cuatro-problemas-regresion` | Recta por mínimos cuadrados y regresión total (12) |
| `sec:cuatro-problemas-circulo` | Ajuste de un círculo (12) |
| `sec:cuatro-problemas-procrustes` | Procrustes (12) |
| `cap:curvatura` | Capítulo 13 (ya existe) |
| `sec:segunda-forma` | Segunda forma fundamental (13) |
| `sec:curvaturas-principales` | Curvaturas principales, Euler y Meusnier (13) |
| `cap:elipsoide` | Capítulo 14 (ya existe) |
| `sec:radios-MN` | Radios de curvatura M y N (14) |
| `sec:latitudes` | Latitudes geodésica, geocéntrica y reducida (14) |
| `cap:esfera` | Capítulo 15 (ya existe) |
| `sec:exceso-esferico` | Exceso esférico (15) |
| `sec:problema-directo-inverso` | Problema directo e inverso sobre la esfera (15) |

## Apéndices y demostraciones con código

| Etiqueta | Qué marca |
|---|---|
| `ap:infinitesimales` | Apéndice de rotaciones infinitesimales (ya existe) |
| `ap:bibliografia` | Bibliografía (ya existe) |
| `ap:notebooks` | Tabla de unidades generada (ya existe) |
