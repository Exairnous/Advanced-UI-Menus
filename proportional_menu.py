from .Utils.core import *


# adds a proportional mode menu
class ProportionalModeOperator(bpy.types.Operator):
    bl_label = "Proportional Mode Operator"
    bl_idname = "view3d.proportional_menu_operator"

    last_mode = ['DISABLED', 'ENABLED']

    def init(self, context):
        if context.space_data.type == 'DOPESHEET_EDITOR':
            if context.tool_settings.use_proportional_action == False:
                context.tool_settings.use_proportional_action = True
                
            else:
                context.tool_settings.use_proportional_action = False
            
            return {'FINISHED'}

        if context.space_data.type == 'GRAPH_EDITOR':
            if context.tool_settings.use_proportional_fcurve == False:
                context.tool_settings.use_proportional_fcurve = True
                
            else:
                context.tool_settings.use_proportional_fcurve = False
            
            return {'FINISHED'}
            
        if context.space_data.type == 'IMAGE_EDITOR':
            if context.space_data.show_maskedit:
                if context.tool_settings.use_proportional_edit_mask == False:
                    context.tool_settings.use_proportional_edit_mask = True
                
                else:
                    context.tool_settings.use_proportional_edit_mask = False
                
                return {'FINISHED'}
                
        if get_mode() == 'OBJECT':
            if context.tool_settings.use_proportional_edit_objects == False:
                context.tool_settings.use_proportional_edit_objects = True
                
            else:
                context.tool_settings.use_proportional_edit_objects = False
            
            return {'FINISHED'}

        # populate the list of last modes
        if context.tool_settings.proportional_edit not in self.last_mode:
            self.last_mode.append(context.tool_settings.proportional_edit)
            
        # keep the list to 2 items
        if len(self.last_mode) > 2:
            del self.last_mode[1]

    def modal(self, context, event):
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name=ProportionalEditingMenu.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle between off and your last used mode
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if context.tool_settings.proportional_edit != self.last_mode[0]:
                context.tool_settings.proportional_edit = self.last_mode[0]
                
            else:
                context.tool_settings.proportional_edit = self.last_mode[1]
            
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.init(context)
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class ProportionalEditingMenu(bpy.types.Menu):
    bl_label = "Proportional"
    bl_idname = "VIEW3D_MT_proportional_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in [edit, particle_edit, gpencil_edit]:
            return True
        else:
            return False

    def draw(self, context):
        menu = Menu(self)

        # add the items to the menu
        for mode in context.tool_settings.bl_rna.properties['proportional_edit'].enum_items:
            menuprop(menu.add_item(), mode.name, mode.identifier, "tool_settings.proportional_edit",
                     icon=mode.icon, disable=True)

class FalloffMenu(bpy.types.Menu):
    bl_label = "Falloff Menu"
    bl_idname = "VIEW3D_MT_falloff_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in [object_mode, edit, particle_edit, gpencil_edit]:
            return True
        else:
            return False

    def draw(self, context):
        menu = Menu(self)
        
        # add the items to the menu
        for mode in context.tool_settings.bl_rna.properties['proportional_edit_falloff'].enum_items:
            menuprop(menu.add_item(), mode.name, mode.identifier, "tool_settings.proportional_edit_falloff",
                     icon=mode.icon, disable=True)

        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ProportionalModeOperator,
    ProportionalEditingMenu,
    FalloffMenu
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global menu hotkeys
    wm = bpy.context.window_manager
    modes = {'Object Mode':'EMPTY',
             'Mesh':'EMPTY',
             'Curve':'EMPTY',
             'Armature':'EMPTY',
             'Metaball':'EMPTY',
             'Lattice':'EMPTY',
             'Particle':'EMPTY',
             'Object Non-modal':'EMPTY',
             'Graph Editor':'GRAPH_EDITOR',
             'Dopesheet':'DOPESHEET_EDITOR',
             'UV Editor':'EMPTY',
             'Grease Pencil Stroke Edit Mode':'EMPTY',
             'Mask Editing':'EMPTY'}
    
    for mode, space in modes.items():
        km = wm.keyconfigs.addon.keymaps.new(name=mode, space_type=space)
        kmi = km.keymap_items.new('view3d.proportional_menu_operator', 'O', 'PRESS')
        addon_keymaps.append((km, kmi))
    
        kmi = km.keymap_items.new('wm.call_menu', 'O', 'PRESS', shift=True)
        kmi.properties.name = 'VIEW3D_MT_falloff_menu'
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
