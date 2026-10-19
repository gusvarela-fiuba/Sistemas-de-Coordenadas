#!/usr/bin/env bash
# Verifica que un PDF del apunte esté entero (no truncado, no a medio escribir, no viejo).
#
# Uso: scripts/verificar_pdf.sh RUTA.pdf [--esperadas ARCHIVO | --min N]
#
# Falla (exit 1) si:
#   (a) pdfinfo da error;
#   (b) el número de páginas no coincide EXACTAMENTE con el de apunte/paginas_esperadas.txt (por
#       defecto; relativo a la raíz del repo) o con el de --esperadas ARCHIVO; con --min N, si tiene
#       menos de N páginas. Sin archivo de páginas esperadas, falla: se genera con
#       scripts/compilar_pdf.sh, que lo escribe junto con el PDF;
#   (c) la última página no tiene el pie «k de M» con M <= total de páginas (portada e índice van
#       en romanos, así que M, las numeradas, es menor que el total);
#   (d) los últimos 1024 bytes no contienen %%EOF.
# Si pasa, exit 0 y una línea «PDF ok: N páginas, M numeradas, tamaño».
# Si se corre dentro de un clon sin el hook activo (core.hooksPath), avisa sin bloquear.
# Requiere poppler (pdfinfo, pdftotext). Funciona en macOS y en Linux.
set -u

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
ESPERADAS_DEF="$RAIZ/apunte/paginas_esperadas.txt"

falla() { echo "verificar_pdf: ERROR: $*" >&2; exit 1; }

PDF=""
MIN=""
ESPERADAS=""
while [ $# -gt 0 ]; do
  case "$1" in
    --min) [ $# -ge 2 ] || falla "--min necesita un número"; MIN="$2"; shift 2 ;;
    --min=*) MIN="${1#--min=}"; shift ;;
    --esperadas) [ $# -ge 2 ] || falla "--esperadas necesita un archivo"; ESPERADAS="$2"; shift 2 ;;
    --esperadas=*) ESPERADAS="${1#--esperadas=}"; shift ;;
    -h|--help) sed -n '2,18p' "$0"; exit 0 ;;
    -*) falla "opción desconocida: $1" ;;
    *) [ -z "$PDF" ] || falla "sobra el argumento: $1"; PDF="$1"; shift ;;
  esac
done
[ -n "$PDF" ] || falla "uso: scripts/verificar_pdf.sh RUTA.pdf [--esperadas ARCHIVO | --min N]"
[ -n "$MIN" ] && [ -n "$ESPERADAS" ] && falla "--min y --esperadas no van juntos"
[ -f "$PDF" ] || falla "no existe el archivo: $PDF"
command -v pdfinfo >/dev/null 2>&1 || falla "falta pdfinfo (instalar poppler / poppler-utils)"
command -v pdftotext >/dev/null 2>&1 || falla "falta pdftotext (instalar poppler / poppler-utils)"

# Aviso no bloqueante: el hook pre-commit solo corre si el clon lo tiene activo. En CI no aplica,
# y el propio hook exporta VERIFICAR_PDF_SIN_AVISO.
if [ -z "${CI:-}" ] && [ -z "${VERIFICAR_PDF_SIN_AVISO:-}" ] && command -v git >/dev/null 2>&1 \
   && git -C "$RAIZ" rev-parse --git-dir >/dev/null 2>&1 \
   && [ "$(git -C "$RAIZ" config --get core.hooksPath 2>/dev/null)" != ".githooks" ]; then
  echo "verificar_pdf: AVISO: el hook pre-commit no está activo en este clon; activarlo con:" >&2
  echo "  git -C \"$RAIZ\" config core.hooksPath .githooks" >&2
fi

MODO="exacto"
if [ -n "$MIN" ]; then
  MODO="minimo"
  case "$MIN" in ''|*[!0-9]*) falla "--min tiene que ser un entero: $MIN" ;; esac
else
  [ -n "$ESPERADAS" ] || ESPERADAS="$ESPERADAS_DEF"
  [ -f "$ESPERADAS" ] || falla "no existe $ESPERADAS (páginas esperadas del PDF); generarlo compilando con scripts/compilar_pdf.sh"
  ESPERADO="$(tr -d ' \t\r\n' < "$ESPERADAS")"
  case "$ESPERADO" in ''|*[!0-9]*) falla "$ESPERADAS tiene que tener una sola línea con un entero (tiene: «$ESPERADO»)" ;; esac
fi

# Tamaño en bytes y legible (wc -c es portable entre macOS y Linux).
BYTES="$(wc -c < "$PDF" | tr -d ' ')"
TAM="$(LC_ALL=C awk -v b="$BYTES" 'BEGIN { if (b >= 1048576) printf "%.2f MB", b/1048576; else printf "%.0f kB", b/1024 }')"

# (d) primero: es lo más barato y lo que delata una copia cortada.
if ! tail -c 1024 "$PDF" | LC_ALL=C grep -a -q '%%EOF'; then
  falla "$PDF ($TAM) no termina en %%EOF: está truncado o se copió mientras se escribía"
fi

# (a) pdfinfo sin errores (devuelve 0 aunque encuentre errores recuperables: se miran ambos).
ERRF="$(mktemp "${TMPDIR:-/tmp}/verificar_pdf.XXXXXX")"
if ! INFO="$(pdfinfo "$PDF" 2>"$ERRF")"; then
  ERR="$(head -n 3 "$ERRF")"; rm -f "$ERRF"
  falla "pdfinfo no puede leer $PDF ($TAM): $ERR"
fi
if grep -q 'Error' "$ERRF"; then
  ERR="$(head -n 3 "$ERRF")"; rm -f "$ERRF"
  falla "pdfinfo informa errores en $PDF ($TAM): $ERR"
fi
rm -f "$ERRF"
PAGS="$(printf '%s\n' "$INFO" | awk '/^Pages:/ { print $2 }')"
case "$PAGS" in ''|*[!0-9]*) falla "pdfinfo no informa el número de páginas de $PDF" ;; esac

# (b) páginas: igualdad exacta con el archivo de esperadas, o mínimo con --min.
if [ "$MODO" = minimo ]; then
  if [ "$PAGS" -lt "$MIN" ]; then
    falla "$PDF tiene $PAGS páginas, menos que el mínimo $MIN (--min)"
  fi
elif [ "$PAGS" -ne "$ESPERADO" ]; then
  if [ "$PAGS" -lt "$ESPERADO" ]; then QUE="menos"; else QUE="más"; fi
  falla "$PDF tiene $PAGS páginas, $QUE que las $ESPERADO de $ESPERADAS; si el PDF es nuevo y está bien, regenerarlo con scripts/compilar_pdf.sh (actualiza el archivo) y stagear los dos"
fi

# (c) pie de la última página: «k de M», con M <= total.
ULT="$(pdftotext -f "$PAGS" -l "$PAGS" "$PDF" - 2>/dev/null)" || falla "pdftotext no puede leer la página $PAGS de $PDF"
NUM="$(printf '%s\n' "$ULT" | grep -oE 'de [0-9]+' | tail -n 1 | grep -oE '[0-9]+')"
[ -n "$NUM" ] || falla "la última página ($PAGS) de $PDF no tiene el pie «k de M»"
if [ "$NUM" -gt "$PAGS" ]; then
  falla "el pie de la última página dice «de $NUM», más que las $PAGS páginas del PDF"
fi

echo "PDF ok: $PAGS páginas, $NUM numeradas, $TAM"
