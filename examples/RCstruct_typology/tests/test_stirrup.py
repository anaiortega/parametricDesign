# -*- coding: utf-8 -*-

import Part, FreeCAD, math
from parametric_design.freeCAD_civil import  draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from parametric_design.freeCAD_civil.structures import generic_RC_members as trcm
from materials.ec2 import EC2_materials

concr=EC2_materials.C30
steel=EC2_materials.S500C

estrName='stirrup'

B=0.20
H=0.30
cover=0.03

reinfConf=cfg.reinfConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=0.0625,Code='EC2',dynamEff=False,decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

pt1=Vector(0,H)
pt2=Vector(B,H)
pt3=Vector(B,0)
pt4=Vector(0,0)


stirrup=rb.rebarFamily(
    reinfCfg=reinfConf,
    identifier='ST',
    diameter=12e-3,
    nmbBars=10,
    lstPtsConcrSect=[pt1,pt2,pt3,pt4,pt1],
    )
    
lstRebarFam=[stirrup]
FreeCAD.newDocument(estrName+"_despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
               title=estrName
)
