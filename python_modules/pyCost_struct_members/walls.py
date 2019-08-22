# -*- coding: utf-8 -*-
from __future__ import division

#Class to generate pyCost quantities of wall structural members.

import math

class WallBase(object):
    '''Base class to calculate quantities of a wall.

    :textComment:   string to comment each measuremt line generated
    :Lenght: wall length
    :meanHeight: mean wall height
    :meanThickness: mean wall thickness 
    :reinfQuant: reinforcement quantity
    '''
    def __init__(self,textComment,Length,meanHeight,meanThickness,reinfQuant):
        self.textComment=textComment
        self.Length=Length
        self.meanHeight=meanHeight
        self.meanThickness=meanThickness
        self.reinfQuant=reinfQuant

    def getReinfConcrete(self):
        '''Return reinforcing concrete quantities to be added to a pyCost 
        project '''
        qntLines=list()
        qntLines.append([self.textComment,1, self.Length, self.meanThickness, self.meanHeight])
        return qntLines
        
    def getReinforcement(self):
        '''Return reinforcement quantities to be added to a pyCost project '''
        qntLines=list()
        if self.reinfQuant>0:
            qntLines.append([self.textComment + ' s/med. aux.',1, self.reinfQuant, None, None])
        return qntLines

class SlopedWallBase(WallBase):
    '''Base class to calculate quantities of a sloped wall.

    :textComment:   string to comment each measuremt line generated 
    :Length: wall length (horizontal projection)
    :Height: wall height (if sloped Height = maximum length of the wall)
    :Thickness: thickness of the stem at the top face. 
    :reinfQuant: reinforcement quantity
    :SlopeTopFace: slope of the top face (H:V) (defaults to 0)
    :SlopeFrontFace: vertical slope at the front face (H:V) (defaults to 0)
    :SlopeBackFace: vertical slope of the back or earth-face (H:V) (defaults to 0)
    '''
    
    def __init__(self,textComment,Length,Height,Thickness,reinfQuant,SlopeTopFace=0,SlopeFrontFace=0,SlopeBackFace=0):
        HeightSect2=Height-Length/SlopeTopFace
        mnHeight=round(0.5*(Height+HeightSect2),2) #height at middle section
        mnThickness=round(Thickness+(Height+HeightSect2)*(SlopeFrontFace+SlopeBackFace)/4.,2)
        super(SlopedWallBase,self).__init__(textComment,Length,mnHeight,mnThickness,reinfQuant)
        self.Thickness=Thickness
        self.SlopeTopFace=SlopeTopFace
        self.SlopeFrontFace=SlopeFrontFace
        self.SlopeBackFace=SlopeBackFace

class RetainingWall(SlopedWallBase):
    '''Quantities of a retainig wall.

    :textComment:   string to comment each measuremt line generated 
    :Length: wall length (horizontal projection)
    :Height: wall height (if sloped Height = maximum length of the wall)
    :Thickness: thickness of the stem at the top face. 
    :reinfQuant: reinforcement quantity
    :SlopeTopFace: slope of the top face (H:V) (defaults to 0)
    :SlopeFrontFace: vertical slope at the front face (H:V) (defaults to 0)
    :SlopeEarthFace: vertical slope of the earth-face (H:V) (defaults to 0)
    :FormworkLateral1: if formwork on the highgest lateral face ='Y' (defaults 
    to yes)
    :FormworkLateral2: if formwork on the highgest lateral face ='Y' (defaults 
    to yes)
    '''
    
    def __init__(self,textComment,Length,Height,Thickness,reinfQuant,SlopeTopFace=0,SlopeFrontFace=0,SlopeEarthFace=0,FormworkLateral1='Y',FormworkLateral2='Y'):
        self.maxHeight=Height
        super(RetainingWall,self).__init__(textComment,Length,Height,Thickness,reinfQuant,SlopeTopFace,SlopeFrontFace,SlopeEarthFace)
        self.FormworkLateral1=FormworkLateral1
        self.FormworkLateral2=FormworkLateral2

    def getHiddenWallFormwork(self):
        '''Return hidden-wall formwork quantities to be added to a pyCost project '''
        qntLines=list()
        formWidth=round(self.meanHeight*math.sqrt(1+self.SlopeBackFace**2),2)
        qntLines.append([self.textComment,1,self.Length,formWidth,None])
        print self.FormworkLateral1
        if self.FormworkLateral1.lower()[0]=='y':
            print 'aquí', self.Thickness
            H=self.maxHeight
            B1=self.Thickness
            B2=self.Thickness+H*self.SlopeFrontFace+H*self.SlopeBackFace
            print 'B1= ', B1, 'B2= ',B2
            qntLines.append([self.textComment,1,None,round((B1+B2)/2.,2),H])
        if self.FormworkLateral2.lower()[0]=='y':
            H=round(self.maxHeight-self.Length/self.SlopeTopFace,2)
            B1=self.Thickness
            B2=self.Thickness+H*self.SlopeFrontFace+H*self.SlopeBackFace
            print 'B1= ', B1, 'B2= ',B2
            qntLines.append([self.textComment,1,None,round((B1+B2)/2.,2),H])
        return qntLines

    def getExposedWallFormwork(self):
        '''Return exposed-wall formwork quantities to be added to a pyCost project '''
        formWidth=round(self.meanHeight*math.sqrt(1+self.SlopeFrontFace**2),2)
        qntLines=list()
        qntLines.append([self.textComment,1,self.Length,formWidth,None])
        return qntLines

    def getWaterproofingPrimer(self):
        '''Return waterproofing primer quantities to be added to a pyCost project '''
        qntLines=list()
        watproofWidth=round(self.meanHeight*math.sqrt(1+self.SlopeBackFace**2),2)
        qntLines.append([self.textComment,1,self.Length,watproofWidth,None])
        return qntLines
        
    def getWaterproofingLayer(self):
        '''Return waterproofing layer quantities to be added to a pyCost project '''
        return self.getWaterproofingPrimer()

    def getDrainageTube(self):
        '''Return drainage tube quantities to be added to a pyCost project '''
        qntLines=list()
        qntLines.append([self.textComment,1,self.Length,None,None])
        return qntLines
        
       
        
class TwoExposedSideWall(SlopedWallBase):
    '''Quantities of a two-exposed-side wall.

    :textComment:   string to comment each measuremt line generated 
    :Length: wall length (horizontal projection)
    :Height: wall height (if sloped Height = maximum length of the wall)
    :Thickness: thickness of the stem at the top face. 
    :reinfQuant: reinforcement quantity
    :SlopeTopFace: slope of the top face (H:V) (defaults to 0)
    :SlopeFrontFace: vertical slope at the front face (H:V) (defaults to 0)
    :SlopeBackFace: vertical slope of the back face (H:V) (defaults to 0)
    :FormworkLateral1: if formwork on the highgest lateral face ='Y' (defaults 
    to yes)
    :FormworkLateral2: if formwork on the highgest lateral face ='Y' (defaults 
    to yes)
    '''
    
    def __init__(self,textComment,Length,Height,Thickness,reinfQuant,SlopeTopFace=0,SlopeFrontFace=0,SlopeBackFace=0,FormworkLateral1='Y',FormworkLateral2='Y'):
        self.maxHeight=Height
        super(TwoExposedSideWall,self).__init__(textComment,Length,Height,Thickness,reinfQuant,SlopeTopFace,SlopeFrontFace,SlopeBackFace)
        self.FormworkLateral1=FormworkLateral1
        self.FormworkLateral2=FormworkLateral2

    def getExposedWallFormwork(self):
        '''Return exposed-wall formwork quantities to be added to a pyCost project '''
        qntLines=list()
        formWidth=round(self.meanHeight*math.sqrt(1+self.SlopeFrontFace**2),2)
        qntLines.append([self.textComment,1,self.Length,formWidth,None])
        formWidth=round(self.meanHeight*math.sqrt(1+self.SlopeBackFace**2),2)
        qntLines.append([self.textComment,1,self.Length,formWidth,None])
        if self.FormworkLateral1.lower()[0]=='y':
            H=self.maxHeight
            B1=self.Thickness
            B2=self.Thickness+H*self.SlopeFrontFace+H*self.SlopeBackFace
            print 'B1= ', B1, 'B2= ',B2
            qntLines.append([self.textComment,1,None,round((B1+B2)/2.,2),H])
        if self.FormworkLateral2.lower()[0]=='y':
            H=round(self.maxHeight-self.Length/self.SlopeTopFace,2)
            B1=self.Thickness
            B2=self.Thickness+H*self.SlopeFrontFace+H*self.SlopeBackFace
            print 'B1= ', B1, 'B2= ',B2
            qntLines.append([self.textComment,1,None,round((B1+B2)/2.,2),H])
        return qntLines

'''
wall=RetainingWall(textComment='wall',Length=5,Height=4,Thickness=0.3,reinfQuant=5000,SlopeTopFace=4.,SlopeFrontFace=1/15.,SlopeEarthFace=1/12.,FormworkLateral1='Y',FormworkLateral2='Y')    

wallExp=TwoExposedSideWall(textComment='wall',Length=5,Height=4,Thickness=0.3,reinfQuant=5000,SlopeTopFace=4.,SlopeFrontFace=1/15.,SlopeBackFace=1/12.,FormworkLateral1='Y',FormworkLateral2='Y')    
'''
