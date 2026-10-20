# %% [markdown]
# # FIUBA - CB104 Sistemas de Coordenadas
# ## Intersección de Variedades en ℝ³: Paraboloide y Plano
#
# **Superficies a intersectar:**
# 1. **Paraboloide de Revolución (invertido):**
#    $$S_1: x^2 + y^2 + z = 1 \iff z = 1 - (x^2 + y^2)$$
#    Vértice en $(0, 0, 1)$, simétrico respecto al eje $Z$ y abierto hacia abajo.
#
# 2. **Plano Vertical:**
#    $$S_2: x + y = 1 \iff y = 1 - x$$
#
# ---
# ### Marco Teórico (Variedades y Espacio Tangente)
# - Funciones implícitas:
#   $$F_1(x, y, z) = x^2 + y^2 + z - 1 = 0$$
#   $$F_2(x, y, z) = x + y - 1 = 0$$
#
# - Vectores normales (Gradientes):
#   $$\nabla F_1(x, y, z) = (2x, 2y, 1)$$
#   $$\nabla F_2(x, y, z) = (1, 1, 0)$$
#
# - Vector director tangente a la curva de intersección:
#   $$\mathbf{v}(x, y, z) = \nabla F_1 \times \nabla F_2 = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ 2x & 2y & 1 \\ 1 & 1 & 0 \end{vmatrix} = (-1, 1, 2x - 2y)$$

# %%
# ==============================================================================
# GUÍA DIDÁCTICA DE PYTHON, NUMPY, MATPLOTLIB Y PLOTLY
# ==============================================================================
# 1. Grillas 1D y 2D (`np.linspace` y `np.meshgrid`):
#    - `np.linspace(a, b, N)` genera `N` puntos equiespaciados entre `a` y `b`
#      (incluyendo ambos extremos).
#    - `R, THETA = np.meshgrid(r, theta)` cruza dos vectores 1D para formar dos
#      matrices 2D de coordenadas polares sobre las cuales evaluamos `X`, `Y`, `Z`
#      de forma vectorizada (sin bucles `for`).
# 2. Potencias en Python (`**` vs. `^`):
#    En Python la potencia se escribe con doble asterisco (`t_vals**2`), a
#    diferencia de Julia o MATLAB donde se usa `^` (en Python `^` es el XOR bit a bit).
# 3. Gráficos 3D estáticos (`matplotlib`) e interactivos (`plotly`):
#    - `ax.plot_surface(X, Y, Z, ...)` dibuja una malla 2D en el espacio 3D.
#    - `ax.quiver(x0, y0, z0, vx, vy, vz)` dibuja una flecha 3D con origen en
#      `(x0, y0, z0)` y componentes `(vx, vy, vz)` (acá, los gradientes normales
#      y el vector tangente a la curva de intersección).
#    - `go.Figure()` de Plotly exporta un archivo `.html` autónomo que se puede
#      girar con el mouse en cualquier navegador.
# ==============================================================================
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

print("✓ Entorno configurado.")

# %% [markdown]
# ## 1. Resolución Analítica
# Sustituyendo la ecuación del plano $y = 1 - x$ en la del paraboloide:
# $$z = 1 - x^2 - (1 - x)^2 = 1 - x^2 - (1 - 2x + x^2) = 2x - 2x^2$$
#
# Tomando $x = t$ como parámetro libre, la curva de intersección $\mathbf{r}(t)$ es una **PARÁBOLA en el espacio**:
# $$\mathbf{r}(t) = \begin{pmatrix} t \\ 1 - t \\ 2t - 2t^2 \end{pmatrix}, \quad t \in \mathbb{R}$$
#
# Puntos notables:
# - **Vértice de la parábola ($z$ máximo):**
#   $$\frac{dz}{dt} = 2 - 4t = 0 \implies t = 0.5 \implies V = (0.5, 0.5, 0.5)$$
# - **Corte con el plano $z = 0$ ($2t - 2t^2 = 0$):**
#   - $t = 0 \implies P_1 = (0, 1, 0)$
#   - $t = 1 \implies P_2 = (1, 0, 0)$

# %%
# Parámetro t para la curva de intersección
t_vals = np.linspace(-0.6, 1.6, 200)
x_curva = t_vals
y_curva = 1.0 - t_vals
z_curva = 2.0 * t_vals - 2.0 * (t_vals**2)

# Vértice
t_v = 0.5
vertice = np.array([t_v, 1.0 - t_v, 2.0*t_v - 2.0*(t_v**2)])

# Puntos de corte en z = 0
P1 = np.array([0.0, 1.0, 0.0])
P2 = np.array([1.0, 0.0, 0.0])

print(f"Vértice de la parábola: V = {vertice}")
print(f"Cortes con z = 0: P1 = {P1}, P2 = {P2}")

# Verificación de tangentes
# Derivada r'(t) = (1, -1, 2 - 4t)
v_vertice = np.array([1.0, -1.0, 2.0 - 4.0*t_v])
print(f"Vector tangente en el vértice (debe ser horizontal, z=0): {v_vertice}")

# %% [markdown]
# ## 2. Visualización 3D con Matplotlib

# %%
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. Malla del Paraboloide z = 1 - (x² + y²) en coordenadas polares
r = np.linspace(0.0, 1.7, 60)
theta = np.linspace(0.0, 2*np.pi, 80)
R, THETA = np.meshgrid(r, theta)
X_parab = R * np.cos(THETA)
Y_parab = R * np.sin(THETA)
Z_parab = 1.0 - (X_parab**2 + Y_parab**2)

# 2. Malla del Plano x + y = 1 => y = 1 - x
x_pl = np.linspace(-1.3, 2.0, 40)
z_pl = np.linspace(-2.0, 1.5, 40)
X_pl, Z_pl = np.meshgrid(x_pl, z_pl)
Y_pl = 1.0 - X_pl

# Superficie Paraboloide
surf1 = ax.plot_surface(X_parab, Y_parab, Z_parab, color='#3498db', alpha=0.35, 
                        edgecolor='none', label='Paraboloide: x²+y²+z=1')

# Superficie Plano
surf2 = ax.plot_surface(X_pl, Y_pl, Z_pl, color='#e67e22', alpha=0.45, 
                        edgecolor='none', label='Plano: x+y=1')

# Curva de Intersección (Parábola 3D)
ax.plot(x_curva, y_curva, z_curva, color='red', lw=4.5, 
        label=r'Intersección: Parábola $\mathbf{r}(t)$', zorder=10)

# Puntos Notables
ax.scatter([vertice[0]], [vertice[1]], [vertice[2]], color='black', s=100, marker='^', label=f'Vértice (0.5, 0.5, 0.5)')
ax.scatter([P1[0], P2[0]], [P1[1], P2[1]], [P1[2], P2[2]], color='darkgreen', s=80, marker='o', label='Cortes en z=0')

# Vectores normales en el vértice (x=0.5, y=0.5, z=0.5)
# Normal al Paraboloide: (2x, 2y, 1) = (1, 1, 1)
ax.quiver(0.5, 0.5, 0.5, 0.6, 0.6, 0.6, color='blue', lw=2.5, arrow_length_ratio=0.2)
ax.text(1.15, 1.15, 1.15, r'$\nabla F_1$', color='blue', fontsize=11, fontweight='bold')

# Normal al Plano: (1, 1, 0)
ax.quiver(0.5, 0.5, 0.5, 0.6, 0.6, 0.0, color='#d35400', lw=2.5, arrow_length_ratio=0.2)
ax.text(1.15, 1.15, 0.5, r'$\nabla F_2$', color='#d35400', fontsize=11, fontweight='bold')

# Vector tangente v = (-1, 1, 0)
ax.quiver(0.5, 0.5, 0.5, -0.6, 0.6, 0.0, color='red', lw=2.5, arrow_length_ratio=0.2)
ax.text(-0.2, 1.15, 0.5, r'$\mathbf{v}$ (tangente)', color='red', fontsize=11, fontweight='bold')

# Configuración de límites y vista
ax.set_xlim(-1.8, 2.0)
ax.set_ylim(-1.8, 2.0)
ax.set_zlim(-2.0, 1.5)
ax.set_xlabel('Eje X', fontweight='bold')
ax.set_ylabel('Eje Y', fontweight='bold')
ax.set_zlabel('Eje Z', fontweight='bold')
ax.set_title(r'Intersección Paraboloide $x^2 + y^2 + z = 1$ y Plano $x + y = 1$', fontsize=13, fontweight='bold', pad=15)
ax.view_init(elev=22, azim=45)

plt.tight_layout()
plt.savefig('interseccion_3d_matplotlib.png', dpi=150)
print("✓ Imagen guardada: interseccion_3d_matplotlib.png")
plt.show()

# %% [markdown]
# ## 3. Visualización 3D Interactiva con Plotly

# %%
fig_plotly = go.Figure()

# Paraboloide
fig_plotly.add_trace(go.Surface(
    x=X_parab, y=Y_parab, z=Z_parab,
    colorscale='Blues', showscale=False, opacity=0.45,
    name='Paraboloide: x² + y² + z = 1',
    hoverinfo='name+x+y+z'
))

# Plano
fig_plotly.add_trace(go.Surface(
    x=X_pl, y=Y_pl, z=Z_pl,
    colorscale='Oranges', showscale=False, opacity=0.5,
    name='Plano: x + y = 1',
    hoverinfo='name+x+y+z'
))

# Curva de Intersección (Parábola)
fig_plotly.add_trace(go.Scatter3d(
    x=x_curva, y=y_curva, z=z_curva,
    mode='lines',
    line=dict(color='red', width=9),
    name='Parábola de Intersección',
    hoverinfo='name+x+y+z'
))

# Puntos notables
fig_plotly.add_trace(go.Scatter3d(
    x=[vertice[0]], y=[vertice[1]], z=[vertice[2]],
    mode='markers+text',
    marker=dict(size=9, color='black', symbol='diamond'),
    text=['Vértice (0.5, 0.5, 0.5)'],
    textposition='top center',
    name='Vértice de la parábola'
))

fig_plotly.add_trace(go.Scatter3d(
    x=[P1[0], P2[0]], y=[P1[1], P2[1]], z=[P1[2], P2[2]],
    mode='markers+text',
    marker=dict(size=7, color='green'),
    text=['P1 (0, 1, 0)', 'P2 (1, 0, 0)'],
    textposition='bottom center',
    name='Cortes z=0'
))

fig_plotly.update_layout(
    title='<b>Intersección 3D: Paraboloide x² + y² + z = 1 y Plano x + y = 1</b><br><sup>CB104 Sistemas de Coordenadas - FIUBA</sup>',
    scene=dict(
        xaxis=dict(title='X', range=[-1.8, 2.0]),
        yaxis=dict(title='Y', range=[-1.8, 2.0]),
        zaxis=dict(title='Z', range=[-2.0, 1.5]),
        aspectmode='cube'
    ),
    width=850, height=650
)

fig_plotly.write_html('interseccion_3d_interactiva.html')
print("✓ Archivo interactivo 3D guardado: interseccion_3d_interactiva.html")
fig_plotly.show()
