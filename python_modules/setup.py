# -*- coding: utf-8 -*-
#!/usr/bin/env python

from __future__ import print_function

#!/usr/bin/env python

# Copyright (C) 2018  Ana Ortega
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 USA
#
# See http://www.xcengineering.xyz/ or email : ana.ortega@xcengineering.xyz
# freeCAD_civil: Tool library for civil work with FreeCAD (RC and metallic structures)
# freeCAD_utils: Generic tool library for working with FreeCAD
# setting_out_work: Tools for setting-out works
# landXMLToFreeCAD: Python utils for FreeCAD (mostly for structural/civil engineering)
# RC_utils: Tools for the design of reinforced concrete
# 


from distutils.core import setup
import sys

myPrefix = sys.prefix
if len (sys.argv) > 2:
    i = 0
    for o in sys.argv:
        if o.startswith ("--prefix"):
            if o == "--prefix":
                if len (sys.argv) >= i:
                    myPrefix = sys.argv[i + 1]
                sys.argv.remove (prefix)
            elif o.startswith ("--prefix=") and len (o[9:]):
                myPrefix = o[9:]
            sys.argv.remove (o)
        i += 1
if not myPrefix and "PREFIX" in os.environ:
    myPrefix = os.environ["PREFIX"]
if not myPrefix or not len (myPrefix):
    myPrefix = "/usr/local"

setup(name='parametricDesign',
      author='Ana Ortega',
      packages=['freeCAD_civil','freeCAD_civil/structures','freeCAD_utils','geometry_utils','landXMLtoFreeCAD','RC_utils','setting_out','layout_utils']
      )
