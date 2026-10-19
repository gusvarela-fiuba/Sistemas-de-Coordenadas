# mapa/

Mapa de conceptos de la materia: nodos (conceptos), columnas (fichas del programa de la materia) y aristas (`requiere`).

- `CONCEPTOS.md` — vocabulario canónico de ids (un concepto, un id; agregar acá antes de usarlo).
- `ESQUEMA.md` — esquema de `mapa.yaml` y reglas que valida `tools/build.py`.
- `_fragmentos/bloque-*.yaml` — **la fuente editable** de fichas y conceptos, un fragmento por bloque de fichas (01-03, 03p-06, 07-10, 11-14). Cada ficha lleva, además de los temas, `pregunta` (una línea) y `nivel` (`troncal` | `complementario` | `avanzado`).
- `_fragmentos/unidades.yaml` — **la fuente editable** de las unidades marimo: `id, archivo, titulo, estado, clases[], pregunta, gancho_agrimensura, nivel`. Su orden es el de las unidades en la portada (`docs/camino.md`).
- `mapa.yaml` — **generado**: la mezcla de los fragmentos más las unidades. No se edita a mano.

Flujo: editar el fragmento (o `unidades.yaml`) que corresponda, correr `uv run tools/merge_mapa.py` (ordena fichas, concatena conceptos, detecta ids duplicados o fuera de `CONCEPTOS.md`, valida vocabularios y que las `clases` de cada unidad existan; con errores no escribe y sale 1) y después `uv run tools/build.py`.
