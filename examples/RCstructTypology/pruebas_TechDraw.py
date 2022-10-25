
allElem=[doc.deck,doc.leftWall,doc.rightWall,doc.pilesLeft,doc.pilesRight,doc.initHeadWall,doc.endHeadWall,doc.wwIL,doc.footIL,doc.wwIR,doc.footIR,doc.wwEL,doc.footEL,doc.wwER,doc.footER]
elemFVw=[doc.deck,doc.leftWall,doc.rightWall,doc.initHeadWall,doc.endHeadWall,doc.wwIL,doc.footIL,doc.wwIR,doc.footIR] # front view
elemDVw=[doc.deck,doc.leftWall,doc.rightWall,doc.initHeadWall,doc.endHeadWall,doc.wwEL,doc.footEL,doc.wwER,doc.footER] # dorsal view

page = doc.addObject('TechDraw::DrawPage','page')
template = doc.addObject('TechDraw::DrawSVGTemplate','Template')
template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/A1_Landscape_blank.svg'
page.Template = doc.Template
topView = doc.addObject('TechDraw::DrawViewPart', 'View')
doc.View.Source = allElem
topView.Caption='Top view'
topView.ScaleType = u"Custom"
topView.Scale=10
topView.Direction = (0.0, 0.0, 1.0)
angAxis=math.degrees(struct.getVectDorsalView().getAngle(Vector(1,0,0)))
angRot=360-angAxis
topView.Rotation=str(round(angRot,2))+' deg'
topView.Source= allElem
topView.HardHidden=True
rc = page.addView(topView)

frontView=doc.addObject('TechDraw::DrawViewPart', 'View')
frontView.Caption='Front view'
frontView.Direction = struct.getVectFrontalView() #(-1.0, 0.0, 0.0)
frontView.Scale=10
rc = page.addView(frontView)
frontView.Source= elemFVw
frontView.HardHidden=False
rc = page.addView(frontView)

dorsView=doc.addObject('TechDraw::DrawViewPart', 'View')
dorsView.Caption='Back view'
dorsView.Direction = struct.getVectDorsalView() #(-1.0, 0.0, 0.0)
dorsView.Scale=10
rc = page.addView(dorsView)
dorsView.Source= elemDVw
dorsView.HardHidden=False
rc = page.addView(dorsView)

leftView=doc.addObject('TechDraw::DrawViewPart', 'View')
leftView.Caption='Left view'
leftView.Direction = struct.getVectLeftView() 
leftView.Scale=10
rc = page.addView(leftView)
leftView.Source= allElem
leftView.HardHidden=False
rc = page.addView(leftView)

rightView=doc.addObject('TechDraw::DrawViewPart', 'View')
rightView.Caption='Right view'
rightView.Direction = struct.getVectRightView() 
rightView.Scale=10
rc = page.addView(rightView)
rightView.Source= allElem
rightView.HardHidden=False
rc = page.addView(rightView)





#TechDraw.writeDXFPage(page,filename)



