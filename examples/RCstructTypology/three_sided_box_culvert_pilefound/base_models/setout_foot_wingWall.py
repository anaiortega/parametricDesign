# Replanteo zapata aleta
tables.settingOutTable(
    lstPoints=pntLst,
    title='Replanteo zapata aleta '+nmbAleta,
    pntTLcorner=nextCorner,
    preffixPnt='ZA'+nmbAleta+'-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=vTransfCoord,
    doc=docSetout,
    )
nextCorner=nextCorner-Vector(0,(len(pntLst)+2)*hRows+desfaseTablas)
