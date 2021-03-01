from manimlib.imports import *
import numpy as np
import bats
# slide scene
from manim_reveal import SlideScene
# manim interface with bats
from manimtda import *

import matplotlib

from scipy.spatial import ConvexHull

def gen_circle2(n, r=1.0):
    theta = np.linspace(0, 2*np.pi*(1 - 1./n), n)
    pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float)
    return pts.T


def gen_point_cloud(n, scale=1.0):
	"""
	sample points on the unit square
	"""
	return np.random.uniform(low=-scale, high=scale, size=(n,2))


def get_dimension_filt(C):
	"""
	get dimension filtration data from bats complex
	"""
	spxs = []
	ts = []
	for d in range(C.maxdim() + 1):
		ts.extend([d for _ in range(C.ncells(d))])
		spxs.extend(C.get_simplices(d))

	return spxs, ts


def dimension_filtration_from_bats(C, pts, **kwargs):
	"""
	get manimtda filtration from bats filtration
	"""
	spxs, ts = get_dimension_filt(C)
	return SimplicialFiltration(pts, spxs, ts, **kwargs)


def get_convex_hull(s, pts, color=BLUE, **kwargs):
	"""
	get convex hull of pts[s] as a Manim polygon
	"""
	spts = np.array([pts[i] for i in s])
	hull_2d = ConvexHull(spts[:,:-1])
	P = Polygon(*[spts[i] for i in hull_2d.vertices],
				color=color,
				**kwargs
				)
	P.set_fill(color, opacity=0.2)
	#P.round_corners(0.05)
	#P.scale(1.3)
	return P


def get_convex_hull_barycenter(s, pts):
	"""
	get barycenter of convex hull
	"""
	spts = np.array([pts[i] for i in s])
	hull_2d = ConvexHull(spts[:,:-1])
	hull_pts = spts[hull_2d.vertices]
	return np.mean(hull_pts, axis=0)



class Nerve(SlideScene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
	def construct(self):
		# pts = gen_circle2(20, r=2.5)
		# pts = pts + np.random.normal(scale=0.2, size=pts.shape)
		pts = gen_point_cloud(100, scale=2.5)

		# put points into bats
		pbats = bats.DataSet(bats.Matrix(pts))
		# get landmarks
		lbats = bats.greedy_landmarks(pbats, 3, bats.Euclidean(), 0)
		lms = np.array(lbats.data()) # numpy array
		# get cover based on landmarks - assign each point to nearest landmarks
		cover = bats.landmark_eps_cover(pbats, lbats, bats.LInfDist(), 0.7)

		# construct the nerve
		N = bats.Nerve(cover, 2)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = bats.RipsFiltration(pbats, bats.Euclidean(), 0.0, 2)
		RFC = bats.ReducedFilteredChainComplex(Fbats, bats.F2())

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))
		lms = np.hstack((lms, np.zeros((lms.shape[0], 1))))
		bcs = np.array([get_convex_hull_barycenter(s, pts) for s in cover])
		print([len(s) for s in cover])
		print(bcs)

		# this is just for point cloud
		F = filtration_from_bats(Fbats, pts, color=BLACK)
		F.shift(3*RIGHT)

		# construct filtration on Nerve
		FN = dimension_filtration_from_bats(N, bcs, color=RED, tri_opacity=0.4)
		FN.shift(3*RIGHT)

		# this just generates the point cloud
		title = TexMobject(r"\text{Nerve of a Cover }\mathcal{N}(\mathcal{U})", color=BLACK).shift(3*UP)
		t = 0.0
		anim = [FadeIn(title)]
		Ft = F.step_to(t)
		anim.append(FadeIn(Ft))
		self.play(*anim)
		self.slide_break()

		# show the open sets
		line0 = TexMobject(r"\mathcal{U}", r"=\{U_0, U_1, U_2\}", color=BLACK).shift(3*LEFT + 1*UP)
		anim = [FadeIn(line0)]
		hulls = [get_convex_hull(cover[i], pts).shift(3*RIGHT) for i in range(len(cover))]
		anim.extend([FadeInFrom(h, DOWN) for h in hulls])
		self.play(*anim)
		self.slide_break()

		# now let's highlight the barycenters
		line1 = TexMobject(r"U_0, U_1, U_2 \in \mathcal{N}(\mathcal{U})_0", color=BLACK)
		line1.next_to(line0, DOWN)
		anim = [FadeIn(line1)]
		Nt = FN.step_to(0)
		anim.append(FadeIn(Nt))
		self.play(*anim)
		self.slide_break()

		# add 1 simplices of Nerve
		line2 = TexMobject(r"(U_i, U_j) \in \mathcal{N}(\mathcal{U})_1", color=BLACK)
		line2a = TexMobject(r"\text{if }~U_i \cap U_j \ne \emptyset", color=BLACK)
		line2.next_to(line0, DOWN)
		line2a.next_to(line2, DOWN)
		anim = [Transform(line1, line2), FadeIn(line2a)]
		Nt = FN.step_to(1)
		anim.append(FadeIn(Nt))
		self.play(*anim)
		self.slide_break()

		# add 2-simplices of nerve
		line3 = TexMobject(r"(U_i, U_j, U_k) \in \mathcal{N}(\mathcal{U})_2", color=BLACK)
		line3a = TexMobject(r"\text{if }~U_i \cap U_j \cap U_k \ne \emptyset", color=BLACK)
		line3.next_to(line0, DOWN)
		line3a.next_to(line3, DOWN)
		anim = [Transform(line1, line3), Transform(line2a, line3a)]
		Nt = FN.step_to(2)
		anim.append(FadeIn(Nt))
		self.play(*anim)
		self.slide_break()
