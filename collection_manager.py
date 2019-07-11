from .Utils.core import *
from .Collection_Manager.internals import *
from .Collection_Manager.operators import *
from .Collection_Manager.ui import *

addon_keymaps = []

classes = (
    ExpandAllOperator,
    ExpandSublevelOperator,
    CMExcludeOperator,
    CMHideOperator,
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
