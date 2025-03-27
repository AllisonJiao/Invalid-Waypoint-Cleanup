bl_info = {
    "name": "Invalid Waypoint Cleanup",
    "blender": (2, 80, 0),
    "location": "Viewport > Right panel"
}

import bpy

from bpy.props import ( BoolProperty, PointerProperty )
from bpy.types import ( PropertyGroup )


def update_automatic_cleanup(self, context):
    if self.wpcu_automatic_cleanup:
        bpy.ops.object.set_automatic_cleanup('EXEC_DEFAULT')
    else:
        bpy.ops.object.set_manual_cleanup('EXEC_DEFAULT')

class WPCUPanel(bpy.types.Panel):
    bl_label = "Invalid Waypoint Cleanup"
    bl_idname = "VIEW3D_PT_invalid_waypoint_cleanup"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Waypoint"

    def draw(self, context):
        layout = self.layout
        wm = context.window_manager
        props = wm.wpcu_tool

        layout.prop(props, "wpcu_automatic_cleanup")
        layout.operator("object.set_automatic_cleanup")
        layout.operator("object.set_manual_cleanup")

# Property groups for UI
class PG_WPCUProperties(PropertyGroup):
    # Option for user to choose waypoint cleanup method
    wpcu_automatic_cleanup: BoolProperty(
        name = "Automatic Waypoint Cleanup",
        description = "Enable/disable automatic calculation of invalid waypoints",
        update = update_automatic_cleanup
    )

# Light casting method to find invalid waypoints
class WPCUAutomaticRemove(bpy.types.Operator):
    bl_idname = "object.set_automatic_cleanup"
    bl_label = "Auto Remove"
    bl_description = ("Automatically remove the invalid waypoints")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.object

        # Get the flight path and control points
        if obj.type == 'CURVE':
            curve = obj
        
        return {'FINISHED'}
    
# User manual remove the waypoints
class WPCUManualRemove(bpy.types.Operator):
    bl_idname = "object.set_manual_cleanup"
    bl_label = "Manual Remove"
    bl_description = ("Manually remove the invalid waypoints")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print(f"Placeholder")

        return {'FINISHED'}

classes = [
    WPCUPanel,
    PG_WPCUProperties,
    WPCUAutomaticRemove,
    WPCUManualRemove
]

def register():
    from bpy.utils import register_class
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.WindowManager.wpcu_tool = PointerProperty(type=PG_WPCUProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in classes:
        bpy.utils.unregister_class(cls)
    del bpy.types.WindowManager.wpcu_tool

if __name__ == "__main__":
    register()