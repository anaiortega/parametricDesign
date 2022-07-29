# -*- coding: utf-8 -*-
from __future__ import division
import math

class SlopedWall(object):
    '''
    :ivar alpha: embankment slope (radians)
    :ivar Lambda: angle between the wall and the road axis (radians)
    '''
    def __init__(self):

    def getAngleTopFace(self):
        '''Return the angle between the top face of the wall and the plane of 
        the foundation required to contain the embankment 
        (see fig. getAngleTopFace.png).
        '''
        retval=math.atan(math.tan(self.alpha)*math.sin(self.Lambda))
        return retval


    def getAngleFillingOverWall(self):
        '''Return the angle of the filling on top of the wall 
        (see fig. getAngleFillingOverWall)
        '''
        retval=math.atan(math.tan(self.alpha)*math.sin(math.Pi/2-self.Lambda))
    
        
