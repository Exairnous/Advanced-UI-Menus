from .Utils.core import *
        
def get_layers(context):
    # if the layer management addon is enabled name the layers with the layer names
    try:
        layernames = []
        # if the name has "layer" in front of a number remove "layer" and leave the number
        for x in range(20):
            layer_name = context.scene.namedlayers.layers[x].name
            if layer_name in ["Layer{}".format(x+1), "Layer0{}".format(x+1)]:
                layernames.append("{0}".format(x+1))
            else:
                # replace blank layer names with a space so the button will be full length
                layernames.append(layer_name if layer_name is not "" else " ")

    # if not then name the layers with numbers
    except:
        layernames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
    
    return layernames
        
def set_layer_func(self, context, event):
    if event.shift:
        # toggle the layer on/off
        context.scene.layers[self.layer_num] = not context.scene.layers[self.layer_num]
        bpy.types.Scene.layer_changed = True
    else:
        # create a boolian list of which layers on and off
        layers = [False]*20
        layers[self.layer_num] = True
            
        # apply the list to blender's layers
        context.scene.layers = layers
        
    bpy.types.Scene.layer_changed = True
        
    return {'FINISHED'}
    
custom_ops = []
        
def add_set_layer_op(num, layer):
    op_name = 'view3d.set_layer_view_'+str(num)
    
    nc = type(  'DynOpSetLayer_'+str(num),
                (bpy.types.Operator, ),
                {'bl_idname': op_name,
                'bl_label': "Set Layer View",
                'bl_description': "Visualize this Layer, Shift-Click to select multiple layers\nName: "+layer,
                'layer_num': bpy.props.IntProperty(name="layer_num"),
                'invoke': set_layer_func
            })
    custom_ops.append(nc)
    bpy.utils.register_class(nc)

class SetObjectLayer(bpy.types.Operator):
    '''Move objects to this Layer, Shift-Click to select multiple layers'''
    bl_idname = "view3d.set_object_layer"
    bl_label = "Move Object To Layers Operator"
    
    layer_num = bpy.props.IntProperty(name="layer_num")
    
    def invoke(self, context, event):
        selected_objects = [object for object in context.scene.objects if object.select == True]
        
        if event.shift:
            # toggle the objects on/off of the layer
            for object in selected_objects:
                if object.layers[self.layer_num] == context.scene.objects.active.layers[self.layer_num]:
                    enabled = not context.scene.objects.active.layers[self.layer_num]
                else:
                    enabled = True
                    break
                
            for object in selected_objects:
                layers = object.layers
                layers[self.layer_num] = enabled
                object.layers = layers
            bpy.types.Scene.layer_changed = True
        else:
            # create a boolian list of which layers on and off
            layers = [False]*20
            layers[self.layer_num] = True
            
            # move the objects to the layer
            for object in selected_objects:
                object.layers = layers
        
        bpy.types.Scene.layer_changed = True
        
        return {'FINISHED'}
    
class LayersWindow(bpy.types.Operator):
    bl_label = "Layers"
    bl_idname = "view3d.layers_window"
    
    current_space = None

    def check(self, context):
        if bpy.types.Scene.layer_changed:
            bpy.types.Scene.layer_changed = False
            return True
        else:
            return False
    
    def draw(self, context):
        if context.space_data:
            self.current_space = context.space_data
        
        ui = Menu(self)
        
        column_flow = ui.add_item("column_flow", columns=2, align=True)
        
        layernames = get_layers(context)
        
        # add the menu items
        for num in range(20):
            op_name = 'view3d.set_layer_view_'+str(num)
            
            has_active = (context.object and context.object.layers[num])
            is_layer_used = self.current_space.layers_used[num]
            icon = ('LAYER_ACTIVE' if has_active else 'LAYER_USED') if is_layer_used else 'RADIOBUT_OFF'
            
            prop = ui.add_item(parent=column_flow).operator("view3d.set_object_layer", "", icon=icon)
            prop.layer_num = num
            
            if num == context.scene.active_layer:
                prop = ui.current_item.operator(op_name, layernames[num], icon='FILE_TICK')
                
            elif context.scene.layers[num]:
                prop = ui.current_item.operator(op_name, layernames[num], icon='RESTRICT_VIEW_OFF')
                
            else:
                prop = ui.current_item.operator(op_name, layernames[num], icon='BLANK1')
            
            ui.current_item.operator_context = 'INVOKE_DEFAULT'
            prop.layer_num = num
            
            ui.current_item.separator()
            
            if num in [4, 14]:
                ui.add_item(parent=column_flow).separator()
                ui.add_item(parent=column_flow).separator()
        
    def invoke(self, context, event):
        wm = context.window_manager
        
        layernames = get_layers(context)
        
        for op in custom_ops:
            bpy.utils.unregister_class(op)
        
        custom_ops.clear()
        
        
        for num, layer in enumerate(layernames):
            add_set_layer_op(num, layer)
        
        return wm.invoke_props_dialog(self)
    
    def execute(self, context):
        return {'FINISHED'}
    
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
        
    if value in ("menu","pie"):
        print("got here")
        km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
        kmi = km.keymap_items.new('view3d.layers_window_operator', 'M', 'PRESS')
        addon_keymaps.append((km, kmi))

def register():
                    
    set_prop("BoolProperty", "bpy.types.Scene.layer_changed", name="layer_changed")

    # create the global hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("3DView - Layers Window")
    set_keybind(setting.value)


def unregister():
    # remove keymaps when add-on is deactivated
    set_keybind("off")
    
    for op in custom_ops:
        bpy.utils.unregister_class(op)
