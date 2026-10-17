---
clase: "NN"            # id del esqueleto del profesor (01..14; 03p = proyectivas 2C2026)
titulo: ...
fecha_2025: "2025-MM-DD"   # sólo si el campus la da; si no, null
fecha_2025_estimada: "2025-MM-DD"   # OPCIONAL: estimación (ritmo semanal, fechas de archivos) cuando fecha_2025 es null
fechas_2026: ["2026-MM-DD"]  # miércoles de la cursada actual que cubren esta clase; [] si no se dictó aún
estado: con-transcripcion   # con-transcripcion | reconstruida | no-dictada | anticipada
fuentes:
  - fuentes/campus/resumenes_clase_2025_profesor.md#clase-N
  - fuentes/transcripciones/2026-MM-DD.md
conceptos: [id1, id2]       # ids de mapa/CONCEPTOS.md
apunte: ["07", "14"]        # prefijos de apunte/contenido/
unidad: 01_rotaciones       # o null
---

# Clase N — Título

> **Estado:** con transcripción del miércoles 2026-MM-DD / **reconstruida sin transcripción** a partir del resumen 2025, el apunte y la bibliografía / no dictada todavía en 2C2026.

## El hilo del profesor (cursada 2025)
Qué quiso que viéramos, en el orden en que lo contó. Citas textuales del resumen del campus entre comillas, con la etiqueta *(profesor, resumen 2025)*.

## Lo que pasó en 2C2026
Qué se hizo en el/los miércoles de este año: ejercicios dados, ejemplos numéricos con los números reales, tareas pedidas, frases del profesor (marcadas *(transcripción auto-traducida)* si vienen del transcript en inglés). Si no hay transcripción: qué se infiere de las fuentes y una lista explícita de lo que falta confirmar.

## Hecho geométrico
Para cada concepto de la clase, un par "lo que dice el álgebra ↔ lo que se ve". Escalera R → R² → R³ → Rⁿ cuando aplique. Nivel: alumno que viene del CBC. Sin teoremas formales; la pregunta antes que la fórmula.

## Cuentas chicas
Uno o dos ejemplos con enteros, a mano, que el alumno pueda reproducir en el cuaderno (y la verificación en Excel/GeoGebra/marimo que usaría el profesor).

## Dónde está desarrollado
- Apunte: secciones (`apunte/contenido/NN-*.tex`) con qué cubre cada una.
- Unidad marimo: archivo y estado (existe / pendiente).
- Bibliografía del campus: título y comentario textual del profesor, tomado de `00_bibliografia_campus_comentarios_profesor.md`.
- Material de clase del profesor (Excel, wxMaxima, GeoGebra) si existe.

## Enlaces del mapa
- Viene de: conceptos previos que la motivan.
- Lleva a: conceptos que se apoyan en esta clase.
- Qué se conserva: la pregunta guía del profesor para esta transformación/operación.

## Huecos y dudas
Lo que no cierra o falta (diferencias entre fuentes, ejercicios sin enunciado, cosas a preguntar en clase).
