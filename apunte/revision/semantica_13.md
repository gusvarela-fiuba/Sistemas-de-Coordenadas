# Revisión semántica — capítulo 13 «Curvatura como forma cuadrática» (2026-10-19)

Archivos revisados: `contenido/13-curvatura.tex`, `scripts/cap13_curvatura.py`, `unidades/12_curvatura.py`, `datos/dem_copernicus/README.md`.

**Resumen:** demostraciones de Euler, Meusnier y cambio de parámetros correctas y sin saltos; más de 60 números cotejados con el script (tabla del DEM, ejemplos, ejercicios, ventanas, porcentajes de celdas) y todos coinciden; ningún grave, sólo menores de redacción, notación, atribución de datos y procedencia en la unidad.

Verificaciones hechas: salida completa del script; paraboloide en (1,2) a mano (\(S=\tfrac1{27}\bigl(\begin{smallmatrix}10&-1\\-4&4\end{smallmatrix}\bigr)\), \(\kappa=(7\pm\sqrt{13})/27\), \(d_1^TId_2=0\)); esfera (normal exterior = \(r_\lambda\times r_\varphi\) normalizada, \(II=-I/R\)); cilindro; Meusnier en el paraboloide (\(1/\cos40^\circ=1{,}30541\)); ejercicios `ex:curv-*` (autovalores, \(-3\pm\sqrt{34}\), acimut \(15{,}5^\circ\)); tabla del DEM (pendientes, acimutes de bajada, \(K=\kappa_1\kappa_2\), \(H\), radios, \(\theta=8{,}0^\circ,87{,}2^\circ,85{,}7^\circ\) y Euler \(-2{,}410;0{,}211;-6{,}035\)); \(M\), \(N\), pasos de grilla de \(1''\) (\(30{,}80\) y \(26{,}19\) m); los tres recuadros contra `12_curvatura.py` (silla en (0,0); cilindro con \(x_0=0\); esfera \(K=0{,}16\); en «loma: terreno suave» \(K\) cambia de signo dentro de \([-1,1]^2\), calculado en grilla de \(0{,}1\)).

## Hallazgos

### Graves

Ninguno.

### Menores

1. **menor — afirmación que el número no sostiene.** `13-curvatura.tex:633`: «Tiene el mismo signo y el mismo orden de magnitud, con diferencias de \(1\) a \(2\) 1/km». En la vaguada el perfil del DEM da \(1{,}259\) y la cuadrática \(0{,}211\): seis veces más, y la diferencia (\(1{,}05\)) es del tamaño del valor mismo. Propuesta: «Tiene el mismo signo; la diferencia es de \(1\) a \(2\) 1/km, que en la vaguada (\(0{,}211\) contra \(1{,}259\)) es mayor que el valor mismo».

2. **menor — atribución de datos (licencia).** `13-curvatura.tex:547-548,659-660` y `datos/dem_copernicus/README.md`: el README exige atribución («uso libre con atribución») y el apunte no la incluye en ninguna parte (tampoco en el complemento C3). Propuesta: agregar al pie de la figura `fig:curv-dem` (o al párrafo «El dato»): «Contiene datos de Copernicus DEM GLO-30, © DLR e.V. 2010-2014 y © Airbus Defence and Space GmbH 2014-2018, provistos bajo COPERNICUS por la Unión Europea y la ESA».

3. **menor — validez de la cuadrática local.** `:557-562,593`: los radios de \(70\) y \(72\) m son menores que la ventana (\(157\times185\) m) y el residuo rms del ajuste es de \(5\) a \(7\) m, comparable a la exactitud vertical del DEM. El texto dice que «la ventana es parte del resultado», pero no advierte que un radio menor que la ventana ya no describe un círculo osculador del terreno sino una curvatura promedio. Propuesta: una oración tras la tabla: «un radio menor que la ventana indica curvatura a la escala de la ventana, no un círculo que bese al terreno».

4. **menor — consigna que contradice su solución.** `:693-695` (ejercicio `ex:curv-helice`): «sin derivar la hélice», pero la solución deriva \(\gamma'\) y \(\gamma''\) (necesita \(\gamma''\) para ver que \(\varphi=0\)). Propuesta: «sin calcular el producto vectorial» o «usando sólo la tangente y el hecho de que \(\gamma''\) apunta al eje».

5. **menor — elipsoide de referencia.** `:537`: M y N con WGS84; el capítulo 0 (tabla de notación) y el capítulo 14 (`:76-82`) trabajan con GRS80 y declaran que «los números del capítulo son de GRS80». La diferencia es de \(0{,}1\) mm, pero el lector ve dos elipsoides. Propuesta: «con GRS80 (idéntico a WGS84 a este nivel)» y recalcular o citar la nota de 14:79-82; el script usa constantes WGS84 (`A_WGS`, `F_WGS`).

6. **menor — notación frente al capítulo 0.** (a) `:20,294`: \(H\) es la curvatura media; en el glosario del capítulo 0 (l.922) \(H\) es el hessiano. Propuesta: una frase en las convenciones («\(H\) es la curvatura media; la hessiana se escribe con palabras o \(\nabla^2h\)»). (b) `:489-490`: \(C\) es aquí el jacobiano del cambio de parámetros; coincide con \(C_{b\to e}\) de la tabla de la sección de cambios de base (\(\tilde I=C^TIC\) es la fila de formas cuadráticas), pero no lo dice. Propuesta: «\(C=C_{(s,t)\to(u,v)}\) en la notación del capítulo~\ref{cap:cambio-base}». (c) `:448`: \(C_n\) (centro de la osculadora) colisiona con ese mismo \(C\); renombrar \(Z_n\) o \(c_n\). (d) `:560`: los coeficientes \(d,e,f\) del DEM colisionan con \(d\) (paso) y \(e\) (autovector unitario en la demostración de l.267).

7. **menor — nombre del objeto.** `:241,275-282`: el capítulo 0 (l.655) llama a \(I^{-1}II\) «operador de forma», y el capítulo 13, que es donde se define, sólo lo llama \(S\). Propuesta: «\(S=I^{-1}II\) (el \emph{operador de forma})» en el teorema `teo:euler`.

8. **menor — hecho no explicitado.** `:186-188`: se afirma que la normal principal de la sección normal es \(\pm n\) «por estar en su plano y ser perpendicular a la tangente»; vale, pero sólo donde \(\kappa\neq0\). Propuesta: agregar «(si la sección tiene curvatura nula, \(\kappa_n=0\) y no hay normal principal; la identidad \(\gamma''\cdot n=II(d)\) sigue valiendo)».

9. **menor — signo de la curvatura del perfil.** `:641-646` (Meusnier a lo largo de la curva de nivel): se multiplica la segunda derivada del perfil con signo (\(-14{,}398\)) por \(\cos\varphi=1/W\), pero el teorema de l.428-434 define \(\varphi\) entre \(\nu\) y \(n\) con \(\kappa>0\). Con \(\kappa<0\) (loma) \(\nu\) apunta hacia abajo y el ángulo es \(180^\circ-\) pendiente. Propuesta: aclarar «con la convención de signo de l.35: \(\kappa=z''\), positiva si la curva se dobla hacia arriba».

10. **menor — consigna de recuadros (todas factibles).** `:59` (silla, punto (0,0), \(\alpha\) de \(0^\circ\) a \(90^\circ\)): el control \(\alpha\) llega a \(180^\circ\) en pasos de \(5^\circ\) y a \(45^\circ\) \(\lvert\kappa_n\rvert<0{,}06\) quita el círculo; correcto. `:419` (cilindro \(x_0=0\), esfera): correcto, pero conviene decir que en el cilindro \(\kappa_1=0{,}4\) vale sólo con \(x_0=0\) (ya lo dice) y que el control arranca en \(x_0=0{,}4\). `:667` (loma suave): \(K\) cambia de signo, \(F\) y \(M\) valen cero sobre los ejes y dejan de serlo fuera de ellos; correcto.

11. **menor — procedencia en la unidad asociada.** `unidades/12_curvatura.py:45` firma «Gustavo Varela»; `:489-499` remite a «apunte, sección “Curvatura: de la curva plana a la forma cuadrática”», a «Prueba 1», «Prueba 2», «con su errata confirmada», al resultado «Fórmula de Euler y radio medio (\(R=\sqrt{R_1R_2}\))», al «apunte *Geometría del Elipsoide y cálculos Geodésicos*» y a la «ficha del capítulo 13». Ninguno de esos nombres existe en el capítulo 13 (secciones: «La segunda forma fundamental», «Curvaturas principales…», «El teorema de Meusnier», …) y varios son procedencia de curso. Propuesta: reemplazar la lista por enlaces a `sec:segunda-forma`, `teo:euler`, `teo:meusnier`, `prop:II-congruencia` y eliminar «errata», «capítulo 13» y la firma.

12. **menor — estado en el capítulo 0.** `00-antes-de-empezar.tex:216-217` marca los capítulos 12 y 13 con «En preparación» aunque ya están completos con unidad interactiva, y `PENDIENTES.md` (tercer ítem) dice que el material de los capítulos 12 a 15 vive en un repositorio privado. Propuesta: coordinar con quien mantenga el capítulo 0 la columna «Observaciones».

13. **menor — README de datos.** `datos/dem_copernicus/README.md`: describe el recorte «para notebook SVD», fecha («Recon 2026-09-21») y alternativas descartadas; no menciona su uso en este capítulo (cuadráticas locales \(7\times7\), curvatura). Los datos que el capítulo cita (celdas, latitud/longitud, cotas \(1014\)–\(2989\) m, \(512\times512\)) coinciden con el README. Propuesta: agregar una línea «usado en los capítulos 13 y C3» y quitar la fecha de reconocimiento si el README se publica.

## Graves del capítulo 13

- Ninguno.
