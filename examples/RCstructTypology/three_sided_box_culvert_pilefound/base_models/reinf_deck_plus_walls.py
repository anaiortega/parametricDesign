import Part, FreeCAD, math
import Draft
import freeCAD_civil 
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
from Draft import *
from materials.ec2 import EC2_materials
from freeCAD_civil import draw_config as cfg

from data import geomData as gd
from data import reinfData as rd

#skewDirVector=Vector(math.cos(math.radians(skew)),math.sin(math.radians(skew)))
skewDirVector=Vector(-math.sin(math.radians(gd.skew)),math.cos(math.radians(gd.skew)))
titSchedule=gd.obraNm.upper()
coverDeck=0.035
coverWall=0.035


concrDeck=EC2_materials.C30 # concrete type in footing
steelDeck=EC2_materials.S500C # steel for footing

#rebar schedule dimensions
scheduleCfg=cfg.scheduleConf(wColumns=[10,30,30,10,20,12],hRows=10,hText=2.5,hTextSketch=2.0)
deckGenConf=cfg.reinfConf(cover=coverDeck,xcConcr=concrDeck,xcSteel=steelDeck,texSize=rd.hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=0.55,factDispReflinSectReb=1.6)
deckLatGenConf=cfg.reinfConf(cover=coverDeck,xcConcr=concrDeck,xcSteel=steelDeck,texSize=rd.hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=0.55,factDispReflinSectReb=1.0)
wallGenConf=cfg.reinfConf(cover=coverWall,xcConcr=concrDeck,xcSteel=steelDeck,texSize=rd.hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=0.55,factDispReflinSectReb=1.6)
stirrGenConf=cfg.reinfConf(cover=coverDeck,xcConcr=concrDeck,xcSteel=steelDeck,texSize=rd.hTexts,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,factPosLabelSectReb=0.65,factDispReflinSectReb=1.9)

docName=gd.obraNm.replace(' ','')+'_armados'
docArmados=App.newDocument(docName,docName)
hBeamPile=2*stirrGenConf.cover+rd.pile_stirrup['hStirr']+rd.pile_stirrup['fi']

# points longitudinal-central section (LC)
pt_LC1=Vector(0,0)
pt_LC2=Vector(gd.Ldeck,0)
pt_LC3=pt_LC2+Vector(0,gd.thDeck+gd.hHeadWall-gd.thPrelosa)
pt_LC4=pt_LC3-Vector(gd.skewThHeadWall,0)
pt_LC5=pt_LC4-Vector(0,gd.hHeadWall)
pt_LC8=pt_LC1+Vector(0,gd.thDeck+gd.hHeadWall-gd.thPrelosa)
pt_LC7=pt_LC8+Vector(gd.skewThHeadWall,0)
pt_LC6=pt_LC7-Vector(0,gd.hHeadWall)
pt_LC1_prelosa=pt_LC1-Vector(0,gd.thPrelosa)
pt_LC2_prelosa=pt_LC2-Vector(0,gd.thPrelosa)
pt_extLC6=pt_LC6-Vector(gd.skewThHeadWall,0)
pt_extLC5=pt_LC5+Vector(gd.skewThHeadWall,0)

# points transversal-central section (TC)
## deck
pt_TC1=Vector(0,0)
pt_TC2=Vector(gd.skewWdeck,0)
pt_TC3=pt_TC2+Vector(0,gd.thDeck-gd.thPrelosa)
pt_TC4=pt_TC1+Vector(0,gd.thDeck-gd.thPrelosa)
## left wall
pt_TC5=pt_TC1-Vector(0,gd.hLeftWall+gd.thPrelosa)
pt_TC6=pt_TC5+Vector(gd.skewThwall,0)
pt_TC7=pt_TC6+Vector(0,gd.hLeftWall)
## right wall
pt_TC8=pt_TC2-Vector(0,gd.hRightWall+gd.thPrelosa)
pt_TC9=pt_TC8-Vector(gd.skewThwall,0)
pt_TC10=pt_TC9+Vector(0,gd.hRightWall)
## prelosa
pt_TC1_prelosa=pt_TC7-Vector(gd.entregaPrelosa,0)
pt_TC2_prelosa=pt_TC10+Vector(gd.entregaPrelosa,0)
pt_TC3_prelosa=pt_TC2_prelosa+Vector(0,gd.thPrelosa)
pt_TC4_prelosa=pt_TC1_prelosa+Vector(0,gd.thPrelosa)


# points transversal-border section (TB) [F-F]
pt_TB1=Vector(0,0)
pt_TB2=Vector(gd.skewWdeck,0)
pt_TB3=pt_TB2+Vector(0,gd.thDeck+gd.hHeadWall-gd.thPrelosa)
pt_TB4=pt_TB1+Vector(0,gd.thDeck+gd.hHeadWall-gd.thPrelosa)

# points transversal-horizontal section (TH)
pt_TH1=Vector(0,0)
pt_TH2=Vector(gd.skewWdeck,0)
pt_TH3=pt_TH2+Vector(0,gd.skewThHeadWall)
pt_TH4=pt_TH1+Vector(0,gd.skewThHeadWall)

# points wall longitudinal horizontal section
pt_WLH2=Vector(0,0)
pt_WLH1=pt_WLH2+gd.skewThwall*skewDirVector
pt_WLH3=pt_WLH2+Vector(gd.Ldeck,0)
pt_WLH4=pt_WLH1+Vector(gd.Ldeck,0)

# points beam over pile
pt_BP1=Vector(0,0)
pt_BP2=Vector(gd.Ldeck,0)
pt_BP3=pt_BP2+Vector(0,hBeamPile)
pt_BP4=pt_BP1+Vector(0,hBeamPile)

# Armaduras tablero
lstRebarFam=list()
rebarCount=0
# tablero transversal inferior
if rd.deck_tr_bot_b1:
    fromToExtPts=[pt_LC1+Vector(rd.width_b1,0),pt_LC2-Vector(rd.width_b1,0)]
else:
    fromToExtPts=[pt_LC1,pt_LC2]
rdef=rd.deck_tr_bot
RF_deck_tr_bot=rb.rebarFamily(
    reinfCfg=deckGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    lstPtsConcrSect=[pt_TC4,pt_TC1,pt_TC2,pt_TC3],
    lstCover=[deckGenConf.cover,rdef['fi'],deckGenConf.cover],
    gapStart=-1.0*deckGenConf.cover,
    gapEnd=-1.0*deckGenConf.cover,
    coverSide='l',
    vectorLRef=Vector(-0.3,-0.3),
    fromToExtPts=fromToExtPts,
    coverSectBars=rdef['fi'],
    sectBarsSide='l',
    spacing=rdef['s'],
    position='posGood',
)
lstRebarFam+=[RF_deck_tr_bot]
rebarCount+=1

if rd.deck_tr_bot_b1:
    #start
    rdef=rd.deck_tr_bot_b1
    fromToExtPts=[pt_LC1,pt_LC1+Vector(rd.width_b1,0)]
    RF_deck_tr_bot_b1S=rb.rebarFamily(
        reinfCfg=deckGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrSect=[pt_TC4,pt_TC1,pt_TC2,pt_TC3],
        lstCover=[deckGenConf.cover,rdef['fi'],deckGenConf.cover],
        gapStart=-1.0*deckGenConf.cover,
        gapEnd=-1.0*deckGenConf.cover,
        coverSide='l',
        vectorLRef=Vector(-0.3,-0.3),
        fromToExtPts=fromToExtPts,
        coverSectBars=rdef['fi'],
        sectBarsSide='l',
        spacing=rdef['s'],
        position='posGood',
    )
    lstRebarFam+=[RF_deck_tr_bot_b1S]
    rebarCount+=1
    # end
    rdef=rd.deck_tr_bot_b1
    fromToExtPts=[pt_LC2-Vector(rd.width_b1,0),pt_LC2]
    RF_deck_tr_bot_b1E=rb.rebarFamily(
        reinfCfg=deckGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrSect=[pt_TC4,pt_TC1,pt_TC2,pt_TC3],
        lstCover=[deckGenConf.cover,rdef['fi'],deckGenConf.cover],
        gapStart=-1.0*deckGenConf.cover,
        gapEnd=-1.0*deckGenConf.cover,
        coverSide='l',
        vectorLRef=Vector(-0.3,-0.3),
        fromToExtPts=fromToExtPts,
        coverSectBars=rdef['fi'],
        sectBarsSide='l',
        spacing=rdef['s'],
        position='posGood',
    )
    lstRebarFam+=[RF_deck_tr_bot_b1E]
    rebarCount+=1
    
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',

# tablero armadura transversal superior
RF_deck_tr_top=rb.rebarFamily(
    reinfCfg=deckGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.deck_tr_top['fi'],
    spacing=rd.deck_tr_top['s'],
    gapStart=-1.5*deckGenConf.cover,
    gapEnd=-1.5*deckGenConf.cover,
    lstPtsConcrSect=[pt_TC1,pt_TC4,pt_TC3,pt_TC2],
    lstCover=[deckGenConf.cover,deckGenConf.cover+rd.stirr_paral_pile['fi'],deckGenConf.cover],
    coverSide='r',
    fromToExtPts=[pt_extLC6,pt_extLC5],
    coverSectBars=deckGenConf.cover+rd.stirr_paral_pile['fi'],
    vectorLRef=Vector(-0.3,0.3),
    position='posPoor',
    )
    
lstRebarFam+=[RF_deck_tr_top]
rebarCount+=1

    
# tablero armadura longitudinal inferior
if rd.deck_tr_bot_b1:
    rencCent=2*rd.deck_tr_bot_b1['fi']
else:
    rencCent=2*rd.deck_tr_bot['fi']
    
RF_deck_ln_bot=rb.rebarFamily(
    reinfCfg=deckGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.deck_ln_bot['fi'],
    spacing=rd.deck_ln_bot['s'],
    gapStart=-1.0*deckGenConf.cover,
    gapEnd=-1.0*deckGenConf.cover,
    lstPtsConcrSect=[pt_extLC6,pt_LC1,pt_LC2,pt_extLC5],
    lstCover=[deckGenConf.cover,rencCent,deckGenConf.cover],
    coverSectBars=2*rd.deck_tr_bot['fi'],
    coverSide='l',
    vectorLRef=Vector(-0.1,-0.4),
    fromToExtPts=[pt_TC7+Vector(0,gd.thPrelosa),pt_TC10+Vector(0,gd.thPrelosa)],
    sectBarsSide='l',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_deck_ln_bot]
rebarCount+=1
# tablero armadura longitudinal superior
RF_deck_ln_top=rb.rebarFamily(
    reinfCfg=deckGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.deck_ln_top['fi'],
    spacing=rd.deck_ln_top['s'],
    lstPtsConcrSect=[pt_LC1,pt_extLC6,pt_extLC5,pt_LC2],
    lstCover=[deckGenConf.cover,deckGenConf.cover+rd.deck_tr_top['fi']+rd.stirr_paral_pile['fi'],deckGenConf.cover],
    fromToExtPts=[pt_TC4,pt_TC3],
    coverSectBars=deckGenConf.cover+rd.deck_tr_top['fi']+rd.stirr_paral_pile['fi'],
    vectorLRef=Vector(-0.3,0.3),
    position='posPoor',
    )
lstRebarFam+=[RF_deck_ln_top]
rebarCount+=1


# armadura cara superior murete de guarda
RF_hwall1_top=rb.rebarFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_top['fi'],
    nmbBars=rd.hwall_top['nmbBars'],
    lstPtsConcrSect=[pt_TB4,pt_TB3],
    lstCover=[stirrGenConf.cover+rd.hwall_stirrup['fi']],
    fromToExtPts=[pt_LC8,pt_LC7],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    extrShapeStart='fix270_len250',
    extrShapeEnd='fix270_len250',
    vectorLRef=Vector(0.3,0.25),
    )
lstRebarFam+=[RF_hwall1_top]
rebarCount+=1

RF_hwall2_top=rb.rebarFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_top['fi'],
#    spacing=rd.hwall_top_heel['s'],
    nmbBars=rd.hwall_top['nmbBars'],
    lstPtsConcrSect=[pt_TB4,pt_TB3],
    lstCover=[stirrGenConf.cover+rd.hwall_stirrup['fi']],
    fromToExtPts=[pt_LC4,pt_LC3],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    extrShapeStart='anc270_posPoor_tens',
    extrShapeEnd='anc270_posPoor_tens',
    )
lstRebarFam+=[RF_hwall2_top]
rebarCount+=1

RF_hwall1_lat_ext=rb.rebarFamily(
    reinfCfg=deckLatGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_lat_outside['fi'],
    nmbBars=rd.hwall_lat_outside['nmbBars'],
    lstPtsConcrSect=[pt_TH1,pt_TH4,pt_TH3,pt_TH2],
    lstCover=[stirrGenConf.cover,stirrGenConf.cover+rd.hwall_stirrup['fi'],stirrGenConf.cover],
    fromToExtPts=[pt_LC1,pt_LC8],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    gapStart=-1.0*stirrGenConf.cover,
    gapEnd=-1.0*stirrGenConf.cover,
    )
lstRebarFam+=[RF_hwall1_lat_ext]
rebarCount+=1

RF_hwall2_lat_ext=rb.rebarFamily(
    reinfCfg=deckLatGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_lat_outside['fi'],
    nmbBars=rd.hwall_lat_outside['nmbBars'],
    lstPtsConcrSect=[pt_TH1,pt_TH4,pt_TH3,pt_TH2],
    lstCover=[stirrGenConf.cover,stirrGenConf.cover+rd.hwall_stirrup['fi'],stirrGenConf.cover],
    fromToExtPts=[pt_LC2,pt_LC3],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='l',
    gapStart=-1.0*stirrGenConf.cover,
    gapEnd=-1.0*stirrGenConf.cover,
    )
lstRebarFam+=[RF_hwall2_lat_ext]
rebarCount+=1


RF_hwall1_lat_int=rb.rebarFamily(
    reinfCfg=deckLatGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_lat_outside['fi'],
    nmbBars=rd.hwall_lat_outside['nmbBars'],
    lstPtsConcrSect=[pt_TH1,pt_TH4,pt_TH3,pt_TH2],
    lstCover=[stirrGenConf.cover,stirrGenConf.cover+rd.hwall_stirrup['fi'],stirrGenConf.cover],
    fromToExtPts=[pt_LC6,pt_LC7],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='l',
    gapStart=-1.0*stirrGenConf.cover,
    gapEnd=-1.0*stirrGenConf.cover,
    )
lstRebarFam+=[RF_hwall1_lat_int]
rebarCount+=1

RF_hwall1_lat_int=rb.rebarFamily(
    reinfCfg=deckLatGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_lat_inside['fi'],
    nmbBars=rd.hwall_lat_inside['nmbBars'],
    lstPtsConcrSect=[pt_TH1,pt_TH4,pt_TH3,pt_TH2],
    lstCover=[stirrGenConf.cover,stirrGenConf.cover+rd.hwall_stirrup['fi'],stirrGenConf.cover],
    fromToExtPts=[pt_LC6,pt_LC7],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='l',
    gapStart=-1.0*stirrGenConf.cover,
    gapEnd=-1.0*stirrGenConf.cover,
    )
lstRebarFam+=[RF_hwall1_lat_int]
rebarCount+=1

RF_hwall2_lat_int=rb.rebarFamily(
    reinfCfg=deckLatGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_lat_inside['fi'],
    nmbBars=rd.hwall_lat_inside['nmbBars'],
    lstPtsConcrSect=[pt_TH1,pt_TH4,pt_TH3,pt_TH2],
    lstCover=[stirrGenConf.cover,stirrGenConf.cover+rd.hwall_stirrup['fi'],stirrGenConf.cover],
    fromToExtPts=[pt_LC5,pt_LC4],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    gapStart=-1.0*stirrGenConf.cover,
    gapEnd=-1.0*stirrGenConf.cover,
    )
lstRebarFam+=[RF_hwall2_lat_int]
rebarCount+=1

# Armadura muros
## Muro izquierdo
### vertical exterior
rdef=rd.wall_vert_ext
RF_Lwall_vert_ext=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapStart=-2.0*wallGenConf.cover,
#    gapEnd=-(RF_deck_ln_top.lstCover[1]+RF_deck_ln_top.diameter+rdef['fi']/2),
    lstPtsConcrSect=[pt_TC6,pt_TC5,pt_TC4,pt_TC4+Vector(gd.thWall+rdef['extend'])],
    coverSide='r',
    vectorLRef=Vector(-0.3,-0.3),
    fromToExtPts=[pt_WLH1,pt_WLH4],
    extrShapeEnd='anc0_posPoor_tens',
    sectBarsSide='r',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_Lwall_vert_ext]
rebarCount+=1
### vertical interior
rdef=rd.wall_vert_int
RF_Lwall_vert_int=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_TC5,pt_TC6,pt_TC7,pt_TC7-Vector(gd.skewThwall,0)],
    coverSide='l',
    vectorLRef=Vector(0.3,-0.2),
    fromToExtPts=[pt_WLH2,pt_WLH3],
    sectBarsSide='l',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_Lwall_vert_int]
rebarCount+=1
### vertical interior conexión muro-tablero
rdef=rd.wall_vert_int
RF_Lwall_vert_int_dowel=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_TC1_prelosa,pt_TC1_prelosa+Vector(0,gd.thDeck),pt_TC4],
    lstCover=[wallGenConf.cover,RF_deck_ln_top.lstCover[1]+RF_deck_ln_top.diameter],
    coverSide='l',
    extrShapeStart='anc0_posGood_tens',
    vectorLRef=Vector(0.3,-0.3),
    fromToExtPts=[pt_WLH2,pt_WLH3],
    sectBarsSide='l',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_Lwall_vert_int_dowel]
rebarCount+=1
### horizontal exterior
rdef=rd.wall_hor_ext
RF_Lwall_hor_ext=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    lstCover=[wallGenConf.cover,wallGenConf.cover+rd.wall_vert_ext['fi'],wallGenConf.cover],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_WLH2,pt_WLH1,pt_WLH4,pt_WLH3],
    coverSide='r',
    vectorLRef=Vector(-0.3,0.32),
    fromToExtPts=[pt_TC5,pt_TC4],
    coverSectBars=wallGenConf.cover+rd.wall_vert_ext['fi'],
    sectBarsSide='r',
    position='posGood',
    )
lstRebarFam+=[RF_Lwall_hor_ext]
rebarCount+=1
### horizontal interior
rdef=rd.wall_hor_int
RF_Lwall_hor_int=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    lstCover=[wallGenConf.cover,wallGenConf.cover+rd.wall_vert_int['fi'],wallGenConf.cover],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_WLH1,pt_WLH2,pt_WLH3,pt_WLH4],
    coverSide='l',
    vectorLRef=Vector(-0.3,-0.3),
    fromToExtPts=[pt_TC6,pt_TC7],
    coverSectBars=wallGenConf.cover+rd.wall_vert_int['fi'],
    sectBarsSide='l',
    position='posGood',
    )
lstRebarFam+=[RF_Lwall_hor_int]
rebarCount+=1


## Muro derecho
### vertical exterior
rdef=rd.wall_vert_ext
RF_Rwall_vert_ext=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapStart=-2.0*wallGenConf.cover,
#    gapEnd=-(RF_deck_ln_top.lstCover[1]+RF_deck_ln_top.diameter+rdef['fi']/2),
    lstPtsConcrSect=[pt_TC9,pt_TC8,pt_TC3,pt_TC3-Vector(gd.thWall+rdef['extend'])],
    coverSide='l',
    vectorLRef=Vector(0.3,-0.3),
    fromToExtPts=[pt_WLH2,pt_WLH3],
    extrShapeEnd='anc0_posPoor_tens',
    sectBarsSide='l',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_Rwall_vert_ext]
rebarCount+=1
### vertical interior
rdef=rd.wall_vert_int
RF_Rwall_vert_int=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_TC8,pt_TC9,pt_TC10,pt_TC10+Vector(gd.skewThwall,0)],
    coverSide='r',
    vectorLRef=Vector(-0.3,-0.2),
    fromToExtPts=[pt_WLH1,pt_WLH4],
    sectBarsSide='r',
    position='posGood',
    )
#    extrShapeStart='anc90_posGood_tens',
#    extrShapeEnd='anc90_posGood_tens',
lstRebarFam+=[RF_Rwall_vert_int]
rebarCount+=1
### vertical interior conexión muro-tablero
rdef=rd.wall_vert_int
RF_Rwall_vert_int_dowel=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_TC2_prelosa,pt_TC2_prelosa+Vector(0,gd.thDeck),pt_TC3],
    lstCover=[wallGenConf.cover,RF_deck_ln_top.lstCover[1]+RF_deck_ln_top.diameter],
    coverSide='r',
    extrShapeStart='anc0_posGood_tens',
    vectorLRef=Vector(-0.3,-0.4),
    fromToExtPts=[pt_WLH1,pt_WLH4],
    sectBarsSide='r',
    position='posGood',
    )
lstRebarFam+=[RF_Rwall_vert_int_dowel]
rebarCount+=1
#
### horizontal exterior
rdef=rd.wall_hor_ext
RF_Rwall_hor_ext=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    lstCover=[wallGenConf.cover,wallGenConf.cover+rd.wall_vert_ext['fi'],wallGenConf.cover],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_WLH1,pt_WLH2,pt_WLH3,pt_WLH4],
    coverSide='l',
    vectorLRef=Vector(-0.3,0.2),
    fromToExtPts=[pt_TC8,pt_TC3],
    coverSectBars=wallGenConf.cover+rd.wall_vert_ext['fi'],
    sectBarsSide='l',
    position='posGood',
    )
lstRebarFam+=[RF_Rwall_hor_ext]
rebarCount+=1
### horizontal exterior
rdef=rd.wall_hor_int
RF_Rwall_hor_int=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    spacing=rdef['s'],
    lstCover=[wallGenConf.cover,wallGenConf.cover+rd.wall_vert_int['fi'],wallGenConf.cover],
    gapStart=-2.0*wallGenConf.cover,
    gapEnd=-2.0*wallGenConf.cover,
    lstPtsConcrSect=[pt_WLH2,pt_WLH1,pt_WLH4,pt_WLH3],
    coverSide='l',
    vectorLRef=Vector(0.3,0.2),
    fromToExtPts=[pt_TC9,pt_TC10],
    coverSectBars=wallGenConf.cover+rd.wall_vert_int['fi'],
    sectBarsSide='r',
    position='posGood',
    )
lstRebarFam+=[RF_Rwall_hor_int]
rebarCount+=1




# Armadura de cortante en muretes de guarda

RF_hwall1_stirrup=rb.stirrupFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_stirrup['fi'],
    lstPtsConcrTransv=[pt_LC1,pt_LC1+Vector(gd.skewThHeadWall,0),pt_LC7,pt_LC8],
    lstCover=[rd.deck_tr_bot['fi']-rd.hwall_stirrup['fi']]+3*[stirrGenConf.cover],
    lstPtsConcrLong=[pt_TB3,pt_TB2],
    spacStrpTransv=rd.hwall_stirrup['sTr'],
    spacStrpLong=rd.hwall_stirrup['sLn'],
    vDirLong=Vector(-1,0),
    nmbStrpTransv=rd.hwall_stirrup['nmbTr'],
    nmbStrpLong=rd.hwall_stirrup['nmbLn'],
    dispStrpTransv=0.0,
    dispStrpLong=rd.hwall_stirrup['dispLn'],
    vectorLRef=Vector(-0.36,-0.2),
    sideLabelLn='r',
    )

lstRebarFam+=[RF_hwall1_stirrup]
rebarCount+=1

RF_hwall2_stirrup=rb.stirrupFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rd.hwall_stirrup['fi'],
    lstPtsConcrTransv=[pt_LC2,pt_LC2-Vector(gd.skewThHeadWall,0),pt_LC4,pt_LC3],
    lstCover=[rd.deck_tr_bot['fi']-rd.hwall_stirrup['fi']]+3*[stirrGenConf.cover],
    lstPtsConcrLong=[pt_TB1,pt_TB4],
    spacStrpTransv=rd.hwall_stirrup['sTr'],
    spacStrpLong=rd.hwall_stirrup['sLn'],
    vDirLong=Vector(1,0),
    nmbStrpTransv=rd.hwall_stirrup['nmbTr'],
    nmbStrpLong=rd.hwall_stirrup['nmbLn'],
    dispStrpTransv=0.0,
    dispStrpLong=rd.hwall_stirrup['dispLn'],
    vectorLRef=Vector(0.36,-0.2),
    sideLabelLn='r',

)

lstRebarFam+=[RF_hwall2_stirrup]
rebarCount+=1

# longitudinal inferior en viga sobre pilotes (left)
rdef=rd.beam_pile_bot
RF_Lbeam_pile_bot=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    nmbBars=rdef['nmbBars'],
    lstPtsConcrSect=[pt_BP1,pt_BP2],
    coverSide='l',
    gapStart=-(wallGenConf.cover+rdef['fi']/2),
    gapEnd=-(wallGenConf.cover+rdef['fi']/2),
    extrShapeStart='anc90_posGood_tens',
    extrShapeEnd='anc90_posGood_tens',
    lstCover=[wallGenConf.cover+rd.pile_stirrup['fi']],
    fromToExtPts=[pt_TC5+Vector(rdef['extraLatCover'],0),pt_TC6-Vector(rdef['extraLatCover'],0)],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='l',
    vectorLRef=Vector(0.2,-0.1),
    )
lstRebarFam+=[RF_Lbeam_pile_bot]
rebarCount+=1

# longitudinal superior en viga sobre pilotes (left)
rdef=rd.beam_pile_top
RF_Lbeam_pile_top=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    nmbBars=rdef['nmbBars'],
    lstPtsConcrSect=[pt_BP4,pt_BP3],
    coverSide='r',
    gapStart=-(wallGenConf.cover+rdef['fi']/2),
    gapEnd=-(wallGenConf.cover+rdef['fi']/2),
    extrShapeStart='anc270_posGood_tens',
    extrShapeEnd='anc2700_posGood_tens',
    lstCover=[wallGenConf.cover+rd.pile_stirrup['fi']],
    fromToExtPts=[pt_TC5+Vector(rdef['extraLatCover'],hBeamPile),pt_TC6+Vector(-rdef['extraLatCover'],hBeamPile)],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    )
lstRebarFam+=[RF_Lbeam_pile_top]
rebarCount+=1

# longitudinal inferior en viga sobre pilotes (right)
rdef=rd.beam_pile_bot
RF_Rbeam_pile_bot=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    nmbBars=rdef['nmbBars'],
    lstPtsConcrSect=[pt_BP1,pt_BP2],
    coverSide='l',
    gapStart=-(wallGenConf.cover+rdef['fi']/2),
    gapEnd=-(wallGenConf.cover+rdef['fi']/2),
    extrShapeStart='anc90_posGood_tens',
    extrShapeEnd='anc90_posGood_tens',
    lstCover=[wallGenConf.cover+rd.pile_stirrup['fi']],
    fromToExtPts=[pt_TC9+Vector(rdef['extraLatCover'],0),pt_TC8-Vector(rdef['extraLatCover'],0)],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='l',
    )
lstRebarFam+=[RF_Rbeam_pile_bot]
rebarCount+=1

# longitudinal superior en viga sobre pilotes (right)
rdef=rd.beam_pile_top
RF_Rbeam_pile_top=rb.rebarFamily(
    reinfCfg=wallGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    nmbBars=rdef['nmbBars'],
    lstPtsConcrSect=[pt_BP4,pt_BP3],
    coverSide='r',
    gapStart=-(wallGenConf.cover+rdef['fi']/2),
    gapEnd=-(wallGenConf.cover+rdef['fi']/2),
    extrShapeStart='anc270_posGood_tens',
    extrShapeEnd='anc270_posGood_tens',
    lstCover=[wallGenConf.cover+rd.pile_stirrup['fi']],
    fromToExtPts=[pt_TC9+Vector(rdef['extraLatCover'],hBeamPile),pt_TC8+Vector(-rdef['extraLatCover'],hBeamPile)],
    coverSectBars=stirrGenConf.cover+rd.hwall_stirrup['fi'],
    sectBarsSide='r',
    )
lstRebarFam+=[RF_Rbeam_pile_top]
rebarCount+=1



# armadura de cortante sobre pilotes
rdef=rd.pile_stirrup
RF_pileIzq_stirrup=rb.stirrupFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    lstPtsConcrTransv=[pt_TC5,pt_TC6,pt_TC6+Vector(0,hBeamPile),pt_TC5+Vector(0,hBeamPile)],
    lstCover=4*[stirrGenConf.cover],
    lstPtsConcrLong=[pt_WLH1,pt_WLH2],
    spacStrpTransv=rdef['sTr'],
    spacStrpLong=rdef['sLn'],
    vDirLong=Vector(1,0),
    nmbStrpTransv=rdef['nmbTr'],
    nmbStrpLong=rdef['nmbLn'],
    dispStrpTransv=rdef['dispTr'],
    dispStrpLong=rdef['dispLn'],
    vectorLRef=Vector(0.45,-0.2),
    sideLabelLn='l',
    )

lstRebarFam+=[RF_pileIzq_stirrup]
rebarCount+=1

rdef=rd.pile_stirrup
RF_pileDer_stirrup=rb.stirrupFamily(
    reinfCfg=stirrGenConf,
    identifier=str(rebarCount+1),
    diameter=rdef['fi'],
    lstPtsConcrTransv=[pt_TC9,pt_TC8,pt_TC8+Vector(0,hBeamPile),pt_TC9+Vector(0,hBeamPile)],
    lstCover=4*[stirrGenConf.cover],
    lstPtsConcrLong=[pt_LC1+Vector(0,gd.thDeck-gd.thPrelosa),pt_LC1],
    spacStrpTransv=rdef['sTr'],
    spacStrpLong=rdef['sLn'],
    vDirLong=Vector(1,0),
    nmbStrpTransv=rdef['nmbTr'],
    nmbStrpLong=rdef['nmbLn'],
    dispStrpTransv=rdef['dispTr'],
    dispStrpLong=rdef['dispLn'],
    vectorLRef=Vector(0.45,-0.2),
    sideLabelLn='r',
    )

lstRebarFam+=[RF_pileDer_stirrup]
rebarCount+=1

if rd.stirr_paral_pile['fi'] >0:
    # armadura de cortante paralela a líneas de pilotes (abrazando armadura transversal)
    # lado izquierdo
    rdef=rd.stirr_paral_pile #diccionario de parámetros de la armadura
    RF_bndParPileIzq_stirrup=rb.stirrupFamily(
        reinfCfg=stirrGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrTransv=[pt_LC1,pt_LC1+Vector(rdef['bStirr'],0),pt_LC1+Vector(rdef['bStirr'],gd.thDeck-gd.thPrelosa),pt_LC1+Vector(0,gd.thDeck-gd.thPrelosa)],
        lstCover=[rd.deck_tr_bot['fi']-rdef['fi'],0,stirrGenConf.cover,0],
        lstPtsConcrLong=[pt_TC4,pt_TC1],
        spacStrpTransv=rdef['sTr'],
        spacStrpLong=rdef['sLn'],
        vDirLong=Vector(1,0),
        nmbStrpTransv=rdef['nmbTr'],
        nmbStrpLong=rdef['nmbLn'],
        dispStrpTransv=stirrGenConf.cover+rdef['dispTr'],
        dispStrpLong=gd.skewThwall+rdef['dispLn'],
        vectorLRef=Vector(-0.2,-0.3),
        )

    lstRebarFam+=[RF_bndParPileIzq_stirrup]
    rebarCount+=1

    # armadura de cortante paralela a líneas de pilotes (abrazando armadura transversal)
    # lado derecho
    rdef=rd.stirr_paral_pile #diccionario de parámetros de la armadura
    RF_bndParPileDer_stirrup=rb.stirrupFamily(
        reinfCfg=stirrGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrTransv=[pt_LC1,pt_LC1+Vector(rdef['bStirr'],0),pt_LC1+Vector(rdef['bStirr'],gd.thDeck-gd.thPrelosa),pt_LC1+Vector(0,gd.thDeck-gd.thPrelosa)],
        lstCover=[rd.deck_tr_bot['fi']-rdef['fi'],0,stirrGenConf.cover,0],
        lstPtsConcrLong=[pt_TC3,pt_TC2],
        spacStrpTransv=rdef['sTr'],
        spacStrpLong=rdef['sLn'],
        vDirLong=Vector(-1,0),
        nmbStrpTransv=rdef['nmbTr'],
        nmbStrpLong=rdef['nmbLn'],
        dispStrpTransv=stirrGenConf.cover+rdef['dispTr'],
        dispStrpLong=gd.skewThwall+rdef['dispLn'],
        vectorLRef=Vector(-0.2,-0.3),
        sideLabelLn='r',
        )

    lstRebarFam+=[RF_bndParPileDer_stirrup]
    rebarCount+=1

if rd.stirr_paral_headwall['fi'] >0:
    #armadura de cortante paralela al murete de guarda (abrazando armadura longitudinal)
    # lado inicial
    rdef=rd.stirr_paral_headwall #diccionario de parámetros de la armadura
    RF_bndParHeadwStart_stirrup=rb.stirrupFamily(
        reinfCfg=stirrGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrTransv=[pt_TC1,pt_TC1+Vector(rdef['bStirr'],0),pt_TC1+Vector(rdef['bStirr'],gd.thDeck-gd.thPrelosa),pt_TC1+Vector(0,gd.thDeck-gd.thPrelosa)],
        lstCover=[2*rd.deck_tr_bot['fi']-rdef['fi'],0,stirrGenConf.cover,0],
        lstPtsConcrLong=[pt_LC6,pt_LC6-Vector(0,gd.thDeck-gd.thPrelosa)],
        spacStrpTransv=rdef['sTr'],
        spacStrpLong=rdef['sLn'],
        vDirLong=Vector(1,0),
        nmbStrpTransv=rdef['nmbTr'],
        nmbStrpLong=rdef['nmbLn'],
        dispStrpTransv=gd.skewThwall+rdef['dispTr'],
        dispStrpLong=rdef['dispLn'],
        vectorLRef=Vector(-0.4,-0.2),
        )

    lstRebarFam+=[RF_bndParHeadwStart_stirrup]
    rebarCount+=1

    #armadura de cortante paralela al murete de guarda (abrazando armadura longitudinal)
    # lado final
    rdef=rd.stirr_paral_headwall #diccionario de parámetros de la armadura
    RF_bndParHeadwEnd_stirrup=rb.stirrupFamily(
        reinfCfg=stirrGenConf,
        identifier=str(rebarCount+1),
        diameter=rdef['fi'],
        lstPtsConcrTransv=[pt_TC1,pt_TC1+Vector(rdef['bStirr'],0),pt_TC1+Vector(rdef['bStirr'],gd.thDeck-gd.thPrelosa),pt_TC1+Vector(0,gd.thDeck-gd.thPrelosa)],
        lstCover=[2*rd.deck_tr_bot['fi']-rdef['fi'],0,stirrGenConf.cover,0],
        lstPtsConcrLong=[pt_LC5,pt_LC5-Vector(0,gd.thDeck-gd.thPrelosa)],
        spacStrpTransv=rdef['sTr'],
        spacStrpLong=rdef['sLn'],
        vDirLong=Vector(-1,0),
        nmbStrpTransv=rdef['nmbTr'],
        nmbStrpLong=rdef['nmbLn'],
        dispStrpTransv=gd.skewThwall+rdef['dispTr'],
        dispStrpLong=rdef['dispLn'],
        vectorLRef=Vector(-0.2,-0.15),
        sideLabelLn='r',
        )

    lstRebarFam+=[RF_bndParHeadwEnd_stirrup]
    rebarCount+=1


#     SECCIONES ARMADO

hSectLn=gd.thDeck+gd.hHeadWall+0.75 # espacio vertical para sección longitudinal
hSectTr=max(gd.hLeftWall+gd.thDeck,gd.hRightWall+gd.thDeck)+0.75

nextAnchor=0

# Sección longitudinal central (LC). SECCIÓN A-A 
vTrans_AA=Vector(0,nextAnchor)
lstPtsConcrSect=[[pt_LC1,pt_LC2,pt_LC3,pt_LC4,pt_LC5,pt_LC6,pt_LC7,pt_LC8,pt_LC1]]
lstShapeRebarFam=[RF_deck_ln_bot,RF_deck_ln_top]
lstSectRebarFam=[RF_deck_tr_bot,RF_deck_tr_top]
lstSectRebarFam+=[RF_hwall1_top,RF_hwall2_top,RF_hwall1_lat_ext,RF_hwall2_lat_ext,RF_hwall1_lat_int,RF_hwall2_lat_int]
if  rd.deck_tr_bot_b1:
    lstSectRebarFam+=[RF_deck_tr_bot_b1S,RF_deck_tr_bot_b1E]
lstShapeStirrupFam=[RF_hwall1_stirrup,RF_hwall2_stirrup]
lstEdgeStirrupFam=[]
if rd.stirr_paral_headwall['fi']>0:
    lstEdgeStirrupFam=[RF_bndParHeadwStart_stirrup,RF_bndParHeadwEnd_stirrup]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,lstShapeStirrupFam=lstShapeStirrupFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTrans_AA)
lstPntsPrelosa=[pt_LC1_prelosa,pt_LC2_prelosa,pt_LC2,pt_LC1,pt_LC1_prelosa]
rb.drawConcreteSection(lstPntsPrelosa,vTrans_AA)
nextAnchor-=hSectLn


# Sección longitudinal por la banda de refuerzo a cortante paralela a los pilotes (LC). SECCIÓN B-B 
if  rd.stirr_paral_pile['fi']>0 or rd.width_b1>0:
    # Sección longitudinal por la banda de refuerzo a cortante paralela a los pilotes (LC). SECCIÓN B-B 
    vTrans_BB=Vector(0,nextAnchor)
    lstPtsConcrSect=[[pt_LC1,pt_LC2,pt_LC3,pt_LC4,pt_LC5,pt_LC6,pt_LC7,pt_LC8,pt_LC1]]
    lstShapeRebarFam=[RF_deck_ln_bot,RF_deck_ln_top]
    lstSectRebarFam=[RF_deck_tr_bot,RF_deck_tr_top]
    lstSectRebarFam+=[RF_hwall1_top,RF_hwall2_top,RF_hwall1_lat_ext,RF_hwall2_lat_ext,RF_hwall1_lat_int,RF_hwall2_lat_int]
    if  rd.deck_tr_bot_b1:
        lstSectRebarFam+=[RF_deck_tr_bot_b1S,RF_deck_tr_bot_b1E]
    lstEdgeStirrupFam=[]
    if rd.stirr_paral_headwall['fi']>0:
        lstEdgeStirrupFam=[RF_bndParHeadwStart_stirrup,RF_bndParHeadwEnd_stirrup]
    lstShapeStirrupFam=[RF_hwall1_stirrup,RF_hwall2_stirrup]
    if rd.stirr_paral_pile['fi']>0:
        lstShapeStirrupFam+=[RF_bndParPileIzq_stirrup]
    rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,lstShapeStirrupFam=lstShapeStirrupFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTrans_BB)
    lstPntsPrelosa=[pt_LC1_prelosa,pt_LC2_prelosa,pt_LC2,pt_LC1,pt_LC1_prelosa]
    rb.drawConcreteSection(lstPntsPrelosa,vTrans_BB)
    nextAnchor-=hSectLn


# Sección horizontal longitudinal de muro por viga sobre pilote
vTransWLH=Vector(0,nextAnchor)
lstPtsConcrSect=[[pt_WLH1,pt_WLH2,pt_WLH3,pt_WLH4,pt_WLH1]]
lstShapeRebarFam=[RF_Lwall_hor_ext,RF_Lwall_hor_int]
lstSectRebarFam=[RF_Lwall_vert_ext,RF_Lwall_vert_int]
lstEdgeStirrupFam=[RF_pileIzq_stirrup]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTransWLH)
nextAnchor-=hSectLn

# Sección transversal esviada central (LC). SECCIÓN D-D
vTrans_DD=Vector(0,nextAnchor)
lstPtsConcrSect=[[pt_TC1,pt_TC5,pt_TC6,pt_TC7,pt_TC1_prelosa,pt_TC4_prelosa,pt_TC3_prelosa,pt_TC2_prelosa,pt_TC10,pt_TC9,pt_TC8,pt_TC2,pt_TC3,pt_TC4,pt_TC1]]
lstShapeRebarFam=[RF_deck_tr_bot,RF_deck_tr_top]
lstShapeRebarFam+=[RF_Lwall_vert_int_dowel,RF_Rwall_vert_int_dowel]
lstShapeRebarFam+=[RF_Lwall_vert_ext,RF_Lwall_vert_int,RF_Rwall_vert_ext,RF_Rwall_vert_int]
lstSectRebarFam=[RF_deck_ln_bot,RF_deck_ln_top]
lstSectRebarFam+=[RF_Lwall_hor_ext,RF_Lwall_hor_int,RF_Rwall_hor_ext,RF_Rwall_hor_int]
lstSectRebarFam+=[RF_Lbeam_pile_bot,RF_Lbeam_pile_top]
lstSectRebarFam+=[RF_Rbeam_pile_bot,RF_Rbeam_pile_top]
lstShapeStirrupFam=[RF_pileIzq_stirrup,RF_pileDer_stirrup]
lstEdgeStirrupFam=[]
if rd.stirr_paral_pile['fi']>0:
    lstEdgeStirrupFam+=[RF_bndParPileIzq_stirrup,RF_bndParPileDer_stirrup]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,lstShapeStirrupFam=lstShapeStirrupFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTrans_DD)
lstPntsPrelosa=[pt_TC1_prelosa,pt_TC2_prelosa,pt_TC3_prelosa,pt_TC4_prelosa,pt_TC1_prelosa]
rb.drawConcreteSection(lstPntsPrelosa,vTrans_DD)
# junta de construcción
vThPrelosa=Vector(0,gd.thPrelosa)
lstPtsJunta=[pt_TC1-vThPrelosa,pt_TC4_prelosa-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans_DD,color=cfg.colorHidden)
lstPtsJunta=[pt_TC3_prelosa-vThPrelosa,pt_TC2-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans_DD,color=cfg.colorHidden)

nextAnchor-=hSectTr               

# Sección transversal esviada por banda de cercos paralelos a murete de guarda.  SECCIÓN E-E
if rd.stirr_paral_headwall['fi']>0 or rd.width_b1>0 :
    # Sección transversal esviada por banda de cercos paralelos a murete de guarda.  SECCIÓN E-E
    vTrans_EE=Vector(0,nextAnchor)
    #lstPtsConcrSect=[[pt_TC1,pt_TC2,pt_TC3,pt_TC4,pt_TC1]]
    lstShapeRebarFam=[RF_deck_tr_top]
    if  rd.deck_tr_bot_b1:
        lstShapeRebarFam+=[RF_deck_tr_bot_b1S]
    else:
        lstShapeRebarFam+=[RF_deck_tr_bot]
    lstShapeRebarFam+=[RF_Lwall_vert_ext,RF_Lwall_vert_int,RF_Rwall_vert_ext,RF_Rwall_vert_int]
    lstShapeRebarFam+=[RF_Lwall_vert_int_dowel,RF_Rwall_vert_int_dowel]
    lstSectRebarFam=[RF_deck_ln_bot,RF_deck_ln_top]
    lstSectRebarFam+=[RF_Lwall_hor_ext,RF_Lwall_hor_int,RF_Rwall_hor_ext,RF_Rwall_hor_int]
    lstSectRebarFam+=[RF_Lbeam_pile_bot,RF_Lbeam_pile_top]
    lstSectRebarFam+=[RF_Rbeam_pile_bot,RF_Rbeam_pile_top]
    lstShapeStirrupFam=[RF_pileIzq_stirrup,RF_pileDer_stirrup]
    if rd.stirr_paral_headwall['fi']>0:
        lstShapeStirrupFam+=[RF_bndParHeadwStart_stirrup]
    lstEdgeStirrupFam=None#[]
    rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,lstShapeStirrupFam=lstShapeStirrupFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTrans_EE)
    rb.drawConcreteSection(lstPntsPrelosa,vTrans_EE)
    # junta de construcción
    lstPtsJunta=[pt_TC1-vThPrelosa,pt_TC4_prelosa-vThPrelosa]
    rb.drawConcreteSection(lstPtsJunta,vTrans_EE,color=cfg.colorHidden)
    lstPtsJunta=[pt_TC3_prelosa-vThPrelosa,pt_TC2-vThPrelosa]
    rb.drawConcreteSection(lstPtsJunta,vTrans_EE,color=cfg.colorHidden)
    nextAnchor-=hSectTr               



# Sección transversal esviada de borde (TB) por murete de guarda. SECCIÓN F-F
vTrans_FF=Vector(0,nextAnchor)-Vector(0,0.7)
lstPtsConcrSect=[[pt_TB1,pt_TC5,pt_TC6,pt_TC7,pt_TC1_prelosa,pt_TC4_prelosa,pt_TC3_prelosa,pt_TC2_prelosa,pt_TC10,pt_TC9,pt_TC8,pt_TB2,pt_TB3,pt_TB4,pt_TB1]]
lstShapeRebarFam=[RF_deck_tr_top]
if  rd.deck_tr_bot_b1:
    lstShapeRebarFam+=[RF_deck_tr_bot_b1S]
else:
    lstShapeRebarFam+=[RF_deck_tr_bot]
lstShapeRebarFam+=[RF_hwall1_top]
lstShapeRebarFam+=[RF_Lwall_vert_ext,RF_Lwall_vert_int,RF_Rwall_vert_ext,RF_Rwall_vert_int]
lstShapeRebarFam+=[RF_Lwall_vert_int_dowel,RF_Rwall_vert_int_dowel]

lstSectRebarFam=[RF_deck_ln_bot,RF_deck_ln_top]
lstSectRebarFam+=[RF_Lwall_hor_ext,RF_Lwall_hor_int,RF_Rwall_hor_ext,RF_Rwall_hor_int]
lstSectRebarFam+=[RF_Lbeam_pile_bot,RF_Lbeam_pile_top]
lstSectRebarFam+=[RF_Rbeam_pile_bot,RF_Rbeam_pile_top]
lstShapeStirrupFam=[RF_pileIzq_stirrup,RF_pileDer_stirrup]
lstEdgeStirrupFam=[RF_hwall1_stirrup]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam=lstShapeRebarFam,lstSectRebarFam=lstSectRebarFam,lstShapeStirrupFam=lstShapeStirrupFam,lstEdgeStirrupFam=lstEdgeStirrupFam,vTranslation=vTrans_FF)
rb.drawConcreteSection(lstPntsPrelosa,vTrans_FF)
# junta de construcción
lstPtsJunta=[pt_TC1-vThPrelosa,pt_TC4_prelosa-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans_FF,color=cfg.colorHidden)
lstPtsJunta=[pt_TC3_prelosa-vThPrelosa,pt_TC2-vThPrelosa]
rb.drawConcreteSection(lstPtsJunta,vTrans_FF,color=cfg.colorHidden)
nextAnchor-=hSectTr

'''

# Sección horizontal por el murete de guarda
vTransTH=Vector(0,nextAnchor)
lstPtsConcrSect=[[pt_TH1,pt_TH2,pt_TH3,pt_TH4,pt_TH1]]
lstShapeRebarFam=[RF_hwall1_lat_ext,RF_hwall1_lat_ext]
lstSectRebarFam=None
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=vTransTH)
nextAnchor-=hSectLn


# sección vertical de viga sobre pilote
vTransLBP=vTransWLH+Vector(0,nextAnchor)
lstPtsConcrSect=[[pt_BP4,pt_BP1,pt_BP2,pt_BP3]]
lstShapeRebarFam=[RF_Lbeam_pile_bot,RF_Lbeam_pile_top]
lstSectRebarFam=[]
rb.drawRCSection(lstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=vTransLBP)
nextAnchor-=hSectLn
'''
