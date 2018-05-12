from .Utils.core import *


class SelectionModeMenu(bpy.types.Menu):
    bl_label = "Select Mode"
    bl_idname = "VIEW3D_MT_selection_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in [edit, particle_edit] and bpy.context.object.type == 'MESH':
            return True
        else:
            return False
    
    def init(self):
        if get_mode() == edit:
            modes = [["Vertex Select", (True, False, False), 'VERTEXSEL'],
                     ["Edge Select", (False, True, False), 'EDGESEL'],
                     ["Face Select", (False, False, True), 'FACESEL'],
                     ["Vertex & Edge Select", (True, True, False), 'EDIT'],
                     ["Vertex & Face Select", (True, False, True), 'EDITMODE_HLT'],
                     ["Edge & Face Select", (False, True, True), 'SPACE2'],
                     ["Vertex, Edge & Face Select", (True, True, True), 'OBJECT_DATAMODE']]
            
            datapath = "tool_settings.mesh_select_mode[0:3]"
            
        else:
            modes = [["Path", 'PATH', 'PARTICLE_PATH'],
                     ["Point", 'POINT', 'PARTICLE_POINT'],
                     ["Tip", 'TIP', 'PARTICLE_TIP']]
            
            datapath = "tool_settings.particle_edit.select_mode"
            
        return modes, datapath
    
    def draw(self, context):
        modes, datapath = self.init()
        menu = Menu(self)
        

        for num, mode in enumerate(modes):
            # add the items to the menu
            menuprop(menu.add_item(), mode[0], mode[1], datapath,
                     icon=mode[2], disable=True)
            
            # add a separator after each section
            if num in [2, 6, 7]:
                menu.add_item().separator()

        menu.add_item().prop(context.space_data, "use_occlude_geometry", icon='ORTHO', toggle=True)
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def set_keybind(value):
    wm = bpy.context.window_manager
    modes = ['Mesh', 'Particle']
    
    if value in ("off", "menu", "pie"):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    else:
        print("invalid value")
        return
        
    if value == "menu":
        modes = ['Mesh', 'Particle']

        for mode in modes:
            km = wm.keyconfigs.addon.keymaps.new(name=mode)
            kmi = km.keymap_items.new('wm.call_menu', 'TAB', 'PRESS', ctrl=True)
            kmi.properties.name = 'VIEW3D_MT_selection_menu'
            addon_keymaps.append((km, kmi))
        
    elif value == "pie":
        ### Pie Code Goes Here ###
        pass

def register():
    # create the global hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("Edit - Selection Menu")
    set_keybind(setting.value)

def unregister():
    # remove keymaps when add-on is deactivated
    set_keybind("off")
