Description:
    Menus to aid the user and increase the speed of interacting with blender's UI.

Installation Instructions:
    Download the script then unpack and copy the folder advanced_ui_menus into your addons folder.
    Open Blender and go to the addons tab in User Preferences.
    Enable the script. 

Shortcuts:
    Brush menu = V (works in: Sculpt mode, Vertex Paint mode, Weight Paint mode, Texture Paint Mode, Particle Edit Mode)
    Curve menu = W (works in: Sculpt mode, Vertex Paint mode, Weight Paint mode, Texture Paint Mode)
    Custom menu = Alt-MiddleMouse
    Delete menu = X
    Dyntopo menu = Ctrl-D Tap for toggle(on/off), hold for menu
    Layers window = M - Tap for set visible layers, hold for move objects to layers
    Manipulator = Ctrl-Space - Tap for toggle(on/off), hold for menu
    Mesh Selection menu = Ctrl-Tab
    Mesh Extrude = E - Tap for extrude, hold for menu
    Mode menu = Tab - Tap for toggle(last/edit), hold for menu
    Pivot Point menu = .
    Proportional = O - Tap for toggle(last/off), hold for menu
    Proportional falloff = Shift-O
    Shading mode = Z - Tap for toggle(last/wireframe), hold for menu
    Snapping = Shift-Tab - Tap for toggle(on/off), hold for menu
    Stroke menu = E (works in: Sculpt mode, Vertex Paint mode, Weight Paint mode, Texture Paint Mode)
    Symmetry menu = Alt-S (works in: Sculpt mode, Texture Paint Mode)
    Texture menu = R (works in: Sculpt mode, Vertex Paint mode, Texture Paint Mode)
    View menu = Q 

Custom Menu Tutorial:
  The Custom Menu is a menu that you can customize with Operators, Separators, Labels, and other
  menus as you see fit. This is a alpha release and as such is not the easiest to use or the most
  feature complete, but should still be useful to people. Also if it is to reach it's true potential
  I will probably need to work closely with the blender UI team. Now onto the tutorial.
  To add an Operator open the menu and go down to Add Custom Item, select Operator. A window will
  come up, type the path to the operator(you can find it by turning on python tooltips and then
  hovering your mouse over a button or menu entry in the ui) in the Path field,
  e.g. bpy.ops.mesh.vertices_smooth(). Type something into the Name field if you want the item to
  have a custom name. If you want the item to have an Icon simply select it from the Icon list. The
  last field on the window controls where the item is placed in the menu; the item will be placed
  directly under the item you specify from the list. Finally press the OK button to add the item.
  The rest of the items are added in a similar fashion, however as far as I know there is no easy
  way to find the path for menus if you want to add them(tooltips only show up for them in some cases).
  If you want to remove an item simply go to Add Custom Item, select Remove Item, and then select
  the item you wish removed and press OK.
