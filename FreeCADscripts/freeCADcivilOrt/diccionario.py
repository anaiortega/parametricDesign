armaduras={
    '1':{
        'diametro': 0.012,
        'separacion': 0.20,
        'listaPtos': [1,2,3,4],
        'listaRec':[0.04,0.03,0.05],
        'lado':'i',
        'radioDob': 0.03,
        'gapIni':-0.1,
        'gapFin':-0.15,
        'vectorLRef':Base.Vector(1,1),
        'hTexto':0.15
        },
    '2':{
        'diametro': 0.016,
        'separacion': 0.15,
        'listaPtos': [1,2,3,4],
        'listaRec':[0.04,0.03,0.05],
        'lado':'i',
        'radioDob': 0.03,
        'gapIni':-0.1,
        'gapFin':-0.15,
        'vectorLRef':[1],
        'hTexto':0.15
        },
}

identificadores=armaduras.keys()        

for i in identificadores:
    diam=armaduras[i]['diametro']
    print diam
    
