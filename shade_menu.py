from .Utils.core import *

# adds a shading mode menu
class ShadeModeOperator(bpy.types.Operator):
    bl_label = "Shading Operator"
    bl_idname = "view3d.shading_menu_operator"

    last_mode = ['WIREFRAME']

    def init(self, context):
        # populate the list of last modes
        if context.space_data.viewport_shade not in self.last_mode:
            self.last_mode.append(context.space_data.viewport_shade)
        
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
            if context.space_data.viewport_shade != self.last_mode[0]:
                context.space_data.viewport_shade = self.last_mode[0]
                
            else:
                context.space_data.viewport_shade = self.last_mode[1]
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.init(context)
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}


class ShadeModeMenu(bpy.types.Menu):
    bl_label = "Shading Mode"
    bl_idname = "VIEW3D_MT_shade_menu"

    def init(self):
        renderer = bpy.context.scene.render.engine

        if renderer == 'BLENDER_RENDER':
            modes = [["Solid", 'SOLID', "SOLID"],
                              ["Wireframe", 'WIREFRAME', "WIRE"],
                              ["Textured", 'TEXTURED', "TEXTURE_SHADED"],
                              ["Material", 'MATERIAL', "MATERIAL_DATA"],
                              ["Rendered", 'RENDERED', "SMOOTH"],
                              ["Bounding Box", 'BOUNDBOX', "BBOX"]]
            
        elif renderer == 'CYCLES':
            modes = [["Solid", 'SOLID', "SOLID"],
                             ["Wireframe", 'WIREFRAME', "WIRE"],
                             ["Textured", 'TEXTURED', "TEXTURE_SHADED"],
                             ["Material", 'MATERIAL', "MATERIAL_DATA"],
                             ["Rendered", 'RENDERED', "SMOOTH"],
                             ["Bounding Box", 'BOUNDBOX', "BBOX"]]
            
        else:
            modes = [["Solid", 'SOLID', "SOLID"],
                             ["Wireframe", 'WIREFRAME', "WIRE"],
                             ["Textured", 'TEXTURED', "TEXTURE_SHADED"],
                             ["Material", 'MATERIAL', "MATERIAL_DATA"],
                             ["Bounding Box", 'BOUNDBOX', "BBOX"]]
            
        return modes

    def draw(self, context):
        modes = self.init()
        #menu = Menu(self)
        
        #add = self.layout
        #add_item = self.layout.row
        
        #add_item().label("haha You're a big idiot")
        #add_item("label(\"haha You're a big idiot\")")

        # add the items to the menu
        for mode in modes:
            menuprop(self.layout.row(), mode[0], mode[1], "space_data.viewport_shade",
                     icon=mode[2], disable=True)

        # add a shading options menu if object can be shaded smooth/flat
        if bpy.context.object.type in ['MESH', 'CURVE', 'SURFACE']:
            self.layout.row().separator()
            self.layout.row().menu(MeshShadeMenu.bl_idname)
            
        # add a display options menu if the mode is not edit
        if get_mode() != 'EDIT':
            self.layout.row().menu(DisplayOptionsMenu.bl_idname)
            
            
        # yay that works; now how do I solve operator_context for my custom menu?
        bisect = self.layout.row()
        bisect.operator_context = 'INVOKE_DEFAULT'
        bisect.operator("mesh.bisect")


class MeshShadeMenu(bpy.types.Menu):
    bl_label = "Mesh Shading Options"
    bl_idname = "VIEW3D_MT_mesh_shade"

    def draw(self, context):
        menu = Menu(self)
        
        if bpy.context.mode == 'EDIT_MESH':
            menu.add_item().operator("mesh.faces_shade_flat", "Shade Flat", icon="MESH_ICOSPHERE")
            menu.add_item().operator("mesh.faces_shade_smooth", "Shade Smooth", icon="MESH_UVSPHERE")
            
        else:
            menu.add_item().operator("object.shade_flat", "Shade Flat", icon="MESH_ICOSPHERE")
            menu.add_item().operator("object.shade_smooth", "Shade Smooth", icon="MESH_UVSPHERE")


class DisplayOptionsMenu(bpy.types.Menu):
    bl_label = "Display Options"
    bl_idname = "VIEW3D_MT_display_options"

    def draw(self, context):
        menu = Menu(self)

        menu.add_item().prop(context.object, 'show_name', toggle=True)
        menu.add_item().prop(context.object, 'show_axis', toggle=True)
        menu.add_item().prop(context.object, 'show_wire', toggle=True)
        menu.add_item().prop(context.object, 'show_x_ray', toggle=True)
        menu.add_item().prop(context.object, 'show_all_edges', toggle=True)
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    # create the global menu hotkey
    wm = bpy.context.window_manager
    #km = wm.keyconfigs.active.keymaps.new(name='3D View', space_type='VIEW_3D')
    km = wm.keyconfigs.active.keymaps['3D View']
    kmi = km.keymap_items.new('view3d.shading_menu_operator', 'Z', 'PRESS')
    addon_keymaps.append((km, kmi))

def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
