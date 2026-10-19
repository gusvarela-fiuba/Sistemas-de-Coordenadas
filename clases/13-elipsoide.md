---
clase: 13
titulo: "Clase 13: geometría del elipsoide"
idea: "El elipsoide de revolución es una elipse girada alrededor de su eje menor, y su simetría fija las direcciones principales sin calcular."
que_se_estudia: ["Parametrización del elipsoide en $(\\varphi,\\lambda)$, radios $M$ y $N$", "Primera forma fundamental $ds^2=M^2d\\varphi^2+N^2\\cos^2\\varphi\\,d\\lambda^2$", "Latitud geodésica y geocéntrica", "Simetría: meridiano y primer vertical son direcciones principales, $K=1/(MN)$"]
conceptos_previos: ["Superficie paramétrica y primera forma (clase 9)", "Curvatura y forma cuadrática (clase 12)", "Reflexión como simetría (clase 3)"]
apunte: ["elipsoide"]
unidades: ["13_elipsoide", "15_transformaciones_conformes"]
animaciones: ["05_elipsoide_euler_meusnier", "06_conforme_tissot_mercator"]
ejercicios_sugeridos: ["Calcular $M$, $N$ y las coordenadas $x'$, $z$ a 45° para $a=5$, $b=4$", "Hallar la diferencia entre latitud geodésica y geocéntrica a 45° para GRS80", "Explicar con la simetría por qué en los polos $M=N$"]
---

# Clase 13: geometría del elipsoide

El elipsoide de revolución es una elipse girada alrededor de su eje menor, y su simetría fija las direcciones principales sin calcular.

## Qué se estudia

- Parametrización del elipsoide en $(\varphi,\lambda)$, radios $M$ y $N$
- Primera forma fundamental $ds^2=M^2d\varphi^2+N^2\cos^2\varphi\,d\lambda^2$
- Latitud geodésica y geocéntrica
- Simetría: meridiano y primer vertical son direcciones principales, $K=1/(MN)$

**Elipsoide** (requiere superficie-parametrica, primera-forma-fundamental, curvatura). Escalera: en $\mathbb R^2$ una elipse es una circunferencia estirada en un eje ($x=a\cos t$, $z=b\sin t$); en $\mathbb R^3$ el elipsoide de revolución es esa elipse girada alrededor de su eje menor: todos los meridianos son la *misma* elipse. Parametrización en $(\varphi,\lambda)$: $r=(N\cos\varphi\cos\lambda,\;N\cos\varphi\sin\lambda,\;N(1-e^2)\sin\varphi)$. Lo que se ve: el paralelo de latitud $\varphi$ es una circunferencia de radio $x'=N\cos\varphi$; $N$ es la distancia desde el punto hasta el eje polar *medida a lo largo de la normal*. Primera forma fundamental (sale de $\|\varphi\|=M$ y $\|\lambda\|=x'$): $ds^2=M^2\,d\varphi^2+N^2\cos^2\varphi\,d\lambda^2$. La esfera del apunte v3, $ds^2=R^2d\varphi^2+R^2\cos^2\varphi\,d\lambda^2$, es el caso $M=N=R$.

Latitud geodésica vs geocéntrica: en la esfera la normal pasa por el centro y las dos latitudes coinciden; en el elipsoide la normal *no* pasa por el centro (salvo en ecuador y polos). De la parametrización, $\tan\varphi_{\text{geoc}}=z/x'=(1-e^2)\tan\varphi$: la geocéntrica es siempre menor en módulo. Lo que se ve: la vertical del lugar (la plomada idealizada) apunta más al polo que la línea al centro.

**Simetría** (requiere curvatura). Deducción a partir de la simetría: el plano meridiano es plano de simetría de la superficie (reflejarlo deja el elipsoide igual, clase 3). Entonces la forma cuadrática de la curvatura en un punto es simétrica respecto de la dirección del meridiano, y por la clase 12 sus extremos están a $90^\circ$: las direcciones principales *tienen que* ser meridiano y primer vertical, sin calcular nada. La simetría de revolución agrega que nada métrico depende de $\lambda$: $M$, $N$, $K=1/(MN)$ son funciones de $\varphi$ sola. Tercera consecuencia: en los polos todas las direcciones son meridianos, así que $M=N$ ahí (punto umbilical); en el ecuador $M=b^2/a$ es el mínimo y $N=a$ es el máximo del primer vertical.

Radios de curvatura, lo que se ve: $M$ (meridiano) es el radio del círculo osculador de la elipse meridiana, crece del ecuador al polo; $N$ (primer vertical) es el radio de la sección normal perpendicular al meridiano y también crece. Como $M<N$ en todo punto salvo los polos, el elipsoide es más curvo a lo largo del meridiano que a lo ancho.

## Conceptos previos

- Superficie paramétrica y primera forma (clase 9)
- Curvatura y forma cuadrática (clase 12)
- Reflexión como simetría (clase 3)

## En el apunte

- Geometría del elipsoide (`cap:elipsoide`)

## Unidades interactivas

- Geometría del elipsoide (`13_elipsoide`)
- Transformaciones conformes: números complejos, Jacobiano y del elipsoide al plano cartográfico (`15_transformaciones_conformes`)

## Animaciones

- `05_elipsoide_euler_meusnier`
- `06_conforme_tissot_mercator`

## Ejercicios sugeridos

- Calcular $M$, $N$ y las coordenadas $x'$, $z$ a 45° para $a=5$, $b=4$
- Hallar la diferencia entre latitud geodésica y geocéntrica a 45° para GRS80
- Explicar con la simetría por qué en los polos $M=N$
