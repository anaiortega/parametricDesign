# Model the deck and walls
from FreeCAD import Vector
from data import geomData as gd
from freeCAD_civil.structures import underpass
import Part
from aux_sharing import sharing_parts as shp
from aux_sharing import sharing_vars as shv

shv.P1=Vector(gd.P1_coo[0],gd.P1_coo[1],gd.P1_coo[2])
shv.P2=Vector(gd.P2_coo[0],gd.P2_coo[1],gd.P2_coo[2])
shv.vTransfCoord=Vector(gd.vTransfCoord_coo[0],gd.vTransfCoord_coo[1],gd.vTransfCoord_coo[2])

vZpos=Vector(0,0,1)
vZneg=Vector(0,0,-1)

hInt=gd.Z_topDeck-gd.thDeck-gd.Z_baseWall
span=gd.wDeck-2*gd.thWall
shp.struct=underpass.Underpass(startLAxPoint=shv.P1-shv.vTransfCoord,
                           endLAxPoint=shv.P2-shv.vTransfCoord,
                           posFrameLAxVect=[0,0,hInt+gd.thDeck],
                           vertIntHeigAx=hInt,
                           intSpan=span,
                           wallTh=gd.thWall,
                           deckTh=gd.thDeck,
                           deckTrSlope=0,
                           skewAngle=gd.skew)
shp.deck,shp.deck_stakingPt=shp.struct.genDeck()
Part.show(shp.deck,'deck')

shp.initHeadWall,shp.stackPinitHeadWall=shp.struct.genHeadWall(leftHeight=gd.hHeadWall,rightHeight=gd.hHeadWall,thickness=gd.thHeadWall,section='I')
Part.show(shp.initHeadWall,'initHeadWall')

shp.endHeadWall,shp.stackPendHeadWall=shp.struct.genHeadWall(leftHeight=gd.hHeadWall,rightHeight=gd.hHeadWall,thickness=gd.thHeadWall,section='E')
Part.show(shp.endHeadWall,'endHeadWall')

shp.leftWall=shp.struct.genLeftWall()
Part.show(shp.leftWall,'leftWall')

shp.rightWall=shp.struct.genRightWall()
Part.show(shp.rightWall,'rightWall')

