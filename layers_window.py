from .Utils.core import *

class SetLayerView(bpy.types.Operator):
    # Visualize this Layer, Shift-Click to select multiple layers
    
    tooltip = set_prop("StringProperty", 
                    "bpy.types.Scene.layer_name", 
                    name="layer_name",
                    default="test")
    
    layer_num = set_prop("IntProperty", 
                    "bpy.types.Scene.layer_num_view", 
                    name="layer_num")
    
    bl_idname = "view3d.set_layer_view"
    bl_label = "Set Layer View"
    bl_description = "Layer Name ({})".format(tooltip[1]["name"])
    
    def invoke(self, context, event):
        if event.shift:
            # toggle the layer on/off
            context.scene.layers[self.layer_num] = not context.scene.layers[self.layer_num]
            bpy.types.Scene.layer_changed = True
            print("tooltip = {}".format(self.tooltip))
        else:
            # create a boolian list of which layers on and off
            layers = [False]*20
            layers[self.layer_num] = True
            
            # apply the list to blender's layers
            context.scene.layers = layers
        
        bpy.types.Scene.layer_changed = True
        
        return {'FINISHED'}
    
class SetObjectLayer(bpy.types.Operator):
    '''Move objects to this Layer, Shift-Click to select multiple layers'''
    bl_idname = "view3d.set_object_layer"
    bl_label = "Move Object To Layers Operator"
    
    layer_num = set_prop("IntProperty", 
                    "bpy.types.Scene.layer_num_object", 
                    name="layer_num")
    
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

class SetLayerViewWindow(bpy.types.Operator):
    bl_label = "Set Visible Layers"
    bl_idname = "view3d.set_layer_view_window"

    def check(self, context):
        if bpy.types.Scene.layer_changed:
            bpy.types.Scene.layer_changed = False
            return True
        else:
            return False
    
    def draw(self, context):
        ui = Menu(self)
        
        column_flow = ui.add_item("column_flow", columns=2)
        #column_flow = ui.add_item()
        
        # if the layer management addon is enabled name the layers with the layer names
        try:
            layernames = []
             # if the name has "layer" in front of a number remove "layer" and leave the number
            for x in range(20):
                if context.scene.namedlayers.layers[x].name in ["Layer{}".format(x+1), "Layer0{}".format(x+1)]:
                    layernames.append("{0}".format(x+1))
                else:
                    layernames.append(context.scene.namedlayers.layers[x].name)

        # if not then name the layers with numbers
        except:
            layernames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
        
        # add the menu items
        for num in range(20):
            #if num == 10:
                #column_flow = ui.add_item()
            if num == context.scene.active_layer:
                prop = ui.add_item(parent=column_flow).operator("view3d.set_layer_view", layernames[num], icon='FILE_TICK')
                
            elif context.scene.layers[num]:
                prop = ui.add_item(parent=column_flow).operator("view3d.set_layer_view", layernames[num], icon='RESTRICT_VIEW_OFF')
                
            else:
                prop = ui.add_item(parent=column_flow).operator("view3d.set_layer_view", layernames[num], icon='BLANK1')
            
            ui.current_item.operator_context = 'INVOKE_DEFAULT'
            prop.layer_num = num
            prop.tooltip = layernames[num]
        
    def execute(self, context):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class SetObjectLayerWindow(bpy.types.Operator):
    bl_label = "Move Object to Layers"
    bl_idname = "view3d.set_object_layer_window"

    def check(self, context):
        if bpy.types.Scene.layer_changed:
            bpy.types.Scene.layer_changed = False
            return True
        else:
            return False
    
    def draw(self, context):
        ui = Menu(self)
        
        column_flow = ui.add_item("column_flow", columns=2)
        
        # if the layer management addon is enabled name the layers with the layer names
        try:
            layernames = []
             # if the name has "layer" in front of a number remove "layer" and leave the number
            for x in range(20):
                if context.scene.namedlayers.layers[x].name in ["Layer{}".format(x+1), "Layer0{}".format(x+1)]:
                    layernames.append("{0}".format(x+1))
                else:
                    layernames.append(context.scene.namedlayers.layers[x].name)

        # if not then name the layers with numbers
        except:
            layernames = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
                     "11", "12", "13", "14", "15", "16", "17", "18", "19", "20"]
        
        # add the menu items
        for num in range(20):
            if context.scene.objects.active.layers[num]:
                prop = ui.add_item(parent=column_flow).operator("view3d.set_object_layer", layernames[num], icon='RESTRICT_VIEW_OFF')
                
            else:
                prop = ui.add_item(parent=column_flow).operator("view3d.set_object_layer", layernames[num], icon='BLANK1')
            
            ui.current_item.operator_context = 'INVOKE_DEFAULT'
            prop.layer_num = num
        
    def execute(self, context):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)
    
class LayersWindowOperator(bpy.types.Operator):
    bl_label = "Layers Window Operator"
    bl_idname = "view3d.layers_window_operator"

    def modal(self, context, event):
        if get_mode() == edit:
            return {'CANCELLED'}
        
        current_time = time.time()
        
        # if key has been held for more than 0.3 seconds call the menu
        if event.value == 'RELEASE' and current_time > self.start_time + 0.3:
            bpy.ops.view3d.set_object_layer_window()
            
            return {'FINISHED'}
        
        # else toggle snap mode on/off
        elif event.value == 'RELEASE' and current_time < self.start_time + 0.3:
            bpy.ops.view3d.set_layer_view_window()
                
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def execute(self, context):
        self.start_time = time.time()
        context.window_manager.modal_handler_add(self)
        
        return {'RUNNING_MODAL'}
    
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
