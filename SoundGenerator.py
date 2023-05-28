import dawdreamer as daw
import numpy as np
import ProjectStructs
from scipy.io import wavfile


class SoundGenerator:
    def generate_project(project: ProjectStructs.Project, output_path: str):
        engine = daw.RenderEngine(project.sample_rate, 128)

        graph = []

        for instrument_key in project.instruments:
            # Load Instrument from project, from its state
            daw_instrument = engine.make_plugin_processor(
                project.instruments[instrument_key].name,
                project.instruments[instrument_key].instrument_path)
            
            
            daw_instrument.open_editor()

            if (project.instruments[instrument_key].save_state_path != ""):
                daw_instrument.load_state(
                    project.instruments[instrument_key].save_state_path)

            graph.append((daw_instrument, []))

            for note_key in project.instruments[instrument_key].notes:
                key_time: float = 0
                while (key_time < project.runtime):
                    
                    # (MIDI note, velocity, start, duration)
                    daw_instrument.add_midi_note(project.instruments[instrument_key].notes[note_key].key,
                                                 project.instruments[instrument_key].notes[note_key].velocity,
                                                 key_time,
                                                 project.instruments[instrument_key].notes[note_key].duration)

                    key_time += 1 / project.instruments[instrument_key].notes[note_key].frequency

            for effect_key in project.instruments[instrument_key].effects:
                daw_effect = engine.make_plugin_processor(
                    project.instruments[instrument_key].effects[effect_key].name, project.instruments[instrument_key].effects[effect_key].effect_path)
                
                daw_effect.open_editor()

                graph.append((daw_effect, [daw_instrument.get_name()]))

        engine.load_graph(graph)
        engine.render(project.runtime)

        audio = engine.get_audio()
        wavfile.write(output_path, project.sample_rate, audio.transpose())
        


# if __name__ == "__main__":
#     test_project = ProjectStructs.Project("Test_Project", 100)
#     test_instrument = ProjectStructs.Instrument(
#         "Surge", "assets\Surge XT.vst3")
#     test_effect = ProjectStructs.Effect("SuperMassive", "assets\ValhallaSupermassive.vst3")
#     test_note1 = ProjectStructs.Note("Key 1", 30, 5, 100, 3)
#     test_note2 = ProjectStructs.Note("Key 1", 20, 2.5, 100, 2)

#     test_project.instruments.update({test_instrument.name: test_instrument})
#     test_project.instruments[test_instrument.name].notes.update(
#         {test_note1.name: test_note1})
#     test_project.instruments[test_instrument.name].notes.update(
#         {test_note2.name: test_note2})
#     test_project.instruments[test_instrument.name].effects.update({test_effect.name: test_effect})

#     SoundGenerator.generate_project(test_project, "eggs.wav")