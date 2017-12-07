# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, Drawing, FreeCADGui
import Draft
import freeCADcivilOrt
from freeCADcivilOrt import Geometria3D
from freeCADcivilOrt import PerfilesMetalicos
from freeCADcivilOrt import Metalicas
from FreeCAD import Base
from Draft import *
#Clave de pórtico con viga de arriostramiento soldada
#El pórtico está en el plano YZ y la viga de arriostramiento 
#se representa en la dirección del eje X global


#NOTA: todas las cotas se dan en mm
#****Datos****
#Vigas del pórtico
tipoPerfilVPort='W'        
idPerfilVPort='30x108'
cantoPerfilVPort=PerfilesMetalicos.W[idPerfilVPort]['h']
eAlmaPerfilVPort=PerfilesMetalicos.W[idPerfilVPort]['e']
eAlaPerfilVPort=PerfilesMetalicos.W[idPerfilVPort]['e1']
#Viga riostra
tipoPerfilVRiost='W'        
idPerfilVRiost='18x46'
cantoPerfilVRiost=PerfilesMetalicos.W[idPerfilVRiost]['h']
eAlmaPerfilVRiost=PerfilesMetalicos.W[idPerfilVRiost]['e']
eAlaPerfilVRiost=PerfilesMetalicos.W[idPerfilVRiost]['e1']
#general
ptePort=0.2                   #pendiente del pórtico en tanto por 1
LVPort=500                    #longitud (dirección Y) de la viga del pórtico a representar
LVRiost=500                      #longitud (dirección X) de la viga riostra a representar
#planos
escala=1                        #escala para generar planos
#****Fin datos****


#Vigas pórtico

ptoIni=Base.Vector(0,-LVPort,-LVPort*ptePort)
ptoFin=Base.Vector(0,0,0)
perfil=tipoPerfilVPort
tamPerfil=idPerfilVPort
incrIni=0
incrFin=LVPort
giroSec=0
vport=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
aux=Part.makeBox(2*cantoPerfilVPort,2*cantoPerfilVPort,2*cantoPerfilVPort,Base.Vector(-cantoPerfilVPort,0,-cantoPerfilVPort))
pieza=vport.cut(aux)
vport.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),180)
aux.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),180)
vport2=vport.cut(aux)
pieza=pieza.fuse(vport2)

#Viga riostra
ptoIni=Base.Vector(eAlmaPerfilVPort/2,0,0)
ptoFin=Base.Vector(LVRiost,0,0)
perfil=tipoPerfilVRiost
tamPerfil=idPerfilVRiost
incrIni=0
incrFin=0
giroSec=0
vriost=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vriost)
ptoIni=Base.Vector(-eAlmaPerfilVPort/2,0,0)
ptoFin=Base.Vector(-LVRiost,0,0)
perfil=tipoPerfilVRiost
tamPerfil=idPerfilVRiost
incrIni=0
incrFin=0
giroSec=0
vriost=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vriost)


Part.show(pieza)

#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=pieza
FreeCADGui.Selection.addSelection(Pieza)

Geometria3D.vistasIsom(App,escala,Pieza)
ocultas='s'
SupInf='Sup'
Geometria3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Ant'
Geometria3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
Geometria3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)

