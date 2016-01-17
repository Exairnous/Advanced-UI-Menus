from .Utils.core import *


# adds a proportional mode menu
class ProportionalModeOperator(bpy.types.Operator):
    bl_label = "Proportional Mode Operator"
    bl_idname = "view3d.proportional_menu_operator"

    last_mode = ['DISABLED', 'ENABLED']

    def init(self, context):
        self.start_time = 0

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
    bl_idname = "view3d.proportional_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in ['EDIT', 'PARTICLE_EDIT']:
            return True
        else:
            return False

    def init(self):
        modes = [["Disabled", 'DISABLED', "PROP_OFF"],
                         ["Enabled", 'ENABLED', "PROP_ON"],
                         ["Projected(2D)", 'PROJECTED', "PROP_ON"],
                         ["Connected", 'CONNECTED', "PROP_CON"]]
        
        datapath = "tool_settings.proportional_edit"
        
        return modes, datapath

    def draw(self, context):
        modes, datapath = self.init()
        menu = Menu(self)

        # add the items to the menu
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], datapath,
                     icon=mode[2], disable=True)

class FalloffMenu(bpy.types.Menu):
    bl_label = "Falloff Menu"
    bl_idname = "view3d.falloff_menu"

    @classmethod
    def poll(self, context):
        if get_mode() in [object_mode, edit, particle_edit]:
            return True
        else:
            return False

    def draw(self, context):
        menu = Menu(self)

        modes = [["Smooth", 'SMOOTH', "SMOOTHCURVE"],
                         ["Sphere", 'SPHERE', "SPHERECURVE"],
                         ["Root", 'ROOT', "ROOTCURVE"],
                         ["Sharp", 'SHARP', "SHARPCURVE"],
                         ["Linear", 'LINEAR', "LINCURVE"],
                         ["Constant", 'CONSTANT', "NOCURVE"],
                         ["Random", 'RANDOM', "RNDCURVE"]]
        
        # add the items to the menu
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], "tool_settings.proportional_edit_falloff",
                     icon=mode[2], disable=True)

        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkeys
    wm = bpy.context.window_manager
    #km = wm.keyconfigs.active.keymaps.new(name='3D View', space_type='VIEW_3D')
    km = wm.keyconfigs.active.keymaps['3D View']
    kmi = km.keymap_items.new('view3d.proportional_menu_operator', 'O', 'PRESS')
    addon_keymaps.append((km, kmi))
    
    kmi = km.keymap_items.new('wm.call_menu', 'O', 'PRESS', shift=True)
    kmi.properties.name = 'view3d.falloff_menu'
    addon_keymaps.append((km, kmi))


def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
