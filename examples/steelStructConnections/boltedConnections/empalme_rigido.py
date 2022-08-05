# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, TechDraw, FreeCADGui
import Draft
import freeCAD_civil 
from freeCAD_civil  import geometry_3D
from freeCAD_civil  import metallic_profiles
from freeCAD_civil  import metallic_struct
from FreeCAD import Base
from Draft import *
#Empalme atornillado entre 2 tramos del mismo perfil. El eje longitudinal del perfil
#se representa en la dirección del eje Y global y el eje fuerte de la sección en la
#dirección del eje Z global

#NOTA: todas las cotas se dan en mm
#****Datos****
tipoPerfil='HEB'
idPerfil='500'
cantoPerfil=metallic_profiles.HEB[idPerfil]['h']
eAlmaPerfil=metallic_profiles.HEB[idPerfil]['e']
eAlaPerfil=metallic_profiles.HEB[idPerfil]['e1']
holguraJunta=2
espCubrejAlas=15               #espesor de los cubrejuntas de las alas
dimYCubrejAlas=500             #largo de los cubrejuntas de las alas
dimXCubrejAlas=300             #ancho de los cubrejuntas de las alas
espCubrejAlma=8                #espesor de los cubrejuntas del alma
dimYCubrejAlma=200             #largo de los cubrejuntas del alma
dimZCubrejAlma=400             #ancho de los cubrejuntas del alma
fiAgujAlas=22                  #diámetro de los agujeros alas
fiAgujAlma=18                  #diámetro de los agujeros alma
#Tornillos alas
nXFilasTAla=4                  #nº de filas de tornillos en dirección X
dXFilasTAla=[75,100,75]        #distancia entre filas de tornillos en dirección X
nYFilasTAla=6                  #nº de filas de tornillos en dirección Y
dYFilasTAla=[75,75,100,75,75]  #distancia entre filas de tornillos en dirección Y
#Tornillos alma
nYFilasTAlma=2                  #nº de filas de tornillos en dirección Y
dYFilasTAlma=[100]              #distancia entre filas de tornillos en dirección Y
nZFilasTAlma=4                  #nº de filas de tornillos en dirección Z
dZFilasTAlma=[75,75,75]         #distancia entre filas de tornillos en dirección Z
#general
Lpieza=1000                    #longitud (dirección Y) del conjunto a representar
#planos
escala=1                     #escala para generar planos
#****Fin datos****


#Perfiles
ptoIni=Base.Vector(0,-Lpieza/2,0)
ptoFin=Base.Vector(0,0,0)
perfil=tipoPerfil
tamPerfil=idPerfil
incrIni=0
incrFin=-holguraJunta/2
giroSec=0
corr1=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=corr1
ptoIni=Base.Vector(0,0,0)
ptoFin=Base.Vector(0,Lpieza/2,0)
perfil=tipoPerfil
tamPerfil=idPerfil
incrIni=-holguraJunta/2
incrFin=0
giroSec=0
corr2=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(corr2)
#Cubrejuntas ala superior
vOrigenL=Base.Vector(0,0,cantoPerfil/2)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordL=[[-dimXCubrejAlas/2,-dimYCubrejAlas/2],[dimXCubrejAlas/2,-dimYCubrejAlas/2],[dimXCubrejAlas/2,dimYCubrejAlas/2],[-dimXCubrejAlas/2,dimYCubrejAlas/2]]
altura=espCubrejAlas
cubrjAlaSup=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(cubrjAlaSup)
#Cubrejuntas ala inferior
vOrigenL=Base.Vector(0,0,-cantoPerfil/2-espCubrejAlas)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordL=[[-dimXCubrejAlas/2,-dimYCubrejAlas/2],[dimXCubrejAlas/2,-dimYCubrejAlas/2],[dimXCubrejAlas/2,dimYCubrejAlas/2],[-dimXCubrejAlas/2,dimYCubrejAlas/2]]
altura=espCubrejAlas
cubrjAlaInf=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(cubrjAlaInf)
#Cubrejuntas alma dorsal 
vOrigenL=Base.Vector(-eAlmaPerfil/2,0,0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(-1,0,0)
listaCoordL=[[-dimYCubrejAlma/2,-dimZCubrejAlma/2],[dimYCubrejAlma/2,-dimZCubrejAlma/2],[dimYCubrejAlma/2,dimZCubrejAlma/2],[-dimYCubrejAlma/2,dimZCubrejAlma/2]]
altura=espCubrejAlma
cubrjAlmaDrs=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(cubrjAlmaDrs)
#Cubrejuntas alma frontal
vOrigenL=Base.Vector(eAlmaPerfil/2,0,0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[-dimYCubrejAlma/2,-dimZCubrejAlma/2],[dimYCubrejAlma/2,-dimZCubrejAlma/2],[dimYCubrejAlma/2,dimZCubrejAlma/2],[-dimYCubrejAlma/2,dimZCubrejAlma/2]]
altura=espCubrejAlma
cubrjAlmaFr=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(cubrjAlmaFr)

#Agujeros en ala inferior
vOrigenL=Base.Vector(0,0,-cantoPerfil/2-espCubrejAlas)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordCentrosL=[]
diametro=fiAgujAlas
altura=espCubrejAlas+eAlaPerfil
xLinic=-math.fsum(dXFilasTAla)/2
yLinic=-math.fsum(dYFilasTAla)/2
for i in range(0,nXFilasTAla):
    for j in range (0,nYFilasTAla):
        centro=[xLinic+math.fsum(dXFilasTAla[0:i]),yLinic+math.fsum(dYFilasTAla[0:j])]
        listaCoordCentrosL.append(centro)

agujAlaInf=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlaInf)

#Agujeros en ala superior
vOrigenL=Base.Vector(0,0,cantoPerfil/2+espCubrejAlas)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,-1)
listaCoordCentrosL=[]
diametro=fiAgujAlas
altura=espCubrejAlas+eAlaPerfil
xLinic=-math.fsum(dXFilasTAla)/2
yLinic=-math.fsum(dYFilasTAla)/2
for i in range(0,nXFilasTAla):
    for j in range (0,nYFilasTAla):
        centro=[xLinic+math.fsum(dXFilasTAla[0:i]),yLinic+math.fsum(dYFilasTAla[0:j])]
        listaCoordCentrosL.append(centro)

agujAlaSup=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlaSup)

#Agujeros en alma
vOrigenL=Base.Vector(-eAlmaPerfil/2-espCubrejAlma,0,0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordCentrosL=[]
diametro=fiAgujAlma
altura=eAlmaPerfil+2*espCubrejAlma
xLinic=-math.fsum(dYFilasTAlma)/2
yLinic=-math.fsum(dZFilasTAlma)/2
for i in range(0,nYFilasTAlma):
    for j in range (0,nZFilasTAlma):
        centro=[xLinic+math.fsum(dYFilasTAlma[0:i]),yLinic+math.fsum(dZFilasTAlma[0:j])]
        listaCoordCentrosL.append(centro)

agujAlma=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlma)

Part.show(pieza)

#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=pieza
FreeCADGui.Selection.addSelection(Pieza)

geometry_3D.vistaIsoAnterosup(App,escala,Pieza)
geometry_3D.vistaIsoAnteroinf(App,escala,Pieza)
geometry_3D.vistaIsoPosterosup(App,escala,Pieza)
geometry_3D.vistaIsoPosteroinf(App,escala,Pieza)

ocultas='s'
SupInf='Sup'
geometry_3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Ant'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)
