from ..Utils.core import *
from .common import *

preset_menus = []

def add_preset_menu(tool_mode, tool):
    id_name = 'VIEW3D_MT_tool_presets_menu_'+tool_mode+'_'+tool
    
    nc = type(  'PresetsMenu'+tool_mode+tool,
                (bpy.types.Menu, ),
                {'bl_idname': id_name,
                'bl_label': "Presets",
                'presets_tool':tool,
                'draw': draw_func
            })
    
    if nc not in preset_menus:
        preset_menus.append(nc)
        bpy.utils.register_class(nc)
        


def draw_func(self, context,):
    layout = self.layout
        
    if get_mode() == sculpt:
        for item in bpy.data.brushes:
            if item.use_paint_sculpt and item.sculpt_tool == self.presets_tool:
                menuprop(layout.row(), item.name, 
                            'bpy.data.brushes["%s"]' % item.name,
                            "tool_settings.sculpt.brush",
                            icon=get_brush_icon(item.sculpt_tool),
                            disable=True, custom_disable_exp=[item.name, context.tool_settings.sculpt.brush.name],
                            path=True)
                
    elif get_mode() == vertex_paint:
        for item in bpy.data.brushes:
            if item.use_paint_vertex and item.vertex_tool == self.presets_tool:
                menuprop(layout.row(), item.name, 
                            'bpy.data.brushes["%s"]' % item.name,
                            "tool_settings.vertex_paint.brush",
                            icon=get_brush_icon(item.vertex_tool),
                            disable=True, custom_disable_exp=[item.name, context.tool_settings.vertex_paint.brush.name],
                            path=True)
    
    elif get_mode() == weight_paint:
        for item in bpy.data.brushes:
            if item.use_paint_weight and item.weight_tool == self.presets_tool:
                menuprop(layout.row(), item.name, 
                            'bpy.data.brushes["%s"]' % item.name,
                            "tool_settings.weight_paint.brush",
                            icon=get_brush_icon(item.weight_tool),
                            disable=True, custom_disable_exp=[item.name, context.tool_settings.weight_paint.brush.name],
                            path=True)
                
    elif get_mode() == texture_paint:
        for item in bpy.data.brushes:
            if item.use_paint_image and item.image_tool == self.presets_tool:
                menuprop(layout.row(), item.name, 
                            'bpy.data.brushes["%s"]' % item.name,
                            "tool_settings.image_paint.brush",
                            icon=get_brush_icon(item.image_tool),
                            disable=True, custom_disable_exp=[item.name, context.tool_settings.image_paint.brush.name],
                            path=True)

def get_num_presets(presets_tool):
    num_presets = 0
    
    for item in bpy.data.brushes:
        if get_mode() == sculpt and item.use_paint_sculpt:
            if item.sculpt_tool == presets_tool:
                num_presets += 1
        
        if get_mode() == vertex_paint and item.use_paint_vertex:
            if item.vertex_tool == presets_tool:
                num_presets += 1
        
        if get_mode() == weight_paint and item.use_paint_weight:
            if item.weight_tool == presets_tool:
                num_presets += 1
        
        if get_mode() == texture_paint and item.use_paint_image:
            if item.image_tool == presets_tool:
                num_presets += 1
    
    return num_presets


def get_current_brush_name(context):
    brush_name = ""

    if get_mode() == sculpt:
        brush_name = context.tool_settings.sculpt.brush.name
    
    if get_mode() == vertex_paint:
        brush_name = context.tool_settings.vertex_paint.brush.name
        
    if get_mode() == weight_paint:
        brush_name = context.tool_settings.weight_paint.brush.name
        
    if get_mode() == texture_paint:
        brush_name = context.tool_settings.image_paint.brush.name
    
    return brush_name
       
class ToolsMenu(bpy.types.Menu):
    bl_label = "Tools"
    bl_idname = "VIEW3D_MT_tools_menu"
    
    def draw(self, context):
        space_type = context.space_data.type
        cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
        
        column = self.layout.column_flow(columns=2)
        
        index = 0
        for tool in cls._tools_flatten(cls.tools_from_context(context)):
            if not tool:
                continue
            
            if tool.idname.split(".")[0] != "builtin_brush":
                index += 1
                continue
            
            row = column.row()
            icon = cls._icon_value_from_icon_handle(tool.icon)
            row.operator("wm.tool_set_by_index", text="   "+tool.label, icon_value=icon).index = index
            if cls._tool_active_from_context(context, space_type).idname == tool.idname:
                row.enabled = False
            
            index += 1
        
        
        for tool in cls._tools_flatten(cls.tools_from_context(context)):
            if tool == None or tool.idname.split(".")[0] != "builtin_brush":
                continue
            row = column.row()
            
            if get_num_presets(tool.data_block) > 1:
                if cls._tool_active_from_context(context, space_type).idname == tool.idname:
                    row.menu("VIEW3D_MT_tool_presets_menu_"+get_mode()+'_'+tool.data_block, text=get_current_brush_name(context), icon='BRUSH_DATA')
                else:
                    row.menu("VIEW3D_MT_tool_presets_menu_"+get_mode()+'_'+tool.data_block, text=" ", icon='BRUSH_DATA')
            else:
                row.label()
