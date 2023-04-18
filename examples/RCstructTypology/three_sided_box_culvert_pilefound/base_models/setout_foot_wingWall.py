# Replanteo zapata aleta
from FreeCAD import Vector
from freeCAD_civil import tables
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo zapata aleta '+shv.nmbAleta,
    pntTLcorner=shv.nextCorner,
    preffixPnt='ZA'+shv.nmbAleta+'-',
    tbCfg=shv.setoutCfg,
    vCooRel2Abs=shv.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*shv.setoutCfg.hRows+shv.desfaseTablas)
