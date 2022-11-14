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
      startLAxPoint: Vector(x,y,z) coordinates of the starting point in the 
                     longitudinal axis where the structure begins
      endLAxPoint:   Vector(x,y,z) coordinates of the ending point in the
                     longitudinal axis where the structure ends
      vertIntHeigAx:  vertical internal height in the central axis of the frame
      intSpan:        distance between internal faces of the walls
      baseSlabTh:     thickness of the base slab
      wallTh:         thickness of the walls
      deckTh:         deck thickness
      deckTrSlope:    deck transversal slope (Z/X) (if skewed, the slope is defined
                      parallel to the skew 
      posFrameLAxVect: position [x,0,z] of the longitudinal axis in the
                       section type
      deltaHRightWall: increase (or decrease if negative) in height of the rigtht wall
                       relative to the height of the left wall.

       kpETL  ________________________________________ kpETR
             |                     ^deckTh            |
             |    _________________↓______________    |
             |   |   deckTrSlope=Z/X ^         kpITR|   |
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

    def __init__(self,startLAxPoint,endLAxPoint,posFrameLAxVect,vertIntHeigAx,intSpan,wallTh,deckTh,deckTrSlope,skewAngle=0,deltaHRightWall=None):
        self.startLAxPoint=startLAxPoint
        self.endLAxPoint=endLAxPoint
        self.ptLAxis=Vector(posFrameLAxVect[0],0,posFrameLAxVect[2])
        self.vertIntHeigAx=vertIntHeigAx
        self.intSpan=intSpan
        self.wallTh=wallTh
        self.deckTh=deckTh
        self.deckTrSlope=deckTrSlope
        self.skewAngle=skewAngle
        self.LAxisVector=self.endLAxPoint-self.startLAxPoint     #vector used for extrusions
        self.rotAngl=(-180/math.pi)*((self.endLAxPoint-self.startLAxPoint).projectToPlane(Vector(0,0,0),Vector(0,0,1))).getAngle(Vector(0,1,0))  #rotation angle
        self.deltaHRightWall=deltaHRightWall
        self.initSectPoints()

    def initSectPoints(self):
        ''' initialize the main points of the transversal section
        '''
        deckThVert=self.getDeckVertTh()
        skewAngleRad=math.radians(self.skewAngle)
        skewUnitVector=Vector(math.cos(skewAngleRad),math.sin(skewAngleRad),0)
        intSpanSkew=self.intSpan/math.cos(skewAngleRad)
        extSpanSkew=(self.intSpan+2*self.wallTh)/math.cos(skewAngleRad)
        hIntL=self.vertIntHeigAx-self.deckTrSlope*intSpanSkew/2
        hExtL=self.vertIntHeigAx-self.deckTrSlope*extSpanSkew/2+deckThVert
        hIntR=self.vertIntHeigAx+self.deckTrSlope*intSpanSkew/2
        hExtR=self.vertIntHeigAx+self.deckTrSlope*extSpanSkew/2+deckThVert
        zUnitVector=Vector(0,0,1)
        Lslope= self.LAxisVector.z/self.LAxisVector.Length #longitudinal slope
        intVectorIncrZskew=Vector(0,0,intSpanSkew/2*math.sin(skewAngleRad)*Lslope)
        extVectorIncrZskew=Vector(0,0,extSpanSkew/2*math.sin(skewAngleRad)*Lslope)
        #keypoints:
        self.kpIBL=-(intSpanSkew/2)*skewUnitVector-intVectorIncrZskew    #internal bottom left
        self.kpIBR=(intSpanSkew/2)*skewUnitVector+intVectorIncrZskew     #internal bottom right
        if self.deltaHRightWall:
            self.kpIBR=self.kpIBR+self.deltaHRightWall*Vector(0,0,-1)
        self.kpEBL=-(extSpanSkew/2)*skewUnitVector-extVectorIncrZskew  #external bottom left
        self.kpEBR=(extSpanSkew/2)*skewUnitVector+extVectorIncrZskew   #external bottom right
        if self.deltaHRightWall:
            self.kpEBR=self.kpEBR+self.deltaHRightWall*Vector(0,0,-1)
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

    def getVectFrontalView(self):
        v=self.getDirecVectLAxis()
        return Vector(-v.x,-v.y,0)

    def getVectDorsalView(self):
        v=self.getDirecVectLAxis()
        return Vector(v.x,v.y,0)

    def getVectRightView(self):
        v=self.getDirecVectLAxis()
        return Vector(v.y,-v.x,0)

    def getVectLeftView(self):
        v=self.getDirecVectLAxis()
        return Vector(-v.y,v.x,0)
     
    def placeAndExtrudeShape(self,shName):
        '''place the shape in the initial position of the longitudinal axis
        and extrudes it until the end point
        '''
        PlaceShpPtVect(shapeId=shName,ptOrig=self.ptLAxis,vDirOrig=Vector(0,1,0),ptDest=self.startLAxPoint,vDirDest=Vector(self.LAxisVector.x,self.LAxisVector.y,0))
        retSh=shName.extrude(self.LAxisVector)
        return retSh

    def getDeckVertTh(self):
        '''Return the thickness of the deck measured vertically
        '''
        deckVertTh=self.deckTh*(1+self.deckTrSlope**2)**(1/2)
        return deckVertTh

    def getSkewWallTh(self):
        '''Return the thichness of the wall in skewed direction
        '''
        skewAngleRad=math.radians(self.skewAngle)
        skewWallTh=self.wallTh/math.cos(skewAngleRad)
        return skewWallTh
        
    def genDeck(self):
        '''return the deck as a part-compound and a list of staking points.
        The staking points are four vertexes of the top of the deck counterclockwise 
        [LE,LS,RS,RE], meaning: L-R left-right, S-E start-end of the box (direction
        according to startLAxPoint -> endLAxPoint)
        
        '''
        linDeck=Part.makePolygon([self.kpETL,self.kpETR,self.ptDeckBR,self.ptDeckBL])
        deck=Part.Face(linDeck)
        retComp=Part.makeCompound([deck])
        retComp=self.placeAndExtrudeShape(retComp)
        stakingPoints=[retComp.Vertexes[1].Point,retComp.Vertexes[0].Point,retComp.Vertexes[2].Point,retComp.Vertexes[3].Point] #see sketch for staking-point's position
        return retComp,stakingPoints

    def genLeftWall(self):
        ''' Return the compound with the left wall '''
        linLeftWall=Part.makePolygon([self.ptDeckBL,self.kpITL,self.kpIBL,self.kpEBL,self.ptDeckBL])
        leftWall=Part.Face(linLeftWall)
        retComp=Part.makeCompound([leftWall])
        return self.placeAndExtrudeShape(retComp)

    def genRightWall(self):
        ''' Return the compound with the right wall '''
        linRightWall=Part.makePolygon([self.kpITR,self.ptDeckBR,self.kpEBR,self.kpIBR,self.kpITR])
        rightWall=Part.Face(linRightWall)
        retComp=Part.makeCompound([rightWall])
        return self.placeAndExtrudeShape(retComp)

    def genDeckAndWalls(self):
        '''Returns a compound with the deck and walls of the structure'''
        #Deck
        deck=self.genDeck()
        #Walls
        leftWall=self.genLeftWall()
        rightWall=self.genRightWall()
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
        ptDeckBL=self.kpITL.add(Vector(-self.wallTh,0,-self.deckTrSlope*self.wallTh*self.wallTh))
        ptLSup1=ptDeckBL.add(Vector(-apSlabSuppWdt,0,0))
        ptLSup2=ptLSup1.add(Vector(0,0,-apSlabSuppTh))
        ptLSup3=ptLSup2.add(Vector(apSlabSuppWdt,0,0))
        linLeftSup=Part.makePolygon([ptDeckBL,ptLSup1,ptLSup2,ptLSup3,ptDeckBL])
        leftSup=Part.Face(linLeftSup)
        ptDeckBR=self.kpITR.add(Vector(self.wallTh,0,self.deckTrSlope*self.wallTh*self.wallTh))
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
        Return the headwall and two points (left and right) to place
        the wing-walls (top external face of the wing-wall)
  
        :param leftHeight:  heigth of the headwall in the left side of the deck
        :param rightHeight: heigth of the headwall in the right side of the deck
        :param thickness:   thickness of the headwall (longitudinal direction)
        :param section:     ='I' generates de headwall in the initial section of the structure
                            ='E' idem for ending section
        '''
        ptWallTL=self.kpETL.add(Vector(0,0,leftHeight))
        ptWallTR=self.kpETR.add(Vector(0,0,rightHeight))
        linWall=Part.makePolygon([ptWallTL,ptWallTR,self.kpETR,self.kpETL,ptWallTL])
        headwall=Part.Face(linWall)
        vectExtr=(self.endLAxPoint-self.startLAxPoint) #extrusion vector
        if section =='I':
            ptDestination=self.startLAxPoint
            vectExtr.normalize().multiply(thickness)
        else:
            ptDestination=self.endLAxPoint
            vectExtr.normalize().multiply(-thickness)
        PlaceShpPtVect(shapeId=headwall,ptOrig=self.ptLAxis,vDirOrig=Vector(0,1,0),ptDest=ptDestination,vDirDest=Vector(self.LAxisVector.x,self.LAxisVector.y,0))
        retSh=headwall.extrude(vectExtr)
        # staking points
        stackPt=[retSh.Vertexes[0].Point,retSh.Vertexes[2].Point]
        return retSh,stackPt

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

    def genArrayPiles(self,fiPile,lengthPile,distPiles,nPiles,refPoint,distFirstPile2refPoint):
        vDirArray=self.LAxisVector.normalize()
        vExtrPile=Vector(0,0,-lengthPile)
        stackPoints=list()
        piles=list()
        for i in range(nPiles):
            centCircle=refPoint+(distFirstPile2refPoint+i*distPiles)*vDirArray
            stackPoints+=[centCircle]
            c=Part.Circle(Center=centCircle,Normal=Vector(0,0,1),Radius=fiPile/2)
            c=c.toShape()
            pile=c.extrude(vExtrPile)
            piles+=[pile]
        piles=Part.makeCompound(piles)
        return piles,stackPoints
        
        

class Wingwall(object):
    '''Generation of a wingwall                                             
                    wallLenght                                             wallTopWidth
           <----------------------------->                                 <----->
           + placementPoint                __wallTopLevel                  ------+ placementPoint
           |  +                                            ______________ /      |\ 
           |     +                                           /\   /\     /       . \
           |        +                                                   /        |  \
           |           +   __1__                        backFaceSlope  /         .   \ frontFaceSlope
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
           <----------><--------><------->                                       <----------------->
            footsLength                                                           footsToeWidth
                                                         <----------------------------------------->
                                                                        footsWidth


    #  placementPoint: point in the global coordinate system where to place the corner of the
    #                  wingwall depicted in the figures
    #  rotAng:         vector of direction with which to align the local Y axis of the wingwall
    '''
    def __init__(self,placementPoint,foundLevel,wallLenght,wallSlope,wallTopWidth,backFaceSlope,frontFaceSlope,vDirTr,vDirLn,dispLn=None):
        '''
        :param placementPoint: point in the global coordinate system where to place the corner of the
                               wingwall (top corner in the intrados facing )
        :param foundLevel: z_global coordinate of the top face of the foundation
        :param wallLenght: length of the wall (longitudinal direction)
        :param wallSlope: slope of the top face of the wall in longitudinal direction
        :param wallTopWidth: width of the top face of the wall (transversal)
        :param backFaceSlope: slope of the intrados (back face) H/V (positive)
        :param frontFaceSlope: slope of the extrados (front face) H/V (positive)
        :param vDirTr: vector in transversal direction (from front to back faces of the wall)
        :param vDirLn: vector in longitudinal direction (from placementPoint to the end of the wall)
        :param dispLn: displacement in longitudinal direction (defaults to None)
        '''
        self.placementPoint=placementPoint
        self.foundLevel=foundLevel
        self.wallLenght=wallLenght
        self.wallSlope=wallSlope
        self.wallTopWidth=wallTopWidth
        self.backFaceSlope=backFaceSlope
        self.frontFaceSlope=frontFaceSlope
        self.vDirTr=vDirTr.normalize()
        self.vDirLn=vDirLn.normalize()
        self.dispLn=dispLn

    def genWingwall(self):
        hStartWall=self.placementPoint.z-self.foundLevel
        hEndWall=hStartWall-self.wallLenght*self.wallSlope
        ptTr1TL=self.placementPoint+self.wallTopWidth*self.vDirTr
        ptTr1BL=ptTr1TL.add(hStartWall*self.backFaceSlope*self.vDirTr).add(Vector(0,0,-hStartWall))
        baseSect1=self.wallTopWidth+hStartWall*self.backFaceSlope+hStartWall*self.frontFaceSlope
        ptTr1BR=ptTr1BL.add(-baseSect1*self.vDirTr)
        faceTr1=Part.Face(Part.makePolygon([ptTr1TL,self.placementPoint,ptTr1BR,ptTr1BL,ptTr1TL]))
        vDeltaZ=self.wallLenght*self.wallSlope*Vector(0,0,-1)
        ptTr2TL=ptTr1TL.add(self.wallLenght*self.vDirLn).add(vDeltaZ)
        ptTr2TR=self.placementPoint.add(self.wallLenght*self.vDirLn).add(vDeltaZ)
        ptTr2BL=ptTr2TL.add(hEndWall*self.backFaceSlope*self.vDirTr).add(Vector(0,0,-hEndWall))
        baseSect2=self.wallTopWidth+hEndWall*self.backFaceSlope+hEndWall*self.frontFaceSlope
        ptTr2BR=ptTr2BL.add(-baseSect2*self.vDirTr)
        faceTr2=Part.Face(Part.makePolygon([ptTr2TL,ptTr2TR,ptTr2BR,ptTr2BL,ptTr2TL]))
        faceTop=Part.Face(Part.makePolygon([ptTr1TL,self.placementPoint,ptTr2TR,ptTr2TL,ptTr1TL]))
        faceBot=Part.Face(Part.makePolygon([ptTr1BL,ptTr1BR,ptTr2BR,ptTr2BL,ptTr1BL]))
        faceBack=Part.Face(Part.makePolygon([ptTr1TL,ptTr2TL,ptTr2BL,ptTr1BL,ptTr1TL]))
        faceFront=Part.Face(Part.makePolygon([self.placementPoint,ptTr2TR,ptTr2BR,ptTr1BR,self.placementPoint]))
        retComp=Part.makeCompound([faceTr1,faceTr2,faceTop,faceBot,faceBack,faceFront])
        stackPts=[self.placementPoint,ptTr2TR] # external face, [point Hmax, point Hmin]
        if self.dispLn:
            vTrans=self.dispLn*self.vDirLn
            retComp.translate(vTrans)
            stackPts=[stackPts[0]+vTrans,stackPts[1]+vTrans]
        return retComp,stackPts

    def genWingwallFoundation(self,footsLength,footsHeight,footsWidth,footsToeWidth):
        ''' Return the footings of a wingwal
 
        :param footsLength: ordered list of foot lengths (longitudinal direction of the wall)
        :param footsHeight: ordered list of foot heights
        :param footsWidth: ordered list of foot widths (transversal direction)
        :param footsToeWidth: ordered list of foot toe lengths (measured from de vertical of 
                             the placementPoint)
        '''
        foots=list()
        stackPts=list()
        vDirTB=Vector(0,0,-1) # vector direction top-bottom
        keyPnt=Vector(self.placementPoint.x,self.placementPoint.y,self.foundLevel)
        for i in range(0,len(footsLength)):
            L=footsLength[i]; H=footsHeight[i]; WF=footsToeWidth[i]; WK=footsWidth[i]-footsToeWidth[i]
            ptoTK=keyPnt.add(WK*self.vDirTr) # top back
            ptoTF=keyPnt.add(-WF*self.vDirTr) # top front
            ptoBK=ptoTK.add(H*vDirTB) # bottom back
            ptoBF=ptoTF.add(H*vDirTB) # bottom front
            faceTr=Part.Face(Part.makePolygon([ptoTK,ptoTF,ptoBF,ptoBK,ptoTK]))
            foot=faceTr.extrude(L*self.vDirLn)
            if self.dispLn:
                foot.translate(self.dispLn*self.vDirLn)
            foots+=[foot]
            vtxs=foot.Vertexes
            stackPts.append([vtxs[0].Point,vtxs[1].Point,vtxs[3].Point,vtxs[2].Point])
            keyPnt=keyPnt.add(L*self.vDirLn)
        retComp=Part.makeCompound(foots)
        return retComp,stackPts

