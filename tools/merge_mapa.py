#!/usr/bin/env python3
"""Mezcla los fragmentos `mapa/_fragmentos/bloque-*.yaml` en `mapa/mapa.yaml`.

Los fragmentos son la fuente editable (uno por bloque de clases); `mapa.yaml` es
generado y lo lee `tools/build.py`. Esquema: mapa/ESQUEMA.md; ids: mapa/CONCEPTOS.md.

Qué hace:
  - concatena `clases` de todos los fragmentos y las ordena por id (01, 02, 03, 03p, 04 … 14);
  - concatena `conceptos`; si un id aparece en dos fragmentos conserva el del bloque cuya
    clase lo lista en CONCEPTOS.md (y lo informa); si CONCEPTOS.md no lo lista, el primero;
  - informa ids que están en los fragmentos y no en CONCEPTOS.md, y viceversa;
  - arma `unidades` con la lista fija de abajo (migradas, piloto y pendientes);
  - escribe `mapa/mapa.yaml` con cabecera `titulo` / `pregunta_guia`.

Uso:  uv run tools/merge_mapa.py [--check]      (--check: no escribe, sólo valida e informa)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
DIR_FRAGMENTOS = RAIZ / "mapa" / "_fragmentos"
CONCEPTOS_MD = RAIZ / "mapa" / "CONCEPTOS.md"
SALIDA = RAIZ / "mapa" / "mapa.yaml"

TITULO = "Sistemas de Coordenadas — mapa de conceptos"
PREGUNTA_GUIA = "transformaciones ↔ operaciones ↔ coordenadas"

# Unidades marimo: id, archivo, título, estado, nota opcional. `pendiente` no se exporta
# (build.py sólo exige que el archivo exista en `piloto`/`migrada`).
UNIDADES: list[dict] = [
    {"id": "01_rotaciones", "archivo": "unidades/01_rotaciones.py", "titulo": "Rotaciones",
     "estado": "pendiente", "nota": "piloto a rehacer; v1 en _legacy"},
    {"id": "03_reflexiones_similaridades", "archivo": "unidades/03_reflexiones_similaridades.py",
     "titulo": "Reflexiones y similaridades", "estado": "pendiente"},
    {"id": "04_afines_homogeneas", "archivo": "unidades/04_afines_homogeneas.py",
     "titulo": "Afinidades y coordenadas homogéneas", "estado": "pendiente"},
    {"id": "05_proyectivas", "archivo": "unidades/05_proyectivas.py", "titulo": "Proyectivas",
     "estado": "migrada"},
    {"id": "06_formas_lineales", "archivo": "unidades/06_formas_lineales.py",
     "titulo": "Formas lineales y dualidad", "estado": "pendiente"},
    {"id": "07_cuna_autovectores", "archivo": "unidades/07_cuna_autovectores.py",
     "titulo": "Producto cuña, determinante, núcleo y autovectores", "estado": "migrada"},
    {"id": "08_cambio_de_base", "archivo": "unidades/08_cambio_de_base.py",
     "titulo": "Cambio de base y diagonalización", "estado": "pendiente"},
    {"id": "09_cambio_de_base_svd", "archivo": "unidades/09_cambio_de_base_svd.py",
     "titulo": "Cambio de base, SVD e inversas", "estado": "pendiente"},
    {"id": "10_jacobiano_primera_forma", "archivo": "unidades/10_jacobiano_primera_forma.py",
     "titulo": "Jacobiano y primera forma fundamental", "estado": "pendiente"},
]


def clave_clase(iid: str) -> tuple[int, str]:
    """'03' -> (3, ''), '03p' -> (3, 'p'): ordena 01, 02, 03, 03p, 04, …"""
    m = re.match(r"(\d+)(.*)$", iid)
    if not m:
        return (10**6, iid)
    return (int(m.group(1)), m.group(2))


def leer_conceptos_md() -> dict[str, str]:
    """{'rotacion': '01', ...} a partir de la tabla de CONCEPTOS.md (fila: `| 01 Rotaciones | id, id |`)."""
    res: dict[str, str] = {}
    if not CONCEPTOS_MD.exists():
        return res
    for linea in CONCEPTOS_MD.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\|\s*(\d+p?)\s+[^|]*\|\s*([^|]*)\|", linea)
        if not m:
            continue
        clase = m.group(1)
        for iid in re.split(r"[,\s]+", m.group(2).strip()):
            if iid:
                res[iid] = clase
    return res


def cargar_fragmentos() -> list[tuple[Path, dict]]:
    rutas = sorted(DIR_FRAGMENTOS.glob("bloque-*.yaml"))
    if not rutas:
        sys.exit(f"ERROR: no hay fragmentos en {DIR_FRAGMENTOS.relative_to(RAIZ)}")
    res = []
    for r in rutas:
        with r.open(encoding="utf-8") as f:
            d = yaml.safe_load(f) or {}
        d.setdefault("clases", [])
        d.setdefault("conceptos", [])
        for c in d["clases"]:
            c["id"] = str(c["id"])
        for k in d["conceptos"]:
            k["clase"] = str(k["clase"])
        res.append((r, d))
    return res


def mezclar(fragmentos: list[tuple[Path, dict]], informes: list[str]) -> dict:
    canon = leer_conceptos_md()

    # clases
    clases: dict[str, tuple[Path, dict]] = {}
    for ruta, d in fragmentos:
        for c in d["clases"]:
            if c["id"] in clases:
                informes.append(f"clase {c['id']} duplicada: {clases[c['id']][0].name} y {ruta.name}; se conserva la primera")
                continue
            clases[c["id"]] = (ruta, c)
    lista_clases = [c for _, c in sorted(clases.values(), key=lambda t: clave_clase(t[1]["id"]))]

    # conceptos
    conceptos: dict[str, tuple[Path, dict]] = {}
    for ruta, d in fragmentos:
        for k in d["conceptos"]:
            iid = k["id"]
            if iid not in conceptos:
                conceptos[iid] = (ruta, k)
                continue
            ruta_prev, prev = conceptos[iid]
            clase_canon = canon.get(iid)
            if clase_canon is not None and k["clase"] == clase_canon and prev["clase"] != clase_canon:
                conceptos[iid] = (ruta, k)
                elegido, descartado = ruta.name, ruta_prev.name
            else:
                elegido, descartado = ruta_prev.name, ruta.name
            informes.append(
                f"concepto '{iid}' duplicado (clase {prev['clase']} en {ruta_prev.name}, clase {k['clase']} en {ruta.name}; "
                f"CONCEPTOS.md lo lista en {clase_canon or '—'}): se conserva {elegido}, se descarta {descartado}"
            )
    lista_conceptos = [k for _, k in conceptos.values()]

    # consistencia con CONCEPTOS.md
    for iid, (ruta, k) in conceptos.items():
        if iid not in canon:
            informes.append(f"concepto '{iid}' ({ruta.name}) no figura en CONCEPTOS.md")
        elif canon[iid] != k["clase"]:
            informes.append(f"concepto '{iid}' está en clase {k['clase']} ({ruta.name}) pero CONCEPTOS.md lo lista en {canon[iid]}")
    for iid, clase in canon.items():
        if iid not in conceptos:
            informes.append(f"CONCEPTOS.md lista '{iid}' (clase {clase}) y ningún fragmento lo define")

    # unidades: validar que las referidas por los conceptos existan en la lista fija
    ids_unidades = {u["id"] for u in UNIDADES}
    for k in lista_conceptos:
        u = k.get("unidad")
        if u is not None and str(u) not in ids_unidades:
            informes.append(f"concepto '{k['id']}' refiere a la unidad '{u}' que no está en UNIDADES de merge_mapa.py")

    return {
        "titulo": TITULO,
        "pregunta_guia": PREGUNTA_GUIA,
        "clases": lista_clases,
        "conceptos": lista_conceptos,
        "unidades": [dict(u) for u in UNIDADES],
    }


class _Dumper(yaml.SafeDumper):
    pass


def _str_repr(dumper: yaml.SafeDumper, valor: str):
    # ids de clase y prefijos de apunte tienen que quedar entre comillas ("01") para no perder el cero
    if re.fullmatch(r"\d+p?|\d{4}-\d{2}-\d{2}", valor):
        return dumper.represent_scalar("tag:yaml.org,2002:str", valor, style='"')
    return dumper.represent_scalar("tag:yaml.org,2002:str", valor)


_Dumper.add_representer(str, _str_repr)


def volcar(datos: dict, fragmentos: list[Path]) -> str:
    cab = (
        "# GENERADO por tools/merge_mapa.py — no editar a mano.\n"
        "# Fuente editable: " + ", ".join(f.relative_to(RAIZ).as_posix() for f in fragmentos) + "\n"
        "# Esquema: mapa/ESQUEMA.md. Regenerar con `uv run tools/merge_mapa.py`.\n"
    )
    cuerpo = yaml.dump(datos, Dumper=_Dumper, sort_keys=False, allow_unicode=True, width=10_000, default_flow_style=None)
    # listas cortas en una línea (flow) sólo para apunte/requiere/fechas: default_flow_style=None ya lo hace para listas de escalares
    return cab + cuerpo


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--check", action="store_true", help="no escribe mapa.yaml; sólo informa")
    args = ap.parse_args()

    fragmentos = cargar_fragmentos()
    informes: list[str] = []
    datos = mezclar(fragmentos, informes)
    texto = volcar(datos, [r for r, _ in fragmentos])
    # el resultado tiene que volver a cargar idéntico
    assert yaml.safe_load(texto)["clases"][0]["id"] == datos["clases"][0]["id"]

    print(f"fragmentos: {', '.join(r.name for r, _ in fragmentos)}")
    print(f"clases: {len(datos['clases'])} ({', '.join(c['id'] for c in datos['clases'])})")
    print(f"conceptos: {len(datos['conceptos'])}")
    print(f"unidades: {len(datos['unidades'])} ({sum(u['estado'] in ('piloto', 'migrada') for u in datos['unidades'])} exportables)")
    for i in informes:
        print(f"  informe: {i}")
    if not informes:
        print("  sin duplicados ni inconsistencias con CONCEPTOS.md")
    if args.check:
        return 0
    SALIDA.write_text(texto, encoding="utf-8")
    print(f"escrito {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
