# -*- coding: utf-8 -*-

__author__= "Ana Ortega (AOO) and Luis C. Pérez Tato (LCPT)"
__cppyright__= "Copyright 2015, AOO and LCPT"
__license__= "GPL"
__version__= "1.0"
__email__= "l.pereztato@gmail.com  ana.Ortega.Ort@gmail.com"

from __future__ import division

import math
import FreeCAD, Part, Draft
from FreeCAD import Base

class Underpass(object):
  '''Generation of a frame underpass in FreeCAD between two points of a
  defined longitudinal axis (it can be the axis of the road). 
  Approach slabs, footing under the walls, sloped deck,..., figure among 
  the capabilities implemented.
  Attributes:
    startLAxPoint: coordinates [X,Y,Z] of the starting point in the 
                   longitudinal axis where the structure begins
    endLAxPoint:   coordinates [X,Y,Z] of the ending point in the
                   longitudinal axis where the structure ends
    vertIntHeigAx:  vertical internal height in the central axis of the frame
    intSpan:        distance between internal faces of the walls
    baseSlabTh:     thickness of the base slab
    wallTh:         thickness of the walls
    deckTh:         deck thickness
    deckSlope:      deck slope
            ________________________________________
           |                     ^deckTh            |
           |    _________________↓______________    |
           |   |   deckSlope=Z/X ^              |   |
           |   |                 |              |   |
           |<->|                 |              |   |
           | wallTh              |              |   |
           |   |                Z|              |   |
           |   |                ^|vertIntHeigAx |   |
           |   |                ||              |   |     
           |   |                ||              |   |
           |   |                ||              |   |
           |   |                |↓___> X        |   |____Top plane of foundation
                                           
                       =              =
                <--------------><-------------->    
                <------------------------------>
                           intSpan






    posFrameLAxVect: local coordinates [x,y] of the longitudinal axis
                     referred to the coordinate system depicted in the
                     figure
            ________________________________________
           |                                        |
           |                                        |
           |                                        |
           |                                        |
           |                  ^Axis Y local         |
           |                  |                     |
           |                  |      [x,y]          |
           |                  |     *Position of    |
           |                  |      the longitudinal axis
           |                  |                     |
           |                  |                     |
           |                  |------------->       |____Top plane of foundation
                               Axis X local
                  =                   =
           <-----------------><-------------------->
  '''

  def __init__(self,startLAxPoint,endLAxPoint,posFrameLAxVect,vertIntHeigAx,intSpan,wallTh,deckTh,deckSlope):
    self.startLAxPoint=Base.Vector(startLAxPoint[0],startLAxPoint[1],startLAxPoint[2])
    self.endLAxPoint=Base.Vector(endLAxPoint[0],endLAxPoint[1],endLAxPoint[2])
    self.dispInPlaneVect=Base.Vector(-posFrameLAxVect[0],-posFrameLAxVect[1],0)
    self.vertIntHeigAx=vertIntHeigAx
    self.intSpan=intSpan
    self.wallTh=wallTh
    self.deckTh=deckTh
    self.deckSlope=deckSlope
    self.LAxisVector=self.endLAxPoint-self.startLAxPoint     #vector used for extrusions
    self.rotAngl=(-180/math.pi)*((self.endLAxPoint-self.startLAxPoint).projectToPlane(Base.Vector(0,0,0),Base.Vector(0,0,1))).getAngle(Base.Vector(0,1,0))                        #rotation angle

  def placeAndExtrudeShape(self,shName):
    '''place the shape in the initial position of the longitudinal axis
    and extrudes it until the end point
    '''
    shName.translate(self.dispInPlaneVect)
    shName.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),self.rotAngl)
    shName.translate(self.startLAxPoint)
    retSh=shName.extrude(self.LAxisVector)
    return retSh

  def genDeckAndWalls(self):
    '''Returns a compound with the deck and walls of the structure'''
    #Deck
    pto1=Base.Vector(0,0,0)
    pto2=pto1.add(Base.Vector(-self.intSpan/2,0))
    pto3=pto2.add(Base.Vector(-self.wallTh,0,0))
    pto13=Base.Vector(-pto3.x,0,pto3.z)
    pto14=Base.Vector(-pto2.x,0,pto2.z)
    pto15=pto1.add(Base.Vector(0,0,self.vertIntHeigAx))
    pto16=pto15.add(Base.Vector(-self.intSpan/2,0,-self.deckSlope*self.intSpan/2))
    pto17=pto16.add(Base.Vector(-self.wallTh,0,-self.deckSlope*self.wallTh*self.wallTh))
    pto22=pto15.add(Base.Vector(self.intSpan/2,0,self.deckSlope*self.intSpan/2))
    pto21=pto22.add(Base.Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh))
    deckThVert=self.deckTh*(1+self.deckSlope**2)**(1/2)
    pto18=pto17.add(Base.Vector(0,0,deckThVert))
    pto19=pto15.add(Base.Vector(0,0,deckThVert))
    pto20=pto21.add(Base.Vector(0,0,deckThVert))
    linDeck=Part.makePolygon([pto15,pto16,pto17,pto18,pto19,pto20,pto21,pto22,pto15])
    deck=Part.Face(linDeck)
    #Walls
    linLeftWall=Part.makePolygon([pto2,pto3,pto17,pto16,pto2])
    leftWall=Part.Face(linLeftWall)
    linRightWall=Part.makePolygon([pto13,pto14,pto22,pto21,pto13])
    rightWall=Part.Face(linRightWall)
    retComp=Part.makeCompound([deck,leftWall,rightWall])
    return self.placeAndExtrudeShape(retComp)

  def genSlabFound(self,baseSlabTh,slabWdtUnderFilling):
    '''Returns a compound with the slab foundation (constant thickness)
    Parameters:
      baseSlabTh:          thickness of the base slab
      slabtWdtUnderFilling:with of slab under the filling  
    '''
    pto1=Base.Vector(0,0,0)
    pto2=pto1.add(Base.Vector(-self.intSpan/2,0))
    pto3=pto2.add(Base.Vector(-self.wallTh,0,0))
    pto4=pto3.add(Base.Vector(-slabWdtUnderFilling,0,0))
    pto5=pto4.add(Base.Vector(0,0,-baseSlabTh))
    pto6=pto1.add(Base.Vector(0,0,-baseSlabTh))
    pto7=Base.Vector(-pto5.x,0,pto5.z)
    pto8=Base.Vector(-pto4.x,0,pto4.z)
    pto9=Base.Vector(-pto3.x,0,pto3.z)
    pto10=Base.Vector(-pto2.x,0,pto2.z)
    linFoundation=Part.makePolygon([pto1,pto2,pto3,pto4,pto5,pto6,pto7,pto8,pto9,pto10,pto1])
    foundation=Part.Face(linFoundation)
    retComp=Part.makeCompound([foundation])
    return self.placeAndExtrudeShape(retComp)

  def genSlabWithFootFound(self,baseSlabTh,footWdtUnderFilling,footingTh,footingWdt,footSlope):
    '''Returns a compound with the foundation consisting in a slab with
    footing under the walls 
    Parameters:
      baseSlabTh:          thickness of the base slab
      footWdtUnderFilling: with of footing under the filling
      footingTh:           thickness of the wall footings
      footingWdt:          width of the wall footing (in the zone of constant thickness)
      footSlope:           slope of the wall footing y/x (in the zone of variable thickness)
    '''
    pto1=Base.Vector(0,0,0)
    pto2=pto1.add(Base.Vector(-self.intSpan/2,0))
    pto3=pto2.add(Base.Vector(-self.wallTh,0,0))
    pto4=pto3.add(Base.Vector(-footWdtUnderFilling,0,0))
    pto5=pto4.add(Base.Vector(0,0,-footingTh))
    pto6=pto5.add(Base.Vector(footingWdt,0,0))
    pto7=pto6.add(Base.Vector(1/footSlope*(footingTh-baseSlabTh),0,footingTh-baseSlabTh))
    pto8=pto1.add(Base.Vector(0,0,-baseSlabTh))
    pto9=Base.Vector(-pto7.x,0,pto7.z)
    pto10=Base.Vector(-pto6.x,0,pto6.z)
    pto11=Base.Vector(-pto5.x,0,pto5.z)
    pto12=Base.Vector(-pto4.x,0,pto4.z)
    pto13=Base.Vector(-pto3.x,0,pto3.z)
    pto14=Base.Vector(-pto2.x,0,pto2.z)
    linFoundation=Part.makePolygon([pto1,pto2,pto3,pto4,pto5,pto6,pto7,pto8,pto9,pto10,pto11,pto12,pto13,pto14,pto1])
    foundation=Part.Face(linFoundation)
    retComp=Part.makeCompound([foundation]) 
    return self.placeAndExtrudeShape(retComp)

  def genApproachSlabs(self,apSlabTh,apSlabWdt,apSlabSlp,apSlabSuppWdt,apSlabSuppTh):
    '''Generates two approach slabs (on both sides of the structure)
    Parameters:
      apSlabTh:     thickness of the approach slabs
      apSlabWdt:    width of the approach slabs
      apSlabSlp:    slope of the approach slabs
      apSlabSuppWdt:width of the support for the approach slab
      apSlabSuppTh: thickness of the support for the approach slab
    '''
    #Supports of the approach slabs
    pto1=Base.Vector(0,0,0)
    pto15=pto1.add(Base.Vector(0,0,self.vertIntHeigAx))
    pto16=pto15.add(Base.Vector(-self.intSpan/2,0,-self.deckSlope*self.intSpan/2))
    pto17=pto16.add(Base.Vector(-self.wallTh,0,-self.deckSlope*self.wallTh*self.wallTh))
    pto23=pto17.add(Base.Vector(-apSlabSuppWdt,0,0))
    pto24=pto23.add(Base.Vector(0,0,-apSlabSuppTh))
    pto25=pto24.add(Base.Vector(apSlabSuppWdt,0,0))
    linLeftSup=Part.makePolygon([pto17,pto23,pto24,pto25,pto17])
    leftSup=Part.Face(linLeftSup)
    pto22=pto15.add(Base.Vector(self.intSpan/2,0,self.deckSlope*self.intSpan/2))
    pto21=pto22.add(Base.Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh))
    pto26=pto21.add(Base.Vector(apSlabSuppWdt,0,0))
    pto27=pto26.add(Base.Vector(0,0,-apSlabSuppTh))
    pto28=pto27.add(Base.Vector(-apSlabSuppWdt,0,0))
    linRightSup=Part.makePolygon([pto21,pto26,pto27,pto28,pto21])
    rightSup=Part.Face(linRightSup)
    #Approach slabs
    pto29=pto23.add(Base.Vector(-apSlabWdt,0,-apSlabSlp*apSlabWdt))
    apslabThVert=apSlabTh*(1+apSlabSlp**2)**(1/2)
    pto30=pto29.add(Base.Vector(0,0,apslabThVert))
    pto31=pto17.add(Base.Vector(0,0,apslabThVert))
    linLeftApSlab=Part.makePolygon([pto17,pto29,pto30,pto31,pto17])
    leftApSlab=Part.Face(linLeftApSlab)
    pto32=pto21.add(Base.Vector(apSlabWdt,0,-apSlabSlp*apSlabWdt))
    pto33=pto32.add(Base.Vector(0,0,apslabThVert))
    pto34=pto21.add(Base.Vector(0,0,apslabThVert))
    linRightApSlab=Part.makePolygon([pto21,pto32,pto33,pto34,pto21])
    rightApSlab=Part.Face(linRightApSlab)
    retComp=Part.makeCompound([leftSup,rightSup,leftApSlab,rightApSlab])
    return self.placeAndExtrudeShape(retComp)
    

class Wingwall(object):
  '''Generation of a wingwall                                             
                                                                         wallTopWidth
                  wallLenght                                             <----->
         <-----------------------------> __wallTopLevel                  ___.___
         |  +                                            ______________ /   |   \
         |     +                                           /\   /\     /    .    \
         |        +                                                   /     |     \
         |           +   __1__                           intraSlope  /      .      \ extraSlope
         |              +     | wallSlope                      _↓__ /       |       \_↓__
         |                 +                                   |   /                 \  |          
         |                    +                               1|  /                   \ |1
         |                       +                             | /                     \|
         ^ Z                         +                         |/           ^Z          \
         |                             |                       /            |            \
         |                             |                      /             |             \
         |--------->Y                  |                     /              |-------->X    \
         |_____________________________| __foundLevel   ____/_______________________________\_____ 
         |          |         |________|              ^|                                          |
         |          |_________|            footsHeight||                                          |
         |__________|                                 ↓|__________________________________________|
         <----------><--------><------->               <------------------->
          footsLength                                    footsIntraWidth
                                                       <----------------------------------------->
                                                                      footsWidth


  '''
  def __init__(self,wallTopLevel,foundLevel,wallLenght,wallSlope,wallTopWidth,intraSlope,extraSlope):
    self.wallTopLevel=wallTopLevel
    self.foundLevel=foundLevel
    self.wallLenght=wallLenght
    self.wallSlope=wallSlope
    self.wallTopWidth=wallTopWidth
    self.intraSlope=intraSlope
    self.extraSlope=extraSlope

  def genWingwall(self):
    hStartWall=abs(self.wallTopLevel-self.foundLevel)
    endWallTopLevel=self.wallTopLevel-self.wallLenght*self.wallSlope
    hEndWall=abs(endWallTopLevel-self.foundLevel)
    hEndWall=hStartWall-self.wallLenght*self.wallSlope
    pto1=Base.Vector(-self.wallTopWidth/2.0,0,self.wallTopLevel)
    pto2=Base.Vector(self.wallTopWidth/2.0,0,self.wallTopLevel)
    pto3=pto1.add(Base.Vector(-(hStartWall*self.intraSlope),0,-hStartWall))
    pto4=pto2.add(Base.Vector(hStartWall*self.extraSlope,0,-hStartWall))
    pto5=Base.Vector(-self.wallTopWidth/2.0,self.wallLenght,endWallTopLevel)
    pto6=Base.Vector(self.wallTopWidth/2.0,self.wallLenght,endWallTopLevel)
    pto7=pto5.add(Base.Vector(-(hEndWall*self.intraSlope),0,-hEndWall))
    pto8=pto6.add(Base.Vector(hEndWall*self.extraSlope,0,-hEndWall))
    faceTr1=Part.Face(Part.makePolygon([pto1,pto2,pto4,pto3,pto1]))
    faceTr2=Part.Face(Part.makePolygon([pto5,pto6,pto8,pto7,pto5]))
    faceTop=Part.Face(Part.makePolygon([pto1,pto2,pto6,pto5,pto1]))
    faceBot=Part.Face(Part.makePolygon([pto3,pto4,pto8,pto7,pto3]))
    faceIntra=Part.Face(Part.makePolygon([pto1,pto5,pto7,pto3,pto1]))
    faceExtra=Part.Face(Part.makePolygon([pto2,pto6,pto8,pto4,pto2]))
    retComp=Part.makeCompound([faceTr1,faceTr2,faceTop,faceBot,faceIntra,faceExtra])
    return retComp

  def genWingwallFoundation(self,footsLength,footsHeight,footsWidth,footsIntraWidth):
    return



wingWall=Wingwall(wallTopLevel=5,foundLevel=-1,wallLenght=6,wallSlope=1/3.0,wallTopWidth=0.5,intraSlope=1/5.0,extraSlope=1/10.0)
ww=wingWall.genWingwall()
Part.show(ww)

struct=Underpass(startLAxPoint=[0,0,0],endLAxPoint=[10,10,1],posFrameLAxVect=[00,0],vertIntHeigAx=7,intSpan=10.75,wallTh=0.5,deckTh=0.5,deckSlope=0.04)
dw=struct.genDeckAndWalls()
Part.show(dw)

slabFound=struct.genSlabFound(baseSlabTh=0.3,slabWdtUnderFilling=0.5)
Part.show(slabFound)

SlabWFoot=struct.genSlabWithFootFound(baseSlabTh=0.3,footWdtUnderFilling=0.5,footingTh=0.8,footingWdt=2.5,footSlope=1)
Part.show(SlabWFoot)
appSlabs=struct.genApproachSlabs(apSlabTh=0.2,apSlabWdt=4.5,apSlabSlp=0.04,apSlabSuppWdt=0.3,apSlabSuppTh=0.3)
Part.show(appSlabs)

eje=Part.makeLine(struct.startLAxPoint,struct.endLAxPoint)
Part.show(eje)
