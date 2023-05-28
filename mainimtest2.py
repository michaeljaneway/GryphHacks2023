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

        freq1 = 2
        freq2 = 3
        
        L1 = 3

        # Setup
        a = Circle(radius=0.2, fill_opacity=1)
        b = Circle(radius=0.2, fill_opacity=1)
        
        l1 = Line(UP * L1, a.get_center()).set_color(WHITE)
        l2 = Line(UP * L1, b.get_center()).set_color(WHITE)

        paint1 = Dot(fill_opacity=0).move_to(a.shift(ORIGIN))
        paint2 = Dot(fill_opacity=0).move_to(b.shift(ORIGIN))

        # Physics
        t = ValueTracker()
        A1 = ValueTracker(0.4)

        l1.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(freq1 * t.get_value()) - PI / 2
            )
        )

        l2.add_updater(
            lambda m: m.set_angle(
                A1.get_value() * np.cos(freq2 * t.get_value()) - PI / 2
            )
        )

        a.add_updater(lambda m: m.move_to(l1.get_end()))
        b.add_updater(lambda m: m.move_to(l2.get_end()))

        paint1.add_updater(lambda m: m.move_to(a.get_center()))
        paint2.add_updater(lambda m: m.move_to(b.get_center()))
        trails = VGroup()

        def add_trail():
            self.play(FadeIn(paint1), FadeIn(paint2), run_time=0.4)

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

        self.add(trails, l1, l2, a, b)

        def simulate(time):
            self.play(
                t.animate.increment_value(time),
                trails[-1][0].animate.set_stroke(color=[BLACK, WHITE]),
                trails[-1][1].animate.set_stroke(color=[BLACK, WHITE]),
                rate_func=linear,
                run_time=time,
            )

        add_trail()
        simulate(10)


if __name__ == "__main__":
    scene = Test()
    scene.render()
