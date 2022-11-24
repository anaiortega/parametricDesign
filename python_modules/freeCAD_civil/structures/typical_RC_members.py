# -*- coding: iso-8859-1 -*-

import math
import Part, FreeCAD
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
import FreeCADGui

colorConcrete=(0.00,1.00,1.00) #cyan

def closed_slab(width,length,thickness,botTrnsRb,topTrnsRb,botLnRb,topLnRb,anchPtTrnsSect,anchPtLnSect,genConf,drawConcrTrSect=True,drawConcrLnSect=True,factGap=1,coverLat=None):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal

    :param width: dimension of the slab in the direction of the transverse rebars
    :param length: dimension of the slab in the direction of the longitudinal rebars
    :param thickness: thickness of the slab
    :param botTrnsRb: data for bottom transverse rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family, 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the slab (as it is drawn in the section),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the slab (as it is drawn in the section)
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param genConf: instance of the reinf_bars.genericConf class
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    :param factGap: the gapSart and gapEnd are made equal to factGap*cover
    :param coverLat: lateral cover (if None, genConf.cover is used)
    '''
    cover=genConf.cover
    if not coverLat:
        coverLat=genConf.cover
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
    # transverse bottom rebar family
    tr_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botTrnsRb['id'],
        diameter=botTrnsRb['fi'],
        spacing=botTrnsRb['s'],
        lstPtsConcrSect=[tr_tl,tr_bl,tr_br,tr_tr],
        lstCover=[coverLat,cover,coverLat],
        coverSide='l',
        vectorLRef=Vector(-0.15,-0.35),
        fromToExtPts=[ln_bl+Vector(botTrnsRb['distRFstart'],0),ln_br-Vector(botTrnsRb['distRFend'],0)],
        sectBarsSide='l',
        gapStart=-factGap*genConf.cover,
        gapEnd=-factGap*genConf.cover,
        )
    tr_bot_rf.createLstRebar()
    tr_bot_rf.drawSectBars()
    tr_bot_rf.drawLstRebar()
    
    # transverse bottom rebar family
    tr_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topTrnsRb['id'],
        diameter=topTrnsRb['fi'],
        spacing=topTrnsRb['s'],
        lstPtsConcrSect=[tr_bl,tr_tl,tr_tr,tr_br],
        lstCover=[coverLat,cover,coverLat],
        coverSide='r',
        vectorLRef=Vector(-0.15,0.35),
        fromToExtPts=[ln_tl+Vector(topTrnsRb['distRFstart'],0),ln_tr-Vector(topTrnsRb['distRFend'],0)],
        sectBarsSide='r',
        gapStart=-factGap*genConf.cover,
        gapEnd=-factGap*genConf.cover,
         )
    tr_top_rf.createLstRebar()
    tr_top_rf.drawSectBars()
    tr_top_rf.drawLstRebar()
    ln_bot_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=botLnRb['id'],
        diameter=botLnRb['fi'],
        spacing=botLnRb['s'],
        lstPtsConcrSect=[ln_tl,ln_bl,ln_br,ln_tr],
        coverSide='l',
        lstCover=[coverLat,genConf.cover+botTrnsRb['fi'],coverLat],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[tr_bl+Vector(botLnRb['distRFstart'],0),tr_br-Vector(botLnRb['distRFend'],0)],
        coverSectBars=genConf.cover+botTrnsRb['fi'],
        sectBarsSide='l',
        gapStart=-factGap*genConf.cover,
        gapEnd=-factGap*genConf.cover,
        )
    ln_bot_rf.createLstRebar()
    ln_bot_rf.drawSectBars()
    ln_bot_rf.drawLstRebar()
    ln_top_rf=rb.rebarFamily(
        genConf=genConf,
        identifier=topLnRb['id'],
        diameter=topLnRb['fi'],
        spacing=topLnRb['s'],
        lstPtsConcrSect=[ln_bl,ln_tl,ln_tr,ln_br],
        coverSide='r',
        lstCover=[coverLat,genConf.cover+topTrnsRb['fi'],coverLat],
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[tr_tl+Vector(topLnRb['distRFstart'],0),tr_tr-Vector(topLnRb['distRFend'],0)],
        coverSectBars=genConf.cover+topTrnsRb['fi'],
        sectBarsSide='r',
        gapStart=-factGap*genConf.cover,
        gapEnd=-factGap*genConf.cover,
         )
    ln_top_rf.createLstRebar()
    ln_top_rf.drawSectBars()
    ln_top_rf.drawLstRebar()
    # Concrete transverse cross-section
    if drawConcrTrSect:
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    if drawConcrLnSect:
        s=Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    FreeCAD.ActiveDocument.recompute()
    return [tr_bot_rf,tr_top_rf,ln_bot_rf,ln_top_rf]
    

def wall(height,length,thickness,leftVertRb,rightVertRb,leftHorRb,rightHorRb,anchPtVertSect,anchPtHorSect,genConf,drawConcrVertSect=True,drawConcrHorSect=True):
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
    :param drawConcrVertSect: 'Y' to draw the vertical concrete cross-section  (defaults to 'Y')
    :param drawConcrHorSect: 'Y' to draw the horizontal concrete cross-section  (defaults to 'Y')
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
        )
    vert_left_rf.createLstRebar()
    vert_left_rf.drawSectBars()
    vert_left_rf.drawLstRebar()
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
        )
    vert_right_rf.createLstRebar()
    vert_right_rf.drawSectBars()
    vert_right_rf.drawLstRebar()
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
        )
    hor_left_rf.createLstRebar()
    hor_left_rf.drawSectBars()
    hor_left_rf.drawLstRebar()
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
        )
    hor_right_rf.createLstRebar()
    hor_right_rf.drawSectBars()
    hor_right_rf.drawLstRebar()
    # Concrete vertical cross-section
    if drawConcrVertSect:
        s=Part.makePolygon([vert_bl,vert_tl,vert_tr,vert_br,vert_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    if drawConcrHorSect:
        s=Part.makePolygon([hor_bl,hor_tl,hor_tr,hor_br,hor_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    FreeCAD.ActiveDocument.recompute()
    return [vert_left_rf,vert_right_rf,hor_left_rf,hor_right_rf]
    
def set_FR_options(RF,RFdef):
    '''Set the attributes of a rebar family
    '''
    if 'gapStart' in RFdef.keys(): RF.gapStart=RFdef['gapStart']
    if 'gapEnd' in RFdef.keys(): RF.gapEnd=RFdef['gapEnd']
    if 'extrShapeStart' in RFdef.keys(): RF.extrShapeStart=RFdef['extrShapeStart']
    if 'extrShapeEnd' in RFdef.keys(): RF.extrShapeEnd=RFdef['extrShapeEnd']
    if 'fixLengthStart' in RFdef.keys(): RF.fixLengthStart=RFdef['fixLengthStart']
    if 'fixLengthEnd' in RFdef.keys(): RF.fixLengthEnd=RFdef['fixLengthEnd']
    if 'vectorLRef' in RFdef.keys(): RF.vectorLRef=RFdef['vectorLRef']
           
def generic_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,genConf,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,stirrHoldTrReinf=None,stirrHoldLnReinf=None,drawConcrTrSect=True,drawConcrLnSect=True):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

    :param width: dimension of the brick in the direction of the transverse rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param genConf: instance of the reinf_bars.genericConf class
    :param angTrns: angle (degrees) between the horizontal and the brick width dimension
    :param angLn: angle (degrees) between the horizontal and the brick length dimension
    :param botTrnsRb: data for bottom transverse rebar family expressed as a dictionary of type 
           {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1,'position':'good'}, 
           where 'id' is the identificacion of the rebar family, 
                  'fi' is the diameter of the rebar, 
                   's' is the spacement, 
                   'distRFstart' is the distance from the first rebar of the family to the left extremity of the brick (as it is drawn in the section),   
                   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the brick (as it is drawn in the section)
                   'position' is the position of the rebars 'good' or 'poor' (used to calculate the 
                              slap length when splitting rebars
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param stirrHoldTrReinf: data for stirrup rebar family that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
The data of the family is given as a dictionary of type:
            {'id': ,'fi': ,'sRealSh': ,'sPerp': ,'nStirrRealSh': , 'nStirrPerp': ,'widthStirr': , 'dispRealSh': , 'dispPerp': }
            where 'id' is the identificacion of the stirrup family, 
                  'fi' is the diameter of the stirrup, 
                  'sRealSh' is the spacement between stirrups represented as real shape,
                  'sPerp'  is the spacement between stirrups in the orthogonal direction,
                  'widthStirr' is the width of the stirrup (internal),
                  'nStirrRealSh' is the number of stirrups in real shape
                  'nStirrPerp' is the number of stirrups in orthogonal direction
                  'dispRealSh' is the displacement of the stirrup family from the left extremity of the section (represented in real shape). If dispRealSh<0 the stirrups are drawn from right to end extremities of the slab
                  'dispPerp' is the displacement of the stirrup family from the left extremity of the section (in the orthogonal direction). If dispPerp<0 the stirrups are drawn from right to end extremities of the slab
    :param stirrHoldLnReinf: data for stirrup rebar family that holds longitudinal top and bottom rebar families
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    '''
    vdirTr=Vector(math.cos(math.radians(angTrns)),math.sin(math.radians(angTrns)))
    vdirLn=Vector(math.cos(math.radians(angLn)),math.sin(math.radians(angLn)))
    vdirTrPerp=Vector(-1*vdirTr.y,vdirTr.x)
    vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
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
    lstRebFam=list()
    lstStirrFam=list()
    # transverse bottom rebar family
    if botTrnsRb:
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
            gapStart=0,
            gapEnd=0,
            position=botTrnsRb['position'],
            )
        set_FR_options(RF=tr_bot_rf,RFdef=botTrnsRb)
        tr_bot_rf.createLstRebar()
        tr_bot_rf.drawSectBars()
        tr_bot_rf.drawLstRebar()
        lstRebFam+=[tr_bot_rf]
    # transverse bottom rebar family
    if topTrnsRb:
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
            gapStart=0,
            gapEnd=0,
            position=topTrnsRb['position'],
            )
        set_FR_options(RF=tr_top_rf,RFdef=topTrnsRb)    
        tr_top_rf.createLstRebar()
        tr_top_rf.drawSectBars()
        tr_top_rf.drawLstRebar()
        lstRebFam+=[tr_top_rf]
    if botLnRb:
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
            gapStart=0,
            gapEnd=0,
            position=botLnRb['position'],
           )
        set_FR_options(RF=ln_bot_rf,RFdef=botLnRb)
        ln_bot_rf.createLstRebar()
        ln_bot_rf.drawSectBars()
        ln_bot_rf.drawLstRebar()
        lstRebFam+=[ln_bot_rf]
    if topLnRb:
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
            gapStart=0,
            gapEnd=0,
            position=topLnRb['position'],
            )
        set_FR_options(RF=ln_top_rf,RFdef=topLnRb)
        ln_top_rf.createLstRebar()
        ln_top_rf.drawSectBars()
        ln_top_rf.drawLstRebar()
        lstRebFam+=[ln_top_rf]
    # Stirrups holding the transverse top and bottom rebar families
    if stirrHoldTrReinf:
        stDic=stirrHoldTrReinf
        bStirr=stDic['widthStirr']+stDic['fi']
        coverStirr=genConf.cover-stDic['fi']
        if dispStrpTransv<0: # stirrups rigth towards left
            lstPtsConcrTransv=[ln_br,ln_br-bStirr*vdirLn,ln_tr-bStirr*vdirLn,ln_tr]
        else: # stirrups left towards right
            lstPtsConcrTransv=[ln_bl,ln_bl+bStirr*vdirLn,ln_tl+bStirr*vdirLn,ln_tl]
        if dispStrpLong<0: # stirrups rigth towards left
            lstPtsConcrLong=[tr_tr,tr_br]
        else:
            lstPtsConcrLong=[tr_tl,tr_bl]
        hold_tr_sf=rb.stirrupFamily(
            genConf=genConf,
            identifier=stDic['id'],
            diameter=stDic['fi'],
            lstPtsConcrTransv=lstPtsConcrTransv,
            lstCover=[coverStirr,0,coverStirr,0],
            lstPtsConcrLong=lstPtsConcrLong,
            spacStrpTransv=abs(stDic['sRealSh']),
            spacStrpLong=stDic['sPerp'],
            vDirLong=vdirTr,
            nmbStrpTransv=stDic['nStirrRealSh'],
            nmbStrpLong=stDic['nStirrPerp'],
            dispStrpTransv=stDic['dispRealSh'],
            dispStrpLong=stDic['dispPerp'],
            vectorLRef=stDic['vectorLref'],
            sideLabelLn=stDic['sideLabelLn'],
            )
        hold_tr_sf.drawRebars()
        hold_tr_sf.drawLnRebars()
        lstStirrFam+=[hold_tr_sf]
    # Stirrups holding the longitudinal top and bottom rebar families
    if stirrHoldLnReinf:
        if dispStrpTransv<0: # stirrups rigth towards left
            lstPtsConcrTransv=[tr_br,tr_br-bStirr*vdirTr,tr_tr-bStirr*vdirTr,tr_tr]
        else: # stirrups left towards right
            lstPtsConcrTransv=[tr_bl,tr_bl+bStirr*vdirTr,tr_tl+bStirr*vdirTr,tr_tl]
        if dispStrpLong<0: # stirrups rigth towards left
            lstPtsConcrLong=[ln_tr,ln_br]
        else:
            lstPtsConcrLong=[ln_tl,ln_bl]
        
        stDic=stirrHoldLnReinf
        bStirr=stDic['widthStirr']+stDic['fi']
        coverStirr=genConf.cover+min(topTrnsRb['fi'],botTrnsRb['fi'])-stDic['fi']
        hold_ln_sf=rb.stirrupFamily(
            genConf=genConf,
            identifier=stDic['id'],
            diameter=stDic['fi'],
            lstPtsConcrTransv=lstPtsConcrTransv,
            lstCover=[coverStirr,0,coverStirr,0],
            lstPtsConcrLong=lstPtsConcrLong,
            spacStrpTransv=stDicabs(['sRealSh']),
            spacStrpLong=stDic['sPerp'],
            vDirLong=vdirLn,
            nmbStrpTransv=stDic['nStirrRealSh'],
            nmbStrpLong=stDic['nStirrPerp'],
            dispStrpTransv=stDic['dispRealSh'],
            dispStrpLong=stDic['dispPerp'],
            vectorLRef=stDic['vectorLref'],
            sideLabelLn=stDic['sideLabelLn'],
            )
        hold_ln_sf.drawRebars()
        hold_ln_sf.drawLnRebars()
        lstStirrFam+=[hold_ln_sf]
    
    # Concrete transverse cross-section
    if drawConcrTrSect:
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    if drawConcrLnSect:
        s=Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam
