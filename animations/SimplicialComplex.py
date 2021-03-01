from manimlib.imports import *
import numpy as np
from manim_reveal import SlideScene

# import manimtda
from manimtda.complex import *

class SimplicialComplex(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):
        triangles = get_triangles()

        tri1 = [triangles[i] for i in range(16) if i not in (5, 10)]

        X0 = create_0skel(tri1, color=BLACK)
        X1 = create_1skel(tri1, color=BLACK)
        X2 = create_2skel(tri1, color=BLACK)

        self.play(
            ShowCreation(X0),
        )
        self.slide_break()

        self.play(
            ShowCreation(X1),
        )
        self.slide_break()
        self.play(
            ShowCreation(X2)
        )
        # self.play(
        #     FadeOut(X0),
        #     FadeOut(X1),
        #     run_time=0.1
        # )
        #
        # rad = 2.5
        # vshift=-0.5
        # hshift=-0.5
        # shift = np.array([4, 0, 0])
        # scale = np.array([[1, 0, 0.00], [0, 1, 0.00], [0, 0, 0]])
        # curve = np.array([[0.04, -0.03, 0], [-0.03, 0.05, 0], [0, 0, 0]])
        # # to_manifold(p, shift=shift, scale=scale, curve=curve)
        #
        # self.play(
        #     X2.apply_function,
        #     lambda p: to_sphere(p, rad=rad, shift=shift, hshift=hshift, vshift=vshift),
        #     run_time=3,
        # )
        #
        #
        # subcpx = [triangles[i] for i in (5, 10)]
        # S2 = create_2skel(subcpx, color=RED)
        #
        # self.play(
        #     ShowCreation(S2)
        # )
        #
        # self.play(
        #     S2.apply_function,
        #     lambda p: to_sphere(p, rad=rad, shift=shift, hshift=hshift, vshift=vshift),
        #     run_time=3,
        # )
        #
        # # S2.color = BLUE
        # # S2.init_colors().set_fill(BLUE, opacity=0.5)
        # self.play(
        #     S2.set_color,
        #     BLUE
        # )
        #
        # self.wait(2)
