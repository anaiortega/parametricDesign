# -*- coding: utf-8 -*-

import Part, FreeCAD, math
from parametric_design.freeCAD_civil import  draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from parametric_design.freeCAD_civil.structures import generic_typical_RC_members as trcm
from materials.ec2 import EC2_materials
from parametric_design.freeCAD_civil import draw_config as cfg

concr=EC2_materials.C30
steel=EC2_materials.S500C

estrName='boxCulvert'
titSchedule=estrName.upper()

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
boxL=25 #length of the box culvert
muret_hg=0.30
muret_th=0.30

scale=1/25
docName=estrName+'_armados'
FreeCAD.newDocument(docName)
# Data  reinforcements
cover=0.03
reinfConf=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2,factPosLabelSectReb=2/3)
# set the dimension style for this document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)


# chamfers' longitudinal rebar definition (diameter, spacement)
ch_rb={'fi':12e-3,'s':0.30}
# armadura longitudinal muretes (no se dibujan, sólo aparecen en despiece)
muret_ln={'fi':0.016,'id':'15','nmBars':2*3,'gap':0.15} # diameter, ID, number of rebars, extension of the rebar through the deck of the box

# Stirrup definition (see interpretartion of variables in handwritten notes)
# Cercos losa de cimentación (envolviendo a armadura transversal)
sRS=0.30
nRS=int(boxL/sRS)
dispRS=(boxL-nRS*sRS)/2
botSlab_stTr1={'id':'20','fi':8e-3,'sRealSh':sRS,'sPerp':0.15,'nStirrRealSh':nRS,'nStirrPerp':5,
               'widthStirr':0.2,'dispRealSh':dispRS,'dispPerp':LW_th,
               'vectorLRef':Vector(-0.3,-0.3),'rightSideLabelLn':True,
               'rightSideCover':False,
               }
botSlab_stTr2={'id':'21','fi':8e-3,'sRealSh':sRS,'sPerp':0.15,'nStirrRealSh':nRS,'nStirrPerp':5,
               'widthStirr':0.2,'dispRealSh':dispRS,'dispPerp':-LW_th,
               'vectorLRef':Vector(-0.3,-0.3),'rightSideLabelLn':False,
                'rightSideCover':True,
               }

# Cercos dintel



#Armadura principal marco 
BS_bot_ln={'fi':0.012,'s':0.30,'id':'1','distRFstart':0,'distRFend':0,'position':'good'} # bottom slab, bottom long. rebars
BS_bot_tr={'fi':0.016,'s':0.30,'id':'3','distRFstart':0,'distRFend':0,'position':'good'} # bottom slab, bottom transv. rebars
BS_top_ln={'fi':0.016,'s':0.30,'id':'2','distRFstart':LW_th,'distRFend':RW_th,'position':'poor'} # bottom slab, top long. rebars
BS_top_tr={'fi':0.016,'s':0.30,'id':'4','distRFstart':0,'distRFend':0,'position':'poor'} # bottom slab, top transv. rebars

TS_bot_ln={'fi':0.016,'s':0.30,'id':'11','distRFstart':LW_th,'distRFend':RW_th,'position':'good'} # top slab, bottom long. rebars
TS_bot_tr={'fi':0.016,'s':0.30,'id':'13','distRFstart':0,'distRFend':0,'position':'good'} # top slab, bottom transv. rebars
TS_top_ln={'fi':0.016,'s':0.30,'id':'12','distRFstart':0,'distRFend':0,'position':'poor'} # top slab, top long. rebars
TS_top_tr={'fi':0.016,'s':0.30,'id':'14','distRFstart':0,'distRFend':0,'position':'poor'} # top slab, top transv. rebars


# left wall, external horiz. rebars
LW_ext_hor={'fi':0.016,
            's':0.30,
            'id':'7L',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-cover,
            'gapEnd':-cover,
            'extrShapeStart':'fix270_len125',
            'extrShapeEnd':'fix270_len125',
            'vectorLRef':Vector(-0.3,0.5),
            'position': 'good',
            } 
# left wall, external vert. rebars
LW_ext_ver={'fi':0.016,
            's':0.30,
            'id':'10L',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-BS_th,
            'gapEnd':-cover,
            'extrShapeEnd': 'lap270_posPoor_tens_perc100',
            'position': 'poor',
            } 
# left wall, internal horiz. rebars
LW_int_hor={'fi':0.016,
            's':0.30,
            'id':'8L',
            'distRFstart':BS_th,
            'distRFend':TS_th,
            'gapStart':-cover,
            'gapEnd':-cover,
            'extrShapeStart':'fix90_len125',
            'extrShapeEnd':'fix90_len125',
            'vectorLRef':Vector(0.3,0.5),
            'position': 'good',
             } 
# left wall, internal vert. rebars
LW_int_ver={'fi':0.016,
            's':0.30,
            'id':'9L',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-BS_th,
            'gapEnd':-(cover+TS_top_tr['fi']+TS_top_ln['fi']),
            'extrShapeEnd':'fix90_len150',
            'vectorLRef':Vector(0.3,0.3),
            'position': 'poor',
            }
# Right wall. Main rebars
 # right wall, external horiz. rebars
RW_ext_hor={'fi':0.016,
            's':0.30,
            'id':'7R',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-cover,
            'gapEnd':-cover,
            'extrShapeStart':'fix90_len125',
            'extrShapeEnd':'fix90_len125',
            'vectorLRef':Vector(0.3,0.5),
            'position': 'good',
            }
# right wall, external vert. rebars
RW_ext_ver={'fi':0.016,
            's':0.30,
            'id':'10R',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-BS_th,
            'gapEnd':-cover,
            'extrShapeEnd':'lap90_posPoor_tens_perc100',
            'vectorLRef':Vector(0.3,0.3),
            'position': 'poor',
            } 
# right wall, internal horiz. rebars
RW_int_hor={'fi':0.016,
            's':0.30,
            'id':'8R',
            'distRFstart':BS_th,
            'distRFend':TS_th,
            'gapStart':-cover,
            'gapEnd':-cover,
            'extrShapeStart':'fix270_len125',
            'extrShapeEnd':'fix270_len125',
            'vectorLRef':Vector(-0.3,0.5),
            'position': 'good',
            }
 # right wall, internal vert. rebars
RW_int_ver={'fi':0.016,
            's':0.30,
            'id':'9R',
            'distRFstart':0,
            'distRFend':0,
            'gapStart':-BS_th,
            'gapEnd':-(cover+TS_top_tr['fi']+TS_top_ln['fi']),
            'extrShapeEnd':'fix270_len150',
            'position': 'poor',
            }

# Bottom dowels
## left wall
diam=LW_ext_ver['fi']
recStart=cover+BS_bot_tr['fi']+BS_bot_ln['fi']
#bottom dowel, external, left wall
LD_ext={'id':'6L',
        'fi':diam,
        's':LW_ext_ver['s'],
        'distRFstart':0,
        'distRFend':0,
        'gapStart':-recStart,
        'extrShapeStart':
        'fix270_len200',
        'extrShapeEnd':'lap0_posGood_tens',
        'vectorLRef':Vector(-0.2,0.2),
        'position':'good',
        }

#bottom dowel, internal, left wall
diam=LW_int_ver['fi']
LD_int={'id':'5L',
        'fi':diam,
        's':LW_int_ver['s'],
        'distRFstart':0,
        'distRFend':0,
        'gapStart':-recStart,
        'extrShapeStart':
        'fix270_len200',
        'extrShapeEnd':'lap0_posGood_tens',
        'vectorLRef':Vector(0.2,0.2),
        'position':'good',
       }

## right wall
diam=RW_ext_ver['fi']
recStart=cover+BS_bot_tr['fi']+BS_bot_ln['fi']
#bottom dowel, external, right wall
RD_ext={'id':'6R',
        'fi':diam,
        's':RW_ext_ver['s'],
        'distRFstart':0,
        'distRFend':0,
        'gapStart':-recStart,
        'extrShapeStart':'fix90_len200',
        'extrShapeEnd':'lap0_posGood_tens',
        'vectorLRef':Vector(0.2,0.2),
        'position':'good',
        }
#bottom dowel, internal, right wall
diam=RW_int_ver['fi']
RD_int={'id':'5R',
        'fi':diam,
        's':RW_int_ver['s'],
        'distRFstart':0,
        'distRFend':0,
        'gapStart':-recStart,
        'extrShapeStart':
        'fix90_len200','extrShapeEnd':
        'lap0_posGood_tens',
        'vectorLRef':Vector(-0.2,0.2),
        'position':'good',
        }#,'fixLengthEnd':5}   

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

extensionLpts=[Vector(0,0),Vector(0,boxL)]
lstPtsConcrSect=[[ext_p1,ext_p2,ext_p3,ext_p4,ext_p1],[int_p1a,int_p1b,int_p2b,int_p2a,int_p3a,int_p3b,int_p4b,int_p4a,int_p1a]]
for lsc in lstPtsConcrSect:
    s=Part.makePolygon(lsc)
    p=Part.show(s)
    FreeCADGui.ActiveDocument.getObject(p.Name).LineColor=cfg.colorConcrete

# Reinforcement
lstRebarFam=list()
## bottom slab
#lstRebarFam+=trcm.closed_slab(width=ext_wd,length=boxL,thickness=BS_th,botTrnsRb=BS_bot_tr,topTrnsRb=BS_top_tr,botLnRb=BS_bot_ln,topLnRb=BS_top_ln,anchPtTrnsSect=ext_p1,anchPtLnSect=ext_p1+Vector(ext_wd+1,0),reinfCfg=reinfConf,drawConcrTrSect=False,drawConcrLnSect=True,factGap=2)

mainLst,stirrLst=trcm.constant_thickness_brick_reinf(width=ext_wd,
                                          length=boxL,
                                          thickness=BS_th,
                                          anchPtTrnsSect=ext_p1,
                                          anchPtLnSect=ext_p1+Vector(ext_wd+1,0),
                                          reinfCfg=reinfConf,
                                          angTrns=0,
                                          angLn=0,
                                          botTrnsRb=BS_bot_tr,
                                          topTrnsRb=BS_top_tr,
                                          botLnRb=BS_bot_ln,
                                          topLnRb=BS_top_ln,
                                          lstStirrHoldTrReinf=[botSlab_stTr1,botSlab_stTr2],
                                          drawConcrTrSect=False,
                                          drawConcrLnSect=True,
                                          )  
lstRebarFam+=mainLst+stirrLst

## top slab
lstRebarFam+=trcm.closed_slab(width=ext_wd,length=boxL,thickness=TS_th,botTrnsRb=TS_bot_tr,topTrnsRb=TS_top_tr,botLnRb=TS_bot_ln,topLnRb=TS_top_ln,anchPtTrnsSect=ext_p1+Vector(0,ext_hg-TS_th),anchPtLnSect=ext_p1+Vector(ext_wd+1,ext_hg-TS_th),reinfCfg=reinfConf,drawConcrTrSect=False,drawConcrLnSect=True,factGap=2)          

## left wall
mainLst,stirrLst=trcm.constant_thickness_brick_reinf(width=ext_hg,
                                      length=boxL,
                                      thickness=LW_th,
                                      anchPtTrnsSect=ext_p1+Vector(LW_th,0),
                                      anchPtLnSect=ext_p1+Vector(0,2*ext_hg),
                                      reinfCfg=reinfConf,
                                      angTrns=90,
                                      angLn=90,
                                      botTrnsRb=LW_int_ver,
                                      topTrnsRb=LW_ext_ver,
                                      botLnRb=LW_int_hor,
                                      topLnRb=LW_ext_hor,
                                      drawConcrTrSect=False,
                                      drawConcrLnSect=True)

lstRebarFam+=mainLst+stirrLst
## right wall
lmainLst,stirrLst=trcm.constant_thickness_brick_reinf(width=ext_hg,
                                      length=boxL,
                                      thickness=RW_th,
                                      anchPtTrnsSect=ext_p4,
                                      anchPtLnSect=ext_p4+Vector(0,2*ext_hg),
                                      reinfCfg=reinfConf,
                                      angTrns=90,
                                      angLn=90,
                                      botTrnsRb=RW_ext_ver,
                                      topTrnsRb=RW_int_ver,
                                      botLnRb=RW_ext_hor,
                                      topLnRb=RW_int_hor,
                                      drawConcrTrSect=False,
                                      drawConcrLnSect=True)

lstRebarFam+=mainLst+stirrLst

## Dowels left wall
mainLst,stirrLst=trcm.constant_thickness_brick_reinf(width=BS_th,
                                      length=boxL,
                                      thickness=LW_th,
                                      anchPtTrnsSect=ext_p1+Vector(LW_th,0),
                                      anchPtLnSect=ext_p1+Vector(0,20),
                                      reinfCfg=reinfConf,
                                      angTrns=90,
                                      angLn=90,
                                      botTrnsRb=LD_int,
                                      topTrnsRb=LD_ext,
                                      botLnRb=None,
                                      topLnRb=None,
                                      drawConcrTrSect=False,
                                      drawConcrLnSect=False,
                                      ) 
lstRebarFam+=mainLst+stirrLst

## Dowels right wall
mainLst,stirrLst=trcm.constant_thickness_brick_reinf(width=BS_th,
                                      length=boxL,
                                      thickness=RW_th,
                                      anchPtTrnsSect=ext_p4,
                                      anchPtLnSect=ext_p4+Vector(0,20),
                                      reinfCfg=reinfConf,
                                      angTrns=90,
                                      angLn=90,
                                      botTrnsRb=RD_ext,
                                      topTrnsRb=RD_int,
                                      botLnRb=None,
                                      topLnRb=None,
                                      drawConcrTrSect=False,
                                      drawConcrLnSect=False,
                                      )
lstRebarFam+=mainLst+stirrLst

muret_rf=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier=muret_ln['id'],
    diameter=muret_ln['fi'],
    lstPtsConcrSect=[Vector(0,0),Vector(0,muret_hg),Vector(boxL,muret_hg),Vector(boxL,0)],
    rightSideCover=False,
    nmbBars=muret_ln['nmBars'],
    gapStart=muret_ln['gap'],
    gapEnd=muret_ln['gap'],
    )
#lstRebarFam+=[muret_rf]

lastId=15
chamfer1_rf=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier=str(lastId+1),
    diameter=ch_rb['fi'],
    spacing=ch_rb['s'],
    lstPtsConcrSect=[int_p1a,int_p1b],
    rightSideCover=False,
    vectorLRef=Vector(0.15,0.15),
    extensionLength=boxL,
    gapStart=math.sqrt(2)*(BS_th-3*cover),
    gapEnd=math.sqrt(2)*(BS_th-3*cover),
    extrShapeStart='fix225_len150',
    extrShapeEnd='fix315_len150',
    )
chamfer1_rf.drawLstRebar()
lastId+=1
chamfer2_rf=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier=str(lastId+1),
    diameter=ch_rb['fi'],
    spacing=ch_rb['s'],
    lstPtsConcrSect=[int_p2b,int_p2a],
    rightSideCover=False,
    vectorLRef=Vector(0.15,-0.15),
    extensionLength=boxL,
    gapStart=math.sqrt(2)*(BS_th-3*cover),
    gapEnd=math.sqrt(2)*(BS_th-3*cover),
    extrShapeStart='fix225_len150',
    extrShapeEnd='fix315_len150',
    )
chamfer2_rf.drawLstRebar()
lastId+=1
chamfer3_rf=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier=str(lastId+1),
    diameter=ch_rb['fi'],
    spacing=ch_rb['s'],
    lstPtsConcrSect=[int_p3a,int_p3b],
    rightSideCover=False,
    vectorLRef=Vector(-0.15,-0.15),
    extensionLength=boxL,
    gapStart=math.sqrt(2)*(BS_th-3*cover),
    gapEnd=math.sqrt(2)*(BS_th-3*cover),
    extrShapeStart='fix225_len150',
    extrShapeEnd='fix315_len150',
    )
chamfer3_rf.drawLstRebar()
lastId+=1
chamfer4_rf=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier=str(lastId+1),
    diameter=ch_rb['fi'],
    spacing=ch_rb['s'],
    lstPtsConcrSect=[int_p4b,int_p4a],
    rightSideCover=False,
    vectorLRef=Vector(-0.15,0.15),
    extensionLength=boxL,
    gapStart=math.sqrt(2)*(BS_th-3*cover),
    gapEnd=math.sqrt(2)*(BS_th-3*cover),
    extrShapeStart='fix225_len150',
    extrShapeEnd='fix315_len150',
    )
chamfer4_rf.drawLstRebar()
lastId+=1

#geometry
rb.drawRCSection(
    lstOfLstPtsConcrSect=lstPtsConcrSect,
    vTranslation=Vector(-2*boxC_int_wd,0,0),
    dimConcrSect=True,
    spacDimLine=2*reinfConf.texSize,
    )
        
    
lstRebarFam+=[chamfer1_rf,chamfer2_rf,chamfer3_rf,chamfer4_rf]
    
doc=FreeCAD.newDocument(estrName+"_despiece",estrName+"_despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
               title=titSchedule,
               doc=doc
               )







