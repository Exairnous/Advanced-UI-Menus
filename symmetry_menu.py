from bpy.props import *
from .Utils.core import *

class MasterSymmetryMenu(bpy.types.Menu):
    bl_label = "Symmetry Options"
    bl_idname = "VIEW3D_MT_master_symmetry_menu"
    
    @classmethod
    def poll(self, context):
        if get_mode() in [sculpt, texture_paint]:
            return True
        else:
            return False
    
    def draw(self, context):
        menu = Menu(self)
        
        if get_mode() == texture_paint:
            menu.add_item().prop(context.tool_settings.image_paint, "use_symmetry_x", toggle=True)
            menu.add_item().prop(context.tool_settings.image_paint, "use_symmetry_y", toggle=True)
            menu.add_item().prop(context.tool_settings.image_paint, "use_symmetry_z", toggle=True)
        else:
        
            menu.add_item().menu(SymmetryMenu.bl_idname)
            menu.add_item().menu(SymmetryRadialMenu.bl_idname)
            menu.add_item().prop(context.tool_settings.sculpt, "use_symmetry_feather", toggle=True)
        
class SymmetryMenu(bpy.types.Menu):
    bl_label = "Symmetry"
    bl_idname = "VIEW3D_MT_symmetry_menu"

    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().label(text="Symmetry")
        menu.add_item().separator()

        menu.add_item().prop(context.tool_settings.sculpt, "use_symmetry_x", toggle=True)
        menu.add_item().prop(context.tool_settings.sculpt, "use_symmetry_y", toggle=True)
        menu.add_item().prop(context.tool_settings.sculpt, "use_symmetry_z", toggle=True)
        
class SymmetryRadialMenu(bpy.types.Menu):
    bl_label = "Radial"
    bl_idname = "VIEW3D_MT_symmetry_radial_menu"

    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().label(text="Radial")
        menu.add_item().separator()
        
        menu.add_item("column").prop(context.tool_settings.sculpt, "radial_symmetry", text="", slider=True)
    
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    
    modes = ['Sculpt', 'Image Paint']
    
    for mode in modes:
        km = wm.keyconfigs.addon.keymaps.new(name=mode)
        kmi = km.keymap_items.new('wm.call_menu', 'S', 'PRESS', alt=True)
        kmi.properties.name = "VIEW3D_MT_master_symmetry_menu"
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
