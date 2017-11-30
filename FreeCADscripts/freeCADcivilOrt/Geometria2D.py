# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, math
import Draft
from FreeCAD import Base

def int2rectas(P1,P2,P3,P4):
    # Devuelve el punto de intersección de 2 rectas 2D
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


def fillet2D(Pini,P2recta1,P1recta2,Pfin,radioConSigno):
    # Devuelve dos segmentos de las rectas definidas por los ptos Pini-P2recta1 y P1recta2-Pfin y el arco de circunferencia de radio igual al valor absoluto de radioConSigno que es tangente a ellas.
    # Pini: pto. 1 de la recta 1, será el 1er pto. de la línea que devuelve la función
    # P2recta1: pto. 2 de la recta 1
    # P1recta2:  pto. 1 de la recta 2
    # Pfin: pto. 2 de la recta 2, será el último pto. de la línea que devuelve la función
    # radioConSigno: radio del arco de circunferencia tangente signo + si de Pini a Pfin gira en el sentido contrario a las agujas del reloj, - en caso contrario.
    signo=radioConSigno/abs(radioConSigno)
    v1=P2recta1.sub(Pini)
    v1.normalize() #vector de dirección de la recta 1
    v2=Pfin.sub(P1recta2)
    v2.normalize() #vector de dirección de la recta 2
    vP1=Base.Vector(-1*signo*v1.y,signo*v1.x)
    vP1.normalize() #vector de dirección perpendicular a la recta 1
    vP1.multiply(abs(radioConSigno))
    vP2=Base.Vector(-1*signo*v2.y,signo*v2.x)
    vP2.normalize() #vector de dirección perpendicular a la recta 2
    vP2.multiply(abs(radioConSigno))
    Paux1=Pini.add(vP1)
    Paux2=Paux1.add(v1)
    Paux3=Pfin.add(vP2)
    Paux4=Paux3.add(v2)
    centro=int2rectas(Paux1,Paux2,Paux3,Paux4)
    vP1.multiply(-1)
    vP2.multiply(-1)
    Pfin1=centro.add(vP1)
    Pini2=centro.add(vP2)
    segm1=Part.makeLine(Pini,Pfin1)
    ang1=angVector2DEjeX(vP1)
    ang2=angVector2DEjeX(vP2)
    if signo==1:
        arco=Part.makeCircle(abs(radioConSigno),centro,Base.Vector(0,0,1),ang1,ang2)
    else:
        arco=Part.makeCircle(abs(radioConSigno),centro,Base.Vector(0,0,1),ang2,ang1)

    segm2=Part.makeLine(Pini2,Pfin)
    linea=Part.Wire([segm1,arco,segm2])
    return linea

    
def angVector2DEjeX(vector2D):
    # Devuelve el ángulo en grados (entre 0 y 360) que forma el vector con el eje X
    # Los ángulos crecen en sentido contrario a las agujas del reloj
    abcisa=vector2D.x
    ordenada=vector2D.y
    if abcisa==0:
        if ordenada <0:
            angulo=270
        else:
            angulo=90
    else:
        angulo=math.atan(abs(ordenada)/abs(abcisa))*180.0/math.pi
        if abcisa < 0:
            if ordenada > 0:
                angulo=180-angulo
            else:
                angulo=180+angulo
        else:
            if ordenada < 0:
                angulo=360-angulo
    return angulo

def arcoCoronaCircular(rInt,rExt,vectorCentro,angIni,angFin):
    # Devuelve el arco de la corona circular (en el plano XY) definido por:
    # rInt: radio interior
    # rExt: radio exterior
    # vectorCentro: centro del círculo (coordenadas x,y)
    # angIni: ángulo inicial (0 a 360º)
    # angFin: ángulo final (0 a 360º)
    # Los ángulos crecen en sentido contrario a las agujas del reloj
    arcoExt=Part.makeCircle(rExt,vectorCentro,Base.Vector(0,0,1),angIni,angFin)
    arcoInt=Part.makeCircle(rInt,vectorCentro,Base.Vector(0,0,1),angIni,angFin)
    angIni=angIni*math.pi/180.0
    angFin=angFin*math.pi/180.0
    r1=Part.makeLine(vectorCentro.add(Base.Vector(rInt*math.cos(angIni),rInt*math.sin(angIni))),vectorCentro.add(Base.Vector(rExt*math.cos(angIni),rExt*math.sin(angIni))))
    r2=Part.makeLine(vectorCentro.add(Base.Vector(rInt*math.cos(angFin),rInt*math.sin(angFin))),vectorCentro.add(Base.Vector(rExt*math.cos(angFin),rExt*math.sin(angFin))))
    arcCoron=Part.Face(Part.Wire([arcoExt,r1,arcoInt,r2]))
    return arcCoron

