import bpy
import time
import sys
import os

object_mode = 'OBJECT'
edit = 'EDIT'
sculpt = 'SCULPT'
vertex_paint = 'VERTEX_PAINT'
weight_paint = 'WEIGHT_PAINT'
texture_paint = 'TEXTURE_PAINT'
particle_edit = 'PARTICLE_EDIT'
pose = 'POSE'
gpencil_edit = 'EDIT_GPENCIL'

PIW = '       '

a_props = []

class Menu():
    def __init__(self, menu):
        self.layout = menu.layout
        self.items = {}
        self.current_item = None

    def add_item(self, ui_type="row", parent=None, name=None, **kwargs):
        # set the parent layout
        if parent:
            layout = parent
        else:
            layout = self.layout
            
        # set unique identifier for new items
        if not name:
            name = len(self.items) + 1
            
        # create and return a ui layout
        if ui_type == "row":
            self.current_item = self.items[name] = layout.row(**kwargs)
            
            return self.current_item

        elif ui_type == "column":
            self.current_item = self.items[name] = layout.column(**kwargs)
            
            return self.current_item

        elif ui_type == "column_flow":
            self.current_item = self.items[name] = layout.column_flow(**kwargs)
            
            return self.current_item

        elif ui_type == "box":
            self.current_item = self.items[name] = layout.box(**kwargs)
            
            return self.current_item

        elif ui_type == "split":
            self.current_item = self.items[name] = layout.split(**kwargs)
            
            return self.current_item
        
        else:
            print("Unknown Type")


def get_selected():
    # get a list of statistics from the info bar
    stats = bpy.context.scene.statistics(bpy.context.view_layer).split(" | ")
    
    # get number of selected verts
    sel_verts = int(stats[1].split(":")[1].split("/")[0])
    
    # get number of selected edges
    sel_edges = int(stats[2].split(":")[1].split("/")[0])
    
    # get number of selected faces
    sel_faces = int(stats[3].split(":")[1].split("/")[0])
    
    return sel_verts, sel_edges, sel_faces


def get_mode():
        return bpy.context.object.mode

def menuprop(item, name, value, data_path,
             icon='NONE', disable=False, disable_icon=None,
             custom_disable_exp=None, method=None, path=False):
    
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

# used for global blender properties
def set_prop(prop_type, path, **kwargs):
    kwstring = ""
    
    # turn **kwargs into a string that can be used with exec
    for k, v in kwargs.items():
        if type(v) is str:
            v = '"{}"'.format(v)
        
        if callable(v):
            exec("from {0} import {1}".format(v.__module__, v.__name__))
            v = v.__name__
            
        kwstring += "{0}={1}, ".format(k, v)
    
    kwstring = kwstring[:-2]
    
    # create the property
    exec("{0} = bpy.props.{1}({2})".format(path, prop_type, kwstring))
    
    # add the path to a list of property paths
    a_props.append(path)
    
    return eval(path)

# used for removing properties created with set_prop
def del_props():
    for prop in a_props:
        exec("del {}".format(prop))
    
    a_props.clear()
    
class SendReport(bpy.types.Operator):
    bl_label = "Send Report"
    bl_idname = "view3d.send_report"
    
    message: bpy.props.StringProperty()
    
    def draw(self, context):
        layout = self.layout
        
        first = True
        string = ""
        
        for num, char in enumerate(self.message):
            if char == "\n":
                if first:
                    layout.row().label(text=string, icon='ERROR')
                    first = False
                else:
                    layout.row().label(text=string, icon='BLANK1')
                    
                string = ""
                continue
            
            string = string + char
        
        if first:
            layout.row().label(text=string, icon='ERROR')
        else:
            layout.row().label(text=string, icon='BLANK1')
    
    def invoke(self, context, event):
        wm = context.window_manager
        
        max_len = 0
        length = 0
        
        for char in self.message:
            if char == "\n":
                if length > max_len:
                    max_len = length
                length = 0
            else:
                length += 1
            
        
        return wm.invoke_popup(self, width=(max_len*6), height=200)
    
    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}
    
def send_report(message):
    bpy.ops.view3d.send_report('INVOKE_DEFAULT', message=message)
    def report():
        bpy.ops.view3d.send_report(message=message)

    #bpy.app.timers.register(report, first_interval=1)




class StickyKey():
    def __init__():
        self.start_time = time.time()
    
    def result(event):
        current_time = time.time()

        if event.value == 'RELEASE':
            if current_time < start_time + 0.3:
                return 'short'
            else:
                return 'long'
    
        return None



class StickyKeyOperatorExample(bpy.types.Operator):
    bl_label = "Sticky Key Operator Example"
    bl_idname = "view3d.sticky_key_operator_example"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        sticky = self.stickykey.result()
        
        # short press action
        if sticky == 'short':
            bpy.ops.wm.call_menu(name=EditorModeMenu.bl_idname)
        
        # long press action
        elif sticky == 'long':
            if get_mode() != self.last_mode[0]:
                bpy.ops.object.mode_set(mode=self.last_mode[0])
                
            else:
                bpy.ops.object.mode_set(mode=self.last_mode[1])
        
        # key is still held down
        else:
            return {'RUNNING_MODAL'}
        
        
        return {'FINISHED'}

    def execute(self, context):
        self.stickykey = StickyKey()
        context.window_manager.modal_handler_add(self)
            
        return {'RUNNING_MODAL'}

classes = (
    SendReport,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
