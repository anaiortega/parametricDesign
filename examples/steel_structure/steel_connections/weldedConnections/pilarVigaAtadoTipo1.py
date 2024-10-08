# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, TechDraw, FreeCADGui
import Draft
from parametric_design.freeCAD_civil import geometry_3D
from parametric_design.freeCAD_civil import metallic_profiles
from parametric_design.freeCAD_civil import metallic_struct
from FreeCAD import Base
from Draft import *

#Unión de viga de atado a ambos lados del pilar

docName='pilar_viga_atado_tipo1'
docGeom=App.newDocument(docName,docName)

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
#Viga de atado
tipoPerfilVAtado='W'        
idPerfilVAtado='18x35'
cantoPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['h']
anchoPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['b']
eAlmaPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['e']
eAlaPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['e1']
holgAlaPilarVAtado=30          #holgura entre el ala del pilar y la viga de atado
#Rigidizadores
#rigidizadores ala viga de atado
eRigAla=19                     #espesor de los rigidizadores en prolongación de las alas de la viga riostra
#rigidizadores alma viga de atado
eRigAlma=13                     #espesor de los rigidizadores del alma la viga riostra para su unión al pilar
solapeRAlmaV=50                 #longitud de solape entre el rigidizador y el alma de la viga
hRAlma=40                       #altura (coord. Z) del acuerdo en las esquinas del rigidizador (ver gráfico)


#general
LPilar=1000                    #longitud (dirección Z) del pilar
LVAtado=750                      #longitud (dirección X) de la viga riostra a representar
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

#Viga de atado
ptoIni=Base.Vector(anchoPerfilPilar/2.0+holgAlaPilarVAtado,0,0)
ptoFin=Base.Vector(LVAtado,0,0)
perfil=tipoPerfilVAtado
tamPerfil=idPerfilVAtado
incrIni=0
incrFin=0
giroSec=0
vatado=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vatado)
ptoIni=geometry_3D.simYZPto(ptoIni)
ptoFin=geometry_3D.simYZPto(ptoFin)
perfil=tipoPerfilVAtado
tamPerfil=idPerfilVAtado
incrIni=0
incrFin=0
giroSec=0
vatado=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vatado)

#Rigidizadores en el plano del ala de la viga
Pto1=Base.Vector(eAlmaPerfilPilar/2.0,0,cantoPerfilVAtado/2.0-eRigAla)
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

#Rigidizadores en el alma de la viga
Pto1=Base.Vector(eAlmaPerfilPilar/2.0,-eRigAlma/2.0-eAlmaPerfilVAtado/2.0,0)
auxX=(cantoPerfilVAtado-2*eRigAla)/2.0
auxY=(anchoPerfilPilar-eAlmaPerfilPilar)/2.0+holgAlaPilarVAtado+solapeRAlmaV

vOrigenL=Pto1
vDirXL=Base.Vector(0,0,1)
vDirYL=Base.Vector(1,0,0)
vDirZL=Base.Vector(0,1,0)
listaCoordChapaL=[[-auxX,0],[-auxX,auxY-holgAlaPilarVAtado-solapeRAlmaV],[-auxX+hRAlma,auxY-holgAlaPilarVAtado-solapeRAlmaV+hRAlma],[-auxX+hRAlma,auxY],[auxX-hRAlma,auxY],[auxX-hRAlma,auxY-holgAlaPilarVAtado-solapeRAlmaV+hRAlma],[auxX,auxY-holgAlaPilarVAtado-solapeRAlmaV],[auxX,0]]
listaCoordAgujL=[]
espesorChapa=eRigAlma
diamAguj=0
rig5=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

vOrigenL=geometry_3D.simYZPto(Pto1)
vDirXL=Base.Vector(0,0,1)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,1,0)
listaCoordChapaL=geometry_3D.simYZlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAlma
diamAguj=0
rig6=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

pieza=pieza.fuse(rig5.fuse(rig6))

Part.show(pieza,'pieza')

views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.pieza],scale=0.10,pageTemplate='A3_Landscape_blank.svg')

