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
    "name": "VSE Strip Time Data Panel",
    "category": "Development",
    "author": "Adam Morris, tin2tin",
    "blender": (2, 80, 0),
}

def draw(self, context):
    from bpy.utils import smpte_from_frame

    layout = self.layout
    layout.use_property_split = False
    layout.use_property_decorate = False

    scene = context.scene
    frame_current = scene.frame_current
    strip = context.active_sequence_strip

    is_effect = isinstance(strip, bpy.types.EffectSequence)

    # Get once.
    frame_start = strip.frame_start
    frame_final_start = strip.frame_final_start
    frame_final_end = strip.frame_final_end
    frame_final_duration = strip.frame_final_duration
    frame_offset_start = strip.frame_offset_start
    frame_offset_end = strip.frame_offset_end

    length_list = (
        str(frame_start),
        str(frame_final_end),
        str(frame_final_duration),
        str(frame_offset_start),
        str(frame_offset_end),
    )

    if not is_effect:
        length_list = length_list + (
            str(strip.animation_offset_start),
            str(strip.animation_offset_end),
        )
    max_length = max(len(x) for x in length_list) + 2
    max_factor = (1.9 - max_length) / 30

    layout.enabled = not strip.lock
    layout.active = not strip.mute
    col = layout.box()
    if strip.type == "SCENE":
        col = col.column(align=True)
        strip_scene = scene.sequence_editor.active_strip.scene.name
        frame_original_start = bpy.data.scenes[str(strip_scene)].frame_start
        frame_original_frame = frame_current - (frame_start + frame_offset_start)
        frame_original = (
            frame_original_start + frame_offset_start + frame_original_frame
        )
        scene = strip.scene

        split = col.split(factor=0.52 + max_factor, align=True)
        split.alignment = "RIGHT"
        split.label(text="Original Frame")
        split = split.split(factor=0.8 + max_factor, align=True)
        split.label(text="%14s" % smpte_from_frame(frame_original))
        split.alignment = "RIGHT"
        split.label(text=str(frame_original) + "    ")

        if scene:
            sta = scene.frame_start
            end = scene.frame_end

            split = col.split(factor=0.52 + max_factor, align=True)
            split.alignment = "RIGHT"
            split.label(text="Start")
            split = split.split(factor=0.8 + max_factor, align=True)
            split.label(text="%14s" % smpte_from_frame(sta))
            split.alignment = "RIGHT"
            split.label(text=str(sta) + "    ")

            split = col.split(factor=0.52 + max_factor, align=True)
            split.alignment = "RIGHT"
            split.label(text="End")
            split = split.split(factor=0.8 + max_factor, align=True)
            split.label(text="%14s" % smpte_from_frame(end))
            split.alignment = "RIGHT"
            split.label(text=str(end) + "    ")

            split = col.split(factor=0.52 + max_factor, align=True)
            split.alignment = "RIGHT"
            split.label(text="Duration")
            split = split.split(factor=0.8 + max_factor, align=True)
            split.label(text="%14s" % smpte_from_frame(end - sta))
            split.alignment = "RIGHT"
            split.label(text=str(end - sta) + "    ")


def register():
    bpy.types.SEQUENCER_PT_time.append(draw)
    bpy.app.handlers.frame_change_pre.append(draw)


def unregister():
    bpy.types.SEQUENCER_PT_time.remove(draw)


if __name__ == "__main__":
    register()
