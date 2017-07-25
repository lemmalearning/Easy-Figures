import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	def __init__(self, xy, xlabel='x', ylabel='y', lw=2, mplprops={}, figure=None):
		self.xy         = xy
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.lw	        = lw
		self.mplprops   = mplprops

	def __draw__(self, zorder=1):
		for xy, xlabel, ylabel, figure, lw in zip(self.xy, self.xlabel, self.ylabel, self.lw):
			plt.plot(xy[0], xy[1], xlabel=xlabel, ylabel=ylabel, lw=lw, zorder=zorder, **self.mplprops)
