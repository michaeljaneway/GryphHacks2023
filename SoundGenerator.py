import dawdreamer as daw
import numpy as np
import ProjectStructs


class SoundGenerator:
    def generate_project(project: ProjectStructs.Project, output_path: str):
        engine = daw.RenderEngine(44100, 128)

        graph = []

        for instrument_key in project.instruments:
            # Load Instrument from project, from its state
            daw_instrument = engine.make_plugin_processor(
                project.instruments[instrument_key].name, 
                project.instruments[instrument_key].instrument_path)
            daw_instrument.load_state(
                project.instruments[instrument_key].save_state_path)

            for note_key in project.instruments[instrument_key].notes:
                key_time: float = 0
                while (key_time < project.time_length):
                    # (MIDI note, velocity, start, duration)
                    daw_instrument.add_midi_note(project.instruments[instrument_key].notes[note_key].key,
                                                 project.instruments[instrument_key].notes[note_key].velocity,
                                                 key_time,
                                                 project.instruments[instrument_key].notes[note_key].duration)

                    key_time += project.instruments[instrument_key].notes[note_key].frequency

            for effect_key in project.instruments[instrument_key].effects:
                pass


if __name__ == "__main__":
    test_project = ProjectStructs.Project()
    test_project.name = "Test_Project"

    SoundGenerator.generate_project(test_project, "eggs.wav")
