import math
import TechDraw
from FreeCAD import Vector
from data import geomData as gd
from aux_sharing import sharing_parts as shp
from aux_sharing import sharing_docs as shd

escalaPlanta=1 ; txtEscPlanta='1:1'
escalaAlzados=1 ; txtEscAlzados='1:1'
# Todos los elementos excepto pilotes
elemNoPile=[shd.docGeom.deck]
elemNoPile+=[shd.docGeom.initHeadWall,shd.docGeom.endHeadWall]
elemNoPile+=[shd.docGeom.leftWall,shd.docGeom.rightWall]
listWingWallObj=shd.docGeom.findObjects(Name='ww*')
listWingWallNames=[o.Label for o in listWingWallObj]

if 'wwEL' in listWingWallNames:
    print('added wingwall EL')
    elemNoPile+=[shd.docGeom.wwEL,shd.docGeom.footEL,shd.docGeom.chamferEL]
    

if 'wwIL' in listWingWallNames:
    print('added wingwall IL')
    elemNoPile+=[shd.docGeom.wwIL,shd.docGeom.footIL,shd.docGeom.chamferIL]

    
if 'wwIR' in listWingWallNames:
    print('added wingwall IR')
    elemNoPile+=[shd.docGeom.wwIR,shd.docGeom.footIR,shd.docGeom.chamferIR]
    

if 'wwER' in listWingWallNames:
    print('added wingwall ER')
    elemNoPile+=[shd.docGeom.wwER,shd.docGeom.footER,shd.docGeom.chamferER]

#Planta
allElem=elemNoPile+[shd.docGeom.pilesLeft,shd.docGeom.pilesRight]
#Left view
elemLVw=elemNoPile
#Right view
elemRVw=elemNoPile
#Front view
elemFVw=elemNoPile
#Dorsal view
elemDVw=elemNoPile

docViews = shd.docGeom.addObject('TechDraw::DrawPage',gd.obraNm+'_vistas')
template = shd.docGeom.addObject('TechDraw::DrawSVGTemplate','Template')
template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/A4_Landscape_blank.svg'
docViews.Template = shd.docGeom.Template
topView = shd.docGeom.addObject('TechDraw::DrawViewPart', 'Planta')
topView.Source = allElem
topView.Caption='PLANTA. ESCALA '+txtEscPlanta
#topView.ScaleType = u"Custom"
#topView.Scale=escalaPlanta*1000
topView.Direction = (0.0, 0.0, 1.0)
angAxis=math.degrees(shp.struct.getVectDorsalView().getAngle(Vector(1,0,0)))
angRot=360-angAxis
topView.Rotation=str(round(angRot,2))+' deg'
topView.Source= allElem
topView.HardHidden=True
rc = docViews.addView(topView)

frontView=shd.docGeom.addObject('TechDraw::DrawViewPart', 'vista_frontal')
frontView.Caption='ALZADO FRONTAL. ESCALA '+txtEscAlzados
frontView.Direction = shp.struct.getVectFrontalView() #(-1.0, 0.0, 0.0)
#frontView.Scale=escalaAlzados*1000
rc = docViews.addView(frontView)
frontView.Source= elemFVw
frontView.HardHidden=False
rc = docViews.addView(frontView)

dorsView=shd.docGeom.addObject('TechDraw::DrawViewPart', 'vista_dorsal')
dorsView.Caption='ALZADO DORSAL. ESCALA '+txtEscAlzados
dorsView.Direction = shp.struct.getVectDorsalView() #(-1.0, 0.0, 0.0)
#dorsView.Scale=escalaAlzados*1000
rc = docViews.addView(dorsView)
dorsView.Source= elemDVw
dorsView.HardHidden=False
rc = docViews.addView(dorsView)

leftView=shd.docGeom.addObject('TechDraw::DrawViewPart', 'vista_lat_drcho')
leftView.Caption='ALZADO LATERAL DERECHO. ESCALA '+txtEscAlzados
leftView.Direction = shp.struct.getVectRightView() 
#leftView.Scale=escalaAlzados*1000
rc = docViews.addView(leftView)
leftView.Source= elemLVw
leftView.HardHidden=False
rc = docViews.addView(leftView)

rightView=shd.docGeom.addObject('TechDraw::DrawViewPart', 'vista_lat_izqudo')
rightView.Caption='ALZADO LATERAL IZQUIERDO. ESCALA '+txtEscAlzados
rightView.Direction = shp.struct.getVectLeftView() 
#rightView.Scale=escalaAlzados*1000
rc = docViews.addView(rightView)
rightView.Source= elemRVw
rightView.HardHidden=False
rc = docViews.addView(rightView)





#TechDraw.writeDXFPage(docViews,path+gd.obraNm+'vistas.dxf')



