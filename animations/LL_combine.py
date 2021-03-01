from manimlib.imports import *
import numpy as np
from manim_reveal import SlideScene

# import manimtda
from manimtda.linalg import *

class LLCombine(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):

        title = TexMobject(r"L L = L", color=BLACK).shift(2*UP)
        self.play(
            Write(title),
        )
        self.slide_break()

        L1 = Lmat().shift(1.125*RIGHT)
        L2 = Lmat().shift(1.125*LEFT)
        self.play(
            ShowCreation(L1),
            ShowCreation(L2)
        )
        self.slide_break()

        self.play(
            ApplyMethod(L1.shift, 1.125*LEFT),
            ApplyMethod(L2.shift, 1.125*RIGHT)
        )
