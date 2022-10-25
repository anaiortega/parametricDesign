from freeCAD_civil.structures import underpass
import Part
from FreeCAD import Vector
vZpos=Vector(0,0,1)
vZneg=Vector(0,0,-1)


doc=App.newDocument("prueba")
struct=underpass.Underpass(startLAxPoint=Vector(0,0,0),endLAxPoint=Vector(1,15,1),posFrameLAxVect=[0,0,7.5],vertIntHeigAx=7,intSpan=6,wallTh=0.85,deckTh=0.85,deckTrSlope=0,skewAngle=30)
deck,deck_stakingPt=struct.genDeck()
Part.show(deck,'deck')

# for v in deck_stakingPt:
#     print(round(v.X,1),round(v.Y,1),round(v.Z,1))

leftWall=struct.genLeftWall()
Part.show(leftWall,'leftWall')

rightWall=struct.genRightWall()
Part.show(rightWall,'rightWall')

v1=leftWall.Vertexes[6]
v2=leftWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
pilesLeft,stakPpilesLeft=struct.genArrayPiles(
    fiPile=0.25,
    lengthPile=6,
    distPiles=0.75,
    nPiles=20,
    refPoint=refPoint,
    distFirstPile2refPoint=0.5)
Part.show(pilesLeft,'pilesLeft')

v1=rightWall.Vertexes[6]
v2=rightWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
pilesRight,stakPpilesRight=struct.genArrayPiles(
    fiPile=0.25,
    lengthPile=6,
    distPiles=0.75,
    nPiles=20,
    refPoint=refPoint,
    distFirstPile2refPoint=0.5)
Part.show(pilesRight,'pilesRight')


initHeadWall,stackPinitHeadWall=struct.genHeadWall(leftHeight=0.5,rightHeight=0.5,thickness=0.5,section='I')
Part.show(initHeadWall,'initHeadWall')

endHeadWall,stackPendHeadWall=struct.genHeadWall(leftHeight=0.5,rightHeight=0.5,thickness=0.5,section='E')
Part.show(endHeadWall,'endHeadWall')

# Aletas
## aleta izquierda sección inicial
vDir=(stackPinitHeadWall[1]-stackPinitHeadWall[0]).normalize()
ptILwingwall=stackPinitHeadWall[0]+struct.getSkewWallTh()*vDir
vDirLn=Vector(-1,-1,0); vDirTr=vDirLn.cross(vZpos)
vDirLn=Vector(0,-1,0);vDirTr=vDirLn.cross(vZpos)
wingWallIL=underpass.Wingwall(placementPoint=ptILwingwall,foundLevel=-6.5,wallLenght=10,wallSlope=1/5.0,wallTopWidth=0.3,backFaceSlope=1/15.0,frontFaceSlope=0,vDirTr=vDirTr,vDirLn=vDirLn)
wwIL=wingWallIL.genWingwall()
footIL,stackPntFootIL=wingWallIL.genWingwallFoundation(footsLength=[5,5],footsHeight=[1.2,1.0],footsWidth=[7,5],footsToeWidth=[2,1.5])
Part.show(wwIL,'wwIL')
Part.show(footIL,'footIL')

## aleta derecha sección inicial
vDir=(stackPinitHeadWall[1]-stackPinitHeadWall[0]).normalize()
ptIRwingwall=stackPinitHeadWall[1]-struct.getSkewWallTh()*vDir
vDirLn=Vector(0.3,-1,0); vDirTr=vDirLn.cross(vZneg)
wingWallIR=underpass.Wingwall(placementPoint=ptIRwingwall,foundLevel=-7,wallLenght=5,wallSlope=1/10,wallTopWidth=0.25,backFaceSlope=1/15,frontFaceSlope=0,vDirTr=vDirTr,vDirLn=vDirLn)
wwIR=wingWallIR.genWingwall()
footIR,stackPntFootIR=wingWallIR.genWingwallFoundation(footsLength=[5.0],footsHeight=[1.0],footsWidth=[6.0],footsToeWidth=[0.5])
Part.show(wwIR,'wwIR')
Part.show(footIR,'footIR')

## aleta izquierda sección final
vDir=(stackPendHeadWall[1]-stackPendHeadWall[0]).normalize()
ptELwingwall=stackPendHeadWall[0]+struct.getSkewWallTh()*vDir
vDirLn=Vector(-0.5,1,0); vDirTr=vDirLn.cross(vZneg)
wingWallEL=underpass.Wingwall(placementPoint=ptELwingwall,foundLevel=-7,wallLenght=8,wallSlope=1/4,wallTopWidth=0.45,backFaceSlope=1/10,frontFaceSlope=0.0,vDirTr=vDirTr,vDirLn=vDirLn)
wwEL=wingWallEL.genWingwall()
footEL,stackPntFootEL=wingWallEL.genWingwallFoundation(footsLength=[3,5],footsHeight=[1.2,0.75],footsWidth=[5,4],footsToeWidth=[1.5,0.5])
Part.show(wwEL,'wwEL')
Part.show(footEL,'footEL')


## aleta derecha sección final
vDir=(stackPendHeadWall[1]-stackPendHeadWall[0]).normalize()
ptERwingwall=stackPendHeadWall[1]-struct.getSkewWallTh()*vDir
vDirLn=Vector(1,1,0); vDirTr=vDirLn.cross(vZpos)
wingWallER=underpass.Wingwall(placementPoint=ptERwingwall,foundLevel=-10,wallLenght=8,wallSlope=1/5,wallTopWidth=0.25,backFaceSlope=1/10,frontFaceSlope=0.0,vDirTr=vDirTr,vDirLn=vDirLn)
wwER=wingWallER.genWingwall()
footER,stackPntFootER=wingWallER.genWingwallFoundation(footsLength=[5,3],footsHeight=[1.2,0.8],footsWidth=[5,4],footsToeWidth=[1.5,0.7])
Part.show(wwER,'wwER')
Part.show(footER,'footER')

