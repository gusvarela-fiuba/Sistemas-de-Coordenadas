# Esquema de `mapa/mapa.yaml`

`mapa.yaml` es la única fuente que lee `tools/build.py` para armar el sitio. Es un archivo **generado**: se edita en `mapa/_fragmentos/bloque-*.yaml` (clases y conceptos) y `mapa/_fragmentos/unidades.yaml` (unidades), y se regenera con `uv run tools/merge_mapa.py` (ver `mapa/README.md`). Tiene tres listas: `clases` (el programa de la materia), `conceptos` (los nodos del mapa) y `unidades` (los notebooks marimo, que en la portada son las unidades del hilo conductor; ver `docs/camino.md`). El merge y el build validan las referencias cruzadas antes de generar nada.

```yaml
titulo: Sistemas de Coordenadas — mapa de conceptos
pregunta_guia: "transformaciones ↔ operaciones ↔ coordenadas"

clases:                          # 15 entradas, en el orden del programa (la 3p es el complemento de proyectivas)
  - id: "01"                     # string de dos dígitos; único; define el orden de las columnas del mapa
    titulo: Rotaciones
    ficha: clases/01-rotaciones.md   # ruta relativa a la raíz del repo; si no existe, el build avisa (warning) y sigue
    nivel: troncal               # ruta de estudio: troncal | complementario | avanzado (filtro de ruta en mapa.html)
    pregunta: "¿Qué se conserva cuando giro, y cómo escribo ese giro como una cuenta?"   # una línea, pregunta de campo que la clase responde
    apunte: ["proyectivas"]      # OPCIONAL: claves \label{cap:<clave>} del apunte; si falta, se infiere de los conceptos de la clase

conceptos:
  - id: rotacion                 # slug único, minúsculas, guion medio
    nombre: Rotación             # texto del nodo
    clase: "01"                  # id de una clase existente (columna donde se dibuja)
    unidad: 01_rotaciones        # OPCIONAL: id de una unidad existente; el nodo linkea ahí (si no, a la ficha de la clase)
    unidades: [01_rotaciones, 02_producto_interno]   # OPCIONAL: ids de unidades existentes para un nodo transversal; si falta `unidad`, se toma la primera (el nodo linkea ahí) y la lista completa va al tooltip
    hecho_geometrico: "dejar quieto un punto, mover otro, acomodar el resto conservando distancias y ángulos"
    que_se_conserva: "distancias y ángulos"
    apunte: ["proyectivas", "14", "15"]   # claves \label{cap:<clave>}: capítulos por nombre ("rotaciones", …), apéndices por número ("14" … "22"); cada una tiene que existir
    requiere: [producto-interno] # ids de conceptos que lo motivan; se dibujan como flechas requerido → concepto

unidades:                        # fuente: mapa/_fragmentos/unidades.yaml; su orden es el de las unidades en la portada
  - id: 01_rotaciones            # único; es el nombre de la carpeta site/unidades/<id>/
    archivo: unidades/01_rotaciones.py   # ruta relativa a la raíz; tiene que existir si el estado se exporta
    titulo: Rotaciones
    estado: piloto               # piloto | migrada | legacy | pendiente
    clases: ["01", "02"]         # ids de clase que cubre (según CONCEPTOS.md y el `unidad` de los conceptos); cada uno tiene que existir
    pregunta: "¿Qué le pasa a cada punto de la parcela cuando giro los ejes…?"   # una línea; la pregunta de campo de la unidad
    gancho_agrimensura: "La estación total mide en sus propios ejes; …"           # una línea; situación de campo (sin fajas ni EPSG)
    nivel: troncal               # troncal | complementario | avanzado
```

El `estado` de una **unidad** es interno (decide qué se exporta); en el sitio una unidad sin exportar figura como «en preparación».Las clases que ninguna unidad cubre (hoy 11–14) van a la última unidad, "Lo que viene".

## Reglas que valida `tools/build.py`

Errores (el build se detiene):

- ids duplicados en `clases`, `conceptos` o `unidades`;
- `conceptos[].clase` que no sea un id de `clases`;
- `conceptos[].unidad` declarado que no sea un id de `unidades`;
- `conceptos[].requiere` con ids que no están en `conceptos` (o que se refieren a sí mismos);
- claves de `apunte` (en conceptos o clases) sin `\label{cap:<clave>}` en los `.tex` que incluye el maestro;
- `unidades[].archivo` inexistente cuando el estado es `piloto` o `migrada`;
- `unidades[].clases` vacío o con ids que no están en `clases`;
- `estado` de unidad fuera del vocabulario (`piloto`, `migrada`, `legacy`, `pendiente`) o `nivel` (clases y unidades) fuera del vocabulario;
- frontmatter de las fichas de `clases/` que no cumpla el esquema de `clases/README.md` (campos, cantidad de ítems, claves de apunte, unidades y animaciones existentes).

(`merge_mapa.py` valida lo mismo sobre los fragmentos y además exige que `pregunta` y `gancho_agrimensura` sean una línea de texto.)

Avisos (el build sigue):

- `clases[].ficha` que todavía no existe (la fase 1 las va escribiendo);
- unidad con estado `legacy` o `pendiente` (no se exporta: `build.py` sólo exporta `piloto` y `migrada`);
- concepto sin `hecho_geometrico` (el hover del nodo queda vacío);
- clase sin `pregunta`, unidad sin `pregunta` o sin `gancho_agrimensura`.

## Qué hace el build con cada campo

- Portada (`index.html`, el hilo conductor): una entrada por unidad en el orden de `unidades.yaml`, con `titulo`, `pregunta`, `gancho_agrimensura`, `nivel`, sus `clases`, link a la unidad si está exportada, a las fichas y a las secciones del apunte (`apunte.pdf#nameddest=cap:<clave>`). Entradas: *Empezar* (unidad 0), *Seguir el programa* (la unidad siguiente a la última marcada en `PROGRAMA_AVANCE`, lista interna de `build.py`), *Repasar* (`mapa.html`), *Autoevaluación*.
- Mapa (`mapa.html`): columnas = `clases` en orden de aparición, todos los nodos del mismo color. Cada nodo lleva `data-nivel` (el `nivel` de su clase) y `data-orden` (posición de la clase) para el filtro de ruta (`troncal` / `todo`) y el deslizador "hasta la clase N" (opacity 0.25 para lo posterior; default N = última clase de `PROGRAMA_AVANCE`).
- Nodo: `nombre`; `<title>` = `hecho_geometrico`; link a `unidades/<unidad>/` si el concepto declara `unidad` y esa unidad se exportó, si no a `clases/<clase>.html`.
- Aristas: `requiere`; la flecha va del requerido al concepto.
- Lista de clases (en `mapa.html`): etiqueta de `nivel`, links a ficha, unidades (las de sus conceptos) y secciones del apunte (título tomado del encabezado que lleva el `\label{cap:<clave>}`).
- Fichas: se arman desde `clases/*.md`; las secciones «En el apunte», «Unidades interactivas» y «Animaciones» salen del frontmatter y llevan enlaces.

## Convenciones

- Claves del apunte: el label sin `cap:` (`"rotaciones"`; los apéndices, dos dígitos como string: `"14"`).
- Ids de clase también como string (`"01"`): YAML convertiría `01` en el entero 1.
- Sin acentos en ids; con acentos en `nombre`/`titulo` (es lo que se muestra).
