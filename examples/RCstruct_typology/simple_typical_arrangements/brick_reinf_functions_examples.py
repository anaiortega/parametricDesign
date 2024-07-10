# -*- coding: utf-8 -*-
from __future__ import division

from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import  draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Generic brick'
titSchedule=estrName.upper()

FreeCAD.newDocument(estrName+'genericBrick')
scale=1/50
reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

width=4 #dimension of the slab in the direction of the transversal rebars
length=5 #dimension of the slab in the direction of the longitudinal rebars
thickness=0.4  #thickness of the slab
# bottom transverse rebars data
botTrnsRb=trcm.brkRbFam(Id=None,fi=20e-3,s=0.15,distRFstart=0.2,distRFend=0,gapStart=-2,extrShapeStart='anc0_posPoor_compr',position='good',vectorLRef=Vector(0.3,-0.2),closedStart=False,addTxt2Label='added text')
# top transverse rebars data
botLnRb=trcm.brkRbFam(fi=16e-3,s=0.20,distRFstart=0.1,distRFend=0.5,extrShapeStart='anc0_posPoor_compr',position='good',vectorLRef=Vector(0.1,-0.3),closedStart=False,closedEnd=True)
# bottom longitudinal rebars data
topTrnsRb=trcm.brkRbFam(Id=None,fi=20e-3,s=0.15,distRFstart=0.2,distRFend=0.1,extrShapeEnd='anc90_posPoor_compr',position='poor',vectorLRef=Vector(-0.3,0.15))
# top longitudinal rebars data
topLnRb=trcm.brkRbFam(Id=None,fi=16e-3,s=0.20,distRFstart=0.1,distRFend=0.3,extrShapeEnd='anc270_posGood_tens',position='poor',vectorLRef=Vector(-0.2,0.3),closedEnd=True)

# stirrups holding transverse rebars
stirrHoldTr=trcm.brkStirrFam(Id='5',fi=8e-3 ,sRealSh=0.30 ,sPerp=0.15 ,nStirrRealSh= 3 ,nStirrPerp=4 ,widthStirr=0.25,dispRealSh= 0,dispPerp=0.1,vectorLRef=Vector(0.3,-0.5),rightSideLabelLn=False,rightSideCover=False)
stirrHoldTr2=trcm.brkStirrFam(Id='5',fi=10e-3 ,sRealSh=0.30 ,sPerp=0.15 ,nStirrRealSh= 3 ,nStirrPerp=4 ,widthStirr=0.25,dispRealSh= 1.5,dispPerp=1,vectorLRef=Vector(0.3,-0.5),rightSideLabelLn=False,rightSideCover=False)

# stirrups holding longitudinal rebars
stirrHoldLn=trcm.brkStirrFam(Id='6' ,fi=10e-3 ,sRealSh=0.20 ,sPerp=0.30 ,nStirrRealSh= 5 ,nStirrPerp=2 ,widthStirr= 0.40,dispRealSh= 1.5,dispPerp=1.3,vectorLRef=Vector(0.2,-0.5),rightSideLabelLn=False,rightSideCover=False,addTxt2Label='note')

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section
lstRebarFam=list()
lstStirrupFam=list()

# orthohedron
lstRebarFam1,lstStirrupFam1,newStartId=trcm.constant_thickness_brick_reinf(
    width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    reinfCfg=reinfCfg,
    angTrns=20,
    angLn=40,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    lstStirrHoldTrReinf=[stirrHoldTr,stirrHoldTr2],
    lstStirrHoldLnReinf=[stirrHoldLn],
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    startId=1
)
lstRebarFam+=lstRebarFam1
lstStirrupFam+=lstStirrupFam1

# sloped faces brick
botTrnsRb.identifier=None; topTrnsRb.identifier=None
botLnRb.identifier=None;topLnRb.identifier=None
anchPtTrnsSect+=Vector(0,4)
anchPtLnSect+=Vector(0,4)
lstRebarFam2,lstStirrupFam2,newStartId=trcm.sloped_faces_brick_reinf(
    width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    reinfCfg=reinfCfg,
    angTrns=20,
    angLn=40,
    trSlopeBottFace=-0.3/1,
    trSlopeTopFace=0.2/1,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    startId=11
)
lstRebarFam+=lstRebarFam2
lstStirrupFam+=lstStirrupFam2


# constant thickness, sloped edge brick
botTrnsRb.identifier=None; topTrnsRb.identifier=None
botLnRb.identifier=None;topLnRb.identifier=None
anchPtTrnsSect+=Vector(0,4)
anchPtLnSect+=Vector(0,4)
lstRebarFam3,lstStirrupFam3,newStartId=trcm.sloped_edge_constant_thickness_brick_reinf(
   width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    reinfCfg=reinfCfg,
    angTrns=20,
    angLn=40,
    slopeEdge=0.2,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    startId=21
)
lstRebarFam+=lstRebarFam3
lstStirrupFam+=lstStirrupFam3

# sloped edge and faces brick
botTrnsRb.identifier=None; topTrnsRb.identifier=None
botLnRb.identifier=None;topLnRb.identifier=None
botTrnsRb.closedStart=True; botTrnsRb.closedEnd=True
topTrnsRb.closedStart=False; topTrnsRb.closedEnd=False
botLnRb.closedStart=False; botLnRb.closedEnd=True
topLnRb.closedStart=True; topLnRb.closedEnd=True
anchPtTrnsSect+=Vector(0,4)
anchPtLnSect+=Vector(0,4)
lstRebarFam4,lstStirrupFam4,newStartId=trcm.sloped_edge_sloped_faces_brick_reinf(
    width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    reinfCfg=reinfCfg,
    slopeEdge=0.2,
    trSlopeBottFace=-0.3/1,
    trSlopeTopFace=0.2/1,
    angTrns=90,
    angLn=90,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    startId=31
)
lstRebarFam+=lstRebarFam4
lstStirrupFam+=lstStirrupFam4
 
doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               schCfg=cfg.XC_scheduleLvarCfg,
               title=titSchedule,
               pntTLcorner=Vector(1,1),
               doc=doc
)
