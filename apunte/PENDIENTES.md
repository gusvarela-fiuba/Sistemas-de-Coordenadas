# Pendientes registrados durante la revisión editorial

Tareas sobre unidades interactivas, datos o material que un capítulo necesita y todavía no existe. Una línea por tarea; se tacha al resolverla.

- [ ] Unidad `09_cambio_de_base_svd`: los deslizadores van de −4 a 4 y no permiten armar A = [[3,0],[4,5]] del ejemplo del capítulo 7. Agregar un caso precargado con esa matriz y una capa con las curvas de nivel ‖Ax‖ = c en el plano de entrada (simulación de comprobación del ejemplo 7.4). Origen: fase C, capítulo 7.
- [ ] Unidad de traslaciones y movimientos rígidos: líneas coordenadas (grilla cartesiana y polar) y composición de traslación con rotación (orden, punto fijo c′=(I−R)⁻¹v), más el pasaje local→obra de una poligonal con deslizadores de Az₀ y E. Origen: fase B, capítulo 2.
- [ ] Material de los capítulos 12 a 15 en preparación: vive en el repositorio privado `sistemas-de-coordenadas-fuentes/apunte/preparacion/` hasta que se desarrolle en el curso.

## Revisión semántica 2026-10-19

- [ ] Cap. 14 (menor): notación de M, N (radios) y de ψ, β (latitudes) ausente de la tabla del capítulo 0; agregar filas y la advertencia «N es el radio, no el norte». `semantica_14.md` #7.
- [ ] Cap. 14 (menor): bibliografía del capítulo sin fuentes de geodesia ni de GRS80/WGS84 (sólo Efimov y Sáenz). `semantica_14.md` #6.
- [ ] Cap. 14 (menor): la frase «simétricos» de la línea 540 no coincide con la tabla (2281/2275 ppm contra 2288 ppm). `semantica_14.md` #5.
- [ ] Cap. 14 (menor): el recuadro de la línea 51 dice «cerca del polo»; la proposición dice «en los polos». `semantica_14.md` #4.
- [ ] Unidad 13 (menor): formato «1,852.20 m» de los números vivos contra «1 852,20 m» del recuadro. `semantica_14.md` #8.
- [ ] Cap. 15 (menor): la letra N nombra el polo norte (línea 431) y el radio del primer vertical (línea 556); renombrar el polo (P_N) y desambiguar en las convenciones. `semantica_15.md` #1.
- [ ] Cap. 15 (menor): ψ designa la latitud isométrica en la línea 523, pero es la geocéntrica en el capítulo 14 y C2 usa q; cambiar a q. `semantica_15.md` #2.
- [ ] Cap. 15 (menor): polar del polar sin probar que el polar tiene det>0; región del triángulo sin precisar; coma colgada en el enunciado de Legendre. `semantica_15.md` #3 a #5.
- [ ] Cap. 15 (menor): pyproj usa Karney, no Vincenty (línea 566); tolerancia con denominadores distintos (e² contra (N−M)/M, líneas 567-568); «no hay fórmulas cerradas» (línea 554). `semantica_15.md` #6, #7, #9.
- [ ] Cap. 15 (menor): ejercicio de ángulos de 100° pregunta «solución única» en el plano, donde no existe solución; reformular. `semantica_15.md` #8.
- [ ] Cap. 15 (menor): bibliografía sin fuentes de trigonometría esférica ni geodesia; la unidad 14 remite a Coxeter para una demostración que el capítulo ya da. `semantica_15.md` #10.
- [ ] Unidad 14 (menor): referencias a secciones y fichas viejas («Polígonos geodésicos…», «Maxima (unidad 14)», «el apunte sobre el elipsoide»); y «22″ del orden de un teodolito» en el ejercicio (b). `semantica_15.md` #11, #13.
- [ ] Cap. 15 (menor): recuadros de las líneas 107 y 379 («crecen a la vez», «centésimas de grado»); α contra Az del capítulo 0. `semantica_15.md` #12, #14.


Menores detectados (detalle, cita y propuesta en `apunte/revision/semantica_<cap>.md`).

- [resuelto] Cap. 5 `05-formas-lineales.tex:396`: la frase «mueve las mediciones de la misma manera en que A mueve los puntos, pero en sentido contrario» confunde `A^T` (retrotrae) con `A^{-T}` (acompaña al punto); reformular.
- [ ] Cap. 5 `05-formas-lineales.tex:492`: la matriz de cambio de base se llama `P` (también en `prop:co-contra`) pero el capítulo 0 fija `C_{e←b}`; unificar o declarar.
- [ ] Cap. 5 `05-formas-lineales.tex:447,470,508`: traslación `c` en `x'=Ax+c`; el capítulo 0 fija `f(x)=Ax+b`.
- [ ] Cap. 5 `05-formas-lineales.tex:387-456`: `\langle\cdot,\cdot\rangle` no figura en la tabla de notación del capítulo 0 (sólo `u\cdot v`).
- [resuelto] Cap. 5 `05-formas-lineales.tex:501`: «sólo cuando A es una rotación» debería decir ortogonal (rotación o reflexión) o ortogonal por escala común.
- [resuelto] Cap. 6 `06-subespacios-cuna-determinante.tex:307`: la proposición (b) dice «sii coplanares (linealmente dependientes)» y la demostración no prueba «coplanares ⇒ dependientes» ni define coplanar (plano por el origen).
- [ ] Cap. 6 `06-subespacios-cuna-determinante.tex:353-378` y `ex:cuna-mixto-losa`: la decisión depende del plano de referencia (tres puntos); contra el plano de ajuste los residuos son ±0,79 mm y ±2,04 mm (el ejercicio daría «coplanares»); aclararlo.
- [ ] Cap. 6 `06-subespacios-cuna-determinante.tex:279,280,329,375`: norma escrita `\lvert\cdot\rvert`; el capítulo 0 declara `\lVert\cdot\rVert`.
- [ ] Cap. 6 `06-subespacios-cuna-determinante.tex:303`: «el cuña de 2×2» debería ser «el menor de 2×2».
- [resuelto] Cap. 7 `07-autovalores-autovectores.tex:410`: `prop:traza-det` se demuestra sólo para n=2,3 y la parte nueva la usa con n=4 (proyector de la recta por cuatro puntos); demostrar el caso general por coeficientes de `det(λI-A)`.
- [ ] Cap. 7 `07-autovalores-autovectores.tex:~660-700` y ejercicio: dilatación de 24,7 µε y desplazamientos de 30-57 mm en 2,5 km son poco verosímiles para la Pampa húmeda sin causa (sismo, subsidencia); agregar causa o reducir la escala.
- [ ] Cap. 7 `07-autovalores-autovectores.tex:693,699`: `E` es tensor de deformación y coordenada Este en la misma página; `ε` es parámetro pequeño y `με` unidad; `e_1,e_2` por `λ`; renombrar el tensor.
- [ ] Cap. 7 `07-autovalores-autovectores.tex:518,524`: «una rotación pequeña es I+εA» sólo vale a primer orden; «En una línea» anuncia una justificación de varias líneas.
- [ ] Cap. 10 `10-derivada-aproximacion-lineal.tex:507`: la subsección de la divergencia no tiene `\label` (proponer `sec:divergencia` y citarla en `tab:operaciones`).
- [ ] Cap. 10 `10-derivada-aproximacion-lineal.tex:525`: «nula, sólo se deforma o gira sin cambiar de área» vale sólo a primer orden; enlazar el ejemplo de traza cero del capítulo 7.
- [ ] C1 `c1-proyectivas.tex:278-281,293-298`: la invarianza de la razón doble se usa con un punto impropio y ni la definición ni `prop:c1-razon-doble` lo cubren; agregar la convención `(a,b;c,∞)=(c-a)/(c-b)` y la extensión por continuidad.
- [ ] C1 `c1-proyectivas.tex:274-277`: «el punto medio y el punto impropio son conjugados armónicos» sin «respecto de A y B» y con evidencia sólo numérica; dar el límite `(c-a)/(c-b)=-1`.
- [ ] C1 `c1-proyectivas.tex:264-265`: «existe y es único» falla en la recta afín si C es el punto medio; decir «en la recta proyectiva».
- [ ] C1 `c1-proyectivas.tex:245,84`: «toda homografía que deja fija la recta ideal es una afinidad» sin demostración (una línea: `h31=h32=0`); título «único invariante numérico» sobreafirma.
- [ ] C1 `c1-proyectivas.tex:277,304,319` y figura: decimales con punto (resto del apunte, con coma); `L` es punto pero en el capítulo 0 es recta; «tres ideas distintas» (línea 338) choca con `c2-conformes.tex:217`.
- [ ] C2 `c2-conformes.tex:233`: «sección~0» escrita a mano y «hoja cuadriculada» sin definición en ninguna parte; referencia colgante.
- [ ] C2 `c2-conformes.tex:307-309,86`: remisión doble «sección~\ref{cap:elipsoide} (capítulo~\ref{cap:elipsoide})» y «puntapié inicial» entrecomillado (suena a atribución de fuente); reformular.
- [ ] C2 `c2-conformes.tex:176-218`: `J(z)` choca con la jacobiana `J`; `S` para la reflexión vs `σ_L` del capítulo 0; el «recíprocamente» de «analítica con f'≠0» requiere diferenciabilidad y `detJ>0`.
- [resuelto] Cap. 12 `12-cuatro-problemas.tex:546` (GRAVE): `dN/dE=1{,}131240` debe ser `1{,}132311` (S_EN/S_EE; el script lo imprime).
- [resuelto] Cap. 12 `:553`: «la total queda en el medio» se usa sin demostración (el enunciado de `prop:cp-dos-regresiones` sólo compara las dos simples); agregar la cuenta con `S_xy t²+(S_xx−S_yy)t−S_xy=0` (ver `revision/semantica_12.md` n.º 2).
- [ ] Cap. 12 `:100-135,343-352`: hipótesis omitidas (S_xx,S_yy>0 y S_xy≠0; λ₁>λ₂ para recta total única; σ₂>0 y caso σ₁=σ₂ con det=−1 da s=0).
- [ ] Cap. 12 `:132-134,176,214,695-700`: autovalores λ₁,λ₂ (el cap. 0 asigna μ a los caps. 12–15) y escala λ en l.214 vs s en l.464; `:592-596` coeficientes D,E,F del círculo chocan con coordenadas (E,N); `C` dispersión vs `C` cambio de base.
- [ ] Cap. 12 `:169,270,282,450,522,558`: «el script» en la prosa (dejar la ruta sólo en pies de figura); `:375-397` unidades del ejemplo Procrustes sin declarar (metros); `:237` sesgo del círculo algebraico en arcos cortos sin demostración; `:568` origen de σ₀/σ₁ sin explicar.
- [resuelto] Unidad `11_cuatro_problemas` `:44,605-611`: firma de autor, referencias a secciones del apunte inexistentes y «ficha de la clase 11»; notación `H=P₀ᵀQ₀, R=VUᵀ, p₀ᵢ` distinta de la del capítulo (`M=B₀ᵀA₀, R=UVᵀ, aᵢ′`).
- [ ] Cap. 13 `13-curvatura.tex:633`: «mismo orden de magnitud» es falso en la vaguada (0,211 vs 1,259); reformular.
- [resuelto] Cap. 13 `:547,659` y `datos/dem_copernicus/README.md`: falta la atribución exigida por las condiciones de uso y atribución del Copernicus DEM («© DLR e.V. 2010-2014 y © Airbus Defence and Space GmbH 2014-2018, provistos bajo COPERNICUS por la UE y la ESA»); no aparece en ninguna parte del apunte.
- [ ] Cap. 13 `:557-593`: advertir que un radio menor que la ventana (70 m frente a 157×185 m, rms 5–7 m) es una curvatura a escala de ventana, no un círculo osculador del terreno.
- [ ] Cap. 13 `:537` usa WGS84 y el cap. 0 y el cap. 14 usan GRS80; `:693` consigna «sin derivar la hélice» contradice la solución; `:20,448,489,560` colisiones de letras (H hessiano/curvatura media, C jacobiano/centro C_n, d,e,f del DEM); `:241` nombrar «operador de forma» a S=I⁻¹II; `:641` signo de la curvatura del perfil en Meusnier.
- [resuelto] Unidad `12_curvatura` `:45,489-499`: firma de autor, «errata confirmada», «ficha de la clase 12» y secciones del apunte que no existen en el cap. 13 («Prueba 1», «Prueba 2», «Fórmula de Euler y radio medio»).
- [ ] Cap. 0 `00-antes-de-empezar.tex:216-217`: «En preparación» en los capítulos 12 y 13, ya completos.
- [resuelto] Cap. 9 `09-cambio-de-base.tex:396`: «(0,86; 0,43)» contradice el (0,870; 0,435) de la línea 390 (número que no coincide; ver `revision/semantica_09.md`, grave 1).
- [ ] Cap. 9 `:24-26,262-264,417-420,473-475,499-501`: letras C, P, A, M, T (y B en la unidad 08) para la misma matriz; «convención ya fijada» (262) remite a la sección 332, posterior. Unificar en C y M.
- [ ] Cap. 9 `:879-880` «no es la matriz de ninguna forma cuadrática» (una no simétrica sí define x^T M x); `:768` cifras redondeadas dan 1,4160 y no 1,4150; `:563-564` «columnas ortonormales (como ocurre para M simétrica)»; `:970` «misma signatura» para una matriz no simétrica; `:959-963` voseo en un ejercicio; `:146,810,849` «inversible».
- [ ] Cap. 9 `:896-900`: la regla K^T(J^TJ)K se prueba en `prop:II-congruencia` (cap. 13), no en el cap. 10; `:825-827`: celdas «gradiente de la cota», «afinidad entre dos sistemas», «elipse de error» sin respaldo en el capítulo.
- [ ] `scripts/cap09_congruencia.py` no corre en CI (sólo `pytest apunte/demostraciones`): crear `demostraciones/cap09_cambio_de_base.py` con `test_prop_congruencia_ortogonal` (SIMBOLICA) y un CONTRAEJEMPLO, y poner `\comprobacion` tras `prop:congruencia-ortogonal` y tras el contraejemplo.
- [ ] Cap. 11 `:213,227`: voz de clase («podríamos llamar», «no me mueve»); `:166-168` mostrar el cofactor de una cuña; `:185-187` «entradas enteras» requiere A entera; `:476` la consigna dice P⁺ y el capítulo llama C a esa matriz.
- [ ] Cap. 0 `:869` `C_{e←b}` frente a `C_{b→e}` del cap. 9; `:424` y `:651` usan B y P; `:577` id `00_desaprender_el_cbc` inexistente (es `00_fundamentos`); `:206` fila 2 lista 01c, el cap. 2 usa 01b; `:216-219` «En preparación» también en 14 y 15.
- [ ] Cap. 0 `:76-77` «Las proposiciones y los teoremas llevan… un recuadro» (hoy 6 de 89); `:891-892` «cada celda remite a la sección donde se demuestra» no vale para la columna de usos (varios están en otro capítulo, ver `revision/semantica_00.md`, menor 7); `:109` «Mapa conceptual» sin leyenda y bajo «unidades interactivas»; `:971` «Similaridad» sin «(semejanza de figuras)»; `:31`, `:571` alusiones a versiones previas.
- [ ] Cap. 2 / demostraciones: `prop:det-factor` sin demostración (ver grave en `revision/semantica_02_demostraciones.md`); menores: `prop:det-producto` general vs n=2,3; `prop:area-poligono` sin comparar con un área independiente (Herón); `prop:puntos-fijos` sólo punto (3) y podría ser SIMBOLICA; `02:268` traslación nula; consignas de las unidades 01b (`02:572`, «alrededor del centro») y 03 (`02:574`).
