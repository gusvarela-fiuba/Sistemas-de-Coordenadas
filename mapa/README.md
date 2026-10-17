# mapa/

Mapa de conceptos de la materia: nodos (conceptos), columnas (clases del esqueleto 2025 del profesor) y aristas (`requiere`).

- `CONCEPTOS.md` — vocabulario canónico de ids (un concepto, un id; agregar acá antes de usarlo).
- `ESQUEMA.md` — esquema de `mapa.yaml` y reglas que valida `tools/build.py`.
- `_fragmentos/bloque-*.yaml` — **la fuente editable** de clases y conceptos, un fragmento por bloque de clases (01-03, 03p-06, 07-10, 11-14). Cada clase lleva, además del esqueleto, `pregunta` (una línea), `validacion` (`pendiente` | `revisado` | `validado-catedra`) y `nivel` (`troncal` | `complementario` | `avanzado`).
- `_fragmentos/unidades.yaml` — **la fuente editable** de las unidades marimo: `id, archivo, titulo, estado, clases[], pregunta, gancho_agrimensura, nivel`. Su orden es el de las estaciones de la portada (`docs/camino.md`).
- `mapa.yaml` — **generado**: la mezcla de los fragmentos más las unidades. No se edita a mano.

Flujo: editar el fragmento (o `unidades.yaml`) que corresponda, correr `uv run tools/merge_mapa.py` (ordena clases, concatena conceptos, detecta ids duplicados o fuera de `CONCEPTOS.md`, valida vocabularios y que las `clases` de cada unidad existan; con errores no escribe y sale 1) y después `uv run tools/build.py`.

Fechas 2025: `fecha_2025` sólo si el campus la da; si no, `null` y la estimación en `fecha_2025_estimada`.
