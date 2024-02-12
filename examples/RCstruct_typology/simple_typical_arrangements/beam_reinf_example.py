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

width=0.7
height=1.5
length=10

# Bottom rebars
botRbLy1={'id':None,'fi':32e-3,'nmbBars':4,'position':'good'}
botRbLy2={'id':None,'fi':25e-3,'nmbBars':5,'position':'good'}
botRbLy3={'id':None,'fi':16e-3,'nmbBars':4,'position':'good'}

# Top rebars
topRbLy1={'id':None,'fi':25e-3,'nmbBars':5,'position':'poor'}
topRbLy2={'id':None,'fi':20e-3,'nmbBars':4,'position':'poor'}

#Lateral rebars (left side)
latLRbLy1={'id':None,'fi':12e-3,'s':0.20,'position':'good'}
latLRbLy2={'id':None,'fi':10e-3,'s':0.10,'position':'good'}

#Lateral rebars (right side)
latRRbLy1={'id':None,'fi':16e-3,'s':0.15,'position':'good'}

# End data
lstRebarFam=list()
lstStirrupFam=list()

# beam
lstRebarFam1,lstStirrupFam1,newStartId=trcm.beam_reinf(
    width=width,
    height=height,
    length=length,
    anchPtTrnsSect=Vector(0,0),
    anchPtLnSect=Vector(2*width,0),
    reinfCfg=reinfCfg,
    angTrns=0,
    angLn=0,
    lstBotRb=[botRbLy1,botRbLy2,botRbLy3],
    lstTopRb=[topRbLy1,topRbLy2],
    lstLeftLatlRb=[latLRbLy1,latLRbLy2],
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
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               title=titSchedule,
               doc=doc
)
