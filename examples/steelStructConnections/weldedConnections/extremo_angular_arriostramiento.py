# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, TechDraw, FreeCADGui
import Draft
import freeCAD_civil
from freeCAD_civil import geometry_3D
from freeCAD_civil import metallic_profiles
from freeCAD_civil import metallic_struct
from FreeCAD import Base
from Draft import *
#Unión dúctil soldada de un angular simple L (de lados iguales) en su extremo
#(ver página 308 del libro publicado por APTA
#"Naves industriales con acero")


#NOTA: todas las cotas se dan en mm
#****Datos****
#Geometría
alfa=32                         #ángulo que forma la diagonal con la vertical
#Diagonal 
tipoPerfilDiag='L'        
idPerfilDiag='40x4'             # se escoge el espesor del perfil de forma que sea 1/10 la dimensión del lado de la L
ladoDiag=metallic_profiles.L[idPerfilDiag]['a']  #lado de la L
espDiag=metallic_profiles.L[idPerfilDiag]['e']   #espesor del perfil
cdgDiag=metallic_profiles.L[idPerfilDiag]['cx']  #distancia del eje de la diagonal a las caras exteriores
#Dimensiones cartela
ZCartela=100
YCartela=150
dimChaflan=20
espCartela=5                   #tomar   espCartela > ladoDiag/10
#general
LDiag=800                     #longitud de la diagonal a representar

#planos
escala=1                        #escala para generar planos
#****Fin datos****

#Dibujo de la diagonal
alfarad=math.radians(alfa)      #ángulo alfa en radianes
ptoIni=Base.Vector(espCartela+cdgDiag,-LDiag*math.sin(alfarad),-LDiag*math.cos(alfarad))
ptoFin=Base.Vector(espCartela+cdgDiag,0,0)
perfil=tipoPerfilDiag
tamPerfil=idPerfilDiag
incrIni=0
incrFin=0
giroSec=90
diag=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=diag
#Part.show(pieza)

#Dibujo de la cartela
P1=Base.Vector(0,YCartela,ZCartela)

aux1=2.5*ladoDiag*math.cos(alfarad)-cdgDiag*math.sin(alfarad)
aux2=1.75*ladoDiag*math.cos(alfarad)+(ladoDiag-cdgDiag)*math.sin(alfarad)
if aux1 > aux2:
    Z1=aux1
else:
    Z1=aux2

aux3=ladoDiag-cdgDiag
Y1=Z1*math.tan(alfarad)
Y2=aux3/math.cos(alfarad)
Y3=Y1-Y2
P4=Base.Vector(0,-Y3,-Z1)
P3=P4.add(Base.Vector(0,dimChaflan,0))
Y4=YCartela+Y3-dimChaflan
angaux=math.radians(90-alfa-30)
P2=P3.add(Base.Vector(0,Y4,Y4*math.tan(angaux)))
P5=P4.add(Base.Vector(0,-ladoDiag/math.cos(alfarad),0))
Z2=dimChaflan*math.sin(alfarad)
Y5=dimChaflan*math.cos(alfarad)
P6=P5.add(Base.Vector(0,-Y5,Z2))
Z3=Z1+ZCartela-Z2
angaux=math.radians(alfa-30)
P7=P6.add(Base.Vector(0,Z3**math.tan(angaux),Z3))


cartela=Part.makePolygon([P1,P2,P3,P4,P5,P6,P7,P1])
cartela=Part.Face(cartela)
vextru=Base.Vector(espCartela,0,0)
cartela=cartela.extrude(vextru)
pieza=pieza.fuse(cartela)

#soldaduras
P8=Base.Vector(0,aux3*math.cos(alfarad),-aux3*math.sin(alfarad))
P9=Base.Vector(0,-cdgDiag*math.cos(alfarad),cdgDiag*math.sin(alfarad))
sold1=metallic_struct.soldadura2Ptos(pieza,pieza,0.4*ladoDiag/10,P4.add(Base.Vector(espCartela,0,0)),P8.add(Base.Vector(espCartela,0,0)))
pieza=pieza.fuse(sold1)
sold2=metallic_struct.soldadura2Ptos(pieza,pieza,0.7*ladoDiag/10,P5.add(Base.Vector(espCartela,0,0)),P9.add(Base.Vector(espCartela,0,0)))
pieza=pieza.fuse(sold2)

Part.show(pieza)

#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=pieza
FreeCADGui.Selection.addSelection(Pieza)

geometry_3D.vistasIsom(App,escala,Pieza)
ocultas='s'
SupInf='Sup'
geometry_3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Ant'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)

