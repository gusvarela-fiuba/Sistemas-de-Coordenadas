---
clase: N              # orden del programa, 1 a 14; el complemento de proyectivas lleva "3p"
titulo: "Capítulo N: <idea en pocas palabras>"
idea: "<una frase que enuncia la idea central>"
que_se_estudia: []        # 3 a 6 ítems
conceptos_previos: []     # ítems o claves de fichas anteriores
apunte: []                # claves de \label{cap:...} del apunte, sin «cap:» (rotaciones, traslaciones, afines, ...)
unidades: []              # ids de unidades/*.py
animaciones: []           # nombres de animaciones/*.mp4 sin extensión, si aplica
ejercicios_sugeridos: []  # 2 a 4 ítems cortos
---

# Capítulo N: <idea en pocas palabras>

<La idea, en una frase.>

## Qué se estudia
Los ítems de `que_se_estudia`, y para cada concepto un par «lo que dice el álgebra ↔ lo que se ve», con la escalera R → R² → R³ → Rⁿ cuando aplique. Nivel: quien viene del CBC; la pregunta antes que la fórmula.

## Conceptos previos
Qué hay que tener a mano de las fichas anteriores.

## En el apunte
Una línea por clave del frontmatter, con rótulo, número y título como en el PDF (p. ej. `- Capítulo 1. Rotaciones: girar es multiplicar`); sin la clave. Los números salen de `apunte/numeracion.json`.

## Unidades interactivas
Lecciones de `unidades/` que acompañan el capítulo.

## Animaciones
Sólo si hay (`animaciones/*.mp4`).

## Ejercicios sugeridos
Dos a cuatro ejercicios cortos, con números enteros que se puedan hacer a mano.
