from aux_sharing import sharing_parts as shp
from freeCAD_utils import geom_utils as gu
from aux_sharing import sharing_EL_wingwall as EL
from freeCAD_civil.structures import underpass
from FreeCAD import Vector
from freeCAD_utils import drawing_tools as dt
import Part
from aux_sharing import sharing_vars as shv

# Model aleta and chamfer EL (end left)
vDir=(shp.stackPendHeadWall[1]-shp.stackPendHeadWall[0]).normalize()
ptELwingwall=shp.stackPendHeadWall[0]+shp.struct.getSkewWallTh()*vDir
if 'deltaZ_top_aletaEL' in locals():
    ptELwingwall=ptELwingwall+deltaZ_top_aletaEL*Vector(0,0,1)
v=shp.struct.getVectDorsalView()
vDirLn=gu.getRotatedVector(v,Vector(0,0,1),EL.angww)
vDirTr=vDirLn.cross(Vector(0,0,-1))
shp.wingWallEL=underpass.Wingwall(placementPoint=ptELwingwall,
                              foundLevel=EL.Zww-shv.vTransfCoord.z,
                              wallLenght=EL.lenww,
                              wallSlope=EL.wallSlopeww,
                              wallTopWidth=EL.ww_data['wallTopWidth'],
                              backFaceSlope=EL.ww_data['backFaceSlope'],
                              frontFaceSlope=EL.ww_data['frontFaceSlope'],
                              vDirTr=vDirTr,
                              vDirLn=vDirLn,
                              dispLn=EL.dispLn,
)
shp.wwEL,shp.stackPntWwEL=shp.wingWallEL.genWingwall()
shp.footEL,shp.stackPntFootEL=shp.wingWallEL.genWingwallFoundation(
    footsLength=[EL.lenww],
    footsHeight=[EL.ww_data['footHeight']],
    footsWidth=[EL.ww_data['footWidth']],
    footsToeWidth=[EL.ww_data['footToeWidth']])
shp.chamferEL=dt.draw_triang_prism(
    p1=ptELwingwall,
    p2=ptELwingwall-shp.struct.getSkewWallTh()*vDir,
    p3=ptELwingwall+vDirLn*EL.dispLn,
    vAxis=Vector(0,0,-EL.hMax),
    )
Part.show(shp.wwEL,'wwEL')
Part.show(shp.footEL,'footEL')
Part.show(shp.chamferEL,'chamferEL')
