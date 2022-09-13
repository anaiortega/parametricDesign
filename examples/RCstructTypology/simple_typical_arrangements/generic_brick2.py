# -*- coding: iso-8859-1 -*-
from __future__ import division
from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

width=4 #dimension of the slab in the direction of the transversal rebars
length=5 #dimension of the slab in the direction of the longitudinal rebars
thickness=0.4  #thickness of the slab
# bottom transverse rebars data
topTrnsRb={'id':'3','fi':16e-3,'s':0.15,'distRFstart':0,'distRFend':0,'extrShapeStart':'anc90_posGood_tens','extrShapeEnd':'anc270_posPoor_tens'}#,'fixLengthEnd':2} 
botTrnsRb={'id':'1','fi':20e-3,'s':0.15,'distRFstart':0,'distRFend':0,'extrShapeStart':'anc90_posGood_tens','fixLengthEnd':5} 
# top transverse rebars data
botLnRb={'id':'2','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.5,'gapStart':1,'gapEnd':2,'extrShapeEnd':'anc45_posGood_compr'}
# bottom longitudinal rebars data
# top longitudinal rebars data
topLnRb={'id':'4','fi':16e-3,'s':0.20,'distRFstart':0.1,'distRFend':0.3,}

anchPtTrnsSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete transversal cross-section
anchPtLnSect=Vector(width+1,0) #anchor point to place the bottom left corner of the concrete longitudinal cross-section

genConf=rb.genericConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=0.125,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,docName='genericBrick')

lstRebarFam=trcm.generic_brick_reinf(width=width,length=length,thickness=thickness,
           anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect,genConf=genConf,
           angTrns=30,angLn=40,
           botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,
           drawConrTrSect='Y',drawConrLnSect='Y') 

App.newDocument("despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
               wColumns=[14,30,25,10,15,15],
               hRows=10,
               hText=2.5,
               hTextSketch=2.5)
