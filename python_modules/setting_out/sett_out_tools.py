# -*- coding: utf-8 -*-

from __future__ import division

__author__= "Ana Ortega (AO_O)"
__cppyright__= "Copyright 2017, AO_O"
__license__= "GPL"
__version__= "1.0"
__email__= " l.pereztato@gmail.com"



import numpy as np
import math
import pandas
import os.path

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def grads_to_rads(angle):
    '''Converts angle in grads (centesimal) into radians'''
    return angle*math.pi/200.


def degr_to_grads(angle):
    '''Converts angle in degrees (sexagesimal) into grads (centesimal) '''
    return angle*200/180.


def sett_out_marco(xAxesInters,yAxesInters,azimuthStruct,Hgauge,thWall,LaxisNeg,LaxisPos,skewAngle=0):
    '''Setting-out points of a box-section underpass.

    :param xAxesInters: X-coordinate of the point of intersection of 
                        the road axis with the structure axis.
    :param yAxesInters: Y-coordinates of the point of intersection of 
                        the road axis with the structure axis.
    :param azimuthStructLax: azimuth of the structure longitudinal axis [grads] 
                         (clockwise from the north line base).
    :param Hgauge:       horizontal clearance gauge.
    :param thWall:       wall thickness
    :param LaxisNeg:     length of longitudinal axis from the axes intersection
                         point towards aletas 1 and 2
    :param LaxisPos:     length of longitudinal axis from the axes intersection
                         point towards aletas 3 and 4
    :param skewAngle:    skew angle [grads] (clockwise) (defaults to 0) 
    '''
    azimuthStructRad=grads_to_rads(azimuthStruct)
    ptAxesInters=np.array([xAxesInters,yAxesInters])
    unitVectStrAxis=np.array([math.sin(azimuthStructRad),math.cos(azimuthStructRad)])
    unitVectOrtogStrAxis=np.array([math.sin(azimuthStructRad+math.pi/2.),math.cos(azimuthStructRad+math.pi/2.)])
    demiDimHor=Hgauge/2.0+thWall
    skewVect=demiDimHor*math.tan(grads_to_rads(skewAngle))*unitVectStrAxis
    print skewVect                       
    pt_start_aleta1=ptAxesInters-LaxisNeg*unitVectStrAxis-demiDimHor*unitVectOrtogStrAxis+skewVect
    pt_start_aleta2=ptAxesInters-LaxisNeg*unitVectStrAxis+demiDimHor*unitVectOrtogStrAxis-skewVect
    pt_start_aleta3=ptAxesInters+LaxisPos*unitVectStrAxis+demiDimHor*unitVectOrtogStrAxis-skewVect
    pt_start_aleta4=ptAxesInters+LaxisPos*unitVectStrAxis-demiDimHor*unitVectOrtogStrAxis+skewVect
    return (pt_start_aleta1,pt_start_aleta2,pt_start_aleta3,pt_start_aleta4)
    
    
def end_point_aleta(start_point,azimuthAleta,lengths):
    unitVectAleta=np.array([math.sin(grads_to_rads(azimuthAleta)),math.cos(grads_to_rads(azimuthAleta))])
    totalLength=np.cumsum(lengths)[-1]
    end_point=start_point+totalLength*unitVectAleta
    return end_point


def sett_out_aleta(start_point,azimuthAleta,azimuthPuntera,wCoron,lengths,widths,widthsPuntera):
    pointsAleta=np.zeros((4*len(lengths),2))
    pointsTalon=np.zeros((2*len(lengths),2))
    pointsPuntera=np.zeros((2*len(lengths),2))
    unitVectAleta=np.array([math.sin(grads_to_rads(azimuthAleta)),math.cos(grads_to_rads(azimuthAleta))])
    unitVectPuntera=np.array([math.sin(grads_to_rads(azimuthPuntera)),math.cos(grads_to_rads(azimuthPuntera))])
    wPunt=np.array(widthsPuntera)+wCoron
    wTalon=np.array(widths)-wPunt
    cumlengths=np.cumsum(lengths)
    cumlengths=np.insert(cumlengths,0,0)
    #Points talón
    for i in range(len(lengths)):
        print 'point talón:', 2*i
        print 'L=', cumlengths[i]
        print 'width=', wTalon[i]
        pointsTalon[2*i]=start_point+cumlengths[i]*unitVectAleta-wTalon[i]*unitVectPuntera
        print 'point talón:', 2*i+1
        print 'L=', cumlengths[i+1]
        print 'width=', wTalon[i]
        pointsTalon[2*i+1]=start_point+cumlengths[i+1]*unitVectAleta-wTalon[i]*unitVectPuntera
    print 'poinstTalon=',pointsTalon
    #Points puntera
    for i in range(len(lengths)):
        pointsPuntera[2*i]=start_point+cumlengths[i]*unitVectAleta+wPunt[i]*unitVectPuntera
        pointsPuntera[2*i+1]=start_point+cumlengths[i+1]*unitVectAleta+wPunt[i]*unitVectPuntera
    print 'pointsPuntera=',pointsPuntera
    #Arranging the point matrix
    pointsAleta[0]=pointsPuntera[0]
    for i in range(2*len(lengths)):
        pointsAleta[i+1]=pointsTalon[i]
    for i in range(1,2*len(lengths)):
        pointsAleta[2*len(lengths)+i]=pointsPuntera[-i]
    print 'pointsAleta=',pointsAleta
    return pointsAleta


def write_points_to_file(title,pointsArr,nDecimalP,fileName,indPntChr=False):
    '''Write the calculated point coordinates included in array pointsArr 
    to file fileName.

    :param title: title to identify the points (e.g. 'ALETA 1')
    :param pointsArr: array with X,Y coord. of the points
    :param nDecimalP: number of decimal places to write coordinates.
    :param fileName: path and name of the file to which append the coordinates
    :param indPntChr: True if points are to be identified with the alphabet 
                      letters, Defaults to False (points identified with
                      numbers 1, 2, 3, ...)

    '''
    if os.path.isfile(fileName):
        f=open(fileName,'a')
    else:
        f=open(fileName,'w')
    f.write('\n\n'+title+ '\n')
    if indPntChr:
        ascii_uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        index=[ascii_uppercase[i] for i in range(len(pointsArr))]
    else:
        index=[i  for i in range(1,len(pointsArr)+1)]
    f.close()
    df = pandas.DataFrame(data=np.around(pointsArr,nDecimalP),index=index,columns=['X','Y'])
    print df
    df.to_csv(fileName,header=True, index=True,sep='\t',float_format='%.3f',mode='a')
    return
        



import numpy

dtype = [('X','float32'), ('Y','float32')]
values = numpy.zeros(20, dtype=dtype)
index = ['Row'+str(i) for i in range(1, len(values)+1)]

df = pandas.DataFrame(values, index=index)

dtype=np.dtype([('X',np.float64),('Y',np.float64)])
