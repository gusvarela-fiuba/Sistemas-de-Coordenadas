Fichas por clase del programa de la materia: una ficha de tema por clase, con el mismo formato en las 15 (la 3p es el complemento de proyectivas).

Cada ficha empieza con un frontmatter YAML: `clase` (1 a 14, o "3p"), `titulo` («Clase N: …»), `idea` (una frase), `que_se_estudia` (3 a 6 ítems), `conceptos_previos`, `apunte` (claves de `\label{cap:…}`), `unidades` (ids de `unidades/*.py`), `animaciones` (nombres de `animaciones/*.mp4` sin extensión) y `ejercicios_sugeridos` (2 a 4 ítems).

El cuerpo tiene seis secciones, en este orden: «Qué se estudia», «Conceptos previos», «En el apunte», «Unidades interactivas», «Animaciones» (si hay) y «Ejercicios sugeridos».

`tools/build.py` valida el frontmatter y arma en el sitio las secciones de apunte, unidades y animaciones con sus enlaces. `PLANTILLA.md` es el molde.
