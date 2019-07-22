from ..Utils.core import *
from .common import *

def draw_texture_paint(menu, context):
    ipaint = context.tool_settings.image_paint
    
    if context.image_paint_object and not ipaint.detect_data():
        if ipaint.missing_uvs or ipaint.missing_materials or ipaint.missing_texture:
            menu.add_item().label(text="Missing Data", icon='ERROR')
            menu.add_item().operator_menu_enum("paint.add_texture_paint_slot", "type", icon='ADD', text="Add Texture Paint Slot")
            return
        
        elif ipaint.missing_stencil:
            menu.add_item().label(text="Missing Data", icon='ERROR')
            menu.add_item().prop(ipaint, "use_stencil_layer", text="Mask")
            menu.add_item().operator("view3d.new_mask_image")
            menu.add_item().separator()
            menu.add_item().menu("VIEW3D_MT_tools_menu", text="  Tools", icon_value=get_active_tool_icon(context))
            return
    
    
    menu.add_item().menu("VIEW3D_MT_tools_menu", text="  Tools", icon_value=get_active_tool_icon(context))
    
    if not ipaint.brush:
        return
    
    menu.add_item().separator()
    
    if ipaint.brush.image_tool in {'DRAW', 'FILL'} and \
        ipaint.brush.blend not in {'ERASE_ALPHA', 'ADD_ALPHA'}:
        menu.add_item().operator(ColorPickerPopup.bl_idname, icon="COLOR")
    
    if ipaint.brush.image_tool not in {'FILL'}:
        menu.add_item().menu(BrushRadiusMenu.bl_idname)
        
    menu.add_item().menu(BrushStrengthMenu.bl_idname)
    
    if ipaint.brush.image_tool in {'MASK'}:
        menu.add_item().menu(BrushWeightMenu.bl_idname, text="Mask Value")
        
    if ipaint.brush.image_tool in {'SOFTEN'}:
        menu.add_item().prop(ipaint.brush, "sharp_threshold", text=PIW+"Sharp Threshold")
    
    menu.add_item().separator()
    
    if ipaint.brush.image_tool in {'DRAW'}:
        menu.add_item().menu(BrushModeMenu.bl_idname, text="Blend")
        
    if ipaint.brush.image_tool in {'SOFTEN'}:
        menu.add_item().menu(DirectionMenu.bl_idname)
        menu.add_item().menu(BlurMode.bl_idname)
    
    menu.add_item().separator()
    
    if ipaint.brush.image_tool in {'MASK'} or ipaint.stencil_image:
        menu.add_item().prop(ipaint, "use_stencil_layer", text="Mask")
    
    if ipaint.brush.image_tool in {'DRAW', 'CLONE', 'MASK'}:
        menu.add_item().prop(ipaint.brush, "use_accumulate")
        
    menu.add_item().prop(ipaint.brush, "use_alpha")
    menu.add_item().prop(ipaint.brush, "use_gradient")



class BlurMode(bpy.types.Menu):
    bl_label = "Blur Mode"
    bl_idname = "VIEW3D_MT_blur_mode"
    
    def draw(self, context):
        menu = Menu(self)
        path = "tool_settings.image_paint.brush.blur_mode"
        
        menu.add_item().label(text="Blur Mode")
        menu.add_item().separator()
        
        # add the menu items
        for item in context.tool_settings.image_paint.brush.bl_rna.properties['blur_mode'].enum_items:
            menuprop(menu.add_item(), item.name, item.identifier, path,
                     icon='RADIOBUT_OFF',
                     disable=True, 
                     disable_icon='RADIOBUT_ON')


class FlipColorsTex(bpy.types.Operator):
    bl_label = "Flip Colors"
    bl_idname = "view3d.flip_colors_tex"
    
    def execute(self, context):
        try:
            bpy.ops.paint.brush_colors_flip()
        except:
            pass
        
        return {'FINISHED'}


class NewMaskImage(bpy.types.Operator):
    '''Add a new mask image'''
    bl_label = "Add New Mask Image"
    bl_idname = "view3d.new_mask_image"
    
    def modal(self, context, event):
        if self.start:
            bpy.ops.image.new('INVOKE_DEFAULT')
            self.start = False
            
        if len(bpy.data.images.items()) > len(self.old_images):
            new_image = list(set(bpy.data.images.items()).difference(self.old_images))[0][1]
            context.tool_settings.image_paint.stencil_image = new_image
            return {'FINISHED'}
        
        if event.value not in ['MOUSEMOVE', 'RELEASE', 'NOTHING']:
            return {'CANCELLED'}
        
        return {'RUNNING_MODAL'}
    
    def execute(self, context):
        self.start = True
        self.old_images = bpy.data.images.items()
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
        
