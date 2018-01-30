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

def put_text_in_pnt(text,point,hText,justif="Left",rotation=None):
    '''Draws in the active document of FreeCAD the text in the specified point 
    with the font size, justificacion ("Left", "Center" or "Right") and rotation
    (expressed in degrees) given as parameters. 
    Justification defaults to "Left"
    Rotation defaults to None
    '''
    tx=Draft.makeText(text,point)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification =justif
    if rotation != None:
        FreeCADGui.ActiveDocument.getObject(tx.Name).Rotation =rotation
    return
    
