"""

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

### About This Script ###

When working with scene strips in the VSE, Blender by default doesn't
give any feedback as to which frame number of a scene strip is under
the playhead. Instead, it mostly displays information about the strip
in the context of the sequence, which isn't particularly useful.

Knowing the "real" frame number or timecode of a scene strip is vital
should you want make changes to the internal scene at the specific
frame beneath the playhead, or between a specific range of frames i.e.
the frames between the in and out point of the strip.

### Known Issues ###

- Deleting the selected scene strip throws up an error: The code needs
conditionals adding to to allow for this.

- Strips modified by the Speed Controller effect don't take the effect
into account: This is potentially something that could be added.

"""

import bpy
from bpy.utils import smpte_from_frame

bl_info = {
    'name': "VSE Strip Time Data Panel",
    'category': 'Development',
    'author': "Adam Morris, tin2tin",
    'blender': (2, 80, 0)
}

class RealFrameNumberDisplay(bpy.types.Panel):
    bl_label = "Strip Time Data"
    bl_idname = "VSE_strip_time_data"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'Strip'

    @classmethod
    def poll(cls, context):
        if context.scene and context.scene.sequence_editor and context.scene.sequence_editor.active_strip:
            return context.scene.sequence_editor.active_strip.type == 'SCENE'
        else:
            return False

    def draw(self, context):
        layout = self.layout

        scn = bpy.context.scene

        currentFrame = scn.frame_current
        stripStart = scn.sequence_editor.active_strip.frame_start
        stripOffset = scn.sequence_editor.active_strip.frame_offset_start
        frameOfStrip = currentFrame - (stripStart + stripOffset)
        stripScene = scn.sequence_editor.active_strip.scene.name
        realStripStart = bpy.data.scenes[str(stripScene)].frame_start
        realFrameNum = realStripStart + stripOffset + frameOfStrip

        row = layout.row()
        row.label(text="Frame Number")

        row = layout.row()
        row.label(text="Scene Frame: " + str(scn.frame_current), icon='SEQUENCE')

        row = layout.row()
        row.label(text="Strip Frame (internal): " + str(realFrameNum), icon='SCENE_DATA')

        row = layout.row()
        row.label(text="Strip Frame (selected): " + str(frameOfStrip), icon='SEQ_STRIP_DUPLICATE')

        row = layout.row()
        row.label(text="Time Code")

        row = layout.row()
        row.label(text="Scene Time: " + smpte_from_frame(scn.frame_current), icon='SEQUENCE')

        row = layout.row()
        row.label(text="Strip Time (internal): " + smpte_from_frame(realFrameNum), icon='SCENE_DATA')

        row = layout.row()
        row.label(text="Strip Time (selected): " + smpte_from_frame(frameOfStrip), icon='SEQ_STRIP_DUPLICATE')

    bpy.app.handlers.frame_change_pre.append(draw)

def register():
    bpy.utils.register_class(RealFrameNumberDisplay)

def unregister():
    bpy.utils.unregister_class(RealFrameNumberDisplay)

if __name__ == "__main__":
    register()
