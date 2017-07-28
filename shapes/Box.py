import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	matplotlib_obj = None
	def __init__(self, x, y, data, xlabel='x', ylabel='y', title=None, lw=2, mplprops={}, figure=None):
		self.x          = x
		self.y			= y
		self.data 		= data
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.title 		= title
		self.lw	        = lw
		self.mplprops   = mplprops

	def __draw__(self, zorder=1):
		for x, y, data, xlabel, ylabel, title in zip(self.x, self.y, self.data, self.xlabel, self.ylabel, self.title):
			plt.axis('on')
			plt.axis([self.x[0], self.x[1], self.y[0], self.y[1]])
			plt.title(self.title)
			plt.xlabel(self.xlabel)
			plt.ylabel(self.ylabel)
			plt.plot(self.data)
