from ..Utils.core import *
from .internals import *

class ExpandAllOperator(bpy.types.Operator):
    '''Expand/Collapse all collections'''
    bl_label = "Expand All Items"
    bl_idname = "view3d.expand_all_items"
    
    def execute(self, context):
        if len(expanded) > 0:
            expanded.clear()
        else:
            for laycol in layer_collections.values():
                if laycol["ptr"].children:
                    expanded.append(laycol["name"])
        
        # set selected row to the first row and update tree view
        context.scene.CMListIndex = 0
        update_property_group(context)
        
        return {'FINISHED'}


class ExpandSublevelOperator(bpy.types.Operator):
    '''Expand/Collapse sublevel. Shift-Click to expand/collapse all sublevels'''
    bl_label = "Expand Sublevel Items"
    bl_idname = "view3d.expand_sublevel"
    
    expand: bpy.props.BoolProperty()
    name: bpy.props.StringProperty()
    index: bpy.props.IntProperty()
    
    def invoke(self, context, event):
        if event.shift:
            # expand/collapse all subcollections
            expand = None
            
            # check whether to expand or collapse
            if self.name in expanded:
                expanded.remove(self.name)
                expand = False
            else:
                expanded.append(self.name)
                expand = True
            
            # do expanding/collapsing
            def loop(laycol):
                for item in laycol.children:
                    if expand:
                        if not item.name in expanded:
                            expanded.append(item.name)
                    else:
                        if item.name in expanded:
                            expanded.remove(item.name)
                        
                    if len(item.children) > 0:
                        loop(item)
            
            loop(layer_collections[self.name]["ptr"])
            
        else:
            # expand/collapse collection
            if self.expand:
                expanded.append(self.name)
            else:
                expanded.remove(self.name)
        
        
        # set selected row to the collection you're expanding/collapsing and update tree view
        context.scene.CMListIndex = self.index
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
            # add object to collection
            
            # check if in collection
            in_collection = True
            
            for obj in context.selected_objects:
                if obj.name not in collection.objects:
                    in_collection = False
            
            if not in_collection:
                # add to collection
                bpy.ops.object.link_to_collection(collection_index=self.collection_index)
                
            else:
                # check and disallow removing from all collections
                for obj in context.selected_objects:
                    if len(obj.users_collection) == 1:
                        send_report("Error removing 1 or more objects from this collection.\nObjects would be left without a collection")
                        
                        return {'FINISHED'}
                
                # remove from collection
                bpy.ops.collection.objects_remove(collection=collection.name)
        
        else:
            # move object to collection
            bpy.ops.object.move_to_collection(collection_index=self.collection_index)
        
        return {'FINISHED'}


class CMExcludeOperator(bpy.types.Operator):
    '''Exclude collection. Shift-Click to isolate collection'''
    bl_label = "Exclude Collection"
    bl_idname = "view3d.exclude_collection"
    
    name: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        laycol_ptr = layer_collections[self.name]["ptr"]
        
        if event.shift:
            # isolate/de-isolate exclusion of collections
            active_layer_collections = [x for x in layer_collections.values() \
                                          if x["ptr"].exclude == False]
            
            # check if collection isolated
            if len(active_layer_collections) == 1 and active_layer_collections[0]["name"] == self.name:
                # enable all collections
                for item in layer_collections.values():
                    item["ptr"].exclude = False
            
            else:
                # isolate collection
                for item in layer_collections.values():
                    if item["name"] != laycol_ptr.name:
                        item["ptr"].exclude = True
                
                laycol_ptr.exclude = False
                
                # exclude all children
                laycol_iter_list = [laycol_ptr.children]
                while len(laycol_iter_list) > 0:
                    new_laycol_iter_list = []
                    for laycol_iter in laycol_iter_list:
                        for layer_collection in laycol_iter:
                            layer_collection.exclude = True
                            if len(layer_collection.children) > 0:
                                new_laycol_iter_list.append(layer_collection.children)
                    
                    laycol_iter_list = new_laycol_iter_list
                            
        
        else:
            # toggle exclusion of collection
            laycol_ptr.exclude = not laycol_ptr.exclude
        
        
        return {'FINISHED'}


class CMHideOperator(bpy.types.Operator):
    '''Hide collection. Shift-Click to isolate collection chain'''
    bl_label = "Hide Collection"
    bl_idname = "view3d.hide_collection"
    
    name: bpy.props.StringProperty()
    
    def invoke(self, context, event):
        laycol_ptr = layer_collections[self.name]["ptr"]
        
        if event.shift:
            # isolate/de-isolate view of collections
            active_layer_collections = [x for x in layer_collections.values() \
                                          if x["ptr"].hide_viewport == False]
            
            layerchain = []
            laycol = layer_collections[self.name]
            
            # get chain of parents up to top level collection
            while laycol["id"] != 0:
                    layerchain.append(laycol)
                    laycol = laycol["parent"]
                    
            # check if reversed layerchain matches active collections
            if layerchain[::-1] == active_layer_collections:
                # show all collections
                for laycol in layer_collections.values():
                    laycol["ptr"].hide_viewport = False
                    
            else:
                # hide all collections
                for laycol in layer_collections.values():
                    laycol["ptr"].hide_viewport = True
                
                # show active collection plus parents
                laycol_ptr.hide_viewport = False
                
                laycol = layer_collections[self.name]
                while laycol["id"] != 0:
                    laycol["ptr"].hide_viewport = False
                    laycol = laycol["parent"]
        
        else:
            # toggle view of collection
            laycol_ptr.hide_viewport = not laycol_ptr.hide_viewport
        
        return {'FINISHED'}


class CMRemoveCollectionOperator(bpy.types.Operator):
    '''Remove Collection'''
    bl_label = "Remove Collection"
    bl_idname = "view3d.remove_collection"
    
    collection_name: bpy.props.StringProperty()
    
    def execute(self, context):
        laycol = layer_collections[self.collection_name]
        collection = laycol["ptr"].collection
        laycol_parent = laycol["parent"]
        
        # save state and remove all hiding properties of parent collection
        orig_parent_hide_select = False
        orig_parent_exclude = False
        orig_parent_hide_viewport = False
        
        if laycol_parent["ptr"].collection.hide_select:
            orig_parent_hide_select = True
        
        if laycol_parent["ptr"].exclude:
            orig_parent_exclude = True
        
        if laycol_parent["ptr"].hide_viewport:
            orig_parent_hide_viewport = True
        
        laycol_parent["ptr"].collection.hide_select = False
        laycol_parent["ptr"].exclude = False
        laycol_parent["ptr"].hide_viewport = False
        
        
        # remove all hiding properties of this collection
        collection.hide_select = False
        laycol["ptr"].exclude = False
        laycol["ptr"].hide_viewport = False
        
        
        # shift all objects in this collection to the parent collection
        if collection.objects:
            orig_selected_objs = context.selected_objects
            orig_active_obj = context.active_object
        
            # select all objects in collection
            bpy.ops.object.select_same_collection(collection=collection.name)
            context.view_layer.objects.active = context.selected_objects[0]
            
            # remove any objects already in parent collection from selection
            for obj in context.selected_objects:
                if obj in laycol["parent"]["ptr"].collection.objects.values():
                    obj.select_set(False)
            
            # link selected objects to parent collection
            bpy.ops.object.link_to_collection(collection_index=laycol_parent["id"])
            
            # remove objects from collection
            bpy.ops.collection.objects_remove(collection=collection.name)
            
            # reset selection original values
            bpy.ops.object.select_all(action='DESELECT')
            
            for obj in orig_selected_objs:
                obj.select_set(True)
            context.view_layer.objects.active = orig_active_obj
        
        
        # shift all child collections to the parent collection
        if collection.children:
            for subcollection in collection.children:
                laycol_parent["ptr"].collection.children.link(subcollection)
        
        # reset hiding properties of parent collection
        laycol_parent["ptr"].collection.hide_select = orig_parent_hide_select
        laycol_parent["ptr"].exclude = orig_parent_exclude
        laycol_parent["ptr"].hide_viewport = orig_parent_hide_viewport
        
        
        # remove collection and update tree view
        bpy.data.collections.remove(collection)
        
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
        
        # if there are collections
        if len(scn.CMListCollection) > 0:
            # get selected collection
            laycol = layer_collections[scn.CMListCollection[scn.CMListIndex].name]
            
            # add new collection
            if self.child:
                laycol["ptr"].collection.children.link(new_collection)
                expanded.append(laycol["name"])
                
            else:
                laycol["parent"]["ptr"].collection.children.link(new_collection)
                
        # if no collections add top level collection and select it
        else:
            scn.collection.children.link(new_collection)
            scn.CMListIndex = 0
        
        # update tree view
        update_property_group(context)
        
        return {'FINISHED'}
