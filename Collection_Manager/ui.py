from ..Utils.core import *
from .internals import *


class CollectionManager(bpy.types.Operator):
    bl_label = "Collection Manager"
    bl_idname = "view3d.collection_manager"
    
    def draw(self, context):
        layout = self.layout
        
        layout.row().label(text="Collection Manager")
        layout.row().separator()
        
        row1 = layout.row()
        row1.alignment = 'LEFT'
        row1.enabled = False
        
        if len(expanded) > 0:
            text = "Collapse All Items"
        else:
            text = "Expand All Items"
        
        row1.operator("view3d.expand_all_items", text=text)
        
        for laycol in collection_tree:
            if laycol["has_children"]:
                row1.enabled = True
                break
            
        layout.row().template_list("CM_UL_items", "", context.scene, "CMListCollection", context.scene, "CMListIndex", rows=15, sort_lock=True)
        
        row2 = layout.row()
        row2.operator("view3d.add_collection", text="Add Collection", icon='COLLECTION_NEW').child = False
        
        row2.operator("view3d.add_collection", text="Add SubCollection", icon='COLLECTION_NEW').child = True
        
        
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


class CM_UL_items(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data,active_propname, index):
        
        laycol = layer_collections[item.name]
        collection = laycol["ptr"].collection
        
        row = layout.row(align=True)
        row.alignment = 'LEFT'
        
        # indent child items
        if laycol["lvl"] > 0:
            for x in range(laycol["lvl"]):
                row.label(icon='BLANK1')
        
        # add expander if collection has children to make UIList act like tree view
        if laycol["has_children"]:
            if laycol["expanded"]:
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
        
        
        row.label(icon='GROUP')
        
        row.prop(collection, "name", text="", expand=True)
        
        # used as a separator (actual separator not wide enough)
        row.label()
        
        # add set_collection op
        row_setcol = row.row()
        row_setcol.operator_context = 'INVOKE_DEFAULT'
        
        icon = 'MESH_CUBE'
        
        if len(context.selected_objects) > 0 and context.active_object:
            if context.active_object.name in collection.objects:
                icon = 'SNAP_VOLUME'
        else:
            row_setcol.enabled = False
        
        
        prop = row_setcol.operator("view3d.set_collection", text="", icon=icon, emboss=False)
        prop.collection_index = laycol["id"]
        prop.collection_name = item.name
        
        
        if laycol["ptr"].exclude:
            icon = 'CHECKBOX_DEHLT'
        else:
            icon='CHECKBOX_HLT'
        
        row.operator("view3d.exclude_collection", text="", icon=icon, emboss=False).name = item.name
            
        
        row.prop(collection, "hide_select", icon='RESTRICT_SELECT_OFF', icon_only=True, emboss=False)
        
        
        if laycol["ptr"].hide_viewport:
            icon = 'HIDE_ON'
        else:
            icon = 'HIDE_OFF'
        
        row.operator("view3d.hide_collection", text="", icon=icon, emboss=False).name = item.name
        
        
        row.operator("view3d.remove_collection", text="", icon='X', emboss=False).collection_name = item.name
    
    
    def invoke(self, context, event):
        pass
