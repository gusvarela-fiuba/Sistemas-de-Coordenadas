"""Escala de Gauss-Kruger en el borde de faja (complemento de conformes). Determinista.

Ejecutar desde la raiz del repositorio:
    uv run python apunte/scripts/capc2_conformes.py

Salida esperada (resumen): borde de faja (lon -58,5, lat -34,6): k-1 = +2.333e-04 = 23,3 cm/km;
ecuador, borde de faja: k-1 = +3.451e-04 = 34,5 cm/km; meridiano central: k-1 = 0.

Se toma el meridiano central y k0 de POSGAR 2007 / Argentina 5 (EPSG:5347) y se
calcula sobre el elipsoide GRS80 (el de POSGAR 2007). PROJ declara WGS 84 en ese
CRS (diferencia de f ~ 1e-10, sin efecto en las cifras), por eso se fija GRS80.
"""
import math
import pyproj

crs = pyproj.CRS("EPSG:5347")
par = {p.name: p.value for p in crs.coordinate_operation.params}
lon0 = par["Longitude of natural origin"]
k0 = par["Scale factor at natural origin"]
print("CRS:", crs.name, "| datum:", crs.datum.name, "| elipsoide en PROJ:", crs.datum.ellipsoid.name)
print(f"Meridiano central = {lon0} deg, k0 = {k0}")

proj = pyproj.Proj(f"+proj=tmerc +lat_0=-90 +lon_0={lon0} +k={k0} +ellps=GRS80")
print("Elipsoide usado: GRS80, a =", proj.crs.ellipsoid.semi_major_metre, "1/f =", proj.crs.ellipsoid.inverse_flattening)

def fila(lat, dl, etiqueta):
    f = proj.get_factors(lon0 + dl, lat)
    k = f.meridional_scale  # conforme: coincide con parallel_scale
    aprox = 0.5 * math.radians(dl) ** 2 * math.cos(math.radians(lat)) ** 2
    print(f"{etiqueta}: lat={lat} dl={dl} mer={f.meridional_scale:.8f} "
          f"par={f.parallel_scale:.8f} areal={f.areal_scale:.8f}")
    print(f"    k-1 = {k-1:+.3e} = {(k-1)*1e6:+.1f} ppm = {(k-1)*1e5:+.1f} cm/km | "
          f"1/2 dl^2 cos^2 = {aprox:.3e} = {aprox*1e5:.1f} cm/km")

fila(-34.6, 0.0, "meridiano central")
fila(-34.6, 1.5, "borde de faja a -34,6")
fila(0.0, 1.5, "ecuador, borde de faja")
