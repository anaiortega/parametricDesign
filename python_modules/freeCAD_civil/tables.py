import math
import Part, FreeCAD, Draft
from FreeCAD import Vector
from freeCAD_civil import draw_config as cfg
import FreeCADGui
from freeCAD_utils import drawing_tools as dt

def drawBoxWtitle(anchPnt,wColumns,title,hText,hRows,numRows):
    totalWidth=sum(wColumns)
    w=Draft.makeRectangle(totalWidth,hRows*(numRows+2))
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
    p1=anchPnt
    p2=p1.add(Vector(0,hRows*(numRows+1)))
    for i in range (0,len(wColumns)):
        p1=p1.add(Vector(wColumns[i],0))
        p2=p2.add(Vector(wColumns[i],0))
        w=Draft.makeLine(p1,p2)
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
    p1=anchPnt+Vector(0,hRows*(numRows))
    p2=p1.add(Vector(totalWidth,0))
    w=Draft.makeLine(p1,p2)
    # Generate title of the table
    pLinea=p1.add(Vector(0,hRows))
    w=Draft.makeLine(pLinea,pLinea.add(Vector(totalWidth,0)))
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorRefLines
    pPos=pLinea.add(Vector(totalWidth/2.0,hRows/2))
    dt.put_text_in_pnt(title,pPos,1.2*hText,cfg.colorTextCenter,"Center")
    return p1
   

def settingOutTable(lstPoints,title,anchPnt=Vector(0,0),preffixPnt='',hText=2.5,hRows=3.75,wColumns=[10,20,20,20]):
    numRows=len(lstPoints)
    p1=drawBoxWtitle(Vector(0,0),wColumns,title,hText,hRows,numRows)
    pLinea=p1.add(Vector(0,hRows/2.0))
    pPos=pLinea.add(Vector(hText/2.0,-hText/2.0))
    dt.put_text_in_pnt('PUNTO',pPos,hText,cfg.colorTextLeft)
    pX=pLinea.add(Vector(wColumns[0]+wColumns[1]/2.0,-hText/2.0))
    dt.put_text_in_pnt('X',pX,hText,cfg.colorTextCenter,"Center")
    pY=pLinea.add(Vector(sum(wColumns[:2])+wColumns[2]/2.0,-hText/2.0))
    dt.put_text_in_pnt('Y',pY,hText,cfg.colorTextCenter,"Center")
    pZ=pLinea.add(Vector(sum(wColumns[:3])+wColumns[3]/2.0,-hText/2.0))
    dt.put_text_in_pnt('Z',pZ,hText,cfg.colorTextCenter,"Center")
    for i in range(len(lstPoints)):
        pnt=preffixPnt+str(i)
        p=lstPoints[i]
        x=round(p.x,3)
        y=round(p.y,3)
        z=round(p.z,3)
        pLinea=pLinea.add(Vector(0,-hRows))
        pPos=pLinea.add(Vector(hText/2.0,0))
        dt.put_text_in_pnt(pnt,pPos,hText,cfg.colorTextLeft)
        pX=pLinea.add(Vector(sum(wColumns[:2])-hText/2.0,-hText/2.0))
        dt.put_text_in_pnt(str(x),pX, hText, cfg.colorTextRight,"Right")
        pY=pLinea.add(Vector(sum(wColumns[:3])-hText/2.0,-hText/2.0))
        dt.put_text_in_pnt(str(y),pY, hText, cfg.colorTextRight,"Right")
        pZ=pLinea.add(Vector(sum(wColumns)-hText/2.0,-hText/2.0))
        dt.put_text_in_pnt(str(z),pZ, hText, cfg.colorTextRight,"Right")
                      

    
    
         
