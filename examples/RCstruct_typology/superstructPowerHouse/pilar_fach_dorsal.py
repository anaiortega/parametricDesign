# -*- coding: utf-8 -*-

import Part, FreeCAD, math, Drawing, FreeCADGui
import Draft
import reinf_bars
from reinf_bars import geometry_3D
from reinf_bars import metallic_profiles
from reinf_bars import metallic_struct
from FreeCAD import Base
from Draft import *

#****Datos****
#Muros y pilares
dimYPilar=0.5e3          #dimensión del pilar en dirección Y (transversal)
dimXPilar=0.5e3          #dimensión del pilar en dirección X (longitudinal)
dimZPilar=8.2e3          #dimensión del pilar en dirección Z (altura)

#Bayoneta
tipoPerfilBY='IPE'
idPerfilBY='300'
cantoBY=metallic_profiles.IPE[idPerfilBY]['h']
anchoBY=metallic_profiles.IPE[idPerfilBY]['b']
ealmaBY=metallic_profiles.IPE[idPerfilBY]['e']
ealaBY=metallic_profiles.IPE[idPerfilBY]['e1']
dimZBay=(13.534-8.20)*1e3              #altura bayoneta entre cabeza de pilar y su intersección con eje de la viga de cubierta

#Viga atado
tipoPerfilVA='UPN'
idPerfilVA='300'
cantoVA=metallic_profiles.UPN[idPerfilVA]['h']
anchoVA=metallic_profiles.UPN[idPerfilVA]['b']
ealmaVA=metallic_profiles.UPN[idPerfilVA]['e']
cdgVA=metallic_profiles.UPN[idPerfilVA]['e2']

#Vigas carrileras
distYejesVCarr=11.8e3
tipoPerfilVCarr='HEB'
idPerfilVCarr='400'
cantoVCarr=metallic_profiles.HEB[idPerfilVCarr]['h']
anchoVCarr=metallic_profiles.HEB[idPerfilVCarr]['b']
ealmaVCarr=metallic_profiles.HEB[idPerfilVCarr]['e']
ealaVCarr=metallic_profiles.HEB[idPerfilVCarr]['e1']
racuerdoVCarr=metallic_profiles.HEB[idPerfilVCarr]['r']

#****Fin datos****


mTrsf=Base.Matrix()
mTrsf.rotateZ(math.pi) # rotate around the z-axis
# formaGirada=forma.transformGeometry(mTrsf)


#Dibujo pilar
esquina=Base.Vector(-dimXPilar/2,-dimYPilar/2,0)
pilar=Part.makeBox(dimXPilar,dimYPilar,dimZPilar,esquina)



#Dibujo de la bayoneta
ptoIni=Base.Vector(-dimXPilar/2+20+cantoBY/2,0,dimZPilar)
ptoFin=ptoIni.add(Base.Vector(0,0,dimZBay))
perfil=tipoPerfilBY
tamPerfil=idPerfilBY
incrIni=0
incrFin=0
giroSec=90
bayonet=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)


#Dibujo de la viga de atado 1
ptoIni=Base.Vector(-dimXPilar/2+20+cantoBY+ealmaBY-cdgVA,anchoBY/2,dimZPilar+cantoVA/2)
ptoFin=ptoIni.add(Base.Vector(0,distYejesVCarr/2-ealmaVCarr/2-anchoBY/2,0))
perfil=tipoPerfilVA
tamPerfil=idPerfilVA
incrIni=0
incrFin=0
giroSec=0
vigaAt1=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)



#Dibujo de la viga de atado 2
ptoIni=Base.Vector(-dimXPilar/2+20+cantoBY+ealmaBY-cdgVA,-anchoBY/2,dimZPilar+cantoVA/2)
ptoFin=ptoIni.add(Base.Vector(0,-distYejesVCarr/2+ealmaVCarr/2+anchoBY/2,0))
perfil=tipoPerfilVA
tamPerfil=idPerfilVA
incrIni=0
incrFin=0
giroSec=0
vigaAt2=metallic_struct.barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)


todo=Part.makeCompound([pilar,bayonet,vigaAt1,vigaAt2])
Todo=FreeCAD.ActiveDocument.addObject("Part::Feature","Todo")
Todo.Shape=todo





