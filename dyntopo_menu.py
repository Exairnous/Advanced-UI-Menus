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
        
        # add the the symmetrize operator to the menu
        menu.add_item().operator("sculpt.symmetrize")
        menu.add_item().separator()
        
        # add the rest of the menu items
        for item in context.tool_settings.sculpt.bl_rna.properties['symmetrize_direction'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, path, disable=True, 
                     icon='RADIOBUT_OFF', disable_icon='RADIOBUT_ON')
            
            
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def set_keybind(value):
    wm = bpy.context.window_manager
    
    if value in ("off", "menu", "pie"):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    else:
        print("invalid value")
        return
        
    if value == "menu":   
        km = wm.keyconfigs.addon.keymaps.new(name='Sculpt')
        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS', ctrl=True)
        kmi.properties.name = 'VIEW3D_MT_dyntopo'
        addon_keymaps.append((km, kmi))
        
    elif value == "pie":
        ### Pie Code Goes Here ###
        pass
    
def register():
    # create the global menu hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("Paint - Dyntopo Menu")
    set_keybind(setting.value)

def unregister():
    # remove keymaps when add-on is deactivated
    set_keybind("off")
