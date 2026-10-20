---
clase: 14
titulo: "Capítulo 15: trigonometría esférica y polígonos geodésicos"
idea: "Sobre la esfera todo se mide en ángulos: un producto interno da la ley de cosenos, y el exceso de los ángulos de un polígono es su área."
que_se_estudia: ["Triángulo esférico: tres planos por el centro", "Ley de cosenos esférica y límite plano", "Exceso esférico: $A+B+C-\\pi=\\text{Área}/R^2$", "Polígono geodésico y error angular de una poligonal", "Problemas directo e inverso sobre el elipsoide"]
conceptos_previos: ["Producto interno y vectorial (capítulos 1 y 6)", "Geodésicas y curvatura (capítulo 13)", "Elipsoide (capítulo 14)"]
apunte: ["esfera"]
unidades: ["14_trigonometria_esferica", "15_transformaciones_conformes"]
animaciones: ["06_conforme_tissot_mercator"]
ejercicios_sugeridos: ["Deducir la ley de cosenos con vértices $A=(0,0,1)$, $B$, $C$", "Verificar el octante: tres ángulos rectos y área un octavo de la esfera", "Calcular el exceso esférico de triángulos de 1 km y 100 km de lado"]
---

# Capítulo 15: trigonometría esférica y polígonos geodésicos

Sobre la esfera todo se mide en ángulos: un producto interno da la ley de cosenos, y el exceso de los ángulos de un polígono es su área.

## Qué se estudia

- Triángulo esférico: tres planos por el centro
- Ley de cosenos esférica y límite plano
- Exceso esférico: $A+B+C-\pi=\text{Área}/R^2$
- Polígono geodésico y error angular de una poligonal
- Problemas directo e inverso sobre el elipsoide

**Trigonometría esférica** (apoyado en el producto interno del capítulo 1, el producto vectorial del capítulo 6 y las geodésicas del capítulo 13). Pregunta: tres puntos sobre la esfera unidad, unidos por círculos máximos; ¿qué relación hay entre los tres lados y los tres ángulos? Lo que se ve: un triángulo esférico son tres planos por el centro; cada lado es el ángulo entre dos radios, cada ángulo es el diedro entre dos de esos planos. Nada mide en metros: todo son ángulos, y la esfera de radio $R$ solo multiplica los lados por $R$. Álgebra: si $A,B,C$ son los vectores unitarios de los vértices, el lado $a$ (opuesto a $A$) cumple $\cos a=B\cdot C$ (capítulo 1: el producto interno mide ángulos); el ángulo en $A$ es el ángulo entre las normales de los planos $OAB$ y $OAC$, es decir entre $A\times B$ y $A\times C$ (capítulo 6: el producto vectorial da la normal del plano por dos puntos). Juntando las dos:
$$\cos a=\cos b\cos c+\sin b\sin c\cos A,$$
la ley de cosenos esférica. Escalera: en el plano, $a^2=b^2+c^2-2bc\cos A$; sobre la esfera los lados chicos ($\sin b\approx b$, $\cos b\approx1-b^2/2$) devuelven la fórmula plana. Es ir a lo chico para volver a lo grande: una Tierra lo bastante chica es plana.

Exceso esférico: en el plano los ángulos suman $\pi$; en la esfera suman más, y el sobrante es el área: $A+B+C-\pi=\text{Área}/R^2$ (Girard). Lo que se ve: el triángulo abomba y los ángulos se abren; cuanto más grande, más se abren. Para topografía la consecuencia es Legendre, un triángulo esférico chico se calcula como plano restando $\varepsilon/3$ a cada ángulo.

**Polígono geodésico** (apoyado en las geodésicas del capítulo 13). Pregunta: una poligonal cerrada de $n$ lados geodésicos; ¿cuánto suman sus ángulos? Álgebra: cortando en triángulos, $\sum\text{ángulos}-(n-2)\pi=\text{Área}/R^2$. Lo que se ve: una poligonal cerrada cuyo error de cierre delata que la Tierra no es plana (ni esfera); en una poligonal de agrimensura el «error angular» tiene una parte que no es error sino exceso esférico, y hay que separarla antes de compensar. Sobre el elipsoide los lados son geodésicas que no son círculos (los meridianos sí, los paralelos no), y no hay ley de cosenos cerrada: problema directo (punto + azimut + distancia → punto) y problema inverso (dos puntos → distancia y azimutes) se resuelven con series como la del arco de meridiano, o numéricamente; un sistema de álgebra computacional hace ahí lo que en la esfera se hace a mano.

## Conceptos previos

- Producto interno y vectorial (capítulos 1 y 6)
- Geodésicas y curvatura (capítulo 13)
- Elipsoide (capítulo 14)

## En el apunte

- Capítulo 15. Coordenadas sobre la esfera y trigonometría esférica

## Unidades interactivas

- Trigonometría esférica (`14_trigonometria_esferica`)
- Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico (`15_transformaciones_conformes`)

## Animaciones

- `06_conforme_tissot_mercator`

## Ejercicios sugeridos

- Deducir la ley de cosenos con vértices $A=(0,0,1)$, $B$, $C$
- Verificar el octante: tres ángulos rectos y área un octavo de la esfera
- Calcular el exceso esférico de triángulos de 1 km y 100 km de lado
