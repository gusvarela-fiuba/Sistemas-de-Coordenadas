# Hoja de ruta

Qué viene después de la entrega 4. Cada línea es una tarea; se tacha al cerrarla y se anota el commit. Los defectos puntuales van en `apunte/PENDIENTES.md`; el estado de cada fase, en `apunte/ESTADO_FASE.md`.

## Entrega 5

### 1. Bloques en lugar de una sola fila

La numeración de los capítulos no cambia, porque la usan las etiquetas, los problemas (12.5), los menús, las fichas y los enlaces publicados. Los bloques son una capa encima: portada, mapa, menús y una página del PDF que diga qué hace falta antes de cada bloque.

| Bloque | Capítulos | Se apoya en |
|---|---|---|
| 0. Fundaciones | 0 (los cinco ladrillos) | nada |
| 1. Mover sin deformar | 1, 2, 3 | 0 |
| 2. Deformar | 4 y C1 (proyectivas) | 1 (homogéneas) |
| 3. Medir | 5, 6 | 0 |
| 4. Leer una matriz | 7, 8, 9 | 3 (determinante) |
| 5. Resolver y ajustar | 11, 12 | 4 (SVD) |
| 6. Lo curvo | 10, 13 | 3 (gradiente) y 4 (autovalores) |
| 7. La Tierra | 14, 15, C2 y C4 | 6 |

- [ ] Agregar `bloque:` y `requiere_bloques:` a las fichas en `mapa/_fragmentos/` y validar con `merge_mapa.py` que las dependencias entre bloques sean coherentes con los `requiere` de los conceptos.
- [ ] Portada y `mapa.html`: vista por bloques con las rutas posibles (por ejemplo, 0 → 3 → 4 → 6 → 7 para llegar rápido a la Tierra).
- [ ] Menús: agrupar por bloque; cada bloque dice en qué se apoya.
- [ ] PDF: una página «Cómo leer este apunte por bloques», con el cuadro y las rutas.

### 2. Cubrir lo que pide el programa y hoy está flojo

Los contenidos mínimos del plan 2023 (CB104, tercer cuatrimestre, 64 horas) incluyen marcos de referencia, Molodensky, transformaciones basadas en grillas, discretización y remuestreo, derivada compleja, transformaciones conformes, plano complejo extendido y proyección estereográfica. En el apunte viven en complementos cortos: C4 tiene 115 líneas y Molodensky aparece dos veces en 290 páginas.

- [ ] C2 → capítulo: derivada compleja y Cauchy–Riemann, por qué C no es R², conformes, plano complejo extendido y proyección estereográfica, Mercator y Gauss–Krüger como conformes. Con unidad y problemas.
- [ ] C4 → capítulo: sistema y marco de referencia, transformación de siete parámetros, Molodensky, grillas de corrección (NTv2), discretización y remuestreo (vecino más cercano, bilineal), número de faja en las coordenadas Gauss–Krüger. Con unidad y problemas.
- [ ] Alturas: sección nueva sobre altura elipsoidal, geoide y altura ortométrica (h = H + N), con su caja «Esto lo vas a usar en Topografía». Hoy no aparecen en el apunte.
- [ ] Problemas para C1 a C4, con `tools/problemas/gen.py`.

### 3. GeoGebra

GeoGebra es una de las herramientas habituales del aula, y ya hay apuntes de álgebra lineal armados como libro de GeoGebra (por ejemplo, las notas interactivas de MATH 2111 de HKUST: 9 capítulos y 52 temas con actividades). La idea es ofrecer las piezas centrales también en GeoGebra, como alternativa a marimo, sin reemplazarlo.

- [ ] Elegir de 8 a 10 escenas, una por bloque: giro como multiplicación compleja, dos espejos = giro, afinidad por tres puntos, determinante como área, direcciones que no giran, circunferencia → elipse (SVD), cambio de base en tres pasos, triángulo esférico con tres ángulos rectos (3D).
- [ ] Construirlas como archivos `.ggb` versionados en `geogebra/`, con el mismo caso inicial que la unidad marimo correspondiente.
- [ ] Publicarlas como un libro de GeoGebra y enlazarlas desde las fichas y los menús (plato «GeoGebra», hoy «a pedido»).

### 4. Probar con alumnos

- [ ] Dos o tres alumnos que terminaron el CBC usan una unidad y su capítulo sin ayuda; anotar dónde se traban.
- [ ] Ajustar «La idea» y los problemas ★ con lo que salga.

### 5. Tablas de resumen

- [ ] Una tabla de clasificación por bloque (movimientos, semejanzas, afinidades: qué conservan, matriz, determinante, puntos fijos), al estilo de los resúmenes de las escuelas de topografía, como hoja de repaso.

## Tomo 2

Temas que enseñan otras escuelas de geodesia y agrimensura y que este apunte no trata. Quedan para un segundo tomo; no entran en las entregas del tomo 1.

- [ ] Cónicas y cuádricas como formas cuadráticas (se apoyan en el capítulo 12, «Curvatura como forma cuadrática», y en los autovalores del 7). Referencia: módulo «Geometrische Modelle der Geodäsie» del KIT (3.er semestre).
- [ ] Gravedad, vertical del lugar, línea de la plomada y geoide; coordenadas astronómicas frente a geodésicas. Referencia: «Fundamentos em Geodésia» (GA112) de la UFPR.
- [ ] Geometría del elipsoide ampliada: secciones normales, línea geodésica y teorema de Clairaut, áreas sobre el elipsoide. Referencia: GA112 (UFPR).
- [ ] Interpolación espacial (más allá del remuestreo del tomo 1): de puntos dispersos a grilla. Referencia: cursos abiertos de la ENSG.
- [ ] Ajuste de observaciones con estadística (pesos, covarianzas, datum, deformaciones), como continuación de los capítulos 11 y 12. Referencia: Niemeier, «Ausgleichungsrechnung».

## Más adelante

- [ ] Favicon del sitio.
- [ ] Los dos menús cuentan las piezas sobre universos distintos; unificar el criterio.
