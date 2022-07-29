escala=0.05    #escala para generar planos


#Vistas de toda la estructura
FreeCADGui.Selection.addSelection(Todo)
#Perspectiva isométrica
App.activeDocument().addObject('Drawing::FeaturePage','TIsometrica')
App.activeDocument().TIsometrica.Template = App.getResourceDir()+'Mod/Drawing/Templates/A1_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','IsoView')
App.activeDocument().IsoView.Source =Todo
App.activeDocument().IsoView.Direction = (1,1,1)
App.activeDocument().IsoView.Rotation=60
App.activeDocument().IsoView.Scale = escala
App.activeDocument().IsoView.X = 400
App.activeDocument().IsoView.Y = 500
App.activeDocument().IsoView.ShowHiddenLines=False
App.activeDocument().TIsometrica.addObject(App.activeDocument().IsoView)
App.activeDocument().recompute()
#Planta
App.activeDocument().addObject('Drawing::FeaturePage','TPlanta')
App.activeDocument().TPlanta.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
App.activeDocument().topView.Source =Todo
App.activeDocument().topView.Direction = (0,0,1)
App.activeDocument().topView.Rotation=0
App.activeDocument().topView.Scale = escala
App.activeDocument().topView.X = 100 
App.activeDocument().topView.Y = 500 
App.activeDocument().topView.ShowHiddenLines=False
App.activeDocument().TPlanta.addObject(App.activeDocument().topView)
App.activeDocument().recompute()

#Alzado frontal
App.activeDocument().addObject('Drawing::FeaturePage','TAlzadoFrontal')
App.activeDocument().TAlzadoFrontal.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','FrontView')
App.activeDocument().FrontView.Source =Todo
App.activeDocument().FrontView.Direction = (1,0,0)
App.activeDocument().FrontView.Rotation=-90
App.activeDocument().FrontView.Scale = escala
App.activeDocument().FrontView.X = 700 
App.activeDocument().FrontView.Y = 800 
App.activeDocument().FrontView.ShowHiddenLines=False
App.activeDocument().TAlzadoFrontal.addObject(App.activeDocument().FrontView)
App.activeDocument().recompute()

#Alzado lateral
App.activeDocument().addObject('Drawing::FeaturePage','TAlzadoLateral')
App.activeDocument().TAlzadoLateral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','RightView')
App.activeDocument().RightView.Source =Todo
App.activeDocument().RightView.Direction = (0,1,0)
App.activeDocument().RightView.Rotation=-90
App.activeDocument().RightView.Scale = escala
App.activeDocument().RightView.X = 100 
App.activeDocument().RightView.Y = 800 
App.activeDocument().RightView.ShowHiddenLines=False
App.activeDocument().TAlzadoLateral.addObject(App.activeDocument().RightView)
App.activeDocument().recompute()

FreeCADGui.Selection.removeSelection(Todo)

##########
#Vistas de un pilar intermedio (y lo que le rodea)
FreeCADGui.Selection.addSelection(PilarIntermedio)
#Perspectiva isométrica
App.activeDocument().addObject('Drawing::FeaturePage','PIIsometrica')
App.activeDocument().PIIsometrica.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','IsoView')
App.activeDocument().IsoView.Source =PilarIntermedio
App.activeDocument().IsoView.Direction = (1,1,1)
App.activeDocument().IsoView.Rotation=60
App.activeDocument().IsoView.Scale = escala
App.activeDocument().IsoView.X = 50
App.activeDocument().IsoView.Y = 800
App.activeDocument().IsoView.ShowHiddenLines=False
App.activeDocument().PIIsometrica.addObject(App.activeDocument().IsoView)
App.activeDocument().recompute()
#Planta
App.activeDocument().addObject('Drawing::FeaturePage','PIPlanta')
App.activeDocument().PIPlanta.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
App.activeDocument().topView.Source =PilarIntermedio
App.activeDocument().topView.Direction = (0,0,1)
App.activeDocument().topView.Rotation=0
App.activeDocument().topView.Scale = escala
App.activeDocument().topView.X = 100 
App.activeDocument().topView.Y = 800 
App.activeDocument().topView.ShowHiddenLines=False
App.activeDocument().PIPlanta.addObject(App.activeDocument().topView)
App.activeDocument().recompute()

#Alzado frontal
App.activeDocument().addObject('Drawing::FeaturePage','PIAlzadoFrontal')
App.activeDocument().PIAlzadoFrontal.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','FrontView')
App.activeDocument().FrontView.Source =PilarIntermedio
App.activeDocument().FrontView.Direction = (1,0,0)
App.activeDocument().FrontView.Rotation=-90
App.activeDocument().FrontView.Scale = escala
App.activeDocument().FrontView.X = 100 
App.activeDocument().FrontView.Y = 800 
App.activeDocument().FrontView.ShowHiddenLines=True
App.activeDocument().PIAlzadoFrontal.addObject(App.activeDocument().FrontView)
App.activeDocument().recompute()

#Alzado lateral
App.activeDocument().addObject('Drawing::FeaturePage','PIAlzadoLateral')
App.activeDocument().PIAlzadoLateral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','RightView')
App.activeDocument().RightView.Source =PilarIntermedio
App.activeDocument().RightView.Direction = (0,-1,0)
App.activeDocument().RightView.Rotation=90
App.activeDocument().RightView.Scale = escala
App.activeDocument().RightView.X = 700
App.activeDocument().RightView.Y = 700
App.activeDocument().RightView.ShowHiddenLines=False 
App.activeDocument().PIAlzadoLateral.addObject(App.activeDocument().RightView)
App.activeDocument().recompute()

FreeCADGui.Selection.removeSelection(PilarIntermedio)


##########
#Vistas de un pilar de esquina (y lo que le rodea)
FreeCADGui.Selection.addSelection(PilarEsquina)
#Perspectiva isométrica
App.activeDocument().addObject('Drawing::FeaturePage','PEIsometrica')
App.activeDocument().PEIsometrica.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','IsoView')
App.activeDocument().IsoView.Source =PilarEsquina
App.activeDocument().IsoView.Direction = (1,1,1)
App.activeDocument().IsoView.Rotation=60
App.activeDocument().IsoView.Scale = escala
App.activeDocument().IsoView.X = 0
App.activeDocument().IsoView.Y = 400
App.activeDocument().IsoView.ShowHiddenLines=False
App.activeDocument().PEIsometrica.addObject(App.activeDocument().IsoView)
App.activeDocument().recompute()
#Planta
App.activeDocument().addObject('Drawing::FeaturePage','PEPlanta')
App.activeDocument().PEPlanta.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
App.activeDocument().topView.Source =PilarEsquina
App.activeDocument().topView.Direction = (0,0,1)
App.activeDocument().topView.Rotation=0
App.activeDocument().topView.Scale = escala
App.activeDocument().topView.X = -500
App.activeDocument().topView.Y = 700 
App.activeDocument().topView.ShowHiddenLines=False
App.activeDocument().PEPlanta.addObject(App.activeDocument().topView)
App.activeDocument().recompute()

#Alzado frontal
App.activeDocument().addObject('Drawing::FeaturePage','PEAlzadoFrontal')
App.activeDocument().PEAlzadoFrontal.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','FrontView')
App.activeDocument().FrontView.Source =PilarEsquina
App.activeDocument().FrontView.Direction = (1,0,0)
App.activeDocument().FrontView.Rotation=-90
App.activeDocument().FrontView.Scale = escala
App.activeDocument().FrontView.X = 100 
App.activeDocument().FrontView.Y = 800 
App.activeDocument().FrontView.ShowHiddenLines=False
App.activeDocument().PEAlzadoFrontal.addObject(App.activeDocument().FrontView)
App.activeDocument().recompute()

#Alzado lateral
App.activeDocument().addObject('Drawing::FeaturePage','PEAlzadoLateral')
App.activeDocument().PEAlzadoLateral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A1_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','RightView')
App.activeDocument().RightView.Source =PilarEsquina
App.activeDocument().RightView.Direction = (0,-1,0)
App.activeDocument().RightView.Rotation=0
App.activeDocument().RightView.Scale = escala
App.activeDocument().RightView.X = -500
App.activeDocument().RightView.Y = -500
App.activeDocument().RightView.ShowHiddenLines=False
App.activeDocument().PEAlzadoLateral.addObject(App.activeDocument().RightView)
App.activeDocument().recompute()

FreeCADGui.Selection.removeSelection(PilarEsquina)

##########
#Vistas de cumbrera
FreeCADGui.Selection.addSelection(Cumbrera)
#Perspectiva isométrica
App.activeDocument().addObject('Drawing::FeaturePage','CUIsometrica')
App.activeDocument().CUIsometrica.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','IsoView')
App.activeDocument().IsoView.Source =Cumbrera
App.activeDocument().IsoView.Direction = (1,1,1)
App.activeDocument().IsoView.Rotation=60
App.activeDocument().IsoView.Scale = escala
App.activeDocument().IsoView.X = 0
App.activeDocument().IsoView.Y = 400
App.activeDocument().IsoView.ShowHiddenLines=False
App.activeDocument().CUIsometrica.addObject(App.activeDocument().IsoView)
App.activeDocument().recompute()
#Planta
App.activeDocument().addObject('Drawing::FeaturePage','CUPlanta')
App.activeDocument().CUPlanta.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
App.activeDocument().topView.Source =Cumbrera
App.activeDocument().topView.Direction = (0,0,-1)
App.activeDocument().topView.Rotation=0
App.activeDocument().topView.Scale = escala
App.activeDocument().topView.X = -500
App.activeDocument().topView.Y = 700 
App.activeDocument().topView.ShowHiddenLines=False
App.activeDocument().CUPlanta.addObject(App.activeDocument().topView)
App.activeDocument().recompute()

#Alzado frontal
App.activeDocument().addObject('Drawing::FeaturePage','CUAlzadoFrontal')
App.activeDocument().CUAlzadoFrontal.Template = App.getResourceDir()+'Mod/Drawing/Templates/A4_vertical.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','FrontView')
App.activeDocument().FrontView.Source =Cumbrera
App.activeDocument().FrontView.Direction = (1,0,0)
App.activeDocument().FrontView.Rotation=-90
App.activeDocument().FrontView.Scale = escala
App.activeDocument().FrontView.X = 100 
App.activeDocument().FrontView.Y = 800 
App.activeDocument().FrontView.ShowHiddenLines=False
App.activeDocument().CUAlzadoFrontal.addObject(App.activeDocument().FrontView)
App.activeDocument().recompute()

#Alzado lateral
App.activeDocument().addObject('Drawing::FeaturePage','CUAlzadoLateral')
App.activeDocument().CUAlzadoLateral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A1_apaisado.svg'
App.activeDocument().addObject('Drawing::FeatureViewPart','RightView')
App.activeDocument().RightView.Source =Cumbrera
App.activeDocument().RightView.Direction = (0,-1,0)
App.activeDocument().RightView.Rotation=0
App.activeDocument().RightView.Scale = escala
App.activeDocument().RightView.X = -500
App.activeDocument().RightView.Y = -500
App.activeDocument().RightView.ShowHiddenLines=False
App.activeDocument().CUAlzadoLateral.addObject(App.activeDocument().RightView)
App.activeDocument().recompute()

FreeCADGui.Selection.removeSelection(Cumbrera)
