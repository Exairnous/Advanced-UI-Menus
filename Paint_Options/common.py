from ..Utils.core import *
from bl_ui.space_toolsystem_common import ToolSelectPanelHelper

brush_icons = {
    "SCULPT_BLOB":'BRUSH_BLOB',
    "SCULPT_CLAY":'BRUSH_CLAY',
    "SCULPT_CLAY_STRIPS":'BRUSH_CLAY_STRIPS',
    "SCULPT_CREASE":'BRUSH_CREASE',
    "SCULPT_DRAW":'BRUSH_SCULPT_DRAW',
    "SCULPT_FILL":'BRUSH_FILL',
    "SCULPT_FLATTEN":'BRUSH_FLATTEN',
    "SCULPT_GRAB":'BRUSH_GRAB',
    "SCULPT_INFLATE":'BRUSH_INFLATE',
    "SCULPT_LAYER":'BRUSH_LAYER',
    "SCULPT_MASK":'BRUSH_MASK',
    "SCULPT_NUDGE":'BRUSH_NUDGE',
    "SCULPT_PINCH":'BRUSH_PINCH',
    "SCULPT_ROTATE":'BRUSH_ROTATE',
    "SCULPT_SCRAPE":'BRUSH_SCRAPE',
    "SCULPT_SIMPLIFY":'BRUSH_DATA',
    "SCULPT_SMOOTH":'BRUSH_SMOOTH',
    "SCULPT_SNAKE_HOOK":'BRUSH_SNAKE_HOOK',
    "SCULPT_THUMB":'BRUSH_THUMB',
    "VERT_AVERAGE":'BRUSH_BLUR',
    "VERT_BLUR":'BRUSH_BLUR',
    "VERT_DRAW":'BRUSH_MIX',
    "VERT_SMEAR":'BRUSH_BLUR',
    "TEX_CLONE":'BRUSH_CLONE',
    "TEX_DRAW":'BRUSH_TEXDRAW',
    "TEX_FILL":'BRUSH_TEXFILL',
    "TEX_MASK":'BRUSH_TEXMASK',
    "TEX_SMEAR":'BRUSH_SMEAR',
    "TEX_SOFTEN":'BRUSH_SOFTEN'
        }

def get_brush_icon(brush):
    if get_mode() == sculpt:
        brush = 'SCULPT_'+brush
    
    elif get_mode() in [vertex_paint, weight_paint]:
        brush = 'VERT_'+brush
    
    elif get_mode() == texture_paint:
        brush = 'TEX_'+brush
    
    return brush_icons[brush]

tool_modes = {
    'SCULPT':'SCULPT',
    'VERTEX_PAINT':'PAINT_VERTEX',
    'WEIGHT_PAINT':'PAINT_WEIGHT',
    'TEXTURE_PAINT':'PAINT_TEXTURE',
    'PARTICLE_EDIT':'PARTICLE'
        }

def get_active_tool_icon(context):
    space_type = context.space_data.type
    cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
    tool = cls._tool_get_active(context, space_type, tool_modes[get_mode()])[0]
    icon = cls._icon_value_from_icon_handle(tool.icon)
    
    return icon

def get_tool_icon(context, icon_str):
    space_type = context.space_data.type
    cls = ToolSelectPanelHelper._tool_class_from_space_type(space_type)
    icon = cls._icon_value_from_icon_handle(icon_str)
    
    return icon

class BrushRadiusMenu(bpy.types.Menu):
    bl_label = "Radius"
    bl_idname = "VIEW3D_MT_brush_radius_menu"

    def init(self, context):
        if get_mode() == particle_edit:
            settings = [["100", 100],
                        ["70", 70],
                        ["50", 50],
                        ["30", 30],
                        ["20", 20],
                        ["10", 10]]
                        
            datapath = "tool_settings.particle_edit.brush.size"
            proppath = context.tool_settings.particle_edit.brush

        else:
            settings = [["200", 200],
                        ["150", 150],
                        ["100", 100],
                        ["50", 50],
                        ["35", 35],
                        ["10", 10]]
                        
            datapath = "tool_settings.unified_paint_settings.size"
            proppath = context.tool_settings.unified_paint_settings

        return settings, datapath, proppath

    def draw(self, context):
        settings, datapath, proppath = self.init(context)
        menu = Menu(self)

        # add the top slider
        menu.add_item().prop(proppath, "size", slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1],
                     datapath, icon='RADIOBUT_OFF', disable=True, 
                     disable_icon='RADIOBUT_ON')
            

class BrushStrengthMenu(bpy.types.Menu):
    bl_label = "Strength"
    bl_idname = "VIEW3D_MT_brush_strength_menu"

    def init(self, context):
        settings = [["1.0", 1.0],
                    ["0.7", 0.7],
                    ["0.5", 0.5],
                    ["0.3", 0.3],
                    ["0.2", 0.2],
                    ["0.1", 0.1]]

        if get_mode() == sculpt:
            datapath = "tool_settings.sculpt.brush.strength"
            proppath = context.tool_settings.sculpt.brush

        elif get_mode() == vertex_paint:
            datapath = "tool_settings.vertex_paint.brush.strength"
            proppath = context.tool_settings.vertex_paint.brush

        elif get_mode() == weight_paint:
            datapath = "tool_settings.weight_paint.brush.strength"
            proppath = context.tool_settings.weight_paint.brush

        elif get_mode() == texture_paint:
            datapath = "tool_settings.image_paint.brush.strength"
            proppath = context.tool_settings.image_paint.brush

        else:
            datapath = "tool_settings.particle_edit.brush.strength"
            proppath = context.tool_settings.particle_edit.brush

        return settings, datapath, proppath

    def draw(self, context):
        settings, datapath, proppath = self.init(context)
        menu = Menu(self)

        # add the top slider
        menu.add_item().prop(proppath, "strength", slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1],
                     datapath, icon='RADIOBUT_OFF', disable=True, 
                     disable_icon='RADIOBUT_ON')


class BrushWeightMenu(bpy.types.Menu):
    bl_label = "Weight"
    bl_idname = "VIEW3D_MT_brush_weight_menu"

    def draw(self, context):
        if get_mode() == weight_paint:
            brush = context.tool_settings.unified_paint_settings
            brushstr = "tool_settings.unified_paint_settings.weight"
            name = "Weight"
        else:
            brush = context.tool_settings.image_paint.brush
            brushstr = "tool_settings.image_paint.brush.weight"
            name = "Mask Value"
        
        menu = Menu(self)
        settings = [["1.0", 1.0],
                    ["0.7", 0.7],
                    ["0.5", 0.5],
                    ["0.3", 0.3],
                    ["0.2", 0.2],
                    ["0.1", 0.1]]

        # add the top slider
        menu.add_item().prop(brush,
                             "weight", text=name, slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1],
                     brushstr,
                     icon='RADIOBUT_OFF', disable=True,
                     disable_icon='RADIOBUT_ON')


class BrushModeMenu(bpy.types.Menu):
    bl_label = "Mode"
    bl_idname = "VIEW3D_MT_brush_mode_menu"

    def init(self):
        if get_mode() == sculpt:
            enum = bpy.context.tool_settings.sculpt.brush.bl_rna.properties['sculpt_plane'].enum_items
            path = "tool_settings.sculpt.brush.sculpt_plane"

        elif get_mode() == texture_paint:
            enum = bpy.context.tool_settings.image_paint.brush.bl_rna.properties['blend'].enum_items
            path = "tool_settings.image_paint.brush.blend"

        elif get_mode() == vertex_paint:
            enum = bpy.context.tool_settings.vertex_paint.brush.bl_rna.properties['blend'].enum_items
            path = "tool_settings.vertex_paint.brush.blend"
        
        elif get_mode() == weight_paint:
            enum = bpy.context.tool_settings.weight_paint.brush.bl_rna.properties['blend'].enum_items
            path = "tool_settings.weight_paint.brush.blend"

        return enum, path

    def draw(self, context):
        enum, path = self.init()
        menu = Menu(self)
        
        if get_mode() == sculpt:
            menu.add_item().label(text="Sculpt Plane")
        else:
            menu.add_item().label(text="Blending Mode")
        menu.add_item().separator()
        
        if get_mode() in [vertex_paint, weight_paint, texture_paint]:
            column_flow = menu.add_item("column_flow", columns=2)
            
            # add all the brush modes to the menu
            for brush in enum:
                menuprop(menu.add_item(parent=column_flow), brush.name,
                         brush.identifier, path, icon='RADIOBUT_OFF',
                         disable=True, disable_icon='RADIOBUT_ON')
            
        else:
            # add all the brush modes to the menu
            for brush in enum:
                menuprop(menu.add_item(), brush.name,
                         brush.identifier, path, icon='RADIOBUT_OFF',
                         disable=True, disable_icon='RADIOBUT_ON')


class DirectionMenu(bpy.types.Menu):
    bl_label = "Direction"
    bl_idname = "VIEW3D_MT_direction_menu"
    
    def draw(self, context):
        menu = Menu(self)
        if get_mode() == sculpt:
            path = context.tool_settings.sculpt.brush
        else:
            path = context.tool_settings.image_paint.brush
        
        menu.add_item().label(text="Direction")
        menu.add_item().separator()
        
        # add the menu items
        menu.add_item().props_enum(path, "direction")



class ColorPickerPopup(bpy.types.Operator):
    bl_label = "Color"
    bl_idname = "view3d.color_picker_popup"
    bl_options = {'REGISTER'}
    
    def check(self, context):
        return True
    
    def draw(self, context):
        menu = Menu(self)
        
        if get_mode() == texture_paint:
            settings = context.tool_settings.image_paint
            brush = settings.brush
            
        else:
            settings = context.tool_settings.vertex_paint
            brush = settings.brush
        
        menu.add_item().template_color_picker(brush, "color", value_slider=True)
        menu.add_item().prop(brush, "color", text="")
        menu.current_item.prop(brush, "secondary_color", text="")
        if get_mode() == vertex_paint:
            menu.current_item.operator("view3d.flip_colors_vert", icon='FILE_REFRESH', text="")
        else:
            menu.current_item.operator("view3d.flip_colors_tex", icon='FILE_REFRESH', text="")
        
        if settings.palette:
            menu.add_item("column").template_palette(settings, "palette", color=True)
        
        menu.add_item().template_ID(settings, "palette", new="palette.new")
        
    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=180)
