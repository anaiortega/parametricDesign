# -*- coding: utf-8 -*-
from __future__ import division
from FreeCAD import Vector
from parametric_design.freeCAD_civil import reinf_bars as rb
from parametric_design.freeCAD_civil.structures import typical_RC_members as trcm
from parametric_design.freeCAD_civil import  draw_config as cfg
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C
cover=0.035; cfg.defaultReinfConf.cover=cover

estrName='Generic cylinder'
titSchedule=estrName.upper()

radius=1
length=15

# longitudinal rebars
lnRb=trcm.brkRbFam(fi=20e-3,nmbBars=15,vectorLRef=Vector(0.5,radius+0.3),extrShapeStart='fix90_len200',maxLrebar=10,position='good')
lnRb2=trcm.brkRbFam(fi=25e-3,s=0.15,distRFstart=1,closedStart=False,lateralCover=0.15,vectorLRef=Vector(-1.2,0.5),gapStart=1,gapEnd=0,extrShapeStart='fix90_len200',maxLrebar=9,position='good',compression=True,drawSketch=False)
# stirrups
stirrF_1=trcm.brkStirrFam(fi=8e-3,sPerp=0.15,nStirrPerp=10,dispPerp=0.5,rightSideLabelLn=True,addL2closed=0.20,closed=True,vectorLRef=Vector(0.3,0.3))
stirrF_2=trcm.brkStirrFam(fi=10e-3,sPerp=0.20,nStirrPerp=8,dispPerp=6,rightSideLabelLn=True,addL2closed=0.20,closed=True,vectorLRef=Vector(0.3,-0.3))
stirrF_3=trcm.brkStirrFam(fi=12e-3,sPerp=0.55,nStirrPerp=20,dispPerp=0.1,rightSideLabelLn=True,addL2closed=0.20,closed=True,fixAnchorStart='fix45_len150',vectorLRef=Vector(0.3,-0.3))


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

cyl=trcm.genericCylReinf(radius=radius,
                         length=length,
                         anchPtTrnsSect=anchPtTrnsSect,
                         anchPtLnSect=anchPtLnSect,
                         reinfCfg=reinfCfg,
                         angLn=0,
                         lnRb=lnRb,
                         lstStirrReinf=[stirrF_1,stirrF_2],
                         drawConcrLnSect=[2,4],
                         startId=1)
cyl.drawTransvConcrSect()
cyl.drawLongConcrSect()
cyl.drawLnRF()
lstStirr=cyl.drawStirrF()

lstRebarFam+=[cyl.lnRb]
lstStirrupFam+=lstStirr
anchPtTrnsSect+=Vector(0,4*radius)
anchPtLnSect+=Vector(0,3*radius)
cyl2=trcm.genericCylReinf(radius=radius,
                         length=length,
                         anchPtTrnsSect=anchPtTrnsSect,
                         anchPtLnSect=anchPtLnSect,
                         reinfCfg=reinfCfg,
                         angLn=75,
                         lnRb=lnRb2,
                         lstStirrReinf=[stirrF_3],
                         drawConcrLnSect=True,
                          startId=cyl.startId)
cyl2.drawTransvConcrSect()
cyl2.drawLongConcrSect()
cyl2.drawLnRF()
lstStirr2=cyl2.drawStirrF()
lstRebarFam+=[cyl2.lnRb]
lstStirrupFam+=lstStirr2

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               schCfg=cfg.XC_scheduleLvarCfg,
               title=titSchedule,
               pntTLcorner=Vector(1,1),
               doc=doc
)
