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
idPerfilPilar='12x30'
cantoPerfilPilar=metallic_profiles.W[idPerfilPilar]['h']
anchoPerfilPilar=metallic_profiles.W[idPerfilPilar]['b']
eAlmaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e']
eAlaPerfilPilar=metallic_profiles.W[idPerfilPilar]['e1']
rPerfilPilar=metallic_profiles.W[idPerfilPilar]['r']
#Viga de atado
tipoPerfilVAtado='W'        
idPerfilVAtado='18x76'
cantoPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['h']
anchoPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['b']
eAlmaPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['e']
eAlaPerfilVAtado=metallic_profiles.W[idPerfilVAtado]['e1']
holgAlaPilarVAtado=25          #holgura entre el ala del pilar y la viga de atado
#Rigidizadores
#rigidizadores ala viga de atado
eRigAla=19                     #espesor de los rigidizadores en prolongación de las alas de la viga riostra
#rigidizadores alma viga de atado
eRigAlma=13                     #espesor de los rigidizadores del alma la viga riostra para su unión al pilar
solapeRigAlmaV=50                 #longitud de solape entre el rigidizador y el alma de la viga
hAcuerdRAlma=40                       #altura (coord. Z) del acuerdo en las esquinas del rigidizador (ver gráfico)

#arriostramiento (ver figura relativa a la rutina metallic_struct.arriostr1Tubo)
tipoPerfilArr='huecoCuad'      #tipo de perfil de la diagonal del arriostramiento
idPerfilArr='140.8' 
planoArr='XZ'                  #plano en el que está el arriostramiento ('XZ' o 'YZ')
hOrigenArr=125                #distancia vertical entre el lado horizontal de la cartela y el punto de
                               #intersección de eje de la diagonal con el plano de inicio de la misma
eCartArr=13                    #espesor de la cartela del arriostramiento
solapeArrCart=150              #longitud de solape entre la cartela del arriostramiento y la diagonal
holguraCartArr=25              #holgura del chaflán de la cartela a cada lado del perfil
ang1=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado vertical
ang2=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado horizontal
VPteArr=-4440.0                 #VPteArr y HPteArr definen la pendiente de la diagonal
HPteArr=-3770.0
LArr=400                       #longitud de diagonal a representar

#general
LPilar=700                    #longitud (dirección Z) del pilar
LVAtado=550                    #longitud (dirección X) de la viga riostra a representar
#planos
escala=1                        #escala para generar planos
#****Fin datos****
signoH=1.0*HPteArr/abs(HPteArr)
signoV=1.0*VPteArr/abs(VPteArr)

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
vectorDir=Base.Vector(1,0,0)
hRig=cantoPerfilVAtado-2*eRigAla
espesorRig=eRigAlma
hAcuerdRig=hAcuerdRAlma
signoRigPosNeg='Neg'
vat=metallic_struct.VatSoldAlmPilarCart(vectorDir,anchoPerfilPilar,eAlmaPerfilPilar,holgAlaPilarVAtado,LVAtado,tipoPerfilVAtado,idPerfilVAtado,eAlmaPerfilVAtado,solapeRigAlmaV,hRig,espesorRig,hAcuerdRig,signoRigPosNeg)
pieza=pieza.fuse(vat)
#Viga de atado 2
vectorDir=Base.Vector(-1,0,0)
signoRigPosNeg='Pos'
vat=metallic_struct.VatSoldAlmPilarCart(vectorDir,anchoPerfilPilar,eAlmaPerfilPilar,holgAlaPilarVAtado,LVAtado,tipoPerfilVAtado,idPerfilVAtado,eAlmaPerfilVAtado,solapeRigAlmaV,hRig,espesorRig,hAcuerdRig,signoRigPosNeg)
pieza=pieza.fuse(vat)


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


#arriostramiento
PtoTrabajo=Base.Vector(0,0,0)
PtoOrigenCart=Base.Vector(signoH*eAlmaPerfilPilar/2.0,0,signoV*cantoPerfilVAtado/2.0)
plano=planoArr
tipoPerfilDiag=tipoPerfilArr
idPerfilDiag=idPerfilArr
VOrigenPerf=hOrigenArr
eCartela=eCartArr
solapePerfCart=solapeArrCart
holguraCart=holguraCartArr
alfa1=ang1
alfa2=ang2
VPte=VPteArr
HPte=HPteArr
LPerf=LArr
todo=metallic_struct.arriostr1Tubo(PtoTrabajo,PtoOrigenCart,plano,tipoPerfilDiag,idPerfilDiag,VOrigenPerf,eCartela,solapePerfCart,holguraCart,alfa1,alfa2,VPte,HPte,LPerf)
todo.add(pieza)

Part.show(todo)

#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=todo
FreeCADGui.Selection.addSelection(Pieza)

geometry_3D.vistaIsoAnterosup(App,escala,Pieza)
geometry_3D.vistaIsoAnteroinf(App,escala,Pieza)
geometry_3D.vistaIsoPosterosup(App,escala,Pieza)
geometry_3D.vistaIsoPosteroinf(App,escala,Pieza)

ocultas='s'
SupInf='Inf'
geometry_3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Post'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Izq'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)
