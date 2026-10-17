#!/usr/bin/env bash
# Correr en la MBA:  bash ~/proyectos/sistemas-de-coordenadas/tools/bootstrap_github.sh
# Registra el PAT de la cuenta gusvarela-fiuba en el llavero, crea el repo en GitHub
# (si no existe), configura origin y verifica acceso. El token no se imprime ni se guarda en archivos.
set -euo pipefail
HANDLE="gusvarela-fiuba"
REPO="sistemas-de-coordenadas"
DESC="CB104 Sistemas de Coordenadas (Agrimensura FIUBA): unidades interactivas marimo, mapa de conceptos, apunte LaTeX y entregas"
R="$HOME/proyectos/$REPO"

cd "$R"
echo "Pegá el PAT clásico de $HANDLE (scopes repo + workflow). No se muestra al tipear."
read -r -s -p "Token: " TOKEN; echo
[ -n "$TOKEN" ] || { echo "token vacío"; exit 1; }

api() { curl -sS -H "Authorization: token $TOKEN" -H "Accept: application/vnd.github+json" "$@"; }

echo "== identidad del token"
LOGIN=$(api https://api.github.com/user | python3 -c 'import sys,json; print(json.load(sys.stdin).get("login",""))')
[ "$LOGIN" = "$HANDLE" ] || { echo "el token pertenece a '$LOGIN', no a '$HANDLE'. Abortado."; exit 1; }
echo "ok: $LOGIN"

echo "== repo en GitHub"
CODE=$(api -o /dev/null -w '%{http_code}' "https://api.github.com/repos/$HANDLE/$REPO")
if [ "$CODE" = "404" ]; then
  api -X POST https://api.github.com/user/repos \
    -d "{\"name\":\"$REPO\",\"description\":\"$DESC\",\"private\":true,\"has_issues\":true,\"has_wiki\":false,\"auto_init\":false}" \
    | python3 -c 'import sys,json; d=json.load(sys.stdin); print("creado:", d.get("html_url") or d)'
else
  echo "ya existe (HTTP $CODE): https://github.com/$HANDLE/$REPO"
fi

echo "== credencial en el llavero (git credential-osxkeychain)"
git config --global credential.helper osxkeychain >/dev/null 2>&1 || true
printf 'protocol=https\nhost=github.com\nusername=%s\npassword=%s\n' "$HANDLE" "$TOKEN" | git credential-osxkeychain store
unset TOKEN

echo "== remote origin"
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "https://github.com/$HANDLE/$REPO.git"
else
  git remote add origin "https://github.com/$HANDLE/$REPO.git"
fi
git config user.name "Gustavo Varela"
git config user.email "guvarela@fi.uba.ar"

echo "== verificación"
git ls-remote --heads origin >/dev/null && echo "acceso a origin OK"
git remote -v
