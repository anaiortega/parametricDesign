# -*- coding: utf-8 -*-

from Draft import makeWire
from FreeCAD import Base

def create_wire_lstPt(lstPoints,closed=True):
    '''Create in the active document of FreeCAD  the wire that 
    joins the points in a list passed as parameter.

    :param lstPoints: list of point coordinates, of type: 
    [[xpto1,ypto1],[xpto2,ypto2],...]
    :param closed:  =True(default) for a closed wire, =False for an open wire.
    '''
    lstFreeCadPts=[Base.Vector(*pt) for pt in lstPoints]
    l=makeWire(lstFreeCadPts,closed)
    return l

