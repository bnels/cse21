from manim import *
from manim_reveal import SlideScene
from manimtda.linalg.shapes import *
from manimtda.utils import *

import sys
sys.path.append(".")

from factorizations import LEUPFact, PLEUFact, PUELFact, UELPFact

class Factorizations(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):
        title = Text("Factorizations",color=BLACK)
        title.shift(3 * UP)
        self.add(title)

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        put_on_arrow = lambda x, Ar: x.next_to(Ar,TOP,buff=SMALL_BUFF)

        scale = 0.5

        # matrix for LEUP
        A1 = Square(color=BLACK)
        # matrix for PUEL
        A2 = Square(color=BLACK)

        Grp(A1, A2).scale(scale)

        # anch1 = Mobject() # anchor for LEUP
        # anch2 = Mobject() # anchor for PUEL
        anch1 = Polygon((0,0,0)) # anchor for LEUP
        anch2 = Polygon((0,0,0)) # anchor for PUEL
        anch1.shift(1*UP)
        anch2.shift(1*DOWN)


        put_on_arrow(A1, anch1)
        put_on_arrow(A2, anch2)
        self.play(FadeIn(Grp(A1, A2)))

        self.slide_break()

        # factorize A1
        fact1=LEUPFact(A1, anch1, scale=scale)
        fact2=PUELFact(A2, anch2, scale=scale)
        self.play(*fact1.animations1(), *fact2.animations1())
        self.play(*fact1.animations2(), *fact2.animations2())

        self.wait(1);
