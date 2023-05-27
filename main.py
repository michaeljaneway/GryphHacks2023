from manim import *

# To open the movie after render.
from manim.utils.file_ops import open_file as open_media_file 

class DemoScene(Scene):
    def construct(self):
        box1 = Rectangle()
        self.add(box1)
        self.wait(20)


if __name__ == '__main__':
    scene = DemoScene()
    scene.render()