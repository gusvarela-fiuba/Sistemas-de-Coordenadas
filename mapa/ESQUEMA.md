# Esquema de `mapa/mapa.yaml`

`mapa.yaml` es la única fuente que lee `tools/build.py` para armar el sitio. Es un archivo **generado**: se edita en `mapa/_fragmentos/bloque-*.yaml` (clases y conceptos) y `mapa/_fragmentos/unidades.yaml` (unidades), y se regenera con `uv run tools/merge_mapa.py` (ver `mapa/README.md`). Tiene tres listas: `clases` (el esqueleto del profesor, cursada 2025), `conceptos` (los nodos del mapa) y `unidades` (los notebooks marimo, que en la portada son las unidades del hilo conductor; ver `docs/camino.md`). El merge y el build validan las referencias cruzadas antes de generar nada.

```yaml
titulo: Sistemas de Coordenadas — mapa de conceptos
pregunta_guia: "transformaciones ↔ operaciones ↔ coordenadas"

clases:                          # 14 entradas, en el orden de la cursada
  - id: "01"                     # string de dos dígitos; único; define el orden de las columnas del mapa
    titulo: Rotaciones
    ficha: clases/01-rotaciones.md   # ruta relativa a la raíz del repo; si no existe, el build avisa (warning) y sigue
    fecha_2025: "2025-08-21"     # fecha en que se dictó en 2025 (string ISO) SÓLO si el campus la da; si no, null
    fecha_2025_estimada: "2025-08-28"   # OPCIONAL: estimación (ritmo semanal, fecha de archivos) cuando fecha_2025 es null; el índice la muestra con "(est.)"
    fechas_2026: ["2026-08-19"]  # lista; puede ser vacía si todavía no se dictó
    estado: con-transcripcion    # PROCEDENCIA del contenido: con-transcripcion | reconstruida | no-dictada | anticipada (armada antes de dictarse; etiqueta "anticipación, pendiente de validar")
    validacion: pendiente        # cuánto se revisó: pendiente | revisado | validado-catedra (independiente de `estado`)
    nivel: troncal               # ruta de estudio: troncal | complementario | avanzado (filtro de ruta en mapa.html)
    pregunta: "¿Qué se conserva cuando giro, y cómo escribo ese giro como una cuenta?"   # una línea, pregunta de campo que la clase responde
    apunte: ["07"]               # OPCIONAL: prefijos de apunte/contenido/NN-*.tex; si falta, se infiere de los conceptos de la clase

conceptos:
  - id: rotacion                 # slug único, minúsculas, guion medio
    nombre: Rotación             # texto del nodo
    clase: "01"                  # id de una clase existente (columna donde se dibuja)
    unidad: 01_rotaciones        # OPCIONAL: id de una unidad existente; el nodo linkea ahí (si no, a la ficha de la clase)
    hecho_geometrico: "dejar quieto un punto, mover otro, acomodar el resto conservando distancias y ángulos"
    que_se_conserva: "distancias y ángulos"
    apunte: ["07", "14", "15"]   # prefijos de apunte/contenido/NN-*.tex (00-11 por tema, 14-22 apéndices; 12 y 13 no existen); cada uno tiene que existir
    requiere: [producto-interno] # ids de conceptos que lo motivan; se dibujan como flechas requerido → concepto

unidades:                        # fuente: mapa/_fragmentos/unidades.yaml; su orden es el de las unidades en la portada
  - id: 01_rotaciones            # único; es el nombre de la carpeta site/unidades/<id>/
    archivo: unidades/01_rotaciones.py   # ruta relativa a la raíz; tiene que existir si el estado se exporta
    titulo: Rotaciones
    estado: piloto               # piloto | migrada | legacy | pendiente
    nota: "piloto a rehacer"     # OPCIONAL: texto libre que se muestra en la portada
    clases: ["01", "02"]         # ids de clase que cubre (según CONCEPTOS.md y el `unidad` de los conceptos); cada uno tiene que existir
    pregunta: "¿Qué le pasa a cada punto de la parcela cuando giro los ejes…?"   # una línea; la pregunta de campo de la unidad
    gancho_agrimensura: "La estación total mide en sus propios ejes; …"           # una línea; situación de campo (sin fajas ni EPSG)
    nivel: troncal               # troncal | complementario | avanzado
```

Estado de una **unidad** en la portada (lo calcula `build.py`, no se declara): `lista` si existe `site/unidades/<id>/index.html`; `en-clase` si alguna de sus clases tiene una `fechas_2026` ≤ hoy y la unidad no está exportada; `todavia-no` si ninguna se dictó. Las clases que ninguna unidad cubre (hoy 11–14) van a la última unidad, "Lo que viene".

## Reglas que valida `tools/build.py`

Errores (el build se detiene):

- ids duplicados en `clases`, `conceptos` o `unidades`;
- `conceptos[].clase` que no sea un id de `clases`;
- `conceptos[].unidad` declarado que no sea un id de `unidades`;
- `conceptos[].requiere` con ids que no están en `conceptos` (o que se refieren a sí mismos);
- prefijos de `apunte` (en conceptos o clases) sin archivo `apunte/contenido/<NN>-*.tex`;
- `unidades[].archivo` inexistente cuando el estado es `piloto` o `migrada`;
- `unidades[].clases` vacío o con ids que no están en `clases`;
- `estado` fuera del vocabulario (clases: `con-transcripcion`, `reconstruida`, `no-dictada`, `anticipada`; unidades: `piloto`, `migrada`, `legacy`, `pendiente`);
- `validacion` (clases) o `nivel` (clases y unidades) fuera del vocabulario.

(`merge_mapa.py` valida lo mismo sobre los fragmentos y además exige que `pregunta` y `gancho_agrimensura` sean una línea de texto.)

Avisos (el build sigue):

- `clases[].ficha` que todavía no existe (la fase 1 las va escribiendo);
- unidad con estado `legacy` o `pendiente` (no se exporta: `build.py` sólo exporta `piloto` y `migrada`; figura en la portada como unidad "en clase" o "todavía no");
- concepto sin `hecho_geometrico` (el hover del nodo queda vacío);
- clase sin `pregunta`, unidad sin `pregunta` o sin `gancho_agrimensura`.

## Qué hace el build con cada campo

- Portada (`index.html`, el hilo conductor): una entrada por unidad en el orden de `unidades.yaml`, con `titulo`, `pregunta`, `gancho_agrimensura`, `nivel`, estado calculado, sus `clases` (cada una con `estado` como procedencia y `validacion`), link a la unidad si está exportada, a las fichas y a las secciones del apunte (`apunte.pdf#nameddest=cap:NN`, con `NN` el prefijo del `.tex`). Entradas: *Empezar* (unidad 0), *Seguir la cursada* (la unidad de la clase con la `fechas_2026` ≤ hoy más reciente), *Repasar* (`mapa.html`).
- Mapa (`mapa.html`): columnas = `clases` en orden de aparición. Color del nodo: `estado` de su clase (teal = con transcripción, dorado = reconstruida, óxido = no dictada, violeta = anticipada). Cada nodo lleva `data-nivel` (el `nivel` de su clase) y `data-orden` (posición de la clase) para el filtro de ruta (`troncal` / `todo`) y el deslizador "hasta la clase N" (opacity 0.25 para lo posterior; default N = última clase dictada).
- Nodo: `nombre`; `<title>` = `hecho_geometrico`; link a `unidades/<unidad>/` si el concepto declara `unidad` y esa unidad se exportó, si no a `clases/<clase>.html`.
- Aristas: `requiere`; la flecha va del requerido al concepto.
- Lista de clases (en `mapa.html`): `fecha_2025` (o `fecha_2025_estimada` con "(est.)"), `fechas_2026`, etiquetas de `estado`, `validacion` y `nivel`, links a ficha, unidades (las de sus conceptos) y secciones del apunte (título tomado del primer `\section{}` de cada `.tex` referido).
- Fichas: dos etiquetas arriba del título, procedencia (`estado`) y `validacion`.

## Convenciones

- Prefijos del apunte: dos dígitos (`"07"`), siempre como string para no perder el cero.
- Ids de clase también como string (`"01"`): YAML convertiría `01` en el entero 1.
- Sin acentos en ids; con acentos en `nombre`/`titulo` (es lo que se muestra).
