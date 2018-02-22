# -*- coding: iso-8859-1 -*-
from __future__ import division

__author__= "Ana Ortega (AO_O) "
__copyright__= "Copyright 2017, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= "ana.ortega@xcengineering.xyz "

import Part, FreeCAD, math
import Draft
from FreeCAD import Vector
import FreeCADGui
from freeCAD_utils import geom_utils
from freeCAD_utils import drawing_tools as dt

#Default bending radius (EHE-08, B 500 S: 10fi para fi<=25 mm, 20fi para fi>25 mm)  
defBendingRad={'0.008':0.08,'0.01':0.10,'0.012':0.12,'0.014':0.14,'0.016':0.16,'0.02':0.20,'0.025':0.25,'0.032':0.64,'8':80,'10':100,'12':120,'14':140,'16':160,'20':200,'25':250,'32':640}   #bending radius
'''
class genericConf(object):
    generic parameteters to be used as default values for several 
    attributes of different rebar families

    :ivar cover:   minimum cover
    :ivar texSize: generic size of text to label rebar families in the 
          drawings
    :ivar dictBendingRad: 

'''


class rebarFamily(object):
    '''Family of reinforcement bars

    :ivar identifier: identifier of the rebar family
    :ivar diameter: diameter of the bar [m]
    :ivar spacing: spacing between bars [m]. If number of bars is defined 
          through parameter nmbBars, then spacing must be = 0 (default value of spacing=0)
    :ivar nmbBars: number of rebars in the family. This parameter is only taken
          into account when spacing=0 (default value of spacing=0)
    :ivar lstPtsConcrSect: list of points in the concrete section to which 
          the bar is 'attached'
    :ivar lstCover: list of covers that correspond to each of the segments 
          defined with lstPtsConcrSect [m]
    :ivar coverSide: side to give cover  ('l' left side, 'r' for right side)
    :ivar vectorLRef: vector to draw the leader line for labeling the bar
    :ivar fromToExtPts: starting and end points that delimit the stretch of 
          rebars.
    :ivar lateralCover: minimal lateral cover to place the rebar family
    :ivar sectBarsSide: side of cover to draw the family as sectioned bars 
          (circles) ('l' left, 'r' right)
    :ivar vectorLRefSec: vector to draw the leader line for labeling the 
          sectioned bar drawing
    :ivar wire: FreeCAD object of type wire that represents the rebar shape
                ( or the rebar shape in section 1 when it is variable).
    :ivar wireSect: FreeCAD object of type wire that represents the rebar at
                    section 2 when the shape of rebars in the family varies 
                    uniformily from section 1 to section 2.
    :ivar lstPtsConcrSect2: parameter only used when defining a rebar family
          with variable shape. In that case, lstPtsConcrSect2 is the list of 
          points in the concrete section 2 to which the bar is 'attached'
    :ivar decLengths: decimal positions to calculate and express lengths and
                      their derivated magnitudes, like weight  (defaults to 2).
    :param decSpacing: decimal positions to express the spacing (defaults to 2).
    :ivar gapStart: increment (decrement if gapStart <0) of the length of 
          the reinforcement at its starting extremity (defaults to 0).
    :ivar gapEnd: increment (decrement if gapEnd<0) of the length of 
          the reinforcement at its ending extremity (defaults to 0).
    :ivar hText: text height (defaults to 0.125)
    :param fixLengthStart: fixed length of the first segment of the rebar 
           (defaults to None = no fixed length)
    :param fixLengthEnd: fixed length of the last segment of the rebar 
           (defaults to None = no fixed length)
    :ivar bendingRad: bending radius (defaults to 10fi if fi<25 mm and
          20fi if fi>25mm)

    '''
    def __init__(self,identifier,diameter,lstPtsConcrSect,lstCover,coverSide,vectorLRef,fromToExtPts,recSec,lateralCover,sectBarsSide,vectorLRefSec,spacing=0,nmbBars=0,lstPtsConcrSect2=[],decLengths=2,decSpacing=2,gapStart=0,gapEnd=0,hText=0.125,fixLengthStart=None,fixLengthEnd=None):
        self.identifier=identifier 
        self.diameter=diameter
        self.spacing=spacing 
        self.lstPtsConcrSect=lstPtsConcrSect 
        self.lstCover= lstCover
        self.coverSide=coverSide 
        self.vectorLRef= vectorLRef
        self.hText= hText
        self.fromToExtPts= fromToExtPts
        self.recSec= recSec
        self.lateralCover=lateralCover 
        self.sectBarsSide= sectBarsSide
        self.vectorLRefSec=vectorLRefSec
        self.lstPtsConcrSect2=lstPtsConcrSect2
        self.decLengths=decLengths
        self.decSpacing=decSpacing
        self.listaPtosArm=[[],[]]
        self.nmbBars=nmbBars
        self.gapStart= gapStart
        self.gapEnd= gapEnd
        self.fixLengthStart=fixLengthStart
        self.fixLengthEnd=fixLengthEnd
        self.bendingRad= defBendingRad[str(diameter)]
        self.wire=None 
        self.wireSect2=None
      
    
    def drawSectBars(self,vTranslation=Vector(0,0,0)):
        '''Draw the rebar family as sectioned bars represented by circles in 
        the RC section.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        vaux=self.fromToExtPts[1].sub(self.fromToExtPts[0])
        Laux=vaux.Length
        nesp=int((Laux-2.0*self.lateralCover-self.diameter)/self.spacing)
        vaux.normalize()
        if self.sectBarsSide == 'l':
            vauxn=Vector(-vaux.y,vaux.x)
        else:
            vauxn=Vector(vaux.y,-vaux.x)
        vauxn.normalize()
        incrini=vaux.multiply((Laux-nesp*self.spacing)/2.0).add(vauxn.multiply(self.recSec+self.diameter/2.0))
        cent=FreeCAD.Placement()
        cent.move(self.fromToExtPts[0].add(incrini).add(vTranslation))
        ptoIniEtiq=self.fromToExtPts[0].add(incrini).add(vTranslation)
        rebarText(ptoIniEtiq,self.vectorLRefSec,self.identifier,self.diameter,self.spacing,0,self.hText)
        vaux.normalize()
        incr=vaux.multiply(self.spacing)
        for i in range(0,nesp+1):
            c=Draft.makeCircle(self.diameter/2.0,cent,False)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,0.00,0.00)
            cent.move(incr)
        p1=ptoIniEtiq.add(self.vectorLRefSec)
        vaux.normalize()
        p2=p1.add(vaux.multiply(self.spacing*nesp)).sub(self.vectorLRefSec)
        w=Draft.makeWire([p1,p2])
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
        return

    def drawRebar(self,vTranslation=Vector(0,0,0)):
        '''Represent the bar family in the RC section as a bar in its 
        true shape.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        if self.wire==None:
            self.createRebar()
        # copy of the rebar wire to be depicted and applying of the translation
        #flechas en extremos de barra
        rebarDraw=self.wire.copy()
        rebarDraw.translate(vTranslation)
        Part.show(rebarDraw)
        rebarEdges=rebarDraw.Edges
        #arrow in extremity 1
        pExtr1=rebarEdges[0].Vertexes[0].Point #vertex at extremity 1
        vArr=rebarEdges[0].tangentAt(0).multiply(self.hText/2.0) #arrow vector
        Draft.rotate(Draft.makeLine(pExtr1,pExtr1.add(vArr)),15,pExtr1)
        #arrow in extremity 2
        pExtr2=rebarEdges[-1].Vertexes[1].Point #vertex at extremity 2
        vArr=rebarEdges[-1].tangentAt(1).multiply(self.hText/2.0) #arrow vector
        Draft.rotate(Draft.makeLine(pExtr2,pExtr2.add(vArr)),180-15,pExtr2)
        # Texts
        ptoIniEtiq=rebarEdges[int(len(rebarEdges)/2.)].CenterOfMass
        rebarText(ptoIniEtiq,self.vectorLRef,self.identifier,self.diameter,self.spacing,self.nmbBars,self.hText)
        return

    def createRebar(self):
        '''Create the wire that represents the true shape of a bar in the 
        family. In case of variable shape, a second wire is created according 
        to the shape defined for section2.
        '''
        self.wire=self.getRebar(self.lstPtsConcrSect)
        self.wireLengths=[round(edg.Length,self.decLengths) for edg in self.wire.Edges]
        if len(self.lstPtsConcrSect2) > 0:
            self.wireSect2=self.getRebar(self.lstPtsConcrSect2)
            self.wireSect2Lengths=[round(edg.Length,self.decLengths) for edg in self.wireSect2.Edges]

    def getRebar(self,lstPtsConcr):
        '''Return the wire that represents the true shape of the bar defined
        by the points of the concrete section listed in lstPtsConcr.

        :param lstPtsConcr: ordered list of points in the concrete section 
        to which the rebar is 'attached'. 
        '''
        npuntos=len(lstPtsConcr)
        lstPtosAux=[pt for pt in lstPtsConcr]
        vaux=lstPtosAux[0].sub(lstPtosAux[1]).normalize()
        if self.fixLengthStart != None:
            lstPtosAux[0]=lstPtosAux[1].add(vaux.multiply(self.fixLengthStart))
        else:
            lstPtosAux[0]=lstPtosAux[0].add(vaux.multiply(self.gapStart))
        vaux=lstPtosAux[-1].sub(lstPtosAux[-2]).normalize()
        if self.fixLengthEnd != None:
            lstPtosAux[-1]=lstPtosAux[-2].add(vaux.multiply(self.fixLengthEnd))
        else:
            lstPtosAux[-1]=lstPtosAux[-1].add(vaux.multiply(self.gapEnd))
        listaaux=[]
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

        lstPtsArm=[listaaux[0]]
        for i in range (1,npuntos-1):
            pint=geom_utils.int2lines(listaaux[2*(i-1)],listaaux[2*(i-1)+1],listaaux[2*i],listaaux[2*i+1])
            lstPtsArm.append(pint)

        lstPtsArm.append(listaaux[2*(npuntos-1)-1])
        lstLines=[Part.Line(lstPtsArm[i],lstPtsArm[i+1]).toShape() for i in range(len(lstPtsArm)-1)]
        rebarWire=Part.Wire(lstLines)
        return rebarWire

    def getNumberOfBars(self):
        '''Return the number of bars in the family.
        '''
        if self.spacing == 0:
            nBar=self.nmbBars
        else:
            vaux=self.fromToExtPts[1].sub(self.fromToExtPts[0])
            Laux=vaux.Length
            nesp=int((Laux-2.0*self.lateralCover-self.diameter)/self.spacing)
            nBar=nesp+1
        return nBar

    def getUnitWeight(self):
        '''Return the weigth [kg] per meter of bar
        '''
        if self.diameter <=12e-3:
            unitWeigth=round(math.pi*self.diameter**2.0/4.*7850,3)
        else:
            unitWeigth=round(math.pi*self.diameter**2.0/4.*7850,2)
        return unitWeigth
        
                        
    

def rebarText(ptoInic,vectorLRef,idArm,diamArm,sepArm,nBarr,hText):
    '''Rotulacion de un grupo de barras de armado

    :param ptoInic: pto del que arranca la linea de referencia
    :param vectorLRef: primer tramo de la linea de referencia
    :param idArm: identifier de la armadura
    :param diamArm: diámetro de la armadura
    :param sepArm: spacing entre barras
    :param nBarr: nº de barras (sólo se tiene en cuenta cuando sepArm=0)
    :param hText: altura del texto
    '''
    p2=ptoInic.add(vectorLRef)
    signo=1.0*vectorLRef.x/abs(vectorLRef.x)
    p3=p2.add(Vector(signo*hText,0))
    p4=p3.add(Vector(signo*hText,0))
    p5=p3.add(Vector(signo*hText/2.0,-hText/2.0))
    w=Draft.makeWire([ptoInic,p2,p3])
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    if len(idArm)==1:
        pl=FreeCAD.Placement()
        pl.move(p4)
        c=Draft.makeCircle(hText*(len(idArm)+1)/2.0,pl,False)
        FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,1.00,0.00)
    else:
        pp1=p4.add(Vector(0,hText))
        pp2=p4.add(Vector(signo*hText*(len(idArm)-1),hText))
        pp3=p4.add(Vector(0,-hText))
        pp4=p4.add(Vector(signo*hText*(len(idArm)-1),-hText))
        pp5=p4.add(Vector(signo*hText*len(idArm),0))
        c1=Part.Arc(pp1,p3,pp3)
        c2=Part.Arc(pp2,pp5,pp4)
        l1=Part.Line(pp1,pp2)
        l2=Part.Line(pp3,pp4)
        etiq=Part.Wire([l1.toShape(),c1.toShape(),l2.toShape(),c2.toShape()])
        Part.show(etiq)
    if vectorLRef.x > 0:
        justif="Left"
        if sepArm == 0:
            tx=idArm + '  ' + str(int(nBarr)) + '%%C' + str(int(1000*diamArm))
        else:
            tx=idArm + '  %%C' + str(int(1000*diamArm)) + 'c/' + str(sepArm)
    else:
        justif="Right"
        if sepArm == 0:
            tx=str(int(nBarr)) + '%%C' + str(int(1000*diamArm)) + '   ' + idArm
        else:
            tx='%%C' + str(int(1000*diamArm)) + 'c/' + str(sepArm) +'   ' + idArm 
    dt.put_text_in_pnt(text=tx,point=p5,hText=hText,justif=justif)
    return
    
def drawSketchRebarShape(rbFam,ptCOG,wColumn,hRow,hText):
    '''Draw the shape skectch of the rbFam reinforcment bar in the bar 
    schedule. Return the total length of the rebar.

    :param rbFam: family of rebars to be represented.
    :param ptCOG:  point where to place the center of gravity of the sketch.
    :param wColumn: width of the column 'Shape' in the bar schedule.
    :param hRow: height of the row in the bar schedule.
    :param hText: height of the text to label the sketch.
    '''
    sketch=rbFam.wire.copy()
    bound=sketch.BoundBox
    cog=sketch.CenterOfMass
    if bound.YLength > bound.XLength:
        sketch.rotate(cog,Vector(0,0,1),-90)
        bound=sketch.BoundBox
    if bound.YLength==0:
        fScale=(0.85*wColumn)/(bound.XLength)
    else:
        fScale=min((0.9*wColumn)/(bound.XLength),hRow/(bound.YLength))
    sketch.scale(fScale,cog)
    sketch.translate(ptCOG.sub(cog))
    Part.show(sketch)
    #Texts
    lengthsText=[str(i) for i in rbFam.wireLengths]
    totalLength=sum(rbFam.wireLengths)
    totalLengthTxt=str(totalLength)
    if rbFam.wireSect2 != None:
        lengthsText=[(lengthsText[i]+'..'+str(rbFam.wireSect2Lengths[i])) if rbFam.wireLengths[i]!=rbFam.wireSect2Lengths[i] else lengthsText[i] for i in range(len(rbFam.wireLengths))]
        totalLength=(totalLength+sum(rbFam.wireSect2Lengths))/2.0
        totalLengthTxt+='...'+str(sum(rbFam.wireSect2Lengths))
    sketchEdges=sketch.Edges
    for i in zip(sketchEdges,lengthsText):
        edg=i[0]
        dt.put_text_in_pnt(text=i[1],point=edg.CenterOfMass,hText=hText,justif="Center",rotation=math.degrees(edg.tangentAt(0).getAngle(Vector(1,0,0))))
    return (totalLength,totalLengthTxt)


                
def barSchedule(lstBarFamilies,wColumns,hRows,hText,hTextSketch):
    ''' Cuadro de despiece de la armadura 

    :param lstBarFamilies: ordered list of rebar families to be included in 
           the schedule
    :param wColumns: list of column widths for the table 
    (correspond to identifier, sketch, diam. and spacing., Number of bars, 
    length of each bar, total weight of the family)
    :param hRows: rows height
    :param hText: text height
    :param hTextSketch: text height for the sketch.
    '''
    #lstBarFamilies=familiasArmad.items() #creamos una lista a partir del diccionario para poder ordenar los valores
    #lstBarFamilies.sort()
    anchoTotal=sum(wColumns)
    w=Draft.makeRectangle(anchoTotal,hRows*(len(lstBarFamilies)+1))
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    p1=Vector(0,0)
    p2=p1.add(Vector(0,hRows*(len(lstBarFamilies)+1)))
    for i in range (0,len(wColumns)):
        p1=p1.add(Vector(wColumns[i],0))
        p2=p2.add(Vector(wColumns[i],0))
        w=Draft.makeLine(p1,p2)
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)

    p1=Vector(0,hRows*(len(lstBarFamilies)))
    p2=p1.add(Vector(anchoTotal,0))
    w=Draft.makeLine(p1,p2)
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)

    #Títulos para la tabla de despiece
    pLinea=p1.add(Vector(0,hRows/2.0))
    pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('POS.',pPos,hText)
    pEsq=pLinea.add(Vector(wColumns[0]+wColumns[1]/2.0,-hText/2.0))
    dt.put_text_in_pnt('ESQUEMA',pEsq,hText,"Center")
    pFiSep=pLinea.add(Vector(wColumns[0]+wColumns[1]+hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('%%C/SEP.',pFiSep.add(Vector(0,hText)), hText)
    dt.put_text_in_pnt('(mm)/(m)',pFiSep.add(Vector(0,-hText)), hText)
    pNbarras=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('NUM.',pNbarras, hText, "Right")
    pLbarra=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]+wColumns[4]-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('LONG.(m)',pLbarra, hText, "Right")
    pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('PESO',pPeso.add(Vector(0,hText)), hText, "Right")
    dt.put_text_in_pnt('(Kg)',pPeso.add(Vector(0,-hText)), hText, "Right")
    pLinea=p1.add(Vector(0,-hRows/2.0))
    pesoTotal=0
    for rbFam in lstBarFamilies:
        formatLength='%.'+str(rbFam.decLengths)+'f'
        formatSpacing='%.'+str(rbFam.decSpacing)+'f'
        if rbFam.wire==None:
            rbFam.createRebar()
        #identifier
        pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
        dt.put_text_in_pnt(rbFam.identifier,pPos, hText)
        #sketch
        pEsq=pLinea.add(Vector(wColumns[0] + wColumns[1]/2.0,0))
        barLength,barLengthTxt=drawSketchRebarShape(rbFam,pEsq,wColumns[1],hRows,hTextSketch)
        pFiSep=pLinea.add(Vector(sum(wColumns[:2])+hText/2.0,-hText/2.0))
        if rbFam.spacing ==0:
            tx='%%C' + str(int(1000*rbFam.diameter))
        else:
            tx='%%C' + str(int(1000*rbFam.diameter)) + 'c/' + formatSpacing %rbFam.spacing
        dt.put_text_in_pnt(tx,pFiSep, hText)
        #number of bars
        pNbarras=pLinea.add(Vector(sum(wColumns[:4])-hText/2.0,-hText/2.0))
        nBar=rbFam.getNumberOfBars()
        dt.put_text_in_pnt(str(nBar),pNbarras, hText, "Right")
        pbarLength=pLinea.add(Vector(sum(wColumns[:5])-hText/2.0,-hText/2.0))
        dt.put_text_in_pnt(barLengthTxt,pbarLength, hText, "Right")
        pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
        peso=nBar*barLength*rbFam.getUnitWeight()
        dt.put_text_in_pnt(formatLength %peso,pPeso, hText, "Right")
        pesoTotal += peso
        pLinea=pLinea.add(Vector(0,-hRows))
    pTotal=pLinea.add(Vector(anchoTotal-hText/2.0,0))
    dt.put_text_in_pnt('TOTAL Kg:   ' + formatLength %pesoTotal,pTotal, hText, "Right")
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
        if rbFam.wire==None:
            rbFam.createRebar()
        totalLength=sum(rbFam.wireLengths)
        if rbFam.wireSect2 != None:
            totalLength=(totalLength+sum(rbFam.wireSect2Lengths))/2.0
        s='currentUnitPriceQ.quantities.append(MeasurementRecord(c= \"'+ str(rbFam.identifier) +'\", uds= ' +str(rbFam.getNumberOfBars()) + ', l= ' + str(totalLength) + ', an= ' + str(rbFam.getUnitWeight())  + ')) \n'
        print s
        f.write(s)
    f.close()
        



def drawRCSection(lstOfLstPtsConcrSect,lstShapeRebarFam,lstSectRebarFam,vTranslation=Vector(0,0,0)):
    '''Draw a reinforced concrete section in the FreeCAD active document

    :param lstPtsConcrSect: list of ordered lists of points to draw the 
           concrete section. Each list of points originates an open wire.
    :param lstShapeRebarFam: list of rebar families that are going to be 
           drawn with their true shape.
    :param lstSectRebarFam: list of rebar families that are going to be 
           drawn as sectioned bars (circles).
    :param vTranslation: Vector to apply a traslation to the RC section drawing.
           It facilitates the adding of several RC-sections to the same sheet of
           FreeCAD.
    '''
    #draw the concrete section
    for lp in lstOfLstPtsConcrSect:
        l=Part.makePolygon(lp)
        l.translate(vTranslation)
        Part.show(l)
    #draw the rebars in their true shape
    for rbFam in lstShapeRebarFam:
        rbFam.drawRebar(vTranslation)
    #draw the sectioned rebars
    for rbFam in lstSectRebarFam:
        rbFam.drawSectBars(vTranslation)
    return
    

# Armadura 3D
def arma8ptos(fi,recubrN,sepFi,radDobl,pto1,pto2,pto3,pto4,pto5,pto6,pto7,pto8,gap1,gap2):
    recubrG=recubrN+float(fi)/1000/2.0
    v=pto6.sub(pto2)
    recArmPlano=(v.Length-2*recubrG-int((v.Length-2.0*recubrG)/sepFi)*sepFi)/2.0
    v1=GeomUtils.vectorUnitario(pto2,pto1)
    v2=GeomUtils.vectorUnitario(pto2,pto3)
    v3=GeomUtils.vectorUnitario(pto3,pto4)
    v4=GeomUtils.vectorUnitario(pto2,pto6)
    v5=GeomUtils.vectorUnitario(pto3,pto7)
    v6=GeomUtils.vectorUnitario(pto6,pto5)
    v7=GeomUtils.vectorUnitario(pto6,pto7)
    v8=GeomUtils.vectorUnitario(pto7,pto8)
    pto1a=pto1.add(GeomUtils.escalarPorVector(recArmPlano,v4)).add(GeomUtils.escalarPorVector(recubrG,v2)).add(GeomUtils.escalarPorVector(gap1,v1))
    pto2a=pto2.add(GeomUtils.escalarPorVector(recArmPlano,v4)).add(GeomUtils.escalarPorVector(recubrG,v2)).add(GeomUtils.escalarPorVector(recubrG,v1))
    pto3a=pto3.add(GeomUtils.escalarPorVector(recArmPlano,v5)).sub(GeomUtils.escalarPorVector(recubrG,v2)).add(GeomUtils.escalarPorVector(recubrG,v3))
    pto4a=pto4.add(GeomUtils.escalarPorVector(recArmPlano,v5)).sub(GeomUtils.escalarPorVector(recubrG,v2)).add(GeomUtils.escalarPorVector(gap2,v3))
    pto5a=pto5.sub(GeomUtils.escalarPorVector(recArmPlano,v4)).add(GeomUtils.escalarPorVector(recubrG,v7)).add(GeomUtils.escalarPorVector(gap1,v6))
    pto6a=pto6.sub(GeomUtils.escalarPorVector(recArmPlano,v4)).add(GeomUtils.escalarPorVector(recubrG,v7)).add(GeomUtils.escalarPorVector(recubrG,v6))
    pto7a=pto7.sub(GeomUtils.escalarPorVector(recArmPlano,v5)).sub(GeomUtils.escalarPorVector(recubrG,v7)).add(GeomUtils.escalarPorVector(recubrG,v8))
    pto8a=pto8.sub(GeomUtils.escalarPorVector(recArmPlano,v5)).sub(GeomUtils.escalarPorVector(recubrG,v7)).add(GeomUtils.escalarPorVector(gap2,v8))
    cara1=Part.Face(Part.makePolygon([pto1a,pto2a,pto6a,pto5a,pto1a]))
    cara2=Part.Face(Part.makePolygon([pto2a,pto6a,pto7a,pto3a,pto2a]))
    cara3=Part.Face(Part.makePolygon([pto3a,pto4a,pto8a,pto7a,pto3a]))
    arma=cara1.fuse(cara2.fuse(cara3))
    armadura=arma.makeFillet(radDobl,arma.Edges)
    return armadura

    
    
