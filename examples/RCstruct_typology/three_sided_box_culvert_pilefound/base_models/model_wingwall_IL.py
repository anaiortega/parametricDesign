from aux_sharing import sharing_parts as shp
from parametric_design.freeCAD_utils import geom_utils as gu
from parametric_design.freeCAD_civil.structures import underpass
from FreeCAD import Vector
from parametric_design.freeCAD_utils import drawing_tools as dt
import Part
from aux_sharing import sharing_IL_wingwall as IL
from aux_sharing import sharing_vars as shv

# Model wing-wall and chamfer (IL) - initial left
vDir=(shp.stackPinitHeadWall[1]-shp.stackPinitHeadWall[0]).normalize()
ptILwingwall=shp.stackPinitHeadWall[0]+shp.struct.getSkewWallTh()*vDir
if 'deltaZ_top_aletaIL' in locals():
    ptILwingwall=ptILwingwall+deltaZ_top_aletaIL*Vector(0,0,1)
v=shp.struct.getVectFrontalView()
vDirLn=gu.getRotatedVector(v,Vector(0,0,-1),IL.angww)
vDirTr=vDirLn.cross(Vector(0,0,1))
shp.wingWallIL=underpass.Wingwall(placementPoint=ptILwingwall,
                              foundLevel=IL.Zww-shv.vTransfCoord.z,
                              wallLenght=IL.lenww,
                              wallSlope=IL.wallSlopeww,
                              wallTopWidth=IL.ww_data['wallTopWidth'],
                              backFaceSlope=IL.ww_data['backFaceSlope'],
                              frontFaceSlope=IL.ww_data['frontFaceSlope'],
                              vDirTr=vDirTr,
                              vDirLn=vDirLn,
                              dispLn=IL.dispLn,
                              )
shp.wwIL,shp.stackPntWwIL=shp.wingWallIL.genWingwall()
shp.footIL,shp.stackPntFootIL=shp.wingWallIL.genWingwallFoundation(
    footsLength=[IL.lenww],
    footsHeight=[IL.ww_data['footHeight']],
    footsWidth=[IL.ww_data['footWidth']],
    footsToeWidth=[IL.ww_data['footToeWidth']])
shp.chamferIL=dt.draw_triang_prism(
    p1=ptILwingwall,
    p2=ptILwingwall-shp.struct.getSkewWallTh()*vDir,
    p3=ptILwingwall+vDirLn*IL.dispLn,
    vAxis=Vector(0,0,-IL.hMax),
    )
Part.show(shp.wwIL,'wwIL')
Part.show(shp.footIL,'footIL')
Part.show(shp.chamferIL,'chamferIL')
