# -*- coding: iso-8859-1 -*-

import Part, FreeCAD
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector

           
def closed_slab(width,length,thickness,botTrnsRb,topTrnsRb,botLnRb,topLnRb,anchPtTrnsSect,anchPtLnSect,genConf,drawConrTrSect='Y',drawConrLnSect='Y'):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal

    :param width: dimension of the slab in the direction of the transversal rebars
    :param length: dimension of the slab in the direction of the longitudinal rebars
    :param thickness: thickness of the slab
    :param botTrnsRb: data for bottom transversal rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'gapL':0.2,'gapR':0.1}, where 'id' is the identificacion of the rebar family, 'fi' is the diameter of the rebar, 's' is the spacement, 'gapL' is the distance from the first rebar of the family to the left extremity of the slab (as it is drawn in the section),   'gapR' is the distance from the last rebar of the family to the rigth extremity of the slab (as it is drawn in the section)
    :param topTrnsRb: same for the top transversal rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transversal cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param genConf: instance of the reinf_bars.genericConf class
    :param drawConrTrSect: 'Y' to draw the transversal concrete cross-section  (defaults to 'Y')
    :param drawConrLnSect: 'Y' to draw the longitudinal concrete cross-section  (defaults to 'Y')
    '''
           
    # Concrete points of the transverse section
    tr_bl=anchPtTrnsSect
    tr_tl=tr_bl+Vector(0,thickness)
    tr_tr=tr_tl+Vector(width,0)
    tr_br= tr_bl+Vector(width,0)
    # Concrete points of the longitudinal section
    ln_bl=anchPtLnSect
    ln_tl=ln_bl+Vector(0,thickness)
    ln_tr=ln_tl+Vector(length,0)
    ln_br= ln_bl+Vector(length,0)
    # Families of rebars
    # transversal bottom rebar family
    tr_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botTrnsRb['id'],
        diameter=botTrnsRb['fi'],
        spacing=botTrnsRb['s'],
        lstPtsConcrSect=[tr_tl,tr_bl,tr_br,tr_tr],
        coverSide='l',
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[ln_bl+Vector(botTrnsRb['gapL'],0),ln_br-Vector(botTrnsRb['gapR'],0)],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.6*length,-0.3)
        )
    tr_bot_rf.createRebar()
    tr_bot_rf.drawSectBars()
    tr_bot_rf.drawRebar()
    # transversal bottom rebar family
    tr_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topTrnsRb['id'],
        diameter=topTrnsRb['fi'],
        spacing=topTrnsRb['s'],
        lstPtsConcrSect=[tr_bl,tr_tl,tr_tr,tr_br],
        coverSide='r',
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[ln_tl+Vector(topTrnsRb['gapL'],0),ln_tr-Vector(topTrnsRb['gapR'],0)],
        sectBarsSide='r',
        vectorLRefSec=Vector(0.6*length,0.3)
        )
    tr_top_rf.createRebar()
    tr_top_rf.drawSectBars()
    tr_top_rf.drawRebar()
    ln_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botLnRb['id'],
        diameter=botLnRb['fi'],
        spacing=botLnRb['s'],
        lstPtsConcrSect=[ln_tl,ln_bl,ln_br,ln_tr],
        coverSide='l',
        lstCover=[genConf.cover,genConf.cover+botTrnsRb['fi'],genConf.cover],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[tr_bl+Vector(botLnRb['gapL'],0),tr_br-Vector(botLnRb['gapR'],0)],
        coverSectBars=genConf.cover++botTrnsRb['fi'],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.6*width,-0.3)
        )
    ln_bot_rf.createRebar()
    ln_bot_rf.drawSectBars()
    ln_bot_rf.drawRebar()
    ln_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topLnRb['id'],
        diameter=topLnRb['fi'],
        spacing=topLnRb['s'],
        lstPtsConcrSect=[ln_bl,ln_tl,ln_tr,ln_br],
        coverSide='r',
        lstCover=[genConf.cover,genConf.cover+topTrnsRb['fi'],genConf.cover],
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[tr_tl+Vector(topLnRb['gapL'],0),tr_tr-Vector(topLnRb['gapR'],0)],
        coverSectBars=genConf.cover++topTrnsRb['fi'],
        sectBarsSide='r',
        vectorLRefSec=Vector(0.6*width,0.3)
        )
    ln_top_rf.createRebar()
    ln_top_rf.drawSectBars()
    ln_top_rf.drawRebar()
    # Concrete transversal cross-section
    if drawConrTrSect[0].lower()=='y':
        Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
    if drawConrLnSect[0].lower()=='y':
        Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
    FreeCAD.ActiveDocument.recompute()    
    
