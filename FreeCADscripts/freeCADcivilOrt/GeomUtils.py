# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
from FreeCAD import Base

def vectorUnitario(pto1,pto2):
    vunit=pto2.sub(pto1)
    vunit.normalize()
    return vunit

def escalarPorVector(escalar,vector):
    v=Base.Vector(escalar*vector.x,escalar*vector.y,escalar*vector.z)
    return v

def cara4ptos(pto1,pto2,pto3,pto4): 
    tr1=Part.Face(Part.makePolygon([pto1,pto2,pto3,pto1]))
    tr2=Part.Face(Part.makePolygon([pto1,pto3,pto4,pto1]))
    cara=Part.makeShell([tr1,tr2])
    return cara

def hexaedro8ptos(pto1,pto2,pto3,pto4,pto5,pto6,pto7,pto8):
    cara1=Part.Face(Part.makePolygon([pto1,pto2,pto3,pto4,pto1]))
    cara2=Part.Face(Part.makePolygon([pto5,pto8,pto7,pto6,pto5]))
    cara3=Part.Face(Part.makePolygon([pto1,pto4,pto8,pto5,pto1]))
    cara4=Part.Face(Part.makePolygon([pto4,pto8,pto7,pto3,pto4]))
    cara5=Part.Face(Part.makePolygon([pto2,pto3,pto7,pto6,pto2]))
    cara6=Part.Face(Part.makePolygon([pto1,pto5,pto6,pto2,pto1]))
    hexaedro=cara2.fuse(cara3.fuse(cara4.fuse(cara5.fuse(cara6.fuse(cara1)))))
    return hexaedro

