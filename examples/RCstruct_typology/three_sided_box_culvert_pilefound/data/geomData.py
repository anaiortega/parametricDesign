import math
obraNm='PF_ria_Tuero_FFCC'

scale=1/25 # Scale to draw concrete cross-section
# Coordenadas absolutas extremos eje cara superior tablero
Z_topDeck=282.39
P1_coo=(596446.6281,4675671.7711,Z_topDeck)
P2_coo=(596453.9545,4675676.9865,Z_topDeck)
vTransfCoord_coo=(596400,4675600,250)

Ldeck=round(math.sqrt((P2_coo[0]-P1_coo[0])**2+(P2_coo[1]-P1_coo[1])**2),2)+1e-2
#print('length of the deck=',Ldeck)

#dimensiones del tablero
spanDeck=6.70 #internal width
thDeck=0.8 # canto total (incluso prelosa)
skew=90-101.92
skewRad=math.radians(skew)
distAxisStartPnt=4.2934
#skew=15
# dimensiones hastiales
Z_baseWall=280.09
thWall=0.80
skewThwall=thWall/math.cos(math.radians(skew)) #skewed thickness of wall
# muretes de guarda
thHeadWall=0.3
hHeadWall=0.3

# dimensiones pilotes
fiPile=0.225
distPilesLeft=1.00
lengthPileLeft=9
nPilesLeft=int(Ldeck/distPilesLeft)+1
distFirstPileLeft2refPoint=(Ldeck-(nPilesLeft-1)*distPilesLeft)/2
if distFirstPileLeft2refPoint<0.3:
    print('distancia inicial desde extremo a 1er. pilote=', round(distFirstPileLeft2refPoint,2))
    nPilesLeft=nPilesLeft-1
    distFirstPileLeft2refPoint=(Ldeck-(nPilesLeft-1)*distPilesLeft)/2

#print('distancia desde extremo a 1er. pilote=', round(distFirstPileLeft2refPoint,2))

distPilesRight=distPilesLeft
lengthPileRight=lengthPileLeft
nPilesRight=nPilesLeft
distFirstPileRight2refPoint=distFirstPileLeft2refPoint

wDeck=spanDeck+2*thWall #ancho total (ortogonal al eje)



thPrelosa=6.5e-2 # espesor prelosa
entregaPrelosa=5e-2 # entrega de la prelosa en el apoyo sobre los muros
cosSkewAngle=math.cos(math.radians(skew))

skewWdeck=round(wDeck/cosSkewAngle,3)  #skewed width of the deck
#print('orthogonal width of the deck=',wDeck)
#print('skewed width of the deck=',skewWdeck)
skewThHeadWall=round(thHeadWall/cosSkewAngle,3)  #skewed thickness of the head wall

#print('skewed thickness of the wall=',skewThwall)

hLeftWall=Z_topDeck-Z_baseWall-thDeck
#print ('height of left walll=',hLeftWall)
hRightWall=hLeftWall


skewWprelosa=skewWdeck-2*skewThHeadWall+2*entregaPrelosa

