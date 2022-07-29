# -*- coding: utf-8 -*-

from __future__ import division

__author__= "Ana Ortega (AO_O)"
__cppyright__= "Copyright 2015, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= " l.pereztato@gmail.com"



import numpy as np
import math
import sys
sys.path.append('./tools')
from setting_out import sett_out_tools as too
from tabulate import tabulate

# DATA
# X, Y coordinates of the point of intersection of the road axis with the
# structure axis.
xAxesInters=727208.208 
yAxesInters=4324243.525
# azimuth of the road axis in the intersection of axes [grads].
# (clockwise from the north line base)
azimuthRoad=207.628   
# azimuth of the structure longitudinal axis [grads].
# (clockwise from the north line base)
azimuthStruct=azimuthRoad-100

# Projected lengths of structure left and right sides from the road axis,
# looking in the forward direction of PKs
# Lleft=17.10
# Lright=14.22
LaxisNeg=14.22
LaxisPos=17.10
# Clearance gauge (horizontal)
Hgauge=8.00
# Wall thickness
thWall=0.70


# Marco
(pt_start_aleta1,pt_start_aleta2,pt_start_aleta3,pt_start_aleta4)=too.sett_out_marco(xAxesInters,yAxesInters,azimuthStruct,Hgauge,thWall,LaxisNeg,LaxisPos,skewAngle=0)
print pt_start_aleta1

#Aleta 1       
#start_point=pt_start_aleta1
start_point=np.array([727194.65176465,4324249.89107282])/1e5

azimuthAleta=azimuthStruct+200+too.degr_to_grads(30.)
azimuthPuntera=azimuthAleta-100.
wCoron=0.30
lengths=[6.20,5.30]
widths=[5.05,3.25]
widthsPuntera=[1.45,0.90]

pt_end_aleta1=too.end_point_aleta(start_point,azimuthAleta,lengths)
points_aleta1=too.sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera)



#Plotting of results in FreeCAD
import Part, FreeCAD, math
from Draft import *
from freeCAD_civil import plot_tools as plot
App.newDocument("aleta")
aleta1found=plot.create_wire_lstPt(lstPoints=points_aleta1,closed=True)
aleta1wall=plot.create_wire_lstPt(lstPoints=[start_point,pt_end_aleta1],closed=False)
