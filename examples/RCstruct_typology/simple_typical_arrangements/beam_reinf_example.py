# -*- coding: iso-8859-1 -*-
from __future__ import division

from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import  draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Generic beam'
titSchedule=estrName.upper()

FreeCAD.newDocument(estrName+'genericBeam')
scale=1/50
reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

width=0.7 # beam cross-section width
height=1.5 # beam cross-section height
length=13 # beam length
angTrns=20 # angle (degrees) between the horizontal and the cross-section width dimension
angLn=90

# Bottom rebars
botRbLy1={'id':'1','fi':32e-3,'nmbBars':4,'position':'good','gapStart':-1.0,'gapEnd':2.0}
botRbLy2={'id':'2','fi':25e-3,'nmbBars':5,'position':'good','extrShapeStart':'fix90_len500','lateralCover':0.1}
botRbLy3={'id':'3','fi':16e-3,'nmbBars':4,'position':'good','extrShapeEnd':'fix45_len420'}

# Top rebars
topRbLy1={'id':'4','fi':25e-3,'nmbBars':5,'position':'poor','vectorLRef':Vector(-0.5,0.5),'closedStart':True,'closedEnd':True}
topRbLy2={'id':'5','fi':20e-3,'nmbBars':4,'position':'poor','nMembers':3,'closedStart':True}#,'extrShapeStart':'anc90_posPoor_tens'}

#Lateral rebars (left side)
latLRbLy1={'id':'6','fi':12e-3,'s':0.20,'position':'good','extensionLength':0.2,'vectorLRef':Vector(-0.5,0.5)}
latLRbLy2={'id':'7','fi':10e-3,'s':0.10,'position':'good','drawSketch':False,'vectorLRef':Vector(-0.5,-0.5)}
#Lateral rebars (right side)
latRRbLy1={'id':'8','fi':16e-3,'s':0.15,'position':'good','maxLrebar':6.0}

# End data


lstRebarFam=list()
lstStirrupFam=list()

# beam
lstRebarFam1,lstStirrupFam1,newStartId=trcm.beam_reinf(
    width=width,
    height=height,
    length=length,
    anchPtTrnsSect=Vector(0,0),
    anchPtLnSect=Vector(5*width,0),
    reinfCfg=reinfCfg,
    angTrns=angTrns,
    angLn=angLn,
    lstBotRb=[],#[botRbLy1,botRbLy2,botRbLy3],
    lstTopRb=[],#[topRbLy1,topRbLy2],
    lstLeftLatlRb=[latLRbLy1],#,latLRbLy2],
    lstRightLatlRb=[latRRbLy1],
    lstStirrReinf=None,
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    anchPtPlan=Vector(-10,0),
    angPlan=0,
    drawPlan=True,
    startId=1,
    clearDistRbLayers=None,
    aggrSize=20e-3)

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam1+lstStirrupFam1,
               title=titSchedule,
               doc=doc
)
