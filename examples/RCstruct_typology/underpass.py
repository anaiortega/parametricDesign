# -*- coding: utf-8 -*-

# Example of underpass modelized with FreeCAD
from parametric_design.freeCAD_civil.structures import underpass
import Part
from FreeCAD import Vector

struct=underpass.Underpass(startLAxPoint=[0,0,0],endLAxPoint=[10,10,1],posFrameLAxVect=[0,0,0],vertIntHeigAx=7,intSpan=10.75,wallTh=0.5,deckTh=0.5,deckSlope=0.04)
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
wingWall=underpass.Wingwall(wallTopLevel=7.5,foundLevel=-1,wallLenght=10,wallSlope=1/3.0,wallTopWidth=wTopWidth,backFaceSlope=1/5.0,frontFaceSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[3,4,3],footsHeight=[2,1,0.5],footsWidth=[6,5,3],footsToeWidth=[2*6/3,2*5/3,2*3/3])
wingwallInitLeft=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Vector(0,0,initLH))
pt2=struct.kpETR.add(Vector(0,0,initRH))
vDir=(pt2-pt1).normalize().multiply(wTopWidth)
ptSType=pt1
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=0)
WWInitLeft=underpass.PlaceShpPtVect(shapeId=wingwallInitLeft,ptOrig=wingWall.placementPoint,vDirOrig=Vector(0,1,0),ptDest=ptStruct,vDirDest=Vector(-1,0,0))
Part.show(WWInitLeft)

#Initial section, wingwall right
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=8,foundLevel=-1,wallLenght=8,wallSlope=1/4.0,wallTopWidth=wTopWidth,backFaceSlope=1/5.0,frontFaceSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[8],footsHeight=[0.75],footsWidth=[5],footsToeWidth=[2*5/3])
wingwallInitRight=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Vector(0,0,initLH))
pt2=struct.kpETR.add(Vector(0,0,initRH))
vDir=(pt1-pt2).normalize().multiply(wTopWidth)
ptSType=pt2+vDir
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=0)
WWInitRight=PlaceShpPtVect(shapeId=wingwallInitRight,ptOrig=wingWall.placementPoint,vDirOrig=Vector(0,1,0),ptDest=ptStruct,vDirDest=Vector(-1,-10,0))
Part.show(WWInitRight)

#Final section, wingwall left
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=8,foundLevel=-1,wallLenght=8,wallSlope=1/5.0,wallTopWidth=wTopWidth,backFaceSlope=1/20.0,frontFaceSlope=1/15.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[4,4],footsHeight=[1,0.5],footsWidth=[5,3],footsToeWidth=[2*5/3,2*3/3])
wingwallEndLeft=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Vector(0,0,endLH))
pt2=struct.kpETR.add(Vector(0,0,endRH))
vDir=(pt2-pt1).normalize().multiply(wTopWidth)
ptSType=pt1+vDir
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=struct.LAxisVector.Length)
WWEndLeft=underpass.PlaceShpPtVect(shapeId=wingwallEndLeft,ptOrig=wingWall.placementPoint,vDirOrig=Vector(0,1,0),ptDest=ptStruct,vDirDest=Vector(1,10,0))
Part.show(WWEndLeft)

#Final section, wingwall right
wTopWidth=0.5
wingWall=Wingwall(wallTopLevel=7.5,foundLevel=-1,wallLenght=12,wallSlope=1/3.0,wallTopWidth=wTopWidth,backFaceSlope=1/5.0,frontFaceSlope=1/10.0)
ww=wingWall.genWingwall()
wfoundt=wingWall.genWingwallFoundation(footsLength=[6,6],footsHeight=[1.5,0.75],footsWidth=[6,5],footsToeWidth=[2*6/3,2*5/3])
wingwallEndRight=Part.makeCompound([ww,wfoundt])
pt1=struct.kpETL.add(Vector(0,0,initLH))
pt2=struct.kpETR.add(Vector(0,0,initRH))
vDir=(pt1-pt2).normalize().multiply(wTopWidth)
ptSType=pt2
ptStruct=struct.getPtStrPKAxis(ptSectType=ptSType,longAxisPK=struct.LAxisVector.Length)
WWEndRight=underpass.PlaceShpPtVect(shapeId=wingwallEndRight,ptOrig=wingWall.placementPoint,vDirOrig=Vector(0,1,0),ptDest=ptStruct,vDirDest=Vector(10,1,0))
Part.show(WWEndRight)
