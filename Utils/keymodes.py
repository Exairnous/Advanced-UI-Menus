from .core import *

# this is a list of keys to deactivate with a list of modes to deactivate them in
keymodes = [# key    any   shift  ctrl   alt   oskey               modes
            ['TAB', False, False, True, False, False, ['Object Non-modal', 'Mesh']],
            ['TAB', False, False, False, False, False, ['Object Non-modal']],
            ['TAB', False, True, False, False, False, ['3D View']], 
            ['TAB', False, True, True, False, False, ['3D View']],
            ['SPACE', False, False, True, False, False, ['3D View']],
            ['COMMA', False, False, False, False, False, ['3D View']],
            ['PERIOD', False, False, False, False, False, ['3D View']],
            ['D', False, False, True, False, False, ['Sculpt']],
            ['E', False, False, False, False, False, ['Mesh', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']],
            ['M', False, False, False, False, False, ['Object Mode']],
            ['O', False, False, False, False, False, ['Object Mode', 'Object Non-modal','Mesh','Curve','Metaball','Lattice','Particle']],
            ['O', False, True, False, False, False, ['Object Mode', 'Object Non-modal','Mesh','Curve','Metaball','Lattice','Particle']],
            ['R', False, False, False, False, False, ['Sculpt', 'Vertex Paint', 'Image Paint']],
            ['S', False, False, False, False, False, ['Sculpt']],
            ['V', False, False, False, False, False, ['Object Non-modal', 'Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']],
            ['W', False, False, False, False, False, ['Sculpt', 'Vertex Paint', 'Weight Paint', 'Image Paint']],
            ['X', False, False, False, False, False, ['Mesh']],
            ['Z', False, False, False, False, False, ['3D View']]
           ]


def opposingkeys(activation):  
    wm = bpy.context.window_manager
        
    # deactivate the opposing keys to prevent clashing and reactivate them on unregister
    # keymode is a list containing the mode and key you want changed
    for key in keymodes:
        # mode is the mode you want the key to be (de)activated for.
        for mode in key[6]:
            km = wm.keyconfigs.active.keymaps[mode]

            # this iterates through all the keys in the current 
            # hotkey layout and (de)activates the ones that
            # match the key we want to (de)activate
            for kmi in km.keymap_items:
                #print(kmi.type, "shift={0}".format(kmi.shift), "ctrl={0}".format(kmi.ctrl), "alt={0}".format(kmi.alt))
                if kmi.type == key[0] and kmi.any == key[1] \
                    and kmi.shift == key[2] and kmi.ctrl == key[3] \
                    and kmi.alt == key[4] and kmi.oskey == key[5]:
                                
                    # (de)activate the current key
                    kmi.active = activation
            