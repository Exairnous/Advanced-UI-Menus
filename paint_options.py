from bpy.app.handlers import persistent
from .Utils.core import *
from .Paint_Options.common import *
from .Paint_Options.brushes import *
from .Paint_Options.particle_edit import *
from .Paint_Options.sculpt import *
from .Paint_Options.texture_paint import *
from .Paint_Options.vertex_paint import *
from .Paint_Options.weight_paint import *

class PaintOptionsMenu(bpy.types.Menu):
    bl_label = "Paint Options"
    bl_idname = "VIEW3D_MT_paint_options"
    
    @classmethod
    def poll(self, context):
        #TODO support image editor
        if context.space_data.type == 'VIEW_3D' and get_mode() in [sculpt, vertex_paint, weight_paint, texture_paint, particle_edit]:
            return True
        else:
            return False
    
    def draw(self, context):
        menu = Menu(self)
        mode = get_mode()

        if mode == sculpt:
            draw_sculpt(menu, context)

        elif mode == vertex_paint:
            draw_vertex_paint(menu, context)
        
        elif mode == weight_paint:
            draw_weight_paint(menu, context)

        elif mode == texture_paint:
            draw_texture_paint(menu, context)

        elif mode == particle_edit:
            draw_particle_edit(menu, context)
        
        elif mode == grease_pencil:
            draw_grease_pencil(menu, context)
            

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    PaintOptionsMenu,
    BrushRadiusMenu,
    BrushStrengthMenu,
    DynDetailMenu,
    DetailMethodMenu,
    BrushModeMenu,
    BrushAutosmoothMenu,
    BrushWeightMenu,
    ParticleCountMenu,
    DirectionMenu,
    BlurMode,
    ParticleLengthMenu,
    ParticlePuffMenu,
    FlipColorsTex,
    FlipColorsVert,
    ColorPickerPopup,
    NewMaskImage,
    ToolsMenu
    )

@persistent
def register_preset_menus(dummy):
        
        cls = ToolSelectPanelHelper._tool_class_from_space_type('VIEW_3D')
        
        
        for obj_mode, tool_mode in {'SCULPT':'SCULPT', 'VERTEX_PAINT':'PAINT_VERTEX', 'WEIGHT_PAINT':'PAINT_WEIGHT', 'TEXTURE_PAINT':'PAINT_TEXTURE'}.items():
            for tool in cls._tools_flatten(cls.tools_from_context(bpy.context, tool_mode)):
                if not tool or tool.idname.split(".")[0] != "builtin_brush":
                    continue

                add_preset_menu(obj_mode, tool.data_block)
        
        bpy.app.handlers.depsgraph_update_pre.remove(register_preset_menus)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.app.handlers.depsgraph_update_pre.append(register_preset_menus)
    
    wm = bpy.context.window_manager
    modes = ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint', 'Particle']
    
    for mode in modes:
        km = wm.keyconfigs.addon.keymaps.new(name=mode)
        kmi = km.keymap_items.new('wm.call_menu', 'V', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_paint_options"
        addon_keymaps.append((km, kmi))

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    for menu in custom_menus:
        bpy.utils.unregister_class(menu)
    
    custom_menus.clear()
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
