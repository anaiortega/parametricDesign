# -*- coding: utf-8 -*-

#*    2013   Ana Ortega    *

import Part, FreeCAD, math, TechDraw, FreeCADGui
import Draft
from parametric_design.freeCAD_civil import geometry_3D
from parametric_design.freeCAD_civil import metallic_profiles
from parametric_design.freeCAD_civil import metallic_struct
from FreeCAD import Base
from Draft import *
from parametric_design.layout_utils import views 

#Unión de viga de atado a ambos lados del pilar

docName='pilar_varr_vcarr_tipo1'
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
holgAlaPilarVAtado=25          #holgura entre el ala del pilar y la viga de atado
#Rigidizadores
#rigidizadores ala viga de atado
eRigAla=19                     #espesor de los rigidizadores en prolongación de las alas de la viga riostra
#rigidizadores alma viga de atado
eRigAlma=13                     #espesor de los rigidizadores del alma la viga riostra para su unión al pilar
solapeRAlmaV=50                 #longitud de solape entre el rigidizador y el alma de la viga
hRAlma=40                       #altura (coord. Z) del acuerdo en las esquinas del rigidizador (ver gráfico)

#arriostramiento (ver figura relativa a la rutina metallic_struct.arriostr1Tubo)
tipoPerfilArr='huecoCuad'      #tipo de perfil de la diagonal del arriostramiento
idPerfilArr='100.4' 
planoArr='XZ'                  #plano en el que está el arriostramiento ('XZ' o 'YZ')
hOrigenArr=125                #distancia vertical entre el lado horizontal de la cartela y el punto de
                               #intersección de eje de la diagonal con el plano de inicio de la misma
eCartArr=9.5                   #espesor de la cartela del arriostramiento
solapeArrCart=150              #longitud de solape entre la cartela del arriostramiento y la diagonal
holguraCartArr=25              #holgura del chaflán de la cartela a cada lado del perfil
ang1=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado vertical
ang2=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado horizontal
VPteArr=3955.0                 #VPteArr y HPteArr definen la pendiente de la diagonal
HPteArr=2550.0
LArr=500                       #longitud de diagonal a representar

#general
LPilar=1100                    #longitud (dirección Z) del pilar
LVAtado=700                    #longitud (dirección X) de la viga riostra a representar
#planos
escala=1                        #escala para generar planos


#Datos de viga carrilera
tipoPerfilVcarr='W'        
idPerfilVcarr='armada425x370'
cantoPerfilVcarr=metallic_profiles.W[idPerfilVcarr]['h']
anchoPerfilVcarr=metallic_profiles.W[idPerfilVcarr]['b']
eAlmaPerfilVcarr=metallic_profiles.W[idPerfilVcarr]['e']
eAlaPerfilVcarr=metallic_profiles.W[idPerfilVcarr]['e1']
rPerfilVcarr=metallic_profiles.W[idPerfilVcarr]['r']
dEjesVcarrVac=(16250-14850)/2.0           #distancia entre los ejes de la viga carrilera y de la viga de acompañamiento

eChapaCab=9.5                    #espesor de la capa de unión entre cabezas de viga carrilera y de viga de acompañamiento
slpChapaVcarr=50                #solape entre la chapa y la cabeza de la viga carrilera
slpChapaVAtado=anchoPerfilVAtado/2.0                 #solape entre la chapa y la cabeza de la viga de acompañamiento

hlgPilarChapa=50                #holgura entre las alas del pilar y la chapa

eRigVCarr=13                   #espesor rigidizadores viga carrilera
#Datos de la ménsula
tipoPerfilMens='W'        
idPerfilMens='24x103'
cantoPerfilMens=metallic_profiles.W[idPerfilMens]['h']
anchoPerfilMens=metallic_profiles.W[idPerfilMens]['b']
eAlmaPerfilMens=metallic_profiles.W[idPerfilMens]['e']
eAlaPerfilMens=metallic_profiles.W[idPerfilMens]['e1']

LMensula=550                    #longitud de la ménsula

erigAlaMens=25                    #espesor de los rigidizadores a disponer en el pilar
                                #en prolongación de las alas de la ménsula
erigCierrMens=19                #espesor del rigidizador de cierre de la ménsula
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

#pieza=pieza.fuse(rig1.fuse(rig2.fuse(rig3.fuse(rig4))))
pieza=pieza.fuse(rig1.fuse(rig2))

#Rigidizadores en el alma de la viga
Pto1=Base.Vector(eAlmaPerfilPilar/2.0,-eRigAlma/2.0-eAlmaPerfilVAtado/2,0)
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

#arriostramiento
PtoTrabajo=Base.Vector(0,0,0)
PtoOrigenCart=Base.Vector(eAlmaPerfilPilar/2,0,cantoPerfilVAtado/2)
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

###VIGA CARRILERA
#Viga carrilera
ptoIni=Base.Vector(-LVAtado,dEjesVcarrVac,cantoPerfilVAtado/2.0-cantoPerfilVcarr/2.0)
ptoFin=Base.Vector(LVAtado,dEjesVcarrVac,cantoPerfilVAtado/2.0-cantoPerfilVcarr/2.0)
perfil=tipoPerfilVcarr
tamPerfil=idPerfilVcarr
incrIni=0
incrFin=0
giroSec=0
viga=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(viga)

#Chapa de unión de cabezas de vigas
#chapa 1
anchoChap=dEjesVcarrVac-anchoPerfilVcarr/2.0-anchoPerfilVAtado/2.0+slpChapaVcarr+slpChapaVAtado
largoChap=LVAtado-anchoPerfilPilar/2.0-hlgPilarChapa
vOrigenL=Base.Vector(-LVAtado,anchoPerfilVAtado/2.0-slpChapaVAtado,cantoPerfilVAtado/2.0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(1,0,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL=[[0,0],[anchoChap,0],[anchoChap,largoChap],[0,largoChap]]
listaCoordAgujL=[]
espesorChapa=eChapaCab
diamAguj=0
chapa=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(chapa)
#chapa 2
vOrigenL=Base.Vector(LVAtado,anchoPerfilVAtado/2.0-slpChapaVAtado,cantoPerfilVAtado/2.0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(-1,0,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL=[[0,0],[anchoChap,0],[anchoChap,largoChap],[0,largoChap]]
listaCoordAgujL=[]
espesorChapa=eChapaCab
diamAguj=0
chapa=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(chapa)

#Rigidizadores en viga carrilera
ptoCentral=Base.Vector(0,dEjesVcarrVac,cantoPerfilVAtado/2.0-cantoPerfilVcarr/2.0)
vDirAlma=Base.Vector(0,0,1)
vDirAla=Base.Vector(0,1,0)
cantoPerfil=cantoPerfilVcarr
anchoPerfil=anchoPerfilVcarr
eAlaPerfil=eAlaPerfilVcarr
eAlmaPerfil=eAlmaPerfilVcarr
radioPerfil=rPerfilVcarr
eRigid=eRigVCarr
rigid=metallic_struct.parRigOrtAlma(ptoCentral,vDirAlma,vDirAla,cantoPerfil,anchoPerfil,eAlaPerfil,eAlmaPerfil,radioPerfil,eRigid)
pieza=pieza.fuse(rigid)

#Ménsula
zMens=cantoPerfilVAtado/2.0-cantoPerfilVcarr-cantoPerfilMens/2.0
ptoIni=Base.Vector(0,cantoPerfilPilar/2.0,zMens)
ptoFin=Base.Vector(0,cantoPerfilPilar/2.0+LMensula,zMens)
perfil=tipoPerfilMens
tamPerfil=idPerfilMens
incrIni=0
incrFin=0
giroSec=0
mensula=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(mensula)

#Rigidizadores en pilar en prolongación de las alas de la ménsula
zCentro=zMens+cantoPerfilMens/2.0-eAlaPerfilMens/2.0
ptoCentral=Base.Vector(0,0,zCentro)
vDirAlma=Base.Vector(0,1,0)
vDirAla=Base.Vector(1,0,0)
cantoPerfil=cantoPerfilPilar
anchoPerfil=anchoPerfilPilar
eAlaPerfil=eAlaPerfilPilar
eAlmaPerfil=eAlmaPerfilPilar
radioPerfil=rPerfilPilar
eRigid=erigAlaMens
rigid=metallic_struct.parRigOrtAlma(ptoCentral,vDirAlma,vDirAla,cantoPerfil,anchoPerfil,eAlaPerfil,eAlmaPerfil,radioPerfil,eRigid)
pieza=pieza.fuse(rigid)

zCentro=zMens-cantoPerfilMens/2.0+eAlaPerfilMens/2.0
ptoCentral=Base.Vector(0,0,zCentro)
rigid=metallic_struct.parRigOrtAlma(ptoCentral,vDirAlma,vDirAla,cantoPerfil,anchoPerfil,eAlaPerfil,eAlmaPerfil,radioPerfil,eRigid)
eRigid=erigAlaMens
pieza=pieza.fuse(rigid)

#Rigidizador de cierre de la ménsula
zMens=cantoPerfilVAtado/2.0-cantoPerfilVcarr-cantoPerfilMens/2.0
vOrigenL=Base.Vector(0,cantoPerfilPilar/2.0+LMensula,zMens)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(0,1,0)
listaCoordChapaL=[[anchoPerfilMens/2.0,-cantoPerfilMens/2.0],[anchoPerfilMens/2.0,cantoPerfilMens/2.0],[-anchoPerfilMens/2.0,cantoPerfilMens/2.0],[-anchoPerfilMens/2.0,-cantoPerfilMens/2.0]]
listaCoordAgujL=[]
espesorChapa=erigCierrMens
diamAguj=0
rigcier=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(rigcier)

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

ocultas='n'
SupInf='Sup'
geometry_3D.vistaPlanta(App,escala,Pieza,ocultas,SupInf)
AntPost='Ant'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)
