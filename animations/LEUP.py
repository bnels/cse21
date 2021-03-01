from manimlib.imports import *
import numpy as np
from manim_reveal import SlideScene

# import manimtda
from manimtda.linalg import *

class LEUP(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):

        title = TexMobject("A = LE_L U P", color=BLACK).shift(2*UP)
        self.play(
            Write(title),
        )
        self.slide_break()

        A = Square(color=BLACK)
        self.play(
            ShowCreation(A)
        )
        self.slide_break()

        L = Lmat()
        U = Umat()
        EL = ELmat(color=BLACK)
        P = Pmat(color=BLACK).shift(2.25*RIGHT)
        self.play(
            ShowCreation(L),
            ShowCreation(U),
            ShowCreation(P),
        )

        self.play(
            FadeIn(EL),
            ApplyMethod(L.shift, 2.25*LEFT),
            ApplyMethod(U.shift, 2.25*RIGHT),
            ApplyMethod(P.shift, 2.25*RIGHT),
            FadeOut(A)
        )
