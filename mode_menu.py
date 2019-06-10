from .Utils.core import *

class EditorModeOperator(bpy.types.Operator):
    bl_label = "Editor Mode Operator"
    bl_idname = "view3d.editor_mode_operator"
    bl_options = {'REGISTER', 'UNDO'}

    last_mode = ['EDIT', 'OBJECT']

    def init(self, obj):
        # set edit mode string based on obj type
        self.last_mode[0] = 'EDIT_GPENCIL' if obj.type == 'GPENCIL' else 'EDIT'
        
        # populate the list of last modes
        if get_mode() not in self.last_mode:
            self.last_mode.append(get_mode())
            
        # keep the list to 2 items
        if len(self.last_mode) > 2:
            del self.last_mode[1]

    def modal(self, context, event):
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name=EditorModeMenu.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle between edit mode and your last used mode
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if get_mode() != self.last_mode[0]:
                bpy.ops.object.mode_set(mode=self.last_mode[0])
                
            else:
                bpy.ops.object.mode_set(mode=self.last_mode[1])
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        obj = context.object
        
        if not obj:
            return {'FINISHED'}
        
        # make sure the object is in a visible layer
        if obj.visible_get() == False:
            return {'FINISHED'}
        
        if obj.type in ["EMPTY", "SPEAKER", "CAMERA", "LAMP"]:
            return {'FINISHED'}
        
        self.init(obj)
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
            
        return {'RUNNING_MODAL'}


class EditorModeMenu(bpy.types.Menu):
    bl_label = "Editor Menu"
    bl_idname = "VIEW3D_MT_mode_menu"

    def init(self, context):
        obj = context.object
        self.mode = get_mode()

        if obj.type == 'MESH':
            modes = [["Object", object_mode, "OBJECT_DATAMODE"],
                     ["Edit", edit, "EDITMODE_HLT"],
                     ["Sculpt", sculpt, "SCULPTMODE_HLT"],
                     ["Vertex Paint", vertex_paint, "VPAINT_HLT"],
                     ["Weight Paint", weight_paint, "WPAINT_HLT"],
                     ["Texture Paint", texture_paint, "TPAINT_HLT"]]

            if len(obj.particle_systems.items()) > 0:
                modes.append(["Particle Edit", particle_edit, "PARTICLEMODE"])
                
        elif obj.type == 'ARMATURE':
            modes = [["Object", object_mode, "OBJECT_DATAMODE"],
                     ["Edit", edit, "EDITMODE_HLT"],
                     ["Pose", pose, "POSE_HLT"]]
        
        elif obj.type == 'GPENCIL':
            modes = [["Object", 'OBJECT', "OBJECT_DATAMODE"],
                     ["Edit", 'EDIT_GPENCIL', "EDITMODE_HLT"],
                     ["Sculpt", 'SCULPT_GPENCIL', "SCULPTMODE_HLT"],
                     ["Draw", 'PAINT_GPENCIL', "GREASEPENCIL"],
                     ["Weight Paint", 'WEIGHT_GPENCIL', "WPAINT_HLT"]]
        
        else:
            modes = [["Object", object_mode, "OBJECT_DATAMODE"],
                     ["Edit", edit, "EDITMODE_HLT"]]
        
            # remove edit mode if object does not have it
            if obj.type in ["EMPTY", "SPEAKER", "CAMERA", "LAMP"]: del modes[1]
            
        return modes

    def draw(self, context):
        modes = self.init(context)
        menu = Menu(self)

        # add the menu items
        for mode in modes:
            prop = menu.add_item(name=mode[0]).operator("object.mode_set", text=mode[0], icon=mode[2])
            prop.mode = mode[1]
            
            # disable the rows that need it
            if self.mode == mode[1]:
                menu.current_item.enabled = False
        

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    EditorModeOperator,
    EditorModeMenu
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('view3d.editor_mode_operator', 'TAB', 'PRESS')
    addon_keymaps.append((km, kmi))
    
    km = wm.keyconfigs.addon.keymaps.new(name='Grease Pencil Stroke Edit Mode')
    kmi = km.keymap_items.new('view3d.editor_mode_operator', 'TAB', 'PRESS')
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
