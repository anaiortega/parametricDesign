# -*- coding: utf-8 -*-
from __future__ import division
from FreeCAD import Vector
from freeCAD_civil import reinf_bars as rb
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import  draw_config as cfg
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C
cover=0.035; cfg.defaultReinfConf.cover=cover

estrName='Generic cylinder'
titSchedule=estrName.upper()

radius=1
length=15

# longitudinal rebars
lnRb1=trcm.brkRbFam(fi=25e-3,s=0.15,distRFstart=1,closedStart=False,lateralCover=0.15,vectorLRef=Vector(-1.2,0.5),gapStart=1,gapEnd=0,extrShapeStart='fix90_len200',maxLrebar=9,position='good',compression=True,drawSketch=False)
lnRb2=trcm.brkRbFam(fi=16e-3,s=0.15,distRFstart=1,closedStart=False,lateralCover=0.15,vectorLRef=Vector(-1.2,1),gapStart=0,gapEnd=0,extrShapeStart='fix90_len200',maxLrebar=9,position='good',compression=True,drawSketch=False)
lnRb3=trcm.brkRbFam(fi=20e-3,nmbBars=15,vectorLRef=Vector(1,-0.8),extrShapeStart='fix90_len200',maxLrebar=10,position='good')
# stirrups
stirrF_1=trcm.brkStirrFam(fi=8e-3,sPerp=0.15,nStirrPerp=10,dispPerp=0.5,rightSideLabelLn=True,addL2closed=0.20,closed=True,vectorLRef=Vector(0.3,-0.3))
stirrF_2=trcm.brkStirrFam(fi=10e-3,sPerp=0.20,nStirrPerp=8,dispPerp=6,rightSideLabelLn=True,addL2closed=0.20,closed=True,vectorLRef=Vector(0.3,-0.7))

                          
docName='genericCyl'
FreeCAD.newDocument(docName)
scale=1/50
reinfCfg=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

lstRebarFam=list()
lstStirrupFam=list()
anchPtTrnsSect=Vector(0,0)
anchPtLnSect=anchPtTrnsSect+Vector(4*radius,0)
lstRebFam,lstStirrFam,newStartId=trcm.cyl_beam_reinf(radius=radius,
                                                     length=length,
                                                     anchPtTrnsSect=anchPtTrnsSect,
                                                     anchPtLnSect=anchPtLnSect,
                                                     reinfCfg=reinfCfg,
                                                     angLn=45,
                                                     lstLnRb=[lnRb1,lnRb2,lnRb3],
                                                     lstStirrReinf=[stirrF_1,stirrF_2],
                                                     drawConcrTrSect=True,
                                                     drawConcrLnSect=[1,2,3],
                                                     startId=1,
                                                     clearDistRbLayers=None,
                                                     aggrSize=20e-3)

lstRebarFam+=lstRebFam
lstStirrupFam+=lstStirrFam

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               schCfg=cfg.XC_scheduleLvarCfg,
               title=titSchedule,
               pntTLcorner=Vector(1,1),
               doc=doc
)
