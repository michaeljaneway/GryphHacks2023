from manim import *
from manim.opengl import *
import numpy as np
from ProjectStructs import *

BLACK = "#343434"
SLATE = "#a2a2a2"
WHITE = "#ece6e2"

W = config.frame_width
H = config.frame_height
config.background_color = BLACK


class AnimRenderScene(ThreeDScene):
    def load_project(self, project: Project):
        self.project = project

    def construct(self):
        self.renderer.background_color = BLACK

        Time = ValueTracker()

        mobject_list = []

        instrument_dict: Dict[str, Instrument] = self.project.getInstruments()

        for instrument_key in instrument_dict:
            note_dict: Dict[str,
                            Note] = instrument_dict[instrument_key].getNotes()

            for note_key in note_dict:
                note = note_dict[note_key]

                note_VGroup = VGroup()

                note_freq = note.getFrequency()
                note_len = 1 + (note.getKey() / 127) * 4
                note_grav = note_len * pow(note_freq * 2 * PI, 2)

                # W value
                ang_freq = np.sqrt(note_grav/note_len)

                note_VGroup.add(Circle(radius=0.2, fill_opacity=1))

                note_VGroup.add(Line(UP * note_len, note_VGroup[0].get_center()).set_color(WHITE))

                note_VGroup.add(Dot(fill_opacity=0).move_to(note_VGroup[0].shift(ORIGIN)))

                note_VGroup[1].add_updater(
                    lambda m: m.set_angle(
                        np.cos(ang_freq * Time.get_value()) - PI / 2
                    )
                )

                note_VGroup[0].add_updater(
                    lambda m: m.move_to(note_VGroup[1].get_end()))

                self.play(FadeIn(note_VGroup[2]), run_time=0.0)

                note_VGroup[2].add_updater(
                    lambda m: m.move_to(note_VGroup[0].get_center()))

                note_VGroup.add(VMobject().start_new_path(note_VGroup[2].get_center()).set_stroke(
                    color=[WHITE, BLACK]).set_sheen_direction(UP))

                note_VGroup[3].add_updater(
                    lambda m, dt: m.shift(DOWN * 0.25 * dt).add_points_as_corners(
                        [note_VGroup[2].get_center()]
                    )
                )

                mobject_list.append(note_VGroup)

        self.add(*mobject_list)

        def simulate(sim_time):
            self.play(
                Time.animate.increment_value(sim_time),
                rate_func=linear,
                run_time=sim_time,
            )

        simulate(self.project.getRuntime())
