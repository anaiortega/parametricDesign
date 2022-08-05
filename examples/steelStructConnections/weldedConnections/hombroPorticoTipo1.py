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
#Hombro de pórtico soldado con viga de arriostramiento
#El pórtico está en el plano YZ y la viga de arriostramiento 
#se representa en la dirección del eje X global


#NOTA: todas las cotas se dan en mm
#****Datos****
#Pilar del pórtico
tipoPerfilPilar='W'        
idPerfilPilar='30x173'
cantoPerfilPilar=metallic_profiles.W[idPerfilPilar]['h']
anchoPerfilPilar=metallic_profiles.W[idPerfilPilar]['b']
eAlmaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e']
eAlaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e1']
#Viga del pórtico
tipoPerfilVPort='W'        
idPerfilVPort='30x90'
cantoPerfilVPort=metallic_profiles.W[idPerfilVPort]['h']
eAlmaPerfilVPort=metallic_profiles.W[idPerfilVPort]['e']
eAlaPerfilVPort=metallic_profiles.W[idPerfilVPort]['e1']
#Viga riostra
tipoPerfilVRiost='W'        
idPerfilVRiost='16x31'
cantoPerfilVRiost=metallic_profiles.W[idPerfilVRiost]['h']
eAlmaPerfilVRiost=metallic_profiles.W[idPerfilVRiost]['e']
eAlaPerfilVRiost=metallic_profiles.W[idPerfilVRiost]['e1']
#Rigidizadores
eRig=16                       #espesor de los rigidizadores
#general
ptePort=0.2                   #pendiente del pórtico en tanto por 1
LPilar=1000                    #longitud (dirección Z) del pilar
LVPort=600                    #longitud (dirección Y) de la viga del pórtico
LVRiost=500                      #longitud (dirección X) de la viga riostra a representar
#planos
escala=1                          #escala para generar planos
#****Fin datos****
#valores auxiliares
hVigaAux=math.sqrt(cantoPerfilVPort**2+(ptePort*cantoPerfilVPort)**2)
haux2=cantoPerfilPilar/2.0*ptePort
Pto1=Base.Vector(-anchoPerfilPilar/2.0,-cantoPerfilPilar/2.0,hVigaAux/2.0-haux2)
haux3=math.sqrt((cantoPerfilPilar-eAlaPerfilPilar)**2+(ptePort*(cantoPerfilPilar-eAlaPerfilPilar))**2)
#Pilar
ptoIni=Base.Vector(0,0,-LPilar)
ptoFin=Base.Vector(0,0,0)
perfil=tipoPerfilPilar
tamPerfil=idPerfilPilar
incrIni=0
incrFin=cantoPerfilVPort
giroSec=0
pilar=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
aux=Part.makeBox(2*cantoPerfilPilar,2*anchoPerfilPilar,2*cantoPerfilPilar,Pto1,Base.Vector(0,1,ptePort))
pilar=pilar.cut(aux)
pieza=pilar

#Viga del pórtico
ptoIni=Base.Vector(0,0,0)
ptoFin=Base.Vector(0,LVPort+cantoPerfilPilar/2.0,(LVPort+cantoPerfilPilar/2.0)*ptePort)
perfil=tipoPerfilVPort
tamPerfil=idPerfilVPort
incrIni=0
incrFin=0
giroSec=0
vport=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
aux=Part.makeBox(cantoPerfilPilar,cantoPerfilPilar,4*cantoPerfilPilar,Base.Vector(-cantoPerfilPilar/2.0,-cantoPerfilPilar/2.0,-2*cantoPerfilPilar))
vport=vport.cut(aux)
pieza=pieza.fuse(vport)

#Viga riostra
ptoIni=Base.Vector(eAlmaPerfilVPort/2.0,0,0)
ptoFin=Base.Vector(LVRiost,0,0)
perfil=tipoPerfilVRiost
tamPerfil=idPerfilVRiost
incrIni=0
incrFin=0
giroSec=0
vriost=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vriost)
ptoIni=Base.Vector(-eAlmaPerfilVPort/2.0,0,0)
ptoFin=Base.Vector(-LVRiost,0,0)
perfil=tipoPerfilVRiost
tamPerfil=idPerfilVRiost
incrIni=0
incrFin=0
giroSec=0
vriost=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vriost)

#Rigidizadores
vOrigenL=Pto1
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,ptePort)
vDirZL=Base.Vector(0,ptePort,-1)
listaCoordChapaL=[[0,0],[anchoPerfilPilar,0],[anchoPerfilPilar,haux3],[0,haux3]]
listaCoordAgujL=[]
espesorChapa=eRig
diamAguj=0
rig1=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
rig1=rig1.cut(pilar)
pieza=pieza.fuse(rig1)
vOrigenL=Pto1.add(Base.Vector(0,0,-hVigaAux))
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,ptePort)
vDirZL=Base.Vector(0,ptePort,1)
listaCoordChapaL=[[0,0],[anchoPerfilPilar,0],[anchoPerfilPilar,haux3],[0,haux3]]
listaCoordAgujL=[]
espesorChapa=eRig
diamAguj=0
rig2=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
rig2=rig2.cut(pilar)
pieza=pieza.fuse(rig2)

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

