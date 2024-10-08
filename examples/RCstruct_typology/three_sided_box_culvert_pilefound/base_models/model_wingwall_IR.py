from aux_sharing import sharing_parts as shp
from parametric_design.freeCAD_utils import geom_utils as gu
from parametric_design.freeCAD_civil.structures import underpass
from FreeCAD import Vector
from parametric_design.freeCAD_utils import drawing_tools as dt
import Part
from aux_sharing import sharing_IR_wingwall as IR
from aux_sharing import sharing_vars as shv

# Model wing-wall and chamfer (IR) - initial right
vDir=(shp.stackPinitHeadWall[1]-shp.stackPinitHeadWall[0]).normalize()
ptIRwingwall=shp.stackPinitHeadWall[1]-shp.struct.getSkewWallTh()*vDir
if 'deltaZ_top_aletaIR' in locals():
    ptIRwingwall=ptIRwingwall+deltaZ_top_aletaIR*Vector(0,0,1)
v=shp.struct.getVectFrontalView()
vDirLn=gu.getRotatedVector(v,Vector(0,0,1),IR.angww)
vDirTr=vDirLn.cross(Vector(0,0,-1))
shp.wingWallIR=underpass.Wingwall(placementPoint=ptIRwingwall,
                              foundLevel=IR.Zww-shv.vTransfCoord.z,
                              wallLenght=IR.lenww,
                              wallSlope=IR.wallSlopeww,
                              wallTopWidth=IR.ww_data['wallTopWidth'],
                              backFaceSlope=IR.ww_data['backFaceSlope'],
                              frontFaceSlope=IR.ww_data['frontFaceSlope'],
                              vDirTr=vDirTr,
                              vDirLn=vDirLn,
                              dispLn=IR.dispLn,
                              )
shp.wwIR,shp.stackPntWwIR=shp.wingWallIR.genWingwall()
shp.footIR,shp.stackPntFootIR=shp.wingWallIR.genWingwallFoundation(
    footsLength=[IR.lenww],
    footsHeight=[IR.ww_data['footHeight']],
    footsWidth=[IR.ww_data['footWidth']],
    footsToeWidth=[IR.ww_data['footToeWidth']])
shp.chamferIR=dt.draw_triang_prism(
    p1=ptIRwingwall,
    p2=ptIRwingwall+shp.struct.getSkewWallTh()*vDir,
    p3=ptIRwingwall+vDirLn*IR.dispLn,
    vAxis=Vector(0,0,-IR.hMax),
    )
Part.show(shp.wwIR,'wwIR')
Part.show(shp.footIR,'footIR')
Part.show(shp.chamferIR,'chamferIR')
