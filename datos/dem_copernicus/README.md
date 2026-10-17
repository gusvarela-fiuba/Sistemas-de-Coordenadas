# DEM Copernicus GLO-30 — recorte Precordillera de Mendoza (para notebook SVD)

Fuente: Copernicus DEM GLO-30, AWS Open Data (S3 público, sin login).
Tile: `https://copernicus-dem-30m.s3.amazonaws.com/Copernicus_DSM_COG_10_S33_00_W069_00_DEM/Copernicus_DSM_COG_10_S33_00_W069_00_DEM.tif`
(COG float32 3600×3600, EPSG:4326, 1 arcsec ≈ 30 m, lon [−69,−68] lat [−33,−32], 35,8 MB; es DSM, no DTM).
Licencia: Copernicus DEM licence (uso libre con atribución). Atribución: "© DLR e.V. 2010-2014 and © Airbus Defence and Space GmbH 2014-2018 provided under COPERNICUS by the European Union and ESA".

Recortes (`.npy` float32, ver `crop_meta.json`):
- `dem_precordillera_512.npy`: filas 512–1024, cols 0–512 → lat −32.284…−32.142, lon −69.000…−68.858; z 1014–2989 m, std 406 m.
- `dem_precordillera_1024.npy`: filas 512–1536, cols 0–1024 → lat −32.427…−32.142, lon −69.000…−68.716; z 597–2989 m, std 513 m.

Prototipo `svd_dem_proto.py` (numpy, matplotlib): espectro, energía, RMS vs k, reconstrucciones k=1…100 en hillshade, vectores singulares como perfiles.

k → RMS (m), recorte 512: 1→103, 2→66, 5→31, 10→17, 20→9.8, 50→4.4, 100→2.0. El relieve "aparece" en k≈20.
Tiempos SVD (M1): 512² 0.06 s, 1024² 0.4 s; reconstrucción con U,s,Vt cacheados < 2 ms → viable con slider en marimo.
Nota didáctica: la energía acumulada engaña (99.6 % con k=1) porque la media (~1600 m) domina σ₁; mostrar también la versión con media restada o usar RMS/std.

Descartados: IGN MDE-Ar (solo por portal web, sin URL directa), NASADEM/SRTM (Earthdata login obligatorio).
Recon 2026-09-21.
