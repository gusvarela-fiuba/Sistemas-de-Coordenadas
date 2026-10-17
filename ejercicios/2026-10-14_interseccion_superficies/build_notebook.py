import json
import nbformat as nbf

nb = nbf.v4.new_notebook()

nb.metadata = {
    "kernelspec": {
        "display_name": "Python (Sistemas de Coordenadas)",
        "language": "python",
        "name": "sistemas_coordenadas"
    },
    "language_info": {
        "codemirror_mode": {"name": "ipython", "version": 3},
        "file_extension": ".py",
        "mimetype": "text/x-python",
        "name": "python",
        "nbconvert_exporter": "python",
        "pygments_lexer": "ipython3",
        "version": "3.12.13"
    }
}

cells = []

# Cell 1: Intro Markdown
cells.append(nbf.v4.new_markdown_cell(r"""# FIUBA - CB104 Sistemas de Coordenadas
## Intersección de Variedades en $\mathbb{R}^3$: Paraboloide y Plano

Modelamos y visualizamos en 3D la intersección entre:
1. **Superficie Cuadrática (Paraboloide de revolución invertido):**
   $$S_1: x^2 + y^2 + z = 1 \iff z = 1 - (x^2 + y^2)$$
   Superficie con vértice en $(0, 0, 1)$, simétrica respecto al eje $Z$ y que se abre hacia abajo ($z \le 1$).

2. **Plano Vertical:**
   $$S_2: x + y = 1 \iff y = 1 - x$$

---
### Marco Teórico (Geometría Diferencial de Variedades)
* **Funciones implícitas de nivel cero:**
  $$F_1(x, y, z) = x^2 + y^2 + z - 1 = 0$$
  $$F_2(x, y, z) = x + y - 1 = 0$$
* **Campos de gradientes normales a cada variedad:**
  $$\nabla F_1(x, y, z) = (2x, 2y, 1)$$
  $$\nabla F_2(x, y, z) = (1, 1, 0)$$
* **Vector tangente a la curva de intersección:**
  $$\mathbf{v}(x, y, z) = \nabla F_1 \times \nabla F_2 = \begin{vmatrix} \hat{i} & \hat{j} & \hat{k} \\ 2x & 2y & 1 \\ 1 & 1 & 0 \end{vmatrix} = (-1, 1, 2x - 2y)$$
"""))

# Cell 2: Imports
cells.append(nbf.v4.new_code_cell(r"""import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['figure.dpi'] = 120
print("✓ Librerías importadas.")
"""))

# Cell 3: Markdown - Resolución analítica
cells.append(nbf.v4.new_markdown_cell(r"""## 1. Resolución Analítica: La Parábola Espacial

Despejando $y = 1 - x$ del plano y sustituyendo en la ecuación del paraboloide:
$$z = 1 - x^2 - y^2 = 1 - x^2 - (1 - x)^2 = 1 - x^2 - (1 - 2x + x^2) = 2x - 2x^2$$

Tomando $x = t$ como parámetro libre, la curva de intersección es una **parábola contenida en el plano vertical $x + y = 1$**:
$$\mathbf{r}(t) = \begin{pmatrix} x(t) \\ y(t) \\ z(t) \end{pmatrix} = \begin{pmatrix} t \\ 1 - t \\ 2t - 2t^2 \end{pmatrix}, \quad t \in \mathbb{R}$$

### Puntos notables de la curva:
1. **Vértice (altura máxima $z$):**
   $$\frac{dz}{dt} = 2 - 4t = 0 \implies t = \frac{1}{2}$$
   $$V = \mathbf{r}(0.5) = \left(\frac{1}{2}, \frac{1}{2}, \frac{1}{2}\right)$$
   En este punto el vector tangente es horizontal: $\mathbf{r}'(0.5) = (1, -1, 0)$.
2. **Corte con el plano horizontal $z = 0$:**
   $$2t - 2t^2 = 0 \implies 2t(1 - t) = 0 \implies t \in \{0, 1\}$$
   * Para $t = 0 \implies P_1 = (0, 1, 0)$
   * Para $t = 1 \implies P_2 = (1, 0, 0)$
"""))

# Cell 4: Código analítico
cells.append(nbf.v4.new_code_cell(r"""# Parametrización de la curva
t_vals = np.linspace(-0.6, 1.6, 300)
x_curva = t_vals
y_curva = 1.0 - t_vals
z_curva = 2.0*t_vals - 2.0*(t_vals**2)

# Vértice
V = np.array([0.5, 0.5, 0.5])
# Cortes en z = 0
P1 = np.array([0.0, 1.0, 0.0])
P2 = np.array([1.0, 0.0, 0.0])

print(f"Vértice de la parábola: V = {V}")
print(f"Intersección con el plano z = 0: P1 = {P1}, P2 = {P2}")
"""))

# Cell 5: Markdown 3D Matplotlib
cells.append(nbf.v4.new_markdown_cell(r"""## 2. Visualización 3D con Matplotlib

Graficamos:
* El **Paraboloide $x^2 + y^2 + z = 1$** (superficie azul).
* El **Plano $x + y = 1$** (superficie naranja).
* La **Curva de intersección** (parábola roja continua).
* Los **vectores normales $\nabla F_1, \nabla F_2$** y el **vector tangente $\mathbf{v}$** evaluados en el vértice.
"""))

# Cell 6: Código 3D Matplotlib
cells.append(nbf.v4.new_code_cell(r"""fig = plt.figure(figsize=(11, 8))
ax = fig.add_subplot(111, projection='3d')

# 1. Malla del Paraboloide en polares (r, theta)
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

# Dibujar superficies translúcidas
ax.plot_surface(X_parab, Y_parab, Z_parab, color='#3498db', alpha=0.35, 
                edgecolor='none', label='Paraboloide x²+y²+z=1')
ax.plot_surface(X_pl, Y_pl, Z_pl, color='#e67e22', alpha=0.45, 
                edgecolor='none', label='Plano x+y=1')

# Curva de Intersección
ax.plot(x_curva, y_curva, z_curva, color='red', lw=4.5, 
        label=r'Intersección: Parábola $\mathbf{r}(t)$', zorder=10)

# Puntos Notables
ax.scatter([V[0]], [V[1]], [V[2]], color='black', s=100, marker='^', label='Vértice (0.5, 0.5, 0.5)')
ax.scatter([P1[0], P2[0]], [P1[1], P2[1]], [P1[2], P2[2]], color='darkgreen', s=80, marker='o', label='Cortes en z=0')

# Vectores normales en el vértice (0.5, 0.5, 0.5)
# Normal al Paraboloide: (2x, 2y, 1) = (1, 1, 1)
ax.quiver(0.5, 0.5, 0.5, 0.5, 0.5, 0.5, color='blue', lw=2.5, arrow_length_ratio=0.2)
ax.text(1.1, 1.1, 1.1, r'$\nabla F_1$', color='blue', fontsize=11, fontweight='bold')

# Normal al Plano: (1, 1, 0)
ax.quiver(0.5, 0.5, 0.5, 0.5, 0.5, 0.0, color='#d35400', lw=2.5, arrow_length_ratio=0.2)
ax.text(1.1, 1.1, 0.5, r'$\nabla F_2$', color='#d35400', fontsize=11, fontweight='bold')

# Vector tangente horizontal: (-1, 1, 0)
ax.quiver(0.5, 0.5, 0.5, -0.6, 0.6, 0.0, color='red', lw=2.5, arrow_length_ratio=0.2)
ax.text(-0.2, 1.2, 0.5, r'$\mathbf{v}$ (tangente)', color='red', fontsize=11, fontweight='bold')

# Límites y perspectiva
ax.set_xlim(-1.8, 2.0)
ax.set_ylim(-1.8, 2.0)
ax.set_zlim(-2.0, 1.5)
ax.set_xlabel('Eje X', fontweight='bold')
ax.set_ylabel('Eje Y', fontweight='bold')
ax.set_zlabel('Eje Z', fontweight='bold')
ax.set_title(r'Intersección Paraboloide $x^2 + y^2 + z = 1$ y Plano $x + y = 1$', fontsize=13, fontweight='bold', pad=15)
ax.view_init(elev=22, azim=45)

plt.tight_layout()
plt.show()
"""))

# Cell 7: Markdown Plotly
cells.append(nbf.v4.new_markdown_cell(r"""## 3. Visualización 3D Interactiva con Plotly

Gráfico interactivo con rotación 360°, zoom, panel de capas e inspección de coordenadas:
"""))

# Cell 8: Código Plotly 3D
cells.append(nbf.v4.new_code_cell(r"""fig_plotly = go.Figure()

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

# Parábola
fig_plotly.add_trace(go.Scatter3d(
    x=x_curva, y=y_curva, z=z_curva,
    mode='lines',
    line=dict(color='red', width=9),
    name='Parábola de Intersección',
    hoverinfo='name+x+y+z'
))

# Vértice
fig_plotly.add_trace(go.Scatter3d(
    x=[V[0]], y=[V[1]], z=[V[2]],
    mode='markers+text',
    marker=dict(size=9, color='black', symbol='diamond'),
    text=['Vértice (0.5, 0.5, 0.5)'],
    textposition='top center',
    name='Vértice de la parábola'
))

# Cortes z = 0
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

html_path = "interseccion_3d_interactiva.html"
fig_plotly.write_html(html_path)
print(f"✓ Gráfico interactivo guardado: {html_path}")
fig_plotly.show()
"""))

nb.cells = cells

output_path = "/Users/gv/.gemini/antigravity-ide/scratch/sistemas_coordenadas/interseccion_3d.ipynb"
with open(output_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)

print(f"Cuaderno Jupyter generado en: {output_path}")
