# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *

# Abutment
# Nomenclature:
# _th: thickness
# _wd: width
# _ln: length
# _hg: height
# _sl: slope (H/V)
#
# WW: wing wall
# L: left, R: right
# AS: approach slab
# BW: back wall

# DATA
#   Geometry
#   Footing
footing_wd=5.00
footing_th=1.00
footingToe=1.75
#   Stem wall
stemW_th=1.00
stemW_ln=8.50
stemW_hg_LWW=3.93
stemW_hg_RWW=4.15
brSeat_wd=0.6+0.5
#   Back wall
backW_hg=1.61
backW_hg_up=0.55
backW_hg_down=0.50
backW_sl=(.5+.6+.3+.3-1.0)/0.7
backW_wd=0.3+0.3
ASseat_wd=0.3
#   Low walls
LlowW_hg=1.32
RlowW_hg=1.34
LlowW_th=0.30
RlowW_th=0.30
#   Approach slab
aprSl_ln=5.00
aprSl_th=0.3
aprSl_sl=-10.0
gap_BW_AS=0.05
gap_WW_AS=0.10

#   Left wing wall
LwingW_ln=3.71
LwingW_sl_up=LwingW_ln/(136.94-137.09)
LwingW_sl_down=3/2.0
LwingW_hg=0.5
#   Right wing wall
RwingW_ln=4.85
RwingW_sl_up=RwingW_ln/(137.12-137.32)
RwingW_sl_down=3/2.0
RwingW_hg=0.5
# End geometry data
hTextsArmados=0.125

#Data reinforcements
cover=0.03
bendRad={'0.008':0.03,'0.010':0.03,'0.012':0.03,'0.014':0.03,'0.016':0.03,'0.020':0.03,'0.025':0.03}   #bending radius
foot_LB_01_dat={'fi':0.016,'s':0.30,'id':'1'}
foot_LB_02_dat={'fi':0.016,'s':0.30,'id':'2'}
foot_TB_01_dat={'fi':0.012,'s':0.125,'id':'3'}
foot_LT_01_dat={'fi':0.012,'s':0.15,'id':'4'}
foot_TT_01_dat={'fi':0.012,'s':0.125,'id':'5'}
foot_TL_01_dat={'fi':0.012,'s':0.125,'id':'6'}
foot_TL_02_dat={'fi':0.012,'s':0.125,'id':'7'}
stemW_VF_01_dat={'fi':0.008,'s':0.15,'id':'9'}
stemW_VF_02_dat={'fi':0.008,'s':0.15,'id':'10'}
stemW_HF_01_dat={'fi':0.016,'s':0.125,'id':'10'}
stemW_VB_01_dat={'fi':0.016,'s':0.15,'id':'12'}
stemW_VB_02_dat={'fi':0.016,'s':0.15,'id':'13'}
stemW_HB_01_dat={'fi':0.016,'s':0.125,'id':'14'}
backW_VB_01_dat={'fi':0.012,'s':0.15,'id':'15'}
backW_VF_01_dat={'fi':0.012,'s':0.15,'id':'16'}
backW_HB_01_dat={'fi':0.012,'s':0.10,'id':'17'}
backW_HF_01_dat={'fi':0.012,'s':0.10,'id':'18'}
stemW_TT_01_dat={'fi':0.020,'s':0.125,'id':'20'}
LwingW_HB_01_dat={'fi':0.010,'s':0.125,'id':'22'}
LwingW_HB_02_dat={'fi':0.010,'s':0.125,'id':'23'}
LwingW_HB_03_dat={'fi':0.010,'s':0.125,'id':'24'}
LwingW_HF_01_dat={'fi':0.010,'s':0.125,'id':'25'}
LwingW_VS_01_dat={'fi':0.010,'s':0.15,'id':'26'}
LwingW_HT_01_dat={'fi':0.020,'nmb':4,'id':'27'}
LwingW_HB_01_dat={'fi':0.012,'nmb':4,'id':'28'}
stemW_VL_01_dat={'fi':0.012,'s':0.125,'id':'29'}
stemW_VL_02_dat={'fi':0.012,'s':0.125,'id':'30'}
LwingW_VB_01_dat={'fi':0.012,'s':0.125,'id':'31'}

RwingW_HB_01_dat={'fi':0.010,'s':0.125,'id':'32'}
RwingW_HB_02_dat={'fi':0.012,'s':0.125,'id':'33'}
RwingW_HB_03_dat={'fi':0.012,'s':0.125,'id':'34'}
RwingW_HF_01_dat={'fi':0.010,'s':0.125,'id':'35'}
RwingW_VS_01_dat={'fi':0.010,'s':0.15,'id':'36'}
RwingW_HT_01_dat={'fi':0.025,'nmb':4,'id':'37'}
RwingW_HB_01_dat={'fi':0.012,'nmb':4,'id':'38'}
stemW_VL_03_dat={'fi':0.012,'s':0.125,'id':'39'}
stemW_VL_04_dat={'fi':0.012,'s':0.125,'id':'40'}
RwingW_VB_01_dat={'fi':0.012,'s':0.125,'id':'31'}

anc1=0.4
anc2=0.5
solap1=0.5
solap2=0.7
# END DATA


#Points
#    Footing
#section A-A
foot_p1=Vector(0,0)
foot_p2=foot_p1.add(Vector(0,footing_th))
foot_p3=foot_p1.add(Vector(footing_wd,footing_th))
foot_p4=foot_p1.add(Vector(footing_wd,0))
#section B-B
foot_p5=Vector(0,0)
foot_p6=foot_p5.add(Vector(0,footing_th))
foot_p7=foot_p5.add(Vector(stemW_ln,footing_th))
foot_p8=foot_p5.add(Vector(stemW_ln,0))
#section C-C and D-D
foot_p9=Vector(footing_wd,0)
foot_p10=foot_p9.add(Vector(0,footing_th))
foot_p11=foot_p9.add(Vector(-footing_wd,footing_th))
foot_p12=foot_p9.add(Vector(-footing_wd,0))

#   Stem and back walls
#Section A-A
stemW_mean_hg=(stemW_hg_LWW+stemW_hg_RWW)/2.0
Hcorbel=brSeat_wd+backW_wd-stemW_th
wall_p1=foot_p2.add(Vector(footingToe,0))
wall_p2=wall_p1.add(Vector(0,stemW_mean_hg))
wall_p3=wall_p2.add(Vector(brSeat_wd,0))
wall_p4=wall_p3.add(Vector(0,backW_hg))
wall_p5=wall_p4.add(Vector(backW_wd-ASseat_wd))
wall_p6=wall_p5.add(Vector(0,-backW_hg_up))
wall_p7=wall_p6.add(Vector(ASseat_wd,0))
wall_p8=wall_p3.add(Vector(backW_wd,-backW_hg_down))                    
wall_p9=wall_p8.add(Vector(-Hcorbel,-Hcorbel/backW_sl))
wall_p10=wall_p1.add(Vector(stemW_th,0))
#Section B-B
wall_p11=foot_p6.add(Vector(0,stemW_hg_LWW))
wall_p12=wall_p11.add(Vector(0,LlowW_hg))
wall_p13=wall_p12.add(Vector(LlowW_th,0))
wall_p14=wall_p13.add(Vector(0,-LlowW_hg))

wall_p18=foot_p7.add(Vector(0,stemW_hg_RWW))
wall_p17=wall_p18.add(Vector(0,RlowW_hg))
wall_p16=wall_p17.add(Vector(-RlowW_th,0))
wall_p15=wall_p16.add(Vector(0,-RlowW_hg))
#    Left wing Wall
lwing_p1=foot_p10.add(Vector(-footingToe,0))
lwing_p2=lwing_p1.add(Vector(0,stemW_hg_LWW))
lwing_p3=lwing_p2.add(Vector(0,LlowW_hg))
lwing_p4=lwing_p3.add(Vector(-brSeat_wd,0))
lwing_p5=lwing_p4.add(Vector(0,backW_hg-LlowW_hg))
lwing_p6=lwing_p5.add(Vector(-LwingW_ln,LwingW_ln/LwingW_sl_up))
lwing_p7=lwing_p6.add(Vector(0,-LwingW_hg))
lwing_p8=lwing_p7.add(Vector(LwingW_ln,-LwingW_ln/RwingW_sl_down))
lwing_p9=lwing_p1.add(Vector(-stemW_th,0))

#    Right wing Wall
rwing_p1=foot_p10.add(Vector(-footingToe,0))
rwing_p2=rwing_p1.add(Vector(0,stemW_hg_LWW))
rwing_p3=rwing_p2.add(Vector(0,LlowW_hg))
rwing_p4=rwing_p3.add(Vector(-brSeat_wd,0))
rwing_p5=rwing_p4.add(Vector(0,backW_hg-LlowW_hg))
rwing_p6=rwing_p5.add(Vector(-RwingW_ln,RwingW_ln/RwingW_sl_up))
rwing_p7=rwing_p6.add(Vector(0,-RwingW_hg))
rwing_p8=rwing_p7.add(Vector(RwingW_ln,-RwingW_ln/RwingW_sl_down))
rwing_p9=rwing_p1.add(Vector(-stemW_th,0))

#   Approach slab
#Section A-A
AS_p1=wall_p6.add(Vector(gap_BW_AS,gap_BW_AS))
AS_p2=AS_p1.add(Vector(0,aprSl_th))
AS_p3=AS_p2.add(Vector(aprSl_ln,aprSl_ln/aprSl_sl))
AS_p4=AS_p3.add(Vector(0,-aprSl_th))


# Reinforcement footing
foot_LB_01=reinf_bars.rebarFamily(
    identifier=foot_LB_01_dat['id'],
    diameter=foot_LB_01_dat['fi'],
    spacing=foot_LB_01_dat['s'],
    lstPtsConcrSect=[foot_p2,foot_p1,foot_p4,foot_p3],
    lstCover=[cover,cover,cover],
    coverSide='l',
    bendingRad= bendRad[str(foot_LB_01_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p5,foot_p8],
    recSec=cover,
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,0.3),
#    lstPtsConcrSect2=[Ptzap_2p,Ptzap_1,Ptzap_4,Ptzap_3p]
)

foot_LB_02=reinf_bars.rebarFamily(
    identifier=foot_LB_02_dat['id'],
    diameter=foot_LB_02_dat['fi'],
    spacing=foot_LB_02_dat['s'],
    lstPtsConcrSect=[foot_p4.add(Vector(-footingToe-stemW_th,0)),foot_p4,foot_p3],
    lstCover=[cover,cover],
    coverSide='l',
    bendingRad= bendRad[str(foot_LB_02_dat['fi'])],
    gapStart=+0.50,
    gapEnd=-0.20,
    vectorLRef=Vector(-0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p5,foot_p8],
    recSec=cover,
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,0.3),
)

foot_TB_01=reinf_bars.rebarFamily(
    identifier=foot_TB_01_dat['id'],
    diameter=foot_TB_01_dat['fi'],
    spacing=foot_TB_01_dat['s'],
    lstPtsConcrSect=[foot_p6,foot_p5,foot_p8,foot_p7],
    lstCover=[cover,cover+foot_LB_01_dat['fi'],cover],
    coverSide='l',
    bendingRad= bendRad[str(foot_TB_01_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p1,foot_p4],
    recSec=cover+foot_LB_01_dat['fi'],
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,-0.3),
)

foot_LT_01=reinf_bars.rebarFamily(
    identifier=foot_LT_01_dat['id'],
    diameter=foot_LT_01_dat['fi'],
    spacing=foot_LT_01_dat['s'],
    lstPtsConcrSect=[foot_p1,foot_p2,foot_p3,foot_p4],
    lstCover=[cover,cover,cover],
    coverSide='r',
    bendingRad= bendRad[str(foot_LT_01_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p6,foot_p7],
    recSec=cover,
    lateralCover=cover,
    sectBarsSide='r',
    vectorLRefSec=Vector(0.3,0.3),
#    lstPtsConcrSect2=[Ptzap_2p,Ptzap_1,Ptzap_4,Ptzap_3p]
)

foot_TT_01=reinf_bars.rebarFamily(
    identifier=foot_TT_01_dat['id'],
    diameter=foot_TT_01_dat['fi'],
    spacing=foot_TT_01_dat['s'],
    lstPtsConcrSect=[foot_p5,foot_p6,foot_p7,foot_p8],
    lstCover=[cover,cover+foot_LT_01_dat['fi'],cover],
    coverSide='r',
    bendingRad= bendRad[str(foot_TT_01_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p2,foot_p3],
    recSec=cover+foot_LT_01_dat['fi'],
    lateralCover=cover,
    sectBarsSide='r',
    vectorLRefSec=Vector(-0.3,0.3),
)

foot_TL_01=reinf_bars.rebarFamily(
    identifier=foot_TL_01_dat['id'],
    diameter=foot_TL_01_dat['fi'],
    spacing=foot_TL_01_dat['s'],
    lstPtsConcrSect=[foot_p6,foot_p5,foot_p8,foot_p7],
    lstCover=[cover,cover+foot_LB_01_dat['fi'],cover],
    coverSide='l',
    bendingRad= bendRad[str(foot_TL_01_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p4,foot_p3],
    recSec=cover+foot_LB_01_dat['fi'],
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(0.3,0.3),
)
foot_TL_02=reinf_bars.rebarFamily(
    identifier=foot_TL_02_dat['id'],
    diameter=foot_TL_02_dat['fi'],
    spacing=foot_TL_02_dat['s'],
    lstPtsConcrSect=[foot_p6,foot_p5,foot_p8,foot_p7],
    lstCover=[cover,cover+foot_LB_01_dat['fi'],cover],
    coverSide='l',
    bendingRad= bendRad[str(foot_TL_02_dat['fi'])],
    gapStart=-0.20,
    gapEnd=-0.20,
    vectorLRef=Vector(0.5,-0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p1,foot_p2],
    recSec=cover+foot_LB_01_dat['fi'],
    lateralCover=cover,
    sectBarsSide='r',
    vectorLRefSec=Vector(-0.3,0.3),
)

#  Stem wall reinforcement
ptaux=wall_p1.add(Vector(0,-footing_th))
stemW_VF_01=reinf_bars.rebarFamily(
    identifier=stemW_VF_01_dat['id'],
    diameter=stemW_VF_01_dat['fi'],
    spacing=stemW_VF_01_dat['s'],
    lstPtsConcrSect=[ptaux.add(Vector(-anc1,0)),ptaux,wall_p1],
    lstCover=[cover,-cover],
    coverSide='l',
    bendingRad= bendRad[str(stemW_VF_01_dat['fi'])],
    gapStart=0,
    gapEnd=solap1,
    vectorLRef=Vector(0.5,0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p5,foot_p8],
    recSec=cover+foot_LB_01_dat['fi']+foot_TB_01_dat['fi'],
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
)
stemW_VF_02=reinf_bars.rebarFamily(
    identifier=stemW_VF_02_dat['id'],
    diameter=stemW_VF_02_dat['fi'],
    spacing=stemW_VF_02_dat['s'],
    lstPtsConcrSect=[wall_p1,wall_p2,wall_p3.add(Vector(backW_wd,0)),wall_p8,wall_p9],
    lstCover=[cover,cover,cover,cover],
    coverSide='r',
    bendingRad= bendRad[str(stemW_VF_02_dat['fi'])],
    gapStart=0,
    gapEnd=anc2,
    vectorLRef=Vector(0.5,0.5),
    hText=hTextsArmados,
    fromToExtPts=[foot_p5,foot_p8],
    recSec=cover,
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
)
stemW_HF_01=reinf_bars.rebarFamily(
    identifier=stemW_HF_01_dat['id'],
    diameter=stemW_HF_01_dat['fi'],
    spacing=stemW_HF_01_dat['s'],
    lstPtsConcrSect=[foot_p6.add(Vector(0,1)),foot_p6,foot_p7,foot_p7.add(Vector(0,1))],
    lstCover=[cover,cover,cover],
    coverSide='r',
    bendingRad= bendRad[str(stemW_HF_01_dat['fi'])],
    vectorLRef=Vector(0.5,0.5),
    fixLengthStart=0.2,
    fixLengthEnd=0.2,
    hText=hTextsArmados,
    fromToExtPts=[foot_p5,foot_p8],
    recSec=cover,
    lateralCover=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
)

'''
# Added 16.01.2018
#Generate the attributes wire for each family that represent the rebar
#(if not generated here it will be generated while drawing the sections or
# the bar schedule
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]
for fa in listafamiliasArmad:
    fa.createRebar()
# end  16.01.2018
'''

# Plan of sections
App.newDocument("planRCsections")
#SECCIONES TRANSVERSALES
#section A-A
lstPtsConcrSect=[[foot_p1,foot_p2,wall_p1,wall_p2,wall_p3,wall_p4,wall_p5,wall_p6,wall_p7,wall_p8,wall_p9,wall_p10,foot_p3,foot_p4,foot_p1],[AS_p1,AS_p2,AS_p3,AS_p4,AS_p1]]
lstShapeRebarFam=[foot_LB_01,foot_LB_02,foot_LT_01,stemW_VF_01,stemW_VF_02]
lstSectRebarFam=[foot_TB_01,foot_TT_01,foot_TL_01,foot_TL_02,stemW_HF_01]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#SECCIONES LONGITUDINALES
#section B-B
lstPtsConcrSect=[[foot_p5,foot_p6,foot_p7,foot_p8,foot_p5],[foot_p6,wall_p11,wall_p12,wall_p13,wall_p14,wall_p15,wall_p16,wall_p17,wall_p18,foot_p7]]
lstShapeRebarFam=[]
lstSectRebarFam=[]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,5,0))

#Left wing wall. Section C-C
lstPtsConcrSect=[[foot_p9,foot_p10,lwing_p1,lwing_p3,lwing_p4,lwing_p5,lwing_p6,lwing_p7,lwing_p8,lwing_p9,foot_p11,foot_p12,foot_p9]]
lstShapeRebarFam=[]
lstSectRebarFam=[]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(20,5,0))

#Right wing wall. Section D-D
lstPtsConcrSect=[[foot_p9,foot_p10,rwing_p1,rwing_p3,rwing_p4,rwing_p5,rwing_p6,rwing_p7,rwing_p8,rwing_p9,foot_p11,foot_p12,foot_p9]]
lstShapeRebarFam=[]
lstSectRebarFam=[]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,5,0))



'''
   #BAR SCHEDULE
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hText=2.5
listafamiliasArmad=[Z1_1,Z1_2,Z1_3,Z1_4,Z1_7,Z1_8,M1_1,M1_2,M1_3,M1_4,M1_5,M1_6,M1_7,M1_8,M1_9]
reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hText,hTextSketch=hText)

# Bar quantities for PyCost
reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/pruebas/presupuesto_rev2/quant_arm.py')
'''
