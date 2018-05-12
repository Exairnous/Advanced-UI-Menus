# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


""" Copyright 2011 GPL licence applies"""

bl_info = {
    "name": "Advanced UI Menus Development Version",
    "description": "Menus for advanced interaction with blender's UI",
    "author": "Ryan Inch",
    "version": ("dev"),
    "blender": (2, 79),
    "location": "View3D - Multiple menus in multiple modes.",
    "warning": '',  # used for warning icon and text in addons panel
    "wiki_url": "http://wiki.blender.org/index.php/Extensions:2.6/Py/Scripts/3D_interaction/Advanced_UI_Menus_Full",
    "category": "User Interface"}

import sys, os

from .Utils.core import *

from . import brush_menu
from . import brushes
from . import curve_menu
from . import custom_menu
from . import delete_menu
from . import dyntopo_menu
from . import extrude_menu
from . import layers_window
from . import manipulator_menu
from . import mode_menu
from . import pivot_menu
from . import proportional_menu
from . import selection_menu
from . import shade_menu
from . import snap_menu
from . import stroke_menu
from . import symmetry_menu
from . import texture_menu
from . import view_menu

addon_files = [ 
               brush_menu,
               curve_menu,
               custom_menu,
               delete_menu,
               dyntopo_menu,
               extrude_menu,
               layers_window,
               manipulator_menu,
               mode_menu,
               pivot_menu,
               proportional_menu,
               selection_menu,
               shade_menu,
               snap_menu,
               stroke_menu,
               symmetry_menu,
               texture_menu,
               view_menu
              ]

def register():
    # register all blender classes
    bpy.utils.register_module(__name__)
    
    # register all files
    for addon_file in addon_files:
        addon_file.register()
 
def unregister():
    # unregister all files
    for addon_file in addon_files:
        addon_file.unregister()
    
    # delete all the properties you have created
    del_props()
    
    # unregister all blender classes
    bpy.utils.unregister_module(__name__)
    
if __name__ == "__main__":
    register()
