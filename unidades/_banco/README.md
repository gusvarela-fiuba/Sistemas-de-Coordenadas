# Fragmentos del banco de autoevaluación

Fuente editable del banco de 120 preguntas (6 por unidad: 2 elementales, 2 medias, 2 avanzadas). Un archivo por
bloque de unidades, `bloque_N.py`, que define `BANCO = {"<id de unidad>": [pregunta, ...]}`.

`uv run python tools/merge_banco.py` valida los fragmentos y genera `unidades/banco_autoevaluacion.py` (no se edita a
mano; `cb104.py` lo importa y `tools/build.py` lo embebe en cada export WASM).

Esquema de cada pregunta:

```python
{
    "id": "06_m1",                 # único en todo el banco: <unidad corta>_<e|m|a><1|2>
    "nivel": "medio",              # elemental | medio | avanzado
    "enunciado": "...",            # primera persona del plural, LaTeX entre $...$ (KaTeX)
    "opciones": [                  # exactamente 4, exactamente una correcta
        {"id": "a", "texto": "...", "correcta": True,  "explicacion": "..."},
        {"id": "b", "texto": "...", "correcta": False, "explicacion": "..."},
        {"id": "c", "texto": "...", "correcta": False, "explicacion": "..."},
        {"id": "d", "texto": "...", "correcta": False, "explicacion": "..."},
    ],
    "rubrica": "...",              # opcional: celda de la rúbrica del apéndice 19 que cubre
}
```
