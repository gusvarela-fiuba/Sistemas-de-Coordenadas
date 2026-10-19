#!/usr/bin/env bash
# Control de que el PDF del apunte no pierda páginas sin decirlo.
#
# Uso: scripts/paginas_no_bajan.sh PDF ANTERIOR MENSAJE
#   PDF       el PDF nuevo (staged en el hook, commiteado en CI)
#   ANTERIOR  archivo con las páginas esperadas del commit anterior (HEAD en el hook, el padre en
#             CI); si no existe o está vacío (primera vez que se versiona), el control no aplica
#   MENSAJE   archivo con el mensaje del commit
#
# Falla (exit 1) si el PDF tiene MENOS páginas que ANTERIOR y el mensaje no incluye
# «PAGINAS-BAJAN: motivo» (con algún texto después de los dos puntos). Lo usan
# .githooks/commit-msg y .github/workflows/pages.yml. Requiere pdfinfo.
set -u

falla() { echo "paginas_no_bajan: ERROR: $*" >&2; exit 1; }
[ $# -eq 3 ] || falla "uso: scripts/paginas_no_bajan.sh PDF ANTERIOR MENSAJE"
PDF="$1"; ANTERIOR="$2"; MENSAJE="$3"

if [ ! -s "$ANTERIOR" ]; then
  echo "paginas_no_bajan: sin páginas esperadas en el commit anterior; el control no aplica"
  exit 0
fi
ANT="$(tr -d ' \t\r\n' < "$ANTERIOR")"
case "$ANT" in ''|*[!0-9]*) falla "el archivo de páginas del commit anterior no tiene un entero: «$ANT»" ;; esac
PAGS="$(pdfinfo "$PDF" 2>/dev/null | awk '/^Pages:/ { print $2 }')"
case "$PAGS" in ''|*[!0-9]*) falla "pdfinfo no puede leer el número de páginas de $PDF" ;; esac

if [ "$PAGS" -ge "$ANT" ]; then
  echo "paginas_no_bajan: ok, $PAGS páginas (antes $ANT)"
  exit 0
fi
if grep -qE 'PAGINAS-BAJAN:[[:space:]]*[^[:space:]]' "$MENSAJE" 2>/dev/null; then
  echo "paginas_no_bajan: el PDF baja de $ANT a $PAGS páginas, aceptado por «PAGINAS-BAJAN» en el mensaje"
  exit 0
fi
falla "el PDF baja de $ANT a $PAGS páginas respecto del commit anterior; si es a propósito, agregar al mensaje del commit una línea «PAGINAS-BAJAN: motivo»"
