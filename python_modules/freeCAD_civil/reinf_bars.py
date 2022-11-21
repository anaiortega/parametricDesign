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
'''Classes to generate in FreeCAD drawings to represent  a reinforced-concrete 
structure and the bar schedule associated.

Diameter of the reinforcement bars must be expressed in meters [m].
Other length magnitudes should be expressed in meters [m].
'''

class genericConf(object):
    '''
    Generic parameteters to be used as default values for several 
    attributes of different rebar families.

    :ivar cover:   minimum cover
    :ivar texSize: generic text size to label rebar families in the 
          drawings. Defaults to 0.125
    :ivar Code: code on structural concrete that applies (defaults to 'EC2') 
    :ivar xcConcr: XC concrete material object (ex: EC2_materials.C25)
    :ivar xcSteel: XC steel material object (ex: EC2_materials.S500C)

    :ivar dynamEff: 'Y' 'yes' 'Yes' ... if dynamic effects may occur (defaults 
          to 'N') 
    :ivar decLengths: decimal positions to calculate and express lengths and
                      their derivated magnitudes, like weight  (defaults to 2).
    :ivar decSpacing: decimal positions to express the spacing (defaults to 2)
                      if spacing has more than decSpacing positions, the 
                      full number is written.
    :ivar sketchScale: scale of the sketch that represents the rebar in the text
                       relative to the text size (defaults to 5)
    :ivar factPosLabelSectReb: factor to locate labels of section-rebars (defaults to 2/3)
    :ivar factDispReflinSectReb: factor to locate reference lines of section-rebars (defaults to 1)
    '''
    def __init__(self,cover,xcConcr,xcSteel,texSize=0.125,Code='EC2',dynamEff='N',decLengths=2,decSpacing=2,sketchScale=5,factPosLabelSectReb=2/3,factDispReflinSectReb=1.0):
        self.cover=cover
        self.texSize=texSize
        self.xcConcr=xcConcr
        self.xcSteel=xcSteel
        self.dynamEff=dynamEff
        self.decLengths=decLengths
        self.decSpacing=decSpacing
        self.sketchScale=sketchScale
        self.factPosLabelSectReb=factPosLabelSectReb
        self.factDispReflinSectReb=factDispReflinSectReb
        if Code == 'EC2':
            from materials.ec2 import EC2_limit_state_checking as Lcalc # doesn't work if only imported here
            
class scheduleConf(object):
    '''Parameters to configure the geometry of the rebar schedule 

    :ivar widthColumns: width of the columns [identifier,sketch, diam. and spacing., 
                        Number of bars, length of each bar, total weight of the family]
                        (defaults to [10,28,20,10,12,12])
    :ivar hRows: rows height (defaults to 12)
    :ivar heightText: text height (defaults to 2.5)
    :ivar heigthTextSketch: text height for the sketch (defaults to 2.0).
    '''
    def __init__(self,widthColumns=[10,28,20,10,12,12],heightRows=12,heightText=2.5,heigthTextSketch=2.0):
        self.widthColumns=widthColumns
        self.heightRows=heightRows
        self.heightText=heightText
        self.heigthTextSketch=heigthTextSketch

class rebarFamilyBase(object):
    ''' Base class for families of reinforcement bars

    :ivar genConf: instance of th class genericConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bars of the family [m]
    '''
    def __init__(self,genConf,identifier,diameter):
        self.genConf=genConf
        self.identifier=identifier
        self.diameter=diameter

    def getInitPntRebLref(self,rebarDraw):
        '''Return the initial point to start the reference line for labeling the rebar
        '''
        rebarEdges=rebarDraw.Edges
        #arrow in extremity 1
        pExtr1=rebarEdges[0].Vertexes[0].Point #vertex at extremity 1
        vArr=rebarEdges[0].tangentAt(0).multiply(0.9*self.genConf.texSize) #arrow vector
        l=Draft.rotate(Draft.makeLine(pExtr1,pExtr1.add(vArr)),15,pExtr1)
        FreeCADGui.ActiveDocument.getObject(l.Name).LineColor = cfg.colorArrows
        #arrow in extremity 2
        pExtr2=rebarEdges[-1].Vertexes[1].Point #vertex at extremity 2
        vArr=rebarEdges[-1].tangentAt(1).multiply(0.9*self.genConf.texSize) #arrow vector
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
        hText=self.genConf.texSize
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
        hText=self.genConf.texSize
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
                print('pp1=',pp1,'pp2=',pp2,'pEndRefL=',pEndRefL,'ppEndRefL=',ppEndRefL)
                c1=Part.Arc(pCentCirc+Vector(0,hText),pCentCirc+Vector(-hText,0),pCentCirc-Vector(0,hText))
            else:
                c1=Part.Arc(pp1,pEndRefL,ppEndRefL)
            c2=Part.Arc(pp2,ppText,ppCentCirc)
            l1=Part.makeLine(pp1,pp2)
            l2=Part.makeLine(ppEndRefL,ppCentCirc)
            etiq=Part.Wire([l1,c1.toShape(),l2,c2.toShape()]) 
            p=Part.show(etiq)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor = cfg.colorRefLines

    def drawSectRebarLref(self,startPnt,endPnt,vauxn):
        '''Draw the reference line for labeling a sectioned rebar family, or
        a family of stirrups in longitudinal section 
        Return the parameters to place the text

        :param startPnt: point position of the first rebar (center of the circle)
        :param startPnt: point position of the last rebar (center of the circle)
        :param vauxn: vector perpendicular to the line defined by the rebars pointing 
                      from concrete towards the rebars
        '''
        factPos=self.genConf.factPosLabelSectReb
        hText=self.genConf.texSize
        vaux=endPnt-startPnt
        vaux.normalize()
        vnorm=-1*vauxn.normalize()
        p1=startPnt+hText*vaux+self.genConf.factDispReflinSectReb*1.5*hText*vnorm
        p2=endPnt-hText*vaux+self.genConf.factDispReflinSectReb*1.5*hText*vnorm
        pol=Part.makePolygon([startPnt,p1,p2,endPnt])
        w=Part.show(pol)
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
            
    def labelSectRebar(self,startPnt,endPnt,vauxn):
        ''' Label (reference lines + text) a family of rebars sectioned.

        :param startPnt: point position of the first rebar (center of the circle)
        :param startPnt: point position of the last rebar (center of the circle)
        :param vauxn: vector perpendicular to the line defined by the rebars pointing 
                      from concrete towards the rebars
        '''
        justif,pText=self.drawSectRebarLref(startPnt,endPnt,vauxn)
        ptoSketch,pos=self.rebarText(justif,pText)
        return ptoSketch,pos
       
    def rebarText(self,justif,pText):
        '''Write the text that labels the rebar family

        :param pEndRefL: point extremity of the reference line where to start the rotulation
        :param pCentCirc: point to place the center of the cirle (wih id)
        :param justif: justification of the text ('Left' or 'Right')
        :param pText: point to place the text 
        '''
        hText=self.genConf.texSize
        if justif=="Left":
            txtColor=cfg.colorTextLeft
            if self.spacing == 0:
                tx=self.identifier + '  ' + str(int(self.nmbBars)) + '%%C' + str(int(1000*self.diameter))
            else:
                tx=self.identifier + '  %%C' + str(int(1000*self.diameter)) + 'c/' + str(self.spacing)
            ptoSketch=pText+Vector((len(tx)-2)*0.7*hText,0)
            pos='l'
        else:
            txtColor=cfg.colorTextRight
            if self.spacing == 0:
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

    :ivar genConf: instance of th class genericConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bar [m]
    :ivar spacing: spacing between bars [m]. If number of bars is defined 
          through parameter nmbBars, then spacing must be = 0 (default value 
          of spacing=0)
    :ivar nmbBars: number of rebars in the family. This parameter is only taken
          into account when spacing=0 (default value of spacing=0)
    :ivar lstPtsConcrSect: list of points in the concrete section to which 
          the bar is 'attached'
    :ivar lstCover: list of covers that correspond to each of the segments 
          defined with lstPtsConcrSect [m]. Defaults to the minimum cover 
          defined with 'genConf'
    :ivar coverSide: side to give cover  ('l' left side, 'r' for right side)
          (defaults to 'r')
    :ivar vectorLRef: vector to draw the leader line for labeling the bar
    :ivar fromToExtPts: starting and end points that delimit the stretch of 
          rebars. Defaults to None, in which case this length must be defined 
          by means of the attribute' extensionLength'.
    :ivar extensionLength: length of the stretch in which the rebar family extends.
          Defaults to None, in which case  this length must be defined 
          by means of the attribute 'fromToExtPts'.
    :ivar lateralCover: minimal lateral cover to place the rebar family.
          Defaults to the minimum cover given with 'genConf'.
    :ivar sectBarsSide: side of cover to draw the family as sectioned bars 
          (circles) ('l' left, 'r' right)
    :ivar coverSectBars: cover to draw the family as sectioned bars 
          (circles) ('l' left, 'r' right). Only needed if the bars are to be drawn.
          Defaults to the minimum cover given with 'genConf'. 
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
          negative cover given with 'genConf').
    :ivar gapEnd: increment (decrement if gapEnd<0) of the length of 
          the reinforcement at its ending extremity  (defaults to the minimum 
          negative cover given with 'genConf').
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
    :ivar compression: True if rebars in compression, False if rebars in tension.  Is used to
                    calculate lap lengths when splitting bars- (defaults to False)  
    :ivar drawSketch: True to draw mini-sketch of the rebars besides the text (defaults to True)
    '''
    def __init__(self,genConf,identifier,diameter,lstPtsConcrSect,fromToExtPts=None,extensionLength=None,lstCover=None,coverSide='r',vectorLRef=Vector(0.5,0.5),coverSectBars=None,lateralCover=None,sectBarsSide='r',spacing=0,nmbBars=0,lstPtsConcrSect2=[],gapStart=None,gapEnd=None,extrShapeStart=None,extrShapeEnd=None,fixLengthStart=None,fixLengthEnd=None,maxLrebar=12,position='poor',compression=False,drawSketch=True):
        super(rebarFamily,self).__init__(genConf,identifier,diameter)
        self.spacing=spacing 
        self.lstPtsConcrSect=lstPtsConcrSect
        if lstCover is None:
            self.lstCover=(len(lstPtsConcrSect)-1)*[genConf.cover]
        else:
            self.lstCover= lstCover
        self.coverSide=coverSide 
        self.vectorLRef= vectorLRef
        self.fromToExtPts= fromToExtPts
        self.extensionLength=extensionLength
        self.coverSectBars=coverSectBars if coverSectBars is not None else genConf.cover
        self.lateralCover=lateralCover if lateralCover is not None else genConf.cover
        self.sectBarsSide= sectBarsSide
        self.lstPtsConcrSect2=lstPtsConcrSect2
        self.listaPtosArm=[[],[]]
        self.nmbBars=nmbBars
        self.gapStart= gapStart if gapStart is not None else -genConf.cover
        self.gapEnd= gapEnd  if gapEnd is not None else -genConf.cover
        self.extrShapeStart=extrShapeStart
        self.extrShapeEnd=extrShapeEnd
        self.fixLengthStart=fixLengthStart
        self.fixLengthEnd=fixLengthEnd
        self.lstWire=None 
        self.wireSect2=None
        self.maxLrebar=maxLrebar
        self.position=position
        self.compression=compression
        self.drawSketch=drawSketch
    
    def drawSectBars(self,vTranslation=Vector(0,0,0)):
        '''Draw the rebar family as sectioned bars represented by circles in 
        the RC section.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        vaux=self.fromToExtPts[1]-self.fromToExtPts[0]
        Laux=vaux.Length
        if self.spacing==0:
            nesp=self.nmbBars-1
            distReb=Laux/(nesp+1)
        else:
            nesp=int((Laux-2.0*self.lateralCover-self.diameter)/self.spacing)
            distReb=self.spacing
        vaux.normalize()
        if self.sectBarsSide == 'l':
            vauxn=Vector(-vaux.y,vaux.x)
        else:
            vauxn=Vector(vaux.y,-vaux.x)
        vauxn.normalize()
        # first rebar
        if self.spacing==0:
            incrini=vaux.multiply(1/2*distReb)+(vauxn.multiply(self.coverSectBars+self.diameter/2.0))
        else:
            incrini=vaux.multiply((Laux-nesp*distReb)/2.0)+(vauxn.multiply(self.coverSectBars+self.diameter/2.0))
        cent=FreeCAD.Placement()
        cent.move(self.fromToExtPts[0].add(incrini).add(vTranslation))
        ptoIniEtiq=self.fromToExtPts[0].add(incrini).add(vTranslation)
        vaux.normalize()
        incr=vaux.multiply(distReb)
        for i in range(0,nesp+1):
            c=Draft.makeCircle(self.diameter/2.0,cent,False)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor =cfg.colorSectBars
            cent.move(incr)
        vaux.normalize()
        endPnt=ptoIniEtiq+vaux.multiply(distReb*nesp)
        self.labelSectRebar(ptoIniEtiq,endPnt,vauxn)
        return

    def drawLstRebar(self,vTranslation=Vector(0,0,0)):
        if self.lstWire==None:
            self.createLstRebar()
        for rw in self.lstWire:
            self.drawRebar(rw,vTranslation)
    
    def drawRebar(self,rebWire,vTranslation=Vector(0,0,0)):
        '''Represent the bar family in the RC section as a bar in its 
        true shape.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        # copy of the rebar wire to be depicted and applying of the translation
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
            wSketch=self.genConf.sketchScale*self.genConf.texSize
            hSketch=self.genConf.sketchScale*self.genConf.texSize
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
    #        ptoSketch=ptoTxt+Vector(0,-(self.genConf.texSize+bound.YLength/2))
            sketch.translate(ptoCDG.sub(cog))
            p=Part.show(sketch)
            FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorRebarSketch
#        drawMiniSketchRebar(rbFam=self,ptCOG=ptoSketch,wColumn=10*self.genConf.texSize,hRow=10*self.genConf.texSize,hText=0)
        return

    def createLstRebar(self):
        '''Create the wire that represents the true shape of a bar in the 
        family. In case of variable shape, a second wire is created according 
        to the shape defined for section2.
        '''
        lstPtRFam=self.getLstPtsRebar(self.lstPtsConcrSect)
        self.lstWire=self.getLstRebars(lstPtRFam)
        if len(self.lstPtsConcrSect2) > 0:
            lstPtsRebar2=self.getLstPtsRebar(self.lstPtsConcrSect2)
            lstLinRebar2=[Part.makeLine(lstPtsRebar2[i],lstPtsRebar2[i+1])for i in range(len(lstPtsRebar2)-1)]
            self.wireSect2=[(Part.Wire(lstLinRebar2))]
        

    def getLstPtsRebar(self,lstPtsConcr):
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
            if self.coverSide == 'l':
                vauxn=Vector(-vaux.y,vaux.x)
            else:
                vauxn=Vector(vaux.y,-vaux.x)
            vauxn.normalize()
            vauxn.multiply(self.lstCover[i]+self.diameter/2.0)
            listaaux.append(lstPtosAux[i].add(vauxn))
            listaaux.append(lstPtosAux[i+1].add(vauxn))

        lstPtsRebar=[listaaux[0]]
        for i in range (1,npuntos-1):
            pint=geom_utils.int2lines(listaaux[2*(i-1)],listaaux[2*(i-1)+1],listaaux[2*i],listaaux[2*i+1])
            lstPtsRebar.append(pint)

        lstPtsRebar.append(listaaux[2*(npuntos-1)-1])
        
        # Start extremity: gaps, straight elongation, hooks
        vaux=lstPtsRebar[1].sub(lstPtsRebar[0]).normalize()
        if self.fixLengthStart != None:
            lstPtsRebar[0]=lstPtsRebar[1].sub(vaux.multiply(self.fixLengthStart))
        else:
            lstPtsRebar[0]=lstPtsRebar[0].sub(vaux.multiply(self.gapStart))
        if self.extrShapeStart is not None:
            extrShAng,extrShLn=self.getExtrShapeParams(self.extrShapeStart)
            vaux=lstPtsRebar[1].sub(lstPtsRebar[0]).normalize()
            if extrShAng == 0:  #straight elongation
                lstPtsRebar[0]=lstPtsRebar[0].sub(vaux.multiply(extrShLn))
            else: #hook
                lstPtsRebar[0]=lstPtsRebar[0].add(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                firstPoint=lstPtsRebar[0].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.insert(0,firstPoint)
#                self.lstCover.insert(0,0)
                
        # End extremity: gaps, straight elongation, hooks
        vaux=lstPtsRebar[-1].sub(lstPtsRebar[-2]).normalize()
        if self.fixLengthEnd != None:
            lstPtsRebar[-1]=lstPtsRebar[-2].add(vaux.multiply(self.fixLengthEnd))
        else:
            lstPtsRebar[-1]=lstPtsRebar[-1].add(vaux.multiply(self.gapEnd))
        if self.extrShapeEnd is not None:
            extrShAng,extrShLn=self.getExtrShapeParams(self.extrShapeEnd)
            vaux=lstPtsRebar[-1].sub(lstPtsRebar[-2]).normalize()
            if extrShAng == 0:  #straight elongation
                lstPtsRebar[-1]=lstPtsRebar[-1].add(vaux.multiply(extrShLn))
            else: #hook
                lstPtsRebar[-1]=lstPtsRebar[-1].sub(vaux.multiply(self.diameter/2.))
                vauxHook=DraftVecUtils.rotate(vaux,math.radians(extrShAng),Vector(0,0,1))
                vauxHook.normalize()
                endPoint=lstPtsRebar[-1].add(vauxHook.multiply(extrShLn))
                lstPtsRebar.append(endPoint)
        return lstPtsRebar
        
                 
    def getLstRebars(self,lstPtsRebar):
        '''Checks the length of the rebar defined by the list of points lstPtsRebar. If 
        it is less than maxLrebar returns a list with the wire defined by those points,
        otherwise, the rebar is splitted in pieces of length less or equal than maxLrebar,
        and a list of wires is returned.

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
            eta1=1.0 if self.position=='good' else 0.7
            contrReb=Lcalc.RebarController(concreteCover=self.genConf.cover, spacing=self.spacing, eta1=eta1, compression= self.compression) # create rebar controllers to calculate anchor or gap lengths
            lapLenght=contrReb.getLapLength(concrete= self.genConf.xcConcr, rebarDiameter=self.diameter, steel=self.genConf.xcSteel, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= 1.0)
            
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
#                length2add=lstDist[indLmax-1]-LtoAdd1+lapLenght
#                firstPnt=lstPtsRebar[0].add(-length2add*vaux)
                firstPnt=lastPnt1.add(-lapLenght*vaux)
                lstPtsRebar.insert(0,firstPnt)
                lstDist=[lstPtsRebar[i].distanceToPoint(lstPtsRebar[i+1]) for i in range(len(lstPtsRebar)-1)]
                lstCumDist=[0]+[sum(lstDist[:y]) for y in range(1, len(lstDist) + 1)] # cummulated lengths
            lstLinRebar=[Part.makeLine(lstPtsRebar[i],lstPtsRebar[i+1])for i in range(len(lstPtsRebar)-1)]
            lstRebars.append(Part.Wire(lstLinRebar))
        return lstRebars
    
    def getNumberOfBars(self):
        '''Return the number of bars in the family.
        '''
        if self.spacing == 0:
            nBar=self.nmbBars
        elif self.extensionLength:
            nBar=int(self.extensionLength/self.spacing)+1
        else:
            vaux=self.fromToExtPts[1].sub(self.fromToExtPts[0])
            Laux=vaux.Length
            nesp=int((Laux-2.0*self.lateralCover-self.diameter)/self.spacing)
            nBar=nesp+1
        return nBar

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
            contrReb=Lcalc.RebarController(concreteCover=self.genConf.cover, spacing=self.spacing, eta1=eta1, compression= compression) # create rebar controllers to calculate anchor or gap lengths
        elif rbEndType in ['fix']:
            rbEndLenght=eval(paramAnc[1].replace('len',''))/1000 # longitud en metros
        else:
            print('rebar end in family ', self.identifier,' must be of type "anc" (anchoring), "lap" (lapping) or "fix" (fixed length)')
        if rbEndType=='anc': # anchor length is calculated
            barShape='bent' if (angle>0) else 'straight'
            rbEndLenght=contrReb.getDesignAnchorageLength(concrete=self.genConf.xcConcr, rebarDiameter=self.diameter, steel=self.genConf.xcSteel, steelEfficiency= 1.0, barShape= barShape)
        elif rbEndType[:4]=='lap': #lap length id calculated
            ratio=1.0
            if len(paramAnc)>3:
                ratio=eval(paramAnc[3].replace('perc',''))/100
            rbEndLenght=contrReb.getLapLength(concrete= self.genConf.xcConcr, rebarDiameter=self.diameter, steel=self.genConf.xcSteel, steelEfficiency= 1.0, ratioOfOverlapedTensionBars= ratio)
        return (angle,rbEndLenght)
    
    def getTextFiSpacing(self):
        '''Return the text for column '%%C/SEP.' of the bar schedule'''
        formatSpacing='%.'+str(self.genConf.decSpacing)+'f'
        if self.spacing ==0:
            txt='%%C' + str(int(1000*self.diameter))
        else:
            if dsu.get_number_decimal_positions(self.spacing)>self.genConf.decSpacing:
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
    ''' Family of shear reinforcement (for now, only rectangular stirrups)

    :ivar genConf: instance of th class genericConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bar [m]
    :ivar lstPtsConcrTransv: list of points in the transversal 
          concrete section to which the first stirrup 
          (rectangular drawing) is 'attached' (4 points)
    :ivar lstPtsConcrLong: list of points in the longitudinal section to which 
          the first stirrup (rectangular drawing) is 'attached'
    :ivar spacStrpTransv: spacement between stirrups in the transversal 
                  section (as in beams, where they are displayed as 
                  rectangles)
    :ivar spacStrpLong: spacement between stirrups in the longitudinal 
          section (as in beams, where they are displayed as lines)
    :ivar vDirLong: vector to define the longitudinal direction
    :ivar nmbStrpTransv: number of stirrups displayed as rectangles
    :ivar nmbStrpLong: number of stirrups displayed as lines
    :ivar lstCover: list of covers for each side of the stirrup. If 
          None, genConf.cover is taken for all sides.
    :ivar dispStrpTransv: displacement of stirrups in the
          transversal section (defaults to None)
    :ivar dispStrpLong: displacement of stirrups in the
          longitudinal section (defaults to None)
    :ivar vectorLRef: vector to draw the leader line for labeling the bar (defaults to Vector(0.5,0.5)
    :ivar sideLabelLn: side to place the label of the stirrups in longitudinal section (defaults to 'l')
    '''
    def __init__(self,genConf,identifier,diameter,lstPtsConcrTransv,lstPtsConcrLong,spacStrpTransv,spacStrpLong,vDirLong,nmbStrpTransv,nmbStrpLong,lstCover=None,dispStrpTransv=None,dispStrpLong=None,vectorLRef=Vector(0.5,0.5),sideLabelLn='l'):
        super(stirrupFamily,self).__init__(genConf,identifier,diameter)
        self.lstPtsConcrTransv=lstPtsConcrTransv
        self.lstPtsConcrLong=lstPtsConcrLong
        self.spacStrpTransv=spacStrpTransv
        self.spacStrpLong=spacStrpLong
        self.vDirLong=vDirLong
        self.nmbStrpTransv=nmbStrpTransv
        self.nmbStrpLong=nmbStrpLong
        self.dispStrpTransv=dispStrpTransv
        self.dispStrpLong=dispStrpLong
        self.vectorLRef=vectorLRef
        self.sideLabelLn=sideLabelLn
        self.lstCover=lstCover
        self.rebarWire=None
        self.lstWire=None
        self.wireSect2=None

    def getVdirTrans(self):
        '''return a unitary direction vector in transversal section'''
        v=self.lstPtsConcrTransv[1]-self.lstPtsConcrTransv[0]
        return v.normalize()
    
    def getVdirLong(self):
        '''return a unitary direction vector in longitudinal section'''
        return self.vDirLong.normalize()

    def getLstCoverAxis(self):
        if not self.lstCover:
            self.lstCover=4*[self.genConf.cover]
        lstCoverAxis=[c+self.diameter/2 for c in self.lstCover]
        return lstCoverAxis
        
    def createLstRebar(self):
        '''Note; This part should be transfered to the base class
        '''
        lstCoverAxis=self.getLstCoverAxis()
        vTr=self.getVdirTrans()
        vPerp=(self.lstPtsConcrTransv[0]-self.lstPtsConcrTransv[3]).normalize()
        lstPtsRebar=[self.lstPtsConcrTransv[0]+lstCoverAxis[3]*vTr-lstCoverAxis[0]*vPerp,
                       self.lstPtsConcrTransv[1]-lstCoverAxis[1]*vTr-lstCoverAxis[0]*vPerp,
                       self.lstPtsConcrTransv[2]-lstCoverAxis[1]*vTr+lstCoverAxis[2]*vPerp,
                       self.lstPtsConcrTransv[3]+lstCoverAxis[3]*vTr+lstCoverAxis[2]*vPerp]
        lstLinRebar=[Part.makeLine(lstPtsRebar[i],lstPtsRebar[i+1])for i in range(len(lstPtsRebar)-1)]
        lstLinRebar+=[Part.makeLine(lstPtsRebar[-1],lstPtsRebar[0])]
        self.rebarWire=Part.Wire(lstLinRebar)
        self.lstWire=[self.rebarWire]
    
    def drawRebars(self,vTranslation=Vector(0,0,0)):
        if not self.rebarWire:
            self.createLstRebar()
        vTr=self.getVdirTrans()
        rebarDraw=self.rebarWire.copy()
        rebarDraw.translate(vTranslation)
        if self.dispStrpTransv:
            rebarDraw.translate(self.dispStrpTransv*vTr)
        rebarFillet= Draft.make_wire(rebarDraw,closed=True,face=False)
        rad=RCutils.bend_rad_hooks_EHE(self.diameter*1e3)/1e3
        rebarFillet.FilletRadius=rad
        FreeCADGui.ActiveDocument.getObject(rebarFillet.Name).LineColor = cfg.colorRebars
        for i in range(1,self.nmbStrpTransv):
            stirr=rebarDraw.copy()
            stirr.translate(i*self.spacStrpTransv*vTr)
            stirrFillet=Draft.make_wire(stirr,closed=True,face=False)
            stirrFillet.FilletRadius=rad
            FreeCADGui.ActiveDocument.getObject(stirrFillet.Name).LineColor = cfg.colorRebars
        FreeCADGui.ActiveDocument.Document.recompute()
        ptoIniEtiq=self.getInitPntRebLref(rebarDraw)
        pEndRefL,pCentCirc,justif,pText=self.drawRebarLref(ptoIniEtiq,self.vectorLRef)
        self.drawDecorId(pEndRefL,pCentCirc,justif)
        ptoSketch,pos=self.rebarText(justif,pText)
        
    def drawLnRebars(self,vTranslation=Vector(0,0,0)):
        lstCoverAxis=self.getLstCoverAxis()
        vLn=self.getVdirLong()
        vReb=(self.lstPtsConcrLong[1]-self.lstPtsConcrLong[0]).normalize()
        lstPtsRebar=[self.lstPtsConcrLong[0]+lstCoverAxis[2]*vReb,
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
        if self.sideLabelLn=='l':
            vauxn=Vector(endPnt.y-startPnt.y,startPnt.x-endPnt.x)
        else:
            vauxn=Vector(startPnt.y-endPnt.y,endPnt.x-startPnt.x)
        vauxn.normalize()
        self.labelSectRebar(startPnt,endPnt,vauxn)

    def rebarText(self,justif,pText):
        '''Write the text that labels the rebar family

        :param pEndRefL: point extremity of the reference line where to start the rotulation
        :param pCentCirc: point to place the center of the cirle (wih id)
        :param justif: justification of the text ('Left' or 'Right')
        :param pText: point to place the text 
        '''
        hText=self.genConf.texSize
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
        if self.spacStrpLong>0:
            txt+=str(self.spacStrpLong)+'/'
        if self.spacStrpTransv>0:
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
 
                
def barSchedule(lstBarFamilies,config=scheduleConf(),title='  ',pntTLcorner=Vector(0,0),doc=FreeCAD.ActiveDocument):
    ''' Create the rebar schedule from a list of rebar families

    :param config: instance of scheduleConf class
    :param lstBarFamilies: ordered list of rebar families to be included in 
           the schedule
    :param wColumns: list of column widths for the table 
    (correspond to identifier, sketch, diam. and spacing., Number of bars, 
    length of each bar, total weight of the family)
    :param hRows: rows height
    :param hText: text height
    :param hTextSketch: text height for the sketch.
    :param title: title for the rebar schedule (defaults to None)
    :param pntTLcorner: point in top-left corner (defaults to Vector(0,0))
    :param doc: document in which to put the schedule (defaults to the 
                active document)
    '''
    FreeCAD.setActiveDocument(doc.Name)
    wColumns=config.widthColumns
    hRows=config.heightRows
    hText=config.heightText
    hTextSketch=config.heigthTextSketch
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
        formatLength='%.'+str(rbFam.genConf.decLengths)+'f'
        formatSpacing='%.'+str(rbFam.genConf.decSpacing)+'f'
        if rbFam.lstWire==None:
            rbFam.createLstRebar()
        for i in range(len(rbFam.lstWire)):
            #identifier
            pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
            dt.put_text_in_pnt(rbFam.identifier,pPos, hText,cfg.colorTextLeft)
            #sketch
            pEsq=pLinea.add(Vector(wColumns[0] + wColumns[1]/2.0,0))
            rW2=rbFam.wireSect2[i] if rbFam.wireSect2 else None
            barLength,barLengthTxt=drawSketchRebarShape(rbFam.lstWire[i],pEsq,wColumns[1],hRows,hTextSketch,rbFam.genConf.decLengths,rW2)
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
        print(s)
        f.write(s)
    f.close()
        
def drawConcreteSection(lstPtsConcrSect,vTranslation=Vector(0,0,0)):
    ''' Draw a section of concrete defined by a list of points in the FreeCAD 
    active document

    :param lstPtsConcrSect: list of ordered lists of points to draw the 
           concrete section. Each list of points originates an open wire.
    :param vTranslation: Vector to apply a traslation to the RC section drawing.
           It facilitates the adding of several RC-sections to the same sheet of
           FreeCAD.
    '''
    l=Part.makePolygon(lstPtsConcrSect)
    l.translate(vTranslation)
    p=Part.show(l)
    FreeCADGui.ActiveDocument.getObject(p.Name).LineColor =cfg.colorConcrete
    


def drawRCSection(lstOfLstPtsConcrSect=None,lstShapeRebarFam=None,lstSectRebarFam=None,lstShapeStirrupFam=None,lstEdgeStirrupFam=None,vTranslation=Vector(0,0,0)):
    '''Draw a reinforced concrete section in the FreeCAD active document

    :param lstOfLstPtsConcrSect: list of ordered lists of points to draw the 
           concrete section. Each list of points originates an open wire.
           (defaults to None)
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
    '''
    if lstOfLstPtsConcrSect:
        #draw the concrete section
        for lp in lstOfLstPtsConcrSect:
            drawConcreteSection(lp,vTranslation)
    if lstShapeRebarFam:
        #draw the rebars in their true shape
        for rbFam in lstShapeRebarFam:
            rbFam.drawLstRebar(vTranslation)
    if lstSectRebarFam:
        #draw the sectioned rebars
        for rbFam in lstSectRebarFam:
            rbFam.drawSectBars(vTranslation)
    if lstShapeStirrupFam:
        for stFam in lstShapeStirrupFam:
            stFam.drawRebars(vTranslation)
    if lstEdgeStirrupFam:
        for stFam in lstEdgeStirrupFam:
            stFam.drawLnRebars(vTranslation)       
            





def rect_stirrup(genConf,identifier,diameter,nmbStirrups,width,height):
    ''' define a closed rectangular stirrup for the quantities schedule
    only, not for drawing it.
    
    :param genConf: instance of th class genericConf that defines generic
          parameters like concrete and steel type, text format, ... 
    :param identifier: identifier of the rebar family
    :param diameter: diameter of the bar [m]
    :param nmbStirrups: number of stirrups
    :param width: width of the stirrup (in the axis of the bar)
    :param height: height of the stirrup (in the axis of the bar)
    '''
    paux1=Vector(0,height)
    paux2=Vector(width,height)
    paux3=Vector(width,0)
    paux4=Vector(0,0)
    rbf=rebarFamily(genConf=genConf,identifier=identifier,diameter=diameter,nmbBars=nmbStirrups,lstPtsConcrSect=[paux1,paux2,paux3,paux4,paux1])
    return rbf
    
                      

                    
