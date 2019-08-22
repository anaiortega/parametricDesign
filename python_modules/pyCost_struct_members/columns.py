# -*- coding: utf-8 -*-
from __future__ import division

#Classes to generate pyCost quantities of column menbers

import math

class ColumnCylind(object):
    '''
    :textComment: string to comment each measuremt line generated 
    :nShafts: number of shafts
    :DiamColumn: diameter
    :Hcolumn: height of the column
    :reinfQuant: reinforcement quantity
    '''
    def __init__(self,textComment,nShafts,DiamColumn,Hcolumn,reinfQuant):
        self.textComment=textComment
        self.nShafts=nShafts
        self.DiamColumn=DiamColumn
        self.Hcolumn=Hcolumn
        self.reinfQuant=reinfQuant
        
    def getReinfConcrete(self):
        '''Return reinforcing concrete quantities to be added to a pyCost 
        project '''
        qntLines=list()
        qntLines.append([self.textComment,self.nShafts, self.Hcolumn, round(math.pi*self.DiamColumn**2/4.,3), None])
        return qntLines

    def getFormwork(self):
        '''Return formwork quantities to be added to a pyCost 
        project '''
        qntLines=list()
        qntLines.append([self.textComment,self.nShafts, self.Hcolumn, round(math.pi*self.DiamColumn,3), None])
        return qntLines

    def getReinforcement(self):
        '''Return reinforcement quantities to be added to a pyCost project '''
        qntLines=list()
        if self.reinfQuant>0:
            qntLines.append([self.textComment + ' s/med. aux.',1, self.reinfQuant, None, None])
        return qntLines

col=ColumnCylind(textComment='column',nShafts=2,DiamColumn=1,Hcolumn=10,reinfQuant=5000)
        
