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
    bl_idname = "view3d.snap_menu"

    def init(self):
        modes = [["Increment", 'INCREMENT', "SNAP_INCREMENT"], ["Vertex", 'VERTEX', "SNAP_VERTEX"],
                 ["Edge", 'EDGE', "SNAP_EDGE"], ["Face", 'FACE', "SNAP_FACE"],
                 ["Volume", 'VOLUME', "SNAP_VOLUME"]]

        return modes

    def draw(self, context):
        modes = self.init()
        menu = Menu(self)

        # add the menu items
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.snap_element",
                     icon=mode[2], disable=True)

        if bpy.context.tool_settings.snap_element != "INCREMENT":
            menu.add_item().separator()
            
            menu.add_item().menu(SnapTargetMenu.bl_idname)
            
            menu.add_item().separator()

        if bpy.context.tool_settings.snap_element not in ["INCREMENT", "VOLUME"]:
            menu.add_item().prop(bpy.context.tool_settings, "use_snap_align_rotation", toggle=True)

        if bpy.context.tool_settings.snap_element == "FACE":
            menu.add_item().prop(bpy.context.tool_settings, "use_snap_project", toggle=True)

        if bpy.context.tool_settings.snap_element == "VOLUME":
            menu.add_item().prop(bpy.context.tool_settings, "use_snap_peel_object", toggle=True)




class SnapTargetMenu(bpy.types.Menu):
    bl_label = "Snap Target"
    bl_idname = "view3d.snap_target_menu"

    def init(self):
        modes = [["Active", 'ACTIVE'], ["Median", 'MEDIAN'],
                 ["Center", 'CENTER'], ["Closest", 'CLOSEST']]

        return modes

    def draw(self, context):
        modes = self.init()
        menu = Menu(self)

        # add the menu items
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.snap_target", disable=True)


### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkey
    wm = bpy.context.window_manager
    #km = wm.keyconfigs.active.keymaps.new(name='3D View', space_type='VIEW_3D')
    km = wm.keyconfigs.active.keymaps['3D View']
    kmi = km.keymap_items.new('view3d.snap_menu_operator', 'TAB', 'PRESS', shift=True)
    addon_keymaps.append((km, kmi))


def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
