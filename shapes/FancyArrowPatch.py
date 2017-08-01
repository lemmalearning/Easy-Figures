import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

class FancyArrowPatch:
	def __init__(self, posA=None, posB=None, path=None, lw=1, arrowstyle='simple', connectionstyle='bar', mutation_scale=3, mplprops={}, figure=None):
		self.posA = posA
		self.posB = posB
		self.path = path
		self.lw = lw
		self.arrowstyle = arrowstyle
		self.connectionstyle = connectionstyle
		self.mutation_scale = mutation_scale
		self.mplprops = mplprops
		self.figure = figure

		fancyArrow = patches.FancyArrowPatch(posA, posB, path, arrowstyle, connectionstyle, mutation_scale = self.mutation_scale, lw=lw, **self.mplprops)
		self.matplotlib_obj = fancyArrow

	def __draw__(self, zorder=1):
		p = self.figure.ax.add_patch(self.matplotlib_obj)
		p.set(zorder=zorder)
