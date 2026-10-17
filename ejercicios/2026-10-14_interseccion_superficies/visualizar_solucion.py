import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go

def generar_grafico_matplotlib():
    fig = plt.figure(figsize=(18, 8))
    
    # -------------------------------------------------------------
    # Vista 1: Perspectiva 3D Completa
    # -------------------------------------------------------------
    ax1 = fig.add_subplot(1, 2, 1, projection='3d')
    
    # 1. Paraboloide: x^2 + y^2 + z = 1  =>  z = 1 - (x^2 + y^2)
    r = np.linspace(0, 1.25, 40)
    theta = np.linspace(0, 2*np.pi, 60)
    R, THETA = np.meshgrid(r, theta)
    X_parab = R * np.cos(THETA)
    Y_parab = R * np.sin(THETA)
    Z_parab = 1 - (X_parab**2 + Y_parab**2)
    
    ax1.plot_surface(X_parab, Y_parab, Z_parab, alpha=0.25, cmap='Blues', edgecolor='none')
    
    # 2. Plano secante: x + y = 1  =>  y = 1 - x
    xp = np.linspace(-0.5, 1.5, 20)
    zp = np.linspace(-0.5, 1.2, 20)
    XP, ZP = np.meshgrid(xp, zp)
    YP = 1 - XP
    ax1.plot_surface(XP, YP, ZP, alpha=0.25, color='orange', edgecolor='none')
    
    # 3. Curva de intersección C: r(t) = (t, 1-t, 2t - 2t^2)
    t = np.linspace(-0.25, 1.25, 200)
    xc = t
    yc = 1 - t
    zc = 2*t - 2*t**2
    ax1.plot(xc, yc, zc, color='crimson', linewidth=3.5, label=r'Curva $C = S_1 \cap S_2$')
    
    # 4. Punto P = (1/4, 3/4, 3/8)
    P = np.array([0.25, 0.75, 0.375])
    ax1.scatter([P[0]], [P[1]], [P[2]], color='black', s=90, zorder=10, label=r'Punto $P\left(\frac{1}{4}, \frac{3}{4}, \frac{3}{8}\right)$')
    
    # 5. Recta tangente: r_tan(s) = P + s*(1, -1, 1)
    s = np.linspace(-0.6, 0.6, 100)
    T = np.array([1.0, -1.0, 1.0])
    xtan = P[0] + s * T[0]
    ytan = P[1] + s * T[1]
    ztan = P[2] + s * T[2]
    ax1.plot(xtan, ytan, ztan, color='forestgreen', linewidth=3, linestyle='--', label=r'Recta Tangente $\mathbf{T}=(1,-1,1)$')
    
    # 6. Plano de referencia: x - z = 0  =>  z = x
    x_ref = np.linspace(-0.5, 1.2, 15)
    y_ref = np.linspace(-0.5, 1.5, 15)
    X_ref, Y_ref = np.meshgrid(x_ref, y_ref)
    Z_ref = X_ref
    ax1.plot_surface(X_ref, Y_ref, Z_ref, alpha=0.18, color='purple', edgecolor='none')
    
    ax1.set_title('Perspectiva 3D: Curva $C$, Recta Tangente y Plano $x - z = 0$', fontsize=13, fontweight='bold', pad=15)
    ax1.set_xlabel('$x$')
    ax1.set_ylabel('$y$')
    ax1.set_zlabel('$z$')
    ax1.set_xlim([-0.6, 1.5])
    ax1.set_ylim([-0.5, 1.5])
    ax1.set_zlim([-0.6, 1.2])
    ax1.view_init(elev=24, azim=45)
    ax1.legend(loc='upper right', fontsize=9)
    
    # -------------------------------------------------------------
    # Vista 2: Proyección X-Z (comprueba el paralelismo geométrico)
    # -------------------------------------------------------------
    ax2 = fig.add_subplot(1, 2, 2)
    
    # En el plano x-z, la recta tangente tiene pendiente: dz/dx = T_z / T_x = 1/1 = 1
    # Y la traza del plano x - z = 0 es la recta z = x (pendiente = 1)
    ax2.plot(x_ref, x_ref, color='purple', linewidth=2.5, linestyle='-', label='Plano de referencia: $z = x$ (pendiente = 1)')
    ax2.plot(xtan, ztan, color='forestgreen', linewidth=3, linestyle='--', label='Recta Tangente proyectada (pendiente = 1)')
    ax2.plot(xc, zc, color='crimson', linewidth=2, label='Curva $C$: $z = 2x - 2x^2$')
    ax2.scatter([P[0]], [P[2]], color='black', s=100, zorder=5, label=r'Punto $P\left(x=\frac{1}{4},\; z=\frac{3}{8}\right)$')
    
    # Anotación demostrativa
    ax2.annotate(r'$P\left(\frac{1}{4}, \frac{3}{8}\right)$' + '\n' + r'Recta tangente $\parallel$ a $z = x$', 
                 xy=(P[0], P[2]), xytext=(P[0]+0.15, P[2]+0.2),
                 arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
                 fontsize=11, bbox=dict(boxstyle="round,pad=0.4", fc="lightyellow", ec="goldenrod"))
    
    ax2.set_title('Vista 2D de perfil (Ejes $X$-$Z$):\nDemostración visual del paralelismo con $x - z = 0$', fontsize=13, fontweight='bold', pad=12)
    ax2.set_xlabel('Eje $x$', fontsize=11)
    ax2.set_ylabel('Eje $z$', fontsize=11)
    ax2.grid(True, linestyle=':', alpha=0.7)
    ax2.set_aspect('equal', adjustable='box')
    ax2.set_xlim([-0.2, 1.2])
    ax2.set_ylim([-0.2, 1.0])
    ax2.legend(loc='lower right', fontsize=9.5)
    
    plt.tight_layout()
    output_png = 'ilustracion_3d.png'
    plt.savefig(output_png, dpi=200)
    print(f"Imagen estática guardada en: {output_png}")
    plt.close()

def generar_html_plotly():
    # Paraboloide
    r = np.linspace(0, 1.2, 35)
    theta = np.linspace(0, 2*np.pi, 50)
    R, THETA = np.meshgrid(r, theta)
    X_parab = R * np.cos(THETA)
    Y_parab = R * np.sin(THETA)
    Z_parab = 1 - (X_parab**2 + Y_parab**2)
    
    # Plano secante x + y = 1
    xp = np.linspace(-0.4, 1.4, 20)
    zp = np.linspace(-0.5, 1.1, 20)
    XP, ZP = np.meshgrid(xp, zp)
    YP = 1 - XP
    
    # Curva C
    t = np.linspace(-0.2, 1.2, 150)
    xc = t
    yc = 1 - t
    zc = 2*t - 2*t**2
    
    # Punto P
    P = np.array([0.25, 0.75, 0.375])
    
    # Recta tangente
    s = np.linspace(-0.5, 0.5, 80)
    T = np.array([1.0, -1.0, 1.0])
    xtan = P[0] + s * T[0]
    ytan = P[1] + s * T[1]
    ztan = P[2] + s * T[2]
    
    # Plano x - z = 0
    x_ref = np.linspace(-0.4, 1.2, 15)
    y_ref = np.linspace(-0.3, 1.3, 15)
    X_ref, Y_ref = np.meshgrid(x_ref, y_ref)
    Z_ref = X_ref
    
    fig = go.Figure()
    
    # 1. Paraboloide
    fig.add_trace(go.Surface(
        x=X_parab, y=Y_parab, z=Z_parab,
        colorscale='Blues', opacity=0.35, showscale=False,
        name='Paraboloide: x² + y² + z = 1'
    ))
    
    # 2. Plano x + y = 1
    fig.add_trace(go.Surface(
        x=XP, y=YP, z=ZP,
        colorscale='YlOrRd', opacity=0.35, showscale=False,
        name='Plano: x + y = 1'
    ))
    
    # 3. Plano x - z = 0
    fig.add_trace(go.Surface(
        x=X_ref, y=Y_ref, z=Z_ref,
        colorscale='Purples', opacity=0.3, showscale=False,
        name='Plano ref: x - z = 0'
    ))
    
    # 4. Curva C
    fig.add_trace(go.Scatter3d(
        x=xc, y=yc, z=zc,
        mode='lines',
        line=dict(color='red', width=8),
        name='Curva C (Intersección)'
    ))
    
    # 5. Recta Tangente
    fig.add_trace(go.Scatter3d(
        x=xtan, y=ytan, z=ztan,
        mode='lines',
        line=dict(color='lime', width=7, dash='dash'),
        name='Recta Tangente en P'
    ))
    
    # 6. Punto P
    fig.add_trace(go.Scatter3d(
        x=[P[0]], y=[P[1]], z=[P[2]],
        mode='markers+text',
        marker=dict(size=10, color='black'),
        text=['P(1/4, 3/4, 3/8)'],
        textposition='top center',
        name='Punto P (Solución)'
    ))
    
    fig.update_layout(
        title='<b>Visualización 3D Interactiva: Intersección y Recta Tangente Paralela</b>',
        scene=dict(
            xaxis_title='Eje X',
            yaxis_title='Eje Y',
            zaxis_title='Eje Z',
            aspectmode='data',
            camera=dict(
                eye=dict(x=1.6, y=1.5, z=1.2)
            )
        ),
        legend=dict(x=0.02, y=0.98),
        margin=dict(l=0, r=0, b=0, t=50)
    )
    
    output_html = 'ilustracion_3d_interactiva.html'
    fig.write_html(output_html)
    print(f"Visualización 3D interactiva guardada en: {output_html}")

if __name__ == '__main__':
    generar_grafico_matplotlib()
    generar_html_plotly()
