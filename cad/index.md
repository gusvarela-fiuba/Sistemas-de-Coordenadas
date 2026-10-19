# Laboratorio CAD: cada comando es una transformación

Un programa de dibujo técnico (LibreCAD, QCAD o AutoCAD; acá, el CAD) guarda cada figura como una lista de coordenadas, y cada comando de edición es una transformación que recalcula esa lista: `ROTATE` es una rotación, `MOVE` una traslación, `MIRROR` una reflexión, `SCALE` una homotecia, `ALIGN` un movimiento rígido o una similaridad, un bloque insertado con escala en $x$ distinta de la escala en $y$ una afinidad, y `STRETCH` no es una sola transformación afín. Para qué sirve: lo que se hace con lápiz en el apunte se puede probar sobre un dibujo de verdad y comparar número a número.

Cómo se usa:

1. Descargá el DXF del ejercicio y abrilo en LibreCAD, QCAD o AutoCAD. Si no se ve nada, hacé un zoom a la extensión del dibujo.
2. Aplicá el comando que pide el ejercicio.
3. Guardá el resultado como DXF (R2000 o R12) con otro nombre.
4. Corré `que_matriz.py` sobre el original y tu resultado, y compará con lo que debería dar.

Todos los ejercicios usan la misma parcela, en metros: $A=(10,10)$, $B=(34,17)$, $C=(40,36)$, $D=(24,38)$ y $E=(6,32)$, con el lado $AB$ de 25 m. Cada DXF trae la parcela como polilínea cerrada (capa `PARCELA`), un punto por vértice (capa `VERTICES`), las letras de los vértices (capa `ETIQUETAS`) y los ejes este y norte (capa `EJES`). Describimos el flujo de AutoCAD y, cuando difiere, cómo se hace en LibreCAD.

## Instrucciones de `que_matriz.py`

Desde la raíz del repositorio:

```
uv run python tools/cad/que_matriz.py original.dxf transformado.dxf
```

Empareja los vértices de los dos archivos por su letra y busca la transformación afín $p' = Mp + t$ que lleva unos a otros. Informa la matriz $M$, la traslación $t$, el determinante de $M$, el residuo (la distancia que queda, en media cuadrática, entre lo que da la fórmula y los puntos del dibujo), la familia más chica que explica el cambio (identidad, traslación, rotación, reflexión, movimiento rígido, similaridad, afinidad o no afín) y su lectura geométrica: el ángulo y el centro de una rotación, el eje de una reflexión, el factor de escala de una similaridad.

- `--tol` cambia el umbral de residuo por encima del cual informa «no afín» (por defecto, 0,005 m).
- `--json` da la misma salida en JSON, para usarla desde otro programa.
- Si faltan letras para emparejar, termina con código 2: hacen falta tres vértices no alineados con la misma letra en los dos archivos.

Atención: al transformar, seleccioná **todo** lo de la parcela, la polilínea, los puntos y las letras. Si movés solo la polilínea, los puntos y las letras quedan donde estaban y el resultado sale como la identidad. Si trabajaste sobre una copia, borrá el original antes de guardar: las letras no pueden repetirse.

## Capítulo 1

Rotaciones (capítulo 1 del apunte, sección «En el CAD»).

### `ROTATE` con punto base: la rotación alrededor de un centro

Girar con un punto base es la rotación $\rho_{c,\theta}(p)=c+R(\theta)(p-c)$ de la sección «Rotaciones en el plano», con $c=A$ y $\theta=30^\circ$.

1. Abrí [`cap01_rotate.dxf`](dxf/cap01_rotate.dxf) y seleccioná la polilínea, los puntos y las letras.
2. Rotá con `ROTATE`, punto base $A$ y ángulo 30 (en LibreCAD, `Modify` → `Rotate`: elegís los objetos, el centro y el ángulo).
3. Listá las coordenadas de los vértices con `LIST` o con `ID` (en LibreCAD, con el enganche a extremos activado, la barra de estado muestra las coordenadas del punto bajo el cursor).
4. Calculá $c+R(30^\circ)(p-c)$ para $B$ y compará.

Qué debería dar: $A$ quieto en $(10,10)$, $B'=(27{,}285;\ 28{,}062)$ y $C'=(22{,}981;\ 47{,}517)$. En coordenadas homogéneas es una sola matriz,

$$H_{A,30^\circ}=\begin{pmatrix}0{,}866&-0{,}500&6{,}340\\0{,}500&0{,}866&-3{,}660\\0&0&1\end{pmatrix},\qquad \det R(30^\circ)=1.$$

Respuesta: [`esperado/cap01_rotate_30.dxf`](dxf/esperado/cap01_rotate_30.dxf).

### `ROTATE` frente a `UCS`: lectura activa y pasiva

Rotar el objeto es la lectura activa; rotar el sistema de coordenadas y dejar el objeto quieto es la pasiva (sección «El punto y sus coordenadas no son lo mismo»).

1. Abrí [`cap01_ucs.dxf`](dxf/cap01_ucs.dxf).
2. Rotá la parcela $30^\circ$ alrededor del origen con `ROTATE` y listá sus vértices con `ID`. Deshacé el giro.
3. Rotá el sistema: `UCS`, opción `Z`, ángulo 30. La parcela no se mueve.
4. Listá de nuevo los vértices con `ID`: ahora salen en el sistema rotado.

Qué debería dar: en la lectura activa $A$ pasa a $(3{,}660;\ 13{,}660)$ y la matriz es $R(30^\circ)$; en la pasiva $A$ se lee $(13{,}660;\ 3{,}660)$ y la matriz es $R(-30^\circ)=R(30^\circ)^T$: el mismo giro con el signo cambiado. LibreCAD no tiene `UCS`: ahí la lectura pasiva se hace a mano, multiplicando las coordenadas por $R(-30^\circ)$, o rotando solo la vista, que cambia el dibujo en pantalla pero no las coordenadas.

Respuestas: [`esperado/cap01_ucs_activa_30.dxf`](dxf/esperado/cap01_ucs_activa_30.dxf) y [`esperado/cap01_ucs_pasiva_30.dxf`](dxf/esperado/cap01_ucs_pasiva_30.dxf).

### `UNITS`: del ángulo matemático al acimut

El archivo trae una línea desde $A$ con acimut $60^\circ$ (el acimut es el ángulo de una dirección contado desde el norte en sentido horario). La caja «Acimut no es $\theta$» del capítulo 1 dice que la misma dirección tiene ángulo matemático $\theta=90^\circ-\mathrm{Az}$, contado desde el este en sentido antihorario.

1. Abrí [`cap01_units.dxf`](dxf/cap01_units.dxf) y listá la línea de la capa `ACIMUT` con `LIST`: el ángulo sale $30^\circ$.
2. Con `UNITS`, poné el cero de los ángulos en el norte y marcá el sentido horario.
3. Listá la misma línea: ahora sale $60^\circ$, el acimut.
4. Volvé `UNITS` a como estaba y reflejá todo el dibujo con `MIRROR` en la recta que pasa por $(0,0)$ y $(10,10)$; listá la línea reflejada: sale $60^\circ$.

Qué debería dar: cambiar el cero del este al norte y el sentido al mismo tiempo es reflejar en la recta $y=x$; la matriz es $\begin{pmatrix}0&1\\1&0\end{pmatrix}$, con determinante $-1$. Por eso cambia el sentido: una reflexión invierte la orientación, y el signo menos de $\theta=90^\circ-\mathrm{Az}$ es esa inversión. En LibreCAD, si no encontrás cómo cambiar el cero y el sentido de los ángulos, hacé la conversión a mano con esa fórmula.

Respuesta: [`esperado/cap01_units_bisectriz.dxf`](dxf/esperado/cap01_units_bisectriz.dxf).

### `ARRAYPOLAR`: componer giros

Seis copias repartidas en la vuelta completa son seis rotaciones $R(60^\circ)^k=R(60^\circ k)$, por la regla $R(\beta)R(\theta)=R(\theta+\beta)$ de la proposición «Propiedades de $R(\theta)$».

1. Abrí [`cap01_arraypolar.dxf`](dxf/cap01_arraypolar.dxf): un triángulo de vértices $(6,2)$, $(9,2)$ y $(7;\ 4{,}5)$.
2. Aplicá `ARRAYPOLAR` con centro en el origen, seis elementos y $360^\circ$ (en LibreCAD, `Modify` → `Rotate` con `Multiple copies`, cinco copias de $60^\circ$).
3. Listá el vértice $(6,2)$ en la primera copia y en la sexta.
4. Para comprobar, dejá solo la primera copia (las letras no pueden repetirse) y guardala.

Qué debería dar: la primera copia es $R(60^\circ)$, con determinante 1, y lleva $(6,2)$ a $(1{,}268;\ 6{,}196)$; la sexta es $R(360^\circ)=I$ y cae sobre el original.

Respuesta: [`esperado/cap01_arraypolar_60.dxf`](dxf/esperado/cap01_arraypolar_60.dxf).

## Capítulo 2

Traslaciones y movimientos rígidos (capítulo 2 del apunte, sección «En el CAD»). `MOVE` es la traslación $\tau_v$ y `ROTATE` con punto base, la rotación del capítulo 1.

### `MOVE` y `ROTATE` frente a `ROTATE` y `MOVE`: el orden importa

1. Abrí [`cap02_move_rotate.dxf`](dxf/cap02_move_rotate.dxf) y seleccioná la polilínea, los puntos y las letras.
2. Trasladá con `MOVE` el vector $(12,4)$ y después rotá con `ROTATE` $90^\circ$ alrededor del origen. Listá $A$ con `ID` y guardá con otro nombre.
3. Volvé al original y hacé lo mismo al revés: primero `ROTATE` $90^\circ$ alrededor del origen, después `MOVE` $(12,4)$. Listá $A$ y guardá.
4. Escribí las dos matrices como producto de la rotación por la traslación, en el orden correcto, y compará con lo listado.

En LibreCAD, el equivalente de los dos comandos está en el menú `Modify`.

Qué debería dar: con $\tau_v$ la traslación de $v=(12,4)$ y $R$ la rotación de $90^\circ$ en el origen, en coordenadas homogéneas de $3\times3$,

$$R\,\tau_v=\begin{pmatrix}0&-1&-4\\1&0&12\\0&0&1\end{pmatrix},\qquad \tau_v\,R=\begin{pmatrix}0&-1&12\\1&0&4\\0&0&1\end{pmatrix}.$$

La primera (primero `MOVE`) lleva $A$ a $(-14,22)$; la segunda (primero `ROTATE`) lo lleva a $(2,14)$. Las dos tienen la misma parte lineal y determinante 1: son rotaciones de $90^\circ$, pero con centros distintos, $(-8,4)$ y $(4,8)$.

Respuestas: [`esperado/cap02_move_rotate.dxf`](dxf/esperado/cap02_move_rotate.dxf) y [`esperado/cap02_rotate_move.dxf`](dxf/esperado/cap02_rotate_move.dxf).

## Capítulo 3

Reflexiones, isometrías y similaridades (capítulo 3 del apunte, sección «En el CAD»). `MIRROR` es la reflexión en una recta, `SCALE` la homotecia y `ALIGN` arma, a partir de dos pares de puntos, un movimiento rígido o una similaridad.

### `MIRROR` dos veces: espejos paralelos y espejos que se cortan

La capa `ESPEJOS` trae las rectas $x=50$, $x=60$, $y=-10$ e $y=x-30$.

1. Abrí [`cap03_mirror.dxf`](dxf/cap03_mirror.dxf), seleccioná la polilínea, los puntos y las letras, y reflejá con `MIRROR` en $x=50$, borrando el original. Listá $A$ con `ID`.
2. Reflejá el resultado en $x=60$ y listá $A$ otra vez.
3. Volvé al original y reflejá primero en $y=-10$ y después en $y=x-30$.
4. Guardá cada resultado con otro nombre y compará.

En LibreCAD, el equivalente está en el menú `Modify`.

Qué debería dar: una sola reflexión en $x=50$ da $M=\begin{pmatrix}-1&0\\0&1\end{pmatrix}$, determinante $-1$, y lleva $A$ a $(90,10)$. Los espejos paralelos, a 10 m uno del otro, dan la traslación de vector $(20,0)$, el doble de la distancia entre ellos (teorema «Dos reflexiones en rectas paralelas componen una traslación»): $A$ termina en $(30,10)$. Los espejos que se cortan en $(20,-10)$ forman $45^\circ$ y dan la rotación de $90^\circ$, el doble del ángulo, alrededor de ese punto (teorema «Dos reflexiones en rectas secantes componen una rotación»): $M=R(90^\circ)$, $t=(10,-30)$ y $A$ termina en $(0,-20)$. En los dos casos el determinante vuelve a ser 1: dos inversiones de la orientación se cancelan.

Respuestas: [`esperado/cap03_mirror_x50.dxf`](dxf/esperado/cap03_mirror_x50.dxf), [`esperado/cap03_mirror_paralelos.dxf`](dxf/esperado/cap03_mirror_paralelos.dxf) y [`esperado/cap03_mirror_cortan.dxf`](dxf/esperado/cap03_mirror_cortan.dxf).

### `ALIGN` y `SCALE`: movimiento rígido frente a similaridad

La capa `DESTINO` trae $A'=(70,10)$ y $B'=(63,34)$, a 25 m entre sí como $A$ y $B$, y $A''=(90,10)$ y $B''=(76,58)$, a 50 m.

1. Abrí [`cap03_align.dxf`](dxf/cap03_align.dxf) y seleccioná la polilínea, los puntos y las letras.
2. Aplicá `ALIGN` con los pares $A\to A'$ y $B\to B'$, y contestá que no al escalado. Guardá con otro nombre.
3. Volvé al original y aplicá `ALIGN` con $A\to A''$ y $B\to B''$, esta vez con escalado. Guardá.
4. Llegá al mismo resultado en dos pasos: `ALIGN` sin escalado con $A\to A''$ y $B$ hacia $B''$, y después `SCALE` con punto base $A''$ y factor 2.

En LibreCAD no hay un `ALIGN` directo: el equivalente está en el menú `Modify`, moviendo, rotando y escalando por separado.

Qué debería dar: sin escala sale un movimiento rígido, $M=R(90^\circ)$, $t=(80,0)$, determinante 1, una rotación de $90^\circ$ alrededor de $(40,40)$. Con escala sale una similaridad de razón 2: $M=2R(90^\circ)=\begin{pmatrix}0&-2\\2&0\end{pmatrix}$, $t=(110,-10)$, determinante 4 (las áreas se multiplican por 4) y centro $(26,42)$; el paso 4 es la descomposición «homotecia después de isometría» del capítulo 3. Con dos pares el `ALIGN` resuelve exacto, porque una similaridad tiene cuatro números libres y dos pares dan cuatro ecuaciones. Con más pares medidos, que nunca encajan perfecto, hace falta un ajuste: elegir la similaridad que deja las menores diferencias en todos los pares a la vez (capítulo «Cuatro problemas de ajuste» del apunte).

Respuestas: [`esperado/cap03_align_rigido.dxf`](dxf/esperado/cap03_align_rigido.dxf) y [`esperado/cap03_align_similaridad.dxf`](dxf/esperado/cap03_align_similaridad.dxf).

## Capítulo 4

Afinidades y coordenadas homogéneas (capítulo 4 del apunte, sección «En el CAD»). Un bloque es una figura guardada una vez que se inserta donde haga falta, con una escala en $x$ y otra en $y$: insertarlo es aplicar la afinidad $f(x)=Ax+b$ con $A=\begin{pmatrix}s_x&0\\0&s_y\end{pmatrix}$.

### Insertar un bloque con escala $x=2$, $y=1$ y con $x=-1$: afinidad no conforme y reflexión

El archivo trae el bloque `PARCELA_BLOQUE`, definido con punto base en el origen.

1. Abrí [`cap04_bloque.dxf`](dxf/cap04_bloque.dxf).
2. Insertá el bloque con `INSERT` en $(0,0)$, con escala 2 en $x$, 1 en $y$ y rotación 0. Guardá con otro nombre.
3. Insertalo de nuevo, ahora con escala $-1$ en $x$ y 1 en $y$. Guardá.
4. Corré `que_matriz.py` sobre cada archivo y mirá el determinante.

En LibreCAD, el equivalente está en el menú de bloques; si tu versión no deja escalas distintas en $x$ y en $y$, hacé este ejercicio en QCAD o AutoCAD.

Qué debería dar: con $x=2$, $y=1$ sale $M=\begin{pmatrix}2&0\\0&1\end{pmatrix}$, determinante 2: el área se duplica y los ángulos cambian, una afinidad que no es conforme (no conserva ángulos). Con $x=-1$ sale $M=\begin{pmatrix}-1&0\\0&1\end{pmatrix}$, determinante $-1$: la reflexión en el eje norte, que conserva distancias e invierte el sentido de giro. Si en el archivo queda también la parcela original, `que_matriz.py` usa los vértices del bloque insertado.

Respuestas: [`esperado/cap04_bloque_x2_y1.dxf`](dxf/esperado/cap04_bloque_x2_y1.dxf) y [`esperado/cap04_bloque_xm1.dxf`](dxf/esperado/cap04_bloque_xm1.dxf).

### `STRETCH`: un contraejemplo

La capa `VENTANA` marca un rectángulo que encierra $C$ y $D$, y deja afuera $A$, $B$ y $E$.

1. Abrí [`cap04_stretch.dxf`](dxf/cap04_stretch.dxf).
2. Aplicá `STRETCH` con una ventana de captura que coincida con la de la capa `VENTANA` y un desplazamiento de $(10,0)$.
3. Comprobá con `ID` que $C$ pasó a $(50,36)$, $D$ a $(34,38)$ y que $A$, $B$ y $E$ no se movieron. Guardá con otro nombre.
4. Corré `que_matriz.py` y leé el residuo.

En LibreCAD, el equivalente está en el menú `Modify`.

Qué debería dar: residuo de 2,527 m, con 3,094 m en $E$, muy por encima del umbral de 0,005 m: «no afín». La razón: $A$, $B$ y $E$ no están alineados y quedaron fijos, y una afinidad queda determinada por la imagen de tres puntos no alineados, así que la única posible es la identidad, que no mueve $C$ ni $D$. El comando mueve unos vértices y deja otros: no entra en ninguna familia del mapa de las transformaciones del capítulo 4.

Respuesta: [`esperado/cap04_stretch_10.dxf`](dxf/esperado/cap04_stretch_10.dxf).

## Capítulo 6

Subespacios, producto cuña y determinante (capítulo 6 del apunte, sección «En el CAD»). `AREA` mide la superficie que encierra una polilínea, y el número que da es el de la fórmula del agrimensor: la mitad de la suma de los cuñas $p_i\wedge p_{i+1}=x_iy_{i+1}-x_{i+1}y_i$ de vértices consecutivos (proposición «Área de un polígono por cuñas»). `SCALE` y un bloque insertado con escalas distintas cambian esa superficie, y el factor es el determinante (proposición «El determinante mide cuánto cambian las áreas»).

### `AREA`: la superficie de la parcela es una suma de cuñas

Cada término $\tfrac12\,p_i\wedge p_{i+1}$ es el área con signo del triángulo que forman el origen y dos vértices consecutivos: positiva si ese triángulo se recorre en sentido antihorario y negativa si se recorre en sentido horario.

1. Abrí [`cap06_area.dxf`](dxf/cap06_area.dxf).
2. Medí la superficie con `AREA`, opción `Object`, eligiendo la polilínea (también la informa `LIST` sobre la polilínea). En LibreCAD, el equivalente es la herramienta de área poligonal del menú de información: marcás los vértices $A$, $B$, $C$, $D$ y $E$ en orden con el enganche a extremos.
3. Calculá a mano los cinco términos $x_iy_{i+1}-x_{i+1}y_i$, de $A$ a $B$, de $B$ a $C$ y así hasta volver de $E$ a $A$, y la mitad de su suma.
4. Repetí la cuenta con el origen en $A$ (restá $A$ a todos los vértices) y compará.

Qué debería dar: el CAD informa un área de 655 m² y un perímetro de 102,384 m. Los cinco términos son $-170$, $544$, $656$, $540$ y $-260$; suman $1310$, y la mitad es $655$ m². La suma sale positiva porque $A$, $B$, $C$, $D$, $E$ están en sentido antihorario; en el orden inverso da $-655$, y el CAD informa el valor absoluto. Los triángulos desde el origen aportan $-85$, $272$, $328$, $270$ y $-130$ m²: los dos negativos son los de los lados $AB$ y $EA$, que cubren la zona entre el origen y la parcela que los otros cuentan de más. Con el origen en $A$ los términos son $0$, $414$, $476$, $420$ y $0$: la suma es otra vez $1310$, porque la superficie no depende de dónde se ponga el origen.

Respuesta: [`esperado/cap06_area_cunas.dxf`](dxf/esperado/cap06_area_cunas.dxf), la misma parcela con los cinco triángulos (capa `CUNAS`) y el área de cada uno; `que_matriz.py` sobre el original y esta respuesta da la identidad y la misma área en los dos archivos.

### `SCALE` e `INSERT`: el área se multiplica por el determinante

El archivo trae la parcela y el bloque `PARCELA_BLOQUE`, definido con punto base en el origen.

1. Abrí [`cap06_scale.dxf`](dxf/cap06_scale.dxf), seleccioná la polilínea, los puntos y las letras, y aplicá `SCALE` con punto base $A$ y factor 2. Medí el área con `AREA` y guardá con otro nombre.
2. Volvé al original e insertá el bloque con `INSERT` en $(0,0)$, con escala 2 en $x$, 1 en $y$ y rotación 0. Medí su área marcando sus cinco vértices con `AREA` y guardá.
3. Antes de mirar el resultado, anticipá: si los lados se duplican en las dos direcciones, ¿por cuánto se multiplica la superficie? ¿Y si se duplican solo en $x$?
4. Corré `que_matriz.py` sobre cada archivo y compará el determinante con el cociente de áreas.

En LibreCAD, `SCALE` está en el menú `Modify`; si tu versión no deja escalas distintas en $x$ y en $y$ para un bloque, hacé el paso 2 en QCAD o AutoCAD.

Qué debería dar: `SCALE` con factor 2 es la homotecia $p\mapsto A+2(p-A)$, con $M=2I$ y $\det M=4$: el área pasa de 655 a 2620 m², cuatro veces más, porque cada cuadradito de la grilla se duplica en ancho y en alto. El bloque con escalas 2 y 1 es $M=\begin{pmatrix}2&0\\0&1\end{pmatrix}$, con $\det M=2$: el área pasa a 1310 m², el doble, aunque los ángulos cambian. En los dos casos `que_matriz.py` informa un cociente de áreas igual a $|\det M|$. Una rotación o una reflexión (determinante $1$ o $-1$) no cambian la superficie.

Respuestas: [`esperado/cap06_scale_2.dxf`](dxf/esperado/cap06_scale_2.dxf) y [`esperado/cap06_bloque_x2_y1_area.dxf`](dxf/esperado/cap06_bloque_x2_y1_area.dxf).

## Capítulo 9

Cambio de base (capítulo 9 del apunte, sección «En el CAD»). `UCS` cambia el sistema de coordenadas con que el CAD lee el dibujo sin mover nada: es la lectura pasiva de una matriz de cambio de base $C$, la que tiene por columnas los vectores de la base nueva.

### `UCS` alineado con el frente: las coordenadas cambian con $C^{-1}$

Imaginá que vas a replantear (marcar en el terreno) construcciones sobre la parcela y que todas las medidas se toman desde el frente $AB$: lo natural es un sistema con origen en $A$, el eje $x$ a lo largo del frente y el eje $y$ perpendicular, hacia adentro. La base nueva es $b_1=(B-A)/25=(0{,}96;\ 0{,}28)$, el versor del frente, y $b_2=(-0{,}28;\ 0{,}96)$, su perpendicular a la izquierda; $C=[\,b_1\mid b_2\,]$ y $\det C=1$. Como la letra $C$ sola es la matriz, al vértice lo nombramos siempre «el vértice $C$».

1. Abrí [`cap09_ucs.dxf`](dxf/cap09_ucs.dxf).
2. Definí el sistema nuevo con `UCS`, dando tres puntos: el origen en $A$, un punto del eje $x$ en $B$ y un punto del lado positivo del eje $y$ en $D$. La parcela no se mueve.
3. Listá con `ID` las coordenadas de los vértices $B$, $C$, $D$ y $E$: ahora salen en el sistema del frente. Medí también el área con `AREA`.
4. Calculá $C^{-1}(p-A)$ para el vértice $C$; como la base es ortonormal, $C^{-1}=C^T$ y cada coordenada nueva es un producto interno, $b_1\cdot(p-A)$ y $b_2\cdot(p-A)$. Compará.
5. Volvé al sistema del dibujo (`UCS`, opción `World`) y, para tener un archivo que `que_matriz.py` pueda leer, aplicá `ALIGN` sin escalado con $A\to(0,0)$ y $B\to(25,0)$. Guardá con otro nombre.
6. Volvé al original y rotá la parcela con `ROTATE`, punto base $A$, opción `Reference`: marcás $A$ y $B$ y das el ángulo nuevo 0. Guardá.

LibreCAD no tiene `UCS`: ahí la lectura pasiva se hace a mano con $C^T(p-A)$, o con los pasos 5 y 6, que sí existen en el menú `Modify` (moviendo y rotando por separado).

Qué debería dar: $B=(25;\ 0)$, el vértice $C=(36{,}080;\ 16{,}560)$, $D=(21{,}280;\ 22{,}960)$ y $E=(2{,}320;\ 22{,}240)$ en el sistema del frente; por ejemplo, para el vértice $C$, $p-A=(30,26)$, $b_1\cdot(30,26)=28{,}8+7{,}28=36{,}08$ y $b_2\cdot(30,26)=-8{,}4+24{,}96=16{,}56$. El área sigue siendo 655 m²: en una base ortonormal las longitudes y las áreas no cambian. El paso 5 da esas mismas coordenadas, ahora como coordenadas del dibujo: $p\mapsto C^T(p-A)$, con $M=C^T=\begin{pmatrix}0{,}960&0{,}280\\-0{,}280&0{,}960\end{pmatrix}$, $t=(-12{,}400;\ -6{,}800)$ y $\det M=1$, una rotación de $-16{,}260^\circ$ (el frente forma $16{,}260^\circ$ con el eje este). El paso 6 es la lectura activa con la misma matriz $M$: la parcela gira alrededor de $A$, que queda en $(10,10)$, y $t=(-2{,}400;\ 3{,}200)$. Girar los ejes $16{,}260^\circ$ da las mismas etiquetas que girar la parcela $-16{,}260^\circ$.

Un detalle importante: el DXF guarda siempre las coordenadas del sistema del dibujo. Cambiar el `UCS` no cambia el archivo, porque no mueve nada; por eso, para comparar con `que_matriz.py`, la lectura pasiva hay que convertirla en un movimiento (paso 5). Y el `UCS` solo admite ejes perpendiculares con la misma unidad: el CAD mide distancias con la cuenta de siempre, $\sqrt{x^2+y^2}$, que solo vale en una base ortonormal.

Respuestas: [`esperado/cap09_ucs_frente.dxf`](dxf/esperado/cap09_ucs_frente.dxf) (lectura pasiva) y [`esperado/cap09_ucs_activa.dxf`](dxf/esperado/cap09_ucs_activa.dxf) (lectura activa).
