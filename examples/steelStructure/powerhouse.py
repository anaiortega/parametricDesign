# -*- coding: utf-8 -*-

import math
import Part, FreeCAD,TechDraw
import Draft
from  freeCAD_civil import geometry_3D as geom3D
from  freeCAD_civil import metallic_profiles as profil
from  freeCAD_civil import metallic_struct as mstruct
from FreeCAD import Base
from Draft import *

#****Datos****
#Muros y pilares
galiboYmuros=12.1*1e3    #gálibo interior entre muros en dirección Y
galiboXmuros=24.71*1e3   #gálibo interior entre muros en dirección X
eMuro1=0.8*1e3           #espesor muros
eMuro2=0.6*1e3           #espesor muros
hMuros=3e3               #altura de muros a representar
dimYPilar=0.7e3          #dimensión del pilar en dirección Y (transversal)
dimXPilar=0.5e3          #dimensión del pilar en dirección X (longitudinal)
dimZPilar=8.2e3          #dimensión del pilar en dirección Z (altura)
dEjesPilares=galiboYmuros+dimYPilar
dimYMensula=0.4e3
dimZ1Mensula=0.4e3
dimZ2Mensula=0.4e3
dXPorticos=[5e3,5e3,5e3,5e3,5e3]    #distancias entre pórticos en direccion X
dPorticosExtremos=(5*5)*1e3     #distancia entre planos centrales de pórticos extremos
pteCub=0.32                     #pendiente de la cubierta
vueloCub=1.05e3                 #vuelo de la viga de cubierta desde su intersección con el eje de la bayoneta
#Bayoneta
tipoPerfilBY='IPE'
idPerfilBY='300'
cantoBY=profil.IPE[idPerfilBY]['h']
anchoBY=profil.IPE[idPerfilBY]['b']
ealmaBY=profil.IPE[idPerfilBY]['e']
distYejesBY=(11.8+0.358*2)*1e3+cantoBY
dimZBay=(11.31-8.20)*1e3              #altura bayoneta entre cabeza de pilar y su intersección con eje de la viga de cubierta
#Placa anclaje en cabeza de pilar (para bayoneta y viga carrilera)
dimXPAB=400                     #dimensión X de la placa
dimYPAB=dimYPilar+dimYMensula   #dimensión Y de la placa
dimZPAB=15                      #dimensión Z de la placa (espesor)
#distAgXPAB=450                  #distancia entre centros de agujeros en dirección X
#distAgYPAB=450                  #distancia entre centros de agujeros en dirección Y
#diamAgPAB=18                    #diámetro de los agujeros
#Viga de cubierta
tipoPerfilVC='IPE'
idPerfilVC='330'
cantoVC=profil.IPE[idPerfilVC]['h']
#Chapa para formar la unión de la cumbrera
eChapaCumb=12         #espesor de la chapa para formar la unión atornillada de la cumbrera
#Viga carrilera
distYejesVCarr=11.8e3             #distancia entre ejes de vigas carrileras
tipoPerfilVCarr='HEB'
idPerfilVCarr='400'
cantoVCarr=profil.HEB[idPerfilVCarr]['h']
anchoVCarr=profil.HEB[idPerfilVCarr]['b']
ealmaVCarr=profil.HEB[idPerfilVCarr]['e']
ealaVCarr=profil.HEB[idPerfilVCarr]['e1']
racuerdoVCarr=profil.HEB[idPerfilVCarr]['r']
extensVCarr=0.3e3   #extensión de la viga carrilera a partir de los ejes de los pilares extremos
#Rigidizadores viga carrilera
eRigVCarr=12        #espesor de los rigidizadores de la viga carrilera
#Viga de acompañamiento
tipoPerfilVAc='IPE'
idPerfilVAc='300'
cantoVAc=profil.IPE[idPerfilVAc]['h']
anchoVAc=profil.IPE[idPerfilVAc]['b']
#Chapa de unión de la viga de acompañamiento con las bayonetas
dimXChVAc=12        #dimensión X (espesor) de la chapa
dimYChVAc=250       #dimensión Y (ancho) de la chapa
dimZChVAc=350       #dimensión Z (altura) de la chapa
cantoVAc=profil.IPE[idPerfilVAc]['h']
#Chapa en cabeza de viga carrilera
solapVCarr=60       #solape sobre viga carrilera
solapVAc=60         #solape sobre viga de acompañamiento
eChapaCab=10        #espesor de la chapa
holgChapaCab=20     #holgura entre chapa y alas de bayoneta
dCabezas=distYejesBY/2-distYejesVCarr/2-anchoVCarr/2-anchoVAc/2
#Correas
tipoPerfilCorrea='IPN'
idPerfilCorrea='220'
cantoCorrea=profil.IPN[idPerfilCorrea]['h']
sepCorreas=[0,1.54e3,1.54e3,1.54e3,1.54e3,1.54e3]            #separación entre las sucesivas correas en la dirección del faldón
vueloCorreas=0.7e3                                    

#****Fin datos****

docName='powerhouse'
docGeom=App.newDocument(docName,docName)

mTrsf=Base.Matrix()
mTrsf.rotateZ(math.pi) # rotate around the z-axis
# formaGirada=forma.transformGeometry(mTrsf)

#Dibujo muros
esq1=Base.Vector(dPorticosExtremos+dimXPilar+0.2,-galiboYmuros/2-eMuro1,-hMuros)
esq2=esq1.sub(Base.Vector(galiboXmuros+eMuro1+eMuro2,0,0))
muro1=Part.makeBox(galiboXmuros+eMuro1+eMuro2,eMuro1,hMuros,esq2)
muro2=Part.makeBox(eMuro2,galiboYmuros,hMuros,esq1.add(Base.Vector(-eMuro2,eMuro1,0)))
muro3=Part.makeBox(eMuro1,galiboYmuros,hMuros,esq2.add(Base.Vector(0,eMuro1,0)))
muro4=Part.makeBox(galiboXmuros+eMuro1+eMuro2,eMuro1,hMuros,esq2.add(Base.Vector(0,eMuro1+galiboYmuros,0)))
muros=muro1.fuse(muro2.fuse(muro3.fuse(muro4)))
Part.show(muros,'muros')

#Dibujo pilar
esquina=Base.Vector(-dimXPilar/2,-dEjesPilares/2-dimYPilar/2,0)
pilar1=Part.makeBox(dimXPilar,dimYPilar,dimZPilar,esquina)
vOrigenL=esquina.add(Base.Vector(0,dimYPilar,dimZPilar))
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[0,0],[dimYMensula,0],[dimYMensula,-dimZ1Mensula],[0,-dimZ1Mensula-dimZ2Mensula]]
altura=dimXPilar
mensula=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pilar=pilar1.fuse(mensula)

#Dibujo de la placa base de la bayoneta
centroPlaca=Base.Vector(0,-dEjesPilares/2-dimYPilar/2+dimYPAB/2,dimZPilar-dimZPAB)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordChapaL=[[-dimXPAB/2,-dimYPAB/2],[dimXPAB/2,-dimYPAB/2],[dimXPAB/2,dimYPAB/2],[-dimXPAB/2,dimYPAB/2]]
placaCabPilar=geom3D.prismaSCgen(centroPlaca,vDirXL,vDirYL,vDirZL,listaCoordChapaL,dimZPAB)
Part.show(placaCabPilar,'placaCabPilar')

pilar=pilar.cut(placaCabPilar)
Part.show(pilar,'pilar')
#listaCoordAgujL=[[-distAgXPAB/2,-distAgYPAB/2],[distAgXPAB/2,-distAgYPAB/2],[distAgXPAB/2,distAgYPAB/2],[-distAgXPAB/2,distAgYPAB/2]]

#placa=mstruct.chapaAgSCgen(centroPlaca,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,dimZPAB,diamAgPAB)

#Dibujo de la bayoneta
ptoIni=Base.Vector(0,-distYejesBY/2,dimZPilar)
ptoFin=ptoIni.add(Base.Vector(0,0,dimZBay))
perfil=tipoPerfilBY
tamPerfil=idPerfilBY
incrIni=0
incrFin=0
giroSec=0
bayonet=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
ptoFinBY=ptoFin

#Dibujo de la viga de cubierta
ptoIni=ptoFinBY
ptoFin=ptoIni.add(Base.Vector(0,distYejesBY/2,distYejesBY/2*pteCub))
perfil=tipoPerfilVC
tamPerfil=idPerfilVC
incrIni=vueloCub
incrFin=cantoVC
giroSec=0
vigaCub=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
ptoCumbera=ptoFin

#Volumen auxiliar para recortar otros por la cara inferior de la viga de cubierta
vOrigenL=ptoFinBY.add(Base.Vector(-5e3,0,0))
vDirXL=Base.Vector(0,1,pteCub)
vDirYL=Base.Vector(0,-pteCub,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[-10e3,-cantoVC/2],[10e3,-cantoVC/2],[10e3,10e3],[-10e3,10e3]]
altura=100e3
vauxCub=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)


#Volumen auxiliar para recortar otros por el plano de simetría vertical
vauxSim=Part.makeBox(100e3,20e3,20e3,Base.Vector(-2e3,0,0))
#Volumen auxiliar para recortar otros por la cara interior de la bayoneta
vauxCIBY=Part.makeBox(100e3,20e3,20e3,Base.Vector(-2e3,-distYejesBY/2+cantoBY/2-20e3,0))
#Volumen auxiliar para recortar otros por la cara exterior de la bayoneta
vauxCEBY=Part.makeBox(100e3,20e3,20e3,Base.Vector(-2e3,-distYejesBY/2-cantoBY/2,0))

#Recortes en piezas
bayoneta=bayonet.cut(vauxCub)
Part.show(bayoneta,'bayoneta')
vigaCub=vigaCub.cut(vauxSim)

#Rigidizadores hombro
ptoIni=ptoFinBY.add(Base.Vector(0,0,-0.50e3+cantoBY/2))
ptoFin=ptoIni.add(Base.Vector(0,math.cos(math.radians(35)),math.sin(math.radians(35))))
perfil=tipoPerfilBY
tamPerfil=idPerfilBY
incrIni=1e3
incrFin=1.5e3
giroSec=0
rig1=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
rig1=rig1.cut(vauxCub)
rig1=rig1.cut(vauxCIBY)
Part.show(rig1,'rig1')

ptoIni=ptoFinBY.add(Base.Vector(0,0,-0.50e3+cantoBY/2))
ptoFin=ptoIni.add(Base.Vector(0,-math.cos(math.radians(35)),math.sin(math.radians(35))))
perfil=tipoPerfilBY
tamPerfil=idPerfilBY
incrIni=1e3
incrFin=1e3
giroSec=0
rig2=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
rig2=rig2.cut(vauxCub)
rig2=rig2.cut(vauxCEBY)
Part.show(rig2,'rig2')

#Rigidizadores cumbrera
ptoIni=ptoCumbera.add(Base.Vector(0,0,-0.50e3+cantoVC/2))
ptoFin=ptoIni.add(Base.Vector(0,-math.cos(math.radians(15)),math.sin(math.radians(15))))
perfil=tipoPerfilVC
tamPerfil=idPerfilVC
incrIni=1e3
incrFin=1e3
giroSec=0
rig3=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
rig3=rig3.cut(vauxCub)
rig3=rig3.cut(vauxSim)

#Chapa en la unión de la cumbrera
aux1=vigaCub.BoundBox
aux2=rig3.BoundBox
xChMin=aux1.XMin
xChMax=aux1.XMax
zChMax=aux1.ZMax
zChMin=aux2.ZMin
ChapaCumbr=Part.makeBox(xChMax-xChMin,eChapaCumb,zChMax-zChMin,Base.Vector(xChMin,-eChapaCumb,zChMin))
Part.show(ChapaCumbr,'ChapaCumbr')
#recortes y representación
vigaCub=vigaCub.cut(ChapaCumbr)
rig3=rig3.cut(ChapaCumbr)
Part.show(vigaCub,'vigaCub')
Part.show(rig3,'rig3')

#Viga carrilera lado izquierdo
ptoIni=Base.Vector(0,-distYejesVCarr/2,dimZPilar+cantoVCarr/2)
ptoFin=ptoIni.add(Base.Vector(dPorticosExtremos,0,0))
perfil=tipoPerfilVCarr
tamPerfil=idPerfilVCarr
incrIni=extensVCarr
incrFin=extensVCarr
giroSec=0
vigaCarrI=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
Part.show(vigaCarrI,'vigaCarrI')
#Rigidizadores viga carrilera
vOrigenL=Base.Vector(-eRigVCarr/2,-distYejesVCarr/2,dimZPilar)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[ealmaVCarr/2+racuerdoVCarr,ealaVCarr],[anchoVCarr/2,ealaVCarr],[anchoVCarr/2,cantoVCarr-ealaVCarr],[ealmaVCarr/2+racuerdoVCarr,cantoVCarr-ealaVCarr],[ealmaVCarr/2,cantoVCarr-ealaVCarr-racuerdoVCarr],[ealmaVCarr/2,ealaVCarr+racuerdoVCarr]]
altura=eRigVCarr
rig1VCarr=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
Part.show(rig1VCarr,'rig1VCarr')
listaCoordL=[[-ealmaVCarr/2-racuerdoVCarr,ealaVCarr],[-anchoVCarr/2,ealaVCarr],[-anchoVCarr/2,cantoVCarr-ealaVCarr],[-ealmaVCarr/2-racuerdoVCarr,cantoVCarr-ealaVCarr],[-ealmaVCarr/2,cantoVCarr-ealaVCarr-racuerdoVCarr],[-ealmaVCarr/2,ealaVCarr+racuerdoVCarr]]
rig2VCarr=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
rigVCarr=rig1VCarr.fuse(rig2VCarr)
Part.show(rig2VCarr,'rig2VCarr')
vigaCarrileraI=vigaCarrI.fuse(rigVCarr)
mTraslac=Base.Matrix()
for vano in range(0,len(dXPorticos)):
    mTraslac.move(Base.Vector(dXPorticos[vano],0,0))
    rig=rigVCarr.copy().transformGeometry(mTraslac)
    vigaCarrileraI=vigaCarrileraI.fuse(rig)

####
#Viga de acompañamiento lado izquierdo
cx=0
cy=-distYejesBY/2
cz=dimZPilar+cantoVCarr-cantoVAc/2
for vano in range(0,len(dXPorticos)):
    #viga de acompañamiento
    ptoIni=(Base.Vector(cx,cy,cz))
    cx=cx+dXPorticos[vano]
    ptoFin=(Base.Vector(cx,cy,cz))
    perfil=tipoPerfilVAc
    tamPerfil=idPerfilVAc
    incrIni=-ealmaBY/2-dimXChVAc
    incrFin=incrIni
    giroSec=0
    Vacomp=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
    Part.show(Vacomp,'Vacomp')
    if vano == 0:
        vigaAcompI=Vacomp
    else:
        vigaAcompI=vigaAcompI.fuse(Vacomp)
    #chapas unión con bayoneta
    cx=cx-dXPorticos[vano]
    vOrigenL=Base.Vector(cx+ealmaBY/2,cy,cz)
    vDirXL=Base.Vector(0,1,0)
    vDirYL=Base.Vector(0,0,1)
    vDirZL=Base.Vector(1,0,0)
    listaCoordL=[[-dimYChVAc/2,-dimZChVAc/2],[dimYChVAc/2,-dimZChVAc/2],[dimYChVAc/2,dimZChVAc/2],[-dimYChVAc/2,dimZChVAc/2]]
    altura=dimXChVAc
    chapa1Vacomp=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    cx=cx+dXPorticos[vano]
    vOrigenL=Base.Vector(cx-ealmaBY/2-dimXChVAc,cy,cz)
    chapa2Vacomp=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    Part.show(chapa1Vacomp,'chapa1Vacomp')
    vigaAcompI=vigaAcompI.fuse(chapa1Vacomp)
    Part.show(chapa2Vacomp,'chapa2Vacomp')
    vigaAcompI=vigaAcompI.fuse(chapa2Vacomp)
    #chapa uniendo cabezas de viga carrilera y de viga de acompañamiento
    dimXChCab=dXPorticos[vano]-anchoBY-2*holgChapaCab
    cx=cx-dXPorticos[vano]
#    vOrigenL=Base.Vector(cx+anchoBY/2+holgChapaCab,cy+anchoVAc/2,cz+cantoVAc/2)
    vOrigenL=Base.Vector(cx+anchoBY/2+holgChapaCab,cy+anchoVAc/2,cz+cantoVAc/2)
    vDirXL=Base.Vector(0,1,0)
    vDirYL=Base.Vector(1,0,0)
    vDirZL=Base.Vector(0,0,1)
    listaCoordL=[[-solapVAc,0],[-solapVAc,dimXChCab],[dCabezas+solapVCarr,dimXChCab],[dCabezas+solapVCarr,0]]
    altura=eChapaCab
    chapaCab=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    Part.show(chapaCab,'chapaCab')
    vigaAcompI=vigaAcompI.fuse(chapaCab)
    cx=cx+dXPorticos[vano]
####    

#Viga carrilera lado derecho
ptoIni=Base.Vector(0,distYejesVCarr/2,dimZPilar+cantoVCarr/2)
ptoFin=ptoIni.add(Base.Vector(dPorticosExtremos,0,0))
perfil=tipoPerfilVCarr
tamPerfil=idPerfilVCarr
incrIni=extensVCarr
incrFin=extensVCarr
giroSec=0
vigaCarrD=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
#Rigidizadores viga carrilera
vOrigenL=Base.Vector(-eRigVCarr/2,distYejesVCarr/2,dimZPilar)
vDirXL=Base.Vector(0,1,0)
vDirYL=Base.Vector(0,0,1)
vDirZL=Base.Vector(1,0,0)
listaCoordL=[[ealmaVCarr/2+racuerdoVCarr,ealaVCarr],[anchoVCarr/2,ealaVCarr],[anchoVCarr/2,cantoVCarr-ealaVCarr],[ealmaVCarr/2+racuerdoVCarr,cantoVCarr-ealaVCarr],[ealmaVCarr/2,cantoVCarr-ealaVCarr-racuerdoVCarr],[ealmaVCarr/2,ealaVCarr+racuerdoVCarr]]
altura=eRigVCarr
rig1VCarr=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
Part.show(rig1VCarr,'rig1VCarr')
listaCoordL=[[-ealmaVCarr/2-racuerdoVCarr,ealaVCarr],[-anchoVCarr/2,ealaVCarr],[-anchoVCarr/2,cantoVCarr-ealaVCarr],[-ealmaVCarr/2-racuerdoVCarr,cantoVCarr-ealaVCarr],[-ealmaVCarr/2,cantoVCarr-ealaVCarr-racuerdoVCarr],[-ealmaVCarr/2,ealaVCarr+racuerdoVCarr]]
rig2VCarr=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
rigVCarr=rig1VCarr.fuse(rig2VCarr)
Part.show(rig2VCarr,'rig2VCarr')
vigaCarrileraD=vigaCarrD.fuse(rigVCarr)
mTraslac=Base.Matrix()
for vano in range(0,len(dXPorticos)):
    mTraslac.move(Base.Vector(dXPorticos[vano],0,0))
    rig=rigVCarr.copy().transformGeometry(mTraslac)
    vigaCarrileraD=vigaCarrileraD.fuse(rig)

#Viga de acompañamiento lado derecho
cx=0
cy=distYejesBY/2
cz=dimZPilar+cantoVCarr-cantoVAc/2
for vano in range(0,len(dXPorticos)):
    #viga de acompañamiento
    ptoIni=(Base.Vector(cx,cy,cz))
    cx=cx+dXPorticos[vano]
    ptoFin=(Base.Vector(cx,cy,cz))
    perfil=tipoPerfilVAc
    tamPerfil=idPerfilVAc
    incrIni=-ealmaBY/2-dimXChVAc
    incrFin=incrIni
    giroSec=0
    Vacomp=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
    Part.show(Vacomp,'Vacomp')
    if vano == 0:
        vigaAcompD=Vacomp
    else:
        vigaAcompD=vigaAcompD.fuse(Vacomp)
    #chapas unión con bayoneta
    cx=cx-dXPorticos[vano]
    vOrigenL=Base.Vector(cx+ealmaBY/2,cy,cz)
    vDirXL=Base.Vector(0,1,0)
    vDirYL=Base.Vector(0,0,1)
    vDirZL=Base.Vector(1,0,0)
    listaCoordL=[[-dimYChVAc/2,-dimZChVAc/2],[dimYChVAc/2,-dimZChVAc/2],[dimYChVAc/2,dimZChVAc/2],[-dimYChVAc/2,dimZChVAc/2]]
    altura=dimXChVAc
    chapa1Vacomp=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    cx=cx+dXPorticos[vano]
    vOrigenL=Base.Vector(cx-ealmaBY/2-dimXChVAc,cy,cz)
    chapa2Vacomp=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    Part.show(chapa1Vacomp,'chapa1Vacomp')
    vigaAcompD=vigaAcompD.fuse(chapa1Vacomp)
    Part.show(chapa2Vacomp,'chapa2Vacomp')
    vigaAcompD=vigaAcompD.fuse(chapa2Vacomp)
    #chapa uniendo cabezas de viga carrilera y de viga de acompañamiento
    dimXChCab=dXPorticos[vano]-anchoBY-2*holgChapaCab
    cx=cx-dXPorticos[vano]
#    vOrigenL=Base.Vector(cx+anchoBY/2+holgChapaCab,cy+anchoVAc/2,cz+cantoVAc/2)
    vOrigenL=Base.Vector(cx+anchoBY/2+holgChapaCab,cy-anchoVAc/2,cz+cantoVAc/2)
    vDirXL=Base.Vector(0,-1,0)
    vDirYL=Base.Vector(1,0,0)
    vDirZL=Base.Vector(0,0,1)
    listaCoordL=[[-solapVAc,0],[-solapVAc,dimXChCab],[dCabezas+solapVCarr,dimXChCab],[dCabezas+solapVCarr,0]]
    altura=eChapaCab
    chapaCab=geom3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
    Part.show(chapaCab,'chapaCab')
    vigaAcompD=vigaAcompD.fuse(chapaCab)
    cx=cx+dXPorticos[vano]

#Generación de pórticos
semiPortico1I=Part.makeCompound([pilar,placaCabPilar,bayoneta,rig1,rig2,ChapaCumbr,vigaCub,rig3])
semiPortico1D=semiPortico1I.transformGeometry(mTrsf)
Portico1=Part.makeCompound([semiPortico1I,semiPortico1D])
mTraslac=Base.Matrix()
mTraslac.move(Base.Vector(dXPorticos[0],0,0))
Portico2=Portico1.copy().transformGeometry(mTraslac)
mTraslac.move(Base.Vector(dXPorticos[1],0,0))
Portico3=Portico1.copy().transformGeometry(mTraslac)
mTraslac.move(Base.Vector(dXPorticos[2],0,0))
Portico4=Portico1.copy().transformGeometry(mTraslac)
mTraslac.move(Base.Vector(dXPorticos[3],0,0))
Portico5=Portico1.copy().transformGeometry(mTraslac)
mTraslac.move(Base.Vector(dXPorticos[4],0,0))
Portico6=Portico1.copy().transformGeometry(mTraslac)
Part.show(Portico1,'Portico1')
Part.show(Portico2,'Portico2')
Part.show(Portico3,'Portico3')
Part.show(Portico4,'Portico4')
Part.show(Portico5,'Portico5')
Part.show(Portico6,'Portico6')
Porticos=Part.makeCompound([Portico1,Portico2,Portico3,Portico4,Portico5,Portico6])
#Correas
dirFaldonIzq=Base.Vector(0,-1,-pteCub).normalize()
dirPerpFaldonIzq=Base.Vector(0,-pteCub,1).normalize()
dirFaldonDer=Base.Vector(0,1,-pteCub).normalize()
dirPerpFaldonDer=Base.Vector(0,pteCub,1).normalize()
distCumb=0

for nc in range(0,len(sepCorreas)):
    print(nc)
    distCumb=distCumb+sepCorreas[nc]
    #Faldón izquierdo
    vdirFaldon=Base.Vector(dirFaldonIzq.x,dirFaldonIzq.y,dirFaldonIzq.z)
    vperFaldon=Base.Vector(dirPerpFaldonIzq.x,dirPerpFaldonIzq.y,dirPerpFaldonIzq.z)
    ptoIni=ptoCumbera.add(vdirFaldon.multiply(distCumb).add(vperFaldon.multiply(cantoCorrea/2+cantoVC/2)))
    ptoFin=ptoIni.add(Base.Vector(dPorticosExtremos,0,0))
    perfil=tipoPerfilCorrea
    tamPerfil=idPerfilCorrea
    incrIni=vueloCorreas
    incrFin=vueloCorreas
    giroSec=math.degrees(math.atan(pteCub))
    Correa=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
    if nc == 0:
        Correas=Correa
    else:
        Correas=Correas.fuse(Correa)
        
    #Faldón derecho
    vdirFaldon=Base.Vector(dirFaldonDer.x,dirFaldonDer.y,dirFaldonDer.z)
    vperFaldon=Base.Vector(dirPerpFaldonDer.x,dirPerpFaldonDer.y,dirPerpFaldonDer.z)
    ptoIni=ptoCumbera.add(vdirFaldon.multiply(distCumb).add(vperFaldon.multiply(cantoCorrea/2+cantoVC/2)))
    ptoFin=ptoIni.add(Base.Vector(dPorticosExtremos,0,0))
    perfil=tipoPerfilCorrea
    tamPerfil=idPerfilCorrea
    incrIni=vueloCorreas
    incrFin=vueloCorreas
    giroSec=-math.degrees(math.atan(pteCub))
    Correa=mstruct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
    Correas=Correas.fuse(Correa)

Part.show(Correas,'Correas')
 
#listas para crear grupos de objetos para representar en planos
#todo
nave=Part.makeCompound([muros,Porticos,vigaCarrileraI,vigaCarrileraD,vigaAcompI,vigaAcompD,Correas])

Part.show(nave,'nave')

from layout_utils import views 
views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.nave],scale=0.01,pageTemplate='A1_Landscape_blank.svg')

'''
#Pilar intermedio (y lo que le rodea)
Xmin=dXPorticos[0]-dimXPilar/2-1e3
Xmax=dXPorticos[0]+dimXPilar/2+1e3
Ymin=-dEjesPilares/2-dimYPilar/2-1e3
Ymax=-dEjesPilares/2+dimYPilar/2+1e3
Zmin=-1.5e3
Zmax=20000
VauxPint=Part.makeBox(Xmax-Xmin,Ymax-Ymin,Zmax-Zmin,Base.Vector(Xmin,Ymin,Zmin))
pilarIntermedio=todo.common(VauxPint)

Part.show(pilarIntermedio,'pilarIntermedio')

#Pilar de esquina (y lo que le rodea)
Xmin=dPorticosExtremos-dimXPilar/2-1e3
Xmax=dPorticosExtremos+dimXPilar/2+1e3
Ymin=-dEjesPilares/2-dimYPilar/2-1e3
Ymax=-dEjesPilares/2+dimYPilar/2+1e3
Zmin=-1.5e3
Zmax=20000
VauxPesq=Part.makeBox(Xmax-Xmin,Ymax-Ymin,Zmax-Zmin,Base.Vector(Xmin,Ymin,Zmin))
pilarEsquina=todo.common(VauxPesq)
Part.show(pilarEsquina,'pilarEsquina')


#Cumbrera
Xmin=dPorticosExtremos-1e3
Xmax=dPorticosExtremos+2e3
Ymin=-1e3
Ymax=1e3
Zmin=1e3
Zmax=20000
VauxCumb=Part.makeBox(Xmax-Xmin,Ymax-Ymin,Zmax-Zmin,Base.Vector(Xmin,Ymin,Zmin))
cumbrera=todo.common(VauxCumb)

Part.show(cumbrera,'cumbrera')
'''

