from manimlib.imports import *
import numpy as np
from manim_reveal import SlideScene

# import manimtda
from manimtda.linalg import *

def Lmat_Block():
    """
    return blocked L matrix for EL commutation
    """
    blocks = [
        ((np.array([-1, 1, 0]), np.array([-1, 0.3, 0]), np.array([-0.3, 0.3, 0])), BLUE), # L11
        ((np.array([-1, 0.3, 0]), np.array([-1, 0, 0]), np.array([-0.3, 0, 0]), np.array([-0.3, 0.3, 0])), ORANGE), # L21
        ((np.array([-0.3, 0.3, 0]), np.array([-0.3, 0, 0]), np.array([0, 0, 0])), RED), # L22
        ((np.array([0, 0, 0]), np.array([0, -1, 0]), np.array([1, -1, 0])), YELLOW_E), # L33
        ((np.array([-1, 0, 0]), np.array([-1, -1, 0]), np.array([-0.3, -1, 0]), np.array([-0.3, 0, 0])), YELLOW_C), # L31
        ((np.array([-0.3, 0, 0]), np.array([-0.3, -1, 0]), np.array([0, -1, 0]), np.array([0, 0, 0])), YELLOW_D), # L32

    ]
    poly = [Polygon(*verts, color=BLACK).set_fill(color, opacity=0.5).round_corners(0.01) for (verts, color) in blocks]
    Lverts = (np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        *poly,
        Square(color=BLACK),
    )

def Lmat_Block_Prod():
    """
    return blocked L matrix for EL commutation
    """
    blocks = [
        ((np.array([-1, 1, 0]), np.array([-1, 0.3, 0]), np.array([-0.3, 0.3, 0])), BLUE), # L11
        ((np.array([-1, 0, 0]), np.array([-1, -0.3, 0]), np.array([-0.3, -0.3, 0]), np.array([-0.3, 0, 0])), ORANGE), # L21
        ((np.array([-0.3, 0, 0]), np.array([-0.3, -0.3, 0]), np.array([0, -0.3, 0])), RED), # L22
    ]
    poly = [Polygon(*verts, color=BLACK).set_fill(color, opacity=0.5).round_corners(0.01) for (verts, color) in blocks]
    Lverts = (np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        *poly,
        Square(color=BLACK),
    )

def Lmat_Block2():
    """
    return blocked L matrix for EL commutation
    """
    blocks = [
        ((np.array([-1, 1, 0]), np.array([-1, 0.3, 0]), np.array([-0.3, 0.3, 0])), BLUE), # L11
        ((np.array([-1, 0, 0]), np.array([-1, -0.3, 0]), np.array([-0.3, -0.3, 0]), np.array([-0.3, 0, 0])), ORANGE), # L21
        ((np.array([0, 0, 0]), np.array([0, -0.3, 0]), np.array([0.3, -0.3, 0])), RED), # L22
    ]
    poly = [Polygon(*verts, color=BLACK).set_fill(color, opacity=0.5).round_corners(0.01) for (verts, color) in blocks]
    Lverts = (np.array([-1, -1, 0]), np.array([1, -1, 0]), np.array([-1, 1, 0]))
    return VGroup(
        *poly,
        Square(color=BLACK),
        Line(np.array([-1,1,0]), np.array([1,-1,0]),color=BLACK)
    )


class LEL_full(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):

        # title = TexMobject(r"E_L L = \tilde{L}E_L", color=BLACK).shift(2*UP)
        # self.play(
        #     Write(title),
        # )
        # self.slide_break()

        L = Lmat_Block().shift(1.125*RIGHT)
        EL = ELmat(color=BLACK).shift(1.125*LEFT)
        self.play(
            ShowCreation(L),
            ShowCreation(EL)
        )
        self.slide_break()

        LB = Lmat_Block_Prod()
        self.play(
            FadeOutAndShift(EL, direction=RIGHT),
            Transform(L[0], LB[0]),
            Transform(L[1], LB[1]),
            Transform(L[2], LB[2]),
            Transform(L[-1], LB[-1]),
            *[FadeOutAndShift(L[i], direction=LEFT) for i in [3,4,5]]
        )
        L = VGroup(L[0], L[1], L[2], L[-1]) # update L vgroup
        self.slide_break()


        L2 = Lmat_Block2().shift(1.125*LEFT)
        EL2 = ELmat(color=BLACK).shift(RIGHT)
        self.play(
            FadeInFrom(EL2, direction=LEFT),
            *[Transform(L[i], L2[i]) for i in range(4)],
            FadeInFrom(L2[-1], direction=RIGHT)
        )
        L = VGroup(L[0], L[1], L[2], L[3], L2[-1]) # update L vgroup
        self.slide_break()

        LB2 = Lmat_Block_Prod()
        self.play(
            FadeOutAndShift(EL2, direction=LEFT),
            *[Transform(L[i], LB2[i]) for i in range(4)],
            FadeOutAndShift(L[-1], direction=RIGHT)
        )
        self.wait()
