import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Point:
	matplotlib_obj = None
	def __init__(self, fig, ax, xys, texts, pointsize=6, fontsize=12, colors='black', latex=True):
		if not isinstance(colors, list):
			colors = [colors]
			xys = [xys]
			texts = [texts]

		self.fig = fig
		self.ax = ax
		self.xys = xys
		self.colors = colors
		self.texts = texts


	def __draw__(self, zorder=1):
		for xy, text, color in zip(self.xys, self.texts, self.colors):
			plt.plot(xy[0], xy[1], 'o{}'.format(color), ms=pointsize, zorder=zorder)
			self.ax.annotate("$"+text+"$" if latex else text, xytext=xy, xy=xy,
			fontsize=fontsize, horizontalalignment='center',
			textcoords='offset points', zorder=zorder)
