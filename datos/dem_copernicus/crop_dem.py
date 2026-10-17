"""Recorta ventanas con relieve del tile Copernicus GLO-30 S33/W069 y las guarda como .npy."""
import json, numpy as np, rasterio
from rasterio.windows import Window

SRC = "Copernicus_DSM_COG_10_S33_00_W069_00_DEM.tif"
# (nombre, fila0, col0, tamaño) — fila 0 = lat -32.0 (norte), col 0 = lon -69.0 (oeste)
WINDOWS = [("dem_precordillera_1024", 512, 0, 1024),
           ("dem_precordillera_512",  512, 0, 512)]
meta = {}
with rasterio.open(SRC) as ds:
    T = ds.transform
    for name, r0, c0, n in WINDOWS:
        a = ds.read(1, window=Window(c0, r0, n, n)).astype(np.float32)
        np.save(f"{name}.npy", a)
        lon0, lat0 = T * (c0, r0)          # esquina NW
        lon1, lat1 = T * (c0 + n, r0 + n)  # esquina SE
        meta[name] = dict(source=SRC, rows=[r0, r0 + n], cols=[c0, c0 + n], shape=list(a.shape),
                          lat=[round(lat1, 4), round(lat0, 4)], lon=[round(lon0, 4), round(lon1, 4)],
                          zmin=float(a.min()), zmax=float(a.max()), zmean=float(a.mean()), zstd=float(a.std()),
                          pixel_deg=round(T.a, 7), pixel_m_approx="~30 m N-S, ~25 m E-W a lat -32")
        print(name, meta[name])
json.dump(meta, open("crop_meta.json", "w"), indent=2)
