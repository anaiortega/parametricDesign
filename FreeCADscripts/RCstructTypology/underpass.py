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

def PlaceShpPtVect(shapeId,ptOrig,vDirOrig,ptDest,vDirDest):
  '''Translates the shape from point ptOrig to point ptDest and
  rotates it in such a way that the direction defined with the vector
  vDirOrig turn into the vDirDest direction
  '''
  shapeId.translate(ptDest-ptOrig)
  vPerp=vDirOrig.cross(vDirDest)
  angRot=vDirOrig.getAngle(vDirDest)
  shapeId.rotate(ptDest,vPerp,angRot*180/math.pi)
  return shapeId
 

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
    posFrameLAxVect: position [x,0,z] of the longitudinal axis in the
                     section type

     kpETL  ________________________________________ kpETR
           |                     ^deckTh            |
           |    _________________↓______________    |
           |   |   deckSlope=Z/X ^         kpITR|   |
           |   |kpITL            |              |   |
           |<->|                 |              |   |
           | wallTh              |              |   |
           |   |                Z|              |   |
           |   |                ^|vertIntHeigAx |   |
           |   |                ||              |   |     
           |   |                ||              |   |
           |   |                ||*posFrameLAxVec   |
     kpEBL |   |kpIBL           |↓___> X        |   |____Top plane of foundation
                                           kpIBR     kpEBR
                       =              =
                <--------------><-------------->    
                <------------------------------>
                           intSpan

  '''

  def __init__(self,startLAxPoint,endLAxPoint,posFrameLAxVect,vertIntHeigAx,intSpan,wallTh,deckTh,deckSlope):
    self.startLAxPoint=Base.Vector(startLAxPoint[0],startLAxPoint[1],startLAxPoint[2])
    self.endLAxPoint=Base.Vector(endLAxPoint[0],endLAxPoint[1],endLAxPoint[2])
    self.ptLAxis=Base.Vector(posFrameLAxVect[0],0,posFrameLAxVect[2])
    self.vertIntHeigAx=vertIntHeigAx
    self.intSpan=intSpan
    self.wallTh=wallTh
    self.deckTh=deckTh
    self.deckSlope=deckSlope
    self.LAxisVector=self.endLAxPoint-self.startLAxPoint     #vector used for extrusions
    self.rotAngl=(-180/math.pi)*((self.endLAxPoint-self.startLAxPoint).projectToPlane(Base.Vector(0,0,0),Base.Vector(0,0,1))).getAngle(Base.Vector(0,1,0))                        #rotation angle
    self.deckThVert=self.deckTh*(1+self.deckSlope**2)**(1/2)
    #keypoints: 
    self.kpIBL=Base.Vector(-self.intSpan/2,0,0)    #internal bottom left
    self.kpIBR=Base.Vector(self.intSpan/2,0,0)     #internal bottom right
    self.kpEBL=self.kpIBL.add(Base.Vector(-self.wallTh,0,0))  #external bottom left
    self.kpEBR=self.kpIBR.add(Base.Vector(self.wallTh,0,0))   #external bottom right
    self.kpITL=Base.Vector(-self.intSpan/2,0,self.vertIntHeigAx-self.deckSlope*self.intSpan/2)  #internal top left
    self.kpITR=Base.Vector(self.intSpan/2,0,self.vertIntHeigAx+self.deckSlope*self.intSpan/2)   #internal top right
    self.kpETL=self.kpITL.add(Base.Vector(-self.wallTh,0,self.deckThVert-self.deckSlope*self.wallTh*self.wallTh))  #external top left
    self.kpETR=self.kpITR.add(Base.Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh+self.deckThVert))   #external top right

  def getDirecVectLAxis(self):
    '''returns the director vector of the longitudinal axis'''
    vDirec=(self.endLAxPoint-self.startLAxPoint).normalize()
    return vDirec
    
  def placeAndExtrudeShape(self,shName):
    '''place the shape in the initial position of the longitudinal axis
    and extrudes it until the end point
    '''
    PlaceShpPtVect(shapeId=shName,ptOrig=self.ptLAxis,vDirOrig=Base.Vector(0,1,0),ptDest=self.startLAxPoint,vDirDest=Base.Vector(self.LAxisVector.x,self.LAxisVector.y,0))
    retSh=shName.extrude(self.LAxisVector)
    return retSh

  def genDeckAndWalls(self):
    '''Returns a compound with the deck and walls of the structure'''
    #Deck
    ptDeckBL=self.kpITL.add(Base.Vector(-self.wallTh,0,-self.deckSlope*self.wallTh*self.wallTh))
    ptDeckBR=self.kpITR.add(Base.Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh))
    linDeck=Part.makePolygon([self.kpITL,ptDeckBL,self.kpETL,self.kpETR,ptDeckBR,self.kpITR,self.kpITL])
    deck=Part.Face(linDeck)
    #Walls
    linLeftWall=Part.makePolygon([self.kpIBL,self.kpEBL,ptDeckBL,self.kpITL,self.kpIBL])
    leftWall=Part.Face(linLeftWall)
    linRightWall=Part.makePolygon([self.kpEBR,self.kpIBR,self.kpITR,ptDeckBR,self.kpEBR])
    rightWall=Part.Face(linRightWall)
    retComp=Part.makeCompound([deck,leftWall,rightWall])
    return self.placeAndExtrudeShape(retComp)

  def genSlabFound(self,baseSlabTh,slabWdtUnderFilling):
    '''Returns a compound with the slab foundation (constant thickness)
    Parameters:
      baseSlabTh:          thickness of the base slab
      slabtWdtUnderFilling:with of slab under the filling  
    '''
    ptSlabTL=self.kpEBL.add(Base.Vector(-slabWdtUnderFilling,0,0))
    ptSlabBL=ptSlabTL.add(Base.Vector(0,0,-baseSlabTh))
    ptSlabTR=self.kpEBR.add(Base.Vector(slabWdtUnderFilling,0,0))
    ptSlabBR=ptSlabTR.add(Base.Vector(0,0,-baseSlabTh))
    linFoundation=Part.makePolygon([ptSlabTL,ptSlabBL,ptSlabBR,ptSlabTR,ptSlabTL])
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
    self.kpIBL=Base.Vector(-self.intSpan/2,0)
    self.kpEBL=self.kpIBL.add(Base.Vector(-self.wallTh,0,0))
    ptFootTL=self.kpEBL.add(Base.Vector(-footWdtUnderFilling,0,0))
    ptFootBL=ptFootTL.add(Base.Vector(0,0,-footingTh))
    ptFootBL2=ptFootBL.add(Base.Vector(footingWdt,0,0))
    ptFootBL3=ptFootBL2.add(Base.Vector(1/footSlope*(footingTh-baseSlabTh),0,footingTh-baseSlabTh))
    ptFootBR3=Base.Vector(-ptFootBL3.x,0,ptFootBL3.z)
    ptFootBR2=Base.Vector(-ptFootBL2.x,0,ptFootBL2.z)
    ptFootBR=Base.Vector(-ptFootBL.x,0,ptFootBL.z)
    ptFootTR=Base.Vector(-ptFootTL.x,0,ptFootTL.z)
    linFoundation=Part.makePolygon([self.kpIBL,self.kpEBL,ptFootTL,ptFootBL,ptFootBL2,ptFootBL3,ptFootBR3,ptFootBR2,ptFootBR,ptFootTR,self.kpEBR,self.kpIBR,self.kpIBL])
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
    ptDeckBL=self.kpITL.add(Base.Vector(-self.wallTh,0,-self.deckSlope*self.wallTh*self.wallTh))
    ptLSup1=ptDeckBL.add(Base.Vector(-apSlabSuppWdt,0,0))
    ptLSup2=ptLSup1.add(Base.Vector(0,0,-apSlabSuppTh))
    ptLSup3=ptLSup2.add(Base.Vector(apSlabSuppWdt,0,0))
    linLeftSup=Part.makePolygon([ptDeckBL,ptLSup1,ptLSup2,ptLSup3,ptDeckBL])
    leftSup=Part.Face(linLeftSup)
    ptDeckBR=self.kpITR.add(Base.Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh))
    ptRSup1=ptDeckBR.add(Base.Vector(apSlabSuppWdt,0,0))
    ptRSup2=ptRSup1.add(Base.Vector(0,0,-apSlabSuppTh))
    ptRSup3=ptRSup2.add(Base.Vector(-apSlabSuppWdt,0,0))
    linRightSup=Part.makePolygon([ptDeckBR,ptRSup1,ptRSup2,ptRSup3,ptDeckBR])
    rightSup=Part.Face(linRightSup)
    #Approach slabs
    ptLApSlab1=ptLSup1.add(Base.Vector(-apSlabWdt,0,-apSlabSlp*apSlabWdt))
    apslabThVert=apSlabTh*(1+apSlabSlp**2)**(1/2)
    ptLApSlab2=ptLApSlab1.add(Base.Vector(0,0,apslabThVert))
    ptLApSlab3=ptDeckBL.add(Base.Vector(0,0,apslabThVert))
    linLeftApSlab=Part.makePolygon([ptDeckBL,ptLApSlab1,ptLApSlab2,ptLApSlab3,ptDeckBL])
    leftApSlab=Part.Face(linLeftApSlab)
    ptRApSlab1=ptDeckBR.add(Base.Vector(apSlabWdt,0,-apSlabSlp*apSlabWdt))
    ptRApSlab2=ptRApSlab1.add(Base.Vector(0,0,apslabThVert))
    ptRApSlab3=ptDeckBR.add(Base.Vector(0,0,apslabThVert))
    linRightApSlab=Part.makePolygon([ptDeckBR,ptRApSlab1,ptRApSlab2,ptRApSlab3,ptDeckBR])
    rightApSlab=Part.Face(linRightApSlab)
    retComp=Part.makeCompound([leftSup,rightSup,leftApSlab,rightApSlab])
    return self.placeAndExtrudeShape(retComp)

  def genHeadWall(self,leftHeight,rightHeight,thickness,section):
    '''Generates the headwall over the end section of the structure
    Parameters:
      leftHeight:  heigth of the headwall in the left side of the deck
      rightHeight: heigth of the headwall in the right side of the deck
      thickness:   thickness of the headwall (longitudinal direction)
      section:     ='I' generates de headwall in the initial section of the structure
                   ='E'     "      "    "      "  "  ending    "     "   "     "
    '''
    ptWallTL=self.kpETL.add(Base.Vector(0,0,leftHeight))
    ptWallTR=self.kpETR.add(Base.Vector(0,0,rightHeight))
    linWall=Part.makePolygon([self.kpETL,self.kpETR,ptWallTR,ptWallTL,self.kpETL])
    headwall=Part.Face(linWall)
    vectExtr=(self.endLAxPoint-self.startLAxPoint)
    if section =='I':
      ptDestination=self.startLAxPoint
      vectExtr.normalize().multiply(thickness)
    else:
      ptDestination=self.endLAxPoint
      vectExtr.normalize().multiply(-thickness)
    PlaceShpPtVect(shapeId=headwall,ptOrig=self.ptLAxis,vDirOrig=Base.Vector(0,1,0),ptDest=ptDestination,vDirDest=Base.Vector(self.LAxisVector.x,self.LAxisVector.y,0))
    retSh=headwall.extrude(vectExtr)
    return retSh

  def getPtStrPKAxis(self,ptSectType,longAxisPK):
    '''Returns any point of the structure, given its position in the section type and
    its PK in the longitudinal axis
    Parameters:
      ptSectType:   point placed in the section type  (XZ plane)
      longAxisPK:   distance, measured in the longitudinal axis, between
                    the initial cross section and the cross section where the
                    point is placed
         
    '''       
#    fictLin=Part.Line(ptSectType,ptSectType.add(Base.Vector(1,0,0)))
    retVtx=Part.Vertex(ptSectType)
    vInAxis=self.getDirecVectLAxis().multiply(longAxisPK)
    PlaceShpPtVect(shapeId=retVtx,ptOrig=self.ptLAxis,vDirOrig=Base.Vector(0,1,0),ptDest=self.startLAxPoint.add(vInAxis),vDirDest=Base.Vector(self.LAxisVector.x,self.LAxisVector.y,0))
    return Base.Vector(retVtx.X,retVtx.Y,retVtx.Z)

class Wingwall(object):
  '''Generation of a wingwall                                             
                  wallLenght                                             wallTopWidth
         <----------------------------->                                 <----->
         + placementPoint                __wallTopLevel                  ------+ placementPoint
         |  +                                            ______________ /      |\ 
         |     +                                           /\   /\     /       . \
         |        +                                                   /        |  \
         |           +   __1__                           intraSlope  /         .   \ extraSlope
         |              +     | wallSlope                      _↓__ /          |    \_↓__
         |                 +                                   |   /                 \  |          
         |                    +                               1|  /                   \ |1
         |                       +                             | /                     \|
         ^ Z                         +                         |/              ^Z       \
         |                             |                       /               |         \
         |                             |                      /                |          \
         |--------->Y                  |                     /                 |----->X    \
         |_____________________________| __foundLevel   ____/_______________________________\_____ 
         |          |         |________|              ^|                                          |
         |          |_________|            footsHeight||                                          |
         |__________|                                 ↓|__________________________________________|
         <----------><--------><------->               <---------------------->
          footsLength                                      footsIntraWidth
                                                       <----------------------------------------->
                                                                      footsWidth

  
#  placementPoint: point in the global coordinate system where to place the corner of the
#                  wingwall depicted in the figures
#  rotAng:         vector of direction with which to align the local Y axis of the wingwall
  '''
  def __init__(self,wallTopLevel,foundLevel,wallLenght,wallSlope,wallTopWidth,intraSlope,extraSlope):
    self.wallTopLevel=wallTopLevel
    self.foundLevel=foundLevel
    self.wallLenght=wallLenght
    self.wallSlope=wallSlope
    self.wallTopWidth=wallTopWidth
    self.intraSlope=intraSlope
    self.extraSlope=extraSlope
    #keyPoints
    self.placementPoint=Base.Vector(0,0,self.wallTopLevel)  

  def genWingwall(self):
    hStartWall=abs(self.wallTopLevel-self.foundLevel)
    endWallTopLevel=self.wallTopLevel-self.wallLenght*self.wallSlope
    hEndWall=abs(endWallTopLevel-self.foundLevel)
    hEndWall=hStartWall-self.wallLenght*self.wallSlope
    ptTr1TL=Base.Vector(-self.wallTopWidth,0,self.wallTopLevel)
    ptTr1BL=ptTr1TL.add(Base.Vector(-(hStartWall*self.intraSlope),0,-hStartWall))
    ptTr1BR=self.placementPoint.add(Base.Vector(hStartWall*self.extraSlope,0,-hStartWall))
    faceTr1=Part.Face(Part.makePolygon([ptTr1TL,self.placementPoint,ptTr1BR,ptTr1BL,ptTr1TL]))
    ptTr2TL=Base.Vector(-self.wallTopWidth,self.wallLenght,endWallTopLevel)
    ptTr2TR=Base.Vector(0,self.wallLenght,endWallTopLevel)
    ptTr2BL=ptTr2TL.add(Base.Vector(-(hEndWall*self.intraSlope),0,-hEndWall))
    ptTr2BR=ptTr2TR.add(Base.Vector(hEndWall*self.extraSlope,0,-hEndWall))
    faceTr2=Part.Face(Part.makePolygon([ptTr2TL,ptTr2TR,ptTr2BR,ptTr2BL,ptTr2TL]))
    faceTop=Part.Face(Part.makePolygon([ptTr1TL,self.placementPoint,ptTr2TR,ptTr2TL,ptTr1TL]))
    faceBot=Part.Face(Part.makePolygon([ptTr1BL,ptTr1BR,ptTr2BR,ptTr2BL,ptTr1BL]))
    faceIntra=Part.Face(Part.makePolygon([ptTr1TL,ptTr2TL,ptTr2BL,ptTr1BL,ptTr1TL]))
    faceExtra=Part.Face(Part.makePolygon([self.placementPoint,ptTr2TR,ptTr2BR,ptTr1BR,self.placementPoint]))
    retComp=Part.makeCompound([faceTr1,faceTr2,faceTop,faceBot,faceIntra,faceExtra])
    return retComp

  def genWingwallFoundation(self,footsLength,footsHeight,footsWidth,footsIntraWidth):
    retFound=[]
    yOrig=0
    for i in range(0,len(footsLength)):
      xOrig=-footsIntraWidth[i]
      zOrig=self.foundLevel-footsHeight[i]
      ptOrig=Base.Vector(xOrig,yOrig,zOrig)
      foot=Part.makeBox(footsWidth[i],footsLength[i],footsHeight[i],ptOrig)
      retFound.append(foot)
      yOrig+=footsLength[i]
    retComp=Part.makeCompound(retFound)
    return retComp




struct=Underpass(startLAxPoint=[0,0,0],endLAxPoint=[10,10,1],posFrameLAxVect=[0,0,0],vertIntHeigAx=7,intSpan=10.75,wallTh=0.5,deckTh=0.5,deckSlope=0.04)
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

#headwalls heights
initLH=0.5
initRH=0.7
endLH=0.6
endRH=0.3

headwallInit=struct.genHeadWall(leftHeight=initLH,rightHeight=initRH,thickness=0.4,section='I')
Part.show(headwallInit)
headwallEnd=struct.genHeadWall(leftHeight=endLH,rightHeight=endRH,thickness=0.4,section='E')
Part.show(headwallEnd)

#wingwalls
#Initial section, wingwall left
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=7.5,foundLevel=-1,wallLenght=10,wallSlope=1/3.0,wallTopWidth=wTopWidth,intraSlope=1/5.0,extraSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[3,4,3],footsHeight=[2,1,0.5],footsWidth=[6,5,3],footsIntraWidth=[2*6/3,2*5/3,2*3/3])
wingwallInitLeft=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Base.Vector(0,0,initLH))
pt2=struct.kpETR.add(Base.Vector(0,0,initRH))
vDir=(pt2-pt1).normalize().multiply(wTopWidth)
ptSType=pt1
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=0)
WWInitLeft=PlaceShpPtVect(shapeId=wingwallInitLeft,ptOrig=wingWall.placementPoint,vDirOrig=Base.Vector(0,1,0),ptDest=ptStruct,vDirDest=Base.Vector(-1,0,0))
Part.show(WWInitLeft)

#Initial section, wingwall right
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=8,foundLevel=-1,wallLenght=8,wallSlope=1/4.0,wallTopWidth=wTopWidth,intraSlope=1/5.0,extraSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[8],footsHeight=[0.75],footsWidth=[5],footsIntraWidth=[2*5/3])
wingwallInitRight=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Base.Vector(0,0,initLH))
pt2=struct.kpETR.add(Base.Vector(0,0,initRH))
vDir=(pt1-pt2).normalize().multiply(wTopWidth)
ptSType=pt2+vDir
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=0)
WWInitRight=PlaceShpPtVect(shapeId=wingwallInitRight,ptOrig=wingWall.placementPoint,vDirOrig=Base.Vector(0,1,0),ptDest=ptStruct,vDirDest=Base.Vector(-1,-10,0))
Part.show(WWInitRight)

#Final section, wingwall left
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=8,foundLevel=-1,wallLenght=8,wallSlope=1/5.0,wallTopWidth=wTopWidth,intraSlope=1/20.0,extraSlope=1/15.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[4,4],footsHeight=[1,0.5],footsWidth=[5,3],footsIntraWidth=[2*5/3,2*3/3])
wingwallEndLeft=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Base.Vector(0,0,endLH))
pt2=struct.kpETR.add(Base.Vector(0,0,endRH))
vDir=(pt2-pt1).normalize().multiply(wTopWidth)
ptSType=pt1+vDir
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=struct.LAxisVector.Length)
WWEndLeft=PlaceShpPtVect(shapeId=wingwallEndLeft,ptOrig=wingWall.placementPoint,vDirOrig=Base.Vector(0,1,0),ptDest=ptStruct,vDirDest=Base.Vector(1,10,0))
Part.show(WWEndLeft)

#Final section, wingwall right
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=7.5,foundLevel=-1,wallLenght=12,wallSlope=1/3.0,wallTopWidth=wTopWidth,intraSlope=1/5.0,extraSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[6,6],footsHeight=[1.5,0.75],footsWidth=[6,5],footsIntraWidth=[2*6/3,2*5/3])
wingwallEndRight=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Base.Vector(0,0,initLH))
pt2=struct.kpETR.add(Base.Vector(0,0,initRH))
vDir=(pt1-pt2).normalize().multiply(wTopWidth)
ptSType=pt2
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=struct.LAxisVector.Length)
WWEndRight=PlaceShpPtVect(shapeId=wingwallEndRight,ptOrig=wingWall.placementPoint,vDirOrig=Base.Vector(0,1,0),ptDest=ptStruct,vDirDest=Base.Vector(10,1,0))
Part.show(WWEndRight)
