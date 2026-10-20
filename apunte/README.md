# Apunte integral — Sistemas de Coordenadas (CB104)

Versión vigente: v4. El apunte está organizado por tema: un capítulo por tema y tres niveles dentro de cada uno (`La idea`, `Construcciones, cuentas y ejemplos`, `En profundidad`). El fuente está partido en formato + contenido.

## Estructura

- `Apunte_Sistemas_de_Coordenadas.tex` — archivo principal (corto): `\documentclass`,
  `\usepackage{apunte-formato}`, metadatos, portada, índice y la lista ordenada de
  `\input{contenido/NN-nombre}` (con `\appendix` antes de los apéndices).
- `apunte-formato.sty` — todo el formato: paquetes, fuentes (fontspec), geometría, paleta
  teal/rust/gold, cajas `idea` / `resultado` / `atencion` / `enunciado`, macros de notación y
  estilos TikZ. No contiene texto.
- `contenido/` — el cuerpo, un archivo por capítulo. Cada archivo arranca con un comentario de
  una línea con su título y un `\chapter{...}\label{cap:<clave>}`. Orden actual: `00-antes-de-empezar`
  (capítulo 0), capítulos `01-rotaciones` a `15-esfera-trigonometria-esferica`, complementos
  `c1-proyectivas`, `c2-conformes`, `c3-terreno-como-matriz`, `c4-marcos-grillas` (rotulados C1 a C4)
  y apéndices `ap1` a `ap6` (labels `ap:*`).
- `Apunte_Sistemas_de_Coordenadas.pdf` — PDF generado.
- `ESTADO.md` — estado del apunte, generado por `scripts/estado.py`.
- `PENDIENTES.md` — tareas abiertas sobre unidades y material.
- `figuras/`, `portada/` — figuras y carátula (la carátula se genera con `portada/gen-portada-tikz.py`).
- `scripts/` — utilidades de mantenimiento del apunte (estado, enlaces y generadores de capítulos).

## Compilar

Desde esta carpeta, en la Mac que tenga TeX Live (necesita las fuentes Linux Libertine O y
DejaVu):

    lualatex Apunte_Sistemas_de_Coordenadas.tex   # 3 pasadas (índice + LastPage + refs)

Sólo `lualatex`: `xelatex` falla por fuentes. Auxiliares (`.aux .log .out .toc`) se pueden
borrar; el `.pdf` se deja regenerado.

## Agregar un capítulo nuevo

1. Crear `contenido/NN-nombre.tex` (número siguiente en la posición que corresponda, kebab-case
   sin acentos), con un comentario de título en la primera línea, el `\chapter{...}` con su
   `\label{cap:<clave>}` y las tres secciones de nivel (`La idea`, `Construcciones, cuentas y
   ejemplos`, `En profundidad`).
2. Agregar una línea `\input{contenido/NN-nombre}` en `Apunte_Sistemas_de_Coordenadas.tex`, en
   el lugar del orden donde va (entre los capítulos temáticos o entre los apéndices).
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
