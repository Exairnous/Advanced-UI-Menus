from .Utils.core import *

# adds a shading mode menu
class ShadeModeOperator(bpy.types.Operator):
    bl_label = "Shading Operator"
    bl_idname = "view3d.shading_menu_operator"

    last_mode = ['WIREFRAME', 'SOLID']

    def init(self, context):
        # populate the list of last modes
        if context.space_data.shading.type not in self.last_mode:
            self.last_mode.append(context.space_data.shading.type)
        
        # keep the list to 2 items
        if len(self.last_mode) > 2:
            del self.last_mode[1]

    def modal(self, context, event):
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.wm.call_menu(name=ShadeModeMenu.bl_idname)
            
            return {'FINISHED'}
        
        # else toggle between wireframe and your last used mode
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            if context.space_data.shading.type != self.last_mode[0]:
                context.space_data.shading.type = self.last_mode[0]
                
            else:
                context.space_data.shading.type = self.last_mode[1]
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.init(context)
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class ShadeModeMenu(bpy.types.Menu):
    bl_label = "Viewport Shading"
    bl_idname = "VIEW3D_MT_shade_menu"

    def init(self):
        renderer = bpy.context.scene.render.engine

        if renderer == 'BLENDER_EEVEE':
            modes = [["Solid", 'SOLID', "SHADING_SOLID"],
                     ["Wireframe", 'WIREFRAME', "SHADING_WIRE"],
                     ["LookDev", 'MATERIAL', "SHADING_TEXTURE"],
                     ["Rendered", 'RENDERED', "SHADING_RENDERED"]]
            
        elif renderer == 'BLENDER_WORKBENCH':
            modes = [["Solid", 'SOLID', "SHADING_SOLID"],
                     ["Wireframe", 'WIREFRAME', "SHADING_WIRE"],
                     ["Rendered", 'RENDERED', "SHADING_RENDERED"]]
            
        elif renderer == 'CYCLES':
            modes = [["Solid", 'SOLID', "SHADING_SOLID"],
                     ["Wireframe", 'WIREFRAME', "SHADING_WIRE"],
                     ["LookDev", 'MATERIAL', "SHADING_TEXTURE"],
                     ["Rendered", 'RENDERED', "SHADING_RENDERED"]]
            
        return modes

    def draw(self, context):
        modes = self.init()
        menu = Menu(self)

        # add the items to the menu
        for mode in modes:
            menuprop(menu.add_item(), mode[0], mode[1], "space_data.shading.type",
                     icon=mode[2], disable=True)
        
        menu.add_item().separator()
        
        # add a shading options menu if object can be shaded smooth/flat
        if context.object and context.object.type in ['MESH', 'CURVE', 'SURFACE']:
            if context.object.use_dynamic_topology_sculpting:
                menu.add_item().prop(context.tool_settings.sculpt, "use_smooth_shading", toggle=True)
            else:
                if not (context.object.type == 'SURFACE' and get_mode() == 'EDIT'):
                    menu.add_item().menu(MeshShadeMenu.bl_idname)

        if context.object:
            menu.add_item().menu(DisplayOptionsMenu.bl_idname)

class MeshShadeMenu(bpy.types.Menu):
    bl_label = "Object Shading"
    bl_idname = "VIEW3D_MT_mesh_shade"

    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().label(text="Object Shading")
        menu.add_item().separator()
        
        if context.mode == 'EDIT_MESH':
            menu.add_item().operator("mesh.faces_shade_flat", text="Shade Flat", icon="MESH_ICOSPHERE")
            menu.add_item().operator("mesh.faces_shade_smooth", text="Shade Smooth", icon="MESH_UVSPHERE")
        
        elif context.mode == 'EDIT_CURVE':
            menu.add_item().operator("curve.shade_flat", text="Shade Flat", icon="MESH_ICOSPHERE")
            menu.add_item().operator("curve.shade_smooth", text="Shade Smooth", icon="MESH_UVSPHERE")
        
        else:
            menu.add_item().operator("object.shade_flat", text="Shade Flat", icon="MESH_ICOSPHERE")
            menu.add_item().operator("object.shade_smooth", text="Shade Smooth", icon="MESH_UVSPHERE")


class DisplayOptionsMenu(bpy.types.Menu):
    bl_label = "Display Options"
    bl_idname = "VIEW3D_MT_display_options"

    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().label(text="Display Options")
        menu.add_item().separator()

        menu.add_item().prop(context.object, 'show_name', toggle=True)
        menu.add_item().prop(context.object, 'show_axis', toggle=True)
        
        print(context.object.type)
        if context.object.type in ['MESH', 'CURVE', 'SURFACE', 'META', 'FONT']:
            menu.add_item().prop(context.object, 'show_wire', toggle=True)
        
        menu.add_item().prop(context.object, 'show_in_front', toggle=True)
        
        if context.object.type == 'MESH':
            menu.add_item().prop(context.object, 'show_all_edges', toggle=True)
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ShadeModeOperator,
    ShadeModeMenu,
    MeshShadeMenu,
    DisplayOptionsMenu
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global menu hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('view3d.shading_menu_operator', 'Z', 'PRESS')
    addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
