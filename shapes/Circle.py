import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Circle:
	matplotlib_obj = None
	def __init__(self, xy=(0,0), diameter=None, radius=None, label="", fc='none', ec='k', props={}, figure=None):
		self.figure = figure
		self.props = props
		if radius!=None:
			circle = patches.Circle(xy, radius=radius, fc=fc, ec=ec, linewidth=3, **self.props)
			self.matplotlib_obj = circle
			if label != "":
				p = (xy[0]+radius, xy[1])
				plt.plot([xy[0],p[0]], [xy[1],p[1]], linewidth=2, ls='dashed', color='black')

				mid_radius = (xy[0]+p[0])/2.0
				textobj = figure.ax.text(mid_radius, xy[1]*1.015, '$'+label+'$', fontsize=.0625*self.figure.width, horizontalalignment='center')


		else:
			circle = patches.Circle(xy, radius=diameter/2, fc=fc, ec=ec, linewidth=3, **self.props)
			self.matplotlib_obj = circle
			if label != "":
				p1 = (xy[0]-diameter/2, xy[1])
				p2 = (xy[0]+diameter/2, xy[1])
				plt.plot([p1[0],p2[0]], [p1[1],p2[1]], linewidth=2, ls='dashed', color='black')

				textobj = self.figure.ax.text(xy[0], xy[1]*1.015, '$'+label+'$', fontsize=.0625*self.figure.width, horizontalalignment='center')


	def __draw__(self, zorder=1):
		c = self.figure.ax.add_patch(self.matplotlib_obj)
		c.set(zorder=zorder)
