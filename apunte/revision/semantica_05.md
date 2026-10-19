# Revisión semántica — capítulo 5 (Formas lineales), subsección «Cómo se transforman las mediciones»

Resumen: sin errores graves; las demostraciones, las cuentas y los números coinciden con `cap05_transpuesta_normales.py`; quedan cinco observaciones menores de formulación y notación.

Alcance: `apunte/contenido/05-formas-lineales.tex` líneas 380-539 (subsección nueva), ejercicio `ex:fl-normales` (líneas ~822-835) y comentario de cabecera (líneas 3-4).

## Verificado sin hallazgos
- Procedencia/voz (rúbrica 1): sin menciones a personas, cursos, fechas ni archivos de origen; la voz es impersonal o plural inclusivo.
- Demostraciones (rúbrica 2): la unicidad y existencia de la adjunta, `(AB)^T=B^TA^T`, `(A^{-1})^T=(A^T)^{-1}`, `R^TR=I` y la proposición de normales (ambas inclusiones de la imagen de la recta, más el diferencial) son correctas y sin saltos. Verificadas a mano.
- Números (rúbrica 3): corrí el script. Coinciden todos: `Au=(4,2)`, `<Au,v>=10`, `A^{-T}`, `q'=(3,5;2)`, `d'=(5,1)`, ángulo 78,69°, recta imagen `-0,5x'+2,5y'=3,25`, `(8,5;3)`, `dh'=(0,005059;0,019261)`, `W'=(100;0)`, cota 32,9559, factor 4 (2,023 m), acimut 37,48°, pendiente 2,041 % frente a 2,176 %, `G'=diag(0,25;1)`. Ejercicio: `A^{-T}n=(1,-1)`, ángulo 26,57°. Las coordenadas Gauss-Krüger reutilizadas de la sección de pendiente son de la faja 5 y están en orden (E,N).
- Recuadros `\unidadInteractiva` (rúbrica 5): ninguno cae en la parte nueva. Los dos del capítulo (líneas 49 y 733) los verifiqué igual contra `unidades/06_formas_lineales.py` y `unidades/00_fundamentos.py`: existen el caso «escala anisótropa diag(2, 1)» con deslizador `k` (`np.diag([k,1])`, fila `(2/k,1)`), el objeto «(b) regla graduada wᵀ (el gradiente)» y el caso «estirar Este ×2: diag(2, 1)» con la fila `(1,1)→(1/2,1)`. Todo coincide.

## Hallazgos

1. **menor** — `05-formas-lineales.tex:396`: «La transpuesta mueve las mediciones (las formas lineales) de la misma manera en que \(A\) mueve los puntos, pero en sentido contrario: lleva la regla del lado de llegada al lado de partida.» La frase mezcla dos cosas: `A^T` *retrotrae* la regla (pullback), mientras que la regla *viaja con el punto* con `A^{-T}` (proposición de normales). «De la misma manera… pero en sentido contrario» confunde a quien después lee «las reglas con \(A^{-T}\)». Propuesta: «`A^T` lleva la regla del lado de llegada al lado de partida (la retrotrae); para acompañar al punto, la regla viaja con `A^{-T}`, como se ve en la proposición~\ref{prop:normales-inversa-transpuesta}.»

2. **menor** — `05-formas-lineales.tex:492`: «es el cambio de base con \(P=A^{-1}\)». El capítulo 0, tabla de notación, fija el cambio de base como `C_{e←b}` (y el capítulo 9 usa `C`); acá, y en `prop:co-contra` (línea 343), se usa `P`. Propuesta: o declarar en el capítulo 0 que en el capítulo 5 la matriz de base es `P` (columnas `b_j`), o escribir `C_{e←b}` en la nueva subsección con «(la `P` de la proposición~\ref{prop:co-contra})».

3. **menor** — `05-formas-lineales.tex:447, 470, 508`: «\(x'=Ax+c\)». La tabla del capítulo 0 fija la afinidad como `f(x)=Ax+b`. Propuesta: usar `b` para el término de traslación en la proposición, el contraejemplo y la aplicación (en la aplicación, `P_1'=b`), o aclarar en el capítulo 0.

4. **menor** — `05-formas-lineales.tex:387-456`: se usa `\langle\cdot,\cdot\rangle` para el producto interno, y a renglón seguido `n\cdot d`, `(An)\cdot d'`. La tabla de notación del capítulo 0 sólo declara `u\cdot v`. Propuesta: agregar `\langle u,v\rangle=u\cdot v` a la tabla («producto interno») o usar `u\cdot v` también en la definición de adjunta.

5. **menor** — `05-formas-lineales.tex:501`: «Sólo cuando \(A\) es una rotación (o una rotación por un factor de escala común) \(A^{-T}\) apunta igual que \(A\)». Es verdad para toda `A` ortogonal (la reflexión incluida): `prop:rotacion-transpuesta` está enunciada para cualquier `R` que conserva el producto interno. Propuesta: «Sólo cuando \(A\) es ortogonal (rotación o reflexión), o ortogonal por un factor de escala común».
