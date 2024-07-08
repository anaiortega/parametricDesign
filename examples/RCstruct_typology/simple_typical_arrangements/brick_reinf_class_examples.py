# -*- coding: utf-8 -*-
from __future__ import division
from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import  draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Generic brick 2'
titSchedule=estrName.upper()

width=4 #dimension of the slab in the direction of the transversal rebars
length=5 #dimension of the slab in the direction of the longitudinal rebars
thickness=0.4  #thickness of the slab
# bottom transverse rebars data
botTrnsRb=trcm.brkRbFam(fi=20e-3,s=0.15,Id='1',gapStart=0.5,extrShapeStart='anc90_posGood_tens',extrShapeEnd='anc90_posGood_tens',position='good',vectorLRef=Vector(-0.3,-0.35),closedStart=False,closedEnd=False) 
# top transverse rebars data
topTrnsRb=trcm.brkRbFam(fi=16e-3,s=0.15,Id='3',extrShapeStart='lap270_posPoor_tens',extrShapeEnd='lap0_posPoor_tens_perc100',position='poor',closedStart=False,closedEnd=False)#,fixLengthEnd=2) 
# bottom longitudinal rebars data
botLnRb=trcm.brkRbFam(fi=16e-3,s=0.20,Id='2',distRFstart=0.1,distRFend=0.5,fixLengthStart=0.5,gapEnd=2,extrShapeEnd='lap45_posGood_compr',position='good',vectorLRef=Vector(0.4,-0.20),closedStart=True,closedEnd=True)
# top longitudinal rebars data
topLnRb=trcm.brkRbFam(fi=16e-3,s=0.20,Id='4',distRFstart=0.1,distRFend=0.3,extrShapeEnd='lap180_posPoor_tens_perc50',position='poor',closedStart=True,closedEnd=False)

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section

docName='genericBrick'
FreeCAD.newDocument(docName)
scale=1/50
reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

# horizontal section constant thickness
brick=trcm.genericBrickReinf(
    width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    reinfCfg=reinfCfg,
    angTrns=0,
    angLn=0,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    )

stYmax=brick.drawTransvConcrSectYmax()
lnXmax=brick.drawLongConcrSectXmax()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()

# inclined section constant thickness
brick.anchPtTrnsSect+=Vector(0,2)
brick.anchPtLnSect+=Vector(0,2)
brick.angTrns=30
brick.angLn=10
brick.drawTransvConcrSectYmax()
brick.drawLongConcrSectXmax()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()


# horizontal section sloped faces
brick.anchPtTrnsSect+=Vector(0,4)
brick.anchPtLnSect+=Vector(0,4)
brick.angTrns=0
brick.angLn=0
brick.trSlopeBottFace=-0.25/1
brick.trSlopeTopFace=0.15/1
brick.drawTransvConcrSectYmax()
brick.drawLongConcrSectXmax()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()

# inclined section inverted sloped faces
brick.anchPtTrnsSect+=Vector(0,3)
brick.anchPtLnSect+=Vector(0,3)
brick.thickness=1.3
brick.angTrns=90
brick.angLn=90
brick.trSlopeBottFace=0.2/2
brick.trSlopeTopFace=-0.1/2
brick.drawTransvConcrSectYmax()
brick.drawLongConcrSectXmax()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()

# horizontal section, constant thickness, sloped edge
brick.anchPtTrnsSect+=Vector(0,10)
brick.anchPtLnSect+=Vector(3,10)
brick.thickness=0.4
brick.angTrns=0
brick.angLn=0
brick.trSlopeBottFace=None
brick.trSlopeTopFace=None
brick.slopeEdge=1/2
brick.drawTransvConcrSectYmax()
brick.drawLongConcrSectXmax()
brick.drawTransvConcrSectYmin()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()
brick.drawBottomVarLongRF()
brick.drawTopVarLongRF()

# inclined section, sloped faces, sloped edge
brick.anchPtTrnsSect+=Vector(0,10)
brick.anchPtLnSect+=Vector(0,10)
brick.thickness=0.25
brick.angTrns=-90
brick.angLn=-90
brick.trSlopeBottFace=-0.1/1
brick.trSlopeTopFace=0.15/1
brick.slopeEdge=1/2
brick.drawTransvConcrSectYmax()
brick.drawTransvConcrSectYmin()
brick.drawLongConcrSectXmax()
brick.drawLongConcrSectXmin()
brick.drawBottomTransvRF()
brick.drawTopTransvRF()
brick.drawBottomLongRF()
brick.drawTopLongRF()
brick.drawBottomVarLongRF()
brick.drawTopVarLongRF()



