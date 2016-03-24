from bpy.types import AddonPreferences
from .core import *
from Advanced_UI_Menus.__init__ import addon_files




def createAum_Settings():
    if bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings.items():
        return
    
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    
    # number equals index of menu in list addon_files from __init__.py
    settings = \
    [("3DView - Custom Menu", 4),
     ("3DView - Layers Window", 8),
     ("3DView - Manipulator Menu", 9),
     ("3DView - Mode Menu", 10),
     ("3DView - Pivot Menu", 11),
     ("3DView - Proportional Menu", 12),
     ("3DView - Shade Menu", 14),
     ("3DView - Snap Menu", 15),
     ("3DView - View Menu", 19),
     ("Edit - Delete Menu", 5),
     ("Edit - Extrude Menu", 7),
     ("Edit - Selection Menu", 13),
     ("Paint - Brush Options", 1),
     ("Paint - Brushes", 2),
     ("Paint - Curve Menu", 3),
     ("Paint - Dyntopo Menu", 6),
     ("Paint - Stroke Menu", 16),
     ("Paint - Symmetry Menu", 17),
     ("Paint - Texture Menu", 18)]
    
    for item in settings:
        aum_item = Aum_Settings.add()
        aum_item.name = item[0]
        aum_item.menu = item[1]
        
def update_keybinds(self, context):
    addon_files[self.menu].set_keybind(self.value)
    pass

class MenuItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(default="")
    menu = bpy.props.IntProperty()
    value = bpy.props.EnumProperty(
        items = [("off", "Off", "Sets Type To Off"), 
                 ("menu", "Menu", "Sets Type To Menu"),
                 ("pie", "Pie", "Sets Type To Pie")],
        default = "menu",
        name = "Type",
        update = update_keybinds)

class SCENE_UL_aum_menus(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(item.name)
        layout.prop(item, "value")

class AumPreferences(AddonPreferences):
    bl_idname = "Advanced_UI_Menus"
    
    settings = bpy.props.CollectionProperty(type=MenuItem)
    settings_index = bpy.props.IntProperty()
    
    def draw(self, context):
        ui = Menu(self)
        
        box = ui.add_item("box").column(align=False)
        box.template_list("SCENE_UL_aum_menus", "", self, "settings", self, "settings_index", rows=5, type='GRID', columns=1)
        
def register():
    createAum_Settings()

def unregister():
    pass
    