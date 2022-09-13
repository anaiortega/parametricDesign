# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C


# Reinforcement of a box culvert with chamfers in all its
# internal corners

# Nomenclature:
# _th: thickness
# _wd: width
# _ln: length
# _hg: height
# W: wall
# LW: left wall
# RW: right wall
# TS: top slab
# BS: bottom slab
# int: internal
# bot: bottom
# top: top
# ver: vertical
# hor: horizontal

#
#DATA
# Data RC box culvert
boxC_int_wd=3.50 # internal width of the box
boxC_int_hg=2 # internal height of the box
chamfer_wd=0.1 # width of the chamfer
chamfer_hg=0.1 # height of the chamfer
LW_th=0.30 # thickness of the left wall
RW_th=0.30 # thickness of the right wall
TS_th=0.30 # thickness of the top slab
BS_th=0.30 # thickness of the bottom slab
boxL=5 #length of the box culvert

# Data  reinforcements
cover=0.03
reinfConf=reinf_bars.genericConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=0.125,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,docName='boxCulvert')

BS_bot_ln={'fi':0.012,'s':0.30,'id':'1','distRFstart':0,'distRFend':0} # bottom slab, bottom long. rebars
BS_bot_tr={'fi':0.016,'s':0.30,'id':'3','distRFstart':0,'distRFend':0} # bottom slab, bottom transv. rebars
BS_top_ln={'fi':0.016,'s':0.30,'id':'2','distRFstart':LW_th,'distRFend':RW_th} # bottom slab, top long. rebars
BS_top_tr={'fi':0.016,'s':0.30,'id':'4','distRFstart':0,'distRFend':0} # bottom slab, top transv. rebars

LW_ext_hor={'fi':0.016,'s':0.30,'id':'7l','distRFstart':0,'distRFend':0} # left wall, external horiz. rebars
LW_ext_ver={'fi':0.016,'s':0.30,'id':'10l','distRFstart':0,'distRFend':0} # left wall, external vert. rebars
LW_int_hor={'fi':0.016,'s':0.30,'id':'8l','distRFstart':BS_th,'distRFend':TS_th} # left wall, internal horiz. rebars
LW_int_ver={'fi':0.016,'s':0.30,'id':'9l','distRFstart':0,'distRFend':0} # left wall, internal vert. rebars

RW_ext_hor={'fi':0.016,'s':0.30,'id':'7r','distRFstart':0,'distRFend':0} # right wall, external horiz. rebars
RW_ext_ver={'fi':0.016,'s':0.30,'id':'10r','distRFstart':0,'distRFend':0} # right wall, external vert. rebars
RW_int_hor={'fi':0.016,'s':0.30,'id':'8r','distRFstart':BS_th,'distRFend':TS_th} # right wall, internal horiz. rebars
RW_int_ver={'fi':0.016,'s':0.30,'id':'9r','distRFstart':0,'distRFend':0} # right wall, internal vert. rebars

TS_bot_ln={'fi':0.016,'s':0.30,'id':'11','distRFstart':LW_th,'distRFend':RW_th} # top slab, bottom long. rebars
TS_bot_tr={'fi':0.016,'s':0.30,'id':'13','distRFstart':0,'distRFend':0} # top slab, bottom transv. rebars
TS_top_ln={'fi':0.016,'s':0.30,'id':'12','distRFstart':0,'distRFend':0} # top slab, top long. rebars
TS_top_tr={'fi':0.016,'s':0.30,'id':'14','distRFstart':0,'distRFend':0} # top slab, top transv. rebars

# Bottom dowels
diam=LW_ext_ver['fi']
recStart=cover+BS_bot_tr['fi']+BS_bot_ln['fi']+diam/2
LD_ext={'id':'6','fi':diam,'s':LW_ext_ver['s'],'distRFstart':0,'distRFend':0,'gapStart':-recStart,'extrShapeStart':'anc270_posGood_tens','extrShapeEnd':'lap_posGood_tens'}#,'fixLengthEnd':5}   #bottom dowel, external, left wall

diam=LW_int_ver['fi']
LD_int={'id':'5','fi':diam,'s':LW_int_ver['s'],'distRFstart':0,'distRFend':0,'gapStart':-recStart,'extrShapeStart':'anc270_posGood_tens','extrShapeEnd':'lap_posGood_tens'}#,'fixLengthEnd':5}   #bottom dowel, internal, left wall

# END DATA


# Concrete transversal section
# external dimensions
ext_hg=BS_th+boxC_int_hg+TS_th
ext_wd=LW_th+boxC_int_wd+RW_th
#Points transversal section
ext_p1=Vector(0,0)
ext_p2=ext_p1.add(Vector(0,ext_hg))
ext_p3=ext_p2.add(Vector(ext_wd,0))
ext_p4=ext_p1.add(Vector(ext_wd,0))

int_p1a=ext_p1.add(Vector(LW_th+chamfer_wd,BS_th))
int_p1b=int_p1a.add(Vector(-chamfer_wd,chamfer_hg))

int_p2a=ext_p2.add(Vector(LW_th+chamfer_wd,-TS_th))
int_p2b=int_p2a.add(Vector(-chamfer_wd,-chamfer_hg))

int_p3a=ext_p3.add(Vector(-RW_th-chamfer_wd,-TS_th))
int_p3b=int_p3a.add(Vector(chamfer_wd,-chamfer_hg))

int_p4a=ext_p4.add(Vector(-RW_th-chamfer_wd,TS_th))
int_p4b=int_p4a.add(Vector(chamfer_wd,chamfer_hg))

lstPtsConcrSect=[[ext_p1,ext_p2,ext_p3,ext_p4,ext_p1],[int_p1a,int_p1b,int_p2b,int_p2a,int_p3a,int_p3b,int_p4b,int_p4a,int_p1a]]
for lsc in lstPtsConcrSect:
    s=Part.makePolygon(lsc)
    Part.show(s)

# Reinforcement
lstRebarFam=list()
## bottom slab
lstRebarFam+=trcm.closed_slab(width=ext_wd,length=boxL,thickness=BS_th,botTrnsRb=BS_bot_tr,topTrnsRb=BS_top_tr,botLnRb=BS_bot_ln,topLnRb=BS_top_ln,anchPtTrnsSect=ext_p1,anchPtLnSect=ext_p1+Vector(ext_wd+1,0),genConf=reinfConf,drawConrTrSect='N',drawConrLnSect='Y')          

## top slab
lstRebarFam+=trcm.closed_slab(width=ext_wd,length=boxL,thickness=TS_th,botTrnsRb=TS_bot_tr,topTrnsRb=TS_top_tr,botLnRb=TS_bot_ln,topLnRb=TS_top_ln,anchPtTrnsSect=ext_p1+Vector(0,ext_hg-TS_th),anchPtLnSect=ext_p1+Vector(ext_wd+1,ext_hg-TS_th),genConf=reinfConf,drawConrTrSect='N',drawConrLnSect='Y')          

## left wall
lstRebarFam+=trcm.wall(height=ext_hg-BS_th,length=boxL,thickness=LW_th,leftVertRb=LW_ext_ver,rightVertRb=LW_int_ver,leftHorRb=LW_ext_hor,rightHorRb=LW_int_hor,anchPtVertSect=ext_p1+Vector(0,BS_th),anchPtHorSect=ext_p1+Vector(0,ext_hg+2),genConf=reinfConf,drawConrVertSect='N',drawConrHorSect='Y')

## right wall
lstRebarFam+=trcm.wall(height=ext_hg-BS_th,length=boxL,thickness=RW_th,leftVertRb=RW_int_ver,rightVertRb=RW_ext_ver,leftHorRb=RW_int_hor,rightHorRb=RW_ext_hor,anchPtVertSect=ext_p1+Vector(LW_th+boxC_int_wd,BS_th),anchPtHorSect=ext_p1+Vector(LW_th+boxC_int_wd,ext_hg+2),genConf=reinfConf,drawConrVertSect='N',drawConrHorSect='Y')

## Dowels left wall
lstRebarFam+=trcm.generic_brick_reinf(width=BS_th,length=boxL,thickness=LW_th,
           anchPtTrnsSect=ext_p1+Vector(LW_th,0),anchPtLnSect=ext_p1+Vector(0,20),genConf=reinfConf,
           angTrns=90,angLn=90,
           botTrnsRb=LD_int,topTrnsRb=LD_ext,botLnRb=None,topLnRb=None,
           drawConrTrSect='N',drawConrLnSect='N') 

FreeCADnewDocument("despiece")
reinf_bars.barSchedule(lstBarFamilies=lstRebarFam,
               wColumns=[14,30,25,10,15,15],
               hRows=10,
               hText=2.5,
               hTextSketch=2.5)






