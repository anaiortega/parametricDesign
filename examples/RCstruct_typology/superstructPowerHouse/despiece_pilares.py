# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil
from freeCAD_civil import reinf_bars
from FreeCAD import Base
from Draft import *

#****Armado de un pilar con ménsula

dimYPilar=0.7            #dimensión Y del pilar
dimXPilar=0.5            #dimensión X del pilar
dimZpilar=8.2            #dimensión Z del pilar (altura)
dimYMensula=0.4
dimZ1Mensula=0.4
dimZ2Mensula=0.4


recNominal=0.05
hTextosArmados=0.125

#ptos para definicion geométrica de secciones-alzados
#alzado 1
P1=Base.Vector(0,0)
P2=Base.Vector(0,dimZpilar)
P3=Base.Vector(dimYPilar,dimZpilar)
P4=Base.Vector(dimYPilar+dimYMensula,dimZpilar)
P5=Base.Vector(dimYPilar+dimYMensula,dimZpilar-dimZ1Mensula)
P6=Base.Vector(dimYPilar,dimZpilar-dimZ1Mensula-dimZ2Mensula)
P7=Base.Vector(dimYPilar,0)
#alzado 2
P8=Base.Vector(0,0)
P9=Base.Vector(0,dimZpilar)
P10=Base.Vector(dimXPilar,dimZpilar)
P11=Base.Vector(dimXPilar,0)
#alzado 3
P12=Base.Vector(0,0)
P13=Base.Vector(0,dimZ1Mensula+dimZ2Mensula/2)
P14=P13.add(Base.Vector(dimXPilar,0))
P15=P12.add(Base.Vector(dimXPilar,0))
#sección 1
P16=Base.Vector(0,0)
P17=P16.add(Base.Vector(0,dimXPilar))
P18=P17.add(Base.Vector(dimYPilar,0))
P19=P16.add(Base.Vector(dimYPilar,0))
#sección 3
P20=Base.Vector(0,0)
P21=P20.add(Base.Vector(0,dimXPilar))
P22=P21.add(Base.Vector(dimYPilar+dimYMensula/2,0))
P23=P20.add(Base.Vector(dimYPilar+dimYMensula/2,0))
#sección 4
P24=Base.Vector(0,0)
P25=P24.add(Base.Vector(0,dimXPilar))
P26=P25.add(Base.Vector(dimYPilar+dimYMensula-0.075,0))
P27=P24.add(Base.Vector(dimYPilar+dimYMensula-0.075,0))
#sección 2
P28=Base.Vector(0,0)
P29=P28.add(Base.Vector(0,dimXPilar))
P30=P29.add(Base.Vector(dimYPilar+dimYMensula-0.15,0))
P31=P28.add(Base.Vector(dimYPilar+dimYMensula-0.15,0))

fiCercosPilar=8e-3
Lsolapefi25=1.35
Lsolapefi20=0.85
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
familiasArmad['2E']={
   'identificador':'2E',
   'diametro':0.020,
   'separacion':0,
   'nBarras':4,
   'listaPtos':[P8,P8.add(Base.Vector(0,Lsolapefi20))],
   'listaRec':[recPral],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':Lsolapefi20,
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
   'nBarras':4,
   'listaPtos':[P8,P9,P10],
   'listaRec':[recPral,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':-0.1,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['3P']={
   'identificador':'3P',
   'diametro':0.020,
   'separacion':0,
   'nBarras':4,
   'listaPtos':[P7.add(Base.Vector(0,4)),P3,P2],
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
familiasArmad['4P']={
   'identificador':'4P',
   'diametro':0.020,
   'separacion':0,
   'nBarras':4,
   'listaPtos':[P1.add(Base.Vector(0,4)),P2,P4,P5,P6],
   'listaRec':[recPral,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':0.60,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['6C']={
   'identificador':'6C',
   'diametro':0.008,
   'separacion':0.25,
   'nBarras':0,
   'listaPtos':[P17,P18,P18.add(Base.Vector(0,-0.380)),P17.add(Base.Vector(0,-0.380)),P17],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[P8,P9],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['5C']={
   'identificador':'5C',
   'diametro':0.008,
   'separacion':0.25,
   'nBarras':0,
   'listaPtos':[P19,P16,P16.add(Base.Vector(0,0.380)),P19.add(Base.Vector(0,0.380)),P19],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
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
familiasArmad['7C']={
   'identificador':'7C',
   'diametro':0.008,
   'separacion':0,
   'nBarras':3,
   'listaPtos':[P24,P25,P26,P27,P24],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['8C']={
   'identificador':'8C',
   'diametro':0.008,
   'separacion':0,
   'nBarras':1,
   'listaPtos':[P20,P21,P22,P23,P20],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}
familiasArmad['9C']={
   'identificador':'9C',
   'diametro':0.008,
   'separacion':0,
   'nBarras':1,
   'listaPtos':[P28,P29,P30,P31,P28],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.05,
   'gapFin':-0.05,
   'vectorLRef':Base.Vector(-0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[],
   'recSec':recPral,
   'recLateral':recPral,
   'ladoDibSec':'d',
}

#Secciones-Alzados
#alzado 1
App.newDocument("alz1")
l1=makeWire([P1,P2,P3,P4,P5,P6,P7],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('1E','1P','3P','4P')

for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('6C',)
for i in range (0,len(idArmaSec)):
   reinf_bars.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#alzado 2
App.newDocument("alz2")
l1=makeWire([P8,P9,P10,P11],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('2E','2P')

for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('6C','5C')
for i in range (0,len(idArmaSec)):
   reinf_bars.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#alzado 3
App.newDocument("alz3")
l1=makeWire([P12,P13,P14,P15],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

hTextosArmados=0.05 
#sección 1
App.newDocument("sec1")
l1=makeWire([P16,P17,P18,P19],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('6C','5C')

for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])


#sección 2
App.newDocument("sec2")
l1=makeWire([P28,P29,P30,P31],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('9C',)
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

#sección 3
App.newDocument("sec3")
l1=makeWire([P20,P21,P22,P23],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('8C',)
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=reinf_bars.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],nBarras=familiasArmad[idArmad[i]]['nBarras'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

#sección 4
App.newDocument("sec4")
l1=makeWire([P24,P25,P26,P27],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
idArmad=('7C',)

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
