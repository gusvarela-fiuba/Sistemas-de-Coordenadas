"""Genera la submuestra 128×128 del DEM de la Precordillera embebida en `unidades/cb104.py` (lección 09).

Toma `dem_precordillera_512.npy` (float32), se queda con `a[::4, ::4]` (paso ≈ 120 m), redondea al metro (int16),
codifica cada fila como deltas (primera columna absoluta), comprime con zlib y lo escribe en base85 entre los
marcadores `# dem-blob:begin` / `# dem-blob:end` de cb104.py, partido en líneas de 96 caracteres. Verifica que lo
que queda escrito se decodifica al mismo array. El export WASM no puede leer archivos, por eso el blob viaja
adentro del módulo (y, vía tools/build.py, adentro de cada lección exportada): hay que mantenerlo en ~20 KB.

Uso (desde la raíz del repo):  uv run python datos/dem_copernicus/embed_dem.py
"""

from __future__ import annotations

import base64
import re
import sys
import zlib
from pathlib import Path

import numpy as np

RAIZ = Path(__file__).resolve().parent.parent.parent
NPY = Path(__file__).resolve().parent / "dem_precordillera_512.npy"
CB104 = RAIZ / "unidades" / "cb104.py"
PASO = 4
ANCHO_LINEA = 96


def codificar(a: np.ndarray) -> str:
    q = np.round(a).astype(np.int16)
    d = np.diff(q, axis=1, prepend=0).astype("<i2")  # columna 0 absoluta, el resto deltas
    return base64.b85encode(zlib.compress(d.tobytes(), 9)).decode("ascii")


def decodificar(blob: str, n: int) -> np.ndarray:
    d = np.frombuffer(zlib.decompress(base64.b85decode(blob)), dtype="<i2").reshape(n, n)
    return np.cumsum(d, axis=1, dtype=np.int32).astype(np.float32)


def main() -> None:
    a = np.load(NPY)
    s = a[::PASO, ::PASO]
    n = s.shape[0]
    blob = codificar(s)
    assert np.array_equal(decodificar(blob, n), np.round(s).astype(np.float32)), "ida y vuelta"
    lineas = [blob[i : i + ANCHO_LINEA] for i in range(0, len(blob), ANCHO_LINEA)]
    bloque = (
        f"# dem-blob:begin  ({n}×{n} = {NPY.name}[::{PASO}, ::{PASO}], int16 al metro, delta por filas, zlib, base85: "
        f"{len(blob)} caracteres)\n_DEM_N = {n}\n_DEM_B85 = (\n"
        + "".join(f'    "{l}"\n' for l in lineas)
        + ")\n# dem-blob:end"
    )
    texto = CB104.read_text(encoding="utf-8")
    patron = re.compile(r"# dem-blob:begin.*?# dem-blob:end", re.S)
    if not patron.search(texto):
        sys.exit(f"ERROR: {CB104} no tiene los marcadores # dem-blob:begin / # dem-blob:end")
    CB104.write_text(patron.sub(lambda m: bloque, texto, count=1), encoding="utf-8")
    print(f"{NPY.name}: {a.shape} → submuestra {s.shape}, alturas {s.min():.1f}–{s.max():.1f} m")
    print(f"blob: {len(blob)} caracteres base85 ({len(bloque)} bytes con formato) escrito en {CB104.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
