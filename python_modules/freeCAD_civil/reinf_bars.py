# -*- coding: iso-8859-1 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2017, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

import math
import bisect
import Part, FreeCAD
import Draft
from FreeCAD import Vector
import FreeCADGui
from FreeCAD import Gui
from freeCAD_utils import geom_utils
from freeCAD_utils import drawing_tools as dt
from RC_utils import reinf_bars_arrang_sets as RCutils
import DraftVecUtils
from materials.ec2 import EC2_limit_state_checking as Lcalc
from misc_utils import data_struct_utils as dsu
from freeCAD_civil import draw_config as cfg
from freeCAD_civil import tables
from misc_utils import log_messages as lmsg
from layout_utils import dimensioning as dim

'''Classes to generate in FreeCAD drawings to represent  a reinforced-concrete 
structure and the bar schedule associated.

Diameter of the reinforcement bars must be expressed in meters [m].
Other length magnitudes should be expressed in meters [m].
'''


class rebarFamilyBase(object):
    ''' Base class for families of reinforcement bars

    :ivar reinfCfg: instance of th class reinfConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bars of the family [m]
    :ivar lstPtsConcrSect: list of points in the concrete section to which 
          the bar is 'attached'
     :ivar lstCover: list of covers that correspond to each of the segments 
          defined with lstPtsConcrSect [m]. Defaults to the minimum cover 
          defined with 'reinfCfg'
    :ivar rightSideCover: side to give cover  (False: left side, True for right side)
          (defaults to True)
    '''
    def __init__(self,reinfCfg,identifier,diameter,lstPtsConcrSect,lstCover=None,rightSideCover=True):
        self.reinfCfg=reinfCfg
        self.identifier=identifier
        self.diameter=diameter
        self.lstPtsConcrSect=lstPtsConcrSect
        if lstCover is None:
            if lstPtsConcrSect:
                self.lstCover=(len(lstPtsConcrSect)-1)*[reinfCfg.cover]
            else:
                self.lstCover=[reinfCfg.cover]
        else:
            self.lstCover= lstCover
        self.rightSideCover=rightSideCover
 
    def getNextLstCover(self):
        '''Return the list of covers for a rebar family that is tangent to the internal face of this family
        '''
        lstNextCover=[c+self.diametre for c in self.lstCover]
        return lstNextCover
    
    def getLstPtsBasicRebar(self,lstPtsConcr):
        '''Return the wire that represents the true shape of the bar defined
        by the points of the concrete section listed in lstPtsConcr.

        :param lstPtsConcr: ordered list of points in the concrete section 
        to which the rebar is 'attached'. 
        '''
        npuntos=len(lstPtsConcr)
        lstPtosAux=[pt for pt in lstPtsConcr]
        # Shape of the main rebar (without gaps, straight elongation, hooks, ...
        listaaux=[]
        npuntos=len(lstPtosAux)
        for i in range (0,npuntos-1):
            vaux=lstPtosAux[i+1].sub(lstPtosAux[i])
            if self.rightSideCover:
                vauxn=Vector(vaux.y,-vaux.x)
            else:
                vauxn=Vector(-vaux.y,vaux.x)
            vauxn.normalize()
            vauxn.multiply(self.lstCover[i]+self.diameter/2.0)
            listaaux.append(lstPtosAux[i].add(vauxn))
            listaaux.append(lstPtosAux[i+1].add(vauxn))

        lstPtsRebar=[listaaux[0]]
        for i in range (1,npuntos-1):
            pint=geom_utils.int2lines(listaaux[2*(i-1)],listaaux[2*(i-1)+1],listaaux[2*i],listaaux[2*i+1])
            lstPtsRebar.append(pint)

        lstPtsRebar.append(listaaux[2*(npuntos-1)-1])
        return lstPtsRebar
        
    def getExtrShapeParams(self,rbEndStrDef):
        '''For extremity rebar shapes 'anc' (anchor) or 'lap' (lapped bars), return 
        the angle that forms with the main rebar, and the length of anchoring or lapping [m]
        '''
        paramAnc=rbEndStrDef.split('_')
        rbEndType=paramAnc[0][:3]
        angle=eval(paramAnc[0][3:])
        if abs(angle-180)<0.1:
            angle=0
        if rbEndType in ['anc','lap']:    
            stress=paramAnc[2]
            compression= True if (stress in 'compr') else False
            pos=paramAnc[1].replace('pos','').lower()
            if pos=='good':
                eta1=1.0
            elif pos=='poor':
                eta1=0.7
            else:
                print('rebar familly ', self.identifier,' must be in "good" or "poor" position')
            contrReb=Lcalc.RebarController(concreteCover=self.reinfCfg.cover, spacing=self.spacing, eta1=eta1, compression= compression) # create rebar controllers to calculate anchor or gap lengths
        elif rbEndType in ['fix']:
            rbEndLenght=eval(paramAnc[1].replace('len',''))/1000 # longitud en metros
        else:
            print('rebar end in family ', self.identifier,' must be of type "anc" (anchoring), "lap" (lapping) or "fix" (fixed length)')
        if rbEndType=='anc': # anchor length is calculated
            barShape='bent' if (angle>0) else 'straight'
            rbEndLenght=contrReb.getDesignAnchorageLength(concrete=self.reinfCfg.xcConcr, rebarDiameter=self.diameter, steel=self.reinfCfg.xcSteel, steelEfficiency= 1.0, barShape= barShape)
        elif rbEndType[:4]=='lap': #lap length id calculated
            ratio=1.0
            if len(paramAnc)>3:
                ratio=eval(paramAnc[3].replace('perc',''))/100
            rbEndLenght=contrReb.getLapLength(concrete= self.reinfCfg.xcConcr, rebarDiameter=self.diameter, steel=self.reinfCfg.xcSteel, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= ratio)
        return (angle,rbEndLenght)
    
    def getInitPntRebLref(self,rebarDraw):
        '''Return the initial point to start the reference line for labeling the rebar
        '''
        rebarEdges=rebarDraw.Edges
        #arrow in extremity 1
        pExtr1=rebarEdges[0].Vertexes[0].Point #vertex at extremity 1
        vArr=rebarEdges[0].tangentAt(0).multiply(0.9*self.reinfCfg.texSize) #arrow vector
        l=Draft.rotate(Draft.makeLine(pExtr1,pExtr1.add(vArr)),15,pExtr1)
        FreeCADGui.ActiveDocument.getObject(l.Name).LineColor = cfg.colorArrows
        #arrow in extremity 2
        pExtr2=rebarEdges[-1].Vertexes[1].Point #vertex at extremity 2
        vArr=rebarEdges[-1].tangentAt(1).multiply(0.9*self.reinfCfg.texSize) #arrow vector
        l=Draft.rotate(Draft.makeLine(pExtr2,pExtr2.add(vArr)),180-15,pExtr2)
        FreeCADGui.ActiveDocument.getObject(l.Name).LineColor = cfg.colorArrows
        # Texts pointing at the longest edge of the rebar
        laux=[e.Length for e in rebarEdges]
        ptoIniEtiq=rebarEdges[laux.index(max(laux))].CenterOfMass
        return ptoIniEtiq
    
    def drawRebarLref(self,ptoInic,vectorLRef):
        '''Draw the reference line for labeling a rebar family. Return the parameters to place the text

        :param ptoInic: start point of the reference line
        :param vectorLRef: vector to place the label
        '''
        hText=self.reinfCfg.texSize
        p2=ptoInic.add(vectorLRef)
        signo=1.0*vectorLRef.x/abs(vectorLRef.x)
        pEndRefL=p2.add(Vector(signo*hText,0))
        pCentCirc=pEndRefL.add(Vector(signo*hText,0))
        pText=pEndRefL.add(Vector(signo*hText/2.0,-hText/2.0))
        w=Draft.makeWire([ptoInic,p2,pEndRefL])
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
        if self.vectorLRef.x > 0:
            justif="Left"
        else:
            justif="Right"
        return pEndRefL,pCentCirc,justif,pText

    def drawDecorId(self,pEndRefL,pCentCirc,justif):
        '''Draw the decoration of the identification in rebar label
        '''
        hText=self.reinfCfg.texSize
        if len(self.identifier)==1:
            pl=FreeCAD.Placement()
            pl.move(pCentCirc)
    #        c=Draft.makeCircle(hText*(len(self.identifier)+1)/2.0,pl,False)
            c=Draft.make_circle(radius=hText*(len(self.identifier)+1)/2.0,placement=pl)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = cfg.colorRefLines
        else:
            signo=-1 if justif=="Right" else 1
            pp1=pCentCirc.add(Vector(0,hText))
            pp2=pCentCirc.add(Vector(signo*hText*(len(self.identifier)-1),hText))
            ppEndRefL=pCentCirc.add(Vector(0,-hText))
            ppCentCirc=pCentCirc.add(Vector(signo*hText*(len(self.identifier)-1),-hText))
            ppText=pCentCirc.add(Vector(signo*hText*len(self.identifier),0))
            
            if (pp1-pEndRefL).Length ==0  or (pp1-ppEndRefL).Length ==0 or (pEndRefL-ppEndRefL).Length == 0:
                c1=Part.Arc(pCentCirc+Vector(0,hText),pCentCirc+Vector(-hText,0),pCentCirc-Vector(0,hText))
            else:
                c1=Part.Arc(pp1,pEndRefL,ppEndRefL)
            c2=Part.Arc(pp2,ppText,ppCentCirc)
            l1=Part.makeLine(pp1,pp2)
            l2=Part.makeLine(ppEndRefL,ppCentCirc)
            etiq=Part.Wire([l1,c1.toShape(),l2,c2.toShape()]) 
            p=Part.show(etiq)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor = cfg.colorRefLines

    def drawSectRebarLref(self,startPnt,endPnt,vauxn,wireCenters):
        '''Draw the reference line for labeling a sectioned rebar family, or
        a family of stirrups in longitudinal section 
        Return the parameters to place the text

        :param startPnt: point position of the first rebar (center of the circle)
        :param startPnt: point position of the last rebar (center of the circle)
        :param vauxn: vector perpendicular to the line defined by the rebars pointing 
                      from concrete towards the rebars
        '''
        factPos=self.reinfCfg.factPosLabelSectReb
        hText=self.reinfCfg.texSize
        if wireCenters:
            offset=abs(self.reinfCfg.factDispReflinSectReb*1.5*self.reinfCfg.texSize)
            initLref=wireCenters.makeOffset2D(offset,join=2,openResult=True)
            if initLref.Length < wireCenters.Length:
                initLref=wireCenters.makeOffset2D(-1*offset,join=2,openResult=True)
            initLrefVertex=initLref.OrderedVertexes
            initLrefPoints=[vtx.Point for vtx in initLrefVertex]
            v1=Vector(initLrefPoints[1]-initLrefPoints[0]).normalize()
            v2=Vector(initLrefPoints[-2]-initLrefPoints[-1]).normalize()
            p1=initLrefPoints[0]+v1*self.reinfCfg.texSize
            p2=initLrefPoints[-1]+v2*self.reinfCfg.texSize
            if startPnt.distanceToPoint(p1) < startPnt.distanceToPoint(p2):
                lstPtsLref=[startPnt,p1]+initLrefPoints[1:-1]+[p2,endPnt]
            else:
                lstPtsLref=[endPnt,p1]+initLrefPoints[1:-1]+[p2,startPnt]
            lref=Part.makePolygon(lstPtsLref)
            w= Part.show(lref)
            p2=lstPtsLref[2]
            vnorm=Vector(p1.y-p2.y,-p1.x+p2.x).normalize()
        else:
            vaux=endPnt-startPnt
            vaux.normalize()
            vnorm=-1*vauxn.normalize()
            p1=startPnt+hText*vaux+self.reinfCfg.factDispReflinSectReb*1.5*hText*vnorm
            p2=endPnt-hText*vaux+self.reinfCfg.factDispReflinSectReb*1.5*hText*vnorm
            lref=Part.makePolygon([startPnt,p1,p2,endPnt])
            w=Part.show(lref)
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
        pStartRefL=p1+factPos*(p2-p1)
        pEndRefL=pStartRefL+hText*vnorm
        w=Draft.makeWire([pStartRefL,pEndRefL])
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
        pCentCirc=pEndRefL+hText*vnorm
        if vnorm.x < 0:
            justif="Right"
            pText=pCentCirc+hText/2*Vector(1,0)-hText/2*Vector(0,1)
        else:
            justif="Left"
            pText=pCentCirc-hText/2*Vector(1,0)-hText/2*Vector(0,1)
        self.drawDecorId(pEndRefL,pCentCirc,justif)
        return justif,pText
            
    def labelSectRebar(self,startPnt,endPnt,vauxn,wireCenters=None):
        ''' Label (reference lines + text) a family of rebars sectioned.

        :param startPnt: point position of the first rebar (center of the circle)
        :param startPnt: point position of the last rebar (center of the circle)
        :param vauxn: vector perpendicular to the line defined by the rebars pointing 
                      from concrete towards the rebars
        '''
        justif,pText=self.drawSectRebarLref(startPnt,endPnt,vauxn,wireCenters)
        ptoSketch,pos=self.rebarText(justif,pText)
        return ptoSketch,pos
       
    def rebarText(self,justif,pText):
        '''Write the text that labels the rebar family

        :param pEndRefL: point extremity of the reference line where to start the rotulation
        :param pCentCirc: point to place the center of the cirle (wih id)
        :param justif: justification of the text ('Left' or 'Right')
        :param pText: point to place the text 
        '''
        hText=self.reinfCfg.texSize
        if justif=="Left":
            txtColor=cfg.colorTextLeft
            if self.nmbBars:
                tx=self.identifier + '  ' + str(int(self.nmbBars)) + '%%C' + str(int(1000*self.diameter))
            else:
                tx=self.identifier + '  %%C' + str(int(1000*self.diameter)) + 'c/' + str(self.spacing)
            ptoSketch=pText+Vector((len(tx)-2)*0.7*hText,0)
            pos='l'
        else:
            txtColor=cfg.colorTextRight
            if self.nmbBars:
                tx=str(int(self.nmbBars)) + '%%C' + str(int(1000*self.diameter)) + '   ' + self.identifier
            else:
                tx='%%C' + str(int(1000*self.diameter)) + 'c/' + str(self.spacing) +'   ' + self.identifier
            ptoSketch=pText+Vector(-(len(tx)-2)*0.7*hText,0)
            pos='r'
        dt.put_text_in_pnt(text=tx,point=pText,hText=hText,color=txtColor,justif=justif)
        return ptoSketch,pos

    def getUnitWeight(self):
        '''Return the weigth [kg] per meter of bar
        '''
        if self.diameter <=12e-3:
            unitWeigth=round(math.pi*self.diameter**2.0/4.*7850,3)
        else:
            unitWeigth=round(math.pi*self.diameter**2.0/4.*7850,2)
        return unitWeigth
    
class rebarFamily(rebarFamilyBase):
    '''Family of reinforcement bars

    :ivar reinfCfg: instance of th class reinfConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bar [m]
    :ivar spacing: spacing between bars [m] (defaults to None). 
            (is 'nmBars' is defined, attribute 'spacing' is ignored)
    :ivar nmbBars: number of rebars in the family. This parameter takes
            precedende over 'spacing'
    :ivar lstPtsConcrSect: list of points in the concrete section to which 
            the bar is 'attached'
    :ivar lstCover: list of covers that correspond to each of the segments 
            defined with lstPtsConcrSect [m]. Defaults to the minimum cover 
            defined with 'reinfCfg'
    :ivar rightSideCover: side to give cover  (False for left side, True for right side)
            (defaults to True)
    :ivar vectorLRef: vector to draw the leader line for labeling the bar
    :ivar fromToExtPts: list of starting and end concrete points that delimit the 
            stretch of  sectioned rebars. Defaults to None, in which case this length 
            must be defined  by means of the attributes  'sectBarsConcrRadius' 
            or 'extensionLength'.
    :ivar sectBarsConcrRadius: radius of the concrete circular section to 
            which ara attached the sectioned rebars. Defaults to None, 
            in which case the stretch of sectioned rebars must be defined 
            with attributes 'fromToExtPts' or 'extensionLength'.
    :ivar extensionLength: length of the stretch in which the rebar family extends.
            Defaults to None, in which case  this length must be defined 
            by means of the attributes 'fromToExtPts' or 'sectBarsConcrRadius'
    :ivar lateralCover: minimal lateral cover to place the rebar family.
            Defaults to the minimum cover given with 'reinfCfg'.
    :ivar rightSideSectBars: side of cover to draw the family as sectioned bars 
            (circles) (False ' left, True right) (defaults to True)
    :ivar coverSectBars: cover to draw the family as sectioned bars 
            (circles) . Only needed if the bars are to be drawn.
            Defaults to the minimum cover given with 'reinfCfg'. 
   :ivar wire: FreeCAD object of type wire that represents the rebar shape
                ( or the rebar shape in section 1 when it is variable).
    :ivar wireSect: FreeCAD object of type wire that represents the rebar at
            section 2 when the shape of rebars in the family varies 
            uniformily from section 1 to section 2.
    :ivar lstPtsConcrSect2: parameter only used when defining a rebar family
            with variable shape. In that case, lstPtsConcrSect2 is the list of 
            points in the concrete section 2 to which the bar is 'attached'
    :ivar gapStart: increment (decrement if gapStart <0) of the length of 
            the reinforcement at its starting extremity (defaults to the minimum 
            negative cover given with 'reinfCfg').
    :ivar gapEnd: increment (decrement if gapEnd<0) of the length of 
            the reinforcement at its ending extremity  (defaults to the minimum 
            negative cover given with 'reinfCfg').
    :ivar extrShapeStart: defines the shape of the bar at its starting 
            extremity. It can be an straight or hook shape with anchor (anc) length, 
            lap length or a given fixed length.
            The anchor or lap length are automatically 
            calculated from the code (for now only EC2), material, and rebar configuration.
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
    :ivar extrShapeEnd:defines a straigth elongation or a hook at the ending 
            extremity of the bar. Definition analogous to extrShapeStart.
    :ivar fixLengthStart: fixed length of the first segment of the rebar 
             (defaults to None = no fixed length)
    :ivar fixLengthEnd: fixed length of the last segment of the rebar 
             (defaults to None = no fixed length)
    :ivar maxLrebar: maximum length of rebars (defaults to 12m)
    :ivar position: 'good' or 'poor' (equivalent to posI and posII in EHE). Is used to
             calculate lap lengths when splitting bars- (defaults to 'poor')
    :ivar compression: True if rebars in compression, False if rebars in tension.  
            Is used to calculate lap lengths when splitting bars- (defaults to False)  
    :ivar drawSketch: True to draw mini-sketch of the rebars besides the text 
            (defaults to True)
    '''
    def __init__(self,reinfCfg,identifier,diameter,lstPtsConcrSect,fromToExtPts=None,sectBarsConcrRadius=None,extensionLength=None,lstCover=None,rightSideCover=True,vectorLRef=Vector(0.5,0.5),coverSectBars=None,lateralCover=None,rightSideSectBars=True,spacing=None,nmbBars=None,lstPtsConcrSect2=[],gapStart=None,gapEnd=None,extrShapeStart=None,extrShapeEnd=None,fixLengthStart=None,fixLengthEnd=None,maxLrebar=12,position='poor',compression=False,drawSketch=True):
        super(rebarFamily,self).__init__(reinfCfg,identifier,diameter,lstPtsConcrSect,lstCover,rightSideCover)
        self.spacing=spacing 
        self.vectorLRef= vectorLRef
        self.fromToExtPts= fromToExtPts
        self.sectBarsConcrRadius=sectBarsConcrRadius
        self.extensionLength=extensionLength
        self.coverSectBars=coverSectBars if coverSectBars is not None else reinfCfg.cover
        self.lateralCover=lateralCover if lateralCover is not None else reinfCfg.cover
        self.rightSideSectBars= rightSideSectBars
        self.lstPtsConcrSect2=lstPtsConcrSect2
        self.listaPtosArm=[[],[]]
        self.nmbBars=nmbBars
        self.gapStart= gapStart if gapStart is not None else -reinfCfg.cover
        self.gapEnd= gapEnd  if gapEnd is not None else -reinfCfg.cover
        self.extrShapeStart=extrShapeStart
        self.extrShapeEnd=extrShapeEnd
        self.fixLengthStart=fixLengthStart
        self.fixLengthEnd=fixLengthEnd
        self.lstWire=None 
        self.wireSect2=None
        self.maxLrebar=maxLrebar
        self.position=position.lower()
        self.compression=compression
        self.drawSketch=drawSketch
    
    def drawPolySectBars(self,vTranslation=Vector(0,0,0)):
        '''Draw the rebar family as sectioned bars represented by circles in 
        the RC section (straight or polygonal shape).

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        vStart=(self.fromToExtPts[1]-self.fromToExtPts[0]).normalize() 
        vEnd=(self.fromToExtPts[-2]-self.fromToExtPts[-1]).normalize()
        concrWire=Part.makePolygon(self.fromToExtPts)
        concrWire.translate(vTranslation)
        if self.rightSideSectBars:
            offset=(self.coverSectBars+self.diameter/2.0)
        else:
            offset=-(self.coverSectBars+self.diameter/2.0)
        if len(self.fromToExtPts)>2:
            initCentersWire=concrWire.makeOffset2D(offset,join=2,openResult=True)
        else:
            vauxn=Vector(vStart.y,-vStart.x).normalize()
            initCentersWire=concrWire.translated(offset*vauxn) 
        initCentersWireVertex=initCentersWire.OrderedVertexes
        Laux=initCentersWire.Length
        # adjust the linear extension of rebars
        initCentersWirePoints=[vtx.Point for vtx in initCentersWireVertex]
        vAux=Vector(initCentersWirePoints[1]-initCentersWirePoints[0]).normalize()
        if vAux != vStart:
            initCentersWirePoints.reverse()
        if self.nmbBars: # spacing is calculated through number of rebars
            firstPoint=initCentersWirePoints[0]+vStart*(self.lateralCover+self.diameter/2.0)
            endPoint=initCentersWirePoints[-1]+vEnd*(self.lateralCover+self.diameter/2.0)
            centersWirePoints=[firstPoint]+initCentersWirePoints[1:-1]+[endPoint]
            centersWire=Part.makePolygon(centersWirePoints) # polyline jointing the cernters of rebars
            centersSectBars=centersWire.discretize(Number=self.nmbBars) # list of points representing the centers of rebars
            self.spacing=centersWire.Length/(self.nmbBars-1) 
        else:
            nesp=int((Laux-2.0*self.lateralCover-self.diameter)/self.spacing)
            distrL=(Laux-self.spacing*nesp)/2.0
            firstPoint=initCentersWirePoints[0]+vStart*distrL
            endPoint=initCentersWirePoints[-1]+vEnd*distrL
            centersWirePoints=[firstPoint]+initCentersWirePoints[1:-1]+[endPoint]
            centersWire=Part.makePolygon(centersWirePoints)
            centersSectBars=centersWire.discretize(Distance=self.spacing)
        vAux=(centersWirePoints[1]-centersWirePoints[0])
        if vAux != vStart:
            centersWire.reverse()
        #Draw sectioned rebars
        zaxis = Vector(0, 0, 1)
        for cent in centersSectBars:
            place=FreeCAD.Placement(); place.move(cent)
            c=Draft.makeCircle(self.diameter/2.0,placement=place,face=False)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor =cfg.colorSectBars
        self.nbarsAux=len(centersSectBars)
        # Data to draw reference line
        startPnt=centersSectBars[0]
        endPnt=centersSectBars[-1]
        vaux=self.fromToExtPts[1]-self.fromToExtPts[0]
        vaux.normalize()
        if self.rightSideSectBars:
            vauxn=Vector(vaux.y,-vaux.x)
        else:
            vauxn=Vector(-vaux.y,vaux.x)
        vauxn.normalize()
        if len(self.fromToExtPts) > 2:
            self.labelSectRebar(startPnt,endPnt,vauxn,wireCenters=centersWire)
        else:
            self.labelSectRebar(startPnt,endPnt,vauxn,wireCenters=None) 
        return
        
    def drawCircSectBars(self,vTranslation=Vector(0,0,0)):
        '''Draw the rebar family as sectioned bars represented by circles in 
        the RC section (circular shape).

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        centersWire=Part.makeCircle(self.sectBarsConcrRadius-self.coverSectBars-self.diameter/2.0)
        Laux=centersWire.Length
        if self.nmbBars:
            self.nbarsAux=self.nmbBars
        else:
            self.nbarsAux=int(Laux/self.spacing)
        centersSectBars=centersWire.discretize(Number=self.nbarsAux)
        #Draw sectioned rebars
        for cent in centersSectBars:
            place=FreeCAD.Placement(); place.move(cent)
            c=Draft.makeCircle(self.diameter/2.0,placement=place,face=False)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor =cfg.colorSectBars
        vaux=centersSectBars[2]-centersSectBars[0]
        vauxn=Vector(-vaux.y,vaux.x)
        vauxn.normalize()
        self.labelSectRebar(centersSectBars[0],centersSectBars[2],vauxn)
      

    def drawLstRebar(self,vTranslation=Vector(0,0,0)):
        if self.lstWire==None:
            self.createLstRebar()
        for rw in self.lstWire:
            self.drawRebar(rw,vTranslation)
        if len(self.lstPairDimPnts)>0:
            self.drawDimRebar(vTranslation)

    def drawDimRebar(self,vTranslation=Vector(0,0,0)):
        spacDimLine=2*self.reinfCfg.texSize
        for l in self.lstPairDimPnts:
            lst_disp=[v+vTranslation for v in l]
            dim.dim_lst_pnts(lstPnts=lst_disp,spacDimLine=spacDimLine)
            
    
    def drawRebar(self,rebWire,vTranslation=Vector(0,0,0)):
        '''Represent the bar family in the RC section as a bar in its 
        true shape.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        # copy of the rebar wire to be depicted and applied the translation
        #flechas en extremos de barra
        rebarDraw=rebWire.copy()
        rebarDraw.translate(vTranslation)
        rebarFillet= Draft.make_wire(rebarDraw)
        rad=RCutils.bend_rad_hooks_EHE(self.diameter*1e3)/1e3
        rebarFillet.FilletRadius=rad
        FreeCADGui.ActiveDocument.getObject(rebarFillet.Name).LineColor = cfg.colorRebars
        FreeCADGui.ActiveDocument.Document.recompute()
        ptoIniEtiq=self.getInitPntRebLref(rebarDraw)
        
        pEndRefL,pCentCirc,justif,pText=self.drawRebarLref(ptoIniEtiq,self.vectorLRef)
        self.drawDecorId(pEndRefL,pCentCirc,justif)
        ptoSketch,pos=self.rebarText(justif,pText)
        # draw sketch
        if self.drawSketch:
            wSketch=self.reinfCfg.sketchScale*self.reinfCfg.texSize
            hSketch=self.reinfCfg.sketchScale*self.reinfCfg.texSize
            sketch=rebWire.copy()
            bound=sketch.BoundBox
            cog=sketch.CenterOfMass
            if bound.XLength==0:
                fScale=hSketch/bound.YLength
            elif bound.YLength==0:
                fScale=wSketch/bound.XLength
            else:
                fScale=min(wSketch/bound.XLength,hSketch/bound.YLength)
            sketch.scale(fScale,cog)
            bound=sketch.BoundBox
            ptoCDG=ptoSketch-Vector(bound.XLength/2,0) if pos=='r' else ptoSketch+Vector(bound.XLength/2,0)
    #        ptoSketch=ptoTxt+Vector(0,-(self.reinfCfg.texSize+bound.YLength/2))
            sketch.translate(ptoCDG.sub(cog))
            p=Part.show(sketch)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorRebarSketch
#        drawMiniSketchRebar(rbFam=self,ptCOG=ptoSketch,wColumn=10*self.reinfCfg.texSize,hRow=10*self.reinfCfg.texSize,hText=0)
        return

    def createLstRebar(self):
        '''Create the wire that represents the true shape of a bar in the 
        family. In case of variable shape, a second wire is created according 
        to the shape defined for section2.
        '''
        lstPtRFam=self.getLstPtsRebar(self.lstPtsConcrSect)
        self.lstWire=self.getLstRebars(lstPtRFam)
        if len(self.lstPtsConcrSect2) > 0:
            lstPtsRebar2,=self.getLstPtsRebar(self.lstPtsConcrSect2)
            lstLinRebar2=[Part.makeLine(lstPtsRebar2[i],lstPtsRebar2[i+1])for i in range(len(lstPtsRebar2)-1)]
            self.wireSect2=[(Part.Wire(lstLinRebar2))]
        

    def getLstPtsRebar(self,lstPtsConcr):
        '''Return lstPtsRebar, which  is list of point of the wire that represents 
        the true shape of the bar defined by the points of the concrete section 
        listed in lstPtsConcr.
        Also creates the attribute lstPairDimPnts, which is a list of pairs of points to 
        dimension hooks, laps, straight elongations and lapping of bars.

        :param lstPtsConcr: ordered list of points in the concrete section 
        to which the rebar is 'attached'. 
        '''
        lstPtsRebar=self.getLstPtsBasicRebar(lstPtsConcr)
        self.lstPairDimPnts=list() 
        # Start extremity: gaps, straight elongation, hooks
        vaux=lstPtsRebar[1].sub(lstPtsRebar[0]).normalize()
        if self.fixLengthStart:
            lstPtsRebar[0]=lstPtsRebar[1].sub(vaux.multiply(self.fixLengthStart))
        else:
            lstPtsRebar[0]=lstPtsRebar[0].sub(vaux.multiply(self.gapStart))
        if self.extrShapeStart:
            extrShAng,extrShLn=self.getExtrShapeParams(self.extrShapeStart)
            vaux=lstPtsRebar[1].sub(lstPtsRebar[0]).normalize()
            if extrShAng == 0:  #straight elongation
                pntInit=lstPtsRebar[0]
                lstPtsRebar[0]=lstPtsRebar[0].sub(vaux.multiply(extrShLn))
                self.lstPairDimPnts+=[[lstPtsRebar[0],pntInit]]
            else: #hook
                lstPtsRebar[0]=lstPtsRebar[0].add(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                firstPoint=lstPtsRebar[0].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.insert(0,firstPoint)
                self.lstPairDimPnts+=[[lstPtsRebar[0],lstPtsRebar[1]]]
        # End extremity: gaps, straight elongation, hooks
        vaux=lstPtsRebar[-1].sub(lstPtsRebar[-2]).normalize()
        if self.fixLengthEnd:
            lstPtsRebar[-1]=lstPtsRebar[-2].add(vaux.multiply(self.fixLengthEnd))
        else:
            lstPtsRebar[-1]=lstPtsRebar[-1].add(vaux.multiply(self.gapEnd))
        if self.extrShapeEnd:
            extrShAng,extrShLn=self.getExtrShapeParams(self.extrShapeEnd)
            vaux=lstPtsRebar[-1].sub(lstPtsRebar[-2]).normalize()
            if extrShAng == 0:  #straight elongation
                pntInit=lstPtsRebar[-1]
                lstPtsRebar[-1]=lstPtsRebar[-1].add(vaux.multiply(extrShLn))
                self.lstPairDimPnts+=[[pntInit,lstPtsRebar[-1]]]
            else: #hook
                lstPtsRebar[-1]=lstPtsRebar[-1].sub(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                endPoint=lstPtsRebar[-1].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.append(endPoint)
                self.lstPairDimPnts+=[[lstPtsRebar[-2],lstPtsRebar[-1]]]
        return lstPtsRebar
        
    def getNumberOfBars(self):
        if self.extensionLength:
            self.nbarsAux=int(self.extensionLength/self.spacing)+1
        return self.nbarsAux

                 
    def getLstRebars(self,lstPtsRebar):
        '''Checks the length of the rebar defined by the list of points lstPtsRebar. If 
        it is less than maxLrebar returns a list with the wire defined by those points,
        otherwise, the rebar is splitted in pieces of length less or equal than 
        maxLrebar, pair of lap points are added to the drawLstRebar, and a list of 
        wires is returned. 

        :param lstPtsRebar: list of points that define the rebar in its entire length.
        '''
        lstRebars=list()
        lstDist=[lstPtsRebar[i].distanceToPoint(lstPtsRebar[i+1]) for i in range(len(lstPtsRebar)-1)]
        if sum(lstDist) <= self.maxLrebar:
            lstLinRebar=[Part.makeLine(lstPtsRebar[i],lstPtsRebar[i+1])for i in range(len(lstPtsRebar)-1)]
            rebarWire=Part.Wire(lstLinRebar)
            lstRebars.append(rebarWire)
        else:
            # calculate slap length
            eta1=1.0 if 'good' in self.position else 0.7
            if not(self.spacing):
                if self.fromToExtPts:
                    p=Part.makePolygon(self.fromToExtPts)
                    self.spacing=p.Length/(self.nmbBars-1)
                elif self.extensionLength:
                    self.spacing=self.extensionLength/(self.nmbBars-1)
                elif self.sectBarsConcrRadius:
                    self.spacing=2*math.pi*self.sectBarsConcrRadius/self.nmbBars
                else:
                    lmsg.error('for rebar family:'+ self.identifier+ "can't  calculate the spacing, either 'fromToExtPts', 'extensionLength' or 'sectBarsConcrRadius' must be defined")
            contrReb=Lcalc.RebarController(concreteCover=self.reinfCfg.cover, spacing=self.spacing, eta1=eta1, compression= self.compression) # create rebar controllers to calculate anchor or gap lengths
            lapLenght=contrReb.getLapLength(concrete= self.reinfCfg.xcConcr, rebarDiameter=self.diameter, steel=self.reinfCfg.xcSteel, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= 1.0)
            
            lstCumDist=[0]+[sum(lstDist[:y]) for y in range(1, len(lstDist) + 1)] # cummulated lengths
            while lstCumDist[-1] > self.maxLrebar:
                indLmax=bisect.bisect_left(lstCumDist,self.maxLrebar)# find the position of maxLrebar in lstCumDist
                lstPtsReb1=lstPtsRebar[:indLmax]
                vaux=lstPtsRebar[indLmax].sub(lstPtsRebar[indLmax-1])
                vaux.normalize()
                LtoAdd1=self.maxLrebar if indLmax==0 else self.maxLrebar-lstCumDist[indLmax-1]
 #               LtoAdd1=self.maxLrebar-lstCumDist[indLmax-1]
                lastPnt1=lstPtsReb1[-1].add(LtoAdd1*vaux)
                lstPtsReb1.append(lastPnt1)
                lstLinRebar1=[Part.makeLine(lstPtsReb1[i],lstPtsReb1[i+1])for i in range(len(lstPtsReb1)-1)]
                lstRebars.append(Part.Wire(lstLinRebar1))
                # next rebar (rest)
                lstPtsRebar=lstPtsRebar[indLmax:]
                firstPnt=lastPnt1.add(-lapLenght*vaux)
                lstPtsRebar.insert(0,firstPnt)
                self.lstPairDimPnts+=[[firstPnt,lastPnt1]]
                lstDist=[lstPtsRebar[i].distanceToPoint(lstPtsRebar[i+1]) for i in range(len(lstPtsRebar)-1)]
                lstCumDist=[0]+[sum(lstDist[:y]) for y in range(1, len(lstDist) + 1)] # cummulated lengths
            lstLinRebar=[Part.makeLine(lstPtsRebar[i],lstPtsRebar[i+1])for i in range(len(lstPtsRebar)-1)]
            lstRebars.append(Part.Wire(lstLinRebar))
        return lstRebars

    def getTextFiSpacing(self):
        '''Return the text for column '%%C/SEP.' of the bar schedule'''
        formatSpacing='%.'+str(self.reinfCfg.decSpacing)+'f'
        if self.nmbBars:
            txt='%%C' + str(int(1000*self.diameter))
        else:
            if dsu.get_number_decimal_positions(self.spacing)>self.reinfCfg.decSpacing:
                txSpacing=str(self.spacing) # all decimals are written
            else:
                txSpacing=formatSpacing %self.spacing
            txt='%%C' + str(int(1000*self.diameter)) + 'c/' + txSpacing
        return txt
 

def drawSketchRebarShape(rW,ptCOG,wColumn,hRow,hText,decLengths=2,rW2=None):
    '''Draw the shape skectch of the reinforcment bar in the bar 
    schedule. Return the total length of the rebar.

    :param rW: rebar wire
    :param ptCOG:  point where to place the center of gravity of the sketch.
    :param wColumn: width of the column 'Shape' in the bar schedule.
    :param hRow: height of the row in the bar schedule.
    :param hText: height of the text to label the sketch.
    :param decLengths: decimal posiitions
    :param rW2: second rebar wire when variable section
    '''
    formatLength='%.'+str(decLengths)+'f'
    sketch=rW.copy()
    bound=sketch.BoundBox
    cog=sketch.CenterOfMass
    if bound.YLength > bound.XLength:
        sketch.rotate(cog,Vector(0,0,1),-90)
        bound=sketch.BoundBox
    if bound.YLength==0:
        fScale=(0.80*wColumn)/(bound.XLength)
    else:
        fScale=min((0.75*wColumn)/(bound.XLength),0.75*hRow/(bound.YLength))
    sketch.scale(fScale,cog)
    pos=sketch.BoundBox.Center
    sketch.translate(ptCOG.sub(pos))
    p=Part.show(sketch)
    FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorRebarSketch
    #Texts
    lstWireLengths=[round(edg.Length,decLengths) for edg in rW.Edges]
    lengthsText=[str(i) for i in lstWireLengths]
    totalLength=round(sum(lstWireLengths),decLengths)
    totalLengthTxt=formatLength %totalLength
    if rW2:
        lstWireLengths2=[round(edg.Length,decLengths) for edg in  rW2.Edges]
        lengthsText2=[str(i) for i in lstWireLengths2]
        totalLength2=round(sum(lstWireLengths2),decLengths)
        totalLength=(totalLength+totalLength2)/2.0
        totalLengthTxt+='...'+ formatLength %sum(lstWireLengths2)
        for j in range(len(lstWireLengths)):
            if lengthsText[j] != lengthsText2[j]:
                lengthsText[j]+='...'+ lengthsText2[j]
    sketchEdges=sketch.Edges
    for i in zip(sketchEdges,lengthsText):
        edg=i[0]
        dt.put_text_in_pnt(text=i[1],point=edg.CenterOfMass,hText=hText,color=cfg.colorTextCenter,justif="Center",rotation=math.degrees(edg.tangentAt(0).getAngle(Vector(1,0,0))))
    return (totalLength,totalLengthTxt)

    
class stirrupFamily(rebarFamilyBase):
    ''' Family of shear reinforcement 

    :ivar reinfCfg: instance of th class reinfConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bar [m]
    :ivar lstPtsConcrLong: list of points in the longitudinal section to which the first stirrup is 'attached'
    :ivar lstPtsConcrSect: list of points in the transversal concrete section to which the first stirrup 
          is 'attached'. Defaults to None, in which case, the concrete section is circular and defined by
            attribute 'concrSectRadius'
    :ivar concrSectRadius: radius of the circular concrete section
           Defaults to None, in which case, the concrete section is polygonal and defined by
            attribute 'lstPtsConcrSect'
    :ivar spacStrpTransv: spacement between stirrups in the transversal section (true shape)
    :ivar spacStrpLong: spacement between stirrups in the longitudinal 
          section (as in beams, where they are displayed as lines)
    :ivar vDirLong: vector to define the longitudinal direction
    :ivar nmbStrpTransv: number of stirrups displayed as true shape
    :ivar nmbStrpLong: number of stirrups displayed as lines
    :ivar lstCover: list of covers for each side of the stirrup. If 
          None, reinfCfg.cover is taken for all sides.
    :ivar rightSideCover:side to give cover  (False left side, True for right side)
          (defaults to True)
    :ivar dispStrpTransv: displacement of stirrups in the
          transversal section (defaults to None)
    :ivar dispStrpLong: displacement of stirrups in the
          longitudinal section (defaults to None)
    :ivar vectorLRef: vector to draw the leader line for labeling the bar (defaults to Vector(0.5,0.5)
    :ivar rightSideLabelLn: side to place the label of the stirrups in longitudinal section (defaults to True right)
    :ivar closed: if closed stirrup True (defaults to True)
    :ivar fixAnchorStart, fixAnchorEnd: anchor definition at start and end, respectively (defaults to None) The anchors are defined as follows:
            fix[angle]= is a positive number, expresed in sexagesimal degrees, 
                        that represents the counterclokwise angle from the first segment 
                        of the rebar towards the hook.
            len[number]: number is the length of the segment to add (in mm)
            Examples: 'fix45_len150'
    
    '''
    def __init__(self,reinfCfg,identifier,diameter,lstPtsConcrLong,lstPtsConcrSect=None,concrSectRadius=None,spacStrpTransv=None,spacStrpLong=None,vDirTrans=None,vDirLong=Vector(1,0),nmbStrpTransv=1,nmbStrpLong=1,lstCover=None,rightSideCover=True,dispStrpTransv=0,dispStrpLong=0,vectorLRef=Vector(0.5,0.5),rightSideLabelLn=True,closed=True,fixAnchorStart=None,fixAnchorEnd=None):
        super(stirrupFamily,self).__init__(reinfCfg,identifier,diameter,lstPtsConcrSect,lstCover,rightSideCover)
        self.lstPtsConcrLong=lstPtsConcrLong
        self.concrSectRadius=concrSectRadius
        self.spacStrpTransv=spacStrpTransv
        self.spacStrpLong=spacStrpLong
        self.vDirTrans=vDirTrans
        self.vDirLong=vDirLong
        self.nmbStrpTransv=nmbStrpTransv
        self.nmbStrpLong=nmbStrpLong
        self.dispStrpTransv=dispStrpTransv
        self.dispStrpLong=dispStrpLong
        self.vectorLRef=vectorLRef
        self.rightSideLabelLn=rightSideLabelLn
        self.closed=closed
        self.fixAnchorStart=fixAnchorStart
        self.fixAnchorEnd=fixAnchorEnd
        self.rebarWire=None
        self.lstWire=None
        self.wireSect2=None

    def getVdirTrans(self):
        '''return a unitary direction vector in transversal section'''
        if self.vDirTrans is None:
            if self.concrSectRadius:
                self.vDirTrans=Vector(0,1)
            else:
                self.vDirTrans=self.lstPtsConcrSect[1]-self.lstPtsConcrSect[0]
        return self.vDirTrans.normalize()
    
    def getVdirLong(self):
        '''return a unitary direction vector in longitudinal section'''
        return self.vDirLong.normalize()

    def getLstCoverAxis(self):
        lstCoverAxis=[c+self.diameter/2 for c in self.lstCover]
        return lstCoverAxis
        
    def createLstRebar(self):
        '''Note; This part should be transfered to the base class
        '''
        if self.concrSectRadius: #circular section
            radAxisStirr=self.concrSectRadius-self.lstCover[0]-self.diameter/2
            self.rebarWire=Part.makeCircle(radAxisStirr)
            self.lstWire=[self.rebarWire]
        elif self.lstPtsConcrSect:
            lstCoverAxis=self.getLstCoverAxis()
            lstPtsRebar=self.getLstPtsBasicRebar(self.lstPtsConcrSect)
            if self.lstPtsConcrSect[0] == self.lstPtsConcrSect[-1]:
                pint=geom_utils.int2lines(lstPtsRebar[0],lstPtsRebar[1],lstPtsRebar[-2],lstPtsRebar[-1])
                lstPtsRebar[0]=pint; lstPtsRebar[-1]=pint
            if self.fixAnchorStart:
                extrShAng,extrShLn=self.getExtrShapeParams(self.fixAnchorStart)
                vaux=lstPtsRebar[1].sub(lstPtsRebar[0]).normalize()
                lstPtsRebar[0]=lstPtsRebar[0].add(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                firstPoint=lstPtsRebar[0].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.insert(0,firstPoint)
            if self.fixAnchorEnd:
                extrShAng,extrShLn=self.getExtrShapeParams(self.fixAnchorEnd)
                vaux=lstPtsRebar[-1].sub(lstPtsRebar[-2]).normalize()
                lstPtsRebar[-1]=lstPtsRebar[-1].sub(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                endPoint=lstPtsRebar[-1].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.append(endPoint)
                lstLinRebar=[Part.makeLine(lstPtsRebar[i],lstPtsRebar[i+1])for i in range(len(lstPtsRebar)-1)]
                self.rebarWire=Part.Wire(lstLinRebar)
                self.lstWire=[self.rebarWire]
            else:
                lmsg.error('for rebar family:'+ self.identifier+ '-> either lstPtsConcrSect or concrSectRadius must be defined.')
 
    def drawPolyRebars(self,vTranslation=Vector(0,0,0)):
        self.getVdirTrans()
        if self.rebarWire is None:
            self.createLstRebar()
        rebarDraw=self.rebarWire.copy()
        rebarDraw.translate(vTranslation)
        if self.dispStrpTransv:
            rebarDraw.translate(self.dispStrpTransv*self.vDirTrans)
        if self.concrSectRadius:
            rebarFillet=rebarDraw
        else:
            rebarFillet= Draft.make_wire(rebarDraw,closed=self.closed,face=False)
            rad=RCutils.bend_rad_hooks_EHE(self.diameter*1e3)/1e3
            rebarFillet.FilletRadius=rad
        FreeCADGui.ActiveDocument.getObject(rebarFillet.Name).LineColor = cfg.colorRebars
        for i in range(1,self.nmbStrpTransv):
            stirr=rebarDraw.copy()
            stirr.translate(i*self.spacStrpTransv*self.vDirTrans)
            stirrFillet=Draft.make_wire(stirr,closed=self.closed,face=False)
            stirrFillet.FilletRadius=rad
            FreeCADGui.ActiveDocument.getObject(stirrFillet.Name).LineColor = cfg.colorRebars
        FreeCADGui.ActiveDocument.Document.recompute()
        ptoIniEtiq=self.getInitPntRebLref(rebarDraw)
        pEndRefL,pCentCirc,justif,pText=self.drawRebarLref(ptoIniEtiq,self.vectorLRef)
        self.drawDecorId(pEndRefL,pCentCirc,justif)
        ptoSketch,pos=self.rebarText(justif,pText)

    def drawCircRebar(self,vTranslation=Vector(0,0,0)):
        if self.rebarWire is None:
            self.createLstRebar()
        radAxisStirr=self.concrSectRadius-self.lstCover[0]-self.diameter/2
        pl=FreeCAD.Placement()
        pl.move(vTranslation)
        c=Draft.make_circle(radius=radAxisStirr,placement=pl,face=False)
        FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = cfg.colorRebars
        ptoIniEtiq=vTranslation+Vector(radAxisStirr,0)
        pEndRefL,pCentCirc,justif,pText=self.drawRebarLref(ptoIniEtiq,self.vectorLRef)
        self.drawDecorId(pEndRefL,pCentCirc,justif)
        ptoSketch,pos=self.rebarText(justif,pText)
        
    def drawLnRebars(self,vTranslation=Vector(0,0,0)):
        lstCoverAxis=self.getLstCoverAxis()
        vLn=self.getVdirLong()
        vReb=(self.lstPtsConcrLong[1]-self.lstPtsConcrLong[0]).normalize()
        lstPtsRebar=[self.lstPtsConcrLong[0]+lstCoverAxis[-1]*vReb,
                     self.lstPtsConcrLong[1]-lstCoverAxis[0]*vReb]
        lstLinRebar=[Part.makeLine(lstPtsRebar[0],lstPtsRebar[1])]
        rebarDraw=Part.Wire(lstLinRebar)
        rebarDraw.translate(vTranslation)
        if self.dispStrpLong:
            rebarDraw.translate(self.dispStrpLong*vLn)
        rebarFillet=Draft.make_wire(rebarDraw)
        FreeCADGui.ActiveDocument.getObject(rebarFillet.Name).LineColor = cfg.colorRebars
        for i in range(1,self.nmbStrpLong):
            stirr=rebarDraw.copy()
            stirr.translate(i*self.spacStrpLong*vLn)
            stirrFillet=Draft.make_wire(stirr)
            FreeCADGui.ActiveDocument.getObject(stirrFillet.Name).LineColor = cfg.colorRebars
        FreeCADGui.ActiveDocument.Document.recompute()
        startPnt=rebarFillet.Points[0]
        endPnt=stirrFillet.Points[0]
        if self.rightSideLabelLn:
            vauxn=Vector(startPnt.y-endPnt.y,endPnt.x-startPnt.x)
        else:
            vauxn=Vector(endPnt.y-startPnt.y,startPnt.x-endPnt.x)
        vauxn.normalize()
        self.labelSectRebar(startPnt,endPnt,vauxn,wireCenters=None)

    

    def rebarText(self,justif,pText):
        '''Write the text that labels the rebar family

        :param pEndRefL: point extremity of the reference line where to start the rotulation
        :param pCentCirc: point to place the center of the cirle (wih id)
        :param justif: justification of the text ('Left' or 'Right')
        :param pText: point to place the text 
        '''
        hText=self.reinfCfg.texSize
        txt=self.getTextFiSpacing()
        if justif=="Left":
            txtColor=cfg.colorTextLeft
            tx=self.identifier + '   '+ txt
            ptoSketch=pText+Vector((len(tx)-2)*0.7*hText,0)
            pos='l'
        else:
            txtColor=cfg.colorTextRight
            tx=txt+'   ' + self.identifier
            ptoSketch=pText+Vector(-(len(tx)-2)*0.7*hText,0)
            pos='r'
        dt.put_text_in_pnt(text=tx,point=pText,hText=hText,color=txtColor,justif=justif)
        return ptoSketch,pos

    def getNumberOfBars(self):
        '''Return the number of bars in the family.
        '''
        nBar=self.nmbStrpTransv*self.nmbStrpLong
        return nBar

    def getTextFiSpacing(self):
        '''Return the text for column '%%C/SEP.' of the bar schedule'''
        txt='c.%%C' + str(int(1000*self.diameter)) + 'c/'
        if self.spacStrpLong:
            txt+=str(self.spacStrpLong)+'/'
        if self.spacStrpTransv:
            txt+=str(self.spacStrpTransv)
        else:
            txt=txt[:-1] 
        return txt
        
       
    
def drawMiniSketchRebar(rbFam,ptCOG,wSketch,hSketch):
    '''Draw the shape sketch of the rebar (not rotated).

    :param rbFam: family of rebars to be represented.
    :param ptCOG:  point where to place the center of gravity of the sketch.
    :param wSketch: maximum width of the sketch
    :param hSketch: maximum height of the sketch
    '''
    sketch=rbFam.wire.copy()
    bound=sketch.BoundBox
    cog=sketch.CenterOfMass
    fScale=min(wSketch/bound.XLength,hSketch/bound.YLength)
    sketch.scale(fScale,cog)
    sketch.translate(ptCOG.sub(cog))
    Part.show(sketch)
 
                
def barSchedule(lstBarFamilies,schCfg=cfg.XC_scheduleCfg,title='  ',pntTLcorner=Vector(0,0),doc=FreeCAD.ActiveDocument):
    ''' Create the rebar schedule from a list of rebar families

    :param schCfg: instance of scheduleConf class (defautls to XC_scheduleCfg
    :param lstBarFamilies: ordered list of rebar families to be included in 
           the schedule
    :param title: title for the rebar schedule (defaults to None)
    :param pntTLcorner: point in top-left corner (defaults to Vector(0,0))
    :param doc: document in which to put the schedule (defaults to the 
                active document)
    '''
    FreeCAD.setActiveDocument(doc.Name)
    wColumns=schCfg.wColumns
    hRows=schCfg.hRows
    hText=schCfg.hText
    hTextSketch=schCfg.hTextSketch
    
    for rf in lstBarFamilies:
        if rf.lstWire==None:
            rf.createLstRebar()
#    totalWidth=sum(wColumns)
    numRows=sum([len(rb.lstWire) for rb in lstBarFamilies])
    totalWidth=sum(wColumns)
    p1=tables.drawBoxWtitle(pntTLcorner,wColumns,title,hText,hRows,numRows,doc)
    #Títulos para la tabla de despiece
    pLinea=p1.add(Vector(0,hRows/2.0))
    pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('POS.',pPos,hText,cfg.colorTextLeft)
    pEsq=pLinea.add(Vector(wColumns[0]+wColumns[1]/2.0,-hText/2.0))
    dt.put_text_in_pnt('ESQUEMA',pEsq,hText,cfg.colorTextCenter,"Center")
    pFiSep=pLinea.add(Vector(wColumns[0]+wColumns[1]+hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('%%C/SEP.',pFiSep.add(Vector(0,hText)), hText,cfg.colorTextLeft)
    dt.put_text_in_pnt('(mm)/(m)',pFiSep.add(Vector(0,-hText)), hText,cfg.colorTextLeft)
    pNbarras=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('NUM.',pNbarras, hText, cfg.colorTextRight,"Right")
    pLbarra=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]+wColumns[4]-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('LONG.',pLbarra.add(Vector(0,hText)), hText, cfg.colorTextRight,"Right")
    dt.put_text_in_pnt('(m)',pLbarra.add(Vector(0,-hText)), hText, cfg.colorTextRight,"Right")
    pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('PESO',pPeso.add(Vector(0,hText)), hText, cfg.colorTextRight,"Right")
    dt.put_text_in_pnt('(Kg)',pPeso.add(Vector(0,-hText)), hText, cfg.colorTextRight,"Right")
    pLinea=p1.add(Vector(0,-hRows/2.0))
    pesoTotal=0
    # order list of rebar families by identifications
    lstIdsOrig=[rbFam.identifier for rbFam in lstBarFamilies]
    lstOrdered=[i for i in lstIdsOrig]
    dsu.sort_human(lstOrdered)
#    orderLstBarFamilies=[x for x,_ in sorted(zip(lstBarFamilies,lstIds),key=lambda x: x[1])]
    for k in lstOrdered:
        index=lstIdsOrig.index(k)
        rbFam=lstBarFamilies[index]
        formatLength='%.'+str(rbFam.reinfCfg.decLengths)+'f'
        formatSpacing='%.'+str(rbFam.reinfCfg.decSpacing)+'f'
        if rbFam.lstWire==None:
            rbFam.createLstRebar()
        for i in range(len(rbFam.lstWire)):
            #identifier
            pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
            dt.put_text_in_pnt(rbFam.identifier,pPos, hText,cfg.colorTextLeft)
            #sketch
            pEsq=pLinea.add(Vector(wColumns[0] + wColumns[1]/2.0,0))
            rW2=rbFam.wireSect2[i] if rbFam.wireSect2 else None
            barLength,barLengthTxt=drawSketchRebarShape(rbFam.lstWire[i],pEsq,wColumns[1],hRows,hTextSketch,rbFam.reinfCfg.decLengths,rW2)
            pFiSep=pLinea.add(Vector(sum(wColumns[:2])+hText/2.0,-hText/2.0))
            tx=rbFam.getTextFiSpacing()
            dt.put_text_in_pnt(tx,pFiSep, hText,cfg.colorTextLeft)
            #number of bars
            pNbarras=pLinea.add(Vector(sum(wColumns[:4])-hText/2.0,-hText/2.0))
            nBar=rbFam.getNumberOfBars()
            dt.put_text_in_pnt(str(nBar),pNbarras, hText, cfg.colorTextRight,"Right")
            pbarLength=pLinea.add(Vector(sum(wColumns[:5])-hText/2.0,-hText/2.0))
            dt.put_text_in_pnt(barLengthTxt,pbarLength, hText, cfg.colorTextRight,"Right")
            pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
            peso=nBar*barLength*rbFam.getUnitWeight()
            dt.put_text_in_pnt(formatLength %peso,pPeso, hText, cfg.colorTextRight,"Right")
            pesoTotal += peso
            pLinea=pLinea.add(Vector(0,-hRows))
    pTotal=pLinea.add(Vector(totalWidth-hText/2.0,0))
    dt.put_text_in_pnt('TOTAL Kg:   ' + formatLength %pesoTotal,pTotal, hText, cfg.colorTextRight,"Right")
    return


def bars_quantities_for_budget(lstBarFamilies,outputFileName):
    '''Generate the quantities of reinforcement bars included in the list and 
    write them in a file that can be processed with pyCost in order to produce 
    a budget.

    :param lstBarFamilies :ordered list of rebar families to be included in 
           the quantities list
    :param outputFileName: file to be created (full path and extension must 
           be given)
    '''
    f=open(outputFileName,'w')
    for rbFam in lstBarFamilies:
        if rbFam.lstWire==None:
            rbFam.createLstRebar()
        totalLength=sum(rbFam.lstWireLengths)
        if rbFam.wireSect2 != None:
            totalLength=(totalLength+sum(rbFam.wireSect2Lengths))/2.0
        s='currentUnitPriceQ.quantities.append(MeasurementRecord(c= \"'+ str(rbFam.identifier) +'\", uds= ' +str(rbFam.getNumberOfBars()) + ', l= ' + str(totalLength) + ', an= ' + str(rbFam.getUnitWeight())  + ')) \n'
        f.write(s)
    f.close()
        
def drawConcreteSection(lstPtsConcrSect,vTranslation=Vector(0,0,0),color=cfg.colorConcrete):
    ''' Draw a section of concrete defined by a list of points in the FreeCAD 
    active document (polygonal shape)

    :param lstPtsConcrSect: list of ordered lists of points to draw the 
           concrete section. Each list of points originates an open wire.
    :param vTranslation: Vector to apply a traslation to the RC section drawing.
           It facilitates the adding of several RC-sections to the same sheet of
           FreeCAD.
    '''
    l=Part.makePolygon(lstPtsConcrSect)
    l.translate(vTranslation)
    p=Part.show(l)
    FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =color
    return p
    
def drawCircConcreteSection(radiusConcrSect,vTranslation=Vector(0,0,0),color=cfg.colorConcrete):
    c=Part.makeCircle(radiusConcrSect)
    c.translate(vTranslation)
    p=Part.show(c)
    FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =color
    return p
   
def drawRCSection(lstOfLstPtsConcrSect=None,radiusConcrSect=None,lstShapeRebarFam=None,lstSectRebarFam=None,lstShapeStirrupFam=None,lstEdgeStirrupFam=None,vTranslation=Vector(0,0,0),dimConcrSect=False):
    '''Draw a reinforced concrete section in the FreeCAD active document

    :param lstOfLstPtsConcrSect: list of ordered lists of points to draw the 
           concrete section. Each list of points originates an open wire.
           (defaults to None)
    :param radiusConcrSect: radius of  the concrete section (for circular shape)
    :param lstShapeRebarFam: list of rebar families that are going to be 
           drawn with their true shape. 
           (defaults to None)
    :param lstSectRebarFam: list of rebar families that are going to be 
           drawn as sectioned bars (circles).
           (defaults to None)
    :param lstShapeStirrupFam: list of stirrup families that are going to be 
           drawn with their true shape.
    :param lstEdgeStirrupFam:  list of stirrup families that are going to be 
           drawn as edge lines.
    :param vTranslation: Vector to apply a traslation to the RC section drawing.
           It facilitates the adding of several RC-sections to the same sheet of
           FreeCAD. (defaults to Vector(0,0,0))
    :param dimConcrSect: True for dimensioning the concrete section
           (defaults to False)
    '''
    if lstOfLstPtsConcrSect:
        #draw the concrete section
        for lp in lstOfLstPtsConcrSect:
            drawConcreteSection(lp,vTranslation)
        if dimConcrSect:
            #dimensioning of concrete section
            if lstShapeRebarFam: r=lstShapeRebarFam[0]
            elif lstSectRebarFam: r=lstSectRebarFam[0]
            elif lstShapeStirrupFam: r=lstShapeStirrupFam[0]
            else: r=lstEdgeStirrupFam[0]
            spacDimLine=3*r.reinfCfg.texSize
            for l in lstOfLstPtsConcrSect:
                lst_disp=[v+vTranslation for v in l]
                dim.dim_lst_pnts(lstPnts=lst_disp,spacDimLine=spacDimLine)
    if radiusConcrSect:
        drawCircConcreteSection(radiusConcrSect,vTranslation)
    if lstShapeRebarFam:
        #draw the rebars in their true shape
        for rbFam in lstShapeRebarFam:
            rbFam.drawLstRebar(vTranslation)
    if lstSectRebarFam:
        #draw the sectioned rebars
        for rbFam in lstSectRebarFam:
            if rbFam.sectBarsConcrRadius:
                rbFam.drawCircSectBars(vTranslation)
            else:
                rbFam.drawPolySectBars(vTranslation)
    if lstShapeStirrupFam:
        for stFam in lstShapeStirrupFam:
            if stFam.concrSectRadius: #circular section
                stFam.drawCircRebar(vTranslation)
            else:
                stFam.drawPolyRebars(vTranslation)
    if lstEdgeStirrupFam:
        for stFam in lstEdgeStirrupFam:
            stFam.drawLnRebars(vTranslation)


