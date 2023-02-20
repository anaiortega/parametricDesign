from freeCAD_civil import tables

docSetout=App.newDocument(obraNm+'_REPL',obraNm+'_REPL')
hText=2.5
hRows=5
wColumns=[15,25,25,18]
desfaseTablas=5 # espacio vertical entre tablas

# Replanteo tablero
exec(open(pathDeck+'../base_models/setout_deck.py').read())

# Replanteo pilotes
exec(open(pathDeck+'../base_models/setout_piles.py').read())

# Alzado aleta 1 (EL)
nmbAleta='1'
pntLst=stackPntWwEL
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 1 (EL)
nmbAleta='1'
pntLst=stackPntFootEL[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 2 (IL)
nmbAleta='2'
pntLst=stackPntWwIL
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 2 (IL)
nmbAleta='2'
pntLst=stackPntFootIL[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 3 (IR)
nmbAleta='3'
pntLst=stackPntWwIR
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 3 (IR)
nmbAleta='3'
pntLst=stackPntFootIR[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 4 (ER)
nmbAleta='4'
pntLst=stackPntWwER
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 4 (ER)
nmbAleta='4'
pntLst=stackPntFootER[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())
