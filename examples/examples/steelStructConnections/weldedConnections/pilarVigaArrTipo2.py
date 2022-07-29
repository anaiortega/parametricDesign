# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, Drawing, FreeCADGui
import Draft
import freeCAD_civil
from freeCAD_civil import geometry_3D
from freeCAD_civil import metallic_profiles
from freeCAD_civil import metallic_struct
from FreeCAD import Base
from Draft import *

#Unión de viga de atado a ambos lados del pilar

#NOTA: todas las cotas se dan en mm
#****Datos****
#Pilar del pórtico
tipoPerfilPilar='W'        
idPerfilPilar='30x173'
cantoPerfilPilar=metallic_profiles.W[idPerfilPilar]['h']
anchoPerfilPilar=metallic_profiles.W[idPerfilPilar]['b']
eAlmaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e']
eAlaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e1']
rPerfilPilar=metallic_profiles.W[idPerfilPilar]['r']
#Viga de atado 1 (la soldada al alma del pilar)
tipoPerfilVAtado1='W'        
idPerfilVAtado1='18x35'
cantoPerfilVAtado1=metallic_profiles.W[idPerfilVAtado1]['h']
anchoPerfilVAtado1=metallic_profiles.W[idPerfilVAtado1]['b']
eAlmaPerfilVAtado1=metallic_profiles.W[idPerfilVAtado1]['e']
eAlaPerfilVAtado1=metallic_profiles.W[idPerfilVAtado1]['e1']
holgAlaPilarVAtado1=25          #holgura entre el ala del pilar y la viga de atado
#Rigidizadores
#rigidizadores ala viga de atado
eRigAla=13                     #espesor de los rigidizadores en prolongación de las alas de la viga riostra
#rigidizadores alma viga de atado
eRigAlma=9.5                    #espesor de los rigidizadores del alma la viga riostra para su unión al pilar
solapeRigAlmaV=50                 #longitud de solape entre el rigidizador y el alma de la viga
hAcuerdRAlma=40                       #altura (coord. Z) del acuerdo en las esquinas del rigidizador (ver gráfico)
#Viga de atado 2 (la soldada al ala del pilar)
tipoPerfilVAtado2='W'        
idPerfilVAtado2='18x76'
cantoPerfilVAtado2=metallic_profiles.W[idPerfilVAtado2]['h']
anchoPerfilVAtado2=metallic_profiles.W[idPerfilVAtado2]['b']
eAlmaPerfilVAtado2=metallic_profiles.W[idPerfilVAtado2]['e']
eAlaPerfilVAtado2=metallic_profiles.W[idPerfilVAtado2]['e1']

#general
LPilar=850                     #longitud (dirección Z) del pilar
LVAtado1=500                    #longitud (dirección X) de la viga riostra a representar
LVAtado2=600                    #longitud (dirección X) de la viga riostra a representar
#planos
escala=1                        #escala para generar planos
#****Fin datos****

#Pilar
ptoIni=Base.Vector(0,0,-LPilar)
ptoFin=Base.Vector(0,0,LPilar)
perfil=tipoPerfilPilar
tamPerfil=idPerfilPilar
incrIni=0
incrFin=0
giroSec=0
pilar=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pilar

#Viga de atado 1
vectorDir=Base.Vector(-1,0,0)
hRig=cantoPerfilVAtado1-2*eRigAla
espesorRig=eRigAlma
hAcuerdRig=hAcuerdRAlma
signoRigPosNeg='Pos'
vat=metallic_struct.VatSoldAlmPilarCart(vectorDir,anchoPerfilPilar,eAlmaPerfilPilar,holgAlaPilarVAtado1,LVAtado1,tipoPerfilVAtado1,idPerfilVAtado1,eAlmaPerfilVAtado1,solapeRigAlmaV,hRig,espesorRig,hAcuerdRig,signoRigPosNeg)
pieza=pieza.fuse(vat)

#Viga de atado 2
vectorDir=Base.Vector(0,1,0)
vat=metallic_struct.VatSoldAlaPilar(vectorDir,cantoPerfilPilar,LVAtado2,tipoPerfilVAtado2,idPerfilVAtado2)
pieza=pieza.fuse(vat)

#Rigidizadores en el plano del ala de la viga
Pto1=Base.Vector(eAlmaPerfilPilar/2.0,0,cantoPerfilVAtado1/2.0-eRigAla)
auxX=(cantoPerfilPilar-2*eAlaPerfilPilar)/2.0
auxY=(anchoPerfilPilar-eAlmaPerfilPilar)/2.0

vOrigenL=Pto1
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(1,0,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL=[[-auxX+rPerfilPilar,0],[-auxX,rPerfilPilar],[-auxX,auxY],[auxX,auxY],[auxX,rPerfilPilar],[auxX-rPerfilPilar,0]]
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig1=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

vOrigenL=geometry_3D.simYZPto(Pto1)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL2=geometry_3D.simYZlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig2=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL2,listaCoordAgujL,espesorChapa,diamAguj)

Pto1=geometry_3D.simXYPto(Pto1)

vOrigenL=Pto1
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(1,0,0)
vDirZL=Base.Vector(0,0,-1)
listaCoordChapaL=geometry_3D.simXYlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig3=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

vOrigenL=geometry_3D.simYZPto(Pto1)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,0,-1)
listaCoordChapaL=geometry_3D.simYZlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig4=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

pieza=pieza.fuse(rig1.fuse(rig2.fuse(rig3.fuse(rig4))))

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
AntPost='Post'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)
