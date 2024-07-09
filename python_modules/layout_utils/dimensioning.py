from FreeCAD import Vector
import FreeCADGui
import Draft


def dim_lst_pnts(lstPnts,spacDimLine,styleName="dimStyle"):
    '''Make dimensions between FreeCAD points in lstPnts. 

    :ivar lstPnts: list of FreeCAD points
    :ivar  spacDimLine: spacement to place the dimension line 
    :ivar styleName: name of the dimension style   
           (defaults to styleName="dimStyle"))
    '''
    FreeCADGui.activateWorkbench("DraftWorkbench")
    zVector=Vector(0,0,1)
    for i in range(len(lstPnts)-1):
        p1=lstPnts[i]
        p2=lstPnts[i+1]
        vNorm=zVector.cross(p2-p1)
        vNorm.normalize()
        p3=p1+spacDimLine*vNorm
        d= Draft.make_dimension(p1, p2, p3)
        Draft.autogroup(d)
        FreeCADGui.ActiveDocument.getObject(d.Name).AnnotationStyle=styleName

        
    
