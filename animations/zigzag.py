from manim import *
from manim_reveal import SlideScene
from manimtda.linalg.shapes import *
from manimtda.utils import *
import numpy as np

import sys
sys.path.append(".")

from factorizations import LEUPFact, PLEUFact, PUELFact, UELPFact, LQUFact, UQLFact

config.background_color = "#F0F1EB"
config.video_slides_dir = "../video_slides"

class ZigzagForward(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
    #self.video_slides_dir = "../video_slides"

    def construct(self):
        # title = Text("Lefward-Initial Algorithm",color=BLACK)
        # title.shift(3.5 * UP)
        # self.add(title)

        matrix_scale = 0.15
        fast_kw = {"run_time": 0.5}

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        put_on_anchor = lambda x, anch: x.next_to(anch,0*(UP+RIGHT),buff=0).shift(0.35*UP)

        # create nodes
        nodes = Grp(*[Dot(color=BLACK) for i in range(8)])
        nodes.shift(3.5*UP)
        npos = []
        for i, n in enumerate(nodes):
            n.shift(1*i * DOWN)
            if i % 2 == 0:
                n.shift(1.5*LEFT)
                npos.append(n.get_center() + 2*matrix_scale*LEFT)
            else:
                n.shift(1.5*RIGHT)
                npos.append(n.get_center() + 2*matrix_scale*RIGHT)
            #print(n.get_arc_center())

        # create edges
        es = []
        esign = [] # keep track of edge directions
        angles = []
        eloc = []
        for i in range(len(nodes)-1):
            if i % 2 == 0:
                # left arrow
                src = nodes[i+1].get_arc_center()
                trg = nodes[i].get_arc_center()
                esign.append(1)
            else:
                # right arrow
                src = nodes[i].get_arc_center()
                trg = nodes[i+1].get_arc_center()
                esign.append(-1)
            es.append(Arrow(src,trg, color=BLACK))
            eloc.append((src + trg) / 2)
            diff = src - trg
            angles.append(np.arctan2(diff[1], diff[0]))

        edges = Grp(*es)
        self.play(FadeIn(nodes), FadeIn(edges), )

        #self.slide_break()

        # put a matrix over each edge
        As = Grp(*[Square(color=BLACK) for i in range(len(edges))])
        As.scale(matrix_scale)

        for i, A in enumerate(As):
            put_on_anchor(A, eloc[i])
            A.rotate(angles[i])

        self.play(FadeIn(As), )

        self.slide_break()

        ## Loop through edges
        # i = 0
        # A = As[i]
        # fact=LEUPFact(A,eloc[i], angle=angles[i], scale=matrix_scale)
        # fact.play_factorize(self)
        # self.slide_break()

        # first pass
        facts = []
        for i, A in enumerate(As):
            if i == 2:
                fast_kw["run_time"] = 0.1
                # self.slide_break()

            fact= LEUPFact(A,eloc[i], angle=angles[i], scale=matrix_scale) if esign[i] == 1 else PUELFact(A,eloc[i], angle=angles[i], scale=matrix_scale)
            fact.play_factorize(self, **fast_kw)
            if i < 2:
                self.slide_break()

            # next pass matrices to next edge, or pass off end of quiver
            # combine matrices on next edge
            # it is the U and P matrices that get passed
            if i < len(As) - 1:
                self.play(
                    fact.P.animate.move_to(npos[i+1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.P.animate.move_to(As[i+1]).rotate(-fact.angle),
                    fact.U.animate.move_to(npos[i+1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.U.animate.move_to(As[i+1]).rotate(-fact.angle),
                    FadeOut(fact.P),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.U),
                    **fast_kw
                )
            else:
                self.play(
                    fact.P.animate.move_to(npos[i+1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.P),
                    fact.U.animate.move_to(npos[i+1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.U),
                    **fast_kw
                )

            facts.append(fact)

            if i < 2:
                self.slide_break()

        fast_kw["run_time"] = 0.5
        self.slide_break()

        # second pass with L/EL commutations
        i = len(facts)
        for fact in reversed(facts):
            i = i-1

            if i == len(facts)-2:
                fast_kw["run_time"] = 0.1
                # self.slide_break()

            # pass L to left
            if i == 0:
                self.play(
                    fact.L.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(FadeOut(fact.L), **fast_kw)
            else:
                tind = (2 if esign[i-1] == 1 else 1)
                tind2 = (0 if esign[i-1] == 1 else 3)
                self.play(
                    fact.L.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.L.animate.move_to(facts[i-1].target_pos[tind]).rotate(-fact.angle),
                    **fast_kw
                )
                if i > len(facts)-3:
                    self.slide_break()

                self.play(FadeOutAndShift(fact.L, facts[i-1].target_pos[tind2] - fact.L.get_center()), **fast_kw)


        self.wait(1)


class ZigzagBackward(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }

    def construct(self):
        # title = Text("Leftward-Initial Algorithm",color=BLACK)
        # title.shift(3.5 * UP)
        # self.add(title)

        matrix_scale = 0.15
        fast_kw = {"run_time": 0.5}

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        put_on_anchor = lambda x, anch: x.next_to(anch,0*(UP+RIGHT),buff=0).shift(0.35*UP)

        # create nodes
        nodes = Grp(*[Dot(color=BLACK) for i in range(8)])
        nodes.shift(3.5*UP)
        npos = []
        for i, n in enumerate(nodes):
            n.shift(1*i * DOWN)
            if i % 2 == 0:
                n.shift(1.5*LEFT)
                npos.append(n.get_center() + 2*matrix_scale*LEFT)
            else:
                n.shift(1.5*RIGHT)
                npos.append(n.get_center() + 2*matrix_scale*RIGHT)
            #print(n.get_arc_center())

        # create edges
        es = []
        esign = [] # keep track of edge directions
        angles = []
        eloc = []
        for i in range(len(nodes)-1):
            if i % 2 == 0:
                # left arrow
                src = nodes[i+1].get_arc_center()
                trg = nodes[i].get_arc_center()
                esign.append(1)
            else:
                # right arrow
                src = nodes[i].get_arc_center()
                trg = nodes[i+1].get_arc_center()
                esign.append(-1)
            es.append(Arrow(src,trg, color=BLACK))
            eloc.append((src + trg) / 2)
            diff = src - trg
            angles.append(np.arctan2(diff[1], diff[0]))

        edges = Grp(*es)
        self.play(FadeIn(nodes), FadeIn(edges), )

        self.slide_break()

        # put a matrix over each edge
        As = Grp(*[Square(color=BLACK) for i in range(len(edges))])
        As.scale(matrix_scale)

        for i, A in enumerate(As):
            put_on_anchor(A, eloc[i])
            A.rotate(angles[i])

        self.play(FadeIn(As), )

        self.slide_break()

        ## Loop through edges
        # i = 0
        # A = As[i]
        # fact=LEUPFact(A,eloc[i], angle=angles[i], scale=matrix_scale)
        # fact.play_factorize(self)
        # self.slide_break()

        # first pass
        facts = []
        for i in reversed(range(len(As))):
            if i == len(As)-3:
                fast_kw["run_time"] = 0.1
                self.slide_break()

            A = As[i]
            fact= PLEUFact(A,eloc[i], angle=angles[i], scale=matrix_scale) if esign[i] == 1 else UELPFact(A,eloc[i], angle=angles[i], scale=matrix_scale)
            fact.play_factorize(self, **fast_kw)
            #self.slide_break()

            # next pass matrices to next edge, or pass off end of quiver
            # combine matrices on next edge
            # it is the U and P matrices that get passed
            if i > 0:
                self.play(
                    fact.P.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.P.animate.move_to(As[i-1]).rotate(-fact.angle),
                    fact.L.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.L.animate.move_to(As[i-1]).rotate(-fact.angle),
                    FadeOut(fact.P),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.L),
                    **fast_kw
                )
            else:
                self.play(
                    fact.P.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.P),
                    fact.L.animate.move_to(npos[i]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(fact.L),
                    **fast_kw
                )

            facts.append(fact)

        fast_kw["run_time"] = 0.5
        self.slide_break()

        #second pass with L/EL commutations
        i = len(facts)
        for fact in reversed(facts):
            i = i-1

            if i == len(As)-3:
                fast_kw["run_time"] = 0.1
                self.slide_break()

            # pass L to left
            if i == 0:
                self.play(
                    fact.U.animate.move_to(npos[-i-1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(FadeOut(fact.U), **fast_kw)
            else:
                tind = (2 if esign[i-1] == 1 else 1)
                tind2 = (0 if esign[i-1] == 1 else 3)
                self.play(
                    fact.U.animate.move_to(npos[-i-1]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(
                    fact.U.animate.move_to(facts[i-1].target_pos[tind]).rotate(-fact.angle),
                    **fast_kw
                )
                self.play(FadeOutAndShift(fact.U, fact.U.get_center() - facts[i-1].target_pos[tind2] ), **fast_kw)

        self.wait(1)


class ZigzagDivideConquer(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }

    def construct(self):
        # title = Text("Divide & Conquer Algorithm",color=BLACK)
        # title.shift(3.5 * UP)
        # self.add(title)

        matrix_scale = 0.15
        fast_kw = {"run_time": 0.2}

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        put_on_anchor = lambda x, anch: x.next_to(anch,0*(UP+RIGHT),buff=0).shift(0.35*UP)

        # create nodes
        nodes = Grp(*[Dot(color=BLACK) for i in range(8)])
        nodes.shift(3.5*UP)
        npos = []
        for i, n in enumerate(nodes):
            n.shift(1*i * DOWN)
            if i % 2 == 0:
                n.shift(1.5*LEFT)
                npos.append(n.get_center() + 2*matrix_scale*LEFT)
            else:
                n.shift(1.5*RIGHT)
                npos.append(n.get_center() + 2*matrix_scale*RIGHT)
            #print(n.get_arc_center())

        # create edges
        es = []
        esign = [] # keep track of edge directions
        angles = []
        eloc = []
        for i in range(len(nodes)-1):
            if i % 2 == 0:
                # left arrow
                src = nodes[i+1].get_arc_center()
                trg = nodes[i].get_arc_center()
                esign.append(1)
            else:
                # right arrow
                src = nodes[i].get_arc_center()
                trg = nodes[i+1].get_arc_center()
                esign.append(-1)
            es.append(Arrow(src,trg, color=BLACK))
            eloc.append((src + trg) / 2)
            diff = src - trg
            angles.append(np.arctan2(diff[1], diff[0]))

        edges = Grp(*es)
        self.play(FadeIn(nodes), FadeIn(edges), )

        self.slide_break()

        # put a matrix over each edge
        As = Grp(*[Square(color=BLACK) for i in range(len(edges))])
        As.scale(matrix_scale)

        for i, A in enumerate(As):
            put_on_anchor(A, eloc[i])
            A.rotate(angles[i])

        self.play(FadeIn(As), )

        self.slide_break()

        # first pass
        Lfacts = []
        Ufacts = []
        for i in range(len(As)//2):

            ui = -(1+i)
            print(i, ui)
            AL = As[i]
            AU = As[ui]
            Lfact= LEUPFact(AL,eloc[i], angle=angles[i], scale=matrix_scale) if esign[i] == 1 else PUELFact(AL,eloc[i], angle=angles[i], scale=matrix_scale)
            Ufact= PLEUFact(AU,eloc[ui], angle=angles[ui], scale=matrix_scale) if esign[ui] == 1 else UELPFact(AU,eloc[ui], angle=angles[ui], scale=matrix_scale)
            self.play(
                *Lfact.animations1(),
                *Ufact.animations1(),
                **fast_kw
            )
            self.play(
                *Lfact.animations2(),
                *Ufact.animations2(),
                **fast_kw
            )
            if i == 0:
                self.slide_break()

            # next pass matrices to next edge, or pass off end of quiver
            # combine matrices on next edge
            # it is the U and P matrices that get passed

            self.play(
                Lfact.P.animate.move_to(npos[i+1]).rotate(-Lfact.angle),
                Ufact.P.animate.move_to(npos[ui-1]).rotate(-Ufact.angle),
                **fast_kw
            )
            self.play(
                Ufact.P.animate.move_to(As[ui-1]).rotate(-Ufact.angle),
                Ufact.L.animate.move_to(npos[ui-1]).rotate(-Ufact.angle),
                Lfact.P.animate.move_to(As[i+1]).rotate(-Lfact.angle),
                Lfact.U.animate.move_to(npos[i+1]).rotate(-Lfact.angle),
                **fast_kw
            )
            self.play(
                Lfact.U.animate.move_to(As[i+1]).rotate(-Lfact.angle),
                FadeOut(Lfact.P),
                Ufact.L.animate.move_to(As[ui-1]).rotate(-Ufact.angle),
                FadeOut(Ufact.P),
                **fast_kw
            )
            self.play(
                FadeOut(Lfact.U),
                FadeOut(Ufact.L),
                **fast_kw
            )

            Lfacts.append(Lfact)
            Ufacts.append(Ufact)

        self.slide_break()
        # LQU factorization
        i = len(As)//2
        Cfact = UQLFact(As[i], eloc[i], angle=angles[i], scale=matrix_scale)
        Cfact.play_factorize(self, **fast_kw)
        self.slide_break()

        # now we begin the backward pass
        tind = (2 if esign[i-1] == 1 else 1)
        tind2 = (0 if esign[i-1] == 1 else 3)
        self.play(
            Cfact.U.animate.move_to(npos[i+1]).rotate(-Cfact.angle),
            Cfact.L.animate.move_to(npos[i]).rotate(-Cfact.angle),
            **fast_kw
        )
        self.play(
            Cfact.U.animate.move_to(Ufacts[-1].target_pos[tind]).rotate(-Cfact.angle),
            Cfact.L.animate.move_to(Lfacts[-1].target_pos[tind]).rotate(-Cfact.angle),
            **fast_kw
        )
        self.play(
            FadeOutAndShift(Cfact.U, Cfact.U.get_center() - Ufacts[-1].target_pos[tind2] ),
            FadeOutAndShift(Cfact.L, Lfacts[-1].target_pos[tind2] - Cfact.L.get_center() ),
            **fast_kw
        )


        #
        # #second pass with L/EL commutations
        i = len(Ufacts)
        for i in reversed(range(len(Ufacts))):
            Ufact = Ufacts[i]
            Lfact = Lfacts[i]
            # for Ufact, LFact in zip(reversed(Ufacts), reversed(Lfacts)):
            #     i = i-1

            # pass U/L off quiver
            if i == 0:
                self.play(
                    Ufact.U.animate.move_to(npos[-1]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(npos[0]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(Ufact.U),
                    FadeOut(Lfact.L),
                    **fast_kw
                )
            else:
                tind = (2 if esign[i-1] == 1 else 1)
                tind2 = (0 if esign[i-1] == 1 else 3)
                Ltind = (2 if esign[i-1] == 1 else 1)
                Ltind2 = (0 if esign[i-1] == 1 else 3)
                self.play(
                    Ufact.U.animate.move_to(npos[-i-1]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(npos[i]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    Ufact.U.animate.move_to(Ufacts[i-1].target_pos[tind]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(Lfacts[i-1].target_pos[Ltind]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOutAndShift(Ufact.U, Ufacts[i-1].target_pos[tind2] - Ufact.U.get_center() ),
                    FadeOutAndShift(Lfact.L, Lfacts[i-1].target_pos[Ltind2] - Lfact.L.get_center()),
                    **fast_kw
                )

        # finally, put in EL form

        self.wait(1)


class ZigzagTitle(SlideScene):
    CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }

    def construct(self):
        # title = Text("Divide & Conquer Algorithm",color=BLACK)
        # title.shift(3.5 * UP)
        # self.add(title)

        matrix_scale = 0.075
        fast_kw = {"run_time": 0.25}

        the_target_of = CreateMoveToTargetCtxtMgr(self)

        put_on_anchor = lambda x, anch: x.next_to(anch,0*(UP+RIGHT),buff=0).shift(0.5*0.35*UP)

        # create nodes
        nodes = Grp(*[Dot(color=BLACK) for i in range(14)])
        nodes.shift(2.75*UP+5*LEFT)
        npos = []
        for i, n in enumerate(nodes):
            n.shift(0.5*i * DOWN)
            if i % 2 == 0:
                n.shift(0.75*LEFT)
                npos.append(n.get_center() + 2*matrix_scale*LEFT)
            else:
                n.shift(0.75*RIGHT)
                npos.append(n.get_center() + 2*matrix_scale*RIGHT)
            #print(n.get_arc_center())

        # create edges
        es = []
        esign = [] # keep track of edge directions
        angles = []
        eloc = []
        for i in range(len(nodes)-1):
            if i % 2 == 0:
                # left arrow
                src = nodes[i+1].get_arc_center()
                trg = nodes[i].get_arc_center()
                esign.append(1)
            else:
                # right arrow
                src = nodes[i].get_arc_center()
                trg = nodes[i+1].get_arc_center()
                esign.append(-1)
            es.append(Arrow(src,trg, color=BLACK))
            eloc.append((src + trg) / 2)
            diff = src - trg
            angles.append(np.arctan2(diff[1], diff[0]))

        edges = Grp(*es)
        # self.play(FadeIn(nodes), FadeIn(edges), )
        self.add(nodes, edges, )

        # put a matrix over each edge
        As = Grp(*[Square(color=BLACK) for i in range(len(edges))])
        As.scale(matrix_scale)

        for i, A in enumerate(As):
            put_on_anchor(A, eloc[i])
            A.rotate(angles[i])

        self.play(FadeIn(As), )


        # first pass
        Lfacts = []
        Ufacts = []
        for i in range(len(As)//2):

            ui = -(1+i)
            print(i, ui)
            AL = As[i]
            AU = As[ui]
            Lfact= LEUPFact(AL,eloc[i], angle=angles[i], scale=matrix_scale) if esign[i] == 1 else PUELFact(AL,eloc[i], angle=angles[i], scale=matrix_scale)
            Ufact= PLEUFact(AU,eloc[ui], angle=angles[ui], scale=matrix_scale) if esign[ui] == 1 else UELPFact(AU,eloc[ui], angle=angles[ui], scale=matrix_scale)
            self.play(
                *Lfact.animations1(),
                *Ufact.animations1(),
                **fast_kw
            )
            self.play(
                *Lfact.animations2(),
                *Ufact.animations2(),
                **fast_kw
            )

            # next pass matrices to next edge, or pass off end of quiver
            # combine matrices on next edge
            # it is the U and P matrices that get passed

            self.play(
                Lfact.P.animate.move_to(npos[i+1]).rotate(-Lfact.angle),
                Ufact.P.animate.move_to(npos[ui-1]).rotate(-Ufact.angle),
                **fast_kw
            )
            self.play(
                Ufact.P.animate.move_to(As[ui-1]).rotate(-Ufact.angle),
                Ufact.L.animate.move_to(npos[ui-1]).rotate(-Ufact.angle),
                Lfact.P.animate.move_to(As[i+1]).rotate(-Lfact.angle),
                Lfact.U.animate.move_to(npos[i+1]).rotate(-Lfact.angle),
                **fast_kw
            )
            self.play(
                Lfact.U.animate.move_to(As[i+1]).rotate(-Lfact.angle),
                FadeOut(Lfact.P),
                Ufact.L.animate.move_to(As[ui-1]).rotate(-Ufact.angle),
                FadeOut(Ufact.P),
                **fast_kw
            )
            self.play(
                FadeOut(Lfact.U),
                FadeOut(Ufact.L),
                **fast_kw
            )

            Lfacts.append(Lfact)
            Ufacts.append(Ufact)

        # LQU factorization
        i = len(As)//2
        Cfact = LQUFact(As[i], eloc[i], angle=angles[i], scale=matrix_scale)
        Cfact.play_factorize(self, **fast_kw)

        # now we begin the backward pass
        tind = (2 if esign[i-1] == 1 else 1)
        tind2 = (0 if esign[i-1] == 1 else 3)
        self.play(
            Cfact.U.animate.move_to(npos[i+1]).rotate(-Cfact.angle),
            Cfact.L.animate.move_to(npos[i]).rotate(-Cfact.angle),
            **fast_kw
        )
        self.play(
            Cfact.U.animate.move_to(Ufacts[-1].target_pos[tind]).rotate(-Cfact.angle),
            Cfact.L.animate.move_to(Lfacts[-1].target_pos[tind]).rotate(-Cfact.angle),
            **fast_kw
        )
        self.play(
            FadeOutAndShift(Cfact.U, Ufacts[-1].target_pos[tind2] - Cfact.U.get_center() ),
            FadeOutAndShift(Cfact.L, Lfacts[-1].target_pos[tind2] - Cfact.L.get_center() ),
            **fast_kw
        )


        #
        # #second pass with L/EL commutations
        i = len(Ufacts)
        for i in reversed(range(len(Ufacts))):
            Ufact = Ufacts[i]
            Lfact = Lfacts[i]
            # for Ufact, LFact in zip(reversed(Ufacts), reversed(Lfacts)):
            #     i = i-1

            # pass U/L off quiver
            if i == 0:
                self.play(
                    Ufact.U.animate.move_to(npos[-1]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(npos[0]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOut(Ufact.U),
                    FadeOut(Lfact.L),
                    **fast_kw
                )
            else:
                tind = (2 if esign[i-1] == 1 else 1)
                tind2 = (0 if esign[i-1] == 1 else 3)
                Ltind = (2 if esign[i-1] == 1 else 1)
                Ltind2 = (0 if esign[i-1] == 1 else 3)
                self.play(
                    Ufact.U.animate.move_to(npos[-i-1]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(npos[i]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    Ufact.U.animate.move_to(Ufacts[i-1].target_pos[tind]).rotate(-Ufact.angle),
                    Lfact.L.animate.move_to(Lfacts[i-1].target_pos[Ltind]).rotate(-Lfact.angle),
                    **fast_kw
                )
                self.play(
                    FadeOutAndShift(Ufact.U, Ufact.U.get_center() - Ufacts[i-1].target_pos[tind2] ),
                    FadeOutAndShift(Lfact.L, Lfacts[i-1].target_pos[Ltind2] - Lfact.L.get_center()),
                    **fast_kw
                )

        # finally, put in EL form

        self.wait(3)
