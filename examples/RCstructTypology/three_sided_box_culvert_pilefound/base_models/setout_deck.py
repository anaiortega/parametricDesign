# Tablero
from FreeCAD import Vector
from freeCAD_civil import tables
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv
from aux_sharing import sharing_parts as shp
from data import geomData as gd

shv.pntLst=[shv.P1-shv.vTransfCoord]
shv.pntLst+=[shv.P1+gd.distAxisStartPnt*shp.struct.getDirecVectLAxis()-shv.vTransfCoord]
shv.pntLst+=[shv.P2-shv.vTransfCoord]
shv.pntLst+=shp.deck_stakingPt
shv.nextCorner=Vector(0,0)
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo tablero',
    pntTLcorner=shv.nextCorner,
    preffixPnt='',
    tbCfg=shv.setoutCfg,
    vCooRel2Abs=shv.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*shv.setoutCfg.hRows+shv.desfaseTablas)
