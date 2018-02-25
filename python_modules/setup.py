# -*- coding: utf-8 -*-
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

setup(name='landXMLToFreeCAD',
      version='0.9.0',
      description='Python utils for FreeCAD (mostly for structural/civil engineering)',
      author='Luis C. Pérez Tato',
      author_email='l.pereztato@gmail.com',
      packages=['landXMLtoFreeCAD'],
     )

setup(name='freeCAD_civil',
      version='0.9.0',
      description='Tool library for civil work with FreeCAD (RC and metallic structures)',
      author='Ana Ortega',
      author_email='ana.ortega@xcengineering.xyz',
      packages=['freeCAD_civil'],
     )

setup(name='freeCAD_utils',
      version='0.9.0',
      description='Generic tool library for working with FreeCAD',
      author='Ana Ortega',
      author_email='ana.ortega@xcengineering.xyz',
      packages=['freeCAD_utils'],
     )

setup(name='setting_out_work',
      version='0.9.0',
      description='Tools for setting-out works',
      author='Ana Ortega',
      author_email='ana.ortega@xcengineering.xyz',
      packages=['setting_out'],
     )

setup(name='RC_utils',
      version='0.9.0',
      description='Tools for the design of reinforced concrete',
      author='Ana Ortega',
      author_email='ana.ortega@xcengineering.xyz',
      packages=['RC_utils'],
     )
