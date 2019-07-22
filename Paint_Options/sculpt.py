from ..Utils.core import *
from .common import *

def draw_sculpt(menu, context):
        brush = context.tool_settings.sculpt.brush
        
        if not brush:
            menu.add_item().menu("VIEW3D_MT_tools_menu")
            return
            
        capabilities = brush.sculpt_capabilities
        
        menu.add_item().menu("VIEW3D_MT_tools_menu", icon='TOOL_SETTINGS')
        menu.add_item().separator()
        
        menu.add_item().menu(BrushRadiusMenu.bl_idname)
        menu.add_item().menu(BrushStrengthMenu.bl_idname)
        
        if context.object.use_dynamic_topology_sculpting and brush.sculpt_tool != 'MASK':
            menu.add_item().menu(DynDetailMenu.bl_idname)
        
        if capabilities.has_auto_smooth:
            menu.add_item().menu(BrushAutosmoothMenu.bl_idname)
        
        if capabilities.has_normal_weight:
            menu.add_item().prop(brush, "normal_weight", text=PIW+"Normal Weight", slider=True)
        
        if capabilities.has_pinch_factor:
            menu.add_item().prop(brush, "crease_pinch_factor", text=PIW+"Pinch", slider=True)
        
        if capabilities.has_rake_factor:
            menu.add_item().prop(brush, "rake_factor", text=PIW+"Rake", slider=True)
        
        if brush.sculpt_tool == 'MASK':
            menu.add_item().prop_menu_enum(brush, "mask_tool")
        
        if capabilities.has_plane_offset:
            menu.add_item().prop(brush, "plane_offset", text=PIW+"Plane Offset", slider=True)
            menu.add_item().prop(brush, "use_plane_trim", text="Trim")
            if brush.use_plane_trim:
                menu.add_item().prop(brush, "plane_trim", text=PIW+"Distance", slider=True)
        
        if capabilities.has_height:
            menu.add_item().prop(brush, "height", text=PIW+"Height", slider=True)
        
        menu.add_item().separator()
        
        menu.add_item().menu(BrushModeMenu.bl_idname, text="Sculpt Plane")
        
        # "not" required to make this work correctly. bug?
        if not capabilities.has_direction:
            menu.add_item().menu(DirectionMenu.bl_idname)
        
        if context.object.use_dynamic_topology_sculpting and brush.sculpt_tool != 'MASK':
            menu.add_item().menu(DetailMethodMenu.bl_idname)
        
        menu.add_item().prop(brush, "use_frontface", text="Front Faces Only", toggle=True)
        
        if capabilities.has_accumulate:
            menu.add_item().prop(brush, "use_accumulate")


class DynDetailMenu(bpy.types.Menu):
    bl_label = "Detail Size"
    bl_idname = "VIEW3D_MT_dyn_detail"

    def init(self):
        settings = [["40", 40],
                    ["30", 30],
                    ["20", 20],
                    ["10", 10],
                    ["5", 5],
                    ["1", 1]]
        
        if bpy.context.tool_settings.sculpt.detail_type_method == 'RELATIVE':
            datapath = "tool_settings.sculpt.detail_size"
            slider_setting = "detail_size"
            
        elif bpy.context.tool_settings.sculpt.detail_type_method == 'CONSTANT':
            datapath = "tool_settings.sculpt.constant_detail_resolution"
            slider_setting = "constant_detail_resolution"
        
        elif bpy.context.tool_settings.sculpt.detail_type_method == 'BRUSH':
            datapath = "tool_settings.sculpt.detail_percent"
            slider_setting = "detail_percent"

        return settings, datapath, slider_setting

    def draw(self, context):
        settings, datapath, slider_setting = self.init()
        menu = Menu(self)
        
        # add the top slider
        menu.add_item().prop(context.tool_settings.sculpt, slider_setting, slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1], datapath, 
                     icon='RADIOBUT_OFF', disable=True,
                     disable_icon='RADIOBUT_ON')


class DetailMethodMenu(bpy.types.Menu):
    bl_label = "Detail Method"
    bl_idname = "VIEW3D_MT_detail_method_menu"
        
    def draw(self, context):
        menu = Menu(self)
        refine_path = "tool_settings.sculpt.detail_refine_method"
        type_path = "tool_settings.sculpt.detail_type_method"
        
        menu.add_item().label(text="Refine")
        menu.add_item().separator()
        
        # add the refine menu items
        for item in context.tool_settings.sculpt.bl_rna.properties['detail_refine_method'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, refine_path, disable=True, 
                     icon='RADIOBUT_OFF', disable_icon='RADIOBUT_ON')
        
        menu.add_item().label(text="")
        
        menu.add_item().label(text="Type")
        menu.add_item().separator()
        
        # add the type menu items
        for item in context.tool_settings.sculpt.bl_rna.properties['detail_type_method'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, type_path, disable=True, 
                     icon='RADIOBUT_OFF', disable_icon='RADIOBUT_ON')


class BrushAutosmoothMenu(bpy.types.Menu):
    bl_label = "Autosmooth"
    bl_idname = "VIEW3D_MT_brush_autosmooth_menu"

    def init(self):
        settings = [["1.0", 1.0],
                    ["0.7", 0.7],
                    ["0.5", 0.5],
                    ["0.3", 0.3],
                    ["0.2", 0.2],
                    ["0.1", 0.1]]

        return settings

    def draw(self, context):
        settings = self.init()
        menu = Menu(self)

        # add the top slider
        menu.add_item().prop(context.tool_settings.sculpt.brush, 
                             "auto_smooth_factor", slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1],
                     "tool_settings.sculpt.brush.auto_smooth_factor",
                     icon='RADIOBUT_OFF', disable=True,
                     disable_icon='RADIOBUT_ON')
