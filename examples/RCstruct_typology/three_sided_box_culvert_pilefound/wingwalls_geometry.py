from FreeCAD import Vector
from freeCAD_civil import tables

# import 
import sys
sys.path.append('/usr/local/src/prg/parametricDesign/examples/RCstruct_typology/three_sided_box_culvert_pilefound/')
from data import data_wingwall1 as datWW1
from data import data_wingwall2 as datWW2
from data import data_wingwall3 as datWW3
from data import data_wingwall4 as datWW4



# Lectura de datos
lstDataDim=list()
exec(open(path+'datos_aleta1.py').read())
lstDataDim.append([datWW1.estrName,datWW1.lWall,datWW1.hWallMax,datWW1.hWallMin,datWW1.wFoot,datWW1.thFoot,datWW1.wTop])
lstDataDim.append([datWW2.estrName,datWW2.lWall,datWW2.hWallMax,datWW2.hWallMin,datWW2.wFoot,datWW2.thFoot,datWW2.wTop])
lstDataDim.append([datWW3.estrName,datWW3.lWall,datWW3.hWallMax,datWW3.hWallMin,datWW3.wFoot,datWW3.thFoot,datWW3.wTop])
lstDataDim.append([datWW4.estrName,datWW4.lWall,datWW4.hWallMax,datWW4.hWallMin,datWW4.wFoot,datWW4.thFoot,datWW4.wTop])
# fin lectura datos

colTitles=['ALETA','Laleta','H1','H2','Bzap','Czap','Emuro']
formatColumns=['{}']+6*['{:.2f}']
title='DIMENSIONES ALETAS'

tables.genericTable(lstData=lstDataDim,
                    title=title,
                    colTitles=colTitles,
                    wColumns=[14]+6*[12],
                    formatColumns=formatColumns,
                    hRows=6.00,
                    hText=2.5,
                    pntTLcorner=Vector(0,100),
                    doc=docDespiece,
                    )

lstDataGeo=list()

exec(open(path+'data_muro.py').read())

lstDataGeo=[['TERRAPLEN',str(round(rhoBackfill*1e-3,1)) + ' t/m3','0 kPa',str(phiBackfill)],
            ['TERR. APOYO',str(round(rhoFoundSoil*1e-3,1)) + ' t/m3',str(round(cohesFoundSoil*1e-3,1))+' kPa',str(phiFoundSoil)],
            ]
colTitles=['Material','Densid.','Cohes.','%%C(sexag.)']
formatColumns=4*['{}']
title='PARAMETROS DE CALCULO'

tables.genericTable(lstData=lstDataGeo,
                    title=title,
                    colTitles=colTitles,
                    wColumns=[26,16,16,17],
                    formatColumns=formatColumns,
                    hRows=6.00,
                    hText=2.5,
                    pntTLcorner=Vector(100,100),
                    doc=docDespiece,
                    )
