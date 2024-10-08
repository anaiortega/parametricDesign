import math
import FreeCAD
from FreeCAD import Vector
from parametric_design.freeCAD_civil import draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from parametric_design.freeCAD_civil import draw_config as cfg

from data import geomData as gd

# Sección transversal ortogonal
hMinMortero=3e-2 # altura mínima del mortero de formación de pendientes
pteMortero=2/100 # pendiente del mortero de formación de pendientes
sobranchoHL=0.20 # sobreancho hormigón de limpieza
thHL=0.1 # espesor hormigón de limpieza
auxDimWall=(gd.thWall-gd.fiPile)/2

# points transversal-central section (TC)
## deck
pt_TC1=Vector(0,0)
pt_TC2=Vector(gd.wDeck,0)
pt_TC3=pt_TC2+Vector(0,gd.thDeck-gd.thPrelosa)
pt_TC4=pt_TC1+Vector(0,gd.thDeck-gd.thPrelosa)
## left wall
pt_TC5=pt_TC1-Vector(0,gd.hLeftWall+gd.thPrelosa)
pt_TC5b=pt_TC5+Vector(auxDimWall,0)
pt_TC6=pt_TC5+Vector(gd.thWall,0)
pt_TC6b=pt_TC6-Vector(auxDimWall,0)
pt_TC7=pt_TC6+Vector(0,gd.hLeftWall)
## right wall
pt_TC8=pt_TC2-Vector(0,gd.hRightWall+gd.thPrelosa)
pt_TC8b=pt_TC8-Vector(auxDimWall,0)
pt_TC9=pt_TC8-Vector(gd.thWall,0)
pt_TC9b=pt_TC9+Vector(auxDimWall,0)
pt_TC10=pt_TC9+Vector(0,gd.hRightWall)
## prelosa
pt_TC1_prelosa=pt_TC7-Vector(gd.entregaPrelosa,0)
pt_TC2_prelosa=pt_TC10+Vector(gd.entregaPrelosa,0)
pt_TC3_prelosa=pt_TC2_prelosa+Vector(0,gd.thPrelosa)
pt_TC4_prelosa=pt_TC1_prelosa+Vector(0,gd.thPrelosa)

## formación pendientes
pt_TC1_ptes=pt_TC4+Vector(0,hMinMortero)
pt_TC2_ptes=pt_TC1_ptes+Vector(gd.wDeck/2,gd.wDeck/2*pteMortero)
pt_TC3_ptes=pt_TC3+Vector(0,hMinMortero)

# hormigón de limpieza
hl_5c=pt_TC5-Vector(sobranchoHL,0)
hl_5d=hl_5c-Vector(0,thHL)
hl_5e=pt_TC5b-Vector(0,thHL)
hl_6c=pt_TC6-Vector(0,thHL)
hl_6d=pt_TC6b-Vector(0,thHL)

hl_8c=pt_TC8+Vector(sobranchoHL,0)
hl_8d=hl_8c-Vector(0,thHL)
hl_8e=pt_TC8b-Vector(0,thHL)
hl_9c=pt_TC9-Vector(0,thHL)
hl_9d=pt_TC9b-Vector(0,thHL)

# murete de guarda
mg_1=pt_TC1+Vector(0,gd.thDeck-gd.thPrelosa+gd.hHeadWall)
mg_2=mg_1+Vector(gd.skewThHeadWall,0)
mg_3=mg_2-Vector(0,gd.hHeadWall)
mg_4=mg_3+Vector(gd.thDeck,0)
mg_5=mg_4-Vector(0,gd.thDeck-gd.thPrelosa)
mg_6=pt_TC1-Vector(0,gd.thPrelosa)
mg_7=mg_5-Vector(0,gd.thPrelosa)
                 

docName=gd.obraNm.replace(' ','')+'_stransv'
docStransv=FreeCAD.newDocument(docName,docName)
# set the dimension style for this document
cfg.set_dim_style(scale=gd.scale,dimStyProp=cfg.XCdimProp)

vTrans=Vector(0,0)
lstPtsConcrSect1= [pt_TC8b,pt_TC8,pt_TC2,pt_TC3,pt_TC4,pt_TC3,pt_TC4,pt_TC1,pt_TC5,pt_TC5b]
rb.drawConcreteSection(lstPtsConcrSect1,vTrans,dimConcrSect=True,spacDimLine=5e-3/gd.scale)
lstPtsConcrSect2=[pt_TC6b,pt_TC6,pt_TC7,pt_TC1_prelosa,pt_TC4_prelosa,pt_TC3_prelosa,pt_TC2_prelosa,pt_TC10,pt_TC9,pt_TC9b]
rb.drawConcreteSection(lstPtsConcrSect2,vTrans,dimConcrSect=True,spacDimLine=5e-3/gd.scale)
lstPtsConcrSect3=[pt_TC5b,pt_TC6b]
rb.drawConcreteSection(lstPtsConcrSect3,vTrans,color=cfg.colorHidden)
lstPtsConcrSect3=[pt_TC9b,pt_TC8b]
rb.drawConcreteSection(lstPtsConcrSect3,vTrans,color=cfg.colorHidden)
# Prelosa
lstPntsPrelosa=[pt_TC1_prelosa,pt_TC2_prelosa,pt_TC3_prelosa,pt_TC4_prelosa,pt_TC1_prelosa]
rb.drawConcreteSection(lstPntsPrelosa,vTrans)
lstPntsMortero=[pt_TC4,pt_TC1_ptes,pt_TC2_ptes,pt_TC3_ptes,pt_TC3,pt_TC4]
rb.drawConcreteSection(lstPntsMortero,vTrans)
# junta de construcción
vThPrelosa=Vector(0,gd.thPrelosa)
lstPtsJunta=[pt_TC1-vThPrelosa,pt_TC4_prelosa-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans,color=cfg.colorHidden)
lstPtsJunta=[pt_TC3_prelosa-vThPrelosa,pt_TC2-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans,color=cfg.colorHidden)


# Hormigón de limpieza
lstHL=[pt_TC5,hl_5c,hl_5d,hl_5e]
rb.drawConcreteSection(lstHL,vTrans)
lstHL=[pt_TC6,hl_6c,hl_6d]
rb.drawConcreteSection(lstHL,vTrans)
lstHL=[hl_5e,hl_6d]
rb.drawConcreteSection(lstHL,vTrans,color=cfg.colorHidden)

lstHL=[pt_TC8,hl_8c,hl_8d,hl_8e]
rb.drawConcreteSection(lstHL,vTrans)
lstHL=[pt_TC9,hl_9c,hl_9d]
rb.drawConcreteSection(lstHL,vTrans)
lstHL=[hl_8e,hl_9d]
rb.drawConcreteSection(lstHL,vTrans,color=cfg.colorHidden)


# murete de guarda
vTrans=Vector(0,2)
lstMG=[mg_5,pt_TC1,mg_1,mg_2,mg_3,mg_4]
rb.drawConcreteSection(lstMG,vTrans,dimConcrSect=True,spacDimLine=5e-3/gd.scale)
lstMG=[pt_TC1,mg_6,mg_7]
rb.drawConcreteSection(lstMG,vTrans)# generate the drawings of geometry (transverse section)

import sys
sys.path.append('/usr/local/src/prg/parametricDesign/examples/RCstruct_typology/three_sided_box_culvert_pilefound/')

from base_models import defGeom_deck_plus_walls



