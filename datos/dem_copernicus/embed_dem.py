"""Genera la submuestra 128×128 del DEM de la Precordillera embebida en `unidades/cb104.py` (lección 09).

Toma `dem_precordillera_512.npy` (float32), se queda con `a[::4, ::4]` (paso ≈ 120 m), redondea al metro (int16),
codifica cada fila como deltas (primera columna absoluta), comprime con zlib y lo escribe en base85 entre los
marcadores `# dem-blob:begin` / `# dem-blob:end` de cb104.py, partido en líneas de 96 caracteres. Verifica que lo
que queda escrito se decodifica al mismo array. El export WASM no puede leer archivos, por eso el blob viaja
adentro del módulo (y, vía tools/build.py, adentro de cada lección exportada): hay que mantenerlo en ~20 KB.

Guía didáctica de Python y NumPy:
  1. Submuestreo por rebanado (*strided slicing* `a[::4, ::4]`):
     - `a[inicio:fin:paso]` toma elementos saltando según `paso`. En 2D, `a[::4, ::4]`
       retiene una de cada 4 filas y una de cada 4 columnas sin hacer copias pesadas
       en memoria intermedia, reduciendo la matriz de 512×512 a 128×128 en una sola instrucción.
  2. Codificación delta bidimensional (`np.diff` y `np.cumsum`):
     - Las alturas topográficas en un terreno natural tienen alta autocorrelación espacial
       (dos puntos vecinos tienen cotas muy parecidas).
     - Al calcular diferencias columna a columna con `np.diff(q, axis=1, prepend=0)`,
       la primera columna almacena la cota de partida y las restantes guardan números muy chicos
       (desniveles locales). El algoritmo DEFLATE (`zlib`) comprime estos enteros pequeños
       con extrema eficiencia.
     - Para recuperar la superficie original, basta aplicar la operación inversa:
       la suma acumulativa `np.cumsum(..., axis=1)`.
  3. Empaquetado binario y texto ASCII seguro (`zlib` + `base85`):
     - `zlib.compress(..., 9)` aplica la máxima compresión sin pérdidas.
     - `base64.b85encode` convierte el flujo binario comprimido en caracteres ASCII legibles
       que pueden embeberse directamente en el código fuente Python del proyecto para su
       ejecución tanto en entornos locales como en WebAssembly (WASM / Pyodide).

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
    """Codifica la matriz de alturas en un blob comprimido en base85."""
    # 1. Redondeamos las cotas al metro entero y convertimos a enteros de 16 bits con signo
    q = np.round(a).astype(np.int16)
    # 2. Obtenemos las diferencias por filas. Con prepend=0, la columna 0 conserva el valor absoluto
    # y las columnas 1 a N-1 almacenan las diferencias con el píxel anterior a la izquierda.
    # Usamos little-endian int16 ("<i2") para garantizar reproducibilidad entre arquitecturas.
    d = np.diff(q, axis=1, prepend=0).astype("<i2")
    # 3. Comprimimos con zlib nivel 9 y codificamos a base85 (más compacto que base64)
    return base64.b85encode(zlib.compress(d.tobytes(), 9)).decode("ascii")


def decodificar(blob: str, n: int) -> np.ndarray:
    """Decodifica el blob base85 reconstruyendo la matriz original n×n mediante np.cumsum."""
    # 1. Decodificamos de base85 a bytes y descomprimimos con zlib
    raw = zlib.decompress(base64.b85decode(blob))
    # 2. Reconstruimos la matriz de enteros (n, n) a partir del buffer binario
    d = np.frombuffer(raw, dtype="<i2").reshape(n, n)
    # 3. Aplicamos la suma acumulada horizontal para restaurar las cotas exactas
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
