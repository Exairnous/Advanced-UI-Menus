from ..Utils.core import *
from .common import *

def draw_particle_edit(menu, context):
    menu.add_item().menu("VIEW3D_MT_tools_menu", icon='TOOL_SETTINGS')
    menu.add_item().separator()
    menu.add_item().menu(BrushRadiusMenu.bl_idname)
    
    if context.tool_settings.particle_edit.tool != 'ADD':
        menu.add_item().menu(BrushStrengthMenu.bl_idname)

    else:
        menu.add_item().menu(ParticleCountMenu.bl_idname)
        menu.add_item().separator()
        menu.add_item().prop(context.tool_settings.particle_edit, 
                                "use_default_interpolate", toggle=True)

        menu.add_item().prop(context.tool_settings.particle_edit.brush, 
                                "steps", text=PIW+"Steps", slider=True)
        menu.add_item().prop(context.tool_settings.particle_edit, 
                                "default_key_count", text=PIW+"Keys", slider=True)

    if context.tool_settings.particle_edit.tool == 'LENGTH':
        menu.add_item().separator()
        menu.add_item().menu(ParticleLengthMenu.bl_idname)

    if context.tool_settings.particle_edit.tool == 'PUFF':
        menu.add_item().separator()
        menu.add_item().menu(ParticlePuffMenu.bl_idname)
        menu.add_item().prop(context.tool_settings.particle_edit.brush, 
                                "use_puff_volume", toggle=True)



class ParticleCountMenu(bpy.types.Menu):
    bl_label = "Count"
    bl_idname = "VIEW3D_MT_particle_count_menu"

    def init(self):
        settings = [["100", 100],
                    ["50", 50],
                    ["25", 25],
                    ["10", 10],
                    ["5", 5],
                    ["1", 1]]

        return settings

    def draw(self, context):
        settings = self.init()
        menu = Menu(self)

        # add the top slider
        menu.add_item().prop(context.tool_settings.particle_edit.brush, 
                             "count", slider=True)
        menu.add_item().separator()

        # add the rest of the menu items
        for i in range(len(settings)):
            menuprop(menu.add_item(), settings[i][0], settings[i][1],
                     "tool_settings.particle_edit.brush.count",
                     icon='RADIOBUT_OFF', disable=True,
                     disable_icon='RADIOBUT_ON')



class ParticleLengthMenu(bpy.types.Menu):
    bl_label = "Length Mode"
    bl_idname = "VIEW3D_MT_particle_length_menu"

    def draw(self, context):
        menu = Menu(self)
        path = "tool_settings.particle_edit.brush.length_mode"

        # add the menu items
        for item in context.tool_settings.particle_edit.brush.bl_rna.properties['length_mode'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, path,
                     icon='RADIOBUT_OFF',
                     disable=True, 
                     disable_icon='RADIOBUT_ON')
        
class ParticlePuffMenu(bpy.types.Menu):
    bl_label = "Puff Mode"
    bl_idname = "VIEW3D_MT_particle_puff_menu"

    def draw(self, context):
        menu = Menu(self)
        path = "tool_settings.particle_edit.brush.puff_mode"

        # add the menu items
        for item in context.tool_settings.particle_edit.brush.bl_rna.properties['puff_mode'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, path,
                     icon='RADIOBUT_OFF',
                     disable=True, 
                     disable_icon='RADIOBUT_ON')
