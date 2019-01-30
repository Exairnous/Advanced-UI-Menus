from .Utils.core import *

class ExtrudeMenuOperator(bpy.types.Operator):
    bl_label = "Extrude Menu Operator"
    bl_idname = "view3d.extrude_menu_operator"
            
    def modal(self, context, event):
        current_time = time.time()
                
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name="VIEW3D_MT_edit_mesh_extrude")
            
            return {'FINISHED'}
                
        # else extrude the selection
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            bpy.ops.view3d.edit_mesh_extrude_move_normal()
            
            return {'FINISHED'}
        
        else:
            return {'RUNNING_MODAL'}
        
    def execute(self, context):
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
                
        return {'RUNNING_MODAL'}
        

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    bpy.utils.register_class(ExtrudeMenuOperator)
    
    # create the global hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Mesh')
    kmi = km.keymap_items.new('view3d.extrude_menu_operator', 'E', 'PRESS')
    addon_keymaps.append((km, kmi))



def unregister():
    bpy.utils.unregister_class(ExtrudeMenuOperator)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()   
