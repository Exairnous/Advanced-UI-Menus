from .Utils.core import *

class ObjectManipulationMenu(bpy.types.Menu):
    bl_label = "Object Manipulation"
    bl_idname = "VIEW3D_MT_obj_manip_menu"
    
    def draw(self, context):
        menu = Menu(self)
        menu.add_item().prop(context.space_data, "show_gizmo_object_translate", text="Move Gizmo")
        menu.add_item().prop(context.space_data, "show_gizmo_object_rotate", text="Rotate Gizmo")
        menu.add_item().prop(context.space_data, "show_gizmo_object_scale", text="Scale Gizmo")
        menu.add_item().label(text="Transform Orientation")
        menu.add_item().separator()
        for mode in context.scene.transform_orientation_slots.items()[0][1].bl_rna.properties['type'].enum_items:
            menuprop(menu.add_item(), mode.name, mode.identifier, "scene.transform_orientation_slots.items()[0][1].type",
            icon='RADIOBUT_OFF', disable=True, disable_icon='RADIOBUT_ON')

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ObjectManipulationMenu,
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global menu hotkey
    wm = bpy.context.window_manager
    modes = ['Object Mode', 'Mesh', 'Curve', 'Armature', 'Metaball', 'Lattice', 'Pose']
    
    for mode in modes:
        km = wm.keyconfigs.addon.keymaps.new(name=mode)
        kmi = km.keymap_items.new('wm.call_menu', 'SPACE', 'PRESS', alt=True)
        kmi.properties.name = "VIEW3D_MT_obj_manip_menu"
        addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
