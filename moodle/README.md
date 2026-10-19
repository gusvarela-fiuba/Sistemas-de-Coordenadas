# moodle/

`moodle_banco_120_preguntas_cb104.xml` es el banco de autoevaluación de CB104 (6 preguntas por unidad: 2 elementales, 2 medias, 2 avanzadas, opción múltiple con explicación por opción) en formato Moodle XML, con una categoría por unidad y nivel bajo `CB104_Sistemas_de_Coordenadas`.
Lo generamos desde los fragmentos de `unidades/_banco/`: `uv run python tools/merge_banco.py && uv run python tools/exportar_moodle_xml.py` (con `--parcial` en ambos mientras el banco no esté completo).
Las fórmulas van como `\( ... \)` y `\[ ... \]` para el filtro MathJax del Campus FIUBA.
Para cargarlo: Banco de preguntas → Importar → formato "Moodle XML", subir el archivo e importar; las categorías se crean solas.
