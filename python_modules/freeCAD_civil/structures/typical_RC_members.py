# -*- coding: iso-8859-1 -*-

import math
import Part, FreeCAD
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector

           
def closed_slab(width,length,thickness,botTrnsRb,topTrnsRb,botLnRb,topLnRb,anchPtTrnsSect,anchPtLnSect,genConf,drawConrTrSect='Y',drawConrLnSect='Y'):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal

    :param width: dimension of the slab in the direction of the transversal rebars
    :param length: dimension of the slab in the direction of the longitudinal rebars
    :param thickness: thickness of the slab
    :param botTrnsRb: data for bottom transversal rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family, 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the slab (as it is drawn in the section),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the slab (as it is drawn in the section)
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
        fromToExtPts=[ln_bl+Vector(botTrnsRb['distRFstart'],0),ln_br-Vector(botTrnsRb['distRFend'],0)],
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
        fromToExtPts=[ln_tl+Vector(topTrnsRb['distRFstart'],0),ln_tr-Vector(topTrnsRb['distRFend'],0)],
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
        fromToExtPts=[tr_bl+Vector(botLnRb['distRFstart'],0),tr_br-Vector(botLnRb['distRFend'],0)],
        coverSectBars=genConf.cover+botTrnsRb['fi'],
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
        fromToExtPts=[tr_tl+Vector(topLnRb['distRFstart'],0),tr_tr-Vector(topLnRb['distRFend'],0)],
        coverSectBars=genConf.cover+topTrnsRb['fi'],
        sectBarsSide='r',
        vectorLRefSec=Vector(0.6*width,0.3)
        )
    ln_top_rf.createRebar()
    ln_top_rf.drawSectBars()
    ln_top_rf.drawRebar()
    # Concrete transversal cross-section
    if drawConrTrSect[0].lower()=='y':
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        Part.show(s)
    if drawConrLnSect[0].lower()=='y':
        s=Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
        Part.show(s)
    FreeCAD.ActiveDocument.recompute()    
    

def wall(height,length,thickness,leftVertRb,rightVertRb,leftHorRb,rightHorRb,anchPtVertSect,anchPtHorSect,genConf,drawConrVertSect='Y',drawConrHorSect='Y'):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: l-left, r-right, vert-vertical, hor-horizontal

    :param height: dimension of the wall in the direction of the vertical rebars
    :param length: dimension of the wall in the direction of the horizontal rebars
    :param thickness: thickness of the wall
    :param leftVertRb: data for left vertical rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family, 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the wall (as it is drawn in the section),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the wall (as it is drawn in the section)
    :param rightVertRb: same for the right vertical rebar family
    :param leftHorRb: same for the left horizontal rebar family
    :param rightHorRb: same for the right horizontal rebar family
    :param anchPtVertSect: anchor point to place the left left corner of the concrete vertical cross-section
    :param anchPtHorSect:  anchor point to place the left left corner of the concrete horizontal cross-section
    :param genConf: instance of the reinf_bars.genericConf class
    :param drawConrVertSect: 'Y' to draw the vertical concrete cross-section  (defaults to 'Y')
    :param drawConrHorSect: 'Y' to draw the horizontal concrete cross-section  (defaults to 'Y')
    '''
           
    # Concrete points of the vertical section
    vert_bl=anchPtVertSect
    vert_tl=vert_bl+Vector(0,height)
    vert_tr=vert_tl+Vector(thickness,0)
    vert_br= vert_bl+Vector(thickness,0)
    # Concrete points of the horizontal section
    hor_bl=anchPtHorSect
    hor_tl=hor_bl+Vector(0,length)
    hor_tr=hor_tl+Vector(thickness,0)
    hor_br= hor_bl+Vector(thickness,0)
    # Families of rebars
    # vertical left rebar family
    vert_left_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=leftVertRb['id'],
        diameter=leftVertRb['fi'],
        spacing=leftVertRb['s'],
        lstPtsConcrSect=[vert_bl,vert_tl,vert_tr],
        coverSide='r',
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[hor_bl+Vector(0,leftVertRb['distRFstart']),hor_tl-Vector(0,leftVertRb['distRFend'])],
        sectBarsSide='r',
        vectorLRefSec=Vector(-0.3,0.6*length)
        )
    vert_left_rf.createRebar()
    vert_left_rf.drawSectBars()
    vert_left_rf.drawRebar()
    # vertical left rebar family
    vert_right_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=rightVertRb['id'],
        diameter=rightVertRb['fi'],
        spacing=rightVertRb['s'],
        lstPtsConcrSect=[vert_br,vert_tr,vert_tl],
        coverSide='l',
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[hor_br+Vector(0,rightVertRb['distRFstart']),hor_tr-Vector(0,rightVertRb['distRFend'])],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.3,0.6*length)
        )
    vert_right_rf.createRebar()
    vert_right_rf.drawSectBars()
    vert_right_rf.drawRebar()
    hor_left_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=leftHorRb['id'],
        diameter=leftHorRb['fi'],
        spacing=leftHorRb['s'],
        lstPtsConcrSect=[hor_br,hor_bl,hor_tl,hor_tr],
        coverSide='r',
        lstCover=[genConf.cover,genConf.cover+leftVertRb['fi'],genConf.cover],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[vert_bl+Vector(0,leftHorRb['distRFstart']),vert_tl-Vector(0,leftHorRb['distRFend'])],
        coverSectBars=genConf.cover+leftVertRb['fi'],
        sectBarsSide='r',
        vectorLRefSec=Vector(-0.3,0.6*height)
        )
    hor_left_rf.createRebar()
    hor_left_rf.drawSectBars()
    hor_left_rf.drawRebar()
    hor_right_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=rightHorRb['id'],
        diameter=rightHorRb['fi'],
        spacing=rightHorRb['s'],
        lstPtsConcrSect=[hor_bl,hor_br,hor_tr,hor_tl],
        coverSide='l',
        lstCover=[genConf.cover,genConf.cover+rightVertRb['fi'],genConf.cover],
        vectorLRef=Vector(0.3,0.4),
        fromToExtPts=[vert_br+Vector(0,rightHorRb['distRFstart']),vert_tr-Vector(0,rightHorRb['distRFend'])],
        coverSectBars=genConf.cover+rightVertRb['fi'],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.3,0.6*height)
        )
    hor_right_rf.createRebar()
    hor_right_rf.drawSectBars()
    hor_right_rf.drawRebar()
    # Concrete vertical cross-section
    if drawConrVertSect[0].lower()=='y':
        s=Part.makePolygon([vert_bl,vert_tl,vert_tr,vert_br,vert_bl])
        Part.show(s)
    if drawConrHorSect[0].lower()=='y':
        s=Part.makePolygon([hor_bl,hor_tl,hor_tr,hor_br,hor_bl])
        Part.show(s)
    FreeCAD.ActiveDocument.recompute()    
    
def set_FR_options(RF,RFdef):
    if 'gapStart' in RFdef.keys(): RF.gapStart=RFdef['gapStart']
    if 'gapEnd' in RFdef.keys(): RF.gapEnd=RFdef['gapEnd']
    if 'anchStart' in RFdef.keys(): RF.anchStart=RFdef['anchStart']
    if 'anchEnd' in RFdef.keys(): RF.anchStart=RFdef['anchEnd']
    if 'fixLengthStart' in RFdef.keys(): RF.anchStart=RFdef['fixLengthStart']
    if 'fixLengthEnd' in RFdef.keys(): RF.anchStart=RFdef['fixLengthEnd']
           
def generic_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,genConf,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,drawConrTrSect='Y',drawConrLnSect='Y'):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

    :param width: dimension of the brick in the direction of the transversal rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transversal cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param genConf: instance of the reinf_bars.genericConf class
    :param angTrns: angle (degrees) between the horizontal and the brick width dimension
    :param angLn: angle (degrees) between the horizontal and the brick length dimension
    :param botTrnsRb: data for bottom transversal rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family, 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the brick (as it is drawn in the section),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the brick (as it is drawn in the section)
    :param topTrnsRb: same for the top transversal rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param drawConrTrSect: 'Y' to draw the transversal concrete cross-section  (defaults to 'Y')
    :param drawConrLnSect: 'Y' to draw the longitudinal concrete cross-section  (defaults to 'Y')
    '''
    vdirTr=Vector(math.cos(math.radians(angTrns)),math.sin(math.radians(angTrns)))
    vdirLn=Vector(math.cos(math.radians(angLn)),math.sin(math.radians(angLn)))
    # Concrete points of the transverse section
    tr_bl=anchPtTrnsSect
    tr_tl=tr_bl+thickness*Vector(-vdirTr.y,vdirTr.x)
    tr_tr=tr_tl+width*vdirTr
    tr_br= tr_bl+width*vdirTr
    # Concrete points of the longitudinal section
    ln_bl=anchPtLnSect
    ln_tl=ln_bl+thickness*Vector(-vdirLn.y,vdirLn.x)
    ln_tr=ln_tl+length*vdirLn
    ln_br= ln_bl+length*vdirLn
    # Families of rebars
    # transversal bottom rebar family
    tr_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botTrnsRb['id'],
        diameter=botTrnsRb['fi'],
        spacing=botTrnsRb['s'],
        lstPtsConcrSect=[tr_bl,tr_br],
        coverSide='l',
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[ln_bl+botTrnsRb['distRFstart']*vdirLn,ln_br-botTrnsRb['distRFend']*vdirLn],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.6*length,-0.3),
        gapStart=0,
        gapEnd=0
        )
    set_FR_options(RF=tr_bot_rf,RFdef=botTrnsRb)
    tr_bot_rf.createRebar()
    tr_bot_rf.drawSectBars()
    tr_bot_rf.drawRebar()
    # transversal bottom rebar family
    tr_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topTrnsRb['id'],
        diameter=topTrnsRb['fi'],
        spacing=topTrnsRb['s'],
        lstPtsConcrSect=[tr_tl,tr_tr],
        coverSide='r',
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[ln_tl+topTrnsRb['distRFstart']*vdirLn,ln_tr-topTrnsRb['distRFend']*vdirLn],
        sectBarsSide='r',
        vectorLRefSec=Vector(0.6*length,0.3),
        gapStart=0,
        gapEnd=0
        )
    set_FR_options(RF=tr_top_rf,RFdef=topTrnsRb)    
    tr_top_rf.createRebar()
    tr_top_rf.drawSectBars()
    tr_top_rf.drawRebar()
    ln_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botLnRb['id'],
        diameter=botLnRb['fi'],
        spacing=botLnRb['s'],
        lstPtsConcrSect=[ln_bl,ln_br],
        coverSide='l',
        lstCover=[genConf.cover+botTrnsRb['fi']],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[tr_bl+botLnRb['distRFstart']*vdirTr,tr_br-botLnRb['distRFend']*vdirTr],
        coverSectBars=genConf.cover+botTrnsRb['fi'],
        sectBarsSide='l',
        vectorLRefSec=Vector(0.6*width,-0.3),
        gapStart=0,
        gapEnd=0
       )
    set_FR_options(RF=ln_bot_rf,RFdef=botLnRb)
    ln_bot_rf.createRebar()
    ln_bot_rf.drawSectBars()
    ln_bot_rf.drawRebar()
    ln_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topLnRb['id'],
        diameter=topLnRb['fi'],
        spacing=topLnRb['s'],
        lstPtsConcrSect=[ln_tl,ln_tr],
        coverSide='r',
        lstCover=[genConf.cover+topTrnsRb['fi']],
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[tr_tl+topLnRb['distRFstart']*vdirTr,tr_tr-topLnRb['distRFend']*vdirTr],
        coverSectBars=genConf.cover+topTrnsRb['fi'],
        sectBarsSide='r',
        vectorLRefSec=Vector(0.6*width,0.3),
        gapStart=0,
        gapEnd=0
        )
    set_FR_options(RF=ln_top_rf,RFdef=topLnRb)
    ln_top_rf.createRebar()
    ln_top_rf.drawSectBars()
    ln_top_rf.drawRebar()
    # Concrete transversal cross-section
    if drawConrTrSect[0].lower()=='y':
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        Part.show(s)
    if drawConrLnSect[0].lower()=='y':
        s=Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
        Part.show(s)
    FreeCAD.ActiveDocument.recompute()    
