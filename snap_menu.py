from .Utils.core import *

# adds a shading mode menu
class SnapMenuOperator(bpy.types.Operator):
    bl_label = "Snap Menu Operator"
    bl_idname = "view3d.snap_menu_operator"

    @classmethod
    def poll(self, context):
        if get_mode() in [object_mode, edit, particle_edit]:
            return True
        else:
            return False

    def modal(self, context, event):
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name=SnapModeMenu.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle snap mode on/off
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if context.tool_settings.use_snap:
                context.tool_settings.use_snap = False
                
            else:
                context.tool_settings.use_snap = True
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class SnapModeMenu(bpy.types.Menu):
    bl_label = "Snap Element"
    bl_idname = "VIEW3D_MT_snap_menu"

    def draw(self, context):
        menu = Menu(self)
        snap_element = bpy.context.tool_settings.snap_element
        
        # menu for node editor
        if context.space_data.type == 'NODE_EDITOR':
            modes = [["Grid", 'GRID', "SNAP_GRID"],
                     ["Node X", 'NODE_X', "SNAP_EDGE"],
                     ["Node Y", 'NODE_Y', "SNAP_EDGE"],
                     ["Node X/Y", 'NODE_XY', "SNAP_EDGE"]]
                     
            # add the menu items
            for mode in modes:
                menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.snap_node_element",
                         icon=mode[2], disable=True)
                
            if snap_element != "INCREMENT":
                menu.add_item().separator()
                menu.add_item().menu(SnapTargetMenu.bl_idname)
        
        # menu for 3d view
        if context.space_data.type == 'VIEW_3D':
            modes = [["Increment", 'INCREMENT', "SNAP_INCREMENT"],
                     ["Vertex", 'VERTEX', "SNAP_VERTEX"],
                     ["Edge", 'EDGE', "SNAP_EDGE"],
                     ["Face", 'FACE', "SNAP_FACE"],
                     ["Volume", 'VOLUME', "SNAP_VOLUME"]]

            # add the menu items
            for mode in modes:
                menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.snap_element",
                         icon=mode[2], disable=True)

            if snap_element != "INCREMENT":
                menu.add_item().separator()
                menu.add_item().menu(SnapTargetMenu.bl_idname)
                
            menu.add_item().separator()

            if snap_element == "INCREMENT":
                menu.add_item().prop(bpy.context.tool_settings, "use_snap_grid_absolute", toggle=True)

            if snap_element not in ["INCREMENT", "VOLUME"]:
                menu.add_item().prop(bpy.context.tool_settings, "use_snap_align_rotation", toggle=True)

            if snap_element == "FACE":
                menu.add_item().prop(bpy.context.tool_settings, "use_snap_project", toggle=True)

            if snap_element == "VOLUME":
                menu.add_item().prop(bpy.context.tool_settings, "use_snap_peel_object", toggle=True)




class SnapTargetMenu(bpy.types.Menu):
    bl_label = "Snap Target"
    bl_idname = "VIEW3D_MT_snap_target_menu"

    def draw(self, context):
        menu = Menu(self)
        modes = [["Active", 'ACTIVE'],
                 ["Median", 'MEDIAN'],
                 ["Center", 'CENTER'],
                 ["Closest", 'CLOSEST']]

        # add the menu items
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.snap_target", disable=True)


### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkey
    wm = bpy.context.window_manager
    modes = {'Object Non-modal':'EMPTY', 'Node Editor':'NODE_EDITOR'}
    
    for mode, space in modes.items():
        km = wm.keyconfigs.addon.keymaps.new(name=mode, space_type=space)
        kmi = km.keymap_items.new('view3d.snap_menu_operator', 'TAB', 'PRESS', shift=True)
        addon_keymaps.append((km, kmi))


def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
