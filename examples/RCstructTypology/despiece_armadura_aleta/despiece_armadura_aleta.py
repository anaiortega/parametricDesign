# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *

# Aleta 1, muro 1, PI+PF+OD 103.52
# DATA
#   Zapata
bZap=5.05 #ancho zapata
lMur=6.20 #longitud muro
eZap=0.90 #espesor de la zapata
recNominal=0.06
hTextosArmados=0.125
bPuntera=1.45  #ancho de la puntera

#  Muro (intradós=cara visible, trasdós= cara en contacto con tierras)
bCoron=0.30  #espesor del muro en coronación
hMurMax=256.38-248.780
hMurMin=2.78+(hMurMax-2.78)/(5.3+6.2)*5.3
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

# Armaduras muro
# Datos solapes
Lpatas=0.40
LsolapeTrasd=0.45
LsolapeIntra=0.95
LrefIntra=4.5
# Vertical trasdós
fi_M1_3=0.010
s_M1_3=0.20
rdob_M1_3=0.03
# Vertical intradós
fi_M1_4=0.020
s_M1_4=0.20
rdob_M1_4=0.03
# Refuerzo vertical intradós
fi_M1_1=0.025
s_M1_1=0.20
rdob_M1_1=0.03
# Horizontal trasdós zona inferior
fi_M1_9=0.016
s_M1_9=0.20
rdob_M1_9=0.03
# Horizontal intradós zona inferior
fi_M1_7=0.016
s_M1_7=0.20
rdob_M1_7=0.03

# Horizontal intradós zona superior
fi_M1_6=0.016
s_M1_6=0.20
rdob_M1_6=0.03

# Horizontal trasdós zona superior
fi_M1_8=0.016
s_M1_8=0.20
rdob_M1_8=0.03

# END DATA


#Puntos sección longitudinal
#    zapata
Plzap_1=Vector(0,0)
Plzap_2=Vector(0,eZap)
Plzap_3=Vector(lMur,eZap)
Plzap_4=Vector(lMur,0)
#    muro
Plmur_1=Vector(0,eZap+hMurMax)
Plmur_2=Vector(lMur,eZap+hMurMin)


#Puntos sección transversal vertical
#    zapata
Ptzap_1=Vector(0,0)
Ptzap_2=Vector(0,eZap)
Ptzap_3=Vector(bZap,eZap)
Ptzap_4=Vector(bZap,0)
#    muro: secciones de altura máxima (1) y mínima (2)
Ptmur_0=Vector(bPuntera,0)
Ptmur_1=Vector(bPuntera,eZap)
Ptmur1_2=Vector(bPuntera,eZap+hMurMax)
Ptmur1_3=Vector(bPuntera+bCoron,eZap+hMurMax)
Ptmur1_3p=Vector(bPuntera+bCoron+(hMurMax-hMurMin)*pendTrasdos,eZap+hMurMin)
Ptmur1_4=Vector(bPuntera+bCoron+hMurMax*pendTrasdos,eZap)
Ptmur1_5=Vector(bPuntera+bCoron+(hMurMax+eZap)*pendTrasdos,0)

Ptmur2_2=Vector(bPuntera,eZap+hMurMin)
Ptmur2_3=Vector(bPuntera+bCoron,eZap+hMurMin)
Ptmur2_4=Vector(bPuntera+bCoron+hMurMin*pendTrasdos,eZap)
Ptmur2_5=Vector(bPuntera+bCoron+(hMurMin+eZap)*pendTrasdos,0)

#Puntos secciones transversales horizonatales
Ph_1=Vector(0,0)
Ph1_2=Vector(0,bCoron+hMurMax*pendTrasdos)
Ph1_3=Vector(lMur,bCoron+hMurMin*pendTrasdos)
Ph_4=Vector(lMur,0)
Ph2_2=Vector(0,bCoron+(hMurMax-hMurMin)*pendTrasdos)
Ph2_3=Vector(lMur,bCoron)

Ph3_2=Vector(0,bCoron+0.2*pendTrasdos)
Ph3_3=Vector(lMur/(hMurMax-hMurMin)*0.2,bCoron)
Ph3_4=Vector(lMur/(hMurMax-hMurMin)*0.2,0)


# Armaduras zapata
# armadura transversal inferior
Z1_1=reinf_bars.rebarFamily(
    identificador='Z1/1',
    diametro=fi_Z1_1,
    separacion=s_Z1_1,
    lstPtosConcrSect=[Ptzap_2,Ptzap_1,Ptzap_4,Ptzap_3],
    listaRec=[recNominal,recNominal,recNominal],
    lado='i',
    radioDob=rdob_Z1_1,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Plzap_1,Plzap_4],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(-0.3,0.3),
#    lstPtosConcrSect2=[Ptzap_2p,Ptzap_1,Ptzap_4,Ptzap_3p]
)
# armadura transversal superior
Z1_2=reinf_bars.rebarFamily(
    identificador='Z1/2',
    diametro=fi_Z1_2,
    separacion=s_Z1_2,
    lstPtosConcrSect=[Ptzap_1,Ptzap_2,Ptzap_3,Ptzap_4],
    listaRec=[recNominal,recNominal,recNominal],
    lado='d',
    radioDob=rdob_Z1_2,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Plzap_2,Plzap_3],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.3))


# armadura longitudinal inferior
Z1_3=reinf_bars.rebarFamily(
    identificador='Z1/3',
    diametro=fi_Z1_3,
    separacion=s_Z1_3,
    lstPtosConcrSect=[Plzap_2,Plzap_1,Plzap_4,Plzap_3],
    listaRec=[recNominal,recNominal+fi_Z1_1,recNominal],
    lado='i',
    radioDob=rdob_Z1_3,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptzap_1,Ptzap_4],
    recSec=recNominal+fi_Z1_1,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(-0.3,-0.3))
# armadura longitudinal superior
Z1_4=reinf_bars.rebarFamily(
    identificador='Z1/4',
    diametro=fi_Z1_4,
    separacion=s_Z1_4,
    lstPtosConcrSect=[Plzap_1,Plzap_2,Plzap_3,Plzap_4],
    listaRec=[recNominal,recNominal+fi_Z1_2,recNominal],
    lado='d',
    radioDob=rdob_Z1_4,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptzap_2,Ptzap_3],
    recSec=recNominal+fi_Z1_2,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.3))

# armadura lateral puntera
Z1_7=reinf_bars.rebarFamily(
    identificador='Z1/7',
    diametro=fi_Z1_7,
    separacion=s_Z1_7,
    lstPtosConcrSect=[Plzap_1,Plzap_4],
    listaRec=[recNominal+fi_Z1_1],
    lado='d',
    radioDob=rdob_Z1_7,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptzap_1,Ptzap_2],
    recSec=recNominal+fi_Z1_1,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.3))

# armadura lateral talón
Z1_8=reinf_bars.rebarFamily(
    identificador='Z1/8',
    diametro=fi_Z1_8,
    separacion=s_Z1_8,
    lstPtosConcrSect=[Plzap_1,Plzap_4],
    listaRec=[recNominal+fi_Z1_1],
    lado='d',
    radioDob=rdob_Z1_8,
    gapIni=-recNominal,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptzap_4,Ptzap_3],
    recSec=recNominal+fi_Z1_1,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(0.3,0.3))

#Armadura muro
# Esperas vertical trasdós
M1_2=reinf_bars.rebarFamily(
    identificador='M1/2',
    diametro=fi_M1_3,
    separacion=s_M1_3,
    lstPtosConcrSect=[Ptmur_0+Vector(-Lpatas,0),Ptmur_0,Ptmur_1],
    listaRec=[-recNominal,recNominal],
    lado='d',
    radioDob=rdob_M1_3,
    gapIni=0,
    gapFin=LsolapeTrasd,
    vectorLRef=Vector(-0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ph_1,Ph_4],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(0.3,0.3)
)
# Armadura vertical trasdós
M1_3=reinf_bars.rebarFamily(
    identificador='M1/3',
    diametro=fi_M1_3,
    separacion=s_M1_3,
    lstPtosConcrSect=[Ptmur_1,Ptmur1_2,Ptmur1_3],
    listaRec=[recNominal,recNominal],
    lado='d',
    radioDob=rdob_M1_3,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(-0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ph_1,Ph_4],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(-0.3,-0.3),
    lstPtosConcrSect2=[Ptmur_1,Ptmur2_2,Ptmur2_3]
    )

# Esperas vertical intradós
M1_5=reinf_bars.rebarFamily(
    identificador='M1/5',
    diametro=fi_M1_4,
    separacion=s_M1_4,
    lstPtosConcrSect=[Ptmur1_5+Vector(Lpatas,0),Ptmur1_5,Ptmur1_4],
    listaRec=[-recNominal,recNominal],
    lado='i',
    radioDob=rdob_M1_4,
    gapIni=0,
    gapFin=LsolapeIntra,
    vectorLRef=Vector(-0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ph1_2,Ph1_3],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(0.3,0.3)
)

# Armadura vertical intradós
M1_4=reinf_bars.rebarFamily(
    identificador='M1/4',
    diametro=fi_M1_4,
    separacion=s_M1_4,
    lstPtosConcrSect=[Ptmur1_4,Ptmur1_3,Ptmur1_2],
    listaRec=[recNominal,recNominal],
    lado='i',
    radioDob=rdob_M1_4,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ph1_2,Ph1_3],
    recSec=recNominal,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.3),
    lstPtosConcrSect2=[Ptmur2_4,Ptmur2_3,Ptmur2_2]    
)

# Refuerzo vertical intradós
M1_1=reinf_bars.rebarFamily(
    identificador='M1/1',
    diametro=fi_M1_1,
    separacion=s_M1_1,
    lstPtosConcrSect=[Ptmur1_5+Vector(Lpatas,0),Ptmur1_5,Ptmur1_4],
    listaRec=[-recNominal,recNominal+fi_M1_4+fi_M1_7],
    lado='i',
    radioDob=rdob_M1_1,
    gapIni=0,
    gapFin=LrefIntra,
    vectorLRef=Vector(0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ph1_2,Ph1_3],
    recSec=recNominal+fi_M1_4+fi_M1_7,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,-0.3)
)
# Horizontal trasdós zona inferior
M1_7=reinf_bars.rebarFamily(
    identificador='M1/7',
    diametro=fi_M1_7,
    separacion=s_M1_7,
    lstPtosConcrSect=[Ph_1,Ph1_2,Ph1_3,Ph_4],
    listaRec=[recNominal,recNominal+fi_Z1_1,recNominal],
    lado='d',
    radioDob=rdob_M1_7,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(-0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptmur1_4,Ptmur1_3p],
    recSec=recNominal+fi_Z1_1,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtosConcrSect2=[Ph_1,Ph2_2,Ph2_3,Ph_4]
)

# Horizontal intradós zona inferior
M1_9=reinf_bars.rebarFamily(
    identificador='M1/9',
    diametro=fi_M1_9,
    separacion=s_M1_9,
    lstPtosConcrSect=[Ph_1+Vector(0,bCoron),Ph_1,Ph_4,Ph2_3],
    listaRec=[recNominal,recNominal+fi_Z1_3,recNominal],
    lado='i',
    radioDob=rdob_M1_9,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(-0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptmur_1,Ptmur2_2],
    recSec=recNominal+fi_Z1_3,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.5),
)

# Horizontal trasdós zona inferior
M1_6=reinf_bars.rebarFamily(
    identificador='M1/6',
    diametro=fi_M1_6,
    separacion=s_M1_6,
    lstPtosConcrSect=[Ph_1,Ph2_2,Ph2_3,Ph_4],
    listaRec=[recNominal,recNominal+fi_Z1_1,recNominal],
    lado='d',
    radioDob=rdob_M1_6,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(-0.5,0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptmur1_3p,Ptmur1_3],
    recSec=recNominal+fi_Z1_1,
    recLateral=recNominal,
    ladoDibSec='i',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtosConcrSect2=[Ph_1,Ph3_2,Ph3_3,Ph3_4]
)

# Horizontal intradós zona superior
M1_8=reinf_bars.rebarFamily(
    identificador='M1/8',
    diametro=fi_M1_8,
    separacion=s_M1_8,
    lstPtosConcrSect=[Ph2_2,Ph_1,Ph_4,Ph2_3],
    listaRec=[recNominal,recNominal+fi_Z1_3,recNominal],
    lado='i',
    radioDob=rdob_M1_8,
    gapIni=0,
    gapFin=-recNominal,
    vectorLRef=Vector(-0.5,-0.5),
    hTexto=hTextosArmados,
    ptosExtension=[Ptmur2_2,Ptmur1_2],
    recSec=recNominal+fi_Z1_3,
    recLateral=recNominal,
    ladoDibSec='d',
    vectorLRefSec=Vector(-0.3,0.5),
    lstPtosConcrSect2=[Ph3_2,Ph_1,Ph3_4,Ph3_3]
)
# Added 16.01.2018
#Generate the attributes wire for each family that represent the rebar
#(if not generated here it will be generated while drawing the sections or
# the bar schedule
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]
for fa in listafamiliasArmad:
    fa.createRebar()
# end  16.01.2018


# Plan of sections
App.newDocument("planRCsections")
#SECCIONES TRANSVERSALES
#sección A-A
lstPtsConcrSect=[[Ptzap_1,Ptzap_2,Ptmur_1,Ptmur1_2,Ptmur1_3,Ptmur1_4,Ptzap_3,Ptzap_4,Ptzap_1]]
lstShapeRebarFam=[Z1_1,Z1_2,M1_1,M1_2,M1_3,M1_5,M1_4]
lstSectRebarFam=[Z1_3,Z1_4,Z1_7,Z1_8,M1_9,M1_7,M1_6,M1_8]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#sección B-B
lstPtsConcrSect=[[Plzap_1,Plzap_2,Plzap_3,Plzap_4,Plzap_1]]
lstShapeRebarFam=[Z1_3,Z1_4]
lstSectRebarFam=[Z1_1,Z1_2]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,5,0))

#SECCIÓN HORIZONTAL POR LA BASE DEL MURO
lstPtsConcrSect=[[Ph_1,Ph1_2,Ph1_3,Ph_4,Ph_1]]
lstShapeRebarFam=[M1_7,M1_9]
lstSectRebarFam=[M1_3,M1_1,M1_4]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0))


#SECCIÓN HORIZONTAL SUPERIOR
lstPtsConcrSect=[[Ph_1,Ph2_2,Ph2_3,Ph_4,Ph_1]]
lstShapeRebarFam=[M1_6,M1_8]
lstSectRebarFam=[]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,0,0))


   #BAR SCHEDULE
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hTexto=2.5
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]
reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hTexto,hTextSketch=hTexto)

# Bar quantities for PyCost
reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
