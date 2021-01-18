"""
TODO: Gaurav
Auto generated with bash.
Create a shared library with make and link to it for production.
"""

# hacked bindings
# lazy evaluation
# JIT

import cppyy
import os

try:
    current_dir = os.path.dirname(__file__)
except NameError:
    current_dir = os.getcwd()
source_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
include_dir = os.path.join(source_dir, 'include')
libs_dir = os.path.join(source_dir, 'libs')

# include paths
cppyy.add_include_path(include_dir)
cppyy.add_include_path(libs_dir)

# Headers used in the python examples. A makefile will replace this.
cppyy.include(os.path.join(include_dir, 'rovers/environment.hpp'))
cppyy.include(os.path.join(include_dir, 'rovers/core/rewards/ireward.hpp'))
cppyy.include(os.path.join(include_dir, 'rovers/core/rewards/difference.hpp'))
cppyy.include(os.path.join(include_dir, 'rovers/core/setup/init_corners.hpp'))
cppyy.include(os.path.join(include_dir, 'rovers/core/poi/iconstraint.hpp'))
cppyy.include(os.path.join(include_dir, 'rovers/core/sensors/isensor.hpp'))

# making c++ namespaces visible
rovers = cppyy.gbl.rovers
thyme = cppyy.gbl.thyme
std = cppyy.gbl.std
eigen = cppyy.gbl.Eigen

# cppyy.set_debug()
