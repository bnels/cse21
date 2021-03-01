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
    pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float)
    return pts.T

class RipsBalls(SlideScene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }

	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = RipsFiltration(pts)

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))

		F = filtration_from_bats(Fbats, pts, color=BLACK)

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
		# cs1 = [Circle(color=BLUE, radius=1.5, fill_opacity=0.2, arc_center=p) for p in pts]
		t = 0.5
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.slide_break()

		t = 1.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.slide_break()

		t = 2.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.slide_break()

		t = 3.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
		self.slide_break()

		t = 5.0
		anim = []
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		anim.extend(Transform_circle_radii(cs, t/2, **circle_opts))
		self.play(*anim)
