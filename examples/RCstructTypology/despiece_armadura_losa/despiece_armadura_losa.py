# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *


elosa=0.45 #espesor de la losa
recNominal=0.05
hTextsArmados=0.125

#ptos para definicion geometrica de secciones longitudinales
#cara superior
Pl1=Vector(0,0)
Pl2=Vector(0.6,0)
Pl3=Vector(1.5,0)
Pl4=Vector(3.30,0)
Pl5=Vector(4.61,0)
Pl6=Vector(15.2,0)
Pl7=Vector(15.8,0)
Pl8=Vector(16.7,0)
Pl9=Vector(17.3,0)
#cara inferior
Pl1i=Pl1.add(Vector(0,-elosa))
Pl2i=Pl2.add(Vector(0,-elosa))
Pl3i=Pl3.add(Vector(0,-elosa))
Pl4i=Pl4.add(Vector(0,-elosa))
Pl5i=Pl5.add(Vector(0,-elosa))
Pl6i=Pl6.add(Vector(0,-elosa))
Pl7i=Pl7.add(Vector(0,-elosa))
Pl8i=Pl8.add(Vector(0,-elosa))
Pl9i=Pl9.add(Vector(0,-elosa))


#ptos para definicion geometrica de secciones transversales
#cara superior
Pt1=Vector(0,0)
Pt2=Vector(0.8,0)
Pt3=Vector(2,0)
Pt4=Vector(2.2,0)
Pt5=Vector(2.90,0)
Pt6=Vector(3.40,0)
Pt7=Vector(7.35,0)
Pt8=Vector(8.55,0)
Pt9=Vector(8.55,0)
Pt10=Vector(8.75,0)
Pt11=Vector(9.95,0)
Pt12=Vector(10.75,0)
#cara inferior
Pt1i=Pt1.add(Vector(0,-elosa))
Pt2i=Pt2.add(Vector(0,-elosa))
Pt3i=Pt3.add(Vector(0,-elosa))
Pt4i=Pt4.add(Vector(0,-elosa))
Pt5i=Pt5.add(Vector(0,-elosa))
Pt6i=Pt6.add(Vector(0,-elosa))
Pt7i=Pt7.add(Vector(0,-elosa))
Pt8i=Pt8.add(Vector(0,-elosa))
Pt9i=Pt9.add(Vector(0,-elosa))
Pt10i=Pt10.add(Vector(0,-elosa))
Pt11i=Pt11.add(Vector(0,-elosa))
Pt12i=Pt12.add(Vector(0,-elosa))

losaGenConf=reinf_bars.genericConf(cover=recNominal,texSize=hTextsArmados,Code='EHE',concrType='HA-30',steelType='B-500',dynamEff='N',decLengths=2,decSpacing=2)

F1S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='1S',
   diameter=0.016,
   spacing=0.20,
   lstPtsConcrSect=[Pl1i,Pl1,Pl4,Pl4i],
   gapStart=0.2,
   gapEnd=-0.10,
   fromToExtPts=[Pt8,Pt11],
   vectorLRefSec=Vector(-0.3,0.3)
)
F1I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='1I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl2i,Pl4i,Pl4],
   coverSide='l',
   gapStart=0.3,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt8i,Pt11i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F2S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='2S',
   diameter=0.016,
   spacing=0.20,
   lstPtsConcrSect=[Pl1i,Pl1,Pl5,Pl5i],
   gapStart=0.2,
   gapEnd=-0.10,
   fromToExtPts=[Pt6,Pt8],
   vectorLRefSec=Vector(-0.3,-0.3)
)
F2I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='2I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl2i,Pl5i,Pl5],
   coverSide='l',
   gapStart=0.3,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt6i,Pt8i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F3S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='3S',
   diameter=0.016,
   spacing=0.20,
   lstPtsConcrSect=[Pl3i,Pl3,Pl5,Pl5i],
   lstCover=[recNominal,recNominal+0.02,recNominal],
   gapStart=-0.10,
   gapEnd=-0.10,
   fromToExtPts=[Pt5,Pt6],
   coverSectBars=recNominal+0.02,
   vectorLRefSec=Vector(-0.3,-0.3)
)
F3I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='3I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl3,Pl3i,Pl5i,Pl5],
   coverSide='l',
   gapStart=-0.10,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt5i,Pt6i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F4S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='4S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl3i,Pl3,Pl3.add(Vector(12+recNominal-0.33,0))],
   lstCover=[recNominal,recNominal+0.02],
   gapStart=-0.10,
   gapEnd=0,
   fromToExtPts=[Pt2,Pt5],
   vectorLRefSec=Vector(-0.3,0.3)
)
F4I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='4I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl3,Pl3i,Pl3i.add(Vector(12+recNominal-0.33,0))],
   lstCover=[recNominal,recNominal+0.012],
   coverSide='l',
   gapStart=-0.10,
   gapEnd=-0,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt2i,Pt5i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F5S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='5S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl3.add(Vector(12+recNominal-0.33,0)),Pl9,Pl9i],
   lstCover=[recNominal+0.02,recNominal],
   gapStart=0.60,
   gapEnd=-0.10,
   fromToExtPts=[Pt2,Pt5],
   vectorLRefSec=Vector(-0.3,0.3)
)
F5I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='5I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl3i.add(Vector(12+recNominal-0.33,0)),Pl9i,Pl9],
   lstCover=[recNominal+0.012,recNominal],
   coverSide='l',
   gapStart=0.45,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt2i,Pt5i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)

F6S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='6S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl6i,Pl6,Pl9,Pl9i],
   gapStart=-0.10,
   gapEnd=-0.10,
   fromToExtPts=[Pt5,Pt7],
   vectorLRefSec=Vector(-0.3,0.3)
)
F6I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='6I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl6,Pl6i,Pl9i,Pl9],
   coverSide='l',
   gapStart=-0.10,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt5i,Pt7i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)

F7=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='7',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pl6i,Pl6,Pl7,Pl7i,Pl6i],
   fromToExtPts=[Pt7,Pt11],
   vectorLRefSec=Vector(-0.3,0.3)
)
F8S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='8S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt6i,Pt6,Pt12,Pt12i],
   lstCover=[recNominal,recNominal+0.016,recNominal],
   gapStart=-0.10,
   gapEnd=0.334,
   fromToExtPts=[Pl2,Pl3],
   coverSectBars=recNominal+0.016,
   vectorLRefSec=Vector(-0.3,0.3)
)
F8I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='8I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt6,Pt6i,Pt11i],
   lstCover=[recNominal,recNominal+0.012],
   coverSide='l',
   gapStart=-0.10,
   gapEnd=0.30,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl2i,Pl3i],
   coverSectBars=recNominal+0.012,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F9S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='9S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt6,Pt12,Pt12i],
   lstCover=[recNominal+0.016,recNominal],
   gapStart=0,
   gapEnd=0.334,
   fromToExtPts=[Pl3,Pl4],
   coverSectBars=recNominal+0.016,
   lateralCover=0,
   vectorLRefSec=Vector(-0.3,0.3)
)
F9I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='9I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt2i,Pt11i],
   lstCover=[recNominal+0.012],
   coverSide='l',
   gapStart=0.30,
   gapEnd=0.30,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl3i,Pl4i],
   coverSectBars=recNominal+0.012,
   lateralCover=0,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F10S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='10S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt6,Pt8,Pt8i],
   lstCover=[recNominal+0.016,recNominal],
   gapStart=0,
   gapEnd=-0.10,
   fromToExtPts=[Pl4,Pl5],
   coverSectBars=recNominal+0.016,
   vectorLRefSec=Vector(-0.3,0.3)
)
F10I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='10I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt2i,Pt8i,Pt8],
   lstCover=[recNominal+0.012,recNominal],
   coverSide='l',
   gapStart=0.30,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl4i,Pl5i],
   coverSectBars=recNominal+0.012,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F11S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='11S',
   diameter=0.020,
   spacing=0.20,
   lstPtsConcrSect=[Pt1i,Pt1,Pt6],
   gapStart=0.45,
   gapEnd=1.2,
   fromToExtPts=[Pl3,Pl5],
   vectorLRefSec=Vector(-0.3,0.3)
)
F12S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='12S',
   diameter=0.020,
   spacing=0.20,
   lstPtsConcrSect=[Pt1i,Pt1,Pt5,Pt5i],
   gapStart=0.45,
   gapEnd=-0.10,
   fromToExtPts=[Pl5,Pl6],
   vectorLRefSec=Vector(-0.3,0.3)
)
F12I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='12I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt1,Pt1i,Pt5i,Pt5],
   coverSide='l',
   gapStart=-0.10,
   gapEnd=-0.10,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl5i,Pl6i],
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F13S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='13S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt1i,Pt1,Pt12,Pt12i],
   lstCover=[recNominal,recNominal+0.012,recNominal],
   gapStart=0.118,
   gapEnd=0.118,
   fromToExtPts=[Pl6,Pl7],
   coverSectBars=recNominal+0.012,
   vectorLRefSec=Vector(-0.3,0.3)
)
F13I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='13I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt2i,Pt11i],
   lstCover=[recNominal+0.012],
   coverSide='l',
   gapStart=0.30,
   gapEnd=0.30,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl6i,Pl7i],
   lateralCover=recNominal+0.012,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F14S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='14S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt1i,Pt1,Pt7,Pt7i],
   lstCover=[recNominal,recNominal+0.012,recNominal],
   gapStart=0.118,
   gapEnd=-0.10,
   fromToExtPts=[Pl7,Pl8],
   coverSectBars=recNominal+0.012,
   vectorLRefSec=Vector(-0.3,0.3)
)
F14I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='14I',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt2i,Pt7i,Pt7],
   lstCover=[recNominal+0.012,recNominal],
   coverSide='l',
   gapStart=0.30,
   gapEnd=-0.1,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pl7i,Pl8i],
   lateralCover=recNominal+0.012,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)

F15S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='15S',
   diameter=0.016,
   spacing=0.10,
   lstPtsConcrSect=[Pl2,Pl3],
   lstCover=[recNominal+0.008],
   gapStart=0.60,
   gapEnd=0.60,
   fromToExtPts=[Pt3,Pt4],
   coverSectBars=recNominal+0.008,
   lateralCover=recNominal+0.008,
   vectorLRefSec=Vector(-0.3,0.3)
)
F15I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='15I',
   diameter=0.016,
   spacing=0.10,
   lstPtsConcrSect=[Pl2i,Pl3i],
   lstCover=[recNominal+0.008],
   coverSide='l',
   gapStart=0.60,
   gapEnd=0.60,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt3i,Pt4i],
   coverSectBars=recNominal+0.008,
   lateralCover=recNominal+0.008,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)

F16S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='16S',
   diameter=0.016,
   spacing=0.10,
   lstPtsConcrSect=[Pl7,Pl8],
   lstCover=[recNominal+0.008],
   gapStart=0.60,
   gapEnd=0.60,
   fromToExtPts=[Pt9,Pt10],
   coverSectBars=recNominal+0.008,
   lateralCover=recNominal+0.008,
   vectorLRefSec=Vector(-0.3,0.3)
)
F16I=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='16I',
   diameter=0.016,
   spacing=0.10,
   lstPtsConcrSect=[Pl7i,Pl8i],
   lstCover=[recNominal+0.008],
   coverSide='l',
   gapStart=0.60,
   gapEnd=0.60,
   vectorLRef=Vector(0.5,-0.5),
   fromToExtPts=[Pt9i,Pt10i],
   coverSectBars=recNominal+0.008,
   lateralCover=recNominal+0.008,
   sectBarsSide='l',
   vectorLRefSec=Vector(-0.3,-0.3)
)
F17=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='17',
   diameter=0.008,
   spacing=0.15,
   lstPtsConcrSect=[Pt3i,Pt3,Pt4,Pt4i,Pt3i],
   fromToExtPts=[Pl2,Pl3],
   vectorLRefSec=Vector(-0.3,0.3)
)
F18=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='18',
   diameter=0.008,
   spacing=0.15,
   lstPtsConcrSect=[Pt9i,Pt9,Pt10,Pt10i,Pt9i],
   fromToExtPts=[Pl7,Pl8],
   vectorLRefSec=Vector(-0.3,0.3)
)

R1S=reinf_bars.rebarFamily(
   genConf=losaGenConf,
   identifier='R1S',
   diameter=0.012,
   spacing=0.20,
   lstPtsConcrSect=[Pt8,Pt11],
   lstCover=[recNominal+0.012],
   gapStart=0.45,
   gapEnd=0.45,
   fromToExtPts=[Pl3,Pl4],
   coverSectBars=recNominal+0.012,
   lateralCover=recNominal+0.1,
   vectorLRefSec=Vector(-0.3,0.3)
)

# Plan of sections
App.newDocument("planRCsections")
#SECCIONES LONGITUDINALES
#sección A-A
lstPtsConcrSect=[[Pl1i,Pl1,Pl2,Pl2i],[Pl8i,Pl3i,Pl3,Pl9,Pl9i]]
lstShapeRebarFam=[F4S,F4I,F5S,F5I]
lstSectRebarFam=[F11S,F9I,F10I,F12S,F12I,F13S,F13I,F14S,F14I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,30,0))

#sección B-B
lstPtsConcrSect=[[Pl1i,Pl1,Pl9,Pl9i],[Pl2i,Pl8i]]
lstShapeRebarFam=[F4S,F4I,F5S,F5I,F15S,F15I]
lstSectRebarFam=[F11S,F9I,F10I,F12S,F12I,F13S,F13I,F14S,F14I,F17]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,25,0))

#sección C-C
lstPtsConcrSect=[[Pl1i,Pl1,Pl2,Pl2i],[Pl8i,Pl3i,Pl3,Pl9,Pl9i]]
lstShapeRebarFam=[F4S,F4I,F5S,F5I]
lstSectRebarFam=[F11S,F9I,F10I,F12S,F12I,F13S,F13I,F14S,F14I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,20,0))

#sección D-D
lstPtsConcrSect=[[Pl1i,Pl1,Pl2,Pl2i],[Pl3,Pl5,Pl5i,Pl3i,Pl3]]
[Pl8i,Pl6i,Pl6,Pl9,Pl9i],
lstShapeRebarFam=[F3S,F3I,F6S,F6I]
lstSectRebarFam=[F11S,F9I,F10I,F13S,F13I,F14S,F14I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,15,0))

#sección E-E
lstPtsConcrSect=[[Pl1i,Pl1,Pl5,Pl5i,Pl2i],[Pl8i,Pl6i,Pl6,Pl9,Pl9i]]
lstShapeRebarFam=[F2S,F2I,F6S,F6I]
lstSectRebarFam=[F8S,F8I,F9S,F9I,F10S,F10I,F13S,F13I,F14S,F14I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,10,0))

#sección F-F
lstPtsConcrSect=[[Pl1i,Pl1,Pl5,Pl5i,Pl2i],[Pl6,Pl7,Pl7i,Pl6i,Pl6]]
[Pl8i,Pl8,Pl9,Pl9i],
lstShapeRebarFam=[F2S,F2I,F7]
lstSectRebarFam=[F8S,F8I,F9S,F9I,F10S,F10I,F13S,F13I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,5,0))

#sección G-G
lstPtsConcrSect=[[Pl1i,Pl1,Pl4,Pl4i,Pl2i],[Pl8i,Pl6i,Pl6,Pl9,Pl9i]]
lstShapeRebarFam=[F1S,F1I,F7,F16S,F16I]
lstSectRebarFam=[F8S,F8I,F9S,F9I,F13S,F13I,R1S,18]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0))

#sección H-H
lstPtsConcrSect=[[Pl1i,Pl1,Pl4,Pl4i,Pl2i],[Pl6,Pl7,Pl7i,Pl6i,Pl6]]
[Pl8i,Pl8,Pl9,Pl9i],
lstShapeRebarFam=[F1S,F1I,F7]
lstSectRebarFam=[F8S,F8I,F9S,F9I,F13S,F13I,R1S]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,-5,0))

#SECCIONES TRANSVERSALES
#sección 1-1
lstPtsConcrSect=[[Pt1i,Pt1,Pt7,Pt7i,Pt2i],[Pt9,Pt10,Pt10i,Pt9i,Pt9],[Pt11i,Pt11,Pt12,Pt12i]]
lstShapeRebarFam=[F14S,F14I,F18]
lstSectRebarFam=[F5S,F5I,F6S,F6I,F16S,F16I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,30,0))


#sección 2-2
lstPtsConcrSect=[[Pt1i,Pt1,Pt12,Pt12i],[Pt2i,Pt11i]]
lstShapeRebarFam=[F13S,F13I]
lstSectRebarFam=[F5S,F5I,F6S,F6I,F7]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,25,0))

#sección 3-3
lstPtsConcrSect=[[Pt1i,Pt1,Pt5,Pt5i,Pt2i],[Pt11i,Pt11,Pt12,Pt12i]]
lstShapeRebarFam=[F12S,F12I]
lstSectRebarFam=[F4S,F4I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,20,0))

#sección 4-4
lstPtsConcrSect=[[Pt1i,Pt1,Pt8,Pt8i,Pt2i],[Pt11i,Pt11,Pt12,Pt12i]]
lstShapeRebarFam=[F11S,F10S,F10I]
lstSectRebarFam=[F4S,F4I,F3S,F3I,F2S,F2I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,15,0))

#sección 5-5
lstPtsConcrSect=[[Pt1i,Pt1,Pt12,Pt12i],[Pt2i,Pt11i]]
lstShapeRebarFam=[F11S,F9S,F9I,R1S]
lstSectRebarFam=[F4S,F4I,F3S,F3I,F2S,F2I,F1S,F1I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,10,0))

#sección 6-6
lstPtsConcrSect=[[Pt1i,Pt1,Pt2,Pt2i],[Pt3,Pt4,Pt4i,Pt3i,Pt3],[Pt11i,Pt6i,Pt6,Pt12,Pt12i]]
lstShapeRebarFam=[F8S,F8I,F17]
lstSectRebarFam=[F2S,F2I,F1S,F1I,F15S,F15I]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(30,5,0))

#DESPIECE DE LA ARMADURA
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hText=2.5
listafamiliasArmad=[F1S,F1I,F2S,F2I,F3S,F3I,F4S,F4I,F5S,F5I,F6S,F6I,F7,F8S,F8I,F9S,F9I,F11S,F12S,F12I,F13S,F13I,F14S,F14I,F15S,F15I,F16S,F16I,F17,F18,R1S]

reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hText,hTextSketch=hText)

#DESPIECE DE LA ARMADURA
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hText=2.5
listafamiliasArmad=[F1S,F1I,F2S,F2I,F3S,F3I,F4S,F4I,F5S,F5I,F6S,F6I,F7,F8S,F8I,F9S,F9I,F11S,F12S,F12I,F13S,F13I,F14S,F14I,F15S,F15I,F16S,F16I,F17,F18,R1S]

reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hText,hTextSketch=hText)

# Bar quantities for PyCost
reinf_bars.bars_quantities_for_budget(lstBarFamilies=listafamiliasArmad,outputFileName='/home/ana/quant_arm.py')
