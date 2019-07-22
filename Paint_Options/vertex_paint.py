from ..Utils.core import *
from .common import *

def draw_vertex_paint(menu, context):
    menu.add_item().menu("VIEW3D_MT_tools_menu", text="  Tools", icon_value=get_active_tool_icon(context))
    menu.add_item().separator()
    
    if context.tool_settings.vertex_paint.brush.vertex_tool == 'DRAW':
        menu.add_item().operator(ColorPickerPopup.bl_idname, icon="COLOR")
    
    menu.add_item().menu(BrushRadiusMenu.bl_idname)
    menu.add_item().menu(BrushStrengthMenu.bl_idname)
    
    if context.tool_settings.vertex_paint.brush.vertex_tool == 'DRAW':
        menu.add_item().separator()
        menu.add_item().menu(BrushModeMenu.bl_idname, text="Blend")


class FlipColorsVert(bpy.types.Operator):
    bl_label = "Flip Colors"
    bl_idname = "view3d.flip_colors_vert"
    
    def execute(self, context):
        color = context.tool_settings.vertex_paint.brush.color
        secondary_color = context.tool_settings.vertex_paint.brush.secondary_color
        
        orig_prim = color.hsv
        orig_sec = secondary_color.hsv
        
        color.hsv = orig_sec
        secondary_color.hsv = orig_prim
        
        return {'FINISHED'}
