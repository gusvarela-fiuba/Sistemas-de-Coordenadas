# mapa/

Mapa de conceptos de la materia: nodos (conceptos), columnas (clases del esqueleto 2025 del profesor) y aristas (`requiere`).

- `CONCEPTOS.md` — vocabulario canónico de ids (un concepto, un id; agregar acá antes de usarlo).
- `ESQUEMA.md` — esquema de `mapa.yaml` y reglas que valida `tools/build.py`.
- `_fragmentos/bloque-*.yaml` — **la fuente editable**, un fragmento por bloque de clases (01-03, 03p-06, 07-10, 11-14).
- `mapa.yaml` — **generado**: la mezcla de los fragmentos más la lista de unidades. No se edita a mano.

Flujo: editar el fragmento que corresponda, correr `uv run tools/merge_mapa.py` (ordena clases, concatena conceptos, detecta ids duplicados o fuera de `CONCEPTOS.md`, arma `unidades`) y después `uv run tools/build.py`. La lista de unidades marimo (archivo, estado, título) vive en `UNIDADES` dentro de `tools/merge_mapa.py`.

Fechas 2025: `fecha_2025` sólo si el campus la da; si no, `null` y la estimación en `fecha_2025_estimada`.
