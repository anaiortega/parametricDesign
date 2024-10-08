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

#Placa base tipo 2
#El origen de coordenadas (X,Y) se sitúa sobre el eje del pilar. El
#origen de Z está en la cara inferior de la placa base.

docName='placa_base_tipo3'
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
dimXPlaca=475               #ancho de la placa base (dirección X) (solo de la parte rectangular)
dimYPlaca=900               #largo de la placa base (dirección Y)
ePlaca=25                   #espesor de la placa base (dirección Z)
xminPlaca=-dimXPlaca/2.0    #coordenada X mínima de la placa
yminPlaca=-dimYPlaca/2.0    #coordenada Y mínima de la placa
holgPbaseRigV=50            #holgura en el chaflán de la placa base a ambos lados del rigidizador vertical
distRigVbordePbase=60       #distancia de la cara exterior del rigidizador vertical al borde de la placa base
#Agujeros (matriz 1)
nXFilasAg1=2                 #nº de filas de agujeros en dirección X
dXFilasAg1=[250]             #distancia entre filas de agujeros en dirección X
nYFilasAg1=4                 #nº de filas de agujeros en dirección Y
dYFilasAg1=[120,240,120]     #distancia entre filas de agujeros en dirección
xminAg1=-(dXFilasAg1[0]/2.0)                #coord. X del centro del agujero con X mímima
yminAg1=-240                 #coord. Y del centro del agujero con Y mímima
fiAguj1=18                   #diámetro de los agujeros
#Agujeros (matriz 2)
nXFilasAg2=1                 #nº de filas de agujeros en dirección X
dXFilasAg2=[]                #distancia entre filas de agujeros en dirección X
nYFilasAg2=2                 #nº de filas de agujeros en dirección Y
dYFilasAg2=[240]             #distancia entre filas de agujeros en dirección
xminAg2=170/2.0+125          #coord. X del centro del agujero con X mímima
yminAg2=-120                 #coord. Y del centro del agujero con Y mímima
fiAguj2=18                   #diámetro de los agujeros

#arriostramiento (ver figura relativa a la rutina metallic_struct.arriostr1Tubo)
tipoPerfilArr='huecoCuad'      #tipo de perfil de la diagonal del arriostramiento
idPerfilArr='140.8' 
anchoPerfilArr=metallic_profiles.huecoCuad[idPerfilArr]['a']
hOrigenArr=250                 #distancia vertical entre el lado horizontal de la cartela y el punto de
                               #intersección de eje de la diagonal con el plano de inicio de la misma
eCartArr=13                    #espesor de la cartela del arriostramiento
solapeArrCart=100              #longitud de solape entre la cartela del arriostramiento y la diagonal
holguraCartArr=25              #holgura del chaflán de la cartela a cada lado del perfil
VPteArr=4445                   #VPteArr y HPteArr definen la pendiente de la diagonal
HPteArr=2550
ang1=30                        #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado vertical
ang2=math.degrees(math.atan(1.0*HPteArr/VPteArr))                 #ángulo entre el eje de la diagonal y el lado de la cartela contiguo a su lado horizontal
LArr=500                       #longitud de diagonal a representar

#Rigidizador vertical
dimYRig=250               #ancho del rigidizador (dirección Y)
dimZRig=150               #altura del rigidizador (dirección Z)
eRig=13                   #espesor del rigidizador (dirección Z)

#general
Lpilar=750                  #longitud de pilar a representar
#planos
escala=1                    #escala para generar planos
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


#Rigidizador vertical
#  valores auxiliares
alfarad=math.atan(1.0*abs(HPteArr)/abs(VPteArr))
zPto1=hOrigenArr
yPto1=1.0*zPto1*abs(HPteArr)/abs(VPteArr)
yPto2=solapeArrCart*math.sin(alfarad)
yaux=(anchoPerfilArr/2.0+holguraCartArr)*math.cos(alfarad)

xOrRig=yPto1+yPto2+yaux
yOrRig=-dimYRig/2.0
zOrRig=ePlaca
vOrigenL=Base.Vector(xOrRig,yOrRig,zOrRig)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[0,0],[dimYRig,0],[dimYRig,dimZRig],[0,dimZRig]]
altura=eRig
rig=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(rig)

#Placa base
#valores auxiliares
xaux=xOrRig+eRig+distRigVbordePbase-xminPlaca-dimXPlaca
yaux=dimYPlaca+yminPlaca-(dimYRig/2.0+holgPbaseRigV)
vOrigenL=Base.Vector(xminPlaca,yminPlaca,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordL=[[0,0],[dimXPlaca,0],[dimXPlaca+xaux,dimYPlaca-yaux-dimYRig-2*holgPbaseRigV],[dimXPlaca+xaux,dimYPlaca-yaux],[dimXPlaca,dimYPlaca],[0,dimYPlaca]]
altura=ePlaca
placa=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(placa)


#Agujeros en placa base (matriz 1)
vOrigenL=Base.Vector(xminAg1,yminAg1,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordCentrosL=[]
diametro=fiAguj1
altura=ePlaca
xLinic=0
yLinic=0
for i in range(0,nXFilasAg1):
    for j in range (0,nYFilasAg1):
        centro=[xLinic+math.fsum(dXFilasAg1[0:i]),yLinic+math.fsum(dYFilasAg1[0:j])]
        listaCoordCentrosL.append(centro)

aguj1=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(aguj1)

#Agujeros en placa base (matriz 2)
vOrigenL=Base.Vector(xminAg2,yminAg2,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordCentrosL=[]
diametro=fiAguj2
altura=ePlaca
xLinic=0
yLinic=0
for i in range(0,nXFilasAg2):
    for j in range (0,nYFilasAg2):
        centro=[xLinic+math.fsum(dXFilasAg2[0:i]),yLinic+math.fsum(dYFilasAg2[0:j])]
        listaCoordCentrosL.append(centro)

aguj2=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(aguj2)

#arriostramiento
PtoTrabajo=Base.Vector(0,0,ePlaca)
PtoOrigenCart=Base.Vector(eAlmaPerfil/2.0,0,ePlaca)
plano='XZ'
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
diagonal=metallic_struct.arriostr1Tubo(PtoTrabajo,PtoOrigenCart,plano,tipoPerfilDiag,idPerfilDiag,VOrigenPerf,eCartela,solapePerfCart,holguraCart,alfa1,alfa2,VPte,HPte,LPerf)

Part.show(pieza,'pieza')
Part.show(diagonal,'diagonal')

views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.pieza,docGeom.diagonal],scale=0.10,pageTemplate='A3_Landscape_blank.svg')

