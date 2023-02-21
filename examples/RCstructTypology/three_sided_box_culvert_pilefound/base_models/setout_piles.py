# Pilotes lado izquierdo
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

shv.pntLst=stakPpilesLeft
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo pilotes (izq.)',
    pntTLcorner=shv.nextCorner,
    preffixPnt='PI-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=shp.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*hRows+desfaseTablas)


# Pilotes lado derecho
shv.pntLst=stakPpilesRight
tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo pilotes (der.)',
    pntTLcorner=shv.nextCorner,
    preffixPnt='PD-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=shp.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*hRows+desfaseTablas)
