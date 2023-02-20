
import math
from freeCAD_civil.structures import underpass
from freeCAD_utils import geom_utils as gu
from freeCAD_utils import drawing_tools as dt
import Part
from FreeCAD import Vector
# PF ría de Tuero FFCC
path='/home/ana/projects/variante-rincon-de-soto/work/montaje_planos_losas/PF_ria_Tuero_FFCC/aletas/'
pathDeck=path.replace('aletas/','')
exec(open(pathDeck+'datosGeom.py').read())
docGeom=App.newDocument(obraNm+'_GEOM',obraNm+'_GEOM')

P1=Vector(P1_coo[0],P1_coo[1],P1_coo[2])
P2=Vector(P2_coo[0],P2_coo[1],P2_coo[2])
vTransfCoord=Vector(vTransfCoord_coo[0],vTransfCoord_coo[1],vTransfCoord_coo[2])

ww_type1a={'wallTopWidth':0.25,'backFaceSlope':0,'frontFaceSlope':0,'footHeight':0.35,'footWidth':1.9,'footToeWidth':0}


# Aleta 1 (EL)
exec(open(path+'datos_aleta1.py').read())
ELww_data=ww_type1a
angELww=33*90/100 # ángulo con el eje en sexagesimales
lenELww=lWall #longitud medida desde el arranque interno
Z_ELww=Z_baseWall
wallSlopeELww=(hWallMax-hWallMin)/lWall
dispLnEL=thWall*math.cos(math.radians(90+skew-angELww))
hMaxEL=hWallMax

# Aleta 2 (IL)
exec(open(path+'datos_aleta2.py').read())
ILww_data=ww_type1a
angILww=33*90/100 # ángulo con el eje en sexagesimales
lenILww=lWall #longitud medida desde el arranque interno
Z_ILww=Z_baseWall
wallSlopeILww=(hWallMax-hWallMin)/lWall
dispLnIL=skewThwall*math.cos(math.radians(90-skew-angILww))
hMaxIL=hWallMax

# Aleta 3 (IR)
exec(open(path+'datos_aleta3.py').read())
IRww_data=ww_type1a
angIRww=33*90/100 # ángulo con el eje en sexagesimales
lenIRww=lWall #longitud medida desde el arranque interno
Z_IRww=Z_baseWall
wallSlopeIRww=(hWallMax-hWallMin)/lWall
dispLnIR=thWall/math.sin(skewRad)*math.cos((90-skewRad)+math.radians(angIRww))
dispLnIR=thWall*math.cos(math.radians(90+skew-angIRww))
hMaxIR=hWallMax


# Aleta 4 (ER)
exec(open(path+'datos_aleta4.py').read())
ERww_data=ww_type1a
angERww=33*90/100 # ángulo con el eje en sexagesimales
lenERww=lWall  #longitud medida desde el arranque interno
Z_ERww=Z_baseWall
wallSlopeERww=(hWallMax-hWallMin)/lWall
dispLnER=skewThwall*math.cos(math.radians(90-skew-angERww))
hMaxER=hWallMax

# fin datos
# Deck and walls
exec(open(pathDeck+'../base_models/model_deck_and_walls.py').read())

# Piles
exec(open(pathDeck+'../base_models/model_piles_deck_plus_walls.py').read())


# angle structure axis with X global axis
# Aleta 1 (EL)
exec(open(pathDeck+'../base_models/model_aleta_EL.py').read())

# Aleta 2 (IL)
## aleta izquierda sección inicial
exec(open(pathDeck+'../base_models/model_aleta_IL.py').read())

# Aleta 3 (IR)
## aleta derecha sección inicial
exec(open(pathDeck+'../base_models/model_aleta_IR.py').read())


# Aleta 4 (ER)
## aleta derecha sección final
exec(open(pathDeck+'../base_models/model_aleta_ER.py').read())

#Vistas
exec(open(pathDeck+'../base_models/views_deck_plus_walls.py').read())
