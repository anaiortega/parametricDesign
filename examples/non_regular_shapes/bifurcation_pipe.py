# -*- coding: utf-8 -*-
import math
import Part,
from FreeCAD import Vector
from layout_utils import views 

docGeom=App.newDocument('pipeBifurc3D','pipeBifurc3D')
#Datos
L1=5000
L2=6490
L3=13787
L4=6000
Ang=80
D1=6000
D2=5500
D3=3900
D4=3700
R1=4570
R2=2860
escala=0.1 #escala para planos
#fin datos

tramo1=Part.makeCone(D1/2,D2/2,L1,Vector(0,0,0),Vector(1,0,0))
pieza=tramo1

tramo2=Part.makeCylinder(D2/2,L2,Vector(L1,0,0),Vector(1,0,0))
pieza=pieza.fuse(tramo2)

tramo3=Part.makeCone(D2/2,D3/2,L3,Vector(L1+L2,0,0),Vector(1,0,0))
pieza=pieza.fuse(tramo3)


centroToro=Vector(L1+L2,D2/2+R1,0)
vdirToro=Vector(0,0,1)
tramo4=Part.makeTorus(R1+D3/2,D3/2,centroToro,vdirToro,0,360,Ang)
tramo4.rotate(centroToro,vdirToro,-90)


pieza=pieza.fuse(tramo4)
Part.show(pieza,'pieza')

Xinic=L1+L2
Ypto=3*D1
Zpto=-3*D1
intervaloX=500
Lplano=10*D1
WPlano=10*D1
vDir=Vector(1,0,0)

i=14
plano=Part.makePlane(Lplano,WPlano,Vector(Xinic+i*intervaloX,Ypto,Zpto),vDir)
inters=pieza.common(plano)
Part.show(inters,'inters')

views.basic_views(docGeom=docGeom,title='bifurcation',lstObjects=[docGeom.pieza,docGeom.inters],scale=0.01,pageTemplate='A1_Landscape_blank.svg')

# Pages templates are in directory /usr/share/freecad-daily/Mod/TechDraw/Templates/

