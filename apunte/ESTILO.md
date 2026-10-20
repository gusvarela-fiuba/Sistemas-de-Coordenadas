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
- Los capítulos **no llevan** párrafo «Convenciones del capítulo» (retirados el 2026-10-19 por
  decisión del editor): toda convención, incluso la propia de un capítulo, va como fila de la
  tabla del capítulo 0, indicando en qué capítulo aplica. En el texto queda, como mucho, una frase
  corta en «La idea» cuando sin ella no se puede leer lo que sigue.
- No se escriben aclaraciones del tipo «en el capítulo X se escribe distinto» o «las tres letras
  designan lo mismo»: se unifica la letra.
- Bien: una fila «Cambio de base» en la tabla del capítulo 0 con «base vieja \(e\), base nueva \(b\), vectores en columna».
- Mal: `Es la misma matriz que el recuadro llama \(P\) y el despeje llama \(A\).`

## 7. Muletillas [chequeos 5 y 6]

- «es decir»: como máximo una vez cada dos páginas (el script tolera una cada 100 líneas de
  fuente por archivo).
- «exactamente»: se elimina cuando no agrega precisión. Bien: `coincide exactamente con el
  valor tabulado hasta la novena cifra`. Mal: `es exactamente la misma idea`.
- Sin «Desarrollo.» al comienzo de los párrafos (ni `\textbf{Desarrollo.}`): el párrafo empieza
  directamente por su contenido.

## 8. Voz para el aula [chequeos 9, 10 y 11]

Los chequeos 9, 10 y 11 son advertencias: se informan en una segunda tabla («Voz para el aula») y
no bloquean ni entran en el total ni en `--estricto`. El objetivo: menos de 4 términos de campo cada
100 líneas en los capítulos 0 a 11, cero nombres de instrumentos, y al menos una pregunta o un
experimento mental en «La idea» de cada capítulo. La lista de términos de campo es la constante
`TERMINOS_CAMPO` de `estilo.py` y se amplía a mano.

1. **Lector.** Un adulto de 18 a 20 años que acaba de terminar el ciclo básico. Nada de analogías
   infantiles (calesitas, tortas, recetas). Sí experimentos mentales en primera persona del lector
   y situaciones físicas que se puedan probar (un libro en el aire, una hoja sobre la mesa).
   - Bien: `Imaginá que estás parado sobre una plataforma que gira. ¿Qué cambia y qué no?`
   - Mal: `Pensá en la calesita: cada caballito da vueltas como en una receta de torta.`

2. **Primero la imagen, después el nombre.** Cada concepto nuevo arranca con una pregunta o un
   experimento mental, dice para qué sirve y recién después lo nombra y lo define. La imagen se
   retoma una vez, cuando el concepto se desarrolla.
   - Bien: `Apoyá un libro sobre la mesa y giralo sin levantarlo: ¿qué punto no se mueve? Para
     describir ese giro con números hace falta una matriz, que llamamos matriz de rotación.`
   - Mal: `Se llama matriz de rotación a toda matriz ortogonal con determinante 1.` (sin nada antes)

3. **Símbolos con presentación.** Ningún símbolo nuevo (\(V\), \(V^*\), \(G\), \(\Sigma\), \(J\),
   \(A^+\), \(\kappa\), etc.) aparece sin una frase que diga qué es y para qué sirve, la primera vez
   en cada capítulo.
   - Bien: `Llamamos \(J\) a la matriz que dice cuánto se estira cada dirección cerca de un punto.`
   - Mal: `Calculamos \(J\) y la invertimos.` (sin decir qué es \(J\))

4. **Instrumentos y procedimientos por lo que hacen.** No se nombran instrumentos que el lector no
   conoce (estación total, nivel, GNSS, limbo): se describe lo que hacen. Lo mismo con los
   procedimientos (radiado, nivelación, poligonal, ajuste): se explican por lo que hacen antes de
   nombrarlos. [chequeo 10]
   - Bien: `Hay instrumentos que miden ángulos horizontales con precisión de hasta un segundo de arco y distancias al milímetro.`
   - Mal: `Se observa con la estación total desde el mojón.`

5. **Términos de campo y de ajuste.** Acimut, cota, Gauss-Krüger, faja, POSGAR, mínimos cuadrados,
   residuo, tolerancia, redundancia, covarianza: una frase llana la primera vez en cada capítulo.
   Los números largos de coordenadas oficiales llevan la aclaración de que importan las diferencias,
   no el valor completo. [chequeo 9]
   - Bien: `El acimut es el ángulo que forma una dirección con el norte, contado en sentido horario.`
   - Mal: `Con el acimut y la cota ajustamos por mínimos cuadrados.` (sin una sola frase llana)

6. **Aplicaciones topográficas.** Empiezan con la situación contada en lenguaje llano antes de los
   datos. Si una aplicación necesita más de dos conceptos de campo que el lector no tiene (Helmert,
   red libre, propagación de errores), se conserva, pero en «En profundidad» o con la caja «Esto lo
   vas a usar en Topografía».
   - Bien: `Hay que ubicar dos puntos nuevos midiendo desde uno conocido. Medimos ángulos y distancias…`
   - Mal: `Sea una red libre con vector de observaciones \(l\) y matriz de covarianza \(\Sigma_l\)…`

7. **Formalidad en su lugar.** Las definiciones y los teoremas se enuncian con precisión y las
   demostraciones largas van en «En profundidad». En «La idea» y en «Construcciones» manda la
   intuición.

8. **Lo que no se recorta.** Las cajas de idea que resumen la tesis de una sección y las preguntas
   al lector no se recortan. [chequeo 11]

9. **NumPy fuera del texto corriente.** Los comandos de NumPy no van en el texto corriente: van en
   las unidades, donde se exploran.
   - Bien: `Probá en la unidad con la matriz que quieras y mirá qué pasa con los autovalores.`
   - Mal: `Se calcula con np.linalg.eig(A) y se toma la segunda columna.`

### Sin límite de páginas (criterio vigente desde la fase G)

El apunte no tiene tope de páginas: puede llegar a 300 o 400 si el contenido lo pide. No se comprime
ni se recorta texto para ahorrar espacio. Si para que algo se entienda hace falta un experimento
mental, una figura, un ejemplo resuelto o un paso intermedio más, se agrega (las figuras y los
números salen siempre de un script en `apunte/scripts/`). Las demostraciones y los desarrollos
largos van completos a «En profundidad», sin resumirlos. Las subsecciones «En el CAD» pueden llevar
capturas y una consigna paso a paso. Lo que no cambia: «La idea» sigue siendo breve (abre el
capítulo, no lo reemplaza); nada de relleno (cada página nueva aporta una imagen, un caso o una
cuenta que el lector no tenía); siguen vigentes las reglas de voz, el contador de términos de campo
y la compilación sin errores. Un capítulo ya cerrado que ganaría con más espacio se anota en
`apunte/ESTADO_NOTAS.md` (sale al final de `ESTADO.md`) y no se reabre sin aprobación. En cada
cierre de capítulo se anotan las páginas antes y después y qué se agregó con el espacio nuevo.

## 9. Etiquetas y definiciones [chequeos 7 y 8]

- Etiquetas con nombre, nunca numéricas: `\label{cap:repaso-algebra}`, no `\label{cap:03}`. Las
  claves `apunte:` de las fichas (`clases/*.md`) y del mapa (`mapa/_fragmentos/*.yaml`) son el
  nombre sin `cap:` (`"repaso-algebra"`).
- Cada definición aparece una sola vez en el apunte: dos `\begin{definicion}[Título]` con el mismo
  título en archivos distintos son un error. Donde haga falta recordarla, una frase y un `\ref`.

## 10. Material interactivo [alcance interactivo]

`uv run python apunte/scripts/estilo.py --alcance interactivo` aplica las mismas normas a la prosa que
ve el lector fuera del apunte: las cadenas de texto de `unidades/*.py` (sin docstrings ni código), las
fichas de `clases/`, `mapa/` (los `.md` y los valores de los `.yaml`), los CDATA de `moodle/` y los
`.md` de la raíz. Corre los chequeos 1 (tilde), 2 (comillas rectas), 3 (decimal; no cuenta los números
de sección ni los de problema, sección o capítulo entre paréntesis, como «los problemas (12.5)»),
5 (es decir), 6 (Desarrollo.), 10 (instrumentos, que acá bloquea), 12 («desaprender») y 13 (imperativo
de tú o de usted). Con `--estricto` es bloqueante en la CI (`.github/workflows/pages.yml`), igual que el
alcance del apunte; `--todo` corre los dos.
