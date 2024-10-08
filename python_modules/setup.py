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


from setuptools import setup
from setuptools import find_packages
import sys
import version

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

parametric_design_packages= ['freeCAD_civil','freeCAD_civil.structures','freeCAD_utils','geometry_utils','landXMLtoFreeCAD','RC_utils','setting_out','layout_utils']

# Get version
pD_version= version.__version__
pD_deb_pkg_folder= None
pD_installation_target= None
usr_local_pth= None
with open('./pd_installation_target.txt','r') as f:
    pd_version= f.readline().strip()
    sys_arch= f.readline().strip()
    pd_deb_pkg_folder= f.readline().strip()
    pd_installation_target= f.readline().strip()
    usr_local_pth= f.readline().strip()
if (pd_version is None):
    logging.error('PD_VERSION not set.')
    exit(1)
if (sys_arch is None):
    logging.error('SYS_ARCH not set.')
    exit(1)
if (pd_deb_pkg_folder is None):
    logging.error('PD_DEB_PKG_FOLDER not set.')
    exit(1)
if (pd_installation_target is None):
    logging.error('PD_INSTALLATION_TARGET not set.')
    exit(1)
if (usr_local_pth is None):
    logging.error('USR_LOCAL not set.')
    exit(1)
    
print('PD temporary folder: '+pd_deb_pkg_folder)
print('PD temporary installation target: '+pd_installation_target)

setup(name='parametricDesign',
      version= pd_version,
      author='Ana Ortega',
      packages= find_packages(include= parametric_design_packages),
      )
