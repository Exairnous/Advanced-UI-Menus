from .Utils.core import *

def get_prop_edit(context):
    if not context.tool_settings.use_proportional_edit:
        return 'DISABLED'
    
    if context.tool_settings.use_proportional_connected:
        return 'CONNECTED'
    
    elif context.tool_settings.use_proportional_projected:
        return 'PROJECTED'
    
    else:
        return 'ENABLED'

def toggle_prop_other(context):
    editor = context.space_data.type
    ts = context.tool_settings
    
    if editor == 'DOPESHEET_EDITOR':
        ts.use_proportional_action = not ts.use_proportional_action
        return

    if editor == 'GRAPH_EDITOR':
        ts.use_proportional_fcurve = not ts.use_proportional_fcurve
        return
            
    if editor == 'IMAGE_EDITOR':
        if context.space_data.show_maskedit:
            ts.use_proportional_edit_mask = not ts.use_proportional_edit_mask  
        
        else:
            ts.use_proportional_edit = not ts.use_proportional_edit
        
        return
                
    if get_mode() == 'OBJECT':
        ts.use_proportional_edit_objects = not ts.use_proportional_edit_objects
        return

class SetPropEditOperator(bpy.types.Operator):
    '''Set Proportional Edit Mode'''
    bl_label = "Set Proportional Edit Operator"
    bl_idname = "view3d.set_prop_edit_operator"
    
    mode: bpy.props.StringProperty()
    
    def execute(self, context):
        if self.mode == 'ENABLED':
            context.tool_settings.use_proportional_edit = True
            context.tool_settings.use_proportional_connected = False
            context.tool_settings.use_proportional_projected = False
        
        elif self.mode == 'CONNECTED':
            context.tool_settings.use_proportional_edit = True
            context.tool_settings.use_proportional_connected = True
            context.tool_settings.use_proportional_projected = False
        
        elif self.mode == 'PROJECTED':
            context.tool_settings.use_proportional_edit = True
            context.tool_settings.use_proportional_connected = False
            context.tool_settings.use_proportional_projected = True
        
        elif self.mode == 'DISABLED':
            context.tool_settings.use_proportional_edit = False
        
        else:
            print("Proportional Edit Mode Not Supported")
        
        return {'FINISHED'}

# adds a proportional mode menu
class ProportionalModeOperator(bpy.types.Operator):
    bl_label = "Proportional Mode Operator"
    bl_idname = "view3d.proportional_menu_operator"

    last_mode = ['DISABLED', 'ENABLED']

    def update_last_mode(self, context):
        # populate the list of last modes
        prop_edit = get_prop_edit(context)
        if prop_edit not in self.last_mode:
            self.last_mode.append(prop_edit)
            
        # keep the list to 2 items
        if len(self.last_mode) > 2:
            del self.last_mode[1]

    def modal(self, context, event):
        current_time = time.time()
        
        if event.value == 'RELEASE' and not context.object:
            ts = context.tool_settings
            ts.use_proportional_edit_objects = not ts.use_proportional_edit_objects
            
            return {'FINISHED'}
        
        if event.value == 'RELEASE' and not (get_mode() in ['EDIT', 'PARTICLE_EDIT', 'EDIT_GPENCIL'] and context.space_data.type == 'VIEW_3D'):
            toggle_prop_other(context)
            return {'FINISHED'}
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name=ProportionalEditingMenu.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle between off and your last used mode
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if get_prop_edit(context) != self.last_mode[0]:
                bpy.ops.view3d.set_prop_edit_operator(mode=self.last_mode[0])
                
            else:
                bpy.ops.view3d.set_prop_edit_operator(mode=self.last_mode[1])
            
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        if context.object and get_mode() in ['EDIT', 'PARTICLE_EDIT', 'EDIT_GPENCIL']:
            self.update_last_mode(context)
            
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class ProportionalEditingMenu(bpy.types.Menu):
    bl_label = "Proportional Edit Mode"
    bl_idname = "VIEW3D_MT_proportional_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in [edit, particle_edit, gpencil_edit]:
            return True
        else:
            return False

    def draw(self, context):
        menu = Menu(self)
        
        # get current prop mode
        prop_edit = get_prop_edit(context)
        
        
        # add the items to the menu
        menu.add_item().operator("view3d.set_prop_edit_operator", text="Disabled", icon='PROP_OFF').mode = 'DISABLED'
        if prop_edit == 'DISABLED':
            menu.current_item.enabled = False
        
        menu.add_item().operator("view3d.set_prop_edit_operator", text="Enabled (Standard)", icon='PROP_ON').mode = 'ENABLED'
        if prop_edit == 'ENABLED':
            menu.current_item.enabled = False
        
        menu.add_item().operator("view3d.set_prop_edit_operator", text="Connected", icon='PROP_CON').mode = 'CONNECTED'
        if prop_edit == 'CONNECTED':
            menu.current_item.enabled = False
        
        menu.add_item().operator("view3d.set_prop_edit_operator", text="Projected (2D)", icon='PROP_PROJECTED').mode = 'PROJECTED'
        if prop_edit == 'PROJECTED':
            menu.current_item.enabled = False
        

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
    SetPropEditOperator,
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
