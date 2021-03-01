from manimlib.imports import *
import numpy as np
from manim_reveal import SlideScene

# import manimtda
from manimtda.linalg import *

class LEL(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):

        title = TexMobject(r"E_L L = \tilde{L}E_L", color=BLACK).shift(2*UP)
        self.play(
            Write(title),
        )
        self.slide_break()

        L = Lmat().shift(1.125*RIGHT)
        EL = ELmat(color=BLACK).shift(1.125*LEFT)
        self.play(
            ShowCreation(L),
            ShowCreation(EL)
        )
        self.slide_break()

        self.play(
            ApplyMethod(L.shift, 2.25*LEFT),
            ApplyMethod(EL.shift, 2.25*RIGHT)
        )
