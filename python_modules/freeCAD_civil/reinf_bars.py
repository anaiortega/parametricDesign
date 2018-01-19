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
import math

class rebarFamily(object):
    '''Family of reinforcement bars

    :ivar identificador: identificador de la armadura
    :ivar diámetro: diámetro de la armadura (en unidades coherentes)
    :ivar separacion: distancia entre ejes de barras (en unidades 
    coherentes). Si damos el nº de barras en lugar de la separación 
    entonces separacion=0
    :ivar nBarras: nº de barras a disponer. Sólo lo considera cuando 
    separacion=0
    :ivar lstPtosConcrSect: lista de ptos (vectores) a partir de los 
    cuales se genera la barra
    :ivar listaRec: lista de recubrimientos respecto a los segmentos 
    definidos por los puntos anteriores (en unidades coherentes)
    :ivar lado: lado hacia el cual se dará el recubrimiento (i para 
    lado izquierdo, d para lado derecho)
    :ivar radioDob: radio para doblado de la armadura (en unidades 
    coherentes)
    :ivar gapIni: incremento (decremento si gapIni<0) de longitud de la 
    armadura en su extremo inicial
    :ivar gapFin: incremento (decremento si gapFin<0) de longitud de la 
    armadura en su extremo final
    :ivar vectorLRef: primer tramo de la linea de referencia para 
    rotulación de la armadura
    :ivar hTexto: altura del texto
    :ivar ptosExtension: ptos. inicial y final entre los que se desarrolla la familia

    :ivar reclateral: recubrimiento mínimo en los extremos para colocar la familia
    :ivar ladoDibSec: lado hacia el cual se dará el recubrimiento (i para lado izquierdo, d para lado derecho)
    :ivar vectorLRef: primer tramo de la linea de referencia para rotulación de la armadura

    :ivar wire: FreeCAD object of type wire that represents the rebar shape
                ( or the rebar shape in section 1 when it is variable).
    :ivar wireSect: FreeCAD object of type wire that represents the rebar at
                    section 2 when the shape of rebars in the family varies 
                    uniformily from section 1 to section 2.

    '''
    def __init__(self,identificador,diametro,separacion,lstPtosConcrSect,listaRec,lado,radioDob,gapIni,gapFin,vectorLRef,hTexto,ptosExtension,recSec,recLateral,ladoDibSec,vectorLRefSec,lstPtosConcrSect2=[]):
        self.identificador=identificador 
        self.diametro=diametro
        self.separacion=separacion 
        self.lstPtosConcrSect=lstPtosConcrSect 
        self.listaRec= listaRec
        self.lado=lado 
        self.radioDob= radioDob
        self.gapIni= gapIni
        self.gapFin= gapFin
        self.vectorLRef= vectorLRef
        self.hTexto= hTexto
        self.ptosExtension= ptosExtension
        self.recSec= recSec
        self.recLateral=recLateral 
        self.ladoDibSec= ladoDibSec
        self.vectorLRefSec=vectorLRefSec
        self.lstPtosConcrSect2=lstPtosConcrSect2    #sección 2 para definir armaduras variables
        self.listaPtosArm=[[],[]]
        self.nBarras=0
        self.wire=None 
        self.wireSect2=None 
      
    
    def drawSectBars(self,vTranslation=Vector(0,0,0)):
        '''Draw the rebar family as sectioned bars represented by circles in 
        the RC section.

        :param vTranslation: Vector (Vector(x,y,z)) to apply a traslation to 
        the drawing (defaults to Vector(0,0,0))
        '''
        vaux=self.ptosExtension[1].sub(self.ptosExtension[0])
        Laux=vaux.Length
        nesp=int((Laux-2.0*self.recLateral-self.diametro)/self.separacion)
        vaux.normalize()
        if self.ladoDibSec == 'i':
            vauxn=Vector(-vaux.y,vaux.x)
        else:
            vauxn=Vector(vaux.y,-vaux.x)
        vauxn.normalize()
        incrini=vaux.multiply((Laux-nesp*self.separacion)/2.0).add(vauxn.multiply(self.recSec+self.diametro/2.0))
        cent=FreeCAD.Placement()
        cent.move(self.ptosExtension[0].add(incrini).add(vTranslation))
        ptoIniEtiq=self.ptosExtension[0].add(incrini).add(vTranslation)
        rebarText(ptoIniEtiq,self.vectorLRefSec,self.identificador,self.diametro,self.separacion,0,self.hTexto)
        vaux.normalize()
        incr=vaux.multiply(self.separacion)
        for i in range(0,nesp+1):
            c=Draft.makeCircle(self.diametro/2.0,cent,False)
            FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,0.00,0.00)
            cent.move(incr)
        p1=ptoIniEtiq.add(self.vectorLRefSec)
        vaux.normalize()
        p2=p1.add(vaux.multiply(self.separacion*nesp)).sub(self.vectorLRefSec)
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
        vArr=rebarEdges[0].tangentAt(0).multiply(self.hTexto/2.0) #arrow vector
        Draft.rotate(Draft.makeLine(pExtr1,pExtr1.add(vArr)),15,pExtr1)
        #arrow in extremity 2
        pExtr2=rebarEdges[-1].Vertexes[1].Point #vertex at extremity 2
        vArr=rebarEdges[-1].tangentAt(1).multiply(self.hTexto/2.0) #arrow vector
        Draft.rotate(Draft.makeLine(pExtr2,pExtr2.add(vArr)),180-15,pExtr2)
        # Texts
        ptoIniEtiq=rebarEdges[int(len(rebarEdges)/2.)].CenterOfMass
        rebarText(ptoIniEtiq,self.vectorLRef,self.identificador,self.diametro,self.separacion,self.nBarras,self.hTexto)
        return

    def createRebar(self):
        '''Create the wire that represents the true shape of a bar in the 
        family. In case of variable shape, a second wire is created according 
        to the shape defined for section2.
        '''
        self.wire=self.getRebar(self.lstPtosConcrSect)
        if len(self.lstPtosConcrSect2) > 0:
            self.wireSect2=self.getRebar(self.lstPtosConcrSect2)

    def getRebar(self,lstPtsConcr):
        '''Return the wire that represents the true shape of the bar defined
        by the points of the concrete section listed in lstPtsConcr.

        :param lstPtsConcr: ordered list of points in the concrete section 
        to which the rebar is 'attached'. 
        '''
        npuntos=len(lstPtsConcr)
        lstPtosAux=[pt for pt in lstPtsConcr]
        vaux=lstPtosAux[0].sub(lstPtosAux[1])
        vaux.normalize().multiply(self.gapIni)
        lstPtosAux[0]=lstPtosAux[0].add(vaux)
        vaux=lstPtosAux[-1].sub(lstPtosAux[-2])
        vaux.normalize().multiply(self.gapFin)
        lstPtosAux[-1]=lstPtosAux[-1].add(vaux)
        listaaux=[]
        for i in range (0,npuntos-1):
            vaux=lstPtosAux[i+1].sub(lstPtosAux[i])
            if self.lado == 'i':
                vauxn=Vector(-vaux.y,vaux.x)
            else:
                vauxn=Vector(vaux.y,-vaux.x)
            vauxn.normalize()
            vauxn.multiply(self.listaRec[i]+self.diametro/2.0)
            listaaux.append(lstPtosAux[i].add(vauxn))
            listaaux.append(lstPtosAux[i+1].add(vauxn))

        lstPtsArm=[listaaux[0]]
        for i in range (1,npuntos-1):
            pint=int2rectas(listaaux[2*(i-1)],listaaux[2*(i-1)+1],listaaux[2*i],listaaux[2*i+1])
            lstPtsArm.append(pint)

        lstPtsArm.append(listaaux[2*(npuntos-1)-1])
        lstLines=[Part.Line(lstPtsArm[i],lstPtsArm[i+1]).toShape() for i in range(len(lstPtsArm)-1)]
        rebarWire=Part.Wire(lstLines)
        return rebarWire
                        
    

def rebarText(ptoInic,vectorLRef,idArm,diamArm,sepArm,nBarr,hTexto):
    '''Rotulacion de un grupo de barras de armado

    :param ptoInic: pto del que arranca la linea de referencia
    :param vectorLRef: primer tramo de la linea de referencia
    :param idArm: identificador de la armadura
    :param diamArm: diámetro de la armadura
    :param sepArm: separacion entre barras
    :param nBarr: nº de barras (sólo se tiene en cuenta cuando sepArm=0)
    :param hTexto: altura del texto
    '''
    p2=ptoInic.add(vectorLRef)
    signo=1.0*vectorLRef.x/abs(vectorLRef.x)
    p3=p2.add(Vector(signo*hTexto,0))
    p4=p3.add(Vector(signo*hTexto,0))
    p5=p3.add(Vector(signo*hTexto/2.0,-hTexto/2.0))
    w=Draft.makeWire([ptoInic,p2,p3])
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    if len(idArm)==1:
        pl=FreeCAD.Placement()
        pl.move(p4)
        c=Draft.makeCircle(hTexto*(len(idArm)+1)/2.0,pl,False)
        FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,1.00,0.00)
    else:
        pp1=p4.add(Vector(0,hTexto))
        pp2=p4.add(Vector(signo*hTexto*(len(idArm)-1),hTexto))
        pp3=p4.add(Vector(0,-hTexto))
        pp4=p4.add(Vector(signo*hTexto*(len(idArm)-1),-hTexto))
        pp5=p4.add(Vector(signo*hTexto*len(idArm),0))
        c1=Part.Arc(pp1,p3,pp3)
        c2=Part.Arc(pp2,pp5,pp4)
        l1=Part.Line(pp1,pp2)
        l2=Part.Line(pp3,pp4)
        etiq=Part.Wire([l1.toShape(),c1.toShape(),l2.toShape(),c2.toShape()])
        Part.show(etiq)
    if vectorLRef.x > 0:
        if sepArm == 0:
            tx=Draft.makeText(idArm + '  ' + str(int(nBarr)) + '%%C' + str(int(1000*diamArm)) , p5)
        else:
            tx=Draft.makeText(idArm + '  %%C' + str(int(1000*diamArm)) + 'c/' + str(sepArm) , p5)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    else:
        if sepArm == 0:
            tx=Draft.makeText(str(int(nBarr)) + '%%C' + str(int(1000*diamArm)) + '   ' + idArm , p5)
        else:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) + 'c/' + str(sepArm) +'   ' + idArm , p5)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    return
    
def drawSketchRebarShape(rebFam,ptCOG,wColumn,hRow,hText,decLengths=2):
    '''Draw the shape skectch of the rebFam reinforcment bar in the bar 
    schedule. Return the total length of the rebar.

    :param rebFam: family of rebars to be represented.
    :param ptCOG:  point where to place the center of gravity of the sketch.
    :param wColumn: width of the column 'Shape' in the bar schedule.
    :param hRow: height of the row in the bar schedule.
    :param hText: height of the text to label the sketch.
    :param decLengths: decimal positions to calculate and express lengths.
    '''
    trueBar=rebFam.wire
    sketch=trueBar.copy()
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
    lengths=[round(edg.Length,decLengths) for edg in trueBar.Edges]
    lengthsText=[str(i) for i in lengths]
    totalLength=sum(lengths)
    totalLengthTxt=str(totalLength)
    if rebFam.wireSect2 != None:
        trueBarSect2=rebFam.wireSect2
        lengthsSect2=[round(edg.Length,decLengths) for edg in trueBarSect2.Edges]
        lengthsText=[(lengthsText[i]+'..'+str(lengthsSect2[i])) if lengths[i]!=lengthsSect2[i] else lengthsText[i] for i in range(len(lengths))]
        totalLength=(totalLength+sum(lengthsSect2))/2.0
        totalLengthTxt+='...'+str(sum(lengthsSect2))
    sketchEdges=sketch.Edges
    for i in zip(sketchEdges,lengthsText):
        edg=i[0]
        tx=Draft.makeText(i[1],edg.CenterOfMass)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Center"
        FreeCADGui.ActiveDocument.getObject(tx.Name).Rotation = math.degrees(edg.tangentAt(0).getAngle(Vector(1,0,0)))
    return (totalLength,totalLengthTxt)



def barSchedule(lstBarFamilies,wColumns,hRows,hText,hTextSketch,decLengths=2,decSpacing=2):
    ''' Cuadro de despiece de la armadura 

    :param lstBarFamilies: ordered list of rebar families to be included in 
           the schedule
    :param wColumns: lista de anchos de columnas de cuadro de despiece 
    (corresponden a posición, esquema, diam. y separac., No. de barras y 
    longitud de cada barra)
    :param hRows: altura de todas las filas
    :param hText: altura textos
    :param hTextSketch: altura para los textos del esquema
    :param decLengths: decimal positions to calculate and express lengths and
                      their derivated magnitudes, like weight  (defaults to 2).
    :param decSpacing: decimal positions to express the spacing (defaults to 2).

    '''
    #lstBarFamilies=familiasArmad.items() #creamos una lista a partir del diccionario para poder ordenar los valores
    #lstBarFamilies.sort()
    formatLength='%.'+str(decLengths)+'f'
    formatSpacing='%.'+str(decSpacing)+'f'
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
    tx=Draft.makeText('POS.',pPos)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    pEsq=pLinea.add(Vector(wColumns[0]+wColumns[1]/2.0,-hText/2.0))
    tx=Draft.makeText('ESQUEMA',pEsq)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Center"
    pFiSep=pLinea.add(Vector(wColumns[0]+wColumns[1]+hText/2.0,-hText/2.0))
    tx=Draft.makeText('%%C/SEP.',pFiSep.add(Vector(0,hText)))
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    tx=Draft.makeText('(mm)/(m)',pFiSep.add(Vector(0,-hText)))
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    pNbarras=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]-hText/2.0,-hText/2.0))
    tx=Draft.makeText('NUM.',pNbarras)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    pLbarra=pLinea.add(Vector(wColumns[0]+wColumns[1]+wColumns[2]+wColumns[3]+wColumns[4]-hText/2.0,-hText/2.0))
    tx=Draft.makeText('LONG.(m)',pLbarra)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
    tx=Draft.makeText('PESO',pPeso.add(Vector(0,hText)))
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    tx=Draft.makeText('(Kg)',pPeso.add(Vector(0,-hText)))
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    
    pLinea=p1.add(Vector(0,-hRows/2.0))
    # iterElem=familiasArmad.iterkeys()
    pesoTotal=0
    for rbFam in lstBarFamilies:
        if rbFam.wire==None:
            rbFam.createRebar()
        #identf=iterElem.next()
#        identf=lstBarFamilies[i][0]
        pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
        tx=Draft.makeText(rbFam.identificador,pPos)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        pEsq=pLinea.add(Vector(wColumns[0] + wColumns[1]/2.0,0))
#        ptosArm=rbFam.listaPtosArm

        barLength,barLengthTxt=drawSketchRebarShape(rbFam,pEsq,wColumns[1],hRows,hTextSketch,decLengths)
        pFiSep=pLinea.add(Vector(sum(wColumns[:2])+hText/2.0,-hText/2.0))
        diamArm=rbFam.diametro
        sepArm=rbFam.separacion
        if sepArm ==0:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) ,pFiSep)
        else:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) + 'c/' + formatSpacing %sepArm,pFiSep)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        pNbarras=pLinea.add(Vector(sum(wColumns[:4])-hText/2.0,-hText/2.0))
        if sepArm == 0:
            nBar=rbFam.nBarras
        else:
            vaux=rbFam.ptosExtension[1].sub(rbFam.ptosExtension[0])
            Laux=vaux.Length
            nesp=int((Laux-2.0*rbFam.recLateral-diamArm)/sepArm)
            nBar=nesp+1
        tx=Draft.makeText(str(nBar),pNbarras)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pbarLength=pLinea.add(Vector(sum(wColumns[:5])-hText/2.0,-hText/2.0))
        tx=Draft.makeText(barLengthTxt,pbarLength)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pPeso=pLinea.add(Vector(sum(wColumns[:6])-hText/2.0,-hText/2.0))
        peso=nBar*barLength*math.pi*diamArm**2.0/4.*7850
        tx=Draft.makeText(formatLength %peso,pPeso)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pesoTotal += peso
        pLinea=pLinea.add(Vector(0,-hRows))
    pTotal=pLinea.add(Vector(anchoTotal-hText/2.0,0))
    tx=Draft.makeText('TOTAL Kg:   ' + formatLength %pesoTotal,pTotal)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hText
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    return


def int2rectas(P1,P2,P3,P4):
    ''' Devuelve el punto de interseccion de 2 rectas

    :param P1 y P2: ptos. que definen la 1a. recta
    :param P3 y P4: ptos. que definen la 2a. recta
    '''
    if P1.x == P2.x:
        if P3.x == P4.x:
            print 'Rectas paralelas'
            Pinters=()
        else:
            xinters=P1.x
            m2=1.0*(P4.y-P3.y)/(P4.x-P3.x) #pte. de la 2a. recta
            b2=P3.y-m2*P3.x            # ordenada pto. de corte 2a. recta con eje Y
            yinters=m2*xinters+b2
            Pinters=Vector(xinters,yinters)
    elif P3.x == P4.x:
        xinters=P3.x
        m1=1.0*(P2.y-P1.y)/(P2.x-P1.x) #pte. de la 2a. recta
        b1=P1.y-m1*P1.x            # ordenada pto. de corte 2a. recta con eje Y
        yinters=m1*xinters+b1
        Pinters=Vector(xinters,yinters)
    else:
        m1=1.0*(P2.y-P1.y)/(P2.x-P1.x) #pte. de la 1a. recta
        b1=P1.y-m1*P1.x            # ordenada pto. de corte 1a. recta con eje Y
        m2=1.0*(P4.y-P3.y)/(P4.x-P3.x) #pte. de la 2a. recta
        b2=P3.y-m2*P3.x            # ordenada pto. de corte 2a. recta con eje Y
        if m1 == m2:
            print 'Rectas paralelas'
            Pinters=()
        else:
            xinters=1.0*(b2-b1)/(m1-m2)
            yinters=m1*xinters+b1
            Pinters=Vector(xinters,yinters)
    return Pinters


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

    
    
