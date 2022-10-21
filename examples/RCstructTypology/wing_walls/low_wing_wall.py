import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials

concrFoot=EC2_materials.C30 # concrete type in footing
steelFoot=EC2_materials.S500C # steel for footing

concrWall=EC2_materials.C30 # concrete type in wall stem
steelWall=EC2_materials.S500C # steel for wall stem

#rebar schedule dimensions
scheduleCfg=reinf_bars.scheduleConf([14,30,25,10,15,15],10,2.5,2.0)

#  DATA
estrName='Aleta 1'
titSchedule=estrName.upper()
hTexts=0.125

#Footing
wFoot=5.05 #ancho zapata
lWall=6.20 #longitud muro
thFoot=0.90 #espesor de la zapata
wToe=1.45  #ancho de la puntera
coverFoot=0.06

# Wall 
wTop=0.30  #espesor del muro en coronación
hWallMax=2.8
hWallMin=1.25
slopeBack=1/15.  #pendiente del trasdós (H/V)
coverWall=0.04
slopeBack=0
alpha_degrees=math.degrees(math.atan(slopeBack)) 
#

footGenConf=reinf_bars.genericConf(cover=coverFoot,xcConcr=concrFoot,xcSteel=steelFoot,texSize=hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

wallGenConf=reinf_bars.genericConf(cover=coverWall,xcConcr=concrWall,xcSteel=steelWall,texSize=hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

# #  Armados zapata
# armadura transversal inferior
fi_foot_tr_bot=0.025
s_foot_tr_bot=0.25
# armadura transversal superior
fi_foot_tr_top=0.025
s_foot_tr_top=0.15
# armadura longitudinal inferior
fi_foot_ln_bot=0.016
s_foot_ln_bot=0.20
# armadura longitudinal superior
fi_foot_ln_top=0.016
s_foot_ln_top=0.20
# armadura lateral talón
fi_foot_lat_heel=0.016
s_foot_lat_heel=0.25
# armadura lateral puntera
fi_foot_lat_toe=0.016
s_foot_lat_toe=0.25

# armaduras muro
# Vertical trasdós
fi_wall_vert_back=0.010
s_wall_vert_back=0.20

# Vertical intradós
fi_wall_vert_front=0.020
s_wall_vert_front=0.20

# Horizontal trasdós zona inferior
fi_wall_horBottom_back=0.016
s_wall_horBottom_back=0.20

# Horizontal intradós zona inferior
fi_wall_horBottom_front=0.016
s_wall_horBottom_front=0.20

# Horizontal intradós zona superior
fi_wall_horTop_front=fi_wall_horBottom_front
s_wall_horTop_front=s_wall_horBottom_front

# Horizontal trasdós zona superior
fi_wall_horTop_back=fi_wall_horBottom_back
s_wall_horTop_back=s_wall_horBottom_back

#END DATA

# points longitudinal section
#  Footing
Plfoot_1=Vector(0,0)
Plfoot_2=Vector(0,thFoot)
Plfoot_3=Vector(lWall,thFoot)
Plfoot_4=Vector(lWall,0)
#    wall
Plwall_1=Vector(0,thFoot+hWallMax)
Plwall_2=Vector(lWall,thFoot+hWallMin)

# points vertical transversal section
Ptfoot_1=Vector(0,0)
Ptfoot_2=Vector(0,thFoot)
Ptfoot_3=Vector(wFoot,thFoot)
Ptfoot_4=Vector(wFoot,0)

# points   wall: sections maximun high (1) and minimum high (2)
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

# points horizontal transversal sections
Ph_1=Vector(0,0)
Ph1_2=Vector(0,wTop+hWallMax*slopeBack)
Ph1_3=Vector(lWall,wTop+hWallMin*slopeBack)
Ph_4=Vector(lWall,0)
Ph2_2=Vector(0,wTop+(hWallMax-hWallMin)*slopeBack)
Ph2_3=Vector(lWall,wTop)

Ph3_2=Vector(0,wTop+0.2*slopeBack)
Ph3_3=Vector(lWall/(hWallMax-hWallMin)*0.2,wTop)
Ph3_4=Vector(lWall/(hWallMax-hWallMin)*0.2,0)

# Armaduras zapata
# armadura transversal inferior
lstRebarFam=list()
rebarCount=0
RF_foot_tr_bot=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_tr_bot,
    lstPtsConcrSect=[Ptfoot_2,Ptfoot_1,Ptfoot_4,Ptfoot_3],
    coverSide='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Plfoot_1,Plfoot_4],
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,0.3),
    spacing=s_foot_tr_bot,
#    lstPtsConcrSect2=[Ptfoot_2p,Ptfoot_1,Ptfoot_4,Ptfoot_3p]
)
lstRebarFam+=[RF_foot_tr_bot]
rebarCount+=1

# armadura transversal superior
RF_foot_tr_top=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_tr_top,
    spacing=s_foot_tr_top,
    lstPtsConcrSect=[Ptfoot_1,Ptfoot_2,Ptfoot_3,Ptfoot_4],
    fromToExtPts=[Plfoot_2,Plfoot_3],
    vectorLRefSec=Vector(-0.3,0.3))
lstRebarFam+=[RF_foot_tr_top]
rebarCount+=1

# armadura longitudinal inferior
RF_foot_ln_bot=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_ln_bot,
    spacing=s_foot_ln_bot,
    lstPtsConcrSect=[Plfoot_2,Plfoot_1,Plfoot_4,Plfoot_3],
    lstCover=[footGenConf.cover,footGenConf.cover+fi_foot_tr_bot,footGenConf.cover],
    coverSide='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[Ptfoot_1,Ptfoot_4],
    coverSectBars=footGenConf.cover+fi_foot_tr_bot,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3))
lstRebarFam+=[RF_foot_ln_bot]
rebarCount+=1
# armadura longitudinal superior
RF_foot_ln_top=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_ln_top,
    spacing=s_foot_ln_top,
    lstPtsConcrSect=[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4],
    lstCover=[footGenConf.cover,footGenConf.cover+fi_foot_tr_top,footGenConf.cover],
    fromToExtPts=[Ptfoot_2,Ptfoot_3],
    coverSectBars=footGenConf.cover+fi_foot_tr_top,
    vectorLRefSec=Vector(-0.3,0.3))
lstRebarFam+=[RF_foot_ln_top]
rebarCount+=1

# armadura lateral puntera
RF_foot_lat_heel=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_lat_heel,
    spacing=s_foot_lat_heel,
    lstPtsConcrSect=[Plfoot_1,Plfoot_4],
    lstCover=[footGenConf.cover+fi_foot_tr_bot],
    fromToExtPts=[Ptfoot_1,Ptfoot_2],
    coverSectBars=footGenConf.cover+fi_foot_tr_bot,
    vectorLRefSec=Vector(-0.3,0.3))
lstRebarFam+=[RF_foot_lat_heel]
rebarCount+=1

# armadura lateral talón
RF_foot_lat_toe=reinf_bars.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_foot_lat_toe,
    spacing=s_foot_lat_toe,
    lstPtsConcrSect=[Plfoot_1,Plfoot_4],
    lstCover=[footGenConf.cover+fi_foot_tr_bot],
    fromToExtPts=[Ptfoot_4,Ptfoot_3],
    coverSectBars=footGenConf.cover+fi_foot_tr_bot,
    sectBarsSide='l',
)
lstRebarFam+=[RF_foot_lat_toe]
rebarCount+=1

#Armadura muro
# Armadura vertical trasdós
RF_wall_vert_back=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_vert_back,
    spacing=s_wall_vert_back,
    lstPtsConcrSect=[Ptwall_1,Ptwall1_2,Ptwall1_3],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ph_1,Ph_4],
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
    lstPtsConcrSect2=[Ptwall_1,Ptwall2_2,Ptwall2_3]
    )
lstRebarFam+=[RF_wall_vert_back]
rebarCount+=1


# Armadura vertical intradós
RF_wall_vert_front=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_vert_front,
    spacing=s_wall_vert_front,
    lstPtsConcrSect=[Ptwall1_4,Ptwall1_3,Ptwall1_2],
    coverSide='l',
    gapStart=0,
    fromToExtPts=[Ph1_2,Ph1_3],
    vectorLRefSec=Vector(-0.3,0.3),
    lstPtsConcrSect2=[Ptwall2_4,Ptwall2_3,Ptwall2_2]    
)
lstRebarFam+=[RF_wall_vert_front]
rebarCount+=1

# Horizontal trasdós zona inferior
RF_wall_horBottom_front=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_horBottom_front,
    spacing=s_wall_horBottom_front,
    lstPtsConcrSect=[Ph_1,Ph1_2,Ph1_3,Ph_4],
    lstCover=[wallGenConf.cover,wallGenConf.cover+fi_foot_tr_bot,wallGenConf.cover],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_4,Ptwall1_3p],
    coverSectBars=wallGenConf.cover+fi_foot_tr_bot,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtsConcrSect2=[Ph_1,Ph2_2,Ph2_3,Ph_4]
)
lstRebarFam+=[RF_wall_horBottom_front]
rebarCount+=1

# Horizontal intradós zona inferior
RF_wall_horBottom_back=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_horBottom_back,
    spacing=s_wall_horBottom_back,
    lstPtsConcrSect=[Ph_1+Vector(0,wTop),Ph_1,Ph_4,Ph2_3],
    lstCover=[wallGenConf.cover,wallGenConf.cover+fi_foot_ln_bot,wallGenConf.cover],
    coverSide='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall_1,Ptwall2_2],
    coverSectBars=wallGenConf.cover+fi_foot_ln_bot,
    vectorLRefSec=Vector(-0.3,0.5),
)
lstRebarFam+=[RF_wall_horBottom_back]
rebarCount+=1

# Horizontal trasdós zona inferior
RF_wall_horTop_front=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_horTop_front,
    spacing=s_wall_horTop_front,
    lstPtsConcrSect=[Ph_1,Ph2_2,Ph2_3,Ph_4],
    lstCover=[wallGenConf.cover,wallGenConf.cover+fi_foot_tr_bot,wallGenConf.cover],
    gapStart=0,
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_3p,Ptwall1_3],
    coverSectBars=wallGenConf.cover+fi_foot_tr_bot,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,0.7),
    lstPtsConcrSect2=[Ph_1,Ph3_2,Ph3_3,Ph3_4]
)
lstRebarFam+=[RF_wall_horTop_front]
rebarCount+=1

# Horizontal intradós zona superior
RF_wall_horTop_back=reinf_bars.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=fi_wall_horTop_back,
    spacing=s_wall_horTop_back,
    lstPtsConcrSect=[Ph2_2,Ph_1,Ph_4,Ph2_3],
    lstCover=[wallGenConf.cover,wallGenConf.cover+fi_foot_ln_bot,wallGenConf.cover],
    coverSide='l',
    gapStart=0,
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall2_2,Ptwall1_2],
    coverSectBars=wallGenConf.cover+fi_foot_ln_bot,
    vectorLRefSec=Vector(-0.3,0.5),
    lstPtsConcrSect2=[Ph3_2,Ph_1,Ph3_4,Ph3_3]
)
lstRebarFam+=[RF_wall_horTop_back]
rebarCount+=1

# Added 16.01.2018
#Generate the attributes wire for each family that represent the rebar
#(if not generated here it will be generated while drawing the sections or
# the bar schedule

for fa in lstRebarFam:
    fa.createLstRebar()
# end  16.01.2018


# Plan of sections
App.newDocument("planRCsections")
#SECCIONES TRANSVERSALES
#sección A-A
lstPtsConcrSect=[[Ptfoot_1,Ptfoot_2,Ptwall_1,Ptwall1_2,Ptwall1_3,Ptwall1_4,Ptfoot_3,Ptfoot_4,Ptfoot_1]]
lstShapeRebarFam=[RF_foot_tr_bot,RF_foot_tr_top,RF_wall_vert_back,RF_wall_vert_front]
lstSectRebarFam=[RF_foot_ln_bot,RF_foot_ln_top,RF_foot_lat_heel,RF_foot_lat_toe,RF_wall_horBottom_back,RF_wall_horBottom_front,RF_wall_horTop_front,RF_wall_horTop_back]
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation=Vector(0,5,0))
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation=Vector(0,5,0))
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#sección B-B
lstPtsConcrSect=[[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4,Plfoot_1]]
lstShapeRebarFam=[RF_foot_ln_bot,RF_foot_ln_top]
lstSectRebarFam=[RF_foot_tr_bot,RF_foot_tr_top]
#vTranslation=Vector(10,5,0))
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,5,0))

#SECCIÓN HORIZONTAL POR LA BASE DEL MURO
lstPtsConcrSect=[[Ph_1,Ph1_2,Ph1_3,Ph_4,Ph_1]]
lstShapeRebarFam=[RF_wall_horBottom_front,RF_wall_horBottom_back]
lstSectRebarFam=[RF_wall_vert_back,RF_wall_vert_front]
# vTranslation=Vector(0,0,0)
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)

    
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)


reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0))


#SECCIÓN HORIZONTAL SUPERIOR
lstPtsConcrSect=[[Ph_1,Ph2_2,Ph2_3,Ph_4,Ph_1]]
lstShapeRebarFam=[RF_wall_horTop_front,RF_wall_horTop_back]
lstSectRebarFam=[]


reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,0,0))


   #BAR SCHEDULE
App.newDocument("despiece")
#altura de las filas
#altura textos

reinf_bars.barSchedule(lstBarFamilies=lstRebarFam,scheduleCfg,title=titSchedule)

# Bar quantities for PyCost
#reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
