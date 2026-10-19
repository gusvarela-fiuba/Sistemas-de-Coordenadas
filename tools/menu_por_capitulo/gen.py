#!/usr/bin/env python3
"""Menú por capítulo: entradas, platos y postres para cada ficha del programa (A4 apaisado, imprimible).

Genera `site/menu-por-capitulo.html`. Lo llama tools/build.py después del laboratorio CAD y del menú
(tools/menu.py), antes de las menciones prohibidas. Los textos de cada capítulo están escritos a mano acá, salvo el título (el del PDF, menu.titulo_capitulo_pdf);
el rótulo de cada capítulo sale de build.rotulo_ficha (numeración del PDF) y los platos de CAD pasan a
«listo» con enlace a cad/#capN cuando el sitio publica site/cad/index.html con esa sección y
cad/ejercicios.yaml tiene ejercicios de ese capítulo. Al final verifica que todo enlace al sitio
(absoluto, con la URL publicada, o relativo) apunte a un archivo existente en site/ (si no, exit 1).

Uso:  uv run python tools/menu_por_capitulo/gen.py [--site site]
"""
from __future__ import annotations

import argparse
import html as H
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from build import CAPITULO_DE_FICHA, MAPA, RAIZ, cargar_mapa, rotulo_ficha  # noqa: E402
from menu import cargar_cad, existe, titulo_capitulo_pdf, url_sitio  # noqa: E402

S = (url_sitio() or "https://gusvarela-fiuba.github.io/Sistemas-de-Coordenadas/").rstrip("/")
SALIDA = "menu-por-capitulo.html"
def U(i): return f"{S}/unidades/{i}/"
def A(i): return f"{S}/animaciones/{i}.mp4"
# item: (nombre, descripcion, tiempo, donde, estado, [(texto,url)])
L="listo"; P="a pedido"
C={}
C["01"]=("Rotaciones: de los complejos a la exponencial",
[("La plataforma que gira","Imaginate arriba de una plataforma que gira. Desde afuera se mueve el objeto; desde arriba, gira el paisaje en sentido contrario. ¿Qué cambió y qué no?","2 min","para explicar",L,[]),
 ("El reloj y el norte","El acimut se cuenta como un reloj: desde las 12 y en sentido horario. El ángulo matemático, desde las 3 y al revés. ¿A qué hora apunta el norte?","3 min","para explicar",L,[]),
 ("Un segundo de arco","Hay instrumentos que miden ángulos con precisión de un segundo. ¿Cuánto se corre un punto a 1 km si el ángulo cambia 1″? (unos 5 mm)","3 min","para explicar",L,[])],
[("El punto que no se movió","Rotación activa y pasiva: mover el punto o mover los ejes.","10 min","televisor",L,[("unidad 01a",U("01a_punto_quieto"))]),
 ("Girar es multiplicar","La rotación del plano como multiplicación por un número complejo de módulo 1.","20 min","puestos",L,[("unidad 01b",U("01b_rotacion_plano"))]),
 ("Tres ejes en el espacio","Rotaciones 3D con controles; primer vistazo a que el orden importa.","10 min","televisor",L,[("unidad 01c",U("01c_rotaciones_3d"))]),
 ("Rotar en CAD","ROTATE, UCS y UNITS: el mismo giro leído como acimut y como ángulo matemático.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Girar 30° y después 45°, ¿es lo mismo que girar 75°? ¿Y en el espacio, con ejes distintos?","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y capítulo del apunte.","en casa","",L,[("ficha",f"{S}/capitulos/01.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["02"]=("Composición, conmutatividad y líneas coordenadas",
[("El libro en el aire","Girá un libro 90° hacia adelante y después 90° de costado; ahora en el otro orden. No termina igual. Con una hoja girando sobre la mesa, sí.","3 min","para explicar",L,[]),
 ("Mover un mueble","Para llevar un mueble de un lugar a otro sin desarmarlo alcanza con girar y deslizar.","2 min","para explicar",L,[]),
 ("Medias y zapatos","Hay operaciones en las que el orden importa y otras en las que no. ¿Cuáles de la vida diaria conmutan?","2 min","para explicar",L,[])],
[("El orden de los giros","Componer rotaciones 3D en un orden y en el otro, y comparar.","10 min","televisor",L,[("unidad 01c",U("01c_rotaciones_3d"))]),
 ("Componer movimientos","Girar y trasladar en el plano; ver qué movimiento resulta.","20 min","puestos",L,[("unidad 01b",U("01b_rotacion_plano")),("unidad 03",U("03_reflexiones_similaridades"))]),
 ("El mazo de cartas","Correr la carta de arriba sin mover la de abajo: la traslación se vuelve lineal en coordenadas homogéneas.","10 min","televisor",L,[("unidad 04",U("04_afines_homogeneas"))]),
 ("Líneas coordenadas","Escena guiada: la grilla cartesiana y la polar (circunferencias y radios) sobre el mismo plano.","10 min","televisor",P,[]),
 ("El orden en CAD","MOVE y ROTATE en distinto orden sobre la misma parcela.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Girás 90° alrededor de un punto A y después −90° alrededor de otro punto B. ¿Qué movimiento queda? (una traslación)","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/02.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["03"]=("Reflexiones, similaridades y afinidades",
[("Los espejos del probador","Dos espejos que se cortan: el reflejo del reflejo está girado el doble del ángulo entre ellos. Si son paralelos, queda corrido el doble de la distancia.","3 min","para explicar",L,[]),
 ("La fotocopia ampliada","Misma forma, otro tamaño: eso es una similaridad.","2 min","para explicar",L,[]),
 ("La sombra de una ventana","Al sol, las paralelas siguen paralelas, pero cambian ángulos y largos: una afinidad.","2 min","para explicar",L,[])],
[("Dos reflexiones, una rotación","Componer reflexiones y ver aparecer rotaciones y traslaciones.","10 min","televisor",L,[("unidad 03",U("03_reflexiones_similaridades"))]),
 ("Afinidades a mano","Deformar una figura y comprobar qué se conserva.","20 min","puestos",L,[("unidad 04",U("04_afines_homogeneas"))]),
 ("Espejos en CAD","MIRROR dos veces y ALIGN: qué matriz aplicaste.","20 min","puestos",P,[]),
 ("El plano escaneado","Planilla: un plano que se encogió 0,4 % en un sentido; corregirlo con tres puntos conocidos.","20 min","puestos",P,[])],
[("Pregunta para llevarse","¿Cuántos puntos hacen falta para fijar una afinidad del plano? (tres, no alineados)","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/03.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["03p"]=("Complemento: transformaciones proyectivas",
[("Las vías del tren","Las vías se juntan en el horizonte: las rectas siguen rectas, pero las paralelas dejan de serlo.","2 min","para explicar",L,[]),
 ("Sol o lámpara","La sombra al sol es una afinidad; la de una lámpara cercana, una proyectiva.","3 min","para explicar",L,[]),
 ("La fachada torcida","Una foto tomada de costado: ¿se puede recuperar la fachada derecha?","2 min","para explicar",L,[])],
[("El pentágono en homogéneas","Animación: la figura en el plano z = 1 y su proyección.","5 min","televisor",L,[("animación 02",A("02_homogeneas_pentagono_3d"))]),
 ("Proyectivas con controles","Mover cuatro puntos y ver cómo se deforma el plano.","20 min","puestos",L,[("unidad 05",U("05_proyectivas"))]),
 ("Rectificar una foto","Planilla: llevar una foto oblicua a vista de frente con cuatro puntos.","20 min","puestos",P,[])],
[("Pregunta para llevarse","¿Cuántos puntos hacen falta para fijar una proyectiva? (cuatro, sin tres alineados)","2 min","para explicar",L,[]),
 ("Una aplicación","Así se arma una foto aérea que se puede medir: el primer paso de la fotogrametría.","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del complemento y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/03p.html"),("apunte",f"{S}/apunte.pdf")])])
C["04"]=("Formas lineales y dualidad",
[("La regla de la subida","Una regla que, para cada paso que das, dice cuánto subiste. Eso es una forma lineal.","2 min","para explicar",L,[]),
 ("Contar curvas de nivel","Una forma lineal se dibuja como curvas de nivel; medir un paso es contar cuántas cruzás.","3 min","para explicar",L,[]),
 ("El precio de la canasta","Una caja que a cada canasta le asigna su costo: suma lo que cuesta cada cosa.","2 min","para explicar",L,[])],
[("Dualidad y gradiente","Animación: el vector y las curvas de nivel que lo miden.","5 min","televisor",L,[("animación 01",A("01_dualidad_gradiente"))]),
 ("Formas lineales con controles","Mover vectores y formas y ver el número que resulta.","20 min","puestos",L,[("unidad 06",U("06_formas_lineales"))]),
 ("Vectores y formas","V y V*: flechas y escalones, el mismo plano mirado de dos maneras.","10 min","televisor",L,[("unidad 00",U("00_fundamentos"))]),
 ("La regla y la carta","Escena guiada sobre una carta con curvas de nivel.","10 min","televisor",P,[])],
[("Pregunta para llevarse","Un desplazamiento se mide en metros; una pendiente, en “por metro”. Si pasás a centímetros, ¿qué pasa con cada uno? (uno se multiplica por 100, el otro se divide)","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/04.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["05"]=("Subespacios, producto cuña y determinante",
[("La goma con grilla","Una grilla estampada en goma, estirada parejo: cada cuadradito pasa a medir lo mismo, el determinante.","2 min","para explicar",L,[]),
 ("El dibujo en el espejo","Si el dibujo queda como visto en un espejo, el determinante es negativo.","2 min","para explicar",L,[]),
 ("Tres mojones alineados","Si tres mojones están en línea, el triángulo que forman no tiene área.","2 min","para explicar",L,[])],
[("Cuña y determinante","El área orientada con controles.","10 min","televisor",L,[("unidad 07a",U("07a_cuna_determinante"))]),
 ("Cuando el área se anula","El plano aplastado sobre una recta: lo que se pierde.","20 min","puestos",L,[("unidad 07b",U("07b_nucleo_autovectores"))]),
 ("Áreas en CAD","AREA y SCALE: el área se multiplica por el determinante.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Si escalás un plano al doble en ambos sentidos, ¿por cuánto se multiplica la superficie? (por 4)","2 min","para explicar",L,[]),
 ("Una aplicación","La superficie de un lote por coordenadas de sus vértices es una suma de cuñas.","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo, apunte y autoevaluación.","en casa","",L,[("ficha",f"{S}/capitulos/05.html"),("apunte",f"{S}/apunte.pdf"),("autoevaluación",f"{S}/autoevaluacion.html")])])
C["06"]=("Subespacios invariantes, autovalores y autovectores",
[("La tela estirada","Al estirar una tela, casi todas las líneas dibujadas giran, salvo algunas direcciones que solo se estiran.","2 min","para explicar",L,[]),
 ("El eje de la puerta","Una puerta gira, pero su eje no se mueve: una dirección que la rotación deja quieta.","2 min","para explicar",L,[]),
 ("¿Siempre hay?","Un giro de 30° en el plano, ¿deja alguna dirección sin girar?","2 min","para explicar",L,[])],
[("Las direcciones que no giran","Buscar con controles las direcciones que solo se estiran.","10 min","televisor",L,[("unidad 07b",U("07b_nucleo_autovectores"))]),
 ("Autovalores en 3D","Puntos y ejes fijos de transformaciones del espacio.","20 min","puestos",L,[("unidad 07c",U("07c_autovalores_3d_puntos_fijos"))]),
 ("La tela y sus direcciones","Escena guiada con casos preparados.","10 min","televisor",P,[])],
[("Pregunta para llevarse","¿Por qué el eje de una rotación en el espacio corresponde al autovalor 1?","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/06.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["07"]=("La SVD: de la circunferencia a la elipse",
[("Girar, estirar, girar","Toda transformación lineal lleva una circunferencia a una elipse, en tres pasos.","2 min","para explicar",L,[]),
 ("La sombra de un aro","La sombra de un aro redondo es una elipse: ¿cuál es el eje largo y cuál el corto?","2 min","para explicar",L,[]),
 ("La elipse finita","Si la elipse queda muy finita, ¿qué le pasó al plano?","2 min","para explicar",L,[])],
[("Del círculo a la elipse","Animación de los tres pasos.","5 min","televisor",L,[("animación 04",A("04_svd_circulo_a_elipse"))]),
 ("SVD con controles","Ver los ejes de la elipse y los valores singulares.","20 min","puestos",L,[("unidad 09",U("09_cambio_de_base_svd"))]),
 ("Los tres pasos","Escena guiada: cada paso por separado, con casos fijos.","10 min","televisor",P,[])],
[("Una aplicación","La elipse de error de un punto medido: el mismo dibujo, otra lectura.","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/07.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["08"]=("Cambio de base y diagonalización",
[("La casa y la dirección","Las coordenadas son etiquetas: la misma casa tiene otra dirección según el sistema.","2 min","para explicar",L,[]),
 ("Dos observadores","Dos personas miran la misma chapa deformada: una ve algo complicado; la otra, alineada con las direcciones que no giran, ve dos estiramientos.","3 min","para explicar",L,[]),
 ("La obra y el catastro","El mismo lote en las coordenadas locales de la obra y en las del catastro.","2 min","para explicar",L,[])],
[("El viaje del cambio de base","Animación: traducir, estirar, devolver.","5 min","televisor",L,[("animación 03",A("03_cambio_de_base_viaje"))]),
 ("Diagonalizar con controles","Ver A = C D C⁻¹ leída de derecha a izquierda.","20 min","puestos",L,[("unidad 08",U("08_cambio_de_base"))]),
 ("Tres pasos","Escena guiada de A = C D C⁻¹, con casos fijos.","10 min","televisor",P,[]),
 ("UCS en CAD","Alinear el sistema con el frente de una parcela y leer las coordenadas.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Si en la base de autovectores la matriz es diagonal, ¿qué hace A aplicada cinco veces?","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/08.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["09"]=("Derivada, gradiente y jacobiano",
[("La lupa","Con una lupa, cualquier terreno suave se ve plano: el jacobiano es lo que muestra la lupa.","2 min","para explicar",L,[]),
 ("Hacia dónde corre el agua","El agua baja por la pendiente máxima: esa dirección es el gradiente.","2 min","para explicar",L,[]),
 ("El cuadradito","Un cuadradito chico, después de una transformación curva, se ve como un paralelogramo.","2 min","para explicar",L,[])],
[("Jacobiano con controles","El paralelogramo local y la primera forma.","20 min","puestos",L,[("unidad 10",U("10_jacobiano_primera_forma"))]),
 ("Gradiente y curvas de nivel","Animación: el gradiente perpendicular a las curvas.","5 min","televisor",L,[("animación 01",A("01_dualidad_gradiente"))]),
 ("Zoom sobre un terreno","Escena guiada: acercarse hasta que el terreno se vea plano.","10 min","televisor",P,[])],
[("Pregunta para llevarse","¿Por qué el agua cruza las curvas de nivel en ángulo recto?","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/09.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["10"]=("Inversas, cuatro subespacios y pseudoinversa",
[("Las mediciones que no cierran","Cuando los datos no cierran, la pseudoinversa elige la respuesta más cercana.","2 min","para explicar",L,[]),
 ("La sombra sobre el piso","La sombra de un punto sobre un plano es lo más cercano que hay en ese plano.","2 min","para explicar",L,[]),
 ("Deshacer una sombra","¿Se puede reconstruir un objeto a partir de su sombra? ¿Qué se perdió?","2 min","para explicar",L,[])],
[("Pseudoinversa con la SVD","Invertir lo que se puede y descartar lo que no.","10 min","televisor",L,[("unidad 09",U("09_cambio_de_base_svd"))]),
 ("La mejor respuesta posible","Problemas con datos de más o de menos.","20 min","puestos",L,[("unidad 11",U("11_cuatro_problemas"))]),
 ("Tres puntos y una recta","Planilla: la recta que mejor pasa por tres puntos no alineados.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Al proyectar sobre el piso, ¿qué información se pierde y cuál queda?","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/10.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["11"]=("Cuatro problemas de ajuste",
[("Tres medidas de la misma distancia","Medís tres veces y no coinciden. ¿Qué anotás? El promedio ya es un ajuste.","2 min","para explicar",L,[]),
 ("Vertical o perpendicular","El error de una recta, ¿se mide en vertical o en perpendicular? Cambia la respuesta.","3 min","para explicar",L,[]),
 ("Dos calcos","Superponer dos calcos del mismo plano: girar, correr y escalar hasta que coincidan.","2 min","para explicar",L,[])],
[("Los cuatro problemas","Regresión, ajuste perpendicular, superposición de calcos y más, con controles.","10 min","televisor",L,[("unidad 11",U("11_cuatro_problemas"))]),
 ("Comparar métodos","Los mismos datos ajustados de varias maneras.","20 min","puestos",L,[("unidad 11",U("11_cuatro_problemas"))]),
 ("Vertical frente a perpendicular","Planilla o GeoGebra con puntos editables.","20 min","puestos",P,[])],
[("Pregunta para llevarse","Si la recta es casi vertical, ¿qué método falla?","2 min","para explicar",L,[]),
 ("Una aplicación","Superponer un relevamiento viejo y uno nuevo es un problema de calcos.","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo, apunte y autoevaluación.","en casa","",L,[("ficha",f"{S}/capitulos/11.html"),("apunte",f"{S}/apunte.pdf"),("autoevaluación",f"{S}/autoevaluacion.html")])])
C["12"]=("Curvatura y formas cuadráticas",
[("El volante","Manejando por una ruta, cuánto hay que girar el volante es la curvatura.","2 min","para explicar",L,[]),
 ("La silla de montar","Sube en una dirección y baja en la otra.","2 min","para explicar",L,[]),
 ("La cáscara de naranja","No se puede aplanar sin romperla; una hoja enrollada, sí.","2 min","para explicar",L,[])],
[("Curvatura con controles","Curvas y superficies, direcciones de máxima y mínima curvatura.","20 min","puestos",L,[("unidad 12",U("12_curvatura"))]),
 ("Euler y Meusnier","Animación: cómo cambia la curvatura con la dirección.","5 min","televisor",L,[("animación 05",A("05_elipsoide_euler_meusnier"))]),
 ("El volante y la ruta","Escena guiada con un tramo recto, una curva y una rotonda.","10 min","televisor",P,[])],
[("Pregunta para llevarse","¿Qué curvatura tiene una ruta recta? ¿Y una rotonda de 20 m de radio? (0 y 1/20 por metro)","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/12.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["13"]=("Geometría del elipsoide",
[("La pelota aplastada","La Tierra es una pelota apenas aplastada: el radio depende de hacia dónde se mire.","2 min","para explicar",L,[]),
 ("Un grado no mide igual","Un grado de latitud mide unos 110,6 km en el ecuador y unos 111,7 km cerca del polo.","2 min","para explicar",L,[]),
 ("¿Dónde está la vertical?","La plomada no apunta al centro de la Tierra.","2 min","para explicar",L,[])],
[("El elipsoide con controles","Radios en el meridiano y en el primer vertical.","20 min","puestos",L,[("unidad 13",U("13_elipsoide"))]),
 ("Euler y Meusnier","Animación sobre el elipsoide.","5 min","televisor",L,[("animación 05",A("05_elipsoide_euler_meusnier"))]),
 ("Radios para tu latitud","Planilla: cada uno calcula los radios donde nació.","20 min","puestos",P,[])],
[("Pregunta para llevarse","En Buenos Aires, ¿la Tierra es más curva en dirección norte-sur o este-oeste? (norte-sur)","2 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo y apunte.","en casa","",L,[("ficha",f"{S}/capitulos/13.html"),("apunte",f"{S}/apunte.pdf")]),
 ("Autoevaluación","Preguntas del banco con respuesta.","10 min","en casa",L,[("autoevaluación",f"{S}/autoevaluacion.html")])])
C["14"]=("Trigonometría esférica y polígonos geodésicos",
[("Tres ángulos rectos","Desde el polo bajás al ecuador, girás 90°, caminás un cuarto del ecuador y volvés al polo: un triángulo con tres ángulos rectos.","3 min","para explicar",L,[]),
 ("El vuelo más corto","El camino más corto entre dos ciudades lejanas no mantiene el rumbo.","2 min","para explicar",L,[]),
 ("Groenlandia y África","En el mapa de Mercator, Groenlandia parece casi tan grande como África.","2 min","para explicar",L,[])],
[("Trigonometría esférica","Triángulos sobre la esfera y su exceso.","20 min","puestos",L,[("unidad 14",U("14_trigonometria_esferica"))]),
 ("Tissot y Mercator","Animación: rumbo fijo como recta y deformación de áreas.","5 min","televisor",L,[("animación 06",A("06_conforme_tissot_mercator"))]),
 ("Transformaciones conformes","Mapas que conservan ángulos.","15 min","puestos",L,[("unidad 15",U("15_transformaciones_conformes"))]),
 ("El triángulo de tres rectos","GeoGebra 3D para girar la esfera.","15 min","puestos",P,[])],
[("Pregunta para llevarse","¿Cuánto suman los ángulos de un triángulo dibujado en una cancha? (casi 180°)","2 min","para explicar",L,[]),
 ("Una aplicación","Buenos Aires–Mendoza: unos 981 km por el camino más corto, con un rumbo que cambia por el camino.","3 min","para explicar",L,[]),
 ("Para repasar","Ficha del capítulo, apunte y autoevaluación.","en casa","",L,[("ficha",f"{S}/capitulos/14.html"),("apunte",f"{S}/apunte.pdf"),("autoevaluación",f"{S}/autoevaluacion.html")])])
ORDEN = ["01","02","03","03p","04","05","06","07","08","09","10","11","12","13","14"]


def platos_cad(site: Path) -> None:
    """Los platos «… en CAD» de las fichas con ejercicios publicados en site/cad/ pasan a «listo» con enlace a cad/#capN."""
    pagina_cad = site / "cad" / "index.html"
    if not pagina_cad.is_file():
        return
    texto_cad = pagina_cad.read_text(encoding="utf-8")
    con_ejercicios = {str(c["capitulo"]) for c in cargar_cad()}
    for k in ORDEN:
        caps = [n for n in CAPITULO_DE_FICHA.get(k, k).split(" y ")
                if n in con_ejercicios and f'id="cap{n}"' in texto_cad]
        if not caps:
            continue
        platos = C[k][2]
        for i, (n, d, t, w, e, ls) in enumerate(platos):
            if "CAD" in n:
                platos[i] = (n, d, t, w, L, ls + [(f"CAD capítulo {c}", f"{S}/cad/#cap{c}") for c in caps])


def item(it):
    n,d,t,w,e,ls=it
    lk=" · ".join(f'<a href="{H.escape(u)}">{H.escape(x)}</a>' for x,u in ls)
    meta=" · ".join(x for x in [t,w] if x)
    cls="ped" if e==P else "ok"
    return f'<div class="it {cls}"><div class=n>{H.escape(n)}<span class=e>{e}</span></div><div class=d>{H.escape(d)}</div><div class=m>{meta}{(" · "+lk) if lk else ""}</div></div>'


def rotulo(k):
    return rotulo_ficha(k)


def generar_html() -> str:
    pages=[]
    for k in ORDEN:
        t,en,pl,po=C[k]
        pages.append(f'<section id="cap-{k}"><h1><span>{rotulo(k)}</span> {H.escape(titulo_capitulo_pdf(k))}</h1><div class=g>'
          +"".join(f'<div class=col><h2>{h}</h2><p class=hs>{s}</p>{"".join(item(i) for i in xs)}</div>' for h,s,xs in [("Entradas","para abrir: una imagen o una pregunta",en),("Platos","el centro del capítulo: televisor y puestos",pl),("Postres","para cerrar y llevarse",po)])
          +'</div><p class=pie>Se elige uno o varios de cada columna. Lo marcado <b>a pedido</b> se prepara para la fecha en que se da el capítulo.</p></section>')
    cover=f'''<section class=cov><h1 class=t>Sistemas de Coordenadas</h1><p class=st>Un menú para cada capítulo</p>
<p>Cada capítulo tiene su menú, con varias <b>entradas</b> para abrir, varios <b>platos</b> para el centro del capítulo y varios <b>postres</b> para cerrar. Se elige lo que se quiera: uno de cada columna, varios o ninguno.</p>
<p>Cada plato dice cuánto lleva y dónde se sirve: <b>para explicar</b> (una imagen o una pregunta), en el <b>televisor</b> (una unidad interactiva o una animación) o en los <b>puestos</b> (cada alumno con la unidad en su computadora).</p>
<p><span class="e ok2">listo</span> ya está en el sitio y se usa hoy. <span class=e>a pedido</span> se prepara para el capítulo que se elija: escenas guiadas, planillas, GeoGebra y los ejercicios de CAD que todavía no están en el laboratorio.</p>
<p>También a pedido, para cualquier capítulo: un guion de una página (qué mostrar, qué preguntar, cuándo pasar a los puestos) y una versión de la unidad preparada para proyectar, con letra grande y casos fijos.</p>
<p class=ix>{" · ".join(f'<a href="#cap-{k}">{rotulo(k)}</a>: '+H.escape(titulo_capitulo_pdf(k)) for k in ORDEN)}</p>
<p>Todo el material: <a href="{S}/">{S[8:]}</a> · <a href="{S}/mapa.html">mapa de conceptos</a> · <a href="{S}/menu.html">qué hay para cada tema</a> · <a href="{S}/cad/">laboratorio CAD</a></p></section>'''
    css='''@page{size:A4 landscape;margin:10mm 11mm}
body{font-family:'DejaVu Sans',sans-serif;font-size:8.3pt;color:#1d2327;line-height:1.32;margin:0}
section{break-after:page;height:186mm;overflow:hidden;box-sizing:border-box;display:flex;flex-direction:column}
section:last-child{break-after:auto}
h1{font-family:'DejaVu Serif',serif;font-size:15pt;color:#0f4c5c;margin:0 0 3mm;border-bottom:1pt solid #0f4c5c;padding-bottom:1.5mm}
h1 span{color:#8a4a1c;font-size:11pt;margin-right:2mm}
.g{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5mm;flex:1}
h2{font-family:'DejaVu Serif',serif;font-size:12pt;margin:0;color:#0f4c5c}
.hs{margin:0 0 2mm;color:#666;font-size:7.6pt}
.it{border:0.4pt solid #c9d3d6;border-left:2.2pt solid #0f4c5c;border-radius:2mm;padding:1.8mm 2.4mm;margin:0 0 2.2mm;background:#f6f9f9;break-inside:avoid}
.it.ped{border-left-color:#8a4a1c;background:#fbf3ec}
.n{font-weight:bold;font-size:8.8pt;display:flex;justify-content:space-between;gap:2mm}
.e{font-weight:normal;font-size:6.8pt;color:#fff;background:#8a4a1c;border-radius:1.5mm;padding:0.2mm 1.6mm;white-space:nowrap;height:fit-content}
.ok .e,.ok2{background:#0f4c5c}
.d{margin:0.8mm 0}
.m{color:#555;font-size:7.4pt}
a{color:#0f4c5c}
.pie{color:#666;font-size:7.4pt;margin:1mm 0 0}
.cov{font-size:10.5pt;line-height:1.5;padding:4mm 25mm}
.cov .t{font-size:24pt;border:0}.st{font-size:14pt;color:#8a4a1c;margin:-2mm 0 6mm;font-family:'DejaVu Serif',serif}
.cov .e{font-size:8.5pt}.ix{font-size:8.6pt;color:#333}'''
    return f"<!doctype html><html lang=es><meta charset=utf-8><title>Un menú para cada capítulo</title><style>{css}</style><body>{cover}{''.join(pages)}</body></html>"


def hrefs_al_sitio(htm: str) -> list[str]:
    """Enlaces que apuntan dentro del sitio, como ruta relativa a site/ (los absolutos con la URL publicada, sin ella)."""
    out = []
    for h in (H.unescape(x) for x in re.findall(r'href="([^"]+)"', htm)):
        if h.startswith(S + "/"):
            out.append(h[len(S) + 1:])
        elif not re.match(r"^[a-z]+:|^#", h):
            out.append(h)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=f"Genera site/{SALIDA} (entradas, platos y postres por capítulo).")
    ap.add_argument("--site", default="site", help="directorio del sitio ya generado (default: site)")
    a = ap.parse_args(argv)
    site = Path(a.site)
    if not site.is_absolute():
        site = RAIZ / site
    if not site.is_dir():
        print(f"ERROR: {site} no existe; correr antes tools/build.py", file=sys.stderr)
        return 1
    platos_cad(site)
    htm = generar_html()
    (site / SALIDA).write_text(htm, encoding="utf-8")
    hrefs = hrefs_al_sitio(htm)
    faltan = sorted({h for h in hrefs if not existe(site, h)})
    # una unidad del mapa sin exportar (build.py --skip-wasm sobre un site/ limpio) es aviso; una que no está en el mapa, error
    del_mapa = {u["id"] for u in cargar_mapa(MAPA)["unidades"]}
    sin_export = [h for h in faltan if re.fullmatch(r"unidades/([^/]+)/", h) and h.split("/")[1] in del_mapa]
    rotos = [h for h in faltan if h not in sin_export]
    if sin_export:
        print(f"  aviso: {len(sin_export)} unidades del mapa sin exportar en {site.name}/unidades (se publican con el build completo)")
    listos = sum(it[4] == L for k in ORDEN for col in C[k][1:] for it in col)
    total = sum(len(col) for k in ORDEN for col in C[k][1:])
    cad = sum(1 for k in ORDEN for it in C[k][2] if "CAD" in it[0] and it[4] == L)
    print(f"  {site / SALIDA}  ({len(ORDEN)} capítulos, {listos} de {total} listos, {cad} platos CAD listos, "
          f"{len(hrefs)} enlaces al sitio verificados)")
    for h in rotos:
        print(f"ERROR: {SALIDA}: enlace roto {h}", file=sys.stderr)
    return 1 if rotos else 0


if __name__ == "__main__":
    sys.exit(main())
