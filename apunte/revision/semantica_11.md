# Revisión semántica — capítulo 11 (`apunte/contenido/11-inversas-pseudoinversa.tex`), sección de la adjugada

Resumen: la adjugada y sus ejemplos están bien calculados (2×2, ejemplo 3×3 con \(\det A=1\), inversa por \(P\,\mathrm{diag}(\tfrac13,1)P^{-1}\)); 2 graves (una demostración que descansa en una propiedad no probada para n general y un error de terminología en la lista de subespacios) y 4 menores.

Verificado sin hallazgos: `def:adjugada` (110-120) y su uso «adjugada»/«adjunta» (122-125, coherente con el glosario del capítulo 0 y con 05-formas-lineales.tex:423-426); cuñas `(2,-3,1)`, `(-3,6,-2)`, `(1,-2,1)`, \(\det A=1\), \(A^{-1}\) y control \(AA^{-1}=I\) (173-188); idea del giro de 90° (135-152); coincidencia de \(\tfrac13\begin{psmallmatrix}2&-1\\-1&2\end{psmallmatrix}\) con adjugada/determinante (205); celdas «Inversa» y «Adjugada» de la tabla del capítulo 0 respaldadas por 96-120 y 154-171; los dos `\unidadInteractiva` (49 y 474-476) piden controles y casos que existen en `unidades/09_cambio_de_base_svd.py` (deslizador y₃, caso «aplastante [[1, 2], [2, 4]]») y `unidades/11_cuatro_problemas.py` (caso «(a) recta de ajuste…», deslizador de ruido, línea que muestra A^T r).

## Graves

1. **Demostración con salto / propiedad no probada** — `11:96-106` (`prop:inversa-existe`, para \(n\times n\)) y `11:113-115`: «Cumple \(A\,\operatorname{adj}(A)=\operatorname{adj}(A)\,A=(\det A)\,I\)». La demostración dice «la construcción que sigue fabrica \(A^{-1}\) cuando \(\det A\neq0\)», pero esa identidad figura dentro de una definición, sin prueba, y sólo se verifica para \(n=2\) (127-152) y, por cuñas, para \(n=3\) (154-171). Para \(n\ge4\) la implicación (b)⇒(a) queda sin sostén. Propuesta: agregar tras la definición (o dentro de la demostración) «El desarrollo del determinante por la fila \(i\) da \(\sum_j a_{ij}C_{ij}=\det A\), que es la entrada \((i,i)\) de \(A\operatorname{adj}A\); si \(k\neq i\), \(\sum_j a_{kj}C_{ij}\) es el determinante de la matriz con la fila \(i\) reemplazada por la \(k\), que tiene dos filas iguales y vale \(0\)», o restringir la construcción a \(n=2,3\) y citar el caso general.
2. **Error de terminología** — `11:215`: «\textbf{imagen} (``rango o co-dominio'')». El codominio es todo \(\R^m\), no la imagen; y «rango», en este apunte (06-subespacios…, `def:nucleo-imagen`, y 11:21-22) es la dimensión de la imagen. Lo mismo en 213: «co-imagen (``rango de entrada o podríamos llamar contra-núcleo'')». Propuesta: «\textbf{imagen}: lo alcanzable a la salida…» y «\textbf{co-imagen}: lo perpendicular al núcleo…», sin los paréntesis entrecomillados.

## Menores

1. **Voz de clase** — `11:213` («podríamos llamar») y `11:227` («``mover la longitud no me mueve''», primera persona entre comillas). Propuesta: reformular en impersonal: «la longitud no mueve el punto».
2. **Cofactores afirmados, no mostrados** — `11:166-168`: «cada cuña \(f_j\times f_k\) tiene por componentes los cofactores de la fila restante». Propuesta: una línea con el caso: \((f_2\times f_3)_1=a_{22}a_{33}-a_{23}a_{32}\), que es el cofactor de \(a_{11}\).
3. **Causa insuficiente** — `11:185-187`: «Que el determinante valga \(1\) explica que la inversa tenga entradas enteras». Hace falta además que \(A\) tenga entradas enteras. Propuesta: «Como \(A\) tiene entradas enteras y \(\det A=1\), la inversa también las tiene».
4. **Letra distinta en la unidad** — `11:476` (caja) dice «\(P^{+}=P/25\)» y el capítulo llama \(C\) a esa matriz (`11:314`); \(P\) además se usa en 192-200 para los autovectores. Propuesta: «\(C^{+}=C/25\)» en la consigna.

## Graves del capítulo 11

Dos: `11:96-106,113-115` (propiedad de la adjugada no probada para n general) y `11:215` («rango o co-dominio»).
