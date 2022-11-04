import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials
docName='despiece_arm'
docDespiece=App.newDocument(docName,docName) #many schedules may be added to this doc (create only for the first wing-wall)

# DATA
estrName='Aleta 1'
nmbAleta=1 # Number of wing_wall
titSchedule=estrName.upper()
hTexts=0.0625  # scale 1:25
alpha_degrees=math.degrees(math.atan(slopeBack)) 
coverFoot=0.03
coverWall=0.03


concrFoot=EC2_materials.C30 # concrete type in footing
steelFoot=EC2_materials.S500C # steel for footing

concrWall=EC2_materials.C30 # concrete type in wall stem
steelWall=EC2_materials.S500C # steel for wall stem

dowels=False # True if dowels in the stem start, otherwise, False

#rebar schedule dimensions
scheduleCfg=rb.scheduleConf(widthColumns=[10,30,20,10,20,12],heightRows=10,heightText=2.5,heigthTextSketch=2.0)

#Footing
wFoot=2.35 #ancho zapata
lWall=3.50 #longitud muro
thFoot=0.35 #espesor de la zapata
wToe=0  #ancho de la puntera
coverFoot=0.03

# Wall 
wTop=0.25  #espesor del muro en coronación
hWallMax=2.6
hWallMin=1.26
slopeBack=0  #pendiente del trasdós (H/V)
coverWall=0.03
alpha_degrees=math.degrees(math.atan(slopeBack)) 

footGenConf=rb.genericConf(cover=coverFoot,xcConcr=concrFoot,xcSteel=steelFoot,texSize=hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=2/3)

wallGenConf=rb.genericConf(cover=coverWall,xcConcr=concrWall,xcSteel=steelWall,texSize=hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=2/3)

# #  Armados zapata
# armadura transversal inferior
foot_tr_bot={'fi':0.012,'s':0.20}
# armadura transversal superior
foot_tr_top={'fi':0.012,'s':0.15}
# armadura longitudinal inferior
foot_ln_bot={'fi':0.012,'s':0.20}
# armadura longitudinal superior
foot_ln_top={'fi':0.012,'s':0.20}
# armadura lateral en todo el perímetro de la zapata  definida por el nº de barras
#foot_lat_heel=None
foot_lat={'fi':0.012,'nmbBars':2,'s':0} 

# armaduras muro
# Vertical trasdós
wall_vert_back={'fi':0.012,'s':0.15}
# Vertical intradós
wall_vert_front={'fi':0.012,'s':0.20}
# Horizontal trasdós zona inferior
wall_horBottom_back={'fi':0.012,'s':0.20}
# Horizontal intradós zona inferior
wall_horBottom_front={'fi':0.012,'s':0.20}
# Horizontal intradós zona superior
wall_horTop_front=wall_horBottom_front
# Horizontal trasdós zona superior
#wall_horTop_back={'fi':0.016,'s':0.20}
wall_horTop_back=wall_horBottom_back
# coronación
wall_top={'fi':0.012,'nmbBars':2,'s':0} 
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

Phf_2=Ph_1.add(Vector(0,wFoot))
Phf_3=Ph_4.add(Vector(0,wFoot))

# Armaduras zapata
# armadura transversal inferior
lstRebarFam=list()
rebarCount=0
RF_foot_tr_bot=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_tr_bot['fi'],
    gapStart=-2.5*footGenConf.cover,
    gapEnd=-2.5*footGenConf.cover,
    lstPtsConcrSect=[Ptfoot_2,Ptfoot_1,Ptfoot_4,Ptfoot_3],
    coverSide='l',
    vectorLRef=Vector(-0.3,-0.3),
    fromToExtPts=[Plfoot_1,Plfoot_4],
    sectBarsSide='l',
    spacing=foot_tr_bot['s'],
#    lstPtsConcrSect2=[Ptfoot_2p,Ptfoot_1,Ptfoot_4,Ptfoot_3p]
)
lstRebarFam+=[RF_foot_tr_bot]
rebarCount+=1

# armadura transversal superior
RF_foot_tr_top=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_tr_top['fi'],
    spacing=foot_tr_top['s'],
    gapStart=-2.5*footGenConf.cover,
    gapEnd=-2.5*footGenConf.cover,
    lstPtsConcrSect=[Ptfoot_1,Ptfoot_2,Ptfoot_3,Ptfoot_4],
    fromToExtPts=[Plfoot_2,Plfoot_3],
    vectorLRef=Vector(0.05,0.35),
    )
lstRebarFam+=[RF_foot_tr_top]
rebarCount+=1

# armadura longitudinal inferior
RF_foot_ln_bot=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_ln_bot['fi'],
    spacing=foot_ln_bot['s'],
    gapStart=-2.5*footGenConf.cover,
    gapEnd=-2.5*footGenConf.cover,
    lstPtsConcrSect=[Plfoot_2,Plfoot_1,Plfoot_4,Plfoot_3],
    lstCover=[footGenConf.cover,footGenConf.cover+foot_tr_bot['fi'],footGenConf.cover],
    coverSide='l',
    vectorLRef=Vector(-0.3,-0.3),
    fromToExtPts=[Ptfoot_1,Ptfoot_4],
    coverSectBars=footGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='l',
    )
lstRebarFam+=[RF_foot_ln_bot]
rebarCount+=1
# armadura longitudinal superior
RF_foot_ln_top=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_ln_top['fi'],
    spacing=foot_ln_top['s'],
    gapStart=-2.5*footGenConf.cover,
    gapEnd=-2.5*footGenConf.cover,
    lstPtsConcrSect=[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4],
    lstCover=[footGenConf.cover,footGenConf.cover+foot_tr_top['fi'],footGenConf.cover],
    fromToExtPts=[Ptfoot_2,Ptfoot_3],
    coverSectBars=footGenConf.cover+foot_tr_top['fi'],
    vectorLRef=Vector(-0.3,0.3),
    )
lstRebarFam+=[RF_foot_ln_top]
rebarCount+=1

# armadura lateral puntera
RF_foot_lat_toe=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_lat['fi'],
#    spacing=foot_lat_heel['s'],
    nmbBars=foot_lat['nmbBars'],
    lstPtsConcrSect=[Ph_1,Phf_2],
    lstCover=[footGenConf.cover+foot_tr_bot['fi']],
    fromToExtPts=[Plfoot_1,Plfoot_2],
    coverSectBars=footGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='r',
    extrShapeStart='anc270_posGood_tens',
    extrShapeEnd='anc270_posGood_tens',
    )
lstRebarFam+=[RF_foot_lat_toe]
rebarCount+=1

# armadura lateral talón
RF_foot_lat_heel=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_lat['fi'],
    spacing=foot_lat['s'],
    coverSide='l',
    nmbBars=foot_lat['nmbBars'],
    lstPtsConcrSect=[Ph_4,Phf_3],
    lstCover=[footGenConf.cover+foot_tr_bot['fi']],
    fromToExtPts=[Plfoot_4,Plfoot_3],
    coverSectBars=footGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='l',
    extrShapeStart='anc90_posGood_tens',
    extrShapeEnd='anc90_posGood_tens',
    )
lstRebarFam+=[RF_foot_lat_heel]
rebarCount+=1

# armadura lateral frontal
RF_foot_lat_front=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_lat['fi'],
    spacing=foot_lat['s'],
    coverSide='l',
    nmbBars=foot_lat['nmbBars'],
    lstPtsConcrSect=[Ph_1,Ph_4],
    lstCover=[footGenConf.cover+foot_tr_bot['fi']],
    fromToExtPts=[Ptfoot_1,Ptfoot_2],
    coverSectBars=footGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='r',
    extrShapeStart='anc90_posGood_tens',
    extrShapeEnd='anc90_posGood_tens',
    )
    
    
lstRebarFam+=[RF_foot_lat_front]
rebarCount+=1

# armadura lateral dorsal
RF_foot_lat_dors=rb.rebarFamily(
    genConf=footGenConf,
    identifier=str(rebarCount+1),
    diameter=foot_lat['fi'],
    spacing=foot_lat['s'],
    coverSide='r',
    nmbBars=foot_lat['nmbBars'],
    lstPtsConcrSect=[Phf_2,Phf_3],
    lstCover=[footGenConf.cover+foot_tr_bot['fi']],
    fromToExtPts=[Ptfoot_4,Ptfoot_3],
    coverSectBars=footGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='l',
    extrShapeStart='anc270_posGood_tens',
    extrShapeEnd='anc2700_posGood_tens',
    )
lstRebarFam+=[RF_foot_lat_dors]
rebarCount+=1

if dowels:
    # Esperas trasdós
    ang=int(90-math.degrees(math.atan(slopeBack)))
    RF_dowel_back=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_back['fi'],
        spacing=wall_vert_back['s'],
        lstPtsConcrSect=[Ptwall1_4,Ptwall1_4+Vector(slopeBack*thFoot,-thFoot)],
        coverSide='r',
        gapStart=0,
        gapEnd=-(footGenConf.cover+foot_tr_bot['fi']+foot_ln_bot['fi']+wall_vert_back['fi']/2),
        extrShapeStart='lap0_posGood_tens',
        extrShapeEnd='fix'+str(ang)+'_len200',
        fromToExtPts=[Ph1_2,Ph1_3],
        vectorLRef=Vector(0.2,0.2),
        )
    
    lstRebarFam+=[RF_dowel_back]
    rebarCount+=1
    ang=270 if wToe>0 else 90
    # Esperas intradós
    RF_dowel_front=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_front['fi'],
        spacing=wall_vert_front['s'],
        coverSide='l',
        lstPtsConcrSect=[Ptwall_1,Ptwall_1+Vector(0,-thFoot)],
        gapStart=0,
        gapEnd=-(footGenConf.cover+foot_tr_bot['fi']+foot_ln_bot['fi']+wall_vert_front['fi']/2),
        extrShapeStart='lap0_posGood_tens',
        extrShapeEnd='fix'+str(ang)+'_len200',
        vectorLRef=Vector(-0.25,0.2),
        fromToExtPts=[Ph_1,Ph_4],
        sectBarsSide='l',
#        lstPtsConcrSect2=[Ptwall_1,Ptwall2_2,Ptwall2_3]
        )
    lstRebarFam+=[RF_dowel_front]
    rebarCount+=1

    #Armadura muro
    # Armadura vertical trasdós
    RF_wall_vert_back=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_back['fi'],
        spacing=wall_vert_back['s'],
        lstPtsConcrSect=[Ptwall1_4,Ptwall1_3,Ptwall1_2],
        coverSide='l',
        gapStart=0,
        fromToExtPts=[Ph1_2,Ph1_3],
        lstPtsConcrSect2=[Ptwall2_4,Ptwall2_3,Ptwall2_2],    
        vectorLRef=Vector(0.25,0.20),
        )
    lstRebarFam+=[RF_wall_vert_back]
    rebarCount+=1

    # Armadura vertical intradós
    RF_wall_vert_front=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_front['fi'],
        spacing=wall_vert_front['s'],
        lstPtsConcrSect=[Ptwall_1,Ptwall1_2,Ptwall1_3],
        gapStart=0,
        vectorLRef=Vector(-0.25,0.2),
        fromToExtPts=[Ph_1,Ph_4],
        sectBarsSide='l',
        lstPtsConcrSect2=[Ptwall_1,Ptwall2_2,Ptwall2_3]
        )

    lstRebarFam+=[RF_wall_vert_front]
    rebarCount+=1

else: # sin esperas
    #Armadura muro
    # Armadura vertical trasdós (en contacto con las tierras)
    ang=int(270-math.degrees(math.atan(slopeBack)))
    RF_wall_vert_back=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_back['fi'],
        spacing=wall_vert_back['s'],
        lstPtsConcrSect=[Ptwall1_4+Vector(slopeBack*thFoot,-thFoot),Ptwall1_3,Ptwall1_2],
        coverSide='l',
        gapStart=-(footGenConf.cover+foot_tr_bot['fi']+foot_ln_bot['fi']+wall_vert_back['fi']/2),
        extrShapeStart='fix'+str(ang)+'_len200',
        fromToExtPts=[Ph1_2,Ph1_3],
        lstPtsConcrSect2=[Ptwall2_4,Ptwall2_3,Ptwall2_2],
        vectorLRef=Vector(0.3,0.3), 
        )
    lstRebarFam+=[RF_wall_vert_back]
    rebarCount+=1

    # Armadura vertical intradós
    ang=90 if wToe>0 else 270
    RF_wall_vert_front=rb.rebarFamily(
        genConf=wallGenConf,
        identifier=str(rebarCount+1),
        diameter=wall_vert_front['fi'],
        spacing=wall_vert_front['s'],
        lstPtsConcrSect=[Ptwall_1+Vector(0,-thFoot),Ptwall1_2,Ptwall1_3],
        gapStart=-(footGenConf.cover+foot_tr_bot['fi']+foot_ln_bot['fi']+wall_vert_front['fi']/2),
        vectorLRef=Vector(-0.3,0.3),
        extrShapeStart='fix'+str(ang)+'_len200',
        fromToExtPts=[Ph_1,Ph_4],
        sectBarsSide='l',
        lstPtsConcrSect2=[Ptwall_1,Ptwall2_2,Ptwall2_3],
        )

    lstRebarFam+=[RF_wall_vert_back]
    rebarCount+=1


# Armadura muro    
# Horizontal trasdós zona inferior
RF_wall_horBottom_front=rb.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=wall_horBottom_front['fi'],
    spacing=wall_horBottom_front['s'],
    lstPtsConcrSect=[Ph_1,Ph1_2,Ph1_3,Ph_4],
    lstCover=[wallGenConf.cover,wallGenConf.cover+foot_tr_bot['fi'],wallGenConf.cover],
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_4,Ptwall1_3p],
    coverSectBars=wallGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='l',
    lstPtsConcrSect2=[Ph_1,Ph2_2,Ph2_3,Ph_4]
    )
lstRebarFam+=[RF_wall_horBottom_front]
rebarCount+=1

# Horizontal intradós zona inferior
RF_wall_horBottom_back=rb.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=wall_horBottom_back['fi'],
    spacing=wall_horBottom_back['s'],
    lstPtsConcrSect=[Ph_1+Vector(0,wTop),Ph_1,Ph_4,Ph2_3],
    lstCover=[wallGenConf.cover,wallGenConf.cover+foot_ln_bot['fi'],wallGenConf.cover],
    coverSide='l',
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall_1,Ptwall2_2],
    coverSectBars=wallGenConf.cover+foot_ln_bot['fi'],
    )
lstRebarFam+=[RF_wall_horBottom_back]
rebarCount+=1

# Horizontal trasdós zona inferior
RF_wall_horTop_front=rb.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=wall_horTop_front['fi'],
    spacing=wall_horTop_front['s'],
    lstPtsConcrSect=[Ph_1,Ph2_2,Ph2_3,Ph_4],
    lstCover=[wallGenConf.cover,wallGenConf.cover+foot_tr_bot['fi'],wallGenConf.cover],
    vectorLRef=Vector(-0.5,0.5),
    fromToExtPts=[Ptwall1_3p,Ptwall1_3],
    coverSectBars=wallGenConf.cover+foot_tr_bot['fi'],
    sectBarsSide='l',
    lstPtsConcrSect2=[Ph_1,Ph3_2,Ph3_3,Ph3_4]
    )
lstRebarFam+=[RF_wall_horTop_front]
rebarCount+=1

# Horizontal intradós zona superior
RF_wall_horTop_back=rb.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=wall_horTop_back['fi'],
    spacing=wall_horTop_back['s'],
    lstPtsConcrSect=[Ph2_2,Ph_1,Ph_4,Ph2_3],
    lstCover=[wallGenConf.cover,wallGenConf.cover+foot_ln_bot['fi'],wallGenConf.cover],
    coverSide='l',
    vectorLRef=Vector(-0.5,-0.5),
    fromToExtPts=[Ptwall2_2,Ptwall1_2],
    coverSectBars=wallGenConf.cover+foot_ln_bot['fi'],
    lstPtsConcrSect2=[Ph3_2,Ph_1,Ph3_4,Ph3_3]
    )
lstRebarFam+=[RF_wall_horTop_back]
rebarCount+=1
# coronación muro
angle1=math.degrees((Plwall_2-Plwall_1).getAngle(Vector(0,-1,0)))
angle1=round(angle1,2)
RF_wall_top=rb.rebarFamily(
    genConf=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=wall_top['fi'],
    spacing=wall_top['s'],
    coverSide='r',
    nmbBars=wall_top['nmbBars'],
    lstPtsConcrSect=[Plwall_1,Plwall_2],
    lstCover=[wallGenConf.cover+wall_vert_back['fi']],
    fromToExtPts=[Ptwall1_2,Ptwall1_3],
    coverSectBars=wallGenConf.cover+wall_vert_back['fi'],
    sectBarsSide='r',
    gapStart=-1.5*wallGenConf.cover-wall_top['fi']/2,
    gapEnd=-wallGenConf.cover-wall_top['fi']/2,
    extrShapeStart='anc'+str(360-angle1)+'_posPoor_tens',
    extrShapeEnd='anc'+str(360-angle1)+'_posPoor_tens',
    vectorLRef=Vector(0.25,0.25),
    )
lstRebarFam+=[RF_wall_top_heel]
rebarCount+=1

# Added 16.01.2018
#Generate the attributes wire for each family that represent the rebar
#(if not generated here it will be generated while drawing the sections or
# the bar schedule

for fa in lstRebarFam:
    fa.createLstRebar()
# end  16.01.2018


# Plan of sections
docName=estrName.replace(' ','')+'_sect'
App.newDocument(docName,docName)
#SECCIONES TRANSVERSALES
#sección A-A (muro + zapata)
lstPtsConcrSect=[[Ptfoot_1,Ptfoot_2,Ptwall_1,Ptwall1_2,Ptwall1_3,Ptwall1_4,Ptfoot_3,Ptfoot_4,Ptfoot_1]]
lstShapeRebarFam=[RF_foot_tr_bot,RF_foot_tr_top,RF_wall_vert_back,RF_wall_vert_front]

if dowels:
    lstShapeRebarFam+=[RF_dowel_back,RF_dowel_front]


lstSectRebarFam=[RF_foot_ln_bot,RF_foot_ln_top,RF_wall_horBottom_back,RF_wall_horBottom_front,RF_wall_horTop_front,RF_wall_horTop_back]
lstSectRebarFam+=[RF_foot_lat_front,RF_foot_lat_dors,RF_wall_top]
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation=Vector(0,5,0))
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation=Vector(0,5,0))
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#sección B-B
lstPtsConcrSect=[[Plfoot_1,Plfoot_2,Plfoot_3,Plfoot_4,Plfoot_1],[Plfoot_2,Plwall_1,Plwall_2,Plfoot_3]]
lstShapeRebarFam=[RF_foot_ln_bot,RF_foot_ln_top,RF_wall_top]
lstSectRebarFam=[RF_foot_tr_bot,RF_foot_tr_top]
lstSectRebarFam+=[RF_foot_lat_toe,RF_foot_lat_heel]
#vTranslation=Vector(10,5,0))

# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(lWall+1,5,0))

#SECCIÓN HORIZONTAL POR LA BASE DEL MURO
lstPtsConcrSect=[[Ph_1,Ph1_2,Ph1_3,Ph_4,Ph_1]]
lstShapeRebarFam=[RF_wall_horBottom_front,RF_wall_horBottom_back]
lstSectRebarFam=[RF_wall_vert_back,RF_wall_vert_front]
# vTranslation=Vector(0,0,0)
# for rf in lstShapeRebarFam:
#     rf.drawLstRebar(vTranslation)

    
# for rf in lstSectRebarFam:
#     rf.drawSectBars(vTranslation)


rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0))


#SECCIÓN HORIZONTAL SUPERIOR
lstPtsConcrSect=[[Ph_1,Ph2_2,Ph2_3,Ph_4,Ph_1]]
lstShapeRebarFam=[RF_wall_horTop_front,RF_wall_horTop_back]
lstSectRebarFam=[]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(lWall+1,0,0))

#SECCIÓN HORIZONTAL ZAPATA
lstPtsConcrSect=[[Ph_1,Phf_2,Phf_3,Ph_4,Ph_1]]
lstShapeRebarFam=[RF_foot_lat_heel,RF_foot_lat_toe,RF_foot_lat_front,RF_foot_lat_dors]
lstSectRebarFam=[]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(2*lWall+2,0,0))

   #BAR SCHEDULE

#altura de las filas
#altura textos
schedulewidth=sum(scheduleCfg.widthColumns)
pntSchedule=Vector((nmbAleta-1)*(schedulewidth+10),0,0)
rb.barSchedule(lstRebarFam,scheduleCfg,title=titSchedule,pntTLcorner=pntSchedule,doc=docDespiece)

# Bar quantities for PyCost
#rb.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
