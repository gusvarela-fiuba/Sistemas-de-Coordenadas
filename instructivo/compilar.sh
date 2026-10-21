#!/usr/bin/env bash
# Compila instructivo/Instructivo_para_estudiantes.tex con LuaLaTeX (vía latexmk) en un
# directorio temporal y deja el PDF al lado del .tex. Toma el formato de apunte/apunte-formato.sty
# a través de TEXINPUTS; no corre dentro de apunte/ ni toca el PDF del apunte.
#
# Uso (desde cualquier lado):  instructivo/compilar.sh [NOMBRE_SIN_EXTENSION ...]
#   Sin argumentos compila todos los .tex de instructivo/.
set -eu
AQUI="$(cd "$(dirname "$0")" && pwd)"
RAIZ="$(cd "$AQUI/.." && pwd)"
DIR="$(mktemp -d)"
trap 'rm -rf "$DIR"' EXIT
cd "$AQUI"
if [ $# -gt 0 ]; then NOMBRES="$*"; else NOMBRES="$(ls *.tex | sed 's/\.tex$//')"; fi
for NOMBRE in $NOMBRES; do
  TEXINPUTS="$RAIZ/apunte:" latexmk -lualatex -interaction=nonstopmode -halt-on-error \
    -outdir="$DIR" -auxdir="$DIR" "$NOMBRE.tex" >"$DIR/latexmk.out" 2>&1 \
    || { tail -40 "$DIR/latexmk.out"; grep -n -E "^!|^l\.[0-9]+" "$DIR/$NOMBRE.log" | head -20; exit 1; }
  if grep -q -E "undefined references|multiply defined|File .* not found" "$DIR/$NOMBRE.log"; then
    grep -n -E "undefined references|multiply defined|File .* not found" "$DIR/$NOMBRE.log"
    exit 1
  fi
  cp "$DIR/$NOMBRE.pdf" "$AQUI/$NOMBRE.pdf"
  echo "instructivo: $AQUI/$NOMBRE.pdf ($(pdfinfo "$AQUI/$NOMBRE.pdf" | awk '/^Pages:/{print $2}') páginas)"
done
