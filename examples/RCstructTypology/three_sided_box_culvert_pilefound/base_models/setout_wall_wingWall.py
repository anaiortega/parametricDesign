# Replanteo alzado aleta

tables.settingOutTable(
    lstPoints=pntLst,
    title='Replanteo alzado aleta '+nmbAleta,
    pntTLcorner=nextCorner,
    preffixPnt='AA'+nmbAleta+'-',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=vTransfCoord,
    doc=docSetout,
    )
nextCorner=nextCorner-Vector(0,(len(pntLst)+2)*hRows+hRows/2)
