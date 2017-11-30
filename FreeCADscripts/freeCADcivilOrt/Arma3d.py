import Part, FreeCAD, math
from FreeCAD import Base
import GeomUtils

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

    
    
