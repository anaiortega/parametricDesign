# -*- coding: utf-8 -*-
'''
__author__= "Ana Ortega (AOO) and Luis C. Pérez Tato (LCPT)"
__cppyright__= "Copyright 2015, AOO and LCPT"
__license__= "GPL"
__version__= "1.0"
__email__= "l.pereztato@gmail.com  ana.Ortega.Ort@gmail.com"
'''
import math
import FreeCAD, Part, Draft
from FreeCAD import Vector

def PlaceShpPtVect(shapeId,ptOrig,vDirOrig,ptDest,vDirDest):
    '''Translates the shape from point ptOrig to point ptDest and
    rotates it in such a way that the direction defined with the vector
    vDirOrig turn into the vDirDest direction
    '''
    shapeId.translate(ptDest-ptOrig)
    vPerp=vDirOrig.cross(vDirDest)
    angRot=vDirOrig.getAngle(vDirDest)
    if angRot != 0:
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

    def __init__(self,startLAxPoint,endLAxPoint,posFrameLAxVect,vertIntHeigAx,intSpan,wallTh,deckTh,deckSlope,skewAngle=0):
        self.startLAxPoint=Vector(startLAxPoint[0],startLAxPoint[1],startLAxPoint[2])
        self.endLAxPoint=Vector(endLAxPoint[0],endLAxPoint[1],endLAxPoint[2])
        self.ptLAxis=Vector(posFrameLAxVect[0],0,posFrameLAxVect[2])
        self.vertIntHeigAx=vertIntHeigAx
        self.intSpan=intSpan
        self.wallTh=wallTh
        self.deckTh=deckTh
        self.deckSlope=deckSlope
        self.skewAngle=skewAngle
        self.LAxisVector=self.endLAxPoint-self.startLAxPoint     #vector used for extrusions
        self.rotAngl=(-180/math.pi)*((self.endLAxPoint-self.startLAxPoint).projectToPlane(Vector(0,0,0),Vector(0,0,1))).getAngle(Vector(0,1,0))  #rotation angle
        self.initSectPoints()

    def initSectPoints(self):
        ''' initialize the main points of the transversal section
        '''
        deckThVert=self.deckTh*(1+self.deckSlope**2)**(1/2)
        skewAngleRad=math.radians(self.skewAngle)
        skewUnitVector=Vector(math.cos(skewAngleRad),math.sin(skewAngleRad),0)
        intSpanSkew=self.intSpan/math.cos(skewAngleRad)
        extSpanSkew=(self.intSpan+2*self.wallTh)/math.cos(skewAngleRad)
        hIntL=self.vertIntHeigAx-self.deckSlope*intSpanSkew/2
        hExtL=self.vertIntHeigAx-self.deckSlope*extSpanSkew/2+deckThVert
        hIntR=self.vertIntHeigAx+self.deckSlope*intSpanSkew/2
        hExtR=self.vertIntHeigAx+self.deckSlope*extSpanSkew/2+deckThVert
        zUnitVector=Vector(0,0,1)
        #keypoints: 
        self.kpIBL=-(intSpanSkew/2)*skewUnitVector    #internal bottom left
        self.kpIBR=(intSpanSkew/2)*skewUnitVector     #internal bottom right
        self.kpEBL=-(extSpanSkew/2)*skewUnitVector  #external bottom left
        self.kpEBR=(extSpanSkew/2)*skewUnitVector   #external bottom right
        self.kpITL=self.kpIBL.add(hIntL*zUnitVector)  #internal top left
        self.kpITR= self.kpIBR.add(hIntR*zUnitVector)   #internal top right
        self.kpETL=self.kpEBL.add(hExtL*zUnitVector)  #external top left
        self.kpETR=self.kpEBR.add(hExtR*zUnitVector)   #external top right
        self.ptDeckBL=self.kpETL.add(-deckThVert*zUnitVector)
        self.ptDeckBR=self.kpETR.add(-deckThVert*zUnitVector)

    def getDirecVectLAxis(self):
        '''returns the director vector of the longitudinal axis'''
        vDirec=(self.endLAxPoint-self.startLAxPoint).normalize()
        return vDirec

    def placeAndExtrudeShape(self,shName):
        '''place the shape in the initial position of the longitudinal axis
        and extrudes it until the end point
        '''
        PlaceShpPtVect(shapeId=shName,ptOrig=self.ptLAxis,vDirOrig=Vector(0,1,0),ptDest=self.startLAxPoint,vDirDest=Vector(self.LAxisVector.x,self.LAxisVector.y,0))
        retSh=shName.extrude(self.LAxisVector)
        return retSh

    def genDeck(self):
        linDeck=Part.makePolygon([self.kpITL,self.ptDeckBL,self.kpETL,self.kpETR,self.ptDeckBR,self.kpITR,self.kpITL])
        deck=Part.Face(linDeck)
        retComp=Part.makeCompound([deck])
        return self.placeAndExtrudeShape(retComp)

    def genLeftWall(self):
        ''' Return the compound with the left wall '''
        linLeftWall=Part.makePolygon([self.kpIBL,self.kpEBL,selfptDeckBL,self.kpITL,self.kpIBL])
        leftWall=Part.Face(linLeftWall)
        retComp=Part.makeCompound([

    def genDeckAndWalls(self):
        '''Returns a compound with the deck and walls of the structure'''
        #Deck

        linDeck=Part.makePolygon([self.kpITL,self.ptDeckBL,self.kpETL,self.kpETR,self.ptDeckBR,self.kpITR,self.kpITL])
        deck=Part.Face(linDeck)
        #Walls
        linLeftWall=Part.makePolygon([self.kpIBL,self.kpEBL,selfptDeckBL,self.kpITL,self.kpIBL])
        leftWall=Part.Face(linLeftWall)
        linRightWall=Part.makePolygon([self.kpEBR,self.kpIBR,self.kpITR,self.ptDeckBR,self.kpEBR])
        rightWall=Part.Face(linRightWall)
        retComp=Part.makeCompound([deck,leftWall,rightWall])
        return self.placeAndExtrudeShape(retComp)

    def genSlabFound(self,baseSlabTh,slabWdtUnderFilling):
        '''Returns a compound with the slab foundation (constant thickness)
        Parameters:
          baseSlabTh:          thickness of the base slab
          slabtWdtUnderFilling:with of slab under the filling  
        '''
        ptSlabTL=self.kpEBL.add(Vector(-slabWdtUnderFilling,0,0))
        ptSlabBL=ptSlabTL.add(Vector(0,0,-baseSlabTh))
        ptSlabTR=self.kpEBR.add(Vector(slabWdtUnderFilling,0,0))
        ptSlabBR=ptSlabTR.add(Vector(0,0,-baseSlabTh))
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
        self.kpIBL=Vector(-self.intSpan/2,0)
        self.kpEBL=self.kpIBL.add(Vector(-self.wallTh,0,0))
        ptFootTL=self.kpEBL.add(Vector(-footWdtUnderFilling,0,0))
        ptFootBL=ptFootTL.add(Vector(0,0,-footingTh))
        ptFootBL2=ptFootBL.add(Vector(footingWdt,0,0))
        ptFootBL3=ptFootBL2.add(Vector(1/footSlope*(footingTh-baseSlabTh),0,footingTh-baseSlabTh))
        ptFootBR3=Vector(-ptFootBL3.x,0,ptFootBL3.z)
        ptFootBR2=Vector(-ptFootBL2.x,0,ptFootBL2.z)
        ptFootBR=Vector(-ptFootBL.x,0,ptFootBL.z)
        ptFootTR=Vector(-ptFootTL.x,0,ptFootTL.z)
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
        ptDeckBL=self.kpITL.add(Vector(-self.wallTh,0,-self.deckSlope*self.wallTh*self.wallTh))
        ptLSup1=ptDeckBL.add(Vector(-apSlabSuppWdt,0,0))
        ptLSup2=ptLSup1.add(Vector(0,0,-apSlabSuppTh))
        ptLSup3=ptLSup2.add(Vector(apSlabSuppWdt,0,0))
        linLeftSup=Part.makePolygon([ptDeckBL,ptLSup1,ptLSup2,ptLSup3,ptDeckBL])
        leftSup=Part.Face(linLeftSup)
        ptDeckBR=self.kpITR.add(Vector(self.wallTh,0,self.deckSlope*self.wallTh*self.wallTh))
        ptRSup1=ptDeckBR.add(Vector(apSlabSuppWdt,0,0))
        ptRSup2=ptRSup1.add(Vector(0,0,-apSlabSuppTh))
        ptRSup3=ptRSup2.add(Vector(-apSlabSuppWdt,0,0))
        linRightSup=Part.makePolygon([ptDeckBR,ptRSup1,ptRSup2,ptRSup3,ptDeckBR])
        rightSup=Part.Face(linRightSup)
        #Approach slabs
        ptLApSlab1=ptLSup1.add(Vector(-apSlabWdt,0,-apSlabSlp*apSlabWdt))
        apslabThVert=apSlabTh*(1+apSlabSlp**2)**(1/2)
        ptLApSlab2=ptLApSlab1.add(Vector(0,0,apslabThVert))
        ptLApSlab3=ptDeckBL.add(Vector(0,0,apslabThVert))
        linLeftApSlab=Part.makePolygon([ptDeckBL,ptLApSlab1,ptLApSlab2,ptLApSlab3,ptDeckBL])
        leftApSlab=Part.Face(linLeftApSlab)
        ptRApSlab1=ptDeckBR.add(Vector(apSlabWdt,0,-apSlabSlp*apSlabWdt))
        ptRApSlab2=ptRApSlab1.add(Vector(0,0,apslabThVert))
        ptRApSlab3=ptDeckBR.add(Vector(0,0,apslabThVert))
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
        ptWallTL=self.kpETL.add(Vector(0,0,leftHeight))
        ptWallTR=self.kpETR.add(Vector(0,0,rightHeight))
        linWall=Part.makePolygon([self.kpETL,self.kpETR,ptWallTR,ptWallTL,self.kpETL])
        headwall=Part.Face(linWall)
        vectExtr=(self.endLAxPoint-self.startLAxPoint)
        if section =='I':
            ptDestination=self.startLAxPoint
          vectExtr.normalize().multiply(thickness)
        else:
            ptDestination=self.endLAxPoint
            vectExtr.normalize().multiply(-thickness)
        PlaceShpPtVect(shapeId=headwall,ptOrig=self.ptLAxis,vDirOrig=Vector(0,1,0),ptDest=ptDestination,vDirDest=Vector(self.LAxisVector.x,self.LAxisVector.y,0))
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
    #    fictLin=Part.Line(ptSectType,ptSectType.add(Vector(1,0,0)))
        retVtx=Part.Vertex(ptSectType)
        vInAxis=self.getDirecVectLAxis().multiply(longAxisPK)
        PlaceShpPtVect(shapeId=retVtx,ptOrig=self.ptLAxis,vDirOrig=Vector(0,1,0),ptDest=self.startLAxPoint.add(vInAxis),vDirDest=Vector(self.LAxisVector.x,self.LAxisVector.y,0))
        return Vector(retVtx.X,retVtx.Y,retVtx.Z)

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
        self.placementPoint=Vector(0,0,self.wallTopLevel)  

    def genWingwall(self):
        hStartWall=abs(self.wallTopLevel-self.foundLevel)
        endWallTopLevel=self.wallTopLevel-self.wallLenght*self.wallSlope
        hEndWall=abs(endWallTopLevel-self.foundLevel)
        hEndWall=hStartWall-self.wallLenght*self.wallSlope
        ptTr1TL=Vector(-self.wallTopWidth,0,self.wallTopLevel)
        ptTr1BL=ptTr1TL.add(Vector(-(hStartWall*self.intraSlope),0,-hStartWall))
        ptTr1BR=self.placementPoint.add(Vector(hStartWall*self.extraSlope,0,-hStartWall))
        faceTr1=Part.Face(Part.makePolygon([ptTr1TL,self.placementPoint,ptTr1BR,ptTr1BL,ptTr1TL]))
        ptTr2TL=Vector(-self.wallTopWidth,self.wallLenght,endWallTopLevel)
        ptTr2TR=Vector(0,self.wallLenght,endWallTopLevel)
        ptTr2BL=ptTr2TL.add(Vector(-(hEndWall*self.intraSlope),0,-hEndWall))
        ptTr2BR=ptTr2TR.add(Vector(hEndWall*self.extraSlope,0,-hEndWall))
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
            ptOrig=Vector(xOrig,yOrig,zOrig)
            foot=Part.makeBox(footsWidth[i],footsLength[i],footsHeight[i],ptOrig)
            retFound.append(foot)
            yOrig+=footsLength[i]
        retComp=Part.makeCompound(retFound)
        return retComp

