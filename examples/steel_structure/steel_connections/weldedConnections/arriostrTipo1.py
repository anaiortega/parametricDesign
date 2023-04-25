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

#Arriostramiento tipo 1 
docName='arriostr_tipo1'
docGeom=App.newDocument(docName,docName)

#****Datos****
#Viga
tipoPerfilViga='W'        
idPerfilViga='18x35'
cantoPerfilViga=metallic_profiles.W[idPerfilViga]['h']
anchoPerfilViga=metallic_profiles.W[idPerfilViga]['b']
eAlmaPerfilViga=metallic_profiles.W[idPerfilViga]['e']
eAlaPerfilViga=metallic_profiles.W[idPerfilViga]['e1']
#Arriostramiento izquierdo
tipoPerfilArrI='huecoCuad'        
idPerfilArrI='140.8'
cantoPerfilArrI=metallic_profiles.huecoCuad[idPerfilArrI]['a']
anchoPerfilArrI=metallic_profiles.huecoCuad[idPerfilArrI]['a']
ePerfilArrI=metallic_profiles.W[idPerfilArrI]['e']
#Arriostramiento derecho
tipoPerfilArrD='huecoCuad'        
idPerfilArrD='140.8'
cantoPerfilArrD=metallic_profiles.huecoCuad[idPerfilArrI]['a']
anchoPerfilArrD=metallic_profiles.huecoCuad[idPerfilArrI]['a']
ePerfilArrD=metallic_profiles.W[idPerfilArrI]['e']
#Cartela
pteArrI=4445.0/2550.0          #tangente del ángulo que forma al arriostramiento
                               #izquierdo con la horizontal (zI/yI)
pteArrD=pteArrI                #tangente del ángulo que forma al arriostramiento
                               #derecho con la horizontal (zD/yD)
hCart=275                      #altura cartela
eCart=13                       #espesor de la cartela
slpArrCart=150                 #solape entre arriostramiento y cartela
holguraCart=25                 #holgura del corte en la cartela a cada lado del
                               #perfil de los arriostramiento
#general
LViga=500                      #longitud (dirección Y) de cada extremo de la viga
LArrI=300                      #longitud del arriostramiento izqdo.
LArrD=300                      #longitud del arriostramiento drcho.
#planos
escala=1                        #escala para generar planos
###Fin datos

#valores auxiliares
alfaIrad=math.atan(1.0/pteArrI)  #ángulo que forma el arriostramiento izqdo. con la vertical
hipotCorteI=cantoPerfilArrI+2*holguraCart    #hipotenusa del corte en el lado izqudo. de la cartela
zCorteI=hipotCorteI*math.sin(alfaIrad)      #altura del corte en el lado izqudo. de la cartela
yCorteI=hipotCorteI*math.cos(alfaIrad)      #base del corte en el lado izqudo. de la cartela
alfaDrad=math.atan(1.0/pteArrD)  #ángulo que forma el arriostramiento drcho. con la vertical
hipotCorteD=cantoPerfilArrD+2*holguraCart    #hipotenusa del corte en el lado drcho. de la cartela
zCorteD=hipotCorteD*math.sin(alfaDrad)      #altura del corte en el lado drcho. de la cartela
yCorteD=hipotCorteD*math.cos(alfaDrad)      #base del corte en el lado drcho. de la cartela
bCartI=(cantoPerfilViga/2+hCart-zCorteI/2)/pteArrI+yCorteI/2
bCartD=(cantoPerfilViga/2+hCart-zCorteD/2)/pteArrD+yCorteD/2
PtoCorteEjeI=Base.Vector(0,-(bCartI-yCorteI/2.0),-(cantoPerfilViga/2.0+hCart-zCorteI/2.0))
PtoCorteEjeD=Base.Vector(0,bCartD-yCorteD/2.0,-(cantoPerfilViga/2+hCart-zCorteD/2.0))
#Viga
ptoIni=Base.Vector(0,-LViga,0)
ptoFin=Base.Vector(0,LViga,0)
perfil=tipoPerfilViga
tamPerfil=idPerfilViga
incrIni=0
incrFin=0
giroSec=0
viga=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=viga

#Cartela
vOrigenL=Base.Vector(-eCart/2.0,0,-cantoPerfilViga/2.0)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,-1)
vDirZL=Base.Vector(1,0,0)
listaCoordChapaL=[[-bCartI,0],[-bCartI,hCart-zCorteI],[-(bCartI-yCorteI),hCart],[bCartD-yCorteD,hCart],[bCartD,hCart-zCorteD],[bCartD,0]]
listaCoordAgujL=[]
espesorChapa=eCart
diamAguj=0
cartela=metallic_struct.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(cartela)

#Arriostramiento izquierdo
ptoIni=PtoCorteEjeI
ptoFin=PtoCorteEjeI.add(Base.Vector(0,-LArrI*math.sin(alfaIrad),-LArrI*math.cos(alfaIrad)))
perfil=tipoPerfilArrI
tamPerfil=idPerfilArrI
incrIni=slpArrCart
incrFin=0
giroSec=0
arrI=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
arrI=arrI.cut(cartela)

#Arriostramiento derecho
ptoIni=PtoCorteEjeD
ptoFin=PtoCorteEjeD.add(Base.Vector(0,LArrD*math.sin(alfaDrad),-LArrD*math.cos(alfaDrad)))
perfil=tipoPerfilArrD
tamPerfil=idPerfilArrD
incrIni=slpArrCart
incrFin=0
giroSec=0
arriostr=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
Part.show(arrI,'arrI')
Part.show(pieza,'pieza')
Part.show(arriostr,'arriostr')
views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.arrI,docGeom.pieza,docGeom.arriostr],scale=0.10,pageTemplate='A3_Landscape_blank.svg')


