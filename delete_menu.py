from .Utils.core import *

# adds a context sensitive delete menu 
class DeleteMenu(bpy.types.Menu):
    bl_label = "Delete"
    bl_idname = "MESH_MT_context_delete_menu"

    @classmethod
    def poll(self, context):
        if get_mode() == 'EDIT':
            return True
        else:
            return False

    def init(self):
        sel_verts_num, sel_edges_num, sel_faces_num = get_selected()
        
        if sel_verts_num and not sel_edges_num and not sel_faces_num:
            selected = "verts"
            
        elif sel_verts_num and sel_edges_num and not sel_faces_num:
            selected = "edges"
            
        elif sel_verts_num and sel_edges_num and sel_faces_num:
            selected = "faces"
            
        else:
            selected = "none"
            
        return selected

    def draw(self, context):
        menu = Menu(self)
        selected = self.init()

        if selected == "none":
            menu.add_item().label("Nothing to Delete")
            return
        
        elif selected == "verts":
            self.draw_verts(menu)
            
        elif selected == "edges":
            self.draw_edges(menu)
            
        else:
            self.draw_faces(menu)

    def draw_verts(self, menu):
        prop = menu.add_item().operator("mesh.delete", "Verts", icon='VERTEXSEL')
        prop.type = 'VERT'
        
        menu.add_item().operator("mesh.dissolve_verts", icon='SNAP_VERTEX')
        menu.add_item().operator("mesh.dissolve_limited", icon='STICKY_UVS_LOC')

    def draw_edges(self, menu):
        prop = menu.add_item().operator("mesh.delete", "Verts", icon='VERTEXSEL')
        prop.type = 'VERT'
        prop = menu.add_item().operator("mesh.delete", "Edges", icon='EDGESEL')
        prop.type = 'EDGE'
        prop = menu.add_item().operator("mesh.delete", "Only Edges & Faces", icon='SPACE2')
        prop.type = 'EDGE_FACE'

        menu.add_item().separator()

        menu.add_item().operator("mesh.dissolve_verts", icon='SNAP_VERTEX')
        menu.add_item().operator("mesh.dissolve_edges", icon='SNAP_EDGE')

        menu.add_item().separator()

        menu.add_item().operator("mesh.dissolve_limited", icon='STICKY_UVS_LOC')

        menu.add_item().separator()

        menu.add_item().operator("mesh.delete_edgeloop", icon='BORDER_LASSO')
        menu.add_item().operator("mesh.edge_collapse", icon='UV_EDGESEL')

    def draw_faces(self, menu):
        prop = menu.add_item().operator("mesh.delete", "Verts", icon='VERTEXSEL')
        prop.type = 'VERT'
        prop = menu.add_item().operator("mesh.delete", "Edges", icon='EDGESEL')
        prop.type = 'EDGE'
        prop = menu.add_item().operator("mesh.delete", "Faces", icon='FACESEL')
        prop.type = 'FACE'
        prop = menu.add_item().operator("mesh.delete", "Only Edges & Faces", icon='SPACE2')
        prop.type = 'EDGE_FACE'
        prop = menu.add_item().operator("mesh.delete", "Only Faces", icon='UV_FACESEL')
        prop.type = 'ONLY_FACE'

        menu.add_item().separator()

        menu.add_item().operator("mesh.dissolve_verts", icon='SNAP_VERTEX')
        menu.add_item().operator("mesh.dissolve_edges", icon='SNAP_EDGE')
        menu.add_item().operator("mesh.dissolve_faces", icon='SNAP_FACE')

        menu.add_item().separator()

        menu.add_item().operator("mesh.dissolve_limited", icon='STICKY_UVS_LOC')

        menu.add_item().separator()

        menu.add_item().operator("mesh.delete_edgeloop", icon='BORDER_LASSO')
        menu.add_item().operator("mesh.edge_collapse", icon='UV_EDGESEL')
        
### ------------ New hotkeys and registration ------------ ###

addon_keymaps = []

def register():

    # create the global menu hotkey
    wm = bpy.context.window_manager
    #km = wm.keyconfigs.active.keymaps.new(name='Mesh', space_type='EMPTY')
    km = wm.keyconfigs.active.keymaps['Mesh']
    kmi = km.keymap_items.new('wm.call_menu', 'X', 'PRESS')
    kmi.properties.name = 'MESH_MT_context_delete_menu'
    addon_keymaps.append((km, kmi))

def unregister():
     # remove keymaps when add-on is deactivated
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()
