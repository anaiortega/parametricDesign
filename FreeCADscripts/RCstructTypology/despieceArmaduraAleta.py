# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCADcivilOrt 
from freeCADcivilOrt import Arma2d
from FreeCAD import Base
from Draft import *

# Aleta 1, muro 1, PI+PF+OD 103.52
# DATA
#   Zapata
bZap=5.05 #ancho zapata
lZap=6.20 #longitud zapata
eZap=0.90 #espesor de la zapata
recNominal=0.06
hTextosArmados=0.125
bPuntera=1.45  #ancho de la puntera

#  Muro (intradós=cara visible, trasdós= cara en contacto con tierras)
eCoron=0.30  #espesor del muro en coronación
hMurMax=
hMurMin=
pendTrasdos=1/15.  #pendiente del trasdós (H/V)

#  Armados zapata
# armadura transversal inferior
fi_Z1_1=0.025
s_Z1_1=0.25
rdob_Z1_1=0.03
# armadura transversal superior
fi_Z1_2=0.025
s_Z1_2=0.15
rdob_Z1_2=0.03
# armadura longitudinal inferior
fi_Z1_3=0.016
s_Z1_3=0.20
rdob_Z1_3=0.03
# armadura longitudinal superior
fi_Z1_4=0.016
s_Z1_4=0.20
rdob_Z1_4=0.03
# armadura lateral talón
fi_Z1_7=0.016
s_Z1_7=0.25
rdob_Z1_7=0.03
# armadura lateral puntera
fi_Z1_8=0.016
s_Z1_8=0.25
rdob_Z1_8=0.03



# END DATA
#Puntos sección longitudinal
Pl1=Base.Vector(0,0)
Pl2=Base.Vector(0,eZap)
Pl3=Base.Vector(lZap,eZap)
Pl4=Base.Vector(lZap,0)

#Puntos sección transversal
Pt1=Base.Vector(0,0)
Pt2=Base.Vector(0,eZap)
Pt3=Base.Vector(bZap,eZap)
Pt4=Base.Vector(bZap,0)

Pt2p=Base.Vector(0,eZap/2.0)
Pt3p=Base.Vector(bZap,eZap/2.0)

familiasArmad={}
# armadura transversal inferior
Z1_1=Arma2d.rebarFamily(identificador='Z1/1',
                 diametro=fi_Z1_1,
                 separacion=s_Z1_1,
                 lstPtosConcrSect=[Pt2,Pt1,Pt4,Pt3],
                 listaRec=[recNominal,recNominal,recNominal],
                 lado='i',
                 radioDob=rdob_Z1_1,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,-0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pl1,Pl4],
                 recSec=recNominal,
                 recLateral=recNominal,
                 ladoDibSec='i',
                        vectorLRefSec=Base.Vector(-0.3,0.3),
                 lstPtosConcrSect2=[Pt2p,Pt1,Pt4,Pt3p]
)
# armadura transversal superior
Z1_2=Arma2d.rebarFamily(identificador='Z1/2',
                 diametro=fi_Z1_2,
                 separacion=s_Z1_2,
                 lstPtosConcrSect=[Pt1,Pt2,Pt3,Pt4],
                 listaRec=[recNominal,recNominal,recNominal],
                 lado='d',
                 radioDob=rdob_Z1_2,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pl2,Pl3],
                 recSec=recNominal,
                 recLateral=recNominal,
                 ladoDibSec='d',
                 vectorLRefSec=Base.Vector(-0.3,0.3))


# armadura longitudinal inferior
Z1_3=Arma2d.rebarFamily(identificador='Z1/3',
                 diametro=fi_Z1_3,
                 separacion=s_Z1_3,
                 lstPtosConcrSect=[Pl2,Pl1,Pl4,Pl3],
                 listaRec=[recNominal,recNominal+fi_Z1_1,recNominal],
                 lado='i',
                 radioDob=rdob_Z1_3,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,-0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pt1,Pt4],
                 recSec=recNominal+fi_Z1_1,
                 recLateral=recNominal,
                 ladoDibSec='i',
                 vectorLRefSec=Base.Vector(-0.3,-0.3))
# armadura longitudinal superior
Z1_4=Arma2d.rebarFamily(identificador='Z1/4',
                 diametro=fi_Z1_4,
                 separacion=s_Z1_4,
                 lstPtosConcrSect=[Pl1,Pl2,Pl3,Pl4],
                 listaRec=[recNominal,recNominal+fi_Z1_2,recNominal],
                 lado='d',
                 radioDob=rdob_Z1_4,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pt2,Pt3],
                 recSec=recNominal+fi_Z1_2,
                 recLateral=recNominal,
                 ladoDibSec='d',
                 vectorLRefSec=Base.Vector(-0.3,0.3))

# armadura lateral puntera
Z1_7=Arma2d.rebarFamily(identificador='Z1/7',
                 diametro=fi_Z1_7,
                 separacion=s_Z1_7,
                 lstPtosConcrSect=[Pl1,Pl4],
                 listaRec=[recNominal+fi_Z1_1],
                 lado='d',
                 radioDob=rdob_Z1_7,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pt1,Pt2],
                  recSec=recNominal+fi_Z1_1,
                 recLateral=(eZap-2*recNominal-s_Z1_7)/2.0,
                 ladoDibSec='d',
                 vectorLRefSec=Base.Vector(-0.3,0.3))

# armadura lateral talón
Z1_8=Arma2d.rebarFamily(identificador='Z1/8',
                 diametro=fi_Z1_8,
                 separacion=s_Z1_8,
                 lstPtosConcrSect=[Pl1,Pl4],
                 listaRec=[recNominal+fi_Z1_1],
                 lado='d',
                 radioDob=rdob_Z1_8,
                 gapIni=-recNominal,
                 gapFin=-recNominal,
                 vectorLRef=Base.Vector(0.5,0.5),
                 hTexto=hTextosArmados,
                 ptosExtension=[Pt4,Pt3],
                  recSec=recNominal+fi_Z1_1,
                 recLateral=(eZap-2*recNominal-s_Z1_8)/2.0,
                 ladoDibSec='i',
                 vectorLRefSec=Base.Vector(0.3,0.3))

#SECCIONES TRANSVERSALES
#sección A-A
App.newDocument("secTR")
l1=makeWire([Pt1,Pt2,Pt3,Pt4],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

lstArmad=[Z1_1,Z1_2]

for rbFam in lstArmad:
    rbFam.armadura()

lstArmaSec=[Z1_3,Z1_4,Z1_7,Z1_8]
for rbFam in lstArmaSec:
   rbFam.armaSec()

#SECCIONES LONGITUDINALES
#sección B-B
App.newDocument("secLN")
l1=makeWire([Pl1,Pl2,Pl3,Pl4],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl1,Pl4],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

lstArmad=[Z1_3,Z1_4,Z1_7,Z1_8]

for rbFam in lstArmad:
    rbFam.armadura()

lstArmaSec=[Z1_1,Z1_2]
for rbFam in lstArmaSec:
    rbFam.armaSec()



   #DESPIECE DE LA ARMADURA
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hTexto=2.5
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8]
Arma2d.cuadroDespiece(anchoColumnas,hFilas,hTexto,listafamiliasArmad)

