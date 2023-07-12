# -*- coding: iso-8859-1 -*-

import math
import Part, FreeCAD
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
import FreeCADGui
from misc_utils import log_messages as lmsg

colorConcrete=(0.00,1.00,1.00) #cyan

class genericBrickReinf(object):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family
                  X-coordinata: transverse direction
                  Y-coordinate: longitudinal direction.

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
           optionally can be defined: {'gapStart','gapEnd','extrShapeStart','extrShapeEnd', 'fixLengthStart','fixLengthEnd','vectorLRef',
                                                  'closedStart','closedEnd'}
           where 'id' is the identificacion of the rebar family, 
                  'fi' is the diameter of the rebar, 
                   's' is the spacement, 
                   'distRFstart' is the distance from the first rebar of the family to the left extremity of the brick (as it is drawn in the section)
                                     if not defined, default is 0   
                   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the brick (as it is drawn in the section)
                                   if not defined, default is 0   
                                   (ignored in transverse rebars when sloped edge is defined)
                   'position' is the position of the rebars 'good' or 'poor' (used to calculate the 
                              slap length when splitting rebars)
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
    :param trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :param trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :ivar slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    '''

    def __init__(self,width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,trSlopeBottFace=None,trSlopeTopFace=None,slopeEdge=None,drawConcrTrSect=True,drawConcrLnSect=True):
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
        self.trSlopeBottFace=trSlopeBottFace
        self.trSlopeTopFace=trSlopeTopFace
        self.slopeEdge=slopeEdge

    def getVdirTransv(self):
        vdirTr=Vector(math.cos(math.radians(self.angTrns)),math.sin(math.radians(self.angTrns)))
        return vdirTr
    
    def getVdirLong(self):
        vdirLn=Vector(math.cos(math.radians(self.angLn)),math.sin(math.radians(self.angLn)))
        return vdirLn

    def getMeanThickness(self):
        '''Return the maan thickness of the brick at X axis, which occurs at the 
        longitudinal section placed at (minX+maxX)/2 coordinate.
        '''
        meanThickness=self.thickness
        if self.trSlopeBottFace: meanThickness+=-self.width*self.trSlopeBottFace/2
        if self.trSlopeTopFace: meanThickness+=self.width*self.trSlopeTopFace/2
        return meanThickness
        
    def getMaxXThickness(self):
        '''Return the thickness of the brick at X axis  at maximum X coordinate'''
        maxXThickness=self.thickness
        if self.trSlopeBottFace: maxXThickness+=-self.width*self.trSlopeBottFace
        if self.trSlopeTopFace: maxXThickness+=self.width*self.trSlopeTopFace
        return maxXThickness

    def getMaxWidth(self):
        '''Return the maximum width of the brick, which occurs at the 
         transverse  section with maximum Y coordinate'''
        maxWidth=self.width
        if self.slopeEdge:
            maxWidth=self.width+self.length*abs(self.slopeEdge)
        return maxWidth

    def getIncrWidth(self):
        ''' return the width increment due to the edge slope '''
        incrWidth=self.getMaxWidth()-self.width
        return incrWidth

    def getTransvBottPnts(self,width):
        '''return the left and right bottom points of the trasverse concrete section
        as function of the section width'''
        vdirTr=self.getVdirTransv(); vdirTrPerp=Vector(-1*vdirTr.y,vdirTr.x)
        tr_bl=self.anchPtTrnsSect
        tr_br= tr_bl+width*vdirTr
        if self.trSlopeBottFace:
            tr_br=tr_br+width*self.trSlopeBottFace*vdirTrPerp
        return tr_bl,tr_br
    
    def getYminTransvBottPnts(self):
        ''' return the left and right bottom points of the trasverse concrete section
        at minimum Y coordinate '''
        tr_bl,tr_br=self.getTransvBottPnts(self.width)
        return tr_bl,tr_br

    def getYmaxTransvBottPnts(self):
        ''' return the left and right bottom points of the trasverse concrete section
        at maximum Y coordinate '''
        maxWidth=self.getMaxWidth()
        tr_bl,tr_br=self.getTransvBottPnts(maxWidth)
        return tr_bl,tr_br

    def getTransvTopPnts(self,width):
        ''' return the left and right top points of the trasverse concrete section
        as function of the section width '''
        vdirTr=self.getVdirTransv(); vdirTrPerp=Vector(-1*vdirTr.y,vdirTr.x)
        tr_tl=self.anchPtTrnsSect+self.thickness*vdirTrPerp
        tr_tr=tr_tl+width*vdirTr
        if self.trSlopeTopFace:
            tr_tr=tr_tr+width*self.trSlopeTopFace*vdirTrPerp
        return tr_tl,tr_tr
       
    def getYminTransvTopPnts(self):
        ''' return the left and right top points of the trasverse concrete section
        at minimum Y coordinate '''
        tr_tl,tr_tr=self.getTransvTopPnts(self.width)
        return tr_tl,tr_tr

    def getYmaxTransvTopPnts(self):
        ''' return the left and right top points of the trasverse concrete section
        at maximum Y coordinate '''
        maxWidth=self.getMaxWidth()
        tr_tl,tr_tr=self.getTransvTopPnts(maxWidth)
        return tr_tl,tr_tr


    def getLongBottPnts(self,x):
        ''' return the left and right bottom points of the longtudinal concrete 
        section in function of the X coordinate (X in transverse direction)'''
        vdirLn=self.getVdirLong(); vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
        ln_bl=self.anchPtLnSect
        ln_br= ln_bl+self.length*self.getVdirLong()
        if self.trSlopeBottFace:
            leftL=x
            rightL=x+self.getIncrWidth()
            ln_bl=ln_bl+leftL*self.trSlopeBottFace*vdirLnPerp
            ln_br=ln_br+rightL*self.trSlopeBottFace*vdirLnPerp
        return ln_bl,ln_br

    def getXminLongBottPnts(self):
        ''' return the left and right bottom points of the longitudinal concrete section
        at minimum X coordinate '''
        ln_bl,ln_br=self.getLongBottPnts(x=0)
        return ln_bl,ln_br
       
    def getXmaxLongBottPnts(self):
        ''' return the left and right bottom points of the longitudinal concrete section
        at maximum X coordinate '''
        ln_bl,ln_br=self.getLongBottPnts(x=self.width)
        return ln_bl,ln_br
       
    def getLongTopPnts(self,x):
        ''' return the left and right top points of the longtudinal concrete 
        section in function of the X coordinate (X in transverse direction)'''
        vdirLn=self.getVdirLong(); vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
        ln_tl=self.anchPtLnSect+self.thickness*vdirLnPerp
        ln_tr= ln_tl+self.length*self.getVdirLong()
        if self.trSlopeTopFace:
            leftL=x
            rightL=x+self.getIncrWidth()
            ln_tl=ln_tl+leftL*self.trSlopeTopFace*vdirLnPerp
            ln_tr=ln_tr+rightL*self.trSlopeTopFace*vdirLnPerp
        return ln_tl,ln_tr
    
    def getXminLongTopPnts(self):
        ''' return the left and right topom points of the longitudinal concrete section
        at minimum X coordinate '''
        ln_tl,ln_tr=self.getLongTopPnts(x=0)
        return ln_tl,ln_tr
       
    def getXmaxLongTopPnts(self):
        ''' return the left and right topom points of the longitudinal concrete section
        at maximum X coordinate '''
        ln_tl,ln_tr=self.getLongTopPnts(x=self.width)
        return ln_tl,ln_tr

    def getTransitionBottPnt(self):
        ''' return the bottom point in the transverse section at Ymax 
        where the transition between constant and variable transverse
        reinforcement occurs '''
        startP,trns_bot=self.getTransvBottPnts(self.getIncrWidth())
        return trns_bot

    def getTransitionTopPnt(self):
        ''' return the top point in the transverse section at Ymax 
        where the transition between constant and variable transverse
        reinforcement occurs '''
        startP,trns_top=self.getTransvTopPnts(self.getIncrWidth())
        return trns_top

    def drawBottomTransvRF(self):
        ''' Draw and return the bottom transverse rebar family '''
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        vdirLn=self.getVdirLong()
        init_RFdef_vars(self.botTrnsRb)
        check_position(self.botTrnsRb)
        lstPtsConcrSect=[tr_bl,tr_br]
        if self.botTrnsRb['closedStart'] or self.botTrnsRb['closedEnd']: tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        if self.botTrnsRb['closedStart']: lstPtsConcrSect.insert(0,tr_tl)
        if self.botTrnsRb['closedEnd']: lstPtsConcrSect.append(tr_tr)
        tr_bot_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.botTrnsRb['id'],
            diameter=self.botTrnsRb['fi'],
            spacing=self.botTrnsRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
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
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vdirLn=self.getVdirLong()
        init_RFdef_vars(self.topTrnsRb)
        check_position(self.topTrnsRb)
        lstPtsConcrSect=[tr_tl,tr_tr]
        if self.topTrnsRb['closedStart'] or self.topTrnsRb['closedEnd']: tr_bl,tr_br=self.getYmaxTransvBottPnts()
        if self.topTrnsRb['closedStart']: lstPtsConcrSect.insert(0,tr_bl)
        if self.topTrnsRb['closedEnd']: lstPtsConcrSect.append(tr_br)
        tr_top_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.topTrnsRb['id'],
            diameter=self.topTrnsRb['fi'],
            spacing=self.topTrnsRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
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
        '''draw and return the  longitudinal bottom rebar family 
        constant length stretch'''
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        vdirTrBott=(tr_br-tr_bl).normalize()
        init_RFdef_vars(self.botLnRb)
        check_position(self.botLnRb)
        if self.slopeEdge:
            fromExtPt=self.getTransitionBottPnt()
        else:
            fromExtPt=tr_bl+self.botLnRb['distRFstart']*vdirTrBott
        lstPtsConcrSect=[ln_bl,ln_br]
        lstCover=[self.reinfCfg.cover+self.botTrnsRb['fi']]
        if self.botLnRb['closedStart'] or self.botLnRb['closedEnd']: ln_tl,ln_tr=self.getXmaxLongTopPnts()
        if self.botLnRb['closedStart']:
            lstPtsConcrSect.insert(0,ln_tl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.botLnRb['closedEnd']:
            lstPtsConcrSect.append(ln_tr)
            lstCover.append(self.reinfCfg.cover)
        ln_bot_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.botLnRb['id'],
            diameter=self.botLnRb['fi'],
            spacing=self.botLnRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
            rightSideCover=False,
            lstCover=lstCover,
            fromToExtPts=[fromExtPt,tr_br-self.botLnRb['distRFend']*vdirTrBott],
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
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        init_RFdef_vars(self.topLnRb)
        check_position(self.topLnRb)  
        if self.slopeEdge:
            fromExtPt=self.getTransitionTopPnt()
        else:
            fromExtPt= tr_tl+self.topLnRb['distRFstart']*vdirTrTop
        lstPtsConcrSect=[ln_tl,ln_tr]
        lstCover=[self.reinfCfg.cover+self.topTrnsRb['fi']]
        if self.topLnRb['closedStart'] or self.topLnRb['closedEnd']: ln_bl,ln_br=self.getXmaxLongBottPnts()
        if self.topLnRb['closedStart']:
            lstPtsConcrSect.insert(0,ln_bl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.topLnRb['closedEnd']:
            lstPtsConcrSect.append(ln_br)
            lstCover.append(self.reinfCfg.cover)
        ln_top_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.topLnRb['id'],
            diameter=self.topLnRb['fi'],
            spacing=self.topLnRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
            rightSideCover=True,
            lstCover=lstCover,
            fromToExtPts=[fromExtPt,tr_tr-self.topLnRb['distRFend']*vdirTrTop],
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

    def drawBottomVarLongRF(self):
        '''draw and return the  longitudinal bottom rebar family 
        in the variable length stretch when slopeEdge is defined'''
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        vdirTrBott=(tr_br-tr_bl).normalize()
        vdirLnBott=(ln_br-ln_bl).normalize()
        Lsect2=self.botLnRb['s']/abs(self.slopeEdge)
        lstPtsConcrSect=[ln_bl,ln_br]
        lstPtsConcrSect2=[ln_bl,ln_bl+Lsect2*vdirLnBott]
        lstCover=[self.reinfCfg.cover+self.botTrnsRb['fi']]
        if self.botLnRb['closedStart'] or self.botLnRb['closedEnd']: ln_tl,ln_tr=self.getXmaxLongTopPnts()
        if self.botLnRb['closedStart']:
            lstPtsConcrSect.insert(0,ln_tl)
            lstPtsConcrSect2.insert(0,ln_tl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.botLnRb['closedEnd']:
            lstPtsConcrSect.append(ln_tr)
            lstPtsConcrSect2.append(ln_tl+Lsect2*vdirLnBott)
            lstCover.append(self.reinfCfg.cover)               
        ln_bot_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.botLnRb['id']+'v',
            diameter=self.botLnRb['fi'],
            spacing=self.botLnRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
            lstPtsConcrSect2=lstPtsConcrSect2,
            rightSideCover=False,
            lstCover=lstCover,
            fromToExtPts=[tr_bl,self.getTransitionBottPnt()],
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
    
    def drawTopVarLongRF(self):
        ''' draw and return the  longitudinal top rebar family
        in the variable length stretch when slopeEdge is defined'''
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        vdirLnTop=(ln_tr-ln_tl).normalize()
        Lsect2=self.botLnRb['s']/abs(self.slopeEdge)
        lstPtsConcrSect=[ln_tl,ln_tr]
        lstPtsConcrSect2=[ln_tl,ln_tl+Lsect2*vdirLnTop]
        lstCover=[self.reinfCfg.cover+self.topTrnsRb['fi']]
        if self.topLnRb['closedStart'] or self.topLnRb['closedEnd']: ln_bl,ln_br=self.getXmaxLongBottPnts()
        if self.topLnRb['closedStart']:
            lstPtsConcrSect.insert(0,ln_bl)
            lstPtsConcrSect2.insert(0,ln_bl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.topLnRb['closedEnd']:
            lstPtsConcrSect.append(ln_br)
            lstPtsConcrSect2.append(ln_bl+Lsect2*vdirLnTop)
            lstCover.append(self.reinfCfg.cover)
        ln_top_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.topLnRb['id']+'v',
            diameter=self.topLnRb['fi'],
            spacing=self.topLnRb['s'],
            lstPtsConcrSect=lstPtsConcrSect,
            lstPtsConcrSect2=lstPtsConcrSect2,
            rightSideCover=True,
            lstCover=lstCover,
            fromToExtPts=[tr_tl,self.getTransitionTopPnt()],
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
        ln_bl,ln_br=self.getXminLongBottPnts()
        ln_tl,ln_tr=self.getXminLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
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
        ln_bl,ln_br=self.getXminLongBottPnts()
        ln_tl,ln_tr=self.getXminLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
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

    def drawClosedTransvConcrSectYmax(self):
        ''' Draw concrete transverse cross-section
        placed at maximum Y coordinate'''
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
        return s

    def drawClosedTransvConcrSectYmin(self):
        ''' Draw concrete transverse cross-section
        placed at minimum Y coordinate'''
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        s=Part.makePolygon([tr_bl,tr_tl,tr_tr,tr_br,tr_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
        return s


    def drawClosedLongConcrSectXmin(self):
        ''' Draw the concrete longitudinal section at minimum X coordinate'''
        minXln_bl,minXln_br=self.getXminLongBottPnts()
        minXln_tl,minXln_tr=self.getXminLongTopPnts()
        s=Part.makePolygon([minXln_bl,minXln_tl,minXln_tr,minXln_br,minXln_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
        return s
      
    def drawClosedLongConcrSectXmax(self):
        ''' Draw the concrete longitudinal section at maximum X coordinate'''
        maxXln_bl,maxXln_br=self.getXmaxLongBottPnts()
        maxXln_tl,maxXln_tr=self.getXmaxLongTopPnts()
        s=Part.makePolygon([maxXln_bl,maxXln_tl,maxXln_tr,maxXln_br,maxXln_bl])
        p=Part.show(s)
        FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =colorConcrete
        return s
      

def constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,drawConcrTrSect=True,drawConcrLnSect=True,startId=1):
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
           where 'id' is the identificacion of the rebar family (if not defined, startId is used), 
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
            where 'id' is the identificacion of the stirrup family (if not defined, startId is used), 
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
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
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
        brick.drawClosedTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawClosedLongConcrSectXmax()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam

def sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,trSlopeBottFace=None,trSlopeTopFace=None,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,drawConcrTrSect=True,drawConcrLnSect=True,startId=1):
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
           where 'id' is the identificacion of the rebar family (if not defined, startId is used), 
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
            where 'id' is the identificacion of the stirrup family (if not defined, startId is used), 
                  'fi' is the diameter of the stirrup, 
                  'sRealSh' is the spacement between stirrups represented as real shape,
                  'sPerp'  is the spacement between stirrups in the orthogonal direction,
                  'widthStirr' is the width of the stirrup (internal),
                  'nStirrRealSh' is the number of stirrups in real shape
                  'nStirrPerp' is the number of stirrups in orthogonal direction
                  'dispRealSh' is the displacement of the stirrup family from the left extremity of the section (represented in real shape). If dispRealSh<0 the stirrups are drawn from right to end extremities of the slab
                  'dispPerp' is the displacement of the stirrup family from the left extremity of the section (in the orthogonal direction). If dispPerp<0 the stirrups are drawn from right to end extremities of the slab
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs. Each onr iss the data for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :param trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :param trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
    if drawConcrTrSect:
        brick.drawClosedTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawClosedLongConcrSectXmax()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam

def sloped_edge_constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,drawConcrTrSect=True,drawConcrLnSect=True,startId=1):
    '''Typical reinforcement arrangement of a brick of constant thickness with an sloped edge 
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
           where 'id' is the identificacion of the rebar family (if not defined, startId is used), 
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
            where 'id' is the identificacion of the stirrup family (if not defined, startId is used), 
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
    :iparam slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
        lstRebFam+=[brick.drawBottomVarLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
        lstRebFam+=[brick.drawTopVarLongRF()]
    if drawConcrTrSect:
        brick.drawClosedTransvConcrSectYmax()
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawClosedLongConcrSectXmax()
        else:
            brick.drawClosedLongConcrSectXmin()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam

def sloped_edge_sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,trSlopeBottFace=None,trSlopeTopFace=None,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,drawConcrTrSect=True,drawConcrLnSect=True,startId=1):
    '''Typical reinforcement arrangement of a brick with an sloped edge and sloped faces
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family

   :param width: dimension of the brick in the direction of the transverse rebars
    :param length: dimension of the brick in the direction of the longitudinal rebars
    :param thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param reinfCfg: instance of the cfg.reinfConf class
    :param slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    :param trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :param trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :param angTrns: angle (degrees) between the horizontal and the brick width dim    :param angLn: angle (degrees) between the horizontal and the brick length dimension
    :param botTrnsRb: data for bottom transverse rebar family expressed as a dictionary of type 
           {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1,'position':'good'}, 
           where 'id' is the identificacion of the rebar family (if not defined, startId is used), 
                  'fi' is the diameter of the rebar, 
                   's' is the spacement, 
                   'distRFstart' is the distance from the first rebar of the family to the left extremity of the brick (as it is drawn in the section),   
                   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the brick (as it is drawn in the section)
                                   (ignored in transverse rebars when sloped edge is defined)
                   'position' is the position of the rebars 'good' or 'poor' (used to calculate the 
                              slap length when splitting rebars
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
     '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
        lstRebFam+=[brick.drawBottomVarLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
        lstRebFam+=[brick.drawTopVarLongRF()]
    if drawConcrTrSect:
        brick.drawClosedTransvConcrSectYmax()
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawClosedLongConcrSectXmax()
        else:
            brick.drawClosedLongConcrSectXmin()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam

def closed_slab(width,length,thickness,botTrnsRb,topTrnsRb,botLnRb,topLnRb,anchPtTrnsSect,anchPtLnSect,reinfCfg,drawConcrTrSect=True,drawConcrLnSect=True,factGap=1,coverLat=None,startId=1):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal

    :param width: dimension of the slab in the direction of the transverse rebars
    :param length: dimension of the slab in the direction of the longitudinal rebars
    :param thickness: thickness of the slab
    :param botTrnsRb: data for bottom transverse rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family(if not defined, startId is used), 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the slab (as it is drawn in the section) (0 if not defined),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the slab (as it is drawn in the section) (0 if not defined)
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
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
    # transverse bottom rebar family
    init_RFdef_vars(botTrnsRb)
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
        position='good',
        )
    set_FR_options(RF=tr_bot_rf,RFdef=botTrnsRb)
    tr_bot_rf.createLstRebar()
    tr_bot_rf.drawPolySectBars()
    tr_bot_rf.drawLstRebar()
    # transverse top rebar family
    init_RFdef_vars(topTrnsRb)
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
        position='poor',
         )
    set_FR_options(RF=tr_top_rf,RFdef=topTrnsRb)
    tr_top_rf.createLstRebar()
    tr_top_rf.drawPolySectBars()
    tr_top_rf.drawLstRebar()
    # longitudinal bottom rebar family
    init_RFdef_vars(botLnRb)
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
        position='good',
        )
    set_FR_options(RF=ln_bot_rf,RFdef=botLnRb)
    ln_bot_rf.createLstRebar()
    ln_bot_rf.drawPolySectBars()
    ln_bot_rf.drawLstRebar()
    # Concrete transverse cross-section
    # longitudinal top rebar family
    init_RFdef_vars(topLnRb)
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
        position='poor',
         )
    set_FR_options(RF=ln_top_rf,RFdef=topLnRb)
    ln_top_rf.createLstRebar()
    ln_top_rf.drawPolySectBars()
    ln_top_rf.drawLstRebar()
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
    

def wall(height,length,thickness,leftVertRb,rightVertRb,leftHorRb,rightHorRb,anchPtVertSect,anchPtHorSect,reinfCfg,drawConcrVertSect=True,drawConcrHorSect=True,startId=1):
    '''Typical reinforcement arrangement of a closed slab
    Nomenclature: l-left, r-right, vert-vertical, hor-horizontal

    :param height: dimension of the wall in the direction of the vertical rebars
    :param length: dimension of the wall in the direction of the horizontal rebars
    :param thickness: thickness of the wall
    :param leftVertRb: data for left vertical rebar family expressed as a dictionary of type {'id':'3','fi':20e-3,'s':0.15,'distRFstart':0.2,'distRFend':0.1}, where 'id' is the identificacion of the rebar family (if not defined, startId is used), 'fi' is the diameter of the rebar, 's' is the spacement, 'distRFstart' is the distance from the first rebar of the family to the left extremity of the wall (as it is drawn in the section),   'distRFend' is the distance from the last rebar of the family to the rigth extremity of the wall (as it is drawn in the section)
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
    check_id([botTrnsRb,topTrnsRb,botLnRb,topLnRb],startId)
    # vertical left rebar family
    init_RFdef_vars(leftVertRb)
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
    # vertical right rebar family
    init_RFdef_vars(rightVertRb)
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
        position='good',
        )
    set_FR_options(RF=vert_right_rf,RFdef=rightVertRb)
    vert_right_rf.createLstRebar()
    vert_right_rf.drawPolySectBars()
    vert_right_rf.drawLstRebar()
    # horizontal left rebar family
    init_RFdef_vars(leftHorRb)
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
        position='good',
        )
    set_FR_options(RF=hor_left_rf,RFdef=leftHorRb)
    hor_left_rf.createLstRebar()
    hor_left_rf.drawPolySectBars()
    hor_left_rf.drawLstRebar()
    # horizontal right rebar family
    init_RFdef_vars(rightHorRb)
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
        position='good',
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
    '''Set optional attributes of RF rebar family that has been defined in dictionary RFdef
    '''
    if 'gapStart' in RFdef.keys(): RF.gapStart=RFdef['gapStart']
    if 'gapEnd' in RFdef.keys(): RF.gapEnd=RFdef['gapEnd']
    if 'extrShapeStart' in RFdef.keys(): RF.extrShapeStart=RFdef['extrShapeStart']
    if 'extrShapeEnd' in RFdef.keys(): RF.extrShapeEnd=RFdef['extrShapeEnd']
    if 'fixLengthStart' in RFdef.keys(): RF.fixLengthStart=RFdef['fixLengthStart']
    if 'fixLengthEnd' in RFdef.keys(): RF.fixLengthEnd=RFdef['fixLengthEnd']
    if 'vectorLRef' in RFdef.keys(): RF.vectorLRef=RFdef['vectorLRef']

def init_RFdef_vars(RFdef):
    ''' Set default values of 'distRFstart' and 'distRFend' if not defined in dictionary RFdef'''
    if 'distRFstart' not in RFdef.keys(): RFdef['distRFstart']=0.0
    if 'distRFend' not in RFdef.keys(): RFdef['distRFend']=0.0
    if 'closedStart' not in RFdef.keys(): RFdef['closedStart']=False
    if 'closedEnd' not in RFdef.keys(): RFdef['closedEnd']=False

def check_position(RFdef):
    if 'position' not in RFdef.keys(): lmsg.error("can't guess position of rebar family id:"+ RFdef['id']+ " 'position' key, good or poor, must be defined")
        
def check_id(lstRFdef, startId):
    ''' Checks if 'id' has been defined for each of the dictionaries in list lstRFdef and, otherwise,
       sets the value of 'id' based on startId'''
    for RFdef in lstRFdef:
        if RFdef:
             if 'id' not in RFdef.keys() or not RFdef['id']:
                 RFdef['id']=str(startId)
                 startId+=1
             
    

