# Hoja de estilo del apunte

Normas para todo `.tex` que incluye el maestro (`Apunte_Sistemas_de_Coordenadas.tex`). El control
automático es `apunte/scripts/estilo.py` (desde la raíz: `uv run python apunte/scripts/estilo.py`);
el número entre corchetes al final de cada norma es el chequeo que la vigila. Lo que el script no
puede ver (persona, notación, «exactamente») se revisa a mano en la pasada editorial.

## 1. Tildes [chequeo 1]

«solo» y los demostrativos (este, esta, ese, esa, estos, estas, esos, esas, aquel, aquella) van
sin tilde, como pide la RAE. La tilde se admite solo cuando hay ambigüedad real, y entonces la línea
lleva el comentario `% ambigüedad`.

- Bien: `La rotación solo depende del ángulo.`
- Bien (ambigüedad real): `Trabajó sólo dos horas en la estación. % ambigüedad`
- Mal: `La rotación sólo depende del ángulo.`

## 2. Comillas [chequeo 2]

- Por defecto, comillas inglesas “ ” mediante `\enquote{...}` (paquete `csquotes`, configurado en
  `apunte-formato.sty`). Un `\enquote` dentro de otro da el segundo nivel, « ».
  Ejemplo: `la pregunta \enquote{¿cuántos pasos de cada vector?}` → la pregunta “¿cuántos pasos de cada vector?”.
- Nombres de botones, deslizadores, casos precargados y demás controles de las unidades
  interactivas: « » escritas directamente, con el texto copiado tal cual aparece en la unidad.
  Ejemplo: `en «caso precargado» elegí «escala anisótropa diag(1.5, s)»`.
- Prohibido escribir a mano ``` `` ``` y `''`. (La derivada segunda `f''` dentro de la matemática no
  cuenta.)

## 3. Terminología: similaridad y conjugación [chequeo 4]

- **Similaridad**: la transformación geométrica que multiplica todas las distancias por una misma
  razón (capítulo 3). Nunca se aplica a matrices.
- **Conjugación**: la relación \(B=C^{-1}AC\) entre matrices; \(A\) y \(B\) son **conjugadas**.
  «Semejantes» aparece una sola vez, como sinónimo, en la definición de matrices conjugadas
  (capítulo 9, `def:conjugacion`). No se usa «semejanza» para matrices.
- Bien: `La matriz de una transformación cambia de base por conjugación.`
- Mal: `La matriz de una transformación cambia por semejanza.`
- La distinción vive en una caja de aviso del capítulo 9 (junto a la definición) y en la entrada
  «Conjugación» del glosario del capítulo 0.

## 4. Persona

- Primera del plural para explicar: `Tomamos la base de autovectores y escribimos la matriz.`
- Impersonal para definiciones y enunciados: `Se llama núcleo de \(A\) al conjunto…`,
  `Si \(\det A\neq0\), entonces \(A\) es invertible.`
- Voseo en las consignas de recuadros y ejercicios: `Mové el deslizador y comprobá que…`,
  `Calculá la inversa.`
- Sin tuteo (`mueve`, `comprueba`, `calcula` como imperativo) ni usted (`compruebe`).

## 5. Números decimales [chequeo 3]

- Coma decimal en el texto, en las fórmulas y en las tablas. En modo matemático se escribe `{,}`
  para que no quede espacio después de la coma: `\(0{,}5\)`, `\(2{,}449\)`.
- Cuando dos números con coma van seguidos, se separan con punto y coma: `\((2{,}6;\ 4{,}2)\)`.
- El punto decimal solo aparece en el código (`lstlisting`, `\texttt`, nombres de archivo, URL) y
  en los nombres literales de controles de las unidades entre « » (norma 2), que se copian tal cual.
- Bien: `las abscisas \(0;\ 0{,}6;\ 1{,}8\)`. Mal: `las abscisas \(0,\ 0.6,\ 1.8\)`.

## 6. Notación: una letra por concepto

- La tabla «Notación y leyenda de símbolos» del capítulo 0 (`sec:notacion`) es la referencia.
  Ejemplos: \(C\) para la matriz de cambio de base (base nueva en columnas,
  \(C=C_{b\to e}\)); \(\operatorname{im}A\) para la imagen; \(\ker A\) para el núcleo;
  \(\operatorname{rango}A\) para el rango; \(A^T\) para la transpuesta.
- Un capítulo que necesita una convención propia la declara en **una sola línea** (párrafo
  «Convenciones del capítulo»). Lo demás no se repite: se remite al capítulo 0.
- No se escriben aclaraciones del tipo «en el capítulo X se escribe distinto» o «las tres letras
  designan lo mismo»: se unifica la letra.
- Bien: `Convenciones del capítulo: vectores en columna; base vieja \(e\), base nueva \(b\).`
- Mal: `Es la misma matriz que el recuadro llama \(P\) y el despeje llama \(A\).`

## 7. Muletillas [chequeos 5 y 6]

- «es decir»: como máximo una vez cada dos páginas (el script tolera una cada 100 líneas de
  fuente por archivo).
- «exactamente»: se elimina cuando no agrega precisión. Bien: `coincide exactamente con el
  valor tabulado hasta la novena cifra`. Mal: `es exactamente la misma idea`.
- Sin «Desarrollo.» al comienzo de los párrafos (ni `\textbf{Desarrollo.}`): el párrafo empieza
  directamente por su contenido.

## 8. Etiquetas y definiciones [chequeos 7 y 8]

- Etiquetas con nombre, nunca numéricas: `\label{cap:repaso-algebra}`, no `\label{cap:03}`. Las
  claves `apunte:` de las fichas (`clases/*.md`) y del mapa (`mapa/_fragmentos/*.yaml`) son el
  nombre sin `cap:` (`"repaso-algebra"`).
- Cada definición aparece una sola vez en el apunte: dos `\begin{definicion}[Título]` con el mismo
  título en archivos distintos son un error. Donde haga falta recordarla, una frase y un `\ref`.
