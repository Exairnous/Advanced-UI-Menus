from .Utils.core import *

collection_tree = []

layer_collections = {}

expanded = []

max_lvl = 0

def update_collection_tree(context):
    collection_tree.clear()
    layer_collections.clear()
    global max_lvl
    max_lvl = 0
    
    get_all_collections(context, context.view_layer.layer_collection.children.items(),
                        {"id": 0,
                         "ptr": context.view_layer.layer_collection,
                         "parent": None},
                        collection_tree, visible=True)

def get_all_collections(context, collections, parent, tree, level=0, visible=False):
    for item in collections:
        layer_collections[item[0]] = {"id": len(layer_collections) +1,
                                      "ptr": item[1],
                                      "parent": parent}
        
        collection = {
        "name": item[0],
        #"ptr": item[1].collection,
        "id": len(layer_collections),
        "lvl": level,
        "visible": True if visible else False,
        "has_children": False,
        "expanded": False,
        "children": []
        }
        
        tree.append(collection)
        
        if len(item[1].children.items()) > 0:
            global max_lvl
            max_lvl += 1
            collection["has_children"] = True
            
            if collection["name"] in expanded:
                get_all_collections(context, item[1].children.items(), layer_collections[item[0]], collection["children"], level+1, visible=True)
                collection["expanded"] = True
                
            else:
                get_all_collections(context, item[1].children.items(), layer_collections[item[0]], collection["children"], level+1)

def update_property_group(context):
    update_collection_tree(context)
    
    context.scene.CMListCollection.clear()
    create_property_group(context, collection_tree)

def create_property_group(context, tree):
    for item in tree:
        if item["visible"]:
            new_cm_listitem = context.scene.CMListCollection.add()
            new_cm_listitem.name = item["name"]
            #new_cm_listitem.obj_ptr = item["ptr"]
            new_cm_listitem.obj_id = item["id"]
            new_cm_listitem.obj_lvl = item["lvl"]
            new_cm_listitem.obj_expanded = item["expanded"]
        
            if item["has_children"]:
                new_cm_listitem.obj_has_children = True
                create_property_group(context, item["children"])

class ExpandAllOperator(bpy.types.Operator):
    '''Expand/Retract all collections'''
    bl_label = "Expand All Items"
    bl_idname = "view3d.expand_all_items"
    
    def execute(self, context):
        if len(expanded) > 0:
            expanded.clear()
        else:
            for laycol in layer_collections.values():
                collection = laycol["ptr"].collection
                if collection.children:
                    expanded.append(collection.name)

        context.scene.CMListIndex = 0
        update_property_group(context)
        
        return {'FINISHED'}

class ExpandSublevelOperator(bpy.types.Operator):
    '''Expand/Retract sublevel. Shift-Click to expand/retract all sublevels'''
    bl_label = "Expand Sublevel Items"
    bl_idname = "view3d.expand_sublevel"
    
    expand: bpy.props.BoolProperty()
    name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    
    def invoke(self, context, event):
        if event.shift:
            expand = None
            
            if self.name in expanded:
                expanded.remove(self.name)
                expand = False
            else:
                expanded.append(self.name)
                expand = True
                
            init_collection = layer_collections[self.name]["ptr"].collection

            def loop(collection):
                for item in collection.children:
                    if expand:
                        if not item.name in expanded:
                            expanded.append(item.name)
                    else:
                        if item.name in expanded:
                            expanded.remove(item.name)
                        
                    if len(item.children) > 0:
                        loop(item)
            
            loop(init_collection)
                    
        else:
            if self.expand:
                expanded.append(self.name)
            else:
                expanded.remove(self.name)
        
        
        context.scene.CMListIndex = self.index
        update_property_group(context)
        
        return {'FINISHED'}
            

class CMNewCollectionOperator(bpy.types.Operator):
    '''Add New Collection'''
    bl_label = "Add New Collection"
    bl_idname = "view3d.add_collection"
    
    child: bpy.props.BoolProperty()
    
    def execute(self, context):
        new_collection = bpy.data.collections.new('Collection')
        scn = context.scene
        
        if len(context.scene.CMListCollection) > 0:
            laycol = layer_collections[scn.CMListCollection[scn.CMListIndex].name]
        
            if self.child:
                laycol["ptr"].collection.children.link(new_collection)
                expanded.append(laycol["ptr"].name)
            
            else:
                laycol["parent"]["ptr"].collection.children.link(new_collection)
        else:
            scn.collection.children.link(new_collection)
            scn.CMListIndex = 0
        
        update_property_group(context)
        
        return {'FINISHED'}


class CMRemoveCollectionOperator(bpy.types.Operator):
    '''Remove Collection'''
    bl_label = "Remove Collection"
    bl_idname = "view3d.remove_collection"
    
    collection_name: bpy.props.StringProperty()
    
    def execute(self, context):
        collection = layer_collections[self.collection_name]["ptr"].collection
        laycol = layer_collections[self.collection_name]
        laycol_parent = laycol["parent"]
        
        if laycol_parent == None:
            parent_collection_id = 0
            laycol_parent_ptr = context.scene.collection
        else:
            parent_collection_id = laycol_parent["id"]
            laycol_parent_ptr = laycol_parent["ptr"]
        
        orig_parent_hide_select = False
        orig_parent_exclude = False
        orig_parent_hide_viewport = False
        
        
        collection.hide_select = False
        laycol["ptr"].exclude = False
        laycol["ptr"].hide_viewport = False
        
        
        if laycol_parent_ptr.collection.hide_select:
            orig_parent_hide_select = True
        
        if laycol_parent_ptr.exclude:
            orig_parent_exclude = True
        
        if laycol_parent_ptr.hide_viewport:
            orig_parent_hide_viewport = True
            
        laycol_parent_ptr.collection.hide_select = False
        laycol_parent_ptr.exclude = False
        laycol_parent_ptr.hide_viewport = False
        
        if collection.objects:
            orig_selected_objs = context.selected_objects
            orig_active_obj = context.active_object
        
                
            bpy.ops.object.select_same_collection(collection=collection.name)
            context.view_layer.objects.active = context.selected_objects[0]
            
            #try:
            bpy.ops.object.link_to_collection(collection_index=parent_collection_id)
            bpy.ops.collection.objects_remove(collection=collection.name)
            #except:
                #pass
            
            bpy.ops.object.select_all(action='DESELECT')
            
            for obj in orig_selected_objs:
                obj.select_set(True)
            context.view_layer.objects.active = orig_active_obj
        
        
        if collection.children:
            for item in collection.children:
                laycol_parent_ptr.collection.children.link(item)
        
        laycol_parent_ptr.collection.hide_select = orig_parent_hide_select
        laycol_parent_ptr.exclude = orig_parent_exclude
        laycol_parent_ptr.hide_viewport = orig_parent_hide_viewport
        
        bpy.data.collections.remove(collection)
        
        update_property_group(context)
        
        return {'FINISHED'}


class CMSetCollectionOperator(bpy.types.Operator):
    '''Click moves object to collection.  Shift-Click adds/removes from collection'''
    bl_label = "Set Collection"
    bl_idname = "view3d.set_collection"
    
    collection_index: bpy.props.IntProperty()
    collection_name: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        collection = layer_collections[self.collection_name]["ptr"].collection
        
        if event.shift:
            in_collection = True
            
            for obj in context.selected_objects:
                if obj.name not in collection.objects:
                    in_collection = False
            
            if not in_collection:
                bpy.ops.object.link_to_collection(collection_index=self.collection_index)
            else:
                for obj in context.selected_objects:
                    if len(obj.users_collection) == 1:
                        send_report("Error removing 1 or more objects from this collection.\nObjects would be left without a collection")
                        return {'FINISHED'}
                    
                bpy.ops.collection.objects_remove(collection=collection.name)
        else:
            bpy.ops.object.move_to_collection(collection_index=self.collection_index)
        
        return {'FINISHED'}
        


class CMListCollection(bpy.types.PropertyGroup):
    #name: bpy.props.StringProperty() -> Instantiated by default
    #obj_ptr: bpy.props.PointerProperty(type=bpy.types.Collection)
    obj_id: bpy.props.IntProperty()
    obj_lvl: bpy.props.IntProperty()
    obj_has_children: bpy.props.BoolProperty(default=False)
    obj_expanded: bpy.props.BoolProperty()


class CM_UL_items(bpy.types.UIList):
    
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        laycol = layer_collections[item.name]["ptr"]
        collection = laycol.collection
        
        row = layout.row(align=True)
        row.alignment = 'LEFT'
        
        if item.obj_lvl > 0:
            for x in range(item.obj_lvl):
                row.label(icon='BLANK1')
        
        if item.obj_has_children:
            if item.obj_expanded:
                prop = row.operator("view3d.expand_sublevel", text="", icon='DISCLOSURE_TRI_DOWN', emboss=False)
                prop.expand = False
                prop.name = item.name
                prop.index = index
            else:
                prop = row.operator("view3d.expand_sublevel", text="", icon='DISCLOSURE_TRI_RIGHT', emboss=False)
                prop.expand = True
                prop.name = item.name
                prop.index = index
        else:
            row.label(icon='BLANK1')
        
        row.label(icon='IMAGE_PLANE')
        row.prop(collection, "name", text="", expand=True)
        row.label()
        
        rowset = row.row()
        rowset.operator_context = 'INVOKE_DEFAULT'
            
        if len(context.selected_objects) > 0 and context.active_object:
            if context.active_object.name in collection.objects:
                prop = rowset.operator("view3d.set_collection", text="", icon='SNAP_VOLUME', emboss=False)
            else:
                prop = rowset.operator("view3d.set_collection", text="", icon='MESH_CUBE', emboss=False)
        else:
            rowset.enabled = False
            prop = rowset.operator("view3d.set_collection", text="", icon='MESH_CUBE', emboss=False)
            
            
            
        prop.collection_index = item.obj_id
        prop.collection_name = collection.name
        
        
        row.prop(laycol, "exclude", text="", emboss=False)
        row.prop(collection, "hide_select", icon='RESTRICT_SELECT_OFF', icon_only=True, emboss=False)
        row.prop(laycol, "hide_viewport", icon='HIDE_OFF', icon_only=True, emboss=False)
        
        row.operator("view3d.remove_collection", text="", icon='X', emboss=False).collection_name = collection.name

    def invoke(self, context, event):
        pass 


class CollectionManager(bpy.types.Operator):
    bl_label = "Collection Manager"
    bl_idname = "view3d.collection_manager"
    
    def draw(self, context):
        layout = self.layout
        
        layout.row().label(text="Collection Manager")
        layout.row().separator()
        
        row1 = layout.row()
        row1.alignment = 'LEFT'
        
        if len(expanded) > 0:
            row1.operator("view3d.expand_all_items", text="Retract All Items")
        else:
            row1.operator("view3d.expand_all_items", text="Expand All Items")
        
        row1.enabled = False
        for item in collection_tree:
            if item["has_children"]:
                row1.enabled = True
                break
            
        layout.row().template_list("CM_UL_items", "", context.scene, "CMListCollection", context.scene, "CMListIndex", rows=15, sort_lock=True)
        
        row = layout.row()
        row.operator("view3d.add_collection", text="Add Collection", icon='COLLECTION_NEW').child = False
        row.operator("view3d.add_collection", text="Add SubCollection", icon='COLLECTION_NEW').child = True
        
        
    def execute(self, context):
        wm = context.window_manager
        lvl = 0
        
        expanded.clear()
        context.scene.CMListIndex = 0
        update_property_group(context)
        
        if max_lvl > 5:
            lvl = max_lvl - 5
        
        if lvl > 25:
            lvl = 25
            
        
        return wm.invoke_popup(self, width=(400+(lvl*20)))
    
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ExpandAllOperator,
    ExpandSublevelOperator,
    CMNewCollectionOperator,
    CMRemoveCollectionOperator,
    CMSetCollectionOperator,
    CMListCollection,
    CM_UL_items,
    CollectionManager,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    set_prop("CollectionProperty", "bpy.types.Scene.CMListCollection", type=CMListCollection)
    set_prop("IntProperty", "bpy.types.Scene.CMListIndex")


    # create the global menu hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode')
    kmi = km.keymap_items.new('view3d.collection_manager', 'M', 'PRESS')
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
