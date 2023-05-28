from manim import *
from manim.opengl import *
import numpy as np
from ProjectStructs import *

BLACK = "#050203"
WHITE = "#ece6e2"

W = config.frame_width
H = config.frame_height
config.background_color = BLACK


class AnimRenderScene(ThreeDScene):
    def load_project(self, project: Project, filepath):
        self.project = project
        self.filepath = filepath

    def construct(self):
        self.renderer.background_color = BLACK

        self.Time = ValueTracker()

        self.instrument_dict: Dict[str,
                                   Instrument] = self.project.getInstruments()
        self.add_notes()
        
        self.add_sound(self.filepath)

        def simulate(sim_time):
            self.play(
                self.Time.animate.increment_value(sim_time),
                rate_func=linear,
                run_time=sim_time,
            )

        simulate(self.project.getRuntime())

    def add_notes(self):
        for instrument_key in self.instrument_dict:
            note_dict: Dict[str,
                            Note] = self.instrument_dict[instrument_key].getNotes()

            for note_key in note_dict:
                note_freq = note_dict[note_key].getFrequency()
                note_len = 1 + (note_dict[note_key].getKey() / 127) * 4
                note_grav = note_len * pow(note_freq * 2 * PI, 2)

                # W value
                ang_freq = np.sqrt(note_grav/note_len)

                note_circle = Circle(radius=0.2, fill_opacity=1)
                note_line = Line(start=UP * 2, end=UP*2 - UP * note_len).set_color(WHITE)

                note_circle.add_updater(
                    lambda m, note_line=note_line: m.move_to(note_line.get_end()))

                note_line.add_updater(
                    lambda m, ang_freq=ang_freq: m.set_angle(np.sin(ang_freq * self.Time.get_value()) - PI / 2
                ))

                self.add(note_line, note_circle)


if __name__ == "__main__":
    test_project = Project("Test_Project", 10)
    test_instrument = Instrument("Surge")
    test_instrument.setInstrumentPath("assets\Surge XT.vst3")
    test_effect = Effect("SuperMassive")
    test_effect.setEffectPath("assets\ValhallaSupermassive.vst3")

    test_note1 = Note("Key 1", 30, 0.1, 100, 3)
    test_note2 = Note("Key 2", 20, 0.01, 100, 2)

    test_project.instruments.update({test_instrument.name: test_instrument})
    test_project.instruments[test_instrument.name].notes.update(
        {test_note1.name: test_note1})
    test_project.instruments[test_instrument.name].notes.update(
        {test_note2.name: test_note2})
    test_project.instruments[test_instrument.name].effects.update(
        {test_effect.name: test_effect})

    animator = AnimRenderScene(ThreeDCamera)
    animator.load_project(test_project)
    animator.render()
