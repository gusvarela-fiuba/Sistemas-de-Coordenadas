"""Recorta ventanas con relieve del tile Copernicus GLO-30 S33/W069 y las guarda como .npy.

Guía didáctica de Python y Rasterio para Agrimensura y Geodesia:
  1. Georreferenciación afín (`ds.transform`):
     - Un archivo GeoTIFF asocia a la matriz discreta de alturas una transformación
       afín bidimensional `T` (capítulos 4 y 10). Esta matriz mapea índices continuos
       de píxel `(columna, fila)` a coordenadas geodésicas angulares `(longitud, latitud)`.
     - En Python, la librería `rasterio` sobrecarga el operador `*` para evaluar la
       transformación afín: `lon, lat = T * (col, fila)`. Fijate que `T.a` representa
       el tamaño de píxel en longitud (positivo hacia el Este) y `T.e` en latitud
       (negativo, porque las filas de la imagen crecen de Norte a Sur).
  2. Lectura eficiente por ventanas (`rasterio.windows.Window`):
     - Para evitar cargar un tile completo de millones de puntos en memoria RAM,
       `Window(c0, r0, ancho, alto)` realiza lecturas directas por bloques desde
       el disco, obteniendo exclusivamente el recorte deseado.
  3. Almacenamiento numérico en formato binario (`np.save`):
     - La función `astype(np.float32)` convierte los datos de elevación a precisión
       simple de 32 bits (suficiente para resolución submétrica en topografía) y
       `np.save` los almacena como archivo `.npy` listo para cómputo matricial rápido.
"""
import json
from pathlib import Path

import numpy as np
try:
    import rasterio
    from rasterio.windows import Window
except ImportError:
    rasterio = None
    Window = None

SRC = "Copernicus_DSM_COG_10_S33_00_W069_00_DEM.tif"
# Definimos las ventanas de interés: (nombre, fila_inicial, col_inicial, tamaño_cuadrado).
# Por convención geodésica, la fila 0 corresponde al límite norte (latitud -32,0°)
# y la columna 0 al límite oeste (longitud -69,0°).
WINDOWS = [
    ("dem_precordillera_1024", 512, 0, 1024),
    ("dem_precordillera_512",  512, 0, 512),
]

meta = {}
# Verificamos si el archivo GeoTIFF original está disponible en la carpeta local;
# si no está (por ejemplo, en entornos ligeros de pruebas), documentamos la estructura.
if rasterio is not None and Path(SRC).exists():
    with rasterio.open(SRC) as ds:
        # Obtenemos la matriz de transformación afín del raster
        T = ds.transform
        for name, r0, c0, n in WINDOWS:
            # 1. Leemos del disco únicamente la ventana cuadrada de n x n píxeles
            a = ds.read(1, window=Window(c0, r0, n, n)).astype(np.float32)

            # 2. Guardamos la matriz de elevaciones en disco en formato binario .npy
            np.save(f"{name}.npy", a)

            # 3. Calculamos las coordenadas geográficas de las esquinas aplicando la afín T
            lon0, lat0 = T * (c0, r0)          # Esquina Noroeste (NW)
            lon1, lat1 = T * (c0 + n, r0 + n)  # Esquina Sureste (SE)

            # 4. Registramos los metadatos topográficos y estadísticos del recorte
            meta[name] = dict(
                source=SRC,
                rows=[r0, r0 + n],
                cols=[c0, c0 + n],
                shape=list(a.shape),
                lat=[round(lat1, 4), round(lat0, 4)],
                lon=[round(lon0, 4), round(lon1, 4)],
                zmin=float(a.min()),
                zmax=float(a.max()),
                zmean=float(a.mean()),
                zstd=float(a.std()),
                pixel_deg=round(T.a, 7),
                pixel_m_approx="~30 m N-S, ~25 m E-W a lat -32",
            )
            print(f"Recorte generado: {name} -> dimensiones {a.shape}, cotas {a.min():.1f} a {a.max():.1f} m")

    # Persistimos el diccionario de metadatos en un archivo JSON formateado
    with open("crop_meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2)

