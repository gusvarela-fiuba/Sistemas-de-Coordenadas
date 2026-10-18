#!/usr/bin/env python3
"""Mezcla los fragmentos `unidades/_banco/bloque_*.py` en `unidades/banco_autoevaluacion.py` (generado).

Valida: cada unidad del hilo (orden de mapa/_fragmentos/unidades.yaml) tiene exactamente 6 preguntas
(2 elementales, 2 medias, 2 avanzadas), cada pregunta 4 opciones con ids a–d y exactamente una correcta,
todas con explicación, e ids de pregunta únicos en todo el banco.

Uso:  uv run python tools/merge_banco.py [--check] [--parcial]
      --check    no escribe, sólo valida
      --parcial  admite que falten unidades (mientras se redacta el banco)
"""
from __future__ import annotations

import argparse
import pprint
import sys
from pathlib import Path

import yaml

RAIZ = Path(__file__).resolve().parent.parent
FRAGMENTOS = RAIZ / "unidades" / "_banco"
SALIDA = RAIZ / "unidades" / "banco_autoevaluacion.py"
NIVELES = ("elemental", "medio", "avanzado")


def orden_unidades() -> list[str]:
    datos = yaml.safe_load((RAIZ / "mapa" / "_fragmentos" / "unidades.yaml").read_text(encoding="utf-8"))
    return [u["id"] for u in datos["unidades"]]


def cargar_fragmentos() -> dict[str, list[dict]]:
    banco: dict[str, list[dict]] = {}
    for f in sorted(FRAGMENTOS.glob("bloque_*.py")):
        ns: dict = {}
        exec(compile(f.read_text(encoding="utf-8"), str(f), "exec"), ns)
        for uid, preguntas in ns["BANCO"].items():
            if uid in banco:
                raise SystemExit(f"{f.name}: la unidad {uid} ya estaba definida en otro fragmento")
            banco[uid] = preguntas
    return banco


def validar(banco: dict[str, list[dict]], unidades: list[str], parcial: bool) -> list[str]:
    errores = []
    ids_vistos: set[str] = set()
    for uid in unidades:
        if uid not in banco:
            if not parcial:
                errores.append(f"falta la unidad {uid}")
            continue
        preguntas = banco[uid]
        if len(preguntas) != 6:
            errores.append(f"{uid}: {len(preguntas)} preguntas, se esperan 6")
        for niv in NIVELES:
            n = sum(1 for p in preguntas if p.get("nivel") == niv)
            if n != 2:
                errores.append(f"{uid}: {n} preguntas de nivel {niv}, se esperan 2")
        for p in preguntas:
            pid = p.get("id", "?")
            if pid in ids_vistos:
                errores.append(f"{uid}: id repetido {pid}")
            ids_vistos.add(pid)
            if not str(p.get("enunciado", "")).strip():
                errores.append(f"{pid}: sin enunciado")
            ops = p.get("opciones", [])
            if len(ops) != 4 or sorted(o.get("id") for o in ops) != ["a", "b", "c", "d"]:
                errores.append(f"{pid}: las opciones deben ser exactamente a, b, c, d")
            if sum(1 for o in ops if o.get("correcta") is True) != 1:
                errores.append(f"{pid}: debe haber exactamente una opción correcta")
            for o in ops:
                if not str(o.get("texto", "")).strip() or not str(o.get("explicacion", "")).strip():
                    errores.append(f"{pid}{o.get('id', '?')}: opción sin texto o sin explicación")
    extra = set(banco) - set(unidades)
    if extra:
        errores.append(f"unidades que no están en el hilo: {sorted(extra)}")
    return errores


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--parcial", action="store_true")
    args = ap.parse_args()
    unidades = orden_unidades()
    banco = cargar_fragmentos()
    errores = validar(banco, unidades, args.parcial)
    if errores:
        print("\n".join("  - " + e for e in errores), file=sys.stderr)
        return 1
    ordenado = {uid: banco[uid] for uid in unidades if uid in banco}
    total = sum(len(v) for v in ordenado.values())
    print(f"banco: {len(ordenado)} unidades, {total} preguntas")
    if args.check:
        return 0
    cuerpo = pprint.pformat(ordenado, width=110, sort_dicts=False)
    SALIDA.write_text(
        '"""GENERADO por tools/merge_banco.py desde unidades/_banco/bloque_*.py: no editar a mano.\n\n'
        "Banco de autoevaluación: 6 preguntas por unidad (2 elementales, 2 medias, 2 avanzadas), 4 opciones\n"
        'con explicación cada una. Lo importa cb104.py y tools/build.py lo embebe en cada export WASM.\n"""\n\n'
        f"BANCO_AUTOEVALUACION = {cuerpo}\n",
        encoding="utf-8",
    )
    print(f"escrito {SALIDA.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
