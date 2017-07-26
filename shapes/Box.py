import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from random import randint, choice
from matplotlib.backends.backend_agg import FigureCanvasAgg
import numpy as np

class Box:
	matplotlib_obj = None
	def __init__(self, x, y, data, xlabel='x', ylabel='y', lw=2, mplprops={}, figure=None):
		self.x          = x
		self.y			= y
		self.data 		= data
		self.xlabel		= xlabel
		self.ylabel		= ylabel
		self.figure     = figure
		self.lw	        = lw
		self.mplprops   = mplprops

	def __draw__(self, zorder=1):
		#for xy, xlabel, ylabel in zip(self.xy, self.xlabel, self.ylabel):
			#plt.plot(xy[0], xy[1], xlabel=, ylabel=, zorder=zorder, **self.mplprops)

		"""
		objects = ('Python', 'C++', 'Java', 'Perl', 'Scala', 'Lisp')
		y_pos = np.arange(len(objects))
		performance = [10,8,6,4,2,1]

		plt.bar(y_pos, performance, align='center', alpha=0.5)
		plt.xticks(y_pos, objects)
		"""
		plt.plot(self.data)
		plt.axis('on')
		plt.axis([self.x[0], self.x[1], self.y[0], self.y[1]])
		plt.xlabel(self.xlabel)
		plt.ylabel(self.ylabel)
		plt.title('Gaussian colored noise')
		plt.show()
