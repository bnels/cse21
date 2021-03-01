from manim import *
from manim_reveal import SlideScene
from manimtda.linalg.shapes import *
from manimtda.utils import *



def EUmat(color=WHITE):
    return VGroup(
        Square(color=color),
        Line(np.array([-1,1,0]), np.array([-0.3,0.3,0]),color=color),
        Line(np.array([0,0.3,0]), np.array([0.3,0,0]),color=color)
    )

def EUhat(color=WHITE):
    EU = ELmat(color)
    EU.rotate(180*DEGREES,about_point=np.array([0,0,0]))
    return EU

def ELhat(color=WHITE):
    EL = EUmat(color)
    EL.rotate(180*DEGREES,about_point=np.array([0,0,0]))
    return EL


class EFact(VMobject):
    """
    Generic class for LEUP/PUEL etc. factorizations

    child classes should implement list order
    """
    def __init__(self,A,Arr,Emat,**kwargs):
        self.angle = kwargs.get("angle", 0.0)

        self.A = A

        self.L = Lmat(corner_radius=0.01)
        self.U = Umat(corner_radius=0.01)
        self.E = Emat(color=BLACK)
        self.P = Pmat(color=BLACK)

        lst = self._create_list()

        mats=Grp(*lst)
        scale = kwargs.get("scale", 0.2)
        self.scale=scale
        mats.scale(scale)
        mats.rotate(self.angle)
        mats.next_to(self.A,0,buff=SMALL_BUFF)
        P_loc = kwargs.get("P_loc", RIGHT)
        self.P.next_to(A,0)
        self.P.shift(self._rotate_loc(3*scale*P_loc))

        VMobject.__init__(self, **kwargs)
        self.add(*lst)

        self.lst = lst
        self.Arr = Arr


    def _rotate_loc(self, loc):
        ca = np.cos(self.angle)
        sa = np.sin(self.angle)
        return np.array([
            ca*loc[0] - sa*loc[1],
            sa*loc[0] + ca*loc[1],
            loc[2]
        ])

    def __call__(self):
        return self.lst

    def _create_list(self):
        """
        return list of matrices in order
        """
        pass

    def make_target(self):
        mats = copy_objs(self.lst)
        Seq(*mats).anchor_position(1,buff=self.scale*SMALL_BUFF)
        Grp(*mats).next_to(self.A,0,buff=SMALL_BUFF)
        Seq(*mats).rotate(self.angle)
        self.target=mats
        self.target_pos=[m.get_center() for m in mats]

    def animations1(self):
        return ShowCreation(self.L), ShowCreation(self.U), ShowCreation(self.P)

    def animations2(self):
        self.make_target()
        return (*MoveTo(self.lst, self.target), FadeOut(self.A))

    def play_factorize(self,scene, **kw):
        scene.play(
            *self.animations1(),
            **kw
        )
        scene.play(
            *self.animations2(),
            **kw
        )


class LEUPFact(EFact):
    def __init__(self,A,Arr,**kwargs):
        super().__init__(A, Arr, ELmat, P_loc=RIGHT, **kwargs)

    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.L, self.E, self.U, self.P]

class PLEUFact(EFact):
    def __init__(self, A, Arr, **kwargs):
        super().__init__(A, Arr, EUmat, P_loc=LEFT, **kwargs)

    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.P, self.L, self.E, self.U]


class PUELFact(EFact):
    def __init__(self, A, Arr, **kwargs):
        super().__init__(A, Arr, ELhat, P_loc=LEFT, **kwargs)

    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.P, self.U, self.E, self.L]

class UELPFact(EFact):
    def __init__(self, A, Arr, **kwargs):
        super().__init__(A, Arr, EUhat, P_loc=RIGHT, **kwargs)

    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.U, self.E, self.L, self.P]


class LUTypeFact(VMobject):
    """
    LQU factorization

    child classes should implement list order
    """
    def __init__(self,A,Arr,**kwargs):
        self.angle = kwargs.get("angle", 0.0)

        self.A = A

        self.L = Lmat(corner_radius=0.01)
        self.U = Umat(corner_radius=0.01)
        self.Q = Pmat(color=BLACK)

        lst = self._create_list()

        mats=Grp(*lst)
        scale = kwargs.get("scale", 0.2)
        self.scale=scale
        mats.scale(scale)
        mats.rotate(self.angle)
        mats.next_to(self.A,0,buff=SMALL_BUFF)

        VMobject.__init__(self, **kwargs)
        self.add(*lst)

        self.lst = lst
        self.Arr = Arr


    def _rotate_loc(self, loc):
        ca = np.cos(self.angle)
        sa = np.sin(self.angle)
        return np.array([
            ca*loc[0] - sa*loc[1],
            sa*loc[0] + ca*loc[1],
            loc[2]
        ])

    def __call__(self):
        return self.lst

    def _create_list(self):
        """
        return list of matrices in order
        """
        pass

    def make_target(self):
        mats = copy_objs(self.lst)
        Seq(*mats).anchor_position(1,buff=self.scale*SMALL_BUFF)
        Grp(*mats).next_to(self.A,0,buff=SMALL_BUFF)
        Seq(*mats).rotate(self.angle)
        self.target=mats
        self.target_pos=[m.get_center() for m in mats]

    def animations1(self):
        return ShowCreation(self.L), ShowCreation(self.Q), ShowCreation(self.U)

    def animations2(self):
        self.make_target()
        return (*MoveTo(self.lst, self.target), FadeOut(self.A))

    def play_factorize(self,scene, **kw):
        scene.play(
            *self.animations1(),
            **kw
        )
        scene.play(
            *self.animations2(),
            **kw
        )


class LQUFact(LUTypeFact):
    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.L, self.Q, self.U]

class UQLFact(LUTypeFact):
    def _create_list(self):
        """
        return list of matrices in order
        """
        return [self.U, self.Q, self.L]
