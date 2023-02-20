# Tablero
pntLst=[P1-vTransfCoord]
pntLst+=[P1+gd.distAxisStartPnt*struct.getDirecVectLAxis()-vTransfCoord]
pntLst+=[P2-vTransfCoord]
pntLst+=deck_stakingPt
nextCorner=Vector(0,0)
tables.settingOutTable(
    lstPoints=pntLst,
    title='Replanteo tablero',
    pntTLcorner=nextCorner,
    preffixPnt='',
    hText=hText,
    hRows=hRows,
    wColumns=wColumns,
    vCooRel2Abs=vTransfCoord,
    doc=docSetout,
    )
nextCorner=nextCorner-Vector(0,(len(pntLst)+2)*hRows+desfaseTablas)
