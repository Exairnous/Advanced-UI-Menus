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

class RemoveBrush(bpy.types.Operator):
    '''Permanently removes brush'''
    bl_label = "Delete Brush"
    bl_idname = "view3d.delete_brush"
    
    def execute(self, context):
        old_space_type = context.area.type
        context.area.type = 'VIEW_3D'
        space_type = context.space_data.type
        cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
        tool = cls._tool_active_from_context(context, space_type).idname.split('.')[1].upper().replace(' ', '_')
        
        context.area.type = old_space_type
        
        brush_list = []
        for brush in bpy.data.brushes:
            if get_mode() == sculpt and brush.use_paint_sculpt:
                if brush.sculpt_tool == tool:
                    brush_list.append(brush.name)
            
            if get_mode() == vertex_paint and brush.use_paint_vertex:
                if brush.vertex_tool == tool:
                    brush_list.append(brush.name)
            
            if get_mode() == weight_paint and brush.use_paint_weight:
                if brush.weight_tool == tool:
                    brush_list.append(brush.name)
            
            if get_mode() == texture_paint and brush.use_paint_image:
                if brush.image_tool == tool:
                    brush_list.append(brush.name)
        
        
        brush = get_active_brush(context)
        index = brush_list.index(brush.name)
        
        bpy.data.brushes.remove(brush)
        
        try:
            new_brush_name = brush_list[index-1] if index > 0 else brush_list[index+1]
        except:
            return {'FINISHED'}
        
        set_active_brush(context, bpy.data.brushes[new_brush_name])
                    
        
        return {'FINISHED'}


def brush_management(self, context):
    layout = self.layout
    
    layout.row().separator()
    
    row = layout.row()
    row.operator("brush.add")
    row.operator("view3d.delete_brush")
            

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
    ToolsMenu,
    RemoveBrush
    )


def register_preset_menus():
        cls = ToolSelectPanelHelper._tool_class_from_space_type('VIEW_3D')
        all_tools = dict([x for x in cls.tools_all()])
        
        for obj_mode, tool_mode in {'SCULPT':'SCULPT', 'VERTEX_PAINT':'PAINT_VERTEX', 'WEIGHT_PAINT':'PAINT_WEIGHT', 'TEXTURE_PAINT':'PAINT_TEXTURE'}.items():
            
            for tool in all_tools[tool_mode][0](bpy.context):
                add_preset_menu(obj_mode, tool.data_block)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # add brush management to toolshelf
    bpy.types.VIEW3D_PT_tools_brush.append(brush_management)
    
    register_preset_menus()
    
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
    
    # remove brush management from toolshelf
    bpy.types.VIEW3D_PT_tools_brush.remove(brush_management)
    
    for menu in preset_menus:
        bpy.utils.unregister_class(menu)
    
    preset_menus.clear()
    
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
