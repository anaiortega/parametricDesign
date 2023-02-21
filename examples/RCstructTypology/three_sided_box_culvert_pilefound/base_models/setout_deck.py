# Tablero
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

shv.pntLst=[P1-shp.vTransfCoord]
shv.pntLst+=[P1+gd.distAxisStartPnt*struct.getDirecVectLAxis()-shp.vTransfCoord]
shv.pntLst+=[P2-shp.vTransfCoord]
shv.pntLst+=shp.deck_stakingPt
shv.nextCorner=Vector(0,0)
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo tablero',
    pntTLcorner=shv.nextCorner,
    preffixPnt='',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=shp.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*hRows+desfaseTablas)
