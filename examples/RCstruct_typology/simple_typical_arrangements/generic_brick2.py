# -*- coding: iso-8859-1 -*-
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
botTrnsRb={'id':'1','fi':20e-3,'s':0.15,'distRFstart':0,'distRFend':0,'gapStart':0.5,'extrShapeStart':'anc90_posGood_tens','extrShapeEnd':'anc90_posGood_tens','position':'good','vectorLRef':Vector(-0.3,-0.35)} 
# top transverse rebars data
topTrnsRb={'id':'3','fi':16e-3,'s':0.15,'distRFstart':0,'distRFend':0,'extrShapeStart':'lap270_posPoor_tens','extrShapeEnd':'lap0_posPoor_tens_perc100','position':'poor'}#,'fixLengthEnd':2} 
# bottom longitudinal rebars data
botLnRb={'id':'2','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.5,'fixLengthStart':5,'gapEnd':2,'extrShapeEnd':'lap45_posGood_compr','position':'good','vectorLRef':Vector(0.4,-0.20)}
# top longitudinal rebars data
topLnRb={'id':'4','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.3,'extrShapeStart':'fix40_len1200','extrShapeEnd':'lap180_posPoor_tens_perc50','position':'poor'}

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section

docName='genericBrick'
FreeCAD.newDocument(docName)
scale=1/50
reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)


lstRebarFam,lstStirrupFam=trcm.generic_brick_reinf(width=width,length=length,thickness=thickness,
           anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect,reinfCfg=reinfCfg,
           angTrns=5,angLn=10,
           botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,
           drawConcrTrSect=True,drawConcrLnSect=True) 

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
               title=titSchedule,
               doc=doc
)
