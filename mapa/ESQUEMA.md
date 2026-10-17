# Esquema de `mapa/mapa.yaml`

`mapa.yaml` es la única fuente que lee `tools/build.py` para armar el sitio. Es un archivo **generado**: se edita en `mapa/_fragmentos/bloque-*.yaml` y se regenera con `uv run tools/merge_mapa.py` (ver `mapa/README.md`). Tiene tres listas: `clases` (el esqueleto del profesor, cursada 2025), `conceptos` (los nodos del mapa) y `unidades` (los notebooks marimo). El build valida las referencias cruzadas antes de generar nada.

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
    estado: con-transcripcion    # con-transcripcion | reconstruida | no-dictada
    apunte: ["07"]               # OPCIONAL: prefijos de apunte/contenido/NN-*.tex; si falta, se infiere de los conceptos de la clase

conceptos:
  - id: rotacion                 # slug único, minúsculas, guion medio
    nombre: Rotación             # texto del nodo
    clase: "01"                  # id de una clase existente (columna donde se dibuja)
    unidad: 01_rotaciones        # OPCIONAL: id de una unidad existente; el nodo linkea ahí (si no, a la ficha de la clase)
    hecho_geometrico: "dejar quieto un punto, mover otro, acomodar el resto conservando distancias y ángulos"
    que_se_conserva: "distancias y ángulos"
    apunte: ["07", "14", "15"]   # prefijos de apunte/contenido/NN-*.tex; cada uno tiene que existir
    requiere: [producto-interno] # ids de conceptos que lo motivan; se dibujan como flechas requerido → concepto

unidades:
  - id: 01_rotaciones            # único; es el nombre de la carpeta site/unidades/<id>/
    archivo: unidades/01_rotaciones.py   # ruta relativa a la raíz; tiene que existir si el estado se exporta
    titulo: Rotaciones
    estado: piloto               # piloto | migrada | legacy | pendiente
    nota: "piloto a rehacer"     # OPCIONAL: texto libre que se muestra en el índice
```

## Reglas que valida `tools/build.py`

Errores (el build se detiene):

- ids duplicados en `clases`, `conceptos` o `unidades`;
- `conceptos[].clase` que no sea un id de `clases`;
- `conceptos[].unidad` declarado que no sea un id de `unidades`;
- `conceptos[].requiere` con ids que no están en `conceptos` (o que se refieren a sí mismos);
- prefijos de `apunte` (en conceptos o clases) sin archivo `apunte/contenido/<NN>-*.tex`;
- `unidades[].archivo` inexistente cuando el estado es `piloto` o `migrada`;
- `estado` fuera del vocabulario (clases: `con-transcripcion`, `reconstruida`, `no-dictada`; unidades: `piloto`, `migrada`, `legacy`, `pendiente`).

Avisos (el build sigue):

- `clases[].ficha` que todavía no existe (la fase 1 las va escribiendo);
- unidad con estado `legacy` o `pendiente` (no se exporta, pero figura en el índice como "pendiente");
- concepto sin `hecho_geometrico` (el hover del nodo queda vacío).

## Qué hace el build con cada campo

- Columnas del mapa: `clases` en orden de aparición. Color del nodo: `estado` de su clase (teal = con transcripción, dorado = reconstruida, óxido = no dictada).
- Nodo: `nombre`; `<title>` = `hecho_geometrico`; link a `unidades/<unidad>/` si el concepto declara `unidad` y esa unidad se exportó, si no a `clases/<clase>.html`.
- Aristas: `requiere`; la flecha va del requerido al concepto.
- Lista de clases: `fecha_2025` (o `fecha_2025_estimada` con "(est.)"), `fechas_2026`, `estado`, links a ficha, unidades (las de sus conceptos) y secciones del apunte (título tomado del primer `\section{}` de cada `.tex` referido).

## Convenciones

- Prefijos del apunte: dos dígitos (`"07"`), siempre como string para no perder el cero.
- Ids de clase también como string (`"01"`): YAML convertiría `01` en el entero 1.
- Sin acentos en ids; con acentos en `nombre`/`titulo` (es lo que se muestra).
