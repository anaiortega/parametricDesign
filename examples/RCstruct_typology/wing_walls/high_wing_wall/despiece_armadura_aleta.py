# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

# Aleta 1, muro 1, PI+PF+OD 103.52
# DATA
estrName='Aleta 1'
titSchedule=estrName.upper()
#   Zapata
wFoot=5.05 #ancho zapata
lWall=6.20 #longitud muro
thFoot=0.90 #espesor de la zapata
cover=0.06
hTexts=0.125
wToe=1.45  #ancho de la puntera

#  Muro (intradós=cara visible, trasdós= cara en contacto con tierras)
wTop=0.30  #espesor del muro en coronación
hWallMax=256.38-248.780
hWallMin=2.78+(hWallMax-2.78)/(5.3+6.2)*5.3
slopeBack=1/15.  #pendiente del trasdós (H/V)

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
Plfoot_1=Vector(0,0)
Plfoot_2=Vector(0,thFoot)
Plfoot_3=Vector(lWall,thFoot)
Plfoot_4=Vector(lWall,0)
#    wall
Plwall_1=Vector(0,thFoot+hWallMax)
Plwall_2=Vector(lWall,thFoot+hWallMin)


#Puntos sección transversal vertical
#    zapata
Ptfoot_1=Vector(0,0)
Ptfoot_2=Vector(0,thFoot)
Ptfoot_3=Vector(wFoot,thFoot)
Ptfoot_4=Vector(wFoot,0)
#    muro: secciones de altura máxima (1) y mínima (2)
Ptwall_0=Vector(wToe,0)
Ptwall_1=Vector(wToe,thFoot)
Ptwall1_2=Vector(wToe,thFoot+hWallMax)
Ptwall1_3=Vector(wToe+wTop,thFoot+hWallMax)
Ptwall1_3p=Vector(wToe+wTop+(hWallMax-hWallMin)*slopeBack,thFoot+hWallMin)
Ptwall1_4=Vector(wToe+wTop+hWallMax*slopeBack,thFoot)
Ptwall1_5=Vector(wToe+wTop+(hWallMax+thFoot)*slopeBack,0)

Ptwall2_2=Vector(wToe,thFoot+hWallMin)
Ptwall2_3=Vector(wToe+wTop,thFoot+hWallMin)
Ptwall2_4=Vector(wToe+wTop+hWallMin*slopeBack,thFoot)
Ptwall2_5=Vector(wToe+wTop+(hWallMin+thFoot)*slopeBack,0)

#Puntos secciones transversales horizontales
Ph_1=Vector(0,0)
Ph1_2=Vector(0,wTop+hWallMax*slopeBack)
Ph1_3=Vector(lWall,wTop+hWallMin*slopeBack)
Ph_4=Vector(lWall,0)
Ph2_2=Vector(0,wTop+(hWallMax-hWallMin)*slopeBack)
Ph2_3=Vector(lWall,wTop)

Ph3_2=Vector(0,wTop+0.2*slopeBack)
Ph3_3=Vector(lWall/(hWallMax-hWallMin)*0.2,wTop)
Ph3_4=Vector(lWall/(hWallMax-hWallMin)*0.2,0)

aletGenConf=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=hTexts,Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

# Armaduras zapata
# armadura transversal inferior
Z1_1=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/1',
    diameter=fi_Z1_1,
    lstPtsConcrSect=[Ptfoot_2,Ptfoot_1,Ptfoot_4,Ptfoot_3],
    rightSideCover='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Plfoot_1,Plfoot_4],
    coverSectBars=cover,
    rightSideSectBars='l',
    spacing=s_Z1_1,
#    lstPtsConcrSect2=[Ptfoot_2p,Ptfoot_1,Ptfoot_4,Ptfoot_3p]
)
# armadura transversal superior
Z1_2=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/2',
    diameter=fi_Z1_2,
    spacing=s_Z1_2,
    lstPtsConcrSect=[Ptfoot_1,Ptfoot_2,Ptfoot_3,Ptfoot_4],
    fromToExtPts=[Plfoot_2,Plfoot_3],
    coverSectBars=cover,


# armadura longitudinal inferior
Z1_3=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/3',
    diameter=fi_Z1_3,
    spacing=s_Z1_3,
    lstPtsConcrSect=[Plfoot_2,Plfoot_1,Plfoot_4,Plfoot_3],
    lstCover=[cover,cover+fi_Z1_1,cover],
    rightSideCover='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Ptfoot_1,Ptfoot_4],
    coverSectBars=cover+fi_Z1_1,
    rightSideSectBars='l')
# armadura longitudinal superior
Z1_4=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/4',
    diameter=fi_Z1_4,
    spacing=s_Z1_4,
    lstPtsConcrSect=[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4],
    lstCover=[cover,cover+fi_Z1_2,cover],
    fromToExtPts=[Ptfoot_2,Ptfoot_3],
    coverSectBars=cover+fi_Z1_2)

# armadura lateral puntera
Z1_7=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/7',
    diameter=fi_Z1_7,
    spacing=s_Z1_7,
    lstPtsConcrSect=[Plfoot_1,Plfoot_4],
    lstCover=[cover+fi_Z1_1],
    fromToExtPts=[Ptfoot_1,Ptfoot_2],
    coverSectBars=cover+fi_Z1_1)

# armadura lateral talón
Z1_8=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='Z1/8',
    diameter=fi_Z1_8,
    spacing=s_Z1_8,
    lstPtsConcrSect=[Plfoot_1,Plfoot_4],
    lstCover=[cover+fi_Z1_1],
    fromToExtPts=[Ptfoot_4,Ptfoot_3],
    coverSectBars=cover+fi_Z1_1,
    rightSideSectBars='l',
)

#Armadura muro
# Esperas vertical trasdós
M1_2=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/2',
    diameter=fi_M1_3,
    spacing=s_M1_3,
    lstPtsConcrSect=[Ptwall_0+Vector(-Lpatas,0),Ptwall_0,Ptwall_1],
    lstCover=[-cover,cover],
    gapStart=0,
    gapEnd=LsolapeTrasd,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ph_1,Ph_4],
    coverSectBars=cover,
    rightSideSectBars='l',
)
# Armadura vertical trasdós
M1_3=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/3',
    diameter=fi_M1_3,
    spacing=s_M1_3,
    lstPtsConcrSect=[Ptwall_1,Ptwall1_2,Ptwall1_3],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ph_1,Ph_4],
    coverSectBars=cover,
    rightSideSectBars='l',
    lstPtsConcrSect2=[Ptwall_1,Ptwall2_2,Ptwall2_3]
    )

# Esperas vertical intradós
M1_5=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/5',
    diameter=fi_M1_4,
    spacing=s_M1_4,
    lstPtsConcrSect=[Ptwall1_5+Vector(Lpatas,0),Ptwall1_5,Ptwall1_4],
    lstCover=[-cover,cover],
    rightSideCover='l',
    gapStart=0,
    gapEnd=LsolapeIntra,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=cover,
    rightSideSectBars='l',
)

# Armadura vertical intradós
M1_4=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/4',
    diameter=fi_M1_4,
    spacing=s_M1_4,
    lstPtsConcrSect=[Ptwall1_4,Ptwall1_3,Ptwall1_2],
    rightSideCover='l',
    gapStart=0,
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=cover,
    lstPtsConcrSect2=[Ptwall2_4,Ptwall2_3,Ptwall2_2]    
)

# Refuerzo vertical intradós
M1_1=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/1',
    diameter=fi_M1_1,
    spacing=s_M1_1,
    lstPtsConcrSect=[Ptwall1_5+Vector(Lpatas,0),Ptwall1_5,Ptwall1_4],
    lstCover=[-cover,cover+fi_M1_4+fi_M1_7],
    rightSideCover='l',
    gapStart=0,
    gapEnd=LrefIntra,
    fromToExtPts=[Ph1_2,Ph1_3],
    coverSectBars=cover+fi_M1_4+fi_M1_7,
)
# Horizontal trasdós zona inferior
M1_7=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/7',
    diameter=fi_M1_7,
    spacing=s_M1_7,
    lstPtsConcrSect=[Ph_1,Ph1_2,Ph1_3,Ph_4],
    lstCover=[cover,cover+fi_Z1_1,cover],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_4,Ptwall1_3p],
    coverSectBars=cover+fi_Z1_1,
    rightSideSectBars='l',
    lstPtsConcrSect2=[Ph_1,Ph2_2,Ph2_3,Ph_4]
)

# Horizontal intradós zona inferior
M1_9=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/9',
    diameter=fi_M1_9,
    spacing=s_M1_9,
    lstPtsConcrSect=[Ph_1+Vector(0,wTop),Ph_1,Ph_4,Ph2_3],
    lstCover=[cover,cover+fi_Z1_3,cover],
    rightSideCover='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall_1,Ptwall2_2],
    coverSectBars=cover+fi_Z1_3,
)

# Horizontal trasdós zona inferior
M1_6=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/6',
    diameter=fi_M1_6,
    spacing=s_M1_6,
    lstPtsConcrSect=[Ph_1,Ph2_2,Ph2_3,Ph_4],
    lstCover=[cover,cover+fi_Z1_1,cover],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_3p,Ptwall1_3],
    coverSectBars=cover+fi_Z1_1,
    rightSideSectBars='l',
    lstPtsConcrSect2=[Ph_1,Ph3_2,Ph3_3,Ph3_4]
)

# Horizontal intradós zona superior
M1_8=reinf_bars.rebarFamily(
    reinfCfg=aletGenConf,
    identifier='M1/8',
    diameter=fi_M1_8,
    spacing=s_M1_8,
    lstPtsConcrSect=[Ph2_2,Ph_1,Ph_4,Ph2_3],
    lstCover=[cover,cover+fi_Z1_3,cover],
    rightSideCover='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall2_2,Ptwall1_2],
    coverSectBars=cover+fi_Z1_3,
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
lstPtsConcrSect=[[Ptfoot_1,Ptfoot_2,Ptwall_1,Ptwall1_2,Ptwall1_3,Ptwall1_4,Ptfoot_3,Ptfoot_4,Ptfoot_1]]
lstShapeRebarFam=[Z1_1,Z1_2,M1_1,M1_2,M1_3,M1_5,M1_4]
lstSectRebarFam=[Z1_3,Z1_4,Z1_7,Z1_8,M1_9,M1_7,M1_6,M1_8]
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation=Vector(0,5,0))
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation=Vector(0,5,0))
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#sección B-B
lstPtsConcrSect=[[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4,Plfoot_1]]
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
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]

reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,title=titSchedule)

# Bar quantities for PyCost
#reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
