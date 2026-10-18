"""GENERADO por tools/merge_banco.py desde unidades/_banco/bloque_*.py: no editar a mano.

Banco de autoevaluación: 6 preguntas por unidad (2 elementales, 2 medias, 2 avanzadas), 4 opciones
con explicación cada una. Lo importa cb104.py y tools/build.py lo embebe en cada export WASM.
"""

BANCO_AUTOEVALUACION = {'00_desaprender_el_cbc': [{'id': '00_e1',
                            'nivel': 'elemental',
                            'enunciado': 'La cota de una loma es $h = 3x + y$, o sea la forma lineal $w^T = '
                                         '(3, 1)$. Si la dibujamos sobre el plano de la parcela, ¿qué vemos?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Una familia de rectas paralelas equiespaciadas, las '
                                                   'curvas de nivel $3x + y = c$: una regla graduada tirada '
                                                   'sobre el plano.',
                                          'correcta': True,
                                          'explicacion': 'Una forma lineal se ve por sus conjuntos de nivel, '
                                                         'que son rectas paralelas a distancia $1/\\lvert '
                                                         'w\\rvert$; leer un punto es ver qué marca lo '
                                                         'atraviesa.'},
                                         {'id': 'b',
                                          'texto': 'Una flecha clavada en el origen con extremo en $(3, 1)$, '
                                                   'como cualquier vector de $\\mathbb R^2$.',
                                          'correcta': False,
                                          'explicacion': 'Eso es tratar la fila como columna: los números de '
                                                         'una forma no son una flecha, y sin métrica no hay '
                                                         'manera de convertirlos en una.'},
                                         {'id': 'c',
                                          'texto': 'Una sola recta, la $3x + y = 0$, porque una forma lineal '
                                                   'es una ecuación y una ecuación es una recta.',
                                          'correcta': False,
                                          'explicacion': 'Esa recta es sólo la marca cero de la regla (el '
                                                         'núcleo de $w^T$); la forma entera asigna un número '
                                                         'a cada punto del plano, no sólo a los que dan '
                                                         '$0$.'},
                                         {'id': 'd',
                                          'texto': 'El número $3 \\cdot 1 + 1 \\cdot 1 = 4$, la lectura de '
                                                   'la forma en el punto $(1, 1)$.',
                                          'correcta': False,
                                          'explicacion': 'Esa es una sola lectura, el valor de la forma en '
                                                         'un punto; la forma es la función entera, no uno de '
                                                         'sus resultados.'}],
                            'rubrica': 'Productos/elemental: una forma lineal es una regla graduada, familia '
                                       'de rectas paralelas equiespaciadas'},
                           {'id': '00_e2',
                            'nivel': 'elemental',
                            'enunciado': 'Los giros de la estación total alrededor de su eje vertical, con '
                                         'la operación hacer uno y después el otro, forman un grupo. ¿Cuál '
                                         'es la inversa de girar $30°$ y respecto de qué operación lo es?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Girar $-30°$, respecto de la composición: hecho después '
                                                   'del primero da el neutro, que es no girar.',
                                          'correcta': True,
                                          'explicacion': 'La inversa es siempre respecto de una operación: '
                                                         'compuesto con el giro de $30°$ devuelve el '
                                                         'elemento neutro, y el neutro de componer giros es '
                                                         'el giro nulo.'},
                                         {'id': 'b',
                                          'texto': 'Girar $\\tfrac{1}{30}$ de grado, porque la inversa de un '
                                                   'elemento es su recíproco.',
                                          'correcta': False,
                                          'explicacion': 'El recíproco es la inversa respecto del producto '
                                                         'de números; acá la operación es componer giros, y '
                                                         '$\\tfrac{1}{30}°$ compuesto con $30°$ da '
                                                         '$30\\tfrac{1}{30}°$, no el neutro.'},
                                         {'id': 'c',
                                          'texto': 'Girar $150°$, porque $30° + 150° = 180°$ y media vuelta '
                                                   'deshace lo hecho.',
                                          'correcta': False,
                                          'explicacion': 'Media vuelta no es el neutro: deja la estación '
                                                         'apuntando al revés. El neutro es el giro de $0°$, '
                                                         'y lo que suma $0°$ con $30°$ es $-30°$.'},
                                         {'id': 'd',
                                          'texto': 'No tiene inversa: una vez girada, la estación no vuelve '
                                                   'sola a la posición inicial.',
                                          'correcta': False,
                                          'explicacion': 'Que no vuelva sola no quita que exista el giro que '
                                                         'la devuelve; en un grupo todo elemento tiene '
                                                         'inversa, y girar $-30°$ lo es.'}],
                            'rubrica': 'SVD/medio: la inversa es siempre respecto de una operacion (suma, '
                                       'producto, composicion)'},
                           {'id': '00_m1',
                            'nivel': 'medio',
                            'enunciado': 'Dibujamos el plano con el Este estirado por 2, $A = '
                                         '\\mathrm{diag}(2, 1)$. La cota es la regla $w^T = (1, 1)$ y el '
                                         'mojón está en $x = (1, 2)$, cota $3$. ¿Qué regla hay que dibujar '
                                         'en el papel para que el mojón dibujado $Ax = (2, 2)$ siga leyendo '
                                         'cota $3$?',
                            'opciones': [{'id': 'a',
                                          'texto': '$(\\tfrac12, 1)$, que es $w^T A^{-1}$: en efecto '
                                                   '$\\tfrac12 \\cdot 2 + 1 \\cdot 2 = 3$.',
                                          'correcta': True,
                                          'explicacion': 'La forma se arrastra con la inversa y por la '
                                                         "derecha, $w'^T = w^T A^{-1}$, justamente para que "
                                                         "$w'^T(Ax) = w^T x$ y la lectura no cambie."},
                                         {'id': 'b',
                                          'texto': '$(2, 1)$, que es $Aw$: la regla va con la misma matriz '
                                                   'que los puntos.',
                                          'correcta': False,
                                          'explicacion': 'Eso mueve la fila como si fuera un punto; con $(2, '
                                                         '1)$ el mojón dibujado lee $2 \\cdot 2 + 1 \\cdot 2 '
                                                         '= 6$, el doble de su cota.'},
                                         {'id': 'c',
                                          'texto': '$(1, 1)$, la misma: la cota es del terreno y no depende '
                                                   'de cómo dibujemos el plano.',
                                          'correcta': False,
                                          'explicacion': 'La cota del mojón no depende del dibujo, pero la '
                                                         'regla escrita en la grilla del papel sí: con $(1, '
                                                         '1)$ el punto $(2, 2)$ lee $4$, no $3$.'},
                                         {'id': 'd',
                                          'texto': '$(2, 2)$, que es $Ax$: regla y mojón van juntos al mismo '
                                                   'lugar.',
                                          'correcta': False,
                                          'explicacion': '$(2, 2)$ es el mojón dibujado, un punto; confunde '
                                                         'el objeto que se lee con la regla que lo lee, y '
                                                         '$(2, 2)\\cdot(2, 2) = 8$.'}],
                            'rubrica': 'Productos/medio: las formas lineales se transforman del lado '
                                       'contrario que los vectores (las rectas de nivel se arrastran con la '
                                       'figura)'},
                           {'id': '00_m2',
                            'nivel': 'medio',
                            'enunciado': 'Movemos la estación total $5$ m al Este: cada mojón $(x, y)$ pasa '
                                         'a leerse $(x - 5, y)$. ¿Por qué esa traslación no es una '
                                         'transformación lineal del plano?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Porque no manda el origen al origen: el $(0, 0)$ pasa a '
                                                   '$(-5, 0)$, y toda lineal conserva el cero.',
                                          'correcta': True,
                                          'explicacion': '$T(0) = T(0 \\cdot v) = 0 \\cdot T(v) = 0$ para '
                                                         'cualquier lineal; la traslación lo viola, y por '
                                                         'eso hace falta homogeneizar para escribirla como '
                                                         'matriz.'},
                                         {'id': 'b',
                                          'texto': 'Porque no conserva las distancias entre mojones: al '
                                                   'correr todo $5$ m los largos cambian.',
                                          'correcta': False,
                                          'explicacion': 'Una traslación conserva todas las distancias y los '
                                                         'ángulos; además, conservar distancias no es lo que '
                                                         'define a una lineal (el corte es lineal y no las '
                                                         'conserva).'},
                                         {'id': 'c',
                                          'texto': 'Porque no tiene inversa: una vez corridos los mojones no '
                                                   'se puede volver atrás.',
                                          'correcta': False,
                                          'explicacion': 'Correr $5$ m al Oeste la deshace; ser invertible '
                                                         'no es ni necesario ni suficiente para ser lineal '
                                                         '(la proyección es lineal y no es invertible).'},
                                         {'id': 'd',
                                          'texto': 'Porque cambia los ángulos entre los lados de la parcela '
                                                   'al correrla.',
                                          'correcta': False,
                                          'explicacion': 'Correr la parcela entera deja idénticos sus '
                                                         'ángulos; la falla no está en lo que conserva sino '
                                                         'en que el cero no queda en el cero.'}],
                            'rubrica': 'Productos/medio: el cero siempre va al cero (ladrillo 3, espacio '
                                       'afin vs. vectorial)'},
                           {'id': '00_a1',
                            'nivel': 'avanzado',
                            'enunciado': 'El plano se dibuja con el Este estirado por 2, $A = '
                                         '\\mathrm{diag}(2, 1)$. Queremos medir largos y ángulos de terreno '
                                         "sobre el papel con $\\langle a, b\\rangle_{G'} = a^T G' b$. ¿Qué "
                                         "matriz $G'$ hay que usar?",
                            'opciones': [{'id': 'a',
                                          'texto': "$G' = A^{-T} A^{-1} = \\mathrm{diag}(\\tfrac14, 1)$: "
                                                   'cada paso Este del papel vale medio metro.',
                                          'correcta': True,
                                          'explicacion': "Si $x' = Ax$, el largo de terreno es $x^T x = x'^T "
                                                         "A^{-T} A^{-1} x'$; con $A^{-1} = "
                                                         '\\mathrm{diag}(\\tfrac12, 1)$ queda '
                                                         '$\\mathrm{diag}(\\tfrac14, 1)$, y con ella la '
                                                         'subida $(2, 1)$ y la marca $(2, -1)$ dan $1 - 1 = '
                                                         '0$: recto.'},
                                         {'id': 'b',
                                          'texto': "$G' = A^T A = \\mathrm{diag}(4, 1)$: la métrica se "
                                                   'transforma con la misma matriz que los puntos.',
                                          'correcta': False,
                                          'explicacion': '$A^T A$ es la métrica que pondría al terreno lo '
                                                         'que el papel mide con $I$, el sentido contrario: '
                                                         'con ella un paso Este del papel valdría dos metros '
                                                         'en vez de medio.'},
                                         {'id': 'c',
                                          'texto': "$G' = A = \\mathrm{diag}(2, 1)$: la propia deformación "
                                                   'del dibujo es la métrica.',
                                          'correcta': False,
                                          'explicacion': '$A$ mueve puntos, no mide; una métrica es '
                                                         'simétrica definida positiva y relaciona dos copias '
                                                         'del mismo vector, por eso aparece elevada al '
                                                         'cuadrado ($A^{-T}A^{-1}$).'},
                                         {'id': 'd',
                                          'texto': "$G' = I$: la cuenta $x_1 x_2 + y_1 y_2$ mide bien en "
                                                   'cualquier grilla.',
                                          'correcta': False,
                                          'explicacion': 'Con $I$ el ángulo recto del terreno entre $(2, 1)$ '
                                                         'y $(2, -1)$ se mide como $53.1°$; la suma de '
                                                         'productos mide de verdad sólo en una grilla '
                                                         'ortonormal.'}],
                            'rubrica': 'SVD/avanzado: no hay base privilegiada a priori; lo unico especial '
                                       'de la canonica es que el producto interno es suma de productos'},
                           {'id': '00_a2',
                            'nivel': 'avanzado',
                            'enunciado': 'En el mojón $(2, 2)$ de la loma $h = 100 - \\tfrac{x^2 + y^2}{4}$ '
                                         'el gradiente es $(-1, -1)$, así que en el terreno el agua baja '
                                         'hacia $(1, 1)$. Dibujamos el plano con el Este estirado por 2. '
                                         '¿Hacia dónde dibujamos la flecha de la bajada más empinada?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Hacia $(2, 1)$: la bajada real $(1, 1)$ pasada por $A = '
                                                   '\\mathrm{diag}(2, 1)$, aunque en el papel no se vea '
                                                   'perpendicular a las elipses.',
                                          'correcta': True,
                                          'explicacion': 'La bajada es un desplazamiento del terreno y viaja '
                                                         'con $A$ como cualquier punto; el ángulo recto con '
                                                         'la curva de nivel vive en la métrica del terreno, '
                                                         'no en la del papel.'},
                                         {'id': 'b',
                                          'texto': 'Hacia $(1, 1)$: los dos números del gradiente, puestos '
                                                   'tal cual como flecha en el dibujo.',
                                          'correcta': False,
                                          'explicacion': 'Eso trata la forma $\\nabla h$ como si fuera un '
                                                         'vector en una grilla que no mide metros; ese trazo '
                                                         'del papel es el desplazamiento $(\\tfrac12, 1)$ '
                                                         'del terreno, que no es la bajada más empinada.'},
                                         {'id': 'c',
                                          'texto': 'Hacia $(1, 2)$: perpendicular a las curvas de nivel tal '
                                                   'como se ven dibujadas.',
                                          'correcta': False,
                                          'explicacion': '$(1, 2)$ es proporcional a la regla arrastrada '
                                                         '$\\pm(\\tfrac12, 1)$, leída como flecha: '
                                                         'perpendicular con $G = I$, la métrica del papel, '
                                                         'pero el papel está estirado y ese ángulo recto es '
                                                         'falso en el terreno.'},
                                         {'id': 'd',
                                          'texto': 'Hacia $(2, -1)$: a lo largo de la curva de nivel que '
                                                   'pasa por el mojón.',
                                          'correcta': False,
                                          'explicacion': 'A lo largo de la curva de nivel la cota no cambia; '
                                                         'es la marca de la regla, y la bajada la cruza en '
                                                         'vez de seguirla.'}],
                            'rubrica': "Productos/avanzado: el gradiente es una forma lineal; 'perpendicular "
                                       "a la curva de nivel' es una frase sobre G^{-1} grad f"}],
 '01a_punto_quieto': [{'id': '01a_e1',
                       'nivel': 'elemental',
                       'enunciado': 'Plantamos la estación total en el origen de la obra, pero con su eje '
                                    '$x$ girado $30°$ antihorario respecto del frente. El mojón no se tocó. '
                                    '¿Qué cambia?',
                       'opciones': [{'id': 'a',
                                     'texto': 'Sus coordenadas, no su lugar: el mismo mojón tiene otra '
                                              'etiqueta en los ejes nuevos.',
                                     'correcta': True,
                                     'explicacion': 'Una coordenada es un número respecto de unos ejes; si '
                                                    'giran los ejes y el punto queda, cambia la lectura y no '
                                                    'el pedazo de hierro (rotación pasiva).'},
                                    {'id': 'b',
                                     'texto': 'Su lugar: el mojón gira $30°$ alrededor del origen junto con '
                                              'los ejes.',
                                     'correcta': False,
                                     'explicacion': 'Eso es la rotación activa, girar el punto con los ejes '
                                                    'quietos; acá giró el instrumento y el mojón sigue '
                                                    'clavado donde estaba.'},
                                    {'id': 'c',
                                     'texto': 'Nada: el mojón está quieto, así que sus coordenadas tienen '
                                              'que ser las mismas.',
                                     'correcta': False,
                                     'explicacion': 'Si no cambiaran, la obra y la estación dirían lo mismo '
                                                    'y no habría que transformar lecturas; la coordenada '
                                                    'depende de los ejes aunque el punto no se mueva.'},
                                    {'id': 'd',
                                     'texto': 'Su distancia al origen, porque se mide sobre ejes distintos.',
                                     'correcta': False,
                                     'explicacion': 'La distancia es del terreno y una rotación la conserva: '
                                                    "$\\sqrt{x'^2 + y'^2} = \\sqrt{x^2 + y^2}$ en cualquier "
                                                    'par de ejes girados.'}],
                       'rubrica': 'Cambio de base/elemental: la misma flecha medida con otra grilla'},
                      {'id': '01a_e2',
                       'nivel': 'elemental',
                       'enunciado': 'El mojón está en $(2, 0)$ en los ejes de la obra. La estación tiene sus '
                                    'ejes girados $90°$ antihorario. ¿Qué lee la estación?',
                       'opciones': [{'id': 'a',
                                     'texto': "$(0, -2)$: el mojón queda sobre el semieje $y'$ negativo, a "
                                              'distancia $2$.',
                                     'correcta': True,
                                     'explicacion': "Con los ejes girados $90°$, $x'$ apunta hacia $+y$ e "
                                                    "$y'$ hacia $-x$; el mojón sobre $+x$ cae sobre $-y'$, y "
                                                    'la cuenta $R(90°)^T(2, 0)$ da lo mismo.'},
                                    {'id': 'b',
                                     'texto': "$(0, 2)$: el mojón queda sobre el semieje $y'$ positivo, a "
                                              'distancia $2$.',
                                     'correcta': False,
                                     'explicacion': '$(0, 2)$ es $R(90°)(2, 0)$: el punto girado $90°$ con '
                                                    'los ejes quietos. Girar los ejes $+90°$ se lee como '
                                                    'girar el punto $-90°$.'},
                                    {'id': 'c',
                                     'texto': "$(-2, 0)$: el eje $x'$ apunta al revés del $x$ de la obra.",
                                     'correcta': False,
                                     'explicacion': 'Eso sería un giro de $180°$ de los ejes; con $90°$ el '
                                                    "eje $x'$ apunta hacia $+y$, y el mojón no está sobre "
                                                    'esa dirección sino perpendicular a ella.'},
                                    {'id': 'd',
                                     'texto': '$(2, 0)$: el mojón no se movió y la lectura es la misma.',
                                     'correcta': False,
                                     'explicacion': "El mojón no se movió, pero sobre el eje $x'$ (que "
                                                    'apunta hacia $+y$) su sombra es $0$: la lectura cambia '
                                                    'aunque el lugar no.'}],
                       'rubrica': 'Rotaciones/elemental: las matrices y las transformaciones lineales tienen '
                                  'una correspondencia 1 a 1'},
                      {'id': '01a_m1',
                       'nivel': 'medio',
                       'enunciado': 'Giramos los ejes de la estación $+\\theta$ y el mojón $P$ queda quieto. '
                                    '¿Qué cuenta da lo que lee la estación?',
                       'opciones': [{'id': 'a',
                                     'texto': '$R(\\theta)^T P$, que es lo mismo que $R(-\\theta)P$: como si '
                                              'el punto hubiera girado $-\\theta$ en los ejes viejos.',
                                     'correcta': True,
                                     'explicacion': 'Cada coordenada nueva es la sombra de $P$ sobre un eje '
                                                    'girado, o sea el producto interno con una columna de '
                                                    '$R(\\theta)$; apiladas, esas cuentas son $R^T P$.'},
                                    {'id': 'b',
                                     'texto': '$R(\\theta)P$: el punto se expresa aplicándole el giro de los '
                                              'ejes.',
                                     'correcta': False,
                                     'explicacion': '$R(\\theta)P$ mueve el punto $+\\theta$ con los ejes '
                                                    'quietos (activa); con los ejes girados $+\\theta$ los '
                                                    'números cambian al revés, con $R(-\\theta)$.'},
                                    {'id': 'c',
                                     'texto': '$P$ sin cambios: el mojón no se movió y la matriz sólo hace '
                                              'falta si se mueve.',
                                     'correcta': False,
                                     'explicacion': 'La matriz convierte etiquetas entre dos sistemas de '
                                                    'ejes; el punto quieto tiene dos etiquetas distintas y '
                                                    'la cuenta pasa de una a la otra.'},
                                    {'id': 'd',
                                     'texto': '$-R(\\theta)P$: el giro de los ejes se compensa cambiando el '
                                              'signo.',
                                     'correcta': False,
                                     'explicacion': 'Cambiar el signo es girar $180°$ más, no deshacer el '
                                                    'giro; lo que invierte una rotación es su transpuesta, '
                                                    'no su opuesta.'}],
                       'rubrica': 'Rotaciones/medio: hay transformaciones que se definen completamente por '
                                  'que propiedades de los objetos transformados mantienen'},
                      {'id': '01a_m2',
                       'nivel': 'medio',
                       'enunciado': 'Sabemos que la inversa de $R(\\theta) = \\begin{pmatrix} \\cos\\theta & '
                                    '-\\sin\\theta \\\\ \\sin\\theta & \\cos\\theta \\end{pmatrix}$ es su '
                                    'transpuesta. ¿Qué le pasa a la matriz al transponerla, y qué giro '
                                    'resulta?',
                       'opciones': [{'id': 'a',
                                     'texto': 'Se cambia de lugar el signo del seno: queda $R(-\\theta)$, el '
                                              'mismo giro para el otro lado.',
                                     'correcta': True,
                                     'explicacion': 'Transponer intercambia $-\\sin\\theta$ y '
                                                    '$\\sin\\theta$, y como $\\sin(-\\theta) = '
                                                    '-\\sin\\theta$ y $\\cos(-\\theta) = \\cos\\theta$, la '
                                                    'transpuesta es exactamente $R(-\\theta)$.'},
                                    {'id': 'b',
                                     'texto': 'Se cambia el signo del coseno: queda $R(180° - \\theta)$.',
                                     'correcta': False,
                                     'explicacion': 'El coseno está en la diagonal y no se mueve al '
                                                    'transponer; cambiarle el signo daría una matriz con '
                                                    '$\\det = 1$ pero de otro ángulo, no la inversa.'},
                                    {'id': 'c',
                                     'texto': 'Nada: $R(\\theta)$ es simétrica, así que la transpuesta es la '
                                              'misma matriz y es su propia inversa.',
                                     'correcta': False,
                                     'explicacion': '$R(\\theta)$ es ortogonal, no simétrica (salvo $\\theta '
                                                    '= 0°$ o $180°$); si fuera su propia inversa, girar dos '
                                                    'veces $\\theta$ no movería nada.'},
                                    {'id': 'd',
                                     'texto': 'Se intercambian senos y cosenos: queda $R(90° - \\theta)$.',
                                     'correcta': False,
                                     'explicacion': 'Transponer intercambia filas por columnas, no las '
                                                    'funciones; además $R(90° - \\theta)$ compuesta con '
                                                    '$R(\\theta)$ da $R(90°)$, no la identidad.'}],
                       'rubrica': 'Rotaciones/elemental: las rotaciones son matrices ortogonales (A^T A = '
                                  'Id) con determinante mayor a 0'},
                      {'id': '01a_a1',
                       'nivel': 'avanzado',
                       'enunciado': 'El mojón es $(4, 3)$ en la obra. Una estación con ejes girados un '
                                    "ángulo que no conocemos lee $(x', y')$. Sin saber el ángulo, ¿qué "
                                    'podemos afirmar de la lectura?',
                       'opciones': [{'id': 'a',
                                     'texto': "$x'^2 + y'^2 = 25$: la distancia al origen no depende de los "
                                              'ejes.',
                                     'correcta': True,
                                     'explicacion': '$R^T R = I$ implica $\\lvert R^T P\\rvert = \\lvert '
                                                    'P\\rvert$ para cualquier $\\theta$; el mojón está a $5$ '
                                                    'm del origen en cualquier sistema girado.'},
                                    {'id': 'b',
                                     'texto': "$x' + y' = 7$: la suma de las coordenadas no depende de los "
                                              'ejes.',
                                     'correcta': False,
                                     'explicacion': 'Sumar coordenadas no mide nada geométrico: con los ejes '
                                                    'girados $90°$ la lectura es $(3, -4)$ y la suma da '
                                                    '$-1$.'},
                                    {'id': 'c',
                                     'texto': "$x' \\cdot y' = 12$: el producto de las coordenadas no "
                                              'depende de los ejes.',
                                     'correcta': False,
                                     'explicacion': 'El producto de coordenadas tampoco es invariante: con '
                                                    'ejes girados $90°$ la lectura $(3, -4)$ da $-12$, y con '
                                                    '$45°$ los números ni siquiera son enteros.'},
                                    {'id': 'd',
                                     'texto': "$(x', y') = (3, 4)$: con ejes distintos las coordenadas se "
                                              'intercambian.',
                                     'correcta': False,
                                     'explicacion': 'Intercambiar coordenadas es el espejo respecto de la '
                                                    'diagonal, no un giro; un giro mezcla las dos con senos '
                                                    'y cosenos y el resultado depende del ángulo.'}],
                       'rubrica': 'Rotaciones/elemental: el producto interno puede servir como base para '
                                  'definir tipos de transformaciones (lo que conserva una ortogonal)'},
                      {'id': '01a_a2',
                       'nivel': 'avanzado',
                       'enunciado': 'Primero giramos los ejes $+30°$ y leemos el mojón $P$. Después, con '
                                    'esos ejes nuevos quietos, giramos el mojón $+30°$ y leemos otra vez. '
                                    '¿Qué da la segunda lectura?',
                       'opciones': [{'id': 'a',
                                     'texto': 'Las coordenadas originales de $P$: la pasiva de $+30°$ y la '
                                              'activa de $+30°$ se cancelan.',
                                     'correcta': True,
                                     'explicacion': 'La primera lectura es $R(30°)^T P$ y la segunda '
                                                    '$R(30°)\\,R(30°)^T P = P$: girar los ejes $+\\theta$ '
                                                    'equivale a girar el punto $-\\theta$, y el giro activo '
                                                    '$+\\theta$ lo deshace.'},
                                    {'id': 'b',
                                     'texto': '$R(60°)P$: dos giros de $30°$ en el mismo sentido se suman.',
                                     'correcta': False,
                                     'explicacion': 'Se suman sólo si los dos son activos; el primero fue de '
                                                    'los ejes, que sobre los números actúa como $R(-30°)$, y '
                                                    '$-30° + 30° = 0°$.'},
                                    {'id': 'c',
                                     'texto': '$R(60°)^T P$: dos giros de ejes de $30°$ se acumulan en '
                                              '$60°$.',
                                     'correcta': False,
                                     'explicacion': 'El segundo giro no fue de los ejes sino del mojón; una '
                                                    'pasiva seguida de una activa del mismo ángulo no '
                                                    'acumula, se cancela.'},
                                    {'id': 'd',
                                     'texto': '$R(30°)P$: el giro del mojón es el único que mueve algo, así '
                                              'que es el único que cuenta.',
                                     'correcta': False,
                                     'explicacion': 'Que el primer giro no mueva el mojón no significa que '
                                                    'no cambie los números; la lectura ya venía transformada '
                                                    'por $R(30°)^T$ antes del giro activo.'}],
                       'rubrica': 'Rotaciones/medio: combinacion de rotaciones son rotaciones (y la pasiva '
                                  'es la inversa de la activa)'}],
 '01b_rotacion_plano': [{'id': '01b_e1',
                         'nivel': 'elemental',
                         'enunciado': 'Giramos la parcela entera alrededor del origen con los ejes quietos. '
                                      '¿Qué conserva una rotación del plano, y qué la distingue de un '
                                      'espejo?',
                         'opciones': [{'id': 'a',
                                       'texto': 'Conserva distancias y ángulos; la distingue del espejo el '
                                                'determinante: $+1$ el giro, $-1$ el espejo.',
                                       'correcta': True,
                                       'explicacion': 'Las dos son ortogonales ($A^T A = I$) y conservan '
                                                      'regla y transportador; el espejo da vuelta la hoja, y '
                                                      'eso lo delata el área con signo del cuadrado '
                                                      'unitario.'},
                                      {'id': 'b',
                                       'texto': 'Conserva distancias pero no ángulos; el espejo conserva '
                                                'ángulos pero no distancias.',
                                       'correcta': False,
                                       'explicacion': 'Conservar todas las distancias obliga a conservar los '
                                                      'ángulos (ley del coseno), y tanto el giro como el '
                                                      'espejo conservan las dos cosas.'},
                                      {'id': 'c',
                                       'texto': 'Conserva el área, y eso basta; el espejo no conserva el '
                                                'área.',
                                       'correcta': False,
                                       'explicacion': 'El corte $\\begin{pmatrix} 1 & 0.5 \\\\ 0 & 1 '
                                                      '\\end{pmatrix}$ conserva el área y no es rotación; el '
                                                      'espejo también conserva el área, sólo le cambia el '
                                                      'signo.'},
                                      {'id': 'd',
                                       'texto': 'Conserva distancias y ángulos, igual que el espejo; nada '
                                                'las distingue salvo el nombre.',
                                       'correcta': False,
                                       'explicacion': 'Las distingue la orientación: una parcela girada se '
                                                      'superpone con la original deslizándola; la reflejada '
                                                      'no, hay que darla vuelta como un guante.'}],
                         'rubrica': 'Rotaciones/medio: hay transformaciones que se definen completamente por '
                                    'que propiedades de los objetos transformados mantienen'},
                        {'id': '01b_e2',
                         'nivel': 'elemental',
                         'enunciado': 'Pensamos el punto $(2, 1)$ como el complejo $z = 2 + i$ y lo '
                                      'multiplicamos por $i$. ¿Qué punto obtenemos y qué movimiento es?',
                         'opciones': [{'id': 'a',
                                       'texto': '$-1 + 2i$, el punto $(-1, 2)$: un cuarto de vuelta '
                                                'antihorario.',
                                       'correcta': True,
                                       'explicacion': '$(2 + i)\\,i = 2i + i^2 = -1 + 2i$; el módulo sigue '
                                                      'siendo $\\sqrt5$ y el argumento subió $90°$, lo mismo '
                                                      'que hace $R(90°)$ con $(2, 1)$.'},
                                      {'id': 'b',
                                       'texto': '$1 - 2i$, el punto $(1, -2)$: un cuarto de vuelta horario.',
                                       'correcta': False,
                                       'explicacion': '$1 - 2i$ es $(2 + i)(-i)$: multiplicar por $-i$ gira '
                                                      '$-90°$. Multiplicar por $i$ suma $+90°$ al argumento, '
                                                      'antihorario.'},
                                      {'id': 'c',
                                       'texto': '$1 + 2i$, el punto $(1, 2)$: las coordenadas se '
                                                'intercambian.',
                                       'correcta': False,
                                       'explicacion': 'Eso olvida que $i^2 = -1$: sin ese signo lo que queda '
                                                      'es el espejo respecto de la diagonal $y = x$, que da '
                                                      'vuelta la figura en vez de girarla.'},
                                      {'id': 'd',
                                       'texto': '$2 - i$, el punto $(2, -1)$: un espejo respecto del eje '
                                                'real.',
                                       'correcta': False,
                                       'explicacion': '$2 - i$ es el conjugado $\\bar z$, un espejo respecto '
                                                      'del eje $x$ con $\\det = -1$; multiplicar por $i$ no '
                                                      'cambia signos sueltos, gira.'}],
                         'rubrica': 'Rotaciones/elemental: multiplicar por i es rotar pi/2'},
                        {'id': '01b_m1',
                         'nivel': 'medio',
                         'enunciado': 'Giramos la parcela $90°$ antihorario alrededor del origen. ¿A dónde '
                                      'va el vértice del frente, $(4, 1)$?',
                         'opciones': [{'id': 'a',
                                       'texto': 'A $(-1, 4)$: cuatro veces la imagen de $e_1$ más una vez la '
                                                'imagen de $e_2$.',
                                       'correcta': True,
                                       'explicacion': 'Las columnas de $R(90°)$ son $Re_1 = (0, 1)$ y $Re_2 '
                                                      '= (-1, 0)$, así que $(4, 1) \\mapsto 4(0, 1) + 1(-1, '
                                                      '0) = (-1, 4)$; un cuarto de vuelta es $(x, y) '
                                                      '\\mapsto (-y, x)$.'},
                                      {'id': 'b',
                                       'texto': 'A $(1, -4)$: el $4$ que estaba sobre $x$ pasa al eje $y$, '
                                                'hacia abajo.',
                                       'correcta': False,
                                       'explicacion': '$(1, -4)$ es el giro horario, $R(-90°)(4, 1)$; '
                                                      'antihorario va de $+x$ hacia $+y$, así que $(4, 0)$ '
                                                      'tiene que ir a $(0, 4)$.'},
                                      {'id': 'c',
                                       'texto': 'A $(1, 4)$: con un cuarto de vuelta las coordenadas se '
                                                'intercambian.',
                                       'correcta': False,
                                       'explicacion': 'Intercambiar sin signo es el espejo respecto de $y = '
                                                      'x$, con $\\det = -1$; falta el menos que distingue al '
                                                      'giro, $(x, y) \\mapsto (-y, x)$.'},
                                      {'id': 'd',
                                       'texto': 'A $(4, -1)$: el vértice pasa al otro lado del eje $x$.',
                                       'correcta': False,
                                       'explicacion': 'Cambiar el signo de una sola coordenada es la '
                                                      'reflexión $\\mathrm{diag}(1, -1)$; un giro mezcla las '
                                                      'dos coordenadas, las dos nuevas dependen de las dos '
                                                      'viejas.'}],
                         'rubrica': 'Productos/elemental: una transformacion lineal tiene una unica matriz; '
                                    'las columnas dicen adonde van los ejes'},
                        {'id': '01b_m2',
                         'nivel': 'medio',
                         'enunciado': 'El corte $M = \\begin{pmatrix} 1 & 0.5 \\\\ 0 & 1 \\end{pmatrix}$ '
                                      'tiene $\\det M = 1$ y manda el cuadrado unitario a un paralelogramo '
                                      'de área $1$. ¿Es una rotación?',
                         'opciones': [{'id': 'a',
                                       'texto': 'No: $\\det = 1$ no alcanza; falla $M^T M = I$, y $M$ no '
                                                'conserva en general largos ni ángulos.',
                                       'correcta': True,
                                       'explicacion': '$M e_2 = (0.5, 1)$ tiene largo $\\sqrt{1.25}$ y ya no '
                                                      'es perpendicular a $M e_1 = (1, 0)$; la rotación es '
                                                      'ortogonal con $\\det = +1$, y acá sólo se cumple lo '
                                                      'segundo.'},
                                      {'id': 'b',
                                       'texto': 'Sí: toda matriz con determinante $1$ es una rotación, '
                                                'porque el determinante dice que el área y la orientación se '
                                                'conservan.',
                                       'correcta': False,
                                       'explicacion': 'Área y orientación son necesarias pero no '
                                                      'suficientes; el corte las conserva y aun así deforma: '
                                                      '$\\det = 1$ es la condición que separa giro de espejo '
                                                      'entre las ortogonales, no entre todas las matrices.'},
                                      {'id': 'c',
                                       'texto': 'No: una rotación sólo puede tener coeficientes $0$, $1$ o '
                                                '$-1$, y el $0.5$ la descarta.',
                                       'correcta': False,
                                       'explicacion': '$R(30°)$ tiene coeficientes $0.866$ y $0.5$ y es una '
                                                      'rotación; lo que descarta a $M$ no es el valor $0.5$ '
                                                      'sino que sus columnas no son perpendiculares de largo '
                                                      '$1$.'},
                                      {'id': 'd',
                                       'texto': 'Sí: conserva el área, y el área es la única propiedad que '
                                                'una rotación tiene que mantener.',
                                       'correcta': False,
                                       'explicacion': 'Lo que define a la rotación es conservar el producto '
                                                      'interno (largos y ángulos de una vez) sin dar vuelta '
                                                      'la hoja; el área se conserva como consecuencia, no '
                                                      'como definición.'}],
                         'rubrica': 'Rotaciones/elemental: las rotaciones son matrices ortogonales (A^T A = '
                                    'Id) con determinante mayor a 0'},
                        {'id': '01b_a1',
                         'nivel': 'avanzado',
                         'enunciado': 'Giramos la parcela $30°$ y después $60°$, o al revés: en los dos '
                                      'órdenes queda $R(90°)$. ¿Por qué las rotaciones del plano conmutan, '
                                      'si el producto de matrices en general no?',
                         'opciones': [{'id': 'a',
                                       'texto': 'Porque $R(\\alpha)$ es multiplicar por $e^{i\\alpha}$, y el '
                                                'producto de complejos conmuta: $e^{i\\alpha}e^{i\\beta} = '
                                                'e^{i(\\alpha + \\beta)}$.',
                                       'correcta': True,
                                       'explicacion': 'Las matrices $\\begin{pmatrix} a & -b \\\\ b & a '
                                                      '\\end{pmatrix}$ son el cuerpo $\\mathbb C$ con otro '
                                                      'ropaje, y en un cuerpo el producto conmuta; los '
                                                      'ángulos se suman en cualquier orden.'},
                                      {'id': 'b',
                                       'texto': 'Porque el producto de matrices $2 \\times 2$ siempre '
                                                'conmuta; la falta de conmutatividad aparece recién en $3 '
                                                '\\times 3$.',
                                       'correcta': False,
                                       'explicacion': 'El espejo $\\mathrm{diag}(1, -1)$ y $R(90°)$ son $2 '
                                                      '\\times 2$ y no conmutan: en un orden dan el espejo '
                                                      'de $y = x$, en el otro el de $y = -x$.'},
                                      {'id': 'c',
                                       'texto': 'No conmutan en general; sólo coincide en este ejemplo '
                                                'porque $30° + 60° = 90°$ es un ángulo especial.',
                                       'correcta': False,
                                       'explicacion': '$R(\\alpha)R(\\beta) = R(\\alpha + \\beta)$ vale para '
                                                      'cualquier par de ángulos, no por casualidad de los '
                                                      'números: la suma de ángulos conmuta siempre.'},
                                      {'id': 'd',
                                       'texto': 'Porque las dos tienen $\\det = 1$, y el producto de '
                                                'determinantes es conmutativo.',
                                       'correcta': False,
                                       'explicacion': 'El determinante del producto conmuta siempre ($\\det '
                                                      'AB = \\det A \\det B$), aunque $AB \\neq BA$; que los '
                                                      'determinantes conmuten no dice nada sobre las '
                                                      'matrices.'}],
                         'rubrica': 'Rotaciones/medio: hay una equivalencia entre operaciones en C y en R^2 '
                                    '(descripta por lo que le hacen a los puntos)'},
                        {'id': '01b_a2',
                         'nivel': 'avanzado',
                         'enunciado': 'Buscamos la rotación que lleva $(1, 0)$ a $(0, -1)$. ¿Qué ángulo es, '
                                      'y hay alguna otra matriz ortogonal que haga lo mismo con ese punto?',
                         'opciones': [{'id': 'a',
                                       'texto': '$\\theta = -90°$; sí: el espejo $\\begin{pmatrix} 0 & -1 '
                                                '\\\\ -1 & 0 \\end{pmatrix}$ también manda $(1, 0)$ a $(0, '
                                                '-1)$, con $\\det = -1$.',
                                       'correcta': True,
                                       'explicacion': 'La primera columna de $R(\\theta)$ es $(\\cos\\theta, '
                                                      '\\sin\\theta) = (0, -1)$, de donde $\\theta = -90°$; '
                                                      'mandar un solo punto no fija la transformación, '
                                                      'conservar distancias y orientación sí.'},
                                      {'id': 'b',
                                       'texto': '$\\theta = 90°$; no: la imagen de $e_1$ determina la '
                                                'rotación y no queda otra.',
                                       'correcta': False,
                                       'explicacion': '$R(90°)$ manda $(1, 0)$ a $(0, 1)$, hacia arriba; '
                                                      'para ir hacia abajo el giro es horario, $-90°$. Y sí '
                                                      'hay otra ortogonal, aunque no sea rotación.'},
                                      {'id': 'c',
                                       'texto': '$\\theta = -90°$; no: la imagen de $e_1$ fija las dos '
                                                'columnas y no queda otra matriz posible.',
                                       'correcta': False,
                                       'explicacion': 'La imagen de $e_1$ fija la primera columna; la '
                                                      'segunda puede ser $(1, 0)$ (giro, $\\det = +1$) o '
                                                      '$(-1, 0)$ (espejo respecto de $y = -x$, $\\det = '
                                                      '-1$).'},
                                      {'id': 'd',
                                       'texto': '$\\theta = 180°$; sí: $\\mathrm{diag}(1, -1)$ también lo '
                                                'hace, porque cambia el signo de la segunda coordenada.',
                                       'correcta': False,
                                       'explicacion': '$R(180°)$ manda $(1, 0)$ a $(-1, 0)$ y '
                                                      '$\\mathrm{diag}(1, -1)$ lo deja en $(1, 0)$: ninguna '
                                                      'de las dos lo lleva a $(0, -1)$.'}],
                         'rubrica': 'Rotaciones/elemental: las rotaciones son matrices ortogonales con '
                                    'determinante mayor a 0 (el espejo cumple A^T A = Id pero det = -1)'}],
 '01c_rotaciones_3d': [{'id': '01c_e1',
                        'nivel': 'elemental',
                        'enunciado': 'Giramos el punto $(1, 2, 3)$ un cuarto de vuelta alrededor del eje '
                                     '$z$, con $R_z(90°) = \\begin{pmatrix} 0 & -1 & 0 \\\\ 1 & 0 & 0 \\\\ 0 '
                                     '& 0 & 1 \\end{pmatrix}$. ¿A dónde va?',
                        'opciones': [{'id': 'a',
                                      'texto': 'A $(-2, 1, 3)$: la $z$ queda y el plano $(x, y)$ gira como '
                                               'en 2D.',
                                      'correcta': True,
                                      'explicacion': '$R_z$ es $R(90°)$ empotrada con un $1$ para la '
                                                     'coordenada que no se mueve: $(1, 2) \\mapsto (-2, 1)$ '
                                                     'y la tercera coordenada se copia; el largo '
                                                     '$\\sqrt{14}$ no cambia.'},
                                     {'id': 'b',
                                      'texto': 'A $(2, -1, 3)$: la $z$ queda y el plano $(x, y)$ gira un '
                                               'cuarto de vuelta.',
                                      'correcta': False,
                                      'explicacion': '$(2, -1)$ es el giro horario $R(-90°)(1, 2)$; con la '
                                                     'mano derecha, antihorario mirando desde la punta de '
                                                     '$z$, el eje $x$ va hacia $y$ y $(x, y) \\mapsto (-y, '
                                                     'x)$.'},
                                     {'id': 'c',
                                      'texto': 'A $(2, 1, 3)$: se intercambian las dos coordenadas que '
                                               'giran.',
                                      'correcta': False,
                                      'explicacion': 'Intercambiar sin signo es el espejo respecto del plano '
                                                     "$y = x$, con $\\det = -1$; la matriz dice $x' = -y$, "
                                                     "$y' = x$."},
                                     {'id': 'd',
                                      'texto': 'A $(-1, -2, 3)$: las coordenadas del plano que gira cambian '
                                               'de signo.',
                                      'correcta': False,
                                      'explicacion': 'Cambiar los dos signos es media vuelta, $R_z(180°) = '
                                                     '\\mathrm{diag}(-1, -1, 1)$, que es $R_z(90°)$ aplicada '
                                                     'dos veces, no una.'}],
                        'rubrica': 'Rotaciones/elemental: las rotaciones son matrices ortogonales (A^T A = '
                                   'Id) con determinante mayor a 0'},
                       {'id': '01c_e2',
                        'nivel': 'elemental',
                        'enunciado': 'Inclinamos el instrumento un ángulo $\\beta \\neq 0$ alrededor del eje '
                                     '$y$, es decir aplicamos $R_y(\\beta)$ a todo el espacio. ¿Qué puntos '
                                     'quedan quietos?',
                        'opciones': [{'id': 'a',
                                      'texto': 'Sólo los puntos del eje $y$: la recta de giro queda fija y '
                                               'todo lo demás gira en planos perpendiculares a ella.',
                                      'correcta': True,
                                      'explicacion': 'La segunda columna de $R_y$ es $e_y$, así que '
                                                     '$R_y(\\lambda e_y) = \\lambda e_y$; cualquier punto '
                                                     'fuera del eje tiene componente en el plano $(z, x)$, '
                                                     'que gira.'},
                                     {'id': 'b',
                                      'texto': 'Todo el plano $xz$, porque es el plano asociado al giro.',
                                      'correcta': False,
                                      'explicacion': 'El plano $(z, x)$ es justamente el que gira: es el '
                                                     'perpendicular al eje, no el eje. Confunde la recta que '
                                                     'queda fija con el plano donde ocurre el movimiento.'},
                                     {'id': 'c',
                                      'texto': 'Ninguno salvo el origen: un giro mueve todo lo que no está '
                                               'en el centro.',
                                      'correcta': False,
                                      'explicacion': 'Eso vale en el plano, donde el centro es un punto; en '
                                                     '3D el centro es una recta entera, y por eso en el '
                                                     'espacio hay que decir alrededor de qué eje.'},
                                     {'id': 'd',
                                      'texto': 'Los ejes $x$ y $z$, porque son los que aparecen en la matriz '
                                               'con senos y cosenos.',
                                      'correcta': False,
                                      'explicacion': 'Que aparezcan con senos y cosenos significa '
                                                     'exactamente que se mueven: $e_x \\mapsto (\\cos\\beta, '
                                                     '0, -\\sin\\beta)$, que no es $e_x$ si $\\beta \\neq '
                                                     '0$.'}],
                        'rubrica': 'Productos/elemental: el eje de una rotacion 3D es el autovector de '
                                   'autovalor 1'},
                       {'id': '01c_m1',
                        'nivel': 'medio',
                        'enunciado': 'Giramos el extremo del eje $x$ del instrumento, $e_x = (1, 0, 0)$, '
                                     'primero $90°$ alrededor de $y$ y después $90°$ alrededor de $z$ (mano '
                                     'derecha). ¿Dónde termina?',
                        'opciones': [{'id': 'a',
                                      'texto': 'En $(0, 0, -1)$: el giro alrededor de $y$ lo baja a $-e_z$, '
                                               'y el giro alrededor de $z$ deja quieto lo que está sobre el '
                                               'eje $z$.',
                                      'correcta': True,
                                      'explicacion': 'Con la mano derecha alrededor de $y$ el ciclo es $e_z '
                                                     '\\to e_x \\to -e_z$, y $-e_z$ está sobre el eje del '
                                                     'segundo giro; es la primera columna de $R_z R_y$.'},
                                     {'id': 'b',
                                      'texto': 'En $(0, 1, 0)$: el giro alrededor de $z$ lo manda a $e_y$, y '
                                               'el giro alrededor de $y$ deja quieto $e_y$.',
                                      'correcta': False,
                                      'explicacion': 'Ese es el otro orden, primero $z$ y después $y$: la '
                                                     'primera columna de $R_y R_z$. En 3D invertir el orden '
                                                     'cambia el destino.'},
                                     {'id': 'c',
                                      'texto': 'En $(1, 0, 0)$: dos cuartos de vuelta alrededor de ejes '
                                               'perpendiculares a $x$ lo devuelven a su lugar.',
                                      'correcta': False,
                                      'explicacion': '$e_x$ no está sobre el eje $y$ ni sobre el eje $z$, '
                                                     'así que ninguno de los dos giros lo deja quieto, y no '
                                                     'hay razón para que el segundo deshaga al primero.'},
                                     {'id': 'd',
                                      'texto': 'En $(-1, 0, 0)$: dos giros de $90°$ suman $180°$ y media '
                                               'vuelta lo da vuelta.',
                                      'correcta': False,
                                      'explicacion': 'Los ángulos se suman sólo cuando el eje es el mismo; '
                                                     'alrededor de ejes distintos la composición es otro '
                                                     'giro, de $120°$ alrededor de $(-1, 1, 1)$, y $e_x$ no '
                                                     'termina en su opuesto.'}],
                        'rubrica': 'Productos/elemental: la composicion es el producto de matrices; las '
                                   'columnas dicen adonde van los ejes'},
                       {'id': '01c_m2',
                        'nivel': 'medio',
                        'enunciado': 'Para nivelar, primero inclinamos la estación alrededor del eje fijo '
                                     '$y$ de la obra ($R_y$, con $90°$ para fijar ideas) y después la '
                                     'giramos alrededor del eje fijo $z$ ($R_z$, también $90°$). ¿Qué matriz '
                                     'describe la operación completa?',
                        'opciones': [{'id': 'a',
                                      'texto': '$R_z R_y$: la matriz de la derecha es la que actúa primero '
                                               'sobre el punto.',
                                      'correcta': True,
                                      'explicacion': 'Aplicar $R_y$ y después $R_z$ a un punto $p$ es '
                                                     '$R_z(R_y p) = (R_z R_y)p$; la escritura va al revés '
                                                     'del orden de aplicación, como en el producto $R_z R_y$ '
                                                     'del cuaderno.'},
                                     {'id': 'b',
                                      'texto': '$R_y R_z$: se escriben en el orden en que se hacen, de '
                                               'izquierda a derecha.',
                                      'correcta': False,
                                      'explicacion': '$R_y R_z\\,p$ aplica primero $R_z$; con giros de $90°$ '
                                                     'manda $e_x$ a $(0, 1, 0)$ en vez de $(0, 0, -1)$, otro '
                                                     'destino.'},
                                     {'id': 'c',
                                      'texto': 'Cualquiera de las dos, $R_z R_y = R_y R_z$: los giros '
                                               'conmutan como en el plano.',
                                      'correcta': False,
                                      'explicacion': 'En el plano conmutan porque todos giran alrededor del '
                                                     'mismo eje; en 3D, alrededor de ejes distintos, $R_z '
                                                     'R_y \\neq R_y R_z$ y el cubo termina en dos lugares '
                                                     'distintos.'},
                                     {'id': 'd',
                                      'texto': '$R_z^T R_y$: al componer hay que transponer la segunda para '
                                               'que actúe sobre los ejes ya girados.',
                                      'correcta': False,
                                      'explicacion': 'Transponer invierte un giro, no lo compone; acá los '
                                                     'dos son activos sobre el instrumento y la segunda '
                                                     'matriz va tal cual, a la izquierda.'}],
                        'rubrica': 'Afinidades/medio: componer es multiplicar matrices y el orden importa'},
                       {'id': '01c_a1',
                        'nivel': 'avanzado',
                        'enunciado': 'Encadenamos $R = R_z(90°)\\,R_y(90°)$. Sabemos que $R$ sigue siendo '
                                     'ortogonal con $\\det R = 1$. ¿Qué podemos decir de su eje?',
                        'opciones': [{'id': 'a',
                                      'texto': 'Tiene que existir y es la recta por $(-1, 1, 1)$: $R$ la '
                                               'deja fija y gira $120°$ alrededor de ella.',
                                      'correcta': True,
                                      'explicacion': 'Toda ortogonal con $\\det = 1$ en $\\mathbb R^3$ deja '
                                                     'fija una recta (Euler); se verifica $R(-1, 1, 1) = '
                                                     '(-1, 1, 1)$, y $\\operatorname{tr} R = 0 = 1 + '
                                                     '2\\cos\\theta$ da $120°$, con $R^3 = I$.'},
                                     {'id': 'b',
                                      'texto': 'Es el eje $z$, porque el último giro fue alrededor de $z$ y '
                                               'es el que manda.',
                                      'correcta': False,
                                      'explicacion': '$R e_z = R_z(R_y e_z) = R_z e_x = e_y \\neq e_z$: el '
                                                     'eje $z$ se mueve. El eje de la composición no es el de '
                                                     'ninguno de los dos giros.'},
                                     {'id': 'c',
                                      'texto': 'Es el eje $y$, porque el primer giro fue alrededor de $y$ y '
                                               'lo dejó quieto.',
                                      'correcta': False,
                                      'explicacion': '$R_y$ deja quieto $e_y$, pero después $R_z$ lo manda a '
                                                     '$-e_x$; lo que queda quieto tras el primer giro no '
                                                     'sobrevive al segundo.'},
                                     {'id': 'd',
                                      'texto': 'No tiene eje: dos giros alrededor de ejes distintos no son '
                                               'un giro, sino otra clase de movimiento.',
                                      'correcta': False,
                                      'explicacion': 'El producto de ortogonales con $\\det = 1$ es '
                                                     'ortogonal con $\\det = 1$, y toda matriz así es un '
                                                     'giro alrededor de alguna recta: la composición de '
                                                     'rotaciones es una rotación.'}],
                        'rubrica': 'Rotaciones/medio: combinacion de rotaciones son rotaciones (el eje fijo, '
                                   'que en la clase 6 sera autovector de autovalor 1)'},
                       {'id': '01c_a2',
                        'nivel': 'avanzado',
                        'enunciado': 'Con giros de $90°$ los dos órdenes, $R_z R_y R_x$ y $R_x R_y R_z$, '
                                     'dejan el cubo en lugares muy distintos. Bajamos los tres ángulos a '
                                     '$1°$ y después a $0.1°$. ¿Qué le pasa a la diferencia entre los dos '
                                     'órdenes?',
                        'opciones': [{'id': 'a',
                                      'texto': 'Cae unas $100$ veces al dividir los ángulos por $10$: es de '
                                               'segundo orden, y con correcciones chicas los dos órdenes '
                                               'casi coinciden.',
                                      'correcta': True,
                                      'explicacion': 'Cada giro chico es $I + \\varepsilon K$ y los términos '
                                                     'de primer orden se suman en cualquier orden; la '
                                                     'diferencia aparece recién en $\\varepsilon^2$, por eso '
                                                     'la no conmutatividad depende de la magnitud.'},
                                     {'id': 'b',
                                      'texto': 'No cambia: la no conmutatividad es una propiedad de los '
                                               'ejes, no del tamaño del ángulo.',
                                      'correcta': False,
                                      'explicacion': 'Los ejes deciden si conmutan exactamente o no, pero '
                                                     'cuánto difieren depende del ángulo: con $\\varepsilon '
                                                     '\\to 0$ ambos órdenes tienden a la misma matriz $I + '
                                                     '\\varepsilon(K_x + K_y + K_z)$.'},
                                     {'id': 'c',
                                      'texto': 'Es exactamente cero: los giros de ángulos chicos conmutan.',
                                      'correcta': False,
                                      'explicacion': 'Conmutan sólo en el límite; para cualquier '
                                                     '$\\varepsilon \\neq 0$ hay una diferencia del orden de '
                                                     '$\\varepsilon^2$, chica pero no nula, y el cuaderno la '
                                                     'mide.'},
                                     {'id': 'd',
                                      'texto': 'Cae unas $10$ veces al dividir los ángulos por $10$: es '
                                               'proporcional al ángulo, como cualquier giro.',
                                      'correcta': False,
                                      'explicacion': 'Si fuera de primer orden, la parte lineal de los dos '
                                                     'productos sería distinta; pero $I + \\varepsilon(K_x + '
                                                     'K_y + K_z)$ es la misma en los dos órdenes y lo que '
                                                     'difiere es el término cuadrático.'}],
                        'rubrica': 'Rotaciones/elemental: la falta de conmutatividad depende de la magnitud; '
                                   "Rotaciones/medio: 'identidad + algo chiquito' da la pista diferencial"}],
 '02_producto_interno': [{'id': '02_e1',
                          'nivel': 'elemental',
                          'enunciado': 'Desde el mojón $B$ salen los lados $BA = (4, 3)$ y $BC = (4, -3)$, '
                                       'los dos de $5$ m. ¿Cuánto vale $\\langle BC, BA\\rangle$?',
                          'opciones': [{'id': 'a',
                                        'texto': '$7$: coordenada por coordenada y sumamos, $4 \\cdot 4 + '
                                                 '(-3) \\cdot 3$.',
                                        'correcta': True,
                                        'explicacion': 'La cuenta es $x_1 x_2 + y_1 y_2 = 16 - 9 = 7$, y '
                                                       'vale $\\lvert BC\\rvert\\,\\lvert '
                                                       'BA\\rvert\\cos\\hat B = 25 \\cos\\hat B$: el ángulo '
                                                       'en $B$ es agudo.'},
                                       {'id': 'b',
                                        'texto': '$25$: el producto de los dos largos, $5 \\cdot 5$.',
                                        'correcta': False,
                                        'explicacion': '$\\lvert v\\rvert\\,\\lvert u\\rvert = 25$ es el '
                                                       'producto interno sólo si apuntan igual '
                                                       '($\\cos\\theta = 1$); acá falta el coseno, que vale '
                                                       '$7/25$.'},
                                       {'id': 'c',
                                        'texto': '$1$: sumamos las coordenadas de $BC$, $4 + (-3)$.',
                                        'correcta': False,
                                        'explicacion': 'Sumar las coordenadas de un vector no mide nada: '
                                                       'cambia si giramos los ejes aunque el mojón no se '
                                                       'mueva. Hay que multiplicar coordenada con coordenada '
                                                       'del otro vector y recién sumar.'},
                                       {'id': 'd',
                                        'texto': '$0.28$: el cociente $7/25$ entre la suma de productos y '
                                                 'los largos.',
                                        'correcta': False,
                                        'explicacion': '$0.28$ es $\\cos\\hat B$, el producto interno ya '
                                                       'dividido por los dos largos; el producto interno es '
                                                       'el $7$ antes de dividir.'}],
                          'rubrica': 'Productos/elemental: el producto interno decide incidencia y '
                                     'ortogonalidad'},
                         {'id': '02_e2',
                          'nivel': 'elemental',
                          'enunciado': 'Giramos los dos lados $BA$ y $BC$ juntos $37°$ alrededor de $B$, sin '
                                       'cambiarles el largo. ¿Qué le pasa a $\\langle BC, BA\\rangle$?',
                          'opciones': [{'id': 'a',
                                        'texto': 'No cambia: la rotación conserva largos y ángulos, y el '
                                                 'producto interno sólo depende de ellos.',
                                        'correcta': True,
                                        'explicacion': '$\\langle Rv, Ru\\rangle = v^T R^T R\\,u = v^T u$ '
                                                       'porque $R^T R = I$; cambian todas las coordenadas y '
                                                       'la cuenta da el mismo $7$.'},
                                       {'id': 'b',
                                        'texto': 'Se multiplica por $\\cos 37°$, porque cada vector giró ese '
                                                 'ángulo.',
                                        'correcta': False,
                                        'explicacion': 'Eso mide la sombra de cada vector sobre su posición '
                                                       'anterior, no el producto entre los dos; el ángulo '
                                                       'entre ellos sigue siendo $\\hat B$ porque giraron '
                                                       'juntos.'},
                                       {'id': 'c',
                                        'texto': 'Cambia, salvo que los dos lados fueran perpendiculares, en '
                                                 'cuyo caso sigue valiendo $0$.',
                                        'correcta': False,
                                        'explicacion': 'La conservación no es un privilegio del $0$: '
                                                       '$\\langle Rv, Ru\\rangle = \\langle v, u\\rangle$ '
                                                       'para cualquier par, perpendicular o no.'},
                                       {'id': 'd',
                                        'texto': 'Cambia de signo si el giro es horario y queda igual si es '
                                                 'antihorario.',
                                        'correcta': False,
                                        'explicacion': '$R(-\\theta)$ también es una rotación con $R^T R = '
                                                       'I$; el sentido del giro no toca la cuenta. Un cambio '
                                                       'de signo exigiría cambiar el ángulo entre los '
                                                       'vectores.'}],
                          'rubrica': 'Rotaciones/elemental: el producto interno puede servir como base para '
                                     'definir tipos de transformaciones'},
                         {'id': '02_m1',
                          'nivel': 'medio',
                          'enunciado': 'De los $5$ m del lado $BC = (4, -3)$, ¿cuánto cae sobre la dirección '
                                       'de la línea de base $BA = (4, 3)$?',
                          'opciones': [{'id': 'a',
                                        'texto': '$1.4$ m: el producto interno $7$ dividido por el largo de '
                                                 '$BA$.',
                                        'correcta': True,
                                        'explicacion': 'La sombra (proyección escalar) es $\\lvert '
                                                       'BC\\rvert\\cos\\hat B = \\langle BC, BA\\rangle / '
                                                       '\\lvert BA\\rvert = 7/5$; Pitágoras lo cierra, '
                                                       '$1.4^2 + 4.8^2 = 25$.'},
                                       {'id': 'b',
                                        'texto': '$5$ m: el lado entero, porque su largo no cambia al '
                                                 'proyectarlo.',
                                        'correcta': False,
                                        'explicacion': 'El largo no cambia al girar, pero proyectar lo '
                                                       'acorta: sobre $BA$ cae sólo la distancia por el '
                                                       'coseno, y $\\cos\\hat B = 0.28$.'},
                                       {'id': 'c',
                                        'texto': '$4.8$ m: el largo por el seno del ángulo en $B$.',
                                        'correcta': False,
                                        'explicacion': '$5\\sin\\hat B = 4.8$ es la parte de $BC$ '
                                                       'perpendicular a $BA$, lo que queda afuera de la '
                                                       'sombra; la sombra va con el coseno.'},
                                       {'id': 'd',
                                        'texto': '$7$ m: el producto interno ya es la proyección.',
                                        'correcta': False,
                                        'explicacion': '$7$ es la sombra multiplicada por el largo de $BA$; '
                                                       'para quedarse con la sombra sola hay que dividir por '
                                                       '$\\lvert BA\\rvert = 5$.'}],
                          'rubrica': 'Rotaciones/medio: hay transformaciones que se definen completamente '
                                     'por que propiedades mantienen (lo que la rotacion conserva: largo, '
                                     'angulo, sombra)'},
                         {'id': '02_m2',
                          'nivel': 'medio',
                          'enunciado': 'Queremos el vector sombra de $v = BC = (4, -3)$ sobre $u = BA = (4, '
                                       '3)$, la proyección vectorial. ¿Cuál es?',
                          'opciones': [{'id': 'a',
                                        'texto': '$\\tfrac{7}{25}(4, 3) = (1.12, 0.84)$: un múltiplo de $u$ '
                                                 'con coeficiente $\\langle v, u\\rangle / \\langle u, '
                                                 'u\\rangle$.',
                                        'correcta': True,
                                        'explicacion': 'El coeficiente es la sombra $7/5$ dividida otra vez '
                                                       'por $\\lvert u\\rvert$ para que multiplique al '
                                                       'unitario: $\\tfrac{7}{5}\\cdot\\tfrac{u}{5} = '
                                                       '\\tfrac{7}{25}u$, y $v - p = (2.88, -3.84)$ es '
                                                       'perpendicular a $u$.'},
                                       {'id': 'b',
                                        'texto': '$\\tfrac{7}{5}(4, 3) = (5.6, 4.2)$: la sombra $1.4$ por el '
                                                 'vector $u$.',
                                        'correcta': False,
                                        'explicacion': 'Multiplica la sombra por $u$ entero, que mide $5$, y '
                                                       'queda cinco veces más largo que la sombra; el '
                                                       'múltiplo correcto es la sombra por el unitario '
                                                       '$u/5$.'},
                                       {'id': 'c',
                                        'texto': '$1.4$: la proyección es un número, cuánto de $v$ cae sobre '
                                                 '$u$.',
                                        'correcta': False,
                                        'explicacion': '$1.4$ es la proyección escalar, un largo; la '
                                                       'proyección vectorial es la flecha de ese largo '
                                                       'apoyada sobre $u$, un elemento de $\\mathbb R^2$.'},
                                       {'id': 'd',
                                        'texto': '$\\tfrac{7}{25}(4, -3) = (1.12, -0.84)$: el coeficiente '
                                                 'por el vector que proyectamos.',
                                        'correcta': False,
                                        'explicacion': 'Eso es un múltiplo de $v$, la sombra de $u$ sobre '
                                                       '$v$; la proyección de $v$ sobre $u$ tiene que caer '
                                                       'sobre la recta de $u$.'}],
                          'rubrica': 'SVD/avanzado: hecho geometrico de proyectar sobre un subespacio (la '
                                     'sombra como vector, no como numero)'},
                         {'id': '02_a1',
                          'nivel': 'avanzado',
                          'enunciado': 'Relevamos $A = (7, 6)$, $B = (10, 10)$ y $C = (14, 7)$. Sin '
                                       'transportador, ¿cuánto vale el ángulo en $B$?',
                          'opciones': [{'id': 'a',
                                        'texto': '$90°$: $BA = (-3, -4)$, $BC = (4, -3)$ y $\\langle BA, '
                                                 'BC\\rangle = -12 + 12 = 0$.',
                                        'correcta': True,
                                        'explicacion': 'Primero se restan coordenadas desde $B$ y después se '
                                                       'hace la cuenta; sombra nula es ángulo recto, y la '
                                                       'ley del coseno lo confirma: $\\lvert AC\\rvert^2 = '
                                                       '25 + 25 - 0 = 50$.'},
                                       {'id': 'b',
                                        'texto': '$0°$: los dos lados miden $5$, así que apuntan en la misma '
                                                 'dirección.',
                                        'correcta': False,
                                        'explicacion': 'Tener el mismo largo no dice nada del ángulo; $(-3, '
                                                       '-4)$ y $(4, -3)$ miden $5$ los dos y son '
                                                       'perpendiculares.'},
                                       {'id': 'c',
                                        'texto': 'Unos $164°$: $\\langle BA, BC\\rangle = -12 - 12 = -24$ y '
                                                 '$\\cos\\hat B = -24/25$.',
                                        'correcta': False,
                                        'explicacion': 'El segundo producto es $(-4)(-3) = +12$, no $-12$; '
                                                       'con el signo bien la suma da $0$. Un ángulo casi '
                                                       'llano exigiría que $BA$ y $BC$ apuntaran en sentidos '
                                                       'casi opuestos, y acá son perpendiculares.'},
                                       {'id': 'd',
                                        'texto': 'Unos $14°$: usamos $A$ y $C$ tal cual, $\\langle A, '
                                                 'C\\rangle = 98 + 42 = 140$, y los largos desde el origen.',
                                        'correcta': False,
                                        'explicacion': 'Los vectores $A$ y $C$ medidos desde el origen '
                                                       'forman un ángulo en el origen, no en $B$; el ángulo '
                                                       'en un vértice se calcula con los lados que salen de '
                                                       'ese vértice, $A - B$ y $C - B$.'}],
                          'rubrica': 'Productos/elemental: el producto interno decide incidencia y '
                                     'ortogonalidad (hecho geometrico: sombra nula es angulo recto)'},
                         {'id': '02_a2',
                          'nivel': 'avanzado',
                          'enunciado': 'La fórmula $\\langle v, u\\rangle = x_1 x_2 + y_1 y_2$ mide largos y '
                                       'ángulos de verdad cuando las coordenadas están en la base canónica. '
                                       '¿Qué tiene de especial esa base?',
                          'opciones': [{'id': 'a',
                                        'texto': 'Que sus ejes son perpendiculares y de largo $1$; en otra '
                                                 'grilla la misma suma de productos no mide y hace falta la '
                                                 'métrica $G$.',
                                        'correcta': True,
                                        'explicacion': 'La suma de productos es $v^T G u$ con $G = I$, y $G '
                                                       '= I$ es justamente la tabla de productos internos de '
                                                       'una base ortonormal; en la grilla del papel estirado '
                                                       "$G' = \\mathrm{diag}(\\tfrac14, 1)$ y la fórmula "
                                                       'ingenua se equivoca.'},
                                       {'id': 'b',
                                        'texto': 'Que es la única base de $\\mathbb R^2$; cualquier otro par '
                                                 'de vectores es sólo un cambio de nombre de la misma.',
                                        'correcta': False,
                                        'explicacion': 'Hay infinitas bases y ninguna es privilegiada a '
                                                       'priori: lo único especial de la canónica es que '
                                                       'sobre ella está definida la distancia por la suma de '
                                                       'productos.'},
                                       {'id': 'c',
                                        'texto': 'Nada: en cualquier base la suma de productos de '
                                                 'coordenadas mide igual, la grilla no cambia la geometría.',
                                        'correcta': False,
                                        'explicacion': 'La geometría no cambia, pero los números sí: con el '
                                                       'Este estirado por 2 el ángulo recto del terreno se '
                                                       'calcula como $53.1°$ si se usa $x_1 x_2 + y_1 y_2$ '
                                                       'en la grilla del papel.'},
                                       {'id': 'd',
                                        'texto': 'Que tiene determinante $1$, y eso garantiza que los largos '
                                                 'salen bien.',
                                        'correcta': False,
                                        'explicacion': 'El corte $\\begin{pmatrix} 1 & 0.5 \\\\ 0 & 1 '
                                                       '\\end{pmatrix}$ también da una base de determinante '
                                                       '$1$ y sus ejes no son perpendiculares: con sus '
                                                       'coordenadas la fórmula mide mal.'}],
                          'rubrica': 'SVD/avanzado: no hay base privilegiada a priori; lo unico especial de '
                                     'la canonica es que en ella el producto interno se calcula como suma de '
                                     'productos'}],
 '03_reflexiones_similaridades': [{'id': '03_e1',
                                   'nivel': 'elemental',
                                   'enunciado': 'Reflejamos la parcela respecto de una recta que pasa por el '
                                                'origen. ¿Qué le pasa a las distancias, a los ángulos y a la '
                                                'orientación?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'Se conservan distancias y orientación, pero los '
                                                          'ángulos cambian.',
                                                 'correcta': False,
                                                 'explicacion': 'Un espejo conserva los ángulos: $H^T H = '
                                                                'I$, es una matriz ortogonal. Lo que cambia '
                                                                'es el sentido de giro, no la forma.'},
                                                {'id': 'b',
                                                 'texto': 'Se conserva todo, también la orientación: $\\det '
                                                          'H = +1$, como en un giro.',
                                                 'correcta': False,
                                                 'explicacion': 'Confunde la reflexión con la rotación. Las '
                                                                'dos son ortogonales, pero el espejo tiene '
                                                                '$\\det = -1$: la parcela recorrida '
                                                                'antihorario sale recorrida horario.'},
                                                {'id': 'c',
                                                 'texto': 'Se conservan distancias y ángulos, pero la '
                                                          'orientación se invierte: $\\det H = -1$.',
                                                 'correcta': True,
                                                 'explicacion': 'El espejo es ortogonal (conserva todo lo '
                                                                'métrico) y da vuelta la hoja: el área con '
                                                                'signo cambia de signo. Por eso dos espejos '
                                                                'seguidos devuelven la orientación y son un '
                                                                'giro.'},
                                                {'id': 'd',
                                                 'texto': 'Las distancias se multiplican por $-1$ y los '
                                                          'ángulos no cambian.',
                                                 'correcta': False,
                                                 'explicacion': 'Una distancia nunca es negativa. Lo que se '
                                                                'escala por $-1$ es la coordenada '
                                                                'perpendicular al espejo, no la distancia '
                                                                'entre puntos, que queda igual.'}],
                                   'rubrica': 'Rotaciones · elemental: las rotaciones son matrices '
                                              'ortogonales con determinante mayor a 0 (la reflexión es la '
                                              'ortogonal con det −1)'},
                                  {'id': '03_e2',
                                   'nivel': 'elemental',
                                   'enunciado': 'Aplicamos al vértice $(4, 1)$ el espejo de la diagonal $y = '
                                                'x$, $H(45°) = \\begin{pmatrix} 0 & 1 \\\\ 1 & 0 '
                                                '\\end{pmatrix}$. ¿A dónde va?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'A $(4, -1)$.',
                                                 'correcta': False,
                                                 'explicacion': 'Ese es el espejo del eje $x$, $H(0°) = '
                                                                '\\mathrm{diag}(1, -1)$. El espejo de la '
                                                                'diagonal no cambia signos: intercambia las '
                                                                'coordenadas.'},
                                                {'id': 'b',
                                                 'texto': 'A $(1, 4)$.',
                                                 'correcta': True,
                                                 'explicacion': '$4\\,(0, 1) + 1\\,(1, 0) = (1, 4)$: las '
                                                                'columnas son las imágenes de $e_1$ y $e_2$, '
                                                                'que se cruzan. El punto pasa al otro lado '
                                                                'de la diagonal a la misma distancia, largo '
                                                                '$\\sqrt{17}$ en los dos.'},
                                                {'id': 'c',
                                                 'texto': 'A $(-1, 4)$.',
                                                 'correcta': False,
                                                 'explicacion': 'Ese es el giro de $90°$, $R(90°)(4, 1) = '
                                                                '(-1, 4)$. Tiene $\\det = +1$; el espejo '
                                                                'tiene $\\det = 0 - 1 = -1$ y no gira: '
                                                                'refleja.'},
                                                {'id': 'd',
                                                 'texto': 'Se queda en $(4, 1)$: la diagonal es una recta '
                                                          'fija.',
                                                 'correcta': False,
                                                 'explicacion': 'Lo que queda fijo punto a punto es la recta '
                                                                'espejo $y = x$; $(4, 1)$ no está sobre '
                                                                'ella, así que cruza al otro lado.'}],
                                   'rubrica': 'Afinidades · elemental: aplicar una afinidad en planilla, '
                                              'matriz por vector columna; las columnas son las imágenes de '
                                              'los ejes'},
                                  {'id': '03_m1',
                                   'nivel': 'medio',
                                   'enunciado': 'Reflejamos primero respecto del eje $x$ y después respecto '
                                                'de la recta de $30°$. ¿Qué transformación resulta de los '
                                                'dos espejos seguidos?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'Una rotación de $30°$, el ángulo entre los dos '
                                                          'espejos.',
                                                 'correcta': False,
                                                 'explicacion': 'El ángulo de giro es el doble del ángulo '
                                                                'entre los espejos: $e_1$ queda sobre el '
                                                                'primer espejo y el segundo lo refleja al '
                                                                'otro lado, a $2\\cdot 30° = 60°$. Falta el '
                                                                'factor $2$.'},
                                                {'id': 'b',
                                                 'texto': 'Otra reflexión, respecto de la bisectriz de '
                                                          '$15°$.',
                                                 'correcta': False,
                                                 'explicacion': 'Dos espejos no son un espejo: $\\det = '
                                                                '(-1)(-1) = +1$, la orientación vuelve. Lo '
                                                                'que queda es un giro, no un espejo '
                                                                'intermedio.'},
                                                {'id': 'c',
                                                 'texto': 'La identidad, porque cada espejo es su propia '
                                                          'inversa.',
                                                 'correcta': False,
                                                 'explicacion': '$H\\,H = I$ vale para el mismo espejo dos '
                                                                'veces. Con rectas distintas el segundo no '
                                                                'deshace al primero: deja un giro del doble '
                                                                'del ángulo entre ellas.'},
                                                {'id': 'd',
                                                 'texto': 'Una rotación de $60°$ alrededor del origen.',
                                                 'correcta': True,
                                                 'explicacion': '$H(30°)\\,H(0°) = R(60°)$: conserva '
                                                                'distancias, deja fijo el punto donde se '
                                                                'cortan los espejos y tiene $\\det = +1$. El '
                                                                'doble del ángulo entre los espejos.'}],
                                   'rubrica': 'Afinidades · medio: dos reflexiones en rectas secantes son '
                                              'una rotación (conservan distancias y dejan un punto fijo)'},
                                  {'id': '03_m2',
                                   'nivel': 'medio',
                                   'enunciado': 'Escribimos la similaridad como número complejo, $z \\mapsto '
                                                '2i\\,z + 1$. ¿Cuánto escala, cuánto gira y cuál es su '
                                                'centro fijo?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'Escala $2$, gira $90°$ y el centro es $(0.2, '
                                                          '0.4)$.',
                                                 'correcta': True,
                                                 'explicacion': '$\\lvert 2i \\rvert = 2$ y $\\arg 2i = '
                                                                '90°$. El centro cumple $c = 2i\\,c + 1$, o '
                                                                'sea $c = 1/(1 - 2i) = (1 + 2i)/5 = 0.2 + '
                                                                '0.4i$; control: $2i(0.2 + 0.4i) + 1 = 0.2 + '
                                                                '0.4i$.'},
                                                {'id': 'b',
                                                 'texto': 'Escala $2$, gira $90°$ y el centro es $(1, 0)$.',
                                                 'correcta': False,
                                                 'explicacion': 'Confunde el corrimiento $b = 1$ con el '
                                                                'centro. El centro es el punto que no se '
                                                                'mueve, $(I - A)\\,c = t$, y $(1, 0)$ va a '
                                                                '$2i + 1 = (1, 2)$: se mueve.'},
                                                {'id': 'c',
                                                 'texto': 'Escala $4$, gira $90°$ y el centro es $(0.2, '
                                                          '0.4)$.',
                                                 'correcta': False,
                                                 'explicacion': '$4 = k^2$ es el factor de área ($\\det A = '
                                                                '4$), no el de longitud. Las distancias se '
                                                                'multiplican por $\\lvert a \\rvert = 2$.'},
                                                {'id': 'd',
                                                 'texto': 'Escala $2$, gira $180°$ y el centro es $(0.2, '
                                                          '0.4)$.',
                                                 'correcta': False,
                                                 'explicacion': 'Multiplicar por $i$ es girar $\\pi/2$, no '
                                                                '$\\pi$; $i^2 = -1$ es lo que da el giro de '
                                                                '$180°$ si se aplica dos veces. El giro de '
                                                                '$2i$ es de $90°$.'}],
                                   'rubrica': 'Rotaciones · medio: hay una equivalencia entre operaciones en '
                                              'C y en R² (multiplicar por i es rotar π/2)'},
                                  {'id': '03_a1',
                                   'nivel': 'avanzado',
                                   'enunciado': 'Para superponer el plano viejo sobre el relevamiento nos '
                                                'alcanzaron dos mojones, pero para corregir un escaneo afín '
                                                'hacen falta tres. ¿Por qué la diferencia?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'Porque la similaridad conserva distancias, y con '
                                                          'un solo mojón ya queda fijada la escala.',
                                                 'correcta': False,
                                                 'explicacion': 'La similaridad no conserva distancias: las '
                                                                'multiplica por $k$. Y un mojón solo no fija '
                                                                'ni la escala ni el giro; da dos ecuaciones '
                                                                'para cuatro incógnitas.'},
                                                {'id': 'b',
                                                 'texto': 'Porque la similaridad tiene cuatro parámetros '
                                                          '($k$, $\\theta$ y el corrimiento) y cada mojón da '
                                                          'dos ecuaciones; la afinidad tiene seis.',
                                                 'correcta': True,
                                                 'explicacion': 'Cuatro incógnitas, dos mojones: $a = (Q_2 - '
                                                                'Q_1)/(P_2 - P_1)$ y $b = Q_1 - aP_1$. La '
                                                                'afinidad $Ax + t$ tiene seis números y '
                                                                'necesita tres pares; el mojón de más sirve '
                                                                'de control.'},
                                                {'id': 'c',
                                                 'texto': 'Porque la afinidad no conserva las rectas y '
                                                          'necesita más puntos para seguirlas.',
                                                 'correcta': False,
                                                 'explicacion': 'La afinidad sí conserva rectas y paralelas. '
                                                                'La diferencia está en los grados de '
                                                                'libertad: dos estiramientos independientes '
                                                                'y una inclinación en lugar de un solo '
                                                                'factor $k$.'},
                                                {'id': 'd',
                                                 'texto': 'No hay diferencia: con dos mojones alcanza para '
                                                          'las dos, el tercero es sólo de control.',
                                                 'correcta': False,
                                                 'explicacion': 'Con dos mojones quedan cuatro ecuaciones '
                                                                'para seis incógnitas: una familia entera de '
                                                                'afinidades pasa por ellos. El tercero no '
                                                                'controla, decide.'}],
                                   'rubrica': 'Afinidades · avanzado: existe una única afinidad que lleva un '
                                              'triángulo dado a otro (tres puntos, seis ecuaciones)'},
                                  {'id': '03_a2',
                                   'nivel': 'avanzado',
                                   'enunciado': 'Repetimos la similaridad $S(x) = 0.85\\,R(30°)\\,x + t$ con '
                                                '$t \\neq 0$: $p$, $S(p)$, $S^2(p)$, … ¿Qué trayectoria '
                                                'dibuja el punto?',
                                   'opciones': [{'id': 'a',
                                                 'texto': 'Una espiral que se enrosca hacia el origen, '
                                                          'porque $k < 1$ achica todo.',
                                                 'correcta': False,
                                                 'explicacion': 'Con $t \\neq 0$ el origen se mueve: $S(0) = '
                                                                't$. La espiral se enrosca hacia el punto '
                                                                'que $S$ deja quieto, que no es el origen.'},
                                                {'id': 'b',
                                                 'texto': 'Un círculo alrededor del centro fijo, porque la '
                                                          'rotación manda sobre la escala.',
                                                 'correcta': False,
                                                 'explicacion': 'El círculo es la trayectoria de la rotación '
                                                                'pura ($k = 1$). Con $k = 0.85$ cada paso '
                                                                'acorta el radio un $15\\%$: la curva se '
                                                                'cierra en espiral.'},
                                                {'id': 'c',
                                                 'texto': 'Una espiral que se enrosca hacia el centro fijo '
                                                          '$c = (I - A)^{-1}\\,t$, no hacia el origen.',
                                                 'correcta': True,
                                                 'explicacion': 'Con el origen puesto en $c$ la similaridad '
                                                                'es sólo girar $30°$ y escalar $0.85$: giro '
                                                                'y homotecia con el mismo centro conmutan, y '
                                                                'la trayectoria es su espiral polar '
                                                                'alrededor de $c$.'},
                                                {'id': 'd',
                                                 'texto': 'Una espiral que se aleja, porque a cada paso se '
                                                          'vuelve a sumar $t$.',
                                                 'correcta': False,
                                                 'explicacion': 'El corrimiento no acumula sin freno: cada '
                                                                'paso también escala por $0.85$ lo que '
                                                                'había. La suma converge y el punto se '
                                                                'acerca a $c$, no se escapa.'}],
                                   'rubrica': 'Afinidades · medio: rotar y trasladar sucesivamente un punto '
                                              'dibuja círculos alrededor del punto fijo de la composición; '
                                              'hallar ese centro'}],
 '04_afines_homogeneas': [{'id': '04_e1',
                           'nivel': 'elemental',
                           'enunciado': 'Escaneamos un plano y la hoja pasó torcida por el rodillo. Si la '
                                        'deformación es una afinidad, ¿en qué figura puede convertirse un '
                                        'cuadrado de la cuadrícula? (Llamamos trapecio al cuadrilátero con '
                                        'dos lados que, prolongados, se cruzan.)',
                           'opciones': [{'id': 'a',
                                         'texto': 'En un paralelogramo cualquiera, nunca en un trapecio.',
                                         'correcta': True,
                                         'explicacion': 'Una afinidad lleva rectas a rectas y paralelas a '
                                                        'paralelas: los lados opuestos difieren en el mismo '
                                                        'vector y $A$ lo manda al mismo vector. Que dos '
                                                        'paralelas se crucen es cosa de una proyectiva.'},
                                        {'id': 'b',
                                         'texto': 'En un trapecio, porque cada eje se estira distinto.',
                                         'correcta': False,
                                         'explicacion': 'Estirar distinto en cada eje deforma los ángulos, '
                                                        'pero no rompe el paralelismo. El trapecio es la '
                                                        'huella de la cámara inclinada, no del rodillo.'},
                                        {'id': 'c',
                                         'texto': 'Sólo en un rectángulo: los ángulos rectos se conservan.',
                                         'correcta': False,
                                         'explicacion': 'Los ángulos no se conservan en una afinidad; sí en '
                                                        'una similaridad. El corte $\\begin{pmatrix} 1 & s '
                                                        '\\\\ 0 & 1 \\end{pmatrix}$ inclina el eje $y$ y '
                                                        'sigue siendo afín.'},
                                        {'id': 'd',
                                         'texto': 'En un cuadrilátero cualquiera, con tal de que los lados '
                                                  'sigan rectos.',
                                         'correcta': False,
                                         'explicacion': 'Eso es lo que permite una proyectiva (cuatro puntos '
                                                        'libres). La afinidad conserva además las paralelas: '
                                                        'con tres vértices el cuarto queda determinado.'}],
                           'rubrica': 'Afinidades · elemental: una afinidad conserva rectas y paralelas; un '
                                      'cuadrado va a un paralelogramo, nunca a un trapecio'},
                          {'id': '04_e2',
                           'nivel': 'elemental',
                           'enunciado': 'Con $H = \\begin{pmatrix} 1.5 & 0.5 & 1 \\\\ 0 & 1.25 & 1 \\\\ 0 & '
                                        '0 & 1 \\end{pmatrix}$ transformamos el punto homogéneo $(4, 2, 1)$. '
                                        '¿Qué terna obtenemos?',
                           'opciones': [{'id': 'a',
                                         'texto': '$(7, 2.5, 1)$.',
                                         'correcta': False,
                                         'explicacion': 'Es $Ap$ sin la tercera columna: el $1$ del punto '
                                                        'enciende la columna $(1, 1, 1)$ y suma la '
                                                        'traslación. Falta $t = (1, 1)$.'},
                                        {'id': 'b',
                                         'texto': '$(6, 4.5, 7)$.',
                                         'correcta': False,
                                         'explicacion': 'Es $H^T$ por el punto: se usaron las columnas como '
                                                        'filas. Cada fila de $H$ por el punto da una '
                                                        'coordenada; con la traspuesta la última fila deja '
                                                        'de ser $(0, 0, 1)$.'},
                                        {'id': 'c',
                                         'texto': '$(8, 3.5, 0)$.',
                                         'correcta': False,
                                         'explicacion': 'La fila $(0, 0, 1)$ garantiza que el $1$ siga '
                                                        'siendo $1$. Con tercera coordenada $0$ la terna '
                                                        'sería un punto impropio, una dirección, no el punto '
                                                        '$(8, 3.5)$.'},
                                        {'id': 'd',
                                         'texto': '$(8, 3.5, 1)$.',
                                         'correcta': True,
                                         'explicacion': '$4\\,(1.5, 0, 0) + 2\\,(0.5, 1.25, 0) + 1\\,(1, 1, '
                                                        '1) = (8, 3.5, 1)$: es $(Ap + t, 1)$ con $Ap = (7, '
                                                        '2.5)$ y $t = (1, 1)$.'}],
                           'rubrica': 'Afinidades · elemental: en coordenadas homogéneas la traslación entra '
                                      'en la 3×3 con última fila (0, 0, 1); el plano afín es w = 1'},
                          {'id': '04_m1',
                           'nivel': 'medio',
                           'enunciado': "Tres mojones $a = (0, 0)$, $b = (1, 0)$ y $c = (0, 1)$ van a $a' = "
                                        "(1, 2)$, $b' = (3, 3)$ y $c' = (2, 4)$. ¿Cuál es la afinidad $x "
                                        '\\mapsto Ax + t$ que los lleva?',
                           'opciones': [{'id': 'a',
                                         'texto': '$A = \\begin{pmatrix} 3 & 2 \\\\ 3 & 4 \\end{pmatrix}$, '
                                                  '$t = (1, 2)$.',
                                         'correcta': False,
                                         'explicacion': 'Puso como columnas las imágenes de $e_1$ y $e_2$ '
                                                        'sin restar la del origen. Las columnas de $A$ son '
                                                        "$Ae_1 = b' - a'$ y $Ae_2 = c' - a'$, porque $A$ "
                                                        'actúa sobre vectores, no sobre puntos.'},
                                        {'id': 'b',
                                         'texto': '$A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$, '
                                                  '$t = (0, 0)$.',
                                         'correcta': False,
                                         'explicacion': '$A$ está bien pero el origen no va al origen: va a '
                                                        '$(1, 2)$. Una $2\\times2$ sola nunca mueve el '
                                                        "origen; hace falta $t = a' = (1, 2)$."},
                                        {'id': 'c',
                                         'texto': '$A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$, '
                                                  '$t = (1, 2)$.',
                                         'correcta': True,
                                         'explicacion': "Como $a$ es el origen, $t = a' = (1, 2)$; después "
                                                        '$Ae_1 = (3, 3) - (1, 2) = (2, 1)$ y $Ae_2 = (2, 4) '
                                                        '- (1, 2) = (1, 2)$. Control: el punto $d = (1, 1) '
                                                        '\\mapsto (3, 3) + (1, 2) = (4, 5)$.'},
                                        {'id': 'd',
                                         'texto': '$A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$, '
                                                  '$t = (-1, -2)$.',
                                         'correcta': False,
                                         'explicacion': "Signo cambiado: $t = a' - Aa$, lo que falta para "
                                                        "que $a$ caiga en $a'$. Con $(-1, -2)$ el origen "
                                                        'iría a $(-1, -2)$, no a $(1, 2)$.'}],
                           'rubrica': 'Afinidades · elemental: aplicar una afinidad en planilla; las '
                                      'columnas son las imágenes de los ejes y la tercera, la del origen'},
                          {'id': '04_m2',
                           'nivel': 'medio',
                           'enunciado': '$R$ gira $90°$ alrededor del origen y $T$ corre $(2, 0)$. ¿A dónde '
                                        'va el origen con $H = TR$ (primero girar, después mover) y con $H = '
                                        'RT$ (primero mover, después girar)?',
                           'opciones': [{'id': 'a',
                                         'texto': 'A $(2, 0)$ con $TR$ y a $(0, 2)$ con $RT$.',
                                         'correcta': True,
                                         'explicacion': 'Con $TR$ el origen no gira (está en el centro) y '
                                                        'después se corre a $(2, 0)$. Con $RT$ primero va a '
                                                        '$(2, 0)$ y después gira $90°$: $(0, 2)$. Mover '
                                                        'antes de girar gira también el corrimiento.'},
                                        {'id': 'b',
                                         'texto': 'A $(2, 0)$ en los dos casos: el orden no importa.',
                                         'correcta': False,
                                         'explicacion': 'Dos traslaciones conmutan, y dos rotaciones con el '
                                                        'mismo centro también; una rotación y una traslación '
                                                        'no. El corrimiento sale girado si se aplica antes.'},
                                        {'id': 'c',
                                         'texto': 'A $(0, 2)$ con $TR$ y a $(2, 0)$ con $RT$.',
                                         'correcta': False,
                                         'explicacion': 'Orden al revés: en un producto de matrices la de la '
                                                        'derecha actúa primero. $TR$ gira primero, así que '
                                                        'el origen termina donde lo deja $T$: $(2, 0)$.'},
                                        {'id': 'd',
                                         'texto': 'A $(0, 0)$ en los dos casos: el origen es fijo para toda '
                                                  'matriz.',
                                         'correcta': False,
                                         'explicacion': 'Eso vale para una $2\\times2$, que hace $A\\,0 = '
                                                        '0$. Las $3\\times3$ homogéneas existen justamente '
                                                        'para mover el origen: $H(0, 0, 1)^T$ es la tercera '
                                                        'columna.'}],
                           'rubrica': 'Afinidades · medio: componer afinidades es multiplicar matrices 3×3; '
                                      'el orden importa salvo casos especiales'},
                          {'id': '04_a1',
                           'nivel': 'avanzado',
                           'enunciado': 'La afinidad $A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$, '
                                        '$t = (1, 2)$ lleva $(0, 0) \\mapsto (1, 2)$, $(1, 0) \\mapsto (3, '
                                        '3)$, $(0, 1) \\mapsto (2, 4)$. ¿Tiene algún punto fijo?',
                           'opciones': [{'id': 'a',
                                         'texto': 'Sí, el origen: toda matriz deja quieto al origen.',
                                         'correcta': False,
                                         'explicacion': 'Eso vale para la parte lineal, no para $Ax + t$: el '
                                                        'origen va a $t = (1, 2)$. El punto fijo es el que '
                                                        'cumple $Ax + t = x$, no $Ax = 0$.'},
                                        {'id': 'b',
                                         'texto': 'No: $I - A$ es singular y el sistema $(I - A)x = t$ es '
                                                  'incompatible ($-x - y = 1$ y $-x - y = 2$ a la vez).',
                                         'correcta': True,
                                         'explicacion': '$\\det(I - A) = 1 - 1 = 0$ y $t$ no está en la '
                                                        'imagen de $I - A$. En la $3\\times3$ el autovector '
                                                        'de autovalor $1$ es $(1, -1, 0)$: un punto ideal, '
                                                        'la dirección $(1, -1)$ se conserva pero ningún '
                                                        'punto propio queda quieto.'},
                                        {'id': 'c',
                                         'texto': 'Sí, $x = (I - A)^{-1}\\,t$: una afinidad siempre tiene un '
                                                  'punto fijo.',
                                         'correcta': False,
                                         'explicacion': 'La fórmula vale cuando $I - A$ es invertible, es '
                                                        'decir cuando $1$ no es autovalor de $A$. Acá $A(1, '
                                                        '-1) = (1, -1)$: hay una dirección con autovalor $1$ '
                                                        'y la inversa no existe.'},
                                        {'id': 'd',
                                         'texto': 'No, porque $\\det A = 3 \\neq 1$ y sólo las isometrías '
                                                  'tienen punto fijo.',
                                         'correcta': False,
                                         'explicacion': 'El determinante no decide: una similaridad con $k '
                                                        '\\neq 1$ tiene $\\det = k^2 \\neq 1$ y siempre '
                                                        'tiene centro. Lo que decide es si $1$ es autovalor '
                                                        'de $A$ y si $t$ es compatible.'}],
                           'rubrica': 'Afinidades · avanzado: los puntos fijos del plano son los '
                                      'autovectores de la 3×3; un autovector con tercera coordenada nula es '
                                      'una dirección conservada'},
                          {'id': '04_a2',
                           'nivel': 'avanzado',
                           'enunciado': 'La afinidad axial de eje $x$, dirección $(1, 1)$ y factor $2$ es $M '
                                        '= B\\,\\mathrm{diag}(1, 2)\\,B^{-1} = \\begin{pmatrix} 1 & 1 \\\\ 0 '
                                        '& 2 \\end{pmatrix}$ con $B = \\begin{pmatrix} 1 & 1 \\\\ 0 & 1 '
                                        '\\end{pmatrix}$. ¿Qué queda fijo y cuánto vale $\\det M$?',
                           'opciones': [{'id': 'a',
                                         'texto': 'Queda fijo sólo el origen y $\\det M = 4$, porque el '
                                                  'factor $2$ actúa en las dos direcciones.',
                                         'correcta': False,
                                         'explicacion': 'El factor $2$ actúa en una sola dirección, $(1, '
                                                        '1)$; sobre el eje $x$ el factor es $1$. Por eso '
                                                        '$\\det M = 1 \\cdot 2 = 2$, y el eje entero queda '
                                                        'quieto, no sólo el origen.'},
                                        {'id': 'b',
                                         'texto': 'Queda fijo el eje $x$ punto a punto y $\\det M = 1$, como '
                                                  'en un corte.',
                                         'correcta': False,
                                         'explicacion': 'El corte $\\begin{pmatrix} 1 & s \\\\ 0 & 1 '
                                                        '\\end{pmatrix}$ conserva el área porque no estira '
                                                        'nada. Acá $M(x, y) = (x + y, 2y)$: la coordenada '
                                                        '$y$ se duplica y el área también.'},
                                        {'id': 'c',
                                         'texto': 'Queda fijo el eje $x$ punto a punto, cada punto se '
                                                  'desliza por su paralela a $(1, 1)$ al doble de distancia, '
                                                  'y $\\det M = 2$.',
                                         'correcta': True,
                                         'explicacion': '$M(x, 0) = (x, 0)$ y $M(x, y) - (x, y) = y\\,(1, '
                                                        '1)$: el desplazamiento va en la dirección $(1, 1)$ '
                                                        'y crece con la distancia al eje. El determinante es '
                                                        'el de la diagonal, $1 \\cdot 2 = 2$, porque '
                                                        'conjugar con $B$ no lo cambia.'},
                                        {'id': 'd',
                                         'texto': 'Queda fija la recta $y = x$ y $\\det M = 2$.',
                                         'correcta': False,
                                         'explicacion': '$(1, 1)$ es la dirección de deslizamiento, un '
                                                        'autovector de autovalor $2$: la recta $y = x$ se '
                                                        'mapea sobre sí misma pero sus puntos se alejan al '
                                                        'doble. La fija punto a punto es el eje, de '
                                                        'autovalor $1$.'}],
                           'rubrica': 'Afinidades · avanzado: ver la descomposición '
                                      'rotación–diagonal–rotación como afinidades axiales sucesivas '
                                      '(adelanto de la SVD)'}],
 '05_proyectivas': [{'id': '05_e1',
                     'nivel': 'elemental',
                     'enunciado': 'Un dron fotografió un lote cuadrado con la cámara inclinada. ¿Qué '
                                  'conserva la transformación proyectiva del terreno a la foto?',
                     'opciones': [{'id': 'a',
                                   'texto': 'Rectas y paralelas, aunque no los ángulos.',
                                   'correcta': False,
                                   'explicacion': 'Eso es una afinidad (última fila $(0, 0, 1)$). En la foto '
                                                  'los alambrados paralelos se juntan en un punto de fuga: '
                                                  'el paralelismo se pierde.'},
                                  {'id': 'b',
                                   'texto': 'Rectas e incidencia, nada más: ni paralelas, ni punto medio, ni '
                                            'ángulos.',
                                   'correcta': True,
                                   'explicacion': 'Una $3\\times3$ invertible manda rayos a rayos: las '
                                                  'rectas siguen rectas y los puntos alineados siguen '
                                                  'alineados. Lo único métrico que sobrevive es la razón '
                                                  'doble de cuatro puntos alineados.'},
                                  {'id': 'c',
                                   'texto': 'Rectas, paralelas y ángulos, pero no las distancias.',
                                   'correcta': False,
                                   'explicacion': 'Eso es una similaridad, la foto tomada desde arriba y '
                                                  'bien vertical. Con la cámara inclinada un cuadrado sale '
                                                  'como trapecio: los ángulos cambian.'},
                                  {'id': 'd',
                                   'texto': 'Nada: en una foto hasta las rectas pueden salir curvas.',
                                   'correcta': False,
                                   'explicacion': 'Una cámara ideal (sin distorsión de lente) es una '
                                                  'proyectiva, y una proyectiva lleva rectas a rectas. Los '
                                                  'alambrados salen rectos, sólo que ya no paralelos.'}],
                     'rubrica': 'Proyectivas · elemental: una proyectiva conserva rectas, nada más; la foto '
                                'de un lote rectangular es un trapecio'},
                    {'id': '05_e2',
                     'nivel': 'elemental',
                     'enunciado': 'Con la $H$ de la foto, el centro del lote da $H\\,(2, 2, 1)^T = (3, 2, '
                                  '1.5)^T$. ¿En qué punto de la foto aparece el centro?',
                     'opciones': [{'id': 'a',
                                   'texto': 'En $(3, 2)$.',
                                   'correcta': False,
                                   'explicacion': 'Son las dos primeras coordenadas sin dividir por la '
                                                  'tercera: el rayo, no el punto. En homogéneas $(3, 2, '
                                                  '1.5)$ y $(2, 1.333, 1)$ son el mismo punto, y sólo el '
                                                  'segundo se lee en el plano $W = 1$.'},
                                  {'id': 'b',
                                   'texto': 'En $(4.5, 3)$.',
                                   'correcta': False,
                                   'explicacion': 'Multiplicó por $1.5$ en vez de dividir. Volver al plano '
                                                  'es escalar la terna hasta que la tercera coordenada valga '
                                                  '$1$: dividir por $W$.'},
                                  {'id': 'c',
                                   'texto': 'En $(2, 1.333)$.',
                                   'correcta': True,
                                   'explicacion': '$(3/1.5,\\ 2/1.5) = (2, 4/3)$: justo el cruce de las '
                                                  'diagonales de la foto. Queda más arriba que la mitad del '
                                                  'trapecio (que está en $y = 1$), hacia el lado lejano, '
                                                  'porque ese lado se achica.'},
                                  {'id': 'd',
                                   'texto': 'En $(2, 2)$: una homografía deja quieto el centro del '
                                            'cuadrilátero.',
                                   'correcta': False,
                                   'explicacion': '$(2, 2)$ es el centro en el terreno. La foto corrió las '
                                                  'esquinas de arriba a $(1, 2)$ y $(3, 2)$; el centro se '
                                                  'mueve con ellas y cae donde se cruzan las diagonales.'}],
                     'rubrica': 'Proyectivas · elemental: los puntos son rayos, (x, y, 1) y λ(x, y, 1) son '
                                'el mismo punto; normalizar dividiendo por W recupera el plano'},
                    {'id': '05_m1',
                     'nivel': 'medio',
                     'enunciado': 'Para rectificar la foto necesitamos la homografía $H$. ¿Cuántos mojones '
                                  'de coordenadas conocidas hacen falta, y por qué?',
                     'opciones': [{'id': 'a',
                                   'texto': 'Tres, como en la afinidad: cada mojón da dos ecuaciones y hay '
                                            'seis incógnitas.',
                                   'correcta': False,
                                   'explicacion': 'Seis incógnitas son las de la afinidad, con la fila $3$ '
                                                  'fijada en $(0, 0, 1)$. En la proyectiva esa fila también '
                                                  'es incógnita; con tres puntos falta decidir cuánta '
                                                  'perspectiva hay.'},
                                  {'id': 'b',
                                   'texto': 'Nueve, uno por cada entrada de la matriz $3\\times3$.',
                                   'correcta': False,
                                   'explicacion': 'Cada mojón aporta dos ecuaciones, no una, y $H$ está '
                                                  'definida a menos de escala: son $8$ grados de libertad, '
                                                  'no $9$. Nueve puntos sobran (y sólo sirven para mínimos '
                                                  'cuadrados).'},
                                  {'id': 'c',
                                   'texto': 'Cuatro, sin tres alineados: nueve números menos la escala son '
                                            'ocho incógnitas, dos ecuaciones por mojón.',
                                   'correcta': True,
                                   'explicacion': '$u = (h_{11}x + h_{12}y + h_{13})/(h_{31}x + h_{32}y + '
                                                  'h_{33})$ y lo mismo para $v$: dos ecuaciones lineales por '
                                                  'par. Con $h_{33} = 1$ queda un $8\\times8$; si tres '
                                                  'mojones están alineados, las ecuaciones se vuelven '
                                                  'dependientes.'},
                                  {'id': 'd',
                                   'texto': 'Cuatro cualesquiera, aunque tres estén sobre una misma recta.',
                                   'correcta': False,
                                   'explicacion': 'Tres alineados dan ecuaciones dependientes (el '
                                                  'determinante de sus ternas es cero) y el sistema no fija '
                                                  '$H$. Hace falta un cuadrilátero de verdad.'}],
                     'rubrica': 'Proyectivas · medio: cuatro puntos, sin tres alineados, determinan la '
                                'homografía; con tres puntos falta decidir cuánta perspectiva hay'},
                    {'id': '05_m2',
                     'nivel': 'medio',
                     'enunciado': 'Con $H = \\begin{pmatrix} 1 & 0.5 & 0 \\\\ 0 & 1 & 0 \\\\ 0 & 0.25 & 1 '
                                  '\\end{pmatrix}$, ¿a dónde va el punto impropio $(0, 1, 0)$ de las rectas '
                                  '$x = $ cte?',
                     'opciones': [{'id': 'a',
                                   'texto': 'Sigue impropio: las rectas $x = $ cte siguen paralelas en la '
                                            'foto.',
                                   'correcta': False,
                                   'explicacion': 'Eso le pasa a $(1, 0, 0)$, cuya imagen es la columna $1$, '
                                                  '$(1, 0, 0)$, con $W = 0$. La columna $2$ tiene $W = 0.25 '
                                                  '\\neq 0$: ese punto ideal se hizo propio.'},
                                  {'id': 'b',
                                   'texto': 'A $(0.5, 1)$, la segunda columna de $H$.',
                                   'correcta': False,
                                   'explicacion': 'La segunda columna es $(0.5, 1, 0.25)$, y falta dividir '
                                                  'por $0.25$. Sin dividir es el rayo; el punto del plano es '
                                                  '$(2, 4)$.'},
                                  {'id': 'c',
                                   'texto': 'A $(0, 1)$: una homografía no mueve las direcciones.',
                                   'correcta': False,
                                   'explicacion': 'Mover direcciones es justamente lo que hace la fila $3$: '
                                                  'un rayo paralelo al plano $W = 1$ se inclina hasta '
                                                  'cortarlo. Si no las moviera, sería una afinidad y no '
                                                  'habría punto de fuga.'},
                                  {'id': 'd',
                                   'texto': 'A $(2, 4)$, un punto propio: ahí se cruzan en la foto todas las '
                                            'rectas $x = $ cte.',
                                   'correcta': True,
                                   'explicacion': '$H(0, 1, 0)^T = (0.5, 1, 0.25)^T \\sim (2, 4, 1)^T$. Las '
                                                  'paralelas del terreno comparten ese punto ideal, y su '
                                                  'imagen común es el punto de fuga, arriba del lote: por '
                                                  'eso el trapecio se angosta hacia arriba.'}],
                     'rubrica': 'Proyectivas · elemental: las paralelas dejan de serlo, se cortan en un '
                                'punto de fuga; el punto ideal común se hizo propio'},
                    {'id': '05_a1',
                     'nivel': 'avanzado',
                     'enunciado': 'El pentágono regular del profesor, con $D = (0, 1)$ arriba y $A$, $B$ '
                                  'abajo. La proyectiva $H = \\begin{pmatrix} -\\sqrt5 & 0 & 0 \\\\ 0 & -1 & '
                                  '1 \\\\ 0 & 4 & 1 \\end{pmatrix}$ deja fijos $A$ y $B$ e intercambia $C$ '
                                  'con $E$. ¿Dónde cae $D$ y cómo queda la imagen?',
                     'opciones': [{'id': 'a',
                                   'texto': '$D$ cae en el centro $(0, 0)$ y la imagen es otro pentágono '
                                            'convexo: las rectas van a rectas.',
                                   'correcta': False,
                                   'explicacion': '$D$ sí cae en el centro, pero la recta $4y + 1 = 0$ que '
                                                  'se va al infinito pasa entre $AB$ y $CE$: los lados que '
                                                  'la cruzan se vuelven dos semirrectas y la figura se '
                                                  'parte.'},
                                  {'id': 'b',
                                   'texto': '$D$ queda fijo, porque está sobre el eje de simetría $x = 0$ '
                                            'del pentágono.',
                                   'correcta': False,
                                   'explicacion': 'El eje de simetría no es una recta fija de $H$. Lo fijo '
                                                  'es la recta $AB$ (punto a punto) y el centro $(0, '
                                                  '0.309)$; $D$ está en $x = 0$ pero $H(0, 1, 1)^T = (0, 0, '
                                                  '5)^T$: va a $(0, 0)$.'},
                                  {'id': 'c',
                                   'texto': '$D$ cae en el centro $(0, 0)$ y la imagen se parte, porque la '
                                            'recta $y = -1/4$ que va al infinito cruza el pentágono.',
                                   'correcta': True,
                                   'explicacion': '$H\\vec D = (0, -1 + 1, 4 + 1) = (0, 0, 5)$. La fila $3$ '
                                                  'da $W = 4y + 1$: negativa en $A$ y $B$ ($y = -0.809$), '
                                                  'positiva en $C$, $D$, $E$; donde $W$ cambia de signo la '
                                                  'imagen pasa por el infinito.'},
                                  {'id': 'd',
                                   'texto': '$D$ se va al infinito, porque es el único vértice que no '
                                            'aparece entre los datos.',
                                   'correcta': False,
                                   'explicacion': 'Al infinito se van los puntos con $W = 0$, los de la '
                                                  'recta $y = -1/4$; $D$ tiene $W = 5$. Que no esté en los '
                                                  'datos no lo exime: la homografía queda fijada por los '
                                                  'otros cuatro.'}],
                     'rubrica': 'Proyectivas · avanzado: analizar el caso en que la imagen de un polígono se '
                                'parte porque un lado cruza la recta que va al infinito (ejercicio del '
                                'pentágono)'},
                    {'id': '05_a2',
                     'nivel': 'avanzado',
                     'enunciado': 'Calculamos $H^2 = 5I$ para la $H$ del pentágono. ¿Qué significa '
                                  'geométricamente?',
                     'opciones': [{'id': 'a',
                                   'texto': 'Aplicarla dos veces es la identidad, porque $5I \\sim I$ en '
                                            'homogéneas: es un espejo proyectivo, una homología armónica con '
                                            'eje $AB$.',
                                   'correcta': True,
                                   'explicacion': 'Las matrices proporcionales son la misma homografía. $H$ '
                                                  'intercambia $C$ con $E$ y manda $D$ al centro del '
                                                  "pentágono; la razón doble $(D, D'; O, X) = -1$ confirma "
                                                  "la cuaterna armónica, con $D = (0, 1)$, su imagen $D' = "
                                                  '(0, 0)$, el centro de la homología $O = (0, 0.309)$ y el '
                                                  'corte $X = (0, -0.809)$ con el eje $AB$.'},
                                  {'id': 'b',
                                   'texto': 'Aplicarla dos veces multiplica todas las coordenadas por $5$: '
                                            'una homotecia de factor $5$ desde el origen.',
                                   'correcta': False,
                                   'explicacion': 'Ignora la escala homogénea: $(5x, 5y, 5)$ es el punto '
                                                  '$(x, y)$, no $(5x, 5y)$. Una homotecia de factor $5$ '
                                                  'sería $\\mathrm{diag}(5, 5, 1)$, no $5I$.'},
                                  {'id': 'c',
                                   'texto': '$H$ es $\\sqrt5\\,I$, una homotecia, porque $H^2 = 5I$ obliga a '
                                            '$H = \\sqrt5\\,I$.',
                                   'correcta': False,
                                   'explicacion': 'Una matriz tiene muchas raíces cuadradas: $H$ no es '
                                                  'diagonal y tiene autovalores $-\\sqrt5$ (doble, sobre '
                                                  '$AB$) y $+\\sqrt5$. $\\sqrt5\\,I$ no intercambiaría '
                                                  'nada.'},
                                  {'id': 'd',
                                   'texto': 'Que $H$ no tiene puntos fijos propios: sus autovalores '
                                            '$\\pm\\sqrt5$ sólo fijan direcciones.',
                                   'correcta': False,
                                   'explicacion': '$A$ y $B$ son fijos y propios: $H\\vec A = '
                                                  '-\\sqrt5\\,\\vec A$ con $W \\neq 0$. El autovalor doble '
                                                  '$-\\sqrt5$ tiene todo un plano de autovectores, la recta '
                                                  '$AB$ entera, más el centro $(0, 0.309)$ para '
                                                  '$+\\sqrt5$.'}],
                     'rubrica': 'Proyectivas · avanzado: razón doble como invariante; reconocer la homología '
                                'y sus autovalores repetidos'}],
 '06_formas_lineales': [{'id': '06_e1',
                         'nivel': 'elemental',
                         'enunciado': 'El profesor dijo que no existe el vector fila. ¿Qué es, entonces, una '
                                      'forma lineal $\\ell = (a, b)$?',
                         'opciones': [{'id': 'a',
                                       'texto': 'Un vector escrito acostado, que se dibuja como una flecha '
                                                'igual que $(a, b)^T$.',
                                       'correcta': False,
                                       'explicacion': 'La flecha $(a, b)$ sólo representa a la forma en la '
                                                      'base canónica, a través del producto interno. Si se '
                                                      'deforma el plano con una $A$ que no lo conserva, la '
                                                      'flecha $A(a, b)^T$ ya no dice nada sobre la regla.'},
                                      {'id': 'b',
                                       'texto': 'La recta $ax + by = 0$ que pasa por el origen.',
                                       'correcta': False,
                                       'explicacion': 'Esa recta es sólo su marca cero (el núcleo). La forma '
                                                      'es toda la familia de rectas $ax + by = k$, una por '
                                                      'cada valor, equiespaciadas.'},
                                      {'id': 'c',
                                       'texto': 'Una regla graduada: una función que a cada vector le asigna '
                                                'un número respetando sumas y escalas, dibujada como rectas '
                                                'de nivel paralelas y equiespaciadas.',
                                       'correcta': True,
                                       'explicacion': '$\\ell(p) = ax + by$ es fila por columna; sus curvas '
                                                      'de nivel son rectas paralelas separadas $1/\\lvert(a, '
                                                      'b)\\rvert$. Dos formas dan una grilla, y todas juntas '
                                                      'forman el espacio dual.'},
                                      {'id': 'd',
                                       'texto': 'Una matriz $2\\times2$ que lleva rectas a rectas.',
                                       'correcta': False,
                                       'explicacion': 'Una matriz $2\\times2$ devuelve un vector; la forma '
                                                      'devuelve un número. La forma es una sola fila; una '
                                                      'matriz es una pila de formas, una por cada coordenada '
                                                      'de salida.'}],
                         'rubrica': 'Productos · elemental: una forma lineal es una regla graduada, familia '
                                    'de rectas paralelas equiespaciadas; la matriz es una pila de reglas'},
                        {'id': '06_e2',
                         'nivel': 'elemental',
                         'enunciado': 'La regla $\\ell = (3, 4)$. ¿Qué marca pasa por el punto $(2, 1)$ y a '
                                      'qué distancia están sus marcas enteras?',
                         'opciones': [{'id': 'a',
                                       'texto': 'La marca $11$, con marcas cada $0.2$.',
                                       'correcta': False,
                                       'explicacion': '$11 = 3 \\cdot 1 + 4 \\cdot 2$: se cruzaron las '
                                                      'coordenadas. La fila multiplica la primera coordenada '
                                                      'por $3$ y la segunda por $4$.'},
                                      {'id': 'b',
                                       'texto': 'La marca $10$, con marcas cada $0.2$.',
                                       'correcta': True,
                                       'explicacion': '$\\ell(2, 1) = 3 \\cdot 2 + 4 \\cdot 1 = 10$: la '
                                                      'recta $3x + 4y = 10$. Como $\\lvert(3, 4)\\rvert = '
                                                      '5$, las marcas enteras están separadas $1/5$: cuanto '
                                                      'más larga la fila, más apretadas las marcas.'},
                                      {'id': 'c',
                                       'texto': 'La marca $10$, con marcas cada $5$.',
                                       'correcta': False,
                                       'explicacion': 'Invierte la separación. Un vector de módulo $5$ cruza '
                                                      'cinco marcas en una unidad de distancia '
                                                      'perpendicular: están cada $1/5$, no cada $5$.'},
                                      {'id': 'd',
                                       'texto': 'La marca $5$, porque la marca es el módulo de la fila.',
                                       'correcta': False,
                                       'explicacion': 'El módulo $5$ fija la separación de las marcas, no la '
                                                      'lectura. La lectura en un punto es fila por columna: '
                                                      '$3 \\cdot 2 + 4 \\cdot 1$.'}],
                         'rubrica': 'Productos · elemental: una forma lineal es una regla graduada; '
                                    'separación de las marcas y lectura en un punto'},
                        {'id': '06_m1',
                         'nivel': 'medio',
                         'enunciado': 'La cota es $h = 2x + y + 100$ y el plano digitalizado quedó deformado '
                                      'por $A = \\begin{pmatrix} 2 & 1 \\\\ 0 & 1 \\end{pmatrix}$: cada '
                                      "punto aparece en $p' = Ap$. Sea $\\ell = (2, 1)$ la fila de la cota. "
                                      "¿Qué fila $\\ell'$ lee sobre $p' = Ap$, para todo $p$, la misma cota "
                                      'que $\\ell$ sobre $p$?',
                         'opciones': [{'id': 'a',
                                       'texto': '$(5, 1)$.',
                                       'correcta': False,
                                       'explicacion': 'Es $A\\,\\ell^T$: la fila movida como si fuera un '
                                                      "punto. Sobre $p' = (3, 1)$ lee $16$ en vez de $3$; "
                                                      'una fila no es una flecha y no va con $A$.'},
                                      {'id': 'b',
                                       'texto': '$(4, 3)$.',
                                       'correcta': False,
                                       'explicacion': 'Es $\\ell A$, el lado correcto pero sin invertir. Esa '
                                                      'regla lee sobre el $p$ original lo que $\\ell$ lee '
                                                      'sobre $Ap$ ($(4, 3)\\cdot(1, 1) = 7 = (2, 1)\\cdot(3, '
                                                      "1)$); sobre $p'$ da $15$."},
                                      {'id': 'c',
                                       'texto': '$(2, 1)$, la misma: la cota del mojón no cambió.',
                                       'correcta': False,
                                       'explicacion': 'La cota no cambió, pero las coordenadas sí: $(2, '
                                                      '1)\\cdot(3, 1) = 7$, el mojón subiría $4$ m sin '
                                                      'moverse. Los coeficientes de la fila dependen de las '
                                                      'coordenadas de los puntos.'},
                                      {'id': 'd',
                                       'texto': '$(1, 0)$.',
                                       'correcta': True,
                                       'explicacion': "$\\ell' = \\ell A^{-1} = (2, 1)\\begin{pmatrix} 1/2 & "
                                                      '-1/2 \\\\ 0 & 1 \\end{pmatrix} = (1, 0)$, y $(1, '
                                                      '0)\\cdot(3, 1) = 3 = (2, 1)\\cdot(1, 1)$. Las marcas '
                                                      'quedaron verticales: la regla se deformó con la '
                                                      'figura.'}],
                         'rubrica': 'Productos · medio: las formas lineales forman el dual y se transforman '
                                    'del lado contrario que los vectores; las rectas de nivel se arrastran '
                                    'con la figura'},
                        {'id': '06_m2',
                         'nivel': 'medio',
                         'enunciado': 'Queremos la recta por $p = (1, 1)$ y $q = (3, 2)$ como fila homogénea '
                                      '$(a, b, c)$ con $ax + by + c = 0$. ¿Qué obtenemos con el producto '
                                      'vectorial de las ternas $(1, 1, 1)$ y $(3, 2, 1)$?',
                         'opciones': [{'id': 'a',
                                       'texto': '$(-1, 2, -1)$: la recta $-x + 2y - 1 = 0$.',
                                       'correcta': True,
                                       'explicacion': '$(1 \\cdot 1 - 1 \\cdot 2,\\ 1 \\cdot 3 - 1 \\cdot '
                                                      '1,\\ 1 \\cdot 2 - 1 \\cdot 3) = (-1, 2, -1)$, y lee '
                                                      '$0$ en las dos ternas: $-1 + 2 - 1 = 0$, $-3 + 4 - 1 '
                                                      '= 0$. Con signo cambiado o escalada es la misma '
                                                      'recta.'},
                                      {'id': 'b',
                                       'texto': '$(2, 1, 0)$: la diferencia de las ternas.',
                                       'correcta': False,
                                       'explicacion': '$q - p$ con tercera coordenada $0$ es la dirección de '
                                                      'la recta, un punto impropio, no la fila que la '
                                                      'describe. Leída como fila da $2x + y$, que no se '
                                                      'anula en $p$.'},
                                      {'id': 'c',
                                       'texto': '$-1$, el área con signo de $p$ y $q$.',
                                       'correcta': False,
                                       'explicacion': '$1 \\cdot 2 - 1 \\cdot 3 = -1$ es la cuña de los '
                                                      'vectores del plano, un número: dice que $p$ y $q$ no '
                                                      'están alineados con el origen. La recta sale de la '
                                                      'cuña de las ternas homogéneas, que tiene tres '
                                                      'componentes.'},
                                      {'id': 'd',
                                       'texto': '$(4, 3, 2)$: la suma de las ternas.',
                                       'correcta': False,
                                       'explicacion': 'La suma de ternas es otro punto, $(2, 1.5)$, el punto '
                                                      'medio del segmento. Es un punto y no una recta: leído '
                                                      'como fila no se anula ni en $p$ ni en $q$.'}],
                         'rubrica': 'Productos · elemental: el producto interno decide incidencia y el '
                                    "vectorial une dos puntos y corta dos rectas; ℓ·p = 0 es 'el punto está "
                                    "en la recta'"},
                        {'id': '06_a1',
                         'nivel': 'avanzado',
                         'enunciado': 'Si los puntos van con $A$ (a la izquierda), ¿por qué una recta, o '
                                      'cualquier forma $\\ell$, tiene que ir con $A^{-1}$ a la derecha, y no '
                                      'con $A$?',
                         'opciones': [{'id': 'a',
                                       'texto': 'Porque la fila es el vector traspuesto, y la traspuesta de '
                                                '$A$ es su inversa.',
                                       'correcta': False,
                                       'explicacion': '$A^T = A^{-1}$ sólo para rotaciones y reflexiones; '
                                                      'por eso con un giro la dualidad no se ve. Con '
                                                      '$\\mathrm{diag}(2, 1)$ la traspuesta es la misma '
                                                      'matriz y la fila debe ir con $\\mathrm{diag}(1/2, '
                                                      '1)$.'},
                                      {'id': 'b',
                                       'texto': "Porque $\\ell A$ lee sobre $p' = Ap$ lo mismo que $\\ell$ "
                                                'sobre $p$.',
                                       'correcta': False,
                                       'explicacion': 'Al revés: $(\\ell A)(p) = \\ell(Ap)$, o sea $\\ell A$ '
                                                      'lee sobre el $p$ original lo que $\\ell$ lee sobre '
                                                      "$Ap$. Para leer sobre $p'$ hay que deshacer $A$: "
                                                      '$\\ell A^{-1}$.'},
                                      {'id': 'c',
                                       'texto': 'Para que la lectura no cambie: $(\\ell A^{-1})(Ap) = \\ell '
                                                'p$, así un punto que estaba en la recta $\\ell p = 0$ sigue '
                                                'estando en su imagen.',
                                       'correcta': True,
                                       'explicacion': 'Es la dualidad: convertimos todo para que nada '
                                                      'cambie. En homogéneas una recta fija es una fila con '
                                                      '$\\ell H \\sim \\ell$, es decir un autovector de '
                                                      '$H^T$; por eso el eje de la homología del pentágono '
                                                      'aparece del lado de las filas.'},
                                      {'id': 'd',
                                       'texto': 'Porque las rectas no se mueven: sólo se transforman los '
                                                'puntos.',
                                       'correcta': False,
                                       'explicacion': 'Si la recta quedara quieta, sus puntos movidos ya no '
                                                      'estarían sobre ella: $(2, 1)\\cdot(3, 1) = 7 \\neq '
                                                      '3$. La recta se arrastra con la figura, con la matriz '
                                                      'inversa y del otro lado.'}],
                         'rubrica': 'Proyectivas · medio: las rectas fijas son formas lineales fijas, '
                                    'dualidad punto–recta (ℓ·p = 0) y su lectura como autovectores de Hᵀ'},
                        {'id': '06_a2',
                         'nivel': 'avanzado',
                         'enunciado': 'Alguien dice que el gradiente de una función es un vector, pero en '
                                      'realidad es una forma lineal. ¿Qué cambia en la práctica para la cota '
                                      '$h(x, y)$ de un terreno?',
                         'opciones': [{'id': 'a',
                                       'texto': 'Nada: los números $(h_x, h_y)$ son los mismos en cualquier '
                                                'grilla, y decir forma lineal en vez de vector es sólo una '
                                                'formalidad de nombre.',
                                       'correcta': False,
                                       'explicacion': 'Los números coinciden sólo en la base canónica con el '
                                                      'producto interno usual. Si cambiamos las unidades de '
                                                      'un eje, la fila se transforma con $A^{-1}$, mientras '
                                                      'una flecha iría con $A$: los números dejan de '
                                                      'coincidir.'},
                                      {'id': 'b',
                                       'texto': 'La flecha perpendicular a las curvas de nivel sólo tiene '
                                                'sentido con un producto interno fijado; si cambiamos las '
                                                'unidades de un eje, la flecha deja de ser perpendicular en '
                                                'el terreno, la regla sigue valiendo.',
                                       'correcta': True,
                                       'explicacion': 'El gradiente es la regla cuyas marcas son los '
                                                      'escalones de altura cerca del punto; su marca cero es '
                                                      'la tangente a la curva de nivel. Dibujarlo como '
                                                      'flecha perpendicular exige una métrica, y en el '
                                                      'elipsoide o con metros y pies mezclados esa métrica '
                                                      'no es la de la grilla.'},
                                      {'id': 'c',
                                       'texto': 'El gradiente deja de ser perpendicular a las curvas de '
                                                'nivel en cualquier sistema de coordenadas, porque su '
                                                'dirección depende de cómo dibujemos el plano.',
                                       'correcta': False,
                                       'explicacion': 'Demasiado fuerte: en la base canónica con el producto '
                                                      'interno usual la flecha $(h_x, h_y)$ sí es '
                                                      'perpendicular. Lo que falla es trasladar esa '
                                                      'perpendicularidad a otra grilla sin llevar también la '
                                                      'métrica.'},
                                      {'id': 'd',
                                       'texto': 'El gradiente pasa a transformarse como un punto, con $A$, '
                                                'en vez de con $A^{-1}$, porque al cambiar de grilla viaja '
                                                'igual que las posiciones del terreno.',
                                       'correcta': False,
                                       'explicacion': 'Justo al revés: por ser forma lineal se transforma '
                                                      'como una fila, con $A^{-1}$ a la derecha. Un vector '
                                                      'de verdad es el que va con $A$.'}],
                         'rubrica': 'Productos · avanzado: el gradiente es una forma lineal cuya recta de '
                                    'nivel cero es la tangente; de ahí que sea perpendicular a la curva de '
                                    'nivel'}],
 '07a_cuna_determinante': [{'id': '07a_e1',
                            'nivel': 'elemental',
                            'enunciado': 'Calculamos $\\det M = 0$ para la matriz de una transformación del '
                                         'plano. ¿Qué le pasa a la parcela?',
                            'opciones': [{'id': 'a',
                                          'texto': 'No cambia de área: el determinante mide cuánto se '
                                                   'agranda, y cero es nada.',
                                          'correcta': False,
                                          'explicacion': 'No cambiar el área es $\\det = 1$. Con $\\det = 0$ '
                                                         'el área después es $0$ por la de antes: la parcela '
                                                         'cae entera sobre una recta.'},
                                         {'id': 'b',
                                          'texto': 'Sale dada vuelta, como en un espejo.',
                                          'correcta': False,
                                          'explicacion': 'Dar vuelta la orientación es $\\det < 0$. En cero '
                                                         'no hay orientación que invertir: no queda área, el '
                                                         'paralelogramo unitario se aplastó a un segmento.'},
                                         {'id': 'c',
                                          'texto': 'Se aplasta sobre una recta (o un punto): las columnas '
                                                   'son colineales y no hay inversa.',
                                          'correcta': True,
                                          'explicacion': '$\\det M = Me_1 \\wedge Me_2 = 0$ dice que las '
                                                         'imágenes de los ejes están alineadas: todo el '
                                                         'plano cae en esa recta. No hay forma de '
                                                         'deshacerlo, como no existe $1/0$.'},
                                         {'id': 'd',
                                          'texto': 'Nada: una matriz con determinante cero es la matriz nula '
                                                   'y deja todo donde estaba.',
                                          'correcta': False,
                                          'explicacion': 'La matriz nula tiene $\\det = 0$, pero '
                                                         '$\\begin{pmatrix} 1 & 2 \\\\ 2 & 4 \\end{pmatrix}$ '
                                                         'también y no es nula. Y la nula no deja nada '
                                                         'quieto: manda todo al origen.'}],
                            'rubrica': 'Productos · medio: el determinante vale cero si hay dependencia '
                                       'lineal; hecho geométrico, es el área o volumen orientado'},
                           {'id': '07a_e2',
                            'nivel': 'elemental',
                            'enunciado': 'Tres mojones de un alambrado que debería ser recto: $A = (1, 1)$, '
                                         '$B = (4, 3)$, $C = (7, 6)$. ¿Cuánto da el detector $(B - A) '
                                         '\\wedge (C - A)$ y qué nos dice?',
                            'opciones': [{'id': 'a',
                                          'texto': '$3$: no están alineados, $C$ se salió del alambrado.',
                                          'correcta': True,
                                          'explicacion': '$(3, 2) \\wedge (6, 5) = 3 \\cdot 5 - 2 \\cdot 6 = '
                                                         '3$, el área del paralelogramo de lados $AB$ y '
                                                         '$AC$. Dividida por $\\lvert AB \\rvert = '
                                                         '\\sqrt{13}$ da $0.83$ m de desvío; con $C = (7, '
                                                         '5)$ daría $0$.'},
                                         {'id': 'b',
                                          'texto': '$28$: no están alineados.',
                                          'correcta': False,
                                          'explicacion': '$3 \\cdot 6 + 2 \\cdot 5 = 28$ es el producto '
                                                         'interno, que mide cuán paralelos son y vale cero '
                                                         'si son perpendiculares. El detector de '
                                                         'colinealidad es la cuña, con la resta cruzada.'},
                                         {'id': 'c',
                                          'texto': '$1.5$: no están alineados.',
                                          'correcta': False,
                                          'explicacion': '$1.5$ es el área del triángulo $ABC$. Detecta lo '
                                                         'mismo, pero el número de la cuenta $u_1 v_2 - u_2 '
                                                         'v_1$, y del determinante, es el del paralelogramo: '
                                                         'el doble.'},
                                         {'id': 'd',
                                          'texto': '$0$: están alineados, porque las tres coordenadas crecen '
                                                   'de a $3$.',
                                          'correcta': False,
                                          'explicacion': 'Las $x$ crecen de a $3$, pero las $y$ de a $2$ y '
                                                         'después de a $3$: $(6, 5)$ no es múltiplo de $(3, '
                                                         '2)$. El detector da $15 - 12 = 3$, que no es '
                                                         'cero.'}],
                            'rubrica': 'Productos · avanzado: el producto cuña arma formas lineales que '
                                       'detectan colinealidad'},
                           {'id': '07a_m1',
                            'nivel': 'medio',
                            'enunciado': 'La parcela tiene área con signo $12$ (recorrida antihorario). ¿Qué '
                                         'área con signo tiene después de $A = \\begin{pmatrix} 2 & 1 \\\\ 1 '
                                         '& 2 \\end{pmatrix}$, y qué área después del espejo '
                                         '$\\mathrm{diag}(1, -1)$ (cada transformación aplicada por separado '
                                         'a la parcela original)?',
                            'opciones': [{'id': 'a',
                                          'texto': '$36$ y $12$.',
                                          'correcta': False,
                                          'explicacion': 'El espejo tiene $\\det = -1$: el tamaño se '
                                                         'mantiene pero el recorrido pasa a horario, y el '
                                                         'área con signo cambia de signo. El signo del '
                                                         'determinante es información, no un detalle.'},
                                         {'id': 'b',
                                          'texto': '$48$ y $-12$.',
                                          'correcta': False,
                                          'explicacion': '$48 = 4 \\cdot 12$ usa sólo la diagonal $2 \\cdot '
                                                         '2$ y se olvida de restar $1 \\cdot 1$. $\\det A = '
                                                         '4 - 1 = 3$, y el área es $3 \\cdot 12 = 36$.'},
                                         {'id': 'c',
                                          'texto': '$36$ y $-12$.',
                                          'correcta': True,
                                          'explicacion': '$\\det A = 3$ multiplica el área de cualquier '
                                                         'figura por $3$, sea cual sea su forma. El espejo '
                                                         'tiene $\\det = -1$: mismo tamaño, orientación al '
                                                         'revés.'},
                                         {'id': 'd',
                                          'texto': '$36$ y $0$.',
                                          'correcta': False,
                                          'explicacion': '$1 + (-1) = 0$ suma la diagonal en vez de '
                                                         'multiplicarla. $\\det \\mathrm{diag}(1, -1) = -1$: '
                                                         'el espejo no aplasta nada, da vuelta.'}],
                            'rubrica': 'Productos · medio: el determinante es el área orientada; cuánto '
                                       'agranda y si da vuelta la orientación'},
                           {'id': '07a_m2',
                            'nivel': 'medio',
                            'enunciado': '¿Por qué $v \\wedge u = -\\,u \\wedge v$?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Porque la cuña es el producto interno con el signo '
                                                   'cambiado.',
                                          'correcta': False,
                                          'explicacion': 'Son operaciones distintas: $(3, 1)\\cdot(1, 2) = '
                                                         '5$ y $(3, 1) \\wedge (1, 2) = 5$ coinciden de '
                                                         'casualidad, pero el producto interno es simétrico '
                                                         'y mide paralelismo; la cuña mide área.'},
                                         {'id': 'b',
                                          'texto': 'No es así: la cuña es simétrica como el producto '
                                                   'interno, $u \\wedge v = v \\wedge u$.',
                                          'correcta': False,
                                          'explicacion': '$(3, 1) \\wedge (1, 2) = 5$ y $(1, 2) \\wedge (3, '
                                                         '1) = -5$. Dos signos distintos para el mismo par '
                                                         'de vectores: no es simétrica.'},
                                         {'id': 'c',
                                          'texto': 'Porque es lineal en cada vector y $w \\wedge w = 0$: '
                                                   'desarrollando $(u + v) \\wedge (u + v) = 0$ queda $u '
                                                   '\\wedge v + v \\wedge u = 0$.',
                                          'correcta': True,
                                          'explicacion': 'Son las dos reglas que definen el determinante: '
                                                         'lineal en cada argumento y nulo con dos vectores '
                                                         'iguales. De ahí sale la antisimetría; '
                                                         'geométricamente, recorrer el paralelogramo al '
                                                         'revés invierte la orientación.'},
                                         {'id': 'd',
                                          'texto': 'Porque invertir el orden es lo mismo que cambiar de '
                                                   'signo los dos vectores: $v \\wedge u = (-u) \\wedge '
                                                   '(-v)$.',
                                          'correcta': False,
                                          'explicacion': '$(-u) \\wedge (-v) = (-1)(-1)\\,u \\wedge v = '
                                                         '+\\,u \\wedge v$: cambiar de signo los dos '
                                                         'vectores no cambia nada. El signo menos viene del '
                                                         'orden, no de los signos.'}],
                            'rubrica': 'Productos · medio: el determinante es la única operación lineal en '
                                       'cada argumento y antisimétrica'},
                           {'id': '07a_a1',
                            'nivel': 'avanzado',
                            'enunciado': 'Para ver si tres mojones están alineados armamos el determinante '
                                         '$3\\times3$ con sus ternas $(x, y, 1)$ como filas. ¿Por qué '
                                         'detecta la alineación?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Porque la columna de unos hace que el determinante sea '
                                                   'siempre cero.',
                                          'correcta': False,
                                          'explicacion': 'Con $A = (1, 1)$, $B = (4, 3)$, $C = (7, 6)$ el '
                                                         'determinante da $3$, no cero. La columna de unos '
                                                         'no anula nada: desarrollando por ella queda $(B - '
                                                         'A) \\wedge (C - A)$.'},
                                         {'id': 'b',
                                          'texto': 'Porque tres puntos alineados en el plano $W = 1$ son '
                                                   'tres rayos que caben en un mismo plano por el origen de '
                                                   '$\\mathbb R^3$: la caja tiene volumen cero.',
                                          'correcta': True,
                                          'explicacion': 'Cada mojón es un rayo; una recta del plano es un '
                                                         'plano por el origen. Tres ternas en un plano son '
                                                         'linealmente dependientes y el volumen orientado '
                                                         '$\\det[\\vec A\\ \\vec B\\ \\vec C]$ se anula. Es '
                                                         'la misma condición «sin tres alineados» de la '
                                                         'homografía.'},
                                         {'id': 'c',
                                          'texto': 'Porque con la columna de unos el determinante se reduce '
                                                   'al producto interno $(B - A) \\cdot (C - A)$, que es '
                                                   'cero si están alineados.',
                                          'correcta': False,
                                          'explicacion': 'El producto interno vale cero cuando los vectores '
                                                         'son perpendiculares, no cuando están alineados. Lo '
                                                         'que queda al desarrollar es la cuña $(B - A) '
                                                         '\\wedge (C - A)$.'},
                                         {'id': 'd',
                                          'texto': 'No lo detecta: hace falta comparar pendientes, $(y_B - '
                                                   'y_A)/(x_B - x_A) = (y_C - y_A)/(x_C - x_A)$.',
                                          'correcta': False,
                                          'explicacion': 'Las pendientes dicen lo mismo pero fallan con una '
                                                         'recta vertical (división por cero). El '
                                                         'determinante es la misma condición escrita sin '
                                                         'dividir: $(x_B - x_A)(y_C - y_A) - (y_B - y_A)(x_C '
                                                         '- x_A) = 0$.'}],
                            'rubrica': 'Productos · avanzado: el producto cuña generaliza el determinante a '
                                       'cualquier dimensión y detecta colinealidad; alineación en '
                                       'homogéneas'},
                           {'id': '07a_a2',
                            'nivel': 'avanzado',
                            'enunciado': 'Animamos de la identidad al espejo con $M(s) = (1 - s)\\,I + '
                                         's\\,\\mathrm{diag}(1, -1) = \\mathrm{diag}(1, 1 - 2s)$, $s$ de $0$ '
                                         'a $1$. ¿Qué le pasa a la parcela en el camino?',
                            'opciones': [{'id': 'a',
                                          'texto': 'El determinante va de $1$ a $-1$ sin sobresaltos: la '
                                                   'parcela sólo gira hasta quedar dada vuelta.',
                                          'correcta': False,
                                          'explicacion': 'Un giro mantiene $\\det = +1$ todo el tiempo. Para '
                                                         'pasar de $+1$ a $-1$ por un camino continuo el '
                                                         'determinante tiene que valer cero en algún '
                                                         'momento: no hay giro que dé vuelta una hoja.'},
                                         {'id': 'b',
                                          'texto': 'El determinante baja de $2$ a $0$ como $1 + (1 - 2s)$ y '
                                                   'nunca es negativo.',
                                          'correcta': False,
                                          'explicacion': 'Sumó la diagonal: eso es la traza. El determinante '
                                                         'de una diagonal es el producto, $1 \\cdot (1 - '
                                                         '2s)$, que vale $1$ en $s = 0$ y $-1$ en $s = 1$.'},
                                         {'id': 'c',
                                          'texto': 'En $s = 1/2$ el determinante vale $0$: la parcela se '
                                                   'aplasta sobre el eje $x$ y después sale dada vuelta; no '
                                                   'se puede invertir la orientación sin pasar por un '
                                                   'aplastamiento.',
                                          'correcta': True,
                                          'explicacion': '$\\det M(s) = 1 - 2s$ cruza cero en $s = 1/2$, '
                                                         'donde $M = \\mathrm{diag}(1, 0)$ manda toda la '
                                                         'dirección $e_2$ al cero: núcleo. Por eso las '
                                                         'rotaciones ($\\det = +1$) y las reflexiones '
                                                         '($\\det = -1$) son dos familias separadas.'},
                                         {'id': 'd',
                                          'texto': 'El determinante es $-1$ en todo el camino, porque el '
                                                   'espejo de llegada es fijo.',
                                          'correcta': False,
                                          'explicacion': 'En $s = 0$ la matriz es la identidad, con $\\det = '
                                                         '1$. El determinante depende de la matriz en cada '
                                                         'instante, $1 - 2s$, no del destino.'}],
                            'rubrica': 'Productos · medio: el núcleo es lo que va al cero; una '
                                       'transformación con núcleo aplasta una dirección entera a un punto'}],
 '07b_nucleo_autovectores': [{'id': '07b_e1',
                              'nivel': 'elemental',
                              'enunciado': 'Hablamos del **núcleo** de una transformación lineal $A$. ¿Qué '
                                           'es?',
                              'opciones': [{'id': 'a',
                                            'texto': 'Los vectores que $A$ deja quietos, los que cumplen $Av '
                                                     '= v$.',
                                            'correcta': False,
                                            'explicacion': 'Eso es el autoespacio de $\\lambda = 1$, no el '
                                                           'núcleo. El núcleo es el autoespacio de $\\lambda '
                                                           '= 0$: lo que va al cero, no lo que se queda.'},
                                           {'id': 'b',
                                            'texto': 'Todos los vectores que $A$ manda al cero; si contiene '
                                                     'algo más que el $0$, una dirección entera se aplasta a '
                                                     'un punto y $\\det A = 0$.',
                                            'correcta': True,
                                            'explicacion': 'Es la definición y su hecho geométrico: el cero '
                                                           'siempre va al cero, y si otra cosa también va al '
                                                           'cero el plano cae sobre una recta, las filas son '
                                                           'colineales y no hay inversa.'},
                                           {'id': 'c',
                                            'texto': 'La recta sobre la que cae todo el plano cuando $\\det '
                                                     'A = 0$, la de la columna de $A$.',
                                            'correcta': False,
                                            'explicacion': 'Esa recta es la **imagen** (lo que sale), no el '
                                                           'núcleo (lo que entra y se pierde). En '
                                                           '$\\begin{pmatrix} 1 & 2 \\\\ 2 & 4 '
                                                           '\\end{pmatrix}$ la imagen es la recta de $(1, '
                                                           '2)$ y el núcleo la de $(2, -1)$.'},
                                           {'id': 'd',
                                            'texto': 'Sólo el vector $0$, en toda transformación lineal, '
                                                     'porque el cero siempre va al cero.',
                                            'correcta': False,
                                            'explicacion': 'El cero siempre está en el núcleo, pero no '
                                                           'siempre está solo: en una proyección o en '
                                                           'cualquier matriz con $\\det A = 0$ hay una recta '
                                                           'entera que va al cero.'}],
                              'rubrica': 'Productos, determinante y autovectores · medio: el núcleo es lo '
                                         'que va al cero; el cero siempre va al cero. Hecho geométrico: una '
                                         'transformación con núcleo aplasta una dirección entera a un punto'},
                             {'id': '07b_e2',
                              'nivel': 'elemental',
                              'enunciado': 'Decimos que $v \\neq 0$ es un **autovector** de $A$ con '
                                           'autovalor $\\lambda$. ¿Qué le pasa a $v$ al aplicar $A$?',
                              'opciones': [{'id': 'a',
                                            'texto': 'No cambia de largo: $\\lvert Av \\rvert = \\lvert v '
                                                     '\\rvert$, aunque pueda girar.',
                                            'correcta': False,
                                            'explicacion': 'Conservar el largo es lo que hace una rotación, '
                                                           'que justamente no tiene autovectores reales. Un '
                                                           'autovector puede cambiar de largo (se multiplica '
                                                           'por $\\lambda$); lo que no cambia es su recta.'},
                                           {'id': 'b',
                                            'texto': 'Gira el mismo ángulo que giran todos los vectores del '
                                                     'plano.',
                                            'correcta': False,
                                            'explicacion': 'Al revés: un autovector es la dirección que **no '
                                                           'gira**. Si todos los vectores giran el mismo '
                                                           'ángulo no nulo, como en un giro, no hay ningún '
                                                           'autovector real.'},
                                           {'id': 'c',
                                            'texto': 'Cae sobre su propia recta: $Av = \\lambda v$, sólo se '
                                                     'estira por $\\lambda$ (si $\\lambda < 0$ se invierte; '
                                                     'si $\\lambda = 0$ va al cero).',
                                            'correcta': True,
                                            'explicacion': 'Es la definición con su hecho geométrico: una '
                                                           'dirección que la transformación no gira. '
                                                           '$\\lambda = 1$ la deja quieta, $-1$ la da '
                                                           'vuelta, $0$ la aplasta: ahí el autovector está '
                                                           'en el núcleo.'},
                                           {'id': 'd',
                                            'texto': 'Coincide con una fila de $A$, porque las filas son las '
                                                     'direcciones propias.',
                                            'correcta': False,
                                            'explicacion': 'Las filas no son autovectores; son las reglas '
                                                           'que miden. El autovector es la **perpendicular** '
                                                           'a una fila de $A - \\lambda I$ (en $\\mathbb '
                                                           'R^3$, la cruz de dos filas), que es otra cosa.'}],
                              'rubrica': 'Productos, determinante y autovectores · elemental: un autovector '
                                         'cumple Av = λv. Hecho geométrico: una dirección que cae sobre sí '
                                         'misma, sólo se estira o se invierte'},
                             {'id': '07b_m1',
                              'nivel': 'medio',
                              'enunciado': 'Tomamos $B = \\begin{pmatrix} 3 & 1 \\\\ 0 & 2 \\end{pmatrix}$ y '
                                           'buscamos sus autovalores con el detector $\\det(B - \\lambda I) '
                                           '= 0$. ¿Qué obtenemos?',
                              'opciones': [{'id': 'a',
                                            'texto': '$\\lambda = 3$ y $\\lambda = 2$, con autovectores $e_1 '
                                                     '= (1, 0)$ y $e_2 = (0, 1)$, los ejes.',
                                            'correcta': False,
                                            'explicacion': 'Los autovalores están bien, pero $e_2$ no es '
                                                           'autovector: $B e_2 = (1, 2)$, que no es múltiplo '
                                                           'de $(0, 1)$. El de $\\lambda = 2$ es la '
                                                           'perpendicular a la fila $(1, 1)$ de $B - 2I$: '
                                                           '$(1, -1)$.'},
                                           {'id': 'b',
                                            'texto': '$\\lambda = 3$ y $\\lambda = 2$: en una triangular '
                                                     '$\\det(B - \\lambda I) = (3 - \\lambda)(2 - \\lambda)$ '
                                                     'y los autovalores son la diagonal.',
                                            'correcta': True,
                                            'explicacion': 'Con un cero debajo de la diagonal el '
                                                           'determinante es el producto de la diagonal, así '
                                                           'que las raíces se leen directo. Los autovectores '
                                                           'salen después: $(1, 0)$ para $3$ y $(1, -1)$ '
                                                           'para $2$, que no son perpendiculares.'},
                                           {'id': 'c',
                                            'texto': '$\\lambda = 3$ y $\\lambda = 1$: los números de la '
                                                     'primera fila.',
                                            'correcta': False,
                                            'explicacion': 'La primera fila es $(3, 1)$, pero el $1$ está '
                                                           'fuera de la diagonal y no entra en $\\det(B - '
                                                           '\\lambda I) = (3 - \\lambda)(2 - \\lambda) - 1 '
                                                           '\\cdot 0$. Los autovalores de una triangular son '
                                                           'los de la **diagonal**.'},
                                           {'id': 'd',
                                            'texto': 'Ninguno real: como $B$ no es simétrica, las raíces '
                                                     'salen complejas.',
                                            'correcta': False,
                                            'explicacion': 'No ser simétrica sólo quita la perpendicularidad '
                                                           'entre autovectores, no su existencia. Las raíces '
                                                           'complejas aparecen con un giro escondido, y $(3 '
                                                           '- \\lambda)(2 - \\lambda)$ tiene dos raíces '
                                                           'reales a la vista.'}],
                              'rubrica': 'Productos, determinante y autovectores · medio: Av = λv ⟺ (A − '
                                         'λI)v = 0 ⟺ det(A − λI) = 0'},
                             {'id': '07b_m2',
                              'nivel': 'medio',
                              'enunciado': 'Comprobamos que $N = \\begin{pmatrix} 1 & 2 \\\\ 2 & 4 '
                                           '\\end{pmatrix}$ tiene $\\det N = 0$ y queremos un vector no nulo '
                                           'de su núcleo. ¿Cuál sirve?',
                              'opciones': [{'id': 'a',
                                            'texto': '$(1, 2)$, la primera columna de $N$.',
                                            'correcta': False,
                                            'explicacion': '$(1, 2)$ genera la **imagen**: todo el plano cae '
                                                           'sobre esa recta. Pero $N(1, 2) = (5, 10) \\neq '
                                                           '0$: no está en el núcleo. Núcleo e imagen son '
                                                           'rectas distintas.'},
                                           {'id': 'b',
                                            'texto': '$(1, -2)$, que cambia el signo de una coordenada de la '
                                                     'fila.',
                                            'correcta': False,
                                            'explicacion': 'La perpendicular a $(a, b)$ es $(b, -a)$, con '
                                                           'las coordenadas **intercambiadas**, no sólo un '
                                                           'signo cambiado. Control: $(1, 2) \\cdot (1, -2) '
                                                           '= -3 \\neq 0$, así que $N(1, -2) \\neq 0$.'},
                                           {'id': 'c',
                                            'texto': '$(2, -1)$, la perpendicular a la fila $(1, 2)$.',
                                            'correcta': True,
                                            'explicacion': '$Nv = 0$ pide que cada fila por $v$ dé cero: '
                                                           '$v_1 + 2v_2 = 0$. La perpendicular $(b, -a)$ a '
                                                           'la fila $(a, b) = (1, 2)$ es $(2, -1)$, y $N(2, '
                                                           '-1) = (2 - 2, 4 - 4) = (0, 0)$.'},
                                           {'id': 'd',
                                            'texto': '$(0, 0)$, que cumple $N(0, 0) = (0, 0)$.',
                                            'correcta': False,
                                            'explicacion': 'El cero está en todo núcleo y no dice nada. Lo '
                                                           'que buscamos es el **otro** vector, el que '
                                                           'muestra que una dirección entera se aplasta: '
                                                           'justamente eso que $\\det N = 0$ anuncia.'}],
                              'rubrica': 'Productos, determinante y autovectores · medio: el autovector sale '
                                         'del producto cruz de dos filas (en R², la perpendicular a una '
                                         'fila). Hecho geométrico: el punto común de las rectas de nivel '
                                         'cero de las filas'},
                             {'id': '07b_a1',
                              'nivel': 'avanzado',
                              'enunciado': 'Buscamos las direcciones propias del giro $R(30°) = '
                                           '\\begin{pmatrix} \\cos 30° & -\\sin 30° \\\\ \\sin 30° & \\cos '
                                           '30° \\end{pmatrix}$ y no encontramos ninguna real. ¿Por qué?',
                              'opciones': [{'id': 'a',
                                            'texto': 'Porque $\\det R = 1$: una matriz de determinante $1$ '
                                                     'no cambia nada y por eso no tiene direcciones que '
                                                     'estirar.',
                                            'correcta': False,
                                            'explicacion': '$\\det = 1$ sólo dice que conserva áreas '
                                                           'orientadas. La cizalla $\\begin{pmatrix} 1 & 1 '
                                                           '\\\\ 0 & 1 \\end{pmatrix}$ también tiene $\\det '
                                                           '= 1$ y sí tiene un autovector real, $(1, 0)$.'},
                                           {'id': 'b',
                                            'texto': 'Porque $\\det(R - \\lambda I) = \\lambda^2 - 2\\cos '
                                                     '30°\\,\\lambda + 1$ tiene discriminante $4\\cos^2 30° '
                                                     '- 4 < 0$: raíces complejas, ninguna dirección real '
                                                     'queda sobre su recta.',
                                            'correcta': True,
                                            'explicacion': 'El detector es un polinomio real de grado $2$ y '
                                                           'puede no tener raíces reales. Para un giro de $0 '
                                                           '< \\theta < 180°$ nunca las tiene: todo gira el '
                                                           'mismo ángulo y ninguna recta cae sobre sí '
                                                           'misma.'},
                                           {'id': 'c',
                                            'texto': 'Porque $R$ no es simétrica, y sólo las matrices '
                                                     'simétricas tienen autovectores reales.',
                                            'correcta': False,
                                            'explicacion': 'La simetría garantiza autovectores reales **y '
                                                           'perpendiculares**, pero no es necesaria: '
                                                           '$\\begin{pmatrix} 3 & 1 \\\\ 0 & 2 '
                                                           '\\end{pmatrix}$ no es simétrica y tiene dos '
                                                           'direcciones propias reales.'},
                                           {'id': 'd',
                                            'texto': 'Sí tiene una: el eje del giro, con autovalor $1$, como '
                                                     'toda rotación.',
                                            'correcta': False,
                                            'explicacion': 'El eje existe en $\\mathbb R^3$, donde el '
                                                           'polinomio es de grado $3$ y siempre tiene una '
                                                           'raíz real. En $\\mathbb R^2$ el eje sería '
                                                           'perpendicular al plano y no está en él: el giro '
                                                           'plano no deja ninguna dirección del plano '
                                                           'quieta.'}],
                              'rubrica': 'Productos, determinante y autovectores · avanzado: autovalores '
                                         'complejos (una rotación escondida): qué figura corresponde a cada '
                                         'caso'},
                             {'id': '07b_a2',
                              'nivel': 'avanzado',
                              'enunciado': 'Comparamos la cizalla $C = \\begin{pmatrix} 1 & 1 \\\\ 0 & 1 '
                                           '\\end{pmatrix}$ con la homotecia $2I$. Las dos tienen un '
                                           'autovalor doble ($\\lambda = 1$ y $\\lambda = 2$). ¿Qué pasa con '
                                           'el núcleo de $A - \\lambda I$ en cada caso?',
                              'opciones': [{'id': 'a',
                                            'texto': 'En las dos es el plano entero: un autovalor doble '
                                                     'siempre da dos direcciones propias independientes.',
                                            'correcta': False,
                                            'explicacion': 'Vale para $2I$ pero no para la cizalla: $C - I = '
                                                           '\\begin{pmatrix} 0 & 1 \\\\ 0 & 0 '
                                                           '\\end{pmatrix}$ no es la matriz nula, su núcleo '
                                                           'es sólo la recta del eje $x$. Raíz doble no '
                                                           'garantiza dos direcciones.'},
                                           {'id': 'b',
                                            'texto': 'En la cizalla es la recta del eje $x$ (una sola '
                                                     'dirección propia); en $2I$ es el plano entero (ninguna '
                                                     'dirección gira).',
                                            'correcta': True,
                                            'explicacion': '$C - I$ tiene una fila no nula, $(0, 1)$, y su '
                                                           'perpendicular $(1, 0)$ es el único autovector: '
                                                           'todo lo demás se inclina hacia el eje $x$. $2I - '
                                                           '2I = 0$ aplasta todo: cada vector del plano es '
                                                           'propio.'},
                                           {'id': 'c',
                                            'texto': 'En la cizalla no hay ninguno, porque inclina todas las '
                                                     'direcciones; en $2I$ hay exactamente dos, los ejes.',
                                            'correcta': False,
                                            'explicacion': 'La cizalla deja quieto el eje $x$: $C(1, 0) = '
                                                           '(1, 0)$. Y $2I$ no privilegia a los ejes: estira '
                                                           'igual cualquier dirección, así que todas son '
                                                           'propias, no sólo dos.'},
                                           {'id': 'd',
                                            'texto': 'En las dos es una sola recta: con $\\det = 1$ y $\\det '
                                                     '= 4$ no hay núcleo, así que a lo sumo queda una '
                                                     'dirección.',
                                            'correcta': False,
                                            'explicacion': 'Mezcla el núcleo de $A$ con el de $A - \\lambda '
                                                           'I$. Que $\\det A \\neq 0$ sólo dice que '
                                                           '$\\lambda = 0$ no es autovalor; para $\\lambda = '
                                                           '2$, $2I - 2I$ tiene determinante cero y su '
                                                           'núcleo es todo el plano.'}],
                              'rubrica': 'Productos, determinante y autovectores · avanzado: autovalor doble '
                                         '(todo un plano de autovectores), núcleo previo, autovalores '
                                         'complejos: qué figura corresponde a cada caso'}],
 '07c_autovalores_3d_puntos_fijos': [{'id': '07c_e1',
                                      'nivel': 'elemental',
                                      'enunciado': 'Componemos dos giros de la estación total y obtenemos '
                                                   'una rotación $R$ de $\\mathbb R^3$. ¿Cómo reconocemos su '
                                                   'eje en el lenguaje de los autovectores?',
                                      'opciones': [{'id': 'a',
                                                    'texto': 'Es el autovector de autovalor $1$: la única '
                                                             'recta que $R$ deja quieta, $Rv = v$.',
                                                    'correcta': True,
                                                    'explicacion': 'Girar alrededor de un eje es dejarlo '
                                                                   'fijo punto a punto: $Rv = v$ es $Av = '
                                                                   '\\lambda v$ con $\\lambda = 1$. Una '
                                                                   'rotación tiene ese único autovalor real; '
                                                                   'los otros dos son complejos y describen '
                                                                   'el giro en el plano perpendicular.'},
                                                   {'id': 'b',
                                                    'texto': 'Es el autovector de autovalor $0$: la '
                                                             'dirección que la rotación aplasta.',
                                                    'correcta': False,
                                                    'explicacion': 'Una rotación no aplasta nada: $\\det R = '
                                                                   '1$, el núcleo es trivial y $0$ no es '
                                                                   'autovalor. El eje no desaparece, queda '
                                                                   'quieto.'},
                                                   {'id': 'c',
                                                    'texto': 'Es el eje del último giro que aplicamos, '
                                                             'porque es el que actúa al final.',
                                                    'correcta': False,
                                                    'explicacion': 'El último giro deja quieto su eje, pero '
                                                                   'el primero ya lo había movido: '
                                                                   '$R_z(90°)R_y(90°)$ manda $e_z$ a $e_y$. '
                                                                   'El eje de la composición es otro, la '
                                                                   'diagonal $(-1, 1, 1)$.'},
                                                   {'id': 'd',
                                                    'texto': 'Es la primera columna de $R$, a dónde va '
                                                             '$e_x$.',
                                                    'correcta': False,
                                                    'explicacion': 'La columna dice a dónde va el eje $x$, y '
                                                                   'en general $e_x$ no es el eje de giro. '
                                                                   'El eje sale de $R - I$: la cruz de dos '
                                                                   'de sus filas.'}],
                                      'rubrica': 'Productos, determinante y autovectores · elemental: el eje '
                                                 'de una rotación 3D es el autovector de autovalor 1'},
                                     {'id': '07c_e2',
                                      'nivel': 'elemental',
                                      'enunciado': 'En el plano vimos giros sin ninguna dirección propia '
                                                   'real. En $\\mathbb R^3$, ¿puede pasar lo mismo con una '
                                                   'matriz $3\\times3$ cualquiera?',
                                      'opciones': [{'id': 'a',
                                                    'texto': 'Sí: si la matriz gira, las tres raíces de '
                                                             '$\\det(A - \\lambda I)$ son complejas y no '
                                                             'queda ninguna recta invariante.',
                                                    'correcta': False,
                                                    'explicacion': 'Las raíces complejas de un polinomio '
                                                                   'real vienen de a pares conjugados. Con '
                                                                   'grado $3$ sobran dos para un par: la '
                                                                   'tercera es real, aunque haya giro en '
                                                                   'algún plano.'},
                                                   {'id': 'b',
                                                    'texto': 'No: $\\det(A - \\lambda I)$ es de grado $3$, '
                                                             'impar, y un polinomio real de grado impar '
                                                             'siempre tiene una raíz real; esa raíz da una '
                                                             'recta que cae sobre sí misma.',
                                                    'correcta': True,
                                                    'explicacion': 'Tres raíces reales, o una real y dos '
                                                                   'complejas conjugadas: siempre hay al '
                                                                   'menos una real, con autovector real. '
                                                                   'Para una rotación esa raíz es $1$ y la '
                                                                   'recta es el eje (Euler).'},
                                                   {'id': 'c',
                                                    'texto': 'No, pero sólo para matrices simétricas; una '
                                                             '$3\\times3$ general puede no tener autovector '
                                                             'real.',
                                                    'correcta': False,
                                                    'explicacion': 'La simetría garantiza **tres** '
                                                                   'autovalores reales. Pero al menos uno '
                                                                   'real lo garantiza el grado impar, sin '
                                                                   'pedir simetría: en $\\mathbb R^3$ no hay '
                                                                   'excepción.'},
                                                   {'id': 'd',
                                                    'texto': 'Sí, salvo que $\\det A \\neq 0$; con '
                                                             'determinante no nulo siempre aparece un '
                                                             'autovector.',
                                                    'correcta': False,
                                                    'explicacion': 'El determinante decide si $\\lambda = 0$ '
                                                                   'es autovalor, nada más. Que exista '
                                                                   'alguna raíz real en $\\mathbb R^3$ es '
                                                                   'cuestión del grado del polinomio, no del '
                                                                   'valor de $\\det A$.'}],
                                      'rubrica': 'Transformaciones proyectivas · medio: los puntos fijos son '
                                                 'los autovectores de H y siempre hay al menos uno real. '
                                                 'Hecho geométrico: toda homografía deja quieto algún punto, '
                                                 'propio o ideal'},
                                     {'id': '07c_m1',
                                      'nivel': 'medio',
                                      'enunciado': 'Para $R = R_z(90°)\\,R_y(90°)$ calculamos $R - I$ y sus '
                                                   'filas son $(-1, -1, 0)$, $(0, -1, 1)$ y $(-1, 0, -1)$. '
                                                   'Con la cruz de dos filas, ¿cuál es el eje de $R$?',
                                      'opciones': [{'id': 'a',
                                                    'texto': '$(0, 0, 1)$: el eje $z$, el del giro que '
                                                             'aplicamos último.',
                                                    'correcta': False,
                                                    'explicacion': '$R\\,e_z = e_y$: el eje $z$ se mueve. El '
                                                                   'giro en $y$ ya lo había llevado a $e_x$ '
                                                                   'antes de que $R_z$ actuara. La cuenta '
                                                                   'con las filas de $R - I$ no da $(0, 0, '
                                                                   '1)$.'},
                                                   {'id': 'b',
                                                    'texto': '$(1, 1, 1)$: la diagonal principal del cubo.',
                                                    'correcta': False,
                                                    'explicacion': 'Control: $R(1, 1, 1) = (-1, 1, -1) \\neq '
                                                                   '(1, 1, 1)$. La cruz $(-1, -1, 0) \\times '
                                                                   '(0, -1, 1)$ da $(-1, 1, 1)$: la primera '
                                                                   'componente es $(-1)(1) - 0 \\cdot (-1) = '
                                                                   '-1$, no $1$.'},
                                                   {'id': 'c',
                                                    'texto': '$(-1, 1, 1)$: la cruz de las dos primeras '
                                                             'filas, y $R(-1, 1, 1) = (-1, 1, 1)$.',
                                                    'correcta': True,
                                                    'explicacion': '$(-1, -1, 0) \\times (0, -1, 1) = '
                                                                   '\\big((-1)(1) - 0(-1),\\ 0 \\cdot 0 - '
                                                                   '(-1)(1),\\ (-1)(-1) - (-1)(0)\\big) = '
                                                                   '(-1, 1, 1)$, perpendicular a las tres '
                                                                   'filas. Las filas 2 y 3 dan $(1, -1, '
                                                                   '-1)$: la misma recta.'},
                                                   {'id': 'd',
                                                    'texto': '$(0, 1, 0)$: el eje $y$, el del primer giro, '
                                                             'que el segundo respeta.',
                                                    'correcta': False,
                                                    'explicacion': 'El segundo giro no lo respeta: '
                                                                   '$R_z(90°)$ manda $e_y$ a $-e_x$, así que '
                                                                   '$R\\,e_y = (-1, 0, 0)$. El eje de la '
                                                                   'composición no está en ningún plano '
                                                                   'coordenado.'}],
                                      'rubrica': 'Productos, determinante y autovectores · medio: el '
                                                 'autovector sale del producto cruz de dos filas. Hecho '
                                                 'geométrico: es el punto común de las rectas de nivel cero '
                                                 'de las filas'},
                                     {'id': '07c_m2',
                                      'nivel': 'medio',
                                      'enunciado': 'Una homografía $H$ del plano, en coordenadas homogéneas, '
                                                   'tiene el autovector $v = (2, 4, 2)$ con $Hv = 3v$. ¿Qué '
                                                   'punto fijo del plano $z = 1$ nos da?',
                                      'opciones': [{'id': 'a',
                                                    'texto': 'El punto $(2, 4)$: las dos primeras '
                                                             'coordenadas del autovector.',
                                                    'correcta': False,
                                                    'explicacion': 'Falta dividir por la tercera coordenada. '
                                                                   '$(2, 4, 2)$ es el rayo que pincha $z = '
                                                                   '1$ en $(2/2, 4/2) = (1, 2)$; el punto '
                                                                   '$(2, 4)$ es el rayo $(2, 4, 1)$, otro '
                                                                   'distinto.'},
                                                   {'id': 'b',
                                                    'texto': 'Ninguno: como $\\lambda = 3 \\neq 1$, $H$ '
                                                             'mueve a $v$ y el punto no queda fijo.',
                                                    'correcta': False,
                                                    'explicacion': 'En homogéneas $v$ y $3v$ son el '
                                                                   '**mismo** punto: el rayo es el mismo. '
                                                                   'Toda recta invariante de $\\mathbb R^3$, '
                                                                   'con cualquier $\\lambda \\neq 0$, pincha '
                                                                   '$z = 1$ en un punto fijo.'},
                                                   {'id': 'c',
                                                    'texto': 'El punto $(1, 2)$: la recta de $v$ pincha el '
                                                             'plano $z = 1$ en $(v_1/v_3, v_2/v_3)$, y '
                                                             '$\\lambda = 3$ no importa.',
                                                    'correcta': True,
                                                    'explicacion': '$Hv = 3v$ dice que la recta de $v$ es '
                                                                   'invariante; normalizando, $(2, 4, 2) '
                                                                   '\\sim (1, 2, 1)$, y $H(1, 2, 1) \\sim '
                                                                   '(1, 2, 1)$: el punto $(1, 2)$ vuelve '
                                                                   'sobre sí mismo. Los puntos fijos de la '
                                                                   'proyectiva son los subespacios '
                                                                   'invariantes de $\\mathbb R^3$.'},
                                                   {'id': 'd',
                                                    'texto': 'Un punto impropio en la dirección $(2, 4)$, '
                                                             'porque los autovectores dan direcciones fijas, '
                                                             'no puntos.',
                                                    'correcta': False,
                                                    'explicacion': 'Un autovector da un punto impropio sólo '
                                                                   'si $v_3 = 0$ (recta paralela al plano $z '
                                                                   '= 1$). Acá $v_3 = 2 \\neq 0$: la recta '
                                                                   'pincha el plano y el punto fijo es '
                                                                   'propio.'}],
                                      'rubrica': 'Afinidades y coordenadas homogéneas · avanzado: los puntos '
                                                 'fijos del plano son los autovectores de la matriz 3×3; un '
                                                 'autovector con tercera coordenada nula es una dirección '
                                                 'conservada (punto ideal fijo)'},
                                     {'id': '07c_a1',
                                      'nivel': 'avanzado',
                                      'enunciado': 'Escribimos el giro de $72°$ alrededor del centro $c = '
                                                   '(2, 1)$ como $H = \\begin{pmatrix} R & t \\\\ 0 & 1 '
                                                   '\\end{pmatrix}$, con $R = R(72°)$. ¿Cuántos puntos fijos '
                                                   'propios tiene, y por qué?',
                                      'opciones': [{'id': 'a',
                                                    'texto': 'Tres, uno por cada raíz de $\\det(H - \\lambda '
                                                             'I)$, que es de grado $3$.',
                                                    'correcta': False,
                                                    'explicacion': 'Grado $3$ da tres raíces, pero no tres '
                                                                   'reales. $\\det(H - \\lambda I) = (1 - '
                                                                   '\\lambda)\\det(R - \\lambda I)$ y el '
                                                                   'factor de $R$ aporta $e^{\\pm i\\,72°}$, '
                                                                   'complejos: sin autovector real, sin '
                                                                   'punto fijo.'},
                                                   {'id': 'b',
                                                    'texto': 'Uno solo, el centro: $\\det(H - \\lambda I) = '
                                                             '(1 - \\lambda)\\det(R - \\lambda I)$, $R$ '
                                                             'aporta dos raíces complejas y queda $\\lambda '
                                                             '= 1$ con autovector $(c, 1)$.',
                                                    'correcta': True,
                                                    'explicacion': 'La última fila $(0, 0, 1)$ factoriza el '
                                                                   'polinomio. El bloque $R$ no tiene raíces '
                                                                   'reales (lección 07b), así que el único '
                                                                   'autovalor real es $1$, y $Hc = c$ dice '
                                                                   'que su autovector es $(2, 1, 1)$: el '
                                                                   'centro, propio.'},
                                                   {'id': 'c',
                                                    'texto': 'Ninguno: un giro no deja nada quieto, como '
                                                             'vimos en el plano con $R(30°)$.',
                                                    'correcta': False,
                                                    'explicacion': '$R(30°)$ como matriz $2\\times2$ no deja '
                                                                   'ninguna **dirección** quieta, pero el '
                                                                   'giro alrededor de $c$ deja quieto al '
                                                                   '**punto** $c$. En homogéneas ese punto '
                                                                   'aparece como el autovector de $\\lambda '
                                                                   '= 1$ de la $3\\times3$.'},
                                                   {'id': 'd',
                                                    'texto': 'Una recta entera de puntos fijos, porque '
                                                             '$\\lambda = 1$ es raíz doble (una de $R$ y '
                                                             'otra de la última fila).',
                                                    'correcta': False,
                                                    'explicacion': '$\\lambda = 1$ no es raíz de $\\det(R - '
                                                                   '\\lambda I) = \\lambda^2 - 2\\cos '
                                                                   '72°\\,\\lambda + 1$, así que es simple. '
                                                                   'Una recta de puntos fijos aparece con '
                                                                   'raíz doble y cruces nulas, como en la '
                                                                   'homología del pentágono, no acá.'}],
                                      'rubrica': 'Productos, determinante y autovectores · medio: los puntos '
                                                 'fijos de una afinidad o de una proyectiva son subespacios '
                                                 'invariantes en R³'},
                                     {'id': '07c_a2',
                                      'nivel': 'avanzado',
                                      'enunciado': 'La homografía $H_c$ del pentágono tiene autovalores $2, '
                                                   '2, -2$. Las tres filas de $H_c - 2I$ son múltiplos de '
                                                   '$(0, -1, 2)$, y el autovector de $-2$ es $(4, 6, 1)$. '
                                                   '¿Qué puntos fijos tiene en el plano?',
                                      'opciones': [{'id': 'a',
                                                    'texto': 'Sólo el centro $(4, 6)$: los autovectores de '
                                                             '$\\lambda = 2$ no cuentan porque $2 \\neq 1$ '
                                                             'los mueve.',
                                                    'correcta': False,
                                                    'explicacion': 'En homogéneas $v$ y $2v$ son el mismo '
                                                                   'punto; cualquier $\\lambda \\neq 0$ da '
                                                                   'puntos fijos. Y $(4, 6)$ tampoco se '
                                                                   'salva con ese criterio: su $\\lambda$ es '
                                                                   '$-2$.'},
                                                   {'id': 'b',
                                                    'texto': 'Dos puntos aislados sobre la recta $y = 2$, '
                                                             'uno por cada raíz $2$, más el centro $(4, 6)$.',
                                                    'correcta': False,
                                                    'explicacion': 'Raíz doble con todas las cruces nulas no '
                                                                   'da dos autovectores sueltos: da un '
                                                                   '**plano** entero de autovectores en '
                                                                   '$\\mathbb R^3$, que corta $z = 1$ en una '
                                                                   'recta entera de puntos fijos, no en dos '
                                                                   'puntos.'},
                                                   {'id': 'c',
                                                    'texto': 'Toda la recta $y = 2$ (el plano $-y + 2z = 0$ '
                                                             'de autovectores de $\\lambda = 2$ cortado con '
                                                             '$z = 1$) y, aparte, el centro $(4, 6)$: una '
                                                             'homología.',
                                                    'correcta': True,
                                                    'explicacion': 'Filas colineales en $H_c - 2I$ '
                                                                   'significan núcleo de dimensión $2$: el '
                                                                   'plano $-y + 2z = 0$, que en $z = 1$ es '
                                                                   '$y = 2$, con $B$ y $D$ del pentágono '
                                                                   'quietos. El autovector $(4, 6, 1)$ de '
                                                                   '$\\lambda = -2$ pincha en el centro. Eje '
                                                                   'más centro: la foto en perspectiva de '
                                                                   'una reflexión.'},
                                                   {'id': 'd',
                                                    'texto': 'Ninguno real: ningún autovalor vale $1$, así '
                                                             'que $H_c$ no deja nada quieto.',
                                                    'correcta': False,
                                                    'explicacion': 'El $\\lambda = 1$ importa para '
                                                                   'afinidades vistas como $Ax + t = x$, '
                                                                   'pero en homogéneas basta cualquier recta '
                                                                   'invariante: $Hv = \\lambda v$ con '
                                                                   '$\\lambda \\neq 0$ es un punto fijo. Acá '
                                                                   'hay una recta entera más un punto.'}],
                                      'rubrica': 'Transformaciones proyectivas · avanzado: reconocer la '
                                                 'homología y sus autovalores repetidos; rectas fijas y '
                                                 'puntos fijos de una homografía'}],
 '08_cambio_de_base': [{'id': '08_e1',
                        'nivel': 'elemental',
                        'enunciado': 'Medimos el mismo mojón con la grilla de la obra y con la grilla '
                                     'oblicua de la parcela. ¿Qué se conserva al cambiar de base y qué '
                                     'cambia?',
                        'opciones': [{'id': 'a',
                                      'texto': 'Se conservan los números del punto; lo que cambia es la '
                                               'figura, que gira hasta alinearse con los ejes nuevos.',
                                      'correcta': False,
                                      'explicacion': 'Es exactamente al revés: el mojón no se toca y la '
                                                     'figura no gira. Lo que cambia son los números con que '
                                                     'lo nombramos; una coordenada es un número **respecto '
                                                     'de unos ejes**.'},
                                     {'id': 'b',
                                      'texto': 'Se conserva el punto con toda su geometría (distancias, '
                                               'ángulos, incidencias); sólo cambian los números que lo '
                                               'describen.',
                                      'correcta': True,
                                      'explicacion': 'El hierro no se movió: convertimos todo para que nada '
                                                     'cambie. Las coordenadas son etiquetas que dependen de '
                                                     'la grilla; la geometría vive en el punto, no en la '
                                                     'etiqueta.'},
                                     {'id': 'c',
                                      'texto': 'Nada se conserva: cada base define su propia geometría y la '
                                               'canónica es la única verdadera.',
                                      'correcta': False,
                                      'explicacion': 'No hay base privilegiada a priori. La canónica sólo es '
                                                     'cómoda porque en ella el producto interno se calcula '
                                                     'como $x_1x_2 + y_1y_2$; la geometría es la misma en '
                                                     'cualquier grilla.'},
                                     {'id': 'd',
                                      'texto': 'Se conservan las coordenadas si los ejes nuevos son '
                                               'perpendiculares; si son oblicuos, el punto se desplaza.',
                                      'correcta': False,
                                      'explicacion': 'Con ejes perpendiculares de largo $1$ cambia la '
                                                     '**cuenta** (proyectar alcanza), no el hecho: los '
                                                     'números cambian igual. Y con ejes oblicuos el punto '
                                                     'tampoco se desplaza; sólo hay que resolver en vez de '
                                                     'proyectar.'}],
                        'rubrica': 'Cambio de base y SVD · avanzado: no hay base privilegiada a priori; lo '
                                   'único especial de la canónica es que en ella el producto interno se '
                                   'calcula como suma de productos. Hecho geométrico: sin distancias, todas '
                                   'las grillas valen lo mismo'},
                       {'id': '08_e2',
                        'nivel': 'elemental',
                        'enunciado': 'Armamos $B$ poniendo en sus columnas los ejes nuevos $b_1, b_2$ '
                                     'escritos en la grilla vieja. ¿Qué hace $B$ con un vector de '
                                     'coordenadas?',
                        'opciones': [{'id': 'a',
                                      'texto': 'Lleva coordenadas viejas a nuevas: $c = Bp$ es la lectura '
                                               'del punto $p$ en la grilla de la parcela.',
                                      'correcta': False,
                                      'explicacion': 'Es el error de la predicción: $Bp$ interpreta a $p$ '
                                                     'como cantidades de $b_1$ y $b_2$, y devuelve otro '
                                                     'punto. Para leer en la base nueva hay que **resolver** '
                                                     '$Bc = p$, o sea $c = B^{-1}p$.'},
                                     {'id': 'b',
                                      'texto': 'Lleva coordenadas nuevas a viejas: $p = Bc = c_1 b_1 + c_2 '
                                               'b_2$; para ir al revés hay que resolver, $c = B^{-1}p$.',
                                      'correcta': True,
                                      'explicacion': 'Multiplicar por $B$ es avanzar $c_1$ veces $b_1$ y '
                                                     '$c_2$ veces $b_2$, en metros de la obra. Las columnas '
                                                     'dicen a dónde van los ejes; leer coordenadas nuevas es '
                                                     'el problema inverso.'},
                                     {'id': 'c',
                                      'texto': 'Sólo es un cambio de base si $b_1 \\perp b_2$; con ejes '
                                               'oblicuos hay que usar $B^\\top$ en lugar de $B$.',
                                      'correcta': False,
                                      'explicacion': 'Cualquier par de direcciones no paralelas es base '
                                                     '($\\det B \\neq 0$). $B^\\top$ sólo coincide con '
                                                     '$B^{-1}$ si los ejes son perpendiculares y de largo '
                                                     '$1$, como en Rotaciones I; en general no sirve.'},
                                     {'id': 'd',
                                      'texto': 'Sus filas son los ejes nuevos y sus columnas los viejos; $B$ '
                                               'convierte en los dos sentidos según de qué lado se '
                                               'multiplique.',
                                      'correcta': False,
                                      'explicacion': 'Los ejes nuevos van en las **columnas**, y $B$ sólo '
                                                     'convierte de nuevas a viejas. Poner los ejes como '
                                                     'filas es usar $B^\\top$, que da otra matriz salvo que '
                                                     '$B$ sea simétrica.'}],
                        'rubrica': 'Cambio de base y SVD · elemental: un cambio de base expresa el mismo '
                                   'vector como combinación de otros vectores; la matriz tiene en sus '
                                   'columnas una base escrita en la otra'},
                       {'id': '08_m1',
                        'nivel': 'medio',
                        'enunciado': 'Tomamos los ejes nuevos $b_1 = (1, 1)$ y $b_2 = (1, -1)$ y el punto $p '
                                     '= (3, 4)$. ¿Cuáles son sus coordenadas $c$ en la base nueva?',
                        'opciones': [{'id': 'a',
                                      'texto': '$c = (7, -1)$, el resultado de $Bp$.',
                                      'correcta': False,
                                      'explicacion': '$Bp$ va de nuevas a viejas, no al revés. $(7, -1)$ son '
                                                     'las coordenadas en la obra del punto $7b_1 - 1b_2 = '
                                                     '(6, 8)$, que no es $p$. Falta el $\\tfrac12$ de '
                                                     '$B^{-1} = \\tfrac12 B$.'},
                                     {'id': 'b',
                                      'texto': '$c = (3.5, -0.5)$: resolviendo $c_1 + c_2 = 3$, $c_1 - c_2 = '
                                               '4$.',
                                      'correcta': True,
                                      'explicacion': '$Bc = p$ es ese sistema: sumando, $2c_1 = 7$; '
                                                     'restando, $2c_2 = -1$. Control: $3.5\\,(1, 1) - '
                                                     '0.5\\,(1, -1) = (3.5 - 0.5,\\ 3.5 + 0.5) = (3, 4)$.'},
                                     {'id': 'c',
                                      'texto': '$c = (3, 4)$: el punto no se movió, así que sus coordenadas '
                                               'tampoco.',
                                      'correcta': False,
                                      'explicacion': 'El punto no se mueve, pero las coordenadas son números '
                                                     'respecto de unos ejes. $(3, 4)$ en la base nueva sería '
                                                     '$3b_1 + 4b_2 = (7, -1)$, otro punto.'},
                                     {'id': 'd',
                                      'texto': '$c = (3.5, 0.5)$: la mitad de la suma y la mitad de la '
                                               'diferencia de las coordenadas.',
                                      'correcta': False,
                                      'explicacion': 'La segunda es $(3 - 4)/2 = -0.5$, con signo. Control: '
                                                     '$3.5\\,(1, 1) + 0.5\\,(1, -1) = (4, 3) \\neq (3, 4)$: '
                                                     'con el signo cambiado se cruzan las coordenadas.'}],
                        'rubrica': 'Cambio de base y SVD · elemental: un cambio de base expresa el mismo '
                                   'vector como combinación de otros vectores. Hecho geométrico: la misma '
                                   'flecha medida con otra grilla'},
                       {'id': '08_m2',
                        'nivel': 'medio',
                        'enunciado': 'Ponemos los autovectores $v_1, v_2$ de $A$ como columnas de $B$, de '
                                     'modo que $B$ traduce de la base propia a la canónica. ¿Qué producto '
                                     'nos devuelve la diagonal $\\Lambda$ de autovalores?',
                        'opciones': [{'id': 'a',
                                      'texto': '$B\\,A\\,B^{-1}$: primero $B^{-1}$ a la derecha para entrar, '
                                               'después $A$, después $B$ para salir.',
                                      'correcta': False,
                                      'explicacion': '$BAB^{-1}$ traduce a la base propia, aplica $A$ (que '
                                                     'espera coordenadas canónicas) y vuelve a canónica: '
                                                     'mezcla las bases y en general no es diagonal. Lo '
                                                     'correcto es $B^{-1}AB$: de propia a canónica con $B$, '
                                                     'transformar con $A$, y de canónica a propia con '
                                                     '$B^{-1}$.'},
                                     {'id': 'b',
                                      'texto': '$B^\\top A\\,B$: la transpuesta deshace a $B$, como en '
                                               'Rotaciones I.',
                                      'correcta': False,
                                      'explicacion': '$B^\\top = B^{-1}$ sólo si las columnas son '
                                                     'perpendiculares de largo $1$, lo que pasa cuando $A$ '
                                                     'es simétrica. Para $\\begin{pmatrix} 3 & 1 \\\\ 0 & 2 '
                                                     '\\end{pmatrix}$ los autovectores $(1, 0)$ y $(1, -1)$ '
                                                     'no lo son y $B^\\top AB$ no es diagonal.'},
                                     {'id': 'c',
                                      'texto': '$B^{-1} A\\,B$: la de la derecha actúa primero, lleva a la '
                                               'base propia; $A$ estira; $B^{-1}$ vuelve a leer en la base '
                                               'propia.',
                                      'correcta': True,
                                      'explicacion': 'Un vector escrito en la base propia pasa por $B$ a '
                                                     'canónica, $A$ lo transforma, y $B^{-1}$ lo lee de '
                                                     'vuelta en la base propia, donde cada eje sólo se '
                                                     'estiró por su $\\lambda$. Es el $T_{\\mathrm{diag}} = '
                                                     'A^{-1}T_{\\mathrm{can}}A$ del profesor, con su $A$ en '
                                                     'el lugar de nuestra $B$.'},
                                     {'id': 'd',
                                      'texto': '$A\\,B$: aplicar $A$ a cada autovector ya da $\\lambda_k '
                                               'v_k$, que es diagonal.',
                                      'correcta': False,
                                      'explicacion': '$AB = B\\Lambda$ tiene en sus columnas $\\lambda_k '
                                                     'v_k$: los autovectores estirados, escritos todavía en '
                                                     'canónica. Para que quede $\\Lambda$ falta leerlos en '
                                                     'la base propia, o sea multiplicar por $B^{-1}$ a la '
                                                     'izquierda.'}],
                        'rubrica': 'Cambio de base y SVD · medio: cambiar la base de la matriz de una '
                                   'transformación es componer con los dos cambios de base: M_av = C_{av←e} '
                                   'M C_{e←av}. Hecho geométrico: traducir, transformar, volver a traducir'},
                       {'id': '08_a1',
                        'nivel': 'avanzado',
                        'enunciado': 'Para $A = \\begin{pmatrix} 2 & 1 \\\\ 1 & 2 \\end{pmatrix}$ tenemos '
                                     '$\\lambda = 3, 1$, $B = \\begin{pmatrix} 1 & 1 \\\\ 1 & -1 '
                                     '\\end{pmatrix}$ y $B^{-1} = \\tfrac12 B$. Calculamos $A^5 = '
                                     'B\\Lambda^5 B^{-1}$ sin multiplicar cinco veces. ¿Cuánto da?',
                        'opciones': [{'id': 'a',
                                      'texto': '$\\begin{pmatrix} 243 & 0 \\\\ 0 & 1 \\end{pmatrix}$, porque '
                                               'en la base propia elevar es elevar los autovalores.',
                                      'correcta': False,
                                      'explicacion': 'Eso es $\\Lambda^5$, la transformación **leída en la '
                                                     'base propia**. $A^5$ pide volver a la canónica: '
                                                     '$B\\Lambda^5B^{-1}$. Sin ese regreso tenemos la misma '
                                                     'transformación en otros números.'},
                                     {'id': 'b',
                                      'texto': '$\\begin{pmatrix} 32 & 1 \\\\ 1 & 32 \\end{pmatrix}$, '
                                               'elevando cada entrada a la quinta.',
                                      'correcta': False,
                                      'explicacion': 'Es `A ** 5` de numpy, que eleva número por número; '
                                                     '$A^5$ es multiplicar matrices. Control rápido: $A^2 = '
                                                     '\\begin{pmatrix} 5 & 4 \\\\ 4 & 5 \\end{pmatrix}$, no '
                                                     '$\\begin{pmatrix} 4 & 1 \\\\ 1 & 4 \\end{pmatrix}$.'},
                                     {'id': 'c',
                                      'texto': '$\\begin{pmatrix} 244 & 242 \\\\ 242 & 244 \\end{pmatrix}$, '
                                               'el producto $B\\,\\mathrm{diag}(243, 1)\\,B$.',
                                      'correcta': False,
                                      'explicacion': 'Falta el $\\tfrac12$ de $B^{-1} = \\tfrac12 B$: se usó '
                                                     '$B$ en lugar de su inversa. Control: $\\det A^5 = 3^5 '
                                                     '= 243$, y $244^2 - 242^2 = 972 \\neq 243$.'},
                                     {'id': 'd',
                                      'texto': '$\\begin{pmatrix} 122 & 121 \\\\ 121 & 122 \\end{pmatrix}$: '
                                               '$\\tfrac12 \\begin{pmatrix} 243 + 1 & 243 - 1 \\\\ 243 - 1 & '
                                               '243 + 1 \\end{pmatrix}$.',
                                      'correcta': True,
                                      'explicacion': '$B\\Lambda^5 = \\begin{pmatrix} 243 & 1 \\\\ 243 & -1 '
                                                     '\\end{pmatrix}$ y, por $\\tfrac12 B$, queda '
                                                     '$\\tfrac12\\begin{pmatrix} 244 & 242 \\\\ 242 & 244 '
                                                     '\\end{pmatrix}$. Lectura: $e_1 = \\tfrac12 b_1 + '
                                                     '\\tfrac12 b_2$; la parte en $b_1$ se multiplica por '
                                                     '$243$ y la de $b_2$ queda; los $B^{-1}B$ del medio se '
                                                     'cancelan.'}],
                        'rubrica': 'Cambio de base y SVD · medio: la base de autovectores permite potencias '
                                   'enteras y reales de la matriz. Hecho geométrico: ver la transformación '
                                   'como un proceso continuo'},
                       {'id': '08_a2',
                        'nivel': 'avanzado',
                        'enunciado': 'Queremos una grilla real en la que la transformación sea sólo estirar '
                                     'cada eje. ¿Cuál de estas matrices se diagonaliza con una base real de '
                                     'autovectores?',
                        'opciones': [{'id': 'a',
                                      'texto': 'La cizalla $\\begin{pmatrix} 1 & 1 \\\\ 0 & 1 '
                                               '\\end{pmatrix}$: tiene $\\lambda = 1$ doble, dos autovalores '
                                               'reales.',
                                      'correcta': False,
                                      'explicacion': 'Dos raíces reales, pero una sola dirección propia: el '
                                                     'núcleo de $C - I$ es la recta del eje $x$. Sin segundo '
                                                     'eje propio no hay grilla en la que $C$ sólo estire; '
                                                     '$B^{-1}CB$ nunca es diagonal.'},
                                     {'id': 'b',
                                      'texto': 'El giro $R(30°)$: conserva largos y ángulos, así que en su '
                                               'propia grilla es la identidad.',
                                      'correcta': False,
                                      'explicacion': '$\\det(R - \\lambda I)$ no tiene raíces reales: '
                                                     'ninguna dirección cae sobre sí misma, y sin '
                                                     'autovectores reales no hay base propia. Lo que sí '
                                                     'tiene es SVD, con $\\Sigma = I$ y el giro en $U$.'},
                                     {'id': 'c',
                                      'texto': 'La triangular $\\begin{pmatrix} 3 & 1 \\\\ 0 & 2 '
                                               '\\end{pmatrix}$: $\\lambda = 3, 2$ distintos, con '
                                               'autovectores $(1, 0)$ y $(1, -1)$ independientes.',
                                      'correcta': True,
                                      'explicacion': 'Dos autovalores reales distintos dan dos direcciones '
                                                     'propias independientes, y eso basta: $B = '
                                                     '\\begin{pmatrix} 1 & 1 \\\\ 0 & -1 \\end{pmatrix}$ y '
                                                     '$B^{-1}AB = \\mathrm{diag}(3, 2)$. Que los ejes '
                                                     'propios no sean perpendiculares no molesta; sólo '
                                                     'impide usar $B^\\top$.'},
                                     {'id': 'd',
                                      'texto': 'Ninguna de las anteriores: para diagonalizar hace falta que '
                                               'la matriz sea simétrica.',
                                      'correcta': False,
                                      'explicacion': 'La simetría garantiza base propia **ortogonal**, pero '
                                                     'no es necesaria. La condición es tener tantos '
                                                     'autovectores reales independientes como dimensiones, y '
                                                     'la triangular los tiene.'}],
                        'rubrica': 'Cambio de base y SVD · avanzado: autovalores complejos: por qué la '
                                   'diagonalización real puede fallar (y elemental: si hay tantos '
                                   'autovectores independientes como dimensiones, en esa base la matriz es '
                                   'diagonal)'}],
 '09_cambio_de_base_svd': [{'id': '09_e1',
                            'nivel': 'elemental',
                            'enunciado': 'Escribimos $A = U\\Sigma V^\\top$ con $\\Sigma = '
                                         '\\mathrm{diag}(\\sigma_1, \\sigma_2)$. ¿Qué miden los valores '
                                         'singulares $\\sigma_1, \\sigma_2$?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Los autovalores de $A$ en valor absoluto, para cualquier '
                                                   'matriz $A$.',
                                          'correcta': False,
                                          'explicacion': 'En general no vale: sí para las simétricas y, más '
                                                         'en general, para las normales (como una rotación '
                                                         'por una escala), pero no para cualquier $A$. Para '
                                                         '$\\begin{pmatrix} 2 & 1 \\\\ 0 & 1 \\end{pmatrix}$ '
                                                         'los autovalores son $2, 1$ y los valores '
                                                         'singulares $2.288, 0.874$: dos preguntas distintas '
                                                         '(qué cae sobre sí mismo, qué par perpendicular '
                                                         'sigue perpendicular).'},
                                         {'id': 'b',
                                          'texto': 'Cuánto se estira cada una de las dos direcciones '
                                                   'perpendiculares $v_1, v_2$ que siguen perpendiculares a '
                                                   'la salida: los semiejes de la elipse imagen del círculo '
                                                   'unitario.',
                                          'correcta': True,
                                          'explicacion': '$Av_k = \\sigma_k u_k$ con $v_1 \\perp v_2$ y $u_1 '
                                                         '\\perp u_2$. El círculo unitario va a una elipse '
                                                         'de semiejes $\\sigma_1 u_1$ y $\\sigma_2 u_2$; los '
                                                         '$\\sigma$ son reales y no negativos siempre.'},
                                         {'id': 'c',
                                          'texto': 'Los ángulos de los dos giros $V^\\top$ y $U$ que '
                                                   'encierran al estiramiento.',
                                          'correcta': False,
                                          'explicacion': 'Los ángulos están en $U$ y $V$, matrices '
                                                         'ortogonales. $\\Sigma$ es la etapa del medio, el '
                                                         'estiramiento de cada eje: largos, no ángulos.'},
                                         {'id': 'd',
                                          'texto': 'Cuánto giran las direcciones propias de $A$ al pasar por '
                                                   'la transformación.',
                                          'correcta': False,
                                          'explicacion': 'Las direcciones propias no giran por definición. '
                                                         'La SVD no habla de direcciones propias sino de un '
                                                         'par perpendicular que sigue perpendicular, y mide '
                                                         'sus estiramientos.'}],
                            'rubrica': 'Cambio de base y SVD · elemental: existe una base ortogonal de la '
                                       'entrada que va a una base ortogonal de la salida. Hecho geométrico: '
                                       'la circunferencia unidad se transforma en una elipse y sus ejes son '
                                       'esa base'},
                           {'id': '09_e2',
                            'nivel': 'elemental',
                            'enunciado': 'Tomamos la diagonal $D = \\begin{pmatrix} 3 & 0 \\\\ 0 & -2 '
                                         '\\end{pmatrix}$. ¿Cuáles son sus valores singulares?',
                            'opciones': [{'id': 'a',
                                          'texto': '$\\sigma = 3$ y $-2$: la matriz ya es diagonal, así que '
                                                   '$\\Sigma = D$.',
                                          'correcta': False,
                                          'explicacion': '$3$ y $-2$ son los **autovalores**. Los valores '
                                                         'singulares nunca son negativos: el signo del $-2$ '
                                                         'se lo lleva $U = \\mathrm{diag}(1, -1)$, como $a = '
                                                         '(\\pm 1)\\lvert a \\rvert$ en $\\mathbb R$.'},
                                         {'id': 'b',
                                          'texto': '$\\sigma = 9$ y $4$: los autovalores de $D^\\top D$.',
                                          'correcta': False,
                                          'explicacion': '$9$ y $4$ son los $\\sigma^2$: los autovalores de '
                                                         '$D^\\top D = \\mathrm{diag}(9, 4)$. Falta la raíz: '
                                                         '$\\sigma_k = \\sqrt{\\mu_k}$.'},
                                         {'id': 'c',
                                          'texto': '$\\sigma = 3$ y $2$: los estiramientos, con el signo del '
                                                   '$-2$ en $U$.',
                                          'correcta': True,
                                          'explicacion': 'Los ejes van a los ejes, estirados $3$ y $2$ '
                                                         'veces; la reflexión del segundo eje es parte del '
                                                         'giro-o-reflexión de salida: $D = \\mathrm{diag}(1, '
                                                         '-1)\\,\\mathrm{diag}(3, 2)\\,I$. Control: '
                                                         '$\\sigma_1\\sigma_2 = 6 = \\lvert \\det D '
                                                         '\\rvert$.'},
                                         {'id': 'd',
                                          'texto': '$\\sigma = \\tfrac13$ y $\\tfrac12$: invertir una '
                                                   'diagonal es tomar recíprocos.',
                                          'correcta': False,
                                          'explicacion': 'Los recíprocos son los valores singulares de '
                                                         '$D^{-1}$, no de $D$. La SVD de $D$ describe cuánto '
                                                         'estira $D$; la inversa deshace esos estiramientos '
                                                         'con $1/\\sigma$.'}],
                            'rubrica': 'Cambio de base y SVD · medio: en la SVD las bases de entrada y '
                                       'salida son distintas, A = UΣVᵀ, y la diagonal nunca es compleja (ni '
                                       'negativa)'},
                           {'id': '09_m1',
                            'nivel': 'medio',
                            'enunciado': 'Con el recorte del DEM $Z$, de $512\\times512$ alturas, hacemos '
                                         '`U, s, Vt = np.linalg.svd(Z)` y armamos $Z_k$ = `U[:, :k] @ '
                                         'np.diag(s[:k]) @ Vt[:k]` con $k = 10$. ¿Qué es $Z_k$?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Una matriz de rango $512$ como $Z$, porque $U$ y '
                                                   '$V^\\top$ siguen siendo las matrices completas.',
                                          'correcta': False,
                                          'explicacion': 'Recortamos $10$ columnas de $U$, $10$ valores de '
                                                         '$s$ y $10$ filas de $V^\\top$: el producto es una '
                                                         'suma de $10$ términos $\\sigma_i u_i v_i^\\top$, '
                                                         'cada uno de rango $1$. El rango de $Z_k$ es $10$.'},
                                         {'id': 'b',
                                          'texto': 'La mejor aproximación de rango $10$ de $Z$: la suma '
                                                   '$\\sum_{i \\le 10} \\sigma_i u_i v_i^\\top$; el error '
                                                   'que queda lo gobiernan los $\\sigma_i$ descartados.',
                                          'correcta': True,
                                          'explicacion': 'Quedarse con los $k$ valores singulares más '
                                                         'grandes es la mejor aproximación de rango $k$ '
                                                         '(Eckart–Young); en el DEM, $\\sigma_1$ paga la '
                                                         'meseta y los siguientes el relieve, por eso el RMS '
                                                         'baja de $103$ m con $k = 1$ a $17$ m con $k = '
                                                         '10$.'},
                                         {'id': 'c',
                                          'texto': 'La pseudoinversa de $Z$ truncada: deshace las $10$ '
                                                   'direcciones principales y anula las demás.',
                                          'correcta': False,
                                          'explicacion': 'La pseudoinversa es $V\\Sigma^{+}U^\\top$, con '
                                                         '$1/\\sigma$ y los factores en el orden inverso. '
                                                         '$Z_k$ no invierte nada: reconstruye $Z$ con los '
                                                         'mismos $\\sigma$, no con sus recíprocos.'},
                                         {'id': 'd',
                                          'texto': '$Z$ con la altura media restada: el primer término se '
                                                   'lleva la meseta y $Z_k$ la elimina.',
                                          'correcta': False,
                                          'explicacion': '$Z_k$ no resta nada: el término $\\sigma_1 u_1 '
                                                         'v_1^\\top$ **es** la meseta y $Z_k$ lo incluye. '
                                                         'Restar la media antes de la SVD es otra operación '
                                                         '(la casilla de la lección), y cambia qué significa '
                                                         '$k = 1$.'}],
                            'rubrica': 'Cambio de base y SVD · medio: A = UΣVᵀ, rotar, estirar, rotar '
                                       '(aplicación: la aproximación de rango k; sin celda propia en la '
                                       'rúbrica)'},
                           {'id': '09_m2',
                            'nivel': 'medio',
                            'enunciado': 'Para $A = \\begin{pmatrix} 2 & 1 \\\\ 0 & 1 \\end{pmatrix}$ '
                                         'calculamos $A^\\top A = \\begin{pmatrix} 4 & 2 \\\\ 2 & 2 '
                                         '\\end{pmatrix}$. Sin resolver la cuadrática, ¿cuánto vale '
                                         '$\\sigma_1^2 + \\sigma_2^2$?',
                            'opciones': [{'id': 'a',
                                          'texto': '$3$: la traza de $A$, suma de sus autovalores $2 + 1$.',
                                          'correcta': False,
                                          'explicacion': 'La traza de $A$ suma los autovalores de $A$, que '
                                                         'no son los $\\sigma$. Los $\\sigma^2$ son los '
                                                         'autovalores de $A^\\top A$, y lo que se suma es la '
                                                         'traza de **esa** matriz.'},
                                         {'id': 'b',
                                          'texto': '$5$: los autovalores al cuadrado, $2^2 + 1^2$.',
                                          'correcta': False,
                                          'explicacion': '$\\sigma_k = \\lvert\\lambda_k\\rvert$ vale para '
                                                         'las matrices normales (por ejemplo las '
                                                         'simétricas), y ésta no lo es ($AA^\\top \\neq '
                                                         'A^\\top A$). Control: $\\sigma_1^2 + \\sigma_2^2 = '
                                                         '(3 + \\sqrt5) + (3 - \\sqrt5) = 6 \\neq 5$.'},
                                         {'id': 'c',
                                          'texto': '$6$: la traza de $A^\\top A$, que es la suma de los '
                                                   'cuadrados de todas las entradas de $A$.',
                                          'correcta': True,
                                          'explicacion': 'Los $\\sigma_k^2$ son los autovalores de $A^\\top '
                                                         'A$ y su suma es la traza, $4 + 2 = 6$; también '
                                                         '$2^2 + 1^2 + 0^2 + 1^2$. Con $\\sigma_1\\sigma_2 = '
                                                         '\\lvert\\det A\\rvert = 2$ queda $\\mu^2 - 6\\mu + '
                                                         '4 = 0$, $\\sigma = 2.288, 0.874$.'},
                                         {'id': 'd',
                                          'texto': '$2$: el determinante de $A$, igual a '
                                                   '$\\sigma_1\\sigma_2$.',
                                          'correcta': False,
                                          'explicacion': '$\\sigma_1\\sigma_2 = \\lvert\\det A\\rvert = 2$ '
                                                         'es el **producto**, no la suma de cuadrados. El '
                                                         'producto $\\sigma_1\\sigma_2$ es el área de la '
                                                         'elipse dividida por $\\pi$; la suma de cuadrados, '
                                                         'la traza de $A^\\top A$.'}],
                            'rubrica': 'Cambio de base y SVD · medio: en la SVD las bases de entrada y '
                                       'salida son distintas, A = UΣVᵀ (construcción de σ a partir de AᵀA)'},
                           {'id': '09_a1',
                            'nivel': 'avanzado',
                            'enunciado': 'Vimos que un giro no se diagonaliza y una cizalla tampoco, pero '
                                         'las dos tienen SVD. ¿Por qué la SVD existe para toda matriz y la '
                                         'diagonalización no?',
                            'opciones': [{'id': 'a',
                                          'texto': 'Porque la SVD admite $\\sigma$ complejos cuando hace '
                                                   'falta, mientras que la diagonalización que estudiamos '
                                                   'sólo acepta autovalores reales.',
                                          'correcta': False,
                                          'explicacion': 'Al revés: los $\\sigma$ **nunca** son complejos ni '
                                                         'negativos. La SVD no esquiva el problema '
                                                         'admitiendo complejos; lo esquiva preguntando otra '
                                                         'cosa (qué par perpendicular sigue perpendicular).'},
                                         {'id': 'b',
                                          'texto': 'Porque los $v_k$ son autovectores de $A^\\top A$, que es '
                                                   'simétrica y cumple $\\langle v, A^\\top A v\\rangle = '
                                                   '\\lVert Av\\rVert^2 \\ge 0$: autovalores reales no '
                                                   'negativos y base ortogonal, siempre; diagonalizar pide '
                                                   'autovectores de $A$ misma, que un giro no tiene.',
                                          'correcta': True,
                                          'explicacion': '$A^\\top A = V\\Sigma^2V^\\top$ es la '
                                                         'diagonalización de una simétrica, que siempre '
                                                         'existe y es ortogonal; $\\sigma_k = '
                                                         '\\sqrt{\\mu_k}$ está definido porque $\\mu_k \\ge '
                                                         '0$, y $u_k = Av_k/\\sigma_k$. La diagonalización '
                                                         'de $A$ exige que $A$ deje rectas quietas, y el '
                                                         'giro no deja ninguna.'},
                                         {'id': 'c',
                                          'texto': 'Porque toda matriz $2\\times2$ es simétrica salvo un '
                                                   'signo, y las simétricas se diagonalizan con base '
                                                   'ortogonal; la SVD sólo acomoda ese signo en $U$.',
                                          'correcta': False,
                                          'explicacion': '$\\begin{pmatrix} 2 & 1 \\\\ 0 & 1 \\end{pmatrix}$ '
                                                         'no es simétrica ni lo es salvo signo, y sus '
                                                         'autovectores no son perpendiculares. La SVD usa '
                                                         'dos bases distintas, $U \\neq V$, no un signo.'},
                                         {'id': 'd',
                                          'texto': 'No es cierto: un giro tampoco tiene SVD, porque no tiene '
                                                   'autovectores reales de los que sacar $U$ y $V$.',
                                          'correcta': False,
                                          'explicacion': 'Un giro $R$ tiene SVD trivial: $R = R \\cdot I '
                                                         '\\cdot I$, con $U = R$, $\\Sigma = I$, $V = I$. '
                                                         'Los vectores singulares no salen de los '
                                                         'autovectores de $R$ sino de los de $R^\\top R = '
                                                         'I$: cualquier par perpendicular.'}],
                            'rubrica': 'Cambio de base y SVD · medio: la diagonal de la SVD nunca es '
                                       'compleja; avanzado: autovalores complejos, por qué la '
                                       'diagonalización real puede fallar; matrices simétricas: cuándo '
                                       'autovectores y vectores singulares coinciden'},
                           {'id': '09_a2',
                            'nivel': 'avanzado',
                            'enunciado': 'La aplastante $P = \\begin{pmatrix} 1 & 2 \\\\ 2 & 4 '
                                         '\\end{pmatrix}$ tiene $\\sigma_1 = 5$, $\\sigma_2 = 0$ y $v_1 = '
                                         'u_1 = \\tfrac{1}{\\sqrt5}(1, 2)$. ¿Cuál es su pseudoinversa '
                                         '$P^{+}$ y qué hace $P^{+}P$ con un vector?',
                            'opciones': [{'id': 'a',
                                          'texto': '$P^{+} = P/5$ y $P^{+}P = I$: la pseudoinversa deshace '
                                                   'lo que $P$ hizo, igual que una inversa.',
                                          'correcta': False,
                                          'explicacion': 'Control: $(P/5)P = P^2/5 = P$, no $I$ ($P^2 = '
                                                         '5P$). Nada puede deshacer del todo a $P$: el '
                                                         'núcleo $(2, -1)$ fue al cero y esa información se '
                                                         'perdió.'},
                                         {'id': 'b',
                                          'texto': 'No existe: $1/\\sigma_2 = 1/0$, el mismo obstáculo que '
                                                   'impide calcular $P^{-1}$.',
                                          'correcta': False,
                                          'explicacion': 'La pseudoinversa esquiva justo eso: donde $\\sigma '
                                                         '= 0$ pone $0$ en lugar de $1/0$ (en $\\mathbb R$, '
                                                         'la pseudoinversa de $0$ es $0$). $P^{+}$ existe '
                                                         'para toda matriz, también para las de rango $1$ y '
                                                         'las no cuadradas.'},
                                         {'id': 'c',
                                          'texto': '$P^{+} = P/25$ y $P^{+}P = P/5$, la proyección sobre la '
                                                   'recta de $(1, 2)$: deshace lo que $P$ no aplastó y manda '
                                                   'el núcleo $(2, -1)$ al cero.',
                                          'correcta': True,
                                          'explicacion': '$P^{+} = v_1\\,\\tfrac15\\,u_1^\\top = '
                                                         '\\tfrac1{25}\\begin{pmatrix} 1 & 2 \\\\ 2 & 4 '
                                                         '\\end{pmatrix}$, y $P^{+}P = \\tfrac15 P = '
                                                         'v_1v_1^\\top$ es la proyección ortogonal sobre la '
                                                         'co-imagen. Es la rango-$1$ con sus cuatro '
                                                         'subespacios: imagen y co-imagen son la recta de '
                                                         '$(1, 2)$; núcleo y contra-imagen, la de $(2, '
                                                         '-1)$.'},
                                         {'id': 'd',
                                          'texto': '$P^{+} = P/25$ y $P^{+}P = I$, porque la pseudoinversa '
                                                   'cumple $PP^{+}P = P$.',
                                          'correcta': False,
                                          'explicacion': '$PP^{+}P = P$ sí se cumple, pero no implica '
                                                         '$P^{+}P = I$: $P^{+}P = P/5$ es una proyección, '
                                                         'que sobre la imagen actúa como la identidad y '
                                                         'sobre el núcleo como el cero. Sólo con todos los '
                                                         '$\\sigma \\neq 0$ la pseudoinversa es la '
                                                         'inversa.'}],
                            'rubrica': 'Cambio de base y SVD · avanzado: pseudoinversa de Moore–Penrose: '
                                       'proyectar sobre la imagen; Productos · avanzado: los cuatro '
                                       'subespacios de una matriz 2×2 de rango 1'}],
 '10_jacobiano_primera_forma': [{'id': '10_e1',
                                 'nivel': 'elemental',
                                 'enunciado': 'Para una superficie $r(u, v)$ armamos la jacobiana $J$ con '
                                              '$r_u$ y $r_v$ como columnas. ¿Qué es la **primera forma '
                                              'fundamental**?',
                                 'opciones': [{'id': 'a',
                                               'texto': 'La tabla $J^\\top J = \\begin{pmatrix} E & F \\\\ F '
                                                        '& G \\end{pmatrix}$ de productos internos de los '
                                                        'ejes locales: $E = \\langle r_u, r_u\\rangle$, $F = '
                                                        '\\langle r_u, r_v\\rangle$, $G = \\langle r_v, '
                                                        'r_v\\rangle$.',
                                               'correcta': True,
                                               'explicacion': 'Es la $VV^\\top$ de la lección 02, con los '
                                                              'ejes en las filas de $V$ (con los ejes como '
                                                              'columnas de $J$ es $J^\\top J$): largos al '
                                                              'cuadrado en la diagonal, el ángulo escondido '
                                                              'en $F$. Con ella medimos pasitos, ángulos y '
                                                              'áreas sin salir de la grilla $(u, v)$.'},
                                              {'id': 'b',
                                               'texto': 'La matriz $3\\times3$ $JJ^\\top$: los productos '
                                                        'internos entre las filas $x$, $y$, $z$ de la '
                                                        'jacobiana.',
                                               'correcta': False,
                                               'explicacion': '$JJ^\\top$ es $3\\times3$ y mezcla las filas, '
                                                              'que no son los ejes locales. La tabla que '
                                                              'mide pasitos de la grilla es $2\\times2$: '
                                                              'entra un pasito $(du, dv)$ de $\\mathbb R^2$, '
                                                              'y por eso es $J^\\top J$.'},
                                              {'id': 'c',
                                               'texto': 'La normal $r_u \\times r_v$, que mide el área del '
                                                        'cuadradito y es lo que no se puede recorrer.',
                                               'correcta': False,
                                               'explicacion': 'La normal es la contra-imagen de $J$, '
                                                              'perpendicular al plano tangente. Su largo '
                                                              'coincide con $\\sqrt{EG - F^2}$, pero la '
                                                              'tabla completa es la que da largos y ángulos; '
                                                              'la normal sola no.'},
                                              {'id': 'd',
                                               'texto': 'La altura $h(u, v)$ con sus derivadas $h_u$ y '
                                                        '$h_v$: la pendiente en cada dirección.',
                                               'correcta': False,
                                               'explicacion': '$h_u, h_v$ son el gradiente, una forma lineal '
                                                              'que dice cuánto sube $h$. La primera forma '
                                                              'mide **largos** de pasos sobre la superficie; '
                                                              'para $r = (u, v, h)$ sale $E = 1 + h_u^2$, $F '
                                                              '= h_uh_v$, $G = 1 + h_v^2$, que no es lo '
                                                              'mismo.'}],
                                 'rubrica': 'Sin celda propia (la rúbrica del apéndice termina en SVD); más '
                                            'cercana: Rotaciones · elemental: el producto interno puede '
                                            'servir como base para definir tipos de transformaciones'},
                                {'id': '10_e2',
                                 'nivel': 'elemental',
                                 'enunciado': 'Sobre la esfera con latitud y longitud encontramos $E = R^2$, '
                                              '$F = 0$, $G = R^2\\cos^2\\varphi$. ¿Qué nos dice $F = 0$?',
                                 'opciones': [{'id': 'a',
                                               'texto': 'Que la superficie es plana en ese punto, como el '
                                                        'cilindro, que se desenrolla.',
                                               'correcta': False,
                                               'explicacion': '$F$ habla del ángulo entre los ejes locales, '
                                                              'no de si la superficie es plana. La esfera '
                                                              'tiene $F = 0$ en todos lados y no se '
                                                              'desenrolla sobre el plano: eso lo decide la '
                                                              'curvatura (que sale de $E, F, G$ y sus '
                                                              'derivadas, lección 12), no el valor de $F$ en '
                                                              'un punto.'},
                                              {'id': 'b',
                                               'texto': 'Que los ejes locales $r_\\varphi$ y $r_\\lambda$ '
                                                        'son perpendiculares (meridianos y paralelos se '
                                                        'cruzan a $90°$), aunque midan distinto porque $E '
                                                        '\\neq G$.',
                                               'correcta': True,
                                               'explicacion': '$F = \\langle r_u, r_v\\rangle = \\lvert '
                                                              'r_u\\rvert\\lvert r_v\\rvert\\cos\\theta$; '
                                                              'con ejes no nulos, $F = 0$ es $\\cos\\theta = '
                                                              '0$. Los largos van aparte: $\\sqrt E = R$ y '
                                                              '$\\sqrt G = R\\cos\\varphi$, por eso un grado '
                                                              'de longitud vale menos que uno de latitud.'},
                                              {'id': 'c',
                                               'texto': 'Que un paso de $1°$ en longitud mide lo mismo que '
                                                        'uno de $1°$ en latitud.',
                                               'correcta': False,
                                               'explicacion': 'Eso pediría $E = G$, y $G = '
                                                              'R^2\\cos^2\\varphi < R^2 = E$ fuera del '
                                                              'ecuador. $F$ no compara largos: compara '
                                                              'direcciones.'},
                                              {'id': 'd',
                                               'texto': 'Que la grilla es perpendicular en el papel; sobre '
                                                        'el terreno los ejes pueden cruzarse a otro ángulo.',
                                               'correcta': False,
                                               'explicacion': 'La grilla $(u, v)$ es perpendicular en el '
                                                              'papel **siempre**; eso no lo mide $F$. $F$ '
                                                              'mide el ángulo **sobre el terreno**: en el '
                                                              'plano inclinado $z = 1 + 0.4u + 0.3v$ la '
                                                              'grilla es perpendicular en el papel y $F = '
                                                              '0.12 \\neq 0$.'}],
                                 'rubrica': 'Sin celda propia; más cercana: Productos, determinante y '
                                            'autovectores · elemental: el producto interno decide incidencia '
                                            'y ortogonalidad'},
                                {'id': '10_m1',
                                 'nivel': 'medio',
                                 'enunciado': 'Parametrizamos el cilindro de radio $R = 10$ m como $r(u, v) '
                                              '= (R\\cos u,\\ R\\sin u,\\ v)$, con $u$ el ángulo y $v$ la '
                                              'altura. ¿Cuánto valen $E, F, G$?',
                                 'opciones': [{'id': 'a',
                                               'texto': '$E = 10$, $F = 0$, $G = 1$: el radio y la unidad de '
                                                        'altura.',
                                               'correcta': False,
                                               'explicacion': 'Falta el cuadrado: $E = \\langle r_u, '
                                                              'r_u\\rangle = R^2\\sin^2u + R^2\\cos^2u = '
                                                              '100$. $E$ es el largo **al cuadrado** del eje '
                                                              'local, como $\\lvert v \\rvert^2 = \\langle '
                                                              'v, v\\rangle$.'},
                                              {'id': 'b',
                                               'texto': '$E = 1$, $F = 0$, $G = 100$: el eje de la altura es '
                                                        'el que se estira.',
                                               'correcta': False,
                                               'explicacion': '$E$ y $G$ al revés. $E$ va con la **primera** '
                                                              'columna, $r_u = (-R\\sin u, R\\cos u, 0)$, de '
                                                              'largo $R$; $G$ con $r_v = (0, 0, 1)$, de '
                                                              'largo $1$. Un paso en $u$ es un arco de '
                                                              '$R\\,du$; un paso en $v$ mide $dv$.'},
                                              {'id': 'c',
                                               'texto': '$E = 100$, $F = 10$, $G = 1$: $F$ es el producto de '
                                                        'los dos largos.',
                                               'correcta': False,
                                               'explicacion': '$F = \\langle r_u, r_v\\rangle = (-R\\sin '
                                                              'u)\\cdot 0 + (R\\cos u)\\cdot 0 + 0 \\cdot 1 '
                                                              '= 0$. El producto de los largos sería '
                                                              '$\\lvert r_u\\rvert\\lvert r_v\\rvert$; $F$ '
                                                              'lleva además el coseno del ángulo, que acá es '
                                                              '$\\cos 90° = 0$.'},
                                              {'id': 'd',
                                               'texto': '$E = 100$, $F = 0$, $G = 1$: constantes en toda la '
                                                        'superficie.',
                                               'correcta': True,
                                               'explicacion': '$r_u = (-R\\sin u, R\\cos u, 0)$ y $r_v = (0, '
                                                              '0, 1)$: $E = R^2 = 100$, $F = 0$, $G = 1$, '
                                                              'sin depender del punto. Un paso de $1°$ en '
                                                              '$u$ mide $\\sqrt E\\,du = 10 \\cdot \\pi/180 '
                                                              '= 0.1745$ m; es la regla del plano con el eje '
                                                              '$u$ reescalado, por eso el cilindro se '
                                                              'desenrolla.'}],
                                 'rubrica': 'Sin celda propia; más cercana: Rotaciones · avanzado: existe la '
                                            'derivada de una transformación y genera un conjunto de vectores '
                                            'tangentes a trayectorias'},
                                {'id': '10_m2',
                                 'nivel': 'medio',
                                 'enunciado': 'En el plano inclinado $z = 1 + 0.4u + 0.3v$ tenemos $E = '
                                              '1.16$, $F = 0.12$, $G = 1.09$. Las líneas de la grilla son '
                                              'perpendiculares en el papel. ¿A qué ángulo se cruzan sobre el '
                                              'plano?',
                                 'opciones': [{'id': 'a',
                                               'texto': 'A $90°$: la grilla es perpendicular y una afinidad '
                                                        'conserva eso.',
                                               'correcta': False,
                                               'explicacion': 'Una afinidad conserva paralelismo, no '
                                                              'ángulos. $F \\neq 0$ es justamente la señal '
                                                              'de que los ejes locales $r_u = (1, 0, 0.4)$ y '
                                                              '$r_v = (0, 1, 0.3)$ ya no son '
                                                              'perpendiculares: $\\langle r_u, r_v\\rangle = '
                                                              '0.12$.'},
                                              {'id': 'b',
                                               'texto': 'A $83.1°$: $\\cos\\theta = F = 0.12$.',
                                               'correcta': False,
                                               'explicacion': '$F$ es $\\lvert r_u\\rvert\\lvert '
                                                              'r_v\\rvert\\cos\\theta$, no el coseno a '
                                                              'secas. Falta dividir por $\\sqrt{EG} = '
                                                              '\\sqrt{1.16 \\cdot 1.09} \\approx 1.124$; sin '
                                                              'normalizar, el ángulo sale levemente mal.'},
                                              {'id': 'c',
                                               'texto': 'A $83.9°$: $\\cos\\theta = F/\\sqrt{EG} = '
                                                        '0.12/\\sqrt{1.16 \\cdot 1.09} \\approx 0.107$.',
                                               'correcta': True,
                                               'explicacion': 'Es el coseno de la lección 02 escrito con la '
                                                              'tabla: $\\cos\\theta = \\langle r_u, '
                                                              'r_v\\rangle / (\\lvert r_u\\rvert\\lvert '
                                                              'r_v\\rvert) = F/\\sqrt{EG}$. $\\arccos 0.107 '
                                                              '\\approx 83.9°$: a $90°$ en el papel, a '
                                                              '$83.9°$ sobre el plano.'},
                                              {'id': 'd',
                                               'texto': 'A $6.1°$: $\\sin\\theta = F/\\sqrt{EG} \\approx '
                                                        '0.107$.',
                                               'correcta': False,
                                               'explicacion': '$F/\\sqrt{EG}$ es el **coseno** del ángulo, '
                                                              'no el seno; $6.1°$ es el complemento. Un $F$ '
                                                              'chico respecto de los largos significa ejes '
                                                              '**casi** perpendiculares, no casi '
                                                              'paralelos.'}],
                                 'rubrica': 'Sin celda propia; más cercana: Productos, determinante y '
                                            'autovectores · elemental: el producto interno decide incidencia '
                                            'y ortogonalidad'},
                                {'id': '10_a1',
                                 'nivel': 'avanzado',
                                 'enunciado': 'En la esfera de $R = 6371$ km, $ds^2 = R^2\\,d\\varphi^2 + '
                                              'R^2\\cos^2\\varphi\\,d\\lambda^2$. Un grado de latitud mide '
                                              '$R\\,\\pi/180 = 111.2$ km en todos lados. ¿Cuánto mide un '
                                              'grado de **longitud** a latitud $45°$?',
                                 'opciones': [{'id': 'a',
                                               'texto': '$111.2$ km: un grado es un grado, la esfera es '
                                                        'simétrica.',
                                               'correcta': False,
                                               'explicacion': 'Ignora $G = R^2\\cos^2\\varphi$: hacia el '
                                                              'polo el eje $r_\\lambda$ se achica hasta '
                                                              'desaparecer (mover la longitud casi no nos '
                                                              'mueve). Sólo en el ecuador, $\\cos 0 = 1$, el '
                                                              'grado de longitud vale $111.2$ km.'},
                                              {'id': 'b',
                                               'texto': '$78.6$ km: $ds = \\sqrt{G}\\,d\\lambda = R\\cos '
                                                        '45°\\cdot\\pi/180$.',
                                               'correcta': True,
                                               'explicacion': 'Con $d\\varphi = 0$ queda $ds = '
                                                              '\\sqrt{G}\\,d\\lambda$, y $\\sqrt G = '
                                                              'R\\cos\\varphi$: el radio del paralelo. $6371 '
                                                              '\\cdot 0.7071 \\cdot 0.01745 = 78.6$ km, '
                                                              'contra $111.2$ km del grado de latitud '
                                                              '($\\sqrt E = R$).'},
                                              {'id': 'c',
                                               'texto': '$55.6$ km: $111.2 \\cdot \\cos^2 45° = 111.2 \\cdot '
                                                        '0.5$.',
                                               'correcta': False,
                                               'explicacion': 'Se usó $G$ sin la raíz. $G = '
                                                              'R^2\\cos^2\\varphi$ es el largo **al '
                                                              'cuadrado** del eje local; el largo es $\\sqrt '
                                                              'G = R\\cos\\varphi$, y $\\cos 45° = 0.707$, '
                                                              'no $0.5$.'},
                                              {'id': 'd',
                                               'texto': '$157.2$ km: $111.2 / \\cos 45°$, porque el paralelo '
                                                        'es más corto y el grado se agranda.',
                                               'correcta': False,
                                               'explicacion': 'Al revés: el paralelo a $45°$ tiene radio '
                                                              '$R\\cos 45°$, más chico que $R$, así que el '
                                                              'mismo ángulo abarca **menos** arco. Se '
                                                              'multiplica por $\\cos\\varphi$, no se '
                                                              'divide.'}],
                                 'rubrica': 'Sin celda propia (métrica como JᵀJ); más cercana: Rotaciones · '
                                            'avanzado: existe la derivada de una transformación y genera '
                                            'vectores tangentes a trayectorias'},
                                {'id': '10_a2',
                                 'nivel': 'avanzado',
                                 'enunciado': 'Sobre la grilla $(u, v)$ de la loma tenemos la altura $h(u, '
                                              'v)$. Alguien afirma que el gradiente es un vector de la '
                                              'grilla, pero no lo es. ¿Qué es entonces, y qué hace falta '
                                              'para dibujar la dirección de máxima pendiente sobre el '
                                              'terreno?',
                                 'opciones': [{'id': 'a',
                                               'texto': 'Es el vector $(h_u, h_v)$ de la grilla; su '
                                                        'perpendicular a las curvas de nivel en el papel ya '
                                                        'es la perpendicular sobre el terreno.',
                                               'correcta': False,
                                               'explicacion': 'La perpendicular del papel y la del terreno '
                                                              'coinciden sólo si $E = G$ y $F = 0$. En la '
                                                              'esfera un paso en $\\lambda$ mide '
                                                              '$\\cos\\varphi$ veces uno en $\\varphi$: la '
                                                              'misma flecha dibujada en la grilla apunta a '
                                                              'otro lado sobre la superficie.'},
                                              {'id': 'b',
                                               'texto': 'Es la fila $(h_u, h_v)$, una forma lineal que lee '
                                                        '$dh = h_u\\,du + h_v\\,dv$ sobre cada pasito; para '
                                                        'volverla flecha sobre el terreno hace falta la '
                                                        'tabla $g = J^\\top J$: la flecha es $g^{-1}(h_u, '
                                                        'h_v)^\\top$.',
                                               'correcta': True,
                                               'explicacion': 'El gradiente es la regla graduada de la '
                                                              'lección 06: la mejor aproximación lineal de '
                                                              '$h$, que cambia de coordenadas con $A^{-1}$ '
                                                              'como toda forma. El puente entre formas y '
                                                              'vectores es el producto interno, y sobre la '
                                                              'superficie ese producto interno es la primera '
                                                              'forma $g$.'},
                                              {'id': 'c',
                                               'texto': 'Es la normal $r_u \\times r_v$ a la superficie: lo '
                                                        'que no se puede recorrer, y por eso marca hacia '
                                                        'dónde sube.',
                                               'correcta': False,
                                               'explicacion': 'La normal sale del plano tangente; la máxima '
                                                              'pendiente es una dirección **dentro** del '
                                                              'plano tangente. Son perpendiculares entre sí: '
                                                              'la normal dice qué es imposible recorrer, no '
                                                              'hacia dónde se sube más rápido.'},
                                              {'id': 'd',
                                               'texto': 'Es la primera columna $r_u = (1, 0, h_u)$ de la '
                                                        'jacobiana, el eje local en el que la altura cambia.',
                                               'correcta': False,
                                               'explicacion': '$r_u$ es a dónde va el eje $u$, un vector '
                                                              'tangente; la altura también cambia a lo largo '
                                                              'de $r_v$. El gradiente junta $h_u$ y $h_v$ en '
                                                              'una sola regla que evalúa cualquier pasito, y '
                                                              'no es ninguna columna de $J$.'}],
                                 'rubrica': 'Productos, determinante y autovectores · avanzado: el gradiente '
                                            'es una forma lineal cuya recta de nivel cero es la tangente; de '
                                            'ahí que sea perpendicular a la curva de nivel'}],
 '11_cuatro_problemas': [{'id': '11_e1',
                          'nivel': 'elemental',
                          'enunciado': 'Tenemos más mediciones que incógnitas: $Ax = y$ con $A$ alta no '
                                       'tiene solución. ¿Qué propiedad reconoce a la solución de mínimos '
                                       'cuadrados?',
                          'opciones': [{'id': 'a',
                                        'texto': 'El residuo $r = y - Ax$ es perpendicular a cada columna de '
                                                 '$A$: $A^\\top(y - Ax) = 0$.',
                                        'correcta': True,
                                        'explicacion': '$Ax$ recorre la imagen de $A$ y el punto más cercano '
                                                       'a $y$ es su proyección ortogonal; lo que sobra es '
                                                       'perpendicular a lo que la matriz puede producir, y '
                                                       'eso son las ecuaciones normales $A^\\top A\\,x = '
                                                       'A^\\top y$.'},
                                       {'id': 'b',
                                        'texto': 'El residuo $r = y - Ax$ es el vector nulo.',
                                        'correcta': False,
                                        'explicacion': 'Residuo nulo sería una solución exacta, que no '
                                                       'existe cuando las mediciones tienen error y sobran '
                                                       'ecuaciones; lo que se pide es el residuo más chico '
                                                       'posible, no cero.'},
                                       {'id': 'c',
                                        'texto': 'El residuo $r = y - Ax$ es perpendicular al vector de '
                                                 'mediciones $y$.',
                                        'correcta': False,
                                        'explicacion': 'La perpendicularidad es con la imagen de $A$ (sus '
                                                       'columnas), no con $y$; $y$ tiene una parte dentro de '
                                                       'la imagen y otra fuera, y el residuo es esa parte de '
                                                       'afuera.'},
                                       {'id': 'd',
                                        'texto': 'Cada ecuación por separado queda con el error más chico '
                                                 'posible.',
                                        'correcta': False,
                                        'explicacion': 'No se puede minimizar cada ecuación por separado: '
                                                       'bajar una sube otra; lo que se minimiza es la suma '
                                                       'de los cuadrados de todas, en conjunto.'}],
                          'rubrica': 'Cambio de base y SVD · avanzado: pseudoinversa de Moore–Penrose, el '
                                     'punto de la imagen más cercano al término independiente; proyectar '
                                     'sobre la imagen'},
                         {'id': '11_e2',
                          'nivel': 'elemental',
                          'enunciado': 'Ajustamos una recta a una nube de puntos. ¿En qué se diferencian la '
                                       'regresión simple y la regresión total?',
                          'opciones': [{'id': 'a',
                                        'texto': 'La simple minimiza las distancias perpendiculares a la '
                                                 'recta; la total, las verticales.',
                                        'correcta': False,
                                        'explicacion': 'Es al revés: la simple es la que mira sólo el error '
                                                       'en $y$ (distancia vertical) y la total es la que '
                                                       'admite error en las dos coordenadas (distancia '
                                                       'perpendicular).'},
                                       {'id': 'b',
                                        'texto': 'La simple minimiza las distancias verticales (error sólo '
                                                 'en $y$); la total, las perpendiculares a la recta (error '
                                                 'en $x$ y en $y$).',
                                        'correcta': True,
                                        'explicacion': 'En la simple las $x$ se toman exactas y el residuo '
                                                       'es vertical; en la total la recta pasa por el '
                                                       'centroide con la dirección propia de mayor autovalor '
                                                       'de $X_0^\\top X_0$ y el residuo es la distancia '
                                                       'perpendicular.'},
                                       {'id': 'c',
                                        'texto': 'Dan siempre la misma recta; cambia sólo el método de '
                                                 'cálculo.',
                                        'correcta': False,
                                        'explicacion': 'Con los mismos cuatro puntos $(\\pm1, 0)$, $(0, '
                                                       '\\pm2)$ la simple da $y = 0$ y la total da $x = 0$: '
                                                       'la pregunta cambia la respuesta.'},
                                       {'id': 'd',
                                        'texto': 'La simple usa dos puntos y la total usa todos.',
                                        'correcta': False,
                                        'explicacion': 'Las dos usan todos los puntos; dos puntos definen '
                                                       'una recta exacta sin residuo, y eso no es ajuste.'}],
                          'rubrica': 'propuesta: Cuatro problemas · elemental · vertical contra '
                                     'perpendicular, la misma nube y dos preguntas distintas'},
                         {'id': '11_m1',
                          'nivel': 'medio',
                          'enunciado': 'Ajustamos $y = ax + b$ a los puntos $(-1, 1)$, $(0, 1)$ y $(1, 4)$ '
                                       'con las ecuaciones normales $A^\\top A\\,x = A^\\top y$, $A = [\\,x '
                                       '\\mid 1\\,]$. ¿Qué obtenemos?',
                          'opciones': [{'id': 'a',
                                        'texto': '$A^\\top A = \\begin{pmatrix} 2 & 0 \\\\ 0 & 3 '
                                                 '\\end{pmatrix}$, $A^\\top y = \\begin{pmatrix} 3 \\\\ 6 '
                                                 '\\end{pmatrix}$, $(a, b) = (3, 2)$.',
                                        'correcta': False,
                                        'explicacion': 'Falta dividir la primera ecuación por $2$: $2a = 3$ '
                                                       'da $a = 3/2$, no $3$; la matriz y el término '
                                                       'independiente están bien.'},
                                       {'id': 'b',
                                        'texto': '$A^\\top A = \\begin{pmatrix} 2 & 0 \\\\ 0 & 3 '
                                                 '\\end{pmatrix}$, $A^\\top y = \\begin{pmatrix} 3 \\\\ 6 '
                                                 '\\end{pmatrix}$, $(a, b) = (2, 3/2)$.',
                                        'correcta': False,
                                        'explicacion': 'Están cambiadas: la primera incógnita es la '
                                                       'pendiente porque la primera columna de $A$ es la de '
                                                       'las $x$; $2a = 3$ y $3b = 6$ dan $a = 3/2$, $b = '
                                                       '2$.'},
                                       {'id': 'c',
                                        'texto': '$A^\\top A = \\begin{pmatrix} 2 & 0 \\\\ 0 & 3 '
                                                 '\\end{pmatrix}$, $A^\\top y = \\begin{pmatrix} 3 \\\\ 6 '
                                                 '\\end{pmatrix}$, $(a, b) = (3/2, 2)$.',
                                        'correcta': True,
                                        'explicacion': 'Con las $x$ centradas $A^\\top A$ sale diagonal, '
                                                       '$\\sum x_i^2 = 2$ y $n = 3$; $\\sum x_i y_i = 3$, '
                                                       '$\\sum y_i = 6$, y la recta $y = \\tfrac32 x + 2$ '
                                                       'deja residuo $(\\tfrac12, -1, \\tfrac12)$, '
                                                       'perpendicular a las dos columnas.'},
                                       {'id': 'd',
                                        'texto': '$A^\\top A = \\begin{pmatrix} 2 & 0 \\\\ 0 & 3 '
                                                 '\\end{pmatrix}$, $A^\\top y = \\begin{pmatrix} 3 \\\\ 6 '
                                                 '\\end{pmatrix}$, $(a, b) = (3/2, 0)$.',
                                        'correcta': False,
                                        'explicacion': 'Con $b = 0$ la recta pasa por el origen a la fuerza, '
                                                       'que es lo que sale al olvidar la columna de unos; la '
                                                       'segunda ecuación normal, $3b = 6$, dice $b = 2$.'}],
                          'rubrica': 'Cambio de base y SVD · avanzado: pseudoinversa de Moore–Penrose, '
                                     'resolver un sistema sobredeterminado proyectando sobre la imagen'},
                         {'id': '11_m2',
                          'nivel': 'medio',
                          'enunciado': 'Ubicamos un poste por sus distancias a tres mojones: $M_1 = (0, 0)$, '
                                       '$M_2 = (6, 0)$, $M_3 = (3, 7)$ a $5$, $5$ y $3$ m. ¿Cómo lo '
                                       'resolvemos y qué punto sale?',
                          'opciones': [{'id': 'a',
                                        'texto': 'Restando las ecuaciones de los círculos se cancela $x^2 + '
                                                 'y^2$ y quedan rectas; con las tres cintas el punto es $(3, '
                                                 '4)$.',
                                        'correcta': True,
                                        'explicacion': 'Primero menos segundo da $12x = 36$ y primero menos '
                                                       'tercero $6x + 14y = 74$: los ejes radicales, un '
                                                       'sistema lineal; $(3, 4)$ cumple los tres círculos '
                                                       '($9 + 16 = 25$, $0 + 9 = 9$).'},
                                       {'id': 'b',
                                        'texto': 'Restando las ecuaciones de los círculos quedan rectas; con '
                                                 'las tres cintas el punto es $(3, -4)$.',
                                        'correcta': False,
                                        'explicacion': '$(3, -4)$ cumple sólo los dos primeros círculos: es '
                                                       'el otro corte, y la tercera cinta ($3$ m a $M_3$) es '
                                                       'justamente la que lo descarta.'},
                                       {'id': 'c',
                                        'texto': 'Cada círculo es cuadrático, así que el sistema no se puede '
                                                 'linealizar y hay que iterar desde una aproximación '
                                                 'inicial.',
                                        'correcta': False,
                                        'explicacion': 'Se puede iterar por Taylor, pero no hace falta: la '
                                                       'diferencia de dos círculos es lineal porque el '
                                                       'término $x^2 + y^2$ es el mismo en todos.'},
                                       {'id': 'd',
                                        'texto': 'Como hay tres ecuaciones y dos incógnitas no hay solución; '
                                                 'tomamos el promedio de los tres mojones, $(3, 7/3)$.',
                                        'correcta': False,
                                        'explicacion': 'Promediar mojones no usa las distancias como '
                                                       'distancias; con tres círculos exactos quedan dos '
                                                       'rectas que se cortan en un punto, y con más de tres '
                                                       'se usan las ecuaciones normales.'}],
                          'rubrica': 'Cambio de base y SVD · avanzado: pseudoinversa, sistema '
                                     'sobredeterminado; con tres mojones todavía es un sistema $2\\times2$ '
                                     'exacto'},
                         {'id': '11_a1',
                          'nivel': 'avanzado',
                          'enunciado': 'Superponemos dos relevamientos del mismo lote (Procrustes): el '
                                       'segundo se midió con otra cinta, en pies. Centramos las nubes, '
                                       'armamos $H = P_0^\\top Q_0$ y sacamos la rotación de su SVD. ¿Qué '
                                       'pasa si no incluimos la escala?',
                          'opciones': [{'id': 'a',
                                        'texto': 'Nada: la rotación $R = VU^\\top$ ya absorbe el cambio de '
                                                 'unidad porque la SVD separa giro de estiramiento.',
                                        'correcta': False,
                                        'explicacion': 'La SVD separa el giro ($U$, $V$) del estiramiento '
                                                       '($\\Sigma$), pero $R = VU^\\top$ es ortogonal y no '
                                                       'puede estirar; el factor de unidad queda en '
                                                       '$\\Sigma$ y hay que leerlo como escala $s$.'},
                                       {'id': 'b',
                                        'texto': 'La rotación sale igual, pero la nube llevada queda '
                                                 '$3{,}28$ veces más chica y el residuo no baja aunque el '
                                                 'giro sea correcto; hace falta la escala $s$.',
                                        'correcta': True,
                                        'explicacion': 'Como las nubes son la misma figura, $\\Sigma$ es un '
                                                       'múltiplo de la identidad y $R$ es exacto; sin $s$ '
                                                       'cada punto queda a $1/3{,}28$ de su distancia '
                                                       'correcta, y el residuo mide ese error de unidad, no '
                                                       'de giro.'},
                                       {'id': 'c',
                                        'texto': 'La rotación sale mal, porque $H$ cambia de forma al '
                                                 'multiplicar $Q$ por una constante.',
                                        'correcta': False,
                                        'explicacion': 'Multiplicar $Q_0$ por una constante multiplica $H$ y '
                                                       '$\\Sigma$ por ella, pero no toca $U$ ni $V$: la '
                                                       'rotación es la misma.'},
                                       {'id': 'd',
                                        'texto': 'Hay que convertir antes a metros; Procrustes sólo funciona '
                                                 'si las dos nubes tienen la misma escala.',
                                        'correcta': False,
                                        'explicacion': 'Procrustes con escala resuelve exactamente ese caso: '
                                                       '$s$ sale de $\\operatorname{tr}\\Sigma / \\lVert '
                                                       'P_0\\rVert^2$ sin convertir nada a mano.'}],
                          'rubrica': 'Cambio de base y SVD · medio: en la SVD las bases de entrada y salida '
                                     'son distintas, girar, estirar, girar; $R = VU^\\top$ se queda con los '
                                     'giros'},
                         {'id': '11_a2',
                          'nivel': 'avanzado',
                          'enunciado': 'Cuatro puntos ya centrados, $(2, 2)$, $(-2, -2)$, $(1, -1)$, $(-1, '
                                       '1)$, con $X^\\top X = \\begin{pmatrix} 10 & 6 \\\\ 6 & 10 '
                                       '\\end{pmatrix}$ (autovalores $16$ y $4$). ¿Qué recta da la regresión '
                                       'total y cuál la regresión simple de $y$ sobre $x$?',
                          'opciones': [{'id': 'a',
                                        'texto': 'Total: $y = x$ (dirección del autovalor $16$); simple: $y '
                                                 '= 0{,}6\\,x$ (pendiente $\\sum x_i y_i / \\sum x_i^2 = '
                                                 '6/10$).',
                                        'correcta': True,
                                        'explicacion': 'La recta total va por la dirección de mayor '
                                                       'dispersión, $(1, 1)$, y deja residuo '
                                                       '$\\lambda_{\\min} = 4$; la simple minimiza sólo '
                                                       'residuos verticales y su pendiente es $6/10$, más '
                                                       'chata que la total. Dos rectas distintas para la '
                                                       'misma nube.'},
                                       {'id': 'b',
                                        'texto': 'Total: $y = -x$ (dirección del autovalor $4$); simple: $y '
                                                 '= 0{,}6\\,x$.',
                                        'correcta': False,
                                        'explicacion': 'El autovalor menor, $4$, da la normal a la recta '
                                                       'total, no su dirección; la recta sigue la dirección '
                                                       'de mayor autovalor, $(1, 1)$.'},
                                       {'id': 'c',
                                        'texto': 'Las dos dan $y = x$: la nube es simétrica respecto de esa '
                                                 'bisectriz y por eso las dos rectas coinciden.',
                                        'correcta': False,
                                        'explicacion': 'La simple mide residuos sólo en $y$ y su pendiente '
                                                       'es $\\sum x_i y_i / \\sum x_i^2 = 6/10 \\neq 1$; '
                                                       'sólo coincidiría con la total si la correlación '
                                                       'fuera perfecta.'},
                                       {'id': 'd',
                                        'texto': 'Total: $y = 0{,}6\\,x$ (el cociente $6/10$ de la matriz); '
                                                 'simple: $y = x$ (la dirección del autovalor $16$).',
                                        'correcta': False,
                                        'explicacion': 'Están cambiadas: $6/10$ es la pendiente de la '
                                                       'regresión simple, y la dirección propia del '
                                                       'autovalor $16$, $y = x$, es la de la total.'}],
                          'rubrica': 'Cambio de base y SVD · elemental: la circunferencia unidad se '
                                     'transforma en una elipse y sus ejes son la base; leída al revés, datos '
                                     '→ elipse de dispersión → ejes'}],
 '12_curvatura': [{'id': '12_e1',
                   'nivel': 'elemental',
                   'enunciado': 'En un punto de una superficie conocemos las dos curvaturas principales '
                                '$\\kappa_1$ y $\\kappa_2$. ¿Qué es la curvatura de Gauss $K$?',
                   'opciones': [{'id': 'a',
                                 'texto': 'El promedio $(\\kappa_1 + \\kappa_2)/2$.',
                                 'correcta': False,
                                 'explicacion': 'Ese promedio es la curvatura media $H$; cambia al doblar '
                                                'una hoja en cilindro, cosa que $K$ no hace.'},
                                {'id': 'b',
                                 'texto': 'La mayor de las dos, $\\kappa_1$.',
                                 'correcta': False,
                                 'explicacion': '$\\kappa_1$ es sólo la curvatura normal máxima; no dice '
                                                'nada del otro rumbo y no distingue la silla del cuenco.'},
                                {'id': 'c',
                                 'texto': 'El producto $\\kappa_1\\kappa_2 = \\det II / \\det I$.',
                                 'correcta': True,
                                 'explicacion': 'Es el determinante de $S = I^{-1} II$, cuánto agranda el '
                                                'área la aplicación normal; su signo dice si la superficie '
                                                'queda de un lado del plano tangente ($K > 0$) o lo cruza '
                                                '($K < 0$).'},
                                {'id': 'd',
                                 'texto': 'La curvatura en el rumbo de la grilla $u$, $L / E$.',
                                 'correcta': False,
                                 'explicacion': '$L/E$ es la curvatura normal en una dirección particular de '
                                                'la grilla, que depende de cómo se parametrizó; $K$ no '
                                                'depende de la grilla.'}],
                   'rubrica': 'propuesta: Curvatura · elemental · $K = \\kappa_1\\kappa_2 = \\det II/\\det '
                              'I$; hecho geométrico: su signo dice cuenco, canaleta o silla'},
                  {'id': '12_e2',
                   'nivel': 'elemental',
                   'enunciado': 'Apoyamos el nivel en el punto más bajo de un paso de montaña: la burbuja '
                                'centra. Hacia el este y el oeste el terreno sube; hacia el norte y el sur '
                                'baja. ¿Qué dice eso de la curvatura en ese punto?',
                   'opciones': [{'id': 'a',
                                 'texto': 'La tangente es horizontal, así que la curvatura es cero en todos '
                                          'los rumbos.',
                                 'correcta': False,
                                 'explicacion': 'Burbuja centrada es gradiente nulo (término lineal cero), '
                                                'no hessiana nula: a un paso el terreno ya se aparta del '
                                                'plano del nivel, y cuánto se aparta es la curvatura.'},
                                {'id': 'b',
                                 'texto': 'Las curvaturas principales tienen signos opuestos y $K < 0$: la '
                                          'superficie cruza su plano tangente.',
                                 'correcta': True,
                                 'explicacion': 'Sube en un rumbo ($\\kappa_1 > 0$) y baja en el '
                                                'perpendicular ($\\kappa_2 < 0$); es la silla $z = (x^2 - '
                                                'y^2)/4$, con $K = -1/4$ y dos rumbos a $45°$ donde la '
                                                'sección normal no se curva.'},
                                {'id': 'c',
                                 'texto': 'Es un pozo: la curvatura es positiva en todos los rumbos.',
                                 'correcta': False,
                                 'explicacion': 'Un pozo sube en todos los rumbos ($z = (x^2 + y^2)/4$); acá '
                                                'hacia el norte baja, y ese signo cambia todo.'},
                                {'id': 'd',
                                 'texto': 'Es una cima: la curvatura es negativa en todos los rumbos.',
                                 'correcta': False,
                                 'explicacion': 'Una cima baja en todos los rumbos; hacia el este el paso '
                                                'sube, así que hay un rumbo de curvatura positiva.'}],
                   'rubrica': 'propuesta: Curvatura · elemental · tangente horizontal no es curvatura cero; '
                              'hecho geométrico: la silla sube en un rumbo y baja en el perpendicular'},
                  {'id': '12_m1',
                   'nivel': 'medio',
                   'enunciado': 'En un punto los radios de curvatura principales valen $R_1 = 4$ m y $R_2 = '
                                '9$ m. El apunte del profesor promedia el radio $1/\\chi(\\alpha)$ sobre un '
                                'cuadrante. ¿Qué radio medio obtiene?',
                   'opciones': [{'id': 'a',
                                 'texto': '$R = 6{,}5$ m, el promedio aritmético de $R_1$ y $R_2$.',
                                 'correcta': False,
                                 'explicacion': 'Promediar los dos extremos a mano ignora cómo varía '
                                                '$1/\\chi(\\alpha)$ entre ellos; la integral con la '
                                                'sustitución $u = \\sqrt{R_2/R_1}\\tan\\alpha$ da la media '
                                                'geométrica, no la aritmética.'},
                                {'id': 'b',
                                 'texto': '$R = 6$ m, porque $R = \\sqrt{R_1 R_2}$.',
                                 'correcta': True,
                                 'explicacion': '$\\frac{2}{\\pi}\\int_0^{\\pi/2} '
                                                '\\frac{d\\alpha}{\\chi(\\alpha)}$ con Euler $\\chi = '
                                                '\\cos^2\\alpha/R_1 + \\sin^2\\alpha/R_2$ se reduce a '
                                                '$\\int_0^\\infty du/(1 + u^2) = \\pi/2$ y queda $\\sqrt{R_1 '
                                                'R_2}$; sobre el elipsoide es $\\sqrt{MN}$, la esfera '
                                                'local.'},
                                {'id': 'c',
                                 'texto': '$R = 4$ m: el radio medio es el menor, porque la curvatura máxima '
                                          'manda.',
                                 'correcta': False,
                                 'explicacion': 'El menor radio es sólo el extremo de un rumbo; el promedio '
                                                'sobre todos los rumbos queda entre $R_1$ y $R_2$.'},
                                {'id': 'd',
                                 'texto': '$R \\approx 5{,}54$ m, el promedio de las curvaturas invertido: '
                                          '$2/(1/R_1 + 1/R_2)$.',
                                 'correcta': False,
                                 'explicacion': 'Esa es la inversa de la curvatura media $H$; el apunte '
                                                'promedia radios sobre el ángulo, no curvaturas, y eso lleva '
                                                'a la media geométrica.'}],
                   'rubrica': 'propuesta: Curvatura · medio · Euler $\\chi(\\alpha) = \\chi_1\\cos^2\\alpha '
                              '+ \\chi_2\\sin^2\\alpha$ y el radio medio $\\sqrt{R_1 R_2}$'},
                  {'id': '12_m2',
                   'nivel': 'medio',
                   'enunciado': 'En una canaleta cilíndrica de radio $R = 2$ las curvaturas principales son '
                                '$\\kappa_1 = 1/2$ (a través) y $\\kappa_2 = 0$ (a lo largo). ¿Cuánto vale '
                                'la curvatura normal en el rumbo a $45°$ de la dirección principal?',
                   'opciones': [{'id': 'a',
                                 'texto': '$\\kappa_n = 1/4$, por Euler: $\\kappa_1\\cos^2 45° + '
                                          '\\kappa_2\\sin^2 45°$.',
                                 'correcta': True,
                                 'explicacion': 'La curvatura normal es una forma cuadrática en el rumbo y a '
                                                '$45°$ pesa mitad y mitad: $\\tfrac12\\cdot\\tfrac12 + '
                                                '0\\cdot\\tfrac12 = \\tfrac14$; el círculo osculador en ese '
                                                'rumbo tiene radio $4$, el doble que a través.'},
                                {'id': 'b',
                                 'texto': '$\\kappa_n = 1/2$: la curvatura es la misma en todos los rumbos '
                                          'porque el punto está sobre un cilindro.',
                                 'correcta': False,
                                 'explicacion': 'Curvatura igual en todo rumbo es la esfera (punto '
                                                'umbilical); el cilindro tiene un rumbo recto, y entre $1/2$ '
                                                'y $0$ la curvatura varía con el rumbo.'},
                                {'id': 'c',
                                 'texto': '$\\kappa_n = \\sqrt{2}/4$, por Euler: $\\kappa_1\\cos 45° + '
                                          '\\kappa_2\\sin 45°$.',
                                 'correcta': False,
                                 'explicacion': 'Euler lleva los cosenos y senos al cuadrado: la curvatura '
                                                'normal es cuadrática en el vector rumbo, no lineal.'},
                                {'id': 'd',
                                 'texto': '$\\kappa_n = 0$: la sección a $45°$ es una recta porque el '
                                          'cilindro se desenrolla en el plano.',
                                 'correcta': False,
                                 'explicacion': 'Desenrollarse sin estirar dice $K = \\kappa_1\\kappa_2 = '
                                                '0$, no que toda sección sea recta; la única sección normal '
                                                'recta es la paralela al eje.'}],
                   'rubrica': 'propuesta: Curvatura · medio · la curvatura normal es cuadrática en el rumbo '
                              '(Euler); hecho geométrico: el cilindro sólo es recto a lo largo del eje'},
                  {'id': '12_a1',
                   'nivel': 'avanzado',
                   'enunciado': 'Por un punto trazamos la sección normal en cierta dirección, de radio de '
                                'curvatura $\\rho_\\alpha = 10$ m, y después un plano con la misma recta '
                                'tangente pero inclinado $60°$ respecto del normal. ¿Qué radio tiene la '
                                'curva de esa sección oblicua?',
                   'opciones': [{'id': 'a',
                                 'texto': '$\\rho_\\beta = 20$ m: inclinar el plano aplana la curva y '
                                          'agranda el radio.',
                                 'correcta': False,
                                 'explicacion': 'Al revés: el círculo osculador de la sección oblicua tiene '
                                                'por centro la proyección del centro de curvatura de la '
                                                'sección normal sobre el plano oblicuo, y el radio queda '
                                                '$\\rho_\\alpha\\cos\\theta$: se achica, no se agranda.'},
                                {'id': 'b',
                                 'texto': '$\\rho_\\beta = 10$ m: el radio depende sólo de la dirección '
                                          'tangente, no del plano que corta.',
                                 'correcta': False,
                                 'explicacion': 'Depende del plano: la curvatura normal es sólo la parte de '
                                                'la aceleración sobre la normal, y un plano inclinado ve '
                                                'además una componente dentro de la superficie.'},
                                {'id': 'c',
                                 'texto': '$\\rho_\\beta = 5$ m, por Meusnier: $\\rho_\\beta = '
                                          '\\rho_\\alpha\\cos\\theta$.',
                                 'correcta': True,
                                 'explicacion': 'Con $\\theta = 60°$, $\\cos\\theta = 1/2$ y el radio se '
                                                'reduce a la mitad; es la misma cuenta que da el radio del '
                                                "paralelo del elipsoide, $x' = N\\cos\\varphi$, como sección "
                                                'oblicua del primer vertical.'},
                                {'id': 'd',
                                 'texto': '$\\rho_\\beta = 10/\\cos 60° = 20$ m, porque la sección oblicua '
                                          'es más larga.',
                                 'correcta': False,
                                 'explicacion': 'Dividir por $\\cos\\theta$ es invertir el factor de la '
                                                'fórmula de Meusnier; la sección oblicua es más curva, así '
                                                'que su radio es $\\rho_\\alpha\\cos\\theta$, menor.'}],
                   'rubrica': 'propuesta: Curvatura · avanzado · Meusnier $\\rho_\\beta = '
                              '\\rho_\\alpha\\cos\\theta$; hecho geométrico: el paralelo es sección oblicua '
                              "del primer vertical, $x' = N\\cos\\varphi$"},
                  {'id': '12_a2',
                   'nivel': 'avanzado',
                   'enunciado': 'Queremos un plano de la Tierra que conserve todas las distancias, aunque '
                                'sea de una región chica. Con $K$ y lo que mostró el cilindro, ¿qué '
                                'concluimos?',
                   'opciones': [{'id': 'a',
                                 'texto': 'Se puede en una región chica: cerca de un punto toda superficie '
                                          'es su plano tangente.',
                                 'correcta': False,
                                 'explicacion': 'El plano tangente aproxima a primer orden, pero conservar '
                                                'distancias conserva $K$ (theorema egregium) y $K = 1/(MN) > '
                                                '0$ en cualquier entorno, por chico que sea; el error es de '
                                                'segundo orden, no cero.'},
                                {'id': 'b',
                                 'texto': 'No se puede: doblar sin estirar no cambia $K$, el plano tiene $K '
                                          '= 0$ y el elipsoide $K = 1/(MN) > 0$.',
                                 'correcta': True,
                                 'explicacion': 'El cilindro ($\\kappa_1 = 1/R$, $\\kappa_2 = 0$, $K = 0$) '
                                                'se desenrolla sin estirar porque comparte $K$ con el plano; '
                                                'la esfera y el elipsoide no, y toda proyección elige qué '
                                                'sacrificar.'},
                                {'id': 'c',
                                 'texto': 'Se puede si la región no contiene los polos, donde $M = N$ y la '
                                          'curvatura es máxima.',
                                 'correcta': False,
                                 'explicacion': '$K > 0$ en todo el elipsoide, polos incluidos o no; los '
                                                'polos sólo son los puntos umbilicales, donde las dos '
                                                'curvaturas coinciden.'},
                                {'id': 'd',
                                 'texto': 'No se puede porque $\\kappa_1 \\ne \\kappa_2$ en el elipsoide; en '
                                          'la esfera, donde son iguales, sí.',
                                 'correcta': False,
                                 'explicacion': 'La esfera tiene $K = 1/R^2 > 0$ y tampoco se aplana; lo que '
                                                'impide la isometría es $K \\ne 0$, no que las curvaturas '
                                                'principales sean distintas.'}],
                   'rubrica': 'propuesta: Curvatura · avanzado · $K$ sobrevive al doblado sin estirar '
                              '(theorema egregium); hecho geométrico: la hoja se enrolla en cilindro pero la '
                              'cáscara no se aplana'}],
 '13_elipsoide': [{'id': '13_e1',
                   'nivel': 'elemental',
                   'enunciado': 'Un receptor GNSS nos da latitud $\\varphi = 45°$ para un punto de la '
                                'superficie del elipsoide ($h = 0$). ¿Qué ángulo forma la recta del mojón al '
                                'centro de la Tierra con el plano del ecuador?',
                   'opciones': [{'id': 'a',
                                 'texto': '$45°$: toda normal a la superficie pasa por el centro.',
                                 'correcta': False,
                                 'explicacion': 'Eso vale en la esfera; en la elipse meridiana la normal es '
                                                'perpendicular a la tangente y corta el eje polar debajo del '
                                                'centro salvo en el ecuador y los polos.'},
                                {'id': 'b',
                                 'texto': 'Un poco menos de $45°$: es la latitud geocéntrica, $\\tan\\psi = '
                                          '(1 - e^2)\\tan\\varphi$.',
                                 'correcta': True,
                                 'explicacion': 'La geodésica $\\varphi$ es el ángulo de la normal; la recta '
                                                'al centro está más acostada, $\\psi = \\arctan(1 - e^2) '
                                                "\\approx 44° 48'$, unos $11{,}5'$ menos en GRS80."},
                                {'id': 'c',
                                 'texto': 'Un poco más de $45°$: el achatamiento empina la recta al centro.',
                                 'correcta': False,
                                 'explicacion': 'El signo está al revés: $(1 - e^2) < 1$ achica la tangente, '
                                                'así que $\\lvert\\psi\\rvert \\le \\lvert\\varphi\\rvert$ '
                                                'siempre.'},
                                {'id': 'd',
                                 'texto': 'No se puede saber sin la altura $h$ del mojón.',
                                 'correcta': False,
                                 'explicacion': 'Sobre la superficie ($h = 0$) $\\psi$ depende sólo de '
                                                '$\\varphi$ y de $e^2$; la altura cambia la cuenta sólo si '
                                                'el punto se corre por la normal.'}],
                   'rubrica': 'propuesta: Elipsoide · elemental · tres latitudes, $\\psi \\le \\beta \\le '
                              '\\varphi$; hecho geométrico: la normal no pasa por el centro'},
                  {'id': '13_e2',
                   'nivel': 'elemental',
                   'enunciado': 'En un punto del elipsoide de revolución hablamos de dos radios de '
                                'curvatura, $M$ y $N$. ¿Qué es cada uno?',
                   'opciones': [{'id': 'a',
                                 'texto': '$M$ es el radio del paralelo y $N$ el del meridiano.',
                                 'correcta': False,
                                 'explicacion': "El radio del paralelo es $x' = N\\cos\\varphi$, no $M$; $M$ "
                                                'es el radio de curvatura de la elipse meridiana.'},
                                {'id': 'b',
                                 'texto': '$M$ es el radio de la sección meridiana y $N$ el de la sección '
                                          'normal perpendicular a ella, el primer vertical; $M \\le N$, '
                                          'iguales sólo en los polos.',
                                 'correcta': True,
                                 'explicacion': 'Son las direcciones principales del elipsoide (por simetría '
                                                'del plano meridiano), con $\\kappa_1 = 1/M$ y $\\kappa_2 = '
                                                '1/N$; el elipsoide es más curvo a lo largo del meridiano '
                                                'que a lo ancho.'},
                                {'id': 'c',
                                 'texto': '$M$ y $N$ son los semiejes $a$ y $b$ de la elipse meridiana.',
                                 'correcta': False,
                                 'explicacion': 'Los semiejes son constantes del elipsoide; $M$ y $N$ '
                                                'cambian con la latitud, de $b^2/a$ y $a$ en el ecuador a '
                                                '$a^2/b$ en el polo.'},
                                {'id': 'd',
                                 'texto': '$M$ es el radio del meridiano y $N$ la distancia del punto al '
                                          'centro de la Tierra.',
                                 'correcta': False,
                                 'explicacion': '$N$ es la distancia del punto al eje polar medida a lo '
                                                'largo de la normal, no al centro; por eso la normal corta '
                                                'el eje polar a $N e^2 \\sin\\varphi$ del centro.'}],
                   'rubrica': 'propuesta: Elipsoide · elemental · $M$ meridiano y $N$ primer vertical son '
                              'las direcciones principales; hecho geométrico: $N$ es el tramo de la normal '
                              'hasta el eje polar'},
                  {'id': '13_m1',
                   'nivel': 'medio',
                   'enunciado': 'En el ecuador de GRS80 ($a = 6378137$ m, $e^2 = 0{,}00669438$) calculamos '
                                '$N - M$. ¿Cuánto da?',
                   'opciones': [{'id': 'a',
                                 'texto': '$0$: en el ecuador la simetría obliga $M = N$.',
                                 'correcta': False,
                                 'explicacion': '$M = N$ ocurre en los polos, donde todos los rumbos son '
                                                'meridianos; en el ecuador la sección meridiana es la más '
                                                'curva ($M = b^2/a$) y el primer vertical es el ecuador '
                                                'mismo ($N = a$).'},
                                {'id': 'b',
                                 'texto': '$a e^2 \\approx 42{,}7$ km, porque $N = a$ y $M = a(1 - e^2)$.',
                                 'correcta': True,
                                 'explicacion': 'Con $\\sin\\varphi = 0$ las dos fórmulas se simplifican y '
                                                '$N - M = a e^2 = (a^2 - b^2)/a$; en el elipsoide de juguete '
                                                '$a = 5$, $b = 4$ da $5 - 3{,}2 = 1{,}8$.'},
                                {'id': 'c',
                                 'texto': '$a - b \\approx 21{,}4$ km, la diferencia entre los semiejes.',
                                 'correcta': False,
                                 'explicacion': '$a - b = af$ es el achatamiento en metros, otra cosa; $N - '
                                                'M$ en el ecuador vale $a e^2 \\approx 2af$, el doble.'},
                                {'id': 'd',
                                 'texto': '$a e^2 / 2 \\approx 21{,}3$ km, porque $M$ lleva exponente $3/2$ '
                                          'y $N$ exponente $1/2$.',
                                 'correcta': False,
                                 'explicacion': 'Los exponentes actúan sobre $1 - e^2\\sin^2\\varphi$, que '
                                                'en el ecuador vale $1$; lo que distingue $M$ de $N$ ahí es '
                                                'el factor $(1 - e^2)$ entero.'}],
                   'rubrica': 'propuesta: Elipsoide · medio · $M$ y $N$ en ecuador y polo; hecho geométrico: '
                              'más curvo a lo largo del meridiano que a lo ancho'},
                  {'id': '13_m2',
                   'nivel': 'medio',
                   'enunciado': 'En la esfera de radio $R$ (el caso $M = N = R$), ¿cuánto mide el radio del '
                                "paralelo de latitud $\\varphi = 60°$, $x' = N\\cos\\varphi$?",
                   'opciones': [{'id': 'a',
                                 'texto': '$R\\sqrt{3}/2$.',
                                 'correcta': False,
                                 'explicacion': 'Eso es $R\\sin 60°$: la altura del punto sobre el ecuador, '
                                                'no la distancia al eje polar.'},
                                {'id': 'b',
                                 'texto': '$R$: todos los paralelos son círculos máximos.',
                                 'correcta': False,
                                 'explicacion': 'Sólo el ecuador es círculo máximo; los demás paralelos '
                                                'tienen radio $R\\cos\\varphi$ y se achican hacia el polo, '
                                                'por eso un grado de longitud vale cada vez menos metros.'},
                                {'id': 'c',
                                 'texto': '$R/2$.',
                                 'correcta': True,
                                 'explicacion': '$\\cos 60° = 1/2$: a $60°$ de latitud un grado de longitud '
                                                'mide la mitad que en el ecuador, y en el elipsoide la misma '
                                                'cuenta lleva $N$ en lugar de $R$.'},
                                {'id': 'd',
                                 'texto': '$R/4$.',
                                 'correcta': False,
                                 'explicacion': 'Es $\\cos^2 60°$: el cuadrado aparece en la primera forma, '
                                                '$G = N^2\\cos^2\\varphi$, pero el radio del paralelo lleva '
                                                'el coseno sin elevar.'}],
                   'rubrica': 'propuesta: Elipsoide · medio · primera forma $E = M^2$, $G = '
                              'N^2\\cos^2\\varphi$; hecho geométrico: el paralelo se achica con '
                              '$\\cos\\varphi$'},
                  {'id': '13_a1',
                   'nivel': 'avanzado',
                   'enunciado': 'Elipsoide de juguete con $a = 5$, $b = 4$ ($e^2 = 0{,}36$). En el ecuador '
                                '$M = 3{,}2$ y $N = 5$. ¿Cuánto valen $M$ y $N$ en el polo?',
                   'opciones': [{'id': 'a',
                                 'texto': '$M = N = 4$: en el polo el radio es $b$, la distancia al centro.',
                                 'correcta': False,
                                 'explicacion': '$b$ es la distancia del polo al centro, no el radio de '
                                                'curvatura; la elipse en el extremo del eje menor es más '
                                                'chata que un círculo de radio $b$ y su osculador es mayor.'},
                                {'id': 'b',
                                 'texto': '$M = N = 5$: en el polo se recupera el radio ecuatorial $a$.',
                                 'correcta': False,
                                 'explicacion': '$N$ crece del ecuador ($a$) al polo, así que no puede '
                                                'volver a $a$: con $\\sin\\varphi = 1$ queda $a/\\sqrt{1 - '
                                                'e^2} = a/(b/a)$.'},
                                {'id': 'c',
                                 'texto': '$M = 3{,}2$ y $N = 5$, como en el ecuador: los radios no dependen '
                                          'de la latitud en un elipsoide de revolución.',
                                 'correcta': False,
                                 'explicacion': 'La simetría de revolución borra la dependencia de '
                                                '$\\lambda$, no la de $\\varphi$; los dos radios crecen del '
                                                'ecuador al polo.'},
                                {'id': 'd',
                                 'texto': '$M = N = a^2/b = 6{,}25$: en el polo coinciden.',
                                 'correcta': True,
                                 'explicacion': 'Con $\\sin^2\\varphi = 1$, $N = a/\\sqrt{1 - e^2} = '
                                                '5/0{,}8$ y $M = a(1 - e^2)/(1 - e^2)^{3/2}$, el mismo '
                                                'valor; en el polo pasan todos los meridianos, todos los '
                                                'rumbos son iguales y el punto es umbilical.'}],
                   'rubrica': 'propuesta: Elipsoide · avanzado · deducciones por simetría: en el polo todos '
                              'los rumbos son meridianos y $M = N = a^2/b$'},
                  {'id': '13_a2',
                   'nivel': 'avanzado',
                   'enunciado': 'Pasamos $(\\varphi, \\lambda, h = 0)$ a cartesianas geocéntricas. $X = '
                                'N\\cos\\varphi\\cos\\lambda$ e $Y = N\\cos\\varphi\\sin\\lambda$ salen '
                                'directo del radio del paralelo. ¿Y la $Z$?',
                   'opciones': [{'id': 'a',
                                 'texto': '$Z = N\\sin\\varphi$, por simetría con $X$ e $Y$.',
                                 'correcta': False,
                                 'explicacion': 'Eso sería si la normal pasara por el centro; como corta el '
                                                'eje polar a $N e^2\\sin\\varphi$ debajo, hay que descontar '
                                                'esa parte: en GRS80 el error es de unos $30$ km a $45°$, y '
                                                'llega a $43$ km cerca del polo.'},
                                {'id': 'b',
                                 'texto': '$Z = N(1 - e^2)\\sin\\varphi$: el tramo de la normal desde el eje '
                                          'polar hasta el punto mide $N$, pero arranca debajo del centro.',
                                 'correcta': True,
                                 'explicacion': '$Z = N\\sin\\varphi - N e^2\\sin\\varphi$; equivale a '
                                                "$\\tan\\psi = Z/x' = (1 - e^2)\\tan\\varphi$, y con $h \\ne "
                                                '0$ pasa a $(N(1 - e^2) + h)\\sin\\varphi$ porque la altura '
                                                'sí se mide por la normal completa.'},
                                {'id': 'c',
                                 'texto': '$Z = b\\sin\\varphi$: en la elipse meridiana el semieje vertical '
                                          'es $b$.',
                                 'correcta': False,
                                 'explicacion': '$z = b\\sin\\beta$ vale con la latitud reducida $\\beta$, '
                                                'la de la circunferencia auxiliar, no con la geodésica '
                                                '$\\varphi$; con $\\varphi$ hace falta el denominador '
                                                '$\\sqrt{1 - e^2\\sin^2\\varphi}$.'},
                                {'id': 'd',
                                 'texto': '$Z = M\\sin\\varphi$, porque la coordenada vertical sigue al '
                                          'meridiano.',
                                 'correcta': False,
                                 'explicacion': '$M$ es el radio de curvatura del meridiano, un radio '
                                                'osculador, no una distancia desde ningún eje; la conversión '
                                                'usa $N$ y el factor $(1 - e^2)$.'}],
                   'rubrica': 'propuesta: Elipsoide · avanzado · conversión $(\\varphi, \\lambda, h) \\to '
                              '(X, Y, Z)$; hecho geométrico: la normal corta el eje polar debajo del '
                              'centro'}],
 '14_trigonometria_esferica': [{'id': '14_e1',
                                'nivel': 'elemental',
                                'enunciado': 'Tomamos tres vértices $A$, $B$, $C$ sobre la esfera unitaria '
                                             'como vectores desde el centro. ¿Qué es el lado $a$ del '
                                             'triángulo esférico, opuesto a $A$?',
                                'opciones': [{'id': 'a',
                                              'texto': 'El segmento recto entre $B$ y $C$, de largo $\\lVert '
                                                       'B - C\\rVert$.',
                                              'correcta': False,
                                              'explicacion': 'La cuerda atraviesa la esfera; el lado va por '
                                                             'la superficie, y lo que se mide es el ángulo '
                                                             'central, no el largo de la cuerda.'},
                                             {'id': 'b',
                                              'texto': 'El arco de círculo máximo entre $B$ y $C$, medido '
                                                       'por el ángulo central: $\\cos a = \\langle B, '
                                                       'C\\rangle$.',
                                              'correcta': True,
                                              'explicacion': 'El círculo máximo es el corte con el plano por '
                                                             'el centro y los dos vértices, la geodésica de '
                                                             'la esfera; nada mide en metros, y sobre radio '
                                                             '$R$ el arco mide $R\\,a$.'},
                                             {'id': 'c',
                                              'texto': 'El arco del paralelo que une $B$ y $C$.',
                                              'correcta': False,
                                              'explicacion': 'Un paralelo no es círculo máximo (salvo el '
                                                             'ecuador) ni camino más corto; los lados de un '
                                                             'triángulo esférico son geodésicas.'},
                                             {'id': 'd',
                                              'texto': 'El ángulo entre los planos $OAB$ y $OAC$.',
                                              'correcta': False,
                                              'explicacion': 'Ese diedro es el ángulo del triángulo en el '
                                                             'vértice $A$, no el lado; el lado es un ángulo '
                                                             'entre vectores, el ángulo es uno entre '
                                                             'planos.'}],
                                'rubrica': 'Productos, determinante y autovectores · elemental: el producto '
                                           'interno decide incidencia y ortogonalidad, el vectorial une dos '
                                           'puntos (lado = producto interno, ángulo = normales)'},
                               {'id': '14_e2',
                                'nivel': 'elemental',
                                'enunciado': 'Medimos los tres ángulos de un triángulo con lados geodésicos '
                                             'sobre la esfera. ¿Por qué suman más de $180°$?',
                                'opciones': [{'id': 'a',
                                              'texto': 'Por el error de los instrumentos: en una esfera '
                                                       'perfecta sumarían $180°$.',
                                              'correcta': False,
                                              'explicacion': 'El sobrante es geometría, no error: con lados '
                                                             "de $100$ km son unos $22''$, repetibles y "
                                                             'proporcionales al área, que no se compensan '
                                                             'como error.'},
                                             {'id': 'b',
                                              'texto': 'Porque la curvatura es positiva: el triángulo '
                                                       'abomba, los ángulos se abren y el sobrante es el '
                                                       'área, $A + B + C - \\pi = \\text{área}/R^2$.',
                                              'correcta': True,
                                              'explicacion': 'Es el teorema de Girard; en una silla de '
                                                             'montar, con $K < 0$, pasa lo contrario y hay '
                                                             'defecto. El octante, con tres ángulos rectos, '
                                                             'suma $270°$ y cubre un octavo de la esfera.'},
                                             {'id': 'c',
                                              'texto': 'Porque los lados se miden en grados y no en metros, '
                                                       'y eso infla los ángulos.',
                                              'correcta': False,
                                              'explicacion': 'Medir los lados como ángulos centrales es una '
                                                             'convención que no afecta a los ángulos del '
                                                             'triángulo; el exceso aparece igual en metros.'},
                                             {'id': 'd',
                                              'texto': 'Suman siempre $270°$, como el triángulo con tres '
                                                       'ángulos rectos.',
                                              'correcta': False,
                                              'explicacion': '$270°$ es sólo el octante; el exceso crece con '
                                                             'el área, y un triángulo de pocos km suma '
                                                             '$180°$ más una fracción de segundo.'}],
                                'rubrica': 'propuesta: Trigonometría esférica · elemental · exceso esférico '
                                           '= área$/R^2$ (Girard); hecho geométrico: el triángulo abomba y '
                                           'los ángulos se abren'},
                               {'id': '14_m1',
                                'nivel': 'medio',
                                'enunciado': 'Un triángulo esférico sobre la esfera de radio $R$ tiene '
                                             'ángulos $100°$, $60°$ y $50°$. ¿Qué área tiene?',
                                'opciones': [{'id': 'a',
                                              'texto': '$\\tfrac{7\\pi}{6} R^2$.',
                                              'correcta': False,
                                              'explicacion': 'Es la suma de los ángulos ($210°$) pasada a '
                                                             'radianes; el área sale del exceso, lo que '
                                                             'sobra de $180°$, no de la suma entera.'},
                                             {'id': 'b',
                                              'texto': '$\\tfrac{\\pi}{6} R^2$.',
                                              'correcta': True,
                                              'explicacion': 'La suma es $210°$, el exceso $30° = \\pi/6$ '
                                                             'rad, y por Girard área $= \\varepsilon R^2$; '
                                                             'es $1/24$ de la esfera entera.'},
                                             {'id': 'c',
                                              'texto': '$30\\,R^2$.',
                                              'correcta': False,
                                              'explicacion': 'El exceso está bien ($30°$) pero quedó en '
                                                             'grados: la fórmula de Girard pide radianes, y '
                                                             '$30\\,R^2$ sería más que la esfera entera.'},
                                             {'id': 'd',
                                              'texto': '$\\tfrac{\\pi}{2} R^2$.',
                                              'correcta': False,
                                              'explicacion': 'Ese es el octante, de exceso $90°$; acá el '
                                                             'exceso es $30°$, un tercio.'}],
                                'rubrica': 'propuesta: Trigonometría esférica · medio · cuenta del exceso y '
                                           'del área con el control del octante'},
                               {'id': '14_m2',
                                'nivel': 'medio',
                                'enunciado': 'Triángulo esférico con $b = c = 60°$ y ángulo $A = 90°$. Con '
                                             'la ley del coseno, ¿cuánto vale $\\cos a$?',
                                'opciones': [{'id': 'a',
                                              'texto': '$\\cos a = \\tfrac14$: $\\cos 60°\\cos 60° + \\sin '
                                                       '60°\\sin 60°\\cos 90°$.',
                                              'correcta': True,
                                              'explicacion': 'El término con $\\cos A$ se anula y queda '
                                                             '$\\cos^2 60° = 1/4$, $a \\approx 75{,}5°$; es '
                                                             'un producto interno, $\\langle B, C\\rangle$, '
                                                             'con los dos vértices a $60°$ del polo en '
                                                             'meridianos perpendiculares.'},
                                             {'id': 'b',
                                              'texto': '$\\cos a = 0$: con $A = 90°$ el lado opuesto también '
                                                       'es recto.',
                                              'correcta': False,
                                              'explicacion': 'Eso pasa si $b$ o $c$ valen $90°$ (por ejemplo '
                                                             'en el octante); con $b = c = 60°$ queda el '
                                                             'producto $\\cos b\\cos c \\ne 0$.'},
                                             {'id': 'c',
                                              'texto': '$\\cos a \\approx 0{,}09$: en el triángulo '
                                                       'rectángulo $a^2 = b^2 + c^2$ da $a = 60°\\sqrt{2} '
                                                       '\\approx 85°$.',
                                              'correcta': False,
                                              'explicacion': 'Pitágoras es el límite plano de la ley del '
                                                             'coseno para lados chicos; a $60°$ de lado la '
                                                             'esfera ya no es plana y la cuenta exacta da '
                                                             '$\\cos a = 1/4$, $a \\approx 75{,}5°$, no '
                                                             '$85°$.'},
                                             {'id': 'd',
                                              'texto': '$\\cos a = 1$: $\\cos 60°\\cos 60° + \\sin 60°\\sin '
                                                       '60°$.',
                                              'correcta': False,
                                              'explicacion': 'Falta el $\\cos A$ en el segundo término; sin '
                                                             'él sale $\\cos(b - c) = 1$, que no es el lado; '
                                                             'con $A = 90°$ el segundo término se anula.'}],
                                'rubrica': 'Productos, determinante y autovectores · elemental: el producto '
                                           'interno decide ángulos (la ley del coseno es $\\langle B, '
                                           'C\\rangle$ con los vértices en coordenadas)'},
                               {'id': '14_a1',
                                'nivel': 'avanzado',
                                'enunciado': 'Cerramos una poligonal de cinco lados geodésicos sobre la '
                                             'esfera de radio $R$. ¿Cuánto suman sus ángulos interiores?',
                                'opciones': [{'id': 'a',
                                              'texto': '$540°$ exactos, como en el plano: el exceso aparece '
                                                       'sólo en triángulos.',
                                              'correcta': False,
                                              'explicacion': 'Cortado en tres triángulos, cada uno aporta su '
                                                             'exceso; la suma total es $540°$ más el área '
                                                             'total sobre $R^2$.'},
                                             {'id': 'b',
                                              'texto': '$540° + \\text{área}/R^2$, porque $\\sum '
                                                       '\\text{ángulos} - (n - 2)\\pi = \\text{área}/R^2$.',
                                              'correcta': True,
                                              'explicacion': 'Se corta en $n - 2 = 3$ triángulos por '
                                                             'diagonales geodésicas y se suman los excesos '
                                                             'de Girard; por eso un cuadrilátero con cuatro '
                                                             'ángulos rectos es imposible sobre la esfera: '
                                                             'sumaría $360° + \\text{área}/R^2 > 360°$.'},
                                             {'id': 'c',
                                              'texto': '$540° + 3\\,\\text{área}/R^2$: un exceso por cada '
                                                       'triángulo del corte.',
                                              'correcta': False,
                                              'explicacion': 'Cada triángulo aporta el exceso de su propia '
                                                             'área, y las tres áreas suman la del polígono; '
                                                             'no se multiplica por el número de triángulos.'},
                                             {'id': 'd',
                                              'texto': '$180° + \\text{área}/R^2$, porque el exceso no '
                                                       'depende del número de lados.',
                                              'correcta': False,
                                              'explicacion': 'El exceso no depende del número de lados, pero '
                                                             'la parte plana sí: $(n - 2)\\cdot 180°$, que '
                                                             'para cinco lados es $540°$.'}],
                                'rubrica': 'propuesta: Trigonometría esférica · avanzado · polígono '
                                           'geodésico, $\\sum\\text{ángulos} - (n-2)\\pi = $ área$/R^2$; '
                                           'hecho geométrico: no hay cuadrilátero de cuatro rectos'},
                               {'id': '14_a2',
                                'nivel': 'avanzado',
                                'enunciado': 'Medimos los tres ángulos de un triángulo de $100$ km de lado '
                                             "sobre la Tierra ($R = 6371$ km) y suman $180° 00' 22''$. ¿Qué "
                                             'concluimos?',
                                'opciones': [{'id': 'a',
                                              'texto': "Los $22''$ son error angular de cierre y hay que "
                                                       'repartirlo entre los tres ángulos como error de '
                                                       'medición.',
                                              'correcta': False,
                                              'explicacion': 'Repartirlos como error borra geometría real: '
                                                             'el exceso de un triángulo equilátero de $100$ '
                                                             'km es $\\text{área}/R^2 \\approx 4330/6371^2 '
                                                             '\\approx 1{,}07\\cdot10^{-4}$ rad, justo '
                                                             "$22''$."},
                                             {'id': 'b',
                                              'texto': "Los $22''$ son el exceso esférico esperado: no hay "
                                                       'error de cierre que compensar, y para calcularlo '
                                                       'como plano se resta $\\varepsilon/3$ a cada ángulo.',
                                              'correcta': True,
                                              'explicacion': 'El área sobre $R^2$ da exactamente esos '
                                                             "$22''$, así que las mediciones cierran; "
                                                             'Legendre resuelve el triángulo chico como '
                                                             'plano con los ángulos reducidos en un tercio '
                                                             'del exceso cada uno.'},
                                             {'id': 'c',
                                              'texto': 'El triángulo es demasiado chico para tener exceso '
                                                       "medible: los $22''$ son error grosero.",
                                              'correcta': False,
                                              'explicacion': 'Con $1$ km de lado el exceso es de '
                                                             "$0{,}002''$, invisible; con $100$ km el área "
                                                             'es $10^4$ veces mayor y el exceso ya es del '
                                                             'orden de lo que mide un teodolito.'},
                                             {'id': 'd',
                                              'texto': "Hay que restar $22''$ a un solo ángulo, el del "
                                                       'vértice más alejado.',
                                              'correcta': False,
                                              'explicacion': 'El exceso no es de un vértice sino del '
                                                             'triángulo entero; Legendre lo reparte en '
                                                             'partes iguales porque para lados chicos el '
                                                             'triángulo es casi equilátero en su efecto.'}],
                                'rubrica': 'Rotaciones · avanzado: ir a lo chico para volver a lo grande (el '
                                           'triángulo chico se calcula como plano una vez separado el '
                                           'exceso)'}],
 '15_transformaciones_conformes': [{'id': '15_e1',
                                    'nivel': 'elemental',
                                    'enunciado': 'Decimos que una proyección del elipsoide al plano es '
                                                 'conforme. ¿Qué conserva exactamente?',
                                    'opciones': [{'id': 'a',
                                                  'texto': 'Las distancias entre puntos cercanos, con un '
                                                           'error que crece con la latitud.',
                                                  'correcta': False,
                                                  'explicacion': 'Ninguna proyección conserva distancias '
                                                                 '(theorema egregium); la conforme cambia la '
                                                                 'escala $k(P)$ de punto a punto y la paga '
                                                                 'explícitamente.'},
                                                 {'id': 'b',
                                                  'texto': 'Los ángulos entre curvas y su orientación; la '
                                                           'escala cambia de un punto a otro.',
                                                  'correcta': True,
                                                  'explicacion': 'Con lupa infinitesimal es una similaridad '
                                                                 'directa, $J = k(P)\\,R(\\theta)$: un '
                                                                 'cuadradito del terreno va a un cuadradito '
                                                                 'girado y escalado, y dos visuales a $90°$ '
                                                                 'siguen a $90°$ en la hoja.'},
                                                 {'id': 'c',
                                                  'texto': 'Las áreas: una hectárea del terreno es una '
                                                           'hectárea en el mapa.',
                                                  'correcta': False,
                                                  'explicacion': 'Conservar áreas es $\\det J = hk = 1$, la '
                                                                 'proyección equivalente; en Mercator a '
                                                                 '$-54°$ cada hectárea se dibuja como '
                                                                 '$2{,}88$ y los ángulos salen exactos.'},
                                                 {'id': 'd',
                                                  'texto': 'Los ángulos sólo entre meridianos y paralelos, '
                                                           'que siguen a $90°$.',
                                                  'correcta': False,
                                                  'explicacion': 'Meridianos y paralelos a $90°$ es sólo $F '
                                                                 '= 0$; la cilíndrica equidistante lo cumple '
                                                                 'y tuerce las demás direcciones hasta $30°$ '
                                                                 'en Ushuaia. Conforme pide además $E = '
                                                                 'G$.'}],
                                    'rubrica': 'Rotaciones · medio: hay transformaciones que se definen '
                                               'completamente por qué propiedades de los objetos '
                                               'transformados mantienen (la conforme, por los ángulos)'},
                                   {'id': '15_e2',
                                    'nivel': 'elemental',
                                    'enunciado': '¿Cuál de estas matrices puede ser el Jacobiano de una '
                                                 'transformación conforme en un punto, es decir, que '
                                                 'conserva ángulos y orientación (directa)?',
                                    'opciones': [{'id': 'a',
                                                  'texto': '$\\begin{pmatrix} 2 & 0 \\\\ 0 & 1 '
                                                           '\\end{pmatrix}$',
                                                  'correcta': False,
                                                  'explicacion': 'Es una afinidad que estira un eje y no el '
                                                                 'otro: $\\sigma_1 = 2 \\ne \\sigma_2 = 1$, '
                                                                 'el círculo de Tissot se vuelve elipse y '
                                                                 'las direcciones a $45°$ giran.'},
                                                 {'id': 'b',
                                                  'texto': '$\\begin{pmatrix} 3 & 4 \\\\ 4 & -3 '
                                                           '\\end{pmatrix}$',
                                                  'correcta': False,
                                                  'explicacion': 'Conserva el tamaño de los ángulos '
                                                                 '($J^\\top J = 25 I$) pero $\\det J = -25 < '
                                                                 '0$: es un espejo por una homotecia, '
                                                                 'invierte la orientación y las proyecciones '
                                                                 'se toman directas.'},
                                                 {'id': 'c',
                                                  'texto': '$\\begin{pmatrix} 3 & -4 \\\\ 4 & 3 '
                                                           '\\end{pmatrix}$',
                                                  'correcta': True,
                                                  'explicacion': 'Tiene la forma $\\begin{pmatrix} a & -b '
                                                                 '\\\\ b & a \\end{pmatrix}$ de multiplicar '
                                                                 'por el complejo $3 + 4i$: $J^\\top J = 25 '
                                                                 'I$, escala $5$, giro $\\arctan(4/3)$, y '
                                                                 '$\\det J = 25 > 0$.'},
                                                 {'id': 'd',
                                                  'texto': '$\\begin{pmatrix} 1 & 0{,}5 \\\\ 0 & 1 '
                                                           '\\end{pmatrix}$',
                                                  'correcta': False,
                                                  'explicacion': 'Es un corte: conserva áreas ($\\det = 1$) '
                                                                 'pero inclina el eje $y$, así que el ángulo '
                                                                 'recto entre los ejes deja de serlo.'}],
                                    'rubrica': 'Rotaciones · medio: hay una equivalencia entre operaciones '
                                               'en $\\mathbb{C}$ y en $\\mathbb{R}^2$ (multiplicar por $a + '
                                               'ib$ es la matriz $[[a, -b], [b, a]]$)'},
                                   {'id': '15_m1',
                                    'nivel': 'medio',
                                    'enunciado': 'En un punto, el Jacobiano de una proyección tiene valores '
                                                 'singulares $\\sigma_1 = 2$ y $\\sigma_2 = 1$. ¿Cuál es la '
                                                 'deformación angular máxima $\\omega_{\\max}$?',
                                    'opciones': [{'id': 'a',
                                                  'texto': '$\\omega_{\\max} = \\arcsin\\tfrac13 \\approx '
                                                           '19{,}5°$.',
                                                  'correcta': False,
                                                  'explicacion': '$\\arcsin\\frac{\\sigma_1 - '
                                                                 '\\sigma_2}{\\sigma_1 + \\sigma_2}$ es el '
                                                                 'giro máximo de una sola dirección; la '
                                                                 'simétrica gira lo mismo al revés, y el '
                                                                 'ángulo entre ambas cambia el doble.'},
                                                 {'id': 'b',
                                                  'texto': '$\\omega_{\\max} = 2\\arcsin\\tfrac13 \\approx '
                                                           '38{,}9°$.',
                                                  'correcta': True,
                                                  'explicacion': '$\\omega_{\\max} = '
                                                                 '2\\arcsin\\frac{\\sigma_1 - '
                                                                 '\\sigma_2}{\\sigma_1 + \\sigma_2} = '
                                                                 '2\\arcsin\\frac{1}{3}$; la indicatriz de '
                                                                 'Tissot es una elipse de semiejes $2$ y $1$ '
                                                                 'y las direcciones que más giran son '
                                                                 'simétricas respecto de su diagonal.'},
                                                 {'id': 'c',
                                                  'texto': '$\\omega_{\\max} = 2\\arcsin\\tfrac12 = 60°$.',
                                                  'correcta': False,
                                                  'explicacion': 'Se usó el cociente $\\sigma_2/\\sigma_1 = '
                                                                 '1/2$ en lugar de $(\\sigma_1 - '
                                                                 '\\sigma_2)/(\\sigma_1 + \\sigma_2) = 1/3$; '
                                                                 'con $r = 1/2$ la fórmula correcta da '
                                                                 '$38{,}9°$.'},
                                                 {'id': 'd',
                                                  'texto': '$\\omega_{\\max} = 0°$: el Jacobiano es diagonal '
                                                           'y conserva el ángulo entre los ejes.',
                                                  'correcta': False,
                                                  'explicacion': 'Los ejes siguen a $90°$ pero las '
                                                                 'direcciones intermedias giran; conforme es '
                                                                 '$\\sigma_1 = \\sigma_2$, no sólo $F = '
                                                                 '0$.'}],
                                    'rubrica': 'Cambio de base y SVD · medio: la SVD gira, estira en '
                                               'direcciones perpendiculares y gira; la indicatriz de Tissot '
                                               'es esa elipse y $\\omega_{\\max}$ sale de $\\sigma_1, '
                                               '\\sigma_2$'},
                                   {'id': '15_m2',
                                    'nivel': 'medio',
                                    'enunciado': 'Calculamos la latitud isométrica en el ecuador, $q(0)$, '
                                                 'con $q(\\varphi) = \\ln\\tan\\!\\left(\\tfrac{\\pi}{4} + '
                                                 '\\tfrac{\\varphi}{2}\\right) - \\tfrac{e}{2}\\ln\\tfrac{1 '
                                                 '+ e\\sin\\varphi}{1 - e\\sin\\varphi}$. ¿Cuánto da?',
                                    'opciones': [{'id': 'a',
                                                  'texto': '$q(0) = 1$.',
                                                  'correcta': False,
                                                  'explicacion': '$\\tan(\\pi/4) = 1$, pero falta el '
                                                                 'logaritmo: $\\ln 1 = 0$.'},
                                                 {'id': 'b',
                                                  'texto': '$q(0) = \\pi/4$.',
                                                  'correcta': False,
                                                  'explicacion': 'Se quedó en el argumento de la tangente; '
                                                                 '$q$ es el logaritmo de la tangente de ese '
                                                                 'ángulo, y $\\ln\\tan(\\pi/4) = 0$.'},
                                                 {'id': 'c',
                                                  'texto': '$q(0) = 0$.',
                                                  'correcta': True,
                                                  'explicacion': '$\\ln\\tan(\\pi/4) = \\ln 1 = 0$ y la '
                                                                 'corrección elipsoidal lleva $\\ln\\frac{1 '
                                                                 '+ 0}{1 - 0} = 0$; Mercator pone el ecuador '
                                                                 'en $y = a\\,q = 0$ y $q$ es impar, '
                                                                 '$q(-\\varphi) = -q(\\varphi)$.'},
                                                 {'id': 'd',
                                                  'texto': '$q(0) = -e/2$.',
                                                  'correcta': False,
                                                  'explicacion': 'La corrección del elipsoide se anula en el '
                                                                 'ecuador porque $\\sin 0 = 0$ deja $\\ln '
                                                                 '1$; el $-e/2$ sólo multiplica ese '
                                                                 'logaritmo.'}],
                                    'rubrica': 'propuesta: Conformes · medio · Mercator es $y = '
                                               'a\\,q(\\varphi)$ con $h = k$; hecho geométrico: el ecuador '
                                               'queda en $y = 0$ y el mapa es simétrico'},
                                   {'id': '15_a1',
                                    'nivel': 'avanzado',
                                    'enunciado': 'En Mercator la escala a lo largo del paralelo es $k = '
                                                 'a/(N\\cos\\varphi)$ y la condición conforme es $h = k$. '
                                                 '¿Por qué el mapa estira hacia los polos y no llega a '
                                                 'dibujarlos?',
                                    'opciones': [{'id': 'a',
                                                  'texto': 'Porque $x = a\\lambda$ dibuja todos los '
                                                           'paralelos con el largo del ecuador, y para '
                                                           'seguir conforme el meridiano se estira lo mismo: '
                                                           '$dy/d\\varphi = aM/(N\\cos\\varphi) \\to '
                                                           '\\infty$ cuando $\\varphi \\to 90°$.',
                                                  'correcta': True,
                                                  'explicacion': 'El paralelo real mide $N\\cos\\varphi$ por '
                                                                 'radián ($0{,}59\\,M$ en $-54°$, cero en el '
                                                                 'polo) y en la hoja mide $a$; $k$ crece sin '
                                                                 'cota y $h = k$ obliga a $y = '
                                                                 'a\\,q(\\varphi)$ con $q \\to \\infty$. A '
                                                                 '$-54°$ cada metro ya son $1{,}70$ en el '
                                                                 'mapa.'},
                                                 {'id': 'b',
                                                  'texto': 'Porque $M$ crece del ecuador al polo y el '
                                                           'meridiano se dibuja a escala verdadera, $h = 1$.',
                                                  'correcta': False,
                                                  'explicacion': '$h = 1$ es la cilíndrica equidistante, que '
                                                                 'llega al polo en $y = S(90°)$ finito; y '
                                                                 '$M$ varía apenas un $1\\,\\%$, no explica '
                                                                 'un estiramiento infinito.'},
                                                 {'id': 'c',
                                                  'texto': 'Porque la latitud isométrica $q$ lleva la '
                                                           'corrección $-\\tfrac{e}{2}\\ln\\tfrac{1 + '
                                                           'e\\sin\\varphi}{1 - e\\sin\\varphi}$, que '
                                                           'diverge en el polo.',
                                                  'correcta': False,
                                                  'explicacion': 'Esa corrección es acotada ($e \\approx '
                                                                 '0{,}08$); la que diverge es la parte '
                                                                 'esférica $\\ln\\tan(\\pi/4 + \\varphi/2)$, '
                                                                 'y pasa también con $e = 0$.'},
                                                 {'id': 'd',
                                                  'texto': 'Porque conserva áreas: lo que el paralelo se '
                                                           'estira el meridiano se aplasta, $hk = 1$, y '
                                                           'cerca del polo ya no cabe nada.',
                                                  'correcta': False,
                                                  'explicacion': '$hk = 1$ es la cilíndrica equivalente, que '
                                                                 'aplasta los polos contra $y = \\pm R$ en '
                                                                 'la esfera; Mercator hace lo contrario, $hk '
                                                                 '= k^2 \\to \\infty$.'}],
                                    'rubrica': 'propuesta: Conformes · avanzado · $h = k$ con $k = '
                                               'a/(N\\cos\\varphi)$: por qué Mercator estira hacia los '
                                               'polos; hecho geométrico: círculos de Tissot que crecen pero '
                                               'siguen círculos'},
                                   {'id': '15_a2',
                                    'nivel': 'avanzado',
                                    'enunciado': 'Queremos la proyección de POSGAR (Gauss-Krüger): conforme '
                                                 'y sin deformación sobre el meridiano central de la faja. '
                                                 'Con las cuatro caras de lo conforme, ¿cómo la planteamos?',
                                    'opciones': [{'id': 'a',
                                                  'texto': 'Como $w = f(q + i\\,\\Delta\\lambda)$ con $f$ '
                                                           'analítica y $f(q) = S(\\varphi)$ sobre el eje '
                                                           'real: la grilla $(\\lambda, q)$ ya es conforme y '
                                                           'la condición en el meridiano central fija $f$.',
                                                  'correcta': True,
                                                  'explicacion': 'Cara D: toda función analítica es '
                                                                 'conforme, y una analítica real sobre el '
                                                                 'eje real queda determinada por sus valores '
                                                                 'ahí; Taylor en $i\\,\\Delta\\lambda$ da $E '
                                                                 '\\approx N\\cos\\varphi\\,\\Delta\\lambda$ '
                                                                 'y una escala $1 + '
                                                                 '\\tfrac12\\cos^2\\varphi\\,\\Delta\\lambda^2$, '
                                                                 'que vale $1$ sobre el meridiano central.'},
                                                 {'id': 'b',
                                                  'texto': 'Como Mercator girado $90°$: $x = '
                                                           'a\\,q(\\varphi)$ e $y = a\\lambda$, con el '
                                                           'cilindro tangente a un meridiano.',
                                                  'correcta': False,
                                                  'explicacion': 'Intercambiar los ejes es una similaridad y '
                                                                 'la proyección sigue siendo Mercator, con '
                                                                 'escala $1$ sobre el ecuador y no sobre el '
                                                                 'meridiano central; girar el cilindro exige '
                                                                 'rehacer la cuenta en $\\varphi$ y '
                                                                 '$\\Delta\\lambda$.'},
                                                 {'id': 'c',
                                                  'texto': 'Como $w = f(\\varphi + i\\,\\Delta\\lambda)$ con '
                                                           '$f$ analítica: cualquier grilla ortogonal sirve '
                                                           'de partida.',
                                                  'correcta': False,
                                                  'explicacion': 'La grilla $(\\lambda, \\varphi)$ es '
                                                                 'ortogonal ($F = 0$) pero no conforme ($E = '
                                                                 'M^2 \\ne G = N^2\\cos^2\\varphi$); '
                                                                 'analítica sobre una grilla no conforme no '
                                                                 'da conforme. Hace falta $q$, con $ds^2 = '
                                                                 'N^2\\cos^2\\varphi\\,(dq^2 + '
                                                                 'd\\lambda^2)$.'},
                                                 {'id': 'd',
                                                  'texto': 'Pidiendo $h = 1$ en toda la faja, como la '
                                                           'cilíndrica equidistante pero con el eje en el '
                                                           'meridiano central.',
                                                  'correcta': False,
                                                  'explicacion': '$h = 1$ en todo punto con $k \\ne 1$ no es '
                                                                 'conforme; la escala $1$ sólo puede '
                                                                 'exigirse sobre el meridiano central y '
                                                                 'crece con $\\Delta\\lambda^2$, por eso las '
                                                                 'fajas de POSGAR son angostas.'}],
                                    'rubrica': 'Rotaciones · elemental: derivar funciones con números '
                                               'complejos sigue las mismas reglas que los reales '
                                               '(Gauss-Krüger como función analítica de $q + '
                                               'i\\,\\Delta\\lambda$)'}]}
