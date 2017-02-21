from .Utils.core import *

class ManipulatorMenuOperator(bpy.types.Operator):
    bl_label = "Transform Menu Operator"
    bl_idname = "view3d.manipulator_operator"

    @classmethod
    def poll(self, context):
        if get_mode() in [object_mode, edit, particle_edit, pose]:
            return True
        else:
            return False
    
    def modal(self, context, event):
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            if bpy.context.space_data.show_manipulator == True:
                bpy.ops.wm.call_menu(name=ManipulatorMenu.bl_idname)
            else:
                bpy.ops.wm.call_menu(name=ManipulatorMenu2.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle manipulator mode on/off
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if context.space_data.show_manipulator:
                context.space_data.show_manipulator = False
                
            else:
                context.space_data.show_manipulator = True
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
    
class ManipulatorMenu(bpy.types.Menu):
    bl_label = "Manipulator"
    bl_idname = "VIEW3D_MT_manipulator_menu"
    
    def draw(self, context):
        menu = Menu(self)
        
        menuprop(menu.add_item(), "Translate", {'TRANSLATE'},
        "space_data.transform_manipulators", 
        icon="MAN_TRANS", disable=True)
        
        menuprop(menu.add_item(), "Rotate", {'ROTATE'},
        "space_data.transform_manipulators", 
        icon="MAN_ROT", disable=True)
        
        menuprop(menu.add_item(), "Scale", {'SCALE'},
        "space_data.transform_manipulators", 
        icon="MAN_SCALE", disable=True)
        menu.add_item().prop_menu_enum(bpy.context.space_data, "transform_orientation")

class ManipulatorMenu2(bpy.types.Menu):
    bl_label = "Transform Orientation"
    bl_idname = "VIEW3D_MT_manipulator_menu_2"
    
    def draw(self, context):
        menu = Menu(self)
        menu.add_item().props_enum(bpy.context.space_data, "transform_orientation")

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('view3d.manipulator_operator', 'SPACE', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))


def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
