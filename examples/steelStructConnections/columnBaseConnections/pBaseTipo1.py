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

#Placa base tipo 1
#El origen de coordenadas (X,Y) se sitúa sobre el eje del pilar. El
#origen de Z está en la cara inferior de la placa base.

docName='placa_base_tipo1'
docGeom=App.newDocument(docName,docName)

#NOTA: todas las cotas se dan en mm
#****Datos****
#Pilar
tipoPerfil='IPE'            #Perfil del pilar
idPerfil='450'              #tama?el perfil del pilar
cantoPerfil=metallic_profiles.IPE[idPerfil]['h']
eAlmaPerfil=metallic_profiles.IPE[idPerfil]['e']
eAlaPerfil=metallic_profiles.IPE[idPerfil]['e1']
bAlaPerfil=metallic_profiles.IPE[idPerfil]['b']
radioPerfil=metallic_profiles.IPE[idPerfil]['r']
#Placa
dimXPlaca=270               #ancho de la placa base (direcci?)
dimYPlaca=720               #largo de la placa base (direcci?)
ePlaca=25                   #espesor de la placa base (direcci?)
xminPlaca=-150/2-60         #coordenada X mínima de la placa
yminPlaca=-290-70           #coordenada Y mínima de la placa
#Soldaduras
eGargantaAlas=10            #espesor de gaganta de la soldadura de las alas del pilar a la placa
eGargantaAlma=8             #espesor de gaganta de la soldadura del alma del pilar a la placa
#Agujeros
nXFilasAg=2                 #nº de filas de agujeros en dirección X
dXFilasAg=[150]             #distancia entre filas de agujeros en dirección X
nYFilasAg=3                 #nº de filas de agujeros en dirección Y
dYFilasAg=[290,290]         #distancia entre filas de agujeros en dirección
xminAg=-150/2               #coord. X del centro del agujero con X mímima
yminAg=-290                 #coord. Y del centro del agujero con Y mímima
fiAguj=40                   #diámetro de los agujeros
#general

Lpieza=500                  #longitud de pilar a representar
#planos
escala=1                    #escala para generar planos
#****Fin datos****


#Perfil pilar
ptoIni=Base.Vector(0,0,ePlaca)
ptoFin=Base.Vector(0,0,ePlaca+Lpieza)
perfil=tipoPerfil
tamPerfil=idPerfil
incrIni=0
incrFin=0
giroSec=0
pilar=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
pieza=pilar

#Placa base
vOrigenL=Base.Vector(xminPlaca,yminPlaca,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordL=[[0,0],[dimXPlaca,0],[dimXPlaca,dimYPlaca],[0,dimYPlaca]]
altura=ePlaca
placa=geometry_3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordL,altura)
pieza=pieza.fuse(placa)

#Soldaduras
##de alas
pieza1=pieza
pieza2=pieza
eGarganta=eGargantaAlas
longitud=bAlaPerfil
centroArista=Base.Vector(0,-cantoPerfil/2,ePlaca)
vDireccion=Base.Vector(1,0,0)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

centroArista=Base.Vector(0,cantoPerfil/2,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

longitud=(bAlaPerfil-eAlmaPerfil)/2-radioPerfil
centroArista=Base.Vector(bAlaPerfil/2-longitud/2,cantoPerfil/2-eAlaPerfil,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

centroArista=Base.Vector(bAlaPerfil/2-longitud/2,-cantoPerfil/2+eAlaPerfil,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

centroArista=Base.Vector(-bAlaPerfil/2+longitud/2,cantoPerfil/2-eAlaPerfil,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

centroArista=Base.Vector(-bAlaPerfil/2+longitud/2,-cantoPerfil/2+eAlaPerfil,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

eGarganta=eGargantaAlas
longitud=bAlaPerfil
centroArista=Base.Vector(0,-cantoPerfil/2,ePlaca)
vDireccion=Base.Vector(1,0,0)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

##de almas
eGarganta=eGargantaAlma
longitud=cantoPerfil-2*eAlaPerfil-2*radioPerfil
centroArista=Base.Vector(eAlmaPerfil/2,0,ePlaca)
vDireccion=Base.Vector(0,1,0)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

centroArista=Base.Vector(-eAlmaPerfil/2,0,ePlaca)
sold=metallic_struct.soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion)
pieza=pieza.fuse(sold)

#Agujeros en placa base
vOrigenL=Base.Vector(xminAg,yminAg,0)
vDirXL=Base.Vector(1,0,0)
vDirYL=Base.Vector(0,1,0)
vDirZL=Base.Vector(0,0,1)
listaCoordCentrosL=[]
diametro=fiAguj
altura=ePlaca
xLinic=0
yLinic=0
for i in range(0,nXFilasAg):
    for j in range (0,nYFilasAg):
        centro=[xLinic+math.fsum(dXFilasAg[0:i]),yLinic+math.fsum(dYFilasAg[0:j])]
        listaCoordCentrosL.append(centro)

aguj=geometry_3D.conjCilindSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordCentrosL,diametro,altura)
pieza=pieza.cut(aguj)

Part.show(pieza,'pieza')

views.basic_views(docGeom=docGeom,title=docName,lstObjects=[docGeom.pieza],scale=0.10,pageTemplate='A3_Landscape_blank.svg')
