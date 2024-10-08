# -*- coding: utf-8 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2018, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

import Part, FreeCAD, math
import Draft
import FreeCADGui

def put_text_in_pnt(text,point,hText,color=(1.00,0.00,0.00),justif="Left",rotation=None):
    '''Draws in the active document of FreeCAD the text in the specified point 
    with the font size, justificacion ("Left", "Center" or "Right") and rotation
    (expressed in degrees) given as parameters. 
    Justification defaults to "Left"
    Rotation defaults to None
    '''
    if rotation != None:
        zaxis=FreeCAD.Vector(0, 0, 1)
        place=FreeCAD.Placement(point,FreeCAD.Rotation(zaxis,rotation))
        tx=Draft.make_text(text,place)
    else:
        tx=Draft.make_text(text,point)
    tx.ViewObject.FontSize = hText
    tx.ViewObject.Justification=justif
    tx.ViewObject.TextColor=color
    return tx

   
def draw_triang_prism(p1,p2,p3,vAxis):
    ''' Return a triangular prism whose base is defined by points p1,p2 and p3
    and its axis is defined by vector vAxis.
    '''
    baseContour=Part.makePolygon([p1,p2,p3,p1])
    base=Part.Face(baseContour)
    retSh=base.extrude(vAxis)
    return retSh

