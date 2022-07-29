# -*- coding: utf-8 -*-

import Part, FreeCAD, math
import Draft
import freeCADcivilOrt
from freeCADcivilOrt import PerfilesMetalicos
from freeCADcivilOrt import Geometria2D
from freeCADcivilOrt import Geometria3D
from FreeCAD import Base
from Draft import *

def barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec=0):
    # dibuja el perfil metálico perfil.tamPerfil entre los puntos 3D ptoIni y ptoFin
    # incrIni: incremento de longitud de la barra por el extremo inicial
    # incrFin: incremento de longitud de la barra por el extremo final
    # giroSec: giro de la sección para orientar la barra
    tipo='PerfilesMetalicos.'+perfil
    if perfil in ['IPN','IPE','HEB','HEA','HEM','W']:
        secc=secDobleT(tipo,tamPerfil)
    elif perfil in ['UPN']:
        secc=secU(tipo,tamPerfil)
    elif perfil in ['L','LD']:
        secc=secAngular(tipo,tamPerfil)
    elif perfil in ['tiranteFi','tiranteCuad','tiranteRect']:
        secc=secTirante(tipo,tamPerfil)
    elif perfil in ['huecoCirc','huecoCuad','huecoRect']:
        secc=secHueco(tipo,tamPerfil)
    elif perfil in ['LF','UF','CF','OF','ZF']:
        secc=secConformado(tipo,tamPerfil)
    
    vunit=(ptoFin.sub(ptoIni)).normalize()
    if incrIni != 0:
        p1=ptoIni.sub(vunit.multiply(incrIni))
    else:
        p1=ptoIni
    vunit=(ptoFin.sub(ptoIni)).normalize()
    if incrFin != 0:
        p2=ptoFin.add(vunit.multiply(incrFin))
    else:
        p2=ptoFin
    eje=p2.sub(p1)
    if (p1.x == p2.x) and (p1.y == p2.y) :
        secc.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    else:
        eje.projectToPlane(Base.Vector(0,0,0),Base.Vector(0,0,1))
        angX=eje.getAngle(Base.Vector(1,0,0))*180.0/math.pi
        secc.rotate(Base.Vector(0,0,0),Base.Vector(0,0,1),angX+90) # se coloca el perfil en un plano
        #perpendicular al plano vertical que pasa por la recta definida por los dos puntos
        eje=p2.sub(p1)
        ejeHsecc=eje.cross(Base.Vector(0,0,1))
        ejeVsecc=ejeHsecc.cross(eje)
        otrogiro=ejeVsecc.getAngle(Base.Vector(0,0,1))*180.0/math.pi
        if p1.z < p2.z :
            secc.rotate(Base.Vector(0,0,0),ejeHsecc,otrogiro)
        else:
            secc.rotate(Base.Vector(0,0,0),ejeHsecc,-otrogiro)

    secc.translate(p1)
    barra=secc.extrude(eje)
    if giroSec != 0 :
        barra.rotate(p1,eje,giroSec)
        
    return barra

def soldadura(pieza1,pieza2,eGarganta,longitud,centroArista,vDireccion):
    #Devuelve una cuña de cilindro para representar una soldadura, siendo:
    #pieza1 y pieza2: piezas a soldar (pueden ser iguales, si fuera una sola pieza)
    #eGarganta: espesor de la garganta de soldadura
    #Longitud: longitud de la soldadura
    #Centro arista: punto central de la soldadura en la intersección de las dos piezas a soldar
    #vDireccion: vector en la dirección de la soldadura
    vDireccion.normalize()
    radio=eGarganta*math.sqrt(2)
    ptoInic=centroArista.sub(vDireccion.multiply(longitud/2.0))
    soldad=Part.makeCylinder(radio,longitud,ptoInic,vDireccion)
    soldad=soldad.cut(pieza1)
    soldad=soldad.cut(pieza2)
    return soldad

def soldadura2Ptos(pieza1,pieza2,eGarganta,PtoInic,PtoFin):
    #Devuelve una cuña de cilindro para representar una soldadura, siendo:
    #pieza1 y pieza2: piezas a soldar (pueden ser iguales, si fuera una sola pieza)
    #eGarganta: espesor de la garganta de soldadura
    #PtoInic: Pto. origen de la línea de soldadura
    #PtoFin: Pto. final de la línea de soldadura
    vDireccion=PtoFin.sub(PtoInic)
    radio=eGarganta*math.sqrt(2)
    longitud=vDireccion.Length
    soldad=Part.makeCylinder(radio,longitud,PtoInic,vDireccion)
    soldad=soldad.cut(pieza1)
    soldad=soldad.cut(pieza2)
    return soldad

def chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj):
    # Devuelve un chapa con agujeros en un sistema de coordenadas general, definido por:
    # vOrigenL: vector que define el pto. origen del sistema de coordenadas local
    # vDirXL: vector en la dirección X del SC local
    # vDirYL: vector en la dirección Y del SC local
    # vDirZL: vector en la dirección Z del SC local
    # listaCoordChapaL: ptos. ordenados para definir la base de la chapa (que estará contenida en el plano XY local). Las coordenadas de estos ptos. se dan en el SC local en la forma: [[x1,y1],[x2,y2],[x3,y3],...].
    # listaCoordAgujL: ptos. para definir los centros de los agujeros. Las coordenadas de estos ptos. se dan en el SC local en la forma: [[x1,y1],[x2,y2],[x3,y3],...].
    # espesorChapa: espesor de la chapa (en dirección vDirZL)
    # diamAguj: diámetro de los agujeros
    placa=Geometria3D.prismaSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,espesorChapa)
    vDirXL.normalize() #vector de dirección X local
    vDirYL.normalize() #vector de dirección Y local
    vDirZL.normalize() #vector de dirección Z local
    for i in range(0,len(listaCoordAgujL)):
        vuX=Base.Vector(vDirXL.x,vDirXL.y,vDirXL.z)
        vuY=Base.Vector(vDirYL.x,vDirYL.y,vDirYL.z)
        centro=vOrigenL.add(vuX.multiply(listaCoordAgujL[i][0])).add(vuY.multiply(listaCoordAgujL[i][1]))
        aguj=Part.makeCylinder(diamAguj/2.0,espesorChapa,centro,vDirZL)
        placa=placa.cut(aguj)
    return placa

def chapaRectAgujRig(ancho,alto,espesor,coordAguj,diamAguj,rigX,rigY):
    # Crea una chapa rectangular con agujeros y rigidizadores. El centro de la misma está en el origen de coordenadas y la chapa está contenida en el plano XY
    # ancho: dimensión X de la chapa
    # alto: dimensión Y de la chapa
    # espesor: dimensión Z de la chapa
    # coordAguj: lista con las coordenadas [x,y] del centro de cada uno de los agujeros
    # diamAguj: diámetro de los agujeros
    # rigX: definición de rigidizadores paralelos al plano XZ. Para cada rigidizador: [[coord X mínima,coord X máxima],coordenada Y del plano medio del rigidizador,alto(dir Z),espesor]
    # rigY: definición de rigidizadores paralelos al plano YZ. Para cada rigidizador: [[coord Y mínima,coord Y máxima],coordenada X del plano medio del rigidizador,alto(dir Z),espesor]
    pieza=Part.makeBox(ancho,alto,espesor,Base.Vector(-ancho/2.0,-alto/2.0))
    for i in range(0,len(coordAguj)):
        aguj=Part.makeCylinder(diamAguj/2.0,espesor,Base.Vector(coordAguj[i][0],coordAguj[i][1]))
        pieza=pieza.cut(aguj)
    for i in range(0,len(rigX)):
        xminRig=rigX[i][0][0]
        xmaxRig=rigX[i][0][1]
        coordYRig=rigX[i][1]
        dimZRig=rigX[i][2]
        dimYRig=rigX[i][3]
        rig=Part.makeBox(xmaxRig-xminRig,dimYRig,dimZRig,Base.Vector(xminRig,coordYRig-dimYRig/2.0,espesor))
        pieza=pieza.fuse(rig)
    for i in range(0,len(rigY)):
        yminRig=rigY[i][0][0]
        ymaxRig=rigY[i][0][1]
        coordXRig=rigY[i][1]
        dimZRig=rigY[i][2]
        dimXRig=rigY[i][3]
        rig=Part.makeBox(dimXRig,ymaxRig-yminRig,dimZRig,Base.Vector(coordXRig-dimXRig/2.0,yminRig,espesor))
        pieza=pieza.fuse(rig)
    return pieza

def secDobleT(tipo,tam):
    # Genera la sección de un perfil metálico I o H
    # La nomenclatura empleada para las dimensiones es la del prontuario de
    # estructuras metálicas del CEDEX
    # tipo: IPE, IPN, HEB, HEM, HEA o cualquier otro doble T definido en el fichero PerfilesMetalicos.py
    # tam: tamaño que define el perfil (80, 100, 120 , ...)
    h=eval(tipo)[tam]['h']
    b=eval(tipo)[tam]['b']
    e=eval(tipo)[tam]['e']
    e1=eval(tipo)[tam]['e1']
    r=eval(tipo)[tam]['r']
    p1=Base.Vector(-e/2.0-r,0,e1-h/2.0)
    p2=Base.Vector(-b/2.0,0,e1-h/2.0)
    p3=Base.Vector(-b/2.0,0,-h/2.0)
    p4=Base.Vector(b/2.0,0,-h/2.0)
    p5=Base.Vector(b/2.0,0,e1-h/2.0)
    p6=Base.Vector(e/2.0+r,0,e1-h/2.0)
    l1=Part.makePolygon([p1,p2,p3,p4,p5,p6])
    arc1=Part.makeCircle(r,p6.add(Base.Vector(0,0,r)),Base.Vector(0,-1,0),180,270)
    p7=Base.Vector(e/2.0,0,e1+r-h/2.0)
    p8=p7.add(Base.Vector(0,0,h-2*r-2*e1))
    l2=Part.makeLine(p7,p8)
    arc2=Part.makeCircle(r,p8.add(Base.Vector(r,0,0)),Base.Vector(0,-1,0),90,180)
    p9=p8.add(Base.Vector(r,0,r))
    p10=Base.Vector(b/2.0,0,h/2.0-e1)
    p11=Base.Vector(b/2.0,0,h/2.0)
    p12=Base.Vector(-b/2.0,0,h/2.0)
    p13=Base.Vector(-b/2.0,0,h/2.0-e1)          
    p14=Base.Vector(-e/2.0-r,0,h/2.0-e1)
    l3=Part.makePolygon([p9,p10,p11,p12,p13,p14])
    arc3=Part.makeCircle(r,p14.add(Base.Vector(0,0,-r)),Base.Vector(0,-1,0),0,90)
    p15=p14.add(Base.Vector(r,0,-r))
    p16=Base.Vector(-e/2.0,0,e1+r-h/2.0)
    l4=Part.makeLine(p15,p16)
    arc4=Part.makeCircle(r,p16.add(Base.Vector(-r,0,0)),Base.Vector(0,-1,0),-90,0)
    secPerfil=Part.Face(Part.Wire([l1,arc1,l2,arc2,l3,arc3,l4,arc4]))
    return secPerfil

def secU(tipo,tam):
    # Genera la sección de un perfil metálico U
    # La nomenclatura empleada para las dimensiones es la del prontuario de
    # estructuras metálicas del CEDEX
    # tipo: UPN o cualquier otro U definido en el fichero PerfilesMetalicos.py
    # tam: tamaño que define el perfil (80, 100, 120 , ...)
    h=eval(tipo)[tam]['h']
    b=eval(tipo)[tam]['b']
    e=eval(tipo)[tam]['e']
    e1=eval(tipo)[tam]['e1']
    r1=eval(tipo)[tam]['r1']
    e2=eval(tipo)[tam]['e2']
    h1=eval(tipo)[tam]['h1']
    p1=Base.Vector(b-e2,h/2.0)
    p2=Base.Vector(-e2,h/2.0)
    p3=Base.Vector(-e2,-h/2.0)
    p4=Base.Vector(b-e2,-h/2.0)
    l1=Part.makePolygon([p1,p2,p3,p4])
    p5=Base.Vector(b-e2,-h/2.0+e1)
    p6=p5.add(Base.Vector(-(b-e-e1)/2.0,(h/2.0-h1/2.0-2*e1)/2.0))
    l2=Geometria2D.fillet2D(p4,p5,p5,p6,r1)
    p7=p6.add(Base.Vector(-(b-e-e1)/2.0,(h/2.0-h1/2.0-2*e1)/2.0))
    p8=Base.Vector(-e2+e,-h1/2.0)
    pmed=Base.Vector(-e2+e,0)
    l3=Geometria2D.fillet2D(p6,p7,p8,pmed,-e1)
    p12=Base.Vector(b-e2,h/2.0-e1)
    p11=p12.add(Base.Vector(-(b-e-e1)/2.0,-(h/2.0-h1/2.0-2*e1)/2.0))
    l4=Geometria2D.fillet2D(p1,p12,p12,p11,-r1)
    p10=p11.add(Base.Vector(-(b-e-e1)/2.0,-(h/2.0-h1/2.0-2*e1)/2.0))
    p9=Base.Vector(-e2+e,h1/2.0)
    l5=Geometria2D.fillet2D(p11,p10,p9,pmed,e1)
    secPerfil=Part.Face(Part.Wire([l1,l2,l3,l4,l5]))
    secPerfil.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    return secPerfil

def secAngular(tipo,tam):
    # Genera la sección de un perfil metálico en L
    # La nomenclatura empleada para las dimensiones es la del prontuario de
    # estructuras metálicas del CEDEX
    # tipo: L, LD u otro perfil angular definido en PerfilesMetalicos.py
    # tam: tamaño que define el perfil ('120?2', '100?5?',  ...)
    a=eval(tipo)[tam]['a']
    b=eval(tipo)[tam]['b']
    e=eval(tipo)[tam]['e']
    r=eval(tipo)[tam]['r']
    r1=eval(tipo)[tam]['r1']
    cx=eval(tipo)[tam]['cx']
    cy=eval(tipo)[tam]['cy']
    p1=Base.Vector(-(b-cy),-cx)
    p2=Base.Vector(cy,-cx)
    p3=Base.Vector(cy,a-cx)
    l1=Part.makePolygon([p1,p2,p3])
    p4=p3.add(Base.Vector(-e,0))
    p5=p4.add(Base.Vector(0,-(a-e)/2.0))
    l2=Geometria2D.fillet2D(p3,p4,p4,p5,r1)
    p6=p5.add(Base.Vector(0,-(a-e)/2.0))
    p7=p6.add(Base.Vector(-(b-e)/2.0,0))
    l3=Geometria2D.fillet2D(p5,p6,p6,p7,-r)
    p8=p7.add(Base.Vector(-(b-e)/2.0,0))
    l4=Geometria2D.fillet2D(p7,p8,p8,p1,r1)
    secPerfil=Part.Face(Part.Wire([l1,l2,l3,l4]))
    secPerfil.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    return secPerfil

def secTirante(tipo,tam):
    if 'Fi' in tipo:
        d=eval(tipo)[tam]['d']
        secPerfil=Part.makeCircle(d/2.0,Base.Vector(0,0,0),Base.Vector(0,1,0))
        secPerfil=Part.Face(Part.Wire([secPerfil]))
    elif 'Cuad' in tipo:
        d=eval(tipo)[tam]['d']
        secPerfil=Part.makePlane(d,d,Base.Vector(0,0,0),Base.Vector(0,1,0))
    elif 'Rect' in tipo:
        b=eval(tipo)[tam]['b']
        d=eval(tipo)[tam]['d']
        secPerfil=Part.makePlane(b,d,Base.Vector(0,0,0),Base.Vector(0,1,0))
    return secPerfil

def secHueco(tipo,tam):
    if 'Circ' in tipo:
        d=eval(tipo)[tam]['d']
        e=eval(tipo)[tam]['e']
        circExt=Part.makeCircle(d/2.0,Base.Vector(0,0,0),Base.Vector(0,1,0))
        circExt=Part.Face(Part.Wire([circExt]))
        circInt=Part.makeCircle(d/2.0-e,Base.Vector(0,0,0),Base.Vector(0,1,0))
        circInt=Part.Face(Part.Wire([circInt]))
        secPerfil=circExt.cut(circInt)
    elif ('Cuad' in tipo) or ('Rect' in tipo):
        a=eval(tipo)[tam]['a']
        e=eval(tipo)[tam]['e']
        r=eval(tipo)[tam]['r']
        if 'Cuad' in tipo:
            b=a
        else:
            b=eval(tipo)[tam]['b']
        p1=Base.Vector((b-2*r)/2.0,0,-a/2.0)
        p2=Base.Vector(b/2.0,0,-a/2.0+r)
        p3=Base.Vector(b/2.0,0,a/2.0-r)
        p4=Base.Vector((b-2*r)/2.0,0,a/2.0)
        p5=Base.Vector(-(b-2*r)/2.0,0,a/2.0)
        p6=Base.Vector(-b/2.0,0,a/2.0-r)
        p7=Base.Vector(-b/2.0,0,-a/2.0+r)
        p8=Base.Vector(-(b-2*r)/2.0,0,-a/2.0)
        l1=Part.makeLine(p8,p1)
        arc1=Part.makeCircle(r,p1.add(Base.Vector(0,0,r)),Base.Vector(0,-1,0),270,360)
        l2=Part.makeLine(p2,p3)
        arc2=Part.makeCircle(r,p3.add(Base.Vector(-r,0,0)),Base.Vector(0,-1,0),0,90)
        l3=Part.makeLine(p4,p5)
        arc3=Part.makeCircle(r,p5.add(Base.Vector(0,0,-r)),Base.Vector(0,-1,0),90,180)
        l4=Part.makeLine(p6,p7)
        arc4=Part.makeCircle(r,p8.add(Base.Vector(0,0,r)),Base.Vector(0,-1,0),180,270)
        lExt=Part.Wire([l1,arc1,l2,arc2,l3,arc3,l4,arc4])
        lInt=lExt.makeOffset(-e)
        secPerfil=Part.Face(lExt).cut(Part.Face(lInt))

    return secPerfil

def secConformado(tipo,tam):
    # Genera la sección de un perfil conformado LF, UF, CF, OF, ZF
    # La nomenclatura empleada para las dimensiones es la de la EAE (anejos de la parte 2)
    # tam: tamaño que define el perfil (por ejemplo: '50.25.3')
    e=eval(tipo)[tam]['e']
    r=eval(tipo)[tam]['r']
    rext=r+e
    if ('LF' in tipo) or ('CF' in tipo) or ('OF' in tipo):
        a=eval(tipo)[tam]['a']
        b=eval(tipo)[tam]['b']
    if 'UF' in tipo:
        b=eval(tipo)[tam]['b']
    if ('UF' in tipo) or ('CF' in tipo) or ('OF' in tipo):
        h=eval(tipo)[tam]['h']
        c=eval(tipo)[tam]['c']
    if ('LF' in tipo) or ('ZF' in tipo):
        c1=eval(tipo)[tam]['c1']
        c2=eval(tipo)[tam]['c2']
    if 'ZF' in tipo:
        h=eval(tipo)[tam]['h']
        b1=eval(tipo)[tam]['b1']
        b2=eval(tipo)[tam]['b2']
        a1=eval(tipo)[tam]['a1']
        a2=eval(tipo)[tam]['a2']
    if 'LF' in tipo:
        pieza1=Part.makePlane(e,a-rext,Base.Vector(-c2,-(c1-rext)))
        pieza2=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(c2-rext),-(c1-rext)),180,270)
        pieza3=Part.makePlane(b-rext,e,Base.Vector(-(c2-rext),-c1))
        secPerfil=pieza1.fuse(pieza2.fuse(pieza3))
    elif 'UF' in tipo:
        pieza1=Part.makePlane(b-rext,e,Base.Vector(-(c-rext),h/2.0-e))
        pieza2=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(c-rext),h/2.0-rext),90,180)
        pieza3=Part.makePlane(e,h-2*rext,Base.Vector(-c,-(h/2.0-rext)))
        pieza4=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(c-rext),-(h/2.0-rext)),180,270)
        pieza5=Part.makePlane(b-rext,e,Base.Vector(-(c-rext),-h/2.0))
        secPerfil=pieza1.fuse(pieza2.fuse(pieza3.fuse(pieza4.fuse(pieza5))))
    elif 'CF' in tipo:
        pieza1=Part.makePlane(e,a-rext,Base.Vector(b-c-e,h/2.0-a))
        pieza2=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(b-c-rext,h/2.0-rext),0,90)
        pieza3=Part.makePlane(b-2*rext,e,Base.Vector(-(c-rext),h/2.0-e))
        pieza4=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(c-rext),h/2.0-rext),90,180)
        pieza5=Part.makePlane(e,h-2*rext,Base.Vector(-c,-(h/2.0-rext)))
        pieza6=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(c-rext),-(h/2.0-rext)),180,270)
        pieza7=Part.makePlane(b-2*rext,e,Base.Vector(-(c-rext),-h/2.0))
        pieza8=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(b-c-rext,-(h/2.0-rext)),270,0)
        pieza9=Part.makePlane(e,a-rext,Base.Vector(b-c-e,-(h/2.0-rext)))
        secPerfil=pieza1.fuse(pieza2.fuse(pieza3.fuse(pieza4.fuse(pieza5.fuse(pieza6.fuse(pieza7.fuse(pieza8.fuse(pieza9))))))))
    elif 'OF' in tipo:
        pieza1=Part.makePlane(a-rext,e,Base.Vector(-(a+b/2.0-e),-c))
        pieza2=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-b/2.0-r,-c+rext),270,360)
        pieza3=Part.makePlane(e,h-2*rext,Base.Vector(-b/2.0,-(c-rext)))
        pieza4=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(b/2.0-rext),h-c-rext),90,180)
        pieza5=Part.makePlane(b-2*rext,e,Base.Vector(-(b/2.0-rext),h-c-e))
        pieza6=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(b/2.0-rext,h-c-rext),0,90)
        pieza7=Part.makePlane(e,h-2*rext,Base.Vector(b/2.0-e,-(c-rext)))
        pieza8=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(b/2.0+r,-c+rext),180,270)
        pieza9=Part.makePlane(a-rext,e,Base.Vector(b/2.0+r,-c))
        secPerfil=pieza1.fuse(pieza2.fuse(pieza3.fuse(pieza4.fuse(pieza5.fuse(pieza6.fuse(pieza7.fuse(pieza8.fuse(pieza9))))))))
    elif 'ZF' in tipo:
        pieza1=Part.makePlane(e,a1-rext,Base.Vector(-(b1-c2),c1-a1))
        pieza2=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(-(b1-c2-rext),c1-rext),90,180)
        pieza3=Part.makePlane(b1-2*rext,e,Base.Vector(-(b1-c2-rext),c1-e))
        pieza4=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(c2-rext,c1-rext),0,90)
        pieza5=Part.makePlane(e,h-2*rext,Base.Vector(c2-e,-(h-c1-rext)))
        pieza6=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(c2-e+rext,-(h-c1-rext)),180,270)
        pieza7=Part.makePlane(b2-2*rext,e,Base.Vector(c2-e+rext,-(h-c1)))
        pieza8=Geometria2D.arcoCoronaCircular(r,rext,Base.Vector(c2-e+b2-rext,-(h-c1-rext)),270,360)
        pieza9=Part.makePlane(e,b2-rext,Base.Vector(c2-e+b2-e,-(h-c1-rext)))
        secPerfil=pieza1.fuse(pieza2.fuse(pieza3.fuse(pieza4.fuse(pieza5.fuse(pieza6.fuse(pieza7.fuse(pieza8.fuse(pieza9))))))))

    secPerfil.rotate(Base.Vector(0,0,0),Base.Vector(1,0,0),90)
    return secPerfil


def arriostr1Tubo(PtoTrabajo,PtoOrigenCart,plano,tipoPerfilDiag,idPerfilDiag,VOrigenPerf,eCartela,solapePerfCart,holguraCart,alfa1,alfa2,VPte,HPte,LPerf):
    #dibuja la cartela y la diagonal de un arriostramiento tipo tubular (el eje de la diagonal está contenido en el plano medio de la cartela)
    #valores auxiliares
    signoH=HPte/abs(HPte)
    signoV=VPte/abs(VPte)
    alfarad=math.atan(1.0*abs(HPte)/abs(VPte))     #ángulo que forma la diagonal con la vertical
    alfa1rad=math.radians(alfa1)
    alfa2rad=math.radians(alfa2)
    zPto1=VOrigenPerf+abs(PtoTrabajo.z-PtoOrigenCart.z)
    yPto1=1.0*zPto1*abs(HPte)/abs(VPte)
    if plano == 'YZ':
        Pto1=PtoTrabajo.add(Base.Vector(0,yPto1*signoH,zPto1*signoV))
    else:
        Pto1=PtoTrabajo.add(Base.Vector(yPto1*signoH,0,zPto1*signoV))
    yPto2=solapePerfCart*math.sin(alfarad)
    zPto2=solapePerfCart*math.cos(alfarad)
    if plano == 'YZ':
        Pto2=Pto1.add(Base.Vector(0,yPto2*signoH,zPto2*signoV))
    else:
        Pto2=Pto1.add(Base.Vector(yPto2*signoH,0,zPto2*signoV))
    if 'Circ' in tipoPerfilDiag:
        bPerfil=PerfilesMetalicos.huecoCirc[idPerfilDiag]['d']
    elif ('Cuad' in tipoPerfilDiag):
        bPerfil=PerfilesMetalicos.huecoCuad[idPerfilDiag]['a']
    elif ('Rect' in tipoPerfilDiag):
        bPerfil=PerfilesMetalicos.huecoRect[idPerfilDiag]['a']
    z3=(bPerfil/2.0+holguraCart)*math.sin(alfarad)
    y3=(bPerfil/2.0+holguraCart)*math.cos(alfarad)
    z4=VOrigenPerf+zPto2+z3
    z5=z4-2*z3
    y4=z5*math.tan(alfarad-alfa2rad)
    if plano == 'YZ':
        y5=yPto1+yPto2+y3-abs(PtoTrabajo.y-PtoOrigenCart.y)
    else:
        y5=yPto1+yPto2+y3-abs(PtoTrabajo.x-PtoOrigenCart.x)
    y6=y5-y4
    y7=y5-2*y3
    z6=y7*math.tan(math.pi/2.0-alfarad-alfa1rad)
    #Diagonal
    ptoIni=Pto1
    ptoFin=Pto2
    perfil=tipoPerfilDiag
    tamPerfil=idPerfilDiag
    incrIni=0
    incrFin=LPerf
    giroSec=0
    arriostr=barra2Ptos(ptoIni,ptoFin,perfil,tamPerfil,incrIni,incrFin,giroSec)
    #Cartela
    if plano == 'YZ':
        vOrigenL=PtoOrigenCart.add(Base.Vector(-eCartela/2.0,0,0))
        vDirXL=Base.Vector(0,0,1).multiply(signoV)
        vDirYL=Base.Vector(0,1,0).multiply(signoH)
        vDirZL=Base.Vector(1,0,0)
    else:
        vOrigenL=PtoOrigenCart.add(Base.Vector(0,-eCartela/2.0,0))
        vDirXL=Base.Vector(0,0,1).multiply(signoV)
        vDirYL=Base.Vector(1,0,0).multiply(signoH)
        vDirZL=Base.Vector(0,1,0)
    listaCoordChapaL=[[0,0],[0,y6],[z5,y5],[z4,y7],[z4-z6,0]]
    listaCoordAgujL=[]
    espesorChapa=eCartela
    diamAguj=0
    cartela=chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
    arriostr.add(cartela)
    return arriostr

def VatSoldAlmPilarCart(vectorDir,anchoPerfilPilar,eAlmaPerfilPilar,holgAlaPilarVAtado,LVAtado,tipoPerfilVAtado,idPerfilVAtado,eAlmaPerfilVAtado,solapeRigAlmaV,hRig,espesorRig,hAcuerdRig,signoRigPosNeg):
    #Viga de atado horizontal soldada al alma del pilar mediante un rigidizador soldado a las almas del 
    #pilar y de la viga
    #vectorDir= vector de dirección de la viga. La viga ha de estar en un plano horizontal, por tanto
    #la coordenada Z de vectorDir debe ser = 0
    #anchoPerfilPilar= ancho del ala del pilar
    #eAlmaPerfilPilar= espesor del alma del pilar
    #holgAlaPilarVAtado= holgura entre el ala del pilar y el extremo de la viga de atado
    #LVAtado= longitud de la viga de atado a representar
    #eAlmaPerfilVAtado= espesor del alma de la viga de atado
    #hRig=altura del rigidizador
    #espesorRig= espesor del rigidizador
    #solapeRigAlmaV= solape entre el rigidizador y el alma de la viga
    #hAcuerdRig= altura del acuerdo en las esquinas del rigidizador
    #signoRigPosNeg= signo del rigidizador ('Pos' o 'Neg') para que se dibuje a uno u otro lado del alma
    vectorDir.normalize().multiply(anchoPerfilPilar/2.0+holgAlaPilarVAtado)
    ptoIni=Base.Vector(0,0,0)
    ptoIni.x=vectorDir.x
    ptoIni.y=vectorDir.y
    ptoIni.z=vectorDir.z
    vectorDir.normalize().multiply(LVAtado)
    ptoFin=ptoIni.add(vectorDir)
    vatado=barra2Ptos(ptoIni,ptoFin,tipoPerfilVAtado,idPerfilVAtado,0,0,0)
    vectorDir.normalize()
    if signoRigPosNeg == 'Pos':
        vectorPerp=Base.Vector(-vectorDir.y,vectorDir.x,0)
    else:
        vectorPerp=Base.Vector(vectorDir.y,-vectorDir.x,0)
    PtoOr=(vectorDir.multiply(eAlmaPerfilPilar/2.0)).add(vectorPerp.multiply(eAlmaPerfilVAtado/2.0))
    auxY=(anchoPerfilPilar-eAlmaPerfilPilar)/2.0+holgAlaPilarVAtado+solapeRigAlmaV
    listaCoordChapaL=[[-hRig/2.0,0],[-hRig/2.0,auxY-holgAlaPilarVAtado-solapeRigAlmaV],[-hRig/2.0+hAcuerdRig,auxY-holgAlaPilarVAtado-solapeRigAlmaV+hAcuerdRig],[-hRig/2.0+hAcuerdRig,auxY],[hRig/2.0-hAcuerdRig,auxY],[hRig/2.0-hAcuerdRig,auxY-holgAlaPilarVAtado-solapeRigAlmaV+hAcuerdRig],[hRig/2.0,auxY-holgAlaPilarVAtado-solapeRigAlmaV],[hRig/2.0,0]]
    rig=chapaAgSCgen(PtoOr,Base.Vector(0,0,1),vectorDir.normalize(),vectorPerp.normalize(),listaCoordChapaL,[],espesorRig,0)
    vectorDir.normalize().multiply(anchoPerfilPilar/2.0+hAcuerdRig)
    centrocil=vectorDir.add(Base.Vector(0,0,hRig/2.0))
    cil=Part.makeCylinder(hAcuerdRig,500,centrocil,vectorPerp.normalize())
    rig=rig.cut(cil)
    centrocil=vectorDir.add(Base.Vector(0,0,-hRig/2.0))
    cil=Part.makeCylinder(hAcuerdRig,500,centrocil,vectorPerp.normalize())
    rig=rig.cut(cil)
    vatado=vatado.fuse(rig)
    return vatado

def VatSoldAlaPilar(vectorDir,cantoPerfilPilar,LVAtado,tipoPerfilVAtado,idPerfilVAtado):
    #Viga de atado horizontal soldada al ala del pilar
    #vectorDir= vector de dirección de la viga. La viga ha de estar en un plano horizontal, por tanto
    #la coordenada Z de vectorDir debe ser = 0
    #cantoPerfilPilar= canto del pilar
    #LVAtado= longitud de la viga de atado a representar
    vectorDir.normalize().multiply(cantoPerfilPilar/2.0)
    ptoIni=Base.Vector(0,0,0)
    ptoIni.x=vectorDir.x
    ptoIni.y=vectorDir.y
    ptoIni.z=vectorDir.z
    vectorDir.normalize().multiply(LVAtado)
    ptoFin=ptoIni.add(vectorDir)
    vatado=barra2Ptos(ptoIni,ptoFin,tipoPerfilVAtado,idPerfilVAtado,0,0,0)
    return vatado

def parRigOrtAlma(ptoCentral,vDirAlma,vDirAla,cantoPerfil,anchoPerfil,eAlaPerfil,eAlmaPerfil,radioPerfil,eRigid):
    #pareja de rigidizadores ortogonales al alma de un perfil
    #ptoCentral= punto situado en la intersección del plano medio del alma del perfil con el plano 
    #            medio de los rigidizadores
    #vDirAlma= vector de dirección del alma del perfil
    #vDirAla= vector de dirección del ala del perfil
    #cantoPerfil= canto del perfil
    #anchoPerfil= ancho del ala del perfil
    #eAlaPerfil= espesor del ala del perfil
    #eAlmaPerfil= espesor del alma del perfil
    #radioPerfil= radio del acuerdo entre el ala y el alma del perfil
    #eRigid= espesor de los rigidizadores
    #Rigidizador 1
    anchoRig=(anchoPerfil-eAlmaPerfil)/2.0
    altRig=cantoPerfil-2*eAlaPerfil
    vDirXL=vDirAla
    vDirYL=vDirAlma
    aux=vDirAlma.cross(vDirAla)
    vDirZL=Base.Vector(0,0,0)
    vDirZL.x=aux.x
    vDirZL.y=aux.y
    vDirZL.z=aux.z
    vOrigenL=ptoCentral.add(vDirAla.normalize().multiply(eAlmaPerfil/2.0)).add(aux.normalize().multiply(-eRigid/2.0))
    listaCoordChapaL=[[0,altRig/2.0-radioPerfil],[radioPerfil,altRig/2.0],[anchoRig,altRig/2.0],[anchoRig,-altRig/2.0],[radioPerfil,-altRig/2.0],[0,-altRig/2.0+radioPerfil]]
    listaCoordAgujL=[]
    espesorChapa=eRigid
    diamAguj=0
    rig1=chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
    #Rigidizador 2
    vDirXL=vDirAla.multiply(-1)
    vOrigenL=vOrigenL.add(vDirXL.normalize().multiply(eAlmaPerfil))
    rig2=chapaAgSCgen(vOrigenL,vDirXL,vDirYL,vDirZL,listaCoordChapaL,listaCoordAgujL,espesorChapa,diamAguj)
    rigidizadores=rig1.fuse(rig2)
    return rigidizadores

