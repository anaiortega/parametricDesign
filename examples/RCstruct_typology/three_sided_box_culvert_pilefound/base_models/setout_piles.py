# Pilotes lado izquierdo
from FreeCAD import Vector
from parametric_design.freeCAD_civil import tables
from aux_sharing import sharing_parts as shp
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

shv.pntLst=shp.stakPpilesLeft
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo pilotes (izq.)',
    pntTLcorner=shv.nextCorner,
    preffixPnt='PI-',
    tbCfg=shv.setoutCfg,
    vCooRel2Abs=shv.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*shv.setoutCfg.hRows+shv.desfaseTablas)


# Pilotes lado derecho
shv.pntLst=shp.stakPpilesRight
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo pilotes (der.)',
    pntTLcorner=shv.nextCorner,
    preffixPnt='PD-',
    tbCfg=shv.setoutCfg,
    vCooRel2Abs=shv.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*shv.setoutCfg.hRows+shv.desfaseTablas)
