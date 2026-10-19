# Revisión semántica — capítulo 12 «Cuatro problemas de ajuste» (2026-10-19)

Archivos revisados: `contenido/12-cuatro-problemas.tex`, `scripts/cap12_cuatro_problemas.py`, `unidades/11_cuatro_problemas.py`.

**Resumen:** matemática sólida (Procrustes con corrección de determinante, m·m′=ρ², regresión total y residuos radiales verificados numéricamente; 40 números cotejados contra la salida del script, coinciden todos salvo uno); un grave (pendiente de la aplicación 1 mal copiada) y varios menores de rigor, notación y estilo.

Verificaciones hechas: salida completa del script; fórmula R = U diag(1, det UVᵀ) Vᵀ y s = (σ₁ + det·σ₂)/Σ‖a′‖² contra búsqueda por fuerza bruta (caso directo y caso reflejado; en el reflejado el óptimo con s>0 coincide con la fórmula); álgebra de la proposición del ejercicio de Helmert; baricentros y datos de C₁, C₂, C₃ contra el capítulo 3; los tres recuadros interactivos contra `cb104.procrustes`, `regresion_total` y `recta_ajuste` (ruido 0, 0,3 y 1).

## Hallazgos

### Graves

1. **grave — número que no coincide.** `12-cuatro-problemas.tex:546`: «\(dN/dE=S_{EN}/S_{EE}=1{,}131240\)». Con \(S_{EN}=163{,}6079\) y \(S_{EE}=144{,}4903\) el cociente es \(1{,}132311\) (el script imprime `dN/dE = 1.132311`; el acimut de \(41^\circ26'57{,}6''\) del texto sí corresponde a ese valor). Propuesta: reemplazar `1{,}131240` por `1{,}132311`.

### Menores

2. **menor — resultado usado sin demostración.** `12-cuatro-problemas.tex:553-554`: «y la total queda en el medio, como corresponde a la proposición~\ref{prop:cp-dos-regresiones}». Esa proposición sólo compara las dos simples (\(m<1/m'\)); que la total quede entre ambas se usa también en l.178 y en el ejercicio de l.693 sin estar probado. Propuesta: agregar a la proposición o a una observación: la pendiente \(t\) de \(v_1\) cumple \(S_{xy}t^2+(S_{xx}-S_{yy})t-S_{xy}=0\) (de \(Cv=\lambda v\)); evaluada en \(m=S_{xy}/S_{xx}\) da \(\tfrac{S_{xy}}{S_{xx}^2}(S_{xy}^2-S_{xx}S_{yy})<0\) y en \(1/m'=S_{yy}/S_{xy}\) da \((S_{xx}S_{yy}-S_{xy}^2)/S_{xy}>0\); como el polinomio es una parábola que abre hacia arriba con raíz negativa, la raíz positiva \(t\) queda entre \(m\) y \(1/m'\) (si \(S_{xy}>0\)).

3. **menor — hipótesis omitidas.** (a) `:100-116`: \(\rho\) y \(1/m'\) exigen \(S_{xx},S_{yy}>0\) y \(S_{xy}\neq0\); sin eso «más empinada» pierde sentido. (b) `:129-135`: la recta total es única sólo si \(\lambda_1>\lambda_2\) (nube no isótropa); con \(\lambda_1=\lambda_2\) cualquier recta por el baricentro sirve. (c) `:343-352`: si \(\det(UV^T)=-1\) y \(\sigma_1=\sigma_2\) la escala óptima es \(s=0\) (no hay rotación que ayude), y la unicidad de \(R\) exige \(\sigma_2>0\). Propuesta: agregar una frase de hipótesis en cada enunciado («si \(\lambda_1>\lambda_2\)», «si \(S_{xx}S_{yy}S_{xy}\neq0\)», «si \(\sigma_2>0\)»).

4. **menor — notación frente al capítulo 0.** `12-cuatro-problemas.tex:132-134,176,695-700` escribe los autovalores como \(\lambda_1,\lambda_2\); la tabla de notación del capítulo 0 asigna \(\mu_1,\mu_2\) a los capítulos 12 a 15 y reserva \(\lambda\) a longitud. Además `:214` llama \(\lambda\) a la escala de Helmert (\(a=\lambda\cos\theta\)) mientras `:464,474` usa \(s\) para la misma cantidad (el capítulo 3 usa \(\lambda\)). Propuesta: \(\mu_i\) para autovalores y \(s\) en todo el capítulo, con una nota en l.214 («el capítulo~\ref{cap:reflexiones} la llama \(\lambda\)»).

5. **menor — colisiones de letras.** (a) `:592-596`: los coeficientes del círculo \(D,E,F\) conviven en el mismo párrafo con las coordenadas \((E,N)\) y con \(E_c\); \(E=-15{,}2909\) se lee como un este. Propuesta: renombrar los coeficientes (por ejemplo \(\alpha,\beta,\gamma\)) o escribir `\(E_{\text{coef}}\)`. (b) `:44`: \(C\) es la matriz de dispersión, y en el capítulo 0 \(C=C_{e\leftarrow b}\) es cambio de base (y en el capítulo 13 es jacobiano); aclarar en las convenciones del capítulo («\(C\), sin subíndices, es la dispersión; no es un cambio de base»). (c) \(a,b\) designan a la vez el centro del círculo (`:200`), las nubes \(a_i,b_i\) (`:313`) y los parámetros de Helmert (`:477`).

6. **menor — voz/procedencia (archivo de origen en la prosa).** `:169` «el script da \(A^Tr=(0,0)\)», `:270` «El script genera siete puntos», `:282`, `:450` «El script comprueba», `:522` «los generó el script», `:558` «El script gira además»; más los cuatro pies «Generada con \texttt{apunte/scripts/…}». Es la convención de otros capítulos (3, 4, 7, 8, 11), de modo que no es una violación aislada, pero la prosa depende de un archivo. Propuesta: en el texto, «la verificación numérica» o «el cálculo con coordenadas reducidas»; dejar la ruta del script sólo en el pie de figura y en una nota inicial del capítulo.

7. **menor — afirmación sin respaldo.** `:236-237`: «tiende a subestimar el radio si los puntos cubren sólo un arco corto». Es cierto (simulación propia con ruido \(0{,}3\) sobre \(r=5\): arco de \(60^\circ\) da radio medio \(2{,}9\); arco de \(210^\circ\) casi no sesga), pero no se demuestra ni se cita. Propuesta: «(se observa numéricamente; no se demuestra aquí)» y mencionar que con \(210^\circ\) el efecto es de milésimas (\(4{,}9596\) contra \(4{,}9604\)).

8. **menor — estimación sin justificar.** `:567-569`: «\(\sigma_0/\sigma_1\approx351''\), con \(\sigma_0=\sigma_2/\sqrt{n-2}\)». La cifra es correcta (\(0{,}0309/18{,}16=1{,}70\cdot10^{-3}\) rad), pero el lector no tiene de dónde sale. Propuesta: una oración: «la pendiente de la recta ajustada tiene desvío \(\sigma_0/\sqrt{S_\parallel}\), con \(S_\parallel=\sigma_1^2\) la suma de cuadrados a lo largo de la recta».

9. **menor — unidades de un ejemplo.** `:375-397` (Procrustes con cuatro puntos): los datos no declaran unidad pero el texto habla de «centímetros» y «cuatro unidades». Propuesta: «en metros» en el enunciado (\(A\) de \(4\times3\) m, perturbaciones de \(2\) a \(6\) cm).

10. **menor — consigna de recuadro vs. unidad (todos factibles).** Verificados: `:57` (d) la pendiente simple nunca supera la total (confirmado con ruido 0,05, 0,3 y 1: 0,5951/0,5952; 0,5696/0,5745; 0,5041/0,5460), `:413` (c) con ruido 0 devuelve 25°, 1,2 y (1,5; 0,5) y \(\sum\langle r_i,Rp_{0i}\rangle\) da \(\sim10^{-15}\) para ruido 0,3 y 1; `:415` (a)→(d) muestra \(A^Tr\) y \(\lambda_{\min}\). Únicos reparos: la unidad usa \(H=P_0^TQ_0\), \(R=VU^T\) y \(p_{0i}\), mientras el capítulo usa \(M=B_0^TA_0\), \(R=UV^T\) y \(a_i'\). Propuesta: una línea en el recuadro de l.413: «(en la unidad, \(P_0\) es la nube \(A\) centrada y \(Q_0\) la \(B\); \(H=M^T\))».

11. **menor — procedencia en la unidad asociada.** `unidades/11_cuatro_problemas.py:44` firma «Gustavo Varela» y `:605-611` remite a secciones del apunte que no existen con esos nombres («Resolución de los cuatro problemas», «Sistemas de ecuaciones y aplicaciones») y a la «ficha de la clase 11». Propuesta: enlazar al capítulo por su etiqueta y sin mencionar clases ni autoría en el cuerpo de la unidad.

## Graves del capítulo 12

- Línea 546: pendiente `1{,}131240` debe ser `1{,}132311`.
