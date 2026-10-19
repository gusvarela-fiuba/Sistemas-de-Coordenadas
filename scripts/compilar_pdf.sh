#!/usr/bin/env bash
# Compila el apunte en un directorio temporal propio y, solo si salió bien, reemplaza el PDF de
# apunte/ de forma atómica. Así nunca queda (ni se commitea) un PDF a medio escribir.
#
# Uso (desde cualquier lado; conviene la raíz del repo):
#   scripts/compilar_pdf.sh                  compila, verifica y reemplaza apunte/Apunte_Sistemas_de_Coordenadas.pdf
#   scripts/compilar_pdf.sh --destino RUTA   compila, verifica y copia el PDF a RUTA (no toca apunte/ ni copia auxiliares)
#   scripts/compilar_pdf.sh --sin-copiar     compila y verifica; imprime la ruta del PDF temporal y no copia nada
#
# Ningún camino de este script escribe ni borra apunte/Apunte_Sistemas_de_Coordenadas.pdf salvo el
# mv final (sin --destino ni --sin-copiar): LaTeX escribe solo en DIR y no se usa latexmk -c/-C.
#
# Pasos: latexmk -lualatex con -outdir/-auxdir en DIR=$(mktemp -d), corriendo desde apunte/ (así
# .latexmkrc regenera los fragmentos y las rutas relativas de \input y figuras se resuelven igual);
# si latexmk termina con 0, el .log no tiene «File … not found», «undefined references»,
# «Citation … undefined» ni «multiply defined», y scripts/verificar_pdf.sh pasa sobre el PDF de DIR, toma el lock,
# copia el PDF a apunte/.Apunte_tmp.XXXX.pdf y lo mueve (mv atómico, mismo sistema de archivos)
# sobre el PDF del maestro; copia también .aux, .log, .toc (y .out, .fls, .fdb_latexmk si existen)
# al lado del maestro, para que apunte/scripts/numeracion.py y los greps del log sigan andando, y
# escribe (también atómico, bajo el mismo lock) apunte/paginas_esperadas.txt con el total de páginas
# del PDF recién verificado: es el único lugar del repo con ese número, y va en el mismo commit que
# el PDF (el hook pre-commit y CI comparan contra él).
#
# Verificación del PDF recién compilado: verificar_pdf.sh con --min igual a la mitad de
# apunte/paginas_esperadas.txt (un cambio legítimo puede sumar o quitar páginas; la mitad solo
# descarta un PDF cortado), o con --min N si se pasa esa opción a este script.
#
# Lock: macOS no trae el flock de util-linux, así que el lock es un directorio: `mkdir` es atómico
# en macOS y en Linux (falla si ya existe). Se toma /tmp/apunte.lock.d (o $APUNTE_LOCK) con un
# reintento cada 2 s hasta 10 min; adentro queda un archivo pid con el PID y el host del dueño. Si
# el lock tiene más de 30 min, o su PID ya no existe en este host, se considera vencido y se borra.
# Se libera al terminar (también si el script se corta, por trap).
set -u

RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
APUNTE="$RAIZ/apunte"
NOMBRE="Apunte_Sistemas_de_Coordenadas"
MAESTRO_PDF="$APUNTE/$NOMBRE.pdf"
VERIFICAR="$RAIZ/scripts/verificar_pdf.sh"
LOCK="${APUNTE_LOCK:-/tmp/apunte.lock.d}"
LOCK_ESPERA=600     # segundos máximos esperando el lock
LOCK_VENCE=1800     # segundos tras los cuales un lock ajeno se da por abandonado

falla() { echo "compilar_pdf: ERROR: $*" >&2; exit 1; }
aviso() { echo "compilar_pdf: $*" >&2; }

ESPERADAS="$APUNTE/paginas_esperadas.txt"
DESTINO=""
SIN_COPIAR=0
MIN=""
ANTES=""
while [ $# -gt 0 ]; do
  case "$1" in
    --destino) [ $# -ge 2 ] || falla "--destino necesita una ruta"; DESTINO="$2"; shift 2 ;;
    --destino=*) DESTINO="${1#--destino=}"; shift ;;
    --sin-copiar) SIN_COPIAR=1; shift ;;
    --min) [ $# -ge 2 ] || falla "--min necesita un número"; MIN="$2"; shift 2 ;;
    -h|--help) sed -n '2,31p' "$0"; exit 0 ;;
    *) falla "opción desconocida: $1" ;;
  esac
done
[ -n "$DESTINO" ] && [ "$SIN_COPIAR" = 1 ] && falla "--destino y --sin-copiar no van juntos"
command -v latexmk >/dev/null 2>&1 || falla "falta latexmk"

# El hook pre-commit (.githooks/pre-commit) bloquea commits de un PDF roto; avisar si este clon
# o worktree no lo tiene activo.
if command -v git >/dev/null 2>&1 && git -C "$RAIZ" rev-parse --git-dir >/dev/null 2>&1; then
  if [ "$(git -C "$RAIZ" config --get core.hooksPath 2>/dev/null)" != ".githooks" ]; then
    aviso "AVISO: core.hooksPath no apunta a .githooks en este clon; activar el hook con:"
    aviso "  git -C \"$RAIZ\" config core.hooksPath .githooks"
  fi
fi

DIR="$(mktemp -d "${TMPDIR:-/tmp}/apunte_compilar.XXXXXX")" || falla "no pude crear el directorio temporal"
TENGO_LOCK=0
TMP_COPIA=""
CONSERVAR_DIR=0     # 1 = no borrar DIR (con --sin-copiar, o si falló, para poder mirar el log)
[ "$SIN_COPIAR" = 1 ] && CONSERVAR_DIR=1

limpiar() {
  [ -n "$TMP_COPIA" ] && rm -f "$TMP_COPIA"
  if [ "$TENGO_LOCK" = 1 ]; then rm -rf "$LOCK"; TENGO_LOCK=0; fi
  # Con --sin-copiar el PDF temporal se deja para quien lo pidió; si falló la compilación, el log.
  [ "$CONSERVAR_DIR" = 1 ] || rm -rf "$DIR"
}
trap limpiar EXIT
trap 'exit 130' INT TERM HUP

# Antigüedad del lock en segundos (stat difiere entre macOS/BSD y Linux/GNU).
edad_lock() {
  local m
  m="$(stat -f %m "$LOCK" 2>/dev/null || stat -c %Y "$LOCK" 2>/dev/null)" || { echo 0; return; }
  echo $(( $(date +%s) - m ))
}

tomar_lock() {
  local inicio pid host
  inicio="$(date +%s)"
  while ! mkdir "$LOCK" 2>/dev/null; do
    pid=""; host=""
    if [ -f "$LOCK/pid" ]; then read -r pid host < "$LOCK/pid" || true; fi
    if [ "$(edad_lock)" -gt "$LOCK_VENCE" ]; then
      aviso "lock vencido (más de $((LOCK_VENCE / 60)) min, PID ${pid:-?}): lo borro"
      rm -rf "$LOCK"; continue
    fi
    if [ -n "$pid" ] && [ "$host" = "$(hostname)" ] && ! kill -0 "$pid" 2>/dev/null; then
      aviso "lock abandonado (el PID $pid ya no existe): lo borro"
      rm -rf "$LOCK"; continue
    fi
    if [ $(( $(date +%s) - inicio )) -ge "$LOCK_ESPERA" ]; then
      falla "no pude tomar el lock $LOCK en $((LOCK_ESPERA / 60)) min (lo tiene el PID ${pid:-?}); no se copió nada"
    fi
    sleep 2
  done
  TENGO_LOCK=1
  echo "$$ $(hostname)" > "$LOCK/pid"
}

# Copia SRC a DST pasando por un temporal en el mismo directorio y mv (atómico).
copiar_atomico() {
  local src="$1" dst="$2" base
  base="$(basename "$dst")"; base="${base%.*}"
  TMP_COPIA="$(mktemp "$(dirname "$dst")/.${base}_tmp.XXXXXX")" || return 1
  # mktemp crea con permisos 600: se dejan en 644 como cualquier archivo del repo.
  cp "$src" "$TMP_COPIA" && chmod 644 "$TMP_COPIA" && mv -f "$TMP_COPIA" "$dst" || return 1
  TMP_COPIA=""
}

# --- Compilación -------------------------------------------------------------------------------
aviso "compilando en $DIR"
LOG_LATEXMK="$DIR/latexmk.salida"
( cd "$APUNTE" && latexmk -lualatex -interaction=nonstopmode -halt-on-error \
    -outdir="$DIR" -auxdir="$DIR" "$NOMBRE.tex" ) > "$LOG_LATEXMK" 2>&1
RC=$?
PDF_TMP="$DIR/$NOMBRE.pdf"
if [ "$RC" -ne 0 ]; then
  CONSERVAR_DIR=1
  grep -A 3 '^!' "$DIR/$NOMBRE.log" 2>/dev/null | head -n 20 >&2
  tail -n 8 "$LOG_LATEXMK" >&2
  falla "latexmk terminó con código $RC (salida completa: $LOG_LATEXMK, log: $DIR/$NOMBRE.log); no se copió nada"
fi
[ -f "$PDF_TMP" ] || falla "latexmk terminó bien pero no está $PDF_TMP; no se copió nada"

# Problemas que no cortan la compilación pero dejan un PDF incompleto: figura o archivo que falta,
# referencias o citas sin resolver, etiquetas repetidas. Cualquiera de ellos frena la copia.
PROBLEMAS="$(grep -nE "File .*not found|undefined references|Citation .*undefined|multiply[- ]defined" "$DIR/$NOMBRE.log" 2>/dev/null | head -n 10)"
if [ -n "$PROBLEMAS" ]; then
  CONSERVAR_DIR=1
  printf '%s\n' "$PROBLEMAS" >&2
  falla "el log de LaTeX ($DIR/$NOMBRE.log) tiene archivos faltantes, referencias sin resolver o etiquetas repetidas; no se copió nada"
fi

if [ -z "$MIN" ]; then
  ANTES="$(tr -d ' \t\r\n' < "$ESPERADAS" 2>/dev/null)"
  case "$ANTES" in ''|*[!0-9]*) MIN=1 ;; *) MIN=$(( ANTES / 2 )) ;; esac
fi
if ! VERIF="$(VERIFICAR_PDF_SIN_AVISO=1 "$VERIFICAR" "$PDF_TMP" --min "$MIN")"; then
  CONSERVAR_DIR=1
  falla "el PDF compilado no pasó verificar_pdf.sh; no se copió nada"
fi

PAGS="$(pdfinfo "$PDF_TMP" 2>/dev/null | awk '/^Pages:/ { print $2 }')"
echo "$PAGS" > "$DIR/paginas_esperadas.txt"
OVERFULL="$(grep -c '^Overfull' "$DIR/$NOMBRE.log" 2>/dev/null || true)"

# --- Copia -------------------------------------------------------------------------------------
if [ "$SIN_COPIAR" = 1 ]; then
  echo "PDF temporal: $PDF_TMP"
elif [ -n "$DESTINO" ]; then
  mkdir -p "$(dirname "$DESTINO")" || falla "no pude crear el directorio de $DESTINO"
  copiar_atomico "$PDF_TMP" "$DESTINO" || falla "no pude copiar el PDF a $DESTINO"
  echo "PDF copiado a $DESTINO"
else
  tomar_lock
  copiar_atomico "$PDF_TMP" "$MAESTRO_PDF" || falla "no pude reemplazar $MAESTRO_PDF"
  copiar_atomico "$DIR/paginas_esperadas.txt" "$ESPERADAS" || falla "no pude escribir $ESPERADAS"
  for ext in aux log toc out fls fdb_latexmk; do
    if [ -f "$DIR/$NOMBRE.$ext" ]; then
      copiar_atomico "$DIR/$NOMBRE.$ext" "$APUNTE/$NOMBRE.$ext" || falla "no pude copiar $NOMBRE.$ext"
    fi
  done
  rm -rf "$LOCK"; TENGO_LOCK=0
  echo "PDF actualizado: $MAESTRO_PDF"
  echo "Páginas esperadas: $PAGS (antes: ${ANTES:-sin archivo}) en apunte/paginas_esperadas.txt; stagearlo junto con el PDF"
fi

echo "$VERIF"
echo "Overfull en el log: ${OVERFULL:-0}"
