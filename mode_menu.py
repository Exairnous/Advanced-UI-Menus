from .Utils.core import *

class EditorModeOperator(bpy.types.Operator):
    bl_label = "Editor Mode Operator"
    bl_idname = "view3d.editor_mode_operator"

    last_mode = ['EDIT', 'OBJECT']

    def init(self):
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
        if not bpy.context.object:
            return {'FINISHED'}
        
        if bpy.context.object.type in ['MESH', 'ARMATURE']:
            self.init()
            self.start_time = time.time()
            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        
        elif bpy.context.object.type in ['CURVE', 'SURFACE', 'META', 'FONT', 'LATTICE']:
            bpy.ops.object.editmode_toggle()
            
            return {'FINISHED'}
        
        else:
            return {'FINISHED'}


class EditorModeMenu(bpy.types.Menu):
    bl_label = "Editor Menu"
    bl_idname = "VIEW3D_MT_mode_menu"

    def init(self):
        ob_type = bpy.context.object.type
        self.mode = get_mode()

        if ob_type == 'MESH':
            modes = [["Object", object_mode, "OBJECT_DATAMODE"],
                              ["Edit", edit, "EDITMODE_HLT"],
                              ["Sculpt", sculpt, "SCULPTMODE_HLT"],
                              ["Vertex Paint", vertex_paint, "VPAINT_HLT"],
                              ["Weight Paint", weight_paint, "WPAINT_HLT"],
                              ["Texture Paint", texture_paint, "TPAINT_HLT"],
                              ["Particle Edit", particle_edit, "PARTICLEMODE"]]
            
            if len(bpy.context.object.particle_systems.items()) == 0:
                del modes[6]
                
        elif ob_type == 'ARMATURE':
            modes = [["Object", object_mode, "OBJECT_DATAMODE"],
                             ["Edit", edit, "EDITMODE_HLT"],
                             ["Pose", pose, "POSE_HLT"]]
            
        return modes

    def draw(self, context):
        modes = self.init()
        menu = Menu(self)

        # add the menu items
        for mode in modes:
            prop = menu.add_item().operator("object.mode_set", mode[0], icon=mode[2])
            prop.mode = mode[1]
            
            # disable the rows that need it
            if self.mode == mode[1]:
                menu.current_item.enabled = False

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
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('view3d.editor_mode_operator', 'TAB', 'PRESS')
        addon_keymaps.append((km, kmi))
        
    elif value == "pie":
        ### Pie Code Goes Here ###
        pass

def register():
    # create the global hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("3DView - View Menu")
    set_keybind(setting.value)

def unregister():
    # remove keymaps when add-on is deactivated
    set_keybind("off")
