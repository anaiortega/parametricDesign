# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
from FreeCAD import Vector

def vectorUnitario(pto1,pto2):
    vunit=pto2.sub(pto1)
    vunit.normalize()
    return vunit

def escalarPorVector(escalar,vector):
    v=Vector(escalar*vector.x,escalar*vector.y,escalar*vector.z)
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

def int2lines(P1,P2,P3,P4):
    ''' Return the intersection point of two lines

    :param P1 y P2: points that define line 1.
    :param P3 y P4: points that define line 2.
    '''
    if P1.x == P2.x:
        if P3.x == P4.x:
            print('Rectas paralelas')
            Pinters=()
        else:
            xinters=P1.x
            m2=1.0*(P4.y-P3.y)/(P4.x-P3.x) #pte. de la 2a. recta
            b2=P3.y-m2*P3.x            # ordenada pto. de corte 2a. recta con eje Y
            yinters=m2*xinters+b2
            Pinters=Vector(xinters,yinters)
    elif P3.x == P4.x:
        xinters=P3.x
        m1=1.0*(P2.y-P1.y)/(P2.x-P1.x) #pte. de la 2a. recta
        b1=P1.y-m1*P1.x            # ordenada pto. de corte 2a. recta con eje Y
        yinters=m1*xinters+b1
        Pinters=Vector(xinters,yinters)
    else:
        m1=1.0*(P2.y-P1.y)/(P2.x-P1.x) #pte. de la 1a. recta
        b1=P1.y-m1*P1.x            # ordenada pto. de corte 1a. recta con eje Y
        m2=1.0*(P4.y-P3.y)/(P4.x-P3.x) #pte. de la 2a. recta
        b2=P3.y-m2*P3.x            # ordenada pto. de corte 2a. recta con eje Y
        if m1 == m2:
            print('Rectas paralelas')
            Pinters=()
        else:
            xinters=1.0*(b2-b1)/(m1-m2)
            yinters=m1*xinters+b1
            Pinters=Vector(xinters,yinters)
    return Pinters

def getRotatedVector(v,vrotAxis,angle):
    '''Return the vector v rotated an angle (expressed in degrees)  around 
    axis defined by the vector vrotAxis'''
    angRad=math.radians(angle)
    retV=math.cos(angRad)*v+math.sin(angRad)*(vrotAxis.cross(v))
    return retV
