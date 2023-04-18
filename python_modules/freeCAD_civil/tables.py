import FreeCAD, Draft
from FreeCAD import Vector
import FreeCADGui
from freeCAD_civil import draw_config as cfg
from freeCAD_utils import drawing_tools as dt


def drawBoxWtitle(pntTLcorner,wColumns,title,hText,hRows,numRows,doc):
    '''Draws the skeleton of lines and title to make a table.
    Return the point in the top left corner to start the new row

    :param pntTLcorner: vector(x,y) to place the top left corner of the table
    :param wColumns: list with the width of the columns
    :param title: general title of the table
    :param hText: height of the text
    :param numRows: number of rows of data (titles excluded) 
    '''
    FreeCAD.setActiveDocument(doc.Name)
    totalWidth=sum(wColumns)
    totalHeight=hRows*(numRows+2)
    pl=FreeCAD.Placement()
    pl.Rotation.Q = (0.0, 0.0, 0.0, 1.0)
    pl.Base = pntTLcorner-Vector(0,totalHeight)
    w=Draft.makeRectangle(totalWidth,totalHeight,placement=pl)
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorFrames
    p1=pntTLcorner-Vector(0,totalHeight)
    p2=p1.add(Vector(0,hRows*(numRows+1)))
    # Vertical lines
    for i in range (0,len(wColumns)):
        p1=p1.add(Vector(wColumns[i],0))
        p2=p2.add(Vector(wColumns[i],0))
        w=Draft.makeLine(p1,p2)
        FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorLinesTables
    p1=pntTLcorner-Vector(0,2*hRows)
    p2=p1.add(Vector(totalWidth,0))
    w=Draft.makeLine(p1,p2)
    # Generate title of the table
    pLinea=p1.add(Vector(0,hRows))
    w=Draft.makeLine(pLinea,pLinea.add(Vector(totalWidth,0)))
    FreeCADGui.ActiveDocument.getObject(w.Name).LineColor = cfg.colorFrames
    pPos=pLinea.add(Vector(totalWidth/2.0,hRows/2-1.25*hText/2))
    dt.put_text_in_pnt(title,pPos,1.25*hText,cfg.colorTextCenter,"Center")
    FreeCAD.ActiveDocument.recompute()
    pntNextTLcorner=p1
    return pntNextTLcorner
   

def settingOutTable(lstPoints,title,pntTLcorner=Vector(0,100),preffixPnt='',tbCfg=cfg.setoutCfg,vCooRel2Abs=Vector(0,0,0),doc=FreeCAD.ActiveDocument):
    '''Create a survey coordinate table from the points in list lstPoints.
    :param lstPoints: list of staking points (freeCAD vectors)
    :param title: title for the table
    :param pntTLcorner: vector(x,y) to place the top left corner of the table (defaults 
           to Vector(0,100))
    :param preffixPnt: preffix to name the points
    :param tbCfg: instance of class tableConf, where the width of columns, 
                            the rows height and the text height are defined.
    :param vCooRel2Ab: vector to add to points to convert model coordinates in
           survey coordinates (defaults to Vector(0,0,0))
    :param doc: document in which to put the schedule (defaults to the 
                active document)
    '''
    FreeCAD.setActiveDocument(doc.Name)
    numRows=len(lstPoints)
    p1=drawBoxWtitle(pntTLcorner,tbCfg.wColumns,title.upper(),tbCfg.hText,tbCfg.hRows,numRows,doc)
    pLinea=p1.add(Vector(0,tbCfg.hRows/2.0))
    pPos=pLinea.add(Vector(tbCfg.hText/2.0,-tbCfg.hText/2.0))
    dt.put_text_in_pnt('PUNTO',pPos,tbCfg.hText,cfg.colorTextLeft)
    pX=pLinea.add(Vector(tbCfg.wColumns[0]+tbCfg.wColumns[1]/2.0,-tbCfg.hText/2.0))
    dt.put_text_in_pnt('X',pX,tbCfg.hText,cfg.colorTextCenter,"Center")
    pY=pLinea.add(Vector(sum(tbCfg.wColumns[:2])+tbCfg.wColumns[2]/2.0,-tbCfg.hText/2.0))
    dt.put_text_in_pnt('Y',pY,tbCfg.hText,cfg.colorTextCenter,"Center")
    pZ=pLinea.add(Vector(sum(tbCfg.wColumns[:3])+tbCfg.wColumns[3]/2.0,-tbCfg.hText/2.0))
    dt.put_text_in_pnt('Z',pZ,tbCfg.hText,cfg.colorTextCenter,"Center")
    for i in range(len(lstPoints)):
        pnt=preffixPnt+str(i+1)
        p=lstPoints[i].add(vCooRel2Abs)
        x='{:.3f}'.format(p.x)
        y='{:.3f}'.format(p.y)
        z='{:.3f}'.format(p.z)
        pLinea=pLinea.add(Vector(0,-tbCfg.hRows))
        pPos=pLinea.add(Vector(tbCfg.hText/2.0,-tbCfg.hText/2.0))
        dt.put_text_in_pnt(pnt,pPos,tbCfg.hText,cfg.colorTextLeft)
        pX=pLinea.add(Vector(sum(tbCfg.wColumns[:2])-tbCfg.hText/2.0,-tbCfg.hText/2.0))
        dt.put_text_in_pnt(x,pX, tbCfg.hText, cfg.colorTextRight,"Right")
        pY=pLinea.add(Vector(sum(tbCfg.wColumns[:3])-tbCfg.hText/2.0,-tbCfg.hText/2.0))
        dt.put_text_in_pnt(y,pY, tbCfg.hText, cfg.colorTextRight,"Right")
        pZ=pLinea.add(Vector(sum(tbCfg.wColumns)-tbCfg.hText/2.0,-tbCfg.hText/2.0))
        dt.put_text_in_pnt(z,pZ, tbCfg.hText, cfg.colorTextRight,"Right")
    FreeCAD.ActiveDocument.recompute()


def genericTable(lstData,title,colTitles,wColumns,formatColumns,hRows=4.00,hText=2.5,pntTLcorner=Vector(0,100),doc=FreeCAD.ActiveDocument):
    '''Create a table with values in lstData.

    :param lstData: list of data [[u1,u2,..],[v1,v2,..],...], each list corresponds to a row.
    :param title: title for the table
    :param colTitles: titles for the columns
    :param wColumns: list with the width of the columns.
    :param formatColumns: list with the format of numbers for each column 
           (ex: ['{}','{:.0f}','{:.2f}', ...])
    :param hRows: height of the rows
    :param hText: height of the text
    :param pntTLcorner: vector(x,y) to place the top left corner of the table (defaults 
           to Vector(0,100))
    :param doc: document in which to put the schedule (defaults to the 
                active document)

    '''
    FreeCAD.setActiveDocument(doc.Name)
    numRows=len(lstData)
    p1=drawBoxWtitle(pntTLcorner,wColumns,title.upper(),hText,hRows,numRows,doc)
    pLinea=p1.add(Vector(0,hRows/2.0-hText/2.0))
    for i in range(len(colTitles)):
        pPos=pLinea+Vector(sum(wColumns[:i])+wColumns[i]/2.0,0)
        dt.put_text_in_pnt(colTitles[i],pPos,hText,cfg.colorTextCenter,"Center")
    for l in range(len(lstData)):
        pLinea=pLinea.add(Vector(0,-hRows))
        dataRow=lstData[l]
        for i in range(len(dataRow)):
            pPos=pLinea+Vector(sum(wColumns[:(i+1)])-hText/2,0)
            f=formatColumns[i] ; nmb=f.format(dataRow[i])
            dt.put_text_in_pnt(nmb,pPos,hText, cfg.colorTextRight,"Right")
    FreeCAD.ActiveDocument.recompute()

    
    
         
