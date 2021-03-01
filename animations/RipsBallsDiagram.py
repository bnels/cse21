from manimlib.imports import *
import numpy as np
import bats
from manim_reveal import SlideScene

# import manimtda
from manimtda import *

def Transform_circle_radii(cs, r, **kwargs):
	"""
	transform each circle in cs to have radius r
	"""
	pts = [c.arc_center for c in cs]
	cs1 = [Circle(radius=r, arc_center=p, **kwargs) for p in pts]
	return [Transform(c0, c1) for c0, c1 in zip(cs, cs1)]

def gen_circle2(n, r=1.0):
    theta = np.linspace(0, 2*np.pi*(1 - 1./n), n)
    pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float, order='F')
    return pts.T

class RipsBallsDiagram(SlideScene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }

	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)
		pts = pts + 3*RIGHT[:-1]

		Fbats = RipsFiltration(pts)
		RFC2 = bats.ReducedFilteredChainComplex(Fbats, bats.F2())

		ps = RFC2.persistence_pairs(1)
		lens = []
		for p in ps:
			lens.append(p.death() - p.birth())
		i = np.argmax(lens)
		p = ps[i]
		v =  RFC2.representative(p)
		subcpx1 = [Fbats.complex().get_simplex(p.dim(),i) for i in v.nzinds()]

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)

		PD = barcode_from_bats(Fbats, [BLUE, RED], spacing=0.2)
		PD.shift(5*LEFT + UP)
		PD.scale_by(0.5)

		circle_opts = {"color":BLUE, "fill_opacity":0.2}
		ds = [Circle(radius=0.05, arc_center=p, color=BLACK, fill_opacity=1.0) for p in pts]
		self.play(
			*(FadeIn(d) for d in ds)
		)
		cs = [Circle(radius=0.1, arc_center=p, **circle_opts) for p in pts]
		self.play(
			*(FadeIn(c) for c in cs)
		)
		self.slide_break()

		for t in [0.5, 1.0, 2.0]:
			anim = []
			Ft = F.step_to(t)
			anim.append(FadeIn(Ft))
			anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
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
			anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
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

		# # cs1 = [Circle(color=BLUE, radius=1.5, fill_opacity=0.2, arc_center=p) for p in pts]
		# t = 0.5
		# anim = []
		# Ft = F.step_to(t)
		# anim.append(FadeIn(Ft))
		# anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		# self.play(*anim)
		# self.slide_break()
		#
		# t = 1.0
		# anim = []
		# Ft = F.step_to(t)
		# anim.append(FadeIn(Ft))
		# anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		# self.play(*anim)
		# self.slide_break()
		#
		# t = 2.0
		# anim = []
		# Ft = F.step_to(t)
		# anim.append(FadeIn(Ft))
		# anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		# self.play(*anim)
		# self.slide_break()
		#
		# t = 3.0
		# anim = []
		# Ft = F.step_to(t)
		# anim.append(FadeIn(Ft))
		# anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		# self.play(*anim)
		# self.slide_break()
		#
		# t = 5.0
		# anim = []
		# Ft = F.step_to(t)
		# anim.append(FadeIn(Ft))
		# anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		# self.play(*anim)
