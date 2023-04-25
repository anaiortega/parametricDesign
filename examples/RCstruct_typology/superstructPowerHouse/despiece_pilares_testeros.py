# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil
from freeCAD_civil import reinf_bars
from FreeCAD import Base
from Draft import *

#****Armado de un pilar con ménsula

dimYPilar=0.5            #dimensión Y del pilar
dimXPilar=0.5            #dimensión X del pilar
dimZpilar=8.2            #dimensión Z del pilar (altura)


recNominal=0.05
hTextosArmados=0.125

#ptos para definicion geométrica de secciones-alzados
#alzado 1
P1=Base.Vector(0,0)
P2=Base.Vector(0,dimZpilar)
P3=Base.Vector(dimYPilar,dimZpilar)
P4=Base.Vector(dimYPilar,0)
#sección 1
P16=Base.Vector(0,0)
P17=P16.add(Base.Vector(0,dimXPilar))
P18=P17.add(Base.Vector(dimYPilar,0))
P19=P16.add(Base.Vector(dimYPilar,0))

fiCercosPilar=8e-3
Lsolapefi25=1.35
recPral=recNominal+fiCercosPilar

familiasArmad={}
familiasArmad['1E']={
   'identificador':'1E',
   'diametro':0.025,
   'separacion':0,
   'nBarras':8,
   'listaPtos':[P1,P1.add(Base.Vector(0,Lsolapefi25))],
   'listaRec':[recPral],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':Lsolapefi25,
   'gapFin':0,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['1P']={
   'identificador':'1P',
   'diametro':0.025,
   'separacion':0,
   'nBarras':8,
   'listaPtos':[P1,P1.add(Base.Vector(0,4+Lsolapefi25))],
   'listaRec':[recPral],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':0,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['2P']={
   'identificador':'2P',
   'diametro':0.020,
   'separacion':0,
   'nBarras':8,
   'listaPtos':[P4.add(Base.Vector(0,4)),P3,P2],
   'listaRec':[recPral,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':-0.1,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['3C']={
   'identificador':'3C',
   'diametro':0.008,
   'separacion':0.20,
   'nBarras':0,
   'listaPtos':[P16,P17,P18,P19,P16],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[P1,P2],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}


familiasArmad['4H']={
   'identificador':'4H',
   'diametro':0.008,
   'separacion':0.20,
   'nBarras':0,
   'listaPtos':[P16,P17],
   'listaRec':[recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[P11,P10],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'i',
}

#Secciones-Alzados
#alzado 1
App.newDocument("alz1")
l1=makeWire([P1,P2,P3,P4],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('1E','1P','2P')

for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('3C',)
for i in range (0,len(idArmaSec)):
   reinf_bars.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])


hTextosArmados=0.05 
#sección 1
App.newDocument("sec1")
l1=makeWire([P16,P17,P18,P19],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('3C','4H')

for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])




#DESPIECE DE LA ARMADURA
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posición, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hTexto=2.5
reinf_bars.cuadroDespiece(anchoColumnas,hFilas,hTexto,familiasArmad)
