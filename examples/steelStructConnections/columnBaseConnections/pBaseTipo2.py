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
from layout_utils import views 

#Placa base tipo 2
#El origen de coordenadas (X,Y) se sitúa sobre el eje del pilar. El
#origen de Z está en la cara inferior de la placa base.

docName='placa_base_tipo2'
docGeom=App.newDocument(docName,docName)

#NOTA: todas las cotas se dan en mm
#****Datos****
#Pilar
tipoPerfil='W'                 #Perfil del pilar
idPerfil='30x173'              #tamaño del perfil del pilar
cantoPerfil=metallic_profiles.W[idPerfil]['h']
eAlmaPerfil=metallic_profiles.W[idPerfil]['e']
eAlaPerfil=metallic_profiles.W[idPerfil]['e1']
bAlaPerfil=metallic_profiles.W[idPerfil]['b']
radioPerfil=metallic_profiles.W[idPerfil]['r']
#Placa
dimXPlaca=475               #ancho de la placa base (dirección X)
dimYPlaca=1200              #largo de la placa base (dirección Y)
ePlaca=25                   #espesor de la placa base (dirección Z)
xminPlaca=-dimXPlaca/2.0      #coordenada X mínima de la placa
yminPlaca=-cantoPerfil/2.0-63.5           #coordenada Y mínima de la placa
#Agujeros
nXFilasAg=2                 #nº de filas de agujeros en dirección X
dXFilasAg=[250]   #distancia entre filas de agujeros en dirección X
nYFilasAg=6                 #nº de filas de agujeros en dirección Y
dYFilasAg=[160,160,160,250,120]         #distancia entre filas de agujeros en dirección
xminAg=-(dXFilasAg[0]/2.0)                #coord. X del centro del agujero con X mímima
yminAg=-160/2.0-160         #coord. Y del centro del agujero con Y mímima
fiAguj=18                   #diámetro de los agujeros

#arriostramiento (ver figura relativa a la rutina metallic_struct.arriostr1Tubo)
tipoPerfilArr='huecoCuad'      #tipo de perfil de la diagonal del arriostramiento
idPerfilArr='140.8' 
anchoPerfilArr=metallic_profiles.huecoCuad[idPerfilArr]['a']
hOrigenArr=600                 #distancia vertical entre el lado horizontal de la cartela y el punto de
                               #intersección de eje de la diagonal con el plano de inicio de la misma
eCartArr=19                    #espesor de la cartela del arriostramiento
solapeArrCart=150              #longitud de solape entre la cartela del arriostramiento y la diagonal
holguraCartArr=25              #holgura del chaflán de la cartela a cada lado del perfil
VPteArr=4420.0                 #VPteArr y HPteArr definen la pendiente de la diagonal
HPteArr=3770.0
ang1=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado vertical
ang2=math.degrees(math.atan(1.0*HPteArr/VPteArr))                 #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado horizontal
LArr=500                       #longitud de diagonal a representar

#Rigidizador vertical
dimXRig=250               #ancho del rigidizador (dirección X)
dimZRig=400               #altura del rigidizador (dirección Z)
eRig=16                   #espesor del rigidizador (dirección Z)

#general
Lpilar=1500                  #longitud de pilar a representar
#planos
escala=1                      #escala para generar planos
#****Fin datos****


#Perfil pilar
ptoIni=Base.Vector(0,0,ePlaca)
ptoFin=Base.Vector(0,0,ePlaca+Lpilar)
perfil=tipoPerfil
tamPerfil=idPerfil
incrIni=0
incrFin=0
giroSec=0
pilar=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pilar

#Placa base
vOrigenL=Base.Vector(xminPlaca,yminPlaca,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordL=[[0,0],[dimXPlaca,0],[dimXPlaca,dimYPlaca],[0,dimYPlaca]]
altura=ePlaca
placa=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(placa)


#Agujeros en placa base
vOrigenL=Base.Vector(xminAg,yminAg,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordCentrosL=[]
diametro=fiAguj
altura=ePlaca
xLinic=0
yLinic=0
for i in range(0,nXFilasAg):
    for j in range (0,nYFilasAg):
        centro=[xLinic+math.fsum(dXFilasAg[0:i]),yLinic+math.fsum(dYFilasAg[0:j])]
        listaCoordCentrosL.append(centro)

aguj=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(aguj)

#Rigidizador vertical
#  valores auxiliares
alfarad=math.atan(1.0*abs(HPteArr)/abs(VPteArr))
zPto1=hOrigenArr
yPto1=1.0*zPto1*abs(HPteArr)/abs(VPteArr)
yPto2=solapeArrCart*math.sin(alfarad)
yaux=(anchoPerfilArr/2.0+holguraCartArr)*math.cos(alfarad)

xOrRig=dimXRig/2
yOrRig=yPto1+yPto2+yaux
zOrRig=ePlaca
vOrigenL=Base.Vector(xOrRig,yOrRig,zOrRig)
vDirXL=Base.Vector(-1,0,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(0,1,0)
listaCoordL=[[0,0],[dimXRig,0],[dimXRig,dimZRig],[0,dimZRig]]
altura=eRig
rig=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(rig)

#arriostramiento
PtoTrabajo=Base.Vector(0,0,ePlaca)
PtoOrigenCart=Base.Vector(0,cantoPerfil/2.0,ePlaca)
plano='YZ'
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
Part.show(pieza,'pieza')

views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.pieza],scale=0.10,pageTemplate='A3_Landscape_blank.svg')

