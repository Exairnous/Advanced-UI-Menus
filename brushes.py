from bpy.props import *
from .Utils.core import *

class BrushesMenu(bpy.types.Menu):
    bl_label = "Brush"
    bl_idname = "view3d.brushes_menu"

    def init(self):
        if get_mode() == sculpt:
            datapath = "tool_settings.sculpt.brush"
            icon = { "BLOB":'BRUSH_BLOB',  
                           "CLAY":'BRUSH_CLAY', 
                           "CLAY_STRIPS":'BRUSH_CLAY_STRIPS', 
                           "CREASE":'BRUSH_CREASE',
                           "DRAW":'BRUSH_SCULPT_DRAW',
                           "FILL":'BRUSH_FILL', 
                           "FLATTEN":'BRUSH_FLATTEN', 
                           "GRAB":'BRUSH_GRAB', 
                           "INFLATE":'BRUSH_INFLATE', 
                           "LAYER":'BRUSH_LAYER', 
                           "MASK":'BRUSH_MASK',  
                           "NUDGE":'BRUSH_NUDGE', 
                           "PINCH":'BRUSH_PINCH',
                           "ROTATE":'BRUSH_ROTATE',
                           "SCRAPE":'BRUSH_SCRAPE',
                           "SIMPLIFY":'BRUSH_SUBTRACT',
                           "SMOOTH":'BRUSH_SMOOTH', 
                           "SNAKE_HOOK":'BRUSH_SNAKE_HOOK',
                           "THUMB":'BRUSH_THUMB'}

        elif get_mode() == vertex_paint:
            datapath = "tool_settings.vertex_paint.brush"
            icon = {"ADD":'BRUSH_ADD',
                          "BLUR":'BRUSH_BLUR',
                          "DARKEN":'BRUSH_DARKEN',
                          "LIGHTEN":'BRUSH_LIGHTEN',
                          "MIX":'BRUSH_MIX',
                          "MUL":'BRUSH_MULTIPLY',
                          "SUB":'BRUSH_SUBTRACT'}

        elif get_mode() == weight_paint:
            datapath = "tool_settings.weight_paint.brush"
            icon = {"ADD":'BRUSH_ADD',
                          "BLUR":'BRUSH_BLUR',
                          "DARKEN":'BRUSH_DARKEN',
                          "LIGHTEN":'BRUSH_LIGHTEN',
                          "MIX":'BRUSH_MIX',
                          "MUL":'BRUSH_MULTIPLY',
                          "SUB":'BRUSH_SUBTRACT'}

        elif get_mode() == texture_paint:
            datapath = "tool_settings.image_paint.brush"
            icon = {"CLONE":'BRUSH_CLONE',
                          "DRAW":'BRUSH_TEXDRAW',
                          "FILL":'BRUSH_TEXFILL',
                          "MASK":'BRUSH_TEXMASK',
                          "SMEAR":'BRUSH_SMEAR',
                          "SOFTEN":'BRUSH_SOFTEN'}

        elif get_mode() == particle_edit:
            datapath = "tool_settings.particle_edit.tool"
            icon = None

        else:
            datapath = ""

        return datapath, icon

    def draw(self, context):
        datapath, icon = self.init()
        menu = Menu(self)
        
        current_brush = eval("bpy.context.{}".format(datapath))
        
        # get the current brush's name
        if current_brush and get_mode() != particle_edit:
            current_brush = current_brush.name

        if get_mode() == particle_edit:
            particle_tools = [["None", 'NONE'],
                                       ["Comb", 'COMB'],
                                       ["Smooth", 'SMOOTH'],
                                       ["Add", 'ADD'],
                                       ["Length", 'LENGTH'],
                                       ["Puff", 'PUFF'],
                                       ["Cut", 'CUT'],
                                       ["Weight", 'WEIGHT']]
            
            # if you are in particle edit mode add the menu items for particle mode
            for tool in particle_tools:
                menuprop(menu.add_item(), tool[0], tool[1], datapath,
                                   icon='RADIOBUT_OFF', disable=True,
                                   disable_icon='RADIOBUT_ON')

        else:
            # iterate over all the brushes
            for item in bpy.data.brushes:
                if get_mode() == sculpt and item.use_paint_sculpt:
                    # if you are in sculpt mode and the brush is a sculpt brush add the brush to the menu
                    brush = menu.add_item().operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=icon[item.sculpt_tool])
                    brush.name = item.name
                    brush.icon = icon[item.sculpt_tool]
                    brush.datapath = datapath
                    #menuprop(menu.add_item(), item.name,
                    #        'bpy.data.brushes["%s"]' % item.name,
                    #        datapath,  icon=icon[item.sculpt_tool], 
                    #        disable=True, custom_disable_exp=[item.name, current_brush],
                    #        path=True)

                if get_mode() == vertex_paint and item.use_paint_vertex:
                    # if you are in vertex paint mode and the brush is a vertex paint brush add the brush to the menu
                    brush = menu.add_item().operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=icon[item.vertex_tool])
                    brush.name = item.name
                    brush.icon = icon[item.vertex_tool]
                    brush.datapath = datapath
                    #menuprop(menu.add_item(), item.name, 
                            #'bpy.data.brushes["%s"]' % item.name,
                            #datapath, icon=icon[item.vertex_tool],
                            #disable=True, custom_disable_exp=[item.name, current_brush],
                            #path=True)

                if get_mode() == weight_paint and item.use_paint_weight:
                    # if you are in weight paint mode and the brush is a weight paint brush add the brush to the menu
                    brush = menu.add_item().operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=icon[item.vertex_tool])
                    brush.name = item.name
                    brush.icon = icon[item.vertex_tool]
                    brush.datapath = datapath
                    #menuprop(menu.add_item(), item.name,
                            #'bpy.data.brushes["%s"]' % item.name,
                            #datapath, icon=icon[item.vertex_tool],
                            #disable=True, custom_disable_exp=[item.name, current_brush],
                            #path=True)

                if get_mode() == texture_paint and item.use_paint_image:
                    # if you are in texture paint mode and the brush is a texture paint brush add the brush to the menu
                    brush = menu.add_item().operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=icon[item.image_tool])
                    brush.name = item.name
                    brush.icon = icon[item.image_tool]
                    brush.datapath = datapath
                    #menuprop(menu.add_item(), item.name,
                            #'bpy.data.brushes["%s"]' % item.name,
                            #datapath, icon=icon[item.image_tool],
                            #disable=True, custom_disable_exp=[item.name, current_brush],
                            #path=True)
                        
class BrushFavMenu(bpy.types.Menu):
    bl_label = "Favourites"
    bl_idname = "VIEW3D_MT_brush_favs"
    
    def draw(self, context):
        menu = Menu(self)
        
        cbm = get_mode().lower()
        if cbm == "texture_paint":
            cbm = "image_paint"
            
        current_brush = eval("bpy.context.tool_settings.{}.brush.name".format(cbm))
        
        for item in bpy.context.scene.BrushFav:
            if get_mode() == sculpt and bpy.data.brushes[item.name].use_paint_sculpt:
                menu.add_item()
                menu.current_item.operator_context = 'INVOKE_DEFAULT'
                brush = menu.current_item.operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=item.icon)
                brush.name = item.name
                brush.icon = item.icon
                brush.datapath = item.datapath
                
            elif get_mode() == vertex_paint and bpy.data.brushes[item.name].use_paint_vertex:
                menu.add_item()
                menu.current_item.operator_context = 'INVOKE_DEFAULT'
                brush = menu.current_item.operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=item.icon)
                brush.name = item.name
                brush.icon = item.icon
                brush.datapath = item.datapath
                
            elif get_mode() == weight_paint and bpy.data.brushes[item.name].use_paint_weight:
                menu.add_item()
                menu.current_item.operator_context = 'INVOKE_DEFAULT'
                brush = menu.current_item.operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=item.icon)
                brush.name = item.name
                brush.icon = item.icon
                brush.datapath = item.datapath
                
            elif get_mode() == texture_paint and bpy.data.brushes[item.name].use_paint_image:
                menu.add_item()
                menu.current_item.operator_context = 'INVOKE_DEFAULT'
                brush = menu.current_item.operator("view3d.set_brush_op", text=item.name if item.name != current_brush else "@  {}  @".format(item.name), icon=item.icon)
                brush.name = item.name
                brush.icon = item.icon
                brush.datapath = item.datapath
        
        if menu.items:
            menu.add_item().separator()
        menu.add_item().menu("view3d.brushes_menu", "All Brushes")
        
class SetBrushOp(bpy.types.Operator):
    '''Select brush. Shift-Click to favourite, Ctrl-Click to unfavourite'''
    bl_idname = "view3d.set_brush_op"
    bl_label = "Set Brush Operator"
    
    name = bpy.props.StringProperty(name="Brush Name")
    icon = bpy.props.StringProperty(name="Brush Icon")
    datapath = bpy.props.StringProperty(name="Brush Datapath")
    
    def invoke(self, context, event):
        if event.shift:
            # prevent duplicates
            for item in bpy.context.scene.BrushFav:
                if item.name == self.name:
                    return {'CANCELLED'}
            # add brush to brush favourites
            fav = bpy.context.scene.BrushFav.add()
            fav.name = self.name
            fav.icon = self.icon
            fav.datapath = self.datapath
            return {'FINISHED'}
        elif event.ctrl:
            # remove brush from brush favourites
            for i, item in enumerate(bpy.context.scene.BrushFav):
                if item.name == self.name:
                    bpy.context.scene.BrushFav.remove(i)
                    return {'FINISHED'}
            return {'CANCELLED'}
        elif event.type == 'LEFTMOUSE':
            # select brush
            bpy.ops.wm.context_set_value(data_path=self.datapath, 
                                         value='bpy.data.brushes["{}"]'
                                         .format(self.name))
            return {'FINISHED'}
        else:
            return {'CANCELLED'}
        
    
class BrushFav(bpy.types.PropertyGroup):
    name = bpy.props.StringProperty(name="Brush Name", default="")
    icon = bpy.props.StringProperty(name="Brush Icon", default="")
    datapath = bpy.props.StringProperty(name="Brush Datapath", default="")

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    bpy.types.Scene.BrushFav = bpy.props.CollectionProperty(type=BrushFav)
    #my_item = bpy.context.scene.BrushFav.add()
    #my_item.brush = "SculptDraw"
    #my_item.icon = "NONE"
    #my_item = bpy.context.scene.BrushFav.add()
    #my_item.brush = "Crease"
    #my_item.icon = "NONE"
    #my_item = bpy.context.scene.BrushFav.add()
    #my_item.brush = "Inflate/Deflate"
    #my_item.icon = "NONE"
    #my_item = bpy.context.scene.BrushFav.add()
    #my_item.brush = "Grab"
    #my_item.icon = "NONE"
    
    wm = bpy.context.window_manager
    modes = ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint', 'Particle']
    
    for mode in modes:
        km = wm.keyconfigs.active.keymaps[mode]
        kmi = km.keymap_items.new('wm.call_menu', 'D', 'PRESS')
        kmi.properties.name = "VIEW3D_MT_brush_favs"
        addon_keymaps.append((km, kmi))

def unregister():
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

