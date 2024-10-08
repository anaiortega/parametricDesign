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
from parametric_design.setting_out import sett_out_tools as too
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


#END DATA

# Marco
(pt_start_aleta1,pt_start_aleta2,pt_start_aleta3,pt_start_aleta4)=too.sett_out_marco(xAxesInters,yAxesInters,azimuthStruct,Hgauge,thWall,LaxisNeg,LaxisPos,skewAngle=0)

#Aleta 1       
start_point=pt_start_aleta1
azimuthAleta=azimuthStruct+200+too.degr_to_grads(30)
azimuthPuntera=azimuthAleta-100
wCoron=0.30
lengths=[6.20,5.30]
widths=[5.05,3.25]
widthsPuntera=[1.45,0.90]

pt_end_aleta1=too.end_point_aleta(start_point,azimuthAleta,lengths)
points_aleta1=too.sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera)

quit()
#Aleta 2       
start_point=pt_start_aleta2
azimuthAleta=azimuthStruct+200-too.degr_to_grads(30)
azimuthPuntera=azimuthAleta+100
wCoron=0.30
lengths=[5.80,3.80]
widths=[5.05,3.25]
widthsPuntera=[1.45,0.90]

pt_end_aleta2=too.end_point_aleta(start_point,azimuthAleta,lengths)
points_aleta2=too.sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera)

#Aleta 3       
start_point=pt_start_aleta3
azimuthAleta=azimuthStruct+too.degr_to_grads(30)
azimuthPuntera=azimuthAleta-100
wCoron=0.30
lengths=[6.00,6.50]
widths=[4.55,3.25]
widthsPuntera=[1.35,0.90]

pt_end_aleta3=too.end_point_aleta(start_point,azimuthAleta,lengths)
points_aleta3=too.sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera)

#Aleta 4       
start_point=pt_start_aleta4
azimuthAleta=azimuthStruct-too.degr_to_grads(30)
azimuthPuntera=azimuthAleta+100
wCoron=0.30
lengths=[6.10,6.40]
widths=[5.05,3.25]
widthsPuntera=[1.45,0.90]

pt_end_aleta4=too.end_point_aleta(start_point,azimuthAleta,lengths)
points_aleta4=too.sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera)
# print tabulate(points_aleta4,headers=['PTO','X', 'Y'], floatfmt=".3f", tablefmt="simple")

#Puntos cuadro de replanteo
points_cuadr_repl=np.array([pt_start_aleta1,pt_start_aleta2,pt_start_aleta3,pt_start_aleta4,pt_end_aleta1,pt_end_aleta2,pt_end_aleta3,pt_end_aleta4])

#Writting of results to a file
too.write_points_to_file(title='CUADRO DE REPLANTEO',pointsArr=points_cuadr_repl,nDecimalP=3,fileName='lst_underpass.txt',indPntChr=False)
too.write_points_to_file(title='ALETA 1',pointsArr=points_aleta1,nDecimalP=3,fileName='lst_underpass.txt',indPntChr=True)
too.write_points_to_file(title='ALETA 2',pointsArr=points_aleta2,nDecimalP=3,fileName='lst_underpass.txt',indPntChr=True)
too.write_points_to_file(title='ALETA 3',pointsArr=points_aleta3,nDecimalP=3,fileName='lst_underpass.txt',indPntChr=True)
too.write_points_to_file(title='ALETA 4',pointsArr=points_aleta4,nDecimalP=3,fileName='lst_underpass.txt',indPntChr=True)


#Plotting of results in FreeCAD
import Part, FreeCAD, math
from Draft import *
from parametric_design.freeCAD_civil import plot_tools as plot
App.newDocument("marco3")
marco=plot.create_wire_lstPt(lstPoints=points_cuadr_repl[0:4],closed=True)
#FreeCADGui.ActiveDocument.getObject(marco.Name).LineColor = (0.00,1.00,0.00)
aleta1found=plot.create_wire_lstPt(lstPoints=points_aleta1,closed=True)
aleta2found=plot.create_wire_lstPt(lstPoints=points_aleta2,closed=True)
aleta3found=plot.create_wire_lstPt(lstPoints=points_aleta3,closed=True)
aleta4found=plot.create_wire_lstPt(lstPoints=points_aleta4,closed=True)

aleta1wall=plot.create_wire_lstPt(lstPoints=[pt_start_aleta1,pt_end_aleta1],closed=False)
aleta2wall=plot.create_wire_lstPt(lstPoints=[pt_start_aleta2,pt_end_aleta2],closed=False)
aleta3wall=plot.create_wire_lstPt(lstPoints=[pt_start_aleta3,pt_end_aleta3],closed=False)
aleta4wall=plot.create_wire_lstPt(lstPoints=[pt_start_aleta4,pt_end_aleta4],closed=False)
