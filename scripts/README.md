# scripts/ — compilación y verificación del PDF del apunte

- `compilar_pdf.sh`: compila `apunte/Apunte_Sistemas_de_Coordenadas.tex` con `latexmk -lualatex` en un directorio temporal propio (`mktemp -d`, con `-outdir`/`-auxdir`, corriendo desde `apunte/` para que `.latexmkrc` regenere los fragmentos y las rutas relativas funcionen). Solo si latexmk termina con 0, el `.log` no tiene «File … not found», «undefined references», «Citation … undefined» ni «multiply defined», y `verificar_pdf.sh` aprueba el PDF temporal, toma el lock y reemplaza con `mv` atómico el PDF de `apunte/` y `apunte/paginas_esperadas.txt`, y copia `.aux`, `.log`, `.toc`, `.out`, `.fls` y `.fdb_latexmk` al lado del maestro (así `apunte/scripts/numeracion.py` lee el `.aux` como siempre). Ningún camino escribe ni borra el PDF de `apunte/` salvo ese `mv` final. Si algo falla no toca nada y deja el directorio temporal para mirar el log. Opciones: `--destino RUTA` (copia el PDF ahí; no toca `apunte/`), `--sin-copiar` (solo compila y verifica; imprime la ruta del PDF temporal), `--min N` (mínimo de páginas del PDF recién compilado; por defecto, la mitad de `paginas_esperadas.txt`). Al final imprime la línea de `verificar_pdf.sh` y la cantidad de Overfull del log, y avisa si el hook no está activo.
- `verificar_pdf.sh RUTA.pdf [--esperadas ARCHIVO | --min N]`: exit 1 con mensaje si `pdfinfo` da error, si la cola del archivo no tiene `%%EOF`, si la última página no tiene el pie «k de M» con M ≤ total, o si el número de páginas no es exactamente el de `apunte/paginas_esperadas.txt` (o el de `--esperadas`; con `--min N`, si es menor que N). Si pasa: «PDF ok: N páginas, M numeradas, tamaño».
- `paginas_no_bajan.sh PDF ANTERIOR MENSAJE`: exit 1 si el PDF tiene menos páginas que las del archivo ANTERIOR (las esperadas del commit previo) y el mensaje del commit no incluye «PAGINAS-BAJAN: motivo». Si ANTERIOR no existe o está vacío, no aplica. Lo usan el hook `commit-msg` y CI.

Compilar (desde la raíz del repo):

```
scripts/compilar_pdf.sh
git add apunte/Apunte_Sistemas_de_Coordenadas.pdf apunte/paginas_esperadas.txt
```

`apunte/paginas_esperadas.txt` es el único lugar del repo con el número de páginas del PDF; lo escribe `compilar_pdf.sh` y va en el mismo commit que el PDF.

**Lock.** macOS no trae el `flock` de util-linux, así que el lock es el directorio `/tmp/apunte.lock.d` (o `$APUNTE_LOCK`): `mkdir` es atómico en macOS y en Linux. Se reintenta cada 2 s hasta 10 min; adentro queda `pid` con el PID y el host del dueño. Un lock con más de 30 min, o cuyo PID ya no existe en este host, se retira con un aviso. Un `trap` lo libera al salir, también ante Ctrl-C o `kill`. Solo se toma para reemplazar los archivos de `apunte/`.

**Hooks.** `.githooks/pre-commit` verifica el PDF staged (`git show :apunte/...pdf`) contra el `apunte/paginas_esperadas.txt` staged (integridad e igualdad de páginas), y bloquea el commit si no pasa, si ese archivo falta en el índice o si tiene cambios sin stagear. `.githooks/commit-msg` (pre-commit no ve el mensaje) bloquea si el PDF staged tiene menos páginas que las de `paginas_esperadas.txt` en HEAD, salvo «PAGINAS-BAJAN: motivo» en el mensaje. Si el PDF no está en el commit, ninguno de los dos hace nada. Se activan una vez por clon o worktree:

```
git config core.hooksPath .githooks
```

**CI.** `.github/workflows/pages.yml` (checkout con `fetch-depth: 2`) corre `scripts/verificar_pdf.sh apunte/Apunte_Sistemas_de_Coordenadas.pdf` sobre lo commiteado y `paginas_no_bajan.sh` contra `paginas_esperadas.txt` del commit padre con el mensaje de `git log -1 --format=%B`, antes de armar el sitio.
