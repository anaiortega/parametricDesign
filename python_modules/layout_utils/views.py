import TechDraw

def basic_views(docGeom,title,lstObjects,scale=None,pageTemplate='A1_Landscape_blank.svg'):
    ''' Generate top, bottom. front, back, left and right views of the objects listed
    in lstObjects that are in document  docGeom.

    :param docGeom: document where the objects are.
    :param title: title to name the page of views
    :param lstObjects: list of type [docGeom.objname] with the objects to render 
                in views. (objname is the name given to the object  when it's shown 
               in document docGeom: Part.show(object,objname)
    :param scale: scale to apply to views (defaults to None => 1:1)
    :param Template: page Template chosen from those in directory /usr/share/freecad-daily/Mod/TechDraw/Templates/ . Defaults to A1_Landscape_blank.svg
    '''
    docViews = docGeom.addObject('TechDraw::DrawPage',title+'_views')
    template = docGeom.addObject('TechDraw::DrawSVGTemplate','Template')
    template.Template = '/usr/share/freecad-daily/Mod/TechDraw/Templates/'+pageTemplate
    docViews.Template = docGeom.Template
    
    topView = docGeom.addObject('TechDraw::DrawViewPart', 'top_view')
    topView.Source = lstObjects
    topView.Caption='TOP VIEW'
    if scale:
        topView.ScaleType = u"Custom"
        topView.Scale=scale
        topView.Caption+='. Scale: '+ str(scale)
    topView.Direction = (0.0, 0.0, 1.0)
#    topView.Rotation=str(round(angRot,2))+' deg'
#    topView.Source= lstObjects
    topView.HardHidden=False
    rc = docViews.addView(topView)

    bottomView=docGeom.addObject('TechDraw::DrawViewPart', 'bottom_view')
    bottomView.Caption='BOTTOM VIEW'
    bottomView.Direction = (0.0, 0.0, -1.0)
    bottomView.Source= lstObjects
    bottomView.HardHidden=False
    if scale:
        bottomView.ScaleType = u"Custom"
        bottomView.Scale=scale
        bottomView.Caption+='. Scale: '+ str(scale)
    rc = docViews.addView(bottomView)

    frontView=docGeom.addObject('TechDraw::DrawViewPart', 'front_view')
    frontView.Caption='FRONT VIEW'
    frontView.Direction = (1.0, 0.0, 0.0)
    #frontView.Scale=escalaAlzados*1000
    frontView.Source= lstObjects
    frontView.HardHidden=False
    if scale:
        frontView.ScaleType = u"Custom"
        frontView.Scale=scale
        frontView.Caption+='. Scale: '+ str(scale)
    rc = docViews.addView(frontView)

    backView=docGeom.addObject('TechDraw::DrawViewPart', 'back_view')
    backView.Caption='BACK VIEW'
    backView.Direction = (-1.0, 0.0, 0.0)
    #backView.Scale=escalaAlzados*1000
    backView.Source= lstObjects
    backView.HardHidden=False
    if scale:
        backView.ScaleType = u"Custom"
        backView.Scale=scale
        backView.Caption+='. Scale: '+ str(scale)
    rc = docViews.addView(backView)

    leftView=docGeom.addObject('TechDraw::DrawViewPart', 'left_view')
    leftView.Caption='LEFT VIEW'
    leftView.Direction = (0.0,-1.0,0.0)
    #leftView.Scale=escalaAlzados*1000
    rc = docViews.addView(leftView)
    leftView.Source= lstObjects
    leftView.HardHidden=False
    if scale:
        leftView.ScaleType = u"Custom"
        leftView.Scale=scale
        leftView.Caption+='. Scale: '+ str(scale)
    rc = docViews.addView(leftView)

    rightView=docGeom.addObject('TechDraw::DrawViewPart', 'right_view')
    rightView.Caption='RIGHT VIEW'
    rightView.Direction =(0.0,1.0,0.0)
    #rightView.Scale=escalaAlzados*1000
    rc = docViews.addView(rightView)
    rightView.Source= lstObjects
    rightView.HardHidden=False
    if scale:
        rightView.ScaleType = u"Custom"
        rightView.Scale=scale
        rightView.Caption+='. Scale: '+ str(scale)
    rc = docViews.addView(rightView)


    
