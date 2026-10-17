# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "matplotlib",
# ]
# ///
"""Producto cuña, determinante, núcleo y autovectores — Clase III

Autor: Gustavo Varela
Sistemas de Coordenadas · Agrimensura · FIUBA · 2026

Plantilla de la serie: cada bloque = pregunta → predecí antes de mirar → animación →
la cuenta a mano → "lo que se ve ↔ lo que dice el álgebra".
"""

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.animation import FuncAnimation
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    return FuncAnimation, Poly3DCollection, mo, np, plt


@app.cell
def _(mo):
    mo.md(r"""
    # Producto cuña, determinante, núcleo y autovectores — Clase III

    **Gustavo Varela** · Sistemas de Coordenadas · Agrimensura · FIUBA · 2026

    Este cuaderno sigue las clases 5, 6 y 7 de los resúmenes de clase del profesor (cursada 2025). La idea que lo hila es una sola, dicha con sus palabras:
    el producto cuña es un **"detector de colinealidad"**. Con ese detector vamos a:

    1. **A.** Medir área orientada en el plano y ver cuándo dos vectores son colineales.
    2. **B.** Medir volumen en el espacio y ver cuándo tres vectores caen en un plano.
    3. **C.** Encontrar el **núcleo** de una transformación: los vectores que van al cero.
    4. **D.** Ver los **subespacios invariantes**: "una dirección que cae sobre sí misma".
    5. **E.** Hallar autovalores y autovectores: construir $A - \lambda I$, "una versión modificada de la transformación que tenga al autovector en el núcleo", y usar el detector sobre sus filas.
    6. **F.** Pasar a $\mathbb{R}^3$: los puntos fijos de una transformación proyectiva del plano **son** los subespacios invariantes de $\mathbb{R}^3$.

    Cada bloque tiene la misma forma: una pregunta, una **escalera** $\mathbb{R} \to \mathbb{R}^2 \to \mathbb{R}^3$ (el caso de una
    coordenada es el que ya sabés; el resto es "lo mismo con más coordenadas"), una predicción antes de mirar, la animación,
    la cuenta a mano con números chicos, y una línea que conecta lo que se ve con lo que dice el álgebra. Ninguna fórmula
    aparece sin su dibujo al lado.

    Convenciones: ángulos en **radianes**, transformación **activa** (se mueven los vectores, los ejes quedan fijos), todo alrededor del origen.
    Las cuentas a mano se verifican con `numpy` al lado (`np.allclose`). Al mover un control la animación se regenera y arranca sola.
    """)
    return


@app.cell
def _(np, plt):
    # ---------- ayudantes compartidos por todos los bloques ----------

    def pmat(M, dec=3):
        """Matriz → LaTeX pmatrix. Imprime enteros sin decimales."""

        def _f(x):
            x = float(x)
            if abs(x - round(x)) < 1e-9:
                return str(int(round(x)))
            return f"{x:.{dec}f}"

        filas = r" \\ ".join(" & ".join(_f(x) for x in fila) for fila in np.atleast_2d(M))
        return r"\begin{pmatrix}" + filas + r"\end{pmatrix}"

    def vec_tex(v):
        """Vector → '(a, b, c)' con enteros sin decimales."""

        def _f(x):
            x = float(x)
            return str(int(round(x))) if abs(x - round(x)) < 1e-9 else f"{x:.3f}"

        return "(" + ",\\ ".join(_f(x) for x in np.asarray(v).ravel()) + ")"

    def anim_html(anim, fig):
        """to_jshtml + script de autoplay (patrón de rotaciones_clase_I). Cierra la figura."""
        html = anim.to_jshtml(default_mode="once") + """<script>
        window.addEventListener("load", function () {
          var b = document.querySelector('button[title="Play"]'); if (b) b.click();
        });</script>"""
        plt.close(fig)
        return html

    def circulo(n=240):
        """Circunferencia unitaria como matriz 2 × n (columnas = puntos)."""
        t = np.linspace(0, 2 * np.pi, n)
        return np.vstack([np.cos(t), np.sin(t)])

    def perp2(fila):
        """En 2D: el vector perpendicular a la fila (a, b) es (b, -a): la cruz (a, b, 0) × (0, 0, 1)."""
        a, b = (float(x) for x in fila)
        return np.array([b, -a])

    def pot_real(A, t):
        """A^t para t real, vía diagonalización A = P D P⁻¹ (autovalores reales positivos)."""
        w, P = np.linalg.eig(A)
        return np.real(P @ np.diag(w.astype(complex) ** t) @ np.linalg.inv(P))

    def rot_y(a):
        c, s = np.cos(a), np.sin(a)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])

    def rot_z(a):
        c, s = np.cos(a), np.sin(a)
        return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])

    return anim_html, circulo, perp2, pmat, pot_real, rot_y, rot_z, vec_tex


@app.cell
def _(mo):
    mo.md(r"""
    ## A. Área orientada: el detector de colinealidad

    **Pregunta.** Tengo dos vectores $u$ y $v$ en el plano. ¿Cómo me doy cuenta de que son paralelos **sin medir ningún ángulo**,
    usando sólo sumas y productos de sus coordenadas?

    **La escalera $\mathbb{R} \to \mathbb{R}^2 \to \mathbb{R}^3$.** Empezamos por lo que ya sabés.

    | | lo que dice el álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}$ | un vector es un número $a$; su "determinante" es $\det[a] = a$ | el "área" de un vector de la recta es su **longitud con signo**: $\lvert a \rvert$ es el largo y el signo dice para qué lado apunta (la orientación). Se aplasta a cero ↔ $a = 0$ |
    | $\mathbb{R}^2$ | $u \wedge v = \det\begin{pmatrix} u_1 & v_1 \\ u_2 & v_2 \end{pmatrix} = u_1 v_2 - u_2 v_1$ | **área orientada** del paralelogramo de $u$ y $v$: positiva si de $u$ a $v$ se gira antihorario, negativa si horario. Se aplasta a cero ↔ $u$ y $v$ colineales |
    | $\mathbb{R}^3$ | $(u \wedge v)\wedge w = \det[u\ v\ w]$ | **volumen orientado** del paralelepípedo (bloque B). Se aplasta a cero ↔ los tres caen en un plano |

    Es lo mismo con más coordenadas: el determinante es siempre "cuánto ocupa, y para qué lado" el bloque que arman los vectores.
    Por eso es un detector de colinealidad: ocupa cero ↔ los vectores son dependientes.
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(r"""
    **Predecí antes de mirar.** $u = (3, 1)$ queda fijo y $v$ (de largo $\sqrt5$) da una vuelta completa desde el eje $x$.

    - ¿En cuántos ángulos el área va a ser exactamente cero? ¿Cuáles?
    - Cuando $v$ está "a la izquierda" de $u$ (antihorario), ¿qué signo esperás?
    - ¿Dónde está el área máxima: cuando $v \perp u$ o cuando $v$ apunta "lo más lejos posible" de $u$?
    """),
        kind="warn",
    )
    return


@app.cell
def _(mo, np):
    theta_a = mo.ui.slider(
        start=0.0, stop=float(2 * np.pi), step=0.01, value=float(2 * np.pi), label="θ final de v (rad)"
    )
    return (theta_a,)


@app.cell
def _(FuncAnimation, anim_html, mo, np, plt, theta_a):
    u_a = np.array([3.0, 1.0])
    th_a = float(theta_a.value)
    _r = np.sqrt(5.0)  # |v| = |(1, 2)|: en θ = atan2(2, 1) ≈ 1.107 rad, v = (1, 2)
    v_a = _r * np.array([np.cos(th_a), np.sin(th_a)])
    det_a = float(np.linalg.det(np.column_stack([u_a, v_a])))

    _N = 60
    _ts = np.linspace(0, th_a, _N) if th_a > 0 else np.array([0.0])
    _phi = np.linspace(0, 2 * np.pi, 400)
    _dets = u_a[0] * _r * np.sin(_phi) - u_a[1] * _r * np.cos(_phi)

    _fig, (_ax, _axd) = plt.subplots(1, 2, figsize=(8.2, 4.0), dpi=90, gridspec_kw={"width_ratios": [1.05, 1]})
    _L = 4.2
    _ax.set_xlim(-_L, _L)
    _ax.set_ylim(-_L, _L)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.plot([-_L * u_a[0], _L * u_a[0]], [-_L * u_a[1], _L * u_a[1]], color="tab:blue", lw=0.6, ls=":", alpha=0.7)
    _ax.annotate("", xy=u_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="tab:blue", lw=2))
    _ax.annotate("u = (3, 1)", u_a, textcoords="offset points", xytext=(5, -12), color="tab:blue")
    _poly = plt.Polygon([[0, 0], u_a, u_a + v_a, v_a], closed=True, fc="tab:green", alpha=0.3, ec="k", lw=0.8)
    _ax.add_patch(_poly)
    _arrow = _ax.annotate("", xy=v_a, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color="tab:red", lw=2))
    _txt = _ax.text(0.02, 0.95, "", transform=_ax.transAxes, fontsize=9)
    _ax.set_title("paralelogramo de u y v(t)", fontsize=10)

    _axd.plot(_phi, _dets, color="tab:purple", lw=1.5)
    _axd.axhline(0, color="gray", lw=0.8)
    _axd.set_xlim(0, 2 * np.pi)
    _axd.set_xlabel("ángulo de v (rad)")
    _axd.set_title("u ∧ v = det[u v] según el ángulo de v", fontsize=10)
    _axd.grid(True, alpha=0.3)
    _axd.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2, 2 * np.pi])
    _axd.set_xticklabels(["0", "π/2", "π", "3π/2", "2π"])
    (_dot,) = _axd.plot([], [], "o", color="black", ms=7)
    _fig.tight_layout()

    def _update(i):
        t = _ts[i]
        v = _r * np.array([np.cos(t), np.sin(t)])
        d = u_a[0] * v[1] - u_a[1] * v[0]
        _arrow.xy = tuple(v)
        _poly.set_xy(np.array([[0, 0], u_a, u_a + v, v]))
        _poly.set_facecolor("tab:green" if d >= 0 else "tab:orange")
        _txt.set_text(f"t = {t:.2f} rad    u ∧ v = {d:+.2f}")
        _dot.set_data([t], [d])
        return _arrow, _poly, _txt, _dot

    _anim = FuncAnimation(_fig, _update, frames=len(_ts), interval=60, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md("**Controles**"),
            theta_a,
            mo.md(
                f"θ = {th_a:.3f} rad = {np.degrees(th_a):.1f}°  \n"
                f"v = ({v_a[0]:.3f}, {v_a[1]:.3f})  \n"
                f"**u ∧ v = det[u v] = {det_a:+.3f}**"
            ),
            mo.md("Verde: área positiva (antihorario de u a v). Naranja: negativa. Llevá θ a 0.32 rad (v ∥ u) y a 3.46 rad (v ∥ −u)."),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="780px", height="480px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return det_a, th_a, u_a, v_a


@app.cell
def _(mo, np):
    _u, _v = np.array([3, 1]), np.array([1, 2])
    _uv = float(np.linalg.det(np.column_stack([_u, _v])))
    _vu = float(np.linalg.det(np.column_stack([_v, _u])))
    _uu = float(np.linalg.det(np.column_stack([_u, 2 * _u])))
    ok_a = bool(np.allclose([_uv, _vu, _uu], [5, -5, 0]))
    mo.md(rf"""
    ### La cuenta a mano

    Con $u = (3, 1)$ y $v = (1, 2)$. Escribimos cada vector en la base $e_1, e_2$ y distribuimos, con dos reglas:
    $e_1 \wedge e_1 = e_2 \wedge e_2 = 0$ (un vector consigo mismo no arma área) y $e_2 \wedge e_1 = -\,e_1 \wedge e_2$ (cambiar el orden cambia el signo).

    $$u \wedge v = (3e_1 + 1e_2) \wedge (1e_1 + 2e_2)
    = 3\cdot 2\; e_1\wedge e_2 \;+\; 1 \cdot 1\; e_2 \wedge e_1
    = (6 - 1)\; e_1 \wedge e_2 = 5\; e_1 \wedge e_2$$

    Es decir $\det\begin{{pmatrix}} 3 & 1 \\ 1 & 2 \end{{pmatrix}} = 3\cdot 2 - 1 \cdot 1 = 5$: área $5$, signo $+$ (de $u$ a $v$ se gira antihorario).

    - Al revés: $v \wedge u = 1\cdot 1 - 2 \cdot 3 = -5$. Misma área, signo opuesto.
    - Colineales: $u \wedge 2u = 3 \cdot 2 - 1 \cdot 6 = 0$. El detector se dispara.

    `numpy`: $\det[u\ v] = {_uv:.0f}$, $\det[v\ u] = {_vu:.0f}$, $\det[u\ 2u] = {_uu:.0f}$ · `np.allclose` con la cuenta → **{ok_a}**

    **Lo que se ve ↔ lo que dice el álgebra.** El área verde o naranja del paralelogramo ↔ $\lvert u \wedge v \rvert = \lvert \det[u\ v] \rvert$, el área orientada;
    el paralelogramo se aplasta a un segmento ↔ $u \wedge v = 0$, el detector de colinealidad se dispara;
    $v$ cruza al otro lado de la recta de $u$ ↔ el determinante cambia de signo (como en $\mathbb{{R}}$: el número $a$ cambia de signo al pasar por $0$).
    """)
    return (ok_a,)


@app.cell
def _(mo):
    mo.md(r"""
    ## B. Volumen y colinealidad en tres dimensiones

    **Pregunta.** Con tres vectores $u, v, w$ en el espacio, ¿qué es lo que "se aplasta" y qué número lo detecta?

    Es el escalón $\mathbb{R}^3$ de la escalera del bloque A, lo mismo con una coordenada más: $u, v, w$ arman un paralelepípedo
    y el determinante mide su **volumen orientado**. Si $w$ cae en el plano de $u$ y $v$, la caja se vuelve una lámina, el volumen
    es cero y los tres vectores ya no son independientes. El detector es el mismo, un piso más arriba:
    $(u \wedge v) \wedge w = \det[u\ v\ w]\; e_1 \wedge e_2 \wedge e_3$ ↔ "cuánto ocupa la caja, y de qué lado del plano de $u, v$ está $w$".
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(r"""
    **Predecí antes de mirar.** $u = (1, 2, 0)$ y $v = (0, 1, 1)$ quedan fijos. $w$ viaja en línea recta desde $w_0 = (1, 0, 2)$
    hasta $w_1 = u + v = (1, 3, 1)$ según $w(s) = (1 - s)\,w_0 + s\,w_1$.

    - ¿Para qué valor de $s$ el volumen es cero? ¿Por qué $u + v$ está en el plano de $u$ y $v$?
    - Si seguís más allá ($s > 1$), ¿el volumen vuelve a crecer? ¿Con qué signo?
    """),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    s_b = mo.ui.slider(start=0.0, stop=1.5, step=0.01, value=1.0, label="s final (posición de w)")
    return (s_b,)


@app.cell
def _(FuncAnimation, Poly3DCollection, anim_html, mo, np, plt, s_b):
    u_b = np.array([1.0, 2.0, 0.0])
    v_b = np.array([0.0, 1.0, 1.0])
    w0_b = np.array([1.0, 0.0, 2.0])
    w1_b = u_b + v_b  # (1, 3, 1): está en el plano de u y v
    s_val_b = float(s_b.value)

    def _w_de(s):
        return (1 - s) * w0_b + s * w1_b

    def _det_de(s):
        return float(np.linalg.det(np.column_stack([u_b, v_b, _w_de(s)])))

    w_b = _w_de(s_val_b)
    det_b = _det_de(s_val_b)
    cruz_b = np.cross(u_b, v_b)  # coeficientes de u ∧ v reordenados: (bf−ce, −(af−cd), ae−bd)

    _N = 50
    _ss = np.linspace(0, s_val_b, _N) if s_val_b > 0 else np.array([0.0])
    _sgrid = np.linspace(0, 1.5, 200)
    _dgrid = [_det_de(s) for s in _sgrid]

    _fig = plt.figure(figsize=(8.4, 4.2), dpi=90)
    _ax = _fig.add_subplot(1, 2, 1, projection="3d")
    _axd = _fig.add_subplot(1, 2, 2)

    def _vertices(w):
        return np.array([np.zeros(3), u_b, u_b + v_b, v_b, w, u_b + w, u_b + v_b + w, v_b + w])

    _caras = [[0, 1, 2, 3], [4, 5, 6, 7], [0, 1, 5, 4], [3, 2, 6, 7], [0, 3, 7, 4], [1, 2, 6, 5]]
    _V0 = _vertices(w0_b)
    _poly = Poly3DCollection([_V0[c] for c in _caras], facecolors="tab:green", edgecolors="k", linewidths=0.6, alpha=0.25)
    _ax.add_collection3d(_poly)
    _L = 3.4
    for _p, _c, _n in ((u_b, "tab:blue", "u"), (v_b, "tab:orange", "v")):
        _ax.plot([0, _p[0]], [0, _p[1]], [0, _p[2]], color=_c, lw=2.2)
        _ax.text(*_p, _n, color=_c)
    (_wl,) = _ax.plot([0, w0_b[0]], [0, w0_b[1]], [0, w0_b[2]], color="tab:red", lw=2.2)
    _wt = _ax.text(*w0_b, "w", color="tab:red")
    # plano de u y v (para ver adónde va w)
    _a, _bb = np.meshgrid(np.linspace(-0.3, 1.3, 2), np.linspace(-0.3, 1.3, 2))
    _plano = _a[..., None] * u_b + _bb[..., None] * v_b
    _ax.plot_surface(_plano[..., 0], _plano[..., 1], _plano[..., 2], color="gray", alpha=0.12, linewidth=0)
    _ax.set_xlim(-0.5, _L)
    _ax.set_ylim(-0.5, _L)
    _ax.set_zlim(-0.5, _L)
    _ax.set_box_aspect((1, 1, 1))
    _ax.set_xlabel("x")
    _ax.set_ylabel("y")
    _ax.set_zlabel("z")
    _ax.view_init(elev=20, azim=-55)
    _tit = _ax.set_title("", fontsize=10)

    _axd.plot(_sgrid, _dgrid, color="tab:purple", lw=1.5)
    _axd.axhline(0, color="gray", lw=0.8)
    _axd.axvline(1, color="gray", lw=0.8, ls=":")
    _axd.set_xlim(0, 1.5)
    _axd.set_xlabel("s")
    _axd.set_title("det[u v w(s)] = volumen orientado", fontsize=10)
    _axd.grid(True, alpha=0.3)
    (_dot,) = _axd.plot([], [], "o", color="black", ms=7)
    _fig.tight_layout()

    def _update(i):
        s = _ss[i]
        w = _w_de(s)
        d = _det_de(s)
        V = _vertices(w)
        _poly.set_verts([V[c] for c in _caras])
        _poly.set_facecolor("tab:green" if d >= 0 else "tab:orange")
        _wl.set_data_3d([0, w[0]], [0, w[1]], [0, w[2]])
        _wt.set_position_3d(w)
        _tit.set_text(f"s = {s:.2f}   w = ({w[0]:.2f}, {w[1]:.2f}, {w[2]:.2f})   det = {d:+.2f}")
        _dot.set_data([s], [d])
        return _poly, _wl, _wt, _tit, _dot

    _anim = FuncAnimation(_fig, _update, frames=len(_ss), interval=70, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md("**Controles**"),
            s_b,
            mo.md(
                f"s = {s_val_b:.2f}  \n"
                f"w(s) = ({w_b[0]:.2f}, {w_b[1]:.2f}, {w_b[2]:.2f})  \n"
                f"**det[u v w] = {det_b:+.3f}**  \n"
                f"u × v = ({cruz_b[0]:.0f}, {cruz_b[1]:.0f}, {cruz_b[2]:.0f}),  (u × v)·w = {float(cruz_b @ w_b):+.3f}"
            ),
            mo.md("El plano gris es el de u y v. En s = 1 la caja queda plana; pasado s = 1, w cruza el plano y el signo cambia."),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="800px", height="500px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return cruz_b, det_b, s_val_b, u_b, v_b, w0_b, w1_b, w_b


@app.cell
def _(mo, np, u_b, v_b, w0_b, w1_b):
    _det0 = float(np.linalg.det(np.column_stack([u_b, v_b, w0_b])))
    _det1 = float(np.linalg.det(np.column_stack([u_b, v_b, w1_b])))
    _cruz = np.cross(u_b, v_b)
    ok_b = bool(np.allclose([_det0, _det1], [4, 0]) and np.allclose(_cruz, [2, -1, 1]) and np.isclose(_cruz @ w0_b, 4))
    mo.md(rf"""
    ### La cuenta a mano

    Primero el producto cuña de dos vectores genéricos de $\mathbb{{R}}^3$. Distribuimos y usamos las mismas dos reglas
    ($e_i \wedge e_i = 0$, $e_j \wedge e_i = -\,e_i \wedge e_j$); quedan tres "áreas", una por cada plano coordenado:

    $$(a e_1 + b e_2 + c e_3)\wedge(d e_1 + e e_2 + f e_3)
    = (ae - bd)\; e_1\wedge e_2 \;+\; (af - cd)\; e_1 \wedge e_3 \;+\; (bf - ce)\; e_2 \wedge e_3 .$$

    Con $u = (1, 2, 0)$ y $v = (0, 1, 1)$: $a{{=}}1, b{{=}}2, c{{=}}0, d{{=}}0, e{{=}}1, f{{=}}1$, así que
    $ae - bd = 1$, $af - cd = 1$, $bf - ce = 2$:

    $$u \wedge v = 1\; e_1\wedge e_2 + 1\; e_1\wedge e_3 + 2\; e_2 \wedge e_3 .$$

    Ahora le pegamos $w = (1, 0, 2) = 1e_1 + 0e_2 + 2e_3$ a cada término. Sólo sobrevive el versor que **falta** en cada par
    (los otros repiten un $e_i$ y dan cero), y hay que ordenar a $e_1\wedge e_2\wedge e_3$ contando los cambios de signo:

    $$\begin{{aligned}}
    e_1\wedge e_2 \wedge w &= 2\; e_1\wedge e_2\wedge e_3 \\
    e_1\wedge e_3 \wedge w &= 0\; e_1\wedge e_3\wedge e_2 = 0 \cdot (-\,e_1\wedge e_2\wedge e_3) = 0 \\
    2\; e_2\wedge e_3 \wedge w &= 2\cdot 1\; e_2\wedge e_3\wedge e_1 = 2\; e_1\wedge e_2\wedge e_3 \quad (\text{{dos intercambios: signo }} +)
    \end{{aligned}}$$

    $$(u \wedge v)\wedge w = (2 + 0 + 2)\; e_1\wedge e_2\wedge e_3 = 4\; e_1\wedge e_2\wedge e_3 \quad\Longrightarrow\quad \det[u\ v\ w] = 4 .$$

    En general $(u \wedge v)\wedge w = \big[(ae - bd)\,w_3 - (af - cd)\,w_2 + (bf - ce)\,w_1\big]\; e_1\wedge e_2\wedge e_3$:
    los tres coeficientes de $u \wedge v$ son las componentes del producto cruz $u \times v = (bf - ce,\ -(af - cd),\ ae - bd) = (2, -1, 1)$,
    y el corchete es $(u \times v)\cdot w = 2 \cdot 1 - 1 \cdot 0 + 1 \cdot 2 = 4$.

    Con $w_1 = u + v = (1, 3, 1)$: $(u \times v)\cdot w_1 = 2 - 3 + 1 = 0$. Detector disparado: $w_1$ está en el plano de $u$ y $v$.

    `numpy`: $\det[u\ v\ w_0] = {_det0:.0f}$, $\det[u\ v\ w_1] = {_det1:.0f}$, $u \times v = ({_cruz[0]:.0f}, {_cruz[1]:.0f}, {_cruz[2]:.0f})$ · `np.allclose` con la cuenta → **{ok_b}**

    **Lo que se ve ↔ lo que dice el álgebra.** La caja se aplasta hasta ser una lámina en el plano gris ↔ $(u\wedge v)\wedge w = 0$;
    $w$ atraviesa el plano ↔ el volumen orientado cambia de signo.
    """)
    return (ok_b,)


@app.cell
def _(mo):
    mo.md(r"""
    ## C. Núcleo: los vectores que van al cero

    **Pregunta.** En una transformación lineal el cero siempre va al cero. ¿Puede haber **otros** vectores que también vayan al cero?
    Y si los hay, ¿qué le pasa al resto del plano?

    El conjunto de vectores que van al cero es el **núcleo**: lo que la transformación **aplasta al cero**.

    **La escalera $\mathbb{R} \to \mathbb{R}^2 \to \mathbb{R}^3$.**

    | | lo que dice el álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}$ | $a \cdot x = 0$: si $a \neq 0$ la única solución es $x = 0$; si $a = 0$, **todo** $x$ va al cero | la recta se estira o se encoge ($a \neq 0$: núcleo $= \{0\}$), o se aplasta entera al punto $0$ ($a = 0$: núcleo $=$ toda la recta). No hay término medio |
    | $\mathbb{R}^2$ | $A v = 0$: el núcleo puede ser $\{0\}$, una **recta**, o todo el plano | el plano queda plano ($\det A \neq 0$), o se **aplasta sobre una recta** ($\det A = 0$: una dirección entera va al cero), o al punto $0$ ($A = 0$) |
    | $\mathbb{R}^3$ | lo mismo con una coordenada más: $\{0\}$, recta, plano o todo | el espacio se aplasta sobre un plano, sobre una recta o al origen |

    **Identidad e inversa, en la misma escalera.** En $\mathbb{R}$, $1$ es el número que no cambia nada y $1/a$ deshace lo que hizo $a$:
    no existe si $a = 0$, porque una recta aplastada a un punto no se puede "desaplastar". En $\mathbb{R}^2$, $I$ es la matriz que no cambia nada
    y $A^{-1}$ deshace $A$: **no existe si $\det A = 0$**, por la misma razón — una vez que el plano cayó sobre una recta, no hay forma de saber
    de dónde vino cada punto. $1/a$ no existe si $a = 0$ ↔ $A^{-1}$ no existe si $\det A = 0$.

    Si el núcleo tiene algo más que el $\vec 0$, la transformación "pierde" una dimensión. El detector lo anuncia antes de dibujar nada:
    las filas de la matriz son colineales, $\det A = 0$.
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(r"""
    **Predecí antes de mirar.** $A = \begin{pmatrix} 1 & 2 \\ 2 & 4 \end{pmatrix}$. Vamos a ir de la identidad a $A$ con
    $A_t = (1 - t)\,I + t\,A$.

    - Mirá las filas: ¿qué te dice el detector de colinealidad sobre $\det A$?
    - ¿Sobre qué recta va a caer todo el plano cuando $t = 1$? (pista: las **columnas**)
    - ¿Qué dirección va a ir al cero? (pista: tiene que ser perpendicular a la **fila** $(1, 2)$, porque $A v = 0$ significa que cada fila "por" $v$ da $0$)
    """),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    t_c = mo.ui.slider(start=0.0, stop=1.0, step=0.01, value=1.0, label="t final (0 = identidad, 1 = A)")
    return (t_c,)


@app.cell
def _(FuncAnimation, anim_html, mo, np, perp2, plt, pmat, t_c):
    A_c = np.array([[1.0, 2.0], [2.0, 4.0]])
    ker_c = perp2(A_c[0])  # (2, -1): perpendicular a la fila (1, 2)
    t_val_c = float(t_c.value)

    def _At(t):
        return (1 - t) * np.eye(2) + t * A_c

    A_t_c = _At(t_val_c)
    det_c = float(np.linalg.det(A_t_c))

    _g = np.linspace(-0.8, 0.8, 9)
    _X, _Y = np.meshgrid(_g, _g)
    _P = np.vstack([_X.ravel(), _Y.ravel()])  # 2 × 81
    _kdir = ker_c / np.linalg.norm(ker_c)
    _K = np.outer(_kdir, np.linspace(-2.6, 2.6, 11))  # puntos sobre la recta del núcleo
    _idir = A_c[:, 0] / np.linalg.norm(A_c[:, 0])  # dirección de la imagen: columna (1, 2)
    _N = 45
    _ts = np.linspace(0, t_val_c, _N) if t_val_c > 0 else np.array([0.0])

    _fig, _ax = plt.subplots(figsize=(4.4, 6.2), dpi=90)
    _ax.set_xlim(-3, 3)
    _ax.set_ylim(-5.2, 5.2)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.plot([-6 * _kdir[0], 6 * _kdir[0]], [-6 * _kdir[1], 6 * _kdir[1]], ls="--", color="tab:red", lw=1, label="núcleo: dirección (2, −1)")
    _ax.plot([-6 * _idir[0], 6 * _idir[0]], [-6 * _idir[1], 6 * _idir[1]], ls="--", color="tab:green", lw=1, label="imagen: dirección (1, 2)")
    _ax.scatter(_P[0], _P[1], s=6, color="tab:blue", alpha=0.25)
    _sc = _ax.scatter(_P[0], _P[1], s=9, color="tab:blue", label="grilla")
    _sk = _ax.scatter(_K[0], _K[1], s=28, color="tab:red", zorder=5, label="puntos del núcleo")
    _ax.legend(loc="upper left", fontsize=7)
    _tit = _ax.set_title("", fontsize=10)
    _fig.tight_layout()

    def _update(i):
        t = _ts[i]
        M = _At(t)
        _sc.set_offsets((M @ _P).T)
        _sk.set_offsets((M @ _K).T)
        _tit.set_text(f"A_t = (1−t) I + t A,   t = {t:.2f},   det A_t = {np.linalg.det(M):+.2f}")
        return _sc, _sk, _tit

    _anim = FuncAnimation(_fig, _update, frames=len(_ts), interval=60, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md("**Controles**"),
            t_c,
            mo.md(rf"$A_t = {pmat(A_t_c)}$, $\det A_t = {det_c:.3f}$"),
            mo.md(
                f"A·(2, −1) = ({(A_c @ ker_c)[0]:.0f}, {(A_c @ ker_c)[1]:.0f})  \n"
                "Los puntos rojos (sobre la recta del núcleo) se juntan todos en el origen; los azules se aplastan sobre la recta verde."
            ),
            mo.md(
                r"**La transformación $A_t = (1 - t)\,I + t\,A$ ↔** cada punto $p$ se desliza en línea recta desde $p$ ($t = 0$) hasta $A p$ ($t = 1$). "
                r"$\det A_t = (1 - t)(1 + 4t)$ ↔ el área de cada cuadradito de la grilla, que baja de $1$ a $0$."
            ),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="440px", height="640px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return A_c, A_t_c, det_c, ker_c, t_val_c


@app.cell
def _(A_c, ker_c, mo, np):
    _Av = A_c @ ker_c
    _cruz3 = np.cross([1, 2, 0], [0, 0, 1])
    ok_c = bool(
        np.isclose(np.linalg.det(A_c), 0)
        and np.allclose(_Av, 0)
        and np.allclose(_cruz3, [2, -1, 0])
        and np.allclose(ker_c, [2, -1])
    )
    mo.md(rf"""
    ### La cuenta a mano

    **1. El detector sobre las filas.** Filas $(1, 2)$ y $(2, 4)$: $\det A = 1 \cdot 4 - 2 \cdot 2 = 0$. Las filas son colineales
    (la segunda es el doble de la primera), así que $A$ tiene núcleo no trivial.

    **2. El núcleo con el producto cruz.** $A v = 0$ pide que **cada fila** multiplicada por $v$ dé cero: $1\cdot v_1 + 2 \cdot v_2 = 0$
    (la segunda fila pide lo mismo, es la misma ecuación). Buscamos entonces $v$ perpendicular a la fila $(1, 2)$. En el plano, "la cruz de la fila"
    es el producto cruz con $e_3$ (la fila metida en $\mathbb{{R}}^3$ con tercera coordenada $0$):

    $$(1, 2, 0) \times (0, 0, 1) = (2\cdot 1 - 0 \cdot 0,\ \ 0\cdot 0 - 1\cdot 1,\ \ 1 \cdot 0 - 2 \cdot 0) = (2, -1, 0)
    \quad\Longrightarrow\quad v = (2, -1).$$

    Regla corta para 2D: la perpendicular a $(a, b)$ es $(b, -a)$.

    **3. Comprobación.** $A v = \begin{{pmatrix}} 1 & 2 \\ 2 & 4 \end{{pmatrix}} \begin{{pmatrix}} 2 \\ -1 \end{{pmatrix}}
    = \begin{{pmatrix}} 2 - 2 \\ 4 - 4 \end{{pmatrix}} = \begin{{pmatrix}} 0 \\ 0 \end{{pmatrix}}$. Y todo el plano va a parar a la recta de la columna $(1, 2)$:
    $A(x, y) = x(1, 2) + y(2, 4) = (x + 2y)\,(1, 2)$.

    `numpy`: $\det A = {np.linalg.det(A_c):.1f}$, $A\,(2, -1) = ({_Av[0]:.0f}, {_Av[1]:.0f})$, cruz $= ({_cruz3[0]}, {_cruz3[1]}, {_cruz3[2]})$ · `np.allclose` → **{ok_c}**

    **Lo que se ve ↔ lo que dice el álgebra.** Los puntos rojos se juntan en el origen ↔ $(2, -1)$ está en el núcleo, es lo que se aplasta al cero;
    el plano entero se aplasta sobre la recta verde ↔ $\det A = 0$, las filas son colineales;
    no se puede volver atrás desde la recta verde ↔ $A^{-1}$ no existe (como $1/0$).
    """)
    return (ok_c,)


@app.cell
def _(mo):
    mo.md(r"""
    ## D. Autovectores: las direcciones que no giran

    **Pregunta.** El núcleo es un subespacio que la transformación manda al cero. ¿Hay subespacios que la transformación mande
    **sobre sí mismos**? Es decir, en palabras del profesor, "una dirección que cae sobre sí misma": la recta por el origen
    en la dirección $v$ va a parar a la misma recta, aunque $v$ se estire o se acorte.

    Si eso pasa, $A v = \lambda v$: $v$ es un **autovector** (la dirección que cae sobre sí misma) y $\lambda$ es su **autovalor**
    (el factor de estiramiento en esa dirección; si $\lambda < 0$ la dirección se da vuelta).

    **La escalera $\mathbb{R} \to \mathbb{R}^2 \to \mathbb{R}^3$.**

    | | lo que dice el álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}$ | toda matriz es un número $a$, y $a \cdot x = \lambda x$ se cumple para **todo** $x$ con $\lambda = a$ | en $\mathbb{R}$ **todo vector es autovector**: la recta entera cae sobre sí misma, estirada por el factor $a$; el único autovalor es $a$ |
    | $\mathbb{R}^2$ | $A v = \lambda v$ sólo para **algunas** direcciones $v$ | sólo algunas rectas por el origen caen sobre sí mismas (a lo sumo dos distintas, o ninguna real si la transformación gira todo); $\lambda$ es cuánto se estira cada una |
    | $\mathbb{R}^3$ | lo mismo con una coordenada más: hasta tres direcciones | rectas por el origen que caen sobre sí mismas; en coordenadas homogéneas, los puntos fijos del plano (bloque F) |

    Abajo, sobre la circunferencia unitaria, cada segmento gris une $v$ con $A v$. Donde $A v$ es paralelo a $v$ el segmento
    queda **sobre la recta de $v$**: esas son las direcciones que no giran.
    """)
    return


@app.cell
def _(mo):
    mat_d = mo.ui.dropdown(
        options={"A = [[2, 1], [1, 2]] (simétrica)": "sim", "B = [[3, 1], [0, 2]] (no simétrica)": "nosim"},
        value="A = [[2, 1], [1, 2]] (simétrica)",
        label="Matriz",
    )
    return (mat_d,)


@app.cell
def _(mat_d, mo):
    mo.callout(
        mo.vstack(
            [
                mo.md(r"""
    **Predecí antes de mirar.** Elegí una matriz.

    - ¿Cuántas direcciones no giran? ¿Puede una transformación del plano tener más de dos?
    - ¿Van a estar a $90°$ entre sí? ¿En los dos casos?
    - Si aplicás $A$ muchas veces a un vector cualquiera, ¿hacia qué dirección se va a ir acercando?
    """),
                mat_d,
            ],
            gap=0.4,
        ),
        kind="warn",
    )
    return


@app.cell
def _(mat_d, np):
    if mat_d.value == "sim":
        A_d = np.array([[2.0, 1.0], [1.0, 2.0]])
        nombre_d = "A"
        # autovectores "lindos" (enteros) y sus autovalores, para la cuenta a mano
        propios_d = [(3.0, np.array([1.0, 1.0])), (1.0, np.array([1.0, -1.0]))]
    else:
        A_d = np.array([[3.0, 1.0], [0.0, 2.0]])
        nombre_d = "B"
        propios_d = [(3.0, np.array([1.0, 0.0])), (2.0, np.array([1.0, -1.0]))]
    lam_dom_d, v_dom_d = propios_d[0]
    return A_d, lam_dom_d, nombre_d, propios_d, v_dom_d


@app.cell
def _(A_d, mo, nombre_d, np, plt, pmat, propios_d):
    _ang = np.linspace(0, 2 * np.pi, 24, endpoint=False)
    _V = np.vstack([np.cos(_ang), np.sin(_ang)])
    _AV = A_d @ _V

    _fig, _ax = plt.subplots(figsize=(5.4, 5.4), dpi=90)
    _L = 3.6
    _ax.set_xlim(-_L, _L)
    _ax.set_ylim(-_L, _L)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _t = np.linspace(0, 2 * np.pi, 300)
    _ax.plot(np.cos(_t), np.sin(_t), color="gray", lw=1)
    _E = A_d @ np.vstack([np.cos(_t), np.sin(_t)])
    _ax.plot(_E[0], _E[1], color="tab:blue", lw=1.2, alpha=0.7, label=f"{nombre_d}·(circunferencia)")
    for _k in range(_V.shape[1]):
        _ax.annotate("", xy=_AV[:, _k], xytext=_V[:, _k], arrowprops=dict(arrowstyle="->", color="gray", lw=0.9, alpha=0.8))
    _cols = ["tab:red", "tab:green"]
    for (_lam, _v), _c in zip(propios_d, _cols):
        _d = _v / np.linalg.norm(_v)
        _ax.plot([-_L * _d[0], _L * _d[0]], [-_L * _d[1], _L * _d[1]], ls="--", color=_c, lw=1.2, label=f"λ = {_lam:.0f}: dirección ({_v[0]:.0f}, {_v[1]:.0f})")
        _ax.annotate("", xy=_lam * _d, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=_c, lw=2.5))
        _ax.annotate("", xy=_d, xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=_c, lw=1.2, alpha=0.6))
    _ax.legend(loc="upper left", fontsize=8)
    _ax.set_title(f"v ↦ {nombre_d} v sobre la circunferencia unitaria", fontsize=10)

    _angulo = float(np.arccos(abs(propios_d[0][1] @ propios_d[1][1]) / (np.linalg.norm(propios_d[0][1]) * np.linalg.norm(propios_d[1][1]))))
    _controles = mo.vstack(
        [
            mo.md(rf"${nombre_d} = {pmat(A_d)}$"),
            mo.md(
                "Segmentos grises: de $v$ a $" + nombre_d + " v$. Flecha gruesa: el autovector estirado $\\lambda v$.  \n"
                f"Ángulo entre las dos direcciones fijas: {_angulo:.4f} rad = {np.degrees(_angulo):.1f}°  \n"
                f"{'Simétrica: las direcciones fijas son perpendiculares.' if nombre_d == 'A' else 'No simétrica: las direcciones fijas NO son perpendiculares.'}"
            ),
        ],
        gap=0.6,
    )
    mo.hstack([_controles, _fig], justify="start", align="start", gap=2, wrap=True)
    return


@app.cell
def _(mo):
    mo.md(r"""
    **¿Y si aplico la transformación muchas veces?** Con $A = P D P^{-1}$ (la descomposición del profesor ↔ ir a la base de
    autovectores, estirar cada eje por su $\lambda$, volver) se puede definir $A^t = P D^t P^{-1}$ para $t$ **real**.
    **La transformación $A^t$ ↔** el mismo estiramiento hecho de a poco: $A^{1/2}$ es "la mitad del camino" (aplicada dos veces da $A$),
    $A^2$ es aplicarla dos veces. En la animación la circunferencia se deforma en una elipse cada vez más alargada, y cualquier punto
    termina "pegado" a la dirección del autovalor más grande, porque $\lambda_1^t$ le gana a $\lambda_2^t$.
    """)
    return


@app.cell
def _(FuncAnimation, A_d, anim_html, circulo, lam_dom_d, mo, nombre_d, np, plt, pot_real, propios_d, v_dom_d):
    _T = 1.5
    _N = 50
    _ts = np.linspace(0, _T, _N)
    _C = circulo()
    _v0s = [np.array([0.0, 1.0]), np.array([-1.0, 0.5])]
    _cols0 = ["tab:red", "tab:green"]
    _L = float(lam_dom_d**_T) * 1.15
    _e = v_dom_d / np.linalg.norm(v_dom_d)

    def _ang_a_dom(p):
        return float(np.arccos(np.clip(abs(p @ _e) / np.linalg.norm(p), 0, 1)))

    _trays = [np.array([pot_real(A_d, t) @ v0 for t in _ts]) for v0 in _v0s]
    _angs = [np.array([_ang_a_dom(p) for p in tr]) for tr in _trays]

    _fig, (_ax, _axa) = plt.subplots(1, 2, figsize=(8.4, 4.2), dpi=90, gridspec_kw={"width_ratios": [1.1, 1]})
    _ax.set_xlim(-_L, _L)
    _ax.set_ylim(-_L, _L)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.plot(_C[0], _C[1], color="gray", lw=1)
    for _lam, _v in propios_d:
        _d = _v / np.linalg.norm(_v)
        _ax.plot([-2 * _L * _d[0], 2 * _L * _d[0]], [-2 * _L * _d[1], 2 * _L * _d[1]], ls="--", color="tab:purple", lw=1, alpha=0.7)
    (_el,) = _ax.plot(_C[0], _C[1], color="tab:blue", lw=1.4, label=f"{nombre_d}^t (circunferencia)")
    _lines, _dots = [], []
    for _tr, _c, _v0 in zip(_trays, _cols0, _v0s):
        (_ln,) = _ax.plot([], [], "-", color=_c, lw=1.2, label=f"{nombre_d}^t v₀, v₀ = ({_v0[0]:.0f}, {_v0[1]:.1f})")
        (_dt,) = _ax.plot([], [], "o", color=_c, ms=6)
        _lines.append(_ln)
        _dots.append(_dt)
    _ax.legend(loc="upper left", fontsize=7)
    _tit = _ax.set_title("", fontsize=10)

    for _an, _c in zip(_angs, _cols0):
        _axa.plot(_ts, _an, color=_c, lw=1.4)
    _adots = [_axa.plot([], [], "o", color=_c, ms=6)[0] for _c in _cols0]
    _axa.axhline(0, color="gray", lw=0.8)
    _axa.set_xlim(0, _T)
    _axa.set_ylim(-0.05, np.pi / 2 + 0.05)
    _axa.set_xlabel("t")
    _axa.set_ylabel("ángulo (rad)")
    _axa.set_title(f"ángulo entre {nombre_d}^t v₀ y la dirección de λ = {lam_dom_d:.0f}", fontsize=9)
    _axa.grid(True, alpha=0.3)
    _fig.tight_layout()

    def _update(i):
        t = _ts[i]
        M = pot_real(A_d, t)
        E = M @ _C
        _el.set_data(E[0], E[1])
        for ln, dt, tr, ad, an in zip(_lines, _dots, _trays, _adots, _angs):
            ln.set_data(tr[: i + 1, 0], tr[: i + 1, 1])
            dt.set_data([tr[i, 0]], [tr[i, 1]])
            ad.set_data([t], [an[i]])
        _tit.set_text(f"{nombre_d}^t,  t = {t:.2f}")
        return [_el, _tit, *_lines, *_dots, *_adots]

    _anim = FuncAnimation(_fig, _update, frames=_N, interval=70, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md("**Trayectorias** $" + nombre_d + "^t v_0$, $t: 0 \\to 1.5$"),
            mo.md(
                f"Dirección dominante: λ = {lam_dom_d:.0f}, ({v_dom_d[0]:.0f}, {v_dom_d[1]:.0f}).  \n"
                f"Ángulo final de cada trayectoria a esa dirección: {_angs[0][-1]:.3f} rad y {_angs[1][-1]:.3f} rad.  \n"
                "Las rectas violetas punteadas son las direcciones fijas: la elipse se alarga a lo largo de la dominante."
            ),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="800px", height="500px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell
def _(A_d, mo, nombre_d, np, pmat, propios_d, vec_tex):
    _lineas = []
    _ok = True
    for _lam, _v in propios_d:
        _Av = A_d @ _v
        _ok = _ok and bool(np.allclose(_Av, _lam * _v))
        _cuenta = " \\\\ ".join(
            f"{A_d[i, 0]:.0f}\\cdot({_v[0]:.0f}) + {A_d[i, 1]:.0f}\\cdot({_v[1]:.0f})" for i in range(2)
        )
        _lineas.append(
            rf"$${nombre_d}\,{vec_tex(_v)}^T = {pmat(A_d)}{pmat(_v.reshape(2, 1))} = \begin{{pmatrix}} {_cuenta} \end{{pmatrix}} = {pmat(_Av.reshape(2, 1))} = {_lam:.0f}\,{pmat(_v.reshape(2, 1))}$$"
        )
    ok_d = _ok
    _w = np.sort(np.linalg.eigvals(A_d))[::-1].real
    mo.md(
        rf"""
    ### La cuenta a mano

    Verificar que una dirección no gira es multiplicar y mirar si sale un múltiplo del mismo vector. Para ${nombre_d} = {pmat(A_d)}$:

    {chr(10).join(_lineas)}

    En la primera, el vector sale multiplicado por ${propios_d[0][0]:.0f}$; en la segunda, por ${propios_d[1][0]:.0f}$. Son los dos autovalores.
    Cómo **encontrarlos** sin adivinar es el bloque E.

    `numpy`: `np.linalg.eigvals` → $({_w[0]:.0f}, {_w[1]:.0f})$ · `np.allclose(A v, λ v)` para los dos → **{ok_d}**

    **Lo que se ve ↔ lo que dice el álgebra.** El segmento gris queda sobre la recta de $v$ ↔ $A v = \lambda v$, $v$ es una dirección que cae sobre sí misma (subespacio invariante);
    la flecha gruesa mide {propios_d[0][0]:.0f} veces la fina ↔ $\lambda = {propios_d[0][0]:.0f}$ es el factor de estiramiento en esa dirección;
    la elipse se alarga y las trayectorias se pegan a una recta ↔ $\lambda_1^t$ le gana a $\lambda_2^t$.
    """
    )
    return (ok_d,)


@app.cell
def _(mo):
    mo.md(r"""
    ## E. Encontrar los autovalores: $A - \lambda I$ y el detector

    **Pregunta.** En el bloque D "vimos" las direcciones fijas. ¿Cómo las calculamos sin mirar el dibujo?

    La idea del profesor, paso a paso:

    1. Si $A v = \lambda v$, entonces $A v - \lambda I v = 0$, o sea $(A - \lambda I)\, v = 0$.
    2. Eso es **construir una versión modificada de la transformación que tenga al autovector en el núcleo**: $A - \lambda I$.
    3. Para que $A - \lambda I$ tenga núcleo no trivial, sus filas tienen que ser colineales: el detector, $\det(A - \lambda I) = 0$.
       Eso es un polinomio en $\lambda$ (el **polinomio característico**) y sus raíces son los autovalores.
    4. Con cada $\lambda$ en la mano, el autovector es la "cruz" de las filas de $A - \lambda I$ (en 2D: la perpendicular a una fila), igual que en el bloque C.

    **La transformación $A - \lambda I$ ↔** a cada vector le restamos $\lambda$ veces él mismo: $A v - \lambda v$. Si $v$ es autovector, lo que queda es cero.
    **El polinomio característico $p(\lambda) = \det(A - \lambda I)$ ↔** "para qué valores de $\lambda$ la transformación modificada aplasta el plano".

    **La escalera $\mathbb{R} \to \mathbb{R}^2 \to \mathbb{R}^3$.**

    | | lo que dice el álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}$ | $a x = \lambda x \Rightarrow (a - \lambda)\,x = 0$; $p(\lambda) = a - \lambda$, grado 1, una raíz: $\lambda = a$ | la "transformación modificada" $a - \lambda$ aplasta la recta sólo cuando $\lambda = a$ |
    | $\mathbb{R}^2$ | $(A - \lambda I)\,v = 0$; $p(\lambda) = \det(A - \lambda I)$, grado 2, a lo sumo dos raíces reales | $A - \lambda I$ aplasta el plano sobre una recta para a lo sumo dos valores de $\lambda$; puede no haber ninguno (giros) |
    | $\mathbb{R}^3$ | grado 3: **siempre** tiene una raíz real | siempre hay al menos una recta que cae sobre sí misma (bloque F) |
    """)
    return


@app.cell
def _(mo):
    mo.callout(
        mo.md(r"""
    **Predecí antes de mirar.** $A = \begin{pmatrix} 2 & 1 \\ 1 & 2 \end{pmatrix}$ y $\lambda$ va a recorrer de $0$ a $4$.
    A la izquierda, $A - \lambda I$ aplicado a la circunferencia unitaria; a la derecha, $p(\lambda) = \det(A - \lambda I)$.

    - ¿Cuántas veces se va a aplastar la elipse a un segmento? ¿En qué valores de $\lambda$? (el bloque D ya te los mostró)
    - Cuando se aplasta, ¿en qué dirección queda el segmento? ¿Tiene algo que ver con el autovector?
    """),
        kind="warn",
    )
    return


@app.cell
def _(mo):
    lam_e = mo.ui.slider(start=0.0, stop=4.0, step=0.01, value=4.0, label="λ final")
    return (lam_e,)


@app.cell
def _(FuncAnimation, anim_html, circulo, lam_e, mo, np, plt, pmat):
    A_e = np.array([[2.0, 1.0], [1.0, 2.0]])
    lam_val_e = float(lam_e.value)
    B_e = A_e - lam_val_e * np.eye(2)
    det_e = float(np.linalg.det(B_e))
    _C = circulo()
    _N = 60
    _ls = np.linspace(0, lam_val_e, _N) if lam_val_e > 0 else np.array([0.0])
    _lgrid = np.linspace(0, 4, 300)
    _pgrid = [np.linalg.det(A_e - l * np.eye(2)) for l in _lgrid]

    _fig, (_ax, _axp) = plt.subplots(1, 2, figsize=(8.4, 4.2), dpi=90, gridspec_kw={"width_ratios": [1.05, 1]})
    _L = 3.3
    _ax.set_xlim(-_L, _L)
    _ax.set_ylim(-_L, _L)
    _ax.set_aspect("equal")
    _ax.axhline(0, color="gray", lw=0.8)
    _ax.axvline(0, color="gray", lw=0.8)
    _ax.grid(True, alpha=0.3)
    _ax.plot(_C[0], _C[1], color="gray", lw=1)
    for _d, _c, _n in ((np.array([1, 1]) / np.sqrt(2), "tab:red", "(1, 1)"), (np.array([1, -1]) / np.sqrt(2), "tab:green", "(1, −1)")):
        _ax.plot([-2 * _L * _d[0], 2 * _L * _d[0]], [-2 * _L * _d[1], 2 * _L * _d[1]], ls="--", color=_c, lw=1, alpha=0.7, label=f"dirección {_n}")
    (_el,) = _ax.plot(_C[0], _C[1], color="tab:blue", lw=1.6, label="(A − λI)·circunferencia")
    _ax.legend(loc="upper left", fontsize=7)
    _tit = _ax.set_title("", fontsize=10)

    _axp.plot(_lgrid, _pgrid, color="tab:purple", lw=1.5)
    _axp.axhline(0, color="gray", lw=0.8)
    for _r in (1, 3):
        _axp.axvline(_r, color="gray", lw=0.8, ls=":")
    _axp.set_xlim(0, 4)
    _axp.set_xlabel("λ")
    _axp.set_title("p(λ) = det(A − λI) = λ² − 4λ + 3", fontsize=10)
    _axp.grid(True, alpha=0.3)
    (_dot,) = _axp.plot([], [], "o", color="black", ms=7)
    _fig.tight_layout()

    def _update(i):
        l = _ls[i]
        M = A_e - l * np.eye(2)
        E = M @ _C
        _el.set_data(E[0], E[1])
        d = np.linalg.det(M)
        _tit.set_text(f"λ = {l:.2f}    det(A − λI) = {d:+.2f}")
        _dot.set_data([l], [d])
        return _el, _tit, _dot

    _anim = FuncAnimation(_fig, _update, frames=len(_ls), interval=60, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md("**Controles**"),
            lam_e,
            mo.md(rf"$A - \lambda I = {pmat(B_e)}$  \n$\det(A - \lambda I) = {det_e:+.3f}$"),
            mo.md("Llevá λ a 1 y a 3: la elipse se vuelve un segmento. Fijate sobre qué recta punteada queda el segmento en cada caso."),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="800px", height="500px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return A_e, B_e, det_e, lam_val_e


@app.cell
def _(A_e, mo, np, perp2):
    _raices = np.sort(np.roots([1, -4, 3]))
    _B3 = A_e - 3 * np.eye(2)
    _B1 = A_e - 1 * np.eye(2)
    _v3 = perp2(_B3[0])  # perpendicular a la fila (-1, 1) → (1, 1)
    _v1 = perp2(_B1[0])  # perpendicular a la fila (1, 1) → (1, -1)
    _cruz3 = np.cross([-1, 1, 0], [0, 0, 1])
    ok_e = bool(
        np.allclose(_raices, [1, 3])
        and np.isclose(np.linalg.det(_B3), 0)
        and np.isclose(np.linalg.det(_B1), 0)
        and np.allclose(_cruz3, [1, 1, 0])
        and np.allclose(A_e @ _v3, 3 * _v3)
        and np.allclose(A_e @ _v1, 1 * _v1)
    )
    mo.md(rf"""
    ### La cuenta a mano

    **1. La versión modificada.** $A - \lambda I = \begin{{pmatrix}} 2 - \lambda & 1 \\ 1 & 2 - \lambda \end{{pmatrix}}$.

    **2. El detector sobre sus filas.**
    $$\det(A - \lambda I) = (2 - \lambda)(2 - \lambda) - 1 \cdot 1 = \lambda^2 - 4\lambda + 3 = (\lambda - 1)(\lambda - 3).$$
    Raíces: $\lambda = 1$ y $\lambda = 3$. Sólo para esos dos valores las filas son colineales y hay algo en el núcleo.

    **3. Autovector de $\lambda = 3$.** $A - 3I = \begin{{pmatrix}} -1 & 1 \\ 1 & -1 \end{{pmatrix}}$; filas $(-1, 1)$ y $(1, -1)$, colineales
    (detector: $(-1)(-1) - 1\cdot 1 = 0$ ✓). La cruz de la fila $(-1, 1)$ con $e_3$:
    $$(-1, 1, 0) \times (0, 0, 1) = (1\cdot 1 - 0\cdot 0,\ \ 0 \cdot 0 - (-1)\cdot 1,\ \ 0) = (1, 1, 0) \quad\Longrightarrow\quad v = (1, 1).$$
    Comprobación: $A\,(1, 1)^T = (2 + 1,\ 1 + 2) = (3, 3) = 3\,(1, 1)$ ✓.

    **4. Autovector de $\lambda = 1$.** $A - I = \begin{{pmatrix}} 1 & 1 \\ 1 & 1 \end{{pmatrix}}$; perpendicular a la fila $(1, 1)$: $v = (1, -1)$.
    Comprobación: $A\,(1, -1)^T = (2 - 1,\ 1 - 2) = (1, -1) = 1\,(1, -1)$ ✓.

    `numpy`: `np.roots([1, -4, 3])` → $({_raices[0]:.0f}, {_raices[1]:.0f})$; $\det(A - 3I) = {np.linalg.det(_B3):.1f}$, $\det(A - I) = {np.linalg.det(_B1):.1f}$;
    cruz $= ({_cruz3[0]}, {_cruz3[1]}, {_cruz3[2]})$; `np.allclose(A v, λ v)` para $(1, 1)$ y $(1, -1)$ · todo → **{ok_e}**

    **Lo que se ve ↔ lo que dice el álgebra.** La elipse se aplasta a un segmento exactamente en $\lambda = 1$ y $\lambda = 3$ ↔ $\det(A - \lambda I) = 0$, las raíces del polinomio característico;
    el punto negro cruza el cero en el gráfico de la derecha ↔ la transformación modificada aplasta el plano;
    el segmento queda sobre la dirección **perpendicular** al autovector ↔ el autovector está en el núcleo de $A - \lambda I$ (va al cero, no aparece en la imagen);
    $A - \lambda I$ no tiene inversa justo ahí ↔ como $1/(a - \lambda)$ en $\mathbb{{R}}$ cuando $\lambda = a$.
    """)
    return (ok_e,)


@app.cell
def _(mo):
    mo.md(r"""
    ## F. Tres dimensiones y los puntos fijos proyectivos

    **Pregunta.** ¿Qué tiene que ver todo esto con los puntos fijos del pentágono de la tarea?

    Recordá la Clase II: un punto del plano $(x, y)$ es el vector $(x, y, 1)$ de $\mathbb{R}^3$, y una transformación proyectiva es una
    matriz $3 \times 3$ que actúa sobre esos vectores (salvo escala). Un punto fijo $H p \sim p$ es exactamente $H p = \lambda p$.
    Con las palabras del profesor: **los puntos fijos de una transformación proyectiva del plano son los subespacios invariantes de $\mathbb{R}^3$**.

    Geométricamente: un autovector es una **recta por el origen** de $\mathbb{R}^3$ que cae sobre sí misma. Esa recta **pincha** el plano
    $z = 1$ en un punto: el punto fijo. Si la recta es paralela al plano (tercera coordenada $0$), no lo pincha: el punto fijo es
    **impropio**, una dirección fija.

    El cálculo es el mismo del bloque E, un piso más arriba en la escalera: raíces de $\det(M - \lambda I)$ y autovector $=$ producto cruz de dos filas de $M - \lambda I$.

    | | lo que dice el álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}^2$ | autovector $=$ perpendicular a **una** fila de $A - \lambda I$ | la dirección que las filas "no ven" (cada fila $\cdot\, v = 0$) |
    | $\mathbb{R}^3$ | autovector $=$ producto cruz de **dos** filas de $M - \lambda I$ | el vector perpendicular a las dos filas a la vez; la tercera fila también le da cero porque las tres son dependientes ($\det = 0$) |

    **Las dos transformaciones de este bloque.** $M_1 = \mathrm{diag}(1, 1, -1)$ ↔ en el plano, la **simetría central** $(x, y) \mapsto (-x, -y)$.
    $M_2 = R_z(\pi/2)\,R_y(\pi/2)$ ↔ una rotación de $\mathbb{R}^3$ (de la Clase I: dos giros de $\pi/2$ compuestos dan un giro de $2\pi/3$ alrededor de un eje nuevo); en el plano, una "rotación proyectiva".
    """)
    return


@app.cell
def _(mo):
    mat_f = mo.ui.dropdown(
        options={"M₁ = diag(1, 1, −1)": "diag", "M₂ = R_z(π/2)·R_y(π/2)": "rot"},
        value="M₂ = R_z(π/2)·R_y(π/2)",
        label="Matriz",
    )
    return (mat_f,)


@app.cell
def _(mat_f, mo):
    mo.callout(
        mo.vstack(
            [
                mo.md(r"""
    **Predecí antes de mirar.** Elegí una matriz.

    - $M_1 = \mathrm{diag}(1, 1, -1)$ manda $(x, y, 1)$ a $(x, y, -1) \sim (-x, -y, 1)$. ¿Qué transformación del plano es? ¿Cuántos puntos fijos propios tiene? ¿Y direcciones fijas?
    - $M_2 = R_z(\pi/2)\,R_y(\pi/2)$ es una rotación de $\mathbb{R}^3$. ¿Cuántos autovalores reales puede tener una rotación? ¿Cuántos puntos fijos reales le quedan al plano?
    """),
                mat_f,
            ],
            gap=0.4,
        ),
        kind="warn",
    )
    return


@app.cell
def _(mat_f, np, rot_y, rot_z):
    if mat_f.value == "diag":
        M_f = np.diag([1.0, 1.0, -1.0])
        nombre_f = "M_1"
    else:
        M_f = rot_z(np.pi / 2) @ rot_y(np.pi / 2)
        M_f = np.round(M_f)  # enteros exactos: [[0,-1,0],[0,0,1],[-1,0,0]]
        nombre_f = "M_2"

    # autovalores reales (sin repetir) y, para cada uno, el autovector por producto cruz de dos filas de M − λI
    _w = np.linalg.eigvals(M_f)
    _reales = sorted({round(float(z.real), 6) for z in _w if abs(z.imag) < 1e-9})
    _complejos = [z for z in _w if abs(z.imag) >= 1e-9]

    def _autovec_cruz(lam):
        B = M_f - lam * np.eye(3)
        mejor = None
        for i, j in ((0, 1), (0, 2), (1, 2)):
            c = np.cross(B[i], B[j])
            if mejor is None or np.linalg.norm(c) > np.linalg.norm(mejor[2]):
                mejor = (i, j, c)
        i, j, c = mejor
        if np.linalg.norm(c) < 1e-9:
            return dict(lam=lam, B=B, plano=True)  # todas las cruces dan cero: el núcleo es un plano
        v = c / np.abs(c).max()
        v = np.round(v, 6)
        return dict(lam=lam, B=B, plano=False, i=i, j=j, cruz=c, v=v)

    info_f = [_autovec_cruz(l) for l in _reales]
    complejos_f = _complejos
    return M_f, complejos_f, info_f, nombre_f


@app.cell
def _(FuncAnimation, M_f, Poly3DCollection, anim_html, info_f, mo, nombre_f, np, plt, pmat, vec_tex):
    _fig = plt.figure(figsize=(5.6, 5.4), dpi=90)
    _ax = _fig.add_subplot(projection="3d")
    _L = 2.6
    _S = 2.2
    # plano z = 1
    _sq = np.array([[-_S, -_S, 1], [_S, -_S, 1], [_S, _S, 1], [-_S, _S, 1]])
    _ax.add_collection3d(Poly3DCollection([_sq], facecolors="tab:blue", alpha=0.12, edgecolors="tab:blue", linewidths=0.8))
    _ax.text(_S, _S, 1.05, "plano z = 1", color="tab:blue", fontsize=8)
    for _p in ((_L, 0, 0), (0, _L, 0), (0, 0, _L)):
        _ax.plot([0, _p[0]], [0, _p[1]], [0, _p[2]], color="gray", lw=0.8)
    _ax.text(_L, 0, 0, "x", color="gray")
    _ax.text(0, _L, 0, "y", color="gray")
    _ax.text(0, 0, _L, "z", color="gray")
    _ax.scatter([0], [0], [0], color="k", s=15)

    _cols = ["tab:red", "tab:green", "tab:orange"]
    _lineas_md = []
    for _inf, _c in zip(info_f, _cols):
        _lam = _inf["lam"]
        if _inf["plano"]:
            # núcleo = plano z = 0: todas las direcciones (a, b, 0) son autovectores → recta de puntos fijos impropios
            _t = np.linspace(0, 2 * np.pi, 120)
            _ax.plot(_L * np.cos(_t), _L * np.sin(_t), 0 * _t, color=_c, lw=1.5, ls="--")
            _ax.text(_L * 0.7, -_L * 0.7, 0.08, "z = 0: todas las direcciones fijas", color=_c, fontsize=8)
            _lineas_md.append(rf"- $\lambda = {_lam:.0f}$: el núcleo de ${nombre_f} - \lambda I$ es **todo el plano** $z = 0$ → toda dirección $(a, b, 0)$ es fija: recta de puntos fijos impropios (la recta del infinito).")
            continue
        _v = _inf["v"]
        _d = _v / np.linalg.norm(_v)
        _ax.plot([-_L * _d[0], _L * _d[0]], [-_L * _d[1], _L * _d[1]], [-_L * _d[2], _L * _d[2]], color=_c, lw=2, label=f"λ = {_lam:.0f}: recta de {vec_tex(_v)}")
        if abs(_v[2]) > 1e-9:
            _pf = _v / _v[2]
            _ax.scatter([_pf[0]], [_pf[1]], [1], marker="*", s=180, color=_c, edgecolors="k", zorder=6)
            _ax.text(_pf[0], _pf[1], 1.15, f"punto fijo ({_pf[0]:.0f}, {_pf[1]:.0f})", color=_c, fontsize=8)
            _lineas_md.append(rf"- $\lambda = {_lam:.0f}$: autovector ${vec_tex(_v)}$, tercera coordenada $\neq 0$ → pincha $z = 1$ en el **punto fijo propio** $({_pf[0]:.0f}, {_pf[1]:.0f})$.")
        else:
            _lineas_md.append(rf"- $\lambda = {_lam:.0f}$: autovector ${vec_tex(_v)}$, tercera coordenada $0$ → paralelo al plano: **punto fijo impropio**, dirección $({_v[0]:.0f}, {_v[1]:.0f})$.")
    _ax.set_xlim(-_L, _L)
    _ax.set_ylim(-_L, _L)
    _ax.set_zlim(-_L, _L)
    _ax.set_box_aspect((1, 1, 1))
    _ax.legend(loc="upper left", fontsize=7)
    _ax.set_title(f"{nombre_f.replace('_', '')}: rectas invariantes de R³ y el plano z = 1", fontsize=10)

    _azims = np.linspace(-60, 300, 48)

    def _update(i):
        _ax.view_init(elev=22, azim=float(_azims[i]))
        return []

    _anim = FuncAnimation(_fig, _update, frames=len(_azims), interval=90, blit=False)
    _html = anim_html(_anim, _fig)

    _controles = mo.vstack(
        [
            mo.md(rf"${nombre_f} = {pmat(M_f)}$"),
            mo.md("\n".join(_lineas_md)),
            mo.md("La vista gira sola para que se vea la recta pinchando el plano."),
        ],
        gap=0.6,
    )
    mo.hstack(
        [_controles, mo.iframe(_html, width="540px", height="600px")],
        justify="start",
        align="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell
def _(M_f, complejos_f, info_f, mo, nombre_f, np, pmat, vec_tex):
    _partes = []
    _ok = True
    for _inf in info_f:
        _lam = _inf["lam"]
        _B = _inf["B"]
        if _inf["plano"]:
            _partes.append(
                rf"""**$\lambda = {_lam:.0f}$.** ${nombre_f} - {_lam:.0f} I = {pmat(_B)}$. Dos filas son **cero**: cualquier cruz de dos filas da $(0, 0, 0)$.
    Es el "caso difícil" que mencionó el profesor: dos autovectores con el mismo autovalor. El núcleo no es una recta sino el plano $z = 0$ entero,
    y cualquier $(a, b, 0)$ cumple ${nombre_f}\,(a, b, 0)^T = (a, b, 0)^T$: todas las direcciones del plano son fijas."""
            )
            _ok = _ok and bool(np.allclose(M_f @ np.array([1, 0, 0]), np.array([1, 0, 0])) and np.allclose(M_f @ np.array([0, 1, 0]), np.array([0, 1, 0])))
            continue
        _i, _j, _c, _v = _inf["i"], _inf["j"], _inf["cruz"], _inf["v"]
        _fi, _fj = _B[_i], _B[_j]
        _ok = _ok and bool(np.allclose(M_f @ _v, _lam * _v)) and bool(np.allclose(_B @ _v, 0))
        _cuenta = (
            rf"({_fi[1]:.0f})({_fj[2]:.0f}) - ({_fi[2]:.0f})({_fj[1]:.0f}),\ \ "
            rf"({_fi[2]:.0f})({_fj[0]:.0f}) - ({_fi[0]:.0f})({_fj[2]:.0f}),\ \ "
            rf"({_fi[0]:.0f})({_fj[1]:.0f}) - ({_fi[1]:.0f})({_fj[0]:.0f})"
        )
        _Mv = M_f @ _v
        _partes.append(
            rf"""**$\lambda = {_lam:.0f}$.** ${nombre_f} - {_lam:.0f} I = {pmat(_B)}$. Cruz de las filas {_i + 1} y {_j + 1}:
    $${vec_tex(_fi)} \times {vec_tex(_fj)} = \big({_cuenta}\big) = {vec_tex(_c)}{"" if np.allclose(_c, _v) else rf" \sim {vec_tex(_v)}"}.$$
    Es perpendicular a **las tres** filas (la que no usamos también da cero: fila {3 - _i - _j + 1 if (_i, _j) != (0, 1) else 3} $\cdot\,v = {float(_B[[k for k in range(3) if k not in (_i, _j)][0]] @ _v):.0f}$), así que está en el núcleo de ${nombre_f} - {_lam:.0f} I$.
    Comprobación: ${nombre_f}\,{vec_tex(_v)}^T = {vec_tex(_Mv)}^T = {_lam:.0f}\,{vec_tex(_v)}^T$ ✓"""
        )
    ok_f = _ok
    _w = np.linalg.eigvals(M_f)
    _pol = np.poly(M_f)  # coeficientes de det(λI − M)

    def _polytex(c):
        # c = [1, c2, c1, c0] de λ³ + c2 λ² + c1 λ + c0
        s = r"\lambda^3"
        for coef, mono in ((c[1], r"\lambda^2"), (c[2], r"\lambda"), (c[3], "")):
            coef = float(np.round(coef, 9))
            if abs(coef) < 1e-9:
                continue
            signo = " - " if coef < 0 else " + "
            mag = "" if (abs(abs(coef) - 1) < 1e-9 and mono) else f"{abs(coef):.0f}"
            s += signo + mag + mono
        return s

    _cplx = (
        rf" Los otros dos, ${complejos_f[0].real:.2f} \pm {abs(complejos_f[0].imag):.2f}\,i$, son complejos: es una rotación de $\mathbb{{R}}^3$ (ángulo $2\pi/3$ alrededor del eje) y sólo deja fija esa recta. En el plano proyectivo: **un solo punto fijo real**, como la cíclica del pentágono."
        if complejos_f
        else r" Todos reales: la transformación deja fijo el origen ($\lambda = -1$) y todas las direcciones ($\lambda = 1$). Es la simetría central $(x, y) \mapsto (-x, -y)$: una homología con centro en el origen y eje en la recta del infinito."
    )
    mo.md(
        rf"""
    ### La cuenta a mano

    **1. Polinomio característico.** Desarrollando $\det({nombre_f} - \lambda I)$ por la primera fila (o mirando la diagonal si es diagonal):
    $\det(\lambda I - {nombre_f}) = {_polytex(_pol)}$. Autovalores reales: {", ".join(rf"$\lambda = {inf['lam']:.0f}$" for inf in info_f)}.{_cplx}

    **2. Autovectores por producto cruz de dos filas.**

    {chr(10).join(_partes)}

    `numpy`: `np.linalg.eigvals` → $({", ".join(f"{z.real:.2f}" + (f"{z.imag:+.2f}i" if abs(z.imag) > 1e-9 else "") for z in _w)})$ ·
    `np.allclose(M v, λ v)` y `np.allclose((M − λI) v, 0)` para cada autovector → **{ok_f}**

    **Lo que se ve ↔ lo que dice el álgebra.** La recta roja cae sobre sí misma y pincha el plano en la estrella ↔ $M v = \lambda v$ con $v_3 \neq 0$ y punto fijo $(v_1/v_3, v_2/v_3)$;
    una recta invariante paralela al plano ↔ $v_3 = 0$, punto fijo impropio.

    **Para la tarea del pentágono.** La $H$ de $3\times 3$ que calculaste para cada correspondencia es una de estas matrices: sus puntos fijos
    (ítem 4) son los autovectores de $H$, y se hallan **exactamente así**: raíces de $\det(H - \lambda I)$ y producto cruz de dos filas de $H - \lambda I$.
    Si la tercera coordenada del autovector da $0$, el punto fijo es impropio. No lo resolvemos acá; es tuyo.
    """
    )
    return (ok_f,)


@app.cell
def _(mo):
    mo.md(r"""
    ## Rúbrica de autoevaluación

    | Elemental | Medio | Avanzado |
    |---|---|---|
    | $u \wedge v = u_1 v_2 - u_2 v_1$ es el área orientada del paralelogramo; vale $0$ si y sólo si $u$ y $v$ son colineales | El producto cuña de $n$ vectores en $\mathbb{R}^n$ es el determinante: mide volumen orientado y detecta dependencia lineal | Las reglas $e_i \wedge e_i = 0$ y $e_j \wedge e_i = -e_i \wedge e_j$ bastan para reconstruir el determinante de cualquier tamaño |
    | En una transformación lineal el cero va al cero; el núcleo son **todos** los vectores que van al cero | $\det A = 0$ ↔ las filas son colineales ↔ el núcleo tiene algo más que el cero ↔ la transformación pierde una dimensión | El núcleo se calcula como producto cruz de las filas (en 2D: la perpendicular a una fila); la imagen es la recta o plano generado por las columnas |
    | Un autovector es una dirección que cae sobre sí misma: $A v = \lambda v$ | $A - \lambda I$ es una versión modificada de la transformación con el autovector en el núcleo; $\det(A - \lambda I) = 0$ da los autovalores | Los autovectores se obtienen con el producto cruz de dos filas de $A - \lambda I$; si todas las cruces dan cero, el núcleo es un plano (autovalor repetido) |
    | Al aplicar $A$ muchas veces, cualquier vector se acerca a la dirección del autovalor más grande | $A = P D P^{-1}$: ir a la base de autovectores, estirar, volver; permite definir $A^t$ para $t$ real | Una matriz simétrica tiene autovectores perpendiculares; una no simétrica en general no, y puede tener autovalores complejos (rotaciones) |
    | Un punto fijo de una transformación proyectiva del plano es un autovector de la matriz $3\times 3$ | La recta invariante de $\mathbb{R}^3$ pincha el plano $z = 1$ en el punto fijo; si $v_3 = 0$ el punto fijo es impropio | Un polinomio de grado 3 siempre tiene una raíz real: toda transformación proyectiva del plano tiene al menos un punto fijo real, propio o impropio |
    | En $\mathbb{R}$ todo es un número: el determinante es $a$, el núcleo es $\{0\}$ salvo que $a = 0$, todo vector es autovector con $\lambda = a$, y $1/a$ no existe si $a = 0$ | Cada concepto de $\mathbb{R}^2$ y $\mathbb{R}^3$ es "lo mismo con más coordenadas": $1 \to I$, $1/a \to A^{-1}$, $a = 0 \leftrightarrow \det A = 0$ | Lo nuevo al subir de dimensión son los casos intermedios: núcleos que son una recta pero no todo, direcciones que son fijas y otras que no |
    """)
    return


@app.cell
def _(mo, np, ok_a, ok_b, ok_c, ok_d, ok_e, ok_f, perp2, pot_real, rot_y, rot_z):
    # ---------- verificaciones automáticas del notebook (independientes de los controles) ----------
    _fallas = []

    def _chk(cond, msg):
        if not cond:
            _fallas.append(msg)

    # A
    _chk(np.isclose(np.linalg.det(np.array([[3, 1], [1, 2]])), 5), "A: det[u v] ≠ 5")
    _chk(np.isclose(np.linalg.det(np.array([[1, 3], [2, 1]])), -5), "A: det[v u] ≠ -5")
    # B
    _u, _v, _w0, _w1 = np.array([1, 2, 0]), np.array([0, 1, 1]), np.array([1, 0, 2]), np.array([1, 3, 1])
    _chk(np.allclose(np.cross(_u, _v), [2, -1, 1]), "B: u × v ≠ (2, -1, 1)")
    _chk(np.isclose(np.linalg.det(np.column_stack([_u, _v, _w0])), 4), "B: det ≠ 4")
    _chk(np.isclose(np.linalg.det(np.column_stack([_u, _v, _w1])), 0), "B: det con w en el plano ≠ 0")
    # C
    _A = np.array([[1, 2], [2, 4]])
    _chk(np.isclose(np.linalg.det(_A), 0) and np.allclose(_A @ perp2(_A[0]), 0), "C: (2, -1) no está en el núcleo")
    _chk(np.isclose(np.linalg.det(0.5 * np.eye(2) + 0.5 * _A), (1 - 0.5) * (1 + 4 * 0.5)), "C: det A_t ≠ (1-t)(1+4t)")
    # D
    _As = np.array([[2, 1], [1, 2]])
    _Bn = np.array([[3, 1], [0, 2]])
    _chk(np.allclose(_As @ [1, 1], 3 * np.array([1, 1])) and np.allclose(_As @ [1, -1], [1, -1]), "D: autovectores de A")
    _chk(np.allclose(_Bn @ [1, 0], [3, 0]) and np.allclose(_Bn @ [1, -1], 2 * np.array([1, -1])), "D: autovectores de B")
    _chk(np.allclose(pot_real(_As, 1.0), _As) and np.allclose(pot_real(_As, 0.5) @ pot_real(_As, 0.5), _As), "D: A^t por diagonalización")
    _chk(np.allclose(pot_real(_Bn, 2.0), _Bn @ _Bn), "D: B^2 por diagonalización")
    # E
    _chk(np.allclose(np.sort(np.roots([1, -4, 3])), [1, 3]), "E: raíces del polinomio característico")
    _chk(np.allclose(np.sort(np.linalg.eigvals(_As)), [1, 3]), "E: eigvals(A) ≠ (1, 3)")
    _chk(np.allclose(np.cross([-1, 1, 0], [0, 0, 1]), [1, 1, 0]), "E: cruz de la fila (-1, 1) ≠ (1, 1, 0)")
    # F
    _M2 = np.round(rot_z(np.pi / 2) @ rot_y(np.pi / 2))
    _chk(np.array_equal(_M2, np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]])), f"F: Rz·Ry = {_M2.tolist()}")
    _eje = np.cross((_M2 - np.eye(3))[0], (_M2 - np.eye(3))[1])
    _chk(np.allclose(_eje, [-1, 1, 1]), f"F: cruz de filas 1 y 2 de M2 − I = {_eje}")
    _chk(np.allclose(_M2 @ [-1, 1, 1], [-1, 1, 1]), "F: (-1, 1, 1) no es fijo por M2")
    _chk(np.isclose(np.trace(_M2), 0), "F: M2 no es una rotación de 2π/3 (traza ≠ 0)")
    _M1 = np.diag([1.0, 1.0, -1.0])
    _chk(np.allclose(np.cross((_M1 + np.eye(3))[0], (_M1 + np.eye(3))[1]), [0, 0, 4]), "F: cruz de filas de M1 + I ≠ (0, 0, 4)")
    _chk(np.allclose(_M1 @ [0, 0, 1], -np.array([0, 0, 1])), "F: (0, 0, 1) no es autovector de M1 con λ = -1")
    # flags de las celdas "cuenta a mano"
    _chk(all([ok_a, ok_b, ok_c, ok_d, ok_e, ok_f]), f"flags de las cuentas a mano: A={ok_a} B={ok_b} C={ok_c} D={ok_d} E={ok_e} F={ok_f}")

    verificacion_ok = not _fallas
    mo.output.append(
        mo.callout(
            mo.md(
                "**Verificación OK** — todas las cuentas a mano de los bloques A–F coinciden con `numpy` "
                "(determinantes, productos cruz, núcleo, autovalores, autovectores, $A^t$ por diagonalización y eje de $R_z R_y$)."
            )
            if verificacion_ok
            else mo.md("**Verificación FALLÓ**\n\n" + "\n".join(f"- {f}" for f in _fallas)),
            kind="success" if verificacion_ok else "danger",
        )
    )
    assert verificacion_ok, "\n".join(_fallas)
    return


if __name__ == "__main__":
    app.run()
