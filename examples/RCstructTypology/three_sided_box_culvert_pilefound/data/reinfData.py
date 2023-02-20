from data import geomData as gd

# datos armaduras
# anchos de banda
width_b1=0.75 # bandas transversales paralelas a muretes de guarda
width_b2=2    # banda longitudinal paralela a bandas de pilotes

L_rebar1=gd.thWall/2+1/5*(gd.spanDeck+gd.thWall) # longitud l de la armadura 1 

hTexts=0.05 # escala 1:20

# Armados tablero
# # armadura transversal inferior 
deck_tr_bot={'fi':0.025,'s':0.15}
deck_tr_bot_b1=None #{'fi':0.025,'s':0.15} # transversal inferior en banda b1
# armadura transversal superior 
deck_tr_top={'fi':0.012,'s':0.15}
# armadura longitudinal inferior
deck_ln_bot={'fi':0.020,'s':0.15}
# armadura longitudinal superior
deck_ln_top={'fi':0.012,'s':0.15}


# armadura lateral en todo el perímetro del tablero  definido por el nº de barras
#deck_lat
deck_lat={'fi':0.012,'nmbBars':3,'s':0} 

# Armados murete de guarda
# transversal superior
hwall_top={'fi':0.012,'nmbBars':3,'s':0}
# lateral lado exterior
hwall_lat_outside={'fi':0.012,'nmbBars':4,'s':0}
# lateral lado interior
hwall_lat_inside={'fi':0.012,'nmbBars':2,'s':0}

# armados muros
## vertical exterior
# extend= dimension to extend the rebar in the to of the deck beyond the internal side of
# the wall. Extension=extend+anchor length
wall_vert_ext={'fi':0.016,'s':0.15,'extend':L_rebar1-gd.thWall}
## vertical interior
wall_vert_int={'fi':0.012,'s':0.15}
## horizontal exterior
wall_hor_ext={'fi':0.016,'s':0.15}
## horizontal interior
wall_hor_int={'fi':0.016,'s':0.15}

# armadura de cortante murete de guarda
sTr=0 # spacing in trasversal section (where stirrups are in true shape). In this case, only one stirrup
sLn=0.15 # spacing in longitudinal section (where stirrups are in true shape).
nmbTr=1 # number of stirrups in the transverse section
nmbLn=int(gd.skewWdeck/sLn)
dispLn=0.10
hwall_stirrup={'fi':0.012,'sTr':sTr,'sLn':sLn,'nmbTr':nmbTr,'nmbLn':nmbLn,'dispLn':dispLn}

# armadura de cortante sobre pilotes [14]
fi=12e-3
sTr=0 # spacing in trasversal section (where stirrups are in true shape). In this case, only one stirrup
sLn=0.15 # spacing in longitudinal section (where stirrups are in true shape).
nmbTr=1 # number of stirrups in the transverse section
nmbLn=int((gd.Ldeck)/sLn)
dispLn=0.11
dispTr=0.0
hStirrup=0.6+fi+wall_hor_ext['fi']
pile_stirrup={'fi':fi,'sTr':sTr,'sLn':sLn,'nmbTr':nmbTr,'nmbLn':nmbLn,'dispLn':dispLn,'dispTr':dispTr,'hStirr':hStirrup}

# armadura de cortante paralela a líneas de pilotes (abrazando armadura transversal) [16]
# si el diámetro es 0, no se crea la familia
fi=8e-3
sTr=0.45
sLn=0.15
nmbTr=int(gd.Ldeck/sTr)
nmbLn=int((width_b2-gd.skewThwall)/sLn)+1
dispTr=0.05
bStirr=0.30+deck_tr_bot['fi']+2*fi # ancho del cerco (entre caras exteriores)
stirr_paral_pile={'fi':fi,'sTr':sTr,'sLn':sLn,'nmbTr':nmbTr,'nmbLn':nmbLn,'bStirr':bStirr,'dispLn':0.11,'dispTr':dispTr}


# armadura de cortante paralela al murete de guarda (abrazando armadura longitudinal) [18]
# si el diámetro es 0, no se crea la familia
fi=8e-3#8e-3#0 #8e-3
sTr=0.45
sLn=0.15
nmbTr=int((gd.skewWdeck-2*gd.skewThwall)/sTr)
nmbLn=int((width_b1-gd.thHeadWall)/sLn)+1
dispTr=0.085
bStirr=0.30+deck_ln_bot['fi']+2*fi # ancho del cerco (entre caras exteriores)
stirr_paral_headwall={'fi':fi,'sTr':sTr,'sLn':sLn,'nmbTr':nmbTr,'nmbLn':nmbLn,'bStirr':bStirr,'dispLn':0.11,'dispTr':dispTr}

# armadura longitudinal inferior en viga sobre pilotes
beam_pile_bot={'fi':0.016,'nmbBars':2,'s':0,'extraLatCover':0} 

# armadura longitudinal superior en viga sobre pilotes
beam_pile_top={'fi':0.016,'nmbBars':2,'s':0,'extraLatCover':0.1} 
