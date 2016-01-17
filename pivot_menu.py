from .Utils.core import *

# adds a pivot point menu 
class PivotPointMenu(bpy.types.Menu):
    bl_label = "Pivot Point"
    bl_idname = "view3d.pivot_point"
    
    def draw(self, context):
        menu = Menu(self)
        pivot_modes = [["Median Point", "'MEDIAN_POINT'", "ROTATECENTER"], 
                                     ["3D Cursor", "'CURSOR'", "CURSOR"],
                                     ["Individual Origins", "'INDIVIDUAL_ORIGINS'", "ROTATECOLLECTION"],
                                     ["Active Element", "'ACTIVE_ELEMENT'", "ROTACTIVE"],
                                     ["Bounding Box Center", "'BOUNDING_BOX_CENTER'", "ROTATE"]]
            
            # create menu
        for mode in pivot_modes:
            prop = menu.add_item().operator("wm.context_set_value", mode[0], icon=mode[2])
            prop.value = mode[1]
            prop.data_path = "space_data.pivot_point"
            if bpy.context.space_data.pivot_point == mode[1][1:-1]:
                menu.current_item.enabled = False

        # if your in object or pose mode add the manip center points
        # menu
        if get_mode() in [object, pose]:
            menu.add_item().separator()
            if not bpy.context.space_data.use_pivot_point_align:
                prop = menu.add_item().operator("wm.context_set_value",
                                                "Enable Manipulate center points", icon="ALIGN")
                
                prop.value = "True"
                prop.data_path = "space_data.use_pivot_point_align"
                
            else:
                prop = menu.add_item().operator("wm.context_set_value",
                                                "Disable Manipulate center points", icon="ALIGN")
                
                prop.value = "False"
                prop.data_path = "space_data.use_pivot_point_align"
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkey
    wm = bpy.context.window_manager
    #km = wm.keyconfigs.active.keymaps.new(name='3D View', space_type='VIEW_3D')
    km = wm.keyconfigs.active.keymaps['3D View']
    kmi = km.keymap_items.new('wm.call_menu', 'PERIOD', 'PRESS')
    kmi.properties.name = 'view3d.pivot_point'
    addon_keymaps.append((km, kmi))


def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
