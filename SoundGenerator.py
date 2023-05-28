import dawdreamer as daw
import numpy as np
import ProjectStructs
from scipy.io import wavfile


class SoundGenerator:
    def generate_project(project: ProjectStructs.Project, output_path: str):
        engine = daw.RenderEngine(project.sample_rate, 128)

        graph = []

        inst_count = 0
        effect_count = 0

        for instrument_key in project.instruments:
            # Load Instrument from project, from its state
            daw_instrument = engine.make_plugin_processor(
                project.instruments[instrument_key].name+str(inst_count),
                project.instruments[instrument_key].instrument_path)

            inst_count += 1

            daw_instrument.open_editor()

            if (project.instruments[instrument_key].save_state_path != ""):
                daw_instrument.load_state(
                    project.instruments[instrument_key].save_state_path)

            graph.append((daw_instrument, []))

            for note_key in project.instruments[instrument_key].notes:
                key_time: float = 0
                frequency_duration = 1 / \
                    project.instruments[instrument_key].notes[note_key].frequency

                while (key_time < project.runtime):
                    # (MIDI note, velocity, start, duration)
                    daw_instrument.add_midi_note(project.instruments[instrument_key].notes[note_key].key,
                                                 project.instruments[instrument_key].notes[note_key].velocity,
                                                 key_time,
                                                 project.instruments[instrument_key].notes[note_key].duration)

                    key_time += frequency_duration

            for effect_key in project.instruments[instrument_key].effects:
                daw_effect = engine.make_plugin_processor(
                    project.instruments[instrument_key].effects[effect_key].name + str(effect_count), project.instruments[instrument_key].effects[effect_key].effect_path)

                effect_count += 1

                daw_effect.open_editor()

                graph.append((daw_effect, [daw_instrument.get_name()]))
                
        print(graph)

        engine.load_graph(graph)
        engine.render(project.runtime)

        audio = engine.get_audio()
        wavfile.write(output_path, project.sample_rate, audio.transpose())
