import bpy
import time
import sys
import os
import re

object_mode = 'OBJECT'
edit = 'EDIT'
sculpt = 'SCULPT'
vertex_paint = 'VERTEX_PAINT'
weight_paint = 'WEIGHT_PAINT'
texture_paint = 'TEXTURE_PAINT'
particle_edit = 'PARTICLE_EDIT'
pose = 'POSE'

a_props = []

class Menu():
    def __init__(self, menu):
        self.layout = menu.layout
        self.items = {}
        self.current_item = None

    def add_item(self, ui_type="row", parent=None, **kwargs):
        # set the parent layout
        if parent:
            layout = parent
        else:
            layout = self.layout
            
        # create and return a ui layout
        if ui_type == "row":
            self.current_item = self.items[len(self.items) + 1] = layout.row(**kwargs)
            
            return self.current_item

        elif ui_type == "column":
            self.current_item = self.items[len(self.items) + 1] = layout.column(**kwargs)
            
            return self.current_item

        elif ui_type == "column_flow":
            self.current_item = self.items[len(self.items) + 1] = layout.column_flow(**kwargs)
            
            return self.current_item

        elif ui_type == "box":
            self.current_item = self.items[len(self.items) + 1] = layout.box(**kwargs)
            
            return self.current_item

        elif ui_type == "split":
            self.current_item = self.items[len(self.items) + 1] = layout.split(**kwargs)
            
            return self.current_item
        
        else:
            print("Unknown Type")


def get_selected():
    # get the number of verts from the information string on the info header
    sel_verts_num = (e for e in bpy.context.scene.statistics().split(" | ")
                                  if e.startswith("Verts:")).__next__()[6:].split("/")
    
    # turn the number of verts from a string to an int
    sel_verts_num = int(sel_verts_num[0].replace(",",""))

    # get the number of edges from the information string on the info header
    sel_edges_num = (e for e in bpy.context.scene.statistics().split(" | ")
                                    if e.startswith("Edges:")).__next__()[6:].split("/")
    
    # turn the number of edges from a string to an int
    sel_edges_num = int(sel_edges_num[0].replace(",",""))

    # get the number of faces from the information string on the info header
    sel_faces_num = (e for e in bpy.context.scene.statistics().split(" | ")
                                  if e.startswith("Faces:")).__next__()[6:].split("/")
    
    # turn the number of faces from a string to an int
    sel_faces_num = int(sel_faces_num[0].replace(",",""))
    
    return sel_verts_num, sel_edges_num, sel_faces_num


def get_mode():
    return bpy.context.object.mode

def menuprop(item, name, value, data_path, icon='NONE',
                          disable=False, disable_icon=None,
                          custom_disable_exp=None,
                          method=None, path=False):
    
    # disable the ui
    if disable:
        disabled = False
        
        # used if you need a custom expression to disable the ui
        if custom_disable_exp:
            if custom_disable_exp[0] == custom_disable_exp[1]:
                item.enabled = False
                disabled = True
                
        # check if the ui should be disabled for numbers
        elif isinstance(eval("bpy.context.{}".format(data_path)), float):
            if round(eval("bpy.context.{}".format(data_path)), 2) == value:
                item.enabled = False
                disabled = True
        
        # check if the ui should be disabled for anything else
        else:
            if eval("bpy.context.{}".format(data_path)) == value:
                item.enabled = False
                disabled = True
        
        # change the icon to the disable_icon if the ui has been disabled
        if disable_icon and disabled:
                    icon = disable_icon
    
    # creates the menu item
    prop = item.operator("wm.context_set_value", text=name, icon=icon)

    # sets what the menu item changes
    if path:
        prop.value = value
        value = eval(value)
        
    elif type(value) == str:
        prop.value = "'{}'".format(value)
        
    else:
        prop.value = '{}'.format(value)

    # sets the path to what is changed
    prop.data_path = data_path

def set_prop(prop_type, path, **kwargs):
    kwstring = ""
    
    # turn **kwargs into a string that can be used with exec
    for k, v in kwargs.items():
        if type(v) is str:
            v = '"{}"'.format(v)
            
        kwstring += "{0}={1}, ".format(k, v)
    
    kwstring = kwstring[:-2]
    
    # create the property
    exec("{0} = bpy.props.{1}({2})".format(path, prop_type, kwstring))
    
    # add the path to a list of property paths
    a_props.append(path)
    
    return eval(path)

def del_props():
    for prop in a_props:
        exec("del {}".format(prop))
    
    a_props.clear()
    
    
            





#def get_view_mode():
#    view = bpy.context.space_data.region_3d.view_matrix
#
#    # check which view we are in and return a string telling us which it is
#    if "{0:.1f}".format(view[0][0]) == "1.0" and "{0:.1f}".format(view[1][2]) == "1.0" and "{0:.1f}".format(view[2][1]) == "-1.0":
#        return "FRONT"
#
#    elif "{0:.1f}".format(view[0][1]) == "1.0" and "{0:.1f}".format(view[1][2]) == "1.0" and "{0:.1f}".format(view[2][0]) == "1.0":
#        return "RIGHT"
#
#    elif "{0:.1f}".format(view[0][0]) == "1.0" and "{0:.1f}".format(view[1][1]) == "1.0" and "{0:.1f}".format(view[2][2]) == "1.0":
#        return "TOP"
#
#    elif "{0:.1f}".format(view[0][0]) == "-1.0" and "{0:.1f}".format(view[1][2]) == "1.0" and "{0:.1f}".format(view[2][1]) == "1.0":
#        return "BACK"
#
#    elif "{0:.1f}".format(view[0][1]) == "-1.0" and "{0:.1f}".format(view[1][2]) == "1.0" and "{0:.1f}".format(view[2][0]) == "-1.0":
#        return "LEFT"
#
#    elif "{0:.1f}".format(view[0][0]) == "1.0" and "{0:.1f}".format(view[1][1]) == "-1.0" and "{0:.1f}".format(view[2][2]) == "-1.0":
#        return "BOTTOM"
#
#    else:
#        return "N/A"
    
