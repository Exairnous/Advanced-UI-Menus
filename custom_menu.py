from .Utils.core import *

__location__ = os.path.dirname(os.path.realpath(__file__)) + "/Utils"

custom_item_list = []

def read_file():
    custom_menu_file = open(os.path.join(__location__, "CustomMenu.txt"), "r")
    global custom_item_list
    
    for line in custom_menu_file:
        custom_item_list.append(eval(line))
    
def get_item_list(context):
    item_list = []
    area = context.space_data.type
    for item in custom_item_list: 
            if item['area'] == area:
                if item['area'] == 'VIEW_3D':
                    mode = get_mode()
                    if item['mode'] == mode:
                        item_list = item['items']
                
                else:
                    item_list = item['items']
    
    return item_list
        

#class CustomMenuOperator(bpy.types.Operator):
    #bl_label = "Right Click Operator"
    #bl_idname = "view3d.right_click_operator"
        
    #def execute(self, context):
        #bpy.ops.object.mode_set()
        #return {'FINISHED'}
                
#class OperatorListMenuOperator(bpy.types.Operator):
#    bl_label = "List Menu Operator"
#    bl_idname = "view3d.op_list_menu_operator"
#    
#    def modal(self, context, event):
#        current_time = time.time()
#        
#        if event.value == 'ENTER':
#            return {'FINISHED'}
#    
#        else:
#            if context.scene.CustomMenuItemPath != self.searchstring:
#                bpy.ops.wm.call_menu(name="view3d.operator_list_menu")
#                self.searchstring = context.scene.CustomMenuItemPath
#            return {'RUNNING_MODAL'}
#    
#    
#    def execute(self, context):
#        self.searchstring = context.scene.CustomMenuItemPath
#        bpy.ops.wm.call_menu(name="view3d.operator_list_menu")
#        context.window_manager.modal_handler_add(self)
#        
#        return {'RUNNING_MODAL'}
    

class CustomMenu(bpy.types.Menu):
    bl_label = "Custom"
    bl_idname = "view3d.custom_menu"
    
    def draw(self, context):
        menu = Menu(self)
        global custom_item_list
       
        item_list = get_item_list(context)

        

        for item in item_list:
            if item['type'] == "SEP":
                menu.add_item().separator()
            elif item['type'] == "LAB":
                menu.add_item().label(item['name'])
            elif item['type'] == "OP":
                if item['name'] != "none":
                    op = menu.add_item().operator(item['path'], item['name'], icon=item['icon'])
                    if item['arg'] != "none":
                        exec("op.{0} = {1}".format(item['arg'], item['arg_val']))
                else:
                    op = menu.add_item().operator(item['path'], icon=item['icon'])
                    if item['arg'] != "none":
                        exec("op.{0} = {1}".format(item['arg'], item['arg_val']))
            elif item['type'] == "MENU":
                if item['name'] != "none":
                    menu.add_item().menu(item['path'], text=item['name'], icon=item['icon'])
                else:
                    menu.add_item().menu(item['path'], icon=item['icon'])

        menu.add_item().menu("view3d.add_custom_item_menu")

class AddCustomItemMenu(bpy.types.Menu):
    bl_label = "Add Custom Item"
    bl_idname = "view3d.add_custom_item_menu"
    
    
    def draw(self, context):
        menu = Menu(self)
        
        
        types = [('OP', 'Operator'),
                 ('SEP', 'Separator'),
                 ('LAB', 'Label'),
                 ('MENU', 'Menu'),
                 #('PROP', 'Property'),
                 ('REM', 'Remove Item')]
        
        for item in types:
            op = menu.add_item().operator("view3d.pre_add_custom_item", text=item[1])
            op.item_type = item[0]
            
class AddCustomItemOperator(bpy.types.Operator):
    bl_label = "Pre Add Custom Item"
    bl_idname = "view3d.pre_add_custom_item"
    bl_options = {'REGISTER'}
    
    item_type = set_prop("EnumProperty", 
                    "bpy.types.Scene.CustomMenuItemType",
                    name = "CustomMenuItemType",
                    items=[('OP','Operator', 'Add A Operator'), ('SEP', 'Separator', 'Add A Separator'), ('LAB', 'Label', 'Add A Label'), ('MENU', 'Menu', 'Add A Menu'), ('PROP', 'Property', 'Add A Property'), ('REM', 'Remove', 'Remove An Item')])
    
    def execute(self, context):
        context.scene.CustomMenuItemType = self.item_type
        
        items = []
        newitems = []
        item_list = get_item_list(context)
        propname = ""
        
        iconlist = bpy.types.UILayout.bl_rna.functions['prop'].parameters['icon'].\
        enum_items.keys()
        icons = []
        
        for value, icon in enumerate(iconlist):
            icons.append((icon, "", icon, icon, int(value)))
        
        for place, item in enumerate(item_list):
            if context.scene.CustomMenuItemType != "REM":
                place = place+1
                
            if item['type'] == "OP":
                name =  item['path']
                if item['name'] != "none":
                    name = item['name']
                items.append((str(place), name, item['path'].capitalize()))
                
            elif item['type'] == "LAB":
                items.append((str(place), item['name'].capitalize(), item['name'].capitalize()))
                
            elif item['type'] == "SEP":
                items.append((str(place), item['type'].capitalize(), item['type'].capitalize()))
                
            elif item['type'] == "MENU":
                name =  item['path']
                if item['name'] != "none":
                    name = item['name']
                items.append((str(place), name, item['path'].capitalize()))
                    
        if context.scene.CustomMenuItemType != "REM":
            items.insert(0, (str(0), "First", "First"))
            propname = "Insert After"
        
            
        for item in reversed(items):
            newitems.append(item)
        
                
        items = newitems
                   
        set_prop("EnumProperty", 
                "bpy.types.Scene.CustomMenuItemList",
                name = propname,
                items = items)
        
        set_prop("EnumProperty", 
                "bpy.types.Scene.CustomMenuItemIcon",
                name = "Icon",
                items = icons)
        
        bpy.ops.view3d.add_custom_item()
        return {'FINISHED'}

class AddCustomItemWindow(bpy.types.Operator):
    bl_label = "Add Custom Item"
    bl_idname = "view3d.add_custom_item"
    bl_options = {'REGISTER'}
    
    def draw(self, context):
        ui = Menu(self)
        scn = context.scene
        
        if scn.CustomMenuItemType == "OP":
            ui.add_item().label("Add An Operator")
            ui.add_item().prop(scn, "CustomMenuItemPath")
            #ui.add_item().menu("view3d.operator_list_menu")
            #ui.add_item().operator("view3d.op_list_menu_operator")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().operator("view3d.add_custom_item_ok_button")
            
        elif scn.CustomMenuItemType == "SEP":
            ui.add_item().label("Add A Separator")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().operator("view3d.add_custom_item_ok_button")
            
        elif scn.CustomMenuItemType == "LAB":
            ui.add_item().label("Add A Label")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().operator("view3d.add_custom_item_ok_button")
            
        elif scn.CustomMenuItemType == "MENU":
            ui.add_item().label("Add A Menu")
            ui.add_item().prop(scn, "CustomMenuItemPath")
            ui.add_item().prop(scn, "CustomMenuItemName")
            ui.add_item().prop(scn, "CustomMenuItemIcon")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().operator("view3d.add_custom_item_ok_button")
             
        elif scn.CustomMenuItemType == "REM":
            ui.add_item().label("Remove")
            ui.add_item().prop(scn, "CustomMenuItemList")
            ui.add_item().operator("view3d.add_custom_item_ok_button")
             
#        else:
#            ui.add_item().prop(scn, "CustomMenuItemPath")
#            ui.add_item().prop(scn, "CustomMenuItemName")
#            ui.add_item().prop(scn, "CustomMenuItemIcon")
#            ui.add_item().prop(scn, "CustomMenuItemList")
#            #ui.add_item().operator("view3d.add_custom_item_ok_button")
        
    def execute(self, context):
        return context.window_manager.invoke_popup(self, width=250)
    
class OperatorListMenu(bpy.types.Menu):
    bl_label = "Operator List"
    bl_idname = "view3d.operator_list_menu"
    
    def get_operator_list(self):
        op_strings = []
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
                    op_strings.append((op_name, op_path))
                    
        
        return op_strings
    
    def draw(self, context):
        menu = Menu(self)
        op_list = self.get_operator_list()
        
        menu.alignment = 'CENTER'
        menu.add_item().prop(context.scene, "CustomMenuItemPath")
        for item in op_list:
            if eval("bpy.ops.{0}.poll()".format(item[1])):
                if context.scene.CustomMenuItemPath.lower() in item[0].lower():
                    menu.add_item().operator(item[1], item[0])

class OkButtonOperator(bpy.types.Operator):
    bl_label = "OK"
    bl_idname = "view3d.add_custom_item_ok_button"
    bl_options = {'REGISTER'}
    
    
    def execute(self, context):
        scn = context.scene
        global __location__
        global custom_item_list
        
        #custom_menu_file = open(os.path.join(__location__, "CustomMenu.txt"), "r")
        #custom_items = custom_menu_file.readlines()
        #custom_menu_file.close()
        
        if scn.CustomMenuItemType == "OP":
            self.SaveOp(context, scn)
        elif scn.CustomMenuItemType == "SEP":
            self.SaveSep(context, scn)
        elif scn.CustomMenuItemType == "LAB":
            self.SaveLab(context, scn)
        elif scn.CustomMenuItemType == "MENU":
            self.SaveMenu(context, scn)
        elif scn.CustomMenuItemType == "REM":
            self.SaveRem(context, scn)
        
        savestring = ""
        
        for item in custom_item_list:
            savestring = savestring + str(item) + "\n"
        
        custom_menu_file = open(os.path.join(__location__, "CustomMenu.txt"), "w")
        custom_menu_file.write(savestring)
        
        scn.CustomMenuItemName = ""
        scn.CustomMenuItemIcon = "NONE"
        scn.CustomMenuItemValue = ""
        scn.CustomMenuItemPath = ""
        scn.CustomMenuItemPlace = ""
        
        return {'FINISHED'}
    
    def SaveOp(self, context, scn):
        try:
            op = re.search('bpy.ops.(.*)\(', scn.CustomMenuItemPath).group(1)
        except:
            try:
                op = re.search('(.*)\(', scn.CustomMenuItemPath).group(1)
            except:
                return "Failed"
        #op = scn.CustomMenuItemPath
        arg = re.search('\((.*)\)', scn.CustomMenuItemPath).group(1)
        item_list = get_item_list(context)
        
        if arg:
            arg = arg.split("=")
        else:
            arg = ("none", "none")


        if scn.CustomMenuItemName:
            name = scn.CustomMenuItemName
        else:
            name = "none"

        if scn.CustomMenuItemIcon:
            icon = scn.CustomMenuItemIcon
        else:
            icon = "NONE"
            
        newitem = {'type':scn.CustomMenuItemType,
                               'path':op,
                               'name':name,
                               'icon':icon,
                               'arg':arg[0],
                               'arg_val':arg[1]}
            
        if item_list != []:
            item_list.insert(int(scn.CustomMenuItemList), newitem)
        else:
            if context.space_data.type == 'VIEW_3D':
                custom_item_list.append({'area':context.space_data.type, 'mode':get_mode(), 'items':[newitem]})
            else:
                custom_item_list.append({'area':context.space_data.type, 'items':[newitem]})

    def SaveLab(self, context, scn):
        item_list = get_item_list(context)
        name = scn.CustomMenuItemName

        newitem = {'type':scn.CustomMenuItemType,
                               'name':scn.CustomMenuItemName}
        
        if item_list != []:
            item_list.insert(int(scn.CustomMenuItemList), newitem)
        else:
            if context.space_data.type == 'VIEW_3D':
                custom_item_list.append({'area':context.space_data.type, 'mode':get_mode(), 'items':[newitem]})
            else:
                custom_item_list.append({'area':context.space_data.type, 'items':[newitem]})

    def SaveSep(self, context, scn):
        item_list = get_item_list(context)
        newitem = {'type':scn.CustomMenuItemType}
        
        if item_list != []:
            item_list.insert(int(scn.CustomMenuItemList), newitem)
        else:
            if context.space_data.type == 'VIEW_3D':
                custom_item_list.append({'area':context.space_data.type, 'mode':get_mode(), 'items':[newitem]})
            else:
                custom_item_list.append({'area':context.space_data.type, 'items':[newitem]})

    def SaveMenu(self, context, scn):
        path = scn.CustomMenuItemPath
        item_list = get_item_list(context)
        
        if scn.CustomMenuItemName:
            name = scn.CustomMenuItemName
        else:
            name = "none"

        if scn.CustomMenuItemIcon:
            icon = scn.CustomMenuItemIcon
        else:
            icon = "NONE"

        newitem = {'type':scn.CustomMenuItemType,
                               'path':path,
                               'name':name,
                               'icon':icon}

        if item_list != []:
            item_list.insert(int(scn.CustomMenuItemList), newitem)
        else:
            if context.space_data.type == 'VIEW_3D':
                custom_item_list.append({'area':context.space_data.type, 'mode':get_mode(), 'items':[newitem]})
            else:
                custom_item_list.append({'area':context.space_data.type, 'items':[newitem]})

    def SaveRem(self, context, scn):
        item_list = get_item_list(context)
        del item_list[int(scn.CustomMenuItemList)]
        
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():
    read_file()
#    custom_menu_file = open(os.path.join(__location__, "CustomMenu.txt"), "r")
#    global custom_item_list
#    for line in custom_menu_file:
#        custom_item_list.append(eval(line))
    
    # create the Test property
    #AddCustomItemOperator.item_type = set_prop("EnumProperty", 
    #                "bpy.types.Scene.CustomMenuItemType",
    #                name = "CustomMenuItemType",
    #                items=[('OP','Operator', 'Add A Operator'), ('SEP', 'Separator', 'Add A Separator'), ('LAB', 'Label', 'Add A Label'), ('MENU', 'Menu', 'Add A Menu'), ('PROP', 'Property', 'Add A Property'), ('REM', 'Remove', 'Remove An Item')])
    
    #set_prop("StringProperty", 
                    #"bpy.types.Scene.CustomMenuItemIcon", 
                    #name="Icon")
    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuItemValue", 
                    name="Value")
    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuItemName", 
                    name="Name")
    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuItemPath", 
                    name="Path")
    
    set_prop("StringProperty", 
                    "bpy.types.Scene.CustomMenuItemPlace", 
                    name="Place")
    
    # create the global hotkey
    wm = bpy.context.window_manager
    modes = ['3D View', 'Timeline', 'Graph Editor', 'Dopesheet', 'NLA Editor',
             'Image', 'Sequencer', 'Clip', 'Node Editor', 'Logic Editor', 'Console']
    #for space_type, name in [['VIEW_3D', '3D View'], ['TIMELINE', 'Timeline'], ['GRAPH_EDITOR', 'Graph Editor'], ['DOPESHEET_EDITOR', 'Dopesheet'],
                       #['NLA_EDITOR', 'NLA Editor'], ['IMAGE_EDITOR', 'Image'], ['SEQUENCE_EDITOR', 'Sequencer'],
                       #['CLIP_EDITOR', 'Clip'], ['NODE_EDITOR', 'Node Editor'], ['LOGIC_EDITOR', 'Logic Editor'], ['CONSOLE', 'Console']]:
        #km = wm.keyconfigs.addon.keymaps.new(name=name, space_type=space_type)
    for mode in modes:
        km = wm.keyconfigs.active.keymaps[mode]
        kmi = km.keymap_items.new('wm.call_menu', 'MIDDLEMOUSE', 'PRESS', alt=True)
        kmi.properties.name = 'view3d.custom_menu'
        addon_keymaps.append((km, kmi))
    
def unregister():
    bpy.types.Scene.Custom_Items = "Not At All!"
    # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
