# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""Prueba mínima del patrón recomendado para animaciones en WASM: plotly con frames + botón play.

No es una unidad de la materia. Sirve para verificar que `marimo export html-wasm` conserva el JSON
de la figura (frames incluidos) sin pasar por `mo.iframe` ni por `FuncAnimation.to_jshtml()`.

Probar local:   uv run marimo run tools/_prueba_plotly.py
Exportar:       uv run marimo export html-wasm --mode run -o /tmp/prueba_plotly tools/_prueba_plotly.py
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


@app.cell
def _(mo):
    angulo = mo.ui.slider(0, 360, value=90, step=5, label="ángulo total (°)")
    angulo
    return (angulo,)


@app.cell
def _(angulo, go, mo, np):
    # un vector que rota desde 0 hasta el ángulo elegido; cada frame es un paso
    _n = 24
    _ts = np.linspace(0, np.deg2rad(angulo.value), _n)
    _frames = [
        go.Frame(
            name=str(_i),
            data=[go.Scatter(x=[0, np.cos(_t)], y=[0, np.sin(_t)], mode="lines+markers")],
        )
        for _i, _t in enumerate(_ts)
    ]
    _fig = go.Figure(
        data=[go.Scatter(x=[0, 1], y=[0, 0], mode="lines+markers", line=dict(color="#1b6f6a", width=4))],
        frames=_frames,
        layout=go.Layout(
            width=420,
            height=420,
            xaxis=dict(range=[-1.2, 1.2], scaleanchor="y", zeroline=True),
            yaxis=dict(range=[-1.2, 1.2], zeroline=True),
            updatemenus=[
                dict(
                    type="buttons",
                    showactive=False,
                    buttons=[
                        dict(label="▶ play", method="animate", args=[None, dict(frame=dict(duration=60, redraw=True), fromcurrent=True)]),
                        dict(label="⏸ pausa", method="animate", args=[[None], dict(mode="immediate", frame=dict(duration=0))]),
                    ],
                )
            ],
        ),
    )
    mo.ui.plotly(_fig)
    return


if __name__ == "__main__":
    app.run()
