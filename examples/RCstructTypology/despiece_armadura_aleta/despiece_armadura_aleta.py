# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

# Aleta 1, muro 1, PI+PF+OD 103.52
# DATA
estrName='Aleta 1'
#   Zapata
bZap=5.05 #ancho zapata
lMur=6.20 #longitud muro
eZap=0.90 #espesor de la zapata
recNominal=0.06
hTextsArmados=0.125
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
# armadura transversal superior
fi_Z1_2=0.025
s_Z1_2=0.15
# armadura longitudinal inferior
fi_Z1_3=0.016
s_Z1_3=0.20
# armadura longitudinal superior
fi_Z1_4=0.016
s_Z1_4=0.20
# armadura lateral talón
fi_Z1_7=0.016
s_Z1_7=0.25
# armadura lateral puntera
fi_Z1_8=0.016
s_Z1_8=0.25

# armaduras muro
# Datos solapes
Lpatas=0.40
LsolapeTrasd=0.45
LsolapeIntra=0.95
LrefIntra=4.5
# Vertical trasdós
fi_M1_3=0.010
s_M1_3=0.20

# Vertical intradós
fi_M1_4=0.020
s_M1_4=0.20

# Refuerzo vertical intradós
fi_M1_1=0.025
s_M1_1=0.20

# Horizontal trasdós zona inferior
fi_M1_9=0.016
s_M1_9=0.20

# Horizontal intradós zona inferior
fi_M1_7=0.016
s_M1_7=0.20


# Horizontal intradós zona superior
fi_M1_6=0.016
s_M1_6=0.20


# Horizontal trasdós zona superior
fi_M1_8=0.016
s_M1_8=0.20


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

#Puntos secciones transversales horizontales
Ph_1=Vector(0,0)
Ph1_2=Vector(0,bCoron+hMurMax*pendTrasdos)
Ph1_3=Vector(lMur,bCoron+hMurMin*pendTrasdos)
Ph_4=Vector(lMur,0)
Ph2_2=Vector(0,bCoron+(hMurMax-hMurMin)*pendTrasdos)
Ph2_3=Vector(lMur,bCoron)

Ph3_2=Vector(0,bCoron+0.2*pendTrasdos)
Ph3_3=Vector(lMur/(hMurMax-hMurMin)*0.2,bCoron)
Ph3_4=Vector(lMur/(hMurMax-hMurMin)*0.2,0)

aletGenConf=reinf_bars.genericConf(cover=recNominal,xcConcr=concr,xcSteel=steel,texSize=hTextsArmados,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

# Armaduras zapata
# armadura transversal inferior
Z1_1=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/1',
    diameter=fi_Z1_1,
    lstPtsConcrSect=[Ptzap_2,Ptzap_1,Ptzap_4,Ptzap_3],
    coverSide='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Plzap_1,Plzap_4],
    coverSectBars=recNominal,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,0.3),
    spacing=s_Z1_1,
#    lstPtsConcrSect2=[Ptzap_2p,Ptzap_1,Ptzap_4,Ptzap_3p]
)
# armadura transversal superior
Z1_2=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/2',
    diameter=fi_Z1_2,
    spacing=s_Z1_2,
    lstPtsConcrSect=[Ptzap_1,Ptzap_2,Ptzap_3,Ptzap_4],
    fromToExtPts=[Plzap_2,Plzap_3],
    coverSectBars=recNominal,
    vectorLRefSec=Vector(-0.3,0.3))


# armadura longitudinal inferior
Z1_3=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/3',
    diameter=fi_Z1_3,
    spacing=s_Z1_3,
    lstPtsConcrSect=[Plzap_2,Plzap_1,Plzap_4,Plzap_3],
    lstCover=[recNominal,recNominal+fi_Z1_1,recNominal],
    coverSide='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Ptzap_1,Ptzap_4],
    coverSectBars=recNominal+fi_Z1_1,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3))
# armadura longitudinal superior
Z1_4=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/4',
    diameter=fi_Z1_4,
    spacing=s_Z1_4,
    lstPtsConcrSect=[Plzap_1,Plzap_2,Plzap_3,Plzap_4],
    lstCover=[recNominal,recNominal+fi_Z1_2,recNominal],
    fromToExtPts=[Ptzap_2,Ptzap_3],
    coverSectBars=recNominal+fi_Z1_2,
    vectorLRefSec=Vector(-0.3,0.3))

# armadura lateral puntera
Z1_7=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/7',
    diameter=fi_Z1_7,
    spacing=s_Z1_7,
    lstPtsConcrSect=[Plzap_1,Plzap_4],
    lstCover=[recNominal+fi_Z1_1],
    fromToExtPts=[Ptzap_1,Ptzap_2],
    coverSectBars=recNominal+fi_Z1_1,
    vectorLRefSec=Vector(-0.3,0.3))

# armadura lateral talón
Z1_8=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='Z1/8',
    diameter=fi_Z1_8,
    spacing=s_Z1_8,
    lstPtsConcrSect=[Plzap_1,Plzap_4],
    lstCover=[recNominal+fi_Z1_1],
    fromToExtPts=[Ptzap_4,Ptzap_3],
    coverSectBars=recNominal+fi_Z1_1,
    sectBarsSide='l',
)

#Armadura muro
# Esperas vertical trasdós
M1_2=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/2',
    diameter=fi_M1_3,
    spacing=s_M1_3,
    lstPtsConcrSect=[Ptmur_0+Vector(-Lpatas,0),Ptmur_0,Ptmur_1],
    lstCover=[-recNominal,recNominal],
    gapStart=0,
    gapEnd=LsolapeTrasd,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ph_1,Ph_4],
    coverSectBars=recNominal,
    sectBarsSide='l',
)
# Armadura vertical trasdós
M1_3=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/3',
    diameter=fi_M1_3,
    spacing=s_M1_3,
    lstPtsConcrSect=[Ptmur_1,Ptmur1_2,Ptmur1_3],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ph_1,Ph_4],
    coverSectBars=recNominal,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
    lstPtsConcrSect2=[Ptmur_1,Ptmur2_2,Ptmur2_3]
    )

# Esperas vertical intradós
M1_5=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/5',
    diameter=fi_M1_4,
    spacing=s_M1_4,
    lstPtsConcrSect=[Ptmur1_5+Vector(Lpatas,0),Ptmur1_5,Ptmur1_4],
    lstCover=[-recNominal,recNominal],
    coverSide='l',
    gapStart=0,
    gapEnd=LsolapeIntra,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=recNominal,
    sectBarsSide='l',
)

# Armadura vertical intradós
M1_4=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/4',
    diameter=fi_M1_4,
    spacing=s_M1_4,
    lstPtsConcrSect=[Ptmur1_4,Ptmur1_3,Ptmur1_2],
    coverSide='l',
    gapStart=0,
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=recNominal,
    vectorLRefSec=Vector(-0.3,0.3),
    lstPtsConcrSect2=[Ptmur2_4,Ptmur2_3,Ptmur2_2]    
)

# Refuerzo vertical intradós
M1_1=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/1',
    diameter=fi_M1_1,
    spacing=s_M1_1,
    lstPtsConcrSect=[Ptmur1_5+Vector(Lpatas,0),Ptmur1_5,Ptmur1_4],
    lstCover=[-recNominal,recNominal+fi_M1_4+fi_M1_7],
    coverSide='l',
    gapStart=0,
    gapEnd=LrefIntra,
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=recNominal+fi_M1_4+fi_M1_7,
    vectorLRefSec=Vector(-0.3,-0.3)
)
# Horizontal trasdós zona inferior
M1_7=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/7',
    diameter=fi_M1_7,
    spacing=s_M1_7,
    lstPtsConcrSect=[Ph_1,Ph1_2,Ph1_3,Ph_4],
    lstCover=[recNominal,recNominal+fi_Z1_1,recNominal],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptmur1_4,Ptmur1_3p],
    coverSectBars=recNominal+fi_Z1_1,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtsConcrSect2=[Ph_1,Ph2_2,Ph2_3,Ph_4]
)

# Horizontal intradós zona inferior
M1_9=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/9',
    diameter=fi_M1_9,
    spacing=s_M1_9,
    lstPtsConcrSect=[Ph_1+Vector(0,bCoron),Ph_1,Ph_4,Ph2_3],
    lstCover=[recNominal,recNominal+fi_Z1_3,recNominal],
    coverSide='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptmur_1,Ptmur2_2],
    coverSectBars=recNominal+fi_Z1_3,
    vectorLRefSec=Vector(-0.3,0.5),
)

# Horizontal trasdós zona inferior
M1_6=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/6',
    diameter=fi_M1_6,
    spacing=s_M1_6,
    lstPtsConcrSect=[Ph_1,Ph2_2,Ph2_3,Ph_4],
    lstCover=[recNominal,recNominal+fi_Z1_1,recNominal],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptmur1_3p,Ptmur1_3],
    coverSectBars=recNominal+fi_Z1_1,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtsConcrSect2=[Ph_1,Ph3_2,Ph3_3,Ph3_4]
)

# Horizontal intradós zona superior
M1_8=reinf_bars.rebarFamily(
    genConf=aletGenConf,
    identifier='M1/8',
    diameter=fi_M1_8,
    spacing=s_M1_8,
    lstPtsConcrSect=[Ph2_2,Ph_1,Ph_4,Ph2_3],
    lstCover=[recNominal,recNominal+fi_Z1_3,recNominal],
    coverSide='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptmur2_2,Ptmur1_2],
    coverSectBars=recNominal+fi_Z1_3,
    vectorLRefSec=Vector(-0.3,0.5),
    lstPtsConcrSect2=[Ph3_2,Ph_1,Ph3_4,Ph3_3]
)

# Added 16.01.2018
#Generate the attributes wire for each family that represent the rebar
#(if not generated here it will be generated while drawing the sections or
# the bar schedule
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]
for fa in listafamiliasArmad:
    fa.createLstRebar()
# end  16.01.2018


# Plan of sections
App.newDocument("planRCsections")
#SECCIONES TRANSVERSALES
#sección A-A
lstPtsConcrSect=[[Ptzap_1,Ptzap_2,Ptmur_1,Ptmur1_2,Ptmur1_3,Ptmur1_4,Ptzap_3,Ptzap_4,Ptzap_1]]
lstShapeRebarFam=[Z1_1,Z1_2,M1_1,M1_2,M1_3,M1_5,M1_4]
lstSectRebarFam=[Z1_3,Z1_4,Z1_7,Z1_8,M1_9,M1_7,M1_6,M1_8]
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation=Vector(0,5,0))
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation=Vector(0,5,0))
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#sección B-B
lstPtsConcrSect=[[Plzap_1,Plzap_2,Plzap_3,Plzap_4,Plzap_1]]
lstShapeRebarFam=[Z1_3,Z1_4]
lstSectRebarFam=[Z1_1,Z1_2]
#vTranslation=Vector(10,5,0))
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,5,0))

#SECCIÓN HORIZONTAL POR LA BASE DEL MURO
lstPtsConcrSect=[[Ph_1,Ph1_2,Ph1_3,Ph_4,Ph_1]]
lstShapeRebarFam=[M1_7,M1_9]
lstSectRebarFam=[M1_3,M1_1,M1_4]
# vTranslation=Vector(0,0,0)
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)

    
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)


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
hText=2.5
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]

reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hText,hTextSketch=2.0)

# Bar quantities for PyCost
#reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
