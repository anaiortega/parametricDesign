from aux_sharing import sharing_parts as shp
from parametric_design.freeCAD_utils import geom_utils as gu
from parametric_design.freeCAD_civil.structures import underpass
from FreeCAD import Vector
from parametric_design.freeCAD_utils import drawing_tools as dt
import Part
from aux_sharing import sharing_ER_wingwall as ER
from aux_sharing import sharing_vars as shv

# Model wing-wall and chamfer (ER) - end right
vDir=(shp.stackPendHeadWall[1]-shp.stackPendHeadWall[0]).normalize()
ptERwingwall=shp.stackPendHeadWall[1]-shp.struct.getSkewWallTh()*vDir
if 'deltaZ_top_aletaER' in locals():
    ptERwingwall=ptERwingwall+deltaZ_top_aletaER*Vector(0,0,1)
v=shp.struct.getVectDorsalView()
vDirLn=gu.getRotatedVector(v,Vector(0,0,-1),ER.angww)
vDirTr=vDirLn.cross(Vector(0,0,1))
shp.wingWallER=underpass.Wingwall(
    placementPoint=ptERwingwall,
    foundLevel=ER.Zww-shv.vTransfCoord.z,
    wallLenght=ER.lenww,
    wallSlope=ER.wallSlopeww,
    wallTopWidth=ER.ww_data['wallTopWidth'],
    backFaceSlope=ER.ww_data['backFaceSlope'],
    frontFaceSlope=ER.ww_data['frontFaceSlope'],
    vDirTr=vDirTr,
    vDirLn=vDirLn,
    dispLn=ER.dispLn,
    )
shp.wwER,shp.stackPntWwER=shp.wingWallER.genWingwall()
shp.footER,shp.stackPntFootER=shp.wingWallER.genWingwallFoundation(
    footsLength=[ER.lenww],
    footsHeight=[ER.ww_data['footHeight']],
    footsWidth=[ER.ww_data['footWidth']],
    footsToeWidth=[ER.ww_data['footToeWidth']])
shp.chamferER=dt.draw_triang_prism(
    p1=ptERwingwall,
    p2=ptERwingwall+shp.struct.getSkewWallTh()*vDir,
    p3=ptERwingwall+vDirLn*ER.dispLn,
    vAxis=Vector(0,0,-ER.hMax),
    )
Part.show(shp.wwER,'wwER')
Part.show(shp.footER,'footER')
Part.show(shp.chamferER,'chamferER')

