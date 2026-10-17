#!/usr/bin/env python3
"""Genera portada-tikz.tex (carátula del apunte Sistemas de Coordenadas).

Sólo figuras, etiquetas mínimas y un hilo en espiral que las recorre (v3, tras "parece un machete"):
monolito 1:4:9 rotado (R_x, R_y, R_z) arriba-izquierda; un mismo punto en cartesianas y esféricas
(R, acimut, latitud) arriba-derecha (ortográfica); cubo unitario -> paralelepípedo A=[v1 v2 v3] con
V = det A y autovector real (centro-izquierda); círculo unidad con e^{i theta} (centro-derecha);
elipsoide de revolución con plano tangente y base local (abajo-derecha).

Proyecciones (viven en TikZ, acá sólo se replican para visibilidad/sombreado):
  portada/proj  oblicua  x->(1,0) y->(.45,.35) z->(0,1)   (figs 1, 2, 4)
  portada/orto  ortográfica, vista az=-60°, el=20°          (fig 3: una esfera se ve redonda)
Regenerar:  python3 gen-portada-tikz.py   (luego lualatex portada-standalone.tex)
"""
import numpy as np, math

# --- proyección oblicua (debe coincidir con portada/proj en el .tex) ---
D = np.array([-0.45, 1.0, -0.35]); D = D / np.linalg.norm(D)      # dirección de vista (entra en la escena)
LIGHT = np.array([-0.35, -1.0, 0.75]); LIGHT /= np.linalg.norm(LIGHT)
# --- proyección ortográfica para la fig. 3 ---
def orto(az_deg, el_deg):
    """base ortográfica: F hacia el observador, R derecha de pantalla, U arriba; D = -F entra en la escena"""
    az,el=math.radians(az_deg),math.radians(el_deg)
    F=np.array([math.cos(el)*math.cos(az), math.cos(el)*math.sin(az), math.sin(el)])
    R=np.cross([0,0,1.0], F); R/=np.linalg.norm(R); U=np.cross(F,R)
    return F,R,U
AZ, EL = -60, 20
F3,R3,U3 = orto(AZ,EL); D3 = -F3                 # fig. 3
F4,R4,U4 = orto(-40,35); D4 = -F4                # fig. 4 (más elevación: se abre el plano xy)
UNIT = 2.2   # cm por unidad en ambas proyecciones

def f(x): return f"{x:.4f}".rstrip('0').rstrip('.') if abs(x) > 1e-9 else "0"
def c3(p): return f"({f(p[0])},{f(p[1])},{f(p[2])})"

out = []
def w(s=""): out.append(s)

# ======================================================================
# Figura 1: monolito 1:4:9 (ancho x=4, espesor y=1, alto z=9), centrado en el origen
# ======================================================================
def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(b): c,s=math.cos(b),math.sin(b); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(g): c,s=math.cos(g),math.sin(g); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
HALF = np.array([2.0, 0.5, 4.5])
def box_faces(R):
    faces=[]
    for axis in range(3):
        for sgn in (-1,1):
            n=np.zeros(3); n[axis]=sgn
            o=[i for i in range(3) if i!=axis]
            quad=[]
            for (s1,s2) in ((-1,-1),(1,-1),(1,1),(-1,1)):
                p=np.zeros(3); p[axis]=sgn*HALF[axis]; p[o[0]]=s1*HALF[o[0]]; p[o[1]]=s2*HALF[o[1]]
                quad.append(R@p)
            faces.append((quad, R@n))
    return faces

def monolito(R, ghost=True, axis=None):
    s=[]
    if ghost:
        for quad,n in box_faces(np.eye(3)):
            if n@D<0:
                s.append("  \\draw[ghost] " + " -- ".join(c3(p) for p in quad) + " -- cycle;")
    if axis is not None:
        a=np.zeros(3); a[axis]=1.0; L=HALF[axis]+2.0 if axis!=2 else HALF[axis]+1.6
        s.append(f"  \\draw[eje] {c3(-L*a)} -- {c3(L*a)};")
    for quad,n in box_faces(R):
        if n@D<0:
            lam=max(0.0,float(n@LIGHT)); dark=int(round(97-26*lam))
            s.append(f"  \\fill[mono, fill=ink!{dark}] " + " -- ".join(c3(p) for p in quad) + " -- cycle;")
    for quad,n in box_faces(R):
        if n@D<0:
            for i in range(4):
                s.append(f"  \\draw[monoedge] {c3(quad[i])} -- {c3(quad[(i+1)%4])};")
    return s

ANG = math.radians(30)
poses=[("x", Rx(ANG), 0, r"R_x(\alpha)", r"\begin{bmatrix}1&0&0\\0&\cos\alpha&-\operatorname{sen}\alpha\\0&\operatorname{sen}\alpha&\cos\alpha\end{bmatrix}"),
       ("y", Ry(ANG), 1, r"R_y(\beta)", r"\begin{bmatrix}\cos\beta&0&\operatorname{sen}\beta\\0&1&0\\-\operatorname{sen}\beta&0&\cos\beta\end{bmatrix}"),
       ("z", Rz(ANG), 2, r"R_z(\gamma)", r"\begin{bmatrix}\cos\gamma&-\operatorname{sen}\gamma&0\\\operatorname{sen}\gamma&\cos\gamma&0\\0&0&1\end{bmatrix}")]

# ======================================================================
# Figura 2: cubo -> paralelepípedo (valores verificados abajo)
# ======================================================================
v1=np.array([1.5,0,0.5]); v2=np.array([0.5,2,0.5]); v3=np.array([0,0,1.5])
A=np.column_stack([v1,v2,v3]); det=np.linalg.det(A)
wv,V=np.linalg.eig(A); i=int(np.argmax(wv.real)); lam=wv[i].real; ev=V[:,i].real; ev=ev/ev.max()
assert abs(lam-2)<1e-9 and abs(det-4.5)<1e-9 and np.allclose(A@ev, lam*ev), (lam,det,ev)
assert np.allclose(ev,[0.5,0.5,1]), ev
# vértices, caras (con normal exterior) y aristas del paralelepípedo, visibilidad genérica
PV={"O":np.zeros(3),"V1":v1,"V2":v2,"V3":v3,"V12":v1+v2,"V13":v1+v3,"V23":v2+v3,"V123":v1+v2+v3}
PF=[("O","V1","V13","V3"),("V2","V12","V123","V23"),      # y=0 / y=1
    ("O","V2","V23","V3"),("V1","V12","V123","V13"),      # x=0 / x=1
    ("O","V1","V12","V2"),("V3","V13","V123","V23")]      # z=0 / z=1
cent=(v1+v2+v3)/2
def face_normal(face):
    p=[PV[k] for k in face]; n=np.cross(p[1]-p[0],p[3]-p[0]); n/=np.linalg.norm(n)
    fc=sum(p)/4
    return n if n@(fc-cent)>0 else -n
pf_vis=[bool(face_normal(fc)@D<0) for fc in PF]
PE=set()
for fc in PF:
    for i in range(4): PE.add(tuple(sorted((fc[i],fc[(i+1)%4]))))
edge_vis={e: any(v and e[0] in fc and e[1] in fc for fc,v in zip(PF,pf_vis)) for e in PE}
assert sum(pf_vis)==3, pf_vis

# ======================================================================
# Figura 3: elipsoide de revolución x²/a²+y²/a²+z²/c²=1, achatado (proyección ortográfica)
# ======================================================================
a_e, c_e = 1.0, 0.90
M=np.diag([1/a_e**2,1/a_e**2,1/c_e**2])
def surf(u,ph): return np.array([a_e*math.cos(u)*math.cos(ph), a_e*math.cos(u)*math.sin(ph), c_e*math.sin(u)])
def normal(p): n=M@p; return n/np.linalg.norm(n)
def vis_pt(p): return normal(p)@D3 < 0
def silhouette(N=90):
    wv=M@D3; wv/=np.linalg.norm(wv)
    p=np.cross(wv,[0,0,1.0]); p/=np.linalg.norm(p); q=np.cross(wv,p)
    pts=[]
    for k in range(N):
        t=2*math.pi*k/N; u=p*math.cos(t)+q*math.sin(t); s=1/math.sqrt(u@M@u); pts.append(s*u)
    return pts
def runs(pts):
    n=len(pts); flags=[vis_pt(p) for p in pts]
    if all(flags): return [(True,pts+[pts[0]])]
    if not any(flags): return [(False,pts+[pts[0]])]
    start=next(i for i in range(n) if flags[i]!=flags[i-1])
    seq=[]; cur=[pts[start]]; curflag=flags[start]
    for k in range(1,n+1):
        i=(start+k)%n
        if flags[i]==curflag: cur.append(pts[i])
        else:
            cur.append(pts[i]); seq.append((curflag,cur)); cur=[pts[i]]; curflag=flags[i]
    seq.append((curflag,cur))
    return seq

uP, phP = math.radians(40), math.radians(-30)
P=surf(uP,phP); assert vis_pt(P)
ru=np.array([-a_e*math.sin(uP)*math.cos(phP), -a_e*math.sin(uP)*math.sin(phP), c_e*math.cos(uP)])
rph=np.array([-a_e*math.cos(uP)*math.sin(phP), a_e*math.cos(uP)*math.cos(phP), 0])
ru_hat=ru/np.linalg.norm(ru); rph_hat=rph/np.linalg.norm(rph)
RU = 0.36*ru_hat
RV = 0.32*(math.cos(math.radians(28))*rph_hat + math.sin(math.radians(28))*ru_hat)
NN = np.cross(RU,RV); NN=0.40*NN/np.linalg.norm(NN)
if NN@normal(P)<0: NN=-NN
assert NN@F3>0, "el observador debe estar del lado exterior del plano tangente"
ang_uv=math.degrees(math.acos(RU@RV/np.linalg.norm(RU)/np.linalg.norm(RV)))
E_,F_,G_ = RU@RU, RU@RV, RV@RV
grid=lambda s,t: P + s*RU + t*RV

# ======================================================================
# Figura 4: un punto en cartesianas (x,y,z) y en esféricas (R, acimut A desde el norte, latitud phi)
# ======================================================================
R_s, A_s, PHI_s = 2.0, math.radians(30), math.radians(50)
dirxy=np.array([math.sin(A_s), math.cos(A_s), 0.0])          # acimut desde y (norte), horario
P4 = R_s*(math.cos(PHI_s)*dirxy + math.sin(PHI_s)*np.array([0,0,1.0]))
P4xy = np.array([P4[0],P4[1],0.0])
LAX=2.4
def panel(spherical):
    s=[]
    s.append(f"  \\draw[ejec] (0,0,0) -- ({LAX},0,0) node[lbl, pos=1, right, text=muted, inner sep=1pt] {{$x$}};")
    s.append(f"  \\draw[ejec] (0,0,0) -- (0,{LAX},0) node[lbl, pos=1, above right, text=muted, inner sep=0.5pt] {{$y$" + (r"{\scriptsize\,(N)}" if spherical else "") + "};")
    s.append(f"  \\draw[ejec] (0,0,0) -- (0,0,{LAX}) node[lbl, pos=1, above, text=muted, inner sep=1pt] {{$z$}};")
    s.append(f"  \\draw[aux] {c3(P4)} -- {c3(P4xy)} -- (0,0,0);")
    if not spherical:
        s.append(f"  \\draw[aux] {c3(P4xy)} -- ({f(P4[0])},0,0)  {c3(P4xy)} -- (0,{f(P4[1])},0);")
        s.append(f"  \\draw[aux] {c3(P4)} -- (0,0,{f(P4[2])});")
        s.append(f"  \\node[lbl, font=\\scriptsize, text=muted, below] at ({f(P4[0])},0,0) {{$x_P$}};")
        s.append(f"  \\node[lbl, font=\\scriptsize, text=muted, right, inner sep=1pt] at (0,{f(P4[1])},0) {{$y_P$}};")
        s.append(f"  \\node[lbl, font=\\scriptsize, text=muted, left, inner sep=1pt] at (0,0,{f(P4[2])}) {{$z_P$}};")
    else:
        ra=0.85; arc=[(ra*math.sin(t), ra*math.cos(t), 0.0) for t in np.linspace(0,A_s,14)]
        s.append("  \\draw[arco] plot[smooth] coordinates {" + " ".join(c3(p) for p in arc) + "};")
        mid=arc[7]; s.append(f"  \\node[lbl, font=\\scriptsize, text=tealdark, below, inner sep=1pt] at {c3(mid)} {{$A$}};")
        rl=1.15; arc2=[rl*(math.cos(t)*dirxy+math.sin(t)*np.array([0,0,1.0])) for t in np.linspace(0,PHI_s,12)]
        s.append("  \\draw[arco] plot[smooth] coordinates {" + " ".join(c3(p) for p in arc2) + "};")
        mid2=arc2[6]; s.append(f"  \\node[lbl, font=\\scriptsize, text=tealdark, right, inner sep=2.5pt] at {c3(mid2)} {{$\\varphi$}};")
    s.append(f"  \\draw[vec] (0,0,0) -- {c3(P4)}" + (" node[pos=.5, sloped, above, font=\\scriptsize, text=rust, inner sep=1.5pt] {$R$}" if spherical else "") + ";")
    s.append(f"  \\fill[ink] {c3(P4)} circle (1.4pt);")
    if spherical:
        s.append(f"  \\node[lbl, etiq, font=\\scriptsize, above right, inner sep=1pt] at {c3(P4)} {{$(R,\\,A,\\,\\varphi)$}};")
    else:
        s.append(f"  \\node[lbl, etiq, font=\\scriptsize, above right, inner sep=1pt] at {c3(P4)} {{$(x_P,\\,y_P,\\,z_P)$}};")
    s.append("  \\fill[ink] (0,0,0) circle (1pt);")
    return s

# ======================================================================
# Emisión del .tex
# ======================================================================
TH = math.radians(40)   # ángulo del círculo unidad de Euler
w("%% portada-tikz.tex — carátula del apunte \"Sistemas de Coordenadas\" (SOLO el tikzpicture).")
w("%% GENERADO por gen-portada-tikz.py (editar el generador, no este archivo).")
w("%% Se incluye con \\input{portada/portada-tikz} desde el principal (colores/fuentes del .sty)")
w("%% o desde portada-standalone.tex. Lienzo: 17.1 x 25.2 cm (área de texto del apunte).")
w("%% Requiere \\usetikzlibrary{arrows.meta,decorations.pathmorphing} (hilo en espiral).")
w("%% Fig. 1: monolito 1:4:9 girado 30° alrededor de x, y, z (proyección oblicua).")
w(f"%% Fig. 2: v1={tuple(v1.tolist())} v2={tuple(v2.tolist())} v3={tuple(v3.tolist())}; det A = {det:.2f}; autovalores {np.round(wv.real,2).tolist()};")
w(f"%%         lambda = {lam:g}, autovector v = ({ev[0]:.4f}, {ev[1]:.4f}, {ev[2]:.4f}) (sobre la cara z=1 del cubo).")
w(f"%% Fig. 3: elipsoide a=b={a_e}, c={c_e} (ortográfica az={AZ}°, el={EL}°); P en u={math.degrees(uP):.0f}°, phi={math.degrees(phP):.0f}°;")
w(f"%%         angulo(r_u,r_v)={ang_uv:.0f}°; E={E_:.3f} F={F_:.3f} G={G_:.3f}.")
w(f"%% Fig. 4: P con R={R_s}, acimut A={math.degrees(A_s):.0f}° (desde el norte, horario), latitud phi={math.degrees(PHI_s):.0f}° (ortográfica az=-40°, el=35°) -> (x,y,z)=({P4[0]:.3f},{P4[1]:.3f},{P4[2]:.3f}).")
w(f"%% Fig. 5: círculo unidad, e^(i theta) con theta={math.degrees(TH):.0f}°.")
w(r"\providecommand{\portadaAutor}{Gustavo Varela}")
w(r"\providecolor{agua}{HTML}{2BB3A3}")
ox=f"({R3[0]*UNIT:.4f}cm,{U3[0]*UNIT:.4f}cm)"; oy=f"({R3[1]*UNIT:.4f}cm,{U3[1]*UNIT:.4f}cm)"; oz=f"({R3[2]*UNIT:.4f}cm,{U3[2]*UNIT:.4f}cm)"
ox4=f"({R4[0]*UNIT:.4f}cm,{U4[0]*UNIT:.4f}cm)"; oy4=f"({R4[1]*UNIT:.4f}cm,{U4[1]*UNIT:.4f}cm)"; oz4=f"({R4[2]*UNIT:.4f}cm,{U4[2]*UNIT:.4f}cm)"
w(r"""\begin{tikzpicture}[
  portada/proj/.style={x={(2.2cm,0cm)}, y={(0.99cm,0.77cm)}, z={(0cm,2.2cm)}},""")
w(f"  portada/orto/.style={{x={{{ox}}}, y={{{oy}}}, z={{{oz}}}}},")
w(f"  portada/orto4/.style={{x={{{ox4}}}, y={{{oy4}}}, z={{{oz4}}}}},")
w(r"""  vec/.style={line width=1.3pt, draw=rust, -{Latex[length=2.8mm,width=2.1mm]}},
  cubo/.style={line width=.5pt, draw=linegray},
  cuboocc/.style={line width=.5pt, draw=linegray, dotted},
  arista/.style={line width=.85pt, draw=tealdark},
  aristaocc/.style={line width=.7pt, draw=tealdark, dotted},
  cara/.style={fill=teal, draw=none},
  ghost/.style={line width=.4pt, draw=linegray, dotted},
  eje/.style={line width=.45pt, draw=muted, dash pattern=on 1.6pt off 1.2pt},
  ejec/.style={line width=.55pt, draw=muted, -{Latex[length=1.8mm,width=1.4mm]}},
  aux/.style={line width=.4pt, draw=linegray, dash pattern=on 1.4pt off 1pt},
  arco/.style={line width=.7pt, draw=tealdark, -{Latex[length=1.6mm,width=1.3mm]}},
  mono/.style={draw=none},
  monoedge/.style={line width=.3pt, draw=ink!55},
  elip/.style={line width=.85pt, draw=teal},
  merid/.style={line width=.45pt, draw=teal},
  meridocc/.style={line width=.35pt, draw=teal!40, dotted},
  plano/.style={fill=paper!93!teal, draw=muted, line width=.5pt},
  grilla/.style={line width=.3pt, draw=linegray},
  hilo/.style={draw=gold!70!paper, line width=.9pt, decorate, decoration={coil, aspect=.35, segment length=2.6mm, amplitude=1.6mm}},
  lbl/.style={font=\small, inner sep=1.2pt},
  etiq/.style={fill=paper, fill opacity=.9, text opacity=1, inner sep=1.4pt},
  every node/.style={text=ink}
]
\useasboundingbox (0,0) rectangle (17.1,25.2);

%% ---------- Título ----------
\node[anchor=west, font=\fontsize{27}{31}\selectfont\bfseries, text=ink] at (0,24.5)
  {Sistemas de Coordenadas};
\node[anchor=west, font=\Large, text=tealdark] at (0,23.35)
  {La geometría es álgebra};
\draw[teal, line width=1.2pt] (0,22.6) -- (17.1,22.6);
\node[anchor=west, font=\normalsize, text=muted] at (0,22.0)
  {Agrimensura \,·\, FIUBA \,·\, 2026};
\node[anchor=west, font=\small, text=muted] at (0,21.4) {\portadaAutor};

%% ---------- Hilo: el recorrido de la materia (detrás de todo) ----------
\draw[hilo] plot[smooth, tension=.8] coordinates
  {(0.5,20.3) (0.7,16.0) (4.5,15.3) (8.9,15.9) (12.2,15.2) (16.7,15.0) (16.85,12.4) (15.9,10.0) (12.5,9.3) (8.0,12.4) (3.5,12.6) (0.6,9.5) (0.5,5.0) (2.2,1.2) (10.2,1.2) (16.5,1.9)};
""")

# ---------- Figura 1 ----------
w("%% ---------- Figura 1 (arriba-izquierda): monolito 1:4:9, giros R_x, R_y, R_z ----------")
XS=[1.6, 4.5, 7.4]; YC=18.55; K=0.16
for (nm,R,ax,lab,mat),xc in zip(poses,XS):
    w(f"\\begin{{scope}}[shift={{({xc}cm,{YC}cm)}}, portada/proj, scale={K}]")
    for s in monolito(R, ghost=True, axis=ax): w(s)
    w("\\end{scope}")
    w(f"\\node[anchor=north, font=\\small, text=ink, inner sep=0pt] at ({xc},{YC-2.05}) {{${lab}$}};")
w()

# ---------- Figura 4 ----------
w("%% ---------- Figura 4 (arriba-derecha): un punto, dos sistemas de coordenadas ----------")
K4=0.6; P4X=[9.9, 13.9]; P4Y=17.15
for spherical,px in zip((False,True),P4X):
    w(f"\\node[anchor=south west, font=\\small, text=tealdark] at ({px-0.3},{P4Y+LAX*K4*UNIT*U4[2]+0.35}) {{{'esféricas' if spherical else 'cartesianas'}}};")
    w(f"\\begin{{scope}}[shift={{({px}cm,{P4Y}cm)}}, portada/orto4, scale={K4}]")
    for s in panel(spherical): w(s)
    w("\\end{scope}")
w()

# ---------- Figura 2 ----------
w("%% ---------- Figura 2 (centro-izquierda): cubo unitario y su imagen por A = [v1 v2 v3] ----------")
OX,OY,K2=2.1,3.3,1.2
w(f"\\begin{{scope}}[shift={{({OX}cm,{OY}cm)}}, portada/proj, scale={K2}]")
for nm,p in PV.items():
    w(f"  \\coordinate ({nm}) at {c3(p)};")
w(f"  \\coordinate (EV) at {c3(ev)};   % autovector")
w(f"  \\coordinate (LEV) at {c3(lam*ev)};   % A v = lambda v")
w(f"  \\coordinate (EXT) at {c3(1.25*lam*ev)};")
w(r"""  % cubo unitario (detrás, tenue)
  \draw[cuboocc] (0,1,0) -- (0,0,0)  (0,1,0) -- (1,1,0)  (0,1,0) -- (0,1,1);
  \draw[cubo] (0,0,0) -- (1,0,0) -- (1,1,0) -- (1,1,1) -- (0,1,1) -- (0,0,1) -- cycle;
  \draw[cubo] (1,0,0) -- (1,0,1) -- (0,0,1)  (1,0,1) -- (1,1,1);
  \node[font=\scriptsize, text=muted, below] at (1,0,0) {$\boldsymbol e_1$};
  \node[font=\scriptsize, text=muted, above left, inner sep=0.5pt] at (0,1,0) {$\boldsymbol e_2$};
  \node[font=\scriptsize, text=muted, left] at (0,0,1) {$\boldsymbol e_3$};
  % paralelepípedo: aristas ocultas, caras visibles (de atrás hacia adelante), aristas visibles""")
for e,v in sorted(edge_vis.items()):
    if not v: w(f"  \\draw[aristaocc] ({e[0]}) -- ({e[1]});")
vis_faces=[(fc,face_normal(fc)) for fc,v in zip(PF,pf_vis) if v]
vis_faces.sort(key=lambda t: -(sum(PV[k] for k in t[0])/4)@D)
for fc,n in vis_faces:
    op=0.14+0.22*max(0.0,float(n@LIGHT))
    w(f"  \\fill[cara, fill opacity={op:.2f}] " + " -- ".join(f"({k})" for k in fc) + " -- cycle;")
for e,v in sorted(edge_vis.items()):
    if v: w(f"  \\draw[arista] ({e[0]}) -- ({e[1]});")
w("  \\node[font=\\fontsize{24}{26}\\selectfont\\bfseries, text=agua] at (1.65,1,1.45) {V};")
w("  \\node[font=\\small, text=agua, anchor=west, inner sep=1pt] at (1.6,1,1.12) {$= \\det A$};")
w(r"""  % generadores (columnas de A)
  \draw[vec, draw opacity=.7] (O) -- (V2) node[lbl, pos=1, below right, text=rust] {$\boldsymbol v_2$};
  \draw[vec] (O) -- (V1) node[lbl, pos=1, below right, text=rust] {$\boldsymbol v_1$};
  \draw[vec] (O) -- (V3) node[lbl, pos=1, left, text=rust] {$\boldsymbol v_3$};
  % recta invariante (autovector real)
  \draw[gold, line width=.55pt, opacity=.85] (O) -- (EXT);
  \draw[gold, line width=1.1pt, opacity=.6, -{Latex[length=2.5mm,width=1.9mm]}] (O) -- (LEV);
  \draw[gold, line width=1.5pt, -{Latex[length=2.7mm,width=2.1mm]}] (O) -- (EV);
  \fill[gold] (EV) circle (1.7pt);
  \fill[gold] (LEV) circle (1.7pt);
  \node[lbl, etiq, above left, text=gold!80!ink] at (EV) {$\boldsymbol v$};
  \node[lbl, etiq, anchor=west, xshift=5pt, text=gold!80!ink] at (LEV) {$A\boldsymbol v = \lambda\boldsymbol v$};
  \fill[ink] (O) circle (1.2pt);
  \node[font=\scriptsize, text=muted, below left, inner sep=1pt] at (O) {$O$};
\end{scope}
""")

# ---------- Figura 5: Euler ----------
w("%% ---------- Figura 5 (centro-derecha): círculo unidad, e^{i theta} ----------")
EX,EY,ER=13.7,12.55,1.45
ct,st=math.cos(TH),math.sin(TH)
w(f"\\begin{{scope}}[shift={{({EX}cm,{EY}cm)}}]")
w(f"  \\draw[ejec] (-{ER+0.35},0) -- ({ER+0.55},0) node[lbl, pos=1, right, text=muted, inner sep=1pt] {{$\\mathrm{{Re}}$}};")
w(f"  \\draw[ejec] (0,-{ER+0.35}) -- (0,{ER+0.55}) node[lbl, pos=1, above, text=muted, inner sep=1pt] {{$\\mathrm{{Im}}$}};")
w(f"  \\draw[elip] (0,0) circle ({ER});")
w(f"  \\draw[aux] ({ER*ct:.4f},{ER*st:.4f}) -- ({ER*ct:.4f},0)  ({ER*ct:.4f},{ER*st:.4f}) -- (0,{ER*st:.4f});")
w(f"  \\draw[arco] ({0.45*ER},0) arc[start angle=0, end angle={math.degrees(TH):.0f}, radius={0.45*ER}];")
w(f"  \\node[font=\\scriptsize, text=tealdark] at ({0.62*ER*math.cos(TH/2):.4f},{0.62*ER*math.sin(TH/2):.4f}) {{$\\theta$}};")
w(f"  \\draw[vec] (0,0) -- ({ER*ct:.4f},{ER*st:.4f});")
w(f"  \\fill[ink] ({ER*ct:.4f},{ER*st:.4f}) circle (1.4pt);")
w(f"  \\node[lbl, etiq, above right, inner sep=1pt] at ({ER*ct:.4f},{ER*st:.4f}) {{$e^{{i\\theta}}$}};")
w(f"  \\node[font=\\scriptsize, text=muted, below] at ({ER*ct/2:.4f},0) {{$\\cos\\theta$}};")
w(f"  \\node[font=\\scriptsize, text=muted, left, inner sep=1pt] at (0,{ER*st/2:.4f}) {{$\\operatorname{{sen}}\\theta$}};")
w(f"  \\node[font=\\scriptsize, text=muted, below left, inner sep=1pt] at ({ER},0) {{$1$}};")
w("\\end{scope}")
w(f"\\node[anchor=north, font=\\large, text=ink] at ({EX},{EY-ER-0.75}) {{$e^{{i\\theta}} = \\cos\\theta + i\\,\\operatorname{{sen}}\\theta$}};")
w()

# ---------- Figura 3 ----------
w("%% ---------- Figura 3 (abajo-derecha): elipsoide de revolución, plano tangente, base local ----------")
CX,CY,SE=13.7,4.3,1.3
w(f"\\begin{{scope}}[shift={{({CX}cm,{CY}cm)}}, portada/orto, scale={SE}]")
sil=silhouette()
w(f"  \\draw[eje] (0,0,{f(-1.35*c_e)}) -- (0,0,{f(1.35*c_e)});")
w("  \\fill[teal, fill opacity=.10] plot[smooth cycle] coordinates {" + " ".join(c3(p) for p in sil) + "};")
curves=[]
for udeg in (-30,0,30,60):
    u=math.radians(udeg); curves.append([surf(u,2*math.pi*k/64) for k in range(64)])
for phdeg in (0,45,90,135):
    ph=math.radians(phdeg); curves.append([surf(2*math.pi*k/64,ph) for k in range(64)])
hid=[];visl=[]
for cv in curves:
    for visf,seg in runs(cv):
        (visl if visf else hid).append(seg)
for seg in hid: w("  \\draw[meridocc] plot[smooth] coordinates {" + " ".join(c3(p) for p in seg) + "};")
for seg in visl: w("  \\draw[merid] plot[smooth] coordinates {" + " ".join(c3(p) for p in seg) + "};")
w("  \\draw[elip] plot[smooth cycle] coordinates {" + " ".join(c3(p) for p in sil) + "};")
rot=[(0.32*math.cos(t),0.32*math.sin(t),1.22*c_e) for t in np.linspace(math.radians(200),math.radians(470),16)]
w("  \\draw[arco, draw=muted] plot[smooth] coordinates {" + " ".join(c3(p) for p in rot) + "};")
G=0.75
corners=[grid(-0.7*G,-0.7*G),grid(1.6*G,-0.7*G),grid(1.6*G,1.6*G),grid(-0.7*G,1.6*G)]
w("  \\fill[plano] " + " -- ".join(c3(p) for p in corners) + " -- cycle;")
for k in (0,G):
    w(f"  \\draw[grilla] {c3(grid(k,-0.7*G))} -- {c3(grid(k,1.6*G))};")
    w(f"  \\draw[grilla] {c3(grid(-0.7*G,k))} -- {c3(grid(1.6*G,k))};")
w(f"  \\draw[vec, line width=1.1pt] {c3(P)} -- {c3(P+RU)} node[lbl, pos=1, above left, text=rust, inner sep=1pt] {{$\\boldsymbol r_u$}};")
w(f"  \\draw[vec, line width=1.1pt] {c3(P)} -- {c3(P+RV)} node[lbl, pos=1, below right, text=rust, inner sep=1pt] {{$\\boldsymbol r_v$}};")
w(f"  \\draw[line width=.9pt, draw=muted, -{{Latex[length=2.4mm,width=1.8mm]}}] {c3(P)} -- {c3(P+NN)} node[lbl, pos=1, right, text=muted, inner sep=1pt] {{$\\boldsymbol n$}};")
w(f"  \\fill[ink] {c3(P)} circle (1.5pt);")
w(f"  \\node[lbl, etiq, below left, inner sep=1pt] at {c3(P)} {{$P$}};")
w("\\end{scope}")
w(r"\end{tikzpicture}")

def proj3(p): return CX+SE*UNIT*(p@R3), CY+SE*UNIT*(p@U3)
pts2=[proj3(p) for p in sil+corners+[P+RU,P+RV,P+NN]]
xs,ys=zip(*pts2); print("fig3 bbox x %.2f..%.2f  y %.2f..%.2f" % (min(xs),max(xs),min(ys),max(ys)))
def proj2(p,ox,oy,k=1.0): return ox+k*(2.2*p[0]+0.99*p[1]), oy+k*(0.77*p[1]+2.2*p[2])
pts=[proj2(p,OX,OY,K2) for p in list(PV.values())+[1.25*lam*ev]]
xs,ys=zip(*pts); print("fig2 bbox x %.2f..%.2f  y %.2f..%.2f" % (min(xs),max(xs),min(ys),max(ys)))
open("portada-tikz.tex","w").write("\n".join(out)+"\n")
print("ok  det=%.3f lam=%g ev=%s  caras visibles=%s  ang(ru,rv)=%.1f" % (det,lam,np.round(ev,4),pf_vis,ang_uv))
