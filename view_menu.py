from .Utils.core import *

# adds a view manipulation menu
class ViewMenu(bpy.types.Menu):
    bl_label = "View"
    bl_idname = "VIEW3D_MT_view_menu"

    def draw(self, context):
        menu = Menu(self)

        view_modes = [["Front", 'FRONT'],
                      ["Right", "RIGHT"],
                      ["Top", "TOP"],
                      ["Back", "BACK"],
                      ["Left", "LEFT"],
                      ["Bottom", "BOTTOM"],
                      ["Camera", "CAMERA"]]
        
        # add the menu items
        for mode in view_modes:
            prop = menu.add_item().operator("view3d.viewnumpad", mode[0])
            prop.type = mode[1]
            if mode[0] in ["Top", "Bottom", "Camera"]:
                menu.add_item().separator()

        menu.add_item().menu(OtherViewMenu.bl_idname)


class OtherViewMenu(bpy.types.Menu):
    bl_label = "Other"
    bl_idname = "VIEW3D_MT_other_view_menu"

    def draw(self, context):
        menu = Menu(self)
        
        menu.add_item().label(text="Other")
        menu.add_item().separator()

        menu.add_item().operator("view3d.view_selected")
        menu.add_item().operator("view3d.view_persportho")
        menu.add_item().operator("view3d.localview", text="View Local/Global")
        menu.add_item().operator("screen.region_quadview")

        menu.add_item().separator()

        menu.add_item().prop(context.space_data, "lock_cursor", toggle=True)
        menu.add_item().prop(context.space_data, "lock_camera", toggle=True)

### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

classes = (
    ViewMenu,
    OtherViewMenu
    )

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # create the global menu hotkey
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
    kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS')
    kmi.properties.name = 'VIEW3D_MT_view_menu'
    addon_keymaps.append((km, kmi))


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
    
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
