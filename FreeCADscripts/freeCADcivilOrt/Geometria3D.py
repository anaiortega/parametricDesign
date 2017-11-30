# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math, Drawing, FreeCADGui
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

def conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura):
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
        if i == 0:
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
    App.activeDocument().addObject('Drawing::FeaturePage','IsoAnterosup')
    App.activeDocument().IsoAnterosup.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoAsup')
    App.activeDocument().IsoAsup.Source =Pieza
    App.activeDocument().IsoAsup.Direction = (1,1,1)
    App.activeDocument().IsoAsup.Rotation=60
    App.activeDocument().IsoAsup.Scale = escala
    App.activeDocument().IsoAsup.X = 700
    App.activeDocument().IsoAsup.Y = 600
    App.activeDocument().IsoAsup.ShowHiddenLines=False
    App.activeDocument().IsoAnterosup.addObject(App.activeDocument().IsoAsup)
    App.activeDocument().recompute()
#Perspectiva isométrica. Vista posteroinferior
    App.activeDocument().addObject('Drawing::FeaturePage','IsoPosteroinf')
    App.activeDocument().IsoPosteroinf.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoPinf')
    App.activeDocument().IsoPinf.Source =Pieza
    App.activeDocument().IsoPinf.Direction = (-1,-1,-1)
    App.activeDocument().IsoPinf.Rotation=300
    App.activeDocument().IsoPinf.Scale = escala
    App.activeDocument().IsoPinf.X = 700
    App.activeDocument().IsoPinf.Y = 600
    App.activeDocument().IsoPinf.ShowHiddenLines=False
    App.activeDocument().IsoPosteroinf.addObject(App.activeDocument().IsoPinf)
    App.activeDocument().recompute()
    return

def vistaIsoAnterosup(App,escala,Pieza):
#Perspectiva isométrica. Vista anterosuperior
    App.activeDocument().addObject('Drawing::FeaturePage','IsoAnterosup')
    App.activeDocument().IsoAnterosup.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoAsup')
    App.activeDocument().IsoAsup.Source =Pieza
    App.activeDocument().IsoAsup.Direction = (1,1,1)
    App.activeDocument().IsoAsup.Rotation=60
    App.activeDocument().IsoAsup.Scale = escala
    App.activeDocument().IsoAsup.X = 700
    App.activeDocument().IsoAsup.Y = 600
    App.activeDocument().IsoAsup.ShowHiddenLines=False
    App.activeDocument().IsoAnterosup.addObject(App.activeDocument().IsoAsup)
    App.activeDocument().recompute()
    return
def vistaIsoAnteroinf(App,escala,Pieza):
#Perspectiva isométrica. Vista anteroinferior
    App.activeDocument().addObject('Drawing::FeaturePage','IsoAnteroinf')
    App.activeDocument().IsoAnteroinf.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoAinf')
    App.activeDocument().IsoAinf.Source =Pieza
    App.activeDocument().IsoAinf.Direction = (1,-1,-1)
    App.activeDocument().IsoAinf.Rotation=60
    App.activeDocument().IsoAinf.Scale = escala
    App.activeDocument().IsoAinf.X = 700
    App.activeDocument().IsoAinf.Y = 600
    App.activeDocument().IsoAinf.ShowHiddenLines=False
    App.activeDocument().IsoAnteroinf.addObject(App.activeDocument().IsoAinf)
    App.activeDocument().recompute()
    return
#
def vistaIsoPosterosup(App,escala,Pieza):
#Perspectiva isométrica. Vista posteroinferior
    App.activeDocument().addObject('Drawing::FeaturePage','IsoPosterosup')
    App.activeDocument().IsoPosterosup.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoPsup')
    App.activeDocument().IsoPsup.Source =Pieza
    App.activeDocument().IsoPsup.Direction = (-1,1,1)
    App.activeDocument().IsoPsup.Rotation=300
    App.activeDocument().IsoPsup.Scale = escala
    App.activeDocument().IsoPsup.X = 700
    App.activeDocument().IsoPsup.Y = 600
    App.activeDocument().IsoPsup.ShowHiddenLines=False
    App.activeDocument().IsoPosterosup.addObject(App.activeDocument().IsoPsup)
    App.activeDocument().recompute()
    return

def vistaIsoPosteroinf(App,escala,Pieza):
#Perspectiva isométrica. Vista posteroinferior
    App.activeDocument().addObject('Drawing::FeaturePage','IsoPosteroinf')
    App.activeDocument().IsoPosteroinf.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoPinf')
    App.activeDocument().IsoPinf.Source =Pieza
    App.activeDocument().IsoPinf.Direction = (-1,-1,-1)
    App.activeDocument().IsoPinf.Rotation=300
    App.activeDocument().IsoPinf.Scale = escala
    App.activeDocument().IsoPinf.X = 700
    App.activeDocument().IsoPinf.Y = 600
    App.activeDocument().IsoPinf.ShowHiddenLines=False
    App.activeDocument().IsoPosteroinf.addObject(App.activeDocument().IsoPinf)
    App.activeDocument().recompute()
    return

def vistaIsoGeneral(App,escala,Pieza,vectorDir,angulo):
#Perspectiva isométrica. Vista general según la dirección vectorDir
    App.activeDocument().addObject('Drawing::FeaturePage','IsoGeneral')
    App.activeDocument().IsoGeneral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','IsoPinf')
    App.activeDocument().IsoPinf.Source =Pieza
    App.activeDocument().IsoPinf.Direction = vectorDir
    App.activeDocument().IsoPinf.Rotation=angulo
    App.activeDocument().IsoPinf.Scale = escala
    App.activeDocument().IsoPinf.X = 700
    App.activeDocument().IsoPinf.Y = 600
    App.activeDocument().IsoPinf.ShowHiddenLines=False
    App.activeDocument().IsoGeneral.addObject(App.activeDocument().IsoPinf)
    App.activeDocument().recompute()
    return

def vistaPlanta(App,escala,Pieza,ocultas,SupInf):
#Planta
    App.activeDocument().addObject('Drawing::FeaturePage','Planta')
    App.activeDocument().Planta.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
    App.activeDocument().topView.Source =Pieza
    if SupInf == 'Sup':
        App.activeDocument().topView.Direction = (0,0,1)
        App.activeDocument().topView.Rotation=90
    else:
        App.activeDocument().topView.Direction = (0,0,-1)
        App.activeDocument().topView.Rotation=0
    App.activeDocument().topView.Scale = escala
    App.activeDocument().topView.X = 700 
    App.activeDocument().topView.Y = 500 
    if ocultas == 's':
        App.activeDocument().topView.ShowHiddenLines=True
    else:
        App.activeDocument().topView.ShowHiddenLines=False
    App.activeDocument().Planta.addObject(App.activeDocument().topView)
    App.activeDocument().recompute()
    return

def vistaFront(App,escala,Pieza,ocultas,AntPost):
#Alzado frontal
    App.activeDocument().addObject('Drawing::FeaturePage','AlzadoFrontal')
    App.activeDocument().AlzadoFrontal.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','FrontView')
    App.activeDocument().FrontView.Source =Pieza
    if AntPost == 'Ant':
        App.activeDocument().FrontView.Direction = (1,0,0)
        App.activeDocument().FrontView.Rotation=270
    else:
        App.activeDocument().FrontView.Direction = (-1,0,0)
        App.activeDocument().FrontView.Rotation=90
    App.activeDocument().FrontView.Scale = escala
    App.activeDocument().FrontView.X = 700 
    App.activeDocument().FrontView.Y = 700 
    if ocultas == 's':
        App.activeDocument().FrontView.ShowHiddenLines=True
    else:
        App.activeDocument().FrontView.ShowHiddenLines=False
    App.activeDocument().AlzadoFrontal.addObject(App.activeDocument().FrontView)
    App.activeDocument().recompute()
    return

def vistaLat(App,escala,Pieza,ocultas,IzqDer):
#Alzado lateral
    App.activeDocument().addObject('Drawing::FeaturePage','AlzadoLateral')
    App.activeDocument().AlzadoLateral.Template = App.getResourceDir()+'Mod/Drawing/Templates/A3_apaisado.svg'
    App.activeDocument().addObject('Drawing::FeatureViewPart','RightView')
    App.activeDocument().RightView.Source =Pieza
    if IzqDer == 'Izq':
        App.activeDocument().RightView.Direction = (0,1,0)
        App.activeDocument().RightView.Rotation=270
    else:
        App.activeDocument().RightView.Direction = (0,-1,0)
        App.activeDocument().RightView.Rotation=90
    App.activeDocument().RightView.Scale = escala
    App.activeDocument().RightView.X = 700 
    App.activeDocument().RightView.Y = 700 
    if ocultas == 's':
        App.activeDocument().RightView.ShowHiddenLines=True
    else:
        App.activeDocument().RightView.ShowHiddenLines=False
    App.activeDocument().AlzadoLateral.addObject(App.activeDocument().RightView)
    App.activeDocument().recompute()
    return
