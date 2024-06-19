# -*- coding: utf-8 -*-

import bisect
import Part, FreeCAD, math
from freeCAD_civil import  draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from materials.ec2 import EC2_materials
from materials.ec2 import EC2_limit_state_checking as Lcalc

concr=EC2_materials.C30
steel=EC2_materials.S500C

estrName='split_rebar'

B=28
H=0.65
Lmax_rebar=12 # maxium lenght of rebar
cover=0

reinfConf=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=0.0625,Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')
pt0=Vector(0,H)
pt1=Vector(0,0)
pt2=Vector(B,0)
pt3=Vector(B,H)

rfam=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier='1',
    diameter=12e-3,
    spacing=0.20,
    lstPtsConcrSect=[pt0,pt1,pt2,pt3],
    fromToExtPts=[pt0,pt3],
    maxLrebar=Lmax_rebar,
    )

pts=rfam.getLstPtsRebar(rfam.lstPtsConcrSect)
wires=rfam.getLstRebars(pts)
rfam.drawLstRebar()
rfam.drawPolySectBars()

lstBarFamilies=[rfam]
rb.barSchedule(lstBarFamilies,title=estrName)





