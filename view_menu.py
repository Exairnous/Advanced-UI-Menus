from .Utils.core import *

### ------------ Menus ------------ ###

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

def set_keybind(value):
    wm = bpy.context.window_manager
    
    if value in ("off", "menu", "pie"):
        for km, kmi in addon_keymaps:
            km.keymap_items.remove(kmi)
        addon_keymaps.clear()
    else:
        print("invalid value")
        return
        
    if value == "menu":   
        km = wm.keyconfigs.addon.keymaps.new(name='Object Non-modal')
        kmi = km.keymap_items.new('wm.call_menu', 'Q', 'PRESS')
        kmi.properties.name = 'VIEW3D_MT_view_menu'
        addon_keymaps.append((km, kmi))
        
    elif value == "pie":
        ### Pie Code Goes Here ###
        pass

def register():
    # create the global hotkey
    Aum_Settings = bpy.context.user_preferences.addons["Advanced_UI_Menus"].preferences.settings
    setting = Aum_Settings.get("3DView - View Menu")
    set_keybind(setting.value)


def unregister():  
    # remove keymaps when add-on is deactivated
    set_keybind("off")
