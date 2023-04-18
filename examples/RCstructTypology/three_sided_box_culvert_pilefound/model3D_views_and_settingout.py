import FreeCAD
import math
from freeCAD_utils import drawing_tools as dt
from FreeCAD import Vector
import sys

currentPath='/usr/local/src/prg/parametricDesign/examples/RCstructTypology/three_sided_box_culvert_pilefound'
sys.path.append(currentPath)
from data import geomData as gd
from aux_sharing import sharing_docs as shd

shd.docGeom=FreeCAD.newDocument(gd.obraNm+'_GEOM',gd.obraNm+'_GEOM')


ww_type1a={'wallTopWidth':0.25,'backFaceSlope':0,'frontFaceSlope':0,'footHeight':0.35,'footWidth':1.9,'footToeWidth':0}


# Aleta 1 (EL)
from data import data_wingwall1 as dww1
from aux_sharing import sharing_EL_wingwall as EL
EL.ww_data=ww_type1a
EL.angww=33*90/100 # ángulo con el eje en sexagesimales
EL.lenww=dww1.lWall #longitud medida desde el arranque interno
EL.Zww=gd.Z_baseWall
EL.wallSlopeww=(dww1.hWallMax-dww1.hWallMin)/dww1.lWall
EL.dispLn=gd.thWall*math.cos(math.radians(90+gd.skew-EL.angww))
EL.hMax=dww1.hWallMax

# Aleta 2 (IL)
from data import data_wingwall1 as dww2
from aux_sharing import sharing_IL_wingwall as IL
IL.ww_data=ww_type1a
IL.angww=33*90/100 # ángulo con el eje en sexagesimales
IL.lenww=dww2.lWall #longitud medida desde el arranque interno
IL.Zww=gd.Z_baseWall
IL.wallSlopeww=(dww2.hWallMax-dww2.hWallMin)/dww2.lWall
IL.dispLn=gd.skewThwall*math.cos(math.radians(90-gd.skew-IL.angww))
IL.hMax=dww2.hWallMax

# Aleta 3 (IR)
from data import data_wingwall1 as dww3
from aux_sharing import sharing_IR_wingwall as IR
IR.ww_data=ww_type1a
IR.angww=33*90/100 # ángulo con el eje en sexagesimales
IR.lenww=dww3.lWall #longitud medida desde el arranque interno
IR.Zww=gd.Z_baseWall
IR.wallSlopeww=(dww3.hWallMax-dww3.hWallMin)/dww3.lWall
IR.dispLn=gd.thWall/math.sin(gd.skewRad)*math.cos((90-gd.skewRad)+math.radians(IR.angww))
IR.dispLn=gd.thWall*math.cos(math.radians(90+gd.skew-IR.angww))
IR.hMax=dww3.hWallMax


# Aleta 4 (ER)
from data import data_wingwall1 as dww4
from aux_sharing import sharing_ER_wingwall as ER
ER.ww_data=ww_type1a
ER.angww=33*90/100 # ángulo con el eje en sexagesimales
ER.lenww=dww4.lWall  #longitud medida desde el arranque interno
ER.Zww=gd.Z_baseWall
ER.wallSlopeww=(dww4.hWallMax-dww4.hWallMin)/dww4.lWall
ER.dispLn=gd.skewThwall*math.cos(math.radians(90-gd.skew-ER.angww))
ER.hMax=dww4.hWallMax

# fin datos


# Deck and walls
from base_models import model_deck_and_walls

# Piles
from base_models import model_piles_deck_plus_walls

# angle structure axis with X global axis
# Aleta 1 (EL)
from base_models import model_wingwall_EL

# Aleta 2 (IL)
## aleta izquierda sección inicial
from base_models import model_wingwall_IL

# Aleta 3 (IR)
## aleta derecha sección inicial
from base_models import model_wingwall_IR

# Aleta 4 (ER)
## aleta derecha sección final
from base_models import model_wingwall_ER
#Vistas
from base_models import views_deck_plus_walls

# go to combo view -> show drawing vistas

# Setting-out
import setout_drawings
