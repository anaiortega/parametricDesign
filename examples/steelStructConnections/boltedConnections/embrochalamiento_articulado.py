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
#Embrochalamiento articulado de una viga secundaria en la viga principal con doble
#casquillo de angular (L, de lados iguales). La viga principal se representa en la dirección del eje 
#Y global y la secundaria en la dirección del eje X global


#NOTA: todas las cotas se dan en mm
#****Datos****
#Viga principal
tipoPerfilVPrinc='IPE'        
idPerfilVPrinc='500'
cantoPerfilVPrinc=metallic_profiles.IPE[idPerfilVPrinc]['h']
eAlmaPerfilVPrinc=metallic_profiles.IPE[idPerfilVPrinc]['e']
eAlaPerfilVPrinc=metallic_profiles.IPE[idPerfilVPrinc]['e1']
#Viga secundaria
tipoPerfilVSec='IPE'        
idPerfilVSec='300'
cantoPerfilVSec=metallic_profiles.IPE[idPerfilVSec]['h']
eAlmaPerfilVSec=metallic_profiles.IPE[idPerfilVSec]['e']
eAlaPerfilVSec=metallic_profiles.IPE[idPerfilVSec]['e1']
#Casquillo de angular
tipoPerfilCasq='L'
idPerfilCasq='120x10'
ePerfilCasq=metallic_profiles.L[idPerfilCasq]['e']
dcdgCasq=metallic_profiles.L[idPerfilCasq]['cx']
dimZCasq=240                    #dimensión Z (altura) del casquillo
#Tornillos
nFilasTorn=3                    #nº de filas de tornillos
dFilasTorn=[70,70]              #distancias entre filas de tornillos (de arriba a abajo). La 1ª fila es de Z mayor
dZCSCasqFilaS=50                #distancia Z desde la cara superior del casquillo hasta la fila más alta
dYAlmaVSecTorn=60               #distancia Y entre la cara del alma de la viga secundaria y la columna de tornillos
dXAlmaVPrincTorn=60             #distancia X entre la cara del alma de la viga principal y la columna de tornillos
fiAgujVprinc=20                 #diámetro de los agujeros en viga pral.
fiAgujVsec=25                   #diámetro de los agujeros en viga secundaria
#general
LVprinc=1000                    #longitud (dirección Y) de la viga principal a representar
LVsec=500                       #longitud (dirección X) de la viga principal a representar
#planos
escala=1                        #escala para generar planos
#****Fin datos****


#Viga principal
ptoIni=Base.Vector(0,-LVprinc/2,0)
ptoFin=Base.Vector(0,LVprinc/2,0)
perfil=tipoPerfilVPrinc
tamPerfil=idPerfilVPrinc
incrIni=0
incrFin=0
giroSec=0
vprinc=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=vprinc
#Viga secundaria
ptoIni=Base.Vector(eAlmaPerfilVPrinc/2,0,0)
ptoFin=Base.Vector(LVsec,0,0)
perfil=tipoPerfilVSec
tamPerfil=idPerfilVSec
incrIni=0
incrFin=0
giroSec=0
vsec=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(vsec)
#Casquillos de angular
ptoIni=Base.Vector(eAlmaPerfilVPrinc/2+dcdgCasq,eAlmaPerfilVSec/2+dcdgCasq,-dimZCasq/2)
ptoFin=Base.Vector(eAlmaPerfilVPrinc/2+dcdgCasq,eAlmaPerfilVSec/2+dcdgCasq,dimZCasq/2)
perfil=tipoPerfilCasq
tamPerfil=idPerfilCasq
incrIni=0
incrFin=0
giroSec=180
casq1=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(casq1)

ptoIni=Base.Vector(eAlmaPerfilVPrinc/2+dcdgCasq,-eAlmaPerfilVSec/2-dcdgCasq,-dimZCasq/2)
ptoFin=Base.Vector(eAlmaPerfilVPrinc/2+dcdgCasq,-eAlmaPerfilVSec/2-dcdgCasq,dimZCasq/2)
perfil=tipoPerfilCasq
tamPerfil=idPerfilCasq
incrIni=0
incrFin=0
giroSec=90
casq1=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(casq1)

#Agujeros sobre viga principal
vOrigenL=Base.Vector(-eAlmaPerfilVPrinc/2,0,0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordCentrosL=[]
diametro=fiAgujVprinc
altura=eAlmaPerfilVPrinc+ePerfilCasq
xLinic=-eAlmaPerfilVSec/2-dYAlmaVSecTorn
yLinic=dimZCasq/2-dZCSCasqFilaS
for i in range(0,nFilasTorn):
    centro=[xLinic,yLinic-math.fsum(dFilasTorn[0:i])]
    listaCoordCentrosL.append(centro)

agujAlmaP1=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlmaP1)

listaCoordCentrosL=[]
xLinic=eAlmaPerfilVSec/2+dYAlmaVSecTorn
for i in range(0,nFilasTorn):
    centro=[xLinic,yLinic-math.fsum(dFilasTorn[0:i])]
    listaCoordCentrosL.append(centro)

agujAlmaP2=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlmaP2)

#Agujeros en viga secundaria
vOrigenL=Base.Vector(0,-eAlmaPerfilVSec/2-ePerfilCasq,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(0,1,0)
listaCoordCentrosL=[]
diametro=fiAgujVsec
altura=eAlmaPerfilVSec+2*ePerfilCasq
xLinic=eAlmaPerfilVPrinc/2+dXAlmaVPrincTorn
yLinic=dimZCasq/2-dZCSCasqFilaS
for i in range(0,nFilasTorn):
    centro=[xLinic,yLinic-math.fsum(dFilasTorn[0:i])]
    listaCoordCentrosL.append(centro)

agujAlmaS=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(agujAlmaS)

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
AntPost='Ant'
geometry_3D.vistaFront(App,escala,Pieza,ocultas,AntPost)
IzqDer='Der'
geometry_3D.vistaLat(App,escala,Pieza,ocultas,IzqDer)
