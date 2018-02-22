'''
Cálculo de longitudes de anclaje de acuerdo a art. 69.5.1 de la EHE-08.
    Posición I, de adherencia buena, para las armaduras que durante el hormigonado forman con la horizontal un ángulo comprendido entre 45° y 90° o que en el caso de formar un ángulo inferior a 45°, están situadas en la mitad inferior de la sección o a una distancia igual o mayor a 30 cm de la cara superior de una capa de hormigonado.
    Posición II, de adherencia deﬁciente, para las armaduras que, durante el hormigonado, no se encuentran en ninguno de los casos anteriores.
    En el caso de que puedan existir efectos dinámicos, las longitudes de anclaje indicadas en 69.5.1.2 se aumentarán en 10 ø.
'''

#Coeficiente m
coefM={
    'HA-25':{'B-400':1.2,'B-500':1.5},
    'HA-30':{'B-400':1.0,'B-500':1.3},
    'HA-35':{'B-400':0.9,'B-500':1.2},
    'HA-40':{'B-400':0.8,'B-500':1.1},
    'HA-45':{'B-400':0.7,'B-500':1.0},
    'HA-50':{'B-400':0.7,'B-500':1.0}
}

#Coeficiente beta
coefBeta={
    'prol_recta':{'tracc':1.0,'compr':1.0},
    'patilla':{'tracc':0.7,'compr':1.0},
    'barra_tr_sold':{'tracc':0.7,'compr':0.7}
}

def l_anclaje(tipoHorm,tipoAcer,fi,posicion,tipoAncl,estado='compr',relacAs=1.0,
              efectDinam='N'):
    '''Devuelve la longitud de anclaje [mm] calculada de acuerdo al
    artículo 69.5.1 de la EHE-08.
    
    :param tipoHorm: tipo de hormigón ('HA-25','HA-30','HA-35,'HA-40',
           'HA-45' ó 'HA-50')
    :param tipoAcer: tipo de acero para armar ('B-400' ó 'B-500')
    :param fi: diámetro de la armadura en mm
    :param posición: posición de la armadura ('I' ó 'II')
    :param tipoAncl: tipo de anclaje ('prol_recta', 'patilla' ó 'barra_tr_sold')
    :param estado: estado tensional de la armadura ('tracc': tracción, 
           'compr':compresión). Valor por defecto='compr' 
    :param relacAs: relación entre la armadura necesaria por cálculo y la 
           armadura realmente existente en la sección a partir de la cual se  
           ancla la armadura. Valor por defecto: 1
    :param efectDinam: ='Y' si se consideran efectos dinámicos, 'N' en caso
           contrario (valor por defecto = 'N')
    '''
    fyk=eval(tipoAcer[-3:])
    m=coefM[tipoHorm][tipoAcer]
    if posicion=='I':
        lb=max(m*fi**2,fyk/20.*fi)
    elif posicion=='II':
        lb=max(1.4*m*fi**2,fyk/14.*fi)
    else:
        print "Not valid value of rebar position ('I' or 'II')"
    beta=coefBeta[tipoAncl][estado]
    lbneta=lb*beta*relacAs
    if efectDinam.upper() in 'SY':
        lbneta=lbneta+10*fi
    if estado[:2].lower() == 'co':
        fact=2/3.
    else:
        fact=1/3.
    l_anc=max(lbneta,10*fi,150,fact*lb)
    return l_anc





