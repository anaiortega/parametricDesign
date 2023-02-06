# -*- coding: iso-8859-1 -*-
from __future__ import division

from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Generic brick'
titSchedule=estrName.upper()

genConf=rb.genericConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=0.125,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'genericBrick')

width=4 #dimension of the slab in the direction of the transversal rebars
length=5 #dimension of the slab in the direction of the longitudinal rebars
thickness=0.4  #thickness of the slab
# bottom transverse rebars data
botTrnsRb={'id':'1','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0,'gapStart':-2,'extrShapeStart':'anc0_posPoor_compr','position':'good','vectorLRef':Vector(0.3,-0.2)}#,'fixLengthEnd':5} 
# top transverse rebars data
botLnRb={'id':'2','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.5,'extrShapeStart':'anc0_posPoor_compr','position':'good','vectorLref':Vector(0.1,-0.3)}
# bottom longitudinal rebars data
topTrnsRb={'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1,'extrShapeEnd':'anc90_posPoor_compr','position':'poor','vectorLRef':Vector(-0.3,0.15)}
# top longitudinal rebars data
topLnRb={'id':'4','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.3,'extrShapeEnd':'anc270_posGood_tens','position':'poor','vectorLref':Vector(-0.2,0.3)}
# stirrups holding transverse rebars
stirrHoldTr={'id':'5' ,'fi':8e-3 ,'sRealSh':0.30 ,'sPerp':0.15 ,'nStirrRealSh': 3 , 'nStirrPerp':4 ,'widthStirr': 0.25, 'dispRealSh': 0.4, 'dispPerp':0.1,'vectorLref':Vector(0.3,-0.5),'sideLabelLn':'l'}

# stirrups holding longitudinal rebars
stirrHoldLn={'id':'6' ,'fi':10e-3 ,'sRealSh':0.20 ,'sPerp':0.30 ,'nStirrRealSh': 5 , 'nStirrPerp':2 ,'widthStirr': 0.40, 'dispRealSh': 1.5, 'dispPerp':1.3,'vectorLref':Vector(0.2,-0.5),'sideLabelLn':'l'}

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section


lstRebarFam,lstStirrupFam=trcm.generic_brick_reinf(
    width=width,
    length=length,
    thickness=thickness,
    anchPtTrnsSect=anchPtTrnsSect,
    anchPtLnSect=anchPtLnSect,
    genConf=genConf,
    angTrns=20,
    angLn=40,
    botTrnsRb=botTrnsRb,
    topTrnsRb=topTrnsRb,
    botLnRb=botLnRb,
    topLnRb=topLnRb,
    stirrHoldTrReinf=stirrHoldTr,
    stirrHoldLnReinf=stirrHoldLn,
    drawConcrTrSect=True,
    drawConcrLnSect=True) 

doc=App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               title=titSchedule,
               doc=doc
)
