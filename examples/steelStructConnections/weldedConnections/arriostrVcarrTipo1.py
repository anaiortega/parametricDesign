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

#Arriostramiento tipo 1 
#****Datos****
#Viga de atado (y de acompañamiento de la carrilera)
tipoPerfilViga='W'        
idPerfilViga='18x35'
cantoPerfilViga=PerfilesMetalicos.W[idPerfilViga]['h']
anchoPerfilViga=PerfilesMetalicos.W[idPerfilViga]['b']
eAlmaPerfilViga=PerfilesMetalicos.W[idPerfilViga]['e']
eAlaPerfilViga=PerfilesMetalicos.W[idPerfilViga]['e1']
#Arriostramiento izquierdo
tipoPerfilArrI='huecoCuad'        
idPerfilArrI='140.8'
cantoPerfilArrI=PerfilesMetalicos.huecoCuad[idPerfilArrI]['a']
anchoPerfilArrI=PerfilesMetalicos.huecoCuad[idPerfilArrI]['a']
ePerfilArrI=PerfilesMetalicos.W[idPerfilArrI]['e']
#Arriostramiento derecho
tipoPerfilArrD='huecoCuad'        
idPerfilArrD='140.8'
cantoPerfilArrD=PerfilesMetalicos.huecoCuad[idPerfilArrI]['a']
anchoPerfilArrD=PerfilesMetalicos.huecoCuad[idPerfilArrI]['a']
ePerfilArrD=PerfilesMetalicos.W[idPerfilArrI]['e']
#Cartela
pteArrI=4420.0/2550.0          #tangente del ángulo que forma al arriostramiento
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

#Datos de viga carrilera
tipoPerfilVcarr='W'        
idPerfilVcarr='24x146'
cantoPerfilVcarr=PerfilesMetalicos.W[idPerfilVcarr]['h']
anchoPerfilVcarr=PerfilesMetalicos.W[idPerfilVcarr]['b']
eAlmaPerfilVcarr=PerfilesMetalicos.W[idPerfilVcarr]['e']
eAlaPerfilVcarr=PerfilesMetalicos.W[idPerfilVcarr]['e1']

dEjesVcarrVac=700               #distancia entre los ejes de la viga carrilera y de la viga de acompañamiento

eChapaCab=19                    #espesor de la capa de unión entre cabezas de viga carrilera y de viga de acompañamiento
slpChapaVcarr=50                #solape entre la chapa y la cabeza de la viga carrilera
slpChapaViga=50                 #solape entre la chapa y la cabeza de la viga de acompañamiento

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
viga=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
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
cartela=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(cartela)

#Arriostramiento izquierdo
ptoIni=PtoCorteEjeI
ptoFin=PtoCorteEjeI.add(Base.Vector(0,-LArrI*math.sin(alfaIrad),-LArrI*math.cos(alfaIrad)))
perfil=tipoPerfilArrI
tamPerfil=idPerfilArrI
incrIni=slpArrCart
incrFin=0
giroSec=0
arrI=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
arrI=arrI.cut(cartela)

#Arriostramiento derecho
ptoIni=PtoCorteEjeD
ptoFin=PtoCorteEjeD.add(Base.Vector(0,LArrD*math.sin(alfaDrad),-LArrD*math.cos(alfaDrad)))
perfil=tipoPerfilArrD
tamPerfil=idPerfilArrD
incrIni=slpArrCart
incrFin=0
giroSec=0
arriostr=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
arriostr.add(arrI)

#Viga carrilera
ptoIni=Base.Vector(-dEjesVcarrVac,-LViga,cantoPerfilViga/2.0-cantoPerfilVcarr/2.0)
ptoFin=Base.Vector(-dEjesVcarrVac,LViga,cantoPerfilViga/2.0-cantoPerfilVcarr/2.0)
perfil=tipoPerfilVcarr
tamPerfil=idPerfilVcarr
incrIni=0
incrFin=0
giroSec=0
viga=Metalicas.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pieza.fuse(viga)


#Chapa de unión de cabezas de vigas
anchoChap=dEjesVcarrVac-anchoPerfilVcarr/2.0-anchoPerfilViga/2.0+slpChapaVcarr+slpChapaViga
largoChap=2*LViga
vOrigenL=Base.Vector(-anchoPerfilViga/2.0+slpChapaViga,-LViga,cantoPerfilViga/2.0)
vDirXL=Base.Vector(-1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL=[[0,0],[anchoChap,0],[anchoChap,largoChap],[0,largoChap]]
listaCoordAgujL=[]
espesorChapa=eChapaCab
diamAguj=0
chapa=Metalicas.chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
pieza=pieza.fuse(chapa)


arriostr.add(pieza)
Part.show(arriostr)




#****Representación en planos
Pieza=FreeCAD.ActiveDocument.addObject("Part::Feature","Pieza")
Pieza.Shape=arriostr
FreeCADGui.Selection.addSelection(Pieza)

Geometria3D.vistasIsom(App,escala,Pieza)
ocultas='n'
Geometria3D.vistaPlanta(App,escala,Pieza,ocultas,'Sup')
Geometria3D.vistaFront(App,escala,Pieza,ocultas,'Ant')
Geometria3D.vistaLat(App,escala,Pieza,ocultas,'Izq')
