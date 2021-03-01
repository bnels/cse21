from manimlib.imports import *
import numpy as np
import scipy as sp
from scipy.spatial.distance import pdist, squareform

class SimplicialComplex(VGroup):
	def __init__(
		self,
		points,
		simplices,
		times,
		tri_opacity=0.2,
		**kwargs
	):
		super().__init__(**kwargs)

		self.current_time = -np.inf

		self.pts = points
		self.tri_opacity=tri_opacity

		self.time = []
		self.dims = []

		for (s, t) in zip(simplices, times):
			self.add_simplex(s, t, **kwargs)

	def time_steps(self):
		return np.unique(self.time)


	def last_time(self):
		return np.max(self.time)


	def step_to(self, t):
		newgp = VGroup(*[self[i] for i in range(len(self.time)) if self.current_time < self.time[i] <= t])
		self.current_time = t
		return newgp


	def get_time(self):
		return self.current_time


	def reset_time(self):
		self.current_time = -np.inf
		return self.current_time


	def at_time(self, t):
		return VGroup(*[self[i] for i in range(len(self.time)) if self.time[i] <= t])


	def add_simplex(self, spx, t, **kwargs):
		print("adding ", spx)
		if len(spx) == 1:
			# add dot
			self.add(
				Dot(self.pts[spx[0]], **kwargs)
			)
			self.time.append(t)
			self.dims.append(0)

		elif len(spx) == 2:
			# add edge
			self.add(
				Line(
					self.pts[spx[0]],
					self.pts[spx[1]],
					**kwargs
				)
			)
			self.time.append(t)
			self.dims.append(1)

		elif len(spx) == 3:
			# add triangle
			self.add(
				Polygon(
					*[self.pts[i] for i in spx],
					**kwargs
				).set_fill(self.color, opacity=self.tri_opacity)
			)
			self.time.append(t)
			self.dims.append(2)

		else:
			raise ValueError


def get_Rips_filtration(pts, tmax=np.inf):
	pts = np.array(pts)
	simplices = []
	times = []
	n = len(pts)
	dists = squareform(pdist(pts))

	for i in range(n):
		simplices.append([i])
		times.append(0)

	for i in range(n):
		for j in range(i):
			simplices.append([j,i])
			times.append(dists[i,j])

	for i in range(n):
		for j in range(i):
			for k in range(j):
				simplices.append([k, j,i])
				times.append(np.max([dists[i,j], dists[i,k], dists[j,k]]))

	return simplices, times


def gen_circle(n=10, r=3):
	theta = [2*np.pi * i/n for i in range(n)]
	pts = [[r*np.cos(t), r*np.sin(t), 0] for t in theta]
	return np.array(pts)

def gen_circle2(n, r=1.0):
	#theta = np.linspace(0, 2*np.pi*(1 - 1./n), n)
	theta = [2*np.pi * i/n for i in range(n)]
	pts = [[r*np.cos(t), r*np.sin(t), 0] for t in theta]
	#pts = np.array([r*np.cos(theta), r*np.sin(theta)],  dtype=np.float, order='F')
	return np.array(pts)


class Title(Scene):
	CONFIG={
        "camera_config":{"background_color":"#F0F1EB"},
    }
	def construct(self):
		pts = gen_circle2(20, r=2.5)
		pts = pts + np.random.normal(scale=0.2, size=pts.shape)

		simplices, times = get_Rips_filtration(pts)

		X = SimplicialComplex(pts,simplices,times, tri_opacity=0.1, color=BLUE) #.move_to(3*RIGHT)

		anim = []
		maxt = X.last_time()
		for t in X.time_steps():
			print(t)
			Xt = X.step_to(t)
			anim.append(FadeIn(
				Xt,
				rate_func=squish_rate_func(linear, t/(t+1), 1),
				run_time=t+1)
			)
			# anim.append(*self.compile_play_args_to_animation_list(
			# 	Xt.set_color,
			# 	BLUE,
			# 	rate_func=squish_rate_func(linear, (t+1)/(t+2), 1),
			# 	run_time=t+2
			# )
			# )

		self.play(*anim)
		self.wait(3)

		T = Polygon(*(X.pts), color=BLUE, fill_opacity=1.0)
		self.play(Transform(X, T))

		self.play(FadeOut(X), run_time=3)
		self.wait(2)
