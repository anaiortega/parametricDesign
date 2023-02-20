# Model piles
# Piles left wall
v1=leftWall.Vertexes[6]
v2=leftWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
pilesLeft,stakPpilesLeft=struct.genArrayPiles(
    fiPile=gd.fiPile,
    lengthPile=gd.lengthPileLeft,
    distPiles=gd.distPilesLeft,
    nPiles=gd.nPilesLeft,
    refPoint=refPoint,
    distFirstPile2refPoint=gd.distFirstPileLeft2refPoint)
Part.show(pilesLeft,'pilesLeft')

# Piles right wall
v1=rightWall.Vertexes[6]
v2=rightWall.Vertexes[4]
refPoint=(v1.Point+v2.Point)/2
pilesRight,stakPpilesRight=struct.genArrayPiles(
    fiPile=gd.fiPile,
    lengthPile=gd.lengthPileRight,
    distPiles=gd.distPilesRight,
    nPiles=gd.nPilesRight,
    refPoint=refPoint,
    distFirstPile2refPoint=gd.distFirstPileRight2refPoint)
Part.show(pilesRight,'pilesRight')
