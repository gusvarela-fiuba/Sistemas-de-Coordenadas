# fuentes/ — material primario de CB104 Sistemas de Coordenadas

Fuentes crudas de la materia CB104 Sistemas de Coordenadas (Agrimensura, FIUBA; profesor Javier Clavijo; cursada 2C2026). Nada de esta carpeta está resumido ni reescrito: son copias fieles de lo que entregó el campus, Notion o las notas propias. Lo elaborado (apuntes, notebooks, entregas) vive fuera de `fuentes/`.

## Subcarpetas

### `campus/`

Material bajado del campus virtual (campusgrado.fi.uba.ar, curso 1279).

- `resumenes_clase_2025_profesor.md`: resúmenes clase por clase escritos por el profesor para la cursada 2025 (el campus los titula "1er Cuatri 2026"), clases 1 a 14. Las clases 1–10 fueron copiadas del campus el 2026-09-21; las clases 11–14 vienen del PDF `campus/clase_por_clase_2do_2025_campus_2026-10-17.pdf` guardado en Dropbox (las 13 y 14 sólo tienen título). Mismo archivo que el de Dropbox `Agrimensura/Sistemas de Coordenadas/campus/`.

### `campus/profesor/`

Archivos que el profesor mandó por el grupo de Google Chat (recibidos el 2026-10-17): la foto del pizarrón del 2026-09-16 con la consigna del pentágono, la planilla `Proyectivas_del_pentagono.xlsx` con la que calculó una proyectiva del pentágono el 23/9, y `LaSVD.wxmx`, la SVD analítica en wxMaxima que mencionó el 14/10. Detalle de cada uno en `campus/profesor/README.md`.

En la misma carpeta están también las 7 fotos del pizarrón del miércoles 2026-09-30 (formas lineales, cambio de base y diagonalización) que Gustavo sacó en clase, no mandadas por el chat: `2026-09-30_pizarron_dualidad_cajas.jpg`, `2026-09-30_pizarron_formas_ejercicio_antes_corregir.jpg`, `2026-09-30_pizarron_formas_ejercicio_corregido.jpg`, `2026-09-30_calc_formas_inversa.jpg`, `2026-09-30_pizarron_cambio_base_grillas_munequitos.jpg`, `2026-09-30_pizarron_matriz_A_autovectores_columnas.jpg` y `2026-09-30_pizarron_despeje_diagonalizacion.jpg`. Qué muestra cada una, en `campus/profesor/README.md`.

### `transcripciones/`

Notas de reunión generadas por Notion AI a partir de la grabación de cada clase de la cursada 2C2026. Un archivo por clase, `AAAA-MM-DD.md`, con front-matter (`fecha`, `materia`, `origen`, `notion_id`, `estado`) y dos secciones: el resumen que armó Notion y el transcript crudo, un párrafo por línea.

- `2026-08-19.md` — Rotaciones. En castellano.
- `2026-09-16.md` — Determinantes, producto vectorial, autovectores. En inglés.
- `2026-09-30.md` — Cambio de base, curvas de nivel, diagonalización. En inglés.
- `2026-10-14.md` — Conjuntos de nivel, gradiente, teorema de la función implícita. En inglés.

Importante: los textos en inglés son **traducciones automáticas de Notion** de una clase dictada en castellano. El transcript es reconocimiento de voz + traducción automática, con errores de transcripción y términos mal traducidos ("car" por "autovalor", "theater product", etc.). Sirven como fuente primaria para reconstruir qué se dijo, no como texto citable.

Clases de 2C2026 y qué hay de cada una:

| Fecha | Transcripción |
|---|---|
| 2026-08-19 | sí (castellano) |
| 2026-08-26 | no hubo clase |
| 2026-09-02 | no (Gustavo ausente) |
| 2026-09-09 | no |
| 2026-09-16 | sí (inglés) |
| 2026-09-23 | no (la nota de Notion está vacía) |
| 2026-09-30 | sí (inglés); además 7 fotos del pizarrón en `campus/profesor/` |
| 2026-10-07 | no (sin nota en Notion; cambio de base y SVD según el cronograma que confirmó el profesor) |
| 2026-10-14 | sí (inglés) |

### `notion/`

Páginas propias de Gustavo en Notion, transcriptas a Markdown con fórmulas en `$…$` / `$$…$$`.

- `sistemas_de_coordenadas_geometria_diferencial.md`: página "🌐 Sistemas de Coordenadas" (2026-08-22, bajo "📐 Geometría Diferencial"): parametrización de superficies, primera forma fundamental, tensor métrico, esfera, matrices de rotación, exponencial de matrices.
