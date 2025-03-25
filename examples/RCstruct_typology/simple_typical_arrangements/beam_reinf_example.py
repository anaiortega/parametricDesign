# -*- coding: utf-8 -*-
from __future__ import division

from FreeCAD import Vector
from parametric_design.freeCAD_civil.structures import generic_typical_RC_members as trcm
from parametric_design.freeCAD_civil import  draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from materials.ec2 import EC2_materials

#          *** DATA ***
## Materials
concr=EC2_materials.C25
steel=EC2_materials.S500C
cover=0.035

## Document and style
estrName='Generic beam'
titSchedule=estrName.upper()
FreeCAD.newDocument(estrName+'genericBeam')
## Config parameters (cfg.reinfConf) and default values:
# cover,                    xcConcr,                   xcSteel,
# texSize=0.125,            Code='EC2',                dynamEff=False,
# decLengths=2,             decSpacing=2,              sketchScale=5,
# factPosLabelSectReb=2/3,  factDispReflinSectReb=1.0, roundAncLap=None
scale=1/25
reinfCfg=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=2.5/(scale*1e3),Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
# set XC dimension style in current document
cfg.set_dim_style(scale=scale,dimStyProp=cfg.XCdimProp)

## Geometry
width=0.7 # beam cross-section width
height=1.5 # beam cross-section height
length=33 # beam length
angTrns=0 # angle (degrees) between the horizontal and the cross-section width dimension
angLn=90

## Rebar families definition. Parameters and default values:
# fi,     s=None,       Id=None,                    nmbBars=None,
# distRFstart=0,        distRFend=0,                closedStart=False,
# closedEnd=False,      vectorLRef=Vector(0.5,0.5), lateralCover=None,
# gapStart=None,        gapEnd=None,                extrShapeStart=None,
# extrShapeEnd=None,    fixLengthStart=None,        fixLengthEnd=None,
# extensionLength=None, maxLrebar=12,               position='poor',
# compression=False,    drawSketch=True,            nMembers=1,
# addCover=0,           addTxt2Label=None,    reinfCfg=cfg.defaultReinfConf)

# Bottom rebars
botRbLy1=trcm.brkRbFam(Id='1',fi=32e-3,nmbBars=4,position='good',gapStart=-1.0,gapEnd=2.0,addTxt2Label='(CAPA 1)')
botRbLy2=trcm.brkRbFam(Id='2',fi=25e-3,nmbBars=5,position='good',extrShapeStart='fix90_len500',lateralCover=0.1,vectorLRef=Vector(-0.3,-0.5))
botRbLy3=trcm.brkRbFam(Id='3',fi=16e-3,nmbBars=4,position='good',extrShapeEnd='fix45_len420')

# Top rebars
topRbLy1=trcm.brkRbFam(Id='4',fi=25e-3,nmbBars=5,position='poor',vectorLRef=Vector(-0.5,0.5),closedStart=True,closedEnd=True)
topRbLy2=trcm.brkRbFam(Id='5',fi=20e-3,nmbBars=4,position='poor',nMembers=3,closedStart=True,addTxt2Label='(CAPA 2)')#,extrShapeStart='anc90_posPoor_tens')

#Lateral rebars (left side)
latLRbLy1=trcm.brkRbFam(Id='6',fi=12e-3,s=0.20,position='good',extensionLength=0.2,vectorLRef=Vector(-0.5,0.5))
latLRbLy2=trcm.brkRbFam(Id='7',fi=10e-3,s=0.10,position='good',drawSketch=False,vectorLRef=Vector(-0.5,-0.5))
#Lateral rebars (right side)
latRRbLy1=trcm.brkRbFam(Id='8',fi=16e-3,s=0.15,position='good',maxLrebar=6.0,gapStart=-0.2,extrShapeStart='anc90_posPoor_tens')

# Stirrup families definition. Parameters and default values:
# fi,                    widthStirr=0.20,        sRealSh=None,
# sPerp=None,            Id=None,                nStirrRealSh=1,
# nStirrPerp=1,          dispRealSh=0,           dispPerp=0,
# vDirTrans=None,        vDirLong=Vector(1,0),   rightSideCover=True,
# vectorLRef=Vector(0.5,0.5), rightSideLabelLn=True,  closed=True,
# addL2closed=0.20,      fixAnchorStart=None,    fixAnchorEnd=None,
# nMembers=1,            addCover=0,             addTxt2Label=None,
# reinfCfg=cfg.defaultReinfConf

fiStirr=12e-3
stirr1=trcm.brkStirrFam(Id='9',fi=fiStirr,sRealSh=0,sPerp=0.15 ,nStirrRealSh=1 ,nStirrPerp=15 ,widthStirr=width-2*cover-fiStirr ,dispRealSh=-cover,dispPerp=0.30,addTxt2Label='stirrup text',vectorLRef=Vector(-0.3,-0.3))
fiStirr2=8e-3
stirr2=trcm.brkStirrFam(Id='10' ,fi=fiStirr2,sRealSh=0.5,sPerp=0.20 ,nStirrRealSh=2,nStirrPerp=30 ,widthStirr=0.35 ,dispRealSh=-cover-0.1,dispPerp=3.0 )

#                 *** END DATA ***


lstRebarFam=list()
lstStirrupFam=list()

# beam reinforcement
lstRebarFam1,lstStirrupFam1,newStartId=trcm.quad_beam_reinf(
    width=width,
    height=height,
    length=length,
    anchPtTrnsSect=Vector(0,0),
    anchPtLnSect=Vector(10*width,0),
    reinfCfg=reinfCfg,
    angTrns=angTrns,
    angLn=angLn,
    lstBotRb=[botRbLy1,botRbLy2,botRbLy3],
    lstTopRb=[topRbLy1,topRbLy2],
    lstLeftLatlRb=[latLRbLy1,latLRbLy2],
    lstRightLatlRb=[latRRbLy1],
    lstStirrReinf=[stirr1,stirr2],
    drawConcrTrSect=True,
    drawConcrLnSect=True,
    anchPtPlan=Vector(-10*width,0),
    angPlan=0,
    drawPlan=True,
    startId=1,
    clearDistRbLayers=None,
    aggrSize=20e-3)
lstRebarFam+=lstRebarFam1
lstStirrupFam+=lstStirrupFam1

doc=FreeCAD.newDocument("SCHEDULE")
rb.barSchedule(lstBarFamilies=lstRebarFam+lstStirrupFam,
               schCfg=cfg.XC_scheduleLvarCfg,
               title=titSchedule,
               pntTLcorner=Vector(1,1),
               doc=doc
)

