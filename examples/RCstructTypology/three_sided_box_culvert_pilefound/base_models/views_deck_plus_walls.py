import TechDraw

escalaPlanta=1 ; txtEscPlanta='1:1'
escalaAlzados=1 ; txtEscAlzados='1:1'
# Todos los elementos excepto pilotes
elemNoPile=[docGeom.deck]
elemNoPile+=[docGeom.initHeadWall,docGeom.endHeadWall]
elemNoPile+=[docGeom.leftWall,docGeom.rightWall]
listWingWallObj=docGeom.findObjects(Name='ww*')
listWingWallNames=[o.Label for o in listWingWallObj]

if 'wwEL' in listWingWallNames:
    print('added wingwall EL')
    elemNoPile+=[docGeom.wwEL,docGeom.footEL,docGeom.chamferEL]
    

if 'wwIL' in listWingWallNames:
    print('added wingwall IL')
    elemNoPile+=[docGeom.wwIL,docGeom.footIL,docGeom.chamferIL]

    
if 'wwIR' in listWingWallNames:
    print('added wingwall IR')
    elemNoPile+=[docGeom.wwIR,docGeom.footIR,docGeom.chamferIR]
    

if 'wwER' in listWingWallNames:
    print('added wingwall ER')
    elemNoPile+=[docGeom.wwER,docGeom.footER,docGeom.chamferER]

#Planta
allElem=elemNoPile+[docGeom.pilesLeft,docGeom.pilesRight]
#Left view
elemLVw=elemNoPile
#Right view
elemRVw=elemNoPile
#Front view
elemFVw=elemNoPile
#Dorsal view
elemDVw=elemNoPile

docViews = docGeom.addObject('TechDraw::DrawPage',gd.obraNm+'_vistas')
template = docGeom.addObject('TechDraw::DrawSVGTemplate','Template')
template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/A4_Landscape_blank.svg'
docViews.Template = docGeom.Template
topView = docGeom.addObject('TechDraw::DrawViewPart', 'Planta')
topView.Source = allElem
topView.Caption='PLANTA. ESCALA '+txtEscPlanta
#topView.ScaleType = u"Custom"
#topView.Scale=escalaPlanta*1000
topView.Direction = (0.0, 0.0, 1.0)
angAxis=math.degrees(struct.getVectDorsalView().getAngle(Vector(1,0,0)))
angRot=360-angAxis
topView.Rotation=str(round(angRot,2))+' deg'
topView.Source= allElem
topView.HardHidden=True
rc = docViews.addView(topView)

frontView=docGeom.addObject('TechDraw::DrawViewPart', 'vista_frontal')
frontView.Caption='ALZADO FRONTAL. ESCALA '+txtEscAlzados
frontView.Direction = struct.getVectFrontalView() #(-1.0, 0.0, 0.0)
#frontView.Scale=escalaAlzados*1000
rc = docViews.addView(frontView)
frontView.Source= elemFVw
frontView.HardHidden=False
rc = docViews.addView(frontView)

dorsView=docGeom.addObject('TechDraw::DrawViewPart', 'vista_dorsal')
dorsView.Caption='ALZADO DORSAL. ESCALA '+txtEscAlzados
dorsView.Direction = struct.getVectDorsalView() #(-1.0, 0.0, 0.0)
#dorsView.Scale=escalaAlzados*1000
rc = docViews.addView(dorsView)
dorsView.Source= elemDVw
dorsView.HardHidden=False
rc = docViews.addView(dorsView)

leftView=docGeom.addObject('TechDraw::DrawViewPart', 'vista_lat_drcho')
leftView.Caption='ALZADO LATERAL DERECHO. ESCALA '+txtEscAlzados
leftView.Direction = struct.getVectRightView() 
#leftView.Scale=escalaAlzados*1000
rc = docViews.addView(leftView)
leftView.Source= elemLVw
leftView.HardHidden=False
rc = docViews.addView(leftView)

rightView=docGeom.addObject('TechDraw::DrawViewPart', 'vista_lat_izqudo')
rightView.Caption='ALZADO LATERAL IZQUIERDO. ESCALA '+txtEscAlzados
rightView.Direction = struct.getVectLeftView() 
#rightView.Scale=escalaAlzados*1000
rc = docViews.addView(rightView)
rightView.Source= elemRVw
rightView.HardHidden=False
rc = docViews.addView(rightView)





#TechDraw.writeDXFPage(docViews,path+gd.obraNm+'vistas.dxf')



