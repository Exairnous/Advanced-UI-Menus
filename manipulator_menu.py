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
                TransformOrientationMenu.hotkey = False
                bpy.ops.wm.call_menu(name=ManipulatorMenu.bl_idname)
            else:
                TransformOrientationMenu.hotkey = True
                bpy.ops.wm.call_menu(name=TransformOrientationMenu.bl_idname)
            
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
        
        menu.add_item().menu(TransformOrientationMenu.bl_idname)

class TransformOrientationMenu(bpy.types.Menu):
    bl_label = "Transform Orientation"
    bl_idname = "VIEW3D_MT_transf_orient_menu"
    
    hotkey = False
    
    def draw(self, context):
        menu = Menu(self)
        
        if not self.hotkey:
            menu.add_item().label(text="Transform Orientation")
            menu.add_item().separator()
        
        #menu.add_item().props_enum(bpy.context.space_data, "transform_orientation")
        for mode in context.space_data.bl_rna.properties['transform_orientation'].enum_items:
            menuprop(menu.add_item(), mode.name, mode.identifier, "space_data.transform_orientation",
            icon='RADIOBUT_OFF', disable=True, disable_icon='RADIOBUT_ON')

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ManipulatorMenuOperator,
    ManipulatorMenu,
    TransformOrientationMenu
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global menu hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('view3d.manipulator_operator', 'SPACE', 'PRESS', ctrl=True)
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
