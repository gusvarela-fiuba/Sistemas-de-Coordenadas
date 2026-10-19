Fichas por capítulo del programa de la materia: una ficha de tema por capítulo, con el mismo formato en las 15 (la 3p es el complemento C1 de proyectivas). El id de la ficha (nombre del archivo, `clase` del frontmatter) es el orden interno del programa; el rótulo visible usa la numeración del PDF: la ficha 03 cubre los capítulos 3 y 4, de la 04 a la 14 el capítulo es el id más uno (la 04 es el capítulo 5, la 14 es el 15) y la 03p es el «Complemento C1».

Cada ficha empieza con un frontmatter YAML: `clase` (1 a 14, o "3p"), `titulo` («Capítulo N: …», con la numeración del PDF; «Capítulos 3 y 4: …» en la 03; «Complemento C1: …» en la 03p), `idea` (una frase), `que_se_estudia` (3 a 6 ítems), `conceptos_previos`, `apunte` (claves de `\label{cap:…}`; el sitio las muestra como «Capítulo 1. Título» con los datos de `apunte/numeracion.json`, que genera `apunte/scripts/numeracion.py` tras compilar el apunte), `unidades` (ids de `unidades/*.py`), `animaciones` (nombres de `animaciones/*.mp4` sin extensión) y `ejercicios_sugeridos` (2 a 4 ítems).

El cuerpo tiene seis secciones, en este orden: «Qué se estudia», «Conceptos previos», «En el apunte», «Unidades interactivas», «Animaciones» (si hay) y «Ejercicios sugeridos».

`tools/build.py` valida el frontmatter y arma en el sitio las secciones de apunte, unidades y animaciones con sus enlaces. `PLANTILLA.md` es el molde.
