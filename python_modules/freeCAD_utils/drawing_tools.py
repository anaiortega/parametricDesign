# -*- coding: iso-8859-1 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2018, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

import Part, FreeCAD, math
import Draft
from FreeCAD import Vector
import FreeCADGui

def put_text_in_pnt(text,point,hText,color,justif="Left",rotation=None):
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
    print('fontsize=',tx.ViewObject.FontSize)
    tx.ViewObject.Justification=justif
    tx.ViewObject.TextColor=color
    return

    
