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

def get_zzbar(k, color=BLUE):
	ZZbar = VGroup(
		Dot(3*LEFT, color=color),
		Dot(ORIGIN, color=color),
		Dot(3*RIGHT, color=color),
		Line(3*LEFT, ORIGIN, color=color),
		Line(ORIGIN, 3*RIGHT, color=color)
	)
	label = TexMobject("H_{}".format(k), color=color)
	label.next_to(ZZbar, LEFT)
	return VGroup(ZZbar, label)


def get_convex_hull_barycenter(s, pts):
	"""
	get barycenter of convex hull
	"""
	spts = np.array([pts[i] for i in s])
	hull_2d = ConvexHull(spts[:,:-1])
	hull_pts = spts[hull_2d.vertices]
	return np.mean(hull_pts, axis=0)



class ZigzagNerve(SlideScene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
        "video_slides_dir":"../video_slides"
    }
	def construct(self):
		pts = gen_circle2(60, r=2.5)
		pts = pts + np.random.normal(scale=0.15, size=pts.shape)
		# pts = gen_point_cloud(100, scale=2.5)

		# put points into bats
		pbats = bats.DataSet(bats.Matrix(pts))
		# get landmarks
		lbats = bats.greedy_landmarks(pbats, 3, bats.Euclidean(), 0)
		lbats2 = bats.greedy_landmarks(pbats, 3, bats.Euclidean(), 5)
		lms = np.array(lbats.data()) # numpy array
		# get cover based on landmarks - assign each point to nearest landmarks
		coverU = bats.landmark_eps_cover(pbats, lbats, bats.LInfDist(), 1.0)
		coverV = bats.landmark_eps_cover(pbats, lbats2, bats.LInfDist(), 1.0)
		coverUV, fU, fV = bats.bivariate_cover(coverU, coverV)

		# Fbats = WeakAlphaFiltration(pts)
		Fbats = bats.RipsFiltration(pbats, bats.Euclidean(), 0.0, 2)
		RFC = bats.ReducedFilteredChainComplex(Fbats, bats.F2())

		pts = np.hstack((pts, np.zeros((pts.shape[0], 1))))
		lms = np.hstack((lms, np.zeros((lms.shape[0], 1))))
		# compute barycenters of hulls
		bcU = np.array([get_convex_hull_barycenter(s, pts) for s in coverU])
		bcV = np.array([get_convex_hull_barycenter(s, pts) for s in coverV])
		bcUV = np.array([get_convex_hull_barycenter(s, pts) for s in coverUV])

		# this is just for point cloud
		F = filtration_from_bats(Fbats, pts, color=BLACK)
		F.shift(3*RIGHT)


		#title = TextMobject(r"Comparing Covers", color=BLACK).shift(3.5*UP)
		anim = []
		# this just generates the point cloud
		Pcloud = F.step_to(0)
		anim.append(FadeIn(Pcloud))
		self.play(*anim)
		self.slide_break()

		# show the open sets in U
		line0 = TexMobject(r"\mathcal{U}", r"=\{U_0, U_1, U_2\}", color=BLACK).shift(3*LEFT + 1*UP)
		anim = [FadeIn(line0)]
		hulls = [get_convex_hull(coverU[i], pts).shift(3*RIGHT) for i in range(len(coverU))]
		hullsU = VGroup(*hulls)
		anim.extend([FadeInFrom(h, DOWN) for h in hulls])
		self.play(*anim)
		self.slide_break()

		# show the other cover V
		line1 = TexMobject(r"\mathcal{V}", r"=\{V_0, V_1, V_2\}", color=BLACK).shift(3*LEFT + 1*UP)
		line1.next_to(line0, DOWN)
		anim = [FadeIn(line1)]
		hulls = [get_convex_hull(coverV[i], pts, color=RED).shift(3*RIGHT) for i in range(len(coverV))]
		hullsV = VGroup(*hulls)
		anim.extend([FadeInFrom(h, DOWN) for h in hulls])
		self.play(*anim)
		self.slide_break()


		line2 = TexMobject(r"\mathcal{U} \times_X \mathcal{V}", color=BLACK).shift(3*LEFT + 1*UP)
		line2.next_to(line1, DOWN)
		anim = [FadeIn(line2)]
		hulls = [get_convex_hull(coverUV[i], pts, color=PURPLE).shift(3*RIGHT) for i in range(len(coverUV))]
		hullsUV = VGroup(*hulls)
		anim.extend([FadeOut(hullsU), FadeOut(hullsV), FadeInFrom(hullsUV, UP)])
		self.play(*anim)
		self.slide_break()

		anim = [FadeOut(Pcloud), FadeOut(hullsUV)]
		line0a = TexMobject(r"\mathcal{U}", color=BLACK).move_to((-3,2.5,0))
		line1a = TexMobject(r"\mathcal{V}", color=BLACK).move_to((3,2.5,0))
		# anim.append(ApplyMethod(line0.move_to, (-3,2.5,0)))
		# anim.append(ApplyMethod(line1.move_to, (3,2.5,0)))
		anim.append(Transform(line0, line0a))
		anim.append(Transform(line1, line1a))
		anim.append(ApplyMethod(line2.move_to, (0,2.5,0)))
		self.play(*anim)
		self.slide_break()

		# shift and scale hulls
		hullsU.shift(6*LEFT)
		hullsUV.shift(3*LEFT)

		hullsU.scale(0.3)
		hullsV.scale(0.3)
		hullsUV.scale(0.3)
		self.play(FadeIn(hullsU), FadeIn(hullsV), FadeIn(hullsUV))
		self.slide_break()

		# Nerve Functor

		# construct nerves
		NU = bats.Nerve(coverU, 2)
		NV = bats.Nerve(coverV, 2)
		NUV = bats.Nerve(coverUV, 2)

		# construct filtration on Nerve
		FU = dimension_filtration_from_bats(NU, bcU, color=BLUE, tri_opacity=0.4)
		FU.shift(3*LEFT)
		FU.scale(0.3)
		CU = FU.step_to(2)
		labelU = TexMobject(r"\mathcal{N}(\mathcal{U})", color=BLACK).move_to((-3,2.5,0))

		# construct filtration on Nerve
		FV = dimension_filtration_from_bats(NV, bcV, color=RED, tri_opacity=0.4)
		FV.shift(3*RIGHT)
		FV.scale(0.3)
		CV = FV.step_to(2)
		labelV = TexMobject(r"\mathcal{N}(\mathcal{V})", color=BLACK).move_to((3,2.5,0))

		# construct filtration on Nerve
		FUV = dimension_filtration_from_bats(NUV, bcUV, color=PURPLE, tri_opacity=0.4)
		FUV.scale(0.3)
		CUV = FUV.step_to(2)
		labelUV = TexMobject(r"\mathcal{N}(\mathcal{U}, \mathcal{V})", color=BLACK).move_to((0,2.5,0))

		anim = [Transform(hullsU, CU), Transform(hullsV, CV), Transform(hullsUV, CUV)]
		anim.extend([Transform(line0, labelU), Transform(line1, labelV), Transform(line2, labelUV)])
		self.play(*anim)
		self.slide_break()

		# arrows for maps
		arU = TexMobject(r"\xleftarrow{p_U}",color=BLACK).move_to((-1.5,2.5,0))
		arV = TexMobject(r"\xrightarrow{p_V}",color=BLACK).move_to((1.5,2.5,0))
		arUc = TexMobject(r"\xleftarrow{}",color=BLACK).move_to((-1.5,0,0))
		arVc = TexMobject(r"\xrightarrow{}",color=BLACK).move_to((1.5,0,0))
		self.play(*[FadeIn(ar) for ar in [arU, arV, arUc, arVc]])
		self.slide_break()

		# apply homology functor

		homtxt = TexMobject(
			r"H_k(\mathcal{N}(\mathcal{U}))",
			r"\xleftarrow{H_k(p_U)}",
			r"H_k(\mathcal{N}(\mathcal{U}, \mathcal{V}))",
			r"\xrightarrow{H_k(p_V)}",
			r"H_k(\mathcal{N}(\mathcal{V}))",
			color=BLACK
		).shift(2.5*UP)
		homtxt1 = TexMobject(r"H_k(\mathcal{N}(\mathcal{U}))", color=BLACK)
		homtxt2 = TexMobject(r"\xleftarrow{H_k(p_U)}", color=BLACK)
		homtxt3 = TexMobject(r"H_k(\mathcal{N}(\mathcal{U}, \mathcal{V}))", color=BLACK).shift(2.5*UP)
		homtxt4 = TexMobject(r"\xrightarrow{H_k(p_V)}", color=BLACK)
		homtxt5 = TexMobject(r"H_k(\mathcal{N}(\mathcal{V}))", color=BLACK)
		homtxt2.next_to(homtxt3, LEFT)
		homtxt1.next_to(homtxt2, LEFT)
		homtxt4.next_to(homtxt3, RIGHT)
		homtxt5.next_to(homtxt4, RIGHT)
		# arUh = TexMobject(r"\xleftarrow{H_k(p_U)}",color=BLACK).move_to((-1.5,2.5,0))
		# arVh = TexMobject(r"\xrightarrow{H_k(p_V)}",color=BLACK).move_to((1.5,2.5,0))
		# labelUh = TexMobject(r"H_k(\mathcal{N}(\mathcal{U}))", color=BLACK).move_to((-3,2.5,0))
		# labelVh = TexMobject(r"H_k(\mathcal{N}(\mathcal{V}))", color=BLACK).move_to((3,2.5,0))
		# labelUVh = TexMobject(r"H_k(\mathcal{N}(\mathcal{U}, \mathcal{V}))", color=BLACK).move_to((0,2.5,0))

		# produce zigzag barcode
		ZZ0 = get_zzbar(0, color=BLUE)
		ZZ0.shift(2*DOWN)
		ZZ1 = get_zzbar(1, color=RED)
		ZZ1.shift(3*DOWN)



		dgrp =VGroup(line0, arU, line2, arV, line1)
		anim = [ Transform( dgrp, homtxt), ShowCreation(ZZ0), ShowCreation(ZZ1)]
		# anim = [ FadeOut( dgrp), FadeIn(homtxt), ShowCreation(ZZ0), ShowCreation(ZZ1)]
		#anim.extend([FadeOut(l) for l in [arU, arV, label0, label1, label2]])

		self.play(*anim)
		self.wait()
