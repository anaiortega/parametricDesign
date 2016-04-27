# -*- coding: utf-8 -*-
from __future__ import division

import re
import xml.etree.ElementTree as ET
import xc_base
import geom 

def extractTag(str):
  tmp= str.split('}')
  return tmp[1]

def getCoordinates(str):
  tmp= str.split(' ')
  return [float(tmp[0]),float(tmp[1]),float(tmp[2])]

def getVertices(str):
  tmp= str.split(' ')
  retval= list()
  for s in tmp:
    retval.append(int(s))
  return retval

def slugify(s):
    """
    Simplifies ugly strings into something URL-friendly.
    >>> print slugify("[Some] _ Article's Title--")
    some-articles-title
    """

    # "[Some] _ Article's Title--"
    # "[some] _ article's title--"
    s = s.lower()

    # "[some] _ article's_title--"
    # "[some]___article's_title__"
    for c in [' ', '-', '.', '/']:
        s = s.replace(c, '_')

    # "[some]___article's_title__"
    # "some___articles_title__"
    s = re.sub('\W', '', s)

    # "some___articles_title__"
    # "some   articles title  "
    s = s.replace('_', ' ')

    # "some   articles title  "
    # "some articles title "
    s = re.sub('\s+', ' ', s)

    # "some articles title "
    # "some articles title"
    s = s.strip()

    # "some articles title"
    # "some_articles_title"
    s = s.replace(' ', '_')

    return s

class Surface(object):
  def __init__(self,name):
    self.name= slugify(name)
    self.dictPoints= dict()
    self.triangles= list()
  def appendPoint(self,id,coord):
    self.dictPoints[id]= coord
  def appendTriangle(self,vertices):
    self.triangles.append(vertices)
  def getNumPoints(self):
    return len(self.dictPoints)
  def getNumTriangles(self):
    return len(self.triangles)
  def writeSTL(self,stlFile):
    '''Writes the triangle mesh in a STL file.'''
    stlFile.write('solid '+self.name+'\n')
    for tr in self.triangles:
      v0= self.dictPoints[tr[0]]; v1= self.dictPoints[tr[1]]; v2= self.dictPoints[tr[2]]
      p0= geom.Pos3d(v0[0],v0[1],v0[2])
      p1= geom.Pos3d(v1[0],v1[1],v1[2])
      p2= geom.Pos3d(v2[0],v2[1],v2[2])
      face= geom.Triangulo3d(p0,p1,p2)
      normal= face.getPlane().getNormal()
      stlFile.write('facet normal '+str(-normal.x)+' '+str(-normal.y)+' '+str(-normal.z)+'\n')
      stlFile.write('  outer loop\n')
      stlFile.write('    vertex '+ str(p0.x)+' '+str(p0.y)+' '+str(p0.z)+'\n')
      stlFile.write('    vertex '+ str(p1.x)+' '+str(p1.y)+' '+str(p1.z)+'\n')
      stlFile.write('    vertex '+ str(p2.x)+' '+str(p2.y)+' '+str(p2.z)+'\n')
      stlFile.write('  end loop\n')
    stlFile.write('endsolid '+self.name+'\n')
  def write(self,f):
    print(self.name)
    for key in self.dictPoints.keys():
      f.write('pto'+ str(key) + '=Base.Vector('+ str(self.dictPoints[key][0]) +','+ str(self.dictPoints[key][1])+','+ str(self.dictPoints[key][2])+') \n')
    f.write(self.name+'= Part.makeCompound([]) \n')
    for tr in self.triangles:
      f.write(self.name+'= '+self.name+'.fuse(Part.Face(Part.makePolygon([pto' + str(tr[0]) + ',pto' + str(tr[1]) + ',pto' + str(tr[2]) + ',pto' + str(tr[0]) + ']))) \n')
  def list(self,f):
    ''' lists the number of points and triangles int the surface.'''
    f.write('surface name: '+ self.name+'\n') 
    f.write('  number of points: '+ str(len(self.dictPoints))+'\n') 
    f.write('  number of triangles: '+ str(len(self.triangles))+'\n')
 
class LandXMLModel(object):
  def __init__(self,xmlFileName):
    self.surfaces= list()
    tree = ET.parse(xmlFileName)
    root = tree.getroot()
    tmp= root.tag.split('}')
    schema= tmp[0]+'}'

    project= root.find(schema+'Project')
    self.projectName= project.attrib['name']

    for child in root:
      rawTag= child.tag
      tag= extractTag(rawTag)
      #print tag, child.attrib
      if(tag=='Surfaces'):
        for child2 in child:
          rawSurfTag= child2.tag
          surfTag= extractTag(rawSurfTag)
          surfaceName= child2.attrib['name']
          surf= Surface(surfaceName)
          #print '  ', surfTag, child2.attrib
          for child3 in child2:
            rawTag3= child3.tag
            tag3= extractTag(rawTag3)
            #print '    ', tag3, child3.attrib
            if(tag3=='Definition'):
              for child4 in child3:
                rawTag4= child4.tag
                tag4= extractTag(rawTag4)
                #print '      ', tag4, child4.attrib
                if(tag4=='Pnts'):
                  for child5 in child4:
                    rawTag5= child5.tag
                    tag5= extractTag(rawTag5)
                    id= child5.attrib['id']
                    coo= getCoordinates(child5.text)
                    surf.appendPoint(int(id),coo)
                elif(tag4=='Faces'):
                  for child5 in child4:
                    rawTag5= child5.tag
                    tag5= extractTag(rawTag5)
                    vertices= getVertices(child5.text)
                    surf.appendTriangle(vertices)
          print "  surface: ", surf.name, " readed:", surf.getNumPoints(), " points", surf.getNumTriangles(), " triangles"
          self.surfaces.append(surf)
      else:
        print 'tag: ', tag,' ignored.'
  def writeSTL(self,fName):
    '''Writes the surfaces in an STL file.'''
    f= open(fName,'w')
    for s in self.surfaces:
      s.writeSTL(f)
    f.close()
  def write(self,f):
    f.write('#' + self.projectName+'\n')
    for s in self.surfaces:
      s.write(f)

  def list(self,f):
    '''list the surfaces readed'''
    for s in self.surfaces:
      s.list(f)
