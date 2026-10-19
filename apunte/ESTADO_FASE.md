# Estado de las fases del plan de cierre

Actualizado en cada commit de fase. Formato de commit: `[FASE-X] [OK|PARADA|BLOQUEO] título`.

| Fase | Contenido | Estado | Commit | PDF |
|---|---|---|---|---|
| 0 | Informe de lectura e infraestructura LaTeX | OK | 6c4f9b6 | — |
| Piloto | Capítulos de rotaciones y afines con el molde | OK | da54735, 0e56d71 | — |
| Paso 1 | Partición en un capítulo por clase y remapeo de labels | OK (aprobado) | a54da0a | — |
| Portada / renombre / cita | Trabajo final CB104; 03 renombrado; condiciones de uso sólo en el repositorio, CITATION y nota | OK | 93740dd, 1f9eeee, 78fa328 | — |
| A | Línea de base (ESTADO.md), Overfull, título interno | OK (aprobada) | 2bb7c4e | — |
| C | Capítulo de SVD, la lectura de las curvas de nivel | OK (aprobado condicionado a lectura) | dec4296 | — |
| B0 | Entrega-1: cero menciones prohibidas, proyectivas, conformes; limpieza del maestro | OK (aprobada) | ef6b397 (tag entrega-1), 622fd50 | entregas/2026-10-19_entrega-1.pdf |
| B | Capítulo 0 fusionado, apéndices ap1–ap6, capítulo 3 partido en 3 y 4 con renumeración, capítulo 2 reescrito | OK, PARADA para revisión | (dos commits de esta fase) | entregas/2026-10-19_fase-B.pdf |
| B1 | Limpieza fuera del PDF: respaldo, fichas, unidades, mapa, banco, herramientas, README, documentos internos, datos personales, enlaces del PDF, historial reescrito | OK, mergeada a main (entrega-2) | d592233, 7752ecb, 9ea5124 | entregas/2026-10-19_fase-B1.pdf |
| D | Capítulos 1 (aplicación), 3, 5, 6, 7, 9, 10 y 11 al molde | OK, PARADA para revisión | 3bf947a (cap. 1), fe14333 (3), 774b234 (5), df62300 (6), de47fcc (7), 195708d (9), a29053d (10), a69ec45 (11), a3293ab (cierre lote 1) | apunte/Apunte_Sistemas_de_Coordenadas.pdf (200 págs.) |
| E | Complementos C1–C4 y apéndices | pendiente | — | — |
| F | Pasada editorial final e INFORME_FINAL.md | pendiente | — | — |

## Historial reescrito el 2026-10-19 (git filter-repo, rutas de material de terceros, datos personales y registros de proceso)

Espejo completo previo al filtro: Forgejo privado `gv/sistemas-de-coordenadas-respaldo-pre-filtro`. Material retirado: Forgejo privado `gv/sistemas-de-coordenadas-fuentes`.

| Referencia | Hash viejo | Hash nuevo |
|---|---|---|
| main (apunte v4 mergeado) | 897ce16 | fb4218f |
| refactor/apunte-por-tema (borrada, mergeada) | d71ee99 | c8266c7 |
| Fase 0 | 6c4f9b6 | 8203315 |
| Paso 1 (partición por clase) | a54da0a | 4798aa4 |
| Fase C (capítulo de SVD) | dec4296 | 7eb68bc |
| Fase A | 2bb7c4e | 2911915 |
| tag entrega-1 (B0) | ef6b397 | e3ef9f9 |
| Fase B | 60755ce | e1a1b6c |

## Sitio publicado

Verificado el 2026-10-19 04:22 -03.

- Merge a main: commit 9ea5124, tag entrega-2.
- Workflow pages.yml: run 23, success (build y deploy). Todos los pasos del job build en success. Paso «Búsqueda de términos sobre el artefacto»: `revisados: 39 html, 20 json, 1 xml, 1 pdf` y `TOTAL: 0 coincidencias fuera de las excepciones`.
- URLs en vivo (200, o 206 con range): portada, mapa, autoevaluación y apunte.pdf 4/4; fichas de clase 15/15; unidades 20/20; animaciones 6/6; redirección de 00_desaprender_el_cbc 200 con `url=../00_fundamentos/`. Sin ningún código distinto.
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
