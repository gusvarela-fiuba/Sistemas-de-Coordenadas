# Sistemas de Coordenadas (CB104) — material de estudio

Material de estudio de la materia CB104 Sistemas de Coordenadas (Agrimensura, FIUBA), hecho por Gustavo Varela como alumno. Tiene dos objetivos: aprobar la materia y dejarle a la cátedra una herramienta interactiva reutilizable.

Qué hay adentro:

- Unidades marimo con animaciones (rotaciones, proyectivas, autovalores y autovectores) que se pueden correr y modificar en el navegador.
- Un mapa de conceptos (nodos y aristas) que hila las clases del cuatrimestre.
- Un apunte LaTeX que funciona como anexo de demostraciones.
- Las entregas de la cursada.

## Estructura

```
clases/     fichas por clase, siguiendo el esqueleto del profesor
fuentes/    transcripciones de clase y material del campus
unidades/   notebooks marimo (una unidad por tema, con animaciones)
apunte/     apunte LaTeX (fuente, portada, contenido por capítulo)
mapa/       grafo de conceptos (mapa.yaml)
tools/      scripts auxiliares (bootstrap, build, publicación)
entregas/   trabajos prácticos entregados
datos/      datos de apoyo (los archivos pesados quedan fuera del repo)
```

## Cómo correr local

Todo Python va por `uv`; no se usa el Python del sistema.

```
uv sync
uv run marimo edit unidades/<archivo>.py
```

Para compilar el apunte (TeX Live, LuaLaTeX), desde `apunte/`:

```
cd apunte
lualatex -interaction=nonstopmode Apunte_Sistemas_de_Coordenadas.tex
lualatex -interaction=nonstopmode Apunte_Sistemas_de_Coordenadas.tex
lualatex -interaction=nonstopmode Apunte_Sistemas_de_Coordenadas.tex
```

Tres pasadas para que cierren índice y referencias cruzadas. Los temporales (`.aux`, `.log`, `.toc`, etc.) están ignorados por git.

## Sitio

El material se publica en GitHub Pages: https://gusvarela-fiuba.github.io/sistemas-de-coordenadas/ (en construcción).

## Licencia

Licencia: a definir.
