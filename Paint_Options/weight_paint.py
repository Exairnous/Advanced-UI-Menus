from ..Utils.core import *
from .common import *

def draw_weight_paint(menu, context):
    menu.add_item().menu("VIEW3D_MT_tools_menu", text="  Tools", icon_value=get_active_tool_icon(context))
    menu.add_item().separator()
    if get_mode() == weight_paint:
        menu.add_item().menu(BrushWeightMenu.bl_idname)
    menu.add_item().menu(BrushRadiusMenu.bl_idname)
    menu.add_item().menu(BrushStrengthMenu.bl_idname)
    menu.add_item().separator()
    menu.add_item().menu(BrushModeMenu.bl_idname, text="Blend")
    menu.add_item().operator("object.vertex_group_smooth")
