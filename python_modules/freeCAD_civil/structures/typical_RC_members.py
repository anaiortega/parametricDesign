# -*- coding: iso-8859-1 -*-

import math
import Part, FreeCAD
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
import FreeCADGui

colorConcrete=(0.00,1.00,1.00) #cyan

class genericBrickReinf(object):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

    :param width: dimension of the brick in the direction of the transverse rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param reinfCfg: instance of the cfg.reinfConf class
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
    :param lstStirrHoldTrReinf: list of stirrHoldTrReinfs . Each one is the data for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
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
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs. Each onr iss the data for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :param slopeBottFace: transverse slope of the brick bottom-face (deltaY/deltaX)
    :param slopeTopFace: transverse slope of the brick top-face (deltaY/deltaX)
    '''

    def __init__(self,width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,slopeBottFace=None,slopeTopFace=None,drawConcrTrSect=True,drawConcrLnSect=True):
        self.width=width
        self.length=length
        self.thickness=thickness
        self.anchPtTrnsSect=anchPtTrnsSect
        self.anchPtLnSect=anchPtLnSect
        self.reinfCfg=reinfCfg
        self.angTrns=angTrns
        self.angLn=angLn
        self.botTrnsRb=botTrnsRb
        self.topTrnsRb=topTrnsRb
        self.botLnRb=botLnRb
        self.topLnRb=topLnRb
        self.lstStirrHoldTrReinf=lstStirrHoldTrReinf
        self.lstStirrHoldLnReinf=lstStirrHoldLnReinf
        self.slopeBottFace=slopeBottFace
        self.slopeTopFace=slopeTopFace

    def getVdirTransv(self):
        vdirTr=Vector(math.cos(math.radians(self.angTrns)),math.sin(math.radians(self.angTrns)))
        return vdirTr
    
    def getVdirLong(self):
        vdirLn=Vector(math.cos(math.radians(self.angLn)),math.sin(math.radians(self.angLn)))
        return vdirLn

    def getMeanThickness(self):
        meanThickness=self.thickness
        if self.slopeBottFace: meanThickness+=-self.width*self.slopeBottFace/2
        if self.slopeTopFace: meanThickness+=self.width*self.slopeTopFace/2
        return meanThickness
        
    def getTransvBottPnts(self):
        ''' return the left and right bottom points of the trasverse concrete section'''
        vdirTr=self.getVdirTransv(); vdirTrPerp=Vector(-1*vdirTr.y,vdirTr.x)
        tr_bl=self.anchPtTrnsSect
        tr_br= tr_bl+self.width*vdirTr
        if self.slopeBottFace:
            tr_br=tr_br+self.width*self.slopeBottFace*vdirTrPerp
        return tr_bl,tr_br

    def getTransvTopPnts(self):
        ''' return the left and right top points of the trasverse concrete section'''
        vdirTr=self.getVdirTransv(); vdirTrPerp=Vector(-1*vdirTr.y,vdirTr.x)
        tr_tl=self.anchPtTrnsSect+self.thickness*vdirTrPerp
        tr_tr=tr_tl+self.width*vdirTr
        if self.slopeTopFace:
            tr_tr=tr_tr+self.width*self.slopeTopFace*vdirTrPerp
        return tr_tl,tr_tr
 
    def getLongBottPnts(self):
        ''' return the left and right bottom points of the longtudinal concrete section'''
        ln_bl=self.anchPtLnSect
        ln_br= ln_bl+self.length*self.getVdirLong()
        return ln_bl,ln_br

    
    def getLongTopPnts(self):
        ''' return the left and right bottom points of the longtudinal concrete section'''
        vdirLn=self.getVdirLong()
        ln_tl=self.anchPtLnSect+self.getMeanThickness()*Vector(-vdirLn.y,vdirLn.x)
        ln_tr=ln_tl+self.length*vdirLn
        return ln_tl,ln_tr
      
    def drawBottomTransvRF(self):
        ''' Draw and return the bottom transverse rebar family '''
        tr_bl,tr_br=self.getTransvBottPnts()
        ln_bl,ln_br=self.getLongBottPnts()
        vdirLn=self.getVdirLong()
        tr_bot_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.botTrnsRb['id'],
            diameter=self.botTrnsRb['fi'],
            spacing=self.botTrnsRb['s'],
            lstPtsConcrSect=[tr_bl,tr_br],
            rightSideCover=False,
            fromToExtPts=[ln_bl+self.botTrnsRb['distRFstart']*vdirLn,ln_br-self.botTrnsRb['distRFend']*vdirLn],
            rightSideSectBars=False,
            gapStart=0,
            gapEnd=0,
            position=self.botTrnsRb['position'],
            )
        set_FR_options(RF=tr_bot_rf,RFdef=self.botTrnsRb)
        tr_bot_rf.createLstRebar()
        tr_bot_rf.drawPolySectBars()
        tr_bot_rf.drawLstRebar()
        return tr_bot_rf

    def drawTopTransvRF(self):
        '''draw and return  the transverse top rebar family'''
        tr_tl,tr_tr=self.getTransvTopPnts()
        ln_tl,ln_tr=self.getLongTopPnts()
        vdirLn=self.getVdirLong()
        tr_top_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.topTrnsRb['id'],
            diameter=self.topTrnsRb['fi'],
            spacing=self.topTrnsRb['s'],
            lstPtsConcrSect=[tr_tl,tr_tr],
            rightSideCover=True,
            fromToExtPts=[ln_tl+self.topTrnsRb['distRFstart']*vdirLn,ln_tr-self.topTrnsRb['distRFend']*vdirLn],
            rightSideSectBars=True,
            gapStart=0,
            gapEnd=0,
            position=self.topTrnsRb['position'],
            )
        set_FR_options(RF=tr_top_rf,RFdef=self.topTrnsRb)    
        tr_top_rf.createLstRebar()
        tr_top_rf.drawPolySectBars()
        tr_top_rf.drawLstRebar()
        return tr_top_rf
        
    def drawBottomLongRF(self):
        '''draw and return the  longitudinal bottom rebar family'''
        ln_bl,ln_br=self.getLongBottPnts()
        tr_bl,tr_br=self.getTransvBottPnts()
        vdirTrBott=(tr_br-tr_bl).normalize()
        ln_bot_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.botLnRb['id'],
            diameter=self.botLnRb['fi'],
            spacing=self.botLnRb['s'],
            lstPtsConcrSect=[ln_bl,ln_br],
            rightSideCover=False,
            lstCover=[self.reinfCfg.cover+self.botTrnsRb['fi']],
            fromToExtPts=[tr_bl+self.botLnRb['distRFstart']*vdirTrBott,tr_br-self.botLnRb['distRFend']*vdirTrBott],
            coverSectBars=self.reinfCfg.cover+self.botTrnsRb['fi'],
            rightSideSectBars=False,
            gapStart=0,
            gapEnd=0,
            position=self.botLnRb['position'],
           )
        set_FR_options(RF=ln_bot_rf,RFdef=self.botLnRb)
        ln_bot_rf.createLstRebar()
        ln_bot_rf.drawPolySectBars()
        ln_bot_rf.drawLstRebar()
        return ln_bot_rf
    
    def drawTopLongRF(self):
        ''' draw and return the  longitudinal top rebar family'''
        ln_tl,ln_tr=self.getLongTopPnts()
        tr_tl,tr_tr=self.getTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        ln_top_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.topLnRb['id'],
            diameter=self.topLnRb['fi'],
            spacing=self.topLnRb['s'],
            lstPtsConcrSect=[ln_tl,ln_tr],
            rightSideCover=True,
            lstCover=[self.reinfCfg.cover+self.topTrnsRb['fi']],
            fromToExtPts=[tr_tl+self.topLnRb['distRFstart']*vdirTrTop,tr_tr-self.topLnRb['distRFend']*vdirTrTop],
            coverSectBars=self.reinfCfg.cover+self.topTrnsRb['fi'],
            rightSideSectBars=True,
            gapStart=0,
            gapEnd=0,
            position=self.topLnRb['position'],
            )
        set_FR_options(RF=ln_top_rf,RFdef=self.topLnRb)
        ln_top_rf.createLstRebar()
        ln_top_rf.drawPolySectBars()
        ln_top_rf.drawLstRebar()
        return ln_top_rf

    def drawStirrHoldingTransvSF(self):
        ''' Draw and retrurn the stirrup family that  holds the transverse top and bottom rebar families '''
        ln_bl,ln_br=self.getLongBottPnts()
        ln_tl,ln_tr=self.getLongTopPnts()
        tr_tl,tr_tr=self.getTransvTopPnts()
        tr_bl,tr_br=self.getTransvBottPnts()
        vdirTr=self.getVdirTransv()
        vdirLn=self.getVdirLong()
        for stirrHoldTrReinf in self.lstStirrHoldTrReinf:
            stDic=stirrHoldTrReinf
            bStirr=stDic['widthStirr']+stDic['fi']
            coverStirr=self.reinfCfg.cover-stDic['fi']
            if stDic['dispRealSh']<0: # stirrups rigth towards left
                lstPtsConcrSect=[ln_br,ln_br-bStirr*vdirLn,ln_tr-bStirr*vdirLn,ln_tr,ln_br]
            else: # stirrups left towards right
                lstPtsConcrSect=[ln_bl,ln_bl+bStirr*vdirLn,ln_tl+bStirr*vdirLn,ln_tl,ln_bl]
            if stDic['dispPerp']<0: # stirrups rigth towards left
                lstPtsConcrLong=[tr_tr,tr_br]
                vDirLong=-1*vdirTr
            else:
                lstPtsConcrLong=[tr_tl,tr_bl]
                vDirLong=vdirTr
            hold_tr_sf=rb.stirrupFamily(
                reinfCfg=self.reinfCfg,
                identifier=stDic['id'],
                diameter=stDic['fi'],
                lstPtsConcrSect=lstPtsConcrSect,
                lstCover=[coverStirr,0,coverStirr,0],
                lstPtsConcrLong=lstPtsConcrLong,
                spacStrpTransv=abs(stDic['sRealSh']),
                spacStrpLong=stDic['sPerp'],
                vDirLong=vDirLong,
                nmbStrpTransv=stDic['nStirrRealSh'],
                nmbStrpLong=stDic['nStirrPerp'],
                dispStrpTransv=abs(stDic['dispRealSh']),
                dispStrpLong=abs(stDic['dispPerp']),
                vectorLRef=stDic['vectorLRef'],
                rightSideLabelLn=stDic['rightSideLabelLn'],
                )
            if 'rightSideCover' in stDic.keys():
                hold_tr_sf.rightSideCover=stDic['rightSideCover']
            hold_tr_sf.drawPolyRebars()
            hold_tr_sf.drawLnRebars()
            return hold_tr_sf
        
    def drawStirrHoldingLongSFf(self):
        ''' Draw and return the stirrup family  that holds the longitudinal top and bottom rebar families'''
        ln_bl,ln_br=self.getLongBottPnts()
        ln_tl,ln_tr=self.getLongTopPnts()
        tr_tl,tr_tr=self.getTransvTopPnts()
        tr_bl,tr_br=self.getTransvBottPnts()
        vdirTr=self.getVdirTransv()
        vdirLn=self.getVdirLong()
        for stirrHoldLnReinf in self.lstStirrHoldLnReinf:
            stDic=stirrHoldLnReinf
            bStirr=stDic['widthStirr']+stDic['fi']
            coverStirr=self.reinfCfg.cover-stDic['fi']
            if stDic['dispRealSh']<0: # stirrups rigth towards left
                lstPtsConcrSect=[tr_br,tr_br-bStirr*vdirTr,tr_tr-bStirr*vdirTr,tr_tr,tr_br]
            else: # stirrups left towards right
                lstPtsConcrSect=[tr_bl,tr_bl+bStirr*vdirTr,tr_tl+bStirr*vdirTr,tr_tl,tr_bl]
            if stDic['dispPerp']<0: # stirrups rigth towards left
                lstPtsConcrLong=[ln_tr,ln_br]
                vDirLong=-1*vdirLn
            else:
                lstPtsConcrLong=[ln_tl,ln_bl]
                vDirLong=vdirLn
#            stDic=stirrHoldLnReinf
            bStirr=stDic['widthStirr']+stDic['fi']
            coverStirr=self.reinfCfg.cover+min(self.topTrnsRb['fi'],self.botTrnsRb['fi'])-stDic['fi']
            hold_ln_sf=rb.stirrupFamily(
                reinfCfg=self.reinfCfg,
                identifier=stDic['id'],
                diameter=stDic['fi'],
                lstPtsConcrSect=lstPtsConcrSect,
                lstCover=[coverStirr,0,coverStirr,0],
                lstPtsConcrLong=lstPtsConcrLong,
                spacStrpTransv=abs(stDic['sRealSh']),
                spacStrpLong=stDic['sPerp'],
                vDirLong=vDirLong,
                nmbStrpTransv=stDic['nStirrRealSh'],
                nmbStrpLong=stDic['nStirrPerp'],
                dispStrpTransv=abs(stDic['dispRealSh']),
                dispStrpLong=abs(stDic['dispPerp']),
                vectorLRef=stDic['vectorLRef'],
                rightSideLabelLn=stDic['rightSideLabelLn'],
                )
            if 'rightSideCover' in stDic.keys():
                hold_ln_sf.rightSideCover=stDic['rightSideCover']
            hold_ln_sf.drawPolyRebars()
            hold_ln_sf.drawLnRebars()
            return hold_ln_sf

    def drawOpenTransvConcrSect(self):
        ''' Draw concrete transverse cross-section'''
        tr_tl,tr_tr=self.getTransvTopPnts()
        tr_bl,tr_br=self.getTransvBottPnts()
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete

    def drawOpenLongConcrSect(self):
        ''' Draw concrete longitudinal cross-section'''
        ln_bl,ln_br=self.getLongBottPnts()
        ln_tl,ln_tr=self.getLongTopPnts()
        s=Part.makePolygon([ln_bl,ln_tl,ln_tr,ln_br,ln_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete



def constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,drawConcrTrSect=True,drawConcrLnSect=True):
    '''Typical reinforcement arrangement of a brick of constant thickness
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

    :param width: dimension of the brick in the direction of the transverse rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param reinfCfg: instance of the cfg.reinfConf class
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
    :param lstStirrHoldTrReinf: list of stirrHoldTrReinfs . Each one is the data for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
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
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs. Each onr iss the data for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,lstStirrHoldTrReinf=lstStirrHoldTrReinf,lstStirrHoldLnReinf=lstStirrHoldLnReinf)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
    if lstStirrHoldTrReinf:
        lstStirrFam+=[brick.drawStirrHoldingTransvSF()]
    if lstStirrHoldLnReinf:
        lstStirrFam+=[brick.drawStirrHoldingLongSFf()]
    if drawConcrTrSect:
        brick.drawOpenTransvConcrSect()
    if drawConcrLnSect:
        brick.drawOpenLongConcrSect()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam

def sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,slopeBottFace=None,slopeTopFace=None,drawConcrTrSect=True,drawConcrLnSect=True):
    '''Typical reinforcement arrangement of a brick of constant thickness
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

    :param width: dimension of the brick in the direction of the transverse rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param reinfCfg: instance of the cfg.reinfConf class
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
    :param lstStirrHoldTrReinf: list of stirrHoldTrReinfs . Each one is the data for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
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
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs. Each onr iss the data for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :param slopeBottFace: transverse slope of the brick bottom-face (deltaY/deltaX)
    :param slopeTopFace: transverse slope of the brick top-face (deltaY/deltaX)
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,slopeBottFace=slopeBottFace,slopeTopFace=slopeTopFace,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
    if drawConcrTrSect:
        brick.drawOpenTransvConcrSect()
    if drawConcrLnSect:
        brick.drawOpenLongConcrSect()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam
    

def closed_slab(width,length,thickness,botTrnsRb,topTrnsRb,botLnRb,topLnRb,anchPtTrnsSect,anchPtLnSect,reinfCfg,drawConcrTrSect=True,drawConcrLnSect=True,factGap=1,coverLat=None):
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
    :param reinfCfg: instance of the reinfConf class
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    :param factGap: the gapSart and gapEnd are made equal to factGap*cover
    :param coverLat: lateral cover (if None, reinfCfg.cover is used)
    '''
    cover=reinfCfg.cover
    if not coverLat:
        coverLat=reinfCfg.cover
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
        reinfCfg=reinfCfg,
        identifier=botTrnsRb['id'],
        diameter=botTrnsRb['fi'],
        spacing=botTrnsRb['s'],
        lstPtsConcrSect=[tr_tl,tr_bl,tr_br,tr_tr],
        lstCover=[coverLat,cover,coverLat],
        rightSideCover=False,
        vectorLRef=Vector(-0.15,-0.35),
        fromToExtPts=[ln_bl+Vector(botTrnsRb['distRFstart'],0),ln_br-Vector(botTrnsRb['distRFend'],0)],
        rightSideSectBars=False,
        gapStart=-factGap*reinfCfg.cover,
        gapEnd=-factGap*reinfCfg.cover,
        )
    set_FR_options(RF=tr_bot_rf,RFdef=botTrnsRb)
    tr_bot_rf.createLstRebar()
    tr_bot_rf.drawPolySectBars()
    tr_bot_rf.drawLstRebar()
    
    # transverse bottom rebar family
    tr_top_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=topTrnsRb['id'],
        diameter=topTrnsRb['fi'],
        spacing=topTrnsRb['s'],
        lstPtsConcrSect=[tr_bl,tr_tl,tr_tr,tr_br],
        lstCover=[coverLat,cover,coverLat],
        rightSideCover=True,
        vectorLRef=Vector(-0.15,0.35),
        fromToExtPts=[ln_tl+Vector(topTrnsRb['distRFstart'],0),ln_tr-Vector(topTrnsRb['distRFend'],0)],
        rightSideSectBars=True,
        gapStart=-factGap*reinfCfg.cover,
        gapEnd=-factGap*reinfCfg.cover,
         )
    set_FR_options(RF=tr_top_rf,RFdef=topTrnsRb)
    tr_top_rf.createLstRebar()
    tr_top_rf.drawPolySectBars()
    tr_top_rf.drawLstRebar()
    ln_bot_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=botLnRb['id'],
        diameter=botLnRb['fi'],
        spacing=botLnRb['s'],
        lstPtsConcrSect=[ln_tl,ln_bl,ln_br,ln_tr],
        rightSideCover=False,
        lstCover=[coverLat,reinfCfg.cover+botTrnsRb['fi'],coverLat],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[tr_bl+Vector(botLnRb['distRFstart'],0),tr_br-Vector(botLnRb['distRFend'],0)],
        coverSectBars=reinfCfg.cover+botTrnsRb['fi'],
        rightSideSectBars=False,
        gapStart=-factGap*reinfCfg.cover,
        gapEnd=-factGap*reinfCfg.cover,
        )
    set_FR_options(RF=ln_bot_rf,RFdef=botLnRb)
    ln_bot_rf.createLstRebar()
    ln_bot_rf.drawPolySectBars()
    ln_bot_rf.drawLstRebar()
    ln_top_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=topLnRb['id'],
        diameter=topLnRb['fi'],
        spacing=topLnRb['s'],
        lstPtsConcrSect=[ln_bl,ln_tl,ln_tr,ln_br],
        rightSideCover=True,
        lstCover=[coverLat,reinfCfg.cover+topTrnsRb['fi'],coverLat],
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[tr_tl+Vector(topLnRb['distRFstart'],0),tr_tr-Vector(topLnRb['distRFend'],0)],
        coverSectBars=reinfCfg.cover+topTrnsRb['fi'],
        rightSideSectBars=True,
        gapStart=-factGap*reinfCfg.cover,
        gapEnd=-factGap*reinfCfg.cover,
         )
    set_FR_options(RF=ln_top_rf,RFdef=topLnRb)
    ln_top_rf.createLstRebar()
    ln_top_rf.drawPolySectBars()
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
    

def wall(height,length,thickness,leftVertRb,rightVertRb,leftHorRb,rightHorRb,anchPtVertSect,anchPtHorSect,reinfCfg,drawConcrVertSect=True,drawConcrHorSect=True):
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
    :param reinfCfg: instance of the reinfConf class
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
        reinfCfg=reinfCfg,
        identifier=leftVertRb['id'],
        diameter=leftVertRb['fi'],
        spacing=leftVertRb['s'],
        lstPtsConcrSect=[vert_bl,vert_tl,vert_tr],
        rightSideCover=True,
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[hor_bl+Vector(0,leftVertRb['distRFstart']),hor_tl-Vector(0,leftVertRb['distRFend'])],
        rightSideSectBars=True,
        )
    set_FR_options(RF=vert_left_rf,RFdef=leftVertRb)
    vert_left_rf.createLstRebar()
    vert_left_rf.drawPolySectBars()
    vert_left_rf.drawLstRebar()
    # vertical left rebar family
    vert_right_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=rightVertRb['id'],
        diameter=rightVertRb['fi'],
        spacing=rightVertRb['s'],
        lstPtsConcrSect=[vert_br,vert_tr,vert_tl],
        rightSideCover=False,
        vectorLRef=Vector(-0.3,0.4),
        fromToExtPts=[hor_br+Vector(0,rightVertRb['distRFstart']),hor_tr-Vector(0,rightVertRb['distRFend'])],
        rightSideSectBars=False,
        )
    set_FR_options(RF=vert_right_rf,RFdef=rightVertRb)
    vert_right_rf.createLstRebar()
    vert_right_rf.drawPolySectBars()
    vert_right_rf.drawLstRebar()
    hor_left_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=leftHorRb['id'],
        diameter=leftHorRb['fi'],
        spacing=leftHorRb['s'],
        lstPtsConcrSect=[hor_br,hor_bl,hor_tl,hor_tr],
        rightSideCover=True,
        lstCover=[reinfCfg.cover,reinfCfg.cover+leftVertRb['fi'],reinfCfg.cover],
        vectorLRef=Vector(-0.3,-0.4),
        fromToExtPts=[vert_bl+Vector(0,leftHorRb['distRFstart']),vert_tl-Vector(0,leftHorRb['distRFend'])],
        coverSectBars=reinfCfg.cover+leftVertRb['fi'],
        rightSideSectBars=True,
        )
    set_FR_options(RF=hor_left_rf,RFdef=leftHorRb)
    hor_left_rf.createLstRebar()
    hor_left_rf.drawPolySectBars()
    hor_left_rf.drawLstRebar()
    hor_right_rf=rb.rebarFamily(
        reinfCfg=reinfCfg,
        identifier=rightHorRb['id'],
        diameter=rightHorRb['fi'],
        spacing=rightHorRb['s'],
        lstPtsConcrSect=[hor_bl,hor_br,hor_tr,hor_tl],
        rightSideCover=False,
        lstCover=[reinfCfg.cover,reinfCfg.cover+rightVertRb['fi'],reinfCfg.cover],
        vectorLRef=Vector(0.3,0.4),
        fromToExtPts=[vert_br+Vector(0,rightHorRb['distRFstart']),vert_tr-Vector(0,rightHorRb['distRFend'])],
        coverSectBars=reinfCfg.cover+rightVertRb['fi'],
        rightSideSectBars=False,
        )
    set_FR_options(RF=hor_right_rf,RFdef=rightHorRb)
    hor_right_rf.createLstRebar()
    hor_right_rf.drawPolySectBars()
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
           
