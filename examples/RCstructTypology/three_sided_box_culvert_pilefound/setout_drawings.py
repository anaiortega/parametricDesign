import FreeCAD
from freeCAD_civil import tables
from aux_sharing import sharing_parts as shp
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv
from freeCAD_civil import draw_config as cfg
from data import geomData as gd

shd.docSetout=FreeCAD.newDocument(gd.obraNm+'_REPL',gd.obraNm+'_REPL')
shv.setoutCfg=cfg.tableConf(wColumns=[15,25,25,18],hRows=5,hText=2.5)

shv.desfaseTablas=5 # espacio vertical entre tablas

# Replanteo tablero
from base_models import setout_deck

# Replanteo pilotes
from base_models import setout_piles


# Alzado aleta 1 (EL)
shv.nmbAleta='1'
shv.pntLst=shp.stackPntWwEL
from base_models import setout_wall_wingWall

# Zapata aleta 1 (EL)
shv.nmbAleta='1'
shv.pntLst=shp.stackPntFootEL[0]
from base_models import setout_foot_wingWall

# Alzado aleta 2 (IL)
shv.nmbAleta='2'
shv.pntLst=shp.stackPntWwIL
from base_models import setout_wall_wingWall

# Zapata aleta 2 (IL)
shv.nmbAleta='2'
shv.pntLst=shp.stackPntFootIL[0]
from base_models import setout_foot_wingWall

# Alzado aleta 3 (IR)
shv.nmbAleta='3'
shv.pntLst=shp.stackPntWwIR
from base_models import setout_wall_wingWall

# Zapata aleta 3 (IR)
shv.nmbAleta='3'
shv.pntLst=shp.stackPntFootIR[0]
from base_models import setout_foot_wingWall

# Alzado aleta 4 (ER)
shv.nmbAleta='4'
shv.pntLst=shp.stackPntWwER
from base_models import setout_wall_wingWall

# Zapata aleta 4 (ER)
shv.nmbAleta='4'
shv.pntLst=shp.stackPntFootER[0]
from base_models import setout_foot_wingWall


