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

#Unión de viga de atado a ambos lados del pilar

#NOTA: todas las cotas se dan en mm
#****Datos****
#Pilar del pórtico
tipoPerfilPilar='W'        
idPerfilPilar='30x173'
cantoPerfilPilar=PerfilesMetalicos.W[idPerfilPilar]['h']
anchoPerfilPilar=PerfilesMetalicos.W[idPerfilPilar]['b']
eAlmaPerfilPilar=PerfilesMetalicos.W[idPerfilPilar]['e']
eAlaPerfilPilar=PerfilesMetalicos.W[idPerfilPilar]['e1']
rPerfilPilar=PerfilesMetalicos.W[idPerfilPilar]['r']
#Viga de atado 1 (la soldada al alma del pilar)
tipoPerfilVAtado1='W'        
idPerfilVAtado1='18x35'
cantoPerfilVAtado1=PerfilesMetalicos.W[idPerfilVAtado1]['h']
anchoPerfilVAtado1=PerfilesMetalicos.W[idPerfilVAtado1]['b']
eAlmaPerfilVAtado1=PerfilesMetalicos.W[idPerfilVAtado1]['e']
eAlaPerfilVAtado1=PerfilesMetalicos.W[idPerfilVAtado1]['e1']
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
idPerfilVAtado2='14x22'
cantoPerfilVAtado2=PerfilesMetalicos.W[idPerfilVAtado2]['h']
anchoPerfilVAtado2=PerfilesMetalicos.W[idPerfilVAtado2]['b']
eAlmaPerfilVAtado2=PerfilesMetalicos.W[idPerfilVAtado2]['e']
eAlaPerfilVAtado2=PerfilesMetalicos.W[idPerfilVAtado2]['e1']

#arriostramiento (ver figura relativa a la rutina Metalicas.arriostr1Tubo)
tipoPerfilArr='huecoCuad'      #tipo de perfil de la diagonal del arriostramiento
idPerfilArr='140.8' 
planoArr='YZ'                  #plano en el que está el arriostramiento ('XZ' o 'YZ')
hOrigenArr=500                #distancia vertical entre el lado horizontal de la cartela y el punto de
                               #intersección de eje de la diagonal con el plano de inicio de la misma
eCartArr=19                    #espesor de la cartela del arriostramiento
solapeArrCart=150              #longitud de solape entre la cartela del arriostramiento y la diagonal
holguraCartArr=25              #holgura del chaflán de la cartela a cada lado del perfil
VPteArr=4440.0                 #VPteArr y HPteArr definen la pendiente de la diagonal
HPteArr=3770.0
ang1=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado vertical
ang2=math.degrees(math.atan(1.0*HPteArr/VPteArr))                #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado horizontal
LArr=400                       #longitud de diagonal a representar


#general
LPilar=1100                    #longitud (dirección Z) del pilar
LVAtado1=500                    #longitud (dirección X) de la viga riostra a representar
LVAtado2=600                    #longitud (dirección X) de la viga riostra a representar
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
pilar=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pilar

#Viga de atado 1
vectorDir=Base.Vector(-1,0,0)
hRig=cantoPerfilVAtado1-2*eRigAla
espesorRig=eRigAlma
hAcuerdRig=hAcuerdRAlma
signoRigPosNeg='Pos'
vat=Metalicas.VatSoldAlmPilarCart(vectorDir,anchoPerfilPilar,eAlmaPerfilPilar,holgAlaPilarVAtado1,LVAtado1,tipoPerfilVAtado1,idPerfilVAtado1,eAlmaPerfilVAtado1,solapeRigAlmaV,hRig,espesorRig,hAcuerdRig,signoRigPosNeg)
pieza=pieza.fuse(vat)

#Viga de atado 2
vectorDir=Base.Vector(0,1,0)
vat=Metalicas.VatSoldAlaPilar(vectorDir,cantoPerfilPilar,LVAtado2,tipoPerfilVAtado2,idPerfilVAtado2)
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
rig1=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

vOrigenL=Geometria3D.simYZPto(Pto1)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL2=Geometria3D.simYZlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig2=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL2,listaCoordAgujL,espesorChapa,diamAguj)

Pto1=Geometria3D.simXYPto(Pto1)

vOrigenL=Pto1
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(1,0,0)
vDirZL=Base.Vector(0,0,-1)
listaCoordChapaL=Geometria3D.simXYlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig3=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

vOrigenL=Geometria3D.simYZPto(Pto1)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,0,-1)
listaCoordChapaL=Geometria3D.simYZlistaCoord(listaCoordChapaL)
listaCoordAgujL=[]
espesorChapa=eRigAla
diamAguj=0
rig4=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)

pieza=pieza.fuse(rig1.fuse(rig2.fuse(rig3.fuse(rig4))))



#arriostramiento
PtoTrabajo=Base.Vector(0,0,0)
PtoOrigenCart=Base.Vector(0,signoH*cantoPerfilPilar/2.0,signoV*cantoPerfilVAtado2/2.0)
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
todo=Metalicas.arriostr1Tubo(PtoTrabajo,PtoOrigenCart,plano,tipoPerfilDiag,idPerfilDiag,VOrigenPerf,eCartela,solapePerfCart,holguraCart,alfa1,alfa2,VPte,HPte,LPerf)
todo.add(pieza)

Part.show(todo)

#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=todo
FreeCADGui.Selection.addSelection(Pieza)

Geometria3D.vistaIsoAnterosup(App,escala,Pieza)
Geometria3D.vistaIsoAnteroinf(App,escala,Pieza)
Geometria3D.vistaIsoPosterosup(App,escala,Pieza)
Geometria3D.vistaIsoPosteroinf(App,escala,Pieza)

ocultas='n'
SupInf='Sup'
Geometria3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Ant'
Geometria3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Izq'
Geometria3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)