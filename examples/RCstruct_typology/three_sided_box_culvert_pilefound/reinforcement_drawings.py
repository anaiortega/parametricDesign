# generate the drawings of the reforcement sections and rebar sckedule
import sys
sys.path.append('/usr/local/src/prg/parametricDesign/examples/RCstruct_typology/three_sided_box_culvert_pilefound')
# Draw reinforcement sections
from base_models import reinf_deck_plus_walls as rdpw

# Rebar schedule
import FreeCAD
from FreeCAD import Vector
from data import geomData as gd
from freeCAD_civil import reinf_bars as rb
from freeCAD_civil import draw_config as cfg

docName=gd.obraNm.replace(' ','')+'_despiece'
docDespiece=FreeCAD.newDocument(docName,docName)
pntSchedule=Vector(0,0)
titSchedule='DESPIECE ARMADURA PORTICO'
#rebar schedule dimensions
scheduleCfg=cfg.scheduleConf(wColumns=[10,30,30,10,20,12],hRows=10,hText=2.5,hTextSketch=2.0)
rb.barSchedule(rdpw.lstRebarFam,scheduleCfg,title=titSchedule,pntTLcorner=pntSchedule,doc=docDespiece)






