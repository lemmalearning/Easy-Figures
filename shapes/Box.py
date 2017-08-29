import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	matplotlib_obj = None
	def __init__(self, x, y, xlabel, ylabel, title, lw, fontsize, mplprops, figure):
		self.x          = x
		self.y			= y
		#self.data 		= data
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.title 		= title
		self.lw	        = lw
		self.mplprops   = mplprops
		self.fontsize = fontsize

	def __draw__(self, zorder=None):
		plt.axis('on')
		plt.axis([self.x[0], self.x[1], self.y[0], self.y[1]])
		plt.tick_params(labelsize=self.fontsize/2.0)
		plt.title(self.title, fontsize=self.fontsize)
		plt.xlabel(self.xlabel, fontsize=self.fontsize)
		plt.ylabel(self.ylabel, fontsize=self.fontsize)
