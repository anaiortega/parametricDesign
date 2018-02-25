# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *


# DATA
#   Geometry
#   Footing
footing_wd=5.00
footing_th=1.00
footing_ln=10.00
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
foot_p7=foot_p5.add(Vector(footing_ln,footing_th))
foot_p8=foot_p5.add(Vector(footing_ln,0))

#rebars definition
gConf=reinf_bars.genericConf(cover=0.05,texSize=0.125,Code='EHE',concrType='HA-30',steelType='B-500',dynamEff='N',decLengths=2,decSpacing=2)

R1=reinf_bars.rebarFamily(
    genConf=gConf,
    identifier='R1',
    diameter=0.016,
    spacing=0.20,
    lstPtsConcrSect=[foot_p1,foot_p4],
    coverSide='l',
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[foot_p5,foot_p8],
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
    anchStart='hook45_posII_compr',
    anchEnd='hook90_posI_tens',
)
R2=reinf_bars.rebarFamily(
    genConf=gConf,
    identifier='R2',
    diameter=0.025,
    spacing=0.20,
    lstPtsConcrSect=[foot_p2,foot_p3],
    fromToExtPts=[foot_p6,foot_p7],
    anchStart='hook270_posI_compr',
    anchEnd='hook225_posII_compr',

)


# Plan of sections
App.newDocument("planRCsections")
#TRANSVERSE SECTION
#section A-A
lstPtsConcrSect=[[foot_p1,foot_p2,foot_p3,foot_p4,foot_p1]]
lstShapeRebarFam=[R1,R2]
lstSectRebarFam=[]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#LONGITUDINAL SECTION
#section B-B
lstPtsConcrSect=[[foot_p5,foot_p6,foot_p7,foot_p8,foot_p5]]
lstShapeRebarFam=[]
lstSectRebarFam=[R1,R2]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,5,0))
