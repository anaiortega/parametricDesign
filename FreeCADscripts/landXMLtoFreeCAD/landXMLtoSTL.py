# -*- coding: utf-8 -*-

import LandXMLtoFreeCad as reader
import sys

xmlFileName= sys.argv[1]
stlFileName= sys.argv[2]

xmlModel= reader.LandXMLModel(xmlFileName)
xmlModel.writeSTL(stlFileName)


