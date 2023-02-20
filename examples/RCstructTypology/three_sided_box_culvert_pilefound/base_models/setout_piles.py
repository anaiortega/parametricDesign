# Pilotes lado izquierdo
pntLst=stakPpilesLeft
tables.settingOutTable(
    lstPoints=pntLst,
    title='Replanteo pilotes (izq.)',
    pntTLcorner=nextCorner,
    preffixPnt='PI-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=vTransfCoord,
    doc=docSetout,
    )
nextCorner=nextCorner-Vector(0,(len(pntLst)+2)*hRows+desfaseTablas)


# Pilotes lado derecho
pntLst=stakPpilesRight
tables.settingOutTable(
    lstPoints=pntLst,
    title='Replanteo pilotes (der.)',
    pntTLcorner=nextCorner,
    preffixPnt='PD-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=vTransfCoord,
    doc=docSetout,
    )
nextCorner=nextCorner-Vector(0,(len(pntLst)+2)*hRows+desfaseTablas)
