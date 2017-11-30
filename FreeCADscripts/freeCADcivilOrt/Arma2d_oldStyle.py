# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
from FreeCAD import Base
import FreeCADGui
import math


def armaSec(identificador,diametro,separacion,recubrimiento,reclateral,ptosExtension,ladoDibSec,vectorLRefSec,hTexto):
    # Definici�n de armadura bolinches
    # identificador: identificador de la armadura
    # diametro: di�metro de la armadura (en unidades coherentes)
    # separacion: distancia entre ejes de barras (en unidades coherentes)
    # recubrimiento: recubrimiento (en unidades coherentes)
    # reclateral: recubrimiento m�nimo en los extremos para colocar la familia
    # ptosExtension: ptos. inicial y final entre los que se desarrolla la familia
    # ladoDibSec: lado hacia el cual se dar� el recubrimiento (i para lado izquierdo, d para lado derecho)
    # vectorLRef: primer tramo de la linea de referencia para rotulaci�n de la armadura
    # hTexto: altura del texto

    vaux=ptosExtension[1].sub(ptosExtension[0])
    Laux=vaux.Length
    nesp=int((Laux-2.0*reclateral-diametro)/separacion)
    vaux.normalize()
    if ladoDibSec == 'i':
        vauxn=Base.Vector(-vaux.y,vaux.x)
    else:
        vauxn=Base.Vector(vaux.y,-vaux.x)
    vauxn.normalize()
    incrini=vaux.multiply((Laux-nesp*separacion)/2.0).add(vauxn.multiply(recubrimiento+diametro/2.0))
    cent=FreeCAD.Placement()
    cent.move(ptosExtension[0].add(incrini))
    ptoIniEtiq=ptosExtension[0].add(incrini)
    textoArmadura(ptoIniEtiq,vectorLRefSec,identificador,diametro,separacion,0,hTexto)
    vaux.normalize()
    incr=vaux.multiply(separacion)
    for i in range(0,nesp+1):
        c=Draft.makeCircle(diametro/2.0,cent,False)
        FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,0.00,0.00)
        cent.move(incr)
    p1=ptoIniEtiq.add(vectorLRefSec)
    vaux.normalize()
    p2=p1.add(vaux.multiply(separacion*nesp)).sub(vectorLRefSec)
    w=Draft.makeWire([p1,p2])
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    return

def armadura(identificador,diametro,separacion,nBarras,listaPtos,listaRec,lado,radioDob,gapIni,gapFin,vectorLRef,hTexto):
    # identificador: identificador de la armadura
    # di�metro: di�metro de la armadura (en unidades coherentes)
    # separacion: distancia entre ejes de barras (en unidades coherentes). Si damos el n� de barras en
    # lugar de la separaci�n entonces separacion=0
    # nBarras: n� de barras a disponer. S�lo lo considera cuando separacion=0
    # listaPtos: lista de ptos (vectores) a partir de los cuales se genera la barra
    # listaRec: lista de recubrimientos respecto a los segmentos definidos por los puntos anteriores (en unidades coherentes)
    # lado: lado hacia el cual se dar� el recubrimiento (i para lado izquierdo, d para lado derecho)
    # radioDob: radio para doblado de la armadura (en unidades coherentes)
    # gapIni: incremento (decremento si gapIni<0) de longitud de la armadura en su extremo inicial
    # gapFin: incremento (decremento si gapFin<0) de longitud de la armadura en su extremo final
    #vectorLRef: primer tramo de la linea de referencia para rotulaci�n de la armadura
    #hTexto: altura del texto

    npuntos=len(listaPtos)
    lstPtosAux=[]
    for i in range (0,npuntos):
        lstPtosAux.append(listaPtos[i])
    
    vaux=lstPtosAux[0].sub(lstPtosAux[1])
    vaux.normalize().multiply(gapIni)
    lstPtosAux[0]=lstPtosAux[0].add(vaux)
    vaux=lstPtosAux[npuntos-1].sub(lstPtosAux[npuntos-2])
    vaux.normalize().multiply(gapFin)
    lstPtosAux[npuntos-1]=lstPtosAux[npuntos-1].add(vaux)
    listaaux=[]
    for i in range (0,npuntos-1):
        vaux=lstPtosAux[i+1].sub(lstPtosAux[i])
        if lado == 'i':
            vauxn=Base.Vector(-vaux.y,vaux.x)
        else:
            vauxn=Base.Vector(vaux.y,-vaux.x)
        vauxn.normalize()
        vauxn.multiply(listaRec[i]+diametro/2.0)
        listaaux.append(lstPtosAux[i].add(vauxn))
        listaaux.append(lstPtosAux[i+1].add(vauxn))
                
    listaPtosArm=[listaaux[0]]
    for i in range (1,npuntos-1):
        pint=int2rectas(listaaux[2*(i-1)],listaaux[2*(i-1)+1],listaaux[2*i],listaaux[2*i+1])
        listaPtosArm.append(pint)
    
    listaPtosArm.append(listaaux[2*(npuntos-1)-1])
    # arma=Part.makePolygon(listaPtosArm)
    # armad=arma.makeFillet(radioDob,arma.Edges)
    # Part.show(armad)
    
    w=Draft.makeWire(listaPtosArm)
    #flechas en extremos de barra
    vaux=listaPtosArm[1].sub(listaPtosArm[0]).normalize().multiply(hTexto/2.0)
    Draft.rotate(Draft.makeLine(listaPtosArm[0],listaPtosArm[0].add(vaux)),15,listaPtosArm[0])
    vaux=listaPtosArm[npuntos-2].sub(listaPtosArm[npuntos-1]).normalize().multiply(hTexto/2.0)
    Draft.rotate(Draft.makeLine(listaPtosArm[npuntos-1],listaPtosArm[npuntos-1].add(vaux)),15,listaPtosArm[npuntos-1])

    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (0.00,0.00,1.00)
    # rotulaci�n
    ptoIniEtiq=listaPtosArm[int(npuntos/2.0)-1].add((listaPtosArm[int(npuntos/2.0)].sub(listaPtosArm[int(npuntos/2.0)-1])).multiply(0.5))
    textoArmadura(ptoIniEtiq,vectorLRef,identificador,diametro,separacion,nBarras,hTexto)
    return listaPtosArm
                        
                        
                        
def int2rectas(P1,P2,P3,P4):
    # Devuelve el punto de interseccion de 2 rectas
    # P1 y P2: ptos. que definen la 1a. recta
    # P3 y P4: ptos. que definen la 2a. recta
    if P1.x == P2.x:
        if P3.x == P4.x:
            print 'Rectas paralelas'
            Pinters=()
        else:
            xinters=P1.x
            m2=1.0*(P4.y-P3.y)/(P4.x-P3.x) #pte. de la 2a. recta
            b2=P3.y-m2*P3.x            # ordenada pto. de corte 2a. recta con eje Y
            yinters=m2*xinters+b2
            Pinters=Base.Vector(xinters,yinters)
    elif P3.x == P4.x:
        xinters=P3.x
        m1=1.0*(P2.y-P1.y)/(P2.x-P1.x) #pte. de la 2a. recta
        b1=P1.y-m1*P1.x            # ordenada pto. de corte 2a. recta con eje Y
        yinters=m1*xinters+b1
        Pinters=Base.Vector(xinters,yinters)
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
            Pinters=Base.Vector(xinters,yinters)
    return Pinters


def textoArmadura(ptoInic,vectorLRef,idArm,diamArm,sepArm,nBarr,hTexto):
    #rotulacion de un grupo de barras de armado
    #ptoInic: pto del que arranca la linea de referencia
    #vectorLRef: primer tramo de la linea de referencia
    #idArm: identificador de la armadura
    #diamArm: di�metro de la armadura
    #sepArm: separacion entre barras
    #nBarr: n� de barras (s�lo se tiene en cuenta cuando sepArm=0)
    #hTexto: altura del texto
    p2=ptoInic.add(vectorLRef)
    signo=1.0*vectorLRef.x/abs(vectorLRef.x)
    p3=p2.add(Base.Vector(signo*hTexto,0))
    p4=p3.add(Base.Vector(signo*hTexto,0))
    p5=p3.add(Base.Vector(signo*hTexto/2.0,-hTexto/2.0))
    w=Draft.makeWire([ptoInic,p2,p3])
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    if len(idArm)==1:
        pl=FreeCAD.Placement()
        pl.move(p4)
        c=Draft.makeCircle(hTexto*(len(idArm)+1)/2.0,pl,False)
        FreeCADGui.ActiveDocument.getObject(c.Name).LineColor = (1.00,1.00,0.00)
    else:
        pp1=p4.add(Base.Vector(0,hTexto))
        pp2=p4.add(Base.Vector(signo*hTexto*(len(idArm)-1),hTexto))
        pp3=p4.add(Base.Vector(0,-hTexto))
        pp4=p4.add(Base.Vector(signo*hTexto*(len(idArm)-1),-hTexto))
        pp5=p4.add(Base.Vector(signo*hTexto*len(idArm),0))
        c1=Part.Arc(pp1,p3,pp3)
        c2=Part.Arc(pp2,pp5,pp4)
        l1=Part.Line(pp1,pp2)
        l2=Part.Line(pp3,pp4)
        etiq=Part.Wire([l1.toShape(),c1.toShape(),l2.toShape(),c2.toShape()])
        Part.show(etiq)
    format="%.2f"
    if vectorLRef.x > 0:
        if sepArm == 0:
            tx=Draft.makeText(idArm + '  ' + str(int(nBarr)) + '%%C' + str(int(1000*diamArm)) , p5)
        else:
            tx=Draft.makeText(idArm + '  %%C' + str(int(1000*diamArm)) + 'c/' + str(format %sepArm) , p5)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    else:
        if sepArm == 0:
            tx=Draft.makeText(str(int(nBarr)) + '%%C' + str(int(1000*diamArm)) + '   ' + idArm , p5)
        else:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) + 'c/' + str(format %sepArm) +'   ' + idArm , p5)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    return
    
            
def monoArmadura(ptoCent,listaPtosArm,htexto,listaLong=[8]*10):
    # Dibuja el mono de la armadura para el despiece
    # ptoCent: punto donde colocar el punto central del mono
    # listaPtosArm: lista de ptos extremos de los segmentos que definen la armadura
    # listaLong: lista con las longitudes de los segmentos del mono (normalmente se tomar� el valor por defecto)
    npuntos=len(listaPtosArm)
    lTotal=0
    lSegm=[]
    ptosMono=[Base.Vector(0,0)]
    xptosMono=[0]
    yptosMono=[0]
    posTextosMono=[]
    for i in range (0,npuntos-1):
        vaux=listaPtosArm[i+1].sub(listaPtosArm[i])
        lSegm.append(vaux.Length)
        lTotal=lTotal+lSegm[i]
        paux=ptosMono[i].add(vaux.normalize().multiply(listaLong[i]))
        ptosMono.append(paux)
        xptosMono.append(paux.x)
        yptosMono.append(paux.y)
        paux2=ptosMono[i].add(vaux.normalize().multiply(listaLong[i]/2.0))
        posTextosMono.append(paux2)
    xmin=min(xptosMono)
    xmax=max(xptosMono)
    ymin=min(yptosMono)
    ymax=max(yptosMono)
    vtrasl=ptoCent.sub(Base.Vector((xmin+xmax)/2.0,(ymin+ymax)/2.0))
    for i in range (0,npuntos):
        ptosMono[i]+=vtrasl
    w=Draft.makeWire(ptosMono)
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (0.00,1.00,0.00)
    format="%.2f"
    for i in range (0,npuntos-1):
        tx=Draft.makeText(str(format %lSegm[i]),posTextosMono[i].add(vtrasl))
        ang=(ptosMono[i+1].sub(ptosMono[i])).getAngle(Base.Vector(1,0))
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = htexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Center"
        FreeCADGui.ActiveDocument.getObject(tx.Name).Rotation = ang*180.0/math.pi
    return 

#CUADRO DE DESPIECE
#Para que se cree es necesario que todas las armaduras previamente se hayan
#dibujado (aunque sea en una secci�n ficticea) con la rutina armadura

def cuadroDespiece(anchoColumnas,hFilas,hTexto,familiasArmad):
    # Cuadro de despiece de la armadura
    # anchoColumnas: ancho de las columnas de cuadro de despiece (corresponden a posici�n, esquema, diam. y separac., No. de barras y longitud de cada barra)
    # hFilas: altura de las filas
    # hTexto: altura textos
    # familiasArmad: datos de las armaduras

    listafamiliasArmad=familiasArmad.items() #creamos una lista a partir del diccionario para poder ordenar los valores
    listafamiliasArmad.sort()
    
    anchoTotal=0
    for i in anchoColumnas:
        anchoTotal +=i

    w=Draft.makeRectangle(anchoTotal,hFilas*(len(listafamiliasArmad)+1))
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)
    p1=Base.Vector(0,0)
    p2=p1.add(Base.Vector(0,hFilas*(len(listafamiliasArmad)+1)))
    for i in range (0,len(anchoColumnas)):
        p1=p1.add(Base.Vector(anchoColumnas[i],0))
        p2=p2.add(Base.Vector(anchoColumnas[i],0))
        w=Draft.makeLine(p1,p2)
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)

    p1=Base.Vector(0,hFilas*(len(listafamiliasArmad)))
    p2=p1.add(Base.Vector(anchoTotal,0))
    w=Draft.makeLine(p1,p2)
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = (1.00,1.00,0.00)

    #T�tulos para la tabla de despiece
    pLinea=p1.add(Base.Vector(0,hFilas/2.0))
    pPos=pLinea.add(Base.Vector(hTexto/2.0,-hTexto/2.0))
    tx=Draft.makeText('POS.',pPos)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    pEsq=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]/2.0,-hTexto/2.0))
    tx=Draft.makeText('ESQUEMA',pEsq)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Center"
    pFiSep=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+hTexto/2.0,-hTexto/2.0))
    tx=Draft.makeText('%%C/SEP.',pFiSep)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    pNbarras=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]-hTexto/2.0,-hTexto/2.0))
    tx=Draft.makeText('NUM.',pNbarras)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    pLbarra=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]+anchoColumnas[4]-hTexto/2.0,-hTexto/2.0))
    tx=Draft.makeText('LONG.(m)',pLbarra)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    pPeso=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]+anchoColumnas[4]+anchoColumnas[5]-hTexto/2.0,-hTexto/2.0))
    tx=Draft.makeText('PESO(Kg)',pPeso)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    
    pLinea=p1.add(Base.Vector(0,-hFilas/2.0))
    # iterElem=familiasArmad.iterkeys()
    format="%.2f"
    pesoTotal=0
    for i in range(0,len(listafamiliasArmad)):
        #identf=iterElem.next()
        identf=listafamiliasArmad[i][0]
        pPos=pLinea.add(Base.Vector(hTexto/2.0,-hTexto/2.0))
        tx=Draft.makeText(familiasArmad[identf]['identificador'],pPos)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        pEsq=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]/2.0,0))
        ptosArm=familiasArmad[identf]['listaPtosArm']
        monoArmadura(pEsq,ptosArm,hTexto,)
        pFiSep=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+hTexto/2.0,-hTexto/2.0))
        diamArm=familiasArmad[identf]['diametro']
        sepArm=familiasArmad[identf]['separacion']
        if sepArm ==0:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) ,pFiSep)
        else:
            tx=Draft.makeText('%%C' + str(int(1000*diamArm)) + 'c/' + str(format %sepArm),pFiSep)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        pNbarras=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]-hTexto/2.0,-hTexto/2.0))
        if sepArm == 0:
            nBar=familiasArmad[identf]['nBarras']
        else:
            vaux=familiasArmad[identf]['ptosExtension'][1].sub(familiasArmad[identf]['ptosExtension'][0])
            Laux=vaux.Length
            nesp=int((Laux-2.0*familiasArmad[identf]['recLateral']-diamArm)/sepArm)
            nBar=nesp+1
        tx=Draft.makeText(str(nBar),pNbarras)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pLbarra=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]+anchoColumnas[4]-hTexto/2.0,-hTexto/2.0))
        Lbarra=0
        for j in range(0,len(ptosArm)-1):
            Lbarra += (ptosArm[j+1].sub(ptosArm[j])).Length
        tx=Draft.makeText(str(format %Lbarra),pLbarra)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pPeso=pLinea.add(Base.Vector(anchoColumnas[0]+anchoColumnas[1]+anchoColumnas[2]+anchoColumnas[3]+anchoColumnas[4]+anchoColumnas[5]-hTexto/2.0,-hTexto/2.0))
        peso=nBar*Lbarra*math.pi*diamArm**2.0/4*7850
        tx=Draft.makeText(str(format %peso),pPeso)
        FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
        FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
        pesoTotal += peso
        pLinea=pLinea.add(Base.Vector(0,-hFilas))
    pTotal=pLinea.add(Base.Vector(anchoTotal-hTexto/2.0,0))
    tx=Draft.makeText('TOTAL Kg:   ' + str(format %pesoTotal),pTotal)
    FreeCADGui.ActiveDocument.getObject(tx.Name).FontSize = hTexto
    FreeCADGui.ActiveDocument.getObject(tx.Name).Justification = "Right"
    return