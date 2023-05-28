from manim import *
from manim.opengl import *
import numpy as np

BLACK = "#343434"
SLATE = "#a2a2a2"
WHITE = "#ece6e2"

W = config.frame_width
H = config.frame_height
config.background_color = BLACK

class Test(ThreeDScene):
    def construct(self):
        
        self.renderer.background_color = BLACK
        
        ceil_len = 3
        w11 = 6
        w21 = w11 * 1.1  # w2 > w1
        w12 = 10
        w22 = w12 * 1.5  # w2 > w1
        
        p1 = 0
        p2 = 0
        L = 3
        T1 = 16 * PI / (w11 + w21)
        T2 = 16 * PI / (w12 + w22)
        
        # Setup
        a = Circle(radius=0.2, fill_opacity=1)
        b = Circle(radius=0.2, fill_opacity=1).shift(UP*0.2)
        l1 = Line(a.get_center() + UP * L, a.get_center()).set_color(WHITE)
        l2 = Line(b.get_center() + UP * L, b.get_center()).set_color(WHITE)
        
        ceil = VGroup(
            DashedLine(
                start=ceil_len * LEFT,
                end=(ceil_len) * RIGHT,
                dashed_ratio=0.4,
                dash_length=0.2,
                color=BLACK,
            ).shift(l1.get_start()[1] * UP)
        )

        paint1 = Dot(fill_opacity=0).move_to(a.shift(ORIGIN))
        paint2 = Dot(fill_opacity=0).move_to(b.shift(ORIGIN))

        # Physics
        t = ValueTracker()
        A1 = ValueTracker(0.4)
        A2 = ValueTracker(0)
        
        l1.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(w11 * t.get_value() + p1)
                + A2.get_value() * np.cos(w21 * t.get_value() + p2)
                - PI / 2
            )
        )
        
        l2.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(w12 * t.get_value() + p1)
                - A2.get_value() * np.cos(w22 * t.get_value() + p2)
                - PI / 2
            )
        )
        
        a.add_updater(lambda m: m.move_to(l1.get_end()))
        b.add_updater(lambda m: m.move_to(l2.get_end()))

        paint1.add_updater(lambda m: m.move_to(a.get_center()))
        paint2.add_updater(lambda m: m.move_to(b.get_center()))
        trails = VGroup()

        def add_trail():
            self.play(FadeIn(paint1), FadeIn(paint2), run_time = 0.4)
            
            trails.add(
                VGroup(
                    VMobject()
                    .start_new_path(paint1.get_center())
                    .set_stroke(color=[WHITE, BLACK])
                    .set_sheen_direction(UP),
                    VMobject()
                    .start_new_path(paint2.get_center())
                    .set_stroke(color=[WHITE, BLACK])
                    .set_sheen_direction(UP),
                )
            )
            
            trails[-1][0].add_updater(
                lambda m, dt: m.shift(DOWN * 0.25 * dt).add_points_as_corners(
                    [paint1.get_center()]
                )
            )
            trails[-1][1].add_updater(
                lambda m, dt: m.shift(DOWN * 0.25 * dt).add_points_as_corners(
                    [paint2.get_center()]
                )
            )

        config = {"stroke_color": SLATE,
                  "stroke_width": 2, "stroke_opacity": 0.2}
        

        self.add(trails, l1, l2, ceil, a, b)

        def simulate(time):
            self.play(
                t.animate.increment_value(time),
                trails[-1][0].animate.set_stroke(color=[BLACK, WHITE]),
                trails[-1][1].animate.set_stroke(color=[BLACK, WHITE]),
                rate_func=linear,
                run_time=time,
            )

        add_trail()
        simulate(5 * T2)


if __name__ == "__main__":
    scene = Test()
    # scene.add_sound("eggs.wav")
    scene.render()
