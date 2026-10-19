# Revisión semántica — capítulo 6 (Subespacios, cuña y determinante): producto mixto y losa

Resumen: sin errores graves; la losa coincide con `cap06_producto_mixto.py` y las demostraciones son correctas; cuatro menores (un salto menor en la proposición del producto mixto, el criterio de planeidad, notación de normas y un giro gramatical).

Alcance: `apunte/contenido/06-subespacios-cuna-determinante.tex` líneas 265-387 (subsección `sec:producto-mixto` y aplicación de la losa) y el ejercicio `ex:cuna-mixto-losa` (líneas ~763-776).

## Verificado sin hallazgos
- Procedencia/voz: sin menciones a personas, clases ni fechas. Los `\textbf{Desarrollo.}` de las líneas 25, 395, 469 y 533 son estructurales (existentes) y no remiten a documentos de origen.
- Números: corrí el script. Coinciden `v×w=(2,1,-1)`, `u·(v×w)=4`, `|v×w|=√6`, altura 1,632993; losa: `a=(8,527;0,432;0,044)`, `b=(8,092;8,796;0,125)`, `c=(-0,441;8,349;0,084)`, `a×b=(-0,333024;-0,709827;71,507748)`, `|a×b|=71,5120`, mixto `0,146864-5,926346+6,006651=0,227169`, `d=3,177` mm, `z4-z_plano=+3,177` mm (el signo «P4 por encima» es correcto). Ejercicio: `c_z=0,089`, mixto `0,584708`, `d=8,176` mm.
- Verifiqué a mano `u×v=(2,-1,1)`, `det M=4`, el desarrollo por la primera columna de la parte (a), la paridad de las permutaciones de la parte (c) y la implicación `u·(v×w)=0 ⇒ coplanares` cuando `v×w≠0`.
- Magnitudes: losa de 8,5 × 8,4 m, cotas del orden de 12 m con diferencias de centímetros, tolerancia de 5 mm: realistas para una losa relevada con estación total. Coordenadas locales (no oficiales), de modo que no corresponde la convención GK.
- Recuadros `\unidadInteractiva` (líneas 140 y 516; fuera de la parte nueva): verificados contra `unidades/07a_cuna_determinante.py` (caso «v gira alrededor de u = (3, 1)») y `unidades/07b_nucleo_autovectores.py` (caso «proyección [[1, 2], [2, 4]]: det 0, el núcleo», núcleo `(2,-1)`, imagen la recta de `(1,2)`). Existen y hacen lo que dice la consigna.

## Hallazgos

1. **menor** — `06-subespacios-cuna-determinante.tex:307`: la proposición (b) afirma «\(u\cdot(v\times w)=0\) si y sólo si \(u,v,w\) son coplanares (linealmente dependientes)», pero la demostración prueba «dependientes ⇒ det=0» y «det=0 ⇒ los tres están en un plano por el origen»; falta la dirección «coplanares ⇒ dependientes» (tres vectores de un subespacio de dimensión 2 son dependientes) y no se aclara que «coplanares» significa «en un plano por el origen». Propuesta: en el enunciado, «…si y sólo si \(u,v,w\) son linealmente dependientes, es decir, están en un mismo plano por el origen», y agregar a la demostración: «Tres vectores de un plano (dimensión 2) son siempre dependientes.» El paso «\(v\times w=0\) ⇒ \(v,w\) dependientes» conviene citarlo expresamente (en el texto sólo se alude a «el análogo en \(\R^3\)»).

2. **menor** — `06-subespacios-cuna-determinante.tex:353-378` y `ex:cuna-mixto-losa`: el criterio de planeidad es la distancia de `P_4` al plano de `P_1,P_2,P_3`. Está dicho con claridad y las cuentas son correctas, pero la decisión depende de esa elección. Calculé el plano de ajuste (mínimos cuadrados ortogonales) de los cuatro puntos: los residuos son ±0,79 mm para `z4=12,431` y ±2,04 mm para `z4=12,436`, es decir, alrededor de `d/4`. Con ese criterio el ejercicio daría «coplanares» (2,0 mm < 5 mm), no «no coplanares». Propuesta: agregar una frase al final de la aplicación y de la solución del ejercicio: «Se midió contra el plano de tres de los puntos; contra el plano de ajuste de los cuatro, el apartamiento es del orden de \(d/4\) (0,8 mm y 2,0 mm). Hay que fijar de antemano qué plano de referencia exige la tolerancia.»

3. **menor** — `06-subespacios-cuna-determinante.tex:279, 280, 329, 375`: la norma de un vector se escribe `\lvert v\times w\rvert`; el capítulo 0 declara `\lVert\cdot\rVert` para la norma. Propuesta: cambiar a `\lVert v\times w\rVert` (líneas 279, 280, 329) y en la fórmula de `d` (línea 375).

4. **menor** — `06-subespacios-cuna-determinante.tex:303`: «el cuña de \(2\times2\) que queda al tachar la fila \(i\)». Ese objeto es el *menor* (cofactor sin signo), no «un cuña»; además «cuña» se usa en masculino en 303 y en 189, 197, 497 y 519. Propuesta: «el menor de \(2\times2\) que queda al tachar la fila \(i\) y la columna de \(u\) (un producto cuña de las otras dos filas)».
