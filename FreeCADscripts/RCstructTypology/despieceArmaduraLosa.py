# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCADcivilOrt 
from freeCADcivilOrt import Arma2d
from FreeCAD import Base
from Draft import *

elosa=0.45 #espesor de la losa
recNominal=0.05
hTextosArmados=0.125

#ptos para definicion geometrica de secciones longitudinales
#cara superior
Pl1=Base.Vector(0,0)
Pl2=Base.Vector(0.6,0)
Pl3=Base.Vector(1.5,0)
Pl4=Base.Vector(3.30,0)
Pl5=Base.Vector(4.61,0)
Pl6=Base.Vector(15.2,0)
Pl7=Base.Vector(15.8,0)
Pl8=Base.Vector(16.7,0)
Pl9=Base.Vector(17.3,0)
#cara inferior
Pl1i=Pl1.add(Base.Vector(0,-elosa))
Pl2i=Pl2.add(Base.Vector(0,-elosa))
Pl3i=Pl3.add(Base.Vector(0,-elosa))
Pl4i=Pl4.add(Base.Vector(0,-elosa))
Pl5i=Pl5.add(Base.Vector(0,-elosa))
Pl6i=Pl6.add(Base.Vector(0,-elosa))
Pl7i=Pl7.add(Base.Vector(0,-elosa))
Pl8i=Pl8.add(Base.Vector(0,-elosa))
Pl9i=Pl9.add(Base.Vector(0,-elosa))


#ptos para definicion geometrica de secciones transversales
#cara superior
Pt1=Base.Vector(0,0)
Pt2=Base.Vector(0.8,0)
Pt3=Base.Vector(2,0)
Pt4=Base.Vector(2.2,0)
Pt5=Base.Vector(2.90,0)
Pt6=Base.Vector(3.40,0)
Pt7=Base.Vector(7.35,0)
Pt8=Base.Vector(8.55,0)
Pt9=Base.Vector(8.55,0)
Pt10=Base.Vector(8.75,0)
Pt11=Base.Vector(9.95,0)
Pt12=Base.Vector(10.75,0)
#cara inferior
Pt1i=Pt1.add(Base.Vector(0,-elosa))
Pt2i=Pt2.add(Base.Vector(0,-elosa))
Pt3i=Pt3.add(Base.Vector(0,-elosa))
Pt4i=Pt4.add(Base.Vector(0,-elosa))
Pt5i=Pt5.add(Base.Vector(0,-elosa))
Pt6i=Pt6.add(Base.Vector(0,-elosa))
Pt7i=Pt7.add(Base.Vector(0,-elosa))
Pt8i=Pt8.add(Base.Vector(0,-elosa))
Pt9i=Pt9.add(Base.Vector(0,-elosa))
Pt10i=Pt10.add(Base.Vector(0,-elosa))
Pt11i=Pt11.add(Base.Vector(0,-elosa))
Pt12i=Pt12.add(Base.Vector(0,-elosa))

familiasArmad={}
familiasArmad['1S']={
   'identificador':'1S',
   'diametro':0.016,
   'separacion':0.20,
   'listaPtos':[Pl1i,Pl1,Pl4,Pl4i],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.2,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt8,Pt11],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['1I']={
   'identificador':'1I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl2i,Pl4i,Pl4],
   'listaRec':[recNominal,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.3,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt8i,Pt11i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['2S']={
   'identificador':'2S',
   'diametro':0.016,
   'separacion':0.20,
   'listaPtos':[Pl1i,Pl1,Pl5,Pl5i],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.2,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt6,Pt8],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['2I']={
   'identificador':'2I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl2i,Pl5i,Pl5],
   'listaRec':[recNominal,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.3,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt6i,Pt8i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['3S']={
   'identificador':'3S',
   'diametro':0.016,
   'separacion':0.20,
   'listaPtos':[Pl3i,Pl3,Pl5,Pl5i],
   'listaRec':[recNominal,recNominal+0.02,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt5,Pt6],
   'recSec':recNominal+0.02,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['3I']={
   'identificador':'3I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl3,Pl3i,Pl5i,Pl5],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt5i,Pt6i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['4S']={
   'identificador':'4S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl3i,Pl3,Pl3.add(Base.Vector(12+recNominal-0.33,0))],
   'listaRec':[recNominal,recNominal+0.02],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':0,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt2,Pt5],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['4I']={
   'identificador':'4I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl3,Pl3i,Pl3i.add(Base.Vector(12+recNominal-0.33,0))],
   'listaRec':[recNominal,recNominal+0.012],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt2i,Pt5i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['5S']={
   'identificador':'5S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl3.add(Base.Vector(12+recNominal-0.33,0)),Pl9,Pl9i],
   'listaRec':[recNominal+0.02,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.60,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt2,Pt5],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['5I']={
   'identificador':'5I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl3i.add(Base.Vector(12+recNominal-0.33,0)),Pl9i,Pl9],
   'listaRec':[recNominal+0.012,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.45,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt2i,Pt5i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}

familiasArmad['6S']={
   'identificador':'6S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl6i,Pl6,Pl9,Pl9i],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt5,Pt7],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['6I']={
   'identificador':'6I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl6,Pl6i,Pl9i,Pl9],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt5i,Pt7i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}

familiasArmad['7']={
   'identificador':'7',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pl6i,Pl6,Pl7,Pl7i,Pl6i],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-recNominal,
   'gapFin':-recNominal,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt7,Pt11],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['8S']={
   'identificador':'8S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt6i,Pt6,Pt12,Pt12i],
   'listaRec':[recNominal,recNominal+0.016,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':0.334,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl2,Pl3],
   'recSec':recNominal+0.016,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['8I']={
   'identificador':'8I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt6,Pt6i,Pt11i],
   'listaRec':[recNominal,recNominal+0.012],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':0.30,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl2i,Pl3i],
   'recSec':recNominal+0.012,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['9S']={
   'identificador':'9S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt6,Pt12,Pt12i],
   'listaRec':[recNominal+0.016,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':0.334,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl3,Pl4],
   'recSec':recNominal+0.016,
   'recLateral':0,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['9I']={
   'identificador':'9I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt2i,Pt11i],
   'listaRec':[recNominal+0.012],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.30,
   'gapFin':0.30,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl3i,Pl4i],
   'recSec':recNominal+0.012,
   'recLateral':0,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['10S']={
   'identificador':'10S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt6,Pt8,Pt8i],
   'listaRec':[recNominal+0.016,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl4,Pl5],
   'recSec':recNominal+0.016,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['10I']={
   'identificador':'10I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt2i,Pt8i,Pt8],
   'listaRec':[recNominal+0.012,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.30,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl4i,Pl5i],
   'recSec':recNominal+0.012,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['11S']={
   'identificador':'11S',
   'diametro':0.020,
   'separacion':0.20,
   'listaPtos':[Pt1i,Pt1,Pt6],
   'listaRec':[recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.45,
   'gapFin':1.2,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl3,Pl5],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['12S']={
   'identificador':'12S',
   'diametro':0.020,
   'separacion':0.20,
   'listaPtos':[Pt1i,Pt1,Pt5,Pt5i],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.45,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl5,Pl6],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['12I']={
   'identificador':'12I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt1,Pt1i,Pt5i,Pt5],
   'listaRec':[recNominal,recNominal,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':-0.10,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl5i,Pl6i],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['13S']={
   'identificador':'13S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt1i,Pt1,Pt12,Pt12i],
   'listaRec':[recNominal,recNominal+0.012,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.118,
   'gapFin':0.118,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl6,Pl7],
   'recSec':recNominal+0.012,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['13I']={
   'identificador':'13I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt2i,Pt11i],
   'listaRec':[recNominal+0.012],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.30,
   'gapFin':0.30,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl6i,Pl7i],
   'recSec':recNominal,
   'recLateral':recNominal+0.012,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['14S']={
   'identificador':'14S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt1i,Pt1,Pt7,Pt7i],
   'listaRec':[recNominal,recNominal+0.012,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.118,
   'gapFin':-0.10,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl7,Pl8],
   'recSec':recNominal+0.012,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['14I']={
   'identificador':'14I',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt2i,Pt7i,Pt7],
   'listaRec':[recNominal+0.012,recNominal],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.30,
   'gapFin':-0.1,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl7i,Pl8i],
   'recSec':recNominal,
   'recLateral':recNominal+0.012,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}

familiasArmad['15S']={
   'identificador':'15S',
   'diametro':0.016,
   'separacion':0.10,
   'listaPtos':[Pl2,Pl3],
   'listaRec':[recNominal+0.008],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.60,
   'gapFin':0.60,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt3,Pt4],
   'recSec':recNominal+0.008,
   'recLateral':recNominal+0.008,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['15I']={
   'identificador':'15I',
   'diametro':0.016,
   'separacion':0.10,
   'listaPtos':[Pl2i,Pl3i],
   'listaRec':[recNominal+0.008],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.60,
   'gapFin':0.60,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt3i,Pt4i],
   'recSec':recNominal+0.008,
   'recLateral':recNominal+0.008,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}

familiasArmad['16S']={
   'identificador':'16S',
   'diametro':0.016,
   'separacion':0.10,
   'listaPtos':[Pl7,Pl8],
   'listaRec':[recNominal+0.008],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.60,
   'gapFin':0.60,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt9,Pt10],
   'recSec':recNominal+0.008,
   'recLateral':recNominal+0.008,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['16I']={
   'identificador':'16I',
   'diametro':0.016,
   'separacion':0.10,
   'listaPtos':[Pl7i,Pl8i],
   'listaRec':[recNominal+0.008],
   'lado':'i',
   'radioDob':0.03,
   'gapIni':0.60,
   'gapFin':0.60,
   'vectorLRef':Base.Vector(0.5,-0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pt9i,Pt10i],
   'recSec':recNominal+0.008,
   'recLateral':recNominal+0.008,
   'ladoDibSec':'i',
   'vectorLRefSec':Base.Vector(-0.3,-0.3)
}
familiasArmad['17']={
   'identificador':'17',
   'diametro':0.008,
   'separacion':0.15,
   'listaPtos':[Pt3i,Pt3,Pt4,Pt4i,Pt3i],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-recNominal,
   'gapFin':-recNominal,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl2,Pl3],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}
familiasArmad['18']={
   'identificador':'18',
   'diametro':0.008,
   'separacion':0.15,
   'listaPtos':[Pt9i,Pt9,Pt10,Pt10i,Pt9i],
   'listaRec':[recNominal,recNominal,recNominal,recNominal],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':-recNominal,
   'gapFin':-recNominal,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl7,Pl8],
   'recSec':recNominal,
   'recLateral':recNominal,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}

familiasArmad['R1S']={
   'identificador':'R1S',
   'diametro':0.012,
   'separacion':0.20,
   'listaPtos':[Pt8,Pt11],
   'listaRec':[recNominal+0.012],
   'lado':'d',
   'radioDob':0.03,
   'gapIni':0.45,
   'gapFin':0.45,
   'vectorLRef':Base.Vector(0.5,0.5),
   'hTexto':hTextosArmados,
   'ptosExtension':[Pl3,Pl4],
   'recSec':recNominal+0.012,
   'recLateral':recNominal+0.1,
   'ladoDibSec':'d',
   'vectorLRefSec':Base.Vector(-0.3,0.3)
}

#SECCIONES LONGITUDINALES
#sección A-A
App.newDocument("secAA")
l1=makeWire([Pl1i,Pl1,Pl2,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl3i,Pl3,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('4S','4I','5S','5I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('11S','9I','10I','12S','12I','13S','13I','14S','14I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección B-B
App.newDocument("secBB")
l1=makeWire([Pl1i,Pl1,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl2i,Pl8i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('4S','4I','5S','5I','15S','15I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('11S','9I','10I','12S','12I','13S','13I','14S','14I','17')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección C-C
App.newDocument("secCC")
l1=makeWire([Pl1i,Pl1,Pl2,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl3i,Pl3,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('4S','4I','5S','5I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('11S','9I','10I','12S','12I','13S','13I','14S','14I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección D-D
App.newDocument("secDD")
l1=makeWire([Pl1i,Pl1,Pl2,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl3,Pl5,Pl5i,Pl3i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl6i,Pl6,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('3S','3I','6S','6I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('11S','9I','10I','13S','13I','14S','14I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección E-E
App.newDocument("secEE")
l1=makeWire([Pl1i,Pl1,Pl5,Pl5i,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl6i,Pl6,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('2S','2I','6S','6I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('8S','8I','9S','9I','10S','10I','13S','13I','14S','14I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección F-F
App.newDocument("secFF")
l1=makeWire([Pl1i,Pl1,Pl5,Pl5i,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl6,Pl7,Pl7i,Pl6i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl8,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('2S','2I','7')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('8S','8I','9S','9I','10S','10I','13S','13I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección G-G
App.newDocument("secGG")
l1=makeWire([Pl1i,Pl1,Pl4,Pl4i,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl6i,Pl6,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('1S','1I','7','16S','16I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('8S','8I','9S','9I','13S','13I','R1S','18')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección H-H
App.newDocument("secHH")
l1=makeWire([Pl1i,Pl1,Pl4,Pl4i,Pl2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl6,Pl7,Pl7i,Pl6i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pl8i,Pl8,Pl9,Pl9i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('1S','1I','7')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('8S','8I','9S','9I','13S','13I','R1S')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])


#SECCIONES TRANSVERSALES
#sección 1-1
App.newDocument("sec11")
l1=makeWire([Pt1i,Pt1,Pt7,Pt7i,Pt2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt9,Pt10,Pt10i,Pt9i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt11i,Pt11,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('14S','14I','18')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('5S','5I','6S','6I','16S','16I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección 2-2
App.newDocument("sec22")
l1=makeWire([Pt1i,Pt1,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt2i,Pt11i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('13S','13I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('5S','5I','6S','6I','7')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección 3-3
App.newDocument("sec33")
l1=makeWire([Pt1i,Pt1,Pt5,Pt5i,Pt2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt11i,Pt11,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('12S','12I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('4S','4I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección 4-4
App.newDocument("sec44")
l1=makeWire([Pt1i,Pt1,Pt8,Pt8i,Pt2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt11i,Pt11,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('11S','10S','10I')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('4S','4I','3S','3I','2S','2I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección 5-5
App.newDocument("sec55")
l1=makeWire([Pt1i,Pt1,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt2i,Pt11i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('11S','9S','9I','R1S')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('4S','4I','3S','3I','2S','2I','1S','1I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#sección 6-6
App.newDocument("sec66")
l1=makeWire([Pt1i,Pt1,Pt2,Pt2i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt3,Pt4,Pt4i,Pt3i],True)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)
l1=makeWire([Pt11i,Pt6i,Pt6,Pt12,Pt12i],False)
FreeCADGui.ActiveDocument.getObject(l1.Name).LineColor = (0.00,1.00,0.00)

idArmad=('8S','8I','17')
for i in range (0,len(idArmad)):
    familiasArmad[idArmad[i]]['listaPtosArm']=Arma2d.armadura(identificador=familiasArmad[idArmad[i]]['identificador'],diametro=familiasArmad[idArmad[i]]['diametro'],separacion=familiasArmad[idArmad[i]]['separacion'],listaPtos=familiasArmad[idArmad[i]]['listaPtos'],listaRec=familiasArmad[idArmad[i]]['listaRec'],lado=familiasArmad[idArmad[i]]['lado'],radioDob=familiasArmad[idArmad[i]]['radioDob'],gapIni=familiasArmad[idArmad[i]]['gapIni'],gapFin=familiasArmad[idArmad[i]]['gapFin'],vectorLRef=familiasArmad[idArmad[i]]['vectorLRef'],hTexto=familiasArmad[idArmad[i]]['hTexto'])

idArmaSec=('2S','2I','1S','1I','15S','15I')
for i in range (0,len(idArmaSec)):
   Arma2d.armaSec(identificador=familiasArmad[idArmaSec[i]]['identificador'],diametro=familiasArmad[idArmaSec[i]]['diametro'],separacion=familiasArmad[idArmaSec[i]]['separacion'],recubrimiento=familiasArmad[idArmaSec[i]]['recSec'],reclateral=familiasArmad[idArmaSec[i]]['recLateral'],ptosExtension=familiasArmad[idArmaSec[i]]['ptosExtension'],ladoDibSec=familiasArmad[idArmaSec[i]]['ladoDibSec'],vectorLRefSec=familiasArmad[idArmaSec[i]]['vectorLRefSec'],hTexto=familiasArmad[idArmaSec[i]]['hTexto'])

#DESPIECE DE LA ARMADURA
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hTexto=2.5
Arma2d.cuadroDespiece(anchoColumnas,hFilas,hTexto,familiasArmad)
