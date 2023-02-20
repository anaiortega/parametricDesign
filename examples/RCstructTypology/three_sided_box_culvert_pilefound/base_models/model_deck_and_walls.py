# Model the deck and walls

vZpos=Vector(0,0,1)
vZneg=Vector(0,0,-1)

hInt=gd.Z_topDeck-gd.thDeck-gd.Z_baseWall
span=gd.wDeck-2*gd.thWall
struct=underpass.Underpass(startLAxPoint=P1-vTransfCoord,
                           endLAxPoint=P2-vTransfCoord,
                           posFrameLAxVect=[0,0,hInt+gd.thDeck],
                           vertIntHeigAx=hInt,
                           intSpan=span,
                           wallTh=gd.thWall,
                           deckTh=gd.thDeck,
                           deckTrSlope=0,
                           skewAngle=gd.skew)
deck,deck_stakingPt=struct.genDeck()
Part.show(deck,'deck')

initHeadWall,stackPinitHeadWall=struct.genHeadWall(leftHeight=gd.hHeadWall,rightHeight=gd.hHeadWall,thickness=gd.thHeadWall,section='I')
Part.show(initHeadWall,'initHeadWall')

endHeadWall,stackPendHeadWall=struct.genHeadWall(leftHeight=gd.hHeadWall,rightHeight=gd.hHeadWall,thickness=gd.thHeadWall,section='E')
Part.show(endHeadWall,'endHeadWall')

leftWall=struct.genLeftWall()
Part.show(leftWall,'leftWall')

rightWall=struct.genRightWall()
Part.show(rightWall,'rightWall')
