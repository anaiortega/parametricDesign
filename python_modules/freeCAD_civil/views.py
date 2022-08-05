# -*- coding: iso-8859-1 -*-
from __future__ import division

import Part, FreeCAD, FreeCADGui, math, TechDraw


def vistaSuperior(tamHoja,orientacion):
    #tamHoja: tamaño de la hoja, a elegir entre 'A4', 'A3', 'A1'
    #orientacion: orientación de la hoja, puede ser 'vertical' o 'apaisado'
    CreaHoja(tamHoja,orientacion)
    figura=Gui.Selection.getSelectionEx()[0]
    App.activeDocument().addObject('TechDraw::FeatureViewPart','topView')
    App.activeDocument().topView.Source = figura.Object


def CreaHoja(tamHoja,orientacion):
    App.activeDocument().addObject('TechDraw::FeaturePage','vista')
    App.activeDocument().vista.Template = App.getResourceDir()+'Mod/TechDraw/Templates/'+tamHoja+'_'+orientacion+'.svg'

