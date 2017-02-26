from bpy.props import *
from .Utils.core import *

class DynTopoMenu(bpy.types.Menu):
    bl_label = "Dyntopo"
    bl_idname = "VIEW3D_MT_dyntopo"
    
    @classmethod
    def poll(self, context):
        if get_mode() == sculpt:
            return True
        else:
            return False
    
    def draw(self, context):
        menu = Menu(self)
        
        if context.object.use_dynamic_topology_sculpting:
            menu.add_item().operator("sculpt.dynamic_topology_toggle", "Disable Dynamic Topology")
            
            menu.add_item().separator()
            
            menu.add_item().operator("sculpt.optimize")
            if bpy.context.tool_settings.sculpt.detail_type_method == 'CONSTANT':
                menu.add_item().operator("sculpt.detail_flood_fill")
            
            menu.add_item().menu(SymmetrizeMenu.bl_idname)
            
        else:
            menu.add_item()
            menu.current_item.operator_context = 'INVOKE_DEFAULT'
            menu.current_item.operator("sculpt.dynamic_topology_toggle", "Enable Dynamic Topology")

            
class SymmetrizeMenu(bpy.types.Menu):
    bl_label = "Symmetrize"
    bl_idname = "VIEW3D_MT_symmetrize_menu"
        
    def draw(self, context):
        menu = Menu(self)
        path = "tool_settings.sculpt.symmetrize_direction"
        items = [["-X to +X", 'NEGATIVE_X'],
                 ["+X to -X", 'POSITIVE_X'],
                 ["-Y to +Y", 'NEGATIVE_Y'],
                 ["+Y to -Y", 'POSITIVE_Y'],
                 ["-Z to +Z", 'NEGATIVE_Z'],
                 ["+Z to -Z", 'POSITIVE_Z']]
        
        # add the the symmetrize operator to the menu
        menu.add_item().operator("sculpt.symmetrize")
        menu.add_item().separator()
        
        # add the rest of the menu items
        for item in items:
            menuprop(menu.add_item(), item[0], item[1], path, disable=True, 
                     icon='RADIOBUT_OFF', disable_icon='RADIOBUT_ON')
            
            
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
    kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=True)
    kmi.properties.name = 'VIEW3D_MT_dyntopo'
    addon_keymaps.append((km, kmi))

def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
