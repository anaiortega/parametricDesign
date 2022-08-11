# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import reinf_bars
from FreeCAD import Vector
from Draft import *


# Reinforcement of a box culvert with chamfers in all its
# internal corners

# Nomenclature:
# _th: thickness
# _wd: width
# _ln: length
# _hg: height
# W: wall
# LW: left wall
# RW: right wall
# TS: top slab
# BS: bottom slab
# int: internal
# bot: bottom
# top: top
# ver: vertical
# hor: horizontal

#
#DATA
# Data RC box culvert
boxC_int_wd=3.50 # internal width of the box
boxC_int_hg=2 # internal height of the box
chamfer_wd=0.1 # width of the chamfer
chamfer_hg=0.1 # height of the chamfer
LW_th=0.30 # thickness of the left wall
RW_th=0.30 # thickness of the right wall
TS_th=0.30 # thickness of the top slab
BS_th=0.30 # thickness of the bottom slab
boxL=5 #length of the box culvert

# Data  reinforcements
cover=0.03
reinfConf=reinf_bars.genericConf(cover=cover,texSize=0.125,Code='EHE',concrType='HA-30',steelType='B-500',dynamEff='N',decLengths=2,decSpacing=2)

BS_bot_ln={'fi':0.016,'s':0.30,'id':'1'} # bottom slab, bottom long. rebars
BS_bot_tr={'fi':0.016,'s':0.30,'id':'3'} # bottom slab, bottom transv. rebars
BS_top_ln={'fi':0.016,'s':0.30,'id':'2'} # bottom slab, top long. rebars
BS_top_tr={'fi':0.016,'s':0.30,'id':'4'} # bottom slab, top transv. rebars

LW_ext_hor={'fi':0.016,'s':0.30,'id':'7l'} # left wall, external horiz. rebars
LW_ext_ver={'fi':0.016,'s':0.30,'id':'10l'} # left wall, external vert. rebars
LW_int_hor={'fi':0.016,'s':0.30,'id':'8l'} # left wall, internal horiz. rebars
LW_int_ver={'fi':0.016,'s':0.30,'id':'9l'} # left wall, internal vert. rebars

RW_ext_hor={'fi':0.016,'s':0.30,'id':'7r'} # right wall, external horiz. rebars
RW_ext_ver={'fi':0.016,'s':0.30,'id':'10r'} # right wall, external vert. rebars
RW_int_hor={'fi':0.016,'s':0.30,'id':'8r'} # right wall, internal horiz. rebars
RW_int_ver={'fi':0.016,'s':0.30,'id':'9r'} # right wall, internal vert. rebars

TS_bot_ln={'fi':0.016,'s':0.30,'id':'11'} # top slab, bottom long. rebars
TS_bot_tr={'fi':0.016,'s':0.30,'id':'13'} # top slab, bottom transv. rebars
TS_top_ln={'fi':0.016,'s':0.30,'id':'12'} # top slab, top long. rebars
TS_top_tr={'fi':0.016,'s':0.30,'id':'14'} # top slab, top transv. rebars
# END DATA

# external dimensions
ext_hg=BS_th+boxC_int_hg+TS_th
ext_wd=LW_th+boxC_int_wd+RW_th

#Points transversal section
ext_p1=Vector(0,0)
ext_p2=ext_p1.add(Vector(0,ext_hg))
ext_p3=ext_p2.add(Vector(ext_wd,0))
ext_p4=ext_p1.add(Vector(ext_wd,0))

int_p1a=ext_p1.add(Vector(LW_th+chamfer_wd,BS_th))
int_p1b=int_p1a.add(Vector(-chamfer_wd,chamfer_hg))

int_p2a=ext_p2.add(Vector(LW_th+chamfer_wd,-TS_th))
int_p2b=int_p2a.add(Vector(-chamfer_wd,-chamfer_hg))

int_p3a=ext_p3.add(Vector(-RW_th-chamfer_wd,-TS_th))
int_p3b=int_p3a.add(Vector(chamfer_wd,-chamfer_hg))

int_p4a=ext_p4.add(Vector(-RW_th-chamfer_wd,TS_th))
int_p4b=int_p4a.add(Vector(chamfer_wd,chamfer_hg))


# auxiliar vectors
vBSth=Vector(0,BS_th) # bottom slab thickness
vTSth=Vector(0,TS_th) # top slab thickness
vLWth=Vector(LW_th,0) # left wall thickness
vRWth=Vector(RW_th,0) # rigth wall thickness
vLength=Vector(boxL,0)
#Points vertical section
p1v=Vector(0,0)
p2v=p1v+vBSth
p3v=p2v+vLength
p4v=p3v-vBSth

p5v=p1v+Vector(0,boxC_int_hg)
p6v=p5v+vTSth
p7v=p7v+vLength
p8v=p8v-vTSth

# Rebar families
# bottom slab, bottom transv. rebars
BS_bot_tr_RF=reinf_bars.rebarFamily(
    genConf=reinfConf,
    identifier=BS_bot_tr['id'],
    diameter=BS_bot_tr['fi'],
    spacing=BS_bot_tr['s'],
    lstPtsConcrSect=[ext_p1+vBSth,ext_p1,ext_p4,ext_p4+vBSth],
    coverSide='l',
    gapStart=-cover,
    gapEnd=-cover,
    vectorLRef=Vector(0.5,-0.5),
    extensionLength=boxL,
    fromToExtPts=[p1v,p4v],
    coverSectBars=cover,
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,0.3),
)
# bottom slab, top transv. rebars
BS_top_tr_RF=reinf_bars.rebarFamily(
    genConf=reinfConf,
    identifier=BS_top_tr['id'],
    diameter=BS_top_tr['fi'],
    spacing=BS_top_tr['s'],
    lstPtsConcrSect=[ext_p1,ext_p1+vBSth,ext_p4+vBSth,ext_p4],
    coverSide='r',
    gapStart=-cover,
    gapEnd=-cover,
    vectorLRef=Vector(0.5,0.5),
    fromToExtPts=[p2v,p3v],
    coverSectBars=cover,
    sectBarsSide='r',
    vectorLRefSec=Vector(-0.3,-0.3),
)
# bottom slab, bottom long.. rebars
BS_bot_ln_RF=reinf_bars.rebarFamily(
    genConf=reinfConf,
    identifier=BS_bot_ln['id'],
    diameter=BS_bot_ln['fi'],
    spacing=BS_bot_ln['s'],
    lstPtsConcrSect=[p2v,p1v,p4v,p3v],
    coverSide='l',
    gapStart=-cover,
    gapEnd=-cover,
    fromToExtPts=[ext_p1,ext_p4],
    coverSectBars=cover+BS_bot_tr['fi'],
    sectBarsSide='l',
    vectorLRefSec=Vector(-0.3,-0.3),
)

# bottom slab, top long.. rebars
BS_top_ln_RF=reinf_bars.rebarFamily(
    genConf=reinfConf,
    identifier=BS_top_ln['id'],
    diameter=BS_top_ln['fi'],
    spacing=BS_top_ln['s'],
    lstPtsConcrSect=[p1v,p2v,p3v,p4v],
    gapStart=-cover,
    gapEnd=-cover,
    fromToExtPts=[ext_p1+vBSth+vLWth,ext_p4+vBSth-vRWth],
    coverSectBars=cover+BS_top_tr['fi'],
    sectBarsSide='r',
    vectorLRefSec=Vector(0.3,0.3),
)


listRebarFamilies=[BS_bot_tr_RF,BS_top_tr_RF,BS_bot_ln_RF,BS_top_ln_RF]
for fa in listRebarFamilies:
    fa.createRebar()

# Plan of sections
App.newDocument("planRCsections")
# Vertical section
lstPtsConcrSect=[[p1v,p2v,p3v,p4v,p1v]]
lstShapeRebarFam=[BS_bot_ln_RF,BS_top_ln_RF]
lstSectRebarFam=[BS_bot_tr_RF,BS_top_tr_RF]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(10,0,0))
# Transversal section
lstPtsConcrSect=[[ext_p1,ext_p2,ext_p3,ext_p4,ext_p1],[int_p1a,int_p1b,int_p2b,int_p2a,int_p3a,int_p3b,int_p4b,int_p4a,int_p1a]]
lstShapeRebarFam=[BS_bot_tr_RF,BS_top_tr_RF]
lstSectRebarFam=[BS_bot_ln_RF,BS_top_ln_RF]
reinf_bars.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0))

#
   #BAR SCHEDULE
App.newDocument("despiece")
#ancho de las columnas de cuadro de despiece (corresponden a posici'on, esquema, diam. y separac., No. de barras y longitud de cada barra)
anchoColumnas=[14,30,25,10,15,15]
#altura de las filas
hFilas=10
#altura textos
hText=2.5
listafamiliasArmad=[BS_bot_tr_RF,BS_top_tr_RF,BS_bot_ln_RF,BS_top_ln_RF]

reinf_bars.barSchedule(lstBarFamilies=listafamiliasArmad,wColumns=anchoColumnas,hRows=hFilas,hText=hText,hTextSketch=hText)
