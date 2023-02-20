# Model wing-wall and chamfer (ER) - end right
vDir=(stackPendHeadWall[1]-stackPendHeadWall[0]).normalize()
ptERwingwall=stackPendHeadWall[1]-struct.getSkewWallTh()*vDir
if 'deltaZ_top_aletaER' in locals():
    ptERwingwall=ptERwingwall+deltaZ_top_aletaER*Vector(0,0,1)
v=struct.getVectDorsalView()
vDirLn=gu.getRotatedVector(v,vZneg,angERww)
vDirTr=vDirLn.cross(vZpos)
wingWallER=underpass.Wingwall(
    placementPoint=ptERwingwall,
    foundLevel=Z_ERww-vTransfCoord.z,
    wallLenght=lenERww,
    wallSlope=wallSlopeERww,
    wallTopWidth=ERww_data['wallTopWidth'],
    backFaceSlope=ERww_data['backFaceSlope'],
    frontFaceSlope=ERww_data['frontFaceSlope'],
    vDirTr=vDirTr,
    vDirLn=vDirLn,
    dispLn=dispLnER,
    )
wwER,stackPntWwER=wingWallER.genWingwall()
footER,stackPntFootER=wingWallER.genWingwallFoundation(
    footsLength=[lenERww],
    footsHeight=[ERww_data['footHeight']],
    footsWidth=[ERww_data['footWidth']],
    footsToeWidth=[ERww_data['footToeWidth']])
chamferER=dt.draw_triang_prism(
    p1=ptERwingwall,
    p2=ptERwingwall+struct.getSkewWallTh()*vDir,
    p3=ptERwingwall+vDirLn*dispLnER,
    vAxis=Vector(0,0,-hMaxER),
    )
Part.show(wwER,'wwER')
Part.show(footER,'footER')
Part.show(chamferER,'chamferER')

