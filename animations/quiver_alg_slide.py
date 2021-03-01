from manimlib.imports import *
from manim_reveal import SlideScene
from manimtda.linalg.shapes import *
from manimtda.utils import *


class LEUPFact(VMobject):
    def __init__(self,A,Arr,**kwargs):
        self.L = Lmat(corner_radius=0.01)
        self.U = Umat(corner_radius=0.01)
        self.EL = ELmat(color=BLACK)
        self.P = Pmat(color=BLACK)

        lst = [self.L, self.EL, self.U, self.P]

        mats=Grp(*lst)
        mats.scale(0.2)
        mats.next_to(Arr,TOP,buff=SMALL_BUFF)
        self.P.next_to(A,RIGHT)

        VMobject.__init__(self, **kwargs)
        self.add(*lst)

        self.lst = lst
        self.Arr = Arr
        self.A = A

    def __call__(self):
        return self.lst

    def make_target(self):
        [Lt, ELt, Ut, Pt] = copy_objs(self.lst)
        Seq(Lt, ELt, Ut, Pt).anchor_position(1)
        Grp(Lt, ELt, Ut, Pt).next_to(self.Arr,TOP,buff=SMALL_BUFF)
        self.target=[Lt, ELt, Ut, Pt]

    def play_factorize(self,scene):
        self.make_target()
        scene.play(
            ShowCreation(self.L),
            ShowCreation(self.U),
            ShowCreation(self.P),
        )
        scene.play(
            *MoveTo(self.lst, self.target),
            FadeOut(self.A)
        )



class QuiverAlg(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    def construct(self):
        title = TextMobject("Quiver Algorithm",color=BLACK)
        title.shift(2.5 * UP)
        self.add(title)

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        # Make quiver
        tA = TexMobject("\\cdot",color=BLACK)
        tB = TexMobject("\\cdot",color=BLACK)
        tC = TexMobject("\\cdot",color=BLACK)

        tArr = TexMobject("\\xleftarrow{\\makebox[1cm]{}}",color=BLACK);
        tArr2 = tArr.copy()
        put_on_arrow =lambda x,Ar: x.next_to(Ar,TOP,buff=SMALL_BUFF)

        # Position elements of quiver
        Grp(tA,tArr,tB,tArr2,tC).scale(2)
        Seq(tA,tArr,tB,tArr2,tC).anchor_position(2)

        # Add quiver
        self.play(FadeIn(Grp(tA,tArr,tB,tArr2,tC)))
        self.play()
        self.slide_break()

        # create two matrices and put on arrows
        A = Square(color=BLACK)
        A2 = Square(color=BLACK)
        Grp(A,A2).scale(0.2)
        put_on_arrow(A,tArr)
        put_on_arrow(A2,tArr2)
        self.play(FadeIn(Grp(A,A2)))
        self.slide_break()

        # factorize A1
        fact1=LEUPFact(A,tArr)
        fact1.play_factorize(self)
        self.slide_break()

        # Matrix pass U,P
        [L,EL,U,P] = fact1()
        with the_target_of(L,EL,U,P,A2) as (Lt,ELt,Ut,Pt,A2t):
            Seq(Ut,Pt,A2t)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)

            Seq(Lt,ELt)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
        self.slide_break()

        #Multiply UPA2
        with the_target_of(U,P,A2) as [Ut,Pt,A2t]:
            put_on_arrow(A2t,tArr2)
            Ut.move_to(A2t)
            Pt.move_to(A2t)
        self.play(
             FadeOut(U),
             FadeOut(P)
        )
        self.slide_break()
        lel1 = Seq(L,EL)

        # Factorize A2
        fact2=LEUPFact(A2,tArr2)
        fact2.play_factorize(self)
        self.slide_break()

        # Matrix pass UP
        [L,EL,U,P] = fact2()
        self.play(
             FadeOutAndShift(U,2*RIGHT),
             FadeOutAndShift(P,2*RIGHT)
        )
        lel2 = Seq(L,EL)
        with the_target_of(L,EL) as (Lt,ELt):
            Seq(Lt,ELt)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)
        self.slide_break()

        ###--BACKWARD PASS--

        #Matrix pass L2
        L1,EL1 = lel1()
        L2,EL2 = lel2()
        with the_target_of(L1,EL1,L2,EL2) as (L1t,EL1t,L2t,EL2t):
            Seq(L1t,EL1t,L2t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
            Seq(EL2t)\
                .anchor_position(0)\
                .next_to(tArr2,TOP,buff=SMALL_BUFF)
        self.slide_break()

        # commute
        with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
            Seq(L1t,L2t,EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
        self.slide_break()

        # multiply
        with the_target_of(L1,EL1,L2) as (L1t,EL1t,L2t):
            Seq(L1t,EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)
            L2t.move_to(L1t)

        self.play(
             FadeOut(L2)
        )
        self.slide_break()

        # matrix pass L1
        self.play(
             FadeOutAndShift(L1,2*LEFT),
        )
        with the_target_of(EL1) as [EL1t]:
            Seq(EL1t)\
                .anchor_position(0)\
                .next_to(tArr,TOP,buff=SMALL_BUFF)

        self.wait(1);
