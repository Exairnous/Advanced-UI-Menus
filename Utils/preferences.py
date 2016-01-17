from bpy.types import AddonPreferences
from .core import *

#Global_Aum_Settings = None
#Global_Aum_Settings_Index = None
menu_type = ["[Off]", "[Menu]", "[Pie]"]

class MenuItem(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(default="")    
    activate = bpy.props.IntProperty(default=1)
    type = bpy.props.IntProperty(default=1)
    type = bpy.props.EnumProperty(
        items = [("off", "Off", "Sets Type To Off"), 
                 ("menu", "Menu", "Sets Type To Menu"),
                 ("pie", "Pie", "Sets Type To Pie")],
        name = "Type")

class SCENE_UL_aum_menus(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        menu = item
        # draw_item must handle the three layout types... Usually 'DEFAULT' and 'COMPACT' can share the same code.
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            # You should always start your row layout by a label (icon + text), this will also make the row easily
            # selectable in the list!
            # We use icon_value of label, as our given icon is an integer value, not an enum ID.
            layout.label(menu.name)
            #layout.prop(pie.activate)
            #row = layout.row()
            #row.props(pie.activate)
            
        # 'GRID' layout type should be as compact as possible (typically a single icon!).
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(menu.name)
            #layout.label("", icon="NODE")

class AumPreferences(AddonPreferences):
    bl_idname = "{}".format(__name__.split(".")[0])
    
    def draw(self, context):
        ui = Menu(self)
        self.initAumSettings()
        print("hi")

        Aum_Settings_Index = bpy.types.Scene.Aum_Settings_Index
        #split = layout.split()
        
        #global Global_Aum_Settings
        #global Global_Aum_Settings_Index
        
        #Global_Aum_Settings = self.Aum_Settings
        #Global_Aum_Settings_Index = self.Aum_Settings_Index
        
        box = ui.add_item("box").column(align=False)
        box.template_list("SCENE_UL_aum_menus", "", context.scene, "Aum_Settings", context.scene, "Aum_Settings_Index", rows=5, type='GRID', columns=1)
        ui.add_item().prop(context.scene, "Aum_Type", expand=True)
        #box.menu("view3d.type_menu")
        
    def initAumSettings(self):
        aum_set = bpy.types.Scene.Aum_Settings
        
        if not aum_set:
            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - View Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - Mode Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - Shade Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - Pivot Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3dView - Proportional Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Edit - Delete Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Edit - Selection Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Grey Brushes Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Red Brushes Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Tan Brushes Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Texture Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Strokes Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " Sculpt - Brush Control Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - Manipulator Menu"

            aum_item = aum_set.add()
            aum_item.name = menu_type[aum_item.type] + " 3DView - Particle Comb Menu"
        
class TypeMenu(bpy.types.Menu):
    bl_label = "Set Type To:"
    bl_idname = "view3d.type_menu"
    
    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().operator("mesh.dissolve_verts", text="Off")
        menu.add_item().operator("mesh.dissolve_verts", text="Menu")
        menu.add_item().operator("mesh.dissolve_verts", text="Pie")
        
        print(bpy.types.Scene.Aum_Settings[bpy.types.Scene.Aum_Settings_Index].name)
        
def register():
    #bpy.utils.register_class(AumPropertyGroup)
    #bpy.utils.register_class(AumSettings)
    
    bpy.types.Scene.Aum_Settings = bpy.props.CollectionProperty(type=MenuItem)
    bpy.types.Scene.Aum_Settings_Index = bpy.props.IntProperty()
    bpy.types.Scene.Aum_Type = bpy.props.EnumProperty(name="Aum_Type",items=(('0','Off','Disable Menu'), ('1','Menu','Use Traditional Menu'), ("2", "Pie", "Use Pie Menu")))
    
    #bpy.utils.register_module(__name__)
    
def unregister():
    pass
    #bpy.utils.unregister_module(__name__)
    