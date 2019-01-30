from .Utils.core import *

# adds a pivot point menu 
class PivotPointMenu(bpy.types.Menu):
    bl_label = "Pivot Point"
    bl_idname = "VIEW3D_MT_pivot_point"
    
    def draw(self, context):
        menu = Menu(self)
        # get set pivot modes based on spacetype
        if context.space_data.type == 'VIEW_3D':
            pivot_modes = [["Median Point", "'MEDIAN_POINT'", "ROTATECENTER"], 
                           ["3D Cursor", "'CURSOR'", "CURSOR"],
                           ["Individual Origins", "'INDIVIDUAL_ORIGINS'", "ROTATECOLLECTION"],
                           ["Active Element", "'ACTIVE_ELEMENT'", "ROTACTIVE"],
                           ["Bounding Box Center", "'BOUNDING_BOX_CENTER'", "ROTATE"]]
                           
        if context.space_data.type == 'GRAPH_EDITOR':
            pivot_modes = [["2D Cursor", "'CURSOR'", "CURSOR"],
                           ["Individual Centers", "'INDIVIDUAL_ORIGINS'", "ROTATECOLLECTION"],
                           ["Bounding Box Center", "'BOUNDING_BOX_CENTER'", "ROTATE"]]
        
        if context.space_data.type == 'IMAGE_EDITOR':
            pivot_modes = [["Median Point", "'MEDIAN'", "ROTATECENTER"], 
                           ["2D Cursor", "'CURSOR'", "CURSOR"],
                           ["Individual Origins", "'INDIVIDUAL_ORIGINS'", "ROTATECOLLECTION"],
                           ["Bounding Box Center", "'CENTER'", "ROTATE"]]
            
            # create menu
        for mode in pivot_modes:
            prop = menu.add_item().operator("wm.context_set_value", mode[0], icon=mode[2])
            prop.value = mode[1]
            prop.data_path = "space_data.pivot_point"
            if bpy.context.space_data.pivot_point == mode[1][1:-1]:
                menu.current_item.enabled = False

        # if your in 3D View and in object or pose mode add the manip center points
        # menu
        if context.space_data.type == 'VIEW_3D':
            if get_mode() in [object_mode, pose]:
                menu.add_item().separator()
                if not bpy.context.space_data.use_pivot_point_align:
                    prop = menu.add_item().operator("wm.context_set_value",
                                                    "Enable Manipulate center points",
                                                    icon="ALIGN")
                
                    prop.value = "True"
                    prop.data_path = "space_data.use_pivot_point_align"
                
                else:
                    prop = menu.add_item().operator("wm.context_set_value",
                                                    "Disable Manipulate center points",
                                                    icon="ALIGN")
                
                    prop.value = "False"
                    prop.data_path = "space_data.use_pivot_point_align"
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    bpy.utils.register_class(PivotPointMenu)
    
    # create the global menu hotkey
    wm = bpy.context.window_manager
    modes = {'Object Non-modal':'EMPTY', 'Graph Editor':'GRAPH_EDITOR', 'Image':'IMAGE_EDITOR'}
    
    for mode, space in modes.items():
        km = wm.keyconfigs.addon.keymaps.new(name=mode, space_type=space)
        kmi = km.keymap_items.new('wm.call_menu', 'PERIOD', 'PRESS')
        kmi.properties.name = 'VIEW3D_MT_pivot_point'
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(PivotPointMenu)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
