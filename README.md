# Sistemas de Coordenadas (CB104) — guía de estudio interactiva

Guía de estudio de la materia CB104 Sistemas de Coordenadas (Agrimensura, FIUBA), escrita por Gustavo Varela como alumno de la cursada 2026. No es material oficial de la cátedra: es la manera en que un alumno recorre la materia, con dos objetivos, aprobarla y dejar una herramienta interactiva reutilizable.

Sitio: https://gusvarela-fiuba.github.io/sistemas-de-coordenadas/

## Qué es

Tres capas, de la más guiada a la más completa:

- **El camino** (la portada): 19 estaciones, una por lección, en el orden del profesor, precedidas por la Estación 0 (encuadre propio del autor: cuatro cosas para desaprender del CBC). Cada estación tiene su pregunta de campo, su gancho de agrimensura, su estado y la lección marimo, que corre en el navegador (WebAssembly, sin instalar nada): situación de campo y predicción, hecho geométrico, manipulación con una figura de tres capas, cuenta a mano y código lado a lado, un Python de hoy y ejercicios.
- **El mapa** (`mapa.html`): los conceptos de las 14 clases como grafo, con filtro de ruta (troncal / todo) y un control "hasta la clase N". Es la herramienta de repaso.
- **El apunte** (`apunte.pdf`): anexo de demostraciones en LaTeX, enlazado por sección desde cada estación. Las fichas por clase (`clases/`) siguen el esqueleto del profesor.

El diseño del camino (principios, secuencia de una lección, datos que lo alimentan, estado actual) está en `docs/camino.md`.

## Cómo correr local

Todo Python va por `uv`; no se usa el Python del sistema.

```
uv sync
uv run python tools/build.py --skip-wasm      # portada, mapa, fichas y apunte.pdf en site/ (sin exportar lecciones)
uv run python -m http.server -d site 8765     # http://localhost:8765/
```

`uv run python tools/build.py` sin `--skip-wasm` exporta además las 19 lecciones a WebAssembly (1–2 s cada una, ~27 MB por lección en `site/unidades/`); para una sola, `--only NN_nombre`. Las lecciones exportadas necesitan HTTP, no andan desde `file://`. Para editar una lección: `uv run marimo edit unidades/NN_nombre.py`. El flujo completo, el molde de lección y cómo agregar una están en `tools/README.md`.

El apunte se compila aparte con TeX Live (LuaLaTeX, tres pasadas desde `apunte/`, ver `apunte/README.md`); el PDF compilado está commiteado y el build lo copia a `site/apunte.pdf`, así que ni el runner de GitHub ni quien clona necesitan TeX.

## Estructura

```
unidades/   lecciones marimo (NN_nombre.py), módulo común cb104.py y PLANTILLA_leccion.py
mapa/       fuente editable del mapa (_fragmentos/*.yaml), mapa.yaml generado, ESQUEMA.md y CONCEPTOS.md
clases/     fichas por clase, siguiendo el esqueleto del profesor
apunte/     apunte LaTeX (fuente por capítulo) y el PDF compilado
docs/       camino.md (diseño de la guía y estado) y auditoria.md (auditoría del material)
tools/      build.py (sitio), merge_mapa.py (mapa), bootstrap_github.sh y el README con el flujo
ejercicios/ resoluciones del material Julia del curso y sus ports a Python
entregas/   trabajos prácticos entregados
fuentes/    transcripciones de clase y material del campus
datos/      datos de apoyo (los archivos pesados quedan fuera del repo)
site/       salida del build (ignorada por git); la publica .github/workflows/pages.yml
```

## Procedencia y validación

Cada clase lleva dos etiquetas independientes, visibles en las fichas y en las estaciones:

- **Procedencia** (de dónde sale el contenido): `con transcripción` (hay transcripción de la clase dictada en 2026); `reconstruida` (armada desde el material del campus y la cursada 2025, sin transcripción); `no dictada` (la clase no se dio: todavía no llegó, o en 2C2026 se salteó, como la 02); `anticipación, pendiente de validar` (lección armada antes de que la clase se dicte; hoy las clases 07 y 10–14, es decir las lecciones 09, 11, 12, 13 y 14).
- **Validación** (cuánto se revisó): `validación pendiente`; `revisado` (revisada por el autor contra el material); `validado por la cátedra` (confirmada por el profesor). Hoy todas las clases están en `pendiente`.

Nada se presenta como contenido de la cátedra si no se dio. Las lecciones tienen además un estado propio (`piloto`, `migrada`, `legacy`, `pendiente`) que dice si se exportan; el estado de cada estación (lista / en clase / todavía no) lo calcula el build.

## Publicación

Cada push a `main` corre `.github/workflows/pages.yml`: `uv sync --frozen`, verificación de que `mapa/mapa.yaml` coincide con los fragmentos, `marimo check` de las lecciones, `tools/build.py` y despliegue a GitHub Pages. En los pull requests corre sólo el build, como CI. Una vez por repo: Settings → Pages → Source: GitHub Actions.

## Licencia

Doble esquema: el contenido (texto de las lecciones, fichas, apunte y mapa de conceptos) es CC BY-SA 4.0 (`LICENSE`) y el código (`tools/`, `unidades/cb104.py` y el código de los notebooks) es MIT (`LICENSE-CODE`); titular Gustavo Varela, 2026.
No están cubiertos los PDFs de la cátedra ni la bibliografía citada: son de sus autores y no se redistribuyen en el repo, salvo los del profesor ya incluidos en `apunte/` (`01_Ejercicios_original.pdf`, `02_afinidad_original.pdf`), que quedan como material de la cátedra.
Esta licencia es una propuesta del asistente, pendiente de confirmación de Gustavo.
