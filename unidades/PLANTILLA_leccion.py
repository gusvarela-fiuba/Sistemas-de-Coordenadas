# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "marimo",
#     "numpy",
#     "plotly",
# ]
# ///
"""PLANTILLA de lección (molde v2, docs/camino.md). No es una unidad: no va en mapa/_fragmentos/unidades.yaml.

Cómo usarla: copiar a `unidades/NN_<tema>.py`, reemplazar todo lo que está entre [corchetes], borrar las notas
"PLANTILLA:" y dar de alta la unidad en `unidades.yaml`. Las seis secciones van en este orden y con `##` visible:

  0. Situación de campo y predicción   (mo.ui.radio + un callout por opción)
  1. Hecho geométrico                  (qué se conserva, escalera R → R² → R³)
  2. Manipulación                      (figura de tres capas: gris antes / teal después / objeto; deslizador + casos precargados)
                                       LAYOUT ESTÁNDAR (pantalla 16:9, columna de marimo de 1240 px): la figura a la
                                       IZQUIERDA (10/16 ≈ 775 px) y a la DERECHA (6/16 ≈ 465 px) UN solo panel con el
                                       selector `caso` arriba, los deslizadores y los números vivos. Se arma con
                                       `lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)`, que equivale a
                                       `mo.hstack([mo.ui.plotly(figura), _panel], widths=[10, 6], align="start", gap=1.25)`.
                                       Tamaños por default: `lib.figura_plano` 540×500 y `lib.figura_espacio` 540×520
                                       (no pasar ancho/alto mayores en la figura de manipulación). La celda que crea el
                                       dropdown `caso` NO lo muestra suelto: `caso` se muestra sólo adentro del panel.
                                       Nada de figura arriba y controles abajo, nada de panel a la izquierda.
  3. Cuenta a mano y código lado a lado (matriz coloreada por columnas)
  4. Python de hoy                     (una sola idea nueva)
  5. Ejercicios                        (dos de lápiz, dos de código con hueco verificados con np.allclose)
  Anexo: enlaces al apunte por sección (../../apunte.pdf#nameddest=cap:NN) y verificación silenciosa.

Tono: primera persona del singular, voz activa ("acá muestro", "lo demuestro en el apunte"). Distinguir siempre
"muestra" (la figura muestra que…) de "demostración" (la demostración está en el apunte, sección NN).
Grados en la interfaz, radianes adentro. Sólo numpy y plotly, vía el módulo común `cb104` (celda marcada).

Chequear:  uv run marimo check --select MW unidades/NN_<tema>.py
Exportar:  uv run python tools/build.py --only NN_<tema>
"""

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import cb104 as lib  # cb104:inline
    return (lib,)


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import plotly.graph_objects as go

    return go, mo, np


@app.cell
def _(mo):
    mo.md(r"""
    # Unidad [NN] — [Título: la pregunta de campo que responde la unidad]

    **Sistemas de Coordenadas** · Agrimensura · FIUBA · 2C2026 · Gustavo Varela

    [PLANTILLA: una o dos líneas: qué clase sigue esta unidad y qué pregunta de campo responde. Por ejemplo:
    "Sigo la clase N (…). La pregunta: ¿qué le pasa a … cuando …?"]

    Código de colores, igual en la figura y en el álgebra: la **primera columna** de una matriz es
    <span style="color:#1b6f6a">**teal**</span>, la **segunda** <span style="color:#b5451b">**rust**</span> y la
    **tercera** <span style="color:#c9a227">**gold**</span>. Cada columna es la imagen de un vector de la base y en la
    figura se dibuja del mismo color.
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 0. Situación de campo y predicción

    [PLANTILLA: una situación concreta de agrimensura, sin fajas ni EPSG. Qué se mide, con qué instrumento, en qué
    marco, y qué número hay que obtener. Dos o tres párrafos como máximo.]
    """)
    return


@app.cell
def _(lib, np):
    # ---------- los números de la predicción salen de acá, nunca a mano ----------
    punto = np.array([4.0, 3.0])  # [PLANTILLA: el punto de la situación de campo]
    M_prediccion = lib.rot2(np.deg2rad(30))  # [PLANTILLA: la transformación de la situación]
    candidatos = {
        "correcta": M_prediccion @ punto,
        "error-tipico": M_prediccion.T @ punto,  # [PLANTILLA: el error típico, por ejemplo el sentido contrario]
        "reflexion": np.diag([1.0, -1.0]) @ punto,
        "mismas": punto.copy(),
    }
    return M_prediccion, candidatos, punto


@app.cell
def _(candidatos, lib, mo):
    prediccion = mo.ui.radio(
        options={
            lib.vec_tex(candidatos["correcta"]): "correcta",
            lib.vec_tex(candidatos["mismas"]) + "  (las mismas)": "mismas",
            lib.vec_tex(candidatos["error-tipico"]): "error-tipico",
            lib.vec_tex(candidatos["reflexion"]): "reflexion",
        },
        value=None,
        label="**Predicción.** [PLANTILLA: la pregunta concreta, con los datos de la situación]. El resultado es…",
    )
    prediccion
    return (prediccion,)


@app.cell
def _(mo, prediccion):
    _respuestas = {
        None: ("neutral", "Elegí una opción antes de seguir: la predicción vale más que la respuesta."),
        "correcta": ("success", "**Sí.** [PLANTILLA: confirmar y adelantar qué va a mostrar la unidad.]"),
        "error-tipico": ("warn", "**No.** [PLANTILLA: explicar el error concreto: qué se confundió con qué, no sólo 'incorrecto'.]"),
        "reflexion": ("warn", "**No.** [PLANTILLA: por qué eso es un espejo y no la transformación de la situación.]"),
        "mismas": ("warn", "**No.** [PLANTILLA: por qué los números cambian aunque el punto no se mueva.]"),
    }
    _kind, _texto = _respuestas[prediccion.value]
    mo.callout(mo.md(_texto), kind=_kind)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 1. Hecho geométrico

    **¿Qué se conserva?** [PLANTILLA: antes que la fórmula, lo que queda igual y lo que cambia.]

    | | álgebra | lo que se ve |
    |---|---|---|
    | $\mathbb{R}$ | [el caso 1D: un número] | [qué hace sobre la recta] |
    | $\mathbb{R}^2$ | [la matriz 2×2] | [qué hace sobre el plano] |
    | $\mathbb{R}^3$ | [la matriz 3×3] | [qué hace sobre el espacio] |

    [PLANTILLA: cada fórmula con su hecho geométrico al lado. Esto es una **muestra** (la figura lo muestra);
    la **demostración** está en el apunte, sección NN (ver anexo).]
    """)
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 2. Manipulación

    [PLANTILLA: qué controlar y qué mirar. Tres capas: gris = antes, teal = después (columnas como flechas),
    violeta = el objeto reconocible con estelas. La figura a la izquierda; a la derecha el panel con los casos
    precargados arriba del deslizador y los números vivos debajo.]
    """)
    return


@app.cell
def _(mo, np):
    # ---------- casos precargados: etiqueta → (tipo, dato, qué se conserva y qué no) ----------
    casos = {
        "identidad (0°)": ("rotacion", 0, "no cambia nada."),
        "giro de 90°": ("rotacion", 90, "se conservan distancias, ángulos y área."),
        "giro de 35°": ("rotacion", 35, "se conservan distancias, ángulos y área."),
        "reflexión (no es rotación)": ("matriz", np.diag([1.0, -1.0]), "conserva distancias pero da vuelta la orientación: área −1."),
        "corte (no es rotación)": ("matriz", np.array([[1.0, 0.5], [0.0, 1.0]]), "conserva el área pero no los ángulos."),
        "proyección det = 0 (no es rotación)": ("matriz", np.array([[1.0, 0.0], [0.0, 0.0]]), "aplasta el plano: área 0."),
    }
    caso = mo.ui.dropdown(options=list(casos), value="giro de 35°", label="caso precargado")
    # PLANTILLA: esta celda no muestra `caso` (ni nada, o a lo sumo el encabezado de la sección); el dropdown se
    # muestra una sola vez, adentro del panel de la celda de la figura.
    return caso, casos


@app.cell
def _(caso, casos, mo):
    # el deslizador depende del caso: arranca en el ángulo del caso y queda deshabilitado en los contraejemplos
    _tipo, _dato, _ = casos[caso.value]
    es_rotacion = _tipo == "rotacion"
    angulo = mo.ui.slider(-180, 180, value=_dato if es_rotacion else 0, step=1, label="θ (°)", disabled=not es_rotacion)
    return angulo, es_rotacion


@app.cell
def _(lib, np):
    # ---------- objetos fijos de la figura ----------
    rango = 5
    objeto_puntos = np.array([[1.0, 1.0], [5.0, 1.0], [5.0, 3.0], [3.0, 4.0], [1.0, 3.0]])  # [PLANTILLA: parcela de vértices enteros]
    cuadrado = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float)
    _ = lib.area_poligono(cuadrado)  # 1: referencia para los números vivos
    return cuadrado, objeto_puntos, rango


@app.cell
def _(angulo, caso, casos, cuadrado, es_rotacion, go, lib, mo, np, objeto_puntos, rango):
    _tipo, _dato, que_conserva = casos[caso.value]
    if es_rotacion:
        theta = np.deg2rad(angulo.value)
        M = lib.rot2(theta)
        camino = [lib.rot2(t) for t in np.linspace(0, theta, 36)]
    else:
        M = np.asarray(_dato, dtype=float)
        camino = [np.eye(2) + s * (M - np.eye(2)) for s in np.linspace(0, 1, 36)]

    def _dinamicas(i):
        """Las trazas que cambian con el cuadro i, en orden fijo."""
        Mi = camino[i]
        f = go.Figure()
        lib.capa_despues(f, Mi, rango)
        lib.objeto(f, lib.transformar(objeto_puntos, Mi), lib.VIOLETA_OBJETO, "parcela",
                   estelas=lib.estelas(objeto_puntos, camino[: i + 1]))
        return list(f.data)

    _titulo = f"θ = {angulo.value}°" if es_rotacion else f"{caso.value}"
    figura = lib.figura_plano(rango + 1, _titulo)
    lib.capa_antes(figura, rango)
    lib.objeto(figura, objeto_puntos, lib.GRIS_ANTES, "parcela antes", relleno=False)
    for _t in _dinamicas(len(camino) - 1):
        figura.add_trace(_t)
    lib.animar(figura, [_dinamicas(i) for i in range(len(camino))])

    area_cuadrado = lib.area_poligono(lib.transformar(cuadrado, M))
    # PLANTILLA: panel único a la derecha: título, selector de caso, deslizadores, números vivos (en ese orden).
    _panel = mo.vstack([
        mo.md("**Controles**"),
        caso,
        angulo,
        mo.md(rf"""
        **Números vivos**

        - área con signo del cuadrado unitario transformado: $\mathbf{{{area_cuadrado:.4f}}}$ ($\det M = {np.linalg.det(M):.4f}$)

        $$M = {lib.matriz_coloreada(M)}$$

        **Qué pasa acá:** {que_conserva} Apretá **reproducir** para ver el camino de la identidad a $M$.
        """),
    ], gap=0.55)
    # PLANTILLA: figura a la IZQUIERDA (10/16) y panel a la DERECHA (6/16). Equivale a
    # mo.hstack([mo.ui.plotly(figura), _panel], widths=[10, 6], align="start", gap=1.25).
    lib.mesa_interactiva(mo, mo.ui.plotly(figura), _panel)
    return M, area_cuadrado


@app.cell
def _(mo):
    mo.md(r"""
    ## 3. Cuenta a mano y código lado a lado

    [PLANTILLA: una cuenta con enteros o valores exactos; a la izquierda el LaTeX con las columnas coloreadas, a la
    derecha el mismo código que corre en la celda. Un hstack por cuenta.]
    """)
    return


@app.cell
def _(lib, mo, np):
    _R = lib.rot2(np.pi / 2)
    _p = np.array([4.0, 3.0])
    _q = _R @ _p
    mo.hstack([
        mo.md(rf"""
        $$R(90°)\,p = {lib.matriz_coloreada(_R, dec=0)} {lib.pmat(_p.reshape(2, 1))} = {lib.pmat(_q.reshape(2, 1))}$$

        [PLANTILLA: la cuenta a mano, término a término.]
        """),
        mo.vstack([
            mo.md("```python\nR = lib.rot2(np.pi / 2)\np = np.array([4.0, 3.0])\nR @ p\n```"),
            mo.md(f"`{np.round(_q, 3).tolist()}`"),
        ]),
    ], widths="equal")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 4. Python de hoy

    [PLANTILLA: una sola idea nueva de Python por unidad, con `shape` y un ejemplo de tres puntos.
    Por ejemplo: una nube es un array N×d con una fila por punto; `lib.transformar(nube, M)` es `nube @ M.T`.]
    """)
    return


@app.cell
def _(lib, mo, np):
    _nube = np.array([[1.0, 0.0], [0.0, 1.0], [2.0, 2.0]])
    _salida = lib.transformar(_nube, lib.rot2(np.pi / 2))
    mo.md(f"`nube.shape = {_nube.shape}` → `transformar(nube, R).shape = {_salida.shape}`\n\n```\n{np.round(_salida, 3)}\n```")
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## 5. Ejercicios

    **(a) Lápiz — elemental** *("[PLANTILLA: frase de la rúbrica del profesor]")*. [PLANTILLA: enunciado.]
    """)
    return


@app.cell
def _(mo):
    mo.accordion({"Ver respuesta (a)": mo.md("[PLANTILLA: respuesta con la cuenta.]")})
    return


@app.cell
def _(mo):
    mo.md(r"""
    **(b) Lápiz — medio** *("[PLANTILLA: frase de la rúbrica]")*. [PLANTILLA: enunciado.]
    """)
    return


@app.cell
def _(mo):
    mo.accordion({"Ver respuesta (b)": mo.md("[PLANTILLA: respuesta con la cuenta.]")})
    return


@app.cell
def _(mo):
    mo.md(r"""
    **(c) Código con hueco — medio** *("[PLANTILLA: frase de la rúbrica]")*. [PLANTILLA: enunciado. Qué tiene
    disponible: `np` y las funciones que se le pasan al `exec`.] Se verifica con `np.allclose`.
    """)
    return


@app.cell
def _(mo):
    editor_c = mo.ui.code_editor(
        value="def rotar(puntos, theta):\n    c, s = np.cos(theta), np.sin(theta)\n    R = ...   # armá la matriz 2×2\n    return ...   # una fila por punto\n",
        language="python",
        min_height=140,
        label="ejercicio (c)",
    )
    editor_c
    return (editor_c,)


@app.cell
def _(editor_c, lib, mo, np):
    _puntos = np.random.default_rng(0).normal(size=(20, 2))
    _theta = 0.7
    _esperado = lib.transformar(_puntos, lib.rot2(_theta))
    _ns = {"np": np}
    try:
        exec(editor_c.value, _ns)
        _obtenido = np.asarray(_ns["rotar"](_puntos, _theta), dtype=float)
        if _obtenido.shape != _esperado.shape:
            _res = mo.callout(mo.md(f"❌ la forma del resultado es `{_obtenido.shape}`; tiene que ser `{_esperado.shape}`."), kind="danger")
        elif np.allclose(_obtenido, _esperado):
            _res = mo.callout(mo.md("✅ coincide con la referencia en 20 puntos al azar."), kind="success")
        else:
            _res = mo.callout(mo.md("❌ no coincide. [PLANTILLA: pista sobre el error más común.]"), kind="warn")
    except Exception as _e:  # el `...` sin completar cae acá
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    **(d) Código con hueco — avanzado** *("[PLANTILLA: frase de la rúbrica]")*. [PLANTILLA: enunciado.]
    """)
    return


@app.cell
def _(mo):
    editor_d = mo.ui.code_editor(
        value="R = ...        # [PLANTILLA: qué armar]\nresultado = ...\n",
        language="python",
        min_height=100,
        label="ejercicio (d)",
    )
    editor_d
    return (editor_d,)


@app.cell
def _(editor_d, lib, mo, np):
    _ns = {"np": np, "rot2": lib.rot2, "rot_x": lib.rot_x, "rot_y": lib.rot_y, "rot_z": lib.rot_z}
    _esperado = np.eye(2)  # [PLANTILLA: la referencia]
    try:
        exec(editor_d.value, _ns)
        _ok = np.allclose(np.asarray(_ns["resultado"], dtype=float), _esperado)
        _res = mo.callout(mo.md("✅ correcto." if _ok else "❌ no coincide con la referencia. [PLANTILLA: pista.]"),
                          kind="success" if _ok else "warn")
    except Exception as _e:
        _res = mo.callout(mo.md(f"Todavía no corre: `{type(_e).__name__}: {_e}`. Completá los `...`."), kind="neutral")
    _res
    return


@app.cell
def _(mo):
    mo.md(r"""
    ## Anexo: dónde está la demostración

    Acá mostré; la demostración está en el apunte:

    - [apunte, sección NN: [título de la sección]](../../apunte.pdf#nameddest=cap:NN)
    - [ficha de la clase N](../../clases/NN.html) · [el hilo conductor](../../index.html) · [unidad anterior](../NN_anterior/index.html)

    [PLANTILLA: los enlaces son relativos a `site/unidades/<id>/index.html`.]
    """)
    return


@app.cell
def _(M_prediccion, area_cuadrado, candidatos, es_rotacion, lib, mo, np, punto):
    # ---------- verificación silenciosa de las cuentas del notebook ----------
    _checks = [
        ("los candidatos de la predicción son distintos entre sí",
         len({tuple(np.round(v, 6)) for v in candidatos.values()}) == len(candidatos)),
        ("la opción correcta coincide con la transformación", lib.exacto(candidatos["correcta"], M_prediccion @ punto)),
        ("rot2(90°) manda e1 a e2", lib.exacto(lib.rot2(np.pi / 2) @ [1, 0], [0, 1])),
    ]
    if es_rotacion:
        _checks.append(("una rotación conserva el área del cuadrado unitario", lib.exacto(area_cuadrado, 1.0, tol=1e-6)))
    assert all(ok for _, ok in _checks), lib.verificar(_checks)
    mo.md(lib.verificar(_checks))
    return


if __name__ == "__main__":
    app.run()
