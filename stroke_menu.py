from bpy.props import *
from .Utils.core import *

airbrush = 'AIRBRUSH'
anchored = 'ANCHORED'
space = 'SPACE'
drag_dot = 'DRAG_DOT'
dots = 'DOTS'
line = 'LINE'
curve = 'CURVE'

class StrokeOptionsMenu(bpy.types.Menu):
    bl_label = "Stroke Options"
    bl_idname = "VIEW3D_MT_stroke_options"
    
    @classmethod
    def poll(self, context):
        if get_mode() in [sculpt, vertex_paint, weight_paint, texture_paint, particle_edit]:
            return True
        else:
            return False
    
    def init(self):
        if get_mode() == sculpt:
            brush = bpy.context.tool_settings.sculpt.brush
            
            if bpy.app.version > (2, 71):
                stroke_method = bpy.context.tool_settings.sculpt.brush.stroke_method
                
            else:
                stroke_method = bpy.context.tool_settings.sculpt.brush.sculpt_stroke_method

        elif get_mode() == texture_paint:
            brush = bpy.context.tool_settings.image_paint.brush
            stroke_method = bpy.context.tool_settings.image_paint.brush.stroke_method

        else:
            brush = bpy.context.tool_settings.vertex_paint.brush
            stroke_method = bpy.context.tool_settings.vertex_paint.brush.stroke_method

        return stroke_method, brush

    def draw(self, context):
        stroke_method, brush = self.init()
        menu = Menu(self)

        menu.add_item().menu(StrokeMethodMenu.bl_idname)

        if stroke_method == space:
            menu.add_item().prop(brush, "spacing", slider=True)

        elif stroke_method == airbrush:
            menu.add_item().prop(brush, "rate", slider=True)

        else:
            pass

        menu.add_item().prop(brush, "jitter", slider=True)
        
        menu.add_item().separator()
        
        menu.add_item().prop(brush, "use_smooth_stroke", toggle=True)

        if brush.use_smooth_stroke:
            menu.add_item().prop(brush, "smooth_stroke_radius", text="Radius", slider=True)
            menu.add_item().prop(brush, "smooth_stroke_factor", text="Factor", slider=True)
            
class StrokeMethodMenu(bpy.types.Menu):
    bl_label = "Stroke Method"
    bl_idname = "VIEW3D_MT_stroke_method"

    def init(self):
        if get_mode() == sculpt:
            path = "tool_settings.sculpt.brush.stroke_method"
            tools = [["Airbrush", airbrush], ["Anchored", anchored], ["Space", space],
                     ["Drag Dot", drag_dot], ["Dots", dots], ["Line", line], ["Curve", curve]]

        elif get_mode() == texture_paint:
            path = "tool_settings.image_paint.brush.stroke_method"
            tools = [["Airbrush", airbrush], ["Space", space], ["Dots", dots], ["Line", line], ["Curve", curve]]

        else:
            path = "tool_settings.vertex_paint.brush.stroke_method"
            tools = [["Airbrush", airbrush], ["Space", space], ["Dots", dots], ["Line", line], ["Curve", curve]]

        return path, tools

    def draw(self, context):
        path, tools = self.init()
        menu = Menu(self)
        
        menu.add_item().label(text="Stroke Method")
        menu.add_item().separator()

        # add the menu items
        for tool in tools:
            menuprop(menu.add_item(), tool[0], tool[1], path,
                               icon='RADIOBUT_OFF', disable=True,
                               disable_icon='RADIOBUT_ON')
    
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def set_keybind(value):
    wm = bpy.context.window_manager
    
    if value in ("off", "menu", "pie"):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    else:
        print("invalid value")
        return
        
    if value == "menu":
        modes = ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']
        
        for mode in modes:
            km = wm.keyconfigs.addon.keymaps.new(name=mode)
            kmi = km.keymap_items.new('wm.call_menu', 'E', 'PRESS')
            kmi.properties.name = "VIEW3D_MT_stroke_options"
            addon_keymaps.append((km, kmi))
        
    elif value == "pie":
        ### Pie Code Goes Here ###
        pass

def register():
    # create the global hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("Paint - Stroke Menu")
    set_keybind(setting.value)

def unregister():
    # remove keymaps when add-on is deactivated
    set_keybind("off")
