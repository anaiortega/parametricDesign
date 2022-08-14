# -*- coding: iso-8859-1 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2017, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

from FreeCAD import Vector
from freeCAD_civil.structures import typical_RC_members as trcm
from freeCAD_civil import reinf_bars as rb

height=4 #dimension of the slab in the direction of the vertical rebars
length=5 #dimension of the slab in the direction of the horizontal rebars
thickness=0.4  #thickness of the slab
# left vertical rebars data
leftVertRb={'id':'1','fi':20e-3,'s':0.15,'gapL':0.2,'gapR':0} 
# right vertical rebars data
leftHorRb={'id':'2','fi':16e-3,'s':0.20,'gapL':0.1,'gapR':0.5}
# lefttom horizontal rebars data
rightVertRb={'id':'3','fi':20e-3,'s':0.15,'gapL':0.2,'gapR':0.1} 
# right horizontal rebars data
rightHorRb={'id':'4','fi':16e-3,'s':0.20,'gapL':0.1,'gapR':0.3}

anchPtVertSect=Vector(0,0) #anchor point to place the bottom left corner of the concrete vertical cross-section
anchPtHorSect=anchPtVertSect+Vector(thickness+3,0) #anchor point to place the bottom left corner of the concrete horizontal cross-section

genConf=rb.genericConf(cover=35e-3,texSize=0.125,Code='EHE',concrType='HA-30',steelType='B-500',dynamEff='N',decLengths=2,decSpacing=2)

trcm.wall(height,length,thickness,leftVertRb,rightVertRb,leftHorRb,rightHorRb,anchPtVertSect,anchPtHorSect,genConf,drawConrVertSect='N',drawConrHorSect='N')           
