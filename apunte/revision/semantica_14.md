# Revisión semántica del capítulo 14 (Geometría del elipsoide)

Archivos: `apunte/contenido/14-elipsoide.tex`, `apunte/scripts/cap14_elipsoide.py`, `unidades/13_elipsoide.py`. Revisión del 2026-10-19.

**Resumen:** el capítulo es matemáticamente correcto y sus números coinciden con el script y con un recálculo independiente; tiene un grave, que está en la unidad 13 (un valor del recuadro que la unidad no muestra) y un resto de procedencia en esa misma unidad, más siete observaciones menores.

## Verificaciones hechas (todas pasan)

- N desde la normal, `tan ψ = (1−e²) tan φ` y `tan β = √(1−e²) tan φ`, recalculados con numpy: ψ = −34,420332° y β = −34,510112° en φ = −34,6°.
- `M = a(1−e²)/W³` y `N/M = 1 + e′² cos²φ = 1,00456637`.
- La serie del arco de meridiano contra `scipy.integrate.quad`: dif. de 5·10⁻⁵ mm, 6·10⁻⁴ mm y 0,0897 mm (el cuadrante). El texto dice «menos de 0,1 mm»: cierto, aunque ajustado.
- pyproj (`Geod('GRS80')`): 1″ de φ = 30,814796 m; 1″ de λ = 25,480605 m; arco ecuador–polo = 10 001 965,7292 m; φ₂ de la base de 10 km = −34,50985505°.
- Máximo de φ−ψ: 11,545′ en 45,0962°.
- Ejemplo de juguete, ejercicios 14.1 a 14.5 y la tabla de esfera contra elipsoide para la base de 10 km (los 22,880 m salen con la fórmula de haversine y los dos radios).
- Más de 15 números del capítulo cotejados con la salida del script. Ninguno discrepa más allá del redondeo, salvo los casos 1 y 3 de abajo.
- Demostraciones leídas paso a paso: prop. del punto, del gran normal, de las latitudes (incluido el máximo con k = 1−e²), de M (derivadas), de las curvaturas principales (simetría + Meusnier) y del promedio √(MN). No encontré saltos ni hipótesis omitidas. Los resultados no demostrados están declarados (la geodésica se aparta del paralelo «hacia el polo», control con pyproj).
- Tareas topográficas: GRS80 con los parámetros pedidos; M = 6 356 008 m y N = 6 385 032 m en Buenos Aires; 1″ = 30,81 m / 25,48 m; base de 10 km en segundos; diferencia esfera/elipsoide de 23 m en 10 km, coherente con R/M−1 y R/N−1.
- Todas las referencias cruzadas (`\ref`) existen. Las 4 figuras PNG y la animación existen.

## Hallazgos

1. **grave** — `14-elipsoide.tex:440` (recuadro `\unidadInteractiva`). Cita: «verificá que … \(N-M=21\,456{,}48\) m». El valor correcto en GRS80 a 45° es N−M = 21 456,4746 m. La unidad muestra `{N-M:,.2f}` = «21,456.47 m» (se comprobó con python que `'%.2f' % 21456.474607 = 21456.47`). Quien verifica no ve el número que el texto nombra. El script imprime «21 456,475» y de ahí vino el redondeo hacia arriba. Propuesta: cambiar a «21 456,47 m» en el recuadro y en el script (`cap14_elipsoide.py`, línea `unidad, GRS80 en 45°`).

2. **grave (procedencia)** — `unidades/13_elipsoide.py:160-161`. Cita: «otro apunte escribe \(x = x'\sin\lambda\), \(y = x'\cos\lambda\), otra convención de ejes». Es una referencia a la errata o variante de otro documento, que el lector no tiene. Propuesta: borrar la frase y dejar sólo «X hacia el meridiano origen».

3. **grave (procedencia)** — `unidades/13_elipsoide.py:54, 149, 502-503`, y `unidades/14_trigonometria_esferica.py:149, 152, 486-487`.
   - `13_elipsoide.py:54`: «Notación del apunte *Geometría del Elipsoide y cálculos Geodésicos*».
   - `13_elipsoide.py:149`: «apunte v3, «Coordenadas curvilíneas y bases locales»; deducción en el apunte *Geometría del Elipsoide*».
   - `13_elipsoide.py:502-503`: «apunte *Geometría del Elipsoide y cálculos Geodésicos*: latitud elipsoidal, conversión…».
   - Esos títulos y esa «v3» no son secciones de este apunte. Hay que reemplazarlos por el capítulo 14 por número y nombre actual («capítulo 14, Geometría del elipsoide»; subsecciones «La normal, la latitud geodésica y el gran normal», «Radios de curvatura M y N», «Longitud del arco de meridiano»).
   - Los enlaces de la sección «Dónde está la demostración» (unidad 13, ~490-515) mezclan nombres de sección que no existen («Arco de meridiano», «Superficies, elipsoide, curvatura…») con el ancla `cap:elipsoide`.
   - Propuesta: reescribir esa sección con los títulos reales del capítulo.

4. **menor** — `14-elipsoide.tex:51` (recuadro). Cita: «pasa por el centro sólo en el ecuador y cerca del polo». La proposición del gran normal (línea 127) dice «en el ecuador y en los polos». Con el deslizador hasta 85° (la unidad no llega a 90°) «cerca del polo» es lo que se ve, pero en el polo la normal pasa por el centro exactamente. Propuesta: «pasa por el centro en el ecuador y en el polo; a 85° ya casi pasa».

5. **menor** — `14-elipsoide.tex:540`. Cita: «\(+2281\) y \(-2275\) partes por millón, simétricos porque…». La tabla de la línea 532 da +22,880 m (2288 ppm) y −22,754 m (−2275 ppm). Los 2281 ppm son R/M−1 con M en el punto de partida, y los 2288 ppm vienen de usar la Δφ exacta (324,5218″, no 10 000/M). «Simétricos» es cierto para los cocientes √(MN)/M y √(MN)/N, que son inversos, pero 2281 y 2275 no son iguales. Propuesta: agregar «aproximadamente; la integración exacta de Δφ explica los 2288 ppm de la tabla».

6. **menor** — `14-elipsoide.tex:637-638`. Cita: «Bibliografía básica. Efimov, *Formas cuadráticas y matrices*; Sáenz, *Cálculo vectorial*.» Es la bibliografía genérica del curso (figura en `ap4-bibliografia.tex`); no cubre nada de geodesia ni cita la fuente de los parámetros GRS80 y WGS84. Propuesta: agregar referencias de geodesia elipsoidal (a verificar por el autor: Torge, *Geodesy*; Moritz, 1980, para GRS80) o decir explícitamente que el capítulo se apoya en los capítulos 5, 10 y 13.

7. **menor (notación, cap. 0)** — `14-elipsoide.tex:17-25` frente a `00-antes-de-empezar.tex:858, 876-880`. El capítulo desambigua «N del primer vertical» contra «norte» («las direcciones se nombran “hacia el norte”»), lo que funciona. Pero la tabla de notación del capítulo 0 usa M para matrices y (E, N) para coordenadas, y no lista M y N como radios de curvatura, ni ψ ni β como latitudes. Propuesta: una fila «Radios de curvatura» y otra «Latitudes geocéntrica y reducida» en la tabla de notación, con la advertencia «N es aquí el radio, no el norte».

8. **menor** — `unidades/13_elipsoide.py:228`. El formato de los «números vivos» es `{v:,.2f}` = «1,852.20 m» (coma de miles, punto decimal) y el texto del recuadro (línea 440) pide «1 852,20 m». Propuesta: aclarar en el recuadro «la unidad lo muestra como 1,852.20» o formatear con coma decimal.

9. **menor** — `00-antes-de-empezar.tex:218` (tabla de operaciones). El capítulo 14 figura en la tabla del capítulo 0 con la observación «En preparación» aunque está completo. Propuesta: quitar la observación cuando se cierre la revisión del capítulo.

10. **menor** — `unidades/13_elipsoide.py:44`. La cabecera lleva «Gustavo Varela». Está en 21 de las 23 unidades, es una convención, y se lo dejo a quien decide la política de autoría; si el apunte va a ser impersonal, conviene quitarlo de todas a la vez.

## Graves del capítulo 14

1. `14-elipsoide.tex:440`: N−M = 21 456,48 m pedido en el recuadro, y la unidad muestra 21 456,47 m (valor exacto 21 456,4746).
2. `unidades/13_elipsoide.py:160-161`: referencia a «otro apunte» con otra convención (procedencia).
3. `unidades/13_elipsoide.py:54, 149, 502-503`: referencias a apuntes y versiones («apunte v3», «Geometría del Elipsoide y cálculos Geodésicos») que no son parte de este apunte (procedencia).

El capítulo `.tex` en sí no tiene graves; los tres están en el recuadro o en la unidad.
