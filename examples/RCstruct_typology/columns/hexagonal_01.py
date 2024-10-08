# -*- coding: utf-8 -*-
from __future__ import division

import math
from FreeCAD import Vector
from parametric_design.freeCAD_civil import  draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Hexagonal column'
titSchedule=estrName.upper()

docArm=FreeCAD.newDocument(estrName+'_arm')
scale=1/50
reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

Hcol= 3.1 # height of the column
# Hexagon dimensions (column cross-section)
Shex=0.5 # side of the hexagon
Hhex=2*Shex*math.cos(math.radians(30)) # height of the hexagon
Whex=Shex+2*Shex*math.sin(math.radians(30)) # width of the hexagon

# Cross-section concrete points
pt1=Vector(-Shex/2,Hhex/2)
pt2=Vector(Shex/2,Hhex/2)
pt3=Vector(Whex/2,0)
pt4=Vector(Shex/2,-Hhex/2)
pt5=Vector(-Shex/2,-Hhex/2)
pt6=Vector(-Whex/2,0)
# Section in height
pl1=Vector(-Whex/2,0)
pl2=Vector(-Whex/2,Hcol)
pl3=Vector(Whex/2,Hcol)
pl4=Vector(Whex/2,0)

fi_stirr=10e-3
fi_vert_rb=16e-3
# Rebar families
# vertical rebars
vert_rf1=rb.rebarFamily(
    reinfCfg=reinfCfg,
    identifier='1',
    diameter=fi_vert_rb,
    spacing=0.1,
    lstPtsConcrSect=[pl1,pl2],
    lstCover=[Whex/2],
    rightSideCover=True,
    vectorLRef=Vector(0.70,-0.15),
    fromToExtPts=[pt1,pt2,pt3],
    lateralCover=0,
    rightSideSectBars=True,
    coverSectBars=reinfCfg.cover+fi_stirr,
    gapStart=0.5,
    extrShapeStart='anc90_posGood_compr',
    )
    
vert_rf2=rb.rebarFamily(
    reinfCfg=reinfCfg,
    identifier='2',
    diameter=fi_vert_rb,
    spacing=0.15,
    lstPtsConcrSect=[pl1,pl2],
    lstCover=[Whex/4],
    rightSideCover=True,
    vectorLRef=Vector(-0.50,-0.15),
    fromToExtPts=[pt1,pt6,pt5,pt4,pt3],
    lateralCover=0.1,
    rightSideSectBars=False,
    coverSectBars=reinfCfg.cover+fi_stirr,
    gapStart=0.5,
    extrShapeStart='anc90_posGood_compr',
    )

stirr1=rb.stirrupFamily(
    reinfCfg=reinfCfg,
    identifier='3',
    diameter=fi_stirr,
    lstPtsConcrSect=[pt1,pt2,pt3,pt4,pt5,pt6,pt1],
    lstPtsConcrLong=[pl1,pl4],
    spacStrpTransv=None,
    spacStrpLong=0.15,
    vDirLong=Vector(0,1),
    nmbStrpTransv=1,
    nmbStrpLong=int(Hcol/.15),
    lstCover=None,
    rightSideCover=True,
    dispStrpTransv=None,
    dispStrpLong=0.1,
    vectorLRef=Vector(0.5,0.4),
    rightSideLabelLn=False)

stirr2=rb.stirrupFamily(
    reinfCfg=reinfCfg,
    identifier='4',
    diameter=fi_stirr,
    lstPtsConcrSect=[pt1,pt5],
    lstPtsConcrLong=[pl4,pl1],
    spacStrpTransv=0.20,
    spacStrpLong=0.15,
    vDirTrans=Vector(1,0),
    vDirLong=Vector(0,1),
    nmbStrpTransv=2,
    nmbStrpLong=int(Hcol/.15),
    lstCover=None,
    rightSideCover=True,
    dispStrpTransv=0.10,
    dispStrpLong=0.15,
    vectorLRef=Vector(-0.5,0.5),
    rightSideLabelLn=True,
    closed=False,
    fixAnchorStart='fix45_len60',
    fixAnchorEnd='fix135_len60',
)

# RF cross section 
rb.drawRCSection(
    lstOfLstPtsConcrSect=[[pt1,pt2,pt3,pt4,pt5,pt6,pt1]],
    lstShapeRebarFam=None,
    lstSectRebarFam=[vert_rf1,vert_rf2],
    lstShapeStirrupFam=[stirr1,stirr2],
    lstEdgeStirrupFam=None,
    vTranslation=Vector(0,0,0),
    )

# RF section in height
rb.drawRCSection(
    lstOfLstPtsConcrSect=[[pl1,pl2,pl3,pl4,pl1]],
    lstShapeRebarFam=[vert_rf1,vert_rf2],
    lstSectRebarFam=None,
    lstShapeStirrupFam=None,
    lstEdgeStirrupFam=[stirr1,stirr2],
    vTranslation=Vector(0,Hhex+0.7),
    dimConcrSect=False,
    
    )
# Geom cross section
rb.drawConcreteSection(
    lstPtsConcrSect=[pt1,pt2,pt3,pt4,pt5,pt6,pt1],
    vTranslation=Vector(-10*Shex,0,0),
    dimConcrSect=True,
    spacDimLine=2*reinfCfg.texSize
    )

# Geom section in height
rb.drawRCSection(
    lstOfLstPtsConcrSect=[[pl1,pl2,pl3,pl4,pl1]],
    vTranslation=Vector(-10*Shex,Hhex+0.7),
    dimConcrSect=False,
    )

docArm.recompute()

docSch=FreeCAD.newDocument(estrName+"_schedule",estrName+"_schedule")
rb.barSchedule(lstBarFamilies=[vert_rf1,vert_rf2,stirr1,stirr2],
               title='hexagonal column',
               doc=docSch
)
