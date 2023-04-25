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
from layout_utils import views 

#Cruce de diagonales con manguito (ver página 298 del libro publicado por APTA
#"Naves industriales con acero"

docName='cruce_diag_manguito3D'
docGeom=App.newDocument(docName,docName)


#NOTA: todas las cotas se dan en mm
#****Datos****
#Diagonal 1 (se representa por detrás)
tipoPerfilDiag1='L'        
idPerfilDiag1='40x4'
cdgDiag1=metallic_profiles.L[idPerfilDiag1]['cy']
angVertDiag1=45                 #ángulo que forma la diagonal 1 con la vertical
#Diagonal 2 (se representa por delante de la diagonal 1)
tipoPerfilDiag2='L'        
idPerfilDiag2='40x4'
cdgDiag2=metallic_profiles.L[idPerfilDiag2]['cy']
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
diag1=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=diag1
#Diagonal 2
ptoIni=Base.Vector(eCartelasExtremas/2+cdgDiag2,-LDiag2/2*math.sin(math.radians(angVertDiag2)),-LDiag2/2*math.cos(math.radians(angVertDiag2)))
ptoFin=Base.Vector(eCartelasExtremas/2+cdgDiag2,LDiag2/2*math.sin(math.radians(angVertDiag2)),LDiag2/2*math.cos(math.radians(angVertDiag2)))
perfil=tipoPerfilDiag2
tamPerfil=idPerfilDiag2
incrIni=0
incrFin=0
giroSec=0
diag2=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(diag2)

Part.show(pieza,'pieza')

views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.pieza],scale=0.10,pageTemplate='A3_Landscape_blank.svg')

#Agujero para manguito

#no está programado


