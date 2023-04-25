import Part
from aux_sharing import sharing_parts as shp
from data import geomData as gd
# Model piles
# Piles left wall
v1=shp.leftWall.Vertexes[6]
v2=shp.leftWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
shp.pilesLeft,shp.stakPpilesLeft=shp.struct.genArrayPiles(
    fiPile=gd.fiPile,
    lengthPile=gd.lengthPileLeft,
    distPiles=gd.distPilesLeft,
    nPiles=gd.nPilesLeft,
    refPoint=refPoint,
    distFirstPile2refPoint=gd.distFirstPileLeft2refPoint)
Part.show(shp.pilesLeft,'pilesLeft')

# Piles right wall
v1=shp.rightWall.Vertexes[6]
v2=shp.rightWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
shp.pilesRight,shp.stakPpilesRight=shp.struct.genArrayPiles(
    fiPile=gd.fiPile,
    lengthPile=gd.lengthPileRight,
    distPiles=gd.distPilesRight,
    nPiles=gd.nPilesRight,
    refPoint=refPoint,
    distFirstPile2refPoint=gd.distFirstPileRight2refPoint)
Part.show(shp.pilesRight,'pilesRight')
