---
clase: 2
titulo: "Capítulo 2: composición, conmutatividad y líneas coordenadas"
idea: "Para nombrar un punto con dos coordenadas hacen falta dos familias de transformaciones que conmuten; la composición y su orden son el hilo entre transformaciones, operaciones y coordenadas."
que_se_estudia: ["Composición de transformaciones: neutro, inversa, asociatividad, y no conmutatividad en general", "Conmutatividad y coordenadas: cuándo un par $(u,v)$ nombra un único punto", "Trayectorias y líneas coordenadas: cartesianas, polares y sobre la esfera", "Homotecia: la escala $kI$ conmuta con las rotaciones del mismo centro", "Traslaciones y movimientos rígidos $x\\mapsto R(\\theta)x+v$"]
conceptos_previos: ["Rotaciones (capítulo 1)", "Matrices y composición de transformaciones lineales"]
apunte: ["traslaciones", "infinitesimales", "composicion-afin", "esfera"]
unidades: ["01c_rotaciones_3d", "03_reflexiones_similaridades"]
animaciones: []
ejercicios_sugeridos: ["Verificar con $R(90°)$ y $H=2I$ que rotación y homotecia conmutan, y con $R_x$, $R_y$ que las rotaciones 3D no", "Armar el cubo de estados de tres vasos y comprobar que las tres transformaciones conmutan", "Iterar $F(x)=R(90°)x+(2,0)^T$ desde el origen y hallar el centro de la circunferencia que recorre", "Mostrar con dos rotaciones que el orden latitud–longitud no es intercambiable"]
---

# Capítulo 2: composición, conmutatividad y líneas coordenadas

Para nombrar un punto con dos coordenadas hacen falta dos familias de transformaciones que conmuten; la composición y su orden son el hilo entre transformaciones, operaciones y coordenadas.

## Qué se estudia

- Composición de transformaciones: neutro, inversa, asociatividad, y no conmutatividad en general
- Conmutatividad y coordenadas: cuándo un par $(u,v)$ nombra un único punto
- Trayectorias y líneas coordenadas: cartesianas, polares y sobre la esfera
- Homotecia: la escala $kI$ conmuta con las rotaciones del mismo centro
- Traslaciones y movimientos rígidos $x\mapsto R(\theta)x+v$

### Composición de transformaciones

Álgebra: hacer $F$ y después $G$ es $G\circ F$, y en matrices $G F$; la matriz de la derecha actúa primero. Se ve: dos movimientos encadenados son un movimiento. La composición es una operación *entre transformaciones*, como la suma lo es entre números: tiene neutro (la identidad), inversa (deshacer) y asociativa, pero no siempre conmuta. Escalera: en $\mathbb R$ componer $x\mapsto ax$ con $x\mapsto bx$ da $abx$ y el orden no importa; en $\mathbb R^2$ las rotaciones alrededor del mismo centro conmutan, $R(\alpha)R(\beta) = R(\alpha+\beta)$; en $\mathbb R^3$ las rotaciones alrededor de ejes distintos no; en $\mathbb R^n$ dos matrices cualesquiera en general no.

### Conmutatividad

Álgebra: $AB = BA$. Se ve: llegar al mismo lugar por los dos caminos del paralelogramo. Para rotaciones chicas la diferencia $AB-BA$ es de segundo orden: la falta de conmutatividad depende de la magnitud de los ángulos. Por qué importa para coordenadas: decir «el punto $(u,v)$» es decir “moví $u$ con la primera transformación y $v$ con la segunda”; si el orden cambia el resultado, el par $(u,v)$ no nombra un único punto. Con los vasos: tres vasos boca arriba/abajo son $2^3 = 8$ estados, los vértices de un cubo; las tres transformaciones (dar vuelta el último, los dos últimos, los tres últimos) conmutan y cada una es su propia inversa; por eso cada estado se nombra con tres bits, que son sus coordenadas. Si en cambio la única transformación permitida es «dar vuelta dos vasos a la vez», el cubo se parte en dos mitades (paridad) y hay estados inaccesibles: esa es la partición en «accesibles o no» del resumen.

### Trayectoria de una transformación

Álgebra: la órbita $v, Av, A^2v, \dots$ y, en continuo, $e^{tM}v$. Se ve: la transformación se identifica con la trayectoria que genera por aplicación repetida. Para una rotación, circunferencias; para una homotecia, rayos desde el centro; para una afinidad general, elipses, espirales o rectas según la matriz. Con determinante 1 la trayectoria «se queda dando vueltas»; si no, crece o se va a cero (capítulo 1).

### Líneas coordenadas

Álgebra: dos familias de transformaciones que conmutan, $T_u$ y $S_v$, y el punto $p(u,v) = T_u S_v p_0$. Se ve: las trayectorias de $T$ y de $S$ son las dos familias de líneas de la grilla. Cartesianas: traslaciones en $x$ y en $y$ (conmutan, grilla de rectas). Polares: rotación y homotecia desde el origen (conmutan, circunferencias y rayos). Esfera: paralelos como trayectorias de $R_z(\lambda)$, meridianos como trayectorias de la rotación alrededor de un eje horizontal; el eje de la rotación que mueve el punto $p$ a lo largo de su meridiano es $e_z\times p$, y ahí aparece el producto cruz como herramienta para hallar los ejes de giro. Como ese eje depende del punto, las dos familias no conmutan globalmente; latitud y longitud funcionan igual porque se fija una convención de orden (primero bajar del polo, después girar).

### Homotecia

Álgebra: $x' = o + k(x-o)$; con centro en el origen, la matriz $kI$. Se ve: todo se agranda o achica desde el centro, cada punto sobre el rayo que lo une al centro; conserva ángulos y paralelas, multiplica distancias por $|k|$. Conmuta con cualquier rotación del mismo centro ($kI\,R = R\,kI$), y por eso rotación y escala juntas dan coordenadas polares. En complejos es el $\rho$ de $\rho e^{i\theta}$, y la conmutatividad es la del producto de complejos. Es “la segunda transformación que me lleva de una trayectoria posible a otra”: salta de una circunferencia a otra.

## Conceptos previos

- Rotaciones (capítulo 1)
- Matrices y composición de transformaciones lineales

## En el apunte

- Capítulo 2. Traslaciones y movimientos rígidos
- Apéndice A.2. Rotaciones infinitesimales y orden de composición
- Apéndice A.3. Composición afín práctica: rotación y escala
- Capítulo 15. Coordenadas sobre la esfera y trigonometría esférica

## Unidades interactivas

- Rotaciones III: tres ejes y el orden importa (`01c_rotaciones_3d`)
- Reflexiones y similaridades (`03_reflexiones_similaridades`)

## Ejercicios sugeridos

- Verificar con $R(90°)$ y $H=2I$ que rotación y homotecia conmutan, y con $R_x$, $R_y$ que las rotaciones 3D no
- Armar el cubo de estados de tres vasos y comprobar que las tres transformaciones conmutan
- Iterar $F(x)=R(90°)x+(2,0)^T$ desde el origen y hallar el centro de la circunferencia que recorre
- Mostrar con dos rotaciones que el orden latitud–longitud no es intercambiable

## En el CAD

- [`MOVE` y `ROTATE` frente a `ROTATE` y `MOVE`: el orden importa](../cad/#cap2)
