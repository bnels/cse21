from manimlib.imports import *
import numpy as np
import bats
from manim_reveal import SlideScene

# import manimtda
from manimtda import *

def gen_circle2(n, r=1.0):
    theta = np.linspace(0, 2*np.pi*(1 - 1./n), n)
    pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float, order='F')
    return pts.T

class RipsDiagram(SlideScene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)
		FC2 = bats.FilteredF2ChainComplex(Fbats)
		RFC2 = bats.ReducedFilteredF2ChainComplex(FC2)

		ps = RFC2.persistence_pairs(1)
		lens = []
		for p in ps:
			lens.append(p.death() - p.birth())
		i = np.argmax(lens)
		p = ps[i]
		v =  RFC2.representative(p)
		subcpx1 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]

		PD = barcode_from_bats(Fbats, [BLUE, RED], spacing=0.2)
		PD.shift(5*LEFT + UP)
		PD.scale_by(0.5)

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)
		F.shift(3*RIGHT)

		t = 0.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		self.play(*anim)
		self.slide_break()

		for t in [0.5, 1.0, 2.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.slide_break()

		# animate coloring of subcomplex
		SC = F.get_subcomplex(subcpx1)
		self.play(
			SC.set_color,
			RED
		)
		self.slide_break()
		self.play(
			SC.set_color,
			BLACK
		)

		for t in [3.0, 5.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(PD.step_to(t))
			self.play(*anim)
			self.slide_break()

		PPs = AbstractPairs([2,2], [BLUE, RED]).shift(3*LEFT)
		self.play(Transform(PD, PPs))
		self.wait(2)
		self.slide_break()

		PD2 = diagram_from_bats(Fbats, [BLUE, RED])
		PD2.shift(5*LEFT + DOWN)
		PD2.scale_by(0.5)
		PD2.step_to(5.0)

		self.play(Transform(PD, PD2))
