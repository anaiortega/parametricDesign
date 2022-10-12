# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from materials.ec2 import EC2_materials

concr=EC2_materials.C30
steel=EC2_materials.S500C

estrName='stirrup'

B=0.20
H=0.30
cover=0.03

reinfConf=rb.genericConf(cover=cover,xcConcr=concr,xcSteel=steel,texSize=0.0625,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2)
FreeCAD.newDocument(estrName+'_armados')

pt1=Vector(0,H)
pt2=Vector(B,H)
pt3=Vector(B,0)
pt4=Vector(0,0)


stirrup=rb.rebarFamily(
    genConf=reinfConf,
    identifier='ST',
    diameter=12e-3,
    nmbBars=10,
    lstPtsConcrSect=[pt1,pt2,pt3,pt4,pt1],
    )
    
lstRebarFam=[stirrup]
FreeCAD.newDocument(estrName+"_despiece")
rb.barSchedule(lstBarFamilies=lstRebarFam,
                       wColumns=[10,34,20,10,12,12],
                       hRows=10,
                       hText=2.5,
                       hTextSketch=2.5)
