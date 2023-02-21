# Replanteo zapata aleta
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

tables.settingOutTable(
    lstPoints=shv.pntLst,
    title='Replanteo zapata aleta '+shv.nmbAleta,
    pntTLcorner=shv.nextCorner,
    preffixPnt='ZA'+shv.nmbAleta+'-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=shp.vTransfCoord,
    doc=shd.docSetout,
    )
shv.nextCorner=shv.nextCorner-Vector(0,(len(shv.pntLst)+2)*hRows+desfaseTablas)
