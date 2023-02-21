from freeCAD_civil import tables
from aux_sharing import sharing_docs as shd
from aux_sharing import sharing_vars as shv

shd.docSetout=FreeCAD.newDocument(obraNm+'_REPL',obraNm+'_REPL')
hText=2.5
hRows=5
wColumns=[15,25,25,18]
desfaseTablas=5 # espacio vertical entre tablas

# Replanteo tablero
exec(open(pathDeck+'../base_models/setout_deck.py').read())

# Replanteo pilotes
exec(open(pathDeck+'../base_models/setout_piles.py').read())

# Alzado aleta 1 (EL)
shv.nmbAleta='1'
shv.pntLst=stackPntWwEL
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 1 (EL)
shv.nmbAleta='1'
shv.pntLst=stackPntFootEL[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 2 (IL)
shv.nmbAleta='2'
shv.pntLst=stackPntWwIL
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 2 (IL)
shv.nmbAleta='2'
shv.pntLst=stackPntFootIL[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 3 (IR)
shv.nmbAleta='3'
shv.pntLst=stackPntWwIR
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 3 (IR)
shv.nmbAleta='3'
shv.pntLst=stackPntFootIR[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())

# Alzado aleta 4 (ER)
shv.nmbAleta='4'
shv.pntLst=stackPntWwER
exec(open(pathDeck+'../base_models/setout_wall_wingWall.py').read())

# Zapata aleta 4 (ER)
shv.nmbAleta='4'
shv.pntLst=stackPntFootER[0]
exec(open(pathDeck+'../base_models/setout_foot_wingWall.py').read())
