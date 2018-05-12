from bpy.props import *
from .Utils.core import *

class RCBrush(bpy.types.Menu):
    bl_label = "Brush Pie"
    bl_idname = "VIEW3D_MT_rc_brush"
        
    def draw(self, context):
        pie = self.layout.menu_pie()
        
        if len(bpy.types.Scene.CustomMenuBrushPie[1]['items']) == 1:
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][0][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            pie.separator()
            
            prop = pie.operator("wm.context_set_value", text='Blob', icon='BRUSH_BLOB')
            prop.value = 'bpy.data.brushes["Blob"]'
            prop.data_path = "tool_settings.sculpt.brush"
            
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            
        elif len(bpy.types.Scene.CustomMenuBrushPie[1]['items']) == 2:
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][0][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][1][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            prop = pie.operator("wm.context_set_value", text='Blob', icon='BRUSH_BLOB')
            prop.value = 'bpy.data.brushes["Blob"]'
            prop.data_path = "tool_settings.sculpt.brush"
            
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            
        elif len(bpy.types.Scene.CustomMenuBrushPie[1]['items']) == 3:
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][0][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][1][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            prop = pie.operator("wm.context_set_value", text='Blob', icon='BRUSH_BLOB')
            prop.value = 'bpy.data.brushes["Blob"]'
            prop.data_path = "tool_settings.sculpt.brush"
            
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][2][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            
        elif len(bpy.types.Scene.CustomMenuBrushPie[1]['items']) == 4:
            # left
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][0][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            # right
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][1][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            # bottom
            prop = pie.operator("wm.context_set_value", text='Blob', icon='BRUSH_BLOB')
            prop.value = 'bpy.data.brushes["Blob"]'
            prop.data_path = "tool_settings.sculpt.brush"
            
            # top
            pie.separator()
            
            # upper left
            pie.separator()
            
            # upper right
            pie.separator()
            
            # lower left
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][3][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
            # lower right
            name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][2][1]
            prop = pie.operator("wm.context_set_value", text=name)
            prop.value = 'bpy.data.brushes["{0}"]'.format(name)
            prop.data_path = "tool_settings.sculpt.brush"
            
        
#        for x in range(2):
#            print("first",x)
#            try:
#                name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][x][1]
#                prop = pie.operator("wm.context_set_value", text=name)
#                prop.value = 'bpy.data.brushes["{0}"]'.format(name)
#                prop.data_path = "tool_settings.sculpt.brush"
#            except:
#                pie.separator()
#        
#        prop = pie.operator("wm.context_set_value", text='Blob', icon='BRUSH_BLOB')
#        prop.value = 'bpy.data.brushes["Blob"]'
#        prop.data_path = "tool_settings.sculpt.brush"
#        
#        for x in range(2, 7):
#            print("second",x)
#            try:
#                name = bpy.types.Scene.CustomMenuBrushPie[1]['items'][x][1]
#                prop = pie.operator("wm.context_set_value", text=name)
#                prop.value = 'bpy.data.brushes["{0}"]'.format(name)
#                prop.data_path = "tool_settings.sculpt.brush"
#            except:
#                pie.separator()
            
                
            
            


### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    set_prop("EnumProperty", 
             "bpy.types.Scene.CustomMenuBrushPie",
             name = "Icon",
             items = [("0","Grab","0"),
                      ("0","Layer","0"),
                      ("0","Snake Hook","0"),
                      ("0","Mask","0")]
            )
    
    wm = bpy.context.window_manager
    modes = ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint', 'Particle']
    
    for mode in modes:
        km = wm.keyconfigs.addon.keymaps.new(name=mode)
        kmi = km.keymap_items.new('wm.call_menu_pie', 'RIGHTMOUSE', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_rc_brush"
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()