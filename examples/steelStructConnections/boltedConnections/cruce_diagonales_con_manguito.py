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
#Cruce de diagonales con manguito (ver página 298 del libro publicado por APTA
#"Naves industriales con acero"



#NOTA: todas las cotas se dan en mm
#****Datos****
#Diagonal 1 (se representa por detrás)
tipoPerfilDiag1='L'        
idPerfilDiag1='40x4'
cdgDiag1=PerfilesMetalicos.L[idPerfilDiag1]['cy']
angVertDiag1=45                 #ángulo que forma la diagonal 1 con la vertical
#Diagonal 2 (se representa por delante de la diagonal 1)
tipoPerfilDiag2='L'        
idPerfilDiag2='40x4'
cdgDiag2=PerfilesMetalicos.L[idPerfilDiag2]['cy']
angVertDiag2=45                 #ángulo que forma la diagonal 2 con la vertical
#Manguito
eCartelasExtremas=6             #espesor de las cartelas en extremos de la diagonal
                                #esta será la separación entre caras de las dos diagonales
fiAgujero=25                    #diámetro del agujero para colocar el manguito
#general
LDiag1=1000                     #longitud de la diagonal 1 a representar
LDiag2=1000                     #longitud de la diagonal 2 a representar
#planos
escala=1                        #escala para generar planos
#****Fin datos****

#Diagonal 1
ptoIni=Base.Vector(-eCartelasExtremas/2-cdgDiag1,-LDiag1/2*math.sin(math.radians(angVertDiag1)),LDiag1/2*math.cos(math.radians(angVertDiag1)))
ptoFin=Base.Vector(-eCartelasExtremas/2-cdgDiag1,LDiag1/2*math.sin(math.radians(angVertDiag1)),-LDiag1/2*math.cos(math.radians(angVertDiag1)))
perfil=tipoPerfilDiag1
tamPerfil=idPerfilDiag1
incrIni=0
incrFin=0
giroSec=180
diag1=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=diag1
#Diagonal 2
ptoIni=Base.Vector(eCartelasExtremas/2+cdgDiag2,-LDiag2/2*math.sin(math.radians(angVertDiag2)),-LDiag2/2*math.cos(math.radians(angVertDiag2)))
ptoFin=Base.Vector(eCartelasExtremas/2+cdgDiag2,LDiag2/2*math.sin(math.radians(angVertDiag2)),LDiag2/2*math.cos(math.radians(angVertDiag2)))
perfil=tipoPerfilDiag2
tamPerfil=idPerfilDiag2
incrIni=0
incrFin=0
giroSec=0
diag2=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(diag2)

#Agujero para manguito

#no está programado

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

