# Apunte integral — Sistemas de Coordenadas (CB104)

Versión vigente: v3 (2026-10-17, portada interior "Versión 3"): 14 clases, 19 unidades, SVD, cuatro problemas, curvatura, elipsoide, trigonometría esférica (secciones anticipadas) y fe de erratas del apunte del elipsoide; 105 págs. La anterior (2026-09-22) tenía 84 págs. Desde el 2026-09-22 el fuente está partido en
formato + contenido (antes era un único `.tex` de ~5000 líneas; ese monolito se conserva en
`_old/Apunte_Sistemas_de_Coordenadas.monolitico-2026-09-22.tex`).

## Estructura

- `Apunte_Sistemas_de_Coordenadas.tex` — archivo principal (corto): `\documentclass`,
  `\usepackage{apunte-formato}`, metadatos (título PDF, autor, textos de encabezado), portada,
  índice, la lista ordenada de `\input{contenido/NN-nombre}` (con los `\part`, `\clearpage`
  y `\appendix` entre medio) y los dos `\includepdf` del final.
- `apunte-formato.sty` — todo el formato: paquetes, fuentes (fontspec), geometría, paleta
  teal/rust/gold, cajas `idea` / `resultado` / `atencion` / `enunciado`, columna `Y` de
  tablas, `\file`, hyperref (colores de links), encabezado/pie (fancyhdr), macros de notación
  (`\R`, `\vect`, `\rhoP`, `\refl`, `\homot`, `\figlabel`) y estilos TikZ. No contiene texto.
- `contenido/NN-nombre.tex` — el cuerpo, en orden, un archivo por bloque lógico. Cada archivo
  arranca con un comentario de una línea con su título. Las figuras TikZ están dentro del
  contenido, donde se usan.
- `Apunte_Sistemas_de_Coordenadas.pdf` — PDF generado.
- `01_Ejercicios_original.pdf`, `02_afinidad_original.pdf` — material del profesor que el
  apunte incluye con `\includepdf`; deben estar en esta misma carpeta.
- `_old/` — backups: `.bak-2026-09-19`, `.bak-2026-09-21`, el monolito previo a la partición
  (`…monolitico-2026-09-22.tex`), la versión original (generada por IA, 2026-09-09)
  (`apunte_sistemas_coordenadas.tex`, 16/9) y la del 9/9.
- `scripts/` — `Apunte_insert_proyectivas_v2.py`, `Apunte_insert_hilo_v3.py`: inserciones
  reproducibles que produjeron v2 y v3 sobre el archivo monolítico. Quedan como referencia
  histórica: **ya no aplican al fuente partido** (operan sobre un solo `.tex`). Para regenerar
  v3 monolítica desde cero: `cp _old/Apunte_Sistemas_de_Coordenadas.bak-2026-09-21.tex X.tex`
  y `python3 scripts/Apunte_insert_hilo_v3.py X.tex`.

## Compilar

Desde esta carpeta, en la Mac que tenga TeX Live (necesita las fuentes Linux Libertine O y
DejaVu):

    lualatex Apunte_Sistemas_de_Coordenadas.tex   # 3 pasadas (índice + LastPage + refs)

Sólo `lualatex`: `xelatex` falla por fuentes. Auxiliares (`.aux .log .out .toc`) se pueden
borrar; el `.pdf` se deja regenerado.

## Agregar una sección nueva

1. Crear `contenido/NN-nombre.tex` (número siguiente en la posición que corresponda, kebab-case
   sin acentos), con un comentario de título en la primera línea y el `\section{...}` a
   continuación.
2. Agregar una línea `\input{contenido/NN-nombre}` en `Apunte_Sistemas_de_Coordenadas.tex`, en
   el lugar del orden donde va (dentro de la "lectura" o del apéndice correspondiente).
3. Si hace falta una caja, color o macro nueva, definirla en `apunte-formato.sty` (en el bloque
   comentado que corresponda), nunca en el contenido ni en el principal.
4. Compilar 3 veces con `lualatex`.

Si se renumera, mantener la numeración consecutiva y el orden de los `\input` sincronizados:
la cantidad de `\input{` en el principal debe coincidir con la cantidad de archivos en
`contenido/`.

## Carátula (2026-09-22, v3: sólo figuras)

`portada/portada-tikz.tex` es la carátula: un solo `tikzpicture`, sin fórmulas ni leyendas (la v2 con matrices y ecuaciones "parecía un machete"). Subtítulo: "La geometría es álgebra". Un hilo en espiral (decoración `coil`, requiere `decorations.pathmorphing`, ya cargada en el `.sty` y en el standalone) recorre las cinco figuras:

- Arriba-izquierda: monolito 1:4:9 girado alrededor de x, y, z, rotulado Rx(α), Ry(β), Rz(γ).
- Arriba-derecha: el mismo punto en cartesianas (x, y, z) y en esféricas (R, acimut A desde el norte, latitud φ), en proyección ortográfica (az −40°, el 35°).
- Centro-izquierda: cubo unitario → paralelepípedo de A = [v1 v2 v3] (v1 = (1,5; 0; 0,5), v2 = (0,5; 2; 0,5), v3 = (0; 0; 1,5)), V = det A en verde agua dentro del cuerpo, recta dorada del autovector v = (0,5; 0,5; 1) con Av = λv (λ = 2).
- Centro-derecha: círculo unidad con e^{iθ}, cos θ, sen θ y la fórmula de Euler debajo.
- Abajo-derecha: elipsoide de revolución (a = 1, c = 0,9, eje polar con flecha) con plano tangente opaco, base r_u, r_v y normal, en ortográfica (az −60°, el 20°) para que no parezca un huevo.

El principal la incluye con `\input{portada/portada-tikz}` dentro del `titlepage`, definiendo antes `\newcommand{\portadaAutor}{...}`. La página siguiente conserva la caja "Propósito" y las notas de versión.

El .tex está **generado** por `portada/gen-portada-tikz.py` (proyecciones, ángulos, vectores, visibilidad, sombreado, ruta del hilo): para retocar, editar el generador y correr `python3 gen-portada-tikz.py`, no el .tex. `portada/portada-standalone.tex` compila la carátula sola (`lualatex` desde `portada/`; `portada.pdf` y `portada.png` son la vista previa).
