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
botTrnsRb={'id':'1','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0,'gapStart':-2,'extrShapeStart':'anc0_posPoor_compr','position':'good','vectorLRef':Vector(0.3,-0.2)}#,'fixLengthEnd':5} 
# top transverse rebars data
botLnRb={'id':'2','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.5,'extrShapeStart':'anc0_posPoor_compr','position':'good','vectorLRef':Vector(0.1,-0.3)}
# bottom longitudinal rebars data
topTrnsRb={'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1,'extrShapeEnd':'anc90_posPoor_compr','position':'poor','vectorLRef':Vector(-0.3,0.15)}
# top longitudinal rebars data
topLnRb={'id':'4','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.3,'extrShapeEnd':'anc270_posGood_tens','position':'poor','vectorLRef':Vector(-0.2,0.3)}

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section


lstRebarFam,lstStirrupFam=trcm.sloped_faces_brick_reinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect,reinfCfg=reinfCfg,angTrns=-90,angLn=0,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,trSlopeBottFace=-0.2/1,trSlopeTopFace=0.15,drawConcrTrSect=True,drawConcrLnSect=True)

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
               title=titSchedule,
               doc=doc
)
