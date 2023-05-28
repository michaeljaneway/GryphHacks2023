from manim import *
from manim.camera.camera import Camera
import numpy as np
from typing import *


class AnimationGenerator(Scene):
        
    
    def construct(self):
        # Creating Dots
        num_of_dots = 120

        dots: List[Dot] = []

        space_between = 7.5 / num_of_dots

        for i in range(num_of_dots):
            dots.append(Dot([6, 3.75 - space_between * i, 0], radius=0.1))
            
        self.add(*dots)
        
        # Animating Dots
        
        directions = []

        for dot in dots:
            directions.append([-dot.get_center()[0], 0, 0])
            dot.set_color(utils.color.random_color())
            
        animations = []
        
        i = 1
        
        for dot, direction in zip(dots, directions):
            animations.append(ApplyMethod(dot.shift, direction, run_time=i))
            i+= 0.1

        
        self.play(*animations)

if __name__ == "__main__":
    scene = AnimationGenerator()
    scene.add_sound("eggs.wav")
    scene.render()
