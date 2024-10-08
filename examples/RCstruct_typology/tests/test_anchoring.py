# -*- coding: utf-8 -*-

import Part, FreeCAD, math
import Draft
from parametric_design.freeCAD_civil import draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C


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
gConf=cfg.reinfConf(cover=0.05,xcConcr=concr,xcSteel=steel,texSize=0.125,Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)

R1=reinf_bars.rebarFamily(
    reinfCfg=gConf,
    identifier='R1',
    diameter=0.016,
    spacing=0.20,
    lstPtsConcrSect=[foot_p1,foot_p4],
    rightSideCover=False,
    vectorLRef=Vector(0.5,-0.5),
    fromToExtPts=[foot_p5,foot_p8],
    rightSideSectBars=False,
    extrShapeStart='anc45_posPoor_compr',
    extrShapeEnd='anc90_posGood_tens',
)
R2=reinf_bars.rebarFamily(
    reinfCfg=gConf,
    identifier='R2',
    diameter=0.025,
    spacing=0.20,
    lstPtsConcrSect=[foot_p2,foot_p3],
    fromToExtPts=[foot_p6,foot_p7],
    extrShapeStart='anc270_posGood_compr',
    extrShapeEnd='anc225_posPoor_compr',

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
