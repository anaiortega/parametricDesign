# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math, TechDraw, FreeCADGui
from FreeCAD import Base

def prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura):
    # Devuelve un prisma en un sistema de coordenadas general, definido por:
    # vOrigenL: vector que define el pto. origen del sistema de coordenadas local
    # vDirXL: vector en la dirección X del SC local
    # vDirYL: vector en la dirección Y del SC local
    # vDirZL: vector en la dirección Z del SC local
    # listaCoordL: ptos. ordenados para definir la base del prisma (que estará contenida en el plano XY local). Las coordenadas de estos ptos. se dan en el SC local en la forma: [[x1,y1],[x2,y2],[x3,y3],...].
    # altura: altura del prisma (en dirección vDirZL)
    vDirXL.normalize() #vector de dirección X local
    vDirYL.normalize() #vector de dirección Y local
    vDirZL.normalize() #vector de dirección Z local
    vertPolig=[]
    for i in range(0,len(listaCoordL)):
        vuX=Base.Vector(vDirXL.x,vDirXL.y,vDirXL.z)
        vuY=Base.Vector(vDirYL.x,vDirYL.y,vDirYL.z)
        vertice=vOrigenL.add(vuX.multiply(listaCoordL[i][0])).add(vuY.multiply(listaCoordL[i][1]))
        vertPolig.append(vertice)
    vertice=vertPolig[0]
    vertPolig.append(vertice)
    base=Part.Face(Part.makePolygon(vertPolig))
    prisma=base.extrude(vDirZL.multiply(altura))
    return prisma

def conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura,tol=1e-5):
    # Devuelve un conjunto de cilindros en un sistema de coordenadas general, definido por:
    # vOrigenL: vector que define el pto. origen del sistema de coordenadas local
    # vDirXL: vector en la dirección X del SC local
    # vDirYL: vector en la dirección Y del SC local
    # vDirZL: vector en la dirección Z del SC local
    # listaCoordCentrosL: ptos. en los centros de la base de los cilindros (que estarán contenidas en el plano XY local). Las coordenadas de estos ptos. se dan en el SC local en la forma: [[x1,y1],[x2,y2],[x3,y3],...].
    # diametro: diámetro de los cilindros.
    # altura: altura de los cilindros (en dirección vDirZL)
    vDirXL.normalize() #vector de dirección X local
    vDirYL.normalize() #vector de dirección Y local
    vDirZL.normalize() #vector de dirección Z local
    for i in range(0,len(listaCoordCentrosL)):
        vuX=Base.Vector(vDirXL.x,vDirXL.y,vDirXL.z)
        vuY=Base.Vector(vDirYL.x,vDirYL.y,vDirYL.z)
        centro=vOrigenL.add(vuX.multiply(listaCoordCentrosL[i][0])).add(vuY.multiply(listaCoordCentrosL[i][1]))
        cil=Part.makeCylinder(diametro/2.0,altura,centro,vDirZL)
        if abs(i) < tol:
            conjCilind=cil
        else:
            conjCilind=conjCilind.fuse(cil)
    return conjCilind

def simXYPto(pto):
    #Devuelve el pto. simétrico del dado respecto al plano XY
    ptoSim=Base.Vector(pto.x,pto.y,-pto.z)
    return ptoSim

def simXZPto(pto):
    #Devuelve el pto. simétrico del dado respecto al plano XZ
    ptoSim=Base.Vector(pto.x,-pto.y,pto.z)
    return ptoSim

def simYZPto(pto):
    #Devuelve el pto. simétrico del dado respecto al plano YZ
    ptoSim=Base.Vector(-pto.x,pto.y,pto.z)
    return ptoSim

def simXYlistaCoord(listaCoord):
    #Devuelve otra lista de coordenadas simétricas de las dadas respecto al plano XY
    listaSim=[0]*len(listaCoord)       #creamos una lista inicial
    for i in range(0,len(listaCoord)):
        listaSim[i]=listaCoord[i][:]
        listaSim[i][2]=-listaSim[i][2]
    return listaSim

def simXZlistaCoord(listaCoord):
    #Devuelve otra lista de coordenadas simétricas de las dadas respecto al plano XZ
    listaSim=[0]*len(listaCoord)       #creamos una lista inicial
    for i in range(0,len(listaCoord)):
        listaSim[i]=listaCoord[i][:]
        listaSim[i][1]=-listaSim[i][1]
    return listaSim

def simYZlistaCoord(listaCoord):
    #Devuelve otra lista de coordenadas simétricas de las dadas respecto al plano YZ
    listaSim=[0]*len(listaCoord)       #creamos una lista inicial
    for i in range(0,len(listaCoord)):
        listaSim[i]=listaCoord[i][:]
        listaSim[i][0]=-listaSim[i][0]
    return listaSim

def vistasIsom(App,escala,Pieza):
#Perspectiva isométrica. Vista anterosuperior
#    App.ActiveDocument().addObject('TechDraw::FeaturePage','IsoAnterosup')
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoAnterosup')
#    App.ActiveDocument().IsoAnterosup.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoAsup')
    App.ActiveDocument.IsoAsup.Source =Pieza
    App.ActiveDocument.IsoAsup.Direction = (1,1,1)
    App.ActiveDocument.IsoAsup.Rotation=60
    App.ActiveDocument.IsoAsup.Scale = escala
    App.ActiveDocument.IsoAsup.X = 700
    App.ActiveDocument.IsoAsup.Y = 600
#    App.ActiveDocument.IsoAsup.ShowHiddenLines=False
    App.ActiveDocument.IsoAnterosup.addObject(App.ActiveDocument.IsoAsup)
    App.ActiveDocument.recompute()
#Perspectiva isométrica. Vista posteroinferior
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoPosteroinf')
    App.ActiveDocument.IsoPosteroinf.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoPinf')
    App.ActiveDocument.IsoPinf.Source =Pieza
    App.ActiveDocument.IsoPinf.Direction = (-1,-1,-1)
    App.ActiveDocument.IsoPinf.Rotation=300
    App.ActiveDocument.IsoPinf.Scale = escala
    App.ActiveDocument.IsoPinf.X = 700
    App.ActiveDocument.IsoPinf.Y = 600
    App.ActiveDocument.IsoPinf.ShowHiddenLines=False
    App.ActiveDocument.IsoPosteroinf.addObject(App.ActiveDocument.IsoPinf)
    App.ActiveDocument.recompute()
    return

def vistaIsoAnterosup(App,escala,Pieza):
#Perspectiva isométrica. Vista anterosuperior
    IsoAnterosup=App.ActiveDocument.addObject('TechDraw::DrawPage','IsoAnterosup')
    template = FreeCAD.ActiveDocument.addObject('TechDraw::DrawSVGTemplate','Template')
    template.Template=App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    IsoAnterosup.Template = FreeCAD.ActiveDocument.Template
#    App.ActiveDocument.IsoAnterosup.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoAsup')
    App.ActiveDocument.IsoAsup.Source =Pieza
    App.ActiveDocument.IsoAsup.Direction = (1,1,1)
    App.ActiveDocument.IsoAsup.Rotation=60
    App.ActiveDocument.IsoAsup.Scale = escala
    App.ActiveDocument.IsoAsup.X = 700
    App.ActiveDocument.IsoAsup.Y = 600
#    App.ActiveDocument.IsoAsup.ShowHiddenLines=False
    App.ActiveDocument.IsoAnterosup.addObject(App.ActiveDocument.IsoAsup)
    App.ActiveDocument.recompute()
    return
def vistaIsoAnteroinf(App,escala,Pieza):
#Perspectiva isométrica. Vista anteroinferior
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoAnteroinf')
    App.ActiveDocument.IsoAnteroinf.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoAinf')
    App.ActiveDocument.IsoAinf.Source =Pieza
    App.ActiveDocument.IsoAinf.Direction = (1,-1,-1)
    App.ActiveDocument.IsoAinf.Rotation=60
    App.ActiveDocument.IsoAinf.Scale = escala
    App.ActiveDocument.IsoAinf.X = 700
    App.ActiveDocument.IsoAinf.Y = 600
    App.ActiveDocument.IsoAinf.ShowHiddenLines=False
    App.ActiveDocument.IsoAnteroinf.addObject(App.ActiveDocument.IsoAinf)
    App.ActiveDocument.recompute()
    return
#
def vistaIsoPosterosup(App,escala,Pieza):
#Perspectiva isométrica. Vista posteroinferior
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoPosterosup')
    App.ActiveDocument.IsoPosterosup.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoPsup')
    App.ActiveDocument.IsoPsup.Source =Pieza
    App.ActiveDocument.IsoPsup.Direction = (-1,1,1)
    App.ActiveDocument.IsoPsup.Rotation=300
    App.ActiveDocument.IsoPsup.Scale = escala
    App.ActiveDocument.IsoPsup.X = 700
    App.ActiveDocument.IsoPsup.Y = 600
    App.ActiveDocument.IsoPsup.ShowHiddenLines=False
    App.ActiveDocument.IsoPosterosup.addObject(App.ActiveDocument.IsoPsup)
    App.ActiveDocument.recompute()
    return

def vistaIsoPosteroinf(App,escala,Pieza):
#Perspectiva isométrica. Vista posteroinferior
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoPosteroinf')
    App.ActiveDocument.IsoPosteroinf.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoPinf')
    App.ActiveDocument.IsoPinf.Source =Pieza
    App.ActiveDocument.IsoPinf.Direction = (-1,-1,-1)
    App.ActiveDocument.IsoPinf.Rotation=300
    App.ActiveDocument.IsoPinf.Scale = escala
    App.ActiveDocument.IsoPinf.X = 700
    App.ActiveDocument.IsoPinf.Y = 600
    App.ActiveDocument.IsoPinf.ShowHiddenLines=False
    App.ActiveDocument.IsoPosteroinf.addObject(App.ActiveDocument.IsoPinf)
    App.ActiveDocument.recompute()
    return

def vistaIsoGeneral(App,escala,Pieza,vectorDir,angulo):
#Perspectiva isométrica. Vista general según la dirección vectorDir
    App.ActiveDocument.addObject('TechDraw::DrawPage','IsoGeneral')
    App.ActiveDocument.IsoGeneral.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','IsoPinf')
    App.ActiveDocument.IsoPinf.Source =Pieza
    App.ActiveDocument.IsoPinf.Direction = vectorDir
    App.ActiveDocument.IsoPinf.Rotation=angulo
    App.ActiveDocument.IsoPinf.Scale = escala
    App.ActiveDocument.IsoPinf.X = 700
    App.ActiveDocument.IsoPinf.Y = 600
    App.ActiveDocument.IsoPinf.ShowHiddenLines=False
    App.ActiveDocument.IsoGeneral.addObject(App.ActiveDocument.IsoPinf)
    App.ActiveDocument.recompute()
    return

def vistaPlanta(App,escala,Pieza,ocultas,SupInf):
#Planta
    App.ActiveDocument.addObject('TechDraw::DrawPage','Planta')
    App.ActiveDocument.Planta.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','topView')
    App.ActiveDocument.topView.Source =Pieza
    if SupInf == 'Sup':
        App.ActiveDocument.topView.Direction = (0,0,1)
        App.ActiveDocument.topView.Rotation=90
    else:
        App.ActiveDocument.topView.Direction = (0,0,-1)
        App.ActiveDocument.topView.Rotation=0
    App.ActiveDocument.topView.Scale = escala
    App.ActiveDocument.topView.X = 700 
    App.ActiveDocument.topView.Y = 500 
    if ocultas == 's':
        App.ActiveDocument.topView.ShowHiddenLines=True
    else:
        App.ActiveDocument.topView.ShowHiddenLines=False
    App.ActiveDocument.Planta.addObject(App.ActiveDocument.topView)
    App.ActiveDocument.recompute()
    return

def vistaFront(App,escala,Pieza,ocultas,AntPost):
#Alzado frontal
    App.ActiveDocument.addObject('TechDraw::DrawPage','AlzadoFrontal')
    App.ActiveDocument.AlzadoFrontal.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','FrontView')
    App.ActiveDocument.FrontView.Source =Pieza
    if AntPost == 'Ant':
        App.ActiveDocument.FrontView.Direction = (1,0,0)
        App.ActiveDocument.FrontView.Rotation=270
    else:
        App.ActiveDocument.FrontView.Direction = (-1,0,0)
        App.ActiveDocument.FrontView.Rotation=90
    App.ActiveDocument.FrontView.Scale = escala
    App.ActiveDocument.FrontView.X = 700 
    App.ActiveDocument.FrontView.Y = 700 
    if ocultas == 's':
        App.ActiveDocument.FrontView.ShowHiddenLines=True
    else:
        App.ActiveDocument.FrontView.ShowHiddenLines=False
    App.ActiveDocument.AlzadoFrontal.addObject(App.ActiveDocument.FrontView)
    App.ActiveDocument.recompute()
    return

def vistaLat(App,escala,Pieza,ocultas,IzqDer):
#Alzado lateral
    App.ActiveDocument.addObject('TechDraw::DrawPage','AlzadoLateral')
    App.ActiveDocument.AlzadoLateral.Template = App.getResourceDir()+'Mod/TechDraw/Templates/A3_Landscape_blank.svg'
    App.ActiveDocument.addObject('TechDraw::DrawViewPart','RightView')
    App.ActiveDocument.RightView.Source =Pieza
    if IzqDer == 'Izq':
        App.ActiveDocument.RightView.Direction = (0,1,0)
        App.ActiveDocument.RightView.Rotation=270
    else:
        App.ActiveDocument.RightView.Direction = (0,-1,0)
        App.ActiveDocument.RightView.Rotation=90
    App.ActiveDocument.RightView.Scale = escala
    App.ActiveDocument.RightView.X = 700 
    App.ActiveDocument.RightView.Y = 700 
    if ocultas == 's':
        App.ActiveDocument.RightView.ShowHiddenLines=True
    else:
        App.ActiveDocument.RightView.ShowHiddenLines=False
    App.ActiveDocument.AlzadoLateral.addObject(App.ActiveDocument.RightView)
    App.ActiveDocument.recompute()
    return
