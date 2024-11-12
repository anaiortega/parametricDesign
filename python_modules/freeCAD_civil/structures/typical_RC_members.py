# -*- coding: utf-8 -*-

import math
import copy
import FreeCAD
import Part
from parametric_design.freeCAD_civil import draw_config as cfg
from parametric_design.freeCAD_civil import reinf_bars as rb
from FreeCAD import Vector
import FreeCADGui
from misc_utils import log_messages as lmsg

class brkRbFam(rb.rebarFamily):
    '''Define a rebar family for a brick reinforcement
    
    :ivar fi: diameter of the bars of the family [m]
    :ivar s: spacing between bars [m] (defaults to None). Either s or nmbBars 
             must be defined
    :ivar Id: identifier of the rebar family (defaults to None)
    :ivar nmbBars: number of rebars in the family. This parameter takes
            precedende over 'spacing' (defaults to None)
    :ivar distRFstart: distance from the first rebar of the family to the left extremity of the brick 
          (as it is drawn in the section)  (not implemented in cylinders)  (defaults to 0)
    :ivar distRFend: distance from the last rebar of the family to the right extremity of the brick 
          (as it is drawn in the section) (not implemented in cylinders)  (defaults to 0)
    :ivar closedStart: the bar extends along the side of the brick before the start 
          (not implemented in cylinders) (defaults to False)
    :ivar closedEnd: the bar extends along the side of the brick after the end 
          (not implemented in cylinders)  (defaults to False)
    :ivar vectorLRef:vector to draw the leader line for labeling the bar (defaults to Vector(0.5,0.5)
    :ivar lateralCover: minimal lateral cover to place the rebar family (defaults to cfg.defaultReinfConf.cover)
    :ivar gapStart: increment (decrement if gapStart <0) of the length of 
            the reinforcement at its starting extremity (defaults to cfg.defaultReinfConf.cover)
    :ivar gapEnd:  increment (decrement if gapEnd<0) of the length of 
            the reinforcement at its ending extremity  (defaults to fg.defaultReinfConf.cover)
    :ivar extrShapeStart:defines the shape of the bar at its starting 
            extremity. It can be an straight or hook shape with anchor (anc) length, 
            lap length or a given fixed length.
            The anchor or lap length are automatically 
            calculated from the code, material, and rebar configuration.
            It's defined as a string parameter that can be read as:
          For anchor end:
            'anc[angle]_position_stressState', where:
            anc[angle]= the anchor length is calculated.
                        angle is a positive number, expresed in sexagesimal degrees, 
                        that represents the counterclokwise angle from the first segment 
                        of the rebar towards the hook.
                        If angle is 0 or 180, the straight anchor length is calculated 
                        'straight' for straight elongation,
            position= 'posGood' if rebar in position I according to EHE definition =
                                position 'good' according to EC2 definition.
                      'posPoor' if rebar in position II according to EHE definition = 
                                position 'poor'. according to EC2 definition.
            stressState= 'tens' if rebar in tension
                         'compr' if rebar in compression.
            Examples: 'anc90_posGood_compr', 'anc0_posPoor_tens'
          For lap end:
            'lap[angle]_position_stressState_perc[percentage]', where:
            lap[angle]= the lap length is calculated.
                        angle is a positive number, expresed in sexagesimal degrees, 
                        that represents the counterclokwise angle from the first segment 
                        of the rebar towards the hook.
            position= 'posGood' if rebar in position I according to EHE definition =
                                position 'good' according to EC2 definition.
                      'posPoor' if rebar in position II according to EHE definition = 
                                position 'poor'. according to EC2 definition.
            stressState= 'tens' if rebar in tension
                         'compr' if rebar in compression.
            perc[percentage]= percentage is the percentage of rebars that are lapped.
            Examples: 'lap90_posGood_compr', 'lap0_posPoor_tens_perc50'
          For fixed end:
            'fix[angle]= same meaning
            len[number]: number is the length of the segment to add (in mm)
            Examples: 'fix45_len150'
            (defaults to None)
    :ivar extrShapeEnd: defines a straigth elongation or a hook at the ending 
            extremity of the bar. Definition analogous to extrShapeStart.(defaults to None)
    :ivar fixLengthStart: fixed length of the first segment of the rebar(defaults to None)
    :ivar fixLengthEnd:fixed length of the last segment of the rebar (defaults to None)
    :ivar extensionLength:length of the stretch in which the rebar family extends.(defaults to None)
    :ivar maxLrebar: maximum length of rebars (defaults to 12 m)
    :ivar position:  'good' or 'poor' (equivalent to posI and posII in EHE). Is used to
             calculate lap lengths when splitting bars- (defaults to 'poor')
    :ivar compression: True if rebars in compression, False if rebars in tension.  
            Is used to calculate lap lengths when splitting bars- (defaults to False)
    :ivar drawSketch: True to draw mini-sketch of the rebars besides the text(defaults to True)
    :ivar nMembers:  number of identic members. The calculated number of bars is multiplied by nMembers(defaults to 1)
    :ivar addTxt2Label: add the specified text to the reinforcement label (defaults to None)
    :ivar addCover: add positive or negative cover to the default calculates cover (defaults to 0)
    :ivar reinfCfg: instance of the reinfConf class that defines generic parameters like concrete and steel type, text format, ... (defaults to cfg.defaultReinfConf)
    '''
    def __init__(self,fi,s=None,Id=None,nmbBars=None,distRFstart=0,distRFend=0,closedStart=False,closedEnd=False,vectorLRef=Vector(0.5,0.5),lateralCover=None,gapStart=None,gapEnd=None,extrShapeStart=None,extrShapeEnd=None,fixLengthStart=None,fixLengthEnd=None,extensionLength=None,maxLrebar=12,position='poor',compression=False,drawSketch=True,nMembers=1,addCover=0,addTxt2Label=None,reinfCfg=cfg.defaultReinfConf):
        super(brkRbFam,self).__init__(reinfCfg=reinfCfg,identifier=Id,diameter=fi,lstPtsConcrSect=[],fromToExtPts=None,sectBarsConcrRadius=1,extensionLength=extensionLength,lstCover=None,rightSideCover=True,vectorLRef=vectorLRef,coverSectBars=None,lateralCover=lateralCover,rightSideSectBars=True,spacing=s,nmbBars=nmbBars,lstPtsConcrSect2=None,gapStart=gapStart,gapEnd=gapEnd,extrShapeStart=extrShapeStart,extrShapeEnd=extrShapeEnd,fixLengthStart=fixLengthStart,fixLengthEnd=fixLengthEnd,maxLrebar=maxLrebar,position=position,compression=compression,drawSketch=drawSketch,nMembers=nMembers,addTxt2Label=addTxt2Label)
        self.distRFstart=distRFstart
        self.distRFend=distRFend
        self.closedStart=closedStart
        self.closedEnd=closedEnd
        self.addCover=addCover
    
    def checkInconsitency(self):
        if self.extrShapeStart and self.closedStart:
            lmsg.warning('Start-extremity shape definition may not be compatible with closed start')
        if self.extrShapeEnd and self.closedEnd:
            lmsg.warning('End-extremity shape definition may not be compatible with closed send')
            
class brkStirrFam(rb.stirrupFamily):
    '''Define a stirrup family for a brick reinforcement

    :ivar fi: diameter of the bars of the family [m]
    :ivar widthStirr: width of the stirrup (internal) (defaults to 0.20)
    :ivar sRealSh: spacement between stirrups represented as real shape (defaults to None)
    :ivar sPerp: spacement between stirrups in the orthogonal direction (defaults to None)
    :ivar Id: identifier of the rebar family (defaults to None)
    :ivar sRealSh: spacement between stirrups represented as real shape 
    :ivar sPerp: spacement between stirrups in orthogonal direction 
    :ivar nStirrPerp: number of stirrups in orthogonal direction (defaults to 1)
    :ivar dispRealSh: displacement of the stirrup family from the left extremity of the section 
          (represented in real shape). If dispRealSh<0 the stirrups are drawn from right to end 
          extremities of the slab (defaults to =0)
    :ivar dispPerp: displacement of the stirrup family from the left extremity of the section 
          (in the orthogonal direction). If dispPerp<0 the stirrups are drawn from right to end 
          extremities of the slab (defaults to 0)
    :ivar vDirTrans: vector to define the transversal direction (defaults to None, in which case 
          the direction of the first side of the concrete section is taken)    
    :ivar vDirLong: vector to define the longitudinal direction (defaults to Vector(1,0)
    :ivar rightSideCover: cover given to the right side (defaults to True)
    :ivar vectorLRef: vector to draw the leader line for labeling the barVector
          (defaults to Vector(0.5,0.5)
    :ivar rightSideLabelLn: side to place the label of the stirrups in longitudinal section 
          (defaults to True -> right)
    :ivar closed: if closed stirrup True (defaults to True)
    :ivar addL2closed: length to add to closed stirrups (defaults to 0.20)
    :ivar fixAnchorStart, fixAnchorEnd: anchor definition at start and end, respectively 
          (defaults to None) The anchors are defined as follows:
            fix[angle]= is a positive number, expresed in sexagesimal degrees, 
                        that represents the counterclokwise angle from the first segment 
                        of the rebar towards the hook.
            len[number]: number is the length of the segment to add (in mm)
            Examples: 'fix45_len150'
    :ivar nMembers: number of identic members. The calculated number of bars is multiplied 
          by nMembers (defaults to 1)
    :ivar addCover: add positive or negative cover to the default calculates cover (defaults to 0)
    :ivar addTxt2Label: add the specified text to the reinforcement label (defaults to None)
    :ivar reinfCfg: instance of the reinfConf class that defines generic parameters like concrete 
          and steel type, text format, ... (defaults to cfg.defaultReinfConf)cfg.defaultReinfConf
    '''
    def __init__(self,fi,widthStirr=0.20,sRealSh=None,sPerp=None,Id=None,nStirrRealSh=1,nStirrPerp=1,dispRealSh=0,dispPerp=0,vDirTrans=None,vDirLong=Vector(1,0),rightSideCover=True,vectorLRef=Vector(0.5,0.5),rightSideLabelLn=True,closed=True,addL2closed=0.20,fixAnchorStart=None,fixAnchorEnd=None,nMembers=1,addCover=0,addTxt2Label=None,reinfCfg=cfg.defaultReinfConf):
        super(brkStirrFam,self).__init__(reinfCfg=reinfCfg,identifier=Id,diameter=fi,lstPtsConcrLong=[],lstPtsConcrSect=[Vector(0,0)],concrSectRadius=None,spacStrpTransv=sRealSh,spacStrpLong=sPerp,vDirTrans=vDirTrans,vDirLong=vDirLong,nmbStrpTransv=nStirrRealSh,nmbStrpLong=nStirrPerp,lstCover=None,lstCoverLong=None,rightSideCover=rightSideCover,dispStrpTransv=abs(dispRealSh),dispStrpLong=abs(dispPerp),vectorLRef=vectorLRef,rightSideLabelLn=rightSideLabelLn,closed=closed,addL2closed=addL2closed,fixAnchorStart=fixAnchorStart,fixAnchorEnd=fixAnchorEnd,nMembers=nMembers,addTxt2Label=addTxt2Label)
        self.dispRealSh=dispRealSh
        self.dispPerp=dispPerp
        self.nStirrRealSh=nStirrRealSh
        self.nStirrPerp=nStirrPerp
        self.widthStirr=widthStirr
        self.addCover=addCover
        
class genericReinfBase(object):
    '''Base class to define generic members reinforcement

    :ivar length: dimension of the member in the direction of the longitudinal rebars
    :ivar thickness: thickness of the menber represented in the longitudinal section. In cylindric
          elements the thicknes is tthe diameter of the cross-section
    :ivar angLn: angle (degrees) between the horizontal and the member length dimension
    :ivar anchPtLnSect: anchor point to place the bottom left corner of the concrete longitudinal section
    :ivar startId: integer to successively identify the reinforcement families created for which their identifier
           has not been defined or it is None (defaults to 1)
   '''
    def __init__(self,length,thickness,angLn,anchPtLnSect,drawConcrLnSect=True,startId=1):
        self.length=length
        self.thickness=thickness
        self.angLn=angLn
        self.anchPtLnSect=anchPtLnSect
        self.startId=startId
                 
    def checkId(self,RF):
        ''' Checks if 'Id' has been defined for the rebar or stirrup family RF, otherwise,
           sets the value of 'Id' based on startId'''
        if not RF.identifier:
            RF.identifier=str(self.startId)
            self.startId+=1
            
    def initRFVvars(self,RF):
        ''' Set default values of 'distRFstart' and 'distRFend' if not defined in dictionary RF'''
        if RF.spacing:
            RF.nmbBars=None
        elif RF.nmbBars:
            RF.s=None
        else:
            lmsg.error("either spacing 's' of number of rebars 'nmbBars' must be defined")
        
    def getVdirLong(self):
        vdirLn=Vector(math.cos(math.radians(self.angLn)),math.sin(math.radians(self.angLn)))
        return vdirLn

    def getSimplLongBottPnts(self):
        ''' return the left and right bottom points of the simple longitudinal concrete 
        section '''
        vdirLn=self.getVdirLong()
        ln_bl=self.anchPtLnSect
        ln_br= ln_bl+self.length*self.getVdirLong()
        return ln_bl,ln_br
    
    def getSimplLongTopPnts(self):
        ''' return the left and right top points of the simple longtudinal concrete 
        section'''
        vdirLn=self.getVdirLong(); vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
        ln_tl=self.anchPtLnSect+self.thickness*vdirLnPerp
        ln_tr= ln_tl+self.length*self.getVdirLong()
        return ln_tl,ln_tr

    def getMaxDiameter(self,lstReinf):
        '''Returns the maximum diameter of the rebars or stirrups defined in list lstReinf
        (if lstReinf doesn't exists, return 0)
        '''
        fiMax=0
        if lstReinf:
            lstDiam=[rb.diameter for rb in lstReinf if rb]
            if len(lstDiam)>0:
                fiMax=max(lstDiam)
        return fiMax
        
class genericBrickReinf(genericReinfBase):
    '''Typical reinforcement arrangement of an open brick 
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-brick rebar family
                  X-coordinata: transverse direction
                  Y-coordinate: longitudinal direction.

    :ivar width: dimension of the brick in the direction of the transverse rebars
    :ivar length: dimension of the brick in the direction of the longitudinal rebars
    :ivar thickness: thickness of the brick at the start (at point anchPtTrnsSect)
    :ivar anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse 
          cross-section
    :ivar anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal 
          section
    :ivar anchPtPlan: anchor point to place the bottom left corner of the concrete plan view
    :ivar reinfCfg: instance of the cfg.reinfConf class
    :ivar angTrns: angle (degrees) between the horizontal and the brick width dimension
    :ivar angLn: angle (degrees) between the horizontal and the brick length dimension
    :ivar botTrnsRb: data for bottom transverse rebar family expressed as instance of brkRbFam class
    :ivar topTrnsRb: same for the top transverse rebar family
    :ivar botLnRb: same for the bottom longitudinal rebar family
    :ivar topLnRb: same for the top longitudinal rebar family
    :ivar sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as 
          instance of brkRbFam class
    :ivar sideXmaxRb: same for side reinforcement in face Xmax (defaults to None)
    :ivar sideYminRb: same for side reinforcement in face Ymin (defaults to None)
    :ivar sideYmaxRb: same for side reinforcement in face Ymax (defaults to None)
    :ivar lstStirrHoldTrReinf: list of stirrHoldTrReinfs expressed as instances of brkStirrFam class. 
          Each one is the data for a stirrup rebar familiy that holds transverse top and bottom rebar 
          families. Real shape is depicted in the longitudinal section
    :ivar lstStirrHoldLnReinf: list of stirrHoldLnReinfs expressed as instances of brkStirrFam class. 
          Each one is the data for a stirrup rebar family that holds longitudinal top and bottom rebar 
          families
    :ivar trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :ivar trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :ivar slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    :ivar drawConcrTrSect: True if a closed concrete transverse cross-section is drawn or a list of 
          edges (e.g. [2,4] if only second and fourth edges are drawn) (defaults to True)
    :ivar drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of 
          edges (e.g. [2,4] if only second and fourth edges are drawn) (defaults to True)
    :ivar anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing 
          (in general, the plan drawing is only used when defining side reinforcement) (defaults to None)
    :ivar angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :ivar drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] 
          if only second and fourth edges are drawn) (anchPtPlan must be defined) (defaults to False)
    :ivar startId: integer to successively identify the reinforcement families created for which 
          their identifier has not been defined or it is None (defaults to 1)
    '''

    def __init__(self,width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,trSlopeBottFace=None,trSlopeTopFace=None,slopeEdge=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
        super(genericBrickReinf,self).__init__(length=length,thickness=thickness,angLn=angLn,anchPtLnSect=anchPtLnSect,startId=startId)
        self.width=width
        self.anchPtTrnsSect=anchPtTrnsSect
        self.reinfCfg=reinfCfg
        self.angTrns=angTrns
        self.botTrnsRb=copy.copy(botTrnsRb)
        self.topTrnsRb=copy.copy(topTrnsRb)
        self.botLnRb=copy.copy(botLnRb)
        self.topLnRb=copy.copy(topLnRb)
        self.sideXminRb=copy.copy(sideXminRb)
        self.sideXmaxRb=copy.copy(sideXmaxRb)
        self.sideYminRb=copy.copy(sideYminRb)
        self.sideYmaxRb=copy.copy(sideYmaxRb)
        self.lstStirrHoldTrReinf=copy.copy(lstStirrHoldTrReinf)
        self.lstStirrHoldLnReinf=copy.copy(lstStirrHoldLnReinf)
        self.trSlopeBottFace=trSlopeBottFace
        self.trSlopeTopFace=trSlopeTopFace
        self.slopeEdge=slopeEdge
        self.drawConcrTrSect=drawConcrTrSect
        self.drawConcrLnSect=drawConcrLnSect
        self.anchPtPlan=anchPtPlan
        self.angPlan=angPlan
        self.drawPlan=drawPlan

    def getMaxStirrHoldTrDiam(self):
        ''' Return the maximum diameter of the stirrup families that hold the transv. rebars'''
        fiMax=self.getMaxDiameter(self.lstStirrHoldTrReinf)
        return fiMax
    
    def getMaxStirrHoldLnDiam(self):
        ''' Return the maximum diameter of the stirrup families that hold the longitucinal rebars'''
        fiMax=self.getMaxDiameter(self.lstStirrHoldLnReinf)
        return fiMax
    
    def getVdirTransv(self):
        vdirTr=Vector(math.cos(math.radians(self.angTrns)),math.sin(math.radians(self.angTrns)))
        return vdirTr
    
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
        ln_bl,ln_br=self.getSimplLongBottPnts()
        if self.trSlopeBottFace:
            vdirLn=self.getVdirLong(); vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
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
        ln_tl,ln_tr=self.getSimplLongTopPnts()
        if self.trSlopeTopFace:
            vdirLn=self.getVdirLong(); vdirLnPerp=Vector(-1*vdirLn.y,vdirLn.x)
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
            if self.anchPtTrnsSect:
                self.anchPtPlan=self.anchPtTrnsSect-2*Vector(self.width,0)
            elif self.anchPtLnSect:
                self.anchPtPlan=self.anchPtLnSect-2*Vector(self.width,0)
            else:
                lmsg.error('either anchPtPlan or anchPtTrnsSectn or anchPtLnSect must be defined')
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

    def getCoverBottomTransvRF(self):
        cover=self.reinfCfg.cover+self.getMaxStirrHoldTrDiam()+self.botTrnsRb.addCover
        return cover

    def getCoverTopTransvRF(self):
        cover=self.reinfCfg.cover+self.getMaxStirrHoldTrDiam()+self.topTrnsRb.addCover
        return cover
              
    def getCoverBottomLongRF(self):
        '''Return the cover of the bottom longitudinal rebars
        '''
        if self.botTrnsRb:
            cover=self.reinfCfg.cover+self.botTrnsRb.diameter+self.getMaxStirrHoldTrDiam()+self.botTrnsRb.addCover
        else:
            cover=self.reinfCfg.cover+self.getMaxStirrHoldLnDiam()+self.botTrnsRb.addCover
        return cover
        
    def getCoverTopLongRF(self):
        '''Return the cover of the top longitudinal rebars
        '''
        if self.topTrnsRb:
            cover=self.reinfCfg.cover+self.topTrnsRb.diameter+self.getMaxStirrHoldTrDiam()+self.topTrnsRb.addCover
        else:
            cover=self.reinfCfg.cover+self.getMaxStirrHoldLnDiam()+self.topTrnsRb.addCover
        return cover

    def getCoverSideXminRF(self):
        '''Return the cover of the side reinforcement in face Xmin'''
        cover=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])+self.sideXminRb.addCover
        return cover
    
    def getCoverSideXmaxRF(self):
        '''Return the cover of the side reinforcement in face Xmax'''
        cover=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])+self.sideXmaxRb.addCover
        return cover
    
    def getCoverSideYminRF(self):
        '''Return the cover of the side reinforcement in face Ymin'''
        cover=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])+self.sideYminRb.addCover
        return cover
    
    def getCoverSideYmaxRF(self):
        '''Return the cover of the side reinforcement in face Ymax'''
        cover=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])+self.sideYmaxRb.addCover
        return cover
   
        
    def drawBottomTransvRF(self):
        ''' Draw and return the bottom transverse rebar family '''
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        vdirLn=self.getVdirLong()
        self.initRFVvars(self.botTrnsRb)
        self.checkId(self.botTrnsRb)
        lstPtsConcrSect=[tr_bl,tr_br]
        cover= self.getCoverBottomTransvRF()
        lstCover=[cover]
        if self.botTrnsRb.closedStart or self.botTrnsRb.closedEnd: tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        if self.botTrnsRb.closedStart:
            lstPtsConcrSect.insert(0,tr_tl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.botTrnsRb.closedEnd:
            lstPtsConcrSect.append(tr_tr)
            lstCover.append(self.reinfCfg.cover)
        if self.slopeEdge:
            tr_bl2,tr_br2=self.getYminTransvBottPnts()
            lstPtsConcrSect2=[tr_bl2,tr_br2]
            if self.botTrnsRb.closedStart or self.botTrnsRb.closedEnd: tr_tl2,tr_tr2=self.getYminTransvTopPnts()
            if self.botTrnsRb.closedStart: lstPtsConcrSect2.insert(0,tr_tl2)
            if self.botTrnsRb.closedEnd: lstPtsConcrSect2.append(tr_tr2)
        else:
            lstPtsConcrSect2=None
        self.botTrnsRb.reinfCfg=self.reinfCfg
        self.botTrnsRb.lstPtsConcrSect=lstPtsConcrSect
        self.botTrnsRb.lstPtsConcrSect2=lstPtsConcrSect2
        self.botTrnsRb.lstCover=lstCover
        self.botTrnsRb.rightSideCover=False
        self.botTrnsRb.fromToExtPts=[ln_bl+self.botTrnsRb.distRFstart*vdirLn,ln_br-self.botTrnsRb.distRFend*vdirLn]
        self.botTrnsRb.coverSectBars=cover
        self.botTrnsRb.rightSideSectBars=False
        self.botTrnsRb.createLstRebar()
        self.botTrnsRb.drawPolySectBars()
        self.botTrnsRb.drawLstRebar()

    def drawTopTransvRF(self):
        '''draw and return  the transverse top rebar family'''
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vdirLn=self.getVdirLong()
        self.initRFVvars(self.topTrnsRb)
        self.checkId(self.topTrnsRb)
        lstPtsConcrSect=[tr_tl,tr_tr]
        cover=self.getCoverTopTransvRF()
        lstCover=[cover]
        if self.topTrnsRb.closedStart or self.topTrnsRb.closedEnd: tr_bl,tr_br=self.getYmaxTransvBottPnts()
        if self.topTrnsRb.closedStart:
            lstPtsConcrSect.insert(0,tr_bl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.topTrnsRb.closedEnd:
            lstPtsConcrSect.append(tr_br)
            lstCover.append(self.reinfCfg.cover)
        if self.slopeEdge:
            tr_tl2,tr_tr2=self.getYminTransvTopPnts()
            lstPtsConcrSect2=[tr_tl2,tr_tr2]
            if self.topTrnsRb.closedStart or self.topTrnsRb.closedEnd: tr_bl2,tr_br2=self.getYminTransvBottPnts()
            if self.topTrnsRb.closedStart: lstPtsConcrSect2.insert(0,tr_bl2)
            if self.topTrnsRb.closedEnd: lstPtsConcrSect2.append(tr_br2)
        else:
            lstPtsConcrSect2=None
        self.topTrnsRb.reinfCfg=self.reinfCfg
        self.topTrnsRb.lstPtsConcrSect=lstPtsConcrSect
        self.topTrnsRb.lstPtsConcrSect2=lstPtsConcrSect2
        self.topTrnsRb.rightSideCover=True
        self.topTrnsRb.fromToExtPts=[ln_tl+self.topTrnsRb.distRFstart*vdirLn,ln_tr-self.topTrnsRb.distRFend*vdirLn]
        self.topTrnsRb.coverSectBars=cover
        self.topTrnsRb.lstCover=lstCover
        self.topTrnsRb.rightSideSectBars=True
        self.topTrnsRb.createLstRebar()
        self.topTrnsRb.drawPolySectBars()
        self.topTrnsRb.drawLstRebar()

        
    def drawBottomLongRF(self):
        '''draw and return the  longitudinal bottom rebar family 
        constant length stretch'''
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        vdirTrBott=(tr_br-tr_bl).normalize()
        self.initRFVvars(self.botLnRb)
        self.checkId(self.botLnRb)
        if self.slopeEdge:
            fromExtPt=self.getTransitionBottPnt()
        else:
            fromExtPt=tr_bl+self.botLnRb.distRFstart*vdirTrBott
        lstPtsConcrSect=[ln_bl,ln_br]
        cover=self.getCoverBottomLongRF()
        lstCover=[cover]
        if self.botLnRb.closedStart or self.botLnRb.closedEnd: ln_tl,ln_tr=self.getXmaxLongTopPnts()
        if self.botLnRb.closedStart:
            lstPtsConcrSect.insert(0,ln_tl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.botLnRb.closedEnd:
            lstPtsConcrSect.append(ln_tr)
            lstCover.append(self.reinfCfg.cover)
        self.botLnRb.reinfCfg=self.reinfCfg
        self.botLnRb.lstPtsConcrSect=lstPtsConcrSect
        self.botLnRb.rightSideCover=False
        self.botLnRb.lstCover=lstCover
        self.botLnRb.fromToExtPts=[fromExtPt,tr_br-self.botLnRb.distRFend*vdirTrBott]
        self.botLnRb.coverSectBars=cover
        self.botLnRb.rightSideSectBars=False
        self.botLnRb.createLstRebar()
        self.botLnRb.drawPolySectBars()
        self.botLnRb.drawLstRebar()
    
    def drawTopLongRF(self):
        ''' draw and return the  longitudinal top rebar family'''
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        self.initRFVvars(self.topLnRb)
        self.checkId(self.topLnRb)  
        if self.slopeEdge:
            fromExtPt=self.getTransitionTopPnt()
        else:
            fromExtPt= tr_tl+self.topLnRb.distRFstart*vdirTrTop
        lstPtsConcrSect=[ln_tl,ln_tr]
        cover=self.getCoverTopLongRF()
        lstCover=[cover]
        if self.topLnRb.closedStart or self.topLnRb.closedEnd: ln_bl,ln_br=self.getXmaxLongBottPnts()
        if self.topLnRb.closedStart:
            lstPtsConcrSect.insert(0,ln_bl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.topLnRb.closedEnd:
            lstPtsConcrSect.append(ln_br)
            lstCover.append(self.reinfCfg.cover)
        self.topLnRb.reinfCfg=self.reinfCfg
        self.topLnRb.lstPtsConcrSect=lstPtsConcrSect
        self.topLnRb.rightSideCover=True
        self.topLnRb.lstCover=lstCover
        self.topLnRb.fromToExtPts=[fromExtPt,tr_tr-self.topLnRb.distRFend*vdirTrTop]
        self.topLnRb.coverSectBars=cover
        self.topLnRb.rightSideSectBars=True
        self.topLnRb.createLstRebar()
        self.topLnRb.drawPolySectBars()
        self.topLnRb.drawLstRebar()

    def drawBottomVarLongRF(self):
        '''draw and return the  longitudinal bottom rebar family 
        in the variable length stretch when slopeEdge is defined'''
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        vdirTrBott=(tr_br-tr_bl).normalize()
        vdirLnBott=(ln_br-ln_bl).normalize()
        Lsect2=self.botLnRb.spacing/abs(self.slopeEdge)
        lstPtsConcrSect=[ln_bl,ln_br]
        lstPtsConcrSect2=[ln_bl,ln_bl+Lsect2*vdirLnBott]
        cover=self.getCoverBottomLongRF()
        lstCover=[cover]
        if self.botLnRb.closedStart or self.botLnRb.closedEnd: ln_tl,ln_tr=self.getXmaxLongTopPnts()
        if self.botLnRb.closedStart:
            lstPtsConcrSect.insert(0,ln_tl)
            lstPtsConcrSect2.insert(0,ln_tl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.botLnRb.closedEnd:
            lstPtsConcrSect.append(ln_tr)
            lstPtsConcrSect2.append(ln_tl+Lsect2*vdirLnBott)
            lstCover.append(self.reinfCfg.cover)
        self.botLnRb.reinfCfg=self.reinfCfg
        self.botLnRb.identifier=self.botLnRb.identifier+'v'
        self.botLnRb.lstPtsConcrSect=lstPtsConcrSect
        self.botLnRb.lstPtsConcrSect2=lstPtsConcrSect2
        self.botLnRb.rightSideCover=False
        self.botLnRb.lstCover=lstCover
        self.botLnRb.fromToExtPts=[tr_bl,self.getTransitionBottPnt()]
        self.botLnRb.coverSectBars=cover
        self.botLnRb.rightSideSectBars=False
        self.botLnRb.createLstRebar()
        self.botLnRb.drawPolySectBars()
        self.botLnRb.drawLstRebar()
    
    def drawTopVarLongRF(self):
        ''' draw and return the  longitudinal top rebar family
        in the variable length stretch when slopeEdge is defined'''
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        vdirTrTop=(tr_tr-tr_tl).normalize()
        vdirLnTop=(ln_tr-ln_tl).normalize()
        Lsect2=self.botLnRb.spacing/abs(self.slopeEdge)
        lstPtsConcrSect=[ln_tl,ln_tr]
        lstPtsConcrSect2=[ln_tl,ln_tl+Lsect2*vdirLnTop]
        cover=self.getCoverTopLongRF()
        lstCover=[cover]
        if self.topLnRb.closedStart or self.topLnRb.closedEnd: ln_bl,ln_br=self.getXmaxLongBottPnts()
        if self.topLnRb.closedStart:
            lstPtsConcrSect.insert(0,ln_bl)
            lstPtsConcrSect2.insert(0,ln_bl)
            lstCover.insert(0,self.reinfCfg.cover)
        if self.topLnRb.closedEnd:
            lstPtsConcrSect.append(ln_br)
            lstPtsConcrSect2.append(ln_bl+Lsect2*vdirLnTop)
            lstCover.append(self.reinfCfg.cover)
        self.topLnRb.reinfCfg=self.reinfCfg
        self.topLnRb.identifier=self.topLnRb.identifier+'v'
        self.topLnRb.lstPtsConcrSect=lstPtsConcrSect
        self.topLnRb.lstPtsConcrSect2=lstPtsConcrSect2
        self.topLnRb.rightSideCover=True
        self.topLnRb.lstCover=lstCover
        self.topLnRb.fromToExtPts=[tr_tl,self.getTransitionTopPnt()]
        self.topLnRb.coverSectBars=cover
        self.topLnRb.rightSideSectBars=True
        self.topLnRb.createLstRebar()
        self.topLnRb.drawPolySectBars()
        self.topLnRb.drawLstRebar()
    
    def drawSideXminRF(self):
        ''' Draw and return the side reinforcement in face Xmin'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vDir=(tr_tl-tr_bl).normalize()
        self.initRFVvars(self.sideXminRb)
        self.checkId(self.sideXminRb)
        if not self.sideXminRb.coverSectBars:
            self.sideXminRb.coverSectBars=self.reinfCfg.cover
        self.sideXminRb.reinfCfg=self.reinfCfg
        cover=self.getCoverSideXminRF()
        lstCover=[cover]
        lstPtsConcrSect=[pl_xmin_ymin,pl_xmin_ymax]
        if self.sideXminRb.closedStart:
            lstPtsConcrSect.insert(0,pl_xmax_ymin)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])
            lstCover.insert(0,coverClose)
        if self.sideXminRb.closedEnd:
            lstPtsConcrSect.append(pl_xmax_ymax)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])
            lstCover.append(coverClose)
        self.sideXminRb.lstPtsConcrSect=lstPtsConcrSect
        self.sideXminRb.lstCover=lstCover
        self.sideXminRb.rightSideCover=True
        self.sideXminRb.fromToExtPts=[tr_bl+self.sideXminRb.distRFstart*vDir,tr_tl-self.sideXminRb.distRFend*vDir]
        self.sideXminRb.rightSideSectBars=True
        self.sideXminRb.createLstRebar()
        self.sideXminRb.drawPolySectBars()
        self.sideXminRb.drawLstRebar()
          
    def drawSideXmaxRF(self):
        ''' Draw and return the side refinforcement in face Xmax'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        tr_bl,tr_br=self.getYmaxTransvBottPnts()
        tr_tl,tr_tr=self.getYmaxTransvTopPnts()
        vDir=(tr_tr-tr_br).normalize()
        self.initRFVvars(self.sideXmaxRb)
        self.checkId(self.sideXmaxRb)
        if not self.sideXmaxRb.coverSectBars:
            self.sideXmaxRb.coverSectBars=self.reinfCfg.cover
        self.sideXmaxRb.reinfCfg=self.reinfCfg
        cover=self.getCoverSideXmaxRF()
        lstCover=[cover]
        lstPtsConcrSect=[pl_xmax_ymin,pl_xmax_ymax]
        if self.sideXmaxRb.closedStart:
            lstPtsConcrSect.insert(0,pl_xmin_ymin)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])
            lstCover.insert(0,coverClose)
        if self.sideXmaxRb.closedEnd:
            lstPtsConcrSect.append(pl_xmin_ymax)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botLnRb,self.topLnRb])
            lstCover.append(coverClose)
        self.sideXmaxRb.lstPtsConcrSect=lstPtsConcrSect
        self.sideXmaxRb.lstCover=lstCover
        self.sideXmaxRb.rightSideCover=False
        self.sideXmaxRb.fromToExtPts=[tr_br+self.sideXmaxRb.distRFstart*vDir,tr_tr-self.sideXmaxRb.distRFend*vDir]
        self.sideXmaxRb.rightSideSectBars=False
        self.sideXmaxRb.createLstRebar()
        self.sideXmaxRb.drawPolySectBars()
        self.sideXmaxRb.drawLstRebar()
          
    def drawSideYminRF(self):
        ''' Draw and return the side refinforcement in face Ymin'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vDir=(ln_tl-ln_bl).normalize()
        self.initRFVvars(self.sideYminRb)
        self.checkId(self.sideYminRb)
        if not self.sideYminRb.coverSectBars:
            self.sideYminRb.coverSectBars=self.reinfCfg.cover
        self.sideYminRb.reinfCfg=self.reinfCfg
        cover=self.getCoverSideYminRF()
        lstCover=[cover]
        lstPtsConcrSect=[pl_xmin_ymin,pl_xmax_ymin]
        if self.sideYminRb.closedStart:
            lstPtsConcrSect.insert(0,pl_xmin_ymax)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])
            lstCover.insert(0,coverClose)
        if self.sideYminRb.closedEnd:
            lstPtsConcrSect.append(pl_xmax_ymax)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])
            lstCover.append(coverClose)
        self.sideYminRb.lstPtsConcrSect=lstPtsConcrSect
        self.sideYminRb.lstCover=lstCover
        self.sideYminRb.rightSideCover=False
        self.sideYminRb.fromToExtPts=[ln_bl+self.sideYminRb.distRFstart*vDir,ln_tl-self.sideYminRb.distRFend*vDir]
        self.sideYminRb.rightSideSectBars=True
        self.sideYminRb.createLstRebar()
        self.sideYminRb.drawPolySectBars()
        self.sideYminRb.drawLstRebar()
          
    def drawSideYmaxRF(self):
        ''' Draw and return the side refinforcement in face Ymax'''
        pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
        ln_bl,ln_br=self.getXmaxLongBottPnts()
        ln_tl,ln_tr=self.getXmaxLongTopPnts()
        vDir=(ln_tr-ln_br).normalize()
        self.initRFVvars(self.sideYmaxRb)
        self.checkId(self.sideYmaxRb)
        if not self.sideYmaxRb.coverSectBars:
            self.sideYmaxRb.coverSectBars=self.reinfCfg.cover
        self.sideYmaxRb.reinfCfg=self.reinfCfg
        cover=self.getCoverSideYmaxRF()
        lstCover=[cover]
        lstPtsConcrSect=[pl_xmin_ymax,pl_xmax_ymax]
        if self.sideYmaxRb.closedStart:
            lstPtsConcrSect.insert(0,pl_xmin_ymin)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])
            lstCover.insert(0,coverClose)
        if self.sideYmaxRb.closedEnd:
            lstPtsConcrSect.append(pl_xmax_ymin)
            coverClose=self.reinfCfg.cover+self.getMaxDiameter([self.botTrnsRb,self.topTrnsRb])
            lstCover.append(coverClose)
        self.sideYmaxRb.lstPtsConcrSect=lstPtsConcrSect
        self.sideYmaxRb.lstCover=lstCover
        self.sideYmaxRb.rightSideCover=True
        self.sideYmaxRb.fromToExtPts=[ln_br+self.sideYmaxRb.distRFstart*vDir,ln_tr-self.sideYmaxRb.distRFend*vDir]
        self.sideYmaxRb.rightSideSectBars=False
        self.sideYmaxRb.createLstRebar()
        self.sideYmaxRb.drawPolySectBars()
        self.sideYmaxRb.drawLstRebar()
          
    def drawStirrHoldingTransvSF(self):
        ''' Draw and retrurn the stirrup family that  holds the transverse top and bottom rebar families '''
        ln_bl,ln_br=self.getXminLongBottPnts()
        ln_tl,ln_tr=self.getXminLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        vdirTr=self.getVdirTransv()
        vdirLn=self.getVdirLong()
        lst_hold_tr_sf=list()
        for stirrHoldTrReinf in self.lstStirrHoldTrReinf:
            self.checkId(stirrHoldTrReinf)
            bStirr=stirrHoldTrReinf.widthStirr+stirrHoldTrReinf.diameter
            coverStirr=self.reinfCfg.cover+stirrHoldTrReinf.addCover
            if stirrHoldTrReinf.dispRealSh<0: # stirrups rigth towards left
                lstPtsConcrSect=[ln_br,ln_br-bStirr*vdirLn,ln_tr-bStirr*vdirLn,ln_tr,ln_br]
            else: # stirrups left towards right
                lstPtsConcrSect=[ln_bl,ln_bl+bStirr*vdirLn,ln_tl+bStirr*vdirLn,ln_tl,ln_bl]
            if stirrHoldTrReinf.dispPerp<0: # stirrups rigth towards left
                lstPtsConcrLong=[tr_tr,tr_br]
                vDirLong=-1*vdirTr
            else:
                lstPtsConcrLong=[tr_tl,tr_bl]
                vDirLong=vdirTr
            self.checkId(stirrHoldTrReinf)
            stirrHoldTrReinf.reinfCfg=self.reinfCfg
            stirrHoldTrReinf.lstPtsConcrSect=lstPtsConcrSect
            stirrHoldTrReinf.lstCover=[coverStirr,0,coverStirr,0]
            stirrHoldTrReinf.lstPtsConcrLong=lstPtsConcrLong
            stirrHoldTrReinf.vDirLong=vDirLong
            stirrHoldTrReinf.drawPolyRebars()
            stirrHoldTrReinf.drawLnRebars()
            lst_hold_tr_sf+=[stirrHoldTrReinf]
        return lst_hold_tr_sf
        
        
    def drawStirrHoldingLongSF(self):
        ''' Draw and return the stirrup family  that holds the longitudinal top and bottom rebar families'''
        ln_bl,ln_br=self.getXminLongBottPnts()
        ln_tl,ln_tr=self.getXminLongTopPnts()
        tr_tl,tr_tr=self.getYminTransvTopPnts()
        tr_bl,tr_br=self.getYminTransvBottPnts()
        vdirTr=self.getVdirTransv()
        vdirLn=self.getVdirLong()
        lst_hold_ln_sf=list()
        for stirrHoldLnReinf in self.lstStirrHoldLnReinf:
            self.checkId(stirrHoldLnReinf)
            bStirr=stirrHoldLnReinf.widthStirr+stirrHoldLnReinf.diameter
            if stirrHoldLnReinf.dispRealSh<0: # stirrups rigth towards left
                lstPtsConcrSect=[tr_br,tr_br-bStirr*vdirTr,tr_tr-bStirr*vdirTr,tr_tr,tr_br]
            else: # stirrups left towards right
                lstPtsConcrSect=[tr_bl,tr_bl+bStirr*vdirTr,tr_tl+bStirr*vdirTr,tr_tl,tr_bl]
            if stirrHoldLnReinf.dispPerp<0: # stirrups rigth towards left
                lstPtsConcrLong=[ln_tr,ln_br]
                vDirLong=-1*vdirLn
            else:
                lstPtsConcrLong=[ln_tl,ln_bl]
                vDirLong=vdirLn
            stirrTopCover=self.getCoverTopLongRF()-stirrHoldLnReinf.diameter+stirrHoldLnReinf.addCover
            stirrBottCover=self.getCoverBottomLongRF()-stirrHoldLnReinf.diameter+stirrHoldLnReinf.addCover
            stirrHoldLnReinf.reinfCfg=self.reinfCfg
            stirrHoldLnReinf.lstPtsConcrSect=lstPtsConcrSect
            stirrHoldLnReinf.lstCover=[stirrBottCover,0,stirrTopCover,0]
            stirrHoldLnReinf.lstPtsConcrLong=lstPtsConcrLong
            stirrHoldLnReinf.vDirLong=vDirLong
            stirrHoldLnReinf.drawPolyRebars()
            stirrHoldLnReinf.drawLnRebars()
            lst_hold_ln_sf+=[stirrHoldLnReinf]
        return lst_hold_ln_sf

    def drawTransvConcrSectYmax(self):
        ''' Draw concrete transverse cross-section
        placed at maximum Y coordinate'''
        if self.drawConcrTrSect:
            tr_tl,tr_tr=self.getYmaxTransvTopPnts()
            tr_bl,tr_br=self.getYmaxTransvBottPnts()
            lstPnts=[tr_bl,tr_tl,tr_tr,tr_br,tr_bl]
            lstEdges=[] if self.drawConcrTrSect == True else self.drawConcrTrSect
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)

    def drawTransvConcrSectYmin(self):
        ''' Draw concrete transverse cross-section
        placed at minimum Y coordinate'''
        if self.drawConcrTrSect:
            tr_tl,tr_tr=self.getYminTransvTopPnts()
            tr_bl,tr_br=self.getYminTransvBottPnts()
            lstPnts=[tr_bl,tr_tl,tr_tr,tr_br,tr_bl]
            lstEdges=[] if self.drawConcrTrSect == True else self.drawConcrTrSect
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)

    def drawLongConcrSectXmin(self):
        ''' Draw the concrete longitudinal section at minimum X coordinate'''
        if self.drawConcrLnSect:
            minXln_bl,minXln_br=self.getXminLongBottPnts()
            minXln_tl,minXln_tr=self.getXminLongTopPnts()
            lstPnts=[minXln_bl,minXln_tl,minXln_tr,minXln_br,minXln_bl]
            lstEdges=[] if self.drawConcrLnSect == True else self.drawConcrLnSect
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)
      
    def drawLongConcrSectXmax(self):
        ''' Draw the concrete longitudinal section at maximum X coordinate'''
        if self.drawConcrLnSect:
            maxXln_bl,maxXln_br=self.getXmaxLongBottPnts()
            maxXln_tl,maxXln_tr=self.getXmaxLongTopPnts()
            lstPnts=[maxXln_bl,maxXln_tl,maxXln_tr,maxXln_br,maxXln_bl]
            lstEdges=[] if self.drawConcrLnSect == True else self.drawConcrLnSect
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)

    def drawPlanConcrView(self):
        " Draw the concrete plan view (usually used when side reinforcement is defined) "
        if self.drawPlan:
            pl_xmin_ymin,pl_xmax_ymin,pl_xmax_ymax,pl_xmin_ymax=self.getPntsPlan()
            lstPnts=[pl_xmin_ymin,pl_xmin_ymax,pl_xmax_ymax,pl_xmax_ymin,pl_xmin_ymin]
            lstEdges=[] if self.drawPlan == True else self.drawPlan
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)

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
    :param botTrnsRb: data for bottom transverse rebar family expressed as instance of brkRbFam class
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as  instance of brkRbFam class
    :param sideXmaxRb: same for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: same for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: same for side reinforcement in face Ymax (defaults to None)
    :param lstStirrHoldTrReinf: list of stirrHoldTrReinfs expressed as instances of brkStirrFam class. Each one is the data 
           for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs expressed as instances of brkStirrFam class. Each one is the data 
           for a stirrup rebar family that holds longitudinal top and bottom rebar families
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) 
           (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
           (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,lstStirrHoldTrReinf=lstStirrHoldTrReinf,lstStirrHoldLnReinf=lstStirrHoldLnReinf,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    if botTrnsRb:
        brick.drawBottomTransvRF()
        lstRebFam+=[brick.botTrnsRb]
    if topTrnsRb:
        brick.drawTopTransvRF()
        lstRebFam+=[brick.topTrnsRb]
    if botLnRb:
        brick.drawBottomLongRF()
        lstRebFam+=[brick.botLnRb]
    if topLnRb:
        brick.drawTopLongRF()
        lstRebFam+=[brick.topLnRb]
    if sideXminRb:
        brick.drawSideXminRF()
        lstRebFam+=[brick.sideXminRb]
    if sideXmaxRb:
        brick.drawSideXmaxRF()
        lstRebFam+=[brick.sideXmaxRb]
    if sideYminRb:
        brick.drawSideYminRF()
        lstRebFam+=[brick.sideYminRb]
    if sideYmaxRb:
        brick.drawSideYmaxRF()
        lstRebFam+=[brick.sideYmaxRb]
    if lstStirrHoldTrReinf:
        lstStirrFam+=brick.drawStirrHoldingTransvSF()
    if lstStirrHoldLnReinf:
        lstStirrFam+=brick.drawStirrHoldingLongSF()
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
    :param botTrnsRb: data for bottom transverse rebar family expressed as instance of brkRbFam class
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as  instance of brkRbFam class
    :param sideXmaxRb: same for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: same for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: same for side reinforcement in face Ymax (defaults to None)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :param trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
     :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) 
           (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
           (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    if botTrnsRb:
        brick.drawBottomTransvRF()
        lstRebFam+=[brick.botTrnsRb]
    if topTrnsRb:
        brick.drawTopTransvRF()
        lstRebFam+=[brick.topTrnsRb]
    if botLnRb:
        brick.drawBottomLongRF()
        lstRebFam+=[brick.botLnRb]
    if topLnRb:
        brick.drawTopLongRF()
        lstRebFam+=[brick.topLnRb]
    if sideXminRb:
        brick.drawSideXminRF()
        lstRebFam+=[brick.sideXminRb]
    if sideXmaxRb:
        brick.drawSideXmaxRF()
        lstRebFam+=[brick.sideXmaxRb]
    if sideYminRb:
        brick.drawSideYminRF()
        lstRebFam+=[brick.sideYminRb]
    if sideYmaxRb:
        brick.drawSideYmaxRF()
        lstRebFam+=[brick.sideYmaxRb]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawLongConcrSectXmax()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def sloped_edge_constant_thickness_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,minSlope2varHorRF=4e-2,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,lstStirrHoldTrReinf=None,lstStirrHoldLnReinf=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param botTrnsRb: data for bottom transverse rebar family expressed as instance of brkRbFam class
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as  instance of brkRbFam class
    :param sideXmaxRb: same for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: same for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: same for side reinforcement in face Ymax (defaults to None)
    :param lstStirrHoldTrReinf: list of stirrHoldTrReinfs expressed as instances of brkStirrFam
           class. Each one is the data for a stirrup rebar familiy that holds transverse top
           and bottom rebar families. Real shape is depicted in the longitudinal section
           (defaults to [])
    :param lstStirrHoldLnReinf: list of stirrHoldLnReinfs expressed as instances of brkStirrFam
           class. Each one is the data for a stirrup rebar family that holds longitudinal top
           and bottom rebar families (defaults to [])
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list
           of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param drawConcrTrSect: True to draw the transverse concrete cross-section  (defaults to True)
    :param drawConcrLnSect: True to draw the longitudinal concrete cross-section  (defaults to True)
    :param slopeEdge: slope of the edge of minimum X-cood (deltaY/deltaX)
    :param minSlope2varHorRF: minimum slope of the edge to draw variable horizontal reinforcement (defaults to 4%)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) 
           (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
           (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,lstStirrHoldTrReinf=lstStirrHoldTrReinf,lstStirrHoldLnReinf=lstStirrHoldLnReinf,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId,)
    if botTrnsRb:
        brick.drawBottomTransvRF()
        lstRebFam+=[brick.botTrnsRb]
    if topTrnsRb:
        brick.drawTopTransvRF()
        lstRebFam+=[brick.topTrnsRb]
    if botLnRb:
        brick.drawBottomLongRF()
        lstRebFam+=[brick.botLnRb]
        if slopeEdge > minSlope2varHorRF:
            brick.drawBottomVarLongRF()
            lstRebFam+=[brick.botLnRb]
    if topLnRb:
        brick.drawTopLongRF()
        lstRebFam+=[brick.topLnRb]
        if slopeEdge > minSlope2varHorRF:
            brick.drawTopVarLongRF()
            lstRebFam+=[brick.topLnRb]
    if sideXminRb:
        brick.drawSideXminRF()
        lstRebFam+=[brick.sideXminRb]
    if sideXmaxRb:
        brick.drawSideXmaxRF()
        lstRebFam+=[brick.sideXmaxRb]
    if sideYminRb:
        brick.drawSideYminRF()
        lstRebFam+=[brick.sideYminRb]
    if sideYmaxRb:
        brick.drawSideYmaxRF()
        lstRebFam+=[brick.sideYmaxRb]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if lstStirrHoldTrReinf:
        lstStirrFam+=brick.drawStirrHoldingTransvSF()
    if lstStirrHoldLnReinf:
        lstStirrFam+=brick.drawStirrHoldingLongSF()
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawLongConcrSectXmax()
        else:
            brick.drawLongConcrSectXmin()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def sloped_edge_sloped_faces_brick_reinf(width,length,thickness,anchPtTrnsSect,anchPtLnSect,reinfCfg,slopeEdge,minSlope2varHorRF=4e-2,trSlopeBottFace=None,trSlopeTopFace=None,angTrns=0,angLn=0,botTrnsRb=None,topTrnsRb=None,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,sideYminRb=None,sideYmaxRb=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1):
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
    :param minSlope2varHorRF: minimum slope of the edge to draw variable horizontal reinforcement (defaults to 4%)
    :param trSlopeBottFace: transverse slope of the brick bottom-face (deltaZ/deltaX)
    :param trSlopeTopFace: transverse slope of the brick top-face (deltaZ/deltaX)
    :param angTrns: angle (degrees) between the horizontal and the brick width dim    :param angLn: angle (degrees) between the horizontal and the brick length dimension
    :param botTrnsRb: data for bottom transverse rebar family expressed as instance of brkRbFam class
    :param topTrnsRb: same for the top transverse rebar family
    :param botLnRb: same for the bottom longitudinal rebar family
    :param topLnRb: same for the top longitudinal rebar family
    :param sideXminRb: data for side reinforcement in face Xmin  (defaults to None), expressed as  instance of brkRbFam class
    :param sideXmaxRb: same for side reinforcement in face Xmax (defaults to None)
    :param sideYminRb: same for side reinforcement in face Ymin (defaults to None)
    :param sideYmaxRb: same for side reinforcement in face Ymax (defaults to None)
    :param drawConcrTrSect: True if the concrete transverse cross-section is drawn (defaults to True)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) 
           (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
           (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
     '''
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    brick=genericBrickReinf(width=width,length=length,thickness=thickness,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botTrnsRb=botTrnsRb,topTrnsRb=topTrnsRb,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,sideYminRb=sideYminRb,sideYmaxRb=sideYmaxRb,trSlopeBottFace=trSlopeBottFace,trSlopeTopFace=trSlopeTopFace,slopeEdge=slopeEdge,drawConcrTrSect=drawConcrTrSect,drawConcrLnSect=drawConcrLnSect,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    if botTrnsRb:
        brick.drawBottomTransvRF()
        lstRebFam+=[brick.botTrnsRb]
    if topTrnsRb:
        brick.drawTopTransvRF()
        lstRebFam+=[brick.topTrnsRb]
    if botLnRb:
        brick.drawBottomLongRF()
        lstRebFam+=[brick.botLnRb]
        if slopeEdge > minSlope2varHorRF:
            brick.drawBottomVarLongRF()
            lstRebFam+=[brick.botLnRb]
    if topLnRb:
        brick.drawTopLongRF()
        lstRebFam+=[brick.topLnRb]
        if slopeEdge > minSlope2varHorRF:
            brick.drawTopVarLongRF()
            lstRebFam+=[brick.topLnRb]
    if drawConcrTrSect:
        brick.drawTransvConcrSectYmax()
    if sideXminRb:
        brick.drawSideXminRF()
        lstRebFam+=[brick.sideXminRb]
    if sideXmaxRb:
        brick.drawSideXmaxRF()
        lstRebFam+=[brick.sideXmaxRb]
    if sideYminRb:
        brick.drawSideYminRF()
        lstRebFam+=[brick.sideYminRb]
    if sideYmaxRb:
        brick.drawSideYmaxRF()
        lstRebFam+=[brick.sideYmaxRb]
    if drawConcrLnSect:
        if slopeEdge>0:
            brick.drawLongConcrSectXmax()
        else:
            brick.drawLongConcrSectXmin()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId

def quad_beam_reinf(width,height,length,anchPtTrnsSect,anchPtLnSect,reinfCfg,angTrns=0,angLn=0,lstBotRb=[],lstTopRb=[],lstLeftLatlRb=[],lstRightLatlRb=[],lstStirrReinf=None,drawConcrTrSect=True,drawConcrLnSect=True,anchPtPlan=None,angPlan=0,drawPlan=False,startId=1,clearDistRbLayers=None,aggrSize=20e-3):
    '''Typical reinforcement arrangement of a rectangular cross-section beam (or column)
    Nomenclature: b-bottom, t-top, l-left, r-right, tr-transverse, ln-longitudinal
                  RF-rebar family, SF-stirrup family, Ly: layer of rebars

    :param width: beam cross-section width
    :param height: beam cross-section height
    :param length: beam length
    :param anchPtTrnsSect: anchor point to place the bottom left corner of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal cross-section
    :param reinfCfg: instance of the cfg.reinfConf class
    :param angTrns: angle (degrees) between the horizontal and the cross-section width dimension
    :param angLn: angle (degrees) between the horizontal and the length dimension
    :param lstBotRb: list of data for bottom rebar layers expressed as instances of brkRbFam class. Each element of 
           the list represents a layer of rebars (first element is the outermost) (defaults to [])
    :paramlstTopRb: same for the top rebar layers
    :param lstLeftLatlRb: same for the lateral rebar layers in the left side of the cross-section
    :param lstRigthtLatlRb: ame for the lateral rebar layers in the right side of the cross-section
    :param lstStirrReinf: list of stirrup families expressed as instances of brkStirrFam class. Each one is the data 
           for a stirrup rebar familiy that holds transverse top and bottom rebar families. Real shape is depicted in the longitudinal section
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn or a list of edges (e.g. [2,4] if only second and fourth edges are drawn)  
           (defaults to True)
    :param anchPtPlan: anchor point to place the (xmin,ymin) point of the plan drawing (in general, the plan drawing is only used when defining side reinforcement) 
           (defaults to None)
    :param angPlan:  angle (degrees) between the horizontal and the plan view (defaults to 0)
    :param drawPlan: True if the closed concrete plan view is drawn or   a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
           (anchPtPlan must be defined) (defaults to False)
    :param startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    :param clearDistRbLayers: clear (horizontal and vertical) distance (in m) between layers of parallel bars. Defaults to None,
                            in which case this distance is calculated in function of the maximum aggregate size and the maximum 
                            diameter of the defined families of rebars  
    :param aggrSize: maximum aggregate size (in m) (used to calculate the clear distance between rebar layers (if not defined by parameter clearDistRebars)
    '''
    initCover=reinfCfg.cover
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    allRF=lstBotRb+lstTopRb+lstLeftLatlRb+lstRightLatlRb
    if len(allRF)==0: # only stirrups or nothing
        brick=genericBrickReinf(width=width,length=length,thickness=height,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botLnRb=None,topLnRb=None,sideXminRb=None,sideXmaxRb=None,lstStirrHoldLnReinf=lstStirrReinf,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
    else:
        if not(clearDistRbLayers):
            # maximum rebar diameter
            fisRb=[rb.diameter for rb in allRF]
            maxFi=max(fisRb)
            clearDistRbLayers=reinfCfg.getMinClearDistRebars(maxFi,aggrSize)
       # maximum dimension of the list of rebar layers
        maxNlayers=max(len(lstBotRb),len(lstTopRb),len(lstLeftLatlRb),len(lstRightLatlRb))
        # make the four lists of the maximum dimension
        lstBotRb+=(maxNlayers-len(lstBotRb))*[None]
        lstTopRb+=(maxNlayers-len(lstTopRb))*[None]
        lstLeftLatlRb+=(maxNlayers-len(lstLeftLatlRb))*[None]
        lstRightLatlRb+=(maxNlayers-len(lstRightLatlRb))*[None]
        if lstStirrReinf and len(lstStirrReinf)>0:
            maxFiStirr=max([rb.diameter for rb in lstStirrReinf])
            reinfCfg.cover=reinfCfg.cover+maxFiStirr
        # init lateral cover if not defined
        for rb in allRF:
            if not rb.lateralCover: rb.lateralCover=reinfCfg.cover
        for ly in range(maxNlayers):
            botLnRb=lstBotRb[ly]
            topLnRb=lstTopRb[ly]
            sideXminRb=lstLeftLatlRb[ly]
            sideXmaxRb=lstRightLatlRb[ly]
            brick=genericBrickReinf(width=width,length=length,thickness=height,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect, reinfCfg=reinfCfg,angTrns=angTrns,angLn=angLn,botLnRb=botLnRb,topLnRb=topLnRb,sideXminRb=sideXminRb,sideXmaxRb=sideXmaxRb,lstStirrHoldLnReinf=lstStirrReinf,anchPtPlan=anchPtPlan,angPlan=angPlan,drawPlan=drawPlan,startId=startId)
            if botLnRb:
                brick.drawBottomLongRF()
                lstRebFam+=[brick.botLnRb]
            if topLnRb:
                brick.drawTopLongRF()
                lstRebFam+=[brick.topLnRb]
            if sideXminRb:
                brick.drawSideXminRF()
                lstRebFam+=[brick.sideXminRb]
            if sideXmaxRb:
                brick.drawSideXmaxRF()
                lstRebFam+=[brick.sideXmaxRb]
            #if lstStirrReinf:
            #    lstStirrFam+=brick.drawStirrHoldingTransvSF()
            fisRb=[rb.diameter for rb in [botLnRb,topLnRb,sideXminRb,sideXmaxRb] if rb]
            # add cover for the next layer
            reinfCfg.cover=reinfCfg.cover+max(fisRb)+clearDistRbLayers
    reinfCfg.cover=initCover # revert cover to the the value defined in config 
    if lstStirrReinf:
        lstStirrFam+=brick.drawStirrHoldingLongSF()
    if drawConcrTrSect:     # 
        brick.drawTransvConcrSectYmax()
    if drawConcrLnSect:
        brick.drawLongConcrSectXmax()
    if drawPlan:
        brick.drawPlanConcrView()
    FreeCAD.ActiveDocument.recompute()
    return lstRebFam,lstStirrFam,brick.startId
    
class genericCylReinf(genericReinfBase):
    '''Typical reinforcement arrangement of cylindrical member

    :ivar radius: radius of the cylinder cross-section
    :ivar length: cylinder length
    :ivar anchPtTrnsSect: anchor point to place the center of the concrete transverse cross-section
    :ivar anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal section
    :param reinfCfg: instance of the cfg.reinfConf class
    :ivar angLn: angle (degrees) between the horizontal and the brick length dimension 
    :ivar lnRb: data for the longitudinal rebar family expressed as instance of brkRbFam class (defaults to None
    :ivar lstStirrReinf: list of stirr families expressed as instances of brkStirrFam class (defaults to None)
    :ivar drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn. 
          Also can be a list of edges (e.g. [2,4] if only second and fourth edges are drawn) (defaults to True)
    :ivar startId: integer to successively identify the reinforcement families created for which their identifier has not been defined or it is None (defaults to 1)
    '''
    def __init__(self,radius,length,anchPtTrnsSect,anchPtLnSect,reinfCfg,angLn=0,lnRb=None,lstStirrReinf=None,drawConcrLnSect=True,startId=1):
        super(genericCylReinf,self).__init__(length=length,thickness=2*radius,angLn=angLn,anchPtLnSect=anchPtLnSect,startId=startId)
        self.radius=radius
        self.anchPtTrnsSect=anchPtTrnsSect+Vector(0,radius)
        self.reinfCfg=reinfCfg
        self.angLn=angLn
        self.lnRb=lnRb
        self.lstStirrReinf=lstStirrReinf
        self.drawConcrLnSect=drawConcrLnSect

    def getMaxStirrDiam(self):
        ''' Return the maximum diameter of the stirrup families'''
        fiMax=self.getMaxDiameter(self.lstStirrReinf)
        return fiMax
    
    def drawLnRF(self):
        ln_bl,ln_br=self.getSimplLongBottPnts()
        vdirTrBott=(ln_br-ln_bl).normalize()
        self.initRFVvars(self.lnRb)
        self.checkId(self.lnRb)
        self.lnRb.reinfCfg=self.reinfCfg
        self.lnRb.lstPtsConcrSect=[ln_bl,ln_br]
        self.lnRb.lstCover=[self.radius-self.lnRb.diameter/2]
        self.lnRb.rightSideCover=False
        self.lnRb.sectBarsConcrRadius=self.radius
        self.lnRb.rightSideSectBars=True
        self.lnRb.coverSectBars=self.reinfCfg.cover+self.getMaxStirrDiam()
        self.lnRb.createLstRebar()
        self.lnRb.drawCircSectBars(vTranslation=self.anchPtTrnsSect)
        self.lnRb.drawLstRebar()

    def drawStirrF(self):
        ln_bl,ln_br=self.getSimplLongBottPnts()
        ln_tl,ln_tr=self.getSimplLongTopPnts()
        vDirLong=(ln_br-ln_bl).normalize()
        lst_stirr=list()
        for stirrF in self.lstStirrReinf:
            self.checkId(stirrF)
            stirrF.reinfCfg=self.reinfCfg
            stirrF.lstPtsConcrSect=None
            stirrF.concrSectRadius=self.radius
            stirrF.lstPtsConcrLong=[ln_bl,ln_tl]
            stirrF.nmbStrpTransv=1
            stirrF.lstCover=[self.reinfCfg.cover]
            stirrF.vDirLong=vDirLong
            stirrF.drawCircRebar(vTranslation=self.anchPtTrnsSect)
            stirrF.drawLnRebars()
            lst_stirr+=[stirrF]
        return lst_stirr

    def drawTransvConcrSect(self):
        rb.drawCircConcreteSection(radiusConcrSect=self.radius,vTranslation=self.anchPtTrnsSect)

    def drawLongConcrSect(self):
        ''' Draw the concrete longitudinal section'''
        if self.drawConcrLnSect:
            ln_bl,ln_br=self.getSimplLongBottPnts()
            ln_tl,ln_tr=self.getSimplLongTopPnts()
            lstPnts=[ln_bl,ln_tl,ln_tr,ln_br,ln_bl]
            lstEdges=[] if self.drawConcrLnSect==True else self.drawConcrLnSect
            rb.drawConcreteSection(lstPnts,lstEdges=lstEdges)
        
def cyl_beam_reinf(radius,length,anchPtTrnsSect,anchPtLnSect,reinfCfg,angLn=0,lstLnRb=[],lstStirrReinf=None,drawConcrTrSect=True,drawConcrLnSect=True,startId=1,clearDistRbLayers=None,aggrSize=20e-3):
    '''Typical reinforcement arrangement of a cylindrical cross-section beam (or column)
    :param radius: radius of the cylinder cross-section
    :param length: cylinder length
    :param anchPtTrnsSect: anchor point to place the center of the concrete transverse cross-section
    :param anchPtLnSect:  anchor point to place the bottom left corner of the concrete longitudinal 
           section
    :param reinfCfg: instance of the cfg.reinfConf class
    :param angLn: angle (degrees) between the horizontal and the brick length dimension 
    :param lstLnRb: list of data for the longitudinal rebar familyiesexpressed as instances 
           of brkRbFam class Each element of  the list represents a layer of rebars 
           (first element is the outermost) (defaults to [])
    :param lstStirrReinf: list of stirr families expressed as instances of brkStirrFam class 
           (defaults to None)
    :param drawConcrTrSect: True if the concrete circular cross-section is drawn. 
          (defaults to True)
    :param drawConcrLnSect: True if a closed concrete longitudinal cross-section is drawn. 
          Also can be a list of edges (e.g. [2,4] if only second and fourth edges are drawn) 
          (defaults to True)
    :param startId: integer to successively identify the reinforcement families created for 
           which their identifier has not been defined or it is None (defaults to 1)
    :param clearDistRbLayers: clear (horizontal and vertical) distance (in m) between layers 
           of parallel bars. Defaults to None, in which case this distance is calculated 
           in function of the maximum aggregate size and the maximum diameter of the defined 
           families of rebars  
    :param aggrSize: maximum aggregate size (in m) (used to calculate the clear distance 
           between rebar layers (if not defined by parameter clearDistRebars)
    '''
    initCover=reinfCfg.cover
    lstRebFam=list(); lstStirrFam=list() # Families of rebars
    # Check identifiers
    for rb in lstLnRb+lstStirrReinf:
        if not rb.identifier:
            rb.identifier=str(startId)
            startId+=1
    if lstStirrReinf and len(lstStirrReinf)>0: # Draw stirrups
        cyl=genericCylReinf(radius=radius,length=length,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect,reinfCfg=reinfCfg,angLn=angLn,lnRb=None,lstStirrReinf=lstStirrReinf,startId=startId)
        lstStirrFam+=cyl.drawStirrF()
        maxFiStirr=cyl.getMaxDiameter(lstStirrReinf)
        reinfCfg.cover=reinfCfg.cover+maxFiStirr
    if len(lstLnRb)>0:
        if not(clearDistRbLayers):
            maxFi=cyl.getMaxDiameter(lstLnRb)
            clearDistRbLayers=reinfCfg.getMinClearDistRebars(maxFi,aggrSize)
        for layer in range(len(lstLnRb)):
            lnRb=lstLnRb[layer]
            cyl=genericCylReinf(radius=radius,length=length,anchPtTrnsSect=anchPtTrnsSect,anchPtLnSect=anchPtLnSect,reinfCfg=reinfCfg,angLn=angLn,lnRb=lnRb,lstStirrReinf=None,drawConcrLnSect=drawConcrLnSect,startId=startId)
            cyl.checkId(lnRb)
            cyl.drawLnRF()
            reinfCfg.cover=reinfCfg.cover+lnRb.diameter+clearDistRbLayers
            lstRebFam+=[lnRb]
    if drawConcrTrSect:
        cyl.drawTransvConcrSect()
    if drawConcrLnSect:
        cyl.drawLongConcrSect()
    return lstRebFam,lstStirrFam,startId
            
    

