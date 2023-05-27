import dawdreamer as daw
import numpy as np
import ProjectStructs


class SoundGenerator:
    def generate_project(project: ProjectStructs.Project, output_path: str):
        engine = daw.RenderEngine(SAMPLE_RATE, BUFFER_SIZE)

        
        
        for instrument in project.instruments:
            pass


if __name__ == "__main__":
    pass