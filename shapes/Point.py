import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Point:
	matplotlib_obj = None
	def __init__(self, xys, texts, pointsize=6, fontsize=12, color='black', latex=True, mplprops={}, figure=None):
		if not isinstance(color, list):
			color = [color]
			xys = [xys]
			texts = [texts]

		self.xys = xys
		self.color = color
		self.texts = texts
		self.pointsize = pointsize
		self.fontsize = fontsize
		self.latex = latex
		self.figure = figure
		self.mplprops = mplprops

	def __draw__(self, zorder=1):
		for xy, text, color in zip(self.xys, self.texts, self.color):
			plt.plot(xy[0], xy[1], 'o', color=color, ms=self.pointsize, zorder=zorder)
			self.figure.ax.annotate("$"+text+"$" if self.latex else text, xytext=xy, xy=xy,
			fontsize=self.fontsize, horizontalalignment='center',
			textcoords='offset points', zorder=zorder, **self.mplprops)
