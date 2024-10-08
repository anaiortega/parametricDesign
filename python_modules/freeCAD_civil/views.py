# -*- coding: utf-8 -*-
from __future__ import division

import Part, FreeCAD, FreeCADGui, math, TechDraw


def vistaSuperior(tamHoja,orientacion):
    #tamHoja: tamaño de la hoja, a elegir entre 'A4', 'A3', 'A1'
    #orientacion: orientación de la hoja, puede ser 'vertical' o 'apaisado'
    CreaHoja(tamHoja,orientacion)
    figura=Gui.Selection.getSelectionEx()[0]
    FreeCAD.activeDocument().addObject('TechDraw::FeatureViewPart','topView')
    FreeCAD.activeDocument().topView.Source = figura.Object


def CreaHoja(tamHoja,orientacion):
    FreeCAD.activeDocument().addObject('TechDraw::FeaturePage','vista')
    FreeCAD.activeDocument().vista.Template = App.getResourceDir()+'Mod/TechDraw/Templates/'+tamHoja+'_'+orientacion+'.svg'

