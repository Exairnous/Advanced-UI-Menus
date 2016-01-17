import xml.etree.ElementTree as ET
import inspect
import collections

from .Utils.core import *

__location__ = os.path.dirname(os.path.realpath(__file__)) + "/Utils"

tree = None
root = None
cur_menu = None

op_list = []
menu_list = []

def read_xml():
    global tree
    global root
    
    tree = ET.parse(os.path.join(__location__, "CustomMenu.xml"))
    root = tree.getroot()
    
def get_menu(context):
    global root
    area = context.space_data.type
    
    if context.object:
        mode = get_mode()
    else:
        mode = context.mode
        
    if area == 'VIEW_3D':
        menu = root.findall(".//menu[@area='{0}'][@mode='{1}']".format(area, mode))
    else:
        menu = root.findall(".//menu[@area='{0}']".format(area))
    
    if not menu:
        new_menu = ET.SubElement(root, "menu")
        new_menu.set("area", area)
        if area == 'VIEW_3D':
            new_menu.set("mode", mode)
            
        format_xml(root)
        tree.write(os.path.join(__location__, "CustomMenu.xml"))
        
        if area == 'VIEW_3D':
            menu = root.findall(".//menu[@area='{0}'][@mode='{1}']".format(area, mode))
        else:
            menu = root.findall(".//menu[@area='{0}']".format(area))
    
    return menu[0]

def get_custom_item_list():
    global cur_menu
    item_list = []
    rem_item_list = []

    item_list.append(("0", "Start", "Start"))

    for place, item in enumerate(cur_menu):
        item_type = item.get("type")

        if item_type == "OP":
            if item[1].text != "none":
                name = "OP: {0}".format(item[1].text)
                desc = item[0].text
            else:   
                ent_op = "bpy.ops.{0}()".format(item[0].text)
                op = eval("{0}.get_rna()".format(ent_op[:str.find(ent_op, "(")]))
                name = "OP: {0}".format(op.bl_rna.name)
                desc = item[0].text
                
        elif item_type == "MENU":
            if item[1].text != "none":
                name = "MENU: {0}".format(item[1].text)
                desc = item[1].text
            else:
                name = "MENU: {0}".format(item[0].text)
                desc = item[0].text
                
        elif item_type == "LAB":
            name = "LAB: {0}".format(item[0].text)
            desc = item[0].text
        else:
            name = "SEP: Separator"
            desc = "Separator"

        item_list.append((str(place+1), name, desc))
        rem_item_list.append((str(place), name, desc))

    set_prop("EnumProperty", 
            "bpy.types.Scene.CustomMenuItemList",
            name = "",
            items=item_list)
    set_prop("EnumProperty", 
            "bpy.types.Scene.CustomMenuItemRemList",
            name = "",
            items=rem_item_list)
            
def fill_operator_list():
    global op_list
    operators = []

    for op_module_name in dir(bpy.ops):
        op_module = getattr(bpy.ops, op_module_name)
        for op_submodule_name in dir(op_module):
            op = getattr(op_module, op_submodule_name)
            text = repr(op)
            ent_op = text.split("\n")[1]
            op_path = ent_op[8:str.find(ent_op, "(")]
            if ent_op.startswith("bpy.ops.") and not "import." in ent_op:
                op = eval("{0}.get_rna()".format(ent_op[:str.find(ent_op, "(")]))
                op_name = op.bl_rna.name
                operators.append((op_path, op_path.split(".")[0].upper() + " - " + op_name, op_path))

    op_list = operators

def get_operator_list(self, context):
    global op_list

    return op_list

def fill_menu_list():
    global menu_list
    menus = []

    for module_name in dir(bpy.types):
        try:
            module_type = "{}".format(eval("bpy.types.{}.__bases__".format(module_name)))
            if "Menu" in module_type:
                label = eval("bpy.types.{}.bl_label".format(module_name))
                name = module_name.split("_")[0] + " - " + label if label != "" else module_name
                menus.append((module_name, name, module_name))
        except:
            pass

    menu_list = menus
    
def get_menu_list(self, context):
    global menu_list

    return menu_list
    
def format_xml(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            format_xml(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i
    
def errmsg(self, errlst):
        for entry in errlst:
            self.layout.row().label(entry)
        return None
    
def get_arg_list(argstring):
    opkwarg_string = argstring
    final_op_kw_list = []
    kwargdic = collections.OrderedDict()

    opkwlist = opkwarg_string.split("=")
    for x, i in enumerate(opkwlist, 1):
        kwarg = i.rsplit(" ", 1)
        if len(kwarg) == 2:
            if x != len(opkwlist):
                if kwarg[0][-1] == ",":
                    kwarg[0] = kwarg[0][:-1]

                final_op_kw_list.append(kwarg[0])

                if kwarg[1][-1] == ",":
                    kwarg[1] = kwarg[1][:-1]
                final_op_kw_list.append(kwarg[1])
            else:
                final_op_kw_list.append(kwarg[0] + kwarg[1])
        else:
            if not kwarg[0]:
                return "ERROR"
            if kwarg[0][-1] == ",":
                kwarg[0] = kwarg[0][:-1]
            final_op_kw_list.append(kwarg[0])
    
    keywords = final_op_kw_list[::2]
    vals = final_op_kw_list[1::2]
    
    for k, v in zip(keywords, vals):
        kwargdic[k] = v
    
    return kwargdic
    
def get_arg_string(op_path):
    op_inst = eval("bpy.ops.{0}.get_instance".format(op_path))
    op_string = str(op_inst)
    op_string = op_string[op_string.find("bpy.ops"):]
    opkwarg_string = op_string[op_string.find("(")+1:op_string.find(")", -1)-1]          
    
    return opkwarg_string
    
def update_args(self, context):
    fill_operator_list()
    if context.scene.CustomMenuItemPath in [x[0] for x in get_operator_list(self, context)]:
        context.scene.CustomMenuOperatorArgs = get_arg_string(context.scene.CustomMenuItemPath)
    
class CustomMenu(bpy.types.Menu):
    bl_label = "Custom Menu"
    bl_idname = "view3d.custom_menu"
    
    
    def draw(self, context):
        menu = Menu(self)
        global tree
        global root
        global cur_menu
       
        cur_menu = get_menu(context)
        
        error_str = "Invalid Arguments for Item(s):"
        errors = []

        for item in cur_menu:
            if item.get("type") == "SEP":
                menu.add_item().separator()
            elif item.get("type") == "LAB":
                menu.add_item().label(item[0].text, icon=item[1].text)
            elif item.get("type") == "OP":
                op_row = menu.add_item()
                #print(op_row.operator_context)
                op_row.operator_context = 'INVOKE_DEFAULT'
                
                if item[1].text != "none":
                    op = op_row.operator(item[0].text, text=item[1].text, icon=item[2].text)
                else:
                    op = op_row.operator(item[0].text, icon=item[2].text)
                
                #print(item[3].text)
                if item[3].text != "none":
                    if ";" in item[3].text:
                        args = item[3].text.split(";")
                        arg_vals = item[4].text.split(";")
                    else:
                        args = [item[3].text]
                        arg_vals = [item[4].text]
                    try:
                        #print(args, " ", arg_vals)
                        for int, arg in enumerate(args):
                            exec("op.{0} = {1}".format(arg, arg_vals[int]))
                    except:
                        errors.append("{0}".format(item[0].text))
                            
            elif item.get("type") == "MENU":
                if item[1].text != "none":
                    menu.add_item().menu(item[0].text, text=item[1].text, icon=item[2].text)
                else:
                    menu.add_item().menu(item[0].text, icon=item[2].text)
            
            elif item.get("type") == "PROP":
                path = item[0].text
                
                #print(path[path.rfind(".")+1:])
                
                if item[1].text != "none":
                    menu.add_item().prop(eval(path[:path.rfind(".")]), path[path.rfind(".")+1:], text=item[1].text, icon=item[2].text, expand=eval(item[3].text), slider=eval(item[4].text), toggle=eval(item[5].text), icon_only=eval(item[6].text), event=eval(item[7].text), full_event=eval(item[8].text), emboss=eval(item[9].text))
                else:
                    menu.add_item().prop(eval(path[:path.rfind(".")]), path[path.rfind(".")+1:], icon=item[2].text, expand=eval(item[3].text), slider=eval(item[4].text), toggle=eval(item[5].text), icon_only=eval(item[6].text), event=eval(item[7].text), full_event=eval(item[8].text), emboss=eval(item[9].text))
        
        menu.add_item().separator()

        op = menu.add_item()
        op.operator_context = 'INVOKE_DEFAULT'
        op.operator("view3d.custom_menu_editor", text="Edit Custom Menu")
        
        #message = lambda x, y: errmsg(x, errors)
        
        if errors:
            context.window_manager.popup_menu(message, title=error_str, icon='ERROR')
        
class CustomMenuEditor(bpy.types.Operator):
    bl_label = "Custom Menu Editor"
    bl_idname = "view3d.custom_menu_editor"
    bl_options = {'REGISTER'}
    
    def check(self, context):
        return True       
    
    def draw(self, context):
        ui = Menu(self)
        scn = context.scene
        
        ui.add_item().prop(scn, "CustomMenuItemType")
        ui.add_item().separator()
        
        
        if scn.CustomMenuItemType == "OP":
            ui.add_item().label("Path:")
            ui.current_item.prop(scn, "CustomMenuItemPath", icon_only=True)
            ui.current_item.operator_context = 'INVOKE_DEFAULT'
            ui.current_item.operator("view3d.search_op_list_menu", text="", icon="LONGDISPLAY")
            ui.current_item.operator_context = 'EXEC_DEFAULT'
            ui.add_item().prop(scn, "CustomMenuOperatorArgs")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item().label("Insert After:")
            ui.current_item.prop(scn, "CustomMenuItemList")
            ui.add_item().separator()
            
        elif scn.CustomMenuItemType == "SEP":
            ui.add_item().label("Insert After:")
            ui.current_item.prop(scn, "CustomMenuItemList")
            ui.add_item().separator()
            
        elif scn.CustomMenuItemType == "LAB":
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item().label("Insert After:")
            ui.current_item.prop(scn, "CustomMenuItemList")
            ui.add_item().separator()
            
        elif scn.CustomMenuItemType == "MENU":
            ui.add_item().label("Path:")
            ui.current_item.prop(scn, "CustomMenuItemPath", icon_only=True)
            ui.current_item.operator_context = 'INVOKE_DEFAULT'
            ui.current_item.operator("view3d.search_menu_list_menu", text="", icon="LONGDISPLAY")
            ui.current_item.operator_context = 'EXEC_DEFAULT'
            #ui.add_item().prop(scn, "CustomMenuItemPath")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item().label("Insert After:")
            ui.current_item.prop(scn, "CustomMenuItemList")
            ui.add_item().separator()
            
        elif scn.CustomMenuItemType == "PROP":
            ui.add_item().prop(scn, "CustomMenuItemPath")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item()
            ui.current_item.prop(scn, "CustomMenuPropExpand")
            ui.current_item.prop(scn, "CustomMenuPropSlider")
            ui.current_item.prop(scn, "CustomMenuPropToggle")
            ui.current_item.prop(scn, "CustomMenuPropIconOnly")
            ui.add_item()
            ui.current_item.prop(scn, "CustomMenuPropEvent")
            ui.current_item.prop(scn, "CustomMenuPropFullEvent")
            ui.current_item.prop(scn, "CustomMenuPropEmboss")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().separator()
             
        elif scn.CustomMenuItemType == "REM":
            ui.add_item().label("Remove Item:")
            ui.current_item.prop(scn, "CustomMenuItemRemList")
            ui.add_item().separator()
            
        if scn.CustomMenuItemType != "REM":
            ui.add_item().operator("view3d.save_custom_item")
        else:
            ui.add_item().operator("view3d.save_custom_item", text="Remove Item")
             
#        else:
#            ui.add_item().prop(scn, "CustomMenuItemPath")
#            ui.add_item().prop(scn, "CustomMenuItemName")
#            ui.add_item().prop(scn, "CustomMenuItemIcon")
#            ui.add_item().prop(scn, "CustomMenuItemList")
#            #ui.add_item().operator("view3d.add_custom_item_ok_button")
        
    def invoke(self, context, event):
        get_custom_item_list()
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        #called when ok button is pressed
        
        return {'FINISHED'}
    
class SaveCustomItem(bpy.types.Operator):
    bl_label = "Add Item"
    bl_idname = "view3d.save_custom_item"
    bl_options = {'REGISTER'}
    
    
    def execute(self, context):
        scn = context.scene
        global __location__
        global tree
        global cur_menu
        
        if scn.CustomMenuItemType != "REM":
            new_item = ET.Element('item')
            cur_menu.insert(int(scn.CustomMenuItemList), new_item)
        
        if scn.CustomMenuItemType == "OP":
            try:
                op_inst = eval("bpy.ops.{0}.get_instance".format(scn.CustomMenuItemPath))
            except:
                bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                message="Invalid Path: {0}".format(scn.CustomMenuItemPath))
                
                return {'CANCELLED'}
            
            new_item.set("type", "OP")
            
            path = ET.SubElement(new_item, "path")
            path.text = scn.CustomMenuItemPath
            name = ET.SubElement(new_item, "name")
            name.text = scn.CustomMenuItemName if scn.CustomMenuItemName else "none"
            icon = ET.SubElement(new_item, "icon")
            icon.text = scn.CustomMenuItemIcon if scn.CustomMenuItemIcon else "none"
            
            op_args = scn.CustomMenuOperatorArgs
            if op_args != '':
                def_args = get_arg_list(get_arg_string(scn.CustomMenuItemPath))
                custom_args = get_arg_list(scn.CustomMenuOperatorArgs)
                
                if custom_args == 'ERROR':
                    bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                    message="Invalid Arguments for Item {0}".format(path.text))
                        
                    return {'CANCELLED'}
                
                for key, val in custom_args.items():
                    if not key in def_args:
                        bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                        message="Invalid Arguments for Item {0}".format(path.text))
                        
                        return {'CANCELLED'}
                    
                    if def_args[key] == val:
                        del custom_args[key]
                    #op_string = str(op_inst)
                    
                    #opkwarg_string = op_string[op_string.find("(")+1:op_string.find(")", -1)]
                    #opkwarg_list = opkwarg_string.replace(",", "")
                    #opkwarg_list = opkwarg_list.split(" ")
                    #opkwarg_list = [opkwarg.split("=")[0] for opkwarg in opkwarg_list]
                    #print(str(opkwarg_list))
                    
                    #if arg_text not in opkwarg_list:
                        #bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                        #message="Invalid Arguments for Item {0}".format(path.text))
                        
                        #return {'CANCELLED'}
                    #exec("op.{0} = {1}".format(arg_text, val_text))
                    #except:
                        #bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                        #message="Invalid Arguments for Item {0}".format(path.text))
                        
                        #return {'CANCELLED'}
                #print(["=".join(x) for x in list(custom_args.items())])
                
                if ["=".join(x) for x in list(custom_args.items())]:
                    arg_item = ET.SubElement(new_item, "arg")
                    arg_item.text = ';'.join(list(custom_args.keys()))
                    arg_val_item = ET.SubElement(new_item, "arg_val")
                    arg_val_item.text = ';'.join(list(custom_args.values()))
                else:
                    arg = ET.SubElement(new_item, "arg")
                    arg.text = "none"
                    arg_val = ET.SubElement(new_item, "arg_val")
                    arg_val.text = "none"
                
            else:
                arg = ET.SubElement(new_item, "arg")
                arg.text = "none"
                arg_val = ET.SubElement(new_item, "arg_val")
                arg_val.text = "none"
                
            
        elif scn.CustomMenuItemType == "SEP":
            new_item.set("type", "SEP")
            new_item.text = ""
            
        elif scn.CustomMenuItemType == "LAB":
            new_item.set("type", "LAB")
            
            name = ET.SubElement(new_item, "name")
            name.text = scn.CustomMenuItemName if scn.CustomMenuItemName else "none"
            icon = ET.SubElement(new_item, "icon")
            icon.text = scn.CustomMenuItemIcon if scn.CustomMenuItemIcon else "none"
            
        elif scn.CustomMenuItemType == "MENU":
            if scn.CustomMenuItemPath == "__required__":
                bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                message="Invalid Path: {0}".format(scn.CustomMenuItemPath))
                
                return {'CANCELLED'}
            
            new_item.set("type", "MENU")
            
            path = ET.SubElement(new_item, "path")
            path.text = scn.CustomMenuItemPath
            name = ET.SubElement(new_item, "name")
            name.text = scn.CustomMenuItemName if scn.CustomMenuItemName else "none"
            icon = ET.SubElement(new_item, "icon")
            icon.text = scn.CustomMenuItemIcon if scn.CustomMenuItemIcon else "none"
            
        elif scn.CustomMenuItemType == "PROP":
            if scn.CustomMenuItemPath == "__required__":
                bpy.ops.view3d.send_report('INVOKE_DEFAULT', \
                message="Invalid Path: {0}".format(scn.CustomMenuItemPath))
                
                return {'CANCELLED'}
            
            new_item.set("type", "PROP")
            
            path = ET.SubElement(new_item, "path")
            path.text = scn.CustomMenuItemPath
            name = ET.SubElement(new_item, "name")
            name.text = scn.CustomMenuItemName if scn.CustomMenuItemName else "none"
            icon = ET.SubElement(new_item, "icon")
            icon.text = scn.CustomMenuItemIcon if scn.CustomMenuItemIcon else "none"
            
            expand = ET.SubElement(new_item, "expand")
            expand.text = str(scn.CustomMenuPropExpand)
            slider = ET.SubElement(new_item, "slider")
            slider.text = str(scn.CustomMenuPropSlider)
            toggle = ET.SubElement(new_item, "toggle")
            toggle.text = str(scn.CustomMenuPropToggle)
            icononly = ET.SubElement(new_item, "icononly")
            icononly.text = str(scn.CustomMenuPropIconOnly)
            event = ET.SubElement(new_item, "event")
            event.text = str(scn.CustomMenuPropEvent)
            fullevent = ET.SubElement(new_item, "fullevent")
            fullevent.text = str(scn.CustomMenuPropFullEvent)
            emboss = ET.SubElement(new_item, "emboss")
            emboss.text = str(scn.CustomMenuPropEmboss)
            
        elif scn.CustomMenuItemType == "REM":
            cur_menu.remove(cur_menu[int(scn.CustomMenuItemRemList)])
            
        format_xml(root)
        
        tree.write(os.path.join(__location__, "CustomMenu.xml"))
        
        scn.CustomMenuItemName = ""
        scn.CustomMenuItemIcon = "NONE"
        scn.CustomMenuItemPath = ""
        scn.CustomMenuOperatorArgs = ""
        
        scn.CustomMenuPropExpand = False
        scn.CustomMenuPropSlider = False
        scn.CustomMenuPropToggle = False
        scn.CustomMenuPropIconOnly = False
        scn.CustomMenuPropEvent = False
        scn.CustomMenuPropFullEvent = False
        scn.CustomMenuPropEmboss = True
        
        # regenerate custom item lists
        get_custom_item_list()
        
        return {'FINISHED'}
    
class SearchableOperatorListMenu(bpy.types.Operator):
    bl_label = "Searchable Operator List Menu"
    bl_idname = "view3d.search_op_list_menu"
    bl_property = "op_enum"
    
    op_enum = bpy.props.EnumProperty(items=get_operator_list)
    
    def invoke(self, context, event):
        fill_operator_list()
        
        wm = context.window_manager
        wm.invoke_search_popup(self)
        
        return {'FINISHED'}
    
    def execute(self, context):
        context.scene.CustomMenuItemPath = self.op_enum
        #bpy.ops.view3d.add_custom_item_xml.check(context)
        
        return{'FINISHED'}
    
class SearchableMenuListMenu(bpy.types.Operator):
    bl_label = "Searchable Menu List Menu"
    bl_idname = "view3d.search_menu_list_menu"
    bl_property = "op_enum"
    
    op_enum = bpy.props.EnumProperty(items=get_menu_list)
    
    def invoke(self, context, event):
        fill_menu_list()
        
        wm = context.window_manager
        wm.invoke_search_popup(self)
        
        return {'FINISHED'}
    
    def execute(self, context):
        context.scene.CustomMenuItemPath = self.op_enum
        #bpy.ops.view3d.add_custom_item_xml.check(context)
        
        return{'FINISHED'}
        
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register(): 
    read_xml()
    
    set_prop("EnumProperty", 
                    "bpy.types.Scene.CustomMenuItemType",
                    name = "",
                    items=[('OP','Add An Operator', 'Operator'), ('SEP', 'Add A Separator', 'Separator'), ('LAB', 'Add A Label', 'Label'), ('MENU', 'Add A Menu', 'Menu'), ('PROP', 'Add A Property', 'Property'), ('REM', 'Remove An Item', 'Remove')])
                    
    iconlist = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].\
               enum_items.keys()
    icons = []
    for value, icon in enumerate(iconlist):
        if icon in ["NONE", "BLANK1"]:
            icons.append((icon, icon, icon, icon, int(value)))
        else:
            icons.append((icon, "", icon, icon, int(value)))
    set_prop("EnumProperty", 
                "bpy.types.Scene.CustomMenuItemIcon",
                name = "Icon",
                items = icons)
    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuItemName", 
                    name="Name")
    
    bpy.types.Scene.CustomMenuItemPath = bpy.props.StringProperty(name="Path",
                    default="__required__",
                    update=update_args)
                    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuOperatorArgs", 
                    name="Args")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropExpand", 
                    default=False,
                    name="Expand")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropSlider", 
                    default=False, 
                    name="Slider")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropToggle", 
                    default=False, 
                    name="Toggle")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropIconOnly", 
                    default=False, 
                    name="IconOnly")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropEvent", 
                    default=False, 
                    name="Event")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropFullEvent", 
                    default=False, 
                    name="FullEvent")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropExpand", 
                    default=False, 
                    name="Expand")
    
    set_prop("BoolProperty", 
                    "bpy.types.Scene.CustomMenuPropEmboss", 
                    default=True, 
                    name="Emboss")
    
    # create the global hotkey
    wm = bpy.context.window_manager
    modes = ['3D View', 'Timeline', 'Graph Editor', 'Dopesheet', 'NLA Editor',
             'Image', 'Sequencer', 'Clip', 'Node Editor', 'Logic Editor', 'Console']
    for mode in modes:
        km = wm.keyconfigs.active.keymaps[mode]
        kmi = km.keymap_items.new('wm.call_menu', 'MIDDLEMOUSE', 'PRESS', alt=True)
        kmi.properties.name = 'view3d.custom_menu'
        addon_keymaps.append((km, kmi))
    
def unregister():
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
