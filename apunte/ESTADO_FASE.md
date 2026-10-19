# Estado de las fases del plan de cierre

Actualizado en cada commit de fase. Formato de commit: `[FASE-X] [OK|PARADA|BLOQUEO] título`.

| Fase | Contenido | Estado | Commit | PDF |
|---|---|---|---|---|
| 0 | Informe de lectura e infraestructura LaTeX | OK | 6c4f9b6 | — |
| Piloto | Capítulos de rotaciones y afines con el molde | OK | da54735, 0e56d71 | — |
| Paso 1 | Partición en un capítulo por tema y remapeo de labels | OK (aprobado) | a54da0a | — |
| Portada / renombre / cita | Trabajo final CB104; 03 renombrado; condiciones de uso sólo en el repositorio, CITATION y nota | OK | 93740dd, 1f9eeee, 78fa328 | — |
| A | Línea de base (ESTADO.md), Overfull, título interno | OK (aprobada) | 2bb7c4e | — |
| C | Capítulo de SVD, la lectura de las curvas de nivel | OK (aprobado condicionado a lectura) | dec4296 | — |
| B0 | Entrega-1: cero menciones prohibidas, proyectivas, conformes; limpieza del maestro | OK (aprobada) | ef6b397 (tag entrega-1), 622fd50 | entregas/2026-10-19_entrega-1.pdf |
| B | Capítulo 0 fusionado, apéndices ap1–ap6, capítulo 3 partido en 3 y 4 con renumeración, capítulo 2 reescrito | OK, PARADA para revisión | (dos commits de esta fase) | entregas/2026-10-19_fase-B.pdf |
| B1 | Limpieza fuera del PDF: respaldo, fichas, unidades, mapa, banco, herramientas, README, documentos internos, datos personales, enlaces del PDF, historial reescrito | OK, mergeada a main (entrega-2) | d592233, 7752ecb, 9ea5124 | entregas/2026-10-19_fase-B1.pdf |
| D | Capítulos 1 (aplicación), 3, 5, 6, 7, 9, 10 y 11 al molde | OK, PARADA para revisión | 3bf947a (cap. 1), fe14333 (3), 774b234 (5), df62300 (6), de47fcc (7), 195708d (9), a29053d (10), a69ec45 (11), a3293ab (cierre lote 1) | apunte/Apunte_Sistemas_de_Coordenadas.pdf (200 págs.) |
| D1 | Correcciones de D, mapa de transformaciones, significado geométrico de las operaciones, conjugación y congruencia | OK | 7f68a8b, bff959d, d8fe53f, 0d187df | — |
| D2 | Demostraciones con código: apunte/demostraciones, extracción de fragmentos, \comprobacion, CI | OK | 2b5f98a | — |
| E | E1 capítulos 12 a 15 — OK; E2 complementos C1–C4 y apéndices — pendiente | E1 OK, E2 pendiente | E1: 4f1194d, 71bb912, 93a7570, 5baeac2, 7beb529 | — |
| F | Hoja de estilo, estructura F1–F7 y pasada editorial de los capítulos 0 a 15 | OK, PARADA para revisión | 85004ed (F0, cero menciones prohibidas), 4a07400 (bitácoras al privado, cap. 11), 596a0d3 (hoja de estilo), f936a08 (estructura), 442485c (0–4), b8154c8 (5–8, con V1 y V2), 9591d53 (solicitud #1, cap. 5), 5419cd1 (9–15) y el commit de parada (este commit) | apunte/Apunte_Sistemas_de_Coordenadas.pdf (251 págs.) |

## Historial reescrito el 2026-10-19 (git filter-repo, rutas de material de terceros, datos personales y registros de proceso)

Espejo completo previo al filtro: Forgejo privado `gv/sistemas-de-coordenadas-respaldo-pre-filtro`. Material retirado: Forgejo privado `gv/sistemas-de-coordenadas-fuentes`.

| Referencia | Hash viejo | Hash nuevo |
|---|---|---|
| main (apunte v4 mergeado) | 897ce16 | fb4218f |
| refactor/apunte-por-tema (borrada, mergeada) | d71ee99 | c8266c7 |
| Fase 0 | 6c4f9b6 | 8203315 |
| Paso 1 (partición por tema) | a54da0a | 4798aa4 |
| Fase C (capítulo de SVD) | dec4296 | 7eb68bc |
| Fase A | 2bb7c4e | 2911915 |
| tag entrega-1 (B0) | ef6b397 | e3ef9f9 |
| Fase B | 60755ce | e1a1b6c |

## Sitio publicado

Verificado el 2026-10-19 04:22 -03.

- Merge a main: commit 9ea5124, tag entrega-2.
- Workflow pages.yml: run 23, success (build y deploy). Todos los pasos del job build en success. Paso «Búsqueda de términos sobre el artefacto»: `revisados: 39 html, 20 json, 1 xml, 1 pdf` y `TOTAL: 0 coincidencias fuera de las excepciones`.
- URLs en vivo (200, o 206 con range): portada, mapa, autoevaluación y apunte.pdf 4/4; fichas de capítulo 15/15; unidades 20/20; animaciones 6/6; redirección de 00_desaprender_el_cbc 200 con `url=../00_fundamentos/`. Sin ningún código distinto.
- PDF publicado: Last-Modified Mon, 19 Oct 2026 07:13:56 GMT, 141 páginas, título «Sistemas de Coordenadas: apunte (trabajo final)»; el SHA-256 coincide con el del PDF del commit de merge (518a63e5c3c0dcb9f6891ec11cd585bab4e6a6bb3dfd0c1a74e7679cdb9d7523).
- Búsqueda de términos sobre lo descargado del sitio vivo: `revisados: 39 html, 1 pdf`, `TOTAL: 0 coincidencias fuera de las excepciones`.
- Unidades 00_fundamentos y 01a_punto_quieto en Chrome real: cargan, con 29 y 22 celdas renderizadas y controles (00: 2 desplegables y 7 grupos de opciones; 01a: 3 deslizadores y 7 grupos de opciones). Sin errores de página ni «Unable to preload CSS»; sólo avisos de recursos precargados no usados.

## Fase D cerrada

Cerrada el 2026-10-19 04:59 -03.

| Capítulo | Título de la aplicación topográfica | Página del PDF |
|---|---|---|
| 1 | Acimut y estación total | 32 |
| 3 | Pasar un levantamiento local al sistema oficial | 60 |
| 5 | La pendiente del terreno como forma lineal | 96 |
| 6 | Superficie de una parcela por coordenadas | 107 |
| 7 | Deformación de una red de control entre dos épocas | 118 |
| 9 | Coordenadas de obra | 148 |
| 10 | Propagación de errores de una radiación | 160 |
| 11 | Ajuste de una red de nivelación | 171 |

- PDF: 200 páginas, título «Sistemas de Coordenadas: apunte (trabajo final)».
- Compilación con lualatex: 0 errores en el log, sin referencias indefinidas ni etiquetas duplicadas; 0 apariciones de «??» en el texto del PDF.
- Archivos que cumplen el mínimo: 10 de 26 (los capítulos 1, 2, 3, 5, 6, 7, 8, 9, 10 y 11); el capítulo 4 sigue sin aplicación topográfica.
- Enlaces y recuadros: 130 enlaces a unidades, 6 a animaciones, 25 recuadros, 0 rotos, 0 menciones prohibidas.
- Build del sitio con WASM: OK; búsqueda de términos sobre el sitio: `revisados: 39 html, 20 json, 1 xml, 1 pdf`, TOTAL 0.

## Fase F cerrada

- Páginas del PDF: 268 antes de F, 251 al cierre (252 antes de los recortes aprobados).
- `estilo.py` en 0 en todo el apunte y bloqueante en CI (`--estricto`, sin `continue-on-error`).
- El informe editorial vive en el repositorio privado (carpeta `revision/`), no en este.

### Decisiones pendientes para el editor

- Capítulos 2 y 4 quedan debajo de la meta de reducción (6,1 % y 9,0 %); bajar más exige tocar enunciados, demostraciones, ejemplos con cuentas o la aplicación.
- Capítulos 8 y 12: la matriz de covarianza o de dispersión usa la letra \(C\) del cambio de base; unificar (por ejemplo \(S\) o \(\Sigma\)), incluida la consigna de la unidad 11.
- Capítulo 7, `def:06-direccion-propia`: es el autovector con otro nombre; candidata a reducirse a una frase conservando la etiqueta.
- Capítulo 8: las definiciones «Forma cuadrática» y «Descomposición en valores singulares» no tienen `\label`.
- Capítulo 5, caja de SVM: cita el helper de `cb104.py`, cuyo nombre remite al código de la materia.
- Capítulos 5 a 8 quedan debajo de la meta del 15 % (6,3 % a 9,7 %); bajar más exige tocar ese material.
- Capítulo 15: \(\psi\) es la ordenada de Mercator en la loxodromia y la latitud geocéntrica en el 14; candidata a otra letra.
- Capítulo 15, «El triángulo polo--punto--punto»: el polo norte es \(N\), que en la aplicación del mismo capítulo es el radio del primer vertical.
- Capítulo 13: \(C\) y \(C_n\) nombran centros de osculadoras, además de la matriz \(C\) del cambio de base.
- Consignas de las unidades 9 y 11: notación \(B^{-1}AB\) y \(P^{+}=P/25\), distinta de la del texto (\(C^{-1}AC\), \(M^{+}=M/25\)); no se tocaron.
- Duplicados: los de los capítulos 9, 11 y 13 quedaron resueltos (ver «Decisión sobre la meta de páginas»); el capítulo 15 conserva sus dos demostraciones del teorema del coseno.
- Capítulo 15: la bibliografía es una lista con negritas; en 8 y 14 es un párrafo.
- Metas de 9 a 15: 5,0 % de líneas antes de los recortes aprobados; la meta de páginas quedó resuelta (ver «Decisión sobre la meta de páginas»).

### Decisión sobre la meta de páginas

F cierra en torno a 250 páginas (251 en el PDF actual); la meta de 240 queda descartada. Recortes aprobados y lo que se aplicó:

- Procedimiento duplicado entre los capítulos 9 y 11: queda completo donde se introduce y el otro lugar remite.
  - Capítulo 9: el ejemplo `ej:cb-diagonalizar` es la versión completa. El párrafo «Diagonalizar es elegir la grilla de los autovectores» pasa de 13 a 5 líneas: conserva \(A\), los autovalores, los autovectores y \(D\) (los usa el párrafo siguiente) y remite al ejemplo. El párrafo «Potencias y la trayectoria de un punto» pierde la cuenta de \(A^5\) con \(D^5\) y su lectura (11 líneas a 4): queda \(A^n=CD^nC^{-1}\) con remisión al ejemplo y el resultado de \(A^5\); la trayectoria con exponente real se conserva.
  - Capítulo 11: el párrafo «Sistema sobredeterminado» (recta por tres puntos) pasa de 20 a 5 líneas y remite a `ej:recta-cuatro-puntos`, del mismo capítulo, que tiene la cuenta completa; la figura `fig:inv-proyeccion` se conserva.
- Deducción por simetría del capítulo 13: la subsección «Hacia el elipsoide» tenía el argumento completo de las direcciones principales (reflexión en el plano meridiano, término cruzado nulo), el mismo de la demostración de `prop:elip-principales` del 14. Queda reducida a la afirmación de las direcciones y curvaturas principales con remisión a `prop:elip-principales` y a `sec:radios-MN` (8 líneas a 5); los valores numéricos de GRS80 se conservan porque los usa la aplicación del DEM. El capítulo 14 no se tocó.
- No se recorta: las dos demostraciones del teorema del coseno del capítulo 15, por ser enfoques distintos.

### Overfull restantes

Todos los avisos de más de 2 pt quedaron corregidos (8 antes, 2 después). Quedan:

| Archivo | Líneas | Tamaño |
|---|---|---:|
| `contenido/05-formas-lineales.tex` | 609–614 | 0,34 pt |
| `contenido/14-elipsoide.tex` | 97–101 | 0,20 pt |

## Entrega 3 publicada

Verificado el 2026-10-19 (hora local).

- Merge a main: commit 460a574 (`--no-ff` de revision-editorial 45bcb6b), tag anotado `entrega-3`; candidata previa `entrega-3-rc` = 73b4f81.
- Contenido: fase F completa; fase G en los capítulos 0 a 4, 10 a 13 y 15; laboratorio CAD en los capítulos 1 a 4; menús por capítulo (`menu.html`, `menu.pdf`, `menu-por-capitulo.html`); problemas por capítulo con respuestas (apéndice A.6, `tools/problemas/gen.py`); barrido de «estación total»; compilación protegida (`scripts/compilar_pdf.sh`, hooks `.githooks`).
- Workflow pages.yml: run 31, success (build y deploy), con el paso «Verificar el PDF commiteado» y la búsqueda de términos sobre el artefacto en 0.
- En vivo: 200 en portada, menús, `cad/` y DXF, mapa, autoevaluación, fichas y unidades; las 15 redirecciones `clases/NN.html` llevan a `capitulos/NN.html`; `apunte.pdf` publicado con 290 páginas, igual a `apunte/paginas_esperadas.txt`, y SHA-256 idéntico al PDF del tag `entrega-3`.
- Pendiente después de la entrega: fase G en 5 a 9 y 14, laboratorio CAD de 6 y 9, complementos C1 a C4, pasada de notación (incluye NumPy en el texto de 1, 4, 6 y 7).


## Entrega 4 candidata (2026-10-19)

Rama `revision-editorial`, sobre la entrega 3 (main 460a574). Olas del bloque «terminar hoy todo lo pendiente después del MVP»:

- Ola 0: PR #6 del editor (problema 12.5 sin Overfull), merge `--no-ff` 9946a6d.
- Ola 1, fase G en los capítulos que faltaban (un agente por capítulo, en worktrees; solo el `.tex` en cada commit): 5 (435e051), 6 (927b53d), 7 (c08ccbb), 8 (2172b28), 9 (3804bbd), 14 (9e4ac42). Con esto los 16 capítulos tienen la voz para el aula. Contador: 5: 5,2 → 2,3 términos cada 100 líneas; 6: 2,4 → 1,9; 7: 4,1 → 3,0; 8: 5,3 → 3,6 (instrumentos 4 → 0); 9: 5,5 → 2,6; 14: 5,2 → 3,8. «La idea» con 9 a 21 preguntas o experimentos en cada uno. Sin Overfull en el apunte.
- Ola 1, laboratorio CAD tanda 2: 322563e (ejercicios `cap06_area`, `cap06_scale`, `cap09_ucs` con 5 respuestas; `que_matriz.py` informa el cociente de áreas; pruebas 37 → 56) y 379ebae (subsecciones `sec:cad-cap06` y `sec:cad-cap09`). Los platos CAD de 6 y 9 pasan a «listo» en los dos menús.
- Ola 1, complementos al mínimo del molde con voz para el aula (E2): C1 3d3b79e, C2 0455b97, C3 779ef82, C4 083f01c; ESTADO_NOTAS 7490e7b. Complementos que cumplen el mínimo: 4 de 4.
- Ola 2, pasada de notación y demostraciones (un solo agente): deef0d4. Tabla del capítulo 0 como única referencia; σ_B, τ_v, ρ_{c,θ} en 2 y 3; Σ con subíndice para la dispersión en 8 y 12; «rango A» en 11; m_tot en 12; capítulo 9 sin letras repetidas; problema 08-4 regenerado desde `gen.py`; demostraciones nuevas de `teo:traslacion-dos-reflexiones-enunciado`, `teo:rotacion-dos-reflexiones-enunciado`, `prop:generador` y `teo:legendre`.
- Decisiones del editor aplicadas en commits separados: fb5bab4 (se retira `capc2_conformes.py`), 32144b1 (C2 sin el enlace «Unidad 19»), f403e4f (C1: μ_i en el patrón), def5d6e (`estilo.py`: «Copernicus DEM GLO-30» no cuenta), 2163ace (C4: caja «Por qué las coordenadas forman una grilla» con el ejemplo de los 100 km verificado), 152ee49 (C4: cita Rodríguez 2007 y bibliografía del IGN).
- Ola 3: PDF 37a83a0 (328 páginas, 0 Overfull, 0 `!`, 0 referencias sin definir), ESTADO 30846c3 (15 de 15, 4 de 4, 97 resultados). Controles de la CI en 0: estilo estricto, prohibidas (árbol y sitio), enlaces, pytest 62.

Decisiones pendientes del editor (en ESTADO_NOTAS.md y en la bitácora privada): matriz que refleja (S en el 2, H en el 3); puntos de control P_i en mayúscula en el 9; consignas de las unidades 9, 11 y 12 con su notación propia; figura `cap09_conjugacion.pdf` puede rotular T_c; `\refl` sigue definida en el `.sty` sin uso.
