# -*- coding: utf-8 -*-
from __future__ import division

import math
from FreeCAD import Vector
from parametric_design.freeCAD_civil import  draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

concr=EC2_materials.C25
steel=EC2_materials.S500C

estrName='Cylindrical column'
titSchedule=estrName.upper()
docArm=FreeCAD.newDocument(estrName+'_arm')
scale=1/50

reinfCfg=cfg.reinfConf(cover=35e-3,xcConcr=concr,xcSteel=steel,texSize=2.5*1e-3/scale,Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

Hcol= 3 # height of the column
Rad=0.5 # radius of the cylinder

# Section in height
pl1=Vector(-Rad,0)
pl2=Vector(-Rad,Hcol)
pl3=Vector(Rad,Hcol)
pl4=Vector(Rad,0)

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
    lstCover=[Rad],
    rightSideCover=True,
    vectorLRef=Vector(0.70,-0.15),
    fromToExtPts=None,
    sectBarsConcrRadius=0.5,
    lateralCover=0,
    rightSideSectBars=True,
    coverSectBars=reinfCfg.cover+fi_stirr,
    gapStart=0.5,
    extrShapeStart='anc90_posGood_compr',
    )

stirr1=rb.stirrupFamily(
    reinfCfg=reinfCfg,
    identifier='2',
    diameter=fi_stirr,
    lstPtsConcrSect=None,
    concrSectRadius=Rad,
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
    vectorLRef=Vector(0.5,-0.5),
    rightSideLabelLn=False)

# Cross section
rb.drawRCSection(
    radiusConcrSect=Rad,
    lstShapeRebarFam=None,
    lstSectRebarFam=[vert_rf1],
    lstShapeStirrupFam=[stirr1],
    lstEdgeStirrupFam=None,
    vTranslation=Vector(0,0,0),
    )

# Section in height
rb.drawRCSection(
    lstOfLstPtsConcrSect=[[pl1,pl2,pl3,pl4,pl1]],
    lstShapeRebarFam=[vert_rf1],
    lstSectRebarFam=None,
    lstShapeStirrupFam=None,
    lstEdgeStirrupFam=[stirr1],
    vTranslation=Vector(0,2*Rad+0.7),
    )
docArm.recompute()
'''
docSch=FreeCAD.newDocument(estrName+"_schedule",estrName+"_schedule")
rb.barSchedule(lstBarFamilies=[vert_rf1,stirr1],
               title='cylindrical column',
               doc=docSch
)
'''
