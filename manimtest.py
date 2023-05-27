from manim import *
import numpy as np
from typing import *


class AnimationGenerator(Scene):
    def construct(self):
        # Creating Dots
        num_of_dots = 120

        dots: List[Dot] = []

        space_between = 8 / num_of_dots

        for i in range(num_of_dots):
            dots.append(Dot([6, 4 - space_between * i, 0]))
            
        self.add(*dots)
        
        # Animating Dots
        
        directions = []

        for dot in dots:
            directions.append([-dot.get_center()[0], 0, 0])

        
        
        
        animations = []
        
        i = 1
        
        for dot, direction in zip(dots, directions):
            animations.append(ApplyMethod(dot.shift, direction, run_time=i))
            i+= 0.1

        
        self.play(*animations)

if __name__ == "__main__":
    scene = AnimationGenerator()
    scene.render()
