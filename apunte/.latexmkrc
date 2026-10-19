# latexmk desde apunte/: antes de compilar, regenera generado/fragmentos/ a partir de
# demostraciones/*.py (ver demostraciones/README.md). Si el extractor falla, no se compila.
system("cd .. && uv run python apunte/scripts/extraer_fragmentos.py") == 0
  or die "extraer_fragmentos falló\n";
