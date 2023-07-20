# -*- coding: iso-8859-1 -*-

import math
import Part, FreeCAD
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
import FreeCADGui
from misc_utils import log_messages as lmsg

class genericBrickReinf(object):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family
                  X-coordinata: transverse direction
                  Y-coordinate: longitudinal direction.

    :ivar width: dimension of the brick in the direction of the transverse rebars
    :ivar length: dimension of the brick in the direction of the longitudinal rebars
    :ivar thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :ivar anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :ivar anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :ivar reinfCfg: instance of the cfg.reinfConf class
    :ivar angTrns: angle (degrees) between the horizontal and the brick width dimension
    :ivar angLn: angle (degrees) between the horizontal and the brick length dimension
    :ivar botTrnsRb: data for bottom transverse rebar family expressed as a dictionary of type 
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
    :ivar topTrnsRb: same for the top transverse rebar family
    :ivar botLnRb: same for the bottom longitudinal rebar family
    :ivar topLnRb: same for the top longitudinal rebar family
    :ivar sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as a dictionary of type: 
    :ivar sideXmaxRb: data for side reinforcement in face Xmax (defaults to None)
    :ivar sideYminRb: data for side reinforcement in face Ymin (defaults to None)
    :ivar sideYmaxRb: data for side reinforcement in face Ymax (defaults to None)
    :ivar lstStirrHoldTrReinf: list of stirrHoldTrReinfs . Each one is the data for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
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
    :ivar lstStirrHoldLnReinf: list of stirrHoldLnReinfs. Each onr iss the data for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :ivar trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :ivar trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :ivar slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    :ivar drawConcrTrSect: True if a closed concrete transverse cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :ivar drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :ivar anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :ivar angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :ivar drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :ivar startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''

    def __init__(self,width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,trSlopeBottFace=None,trSlopeTopFace=None,slopeEdge=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
        self.sideXminRb=sideXminRb
        self.sideXmaxRb=sideXmaxRb
        self.sideYminRb=sideYminRb
        self.sideYmaxRb=sideYmaxRb
        self.lstStirrHoldTrReinf=lstStirrHoldTrReinf
        self.lstStirrHoldLnReinf=lstStirrHoldLnReinf
        self.trSlopeBottFace=trSlopeBottFace
        self.trSlopeTopFace=trSlopeTopFace
        self.slopeEdge=slopeEdge
        self.drawConcrTrSect=drawConcrTrSect
        self.drawConcrLnSect=drawConcrLnSect
        self.anchPtPlan=anchPtPlan
        self.angPlan=angPlan
        self.drawPlan=drawPlan
        self.startId=startId
        
    def checkPosition(self,RFdef):
        if 'position' not in RFdef.keys(): lmsg.error("can't guess position of rebar family id:"+ RFdef['id']+ " 'position' key, 'good' or 'poor', must be defined")

    def checkId(self,RFdef):
        ''' Checks if 'id' has been defined for dictionary RFdec and, otherwise,
           sets the value of 'id' based on startId'''
        if 'id' not in RFdef.keys() or not RFdef['id']:
            RFdef['id']=str(self.startId)
            self.startId+=1
        
    def initRFdefVvars(self,RFdef):
        ''' Set default values of 'distRFstart' and 'distRFend' if not defined in dictionary RFdef'''
        if 'distRFstart' not in RFdef.keys(): RFdef['distRFstart']=0.0
        if 'distRFend' not in RFdef.keys(): RFdef['distRFend']=0.0
        if 'closedStart' not in RFdef.keys(): RFdef['closedStart']=False
        if 'closedEnd' not in RFdef.keys(): RFdef['closedEnd']=False
        
    def setFRoptions(self,RF,RFdef):
        '''Set optional attributes of RF rebar family that has been defined in dictionary RFdef
        '''
        if 'gapStart' in RFdef.keys(): RF.gapStart=RFdef['gapStart']
        if 'gapEnd' in RFdef.keys(): RF.gapEnd=RFdef['gapEnd']
        if 'extrShapeStart' in RFdef.keys(): RF.extrShapeStart=RFdef['extrShapeStart']
        if 'extrShapeEnd' in RFdef.keys(): RF.extrShapeEnd=RFdef['extrShapeEnd']
        if 'fixLengthStart' in RFdef.keys(): RF.fixLengthStart=RFdef['fixLengthStart']
        if 'fixLengthEnd' in RFdef.keys(): RF.fixLengthEnd=RFdef['fixLengthEnd']
        if 'vectorLRef' in RFdef.keys(): RF.vectorLRef=RFdef['vectorLRef']
        
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

    def getPntsPlan(self):
        if not self.anchPtPlan:
            lmsg.error('the point to anchor the plan view (anchPlan) is not defined')
        else:
            angP=math.radians(self.angPlan)
            vtr=Vector(math.cos(angP),math.sin(angP))
            vln=Vector(-vtr.y,vtr.x)
            pl_xmin_ymin=self.anchPtPlan
            pl_xmax_ymin=pl_xmin_ymin+self.width*vtr
            pl_xmax_ymax=pl_xmax_ymin+self.length*vln
            if not self.slopeEdge:
                pl_xmin_ymax=pl_xmin_ymin+self.length*vln
            else:
                pl_xmin_ymax=pl_xmax_ymax-(self.width+self.length*self.slopeEdge)*vtr
            return pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax
              
    def drawBottomTransvRF(self):
        ''' Draw and return the bottom transverse rebar family '''
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        vdirLn=self.getVdirLong()
        self.initRFdefVvars(self.botTrnsRb)
        self.checkPosition(self.botTrnsRb)
        self.checkId(self.botTrnsRb)
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
            position=self.botTrnsRb['position'],
            )
        self.setFRoptions(RF=tr_bot_rf,RFdef=self.botTrnsRb)
        tr_bot_rf.createLstRebar()
        tr_bot_rf.drawPolySectBars()
        tr_bot_rf.drawLstRebar()
        return tr_bot_rf

    def drawTopTransvRF(self):
        '''draw and return  the transverse top rebar family'''
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vdirLn=self.getVdirLong()
        self.initRFdefVvars(self.topTrnsRb)
        self.checkPosition(self.topTrnsRb)
        self.checkId(self.topTrnsRb)
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
        self.setFRoptions(RF=tr_top_rf,RFdef=self.topTrnsRb)    
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
        self.initRFdefVvars(self.botLnRb)
        self.checkPosition(self.botLnRb)
        self.checkId(self.botLnRb)
        if self.slopeEdge:
            fromExtPt=self.getTransitionBottPnt()
        else:
            fromExtPt=tr_bl+self.botLnRb['distRFstart']*vdirTrBott
        lstPtsConcrSect=[ln_bl,ln_br]
        if self.botTrnsRb:
            lstCover=[self.reinfCfg.cover+self.botTrnsRb['fi']]
            coverSectBars=self.reinfCfg.cover+self.botTrnsRb['fi']
        else:
            lstCover=[self.reinfCfg.cover]
            coverSectBars=self.reinfCfg.cover
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
            coverSectBars=coverSectBars,
            rightSideSectBars=False,
            gapStart=0,
            gapEnd=0,
            position=self.botLnRb['position'],
           )
        self.setFRoptions(RF=ln_bot_rf,RFdef=self.botLnRb)
        ln_bot_rf.createLstRebar()
        ln_bot_rf.drawPolySectBars()
        ln_bot_rf.drawLstRebar()
        return ln_bot_rf
    
    def drawTopLongRF(self):
        ''' draw and return the  longitudinal top rebar family'''
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        self.initRFdefVvars(self.topLnRb)
        self.checkPosition(self.topLnRb)  
        self.checkId(self.topLnRb)  
        if self.slopeEdge:
            fromExtPt=self.getTransitionTopPnt()
        else:
            fromExtPt= tr_tl+self.topLnRb['distRFstart']*vdirTrTop
        lstPtsConcrSect=[ln_tl,ln_tr]
        if self.topTrnsRb:
            lstCover=[self.reinfCfg.cover+self.topTrnsRb['fi']]
            coverSectBars=self.reinfCfg.cover+self.topTrnsRb['fi']
        else:
            lstCover=[self.reinfCfg.cover]
            coverSectBars=self.reinfCfg.cover
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
            coverSectBars=coverSectBars,
            rightSideSectBars=True,
            gapStart=0,
            gapEnd=0,
            position=self.topLnRb['position'],
            )
        self.setFRoptions(RF=ln_top_rf,RFdef=self.topLnRb)
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
        if self.botLnRb:
            lstCover=[self.reinfCfg.cover+self.botTrnsRb['fi']]
            coverSectBars=self.reinfCfg.cover+self.botTrnsRb['fi']
        else:
            lstCover=[self.reinfCfg.cover]
            coverSectBars=self.reinfCfg.cover
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
            coverSectBars=coverSectBars,
            rightSideSectBars=False,
            gapStart=0,
            gapEnd=0,
            position=self.botLnRb['position'],
           )
        self.setFRoptions(RF=ln_bot_rf,RFdef=self.botLnRb)
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
        if self.topTrnsRb:
            lstCover=[self.reinfCfg.cover+self.topTrnsRb['fi']]
            coverSectBars=self.reinfCfg.cover+self.topTrnsRb['fi']
        else:
            lstCover=[self.reinfCfg.cover]
            coverSectBars=self.reinfCfg.cover
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
            coverSectBars=coverSectBars,
            rightSideSectBars=True,
            gapStart=0,
            gapEnd=0,
            position=self.topLnRb['position'],
            )
        self.setFRoptions(RF=ln_top_rf,RFdef=self.topLnRb)
        ln_top_rf.createLstRebar()
        ln_top_rf.drawPolySectBars()
        ln_top_rf.drawLstRebar()
        return ln_top_rf
    
    def drawSideXminRF(self):
        ''' Draw and return the side refinforcement in face Xmin'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vDir=(tr_tl-tr_bl).normalize()
        self.initRFdefVvars(self.sideXminRb)
        self.checkPosition(self.sideXminRb)
        self.checkId(self.sideXminRb)
        if 'coverSectBars' in self.sideXminRb.keys():
            coverSectBars=self.sideXminRb['coverSectBars']
        else:
            coverSectBars=self.reinfCfg.cover
        side_xmin_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.sideXminRb['id'],
            diameter=self.sideXminRb['fi'],
            nmbBars=self.sideXminRb['nmbBars'],
            lstPtsConcrSect=[pl_xmin_ymin,pl_xmin_ymax],
            rightSideCover=True,
            fromToExtPts=[tr_bl+self.sideXminRb['distRFstart']*vDir,tr_tl-self.sideXminRb['distRFend']*vDir],
            coverSectBars=coverSectBars,
            rightSideSectBars=True,
            position=self.sideXminRb['position'],
            )
        self.setFRoptions(RF=side_xmin_rf,RFdef=self.sideXminRb)
        side_xmin_rf.createLstRebar()
        side_xmin_rf.drawPolySectBars()
        side_xmin_rf.drawLstRebar()
        return side_xmin_rf
          
    def drawSideXmaxRF(self):
        ''' Draw and return the side refinforcement in face Xmax'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vDir=(tr_tr-tr_br).normalize()
        self.initRFdefVvars(self.sideXmaxRb)
        self.checkPosition(self.sideXmaxRb)
        self.checkId(self.sideXmaxRb)
        if 'coverSectBars' in self.sideXmaxRb.keys():
            coverSectBars=self.sideXmaxRb['coverSectBars']
        else:
            coverSectBars=self.reinfCfg.cover
        side_xmax_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.sideXmaxRb['id'],
            diameter=self.sideXmaxRb['fi'],
            nmbBars=self.sideXmaxRb['nmbBars'],
            lstPtsConcrSect=[pl_xmax_ymin,pl_xmax_ymax],
            rightSideCover=False,
            fromToExtPts=[tr_br+self.sideXmaxRb['distRFstart']*vDir,tr_tr-self.sideXmaxRb['distRFend']*vDir],
            coverSectBars=coverSectBars,
            rightSideSectBars=False,
            position=self.sideXmaxRb['position'],
            )
        self.setFRoptions(RF=side_xmax_rf,RFdef=self.sideXmaxRb)
        side_xmax_rf.createLstRebar()
        side_xmax_rf.drawPolySectBars()
        side_xmax_rf.drawLstRebar()
        return side_xmax_rf
          
    def drawSideYminRF(self):
        ''' Draw and return the side refinforcement in face Ymin'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vDir=(ln_tl-ln_bl).normalize()
        self.initRFdefVvars(self.sideYminRb)
        self.checkPosition(self.sideYminRb)
        self.checkId(self.sideYminRb)
        if 'coverSectBars' in self.sideYminRb.keys():
            coverSectBars=self.sideYminRb['coverSectBars']
        else:
            coverSectBars=self.reinfCfg.cover
        side_ymin_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.sideYminRb['id'],
            diameter=self.sideYminRb['fi'],
            nmbBars=self.sideYminRb['nmbBars'],
            lstPtsConcrSect=[pl_xmin_ymin,pl_xmax_ymin],
            rightSideCover=False,
            fromToExtPts=[ln_bl+self.sideYminRb['distRFstart']*vDir,ln_tl-self.sideYminRb['distRFend']*vDir],
            coverSectBars=coverSectBars,
            rightSideSectBars=True,
            position=self.sideYminRb['position'],
            )
        self.setFRoptions(RF=side_ymin_rf,RFdef=self.sideYminRb)
        side_ymin_rf.createLstRebar()
        side_ymin_rf.drawPolySectBars()
        side_ymin_rf.drawLstRebar()
        return side_ymin_rf
          
    def drawSideYmaxRF(self):
        ''' Draw and return the side refinforcement in face Ymax'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vDir=(ln_tr-ln_br).normalize()
        self.initRFdefVvars(self.sideYmaxRb)
        self.checkPosition(self.sideYmaxRb)
        self.checkId(self.sideYmaxRb)
        if 'coverSectBars' in self.sideYmaxRb.keys():
            coverSectBars=self.sideYmaxRb['coverSectBars']
        else:
            coverSectBars=self.reinfCfg.cover
        side_ymax_rf=rb.rebarFamily(
            reinfCfg=self.reinfCfg,
            identifier=self.sideYmaxRb['id'],
            diameter=self.sideYmaxRb['fi'],
            nmbBars=self.sideYmaxRb['nmbBars'],
            lstPtsConcrSect=[pl_xmin_ymax,pl_xmax_ymax],
            rightSideCover=True,
            fromToExtPts=[ln_br+self.sideYmaxRb['distRFstart']*vDir,ln_tr-self.sideYmaxRb['distRFend']*vDir],
            coverSectBars=coverSectBars,
            rightSideSectBars=False,
            position=self.sideYmaxRb['position'],
            )
        self.setFRoptions(RF=side_ymax_rf,RFdef=self.sideYmaxRb)
        side_ymax_rf.createLstRebar()
        side_ymax_rf.drawPolySectBars()
        side_ymax_rf.drawLstRebar()
        return side_ymax_rf
          
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

    def drawTransvConcrSectYmax(self):
        ''' Draw concrete transverse cross-section
        placed at maximum Y coordinate'''
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        lstPnts=[tr_bl,tr_tl,tr_tr,tr_br,tr_bl]
        if self.drawConcrTrSect == True: #closed section
            s=Part.makePolygon(lstPnts)
            p=Part.show(s)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        elif  type(self.drawConcrTrSect) == list:
            for n_edge in self.drawConcrTrSect:
                l=Part.makeLine(lstPnts[n_edge-1],lstPnts[n_edge])
                p=Part.show(l)
                FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        else:
            lmsg.error(" 'drawConcrTrSect' must be 'True' for closed section or a list of the edges you want draw")

    def drawTransvConcrSectYmin(self):
        ''' Draw concrete transverse cross-section
        placed at minimum Y coordinate'''
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        lstPnts=[tr_bl,tr_tl,tr_tr,tr_br,tr_bl]
        if self.drawConcrTrSect == True: #closed section
            s=Part.makePolygon(lstPnts)
            p=Part.show(s)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        elif  type(self.drawConcrTrSect) == list:
            for n_edge in self.drawConcrTrSect:
                l=Part.makeLine(lstPnts[n_edge-1],lstPnts[n_edge])
                p=Part.show(l)
                FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        else:
            lmsg.error(" 'drawConcrTrSect' must be 'True' for closed section or a list of the edges you want draw")

    def drawLongConcrSectXmin(self):
        ''' Draw the concrete longitudinal section at minimum X coordinate'''
        minXln_bl,minXln_br=self.getXminLongBottPnts()
        minXln_tl,minXln_tr=self.getXminLongTopPnts()
        lstPnts=[minXln_bl,minXln_tl,minXln_tr,minXln_br,minXln_bl]
        if self.drawConcrLnSect == True: #closed section
            s=Part.makePolygon(lstPnts)
            p=Part.show(s)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        elif  type(self.drawConcrLnSect) == list:
            for n_edge in self.drawConcrLnSect:
                l=Part.makeLine(lstPnts[n_edge-1],lstPnts[n_edge])
                p=Part.show(l)
                FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        else:
            lmsg.error(" 'drawConcrLnSect' must be 'True' for closed section or a list of the edges you want draw")
      
    def drawLongConcrSectXmax(self):
        ''' Draw the concrete longitudinal section at maximum X coordinate'''
        maxXln_bl,maxXln_br=self.getXmaxLongBottPnts()
        maxXln_tl,maxXln_tr=self.getXmaxLongTopPnts()
        lstPnts=[maxXln_bl,maxXln_tl,maxXln_tr,maxXln_br,maxXln_bl]
        if self.drawConcrLnSect == True: #closed section
            s=Part.makePolygon(lstPnts)
            p=Part.show(s)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        elif  type(self.drawConcrLnSect) == list:
            for n_edge in self.drawConcrLnSect:
                l=Part.makeLine(lstPnts[n_edge-1],lstPnts[n_edge])
                p=Part.show(l)
                FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        else:
            lmsg.error(" 'drawConcrLnSect' must be 'True' for closed section or a list of the edges you want draw")

    def drawPlanConcrView(self):
        " Draw the concrete plan view (usually used when side reinforcement is defined) "
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        lstPnts=[pl_xmin_ymin,pl_xmin_ymax,pl_xmax_ymax,pl_xmax_ymin,pl_xmin_ymin]
        if self.drawPlan == True: #closed section
            s=Part.makePolygon(lstPnts)
            p=Part.show(s)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        elif  type(self.drawPlan) == list:
            for n_edge in self.drawPlan:
                l=Part.makeLine(lstPnts[n_edge-1],lstPnts[n_edge])
                p=Part.show(l)
                FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
        else:
            lmsg.error(" 'drawPlan' must be 'True' for closed section or a list of the edges you want draw")
      

def constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as a dictionary of type: 
    :param sideXmaxRb: data for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: data for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: data for side reinforcement in face Ymax (defaults to None)
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
  (defaults to True)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,lstStirrHoldTrReinf=lstStirrHoldTrReinf,lstStirrHoldLnReinf=lstStirrHoldLnReinf,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
    if sideXminRb:
        lstRebFam+=[brick.drawSideXminRF()]
    if sideXmaxRb:
        lstRebFam+=[brick.drawSideXmaxRF()]
    if sideYminRb:
        lstRebFam+=[brick.drawSideYminRF()]
    if sideYmaxRb:
        lstRebFam+=[brick.drawSideYmaxRF()]
    if lstStirrHoldTrReinf:
        lstStirrFam+=[brick.drawStirrHoldingTransvSF()]
    if lstStirrHoldLnReinf:
        lstStirrFam+=[brick.drawStirrHoldingLongSFf()]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawLongConcrSectXmax()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,trSlopeBottFace=None,trSlopeTopFace=None,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as a dictionary of type: 
    :param sideXmaxRb: data for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: data for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: data for side reinforcement in face Ymax (defaults to None)
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
  (defaults to True)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    if botTrnsRb:
        lstRebFam+=[brick.drawBottomTransvRF()]
    if topTrnsRb:
        lstRebFam+=[brick.drawTopTransvRF()]
    if botLnRb:
        lstRebFam+=[brick.drawBottomLongRF()]
    if topLnRb:
        lstRebFam+=[brick.drawTopLongRF()]
    if sideXminRb:
        lstRebFam+=[brick.drawSideXminRF()]
    if sideXmaxRb:
        lstRebFam+=[brick.drawSideXmaxRF()]
    if sideYminRb:
        lstRebFam+=[brick.drawSideYminRF()]
    if sideYmaxRb:
        lstRebFam+=[brick.drawSideYmaxRF()]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawLongConcrSectXmax()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def sloped_edge_constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as a dictionary of type: 
    :param sideXmaxRb: data for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: data for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: data for side reinforcement in face Ymax (defaults to None)
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
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
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
    if sideXminRb:
        lstRebFam+=[brick.drawSideXminRF()]
    if sideXmaxRb:
        lstRebFam+=[brick.drawSideXmaxRF()]
    if sideYminRb:
        lstRebFam+=[brick.drawSideYminRF()]
    if sideYmaxRb:
        lstRebFam+=[brick.drawSideYmaxRF()]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawLongConcrSectXmax()
        else:
            brick.drawLongConcrSectXmin()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def sloped_edge_sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,trSlopeBottFace=None,trSlopeTopFace=None,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as a dictionary of type: 
    :param sideXmaxRb: data for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: data for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: data for side reinforcement in face Ymax (defaults to None)
    :param drawConcrTrSect: True if the concrete transverse cross-section is drawn (defaults to True)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
     '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
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
        brick.drawTransvConcrSectYmax()
    if sideXminRb:
        lstRebFam+=[brick.drawSideXminRF()]
    if sideXmaxRb:
        lstRebFam+=[brick.drawSideXmaxRF()]
    if sideYminRb:
        lstRebFam+=[brick.drawSideYminRF()]
    if sideYmaxRb:
        lstRebFam+=[brick.drawSideYmaxRF()]
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawLongConcrSectXmax()
        else:
            brick.drawLongConcrSectXmin()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

    


        
             
    

