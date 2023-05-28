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

        self.Time = ValueTracker()

        # i = instrument, j = note
        self.note_values: List[List[Dict[str, float]]] = []

        self.instrument_dict: Dict[str,
                                   Instrument] = self.project.getInstruments()

        self.generate_vals()
        self.add_notes()

        def simulate(sim_time):
            self.play(
                self.Time.animate.increment_value(sim_time),
                rate_func=linear,
                run_time=sim_time,
            )

        simulate(self.project.getRuntime())

    def generate_vals(self):
        for i, instrument_key in enumerate(self.instrument_dict):
            note_dict: Dict[str,
                            Note] = self.instrument_dict[instrument_key].getNotes()

            self.note_values.append([])

            for j, note_key in enumerate(note_dict):
                note = note_dict[note_key]

                self.note_values[i].append([])

                note_freq = note.getFrequency()
                note_len = 1 + (note.getKey() / 127) * 4
                note_grav = note_len * pow(note_freq * 2 * PI, 2)

                # W value
                ang_freq = np.sqrt(note_grav/note_len)

                self.note_values[i][j] = {
                    "freq": note_freq,
                    "len": note_len,
                    "grav": note_grav,
                    "ang_freq": ang_freq,
                }

    def add_notes(self):
        for i, instrument_key in enumerate(self.instrument_dict):
            note_dict: Dict[str,
                            Note] = self.instrument_dict[instrument_key].getNotes()

            for j, note_key in enumerate(note_dict):
                vals = self.note_values[i][j]

                note_circle = Circle(radius=0.2, fill_opacity=1)
                note_line = Line(start= UP * vals["len"], end=note_circle.get_center()).set_color(WHITE)
                
                note_circle.add(note_line)

                note_line.add_updater(lambda m: m.set_angle(
                    np.cos(vals["ang_freq"] * self.Time.get_value()) - PI / 2
                ))

                note_circle.add_updater(
                    lambda m: m.move_to(note_line.get_end()))

                self.add(note_line, note_circle)
