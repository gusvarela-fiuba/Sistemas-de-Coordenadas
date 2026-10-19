# Demostraciones con código

Cada proposición, teorema, lema y corolario del apunte tiene (o va a tener) una comprobación
ejecutable en esta carpeta. El PDF muestra su fragmento clave en un recuadro, con el enlace a la
línea de este archivo (macro `\comprobacion` de `apunte/apunte-formato.sty`).

```sh
uv run pytest apunte/demostraciones -q                    # todas las pruebas (CI: paso «Demostraciones»)
uv run python apunte/scripts/extraer_fragmentos.py        # regenera apunte/generado/fragmentos/
uv run python apunte/scripts/verificar_comprobaciones.py  # cobertura: N de M resultados con comprobación
```

## Archivos

Un archivo por capítulo: `cap01_rotaciones.py`, `cap02_traslaciones.py`, `cap03_similaridades.py`,
`cap04_afines.py`, `cap05_formas_lineales.py`, `cap06_cuna_determinante.py`, `cap07_autovectores.py`,
`cap08_svd.py`, `cap09_cambio_de_base.py`, `cap10_derivada.py`, `cap11_inversas.py`,
`cap12_cuatro_problemas.py`, `cap13_curvatura.py`, `cap14_elipsoide.py`, `cap15_esfera.py`,
`c1_proyectivas.py`, `c2_conformes.py`, `c3_terreno.py`, `c4_marcos.py`. Pytest los recoge por
nombre (`python_files` en `pyproject.toml`). `conftest.py` da el fixture `rng`
(`np.random.default_rng(104)`, la misma semilla en cada prueba).

## Una función por resultado

- Nombre: `test_` + etiqueta LaTeX con `:` y `-` cambiados por `_`
  (`prop:det-factor` → `test_prop_det_factor`). Una etiqueta, una función.
- Docstring de tres líneas, en este orden:
  1. la etiqueta LaTeX (`prop:det-factor`);
  2. el tipo: `SIMBOLICA`, `NUMERICA` o `CONTRAEJEMPLO`;
  3. qué verifica exactamente, en una frase.
- Marcadores `# >>> fragmento` y `# <<< fragmento` (cada uno en su línea) alrededor de las
  **3 a 8 líneas** que se muestran en el PDF. Que el fragmento se entienda solo: las funciones
  auxiliares van arriba en el archivo, con nombre explícito.

## Tipos

- `SIMBOLICA`: identidad algebraica con sympy, para variables simbólicas. Demuestra esa
  identidad, no las hipótesis del enunciado ni los pasos que no son cuentas.
- `NUMERICA`: semilla fija (fixture `rng`), `CASOS = 200` o más como asignación literal dentro
  de la función (el extractor la lee para el rótulo «N casos») y tolerancia explícita
  (`TOL`, `atol=`). No es una demostración.
- `CONTRAEJEMPLO`: un caso concreto que muestra que la afirmación, sin alguna hipótesis o en su
  forma general, no vale.

## Del código al PDF

1. `apunte/scripts/extraer_fragmentos.py` escribe `apunte/generado/fragmentos/<etiqueta>.tex`,
   con `:` → `_` en el nombre (`prop:det-factor` → `prop_det-factor.tex`): tipo, casos, módulo,
   línea inicial y el fragmento en `lstlisting`. Falla (exit 1) si falta el docstring o el tipo,
   si la etiqueta no corresponde al nombre de la función, si una NUMERICA no fija `CASOS ≥ 200`,
   si el fragmento tiene menos de 3 o más de 8 líneas o si una etiqueta se repite. Es idempotente
   y borra los fragmentos de etiquetas que ya no existen.
2. `apunte/.latexmkrc` lo corre al arrancar `latexmk` desde `apunte/`; si falla, no se compila.
   `apunte/generado/` se versiona: CI comprueba que coincide con las pruebas.
3. En el `.tex`, después de la demostración (o del enunciado, si no tiene):
   `\comprobacion{prop:det-factor}{NUMERICA}`. Si el fragmento no existe, el PDF muestra
   «[comprobación pendiente: …]» en gris; si el tipo pedido difiere del de la prueba, manda el de
   la prueba y queda un aviso en el log.

## Cobertura

`apunte/scripts/verificar_comprobaciones.py` lista cada resultado de los archivos que incluye el
maestro, con su etiqueta, si tiene `\comprobacion{<etiqueta>}` en las 40 líneas siguientes a su
demostración (o a su enunciado) y si existe `test_<etiqueta>`. Termina con «N de M resultados
con comprobación». Con `--estricto` sale con 1 si falta alguna; CI lo va a usar cuando la
cobertura esté completa. `apunte/scripts/estado.py` resume lo mismo por archivo (columnas
«Resultados», «Con comprobación», «Tipo»).
