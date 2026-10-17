"""Prototipo: reconstrucción de un DEM (Copernicus GLO-30, Precordillera de Mendoza) con SVD truncada.

Uso: python svd_dem_proto.py [dem.npy]   (default: dem_precordillera_512.npy)
Genera svd_dem_proto.png, imprime tabla k -> RMS (m) y tiempos de SVD para 512 y 1024.
"""
import sys, time, json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

path = sys.argv[1] if len(sys.argv) > 1 else "dem_precordillera_512.npy"
Z = np.load(path).astype(np.float64)
n, m = Z.shape
KS = [1, 2, 5, 10, 20, 50, 100]

# ---- SVD ----
t0 = time.perf_counter()
U, s, Vt = np.linalg.svd(Z, full_matrices=False)
t_svd = time.perf_counter() - t0
print(f"{path}: {n}x{m}, SVD en {t_svd:.3f} s")

def recon(k):
    return (U[:, :k] * s[:k]) @ Vt[:k, :]

energy = np.cumsum(s**2) / np.sum(s**2)
rms = {k: float(np.sqrt(np.mean((Z - recon(k))**2))) for k in KS}
rel = {k: rms[k] / Z.std() for k in KS}

print("\n k   RMS (m)   RMS/std   energía acumulada")
for k in KS:
    print(f"{k:4d}  {rms[k]:8.2f}  {rel[k]:7.3f}   {energy[k-1]:.6f}")
# k mínimo para RMS < 10 m / 5 m
for thr in (50, 20, 10, 5):
    kk = next((k for k in range(1, len(s)+1) if np.sqrt(np.mean((Z - recon(k))**2)) < thr), None)
    print(f"k mínimo con RMS < {thr:3d} m: {kk}")

# ---- figura ----
ls = LightSource(azdeg=315, altdeg=45)
vmin, vmax = Z.min(), Z.max()
def shade(A):
    return ls.shade(A, cmap=plt.cm.terrain, vert_exag=1.0, blend_mode="overlay",
                    dx=25, dy=30, vmin=vmin, vmax=vmax)

fig = plt.figure(figsize=(18, 14), constrained_layout=True)
gs = fig.add_gridspec(4, 4)

ax = fig.add_subplot(gs[0, 0]); ax.semilogy(np.arange(1, len(s)+1), s, lw=1)
ax.set_title("(a) Valores singulares (log)"); ax.set_xlabel("k"); ax.set_ylabel("σ_k"); ax.grid(alpha=.3)
ax = fig.add_subplot(gs[0, 1]); ax.plot(np.arange(1, len(s)+1), energy, lw=1)
ax.set_xscale("log"); ax.set_ylim(0.9, 1.001); ax.set_title("(b) Energía acumulada Σσ²"); ax.set_xlabel("k (log)"); ax.grid(alpha=.3)
for k in KS: ax.axvline(k, color="gray", lw=.5, ls=":")
ax = fig.add_subplot(gs[0, 2]); ax.plot(KS, [rms[k] for k in KS], "o-")
ax.set_xscale("log"); ax.set_yscale("log"); ax.set_title("(b') RMS del error [m] vs k"); ax.set_xlabel("k"); ax.set_ylabel("RMS [m]"); ax.grid(alpha=.3, which="both")
ax = fig.add_subplot(gs[0, 3]); ax.imshow(shade(Z)); ax.set_title(f"Original {n}×{m}  (z {vmin:.0f}–{vmax:.0f} m)"); ax.axis("off")

for i, k in enumerate(KS):
    ax = fig.add_subplot(gs[1 + i // 4, i % 4])
    ax.imshow(shade(recon(k))); ax.axis("off")
    ax.set_title(f"(c) k={k}  RMS={rms[k]:.1f} m  ({100*energy[k-1]:.2f}% energía)")

ax = fig.add_subplot(gs[2, 3])
ax.imshow(np.abs(Z - recon(20)), cmap="magma", vmin=0, vmax=100); ax.axis("off"); ax.set_title("|error| k=20 (0–100 m)")

ax = fig.add_subplot(gs[3, 0:2])
for j in range(3): ax.plot(U[:, j], lw=.8, label=f"u{j+1}")
ax.set_title("(d) 3 primeros vectores singulares izquierdos (perfil N→S, filas)"); ax.legend(); ax.grid(alpha=.3)
ax = fig.add_subplot(gs[3, 2:4])
for j in range(3): ax.plot(Vt[j, :], lw=.8, label=f"v{j+1}")
ax.set_title("(d) 3 primeros vectores singulares derechos (perfil W→E, columnas)"); ax.legend(); ax.grid(alpha=.3)

fig.suptitle(f"DEM Copernicus GLO-30 — Precordillera de Mendoza — SVD truncada ({path})", fontsize=14)
fig.savefig("svd_dem_proto.png", dpi=110)
print("figura: svd_dem_proto.png")

# ---- benchmark ----
print("\nTiempos SVD (np.linalg.svd, full_matrices=False), mediana de 3:")
bench = {}
for name in ("dem_precordillera_512.npy", "dem_precordillera_1024.npy"):
    A = np.load(name)
    for dt in (np.float32, np.float64):
        B = A.astype(dt); ts = []
        for _ in range(3):
            t0 = time.perf_counter(); np.linalg.svd(B, full_matrices=False); ts.append(time.perf_counter() - t0)
        bench[f"{B.shape[0]}_{dt.__name__}"] = float(np.median(ts))
        print(f"  {B.shape[0]}x{B.shape[1]} {dt.__name__}: {np.median(ts):.3f} s")
    # reconstrucción sola (lo que haría el slider con U,s,Vt cacheados)
    U_, s_, Vt_ = np.linalg.svd(A.astype(np.float32), full_matrices=False)
    t0 = time.perf_counter(); (U_[:, :50] * s_[:50]) @ Vt_[:50]; tr = time.perf_counter() - t0
    print(f"  {A.shape[0]}: reconstrucción k=50 con factores cacheados: {tr*1000:.1f} ms")
json.dump({"rms_m": rms, "energy": {k: float(energy[k-1]) for k in KS}, "t_svd_s": bench}, open("svd_results.json", "w"), indent=2)
