# -*- coding: iso-8859-1 -*-

import Part, FreeCAD, FreeCADGui, math, Drawing
from __future__ import division


def vistaSuperior(tamHoja,orientacion):
    #tamHoja: tama�o de la hoja, a elegir entre 'A4', 'A3', 'A1'
    #orientacion: orientaci�n de la hoja, puede ser 'vertical' o 'apaisado'
    CreaHoja(tamHoja,orientacion)
    figura=Gui.Selection.getSelectionEx()[0]
    App.activeDocument().addObject('Drawing::FeatureViewPart','topView')
    App.activeDocument().topView.Source = figura.Object


def CreaHoja(tamHoja,orientacion):
    App.activeDocument().addObject('Drawing::FeaturePage','vista')
    App.activeDocument().vista.Template = App.getResourceDir()+'Mod/Drawing/Templates/'+tamHoja+'_'+orientacion+'.svg'

