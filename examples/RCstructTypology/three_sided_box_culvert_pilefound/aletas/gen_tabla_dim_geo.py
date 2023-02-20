import Part, FreeCAD, math
from FreeCAD import Vector
from freeCAD_civil import tables

# Lectura de datos
lstDataDim=list()
exec(open(path+'datos_aleta1.py').read())
lstDataDim.append([estrName,lWall,hWallMax,hWallMin,wFoot,thFoot,wTop])
exec(open(path+'datos_aleta2.py').read())
lstDataDim.append([estrName,lWall,hWallMax,hWallMin,wFoot,thFoot,wTop])
exec(open(path+'datos_aleta3.py').read())
lstDataDim.append([estrName,lWall,hWallMax,hWallMin,wFoot,thFoot,wTop])
exec(open(path+'datos_aleta4.py').read())
lstDataDim.append([estrName,lWall,hWallMax,hWallMin,wFoot,thFoot,wTop])
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
